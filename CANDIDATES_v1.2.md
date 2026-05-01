# Builders Doctrine — v1.2 Candidates

**Status:** unratified. Items here are in flight for the next doctrine version. v1.1 tag remains canonical until v1.2 is locked.

**Authoring rule.** Anything in this file must survive at least one external test (an EMBA peer applying it, an SBIR reviewer reading it, a conformance audit) before being merged into the doctrine body. Candidates that fail their test get deleted, not promoted.

---

## Candidate 1 — Rename of Principle #1

**From:** "The code is the man"
**To:** "The code is the story"
**Decided:** 2026-05-01

### Why

The original line was personal to Hans — biographical, gendered, autobiographical. The Builders' Method is supposed to be a *method*, not a memoir. If the founding principle only works for Hans, the doctrine is autobiography wearing engineering clothes; if it works for anyone who picks up the method, it is a method.

"The code is the story" universalizes without losing the substantive claim:
- Anyone has a story.
- The method already requires writing the story down (STORY.md exists in every product).
- The line tells future adopters what to *do*, not just what is *true* — write your story, then compile it.
- Operationally accurate: this is already how Hans builds. The line just names what is already happening.

### What changed in the doctrine body

- Principle #1 heading and body rewritten to explicitly universalize: "Whoever builds a product encodes their story." Hans's specifics moved into the "Born in" trace where they belong; the principle itself is portable.
- A new paragraph "Why it universalizes" added under Principle #1 to make the portability claim explicit, not implied.
- Section III ("The Person Behind the Code") closing line updated: "The code is the story" replaces "the code is the man." The biographical sequence still belongs to Hans — but the line about it generalizes.

### What stays personal

The "Born in" traces under each principle still belong to Hans's biography. That is correct. The principles universalize; the biography stays Hans's because the *moat* is biographical and biographies do not generalize. A peer adopting the method gets their own "Born in" entries — they do not inherit Hans's.

---

## Candidate 2 — Portability principle

**Working name:** "Portability of the method, biography of the maker"
**Status:** captured here, not yet placed in the doctrine body. Awaiting v1.2 ratification + decision on placement (new section, or extension of Principle #1, or extension of Section VII Measurement).

### Statement

The method is portable. Any builder can adopt The Builders' Method and apply it to their own product. The moat is not portable. The biography that compiles into the product belongs to whoever is doing the building. When this method spreads, the framework is shared; the biographies are not. Each builder's products are agentic versions of *their* story, not Hans's.

This is the engineering claim that turns autobiography into a method. Without it, the doctrine reads as Hans's personal philosophy. With it, the doctrine becomes something other people can apply — and apply *honestly* (with their own moat), not by impersonating Hans's lineage.

### Why it matters

1. **Method vs memoir test.** If the method only works for Hans, it is not a method. The portability principle is the assertion that lets the rest of the doctrine generalize.
2. **Reproducibility test (Section VII).** A clean-room rebuild requires that the framework be portable. The portability principle is the philosophical version of what reproducibility tests operationally.
3. **AI Tradecraft brand.** The brand is a field, not a single practitioner's signature. The field has to be inheritable for the brand to be a category.
4. **SBIR / EMBA framing.** Reviewers ask "is this an artisanal one-off or a system?" The portability principle is the explicit answer.

### Open placement question

Three options for where this lives in v1.2:

1. **Extension of Principle #1.** Add a "Why it universalizes" paragraph (already done in this candidate's draft) and call that sufficient.
2. **New section II.0** between section I and the Founding Principles. Frame the doctrine as portable-by-construction before the principles begin.
3. **Extension of Section VII (Measurement Surface).** Tie it directly to the reproducibility protocol so the philosophical claim is anchored in the test that operationalizes it.

**My vote (for Hans's review):** Option 3. Reproducibility is already the operational test of portability; framing the philosophical claim as "what reproducibility tests" keeps it grounded in something that has to actually work in code, not just sound right in a pitch.

### External test before promoting

Pick one external case before merging this into the doctrine body:
- An EMBA peer (or other builder) reads the doctrine cold and applies it to their own product.
- They produce: their own STORY.md, their own commandments file, their own Guardian baseline.
- If their product reads as theirs (their biography in the prompts, their refusal list, their voice), the principle is validated.
- If their product reads like a Hans clone, the principle has failed and the framework is not portable.

Until at least one external case clears, this is a candidate, not a principle.

---

## Findings from synthetic portability test (2026-05-01)

A synthetic external test was run on 2026-05-01: apply the framework cold to a hypothetical builder with a deliberately-different biography (Maria Reyes-Chen, RN, MSN — fourteen years pediatric oncology, niece died of glioblastoma in 2019, building "Anchor" for parents of kids with cancer). The framework produced a coherent product clearly *hers* and not a Hans clone, validating the portability claim provisionally. The test also surfaced three real architectural items that need to be addressed in v1.2:

### Finding 1 — Principle #3 wellness-scoping is too narrow

**Current state.** v1.1 scopes "Designed to be needed less, not more" as wellness-specific, marking it `n/a` for operator tools (Operator, Custer) in the conformance matrix.

**The test surfaced.** Maria's product is neither wellness nor operator — it is a *caregiver tool*. The principle still applies but with a different success criterion: capability under crisis (parent advocating for their child more effectively over time), not autonomy after recovery (wellness frame).

**Implication for v1.2.** The current binary scoping (wellness | operator) misses caregiver-tools, advocacy-tools, education-tools, and several other categories. The principle is more universal than v1.1 currently states. Reframe the scoping note to: *"the dependency test applies to all products; the success criterion varies by product domain."* List the known shapes (wellness → autonomy after recovery; operator → capability at work; caregiver → capability under crisis) and accept that future builders will surface new shapes.

### Finding 2 — Principle #7 should be renamed

**Current state.** Principle #7 is "Stoic commandments." Stoicism is the framework that survived your collapse and rebuilt you. It is the right framework for *your* products.

**The test surfaced.** Maria's product needs a commandments file and a Guardian audit, but Stoicism is not her ethical floor. Her floor is palliative-care ethics + trauma-informed care. The form (commandments file + Guardian audit + drift detection) is portable; the framework name (Stoic) is not.

**Implication for v1.2.** Rename Principle #7 to something framework-agnostic — candidates: "Commandments rooted in the builder's ethical framework," "Ethical commandments and drift audit," "Doctrine commandments." The Stoic specifics belong in TOP's product-level commandments file, not in the meta-doctrine. The principle is "have a commandments file and audit drift against it" — the contents come from whoever's biography is doing the building.

### Finding 3 — "Crisis" is product-defined; the floor pattern is universal

**Current state.** Principle #11 is "Crisis floors above features." In v1.1 the implicit example is TOP's suicide-prevention floor (Veterans Crisis Line 988, hard-coded above every feature, ungated, A/B-test-forbidden).

**The test surfaced.** Maria's crisis is not suicidal ideation — it is acute oncologic emergency (child showing emergency symptoms, immediate care-team or ER routing). Custer's crisis is different again (election-day field emergency, candidate threat). Operator's crisis surface is unclear.

**Implication for v1.2.** The principle should explicitly state two things: (a) the *pattern* of a crisis floor (hard-coded above features, ungated, A/B-test-forbidden) is universal; (b) *what counts as crisis* is product- and builder-defined and must be named explicitly per product. Without this distinction, a future builder will assume your suicide-floor is *the* crisis floor instead of *a* crisis floor.

### What the test did not cover

These findings are from a synthetic test only. A real external test (an actual EMBA peer or other builder applying the framework cold) is still required before Candidate 2 (portability principle) can be ratified. Synthetic tests miss things real builders surface — friction, resistance, moments where the framework feels alien, biographical detail that does not slot cleanly. Treat these three findings as a pre-test checklist of items to fix; expect the real external test to surface more.

---

## Items deferred to v1.2 from v1.1 stress test (already tracked elsewhere)

- TOP Guardian regex bug (`f?"""` pattern) — fix during Anatomy v2 Session 1
- TOP missing `lingo` specialist file resolution
- Operator Guardian API standardization to match TOP / Custer surface
- Approval-queue API standardization across all three products

These are surfaced here for completeness but lived in `STRESS_TEST_v1.0.md` and `ANATOMY_V2_PLAN.md` first.

---

## Ratification

v1.2 is ratified when:
1. Candidate 1 (rename) is propagated through every reference in this repo + cross-references in CLAUDE.md / memory (done 2026-05-01).
2. Candidate 2 (portability principle) clears at least one external test.
3. The version header in `THE_BUILDERS_DOCTRINE.md` is bumped from `v1.2-draft` to `v1.2` and the repo is tagged.

Until all three, v1.1 remains the canonical version. v1.2-draft is in flight.
