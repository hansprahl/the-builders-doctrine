"""
Tests for kit/chassis/specialists.py.

Run with:  python3 kit/chassis/test_specialists.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kit.chassis.specialists import Specialist, SpecialistRegistry


def _runner_for(name: str):
    def _run(query: str) -> str:
        return f"[{name}] {query}"
    return _run


class TestSpecialistDataclass(unittest.TestCase):
    def test_valid_construction(self):
        s = Specialist(name="vera", description="schedule", run=_runner_for("vera"))
        self.assertEqual(s.name, "vera")
        self.assertEqual(s.description, "schedule")
        self.assertEqual(s.roles, frozenset({"user", "admin"}))

    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            Specialist(name="", description="x", run=lambda q: q)
        with self.assertRaises(ValueError):
            Specialist(name="   ", description="x", run=lambda q: q)

    def test_invalid_name_format_rejected(self):
        # Uppercase, leading digit, or special chars — all rejected.
        for bad in ("Vera", "1vera", "vera-1", "ask vera", "vera!"):
            with self.assertRaises(ValueError, msg=f"expected reject: {bad!r}"):
                Specialist(name=bad, description="x", run=lambda q: q)

    def test_empty_description_rejected(self):
        with self.assertRaises(ValueError):
            Specialist(name="vera", description="", run=lambda q: q)

    def test_non_callable_run_rejected(self):
        with self.assertRaises(ValueError):
            Specialist(name="vera", description="x", run="not callable")

    def test_empty_roles_rejected(self):
        with self.assertRaises(ValueError):
            Specialist(name="vera", description="x", run=lambda q: q,
                       roles=frozenset())

    def test_custom_roles(self):
        s = Specialist(name="forge", description="dev",
                       run=_runner_for("forge"),
                       roles=frozenset({"admin"}))
        self.assertEqual(s.roles, frozenset({"admin"}))


class TestRegistryRegistration(unittest.TestCase):
    def setUp(self):
        self.reg = SpecialistRegistry()

    def test_register_then_get(self):
        s = Specialist(name="vera", description="schedule", run=_runner_for("vera"))
        self.reg.register(s)
        self.assertEqual(self.reg.get("vera"), s)
        self.assertTrue(self.reg.has("vera"))

    def test_get_unknown_raises(self):
        with self.assertRaises(KeyError):
            self.reg.get("nonexistent")

    def test_duplicate_name_rejected(self):
        s1 = Specialist(name="vera", description="schedule", run=_runner_for("v1"))
        s2 = Specialist(name="vera", description="other", run=_runner_for("v2"))
        self.reg.register(s1)
        with self.assertRaises(ValueError):
            self.reg.register(s2)

    def test_unregister(self):
        s = Specialist(name="vera", description="schedule", run=_runner_for("vera"))
        self.reg.register(s)
        self.reg.unregister("vera")
        self.assertFalse(self.reg.has("vera"))
        # Unregistering a nonexistent name is a no-op.
        self.reg.unregister("nonexistent")

    def test_names_sorted(self):
        for n in ("scout", "vera", "atlas", "rex"):
            self.reg.register(Specialist(
                name=n, description=f"{n} scope", run=_runner_for(n),
            ))
        self.assertEqual(self.reg.names(), ["atlas", "rex", "scout", "vera"])


class TestRoleFiltering(unittest.TestCase):
    def setUp(self):
        self.reg = SpecialistRegistry()
        self.reg.register(Specialist(
            name="vera", description="schedule",
            run=_runner_for("vera"),
            roles=frozenset({"user", "admin"}),
        ))
        self.reg.register(Specialist(
            name="forge", description="dev",
            run=_runner_for("forge"),
            roles=frozenset({"admin"}),
        ))

    def test_user_role_excludes_admin_only(self):
        names = [s.name for s in self.reg.list_for_role("user")]
        self.assertEqual(names, ["vera"])

    def test_admin_role_sees_all(self):
        names = [s.name for s in self.reg.list_for_role("admin")]
        self.assertEqual(names, ["forge", "vera"])

    def test_unknown_role_returns_empty(self):
        self.assertEqual(self.reg.list_for_role("nonexistent"), [])

    def test_make_tools_user_role(self):
        tools = self.reg.make_tools(role="user")
        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0].__name__, "ask_vera")

    def test_make_tools_admin_role(self):
        tools = self.reg.make_tools(role="admin")
        names = sorted(t.__name__ for t in tools)
        self.assertEqual(names, ["ask_forge", "ask_vera"])


class TestInvocation(unittest.TestCase):
    def setUp(self):
        self.reg = SpecialistRegistry()
        self.reg.register(Specialist(
            name="vera", description="schedule", run=_runner_for("vera"),
        ))

    def test_call_invokes_run(self):
        result = self.reg.call("vera", "hello")
        self.assertEqual(result, "[vera] hello")

    def test_call_unknown_raises(self):
        with self.assertRaises(KeyError):
            self.reg.call("nonexistent", "x")

    def test_make_tools_returns_callable_with_correct_doc(self):
        tools = self.reg.make_tools(role="user")
        ask_vera = tools[0]
        self.assertEqual(ask_vera("hello"), "[vera] hello")
        self.assertIn("Vera", ask_vera.__doc__)
        self.assertIn("schedule", ask_vera.__doc__)


class TestConfidenceCapture(unittest.TestCase):
    def test_capture_wraps_response(self):
        captures = []
        def capture(name, query, raw):
            captures.append((name, query, raw))
            return raw + " [captured]"

        reg = SpecialistRegistry(confidence_capture=capture)
        reg.register(Specialist(
            name="vera", description="schedule", run=_runner_for("vera"),
        ))
        result = reg.call("vera", "hello")
        self.assertEqual(result, "[vera] hello [captured]")
        self.assertEqual(captures, [("vera", "hello", "[vera] hello")])

    def test_capture_failure_returns_raw(self):
        def boom(name, query, raw):
            raise RuntimeError("capture failed")
        reg = SpecialistRegistry(confidence_capture=boom)
        reg.register(Specialist(
            name="vera", description="schedule", run=_runner_for("vera"),
        ))
        # Capture failure must not propagate — raw is returned.
        result = reg.call("vera", "hello")
        self.assertEqual(result, "[vera] hello")


class TestNoLeakValidator(unittest.TestCase):
    def setUp(self):
        self.reg = SpecialistRegistry()
        for n in ("vera", "rex", "forge"):
            self.reg.register(Specialist(
                name=n, description=f"{n} scope", run=_runner_for(n),
            ))

    def test_clean_text_returns_empty(self):
        leaks = self.reg.validate_no_leak("Your meeting is at 3pm.")
        self.assertEqual(leaks, [])

    def test_detects_leak(self):
        leaks = self.reg.validate_no_leak("Let me ask Vera to check.")
        self.assertEqual(leaks, ["vera"])

    def test_detects_multiple_leaks(self):
        leaks = self.reg.validate_no_leak("Vera and Rex both reported back.")
        self.assertEqual(leaks, ["rex", "vera"])

    def test_word_boundary_avoids_false_positive(self):
        # "verandah" contains "vera" but is not a leak.
        leaks = self.reg.validate_no_leak("The verandah is finished.")
        self.assertEqual(leaks, [])

    def test_ignore_list(self):
        # Forge is also a common English word — caller may ignore it.
        leaks = self.reg.validate_no_leak(
            "The blacksmith ran the forge.",
            ignore={"forge"},
        )
        self.assertEqual(leaks, [])


class TestScopeOverlapDiagnostic(unittest.TestCase):
    def test_overlapping_scopes_surfaced(self):
        reg = SpecialistRegistry()
        reg.register(Specialist(
            name="vera", description="schedule, calendar, tasks, planning",
            run=_runner_for("vera"),
        ))
        reg.register(Specialist(
            name="atlas", description="finance, balances, transactions",
            run=_runner_for("atlas"),
        ))
        reg.register(Specialist(
            name="scout", description="habits, journal, tasks, planning",
            run=_runner_for("scout"),
        ))
        overlaps = reg.find_overlapping_scopes()
        # vera and scout share "tasks" and "planning"
        pairs_with_words = {(a, b, w) for (a, b, w) in overlaps
                            if {a, b} == {"scout", "vera"}}
        self.assertIn(("scout", "vera", "tasks"), pairs_with_words)
        self.assertIn(("scout", "vera", "planning"), pairs_with_words)

    def test_no_overlaps_returns_empty(self):
        reg = SpecialistRegistry()
        reg.register(Specialist(
            name="vera", description="calendar tasks reminders",
            run=_runner_for("vera"),
        ))
        reg.register(Specialist(
            name="atlas", description="finance balances spending",
            run=_runner_for("atlas"),
        ))
        self.assertEqual(reg.find_overlapping_scopes(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
