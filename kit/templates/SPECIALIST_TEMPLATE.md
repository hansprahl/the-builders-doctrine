# SPECIALIST — New Specialist Build Checklist

**Run this once per specialist, not once per product.** This template differs from STORY/COMMANDMENTS/REFUSAL/CRISIS — those are bootstrapped once when the builder onboards. This is a *recurring* artifact: every time the builder adds a named agent to the product, they fill out a copy of this template, attach it to the build PR, and merge it alongside the specialist's code.

The interview at [`../onboarding/specialist_interview.yaml`](../onboarding/specialist_interview.yaml) walks the builder through the fields. The specialist's system prompt produced by the interview must pass the Prompt Guardian's tolerance bands on every commandment dimension before merge.

---

## Why this template exists

A specialist is a named agent with a tool allowlist, a system prompt, and a defined scope inside the product's chassis. Letting a specialist drift from doctrine — letting it own a domain it should not, hold tools it should not, or self-approve its own actions — is the most common way a chassis stops being trustworthy.

This template enforces five disciplines:

1. **Naming convention** — every specialist has a name that matches the product's pattern (callsign / snake_case / domain-noun — set by the product).
2. **Explicit scope** — what it owns AND what it does not own, named against existing specialists.
3. **Tool allowlist** — explicit, minimal, no wildcards, no `approve()`/`reject()`. Specialists never self-approve.
4. **Doctrine integration** — every commandment is wired in at build time and audited at runtime.
5. **Refusal scope-lock** — every new feature, including a new specialist, runs through the refusal audit before merge.

---

## 1. Identity

- **Name:** (per the product's naming convention — see your product's CLAUDE.md or COMMANDMENTS.md)
- **Domain:** (one sentence — what this specialist owns)
- **Why a new specialist?** (which existing specialist would otherwise handle this and why splitting is right)

<!-- KIT:FIELD name="specialist_identity" required="true" min_words="60" -->
[Fill in name, domain, and the case for splitting. If you cannot make the case for splitting, the work probably belongs in an existing specialist — extend it, do not fork it.]
<!-- KIT:END -->

### Hard-floor applicability gates

Some products have hard floors that change the rest of this template (voter PII, multi-tenant isolation, financial actions, regulated content, crisis surfaces). Answer the gates that apply to your product. If a gate is not on your product's list, mark it n/a.

<!-- KIT:FIELD name="hard_floor_gates" required="true" min_words="40" -->
[For each hard-floor your product enforces (per its COMMANDMENTS.md), state whether this specialist is in scope. Examples:
- Touches user PII? (yes/no — if yes, the relevant data-isolation discipline applies)
- Sends outreach / takes external actions? (yes/no — if yes, every action queues for approval)
- Operates per-tenant in a multi-user deployment? (yes/no — if yes, ContextVar discipline applies)
- Touches a regulated surface (clinical, legal, financial, voter)? (yes/no — if yes, the corresponding refusal-scope-lock category applies)
Each yes triggers a discipline section below; each no allows the section to be marked n/a with reasoning.]
<!-- KIT:END -->

---

## 1.5. MCA position

The specialist's position in the product's unit structure per Mission Command Architecture. If the product is single-agent or pre-MCA, mark these fields `na_with_reasoning` rather than guessing. Reference: `~/Projects/the-builders-doctrine/MISSION_COMMAND_ARCHITECTURE.md` — specifically `## The Authority Gradient`, `## Roles per echelon`, and `## The Staff Channel`.

### Authority tier

<!-- KIT:FIELD name="authority_tier" required="true" min_words="20" -->
[One of: `officer` (sets intent, allocates resources, calls done) / `nco` (translates intent to task, QCs subordinate output, re-tasks within scope) / `soldier` (executes within task spec, surfaces ambiguity, "I don't know" as stop signal) / `staff` (advisory authority within domain, no chain-of-command position) / `na_with_reasoning` (single-agent product, MCA does not yet apply). State the tier and one sentence on why this tier and not the next one up or down.]
<!-- KIT:END -->

### Role

<!-- KIT:FIELD name="role" required="true" min_words="20" -->
[The specific functional role per MCA's role taxonomy. Command-channel roles: `PL` / `SL` / `soldier` / `CC` / `XO` / `1SG` / `PSG` / `BC` / `CSM`. Staff-channel roles: `s2_intel` / `s3_ops` / `s4_logistics` / `s6_signal` / `wo_legal` / `wo_ethics` / etc. Or a product-specific functional name (`drake`, `sentinel`, `marshall`, `halsey`). Document the doctrinal lineage in a sentence (e.g., "drake is the S-2/OPFOR-shape — intelligence and adversary analysis"). Per the discipline note in MCA's naming convention: do not use Army ranks (CPT, SFC, MSG) as the role identifier.]
<!-- KIT:END -->

### Channel

<!-- KIT:FIELD name="channel" required="true" min_words="20" -->
[One of: `command` (line agent in the chain of command — PL/SL/soldier-shape) / `staff` (advisory-channel agent — S-staff or Warrant-Officer-shape; advises the line, never overrides). If staff-channel, name the line commander whose decisions this specialist advises. Staff agents follow the advisory-never-override-always-log discipline (MCA `## The advisory-never-override-always-log rule`).]
<!-- KIT:END -->

### Escalation threshold

<!-- KIT:FIELD name="escalation_threshold" required="true" min_words="40" -->
[The conditions under which this specialist escalates up the gradient rather than resolving in scope. Examples by tier: Soldier — "If the task as written cannot be executed truthfully, return `I don't know` with reasoning." NCO/SL — "If a soldier blocks repeatedly on the same task class, escalate to PL. If a re-do has been routed five times to the same soldier without success, escalate." Officer/PL — "If reality diverges from commander's intent, RFI up rather than rewrite intent." Staff — "If a line decision contradicts a hard floor (refusal-list item, crisis-floor breach), flag with HIGH confidence and log; do not attempt to override." Each escalation is also a logged event per the violation-logging rule.]
<!-- KIT:END -->

### Disciplined-initiative scope

<!-- KIT:FIELD name="disciplined_initiative_scope" required="true" min_words="40" -->
[What this specialist may revise without escalating. Per ADP 6-0's "disciplined initiative" principle, each tier exercises bounded autonomy. Examples: Soldier — "May choose between equivalent execution paths under task spec; may NOT redefine the task." NCO/SL — "May re-task a soldier when output fails QC; may NOT reassign across squads or rewrite intent." Officer/PL — "May revise the plan when situation diverges; may NOT rewrite commander's intent." Staff — "May escalate confidence on a flagged risk; may NOT override line decisions." State the scope and the bright line where authority stops.]
<!-- KIT:END -->

---

## 2. Scope boundary

- **Owns:** (the specific domains)
- **Does NOT own:** (explicit overlap with existing specialists — name them)
- **Cross-specialist calls:** (which other specialists does this one consume context from?)
- **Handoff triggers:** (when does this specialist surface "that's not mine" and route back to the orchestrator?)

<!-- KIT:FIELD name="scope_boundary" required="true" min_words="80" -->
[Be explicit. "Generic intelligence" is not a scope; "competitive analysis on named competitors with public web surfaces" is. Overlap is the most common drift; naming overlapping specialists by name forces the boundary.]
<!-- KIT:END -->

---

## 3. Tools

- **Existing tools needed:** (list from your product's tool registry — be minimal)
- **New tools required:** (list what needs to be built)
- **Approval-gated tools:** (every tool with a real-world effect routes through your product's approval queue)
- **Tools deliberately excluded:** (especially `approve()` and `reject()` — specialists never self-approve)

<!-- KIT:FIELD name="tools" required="true" min_words="80" -->
[Enumerate. The tool allowlist is the security boundary; vague allowlists are the same as no allowlist. For each new tool, state what it does, what it returns, and whether it has a real-world effect (and therefore queues).]
<!-- KIT:END -->

### Reversibility test for approval routing

For each tool with a possible real-world effect: *"If this runs by mistake, can the user reverse it in under 60 seconds for under $0?"* If no, it queues. The test is mechanical, not aesthetic. A tool that posts to social media queues. A tool that sends email queues. A tool that reads a public webpage does not queue.

<!-- KIT:FIELD name="approval_audit" required="conditional_on:tools" min_words="40" -->
[For each tool that potentially has a real-world effect, run the reversibility test and document the result. List the queue path for each.]
<!-- KIT:END -->

---

## 4. Doctrine integration

Every specialist must wire into the items below. Anything left unchecked is a release blocker. The exact items are product-specific (your product's COMMANDMENTS.md is the authority); the categories below are the universal pattern.

| Category | What to build | Status |
|---|---|---|
| **Named registration** | Specialist file at the product's specialist path; imported into the orchestrator/router | [ ] |
| **Tool allowlist** | `TOOLS = [...]` (or product equivalent) at module level, explicit, no wildcards, no `approve`/`reject` | [ ] |
| **Commander's intent / direction surface** | SYSTEM_PROMPT explicitly frames the specialist as taking direction from a commander/operator/principal, surfacing ambiguity rather than resolving | [ ] |
| **Approval queue routing** | Every irreversible action this specialist can take is routed through the product's approval queue | [ ] |
| **CONFIDENCE block** | SYSTEM_PROMPT includes the standard CONFIDENCE/REASONING block so every recommendation is calibrated | [ ] |
| **Per-tenant context (if multi-user)** | Specialist reads tenant biographical context via the user-context layer; never hardcodes voice or identity assumptions; `ContextVar` set at entry, `LookupError` on unset | [ ] |
| **Refusal scope-lock** | New feature spec attached as a REFUSAL_LIST audit entry before merge | [ ] |
| **Prompt Guardian wiring** | Specialist's prompt path registered in the product's Prompt Guardian; weekly audit covers it | [ ] |
| **Reflection Gate (if used)** | Specialist responses route through the Reflection Gate before delivery; Gate evaluates against this product's commandments | [ ] |
| **Runtime visibility (if applicable)** | If the product has a duty-roster / cockpit / telemetry surface, the specialist is wired in (e.g., `mark_start`/`mark_end`) | [ ] |
| **Handoff log (if applicable)** | Cross-specialist calls write to the handoff log | [ ] |

<!-- KIT:FIELD name="doctrine_wiring" required="true" min_words="100" -->
[Walk through your product's actual doctrine list (from COMMANDMENTS.md and the product's CLAUDE.md "before adding a specialist" checklist). Confirm each item. Flag any item where the specialist deviates and explain why.]
<!-- KIT:END -->

---

## 5. Hard-floor disciplines

Each section below is conditional — it applies only if the corresponding gate in §1 returned yes. If marked n/a, populate the field with a one-paragraph reasoning.

### 5a. User-data isolation

<!-- KIT:FIELD name="data_isolation" required="conditional_on:hard_floor_gates" min_words="40" -->
[If the specialist touches user PII (voters, customers, tenants, etc.): name the tools that touch user rows, the aggregation pattern that reduces individual rows to counts/segments before any LLM sees them, the chain-of-custody logging path, and the failure mode if aggregation is bypassed. If the specialist touches no user PII: mark n/a with reasoning.]
<!-- KIT:END -->

### 5b. Outreach / external action approval

<!-- KIT:FIELD name="outreach_discipline" required="conditional_on:hard_floor_gates" min_words="40" -->
[If the specialist sends outreach or takes external actions: list every outreach surface (SMS, email, social, press, etc.), the queue path for each, the approval UX (where the operator sees the queued action), and the no-bypass guarantee — that is, that no code path could fire an outreach without queueing. If no outreach: mark n/a.]
<!-- KIT:END -->

### 5c. Per-tenant isolation (multi-user only)

<!-- KIT:FIELD name="tenant_isolation" required="conditional_on:hard_floor_gates" min_words="40" -->
[If the product is multi-tenant: confirm the specialist sets `ContextVar` for the active tenant at entry, raises `LookupError` on unset (no silent fallbacks), reads only the current tenant's memory namespace, tags every memory write with the tenant's user_id, and carries per-tenant scoping on every external-API call. Confirm the specialist runs cleanly for two distinct tenant contexts in the same process — or name the failure mode and queue a fix before SaaS launch. If single-tenant: mark n/a.]
<!-- KIT:END -->

### 5d. Regulated-surface compliance

<!-- KIT:FIELD name="regulated_compliance" required="conditional_on:hard_floor_gates" min_words="40" -->
[If the specialist touches a regulated surface (clinical, legal, financial, voter, child-welfare, etc.): name the regulation, the compliance discipline the product enforces (e.g., voter-file CRS isolation, HIPAA, fair-lending), and the audit trail required. If unregulated: mark n/a.]
<!-- KIT:END -->

---

## 6. State consumption

Most products thread some shared state through every specialist call (a snapshot, a session, a workspace context, a campaign brief, a venture context). Specify what this specialist reads from and writes to that shared state.

<!-- KIT:FIELD name="state_consumption" required="true" min_words="60" -->
[Name the shared state object. List the fields this specialist reads. List the fields it writes/updates. Specify stale-data handling: what does this specialist do if a required field is missing or outdated — refuse, surface the gap to the operator, fall back to a safe default? If your product has no shared state object yet, name that as a gap and mark this section n/a-pending.]
<!-- KIT:END -->

---

## 7. System prompt

Write the full SYSTEM_PROMPT here. Must include:

- **Role line:** product-specific, names the specialist and the product context
- **Domain scope and explicit non-scope**
- **Direction posture:** surfaces ambiguity rather than resolves; takes commander's intent from the operator
- **CONFIDENCE/REASONING block requirement**
- **Approval queue:** every real-world effect goes through the queue, never directly
- **Refusal-scope-lock:** cite REFUSAL_LIST.md when a feature is touched
- **Voice:** per the product's COMMANDMENTS.md voice rules
- **Hard-floor disciplines:** restate the ones that apply (PII isolation, outreach queue, tenant isolation, regulated compliance) — short and explicit
- **Confidentiality of internals:** if the product policy is that specialist names/callsigns are not surfaced to users unless directly asked, state that

<!-- KIT:FIELD name="system_prompt" required="true" min_words="200" -->
[Write the full SYSTEM_PROMPT. The Prompt Guardian will score this against every commandment dimension at merge time. Drift on any soft commandment queues a correction; drift below a hard floor is a release blocker.]
<!-- KIT:END -->

---

## 8. Refusal scope-lock entry

Before merge, copy your product's refusal-list audit template, fill it out for this specialist's introduction, and commit it alongside the build PR. Unchecked refusal boxes block merge.

<!-- KIT:FIELD name="refusal_audit_entry" required="true" min_words="60" -->
[Paste your product's refusal-audit template (from REFUSAL_LIST.md or REFUSAL_AUDIT.md), filled in for this specialist. Include both the inherited refusals (engagement-max, surveillance, parasocial) and the product-specific refusals. State PASS / REVISE / REFUSE.]
<!-- KIT:END -->

---

## 9. Validation

Before merging:

- [ ] Specialist file at the product's specialist path defines SYSTEM_PROMPT, TOOLS, and `run()` (or product-equivalent entry point)
- [ ] Imported and registered in the orchestrator / router
- [ ] Tool allowlist excludes self-approve tools (specialists never self-approve)
- [ ] Every tool with a real-world effect routes through the approval queue
- [ ] CONFIDENCE block parses correctly from a test response
- [ ] Reflection Gate run on a test response — no commandment drift
- [ ] Prompt Guardian scored the new prompt — no commandment dimension drifts below tolerance
- [ ] Hard-floor checks (PII, outreach, tenant, regulated) tested where applicable — drift below floor is a release blocker
- [ ] State-consumption: specialist reads the shared state correctly; stale-data handling tested
- [ ] If applicable: cockpit / duty-roster / handoff-log surfaces show the new specialist correctly under load
- [ ] Refusal scope-lock entry committed with the build PR
- [ ] If multi-tenant: specialist runs cleanly for two distinct user_id contexts in the same process (or the gap is explicitly logged)

---

## Reference

- [COMMANDMENTS.md](COMMANDMENTS.md) — your product's commandments; every specialist inherits them
- [REFUSAL_LIST.md](REFUSAL_LIST.md) — the refusal audit template this specialist's introduction must pass
- [STORY.md](STORY.md) — the source-of-truth bio; the specialist's voice is downstream of this
- `~/Projects/the-builders-doctrine/PROMPT_DOCTRINE.md` — universal structural rules every prompt follows
