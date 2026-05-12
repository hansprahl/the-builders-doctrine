# Working Backwards — Portfolio-Shared Process Artifact

**Status:** v1.0, 2026-05-12
**Origin:** Brad Hampton (MegazoneCloud) call 2026-05-12 — pointed Hans at Amazon's PR/FAQ methodology as gospel inside AWS and the broader SaaS channel.
**Authority:** Portfolio-shared. Sits alongside Prompt Doctrine and Agent Doctrine.
**Scope rule:** Required before any new product, new mode, or major feature ships in any portfolio product. Sits at the **scoping** layer; Prompt Doctrine and Agent Doctrine sit at the **building** layer.

---

## What it is

Working Backwards is a discipline: before writing a single line of code, the builder writes a **mock press release** describing the finished product as if it has already shipped, plus an **FAQ** answering customer questions and internal stakeholder concerns. The press release describes the product in customer language; the FAQ defends it against the hard questions a skeptic would ask.

The purpose is not the artifact. The purpose is the writing process. If you can't write a press release that excites a real customer, the product isn't worth building. If you can't answer the hard FAQ questions without hedging, the product isn't ready.

Half of Amazon's PR/FAQs never become products. The writing kills bad ideas cheaply. AWS, Kindle, Prime Video, Alexa all came through this process.

## When to write a PR/FAQ

**Required before:**
- Any new product (e.g., Assayer launch, Operator-as-SaaS, Vibeloom)
- Any new mode on an existing product (e.g., Operator's TRD/BRD generation mode)
- Any major feature that changes the customer-facing value proposition
- Any pitch that needs to land an external warm-intro request (e.g., Brad's network)

**Not required for:**
- Internal refactors that don't change customer-facing surface
- Bug fixes
- Doctrine updates (they have their own review surface — this file, the cross-map, the doctrine itself)
- Anything captured under "build one thing at a time" inside a single session

## The artifact — three parts, six pages total

### Part 1 — Press Release (~1 page)

Written as if the product has already launched successfully. Customer language only. No internal jargon. No hedging language ("we hope to," "we're exploring") — write it as if it's real.

**Required sections:**

- **Headline** — one line, customer-readable
- **Subheading** — audience + benefit, one line
- **Summary paragraph** — the news
- **Problem paragraph** — what's broken today, in concrete scenarios, not abstract pain points (Amazon's example: *"Readers who travel frequently carry three to four books in their bag, adding weight and bulk"* — not *"customers want convenience"*)
- **Solution paragraph** — how the product solves it
- **Quote from leader** — what the builder says about why it matters
- **Quote from a hypothetical customer** — what the customer says about the experience
- **Call to action** — what the customer does next

### Part 2 — External FAQ (~1–2 pages)

The questions a customer or a press reporter would ask. Direct, specific, no hedging.

**Required questions (minimum):**

- What is this product?
- Who is it for?
- What problem does it solve?
- How does it work?
- What does it cost?
- How is it different from [closest competitor]?
- When can I use it?
- What's the catch?

### Part 3 — Internal FAQ (~2–3 pages)

The hard questions stakeholders (and a skeptical advisor) would ask about feasibility, risk, and second-order effects. Longer, more challenging, blunt.

**Required questions (minimum):**

- Why are we building this?
- Why now?
- Why are we the ones to build it?
- What does the moat look like at scale?
- What are the unit economics?
- What's the technical risk?
- What's the regulatory/compliance risk?
- What happens if we fail?
- What's the kill criterion?
- Who is harmed by this product if it succeeds?
- What is the dependency test answer (wellness-scoped products only)?
- What is the refusal list check (every product)?

## The discipline — non-negotiables

1. **Customer-language only in the press release.** If a customer can't understand it, rewrite. Internal jargon, acronyms, and methodology vocabulary belong in the internal FAQ — not the press release.
2. **Persuasion test.** *"If this write-up doesn't convince someone to buy the product, it needs to be rewritten."* The test isn't whether the writer thinks it's good; it's whether the reader is moved.
3. **Six pages maximum.** Three minutes per page reading time. If it doesn't fit, the scope is too broad.
4. **No pre-reading.** The PR/FAQ is distributed only at the review meeting. Everyone reads the same version simultaneously. (Solo-operator adaptation: the founder reads the final draft cold immediately before the build-or-kill decision, not during the writing.)
5. **Iterative refinement.** Multiple drafts are normal. First draft is for the writer; second draft is for an advisor; third draft is for the build-or-kill decision.
6. **No code until PR/FAQ passes the build-or-kill review.**

## The review protocol — 60 minutes

**For Amazon (multi-person):**

- **20 minutes silent reading.** Everyone reads the entire PR/FAQ simultaneously. No pre-reading allowed.
- **40 minutes discussion.** Leadership provides high-quality feedback, poses challenging questions, identifies gaps.
- **Outcome:** build / investigate further / kill.

**For a solo operator (Hans-adapted):**

- **20 minutes silent reading.** Read the final draft cold, as if you weren't the writer. No editing during this pass — annotate only.
- **20 minutes adversarial pass.** Run the document through the relevant specialist for adversarial review: Drake for OPFOR/red-team, Halsey for engineering risk, Banks for unit economics, Sentinel for ethics. Each surfaces one or two blocking concerns.
- **20 minutes decision.** Build / investigate further / kill. If "investigate further," write down exactly what's gating the decision and what evidence would resolve it.

## Integration with Builders' Doctrine

**Before writing the PR/FAQ:**
- Confirm the proposed product/feature passes the **Refusal List** (Principle #8). If it violates a refusal, stop — don't write.
- Confirm the proposed product/feature passes the **Crisis Floors** check (Principle #11) if it touches a vulnerable user.

**During writing:**
- Apply **#12 What else? Active extraction** — drill into nouns, follow networks, find what the brief didn't volunteer. The PR/FAQ should reveal assumptions the brief buried.
- Apply **#6 Truth as architecture** — no hedging language in the press release; bluntness in the internal FAQ. The PR/FAQ leaves an audit trail of what the builder believed at scoping time.

**After writing:**
- The PR/FAQ becomes a doctrine artifact, archived under `~/Projects/<product>/working_backwards/<feature>_v<n>.md`.
- When the product ships, the launched product is audited against the PR/FAQ. Material drifts get logged. (This is the AAR loop — what we said we'd build vs. what shipped.)

## When to break the rules

The PR/FAQ is doctrine, not bureaucracy. Three escape hatches:

1. **Immediate-response builds** (rapid response to a campaign event, a security patch, a customer escalation) — skip the PR/FAQ; document the bypass in the post-action AAR.
2. **Exploratory spikes** under 4 hours — skip the PR/FAQ; if the spike produces something worth shipping, write the PR/FAQ after the spike, before any further build.
3. **Internal tooling for the founder only** — skip the PR/FAQ; the founder is the customer and the builder, so the artifact's review function collapses.

Any non-emergency build that exceeds 4 hours of work without a PR/FAQ is doctrine drift and gets flagged at the next Guardian audit.

## Templates

A template PR/FAQ skeleton lives at `kit/templates/PR_FAQ_TEMPLATE.md` in this repo. Each portfolio product can adapt it to product-specific FAQ sections (e.g., TOP adds the dependency-test FAQ question; Custer adds the voter-PII isolation FAQ question).

## Sources

- Amazon Leadership Principles (official): https://www.amazon.jobs/content/en/our-workplace/leadership-principles
- Working Backwards — Colin Bryar's PR/FAQ guide: https://coda.io/@colin-bryar/working-backwards-how-write-an-amazon-pr-faq
- Working Backwards: Insights, Stories, and Secrets from Inside Amazon — Bryar & Carr (book): ISBN 978-1250267597
