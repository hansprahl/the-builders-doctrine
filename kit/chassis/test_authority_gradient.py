"""
Tests for kit/chassis/authority_gradient.py.

Run with:  python3 -m pytest kit/chassis/test_authority_gradient.py -v
or:        python3 kit/chassis/test_authority_gradient.py

Verifies the doctrine invariants the module preserves:
  - WORLD_BOUNDARY never tier-authorized (Principle #4 hard floor)
  - Tier authorization table is overridable per product
  - Violations logged, not blocked (observational doctrine)
  - Approval-queue integration by callback, not hard import
  - No LLM dependency
  - Five outcome metrics computed correctly
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kit.chassis.authority_gradient import (
    ActionClass,
    AuthorityGradient,
    Channel,
    DEFAULT_TIER_AUTHORIZED_CLASSES,
    GradientEvent,
    GradientLog,
    Tier,
    classify_action,
    infer_tier_from_callsign,
    is_violation,
)


SAMPLE_TOOLS: dict[str, ActionClass] = {
    "send_email": ActionClass.WORLD_BOUNDARY,
    "post_publicly": ActionClass.WORLD_BOUNDARY,
    "delegate_to_squad": ActionClass.REVERSIBLE_IN_MISSION,
    "declare_done": ActionClass.TERMINAL,
    "what_else_reflection": ActionClass.PLANNING,
    "draft_post": ActionClass.REVERSIBLE_IN_UNIT,
    "produce_artifact": ActionClass.REVERSIBLE_IN_UNIT,
}


# ──────────────────────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────────────────────


class TestEnums(unittest.TestCase):
    def test_tier_values_are_mca_vocabulary(self):
        self.assertEqual(Tier.OFFICER.value, "officer")
        self.assertEqual(Tier.NCO.value, "nco")
        self.assertEqual(Tier.SOLDIER.value, "soldier")

    def test_channel_values_match_mca(self):
        self.assertEqual(Channel.COMMAND.value, "command")
        self.assertEqual(Channel.STAFF.value, "staff")

    def test_action_classes_cover_gradient_table(self):
        values = {a.value for a in ActionClass}
        self.assertEqual(
            values,
            {
                "world_boundary",
                "reversible_in_mission",
                "reversible_in_unit",
                "planning",
                "terminal",
            },
        )


# ──────────────────────────────────────────────────────────────────────────────
# classify_action
# ──────────────────────────────────────────────────────────────────────────────


class TestClassifyAction(unittest.TestCase):
    def test_known_tool_returns_mapped_class(self):
        self.assertEqual(
            classify_action("send_email", SAMPLE_TOOLS),
            ActionClass.WORLD_BOUNDARY,
        )

    def test_unknown_tool_returns_default(self):
        self.assertEqual(
            classify_action("unknown_tool", SAMPLE_TOOLS),
            ActionClass.REVERSIBLE_IN_UNIT,
        )

    def test_unknown_tool_with_custom_default(self):
        self.assertEqual(
            classify_action(
                "unknown_tool", SAMPLE_TOOLS, default=ActionClass.PLANNING,
            ),
            ActionClass.PLANNING,
        )


# ──────────────────────────────────────────────────────────────────────────────
# is_violation — Principle #4 invariants
# ──────────────────────────────────────────────────────────────────────────────


class TestIsViolation(unittest.TestCase):
    def test_world_boundary_is_never_a_tier_violation(self):
        for tier in (Tier.OFFICER, Tier.NCO, Tier.SOLDIER):
            self.assertFalse(
                is_violation(tier, ActionClass.WORLD_BOUNDARY),
                f"WORLD_BOUNDARY flagged as tier violation for {tier}",
            )

    def test_nco_terminal_is_violation(self):
        self.assertTrue(is_violation(Tier.NCO, ActionClass.TERMINAL))

    def test_nco_planning_is_violation(self):
        self.assertTrue(is_violation(Tier.NCO, ActionClass.PLANNING))

    def test_nco_in_unit_is_authorized(self):
        self.assertFalse(is_violation(Tier.NCO, ActionClass.REVERSIBLE_IN_UNIT))

    def test_officer_all_non_world_boundary_authorized(self):
        for ac in (
            ActionClass.REVERSIBLE_IN_UNIT,
            ActionClass.REVERSIBLE_IN_MISSION,
            ActionClass.PLANNING,
            ActionClass.TERMINAL,
        ):
            self.assertFalse(is_violation(Tier.OFFICER, ac))

    def test_soldier_only_in_unit_authorized(self):
        self.assertFalse(is_violation(Tier.SOLDIER, ActionClass.REVERSIBLE_IN_UNIT))
        self.assertTrue(is_violation(Tier.SOLDIER, ActionClass.REVERSIBLE_IN_MISSION))
        self.assertTrue(is_violation(Tier.SOLDIER, ActionClass.PLANNING))
        self.assertTrue(is_violation(Tier.SOLDIER, ActionClass.TERMINAL))

    def test_custom_table_can_expand_nco_authority(self):
        custom = {
            Tier.NCO: frozenset({
                ActionClass.REVERSIBLE_IN_UNIT,
                ActionClass.REVERSIBLE_IN_MISSION,
            }),
        }
        self.assertFalse(
            is_violation(
                Tier.NCO, ActionClass.REVERSIBLE_IN_MISSION,
                tier_authorized_classes=custom,
            ),
        )

    def test_custom_table_cannot_authorize_world_boundary(self):
        # Even if a product tries to authorize WORLD_BOUNDARY for NCO, the
        # invariant holds: WORLD_BOUNDARY is never a tier-violation, so it
        # always escalates regardless of table entries.
        custom = {Tier.NCO: frozenset({ActionClass.WORLD_BOUNDARY})}
        self.assertFalse(
            is_violation(
                Tier.NCO, ActionClass.WORLD_BOUNDARY,
                tier_authorized_classes=custom,
            ),
        )


# ──────────────────────────────────────────────────────────────────────────────
# infer_tier_from_callsign
# ──────────────────────────────────────────────────────────────────────────────


class TestInferTier(unittest.TestCase):
    def test_pl_is_officer(self):
        self.assertEqual(infer_tier_from_callsign("PL"), Tier.OFFICER)

    def test_empty_is_officer(self):
        self.assertEqual(infer_tier_from_callsign(""), Tier.OFFICER)

    def test_single_slash_is_nco(self):
        self.assertEqual(infer_tier_from_callsign("1/1"), Tier.NCO)
        self.assertEqual(infer_tier_from_callsign("1/2"), Tier.NCO)

    def test_two_slashes_is_soldier(self):
        self.assertEqual(infer_tier_from_callsign("1/1/A"), Tier.SOLDIER)
        self.assertEqual(infer_tier_from_callsign("1/2/B"), Tier.SOLDIER)


# ──────────────────────────────────────────────────────────────────────────────
# GradientLog — logging behavior
# ──────────────────────────────────────────────────────────────────────────────


class TestGradientLogBasics(unittest.TestCase):
    def test_log_event_returns_event(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        event = log.log_event(Tier.NCO, "1/1", "draft_post")
        self.assertIsInstance(event, GradientEvent)
        self.assertEqual(event.action_class, ActionClass.REVERSIBLE_IN_UNIT)
        self.assertFalse(event.is_violation)
        self.assertFalse(event.is_world_boundary)

    def test_log_event_flags_violation_but_does_not_block(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        event = log.log_event(Tier.NCO, "1/1", "declare_done")
        self.assertTrue(event.is_violation)
        self.assertEqual(event.action_class, ActionClass.TERMINAL)
        # event still in log — observational
        self.assertEqual(len(log.events), 1)

    def test_world_boundary_flagged(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        event = log.log_event(Tier.OFFICER, "PL", "send_email")
        self.assertTrue(event.is_world_boundary)
        self.assertFalse(event.is_violation)  # PL doing world action is routing, not violation

    def test_event_to_dict_serializable(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        event = log.log_event(Tier.NCO, "1/1", "draft_post", notes="test")
        d = event.to_dict()
        self.assertEqual(d["actor_tier"], "nco")
        self.assertEqual(d["action_class"], "reversible_in_unit")
        # Round-trip through JSON
        self.assertEqual(json.loads(event.to_jsonl())["tool_name"], "draft_post")

    def test_run_dir_writes_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            log = GradientLog(tool_classes=SAMPLE_TOOLS, run_dir=run_dir)
            log.log_event(Tier.NCO, "1/1", "draft_post")
            log.log_event(Tier.OFFICER, "PL", "declare_done")
            jsonl_path = run_dir / "gradient_log.jsonl"
            self.assertTrue(jsonl_path.exists())
            lines = jsonl_path.read_text().strip().splitlines()
            self.assertEqual(len(lines), 2)

    def test_no_run_dir_is_in_memory_only(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        log.log_event(Tier.NCO, "1/1", "draft_post")
        # No file system side effects — just events in memory
        self.assertEqual(len(log.events), 1)


# ──────────────────────────────────────────────────────────────────────────────
# Callback hooks
# ──────────────────────────────────────────────────────────────────────────────


class TestCallbackHooks(unittest.TestCase):
    def test_on_world_boundary_fires_on_world_action(self):
        hook = MagicMock()
        log = GradientLog(tool_classes=SAMPLE_TOOLS, on_world_boundary=hook)
        log.log_event(Tier.OFFICER, "PL", "send_email")
        hook.assert_called_once()
        event = hook.call_args[0][0]
        self.assertEqual(event.tool_name, "send_email")

    def test_on_world_boundary_does_not_fire_on_in_unit(self):
        hook = MagicMock()
        log = GradientLog(tool_classes=SAMPLE_TOOLS, on_world_boundary=hook)
        log.log_event(Tier.NCO, "1/1", "draft_post")
        hook.assert_not_called()

    def test_on_violation_fires_on_tier_scope_violation(self):
        hook = MagicMock()
        log = GradientLog(tool_classes=SAMPLE_TOOLS, on_violation=hook)
        log.log_event(Tier.NCO, "1/1", "declare_done")
        hook.assert_called_once()

    def test_on_violation_does_not_fire_on_authorized_action(self):
        hook = MagicMock()
        log = GradientLog(tool_classes=SAMPLE_TOOLS, on_violation=hook)
        log.log_event(Tier.OFFICER, "PL", "declare_done")
        hook.assert_not_called()

    def test_callback_exception_does_not_break_logging(self):
        def broken(event):
            raise RuntimeError("boom")
        log = GradientLog(
            tool_classes=SAMPLE_TOOLS,
            on_world_boundary=broken,
        )
        # Should not raise — exception is logged and swallowed
        event = log.log_event(Tier.OFFICER, "PL", "send_email")
        self.assertEqual(event.tool_name, "send_email")
        self.assertEqual(len(log.events), 1)


# ──────────────────────────────────────────────────────────────────────────────
# Metrics
# ──────────────────────────────────────────────────────────────────────────────


class TestMetrics(unittest.TestCase):
    def _build_log_with_mixed_events(self) -> GradientLog:
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        # 3 NCO in-unit, 2 PL escalations (delegate + declare_done)
        log.log_event(Tier.NCO, "1/1", "draft_post")
        log.log_event(Tier.NCO, "1/2", "produce_artifact")
        log.log_event(Tier.NCO, "1/3", "draft_post")
        log.log_event(Tier.OFFICER, "PL", "delegate_to_squad")
        log.log_event(Tier.OFFICER, "PL", "declare_done")
        return log

    def test_escalation_ratio(self):
        log = self._build_log_with_mixed_events()
        m = log.metric_escalation_ratio()
        self.assertEqual(m["in_unit_resolutions"], 3)
        self.assertEqual(m["escalations"], 2)
        self.assertEqual(m["total"], 5)
        self.assertAlmostEqual(m["in_unit_pct"], 0.6)

    def test_escalation_ratio_empty(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        m = log.metric_escalation_ratio()
        self.assertEqual(m["total"], 0)
        self.assertEqual(m["in_unit_pct"], 0.0)

    def test_pl_cycle_time_no_turns(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        m = log.metric_pl_cycle_time()
        self.assertEqual(m["turns"], 0)
        self.assertIsNone(m["mean_sec"])

    def test_pl_cycle_time_with_turns(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        # Simulate two turns
        log.pl_turn_starts = [100.0, 200.0]
        log.pl_turn_ends = [110.0, 230.0]
        m = log.metric_pl_cycle_time()
        self.assertEqual(m["turns"], 2)
        self.assertAlmostEqual(m["mean_sec"], 20.0)  # (10 + 30) / 2

    def test_violation_count(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        log.log_event(Tier.NCO, "1/1", "declare_done")  # violation
        log.log_event(Tier.SOLDIER, "1/1/A", "delegate_to_squad")  # violation
        log.log_event(Tier.NCO, "1/2", "draft_post")  # clean
        m = log.metric_violation_count()
        self.assertEqual(m["total"], 2)
        self.assertEqual(m["by_tier"], {"nco": 1, "soldier": 1})

    def test_hard_floor_breach_count_with_approval(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        log.log_event(
            Tier.OFFICER, "PL", "send_email",
            notes="queued action_id=abc123 awaiting approval",
        )
        m = log.metric_hard_floor_breach_count()
        self.assertEqual(m["world_boundary_attempts"], 1)
        self.assertEqual(m["breaches"], 0)

    def test_hard_floor_breach_count_no_approval_evidence(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        log.log_event(Tier.NCO, "1/1", "send_email")  # no approval in notes
        m = log.metric_hard_floor_breach_count()
        self.assertEqual(m["world_boundary_attempts"], 1)
        self.assertEqual(m["breaches"], 1)

    def test_reflection_results_counted(self):
        log = GradientLog(tool_classes=SAMPLE_TOOLS)
        log.log_reflection_result("proceed")
        log.log_reflection_result("iterate")
        log.log_reflection_result("iterate", was_confident_zero_gaps=True)
        log.log_reflection_result("refuse")
        m = log.metric_confident_zero_gaps_rate()
        self.assertEqual(m["total_gate_evaluations"], 4)
        self.assertEqual(m["proceeds"], 1)
        self.assertEqual(m["iterates"], 2)
        self.assertEqual(m["refuses"], 1)
        self.assertEqual(m["confident_zero_gaps_caught"], 1)

    def test_all_metrics_writes_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            log = GradientLog(tool_classes=SAMPLE_TOOLS, run_dir=run_dir)
            log.log_event(Tier.NCO, "1/1", "draft_post")
            log.all_metrics()
            metrics_path = run_dir / "gradient_metrics.json"
            self.assertTrue(metrics_path.exists())
            data = json.loads(metrics_path.read_text())
            self.assertIn("escalation_ratio", data)
            self.assertIn("hard_floor_breach_count", data)


# ──────────────────────────────────────────────────────────────────────────────
# AuthorityGradient facade
# ──────────────────────────────────────────────────────────────────────────────


class TestFacade(unittest.TestCase):
    def test_classify_through_facade(self):
        ag = AuthorityGradient(tool_classes=SAMPLE_TOOLS)
        self.assertEqual(ag.classify("send_email"), ActionClass.WORLD_BOUNDARY)
        self.assertEqual(ag.classify("unknown"), ActionClass.REVERSIBLE_IN_UNIT)

    def test_violates_through_facade(self):
        ag = AuthorityGradient(tool_classes=SAMPLE_TOOLS)
        self.assertTrue(ag.violates(Tier.NCO, "declare_done"))
        self.assertFalse(ag.violates(Tier.OFFICER, "declare_done"))

    def test_facade_log_is_usable(self):
        ag = AuthorityGradient(tool_classes=SAMPLE_TOOLS)
        ag.log.log_event(Tier.NCO, "1/1", "draft_post")
        self.assertEqual(len(ag.log.events), 1)


# ──────────────────────────────────────────────────────────────────────────────
# No LLM dependency
# ──────────────────────────────────────────────────────────────────────────────


class TestNoLLMDependency(unittest.TestCase):
    def test_module_does_not_import_anthropic(self):
        import kit.chassis.authority_gradient as mod
        # Module should not have anthropic / openai / etc. as dependencies
        for forbidden in ("anthropic", "openai"):
            self.assertFalse(
                hasattr(mod, forbidden),
                f"chassis must not depend on {forbidden}",
            )

    def test_classifier_works_offline(self):
        # Pure-function classifier should produce deterministic output with
        # zero side effects — covered implicitly by other tests, but a single
        # offline smoke test makes the invariant explicit.
        ag = AuthorityGradient(tool_classes={"x": ActionClass.WORLD_BOUNDARY})
        self.assertEqual(ag.classify("x"), ActionClass.WORLD_BOUNDARY)
        self.assertEqual(ag.classify("y"), ActionClass.REVERSIBLE_IN_UNIT)


if __name__ == "__main__":
    unittest.main()
