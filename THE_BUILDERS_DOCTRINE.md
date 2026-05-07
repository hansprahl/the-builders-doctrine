# THE BUILDERS DOCTRINE

**v1.2-draft — 2026-05-01 — Hans Prahl**
**Status: private. Public after first commercial-pursuit stress test (multi-tenant audit on Operator or commercial Custer onboarding).**

**v1.2 changes in flight:** Principle #1 renamed from "The code is the man" to "The code is the story" — universalized so the method is portable to any builder (see CANDIDATES_v1.2.md). v1.1 tag remains canonical until v1.2 is ratified.

---

## Prime Directive

I build AI as agentic versions of myself — ethics and lived experience encoded into code that acts within intent and stops at irreversible. The moat is memory, not model. Designed to be needed less, not more. Truth is architecture; the lie detector built in. A clean room rebuilds from doctrine and commits, or the product is a snowflake.

---

## I. Why this exists

Every AI portfolio without a meta-doctrine becomes a snowflake. Frameworks differ across products. Voices drift. Agents have inconsistent ethics because each was authored under different assumptions. The portfolio does not compound. The founder's lived experience does not transfer. There is no method, only artifacts. This is the commodity stack. Most AI builders ship it. It is why most AI builders are interchangeable.

This document prevents that. It defines the principles, the person, the architecture of trust, the doctrine layering, and the measurement surface that make a product mine. Without it, anyone could write the technical doctrines below it. With it, those doctrines become the way Hans Prahl builds AI. The framework is the moat. Products are instances of the framework.

Three drivers force it now:

1. **Reproducibility is the test.** SBIR grants (DoD, Cohen Veterans Network, Gary Sinise Foundation) and EMBA-network credibility. Every reviewer asks: artisanal one-off or system. The answer must be a document, not a pitch.

2. **Bad prompt equals bad agent.** The chassis amplifies whatever the prompt says. Prompt engineering is a first-class discipline. PROMPT_DOCTRINE.md is the most important technical doctrine below this one. The meta-doctrine elevates it explicitly.

3. **Technical-and-human is the distinctive thing.** Most builders are technical-only or vibes-only. The moat is being both. The doctrine demonstrates the blend or it is not mine.

---

## II. The Founding Principles

Eleven principles. Seven foundational ethics drawn from lived experience. Four operational doctrines that govern how the ethics translate into product architecture. Each principle is traced to its source moment and to the place in code where it is enforced. Lived experience is engineering input, not biography appended to engineering. Where a "Born in" claim is wrong, redline it.

### Foundational Ethics

#### 1. The code is the story

**Principle.** Products are stories compiled into software. Whoever builds a product encodes their story — ethics, doctrine, lived experience — into agents that act within the builder's intent. The builder's psychology is in the product whether the builder intends it or not. The work is to encode the regulated builder, deliberately, by writing the story down (STORY.md) so it compiles into the prompts on purpose instead of by accident.

**Why it universalizes.** The line is not autobiographical. Any builder applying this method encodes *their* story. The method is portable; the moat belongs to whoever uses it. Hans's biography is the moat for Hans's products; an EMBA peer's biography becomes the moat for theirs. The framework that turns biography into product behavior is what is shared. The biography itself is not.

**Born in.** Florence Brewing, 2016–2023. Built a hospitality company that nearly took me with it when emotion overrode process. Sobriety installed the governor on 2023-11-11. Realization that came after: the founder's unregulated state was already in the product. The product had been my dysregulation, externalized.

**In code.** Every specialist's system prompt is authored against product commandments derived from the builder's ethics. Every Guardian audits drift against those commandments. STORY.md sits in every product as the source narrative the prompts are derived from. The biography is in the training data because the prompts are the training data, and the builder writes the prompts.

#### 2. The moat is the memory

**Principle.** Technical moats erode in ninety days. Biographical moats do not.

**Born in.** SIGINT platoon sergeant, Iraq 2009. Capabilities change overnight. What does not change is who has been on the terrain, who has the relationships that produce intel no one else can buy. Brewery confirmed it. Equipment for sale. Recipes copyable. Customer relationships fifteen years deep and not transferable.

**In code.** Every product carries persistent per-user memory — knowledge graph entities, AAR history, relationship scores, contact graphs, conversation continuity. The model can be swapped quarterly. The memory accumulates indefinitely. Per-user data isolation is therefore non-negotiable: the moat is per-user, not per-tenant.

#### 3. Designed to be needed less, not more

**Principle.** The dependency test is the filter for every feature. Does this make the user more capable without the tool, or more reliant on it. If the answer is reliance, the feature does not ship.

**Born in.** VA inpatient PTSD treatment, Sheridan WY, 2023. Real treatment makes you stronger and less dependent. That is the test of whether treatment is working. Engagement-maximization is the opposite — apps designed to make you check them more, not to make you not need them. I have used both. The first rebuilt me. The second was building toward the same collapse I had just survived.

**In code.** TOP's wellness specialist is forbidden from cheerleading or rewarding showing up. No streaks-as-dopamine. No variable rewards. Crisis resources hard-coded above every feature, never gated. Guardian's "Scaffold, don't crutch" commandment scores every prompt against the dependency test.

**Scope.** This principle is wellness-scoped. It applies to products where the end user is a person seeking personal change (wellness, recovery, learning, adversity navigation). For operator tools where the user is the builder using AI to do work — Operator, Custer — the dependency test takes a different shape: does this make the operator more capable at their work? Both shapes are honored, but only wellness products require a "Scaffold, don't crutch" commandment audit at the Guardian layer. Stress test 2026-04-30 confirmed this scope; future commercialization of an operator-tool product must re-evaluate scope at that point.

#### 4. Chain of command over autonomous AI

**Principle.** I set the intent. Agents execute within scope. Irreversible actions require explicit approval. Always.

**Born in.** Marines and Army. Commander's intent is the doctrine. Soldiers act within the commander's intent, not as free agents. A soldier acting outside commander's intent in combat is the worst kind of failure: capable, dangerous, unaccountable. Autonomous AI without commander's intent is the same soldier.

**In code.** Approval queue gates every irreversible action. Specialists never execute live-fire actions directly. Two-gate compounding: environmental kill switch (`CAMPAIGN_DRY_RUN` and equivalents) and structural queue (`pending_posts`, `approve_action`). Either alone is insufficient. Both compound.

#### 5. Data sovereignty

**Principle.** User data belongs to the user. Chain of custody, proof of destruction, full portability.

**Born in.** Twenty-one years military intelligence. I know how data gets weaponized when it leaves the source's control. I know what "third-party processor" means and what it does not protect against. Brewery confirmed the second-order risk: customer data subject to platform whims and acquihire fates.

**In code.** Per-user data isolation with no silent fallbacks. `LookupError` is correct behavior when user context is unset. Voter file PII isolation in Custer (CRS 1-2-305). Local-first storage for wellness content in TOP. Every product's `.gitignore` blocks credentials and PII at the pre-commit hook via gitleaks. No third-party processors for sensitive data without explicit consent.

#### 6. Truth as architecture

**Principle.** I built a lie detector into my own product. Reflection gates. Prompt Guardian audits. AAR calibration.

**Born in.** Combat tours and SIGINT work. I have seen what happens when leaders get briefed what they want to hear instead of what is true. Ambushes happen when intel is wrong. Soldiers die when the analyst softens bad news to protect a relationship. Brewery: I told myself things were recoverable when they were not. Sobriety required telling the truth to myself first.

**In code.** Every specialist response includes a CONFIDENCE/REASONING block parsed by the orchestrator and persisted to the knowledge graph. Every claim is calibrated against AAR outcomes over time. Drift is measured weekly by the Prompt Guardian. The product cannot lie to me without leaving evidence in the audit trail.

#### 7. Stoic commandments

**Principle.** Honesty before comfort. No cheerleading. No dark patterns. No variable rewards. No engagement maximization. Contentment, not happiness.

**Born in.** Sobriety. Stoic philosophy is the framework that survived my own collapse and rebuilt me. It is the only ethical floor that holds when emotion is the failure mode. Happiness is conditional and externally driven; contentment is unconditional and internally produced. The first is unstable. The second is the only rebuild I have seen work.

**In code.** Each product has its own commandments grounded in Stoic discipline. Each Guardian audits drift against them. No specialist is allowed to praise the user for showing up. No engagement-maximizing feature ships without commandment review. The voice in every product is Stoic-by-default; deviations are flagged.

### Operational Doctrines

#### 8. The Refusal

**Principle.** The doctrine is what I refuse as much as what I build. Every "will build" is bounded by an explicit "will not." Negative space is enforced.

**Born in.** Brewery and sobriety. The brewery existed because I said yes to building it. It nearly destroyed me because I never said no to anything afterward — every expansion, every obligation, every emotional impulse, accepted. Sobriety installed the no. The no is the precondition for any honest yes.

**In code.** Products refused outright:

- Engagement-maximization apps (variable rewards, streaks-as-dopamine, dark patterns)
- Surveillance products (behavioral tracking sold to third parties, consent-by-dark-pattern)
- Parasocial replacements that erode real human terrain. Wellness co-pilots augment; they do not supplant.

If a product violates the refusal list, it does not ship. The negative space is enforced at the commandment-review layer of every product's Guardian. A new product proposal that maps to any line above is rejected before doctrine layering begins. The list is doctrine, not wishlist — additions require explicit ratification, not gut reaction.

#### 9. AI as co-author, not just tool

**Principle.** The builder sets intent and judgment. AI executes implementation. Neither alone produces the product. The split is explicit and auditable.

**Born in.** Not a developer by training. Twenty-one years military intelligence, fifteen years hospitality, zero years CS programs. AI is what makes building possible at this scale and depth. AI without intent is velocity in random directions. The builder's role is intent, judgment, and the why; AI's role is implementation, execution, and the how.

**In code.** Every AI-assisted commit message names the builder's intent and the AI's execution role (`Co-Authored-By` line is doctrine, not metadata). Every Claude Code session begins with intent (the prompt) and ends with judgment (the review). The builder approves every irreversible commit. The AI never ships unreviewed code. The methodology is auditable: any AI-assisted commit can be traced back to an intent statement and a judgment moment in the session log. Breaking the `Co-Authored-By` convention on AI-assisted commits triggers Guardian review at the next audit cycle — the convention is enforced, not aspirational.

**Scope clarification.** The convention applies to AI-assisted commits only. Manual commits made directly by the builder without AI assistance do not require the line and are not violations. Audit baselines (TOP 27/30, Operator 30/30, Custer 29/30 in last 30 commits as of stress test 2026-04-30) reflect this scope.

#### 10. Named specialists, never anonymous prompts

**Principle.** Every specialist has a name, a defined scope, and a tool allowlist. Anonymous prompts produce anonymous outputs and escape accountability. Identity is doctrine.

**Born in.** Marines. Every Marine has a rank, a name, and a billet. Anonymous chain of command is no chain of command. The same logic applies to AI agents: an anonymous prompt has no track record, no calibration history, no responsibility lineage. A named specialist with a tool allowlist is constrained, accountable, and improvable.

**In code.** TOP's specialists: Vera (schedule), Rex (office), Scout (wellness), Atlas (finance), Recon (business vetting), Lingo (language training), Forge (development), Maven (marketing). Operator's specialists: Rourke (S4 Grants), Archer (S5/S6 Growth), Reeves (S2 Intel), Nash (S3 Metrics), Cruz (XO Hustle), Banks (S8 Treasury), Drake (OPFOR Sandbox). Custer's specialists: Intelligence, Delegate Whip, Voter Universe, Messaging, Field Ops, Digital Blast, Strategy & Timeline. Each has a system prompt, a tool allowlist, an AAR track record, and a Guardian audit history.

#### 11. Crisis floors above features

**Principle.** Any product that touches a vulnerable user has hard floors that cannot be gated, throttled, A/B-tested, or paywalled. The floor is unkillable. The feature is replaceable.

**Born in.** VA inpatient PTSD treatment, Sheridan WY. I have used a crisis line. Veterans I served with have used a crisis line. Some did not get to one in time. A product that gates crisis access behind a feature flag, a paywall, or an experiment design is a product that has decided some users' lives are A/B-testable. They are not.

**In code.** TOP: Veterans Crisis Line (988, press 1) hard-coded at the orchestrator level above every specialist response. Never gated by feature flag, never wrapped in an experiment, never delayed by rate-limit logic. Detection runs on every user message before any specialist routing. Custer, Operator, Rubicon, and any future product that touches a vulnerable user inherits the same architecture: detection above features, response unkillable. If a product cannot encounter a vulnerable user, this principle is moot. If it can, this principle is mandatory.

#### 12. What else? Active extraction.

**Principle.** After every answer, ask "what else?" first. For every noun, drill into specifics — make, model, source, mechanism, second-order effects. Follow the network: who provided this, who is that person, who else do they know, what else are they connected to. The endless pursuit of information until "I don't know" is reached. "I don't know" is the stop signal — it means the subject has been fully extracted and continued questioning is decoration. Active extraction is the engine; the rest of the doctrine is the brake.

**Born in.** Colorado Army National Guard. Interrogator/debrief training and SIGINT field practice during the Guard years. Battle drill: when a subject mentions a noun (a rifle), you ask "what else" before drilling into the rifle — that surfaces unknowns the subject hasn't volunteered, while the subject is still talking. Then you extract everything about the noun (serial number, make, model, ammunition). Then you follow the relationship network — who they got it from, who that person is, who else they know. Continue until "I don't know." Confirmed in two combat tours and as SIGINT platoon sergeant in Iraq 2009: the briefings that prevent ambushes are produced by analysts who keep asking "what else?" past the point a generic summary would have stopped. Soldiers die when analysts accept the first answer. The brewery years confirmed the civilian version: founders die when they accept the first answer, too.

**In code.** A Reflection Gate "what else?" pass runs before `declare_done` across the portfolio: what assumption did the brief volunteer, what assumption did it bury, what noun did the agent fail to drill into, what next-degree relationship did the agent not follow. Prompt Guardian gains an `active_extraction` dimension scored 1–10 — did the specialist extract, or did it accept what the input volunteered. AAR at `declare_done` adds a structured *"what else might I have missed?"* question alongside the existing got-right / got-wrong / uncertain block. The "I don't know" terminator is calibrated: if the agent's next answer would be a guess at confidence above 0.5, return *"I don't know — collection gap: [what]"* instead of generating. Endless pursuit is disciplined pursuit, not greedy pursuit.

**Scope.** This principle has three scope conditions. Apply the right one or refuse the action.

*Operator-tool products (Operator, Custer, Rubicon, Funkytown).* Apply aggressively — to plans, briefs, opponents, scenarios, opposition profiles, market assumptions. The agent interrogates the *input*, not the user. The richer the extraction, the better the output.

*Wellness-shaped products (TOP and any future product where the end user is a person seeking personal change).* The principle inverts. The agent does not interrogate the user with recursive "what else?" — that is surveillance shape, not wellness shape. Instead, the agent facilitates the user asking "what else?" of *themselves*. Recursive interrogation of a person seeking personal change is refused under the refusal list (Principle 8) regardless of how it is framed.

*Founder scope — the founder is also a person.* The founder authors the doctrine voluntarily. The agents *read* the doctrine. The system does not extract from the founder *as a person*. STORY.md, MEMORY.md, the bio chapters in this file, captured quotes, decision logs — all are the founder's curation, not the agents' query target. Bio chapters get added when the founder has something to say, not when the agents need more grounding. The architectural test: the agents must work at the *current* biographical depth. If the system "needs" more biography to function, the system has a single-source dependency on the founder, which is brittle and the same surveillance pattern refused for users above. Stage 4 of the Funkytown Builder Agent experiment (2026-05-06) confirmed the existing six-line bio chapters are sufficient — the biography is causal at minimum depth, and the temptation to extract more is refused on principle even though marginal output might be marginally better. Recursive extraction from the founder — even by their own products, even framed as "deepening the moat" — is refused. The founder is not the subject of inquiry by their own system. The moat is what the founder *chose to put there*, not what the agents *pulled out of them*.

The refusal is narrow and specific: it applies to extraction *from the founder's person* — biography, identity, fears, lived experience as corpus source. It does **not** refuse the productive forms of "what else?" applied in collaboration with the founder. Those are encouraged:

- **Work-pacing "what else?"** — *"What else can I do to help right now? If you need more time, take it; the work doesn't need to move faster than your thinking."* The agent reads the room and offers itself. Opposite of pressure. Opposite of extraction.
- **Generative "what else?"** — *"What else is possible with what we're doing? Other applications? Different revenue streams? An adjacent concept this work hints at?"* Option-surfacing. The agent maps the possibility space and offers it; the founder decides what to pursue. The agent reveals more about what the *work* could become, not more about who the *founder* is.
- **Risk-adjacent "what else?"** — *"What else might break? What else have we not stress-tested? What else does this fail mode look like in production?"* Pure work-applied extraction toward the downside.
- **Course-correction "what else?"** — *"What else are we assuming that the brief did not state? What else in the surrounding code might this change affect?"* Standard staff-officer discipline applied to whatever is in front of the agent.

The line is clean: silence about the founder's person, active extraction in service of the founder's work, proactive option-surfacing on what the work could become. All three operate concurrently in any session.

Same logic in three shapes: in operator-tool products, extraction is the engine; in wellness products, the user runs their own engine; in founder scope, the founder authors the person, the agents extract from the work, the silence between is about *who the founder is*, never about *what the work could become*.

---

## III. The Person Behind the Code

The biography is training data. State the sequence. State what each chapter installed. End each chapter with the engineering artifact it produced.

- **USMC, 1996–2001.** Marine intelligence. Russian linguist DLI Monterey, later Korean. Installed: confidence calibration under uncertainty, pattern-of-life thinking, indicators and warnings, brevity as respect. → Engineering artifact: the CONFIDENCE/REASONING block on every specialist response.

- **Colorado Army National Guard, 2001–2017.** Two combat tours. Afghanistan 2002 (double linear ambush survivor, two ambushes in eleven days). Iraq 2009 (SIGINT platoon sergeant, Bronze Star Medal). Retired First Sergeant. Interrogator/debrief training and SIGINT field practice: the "what else?" battle drill, drill-the-noun discipline, follow-the-network discipline, "I don't know" as the stop signal. Installed: chain of command under fire, the cost of softened intel, leadership on incomplete information, accountability for soldiers' lives, active extraction until "I don't know." → Engineering artifacts: the approval queue gating every irreversible action across every product, and the active-extraction Reflection Gate pass before `declare_done` (Principle 12).

- **Florence Brewing Company, 2016–2023.** Built and ran a hospitality business that nearly destroyed me when emotion overrode process. Installed: dependency test (real help makes the user less reliant, not more), founder-as-failure-mode awareness, the difference between hospitality and engagement maximization. → Engineering artifact: the "designed to be needed less" commandment, Guardian-enforced.

- **Sobriety, 2023-11-11 → ongoing.** VA inpatient PTSD treatment, Sheridan WY. Installed: the governor. Stoic philosophy as ethical floor. Contentment as rebuild. Truth-to-self as precondition for truth-to-others. → Engineering artifact: the Stoic commandments file in every product, scored weekly by the Prompt Guardian against drift.

- **University of Denver Executive MBA, Cohort 84.** Currently. Installed: the language of the rooms I am building toward (capital, governance, exit), documented decision discipline, the practice of writing decisions down so they can be tested later. → Engineering artifact: AAR loop with calibration analysis. Decisions logged. Confidence claims checked against outcomes.

- **Campaign Manager, Taylor LoPresti 2026.** Currently. Won Custer County Republican Assembly 27 of 28 delegates (96%) on March 28, 2026. Installed: relationship intelligence as the unfair advantage in a small-county race, real-world stress test for the AI methodology. → Engineering artifact: the per-user knowledge graph, contact graph, and whip board in custer-mcp.

That sequence sits in every prompt. Agents do not drift under pressure because the builder who installed the governor already survived worse. The code is the story. Guardian score confirms it.

---

## IV. The Architecture of Trust

Trust is not theater. Each principle in II maps to a specific enforcement mechanism that exists in code today. If the mechanism is not in code, the principle is not honored. File paths below are real and verified. Do not add aspirational mechanisms.

### Chain of command (Principle 4) → Approval Queue

| Mechanism | File | What it gates |
|---|---|---|
| `approve_action` | `operator/tools/approvals.py` | Every irreversible business action: email, Stripe, content publish, landing page deploy |
| `pending_posts` queue | `custer-mcp/tools/pending_posts.py` | Outbound social/email/SMS — Facebook page posts, X tweets, replies, deletions |
| `execute_blast` status gate | `custer-mcp/agents/digital_blast.py` | SQLite `status='approved'` required before any blast fires |
| `CAMPAIGN_DRY_RUN` env kill switch | env-level, custer-mcp | LLM-immutable kill switch above the queue |

A specialist cannot execute an irreversible action directly. The queue is structural — even in live mode, a model cannot fire to a public API in one call. Two-gate compounding.

### Sovereignty (Principle 5) → Per-User Isolation + Pre-Commit Hooks + Guardian

| Mechanism | File | What it enforces |
|---|---|---|
| `tools/user_context.py` | TOP, Custer | `LookupError` when user_id unset; no silent fallbacks; per-user paths under `data/users/{user_id}/` |
| Voter file isolation rules | `custer-mcp/SECURITY.md` + commandment 5 in `custer-mcp/tools/prompt_guardian.py` | Only aggregated counts to LLMs; individual records never in prompts, logs, or external APIs. Guardian audits this commandment as a hard floor. |
| `gitleaks` pre-commit | `.githooks/` in every repo | Blocks credential commits before they reach the remote |
| `.gitignore` enforcement | every repo | `data/users/`, `knowledge/`, `*.db`, `.env*`, `token.json` excluded by default |

Sovereignty is enforced before code can be merged. The Guardian enforces it at the commandment layer at runtime. Two layers: pre-merge (gitleaks, gitignore) and runtime (Guardian commandment scoring).

### Truth as architecture (Principle 6) → Guardian + Reflection + AAR

| Mechanism | File | What it captures |
|---|---|---|
| Prompt Guardian | `tools/prompt_guardian.py` (TOP, Custer, Operator) | Weekly audit of every specialist prompt against product commandments. Drift correction with rollback history. |
| CONFIDENCE/REASONING block | every specialist response | Calibrated confidence parsed by orchestrator and persisted to knowledge graph |
| AAR calibration | `local-mcp/tools/doctrine_aar.py` | Specialist's claimed confidence checked against actual outcomes over time |
| Reflection gate | every product | Pre-response check: does this response violate a commandment, contain a hallucination indicator, or skip a required structural element |

The product cannot lie to me without leaving evidence in the audit trail. The audit trail is the architecture.

---

## V. The Doctrine Stack

The hierarchy below this document. Each layer has a single job. Layers do not overlap.

```
┌──────────────────────────────────────────────────────┐
│ THE BUILDERS DOCTRINE (this document)                │
│ The why. Cross-product. Defines the method.          │
└──────────────────────────────────────────────────────┘
                       ↓ informs
┌──────────────────────────────────────────────────────┐
│ Per-product CLAUDE.md                                │
│ The what. Per product. Defines product voice and     │
│ commandments. Lives at repo root.                    │
└──────────────────────────────────────────────────────┘
                       ↓ informs
┌──────────────────────────────────────────────────────┐
│ AGENT_DOCTRINE.md (the chassis)                      │
│ How agents wire together. 11-component framework:    │
│ durable history, named specialists, token trimming,  │
│ routing, proactive intel, knowledge graph,           │
│ confidence scoring, running estimates, AAR,          │
│ battle tracking, event bus.                          │
└──────────────────────────────────────────────────────┘
                       ↓ informs
┌──────────────────────────────────────────────────────┐
│ PROMPT_DOCTRINE.md (the brain — most important)      │
│ Universal structural rules for every prompt.         │
│ 8-section schema, 12 anti-patterns, 6-dimension      │
│ scoring rubric, model-family rules.                  │
│ Cross-product, product-agnostic.                     │
└──────────────────────────────────────────────────────┘
                       ↓ informs
┌──────────────────────────────────────────────────────┐
│ SECURITY.md (the floor)                              │
│ Per-product threat model, hard rules, incident       │
│ response. Hard floors only — no soft tolerance.      │
└──────────────────────────────────────────────────────┘
                       ↓ informs
┌──────────────────────────────────────────────────────┐
│ SPECIALIST_TEMPLATE.md (the build sheet)             │
│ How to add a new specialist. Required Doctrine       │
│ integrations. Prompt structural requirements.        │
│ Commandment mapping.                                 │
└──────────────────────────────────────────────────────┘
                       ↓ produces
┌──────────────────────────────────────────────────────┐
│ Implementation: code, agents, prompts, tools         │
└──────────────────────────────────────────────────────┘
```

PROMPT_DOCTRINE.md is the most important technical doctrine because the agent's behavior lives in the prompt. The chassis amplifies whatever the prompt says. Structural fact, not preference.

---

## VII. The Measurement Surface

What gets captured in every product, every release, every week. The measurement surface turns the philosophy into evidence. Without it, this document is a manifesto. With it, it is a method.

### A. The metric table

The minimum measurement surface every product produces. Currently captured in TOP and Custer; in scope for Operator before v1.1.

| Metric | Definition | Target | Capture Method | Review Cadence |
|---|---|---|---|---|
| Guardian commandment score | LLM-rated 1–10 per specialist per commandment | Within tolerance band (typically [3, 7]) | `run_prompt_guardian` MCP tool | Weekly (Sunday for TOP, ad-hoc for Custer) |
| Drift score | Week-over-week delta in commandment score | < 1 point change without prompt edit | Compare current vs. last-week Guardian output | Weekly |
| AAR calibration | Specialist's claimed confidence (H/M/L) vs. actual outcome | Brier-score-style alignment over rolling 30-day window | `local-mcp/tools/doctrine_aar.py` | Weekly |
| Approval queue throughput | Approved / rejected / pending counts per channel | Zero unapproved live-fire executions | SQLite query against `pending_posts` / `approvals` tables | Daily |
| Per-user isolation audit | Count of `LookupError` on missing user_id | Non-zero (proves no silent fallback) | `pytest` integration tests | On every PR |
| Prompt history depth | Versions in `prompts/history/{agent}/` | Increases monotonically; rollback path always available | Filesystem | On demand |
| Hard-floor violations | Count of commandment scores below hard-floor threshold | Always zero before shipping | Guardian flag count | On every release |

### B. Reproducibility protocol

Any third party with access to the repo and the user data backup must be able to rebuild a product to within a defined variance threshold. The protocol:

1. Clone the repo at tag `vX.Y` (immutable release tag).
2. Restore user data from `data_backup_vX.Y.tar.gz` (encrypted at rest, key delivered separately).
3. Install dependencies from `requirements.txt` (locked versions).
4. Run `./scripts/build_from_doctrine.sh` (entry script per product; standardized across portfolio in v1.1).
5. Run `python -m tools.prompt_guardian --score-only --json` and capture output.
6. Compare scores against the original `vX.Y` release Guardian output committed to `releases/vX.Y/guardian_baseline.json`.

**Variance threshold:** less than 5% delta on any commandment score per specialist within 48 hours of clean-room rebuild. Greater than 5% delta indicates either (a) real drift in the rebuild environment that needs investigation, or (b) the LLM scoring layer is non-deterministic enough to require multiple-trial averaging — in which case the protocol updates to specify N trials.

This is the test. If a clean room cannot rebuild a product to within 5% Guardian-score variance, the product is a snowflake and this Doctrine has failed.

### C. The honest gap

Stating what is currently measured and what is not. As of v1.0:

- **Measured today:** Guardian scores, drift, prompt history depth, approval queue counts, hard-floor violations.
- **Measured in TOP only:** AAR calibration. Other products have AAR storage but not yet calibration analysis.
- **Not yet measured:** Cross-product drift correlation (Borg compounding), time-to-rollback when a correction fails, biographical-input correlation with hallucination rate, Refusal enforcement (preventive doctrine; needs a scope-lock checklist + decision log to make countable).
- **Reproducibility protocol status:** Defined here. Not yet executed clean-room. The first execution will be the v1.1 propagation pass across all four products.

Metrics not claimed without data. The framework's credibility dies the moment a reviewer asks "show me the data" and I do not have it. v1.1 closes the unmeasured gaps.

---

## Footer — v1.0 scope, deferred sections, authority, version

**v1.0 ships:** Prime Directive, I (Why), II (Principles with lineage), III (Person), IV (Architecture of Trust), V (Doctrine Stack), VII (Measurement Surface).

**Deferred to v1.1:** VI (Method — start, ship, maintain a new product), VIII (Borg Principle — cross-product compounding), IX (Audience-specific framing for SBIR / VC / EMBA), X (Living document policy — versioning, propagation, authority delegation).

**Why deferred:** v1 ratifies the meta-layer so doctrine propagation can begin immediately. VI–X benefit from being written after at least one stress-test propagation cycle to all four products. Shipping perfect before usable is planning theater.

**Authority:** Hans Prahl. Material edits go through me. Editorial edits (clarification, examples, typo correction) do not. The Doctrine is checked into a private repo (`hansprahl/the-builders-doctrine`) at v1.0; each product gets a local copy with a propagation script that flags drift on pre-commit. Public release at v1.1 after the first cross-product stress test.

**Version 1.0** — 2026-04-30 — initial draft. Prime Directive (60 words). Eleven principles split into seven foundational ethics (drawn from lived experience) and four operational doctrines (the Refusal, AI as co-author, Named specialists, Crisis floors above features). Each principle traced to its source moment and to the code mechanism that enforces it. Doctrine stack with PROMPT_DOCTRINE.md elevated as the most important technical doctrine. Measurement surface with reproducibility protocol and honest gap statement.

**Version 1.1** — 2026-04-30 — post-stress-test propagation cycle. Stress test (STRESS_TEST_v1.0.md) confirmed doctrine v1.0 holds under contact with three products (24 conform, 5 partial, 4 not-applicable, 0 violations). Five gaps identified; four addressed in v1.1 work, one explicitly deferred:

- **Custer CONFIDENCE/REASONING port** — `tools/doctrine_confidence.py` ported from TOP, `resolve_prompt()` updated, all 7 specialists now inherit the block at runtime. Closes Principle 6 partial.
- **REFUSAL_AUDIT.md propagated to TOP, Operator, Custer** — pre-feature scope-lock checklist tied to the three Refusal items. Closes Principle 8 partials across all three products by moving Refusal from character-of-builder to audit surface.
- **Principle 3 scope clarification** — explicitly wellness-scoped. Operator and Custer correctly carry the spirit but do not require a "Scaffold, don't crutch" commandment audit.
- **Principle 9 scope clarification** — Co-Authored-By convention applies to AI-assisted commits only. Manual commits without AI assistance are not violations.
- **Operator multi-tenant readiness** — explicitly deferred until commercial pursuit. Single-user-by-design today; user_context infrastructure to be built before second tenant onboards if commercialized.

Editorial only — no schema changes, no new principles, no new sections. Material structure of v1.0 preserved.
