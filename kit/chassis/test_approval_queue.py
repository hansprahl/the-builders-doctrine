"""
Tests for kit/chassis/approval_queue.py.

Run with:  python3 kit/chassis/test_approval_queue.py
"""

from __future__ import annotations

import sys
import threading
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kit.chassis.approval_queue import (
    Action,
    ApprovalQueue,
    InMemoryStore,
    JsonFileStore,
    PENDING, APPROVED, REJECTED, EXECUTED, FAILED,
)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers used across tests
# ──────────────────────────────────────────────────────────────────────────────

def echo_executor(action: Action) -> str:
    return f"executed {action.type} for {action.payload.get('to', '?')}"


def boom_executor(action: Action) -> str:
    raise RuntimeError("simulated failure")


# ──────────────────────────────────────────────────────────────────────────────
# Queue + transitions
# ──────────────────────────────────────────────────────────────────────────────

class TestQueueAndApprove(unittest.TestCase):
    def setUp(self):
        self.queue = ApprovalQueue(
            store=InMemoryStore(),
            executors={"send_email": echo_executor},
        )

    def test_queue_creates_pending_action(self):
        a = self.queue.queue("send_email", "test", {"to": "x@y.com"})
        self.assertEqual(a.status, PENDING)
        self.assertEqual(a.type, "send_email")
        self.assertEqual(a.summary, "test")
        self.assertEqual(a.payload, {"to": "x@y.com"})
        self.assertIsNotNone(a.created_at)
        self.assertIsNone(a.resolved_at)
        self.assertEqual(len(a.id), 8)

    def test_list_pending_returns_only_pending(self):
        a = self.queue.queue("send_email", "1", {"to": "a"})
        b = self.queue.queue("send_email", "2", {"to": "b"})
        self.queue.reject(a.id)
        pending = self.queue.list_pending()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].id, b.id)

    def test_approve_with_auto_execute_runs_executor(self):
        a = self.queue.queue("send_email", "test", {"to": "x@y.com"})
        result = self.queue.approve(a.id)
        self.assertEqual(result.status, EXECUTED)
        self.assertIn("executed send_email", result.result)
        self.assertIsNotNone(result.resolved_at)

    def test_approve_persists_through_store(self):
        a = self.queue.queue("send_email", "test", {"to": "x@y.com"})
        self.queue.approve(a.id)
        # Fresh fetch should see the updated state.
        again = self.queue.get(a.id)
        self.assertEqual(again.status, EXECUTED)

    def test_reject_marks_terminal_no_executor_called(self):
        called = []
        queue = ApprovalQueue(
            store=InMemoryStore(),
            executors={"x": lambda a: called.append(a) or "ok"},
        )
        a = queue.queue("x", "summary", {})
        queue.reject(a.id)
        self.assertFalse(called)
        self.assertEqual(queue.get(a.id).status, REJECTED)

    def test_approve_missing_action_raises(self):
        with self.assertRaises(ValueError):
            self.queue.approve("nonexistent")

    def test_approve_already_terminal_raises(self):
        a = self.queue.queue("send_email", "test", {"to": "x"})
        self.queue.reject(a.id)
        with self.assertRaises(ValueError):
            self.queue.approve(a.id)

    def test_clear_resolved(self):
        a = self.queue.queue("send_email", "1", {"to": "a"})
        b = self.queue.queue("send_email", "2", {"to": "b"})
        c = self.queue.queue("send_email", "3", {"to": "c"})
        self.queue.approve(a.id)   # → executed
        self.queue.reject(b.id)    # → rejected
        # c stays pending
        removed = self.queue.clear_resolved()
        self.assertEqual(removed, 2)
        self.assertEqual(len(self.queue.list_pending()), 1)


# ──────────────────────────────────────────────────────────────────────────────
# Two-phase mode (Operator-style)
# ──────────────────────────────────────────────────────────────────────────────

class TestTwoPhaseMode(unittest.TestCase):
    def setUp(self):
        self.queue = ApprovalQueue(
            store=InMemoryStore(),
            executors={"payment": echo_executor},
            auto_execute_on_approve=False,
        )

    def test_approve_stops_at_approved(self):
        a = self.queue.queue("payment", "send $50", {"to": "x"})
        result = self.queue.approve(a.id)
        self.assertEqual(result.status, APPROVED)
        self.assertIsNone(result.result)

    def test_explicit_execute_runs_executor(self):
        a = self.queue.queue("payment", "send $50", {"to": "x"})
        self.queue.approve(a.id)
        result = self.queue.execute(a.id)
        self.assertEqual(result.status, EXECUTED)
        self.assertIn("executed payment", result.result)

    def test_execute_on_pending_raises(self):
        a = self.queue.queue("payment", "send $50", {"to": "x"})
        with self.assertRaises(ValueError):
            self.queue.execute(a.id)

    def test_execute_on_executed_raises(self):
        a = self.queue.queue("payment", "send $50", {"to": "x"})
        self.queue.approve(a.id)
        self.queue.execute(a.id)
        with self.assertRaises(ValueError):
            self.queue.execute(a.id)


# ──────────────────────────────────────────────────────────────────────────────
# Failure handling
# ──────────────────────────────────────────────────────────────────────────────

class TestExecutorFailures(unittest.TestCase):
    def test_executor_exception_marks_failed(self):
        queue = ApprovalQueue(
            store=InMemoryStore(),
            executors={"x": boom_executor},
        )
        a = queue.queue("x", "test", {})
        result = queue.approve(a.id)
        self.assertEqual(result.status, FAILED)
        self.assertIn("simulated failure", result.error)

    def test_no_executor_marks_failed_with_clear_message(self):
        queue = ApprovalQueue(
            store=InMemoryStore(),
            executors={},
        )
        a = queue.queue("unknown_type", "test", {})
        result = queue.approve(a.id)
        self.assertEqual(result.status, FAILED)
        self.assertIn("no executor registered", result.error)
        self.assertIn("unknown_type", result.error)


# ──────────────────────────────────────────────────────────────────────────────
# Auto-execute (admin fast-path)
# ──────────────────────────────────────────────────────────────────────────────

class TestAutoExecuteTypes(unittest.TestCase):
    def test_auto_execute_bypasses_queue(self):
        queue = ApprovalQueue(
            store=InMemoryStore(),
            executors={"update_prompt": echo_executor},
            auto_execute_types={"update_prompt"},
        )
        a = queue.queue("update_prompt", "prompt update", {"to": "guardian"})
        # Already executed; never appeared in pending.
        self.assertEqual(a.status, EXECUTED)
        self.assertEqual(queue.list_pending(), [])

    def test_non_auto_execute_still_queues(self):
        queue = ApprovalQueue(
            store=InMemoryStore(),
            executors={"update_prompt": echo_executor,
                       "send_email": echo_executor},
            auto_execute_types={"update_prompt"},
        )
        a = queue.queue("send_email", "email", {"to": "x"})
        self.assertEqual(a.status, PENDING)
        self.assertEqual(len(queue.list_pending()), 1)


# ──────────────────────────────────────────────────────────────────────────────
# Per-user filtering
# ──────────────────────────────────────────────────────────────────────────────

class TestPerUser(unittest.TestCase):
    def test_list_pending_filters_by_user(self):
        queue = ApprovalQueue(store=InMemoryStore(),
                              executors={"x": echo_executor})
        queue.queue("x", "for hans", {}, user_id="hans")
        queue.queue("x", "for shane", {}, user_id="shane")
        queue.queue("x", "no user", {})
        self.assertEqual(len(queue.list_pending(user_id="hans")), 1)
        self.assertEqual(len(queue.list_pending(user_id="shane")), 1)
        self.assertEqual(len(queue.list_pending()), 3)


# ──────────────────────────────────────────────────────────────────────────────
# Hooks
# ──────────────────────────────────────────────────────────────────────────────

class TestHooks(unittest.TestCase):
    def test_on_queue_fires(self):
        seen = []
        queue = ApprovalQueue(store=InMemoryStore(),
                              executors={"x": echo_executor},
                              on_queue=seen.append)
        queue.queue("x", "test", {})
        self.assertEqual(len(seen), 1)
        self.assertEqual(seen[0].status, PENDING)

    def test_on_approve_and_on_execute_both_fire(self):
        approves, executes = [], []
        queue = ApprovalQueue(store=InMemoryStore(),
                              executors={"x": echo_executor},
                              on_approve=approves.append,
                              on_execute=executes.append)
        a = queue.queue("x", "test", {})
        queue.approve(a.id)
        self.assertEqual(len(approves), 1)
        self.assertEqual(len(executes), 1)
        # on_approve sees the action mid-transition (status=approved); by the
        # time on_execute fires, status=executed.
        self.assertEqual(executes[0].status, EXECUTED)

    def test_on_reject_fires(self):
        rejects = []
        queue = ApprovalQueue(store=InMemoryStore(),
                              executors={"x": echo_executor},
                              on_reject=rejects.append)
        a = queue.queue("x", "test", {})
        queue.reject(a.id)
        self.assertEqual(len(rejects), 1)

    def test_hook_exception_is_swallowed(self):
        def bad_hook(action):
            raise RuntimeError("hook failed")
        queue = ApprovalQueue(store=InMemoryStore(),
                              executors={"x": echo_executor},
                              on_queue=bad_hook)
        # Must not raise; hook failure can never block the queue write.
        a = queue.queue("x", "test", {})
        self.assertEqual(a.status, PENDING)


# ──────────────────────────────────────────────────────────────────────────────
# JsonFileStore round-trip
# ──────────────────────────────────────────────────────────────────────────────

class TestJsonFileStore(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = Path(tempfile.mkdtemp())
        self.path = self.tmp / "approvals.json"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_roundtrip(self):
        queue1 = ApprovalQueue(
            store=JsonFileStore(self.path),
            executors={"x": echo_executor},
        )
        a = queue1.queue("x", "first", {"k": "v"})
        # Open a second queue against the same file.
        queue2 = ApprovalQueue(
            store=JsonFileStore(self.path),
            executors={"x": echo_executor},
        )
        loaded = queue2.get(a.id)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.summary, "first")
        self.assertEqual(loaded.payload, {"k": "v"})

    def test_corrupt_file_starts_empty(self):
        self.path.write_text("not valid json", encoding="utf-8")
        queue = ApprovalQueue(store=JsonFileStore(self.path))
        self.assertEqual(queue.list_pending(), [])

    def test_atomic_write(self):
        queue = ApprovalQueue(
            store=JsonFileStore(self.path),
            executors={"x": echo_executor},
        )
        queue.queue("x", "a", {})
        # No leftover .tmp file
        leftovers = list(self.tmp.glob("*.tmp"))
        self.assertEqual(leftovers, [])

    def test_extra_fields_in_persisted_action_ignored(self):
        # Old persisted action with an extra key from a future schema.
        self.path.write_text(
            '[{"id":"abc","type":"x","summary":"old","payload":{},'
            '"status":"pending","created_at":"2026-05-01T00:00:00+00:00",'
            '"some_future_field":"ignore me"}]',
            encoding="utf-8",
        )
        queue = ApprovalQueue(store=JsonFileStore(self.path))
        a = queue.get("abc")
        self.assertEqual(a.summary, "old")


# ──────────────────────────────────────────────────────────────────────────────
# Concurrency
# ──────────────────────────────────────────────────────────────────────────────

class TestConcurrency(unittest.TestCase):
    def test_only_one_thread_can_approve(self):
        """Two threads racing to approve the same action: one wins, one ValueErrors."""
        queue = ApprovalQueue(
            store=InMemoryStore(),
            executors={"x": echo_executor},
        )
        a = queue.queue("x", "race", {})

        results = {"wins": 0, "losses": 0}
        barrier = threading.Barrier(2)
        lock = threading.Lock()

        def attempt():
            barrier.wait()
            try:
                queue.approve(a.id)
                with lock:
                    results["wins"] += 1
            except ValueError:
                with lock:
                    results["losses"] += 1

        threads = [threading.Thread(target=attempt) for _ in range(2)]
        for t in threads: t.start()
        for t in threads: t.join()

        self.assertEqual(results["wins"], 1)
        self.assertEqual(results["losses"], 1)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.CRITICAL)  # silence executor-failure logs
    unittest.main(verbosity=2)
