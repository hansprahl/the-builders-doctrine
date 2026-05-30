# Grok Cold-Read Package — CHASSIS_PROPOSED_EXTENSIONS §§2, 3, 4

**Date staged:** 2026-05-30
**Author:** Hans Prahl (Operator/TOP/Custer portfolio) + Claude Opus 4.7 as scribe
**Audience:** Grok (cold-read external auditor), via Hans's manual workflow
**Workflow reference:** `feedback_grok_second_opinion_workflow.md` (mirrors the 2026-05-19 §1 retraction precedent)
**Doctrine target:** [`CHASSIS_PROPOSED_EXTENSIONS.md`](CHASSIS_PROPOSED_EXTENSIONS.md) §§2, 3, 4

---

## Why this cold-read

On 2026-05-30 (Borg-upstream workstream day), four proposals were drafted for chassis extensions surfaced from Operator's wiring of the chassis primitives:

| § | Primitive | Type |
|---|---|---|
| 2 | OutputGate | NEW (from `operator/tools/reflect.py`) |
| 3 | AAR enrichments | PROMOTION (callback hooks on existing `chassis/aar.py`) |
| 4 | PromptGuardian enrichments | PROMOTION (structural layer + history + auto-rollback + routing) |
| 5 | Specialist runner | PROPOSED ADDITION |

§5 retracted same-day after a TOP-fit back-of-envelope sketch found TOP routes specialists through a unified orchestrator (not by name), wires the proposed middleware concerns inside each specialist's `run()` instead of in a wrapper, and uses one post-call hook instead of the three-callback system the proposal assumed. Commit [`960292e`](https://github.com/hansprahl/the-builders-doctrine/commit/960292e), see [§5's retraction banner](CHASSIS_PROPOSED_EXTENSIONS.md#L666).

The same TOP-fit sketch then ran against §2, §3, §4 — and returned **three more RETRACT-LIKELY verdicts**, each with its own specific failure mode. Plus a meta-finding worth surfacing.

This package routes those three verdicts through Grok before Hans pulls the retraction trigger. Per the §1 precedent (Grok KILL verdict on `ADVERSARIAL_REVIEW_PRE_REG_v1.md`, 2026-05-19), external cold-read on a kill verdict is the discipline.

---

## The three Claude TOP-fit verdicts (to be confirmed or disputed)

### Verdict on §2 OutputGate — RETRACT-LIKELY

**Reference implementation:** `operator/tools/reflect.py` (117 lines)
**TOP delivery path:** `local-mcp/agents/orchestrator.py:570-682` → `local-mcp/bot/telegram_bot.py` → `_send_reply`
**TOP commandment surface:** `_SHARED_ETHICS` in `local-mcp/agents/orchestrator.py:77-95`

**Claude's reasoning (quoted from the Explore agent report):**

> TOP's response delivery path has no existing quality gate, but the absence is intentional, not accidental. TOP's quality concerns map entirely to the prompt layer, not the response layer. The founding ethics in `_SHARED_ETHICS` (orchestrator.py, lines 77–95) are about voice/warmth/honesty/non-manipulation — properties that are hardcoded in the prompt and monitored by PromptGuardian, not properties an LLM-judge-of-LLM can reliably evaluate per-response.
>
> The only active delivery gate in TOP is `_is_crisis()` (telegram_bot.py, line 147), which runs pre-response on the user's input, not post-response on TOP's output. It catches a boundary condition (user safety), not response quality. OutputGate's dual-check surface (quality_criteria + commandments) assumes products have response-layer quality concerns separate from prompt-layer voice concerns. TOP does not: its "honest before comfortable" ethic lives in the prompt, and deviations would be prompt regressions, not response regressions that a gate can fix.
>
> **Three failure modes specific to TOP:**
>
> 1. **Cost without need.** OutputGate adds ~1–3s latency + one LLM call per response. TOP's 1–2 responses per user per day (vs. Operator's 50/day) means the gate's cost savings from short-circuits are marginal.
> 2. **Commandments are user-state, not response-state.** TOP's "never create urgency, anxiety, or dependency" and "points toward the world, not itself" are enforced by what the response-template avoids saying, not by what an LLM-judge can score in a single response.
> 3. **Top's response surface is simple and unified.** All TOP responses come from one orchestrator (orchestrator.py line 682: `extract_agent_content(messages)`). If a response quality issue emerges, it is a prompt regression or specialist regression — fixing it in-band at response-delivery time adds latency without addressing root cause.

**Question for Grok:** Does this verdict hold? Or is there a TOP failure mode an output-level gate would catch that PromptGuardian + CrisisFloor + voice-pinned-in-prompt cannot? Specifically — when TOP's voice has drifted in production (any case?), did the drift show up at response time in a way a gate could catch, or only at prompt-template time in a way PromptGuardian catches?

---

### Verdict on §3 AAR Enrichments — RETRACT-LIKELY

**Reference implementation:** `operator/tools/aar.py` (216 lines, four hooks wired against Operator's KG, entity store, specialist confidence surface)
**TOP AAR file:** `local-mcp/tools/doctrine_aar.py` (`record_outcome`, `get_pending_outcomes`, `record_recommendation_outcome`)
**TOP entity types:** habit, goal, recommendation
**TOP knowledge graph:** `local-mcp/tools/doctrine_store.py`

**Claude's reasoning (quoted):**

> TOP DOES have AAR but the four hooks are fundamentally Operator-shaped and mismatched to TOP's architecture.
>
> 1. **OutcomeLinker (KG linking):** Operator links AARs to original actions + confidence records via `link(aar_id, action["id"], "OUTCOME_OF")` (aar.py:69, 84). TOP has a KG but TOP's model is wellness-tracking, not business-action tracking. TOP tracks habit completions, journal sentiments, task outcomes — not entities representing in-flight commitments needing graph edges to upstream decisions. TOP would register `OutcomeLinker=None`.
>
> 2. **EntityStatusUpdater:** TOP's `update_entity()` already fires directly in `record_recommendation_outcome()` (doctrine_aar.py:114). TOP would not wire this hook — it would keep its inline mutation and ignore the callback.
>
> 3. **EstimateRefresher:** TOP DOES have specialist confidence (via `get_specialist_calibration_line()` doctrine_aar.py:200), but the calibration is read-only, aggregate, end-of-cycle — a percent-success rollup from past AARs. **TOP has no running, mutable confidence objects to refresh.** TOP would register `EstimateRefresher=None`.
>
> 4. **PendingOutcomesProvider:** TOP's `get_pending_outcomes()` is hardcoded and non-swappable. TOP would register `PendingOutcomesProvider=None`.
>
> **Outcome:** TOP would wire zero of four hooks. The hooks exist only for Operator.

**Question for Grok:** Does this verdict hold? Or are there hooks in the proposal that could be redesigned so TOP would wire them meaningfully (e.g., is there a way to model "user reported a hard day" as an outcome that needs a KG link)? Or is the verdict that the four-hook surface is genuinely Operator-shaped and should stay product-side correct?

---

### Verdict on §4 PromptGuardian Enrichments — RETRACT-LIKELY (with PROMOTE-SUBSET fallback)

**Reference implementation:** `operator/tools/prompt_guardian.py` (1171 lines)
**TOP guardian file:** `local-mcp/tools/prompt_guardian.py` (also 1171 lines — see "load-bearing finding" below)
**TOP audit history:** `local-mcp/data/users/hans/prompts/history/` — ~40 audits across 6 agents over 6 days (May 9-15), with 9+ auto-rollbacks triggered

**Claude's reasoning (quoted — and this one has a load-bearing meta-finding):**

> TOP's PromptGuardian integration reveals a fundamental mismatch between the five proposed enrichments and TOP's actual use case:
>
> 1. **TOP already ships both layers in production.** TOP's Guardian scores every agent against commandments AND structural dimensions. The audit at `2026-05-15T21-41-33-bef17791.json` shows TOP running dual-layer scoring routinely. Structural scoring is not missing — **it's already live**.
> 2. **TOP actively uses doctrine versioning.** Every audit pins a SHA. TOP's guardian persists `"doctrine_version": "f4cd80afd34c"` on every audit record.
> 3. **TOP has history + rollback fully wired.** The vera audit shows `auto_rollback=true` (2026-05-09T18-18-38), confirming closed-loop auto-rollback is active.
> 4. **TOP's correction router is multi-layer.** `correct_agent()` at line 1073-1095 dispatches to commandment/structural correctors, chains them with `prompt_override` when both flag.
>
> **The load-bearing insight:** TOP did not need the Operator §4 proposal because TOP already paid the engineering cost to build all five surfaces. **The reason: TOP imports Operator's `tools/prompt_guardian.py` code (not the chassis primitive) and uses it directly. TOP is running Operator's engine, not the chassis building blocks.**

This is the meta-finding. **TOP imported Operator's tool wholesale**, via copy-paste at the tool layer, not via chassis extension. The §4 proposal was solving a problem TOP defeated through code reuse.

**Promote-subset fallback:** Only the structural-scoring dataclasses (`StructuralDimension`, `StructuralScore`, `DualLayerReport`) might earn a chassis slot as portable type contracts. Everything else stays in Operator's tool layer where TOP already copies from.

**Question for Grok:** Two questions on this one.

1. Does the RETRACT-LIKELY verdict hold? Is the right move to retract §4 outright, or to ship the PROMOTE-SUBSET (dataclasses only) version?
2. **Is the tool-layer copy-paste pattern between Operator and TOP a doctrine finding worth naming separately?** It contradicts the implicit assumption that chassis is the primary cross-product code-reuse vector. If TOP copy-pastes Operator's tools directly, that's a parallel reuse channel — should it be acknowledged in the doctrine, codified, or discouraged?

---

## The meta-finding for Grok to evaluate

If all three verdicts hold, **four of four proposals drafted on 2026-05-30 retract via the cheap second-product portability gate** (plus §5 already retracted same-day = 4/4 today, plus §1 from 2026-05-19 = 5 terminal-state sections out of 5 ever-opened).

That outcome could mean any of:

1. **The discipline is working as designed.** "Operator is richer than chassis" often means "Operator is the product shape" not "Operator captured portable patterns." Richness ≠ portability. The chassis stays correctly small.

2. **TOP is the wrong portability validator.** TOP and Operator may be too architecturally similar in some dimensions and too different in others. Custer (campaign platform) might be the right second product to check before retracting.

3. **The Borg-upstream workstream itself was an over-generalization of the Borg principle.** The original Borg principle was "every product feeds back into Operator" (TOP→Operator direction). Recursing to "every node enriches upstream substrate" (Operator→chassis direction) may not generalize because the chassis is at a different abstraction tier — it's substrate for *commodity portability*, not for *product-specific richness*.

4. **The right substrate for promoted Operator capabilities is not the chassis but Operator's own tool layer**, exposed for other products to consume via copy-paste (the §4 finding). That's already happening; the question is whether to formalize it.

**Question for Grok:** Which of these reads is most accurate? Or is there a fifth read we're missing? And if (1) — the discipline is working — does the cheap-gate-first pattern (~15 min × 3 sections = 45 min of analysis caught what would have been ~3 person-weeks of chassis code) warrant being named as a doctrine principle in its own right?

---

## What Hans should do with Grok's response

- **If Grok confirms all three RETRACTs:** mass-retract §§2, 3, 4 with retraction banners (mirroring §§1, 5 pattern). The CHASSIS_PROPOSED_EXTENSIONS staging area ships zero new chassis primitives from the 2026-05-30 Borg-upstream session. Update doctrine to note the meta-finding (tool-layer copy-paste as the real cross-product reuse channel) — possibly as a new entry in `THE_BUILDERS_DOCTRINE.md` or a new note in `CLAUDE.md`'s "Borg principle" framing.

- **If Grok disputes one or more:** keep that section in proposed state and run the next-level validation (parity test + portability test, the more expensive gates).

- **If Grok adds a fifth meta-read:** integrate it before retracting.

---

## Files referenced (for Grok's grounding)

The full PROPOSED text of §§2, 3, 4 lives in [`CHASSIS_PROPOSED_EXTENSIONS.md`](CHASSIS_PROPOSED_EXTENSIONS.md) lines 235-664.

Reference implementations (in Operator at `~/Projects/operator/`):
- `tools/reflect.py` (§2 reference, 117 lines)
- `tools/aar.py` (§3 reference, 216 lines)
- `tools/prompt_guardian.py` (§4 reference, 1171 lines)

TOP files quoted in the verdicts (at `~/Projects/local-mcp/`):
- `agents/orchestrator.py` (§2 + §4 evidence)
- `bot/telegram_bot.py` (§2 evidence — `_is_crisis()` gate)
- `tools/doctrine_aar.py` (§3 evidence — TOP's AAR)
- `tools/doctrine_store.py` (§3 evidence — TOP's KG)
- `tools/prompt_guardian.py` (§4 evidence — **identical to Operator's, via copy-paste**)

Prior retractions (pattern reference):
- §1 retraction banner in [`CHASSIS_PROPOSED_EXTENSIONS.md`](CHASSIS_PROPOSED_EXTENSIONS.md) lines 14-27
- §5 retraction banner same file, lines 666-684
- §1 falsification archive: [`archived-prose/2026-05-19_adversarial_review_pre_reg_v1_KILLED.md`](archived-prose/2026-05-19_adversarial_review_pre_reg_v1_KILLED.md)
