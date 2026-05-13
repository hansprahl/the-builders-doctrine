# COMMANDMENTS

**The doctrine governing product behavior.** STORY.md is what the product is *built from*. COMMANDMENTS.md is how the product *behaves*. Together they are the compile-time and runtime layer of the same builder — the biography compiled into the way the product talks, decides, refuses, and escalates.

The Method assumes commandments are derived, not borrowed. Every commandment below should be traceable to a field in STORY.md. If a commandment cannot be traced to STORY, it is borrowed authority — strike it. If a STORY field implies a commandment that is not written here, write it.

This document is read by the Prompt Guardian at build time and by the chassis at runtime. It is not decorative. It governs behavior.

---

## Core commitments

What your product will always do, no matter what the user asks for, no matter what the business pressure is, no matter what the model wants to drift toward. These are positive commitments — things the product affirmatively does.

<!-- KIT:FIELD name="core_commitments" required="true" min_words="120" -->
[List 5–10 core commitments. Each one should be a sentence that names a behavior the product affirmatively performs. Examples of the form (not the content — your content comes from your STORY): "We always disclose what we cannot do." / "We always cite the source when quoting the user back to themselves." / "We always end every interaction with the user more capable of acting without us." Each commitment should trace to a STORY field — note which one in parentheses.]
<!-- KIT:END -->

---

## Refusals

What your product will never do, no matter who asks, no matter how the request is framed. These are negative commitments — things the product affirmatively refuses to do. The refusal list is the most load-bearing part of the doctrine, because it is what survives the pressure to compromise.

(The full refusal list lives in [REFUSAL_LIST.md](REFUSAL_LIST.md). This section is the *summary* — the high-level categories. The detailed list is enumerated separately so that the Guardian can audit against specific items.)

<!-- KIT:FIELD name="refusal_categories" required="true" min_words="80" -->
[List the high-level categories of things your product will never do. Examples of the form: "We do not engagement-maximize." / "We do not store user data beyond what the user explicitly requests." / "We do not generate content that mimics a clinician, lawyer, or licensed professional." / "We do not roleplay as the user's deceased loved ones." Each category should trace to a STORY field — note which crisis or value it comes from.]
<!-- KIT:END -->

---

## Long-horizon refusals (Principle #13)

Principle #13 (*The Long Horizon*) requires the product to name **short-horizon revenue paths and engagement levers explicitly rejected because they erode long-horizon trust.** Refusals above are general; this field is specifically the short-vs-long-horizon trade-offs.

The brewery taught the principle in dollars: the four-year compound (brand, location, relationships, regulars) wasn't visible to quarterly-snapshot tools. The same inverts here — every short-horizon shortcut that erodes the long-horizon moat costs more than it saves. Sobriety installed the same principle on the personal scale.

Each entry below is a *path* you could have taken (and competitors will take) but chose not to, with reasoning that names the long-horizon trade.

<!-- KIT:FIELD name="long_horizon_refusals" required="true" min_words="80" -->
[List 3–6 specific short-horizon revenue / engagement paths your product refuses. Each entry: the path itself (one sentence), what it would yield in the short term (revenue / DAU / retention), what it would erode over the long horizon (trust / sovereignty / dependency / chain-of-custody), and trace to STORY or REFUSAL_LIST. Examples of the form: "We refuse to add a notification stream — would lift D7 retention by an estimated 12% based on category benchmarks but converts a tool the user controls into one that controls the user (violates designed-to-be-needed-less)." / "We refuse to sell anonymized behavioral telemetry to third parties — clean ARPU lift but breaks data sovereignty (Principle #5)." / "We refuse to add variable-reward mechanics — would lift session length but degrades the wellness population we exist to serve." Trace each entry to a Principle (typically #2 memory-moat, #3 needed-less, #5 sovereignty, #6 truth-as-architecture, or the relevant STORY chapter). Trace also to `WORKING_BACKWARDS.md` if the PR/FAQ for the feature surfaced the trade. If the product has not yet faced a short-horizon temptation worth refusing, mark `not_yet` with the path to first identification (typically the first PR/FAQ exercise).]
<!-- KIT:END -->

---

## Floor principles

The non-negotiable safety/ethics floor below which the product will not function. These differ from refusals in that they are *operating preconditions* — if the floor is breached, the product stops, hands off, or fails closed. They are not behaviors the product avoids; they are conditions the product requires to operate.

<!-- KIT:FIELD name="floor_principles" required="true" min_words="100" -->
[List the floor principles. Examples of the form: "If a user expresses suicidal intent, the product surfaces a crisis resource immediately and does not gate the resource behind any feature, paywall, or onboarding step." / "If user PII would be transmitted to an external service, the product fails closed and surfaces the failure to the builder, not the user." / "If the model returns content that violates a refusal, the product surfaces the violation rather than silently filtering." Each floor should trace to a STORY field that explains why the floor exists.]
<!-- KIT:END -->

---

## Voice rules

How the product speaks. The voice is a downstream consequence of STORY — terse vs warm, honest vs comforting, plain vs ornate, direct vs indirect. The Method assumes voice is *chosen* and *enforced*, not whatever the model defaults to. Drift in voice is one of the earliest signals the doctrine is failing.

<!-- KIT:FIELD name="voice_rules" required="true" min_words="80" -->
[Describe how your product speaks. Tone, length, posture, what it never says, what it always says. Examples of the form: "Terse. Lead with the action. No padding, no cheerleading, no closing-paragraph summaries." / "Direct address (you), never first-person plural (we) unless explicitly representing the team." / "Names emotion when the user names emotion; does not project emotion onto the user." Each rule should trace to a STORY field that explains why this voice is the right voice for this builder and these users.]
<!-- KIT:END -->

---

## Escalation rules

When the product stops being the product and hands off to a human. The Method assumes that no AI product is the right tool for every user state — and that knowing when to step out is a feature, not a failure. The chain-of-command principle (the builder sets intent; the agent executes within scope) requires explicit handoff conditions.

<!-- KIT:FIELD name="escalation_rules" required="true" min_words="80" -->
[Describe the conditions under which the product hands off to a human. Examples of the form: "If the user describes a medical emergency, the product surfaces 911 and does not continue the conversation in a clinical voice." / "If the user requests a change to their account that affects billing or data retention, the product surfaces a human approval queue." / "If the model encounters a refusal-list violation in its own output, the product surfaces the violation to the builder for review." Each rule should trace to a STORY field, a refusal, or a floor principle.]
<!-- KIT:END -->

---

## How this is enforced

The commandments above are not aspirational. They are enforced at three layers:

1. **Build time** — the Prompt Guardian audits every prompt against this document. Commandment violations are flagged before the prompt ships.
2. **Runtime** — the chassis reads this document at boot and threads the commandments through the system prompt of every specialist.
3. **AAR** — every interaction is reviewed against this document in the After-Action Review loop. Drift is surfaced to the builder for approval before correction.

If a commandment is here but not enforced at all three layers, it is decorative. Move it, fix the enforcement, or strike it.
