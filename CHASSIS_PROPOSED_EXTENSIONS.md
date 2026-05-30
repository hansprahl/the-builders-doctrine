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

## 2. OutputGate Chassis (`chassis/output_gate.py`) — **NEW PRIMITIVE**

**Status:** PROPOSED 2026-05-30 from the Borg-upstream workstream surfaced during the Operator chassis-wiring day. Reference implementation runs in production today as `operator/tools/reflect.py` (117 lines).

**Date opened:** 2026-05-30, during the Operator `chassis/wire-all-primitives` migration.

**Why this is a different primitive from `chassis/reflection_gate.py`.** The existing `ReflectionGate` implements Principle #12 *active extraction* — K/I/G (Known/Inferred/Gap) coverage scoring on agent work products during development, scope-aware refusals, RFI routing. It is an **introspection/coverage** gate, used at `declare_done` to surface what the agent does not know.

`OutputGate` is a different concept entirely: a **response-level quality + commandment filter** that runs AFTER a specialist produces a response but BEFORE delivery to the user. Same-or-corrected: it returns the response unchanged if quality holds, or a minimally-edited version if it does not. The two primitives compose (a response can pass both ReflectionGate's coverage check and still need OutputGate's quality filter), but they are not substitutes.

### The failure mode

Operator runs this on every specialist response. The failure mode it catches, as observed in production over the eight months Operator has shipped:

| Pattern | Example | Detection signal |
|---|---|---|
| Intent miss | User asked "what's our runway?" — specialist returned grant-pipeline analysis | response does not answer the question asked |
| Vague advice | "You should consider exploring revenue diversification options" with no specific next step | response is non-actionable; no name, number, or motion attached |
| Inflated number | "We can scale to $1M ARR in 90 days" without basis | projections lacking citation, mechanism, or comparable cohort |
| Overstep on consent | specialist drafts and "sends" without queueing for approval, or implies a world-boundary action is already executed | response asserts irreversible motion without the queue marker |
| Over-research stalling | 1200-word memo of caveats when the user asked for a decision | response is comprehensive but undelivers on the decision asked for |
| Comfort-substitution for honesty | response answers "yes, that's possible" when the honest answer is "I don't know" | response provides confidence not supported by data the specialist actually saw |

The substrate failure is the same one Prompt Guardian addresses at the prompt layer, expressed at the response layer. OutputGate catches per-response drift that the prompt-time guardian cannot anticipate (input-dependent quality regressions, model-of-the-day variance, edge-case specialist responses).

### Role and authority shape

A **single-shot LLM filter** that runs synchronously between specialist response generation and user delivery. Function-style entry point — no class needed, no state between calls.

Authority: **advisory + minimal-edit corrective.** OutputGate can rewrite the response with minimal changes if it judges the response fails one of the dual-check criteria. It cannot block delivery — if the gate errors, times out, or judges the response empty after correction, the original response ships. The user always receives a response; the question is only whether OutputGate had a chance to improve it.

Composes with ReflectionGate (coverage check), PromptGuardian (prompt-layer audit), and the approval queue (world-boundary actions). OutputGate sits closest to the user — it is the last layer before delivery.

### Spec sketch

```python
# kit/chassis/output_gate.py

from dataclasses import dataclass, field
from typing import Callable, Optional, Sequence
import json


@dataclass(frozen=True)
class QualityCriterion:
    """One quality dimension the gate evaluates.

    Products supply their own criteria — there is no canonical list.
    Operator ships with intent_match / actionable / complete / honest.
    """
    id: str
    description: str  # one-line guidance shown to the LLM judge


@dataclass(frozen=True)
class CommandmentCheck:
    """One commandment the gate evaluates per response.

    Same name as PromptGuardian's commandment but a different evaluation
    surface — here it scores a single response, not a prompt-template.
    """
    id: str
    description: str


@dataclass
class GateResult:
    passed: bool
    quality: dict[str, bool]
    commandments: dict[str, bool]
    issues: list[str] = field(default_factory=list)
    corrected_response: Optional[str] = None


class OutputGate:
    """Response-level quality + commandment filter.

    Run per-response, returns same-or-corrected. Never blocks delivery.

    Parameters
    ----------
    quality_criteria : Sequence[QualityCriterion]
        Product-specific quality dimensions.
    commandments : Sequence[CommandmentCheck]
        Product-specific commandments evaluated per response.
    chat_completion : Callable
        LLM call surface: chat_completion(system, user, *, max_tokens, caller) -> str
    log_handler : Optional[Callable[[dict], None]]
        Called with the issue record when the gate flags a response.
        Product supplies its own storage (Operator uses reflection_log.json
        with a last-100 cap; TOP could use Postgres; doctrine repo could
        no-op).
    min_response_chars : int
        Responses shorter than this skip the gate (default 50).
    error_prefixes : Sequence[str]
        Response prefixes that signal a known error path; skip the gate
        (default ("Hit an error",)).
    """
    def __init__(
        self,
        quality_criteria: Sequence[QualityCriterion],
        commandments: Sequence[CommandmentCheck],
        chat_completion: Callable[..., str],
        log_handler: Optional[Callable[[dict], None]] = None,
        *,
        min_response_chars: int = 50,
        error_prefixes: Sequence[str] = ("Hit an error",),
    ): ...

    def evaluate(self, query: str, response: str) -> GateResult: ...

    def filter(self, query: str, response: str) -> str:
        """Return original response (if passed or gate errored) or
        corrected response (if gate flagged and produced a non-empty fix).
        This is the function products call on every response."""
        ...
```

The chassis primitive provides the dual-check scaffolding (quality criteria + commandments + JSON contract + minimal-edit rule + non-blocking failure mode + log hook + short-circuit-on-error). Products supply the actual criteria, commandment list, LLM client, and log storage. The "80% good = ship" rule and "I-don't-know passes" rule are encoded in the system-prompt template the chassis owns (mirroring how PromptGuardian owns its commandment-evaluation template).

### What it is NOT

- **Not a content-safety gate.** That is CrisisFloor's job. OutputGate runs after CrisisFloor, on responses that have already cleared the crisis floor.
- **Not a coverage gate.** That is ReflectionGate's job. OutputGate evaluates response quality, not whether the agent has named its known/inferred/gap surface.
- **Not a world-boundary gate.** That is ApprovalQueue's job. OutputGate runs on the response text itself, not on outbound side effects.
- **Not a prompt-improvement engine.** That is PromptGuardian's job. OutputGate operates on a per-response basis with no memory; PromptGuardian operates on prompt-templates with full audit history.
- **Not delivery-blocking.** Any failure mode (LLM timeout, JSON parse error, empty correction) returns the original response. Delivery is never gated on OutputGate's availability.
- **Not autonomous learning.** The criteria and commandments are static; if a new failure pattern emerges, the product updates its criteria list. There is no in-band learning loop.

### Risks named in advance

- **LLM-judges-LLM circularity.** OutputGate uses an LLM to judge another LLM's output. Two known failure modes: (a) sycophantic pass (the judge agrees with the response because both share the same model family's biases); (b) over-correction (the judge rewrites stylistically idiosyncratic but correct responses). Mitigation: the gate's system prompt explicitly enforces "80% good = pass" and "minimal-change rule"; periodic audit of the log surface for over-correction drift.
- **Cost compounding.** Every specialist response now triggers a second LLM call. At Operator's volume (~50 specialist calls/day in v1), this is negligible. At Operator-SaaS scale (1000 tenants × 50 calls/day = 50K reflection calls/day) it becomes a line item. Mitigation: cost-cap hook (product-supplied), and `min_response_chars` + `error_prefixes` short-circuits keep the cheap-skip path fast.
- **Latency.** Adds one LLM round-trip per response. At Anthropic's typical TTFT this is 1–3 seconds added to user-visible latency. Mitigation: products can run OutputGate against a faster, cheaper model than the specialist itself (Haiku-class for the judge, Sonnet/Opus for the specialist).
- **Comfort substitution.** "OutputGate passed the response" becomes the new "I checked the response carefully" — same failure mode named in §1's "the chassis replaces honest founder reflection with automated comfort." Mitigation: gate outputs are inputs to founder periodic review of the log surface, not substitutes for it.
- **Silent corrective drift.** If the gate routinely corrects responses but the corrections are subtly wrong, the user receives lower-quality content without knowing the gate intervened. Mitigation: `evaluate()` returns the full `GateResult` (with `corrected_response` separate from the chosen delivery); the log surface records every correction; products can sample-audit corrections offline.

### Validation requirement (what earns its place)

**Pre-registered before chassis migration:**

1. **Parity test against Operator's reflect.py.** Promote a candidate `kit/chassis/output_gate.py`. Re-vendor it into Operator (replacing `tools/reflect.py`'s body with a thin adapter over the chassis primitive). Run Operator's existing reflection-log corpus (last 100 entries) through both the legacy and chassis implementations. **Earns its place if pass/fail decisions match on ≥95% of the corpus AND corrected-response outputs are functionally equivalent (same intent, same length within ±20%, same commandment compliance) on ≥90% of corrections.**

2. **Portability test on a second product.** TOP (Thriving On Purpose) consumes the candidate chassis primitive with TOP-specific quality criteria and commandments. Verify a small TOP-corpus (10 sample responses) flows through the gate with the expected pass/correction behavior. The promoted primitive must be portable across products with different criteria, different LLM clients, and different log storage backends — that is the chassis test.

3. **Cost cap audit.** Run the chassis primitive 100 times against varied response sizes. Verify aggregate cost matches estimate; verify zero hangs (timeout discipline holds); verify the `min_response_chars` + `error_prefixes` short-circuits skip the cheap-skip path at <5ms.

4. **Non-blocking failure mode audit.** Inject five failure conditions (LLM timeout, JSON parse error, empty corrected_response, LLM returns invalid quality keys, LLM raises). Verify each case returns the original response unmodified. **Delivery is never gated on the gate.**

### Migration criteria

OutputGate ships out of staging and into `kit/chassis/output_gate.py` when:

1. Parity test passes (≥95% pass/fail agreement, ≥90% functional-equivalent corrections).
2. Portability test passes (TOP consumes successfully with its own criteria).
3. Cost-cap and non-blocking audits pass.
4. Operator's `tools/reflect.py` shrinks to a thin adapter (function preserved; body delegates to chassis OutputGate); TOP wires the chassis primitive at its delivery point.

If parity fails, the section here is updated with the divergence pattern and either revised (refine the chassis API to match the production reference) or retracted (the right move was to keep reflect.py product-specific). Falsifications are doctrine evidence.

---

## 3. AAR Enrichments (`chassis/aar.py` — extension) — **PROMOTION**

**Status:** PROPOSED 2026-05-30 from the Borg-upstream workstream. The chassis already has `kit/chassis/aar.py` (390 lines, class-based `AARLog` with SQLite persistence). Operator's `tools/aar.py` (216 lines) is smaller but **richer in semantics**: it integrates with a Knowledge Graph, mutates entity status on outcome, queries pending outcomes, and refreshes specialist confidence estimates. This proposal promotes those semantic hooks upstream — NOT by importing the KG into the chassis (KG-agnosticism is the right chassis posture) but by adding **callback hooks** so each capability can plug in.

**Date opened:** 2026-05-30.

### The failure mode

Operator's AAR has been shipping for months and the chassis AAR is a partial-coverage substitute. The four failure modes that surface when a product wires only the chassis AAR:

| Pattern | What chassis lacks | Why this is a chassis-shape problem |
|---|---|---|
| Disconnected outcomes | Chassis stores `action_id` as a dumb string; no graph edges to the original action, the specialist's confidence estimate at the time, or the predicate the outcome calibrates | An AAR row that cannot point back to its causal predecessors is a log entry, not an after-action review. The whole point is closing the loop. |
| Stale entity state | After an outcome is recorded, the originating action's `status` field stays "in_progress" indefinitely; downstream consumers of the action store see false state | If the AAR knows the grant was awarded, the grant's status should be "awarded." Forcing every product to wire its own post-outcome status-update logic is non-portable substrate. |
| No pending-outcomes view | Chassis can list past outcomes; it cannot answer "what did we commit to that we have not yet measured?" | The pending-outcomes question is the running estimate's denominator. Without it, calibration reports are over-confident — they measure precision on what closed, ignoring what is open. |
| Specialist estimate goes stale | Specialists have running confidence estimates (per Agent Doctrine). Outcome records don't refresh them | If the AAR is the calibration loop's measurement leg, the specialist's running estimate is the prediction leg. Decoupling the two means the prediction surface never learns from the measurement surface. |

### Role and authority shape

Extension of existing chassis `AARLog` class. Adds **four callback hooks** that products may register; if no callback is registered, behavior matches today's chassis (KG-agnostic, no-op). The chassis stays KG-free; products plug in their own graph, entity store, and confidence-estimate surface.

Authority: **observer + product-controlled mutation.** The chassis records the outcome; the callbacks fire, and what they do (graph linking, entity mutation, estimate refresh) is the product's responsibility. The chassis does not assume any specific KG schema or entity-store API.

### Spec sketch

```python
# kit/chassis/aar.py — ADDITIONS to existing AARLog class

from typing import Callable, Optional, Protocol


class OutcomeLinker(Protocol):
    """Product-supplied hook: link the AAR record to upstream entities."""
    def link(self, *, aar_id: str, action_id: Optional[str],
             specialist: Optional[str], outcome: str) -> None: ...


class EntityStatusUpdater(Protocol):
    """Product-supplied hook: mutate the originating action's status."""
    def update(self, *, action_id: str, outcome: str,
               action_type: Optional[str] = None) -> None: ...


class EstimateRefresher(Protocol):
    """Product-supplied hook: refresh the specialist's running confidence
    estimate after an outcome is recorded against their work."""
    def refresh(self, *, specialist: str, outcome: str) -> None: ...


class PendingOutcomesProvider(Protocol):
    """Product-supplied hook: enumerate trackable entities that are
    initiated but not yet resolved (grants awaiting decision, campaigns
    in flight, plans not yet executed, etc.). Returns what the AAR layer
    needs to render a 'pending' view alongside historical outcomes."""
    def pending(self, *, max_age_days: int = 90) -> list[dict]: ...


# AARLog __init__ gains four optional kwargs:
#
#   def __init__(self, db_path, *,
#                outcome_linker: Optional[OutcomeLinker] = None,
#                entity_status_updater: Optional[EntityStatusUpdater] = None,
#                estimate_refresher: Optional[EstimateRefresher] = None,
#                pending_provider: Optional[PendingOutcomesProvider] = None):
#       ...
#
# AARLog.record_outcome() gains a post-record hook sequence:
#   1. Write the AAR row (existing behavior).
#   2. If outcome_linker:        outcome_linker.link(...)
#   3. If entity_status_updater: entity_status_updater.update(...)
#   4. If estimate_refresher:    estimate_refresher.refresh(...)
#   Failures in any callback are logged (chassis logger) and swallowed —
#   the AAR record persists regardless. Hooks are advisory enrichments,
#   not gates.
#
# AARLog gains:
#   def list_pending_outcomes(self, *, max_age_days: int = 90) -> list[dict]:
#       if self._pending_provider is None:
#           return []  # chassis is KG-agnostic by default
#       return self._pending_provider.pending(max_age_days=max_age_days)
#
#   def format_pending_for_brief(self, *, max_age_days: int = 90,
#                                limit: int = 20) -> str:
#       """Render pending outcomes as a human-readable brief snippet."""
```

### What it is NOT

- **Not a Knowledge Graph in the chassis.** The chassis stays KG-agnostic. Operator wires its KG via the `OutcomeLinker` callback. Products with no KG register no linker and behave like today's chassis.
- **Not a forced status-mutation contract.** The `EntityStatusUpdater` is optional. Products that don't track entity state register no updater.
- **Not an automatic confidence-prediction layer.** Refresh logic lives in the product. The chassis only fires the hook; what "refresh" means (Bayesian update, EMA smoothing, full retraining) is the product's call.
- **Not a replacement for the existing chassis AARLog public surface.** All existing methods stay; the additions are additive.

### Risks named in advance

- **Hook-cascade silently corrupts data.** A buggy `EntityStatusUpdater` mutates state incorrectly; the AAR record is correct but downstream consumers see wrong status. Mitigation: hook failures are logged but do not block the AAR write; products can run AAR write + entity update in a transaction if their store supports it.
- **Hooks introduce hidden coupling across products.** Two products with different KG schemas wire different linkers; chassis tests can't validate either. Mitigation: chassis test suite covers the contract (linker is called with right args at right time, failures are swallowed), not the linker implementation.
- **Pending-outcomes accuracy depends on the product's provider.** The chassis can't validate that "pending" really means pending. A product that returns stale or wrong pending records corrupts the calibration math. Mitigation: documented in the protocol — the product owns the pending-truth invariant.

### Validation requirement

**Pre-registered before chassis migration:**

1. **Parity test against Operator's aar.py.** Wire Operator's KG-aware code as four callbacks; verify the chassis primitive + callbacks produces identical AAR rows AND identical downstream side effects (graph edges created, entity status mutated, specialist estimate refreshed). Test corpus: Operator's last 50 recorded outcomes replayed against the new wiring. **Earns its place if the AAR rows match byte-for-byte AND all four hook surfaces fire with arguments matching the legacy code's behavior.**

2. **Portability test on a second product.** TOP wires `OutcomeLinker` and `EstimateRefresher` against its own surfaces (TOP has neither a KG nor an entity store; it should register only the estimate refresher and behave correctly with the others null). Verify the chassis primitive handles partial-hook registration gracefully — none, some, all combinations.

3. **Hook-failure containment audit.** Inject failures (raise in linker, raise in updater, raise in refresher). Verify AAR rows persist correctly and only the failed hook is missed; verify failures are logged with enough context to debug.

### Migration criteria

Promoted into `kit/chassis/aar.py` when:

1. Parity test passes (Operator's KG-wired chassis ≡ Operator's legacy aar.py).
2. Portability test passes (TOP partial-hook config works correctly).
3. Operator's `tools/aar.py` shrinks to a callback-registration layer (the four hook implementations) plus product-specific helpers; chassis owns the loop machinery.

---

## 4. PromptGuardian Enrichments (`chassis/prompt_guardian.py` — extension) — **PROMOTION**

**Status:** PROPOSED 2026-05-30 from the Borg-upstream workstream. The chassis already has `kit/chassis/prompt_guardian.py` (551 lines, `Commandment` / `CommandmentScore` / `GuardianReport` dataclasses + `PromptGuardian` base class). Operator's `tools/prompt_guardian.py` (1171 lines, 2.1× larger) ships a closed-loop dual-layer auditor in production: structural-rubric scoring layered on commandment scoring, doctrine-text SHA versioning, version history + rollback API, auto-rollback on regression, multi-layer correction routing with evidence-based surgery. The chassis primitive is **building blocks**; Operator's version is **the engine**. This proposal promotes the engine's load-bearing pieces upstream.

**Date opened:** 2026-05-30.

### The failure mode

PromptGuardian-as-building-blocks (today's chassis shape) requires every consuming product to rebuild the same closed-loop machinery. Operator did this; if TOP and Custer wire the chassis from scratch, they will rebuild the same five capabilities or skip them and ship lower-quality prompt audits.

| Pattern | What chassis lacks | Why this is a chassis-shape problem |
|---|---|---|
| Single-layer score | Only commandment scoring; no structural-rubric layer | A prompt can satisfy every commandment (honest, no engagement-max, Hans decides) and still be structurally weak (no role, vague task, missing output spec). Structural scoring is the upstream Prompt Doctrine's load-bearing layer; it must travel with the guardian. |
| No doctrine versioning | Chassis cannot pin which version of the upstream Prompt Doctrine was active at audit time | If the doctrine evolves and a prompt regresses, the product cannot tell whether the prompt got worse or the doctrine got stricter. Versioning is the only way to disambiguate. |
| No history, no rollback | A prompt-correction that makes things worse leaves the product stuck on the worse version | The closed-loop architecture (audit → correct → re-audit → rollback if regressed) requires a history layer. Without it, Guardian becomes write-only. |
| No auto-rollback on regression | Operator's `apply_prompt_update()` re-audits both layers, detects new flags, and reverts | Without auto-rollback the operator-in-the-loop must manually compare flags before/after on every correction. Doesn't scale. |
| No correction routing | Chassis `correct_agent()` is single-shot, single-layer | Real audits flag commandment-only, structural-only, or both layers. Routing surgery to the right corrector (and sequencing them when both flag) is the difference between effective and ineffective correction. |

### Role and authority shape

Extension of the existing chassis `PromptGuardian` class. Adds **five capability surfaces**: structural-rubric scoring (a second scorer alongside commandment scoring), doctrine versioning (SHA pin), prompt history (durable storage + rollback API), closed-loop auto-rollback (regression detection), correction routing (dispatch to the right corrector).

Authority: **advisory + closed-loop corrective.** Same authority shape as today: the guardian audits, proposes corrections, and applies them; Hans always retains rollback authority. The promotion does not change the authority gradient — it makes the audit + correction loop more complete.

### Spec sketch

```python
# kit/chassis/prompt_guardian.py — ADDITIONS

from typing import Callable, Optional, Sequence, Protocol


@dataclass(frozen=True)
class StructuralDimension:
    """One structural-rubric dimension (analogue to Commandment but for
    Prompt Doctrine structural rules: role_clarity, task_specificity,
    output_specification, context_curation, anti_pattern_absence,
    production_readiness)."""
    id: str
    name: str
    floor: int  # minimum acceptable score (default 3 of 5)


@dataclass
class StructuralScore:
    dimension: str
    score: int
    flagged: bool
    evidence: Optional[str] = None  # exact prompt phrase that triggered


@dataclass
class DualLayerReport:
    agent: str
    commandment_scores: list[CommandmentScore]
    structural_scores: list[StructuralScore]
    doctrine_version: str  # short SHA of upstream Prompt Doctrine
    any_flagged: bool
    layers_flagged: list[str]  # subset of ["commandment", "structural"]


class PromptStore(Protocol):
    """Product-supplied: durable storage for prompt history + rollback."""
    def save_version(self, *, agent: str, prompt: str, timestamp: str,
                     audit_id: Optional[str] = None) -> None: ...
    def list_versions(self, agent: str) -> list[dict]: ...
    def load_version(self, agent: str, timestamp: str) -> str: ...
    def current(self, agent: str) -> Optional[str]: ...


class DoctrineReader(Protocol):
    """Product-supplied: read the upstream Prompt Doctrine and return its
    content + a short version hash. Lets the guardian pin the doctrine
    state active at audit time."""
    def read(self) -> tuple[str, str]: ...  # (doctrine_text, short_sha)


# PromptGuardian gains:
#
#   structural_dimensions: Optional[Sequence[StructuralDimension]] = None
#   structural_corrector: Optional[Callable[..., str]] = None
#   prompt_store: Optional[PromptStore] = None
#   doctrine_reader: Optional[DoctrineReader] = None
#
# New methods (each no-op or raise NotConfigured if its hook is unset):
#
#   def score_agent_dual(self, agent_name) -> DualLayerReport:
#       """Score against both commandments and structural dimensions in one
#       pass. doctrine_version pinned at call time via doctrine_reader."""
#
#   def correct_agent_routed(self, agent_name, report: DualLayerReport
#                           ) -> Optional[str]:
#       """Route to the right corrector based on which layers flagged.
#       Both flagged → commandment corrector first, then structural with
#       prompt_override pointing at the commandment-corrected text."""
#
#   def apply_prompt_update(self, agent_name, new_prompt,
#                           parent_audit_id=None, skip_reaudit=False
#                           ) -> str:
#       """Closed-loop:
#       1. Save current to history via prompt_store.save_version
#       2. Apply the new prompt
#       3. Re-audit (dual layer)
#       4. If new flags introduced vs previous audit → AUTO-ROLLBACK
#          and re-audit again to confirm rollback succeeded
#       5. Return status string ('applied' / 'rolled-back: regression
#          detected on <layers>' / 're-audit failed: ...')."""
#
#   def list_prompt_history(self, agent_name) -> list[dict]: ...
#   def rollback_prompt(self, agent_name,
#                       timestamp: Optional[str] = None) -> str: ...
```

### What it is NOT

- **Not a replacement for the existing chassis PromptGuardian.** All current public methods (`score_agent`, `correct_agent`, `audit`) stay. The additions extend; they do not displace.
- **Not opinionated about doctrine source.** The `DoctrineReader` protocol lets products point at the upstream Prompt Doctrine, a fork, a frozen snapshot, or no doctrine. The chassis does not assume a specific filesystem layout.
- **Not opinionated about storage.** `PromptStore` lets products use filesystem (Operator), Postgres (TOP), or Git refs (doctrine repo). The chassis defines the protocol, not the backend.
- **Not opinionated about corrector LLM.** Same chat-completion injection pattern as today's chassis.

### Risks named in advance

- **Engine-shape lock-in.** Promoting Operator's specific dual-layer architecture into the chassis assumes other products will want this exact shape. Mitigation: structural-rubric scoring is gated on `structural_dimensions` being non-None; products that want commandment-only behavior pass `None` and get today's chassis behavior unchanged.
- **Doctrine-versioning misuse.** A product that pins a stale doctrine SHA produces audits that diverge from the live doctrine without warning. Mitigation: `DualLayerReport.doctrine_version` is surfaced in the audit report; mismatches against the live SHA should be a visible warning in the product's audit UI (not the chassis's responsibility, but documented as a product-level guard).
- **Auto-rollback false positives.** A correction that adds a NEW flag in the structural layer but FIXES a critical commandment flag should probably ship despite the new structural flag. The current auto-rollback rule (any new flag → revert) is too coarse. Mitigation: auto-rollback policy is configurable via callback (`should_rollback(prev_report, new_report) -> bool`); products supply the policy; chassis ships a sensible default (rollback on any new HARD-FLOOR breach, allow new tolerance-band flags through).
- **History-storage growth.** Every audit + correction writes a new version. At Operator's scale this is a non-issue; at SaaS scale it bloats. Mitigation: `PromptStore` protocol lets products implement retention policy (last-N versions per agent, time-based pruning). Not the chassis's concern.

### Validation requirement

**Pre-registered before chassis migration:**

1. **Parity test against Operator's prompt_guardian.py.** Wire Operator's filesystem store, doctrine reader, and structural-rubric dimensions through the candidate chassis. Re-run the last 30 days of Operator's actual Guardian audits (audit-only mode against the same agents at the same timestamps). **Earns its place if (a) commandment scores match exactly, (b) structural scores match within ±1 point per dimension, (c) doctrine-version pins match exactly, (d) correction routing dispatches to the same corrector on each flagged case.**

2. **Auto-rollback regression test.** Construct three test cases: (a) a correction that fixes everything (should NOT rollback), (b) a correction that fixes commandments but adds structural flags (depends on policy; default-policy = allow), (c) a correction that adds a HARD-FLOOR breach (should rollback). Verify the policy mechanism handles all three.

3. **Portability test on a second product.** TOP wires the chassis primitive with TOP-specific commandments and structural dimensions (TOP has different commandments per its `engagement_max_forbidden` set). Audit one TOP specialist; verify the closed loop works end-to-end (audit → correct → re-audit → either-apply-or-rollback) without product-specific scaffolding leaking into the chassis.

### Migration criteria

Promoted into `kit/chassis/prompt_guardian.py` when:

1. Parity test passes.
2. Auto-rollback regression test passes against all three policies.
3. TOP portability test passes.
4. Operator's `tools/prompt_guardian.py` shrinks: the structural scorer, history layer, doctrine versioning, and closed-loop machinery all delegate to chassis; Operator-specific code remains for the commandment list, the structural-rubric content, and the filesystem-backed `PromptStore` implementation.

If parity fails on the structural-layer scores (subjective LLM judgments may not be deterministic enough to match within ±1), the section is revised to relax that bound or retracted in favor of keeping the engine product-specific.

---

## 5. Specialist Function-Style Runner (`chassis/specialist_runner.py`) — **RETRACTED 2026-05-30**

> **Status: RETRACTED 2026-05-30 by TOP-fit back-of-envelope verdict against the second-product portability gate this section pre-registered.**
>
> **Verdict summary:** Specialist function-style runners are inherently product-shaped. TOP's specialist invocation diverges from the proposed signature in three load-bearing ways: (1) TOP routes all user queries through a **unified orchestrator** (`local-mcp/agents/orchestrator.py:570-682`), users never address specialists by name — the proposed `name: str` parameter is the wrong abstraction; (2) TOP wires the same three middleware concerns **INSIDE each specialist's `run()`** (`agents/specialists/schedule.py:750-752` shows the pattern: `resolve_prompt("vera", SYSTEM_PROMPT)` + `query += get_queue_brief("Vera", ...)`), not in a wrapper — the proposed runner would rearrange middleware TOP already solved at a different layer; (3) TOP's only post-call hook is `_capture_confidence(...)` (orchestrator line 209), not the three-callback `on_start`/`on_end`/`on_error` system the proposal assumes. The actual TOP call site is one line, not eleven kwargs: `return _capture_confidence("vera", query, run(query))`.
>
> **Validation gate that fired:** Section §5's "Validation requirement #1" pre-registered: *"Before any chassis code is written, sketch how TOP would consume the runner. If the sketch reveals TOP would route specialists differently … the section is retracted in favor of keeping Operator's runner product-specific."* The sketch was run 2026-05-30 immediately after §5 was drafted. Verdict: TOP routes by orchestrator, not by name; the function signature does not fit. The gate fired correctly without a single line of chassis code written. Per the doctrine of pre-registered validation, the section retracts.
>
> **What ships instead:** Operator keeps `agents/specialists/__init__.py` as a product-specific runner. TOP keeps its inside-`run()` middleware pattern. The chassis-level lesson — that two products solved the same per-call middleware problem at two different layers — gets documented in `kit/chassis/specialists.py` docstring as a portability note, NOT as a runner primitive. **The chassis stays smaller and honest about what is portable.**
>
> **What the workflow catches and what it does not.** The back-of-envelope second-product sketch is the cheapest validation gate in the staging area's discipline. It cost ~15 minutes of analysis (no implementation) and caught a primitive that would have shipped only for Operator. The discipline catches **shape mismatches**; it does not catch **subtle behavioral divergence** (that's what parity tests are for, on primitives that pass the back-of-envelope first). The order matters — cheap gates run first; expensive gates run only on what survives them.

The original spec sketch follows, preserved verbatim. **Nothing below this banner is load-bearing.** The section is kept under Law VII so future builders can inspect the shape of what was caught — and so the staging-area discipline shows its second terminal state alongside §1.

---

**Date opened:** 2026-05-30.

**Original framing (preserved for falsification record).** The chassis ships `kit/chassis/specialists.py` (299 lines, class-based `Specialist` + `SpecialistRegistry`). Operator's `agents/specialists/__init__.py` (102 lines) wires a function-style alternative: `run_specialist(name, system_prompt, tools, query, ...)` that resolves the active prompt dynamically per call, injects a cross-cutting `SHAPING_SHELL` doctrine constant, and threads heartbeat + archive logging through every invocation.

This proposal was opened as the most architecturally philosophical of the four: **not a clear win** to promote. The question was whether the function-style runner was the right abstraction at the chassis layer or whether it was correctly product-specific. Section was opened in the staging area as a **deliberation** — the alternative outcome (retraction with a documented rationale) was as valid as promotion. **It retracted.**

### The failure mode

Operator runs the function-style runner because three cross-cutting concerns must apply uniformly to every specialist call:

| Concern | Why it must apply per-call | Why class-based registry alone misses it |
|---|---|---|
| Dynamic prompt resolution | A PromptGuardian correction must take effect on the NEXT specialist call, not on next deploy | Class-based `Specialist.run()` is constructed with a static prompt. The orchestrator must rebuild Specialist instances to pick up corrections — easy to forget. |
| `SHAPING_SHELL` injection | Closure-gate doctrine constant from `SHAPING_OPERATIONS.md` must travel with every specialist response, not be left to specialist prompts to remember | Chassis has no convention for cross-cutting doctrine constants that apply to all specialists. Each product would re-implement injection. |
| Heartbeat + archive logging | Operations need to know which specialist ran when, with what topic; failures must be non-fatally archived | Class-based `Specialist.run()` is a pure callable; logging hooks are the caller's job and routinely get skipped. |

The pattern is real and load-bearing. The question is the right home for it.

### Role and authority shape

A **stateless utility function** wrapping any `Specialist.run()` callable with three middleware concerns: dynamic-prompt-resolve (via a prompt_resolver callback), suffix-injection (via a configurable shaping shell constant), and lifecycle hooks (start/end callbacks).

Authority: **transparent.** The runner does not gate, transform, or judge. It composes existing chassis primitives (`PromptGuardian.resolve_prompt`, `Specialist.run`) with cross-cutting glue. The promoted primitive is more like `functools.wraps` for specialist calls than a new authority surface.

### Spec sketch

```python
# kit/chassis/specialist_runner.py

from typing import Callable, Optional, Sequence


def run_specialist(
    *,
    name: str,
    system_prompt: str,
    tools: Sequence,
    query: str,
    runner: Callable[[str, Sequence, str], str],  # the actual Specialist.run
    prompt_resolver: Optional[Callable[[str, str], str]] = None,
    prompt_suffix: str = "",
    on_start: Optional[Callable[[str, str], None]] = None,
    on_end: Optional[Callable[[str, str, str], None]] = None,
    on_error: Optional[Callable[[str, Exception], None]] = None,
    fallback_msg: str = "(No results.)",
) -> str:
    """Stateless function-style specialist invocation.

    Middleware stack (in order):
      1. resolve active prompt via prompt_resolver(name, system_prompt)
      2. append prompt_suffix (e.g., SHAPING_SHELL closure gate)
      3. fire on_start(name, query)
      4. invoke runner(resolved_prompt, tools, query)
      5. fire on_end(name, query, result) or on_error(name, exc)
      6. return result or fallback_msg
    """
```

### What it is NOT

- **Not a replacement for `Specialist` / `SpecialistRegistry`.** The class-based registry stays as the right surface for products that need specialist discovery, role-based listing, scope-overlap validation, and tool factory generation. The function-style runner is for products that have already resolved which specialist to invoke and want the cross-cutting middleware applied uniformly.
- **Not a tool factory.** The runner does not construct LangChain agents, manage caching, or wire LLM backends. Those concerns stay product-specific (Operator's `agents/specialists/__init__.py` mixes them in because Operator is a single LangGraph product; the chassis abstraction is tighter).
- **Not opinionated about the suffix.** The `SHAPING_SHELL` constant is Operator's choice. Products supply their own suffix string (or empty).
- **Not opinionated about logging.** Lifecycle hooks are optional callbacks; products implement them or pass `None`.

### Risks named in advance

- **Architectural duplication.** The chassis would ship two ways to call specialists (class-based registry + function-style runner). Two-ways-to-do-X is itself a chassis-shape problem. Mitigation: explicit doctrine note in chassis docs explaining when each is right (registry for discovery + routing; runner for stateless per-call middleware).
- **Promoting the wrong abstraction.** Operator's runner mixes too many concerns (caching, venture context, LangChain bootstrap) — extracting only the portable cross-cutting middleware risks shipping a hollow primitive that nobody uses. Mitigation: validation requirement #1 below — a second product must consume the chassis runner with non-trivial use before promotion is real.
- **The right answer is to keep this product-specific.** A perfectly valid outcome is retracting this section with the rationale: "Specialist runners are inherently product-shaped; the right chassis-layer move was the function-style entry point in the existing `Specialist` class, not a separate runner module." Mitigation: this section is explicitly opened as a deliberation, not a forgone conclusion.

### Validation requirement

**Pre-registered before chassis migration:**

1. **Second-product portability test.** Before any chassis code is written, sketch how TOP would consume the runner. If the sketch reveals TOP would route specialists differently (e.g., TOP's wellness specialists are routed by user-state, not by name, and the function signature doesn't fit), the section is retracted in favor of keeping Operator's runner product-specific. **The chassis test is portability across products; if it doesn't pass the back-of-envelope test, the runner is not a chassis primitive.**

2. **Parity test against Operator's `run_specialist`.** If the second-product test passes, build the chassis runner, re-wire Operator to consume it, verify the existing specialist behavior is unchanged across a 30-day-corpus replay of Operator's specialist invocations.

3. **Middleware-ordering audit.** Verify the middleware order (resolve → suffix → start → run → end → return) is deterministic and that hook failures (e.g., `on_end` raises) do not corrupt the returned result.

### Migration criteria

Promoted into `kit/chassis/specialist_runner.py` when:

1. Second-product back-of-envelope sketch shows the function signature is portable.
2. Parity test passes.
3. Middleware-ordering audit passes.

**Retraction is an acceptable terminal state for this section.** If the second-product sketch fails — TOP would route specialists differently, Custer would inject different middleware — the section here is updated with the falsification rationale and closed. Per the §1 banner pattern, retraction is doctrine evidence, not failure.

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

This file is a staging area, not a backlog. Sections move out (to `kit/chassis/` or to retraction) when evidence arrives.

**Sections at terminal state:**

- **§1, retracted 2026-05-19** by Grok cold-read KILL verdict on the pre-registration plan — first section to reach terminal state, the file's discipline working as designed.
- **§5, retracted 2026-05-30** by TOP-fit back-of-envelope verdict on the pre-registered second-product portability gate — second section to reach terminal state, the cheapest validation gate firing correctly without a line of chassis code written. The discipline is reproducible.
