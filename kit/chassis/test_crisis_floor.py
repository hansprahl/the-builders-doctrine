"""
Tests for kit/chassis/crisis_floor.py.

Run with:  python3 -m pytest kit/chassis/test_crisis_floor.py -v
or:        python3 kit/chassis/test_crisis_floor.py    (uses unittest harness)

The tests verify the doctrine invariants the module is supposed to preserve:
deterministic detection, fixed-response semantics, alert side-effect,
WARNING log line, fail-safe on alert handler exception, and the kit-template
loader contract.
"""

from __future__ import annotations

import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

# Ensure repo root is importable when running this file directly.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kit.chassis.crisis_floor import (
    CrisisEvent,
    CrisisFloor,
    _extract_phrases,
)

SAMPLE_PHRASES = {
    "kill myself", "killing myself",
    "end my life", "want to die",
    "no reason to live",
    "self-harm",
}

SAMPLE_RESPONSE = (
    "Stop.\n"
    "I can't help you with this. A machine can't.\n"
    "What you need is a real person.\n"
    "Crisis line: 988"
)


class TestDetection(unittest.TestCase):
    def setUp(self):
        self.floor = CrisisFloor(phrases=SAMPLE_PHRASES, response=SAMPLE_RESPONSE)

    def test_direct_phrase_fires(self):
        self.assertTrue(self.floor.is_crisis("I want to kill myself"))
        self.assertTrue(self.floor.is_crisis("I just want to die"))
        self.assertTrue(self.floor.is_crisis("there is no reason to live"))

    def test_case_insensitive(self):
        self.assertTrue(self.floor.is_crisis("KILL MYSELF"))
        self.assertTrue(self.floor.is_crisis("Want To Die"))

    def test_substring_match(self):
        # The phrase fires even when embedded mid-sentence.
        self.assertTrue(self.floor.is_crisis(
            "honestly some days I want to die and I don't tell anyone"
        ))

    def test_unrelated_text_does_not_fire(self):
        self.assertFalse(self.floor.is_crisis("hello, how are you today?"))
        self.assertFalse(self.floor.is_crisis("the meeting at 3pm went well"))

    def test_empty_text_does_not_fire(self):
        self.assertFalse(self.floor.is_crisis(""))
        self.assertFalse(self.floor.is_crisis("   "))

    def test_deterministic(self):
        # Same input twice — same output. No sampling, no probability.
        msg = "I want to kill myself"
        for _ in range(50):
            self.assertTrue(self.floor.is_crisis(msg))

    def test_matched_phrase_returned(self):
        match = self.floor.matched_phrase("today I want to die honestly")
        self.assertEqual(match, "want to die")
        self.assertIsNone(self.floor.matched_phrase("nothing wrong here"))


class TestHandler(unittest.TestCase):
    def setUp(self):
        self.alerts: list[CrisisEvent] = []
        self.floor = CrisisFloor(
            phrases=SAMPLE_PHRASES,
            response=SAMPLE_RESPONSE,
            admin_alert=self.alerts.append,
        )

    def test_returns_fixed_response(self):
        reply = self.floor.handle_crisis("hans", "I want to kill myself")
        self.assertEqual(reply, SAMPLE_RESPONSE)

    def test_response_is_unchanged_across_calls(self):
        # No personalization, no model generation, no variation.
        a = self.floor.handle_crisis("user_a", "I want to die")
        b = self.floor.handle_crisis("user_b", "killing myself tonight")
        self.assertEqual(a, b)

    def test_admin_alert_receives_event(self):
        self.floor.handle_crisis("hans", "I want to kill myself")
        self.assertEqual(len(self.alerts), 1)
        ev = self.alerts[0]
        self.assertIsInstance(ev, CrisisEvent)
        self.assertEqual(ev.user_id, "hans")
        self.assertIn("kill myself", ev.text)
        self.assertEqual(ev.matched_phrase, "kill myself")

    def test_admin_alert_failure_does_not_block_response(self):
        def boom(event):
            raise RuntimeError("alert handler crashed")
        floor = CrisisFloor(
            phrases=SAMPLE_PHRASES, response=SAMPLE_RESPONSE,
            admin_alert=boom,
        )
        # Must not raise — the user-facing response is the load-bearing
        # guarantee; alerts are best-effort.
        reply = floor.handle_crisis("hans", "want to die")
        self.assertEqual(reply, SAMPLE_RESPONSE)

    def test_warning_log_line_lands(self):
        with self.assertLogs("kit.chassis.crisis_floor", level="WARNING") as cm:
            self.floor.handle_crisis("hans", "I want to die")
        # One WARNING line, contains the marker, the user_id, and the
        # matched phrase.
        self.assertEqual(len(cm.records), 1)
        rec = cm.records[0]
        self.assertEqual(rec.levelname, "WARNING")
        self.assertIn("CRISIS DETECTED", rec.getMessage())
        self.assertIn("hans", rec.getMessage())
        self.assertIn("want to die", rec.getMessage())

    def test_excerpt_truncation(self):
        long_text = "I want to die " + ("x" * 500)
        floor = CrisisFloor(
            phrases=SAMPLE_PHRASES, response=SAMPLE_RESPONSE,
            admin_alert=self.alerts.append,
            excerpt_len=50,
        )
        floor.handle_crisis("hans", long_text)
        ev = self.alerts[-1]
        self.assertLessEqual(len(ev.excerpt), 50)
        self.assertIn("want to die", ev.excerpt)


class TestConstructor(unittest.TestCase):
    def test_empty_phrases_rejected(self):
        with self.assertRaises(ValueError):
            CrisisFloor(phrases=[], response="x")
        with self.assertRaises(ValueError):
            CrisisFloor(phrases=["", "  "], response="x")

    def test_empty_response_rejected(self):
        with self.assertRaises(ValueError):
            CrisisFloor(phrases=["want to die"], response="")
        with self.assertRaises(ValueError):
            CrisisFloor(phrases=["want to die"], response="   ")

    def test_phrases_normalized_at_construction(self):
        floor = CrisisFloor(
            phrases=["KILL MYSELF", "  Want To Die  "],
            response="x",
        )
        self.assertIn("kill myself", floor.phrases)
        self.assertIn("want to die", floor.phrases)


class TestPhraseExtractor(unittest.TestCase):
    def test_plain_lines(self):
        body = "kill myself\nwant to die\nno reason to live"
        self.assertEqual(
            _extract_phrases(body),
            ["kill myself", "want to die", "no reason to live"],
        )

    def test_bullets(self):
        body = "- kill myself\n- want to die\n* end my life"
        out = _extract_phrases(body)
        self.assertIn("kill myself", out)
        self.assertIn("want to die", out)
        self.assertIn("end my life", out)

    def test_quoted(self):
        body = '"kill myself"\n"want to die"'
        out = _extract_phrases(body)
        self.assertIn("kill myself", out)
        self.assertIn("want to die", out)

    def test_inline_comments_stripped(self):
        body = "kill myself  # direct ideation\nwant to die"
        out = _extract_phrases(body)
        self.assertIn("kill myself", out)
        self.assertNotIn("# direct ideation", " ".join(out))

    def test_section_headers_skipped(self):
        body = (
            "### direct ideation\n"
            "kill myself\n"
            "Direct triggers:\n"
            "want to die\n"
        )
        out = _extract_phrases(body)
        self.assertIn("kill myself", out)
        self.assertIn("want to die", out)
        self.assertNotIn("direct ideation", out)
        self.assertNotIn("direct triggers", out)

    def test_dedupes(self):
        body = "kill myself\nkill myself\nKILL MYSELF"
        self.assertEqual(_extract_phrases(body), ["kill myself"])

    def test_long_prose_lines_filtered(self):
        body = (
            "this is a long sentence that is clearly explanatory text and "
            "not a substring trigger phrase the runtime would actually use"
        )
        self.assertEqual(_extract_phrases(body), [])


class TestFromKitTemplate(unittest.TestCase):
    """
    Smoke-test the loader against a synthetic populated template. We don't
    test against the kit's STORY-only fixtures because CRISIS_TRIGGERS.md
    in the kit is by design unfilled — the test creates its own filled copy
    in a tempdir.
    """
    def setUp(self):
        import tempfile
        self.tmp = Path(tempfile.mkdtemp())
        self.path = self.tmp / "CRISIS_TRIGGERS.md"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, applicability: str, phrases: str, response: str):
        self.path.write_text(
            f"# CRISIS_TRIGGERS\n\n"
            f"<!-- KIT:FIELD name=\"crisis_applicability\" required=\"true\" min_words=\"60\" -->\n"
            f"{applicability}\n"
            f"<!-- KIT:END -->\n\n"
            f"<!-- KIT:FIELD name=\"trigger_phrases\" required=\"conditional_on:crisis_applicability\" min_words=\"60\" -->\n"
            f"{phrases}\n"
            f"<!-- KIT:END -->\n\n"
            f"<!-- KIT:FIELD name=\"response_template\" required=\"conditional_on:crisis_applicability\" min_words=\"60\" -->\n"
            f"{response}\n"
            f"<!-- KIT:END -->\n",
            encoding="utf-8",
        )

    def test_loads_populated_template(self):
        self._write(
            applicability=(
                "This product applies. Users may bring suicidal ideation "
                "and self-harm signals via the Telegram chat surface. The "
                "veteran population is at elevated baseline risk per VA "
                "data, and journal entries can surface acute distress."
            ),
            phrases="kill myself\nwant to die\nno reason to live",
            response=SAMPLE_RESPONSE,
        )
        floor = CrisisFloor.from_kit_template(self.path)
        self.assertTrue(floor.is_crisis("I want to die"))
        self.assertEqual(floor.handle_crisis("hans", "I want to die"),
                         SAMPLE_RESPONSE)

    def test_na_applicability_raises(self):
        self._write(
            applicability=(
                "N/A — this is a B2B accounting tool with no freeform "
                "user text surface. Users interact only via structured "
                "form fields, so distress cannot plausibly arrive here."
            ),
            phrases="(unused)",
            response="(unused)",
        )
        with self.assertRaises(ValueError):
            CrisisFloor.from_kit_template(self.path)

    def test_unfilled_phrases_raises(self):
        self._write(
            applicability="This product applies. " * 20,
            phrases="[your phrases here]",
            response=SAMPLE_RESPONSE,
        )
        with self.assertRaises(ValueError):
            CrisisFloor.from_kit_template(self.path)

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            CrisisFloor.from_kit_template(self.tmp / "nope.md")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    unittest.main(verbosity=2)
