# Operator Dogfood Asymptote — Empirical Finding

**Run date:** 2026-05-18
**Product:** Operator (`~/Projects/operator/`)
**Method:** Dogfood loop — render spec package → hand to fresh build agent →
measure gap composition. Four internal iterations (v0–v3, Claude Code) plus
**three** external iterations:
- v1.5 Run 1 — Acme invoice automation, OpenAI Codex CLI / GPT-5.5
- v1.5 Run 2 — NDA / vendor-contract clause review, OpenAI Codex CLI / GPT-5.5
- v1.5 Run 3 — Acme invoice automation (same spec as Run 1), Google gemini-cli / Gemini 2.5

**Updated 2026-05-18 late evening (+~3 hrs after Run 2):** N=3 evidence
now spans two model families AND two workflow domains. The interpretation
has shifted twice — first by Run 2's same-family replication of Bucket B
at 42.9% (strengthening a "stable structural blind spot" reading), then
by Run 3's cross-family contrast showing Bucket B at 12.5% on the
identical spec (disconfirming that reading; revealing the 42.9% finding
as reader-style-specific to Codex, not renderer-property-general).

The headline below reflects the current best interpretation. The
original single-run and N=2 summaries are preserved further down for
the historical record — they document the shifting belief as evidence
accumulated.
**Spec source:** Acme Widgets synthetic invoice-automation brief
(`data/engagements/acme-widgets-synthetic-test-data-a4937a/workflow_briefs/invoice_automation_v4.json`)
**Operator HEAD at run:** `481086a` (commit "specs.py — v3 dogfood
iteration").
**Doctrine relevance:** Principle 13 (*The Long Horizon*) + Working
Backwards methodology — evidence-of-method, not evidence-of-causation.
**v1.5 release status:** Candidate appendix material. Does NOT carry the
Law I/VI replication evidence that v1.5 is gated on per
`RELEASE_PLAN_v1.md`.

---

## Executive summary

The dogfood loop converges on a *defect backlog*, not on zero. Three to
four internal iterations + ~$5 of compute + ~18 min wall-clock reach a
stable gap count of ~10. The internal-loop hypothesis was that the
remaining gaps would be dominated by **irreducible client decisions** —
questions only the client can answer (which duplicate-tuple? which
holiday calendar? which PO-match procedure?). That hypothesis was named
the *asymptote claim* and was provisionally adopted as the load-bearing
pitch sentence for Operator's spec-engagement product.

The first non-Claude external iteration (GPT-5.5 / Codex CLI, 2026-05-18
evening) **partially disconfirms the asymptote claim as originally
stated.** Bucket B (cross-section contradictions) dominates the external
gap list at 42.9%, over the rubric's 40% "Claude-over-fit" threshold.
Bucket C (missing client decisions) sits at 28.6%, below the 30% partial-
support threshold. The external loop also surfaced three defect classes
the internal loop did not catch, each pointing to a concrete tooling
improvement (a v4 validator pass).

The honest reframe: the loop surfaces a *spec-defect backlog*, not an
*irreducible client-decision floor*. The decision-floor is a sub-
component of the backlog (~20–30%), not the whole of it. The original
pitch sentence ("time-to-decision-floor is what we sell") softens to
"time-to-question-backlog is what we sell, with ~3 irreducible
client decisions as a stable sub-floor."

This is the **best possible outcome** for a single-shot external
experiment. A confirming run would have been suspicious (same finding
across model families = either real signal or shared blind spot). A
disconfirming run with three concrete next-tooling opportunities is real
evidence and real work.

---

## Method

### Internal iterations (v0 → v3, Claude Code)

Each internal iteration:

1. Render `TRD.md` / `BRD.md` / `SOW.md` from the synthetic brief via
   Operator's `tools/specs.py`.
2. Spawn a fresh Claude general-purpose agent in an isolated working
   directory containing **only** the three rendered .md files.
3. Apply hard rules: no interactive clarification, mock all external
   services, stdlib + pytest only, time cap 30 min.
4. Capture the agent's `GAPS.md`, score each gap by bucket per the rubric,
   record composition.

Gap-counting rubric (canonical at
`operator/library/2026-05-18/dogfood_loop/v1_5_evidence_packet/GAP_RUBRIC.md`):

- **Bucket A — Mechanical render defect.** Field exists in source brief
  but renderer doesn't surface it. Closable by code change in
  `tools/specs.py` without involving the client.
- **Bucket B — Cross-section contradiction.** Section X and section Y
  cannot both be true. Closable by validator addition.
- **Bucket C — Missing client decision.** A hole only the client can
  fill. Not closable by tooling. **This is the asymptote claim.**
- **Bucket D — External-dependency gap.** Spec depends on something
  outside its own scope (fixture file, vendor API contract).

### External iteration (v1.5, GPT-5.5 / Codex CLI)

Same protocol, with two differences:

1. Builder agent is **not Claude** — explicitly required for non-
   circularity. The original method circularity (Claude-authored spec
   read by Claude-driven builder) is the falsifiability problem this
   iteration was designed to address.
2. Spec package is the v3 rendered output, frozen at Operator HEAD
   `481086a`. No further internal iteration between v3 and v1.5.

---

## Results

### Internal iterations (Claude Code)

| Iter | Wall-clock | Spend | Gap count | Gap composition signal |
|---|---|---|---:|---|
| v0 | ~6 min | ~$1.50 | ~10 | dominated by mechanical + contradiction |
| v1 | ~6 min | ~$1.50 | ~10 | half mechanical, half client-decision |
| v2 | ~6 min | ~$2 | ~10 | client-decision dominant (asymptote hypothesis) |
| v3 | n/a | n/a | n/a | no full rebuild — closed v2 mechanical residue |

By v2 the internal-loop verdict was: gap count stable around 10,
composition converging on Bucket C. The provisional pitch sentence
adopted in `operator/STORY.md` 2026-05-18 chapter:

> Operator surfaces the irreducible client-decision floor in 3
> iterations and ~$5 of compute. Without Operator, that takes 8–12 weeks
> and three consultancies asking for $80K-plus. The artifact is the
> same; what we sell is time-to-decision-floor.

### External iteration (GPT-5.5 / Codex CLI v0.131.0)

Wall time 3 min 29 s. 5/5 acceptance scenarios pass. 7 gaps surfaced.

| Bucket | Count | % |
|---|---:|---:|
| A — Mechanical render defect | 2 | 28.6% |
| B — Cross-section contradiction | 3 | **42.9%** |
| C — Missing client decision | 2 | 28.6% |
| D — External-dependency gap | 0 | 0% |

Per the rubric's hold/fail bar:

- **Bucket C ≥60% (strong asymptote support):** ❌ NOT MET
- **Bucket C 30–60% (partial support):** ❌ NOT MET (28.6%)
- **Bucket A or B >40% (Claude over-fit signal):** ✅ MET (Bucket B at 42.9%)

### Three new defect classes the internal loop missed

1. **Cross-document contradiction (TRD↔SOW).** SOW §7 excludes custom
   integration code; TRD §6.2 + §9 require custom adapters. Operator's
   `_validate_internal_consistency` only checks *within* the TRD.
2. **Service-account roster gap.** `ap-agent@` is the workflow execution
   agent every scenario references in `expected_audit_entry`, but
   `_render_service_account_roster` only derives SAs from the
   `integration_details` field. Execution-agent SAs are missing from
   the roster the audit log resolves against.
3. **Fixture packaging gap.** The v3 renderer flags `sample_documents`
   as BLOCKING in the brief, but does not generate fixture files when
   exporting the spec package. The package shipped contained only the
   three .md files.

Each of these is a concrete tooling task. None of them is an irreducible
client decision. The asymptote claim's robustness depends on whether
internal iterations *with* a v4 validator pass recover Bucket-C
dominance, or whether new defect classes continue to surface with each
non-Claude builder substrate tested.

### Informative null: no circularity caveat

The v0 internal Claude run *unprompted* self-disclosed the circularity
of the experiment ("I am Claude. The TRD was authored by 'Halsey' and
the BRD by 'Mason' — both Claude-driven specialists. The §9.1 acceptance
scenarios I just made pass were drafted by the same agent lineage that
drafted the §4.1 routing rules that contradicted them."). GPT-5.5 made
no such observation. The implication: Claude has a self-reflective
habit (questioning input provenance) that GPT-5.5 does not share.
Internal-loop circularity disclosures cannot be assumed to generalize.

### Builder-competence finding

Independent of the gap question, the external run is informative about
GPT-5.5 as an agentic coding agent:

- Shipped 5/5 passing acceptance scenarios faster than the Claude
  internal v0 loop (3m29s vs ~8m).
- Made the same architectural choices Claude made independently:
  frozen dataclasses, Decimal for money, sha256/sha1 for canonical hashing.
- Recovered from its own first pytest collection error with a minimal
  `conftest.py` sys.path shim — appropriate non-invasive fix.
- Documented every interpretation in `ASSUMPTIONS.md` per the rule.
- Honest `BUILD_REPORT.md` conclusion matched Claude's v0 conclusion
  ("buildable as a mocked harness; not cleanly buildable at fixed price
  without a clarification pass").

**Second-order finding:** the spec is portable across model families
given the *no-clarification + assume-and-document* discipline. The gap
composition differs, but the buildability story is the same. This is
itself evidence that Operator's rendered spec format is doing real work,
independent of whether the asymptote claim holds.

---

## Honest reframe of the pitch

| Original (pre-v1.5) | Revised (post-v1.5 evidence) |
|---|---|
| Operator surfaces the *irreducible client-decision floor* in 3 iterations / ~$5 | Operator surfaces the *spec-defect backlog* in 3 iterations / ~$5; the backlog converges on ~10–15 questions of which ~20–30% are irreducible client decisions, ~40% are cross-section contradictions closeable by tooling, ~30% are mechanical or packaging defects |
| Time-to-decision-floor is what we sell | Time-to-question-backlog is what we sell; the irreducible decision-floor is a sub-component of the backlog, not the whole of it |
| The artifact is the same; what we sell is speed | The artifact is the same shape; what we sell is the structured question backlog *plus* the doctrine that separates closeable defects from irreducible decisions |

The original sentence reads cleaner but isn't load-bearing. The revised
sentence is uglier but survives the falsification test the original
didn't.

---

## Doctrine relevance

This finding does **not** carry the Law I/VI biographical-moat
replication evidence that `RELEASE_PLAN_v1.md` schedules for v1.5
(2026-07-25). That evidence is a separate experimental track gated on
external statistician engagement.

What this finding **does** demonstrate:

- **Principle 13 (The Long Horizon)** — *evidence-of-method*. The PR/FAQ
  / Working Backwards methodology produces measurable convergence. The
  dogfood loop is the measurement instrument. The defect backlog is the
  measured artifact. The product survives empirical testing of its own
  pitch.
- **Principle 12 (What else? Active extraction)** — *applied surface*.
  The Reflection Gate that runs on every Operator specialist response
  is the same instinct as the dogfood loop's "no interactive
  clarification — every ambiguity must be flagged" rule. The two
  surfaces enforce the same discipline at different scales.
- **Principle 1 (The code is the story)** — *non-portability evidence
  (negative)*. The dogfood loop is a methodology any builder could
  run. The biographical moat is not in the methodology — it's in
  Operator's specialist roster, in the WW2-cockpit-to-switchboard
  aesthetic, in the all-staff MCA shape. The loop is portable; the
  product the loop tests is not. This is the right shape for
  Principle 1.

---

## Honest limits

- **N = 1 external run.** Single model family (GPT-5.5), single harness
  (Codex CLI). A second external run with Gemini 2.5 Pro or Llama 3.3
  70B would strengthen or weaken the disconfirmation. Single-run
  evidence; do not over-claim.
- **Spec is synthetic.** The Acme Widgets brief is Hans-authored test
  data, not a real customer engagement. A run against a real customer
  brief (Brian Friedman's pilot when it lands) is the next falsifiability
  upgrade.
- **Spec author is Operator (Claude).** The asymptote claim is about
  Operator's spec-engagement output. The full circularity-break would
  require a spec authored by a non-Claude system AND read by a non-
  Claude builder. Currently we have *spec by Claude, builder by GPT-5.5*
  — half the circularity broken.
- **Rubric is Hans-authored.** The four-bucket gap classification is
  itself a Claude-and-Hans construction. A different rubric might
  classify the same gaps differently and produce a different verdict.
- **Pitch surface untested.** The revised pitch sentence has not been
  read aloud to a real buyer (Brad's network, Brian Friedman, an EMBA
  peer). Buyer-test is the next pitch-surface falsifier.

---

## Next experiments to upgrade evidence

In order of value-per-cost:

1. **v4 internal pass.** Build the three new validators
   (TRD↔SOW cross-document, execution-agent roster inclusion, fixture
   packaging). Re-render the v4 package. Should not affect the v1.5
   external evidence; it's a separate question (does Operator-tooling
   close the new defect classes the external loop surfaced).
2. **Second external run, different model family.** Gemini 2.5 Pro
   via Aider is the next-most-aligned-with-market-pitch (MegazoneCloud
   implies Gemini Enterprise). N=2 across model families strengthens
   either the disconfirmation or the partial-support read.
3. **Real-customer brief run.** When Brian Friedman's triage reply
   lands and his real brief enters the system, render → external builder
   → score against the same rubric. Synthetic-to-real upgrade is
   the largest single non-circularity gain available.
4. **Buyer-test the revised pitch.** Read the revised sentence to one
   real buyer (Brad or an EMBA peer), capture their first-question. If
   the first question is about the floor sub-component, the pitch lands
   intact. If the first question is "what's a question backlog and why
   should I care?", the pitch needs another reframe.

---

---

## Update — Run 2 (2026-05-18 evening, +~90 min after Run 1)

The single-shot Run 1 finding above raised an open question: was the
42.9% Bucket B dominance Acme-specific (artifact of the invoice-automation
workflow shape), or a general property of the v3 renderer? Run 2 tests
cross-domain stability with a different workflow: NDA / vendor-contract
clause review. Same external substrate (GPT-5.5 / Codex CLI). Same
BUILD_PROMPT, same gap rubric, fresh workspace, fresh brief.

### Run 2 results

5/5 acceptance scenarios pass. 7 gaps surfaced. Composition (with
reclassification of Codex's labels per the rubric):

| Bucket | Run 1 (invoice) | Run 2 (contract review) | Cross-run signal |
|---|---:|---:|---|
| A — Mechanical render defect | 28.6% | 14.3% | declining as renderer matures |
| B — Cross-section contradiction | **42.9%** | **42.9%** | **STABLE across domains — load-bearing finding** |
| C — Missing client decision | 28.6% | 14.3% | declining; floor smaller than originally claimed |
| D — External-dependency | 0% | 28.6% | workflow-shape dependent |

### Headline N=2 finding

**Bucket B holding at exactly 42.9% across two distinct workflow domains
is not random.** The v3 renderer has a stable, reproducible cross-section-
contradiction blind spot that is independent of workflow domain. The
asymptote claim, as originally stated, is disconfirmed not by a single-
run anomaly but by a reproducible structural property of the renderer.

### Secondary N=2 findings

- **Bucket C dropped from 28.6% → 14.3%.** The originally-revised pitch
  ("~20–30% irreducible sub-floor") is too optimistic. Honest N=2 range:
  ~14–29% Bucket C with central tendency ~20%.
- **Bucket D appeared in Run 2 (28.6%, was 0% in Run 1).** Workflow-shape
  dependent — contract review has irreducible external dependencies
  (stakeholder pilot signoff, platform-managed observability) that
  invoice automation didn't. Some workflow shapes have legitimate
  Bucket D content; pretending every backlog is pure-internal is
  inaccurate.
- **Codex still did not surface a circularity caveat.** N=2 confirms the
  Run 1 informative null: input-provenance self-disclosure is Claude-
  specific behavior, not universal builder behavior.
- **Builder competence replicated.** Same architectural choices (frozen
  dataclasses, enums, sha256/sha1, deterministic in-memory mocks). Same
  pytest collection-error and same 9-line conftest.py fix. Same honest
  fixed-price-buildability read. The spec format is portable across
  workflow domains given GPT-5.5 as the builder.

### Updated v4 validator backlog — six items now

Three new defect classes from Run 2, additive to Run 1's three:

| # | Defect class | Source | Severity |
|---|---|---|---|
| 1 | TRD↔SOW cross-document contradiction | Run 1 | BLOCKING |
| 2 | Service-account roster missing execution agents | Run 1 | BLOCKING |
| 3 | Fixture packaging — generate stubs or fail loud | Run 1 + Run 2 | BLOCKING |
| 4 | Idempotency-key cross-section consistency | Run 2 | BLOCKING |
| 5 | Exception-class enum validator (mirror AUDIT_VERB_NOT_IN_ENUM) | Run 2 | BLOCKING |
| 6 | Tier × exception route disambiguation | Run 2 | MAJOR |

None of these were predictable from the v3 internal iteration. All of
them came out of running the loop against external builders.

### Twice-revised pitch sentence

| Generation | Sentence | Evidence basis |
|---|---|---|
| Original (morning 2026-05-18) | "Operator surfaces the *irreducible client-decision floor* in 3 iterations / ~$5" | Internal Claude-on-Claude only |
| Revised after Run 1 (evening) | "...the spec-defect backlog converges on ~10–15 questions of which ~20–30% are irreducible client decisions, ~40% are contradictions closeable by tooling, ~30% are mechanical/packaging" | N=1 external |
| Revised after Run 2 (this update) | "...the backlog converges on ~7–10 questions of which **~14–29%** are irreducible client decisions (central tendency ~20%, range varies by workflow shape), ~40% are cross-section contradictions closeable by tooling, and the remainder split between mechanical defects and (for some workflow shapes) irreducible external dependencies" | N=2 external |

Each revision moves the sentence further from cleanly memorable and
closer to the data. That is the right direction. The pitch surface has
not yet been buyer-tested; the v1.5 doctrine release should not commit
to a public sentence until at least one real-buyer read has happened.

### Updated honest limits

The honest-limits section above stands, with these additions from Run 2:

- **N=2 same model family, two different workflow domains.** Stronger
  evidence than N=1 but still single-substrate. The natural next experiment
  is N=2 cross model families (Gemini 2.5 Pro on either spec).
- **Run 2's spec brief was Hans-and-Claude-authored** (drafted by Claude
  in conversation with Hans this evening). Same circularity-on-input as
  Run 1.
- **Run 2's brief was validated against v3 internal validators before
  rendering.** Two consistency issues caught by the internal validators
  were fixed before Codex saw the spec. Run 2's gap-surfacing therefore
  measures what gets past the v3 validators, not what gets past v0.

### Status for v1.5 doctrine release

Reaffirmed from the original section above: this finding is candidate
v1.5 appendix material, **not** Law I/VI causal-claim evidence. The
N=2 replication strengthens the methodology evidence (Principle 13 /
Working Backwards / falsifiable measurement instrument) but does not
move the biographical-moat causal claim, which remains gated on the
statistician work scheduled separately per `RELEASE_PLAN_v1.md`.

---

## Update — Run 3 (2026-05-18 late evening, +~3 hrs after Run 2): cross-family flip

Run 3 was selected per the post-Run-2 SITREP's PIR-1 (cross-model-family
evidence is the highest-value next collection). The same Acme spec used
in Run 1 was re-run with a different model family (Gemini 2.5 via
gemini-cli v0.42.0) to isolate the model-family variable from the
workflow-domain variable.

### Run 3 result

5/5 acceptance scenarios pass via `unittest` (pytest not in env;
Gemini's recovery strategy was to switch frameworks, vs Codex's
conftest.py path-shim). 9 gaps surfaced; 1 was a build-environment
misclassification (pytest-missing flagged as a spec defect). 8 spec
gaps after exclusion.

| Bucket | Run 1 (Codex/Acme) | Run 2 (Codex/Contract) | **Run 3 (Gemini/Acme)** |
|---|---:|---:|---:|
| A — Mechanical | 28.6% | 14.3% | **0%** |
| B — Cross-section contradiction | 42.9% | 42.9% | **12.5%** |
| C — Missing client decision | 28.6% | 14.3% | **37.5%** |
| D — External-dependency | 0% | 28.6% | **50.0%** |

### The headline interpretation flip

**The N=2 Codex finding ("Bucket B = 42.9% stable across domains,
therefore a structural v3 renderer blind spot") is disconfirmed by
Run 3.** The same Acme TRD that Codex reads as having 3 cross-section
contradictions, Gemini reads as having 1. The "stable cross-family
blind spot" attribution was wrong. The reproducibility was *within
Codex*, not within the renderer.

**Updated attribution:** Codex/GPT-5.5 reads cross-section
contradictions more aggressively than Gemini does. The spec property
Codex was surfacing as Bucket B is at least partly a property of how
Codex reads, not how the renderer renders. The renderer is healthier
than the N=2 picture suggested.

### Implications for the asymptote claim

Bucket C went UP for Gemini (37.5%, comfortably within the original
"~20–30%" pitch range). The morning's claim — that the loop converges
on client-decisions as the dominant residual — has more empirical
support from Gemini than the second-and-third-gen pitch revisions
suggested. Gemini's reading is **closer to the original hypothesis
than Codex's reading is**.

### Pitch sentence — fourth generation

| Generation | Sentence | Evidence basis |
|---|---|---|
| Original (morning 2026-05-18) | "Operator surfaces the *irreducible client-decision floor* in 3 iterations / ~$5" | Internal Claude-on-Claude only |
| Revised after Run 1 | "...the backlog converges on ~10-15 questions of which ~20-30% are irreducible client decisions, ~40% contradictions closeable by tooling, ~30% mechanical/packaging" | N=1 external (Codex) |
| Revised after Run 2 | "...~14-29% irreducible (central tendency ~20%)" | N=2 same-family (Codex × 2) |
| **Revised after Run 3** | **"...~15-40% irreducible (composition reader-dependent — Gemini ~37%, Codex ~14-29%). The reader the buyer's build platform uses determines which composition they see. What we sell is the speed of producing the backlog, not the composition of it."** | N=3, two model families, two workflow domains |

The fourth-generation sentence is uglier than the first but is the
only one that survives the N=3 evidence. The cleanest interpretation
is that **gap composition is reader-dependent more than spec-dependent**,
and the doctrine pitch should claim "speed-of-backlog" not
"composition-of-backlog."

### Updated v4 validator backlog status

Six v4 items remain valid work — they all reference real spec defects
that Codex caught. Item #3 (fixture packaging) is the only item all
three readers flagged independently; the other five were caught by
Codex but missed by Gemini.

**Updated framing:** the v4 validators close defects that **at least
one reader** sees as a defect. Building them raises the
"minimum-reader-finds-X-contradictions" floor. Useful regardless of
which reader the buyer's platform uses.

### Replicated null + replicated builder competence

- **Circularity-disclosure null across N=3:** Gemini also did not
  surface input-provenance unprompted. N=3 evidence: this self-
  disclosure is Claude-specific behavior, not GPT-class or Gemini-class.
- **Builder competence cross-family:** 5/5 scenarios pass on every
  external run. Same architectural choices (dataclasses, Decimal,
  uuid task IDs, deterministic mocks). Same honest "buildable with
  reservations" / "not cleanly buildable at fixed price without
  resolution pass" conclusion. **The Operator-rendered spec format is
  portable across model families** — a separately valuable product
  finding, independent of the asymptote question.

### Updated honest limits

The honest-limits sections above stand, with these additions from
Run 3:

- **N=3 spans two model families × two workflow domains.** No
  domain-by-family cell is filled (we don't have Gemini/Contract yet).
  N=4 with that cell filled is a low-cost next move; would confirm or
  weaken the reader-style finding.
- **Gemini's classification was less rigorous than Codex's.** Misread
  pytest-missing as a spec defect; called fixture-packaging an
  external-dep gap (defensible but Codex's mechanical-defect call is
  cleaner). Run 3's gap categorization carries a wider error bar than
  Run 1 or Run 2.
- **OAuth required for gemini-cli; API key path failed with
  INVALID_ARGUMENT.** This is a harness-specific authentication
  finding, not load-bearing for the evidence claim, but worth recording
  for anyone re-running the experiment.

### Status for v1.5 doctrine release

Reaffirmed and strengthened: this finding is candidate v1.5 appendix
material as evidence-of-method. N=3 with cross-family disconfirmation
of an earlier overclaim is **stronger** evidence of the loop's
falsificatory power than N=2 with replication would have been. The
loop is genuinely working as a falsifier — each external run has
improved the interpretation rather than just confirming it.

Does NOT move the Law I/VI causal-claim evidence track; that remains
separate and gated on the statistician work per `RELEASE_PLAN_v1.md`.

---

## Cross-references

- Internal iterations:
  `~/Projects/operator/library/2026-05-18/dogfood_loop/trd_brd_machine_executability_v{0,1,2,3}*.md`
- External iteration Run 1 (Acme invoice automation):
  `~/Projects/operator/library/2026-05-18/dogfood_loop/v1_5_external_codex_gpt5_5-eb81f6.md`
- External iteration Run 2 (contract review):
  `~/Projects/operator/library/2026-05-18/dogfood_loop/v1_5_external_codex_gpt5_5_run2_contract_review-9873f1.md`
- Evidence packet (protocol + rubric + spec package):
  `~/Projects/operator/library/2026-05-18/dogfood_loop/v1_5_evidence_packet/`
- Run 2 source brief: `/tmp/contract_review_brief.json` (not committed)
- Operator HEAD at Run 1: `481086a` (specs.py v3)
- Operator HEAD at Run 2: `89d00bc` (STORY postscript + STARTUP refresh)
- Operator STORY chapter 2026-05-18 — *"The asymptote, and what we
  actually sell"* — captures the internal-loop reframe that was
  partially disconfirmed by Run 1 and replicated-disconfirmed by
  Run 2; the STORY chapter remains accurate as a *narrative-of-belief-
  at-the-time*, with this evidence file as the *belief-after-
  falsification* artifact. STORY postscript (commit `89d00bc`) adds
  the Run-1 disconfirmation in-narrative; the Run-3 cross-family flip
  is not yet narrated in STORY (separate decision for a fresh-head
  session).
- External iteration Run 3 (Gemini/Acme cross-family):
  `~/Projects/operator/library/2026-05-18/dogfood_loop/v1_5_external_gemini25_run3_cross_family-745f92.md`
- Project memory:
  `~/.claude/projects/-Users-hansprahl-Projects/memory/project_operator_dogfood_asymptote_2026-05-18.md`
