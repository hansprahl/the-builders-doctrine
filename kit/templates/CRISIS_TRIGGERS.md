# CRISIS_TRIGGERS

**The hard floor: the moment your product stops what it is doing and routes the user to a human.** This file specifies the trigger phrases, response text, detection mechanism, surface coverage, and admin-alert protocol for that floor.

Not every product needs a CRISIS_TRIGGERS.md. The interview at [`../onboarding/crisis_interview.yaml`](../onboarding/crisis_interview.yaml) determines whether your product needs one — the gating question is whether your users may speak to the product while in distress, and whether the product's surfaces include freeform text the user can author. If yes, this file is required. If no, mark this file *N/A — does not apply* with a one-paragraph reasoning, and proceed.

The Method does not prescribe what counts as a crisis for your product. It prescribes that *if* your product can encounter one, the response is non-negotiable, deterministic, model-free, and unkillable.

---

## Applicability

<!-- KIT:FIELD name="crisis_applicability" required="true" min_words="60" -->
[State whether this file applies to your product. If yes, name the kind of crisis your users may bring to the product (suicidal ideation, self-harm, substance relapse, domestic violence disclosure, child welfare disclosure, etc.) — be specific. If no, explain why your product cannot encounter user distress in any inbound surface (e.g., "B2B accounting tool with no freeform user text"). Trace to STORY.md the_users — the population you are building for is the source of this answer.]
<!-- KIT:END -->

---

## The crisis floor — non-negotiable rules

These five rules apply to every product that needs a crisis floor. They are not configurable per product — only the contents of the trigger list, response text, and alert recipient are.

1. **Crisis detection runs before anything else.** No LLM call, no orchestrator route, no tool dispatch happens on an inbound message until the crisis check has run and returned False. The check is a substring match against the phrase list — deliberately simple, no model dependency, no API call, no failure mode that could degrade safety under load or outage.
2. **The check covers every inbound text surface.** If a new inbound text surface is added, the crisis check must wrap that surface before anything else runs. Release-blocking, not a follow-up task.
3. **The response is fixed and unconditional.** No model-generated language. No personalization. No variant testing. No A/B. No paywall. No feature gate. Changing the response requires the builder's explicit approval and a dated entry in this file's change history.
4. **An alert fires immediately to the human responsible.** The machine cannot help; the human responsible for the product (or for the user, in cases where the builder has direct relationship with users) gets notified so they can make a personal contact if appropriate.
5. **The detection event is logged at WARNING level.** User identifier (or anonymous token if PII discipline forbids), first N characters of the message, timestamp. Local-file. Never transmitted off-host. Reviewed in the AAR loop for false-negative audit, not for analytics.

---

## Trigger phrases

Substring match, lowercase, on inbound message text. A message triggers if any phrase below is present as a substring after lowercasing the input. The list is intentionally broad on the side of false-positives — a false-positive crisis response is annoying; a false-negative is the failure mode this file exists to prevent.

The trigger list is product-specific. Reference patterns: TOP's list (suicide/self-harm) is in `~/Projects/local-mcp/CRISIS_TRIGGERS.md`. Your list will reflect the kind of crisis your STORY.md `the_users` field named.

<!-- KIT:FIELD name="trigger_phrases" required="conditional_on:crisis_applicability" min_words="60" -->
[List your trigger phrases, organized by category (e.g., direct ideation, plan-language, indirect distress, substance-relapse markers — whatever categories apply to your product). Each phrase is a lowercased substring. The list should be broad enough that a user in genuine distress will trigger the floor, even at the cost of occasional false-positives. Source-of-truth pointer: name the code constant in your product where this list lives (e.g., `_CRISIS_PHRASES` in `agents/telegram_bot.py:122-134`). The doc and the code are the same list — when they diverge, code wins for runtime; doc must re-sync.]
<!-- KIT:END -->

### How to add or remove a phrase

A phrase is added by editing the code constant and updating this file in the same commit. Removing a phrase requires the builder's explicit approval and a documented reason in the change history below — the bias is always toward keeping detection broad.

### What this list does NOT cover (deliberately)

<!-- KIT:FIELD name="trigger_exclusions" required="false" min_words="40" -->
[List the kinds of distress signals you have deliberately not included as substring triggers (e.g., metaphorical language, tone-only signals, rare-edge phrasings) and what other layer catches them (typically a prompt-level safety dimension on the conversational specialist). Naming the exclusions explicitly is what keeps the list honest — without this, the list either over-collects or under-collects and you cannot tell which.]
<!-- KIT:END -->

---

## Response template

The exact text the product sends to the user when a trigger fires. No model generation. No personalization beyond mechanical templating (the builder may template in resource phone numbers, etc., but the words are fixed).

<!-- KIT:FIELD name="response_template" required="conditional_on:crisis_applicability" min_words="60" -->
[Paste the canonical response text here, exactly as the product sends it. This is the source of truth. The code constant in your product (e.g., `_CRISIS_RESPONSE`) is the runtime authority; this file is the spec. They must match.]
<!-- KIT:END -->

### Why this exact wording

<!-- KIT:FIELD name="response_rationale" required="conditional_on:crisis_applicability" min_words="80" -->
[Walk through the response sentence by sentence and name the design choice behind each. Why the opener, why the named resources in the order given, why the closing line. Trace each choice to a STORY.md field — usually formative_crisis (what the builder has lived) or the_users (who the product is for). Without rationale captured, future contributors cannot tell which words are load-bearing and which are aesthetic.]
<!-- KIT:END -->

### What the response does NOT do

<!-- KIT:FIELD name="response_exclusions" required="false" min_words="40" -->
[List explicitly what the response avoids — common patterns include: does not offer to keep talking, does not suggest a follow-up tool inside the product, does not lock the user out, does not chain into any LLM call, does not validate the feeling. Naming exclusions makes it harder for a future feature to drift in.]
<!-- KIT:END -->

---

## Detection mechanism

```
function is_crisis(text):
    lowered = text.lower()
    return any(phrase in lowered for phrase in CRISIS_PHRASES)
```

Properties this implementation guarantees:

- **No model dependency.** Runs offline, runs during API outages, runs faster than any LLM call could complete.
- **Deterministic.** The same input always produces the same output. No sampling, no temperature, no probability threshold.
- **Fail-open by design.** The check wraps the inbound-message handler — runs before user-context resolution, before specialist routing, before any tool. No upstream code path can disable it without a code change.
- **Bypass-resistant.** Substring match on lowercased input with no tokenization beyond `.lower()`. Evasion would require deliberate adversarial phrasing — that is acceptable, since a user trying to evade the filter is not the user this file exists to protect.

If your implementation differs from the reference (e.g., regex match, normalized whitespace), document the difference here and explain why the standard guarantees still hold.

<!-- KIT:FIELD name="detection_implementation_notes" required="false" min_words="40" -->
[Any product-specific implementation notes — language other than Python, special tokenization, multilingual support, etc. Default is the reference implementation above; deviations live here.]
<!-- KIT:END -->

---

## Surfaces wrapped

| Surface | Call site (file:line) | Notes |
|---|---|---|

<!-- KIT:FIELD name="surfaces_table" required="conditional_on:crisis_applicability" min_words="40" -->
[Fill in the table above with every inbound user-text surface in your product, the file:line where the crisis check is invoked, and any per-surface notes. Common surfaces: chat text, message captions on photo/voice uploads, email reply, SMS, web form submission, voice-message transcription. The table is the audit surface — if a row is missing, the surface is unwrapped.]
<!-- KIT:END -->

### Surfaces not yet wrapped (release-blocking when added)

<!-- KIT:FIELD name="surfaces_pending" required="false" min_words="20" -->
[List inbound surfaces that are planned but not yet shipped, so the wrapping requirement is captured before the surface goes live. Empty if all current surfaces are wrapped and no new ones are imminent.]
<!-- KIT:END -->

---

## Admin alert protocol

When the crisis check fires, two things happen:

1. **The crisis response goes to the user immediately**, via the same channel the user is on. No queueing, no approval gate, no delay.
2. **An alert goes to the human responsible** for the product or the user. The alert includes the user identifier, a truncated message excerpt, and a one-line context note.

<!-- KIT:FIELD name="admin_alert_recipient" required="conditional_on:crisis_applicability" min_words="40" -->
[Name the alert recipient (typically the builder for v1 instances; per-tenant administrator for SaaS instances), the channel (Telegram, email, SMS, Slack, paging service), and any suppression rules (e.g., self-alert loops). If your product is multi-tenant and tenants will receive alerts about their own users, document the routing rule here.]
<!-- KIT:END -->

The alert is a feature, not surveillance. It exists because when a person in the builder's reachable network is in crisis, the right thing is to give the builder the chance to make a personal contact. The alert protocol must be re-examined any time the user population grows beyond the builder's reachable network.

---

## Logging

The crisis detection event is logged at `WARNING` level. The log line includes:

- A fixed marker string (e.g., `CRISIS DETECTED`)
- The user identifier (or anonymous token, if PII discipline forbids identifying)
- The first N characters of the triggering message (default 120)

Local file. Never transmitted off-host. Reviewed in the AAR loop for: (1) verifying the trigger list catches what it should, (2) verifying the response fires correctly when triggered. Never used for analytics, model training, or any purpose other than safety audit.

<!-- KIT:FIELD name="logging_notes" required="false" min_words="20" -->
[Any product-specific logging notes — log path, retention, who reviews, how often. Default is local-file, audited in AAR.]
<!-- KIT:END -->

---

## Review cadence

- **Weekly.** Prompt Guardian audit verifies the relevant specialist's prompt does not violate the safety-floor commandment. Catches prompt-level drift; does not exercise the wiring.
- **Monthly.** The builder manually triggers a test crisis message and verifies (a) the response fires, (b) the admin alert fires (modulo self-alert suppression), (c) the log line lands at WARNING. Result recorded in change history.
- **On any change to the inbound-message path.** PRs touching message handlers require this file's review checklist filled in and committed alongside the PR.

### Review checklist (for inbound-path PRs)

- [ ] Does the new code path receive untrusted user-supplied text before any other processing?
- [ ] If yes, does it call `is_crisis(text)` and route to `handle_crisis(...)` before anything else?
- [ ] Does it preserve the property that crisis detection has no LLM dependency?
- [ ] Does it preserve the property that the response is the canonical fixed string from this file, not a model-generated variant?
- [ ] Has the surface been added to the "Surfaces wrapped" table above?

---

## What this file is not

- **Not a clinical screening tool.** The trigger list is engineered to interrupt the immediate trajectory and route to a human, not to make a clinical determination.
- **Not exhaustive.** Indirect ideation, metaphor, and tone-only signals are not caught here — that is the conversational specialist's prompt-level layer. This file handles the unambiguous floor.
- **Not gated.** No commandment, no feature flag, no user setting can disable the crisis check. Even users who opt out of every other product feature still receive the crisis check on every inbound message. This is doctrine, not configuration.

---

## Change history

A dated record of every modification to the trigger list, the response, the detection mechanism, or the alert protocol. Required.

| Date | Change | Author | Reason |
|---|---|---|---|
| YYYY-MM-DD | File created — bootstrap from kit template | builder | initial onboarding |

---

## Trace

- [COMMANDMENTS.md](COMMANDMENTS.md) — the commandment that anchors this file (typically the safety-floor or crisis-floor commandment).
- [STORY.md](STORY.md) `formative_crisis` — what the builder has lived that justifies the floor existing.
- [STORY.md](STORY.md) `the_users` — who the floor protects.
