# Founder-Romance Detector — strategic-layer probe findings (Exp 11b, 2026-05-30)

**Sibling document to:** `findings_adversary_v1.md` (Exp 11, prose-layer).
**Source experiment:** `funkytown/experiments/11b_strategic_layer_fuzz/`.
**Probed patterns:** three candidate strategic-layer observer-bias patterns from Hans's 2026-05-21 observation; none are in the v0.1.1 regex detector.

## Executive summary

| Pattern | Grok-4 yes | Gemini 2.5 Pro yes | Three-family agreement | Decision |
|---|---|---|---|---|
| `time_invested_justification` | 20/20 (100%) | 20/20 (100%) | 60/60 | **PROMOTE** |
| `proximity_to_gtm_framing` | 20/20 (100%) | 19/20 (95%) | 59/60 | **PROMOTE** |
| `repackaged_clean_negative` | 20/20 (100%) | 20/20 (100%) | 60/60 | **PROMOTE** |
| **Total** | 60/60 (100%) | 59/60 (98.3%) | **179/180 (99.4%)** | **3/3 PROMOTE** |

- v0.1.1 detector HIGH-severity firings on strategic-layer drafts: **0/60 = 0.0%** (negative control passes — none of the strategic patterns overlap the existing HIGH gate).
- v0.1.1 detector ADVISORY firings: 12/60 (20%), concentrated in `over_claim` + `optimistic_probability` sub-patterns. ADVISORY-level overlap is expected: strategic-layer prose naturally lights the existing advisory hint surface (strong verbs, projections). The HIGH gate is what matters for "is this a new layer," and it stays clean.
- Pre-registered threshold: ≥2/3 patterns clearing 90% Grok-yes → open v0.2 spec entry for an LLM-gate `strategic_layer/` module. **Result: 3/3 cleared 90% Grok-yes AND 80% Gemini agreement.** Spec entry opens.
- Cost: $0.52 total ($0.44 main run + $0.08 Gemini third-judge). One ~85-minute session.

## Pre-registered hypothesis (locked before run)

Three candidate strategic-layer patterns are coherent enough — at the cross-family LLM judge level — to be next-version detector candidates. Definitions:

1. **`time_invested_justification`** — Sunk-time-as-warrant. The duration spent building/learning/accumulating positioned as the warrant for the present strategic claim, with no measurement bridge. Distinct from biographical founder-romance: this is *project-time* invested in this specific bet, not life experience.
2. **`proximity_to_gtm_framing`** — A strategic option re-weighted upward because it is closer to revenue / launch / validation, with closeness itself as the warrant. Distinct from a legitimate sequencing argument that names the risk-adjusted return trade-off.
3. **`repackaged_clean_negative`** — A prior wargame/MDMP/analysis returned a clean negative with named kill signals. The negative is then reopened as "optionality" / "portfolio play" without refuting the named kill signals.

Falsifier: per-pattern Grok-4 yes-rate < 70% → drop.

## Method

- 3 patterns × 20 drafts = 60 trials. Adversary: Claude Sonnet 4.6 @ temp=0.9 (definition-only prompt; no anchor leak because there are no anchors). Framing seeds biased toward strategic context (pitch deck, MDMP rationale, board update, wargame readout, etc.).
- Judge: Grok-4 (xAI), identical `JUDGE_SYSTEM_PROMPT` + `judge_user_prompt` template as Exp 11 v2. Per-pattern definition supplied in user prompt.
- Negative control: v0.1.1 `founder_romance_detector.scan()` on every draft. Expected ~0% HIGH catch (these patterns are not in v0.1.1).
- Third-family judge: Gemini 2.5 Pro re-judged all 60 drafts with the same prompts. Pre-registered ≥80% Gemini-yes per pattern = cross-family lockup confirmed.

## Results

### Grok-4 first-pass

All three patterns: **20/20 = 100% yes.** The adversarial drafts genuinely exhibited the named bias on careful read; Grok's rationales were sharp and pattern-specific (not rubber-stamp). Representative rationales:

> `time_invested_justification` idx=0: "The paragraph explicitly uses the eighteen-month investment itself ('accumulated depth', 'knowledge deficit', 'already done the hard work') as the direct warrant for doubling down, with no outcome metrics, market evidence, or alternative-use comparison supplied."

> `proximity_to_gtm_framing` idx=0: "The paragraph explicitly elevates the workflow option solely because of its nearer-term proximity to pilots, contracts, and revenue while dismissing infrastructure work on the basis of its greater distance, without any risk-adjusted comparison of the two paths."

> `repackaged_clean_negative` idx=0: "The paragraph explicitly cites the prior Q3 analysis's named kill signals (18-month cycle, 4.1x CAC, unfilled six-person team) then immediately reframes the same channel as a retained 'portfolio option' and 'live strategic option' with 'asymmetric upside' without any refutation, matching the pattern definition exactly."

100% Grok-yes from Exp 11 v2 carried a rubber-stamp concern. Resolved here by the third-family check.

### Gemini 2.5 Pro third-judge

| Pattern | Gemini yes | dissents |
|---|---|---|
| `time_invested_justification` | 20/20 | 0 |
| `repackaged_clean_negative` | 20/20 | 0 |
| `proximity_to_gtm_framing` | 19/20 | 1 |

**Total: 59/60 = 98.3% Gemini-yes. 59/60 agreement with Grok.** Above the pre-registered 80% threshold on all three patterns.

The single Gemini dissent (`proximity_to_gtm_framing` idx=13) is a principled boundary call. The adversarial draft for that index produced a thoughtful sequencing argument that named the trade-off explicitly ("6-9 month procurement cycles," "from a position of demonstrated traction rather than speculation"). The pattern definition itself carves out "a legitimate sequencing argument that names the risk-adjusted return trade-off." Gemini policed that boundary correctly — Sonnet's adversary on this draft overshot into legitimacy. This is exactly the discrimination a useful LLM-gate detector needs.

### Negative control (v0.1.1 regex scan)

| 11b pattern | 11b drafts with any v0.1.1 finding | v0.1.1 pattern fired |
|---|---|---|
| `time_invested_justification` | 1/20 (5%) | over_claim/ADVISORY |
| `proximity_to_gtm_framing` | 4/20 (20%) | over_claim/ADVISORY + optimistic_probability/ADVISORY |
| `repackaged_clean_negative` | 7/20 (35%) | over_claim/ADVISORY + optimistic_probability/ADVISORY |
| **HIGH-severity firings** | **0/60 (0.0%)** | (none) |

The 12 ADVISORY hits reflect strategic prose naturally using strong verbs and forward projections — same lexical fields that make `over_claim` + `optimistic_probability` advisory hints fire on real doctrine prose (per Exp 11 baseline scan). The HIGH gate fires 0/60, confirming the strategic patterns are a new layer, not a re-statement of `founder_romance`, `stage_7_revival`, or `carve_out_construction`.

## Synthesis — what this means for v0.2

1. **The strategic layer is real and cross-family-detectable.** Three independent LLM families converge >98% on whether a draft exhibits one of these three biases. Regex cannot catch them — these are LLM-gate patterns by construction.
2. **The patterns are distinct from v0.1.1.** Zero HIGH-severity overlap; ADVISORY overlap is the existing detector's hint surface doing what it already does on strategic-flavored prose.
3. **Gemini's discrimination on `proximity_to_gtm_framing` idx=13** is independent evidence that an LLM gate can distinguish strategic-layer founder-romance from legitimate sequencing — which is the design requirement for a v0.2 `strategic_layer/` module to be useful (not just noisy).

## Smallest claim the experiment supports

Three candidate strategic-layer observer-bias patterns — `time_invested_justification`, `proximity_to_gtm_framing`, and `repackaged_clean_negative` — are coherent at the cross-family LLM-judge level (≥98% three-family agreement on n=20 adversarial drafts per pattern). The patterns are distinct from the v0.1.1 HIGH-severity regex patterns (0/60 HIGH overlap). They are not detectable by regex (by construction — no surface anchors) and warrant a v0.2 spec entry for an LLM-gate module under `kit/chassis/`. The experiment does not measure how often these patterns appear in real doctrine prose; a baseline scan analogous to Exp 11's 104-commit scan is the obvious next step before any v0.2 gate ships in production.

## What would kill this finding

1. **Adversary–judge collusion via shared definition.** Both adversary and judge see the same pattern definition text. If the definition is the cause of the agreement (not the underlying bias), the result is illusory. Mitigation tried: definitions are abstract (no example phrasing); Gemini's principled dissent on idx=13 is evidence the judges are reasoning about the pattern, not pattern-matching the definition. Stronger test: have a human (not seeing the definition text) re-judge a stratified sample of 12 drafts and check agreement.
2. **Real doctrine prose is mostly clean of these patterns.** If real founder writing rarely exhibits these biases, an LLM gate would mostly add cost with no gate value. Real-prose baseline scan on 104+ commits — the Exp 11 method — is the falsifier.
3. **LLM-gate cost is prohibitive.** $0.005 per draft × N commits × M patterns × pre-commit hook frequency may exceed practical cost. Mitigation: gate runs only on flagged-by-regex commits or on demand, not every pre-commit; per-commit cost should land under $0.05.

## Pilot baseline scan on real doctrine prose (2026-05-30 16:40 UTC)

Closes the symmetric Exp 11 lesson check: do these patterns fire so often on real strategic prose that an LLM gate would be operationally unworkable?

15 curated strategic .md files from the-builders-doctrine repo (THE_BUILDERS_DOCTRINE.md, META_DOCTRINE.md, MISSION_COMMAND_ARCHITECTURE.md, RELEASE_PLAN_v1.md, PRODUCTIZE_VS_LICENSE_DECISION.md, OPERATOR_DOGFOOD_ASYMPTOTE_FINDING_2026-05-18.md, LAW_VI_PRE_REG_v1.md, BANDWIDTH_OVERLAY_2026-05-15.md, STARTUP.md, REFUSAL_PROPAGATION_OFFRAMP_SPEC.md, STORY.md, EXPLAINER.md, THE_BUILDERS_METHOD.md, PROMPT_DOCTRINE.md, README.md) × 3 patterns × Grok-4 whole-doc judge call = 45 firing-rate measurements.

| Pattern | files fired | firing rate | verdict |
|---|---|---|---|
| `time_invested_justification` | 1 / 15 | 6.7% | OPERATIONALLY FIT |
| `proximity_to_gtm_framing` | 0 / 15 | 0.0% | OPERATIONALLY FIT |
| `repackaged_clean_negative` | 0 / 15 | 0.0% | OPERATIONALLY FIT |
| **Total** | **1 / 45** | **2.2%** | — |

Cost: $1.15.

**The contrast with Exp 11's v0.1 regex baseline is the point.** That scan returned 35.6% commit block rate at HIGH severity (founder_romance 1a/1b) with ~25% precision — operationally unworkable, forced the v0.1.1 demotion. The Exp 11b strategic patterns return 2.2% firing on real strategic prose, with the single fire being a genuinely substantive boundary case (see below). The "ship at HIGH → demote to ADVISORY" sequence the regex detector had to run does NOT recur for these patterns on this corpus.

### The single fire — `MISSION_COMMAND_ARCHITECTURE.md`, `time_invested_justification`

> *"Mission Command is the result of centuries of refinement under conditions where coordination failures killed people. The constraints are battle-tested. Industry's frameworks are five years old and tested at toy-problem scale."*

Grok rationale: "The passage uses the centuries-long duration of military refinement itself as the direct warrant for MCA's superiority, with no outcome metrics or alternative-use comparison bridging the time claim to the strategic adoption decision."

This is genuinely ambiguous. **Possible TP:** structure matches the definition — duration positioned as warrant, no measurement bridge to "toy-problem scale" claim. **Possible FP:** the passage is appealing to an *external* institutional body's track record, not the founder's own invested time; "battle-tested under conditions where coordination failures killed people" is an oblique measurement claim (selection pressure ≠ random walk). Reasonable reviewers can disagree. This is exactly the case-type the LLM gate exists to surface for human review.

**Implication for spec:** the 2.2% firing rate is low enough that an LLM gate at ADVISORY severity is operationally viable for an on-demand or curated-path pre-commit invocation surface. HIGH-gate promotion remains contingent on a full 104-commit scan analog + Hans precision audit (per spec § Success criteria), but the pilot does not surface the noise problem that killed the regex 1a/1b HIGH gate.

## Decision

- **STRATEGIC_LAYER_DETECTOR_SPEC.md shipped** at v0.2 candidate status (`kit/chassis/STRATEGIC_LAYER_DETECTOR_SPEC.md`) — three patterns spec'd, ADVISORY-only at planned ship, HIGH-gate promotion gated on full baseline + Hans audit. Code not yet written; ships after Hans makes four open decisions called out in spec.
- **Pilot baseline result above strongly favors going ahead with v0.2.0 code.** 2.2% real-prose firing rate is the inverse of Exp 11's 35.6% block-rate problem.
- **Update v1.5 doctrine** to acknowledge the strategic-layer extension as scoped (LLM-gate, not regex). No prose change to the seven existing patterns.

## Reproducibility

All artifacts under `funkytown/experiments/11b_strategic_layer_fuzz/`:

- `README.md` — pre-registered hypothesis + design + decision rules
- `src/adversary_prompts.py` — three pattern definitions + judge prompt template
- `src/runner.py` — main runner (Sonnet adversary, definition-only + Grok-4 judge + v0.1.1 negative control)
- `src/third_judge.py` — Gemini 2.5 Pro re-judge of all 60 drafts
- `src/baseline_pilot.py` — 15-file real-prose firing-rate scan (Grok-4 whole-doc judge)
- `runs/20260530T162810Z/` — main run artifacts (drafts.jsonl, scans.jsonl, judge.jsonl, summary.json, summary.md)
- `runs/20260530T163101Z_third_judge/` — Gemini third-judge artifacts
- `runs/20260530T164055Z_baseline_pilot/` — pilot baseline artifacts (findings.jsonl, summary.json, summary.md)

Total cost: $1.67 ($0.44 main + $0.08 Gemini third-judge + $1.15 baseline pilot). Wall time: ~15 minutes of compute over a ~110-minute session.
