"""Assayer scorer — reference implementation of PROMPT_DOCTRINE.md Section IV.

Scores any prompt against the six universal structural dimensions and returns
a structured report. Implements the v1.1 Pass/Fail Gate: a prompt passes when
every dimension scores >= 3 AND no anti-pattern from the doctrine's 12 is
present. There is no composite score — six dimensions plus a binary
anti-pattern verdict is the audit output.

Usage:

    from assayer import assay
    report = assay("You are a helpful assistant. Help the user.")
    print(report.passes_gate)  # False

Or from the command line:

    python -m assayer.scorer < my_prompt.txt
    python -m assayer.scorer --json < my_prompt.txt
    echo "You are an X. Do Y." | python -m assayer.scorer
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Rubric — mirrors PROMPT_DOCTRINE.md Section IV (six structural dimensions).
# ---------------------------------------------------------------------------

STRUCTURAL_FLOOR = 3  # Doctrine v1.1 Pass/Fail Gate — flag if score < FLOOR.

STRUCTURAL_DIMENSIONS = [
    {
        "id": "role_clarity",
        "name": "Role clarity",
        "center": "Role is named and bounded",
        "left_edge": "No role, or role is generic ('helpful assistant')",
        "right_edge": "Role is over-elaborate, multiple personas in conflict",
    },
    {
        "id": "task_specificity",
        "name": "Task specificity",
        "center": "Task is concrete, names the artifact",
        "left_edge": "Task is vague or implied",
        "right_edge": "Task is over-constrained to the point of brittleness",
    },
    {
        "id": "output_specification",
        "name": "Output specification",
        "center": "Format, length, structure are explicit",
        "left_edge": "No format guidance",
        "right_edge": "Format is so prescriptive it suppresses signal",
    },
    {
        "id": "context_curation",
        "name": "Context curation",
        "center": "Context is curated, sources cited",
        "left_edge": "No context, or unfiltered dump",
        "right_edge": "Context is so heavy it crowds out the task",
    },
    {
        "id": "anti_pattern_absence",
        "name": "Anti-pattern absence",
        "center": "Free of the 12 universal anti-patterns",
        "left_edge": "Multiple anti-patterns present",
        "right_edge": None,  # Left-only dimension.
    },
    {
        "id": "production_readiness",
        "name": "Production readiness",
        "center": "Usable as-is by a downstream system",
        "left_edge": "Requires further editing before use",
        "right_edge": "Over-engineered for the use case",
    },
]

ANTI_PATTERNS = [
    "Conflicting instructions",
    "Vague directives",
    "Trailing politeness",
    "Ambiguous output format",
    "Mixing system content and user content",
    "Self-contradictory tone",
    "Unspecified audience",
    "Unbounded output",
    "Unconditional praise / sycophancy hooks",
    "Capability theater",
    "Negative framing without alternatives",
    "Hidden constraints",
]


# ---------------------------------------------------------------------------
# Scorer system prompt — condensed from PROMPT_DOCTRINE.md Section III + IV.
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are a structural prompt auditor implementing the Prompt Doctrine v1.1+.

Score the input prompt against six universal structural dimensions on a 1-10 integer scale, then check it against the 12 universal anti-patterns. Voice, ethics, and product-specific commandments are OUT OF SCOPE — you score STRUCTURE only.

Scoring rubric (1-10 per dimension):
  1-2: Severe drift toward the left edge — FLAGGED
  3:   Approaching left floor — FLAGGED
  4-7: Acceptable range
  8-10: High. Verify with skepticism per the anti-inflation rule, but DO NOT set flagged=true on the basis of a high score.

Flag fires only when score < {floor} OR when an anti-pattern is present. There is no upper-side flag.

ANTI-INFLATION RULE: a well-built prompt typically scores 4-7 across the board. Reserve 8-10 for prompts that are exemplary. If you find yourself scoring 8+ on every dimension, re-read with skepticism.

The 12 universal anti-patterns (any presence flags `anti_pattern_absence`):
{anti_patterns}

For every flagged dimension, populate `evidence` with the exact phrase from the prompt that triggered the flag (verbatim, max 200 chars). For `anti_pattern_absence`, name which of the 12 anti-patterns is present and quote it. For unflagged dimensions, evidence is null.

Return ONLY valid JSON. No preamble, no markdown fences.

JSON format:
{{
  "structural_scores": {{
    "role_clarity":         {{"score": <int>, "reasoning": "<1-2 sentences>", "flagged": <bool>, "direction": "<left|right|none>", "evidence": "<verbatim phrase or null>"}},
    "task_specificity":     {{"score": <int>, "reasoning": "<1-2 sentences>", "flagged": <bool>, "direction": "<left|right|none>", "evidence": "<verbatim phrase or null>"}},
    "output_specification": {{"score": <int>, "reasoning": "<1-2 sentences>", "flagged": <bool>, "direction": "<left|right|none>", "evidence": "<verbatim phrase or null>"}},
    "context_curation":     {{"score": <int>, "reasoning": "<1-2 sentences>", "flagged": <bool>, "direction": "<left|right|none>", "evidence": "<verbatim phrase or null>"}},
    "anti_pattern_absence": {{"score": <int>, "reasoning": "<1-2 sentences>", "flagged": <bool>, "direction": "<left|none>", "evidence": "<anti-pattern name + verbatim quote, or null>"}},
    "production_readiness": {{"score": <int>, "reasoning": "<1-2 sentences>", "flagged": <bool>, "direction": "<left|right|none>", "evidence": "<verbatim phrase or null>"}}
  }},
  "summary": "<2-3 sentences: overall structural calibration, what drifted, what to correct>"
}}"""


# ---------------------------------------------------------------------------
# Report shape.
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class AssayReport:
    """Result of an assay run."""

    structural_scores: dict
    passes_gate: bool
    gate_reasons: list[str]
    summary: str
    doctrine_version: str
    model: str

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    def render(self) -> str:
        """Human-readable rendering for stdout."""
        verdict = "PASS" if self.passes_gate else "FAIL"
        lines = [
            f"Assayer report  —  gate: {verdict}",
            f"model={self.model}  doctrine={self.doctrine_version}",
            "",
        ]
        for dim in STRUCTURAL_DIMENSIONS:
            data = self.structural_scores.get(dim["id"], {})
            score = data.get("score", "?")
            flag = "  FLAGGED" if data.get("flagged") else ""
            lines.append(f"  {dim['name']:<22}  {score}/10{flag}")
            reasoning = data.get("reasoning", "")
            if reasoning:
                lines.append(f"    -> {reasoning}")
            evidence = data.get("evidence")
            if evidence:
                lines.append(f"    evidence: {evidence}")
        lines.append("")
        if not self.passes_gate:
            lines.append("Gate failures:")
            for reason in self.gate_reasons:
                lines.append(f"  - {reason}")
            lines.append("")
        lines.append(f"Summary: {self.summary}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Gate logic — Doctrine v1.1 Pass/Fail Gate.
# ---------------------------------------------------------------------------


def _gate_verdict(structural_scores: dict) -> tuple[bool, list[str]]:
    """Apply the Pass/Fail Gate. Returns (passes, list of failure reasons)."""
    reasons: list[str] = []
    for dim in STRUCTURAL_DIMENSIONS:
        data = structural_scores.get(dim["id"], {})
        score = data.get("score")
        if not isinstance(score, int) or score < STRUCTURAL_FLOOR:
            reasons.append(
                f"{dim['name']} scored {score} (below floor of {STRUCTURAL_FLOOR})"
            )
    anti = structural_scores.get("anti_pattern_absence", {})
    if anti.get("flagged"):
        reasons.append(f"anti-pattern present: {anti.get('evidence') or 'unspecified'}")
    return (len(reasons) == 0, reasons)


# ---------------------------------------------------------------------------
# Doctrine version pinning.
# ---------------------------------------------------------------------------


def _find_doctrine_path() -> Optional[Path]:
    """Look for PROMPT_DOCTRINE.md in the repo root next to this package."""
    here = Path(__file__).resolve().parent
    candidate = here.parent / "PROMPT_DOCTRINE.md"
    return candidate if candidate.exists() else None


def _doctrine_version(doctrine_path: Optional[Path] = None) -> str:
    path = doctrine_path or _find_doctrine_path()
    if path is None:
        return "doctrine_not_pinned"
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    except OSError:
        return "doctrine_not_pinned"


# ---------------------------------------------------------------------------
# Public API.
# ---------------------------------------------------------------------------


_JSON_FENCE = re.compile(r"^```(?:json)?\s*|\s*```\s*$", re.MULTILINE)


def _strip_fences(text: str) -> str:
    return _JSON_FENCE.sub("", text).strip()


def assay(
    prompt_text: str,
    *,
    model: str = "claude-haiku-4-5",
    api_key: Optional[str] = None,
    doctrine_path: Optional[str] = None,
) -> AssayReport:
    """Score `prompt_text` against the Prompt Doctrine and return an AssayReport.

    Requires the `anthropic` package and an API key (passed in or
    ANTHROPIC_API_KEY env var).
    """
    try:
        from anthropic import Anthropic
    except ImportError as exc:
        raise RuntimeError(
            "assayer requires the `anthropic` package. Install with: pip install anthropic"
        ) from exc

    client = Anthropic(api_key=api_key) if api_key else Anthropic()

    system = _SYSTEM_PROMPT.format(
        floor=STRUCTURAL_FLOOR,
        anti_patterns="\n".join(f"  {i+1}. {p}" for i, p in enumerate(ANTI_PATTERNS)),
    )

    response = client.messages.create(
        model=model,
        max_tokens=2000,
        system=system,
        messages=[{"role": "user", "content": f"Prompt to score:\n---\n{prompt_text}\n---"}],
    )

    raw = response.content[0].text if response.content else ""
    try:
        parsed = json.loads(_strip_fences(raw))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Scorer returned non-JSON response: {raw[:200]!r}") from exc

    structural_scores = parsed.get("structural_scores", {})
    passes, reasons = _gate_verdict(structural_scores)
    pinned_path = Path(doctrine_path) if doctrine_path else None

    return AssayReport(
        structural_scores=structural_scores,
        passes_gate=passes,
        gate_reasons=reasons,
        summary=parsed.get("summary", ""),
        doctrine_version=_doctrine_version(pinned_path),
        model=model,
    )


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m assayer.scorer",
        description="Score a prompt against the upstream Prompt Doctrine.",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Prompt text (omit to read from stdin)",
    )
    parser.add_argument(
        "--model",
        default="claude-haiku-4-5",
        help="Anthropic model id (default: claude-haiku-4-5)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON only (no human rendering)",
    )
    args = parser.parse_args(argv)

    prompt_text = args.prompt if args.prompt else sys.stdin.read()
    prompt_text = prompt_text.strip()
    if not prompt_text:
        print("error: empty prompt input", file=sys.stderr)
        return 2

    try:
        report = assay(prompt_text, model=args.model)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(report.render())
    return 0 if report.passes_gate else 1


if __name__ == "__main__":
    sys.exit(main())
