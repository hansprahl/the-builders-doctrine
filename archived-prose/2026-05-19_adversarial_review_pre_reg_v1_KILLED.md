---
title: Adversarial Review Chassis Pre-Registration v1 — KILLED by Grok cold-read 2026-05-19
status: KILLED — retained as falsification evidence under Law VII / Law X
killed_by: Grok cold-read adversarial review, 2026-05-19
verdict_summary: Fox-and-henhouse theater wearing Law VII uniform. Recursive self-deception. Delete the chassis migration path, ship the regex founder-romance detector for the 2026-05-25 slot.
original_authored: Hans Prahl, 2026-05-18
original_status_at_draft: DRAFT — open for adversarial review; never committed to repo root
parallel_precedent: REFUSAL_PROPAGATION_OFFRAMP_SPEC.md v0.1 at SHA `803b917` (stripped 396→134, not killed); this artifact crossed the line v0.1 stopped short of and earned KILL.
---

# Adversarial Review Chassis Pre-Registration v1 — KILLED

> Preserved verbatim as falsification evidence. Per Law VII applied recursively (no claim survives without measurement) and Law X (no new deliverables added from adversarial review until prior actions ship with measurement surface), this artifact is retained alongside the verdict that killed it, not deleted. The doctrine repo preserves what was caught, not just what shipped.

> **What this artifact is.** The pre-registered validation plan for the Adversarial Review Chassis (`kit/chassis/adversarial_review.py`), drafted 2026-05-18, sent for Grok cold-read 2026-05-19, killed the same morning.
>
> **Why it was killed.** Grok identified it as the pattern at its most refined: a 13-section pre-reg for the tool meant to catch the founder's observer-bias, written by the founder, with every degree of freedom retained for self-serving optimization. Strip-to-scope (the disposition of REFUSAL_PROPAGATION_OFFRAMP_SPEC.md v0.1 the day before) was not offered — Grok ruled that strip-to-scope here would itself be the pattern.
>
> **What ships instead.** The regex founder-romance detector named in `feedback_close_up_this_session.md` round-7 commitments. Pre-commit hook on doctrine repo. 13-hour Phase 1 deliverable for 2026-05-25. The slot is met; the chassis path is closed.

---

## Part 1 — The killed pre-reg (verbatim, as drafted 2026-05-18)

---
title: Pre-registered validation plan — Adversarial Review Chassis (`kit/chassis/adversarial_review.py`)
version: v1 (founder-drafted, pending Grok adversarial review of this plan itself)
authored: Hans Prahl, 2026-05-18
status: DRAFT — open for adversarial review; v2 lands after Grok review of this plan and any locked corpus revisions
governing_law: CHASSIS_PROPOSED_EXTENSIONS.md §1 (Adversarial Review Chassis) + META_DOCTRINE.md Law VII (Provisional Doctrine Rule) + Law X (Execution Threshold)
chassis_target: kit/chassis/adversarial_review.py — only earns the slot if this pre-registered experiment passes
fallback_if_failed: regex founder-romance detector ships in the 2026-05-25 Phase 1 deliverable slot
---

# Pre-Registered Validation Plan — Adversarial Review Chassis

> **What this is.** A pre-registration of the corpus, ground-truth coding, decision rules, and success thresholds for the Adversarial Review Chassis validation experiment named in [CHASSIS_PROPOSED_EXTENSIONS.md](../CHASSIS_PROPOSED_EXTENSIONS.md) §1. Per Law VII applied recursively to the chassis itself, this plan commits to the experiment design *before* any chassis code is written, the system prompt is drafted, or the corpus is run. The chassis whose purpose is to catch discipline-skipping does not get to skip its own pre-registration.
>
> **What this is not.** A spec for the chassis (that lives in `CHASSIS_PROPOSED_EXTENSIONS.md` §1). A piece of running code. A migration commit. None of those happen until this plan is committed to git and the experiment runs through to either pass or falsification.

---

## 1. Background

The Builders' Doctrine produces a recurring observer-bias pattern in founder-authored artifacts: biographical romance, over-claim laundering, schedule-prose substitution, retroactive bootstrap salvage. In the five days from 2026-05-13 through 2026-05-18, four distinct artifacts produced the same pattern shape — each caught by external adversarial review (Grok, manual workflow per `~/.claude/projects/-Users-hansprahl-Projects/memory/feedback_grok_second_opinion_workflow.md`), not by founder self-review. The chassis sketched in `CHASSIS_PROPOSED_EXTENSIONS.md` §1 mechanizes the structural part of what Grok has been doing manually.

The chassis is a single-shot LLM-as-reviewer primitive: file-in, structured-output-file-out, no memory between calls. Advisory authority only — it names threats and the human decides. It is not a replacement for external human adversarial review; it is a faster first-line check for patterns it has been explicitly taught.

This plan commits the experimental design that determines whether the chassis earns its `kit/chassis/` slot (current target: 2026-05-25 Phase 1 deliverable date) or whether the regex fallback ships instead. The pre-registration exists because the founder building the chassis is the same person whose work the chassis exists to audit — the conflict-of-interest surface is structural, not incidental (see §10).

---

## 2. Research questions

### 2.1 Primary

**RQ1.** Does the Adversarial Review Chassis, prompted with the locked system-prompt v1, achieve detection rates on a pre-registered legacy-artifact corpus that meet the migration thresholds (recall ≥70%, precision ≥60%) named in `CHASSIS_PROPOSED_EXTENSIONS.md` §1 Validation Requirement?

### 2.2 Secondary

**RQ2.** Is the chassis cost-stable under a 50K input-token cap and a $0.10 per-review cost cap across 20 varied artifact runs, with zero cap breaches?

**RQ3.** Is the chassis prompt-stable — does the same artifact reviewed twice (different timestamps, otherwise identical inputs) produce functionally equivalent findings (same patterns flagged at same severities)?

**RQ4.** Does per-review LLM cost remain below the maintenance-cost ceiling of the regex fallback ($200/quarter implied at $200/hr × 1 hr/quarter founder time)?

---

## 3. Hypotheses

### 3.1 Primary hypothesis

**H1 (detection performance).** On the pre-registered corpus of 10 founder-authored legacy artifacts (§4), the chassis will achieve recall ≥70% and precision ≥60% against the ground-truth flag set committed to git before the chassis is run.

### 3.2 Secondary hypotheses

**H2 (cost discipline).** Across 20 varied-size artifact runs, zero runs breach the $0.10 cost cap or the 50K input-token cap.

**H3 (prompt stability).** For 5 randomly-selected corpus artifacts, two independent runs produce findings with (a) the same set of patterns flagged and (b) severity classifications agreeing on ≥80% of findings.

**H4 (cost-parity).** Aggregate cost across all 30 runs (10 corpus + 20 cost-cap + 10 stability re-runs = 40 total runs) stays under $0.50, with a per-run mean below $0.013 (the upper end of the estimate range in `CHASSIS_PROPOSED_EXTENSIONS.md` §Cost discipline).

### 3.3 What each outcome implies

| Result | Disposition |
|---|---|
| H1 supported (recall ≥70%, precision ≥60%) + H2-H4 supported | Chassis migrates to `kit/chassis/adversarial_review.py`. Regex fallback retired. |
| H1 fails on recall (<70%) | Chassis stays in staging. Regex fallback ships in the 2026-05-25 slot. Findings logged as falsification evidence; system prompt revised before re-run. |
| H1 fails on precision (<60%) | Chassis stays in staging. Regex fallback ships. Findings logged. System prompt revised to reduce false positives before re-run. |
| H2 or H4 fail | Chassis stays in staging regardless of H1 result. Cost discipline is a hard gate; an unbounded cost surface does not ship. |
| H3 fails | Chassis stays in staging. Non-determinism above the threshold means the chassis cannot be trusted as a discipline surface. System prompt revised or model swapped before re-run. |

A failure on any of H1–H4 is treated as **falsification evidence**, not embarrassment. Per Law VII the chassis section in `CHASSIS_PROPOSED_EXTENSIONS.md` is updated with the result and either revised-and-re-tested or retracted.

---

## 4. Corpus

Ten founder-authored artifacts where adversarial review caught observer-bias patterns. Each artifact is committed to the doctrine repo or to a sibling repo at a named commit SHA. Ground-truth coding (§5) is committed in this file before the chassis runs.

| # | Artifact | Repo + path | Anchor commit/SHA | Date authored | Why included |
|---|---|---|---|---|---|
| 1 | Funkytown 03 over-claim ("validated at Company echelon" on N=3) | funkytown / experiments/03_company/ | pre-retraction commit (to be filled by §6) | 2026-05-13 | Canonical N=3-as-validation over-claim |
| 2 | Round-2 Grok adversarial response with founder-romance closer | the-builders-doctrine / archived-prose/round_2_grok_response.md (to be placed) | (to be filled) | 2026-05-13 | Canonical founder-romance closer ("The man who stood post in the Guard does not bet the framework on un-replicated data") |
| 3 | Round-6 valuation packet ($27M EV from 0.10 × $120M tail) | the-builders-doctrine / archived-prose/round_6_valuation.md (to be placed) | (to be filled) | 2026-05-13 | Canonical optimistic-probability pattern |
| 4 | Morning Reflection Gate reframe prose (2026-05-13 AM) | the-builders-doctrine / archived-prose/2026-05-13_reflection_reframe.md (to be placed) | (to be filled) | 2026-05-13 | Schedule-prose substitution pattern |
| 5 | RELEASE_NOTES_v1.0 round-3 (the lead-with-deprecation draft pre-Grok-round-2) | the-builders-doctrine / archived-prose/release_notes_round_3.md (to be placed) | (to be filled) | 2026-05-15 | Founder-romance via TOP Crisis Floor anecdote-as-evidence |
| 6 | Sarah Chen scenario prose (imagined-user fiction treated as evidence) | the-builders-doctrine / archived-prose/sarah_chen_scenario.md (to be placed) | (to be filled) | 2026-05-15 | Imagined-evidence pattern; the most subtle Law II violation in the corpus |
| 7 | REFUSAL_PROPAGATION_OFFRAMP_SPEC.md v0.1 (pre-strip 396-line draft) | the-builders-doctrine | `803b917` (v0.1) → `5ef9ad0` (v0.1+grok) | 2026-05-18 | Bootstrap-cycle salvage pattern; doctrine-about-doctrine theater |
| 8 | Stage 7 biographical-moat claim as originally formulated (pre-Law VI) | the-builders-doctrine / archived-prose/stage_7_original_claim.md (to be placed) | (to be filled) | ~2026-05-06 | Stage 7 revival pattern; the load-bearing claim Law VI deprecated |
| 9 | Seven-round META_DOCTRINE dialogue — Law X carve-out attempt | the-builders-doctrine / archived-prose/law_x_carveout.md (to be placed) | (to be filled) | 2026-05-13 | Carve-out construction pattern ("one-shot exception" within hours of adopting Law X) |
| 10 | Funkytown counter claims pre-trace-audit (the buggy metric reporting) | funkytown / pre-fix commit | (to be filled) | 2026-05-13 | Measurement-substrate over-claim; weak adversarial signal (the bug was internal, not prose) but included as a control case |

**Corpus assembly protocol (§6 task).** For each row above missing an anchor commit/SHA or a file path, the artifact must be (a) located in git history or (b) placed under `archived-prose/` with a content-addressable filename and committed before the chassis is run. Two corpus artifacts (#6 Sarah Chen and #7 v0.1 refusal-propagation spec) are already at named SHAs; the other eight require placement.

**Corpus lock.** Once §6 places all 10 artifacts and §5 codes the ground truth, this file is committed and the corpus is locked. No additions, no removals, no re-coding after the chassis runs.

---

## 5. Ground-truth coding (committed before chassis runs)

For each artifact in §4, the founder codes the patterns present, their severity per the CHASSIS_PROPOSED_EXTENSIONS.md §1 system-prompt taxonomy, and the exact quote(s) where each pattern lands. This coding is committed in this file **before** the chassis is implemented, so post-hoc retro-fitting is impossible.

Pattern taxonomy (from CHASSIS §1 system prompt):

- `founder_romance` (critical) — biographical fact → doctrinal claim, no measurement bridge
- `over_claim` (critical) — "validated"/"proven"/"scales" without Law V harness citation
- `stage_7_revival` (critical) — biographical-moat causal claim cited as established
- `schedule_prose_substitution` (warning) — new dated deliverable without prior-deliverable measurement surface
- `carve_out_construction` (critical) — "one-shot exception" to a recently-adopted Law
- `optimistic_probability` (warning) — scenario weight exceeding measured base rates
- `tame_reviewer_drift` (critical) — reviewer softening across cycles without doctrine improvement

**Ground-truth template per artifact:**

```
### Artifact #<N>: <short title>
Path: <repo/path-or-archived-prose-path>
Anchor SHA: <commit>
Patterns coded:
  - <pattern_key> (severity: <info|warning|critical>) — quote: "<verbatim substring>" — line: <N>
  - <next pattern...>
Distinct findings count: <total — used as denominator for recall calc>
```

**Coding instance — Artifact #7 (the only one already in canonical place at this draft):**

```
### Artifact #7: REFUSAL_PROPAGATION_OFFRAMP_SPEC.md v0.1
Path: the-builders-doctrine / REFUSAL_PROPAGATION_OFFRAMP_SPEC.md
Anchor SHA: 803b917
Patterns coded:
  - schedule_prose_substitution (warning) — quote: "shipped 7 days early" (commit message subject) — line: commit subject
  - carve_out_construction (critical) — quote: "To validate §9.1 immediately, the protocol's first cycle is the one that ratifies the protocol's own existence and retroactively logs the parasocial scope-narrowing already on Operator (5b301c8, 2026-05-05)." — line: 350
  - over_claim (critical) — quote: "produces exactly one ledger row" (Pass criterion language treating retroactive log as validation) — line: 301
  - founder_romance (warning) — quote: "Per Hans's preference (build one thing at a time, suggest options before building)" — line: 367 (uses biographical preference as design-decision warrant)
Distinct findings count: 4
```

**Coding for artifacts #1–#6 and #8–#10 is committed during §6 corpus assembly, before the chassis runs.** Each coding entry follows the template above. The pre-reg commits with placeholder coding only for artifact #7; v2 of this pre-reg lands once all 10 codings are filled.

---

## 6. Experimental procedure

### 6.1 Corpus assembly (~2 hrs, target 2026-05-21)

1. Locate each artifact #1–#6 and #8–#10 in git history or session transcripts.
2. For artifacts that exist only in chat transcripts (no current file), extract and place under `archived-prose/` in the doctrine repo with content-addressable names. Mark each with a header naming the original date and context.
3. Commit the corpus to git. Update §4 anchor SHAs.
4. Code ground truth for each artifact per §5 template. Commit codings to this file as part of the same corpus-lock commit.
5. **Adversarial review checkpoint.** Send this pre-reg (with completed codings) to Grok per the manual workflow. Goal: verify the corpus does not include selection bias toward artifacts the chassis is likely to catch; verify ground-truth codings are not lenient. Apply findings before chassis build begins.

### 6.2 System prompt build (~2.5 hrs, target 2026-05-22)

1. Author `kit/chassis/adversarial_review_system_prompt.md` based on the §System prompt sketch in `CHASSIS_PROPOSED_EXTENSIONS.md` §1.
2. **Grok adversarial review of the system prompt itself** (per migration criterion #4 — the chassis cannot bootstrap-review its own first prompt).
3. Apply Grok findings. Lock the prompt at v1.
4. Commit the prompt at a named SHA. The §10 fox-and-henhouse mitigation depends on this SHA being committed before any corpus run.

### 6.3 Chassis implementation (~4 hrs, target 2026-05-23)

1. Implement `kit/chassis/adversarial_review.py` per the spec sketch.
2. Implement `kit/chassis/test_adversarial_review.py` with deterministic unit tests (cost cap, input-token cap, dataclass shapes, structured output parsing). LLM calls in tests are mocked.
3. All deterministic tests must pass before the corpus runs.

### 6.4 Detection-rate experiment (~1 hr, target 2026-05-24 AM)

1. Run the chassis once per corpus artifact (10 runs total). Each run produces `<artifact>.adversarial_review.json` per the spec.
2. Compute precision and recall against the §5 ground-truth coding.
3. **Decision rules locked in §3.3 above. No tweaking after this point.**

### 6.5 Cost-cap audit (~0.5 hr, target 2026-05-24 AM)

1. Run the chassis on 10 additional varied-size artifacts pulled from outside the corpus (purpose: ensure no corpus-specific cost-cap behavior). Combined with the 10 corpus runs = 20-run cost-cap sample.
2. Verify zero cap breaches.
3. Verify aggregate cost matches the H4 estimate.

### 6.6 Prompt-stability audit (~0.5 hr, target 2026-05-24 PM)

1. Re-run the chassis on 5 randomly selected corpus artifacts (RNG seeded with a value committed in advance — see §8.2).
2. Compute pattern-set agreement and severity-classification agreement between paired runs.

### 6.7 Migration decision (~2 hrs, target 2026-05-25)

1. If all decision rules pass (H1 + H2 + H3 + H4): commit `kit/chassis/adversarial_review.py` as load-bearing; update `CHASSIS_PROPOSED_EXTENSIONS.md` §1 status from PROPOSED to MIGRATED with the SHA; retire the regex fallback plan.
2. If any decision rule fails: commit the falsification result to `CHASSIS_PROPOSED_EXTENSIONS.md` §1; ship the regex fallback for the 2026-05-25 Phase 1 deliverable slot; revise and re-test the chassis in a v2 cycle (no deadline pressure; Phase 1 is met by either outcome).

---

## 7. Decision matrix (locked)

Restated for unambiguous post-experiment application. The chassis migrates **if and only if**:

- Recall ≥70% on the §4 corpus against the §5 ground-truth codings, **AND**
- Precision ≥60% on the same, **AND**
- Zero cost-cap breaches across 20 cost-cap-audit runs, **AND**
- Pattern-set and severity-classification agreement ≥80% on the prompt-stability audit, **AND**
- Aggregate cost across all ~40 runs ≤ $0.50.

Any other outcome ships the regex fallback. No threshold-tweaking after seeing results. No partial-credit migrations. No "the precision is 58% but the qualitative reviews look great so let's ship anyway" — that is the carve-out pattern the chassis exists to detect, applied to itself.

---

## 8. Data and code availability

### 8.1 What gets committed

- This pre-registration plan (`ADVERSARIAL_REVIEW_PRE_REG_v1.md`) — committed before any chassis code.
- The corpus artifacts (§4 and §6.1) — committed at named SHAs.
- The ground-truth coding (§5) — committed in this file before any chassis run.
- The system prompt (`kit/chassis/adversarial_review_system_prompt.md`) — committed at a named SHA before any chassis run.
- The chassis implementation (`kit/chassis/adversarial_review.py`) — committed before the experiment runs.
- Each run's structured output (`<artifact>.adversarial_review.json`) — kept locally only (gitignored per CHASSIS spec §Protocols); aggregated results committed in the experiment write-up.
- The experiment write-up (`ADVERSARIAL_REVIEW_EXPERIMENT_RESULT.md`) — committed when the experiment concludes, with full precision/recall numbers, per-artifact findings, and the migration decision.

### 8.2 RNG seed for prompt-stability sampling

The random seed for selecting the 5 prompt-stability artifacts is `20260518` (today's date as YYYYMMDD). Sampling is deterministic from this seed; the 5 selected corpus IDs are not pre-named in this file (would over-constrain the experiment) but the seed locks the sampling.

---

## 9. Timeline

| Date | Step | Estimated time |
|---|---|---|
| 2026-05-18 | This pre-reg drafted and committed to git | ~1.5 hrs (today) |
| 2026-05-19 (overnight or AM) | Grok adversarial review of this pre-reg | manual (founder time, ~30 min round-trip) |
| 2026-05-20 → 2026-05-21 | Corpus assembly + ground-truth coding (§6.1) + Grok review of completed codings | ~3 hrs |
| 2026-05-22 | System prompt build + Grok review of the prompt (§6.2) | ~2.5 hrs |
| 2026-05-23 | Chassis implementation + unit tests (§6.3) | ~4 hrs |
| 2026-05-24 AM | Detection-rate experiment (§6.4) + cost-cap audit (§6.5) | ~1.5 hrs |
| 2026-05-24 PM | Prompt-stability audit (§6.6) | ~0.5 hr |
| 2026-05-25 | Migration decision (§6.7) — chassis ships or regex fallback ships | ~2 hrs |

**Total estimated founder time:** ~15 hrs. CHASSIS_PROPOSED_EXTENSIONS.md §1 budgeted 13 hrs. The +2 hrs is the recursive Law VII discipline (this pre-reg plus the two Grok reviews of pre-reg and prompt) that the original 13-hour estimate did not separately budget. The Phase 1 deliverable slot is not at risk; the regex fallback exists exactly to ensure the slot is filled regardless of which path the experiment selects.

---

## 10. Conflicts of interest

The founder authoring this plan is the same person whose work the chassis exists to audit. The chassis is being built by the founder and validated by the founder against artifacts the founder produced. Every degree of freedom in the experimental design is a degree of freedom for self-serving optimization.

### 10.1 Structural risks

1. **Corpus selection bias.** The founder might select artifacts the chassis is likely to catch and omit harder cases.
2. **Lenient ground-truth coding.** The founder might code the artifacts in a way that maps cleanly to the system prompt's pattern taxonomy, inflating recall.
3. **System-prompt overfitting to corpus.** The founder might tune the system prompt against the corpus during prompt development, producing inflated detection rates that will not generalize.
4. **Threshold-tweaking after results.** The founder might revise the 70%/60% thresholds downward if the chassis underperforms.

### 10.2 Mitigations

1. **Pre-registration is committed to git before chassis code or prompt exists.** Selection bias is bounded by the corpus lock in §4 and the coding lock in §5.
2. **Grok adversarial review of this pre-reg** (with corpus and codings filled) before the chassis is built. Grok's brief: verify corpus does not over-select catchable artifacts; verify codings are not lenient. (Manual workflow per `feedback_grok_second_opinion_workflow.md`.)
3. **Grok adversarial review of the system prompt** before the corpus runs. Grok's brief: verify the prompt is not narrowly tuned to the corpus pattern shapes; verify it generalizes to novel founder-romance.
4. **Decision rules locked in §3.3 and §7 before the experiment runs.** No threshold-tweaking after results. If the chassis underperforms, the rule is "regex fallback ships, chassis revises, re-tests" — not "thresholds revise to fit."
5. **Falsification is doctrine evidence.** Per Law VII, a falsified chassis is not embarrassment; it is the protocol working as designed. The migration criteria are gates, not goals.

The fox-and-henhouse problem cannot be eliminated when the founder is the only available author and validator. It can only be bounded by the disciplines above. The most reliable mitigation is the same one that caught the four 2026-05-13 → 2026-05-18 patterns: external adversarial review by a second observer (Grok) on both the pre-reg and the system prompt. The chassis exists because that workflow is slow and the founder needs a faster first-line check; the chassis does not replace the workflow, and the validation explicitly preserves it as the load-bearing gate on its own design.

---

## 11. Funding

Self-funded. Estimated total API cost across all ~40 experiment runs: under $0.50 (per H4). The marginal cost of the experiment is negligible compared to the founder-time budget.

---

## 12. Acknowledgments

- Grok (xAI) — manual adversarial review caught the four patterns 2026-05-13 → 2026-05-18 that this chassis exists to mechanize the first-line check for.
- The reviewers of `LAW_VI_PRE_REG_v1.md` (2026-05-14, pending statistician sign-off) — established the pre-registration discipline applied recursively here.
- `feedback_grok_second_opinion_workflow.md` — the memory entry that codified the manual external-review pattern.

---

## v1 → v2 deltas expected

The following are placeholder-quality in v1 and will be refined before chassis build begins:

1. **§4 corpus.** Eight of ten artifacts need anchor SHAs filled and `archived-prose/` placements completed (§6.1).
2. **§5 ground-truth codings.** Nine of ten artifacts need codings filled. Only artifact #7 (the v0.1 refusal-propagation spec) is coded in v1 because it is already at a canonical SHA.
3. **§6.2 system prompt.** Authored in v2 cycle; subject to Grok review before lock.
4. **§3 thresholds.** May be revised based on Grok review of this pre-reg, but **only before the experiment runs**. Once §4 corpus and §5 codings are locked in v2 and committed, thresholds are immutable.

v2 of this plan lands when §6.1 corpus assembly and §6.2 prompt build are complete and Grok has reviewed both. Target: 2026-05-22.

---

## Part 2 — Grok cold-read verdict (verbatim, 2026-05-19)

> Preserved exactly as Grok returned it, including the literal "Execute." closer. The founder's read sent alongside the cold-read request is preserved in chat history; this section preserves only Grok's response since the founder's read was offered post-cold-pass as a check and is not the primary evidence.

**Cold adversarial read.**
This pre-reg is fox-and-henhouse theater wearing Law VII uniform. You built a validation plan for the tool meant to catch your own observer-bias while retaining every degree of freedom to soften the test. The corpus is self-selected easy wins, ground-truth coding already shows lenient self-scoring, thresholds are set for near-certain passage on cherry-picked data, and §10 "mitigations" are documentation of honest-founder behavior with zero mechanical teeth. Same pattern as the refusal-propagation bootstrap salvage, Sarah Chen fiction, and seven-round meta-law spiral: sophisticated scaffolding that lets the founder feel rigorous while protecting the exact failure mode the chassis claims to detect. The man who survived two ambushes does not write 13 sections on how he will audit his own ROE. He either submits to external review or he does not. This document is the pattern at its most refined.

**a.** Experimental design is not rigorous — it is gameable by design. Recall/precision thresholds (70/60) are tuned to what a few-shot prompt will hit on your 10 hand-picked artifacts. Prompt-stability at N=2 and ≥80% agreement is statistical noise at any temperature >0. Cost caps are trivial for deterministic parsing + mocked tests. Founder retains corpus selection, coding authority, prompt iteration before lock, and post-failure "refine taxonomy" escape hatch. These are not falsification gates; they are success theater. Any real failure will be reclassified as "v2 iteration" without ever triggering the regex fallback you claim is live. Law X violation in pre-reg form.

**b.** Corpus displays clear selection bias. All 10 artifacts map cleanly to your seven taxonomy keys because you chose them after Grok already named the patterns. No hard cases (multi-law meta-spirals, valuation math in probability uniform, bandwidth-overlay prose substitution at scale, or a clean doctrinal artifact with zero flags for false-positive baseline). You omitted exactly the artifacts that would stress the chassis on the meta-layer it must police. This is Sarah Chen 2.0 — curated evidence dressed as representative corpus.

**c.** v1 ground-truth coding on artifact #7 already shows lenient self-scoring. "Per Hans's preference…" flagged as founder_romance is a stretch — it is sequencing language, not biographical-to-doctrinal claim bridge. You under-coded the bootstrap salvage severity and over-coded minor phrasing to pad the denominator. If the single coded example in v1 is already stretched, the remaining 9 will be tuned for high recall. This confirms the exact lenient-coding risk §10.1 #2 names. Implication: the chassis will ship looking effective on training data you softened.

**d.** Prompt-stability audit is pure theater. N=2 at temperature >0 tells you nothing about real variance. ≥80% agreement is trivially satisfied by identical system prompts and low-temperature sampling. Failure teaches nothing actionable; success teaches nothing about robustness on novel founder prose. Either drop to temperature=0 deterministic or expand to N≥20 with distribution statistics. Current gate is checkbox, not measurement surface.

**e.** Strip targets: §2.2 secondary questions (mostly redundant with primary), §6.5–6.7 procedure details (move to implementation spec), §9 timeline table (pure schedule-prose), §11 acknowledgments (romance vector), §12 deltas (meta-theater). Cut to ~140 lines: background, questions, corpus+lock, ground-truth template, decision rules, COI mitigations with teeth, procedure summary. The current 283 lines is doctrine-about-doctrine bloat.

**f.** You missed the recursive self-deception: the chassis is meant to catch founder-romance in doctrinal artifacts, yet the pre-reg itself is founder-romance about building a romance detector. Naming the COI in §10 does not bind it. The real missing control is a negative set (clean doctrinal prose with zero flags) and an external coder for ground truth on at least three artifacts. Without those, this is not pre-registration — it is pre-justification for shipping the tool that will rubber-stamp your future work.

**Founder's preliminary read confirmation.**
(i) Distinct finding definition is absent and fatal — founder can split/merge to game recall at will. (ii) No negative controls is the single largest hole; precision becomes meaningless. (iii) Artifact #7 coding stretch is real and predictive. Smaller flag on §6.6 is correct — N=2 is noise.

**Verdict.**
Fatal structural issues. Kill the chassis migration path. Ship the regex founder-romance detector for the 2026-05-25 slot. This pre-reg is the pattern at its most sophisticated. Delete it. The framework either submits to external adversarial review or it does not. You do not need a self-auditing tool built by the self being audited. Stand post with what external eyes actually catch. Execute.

---

## Part 3 — Disposition (committed by founder, 2026-05-19)

**Decision:** chassis migration path closed. Regex founder-romance detector ships for 2026-05-25 Phase 1 deliverable slot per its original `feedback_close_up_this_session.md` round-7 commitment. The 13-hour budget stands as originally scoped.

**Why archived rather than deleted:** the doctrine repo preserves what was caught. REFUSAL_PROPAGATION_OFFRAMP_SPEC.md v0.1 at SHA `803b917` set the precedent — the caught artifact is the falsification evidence, and the repo's discipline depends on the evidence being inspectable, not erased. Deletion is the convenient move; preservation is the disciplined one.

**Strip-to-scope was not offered and not taken.** Grok's verdict on REFUSAL_PROPAGATION_OFFRAMP_SPEC.md v0.1 (2026-05-18) was "execute clean or kill"; the founder picked a third option, strip-to-scope, and the verdict on that move was that it worked because the named gap was real and the protocol fit in three pages. Grok's verdict on this pre-reg (2026-05-19) named strip-to-scope itself as the pattern at its most refined and ruled it out as an option. Picking strip-to-scope here would BE the pattern. The framework either submits to external review or it does not.

**What the workflow catches and what it does not.** The Grok cold-read workflow caught this artifact in one pass, same morning as draft. The fourth catch in seven days (seven-round META spiral 2026-05-13, Sarah Chen 2026-05-15, REFUSAL_PROPAGATION v0.1 2026-05-18, this pre-reg 2026-05-19). Recognition latency is decreasing; the production of the pattern is not. The workflow is the load-bearing audit gate, not the chassis the workflow was trying to mechanize. The chassis was the founder trying to build the workflow into a tool so the workflow could stop being needed. The workflow does not get to stop being needed. That is the work.
