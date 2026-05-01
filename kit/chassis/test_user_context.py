"""
Tests for kit/chassis/user_context.py.

Run with:  python3 kit/chassis/test_user_context.py
"""

from __future__ import annotations

import asyncio
import shutil
import sys
import tempfile
import threading
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kit.chassis.user_context import UserContext


class TestCoreGetSet(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.ctx = UserContext(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_get_without_set_raises_lookup_error(self):
        # The crash is the doctrine. Catching LookupError here would
        # contradict the rationale TOP carries in its source comment.
        with self.assertRaises(LookupError):
            self.ctx.get()

    def test_set_then_get_returns_value(self):
        self.ctx.set("hans")
        self.assertEqual(self.ctx.get(), "hans")

    def test_set_empty_string_rejected(self):
        with self.assertRaises(ValueError):
            self.ctx.set("")

    def test_set_non_string_rejected(self):
        with self.assertRaises(ValueError):
            self.ctx.set(None)
        with self.assertRaises(ValueError):
            self.ctx.set(42)

    def test_get_or_none_without_set(self):
        self.assertIsNone(self.ctx.get_or_none())

    def test_get_or_none_after_set(self):
        self.ctx.set("hans")
        self.assertEqual(self.ctx.get_or_none(), "hans")

    def test_is_set_reflects_state(self):
        self.assertFalse(self.ctx.is_set())
        self.ctx.set("hans")
        self.assertTrue(self.ctx.is_set())


class TestScope(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.ctx = UserContext(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_scope_binds_within_block(self):
        with self.ctx.scope("hans"):
            self.assertEqual(self.ctx.get(), "hans")

    def test_scope_restores_unset_state_on_exit(self):
        with self.ctx.scope("hans"):
            pass
        with self.assertRaises(LookupError):
            self.ctx.get()

    def test_scope_restores_prior_value_on_exit(self):
        self.ctx.set("alpha")
        with self.ctx.scope("beta"):
            self.assertEqual(self.ctx.get(), "beta")
        self.assertEqual(self.ctx.get(), "alpha")

    def test_nested_scopes(self):
        with self.ctx.scope("alpha"):
            with self.ctx.scope("beta"):
                self.assertEqual(self.ctx.get(), "beta")
            self.assertEqual(self.ctx.get(), "alpha")
        with self.assertRaises(LookupError):
            self.ctx.get()

    def test_scope_restores_on_exception(self):
        try:
            with self.ctx.scope("hans"):
                raise RuntimeError("boom")
        except RuntimeError:
            pass
        # Even on exception, scope must reset.
        with self.assertRaises(LookupError):
            self.ctx.get()


class TestThreadIsolation(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.ctx = UserContext(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_threads_have_isolated_values(self):
        """
        ContextVars do NOT propagate to threads created after a set().
        The child thread sees the unset state — which is the right
        behavior: every thread is its own entry point and must set
        its own user.
        """
        self.ctx.set("main_user")

        seen = {}

        def worker(name: str, user_to_set: str):
            # Child thread starts with no user (correct).
            seen[(name, "before_set")] = self.ctx.get_or_none()
            self.ctx.set(user_to_set)
            seen[(name, "after_set")] = self.ctx.get()

        t1 = threading.Thread(target=worker, args=("t1", "thread_one"))
        t2 = threading.Thread(target=worker, args=("t2", "thread_two"))
        t1.start(); t2.start(); t1.join(); t2.join()

        # Each thread sees only its own value.
        self.assertIsNone(seen[("t1", "before_set")])
        self.assertIsNone(seen[("t2", "before_set")])
        self.assertEqual(seen[("t1", "after_set")], "thread_one")
        self.assertEqual(seen[("t2", "after_set")], "thread_two")

        # Main thread is unaffected by either child thread.
        self.assertEqual(self.ctx.get(), "main_user")


class TestAsyncIsolation(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.ctx = UserContext(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_async_tasks_have_isolated_values(self):
        """
        ContextVars in asyncio: parent context is COPIED into a child task
        at creation time. Mutations in the child do NOT leak back to the
        parent or to sibling tasks.
        """
        async def task(name: str, user_to_set: str, report: list):
            report.append((name, "start", self.ctx.get_or_none()))
            self.ctx.set(user_to_set)
            await asyncio.sleep(0)  # yield to other tasks
            report.append((name, "end", self.ctx.get()))

        async def main():
            self.ctx.set("parent_user")
            report = []
            await asyncio.gather(
                task("a", "user_a", report),
                task("b", "user_b", report),
            )
            return report, self.ctx.get()

        report, parent_after = asyncio.run(main())

        # Each task starts with the parent's value (copy-on-spawn).
        starts = {n: v for (n, evt, v) in report if evt == "start"}
        self.assertEqual(starts["a"], "parent_user")
        self.assertEqual(starts["b"], "parent_user")

        # Each task ends with its own value.
        ends = {n: v for (n, evt, v) in report if evt == "end"}
        self.assertEqual(ends["a"], "user_a")
        self.assertEqual(ends["b"], "user_b")

        # Parent is unaffected by either child task.
        self.assertEqual(parent_after, "parent_user")


class TestDataPath(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.ctx = UserContext(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_data_path_without_user_raises(self):
        with self.assertRaises(LookupError):
            self.ctx.data_path("journal.json")

    def test_data_path_layout(self):
        self.ctx.set("hans")
        p = self.ctx.data_path("journal.json")
        self.assertEqual(p, self.tmp / "users" / "hans" / "journal.json")

    def test_data_path_creates_parent_directory(self):
        self.ctx.set("hans")
        p = self.ctx.data_path("nested", "subdir", "file.json")
        self.assertTrue(p.parent.exists())
        self.assertTrue(p.parent.is_dir())

    def test_user_dir(self):
        self.ctx.set("hans")
        d = self.ctx.user_dir()
        self.assertEqual(d, self.tmp / "users" / "hans")
        self.assertTrue(d.exists())

    def test_users_subdir_override(self):
        ctx = UserContext(self.tmp, users_subdir="tenants")
        ctx.set("acme")
        p = ctx.data_path("config.json")
        self.assertEqual(p, self.tmp / "tenants" / "acme" / "config.json")


class TestMultipleInstances(unittest.TestCase):
    """Two UserContexts must not share state — important for tests and for
    products that run side-by-side in the same process (e.g., a multi-product
    server)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_independent_contexts(self):
        a = UserContext(self.tmp)
        b = UserContext(self.tmp)
        a.set("user_a")
        with self.assertRaises(LookupError):
            b.get()
        self.assertEqual(a.get(), "user_a")
        b.set("user_b")
        self.assertEqual(a.get(), "user_a")
        self.assertEqual(b.get(), "user_b")


if __name__ == "__main__":
    unittest.main(verbosity=2)
