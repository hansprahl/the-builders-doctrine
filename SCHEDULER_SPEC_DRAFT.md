# Scheduler Primitive — Draft Spec v0.1

**Status.** Draft. Not implemented. Proposed as a Phase 2 chassis primitive for The Builders' Kit. Lives in the doctrine repo as a spec; the implementation will live in Operator first, then back-port to the Kit chassis.

**Author.** Hans Prahl, with AI co-authoring.
**Date.** 2026-05-01.

## Why this primitive exists

A builder using The Builders' Method has scheduled work that does not require their direct attention: weekly competitive-landscape audits, monthly portfolio conformance re-audits, periodic intelligence sweeps, scheduled SBIR-eligibility scans, recurring market research on a defined target list. Today this work either does not happen (the builder is too busy) or it happens manually (the builder loses hours to it on the cadence). Neither is the right answer.

The right answer is an agentic primitive: the builder declares the work as a scheduled task, the chassis fires the agent on cadence, the agent executes against a bounded tool allowlist, the output deposits to a known Drive folder, and the builder receives a notification with a link. The builder reads the report on their own time. The agent never asks the builder to do anything mid-run.

This is not autonomy in the sense the doctrine refuses (Principle #4: irreversible actions require explicit approval, always). It is autonomy bounded by tool allowlists and by approval-queue routing for any write that escapes the report. The agent's writes are constrained to: (a) a markdown report deposited in a designated Drive folder, (b) a notification to the builder. Anything else queues.

This primitive is the operationalization of "designed to be needed less, not more" applied to the builder's own labor. The builder's calendar is the scarce resource; the agent's runtime is not. Move the work from the calendar to the agent.

## Architecture overview

```
┌──────────────────┐
│ Task spec file   │ ← human-authored, declarative
│ tasks/<name>.md  │   (YAML frontmatter + procedure body)
└────────┬─────────┘
         │ scanned by
         ▼
┌──────────────────┐
│ launchd / cron   │ ← durable scheduler, OS-level
│ (per task)       │   (survives restarts, no Claude session)
└────────┬─────────┘
         │ fires
         ▼
┌──────────────────┐    queries    ┌──────────────────┐
│ Runner (python)  │ ─────────────▶│ Per-user memory  │
│ ~300 lines       │               │ (chassis primitive)│
└────────┬─────────┘               └──────────────────┘
         │ calls
         ▼
┌──────────────────┐    audited by  ┌──────────────────┐
│ Anthropic API    │ ◀──────────────│ Prompt Guardian  │
│ (agent execution)│                │ (chassis primitive)│
└────────┬─────────┘                └──────────────────┘
         │ produces
         ▼
┌──────────────────┐    if write   ┌──────────────────┐
│ Tool calls       │ ─────────────▶│ Approval Queue   │
│ (allowlisted)    │   (irreversible)│ (chassis primitive)│
└────────┬─────────┘               └──────────────────┘
         │ on completion
         ▼
┌──────────────────┐               ┌──────────────────┐
│ Drive deposit    │               │ Notification     │
│ (markdown report)│               │ (Telegram/email) │
└──────────────────┘               └──────────────────┘
         │
         ▼
┌──────────────────┐
│ AAR loop         │ ← logs result, claimed confidence,
│ (chassis primitive)│  outcome signal for calibration
└──────────────────┘
```

## Task spec format

Task specs live in `tasks/<name>.md` in the product repo. Markdown body for the procedure (human-readable). YAML frontmatter for the runner. The runner reads frontmatter; the agent reads the procedure body as part of its system prompt.

### Frontmatter schema

```yaml
---
# identity
name: <snake_case_task_name>          # required, unique per repo
description: <one-line summary>        # required, shown in notifications

# scheduling
cron: "<minute> <hour> <dom> <mon> <dow>"   # standard 5-field cron, local time
recurring: <true|false>                # one-shot vs repeating
durable: <true|false>                  # persist across runner restarts (default true)

# output
output_path: gdrive://<folder-path>    # Drive folder for reports
output_filename_template: <YYYY-MM-DD>_<name>.md  # naming convention
notification:
  channel: <telegram|email|none>
  on_success: true
  on_partial: true
  on_failure: true

# capability bounds
tool_allowlist:                        # explicit, no wildcards
  - filesystem.read
  - filesystem.list
  - web.search
  - drive.upload
  - notify.telegram
agent_type: <claude-opus-4-7|claude-sonnet-4-6|claude-haiku-4-5>
bounds:
  max_runtime_sec: 3600                # hard kill at this
  max_tokens: 200000                   # hard cap
  max_api_calls: 50                    # hard cap
  max_drive_writes: 1                  # usually one report per run

# approval posture
approval_queue: <true|false>           # if true, all write actions queue
                                       # if false (read-only audit), agent writes the
                                       # report directly to its declared output_path
                                       # — but ONLY to that path. Anything else still queues.

# memory + AAR
memory_scope: <product|task|none>      # which memory namespace the agent can read
aar_log: <true|false>                  # log claimed confidence + outcome signal
guardian_audit: <true|false>           # subject the system prompt to weekly Guardian audit
---
```

### Procedure body (markdown)

The body of the file is the procedure the agent executes. It becomes part of the agent's system prompt at runtime. Three sections required:

1. **Context** — what the agent should know before starting (links to relevant repo files, prior reports, upstream doctrine)
2. **Procedure** — the numbered steps the agent executes
3. **Output format** — what the report looks like (sections, tables, length bound)

Optional section: **Failure handling** — task-specific guidance on how to handle expected failure modes (e.g., "if a product directory has moved, abort and notify; do not search the filesystem for it").

## Runner pseudocode

```python
def run_task(task_spec_path: Path) -> RunResult:
    spec = parse_task_spec(task_spec_path)
    enforce_bounds(spec.bounds)  # set timeout, token meter, call counter

    system_prompt = build_system_prompt(
        chassis_doctrine=load_doctrine(),
        product_commandments=load_commandments(spec.product),
        procedure=spec.procedure_body,
        tool_allowlist=spec.tool_allowlist,
    )

    if spec.guardian_audit:
        guardian_score = guardian_audit(system_prompt, spec.product_commandments)
        if guardian_score < 0.85:
            notify_failure("Guardian audit failed pre-flight", spec)
            return RunResult.aborted

    memory = load_memory(spec.memory_scope, spec.product) if spec.memory_scope != "none" else None

    try:
        agent_output = anthropic_call(
            model=spec.agent_type,
            system=system_prompt,
            messages=[user_request_from(spec)],
            tools=resolve_tools(spec.tool_allowlist),
            max_tokens=spec.bounds.max_tokens,
            timeout=spec.bounds.max_runtime_sec,
        )
    except BoundsExceeded as e:
        partial = capture_partial(agent_output)
        deposit(partial, spec, status="partial")
        notify(spec, status="partial", reason=str(e))
        if spec.aar_log:
            aar_log_result(spec, partial, status="partial", reason=str(e))
        return RunResult.partial

    # if approval_queue is true, route any write tool calls through queue
    # if approval_queue is false, only the declared output_path write is allowed
    enforce_write_policy(agent_output, spec)

    report = extract_report(agent_output)
    drive_link = upload_to_drive(report, spec.output_path, spec.output_filename_template)
    if spec.notification.on_success:
        notify(spec, status="success", link=drive_link)
    if spec.aar_log:
        aar_log_result(spec, report, status="success", link=drive_link)

    return RunResult.success
```

## Drive folder layout

One folder per product, one subfolder per task, one file per run.

```
gdrive://builders-kit-reports/
├── the-builders-doctrine/
│   ├── artifact-audits/
│   │   ├── 2026-05-01_artifact_audit.md
│   │   ├── 2026-05-29_artifact_audit_rerun.md
│   │   └── ...
│   └── portability-tests/
│       └── ...
├── operator/
│   ├── competitive-landscape/
│   │   ├── 2026-05-08_competitive_landscape.md
│   │   └── ...
│   └── sbir-eligibility/
│       └── ...
├── custer-mcp/
│   └── opposition-monitoring/
│       └── ...
└── top/
    └── ...
```

The folder naming is normative, not optional. A builder applying the Method ships their reports to the same shape so any future builder can read them in order without learning a new layout.

## Notification pattern

Three notification states. All ship the same minimal payload: status + one-line summary + link.

- **success:** `[<task_name>] Report ready. <one-line summary>. <drive_link>`
- **partial:** `[<task_name>] Partial report (reason: <bound_exceeded|tool_failure|guardian_block>). <drive_link>`
- **failure:** `[<task_name>] Task failed before report. <reason>. No deposit. Check runner log: <log_link>`

The builder reads three lines and decides whether to act now or read the report later. The notification never includes the report body — links only. This forces the builder to actually read the report instead of triaging from a notification feed.

## Approval queue seam (Principle #4 enforcement)

Two modes per task spec:

**`approval_queue: false` (read-only audit / research mode).** The agent's only allowed write is the declared `output_path` deposit. Any tool call that attempts a write outside `output_path` is rejected by the runner before reaching the API for execution. This is the right mode for: artifact audits, competitive intelligence, market research, opposition monitoring, SBIR-eligibility scans, anything where the output is a report.

**`approval_queue: true` (proposes-actions mode).** The agent may propose write actions (send an email, create a calendar event, send a Telegram blast, charge a card). Each proposed write is captured as an Approval Queue entry. The agent's report includes the proposed actions; the deposit happens; the notification tells the builder there are queued actions to review. The builder reviews on their time and approves or rejects.

**The chassis-level invariant:** an agent run can never directly produce an irreversible side effect outside its declared `output_path`. Either the action is the report itself (read-only) or the action queues for the builder. Principle #4 is enforced in the runner, not in the agent's prompt.

## Failure handling

Three classes of failure. Each handled deterministically:

1. **Bounds exceeded** (max_runtime, max_tokens, max_api_calls). Runner kills the agent, captures whatever partial output exists, deposits as `<filename>.partial.md`, sends partial notification. Bounds are deliberately tight in the task spec — exceeding them is signal that the task is wrong, not that the agent is wrong.

2. **Tool failure** (Drive auth fails, web search 503s, filesystem path missing). Runner catches the tool error, agent receives the error in its tool-result channel, agent decides whether to abort or work around. If the agent aborts, partial deposit + partial notification. If the agent works around (fallback to a different tool, retry), the run continues — the AAR log captures both attempts.

3. **Guardian block** (system prompt fails Guardian audit before the agent runs). Runner does not call the API. No deposit. Failure notification with the Guardian's flagged drift. Builder fixes the prompt or commandments and re-enables the task. This is the chassis refusing to run a task whose ethics are out of conformance — a feature, not a bug.

## Integration with existing chassis primitives

- **Per-user memory.** Tasks declare `memory_scope`. Read-only audits typically scope to `product` (read everything in that product's memory) or `none`. Proposes-actions tasks may need wider scope. Memory writes from inside a scheduled task happen through the AAR log, not through ad-hoc graph writes.
- **Prompt Guardian.** Every task's system prompt is treated as a specialist prompt and audited weekly. A task whose Guardian score drops below threshold is auto-disabled until the builder reviews. Drift correction queues per existing Guardian pattern.
- **AAR loop.** Every task run logs claimed confidence (the report's CONFIDENCE block) and waits for an outcome signal (the next run's diff, the builder's reaction, a metric). Calibration accumulates per-task over time. A task whose claimed confidence consistently overshoots actual outcomes is flagged for prompt review.
- **Approval Queue.** See above. Write actions outside `output_path` always route through the queue.
- **Crisis Floor.** Does not apply — scheduled tasks are not user-facing. The crisis surface is the user/agent boundary, not the agent/runner boundary. Documented here for completeness.
- **Named specialists.** A scheduled task is itself a named specialist. The task's `name` is the specialist name. The task's procedure body is the specialist's system prompt. The task's tool_allowlist is the specialist's tool allowlist. This means scheduled tasks fit cleanly into the existing specialist registry — they just have a cron trigger instead of a routing trigger.

## Out of scope for v0.1

- Multi-step tasks (task A's output triggers task B). Defer to v0.2.
- Web UI for task management. CLI + file-based for v0.1.
- Real-time streaming of partial output. Deposit-on-completion only.
- Cross-product report aggregation (e.g. "every Sunday, summarize the week's reports across all products"). Defer to v0.3 once enough single-task data exists to know what aggregation matters.

## First concrete task

`tasks/2026-05-29_artifact_audit_rerun.md` — the artifact audit re-run committed to publicly in `ARTIFACT_AUDIT_2026-05-01.md`. Authored alongside this spec to validate that the format works before the runner exists.

When the runner ships, this task spec gets picked up and the audit runs autonomously. Until then, the task spec is a precise statement of what the runner needs to support.

## What this spec does NOT yet decide

These are intentionally open and deferred to implementation:

- **Where the runner lives.** Operator (its specialist registry is the natural home) vs. local-mcp (its tool surface is closer to the API needs) vs. a new dedicated repo (`hansprahl/builders-runner`). Each has tradeoffs — Operator wins on chassis integration, local-mcp wins on tool plumbing, dedicated repo wins on portability for other Method adopters. **Recommendation:** Operator first (it's where the autonomous-business-agent thesis lives), then extract to a portable runner when Phase 2 of the Kit ships.
- **Auth posture.** The runner needs API keys (Anthropic), Drive auth (OAuth), Telegram bot token. Where these live and how they rotate is a SECURITY.md update, not a spec decision.
- **The exact YAML library + parser.** Pick during implementation.
- **Whether `tool_allowlist` enumerates tools or tool *categories*.** Categories are easier to reason about; enumerated tools are safer. Probably both — categories for ergonomics, with enumerated overrides for tasks that need narrower scope.

## Next steps after this spec lands

1. Build the v0.1 runner in Operator (~2-3 sessions).
2. Run the 2026-05-29 audit task against it as the first real exercise.
3. Add a second task spec for a recurring research job (e.g., weekly competitive-landscape audit for Operator's market) to test the recurring path.
4. Back-port the runner to the Kit chassis spec when Kit Phase 2 starts.
