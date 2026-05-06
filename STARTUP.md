# STARTUP — The Builders' Doctrine (AI Tradecraft meta-repo)

> Last updated: 2026-05-06. When this file disagrees with the code, the code wins.

## Identity

Portfolio-meta repo for **AI Tradecraft, by Hans Prahl**. Holds the methodology (Builders' Doctrine), the Kit (coverage scorer + interview templates that walk a builder through it), and the Chassis (six portable runtime components lifted from TOP/Operator/Custer). Sits *above* every per-product `CLAUDE.md`. Private through v1.0; public release gated on one external builder running the kit cold and producing a working instance.

**Stage:** v1.0 tagged 2026-04-30. Phase 1 (kit/coverage) and Phase 2 (chassis suite — six components, parity-tested vs. TOP) shipped 2026-05-01. Public-release brand **LOCKED 2026-05-05 as Assayer**. No commits to this repo since 2026-05-01; downstream propagation has been the work.

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

- **External validation** — first formal outreach SENT 2026-05-05 (Myers, Brad, Ryan Whitaker). Watch inbox.
- **Chassis adoption** — first wiring (`chassis/wire-approval-queue`, commit `d70e7b9`) sits **local-only on Operator**, unpushed, soaking. Five of six chassis components still unwired in any product.
- **Custer STORY.md** — 0 of 7 fields populated. Hans's voice, before May 15 deadline, not delegate-able.
- **Trademark queue** — Assayer (Class 9 + 42), AI Tradecraft, Builders' Kit, Operator. Peter Lemire owns.
- **Domain footprint** — `assayerhq.com` + defensives + `aitradecraft.io` not yet registered.
- **`assayer.dev` collision** — production-readiness-review tool in adjacent class. Decision: proceed; bet on substrate differentiation. Peter to confirm in formal sweep.

## Architecture (load-bearing)

- **`THE_BUILDERS_DOCTRINE.md`** — the prose. Eleven principles + four operational doctrines. Canonical doctrine artifact.
- **`PROMPT_DOCTRINE.md`** — universal prompt structural rules. The rubric every product's Guardian enforces.
- **`THE_BUILDERS_METHOD.md`** — the methodology in builder-facing form.
- **`kit/coverage.py`** — single-file scorer. Three CLI surfaces (`--score`, `--list`, `--interview`).
- **`kit/templates/`** — seven templates (STORY, COMMANDMENTS, REFUSAL_LIST, CRISIS_TRIGGERS, SPECIALIST_TEMPLATE, AGENT_DOCTRINE, SECURITY) with `KIT:FIELD` markers.
- **`kit/onboarding/`** — six interviews with `depends_on` graphs that enforce authoring order.
- **`kit/chassis/`** — six portable runtime components: Crisis Floor, Approval Queue, Per-User Context (ContextVar with LookupError-on-unset), Named Specialists, AAR Loop, Prompt Guardian. 158 unit tests; 8 parity tests against TOP's actual production constants.
- **`baselines/v1.1/`** — frozen baseline for the next stress-test propagation.

## Active risks

1. **Single-builder validation pending.** Until an external builder runs the kit cold, "portable" is an unverified claim. Three thesis-outreach emails are the first real test.
2. **Soak debt on the chassis wiring.** 3,500 lines of new code shipped 2026-05-01 with unit + parity tests but zero soak under real load. The `chassis/wire-approval-queue` branch is the canary; do not push or merge until it has been used in real usage.
3. **Brand-collision in adjacent space.** `assayer.dev` is live in production-readiness-review. Acceptable but real; no silent re-litigation without new info.
4. **No CI on this repo.** All gates (gitleaks, prompt-injection scan, parity tests) live in product repos. Doctrine repo is doctrine + kit; treat changes here as carefully as any product repo because every product inherits at next Guardian audit.

## Hands-off

- **Material doctrine edits** — Hans approval + version bump. Editorial (typo, clarification, example) is fine.
- **Patent-adjacent text** — Subsystem A (the closed loop) is patent-pending. The split between free (Assayer scorer + doctrine) and paid (corrector, stash-and-rollback, two-corrector router, recommendations engine, CI gate) is load-bearing for IP. **Do not move features across that line without Hans + Peter Lemire.**
- **`PATENT_DISCLOSURE.md` (in Operator repo)** — pre-filing legal doc. Has a known inventor-bio error (line 160 says "USMC retired"; correct is Army NG retired). Do **not** unilaterally edit; flag for IP attorney at first contact.
- **The Refusal list** — canonical lives in `THE_BUILDERS_DOCTRINE.md II.8`. Per-product audit logs are downstream (`REFUSAL_AUDIT.md`). Don't fork.

## Recent significant changes

- `bfc3b6e` STORY.md origin chapter (2026-05-01)
- `21723c2` chassis: relative imports + lazy kit.coverage import in crisis_floor
- `ecc3c89` chassis/parity_top — integration tests vs. TOP's actual production data
- `7f87086` chassis/prompt_guardian — sixth and final Phase 2 component
- `8ae8dfa` chassis/aar — fifth portable chassis component
- `ce3abfa` chassis/specialists — fourth portable chassis component
- `f6235cc` chassis/user_context — third portable chassis component
- `4229783` chassis/approval_queue — second portable chassis component
- `4c5b22e` chassis/crisis_floor — first portable chassis component
- `b9bd07d` kit Phase 1 scoring engine + interview runner

## Pointer index

**Doctrine artifacts (this repo):**
- `THE_BUILDERS_DOCTRINE.md` — the methodology prose, v1.0
- `THE_BUILDERS_METHOD.md` — builder-facing method
- `PROMPT_DOCTRINE.md` — universal prompt structural rules (canonical upstream)
- `EXPLAINER.md` — public-facing explainer draft
- `WIRING_DIAGRAM.md` — how the chassis wires into a product
- `STRESS_TEST_v1.0.md` — propagation test results
- `ARTIFACT_AUDIT_2026-05-01.md` — audit at v1.0 lock
- `STORY.md` — founder narrative; tail before any new chapter

**Memory files (load on demand):**
- `reference_builders_doctrine_canonical.md` — canonical location, layer position, v1.0 contents
- `project_assayer_brand_lock.md` — public-release brand lock 2026-05-05
- `project_agentic_tuner_hypothesis.md` — parent hypothesis; Assayer is the locked name
- `reference_doctrine_naming.md` — three scales (brand / methodology / artifact / session)
- `feedback_doctrine_naming_convention.md` — never bare DOCTRINE.md
- `project_operator_chassis_wiring_branch.md` — `chassis/wire-approval-queue` soak status
- `project_thesis_outreach_sent_2026-05-05.md` — first external validation event
- `quote_reliability.md` — four-lens reliability standard (audit/scale/promise/founder)
- `project_drake_premortem_2026-05-06.md` — scale-grade failure inventory
- `project_observability_spec_v0_1.md` — six emission categories, scale-grade gate
- `project_intake_pipeline_tier1.md` — self-serve inbox shipped in Operator 2026-05-06
- `feedback_session_as_reliability_checkpoint.md` — session-discipline principle
- `quote_biographical_reflection_substrate.md` — the moat is biographical, not technical
- `project_competitive_landscape.md` — read before any external Kit pitch
- `project_plugineval_competitor.md` — wshobson/agents PluginEval, direct Assayer competitor

**Cross-repo pointers (where the doctrine lives downstream):**
- `~/Projects/local-mcp/` — TOP (chassis parity baseline)
- `~/Projects/operator/` — Operator (first chassis wiring; patent-pending closed loop)
- `~/Projects/custer-mcp/` — Custer (Guardian recommendations engine origin)
- `~/Projects/RPR/` — RPR (first Agentic Tuner demo; score-only Borg port)
