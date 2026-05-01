"""
The Builders' Kit — Approval Queue.

Portable implementation of the irreversible-action gating primitive that
appears in TOP's tools/approvals.py and Operator's tools/approvals.py.
Both products converge on the same shape (queue → list pending → approve
or reject → execute) but differ on execution timing: TOP auto-executes
on approve, Operator separates approve from execute. The chassis
supports both via configuration.

Doctrine invariants this module preserves (non-negotiable):

  1. No irreversible action runs without explicit human approval, except
     for action types in the auto_execute_types allowlist (intended for
     admin-only system actions like prompt updates).
  2. Approve and reject are terminal-state transitions. A rejected
     action cannot be later approved without re-queuing.
  3. Execution failures are recorded; the action moves to a failed
     terminal state, not back to approved.
  4. Per-user isolation: when user_id is set on a queued action, list
     and approve operations can be filtered by user. The chassis does
     NOT enforce isolation — that is the caller's contract — but it
     provides the primitive.

Usage:

    from kit.chassis import ApprovalQueue, JsonFileStore

    # Register executors per action type
    def execute_send_email(action):
        send_email(**action.payload)
        return f"Email sent to {action.payload['to']}"

    queue = ApprovalQueue(
        store=JsonFileStore(Path("data/pending_approvals.json")),
        executors={"send_email": execute_send_email},
        auto_execute_on_approve=True,            # TOP-style
    )

    # In a tool that wants to gate an action:
    action = queue.queue(
        action_type="send_email",
        summary="Email Jane re: meeting time",
        payload={"to": "jane@example.com", "subject": "...", "body": "..."},
    )
    # → Action(id='a3f8b1c2', type='send_email', status='pending', ...)

    # Later, when the human approves via Telegram / dashboard / CLI:
    queue.approve(action.id)
    # → executes the registered executor and transitions to 'executed'
"""

from __future__ import annotations

import json
import logging
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional, Protocol

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Action
# ──────────────────────────────────────────────────────────────────────────────

PENDING = "pending"
APPROVED = "approved"
REJECTED = "rejected"
EXECUTED = "executed"
FAILED = "failed"

TERMINAL_STATUSES = frozenset({REJECTED, EXECUTED, FAILED})


@dataclass
class Action:
    """One queued action. Mutable in-place — the queue manages transitions."""
    id: str
    type: str
    summary: str
    payload: dict
    status: str = PENDING
    created_at: str = ""
    resolved_at: Optional[str] = None
    user_id: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Action":
        # Tolerant of extra keys; ignore them so old persisted actions still load.
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in d.items() if k in known})

    @property
    def is_pending(self) -> bool:
        return self.status == PENDING

    @property
    def is_terminal(self) -> bool:
        return self.status in TERMINAL_STATUSES


# ──────────────────────────────────────────────────────────────────────────────
# Storage
# ──────────────────────────────────────────────────────────────────────────────

class Store(Protocol):
    """Storage backend contract. Implement load() and save()."""
    def load(self) -> list[Action]: ...
    def save(self, actions: list[Action]) -> None: ...


class InMemoryStore:
    """In-memory store. Loses state on process exit. Good for tests + smoke."""
    def __init__(self) -> None:
        self._actions: list[Action] = []

    def load(self) -> list[Action]:
        # Return a shallow copy so callers can mutate without disturbing state.
        return list(self._actions)

    def save(self, actions: list[Action]) -> None:
        self._actions = list(actions)


class JsonFileStore:
    """JSON-file store with atomic writes. Default for production use."""
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[Action]:
        if not self.path.exists():
            return []
        try:
            with self.path.open("r", encoding="utf-8") as fh:
                raw = json.load(fh)
        except (json.JSONDecodeError, OSError):
            logger.warning(f"approval queue: failed to load {self.path}; "
                           f"starting empty")
            return []
        if not isinstance(raw, list):
            return []
        return [Action.from_dict(d) for d in raw if isinstance(d, dict)]

    def save(self, actions: list[Action]) -> None:
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump([a.to_dict() for a in actions], fh, indent=2)
        tmp.replace(self.path)


# ──────────────────────────────────────────────────────────────────────────────
# Hooks
# ──────────────────────────────────────────────────────────────────────────────

Hook = Callable[[Action], None]
Executor = Callable[[Action], str]


# ──────────────────────────────────────────────────────────────────────────────
# ApprovalQueue
# ──────────────────────────────────────────────────────────────────────────────

class ApprovalQueue:
    """
    The portable approval queue. Configure once per product; call queue()
    before any irreversible action; approve()/reject() from the human's
    decision channel.
    """

    def __init__(
        self,
        store: Optional[Store] = None,
        *,
        executors: Optional[dict[str, Executor]] = None,
        auto_execute_types: Optional[set[str]] = None,
        auto_execute_on_approve: bool = True,
        on_queue: Optional[Hook] = None,
        on_approve: Optional[Hook] = None,
        on_reject: Optional[Hook] = None,
        on_execute: Optional[Hook] = None,
    ) -> None:
        """
        Args:
            store: Persistence backend. Defaults to InMemoryStore.
            executors: action_type → callable(action) -> result_string.
                Registered executors run on approve (when
                auto_execute_on_approve=True) or on explicit execute().
            auto_execute_types: action_types that bypass the queue and
                run immediately. Use sparingly — admin-only system
                actions like prompt updates.
            auto_execute_on_approve: When True (TOP-style), approve()
                transitions directly to executed/failed via the registered
                executor. When False (Operator-style), approve() stops at
                'approved' and the caller must explicitly call execute().
            on_queue / on_approve / on_reject / on_execute: hooks fired
                after each transition. Failures are logged; never raise
                back to the caller. Use for Telegram alerts, AAR
                resolution, audit logs.
        """
        self.store = store or InMemoryStore()
        self.executors: dict[str, Executor] = dict(executors or {})
        self.auto_execute_types = set(auto_execute_types or [])
        self.auto_execute_on_approve = auto_execute_on_approve
        self.on_queue = on_queue
        self.on_approve = on_approve
        self.on_reject = on_reject
        self.on_execute = on_execute
        # Serialize all read-modify-write cycles. The doctrine's approval
        # gate cannot tolerate races where two approvers see the same
        # action and both transition it.
        self._lock = threading.RLock()

    # ── Queue ────────────────────────────────────────────────────────────────

    def queue(
        self,
        action_type: str,
        summary: str,
        payload: dict,
        *,
        user_id: Optional[str] = None,
    ) -> Action:
        """Queue an action. If action_type is in auto_execute_types, runs
        immediately and returns the action in 'executed' (or 'failed') state.
        """
        if action_type in self.auto_execute_types:
            action = Action(
                id=_new_id(),
                type=action_type,
                summary=summary,
                payload=dict(payload),
                status=APPROVED,                    # implicit
                created_at=_now_iso(),
                resolved_at=_now_iso(),
                user_id=user_id,
            )
            self._execute_in_place(action)
            with self._lock:
                actions = self.store.load()
                actions.append(action)
                self.store.save(actions)
            self._fire(self.on_execute, action)
            return action

        action = Action(
            id=_new_id(),
            type=action_type,
            summary=summary,
            payload=dict(payload),
            status=PENDING,
            created_at=_now_iso(),
            user_id=user_id,
        )
        with self._lock:
            actions = self.store.load()
            actions.append(action)
            self.store.save(actions)
        self._fire(self.on_queue, action)
        return action

    # ── Read ─────────────────────────────────────────────────────────────────

    def list_pending(self, *, user_id: Optional[str] = None) -> list[Action]:
        """Return all pending actions, optionally filtered to a user."""
        with self._lock:
            actions = self.store.load()
        pending = [a for a in actions if a.is_pending]
        if user_id is not None:
            pending = [a for a in pending if a.user_id == user_id]
        return pending

    def get(self, action_id: str) -> Optional[Action]:
        """Return the action with this id, or None."""
        with self._lock:
            actions = self.store.load()
        for a in actions:
            if a.id == action_id:
                return a
        return None

    # ── Transitions ──────────────────────────────────────────────────────────

    def approve(self, action_id: str) -> Action:
        """
        Approve a pending action. Raises ValueError if the action is missing
        or already terminal.

        If auto_execute_on_approve is True (default), this also runs the
        registered executor and transitions the action to executed/failed.
        Otherwise the action stops at 'approved' and the caller must call
        execute() explicitly.
        """
        with self._lock:
            actions = self.store.load()
            target = _find_pending_or_raise(actions, action_id)
            target.status = APPROVED
            target.resolved_at = _now_iso()
            self.store.save(actions)

        self._fire(self.on_approve, target)

        if self.auto_execute_on_approve:
            self._execute_action(target)

        return target

    def reject(self, action_id: str) -> Action:
        """Reject a pending action. Raises if missing or already terminal."""
        with self._lock:
            actions = self.store.load()
            target = _find_pending_or_raise(actions, action_id)
            target.status = REJECTED
            target.resolved_at = _now_iso()
            self.store.save(actions)
        self._fire(self.on_reject, target)
        return target

    def execute(self, action_id: str) -> Action:
        """
        Explicit execute step (Operator-style two-phase). Only valid for
        actions in 'approved' status. Use when auto_execute_on_approve=False.
        """
        with self._lock:
            actions = self.store.load()
            target = None
            for a in actions:
                if a.id == action_id:
                    target = a
                    break
            if target is None:
                raise ValueError(f"action {action_id!r} not found")
            if target.status != APPROVED:
                raise ValueError(
                    f"action {action_id!r} is {target.status}, not approved"
                )
        # Release the lock before running the executor — executors can be
        # slow (network, disk) and we don't want to block other queue ops.
        self._execute_action(target)
        return target

    def clear_resolved(self) -> int:
        """Remove all terminal-status actions. Returns count removed."""
        with self._lock:
            actions = self.store.load()
            kept = [a for a in actions if not a.is_terminal]
            removed = len(actions) - len(kept)
            self.store.save(kept)
        return removed

    # ── Internal ─────────────────────────────────────────────────────────────

    def _execute_action(self, action: Action) -> None:
        """Run the registered executor and persist the result."""
        self._execute_in_place(action)
        with self._lock:
            actions = self.store.load()
            for i, a in enumerate(actions):
                if a.id == action.id:
                    actions[i] = action
                    break
            self.store.save(actions)
        self._fire(self.on_execute, action)

    def _execute_in_place(self, action: Action) -> None:
        """Mutate `action` based on executor result. Does not persist."""
        executor = self.executors.get(action.type)
        if executor is None:
            action.status = FAILED
            action.error = f"no executor registered for action type {action.type!r}"
            action.resolved_at = _now_iso()
            return
        try:
            result = executor(action)
            action.status = EXECUTED
            action.result = str(result) if result is not None else ""
            action.resolved_at = _now_iso()
        except Exception as exc:
            action.status = FAILED
            action.error = repr(exc)
            action.resolved_at = _now_iso()
            logger.exception(
                f"executor for {action.type!r} raised on action {action.id}"
            )

    def _fire(self, hook: Optional[Hook], action: Action) -> None:
        if hook is None:
            return
        try:
            hook(action)
        except Exception as exc:
            logger.error(
                f"approval-queue hook raised on action {action.id}: {exc!r}"
            )


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _new_id() -> str:
    return uuid.uuid4().hex[:8]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _find_pending_or_raise(actions: list[Action], action_id: str) -> Action:
    for a in actions:
        if a.id == action_id:
            if a.status != PENDING:
                raise ValueError(
                    f"action {action_id!r} is {a.status}, not pending"
                )
            return a
    raise ValueError(f"action {action_id!r} not found")
