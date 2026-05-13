"""
The Builders' Kit — Reflection Gate.

Portable implementation of Principle #12 (*What else? Active extraction*).
Runs before `declare_done` at every tier of an MCA unit (or at any
specialist's done-call in a non-MCA product). Inspects the agent's draft
output for Known/Inferred/Gap (K/I/G) coverage and returns a structured
recommendation: proceed, iterate, or refuse.

Doctrine invariants this module preserves (non-negotiable):

  1. No LLM dependency in the chassis. The reflector is a caller-supplied
     callback (same shape as crisis_floor's admin_alert). The chassis owns
     the protocol — prompt template, response schema, decision logic.
     The caller owns the LLM call.

  2. Scope-aware refusal. The gate has three scope modes per
     THE_BUILDERS_DOCTRINE.md Principle #12:
       - operator_tool — agent introspects on its own work product;
         the gate runs as written.
       - wellness — recursive interrogation of the user is REFUSED.
         The gate flips to facilitate the user asking "what else?" of
         themselves. Surveillance shape is the failure mode.
       - founder — extraction from the founder as a person is REFUSED.
         STORY/MEMORY are curated by the founder, not queried by their
         own system.

  3. Confident-zero-gaps is a failure mode, not a success. A reflector
     response that names no gaps AND acknowledges no uncertainty is
     evidence of compliance-shape, not truthful coverage. The gate
     returns 'iterate' with a structural challenge in that case.

  4. "I don't know" is the calibrated stop signal. A reflector response
     that explicitly acknowledges uncertainty is honored as honest
     output. uncertainty_acknowledged=True with empty gaps is a valid
     'proceed' result; the agent has done its work and named its limit.

  5. Gaps become RFI candidates, not silent debt. The gate's output
     `gaps` list is the input to the unit's RFI registry (per MCA's
     RFI protocol). The gate itself does not issue RFIs — that's the
     caller's responsibility — but the data shape is RFI-compatible.

Usage:

    from kit.chassis import ReflectionGate, ReflectorResponse

    def my_reflector(prompt, draft):
        # Caller's LLM call. Returns ReflectorResponse.
        response_text = anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": prompt}],
            system=f"Inspect this draft for K/I/G coverage:\\n{draft}",
        )
        return ReflectorResponse.parse(response_text.content[0].text)

    gate = ReflectionGate(
        scope="operator_tool",
        reflector=my_reflector,
        doctrinal_questions=[
            "Have you verified vote count against the canonical source?",
            "Have you checked the candidate filing deadline?",
        ],
    )

    # Before declare_done:
    result = gate.evaluate(draft=current_draft, context={"echelon": "PL"})
    if result.recommendation == "iterate":
        # gaps become next-round work; route to RFI registry if MCA-shaped
        for gap in result.gaps:
            unit.rfi_registry.issue(gap, requestor=current_callsign)
        return  # do not declare_done
    elif result.recommendation == "refuse":
        # the gate refused on doctrine (e.g., wellness scope tried to extract)
        log_doctrine_event(result.refusal_reason)
        return
    # else: proceed with declare_done
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Literal, Optional

ScopeMode = Literal["operator_tool", "wellness", "founder"]
Recommendation = Literal["proceed", "iterate", "refuse"]

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Data shapes
# ──────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ReflectorResponse:
    """
    The structured response a reflector callable must return.

    The reflector inspects a draft and returns K/I/G coverage plus an
    explicit uncertainty acknowledgement. The chassis does not call the
    LLM; the caller does, and parses the LLM output into this shape.
    """
    known: tuple[str, ...]
    inferred: tuple[str, ...]
    gaps: tuple[str, ...]
    uncertainty_acknowledged: bool
    raw: str = ""               # full LLM response, retained for audit

    def has_any_signal(self) -> bool:
        """True if the reflector returned any K/I/G items at all."""
        return bool(self.known or self.inferred or self.gaps)


@dataclass(frozen=True)
class ReflectionResult:
    """The Reflection Gate's structured output. Caller acts on this."""
    recommendation: Recommendation
    gaps: tuple[str, ...]
    uncertainty_acknowledged: bool
    refusal_reason: str = ""
    iterate_reason: str = ""
    reflector_response: Optional[ReflectorResponse] = None
    scope: ScopeMode = "operator_tool"
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_audit_record(self) -> dict:
        """JSON-serializable record for the doctrine event log."""
        return {
            "recommendation": self.recommendation,
            "scope": self.scope,
            "gaps": list(self.gaps),
            "uncertainty_acknowledged": self.uncertainty_acknowledged,
            "refusal_reason": self.refusal_reason,
            "iterate_reason": self.iterate_reason,
            "timestamp": self.timestamp.isoformat(),
        }


# ──────────────────────────────────────────────────────────────────────────────
# The gate
# ──────────────────────────────────────────────────────────────────────────────


# Sentinel for context fields that mark a wellness call as user-facing
# extraction (the failure mode the gate must refuse).
_USER_FACING_KEYS = frozenset(
    {"target_user_id", "user_id", "subject_user_id"}
)


class ReflectionGate:
    """
    Parameterizable Reflection Gate for Principle #12.

    One instance per scope per product. A product with both an operator-
    tool surface (admin panel, build pipeline) and a wellness surface
    (user-facing chat) constructs two gates with different scope modes.

    The gate owns three things:
      1. The scope mode (operator_tool / wellness / founder).
      2. A reflector callback (caller-supplied; chassis stays
         LLM-independent).
      3. The decision logic per Principle #12's scope conditions.

    It does NOT own:
      - the LLM call (reflector is the caller's transport)
      - the RFI registry (the gate produces gap candidates; the unit's
        RFI registry consumes them)
      - the audit log (the gate returns audit records; the caller
        persists them)
    """

    def __init__(
        self,
        scope: ScopeMode,
        reflector: Optional[Callable[[str, str], ReflectorResponse]] = None,
        *,
        doctrinal_questions: tuple[str, ...] = (),
        require_uncertainty_on_zero_gaps: bool = True,
        log_handler: Optional[logging.Logger] = None,
    ) -> None:
        if scope not in ("operator_tool", "wellness", "founder"):
            raise ValueError(
                f"scope must be one of operator_tool/wellness/founder, "
                f"got {scope!r}"
            )

        self.scope = scope
        self.reflector = reflector
        self.doctrinal_questions = tuple(doctrinal_questions)
        self.require_uncertainty_on_zero_gaps = require_uncertainty_on_zero_gaps
        self.logger = log_handler or logger

    # ── Prompt construction ──────────────────────────────────────────────────

    def build_reflection_prompt(
        self,
        draft: str,
        context: Optional[dict] = None,
    ) -> str:
        """
        Returns the structured prompt the caller should feed to the
        reflector LLM. The prompt enforces K/I/G shape in the response
        and explicitly invites uncertainty rather than punishing it.

        Scope-aware: wellness mode produces a *user-facing reflective
        question* prompt rather than an introspection prompt; founder
        mode is not reachable here (evaluate() refuses before reaching
        prompt construction).
        """
        context = context or {}

        if self.scope == "wellness":
            return self._build_wellness_prompt(draft, context)
        if self.scope == "founder":
            # Defensive: should never be called in founder scope, but if
            # it is, return a refusal-shaped prompt rather than an
            # extraction-shaped one.
            return (
                "REFUSED: The Reflection Gate is in founder scope. "
                "The founder is not the subject of inquiry by their own "
                "system. Curated bio is the input, not the target."
            )

        # operator_tool — standard introspection
        questions_block = ""
        if self.doctrinal_questions:
            qs = "\n".join(f"  - {q}" for q in self.doctrinal_questions)
            questions_block = (
                "\nProduct-specific doctrinal questions to check against:\n"
                + qs + "\n"
            )

        echelon_block = ""
        echelon = context.get("echelon")
        if echelon:
            echelon_block = (
                f"\nThis reflection is for the {echelon} tier's done-call. "
                f"Apply that tier's authority scope.\n"
            )

        return (
            "REFLECTION GATE (Principle #12 — Active Extraction)\n"
            "\n"
            "Inspect the draft below for Known / Inferred / Gap coverage. "
            "Return your response in exactly this structure:\n"
            "\n"
            "KNOWN:\n"
            "  - <item with source>\n"
            "  - ...\n"
            "\n"
            "INFERRED:\n"
            "  - <inference with the reasoning that supports it>\n"
            "  - ...\n"
            "\n"
            "GAPS:\n"
            "  - <specific information still missing, with what decision "
            "it would change>\n"
            "  - ...\n"
            "\n"
            "UNCERTAINTY: <yes|no>\n"
            "  If yes, the draft acknowledges what it does not know. "
            "'I don't know' is the calibrated stop signal — it is valid "
            "output, not failure. Mark yes if the draft names its limit.\n"
            f"{questions_block}"
            f"{echelon_block}"
            "\n"
            "Confident-zero-gaps with no uncertainty acknowledgement is "
            "the failure mode this gate exists to surface. If the draft "
            "appears comprehensive but lists no gaps and acknowledges no "
            "uncertainty, name one structural gap that a comprehensive "
            "answer would still leave open.\n"
            "\n"
            "DRAFT:\n"
            "---\n"
            f"{draft}\n"
            "---\n"
        )

    def _build_wellness_prompt(self, draft: str, context: dict) -> str:
        """
        Wellness scope inverts: the gate produces a reflective question
        the system can offer to the user, not an introspection over the
        user. The user does the asking; the system facilitates.
        """
        return (
            "WELLNESS REFLECTION (Principle #12 — inverted scope)\n"
            "\n"
            "This product is wellness-shaped. The Reflection Gate is "
            "INVERTED: the system does not interrogate the user with "
            "recursive 'what else?' questions. Surveillance shape is "
            "refused per Principle #12.\n"
            "\n"
            "Instead, given the conversation context below, return a "
            "SINGLE open-ended question the system can OFFER to the user "
            "that helps them ask 'what else?' of themselves. The question "
            "must:\n"
            "  - be offered, not pressed\n"
            "  - be answerable in the user's own pace\n"
            "  - not be a series of follow-ups\n"
            "  - acknowledge that 'I don't know' is a valid answer\n"
            "\n"
            "Return your response as:\n"
            "QUESTION: <the single reflective question>\n"
            "GAPS: <empty in wellness scope>\n"
            "UNCERTAINTY: <yes if the system should signal it doesn't know>\n"
            "\n"
            "CONTEXT:\n"
            "---\n"
            f"{draft}\n"
            "---\n"
        )

    # ── Evaluation ───────────────────────────────────────────────────────────

    def evaluate(
        self,
        draft: str,
        context: Optional[dict] = None,
    ) -> ReflectionResult:
        """
        Run the gate. Returns ReflectionResult with a recommendation.

        For 'operator_tool' scope: builds prompt, calls reflector, applies
        decision logic per Principle #12 + the confident-zero-gaps floor.

        For 'wellness' scope: refuses if the context indicates the call
        is interrogating the user; supports inverted use where the gate
        facilitates user self-reflection.

        For 'founder' scope: refuses always — the founder is not the
        subject of inquiry.
        """
        context = context or {}

        # ── Founder scope: hard refusal ──────────────────────────────────
        if self.scope == "founder":
            result = ReflectionResult(
                recommendation="refuse",
                gaps=(),
                uncertainty_acknowledged=False,
                refusal_reason=(
                    "Founder scope: the founder is not the subject of "
                    "inquiry by their own system. STORY/MEMORY are "
                    "curated by the founder, not extracted from them. "
                    "Refused per Principle #12, founder-scope clause."
                ),
                scope=self.scope,
            )
            self.logger.warning(
                f"ReflectionGate.evaluate refused: scope=founder"
            )
            return result

        # ── Wellness scope: refuse user-facing extraction ────────────────
        if self.scope == "wellness":
            # Detect whether this call is extracting from the user.
            # The signal: context names a target user as subject.
            extracting_user = any(
                k in context for k in _USER_FACING_KEYS
            ) and not context.get("inverted_user_self_reflection", False)

            if extracting_user:
                result = ReflectionResult(
                    recommendation="refuse",
                    gaps=(),
                    uncertainty_acknowledged=False,
                    refusal_reason=(
                        "Wellness scope: recursive interrogation of the "
                        "user is surveillance shape. Refused per Principle "
                        "#12, wellness-scope clause. Invert the call to "
                        "facilitate user self-reflection (pass "
                        "inverted_user_self_reflection=True in context) "
                        "or call from operator_tool scope if the subject "
                        "is the system's own work product."
                    ),
                    scope=self.scope,
                )
                self.logger.warning(
                    f"ReflectionGate.evaluate refused: scope=wellness, "
                    f"user-facing extraction"
                )
                return result

        # ── Reflector required for non-refusal paths ─────────────────────
        if self.reflector is None:
            raise ValueError(
                "ReflectionGate.evaluate called with no reflector "
                "configured. Either pass a reflector at construction or "
                "use build_reflection_prompt() to drive the LLM call "
                "yourself and call evaluate_with_response() instead."
            )

        prompt = self.build_reflection_prompt(draft, context)
        response = self.reflector(prompt, draft)
        return self.evaluate_with_response(response, context=context)

    def evaluate_with_response(
        self,
        response: ReflectorResponse,
        context: Optional[dict] = None,
    ) -> ReflectionResult:
        """
        Apply the decision logic to a pre-collected ReflectorResponse.

        Useful when the caller wires the LLM call directly (using
        build_reflection_prompt) rather than passing a reflector callback.
        Same decision logic; just skips the LLM round-trip inside the
        chassis.
        """
        context = context or {}

        # Compliance-shape detector: zero gaps + no uncertainty is the
        # failure mode Principle #12 exists to surface. The gate refuses
        # to let it pass even if the draft "looks complete."
        if (
            not response.gaps
            and not response.uncertainty_acknowledged
            and self.require_uncertainty_on_zero_gaps
            and self.scope == "operator_tool"
        ):
            return ReflectionResult(
                recommendation="iterate",
                gaps=("structural: reflector returned zero gaps with no "
                      "uncertainty acknowledged — the confident-comprehensive "
                      "failure mode. Run reflection again and require at "
                      "least one structural gap or one explicit "
                      "uncertainty.",),
                uncertainty_acknowledged=False,
                iterate_reason=(
                    "Confident-zero-gaps failure mode (Principle #12). "
                    "A truly complete answer surfaces what it does not "
                    "yet know — or names a structural limit explicitly."
                ),
                reflector_response=response,
                scope=self.scope,
            )

        # Gaps present → iterate. Caller routes gaps to RFI registry.
        if response.gaps:
            return ReflectionResult(
                recommendation="iterate",
                gaps=response.gaps,
                uncertainty_acknowledged=response.uncertainty_acknowledged,
                iterate_reason=(
                    f"Reflection surfaced {len(response.gaps)} gap(s). "
                    f"Route to RFI registry or address in next round."
                ),
                reflector_response=response,
                scope=self.scope,
            )

        # No gaps + uncertainty acknowledged → proceed.
        # The agent has done its work and named its limit.
        return ReflectionResult(
            recommendation="proceed",
            gaps=(),
            uncertainty_acknowledged=response.uncertainty_acknowledged,
            reflector_response=response,
            scope=self.scope,
        )

    # ── Construction from kit artifacts ──────────────────────────────────────

    @classmethod
    def from_kit_template(
        cls,
        template_path: Path,
        reflector: Optional[Callable[[str, str], ReflectorResponse]] = None,
        **kwargs,
    ) -> "ReflectionGate":
        """
        Build a ReflectionGate from a populated AGENT_DOCTRINE.md.

        Reads the `active_extraction_gate` KIT:FIELD. The body of that
        field is expected to indicate the scope (operator_tool / wellness
        / mixed). If 'mixed', the caller is responsible for constructing
        multiple gates per surface; this loader raises.

        Raises ValueError if the field is unpopulated or marks the
        product as `not_yet` (gate is aspirational; doctrine names the
        gap honestly rather than hand-waving a chassis instance).
        """
        if not template_path.exists():
            raise FileNotFoundError(f"template not found: {template_path}")

        # Lazy import — keeps chassis vendoring independent of coverage.
        from kit.coverage import parse_template
        fields = {f.name: f for f in parse_template(template_path)}

        gate_field = fields.get("active_extraction_gate")
        if not gate_field:
            raise ValueError(
                f"{template_path} has no active_extraction_gate field; "
                f"the template may be older than v1.2"
            )

        body = gate_field.body.strip()
        if _is_placeholder(body):
            raise ValueError(
                f"active_extraction_gate not populated in {template_path}"
            )

        scope = _infer_scope_from_body(body)
        if scope is None:
            raise ValueError(
                f"active_extraction_gate in {template_path} did not name a "
                f"scope (operator_tool / wellness / founder). Add an "
                f"explicit scope declaration."
            )

        if "not_yet" in body.lower() or "aspirational" in body.lower():
            raise ValueError(
                f"active_extraction_gate in {template_path} is marked "
                f"not_yet / aspirational. The doctrine prefers an honest "
                f"gap to a hand-waved chassis instance — name the path to "
                f"implementation before constructing the gate."
            )

        return cls(scope=scope, reflector=reflector, **kwargs)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

_PLACEHOLDER_RE = re.compile(r'^\s*\[.*\]\s*$', re.DOTALL)


def _is_placeholder(body: str) -> bool:
    stripped = body.strip()
    return bool(stripped) and bool(_PLACEHOLDER_RE.match(stripped))


def _infer_scope_from_body(body: str) -> Optional[ScopeMode]:
    """
    Infer scope from the active_extraction_gate field body.

    Looks for explicit scope language. Prefers earliest, most specific
    match. Returns None if no scope can be inferred.
    """
    lowered = body.lower()

    # Explicit declarations first (highest signal).
    if "scope: operator_tool" in lowered or "scope=operator_tool" in lowered:
        return "operator_tool"
    if "scope: wellness" in lowered or "scope=wellness" in lowered:
        return "wellness"
    if "scope: founder" in lowered or "scope=founder" in lowered:
        return "founder"

    # Fallback: keyword presence.
    if "wellness" in lowered:
        return "wellness"
    if "operator-tool" in lowered or "operator_tool" in lowered:
        return "operator_tool"
    if "founder scope" in lowered:
        return "founder"

    return None


# ──────────────────────────────────────────────────────────────────────────────
# Convenience: parse a reflector LLM response into ReflectorResponse
# ──────────────────────────────────────────────────────────────────────────────


_KNOWN_HEADER_RE = re.compile(r'^\s*KNOWN\s*:\s*$', re.MULTILINE)
_INFERRED_HEADER_RE = re.compile(r'^\s*INFERRED\s*:\s*$', re.MULTILINE)
_GAPS_HEADER_RE = re.compile(r'^\s*GAPS\s*:\s*$', re.MULTILINE)
_UNCERTAINTY_LINE_RE = re.compile(
    r'^\s*UNCERTAINTY\s*:\s*(yes|no)\b', re.MULTILINE | re.IGNORECASE
)


def parse_reflector_response(raw: str) -> ReflectorResponse:
    """
    Parse an LLM response that follows the gate's standard prompt format
    into a ReflectorResponse. Tolerant of minor formatting drift but
    requires the four section markers (KNOWN / INFERRED / GAPS /
    UNCERTAINTY) to be present.

    Callers who use a different prompt format can construct
    ReflectorResponse directly without this parser.
    """
    known = _extract_section(raw, _KNOWN_HEADER_RE,
                             [_INFERRED_HEADER_RE, _GAPS_HEADER_RE,
                              _UNCERTAINTY_LINE_RE])
    inferred = _extract_section(raw, _INFERRED_HEADER_RE,
                                [_GAPS_HEADER_RE, _UNCERTAINTY_LINE_RE])
    gaps = _extract_section(raw, _GAPS_HEADER_RE,
                            [_UNCERTAINTY_LINE_RE])

    uncertainty_match = _UNCERTAINTY_LINE_RE.search(raw)
    uncertainty = (
        uncertainty_match.group(1).lower() == "yes"
        if uncertainty_match
        else False
    )

    return ReflectorResponse(
        known=tuple(known),
        inferred=tuple(inferred),
        gaps=tuple(gaps),
        uncertainty_acknowledged=uncertainty,
        raw=raw,
    )


_BULLET_RE = re.compile(r'^\s*[-*•]\s*(.+?)\s*$')


def _extract_section(
    text: str,
    header_re: re.Pattern,
    end_res: list[re.Pattern],
) -> list[str]:
    """Pull bullet-list items between a header and the next section."""
    header = header_re.search(text)
    if not header:
        return []
    start = header.end()

    # Find the earliest end-marker after start.
    end = len(text)
    for end_re in end_res:
        m = end_re.search(text, pos=start)
        if m and m.start() < end:
            end = m.start()

    section_body = text[start:end]
    items: list[str] = []
    for raw_line in section_body.splitlines():
        m = _BULLET_RE.match(raw_line)
        if not m:
            continue
        candidate = m.group(1).strip()
        if not candidate:
            continue
        items.append(candidate)
    return items
