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

## Standing reference — capacity (overlay §1, corrected 2026-05-21)

| Workstream | Wk 05-15 | Wk 05-22 | Wk 05-29 | Wk 06-05 | Wk 06-12 | Wk 06-19 | Wk 06-26 |
|---|---|---|---|---|---|---|---|
| Realistic doctrine-productive capacity (Hans 2026-05-21) | **15** | **15** | **15** | **15** | **15** | **15** | **15** |
| Crash-week ceiling (known load windows only) | 25 | 25 | 25 | 25 | 25 | 25 | 25 |

> Capacity corrected at the 2026-05-21 weekly check-in. Original overlay row (29 / 28 / 26 / 34 ...) was the 40%-of-raw heuristic without ground truth. Same-session calibration walked 5 → 10 → 15 as forward-demand math was made explicit; **15 hr/wk steady-state** is the locked number, with **~25 hr/wk crash-week ceiling** acceptable for known windows (Exp 10/10b before 2026-05-30; LAW_VI_PRE_REG_v2 sign-off around 2026-07-01). See [memory: founder-capacity-15hr-wk-2026-05-21](/Users/hansprahl/.claude/projects/-Users-hansprahl-Projects-the-builders-doctrine/memory/founder_capacity_10hr_wk_2026_05_21.md) for full reasoning + downstream implications.

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

**Status:** populated 2026-05-21 PM. Awaiting Hans confirmation on workstream hours.

### Workstream actuals (hrs)

| Workstream | Forecast | Actual | Flag |
|---|---|---|---|
| EMBA | 12 | _ (Hans) | _ |
| Custer | 2 | _ (Hans) | _ |
| Health (Formations + diabetes/sobriety) | 5.5 | _ (Hans) | _ |
| Family / household | 10 | _ (Hans) | _ |
| Other (NECC, Biffle, advisors) | 10 | _ (Hans) | _ |
| **Doctrine** | (forecast row n/a after capacity correction) | **~40–60 (observable, Hans confirm)** | **🔴 RED — §5#1 fires** |
| **Doctrine capacity (corrected 2026-05-21)** | **15** | — | — |
| **Crash-week ceiling** | **25** | — | — |
| **Util %** | — | **~267–400%** | **🔴 RED — §4c.3 fires** |

### Deliverable actuals (hrs against estimate)

| # | Deliverable | Due | Est. | Actual | Status |
|---|---|---|---|---|---|
| 1 | Bandwidth overlay populated | 2026-05-15 | 2 | ~0 (this wk) | shipped `ccd526b` 2026-05-14 (before window) |
| 2 | Weekly tripwires per workstream | 2026-05-15 | 2 | ~0 (this wk) | shipped `44d6384` 2026-05-14 (before window) |
| 3 | Law VIII truncation criteria pre-registered | 2026-05-15 | 1 | ~0 (this wk) | shipped 2026-05-14 (part of `ccd526b`, before window) |
| 4 | External statistician identified | 2026-06-22 (RELEASE_PLAN supersedes overlay 05-18) | 8 | 0 | deferred — §4c.1 resolved 2026-05-18 by release-cadence reframe |
| 6 | All framework holds carry execution dates | 2026-05-22 | 6 | 1.5 | shipped `4d24319` 2026-05-15, 7 days early |
| 7 | Productize-vs-license decision | 2026-06-08 (overlay) / 2026-05-25 (RELEASE_PLAN) | 10 | ~4 | LOCKED `712684a` 2026-05-20, 5 days early, Option C (Hybrid) |
| 8 | Refusal-propagation off-ramp primitive spec | 2026-06-08 (overlay) / 2026-05-25 (RELEASE_PLAN) | 8 | ~1 | FROZEN `f800b38` 2026-05-20, 5 days early, v0.2 |
| 9 | Founder-romance detector v0.1 | 2026-06-08 (overlay) / 2026-05-25 (RELEASE_PLAN) | 13 | ~2 | SHIPPED `81dfbd7` 2026-05-20, 5 days early (regex; Adversarial Review successor was retracted 2026-05-19) |
| 10 | EXPLAINER rewrite (Phase 2) | 2026-06-15 (overlay) / 2026-05-27 (RELEASE_PLAN) | 20 (overlay) / 15 (RELEASE_PLAN) | ~0.7 | shipped `9ffe65e` 2026-05-20, 7 days early, deprecation-as-trust-signal frame |

### Phase 2 ship-day items shipped early this week

| Item | Commit | Est. | Actual |
|---|---|---|---|
| v1.0 release notes | `4fe5afa` | (Phase 2) | ~0.3 |
| Public landing page (`docs/index.html` + `style.css`) | `dd2732b` | (Phase 2) | ~1 |
| CLAUDE.md for doctrine-repo | `6bd8334` | n/a | ~1 |
| STARTUP.md sweep + ship-day deploy steps | `ab78a5f`, `bd44263` | n/a | ~0.5 |

### Cross-portfolio doctrine work this week (charged to doctrine workstream)

| Item | Commits | Est. | Actual |
|---|---|---|---|
| Operator dogfood asymptote experiment (N=1 → N=20 + finding) | 18 commits 2026-05-18 → 2026-05-19 (`9d2ac59` → `403f30c`) + Operator specs.py validators #2-#42 (~20 commits) | n/a | _ (heavy — Hans confirm; rough ~20-30 hrs) |
| Funkytown Exp 05-10 sequence (Squad/Platoon/Company falsification) | 30+ commits 2026-05-19 → 2026-05-20 (`25fd642` → `986936f`) | n/a | _ (heavy — Hans confirm; rough ~15-25 hrs) |
| MCA v3 → v4 → v5 → v5-candidate doctrine evolution + Grok pressure-tests | `9192ed3`, `69c1d2f`, `db637a3`, `17adecb`, `789e643`, `41c298e` | n/a | ~3-5 |
| PROMPT_DOCTRINE v1.1 → v1.3 propagation (TOP/Custer/Operator Borg port) | `630ba79`, `85dc39f`, `7148344`, `1f78ab2` + 3 product-repo propagations | n/a | ~2-3 |
| Assayer v0.1 scorer | `6accb9e` | n/a | ~1-2 |
| RELEASE_NOTES_v1.0 round-3 + STORY chapter (Sarah Chen) | `bceff4a` | n/a | _ |
| Anatomy v2 Session 1B (queue standardization, BD + TOP + Operator + Custer) | `216585a` + 4 product propagations | n/a | _ |
| MENTAL_MODEL_RADIO_NET + ADP 6-0 translation companion | `9ffda6a` | n/a | ~1 |
| HANS_VOICE_PRINCIPLES.md (canonical portfolio voice file) | `db2dae0` | n/a | ~1 |
| SHAPING_OPERATIONS v0.2 doctrine + Operator port | `b16ff33`, `4e96aea` + Operator `7837055` | n/a | ~2 |
| Adversarial Review chassis RETRACTED + archived | `114630e` | n/a | ~0.5 |

### Tripwire results (§4a + §4b + §4c)

- **§4a workstream tripwires:** pending Hans's non-doctrine workstream hour numbers (EMBA / Custer / Health / Family / Other). Doctrine workstream: 🔴 **RED.** Observable ~40–60 hrs vs. 15 hr/wk capacity = 167–300% over the 25% red-flag threshold (~19 hr/wk yellow / ~19 hr/wk red); also over the 25 hr/wk crash-week ceiling.
- **§4b deliverable tripwires:**
  - Mid-window hours-to-date >60% of est: **none** — all five Phase 1 deliverables (#6, #7, #8, #9, #10) shipped UNDER estimate, 5–7 days early. Reshape discipline held in all five cases. Deliverable-level discipline is intact; the overshoot is from unplanned empirical work (asymptote + Funkytown), not deliverable bloat.
  - Date misses: **none.**
- **§4c cascade tripwires:**
  - **4c.1 — RESOLVED 2026-05-18.** Overlay §4c.1 made #4 statistician identification a 2026-05-18 EOD gate whose miss auto-fired truncate-at-Platoon. RELEASE_PLAN_v1.md (`ab95bd7`, 2026-05-14) reframed statistician engagement to 2026-06-22 post-v1.0 traction and made truncate-at-Platoon Plan A explicitly. The cascade is therefore satisfied-by-reframe, not by hitting the original date. No cascade action required this week.
  - 4c.2 — two consecutive yellow flags on any workstream: N/A (first check).
  - 4c.3 — week utilization >100% capacity: 🔴 **YES.** Doctrine utilization ~267–400% of corrected 15-hr capacity (also exceeds 25-hr crash ceiling). Prescribed action: "climb pauses. Re-cut at the next Thursday gate, not at first missed milestone." Next-gate re-cut = **2026-05-28.**
  - 4c.4 — any deliverable miss re-cut date by ≥25% est. hrs: **No.** All shipped under estimate, early.

### §5 truncation triggers (this is the load-bearing read)

- 🔴 **§5 #1 fires.** "Any single workstream overruns its estimated hours by ≥25% at week-end check" — doctrine actual (~40–60) vs. corrected capacity (15) is 167–300% over the 25% threshold. Trigger fires mechanically.
- ✓ **Prescribed action:** truncate-at-Platoon v1.0 ships per §5 release-package list (13 principles + MCA Platoon scope + 8 chassis + Funkytown 01+02 + ADP 6-0 + Law I deprecation notice; no Company/Battalion claims).
- ✓ **This is consistent with RELEASE_PLAN_v1.md** (`ab95bd7`, 2026-05-14), which made truncate-at-Platoon Plan A explicitly two weeks ago. **The trigger firing ratifies the existing plan rather than forcing a reversal.** No new doctrine artifact required; the existing release plan already encodes the truncated package as the v1.0 ship.

### Action taken on red flags

- Capacity correction applied: BANDWIDTH_OVERLAY §1 capacity row + this file's standing reference + RELEASE_PLAN_v1.md bandwidth-check line all edited to **15 hr/wk steady-state / 25 hr/wk crash ceiling** (was 29 / 28 / 26 / 34 ...). Hans-stated number at the 2026-05-21 check-in; original heuristic row preserved struck-through in the overlay for audit trail. Same-session calibration walked 5 → 10 → 15 as forward demand was made explicit; 15 is the locked number. See memory: `founder_capacity_15hr_wk_2026_05_21.md`.
- §5 #1 trigger fired; action = truncate-at-Platoon v1.0 ship 2026-06-01. **Already Plan A** per RELEASE_PLAN_v1; no scope change.
- §4c.3 cascade fired; action = "climb pauses, re-cut at next gate" → 2026-05-28 re-cut planned. RELEASE_PLAN_v1.md bandwidth-check + combined-hours lines were updated tonight against the 15 hr/wk capacity: 10-week capacity now 150 hrs; remaining demand to v1.5 ~115 hrs after Phase 1+2 ships; ~35-hr buffer **conditional on statistician delegation of Law VI execution closing by 2026-06-22.**
- No second re-cut available per §5 #6: "Any single doctrine deliverable misses its re-cut date by ≥25% of estimated hours → auto-fallback B fires mechanically. Truncate-at-Platoon v1.0 ships. No second re-cut." Truncate-at-Platoon is now the floor; further slippage doesn't have anywhere to go but indefinitely-deferred.

### Notes

- **The reshape discipline held on planned work.** Originally estimated ~58 hrs across the early-ship Phase 1 + 2 deliverables (10→4 + 8→1 + 13→2 + 15→0.7 + 20→0.3 + ~1 + ~1) → ~9 hrs actual. The overshoot was unplanned empirical work (Operator dogfood asymptote N=1→N=20, Funkytown Exp 05–10), not deliverable bloat. The same discipline that collapsed deliverable estimates 6× did not constrain the reactive empirical surface.
- **Wk 05-15 effective parallel count:** bundle(#1+#2+#3) shipped before window + #6, #7, #8, #9, #10 in flight = 5 active during the week. Per micro-bundle refinement (sub-2-hour items count as one), effective parallel was at Law IX threshold = 3, not over.
- **Pace context for next session:** at 10 hr/wk capacity, this week's ~40–60 hr pace burned down a reserve that doesn't exist. Continuous overhead (weekly check-in + STORY chapters + drift sweeps + cross-portfolio propagation) is 2–3 hr/wk = 20–30% of capacity. Funkytown Exp 10b + 10 by 2026-05-30 (~6–8 hrs) is the next near-term load that approaches the weekly ceiling.

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
