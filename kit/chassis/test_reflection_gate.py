"""
Tests for kit/chassis/reflection_gate.py.

Run with:  python3 -m pytest kit/chassis/test_reflection_gate.py -v
or:        python3 kit/chassis/test_reflection_gate.py

The tests verify the doctrine invariants the module preserves:
  - Scope-aware refusal (founder, wellness)
  - K/I/G evaluation logic
  - Confident-zero-gaps failure-mode detection (Principle #12's core)
  - Uncertainty-acknowledged honored as 'proceed' signal
  - LLM-independent chassis (reflector is caller-supplied)
  - Gaps surface as RFI-compatible candidates
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

# Ensure repo root is importable when running this file directly.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kit.chassis.reflection_gate import (
    ReflectionGate,
    ReflectionResult,
    ReflectorResponse,
    parse_reflector_response,
    _infer_scope_from_body,
)


# ──────────────────────────────────────────────────────────────────────────────
# Construction
# ──────────────────────────────────────────────────────────────────────────────


class TestConstruction(unittest.TestCase):
    def test_rejects_invalid_scope(self):
        with self.assertRaises(ValueError):
            ReflectionGate(scope="invalid_scope")  # type: ignore[arg-type]

    def test_accepts_valid_scopes(self):
        for scope in ("operator_tool", "wellness", "founder"):
            gate = ReflectionGate(scope=scope)  # type: ignore[arg-type]
            self.assertEqual(gate.scope, scope)

    def test_doctrinal_questions_stored_as_tuple(self):
        gate = ReflectionGate(
            scope="operator_tool",
            doctrinal_questions=["a", "b"],  # type: ignore[arg-type]
        )
        self.assertEqual(gate.doctrinal_questions, ("a", "b"))


# ──────────────────────────────────────────────────────────────────────────────
# Founder scope: hard refusal
# ──────────────────────────────────────────────────────────────────────────────


class TestFounderScope(unittest.TestCase):
    def test_founder_scope_refuses_always(self):
        gate = ReflectionGate(scope="founder")
        result = gate.evaluate(draft="anything", context={})
        self.assertEqual(result.recommendation, "refuse")
        self.assertIn("founder is not the subject", result.refusal_reason)

    def test_founder_refusal_does_not_call_reflector(self):
        reflector = MagicMock()
        gate = ReflectionGate(scope="founder", reflector=reflector)
        gate.evaluate(draft="anything", context={})
        reflector.assert_not_called()

    def test_founder_prompt_is_a_refusal(self):
        gate = ReflectionGate(scope="founder")
        prompt = gate.build_reflection_prompt(draft="x", context={})
        self.assertIn("REFUSED", prompt)


# ──────────────────────────────────────────────────────────────────────────────
# Wellness scope: refuse user-facing extraction
# ──────────────────────────────────────────────────────────────────────────────


class TestWellnessScope(unittest.TestCase):
    def test_wellness_refuses_user_facing_extraction(self):
        gate = ReflectionGate(scope="wellness")
        result = gate.evaluate(
            draft="user's journal entry",
            context={"target_user_id": "u123"},
        )
        self.assertEqual(result.recommendation, "refuse")
        self.assertIn("surveillance shape", result.refusal_reason)

    def test_wellness_inverted_mode_proceeds(self):
        # In inverted mode the gate is helping the user self-reflect, not
        # extracting from them. The gate must not refuse, but it does
        # need a reflector to evaluate the prompt response.
        reflector = MagicMock(
            return_value=ReflectorResponse(
                known=(), inferred=(), gaps=(),
                uncertainty_acknowledged=True,
            )
        )
        gate = ReflectionGate(scope="wellness", reflector=reflector)
        result = gate.evaluate(
            draft="conversation context",
            context={
                "target_user_id": "u123",
                "inverted_user_self_reflection": True,
            },
        )
        # Should proceed (uncertainty acknowledged, no gaps)
        self.assertEqual(result.recommendation, "proceed")

    def test_wellness_prompt_is_inverted(self):
        gate = ReflectionGate(scope="wellness")
        prompt = gate.build_reflection_prompt(draft="ctx", context={})
        self.assertIn("INVERTED", prompt)
        self.assertIn("offered, not pressed", prompt)


# ──────────────────────────────────────────────────────────────────────────────
# Operator-tool scope: K/I/G evaluation
# ──────────────────────────────────────────────────────────────────────────────


class TestOperatorToolScope(unittest.TestCase):
    def test_gaps_present_returns_iterate(self):
        response = ReflectorResponse(
            known=("vote count: 27/28",),
            inferred=("opposition will refile by primary",),
            gaps=("Helton's tax-vote direction unconfirmed",),
            uncertainty_acknowledged=True,
        )
        gate = ReflectionGate(scope="operator_tool", reflector=lambda p, d: response)
        result = gate.evaluate(draft="draft", context={"echelon": "PL"})
        self.assertEqual(result.recommendation, "iterate")
        self.assertEqual(
            result.gaps,
            ("Helton's tax-vote direction unconfirmed",),
        )
        self.assertTrue(result.uncertainty_acknowledged)

    def test_no_gaps_with_uncertainty_returns_proceed(self):
        response = ReflectorResponse(
            known=("vote count: 27/28",),
            inferred=(),
            gaps=(),
            uncertainty_acknowledged=True,
        )
        gate = ReflectionGate(scope="operator_tool", reflector=lambda p, d: response)
        result = gate.evaluate(draft="draft", context={})
        self.assertEqual(result.recommendation, "proceed")
        self.assertEqual(result.gaps, ())

    def test_confident_zero_gaps_returns_iterate(self):
        """The Principle #12 core test: confident-zero-gaps is a failure mode."""
        response = ReflectorResponse(
            known=("everything is fine",),
            inferred=(),
            gaps=(),
            uncertainty_acknowledged=False,
        )
        gate = ReflectionGate(scope="operator_tool", reflector=lambda p, d: response)
        result = gate.evaluate(draft="draft", context={})
        self.assertEqual(result.recommendation, "iterate")
        # iterate_reason names the Principle #12 failure mode
        self.assertIn("Principle #12", result.iterate_reason)
        self.assertIn("zero-gaps", result.iterate_reason.lower())
        # The structural-gap message goes in the gaps list
        self.assertEqual(len(result.gaps), 1)
        self.assertIn("structural", result.gaps[0])

    def test_confident_zero_gaps_can_be_disabled(self):
        response = ReflectorResponse(
            known=(), inferred=(), gaps=(),
            uncertainty_acknowledged=False,
        )
        gate = ReflectionGate(
            scope="operator_tool",
            reflector=lambda p, d: response,
            require_uncertainty_on_zero_gaps=False,
        )
        result = gate.evaluate(draft="draft", context={})
        self.assertEqual(result.recommendation, "proceed")

    def test_evaluate_without_reflector_raises(self):
        gate = ReflectionGate(scope="operator_tool", reflector=None)
        with self.assertRaises(ValueError) as ctx:
            gate.evaluate(draft="draft", context={})
        self.assertIn("no reflector configured", str(ctx.exception))

    def test_evaluate_with_response_skips_reflector(self):
        response = ReflectorResponse(
            known=("x",), inferred=(), gaps=("y",),
            uncertainty_acknowledged=True,
        )
        gate = ReflectionGate(scope="operator_tool", reflector=None)
        result = gate.evaluate_with_response(response)
        self.assertEqual(result.recommendation, "iterate")
        self.assertEqual(result.gaps, ("y",))


# ──────────────────────────────────────────────────────────────────────────────
# Prompt construction
# ──────────────────────────────────────────────────────────────────────────────


class TestPromptConstruction(unittest.TestCase):
    def test_operator_tool_prompt_includes_kig_structure(self):
        gate = ReflectionGate(scope="operator_tool")
        prompt = gate.build_reflection_prompt(draft="x", context={})
        for marker in ("KNOWN:", "INFERRED:", "GAPS:", "UNCERTAINTY:"):
            self.assertIn(marker, prompt)

    def test_prompt_includes_echelon_when_provided(self):
        gate = ReflectionGate(scope="operator_tool")
        prompt = gate.build_reflection_prompt(
            draft="x", context={"echelon": "PL"}
        )
        self.assertIn("PL tier", prompt)

    def test_prompt_includes_doctrinal_questions(self):
        gate = ReflectionGate(
            scope="operator_tool",
            doctrinal_questions=(
                "Have you verified vote count?",
                "Have you checked the filing deadline?",
            ),
        )
        prompt = gate.build_reflection_prompt(draft="x", context={})
        self.assertIn("vote count", prompt)
        self.assertIn("filing deadline", prompt)

    def test_prompt_includes_draft(self):
        gate = ReflectionGate(scope="operator_tool")
        prompt = gate.build_reflection_prompt(
            draft="THE_SPECIFIC_DRAFT_TEXT", context={}
        )
        self.assertIn("THE_SPECIFIC_DRAFT_TEXT", prompt)


# ──────────────────────────────────────────────────────────────────────────────
# Response parsing
# ──────────────────────────────────────────────────────────────────────────────


class TestParseReflectorResponse(unittest.TestCase):
    def test_parses_full_response(self):
        raw = (
            "KNOWN:\n"
            "  - Taylor won 27/28 delegates\n"
            "  - Assembly was 2026-03-28\n"
            "INFERRED:\n"
            "  - Opposition lacks ground game\n"
            "GAPS:\n"
            "  - Helton's tax-vote direction unconfirmed\n"
            "  - Filing deadline impact unverified\n"
            "UNCERTAINTY: yes\n"
        )
        response = parse_reflector_response(raw)
        self.assertEqual(
            response.known,
            ("Taylor won 27/28 delegates", "Assembly was 2026-03-28"),
        )
        self.assertEqual(
            response.inferred, ("Opposition lacks ground game",)
        )
        self.assertEqual(
            response.gaps,
            (
                "Helton's tax-vote direction unconfirmed",
                "Filing deadline impact unverified",
            ),
        )
        self.assertTrue(response.uncertainty_acknowledged)

    def test_parses_uncertainty_no(self):
        raw = (
            "KNOWN:\n  - x\n"
            "INFERRED:\n"
            "GAPS:\n"
            "UNCERTAINTY: no\n"
        )
        response = parse_reflector_response(raw)
        self.assertFalse(response.uncertainty_acknowledged)

    def test_missing_uncertainty_defaults_false(self):
        raw = "KNOWN:\n  - x\nINFERRED:\nGAPS:\n"
        response = parse_reflector_response(raw)
        self.assertFalse(response.uncertainty_acknowledged)


# ──────────────────────────────────────────────────────────────────────────────
# Scope inference (for from_kit_template)
# ──────────────────────────────────────────────────────────────────────────────


class TestScopeInference(unittest.TestCase):
    def test_infers_operator_tool(self):
        body = "This product is in operator_tool scope. Standard gate applies."
        self.assertEqual(_infer_scope_from_body(body), "operator_tool")

    def test_infers_wellness(self):
        body = "TOP is wellness-shaped. The gate inverts to user self-reflection."
        self.assertEqual(_infer_scope_from_body(body), "wellness")

    def test_explicit_scope_declaration_wins(self):
        body = "scope: operator_tool. Wellness keywords elsewhere are noise."
        self.assertEqual(_infer_scope_from_body(body), "operator_tool")

    def test_unknown_scope_returns_none(self):
        body = "Lorem ipsum dolor sit amet."
        self.assertIsNone(_infer_scope_from_body(body))


# ──────────────────────────────────────────────────────────────────────────────
# Audit record
# ──────────────────────────────────────────────────────────────────────────────


class TestAuditRecord(unittest.TestCase):
    def test_to_audit_record_is_json_serializable(self):
        result = ReflectionResult(
            recommendation="iterate",
            gaps=("gap one", "gap two"),
            uncertainty_acknowledged=True,
            iterate_reason="reflection found gaps",
            scope="operator_tool",
        )
        record = result.to_audit_record()
        # Round-trip through JSON proves serializability.
        s = json.dumps(record)
        back = json.loads(s)
        self.assertEqual(back["recommendation"], "iterate")
        self.assertEqual(back["gaps"], ["gap one", "gap two"])
        self.assertTrue(back["uncertainty_acknowledged"])
        self.assertEqual(back["scope"], "operator_tool")
        self.assertIn("timestamp", back)


# ──────────────────────────────────────────────────────────────────────────────
# Reflector callback integration
# ──────────────────────────────────────────────────────────────────────────────


class TestReflectorIntegration(unittest.TestCase):
    def test_reflector_receives_prompt_and_draft(self):
        captured: dict = {}

        def my_reflector(prompt: str, draft: str) -> ReflectorResponse:
            captured["prompt"] = prompt
            captured["draft"] = draft
            return ReflectorResponse(
                known=("k",), inferred=(), gaps=(),
                uncertainty_acknowledged=True,
            )

        gate = ReflectionGate(scope="operator_tool", reflector=my_reflector)
        gate.evaluate(draft="THE_DRAFT", context={"echelon": "SL"})

        self.assertIn("KNOWN:", captured["prompt"])
        self.assertEqual(captured["draft"], "THE_DRAFT")
        self.assertIn("SL tier", captured["prompt"])

    def test_reflector_response_preserved_in_result(self):
        response = ReflectorResponse(
            known=("k",), inferred=("i",), gaps=("g",),
            uncertainty_acknowledged=True,
            raw="raw-llm-output",
        )
        gate = ReflectionGate(scope="operator_tool",
                              reflector=lambda p, d: response)
        result = gate.evaluate(draft="x", context={})
        self.assertIs(result.reflector_response, response)
        self.assertEqual(result.reflector_response.raw, "raw-llm-output")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    unittest.main(verbosity=2)
