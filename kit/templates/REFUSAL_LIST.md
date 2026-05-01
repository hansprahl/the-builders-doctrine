# REFUSAL_LIST

**What your product will never do, enumerated.** The refusal list is the most load-bearing part of the doctrine — it is what survives pressure to compromise. [COMMANDMENTS.md](COMMANDMENTS.md) carries the high-level *categories*; this file carries the specific *items* the Guardian audits against.

The Method assumes refusals are *derived*, not borrowed. Every refusal below should trace to a field in [STORY.md](STORY.md) — most often `formative_crisis` (what you have lived that you will not let your product reproduce) or `the_users` (what they need the product to never do, because of where they are coming from).

If a refusal cannot be traced to STORY, it is borrowed authority — strike it. If a STORY field implies a refusal that is not written here, write it. The interview at [`../onboarding/refusal_interview.yaml`](../onboarding/refusal_interview.yaml) walks builders through generating refusal items from STORY.md fields.

---

## Inheritance from the canonical refusal list

Three refusal categories live upstream in `~/Projects/the-builders-doctrine/THE_BUILDERS_DOCTRINE.md` II.8 and are inherited by every product in the portfolio. They are the floor — your product-specific refusals extend them, never replace them.

1. **Engagement-maximization** — variable rewards, streaks-as-dopamine, dark patterns, anything that makes the product feel needed for its own sake.
2. **Surveillance** — behavioral tracking sold to third parties, consent-by-dark-pattern, retention beyond what the user explicitly requested.
3. **Parasocial replacement** — a product that positions itself as a substitute for human relationships rather than scaffolding for them.

Every product-specific refusal below extends or specializes one of these three, or names a fourth category derived from your STORY.md.

---

## Product-specific refusals

Add one entry per refusal. Each entry is its own KIT:FIELD block so the scorer can audit completeness independently.

### Refusal 1

<!-- KIT:FIELD name="refusal_1" required="true" min_words="40" -->
[Describe the refusal. State the behavior the product will never perform, the specific edge case the refusal covers, and which STORY.md field it traces to. Example form (not content): "The product will not roleplay as a deceased loved one. Even if the user explicitly requests it. Traces to formative_crisis (the user population includes bereaved consumers; impersonation of the dead is a parasocial harm pattern the product was built specifically not to reproduce)."]
<!-- KIT:END -->

### Refusal 2

<!-- KIT:FIELD name="refusal_2" required="true" min_words="40" -->
[Describe the refusal. STORY trace required.]
<!-- KIT:END -->

### Refusal 3

<!-- KIT:FIELD name="refusal_3" required="true" min_words="40" -->
[Describe the refusal. STORY trace required.]
<!-- KIT:END -->

### Refusal 4 (optional)

<!-- KIT:FIELD name="refusal_4" required="false" min_words="40" -->
[Optional fourth refusal. Add more KIT:FIELD blocks (refusal_5, refusal_6, ...) as needed. The scorer counts populated refusals; min_count is set in coverage.py.]
<!-- KIT:END -->

---

## Audit template

Every feature added to the product runs through this template before merge. If any box is unchecked, the feature does not ship without explicit builder override (logged in the audit history below with reasoning).

```
### Feature: [name]
Date: [YYYY-MM-DD]
Proposed by: [builder / Claude / contributor]
Linked PR or commit: [if applicable]

Inherited refusals:
- [ ] Engagement-max: feature does NOT introduce variable rewards,
      dopamine streaks, or dark patterns. Reasoning: ...
- [ ] Surveillance: feature does NOT collect or transmit behavioral data
      beyond what the user explicitly requested. Reasoning: ...
- [ ] Parasocial: feature does NOT position the product as a substitute
      for human relationships. Reasoning: ...

Product-specific refusals:
- [ ] Refusal 1: ...
- [ ] Refusal 2: ...
- [ ] Refusal 3: ...

Verdict: PASS / REVISE / REFUSE
```

---

## Audit history

Past audits accumulate below, newest first. The audit trail is doctrine — not paperwork.

<!-- KIT:AUDIT_LOG -->
[Entries appended here over the lifetime of the product. The first entry is typically the bootstrap audit confirming initial features pass the refusal list.]
<!-- KIT:END -->

---

## Trace

The refusal list is the operative form of [STORY.md](STORY.md) `formative_crisis` and `the_users` fields. If a future builder reads this file and cannot tell what crisis or user-need each refusal came from, the trace is broken — fix the entry before continuing.
