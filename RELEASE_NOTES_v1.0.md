---
title: The Builders' Doctrine — v1.0 Release Notes
version: v1.0
release_date: 2026-06-01 (target)
status: DRAFT — for Phase 2 review, locks 2026-05-30
authority: Hans Prahl
companion_artifacts: RELEASE_PLAN_v1.md, META_DOCTRINE.md, LAW_VI_PRE_REG_v1.md, BANDWIDTH_OVERLAY_2026-05-15.md
---

# The Builders' Doctrine — v1.0

The Builders' Doctrine is a methodology for compiling lived experience into AI-product behavior. Ethics encoded as commandments. Refusals named explicitly. Agents calibrated against truthful outcomes. v1.0 is the first public release.

**What you get in v1.0.** The doctrine prose (13 principles, six methodological laws). The Kit (templates + interviews + a single-file coverage scorer). The chassis (eight portable runtime components). Two empirical experiments at Platoon scale. A versioned roadmap with dated v1.5 + v2.0 commitments.

**What v1.0 names as not yet proven.** The most-cited principle's *causal* claim is deprecated pending a replication study committed for v1.5. The Mission Command Architecture is validated at Platoon scope only; rungs above are hypothesis. The hard release gate — one external builder running the Kit cold — has not been cleared. Each is named explicitly in the sections below.

---

## 1. What ships in v1.0

### 1.1 The doctrine

- **`THE_BUILDERS_DOCTRINE.md`** — 13 principles. Seven foundational ethics (the code is the story, the moat is the memory, designed to be needed less, chain of command over autonomous AI, data sovereignty, truth as architecture, Stoic commandments). Six operational doctrines (the Refusal, AI as co-author, Named specialists, Crisis floors, What else? — active extraction, The Long Horizon). Each principle traced to its source moment and to the code that enforces it.
- **`META_DOCTRINE.md`** — six formal laws (V–X) governing how the doctrine is allowed to make claims. Law V (Echelon Decay Gate). Law VI (Biographical Falsification Gate). Law VII (Provisional Doctrine Rule — holds require execution dates). Law VIII (Meta-Schedule Gate — bandwidth overlay before milestones). Law IX (Delegation Threshold — single-point-of-failure protection). Law X (Execution Threshold + cap on doctrine bloat).
- **`MISSION_COMMAND_ARCHITECTURE.md`** — portfolio-wide agentic architecture. ADP 6-0's seven principles of Mission Command mapped to LLM-agent properties. Three-tier Platoon Pattern (Squad Leader / Platoon Leader / Soldier). Authority Gradient with officer / NCO / soldier tiers and overridable tool-to-class table. Staff Channel for advisory-never-override agents. **Scope in v1.0: Platoon-validated only.** Rungs 3–9 (Company → COCOM) are hypothesis, not validated architecture.
- **`ADP_6_0_TRANSLATION.md`** — civilian glossary for the Army vocabulary used throughout MCA and the doctrine.
- **`PROMPT_DOCTRINE.md`** — universal structural rules for every prompt across every product. The rubric every product's Prompt Guardian enforces.
- **`WORKING_BACKWARDS.md`** + **`AMAZON_LP_CROSSMAP.md`** — Amazon PR/FAQ-first scoping methodology. Operationalizes Principle #13 at the scoping layer.
- **`STORY.md`** — origin narrative; the methodology's autobiographical source.

### 1.2 The Kit

- **`kit/coverage.py`** — single-file scorer with three CLI surfaces (`--score`, `--list`, `--interview`). Scores 88 fields across 8 templates.
- **`kit/templates/`** — eight templates (STORY, COMMANDMENTS, REFUSAL_LIST, CRISIS_TRIGGERS, SPECIALIST_TEMPLATE, AGENT_DOCTRINE, SECURITY, PR_FAQ) with `KIT:FIELD` markers.
- **`kit/onboarding/`** — eight interviews with `depends_on` graphs that enforce authoring order. A builder cannot author CRISIS_TRIGGERS before STORY's `the_users` field is populated; cannot author SPECIALIST_TEMPLATE before COMMANDMENTS exists.

### 1.3 The chassis

Eight portable runtime components. 230 unit tests. 8 parity tests against TOP's production constants — these prove fidelity to the source product, not generality across all app shapes. Portability to other shapes is verified by reading the adapter pattern and matching interface contracts.

| Component | Doctrine source | Surface |
|---|---|---|
| Crisis Floor | Principle #11 | Parameterized phrase set + response string; 14-phrase TOP parity |
| Approval Queue | Principle #4 | Action shape + on-disk JSON; Option A adapter pattern in `WIRING_DIAGRAM.md` |
| Per-User Context | Principle #5 | ContextVar with `LookupError` on unset — no silent fallbacks |
| Named Specialists | Principle #10 | Registry interface; accepts arbitrary specialist identifiers |
| AAR Loop | Principle #6 | Outcome-scale + persistence interface |
| Prompt Guardian | Principle #6 + PROMPT_DOCTRINE | Structural scoring rubric; Borg-ported to TOP + Custer (`8a47d39`, `ca8aa33`) |
| Reflection Gate | Principle #12 | Scope-aware (operator_tool / wellness / founder); 29 unit tests |
| Authority Gradient | Mission Command Architecture | `Tier` / `Channel` enums + overridable tool-class table; 43 unit tests; Funkytown 02 N=3 validation |

### 1.4 The empirical record

- **Funkytown Experiment 01** — Platoon-scale ablation, N=3 × 7 stages, ~$64 total cost. Validated the Platoon Pattern as functional architecture. Stage 7's biographical-substrate finding is deprecated per Law VI (see §2).
- **Funkytown Experiment 02** — Authority Gradient validation, N=3, 2026-05-13. Mean 61.1% in-unit resolution. 0 tier-scope violations. 0 hard-floor breaches. Validates the Authority Gradient chassis primitive at Platoon scale.

Validated rungs of the MCA scale ladder (Squad → Platoon → Company → Battalion → Brigade → Division → Corps → Army Group → COCOM): **Squad and Platoon (rungs 1 and 2 of 9).** Rungs 3–9 are hypothesis.

### 1.5 The brand stack (locked 2026-05-05)

```
AI Tradecraft (umbrella, by Hans Prahl)
├── Assayer            — free public scorer + doctrine document
├── The Builders' Kit  — paid operationalization (this repo's kit/)
└── Operator           — patented closed-loop implementation
```

v1.0 is the public release of the doctrine + the free Kit. Operator's commercial release is a separate timeline.

### 1.6 Commercial structure (provisional lock 2026-05-20)

v1.0 ships under a **Hybrid** commercial structure. Operator (Subsystem A patent-pending), the AI Tradecraft umbrella, and the audit + certification function remain Hans-owned under all scenarios. The Builders' Kit operationalization layer (hosted onboarding, fielding deployments, customer success) is open to license when a real third-party counterparty surfaces. Legal instruments for any future licensing defer to counsel review at the point a deal is named — none are required for the v1.0 lock itself.

The structure is provisional. Mandatory re-review at 2026-07-31 release-gate check per the release-cadence framework. Full rationale, four-lens rubric scoring, and counsel-gated-question appendix in `PRODUCTIZE_VS_LICENSE_DECISION.md`.

---

## 2. What we deprecated in v1.0

**Principle #1 — "the code is the story" — ships with a deprecation notice on its *causal* claim.** The doctrine prose is unchanged. What is deprecated is the methodological claim that *biographical substrate is causally load-bearing in agent decision-making* — i.e., that biographical input is what makes the resulting product better than a generic-input control.

Stage 7 of Funkytown Experiment 01 was N=3 per arm on one engineered brief, no blinded controls, no reverse arm. The evidence was insufficient for the weight of the claim. Adversarial review on 2026-05-13 named it; we accepted the catch.

**Scope.** Chassis and methodology ship forward with their own measurement surfaces (`META_DOCTRINE.md §VI`); the deprecation is scoped to Law I causal claims, not engineering or structural claims.

**What v1.5 settles.** The Law VI replication study (108 runs, 3 arms, 3 briefs, blinded controls, statistician sign-off, OSF.io pre-registration) returns one of three verdicts on 2026-07-25: *earned* (principle restored with empirical citation), *qualified* (principle restated with measured scope), or *retracted* (principle removed; framework continues with chassis + methodology unchanged). The pre-registration v1 is in this repo today (`LAW_VI_PRE_REG_v1.md`).

---

## 3. What ships in v1.5 — binding commitments

Per Law VII (Provisional Doctrine Rule), every hold in the framework carries an execution date.

| Date | Deliverable | Gate |
|---|---|---|
| 2026-06-22 | External statistician engaged | Cohort 84 referrals / DU stats clinic / paid lane |
| 2026-07-01 | LAW_VI_PRE_REG_v2 with statistician sign-off | Power calc, multi-comparison correction, exclusion criteria refined |
| 2026-07-05 | OSF.io public pre-registration | Plan locked publicly before any v1.5 experiment data collected |
| 2026-07-15 | Law VI experiment complete | 108 runs, 3 arms, 3 briefs (fragile-venture / regulatory-compliance / wellness-shaped) |
| 2026-07-20 | Law VI verdict | Statistician runs pre-registered analysis; mechanical earn / qualify / retract |
| **2026-07-25** | **v1.5 ships** | Principle #1 status updated in public doctrine |

---

## 4. What ships in v2.0 — provisional

| Commitment | Target window | Gate |
|---|---|---|
| Company-scale MCA validation | Q4 2026 | Funkytown Exp 03+ with Law V harness (N≥9 full-hierarchy + live cross-echelon conflict injection) |
| Community-replication study | Q4 2026 — Q1 2027 | Post-v1.0 traction; uses v1.0 Kit as the replication harness |
| Industry case studies | Q1 2027 | Requires v1.0 in production at 3+ external builders |

**Auto-truncate triggers (selected from `META_DOCTRINE.md §X`):**

| Trigger | Action |
|---|---|
| v1.0 ship slips past 2026-06-08 | Phase 2 strips to minimum: doctrine + chassis + Kit + release notes; landing page + outreach defer |
| v1.0 ships but no external builder runs Kit by 2026-07-31 | v2.0 prep pauses; positioning re-evaluated; release gate has not moved |

Any prose-only commitment past its date converts to "deferred indefinitely until measured evidence ships." Slip enforcement is mechanical, not founder discretion. Full trigger register: `META_DOCTRINE.md §X`.

---

## 5. The methodological commitment

The doctrine governs what the builder does. META_DOCTRINE governs what the doctrine itself must do to remain honest. v1.0 ships six formal laws (V–X) as the public methodological commitment.

- **Law V — Echelon Decay Gate.** Any rung-N validation claim on the MCA scale ladder requires N≥9 full-hierarchy runs with live cross-echelon conflict injection. Squad + Platoon validated; rungs 3–9 are hypothesis until measured.
- **Law VI — Biographical Falsification Gate.** Any Law I causal claim requires the replication discipline named in §2.
- **Law VII — Provisional Doctrine Rule.** Every hold in the framework carries an execution date pointing at a falsification experiment, or it gets retracted.
- **Law VIII — Meta-Schedule Gate.** Any multi-workstream timeline carrying doctrinal claims requires published hours budget, weekly tripwires, and pre-registered truncation criteria before first milestone.
- **Law IX — Delegation Threshold.** Any workstream exceeding 40 founder hours or carrying >3 parallel deliverables requires explicit delegation before dates lock.
- **Law X — Execution Threshold + cap.** No new law or deliverable may be added from adversarial review until the prior packet's top actions have shipped with measurement surface. META_DOCTRINE caps at six laws.

The laws are not aspiration. They are the gates the doctrine itself has to pass before it ships a claim.

---

## 6. The hard release gate

v1.0 is a public release of the methodology. It is **not** a release-gate clearance.

The release gate is: **one external builder runs the Kit cold and produces a working product instance.** That gate has not moved. v1.0 ships to put the Kit in front of external eyes — Brad Hampton outreach 2026-06-02; cohort 84 distribution 2026-06-03 → 06-10; first-external-builder signal target 2026-06-15.

If no external builder runs the Kit by 2026-07-31, v2.0 prep pauses and positioning gets re-evaluated.

---

## 7. How to engage

- **Read the doctrine.** Start with `THE_BUILDERS_DOCTRINE.md`. If the Army vocabulary in `MISSION_COMMAND_ARCHITECTURE.md` is unfamiliar, read `ADP_6_0_TRANSLATION.md` first.
- **Run the Kit.** Score your existing product's STORY / COMMANDMENTS / REFUSAL_LIST / CRISIS_TRIGGERS / SPECIALIST_TEMPLATE / AGENT_DOCTRINE / SECURITY / PR_FAQ surfaces against the rubric. The interview runner walks a new build through authoring them in `depends_on` order.
- **Port the chassis.** `kit/chassis/` is engineering. Eight components, 230 tests, 8 parity tests against production. Drop-in for any product that wires its public functions through an adapter (see `WIRING_DIAGRAM.md`).
- **Send a builder catch.** If you run the Kit cold and something breaks — a template field that doesn't map, an interview question with no good answer, a chassis component that won't port — open an issue. Builder catches are what move v1.5 and v2.0.

**Worked example — Crisis Floor in TOP.** The Crisis Floor chassis component is parameterized at import time with a phrase set and response string. TOP (the veterans-wellness product) configures it with 14 distress phrases parsed from `agents/telegram_bot.py` and a response string that names the Veterans Crisis Line (988, press 1). The chassis is parity-tested against TOP's literal `_CRISIS_PHRASES` set and `_CRISIS_RESPONSE` string — identical booleans on every phrase, verbatim response text. This shows what fidelity to a source product looks like; it does not by itself prove portability to other product shapes. A builder porting Crisis Floor into a non-Telegram, non-wellness product configures the parameters for their domain.

---

## 8. What this release is not

- It is not a claim that biographical substrate is causally load-bearing. That claim is deprecated. Law VI replication settles it in v1.5.
- It is not validated MCA above Platoon scale. Squad + Platoon only.
- It is not a finished product. The Kit ships; commercial operationalization (hosted onboarding, audits, certification) is downstream of the release-gate clearance.
- It is not the framework's stable state. v1.5 is committed. v2.0 is provisional. The doctrine is a living document; the laws govern how it is allowed to change.

---

## 9. Authority

Hans Prahl. Material edits to the doctrine require my approval and a version bump. Editorial edits (typo, clarification, example) do not.

---

*v1.0 — 2026-06-01 — Ships what is proven. Names what is not. Commits dates to both.*
