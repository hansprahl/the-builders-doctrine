# The Builders' Doctrine

A methodology for compiling lived experience into AI-product behavior. Ethics encoded as commandments. Refusals named explicitly. Agents calibrated against truthful outcomes.

The meta-doctrine for the Hans Prahl AI portfolio. This repository is the canonical source. Each downstream product (TOP, Operator, Custer, Rubicon, future) carries a propagated copy with drift detection at pre-commit.

> **Prime Directive.** I build AI as agentic versions of the builder — ethics and lived experience encoded into code that acts within intent and stops at irreversible. The moat is memory, not model. Designed to be needed less, not more. Truth is architecture; the lie detector built in. A clean room rebuilds from doctrine and commits, or the product is a snowflake.

## Start here

- [EXPLAINER.md](EXPLAINER.md) — plain-language explainer for a non-technical reader, peer, or investor. Best entry point.
- [THE_BUILDERS_DOCTRINE.md](THE_BUILDERS_DOCTRINE.md) — the canonical doctrine prose. Austere by design.
- [RELEASE_NOTES_v1.0.md](RELEASE_NOTES_v1.0.md) — what ships at v1.0, what is deprecated, what is on the v1.5 roadmap.
- [ADP_6_0_TRANSLATION.md](ADP_6_0_TRANSLATION.md) — civilian glossary for the Army vocabulary that appears in `MISSION_COMMAND_ARCHITECTURE.md` (commander's intent, OPORD-down/SITREP-up, Squad → COCOM scale ladder).

## What ships in v1.0

- **The doctrine prose** — thirteen principles (seven foundational ethics, six operational doctrines) plus six methodological laws governing how the doctrine itself is allowed to make claims.
- **The Kit** — an eight-template coverage scorer plus an interview runner that walks a builder through authoring each template in dependency order. `kit/coverage.py --list`, `kit/coverage.py --score`, `kit/coverage.py --interview`.
- **The chassis** — nine portable runtime components (Crisis Floor, Approval Queue, Per-User Context, Named Specialists, AAR Loop, Prompt Guardian, Reflection Gate, Authority Gradient, Founder-Romance Detector). 276 unit tests; parity-tested against a live production product.
- **Two empirical experiments at Platoon scale** — `MISSION_COMMAND_ARCHITECTURE.md` ships at Platoon scope; rungs above (Company, Battalion, etc.) are explicitly named as hypothesis, not validated architecture.
- **A versioned roadmap** — `RELEASE_PLAN_v1.md` carries dated v1.5 (2026-07-25) and v2.0 (Q4 2026) commitments. Holds without dates are not allowed per [META_DOCTRINE.md](META_DOCTRINE.md) Law VII.

## Versions

- **v1.0-public** — 2026-05-21 — first public release. Shipped 11 days early from a 2026-06-01 target after Phase 1 + Phase 2 deliverables collapsed under the reshape discipline (`THE_BUILDERS_DOCTRINE.md` §II Principle 12: *What else? Active extraction*).
- **v1.2** — 2026-05-13 — added Principles 12 and 13, Mission Command Architecture, Working Backwards methodology, Authority Gradient + Reflection Gate chassis components.
- **v1.1** — 2026-04-30 — post-stress-test propagation cycle.
- **v1.0** — 2026-04-30 — initial draft (internal).

**Authority:** Hans Prahl. Material edits go through Hans + a version bump. Editorial edits do not.

## What's not yet proven

Three load-bearing items are named explicitly at v1.0 release rather than buried:

- **Principle #1's *causal* claim is deprecated** pending a pre-registered replication study (Law VI / [LAW_VI_PRE_REG_v1.md](LAW_VI_PRE_REG_v1.md)). The verdict lands by 2026-07-20; v1.5 ships 2026-07-25 carrying it. If the study earns the claim back, it earns back; if it doesn't, the retraction stays and the framework still ships.
- **Mission Command Architecture is validated at Platoon scope only.** Rungs 3–9 (Company through Combatant Command) are hypothesis, named as such. Company-scale validation is the v2.0 gate (Q4 2026).
- **The hard release gate — one external builder running the Kit cold and producing a working product instance — has not been cleared.** The v1.0 ship and the Brad Hampton channel outreach are how the Kit gets in front of external eyes. If no external builder runs by 2026-07-31, v2.0 prep pauses and positioning gets re-evaluated.

See [RELEASE_NOTES_v1.0.md](RELEASE_NOTES_v1.0.md) for full detail on each.

## Repository layout

**Doctrine prose:**
- [THE_BUILDERS_DOCTRINE.md](THE_BUILDERS_DOCTRINE.md) — the 13 principles
- [META_DOCTRINE.md](META_DOCTRINE.md) — six methodological laws governing the doctrine itself
- [MISSION_COMMAND_ARCHITECTURE.md](MISSION_COMMAND_ARCHITECTURE.md) — portfolio-wide agentic architecture (ADP 6-0, runtime authority)
- [TRAINING_ARCHITECTURE.md](TRAINING_ARCHITECTURE.md) — portfolio-wide readiness doctrine (ADP 7-0, certify-to-standard before trust); folds in its own civilian glossary
- [PROMPT_DOCTRINE.md](PROMPT_DOCTRINE.md) — universal prompt structural rules
- [WORKING_BACKWARDS.md](WORKING_BACKWARDS.md) — Amazon PR/FAQ-first scoping discipline
- [EXPLAINER.md](EXPLAINER.md) — plain-language translator (start here)

**The Kit:**
- `kit/coverage.py` — single-file scorer; 88 KIT:FIELD blocks across 8 templates
- `kit/templates/` — STORY, COMMANDMENTS, REFUSAL_LIST, CRISIS_TRIGGERS, SPECIALIST_TEMPLATE, AGENT_DOCTRINE, SECURITY, PR_FAQ
- `kit/onboarding/` — interview runners with `depends_on` graphs that enforce authoring order

**The chassis (`kit/chassis/`):**
- `crisis_floor.py` — Crisis-line detection and routing (unkillable per Principle #11)
- `approval_queue.py` — Gates irreversible actions to founder approval (Principle #4)
- `user_context.py` — Per-user data isolation (Principle #5; ContextVar with LookupError-on-unset)
- `specialists.py` — Named-agent registry (Principle #10)
- `aar.py` — After-Action Review loop (truth-as-architecture per Principle #6)
- `prompt_guardian.py` — Drift detection against per-product commandments
- `reflection_gate.py` — Principle #12 primitive; runs before every `declare_done`
- `authority_gradient.py` — Mission Command Architecture primitive (Tier/Channel enums + tool-class table)
- `founder_romance_detector.py` — Regex linter for observer-bias patterns; pre-commit hook on this repo

**Empirical evidence + audit trail:**
- [STORY.md](STORY.md) — founder narrative; the lived experience compiled into the doctrine
- [LAW_VI_PRE_REG_v1.md](LAW_VI_PRE_REG_v1.md) — pre-registered analysis plan for the biographical-substrate replication study
- [STRESS_TEST_v1.0.md](STRESS_TEST_v1.0.md) — propagation test results
- [ARTIFACT_AUDIT_2026-05-01.md](ARTIFACT_AUDIT_2026-05-01.md) — audit at v1.0 lock
- `OPERATOR_DOGFOOD_ASYMPTOTE_FINDING_2026-05-18.md` — evidence-of-method finding from running the doctrine against its own work
- [CANDIDATES_v1.2.md](CANDIDATES_v1.2.md) — historical doctrine-version candidate log (closed)
- `archived-prose/` — retracted claims preserved as falsification evidence (Law VII)

## How to use it

1. Read [EXPLAINER.md](EXPLAINER.md) to decide if the framework matches your build philosophy.
2. Clone the repo. Run `python kit/coverage.py --list` to see the eight templates.
3. Run `python kit/coverage.py --interview` to walk through authoring your own product's templates in dependency order.
4. Wire the chassis components into your product. Each `kit/chassis/*.py` ships with unit tests showing intended usage.
5. Install the pre-commit hook (`.pre-commit-config.yaml`) so the founder-romance detector runs on every commit to your own doctrine surfaces.

If a clean room cannot rebuild your product from doctrine and commits, you have not built a product. You have built a snowflake. That is the test.

## License + IP

The v1.0 license is being finalized with counsel (Peter Lemire). Until the formal LICENSE file lands: all rights reserved by Hans Prahl. The methodology and doctrine prose are publishable and citable; downstream productization is gated on the engagement letter being signed.

Subsystem A (the closed loop in Operator) is patent-pending. The free / paid split is documented in [PRODUCTIZE_VS_LICENSE_DECISION.md](PRODUCTIZE_VS_LICENSE_DECISION.md): the Assayer scorer + this doctrine ship free; commercial productization, audit, and certification surfaces are paid.

For commercial inquiries, contact Hans Prahl directly.

## Contact

- AI Tradecraft, by Hans Prahl — `hans.t.prahl@gmail.com`
