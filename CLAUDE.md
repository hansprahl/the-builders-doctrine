# The Builders' Doctrine — repo-level instructions

> Auto-loads in every Claude Code session inside this repo. Holds the durable rules and disciplines. Dated state — current phase, what shipped, what's at risk — lives in `STARTUP.md`. When this file disagrees with the code or with `STARTUP.md`, the code wins, then `STARTUP.md`, then this file.

## Identity

This is the portfolio-meta repo for **AI Tradecraft, by Hans Prahl**. It holds the methodology (`THE_BUILDERS_DOCTRINE.md`), the methodological laws governing the doctrine itself (`META_DOCTRINE.md` Laws V–X), the public-facing translator (`EXPLAINER.md`), the Kit (coverage scorer + interview templates), and the chassis (portable runtime components). Every per-product `CLAUDE.md` downstream inherits from what is locked here.

## Stage (current frame for inference)

The v1.0-public ship is dated **2026-06-01** per `RELEASE_PLAN_v1.md`. Internal tags v1.0 / v1.1 / v1.2 already exist; v1.0-public is the next ship. The Law VI replication study returns its verdict **2026-07-20**; v1.5 ships **2026-07-25** carrying the verdict. Until v1.5, the Law I causal claim (biographical substrate → product behavior) is **deprecated**, not retracted — the chassis ships forward, the doctrine prose ships unchanged, but the *causal* substantiation is named as v1.5-conditional and the deprecation is published as a trust signal per `RELEASE_NOTES_v1.0.md §2`.

`STARTUP.md` holds dated phase state; read it for current Phase 1 / Phase 2 closures.

## Hard rules — doctrine-repo specific

- **Material doctrine edits require Hans approval and a version bump.** Editorial edits (typo, clarification, example) do not. "Material" means: changing a principle's name or definition; adding or removing a principle, law, or refusal; reframing what the doctrine claims. If in doubt, ask.
- **The Refusal list is canonical in `THE_BUILDERS_DOCTRINE.md §II.8`.** Per-product `REFUSAL_AUDIT.md` files are downstream audit logs; the canonical list does not get forked into a product file.
- **Patent-adjacent text** — Subsystem A (the closed loop) is patent-pending. The free / paid split (Assayer scorer + doctrine free; corrector, stash-and-rollback, two-corrector router, recommendations engine, CI gate paid) is load-bearing for IP. Do not move features across that line without Hans + Peter Lemire (IP counsel).
- **`OPERATOR_PATENT_DISCLOSURE.md` (in the Operator repo) is pre-filing legal text.** Bio verified correct 2026-05-20 at line 204. Do not unilaterally edit; any bio or claim change goes through Hans + IP attorney.
- **Never skip the founder-romance pre-commit hook** (`git commit --no-verify`) without Hans's explicit per-commit permission. When permission is given, log the override in the commit message per `kit/chassis/FOUNDER_ROMANCE_DETECTOR_SPEC.md §"Override mechanism"`. The override pattern is: state the file:line, the pattern flagged, why the finding is a known FP class, and that the review was logged.
- **No new doctrine claim without an execution date** (Law VII). Any prose-only commitment past its date converts to "deferred indefinitely until measured evidence ships." Slip enforcement is mechanical, not founder discretion.
- **No new law or deliverable from adversarial review until prior packet's top actions have shipped with measurement surface** (Law X). META_DOCTRINE caps at six laws (V–X).

## Discipline patterns — read these before proposing work

- **Adversarial reshape before execute.** Before any deliverable estimated at >2 hrs, run a reshape pass: read the existing artifact, name what is actually missing vs. what the scope claim asserts, write the verdict, *then* execute. Empirically the scope claim collapses ~60-80% on real reshape (today's Phase 1: 4 of 4 deliverables collapsed — framework-holds 6→1.5 hrs, refusal-spec 8→1 hr, productize-vs-license 10→4 hrs, founder-romance detector 13→2 hrs; today's EXPLAINER rewrite: 15-hr scope → 40 min actual). Without the reshape pass, the work expands to fill the estimate. See `[[feedback-adversarial-reshape-is-the-deliverable]]`.
- **Doctrine-vs-code drift is the highest-risk artifact in this repo.** Two flavors caught in the 2026-05-20 sprint alone: (a) *forward-stale* — doctrine says X but code doesn't do X yet (e.g., MCA "all 10 specialists are staff-channel" before the chassis wires the channel); (b) *reverse-stale* — code does X but doctrine still says it's deferred (e.g., `fetch_url` sanitize shipped 2026-04-28 but doctrine listed it deferred for 22 days; approve/reject removal shipped before 2026-05-20 but doctrine still listed it as open). Every commit closing code work in this portfolio must close the doctrine surface in the same patch. Reverse-stale is sneakier — engineering momentum hides it.
- **Sequencing discipline.** Do deliverables in date order per `RELEASE_PLAN_v1.md`. The release plan's `## 8. Decision points along the way` table is the gate schedule, not aspiration. The pitch / EXPLAINER / CLAUDE writing windows are protected for a reason — fresh eyes catch what a sprint pass misses. Sprint mode overrides only with explicit user direction; even then, the discipline becomes "every commit closes code + doctrine together, no exceptions."
- **Build one thing at a time** (Hans's standing rule). Suggest options, wait for selection, then build. Don't bundle multiple enhancements into one commit unless explicitly authorized for the sprint.

## Founder-romance detector + pre-commit hook

The detector at `kit/chassis/founder_romance_detector.py` is the regex linter for the seven observer-bias patterns in the caught-artifact taxonomy. Pre-commit configuration at `.pre-commit-config.yaml`. HIGH-severity patterns (founder_romance 1a/1b, stage_7_revival, carve_out_construction) block the commit; ADVISORY patterns emit warnings. Field-validated against 49 doctrine .md files; 11 HIGH findings on first scan (mix of true positives and anticipated FPs).

Exclude list (in `.pre-commit-config.yaml`): `kit/chassis/test_corpus/`, the spec itself, `archived-prose/`, `dist/`, `STORY.md` (founder narrative by design), `CHASSIS_PROPOSED_EXTENSIONS.md` (taxonomy contains caught examples verbatim).

If the detector fires on a verbatim doctrine quote (e.g., principle name "Chain of command over autonomous AI" trips 1b stoic-NCO-register), use the override mechanism with a logged reason — don't add the file to the exclude list. See `RELEASE_NOTES_v1.0.md` commit `4fe5afa` for the first logged override pattern.

## Pointer index — load-bearing artifacts

**Doctrine prose:**
- `THE_BUILDERS_DOCTRINE.md` — 13 principles (canonical artifact)
- `META_DOCTRINE.md` — six methodological laws (V–X)
- `MISSION_COMMAND_ARCHITECTURE.md` — portfolio-wide agentic architecture (Platoon-validated; rungs 3-9 hypothesis)
- `ADP_6_0_TRANSLATION.md` — civilian glossary for Army vocabulary in MCA
- `PROMPT_DOCTRINE.md` — universal prompt structural rules (canonical upstream)
- `THE_BUILDERS_METHOD.md` — builder-facing method
- `EXPLAINER.md` — plain-language translator; the v1.0 public-facing on-ramp; carries the deprecation-as-trust-signal frame
- `STORY.md` — origin narrative

**Release + planning:**
- `RELEASE_PLAN_v1.md` — operational plan for v1.0 (2026-06-01), v1.5 (2026-07-25), v2.0 (Q4 2026). Read before proposing any deliverable re-cut.
- `RELEASE_NOTES_v1.0.md` — public release notes; locks 2026-05-30
- `BANDWIDTH_OVERLAY_2026-05-15.md` — weekly hours ledger + tripwires + truncation triggers
- `STARTUP.md` — dated phase state; current sprint context

**Empirical record + commitments:**
- `LAW_VI_PRE_REG_v1.md` — pre-registration for the biographical-moat replication study; blocks v1.5 ship
- `OPERATOR_DOGFOOD_ASYMPTOTE_FINDING_2026-05-18.md` — Principle 13 evidence-of-method finding (NOT Law I/VI causal evidence — separate track)
- `REFUSAL_PROPAGATION_OFFRAMP_SPEC.md` — FROZEN spec (v0.2)
- `PRODUCTIZE_VS_LICENSE_DECISION.md` — LOCKED 2026-05-20 (Option C Hybrid); mandatory re-review 2026-07-31

**Kit + chassis:**
- `kit/coverage.py` — single-file scorer (88 fields, 8 templates)
- `kit/templates/`, `kit/onboarding/` — eight templates with interview runners
- `kit/chassis/` — 9 portable runtime components (Crisis Floor, Approval Queue, Per-User Context, Named Specialists, AAR Loop, Prompt Guardian, Reflection Gate, Authority Gradient, Founder-Romance Detector); 276 unit tests

**Per-product CLAUDE.md files (downstream inheritance):**
- `~/Projects/local-mcp/CLAUDE.md` — TOP (chassis parity baseline)
- `~/Projects/operator/CLAUDE.md` — Operator (first chassis wiring; patent-pending closed loop)
- `~/Projects/custer-mcp/CLAUDE.md` — Custer (Guardian recommendations engine origin)
- `~/Projects/rubicon/CLAUDE.md` — Rubicon (paused 2026-04-13 behind tag `rubicon-cohort-v1`)

## When in doubt

Ask. The doctrine is a living document and the version cadence exists exactly so that change can be deliberate. If a proposed edit feels like it would change what the doctrine *claims*, surface it as a question rather than executing.
