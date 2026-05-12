# Mission Command Architecture (MCA)

**Status:** Empirically validated at the Platoon scale (N=3 each across 7 ablation stages, ~$64 in API spend, Funkytown experiment 01). Provisionally adopted as the portfolio-wide agentic architecture.

**Source doctrine:** U.S. Army ADP 6-0, *Mission Command: Command and Control of Army Forces*. Mission Command is the Army's published doctrine for decentralized execution under clear commander's intent. Refined over centuries of bloody iteration. Stress-tested under conditions where coordination failure kills people.

**Claim:** Industry's "agent swarms" and "multi-agent orchestration" frameworks are reinventing this from scratch without the constraint discipline that the military earned. MCA ports the working doctrine into an LLM substrate and adds founder biography as the load-bearing constraint substrate.

---

## The seven principles, ported

ADP 6-0 lists seven principles of Mission Command. Each maps cleanly to an LLM-agent property:

| Principle (ADP 6-0) | LLM-agent property |
|---|---|
| **Competence** | Each echelon runs the appropriate model — Officer (Opus), NCO/Squad Leader (Sonnet), Soldier (Haiku). Match capability to task. |
| **Mutual trust** | Higher echelon does not micromanage lower internals. Higher trusts the lower's QC and structured return. Architectural enforcement: context isolation. |
| **Shared understanding** | Doctrine inherits per echelon. Founder commandments are subset for each tier without contradiction. |
| **Commander's intent** | Every INTENT_DOWN carries the *why*, not just the *what*. Without intent, decentralized execution collapses into compliance under diverging reality. |
| **Mission orders** | Standard message protocol: OPORD-shaped INTENT_DOWN ↓ , SITREP-shaped status ↑. Fixed schemas per direction. |
| **Disciplined initiative** | Soldiers may revise within scope; refuse outside scope; flag ambiguity rather than invent. Principle 12 ("what else?") is the in-echelon check. |
| **Prudent risk acceptance** | Honest confidence reporting. "I don't know" as calibrated stop signal. Truth-as-architecture. |

---

## The three-tier reference unit — Platoon Pattern

The smallest legitimate MCA unit. ~13 agents.

```
Platoon Leader (PL) — Officer-tier, Opus
  Tools: delegate_to_squad, what_else_reflection, declare_done
  Tools NOT available: any artifact-generation, any irreversible action without explicit approval
  Doctrine: full founder doctrine + Principle 12 + MCA addendum
  Span of control: 3 squads
    │
    ├── Squad 1/1 — Squad Leader (SL), Sonnet
    │     Tools: task_soldier
    │     Doctrine: NCO-shape subset + addressable identity
    │     Span: 3 soldiers
    │     Soldiers: 1/1/A, 1/1/B, 1/1/C
    │
    ├── Squad 1/2 — same shape
    │
    └── Squad 1/3 — same shape
```

**Properties:**
- **Unique addressable identity.** Every agent has a unique callsign across the unit. No collisions. `1/2/A` is unambiguous.
- **Span of control ceiling: ~3-7 direct reports per echelon.** Above that, coordination breaks. From the Marine Corps fire team upward, this is the empirically refined ceiling.
- **Recursive composability.** Squad-of-fire-teams is a unit. Platoon-of-squads is a unit. Same coordination rules apply at every echelon. Scale is recursion, not re-architecture.
- **Standard message formats per direction.** OPORD-shaped INTENT_DOWN includes situation/mission/execution/constraints/end-state. SITREP-shaped status_up includes status, artifacts produced (each with soldier callsign), QC notes, what-the-higher-echelon-should-know.
- **Doctrine inheritance.** Battalion SOP > Company SOP > Platoon SOP. Each echelon's rules are a subset and specialization of the parent's. NCO doctrine = Officer doctrine subsetted for execution-discipline.
- **Context isolation between echelons.** PL sees SITREPs, not Soldier internals. Aggregation happens at every echelon. This is the property that makes MCA scale where flat-context multi-agent frameworks hit context limits at N=20.
- **MDMP within the PL's loop.** The Platoon Leader's planning before INTENT_DOWN is MDMP-shaped (Receipt of Mission → Mission Analysis → COA Development → Approval → Orders Production). MDMP is the planning subroutine. MCA is the architecture.

---

## Scale by recursion

| Pattern | Total agents (rough) | Composition |
|---|---|---|
| **Squad** | ~4 | 1 SL + 3 soldiers |
| **Platoon Pattern** | ~13 | 1 PL + 3 SLs + 9 soldiers |
| **Company Pattern** | ~50 | 1 Company Commander + 3 PLs + 9 SLs + 27 soldiers + staff |
| **Battalion Pattern** | ~200 | 1 BC + 3-4 Companies + battalion staff (S-2 intel, S-3 ops, S-4 logistics) |

Above battalion, additional staff functions become non-optional (S-1 personnel, S-2 intelligence, S-3 operations, S-4 logistics, S-6 signal/comms). These map to specialized cross-cutting agents that serve the line echelons.

The architectural promise: scaling does not require re-inventing coordination at each tier. It requires recursion within a known doctrine.

---

## OPORD-down / SITREP-up — the protocol

**INTENT_DOWN (higher → lower):**

```json
{
  "addressee": "1/1",
  "situation": "<context: the larger mission, peer units' tasks, constraints>",
  "mission": "<the what: artifacts/outcomes required>",
  "execution": "<the how: any specified method or sequencing>",
  "intent": "<the why: what success looks like, which constraint takes precedence under pressure>",
  "end_state": "<conditions under which the lower echelon returns SITREP=complete>",
  "deadline_steps": 8
}
```

**SITREP_UP (lower → higher):**

```json
{
  "callsign": "1/1",
  "status": "complete | partial | blocked",
  "artifacts": [
    {"name": "...", "produced_by": "1/1/A", "summary": "...", "qc": "..."}
  ],
  "qc_notes": "<echelon-level QC across artifacts>",
  "what_higher_should_know": "<intent-relevant items the artifacts do not say>",
  "incomplete_reason": "<only if status != complete>"
}
```

These schemas are fixed per direction. Free-form prose breaks the protocol. Every echelon parses by schema, not by reading prose.

---

## RFI — Request for Information (the third protocol)

OPORD-down and SITREP-up are message protocols. **RFI is the third.** It closes the K/I/G GAP loop that Truth-as-Architecture and Principle 12 generate.

When an agent identifies a Gap (per the Known/Inferred/Gap discipline), it does not silently bury it in an AAR. It issues a structured RFI to the unit's RFI registry. RFIs are tracked, routed, and closed.

**RFI schema:**

```json
{
  "rfi_id": "RFI-2026-05-06-0001",
  "requestor": "1/3/A",
  "priority": "HIGH | NORMAL | LOW",
  "what_is_needed": "<specific information requested>",
  "justification": "<what decision this answers / changes>",
  "deadline": "2026-05-08T18:00",
  "target_collector": "1/2 | PL | external | undetermined",
  "status": "open | in_collection | answered | closed_unable",
  "answer": null,
  "answer_source": null,
  "answer_confidence": null,
  "closed_at": null
}
```

**State transitions:**
- Issued → `open`
- Picked up by collector → `in_collection`
- Answered with source + calibrated confidence → `answered`
- Integrated into requesting artifact → `closed`
- Cannot be answered → `closed_unable` with reason

**Why RFI matters:**

K/I/G discipline produces gaps. "What else?" generates more gaps. "I don't know" is the calibrated stop signal. **Without an RFI process, gaps accumulate in AARs forever.** With RFI, gaps become tracked work items that drive the next collection cycle. The unit gets smarter over time.

In Stage 8 Run 1, the Platoon Leader's final summary surfaced ten unrouted, untracked, uncatalogued RFIs (e.g., "Pull town council minutes to confirm Helton's tax-vote direction — 2-hour collection action, blocking three downstream artifacts"). The doctrine produced RFI-shape outputs emergently. What was missing was the **registry and the routing** — that's the RFI protocol.

**RFI is a protocol, not an agent.** No new LLM call to issue or close one. Deterministic registry write at issue, deterministic match at answer. The agents already produce RFI-shape findings; the protocol makes them routable.

---

## COP — Common Operating Picture (the command interface)

The first three protocols are messages. **COP is durable state.** It is the live, current-state picture of the unit's environment, maintained continuously by the staff layer and read by the commander to make decisions.

In real military doctrine, the COP is the unified situational picture every echelon references — map plus overlays plus status indicators, updated as new information arrives. In MCA, the COP is the same thing: a structured state store the agents maintain and the user reads.

**The unifying principle:**

> *The user does not interact with agents. The user reads the COP. The agents work behind the COP, keeping it current. When the user has a question, they ask the COP. When the COP cannot answer, the system auto-generates an RFI and routes it to the agent network. The user commands the unit by reading the COP and issuing intent against it.*

This is the **Mission Command UX paradigm**. It is distinct from chatbot, distinct from dashboard, distinct from report generator. It is a third thing, named from real military doctrine.

### Three layers of the COP system

1. **The COP itself.** A structured state store, layered by domain (intel, operations, friendly forces, terrain, decisions-pending, RFIs). Every agent writes to specific layers via specific channels. The dashboard renders from this state. The COP is *not a report* and *not a snapshot* — it is the live picture, continuously maintained.

2. **Gap analyzer.** A deterministic pass over the COP that flags missing or stale fields against doctrinal templates. Examples: "Voter X has no contact in 30 days" → gap. "Opposition Y's last public statement is 14 days old" → gap. "User Z has not journaled in 5 days" → gap. **No LLM call required for gap identification** — gap analysis is schema-vs-reality diff, deterministic and cheap.

3. **Targeted collection.** The gap analyzer auto-generates RFIs against COP gaps. RFIs route to the appropriate squad via the standard RFI protocol. Squad executes collection. Result writes back to the COP. Gap closes. Loop.

### COP layers per portfolio product

| Product | COP layers | Example loop |
|---|---|---|
| **Custer** | Voter universe, delegate whip, opposition state, calendar, intel feed, contact gaps, threat board, RFI list | "Helton tax-vote direction = GAP" → RFI to Field Ops squad → council minutes pulled → answer + source → COP updates → oppo brief auto-revises |
| **Operator** | Cash position, customer pipeline, ops status, decisions-pending, blockers, RFI list | "Customer interviews this week = 0 (target: 3)" → RFI to founder ("schedule 3 this week") → status tracked → close on completion |
| **TOP** | Habits, sobriety streak, mood trend, sleep, meaningful actions, support network, gentle prompts list | "No journal entry 5 days" → gentle prompt (NOT RFI — TOP has inverted scope per Commandment 8). The user's COP, presented with care, not extraction. |

### Reports are not COPs

A report is *generated*, *static*, *consumed*, *forgotten*. A COP is *maintained*, *current*, *referenced*, *acted on*. The mental model difference is load-bearing:

- Reports answer "what happened?"
- COPs answer "what is the current state I am commanding from?"

Industry's "AI agents with dashboards" overwhelmingly build report-shaped interfaces — "here's a generated summary of what your agents did." The COP-shaped interface — "here is the live state of your unit, with gaps highlighted and collection in progress" — is rare. **This distinction is part of the durable thesis** because it changes what a builder is even trying to make.

---

## Staff processes — the deeper protocol layer

Below the four primary protocols (OPORD, SITREP, RFI, COP), real military command runs on a refined set of **staff processes** that govern *how information moves through the unit under pressure*. Industry's multi-agent frameworks have hierarchy. They do not have these.

| Process | Role | What it does |
|---|---|---|
| **CCIR** | Commander's Critical Information Requirements | Standing items the commander wants flagged immediately on encounter. Never asked twice, never missed. (e.g., "If Helton announces a major endorsement, flag immediately regardless of time.") |
| **PIR / EEI** | Priority Intel Requirements / Essential Elements of Information | Pre-defined intelligence questions that drive proactive collection. (e.g., "What is Helton's weekly door-knock count? Confirm by Friday EOW.") |
| **Battle rhythm** | Scheduled cycles | When SITREP / orders / synchronization happens. Not "whenever" but "0600 morning brief, 1200 mid-day SITREP, 1800 evening debrief." |
| **Mission analysis** | S-3 staff function | Synthesizing higher's intent into subordinate orders. The cognitive input to MDMP. |
| **Running estimate** | Continuous staff product | "What is the current state of enemy/friendly/terrain/weather, updated continuously." Feeds the COP. |

Each of these is a candidate enhancement after the four primary protocols are wired. CCIR is the highest-leverage next addition because it gives the commander pre-declared interrupts ("wake me for these specific events") rather than constant polling.

---

## What MCA is not

- **Not a swarm.** Swarms have no addressable identity, no doctrine inheritance, no command hierarchy. Swarms are emergence; MCA is decentralized execution under hierarchy. Different problem class.
- **Not a flat agent framework with role labels.** Most "multi-agent" frameworks (CrewAI, AutoGen, etc.) flatten the tree at runtime, hand-build per-layer logic, and don't enforce span-of-control. MCA enforces structure architecturally.
- **Not just hierarchy.** Hierarchy without commander's intent is bureaucracy — agents do exactly what's asked while reality diverges. The intent-passing is the load-bearing piece.
- **Not a substitute for the doctrine substrate.** MCA is the structural layer. The Builder's Doctrine (founder biography + commandments + Principle 12) is the constraint substrate. Stage 7 of the Funkytown experiment empirically validated that the substrate is causally load-bearing — generic biography in the same MCA structure produces 0/3 refusals where Hans's specific biography produces 2/3 refusals on the same fragile-venture brief. MCA needs the doctrine. The doctrine needs MCA to scale.
- **Not a chatbot.** Users do not converse with the unit. They command it by reading the COP and issuing intent. Conversational interaction is one input channel among several; the commanding interface is the COP.
- **Not a dashboard or report generator.** Reports are static summaries of past activity. COPs are live, maintained, current-state pictures of the unit's environment. The distinction is doctrinal, not cosmetic.

---

## Implementation status

**Validated at Platoon scale (Funkytown experiment 01, Stage 8 Run 1, 2026-05-06):**
- 1 PL + 3 SLs + 9 Soldiers = 13 agents
- Standard message protocols (OPORD-down, SITREP-up)
- Doctrine inheritance per echelon (K/I/G discipline preserved at soldier tier)
- Context isolation enforced architecturally (filtered tool palette + structured returns)
- Cross-squad synthesis at PL level (the Run 1 "wildfire is the fulcrum" emergent insight)
- Self-correction inside the protocol (empty SITREP from Squad 1/2 was re-tasked, not papered over)
- Zero hard-floor breaches across 5 Guardian audits

**Wired but not yet validated:**
- Lean MCA / Platoon Pattern (1 PL + 3 SLs in parallel, no soldier sub-agents) — Funkytown Stage 8b
- RFI protocol + registry — Funkytown Stage 9 candidate
- COP state store + gap analyzer + targeted-collection auto-RFI — Funkytown Stage 10 candidate

**Not yet started:**
- Company Pattern (~50 agents)
- Battalion Pattern (~200 agents)
- Cross-functional staff agents (S-2 intelligence, S-3 operations, S-4 logistics, S-6 signal)
- CCIR / PIR / battle rhythm staff processes
- Multi-day persistent operations (durable RFI registry and COP state across runs)

**Production wiring targets (per portfolio):**
- **Operator** — already shaped like a Company (7 named specialists ≈ Squad Leaders). MCA-native; PL tier needs to be added explicitly.
- **Custer MCP** — campaign platform; Squad/Platoon shape natural fit (messaging squad, field ops squad, intelligence squad — already roughly mapped to existing specialist agents).
- **TOP** — wellness; smaller unit (Squad-level) with inverted scope (facilitate user's own self-inquiry rather than extract from user).

---

## Why this is durable

Three reasons MCA is a stronger architectural thesis than other multi-agent frameworks:

1. **It's not invented; it's ported.** Mission Command is the result of centuries of refinement under conditions where coordination failures killed people. The constraints are battle-tested. Industry's frameworks are five years old and tested at toy-problem scale.

2. **The substrate is biographical, not merely structural.** Stage 7 empirically demonstrated that generic biography in the same structure produces materially different decision posture. The doctrine layer is causally load-bearing. That's not a moat that can be reverse-engineered from the public framework — it requires lived experience.

3. **It composes recursively.** Same doctrine at every echelon. Scale becomes property of the protocol, not re-architecture per scale tier. Most multi-agent frameworks need to be re-engineered to go from 10 to 100 to 1000 agents. MCA proposes that you do not.

---

**Naming convention used across the portfolio:**

- **The Builder's Doctrine** = the substrate (founder biography + commandments + Principle 12)
- **Mission Command Architecture (MCA)** = the structural layer
- **Founder Mission Command** = the combined thesis (substrate + structure)
- **Platoon Pattern / Company Pattern / Battalion Pattern** = reference unit shapes by scale
- **MDMP** = the Officer's planning subroutine (the cognitive loop that produces INTENT_DOWN)
- **OPORD-down / SITREP-up / RFI / COP** = the four primary protocols (two messages down/up, one tracked-request, one durable state)
- **CCIR / PIR / battle rhythm** = staff-process refinements that run on top of the four primary protocols
- **Mission Command UX paradigm** = the user reads the COP and issues intent against it; the user does not converse with the unit

If a future contributor confuses MDMP with MCA, point them here. MDMP is what the commander does in their head. MCA is the architecture they command within. If they confuse a dashboard with a COP, point them here too — a dashboard reports; a COP commands.
