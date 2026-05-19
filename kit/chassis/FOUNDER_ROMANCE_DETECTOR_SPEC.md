# Founder-Romance Detector — Spec v0.1

**Status:** in build (Phase 1 deliverable, slot 2026-05-25)
**Replaces:** Adversarial Review chassis (RETRACTED 2026-05-19 — see `archived-prose/2026-05-19_adversarial_review_pre_reg_v1_KILLED.md`)
**Original commitment:** `feedback_close_up_this_session.md` round-7, 2026-05-13
**Authority:** advisory. The detector names threats; the human decides. Pre-commit hook can be overridden with logged reason.

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

## Pattern definitions (v0.1)

All seven patterns from the retracted Adversarial Review §1 taxonomy. Each entry: name, definition, regex/heuristic approximation, expected precision/recall profile against the corpus.

### 1. `founder_romance`

**Definition.** A sentence where a biographical fact about the founder is positioned to bear doctrinal weight without an intervening measurement bridge. Form: `[biographical clause] → [doctrinal claim]` adjacency within two sentences.

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

The pre-commit hook fails on any **high-severity** finding (currently: `founder_romance` 1a, `carve_out_construction`, `stage_7_revival`). All other findings emit a warning and exit 0.

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

- **v0.1** (this build) — patterns 1, 3, 5 high-severity; patterns 2, 4, 6 advisory; pattern 7 stub.
- **v0.1.1** — tune thresholds against corpus until success criteria pass.
- **v0.2** — `OVERRIDE_LOG.md` auto-append; broaden corpus to ≥25 entries; add 2nd-reviewer rotation hook stubs.
- **v0.3** — extend to product repos (TOP, Operator, Custer). Each product carries its own patterns file.
- **Not roadmap:** LLM-as-reviewer chassis. That path was closed 2026-05-19. Future expansion stays regex-and-heuristic.

## What this detector does NOT replace

Grok cold-read remains the load-bearing audit gate (per `feedback_grok_second_opinion_workflow.md`). The regex detector is the first-line check; Grok is the deep check. If the detector ever begins to feel like the audit gate, the detector has failed and Grok is still the audit. See the Adversarial Review retraction for the precedent — the workflow does not get to stop being needed.
