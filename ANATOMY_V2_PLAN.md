# Anatomy Doctrine v2 — Implementation Plan

**Locked: 2026-04-30 — Hans Prahl + Claude**
**Status: planned, not started. Anatomy Doctrine v1 currently lives at `rubicon/api/runtime/anatomy.py`. v2 work happens in this repo.**

---

## Locked decisions (reference)

| # | Decision | Locked |
|---|---|---|
| 1 | Tier 1 scope | All four additions (Soul reweight, Nervous System, Immune System, Spinal Cord) |
| 2 | Tier 2 scope | 2.1 (vitals over time) + 2.2 (diagnostic + prescriptive layer) only. 2.3 (audit-as-anatomy) deferred to post-merge work |
| 3 | Location | Migrate Anatomy Doctrine out of Rubicon to `hansprahl/the-builders-doctrine/frameworks/anatomy/`. Becomes portfolio-wide, not Rubicon-specific |
| 4 | Standardization | Guardian + approval-queue APIs standardized across TOP, Operator, Custer **before** Tier 1.3 (Immune) and Tier 1.4 (Spinal) land |
| 5 | Weights | Soul 0.18, Gut 0.16, Heart 0.14, Brain 0.12 (Brain demoted below Gut and Heart per the three-system governance doctrine — see `quote_three_governance_systems.md`). Voice 0.09, Hands 0.07, Skin 0.06, Muscle 0.06, Connective 0.06, Blood 0.06. Sum 1.00. Tier 1 additions (Nervous, Immune, Spinal) reweight at the time they land |
| 6 | Measurement | Option B — Gut measurement evolves alongside the weight bump. Form-completeness Gut metric retired; replaced with intuition-shaped metrics (anomaly detection rate, low-confidence accuracy, unprompted-concern surface) |
| 6 (cadence) | Sequence | One session every 2 weeks as target. 6 sessions × 2 weeks ≈ 3 months. Skip a week if campaign / EMBA / soak demands it. Doctrine work waits; campaign and EMBA don't. |

---

## Sequence

Numbers are session-relative, not calendar-locked. Slip without guilt; resume when capacity is real.

### Session 1 — Standardize Guardian + queue APIs

Pre-Anatomy work. Closes the cross-product API drift surfaced in `STRESS_TEST_v1.0.md`.

**Deliverables:**
- `tools/prompt_guardian.py` interface spec — required exports: `score_one(agent_name)`, `run_guardian()`, `list_prompt_history(agent_name)`, `rollback_prompt(agent_name, timestamp=None)`, `_read_default_prompt(agent_name)` — applied to all three products
- TOP regex bug fixed (`f?"""` pattern, same as Custer)
- TOP missing `lingo` specialist resolved (either restored or removed from SPECIALISTS dict)
- TOP user_context handling for Guardian runs (set hans by default for score-only runs)
- Operator's Guardian internal API aligned with TOP/Custer
- Approval-queue API standardized — `queue(action_type, payload)`, `approve(id)`, `reject(id, reason)`, `pending(channel=None)`, `throughput_stats()` — applied across `operator/tools/approvals.py`, `custer-mcp/tools/pending_posts.py` + `agents/digital_blast.py`
- Validation: re-run baseline capture script on all three products. All three should produce a clean baseline JSON.

**Acceptance:** all three products score-clean against their own Guardian without API errors.

### Session 1B — Approval-queue API standardization

Carved out of Session 1 after the queue recon (2026-05-15) surfaced drift larger than the plan anticipated. Session 1 closed cleanly on the Guardian half; the queue half is its own session because the storage layer is heterogeneous, not just the function names.

**What the recon found:**

1. **Category key trichotomy** — Operator uses `action_type`, TOP uses `type`, Custer pending_posts uses `channel` (which is semantically a sub-discriminator, not a top-level type). Custer also has a *second* queue (`blasts`) that splits build/approve/execute across three calls.
2. **Storage heterogeneity** — Operator + TOP persist JSON files; Custer uses SQLite. IDs differ (8-char uuid string vs int autoincrement). Payload encoding differs (dict / JSON-string / TEXT column / normalized columns).
3. **Approve-vs-execute conflation** — Operator separates `approve_action` (state transition) from `execute_approved` (side effect). TOP and Custer pending_posts collapse them — approving fires the side effect immediately. Anatomy v2's `approve(id)` must define which semantic it locks in.
4. **`reject(id, reason)` signature missing** — Operator and TOP both lack the `reason` param; Custer blasts has no reject path at all. Only Custer pending_posts has it.
5. **`pending(channel=None)` filter + `throughput_stats()` are net-new across the board** — channel filtering exists in some schemas but is never exposed; throughput counting exists only as an internal rate-limit helper in Operator.

**Locked canonical API:**

| Function | Signature | Semantics |
|---|---|---|
| `queue(action_type, payload)` | `(str, dict) -> str` (returns id) | Enqueue; never executes |
| `approve(id)` | `(str) -> dict` | State transition only; returns payload. Side effect via separate `execute(id)` call (Operator pattern; TOP/Custer get a refactor to split the two) |
| `reject(id, reason)` | `(str, str) -> str` | Reason becomes mandatory; persisted on the item |
| `pending(channel=None)` | `(Optional[str]) -> list[dict]` | Filter by channel/sub-discriminator |
| `throughput_stats()` | `() -> dict` | Returns `{queued_24h, approved_24h, rejected_24h, executed_24h, median_time_to_decision, p95_time_to_decision}` — the Spinal Cord body system reads this directly |

**Storage canonicalization:** payload always crosses the wire as `dict`; persistence converts to whatever the backend needs. ID type is opaque str across the wire (uuid for Operator/TOP, str(int) for Custer SQLite rows).

**Per-product migration:**

- **Operator** (`tools/approvals.py`): add `reason` param to reject, add `pending(channel=None)`, add `throughput_stats()`, alias canonical names alongside legacy `queue_action`/`approve_action`. ~2h.
- **TOP** (`tools/approvals.py`): split approve from execute, add `reason`, convert `details` JSON-string → `payload` dict, add `pending(channel=None)` + `throughput_stats()`. ~3h.
- **Custer** (`tools/pending_posts.py`): split approve from execute, expose existing `rejection_reason` via canonical signature, rename `channel`→`action_type` (with `channel` becoming a payload field), add `pending(channel=None)` filter + `throughput_stats()`. ~3h.
- **Custer blasts** (`agents/digital_blast.py` + `db/schema.py`): add `reject(id, reason)` path; the existing build/approve/execute three-step stays but gains a canonical surface. ~1h.
- **Cross-queue Spinal Cord aggregator** in Custer (one body needs throughput across both queues). ~2h.
- **Tests + validation** (per-product unit + cross-product parity). ~2h.

**Total effort:** ~13–14h. Own session.

**Acceptance:** all three products expose the canonical five via consistent signatures; Spinal Cord prerequisite met (Session 3 can read `throughput_stats()` without product-specific adapters).

**Sequencing rule:** Session 1B blocks Session 3 (Immune System depends on standardized Guardian — done — and Spinal Cord depends on standardized queue throughput stats). Session 2 (Soul reweight + Spinal Cord body system itself) also depends on 1B. Session 1B must land before Session 2.

### Session 2 — Tier 1.1 (Soul reweight) + Tier 1.4 (Spinal Cord)

**Deliverables:**
- Migrate `anatomy.py` from Rubicon to `frameworks/anatomy/anatomy.py` in this repo
- Add Spinal Cord body system. Health = % irreversible actions through queue (hard floor — must be 100%) + queue depth + approval/reject ratio + median time-to-decision
- Update weights dict to locked v5 hierarchy (Soul 0.18, Gut 0.16, Heart 0.14, Brain 0.12, etc.)
- Spinal Cord weight slotted in (below the four governance systems, above Voice — proposed 0.10, redistribute the rest)
- Adapter modules `bridge_top.py`, `bridge_operator.py`, `bridge_custer.py` — each pulls Spinal Cord metrics from that product's standardized approval queue
- Update tests in Rubicon to point at the new location (or stub out if Rubicon stays paused)

**Acceptance:** Spinal Cord body system computes for all three products; reweighted aggregate health calculates cleanly.

### Session 3 — Tier 1.2 (Nervous System) + Tier 1.3 (Immune System)

**Deliverables:**
- Add Nervous System body system. Health = events/day × handler success rate × subscriber coverage. Source: each product's event bus (TOP `tools/doctrine_events.py`, Operator's bus, Custer's TBD — see open question below)
- Add Immune System body system. Health = days-since-last-Guardian-run × commandment coverage × correction accuracy × % specialists in tolerance. Source: each product's standardized Guardian (post-Session 1)
- Adapter bridges extended to expose Nervous + Immune metrics per product
- Reweight to slot Nervous + Immune into hierarchy (proposed: Nervous 0.06, Immune 0.08 — Immune higher because it's drift defense, more load-bearing)
- Final weights table after Tier 1 complete

**Open question for Session 3:** Custer has no event bus. Either (a) accept Nervous System reads N/A for Custer until an event bus is added, or (b) add a minimal event bus to Custer as part of this session. My vote: a — N/A is honest.

**Acceptance:** Nervous + Immune compute for products that have the underlying infrastructure; explicit N/A where infrastructure is missing.

### Session 4 — Soak

No work. Let Tier 1 generate data for two weeks. Specifically:
- Spinal Cord captures real approval throughput
- Nervous System captures real event volume
- Immune System captures Guardian baselines
- The new weights produce real overall_health numbers, not synthetic

**Acceptance:** the data Session 5 will visualize actually exists.

### Session 5 — Tier 2.2 (diagnostic + prescriptive layer)

**Deliverables:**
- Refactor `BodySystem` dataclass — `detail` becomes `{current_status, action_to_improve, severity}` structured object
- Update all 13 (10 original + 3 Tier 1) body-system computations to populate the structured detail
- Gut measurement redesigned (Decision 6 / Option B):
  - Retired: enrichment-question completeness
  - New: anomaly detection rate × low-confidence accuracy × unprompted-concern surface
  - This is the intuition-shaped Gut metric per the three-system doctrine
- Update Rubicon's `anatomy-display.tsx` to render structured detail (or defer UI until Agentic Tuner)
- Migration script for any existing AgentAnatomy records (probably not needed if Rubicon is paused — verify)

**Acceptance:** every body system below threshold names a specific action. Gut metric reflects intuition, not form-fills.

### Session 6 — Tier 2.1 (vitals over time)

**Deliverables:**
- New table `agent_anatomy_vitals` — `(timestamp, agent_id, system_name, health, status)`
- Daily snapshot job — runs once per agent per day, captures all body-system healths
- API endpoints to retrieve vitals time series
- Renderer: sparkline per body system, full chart per system on demand
- Initial 2-week data window from Session 4 soak now visible as a real trend

**Acceptance:** every body system has a 14+ day health trace. Compounding signal is visible, not theoretical.

### Sessions 7+ (out of scope for v2 sprint)

- Tier 2.3 (audit-as-anatomy) — deferred until merge work
- Tier 3 (unified Anatomy + AGENT_DOCTRINE) — multi-session, post-v2
- Tier 4 (lifecycle, muscle memory, circulation) — capture as ideas, defer

---

## Capacity flag

This is real work on top of:

- TOP pilots running
- Operator deployed
- Custer in run-up to general election (2026-11-03)
- EMBA Cohort 84 in flight
- Builders Doctrine v1.1 just shipped, needs to soak
- v1.2 doctrine work (validation on external case, public release)

**The doctrine waits when life requires it.** Skip sessions when needed. The plan is a target, not an obligation. Three sessions of soak between Tier 1 and Tier 2 isn't laziness — it's the signal accumulating.

If you slip three sessions in a row, that's a signal to revisit whether v2 is the right work or whether something else demands attention. It's not failure; it's calibration.

---

## What this plan does NOT cover

- Building Tier 2.3 (audit-as-anatomy) — defers to post-merge
- The Tier 3 merge itself — separate plan when the time comes
- Multi-tenant readiness for the merged framework — couples to Operator multi-tenant decision (deferred per Builders Doctrine v1.1)
- Agentic Tuner v0.1 — separate product, 9–12 month timeline, builds on this work but isn't this work
- Rubicon's UI updates — defer or treat as Agentic Tuner work
- Public release of the Anatomy framework — happens with Builders Doctrine v1.2 release, not standalone

---

## Cross-references

- Builders Doctrine v1.1: `THE_BUILDERS_DOCTRINE.md` (this repo, tag v1.1)
- Anatomy Doctrine v1: `rubicon/api/runtime/anatomy.py` (frozen with rest of Rubicon at tag rubicon-cohort-v1)
- AGENT_DOCTRINE.md: `local-mcp/AGENT_DOCTRINE.md` (TOP)
- Stress test that surfaced the standardization gap: `STRESS_TEST_v1.0.md` (this repo)
- Three-system governance quote: `~/.claude/projects/-Users-hansprahl-Projects-custer-mcp/memory/quote_three_governance_systems.md`
- Scope draft this plan supersedes: `custer-mcp/_anatomy_doctrine_v2_scope.md` (working doc, can be deleted after Hans signs off on this plan)

---

**Ready to start when capacity allows. Session 1 is the natural starting point — no Anatomy work depends on standardization being unsolved.**
