# Artifact Audit — 2026-05-01

**Author's portfolio scored against [`THE_BUILDERS_METHOD.md`](THE_BUILDERS_METHOD.md) Section IV ("Required Artifacts").**

## Why this audit exists

The Method requires eight artifacts per product (Section IV). It also requires a conformance audit (Section IX) that scores each product against the eleven principles. Until 2026-05-01, neither the artifact set nor the conformance scoring had been written down for the author's own portfolio. The Method document referenced required artifacts that several products did not actually contain.

A reviewer surfaced this honestly: "Required files list good. Ensure every one exists in current repos or mark 'stub for v1.0'. Trust table must link real file paths, not aspirational. If STORY.md or CRISIS.md missing in any product, note it. No theater."

This audit is the answer. It scores the author's four-product portfolio against Section IV's required-artifact set, names every gap, and assigns a remediation plan with dates. It ships as part of Method v0.9 Provisional — not because v0.9 has nothing to fix, but because shipping the audit *with* the framework is more honest than shipping the framework alone.

This audit does not satisfy the v1.0 precondition for third-party scoring (Section II Limit #2). It is the author's self-audit. An outside reader scoring this same matrix is the v1.0 gate.

## The portfolio

| Product | Path | What it is |
|---|---|---|
| TOP (Thriving On Purpose) | `/Users/hansprahl/Projects/local-mcp/` | Veteran wellness AI. Deployed on Railway, Telegram primary surface. |
| Operator | `/Users/hansprahl/Projects/operator/` | Autonomous business agent. MDMP planning, seven named specialists. |
| Custer | `/Users/hansprahl/Projects/custer-mcp/` | Campaign platform for Taylor LoPresti 2026 (Custer County Commissioner, CO). |
| Rubicon | `/Users/hansprahl/Projects/rubicon/` | EMBA cohort digital twin platform. Paused 2026-04-13 behind tag `rubicon-cohort-v1`. |

## Coverage matrix

Legend:
- **✓** — exists as a dedicated file with real content
- **⚠** — inline-only (embedded inside CLAUDE.md or another file, not extracted) OR exists but thin
- **✗** — missing entirely
- **n/a** — not applicable, but the n/a must be declared explicitly in the product's CLAUDE.md or SECURITY.md

| # | Required artifact | TOP | Operator | Custer | Rubicon |
|---|---|---|---|---|---|
| 1 | `STORY.md` | ✓ (22,191 words) | ✓ (3,204) | ✗ missing | ⚠ thin (573) |
| 2 | Commandments file | ⚠ inline in CLAUDE.md | ⚠ inline | ⚠ inline | ⚠ inline |
| 3 | Refusal list | ⚠ audit-only (REFUSAL_AUDIT.md) | ⚠ audit-only | ⚠ audit-only | ✗ missing |
| 4 | `SPECIALIST_TEMPLATE.md` | ✓ (487) | ✗ | ✗ | ✗ |
| 5 | Crisis trigger document | ⚠ inline-only | ⚠ no n/a declared | ⚠ inline-only | ⚠ no n/a declared |
| 6 | `AGENT_DOCTRINE.md` | ✓ (5,165) | ✗ | ✗ | ✗ |
| 7 | `PROMPT_DOCTRINE.md` | ✗ (referenced, file absent) | ✗ | ✓ (1,978) | ✗ |
| 8 | `SECURITY.md` | ✓ (1,371) | ✓ (829) | ✓ (882) | ✓ (798) |

**Coverage scores (✓ count over 8):** TOP 5 / Operator 2 / Custer 2 / Rubicon 1. Mean across portfolio: 2.5/8 (31%).

## Per-product findings

### TOP — 5/8 (highest coverage; flagship)

**Strengths.** STORY.md is substantive (22k+ words, dated chapters, founder narrative). AGENT_DOCTRINE.md exists as a real chassis spec (5k+ words, eleven components named and pointed at implementations). SPECIALIST_TEMPLATE.md exists. SECURITY.md is complete and current. NORTHSTAR.md provides product purpose grounding.

**Gaps.**

- **Commandments file (⚠).** Stoic commandments live inline in CLAUDE.md ("Stoic philosophy" + "Founding ethics" sections + "Truth and intellectual honesty"). They are real and used, but cannot be cleanly Guardian-audited as long as they are mixed with build instructions in CLAUDE.md. **Remediation:** extract to `COMMANDMENTS.md`. Estimated effort: 1 hour.
- **Refusal list (⚠).** REFUSAL_AUDIT.md is the audit log, not the refusal list. The list itself is upstream in `THE_BUILDERS_DOCTRINE.md II.8`. This is a real design pattern (shared upstream list, per-product audit log) — but the Method document does not acknowledge it. **Remediation:** either acknowledge the pattern in the Method (Section IV update) or extract a per-product `REFUSAL_LIST.md` derived from the upstream list. The first option is cheaper and probably more honest.
- **Crisis trigger document (⚠).** TOP's crisis pattern is real (Veterans Crisis Line 988 press 1 hard-coded above every feature). But the trigger conditions (suicidal ideation, acute psychiatric crisis) are not in a dedicated `CRISIS_TRIGGERS.md`. They live inline in CLAUDE.md and in the wellness specialist's prompt. **Remediation:** extract to `CRISIS_TRIGGERS.md`. Estimated effort: 1 hour.
- **PROMPT_DOCTRINE.md (✗).** TOP's own CLAUDE.md says "Prompt Doctrine — universal structural rules for every prompt across every product... Lives in each product's PROMPT_DOCTRINE.md." The file does not exist in TOP. The reference is aspirational. **Remediation:** either author the file (Custer's version is the closest existing template) or update TOP's CLAUDE.md to reference Custer's as the canonical version pending consolidation. Estimated effort: 4–6 hours (real authoring) or 5 minutes (reference update).

### Operator — 2/8

**Strengths.** STORY.md exists (3,204 words, real). SECURITY.md exists. Approval Queue language in CLAUDE.md is concrete and enforced (Principle 4 has a real mechanism). REFUSAL_AUDIT.md exists.

**Gaps.**

- **Commandments file (⚠).** Inline in CLAUDE.md "North Star" section. Same extraction work as TOP. **Remediation:** extract to `COMMANDMENTS.md`. 1 hour.
- **SPECIALIST_TEMPLATE.md (✗).** Operator has seven named specialists — but the build sheet for adding a new one is not documented. New specialists are likely being authored ad hoc against precedent rather than against a checklist. **Remediation:** copy TOP's template, adapt to Operator's specialist patterns. 2 hours.
- **AGENT_DOCTRINE.md (✗).** Operator runs an agentic chassis but does not have it documented. The Method says this artifact is required. **Remediation:** either author Operator's own AGENT_DOCTRINE.md or have CLAUDE.md reference TOP's as the canonical chassis spec the product implements. The second option is a stop-gap; the first is the real fix. 4–8 hours for the real fix.
- **PROMPT_DOCTRINE.md (✗).** Same as TOP. **Remediation:** reference Custer's pending consolidation, or author. 5 min reference / 4–6 hours real.
- **Crisis trigger document (⚠).** Operator is non-consumer (the user is the builder). It does not have a consumer crisis surface. But the Method requires explicit n/a declaration. The current state is ambiguous. **Remediation:** add a "Crisis surface — n/a, non-consumer product, builder is the user" declaration to Operator's CLAUDE.md or SECURITY.md. 15 min.

### Custer — 2/8

**Strengths.** PROMPT_DOCTRINE.md exists and is substantive (1,978 words). SECURITY.md is complete and reflects voter-PII isolation requirements (CRS 1-2-305). Seven north-star points in CLAUDE.md function as commandments-in-spirit. REFUSAL_AUDIT.md exists.

**Gaps.**

- **STORY.md (✗) — biggest single gap in the portfolio.** Custer has been running 18+ months. It has won assemblies (27/28 delegates at Custer County Assembly 2026-03-28). It has 1,945 voters in its data layer and a candidate (Taylor LoPresti) the platform is built around. It has no biographical narrative compiling into it. Principle #1 ("the code is the story") is not honored on a live, working, winning product. This is the most consequential finding of the audit. **Remediation:** author Custer's STORY.md. Founder's story (Hans's brewery → military intelligence → Taylor's race), the candidate's story (Taylor's DEA career → Westcliffe → why he is running), the campaign's story (assembly win → primary lock-in → general election plan). Estimated effort: 6–10 hours.
- **Commandments file (⚠).** Inline in CLAUDE.md NORTH STAR section. Same extraction. 1 hour.
- **SPECIALIST_TEMPLATE.md (✗).** Custer has six specialists (Intelligence, Delegate Whip, Voter Universe, Messaging, Field Ops, Digital Blast, Strategy & Timeline). Same as Operator — the template is missing. 2 hours.
- **AGENT_DOCTRINE.md (✗).** Same as Operator. 4–8 hours.
- **Crisis trigger document (⚠).** Custer's crisis surface is different from TOP's (campaign-specific: candidate threat, election-day field emergency, voter-PII exposure incident). CLAUDE.md mentions "If an incident occurs" with a 24h ack / 7-day patch posture. This is partially documented but not extracted. **Remediation:** extract to `CRISIS_TRIGGERS.md`. Include candidate threat, voter-PII exposure, election-day emergency. 2 hours.

### Rubicon — 1/8

**Strengths.** SECURITY.md exists. STORY.md exists (thin but present). NORTH_STAR.md exists.

**Gaps.** Six of eight artifacts missing. Rubicon is paused (behind tag `rubicon-cohort-v1`, 2026-04-13). The gap reflects the pause.

**Remediation posture.** Either:

- **(a)** Declare Rubicon explicitly out of scope for the Method until/unless it un-pauses. Add a "Method conformance — paused; not currently audited under v0.9" line to Rubicon's CLAUDE.md.
- **(b)** Build the missing artifacts when Rubicon un-pauses, treating un-pause as an opportunity for clean Method conformance from start.

Option (a) is the honest move tonight. Option (b) is what happens at un-pause.

## Cross-cutting findings (more important than per-product)

### 1. No product has an extracted `COMMANDMENTS.md`

All four products embed commandments inline in CLAUDE.md. The Method requires commandments to be explicit, named, dated, and Guardian-audited — but a CLAUDE.md mixing build instructions with ethical floors cannot be cleanly Guardian-audited as a commandments file. **This is the single most consistent gap.** Remediation across all four products is a one-pattern, four-extraction job; ~4 hours total.

### 2. The refusal list lives upstream in the doctrine, not per-product

`REFUSAL_AUDIT.md` exists in three of four products as the per-product *audit log* of the refusal. The list itself lives in `THE_BUILDERS_DOCTRINE.md II.8`. The Method document says "maintain a refusal list per product" — implying per-product. The actual practice is "shared upstream list, per-product audit log." Either the practice is right and the Method is wrong, or the practice is wrong and every product is missing a real refusal list. The author's view: the practice is right (one list, derived from the doctrine, audited per-product) and the Method needs a Section IV update to reflect it. This is a candidate finding for v1.2 of the Method.

### 3. No product has a dedicated `CRISIS_TRIGGERS.md`

TOP and Custer have crisis surfaces. The triggers live inline. Operator and Rubicon do not have consumer crisis surfaces and make no explicit n/a declaration. The Method requires explicit documentation either way. Remediation: extract for TOP and Custer (3 hours total); declare n/a for Operator and Rubicon (30 min total).

### 4. `PROMPT_DOCTRINE.md` exists only in Custer

TOP and Operator reference the file in their CLAUDE.md as if it lived in their repos. It does not. Either Custer's becomes the canonical version that all products reference, or each product gets its own. The author's view: consolidate to one canonical version (Custer's, as the most developed) and have each product reference it. This is a v1.2 doctrine refinement.

### 5. `AGENT_DOCTRINE.md` exists only in TOP

Operator and Custer run agentic chassis but do not have them documented. They are agents in production without specs. Remediation is real chassis-doc work (4–8 hours per product) and is the most expensive finding in the audit. It is also the most operationally important — the Method's claim that the chassis is reproducible cannot be validated against products whose chassis is undocumented.

### 6. `SPECIALIST_TEMPLATE.md` exists only in TOP

Operator and Custer add specialists ad hoc. The Method requires the build sheet. Remediation: copy and adapt TOP's template; ~2 hours per product.

### 7. `STORY.md` is missing from Custer entirely

Principle #1 ("the code is the story") is the foundational principle of the Method. Custer is the product the author is most actively running. The gap is structural, not incidental. Remediation: author Custer's STORY.md; ~6–10 hours.

## Remediation plan

Effort estimates assume the author working in focused sessions with AI assistance, not fresh-context cold authoring.

### Tier 1 — single-pattern, four-product extractions (target: 2026-05-08)

Highest leverage. One extraction pattern, four executions.

- [ ] Extract `COMMANDMENTS.md` from CLAUDE.md inline in TOP, Operator, Custer, Rubicon. ~4 hours total.
- [ ] Extract `CRISIS_TRIGGERS.md` from inline references in TOP and Custer. Add explicit "Crisis surface — n/a, non-consumer product" to Operator and Rubicon CLAUDE.md or SECURITY.md. ~3.5 hours total.
- [ ] Reconcile the refusal-list architecture in the Method document. Either rewrite Section IV to acknowledge "one upstream list, per-product audit log" or rebuild per-product `REFUSAL_LIST.md` files derived from the upstream. The first option is preferred. ~30 min for the Method edit.

**Tier 1 total: ~8 hours.**

### Tier 2 — per-product authoring (target: 2026-05-15)

Real writing work, not extraction.

- [ ] Author Custer's `STORY.md`. ~6–10 hours.
- [ ] Build `SPECIALIST_TEMPLATE.md` for Operator and Custer. ~4 hours total.
- [ ] Decide PROMPT_DOCTRINE.md consolidation — either author per-product or designate Custer's as canonical. If consolidation: update TOP and Operator CLAUDE.md to reference Custer's. ~30 min for reference update; ~8–12 hours for per-product authoring.

**Tier 2 total: ~10–24 hours depending on PROMPT_DOCTRINE choice.**

### Tier 3 — chassis-doc authoring (target: 2026-05-29)

Most expensive, most operationally important.

- [ ] Author `AGENT_DOCTRINE.md` for Operator. ~6–8 hours.
- [ ] Author `AGENT_DOCTRINE.md` for Custer. ~6–8 hours.

**Tier 3 total: ~12–16 hours.**

### Tier 4 — defer until pause clears

- Rubicon's missing artifacts. Decision deferred until Rubicon un-pauses. Add a "Method conformance — paused" declaration tonight. ~10 min.

### Total remediation effort

Tiers 1–3 combined: **~30–48 hours** of focused work over ~3 weeks. This is the cost of bringing the portfolio to honest Section IV conformance. Phase 2 of the Builders' Kit external test (one outside builder applies the framework cold) should run *after* Tier 1 minimum, and ideally after Tier 2.

## What this audit demonstrates

The Method is operational only insofar as the artifacts exist. Today they mostly do not. The Method document and the portfolio do not currently match.

That gap is the main honest claim in v0.9 Provisional. Section II already states it abstractly ("the reproducibility script does not yet exist," "the audit has not been third-party scored"). This audit makes the gap concrete: per-product, per-artifact, with remediation dates.

What this audit does not do:
- It does not satisfy v1.0 precondition #2 (third-party scoring). This is the author scoring his own portfolio. An outside reader scoring this same matrix is the v1.0 gate.
- It does not satisfy v1.0 precondition #1 (executable reproducibility script). That work is separate.
- It does not validate the portability claim. That requires a real external case (Section II Limit #4).

What it does do:
- It surfaces the gap between the Method's required-artifact set and the portfolio's current state.
- It assigns dated remediation to every gap.
- It demonstrates that the Section IX audit format is operational, not aspirational.
- It commits the author publicly to closing the gap by 2026-05-29.

If the gap is not closed by 2026-05-29, the Method's Section IV claim weakens further and the next revision should restructure Section IV around what the portfolio actually has rather than around what the framework wants it to have.

---

**Audit author.** Hans Prahl, with AI co-authoring.
**Audit date.** 2026-05-01.
**Next audit.** 2026-05-29 (Tier 1–3 completion check) or before any external claim that the Method is operational, whichever comes first.
