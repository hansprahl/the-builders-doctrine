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

The press release is the customer-facing launch announcement. Customer language only, no internal jargon, ~1 page. If you cannot write the press release plainly, the product is not yet specified clearly enough.

<!-- KIT:FIELD name="press_release" required="true" min_words="200" -->
[Author the full press release with the following structure:

**Headline** — one line, customer-readable, states the news.

**Subheading** — audience + benefit, one line.

**Summary** — one paragraph. What the product is, who it's for, why it matters now.

**Problem** — concrete scenario, not abstract pain point. Specific customer in a specific situation with specific numbers. Pattern: "A [size] [vertical] company with [specific volume metric] needs to [specific outcome] but [specific obstacle blocks them]. Today they [current workaround] which costs [specific cost in dollars or time]."

**Solution** — how the product solves the problem in plain language. Walk the customer through what happens. Pattern: "[Product name] does [specific action]. Customer provides [input], product produces [output], [downstream consumer] does [the rest]. Time: [duration]. Cost: [price]."

**Quote from builder/company leader** — one or two sentences in their voice, plain not hyped.

**Quote from hypothetical customer** — one or two sentences in customer voice, specific outcome not generic praise.

**Call to action** — specific URL, contact path, or signup mechanism.

If the press release doesn't fit on one page, the scope is too broad — narrow before continuing.]
<!-- KIT:END -->

---

## Part 2 — External FAQ (~1–2 pages)

The eight questions a customer asks before buying. Answer in customer language, plain, no hedging.

<!-- KIT:FIELD name="external_faq" required="true" min_words="200" -->
[Answer all eight questions:

1. **What is [product]?** — plain-language definition.
2. **Who is it for?** — specific customer archetype: vertical, size, role.
3. **What problem does it solve?** — expand on edge cases beyond the headline problem.
4. **How does it work?** — step by step, customer-facing. Don't describe internal architecture.
5. **What does it cost?** — pricing model, specific. If not final, state model and range under consideration.
6. **How is it different from [closest competitor]?** — name the competitor; state the difference honestly; don't claim the competitor is bad.
7. **When can I use it?** — specific timeline: beta, GA, waitlist.
8. **What's the catch?** — honest limitations. What it doesn't do. What the customer must provide. Trust-building question; answer plainly.]
<!-- KIT:END -->

---

## Part 3 — Internal FAQ (~2–3 pages)

### Why are we building this?

<!-- KIT:FIELD name="why_build" required="true" min_words="60" -->
[The strategic rationale. Reference the demand evidence — frequency, segment, channel. Tie to the broader portfolio thesis. If the answer is "the founder thinks it's interesting," reconsider the build.]
<!-- KIT:END -->

### Why now?

<!-- KIT:FIELD name="why_now" required="true" min_words="40" -->
[What changed in the market, the platform layer, or the customer's posture that makes this the right time. Why not 12 months ago? Why not 12 months from now? If the timing argument doesn't exist, this is a perpetual idea — kill or table.]
<!-- KIT:END -->

### Why are we the ones to build it?

<!-- KIT:FIELD name="why_us" required="true" min_words="60" -->
[The biographical-moat answer. What does the builder bring that nobody else does? Don't say "we have a strong team" — that's table stakes. Name the specific edge: lived experience, regulatory access, technical depth, ground-truth corpus. Trace to STORY.md.]
<!-- KIT:END -->

### What does the moat look like at scale?

<!-- KIT:FIELD name="long_horizon_moat" required="true" min_words="60" -->
[Project to the 10-year horizon per Principle #13 (The Long Horizon). What compounds? What becomes harder to copy as the product matures? Memory? Ground-truth corpus? Network effects? Regulatory position? If the answer is "nothing structural — it's just a feature," reconsider the build. Working Backwards' load-bearing test: the internal FAQ defends the product on the ten-year horizon, not the launch quarter.]
<!-- KIT:END -->

### What are the unit economics?

<!-- KIT:FIELD name="unit_economics" required="true" min_words="40" -->
[CAC, LTV, payback period. Margin structure. If pre-revenue, state assumptions explicitly with confidence level (HIGH/MED/LOW per the CONFIDENCE doctrine). Banks-style analysis if Operator's S5/Finance specialist exists.]
<!-- KIT:END -->

### What's the technical risk?

<!-- KIT:FIELD name="technical_risk" required="true" min_words="40" -->
[Halsey-style assessment. The hardest engineering problem. The failure mode. The buy-vs-build call on each major component. Where existing chassis primitives can be lifted (Crisis Floor, Approval Queue, etc.) and where new code is unavoidable.]
<!-- KIT:END -->

### What's the regulatory / compliance risk?

<!-- KIT:FIELD name="regulatory_risk" required="conditional_on:hard_floor_check" min_words="40" -->
[Marshall-style assessment if applicable. Regulations that apply (HIPAA, voter-file CRS, ITAR, GDPR, fair-lending, etc.). What counsel needs to review before launch. Patent/IP posture. If no regulated surface is touched, mark `na_with_reasoning` and explain why.]
<!-- KIT:END -->

### What happens if we fail?

<!-- KIT:FIELD name="failure_cost" required="true" min_words="40" -->
[Honest answer. Cost of failure — capital, time, reputation, opportunity cost. Is failure recoverable? Is failure visible to others (a customer commitment, a public bet) or contained (an internal exploration)?]
<!-- KIT:END -->

### What's the kill criterion?

<!-- KIT:FIELD name="kill_criterion" required="true" min_words="30" -->
[Pre-registered. The specific metric or signal that tells us to kill this product. Don't write "if it doesn't work" — write the specific condition: "if CAC > $X by day N" or "if conversion < Y% by quarter Z" or "if zero qualified intros materialize from Brad's channel in 60 days." If the kill criterion is not measurable, the build cannot be stopped honestly.]
<!-- KIT:END -->

### Who is harmed by this product if it succeeds?

<!-- KIT:FIELD name="harm_analysis" required="true" min_words="40" -->
[The refusal-list adjacent question. Does success of this product harm anyone? Users, communities, the labor market, the founder's portfolio coherence? If yes, is the harm acceptable? If no, write that down explicitly. Refusal-list candidates often surface here that didn't appear in REFUSAL_LIST.md.]
<!-- KIT:END -->

### Does this pass the Refusal List check?

<!-- KIT:FIELD name="refusal_list_check" required="true" min_words="20" -->
[Reference `kit/templates/REFUSAL_LIST.md` and the product's own commandments. State PASS or FAIL with reason. A FAIL stops the build; do not continue writing the PR/FAQ for a feature that fails the refusal check.]
<!-- KIT:END -->

### Does this pass the Dependency Test? (wellness-shaped products only)

<!-- KIT:FIELD name="dependency_test_check" required="conditional_on:hard_floor_check" min_words="20" -->
[Reference Principle #3. Does this make the user more capable without the tool, or more reliant on it? PASS or FAIL with reason. Wellness products that fail this test do not ship. For operator-tool products (Operator, Custer, Rubicon), mark `na_with_reasoning` per the scope-inversion rule.]
<!-- KIT:END -->

### Does this pass the Crisis Floors check? (any product touching vulnerable users)

<!-- KIT:FIELD name="crisis_floor_check" required="conditional_on:hard_floor_check" min_words="20" -->
[Reference Principle #11. Crisis-detection floors must be hard-coded above the feature. State PASS or FAIL with the specific floor implementation cited. For products that cannot encounter a vulnerable user, mark `na_with_reasoning` explaining why.]
<!-- KIT:END -->

### What's the chain-of-command posture?

<!-- KIT:FIELD name="chain_of_command_posture" required="true" min_words="40" -->
[Reference Principle #4. Which actions are Type 1 (irreversible, founder-approval-gated)? Which are Type 2 (reversible, agent-executable within scope)? Name the gate explicitly. For MCA-shaped products, also state which authority tier resolves each action class per the gradient routing table (NCO for in-unit, PL for in-mission, Hans for world-boundary).]
<!-- KIT:END -->

### How does this pass the Working Backwards review?

<!-- KIT:FIELD name="working_backwards_self_audit" required="true" min_words="40" -->
[Self-audit. Did the writing process change the scope? Did the FAQ surface a blocker that the press release glossed over? What was modified between v0 and the current draft? If nothing changed — if the press release came out clean on the first pass — the writing didn't do its job. Working Backwards' value is in what it forces you to find.]
<!-- KIT:END -->

---

## Product-specific FAQ additions

Add product-specific FAQ questions below based on the product family. These are not scored by the Kit; they're prompts to remind the builder of their product's particular hard floors.

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

<!-- KIT:FIELD name="decision_record" required="true" min_words="30" -->
[At build-or-kill review date, record:

**Build-or-kill review date:** [YYYY-MM-DD]
**Decision:** [BUILD | INVESTIGATE FURTHER | KILL]
**If INVESTIGATE FURTHER:** what evidence would resolve the gating question?
**If BUILD:** narrow first slice scoped to.
**If KILL:** rationale recorded for future reference.

Decisions must be pre-committed and dated. A PR/FAQ without a decision record is a draft, not a doctrine artifact.]
<!-- KIT:END -->

---

## Hard-floor check (gates conditional fields)

This field gates whether the conditional checks above (regulatory, crisis floor, dependency test) apply.

<!-- KIT:FIELD name="hard_floor_check" required="true" min_words="30" -->
[State which hard floors this product/feature touches: vulnerable users (crisis floor applies), regulated surface (regulatory_risk applies), wellness population (dependency test applies), multi-tenant data (per-user isolation applies). For each: "applies" or "n/a with reason." This field is what the conditional KIT:FIELD blocks above gate on.]
<!-- KIT:END -->

---

*This template lives at `~/Projects/the-builders-doctrine/kit/templates/PR_FAQ_TEMPLATE.md`. Each portfolio product copies this skeleton into `~/Projects/<product>/working_backwards/<feature>_v<n>.md` and adapts it. The template evolves — update the upstream when product-shaped patterns emerge.*

*Two modes of use: (1) **bootstrap mode** — a builder's first PR/FAQ for their product, authored via `coverage.py --interview` driving `pr_faq_interview.yaml` after STORY and REFUSAL_LIST are populated; (2) **per-feature mode** — a fresh copy authored every time scope is committed, before code is written. Both modes score against the same KIT:FIELD blocks.*
