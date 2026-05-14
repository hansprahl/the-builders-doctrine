# ADP 6-0 — Civilian Translation

**Status:** v0.1 — 2026-05-13 evening.
**Purpose:** Bridge the Army vocabulary that load-bears across `MISSION_COMMAND_ARCHITECTURE.md`, `THE_BUILDERS_DOCTRINE.md`, and `META_DOCTRINE.md` into language a non-military reader can follow on first read without losing the doctrinal precision.

This is a glossary plus a few short essays. Read top-to-bottom the first time. Reference-skim after that.

---

## Why this exists

The Builders' Doctrine ports U.S. Army field doctrine onto an LLM substrate. Army field doctrine is precise — every term has a fixed meaning, refined over centuries of iteration under conditions where coordination failures killed people. That precision is the reason we ported it. It is also the reason a civilian reader bounces off the artifacts on first contact.

Grok's 2026-05-13 adversarial review named the audience risk plainly: a venture capitalist, a customer, or a non-veteran builder who opens `MISSION_COMMAND_ARCHITECTURE.md` and meets "S-2-shape," "OPORD-down/SITREP-up," "PSG vs 1SG," "Authority Gradient," and "PIR/EEI" in the first three pages will close the tab. The doctrine cannot earn its audience if the audience cannot parse the doctrine.

The fix is not to soften the doctrine. The fix is this document — a translation surface that preserves every load-bearing distinction while giving civilian readers a path in.

**Rule for contributors.** When an Army term first appears in any externally-facing artifact (pitch decks, PR/FAQs, public README, EXPLAINER.md, customer-facing prose), inline a civilian gloss the first time it appears. Example: *"Commander's Intent (the 'why' behind a task — what success looks like and which constraint takes precedence under pressure)."* The translation table below is the canonical source for those glosses.

---

## ADP 6-0 in one paragraph

ADP 6-0 is the U.S. Army's published doctrine on **Mission Command** — the philosophy of how Army units are commanded and controlled. Its core idea: under uncertainty and pressure, centralized detailed orders fail because reality diverges faster than commanders can re-plan. The answer is to push decision authority down to the lowest competent echelon, bind it with a clear *commander's intent* (the why, not just the what), and let subordinates take disciplined initiative within their scope. The doctrine spells out seven principles, two parallel command structures (line and staff), and a small set of message protocols that make decentralized execution actually work instead of degenerating into chaos. We ported all of it.

---

## The COCOM-as-destination clarification

The MCA scale ladder runs:

> Squad → Platoon → Company → Battalion → Brigade → Division → Corps → Army Group → COCOM

A reader who skims that line easily misreads it as "the architecture works at COCOM scale today." It does not. Today we have **Squad** and **Platoon** validated (Funkytown experiments 01 and 02). Every rung above is unvalidated — and per Law V (the Echelon Decay Gate, see `META_DOCTRINE.md`) cannot be claimed validated without N≥9 full-hierarchy runs with live cross-echelon conflict injected.

**COCOM is the objective, not the pitch.** The full scale ladder names *where this is going* — one human operator commanding a theater command's worth of LLM-substrate agents, through Mission Command's chain of intent. That is the destination thesis. It is not the current product claim. Pitch language must keep these distinct. Confusing them is the over-claim Grok caught us on for Company-scale; the same discipline applies to every rung above it.

If a civilian reader takes one thing from this document, it should be that. The climb is honest. We have climbed two rungs of nine. The other seven are the work.

---

## The scale ladder — civilian gloss

Each rung is roughly 3–4× the size of the rung below. Sizes are rough; what matters is the **roles that emerge** at each new rung (the staff functions, the senior NCOs, the parallel command structures) which did not exist below.

| Rung | Army size | Civilian gloss | LLM-agent count (rough) |
|---|---|---|---|
| **Squad** | ~9 soldiers + leader | Small team — one lead, a few executors | ~4 agents |
| **Platoon** | ~30 soldiers across 3 squads | Team-of-teams — one lead overseeing several small teams | ~13 agents |
| **Company** | ~150 across 3 platoons + staff | First scale where the leader can't personally hold every domain; specialists attach (intel, logistics) | ~50 agents |
| **Battalion** | ~700 across 3–4 companies + full staff | Full staff functions become non-optional (personnel, intel, ops, logistics, signal) | ~200 agents |
| **Brigade** | ~3,500 | Multi-battalion combined-arms organization | ~700 agents (projected) |
| **Division** | ~15,000 | Standing major formation — strategic-tactical bridge | ~3,000 agents (projected) |
| **Corps** | ~45,000 | Multi-division operational formation | (projected) |
| **Army Group / Field Army** | ~100,000+ | Theater-level ground formation | (projected) |
| **COCOM (Combatant Command)** | hundreds of thousands | Theater command — strategic-level coordination across services, regions, partner nations. A four-star general's scope. | (projected) |

**Validation status as of 2026-05-13:** Squad and Platoon validated. Company-and-above are doctrine on paper, not validated architecture. Law V governs how validation claims at each higher rung are allowed to ship.

---

## Roles — civilian gloss

Roles are *functional positions*, not rank identity. The architecture reads role and authority tier; rank itself is documentation of doctrinal lineage, never an agent's name. (See MCA "Discipline — ranks are documentation, never identity.")

| Army role | Tier | Civilian gloss |
|---|---|---|
| **PL** (Platoon Leader) | Officer | Junior leader running one team-of-teams. Sets intent, allocates across the squads under them, owns the team's outcome. |
| **SL** (Squad Leader) | NCO | Hands-on team lead. Owns standards, owns task assignment, owns quality of execution within the team. Can re-do or re-task without going up. |
| **Soldier** | Soldier | Individual executor. Disciplined initiative within the task spec. "I don't know" is a calibrated stop signal, not a failure. |
| **CC** (Company Commander) | Officer | Owns the mission across multiple platoons. The trade-off-maker. Distinct from PL because PL is consumed by their own platoon. |
| **XO** (Executive Officer) | Officer | The commander's internal-operations counterpart. Owns logistics, sync, coordination — frees the commander to focus on mission and external relationships. |
| **1SG** (First Sergeant) | NCO | Senior NCO at company. Owns standards, training, discipline across all the company's NCOs and soldiers. Runs the enlisted side in parallel to the officer line. |
| **PSG** (Platoon Sergeant) | NCO | Senior NCO at platoon. Bridges PL and SLs. At small scale, collapsed into PL; emerges as a distinct role at Company. |
| **BC** (Battalion Commander) | Officer | Owns mission across multiple companies. |
| **CSM** (Command Sergeant Major) | NCO | Senior NCO at battalion. Runs the senior NCO channel across 1SGs. |

**Line vs Staff** (two parallel structures, both load-bearing):

| Channel | What it does | Civilian gloss |
|---|---|---|
| **Command (line)** | Sets intent, allocates resources, signs for outcomes. Intent flows down; situation reports flow up. | The chain of accountability. |
| **Staff / specialist** | Provides domain analysis (intel, legal, technical, ethics). Advisory authority within domain. **Never commands the line.** Always logged. | Subject-matter experts who advise but don't decide. The line decides; if it declines the advice, the decline is recorded. |

The portfolio's named specialists (Drake/OPFOR, Marshall/Legal, Sentinel/Ethics, Halsey/CTO) are all staff-channel agents.

---

## Staff numbering — civilian gloss

The Army numbers staff functions consistently from battalion upward:

| Staff section | Domain | Civilian gloss |
|---|---|---|
| **S-1** | Personnel / admin | HR, headcount, personnel actions |
| **S-2** | Intelligence | Adversary analysis, environmental scanning, red-team |
| **S-3** | Operations | Current operations, planning, training |
| **S-4** | Logistics | Supply, maintenance, transport, sustainment |
| **S-6** | Signal / communications | Networks, IT, comms infrastructure |

When you read "S-2-shape" applied to an agent, it means: an agent whose functional role is adversary/intelligence analysis, with advisory authority and no command over the line. Drake is S-2-shape. Halsey is S-6-shape.

---

## The four primary protocols — civilian gloss

The architecture moves information through the unit on a small fixed set of protocols. Two are messages (one down, one up); one is a tracked-request channel; one is durable state.

| Protocol | Army name | Civilian gloss |
|---|---|---|
| **OPORD-down** | Operations Order | A structured task brief from higher to lower. Includes: situation, mission, execution, intent ("why"), end-state, deadline. Fixed schema — not free-form prose. |
| **SITREP-up** | Situation Report | A structured status return from lower to higher. Includes: status, artifacts produced (with the executor's callsign), QC notes, what-the-higher-echelon-should-know. Fixed schema. |
| **RFI** | Request for Information | A tracked, routable question with a deadline. Gaps in knowledge become RFIs rather than being silently buried. RFIs get a registry entry, a collector, and a closing answer with source and confidence. |
| **COP** | Common Operating Picture | The unit's live, current-state picture of its environment — maintained continuously by staff, read by the commander to make decisions. Distinct from a report (static, generated, consumed) — the COP is maintained, current, and acted on. |

Two more protocols sit on top of these for larger units:

| Protocol | Civilian gloss |
|---|---|
| **CCIR** (Commander's Critical Information Requirements) | Pre-declared interrupts: "wake me immediately if X happens." The commander does not poll; the unit pages them. |
| **PIR / EEI** (Priority Intel Requirements / Essential Elements of Information) | Pre-defined intelligence questions that drive proactive collection. |
| **Battle rhythm** | The scheduled cadence of briefs, syncs, debriefs. Not "whenever" but "0600 morning brief, 1200 mid-day SITREP, 1800 evening debrief." |

---

## Other terms that show up

| Term | Civilian gloss |
|---|---|
| **Commander's Intent** | The *why* behind a task — what success looks like and which constraint takes precedence under pressure. Decentralized execution depends on every subordinate carrying this, not just the order. |
| **Mission Orders** | Orders that specify *what* and *why*, leaving *how* to the executor's judgment. Opposite of detailed step-by-step direction. |
| **Disciplined Initiative** | Acting within scope when reality diverges from the order. Not freelancing; not waiting for permission either. Bound by intent, scope, and the integrity to flag ambiguity rather than invent. |
| **Prudent Risk Acceptance** | Honest confidence reporting under uncertainty. Calibrated "I don't know" as a stop signal. Not optimism. Not pessimism. Calibration. |
| **Mutual Trust** | Higher echelons do not micromanage lower internals. Higher trusts the lower's QC and structured return. In our architecture this is enforced by context isolation — higher reads SITREP, not soldier internals. |
| **Shared Understanding** | Doctrine inherits per echelon. Founder commandments are subset for each tier without contradiction. Everyone is operating from the same substrate. |
| **MDMP** (Military Decision-Making Process) | The commander's planning subroutine — the cognitive loop that produces a clean OPORD. Steps: receipt of mission → mission analysis → COA development → approval → orders production. MDMP is *what the commander does in their head before issuing OPORD-down*. |
| **Running Estimate** | A continuously-updated staff product. "What is the current state of enemy/friendly/terrain/weather, updated continuously." Feeds the COP. |
| **Authority Gradient** | The three-tier (officer/NCO/soldier) mapping of which action class an agent may resolve without escalating. Not a bypass of human approval at the world boundary — a routing rule for what stays internal versus what must escalate. |
| **Hard floor (Principle #4)** | Irreversible / world-boundary actions require the human's explicit approval. The Authority Gradient routes approval inside the unit; it does not move this floor. |
| **K/I/G discipline** | Known / Inferred / Gap — every claim is tagged with its epistemic status. Gaps become RFIs, not silent assumptions. |
| **Echelon** | A level in the command hierarchy. Squad is an echelon. Platoon is an echelon. Soldiers are not. |
| **Span of control** | How many direct reports a leader can effectively coordinate. Doctrine says ~3-7 per echelon; above that, coordination breaks. |
| **Recursive composability** | Squad-of-fire-teams is a unit. Platoon-of-squads is a unit. Same rules apply at every echelon. Scale is recursion, not re-architecture. |

---

## How to use this document

**Internal artifacts** (memory, experiment write-ups, chassis source, architecture docs) — use the Army vocabulary directly. Precision matters more than first-read accessibility.

**External artifacts** (pitches, PR/FAQs, EXPLAINER.md, public README, customer prose) — inline the civilian gloss the first time each Army term appears. Link back here for the full table.

**Verbal use** (talking to a VC, a customer, a builder who didn't serve) — lead with the civilian gloss, layer the Army term in as the precision-vocabulary callout. "What we call *commander's intent* in the doctrine — meaning the *why* behind a task — is the load-bearing piece."

The doctrine's source is Army field manuals. Its audience is mostly not Army. The translation surface is how those two facts coexist without one strangling the other.
