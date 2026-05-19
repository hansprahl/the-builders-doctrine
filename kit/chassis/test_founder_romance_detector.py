"""
Tests for kit/chassis/founder_romance_detector.py.

Run with:  python3 kit/chassis/test_founder_romance_detector.py

Covers:
  - Unit tests for the biographical-closer regexes (positive + negative).
  - Corpus integration tests against kit/chassis/test_corpus/.
    Manifest in test_corpus/manifest.yaml declares ground truth.
    For v0.1: founder_romance is enforced; other patterns are advisory.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

# Allow running as `python3 kit/chassis/test_founder_romance_detector.py`
# from the repo root without needing to install the package.
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kit.chassis.founder_romance_detector import (
    Pattern,
    Severity,
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


# --- Unit tests ---


class BiographicalCloserUnitTests(unittest.TestCase):
    """Sub-pattern 1a: role-as-narrator phrasing."""

    def test_canonical_round_two_quote_fires(self) -> None:
        text = "The man who stood post in the Guard does not bet the framework on un-replicated data."
        findings = scan(text)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].pattern, Pattern.FOUNDER_ROMANCE)
        self.assertEqual(findings[0].severity, Severity.HIGH)
        self.assertEqual(findings[0].sub_pattern, "1a_biographical_closer")

    def test_role_variants_all_fire(self) -> None:
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
                findings = scan(text)
                self.assertEqual(len(findings), 1, f"expected one hit on: {text}")
                self.assertEqual(findings[0].pattern, Pattern.FOUNDER_ROMANCE)

    def test_having_served_fires(self) -> None:
        cases = [
            "Having served two combat tours, the founder can speak to authority gradient.",
            "Having carried both a Bronze Star and a brewery exit, the builder names the moat.",
            "Having survived double linear ambush, I trust the chain of command.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(len(scan(text)), 1)

    def test_first_person_post_phrasing_fires(self) -> None:
        cases = [
            "I stood post on the wire and the doctrine holds.",
            "I've carried the weight of two businesses; the framework is sound.",
            "I held the line in 2009 and that is why this principle matters.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(len(scan(text)), 1)

    def test_clean_prose_does_not_fire(self) -> None:
        cases = [
            "The N=9 replication target is set at three runs per platoon per echelon.",
            "Law V requires measurement surface that matches the claim before the claim ships.",
            "The Prompt Guardian scores each commandment against a tolerance window.",
            "Returns a list of findings sorted by line number.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(scan(text), [], f"unexpected hit on clean prose: {text}")

    def test_role_word_in_descriptive_prose_does_not_fire(self) -> None:
        """`the founder` alone without `who` should not fire."""
        cases = [
            "The founder is responsible for the doctrine's evolution.",
            "The builder writes the spec before the corpus.",
            "Veterans are one of three target cohorts in the TAM analysis.",
            "Operators of agentic systems must implement an approval queue.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(scan(text), [], f"unexpected hit on: {text}")

    def test_finding_has_line_number_and_excerpt(self) -> None:
        text = (
            "Some context about Mission Command Architecture.\n"
            "Another sentence about Law V and N=9.\n"
            "The man who stood post in the Guard does not bet the framework on un-replicated data.\n"
            "A trailing sentence.\n"
        )
        findings = scan(text, file_path="example.md")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line_number, 3)
        self.assertEqual(findings[0].file_path, "example.md")
        self.assertIn("the man who", findings[0].excerpt.lower())

    def test_multiple_hits_in_one_text(self) -> None:
        text = (
            "The man who stood post in the Guard does not bet the framework on un-replicated data.\n"
            "Separately, the marine who survived two tours speaks to authority gradient.\n"
        )
        findings = scan(text)
        self.assertEqual(len(findings), 2)
        self.assertEqual({f.line_number for f in findings}, {1, 2})


# --- Corpus integration tests ---


class CorpusIntegrationTests(unittest.TestCase):
    """v0.1 enforces founder_romance on caught files; clean files must produce no founder_romance findings."""

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
        founder_romance_hits = [f for f in findings if f.pattern == Pattern.FOUNDER_ROMANCE]
        self.assertGreaterEqual(
            len(founder_romance_hits),
            1,
            "canonical round-2 founder-romance closer must fire on founder_romance",
        )

    def test_caught_06_adversarial_pre_reg_does_not_fire_v01(self) -> None:
        """The §1 background passage exhibits founder_romance/over_claim per the manifest,
        but the specific prose uses 'founder' as a noun ("the founder building the chassis...")
        rather than role-as-narrator ("the founder who..."). v0.1's biographical-closer
        sub-pattern is intentionally narrow and is expected to miss this case. This test
        documents the v0.1 known false-negative — when sub-pattern 1c (bio-to-doctrine
        adjacency) ships, this test inverts to assertGreaterEqual.
        """
        findings = self._scan_corpus_file("caught_06_adversarial_pre_reg_excerpt.md")
        founder_romance_hits = [f for f in findings if f.pattern == Pattern.FOUNDER_ROMANCE]
        self.assertEqual(
            len(founder_romance_hits),
            0,
            "v0.1 known limitation: sub-pattern 1a is intentionally narrow",
        )

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

    def test_v01_recall_on_founder_romance_corpus_entries(self) -> None:
        """v0.1 founder_romance recall against corpus entries that the manifest tags as founder_romance.

        Spec target: ≥70%. v0.1 ships sub-pattern 1a only; the only corpus entry
        that exhibits 1a verbatim is caught_01. Other founder_romance corpus
        entries (caught_06) exhibit sub-pattern 1c which is not yet implemented.
        v0.1 recall is therefore 1/2 = 50%. Test asserts the current ceiling
        and documents the gap for v0.1.1.
        """
        entries = _parse_manifest_entries(self.manifest_path)
        fr_entries = [name for name, status, patterns in entries
                      if status == "caught" and "founder_romance" in patterns]
        self.assertGreater(len(fr_entries), 0, "no founder_romance corpus entries found")

        fired = 0
        for file_name in fr_entries:
            findings = self._scan_corpus_file(file_name)
            if any(f.pattern == Pattern.FOUNDER_ROMANCE for f in findings):
                fired += 1

        recall = fired / len(fr_entries) if fr_entries else 0.0
        # v0.1 ceiling — only 1a is implemented. When 1b/1c ship, raise this.
        self.assertGreaterEqual(
            recall,
            0.5,
            f"v0.1 founder_romance recall regression: {fired}/{len(fr_entries)} = {recall:.0%}",
        )

    def test_v01_precision_on_clean_corpus(self) -> None:
        """v0.1 founder_romance precision = TP / (TP + FP) on the corpus.

        Spec target: ≥60%. With sub-pattern 1a only and 3 clean files all producing
        zero hits, precision should be 1.0 (no false positives).
        """
        entries = _parse_manifest_entries(self.manifest_path)
        fr_positive_files = [name for name, status, patterns in entries
                             if status == "caught" and "founder_romance" in patterns]
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


# --- CLI smoke tests ---


class CLISmokeTests(unittest.TestCase):
    def test_scan_file_returns_findings(self) -> None:
        path = CORPUS_DIR / "caught_01_founder_romance_closer.md"
        findings = scan_file(path)
        # frontmatter contains no matches; body has one canonical hit.
        # scan_file doesn't strip frontmatter — but the frontmatter doesn't
        # contain biographical-closer phrasing, so total hits should still be 1.
        self.assertGreaterEqual(len(findings), 1)
        self.assertTrue(any(f.pattern == Pattern.FOUNDER_ROMANCE for f in findings))

    def test_finding_format_includes_severity_and_location(self) -> None:
        text = "The man who stood post in the Guard does not bet the framework on un-replicated data."
        findings = scan(text, file_path="test.md")
        formatted = findings[0].format()
        self.assertIn("HIGH", formatted)
        self.assertIn("founder_romance", formatted)
        self.assertIn("test.md:1", formatted)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.CRITICAL)
    unittest.main(verbosity=2)
