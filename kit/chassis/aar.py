"""
The Builders' Kit — After-Action Reviews (AAR) Loop.

Portable implementation of doctrine component #9 from TOP's
tools/doctrine_aar.py. Tracks outcomes of recommendations, habits, tasks,
goals, and routines. Calibrates specialist confidence against reality
over time — the mechanism that lets truthful data override cheap claims.

This chassis module is SQLite-backed and self-contained. It does NOT
depend on the Knowledge Graph chassis (which may or may not exist in
a given product). When products want to link AAR entries to entities
in a Knowledge Graph, they pass an `action_id` at record time; the
chassis stores it for later cross-reference but does not require it.

Doctrine invariants this module preserves (non-negotiable):

  1. The four-outcome scale is durable and coarse: success / failure /
     partial / abandoned. Resist the urge to add finer grain — coarseness
     is what makes outcomes comparable across products and time.
  2. Confidence is cheap; outcomes are expensive and truthful. AAR is
     the mechanism that lets truthful data override cheap claims.
  3. Per-specialist calibration is the load-bearing report — surfaces
     specialists whose claimed confidence consistently overshoots
     reality.

Usage:

    from kit.chassis import AARLog

    log = AARLog(db_path=Path("data/aar.db"))

    # When an action's outcome becomes known:
    aar_id = log.record_outcome(
        action_type="recommendation",
        action_name="start morning run 3x/week",
        outcome="partial",
        details="Ran twice in week 1, once in week 2. Injury recurrence.",
        specialist="scout",
    )

    # Get the calibration report:
    report = log.calibration_report(specialist="scout")
    print(report.summary())
    # → "AAR: 12 tracked | 58% success | S:7 F:2 P:2 A:1"

    # Inject calibration into the orchestrator prompt:
    block = log.format_for_prompt(specialist_labels={
        "vera": "Vera (Schedule)",
        "scout": "Scout (Wellness)",
    })
"""

from __future__ import annotations

import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Optional

# The four-outcome scale. Ordered by emotional valence so reports can
# show the dimension consistently across products.
SUCCESS = "success"
FAILURE = "failure"
PARTIAL = "partial"
ABANDONED = "abandoned"

VALID_OUTCOMES = frozenset({SUCCESS, FAILURE, PARTIAL, ABANDONED})

# Action types this module accepts. The set is open by default — products
# may pass any string. The constants are conventions, not constraints.
HABIT = "habit"
TASK = "task"
GOAL = "goal"
ROUTINE = "routine"
RECOMMENDATION = "recommendation"


# ──────────────────────────────────────────────────────────────────────────────
# Data shapes
# ──────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class AAR:
    """One after-action record."""
    id: str
    action_type: str
    action_name: str
    outcome: str
    details: str
    specialist: str
    recorded_at: str
    action_id: Optional[str] = None

    @classmethod
    def from_row(cls, row: sqlite3.Row | tuple) -> "AAR":
        # Tolerant of either positional or named row access.
        if isinstance(row, sqlite3.Row):
            return cls(**{k: row[k] for k in row.keys()})
        return cls(*row)


@dataclass(frozen=True)
class CalibrationReport:
    """Per-specialist (or aggregate) outcome counts."""
    specialist: str       # empty string = aggregate across all specialists
    total: int
    success: int
    failure: int
    partial: int
    abandoned: int

    @property
    def success_rate(self) -> float:
        """Success ratio in [0.0, 1.0]. 0.0 when total is 0."""
        return (self.success / self.total) if self.total > 0 else 0.0

    def summary(self) -> str:
        """One-line summary, matching TOP's format."""
        if self.total == 0:
            return "AAR: 0 tracked"
        breakdown = " ".join(
            f"{label}:{count}"
            for label, count in (
                ("S", self.success), ("F", self.failure),
                ("P", self.partial), ("A", self.abandoned),
            )
            if count > 0
        )
        rate_pct = self.success_rate * 100.0
        return f"AAR: {self.total} tracked | {rate_pct:.0f}% success | {breakdown}"


# ──────────────────────────────────────────────────────────────────────────────
# AARLog
# ──────────────────────────────────────────────────────────────────────────────

class AARLog:
    """SQLite-backed after-action-review log. One per product."""

    _SCHEMA = """
    CREATE TABLE IF NOT EXISTS aar (
        id TEXT PRIMARY KEY,
        action_type TEXT NOT NULL,
        action_name TEXT NOT NULL,
        outcome TEXT NOT NULL,
        details TEXT NOT NULL DEFAULT '',
        specialist TEXT NOT NULL DEFAULT '',
        recorded_at TEXT NOT NULL,
        action_id TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_aar_specialist ON aar(specialist);
    CREATE INDEX IF NOT EXISTS idx_aar_outcome ON aar(outcome);
    CREATE INDEX IF NOT EXISTS idx_aar_recorded_at ON aar(recorded_at);
    """

    def __init__(self, db_path: Path | str = ":memory:") -> None:
        """
        Args:
            db_path: SQLite database path. Use ":memory:" for tests.
                Parent directory is created if needed.
        """
        self.db_path = str(db_path)
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        # Hold one connection so :memory: persists between calls.
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        # WAL improves concurrent read/write; safe to set on every connect.
        if self.db_path != ":memory:":
            self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(self._SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    @contextmanager
    def _cursor(self) -> Iterator[sqlite3.Cursor]:
        cur = self._conn.cursor()
        try:
            yield cur
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cur.close()

    # ── Record ───────────────────────────────────────────────────────────────

    def record_outcome(
        self,
        action_type: str,
        action_name: str,
        outcome: str,
        *,
        details: str = "",
        specialist: str = "",
        action_id: Optional[str] = None,
    ) -> str:
        """
        Record an outcome. Returns the new AAR id.

        Raises:
            ValueError: if outcome is not in VALID_OUTCOMES, or
                action_type / action_name are empty.
        """
        if outcome not in VALID_OUTCOMES:
            raise ValueError(
                f"outcome must be one of {sorted(VALID_OUTCOMES)}; "
                f"got {outcome!r}"
            )
        if not action_type or not action_type.strip():
            raise ValueError("action_type must be non-empty")
        if not action_name or not action_name.strip():
            raise ValueError("action_name must be non-empty")

        aar_id = uuid.uuid4().hex[:12]
        recorded_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO aar (id, action_type, action_name, outcome, "
                "details, specialist, recorded_at, action_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (aar_id, action_type, action_name, outcome,
                 details, specialist, recorded_at, action_id),
            )
        return aar_id

    # ── Read ─────────────────────────────────────────────────────────────────

    def list_outcomes(
        self,
        *,
        specialist: Optional[str] = None,
        action_type: Optional[str] = None,
        limit: int = 200,
    ) -> list[AAR]:
        """All AARs, newest first, optionally filtered."""
        sql = "SELECT * FROM aar"
        clauses = []
        params: list = []
        if specialist is not None:
            clauses.append("specialist = ?")
            params.append(specialist)
        if action_type is not None:
            clauses.append("action_type = ?")
            params.append(action_type)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY recorded_at DESC LIMIT ?"
        params.append(limit)
        with self._cursor() as cur:
            rows = cur.execute(sql, params).fetchall()
        return [AAR.from_row(r) for r in rows]

    def get(self, aar_id: str) -> Optional[AAR]:
        """Return the AAR with this id, or None."""
        with self._cursor() as cur:
            row = cur.execute(
                "SELECT * FROM aar WHERE id = ?", (aar_id,)
            ).fetchone()
        return AAR.from_row(row) if row else None

    # ── Calibration ──────────────────────────────────────────────────────────

    def calibration_report(
        self,
        specialist: Optional[str] = None,
    ) -> CalibrationReport:
        """
        Aggregate outcome counts. If specialist is None, aggregates across
        all specialists. If specialist is given but has no AARs, returns
        a zero report (not an error — absence of data is itself signal).
        """
        sql = "SELECT outcome, COUNT(*) AS n FROM aar"
        params: list = []
        if specialist is not None:
            sql += " WHERE specialist = ?"
            params.append(specialist)
        sql += " GROUP BY outcome"
        with self._cursor() as cur:
            rows = cur.execute(sql, params).fetchall()
        counts = {SUCCESS: 0, FAILURE: 0, PARTIAL: 0, ABANDONED: 0}
        for r in rows:
            outcome = r["outcome"]
            if outcome in counts:
                counts[outcome] = r["n"]
        return CalibrationReport(
            specialist=specialist or "",
            total=sum(counts.values()),
            success=counts[SUCCESS],
            failure=counts[FAILURE],
            partial=counts[PARTIAL],
            abandoned=counts[ABANDONED],
        )

    def calibration_by_specialist(self) -> dict[str, CalibrationReport]:
        """
        Per-specialist calibration reports. Specialists with no AARs are
        omitted. Specialists with empty-string identifier are omitted (the
        chassis treats unspecified-specialist AARs as ungrouped data).
        """
        with self._cursor() as cur:
            rows = cur.execute(
                "SELECT specialist, outcome, COUNT(*) AS n FROM aar "
                "WHERE specialist != '' "
                "GROUP BY specialist, outcome"
            ).fetchall()
        by_spec: dict[str, dict[str, int]] = {}
        for r in rows:
            spec = r["specialist"]
            by_spec.setdefault(spec, {SUCCESS: 0, FAILURE: 0, PARTIAL: 0, ABANDONED: 0})
            outcome = r["outcome"]
            if outcome in by_spec[spec]:
                by_spec[spec][outcome] = r["n"]
        return {
            spec: CalibrationReport(
                specialist=spec,
                total=sum(counts.values()),
                success=counts[SUCCESS],
                failure=counts[FAILURE],
                partial=counts[PARTIAL],
                abandoned=counts[ABANDONED],
            )
            for spec, counts in by_spec.items()
        }

    # ── Prompt-injection helpers ─────────────────────────────────────────────

    def format_for_prompt(
        self,
        *,
        specialist_labels: Optional[dict[str, str]] = None,
        header: str = "[STAFF TRACK RECORDS — calibration from AAR outcomes:]",
    ) -> str:
        """
        Emit a multi-line block suitable for injection into an orchestrator
        system prompt. Empty string when no calibration data exists.

        Args:
            specialist_labels: Map of specialist_name → display label
                (e.g. {'vera': 'Vera (Schedule)'}). Specialists not in
                this map are skipped. Pass None to use raw names for
                everyone with data.
            header: First line of the block. Customize per product.
        """
        by_spec = self.calibration_by_specialist()
        if not by_spec:
            return ""
        lines = [header]
        if specialist_labels is not None:
            ordered = [(spec, specialist_labels[spec]) for spec in specialist_labels
                       if spec in by_spec]
        else:
            ordered = [(spec, spec.title()) for spec in sorted(by_spec.keys())]
        if not ordered:
            return ""
        for spec, label in ordered:
            report = by_spec[spec]
            if report.total == 0:
                continue
            lines.append(f"  {label}: {report.summary()[5:]}")  # strip "AAR: " prefix
        return "\n".join(lines) if len(lines) > 1 else ""

    def specialist_line(self, specialist: str) -> str:
        """
        One-line track record for a specific specialist, suitable for
        injecting into that specialist's own system prompt. Empty if
        no data.
        """
        report = self.calibration_report(specialist=specialist)
        if report.total == 0:
            return ""
        rate_pct = report.success_rate * 100.0
        breakdown = " ".join(
            f"{label}:{count}"
            for label, count in (
                ("S", report.success), ("F", report.failure),
                ("P", report.partial), ("A", report.abandoned),
            )
            if count > 0
        )
        return (
            f"YOUR TRACK RECORD — {report.total} recommendations tracked | "
            f"{rate_pct:.0f}% success | {breakdown}"
        )
