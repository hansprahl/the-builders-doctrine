"""
The Builders' Kit — Named Specialists registry.

Portable implementation of the multi-specialist registry pattern from TOP's
agents/orchestrator.py. Each specialist has a persistent identity: a name,
a one-line scope description, an entrypoint function, and optional role
restrictions. The registry maps name → specialist module and produces the
`ask_{name}` callables an orchestrator binds as tools.

The naming convention is product-specific. TOP uses first names (Vera, Rex,
Scout, Atlas, Recon, Maven, Forge). Operator uses military call signs.
Custer might use staff role names. The chassis stays agnostic.

Doctrine invariants this module preserves (non-negotiable):

  1. Persistent identity. Each specialist has a stable name. The orchestrator
     routes by name, not by domain string.
  2. Scope-non-overlap. Two specialists cannot register under the same name.
     Two specialists CAN claim overlapping scopes — but the registry surfaces
     this so the prompt author can disambiguate.
  3. Specialist names are internal. The chassis provides a soft-validation
     helper (validate_no_leak) but does not silently scrub — caller decides.
  4. Tool allowlist by role. The same registry can produce a different tool
     set per role (admin sees all specialists; user sees a subset). This
     lets multi-tenant products gate sensitive specialists per tenant.
  5. The orchestrator never calls a specialist's run() directly — only
     through the registry's ask_* wrappers. The wrapper is where
     confidence capture and other cross-cutting concerns live.

Usage:

    from kit.chassis import SpecialistRegistry, Specialist

    def vera_run(query: str) -> str:
        from agents.specialists.schedule import run
        return run(query)

    registry = SpecialistRegistry(
        confidence_capture=parse_and_persist_confidence_block,
    )

    registry.register(Specialist(
        name="vera",
        description="schedule, calendar, tasks, planning, projects, reminders",
        run=vera_run,
        roles={"user", "admin"},
    ))
    registry.register(Specialist(
        name="forge",
        description="dev specialist — code reads/writes/runs",
        run=forge_run,
        roles={"admin"},   # not exposed to regular users
    ))

    # Build the tool set for a given role:
    user_tools = registry.make_tools(role="user")
    admin_tools = registry.make_tools(role="admin")

    # Or call directly:
    response = registry.call("vera", "what's on my plate today?")
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional

logger = logging.getLogger(__name__)

SpecialistRunFn = Callable[[str], str]
ConfidenceCapture = Callable[[str, str, str], str]   # (name, query, raw) -> cleaned


# ──────────────────────────────────────────────────────────────────────────────
# Specialist
# ──────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Specialist:
    """One named specialist. Frozen so the registry can rely on identity."""
    name: str
    description: str
    run: SpecialistRunFn
    roles: frozenset[str] = field(default_factory=lambda: frozenset({"user", "admin"}))

    def __post_init__(self):
        # Validate at construction so registry-time errors don't show up
        # later as cryptic AttributeErrors.
        if not self.name or not self.name.strip():
            raise ValueError("Specialist name must be a non-empty string")
        if not re.match(r"^[a-z][a-z0-9_]*$", self.name):
            raise ValueError(
                f"Specialist name {self.name!r} must be lowercase, start with "
                f"a letter, and contain only letters, digits, and underscores"
            )
        if not self.description or not self.description.strip():
            raise ValueError(
                f"Specialist {self.name!r} requires a non-empty description"
            )
        if not callable(self.run):
            raise ValueError(
                f"Specialist {self.name!r} requires a callable run function"
            )
        if not self.roles:
            raise ValueError(
                f"Specialist {self.name!r} requires at least one role"
            )
        # Normalize roles to a frozenset.
        object.__setattr__(self, "roles", frozenset(self.roles))


# ──────────────────────────────────────────────────────────────────────────────
# Registry
# ──────────────────────────────────────────────────────────────────────────────

class SpecialistRegistry:
    """
    The portable named-specialists registry. Configure once per product;
    register specialists at startup; produce role-scoped tool sets for
    the orchestrator.
    """

    def __init__(
        self,
        *,
        confidence_capture: Optional[ConfidenceCapture] = None,
    ) -> None:
        """
        Args:
            confidence_capture: Optional wrapper called as
                `confidence_capture(name, query, raw_response)` and expected
                to return the cleaned response (with the CONFIDENCE block
                stripped after persisting it). Wired at the registry level
                so every specialist call goes through the same hook.
        """
        self._specialists: dict[str, Specialist] = {}
        self._confidence_capture = confidence_capture

    # ── Registration ─────────────────────────────────────────────────────────

    def register(self, specialist: Specialist) -> None:
        """Add a specialist. Raises ValueError on name collision."""
        if specialist.name in self._specialists:
            raise ValueError(
                f"specialist {specialist.name!r} already registered; "
                f"each name must be unique"
            )
        self._specialists[specialist.name] = specialist

    def unregister(self, name: str) -> None:
        """Remove a specialist. Useful for tests and hot-reload scenarios."""
        self._specialists.pop(name, None)

    # ── Read ─────────────────────────────────────────────────────────────────

    def get(self, name: str) -> Specialist:
        """Return the named specialist. Raises KeyError if not registered."""
        if name not in self._specialists:
            raise KeyError(
                f"no specialist named {name!r}; "
                f"registered: {sorted(self._specialists.keys())}"
            )
        return self._specialists[name]

    def has(self, name: str) -> bool:
        return name in self._specialists

    def names(self) -> list[str]:
        """All registered specialist names, sorted."""
        return sorted(self._specialists.keys())

    def list_for_role(self, role: str) -> list[Specialist]:
        """Specialists visible to the given role, sorted by name."""
        return sorted(
            (s for s in self._specialists.values() if role in s.roles),
            key=lambda s: s.name,
        )

    def all(self) -> list[Specialist]:
        """All specialists regardless of role, sorted by name."""
        return sorted(self._specialists.values(), key=lambda s: s.name)

    # ── Invocation ───────────────────────────────────────────────────────────

    def call(self, name: str, query: str) -> str:
        """
        Invoke a specialist by name. Applies confidence_capture if configured.
        The orchestrator should use this rather than calling run() directly.
        """
        specialist = self.get(name)
        raw = specialist.run(query)
        if self._confidence_capture is not None:
            try:
                return self._confidence_capture(specialist.name, query, raw)
            except Exception as exc:
                logger.warning(
                    f"confidence_capture failed for {specialist.name!r}: "
                    f"{exc!r} — returning raw response"
                )
                return raw
        return raw

    # ── Tool set construction ────────────────────────────────────────────────

    def make_tools(self, *, role: str = "user") -> list[Callable[[str], str]]:
        """
        Produce a list of `ask_{name}(query) -> str` callables for the given
        role. These are the bindings the orchestrator registers as tools.

        The returned callables carry a __doc__ matching the specialist's
        description so an LLM-tool framework can extract it for the tool
        manifest.
        """
        tools: list[Callable[[str], str]] = []
        for spec in self.list_for_role(role):
            tools.append(self._make_ask_callable(spec))
        return tools

    def _make_ask_callable(self, spec: Specialist) -> Callable[[str], str]:
        """Build a single `ask_{name}(query)` callable for one specialist."""
        def ask(query: str) -> str:
            return self.call(spec.name, query)
        ask.__name__ = f"ask_{spec.name}"
        ask.__qualname__ = f"ask_{spec.name}"
        ask.__doc__ = (
            f"Ask {spec.name.title()}, the {spec.description}.\n\n"
            f"Args:\n"
            f"    query: What you want {spec.name.title()} to do or look up."
        )
        return ask

    # ── Soft validation ──────────────────────────────────────────────────────

    def validate_no_leak(
        self,
        text: str,
        *,
        ignore: Iterable[str] = (),
    ) -> list[str]:
        """
        Scan `text` for occurrences of specialist names. Returns a list of
        names that appear as standalone words in the text.

        Use as a soft check after the orchestrator emits user-facing text.
        The chassis does NOT silently scrub — caller decides whether to log,
        warn, or block. (TOP's rule is to enforce no-leak via prompt
        instruction; this validator is the secondary belt-and-suspenders
        check.)

        Args:
            text: The text to scan.
            ignore: Names to skip — e.g. specialist names that are also
                common English words ("Forge"), or names the product
                deliberately surfaces.
        """
        ignore_set = {n.lower() for n in ignore}
        leaked: list[str] = []
        lowered_text = text.lower()
        for name in self._specialists:
            if name in ignore_set:
                continue
            # Word-boundary match against the lowercased text.
            if re.search(rf"\b{re.escape(name)}\b", lowered_text):
                leaked.append(name)
        return sorted(leaked)

    # ── Scope analysis ───────────────────────────────────────────────────────

    def find_overlapping_scopes(self) -> list[tuple[str, str, str]]:
        """
        Return triples of (name_a, name_b, shared_keyword) for specialists
        whose descriptions share substantive keywords. A diagnostic for
        prompt authors — overlapping scopes mean the orchestrator may
        route ambiguously.

        Heuristic: if two specialists' descriptions share a meaningful
        word (≥4 characters, not in a stopword list), surface the pair.
        """
        STOPWORDS = {
            "with", "from", "this", "that", "your", "into", "over", "about",
            "what", "when", "where", "which", "specialist", "and", "or", "the",
            "for", "user", "users", "data", "tools",
        }
        # Build per-specialist keyword sets.
        kw_by_spec: dict[str, set[str]] = {}
        for s in self._specialists.values():
            words = re.findall(r"[a-z]{4,}", s.description.lower())
            kw_by_spec[s.name] = {w for w in words if w not in STOPWORDS}

        names = sorted(kw_by_spec.keys())
        overlaps: list[tuple[str, str, str]] = []
        for i, a in enumerate(names):
            for b in names[i+1:]:
                shared = kw_by_spec[a] & kw_by_spec[b]
                for kw in sorted(shared):
                    overlaps.append((a, b, kw))
        return overlaps
