# Stress Test — THE_BUILDERS_DOCTRINE v1.0

**Audited:** 2026-04-30
**Auditor:** Claude (via Hans)
**Doctrine version:** v1.0 — `hansprahl/the-builders-doctrine` at tag `v1.0`
**Products audited:** TOP (`local-mcp`), Operator (`operator`), Custer (`custer-mcp`)
**Products deferred:** Rubicon — frozen behind tag `rubicon-cohort-v1`, audit on resume

---

## Executive summary

Doctrine v1.0 survives contact with the products. Of 33 cells (11 principles × 3 products), 24 conform fully, 5 are partial, and 4 are not-applicable for product-specific reasons. Zero outright violations.

The framework is real, not aspirational. The five partial cells identify concrete v1.1 work — none are existential. The largest single gap is Custer's missing CONFIDENCE/REASONING coverage (1 of 7 specialists carry the block), which is mechanical to fix and does not require doctrine revision.

The four "not applicable" cells are honest scope acknowledgments (wellness-specific principles do not apply to business or campaign tools) rather than gaps. v1.1 should consider whether the doctrine should explicitly mark which principles are universal vs. wellness-specific, or whether the current implicit treatment is fine.

---

## Methodology

**Documentary audit, not runtime audit.** This pass reads code, configuration, and commit history. It does not test deployed behavior on Railway, in Telegram, or against live users.

**Per-cell evidence required.** Conformance is asserted only where a code mechanism is named (file + function or pattern). Where a principle is honored *in practice but not by mechanism*, the cell is marked partial.

**Skipped products.** Rubicon is frozen behind a tag and was not audited. Per the doctrine's authority section, frozen products are audited on resume, not maintained against the live doctrine.

**Honest limits of this audit:**
- No runtime testing — deployed behavior on Railway / Telegram not validated
- No user-side validation — pilots not surveyed, dependency-test perception not tested
- No reproducibility protocol execution — clone-restore-rebuild deferred to v1.1 propagation cycle
- No live Guardian runs against full specialist sets — would have produced fresher score baselines but with cost; deferred

---

## Conformance matrix

Legend: ✓ = conforms with named mechanism; ⚠ = partial (honored in spirit, gap in mechanism or coverage); ✗ = violates; n/a = not applicable to this product

| # | Principle | TOP | Operator | Custer |
|---|---|---|---|---|
| 1 | The code is the man | ✓ | ✓ | ✓ |
| 2 | The moat is the memory | ✓ | ✓ | ✓ |
| 3 | Designed to be needed less | ✓ | n/a (wellness-specific) | n/a (wellness-specific) |
| 4 | Chain of command over autonomous AI | ✓ | ✓ | ✓ |
| 5 | Data sovereignty | ✓ | ⚠ | ✓ |
| 6 | Truth as architecture | ✓ | ✓ | ⚠ |
| 7 | Stoic commandments | ✓ | ✓ (adapted) | ✓ |
| 8 | The Refusal | ⚠ | ⚠ | ⚠ |
| 9 | AI as co-author | ✓ (27/30) | ✓ (30/30) | ✓ (29/30) |
| 10 | Named specialists | ✓ (8) | ✓ (7) | ✓ (7) |
| 11 | Crisis floors above features | ✓ | n/a (business agent) | n/a (campaign tool) |

**Totals:** 24 ✓, 5 ⚠, 4 n/a, 0 ✗

---

## Per-cell reasoning — partials and n/a

### Principle 5 — Data sovereignty: Operator ⚠

**Honored in spirit.** Operator's data lives locally on Hans's machine and Railway deployment. `.gitignore` blocks credentials. Gitleaks pre-commit (`.git/hooks/pre-commit`) runs on every commit. No third-party processors handle sensitive data.

**Gap.** Operator is single-user by design — Hans only. There is no `tools/user_context.py` with `LookupError`-on-unset enforcement, no per-user data paths under `data/users/{user_id}/`, no multi-tenant isolation infrastructure. The principle's structural enforcement (against silent fallbacks) does not exist because it has not been needed.

**Implication.** If Operator is ever commercialized to multi-tenant SaaS, the multi-user infrastructure has to be built before the second tenant onboards. Custer already has this layer (built in this session). Operator does not.

**Recommended v1.1.** Either (a) port the user_context pattern from Custer to Operator preemptively (cheap insurance), or (b) explicitly note in Operator's CLAUDE.md that multi-tenant readiness is deferred until commercial pursuit.

### Principle 6 — Truth as architecture: Custer ⚠

**Honored in part.** Custer's Prompt Guardian (shipped this session) audits prompts against five commandments with rollback history. `agents/intelligence.py` includes an explicit confidence instruction in its LLM call.

**Gap.** Six of seven Custer specialists (`delegate_whip`, `voter_universe`, `messaging`, `field_ops`, `digital_blast`, `strategy_timeline`) do not include a CONFIDENCE/REASONING block in their system prompts. This means:
- Specialist responses are not parsed for confidence
- AAR calibration cannot run (no confidence data to calibrate against)
- The audit trail required by the principle is incomplete

TOP solves this by injecting `CONFIDENCE_INSTRUCTION` from `tools/doctrine_confidence.py` via `resolve_prompt()` for every specialist at runtime — single source, applied universally. Custer's `resolve_prompt()` does not yet inject the equivalent.

**Recommended v1.1.** Port TOP's pattern: create `custer-mcp/tools/doctrine_confidence.py` with a CONFIDENCE_INSTRUCTION block, modify `tools/prompt_guardian.py:resolve_prompt()` to append it, and verify all seven specialists' responses now include a confidence block. Estimated 30–60 lines.

### Principle 8 — The Refusal: all three ⚠

**Honored in spirit, not by mechanism.** None of the three products contain features matching the refusal list:
- No engagement-maximization patterns (no streaks, no variable rewards, no dark patterns)
- No surveillance products (no third-party data sales, no consent-by-dark-pattern)
- No parasocial replacement features (TOP's wellness specialist is forbidden cheerleading by commandment 3)

The Refusal is therefore conformed-by-character-of-builder, not by code-level enforcement. There is no:
- Commandment scoring against refusal categories
- Scope-lock checklist requiring explicit refusal audit before new features ship
- Decision log of features considered and refused

**Why this matters.** A future product proposal that quietly contains a refused pattern (e.g., a "streak" added to TOP's habit tracking, framed as motivation) might pass commandment review because the existing commandments don't explicitly name the refusal categories. The refusal exists in Hans's head, not in the audit surface.

**Recommended v1.1.** Add a `REFUSAL_AUDIT.md` checklist to each product repo. Pre-feature-ship checkpoint: every new feature confirmed against each refusal item with explicit "no, this does not violate" rationale. Logged to git. Becomes the audit trail the principle currently lacks.

### Principle 9 — AI as co-author: all three ✓ (with note)

**TOP 27/30, Operator 30/30, Custer 29/30** in the last 30 commits. All above 90%. Convention is real.

**Note on the missing 1–3 commits per repo.** Likely manual non-AI commits Hans made directly. Not a violation — the principle says AI-assisted commits must include the line, not that all commits must be AI-assisted. v1.1 could clarify this in the doctrine text if reviewers find it ambiguous.

### Principle 3 — Designed to be needed less: Operator + Custer n/a

**Why n/a.** Principle 3 is wellness-specific. It applies to products where the end-user is the human seeking change, and the dependency test is whether the product builds resilience or builds reliance. TOP's user is a veteran working on wellness; the test applies directly.

Operator's user is Hans operating his business. Custer's user is Hans running a campaign. In both cases, the user is *the operator using a tool to do work*, not *a user seeking personal change*. The dependency test is structurally different — does the tool make Hans more capable as an operator, not whether it makes him need the tool more.

**Doctrine question for v1.1.** Should Principle 3 be explicitly scoped to wellness/personal-change products in the doctrine text? Or should it remain implicit and the audit honor that scope? Current treatment is implicit; Custer's commandments do not include a "scaffold not crutch" equivalent because it would not fit. The doctrine reads as if it should — clarification recommended.

### Principle 11 — Crisis floors above features: Operator + Custer n/a

**Why n/a.** Principle 11 applies to products that can encounter a vulnerable user in crisis. TOP can — veterans with PTSD, suicidal ideation. Veterans Crisis Line (988, press 1) is hard-coded across `agents/orchestrator.py`, `agents/telegram_bot.py`, `tools/onboarding.py`.

Operator is a business agent — its surface is grants, marketing, finance. No crisis path. Custer is a campaign tool — its surface is voters, delegates, field operations. No crisis path either.

The principle is architectural: *if* the product can encounter a vulnerable user, the floor is mandatory. The current "n/a" assignments are honest scope; they should be re-audited if either product expands its surface to touch vulnerable users.

---

## Identified gaps for v1.1

Five concrete pieces of work, prioritized:

| Priority | Gap | Product(s) | Estimated effort |
|---|---|---|---|
| **High** | Port CONFIDENCE/REASONING injection to Custer specialists | Custer | 30–60 lines, 1 session |
| **Medium** | Add REFUSAL_AUDIT.md checklist to each product repo | TOP, Operator, Custer | 15–30 lines per repo, parallel |
| **Medium** | Clarify Principle 3 scope (wellness-specific vs. universal) in doctrine text | Doctrine itself | 1–2 paragraph edit |
| **Low** | Decide on Operator multi-tenant readiness — port user_context now or defer | Operator | 100–200 lines if porting; 1 paragraph if deferring |
| **Low** | Update Principle 9 doctrine text to clarify AI-assisted-only scope | Doctrine itself | 1 sentence edit |

---

## Doctrine-side observations

Three doctrine-level findings emerged from the audit. None require v1.1 commits *to the doctrine* unless Hans wants them:

1. **Principle 3 (Designed to be needed less) is wellness-scoped in practice.** Custer and Operator do not enforce it because it does not fit. The doctrine reads as universal but applies only to wellness/personal-change products. Either explicitly scope it in the text, or accept implicit scope.

2. **Principle 11 (Crisis floors) is conditionally universal — applies *if* the product can encounter a vulnerable user.** This is correctly stated in the doctrine ("If a product cannot encounter a vulnerable user, this principle is moot"). Audit confirms this conditional reading is the right one.

3. **Principle 8 (The Refusal) lacks mechanism in every product.** This is a doctrine-text strength (the principle exists) but a doctrine-implementation gap (no enforcement code exists). Adding REFUSAL_AUDIT.md per product closes the gap without changing doctrine text.

---

## What this audit cannot tell you

Honest limits, in case a reviewer asks:

- **Whether the products work for users.** Pilots have not been surveyed. The dependency-test perception in TOP is unmeasured.
- **Whether the deployed environments match the repo state.** Railway behavior, Telegram bot behavior, and live database state are not verified against the audit findings.
- **Whether the reproducibility protocol actually achieves <5% variance.** First clean-room execution is part of v1.1 work, not this stress test.
- **Whether the Refusal list is complete.** Hans confirmed three items as load-bearing (engagement-max, surveillance, parasocial). Other categories may exist that he has not yet articulated.
- **Whether biographical-input correlation with hallucination rate is real.** Asserted by the doctrine, not measured. Listed in the honest gap section of THE_BUILDERS_DOCTRINE.md Section VII.C.

---

## Recommendation

**Doctrine v1.0 holds.** No principle requires retraction. Five mechanical gaps identified for v1.1. Three doctrine-text clarifications recommended but not required.

**Suggested v1.1 sequence:**

1. Custer CONFIDENCE/REASONING port (highest signal-to-effort ratio)
2. REFUSAL_AUDIT.md checklist propagation across three products (medium signal, low effort)
3. Doctrine text clarifications on Principle 3 scope and Principle 9 AI-assisted-only (1 commit to doctrine repo)
4. Operator multi-tenant decision (defer or port)

**Estimated v1.1 cost:** one focused session, $1–$3 in API costs, no architectural changes.

---

**Audit complete.** Doctrine survives stress test with five identified gaps and three clarifications. Ready for propagation cycle.
