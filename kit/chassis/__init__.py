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

from .crisis_floor import CrisisFloor, CrisisEvent
from .approval_queue import (
    Action,
    ApprovalQueue,
    InMemoryStore,
    JsonFileStore,
    PENDING, APPROVED, REJECTED, EXECUTED, FAILED,
)
from .user_context import UserContext
from .specialists import Specialist, SpecialistRegistry
from .aar import (
    AAR, AARLog, CalibrationReport,
    SUCCESS, FAILURE, PARTIAL, ABANDONED, VALID_OUTCOMES,
    HABIT, TASK, GOAL, ROUTINE, RECOMMENDATION,
)
from .prompt_guardian import (
    Commandment, CommandmentScore, GuardianReport, GuardianError,
    PromptGuardian,
    build_scoring_system_prompt, build_correction_system_prompt,
)
from .reflection_gate import (
    ReflectionGate, ReflectionResult, ReflectorResponse,
    parse_reflector_response,
)
from .authority_gradient import (
    AuthorityGradient, GradientLog, GradientEvent,
    Tier, Channel, ActionClass,
    DEFAULT_TIER_AUTHORIZED_CLASSES,
    classify_action, is_violation, infer_tier_from_callsign,
)

__all__ = [
    "CrisisFloor", "CrisisEvent",
    "Action", "ApprovalQueue", "InMemoryStore", "JsonFileStore",
    "PENDING", "APPROVED", "REJECTED", "EXECUTED", "FAILED",
    "UserContext",
    "Specialist", "SpecialistRegistry",
    "AAR", "AARLog", "CalibrationReport",
    "SUCCESS", "FAILURE", "PARTIAL", "ABANDONED", "VALID_OUTCOMES",
    "HABIT", "TASK", "GOAL", "ROUTINE", "RECOMMENDATION",
    "Commandment", "CommandmentScore", "GuardianReport", "GuardianError",
    "PromptGuardian",
    "build_scoring_system_prompt", "build_correction_system_prompt",
    "ReflectionGate", "ReflectionResult", "ReflectorResponse",
    "parse_reflector_response",
]
