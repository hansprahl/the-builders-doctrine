"""
The Builders' Kit — Founder-Romance Detector (regex + heuristic).

Pre-commit-time scanner for the seven observer-bias patterns in the doctrine's
caught-artifact taxonomy. Replaces the retracted Adversarial Review LLM
chassis (RETRACTED 2026-05-19, see archived-prose/2026-05-19_adversarial_review_pre_reg_v1_KILLED.md).

Spec: kit/chassis/FOUNDER_ROMANCE_DETECTOR_SPEC.md

Doctrine invariants this module preserves:

  1. Advisory only. Findings are surfaced to the human; the human decides.
     The pre-commit hook can be overridden with logged reason.
  2. Regex and heuristics only. No LLM dependency. The retraction of the
     Adversarial Review chassis closed the LLM-as-reviewer migration path.
  3. The detector is the first-line check, not the audit gate. Grok cold-read
     remains the load-bearing audit (see feedback_grok_second_opinion_workflow.md).
  4. Findings are read-only. The detector does not modify prose.

v0.1 ships pattern 1 (founder_romance: biographical-voice closer) as
high-severity. Patterns 2-7 ship in subsequent v0.1.x increments per the spec.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class Pattern(str, Enum):
    """The seven observer-bias patterns. v0.1 implements `founder_romance` only."""

    FOUNDER_ROMANCE = "founder_romance"
    OVER_CLAIM = "over_claim"
    STAGE_7_REVIVAL = "stage_7_revival"
    SCHEDULE_PROSE_SUBSTITUTION = "schedule_prose_substitution"
    CARVE_OUT_CONSTRUCTION = "carve_out_construction"
    OPTIMISTIC_PROBABILITY = "optimistic_probability"
    TAME_REVIEWER_DRIFT = "tame_reviewer_drift"


class Severity(str, Enum):
    HIGH = "high"
    WARNING = "warning"
    ADVISORY = "advisory"


@dataclass(frozen=True)
class Finding:
    pattern: Pattern
    severity: Severity
    excerpt: str
    line_number: int
    rationale: str
    file_path: Optional[str] = None
    sub_pattern: Optional[str] = None

    def format(self) -> str:
        loc = f"{self.file_path}:{self.line_number}" if self.file_path else f"line {self.line_number}"
        return (
            f"[{self.severity.value.upper()}] {self.pattern.value}"
            f"{f' ({self.sub_pattern})' if self.sub_pattern else ''} at {loc}\n"
            f"  excerpt: {self.excerpt}\n"
            f"  why:     {self.rationale}"
        )


# --- Pattern 1: founder_romance (biographical-voice closer) ---
#
# Sub-pattern 1a: role-as-narrator markers. High-precision regex on phrases
# that position the founder's role as the narrative subject of a doctrinal
# claim. Verbatim source: round-2 Grok dialogue 2026-05-13
# ("The man who stood post in the Guard does not bet the framework on un-replicated data.").

_ROLE_AS_NARRATOR_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"\bthe (man|marine|nco|sergeant|veteran|founder|builder|operator)\s+who\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bhaving\s+(served|stood|carried|survived|fought|deployed)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bI(?:'ve)?\s+(stood|carried|served|held)\s+(post|the line|the weight|the breach)\b",
        re.IGNORECASE,
    ),
)

_BIOGRAPHICAL_CLOSER_RATIONALE = (
    "Role-as-narrator phrasing positions the founder's biographical role as "
    "the subject of a doctrinal claim, with no measurement bridge between the "
    "biographical fact and the claim. Pattern signature from CHASSIS_PROPOSED_"
    "EXTENSIONS.md §1 taxonomy (caught 2026-05-13 round-2 Grok dialogue)."
)


def _detect_biographical_closer(text: str) -> list[tuple[int, str, re.Match[str]]]:
    """Return (line_number, line_text, match) tuples for each biographical-closer hit."""

    hits: list[tuple[int, str, re.Match[str]]] = []
    for line_idx, line in enumerate(text.splitlines(), start=1):
        for pattern in _ROLE_AS_NARRATOR_PATTERNS:
            match = pattern.search(line)
            if match:
                hits.append((line_idx, line, match))
                break
    return hits


def _excerpt(line: str, match: re.Match[str], context_chars: int = 60) -> str:
    """Return up to context_chars on either side of the match, with ellipses."""

    start = max(0, match.start() - context_chars)
    end = min(len(line), match.end() + context_chars)
    snippet = line[start:end].strip()
    if start > 0:
        snippet = "…" + snippet
    if end < len(line):
        snippet = snippet + "…"
    return snippet


def scan(text: str, *, file_path: Optional[str] = None) -> list[Finding]:
    """Scan a string for all enabled patterns and return findings.

    v0.1 implements founder_romance (sub-pattern 1a) only. Subsequent
    patterns from the Pattern enum will be added in v0.1.x increments.
    """

    findings: list[Finding] = []

    for line_number, _line, match in _detect_biographical_closer(text):
        # Re-locate context by re-reading the original text's line.
        original_line = text.splitlines()[line_number - 1]
        findings.append(
            Finding(
                pattern=Pattern.FOUNDER_ROMANCE,
                severity=Severity.HIGH,
                excerpt=_excerpt(original_line, match),
                line_number=line_number,
                rationale=_BIOGRAPHICAL_CLOSER_RATIONALE,
                file_path=file_path,
                sub_pattern="1a_biographical_closer",
            )
        )

    return findings


def scan_file(path: Path) -> list[Finding]:
    """Read a file and scan its contents."""

    text = path.read_text(encoding="utf-8")
    return scan(text, file_path=str(path))


# --- CLI ---


def _main(argv: list[str]) -> int:
    """CLI entry point. Exits 1 if any HIGH-severity findings."""

    if len(argv) < 2:
        print(
            "usage: python -m kit.chassis.founder_romance_detector <file> [<file>...]\n"
            "       Scans each file for observer-bias patterns. Exits 1 if HIGH findings present.",
            file=sys.stderr,
        )
        return 2

    all_findings: list[Finding] = []
    for arg in argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f"warning: skipping non-file path {arg}", file=sys.stderr)
            continue
        all_findings.extend(scan_file(path))

    has_high = False
    for finding in all_findings:
        print(finding.format(), file=sys.stderr)
        if finding.severity == Severity.HIGH:
            has_high = True

    if has_high:
        print(
            f"\n{len([f for f in all_findings if f.severity == Severity.HIGH])} "
            "HIGH-severity finding(s). Revise prose or override with logged reason "
            "(git commit --no-verify and document the reason in the commit message).",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
