# PR/FAQ — [PRODUCT OR FEATURE NAME]

**Version:** v[N] [DRAFT | FINAL]
**Author:** [name]
**Date:** [YYYY-MM-DD]
**Build-or-kill review:** [scheduled date | not yet scheduled]
**Working Backwards doctrine:** see `~/Projects/the-builders-doctrine/WORKING_BACKWARDS.md`

> **Discipline before writing:** confirm the proposed product/feature passes the Refusal List (Principle #8) and the Crisis Floors check (Principle #11) if it touches a vulnerable user. If it violates a refusal, stop. Don't write.
>
> **Length target:** 6 pages total (~3 min/page reading time). If it doesn't fit, the scope is too broad — narrow before writing more.
>
> **Voice:** Press Release in customer language only, no internal jargon. FAQs are direct, blunt, no hedging.

---

## Part 1 — Press Release (~1 page)

### Headline

[One line. Customer-readable. State the news.]

### Subheading

[Audience + benefit, one line.]

### Summary

[One paragraph. The news, in plain language. What the product is, who it's for, why it matters now.]

### Problem

[Concrete scenario, not abstract pain point. Use a specific customer in a specific situation with specific numbers.
Example pattern: "A [size] [vertical] company with [specific volume metric] needs to [specific outcome] but [specific obstacle blocks them]. Today they [current workaround] which costs [specific cost in dollars or time]."]

### Solution

[How the product solves the problem. Plain language. Walk the customer through what happens.
Example pattern: "[Product name] does [specific action]. The customer provides [input], the product produces [output], and [downstream consumer] does [the rest]. Time: [duration]. Cost: [price]."]

### Quote from [builder / company leader]

> "[One or two sentences. Why this matters from the builder's perspective. Plain, not hyped.]"
>
> — [Name, role]

### Quote from a hypothetical customer

> "[One or two sentences. The customer's experience, in their own voice. Specific outcome, not generic praise.]"
>
> — [Hypothetical customer name, role, company type]

### Call to action

[What the customer does next. Specific URL, contact path, or signup mechanism.]

---

## Part 2 — External FAQ (~1–2 pages)

### What is [product]?

[Plain-language answer.]

### Who is it for?

[Specific customer archetype. Vertical, size, role.]

### What problem does it solve?

[Plain-language answer. Reference the press release problem paragraph but expand on edge cases.]

### How does it work?

[Step by step, customer-facing. Don't describe internal architecture.]

### What does it cost?

[Pricing model. Be specific. If pricing isn't final, state the model and the range under consideration.]

### How is it different from [closest competitor]?

[Direct comparison. Name the competitor. State the differentiation honestly. Don't claim the competitor is bad — claim the difference.]

### When can I use it?

[Specific timeline. Beta, GA, waitlist, etc.]

### What's the catch?

[Honest limitations. What it doesn't do. What it requires the customer to provide. This is a trust-building question; answer it plainly.]

---

## Part 3 — Internal FAQ (~2–3 pages)

### Why are we building this?

[The strategic rationale. Reference the demand evidence — frequency, segment, channel. Tie to the broader portfolio thesis.]

### Why now?

[What's changed in the market, the platform layer, the customer's posture that makes this the right time. Why not 12 months ago? Why not 12 months from now?]

### Why are we the ones to build it?

[The biographical-moat answer. What does the builder bring that nobody else does? Don't say "we have a strong team" — that's table stakes. Name the specific edge.]

### What does the moat look like at scale?

[Project to the 10-year horizon (Principle #13). What compounds? What becomes harder to copy as the product matures? If the answer is "nothing structural — it's just a feature," reconsider the build.]

### What are the unit economics?

[Banks-style analysis. CAC, LTV, payback period. Margin structure. If pre-revenue, state assumptions explicitly and confidence level.]

### What's the technical risk?

[Halsey-style assessment. What's the hardest engineering problem? What's the failure mode? What's the buy-vs-build call on each major component?]

### What's the regulatory / compliance risk?

[Marshall-style assessment if applicable. What regulations apply? What does counsel need to review before launch? What's the patent/IP posture?]

### What happens if we fail?

[Honest answer. What's the cost of failure — capital, time, reputation, opportunity cost? Is failure recoverable?]

### What's the kill criterion?

[Pre-registered. What metric or signal would tell us to kill this product? Don't write "if it doesn't work" — write the specific condition: "if CAC > $X by day N" or "if conversion < Y% by quarter Z."]

### Who is harmed by this product if it succeeds?

[The refusal-list adjacent question. Does success of this product harm anyone? Users, communities, the labor market, the founder's portfolio coherence? If yes, is the harm acceptable? If no, write that down explicitly.]

### Does this pass the Refusal List check?

[Reference `kit/templates/REFUSAL_LIST.md` and the product's own commandments. State the result: PASS or FAIL with reason.]

### Does this pass the Dependency Test? (wellness-shaped products only)

[Reference Principle #3. Does this make the user more capable without the tool, or more reliant on it? PASS or FAIL with reason. Wellness products that fail this test do not ship.]

### Does this pass the Crisis Floors check? (any product touching vulnerable users)

[Reference Principle #11. Are crisis-detection floors hard-coded above the feature? PASS or FAIL with reason.]

### What's the chain-of-command posture?

[Reference Principle #4. Which actions are Type 1 (irreversible, founder-approval-gated)? Which are Type 2 (reversible, agent-executable within scope)? Name the gate explicitly.]

### How does this pass the Working Backwards review?

[Self-audit. Did the writing process change the scope? Did the FAQ surface a blocker that the press release glossed over? What was modified between v0 and the current draft?]

---

## Product-specific FAQ additions

Add product-specific FAQ questions below based on the product family:

**TOP (wellness):**
- Does the voice surface honor the "rendering layer, not personality" rule?
- Is the Stoic register enforced at the Guardian audit layer?

**Custer (campaign):**
- Does this respect voter-PII isolation under CRS 1-2-305?
- Does outreach route through the approval queue?

**Operator (autonomous business agent):**
- Which specialist owns this feature?
- Does the approval gate cover every irreversible action this feature can take?

**RPR (engineering brand):**
- Does any imagery / copy use outdoor-lifestyle stock photography (refusal)?
- Is the texture attribution path documented?

---

## Decision record

**Build-or-kill review date:** [YYYY-MM-DD]
**Decision:** [BUILD | INVESTIGATE FURTHER | KILL]
**If INVESTIGATE FURTHER:** what evidence would resolve the gating question?
**If BUILD:** narrow first slice scoped to:
**If KILL:** rationale recorded for future reference:

---

*This template lives at `~/Projects/the-builders-doctrine/kit/templates/PR_FAQ_TEMPLATE.md`. Each portfolio product copies this skeleton into `~/Projects/<product>/working_backwards/<feature>_v<n>.md` and adapts it. The template evolves — update the upstream when product-shaped patterns emerge.*
