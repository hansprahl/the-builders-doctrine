---
status: ACTIVE — first check due Thursday 2026-05-21 EOD
gate: Law VIII (Meta-Schedule) + Law IX (Delegation Threshold)
owner: Hans Prahl
parent: BANDWIDTH_OVERLAY_2026-05-15.md (§4d weekly check-in protocol)
release_plan: RELEASE_PLAN_v1.md (supersedes overlay §2/§3 for deliverable dates)
---

# Bandwidth Actuals — 2026 v1.0 ship cycle

> Weekly ledger of actual hours and tripwire results against `BANDWIDTH_OVERLAY_2026-05-15.md §1` capacity and §4 tripwires. One block per Thursday EOD. Commit the actuals + any triggered action to git the same night per §4d.5.
>
> Weeks run Friday → Thursday so each block closes at the Thursday check (e.g. Wk 05-15 covers 2026-05-15 → 2026-05-21).
>
> Deliverable IDs (#1–#12) and tripwire rules track the overlay. Deliverable **dates** track RELEASE_PLAN_v1.md where the two diverge (Phase 1 trio = 2026-05-25, not the overlay's 2026-06-08).

---

## Standing reference — capacity (overlay §1)

| Workstream | Wk 05-15 | Wk 05-22 | Wk 05-29 | Wk 06-05 | Wk 06-12 | Wk 06-19 | Wk 06-26 |
|---|---|---|---|---|---|---|---|
| Realistic doctrine-productive capacity | 29 | 28 | 26 | 34 | 34 | 34 | 34 |

## Standing reference — tripwire yellow/red thresholds (overlay §4a)

| Workstream | Yellow | Red |
|---|---|---|
| EMBA | >20% over forecast | >25% over OR missed class/exam |
| Custer | >3/wk for 2 wks | >5/wk |
| Health | Formations <85% | Formations <70% OR missed appt |
| Family | >12/wk | >15/wk OR explicit ask |
| Other | >12/wk | >15/wk |

---

## Wk 05-15 — closes Thursday 2026-05-21 EOD

**Status:** in progress. Fill on 2026-05-21.

### Workstream actuals (hrs)

| Workstream | Forecast | Actual | Flag |
|---|---|---|---|
| EMBA | 12 | _ | _ |
| Custer | 2 | _ | _ |
| Health (Formations + diabetes/sobriety) | 5.5 | _ | _ |
| Family / household | 10 | _ | _ |
| Other (NECC, Biffle, advisors) | 10 | _ | _ |
| **Doctrine** | **19** | _ | _ |
| **Doctrine capacity** | **29** | — | — |
| **Util %** | **66%** | _ | _ |

### Deliverable actuals (hrs against estimate)

| # | Deliverable | Due | Est. | Actual | Status |
|---|---|---|---|---|---|
| 1 | Bandwidth overlay populated | 2026-05-15 | 2 | _ | shipped `ccd526b` 2026-05-14 |
| 2 | Weekly tripwires per workstream | 2026-05-15 | 2 | _ | shipped `44d6384` 2026-05-14 |
| 3 | Law VIII truncation criteria pre-registered | 2026-05-15 | 1 | _ | shipped 2026-05-14 (part of `ccd526b`) |
| 4 | External statistician identified | 2026-05-18 (overlay) / 2026-06-22 (RELEASE_PLAN) | 8 | _ | **see §4c.1 below — date conflict to resolve** |
| 6 | All framework holds carry execution dates | 2026-05-22 | 6 | _ | shipped `4d24319` 7 days early |

### Cross-portfolio doctrine work this week (not numbered in §2)

| Item | Commit | Est. hrs | Actual |
|---|---|---|---|
| RELEASE_NOTES_v1.0 round-3 + STORY chapter | `bceff4a` | _ | _ |
| Anatomy v2 Session 1B (queue standardization) | `216585a` | _ | _ |

### Tripwire results (§4a + §4b + §4c)

- **§4a workstream tripwires:** _none / yellow:__ / red:__
- **§4b deliverable tripwires:**
  - Mid-window hours-to-date >60% of est: _none / list:__
  - Date misses: _none / list:__
- **§4c cascade tripwires:**
  - **4c.1 — RESOLVED 2026-05-18.** Overlay §4c.1 made #4 statistician identification a 2026-05-18 EOD gate whose miss auto-fired truncate-at-Platoon. RELEASE_PLAN_v1.md (`ab95bd7`, 2026-05-14) reframed statistician engagement to 2026-06-22 post-v1.0 traction and made truncate-at-Platoon Plan A explicitly. The cascade is therefore satisfied-by-reframe, not by hitting the original date. STARTUP.md v1.5 commitments section carries the resolution note. No cascade action required this week.
  - 4c.2 — two consecutive yellow flags on any workstream: N/A (first check)
  - 4c.3 — week utilization >100% capacity: _Yes/No_
  - 4c.4 — any deliverable miss re-cut date by ≥25% est. hrs: _Yes/No_

### Action taken on red flags

_None / describe + commit SHA_

### Notes

- Wk 05-15 effective parallel count per §3 footnote: bundle(#1+#2+#3) + #4 + #6 = 3 = at Law IX threshold, legal.
- Two extra commits this week (`bceff4a`, `216585a`) charged to doctrine; need to attribute hours so doctrine actual ≤ 29.

---

## Wk 05-22 — closes Thursday 2026-05-29 EOD

_Scaffold — fill on 2026-05-29._

### Active deliverables this week

| # | Deliverable | Due | Est. | Notes |
|---|---|---|---|---|
| 7 | Productize-vs-license decision | 2026-05-25 | 10 | Hans + counsel |
| 8 | Refusal-propagation off-ramp primitive spec | 2026-05-25 | 8 | Hans |
| 9 | Founder-romance detector (regex + pre-commit + reviewer) | 2026-05-25 | 13 | Hans; Adversarial Review chassis is the LLM-reviewer successor |

Per RELEASE_PLAN Phase 1 close. Wk 05-22 forecast doctrine load 22 hrs vs. 28 capacity; three deliverables converging on 05-25 — Law IX at threshold.

---

## Wk 05-29 — closes Thursday 2026-06-04 EOD

**EMBA finals + Exam 2 + Conceptual Quiz week. Zero doctrine hours. No deliverables.**

Tripwire still fires Thursday to confirm Health + EMBA forecasts held.

---

## Wk 06-05 — closes Thursday 2026-06-11 EOD

_Scaffold — fill on 2026-06-11. Phase 2 deliverables in flight: pitch/CLAUDE/EXPLAINER rewrite (2026-05-27), v1.0 release notes (2026-05-29), landing page (2026-05-30), **v1.0 ship 2026-06-01**._

---

## Wk 06-12, Wk 06-19, Wk 06-26

_Scaffolds added at each Thursday check._
