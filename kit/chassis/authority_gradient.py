"""
The Builders' Kit — Authority Gradient.

Portable implementation of the Mission Command Architecture authority gradient
(MCA `## The Authority Gradient`). Classifies every tool dispatch into an
action class, checks whether the acting tier is authorized for that class,
logs violations without blocking, and produces five outcome metrics.

Validated empirically in funkytown Experiment 02 (N=3, 2026-05-13) — mean
in-unit resolution 61.1%, 0 tier violations, 0 hard-floor breaches.

Doctrine invariants this module preserves (non-negotiable):

  1. No LLM dependency. This is a deterministic classifier + logger.
     Action classes are derived from a caller-supplied tool→class mapping
     and an overridable tier→authorized-classes table.

  2. WORLD_BOUNDARY is never tier-authorized. Regardless of tier, any
     action that crosses the unit boundary (send_email, post_publicly,
     dispatch_campaign, commit_spend, etc.) routes through the approval
     queue. This preserves Principle #4's hard floor.

  3. Violations are logged, not blocked. The gradient is observational —
     the doctrine evidence comes from seeing where natural drift happens,
     not from artificially preventing it. Products that want hard
     enforcement compose the gradient with their own dispatch gate.

  4. Approval-queue integration is by callback, not hard import. Callers
     pass an `on_world_boundary` hook; the chassis stays composable.

  5. Per-tier authorization is overridable. Default table maps to standard
     officer / NCO / soldier authority gradient; products with different
     role taxonomies can pass their own.

Usage:

    from kit.chassis import (
        AuthorityGradient, GradientLog, Tier, Channel, ActionClass,
        ApprovalQueue,
    )

    # Per-product tool → action class mapping
    TOOL_CLASSES = {
        "send_email": ActionClass.WORLD_BOUNDARY,
        "send_sms":   ActionClass.WORLD_BOUNDARY,
        "draft_post": ActionClass.REVERSIBLE_IN_UNIT,
        "delegate_to_specialist": ActionClass.REVERSIBLE_IN_MISSION,
        "declare_done": ActionClass.TERMINAL,
    }

    # Wire world-boundary actions into the approval queue
    def queue_for_approval(event):
        approval_queue.queue(
            action_type=event.tool_name,
            summary=f"{event.actor_callsign} requested {event.tool_name}",
            payload=event.notes,
        )

    log = GradientLog(
        run_dir=Path("runs/2026-05-13"),
        tool_classes=TOOL_CLASSES,
        on_world_boundary=queue_for_approval,
    )

    # In the dispatcher:
    log.log_event(
        actor_tier=Tier.NCO,
        actor_callsign="1/2",
        tool_name="draft_post",
    )

    # At end of run:
    metrics = log.all_metrics()
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Enums — MCA vocabulary
# ──────────────────────────────────────────────────────────────────────────────


class Tier(str, Enum):
    """Authority tier per MCA `## The Authority Gradient`."""
    OFFICER = "officer"   # PL / CO / Battalion CDR — sets intent, calls done
    NCO = "nco"           # SL / PSG / 1SG — owns execution within scope
    SOLDIER = "soldier"   # individual contributor under NCO supervision


class Channel(str, Enum):
    """Command vs staff channel per MCA `## Staff Channel`."""
    COMMAND = "command"   # line agents — receive intent, return SITREP
    STAFF = "staff"       # advisory agents — S-2/S-4/WO-shape; never-override-always-log


class ActionClass(str, Enum):
    """Action classes the gradient recognizes per MCA's gradient table."""
    WORLD_BOUNDARY = "world_boundary"
    REVERSIBLE_IN_MISSION = "reversible_in_mission"
    REVERSIBLE_IN_UNIT = "reversible_in_unit"
    PLANNING = "planning"     # in-unit reflection / synthesis (officer-tier)
    TERMINAL = "terminal"     # declare_done


# ──────────────────────────────────────────────────────────────────────────────
# Default authorization table
# ──────────────────────────────────────────────────────────────────────────────


# Default tier → authorized action classes. Products override by passing
# `tier_authorized_classes` to GradientLog / AuthorityGradient.
#
# Note WORLD_BOUNDARY is intentionally absent from every tier — that class
# always escalates regardless of tier. See is_violation() and the
# on_world_boundary hook.
DEFAULT_TIER_AUTHORIZED_CLASSES: dict[Tier, frozenset[ActionClass]] = {
    Tier.SOLDIER: frozenset({ActionClass.REVERSIBLE_IN_UNIT}),
    Tier.NCO: frozenset({ActionClass.REVERSIBLE_IN_UNIT}),
    Tier.OFFICER: frozenset({
        ActionClass.REVERSIBLE_IN_UNIT,
        ActionClass.REVERSIBLE_IN_MISSION,
        ActionClass.PLANNING,
        ActionClass.TERMINAL,
    }),
}


# ──────────────────────────────────────────────────────────────────────────────
# Classification
# ──────────────────────────────────────────────────────────────────────────────


def classify_action(
    tool_name: str,
    tool_classes: dict[str, ActionClass],
    default: ActionClass = ActionClass.REVERSIBLE_IN_UNIT,
) -> ActionClass:
    """Map a tool name to its action class. Unknown tools fall back to `default`.

    The safest default is REVERSIBLE_IN_UNIT — artifact-shaped work that any
    tier can perform. Products that prefer fail-closed should pass a stricter
    default (e.g. PLANNING) so unknown tools require officer authorization.
    """
    return tool_classes.get(tool_name, default)


def is_violation(
    tier: Tier,
    action_class: ActionClass,
    tier_authorized_classes: dict[Tier, frozenset[ActionClass]] = DEFAULT_TIER_AUTHORIZED_CLASSES,
) -> bool:
    """True if a tier is acting outside its authorized action classes.

    WORLD_BOUNDARY is never a tier-violation per se — it's a routing event
    that always requires founder approval. The gradient flags it as a
    `is_world_boundary` event separately so the approval-queue integration
    fires regardless of which tier attempted it.
    """
    if action_class == ActionClass.WORLD_BOUNDARY:
        return False
    return action_class not in tier_authorized_classes.get(tier, frozenset())


# ──────────────────────────────────────────────────────────────────────────────
# Event + log
# ──────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class GradientEvent:
    """A single gradient routing event for the run."""
    timestamp: float
    actor_tier: Tier
    actor_callsign: str
    tool_name: str
    action_class: ActionClass
    is_violation: bool
    is_world_boundary: bool
    channel: Channel = Channel.COMMAND
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "actor_tier": self.actor_tier.value,
            "actor_callsign": self.actor_callsign,
            "tool_name": self.tool_name,
            "action_class": self.action_class.value,
            "is_violation": self.is_violation,
            "is_world_boundary": self.is_world_boundary,
            "channel": self.channel.value,
            "notes": self.notes,
        }

    def to_jsonl(self) -> str:
        return json.dumps(self.to_dict())


# Type aliases for callback hooks
OnWorldBoundary = Callable[[GradientEvent], None]
OnViolation = Callable[[GradientEvent], None]


@dataclass
class GradientLog:
    """Live event log + outcome metric collector for one run.

    The log is observational: every tool dispatch produces an event regardless
    of whether it violated the gradient or crossed a world boundary. Callers
    plug in hooks to act on those events (e.g. enqueue world-boundary actions
    for approval, alert on tier violations).

    Configuration:
      run_dir              — where gradient_log.jsonl and gradient_metrics.json
                             land. If None, log is in-memory only.
      tool_classes         — mapping from tool_name to ActionClass. REQUIRED.
      tier_authorized_classes — override the default per-tier auth table.
      on_world_boundary    — callback for every world-boundary attempt; the
                             integration point for ApprovalQueue.
      on_violation         — callback for every tier-scope violation.
      default_action_class — fallback class for unknown tool names.
    """

    tool_classes: dict[str, ActionClass]
    run_dir: Optional[Path] = None
    tier_authorized_classes: dict[Tier, frozenset[ActionClass]] = field(
        default_factory=lambda: dict(DEFAULT_TIER_AUTHORIZED_CLASSES)
    )
    on_world_boundary: Optional[OnWorldBoundary] = None
    on_violation: Optional[OnViolation] = None
    default_action_class: ActionClass = ActionClass.REVERSIBLE_IN_UNIT

    events: list[GradientEvent] = field(default_factory=list)
    pl_turn_starts: list[float] = field(default_factory=list)
    pl_turn_ends: list[float] = field(default_factory=list)
    confident_zero_gaps_iterations: int = 0
    reflection_gate_proceeds: int = 0
    reflection_gate_iterates: int = 0
    reflection_gate_refuses: int = 0
    declare_done_calls: int = 0

    def log_event(
        self,
        actor_tier: Tier,
        actor_callsign: str,
        tool_name: str,
        channel: Channel = Channel.COMMAND,
        notes: str = "",
    ) -> GradientEvent:
        action_class = classify_action(
            tool_name, self.tool_classes, self.default_action_class,
        )
        violation = is_violation(
            actor_tier, action_class, self.tier_authorized_classes,
        )
        event = GradientEvent(
            timestamp=time.time(),
            actor_tier=actor_tier,
            actor_callsign=actor_callsign,
            tool_name=tool_name,
            action_class=action_class,
            is_violation=violation,
            is_world_boundary=(action_class == ActionClass.WORLD_BOUNDARY),
            channel=channel,
            notes=notes,
        )
        self.events.append(event)

        if self.run_dir is not None:
            path = self.run_dir / "gradient_log.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "a") as f:
                f.write(event.to_jsonl() + "\n")

        if event.is_world_boundary and self.on_world_boundary is not None:
            try:
                self.on_world_boundary(event)
            except Exception:
                logger.exception(
                    "on_world_boundary callback failed for %s by %s",
                    tool_name, actor_callsign,
                )

        if event.is_violation and self.on_violation is not None:
            try:
                self.on_violation(event)
            except Exception:
                logger.exception(
                    "on_violation callback failed for %s by %s",
                    tool_name, actor_callsign,
                )

        return event

    def log_pl_turn_start(self) -> None:
        self.pl_turn_starts.append(time.time())

    def log_pl_turn_end(self) -> None:
        self.pl_turn_ends.append(time.time())

    def log_reflection_result(
        self,
        recommendation: str,
        was_confident_zero_gaps: bool = False,
    ) -> None:
        if recommendation == "proceed":
            self.reflection_gate_proceeds += 1
        elif recommendation == "iterate":
            self.reflection_gate_iterates += 1
            if was_confident_zero_gaps:
                self.confident_zero_gaps_iterations += 1
        elif recommendation == "refuse":
            self.reflection_gate_refuses += 1

    # ── Metric computation ──────────────────────────────────────────────────

    def metric_escalation_ratio(self) -> dict[str, Any]:
        """In-unit NCO resolutions vs. escalations (any PL/world-boundary action).

        Hypothesis under Experiment 02: ≥30% in-unit resolution makes the
        gradient observable. Below ~5% suggests the gradient is cosmetic.
        """
        in_unit = sum(
            1 for e in self.events
            if e.actor_tier == Tier.NCO
            and e.action_class == ActionClass.REVERSIBLE_IN_UNIT
        )
        escalations = sum(
            1 for e in self.events
            if e.action_class in (
                ActionClass.REVERSIBLE_IN_MISSION,
                ActionClass.PLANNING,
                ActionClass.TERMINAL,
                ActionClass.WORLD_BOUNDARY,
            )
        )
        total = in_unit + escalations
        return {
            "in_unit_resolutions": in_unit,
            "escalations": escalations,
            "total": total,
            "in_unit_pct": (in_unit / total) if total else 0.0,
        }

    def metric_pl_cycle_time(self) -> dict[str, Any]:
        """Wall-clock per PL turn (OPORD-down → SITREP-up)."""
        if (
            not self.pl_turn_starts
            or len(self.pl_turn_starts) != len(self.pl_turn_ends)
        ):
            return {"turns": 0, "mean_sec": None, "median_sec": None, "raw": []}
        deltas = [e - s for s, e in zip(self.pl_turn_starts, self.pl_turn_ends)]
        deltas_sorted = sorted(deltas)
        median = deltas_sorted[len(deltas_sorted) // 2] if deltas_sorted else None
        return {
            "turns": len(deltas),
            "mean_sec": sum(deltas) / len(deltas),
            "median_sec": median,
            "raw": deltas,
        }

    def metric_violation_count(self) -> dict[str, Any]:
        """Tier-scope violations, broken down by tier."""
        by_tier: dict[str, int] = {}
        for e in self.events:
            if e.is_violation:
                by_tier[e.actor_tier.value] = by_tier.get(e.actor_tier.value, 0) + 1
        return {
            "total": sum(by_tier.values()),
            "by_tier": by_tier,
            "events": [
                {
                    "callsign": e.actor_callsign,
                    "tool": e.tool_name,
                    "class": e.action_class.value,
                }
                for e in self.events if e.is_violation
            ],
        }

    def metric_hard_floor_breach_count(self) -> dict[str, Any]:
        """Principle #4 hard floor: world-boundary without approval evidence.

        A breach = world-boundary event whose notes do not mention 'approval'.
        Callers that wire `on_world_boundary` to an ApprovalQueue should record
        the queued action_id in `notes` so this metric reflects the routing.
        """
        world_events = [e for e in self.events if e.is_world_boundary]
        breaches = [e for e in world_events if "approval" not in e.notes.lower()]
        return {
            "world_boundary_attempts": len(world_events),
            "breaches": len(breaches),
            "events": [
                {
                    "callsign": e.actor_callsign,
                    "tool": e.tool_name,
                    "notes": e.notes,
                }
                for e in breaches
            ],
        }

    def metric_confident_zero_gaps_rate(self) -> dict[str, Any]:
        """Reflection Gate v1.2 catches confident-zero-gaps as a Principle #12
        failure mode. Validated empirically in funkytown 02; brief-class
        dependent (closed-ended briefs produce the failure mode more reliably).
        """
        total = (
            self.reflection_gate_proceeds
            + self.reflection_gate_iterates
            + self.reflection_gate_refuses
        )
        return {
            "total_gate_evaluations": total,
            "proceeds": self.reflection_gate_proceeds,
            "iterates": self.reflection_gate_iterates,
            "refuses": self.reflection_gate_refuses,
            "confident_zero_gaps_caught": self.confident_zero_gaps_iterations,
            "confident_zero_gaps_rate": (
                self.confident_zero_gaps_iterations / total if total else 0.0
            ),
            "declare_done_calls": self.declare_done_calls,
        }

    def all_metrics(self) -> dict[str, Any]:
        """Compute all five outcome metrics. Writes to gradient_metrics.json
        if run_dir is set."""
        metrics = {
            "escalation_ratio": self.metric_escalation_ratio(),
            "pl_cycle_time": self.metric_pl_cycle_time(),
            "violation_count": self.metric_violation_count(),
            "hard_floor_breach_count": self.metric_hard_floor_breach_count(),
            "confident_zero_gaps_rate": self.metric_confident_zero_gaps_rate(),
        }
        if self.run_dir is not None:
            path = self.run_dir / "gradient_metrics.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump(metrics, f, indent=2)
        return metrics


# ──────────────────────────────────────────────────────────────────────────────
# Tier inference helper
# ──────────────────────────────────────────────────────────────────────────────


def infer_tier_from_callsign(callsign: str) -> Tier:
    """Infer Tier from MCA callsign convention.

    Conventions (one-slash = squad, two-slash = soldier within squad):
      ''            → OFFICER  (Platoon Leader, no segments)
      'PL'          → OFFICER
      '1/1', '1/2'  → NCO      (Squad Leaders)
      '1/1/A'       → SOLDIER  (individual under SL)

    Products with different callsign schemes should pass their own inference
    function — this helper exists for funkytown-style Platoon Lean conventions.
    """
    if not callsign or callsign == "PL":
        return Tier.OFFICER
    segments = callsign.count("/") + 1
    if segments >= 3:
        return Tier.SOLDIER
    return Tier.NCO


# ──────────────────────────────────────────────────────────────────────────────
# Facade — single object that bundles classifier + log
# ──────────────────────────────────────────────────────────────────────────────


@dataclass
class AuthorityGradient:
    """Facade bundling the tool→class table, the per-tier auth table, and
    a GradientLog. Convenience wrapper; products can also use GradientLog
    directly.

    Two ways to use:

      # 1. As a facade with a single log
      gradient = AuthorityGradient(
          tool_classes=TOOL_CLASSES,
          run_dir=Path("runs/2026-05-13"),
      )
      gradient.log.log_event(Tier.NCO, "1/2", "draft_post")

      # 2. As a stateless classifier (no log)
      cls = AuthorityGradient(tool_classes=TOOL_CLASSES)
      cls.classify("send_email")           # → ActionClass.WORLD_BOUNDARY
      cls.violates(Tier.NCO, "declare_done")  # → True
    """

    tool_classes: dict[str, ActionClass]
    run_dir: Optional[Path] = None
    tier_authorized_classes: dict[Tier, frozenset[ActionClass]] = field(
        default_factory=lambda: dict(DEFAULT_TIER_AUTHORIZED_CLASSES)
    )
    on_world_boundary: Optional[OnWorldBoundary] = None
    on_violation: Optional[OnViolation] = None
    default_action_class: ActionClass = ActionClass.REVERSIBLE_IN_UNIT

    log: GradientLog = field(init=False)

    def __post_init__(self) -> None:
        self.log = GradientLog(
            tool_classes=self.tool_classes,
            run_dir=self.run_dir,
            tier_authorized_classes=self.tier_authorized_classes,
            on_world_boundary=self.on_world_boundary,
            on_violation=self.on_violation,
            default_action_class=self.default_action_class,
        )

    def classify(self, tool_name: str) -> ActionClass:
        return classify_action(
            tool_name, self.tool_classes, self.default_action_class,
        )

    def violates(self, tier: Tier, tool_name: str) -> bool:
        return is_violation(
            tier, self.classify(tool_name), self.tier_authorized_classes,
        )
