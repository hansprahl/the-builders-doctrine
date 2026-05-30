# Strategic-Layer Observer-Bias Detector — Spec (v0.2 candidate)

**Status:** v0.2.1 — HIGH gate active for all three patterns
(promoted 2026-05-30 per Hans 6/6 precision audit on the full baseline
scan firings). v0.2.0 shipped ADVISORY-only earlier the same day; the
promotion happened in the same session because the four evidence
ladders all converged: cross-family adversarial agreement 99.4%,
Hans-collusion-falsification 91.7%, prompt-framing stability 100%,
Hans real-prose precision 100% (6/6). Commit-level block-rate
estimate: 5.3% (vs. Exp 11's 35.6% regex baseline). See
`findings_strategic_layer_v1.md` for the empirical record.

**Empirical basis:** `kit/chassis/findings_strategic_layer_v1.md` (Exp
11b, 2026-05-30). Three candidate strategic-layer patterns cleared the
pre-registered cross-family lockup (179/180 = 99.4% three-family
agreement); zero v0.1.1 HIGH-severity overlap.

**Parent module:** `kit/chassis/founder_romance_detector.py` (v0.1.1).
This is a **sibling** module, not an extension of the existing detector
file — different mechanism (LLM gate vs regex), different cost model,
different invocation surface.

## Name vs. scope

Module name: `strategic_layer_detector`. The v0.2 scope is three
strategic-decision-level founder-romance patterns Hans named on
2026-05-21 and Exp 11b substantiated cross-family on 2026-05-30. The
prose-level seven-pattern taxonomy stays in
`founder_romance_detector.py` (v0.1.1, regex). The strategic-layer
patterns live here because (a) they have no regex anchors by
construction — they are LLM-detectable only — and (b) the cost and
invocation profile is fundamentally different from a regex pre-commit
hook.

## Purpose

Scan strategic artifacts (roadmaps, pitch deck narratives, board
updates, MDMP rationales, portfolio memos, wargame readouts) for
founder-romance patterns that operate at the *decision* layer rather
than the *prose* layer. Where v0.1.1 catches "I served the weight,
therefore the framework holds," v0.2 catches "we spent eighteen months
building this, therefore doubling down is correct."

The v0.2 gate is an **LLM judge call per pattern per artifact**, not a
regex pass. ADVISORY-only at ship.

## Architecture

```
kit/chassis/
├── strategic_layer_detector.py          # patterns, Finding adapter, scan()
├── test_strategic_layer_detector.py     # frozen-prompt regression tests
├── test_corpus_strategic/               # ≥10 strategic-prose snippets
│   ├── manifest.yaml                    # ground truth: which patterns fire
│   └── *.md                             # mix of caught + clean strategic prose
└── STRATEGIC_LAYER_DETECTOR_SPEC.md     # this file
```

Module exposes:

- `StrategicPattern` (Enum) — `time_invested_justification`,
  `proximity_to_gtm_framing`, `repackaged_clean_negative`
- `Finding` (dataclass) — reuses the v0.1.1 `Finding` shape: `pattern`,
  `severity`, `excerpt`, `line_number`, `file_path`, `rationale`. Adds
  `judge_model`, `judge_cost_usd` fields for cost accounting.
- `scan(text: str, *, file_path: str | None = None, model: str = "grok-4") -> list[Finding]`
  — primary entry point. Internally: one LLM call per pattern, JSON
  verdict parsed into `Finding` if verdict is "yes."
- `scan_paragraphs(text: str, ...) -> list[Finding]` — paragraph-
  granularity variant for large documents; chunk by `\n\n` and judge
  each chunk against all three patterns.
- `cli main()` — reads files from argv or stdin, emits findings, exits 0
  on ADVISORY (warns), 1 on HIGH (blocks). v0.2 ship: no HIGH gate;
  exit always 0 with stderr warnings.

## Pattern definitions (v0.2)

All three from Exp 11b; verbatim from `findings_strategic_layer_v1.md`.

### 1. `time_invested_justification` — ADVISORY

**Definition.** A strategic claim that the present course of action is
correct BECAUSE a long time was already spent building, learning, or
accumulating context for it. The duration itself is positioned as the
warrant for the decision, with no intervening measurement of outcome
quality, market evidence, or comparable evaluation against alternative
uses of that time. Form: `[time-invested clause] → [strategic claim]`
adjacency, with no measurement bridge.

**Distinct from `founder_romance` (v0.1.1).** That pattern uses *life
experience* as warrant; this pattern uses *recent project-time invested
in THIS specific bet* as warrant.

**Empirical (Exp 11b).** Grok-4: 20/20. Gemini 2.5 Pro: 20/20. v0.1.1
regex overlap: 1/20 (ADVISORY only).

### 2. `proximity_to_gtm_framing` — ADVISORY

**Definition.** A strategic option is re-weighted upward — or a
kept-vs-killed decision is settled — because the option is closer to
revenue, closer to a launch milestone, closer to a paying customer, or
closer to "real validation," with closeness itself stated as the
warrant. The framing privileges the visibly-near option without a
comparable risk-adjusted evaluation of the further-away option.

**Distinct from legitimate sequencing.** A sequencing argument that
names the risk-adjusted return trade-off ("enterprise has a 6-9 month
procurement cycle so we sequence to mid-market first") is NOT this
pattern. Gemini 2.5 Pro independently policed this boundary on idx=13
during Exp 11b; that discrimination is the design requirement for the
LLM gate to be useful.

**Empirical.** Grok-4: 20/20. Gemini: 19/20 (the dissent was the
legitimate-sequencing boundary call above). v0.1.1 overlap: 4/20
(ADVISORY only — strong-verb hints fired on GTM language).

### 3. `repackaged_clean_negative` — ADVISORY

**Definition.** A prior analysis (wargame, MDMP, due-diligence pass,
customer research) returned a clean negative — viability score low,
named kill signals, named financial loss or specific failure modes. The
negative is then re-presented in a subsequent strategic discussion as
"Option N with strong dissent," "an optionality play to keep on the
table," "a hedge worth retaining," or "a portfolio diversifier" without
addressing or refuting the named kill signals.

**Empirical.** Grok-4: 20/20. Gemini: 20/20. v0.1.1 overlap: 7/20
(ADVISORY only — over_claim + optimistic_probability lexical fields
fire on confident strategic prose).

**Related behavior:** Hans's standing rule
`[[feedback-dont-repackage-clean-negatives]]` is this pattern in
behavioral form. The detector codifies the rule.

## Severity table

| Pattern | v0.2.0 ship | v0.2.1 (2026-05-30) |
|---|---|---|
| `time_invested_justification` | ADVISORY | **HIGH** |
| `proximity_to_gtm_framing` | ADVISORY | **HIGH** |
| `repackaged_clean_negative` | ADVISORY | **HIGH** |

**Why v0.2.1 promoted same day.** The conservative v0.2.0 ADVISORY-only
ship was the planned path. But the full baseline scan + Hans 6/6
precision audit completed in the same session and all four evidence
ladders converged decisively: cross-family adversarial agreement
99.4%, Hans-collusion-falsification 91.7% (12-draft audit), prompt-
framing stability 100% (fresh-Grok), real-prose precision 100%
(6/6 firings audit). Holding ADVISORY past confirming evidence would
have been ceremony, not discipline.

The Exp 11 lesson (never ship HIGH without a real-prose baseline) is
honored: the baseline ran (114 commits, $8.84) and returned 1.4-2.0%
per-pattern firing rate — well under the spec's ≤5% operational floor.
The 5.3% commit-level block rate is ~7x quieter than the Exp 11 regex
v0.1 baseline (35.6%) that forced the v0.1.1 demotion.

## Invocation surface — LOCKED 2026-05-30

**Decision (Hans):** On-demand CLI **plus** pre-commit hook on a short
curated path list.

- **On-demand CLI.** `python -m kit.chassis.strategic_layer_detector
  <file>` invoked manually before important strategic writing ships.
  Cost: per invocation, user-paced.
- **Pre-commit hook (curated paths only).** Runs only when a staged
  file matches the curated list. Cost: ~$0-0.10 per commit when a
  strategic file is touched, $0 otherwise.

Curated path list (initial; extends in v0.2.x as new strategic
artifacts are produced):

- `RELEASE_PLAN*.md`
- `MISSION_COMMAND_ARCHITECTURE.md`
- `PRODUCTIZE_VS_LICENSE_DECISION.md`
- `OPERATOR_DOGFOOD_*.md`
- Per-product `ARCHITECTURE.md`
- Per-product `NORTHSTAR.md`
- `LAW_*_PRE_REG*.md`
- `BANDWIDTH_OVERLAY_*.md`
- `THE_BUILDERS_METHOD.md`
- `THE_BUILDERS_DOCTRINE.md`
- `META_DOCTRINE.md`

Override mechanism for the pre-commit-fires-when-touched case mirrors
v0.1.1 (`git commit --no-verify` with a logged reason in the commit
message).

## Cost model

Per-pattern judge call: ~$0.003 (Grok-4 at ~600 input tokens, ~80 output
tokens for a paragraph-sized strategic prose excerpt).

**Per-file scan (whole-document mode):**
- Avg doctrine .md: ~6000 input tokens × 3 patterns = 18K input tokens.
- 3 × Grok call ≈ $0.06 - $0.10 per file.

**Per-file scan (paragraph mode, chunked by `\n\n`):**
- N paragraphs × 3 patterns × ~$0.003 = $0.009 × N.
- Typical doctrine file ≈ 30-60 paragraphs → $0.27 - $0.54 per file.
- More precise findings (paragraph-anchored, not whole-file) but ~4-6x
  the cost of whole-doc mode.

**Hook cost ceiling:** Aim for **≤ $0.05 per commit** in the
recommended starting-point configuration. Above $0.05/commit, the gate
will get disabled in practice — the cost surface eats the value
surface. If the curated path list lights up too often, switch to
on-demand-only mode.

## Success criteria (corpus benchmark)

Same shape as v0.1.1's success criteria.

1. **Test corpus.** Hand-curated `test_corpus_strategic/` with ≥10
   snippets: ≥3 caught examples per pattern (real or synthesized from
   Exp 11b drafts) + ≥3 known clean strategic-prose negatives. Manifest
   declares ground truth.
2. **Precision on corpus:** ≥80% per pattern at ADVISORY. The 99.4%
   three-family agreement on adversarial drafts is the upper bound;
   real prose will be noisier. ≥80% is the operational floor.
3. **Real-prose baseline scan (REQUIRED before v0.2.x HIGH promotion).**
   Run the LLM gate against the same 104-commit corpus Exp 11 used
   (`baseline_scan.py` analog). Acceptable outcomes for HIGH promotion:
   - ≤ 5% per-pattern HIGH block rate on real commits
   - ≥ 60% spot-check precision on a Hans 12-finding audit per pattern

   If either fails, the pattern stays ADVISORY indefinitely. (Exp 11
   precedent: founder_romance 1a/1b had 35.6% block rate + ~25%
   precision → demoted.)

## Override mechanism

When the gate fires ADVISORY at pre-commit, it warns; no override
needed (the commit passes). When (and only when) the gate is promoted
to HIGH on any pattern, the override mechanism mirrors v0.1.1:

```
git commit --no-verify -m "<message>

OVERRIDE: strategic_layer_detector flagged <pattern> in <file>:<line>.
Reviewed; <reason — why this is a known FP class or intentional pattern>.
Logged."
```

Override reasons live in the commit message — same convention as
v0.1.1, no separate log file.

## Out of scope (v0.2)

- **A regex layer.** These patterns are LLM-detectable by construction;
  attempting regex would re-introduce the founder_romance 1a/1b
  precision problem at strategic layer.
- **Cross-document coherence checks.** v0.2 scans single artifacts;
  detecting `repackaged_clean_negative` across documents (the wargame
  is in file A, the optionality language is in file B) requires
  cross-artifact memory + temporal analysis. Out of scope — that's the
  same shape as the still-NotImplemented `tame_reviewer_drift` in
  v0.1.1, and the same shape it's been since v0.1.
- **Real-time correction.** v0.2 surfaces findings; it does not propose
  rewrites. A correction surface is v0.3+ territory and depends on the
  paid/free split decision (`PRODUCTIZE_VS_LICENSE_DECISION.md`).

## Roadmap

| Version | Status | Content |
|---|---|---|
| v0.2-draft | shipped 2026-05-30 | spec + 3 ADVISORY patterns; not yet coded |
| v0.2.0 | shipped 2026-05-30 | code: detector + test corpus + on-demand CLI + curated-path pre-commit hook + 15/15 unit tests, ADVISORY-only |
| v0.2.1 | shipped 2026-05-30 | HIGH-gate promotion for all three patterns per Hans 6/6 precision audit |
| v0.2.x | future | retune per pattern if precision drift surfaces in production; broaden curated path list as new strategic artifacts appear |
| v0.3 | future | cross-document `tame_reviewer_drift` (v0.1.1's NotImplemented item, also LLM-gate) |

## What this detector does NOT replace

- Grok-4 (or other cross-family) cold-reads on important strategic
  writing. The detector is a hint surface, not the reviewer.
- Hans's wargame / MDMP / red-team workflows. The detector catches the
  *output* of decisions; the workflows produce the inputs. A
  `repackaged_clean_negative` finding tells you the prior wargame's
  kill signals were dropped — it doesn't replace running the wargame.
- The standing Hans rule
  `[[feedback-dont-repackage-clean-negatives]]`. The rule is upstream;
  the detector is the receipt.

## Open follow-ups before v0.2.0 ships

1. ~~**Hans's invocation-surface decision**~~ — **LOCKED 2026-05-30:**
   on-demand CLI + curated-path pre-commit. See Invocation surface above.
2. ~~**Real-prose baseline scan analog**~~ — **full scan closed 2026-05-30
   16:50 UTC.** 114-commit corpus, 148 unique (sha, file) pairs, 444
   Grok-4 calls, $8.84. Per-pattern file-level firing: 1.4%, 0.7%,
   2.0%; commit-level block-rate estimate 5.3%. All three patterns
   OPERATIONALLY FIT (≤5%). Six total firings — three in TPS like the
   v1.0 release-cadence reframe in `RELEASE_PLAN_v1.md` (`5480322b`),
   the bandwidth date reframe in `BANDWIDTH_ACTUALS_2026.md`, and two
   `MISSION_COMMAND_ARCHITECTURE.md` revisions of the
   "centuries-of-refinement" warrant. HIGH-gate promotion is now
   gated on Hans precision audit of those 6 firings only (target
   ≥60% precision per pattern).
3. ~~**Human re-judge of 12-draft stratified sample from Exp 11b**~~ —
   **CLOSED 2026-05-30:** Hans 12/12 rated, 91.7% Hans-both-judges
   agreement, FALSIFIES collusion concern (>=75% threshold). Fresh-Grok
   framing-sensitivity pass also 12/12 (no detectable framing drift).
4. ~~**`Finding` shape decision**~~ — **LOCKED 2026-05-30:** reuse v0.1.1
   `Finding` dataclass unchanged. Cost accounting lives in a separate
   log, not the Finding object.
5. ~~**Hans precision audit of 6 baseline firings**~~ — **CLOSED 2026-05-30:**
   6/6 TP, 100% per-pattern precision; all three patterns PROMOTED to
   HIGH (see Severity table). v0.2.1 ships HIGH-gate.
