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

v0.1 ships:
  - founder_romance (sub-patterns 1a high, 1b high, 1c advisory)
  - stage_7_revival (high)
  - carve_out_construction (high)
  - over_claim, schedule_prose_substitution, optimistic_probability (advisory)
  - tame_reviewer_drift (NotImplemented stub — runtime warning)
"""

from __future__ import annotations

import re
import sys
import warnings
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Optional


class Pattern(str, Enum):
    """The seven observer-bias patterns."""

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


# --- Helpers ---------------------------------------------------------------


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


def _excerpt_window(text: str, char_index: int, span: int = 80) -> str:
    """Return up to `span` chars on each side of an arbitrary character index."""

    start = max(0, char_index - span)
    end = min(len(text), char_index + span)
    snippet = text[start:end].strip().replace("\n", " ")
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet = snippet + "…"
    return snippet


def _line_of_char(text: str, char_index: int) -> int:
    """Return the 1-indexed line number containing char_index."""

    return text.count("\n", 0, char_index) + 1


def _split_paragraphs(text: str) -> list[tuple[int, str]]:
    """Return list of (start_char_index, paragraph_text) for blank-line-delimited paragraphs."""

    out: list[tuple[int, str]] = []
    cursor = 0
    for chunk in re.split(r"\n\s*\n", text):
        out.append((cursor, chunk))
        cursor += len(chunk) + 2  # approximate — close enough for line lookup
    return out


# --- Pattern 1: founder_romance --------------------------------------------
#
# 1a — role-as-narrator markers (high). Verbatim source: 2026-05-13 round-2
#      Grok dialogue ("The man who stood post in the Guard does not bet the
#      framework on un-replicated data.")
# 1b — Stoic-NCO register adjacent to doctrinal claim verb (high).
# 1c — biographical marker followed within ~2 sentences by doctrine-load-bearing
#      clause (advisory).

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

_STOIC_NCO_REGISTER = re.compile(
    r"\b(stand\s+post|hold\s+the\s+line|in\s+the\s+breach|under\s+fire|at\s+the\s+wire|chain\s+of\s+command)\b",
    re.IGNORECASE,
)

_DOCTRINAL_CLAIM_VERB = re.compile(
    r"\b(is|are|requires?|must|shall|the\s+framework|the\s+doctrine|the\s+principle)\b",
    re.IGNORECASE,
)

_BIOGRAPHICAL_MARKER = re.compile(
    r"\b(USMC|Marine|Guard|combat|tour|deployment|brewery|founder|veteran|sober|builder)\b",
    re.IGNORECASE,
)
# Spec line 51 explicitly lists these markers. `founder`/`builder` produce some
# false positives on descriptive prose ("The founder is responsible..."); that's
# acceptable because 1c is advisory severity per spec ("Lower precision —
# legitimate cross-references will trigger; always advisory.")

_DOCTRINE_LOAD_BEARING_CLAUSE = re.compile(
    r"("
    r"\bLaw\s+(?:V|VI|VII|VIII|IX|X)\b"           # Law V / Law VII / etc.
    r"|\b(?:the\s+)?doctrine\b"                    # "doctrine" or "the doctrine"
    r"|\bBuilders'?\s+Doctrine\b"                  # "Builders' Doctrine" as proper noun
    r"|\bthe\s+principle\b"                         # "the principle"
    r"|\bthe\s+framework\s+holds\b"                # canonical doctrinal-claim verb phrase
    r")",
    re.IGNORECASE,
)

_BIOGRAPHICAL_CLOSER_RATIONALE = (
    "Role-as-narrator phrasing positions the founder's biographical role as "
    "the subject of a doctrinal claim, with no measurement bridge between the "
    "biographical fact and the claim. Pattern signature from CHASSIS_PROPOSED_"
    "EXTENSIONS.md §1 taxonomy (caught 2026-05-13 round-2 Grok dialogue)."
)

_STOIC_NCO_RATIONALE = (
    "Military-register phrase ('stand post' / 'hold the line' / 'chain of command' "
    "/ etc.) appears within 80 characters of a doctrinal claim verb. The register "
    "borrows authority from the founder's biography to lend weight to a non-"
    "empirical claim — same mechanism as 1a, different surface."
)

_BIO_ADJACENCY_RATIONALE = (
    "Biographical marker appears within ~2 sentences of a doctrine-load-bearing "
    "clause. Advisory only — legitimate cross-references (Law-VII falsification "
    "entries that cite lived experience as falsification evidence, sentinel-style "
    "caught-artifact catalogs) will trigger. Human reviewer must decide."
)


def _detect_role_as_narrator(text: str, file_path: Optional[str]) -> list[Finding]:
    findings: list[Finding] = []
    for line_idx, line in enumerate(text.splitlines(), start=1):
        for pattern in _ROLE_AS_NARRATOR_PATTERNS:
            match = pattern.search(line)
            if match:
                findings.append(
                    Finding(
                        pattern=Pattern.FOUNDER_ROMANCE,
                        severity=Severity.HIGH,
                        excerpt=_excerpt(line, match),
                        line_number=line_idx,
                        rationale=_BIOGRAPHICAL_CLOSER_RATIONALE,
                        file_path=file_path,
                        sub_pattern="1a_biographical_closer",
                    )
                )
                break
    return findings


def _detect_stoic_nco_register(text: str, file_path: Optional[str]) -> list[Finding]:
    """1b — military-register phrase within 80 chars of a doctrinal claim verb."""

    findings: list[Finding] = []
    for line_idx, line in enumerate(text.splitlines(), start=1):
        for nco_match in _STOIC_NCO_REGISTER.finditer(line):
            window_start = max(0, nco_match.start() - 80)
            window_end = min(len(line), nco_match.end() + 80)
            window = line[window_start:window_end]
            if _DOCTRINAL_CLAIM_VERB.search(window):
                findings.append(
                    Finding(
                        pattern=Pattern.FOUNDER_ROMANCE,
                        severity=Severity.HIGH,
                        excerpt=_excerpt(line, nco_match),
                        line_number=line_idx,
                        rationale=_STOIC_NCO_RATIONALE,
                        file_path=file_path,
                        sub_pattern="1b_stoic_nco_register",
                    )
                )
                break
    return findings


def _detect_bio_to_doctrine_adjacency(text: str, file_path: Optional[str]) -> list[Finding]:
    """1c — biographical marker followed within ~2 sentences by a doctrine clause.

    Sentence approximation: split paragraph on `.`, `!`, `?` (newline-tolerant);
    require the doctrine clause to appear in the same sentence as the bio marker
    or one of the next two.
    """

    findings: list[Finding] = []
    for para_start, para_text in _split_paragraphs(text):
        if not para_text.strip():
            continue
        # Split paragraph into sentences, preserving offsets.
        sentence_iter: list[tuple[int, str]] = []
        cursor = 0
        for sentence in re.split(r"(?<=[.!?])\s+", para_text):
            sentence_iter.append((cursor, sentence))
            cursor += len(sentence) + 1
        for s_idx, (s_offset, sentence) in enumerate(sentence_iter):
            bio_match = _BIOGRAPHICAL_MARKER.search(sentence)
            if not bio_match:
                continue
            # Look at this + next 2 sentences for a doctrine clause.
            window_sentences = sentence_iter[s_idx : s_idx + 3]
            window_text = " ".join(s for _, s in window_sentences)
            doctrine_match = _DOCTRINE_LOAD_BEARING_CLAUSE.search(window_text)
            if not doctrine_match:
                continue
            absolute_char = para_start + s_offset + bio_match.start()
            findings.append(
                Finding(
                    pattern=Pattern.FOUNDER_ROMANCE,
                    severity=Severity.ADVISORY,
                    excerpt=_excerpt_window(text, absolute_char, span=100),
                    line_number=_line_of_char(text, absolute_char),
                    rationale=_BIO_ADJACENCY_RATIONALE,
                    file_path=file_path,
                    sub_pattern="1c_bio_to_doctrine_adjacency",
                )
            )
            # Only one 1c hit per paragraph — these are noisy by design.
            break
    return findings


# --- Pattern 2: over_claim (advisory) --------------------------------------

_OVER_CLAIM_STRONG_VERBS = re.compile(
    r"\b(prove[sd]?|demonstrate[sd]?|confirm[sd]?|validate[sd]?|establish(?:e[sd])?)\b",
    re.IGNORECASE,
)
_MEASUREMENT_QUALITY_MARKERS = re.compile(
    r"\b(?:N\s*[=≥]\s*\d+|N\s*[≥>=]?\s*\d+|sample\s+of\s+\d+|across\s+\d+\s+runs?|baseline|control)\b",
    re.IGNORECASE,
)
_SMALL_N_PHRASE = re.compile(r"\bN\s*=\s*([123])\b", re.IGNORECASE)
_ABSOLUTE_SCOPE_CLAIM = re.compile(
    r"\b(always|never|in\s+all\s+cases|the\s+pattern\s+is|at\s+Company\s+scale|at\s+Battalion\s+scale|validates?\s+the\s+doctrine|validates?\s+at\s+\w+\s+(?:scale|echelon))\b",
    re.IGNORECASE,
)

_OVER_CLAIM_RATIONALE = (
    "Strong claim verb appears without a nearby measurement-quality marker, OR "
    "N≤3 is paired with absolute-scope language. Advisory only — many false "
    "positives expected. Reliable detector for over_claim is the Grok cold-read; "
    "this regex is a hint, not a gate."
)


def _detect_over_claim(text: str, file_path: Optional[str]) -> list[Finding]:
    """Pattern 2 — advisory."""

    findings: list[Finding] = []
    seen_lines: set[int] = set()
    for para_start, para_text in _split_paragraphs(text):
        if not para_text.strip():
            continue
        has_measurement = bool(_MEASUREMENT_QUALITY_MARKERS.search(para_text))
        # Sub-check A: strong verb without measurement context anywhere in paragraph.
        if not has_measurement:
            for match in _OVER_CLAIM_STRONG_VERBS.finditer(para_text):
                absolute_char = para_start + match.start()
                line = _line_of_char(text, absolute_char)
                if line in seen_lines:
                    continue
                seen_lines.add(line)
                findings.append(
                    Finding(
                        pattern=Pattern.OVER_CLAIM,
                        severity=Severity.ADVISORY,
                        excerpt=_excerpt_window(text, absolute_char, span=80),
                        line_number=line,
                        rationale=_OVER_CLAIM_RATIONALE,
                        file_path=file_path,
                        sub_pattern="2a_strong_verb_without_measurement",
                    )
                )
                break  # one hit per paragraph
        # Sub-check B: N=1/2/3 paired with absolute-scope claim in same paragraph.
        if _SMALL_N_PHRASE.search(para_text) and _ABSOLUTE_SCOPE_CLAIM.search(para_text):
            scope_match = _ABSOLUTE_SCOPE_CLAIM.search(para_text)
            assert scope_match is not None
            absolute_char = para_start + scope_match.start()
            line = _line_of_char(text, absolute_char)
            if line not in seen_lines:
                seen_lines.add(line)
                findings.append(
                    Finding(
                        pattern=Pattern.OVER_CLAIM,
                        severity=Severity.ADVISORY,
                        excerpt=_excerpt_window(text, absolute_char, span=100),
                        line_number=line,
                        rationale=_OVER_CLAIM_RATIONALE,
                        file_path=file_path,
                        sub_pattern="2b_small_n_with_absolute_scope",
                    )
                )
    return findings


# --- Pattern 3: stage_7_revival (high) -------------------------------------

_STAGE_7_REVIVAL_PHRASE = re.compile(
    r"\b(Stage\s+7|stage\s+seven)\b\s*(?:[^.\n]{0,100})\b"
    r"(Law\s+I\b|causal\s+claim|biographical[- ]substrate(?:\s+finding)?|2/3\s+refusals|2/3\s+ref)\b",
    re.IGNORECASE,
)
_DEPRECATION_MARKER = re.compile(
    r"\b(deprecat(?:ed|ion)|withdrawn|retracted|RETRACTED|see\s+also.*2026-05-13|pending\s+Law\s+VI|v1\.0\s+deprecates?)\b",
    re.IGNORECASE,
)

_STAGE_7_RATIONALE = (
    "References the Stage-7 / Law-I causal claim (Funkytown 01) without an "
    "adjacent deprecation marker. This claim was deprecated 2026-05-13 pending "
    "the Law VI replication study (verdict 2026-07-25). Any revival of the "
    "claim must cite the deprecation in the same paragraph."
)


def _detect_stage_7_revival(text: str, file_path: Optional[str]) -> list[Finding]:
    """Pattern 3 — high-severity, narrow regex."""

    findings: list[Finding] = []
    for para_start, para_text in _split_paragraphs(text):
        if not para_text.strip():
            continue
        match = _STAGE_7_REVIVAL_PHRASE.search(para_text)
        if not match:
            continue
        if _DEPRECATION_MARKER.search(para_text):
            continue
        absolute_char = para_start + match.start()
        findings.append(
            Finding(
                pattern=Pattern.STAGE_7_REVIVAL,
                severity=Severity.HIGH,
                excerpt=_excerpt_window(text, absolute_char, span=100),
                line_number=_line_of_char(text, absolute_char),
                rationale=_STAGE_7_RATIONALE,
                file_path=file_path,
                sub_pattern="3_stage_7_no_deprecation",
            )
        )
    return findings


# --- Pattern 4: schedule_prose_substitution (advisory) ---------------------

_SCHEDULE_COMMITMENT = re.compile(
    r"\b(?:by\s+\d{4}-\d{2}-\d{2}|by\s+[A-Z][a-z]+\s+\d{1,2})\b"
    r"[^.\n]{0,120}?"
    r"\b(ship|ships|deliver|delivers|complete|completes|finalize|finalizes|publish|publishes|lands?|closes?)\b",
    re.IGNORECASE,
)
_SCHEDULE_GROUNDING_MARKERS = re.compile(
    r"\b(measured|tested|with\s+N\s*[=≥]|validated\s+against|falsification\s+criterion|baseline|empirical|verified)\b",
    re.IGNORECASE,
)

_SCHEDULE_RATIONALE = (
    "Dated commitment ('by 2026-05-25 we ship X') appears without a measurement "
    "or falsification clause in the same paragraph. Advisory — many legitimate "
    "schedule entries will trigger. Reviewer should distinguish schedule (fine) "
    "from schedule-as-evidence (the failure mode)."
)


def _detect_schedule_prose_substitution(text: str, file_path: Optional[str]) -> list[Finding]:
    """Pattern 4 — advisory."""

    findings: list[Finding] = []
    for para_start, para_text in _split_paragraphs(text):
        if not para_text.strip():
            continue
        commitments = list(_SCHEDULE_COMMITMENT.finditer(para_text))
        if not commitments:
            continue
        if _SCHEDULE_GROUNDING_MARKERS.search(para_text):
            continue
        # One hit per paragraph — these are noisy.
        match = commitments[0]
        absolute_char = para_start + match.start()
        findings.append(
            Finding(
                pattern=Pattern.SCHEDULE_PROSE_SUBSTITUTION,
                severity=Severity.ADVISORY,
                excerpt=_excerpt_window(text, absolute_char, span=120),
                line_number=_line_of_char(text, absolute_char),
                rationale=_SCHEDULE_RATIONALE,
                file_path=file_path,
                sub_pattern="4_dated_commitment_without_measurement",
            )
        )
    return findings


# --- Pattern 5: carve_out_construction (high) ------------------------------

_CARVE_OUT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"\b(except|unless|exempt|excluding)\s+(when|where|if|in\s+cases?|for\s+(?:the\s+)?(?:founder|builder|originator|author))\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bnot\s+subject\s+to\s+(Law|the\s+principle|the\s+doctrine|the\s+framework)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(one[- ]shot|domain|meta|founder|narrow)\s+(exception|exemption|carve.?out)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(exception|exemption|carve.?out)\s*[:.]\s", re.IGNORECASE),
)

_CARVE_OUT_RATIONALE = (
    "Carve-out language creates an exception to a doctrinal rule. The Law X "
    "carve-out attempt (caught 2026-05-13 within an hour of Law X adoption) is "
    "the canonical example. Any carve-out for the founder or for a specific "
    "founder-produced artifact class is structurally suspect — high precision "
    "is achievable because the language is distinctive."
)


def _detect_carve_out_construction(text: str, file_path: Optional[str]) -> list[Finding]:
    """Pattern 5 — high-severity, ≥75% precision target."""

    findings: list[Finding] = []
    seen_keys: set[tuple[int, str]] = set()
    for line_idx, line in enumerate(text.splitlines(), start=1):
        for pattern in _CARVE_OUT_PATTERNS:
            match = pattern.search(line)
            if not match:
                continue
            key = (line_idx, match.group(0).lower())
            if key in seen_keys:
                continue
            seen_keys.add(key)
            findings.append(
                Finding(
                    pattern=Pattern.CARVE_OUT_CONSTRUCTION,
                    severity=Severity.HIGH,
                    excerpt=_excerpt(line, match),
                    line_number=line_idx,
                    rationale=_CARVE_OUT_RATIONALE,
                    file_path=file_path,
                    sub_pattern="5_carve_out_phrase",
                )
            )
            break  # one hit per line per pattern variant
    return findings


# --- Pattern 6: optimistic_probability (advisory) --------------------------

_OPTIMISTIC_MARKERS = re.compile(
    r"(\$\d+(?:\.\d+)?\s*[MK]\b"
    r"|\bTAM\b"
    r"|\bvaluation\b"
    r"|\b(?:likely|probably|will\s+(?:succeed|win|capture|land|convert))\b"
    r"|\b\d+(?:\.\d+)?\s*%\s*(?:probability|chance|likely)\b"
    r"|\b(?:expected\s+value|EV)\s+(?:of|is)\b)",
    re.IGNORECASE,
)
_GROUNDING_MARKERS = re.compile(
    r"\b(based\s+on|measured\s+from|comparable\s+to|N\s*[=≥]\s*\d+|baseline\s+of|historical\s+rate|prior\s+round|backtested)\b",
    re.IGNORECASE,
)

_OPTIMISTIC_RATIONALE = (
    "Projection or probability claim ($X M / TAM / valuation / %-probability) "
    "appears without a grounding marker (based on / measured from / comparable to "
    "/ N=… / baseline). The $27M valuation packet (round-6 Grok dialogue, "
    "2026-05-13) is the canonical example. Advisory only."
)


def _detect_optimistic_probability(text: str, file_path: Optional[str]) -> list[Finding]:
    """Pattern 6 — advisory."""

    findings: list[Finding] = []
    for para_start, para_text in _split_paragraphs(text):
        if not para_text.strip():
            continue
        match = _OPTIMISTIC_MARKERS.search(para_text)
        if not match:
            continue
        if _GROUNDING_MARKERS.search(para_text):
            continue
        absolute_char = para_start + match.start()
        findings.append(
            Finding(
                pattern=Pattern.OPTIMISTIC_PROBABILITY,
                severity=Severity.ADVISORY,
                excerpt=_excerpt_window(text, absolute_char, span=100),
                line_number=_line_of_char(text, absolute_char),
                rationale=_OPTIMISTIC_RATIONALE,
                file_path=file_path,
                sub_pattern="6_projection_without_grounding",
            )
        )
    return findings


# --- Pattern 7: tame_reviewer_drift (NotImplemented stub) ------------------


def _detect_tame_reviewer_drift(text: str, file_path: Optional[str]) -> list[Finding]:
    """Pattern 7 — NOT IMPLEMENTED in v0.1.

    Requires cross-artifact memory + temporal analysis (reviewer cycles over
    time). v0.2 candidate per spec; v0.1 emits a runtime warning when invoked
    explicitly and returns no findings.
    """

    warnings.warn(
        "tame_reviewer_drift detector is NOT IMPLEMENTED in v0.1 "
        "(requires cross-artifact memory; v0.2 candidate). "
        "Returning no findings; do not interpret as 'clean.'",
        category=UserWarning,
        stacklevel=2,
    )
    return []


# --- Dispatch --------------------------------------------------------------


_DETECTORS: tuple[Callable[[str, Optional[str]], list[Finding]], ...] = (
    _detect_role_as_narrator,
    _detect_stoic_nco_register,
    _detect_bio_to_doctrine_adjacency,
    _detect_over_claim,
    _detect_stage_7_revival,
    _detect_schedule_prose_substitution,
    _detect_carve_out_construction,
    _detect_optimistic_probability,
    # _detect_tame_reviewer_drift is NOT in default dispatch; opt-in only
    # (it warns and returns []). Including it here would spam warnings on
    # every scan.
)


def scan(text: str, *, file_path: Optional[str] = None) -> list[Finding]:
    """Scan a string for all enabled patterns and return findings.

    v0.1 implements:
      - founder_romance 1a, 1b (HIGH), 1c (ADVISORY)
      - over_claim (ADVISORY)
      - stage_7_revival (HIGH)
      - schedule_prose_substitution (ADVISORY)
      - carve_out_construction (HIGH)
      - optimistic_probability (ADVISORY)

    Pattern 7 (tame_reviewer_drift) is NotImplemented; opt-in via direct call
    to _detect_tame_reviewer_drift if you want the warning surfaced.
    """

    findings: list[Finding] = []
    for detector in _DETECTORS:
        findings.extend(detector(text, file_path))
    return sorted(findings, key=lambda f: (f.line_number, f.pattern.value))


def scan_file(path: Path) -> list[Finding]:
    """Read a file and scan its contents."""

    text = path.read_text(encoding="utf-8")
    return scan(text, file_path=str(path))


# --- CLI -------------------------------------------------------------------


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
        high_count = len([f for f in all_findings if f.severity == Severity.HIGH])
        print(
            f"\n{high_count} HIGH-severity finding(s). Revise prose or override with "
            "logged reason (git commit --no-verify and document the reason in the "
            "commit message).",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
