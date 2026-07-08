# Training Architecture (TA)

**Status:** v0.1 — 2026-06-05. Doctrine, not a new experiment. Unlike `MISSION_COMMAND_ARCHITECTURE.md`, this document does not introduce unvalidated machinery — it **names a discipline already running in production across the portfolio** (Prompt Guardian, Reflection Gate, SPECIALIST_TEMPLATE certification, the AAR component, sandbox→gate→live rollout, the capability registry) and unifies it under one source doctrine. The components are validated by use; the *unification* is new and carries no separate empirical claim. See "What this does NOT establish" before citing it as more than that.

**Source doctrine:** U.S. Army ADP 7-0, *Training*. ADP 7-0 is the Army's published doctrine for how units build and sustain proficiency: a Mission Essential Task List (METL) of the tasks that matter, each task written as Task / Conditions / Standards, trained crawl-walk-run, certified to standard, and improved through the After Action Review. Refined over decades under the constraint that a unit that trains to a soft standard dies to a hard enemy.

**Companion to MCA.** ADP 6-0 (Mission Command) governs how authority flows *at runtime* — who may act, who must escalate. ADP 7-0 (Training) governs how a capability earns the right to act *before* runtime — how it is certified to standard and kept there. MCA is the chain of command; TA is the train-up and the readiness check. A product needs both: MCA says the staff specialist is advisory and the world boundary escalates to the commander; TA says that specialist does not go live until it is certified against its standard, and a NO-GO sends it back to retrain.

**Civilian readers:** every Army term used here is glossed in the "Civilian translation" section at the bottom. Read that first if "METL," "T/C/S," "crawl-walk-run," or "AAR" are unfamiliar.

**Claim:** Industry ships agents and "evals" as an afterthought — a benchmark run once, a vibe check, a launch. The Army solved "how do you certify that a unit can perform under real conditions, and keep it there" decades ago, under lethal stakes. TA ports that working doctrine onto the LLM substrate. The portfolio already does most of it; this document makes it legible, mandatory, and reusable.

---

## The principles, ported

ADP 7-0 (2024) enumerates **nine** principles of training (¶3-2). Each maps to a portfolio property that already exists or should. (Principle names below are verbatim from ADP 7-0; the 2026-07-07 ground-truth audit corrected an earlier version of this table that listed five and mislabeled two.)

| Principle (ADP 7-0 ¶3-2) | Portfolio property |
|---|---|
| **Commanders are the primary trainers** | Hans authors the commandments and STORY; the biography *is* the training data. The trainer of every specialist is the commander, not a vendor benchmark. (Builders Doctrine: "the prompts are the training data, and the builder writes the prompts.") |
| **NCOs train individuals, crews, and small teams; they advise commanders** | The NCO/SL tier owns task-level standards and QC within scope (MCA authority gradient). Squad-tier training and re-tasking happens without laddering to the commander. |
| **Train using multiechelon techniques** | Certification runs at every echelon (Squad → Platoon → Company), not just top-level. A capability is trained at the tier that owns it. |
| **Train as a combined arms team** | Specialists are certified working *together* (MDMP handoffs, cross-specialist review), not only in isolation — the combined staff, not just the individual officer. |
| **Train to standard using appropriate doctrine** | A capability ships when it passes its standard (GO), not when a sprint ends; and the standard is the *doctrine* (SPECIALIST_TEMPLATE, the commandments), not an improvised bar. Calendar pressure does not lower it. |
| **Train as you fight** | Certify under realistic conditions, not toy ones. The **Rubicon-simulated** stage runs plans against cohort digital twins; Drake (OPFOR) wargames against real adversary models; cross-family adversarial review tests prompts against Grok/GPT/Llama, not just the home model. |
| **Sustain levels of training proficiency over time** | The Guardian's *weekly* audit and the AAR loop keep a certified capability at standard after launch — proficiency decays without sustainment. |
| **Train to maintain** | Keep the tool itself serviceable: the reliability-checkpoint discipline (leave the tool better than you found it), the health heartbeat, dependency hygiene. Training includes maintaining the machine that trains. |
| **Fight to train** | Certification is not optional overhead to be cut under deadline. The CI gate (`guardian_ci.py`) makes it non-skippable — training time is defended, not sacrificed to the next feature. |

---

## The METL — what a unit must be able to do

A **Mission Essential Task List** is the finite set of tasks a unit must perform to standard. The portfolio already keeps METLs; it just doesn't call them that:

- **For a specialist:** its tool allowlist + scope statement *is* its METL — the bounded set of tasks it is certified to perform, and (by exclusion) the tasks it must refuse or escalate.
- **For a product:** the capability registry (Operator's `tools/capabilities.py`) *is* the METL — and its doctrine ("every entry must map to wired Python; mark un-deployed entries `specced`/`planned`, never `deployed`") is exactly METL discipline: you do not claim a task as trained-to-standard when it is not.

The refusal list is the METL's mirror image — the explicit set of tasks the unit is certified **never** to perform.

---

## Task / Conditions / Standards — the universal spec

Every Army task is written the same way, and so should every capability and every eval:

- **Task** — the measurable action. ("Send a buyer-facing Snapshot.")
- **Conditions** — what is given and what constrains it. ("Given an internal-reviewed brief; through the approval queue; with status tags stripped.")
- **Standards** — the GO/NO-GO criteria. ("Single confident number, no L1–L4 itemization, internal-review gate cleared.")

T/C/S is the bridge between a capability and its eval: **the standard is the eval.** A capability is not "done" until its standard is written down and checkable. The places this already lives:

- **Prompt Guardian** scores each specialist prompt against its commandments — a standard, checked.
- **The Reflection Gate** runs the *what else?* pass before `declare_done` — a standard, checked, on every response.
- **The eight commandments + `guardian_ci.py`** are the per-PR standard a change must clear before merge.

Where a capability has no written standard, it has not been specified — it has only been hoped for.

---

## Certify before trust — the train-and-certify-leaders loop

ADP 7-0 trains and **certifies** leaders before they are trusted to lead training. The portfolio analog is specialist onboarding: a specialist does not go live until it is certified against the build sheet.

`SPECIALIST_TEMPLATE.md` is that certification checklist — callsign, scope, tool allowlist, the Doctrine integration rows, approval-gated actions, refusal-scope lock, Guardian wiring. **Wiring the Guardian before merge is the certification.** An uncertified specialist is a leader who has not passed the standard, turned loose on a real mission. The template makes the standard explicit; the CI gate makes it enforced.

---

## Crawl–Walk–Run — the rollout, not just the lesson

Crawl-walk-run is progressive proficiency under rising realism. It is the curriculum's pedagogy (read → run → drive-it-live) **and** the portfolio's rollout discipline for a new capability:

| Rep | In the curriculum (human training) | In the product (capability rollout) |
|---|---|---|
| **Crawl** | Read the worked example | Build it; run it in a sandbox / paper-money mode (Drake) |
| **Walk** | Run `experiment.py` and watch each step | Run it behind the approval queue — every effect gated, nothing autonomous |
| **Run** | Drive the interactive widget blind, predict before revealing | Run it live, with the AAR and Guardian still watching |

You do not let a capability *run* (autonomous at the world boundary) before it has *walked* (proven correct under the approval gate). That is the same instinct as not letting a soldier run live-fire before dry-fire.

---

## The 8-step model and the AAR loop

ADP 7-0's training model ends where the value compounds: **Step 7 conduct an AAR → Step 8 retrain.** This is already a first-class portfolio component:

- **AAR** is Agent Doctrine component #9 and a chassis primitive (`kit/chassis/aar.py`). Every significant action gets a what-was-supposed-to-happen / what-happened / sustain-improve pass.
- **Advisory-never-override-always-log** (MCA) is the AAR's evidence trail: a declined Sentinel/Drake/Marshall flag that later predicts a failure is doctrine evidence, surfaced at the next review, not noise.
- **Retrain** is the closing of the loop: a NO-GO does not ship — it routes back. In the curriculum, a missed self-check sends the learner back to retrain the rung. In the product, a Guardian-flagged drift queues a correction for approval and re-audit.

The AAR is the mechanism by which "train to sustain" actually happens: proficiency is not certified once, it is re-certified continuously.

---

## The human-training instance — the learn-ai curriculum

The portfolio's first explicit TA instance is the `operator/learn-ai/` curriculum — Hans's own bottom-up AI training, built as Army training:

- The 10-rung ladder is the **METL**.
- Each rung opens with **Task / Conditions / Standards** and a TLO + ELOs.
- The practical is **crawl-walk-run** (read → `experiment.py` → drive the visual blind).
- The self-check is a **GO / NO-GO**; five-for-five advances, any miss is a **retrain**.
- Each rung closes with an **AAR**.
- A scheduled agent builds the next rung in this exact format and renders it to a browser course.

The curriculum is to TA what a product is to MCA: a concrete instance of the doctrine, not the doctrine itself. The same structure governs onboarding any human (a future PAS client, a teammate) or certifying any agent.

---

## What this does NOT establish

Same honesty discipline as MCA. This document does **not** establish:

- That naming the discipline "Training Architecture" improves any outcome beyond what each component (Guardian, Reflection Gate, AAR, SPECIALIST_TEMPLATE) already delivers on its own. The unification is for legibility and reuse, not a measured performance claim.
- That the T/C/S-as-eval framing has been ablation-tested the way MCA's Authority Gradient was in Funkytown. It has not. It is doctrine adopted because the components are already load-bearing, not because a controlled experiment showed the framing wins. **The validation home for closing this gap is Funkytown** (`funkytown/CLAUDE.md` registers TA as a certification-harness candidate) — does writing an explicit standard *before* build measurably change agent outcomes is the open experiment.
- That crawl-walk-run rollout is followed everywhere today. It is the standard this document sets; conformance is a separate audit.
- Anything about non-Claude families. Like the MCA meta-layer finding, any claim that certification-by-prompt-standard transfers across model families is unverified and out of scope here.

What stays load-bearing: the components are real, in production, and independently justified. TA is the doctrine that says they are one discipline — certify to standard before trust, sustain by AAR — and makes that discipline mandatory and portable.

---

## Civilian translation

The Army vocabulary, glossed. Inline these the first time a term appears in any external-facing artifact (same rule as `ADP_6_0_TRANSLATION.md`).

| Term | Civilian gloss |
|---|---|
| **ADP 7-0** | The U.S. Army's published doctrine on *Training* — how units build and keep the proficiency to perform their essential tasks. |
| **METL** (Mission Essential Task List) | The finite list of tasks a unit must be able to do well. Everything else is secondary. For an agent: its allowed scope; for a product: its real capability list. |
| **Task / Conditions / Standards (T/C/S)** | The fixed way every task is specified: the action, the circumstances it's done under, and the measurable bar for success. The standard *is* the test. |
| **TLO / ELO** | Terminal Learning Objective (what you can do at the end) and Enabling Learning Objectives (the sub-skills that build to it). |
| **Crawl–Walk–Run** | Train in three reps of rising realism: slow and guided, then assisted, then live under realistic conditions. Don't run before you've walked. |
| **Train to standard, not to time** | You're done when you meet the bar, not when the clock runs out. The deadline never lowers the standard. |
| **Train as you fight** | Practice under conditions as close to real as possible — real adversary models, real scenarios — so the certification means something. |
| **Train to sustain** | Proficiency decays. Re-check and re-train on a cadence; certification is continuous, not one-time. |
| **GO / NO-GO** | The binary readiness verdict. GO = meets standard, advance. NO-GO = does not, retrain and re-test. No partial credit. |
| **Certify** | Formally verify a leader/unit meets the standard before trusting them with the real mission. Here: a specialist passing the SPECIALIST_TEMPLATE build sheet + Guardian wiring before merge. |
| **AAR** (After Action Review) | The structured debrief: what was supposed to happen, what actually happened, what to sustain and what to improve. The loop that turns a single event into training. |
| **8-step training model** | ADP 7-0's plan → certify leaders → recon → issue plan → rehearse → execute → **AAR → retrain** cycle. The value is in the last two steps closing the loop. |

---

*TA is the readiness doctrine. MCA is the command doctrine. Together: a capability is commanded under intent and stops at irreversible (MCA), and it does not get to act at all until it is certified to standard and is kept there by the AAR (TA).*
