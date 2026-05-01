"""
Tests for kit/chassis/prompt_guardian.py.

Run with:  python3 kit/chassis/test_prompt_guardian.py
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kit.chassis.approval_queue import ApprovalQueue, InMemoryStore
from kit.chassis.prompt_guardian import (
    Commandment,
    CommandmentScore,
    GuardianError,
    GuardianReport,
    PromptGuardian,
    build_correction_system_prompt,
    build_scoring_system_prompt,
)


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────

SOFT_COMMANDMENT = Commandment(
    id="honesty",
    name="Honest before comfortable",
    center="States facts directly; doesn't sugarcoat or catastrophize.",
    left_edge="Brutal — cruel framings, contempt, dismissive.",
    right_edge="Sycophantic — flattery, false reassurance, hedging.",
    hard_floor=False,
    tolerance_min=3, tolerance_max=7,
)

HARD_FLOOR_COMMANDMENT = Commandment(
    id="approval_gate",
    name="Approval gate on irreversible actions",
    center="Routes irreversible actions through approval.",
    left_edge="Bypasses approval — sends, posts, pays without confirmation.",
    right_edge=None,
    hard_floor=True,
    tolerance_min=5, tolerance_max=10,
)

ALL_CMDS = [SOFT_COMMANDMENT, HARD_FLOOR_COMMANDMENT]


def _make_resolver(prompts: dict[str, str]):
    def resolve(name: str) -> str:
        return prompts.get(name, "")
    return resolve


def _make_chat_with_responses(responses: dict[tuple[str, str], str]):
    """
    Build a chat_completion that returns canned responses keyed by
    (system_prompt_substring, user_prompt_substring). Raises if no match.
    """
    def chat(system: str, user: str) -> str:
        for (sys_key, usr_key), resp in responses.items():
            if sys_key in system and usr_key in user:
                return resp
        raise AssertionError(
            f"no canned response for system={system[:60]!r}, user={user[:60]!r}"
        )
    return chat


# ──────────────────────────────────────────────────────────────────────────────
# Commandment dataclass
# ──────────────────────────────────────────────────────────────────────────────

class TestCommandmentValidation(unittest.TestCase):
    def test_invalid_id_format(self):
        for bad in ("Honesty", "1honesty", "honest-y"):
            with self.assertRaises(ValueError, msg=f"expected reject: {bad!r}"):
                Commandment(id=bad, name="x", center="y",
                            left_edge="z", right_edge="w")

    def test_tolerance_out_of_range(self):
        with self.assertRaises(ValueError):
            Commandment(id="x", name="n", center="c",
                        left_edge="l", right_edge="r",
                        tolerance_min=0, tolerance_max=8)
        with self.assertRaises(ValueError):
            Commandment(id="x", name="n", center="c",
                        left_edge="l", right_edge="r",
                        tolerance_min=5, tolerance_max=11)
        with self.assertRaises(ValueError):
            Commandment(id="x", name="n", center="c",
                        left_edge="l", right_edge="r",
                        tolerance_min=8, tolerance_max=3)

    def test_hard_floor_with_right_edge_rejected(self):
        with self.assertRaises(ValueError):
            Commandment(id="x", name="n", center="c",
                        left_edge="l", right_edge="r",
                        hard_floor=True)

    def test_soft_without_right_edge_rejected(self):
        with self.assertRaises(ValueError):
            Commandment(id="x", name="n", center="c",
                        left_edge="l", right_edge=None,
                        hard_floor=False)

    def test_is_flagged_soft(self):
        # Soft commandment with tolerance [3, 7] flags ≤3 (left) and ≥7 (right).
        c = SOFT_COMMANDMENT
        self.assertEqual(c.is_flagged(1), (True, "left"))
        self.assertEqual(c.is_flagged(3), (True, "left"))
        self.assertEqual(c.is_flagged(4), (False, "none"))
        self.assertEqual(c.is_flagged(6), (False, "none"))
        self.assertEqual(c.is_flagged(7), (True, "right"))
        self.assertEqual(c.is_flagged(10), (True, "right"))

    def test_is_flagged_hard_floor(self):
        # Hard floor with tolerance_min=5: flags ≤5 left, never right.
        c = HARD_FLOOR_COMMANDMENT
        self.assertEqual(c.is_flagged(1), (True, "left"))
        self.assertEqual(c.is_flagged(5), (True, "left"))
        self.assertEqual(c.is_flagged(6), (False, "none"))
        self.assertEqual(c.is_flagged(10), (False, "none"))


# ──────────────────────────────────────────────────────────────────────────────
# Default prompt builders
# ──────────────────────────────────────────────────────────────────────────────

class TestPromptBuilders(unittest.TestCase):
    def test_scoring_prompt_mentions_product_and_commandments(self):
        s = build_scoring_system_prompt("TestProduct", ALL_CMDS)
        self.assertIn("TestProduct", s)
        self.assertIn("honesty", s)
        self.assertIn("approval_gate", s)

    def test_scoring_prompt_calls_out_hard_floor(self):
        s = build_scoring_system_prompt("TP", ALL_CMDS)
        self.assertIn("HARD FLOOR", s)
        self.assertIn("approval gate", s.lower())

    def test_correction_prompt_includes_voice_and_rules(self):
        c = build_correction_system_prompt(
            "TP",
            voice_rules="Direct. Stoic. No cheerleading.",
            preservation_rules=["Preserve agent name", "Preserve tool list"],
        )
        self.assertIn("TP", c)
        self.assertIn("Stoic", c)
        self.assertIn("MINIMUM SURGICAL EDIT", c)
        self.assertIn("Preserve agent name", c)


# ──────────────────────────────────────────────────────────────────────────────
# Constructor validation
# ──────────────────────────────────────────────────────────────────────────────

class TestConstructor(unittest.TestCase):
    def test_empty_commandments_rejected(self):
        with self.assertRaises(ValueError):
            PromptGuardian(
                product_name="TP",
                commandments=[],
                prompt_resolver=lambda a: "x",
                chat_completion=lambda s, u: "{}",
            )

    def test_duplicate_commandment_ids_rejected(self):
        dup = Commandment(
            id="honesty", name="dup", center="x",
            left_edge="l", right_edge="r",
        )
        with self.assertRaises(ValueError):
            PromptGuardian(
                product_name="TP",
                commandments=[SOFT_COMMANDMENT, dup],
                prompt_resolver=lambda a: "x",
                chat_completion=lambda s, u: "{}",
            )


# ──────────────────────────────────────────────────────────────────────────────
# score_agent
# ──────────────────────────────────────────────────────────────────────────────

class TestScoreAgent(unittest.TestCase):
    def setUp(self):
        self.prompts = {"vera": "You are Vera. Be honest and approval-gated."}

    def test_clean_score_no_flags(self):
        chat = _make_chat_with_responses({
            ("prompt auditor", "Agent: vera"): json.dumps({
                "agent": "vera",
                "scores": {
                    "honesty": {"score": 5, "reasoning": "balanced",
                                "flagged": False, "direction": "none"},
                    "approval_gate": {"score": 8, "reasoning": "well above floor",
                                      "flagged": False, "direction": "none"},
                },
                "any_flagged": False,
                "summary": "calibrated",
            }),
        })
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
        )
        report = guardian.score_agent("vera")
        self.assertFalse(report.any_flagged)
        self.assertEqual(len(report.scores), 2)
        self.assertEqual(report.scores[0].score, 5)

    def test_left_drift_flagged(self):
        chat = _make_chat_with_responses({
            ("prompt auditor", "Agent: vera"): json.dumps({
                "agent": "vera",
                "scores": {
                    "honesty": {"score": 2, "reasoning": "brutal", "flagged": True, "direction": "left"},
                    "approval_gate": {"score": 7, "reasoning": "ok", "flagged": False, "direction": "none"},
                },
                "any_flagged": True,
                "summary": "honesty drifted left",
            }),
        })
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
        )
        report = guardian.score_agent("vera")
        self.assertTrue(report.any_flagged)
        flagged = report.flagged_scores()
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0].commandment_id, "honesty")
        self.assertEqual(flagged[0].direction, "left")

    def test_chassis_enforces_flag_decision_not_llm(self):
        """
        The LLM might claim flagged=False even when the score crosses the
        threshold. The chassis must use its own is_flagged() rather than
        trusting the LLM's flag.
        """
        chat = _make_chat_with_responses({
            ("prompt auditor", "Agent: vera"): json.dumps({
                "agent": "vera",
                "scores": {
                    "honesty": {"score": 9, "reasoning": "right drift",
                                "flagged": False,           # LLM lies
                                "direction": "none"},        # LLM lies
                    "approval_gate": {"score": 8, "reasoning": "ok",
                                      "flagged": False, "direction": "none"},
                },
                "any_flagged": False,                          # LLM lies
                "summary": "x",
            }),
        })
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
        )
        report = guardian.score_agent("vera")
        # Chassis correctly flags despite LLM saying not-flagged.
        self.assertTrue(report.any_flagged)
        honesty = next(s for s in report.scores if s.commandment_id == "honesty")
        self.assertTrue(honesty.flagged)
        self.assertEqual(honesty.direction, "right")

    def test_hard_floor_drift_above_min_not_flagged(self):
        chat = _make_chat_with_responses({
            ("prompt auditor", "Agent: vera"): json.dumps({
                "agent": "vera",
                "scores": {
                    "honesty": {"score": 5, "reasoning": "ok", "flagged": False, "direction": "none"},
                    "approval_gate": {"score": 9, "reasoning": "very gated", "flagged": False, "direction": "none"},
                },
                "any_flagged": False,
                "summary": "ok",
            }),
        })
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
        )
        report = guardian.score_agent("vera")
        ag = next(s for s in report.scores if s.commandment_id == "approval_gate")
        self.assertFalse(ag.flagged)  # 9 above min=5 on hard floor → fine

    def test_hard_floor_drift_below_min_flagged(self):
        chat = _make_chat_with_responses({
            ("prompt auditor", "Agent: vera"): json.dumps({
                "agent": "vera",
                "scores": {
                    "honesty": {"score": 5, "reasoning": "ok", "flagged": False, "direction": "none"},
                    "approval_gate": {"score": 3, "reasoning": "skips gate",
                                      "flagged": True, "direction": "left"},
                },
                "any_flagged": True,
                "summary": "approval gate broken",
            }),
        })
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
        )
        report = guardian.score_agent("vera")
        ag = next(s for s in report.scores if s.commandment_id == "approval_gate")
        self.assertTrue(ag.flagged)
        self.assertEqual(ag.direction, "left")

    def test_empty_prompt_raises(self):
        chat = lambda s, u: "{}"
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=lambda a: "",
            chat_completion=chat,
        )
        with self.assertRaises(GuardianError):
            guardian.score_agent("ghost")

    def test_invalid_json_raises(self):
        chat = lambda s, u: "this is not JSON"
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver({"vera": "x"}),
            chat_completion=chat,
        )
        with self.assertRaises(GuardianError):
            guardian.score_agent("vera")

    def test_missing_commandment_in_response_raises(self):
        chat = lambda s, u: json.dumps({
            "agent": "vera",
            "scores": {"honesty": {"score": 5, "reasoning": "x"}},  # no approval_gate
            "any_flagged": False,
            "summary": "",
        })
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver({"vera": "x"}),
            chat_completion=chat,
        )
        with self.assertRaises(GuardianError):
            guardian.score_agent("vera")

    def test_score_out_of_range_raises(self):
        chat = lambda s, u: json.dumps({
            "agent": "vera",
            "scores": {
                "honesty": {"score": 11, "reasoning": "x"},
                "approval_gate": {"score": 6, "reasoning": "x"},
            },
            "any_flagged": True,
            "summary": "x",
        })
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver({"vera": "x"}),
            chat_completion=chat,
        )
        with self.assertRaises(GuardianError):
            guardian.score_agent("vera")

    def test_strips_json_code_fences(self):
        chat = lambda s, u: (
            "```json\n"
            + json.dumps({
                "agent": "vera",
                "scores": {
                    "honesty": {"score": 5, "reasoning": "x"},
                    "approval_gate": {"score": 6, "reasoning": "x"},
                },
                "any_flagged": False,
                "summary": "ok",
            })
            + "\n```"
        )
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver({"vera": "x"}),
            chat_completion=chat,
        )
        report = guardian.score_agent("vera")
        self.assertEqual(len(report.scores), 2)


# ──────────────────────────────────────────────────────────────────────────────
# correct_agent + audit
# ──────────────────────────────────────────────────────────────────────────────

class TestCorrectAndAudit(unittest.TestCase):
    def setUp(self):
        self.prompts = {"vera": "You are Vera. Old prompt."}

    def _flagged_score_response(self, agent: str = "vera") -> str:
        return json.dumps({
            "agent": agent,
            "scores": {
                "honesty": {"score": 2, "reasoning": "brutal",
                            "flagged": True, "direction": "left"},
                "approval_gate": {"score": 6, "reasoning": "ok",
                                  "flagged": False, "direction": "none"},
            },
            "any_flagged": True,
            "summary": "honesty drifted left toward brutal",
        })

    def _clean_score_response(self, agent: str = "vera") -> str:
        return json.dumps({
            "agent": agent,
            "scores": {
                "honesty": {"score": 5, "reasoning": "ok",
                            "flagged": False, "direction": "none"},
                "approval_gate": {"score": 7, "reasoning": "ok",
                                  "flagged": False, "direction": "none"},
            },
            "any_flagged": False,
            "summary": "calibrated",
        })

    def test_correct_returns_none_when_not_flagged(self):
        chat = lambda s, u: self._clean_score_response()
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
            correction_system="(unused)",
        )
        report = guardian.score_agent("vera")
        self.assertIsNone(guardian.correct_agent("vera", report))

    def test_correct_returns_none_when_no_correction_system(self):
        chat = lambda s, u: self._flagged_score_response()
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
            correction_system=None,    # not configured
        )
        report = guardian.score_agent("vera")
        self.assertIsNone(guardian.correct_agent("vera", report))

    def test_correct_returns_string_when_flagged(self):
        def chat(system, user):
            if "auditor" in system.lower() or "audit" in system.lower() \
                    or "score" in system.lower():
                return self._flagged_score_response()
            else:
                return "You are Vera. Corrected prompt."
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
            correction_system="You are a corrector.",
        )
        report = guardian.score_agent("vera")
        corrected = guardian.correct_agent("vera", report)
        self.assertEqual(corrected, "You are Vera. Corrected prompt.")

    def test_audit_queues_correction_via_approval_queue(self):
        def chat(system, user):
            if "auditor" in system or "score" in system:
                return self._flagged_score_response("vera")
            return "You are Vera. Corrected."
        queue = ApprovalQueue(
            store=InMemoryStore(),
            executors={},
        )
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
            correction_system="You are a corrector.",
            approval_queue=queue,
        )
        result = guardian.audit(["vera"])
        self.assertEqual(result["agents_audited"], 1)
        self.assertEqual(result["agents_flagged"], 1)
        self.assertEqual(result["corrections_queued"], 1)
        pending = queue.list_pending()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].type, "prompt_correction")
        self.assertEqual(pending[0].payload["agent"], "vera")
        self.assertIn("Corrected", pending[0].payload["corrected_prompt"])

    def test_audit_clean_agent_no_correction(self):
        chat = lambda s, u: self._clean_score_response("vera")
        queue = ApprovalQueue(store=InMemoryStore())
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
            correction_system="(unused)",
            approval_queue=queue,
        )
        result = guardian.audit(["vera"])
        self.assertEqual(result["agents_flagged"], 0)
        self.assertEqual(result["corrections_queued"], 0)
        self.assertEqual(queue.list_pending(), [])

    def test_audit_handles_scoring_errors(self):
        def chat(system, user):
            raise RuntimeError("LLM down")
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
        )
        result = guardian.audit(["vera", "rex"])
        self.assertEqual(result["agents_audited"], 2)
        self.assertEqual(result["scoring_errors"], 2)
        for entry in result["results"]:
            self.assertEqual(entry["status"], "error")

    def test_audit_handles_correction_errors_gracefully(self):
        call_count = {"n": 0}
        def chat(system, user):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return self._flagged_score_response("vera")
            raise RuntimeError("correction LLM down")
        queue = ApprovalQueue(store=InMemoryStore())
        guardian = PromptGuardian(
            product_name="TP", commandments=ALL_CMDS,
            prompt_resolver=_make_resolver(self.prompts),
            chat_completion=chat,
            correction_system="(corrector)",
            approval_queue=queue,
        )
        result = guardian.audit(["vera"])
        # Scoring succeeded; correction failed; no crash.
        self.assertEqual(result["agents_flagged"], 1)
        self.assertEqual(result["corrections_queued"], 0)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.CRITICAL)
    unittest.main(verbosity=2)
