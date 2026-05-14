# META_DOCTRINE — Laws governing the framework itself

**Date opened:** 2026-05-13 evening
**Authored:** Hans Prahl (founder) + Grok adversarial-review trigger
**Status:** v0.1 — inaugural law (V) seeded; Laws I–IV reserved as placeholders for future formalization of existing implicit doctrinal laws.

---

## Why this file exists

The Builders' Doctrine (`THE_BUILDERS_DOCTRINE.md`) defines the principles. The Builders' Method (`THE_BUILDERS_METHOD.md`) defines the reproducibility framework. This file sits one level above both — it defines the **methodological laws** that govern how the doctrine itself is allowed to make claims.

The trigger event for opening this file was a 2026-05-13 evening adversarial review by Grok that named two over-claims in the day's work:
- The Reflection Gate's "structured-uncertainty enforcement" reframe was post-hoc salvage and violated the audit-measurement-before-law rule the founder himself wrote.
- The Funkytown Experiment 03 "first-contact validation of Mission Command at Company scope" claim was a toy-demo dressed as doctrine.

Both over-claims were retracted that night. The retraction surfaced the need for a methodological law that prevents the founder from inflating future rung-N claims on simplified or single-call evidence. Grok proposed that law explicitly. It is now Law V — Echelon Decay Gate.

The roman-numeral numbering (V) preserves Grok's framing and signals that Laws I–IV are implicit in the existing doctrine (biography as moat, audit-measurement-before-law, chassis-from-experiment loop, truth-as-architecture) and may be formalized into this file when convenient. The numbering is not load-bearing — the laws are.

---

## Laws I–IV — placeholders for future formalization

These laws are operating implicitly across the existing doctrine. Formalize them into this file when a future review surfaces the need.

- **Law I (implicit):** Biography as moat — the founder's lived sequence is the unfair advantage; the doctrine compiles it into agent behavior. Referenced in the Amazon LP cross-map and throughout `THE_BUILDERS_DOCTRINE.md`. Restated phrasing in some artifacts: *"hold the line under pull."*
- **Law II (implicit):** Audit measurement before drafting any law — codified as `feedback_audit_measurement_before_law.md` in memory and referenced in Funkytown Experiment 02. Any metric used to justify a doctrinal claim must be audited against trace data before the claim ships.
- **Law III (implicit):** Chassis-from-experiment loop — doctrine prose → experiment design → empirical test → chassis primitive → product integration → doctrine update. Each step constrains the next; falsified hypotheses update doctrine before the chassis ships. Named for the first time in `STORY.md` chapter for 2026-05-13.
- **Law IV (implicit):** Truth as architecture — Principle #3 of the doctrine elevated to a methodological law. Every doctrinal claim is calibrated against what is actually known. No softened intel, no false certainty laundered as confidence. The lie detector is built in.

---

## Law V — Echelon Decay Gate

**Stated:** Any rung-N validation claim on the MCA scale ladder (Squad → Platoon → Company → Battalion → Brigade → Division → Corps → Army Group → COCOM) requires **N≥9 full-hierarchy runs with live cross-echelon conflict injected**. Simplified single-call demos, hand-placed traps visible to the observer, and synthetic briefs without emergent conflict are rejected as evidence for the claim. The measurement surface must match the claim before the claim ships.

**Trigger.** 2026-05-13 evening. Funkytown Experiment 03 ran an N=3 MVP smoke test where each "platoon" was a single Sonnet call returning a SITREP — no PL turn loop, no SL squads, no real artifact production, no parallel platoon load, no synthesis surface beyond three short SITREPs. The CC found a hand-placed cross-customer trap I had buried in the brief. I committed the result as "first-contact validation of Mission Command Architecture at Company echelon." A second-opinion read from Grok named the gap plainly: N=3 simplified single-Sonnet returns on a synthetic brief is a proof-of-concept toy demo, not a doctrine-rung validation. The hierarchy was never stressed. The hierarchical-attention-decay failure mode that would actually test Company-scale coordination was not exercised because no real hierarchy ran. The trap was visible to me because I placed it there. None of that constitutes empirical validation.

**Why N≥9 specifically.** Three runs per platoon per echelon, with three platoons spinning up real PL+SL hierarchies, produces enough sample to bound the catch rate of an emergent failure with a meaningful confidence interval. N=3 at the top echelon with simplified subordinates does not. The 9 figure is calibrated to the smallest defensible sample for a doctrinal claim at this scale; it can be revised up but not down.

**Why "live cross-echelon conflict injected" specifically.** Hand-placed observer-visible traps test only that the CC can find what the observer already found. Real Company-scale coordination problems are *emergent* — they arise from the interaction of subordinate units operating under independent commander's intent translations, and they are *invisible* until cascade. The Echelon Decay Gate forbids the trivial case (hand-placed, visible) and demands the hard case (live-injected, emergent). The conflict injection harness is engineering scaffold required before any rung-N claim is allowed to ship.

**Hierarchical attention decay — the failure mode this law forces measurement on.** Grok's review surfaced an unnamed failure mode: at Company+ scale the Commander must synthesize multiple SITREPs containing conflicting tenant biographies and intent signals inside one context window. Human staffs are trained to chunk and prioritize; LLMs degrade non-linearly on multi-document synthesis. The previous probability estimates for the climb (Squad → COCOM) anchored on Squad/Platoon validating cleanly without exercising the synthesis surface where decay shows up. Law V exists in part to ensure the synthesis surface gets exercised at every rung before the claim advances.

**Operational consequences.**
- Rung 3 (Company) is **not yet validated** as of 2026-05-13. The MVP run set from that night is engineering scaffold, not a rung advance.
- The Squad → Platoon claims (rungs 1, 2) **were validated under conditions that meet or approximate Law V's standard** (Experiment 01 + 02 had real squad hierarchies, real artifact production, multiple runs). Those rungs remain claimed.
- The budget estimate to climb the rest of the ladder revises upward. Previous estimate (~$60K–120K total API) assumed simplified runs; under Law V the per-rung budget grows roughly 3–5× because N≥9 full-hierarchy runs replace N=3 simplified runs. New rough ladder budget: ~$200K–500K of API. This is the honest number.
- Any future claim of the form *"MCA scales to rung N"* must cite the N≥9 full-hierarchy + live-conflict run set that supports it, OR explicitly note the claim is engineering scaffold not doctrinal advance.

**Cross-references.**
- The retraction that produced Law V: Funkytown Experiment 03 FINDINGS.md, 2026-05-13 late evening.
- The audit rule Law V applies recursively to the framework: `~/.claude/projects/-Users-hansprahl-Projects/memory/feedback_audit_measurement_before_law.md`.
- The adversarial review trigger: 2026-05-13 evening Grok second-opinion paste (manual workflow; not persisted as memory per `feedback_grok_second_opinion_workflow.md`).

---

## What goes in future entries

Laws added to this file should govern *how the doctrine is allowed to make claims*, not *what the doctrine claims*. The distinction matters: principles in `THE_BUILDERS_DOCTRINE.md` describe what the builder does; laws in this file describe what the doctrine itself must do to remain honest. If a candidate entry feels like it belongs in the principles document, it does — keep it there.

Add an entry to this file when:
1. A specific incident reveals the doctrine made a claim it should not have been allowed to make.
2. A methodological rule emerges that would have prevented that incident.
3. The rule is concrete enough to be operationalized (a checklist, a quorum, a threshold, a refusal).

Do NOT add entries here that are restatements of existing principles. Do NOT add entries that read as ambition rather than discipline.
