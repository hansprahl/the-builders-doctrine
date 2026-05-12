---
# identity
name: artifact_audit_rerun_2026_05_29
description: Re-run the artifact audit committed publicly in ARTIFACT_AUDIT_2026-05-01.md and produce a diff against baseline.

# scheduling
cron: "13 9 29 5 *"
recurring: false
durable: true

# output
output_path: gdrive://builders-kit-reports/the-builders-doctrine/artifact-audits/
output_filename_template: 2026-05-29_artifact_audit_rerun.md
notification:
  channel: telegram
  on_success: true
  on_partial: true
  on_failure: true

# capability bounds
tool_allowlist:
  - filesystem.read
  - filesystem.list
  - drive.upload
  - notify.telegram
agent_type: claude-opus-4-7
bounds:
  max_runtime_sec: 3600
  max_tokens: 200000
  max_api_calls: 30
  max_drive_writes: 1

# approval posture — read-only audit, no proposed actions outside the deposit
approval_queue: false

# memory + AAR
memory_scope: product
aar_log: true
guardian_audit: true
---

# Re-run artifact audit — 2026-05-29

## Context

This task re-runs the artifact audit committed publicly in `ARTIFACT_AUDIT_2026-05-01.md`. Read the baseline audit, the canonical Method document, and walk the four products to score current state.

Files to load before scoring:
- `~/Projects/the-builders-doctrine/ARTIFACT_AUDIT_2026-05-01.md` — baseline scores, dated remediation plan, methodology
- `~/Projects/the-builders-doctrine/THE_BUILDERS_METHOD.md` Section IV — canonical required-artifact list

Products to walk:
- TOP — `~/Projects/local-mcp/`
- Operator — `~/Projects/operator/`
- Custer — `~/Projects/custer-mcp/`
- Rubicon — `~/Projects/rubicon/`

Required artifacts to score (per product, eight cells):
1. `STORY.md`
2. Commandments file (extracted COMMANDMENTS.md, or inline-in-CLAUDE.md, or missing)
3. Refusal list (per-product file, upstream-doctrine pattern with audit log, or missing)
4. `SPECIALIST_TEMPLATE.md`
5. Crisis trigger document (`CRISIS_TRIGGERS.md`, or explicit n/a declaration in CLAUDE.md or SECURITY.md, or missing)
6. `AGENT_DOCTRINE.md`
7. `PROMPT_DOCTRINE.md`
8. `SECURITY.md`

Score each cell:
- ✓ — exists as a dedicated file with real content
- ⚠ — inline-only OR exists but thin
- ✗ — missing entirely
- n/a — not applicable, with explicit declaration

Baseline scores (2026-05-01) for diff:
- TOP: 5/8
- Operator: 2/8
- Custer: 2/8
- Rubicon: 1/8
- Portfolio mean: 31%

## Procedure

1. Load the baseline and Method Section IV. Confirm the artifact list has not changed since 2026-05-01.

2. For each of the four products, walk the repo root and (where relevant) the top three directory levels. Score each of the eight required artifacts using the legend above.

3. Compute the diff per product (cells changed: ✗→⚠, ⚠→✓, etc.) and the overall portfolio mean delta vs the 31% baseline.

4. Score each remediation tier from the baseline plan against today (2026-05-29):

   **Tier 1** (was due 2026-05-08):
   - Extracted COMMANDMENTS.md in TOP, Operator, Custer, Rubicon
   - Extracted CRISIS_TRIGGERS.md in TOP and Custer
   - Explicit n/a declarations in Operator and Rubicon for crisis surface
   - Refusal-list architecture decision recorded in THE_BUILDERS_METHOD.md (per-product vs upstream pattern)

   **Tier 2** (was due 2026-05-15):
   - Custer's STORY.md authored
   - SPECIALIST_TEMPLATE.md authored for Operator and Custer
   - PROMPT_DOCTRINE consolidation decision recorded

   **Tier 3** (was due TODAY, 2026-05-29):
   - AGENT_DOCTRINE.md authored for Operator
   - AGENT_DOCTRINE.md authored for Custer

   For each tier, mark: **met** / **partial** (with what specifically missed) / **missed**.

5. Identify cross-cutting findings worth feeding into v1.2 of the doctrine or v1.0 of the Method:
   - New gaps not present at baseline
   - Architecture changes the remediation surfaced (e.g., refusal-list pattern decision)
   - Anything that changes the v1.0 release readiness

6. Write the report at the declared `output_path` with the declared filename. Sections required:

   - **Header** — date, link to baseline, summary line: "met" / "partial — N gaps" / "missed — public commitment not honored"
   - **Coverage matrix** — per-product, per-artifact, with diff arrows where cells changed since baseline
   - **Per-product diff** — short paragraph per product describing what changed
   - **Tier-by-tier remediation status** — bullets with met / partial / missed
   - **Cross-cutting findings** — for v1.2 / v1.0 input
   - **Recommendation** — continue toward v1.0 / commission third-party audit / extend remediation
   - **CONFIDENCE block** — agent's claimed confidence in the audit, plus reasoning

7. Send the notification per the spec's success/partial/failure pattern. Notification body: `[artifact_audit_rerun_2026_05_29] <status>. <one-line summary>. <drive_link>`.

8. Do NOT commit, push, or modify any product file. The audit is measurement, not remediation. If something looks broken in a product, surface it in the report; don't fix it.

## Output format

Markdown. ≤2000 words. Structure as in step 6 above. Tables for the coverage matrix and per-product diff. CONFIDENCE block at the end with `confidence: 0.0-1.0` and `reasoning: <short paragraph>`.

## Failure handling

- If a product directory has moved or been renamed, abort scoring for that product and note in the report. Do not search the filesystem for it.
- If `ARTIFACT_AUDIT_2026-05-01.md` cannot be loaded, abort the entire task with a failure notification. The diff is meaningless without the baseline.
- If the Guardian pre-flight audit fails, the runner aborts before the agent runs (per spec). No deposit.
- If `bounds.max_runtime_sec` is hit, deposit whatever partial coverage matrix exists with status="partial" and note which products were not yet scored.

## Voice

Terse. Honest before comfortable. State facts; let the builder decide. No cheerleading on tier completion, no doom-tone on misses. Stoic posture matches the doctrine this audit is auditing against.

## Why this task is the first one

This task is the first concrete instance of the SCHEDULER_SPEC_DRAFT format. It is also the public commitment the 2026-05-01 audit made in writing. Building it as a task spec — even before the runner exists — proves that the spec format can express a real, dated, accountable piece of agent work. If the spec format breaks down at the first concrete task, the spec is wrong; revise the spec, not the task.
