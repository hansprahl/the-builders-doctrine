# Grok Cold-Read Package — Codify the Two-Reuse-Channels Finding into Canonical Doctrine

**Date staged:** 2026-05-30
**Author:** Hans Prahl (Operator/TOP/Custer portfolio) + Claude Opus 4.7 as scribe
**Audience:** Grok (cold-read external auditor), via Hans's manual workflow
**Workflow reference:** `feedback_grok_second_opinion_workflow.md` (mirrors the 2026-05-19 §1 retraction precedent and the 2026-05-30 §§2/3/4 cold-read that *produced* this finding)
**Doctrine targets:**
- [`THE_BUILDERS_DOCTRINE.md`](THE_BUILDERS_DOCTRINE.md) — add Principle #14 after #13 (line 207)
- [`THE_BUILDERS_DOCTRINE.md`](THE_BUILDERS_DOCTRINE.md) line 375 footer — patch the v1.0 strike note to acknowledge partial supersession
- `~/.claude/CLAUDE.md` line 48 — expand the Borg Principle bullet from one line to a tiered framing

---

## Why this cold-read

On 2026-05-30 the chassis Borg-upstream workstream produced a mass retraction: §§2, 3, 4, 5 in `CHASSIS_PROPOSED_EXTENSIONS.md` were all retracted within hours of each other after a cheap-gate-first second-product portability sketch. §4's retraction triggered a Grok cold-read (see [2026-05-30_grok_cold_read_chassis_proposals_2_3_4.md](2026-05-30_grok_cold_read_chassis_proposals_2_3_4.md)) whose verdict surfaced the actual deliverable of the day: **the Borg principle has a tiering problem.** Reuse runs on two channels, not one. Forcing rich product engines into the thin chassis abstraction either guts the policy or balloons the substrate.

That finding currently lives only in `CHASSIS_PROPOSED_EXTENSIONS.md` under the closing section *"Meta-finding from the 2026-05-30 mass retraction — the two reuse channels."* It explicitly marks itself as NOT YET doctrine-canonized.

This package routes the proposed canonical-doctrine codification through Grok before Hans commits. Per the §1 + §4 precedents, doctrinal claims that reverse or supersede prior doctrine calls earn external cold-read.

**Specifically this codification:**
- Adds a numbered principle (#14, "The Two Reuse Channels") to `THE_BUILDERS_DOCTRINE.md`, which currently has #1–#13.
- The doctrine **explicitly struck a "Borg" section on 2026-05-15** with the footer note: *"Cross-product Borg behavior is encoded in the chassis-port surface and validated empirically; doctrinal prose adds no signal."* This codification partially reverses that strike — the 2026-05-30 mass retraction is the new empirical evidence that doctrinal prose has signal after all.
- Expands `~/.claude/CLAUDE.md` Borg bullet from one line to a tiered framing.

---

## The proposed addition to THE_BUILDERS_DOCTRINE.md (Principle #14)

To be inserted after Principle #13 (line 207, before the `---` separator). Follows the established #12/#13 structural template (**Principle / Born in / In code / Empirical posture / Scope / Vocabulary translation**).

```markdown
#### 14. The Two Reuse Channels

**Principle.** Cross-product code reuse runs on two channels, not one. The first channel is the *chassis layer* — thin, universal, low-context primitives wired identically across products. The second channel is *tool-layer copy-adapt* — rich, doctrine-heavy engines that products copy from each other and substitute the doctrine-specific surfaces (commandments, scoring rubrics, history shape) without going through a shared abstraction. Each channel has its own fitness landscape. Chassis wins when the primitive's interface is more stable than the policy code behind it. Tool-layer copy-adapt wins when the policy code is itself the load-bearing substance and forcing it through a thin abstraction would either gut the policy or balloon the chassis surface. The Borg principle ("every product feeds back into Operator") is honored on both channels. The error mode is forcing a rich engine through the chassis because the principle seems to mandate it — that produces either a gutted primitive or a chassis ballooned to one consumer's shape.

**Born in.** 2026-05-30 mass retraction. The chassis Borg-upstream workstream opened five proposed primitives (`AdversarialReview`, `OutputGate`, `AAR` enrichments, `PromptGuardian` enrichments, function-style `Specialist` runner). All five retracted within fifteen days, four on the same day, after a cheap-gate-first back-of-envelope portability sketch against TOP (the second consuming product) showed each one either gutted the policy or ballooned the chassis surface. The §4 retraction was the most load-bearing: a Grok cold-read fact-correction surfaced that TOP's `local-mcp/tools/prompt_guardian.py` is a 1171-line *copy-adapt* of Operator's 1354-line `tools/prompt_guardian.py` — same architecture (dual-layer scoring, closed-loop correction with auto-rollback, history, doctrine SHA pinning), different commandment sets (wellness vs business). The reuse vector was direct file-level copy-adapt with product-doctrine substitution, not chassis composition. The Operator-side richness had already traveled to TOP through a parallel channel that bypassed the chassis entirely. Naming the channel was a retroactive observation; the doctrine had been operating on it for months without seeing it.

**In code.** The discipline is procedural and lives in `CHASSIS_PROPOSED_EXTENSIONS.md` as the staging area. Any candidate primitive must (a) explicitly assess whether it is *commodity-shape* (chassis-fit) or *rich-engine-shape* (tool-layer-fit) before any validation experiments are specified, and (b) pass the cheap-gate-first portability sketch against the second consuming product before any chassis code is written. A section that proposes promoting a rich engine into the chassis without naming its tier is auto-retracted on next cold-read. The PROMOTE-SUBSET disposition (extract only the smallest portable type contracts from a richer reference) is a valid intermediate outcome. Today the chassis layer hosts: `ApprovalQueue`, `CrisisFloor`, `ReflectionGate`, `AuthorityGradient`, `UserContext`, `AARLog` (the simple primitive, not Operator's KG-enriched version), `PromptGuardian` (the building-blocks base, not Operator's 1354-line engine), `Specialist` + `SpecialistRegistry`. The tool-layer copy-adapt channel hosts as its first named example: TOP ↔ Operator `prompt_guardian.py`. Both channels are first-class. Both are how the Borg principle gets executed.

**Empirical posture (2026-05-30, N=5 staging-area proposals).** Five primitives proposed, five retracted. §1 (`AdversarialReview`) retracted 2026-05-19 on its own terms (over-architecting). §§2/3/4/5 retracted 2026-05-30 on tier-mismatch grounds; §4's Grok cold-read produced the explicit two-channel naming. Roughly 45 minutes of cheap-gate-first sketches × four sections caught what would have been an estimated 3–6 person-weeks of chassis code + parity-test machinery. The N is small, and "cheap gate retracts everything" is itself a signal worth watching — if proposals two through six all retract too, the test may be over-tuned or the staging area may be looking in the wrong place. As of 2026-05-30 the test is held as load-bearing because the retraction reasons were specific and Grok cold-read concurred on three of four.

**Scope.** Applies to any cross-product code reuse decision. Three clarifications.

*Chassis additions.* Any new file under `kit/chassis/` must pass the second-product portability sketch first. Default disposition is REJECT unless the primitive is commodity-shape. PROMOTE-SUBSET is preferred over PROMOTE-FULL when the source is a rich engine.

*Tool-layer copy-adapt.* When a product copy-adapts another product's tool, the receiving product owns the divergence and the substitution. The source product is not the canonical version; the substrate (Mission Command + Agent Doctrine + the Builders' Doctrine) is. Substitution must preserve the doctrine-load-bearing structure (e.g., dual-layer scoring) while replacing the doctrine-specific surface (commandments).

*Drift detection.* If the same engine starts diverging in three or more products with the same architectural pattern, that is the signal to reconsider chassis promotion at the PROMOTE-SUBSET level. Until then, copy-adapt is correct and not a code-smell.

**Vocabulary translation.** This principle is the doctrine-level companion to the operational Borg principle in CLAUDE.md. The Borg principle states *that* reuse happens; this principle names *how* it happens and *which channel applies when*. The 2026-05-15 audit struck a previously-deferred "Borg" section from this doctrine on the grounds that empirical chassis-port surface had no doctrinal prose to add. That call held until 2026-05-30, when the mass retraction surfaced the tiering refinement. This principle supersedes the 2026-05-15 strike with cause — the empirical surface did produce signal, and the signal is the two-channel framing above.
```

---

## The proposed patch to THE_BUILDERS_DOCTRINE.md line 375 footer

Current sentence inside the footer paragraph:

> "Cross-product Borg behavior is encoded in the chassis-port surface and validated empirically; doctrinal prose adds no signal."

Proposed replacement (one sentence added at the end):

> "Cross-product Borg behavior is encoded in the chassis-port surface and validated empirically; doctrinal prose adds no signal. **Partially superseded 2026-05-30: the cross-product Borg mass retraction (CHASSIS_PROPOSED_EXTENSIONS.md §§2–5) produced a tiering refinement now codified as Principle #14, "The Two Reuse Channels."** "

---

## The proposed update to `~/.claude/CLAUDE.md` (line 48 bullet under "Shared frameworks")

Current:

```markdown
- **Borg Principle** — every product, capability, and tool feeds back into Operator. Nothing exists in isolation. The collective gets stronger with each addition.
```

Proposed:

```markdown
- **Borg Principle (two channels)** — every product, capability, and tool feeds back into Operator. Nothing exists in isolation. The collective gets stronger with each addition. **Reuse runs on two channels:** (1) *chassis layer* — thin, universal, low-context primitives (ApprovalQueue, CrisisFloor, UserContext, AuthorityGradient, ReflectionGate) wired identically across products; (2) *tool-layer copy-adapt* — rich, doctrine-heavy engines (PromptGuardian, AAR) that products copy from each other and substitute the doctrine surface (commandments, scoring rubrics) without a shared abstraction. Forcing a rich engine through the chassis either guts the policy or balloons the substrate. **Cheap-gate-first** (sketch second-product portability against TOP before drafting any chassis code) is the mandatory pre-test. See `~/Projects/the-builders-doctrine/THE_BUILDERS_DOCTRINE.md` Principle #14 for the long form.
```

---

## Questions for Grok

The four questions below are what Hans is asking Grok to chew on. Verdicts welcome; reframes more welcome.

### Q1 — Is "The Two Reuse Channels" load-bearing enough to earn a numbered principle?

The 2026-05-15 doctrine audit explicitly struck a Borg section as redundant ("doctrinal prose adds no signal"). The 2026-05-30 mass retraction is N=5 of proposals, 5 retracted — small N, all retractions specific, three Grok-concurred. Is that enough empirical surface to (a) add a numbered principle reversing the strike, or should this stay at the (b) "subsection inside Section IV (Architecture of Trust)" tier, or (c) "addendum-only-to-CLAUDE.md, keep doctrine silent" tier?

The risk of (a): over-weighting a doctrinal observation that the empirical surface already validates without prose. The risk of (b) or (c): future builders skipping the cheap-gate-first discipline because the doctrine doesn't surface it as load-bearing.

Hans's instinct: numbered principle, because Principle #12 and #13 both originated from specific incidents (one war story, one brewery exit) and earned numbered status. The 2026-05-30 mass retraction is the equivalent founding incident for #14. But Hans wants Grok to pressure-test the over-weighting risk.

### Q2 — Does the principle correctly name the *failure mode*, or is it naming the *workflow* and dressing it as a failure-mode principle?

The principle's load-bearing claim is: *forcing a rich engine through the chassis abstraction either guts the policy or balloons the substrate.* That's a failure-mode claim. The rest of the principle (cheap-gate-first, PROMOTE-SUBSET disposition, REJECT default) is workflow that *prevents* that failure mode.

Does the principle stand on the failure-mode claim alone? Or is the workflow doing the actual load-bearing work and the failure-mode framing is a thin abstraction over what's really a procedural discipline?

If the latter, the principle should be reframed as "The Cheap-Gate-First Discipline" or similar — workflow-first, failure-mode-second. Hans is open to that reframe.

### Q3 — Is the empirical posture honest?

N=5 staging-area proposals, 5/5 retracted. The "Born in" section claims this caught 3–6 person-weeks of work that would otherwise have been spent on chassis code + parity tests. The "Empirical posture" section explicitly flags the small N and the "cheap gate retracts everything" failure mode that would invalidate the test.

Is the honest-gap language sufficient? Is there a Law VII-style additional flag needed (e.g., "this principle is held tentatively until N≥9 staging-area proposals with non-zero PROMOTE-FULL outcomes")?

Hans's instinct: the language is honest as written; the principle is held as load-bearing because the *reasons* for each retraction are specific (not just "we got tired of writing"). But if Grok thinks the empirical posture needs an explicit "tentative until N=9" hedge, Hans will add it.

### Q4 — Does the partial-supersession framing of the 2026-05-15 strike read as cause-and-effect honest, or as retconning?

The 2026-05-15 strike of Section VIII (Borg) was specifically grounded in *"empirical chassis-port surface has no doctrinal prose to add."* The 2026-05-30 finding contradicts that — empirical chassis-port surface produced explicit doctrinal prose. The proposed footer patch acknowledges "Partially superseded 2026-05-30."

Does that read as the doctrine evolving cleanly with cause, or does it read as the founder retconning the 2026-05-15 call to enable a new principle that aligns with current-state thinking?

Hans's instinct: the empirical surface genuinely produced the prose (the meta-section in CHASSIS_PROPOSED_EXTENSIONS.md was the doctrine writing itself; #14 just promotes it to canonical). But the founder being his own audit chair on this call is exactly the same-session self-audit failure mode named in `feedback_no_same_session_self_audit.md`. Grok is the cold chair.

---

## Verdict request

For each of the three artifacts (Principle #14, line 375 patch, CLAUDE.md bullet), Grok please return one of:

- **SHIP** — text is correct as drafted, commit it.
- **SHIP-WITH-EDITS** — text is structurally correct but needs specific edits before commit. List them.
- **REFRAME** — the principle is correct but the framing/placement is wrong. Propose the alternative.
- **HOLD** — the principle is not load-bearing enough to canonize today. Reason required.
- **RETRACT** — the finding itself is wrong or premature. Reason required.

Append the verdict with whichever Q1–Q4 surfaced the call.

---

## Files for Grok to reference if needed

- [`CHASSIS_PROPOSED_EXTENSIONS.md`](CHASSIS_PROPOSED_EXTENSIONS.md) — the staging area; closing meta-section is the source text being promoted
- [`THE_BUILDERS_DOCTRINE.md`](THE_BUILDERS_DOCTRINE.md) — current state of canonical doctrine
- [`2026-05-30_grok_cold_read_chassis_proposals_2_3_4.md`](2026-05-30_grok_cold_read_chassis_proposals_2_3_4.md) — the prior cold-read package this finding emerged from
- `~/.claude/CLAUDE.md` — the global file with the current one-line Borg bullet
- `~/Projects/the-builders-doctrine/META_DOCTRINE.md` — Laws V–X, doctrinal-evolution rules (relevant to Q4)

---

**End of cold-read package.**
