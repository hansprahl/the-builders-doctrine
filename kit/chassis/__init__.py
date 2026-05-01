"""
The Builders' Kit — chassis.

Portable, transport-agnostic implementations of the doctrine's load-bearing
runtime components. Each chassis module is parameterizable per product but
preserves the doctrine's invariants:

  - Crisis Floor: no LLM dependency, deterministic, fail-open
  - Approval Queue: irreversible actions gate on human approval
  - Named Specialists: registry + tool allowlist + scope-lock
  - AAR Loop: outcomes calibrate confidence over time
  - Per-User Memory: ContextVar with LookupError on unset
  - Prompt Guardian: weekly audit against per-product commandments

Phase 2 of the kit ships these one at a time. Crisis Floor is first.
"""

from kit.chassis.crisis_floor import CrisisFloor, CrisisEvent

__all__ = ["CrisisFloor", "CrisisEvent"]
