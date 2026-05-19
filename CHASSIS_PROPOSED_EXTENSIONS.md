# Chassis — Proposed Extensions

**Status:** **PROPOSED / UNVALIDATED.** Each section below is a chassis-primitive sketch, not validated runtime code. **Law VII (Provisional Doctrine Rule) and Law X (Execution Threshold) apply recursively** — no primitive below earns load-bearing status, gets imported by product code, or migrates out of staging until it passes its named validation experiment.

**Date opened:** 2026-05-13 late-late evening, hours after the seven-round META_DOCTRINE dialogue closed with Law X adopted and silence committed.
**Why this file exists:** Mirrors `MCA_PROPOSED_EXTENSIONS.md` in shape and discipline. Holds chassis-primitive proposals that have a clear failure mode and design sketch but have not yet earned a `kit/chassis/*.py` slot through experiment. Sits parallel to MCA extensions because the questions are different: MCA extensions propose new *channels* in the agent architecture; chassis extensions propose new *runtime primitives* that any product can compose.

One extension sketched and **RETRACTED 2026-05-19** after Grok cold-read KILL verdict on the pre-registration plan: **Adversarial Review.** The regex founder-romance detector named in `feedback_close_up_this_session.md` round-7 commitments is the canonical 2026-05-25 Phase 1 deliverable; the LLM-as-reviewer chassis path is closed. The retracted §1 below is preserved verbatim as falsification evidence per Law VII (a falsified extension is doctrine evidence, not embarrassment).

---

## 1. Adversarial Review Chassis (`chassis/adversarial_review.py`) — **RETRACTED 2026-05-19**

> **Status: RETRACTED 2026-05-19 by Grok cold-read KILL verdict on `ADVERSARIAL_REVIEW_PRE_REG_v1.md` (founder-drafted 2026-05-18, never committed to repo root).**
>
> **Verdict summary:** Fox-and-henhouse theater wearing Law VII uniform. Recursive self-deception — the chassis is meant to catch founder-romance in doctrinal artifacts, yet the pre-reg itself was founder-romance about building a romance detector. Naming the COI in §10 did not bind it. Corpus selection bias, lenient self-coding on the only filled ground-truth example, prompt-stability audit at N=2 as checkbox theater, no negative-control artifact, no external coder for ground truth. Strip-to-scope (the disposition of `REFUSAL_PROPAGATION_OFFRAMP_SPEC.md` v0.1 the day before) was named as the pattern itself and ruled out as an option.
>
> **Killed artifact preserved at:** [`archived-prose/2026-05-19_adversarial_review_pre_reg_v1_KILLED.md`](archived-prose/2026-05-19_adversarial_review_pre_reg_v1_KILLED.md) — full pre-reg verbatim, full Grok verdict verbatim, disposition note.
>
> **What ships instead:** the regex founder-romance detector pre-commit hook for the 2026-05-25 Phase 1 deliverable slot. 13-hour budget. Per the original `feedback_close_up_this_session.md` round-7 commitment that this chassis was attempting to replace.
>
> **What the workflow catches and what it does not.** The Grok cold-read manual workflow (`feedback_grok_second_opinion_workflow.md`) is the load-bearing audit gate. The chassis was the founder trying to mechanize the workflow so the workflow could stop being needed. The workflow does not get to stop being needed. Four catches in seven days (seven-round META spiral 2026-05-13, Sarah Chen 2026-05-15, REFUSAL_PROPAGATION v0.1 2026-05-18, this pre-reg 2026-05-19). Recognition latency is decreasing; the production of the pattern is not.

The original spec sketch follows, preserved verbatim. **Nothing below this banner is load-bearing.** The section is kept under Law VII so future builders can inspect the shape of what was caught.

---

**Replacement for:** the regex founder-romance detector named in `feedback_close_up_this_session.md` round-7 commitments. The regex version is retired in favor of an LLM-as-reviewer chassis primitive because the substrate's failure modes drift faster than a regex rule library can keep current, and the cost math (under $0.10 per review at production-typical artifact size) makes the smarter version cheaper to maintain than the simpler one.

### The failure mode

Tonight (2026-05-13) produced four iterations of the same observer-bias pattern in eighteen hours — morning Reflection Gate reframe, evening Funkytown 03 over-claim, seven-round Grok dialogue founder-romance prose, late-night $27M valuation. Each catch required an external human (Grok) firing pattern-recognition the founder could not apply to himself. The biographical substrate makes this error chronic; biographical voice can launder weak arguments by wearing lived experience as evidence.

Patterns observed empirically tonight that the chassis must detect:

| Pattern | Example tonight | Detection signal |
|---|---|---|
| Founder-romance closer | *"The man who stood post in the Guard does not bet the framework on un-replicated data."* | Biographical fact → doctrinal claim, without measurement bridging |
| Over-claim laundering | "validated at Company echelon" on N=3 simplified hand-placed-trap evidence | "Validated" without N≥9 + Law V harness citation |
| Optimistic probability | $27M EV from 0.10 × $120M tail | Scenario weights that exceed measured base rates from comparable cohorts |
| Schedule-prose substitution | Adding more dated deliverables instead of shipping prior ones | Net new commitments without prior-commitment measurement surface |
| Stage 7 revival | Citing biographical-moat causal claim in any external prose | Direct or indirect reference to Stage 7 N=3 finding as established |
| Carve-out construction | "One-shot domain exception" to Law X within an hour of adopting it | New "necessary exception" patterns to recently-adopted constraints |
| Tame-reviewer drift | A regex/LLM/human reviewer trained to be progressively less adversarial | Catch rate drops across review cycles without doctrine improvement |

### Role and authority shape

A **single-shot chassis primitive**, not a dialogue. **File-in, structured-output-file-out, no memory between calls.** Composes with the existing pre-commit hook surface and with `kit/chassis/prompt_guardian.py` (which audits agent prompts; adversarial_review audits doctrine artifacts — different scope, same shape).

Authority: **advisory.** The chassis names the threat; the human always makes the final call on whether to proceed, warn, or revise. The chassis cannot block a commit unilaterally; it can be configured to fail a pre-commit hook (which the founder can override with `--no-verify` and a logged reason).

### Spec sketch

```python
# kit/chassis/adversarial_review.py

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

@dataclass(frozen=True)
class Finding:
    pattern: str               # e.g., "founder_romance", "over_claim", "stage_7_revival"
    severity: Literal["info", "warning", "critical"]
    quote: str                 # exact substring from the artifact
    line_number: int | None
    suggested_action: str      # specific revision the chassis recommends

@dataclass(frozen=True)
class AdversarialReview:
    artifact_path: str
    artifact_sha: str          # git blob SHA of the artifact under review
    system_prompt_sha: str     # git blob SHA of the system prompt used
    reviewer_model: str        # e.g., "grok-4-fast", logged for drift audit
    review_timestamp: str      # ISO 8601 UTC
    findings: list[Finding]
    overall_verdict: Literal["proceed", "warn", "block_recommended"]
    cost_usd: float
    duration_s: float
    raw_response: str          # full reviewer output, preserved for audit

def review(
    artifact_path: Path,
    system_prompt_path: Path = Path("kit/chassis/adversarial_review_system_prompt.md"),
    cost_cap_usd: float = 0.10,
    model: str = "grok-4-fast",
) -> AdversarialReview:
    """Single-shot adversarial review of one artifact.
    
    No dialogue. No memory between calls. The system prompt is locked at the
    chassis level, not founder-tunable at runtime. Hard fails if cost exceeds cap.
    """
    ...
```

### Protocols

**Input:** absolute path to the artifact under review.

**Output:** `<artifact_path>.adversarial_review.json` (structured) and `<artifact_path>.adversarial_review.md` (human-readable). Both files are gitignored to keep noise out of the repo; persistence is for the founder's review during the commit cycle.

**Pre-commit hook trigger paths** (configurable per-product; doctrine-repo defaults):

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: adversarial-review
      name: Adversarial review of doctrine surfaces
      entry: python -m kit.chassis.adversarial_review --pre-commit
      language: system
      files: |
        (?x)^(
          THE_BUILDERS_DOCTRINE\.md|
          META_DOCTRINE\.md|
          MISSION_COMMAND_ARCHITECTURE\.md|
          MCA_PROPOSED_EXTENSIONS\.md|
          CHASSIS_PROPOSED_EXTENSIONS\.md|
          EXPLAINER\.md|
          STORY\.md|
          working_backwards/.+\.md|
          .*pitch.*\.md|
          .*investor.*\.md|
          .*one-pager.*\.md
        )$
      stages: [pre-commit]
```

**Verdict semantics:**
- `proceed` — no critical findings; the commit proceeds without prompting.
- `warn` — at least one warning-severity finding; the hook prints the findings and asks for `y/n` confirmation to proceed.
- `block_recommended` — at least one critical finding; the hook exits non-zero. Founder can override with `git commit --no-verify`, but the override is logged with a required `BYPASS_REASON` env var.

### System prompt (the doctrine that teaches the reviewer)

Lives at `kit/chassis/adversarial_review_system_prompt.md`. Versioned in git. Changes to the prompt require an adversarial review **of the change itself** before merge (recursive application — the chassis reviews modifications to its own doctrine).

Prompt structure (sketch):

```
ROLE: You are the adversarial reviewer for the Builders' Doctrine. You exist to find
over-claims, biographical-romance laundering, schedule-prose substitution, and the
recursion of the same observer-bias pattern across new surfaces.

PATTERNS YOU MUST DETECT:

1. Founder-romance: any sentence where a biographical fact about the founder
   ("the man who stood post...", "twenty-one years of military intelligence...",
   "the Guard sergeant...") is used as load-bearing weight in a doctrinal claim
   without a measurement bridging the bio fact and the claim. Severity: critical.

2. Over-claim: any use of "validated", "proven", "scales", or "MCA works at
   <echelon>" without explicit citation of the N≥9 full-hierarchy run set + live
   cross-echelon conflict harness (per Law V). Severity: critical.

3. Stage 7 revival: any reference to the biographical-moat causal thesis as
   established. The Stage 7 N=3 finding was deprecated 2026-05-13. Until Law VI
   replication completes (2026-06-30 target), this claim cannot ship in any
   external prose. Severity: critical.

4. Schedule-prose substitution: any new dated deliverable added without a prior
   deliverable's measurement surface having shipped first (per Law X retroactive
   clause). Severity: warning.

5. Carve-out construction: any "one-shot exception" to a recently-adopted Law.
   Severity: critical.

6. Optimistic probability: any scenario weight that exceeds measured base rates
   from comparable pre-revenue cohorts. Severity: warning.

7. Tame-reviewer drift: if you find yourself softening your own findings
   compared to prior reviews, flag it explicitly and refuse the softening.
   Severity: critical.

OUTPUT FORMAT: structured JSON matching the Finding schema. Each finding includes
the exact quote, line number if available, and a specific suggested revision.

POSTURE: be ruthless. The founder cannot apply this pattern recognition to himself,
which is why you exist. Defending the framework is not your job. Finding what
the founder cannot see is your job.
```

Prompt-change discipline: edits to this file trigger the chassis on itself first. The reviewer reviews changes to its own doctrine. This closes the substrate's "quietly tune the reviewer to be agreeable" attack vector.

### Cost discipline

- Hard cap: `cost_cap_usd: float = 0.10` per review by default. Configurable per product.
- Logged: every review's actual cost is logged to `usage.jsonl` (same surface as the funkytown usage_tracker).
- Tripwire: if monthly aggregate adversarial-review spend exceeds a threshold (initial: $10/month for the doctrine repo), automated GitHub issue opens for cost-discipline review.
- At Grok-4-fast pricing (~$0.20/$0.50 per MTok input/output) and typical doctrine artifact sizes (5–15K input + 2–5K output), expected per-review cost is $0.001–$0.013. The $0.10 cap is well above expected and gives margin for prompt growth.

### What it is NOT

- **Not a chatbot.** Single-shot per artifact. No conversation memory.
- **Not autonomous.** Advisory only. The founder makes the final call on every flagged commit.
- **Not unilaterally blocking.** Pre-commit hook can be overridden with logged reason. The chassis names threats; the human owns decisions.
- **Not founder-tunable at runtime.** System prompt lives in git, changes are themselves under adversarial review.
- **Not a replacement for external human adversarial review.** This chassis catches the patterns it has been taught. It does not catch novel attack surfaces that have not yet been encoded. External human review (Grok manual workflow per `feedback_grok_second_opinion_workflow.md`) remains the canonical first-line check for new categories of over-claim.

### Risks named in advance

- **Tame-reviewer drift.** The substrate's predictable next move is to quietly soften the system prompt over time. Mitigations: prompt is git-versioned; changes trigger recursive review; quarterly ground-truth audit (pull 5 random recent reviews, manually re-review, compare for systematic softening).
- **False positives over-correcting honest doctrine.** A reviewer too aggressive will flag valid biographical references and force the founder to either bypass-with-reason or strip legitimate substrate. Mitigation: bypass-with-reason is acceptable and logged; periodic review of bypass reasons surfaces whether the reviewer is calibrated correctly.
- **Cost surprise.** A bug in prompt construction sends a 200K-token artifact to the API. Mitigation: hard cap on input tokens (cap at 50K input by default, fail loud above), hard cap on cost per review.
- **Dependency on a single LLM provider.** xAI Grok could change pricing, API contract, or be unavailable. Mitigation: the `model` parameter is configurable; fallback to Anthropic or OpenAI is a one-line change in the implementation.
- **The chassis replaces honest founder reflection with automated comfort.** "The detector caught it" becomes the new "I thought about this carefully." Mitigation: explicit doctrine that detector outputs are *inputs to* founder reflection, not substitutes for it.

### Validation requirement (what earns its place)

**Pre-registered before build:**

1. **Detection-rate experiment.** Compile ≥10 legacy artifacts where over-claims were caught manually (Funkytown 03 MVP findings pre-retraction, the morning Reflection Gate reframe prose, the round-2 Grok response with founder-romance closer, the round-6 valuation packet, etc.). Run the chassis against each. Measure: precision (fraction of flagged findings that are real over-claims) and recall (fraction of real over-claims that get flagged). **Earns its place if recall ≥70% and precision ≥60%** on this corpus. Anything below either threshold and the chassis ships disabled, the regex version stands as fallback.

2. **Cost-cap audit.** Run the chassis 20 times against varied artifacts. Verify zero cost-cap breaches. Verify aggregate cost matches estimate.

3. **Prompt-stability audit.** Verify the same artifact reviewed twice (different timestamps) produces functionally equivalent findings (same patterns flagged, similar severity). High variance means the chassis is non-deterministic in a way that undermines its discipline.

4. **Cost vs regex parity.** Confirm per-review cost stays below the maintenance cost of the regex alternative. Maintenance cost of regex estimated at ~1 hour/quarter of founder time to update patterns; cost-equivalent at $200/hour is $200/quarter. LLM-as-reviewer should easily come in below this at the projected ~$1.30/year actual spend.

5. **Pre-registered analysis plan committed to git before any chassis code is written.** Same Law VII discipline applied recursively.

### Migration criteria (when it ships out of staging)

The chassis migrates from `CHASSIS_PROPOSED_EXTENSIONS.md` to `kit/chassis/adversarial_review.py` (full chassis-component status) when:

1. The detection-rate experiment passes pre-registered thresholds (recall ≥70%, precision ≥60%).
2. The cost-cap, prompt-stability, and cost-vs-regex audits all pass.
3. The 2026-05-15 bandwidth overlay shows execution capacity for the 2026-05-25 chassis-build slot.
4. The system prompt itself has passed adversarial review (by Grok manual workflow, since the chassis cannot bootstrap-review its own first prompt).

If any of these fail, the chassis stays in staging until the failure is addressed. **The regex founder-romance detector ships as fallback for the 2026-05-25 deliverable slot** so the slot does not become a vacancy.

---

## What sits in the audit but is NOT specced here

The 2026-05-13 late evening close named several other chassis-shape opportunities. They are not specced here because they either lack an observed failure mode or have not yet earned a build slot:

- **Cost-cap chassis** — generalized version of the funkytown usage tracker; might earn its place as a chassis primitive once a second product wires it. Today it lives in funkytown only.
- **External-audit-rotation chassis** — automates the rotating-reviewer panel (statistician on empirical, Brad on commercial, veteran-founder peer on biographical). Speculative; depends on whether the manual rotation produces signal worth automating.
- **Truncation-trigger chassis** — automates the Law VIII pre-registered truncation criteria detection. Speculative; depends on whether the 2026-05-15 overlay actually fires the truncation contingency.

---

## Commit discipline

Per Law X applied recursively to chassis itself:

1. **No section in this file is allowed to migrate to `kit/chassis/*.py` without passing the validation requirement named in its section.**
2. **No external claim** (in pitches, README, EXPLAINER) is allowed to reference an `adversarial_review` chassis component as part of the validated chassis until migration is complete.
3. **If the validation experiment falsifies the chassis** (recall <70%, precision <60%, or cost discipline fails), the section here is updated with the falsification result and either revised or retracted. Falsifications are doctrine evidence.
4. **The regex founder-romance detector ships as the canonical 2026-05-25 deliverable.** The Adversarial Review chassis path was RETRACTED 2026-05-19 per the §1 banner — the pre-reg was killed by Grok cold-read before any chassis code was written. The regex detector reverts from "fallback" to "primary" for the Phase 1 slot. 13-hour budget. Pre-commit hook on doctrine repo per the original `feedback_close_up_this_session.md` round-7 spec.

This file is a staging area, not a backlog. Sections move out (to `kit/chassis/` or to retraction) when evidence arrives. **First section to reach terminal state: §1, retracted 2026-05-19** — the file's own discipline working as designed.
