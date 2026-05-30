# Findings — Adversarial fuzz of the Founder-Romance Detector (v0.1)

**Experiment:** Funkytown 11 ("adversary fuzz")
**Run dates:** 2026-05-30
**Detector under test:** `kit/chassis/founder_romance_detector.py` at `v0.1` commit hash. Spec at `kit/chassis/FOUNDER_ROMANCE_DETECTOR_SPEC.md`.
**Output of this finding:** detector patched to `v0.1.1` (severity demotion + two file exclusions), this document, and an open follow-up (corpus-assembly + v0.1.2 retuning).

## Executive summary

The v0.1 regex-based detector for observer-bias patterns in doctrine prose **does not function as a meaningful first-line check at HIGH severity for the `founder_romance` pattern.** Under fair adversarial pressure (definition-only adversary, cross-family Grok-4 judge) the detector caught 20% of bias-exhibiting drafts. Against 104 real doctrine commits, the v0.1 hook would have blocked 35.6% of them under HIGH-severity rules, with HIGH-severity precision of roughly 25%. The block-rate × precision combination triggers the spec's own "ship-disabled + tune in v0.1.x" gate.

**Action taken:** `founder_romance` 1a + 1b demoted HIGH → ADVISORY in `v0.1.1`. Pre-commit hook no longer blocks on this pattern. Grok cold-read becomes the formal first-line gate until `v0.1.2+` retuning. `stage_7_revival` and `carve_out_construction` stay HIGH (narrow, structurally distinctive, baseline-rate clean). `over_claim` and `optimistic_probability` stay ADVISORY — the baseline data **kills** the v2 Grok recommendation to promote them, because real doctrine prose trips them constantly.

**What this finding does NOT claim.** The detector is not "useless." Within its v0.1.1 ADVISORY role for founder_romance and HIGH role for the two narrow patterns, it provides a real signal on the subset of prose where regex anchors line up. The detector also continues to serve as a no-LLM, zero-latency hint surface, which an LLM-based reviewer cannot do. What this finding establishes is that the regex cannot bear HIGH severity for `founder_romance` on real doctrine prose at v0.1's threshold settings.

## Pre-registered hypothesis (locked before v1 runs)

The 7 patterns in v0.1 are regex-based and therefore brittle to paraphrase. An adversary LLM that knows the pattern definition will produce prose that (a) a careful reviewer catches as the same observer-bias the pattern is named for, but (b) the detector misses. **Falsifier:** ≥3 true evasions per pattern, or ≥1 evasion in ≥4 patterns → structural rework of the spec. **Null result:** 0 evasions across 120 trials → detector ships v0.1 as-is.

True evasion = detector miss + judge=yes + Hans audit confirms (10% stratified sample, 12 cases, ≤2 dissents acceptable).

Pre-reg lives at `funkytown/experiments/11_adversary_fuzz/README.md`.

## v1 run — adversary explicitly told regex anchors (2026-05-30 15:30 UTC)

**Setup:** 6 patterns × 20 drafts × `claude-sonnet-4-6` adversary (temperature=0.9). System prompt told the adversary the *pattern definition* AND the *regex anchors* AND instructed "exhibit the bias while paraphrasing around the anchors." Judge: `claude-sonnet-4-6` (temperature=0.0, same family as adversary).

**Result:**

| Pattern | Detector caught | Detector missed | Claude-judge yes (candidate evasion) |
|---|---|---|---|
| founder_romance | 0/20 | 20 | 20 |
| over_claim | 0/20 | 20 | 20 |
| stage_7_revival | 0/20 | 20 | 19 |
| schedule_prose_substitution | 0/20 | 20 | 20 |
| carve_out_construction | 0/20 | 20 | 20 |
| optimistic_probability | 2/20 | 18 | 18 |
| **Total** | **2/120 (1.7%)** | **118** | **117 (98%)** |

Cost: $0.91. Wall time 2.5 min. Pre-audit decision flags triggered: broaden all 6 patterns + structural rework.

Raw data: `funkytown/experiments/11_adversary_fuzz/runs/20260530T153006Z/`.

## Grok-4 pressure-test of v1 → "retract"

Sent v1 result + 12 stratified-audit cases + the 6 pattern definitions + regex anchors + pre-reg + decision rules to Grok-4 for cold-read external review. Three structural attacks, all material:

1. **Adversary-prompt rigging.** "The current setup is equivalent to giving a student the grading rubric and then grading them on whether they can avoid the rubric's bullet points." Fair test gives only the bias definition.
2. **Judge bias.** Same-family judge (Sonnet 4.6 judge on Sonnet 4.6 adversary output). On a 6-case re-audit, Grok concurred with the Claude-judge on 4/6 and dissented on 2/6 = 33% disagreement, over the pre-reg's 20% acceptance bar. Judge unreliable as a screen.
3. **Frame confusion.** Conflates "regex misses paraphrase" (expected for a first-line check) with "detector is broken" (stronger claim). The experiment never measured baseline catch rate on real non-adversarial prose, so cannot speak to operational utility.

**Grok's v1 verdict:** Retract. Smallest supported claim: *"A Sonnet-4.6 adversary explicitly told the regex anchors can reliably produce 118/120 paraphrases that also fool a second Sonnet-4.6 judge."*

Full pressure-test response: `funkytown/experiments/11_adversary_fuzz/runs/20260530T153006Z/grok_pressure_test.md`.

## v2 run — fair adversary + cross-family Grok-4 judge (2026-05-30 15:42 UTC)

Accepted Grok's first two structural attacks. Re-ran with corrections:

- **Adversary prompt:** definition only, NO regex anchors, NO "evade" instruction. Just "exhibit the pattern in plausible founder voice; vary phrasing across drafts."
- **Judge:** Grok-4 via xAI API (temperature=0.2). Cross-family.

Same 120 trials, same detector, same true-evasion definition.

**Result:**

| Pattern | v1 caught | **v2 caught** | v2 Grok-yes evasions |
|---|---|---|---|
| founder_romance | 0/20 | 1/20 | 19 |
| over_claim | 0/20 | 11/20 | 9 |
| stage_7_revival | 0/20 | 1/20 | 19 |
| schedule_prose_substitution | 0/20 | 0/20 | 20 |
| carve_out_construction | 0/20 | 2/20 | 18 |
| optimistic_probability | 2/20 | 9/20 | 11 |
| **Total** | **2/120 (1.7%)** | **24/120 (20%)** | **96/120 (80%)** |

Cost: $0.73. Wall time ~2 min.

Detector catch rate moved 1.7% → 20% — order-of-magnitude shift. **The v1 result was inflated by exactly that factor.** Grok's first attack (the rigging critique) was load-bearing.

Grok-4 returned `yes` on all 96 detector misses. Per-rationale spot-check: substantive on most (Cases 7-8 explicitly isolate the small-N-to-universal extrapolation and the pilot-to-portfolio leap); one was rote (Case 5). Grok concedes his own judging is "tighter than the v1 Claude outputs" but not perfectly so.

Raw data: `funkytown/experiments/11_adversary_fuzz/runs/20260530T154245Z_v2/`.

## Grok-4 pressure-test of v2 → "hold in scope-narrowed form"

Sent v2 result + delta-from-v1 + audit sample back to Grok. He retracted v1's "retract" verdict and refined:

1. **Rigging critique closed.** v2 drafts show no anchor leakage.
2. **Judge bias self-audit.** Conceded; tighter than v1 Claude but not perfect.
3. **The 20% catch rate is bimodal.** Driven entirely by `over_claim` (11/20) and `optimistic_probability` (9/20), whose absolute verbs and numeric anchors are hard to paraphrase. The other four patterns stay near zero. *Uniform decision-rule application is unwarranted.*
4. **Baseline-rate gap still unaddressed.** Minimum additional measurement: detector pass over last ~200 real doctrine commits.

**Grok's v2 final verdict (verbatim, last paragraph):**

> The corrected experiment demonstrates that the regex set is reliably evadable for `founder_romance`, `stage_7_revival`, `schedule_prose_substitution`, and `carve_out_construction` under definition-only adversarial pressure (Cases 3, 4, 9, 10, 11, and 12 are representative), while retaining useful signal on `over_claim` and `optimistic_probability`; the appropriate action is therefore to demote the four flexible patterns to advisory severity, log overrides, and make the Grok cold-read the documented first-line gate for those patterns rather than triggering a full structural rework of the detector.

Full response: `funkytown/experiments/11_adversary_fuzz/runs/20260530T154245Z_v2/grok_pressure_test_v2.md`.

## Baseline scan over 104 real doctrine commits (2026-05-30 15:50 UTC)

Closed Grok's third attack. Walked every commit since 2026-03-01 in `the-builders-doctrine` that touched a `.md` file, scanned the post-commit state of each modified file, applied the production exclude list, tabulated.

**Headline numbers:**

- Commits scanned: 104 (every `.md`-touching commit since 2026-03-01)
- Files scanned: 153 (after exclusions: 23 excluded per `.pre-commit-config.yaml`)
- **Operational block rate under v0.1: 35.6%** (37/104 commits would have been blocked by ≥1 HIGH finding)
- Any-finding rate: 89.4% (93/104)
- Total findings: 870 (56 HIGH, 814 ADVISORY)

**Per-pattern HIGH findings (the v0.1 blocking surface):**

| Pattern | HIGH findings | Share of HIGH | Comment |
|---|---|---|---|
| founder_romance | 53 | 95% | dominant noise source |
| carve_out_construction | 2 | 4% | narrow, real |
| stage_7_revival | 1 | 2% | rare; sole hit was on the Stage-7 replication pre-reg itself |

**Per-pattern ADVISORY findings:**

| Pattern | ADVISORY findings | Comment |
|---|---|---|
| over_claim | 397 | strong-verb without nearby measurement; ~2.6/file |
| founder_romance/1c | 347 | bio-adjacency; broad regex |
| optimistic_probability | 66 | $/percent/projection without grounding |
| schedule_prose_substitution | 4 | rare in real prose |

**Precision spot-check** (3 findings × 6 patterns; eyeballed by the experimenter):

- founder_romance/1a `THE_BUILDERS_DOCTRINE.md:227` ("the builder who installed the governor already survived worse") — **TP**.
- founder_romance/1c `THE_BUILDERS_DOCTRINE.md:48` (lived-experience → "psychology is in the product") — **borderline**. Doctrine's central thesis trips its own detector. Cannot be distinguished from unintentional bias by regex.
- carve_out_construction `REFUSAL_PROPAGATION_OFFRAMP_SPEC.md:253` — **FP**. Table row listing carve-out as a forbidden pattern, not committing one.
- stage_7_revival `LAW_VI_PRE_REG_v1.md:2` — **FP-in-context**. The file's purpose is to formally replicate Stage 7; deprecation framing exists upstream, not in the regex proximity window.
- over_claim "validated" hits at STARTUP.md, RELEASE_NOTES_v1.0.md, OPERATOR_DOGFOOD_ASYMPTOTE — **FPs** (measurement present but outside the regex proximity window).
- optimistic_probability "$53K", "$2K", "90% across 30 commits" — **FPs** (all real measured numbers).

Of 4 HIGH-severity findings in the precision sample, 1 is a clean TP, 3 are FPs (or FP-in-context). Rough HIGH precision: **~25%**, below the spec's ≥60% bar in `Success criteria §2`.

Raw data: `funkytown/experiments/11_adversary_fuzz/runs/20260530T155033Z_baseline/`.

## Synthesis — what survives, what changes

The baseline data **partly confirms and partly inverts Grok's v2 verdict.**

**Confirms:**
- `founder_romance` cannot bear HIGH severity. Block rate 35.6%, HIGH precision ~25%, doctrine's central thesis trips its own detector. Demotion to ADVISORY is the spec's own remedy under its `Success criteria §"If founder_romance precision/recall fails"` path.
- Grok cold-read should be the formal first-line gate for `founder_romance` until retuning.

**Inverts:**
- Grok v2 wanted `over_claim` and `optimistic_probability` promoted to HIGH (because their adversarial catch rate is highest, ~11/20 and 9/20). **Baseline data kills this.** These patterns already fire 397 and 66 times across 104 commits at ADVISORY. Promotion would push commit-block rate above 80% — operationally unworkable. Their high catch rate under adversarial pressure reflects regex traction on broad lexical fields, not absence of FPs on real prose.

**Confirms (narrow):**
- `stage_7_revival` and `carve_out_construction` keep HIGH. Both fire rarely in baseline (1 and 2 HIGH respectively); both have structurally distinctive regex; the FP cases are file-specific (the replication pre-reg, the doctrine table that lists the patterns by name). Two file exclusions added rather than severity demotion.

## Patch (v0.1.1, shipped same session)

1. **Detector code** (`kit/chassis/founder_romance_detector.py`): `_detect_role_as_narrator` (1a) and `_detect_stoic_nco_register` (1b) emit `Severity.ADVISORY` instead of `Severity.HIGH`. Inline comments cite this finding.
2. **Tests** (`kit/chassis/test_founder_romance_detector.py`): three assertions updated to expect `ADVISORY` for 1a/1b. All 46 tests pass.
3. **Pre-commit-config** (`.pre-commit-config.yaml`): description updated; two file exclusions added — `LAW_VI_PRE_REG_v1.md` (Stage 7 replication pre-reg) and `REFUSAL_PROPAGATION_OFFRAMP_SPEC.md` (spec table that lists carve-out as a forbidden pattern). Also excludes this findings file from itself.
4. **Spec** (`kit/chassis/FOUNDER_ROMANCE_DETECTOR_SPEC.md`): version → v0.1.1. Status section rewritten with empirical basis. Severity table added under `Pattern definitions`. Override-mechanism section updated. Roadmap entries split into v0.1 (superseded) / v0.1.1 (shipped today) / v0.1.2 (TBD retuning).

## Post-patch verification

Re-ran the baseline scan against the same 104 commits after the v0.1.1 patch, with the baseline scan's exclude list synced to the updated `.pre-commit-config.yaml`:

| Metric | v0.1 (pre-patch) | **v0.1.1 (post-patch)** |
|---|---|---|
| Operational block rate (HIGH on ≥1 file in commit) | **35.6%** (37/104) | **0.0%** (0/104) |
| Any-finding rate (HIGH + ADVISORY) | 89.4% | 84.6% |
| HIGH findings by pattern | founder_romance 53, carve_out 2, stage_7_revival 1 | (none in non-excluded files) |
| ADVISORY findings by pattern | over_claim 397, founder_romance 347, optimistic 66, schedule 4 | over_claim 383, founder_romance 376, optimistic 66, schedule 4 |
| Files scanned | 153 (23 excluded) | 147 (29 excluded — two new file exclusions) |

The any-finding rate barely moves (advisory hints still emit on 84.6% of commits) because the patch was a severity demotion, not a regex change. Operational block rate goes to zero on the historical corpus, which is the desired v0.1.1 behavior — Grok cold-read is the formal first-line gate while the regex retunes.

Raw data: `funkytown/experiments/11_adversary_fuzz/runs/20260530T160043Z_baseline/`.

## Smallest claim the experiment supports

A regex-based observer-bias detector with the v0.1 anchors for `founder_romance` cannot bear HIGH severity in a pre-commit hook on the doctrine repo as of 2026-05-30: real doctrine prose trips the 1a + 1b regex at 35.6% of commits with ~25% HIGH precision, below the spec's stated ≥60% precision bar. Under fair adversarial pressure (definition-only adversary, cross-family judge), the v0.1 detector catches 20% of bias-exhibiting drafts; the remaining 80% are catchable by a cross-family LLM judge but not by the v0.1 regex. The structural conclusion is severity-stratified, not a full structural rework.

## What would kill this finding

1. **Baseline FPs are real TPs.** If the precision spot-check undercounts — e.g., the "FP-in-context" Stage-7 revival in `LAW_VI_PRE_REG_v1.md:2` is a real TP and the file SHOULD be blocked from committing without explicit deprecation framing in the regex window — then the block rate is more honest than the precision read. Spot-check sample size (n=4 HIGH) is small. A formal precision audit of all 56 HIGH findings is the next experiment.
2. **20% v2 catch rate is an underestimate of real-prose performance.** If non-adversarial doctrine prose uses the regex anchors more honestly than the fair-adversary did (i.e., real founders use "the man who" instead of paraphrasing), the detector at HIGH severity may have caught real bias at higher rates than 25% precision suggests. The baseline-rate precision sample is too small to falsify this.
3. **The Grok-4 judge has its own systematic bias toward "yes."** Spot-check found one rote rationale (Case 5). A formal cross-judge experiment (replicate v2 with a third judge — GPT-5 or Llama 3.1) would establish whether the 96/96 yes rate is real cross-family agreement or a Grok-specific permissiveness.

If any of these turn out true, the v0.1.1 patch is reversible in one commit (re-elevate 1a/1b to HIGH).

## Follow-ups (not done in this session)

- **v0.1.2 corpus assembly.** Use the 104-commit baseline scan output as the source for a labeled corpus (caught / clean / mixed) — Hans hand-labels a stratified sample of ~30 findings per pattern, retune regex thresholds, target ≥60% HIGH precision before re-promoting any pattern.
- **Formal precision audit of all 56 HIGH findings.** Brief task — ~30 min Hans audit on the full HIGH set, not a 4-case spot-check.
- **Third-judge robustness check.** Replicate v2 with GPT-5 or Llama 3.1 as a third independent judge; measure cross-family agreement rate beyond Sonnet→Grok.
- **Strategic-layer founder-romance probe (Exp 11b candidate).** Time-invested justifications, proximity-to-GTM framings, repackaged-clean-negative-as-optionality. None of these are in the current spec. Exp 11b would generate adversarial drafts for the candidate patterns and assess whether they extend the detector beyond prose-level into strategic-decision text.
- **`tame_reviewer_drift`** still NotImplemented. Out of v0.1.1 scope.

## Reproducibility

All artifacts under `funkytown/experiments/11_adversary_fuzz/`:

- `README.md` — pre-registered hypothesis + design + decision rules
- `src/adversary_prompts.py` — v1 + v2 adversary system prompts (v1 leaks anchors, v2 does not)
- `src/runner.py` — v1 runner (Sonnet adversary + Sonnet judge)
- `src/runner_v2.py` — v2 runner (Sonnet adversary, definition-only + Grok-4 judge)
- `src/build_audit_sample.py` — Hans audit sample generator
- `src/grok_pressure_test.py` — Grok-4 cold-read on v1
- `src/grok_pressure_test_v2.py` — Grok-4 cold-read on v2
- `src/baseline_scan.py` — 104-commit baseline scan with precision spot-check sample
- `runs/20260530T153006Z/` — v1 run artifacts (drafts.jsonl, scans.jsonl, judge.jsonl, summary.json, audit_sample.md, grok_pressure_test.md)
- `runs/20260530T154245Z_v2/` — v2 run artifacts (same shape, + grok_pressure_test_v2.md)
- `runs/20260530T155033Z_baseline/` — baseline scan results (scan_results.json, scan_results.md, findings_sample.jsonl, per_commit.jsonl)

Total experimental cost: $1.64 ($0.91 v1 + $0.73 v2 + baseline scan is detector-only, no API). Total wall time: ~12 minutes of compute over a ~90-minute session.
