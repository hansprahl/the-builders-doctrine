# FM 6-0 — Execution-Layer Cross-Map

**Status:** v0.1 — 2026-06-05.
**Origin:** Hans observation, 2026-06-05 — the doctrine names and translates **ADP 6-0** (the *philosophy* of mission command) but never names **FM 6-0** (*Commander and Staff Organization and Operations* — the *execution* manual), even though most of FM 6-0's content is already ported piecemeal across `MISSION_COMMAND_ARCHITECTURE.md`, `SHAPING_OPERATIONS.md`, and `kit/templates/AGENT_DOCTRINE.md`.
**Purpose:** Name FM 6-0 as the source doctrine for MCA's execution / staff-process layer, and consolidate the scattered "wired vs. named vs. absent" inventory into one legible table. Same shape as `ADP_6_0_TRANSLATION.md` and `AMAZON_LP_CROSSMAP.md`: take the structural pattern the audience trusts, keep the moat in what feeds it.
**Rule:** This document **ships no new claim and builds nothing.** It is provenance + legibility only. Every FM 6-0 capability not already wired is gated behind Law V (Echelon Decay Gate — validation) and Law X (Execution Threshold — no new deliverable until the prior packet ships with measurement surface). The current open packet is the 2026-06-15 statistician engagement. Naming the source is editorial; building the gaps is not, and is not authorized here.

---

## Why this exists

The Builders' Doctrine ports two different layers of U.S. Army field doctrine, and until now only one of them was named.

- **ADP 6-0 — Mission Command** is the *philosophy*: push decision authority to the lowest competent echelon, bind it with commander's intent, allow disciplined initiative. It answers **"how should a unit be commanded?"** It is named, ported (`MISSION_COMMAND_ARCHITECTURE.md` §"The seven principles, ported"), and translated for civilians (`ADP_6_0_TRANSLATION.md`).

- **FM 6-0 — Commander and Staff Organization and Operations** is the *execution manual*: how the staff is organized, how the command post runs, how MDMP produces an order, how running estimates and the COP stay current, what an OPORD/FRAGORD/WARNORD actually contains, what CCIR and battle rhythm are. It answers **"how does the unit actually run, hour to hour, under load?"** It was **never named** in the doctrine — yet its content is the unacknowledged parent of MCA's entire protocol layer (OPORD-down/SITREP-up, RFI, COP, the Staff Channel, the "Staff processes" table).

You can ship mission-command philosophy without FM 6-0 and get a beautiful intent-passing story that has no idea how the staff keeps the picture current. You can ship FM 6-0 mechanics without ADP 6-0 and get a bureaucracy that executes orders perfectly while reality diverges. The doctrine already carries both — it just only cited one. This document closes the citation gap and inventories the rest.

---

## FM 6-0 in one paragraph

FM 6-0 is the U.S. Army's published doctrine on **how a commander and staff are organized and how they operate** — the execution layer beneath the mission-command philosophy. It specifies: how the command post is organized and run (including battle rhythm and CCIR); how the staff is sectioned (S-1 personnel, S-2 intelligence, S-3 operations, S-4 logistics, S-6 signal); the Military Decision-Making Process (MDMP) and Troop Leading Procedures (TLP) that turn a higher's intent into a subordinate's order; the Rapid Decision-Making and Synchronization Process (RDSP) for re-planning mid-execution; running estimates and the common operating picture that keep the staff current; the formats for plans and orders (OPORD / FRAGORD / WARNORD); and the supporting drills — rehearsals, liaison, risk management, military briefings. ADP 6-0 is the *why*; FM 6-0 is the *how the staff actually runs the why*.

---

## The division of labor

| Layer | Army source | Question it answers | Status in the doctrine |
|---|---|---|---|
| **Philosophy** | ADP 6-0 (Mission Command) | How should a unit be commanded under uncertainty? | Named, ported, civilian-translated |
| **Execution / staff** | **FM 6-0** (Commander & Staff Org & Ops) | How does the staff actually run it, hour to hour? | **Content present, source unnamed until this doc** |
| **Scoping** | Amazon Working Backwards / LP | What should we build before we build it? | Named, cross-mapped (`AMAZON_LP_CROSSMAP.md`) |

---

## Full cross-map

Status legend: **✅ Wired** (built and in the architecture) · **⚠️ Named, unbuilt** (MCA already inventories it as a candidate; not built) · **❌ Absent** (not in the doctrine at all).

| FM 6-0 element | What we have here | Status | Disposition (Law VII) |
|---|---|---|---|
| **Staff organization (S-1…S-9)** | MCA Staff Channel; named specialists (Drake/S-2, Marshall/Legal, Halsey/S-6); `ADP_6_0_TRANSLATION` staff-numbering gloss | ✅ Wired (as advisory roles) | Structure named and in use |
| **Cross-functional staff *agents* (S-2/3/4/6 as standing agents)** | MCA "Not yet started" | ⚠️ Named, unbuilt | Deferred — Law V + Law X gated; no date until prior packet ships |
| **Command post organization & operations** | COP system (MCA §COP); three-layer COP per product | ✅ Wired (doctrine); live cross-run COP state ⚠️ Funkytown Stage 10 candidate | COP doctrine in use; persistent state store deferred (Stage 10) |
| **MDMP** (7 steps: receipt → mission analysis → COA dev → COA analysis/wargame → COA comparison → COA approval → orders) | Operator runs it; SHAPING flow; AGENT_DOCTRINE; ADP translation | ✅ Wired | In use at Platoon scope (audit 2026-07-07: step list corrected from a 5-step compression) |
| **Troop Leading Procedures (TLP)** | SL-tier task assignment within squad; referenced, not formalized as the 8-step drill | ⚠️ Partial | Squad-tier planning works; formal TLP drill not schema'd |
| **Rapid Decision-Making & Synchronization (RDSP)** | — re-plan-on-the-fly mid-execution loop | ❌ Absent | Genuine gap; deferred — Law X gated |
| **Running estimates** | MCA "Staff processes" table; AGENT_DOCTRINE; ADP translation | ⚠️ Named, unbuilt | Deferred — feeds COP; Law V + Law X gated |
| **Common operating picture (COP)** | MCA §COP — live current-state picture vs. static report | ✅ Wired (doctrine, Platoon) | In use; persistence across runs deferred (Stage 10) |
| **Orders formats — OPORD** | MCA OPORD-down, fixed schema | ✅ Wired & validated (Platoon, Funkytown 01) | In use |
| **Orders formats — FRAGORD / WARNORD** | Mentioned in `SHAPING_OPERATIONS` (branches/sequels) | ⚠️ Partial | Not schema'd; sits with the SHAPING branch/sequel work |
| **CCIR** (Commander's Critical Information Requirements) | MCA "Staff processes" table — flagged as highest-leverage next addition | ⚠️ Named, unbuilt | Deferred — Law X gated; MCA names it the first staff-process to add |
| **PIR / EEI** (priority intel / essential elements) | MCA "Staff processes" table | ⚠️ Named, unbuilt | Deferred — Law X gated |
| **Battle rhythm** (scheduled brief/sync/debrief cadence) | MCA "Staff processes" table; `SCHEDULER_SPEC_DRAFT.md` is the primitive | ⚠️ Named, unbuilt | Deferred — scheduler spec exists; wiring Law X gated |
| **After Action Review (AAR)** | Chassis component (`kit/chassis/`, AAR Loop); Agent Doctrine | ✅ Wired & validated | In use across products |
| **Liaison** (cross-unit coordination) | RFI protocol — tracked, routable cross-unit info request | ✅ Wired (doctrine); ⚠️ RFI registry not yet validated (Stage 9 candidate) | RFI is the analog; registry deferred (Stage 9) |
| **Military briefings** | SITREP-up (fixed schema); COP read | ✅ Partial | SITREP serves; no formal briefing-format taxonomy |
| **Risk management** (RM worksheet / hazard control) | Authority Gradient + Approval Queue gate irreversible actions (partial analog); Principle #4 hard floor | ✅ Partial | World-boundary risk gated; formal RM worksheet absent |
| **Information collection** | RFI + COP gap analyzer | ⚠️ Partial | Targeted-collection auto-RFI is Stage 10 candidate |
| **Rehearsals** (confirm the plan before execution) | — | ❌ Absent | Genuine gap; no pre-execution rehearsal step |
| **Knowledge / information management** | COP system + memory substrate | ✅ Partial | COP + durable history cover the core; not formalized as KM doctrine |

---

## What this surfaces

Three honest reads fall out of the table:

1. **The execution layer is real and mostly already FM-6-0-shaped.** OPORD, SITREP, COP, MDMP, AAR, the Staff Channel — all present, several validated at Platoon. Hans's instinct was right that a piece was unnamed; it was *not* right that the capability was missing. The map already lived inside MCA's "Staff processes" and "Not yet started" tables — it just wasn't attributed to FM 6-0 or consolidated.

2. **The named-but-unbuilt block is MCA's own backlog, correctly parked.** CCIR, PIR, running estimate, battle rhythm, cross-functional staff agents — MCA already inventories every one of these and already gates them behind Law V (validation) and Law X (execution threshold). This cross-map changes nothing about that gating. It only makes the backlog legible in one place and forces each item to carry a Law VII disposition instead of drifting as a loose "not yet started" note.

3. **Two items are genuinely absent, not merely deferred: RDSP and rehearsals.** Both are FM 6-0 execution drills with no analog anywhere in the doctrine. RDSP (re-plan mid-execution when the situation shifts) is partially addressed by `SHAPING_OPERATIONS` branches/sequels but not as a runtime loop. Rehearsals (confirm the plan before committing) have no representation at all. These are the only candidates that would be *new doctrine* rather than *consolidated backlog* — and per Law X they do not get drafted until the prior packet ships.

---

## Discipline note — what this document is not

This is not authorization to build the staff-process layer. Per `META_DOCTRINE.md` Law X, no new deliverable is added from a review observation until the prior packet's top actions have shipped with measurement surface. The open packet is the **2026-06-15 statistician engagement** (the v1.5 Law VI conditional). Until that ships, the FM 6-0 capability gaps stay on the shelf with the dispositions above.

This document also does **not** alter MCA's validation posture. MCA is validated at **Squad + Platoon only** (Law V). Every FM 6-0 element marked ✅ above is wired at Platoon scope; none of it constitutes a Company-or-above validation claim. The cross-functional staff agents an FM 6-0 reader would expect (a real S-2, S-3, S-4, S-6 standing up at Company) are exactly the rung that is *not yet validated*.

When the statistician packet ships and Law X opens, the natural first pickup is the item MCA already names highest-leverage: **CCIR** — pre-declared interrupts so the commander is paged on named events instead of polling. That is a build decision for that day, run through the elon-algorithm and an adversarial reshape, not a commitment made here.

---

## How to use this document

- **Internal artifacts** (architecture docs, experiment write-ups, chassis source) — cite FM 6-0 as the execution-layer source the same way you cite ADP 6-0 for the philosophy layer. When you add a staff process to MCA, update the status column here in the same patch (doctrine-vs-code drift is the highest-risk artifact in this repo — close the surface in the same commit).
- **External artifacts** (pitches, EXPLAINER, README) — FM 6-0 vocabulary buys the same channel legitimacy ADP 6-0 and Amazon LP buy: "the execution layer is sourced from the Army's published staff-operations manual, not improvised." Inline the civilian gloss from `ADP_6_0_TRANSLATION.md` the first time each term appears.
- **As a roadmap** — the ⚠️ rows are the prioritized, Law-gated backlog for the staff-process layer. Read the disposition column before proposing any of them.

---

## Cross-references

- `MISSION_COMMAND_ARCHITECTURE.md` — §"The Staff Channel", §"OPORD-down / SITREP-up", §"Staff processes — the deeper protocol layer", §"Implementation status"
- `ADP_6_0_TRANSLATION.md` — civilian gloss for every Army term used above (philosophy layer)
- `SHAPING_OPERATIONS.md` — Phase 0 / branches / sequels (the RDSP-adjacent work)
- `SCHEDULER_SPEC_DRAFT.md` — the battle-rhythm primitive
- `kit/templates/AGENT_DOCTRINE.md` — running estimate, AAR, MCA unit structure in the Agent Doctrine surface
- `META_DOCTRINE.md` — Law V (Echelon Decay Gate), Law VII (Provisional Doctrine Rule), Law X (Execution Threshold) — the gates governing every ⚠️ row

---

## Source

- FM 6-0, *Commander and Staff Organization and Operations*, Headquarters, Department of the Army (**May 2022**, which supersedes the 5 May 2014 edition). Companion to ADP 6-0 (*Command and Control*, 07 July 2026, superseding *Mission Command…* 2019). ADP 6-0 is the philosophy; FM 6-0 is how the staff executes it. (Editions corrected 2026-07-07 ground-truth audit; the coordinating-staff roster used to cross-map the specialists is FM 6-0 2022 ¶2-46.)
