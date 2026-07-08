# IPB — Analysis-Layer Cross-Map (ADP 2-0 / IPB)

**Status:** v0.1 — 2026-06-05.
**Origin:** Hans observation, 2026-06-05 — the doctrine names and translates **ADP 6-0** (the *philosophy* of command) and now **FM 6-0** (the *execution* / staff layer), but never names the **Intelligence** parent: **ADP 2-0** (*Intelligence*) and its flagship analytic method, **IPB** (*Intelligence Preparation of the Battlefield/Operational Environment*, ATP 2-01.3). Yet the doctrine already speaks the MI dialect fluently — K/I/G tagging, RFI, PIR/EEI/CCIR, calibrated confidence, Drake as the S-2/OPFOR shape — without ever citing the grammar those terms come from. This is the deepest biographical fit in the portfolio (Hans's 21-year MI trade) and, for exactly that reason, the one most at risk of being mis-sold as moat evidence. It is not. See the Rule.
**Purpose:** Name ADP 2-0 / IPB as the source doctrine for the portfolio's **analysis layer** — how an agent *understands a problem space before and during action* — and consolidate the scattered "wired vs. named vs. absent" inventory into one legible table. Same shape and discipline as `ADP_6_0_TRANSLATION.md`, `FM_6_0_CROSSMAP.md`, and `AMAZON_LP_CROSSMAP.md`.
**Rule:** This document **ships no new claim and builds nothing.** It is provenance + legibility only. Two specific guardrails:
1. **Law X (Execution Threshold)** — naming the source is editorial; *building* any unbuilt analytic capability below is a new deliverable and is gated behind the open packet (the **2026-06-22 statistician engagement**, the v1.5 Law VI conditional). Not authorized here.
2. **Law VI (Biographical Falsification Gate)** — porting more of Hans's own trade is the textbook way to *accidentally* substantiate the Law I biographical-moat claim that Law VI has **deprecated and under falsification test until 2026-07-25.** This document is tradecraft *documentation*, not moat *evidence*. The biographical fit explains why the grammar maps cleanly; it is not offered as proof that biography causes product behavior. Keep it on the documentation side of that line.

---

## Why this exists

The Builders' Doctrine ports four different layers of doctrine. Three were named; the analysis layer was the fluent-but-unattributed one.

- **ADP 6-0 — Mission Command** is the *philosophy*: how a unit should be commanded under uncertainty. Named, ported, translated.
- **FM 6-0 — Commander & Staff Org & Ops** is the *execution / staff* layer: how the staff actually runs it, hour to hour. Named (`FM_6_0_CROSSMAP.md`).
- **ADP 2-0 / IPB — Intelligence** is the *analysis* layer: how the unit *understands the operational environment and the threat* well enough to decide. It answers **"what do we actually know, what are we inferring, where are the gaps, and what is the adversary most likely / most dangerously going to do?"** It was **never named** — yet its discipline is the spine of the doctrine's truth-as-architecture stance.

The asymmetry with FM 6-0 is instructive. With FM 6-0, the *capability* was present and the *source* was unnamed. With IPB, the **epistemic discipline** is present — and is the doctrine's core strength — while the **structured method** (the four-step IPB drill, threat templates, collection synchronization) is mostly named-or-absent. The doctrine inherited the *rigor* of military intelligence without inheriting its *procedure*. That is the honest shape of the gap.

---

## ADP 2-0 / IPB in one paragraph

ADP 2-0 is the U.S. Army's keystone doctrine on **intelligence** — the function that reduces uncertainty about the operational environment and the threat so the commander can decide. Its flagship analytic method is **IPB (Intelligence Preparation of the Battlefield/Operational Environment)**, a four-step drill run *before and during* operations: (1) **define the operational environment** — bound the problem; (2) **describe environmental effects** — terrain, weather, and civil considerations that constrain everyone (OAKOC / ASCOPE / PMESII-PT); (3) **evaluate the threat** — build a model of the adversary's capabilities and doctrine; (4) **determine threat courses of action** — the predictive step, producing the *most likely* (MLCOA) and *most dangerous* (MDCOA) enemy options. Feeding it is **collection management** (ATP 2-01): the machinery of **PIR/EEI** (what the commander must know), **RFI** (requests for information), **NAI/TAI** (named/targeted areas to watch), **indicators & warnings**, and the **collection plan** that synchronizes who-watches-what. Running underneath all of it is the epistemic discipline: distinguish what is **known** from what is **inferred** from what is a **gap**, report **calibrated confidence**, and treat "I don't know" as a valid, valuable answer. ADP 6-0 is the *why*; FM 6-0 is *how the staff runs it*; IPB is *how the staff knows enough to run it*.

---

## The division of labor

| Layer | Army source | Question it answers | Status in the doctrine |
|---|---|---|---|
| **Philosophy** | ADP 6-0 (Mission Command) | How should a unit be commanded under uncertainty? | Named, ported, civilian-translated |
| **Execution / staff** | FM 6-0 (Commander & Staff Org & Ops) | How does the staff actually run it, hour to hour? | Named, cross-mapped (`FM_6_0_CROSSMAP.md`) |
| **Analysis** | **ADP 2-0 / IPB** (Intelligence) | What do we know, infer, and not know — and what will the adversary do? | **Discipline present, source unnamed until this doc** |
| **Scoping** | Amazon Working Backwards / LP | What should we build before we build it? | Named, cross-mapped (`AMAZON_LP_CROSSMAP.md`) |

---

## The four IPB steps, cross-mapped

| IPB step | Closest analog in the portfolio | Status |
|---|---|---|
| **1. Define the operational environment** (bound the problem) | Mission analysis inside the PL's MDMP loop; Working Backwards scoping | ⚠️ Partial — done implicitly in planning; no formal IPB Step-1 drill |
| **2. Describe environmental effects** (terrain/weather/civil; OAKOC/ASCOPE/PMESII-PT) | Per-User Context / UserContext as a thin "civil considerations" analog | ❌ Mostly absent — no environmental-constraints model as an analytic step |
| **3. Evaluate the threat** (adversary capability model) | **Drake (S-2 / OPFOR / red team)**; adversary-fuzz (Exp 11); founder-romance + strategic-layer detectors as self-threat models | ✅ Partial — threat evaluation runs as a named specialist; no formal threat template/doctrinal overlay |
| **4. Determine threat COAs** (MLCOA / MDCOA — the predictive step) | Drake's adversary-COA outputs; `SHAPING_OPERATIONS` branches/sequels | ⚠️ Partial — predictive framing present in red-team; not formalized as MLCOA/MDCOA |

---

## Full cross-map

Status legend: **✅ Wired** (built and in the architecture) · **⚠️ Named, unbuilt** (already inventoried as a candidate; not built) · **❌ Absent** (not in the doctrine at all).

| ADP 2-0 / IPB element | What we have here | Status | Disposition (Law VII) |
|---|---|---|---|
| **K/I/G discipline** (Known / Inferred / Gap) | Truth-as-Architecture; the GAP feeds the RFI loop; Principle 12 ("what else?") generates gaps | ✅ Wired & validated | Core of the doctrine; in use across products |
| **Calibrated confidence** | Agent Doctrine #7 (Confidence Scoring); "I don't know" as calibrated stop; risk acceptance | ✅ Wired & validated | In use; LOW confidence treated as signal, not failure |
| **RFI** (Request for Information) | MCA third protocol; structured registry/routing schema; closes the K/I/G GAP loop | ✅ Wired (doctrine); registry ⚠️ Stage 9 candidate | Protocol in use; registry/routing deferred (Stage 9) |
| **PIR / EEI** (priority intel / essential elements) | MCA "Staff processes"; staff drives proactive collection — *plumbing owned by* `FM_6_0_CROSSMAP.md` | ⚠️ Named, unbuilt | Deferred — Law X gated; here it is the *requirement that drives analysis*, not the schedule |
| **CCIR** (commander's critical info requirements) | Staff agents as standing watchers; MCA names it highest-leverage next add | ⚠️ Named, unbuilt | Deferred — Law X gated; see FM 6-0 cross-map for the staff-process reading |
| **Threat evaluation** (IPB Step 3) | **Drake (S-2 / OPFOR)**; adversary fuzz (Exp 11); self-threat detectors (founder-romance, strategic-layer) | ✅ Partial | Runs as named specialist; formal threat template absent |
| **Threat COA prediction** (MLCOA / MDCOA, IPB Step 4) | Drake adversary-COA outputs; SHAPING branches/sequels | ⚠️ Partial | Predictive framing present; MLCOA/MDCOA not schema'd |
| **Indicators & Warnings (I&W)** | Agent Doctrine #5 (Proactive Intelligence) — monitor jobs, at-risk detection, scheduled watchers | ✅ Partial | Event-driven watchers exist; indicator lists not tied to declared PIR |
| **Running intelligence estimate** | Agent Doctrine #8 (Running Estimates) — live domain snapshot read on every turn | ✅ Wired (Agent Doctrine); ⚠️ at MCA scope | In use per-product; MCA-scope estimate deferred (see FM 6-0 cross-map) |
| **Intelligence database / OE knowledge** | Agent Doctrine #6 (Knowledge Graph) — queryable entity/relationship store | ✅ Wired | The "what we know about the environment" substrate |
| **Collection plan / ISR synchronization** | RFI is the request primitive; no synchronized collection matrix | ⚠️ Partial | Targeted-collection auto-RFI is a Stage 10 candidate; matrix absent |
| **NAI / TAI** (named / targeted areas of interest) | — | ❌ Absent | Genuine gap; no spatial/topical "watch this" primitive beyond ad-hoc monitors |
| **Define OE** (IPB Step 1) | Implicit in MDMP mission analysis + Working Backwards | ⚠️ Partial | No formal problem-bounding drill |
| **Describe environmental effects** (IPB Step 2; OAKOC/ASCOPE/PMESII-PT) | Per-User Context as thin "civil considerations" analog | ❌ Mostly absent | Genuine gap; no environment-constraints model as an analytic step |
| **Source reliability / info credibility** (the A-1…F-6 grading) | Confidence scoring carries credibility informally; no source-grading taxonomy | ⚠️ Partial | Confidence ≈ credibility; formal source-reliability scale absent |

---

## What this surfaces

Three honest reads fall out of the table:

1. **The doctrine already ported IPB's *discipline* — and it is the spine, not a wing.** K/I/G tagging, calibrated confidence, "I don't know" as a valid answer, named gaps that become tracked RFIs — this is military-intelligence epistemic rigor, and it is exactly what `THE_BUILDERS_DOCTRINE.md` calls Truth-as-Architecture. The most important thing intelligence tradecraft teaches (be honest about what you don't know) was inherited first and is validated across products. Hans's instinct that a piece was unnamed is correct; the rigor itself was never missing.

2. **What was *not* ported is the *method* — the four-step drill and the collection machinery.** IPB Steps 1–2 (bound the problem, model the environment's constraints) are mostly implicit or absent. Step 3–4 (evaluate the threat, predict its COAs) run as Drake but without the formal threat-template / MLCOA-MDCOA structure. NAI/TAI and a synchronized collection plan are absent. This is the symmetric opposite of the FM 6-0 finding: there the capability was present and the source unnamed; here the *source's procedure* is the gap, while its *ethos* is already load-bearing.

3. **Drake is IPB Step 3 wearing a callsign — and the self-threat detectors are IPB turned inward.** The founder-romance detector and strategic-layer detector are, structurally, *threat evaluation aimed at the builder's own reasoning* — adversary analysis where the adversary is observer bias. That is a genuinely original move and worth naming as such, but it is documentation of an existing pattern, not a new claim.

---

## Discipline note — what this document is not

This is not authorization to build the analysis layer. Per `META_DOCTRINE.md` Law X, no new deliverable is added from a review observation until the prior packet's top actions have shipped with measurement surface. The open packet is the **2026-06-22 statistician engagement** (the v1.5 Law VI conditional). Until that ships, every ⚠️/❌ row above stays on the shelf with the dispositions listed.

It is also **not moat evidence, and the timing makes that guardrail load-bearing.** Law VI has the Law I biographical-moat claim *deprecated and under falsification test until 2026-07-25.* Porting the doctrine of Hans's own 21-year trade is precisely the kind of artifact that, written carelessly, reads as "see — the biography *is* the product." It is not offered that way. The biographical fit is the *reason the grammar maps cleanly enough to document*; it is not *proof that biography causes product behavior*. Any future build off this cross-map inherits the same constraint until Law VI returns its verdict.

When the statistician packet ships and Law X opens, the natural first pickups are the two items that are both genuinely absent and high-leverage: a **threat-template formalism** (give Drake the IPB Step-3 structure it already half-runs) and **NAI/TAI** (a declared "watch this" primitive to anchor the proactive-intelligence monitors to named PIR). Both are build decisions for that day, run through the elon-algorithm and an adversarial reshape — not commitments made here.

---

## How to use this document

- **Internal artifacts** — cite ADP 2-0 / IPB as the analysis-layer source the same way you cite ADP 6-0 (philosophy) and FM 6-0 (execution). When you add an analytic capability, update the status column here in the same patch (doctrine-vs-code drift is the highest-risk artifact in this repo — close the surface in the same commit).
- **External artifacts** — IPB vocabulary buys the same channel legitimacy ADP 6-0, FM 6-0, and Amazon LP buy: "the analysis layer is sourced from the Army's published intelligence doctrine, not improvised." **But** never let an IPB reference drift into a moat claim while Law VI is open — frame it as method provenance, not biographical proof.
- **As a roadmap** — the ⚠️/❌ rows are the prioritized, Law-gated backlog for the analysis layer. Read the disposition column before proposing any of them.

---

## Cross-references

- `MISSION_COMMAND_ARCHITECTURE.md` — §"RFI — Request for Information", §"The Staff Channel" (Drake/S-2), §"Staff processes" (CCIR/PIR/EEI)
- `FM_6_0_CROSSMAP.md` — the execution-layer cross-map; owns CCIR/PIR/EEI/running-estimate as *staff plumbing* (this doc owns them as *analytic requirements* — read both)
- `ADP_6_0_TRANSLATION.md` — civilian gloss for the Army terms used above (philosophy + execution layers; IPB terms to be added next)
- `kit/templates/AGENT_DOCTRINE.md` — Proactive Intelligence (#5, the I&W analog), Knowledge Graph (#6), Confidence Scoring (#7), Running Estimates (#8)
- `kit/chassis/STRATEGIC_LAYER_DETECTOR_SPEC.md`, `kit/chassis/FOUNDER_ROMANCE_DETECTOR_SPEC.md` — IPB threat evaluation turned inward on builder bias
- `SHAPING_OPERATIONS.md` — branches/sequels (the threat-COA-adjacent work)
- `META_DOCTRINE.md` — Law V (Echelon Decay Gate), Law VI (Biographical Falsification Gate), Law VII (Provisional Doctrine Rule), Law X (Execution Threshold) — the gates governing every ⚠️/❌ row

---

## Source

- ADP 2-0, *Intelligence*, Headquarters, Department of the Army (July 2019). Keystone Army doctrine for the intelligence warfighting function.
- ATP 2-01.3, *Intelligence Preparation of the Battlefield/Operational Environment* — the four-step IPB method (define OE → describe effects → evaluate threat → determine threat COAs).
- ATP 2-01, *Plan Requirements and Assess Collection* — PIR/EEI, RFI, NAI/TAI, indicators & warnings, the collection plan.
- ADP 6-0 is the philosophy; FM 6-0 is how the staff executes it; ADP 2-0 / IPB is how the staff knows enough to execute.
