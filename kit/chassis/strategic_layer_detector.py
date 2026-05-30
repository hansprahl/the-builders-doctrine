"""Strategic-Layer Observer-Bias Detector — v0.2.0 candidate.

Sibling module to `founder_romance_detector.py` (v0.1.1, regex-based).
This module is LLM-gate by construction: the three Exp 11b strategic-
layer patterns have no regex anchors and require a cross-family judge
for the bias call.

Spec: kit/chassis/STRATEGIC_LAYER_DETECTOR_SPEC.md
Empirical basis: kit/chassis/findings_strategic_layer_v1.md (Exp 11b,
                  2026-05-30)

Invocation (per spec):
    - On-demand CLI:   python -m kit.chassis.strategic_layer_detector <file>
    - Pre-commit hook: configured in .pre-commit-config.yaml on a
                       curated path list. The hook only runs when a
                       staged file is in the curated list.

Severity at v0.2.0:
    - All three patterns ship ADVISORY-only. HIGH-gate promotion is
      gated on the full baseline-scan results (Exp 11b open follow-up).
"""
from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

# Reuse the v0.1.1 Finding + Severity types unchanged (Hans decision
# 2026-05-30). Avoid circular imports by importing the symbols directly.
from kit.chassis.founder_romance_detector import Finding, Severity  # noqa: E402


# Strategic pattern identifiers, kept distinct from the v0.1.1 `Pattern`
# Enum so the two detectors can coexist without ID collision.
class StrategicPattern(str, Enum):
    TIME_INVESTED_JUSTIFICATION = "time_invested_justification"
    PROXIMITY_TO_GTM_FRAMING = "proximity_to_gtm_framing"
    REPACKAGED_CLEAN_NEGATIVE = "repackaged_clean_negative"


# Pattern definitions — verbatim from Exp 11b. Same string supplied to
# the LLM judge that returned 99.4% three-family agreement.
PATTERN_DEFINITIONS: dict[str, str] = {
    StrategicPattern.TIME_INVESTED_JUSTIFICATION.value: (
        "A strategic claim that the present course of action is correct "
        "BECAUSE a long time was already spent building, learning, or "
        "accumulating context for it. The duration itself is positioned as "
        "the warrant for the decision, with no intervening measurement of "
        "outcome quality, market evidence, or comparable evaluation against "
        "alternative uses of that time. Form: [time-invested clause] -> "
        "[strategic claim] adjacency, with no measurement bridge. Distinct "
        "from biographical 'founder-romance' (which uses life experience as "
        "warrant); this pattern uses recent project-time invested in THIS "
        "specific bet as warrant."
    ),
    StrategicPattern.PROXIMITY_TO_GTM_FRAMING.value: (
        "A strategic option is re-weighted upward — or a kept-vs-killed "
        "decision is settled — because the option is closer to revenue, "
        "closer to a launch milestone, closer to a paying customer, or "
        "closer to 'real validation,' with closeness itself stated as the "
        "warrant. The framing privileges the visibly-near option without a "
        "comparable risk-adjusted evaluation of the further-away option. "
        "Distinct from a legitimate sequencing argument that names the "
        "risk-adjusted return trade-off; this pattern asserts proximity-to-"
        "GTM as a self-justifying argument."
    ),
    StrategicPattern.REPACKAGED_CLEAN_NEGATIVE.value: (
        "A prior analysis (wargame, MDMP, due-diligence pass, customer "
        "research) returned a clean negative — viability score low, named "
        "kill signals, named financial loss or specific failure modes. The "
        "negative is then re-presented in a subsequent strategic discussion "
        "as 'Option N with strong dissent,' 'an optionality play to keep on "
        "the table,' 'a hedge worth retaining,' or 'a portfolio diversifier' "
        "without addressing or refuting the named kill signals. Form: clean-"
        "negative result adjacent to optionality / hedging / portfolio "
        "language, in a way that effectively reopens a decision the prior "
        "analysis closed."
    ),
}


# Severity table.
#
# v0.2.0 shipped ADVISORY-only. v0.2.1 (2026-05-30) promotes all three
# patterns to HIGH per Hans precision audit of the 6 baseline firings
# (6/6 TP, 100% precision per pattern, above the >=60% spec threshold).
# See findings_strategic_layer_v1.md "Hans precision audit" section.
SEVERITY: dict[str, Severity] = {
    StrategicPattern.TIME_INVESTED_JUSTIFICATION.value: Severity.HIGH,
    StrategicPattern.PROXIMITY_TO_GTM_FRAMING.value: Severity.HIGH,
    StrategicPattern.REPACKAGED_CLEAN_NEGATIVE.value: Severity.HIGH,
}


_JUDGE_SYSTEM_PROMPT = """You are a careful human reviewer auditing a candidate observer-bias pattern.

You are shown a paragraph from a strategic document (roadmap, pitch deck, board update, MDMP rationale, portfolio memo, wargame readout).

Your job: read the pattern definition + the paragraph, decide whether a careful human reviewer reading this paragraph in context would recognize the SAME observer-bias the pattern is named for.

The bar: would a thoughtful reader who knows about this specific bias catch it on careful read? Not "could you construct a reading where it's biased" — would they actually flag it.

If yes: output the SHORTEST contiguous excerpt (one or two sentences) that best exhibits the pattern, and a one-sentence rationale.
If no: output verdict "no" with brief reason.

Output JSON only, no preamble:
{"verdict": "yes" | "no", "excerpt": "<short excerpt or empty>", "rationale": "<one sentence>"}"""


def _judge_user_prompt(pattern_id: str, document_text: str,
                        file_path: Optional[str]) -> str:
    definition = PATTERN_DEFINITIONS[pattern_id]
    path_line = f"File path: {file_path}\n\n" if file_path else ""
    return (
        f"Pattern under review: `{pattern_id}`\n\n"
        f"Definition:\n{definition}\n\n"
        f"{path_line}"
        f"Document text:\n{document_text}\n\n"
        "Read the entire document. Does any passage genuinely exhibit "
        "the observer-bias pattern named above?\n\n"
        "Output JSON only:\n"
        "{\"verdict\": \"yes\" | \"no\", \"excerpt\": \"<short excerpt>\", "
        "\"rationale\": \"<one sentence>\"}"
    )


def _find_line_of_excerpt(text: str, excerpt: str) -> int:
    """Return 1-indexed line where the excerpt's first ~40 chars appear,
    or 1 if not found."""
    if not excerpt:
        return 1
    needle = excerpt.strip()[:40]
    if not needle:
        return 1
    idx = text.find(needle)
    if idx == -1:
        return 1
    return text.count("\n", 0, idx) + 1


def _build_judge_client(model: str):
    """Build the LLM judge client. Defaults to Grok-4 via xAI; the model
    name is configurable for future cross-family expansion.

    Returns a callable `judge(pattern_id, text, file_path) -> dict` with
    keys verdict, excerpt, rationale, cost_usd.
    """
    if not model.startswith("grok"):
        raise NotImplementedError(
            f"strategic_layer_detector only supports Grok models in "
            f"v0.2.0. Requested model={model}. Cross-family expansion "
            f"is on the v0.3 roadmap."
        )

    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "XAI_API_KEY env var must be set to invoke "
            "strategic_layer_detector. See .env in the doctrine repo or "
            "the per-product .env."
        )

    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError(
            "openai SDK required (`pip install openai`)."
        ) from e

    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

    # Grok-4 pricing per 1M tokens (May 2026 confirmed).
    in_per_m, out_per_m = 3.0, 15.0

    def _judge(pattern_id: str, text: str, file_path: Optional[str]) -> dict:
        user = _judge_user_prompt(pattern_id, text, file_path)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _JUDGE_SYSTEM_PROMPT},
                {"role": "user", "content": user},
            ],
            temperature=0.1,
            max_tokens=400,
        )
        raw = (resp.choices[0].message.content or "").strip()
        verdict, excerpt, rationale = None, "", ""
        try:
            parsed = json.loads(raw)
            verdict = parsed.get("verdict")
            excerpt = (parsed.get("excerpt") or "").strip()
            rationale = (parsed.get("rationale") or "").strip()
        except json.JSONDecodeError:
            lower = raw.lower()
            if '"yes"' in lower or lower.startswith("yes"):
                verdict = "yes"
            elif '"no"' in lower or lower.startswith("no"):
                verdict = "no"
            rationale = raw[:400]
        in_t = resp.usage.prompt_tokens
        out_t = resp.usage.completion_tokens
        cost = in_t / 1_000_000 * in_per_m + out_t / 1_000_000 * out_per_m
        return {
            "verdict": verdict, "excerpt": excerpt, "rationale": rationale,
            "input_tokens": in_t, "output_tokens": out_t,
            "cost_usd": round(cost, 6),
        }

    return _judge


# --- Public API ----------------------------------------------------------


def scan(
    text: str,
    *,
    file_path: Optional[str] = None,
    model: str = "grok-4",
    judge: Optional[callable] = None,
) -> list[Finding]:
    """Scan strategic prose for the three Exp 11b patterns.

    One LLM judge call per pattern. Returns Finding objects only for
    patterns where the judge returned verdict="yes."

    Args:
        text: the strategic-prose text to scan.
        file_path: optional file path (annotates findings, also passed
            to the judge as a context hint).
        model: LLM judge model name. v0.2.0 supports grok-* only.
        judge: optional injected callable for testing. Signature:
            judge(pattern_id: str, text: str, file_path: Optional[str])
                  -> {"verdict", "excerpt", "rationale", ...}
            Bypasses the live LLM client.

    Returns:
        list[Finding] sorted by pattern_id, all severity ADVISORY at v0.2.0.

    Cost: ~$0.06-0.10 per file for typical doctrine-size .md (in
    whole-doc mode). The CLI / pre-commit hook will only invoke `scan`
    on the curated path list per spec.
    """
    if judge is None:
        judge = _build_judge_client(model)

    findings: list[Finding] = []
    for pattern_id in PATTERN_DEFINITIONS:
        result = judge(pattern_id, text, file_path)
        if result.get("verdict") != "yes":
            continue
        line_number = _find_line_of_excerpt(text, result.get("excerpt", ""))
        findings.append(
            Finding(
                # NOTE: we annotate with a synthetic Pattern-like adapter.
                # Finding.pattern is typed `Pattern` (v0.1.1 Enum); we use
                # a thin wrapper so the .format() output reads cleanly.
                pattern=_StrategicPatternAdapter(pattern_id),
                severity=SEVERITY[pattern_id],
                excerpt=result.get("excerpt", "").strip()[:500],
                line_number=line_number,
                rationale=result.get("rationale", "").strip(),
                file_path=file_path,
                sub_pattern=None,
            )
        )
    return sorted(findings, key=lambda f: f.pattern.value)


class _StrategicPatternAdapter:
    """Thin wrapper so Finding.pattern.value yields the strategic
    pattern id even though Finding.pattern is typed as `Pattern`
    (v0.1.1 Enum). Keeps the Finding dataclass unchanged per Hans
    decision 2026-05-30.
    """
    __slots__ = ("value",)

    def __init__(self, value: str) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"StrategicPattern.{self.value.upper()}"

    def __eq__(self, other) -> bool:
        if isinstance(other, _StrategicPatternAdapter):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(("strategic", self.value))


def scan_file(path: Path, model: str = "grok-4") -> list[Finding]:
    """Read a file and scan its contents."""
    text = path.read_text(encoding="utf-8")
    return scan(text, file_path=str(path), model=model)


# --- CLI -----------------------------------------------------------------


def _main(argv: list[str]) -> int:
    """CLI entry point.

    v0.2.1: HIGH-gate active for all three patterns (promoted from
    ADVISORY 2026-05-30 per Hans 6/6 precision audit). Exits 1 if any
    HIGH findings present; override via the standard pattern:

        git commit --no-verify -m "<message>

        OVERRIDE: strategic_layer_detector flagged <pattern> in <file>.
        Reviewed; <reason>. Logged."

    Soft-fail behavior: if the judge client cannot be built (no
    XAI_API_KEY, network unreachable, openai SDK missing), the affected
    file is skipped with a warning and the commit is NOT blocked.
    """
    if len(argv) < 2:
        print(
            "usage: python -m kit.chassis.strategic_layer_detector "
            "<file> [<file>...]\n"
            "       v0.2.1: LLM gate (Grok-4). Exits 1 on HIGH findings.",
            file=sys.stderr,
        )
        return 2

    files = []
    for arg in argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f"warning: skipping non-file path {arg}", file=sys.stderr)
            continue
        files.append(path)

    if not files:
        return 0

    all_findings: list[Finding] = []
    skipped_files: list[tuple[Path, str]] = []
    for path in files:
        try:
            all_findings.extend(scan_file(path))
        except Exception as e:
            skipped_files.append((path, f"{type(e).__name__}: {e}"))
            continue

    for path, reason in skipped_files:
        print(
            f"warning: strategic_layer_detector skipped {path}: {reason}",
            file=sys.stderr,
        )

    for finding in all_findings:
        print(finding.format(), file=sys.stderr)

    has_high = any(f.severity == Severity.HIGH for f in all_findings)
    if has_high:
        high_count = sum(1 for f in all_findings
                         if f.severity == Severity.HIGH)
        print(
            f"\n{high_count} HIGH-severity strategic-layer finding(s). "
            f"Revise prose or override with logged reason (git commit "
            f"--no-verify and document the reason in the commit message).",
            file=sys.stderr,
        )
        return 1

    if all_findings:
        print(
            f"\n{len(all_findings)} ADVISORY strategic-layer finding(s).",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
