# MCA — Murder Board Decision Record (2026-07-07)

**Status:** **RATIFIED by Hans 2026-07-07** (with the three open calls answered — see "What this does NOT decide", now resolved). The panel was advisory; these are Hans's decisions.
**Inputs:** 4 murder-board runs (Grok/xAI + GPT/OpenAI ×2 rounds; +Fable/Anthropic; +Gemini/Google
verification; +Gemini solo full-ruling). Transcripts in session scratchpad. Total spend ~$0.90.
**Under test:** MCA's three sub-theses — (1) the doctrine port is load-bearing engineering; (2)
biography is the moat; (3) it scales by recursion.

---

## BLUF

**Unanimous verdict across all lineages: REWRITE (class: EXPERIMENT). No KILL.** The build is not
wrong; the **claim stack is inverted** — the cheapest ~20% (a small governance kernel) carries almost
all the *validated* value; the expensive ~80% (11-role staff roster, MDMP ceremony, Squad→COCOM scale
ladder, biography-moat marketing) carries almost all the *unvalidated* risk. Ship the kernel, demote the
rest to configuration + labeled narrative, and gate every bold claim behind three cheap experiments.

The doctrine framing is **not dead** — but its defensible form is narrower and different from how it's
currently claimed (see "Corrected claim stack").

---

## Corrected claim stack (what's earned / unproven / broken)

| Sub-thesis | Prior claim | Post-board verdict |
|---|---|---|
| **1 — port is load-bearing** | "Strip the Army vocab and you don't get a generic swarm" | **PARTIALLY TRUE.** A ~5-primitive governance kernel genuinely generalizes and is non-default. The 11-role roster / MDMP ceremony / scale ladder are **unproven vs. a competent from-scratch design** and must not be claimed as load-bearing until tested. |
| **2 — biography is the moat** | "The moat isn't the model, it's the memory" | **NOT EARNED — retire from marketing now.** Corpus-predicts-judgment reached parity on *routine* decisions (failure to confirm, not falsification). A judgment-moat, if it exists, lives in rare **refusal/veto** cases, never isolated. Defensible fallback (true by construction): *"the moat is the accumulated decision/refusal log corpus."* |
| **3 — scales by recursion** | "Company-shaped, composes upward to multi-tenant" | **UNVALIDATED — do not build on it.** N=3 at Platoon is the whole base. Cap all public claims at Platoon (≤10 agents) until an escalation-failure curve at 3→6→11 agents shows sub-linear error-per-handoff. |

## The governance kernel — what actually ships (5 primitives, Fable's set)

The load-bearing, disconfirmation-resistant core — domain-neutral, ~40–100 LOC, wraps any orchestrator:
1. **World-boundary approval gate** — any action affecting external state queues for human approval.
2. **Self-approval ban** — staff/line separation enforced in code (a gate an agent can clear for itself
   is theater). *Most disconfirmation-resistant element in the entire evidence base.*
3. **Advisory-decline-becomes-evidence log** — immutable; a declined flag that later predicts a failure
   is doctrine evidence, surfaced at review.
4. **Intent-contract task messages** — goal + constraints + acceptable-risk, never procedure. The one
   genuinely non-default message shape from ADP 6-0.
5. **Calibrated-confidence reporting** — "I don't know" as a valid, valued output.

**Demote** the 11 named S-sections, MDMP ceremony, and scale ladder to **configurations the kernel
supports** ("Domain Packages"), not the architecture.

## Surfaced disagreements (NOT smoothed — the signal)

1. **Does the source of the borrowed spec matter?**
   - *Grok + GPT:* No — any complete spec is an equivalent forcing function; seed the kernel with a
     plain-English (ITIL-style) authority grammar to kill the vocab confound at zero cost.
   - *Gemini (dissent):* **Yes — domain-fitness is the active ingredient.** A domain-mismatched spec
     (hospital ICS for maneuver warfare; ITIL for adversarial business ops) fails. Army doctrine is
     valuable *because* its domain — adversarial, hierarchical, mission-oriented — **matches
     competitive business operations.** "The costume IS the capability because the costume dictates the
     function." → This partially rescues the doctrine framing, reframed as domain-fit, not magic.
   - **Unresolved. Bears on whether the default Domain Package is neutral-grammar or military-doctrine.**

2. **How large is the vocabulary-priming effect?**
   - *Grok + GPT:* Small — <4% on outcome metrics (not style) for xAI/OpenAI; 2-arm test may suffice.
   - *Gemini + Fable:* Large and conceptual (ontology activation, not style); **understated** by the
     claim; 3-arm mandatory. Gemini + Fable are the two that say "big"; note Fable is Anthropic-lineage
     and Grok flagged Anthropic's tuning may make the effect largest there.
   - **Operator deploys on Anthropic → treat the effect as real for our models → 3-arm is the safe
     default.** Both disagreements are settled cheaply by E1 below.

## Decided build order

1. **Ship the 5-primitive kernel** as a domain-neutral layer. This is the product surface.
2. **Instrument the queue-depth tripwire** (Grok): measured approval-queue depth per tenant; if it
   exceeds one business day of the commander's review bandwidth, **halt onboarding — never relax the
   gate.** This is the operational failure mode that arrives first.
3. **Retire "biography is the moat"** from all external material this week. Replace with "the moat is
   the accumulated decision/refusal log corpus."
4. **Reposition doctrine honestly:** not "the Army was right about agents" — *"we used a complete,
   domain-fit authority spec as a forcing function; source chosen for domain-fitness, validated
   empirically."* Doctrine becomes the first **Domain Package**, explicitly labeled.
5. **Cap all scale claims at Platoon** until the escalation curve exists.

## E1 — the deconfounded ablation (design this before writing agent code)

Gemini's 3-arm design (the cleanest proposed); resolves BOTH disagreements at once. Home: a funkytown
experiment (successor to Exp 01, which validated MCA at Platoon).

- **Arm A — Full system:** kernel + MCA Domain Package (structure) + **Army vocabulary**.
- **Arm B — Structure only:** kernel + MCA Domain Package (structure) + **plain vocabulary**.
- **Arm C — Control:** kernel + baseline "Corporate Team" package (Manager/Lead/Analyst) + plain vocab.
- **Reads:** `(B − C)` isolates the value of the **MCA structure**; `(A − B)` isolates the value of the
  **military vocabulary** (the priming effect, on *our* deployment family).
- **Design:** N ≥ 20 tasks/arm, procedurally varied, ambiguous enough to require escalation judgment.
  Pre-registered metric = **logged coordination failures** (Grok's metric); secondary = human-review
  hours, tokens/accepted-output, decision latency. Score *structural* markers (escalation correctness,
  role hand-off, boundary misses) separately from *style*, so a vocab-driven style shift can't be
  mistaken for a structural win.
- **Decision rules:** structure earns its keep iff `(B − C)` clears a pre-registered threshold. If
  `(A − B)` < 3% → drop to 2-arm for future tests and treat vocab as cosmetic. If `(A − B)` is large →
  vocabulary is a real lever on Anthropic models; surface it as an explicit, labeled config, never a
  silent default.
- **Est. cost:** ~$500–1k, weeks not months.

## E2 / E3 (independently priced — do not bundle behind E1 or scale)

- **E2 — founder-fluency (the only test that touches H_C):** one **non-veteran** builder replicates a
  real workflow from kernel-only docs vs. full-MCA docs; measure onboarding time, error rate, output
  quality. Settles whether MCA is portable architecture or Hans-coherence scaffold.
- **E3 — the moat, where it would actually live:** Law VI re-run on **refusal/veto cases specifically**,
  not routine decisions. Clears → ship the refusal set as a copy-resistant constraint pack. Parity →
  the biography-moat claim stays retired; the log-corpus claim stands.

## Second Domain Package (proves the architecture, not a claim)

Gemini's recommendation: once the kernel + MCA package works, build a **second package from a different
high-consequence domain — aviation Crew Resource Management (CRM)** — flatter hierarchy, cross-checking,
a deliberate contrast to MCA. Running both MCA and CRM packages on the same kernel *proves* the
pluggable-kernel thesis empirically. Deferred; not gated here.

## Hans's calls — RESOLVED 2026-07-07

1. **Product-you-sell vs. force-multiplier-you-own → BOTH.** The orchestrator's amendment is ratified as
   the operating rule: **de-uniform what you sell; keep the uniform on what you operate.** The sellable
   surface is the neutral kernel + Domain Packages; Hans's own operating layer keeps the military
   framing for coherence. Grok's 60-day paid-WTP test remains available before any open-source decision.
2. **E1 now.** The 3-arm ablation is the greenlit next build — the cheapest thing that converts the
   biggest unknown.
3. **Kernel lives as a chassis primitive.** → **GATED behind cheap-gate-first** (`feedback-cheap-gate-
   first-before-chassis-code`): the second-product portability sketch (kernel vs. TOP) runs BEFORE any
   chassis code is written. Non-negotiable per Hans's own doctrine; that ~15-min sketch is the first
   step of the kernel build, not this decision.

**Immediate build queue:** (a) E1 experiment design + harness [now]; (b) kernel chassis primitive,
first step = cheap-gate-first portability sketch [after/parallel]. One at a time.

---

*Ratified. E1 is the active build.*
