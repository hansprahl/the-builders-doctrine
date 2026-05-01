"""
Tests for kit/chassis/aar.py.

Run with:  python3 kit/chassis/test_aar.py
"""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kit.chassis.aar import (
    AAR, AARLog, CalibrationReport,
    SUCCESS, FAILURE, PARTIAL, ABANDONED,
    VALID_OUTCOMES, HABIT, RECOMMENDATION,
)


class TestRecordOutcome(unittest.TestCase):
    def setUp(self):
        self.log = AARLog()  # in-memory

    def tearDown(self):
        self.log.close()

    def test_record_returns_id(self):
        aid = self.log.record_outcome(HABIT, "morning run", SUCCESS,
                                       specialist="scout")
        self.assertEqual(len(aid), 12)
        loaded = self.log.get(aid)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.action_type, HABIT)
        self.assertEqual(loaded.action_name, "morning run")
        self.assertEqual(loaded.outcome, SUCCESS)
        self.assertEqual(loaded.specialist, "scout")

    def test_invalid_outcome_raises(self):
        with self.assertRaises(ValueError):
            self.log.record_outcome(HABIT, "morning run", "kind-of-worked")

    def test_empty_action_type_raises(self):
        with self.assertRaises(ValueError):
            self.log.record_outcome("", "morning run", SUCCESS)

    def test_empty_action_name_raises(self):
        with self.assertRaises(ValueError):
            self.log.record_outcome(HABIT, "", SUCCESS)

    def test_action_id_persisted(self):
        aid = self.log.record_outcome(
            RECOMMENDATION, "rec X", PARTIAL,
            specialist="scout", action_id="abc123",
        )
        loaded = self.log.get(aid)
        self.assertEqual(loaded.action_id, "abc123")

    def test_action_id_optional(self):
        aid = self.log.record_outcome(HABIT, "x", SUCCESS, specialist="scout")
        loaded = self.log.get(aid)
        self.assertIsNone(loaded.action_id)


class TestListOutcomes(unittest.TestCase):
    def setUp(self):
        self.log = AARLog()
        self.log.record_outcome(HABIT, "run", SUCCESS, specialist="scout")
        self.log.record_outcome(HABIT, "meditate", PARTIAL, specialist="scout")
        self.log.record_outcome(RECOMMENDATION, "save more", SUCCESS, specialist="atlas")

    def tearDown(self):
        self.log.close()

    def test_list_all(self):
        out = self.log.list_outcomes()
        self.assertEqual(len(out), 3)

    def test_filter_by_specialist(self):
        out = self.log.list_outcomes(specialist="scout")
        self.assertEqual(len(out), 2)
        self.assertTrue(all(o.specialist == "scout" for o in out))

    def test_filter_by_action_type(self):
        out = self.log.list_outcomes(action_type=RECOMMENDATION)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].action_name, "save more")

    def test_combined_filter(self):
        out = self.log.list_outcomes(specialist="scout", action_type=HABIT)
        self.assertEqual(len(out), 2)

    def test_limit(self):
        out = self.log.list_outcomes(limit=1)
        self.assertEqual(len(out), 1)


class TestCalibrationReport(unittest.TestCase):
    def setUp(self):
        self.log = AARLog()

    def tearDown(self):
        self.log.close()

    def test_empty_report(self):
        r = self.log.calibration_report()
        self.assertEqual(r.total, 0)
        self.assertEqual(r.success_rate, 0.0)

    def test_aggregate(self):
        # 3 success, 1 failure, 1 partial, 0 abandoned across 2 specialists
        for spec in ("scout", "atlas"):
            self.log.record_outcome(HABIT, "x", SUCCESS, specialist=spec)
        self.log.record_outcome(HABIT, "y", SUCCESS, specialist="scout")
        self.log.record_outcome(HABIT, "z", FAILURE, specialist="atlas")
        self.log.record_outcome(HABIT, "w", PARTIAL, specialist="scout")

        r = self.log.calibration_report()
        self.assertEqual(r.total, 5)
        self.assertEqual(r.success, 3)
        self.assertEqual(r.failure, 1)
        self.assertEqual(r.partial, 1)
        self.assertEqual(r.abandoned, 0)
        self.assertAlmostEqual(r.success_rate, 0.6)

    def test_per_specialist_filter(self):
        self.log.record_outcome(HABIT, "x", SUCCESS, specialist="scout")
        self.log.record_outcome(HABIT, "y", FAILURE, specialist="atlas")
        r = self.log.calibration_report(specialist="scout")
        self.assertEqual(r.total, 1)
        self.assertEqual(r.success, 1)
        self.assertEqual(r.failure, 0)

    def test_specialist_no_data_zero_report(self):
        self.log.record_outcome(HABIT, "x", SUCCESS, specialist="scout")
        r = self.log.calibration_report(specialist="atlas")
        self.assertEqual(r.total, 0)
        self.assertEqual(r.specialist, "atlas")

    def test_summary_format(self):
        self.log.record_outcome(HABIT, "x", SUCCESS, specialist="scout")
        self.log.record_outcome(HABIT, "y", FAILURE, specialist="scout")
        r = self.log.calibration_report(specialist="scout")
        self.assertIn("2 tracked", r.summary())
        self.assertIn("50% success", r.summary())
        self.assertIn("S:1", r.summary())
        self.assertIn("F:1", r.summary())

    def test_summary_skips_zero_categories(self):
        self.log.record_outcome(HABIT, "x", SUCCESS, specialist="scout")
        r = self.log.calibration_report(specialist="scout")
        # Only S:1 should appear (no F/P/A counts of 0).
        self.assertIn("S:1", r.summary())
        self.assertNotIn("F:0", r.summary())
        self.assertNotIn("P:0", r.summary())
        self.assertNotIn("A:0", r.summary())


class TestCalibrationBySpecialist(unittest.TestCase):
    def setUp(self):
        self.log = AARLog()

    def tearDown(self):
        self.log.close()

    def test_groups_by_specialist(self):
        self.log.record_outcome(HABIT, "x", SUCCESS, specialist="scout")
        self.log.record_outcome(HABIT, "y", SUCCESS, specialist="scout")
        self.log.record_outcome(HABIT, "z", FAILURE, specialist="atlas")
        report = self.log.calibration_by_specialist()
        self.assertEqual(set(report.keys()), {"scout", "atlas"})
        self.assertEqual(report["scout"].total, 2)
        self.assertEqual(report["scout"].success, 2)
        self.assertEqual(report["atlas"].total, 1)
        self.assertEqual(report["atlas"].failure, 1)

    def test_empty_specialist_excluded(self):
        # AARs with no specialist field are ungrouped data and should not
        # appear in per-specialist reports.
        self.log.record_outcome(HABIT, "x", SUCCESS)
        self.log.record_outcome(HABIT, "y", SUCCESS, specialist="scout")
        report = self.log.calibration_by_specialist()
        self.assertEqual(set(report.keys()), {"scout"})


class TestFormatForPrompt(unittest.TestCase):
    def setUp(self):
        self.log = AARLog()

    def tearDown(self):
        self.log.close()

    def test_empty_returns_empty_string(self):
        self.assertEqual(self.log.format_for_prompt(), "")

    def test_renders_track_records(self):
        self.log.record_outcome(HABIT, "a", SUCCESS, specialist="scout")
        self.log.record_outcome(HABIT, "b", FAILURE, specialist="scout")
        self.log.record_outcome(HABIT, "c", SUCCESS, specialist="atlas")
        block = self.log.format_for_prompt(specialist_labels={
            "scout": "Scout (Wellness)",
            "atlas": "Atlas (Finance)",
        })
        self.assertIn("STAFF TRACK RECORDS", block)
        self.assertIn("Scout (Wellness):", block)
        self.assertIn("Atlas (Finance):", block)
        # Order respects the labels dict's insertion order.
        scout_idx = block.index("Scout")
        atlas_idx = block.index("Atlas")
        self.assertLess(scout_idx, atlas_idx)

    def test_specialists_not_in_labels_are_skipped(self):
        self.log.record_outcome(HABIT, "a", SUCCESS, specialist="scout")
        self.log.record_outcome(HABIT, "b", SUCCESS, specialist="forge")
        block = self.log.format_for_prompt(specialist_labels={
            "scout": "Scout (Wellness)",
        })
        self.assertIn("Scout", block)
        self.assertNotIn("Forge", block)
        self.assertNotIn("forge", block)

    def test_no_labels_uses_raw_names(self):
        self.log.record_outcome(HABIT, "a", SUCCESS, specialist="scout")
        block = self.log.format_for_prompt()
        self.assertIn("Scout", block)  # title-cased

    def test_custom_header(self):
        self.log.record_outcome(HABIT, "a", SUCCESS, specialist="scout")
        block = self.log.format_for_prompt(
            specialist_labels={"scout": "Scout"},
            header="[CUSTOM HEADER]",
        )
        self.assertTrue(block.startswith("[CUSTOM HEADER]"))


class TestSpecialistLine(unittest.TestCase):
    def setUp(self):
        self.log = AARLog()

    def tearDown(self):
        self.log.close()

    def test_empty_returns_empty(self):
        self.assertEqual(self.log.specialist_line("scout"), "")

    def test_renders_summary(self):
        self.log.record_outcome(HABIT, "a", SUCCESS, specialist="scout")
        line = self.log.specialist_line("scout")
        self.assertIn("YOUR TRACK RECORD", line)
        self.assertIn("1 recommendations tracked", line)
        self.assertIn("100% success", line)


class TestPersistenceAcrossInstances(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.path = self.tmp / "aar.db"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_disk_roundtrip(self):
        log1 = AARLog(db_path=self.path)
        aid = log1.record_outcome(HABIT, "x", SUCCESS, specialist="scout")
        log1.close()

        log2 = AARLog(db_path=self.path)
        loaded = log2.get(aid)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.outcome, SUCCESS)
        log2.close()

    def test_creates_parent_directory(self):
        nested = self.tmp / "deep" / "nested" / "aar.db"
        log = AARLog(db_path=nested)
        log.record_outcome(HABIT, "x", SUCCESS, specialist="scout")
        log.close()
        self.assertTrue(nested.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
