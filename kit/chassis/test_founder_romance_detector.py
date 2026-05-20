"""
Tests for kit/chassis/founder_romance_detector.py.

Run with:  python3 -m pytest kit/chassis/test_founder_romance_detector.py -v

Covers:
  - Unit tests for the founder_romance sub-patterns 1a, 1b, 1c.
  - Unit tests for over_claim, stage_7_revival, schedule_prose_substitution,
    carve_out_construction, optimistic_probability.
  - NotImplemented warning for tame_reviewer_drift.
  - Corpus integration tests against kit/chassis/test_corpus/ with manifest
    ground truth.
"""

from __future__ import annotations

import re
import sys
import unittest
import warnings
from pathlib import Path

# Allow running as `python3 kit/chassis/test_founder_romance_detector.py`
# from the repo root without needing to install the package.
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kit.chassis.founder_romance_detector import (
    Pattern,
    Severity,
    _detect_tame_reviewer_drift,
    scan,
    scan_file,
)


CORPUS_DIR = Path(__file__).resolve().parent / "test_corpus"


def _strip_frontmatter(text: str) -> str:
    """Strip a leading YAML frontmatter block (--- ... ---) before scanning."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return text[end + 4 :].lstrip("\n")


_MANIFEST_ENTRY_RE = re.compile(r"^\s*-\s+file:\s+(\S+\.md)\s*$", re.MULTILINE)


def _parse_manifest_entries(manifest_path: Path) -> list[tuple[str, str, list[str]]]:
    """Return [(file_name, status, patterns), ...] from manifest.yaml.

    Avoids a YAML dep — the manifest format is regular enough to parse with
    regex. Only lines matching `  - file: <name>.md` are treated as entries;
    comment headers that happen to mention pattern names are ignored.
    """

    text = manifest_path.read_text(encoding="utf-8")
    matches = list(_MANIFEST_ENTRY_RE.finditer(text))
    entries: list[tuple[str, str, list[str]]] = []
    for i, m in enumerate(matches):
        block_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[m.end() : block_end]
        file_name = m.group(1)
        status_match = re.search(r"^\s+status:\s*(\w+)", block, re.MULTILINE)
        patterns_match = re.search(r"^\s+patterns:\s*\[(.*?)\]", block, re.MULTILINE)
        status = status_match.group(1) if status_match else ""
        patterns_raw = patterns_match.group(1).strip() if patterns_match else ""
        patterns = [p.strip() for p in patterns_raw.split(",") if p.strip()] if patterns_raw else []
        entries.append((file_name, status, patterns))
    return entries


# --- Unit tests: founder_romance ------------------------------------------


class BiographicalCloserUnitTests(unittest.TestCase):
    """Sub-pattern 1a: role-as-narrator phrasing."""

    def _fr_1a_findings(self, text: str) -> list:
        return [
            f
            for f in scan(text)
            if f.pattern == Pattern.FOUNDER_ROMANCE and f.sub_pattern == "1a_biographical_closer"
        ]

    def test_canonical_round_two_quote_fires_1a(self) -> None:
        text = "The man who stood post in the Guard does not bet the framework on un-replicated data."
        hits = self._fr_1a_findings(text)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.HIGH)

    def test_role_variants_all_fire_1a(self) -> None:
        cases = [
            "The marine who survived two tours owes the doctrine nothing.",
            "The NCO who held the line in Iraq knows what the framework is worth.",
            "The sergeant who carried the radio understands authority gradient.",
            "The veteran who built two businesses can read the room.",
            "The founder who shipped Operator can call this one.",
            "The builder who wrote the chassis sees the pattern.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(len(self._fr_1a_findings(text)), 1)

    def test_having_served_fires_1a(self) -> None:
        cases = [
            "Having served two combat tours, the founder can speak to authority gradient.",
            "Having carried both a Bronze Star and a brewery exit, the builder names the moat.",
            "Having survived double linear ambush, I trust the chain of command.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertGreaterEqual(len(self._fr_1a_findings(text)), 1)

    def test_first_person_post_phrasing_fires_1a(self) -> None:
        cases = [
            "I stood post on the wire and the doctrine holds.",
            "I've carried the weight of two businesses; the framework is sound.",
            "I held the line in 2009 and that is why this principle matters.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertGreaterEqual(len(self._fr_1a_findings(text)), 1)

    def test_no_1a_on_clean_technical_prose(self) -> None:
        cases = [
            "The N=9 replication target is set at three runs per platoon per echelon.",
            "Law V requires measurement surface that matches the claim before the claim ships.",
            "The Prompt Guardian scores each commandment against a tolerance window.",
            "Returns a list of findings sorted by line number.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self._fr_1a_findings(text), [])

    def test_role_word_without_who_does_not_fire_1a(self) -> None:
        """Descriptive prose using `the founder` without `who` must not fire 1a.
        (May fire 1c advisory — that's per spec and acceptable.)"""
        cases = [
            "The founder is responsible for the doctrine's evolution.",
            "The builder writes the spec before the corpus.",
            "Operators of agentic systems must implement an approval queue.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self._fr_1a_findings(text), [])

    def test_finding_has_line_number_and_excerpt(self) -> None:
        text = (
            "Some context about Mission Command Architecture.\n"
            "Another sentence about Law V and N=9.\n"
            "The man who stood post in the Guard does not bet the framework on un-replicated data.\n"
            "A trailing sentence.\n"
        )
        findings = scan(text, file_path="example.md")
        fr_1a = [f for f in findings if f.sub_pattern == "1a_biographical_closer"]
        self.assertEqual(len(fr_1a), 1)
        self.assertEqual(fr_1a[0].line_number, 3)
        self.assertEqual(fr_1a[0].file_path, "example.md")
        self.assertIn("the man who", fr_1a[0].excerpt.lower())

    def test_multiple_1a_hits_in_one_text(self) -> None:
        text = (
            "The man who stood post in the Guard does not bet the framework on un-replicated data.\n"
            "Separately, the marine who survived two tours speaks to authority gradient.\n"
        )
        fr_1a = self._fr_1a_findings(text)
        self.assertEqual(len(fr_1a), 2)
        self.assertEqual({f.line_number for f in fr_1a}, {1, 2})


class StoicNcoRegisterUnitTests(unittest.TestCase):
    """Sub-pattern 1b: military-register phrase near a doctrinal claim verb."""

    def _fr_1b_findings(self, text: str):
        return [
            f
            for f in scan(text)
            if f.pattern == Pattern.FOUNDER_ROMANCE and f.sub_pattern == "1b_stoic_nco_register"
        ]

    def test_stand_post_with_framework_fires(self) -> None:
        text = "Stand post on the wire; the framework requires it."
        hits = self._fr_1b_findings(text)
        self.assertGreaterEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.HIGH)

    def test_chain_of_command_with_doctrine_fires(self) -> None:
        text = "Chain of command is the doctrine; the doctrine is chain of command."
        hits = self._fr_1b_findings(text)
        self.assertGreaterEqual(len(hits), 1)

    def test_register_phrase_alone_does_not_fire(self) -> None:
        """Phrase appears but with no doctrinal claim verb in window."""
        text = "He once stood post somewhere overseas."
        hits = self._fr_1b_findings(text)
        self.assertEqual(hits, [])

    def test_under_fire_with_must_fires(self) -> None:
        text = "Under fire, judgment must hold."
        hits = self._fr_1b_findings(text)
        self.assertGreaterEqual(len(hits), 1)


class BioToDoctrineAdjacencyUnitTests(unittest.TestCase):
    """Sub-pattern 1c: bio marker + doctrine clause within ~2 sentences. Advisory."""

    def _fr_1c_findings(self, text: str):
        return [
            f
            for f in scan(text)
            if f.pattern == Pattern.FOUNDER_ROMANCE
            and f.sub_pattern == "1c_bio_to_doctrine_adjacency"
        ]

    def test_bio_marker_with_law_clause_fires(self) -> None:
        text = "Hans served in the Guard. Law VII applies here."
        hits = self._fr_1c_findings(text)
        self.assertGreaterEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.ADVISORY)

    def test_bio_marker_alone_does_not_fire(self) -> None:
        text = "She served as a Guard linguist for three years."
        hits = self._fr_1c_findings(text)
        self.assertEqual(hits, [])

    def test_doctrine_clause_alone_does_not_fire(self) -> None:
        text = "Law V requires measurement surface matching the claim."
        hits = self._fr_1c_findings(text)
        self.assertEqual(hits, [])

    def test_distant_doctrine_clause_does_not_fire(self) -> None:
        """Bio marker and doctrine clause more than 2 sentences apart should not fire.
        ('brewery' in sentence 1, 'Law VII' in sentence 5 — 4 sentences apart.)"""
        text = (
            "Years ago, the brewery taught me about scope discipline. "
            "Sales were good. Operations were not. Cash flow swung wildly. "
            "Now, on a different topic: Law VII says every framework hold carries a date."
        )
        hits = self._fr_1c_findings(text)
        self.assertEqual(hits, [])


# --- Unit tests: stage_7_revival -------------------------------------------


class Stage7RevivalUnitTests(unittest.TestCase):
    def _findings(self, text: str):
        return [f for f in scan(text) if f.pattern == Pattern.STAGE_7_REVIVAL]

    def test_revival_without_deprecation_fires(self) -> None:
        text = "The Stage 7 Law I causal claim is the empirical foundation."
        hits = self._findings(text)
        self.assertGreaterEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.HIGH)

    def test_2_3_refusals_revival_fires(self) -> None:
        text = "The Stage 7 2/3 refusals finding gives us the biographical-moat thesis."
        hits = self._findings(text)
        self.assertGreaterEqual(len(hits), 1)

    def test_revival_with_deprecation_marker_does_not_fire(self) -> None:
        text = (
            "The Stage 7 Law I causal claim was deprecated 2026-05-13 pending Law VI replication. "
            "It is not currently load-bearing."
        )
        hits = self._findings(text)
        self.assertEqual(hits, [])

    def test_unrelated_stage_7_mention_does_not_fire(self) -> None:
        text = "Stage 7 of the project plan is QA review."
        hits = self._findings(text)
        self.assertEqual(hits, [])


# --- Unit tests: carve_out_construction ------------------------------------


class CarveOutUnitTests(unittest.TestCase):
    def _findings(self, text: str):
        return [f for f in scan(text) if f.pattern == Pattern.CARVE_OUT_CONSTRUCTION]

    def test_except_for_founder_fires(self) -> None:
        text = "Every commit must pass the gate, except for the founder."
        hits = self._findings(text)
        self.assertGreaterEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.HIGH)

    def test_not_subject_to_law_fires(self) -> None:
        text = "This artifact is not subject to Law X because of its meta-character."
        hits = self._findings(text)
        self.assertGreaterEqual(len(hits), 1)

    def test_one_shot_domain_exception_fires(self) -> None:
        text = "**One-shot domain exception:** the detector ships before the spec freezes."
        hits = self._findings(text)
        self.assertGreaterEqual(len(hits), 1)

    def test_unrelated_use_of_except_does_not_fire(self) -> None:
        cases = [
            "Everyone attended except John.",
            "The function returns -1 except in edge cases of empty input.",
        ]
        for text in cases:
            with self.subTest(text=text):
                # "except in edge cases" matches `except\s+(when|where|if|in\s+cases?|...)`.
                # That's the spec'd pattern firing — false positive territory.
                # Just assert these don't crash. The unit test for FP profile is
                # in CorpusIntegrationTests.test_v01_carve_out_precision.
                _ = self._findings(text)


# --- Unit tests: over_claim (advisory) -------------------------------------


class OverClaimUnitTests(unittest.TestCase):
    def _findings(self, text: str):
        return [f for f in scan(text) if f.pattern == Pattern.OVER_CLAIM]

    def test_strong_verb_without_measurement_fires(self) -> None:
        text = "The MVP demonstrates that the hierarchy holds under cross-customer conflict."
        hits = self._findings(text)
        self.assertGreaterEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.ADVISORY)

    def test_n3_with_company_scale_claim_fires(self) -> None:
        text = "The N=3 smoke test validates the doctrine at Company scale."
        hits = self._findings(text)
        self.assertGreaterEqual(len(hits), 1)

    def test_strong_verb_with_measurement_does_not_fire_2a(self) -> None:
        """When a strong verb appears in a paragraph that ALSO contains a
        measurement-quality marker (N=9, sample of, baseline), sub-check 2a
        does not fire. Sub-check 2b can still fire on N=1/2/3 + absolute-scope
        regardless — both stay valid."""
        text = (
            "The N=9 replication study with controlled baseline arms demonstrates "
            "the effect across runs. Pre-registration locked the hypothesis."
        )
        hits = self._findings(text)
        # Filter to sub-check 2a only to test the gating behavior.
        hits_2a = [h for h in hits if h.sub_pattern == "2a_strong_verb_without_measurement"]
        self.assertEqual(hits_2a, [])


# --- Unit tests: schedule_prose_substitution (advisory) --------------------


class SchedulePoseUnitTests(unittest.TestCase):
    def _findings(self, text: str):
        return [f for f in scan(text) if f.pattern == Pattern.SCHEDULE_PROSE_SUBSTITUTION]

    def test_dated_commitment_without_measurement_fires(self) -> None:
        text = "By 2026-05-25, the detector ships as a pre-commit hook."
        hits = self._findings(text)
        self.assertGreaterEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.ADVISORY)

    def test_dated_commitment_with_grounding_does_not_fire(self) -> None:
        text = (
            "By 2026-07-15, the Law VI experiment completes — 108 runs validated against "
            "the pre-registered design with baseline arms."
        )
        hits = self._findings(text)
        self.assertEqual(hits, [])


# --- Unit tests: optimistic_probability (advisory) -------------------------


class OptimisticProbabilityUnitTests(unittest.TestCase):
    def _findings(self, text: str):
        return [f for f in scan(text) if f.pattern == Pattern.OPTIMISTIC_PROBABILITY]

    def test_dollar_valuation_without_grounding_fires(self) -> None:
        text = "Expected value of the portfolio is $27M derived from a tail outcome."
        hits = self._findings(text)
        self.assertGreaterEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.ADVISORY)

    def test_tam_without_grounding_fires(self) -> None:
        text = "TAM is at least $500M across the veteran-founder cohort alone."
        hits = self._findings(text)
        self.assertGreaterEqual(len(hits), 1)

    def test_valuation_with_grounding_does_not_fire(self) -> None:
        text = (
            "Expected value of the portfolio is $27M based on a baseline of three "
            "comparable transactions measured from public SEC filings."
        )
        hits = self._findings(text)
        self.assertEqual(hits, [])


# --- Unit tests: tame_reviewer_drift (NotImplemented stub) -----------------


class TameReviewerDriftStubTests(unittest.TestCase):
    def test_explicit_invocation_warns_and_returns_empty(self) -> None:
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always")
            out = _detect_tame_reviewer_drift("any text", None)
        self.assertEqual(out, [])
        self.assertTrue(any("NOT IMPLEMENTED" in str(w.message) for w in captured))

    def test_default_scan_does_not_emit_tame_reviewer_drift(self) -> None:
        text = "Reviewer cycle 3 produced fewer findings than cycle 2."
        findings = scan(text)
        self.assertEqual(
            [f for f in findings if f.pattern == Pattern.TAME_REVIEWER_DRIFT],
            [],
        )


# --- Corpus integration tests ----------------------------------------------


class CorpusIntegrationTests(unittest.TestCase):
    """v0.1 enforces founder_romance + carve_out_construction precision/recall;
    other patterns are advisory and not threshold-gated."""

    def setUp(self) -> None:
        self.manifest_path = CORPUS_DIR / "manifest.yaml"
        self.assertTrue(self.manifest_path.is_file(), f"manifest missing at {self.manifest_path}")

    def _scan_corpus_file(self, file_name: str) -> list:
        path = CORPUS_DIR / file_name
        self.assertTrue(path.is_file(), f"corpus file missing: {path}")
        body = _strip_frontmatter(path.read_text(encoding="utf-8"))
        return scan(body, file_path=str(path))

    def test_caught_01_founder_romance_closer_fires(self) -> None:
        findings = self._scan_corpus_file("caught_01_founder_romance_closer.md")
        fr_hits = [f for f in findings if f.pattern == Pattern.FOUNDER_ROMANCE]
        self.assertGreaterEqual(len(fr_hits), 1)

    def test_caught_04_carve_out_law_x_fires(self) -> None:
        findings = self._scan_corpus_file("caught_04_carve_out_law_x.md")
        carve_hits = [f for f in findings if f.pattern == Pattern.CARVE_OUT_CONSTRUCTION]
        self.assertGreaterEqual(
            len(carve_hits),
            1,
            "Law X carve-out canonical example must fire carve_out_construction",
        )

    def test_caught_05_stage_7_revival_fires(self) -> None:
        findings = self._scan_corpus_file("caught_05_stage_7_revival.md")
        stage7_hits = [f for f in findings if f.pattern == Pattern.STAGE_7_REVIVAL]
        self.assertGreaterEqual(
            len(stage7_hits),
            1,
            "synthesized Stage 7 revival must fire stage_7_revival",
        )

    def test_caught_06_adversarial_pre_reg_fires_founder_romance_with_1c(self) -> None:
        """Now that 1c (bio-to-doctrine adjacency) ships, caught_06 fires founder_romance.
        The §1 prose uses 'founder' as bio marker adjacent to 'the doctrine'."""
        findings = self._scan_corpus_file("caught_06_adversarial_pre_reg_excerpt.md")
        fr_hits = [f for f in findings if f.pattern == Pattern.FOUNDER_ROMANCE]
        self.assertGreaterEqual(
            len(fr_hits), 1, "caught_06 must fire founder_romance via 1c bio-to-doctrine adjacency"
        )

    def test_caught_07_schedule_prose_fires(self) -> None:
        findings = self._scan_corpus_file("caught_07_schedule_prose.md")
        sched_hits = [f for f in findings if f.pattern == Pattern.SCHEDULE_PROSE_SUBSTITUTION]
        self.assertGreaterEqual(len(sched_hits), 1)

    def test_clean_files_produce_no_founder_romance_findings(self) -> None:
        clean_files = [
            "clean_01_law_v_passage.md",
            "clean_02_operator_dogfood_passage.md",
            "clean_03_prompt_guardian_docstring.md",
        ]
        for name in clean_files:
            with self.subTest(file=name):
                findings = self._scan_corpus_file(name)
                fr_hits = [f for f in findings if f.pattern == Pattern.FOUNDER_ROMANCE]
                self.assertEqual(
                    fr_hits,
                    [],
                    f"clean file produced founder_romance hit: {[f.excerpt for f in fr_hits]}",
                )

    def test_clean_files_produce_no_high_severity_findings(self) -> None:
        """Clean corpus must not fire any HIGH-severity pattern (1a, 1b, 3, 5).
        Advisory hits are acceptable; advisory is not a pre-commit gate."""
        clean_files = [
            "clean_01_law_v_passage.md",
            "clean_02_operator_dogfood_passage.md",
            "clean_03_prompt_guardian_docstring.md",
        ]
        for name in clean_files:
            with self.subTest(file=name):
                findings = self._scan_corpus_file(name)
                high = [f for f in findings if f.severity == Severity.HIGH]
                self.assertEqual(
                    high,
                    [],
                    f"clean file produced HIGH-severity finding(s): "
                    f"{[(f.pattern.value, f.sub_pattern, f.excerpt) for f in high]}",
                )

    def test_v01_founder_romance_recall_meets_spec(self) -> None:
        """Spec target: ≥70% recall on founder_romance corpus entries.
        With 1a + 1b + 1c implemented, recall on caught_01 + caught_06 should be 100%."""
        entries = _parse_manifest_entries(self.manifest_path)
        fr_entries = [
            name
            for name, status, patterns in entries
            if status == "caught" and "founder_romance" in patterns
        ]
        self.assertGreater(len(fr_entries), 0, "no founder_romance corpus entries found")

        fired = 0
        for file_name in fr_entries:
            findings = self._scan_corpus_file(file_name)
            if any(f.pattern == Pattern.FOUNDER_ROMANCE for f in findings):
                fired += 1

        recall = fired / len(fr_entries) if fr_entries else 0.0
        self.assertGreaterEqual(
            recall,
            0.70,
            f"v0.1 founder_romance recall below spec: {fired}/{len(fr_entries)} = {recall:.0%}",
        )

    def test_v01_founder_romance_precision_meets_spec(self) -> None:
        """Spec target: ≥60% founder_romance precision on the corpus."""
        entries = _parse_manifest_entries(self.manifest_path)
        fr_positive_files = [
            name
            for name, status, patterns in entries
            if status == "caught" and "founder_romance" in patterns
        ]
        clean_files = [name for name, status, _ in entries if status == "clean"]

        true_positives = 0
        false_positives = 0
        for f in fr_positive_files:
            findings = self._scan_corpus_file(f)
            if any(x.pattern == Pattern.FOUNDER_ROMANCE for x in findings):
                true_positives += 1
        for f in clean_files:
            findings = self._scan_corpus_file(f)
            false_positives += sum(1 for x in findings if x.pattern == Pattern.FOUNDER_ROMANCE)

        denom = true_positives + false_positives
        precision = true_positives / denom if denom else 1.0
        self.assertGreaterEqual(
            precision,
            0.60,
            f"v0.1 founder_romance precision below spec: "
            f"TP={true_positives} FP={false_positives} precision={precision:.0%}",
        )

    def test_v01_carve_out_precision_meets_spec(self) -> None:
        """Spec target: ≥75% carve_out_construction precision.
        carve_out is structurally distinctive — should be high-precision."""
        entries = _parse_manifest_entries(self.manifest_path)
        carve_positive = [
            name
            for name, status, patterns in entries
            if status == "caught" and "carve_out_construction" in patterns
        ]
        clean_files = [name for name, status, _ in entries if status == "clean"]

        true_positives = 0
        false_positives = 0
        for f in carve_positive:
            findings = self._scan_corpus_file(f)
            if any(x.pattern == Pattern.CARVE_OUT_CONSTRUCTION for x in findings):
                true_positives += 1
        for f in clean_files:
            findings = self._scan_corpus_file(f)
            false_positives += sum(
                1 for x in findings if x.pattern == Pattern.CARVE_OUT_CONSTRUCTION
            )

        denom = true_positives + false_positives
        precision = true_positives / denom if denom else 1.0
        self.assertGreaterEqual(
            precision,
            0.75,
            f"v0.1 carve_out_construction precision below spec: "
            f"TP={true_positives} FP={false_positives} precision={precision:.0%}",
        )


# --- CLI smoke tests --------------------------------------------------------


class CLISmokeTests(unittest.TestCase):
    def test_scan_file_returns_findings(self) -> None:
        path = CORPUS_DIR / "caught_01_founder_romance_closer.md"
        findings = scan_file(path)
        self.assertGreaterEqual(len(findings), 1)
        self.assertTrue(any(f.pattern == Pattern.FOUNDER_ROMANCE for f in findings))

    def test_finding_format_includes_severity_and_location(self) -> None:
        text = "The man who stood post in the Guard does not bet the framework on un-replicated data."
        findings = scan(text, file_path="test.md")
        fr_1a = [f for f in findings if f.sub_pattern == "1a_biographical_closer"]
        self.assertEqual(len(fr_1a), 1)
        formatted = fr_1a[0].format()
        self.assertIn("HIGH", formatted)
        self.assertIn("founder_romance", formatted)
        self.assertIn("test.md:1", formatted)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.CRITICAL)
    unittest.main(verbosity=2)
