# Amazon Leadership Principles — Cross-Map to Builders' Doctrine

**Status:** v1.0, 2026-05-12
**Origin:** Brad Hampton (MegazoneCloud) call 2026-05-12 — directed Hans to Amazon's Leadership Principles + Working Backwards as the vocabulary AWS/SaaS channel buyers already trust.
**Purpose:** Map Amazon's 16 LPs against Builders' Doctrine's 12 principles. Determine what to translate (vocabulary for pitches), what to codify (genuinely new), what to reject (doesn't fit a solo-builder posture), and where to hold the line (conflicting at scale).
**Rule:** When pitching the SaaS channel, speak their vocabulary. Internally, hold the Builders' Doctrine. Same shape as the GEPA borrow — take the structural pattern the audience trusts; keep the moat in what feeds it.

---

## Full cross-map

| # | Amazon LP | Builders' Doctrine equivalent | Action |
|---|---|---|---|
| 1 | **Customer Obsession** — start with customer, work backwards | **#3 Designed to be needed less, not more** — sharper, constrains *against* engagement maximization | Translate vocabulary; hold the line |
| 2 | **Ownership** — long-term, beyond your team | (no direct equivalent — practiced, not codified) | **Codify as new #13 The Long Horizon** |
| 3 | **Invent and Simplify** | Practiced ("don't refactor what isn't broken", terse, additive) but not principled | Translate vocabulary |
| 4 | **Are Right, A Lot** | **#6 Truth as architecture** — stronger formulation (built lie-detector into own product) | Translate vocabulary |
| 5 | **Learn and Be Curious** | **#12 What else? Active extraction** — adjacent, MI-trained version | Translate vocabulary |
| 6 | **Hire and Develop the Best** | N/A — solo operator | **Reject explicitly** |
| 7 | **Insist on the Highest Standards** | **#7 Stoic commandments** — adjacent register | Translate vocabulary |
| 8 | **Think Big** | **#2 The moat is the memory** + practiced (Anguilla, Operator-as-SaaS) | Translate vocabulary |
| 9 | **Bias for Action** — speed matters; Type 1 (irreversible) vs Type 2 (reversible) | **#4 Chain of command over autonomous AI** — your approval gate IS Type 1/Type 2 in different vocabulary | Translate vocabulary |
| 10 | **Frugality** | Implicit — solo operator, AI build, no team | Translate vocabulary |
| 11 | **Earn Trust** — listen, speak candidly, self-criticize | **#6 Truth as architecture** + **#7 Stoic commandments** | Translate vocabulary |
| 12 | **Dive Deep** — details, audit, skepticism on metrics | **#12 What else? Active extraction** + "audit before declaring done" + "lead with measured, not built" | Translate vocabulary |
| 13 | **Have Backbone; Disagree and Commit** | "Hold the line under pull" (Law I at personal scale) + **#7 Stoic commandments** | Translate vocabulary |
| 14 | **Deliver Results** | Practiced ("85% on time beats 100% late") | Translate vocabulary |
| 15 | **Strive to be Earth's Best Employer** | N/A — solo operator | **Reject explicitly** |
| 16 | **Success and Scale Bring Broad Responsibility** | **#5 Data sovereignty** + **#11 Crisis floors above features** + **#8 The Refusal** | Translate vocabulary |

## Where Builders' Doctrine is stronger

These aren't equivalences — they're upgrades the Builders' Doctrine offers over the Amazon LP:

- **Customer Obsession → Designed to be needed less.** Amazon's version drifts toward engagement maximization at scale (the metric is session length, retention, DAUs). Builders' Doctrine inverts: the metric is whether the user becomes more capable *without* the tool. Same starting posture, opposite endpoint.
- **Are Right, A Lot → Truth as architecture.** Amazon asks leaders to be right often. Builders' Doctrine builds the lie detector into the product itself (Reflection Gate, Prompt Guardian, AAR calibration). Not "be right a lot" — "leave evidence in the audit trail when wrong."
- **Have Backbone → Hold the line under pull.** Same posture, but Builders' Doctrine names the failure mode (cheerleading under social pressure) and codes against it (refusal lists, stoic register enforcement at Guardian audit).
- **Customer Obsession + Working Backwards together → still needs the dependency test.** Working Backwards optimizes for what excites the customer at launch. The dependency test asks whether what excites them at launch makes them stronger or more reliant. Both filters run; Working Backwards alone is incomplete for wellness-shaped products.

## Where to hold the line on conflicts

**Customer Obsession at scale drifts toward engagement maximization.** If you adopt "customer obsession" vocabulary in pitches, the doctrine internally has to be: *we obsess over the customer's outcome, not their session length.* Write that distinction explicitly into any product surface where the LP vocabulary appears. Don't let it erode the dependency test.

**Think Big in stoic register.** Amazon "Think Big" has produced both AWS and a lot of waste. Builders' Doctrine "the moat is the memory" already does the work — and stoic posture acts as the brake on think-big drift toward unfounded ambition. When pitching, speak "think big"; internally measure against the moat thesis and the refusal list.

**Hire and Develop the Best is solo-operator-incompatible.** Restate as: *Build agents you'd hire.* Named specialists with system prompts, tool allowlists, AAR track records, and Guardian audit history are the solo-operator analog. The principle isn't ignored; it's reshaped for who actually does the work.

## Working Backwards — the process artifact

Brad's load-bearing instruction wasn't just about Leadership Principles. It was about the **PR/FAQ method** (Working Backwards): write the press release and FAQ *before* code. Half of Amazon's PR/FAQs never become products — the writing surfaces weakness before any engineer is spent. AWS, Kindle, Prime Video, Alexa all came through this process.

This is a process artifact, not a principle. Lives at `~/Projects/the-builders-doctrine/WORKING_BACKWARDS.md` — when to write a PR/FAQ, the structure, the discipline rules, the review protocol.

**Where it sits in the Builders' Doctrine stack:**

- **Prompt Doctrine** governs every prompt across every product.
- **Agent Doctrine** governs every specialist's wiring.
- **Working Backwards** governs every new product, mode, or major feature *before code*.

The three are orthogonal. Working Backwards is the *scoping* layer; Prompt and Agent Doctrines are the *building* layer.

## Pitch-surface translation cheat sheet

When pitching SaaS-channel audiences (Brad's network, AWS-trained buyers, enterprise procurement):

| You say | They hear | Internal posture (don't say aloud) |
|---|---|---|
| Customer obsession | Familiar / trusted | Designed to be needed less — outcome over session length |
| Bias for action | Familiar / trusted | Chain of command — Type 1 actions gate to founder approval |
| Dive deep | Familiar / trusted | Active extraction — "what else?" battle drill from MI |
| Earn trust | Familiar / trusted | Truth as architecture — audit trail leaves evidence |
| Working backwards | Familiar / trusted | PR/FAQ before code; product survives the writing |
| Type 1 / Type 2 decisions | Familiar / trusted | Approval queue gates Type 1; agents execute Type 2 within scope |
| Frugality | Familiar / trusted | Solo operator + AI build; constraint-driven invention |

When pitching wellness audiences, MI-network audiences, or the veteran customer surface, the Builders' Doctrine vocabulary lands better than Amazon's. The translation is audience-conditional, not absolute.

## Audit cadence

Re-read this cross-map before any pitch to a SaaS-channel buyer. Re-read it before adopting any new principle that overlaps with an existing Builders' Doctrine principle — the trap is that translation drifts into replacement. The doctrine doesn't change. The vocabulary on the pitch surface changes.

## Sources

- Amazon Leadership Principles (official): https://www.amazon.jobs/content/en/our-workplace/leadership-principles
- Working Backwards — Colin Bryar's PR/FAQ guide: https://coda.io/@colin-bryar/working-backwards-how-write-an-amazon-pr-faq
- Working Backwards: Insights, Stories, and Secrets from Inside Amazon — Bryar & Carr (book): ISBN 978-1250267597
