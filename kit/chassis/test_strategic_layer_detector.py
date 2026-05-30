"""Unit tests for strategic_layer_detector (v0.2.0).

Mocks the LLM judge via the injected `judge` callable on scan(). Live
LLM calls are not exercised here — those live in the funkytown
experiment scripts and the v0.2.0 corpus regression suite (separate
artifact, not yet wired).
"""
from __future__ import annotations

import unittest
from kit.chassis.strategic_layer_detector import (
    PATTERN_DEFINITIONS, SEVERITY, StrategicPattern, scan,
    _find_line_of_excerpt, _StrategicPatternAdapter,
)
from kit.chassis.founder_romance_detector import Finding, Severity


def _fixed_judge(verdicts: dict):
    """Build a judge callable that returns pre-set verdicts per pattern."""
    def judge(pattern_id, text, file_path):
        v = verdicts.get(pattern_id, {"verdict": "no"})
        return {
            "verdict": v["verdict"],
            "excerpt": v.get("excerpt", ""),
            "rationale": v.get("rationale", ""),
            "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0,
        }
    return judge


SAMPLE_TIME_INVESTED = """We are doubling down on the enterprise compliance vertical, and this is not a pivot—it is a deliberate concentration. Over the past eighteen months, our team has lived inside the compliance workflows of mid-market financial institutions, mapping edge cases. That accumulated depth is precisely why this is the right market for us to own. Competitors entering today would face an eighteen-month knowledge deficit that cannot be shortcut.
"""

SAMPLE_PROXIMITY = """We've made a deliberate choice to concentrate our near-term engineering resources on the workflow layer rather than continuing to deepen the underlying data pipeline. The workflow layer is where the contract conversations are happening right now — three enterprise pilots are mid-negotiation. The infrastructure work sits two or three quarters away from any customer-visible impact, which means it sits two or three quarters away from anything we can show a partner.
"""

SAMPLE_CLEAN = """Our Q3 plan focuses on the mid-market segment based on a 14-day customer-discovery study (n=42) that showed 73% interest at our target price point. The enterprise segment had insufficient signal (n=8 conversations, mixed responses) to commit roadmap resources this quarter; we'll re-test enterprise demand in Q1 with a structured outbound experiment.
"""


class TestPatternDefinitions(unittest.TestCase):

    def test_all_three_patterns_have_definitions(self):
        self.assertEqual(set(PATTERN_DEFINITIONS),
                         {p.value for p in StrategicPattern})

    def test_definitions_non_empty(self):
        for pid, defn in PATTERN_DEFINITIONS.items():
            self.assertGreater(len(defn), 100,
                               f"{pid} definition too short")

    def test_all_advisory_at_ship(self):
        for pid in PATTERN_DEFINITIONS:
            # v0.2.1 (2026-05-30): all three patterns promoted ADVISORY ->
            # HIGH per Hans 6/6 precision audit on the full-baseline firings.
            self.assertEqual(SEVERITY[pid], Severity.HIGH,
                             f"{pid} not HIGH at v0.2.1 promotion")


class TestScanReturnsFindings(unittest.TestCase):

    def test_no_findings_when_judge_returns_no(self):
        judge = _fixed_judge({})
        findings = scan(SAMPLE_CLEAN, judge=judge)
        self.assertEqual(findings, [])

    def test_one_finding_when_one_pattern_fires(self):
        judge = _fixed_judge({
            "time_invested_justification": {
                "verdict": "yes",
                "excerpt": "That accumulated depth is precisely why this is the right market for us to own.",
                "rationale": "The eighteen-month investment is positioned as the warrant for the strategic claim.",
            },
        })
        findings = scan(SAMPLE_TIME_INVESTED, judge=judge,
                        file_path="test.md")
        self.assertEqual(len(findings), 1)
        f = findings[0]
        self.assertEqual(f.pattern.value, "time_invested_justification")
        self.assertEqual(f.severity, Severity.HIGH)
        self.assertIn("accumulated depth", f.excerpt)
        self.assertEqual(f.file_path, "test.md")

    def test_all_three_patterns_can_fire(self):
        judge = _fixed_judge({
            "time_invested_justification": {"verdict": "yes",
                "excerpt": "x", "rationale": "r1"},
            "proximity_to_gtm_framing": {"verdict": "yes",
                "excerpt": "y", "rationale": "r2"},
            "repackaged_clean_negative": {"verdict": "yes",
                "excerpt": "z", "rationale": "r3"},
        })
        findings = scan("test text", judge=judge)
        self.assertEqual(len(findings), 3)
        ids = {f.pattern.value for f in findings}
        self.assertEqual(ids, {p.value for p in StrategicPattern})

    def test_findings_are_high_severity_after_promotion(self):
        judge = _fixed_judge({
            "proximity_to_gtm_framing": {"verdict": "yes",
                "excerpt": "x", "rationale": "r"},
        })
        findings = scan(SAMPLE_PROXIMITY, judge=judge)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, Severity.HIGH)


class TestLineNumberLookup(unittest.TestCase):

    def test_finds_line_when_excerpt_present(self):
        text = "line one\nline two\nline three with the marker word\nline four"
        self.assertEqual(
            _find_line_of_excerpt(text, "the marker word"),
            3,
        )

    def test_returns_one_when_excerpt_not_found(self):
        text = "line one\nline two"
        self.assertEqual(_find_line_of_excerpt(text, "absent string"), 1)

    def test_returns_one_when_excerpt_empty(self):
        self.assertEqual(_find_line_of_excerpt("anything", ""), 1)


class TestFindingFormat(unittest.TestCase):

    def test_format_includes_severity_pattern_and_excerpt(self):
        judge = _fixed_judge({
            "repackaged_clean_negative": {
                "verdict": "yes",
                "excerpt": "Q3 channel analysis flagged enterprise direct as non-viable",
                "rationale": "Named kill signals reframed as optionality without refutation.",
            },
        })
        findings = scan(SAMPLE_PROXIMITY, judge=judge, file_path="strat.md")
        self.assertEqual(len(findings), 1)
        formatted = findings[0].format()
        self.assertIn("HIGH", formatted)
        self.assertIn("repackaged_clean_negative", formatted)
        self.assertIn("kill signals", formatted)
        self.assertIn("strat.md", formatted)


class TestStrategicPatternAdapter(unittest.TestCase):

    def test_value_attribute(self):
        a = _StrategicPatternAdapter("time_invested_justification")
        self.assertEqual(a.value, "time_invested_justification")

    def test_equality_with_string(self):
        a = _StrategicPatternAdapter("proximity_to_gtm_framing")
        self.assertEqual(a, "proximity_to_gtm_framing")

    def test_equality_with_other_adapter(self):
        a = _StrategicPatternAdapter("repackaged_clean_negative")
        b = _StrategicPatternAdapter("repackaged_clean_negative")
        self.assertEqual(a, b)

    def test_hashable(self):
        a = _StrategicPatternAdapter("time_invested_justification")
        self.assertEqual(hash(a), hash(a))


if __name__ == "__main__":
    unittest.main()
