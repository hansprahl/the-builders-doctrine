# Shaping Operations — Phase 0, Branches, and Sequels

**Status:** v0.2 — 2026-05-20 — gating-mechanism shell validated at Squad scale via Exp 07b cross-family falsification (Grok + Gemini both above falsification thresholds); PC content quality measured as a multiplier on top of the shell.
**Source authority:** ADP 5-0 (The Operations Process), FM 5-0 (Planning and Orders Production), JP 3-0 (Joint Operations) Phasing Model
**Builder authority:** Hans Prahl (J3 muscle memory, surfaced 2026-05-20 during Exp 06 hardening)
**Relationship to other doctrine:** Extension to [MISSION_COMMAND_ARCHITECTURE.md](MISSION_COMMAND_ARCHITECTURE.md); operates within the MDMP subroutine the doctrine already names. Civilian glosses follow the convention established in [ADP_6_0_TRANSLATION.md](ADP_6_0_TRANSLATION.md).

---

## The gap this document closes

The chassis as built executes decisive operations well. CC reads brief, sets intent, PLs plan, SLs dispatch, artifacts get produced, AAR closes the loop. That is the **Phase III** of the joint phasing model — *dominate*. The decisive operation.

What the chassis does not do explicitly:

- **Phase 0 — Shape.** Before decisive operations begin, what conditions must exist in the operating environment for them to succeed? What needs to be set, pre-positioned, gathered, degraded, or modified before the main operation runs? A combatant command spends years in Phase 0 — partner training, ISR coverage, basing rights, narrative pre-positioning, key-leader engagement — so that when Phase III kicks off, the environment is *already shaped* in the operation's favor.
- **Branch plans.** Pre-thought forks for "if the environment shifts during execution, here is the next move." MDMP doctrine names these explicitly; we do not produce them.
- **Sequel plans.** Pre-thought next-operation OPORDs — "after this operation succeeds (or fails), here is what we execute next." Also MDMP doctrine; also absent from our pipeline.

A combatant command without Phase 0 is a unit that executes well only when the environment happens to be favorable. A combatant command without branches and sequels is a unit that wins the first engagement and freezes when the situation changes.

We are the latter. This document specifies the fix.

---

## What "Shape" means in Army doctrine

**Joint Pub 3-0 phasing model (six phases, summarized):**

| Phase | Name | What happens |
|---|---|---|
| **0** | **Shape** | **Continuous, often years long. Set conditions for decisive operations. Partner-force training, ISR, info ops, civil affairs, economic measures, deception, key-leader engagement.** |
| I | Deter | Demonstrate capability and resolve to prevent escalation |
| II | Seize Initiative | Apply force to gain advantage; degrade enemy C2 |
| III | Dominate | Decisive operations — the main effort |
| IV | Stabilize | Restore essential services and security |
| V | Enable Civil Authority | Transition to civil control |

**Key doctrinal points:**

1. Phase 0 is **continuous**, not a discrete event. Shaping never stops. While Phase III is running for one mission, Phase 0 is already shaping the environment for the next mission.
2. Shaping operations are **deliberate** — they have intent, named effects, named actors, named time horizons. They are not "background activity."
3. Shaping produces **measurable conditions** in the operational environment. The Phase III mission analyst can read those conditions out of the COP and decide whether the environment is shaped enough to launch.
4. Without Phase 0 explicitly named, the staff defaults to assuming the environment is whatever it happens to be when the mission analyst opens the brief. That assumption is the source of most operation failures that look like "we executed perfectly but the environment was wrong."

**Civilian gloss.** Phase 0 = the work you do *before* the launch to make sure the launch lands. Recon, audience research, pre-positioning, partner alignment, narrative seeding. The work that, if you skip it, makes the launch feel like shouting into a void no matter how good the launch is. Every successful startup launch has months or years of invisible Phase 0; every failed launch is a Phase III plan dropped into an unshaped Phase 0 environment.

---

## What changes in MCA

Today the chassis runs (Operator-shape):

```
Brief → Mission Analysis → COA Development → COA Selection
      → OPORD → INTENT_DOWN → execution → SITREP_UP → AAR
```

Mission Analysis is the closest thing we have to Phase 0. It reads the environment. But it does not *change* the environment. It does not produce shaping orders. It does not name pre-conditions that must exist before Phase III can launch.

**With Phase 0 explicit, the chassis runs:**

```
Brief → Mission Analysis → Phase 0 Shaping OPORD ────────────────┐
                                                                  │
                                                                  ▼
                                                          [Shape operations:
                                                           ISR, prep, partner
                                                           alignment, narrative,
                                                           pre-positioning. May
                                                           run for hours, days,
                                                           or weeks before
                                                           Phase III launches.]
                                                                  │
                                                                  ▼
                          Conditions met? ─────── no ─── continue Phase 0
                                  │ yes
                                  ▼
                     COA Development → COA Selection → OPORD → INTENT_DOWN
                                  │
                                  ▼
                          Execute Phase III ──── concurrent ──── Branch monitoring
                                  │                              (env shifts trigger
                                  ▼                               branch activation)
                              SITREP_UP
                                  │
                                  ▼
                                AAR → Sequel plan triggers next OPORD
```

Two new named artifacts:

1. **Shaping OPORD (Phase 0 OPORD).** Distinct from the main OPORD. Output: named pre-conditions, recon priorities, environment-modification actions, who owns each, by what date, with measurable completion criteria. Phase III gate cannot lift until all named pre-conditions read "set."
2. **Branch Plans + Sequel Plans.** Branches: pre-thought forks attached to each Phase III COA. Sequels: pre-thought next-operation OPORDs at the end of each AAR. Both follow OPORD shape but live in COP rather than firing immediately.

---

## Shaping OPORD — proposed schema

A Shaping OPORD is an OPORD-shaped artifact. It uses the same skeleton as a normal OPORD (Situation / Mission / Execution / Sustainment / Command and Signal) but the *content* is shaping-specific.

```
SHAPING_OPORD_v0.1 (Phase 0)

1. SITUATION
   1.1 Operational environment as-is (what's true today)
   1.2 Operational environment as-required-for-Phase-III (what must be true to launch)
   1.3 Gap analysis: difference between 1.1 and 1.2

2. MISSION
   "By <date>, shape <named environment elements> such that
    <named pre-conditions> are met, in order to enable Phase III launch."

3. EXECUTION
   3.1 Named shaping actions (each with: actor, target, effect, completion criterion)
   3.2 Sequencing — which actions run when, dependencies between actions
   3.3 Measure-of-effectiveness per action — how do we know it worked?

4. SUSTAINMENT
   4.1 Resources required (compute, time, capital, attention, partner cooperation)
   4.2 Burn rate, abort criteria

5. COMMAND AND SIGNAL
   5.1 Who owns the Phase 0 plan (typically the CC's S-3-shape — operations staff)
   5.2 Phase III launch gate — named human or named role with authority to lift the gate
   5.3 Reporting cadence during Phase 0

PRE-CONDITIONS (the named output that gates Phase III):
- [ ] PC-1: <named condition>     status: [ unset | in-progress | set ]   owner:
- [ ] PC-2: <named condition>     status:                                  owner:
- [ ] PC-3: ...
```

The pre-conditions list is the *gate*. CC cannot launch Phase III until every PC reads "set." This is the architectural mechanism that makes shaping deliberate rather than implicit.

---

## Branch Plans — proposed schema

A Branch Plan is attached to a Phase III COA. It says: "if the environment changes in shape X during execution, switch from this COA to the named branch."

```
BRANCH_PLAN_v0.1 (attached to a Phase III COA)

TRIGGER:
   <named environmental condition that, if observed during execution, activates this branch>
   Example: "Wabash compliance analyst out for >7 days during 01-08→01-15 launch window"

DECISION AUTHORITY:
   <named human or named role with authority to activate this branch>

BRANCH OPORD (concise):
   1.1 What changes from the main OPORD
   1.2 What stays the same
   1.3 Re-task assignments (who picks up what)
   1.4 Estimated time to switch
   1.5 What success looks like under the branch
```

Branches are pre-staged at OPORD time, sit dormant in COP, and activate on observed trigger conditions. They are not "the contingency we'll figure out in the moment" — they are written, signed, gate-cleared *before* execution starts.

---

## Sequel Plans — proposed schema

A Sequel Plan is produced at AAR time. It says: "based on what happened in this operation, here is the next OPORD."

```
SEQUEL_PLAN_v0.1 (produced at AAR closure)

PRIOR OPERATION SUMMARY:
   What ran, what succeeded, what failed, what changed in the operational environment.

SEQUEL TRIGGER:
   Did this operation succeed, partially succeed, or fail? (Outcome determines which
   sequel applies — sequels for each outcome are pre-planned.)

NEXT OPERATION OPORD (initial draft):
   Standard OPORD shape. May reuse 60-90% of prior OPORD if the operation succeeded,
   or restructure heavily if it failed. The point is that the next OPORD is *already
   drafted* when AAR closes, rather than starting from scratch.

CARRY-FORWARD CONDITIONS:
   What pre-conditions are already set as a side effect of the prior operation?
   (These reduce the next Phase 0's workload.)
```

Sequels turn the chassis from a one-shot pipeline into a campaign. The Operator runs operations, not one-time launches.

---

## Distinguishing Phase 0 from Mission Analysis

The two are related and easy to conflate. They are not the same.

| | Mission Analysis | Phase 0 Shaping |
|---|---|---|
| **When** | Once, at start of each OPORD cycle | Continuous, often pre-dating the OPORD by days/weeks |
| **What it does** | *Reads* the environment | *Modifies* the environment |
| **What it produces** | A read-only situation report | OPORDs that direct shaping actions; named pre-conditions that gate Phase III |
| **Whether it acts** | No — analyst, not actor | Yes — directive, with owned named effects |
| **Civilian analog** | "Doing your homework before you write the launch plan" | "Doing the work that makes the launch possible — building the email list, getting the endorsements, pre-positioning the press, etc." |

In MCA terms: Mission Analysis is an S-2-shape function (intel staff advising). Phase 0 is an S-3-shape function (operations staff directing).

---

## Product applications

### Operator (autonomous business agent)

**Phase 0 examples for a typical Operator brief ("launch product X"):**

- PC-1: Mailing list grown to N qualified subscribers
- PC-2: At least M named press contacts briefed on the launch
- PC-3: Pricing positioning A/B tested against competitor set
- PC-4: Customer-facing FAQ legally reviewed
- PC-5: Support runbook in place, on-call rotation named
- PC-6: Distribution channels (App Store, Stripe, etc.) configured and tested

A launch operation cannot fire until all six read "set." Today Operator skips this. The launch fires whenever the operator says "go" — and the operator can say "go" before any of the six are true.

**The Phase 0 specialist this implies:** an S-3-shape ("Shaping Officer") who owns Phase 0 OPORDs. May initially be a role on the existing Operator MDMP loop rather than a new agent. Pre-condition gate enforcement is the lift.

### Custer (campaign management)

**Phase 0 examples for a campaign push:**

- PC-1: Voter universe segmented and prioritized by persuadability score
- PC-2: At least N delegate endorsements secured before the assembly push
- PC-3: Opposition message vectors enumerated and counter-messages drafted
- PC-4: Volunteer base trained for the door-knock scenario
- PC-5: Local press contacts briefed; rapid-response drafts on file

Custer kind of produces these (voter universe brief, opposition brief, delegate contact log) but treats them as deliverables, not as gating pre-conditions. The Phase 0 reframe is: these are *gates on the door-knock OPORD*, not by-products of it.

### TOP (Thriving On Purpose)

**Phase 0 examples for a wellness intervention:**

- PC-1: Sleep environment audited (light, noise, temperature)
- PC-2: Pantry audit complete; trigger foods identified and addressed
- PC-3: Social support network mapped; at least one peer enrolled as accountability partner
- PC-4: Crisis-line numbers stored in phone, partner notified
- PC-5: First-week routine block scheduled; conflicting commitments resolved

The wellness equivalent of "shaping the environment" is real — most interventions fail because the environment is hostile to the new behavior, not because the new behavior is wrong. TOP would benefit from a Phase 0 specialist that enforces these conditions before the daily-prompt loop starts asking the user to change behavior.

### Funkytown (sandbox)

**Phase 0 examples for the Wabash AAT2 brief:**

- PC-1: Compliance analyst absence-coverage plan reviewed and approved
- PC-2: Flag-list ownership assigned in writing
- PC-3: Audit-trail immutability mechanism specified
- PC-4: General Counsel sign-off on three open contract sections (5b, 7a, 9c)
- PC-5: Renata Senior Architect availability confirmed for pre-launch review block

The Exp 06 Squad 1/3 artifacts (regulatory_delta, spof_continuity_plan, audit_trail_documentation) *describe* these conditions but do not *enforce* them as gates. A Phase 0 reframe would make the Squad 1/3 outputs the gating pre-conditions of the launch OPORD, not deliverables of it.

---

## Why this matters for the grader-bias finding from Exp 06

The Sonnet-vs-Opus grader divergence in Exp 06 hardening shows that **evaluation** is doctrinally underdeveloped in the chassis just as **shaping** is. Both gaps point in the same direction: we have good execution doctrine and weak preparation-and-evaluation doctrine.

Shaping is the "before" gap. Evaluation is the "after" gap. The chassis as-built treats both as implicit. Both need explicit named-artifact-producing roles to stop being implicit.

The connection: a Shaping OPORD specifies measurable completion criteria for each pre-condition. Those criteria are themselves evaluation primitives. The same artifact discipline that makes shaping explicit makes the post-operation evaluation cleaner. **A chassis that does Phase 0 well will produce AAR data that an evaluator can read; a chassis that skips Phase 0 produces AARs that have nothing to evaluate against except "did the deliverables ship."**

---

## Open questions before piloting

1. **Where does Phase 0 live in the existing MCA seat structure?** Candidates: a new S-3-shape staff seat ("Shaping Officer"), an extension of the existing PL planning loop, or a separate Squad upstream of the line Squads.
2. **How is the Phase III gate enforced architecturally?** A COP-level check at the start of every execution call? A separate "gate lifted by" event? A named human authority?
3. **Sequel chaining — when does the chassis stop?** If every operation produces a sequel, the loop never closes. Need an end-state criterion at the CC level.
4. **Branch activation latency.** If a branch trigger fires mid-execution, how fast can the chassis switch? What state has to be preserved during the switch?
5. **How does Phase 0 interact with cost?** Shaping operations consume time and compute. A chassis that runs Phase 0 indefinitely never executes. Need a budget per Phase 0.

---

## Recommended next move

**Pilot in funkytown (Exp 07) before touching Operator.** The same pattern as Exp 05 → Exp 06: test the chassis change in the sandbox, then port to production once the mechanism is validated.

Specifically:

1. Add a Phase 0 Squad upstream of the existing Squad 1/3 in funkytown Exp 06.
2. Phase 0 Squad produces a Shaping OPORD with 4-5 named pre-conditions.
3. Squad 1/3 dispatch is gated on those pre-conditions reading "set" in the COP.
4. Compare runs with Phase 0 vs without (using same SQUAD_BRIEF.md as Exp 06).
5. Grade with Sonnet AND Opus (we know they disagree; capture both).

If the Phase 0 version produces meaningfully different artifacts — or if the gating itself produces value (because Squad 1/3 has to wait for conditions to be set, which surfaces real gaps in the brief that lean execution would have masked) — port to Operator's MDMP.

Estimated cost: ~$5-10, ~2 hours build, half-day analysis.

---

## Status

**v0.2 — gating-mechanism shell validated at Squad scale, with measured content-quality multiplier on top.**

Empirical history:

- **v0.1 (drafted 2026-05-20 morning).** Doctrine entry only, no code, pilot pending.
- **Pilot — Exp 07 (2026-05-20 afternoon).** Full ~90-line hand-authored Shaping OPORD prepended to D18 (Sonnet + coord, no personas). Result: 11/12 wins vs D18 under both Sonnet and Opus graders; NA axis +2.14. Initial verdict: structured-PC gating validated.
- **Adversarial review — Grok (2026-05-20).** Verdict: ARTIFACTUAL. Six attacks landed; primary attack: cannot separate the gating *mechanism* from the ~90 lines of substantive *content*. Doctrine propagation HALTED.
- **Falsification — Exp 07b (2026-05-20 evening).** Stripped the substantive content to a single neutral sentence ("List any open pre-conditions or gaps from prior artifacts and close them before declaring complete. Use named roles where appropriate.") and ran N=6 against N=6 D18 baseline. Blind-graded by four graders (Sonnet, Opus, Grok-4, Gemini 2.5 Pro). Non-Anthropic graders decisive per pre-registered spec.
  - Cross-family verdict: 32/48 wins (67%), NA delta +1.02. Both falsification thresholds (NA ≥ +0.8, wins ≥ 7/12) cleared.
  - Verdict: **SURVIVES in attenuated form.** Shell carries ~48% of the original NA lift; substantive PC content carries the other ~52%.

What this means for the doctrine:

- The gating *shell* (Soldiers prompted to surface and close gaps with named roles) is the load-bearing primitive. It carries measurable lift independent of PC quality.
- The substantive PC *content* (specific roles, dated triggers, status flags, sequencing) is a measured multiplier on top of the shell — roughly doubling the named-accountability lift in the Wabash case.
- Both primitives are real. A v0.2 implementation may ship with the minimum-viable shell and add hand-authored PCs as a quality multiplier where the deliverable warrants the authoring cost.

Deferred follow-ups:

- Human-grading third leg (HUMAN_GRADING_PACKET.md, 12 EXP07B-vs-D18 pairs) is queued; verdict revisable if it lands materially different from the LLM consensus.
- Exp 07b secondary analysis (EXP07B-minimal vs EXP07-full head-to-head) not yet graded; current shell-vs-content split is estimated by subtracting deltas, not measured directly.
- Generalization beyond Wabash regulatory-compliance brief untested.
- Phase 0 Squad as *generator* (can an agent produce equivalent-quality PCs?) deferred to a separate experiment.

---

## Cross-references

- [MISSION_COMMAND_ARCHITECTURE.md](MISSION_COMMAND_ARCHITECTURE.md) — the architecture this extends
- [ADP_6_0_TRANSLATION.md](ADP_6_0_TRANSLATION.md) — civilian glossary; Phase 0 / branches / sequels will be added there in next pass
- [MCA_PROPOSED_EXTENSIONS.md](MCA_PROPOSED_EXTENSIONS.md) — companion file for proposed MCA additions; this doc is a candidate for promotion into MCA proper after pilot
- funkytown Exp 06 FINDINGS.md — the experiment that surfaced the gap

---

*Drafted in response to Hans's J3 observation that the chassis executes well but does not shape. The observation was correct.*
