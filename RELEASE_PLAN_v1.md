---
title: The Builders' Doctrine — v1.0 Release Plan
version: v1.0 (operational)
authored: 2026-05-14
status: ACTIVE — supersedes the post-Grok 12-deliverable schedule as the operational plan
governing_laws: META_DOCTRINE.md VII (Provisional Doctrine), VIII (Meta-Schedule), X (Execution Threshold)
companion_artifacts: BANDWIDTH_OVERLAY_2026-05-15.md, LAW_VI_PRE_REG_v1.md
---

# v1.0 Release Plan — Ship What's Proven, Version What's Working

> **The reframe.** Truncate-at-Platoon was always the shippable v1.0 release package per Law VIII. Yesterday it was named the contingency plan. Today (2026-05-14) it becomes Plan A. v1.0 ships what is proven now with explicit deprecation of what isn't. v1.5 carries the Law VI replication verdict. v2.0 carries Company-scale validation + community study. Standard versioned release cadence — Linux, Python, every major framework operates this way.
>
> **Why now.** The 12-deliverable schedule from 2026-05-13 evening front-loaded a $2K statistician engagement and 78 hours of formal-study work into 10 weeks of constrained bandwidth (EMBA + Custer + health). The bandwidth overlay caught the infeasibility this morning and triggered a Law IX re-cut. The release-cadence reframe is the deeper Law IX move: re-cut not just the dates, but the scope.

---

## 1. What ships in v1.0 (verified inventory)

| Component | v1.0 status | Source artifact |
|---|---|---|
| THE_BUILDERS_DOCTRINE.md (13 principles) | ✓ ships | repo root |
| Principle 1 (biographical moat) | ✓ ships WITH explicit deprecation notice + v1.5 commitment | doctrine §I.1 + release notes |
| Principles 2–13 | ✓ ships | doctrine §I-II |
| MISSION_COMMAND_ARCHITECTURE.md | ✓ ships — Platoon scope only; rungs 3-9 named as hypothesis | MCA + ADP 6-0 translation |
| 8 chassis components | ✓ ships — engineering ports only; biographical-moat causal claim explicitly withdrawn from chassis docs | `kit/chassis/` |
| The Kit (88 fields, 8 templates) | ✓ ships | `kit/templates/`, `kit/onboarding/`, `kit/coverage.py` |
| Funkytown 01 + 02 empirical results | ✓ ships as appendix | `~/Projects/funkytown/findings/` referenced |
| ADP 6-0 translation | ✓ ships | `ADP_6_0_TRANSLATION.md` |
| PROMPT_DOCTRINE.md + WORKING_BACKWARDS.md + AMAZON_LP_CROSSMAP.md | ✓ ships | repo root |
| META_DOCTRINE.md (Laws V–X) | ✓ ships | repo root |
| STORY.md | ✓ ships | repo root |
| Law I deprecation notice + v1.5 roadmap | ✓ ships as part of release notes | NEW artifact |
| LAW_VI_PRE_REG_v1.md | ✓ ships as working document; v1.5 ratifies post-replication | repo root |

## 2. What ships in v1.5 (binding commitments, per Law VII)

| Commitment | Target date | Gate |
|---|---|---|
| External statistician engaged | 2026-06-22 | Founder identifies via cohort 84 referrals / DU stats clinic / paid lane |
| LAW_VI_PRE_REG_v2 with statistician sign-off | 2026-07-01 | Stat refines power calc, multi-comparison correction, exclusion criteria |
| OSF.io public pre-registration | 2026-07-05 | Plan locked publicly before any v1.5 experiment data collected |
| Law VI experiment complete (108 runs, 3 arms, 3 briefs) | 2026-07-15 | Funkytown Exp 04 harness (spec'd today, engineering ~17 hrs) |
| Law VI verdict + analysis | 2026-07-20 | Statistician runs pre-registered analysis; mechanical earn/retract decision |
| **v1.5 ships** | **2026-07-25** | Law I formally earned, qualified, or retracted in public doctrine update |

**If statistician cannot be engaged by 2026-06-30:** v1.5 commitment slips to "Law I status unchanged, framework versioned v1.1 with operational improvements only." Law VI carries forward to v1.5 with new dated commitment. Per Law X: prose-only commitments auto-truncate; no second slip without retraction.

## 3. What ships in v2.0 (provisional)

| Commitment | Target window | Gate |
|---|---|---|
| Company-scale validation | Q4 2026 | Funkytown Exp 03+ with Law V harness (N≥9 full-hierarchy + live cross-echelon conflict injection) |
| Community-replication study | Q4 2026 — Q1 2027 | Post-v1.0 traction; uses v1.0 Kit as the replication harness |
| Industry case studies | Q1 2027 | Requires v1.0 in production at 3+ external builders |

v2.0 commitments are provisional per Law VII — they get explicit dates and falsification criteria as v1.5 progresses or get retracted.

---

## 4. v1.0 ship schedule (dated milestones)

> **Capacity check against bandwidth overlay (re-cut 2026-05-21 against corrected 15 hr/wk steady-state):** ~50 hours of work across 2.5 weeks at original scope; ~9 hrs actual after Phase 1+2 reshape collapsed planned items 6×. Fits inside the bandwidth overlay's revised **~105-hr 7-week budget** (was 219 under the 40%-of-raw heuristic; corrected to 15 hr/wk after the founder's stated capacity at the 2026-05-21 weekly check-in). Wk 05-29 (EMBA finals) remains protected per Law VIII.

### Phase 1 — Final v1.0 prep (2026-05-14 → 2026-05-25)

| Date | Deliverable | Hrs | Owner |
|---|---|---|---|
| 2026-05-14 | RELEASE_PLAN_v1.md (this artifact) | 2 | Hans |
| 2026-05-22 | All framework holds carry execution dates (was #6) — **SHIPPED 2026-05-15 (`4d24319`), 7 days early; 1.5 actual hrs vs 6 scoped; 17 holds retired by strike/pointer; 4 dated holds remain (tracked elsewhere); inline edits, no standalone artifact** | 6 | Hans |
| 2026-05-25 | Productize-vs-license decision (was #7) — locked before public release — **LOCKED 2026-05-20 (5 days early): Option C (Hybrid). Counsel-free per scaffold reshape; ~4 actual hrs vs 10 scoped. See `PRODUCTIZE_VS_LICENSE_DECISION.md` §9.** | 10 | Hans |
| 2026-05-25 | Refusal-propagation off-ramp primitive spec (was #8) | 8 | Hans |
| 2026-05-25 | Founder-romance detector (was #9) — pre-commit hook on doctrine repo | 13 | Hans |

### Phase 2 — Public-facing artifacts (2026-05-26 → 2026-06-01)

| Date | Deliverable | Hrs | Owner |
|---|---|---|---|
| 2026-05-27 | Pitch / CLAUDE / EXPLAINER rewrite (was #10 — reshape for v1.0 claims, NO biographical-moat causal claim) | 15 | Hans |
| 2026-05-29 | v1.0 release notes draft — explicit Law I deprecation + v1.5 roadmap | 4 | Hans |
| 2026-05-30 | Public landing page (assayerhq.com or temporary) | 6 | Hans |
| 2026-06-01 | **v1.0 git tag + public release announcement** | 2 | Hans |

### Phase 3 — Release-gate testing + outreach (2026-06-01 → 2026-06-15)

| Date | Deliverable | Hrs | Owner |
|---|---|---|---|
| 2026-06-02 | Brad Hampton outreach with v1.0 link | 2 | Hans |
| 2026-06-02 | Myers + Whitaker re-engagement | 2 | Hans |
| 2026-06-03 → 06-10 | Cohort 84 distribution; selected DU faculty distribution | 4 | Hans |
| 2026-06-15 | TOP retention data + Principle 3 falsification verdict (was #11) — for v1.5 | 12 | Hans |
| 2026-06-15 | First-external-builder-running-the-Kit signal target | — | release-gate watch |

### Phase 4 — v1.5 prep (2026-06-15 → 2026-07-25)

| Date | Deliverable | Hrs | Owner |
|---|---|---|---|
| 2026-06-22 | External statistician identified | 8 | Hans |
| 2026-07-01 | LAW_VI_PRE_REG_v2 with statistician sign-off | 20 | Hans + stat |
| 2026-07-05 | OSF.io pre-registration posted publicly | 1 | Hans |
| 2026-07-10 | Funkytown Exp 04 harness implemented (~17 hrs eng per HARNESS_SPEC.md) | 17 | Hans |
| 2026-07-10 → 07-15 | Law VI 108 runs + outcome coding (blinded) | 25 | Hans (orchestration) |
| 2026-07-16 → 07-19 | Statistician runs pre-registered analysis | ~5 stat | Statistician |
| 2026-07-20 | Law VI verdict | 2 | Statistician → Hans |
| 2026-07-25 | **v1.5 release** | 8 | Hans |

**v1.0 total hours at original scope: ~89 (Phases 1+2). Actual after reshape: ~12 (Phase 1+2 shipped under estimate, 5–7 days early per BANDWIDTH_ACTUALS_2026.md). Remaining to ship 2026-06-01: ~2 hrs (tag + flip public + Pages deploy + Brad outreach).**
**v1.5 total hours: ~87 (Phases 3+4 + verdict) at original scope.**
**Combined original scope: 176 hours / 10 weeks. Remaining after Phase 1+2 ship: ~115 hours across the 10-week window.**

> **Bandwidth re-cut 2026-05-21.** Original line read "Combined: 176 hours across 10 weeks vs. bandwidth budget of 219 hours" — both numbers stale. The 219-hr budget was the 40%-of-raw heuristic; corrected to **15 hr/wk × 10 wks = 150 hrs** after the founder's stated capacity at the 2026-05-21 weekly check-in. Combined remaining demand (~115 hrs) fits 150-hr corrected capacity with **~35-hr buffer**, **conditional on statistician delegation of Law VI execution (Phase 4, ~25 hrs orchestration) closing by 2026-06-22.** Solo Law VI execution would push remaining demand to ~140+ hrs and consume the buffer. Per Law IX (>40 founder hrs on a single workstream without delegation = re-cut at the gate), statistician delegation is mandatory, not optional. See [memory: founder-capacity-15hr-wk-2026-05-21](/Users/hansprahl/.claude/projects/-Users-hansprahl-Projects-the-builders-doctrine/memory/founder_capacity_10hr_wk_2026_05_21.md).

---

## 5. What was cut, what was reshaped, what stayed

Mapped to the original 12 deliverables from `project_late_night_2026-05-13_grok_round7.md`:

| # | Original | New status |
|---|---|---|
| 1 | Bandwidth overlay | DONE 2026-05-14 |
| 2 | Weekly tripwires | DONE 2026-05-14 |
| 3 | Law VIII truncation criteria | DONE 2026-05-14 |
| 4 | External statistician identified | **MOVED to v1.5 (06-22)** — no longer Law VI auto-fallback B trigger; sequencing is now release-cadence |
| 5 | Law VI pre-reg + power calc | v1 DONE 2026-05-14; **v2 MOVED to v1.5 (07-01)** |
| 6 | All framework holds carry dates | **SHIPPED 2026-05-15 (`4d24319`), 7 days early** |
| 7 | Productize-vs-license decision | **LOCKED 2026-05-20 (5 days early): Option C (Hybrid)** |
| 8 | Refusal-propagation off-ramp spec | KEEP for v1.0 (05-25) |
| 9 | Founder-romance detector | KEEP for v1.0 (05-25) |
| 10 | Pitch/CLAUDE/EXPLAINER rewrite | **RESHAPE for v1.0 (05-27)** — no biographical-moat causal claim language |
| 11 | TOP retention + Principle 3 verdict | KEEP for v1.0 (06-15) |
| 12 | Law VI Stage 7 replication complete | **MOVED to v1.5 (07-20)** |

**Net change:** No deliverables cut from the framework. All twelve still execute. The shift is **sequencing**: v1.0 ships what is currently proven; v1.5 ships the Law VI verdict; v2.0 ships Company-scale validation + community work. Same destination, different release cadence.

---

## 6. Auto-fallback (Law VIII) under release-cadence framing

Auto-fallback B (truncate-at-Platoon) is **now Plan A.** It is not a fallback. It is the v1.0 ship.

Replacement auto-fallbacks under the release-cadence model:

| Trigger | Action |
|---|---|
| v1.0 ship slips past 2026-06-08 (1 week beyond target) | Strip Phase 2 to minimum: doctrine + chassis + Kit + release notes; defer landing page + outreach to post-ship; v1.0 ships 2026-06-08 |
| v1.0 ships but no external builder runs the Kit by 2026-07-31 | Release-gate has not moved; pause v2.0 prep work; re-evaluate Brad / Myers / Whitaker pitch; consider revised positioning |
| Statistician not engaged by 2026-06-30 | v1.5 slips to v1.1 (operational improvements only, Law VI unchanged); Law VI commitment carries to v1.5 with new dated re-commit |
| v1.5 Law VI experiment shows the effect collapses | Law I formally retracted; v1.5 release notes name retraction; framework continues with chassis + methodology unchanged; commercial pitch reshapes accordingly |
| v1.5 Law VI experiment confirms effect | Law I formally earned; v1.5 release notes update Principle 1; biographical-moat causal claim becomes available for external pitches |
| Any v1.5 milestone slips by 2+ weeks | Apply Law X auto-truncate: any prose-only commitment past its date converts to "deferred indefinitely until measured evidence ships" |

---

## 7. Risk register

| Risk | Mitigation |
|---|---|
| v2 vaporware risk | Dated commitments in v1.0 release notes; auto-truncate clauses in §6 |
| Cherry-picking-by-versioning critique | Pre-registration discipline per version; v1.5 Law I claim only earned if Law VI study runs to spec |
| Public-launch attack surface ("your headline principle is deprecated") | Lead with deprecation as trust signal: "We tested our most cited principle, found N=3 insufficient, named it publicly, running the proper study by 07-20" |
| Brand-versioning tension (doctrine ≠ software) | Versions apply to *artifacts* not to AI Tradecraft brand or underlying methodology |
| Brad's intro offer was conditional on biographical-moat thesis | v1.0 pitch lands on chassis + methodology + audit discipline; biographical-moat is v1.5 conditional |
| External builder catches v1.0 over-claim | Versioned patch (v1.0.1); audit-discipline story strengthens |
| Bandwidth still infeasible despite re-cut | Tripwire fires at 25% overrun on any week; Phase 2 strip-down (§6) kicks in |

---

## 8. Decision points along the way

| Date | Decision | Triggered if |
|---|---|---|
| 2026-05-22 | Continue to Phase 2 or strip Phase 1 scope | Hrs spent >25% over Phase 1 estimate |
| 2026-05-29 | Continue to Phase 2 final push or strip landing page | Hrs spent >25% over Phase 2 estimate by this date |
| 2026-06-01 | Ship or slip | Phase 1+2 complete OR strip-down triggered |
| 2026-06-15 | Engage statistician or convert v1.5 → v1.1 | External builder signal + cohort lead status |
| 2026-07-01 | Lock pre-reg v2 or extend stat search | Statistician engaged + design refined |
| 2026-07-20 | Earn / retract / qualify Law I | Statistician verdict delivered |
| 2026-07-25 | v1.5 ships or slips | All v1.5 milestones met |

---

## 9. What this plan does NOT change

- The bandwidth overlay (BANDWIDTH_OVERLAY_2026-05-15.md) remains the operational ledger for weekly hour tracking + tripwire firing
- The pre-registration document (LAW_VI_PRE_REG_v1.md) remains the v1 working draft; v2 lands with statistician
- The chassis (8 components, 230 tests) is unchanged
- The brand stack (AI Tradecraft / Assayer / Builders' Kit / Operator) is unchanged
- The hard release gate (one external builder running the Kit cold) is unchanged
- Law I remains deprecated as a causal claim until v1.5 verdict

---

## 10. What this plan changes

- **Sequencing.** v1.0 ships before Law VI replication runs. The framework reaches the public before the most consequential claim is empirically validated.
- **Auto-fallback semantics.** Truncate-at-Platoon was Plan B; it is now Plan A.
- **Marketing voice.** "We shipped what we can prove and named what we can't yet, with a dated roadmap." Honest, Stoic, calibrated.
- **Cost timing.** $2K statistician engagement moves from "now" to "post v1.0 traction signal" (2026-06-22 target).
- **Operational tempo.** v1.0 in 2.5 weeks, v1.5 in 10 weeks, v2.0 in ~6 months. Compounding release cadence vs. one-shot validate-then-ship.
