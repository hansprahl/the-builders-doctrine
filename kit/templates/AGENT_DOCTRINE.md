# AGENT_DOCTRINE

**The engineering spec for how this product's multi-specialist agent system remembers, calibrates, and reacts.** Eleven components in three layers. Each component is a specific capability with a specific implementation path, failure modes, and a self-test. AGENT_DOCTRINE is *how the machine works*; COMMANDMENTS, REFUSAL_LIST, and STORY are *why*.

The Method does not require all eleven components to be implemented at v1. It requires that every component is *named*, that those that are implemented are documented to the depth of "a new contributor can find the code and exercise it," that those that are not implemented are marked with reasoning (not absence), and that the loop they form together is described in product-specific language — not boilerplate.

The eleven are numbered to stay comparable across products in the portfolio. Gaps or renames should preserve the numbers so test output stays diffable.

---

## Posture

<!-- KIT:FIELD name="agentic_posture" required="true" min_words="60" -->
[Name what kind of multi-agent system this is. How many specialists. Who orchestrates. What "specialist" means in this product (a domain owner with its own prompt and tool allowlist? a routed sub-graph? a separate process?). What the orchestrator is not allowed to do (e.g., "the orchestrator never calls tools directly — only `ask_*` specialist wrappers"). Trace to STORY.md `the_users` if the population's sensitivity sets architectural constraints (per-user isolation, approval routing, etc.).]
<!-- KIT:END -->

---

## Design principles

These five principles are portfolio-shared and apply by default. Override or add product-specific principles in the field below; do not delete the defaults without justification.

1. **Accumulate, don't forget.** Every meaningful action leaves a trace in durable storage. Hot state is fine in JSON; doctrine-tracked state goes in a queryable graph.
2. **Calibrate confidence against reality.** Specialists report confidence; AARs record outcomes; the gap is the learning signal.
3. **React, don't poll.** When state changes, the system fires an event. Subscribers respond. Cron is for clock-driven work only.
4. **Namespace the new stuff.** Files added for the doctrine namespace cleanly so they coexist with pre-existing tools.
5. **The framework is additive.** Nothing in the doctrine is required for a specialist to *function*. The doctrine makes specialists *better*, not *possible*.

<!-- KIT:FIELD name="design_principles_additions" required="false" min_words="40" -->
[Product-specific principles that extend the defaults. Examples - "Mechanical short-circuits beat LLM routing for high-stakes deterministic actions"; "Per-tenant isolation is enforced at the entity level, not just the API"; "Voice rendering never initiates — only confirms a written event."]
<!-- KIT:END -->

---

## Targets and thresholds

The numbers that tell you whether the doctrine is working. Initial targets are starting points — measured values should replace them as real data accumulates.

| Signal | Healthy | Watch | Broken |
|---|---|---|---|

<!-- KIT:FIELD name="targets_thresholds" required="true" min_words="60" -->
[Fill the table above. At minimum: knowledge graph size after 1 week and 1 month; query latency for common lookups; DB size; confidence-block parse rate; AAR coverage of pending recommendations; per-specialist success rate (AAR-calibrated); running-estimate staleness; event-handler failure rate. Each row has three thresholds — Healthy, Watch, Broken — and "act on Watch" / "treat Broken as incident" rules. Calibrate to your own scale; TOP's numbers do not transfer to a campaign platform.]
<!-- KIT:END -->

---

## Component reference

Each component is a single capability. The shape per component is:

- **What** — one sentence on what the component does
- **Where** — file paths in this product's codebase
- **Status** — `implemented` / `partial` / `not_yet` / `na_with_reasoning`
- **Why it matters** — what the product would lose without it
- **Example** — a code or interaction snippet a contributor can lift
- **Failure modes** — at least 3, each with mitigation

If a component is `na_with_reasoning`, the field captures the reasoning paragraph. Do not omit components — name and justify.

---

### Foundation layer

Infrastructure that makes a persistent multi-agent system possible at all.

#### 1. Durable History

Conversation state survives process restarts. Without this, every redeploy wipes the user's context.

<!-- KIT:FIELD name="component_1_durable_history" required="true" min_words="80" -->
[Fill: What / Where / Status / Why it matters / Example / Failure modes (≥3 with mitigations). TOP reference - LangGraph SqliteSaver checkpointing thread state per user. If your product uses a different framework or has no orchestrator-style conversation yet, name what plays this role and why (or mark not_yet with the path that gets you there).]
<!-- KIT:END -->

#### 2. Named Specialists

Each specialist has a persistent identity (a name, a scope, a tool allowlist, a system prompt). The orchestrator routes by name, not by domain string. Names are cheaper tokens, easier prompts, and carry implicit scope. Naming convention is product-specific (TOP: Vera/Rex/Scout/Atlas/Recon/Forge/Maven; Operator: military-call-sign style; Custer: campaign-staff role names).

<!-- KIT:FIELD name="component_2_named_specialists" required="true" min_words="80" -->
[Fill: What / Where / Status / Why it matters / Example / Failure modes. Include - the naming convention used in this product, where the registry lives, the scope-non-overlap rule, the surface rule (do specialist names ever reach the user-facing response?). Reference SPECIALIST_TEMPLATE.md for the per-specialist authoring path.]
<!-- KIT:END -->

#### 3. Token Trimming

The system enforces a hard token budget on conversation history sent to the LLM, preserving message-pair integrity (no orphaned tool_call without its tool_result). Without trimming, long conversations either crash, degrade, or quietly cost more than the user noticed.

<!-- KIT:FIELD name="component_3_token_trimming" required="true" min_words="60" -->
[Fill: What / Where / Status / Strategy (which trim algorithm, which budget) / Fallback if trim raises / Failure modes (budget too low, budget too high, malformed sequence triggers fallback that loses guarantees). If your product does not yet have a multi-turn LLM loop, this can be `not_yet` with the path.]
<!-- KIT:END -->

#### 4. Specialist Routing

The orchestrator decides which specialist(s) to call for a given request. Multi-specialist requests fan out and synthesize. High-stakes deterministic actions bypass the LLM via mechanical short-circuits.

<!-- KIT:FIELD name="component_4_specialist_routing" required="true" min_words="80" -->
[Fill: What / Where / Status / Routing principle (LLM-decided vs deterministic) / Mechanical short-circuit examples (when does routing skip the LLM entirely and why?) / Failure modes (LLM picks wrong specialist, calls one when request spanned two, buries pending-approval prompt). Trace to COMMANDMENTS.md if approval-passthrough is doctrine, not convention.]
<!-- KIT:END -->

#### 5. Proactive Intelligence

Background processes that act without being asked: morning briefings, evening check-ins, monitor jobs, at-risk detection, scheduled outreach. The dependency test applies — proactive output must make the user *more capable*, not *more reliant*. This is the component most at risk of violating the founding ethic.

<!-- KIT:FIELD name="component_5_proactive_intelligence" required="true" min_words="80" -->
[Fill: What / Where / Status / Why it matters / Example (a real scheduled job registration from your code) / Failure modes (job fires when user isn't reachable, two instances overlap, "helpful" nudge becomes a notification stream) / Trace to STORY.md or COMMANDMENTS.md - the dependency test that gates new proactive features.]
<!-- KIT:END -->

---

### Memory + calibration layer

State that accumulates over time and makes the system *learn*.

#### 6. Knowledge Graph

A queryable entity/relationship store. Every doctrine component that needs to accumulate cross-cutting state writes here. Other tools read.

<!-- KIT:FIELD name="component_6_knowledge_graph" required="true" min_words="100" -->
[Fill: What / Where / Status / Schema (entities table columns, relationships table columns, indexes, journal mode) / Public API (the function names a contributor can call: create_entity, link, find_entities, get_related, count_entities, etc.) / Conventions (entity-type naming, relationship-type naming - SHOUTY_SNAKE_CASE in TOP) / What it's not (it's not a replacement for per-domain JSON state) / Failure modes (no delete API, no schema validation on JSON blobs, JSON-path scans don't index, cross-user leak risk, write contention under load).]
<!-- KIT:END -->

#### 7. Confidence Scoring

Every specialist response carries a structured confidence assessment the orchestrator parses, strips from the user-visible reply, and persists. LOW confidence is *valuable*, not failure — it tells the user where to verify. Fabrication to reach HIGH is a worse failure than an honest LOW.

<!-- KIT:FIELD name="component_7_confidence_scoring" required="true" min_words="80" -->
[Fill: What / Where / Status / Format (the exact CONFIDENCE block specialists emit) / Scale (HIGH/MEDIUM/LOW with score ranges) / Parsing function name / Persistence function name / Prompt-wiring (how specialists are instructed) / Failure modes (specialist forgets the block, emits in wrong format, performative HIGH scores, one-word reasoning) / Trace to COMMANDMENTS.md - which commandment makes "I don't know" required.]
<!-- KIT:END -->

#### 8. Running Estimates

Each specialist maintains a live snapshot of its domain. The orchestrator reads these on every turn and injects them into its routing prompt — so it routes without re-asking the specialists.

<!-- KIT:FIELD name="component_8_running_estimates" required="true" min_words="80" -->
[Fill: What / Where / Status / Per-specialist schema (which fields each specialist's estimate carries) / Public API (update_estimate, get_estimate, refresh_estimate, format_for_prompt) / Compute functions (which specialists have real compute, which are placeholders) / Storage (which entity type) / Use in prompts (the exact block format the orchestrator sees) / Failure modes (estimate goes stale, compute crashes silently, placeholder specialists never refresh).]
<!-- KIT:END -->

#### 9. After-Action Reviews

Tracks outcomes of recommendations, habits, tasks, goals, routines. Calibrates specialist confidence against reality over time. The mechanism that lets truthful data override cheap claims.

<!-- KIT:FIELD name="component_9_aar" required="true" min_words="80" -->
[Fill: What / Where / Status / Public API (record_outcome, get_pending_outcomes, get_calibration_report) / Outcome scale (success/failure/partial/abandoned, or whatever your product uses) / Calibration loop (recommendation → graph entity → outcome → linked AAR → calibration report → future confidence adjustments) / Failure modes (no one records, AAR not linked to source action, subjective outcome scale, per-specialist not per-user calibration) / Trace to COMMANDMENTS.md - the honesty commandment that makes outcome tracking required.]
<!-- KIT:END -->

---

### Reactivity layer

The shift from polling to events.

#### 10. Battle Tracking

Milestone tracking for in-flight initiatives. The MDMP origin term ("maintaining a live picture of unit status against the plan") may map to projects + stalled-detection in a personal product, to delegate-whip count + assembly-progress in a campaign, to plan history + execution status in an Operator-style autonomous agent. The mapping is product-specific.

<!-- KIT:FIELD name="component_10_battle_tracking" required="true" min_words="60" -->
[Fill: What / Where / Status / Mapping (what plays this role in your product? projects, plans, whip counts, campaign milestones?) / Why this mapping (your product probably doesn't run literal MDMP - what does it need from the battle-tracking primitive?) / Example / Failure modes (wrong grain, paused-vs-abandoned indistinguishable, etc.) / Future work (when does this grow a dedicated module?).]
<!-- KIT:END -->

#### 11. Event-Driven Architecture

An internal event bus with persistent storage. Replaces "check every N minutes" polling with "fire when state changes" reactivity. Subscribers register at startup; events persist before handlers run so a crashed handler doesn't lose the event.

<!-- KIT:FIELD name="component_11_event_bus" required="true" min_words="100" -->
[Fill: What / Where / Status / Schema (events table) / Public API (publish, subscribe, get_event_log, count_events) / Subscription model (in-memory? durable?) / Dispatch rules (exact match → wildcard → prefix wildcard) / Persistence semantics (events stored before handlers; no retry; failures swallowed) / Naming convention (`<domain>.<verb>`) / Why it matters (polling vs reactivity tradeoff) / Failure modes (subscribers in-memory only, handler crashes swallowed, no retry, synchronous dispatch blocks publisher, unbounded events.db growth).]
<!-- KIT:END -->

---

## MCA — unit structure

Mission Command Architecture (`~/Projects/the-builders-doctrine/MISSION_COMMAND_ARCHITECTURE.md`) is the portfolio's structural layer for multi-agent systems. A product authoring AGENT_DOCTRINE must declare its unit structure, how it isolates context between echelons, and what its intent-down format looks like — or mark `na_with_reasoning` if the product is single-agent and MCA does not apply.

### Unit structure

The shape of this product's unit: which echelons exist, who fills each role, how the authority gradient is encoded, and where the staff channel attaches (if any). Reference unit shapes in MCA: Squad (~4), Platoon Pattern (~13), Company Pattern (~50), Battalion Pattern (~200). Most products at v1 are Squad- or Platoon-shaped.

<!-- KIT:FIELD name="unit_structure" required="true" min_words="80" -->
[Fill: which echelons this product has and the role at each (PL? SLs? soldiers? staff specialists?). The authority_tier per role (officer / nco / soldier per the Authority Gradient section of MCA). Callsign convention (numeric like `1/2/A` or functional like `drake`). Span of control per echelon (3-7 direct reports per ADP 6-0). If this product is single-agent or non-hierarchical, mark `na_with_reasoning` and explain why MCA scale-up doesn't apply yet (e.g., single-user wellness product, validation experiment, sub-platoon team). Reference: MCA `## Roles per echelon` and `## The Authority Gradient`.]
<!-- KIT:END -->

### Echelon isolation

A load-bearing MCA property: higher echelons see SITREPs, not soldier internals. Aggregation happens at every echelon. Without isolation, flat-context multi-agent systems hit token limits at N≈20. Describe how this product enforces context isolation between echelons.

<!-- KIT:FIELD name="echelon_isolation" required="true" min_words="60" -->
[Fill: how this product prevents higher-echelon context from contaminating with lower-echelon internals. Examples - filtered tool palette per echelon (PL has `delegate_to_squad` but not artifact tools); structured return shape (SITREP_UP schema, no free-form prose); separate conversation threads per echelon. If single-agent, mark `na_with_reasoning`. Failure mode: if you don't isolate, an SL's full reasoning trace leaks into the PL's context and the unit doesn't scale past Squad.]
<!-- KIT:END -->

### Intent format

The OPORD-down format used in this product. Commander's intent (the *why*) is load-bearing — without it, decentralized execution collapses into compliance under diverging reality.

<!-- KIT:FIELD name="intent_format" required="true" min_words="60" -->
[Fill: the schema this product uses for INTENT_DOWN. Minimum fields per MCA: `addressee`, `situation`, `mission`, `execution`, `intent` (the why), `end_state` (return conditions), `deadline_steps`. If you use a custom shape, document it. If single-agent or pre-MCA, mark `na_with_reasoning`. Example from MCA: `{"addressee": "1/1", "situation": "...", "mission": "...", "intent": "...", "end_state": "...", "deadline_steps": 8}`.]
<!-- KIT:END -->

---

## Active extraction gate (Principle #12)

Principle #12 (*What else? Active extraction*) requires a Reflection Gate before `declare_done` at every tier. The agent surfaces what is unknown rather than burying it in a confident summary. "I don't know" is the calibrated stop signal. The Reflection Gate is where the K/I/G (Known/Inferred/Gap) discipline becomes load-bearing.

**Scope inversion** — per the Principle #12 doctrine, the gate has three scope conditions:

- **Operator-tool products** (Operator, Custer, Rubicon-style): apply the gate as written — the system asks *itself* what else might be true or missing before declaring complete.
- **Wellness-shaped products** (TOP and any future product where the end user is a person seeking personal change): the gate inverts — the system does **not** interrogate the user with recursive "what else?" Surveillance shape is refused. Instead the system facilitates the user asking "what else?" of *themselves*.
- **Founder scope**: the system does not extract from the founder *as a person*. STORY/MEMORY are curated by the founder, not queried.

<!-- KIT:FIELD name="active_extraction_gate" required="true" min_words="80" -->
[Fill: this product's scope condition (operator-tool / wellness / mixed) and how the Reflection Gate is implemented at each echelon's done-call. Operator-tool example: PL calls `what_else_reflection` before `declare_done`; the gate inspects the SITREP for K/I/G coverage and returns Gaps that route to RFIs. Wellness example: the gate is inverted — agent prompts user with a reflective question rather than executing recursive extraction (TOP's evening checkin shape). If this product does not yet implement the gate, mark `not_yet` with the path to implementation. Trace to MCA `## The Authority Gradient` (each tier's done-call runs its own gate) and to THE_BUILDERS_DOCTRINE.md Principle #12.]
<!-- KIT:END -->

---

## How the components compose

The value is in the loop, not in any single component. A new contributor reading this section should be able to trace one user request from inbound through every component that touches it.

<!-- KIT:FIELD name="composition_narrative" required="true" min_words="100" -->
[Walk through a typical specialist call exercising multiple components in sequence. Use real specialist names from your product. Reference shape (TOP) - user asks → orchestrator reads running estimates from the graph and injects them → routes to a named specialist → specialist works and emits CONFIDENCE block → orchestrator parses confidence, stores in graph, strips from reply → trackable recommendations create graph entities for later AAR linkage → durable history checkpoints, token trimming bounds context → state changes fire events → subscribers (proactive intelligence) react → days later AAR records outcome → calibration report shifts future confidence. Your loop will look different — write it for your product.]
<!-- KIT:END -->

---

## Validation

The doctrine self-test. A new contributor can run one command and learn whether all eleven components are operational.

<!-- KIT:FIELD name="validation_command" required="true" min_words="40" -->
[Name the test command (TOP's is `python runner.py test_doctrine`). Describe what each per-component test actually does — import-only smoke tests are not enough; real round-trip assertions against temp databases are the bar. Components that are `na_with_reasoning` skip with a marker, not a fail. The test reports `DOCTRINE: N/N components operational` where N is the count of non-N/A components.]
<!-- KIT:END -->

A complete system reports `DOCTRINE: 11/11 components operational` (or `N/N` if some components are N/A-with-reasoning). Any failure identifies which component is broken and why.

---

## Schema migrations

The doctrine's persistent stores (knowledge graph, events) are initialized with `CREATE TABLE IF NOT EXISTS`. There is no migration framework by default. The first time a real schema change is needed, follow this playbook:

1. **Add a `schema_version` table.** Track per-component version.
2. **Write a migration function per version bump.** Live alongside `_init_db` in the affected module.
3. **Run on `_ensure_db`.** After init, check version against target, apply each migration in order.
4. **Back up before running.** `cp db.sqlite db.sqlite.bak-YYYYMMDD` as the first step of any migration function.
5. **Test in a temp DB first.** Use the test suite's temp-DB context manager.

Adding migration machinery prematurely is dead code. Add it the first time a real migration is needed, not before.

<!-- KIT:FIELD name="migration_status" required="false" min_words="20" -->
[Has the product needed a real schema migration yet? If yes, document the playbook deviation and the version registry. If no, leave the default playbook in place and note "no migrations performed."]
<!-- KIT:END -->

---

## Out of scope

Features the doctrine deliberately does *not* yet provide. Naming them lets a reader know where the framework stops.

<!-- KIT:FIELD name="out_of_scope" required="true" min_words="60" -->
[List, with reasoning. Common items - per-user data isolation (if the doctrine DBs are shared across users today), encryption at rest (if doctrine writes plaintext), durable event replay (if events are fire-and-forget today), cross-user calibration (if AAR is per-specialist), automated cleanup (if entity / event growth is unbounded), a proper status dashboard. Each item names what would be required to bring it in scope.]
<!-- KIT:END -->

---

## What this file is not

- **Not the source of values.** The "why" lives in STORY.md, COMMANDMENTS.md, and REFUSAL_LIST.md. This file is the engineering spec.
- **Not exhaustive.** The eleven components are the ones the portfolio has converged on. A product may need a twelfth — add it as `12.` and propose it upstream when it stabilizes.
- **Not a fixed checklist.** A product may have valid reasons to mark components 5 or 11 as `not_yet` indefinitely. The doctrine cares that the gap is named, not that every component is shipped.

---

## Changelog

A dated record of structural changes to component implementations or schemas. Required.

| Date | Change | Author | Reason |
|---|---|---|---|
| YYYY-MM-DD | File created — bootstrap from kit template | builder | initial onboarding |

---

## Trace

- [STORY.md](STORY.md) — the founder narrative whose constraints shape architectural choices.
- [COMMANDMENTS.md](COMMANDMENTS.md) — the doctrines that components #4 (approval passthrough), #7 (honesty), #9 (calibration honesty) operationalize.
- [SPECIALIST_TEMPLATE.md](SPECIALIST_TEMPLATE.md) — the per-specialist authoring path that component #2 enforces at the per-specialist scale.
- [SECURITY.md](SECURITY.md) — the data-isolation and encryption-at-rest items in "Out of scope" trace here.
- [CRISIS_TRIGGERS.md](CRISIS_TRIGGERS.md) — the inbound-surface wrapping that components #4 (routing) and #11 (event bus) must not bypass.
