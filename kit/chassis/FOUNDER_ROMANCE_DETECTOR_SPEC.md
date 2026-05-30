# Founder-Romance Detector — Spec v0.1.1

**Status:** v0.1.1 SHIPPED 2026-05-30. **Severity change from v0.1:** `founder_romance` 1a + 1b demoted HIGH → ADVISORY per Exp 11 (funkytown experiment 11) baseline scan + Grok-4 v2 pressure-test. HIGH-severity findings now ship only from `stage_7_revival` + `carve_out_construction`. Two new file exclusions added for legitimate-purpose Stage-7 / carve-out narration (`LAW_VI_PRE_REG_v1.md`, `REFUSAL_PROPAGATION_OFFRAMP_SPEC.md`). Full empirical record at `kit/chassis/findings_adversary_v1.md`.

**v0.1 (superseded):** SHIPPED 2026-05-20. founder_romance 1a/1b HIGH + 1c ADVISORY; corpus benchmark passing on a 10-file test set. The 49-file field validation flagged the false-positive class but did not force severity revision — Exp 11 baseline scan did.

**Replaces:** Adversarial Review chassis (RETRACTED 2026-05-19 — see `archived-prose/2026-05-19_adversarial_review_pre_reg_v1_KILLED.md`)
**Original commitment:** `feedback_close_up_this_session.md` round-7, 2026-05-13
**Authority:** advisory. The detector names threats; the human decides. Pre-commit hook can be overridden with logged reason.

**v0.1.1 empirical basis (Exp 11, 2026-05-30):** 120-trial fair-adversary fuzz (Sonnet 4.6 adversary given pattern definition only, no regex-anchor leak) + Grok-4 cross-family judge: detector caught **24/120 (20%)** of adversarial drafts; Grok-4 confirmed 96/96 detector misses as candidate evasions. Baseline scan over 104 real .md commits in this repo since 2026-03-01: **35.6% commit-block rate** under v0.1 (37/104 commits would have been blocked by `founder_romance` HIGH findings) with ~25% HIGH precision on a 4-finding spot-check. The block-rate × precision combination triggers this spec's own "ship-disabled + tune in v0.1.x" path for founder_romance. v0.1.1 demotes 1a + 1b to ADVISORY to close the block-rate gap without losing the advisory signal; v0.1.2+ will retune the regex against a corpus of caught-vs-clean doctrine prose before re-promotion is considered.

**Grok cold-read is the formal first-line gate for founder_romance** until v0.1.2+ regex retuning. The regex is a hint; the human reviewer is the gate.

**Two non-changes from v0.1:** Per Exp 11 finding §"What the baseline data kills," do NOT promote `over_claim` or `optimistic_probability` to HIGH severity — baseline showed 397 + 66 ADVISORY findings respectively across 104 commits; promotion would push block rate above 80%. Their adversarial evasion rate (under fair-test) reflects regex limits on broad lexical fields, not a precision failure to gate at HIGH.

---

## Name vs. scope

The module name says "founder-romance," but the v0.1 scope covers all seven patterns in the observer-bias taxonomy first listed in the retracted Adversarial Review §1 spec. The name is preserved because (a) founder-romance is the primary pattern, (b) the round-7 commitment used this name, and (c) all six sibling patterns share the same mechanism: a builder's blind spot about prose the builder produced. Renaming to "doctrine_bias_detector" is a defensible v0.2 move; v0.1 keeps the historical name.

## Purpose

Scan doctrine-repo artifacts (Markdown, primarily) for prose patterns associated with caught founder-romance and observer-bias incidents. Surface findings at pre-commit time so the founder must either revise the prose or explicitly override with a logged reason. The detector is regex-and-heuristic; it does not use an LLM. Coverage is best-effort — patterns that require semantic reasoning ship as heuristic stubs with documented false-positive/false-negative profiles.

## Architecture

```
kit/chassis/
├── founder_romance_detector.py     # patterns, Finding dataclass, scan()
├── test_founder_romance_detector.py
├── test_corpus/                    # ≥10 legacy artifacts (positive + negative)
│   ├── manifest.yaml               # ground truth: which patterns each file should fire
│   └── *.md                        # snippets from caught/clean prose
└── FOUNDER_ROMANCE_DETECTOR_SPEC.md (this file)

.pre-commit-config.yaml             # hook entry (added when v0.1 ships)
```

The module exposes:

- `Pattern` (Enum) — the seven pattern identifiers
- `Finding` (dataclass) — `pattern`, `severity`, `excerpt`, `line_number`, `file_path`, `rationale`
- `scan(text: str, *, file_path: str | None = None) -> list[Finding]` — primary entry point
- `cli main()` — reads files from argv or stdin, emits findings to stderr, exits 1 if any high-severity findings

## Pattern definitions (v0.1.1)

All seven patterns from the retracted Adversarial Review §1 taxonomy. Each entry: name, definition, regex/heuristic approximation, expected precision/recall profile against the corpus.

**Severity table (v0.1.1):**

| Pattern | v0.1 severity | v0.1.1 severity | Reason |
|---|---|---|---|
| 1a `founder_romance/role-as-narrator` | HIGH | **ADVISORY** | Exp 11 baseline: 35.6% block rate, ~25% HIGH precision. Doctrine prose itself argues from biography. |
| 1b `founder_romance/stoic-NCO register` | HIGH | **ADVISORY** | Same FP class as 1a. |
| 1c `founder_romance/bio-adjacency` | ADVISORY | ADVISORY | unchanged |
| 2 `over_claim` | ADVISORY | ADVISORY | unchanged; do NOT promote (397 baseline ADVISORY findings) |
| 3 `stage_7_revival` | HIGH | HIGH | unchanged; narrow regex, structurally distinctive |
| 4 `schedule_prose_substitution` | ADVISORY | ADVISORY | unchanged |
| 5 `carve_out_construction` | HIGH | HIGH | unchanged; narrow regex, structurally distinctive |
| 6 `optimistic_probability` | ADVISORY | ADVISORY | unchanged; do NOT promote (66 baseline ADVISORY findings) |
| 7 `tame_reviewer_drift` | NotImplemented | NotImplemented | unchanged |

### 1. `founder_romance`

**Definition.** A sentence where a biographical fact about the founder is positioned to bear doctrinal weight without an intervening measurement bridge. Form: `[biographical clause] → [doctrinal claim]` adjacency within two sentences.

**v0.1.1 severity:** ADVISORY for all three sub-checks (1a, 1b, 1c). Demoted from v0.1's HIGH severity for 1a/1b per Exp 11 baseline scan. Grok cold-read is the first-line gate for this pattern until v0.1.2+ retuning.

**v0.1 detection.** Three regex sub-checks:

- **1a. Biographical-voice closer.** Sentences containing role-as-narrator markers: `\b(the (man|marine|nco|sergeant|veteran|founder|builder) who)\b/i`, `\b(having (served|stood|carried|survived))\b/i`, `\bI(?:'ve)? (stood|carried|served) (post|the line|the weight)\b/i`. High precision, moderate recall.
- **1b. Stoic-NCO register.** Phrases borrowed from military doctrine register and used to lend authority to a non-empirical claim: `\b(stand post|hold the line|in the breach|under fire|at the wire|chain of command)\b/i` within 80 characters of a doctrinal claim verb (`is|requires|must|shall|the framework`). Moderate precision; flags some legitimate usage and requires human review.
- **1c. Bio-to-doctrine adjacency.** A sentence containing biographical markers (`USMC|Marine|Guard|combat|tour|deployment|brewery|founder|veteran|sober`) followed within two sentences by a doctrine-load-bearing clause (`Law (V|VI|VII|VIII|IX|X)|the doctrine|the framework holds|the principle`). Lower precision (legitimate cross-references will trigger); always advisory.

**Profile.** Target ≥70% recall, ≥60% precision on the corpus.

### 2. `over_claim`

**Definition.** A finding presented at a confidence level the underlying measurement cannot support. Examples: N=1 result stated as general claim; engineering-scaffold output cited as rung-3 validation evidence.

**v0.1 detection.** Heuristic stub. Regex flags:

- Strong claim verbs (`proves|demonstrates|confirms|validates|establishes`) without nearby measurement-quality markers (`N=\d+|sample of \d+|across \d+ runs|baseline|control`).
- N=1 / N=2 / N=3 results paired with absolute-claim language (`always|never|in all cases|the pattern is`).

**Profile.** Low precision expected — many false positives. Documented as advisory-only. The reliable detector for over_claim is the Grok cold-read; the regex is a hint, not a gate.

### 3. `stage_7_revival`

**Definition.** A doctrinal claim that was previously deprecated reappearing without reference to the deprecation. Specific to the Funkytown 01 Stage 7 Law I causal claim (deprecated 2026-05-13).

**v0.1 detection.** Regex for revived deprecated phrases: `\b(Stage 7|stage seven) (Law I|causal claim|biographical[- ]substrate finding|2/3 refusals)\b/i` without a same-paragraph deprecation marker (`deprecated|withdrawn|retracted|RETRACTED|see also.*2026-05-13`).

**Profile.** Narrow but high precision when it fires. Covers one specific historical claim; will need maintenance as the deprecation list grows.

### 4. `schedule_prose_substitution`

**Definition.** A dated commitment presented as if it were the work itself. "By 2026-05-25 we will ship X" presented as evidence X is shipping, with no measurement gate.

**v0.1 detection.** Regex for date + commitment verb + absence-of-measurement-clause:

- Pattern: `\b(20\d\d-\d{2}-\d{2}|by [A-Z]\w+ \d+)\b.{0,80}\b(ship|deliver|complete|finalize|publish|commit)\b` not followed within the same paragraph by a measurement clause (`measured|tested|with N=|validated against|falsification criterion`).

**Profile.** Moderate precision. Many legitimate schedule entries will trigger; advisory.

### 5. `carve_out_construction`

**Definition.** Doctrinal carve-out language that creates an exception for the founder or for a specific class of artifact the founder produced. The Law X carve-out attempt (caught 2026-05-13) is the canonical example.

**v0.1 detection.** Regex: `\b(except|unless|exempt|excluding)\s+(when|where|if|in cases?|for (the )?(founder|builder|originator|author))\b/i`. Also: `\bnot subject to (Law|the principle|the doctrine)\b/i`.

**Profile.** High precision (carve-out language is structurally distinctive). Moderate recall — sophisticated carve-outs are paraphrased and slip past regex.

### 6. `optimistic_probability`

**Definition.** Probability or projection claims that are not grounded in measurement. Round-6 Grok dialogue's $27M valuation packet is the canonical example.

**v0.1 detection.** Regex for projection language without grounding:

- Pattern: `(\$\d+[MK]|\d+%|likely|probably|will (succeed|win|capture)|TAM|valuation)` paired with absence of grounding markers (`based on|measured from|comparable to|N=|baseline of`).

**Profile.** Low precision expected. Advisory-only stub.

### 7. `tame_reviewer_drift`

**Definition.** A reviewer (regex, LLM, or human) that grows progressively less adversarial across review cycles without doctrine improvement. Detected over time, not per-artifact.

**v0.1 detection.** **Not implemented in v0.1.** Requires cross-artifact memory + temporal analysis. v0.1 ships this pattern with a `NotImplemented` flag in the Pattern enum and a runtime warning. v0.2 candidate: cross-reference catch-ledger entries in `feedback_grok_second_opinion_workflow.md`.

---

## Success criteria (corpus benchmark)

A corpus of ≥10 legacy artifacts lives in `test_corpus/`. Each entry is a Markdown snippet with a frontmatter manifest entry declaring:

```yaml
file: caught_funkytown_03_mvp_pre_retraction.md
status: caught       # caught | clean | mixed
patterns:            # patterns that SHOULD fire on this file
  - over_claim
  - schedule_prose_substitution
```

The detector earns v0.1 ship when:

1. **`founder_romance` recall ≥ 70%** against corpus-positive entries.
2. **`founder_romance` precision ≥ 60%** against corpus-negative entries.
3. **`carve_out_construction` precision ≥ 75%** (this pattern is structurally distinctive and should be high-precision).
4. The other patterns ship as **advisory-only** with no precision/recall threshold. They are documented as "hint" patterns and the human reviews each finding.

If `founder_romance` precision/recall fails, v0.1 ships disabled and the regex patterns are tuned against the corpus in v0.1.1 before the pre-commit hook is enabled in production.

## Override mechanism

The pre-commit hook fails on any **high-severity** finding. As of v0.1.1 that means `carve_out_construction` and `stage_7_revival` only. `founder_romance` 1a + 1b were HIGH in v0.1 but were demoted to ADVISORY per Exp 11. All other findings emit a warning and exit 0.

The founder can override a failing hook with:

```
git commit --no-verify -m "<message>

OVERRIDE: founder_romance_detector flagged biographical-closer in CHASSIS_EXTENSIONS.md §3.
Reviewed; this is a Law-VII falsification entry that legitimately cites lived experience as
falsification evidence rather than as doctrinal substantiation. Logged.
"
```

The override reason is captured in commit-message convention — not a separate log file (yet). v0.2 candidate: append override reasons to `OVERRIDE_LOG.md` automatically via post-commit hook.

## Out of scope (v0.1)

- LLM-based semantic analysis (the chassis that would have done this was RETRACTED 2026-05-19).
- Cross-artifact memory (`tame_reviewer_drift`, doctrine-claim consistency across commits).
- Second-reviewer rotation. The round-7 commitment named rotating human reviewers (Brad on commercial, statistician on empirical, veteran-founder peer on biographical prose); that's a separate process artifact, not detector code.
- Auto-correction of flagged prose. Detector is read-only.

## Roadmap

- **v0.1** (shipped 2026-05-20, superseded 2026-05-30) — patterns 1, 3, 5 HIGH; patterns 2, 4, 6 ADVISORY; pattern 7 stub.
- **v0.1.1** (shipped 2026-05-30) — Pattern 1 (founder_romance) 1a + 1b demoted HIGH → ADVISORY per Exp 11 baseline scan. Two file exclusions added (`LAW_VI_PRE_REG_v1.md`, `REFUSAL_PROPAGATION_OFFRAMP_SPEC.md`). Empirical record at `findings_adversary_v1.md`.
- **v0.1.2** (TBD) — retune founder_romance regex against a baseline-derived corpus of caught-vs-clean doctrine prose. Target: ≥60% HIGH precision before any re-promotion. Pre-req: enlarged corpus assembled from the 104-commit baseline scan output.
- **v0.2** — `OVERRIDE_LOG.md` auto-append; broaden corpus to ≥25 entries; add 2nd-reviewer rotation hook stubs.
- **v0.3** — extend to product repos (TOP, Operator, Custer). Each product carries its own patterns file.
- **Not roadmap:** LLM-as-reviewer chassis. That path was closed 2026-05-19. Future expansion stays regex-and-heuristic.

## What this detector does NOT replace

Grok cold-read remains the load-bearing audit gate (per `feedback_grok_second_opinion_workflow.md`). The regex detector is the first-line check; Grok is the deep check. If the detector ever begins to feel like the audit gate, the detector has failed and Grok is still the audit. See the Adversarial Review retraction for the precedent — the workflow does not get to stop being needed.
