"""
The Builders' Kit — Per-User Context.

Portable implementation of the per-user isolation primitive specified in
TOP's tools/user_context.py. The pattern: a ContextVar with no default,
so any code path that reaches `get()` without first calling `set()`
raises LookupError. The crash is the doctrine working correctly.

From TOP's source comment, preserved here verbatim because it is the
load-bearing rationale:

    Phase (a) of the hardening plan: the ContextVar has no default and
    no fallback. Any code path that reaches get_user_id() without first
    calling set_user_id() will raise LookupError loudly. Phase (b) ran
    long enough to confirm every production call site sets the user
    explicitly (telegram_bot per-message, runner per-job, oauth_server
    per-request, server.py at module load). With real financial data
    now flowing through Plaid, silent fallbacks are unacceptable — we
    want the crash and the stack, not a silent write to the wrong user.

This chassis module is a class wrapper around that pattern, so each
product (and each test) gets its own isolated ContextVar instance.

Doctrine invariants this module preserves (non-negotiable):

  1. No default value. `get()` raises LookupError when the user is
     unset. Callers MUST set the user at the entry point.
  2. No silent fallback to a "default user" or environment variable.
     The crash is preferred over a wrong write.
  3. Async- and thread-safe via Python's ContextVar (each task / thread
     sees its own value; setting from a parent task propagates to
     children but not to siblings).
  4. Per-user data path derivation is part of the same primitive — the
     same module that owns the user_id ContextVar owns the function
     that constructs paths from it. This prevents drift between code
     that reads user_id and code that builds per-user file paths.

Usage:

    from kit.chassis import UserContext

    ctx = UserContext(base_dir=Path("/path/to/data"))

    # At every entry point (request handler, scheduled job, CLI command):
    ctx.set("hans")
    do_work_that_reads_or_writes_user_data()

    # In a tool:
    uid = ctx.get()  # raises LookupError if unset — that's correct
    journal_path = ctx.data_path("journal.json")  # → data/users/hans/journal.json

    # For tests or scoped operations:
    with ctx.scope("test_user_42"):
        run_some_user_specific_thing()
    # ctx is automatically reset to its prior state
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from typing import Iterator, Optional


class UserContext:
    """
    Per-instance per-user context. One instance per product, typically
    created at module load and passed (or imported) wherever needed.

    Using a class instead of module-level globals gives every test its
    own isolated ContextVar — which is what you want when tests run in
    parallel or back-to-back without bleeding state.
    """

    def __init__(
        self,
        base_dir: Path,
        *,
        users_subdir: str = "users",
    ) -> None:
        """
        Args:
            base_dir: Root directory for per-user data. data_path() resolves
                paths under base_dir/users_subdir/{user_id}/...
            users_subdir: Subdirectory name under base_dir. Default 'users'.
        """
        self.base_dir = Path(base_dir)
        self.users_subdir = users_subdir
        # ContextVar instance is unique per UserContext instance, so
        # multiple UserContexts in the same process do not share state.
        self._var: ContextVar[str] = ContextVar(
            f"user_id_{id(self)}"  # name is for debugging only
        )

    # ── Core get/set ─────────────────────────────────────────────────────────

    def get(self) -> str:
        """
        Return the current user_id.

        Raises:
            LookupError: if set() has not been called in the current
                context. Callers should NOT catch this — it indicates a
                missing entry-point initialization that must be fixed at
                the entry point, not papered over here.
        """
        return self._var.get()

    def set(self, user_id: str) -> None:
        """
        Set the user_id for the current context.

        Args:
            user_id: A non-empty string identifying the user. Empty
                strings are rejected to prevent silent "user is empty"
                bugs that look like LookupErrors but aren't.
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError(
                f"user_id must be a non-empty string; got {user_id!r}"
            )
        self._var.set(user_id)

    def get_or_none(self) -> Optional[str]:
        """
        Safe variant of get() that returns None instead of raising.

        Use sparingly — most code paths in a per-user system want the
        crash. Reserve this for tools that genuinely run before the
        user is established (login flows, public health checks).
        """
        try:
            return self._var.get()
        except LookupError:
            return None

    def is_set(self) -> bool:
        """True if a user_id is set in the current context."""
        return self.get_or_none() is not None

    # ── Scope ────────────────────────────────────────────────────────────────

    @contextmanager
    def scope(self, user_id: str) -> Iterator[None]:
        """
        Temporarily bind user_id within a `with` block. Restores the
        prior state on exit, including the unset state.

        Use for: per-request handlers, scheduled job workers, tests that
        exercise multiple users in sequence.
        """
        token = None
        try:
            token = self._var.set(user_id)
            yield
        finally:
            if token is not None:
                self._var.reset(token)

    # ── Per-user data path ───────────────────────────────────────────────────

    def data_path(self, *parts: str) -> Path:
        """
        Build a per-user file path under base_dir/users_subdir/{user_id}/...

        Creates the directory if it does not exist. Raises LookupError
        via get() if the user is unset — by design.

        Example:
            ctx.set("hans")
            p = ctx.data_path("journal", "2026-05.json")
            # → /path/to/data/users/hans/journal/2026-05.json
        """
        uid = self.get()
        path = self.base_dir / self.users_subdir / uid
        if parts:
            path = path.joinpath(*parts)
            # Create parent of the final file (or the directory itself
            # if the path was meant as a directory). We can't tell, so
            # mkdir the parent.
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)
        return path

    def user_dir(self) -> Path:
        """The per-user root directory. Created if missing."""
        return self.data_path()
