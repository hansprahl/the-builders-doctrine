# STARTUP — The Builders' Doctrine (AI Tradecraft meta-repo)

> Last updated: 2026-05-13. When this file disagrees with the code, the code wins.

## Identity

Portfolio-meta repo for **AI Tradecraft, by Hans Prahl**. Holds the methodology (Builders' Doctrine), the Kit (coverage scorer + interview templates that walk a builder through it), and the Chassis (seven portable runtime components lifted from TOP/Operator/Custer + ported from Principle #12). Sits *above* every per-product `CLAUDE.md`. Private through public release; release gated on one external builder running the kit cold and producing a working instance.

**Stage:** **v1.2 tagged 2026-05-13** (ratifies the in-flight v1.2 changes that had been live since 2026-05-01). v1.0 + v1.1 tagged 2026-04-30 (initial draft + post-stress-test propagation cycle). v1.2 captures: Principle #1 rename ("code is the story"), Principle #12 *What else? Active extraction* (2026-05-06, `876f452`), Principle #13 *The Long Horizon* (2026-05-12, `ad0d125`), Mission Command Architecture (2026-05-12, `3a3bb0d`) with Authority Gradient + Scale-Up Role Taxonomy + Staff Channel sections added (2026-05-13, `82e26ff`), Amazon LP cross-map + Working Backwards methodology, Kit field surface brought current (88 fields across 8 templates), `pr_faq_interview.yaml`, `chassis/reflection_gate.py` (seventh chassis component, Principle #12 primitive, 29 tests), and `chassis/authority_gradient.py` (eighth chassis component, MCA Authority Gradient primitive, 43 tests, 2026-05-13 `992e1b1`). Public-release brand **LOCKED 2026-05-05 as Assayer**. MCA is empirically validated at Platoon scale across two experiments: Funkytown 01 (N=3 × 7 ablation stages, ~$64) and Funkytown 02 Authority Gradient (N=3, 2026-05-13, mean 61.1% in-unit resolution, 0 tier violations, 0 hard-floor breaches — ✅ validate). Company and Battalion scale-up taxonomy is doctrine, not validated architecture.

## Commander's intent (north star)

> Lived experience compiled into AI-product behavior. Ethics encoded as commandments, refusals named explicitly, agents calibrated against truthful outcomes. Methodology ships free; operationalization (kit, hosted onboarding, audits) generates revenue downstream. The hard gate is one external builder running the kit cold and producing a working product instance. Until that happens, none of this goes public.

## Brand stack (locked 2026-05-05)

```
AI Tradecraft (umbrella, by Hans Prahl)
├── Assayer            — free public scorer + doctrine document
├── The Builders' Kit  — paid operationalization (this repo's kit/)
└── Operator           — patented closed-loop implementation
```

## Active phase — release-gate clearing

The methodology is code. The chassis is parity-tested against TOP. What hasn't happened yet:

- **External validation** — three thesis letters sent 2026-05-05 (Myers, Brad, Whitaker). **Brad path is moving**: biographical-moat thesis endorsed 2026-05-06 (`quote_brad_hampton_biographical_moat.md`); 30-min call 2026-05-12 named a specific SMB market gap (TRD/BRD pairs for Gemini Enterprise, 7/10 of his recent calls). Brad is **channel, not customer** — intro offer conditional on a sharper pitch + sellable MVP. Myers and Whitaker statuses not in memory; assume silence. Operator elevator pitch v1 captured 2026-05-12 (`quote_operator_elevator_pitch_v1_2026-05-12.md`).
- **Chassis adoption** — first wiring (`chassis/wire-approval-queue`, commit `d70e7b9`) was local-only on Operator at 2026-05-01; current status not re-verified from this repo. Five of six chassis components remained unwired as of 2026-05-01 — re-verify from Operator before asserting. Guardian structural scoring layer Borg-ported to TOP (`8a47d39`) and Custer (`ca8aa33`) on 2026-05-09; Operator skipped.
- **Custer STORY.md** — track on Custer side; not load-bearing for this repo.
- **Trademark queue** — Assayer (Class 9 + 42), AI Tradecraft, Builders' Kit, Operator. Peter Lemire owns.
- **Domain footprint** — `assayerhq.com` + defensives + `aitradecraft.io` not yet registered.
- **`assayer.dev` collision** — production-readiness-review tool in adjacent class. Decision: proceed; bet on substrate differentiation. Peter to confirm in formal sweep.

## Architecture (load-bearing)

- **`THE_BUILDERS_DOCTRINE.md`** — the prose. **Thirteen principles**: seven foundational ethics + six operational doctrines. Canonical doctrine artifact. (v1.0 shipped with 11; #12 and #13 folded in post-tag.)
- **`MISSION_COMMAND_ARCHITECTURE.md`** — portfolio-wide agentic architecture (2026-05-12). ADP 6-0's seven principles mapped to LLM-agent properties; 3-tier Platoon Pattern; recursive composability; context isolation between echelons. **Provisionally adopted** based on Funkytown Experiment 01 (Platoon scale, N=3 × 7 ablation stages, ~$64). Scale-up to Company/Battalion is the next falsification rung.
- **`SCHEDULER_SPEC_DRAFT.md`** — primitive spec paired with MCA (2026-05-12). Time-based intent injection into the running unit.
- **`WORKING_BACKWARDS.md`** + **`AMAZON_LP_CROSSMAP.md`** — Amazon's PR/FAQ-first product methodology adopted 2026-05-12 as the portfolio-shared scoping process. Operationalizes Principle #13 at the scoping layer. Vocabulary buys legitimacy in the SaaS/AWS channel (per Brad Hampton call 2026-05-12).
- **`PRINCIPLE_13_DRAFT.md`** — drafting workspace for Principle #13 (already folded into the doctrine prose; retained as scratchpad).
- **`PROMPT_DOCTRINE.md`** — universal prompt structural rules. The rubric every product's Guardian enforces.
- **`THE_BUILDERS_METHOD.md`** — the methodology in builder-facing form.
- **`kit/coverage.py`** — single-file scorer. Three CLI surfaces (`--score`, `--list`, `--interview`). As of v1.2: scores **88 fields across 8 templates** including the new MCA position fields (SPECIALIST_TEMPLATE), Principle #12 gate (AGENT_DOCTRINE), Principle #13 refusals (COMMANDMENTS), and the Working Backwards surface (PR_FAQ_TEMPLATE).
- **`kit/templates/`** — seven templates (STORY, COMMANDMENTS, REFUSAL_LIST, CRISIS_TRIGGERS, SPECIALIST_TEMPLATE, AGENT_DOCTRINE, SECURITY) with `KIT:FIELD` markers.
- **`kit/onboarding/`** — seven interviews with `depends_on` graphs that enforce authoring order (added `pr_faq_interview.yaml` in v1.2).
- **`kit/chassis/`** — **eight portable runtime components** (added `reflection_gate.py` + `authority_gradient.py` in v1.2): Crisis Floor, Approval Queue, Per-User Context (ContextVar with LookupError-on-unset), Named Specialists, AAR Loop, Prompt Guardian, **Reflection Gate** (Principle #12 primitive, scope-aware: operator_tool / wellness / founder; 29 unit tests), **Authority Gradient** (MCA primitive — Tier/Channel enums, overridable tool→class table, `on_world_boundary` callback hook composing with ApprovalQueue; 43 unit tests; ported from funkytown Experiment 02 validation). 230 unit tests total; 8 parity tests against TOP's actual production constants.
- **`baselines/v1.1/`** — frozen baseline for the next stress-test propagation.

## Active risks

1. **Single-builder validation still pending.** Brad call 2026-05-12 named a market gap and offered conditional intros; no external builder has yet run the Kit cold. Brad is channel, not customer — the release gate has not moved.
2. ~~**Doctrine–Kit drift.**~~ **CLOSED in v1.2 (2026-05-13).** Doctrine carries 13 principles + MCA + Working Backwards. The Kit's templates now score those layers explicitly: AGENT_DOCTRINE has `active_extraction_gate` + MCA unit-structure fields; COMMANDMENTS has `long_horizon_refusals`; SPECIALIST_TEMPLATE has `authority_tier`/`role`/`channel`/`escalation_threshold`/`disciplined_initiative_scope`; PR_FAQ_TEMPLATE has the full Working Backwards surface. A builder running the Kit cold post-v1.2 gets signal on every layer the doctrine carries.
3. **MCA empirical claim is one experiment.** Funkytown 01 = Platoon scale only, N=3 across 7 stages. "Portfolio-wide architecture" before a second independent validation (Company scale at minimum) is real audit-grade exposure. Hans's stated falsification ladder (`founding_principle_full_portfolio_pipeline_2026-05-11.md`): Platoon → Company → Battalion. Company scale not yet run.
4. **Soak debt on the chassis wiring** (carry-over). 3,500 lines shipped 2026-05-01. `chassis/wire-approval-queue` was local-only and unpushed at last check; re-verify Operator side before asserting state. **Seven of eight chassis components remain unwired in any product** as of 2026-05-13 — the eighth (`authority_gradient`) is referenced in all 4 product CLAUDE.mds (Custer `356669a`, TOP `55e7a88`, Operator `376510c`, RPR `9943bcc`) but not yet imported by any product code. Operator is the queued first adopter for `authority_gradient` per the same `chassis/wire-approval-queue` precedent.
5. **Brand-collision in adjacent space.** `assayer.dev` is live in production-readiness-review. Acceptable but real; no silent re-litigation without new info.
6. **No CI on this repo.** All gates (gitleaks, prompt-injection scan, parity tests) live in product repos. Doctrine repo is doctrine + kit; treat changes here as carefully as any product repo because every product inherits at next Guardian audit.

## Hands-off

- **Material doctrine edits** — Hans approval + version bump. Editorial (typo, clarification, example) is fine.
- **Patent-adjacent text** — Subsystem A (the closed loop) is patent-pending. The split between free (Assayer scorer + doctrine) and paid (corrector, stash-and-rollback, two-corrector router, recommendations engine, CI gate) is load-bearing for IP. **Do not move features across that line without Hans + Peter Lemire.**
- **`PATENT_DISCLOSURE.md` (in Operator repo)** — pre-filing legal doc. Has a known inventor-bio error (line 160 says "USMC retired"; correct is Army NG retired). Do **not** unilaterally edit; flag for IP attorney at first contact.
- **The Refusal list** — canonical lives in `THE_BUILDERS_DOCTRINE.md II.8`. Per-product audit logs are downstream (`REFUSAL_AUDIT.md`). Don't fork.

## Recent significant changes

- **`992e1b1` chassis/authority_gradient — eighth portable chassis component (MCA primitive); funkytown Experiment 02 closed ✅ (2026-05-13)**
- **`1755af2` chassis/reflection_gate — seventh portable chassis component (Principle #12) (2026-05-13)**
- **`6c9c3a6` Kit — close Doctrine drift; 88 fields across 8 templates, pr_faq interview lands (2026-05-13)**
- **`82e26ff` MCA — Authority Gradient + Scale-Up Role Taxonomy + Staff Channel; ratify v1.2 (2026-05-13)**
- **`f1ece26` STARTUP.md — refresh to current state (2026-05-13)**
- `3a3bb0d` Mission Command Architecture doctrine + Scheduler primitive spec + example task (2026-05-12)
- `ad0d125` Adopt Amazon LP cross-map + Working Backwards methodology; add Principle #13 Long Horizon (2026-05-12)
- `876f452` Add Principle #12 *What else? Active extraction* (2026-05-06)
- `07da6b8` STARTUP.md: scope memory pointers to portfolio-meta dir, not Custer-scoped (2026-05-06)
- `828ab0a` STARTUP.md + STORY chapter — Assayer brand lock, thesis outreach sent, reliability principle named (2026-05-06)
- `bfc3b6e` STORY.md origin chapter (2026-05-01)
- `21723c2` chassis: relative imports + lazy kit.coverage import in crisis_floor (2026-05-01)
- `ecc3c89` chassis/parity_top — integration tests vs. TOP's actual production data (2026-05-01)
- `7f87086` chassis/prompt_guardian — sixth and final Phase 2 component (2026-05-01)
- `b9bd07d` kit Phase 1 scoring engine + interview runner (2026-05-01)

## Pointer index

**Doctrine artifacts (this repo):**
- `THE_BUILDERS_DOCTRINE.md` — the methodology prose, v1.2 (13 principles)
- `MISSION_COMMAND_ARCHITECTURE.md` — portfolio-wide agentic architecture (2026-05-12)
- `SCHEDULER_SPEC_DRAFT.md` — primitive spec paired with MCA
- `WORKING_BACKWARDS.md` — Amazon PR/FAQ-first scoping methodology (adopted 2026-05-12)
- `AMAZON_LP_CROSSMAP.md` — Amazon Leadership Principles cross-map
- `PRINCIPLE_13_DRAFT.md` — scratchpad for Long Horizon (folded into main doctrine)
- `THE_BUILDERS_METHOD.md` — builder-facing method
- `PROMPT_DOCTRINE.md` — universal prompt structural rules (canonical upstream)
- `EXPLAINER.md` — public-facing explainer draft
- `WIRING_DIAGRAM.md` — how the chassis wires into a product
- `STRESS_TEST_v1.0.md` — propagation test results
- `ARTIFACT_AUDIT_2026-05-01.md` — audit at v1.0 lock
- `STORY.md` — founder narrative; tail before any new chapter

**Memory files (load on demand)** — all live in the portfolio-meta scope at `/Users/hansprahl/.claude/projects/-Users-hansprahl-Projects/memory/`:
- `reference_builders_doctrine_canonical.md` — canonical location, layer position, v1.0 contents
- `project_assayer_brand_lock.md` — public-release brand lock 2026-05-05
- `project_agentic_tuner_hypothesis.md` — parent hypothesis; Assayer is the locked name
- `reference_doctrine_naming.md` — three scales (brand / methodology / artifact / session)
- `feedback_doctrine_naming_convention.md` — never bare DOCTRINE.md
- `project_operator_chassis_wiring_branch.md` — `chassis/wire-approval-queue` soak status (re-verify)
- `project_thesis_outreach_sent_2026-05-05.md` — first external validation event
- `quote_brad_hampton_biographical_moat.md` — Brad's biographical-moat endorsement 2026-05-06
- `project_brad_smb_trd_brd_niche_2026-05-12.md` — Brad call 2026-05-12; SMB TRD/BRD market gap; channel-not-customer
- `quote_operator_elevator_pitch_v1_2026-05-12.md` — first customer-facing pitch
- `founding_principle_full_portfolio_pipeline_2026-05-11.md` — full portfolio pipeline + Mission Command scaling falsification ladder
- `quote_reliability.md` — four-lens reliability standard (audit/scale/promise/founder)
- `project_drake_premortem_2026-05-06.md` — scale-grade failure inventory
- `project_observability_spec_v0_1.md` — six emission categories, scale-grade gate
- `project_intake_pipeline_tier1.md` — self-serve inbox shipped in Operator 2026-05-06
- `project_guardian_structural_scoring_layer.md` — Guardian structural scoring Borg-ported to TOP/Custer 2026-05-09
- `feedback_session_as_reliability_checkpoint.md` — session-discipline principle
- `feedback_stoic_register_held_under_pull_2026-05-11.md` — voice discipline under pressure
- `feedback_grok_second_opinion_workflow.md` — Grok as second-opinion check before locking high-level decisions
- `feedback_audit_measurement_before_law.md` — Funkytown Stage 9 near-miss; audit metric code before doctrine
- `quote_biographical_reflection_substrate.md` — the moat is biographical, not technical
- `project_competitive_landscape.md` — read before any external Kit pitch
- `project_plugineval_competitor.md` — wshobson/agents PluginEval, direct Assayer competitor

**Cross-repo pointers (where the doctrine lives downstream):**
- `~/Projects/local-mcp/` — TOP (chassis parity baseline)
- `~/Projects/operator/` — Operator (first chassis wiring; patent-pending closed loop)
- `~/Projects/custer-mcp/` — Custer (Guardian recommendations engine origin)
- `~/Projects/RPR/` — RPR (first Agentic Tuner demo; score-only Borg port)
