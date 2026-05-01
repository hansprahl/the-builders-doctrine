"""
The Builders' Kit — Prompt Guardian.

Portable implementation of the adaptive prompt-optimization primitive
specified in TOP, Operator, and Custer. The Guardian periodically scores
each specialist's system prompt against a list of product-specific
Commandments, flags drift, generates a minimum-surgical correction,
and queues that correction for human approval. The same primitive runs
across all three products with different commandment sets.

Doctrine invariants this module preserves (non-negotiable):

  1. Source code is read-only with respect to the Guardian. Corrections
     never overwrite .py source. They are written to a file (or store)
     that the runtime resolves *before* falling back to the .py default.
  2. Hard-floor commandments only flag left drift. Drift "above" the hard
     floor is never a correction trigger — only drift below it.
  3. Corrections never auto-apply. Every correction routes through the
     ApprovalQueue chassis. The human (or designated approver) decides.
  4. The MINIMUM-SURGICAL-EDIT discipline is in the correction prompt,
     not in the chassis code. The chassis sends the LLM the rules and
     trusts the LLM to follow them; rejections of bad corrections happen
     at approval time, not at scoring time.

This module is LLM-agnostic. The product passes a `chat_completion`
callable that takes (system_prompt, user_prompt) and returns raw text.
The chassis handles JSON parsing, drift detection, and approval-queue
wiring.

Usage:

    from kit.chassis import (
        ApprovalQueue, JsonFileStore,
        PromptGuardian, Commandment,
    )

    commandments = [
        Commandment(
            id="honest_numbers",
            name="Honest numbers, not hype",
            center="Real data, cited sources, realistic projections.",
            left_edge="Pessimistic to the point of discouraging action.",
            right_edge="Inflated metrics, vanity numbers, no-basis projections.",
            hard_floor=False,
            tolerance_min=3, tolerance_max=7,
        ),
        Commandment(
            id="money_is_real",
            name="Money is real",
            center="Every dollar tracked. Outbound payments gated.",
            left_edge="Financial errors — wrong amounts, missed payments.",
            right_edge=None,                    # hard floor — left only
            hard_floor=True,
            tolerance_min=5, tolerance_max=10,
        ),
        # ... more
    ]

    queue = ApprovalQueue(...)

    def my_resolver(agent: str) -> str:
        return read_active_prompt_for(agent)

    def my_writer(agent: str, new_prompt: str) -> None:
        # Caller decides where to persist — file, DB, etc.
        save_prompt_for(agent, new_prompt)

    def my_chat(system: str, user: str) -> str:
        return llm_call(system=system, user=user)

    guardian = PromptGuardian(
        product_name="TOP",
        commandments=commandments,
        prompt_resolver=my_resolver,
        chat_completion=my_chat,
        approval_queue=queue,
    )

    # When ApprovalQueue executes 'prompt_correction' actions, my_writer
    # is the executor that applies the corrected prompt.
    queue.executors["prompt_correction"] = lambda action: (
        my_writer(action.payload["agent"], action.payload["corrected_prompt"]),
        f"applied correction for {action.payload['agent']}",
    )[1]

    # Run an audit across one or many agents:
    report = guardian.audit(["scout", "rex", "vera"])
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Callable, Optional

logger = logging.getLogger(__name__)

ChatCompletion = Callable[[str, str], str]            # (system, user) -> raw
PromptResolver = Callable[[str], str]                 # agent -> active prompt
DriftDirection = str                                  # 'left' | 'right' | 'none'


# ──────────────────────────────────────────────────────────────────────────────
# Commandment + scoring data shapes
# ──────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Commandment:
    """One commandment dimension the Guardian scores against."""
    id: str
    name: str
    center: str
    left_edge: str
    right_edge: Optional[str]       # None for hard-floor commandments
    hard_floor: bool = False
    tolerance_min: int = 3
    tolerance_max: int = 7

    def __post_init__(self):
        if not re.match(r"^[a-z][a-z0-9_]*$", self.id):
            raise ValueError(
                f"Commandment id {self.id!r} must be lowercase, start with "
                f"a letter, and contain only letters, digits, underscores"
            )
        if not (1 <= self.tolerance_min <= self.tolerance_max <= 10):
            raise ValueError(
                f"Commandment {self.id!r} has invalid tolerance: "
                f"[{self.tolerance_min}, {self.tolerance_max}] must be "
                f"in [1,10] with min <= max"
            )
        if self.hard_floor and self.right_edge is not None:
            raise ValueError(
                f"Commandment {self.id!r} is hard_floor=True but has a "
                f"right_edge; hard floors only flag left drift"
            )
        if not self.hard_floor and self.right_edge is None:
            raise ValueError(
                f"Commandment {self.id!r} is hard_floor=False but has no "
                f"right_edge; soft commandments need both edges"
            )

    def is_flagged(self, score: int) -> tuple[bool, DriftDirection]:
        """Determine flag state and drift direction for a given score."""
        if score <= self.tolerance_min:
            # Drift toward the left edge (or below the hard floor).
            return True, "left"
        if not self.hard_floor and score >= self.tolerance_max:
            return True, "right"
        return False, "none"


@dataclass(frozen=True)
class CommandmentScore:
    """One commandment's score within a single agent's audit."""
    commandment_id: str
    score: int
    reasoning: str
    flagged: bool
    direction: DriftDirection


@dataclass(frozen=True)
class GuardianReport:
    """A full audit report for one agent."""
    agent: str
    scores: list[CommandmentScore]
    any_flagged: bool
    summary: str

    def flagged_scores(self) -> list[CommandmentScore]:
        return [s for s in self.scores if s.flagged]


# ──────────────────────────────────────────────────────────────────────────────
# Default scoring + correction system prompts
# ──────────────────────────────────────────────────────────────────────────────

def build_scoring_system_prompt(
    product_name: str,
    commandments: list[Commandment],
) -> str:
    """
    Generate a default scoring system prompt for a product. Products with
    bespoke voice rules can override by passing their own scoring_system
    to the Guardian constructor.
    """
    rubric = "\n".join(
        f"  {c.id}: {{\"score\": <int>, \"reasoning\": \"<1-2 sentences>\", "
        f"\"flagged\": <bool>, "
        f"\"direction\": \"<left|{('none' if c.hard_floor else 'right|none')}>\"}}"
        for c in commandments
    )
    hard_floor_note = ""
    hard_floors = [c for c in commandments if c.hard_floor]
    if hard_floors:
        names = ", ".join(c.name for c in hard_floors)
        hard_floor_note = (
            f"\n\nHARD FLOOR commandments ({names}) only flag LEFT drift. "
            f"Scores at or above their tolerance_min are always acceptable."
        )

    return (
        f"You are a prompt auditor for {product_name}.\n\n"
        f"Score a specialist agent's system prompt against {product_name}'s "
        f"commandments. Return ONLY valid JSON. No preamble, no markdown.\n\n"
        f"Scoring rubric (1-10 per commandment):\n"
        f"  1-2 : Severe drift toward the left edge\n"
        f"  3   : Approaching left tolerance — FLAGGED\n"
        f"  4-6 : Well-calibrated center — acceptable\n"
        f"  7   : Approaching right tolerance — FLAGGED\n"
        f"  8-10: Severe drift toward the right edge — FLAGGED"
        f"{hard_floor_note}\n\n"
        f"JSON format:\n"
        f"{{\n"
        f'  "agent": "<agent_name>",\n'
        f'  "scores": {{\n{rubric}\n  }},\n'
        f'  "any_flagged": <bool>,\n'
        f'  "summary": "<2-3 sentences: what drifted, what to correct>"\n'
        f"}}"
    )


def build_correction_system_prompt(
    product_name: str,
    voice_rules: str,
    preservation_rules: list[str],
) -> str:
    """
    Generate a default correction system prompt. The minimum-surgical-edit
    discipline is the load-bearing rule — preserve everything except the
    flagged dimension's lines.
    """
    preserve_block = "\n".join(
        f"  {i+1}. {rule}" for i, rule in enumerate(preservation_rules)
    )
    return (
        f"You are a prompt corrector for {product_name}.\n\n"
        f"Voice: {voice_rules}\n\n"
        f"YOUR JOB: Make the MINIMUM SURGICAL EDIT to bring flagged "
        f"dimensions back toward center. A correction should typically "
        f"change 1-3 lines, not rewrite paragraphs.\n\n"
        f"HARD PRESERVATION RULES (violating these means rejection):\n"
        f"{preserve_block}\n\n"
        f"If you cannot address the flagged dimension without violating "
        f"a preservation rule, return the prompt UNCHANGED. A no-op is "
        f"better than a destructive rewrite.\n\n"
        f"Return ONLY the corrected system prompt text. No preamble, no "
        f"explanation."
    )


# ──────────────────────────────────────────────────────────────────────────────
# PromptGuardian
# ──────────────────────────────────────────────────────────────────────────────

class PromptGuardian:
    """
    The portable Prompt Guardian. Configure once per product; call audit()
    on a recurring schedule (weekly is the default cadence in TOP and
    Operator).
    """

    def __init__(
        self,
        product_name: str,
        commandments: list[Commandment],
        prompt_resolver: PromptResolver,
        chat_completion: ChatCompletion,
        *,
        agent_descriptions: Optional[dict[str, str]] = None,
        scoring_system: Optional[str] = None,
        correction_system: Optional[str] = None,
        approval_queue=None,                  # ApprovalQueue or compatible
        correction_action_type: str = "prompt_correction",
    ) -> None:
        if not commandments:
            raise ValueError(
                "PromptGuardian requires at least one Commandment"
            )
        # Validate uniqueness of ids.
        seen: set[str] = set()
        for c in commandments:
            if c.id in seen:
                raise ValueError(f"duplicate commandment id: {c.id!r}")
            seen.add(c.id)

        self.product_name = product_name
        self.commandments = list(commandments)
        self.commandments_by_id = {c.id: c for c in commandments}
        self.prompt_resolver = prompt_resolver
        self.chat_completion = chat_completion
        self.agent_descriptions = dict(agent_descriptions or {})
        self.scoring_system = scoring_system or build_scoring_system_prompt(
            product_name, commandments,
        )
        self.correction_system = correction_system  # optional; product-supplied
        self.approval_queue = approval_queue
        self.correction_action_type = correction_action_type

    # ── Scoring ──────────────────────────────────────────────────────────────

    def score_agent(self, agent_name: str) -> GuardianReport:
        """Score one agent's active prompt. Raises GuardianError on failure."""
        active = self.prompt_resolver(agent_name)
        if not active or not active.strip():
            raise GuardianError(
                f"prompt_resolver returned empty prompt for {agent_name!r}"
            )

        commandment_block = self._render_commandments_for_user_prompt()
        description = self.agent_descriptions.get(agent_name, "")
        user_msg = (
            f"Agent: {agent_name}\n"
            f"Description: {description}\n\n"
            f"Commandments:\n{commandment_block}\n\n"
            f"System prompt to score:\n\n{active}"
        )

        try:
            raw = self.chat_completion(self.scoring_system, user_msg)
        except Exception as exc:
            raise GuardianError(
                f"chat_completion raised on scoring {agent_name}: {exc!r}"
            ) from exc

        return self._parse_score_response(agent_name, raw)

    def correct_agent(
        self,
        agent_name: str,
        report: GuardianReport,
    ) -> Optional[str]:
        """
        Generate a corrected prompt for a flagged agent. Returns the new
        prompt string, or None if not flagged or correction not configured.
        """
        if not report.any_flagged:
            return None
        if self.correction_system is None:
            logger.warning(
                f"agent {agent_name!r} flagged but no correction_system "
                f"prompt configured; skipping correction"
            )
            return None

        active = self.prompt_resolver(agent_name)
        flagged_lines = "\n".join(
            f"  {s.commandment_id}: score {s.score}/10, "
            f"direction: {s.direction}, reasoning: {s.reasoning}"
            for s in report.flagged_scores()
        )
        user_msg = (
            f"Agent: {agent_name}\n\n"
            f"Flagged dimensions:\n{flagged_lines}\n\n"
            f"Current system prompt:\n\n{active}"
        )

        try:
            corrected = self.chat_completion(self.correction_system, user_msg)
        except Exception as exc:
            logger.error(
                f"correction generation failed for {agent_name}: {exc!r}"
            )
            return None

        corrected = corrected.strip() if corrected else ""
        if not corrected:
            logger.warning(
                f"correction generation returned empty for {agent_name}"
            )
            return None
        return corrected

    # ── Audit loop ───────────────────────────────────────────────────────────

    def audit(
        self,
        agents: list[str],
    ) -> dict:
        """
        Score every named agent. For each flagged agent, generate a correction
        and queue it via the approval_queue (if configured). Returns a summary
        dict suitable for logging or surfacing to the operator.
        """
        results: list[dict] = []
        flagged_agents: list[str] = []
        corrections_queued = 0
        scoring_errors = 0

        for agent_name in agents:
            try:
                report = self.score_agent(agent_name)
            except GuardianError as exc:
                results.append({
                    "agent": agent_name,
                    "status": "error",
                    "error": str(exc),
                })
                scoring_errors += 1
                continue

            entry: dict = {
                "agent": agent_name,
                "status": "ok",
                "any_flagged": report.any_flagged,
                "scores": {
                    s.commandment_id: s.score for s in report.scores
                },
                "summary": report.summary,
            }

            if report.any_flagged:
                flagged_agents.append(agent_name)
                corrected = self.correct_agent(agent_name, report)
                if corrected and self.approval_queue is not None:
                    self.approval_queue.queue(
                        action_type=self.correction_action_type,
                        summary=f"Prompt correction for {agent_name}: "
                                f"{report.summary}",
                        payload={
                            "agent": agent_name,
                            "corrected_prompt": corrected,
                            "report": {
                                "scores": [
                                    {
                                        "id": s.commandment_id,
                                        "score": s.score,
                                        "flagged": s.flagged,
                                        "direction": s.direction,
                                        "reasoning": s.reasoning,
                                    }
                                    for s in report.scores
                                ],
                                "summary": report.summary,
                            },
                        },
                    )
                    corrections_queued += 1
                    entry["correction_queued"] = True
                elif corrected:
                    entry["correction_queued"] = False
                    entry["corrected_prompt"] = corrected
                else:
                    entry["correction_queued"] = False

            results.append(entry)

        return {
            "product": self.product_name,
            "agents_audited": len(agents),
            "agents_flagged": len(flagged_agents),
            "corrections_queued": corrections_queued,
            "scoring_errors": scoring_errors,
            "flagged_agents": flagged_agents,
            "results": results,
        }

    # ── Internal ─────────────────────────────────────────────────────────────

    def _render_commandments_for_user_prompt(self) -> str:
        return "\n".join(
            f"  {i+1}. {c.name}\n"
            f"     Center: {c.center}\n"
            f"     Left edge: {c.left_edge}\n"
            f"     Right edge: {c.right_edge or 'N/A (hard floor only)'}\n"
            f"     Tolerance: [{c.tolerance_min}, {c.tolerance_max}]"
            for i, c in enumerate(self.commandments)
        )

    def _parse_score_response(
        self,
        agent_name: str,
        raw: str,
    ) -> GuardianReport:
        """Extract the JSON report. Tolerant of code-fence wrapping."""
        cleaned = self._strip_json_fences(raw).strip()
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise GuardianError(
                f"could not parse scoring response for {agent_name}: "
                f"{exc!r}; raw response was: {raw[:200]!r}"
            ) from exc

        scores_data = data.get("scores", {}) or {}
        if not isinstance(scores_data, dict):
            raise GuardianError(
                f"'scores' field must be a dict in response for {agent_name}"
            )

        scores: list[CommandmentScore] = []
        for c in self.commandments:
            s_data = scores_data.get(c.id)
            if not isinstance(s_data, dict):
                raise GuardianError(
                    f"missing or malformed score for commandment {c.id!r} "
                    f"in response for {agent_name}"
                )
            try:
                score_int = int(s_data.get("score", 0))
            except (TypeError, ValueError):
                raise GuardianError(
                    f"non-integer score for {c.id!r} in response for "
                    f"{agent_name}: {s_data.get('score')!r}"
                )
            if not 1 <= score_int <= 10:
                raise GuardianError(
                    f"score {score_int} for {c.id!r} out of 1-10 range "
                    f"in response for {agent_name}"
                )
            # We compute flagged + direction ourselves rather than trusting
            # the LLM. The LLM scores; the chassis enforces.
            flagged, direction = c.is_flagged(score_int)
            scores.append(CommandmentScore(
                commandment_id=c.id,
                score=score_int,
                reasoning=str(s_data.get("reasoning", "")).strip(),
                flagged=flagged,
                direction=direction,
            ))

        any_flagged = any(s.flagged for s in scores)
        summary = str(data.get("summary", "")).strip()
        return GuardianReport(
            agent=agent_name,
            scores=scores,
            any_flagged=any_flagged,
            summary=summary,
        )

    @staticmethod
    def _strip_json_fences(text: str) -> str:
        """Strip ``` and ```json fences if the LLM wrapped the JSON."""
        text = text.strip()
        if text.startswith("```"):
            # Remove opening fence (```json or ```)
            text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        if text.endswith("```"):
            text = re.sub(r"\n?```$", "", text)
        return text


# ──────────────────────────────────────────────────────────────────────────────
# Errors
# ──────────────────────────────────────────────────────────────────────────────

class GuardianError(RuntimeError):
    """Raised when the Guardian cannot complete an operation."""
