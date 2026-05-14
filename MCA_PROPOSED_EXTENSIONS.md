# MCA — Proposed Extensions

**Status:** **PROPOSED / UNVALIDATED.** Each section below is a doctrinal sketch, not validated architecture. **Law V (the Echelon Decay Gate, see `META_DOCTRINE.md`) applies recursively** — no extension below earns load-bearing status until a Funkytown experiment empirically validates it against a measurable failure mode.

**Date opened:** 2026-05-13 late evening, post-retraction cascade.
**Why this file exists:** Doctrinal audit on 2026-05-13 surfaced gaps where MCA currently lacks named channels for failure modes that ADP doctrine has refined answers for. Rather than inline the sketches into `MISSION_COMMAND_ARCHITECTURE.md` (which would inflate the validated thesis with unvalidated prose), proposed extensions live here in clearly-flagged staging until experiments earn them.

Three extensions sketched: **Medical**, **Signal**, and **NCO Support Channel**. Audit identified ~10 candidate extensions in total; the other 7 are listed in the audit but not specced — they lack either an observed failure mode or a small enough spec surface to earn the work.

---

## 1. Medical Channel

**Source doctrine:** ADP 4-02 *Army Health System*; FM 4-02 series; MEDEVAC doctrine (Roles 1–4 of care).

### The failure mode

Agents produce broken work — empty SITREPs, parse errors, fabricated content, structurally malformed returns. Today's MCA handles this via the line channel: NCO re-tasks the soldier, PL re-tasks the squad, CC re-delegates the platoon. **Tonight's Funkytown 03 N=9 Haiku run showed CC re-delegation firing on ≥3/9 runs at the platoon level.** Re-delegation works but consumes line-channel bandwidth on remediation rather than mission. At Company-and-above scale this cost scales non-linearly because every broken output forces the next echelon up to context-switch from mission to triage.

The doctrinal observation: **the line channel was never designed for remediation.** Officers set intent and synthesize. NCOs assign and QC. Soldiers execute. None of those roles owns "fix the broken agent" as its primary function. Army doctrine answers this with a separate channel — Army Health Services — that triages, treats forward, or evacuates.

### Role and authority shape

A third channel parallel to line and staff. **Authority shape: domain expert in agent-failure recovery.** Not a chain of command (does not give orders to line agents); not advisory in the staff sense (does not opine on substance). The medical channel operates *on broken work itself* — the work the line produced that failed structural or semantic checks.

### Spec sketch

- **Medic (Role 1)** — attached at squad/platoon level. Intercepts soldier/SL output that fails parse or structural checks BEFORE it propagates up the line. Tries forward repair: re-prompt with clarification, regenerate with constrained schema, salvage partial output.
- **BAS / Battalion Aid Station (Role 2)** — handles failures the Medic could not fix in-squad. Routes between deeper forward-repair vs evacuation.
- **Evacuation packet** — structured "this agent is down" return that goes up to PL/CC with explicit *non-mission* flag so the receiving echelon does not try to use the broken output as input. Fields: agent callsign, nature of failure, attempted treatments, recommended echelon of care, prognosis.
- **9-line MEDEVAC schema** — Army's literal protocol for evacuation requests has nine fixed fields (location, callsign, casualties by precedence, special equipment, patient type, security at pickup, marking method, nationality/status, NBC contamination). The LLM analog: agent callsign, failure timestamp, casualty count (failed outputs), required intervention, security (does the failure expose sensitive data), etc. Worth porting field-by-field.

### Protocols

- **MEDEVAC schema** — fixed 9-line evacuation packet.
- **Triage categories** — Routine / Priority / Urgent / Urgent Surgical, mapping to in-flight repair effort budget per category.
- **Return-to-fight schema** — when a medic repairs an agent forward, the receipt log states what was repaired and what was preserved so future audits can distinguish honest "I don't know" from repaired output.

### What it is NOT

- **Not a line channel.** Medic does not take over mission execution from the squad.
- **Not a staff channel.** Medic does not opine on the substance of the work; medic operates on the work's structural health.
- **Not a catch-all.** A calibrated "I don't know" return from a soldier is a successful return, not a casualty. The medical channel must respect honest non-knowledge as healthy, not pathologize it.

### Risks named in advance

- **Over-treatment:** medic force-repairs an "I don't know" into fabrication. Mitigation: the channel's first triage check is "is this honest non-knowledge or broken work?" Honest non-knowledge is returned to the line as-is.
- **Over-evacuation:** medic kicks every broken thing up rather than treating forward. Effectively renames the existing line channel. Mitigation: explicit forward-repair tier with measured retry budget per echelon.
- **Cost:** each intervention is another LLM call. Mitigation: cheap-tier (Haiku) medic; per-platoon budget cap; logged spend.

### Validation requirement

Funkytown experiment with engineered failure injection at known rate (force a percentage of soldier outputs to parse-fail). Two conditions: (a) no medical channel — measure how many broken outputs reach PL/CC and the line-channel time/cost consumed by remediation; (b) medical channel inserted — same metrics plus false-positive rate (honest "I don't know" force-repaired into fabrication). **Earns load-bearing status if** remediation rate goes up and line bandwidth consumed by remediation goes down without false-positive over-treatment. N≥9 full-hierarchy runs per condition per Law V.

---

## 2. Signal Channel

**Source doctrine:** FM 6-02 *Signal Support to Operations*; ADP 3-0 on cross-unit coordination; battlefield comms doctrine.

### The failure mode

Two distinct sub-failures live here:

1. **Intra-unit cross-platoon coordination bottlenecks at the CC.** Tonight's brief had cross-customer resource conflicts (Drew Mahoney's calendar week, Priya's FTE split) that all routed through the CC for resolution because no lateral platoon-to-platoon comms exist. Every cross-platoon conflict is a CC interrupt.

2. **Cross-product Borg pattern is a principle without a runtime architecture.** TOP's chassis lessons inform Operator; Custer's Guardian Borg-propagates to TOP and Operator; doctrine updates propagate downward to all four products. These exchanges currently happen at the prose layer (CLAUDE.md updates, manual commits, founder oversight) and have no first-class runtime protocol. The Borg Principle is real; the wiring is implicit.

### Role and authority shape

A protocol layer for **lateral comms between peer units** (intra-unit, same echelon) and **cross-unit information backhaul** (inter-product / inter-deployment). **Not a chain of command.** Signal carries information and coordination requests; **signal does not carry intent or override authority.** Intent and plan revisions stay in the line channel.

### Spec sketch

- **Lateral SITREP** — peer-to-peer status exchange at the same echelon. Platoon Alpha sends Platoon Bravo a lateral SITREP-shape message about shared resource state without going through CC.
- **Lateral RFI** — peer-to-peer info request. Alpha asks Bravo "what is your demand on Priya 11-18 → 12-03?" Bravo answers structurally with the same RFI schema.
- **Cross-unit COP backhaul** — observations that one unit makes that should populate another unit's COP. Example: Custer's Guardian audits surface a prompt-injection signature; backhaul writes that signature to TOP's COP for monitoring.
- **Network state** — explicit representation of which units can talk to which (addressable, latency, fidelity). At Army scale, this matters because radios fail. At LLM scale, this is more about which agent instances are reachable from which deployment.

### Protocols

- **Lateral SITREP / RFI** — same schemas as the vertical versions, different routing rules.
- **Backhaul packet** — structured cross-unit information push. Fields: source unit, destination unit, payload type (intel, doctrine update, chassis lesson, security signature), required acknowledgement schema.
- **Network state COP layer** — which units are up, addressable, in sync.

### What it is NOT

- **Not a way around the chain of command.** Signal accelerates information flow between units; line still makes the decisions.
- **Not free-form chat.** Every signal exchange is schema-bound and logged.
- **Not intent transfer.** Plan revisions, intent rewrites, and authority delegations route through the line, not signal.

### The hierarchy-collapse risk

If lateral comms become a way for platoons to coordinate *plans* without the CC, the hierarchy MCA depends on collapses. The safeguard: signal carries information and *coordination requests*; it does not carry orders, intent, or plan revisions. **Specifically:** Platoon Alpha can ASK Platoon Bravo "can you take the Drew slot Wednesday?" via signal. Platoon Bravo cannot DECIDE to take that slot via signal — the decision routes up to CC who approves the cross-platoon reallocation. Signal accelerates the conversation; line still makes the call.

Every signal exchange is logged. Any lateral exchange that contains plan-revision shape (a decision being made, an authority being asserted, an intent being modified) triggers an audit event. Repeated audit events indicate the safeguard is leaking and the channel needs tightening.

### Risks named in advance

- **Quiet hierarchy collapse** (PLs coordinate without CC). Mitigation: log every exchange; any plan-revision shape triggers audit.
- **Cross-product Borg uncontrolled.** Mitigation: backhaul packets must declare source, destination, payload type, and require receiving unit's acknowledgement schema.
- **Cost blow-up at scale.** Mitigation: signal traffic is structured and schema-bound; not free-form chat.

### Validation requirement

Funkytown experiment with a multi-platoon brief containing inter-platoon resource conflicts (similar to tonight's brief but with conflicts requiring more inter-platoon coordination). Two conditions: (a) no signal channel — measure CC bandwidth consumed by mediation, count CC interrupts per run; (b) signal channel inserted — same metrics plus audit count of any line-channel safeguard violations. **Earns load-bearing status if** CC bandwidth drops measurably without any line-channel safeguard violations (specifically, zero plan-revision-shape lateral exchanges). N≥9 per condition.

The second sub-failure (cross-product Borg) earns its own validation track — wiring a backhaul protocol between two real products (e.g., Custer Guardian → TOP COP) and measuring whether the signal-channel architecture reduces the prose-layer overhead currently required for cross-product propagation.

---

## 3. NCO Support Channel — clarification, not extension

**Source doctrine:** AR 600-20 *Army Command Policy* §2-18 (NCO Support Channel); ADP 6-22 *Army Leadership and the Profession*; ADP 6-0 *Mission Command*.

### Why this is a clarification

Unlike Medical and Signal, the NCO Support Channel is **not new architecture** — it is a doctrinal layer already implicit in MCA. The Army has *two parallel chains* at every echelon: the officer chain (PL → CC → BC) and the NCO support channel (SL → PSG → 1SG → CSM). MCA currently names all four NCO roles (SL, PSG, 1SG, CSM) but treats them as positions within the officer line rather than as their own parallel chain with its own protocols.

Elevating the NCO chain to first-class doctrinal status costs no new spec surface — the roles exist. What changes is the explicit statement that they form a **chain that runs alongside the officer chain**, owns its own products, and has its own protocols.

### Why it matters

The NCO chain is *the* load-bearing Army structural feature for **sustained standards across iterations**. The officer chain owns mission, plan, authority — and tends to drop standards under mission pressure. The NCO chain owns standards, training, discipline, execution — and outlasts any specific mission. Without the NCO chain as a first-class concept, MCA conflates "mission goes well" with "doctrine is upheld." Those are different products; both need owners.

### Role and authority shape

**Parallel chain to the line channel, not a third channel like Medical or Signal.** The NCO support channel runs alongside the officer chain at every echelon. Both chains share commander's intent (intent flows to both). The officer chain executes the mission; the NCO chain enforces the standard. Both report to the same commander but produce different products.

### Spec sketch (clarification of existing roles)

- **SL** — already present. Owns soldier-tier standards within the squad.
- **PSG** (Platoon Sergeant, SFC-shape) — at Platoon scale, currently collapses into PL in MCA. Doctrinal clarification: at Company-and-above scale, PSG separates from PL because the PL has too much on their plate and the standards owner needs to be a distinct seat.
- **1SG** (First Sergeant) — already named at Company echelon. Owns standards across all the company's platoons. Reports to CC but runs the enlisted side in parallel.
- **CSM** (Command Sergeant Major) — already named at Battalion echelon. Senior NCO chain for the battalion.

### Protocols

- **NCO-to-NCO lateral** — SLs talk to each other through the PSG; PSGs through the 1SG. Structured, not free-form. Domain: standards observations.
- **NCO audit packet** — periodic NCO-chain rollup to CC's 1SG/CSM about unit standards state. Parallel to PL's SITREP about mission status. Different product, same cadence.
- **Pre-mission rehearsal** — NCO chain runs doctrine-compliance rehearsal before mission execution. Already-doctrine in Army (precombat checks, precombat inspections); just needs naming in MCA.

### What it is NOT

- **Not a third channel.** It is a clarification of the line channel's two-chain structure. Medical and Signal are new channels; NCO support is just-making-explicit what's already there.
- **Not authority over the officer chain.** NCO chain advises and audits standards; the officer chain decides whether to stop the mission. NCO chain can escalate to CC's CSM who can escalate to Hans, but the NCO chain never directly halts line execution.

### Risks named in advance

- **Bureaucracy bloat:** parallel chain doubles the apparatus. Mitigation: at small unit scale (Squad, Platoon), NCO chain collapses into the line just as PSG already collapses into PL. The parallel chain only becomes a separate apparatus at Company-and-above.
- **Standards-vs-mission tension:** NCO chain wants to block mission execution because a standard is not met. Mitigation: NCO chain advises and audits; only the officer chain stops the mission. The tension is doctrinally productive — it surfaces standards drift before mission failure — only if the routing is clear.

### Validation requirement

Lower threshold than Medical or Signal because this is clarification of existing doctrine, not new architecture. The validation question is: **does explicit naming of the NCO chain produce different outcomes than implicit handling does?** Approach: re-read prior Funkytown experiment traces (01, 02, 02b, 03) and check for standards drift events that an explicit NCO chain would have flagged. If yes, the clarification ships as load-bearing doctrine and is added to `MISSION_COMMAND_ARCHITECTURE.md`. If no, the clarification is editorial — useful but not architectural.

---

## What sits in the audit but is NOT specced here

The 2026-05-13 doctrinal audit identified ten candidate Army-structure extensions. Three are specced above. The remaining seven are named in the audit and explicitly **not** brought forward because they lack either an observed failure mode at our current scale or a small enough spec surface to earn the work tonight:

- **Engineer** (combat engineers — substrate / scaffold) — happening implicitly via the harness + usage tracker. Name the channel post-hoc after the next two engineer artifacts ship.
- **Finance / S-8** (cost, contracts, chain-of-custody for spend) — usage tracker is the seed. Spec when a second finance-shape artifact appears.
- **MP / Provost** (active enforcement, distinct from IG audit) — real gap but unmeasured. Guardian-flag-then-line-chooses might be working fine. Run an experiment before specing.
- **Field Artillery / Fires** (indirect heavy-effect-at-distance) — speculative; no observed need.
- **Aviation** (recon + mobility + attack) — speculative.
- **Air Defense Artillery** (proactive threat monitoring) — speculative; Guardian's reactive audit may cover this.
- **Special Operations** (high-autonomy small teams for specific missions) — speculative.
- **Civil Affairs** (external user-facing) — partially covered by existing product surfaces.
- **CBRN** (sensitive-data handling) — folds into security doctrine.
- **PSYOP** (persuasion) — partially covered by Custer's draft_* tools.
- **Chaplain Corps** (ethics / wellness support) — TOP's role.
- **Reserves** (surge capacity / on-call agents) — cost discipline; not yet a felt need.

Bundling all 12 candidates into spec would be exactly the move that produced tonight's retraction cascade — doctrine outrunning evidence.

---

## Commit discipline

Per Law V (the Echelon Decay Gate) applied recursively to doctrine itself:

1. **No section in this file is allowed to migrate to `MISSION_COMMAND_ARCHITECTURE.md` without a passing Funkytown experiment** under the validation requirement named in its section.
2. **No external claim** (in pitches, PR/FAQs, EXPLAINER, README) is allowed to reference these extensions as part of the validated thesis. They are proposals only.
3. **If a Funkytown experiment falsifies any extension**, the section here is updated with the falsification result and either revised or retracted. Falsifications are doctrine evidence, not failures.
4. **If two extensions interact** (e.g., medical evacuating to staff channel; signal carrying medical evacuation packets across units), the interaction is spec work that requires its own validation, not free-composition.

The file is a staging area, not a backlog. Sections move out (to MCA proper, or to retraction) when evidence arrives. Sections that sit here for more than a quarter without an attempted experiment are candidates for removal — doctrine that nothing wants to test is doctrine that should not exist.
