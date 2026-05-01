# SECURITY

**The security posture of this product, written so a reader can audit it without reading the code.** Data inventory, threat model, defenses today, open risks, surface-level structural gaps, vulnerability reporting, incident runbook.

The Method does not prescribe a specific posture (financial-grade, medical-adjacent, political-campaign, consumer-grade). It prescribes that whichever posture you adopt is named explicitly, that the data you hold is enumerated against its sensitivity, that your *known* open risks are written down honestly, and that surfaces you cannot yet harden are disclosed (not papered over).

Posture is calibrated to the data, not to the builder's preference. A product holding bank credentials is financial-grade whether the builder likes the ceremony or not.

---

## Posture calibration

<!-- KIT:FIELD name="product_posture" required="true" min_words="60" -->
[Name the calibration this product is held to and why. Examples from the portfolio: "financial-grade — moves money via Stripe, sends email as the user, irreversible actions" (Operator); "medical-adjacent — holds veteran mental health journals, suicide-signal text, therapy-adjacent content; treated as if HIPAA applied even though not licensed" (TOP); "political-campaign — Colorado voter file under CRS 1-2-305, mass-outreach surfaces under TCPA/CAN-SPAM" (Custer). The posture must be calibrated to the most sensitive data class the product holds, not the most common. Trace to STORY.md `the_users` — the population sets the floor.]
<!-- KIT:END -->

---

## What this system protects

The data inventory is the spine of the document. Every row names a class of data, its sensitivity, and where it physically lives. If a class of data exists in the running system but is not in the table, the table is wrong.

| Data | Sensitivity | Where it lives |
|---|---|---|

<!-- KIT:FIELD name="data_inventory" required="true" min_words="80" -->
[Fill the table above with every distinct class of data the product holds. Sensitivity tiers: Critical (credentials, financial keys, regulated PII), Very High (mental-health-adjacent, identity narrative), High (regulatory, professional PII, user-account credentials), Medium (operational metadata), Low (logs, coordination state). "Where it lives" must be a real path or service: SQLite table name, file path, third-party service. Not "various places."]
<!-- KIT:END -->

---

## Threat model

A threat model is three lists: what is *in scope* (the failure modes you are designing against), what is *out of scope* (failure modes you are not — and the user/operator should know this), and the *threat actors* you are calibrating against. The out-of-scope list is as load-bearing as the in-scope list — it tells the reader where this document stops covering them.

### In scope

<!-- KIT:FIELD name="threat_in_scope" required="true" min_words="60" -->
[List the failure modes this product's defenses are designed to resist. Examples: unauthorized PII exposure, prompt injection leading to tool misuse, cross-tenant data leak, irreversible action without approval, API key exfiltration, supply-chain compromise, privilege escalation. Be specific to this product — generic lists are signal that the threat model has not been thought through.]
<!-- KIT:END -->

### Out of scope

<!-- KIT:FIELD name="threat_out_scope" required="true" min_words="40" -->
[List the failure modes this product is *not* designed to resist, so the user/operator can compensate at a different layer. Common: physical access to the operator's machine, compromise of upstream platform (Anthropic, Telegram, Stripe), denial-of-service against the hosting provider, attacks against the user's authenticated device session. Naming these is honesty, not weakness — it tells the reader where to look elsewhere.]
<!-- KIT:END -->

### Threat actors

<!-- KIT:FIELD name="threat_actors" required="true" min_words="40" -->
[Name the actors, in order of likelihood: who is most plausibly going to come at this product? Primary, secondary, tertiary. Common shape: primary = direct adversary or compromised user account; secondary = supply chain (compromised dependency); tertiary = opportunistic external probing. Tie to the product context — Custer's primary is "opposition research entity"; Operator's is "hostile content in scraped competitor pages or incoming Gmail."]
<!-- KIT:END -->

---

## Regulatory / compliance positioning

If this product touches a regulated data class (voter file, HIPAA-adjacent health data, financial accounts, EU resident data, child welfare records), name the regime and how the product complies — or, if the product is treated *as if* a regime applied without being legally bound by it, say that explicitly. The "as if" framing is honest and load-bearing; it tells future contributors which protections are statutory and which are voluntary.

<!-- KIT:FIELD name="compliance_positioning" required="false" min_words="60" -->
[If applicable, name the regime (CRS 1-2-305, HIPAA, GDPR, TCPA, CAN-SPAM, GLBA, COPPA, etc.) and the specific obligations the product meets. If the product is calibrated to a regime *as if* the regime applied (TOP's HIPAA-adjacent posture without being a licensed medical device), say so and explain the gap. If no regulated data, mark this section N/A with one-sentence reasoning.]
<!-- KIT:END -->

---

## Defenses currently in place

The set of defenses *that actually exist in the running code as of this commit*. Aspirational defenses go in "Known open risks" below, not here. The line between the two is what makes this section trustworthy.

<!-- KIT:FIELD name="defenses_in_place" required="true" min_words="80" -->
[Enumerate the defenses today. Common categories: secret hygiene (gitignore, gitleaks, secret scanning), approval gates for irreversible actions, per-user/per-tenant data isolation, prompt-level safety (Guardian, Reflection Gate), pre-commit hooks, file permissions, parameterized queries, allowlists, crisis floor wiring (point to CRISIS_TRIGGERS.md if applicable). Each defense names the mechanism — "approval queue at `agents/approval_queue.py`" beats "human approves actions."]
<!-- KIT:END -->

---

## Known open risks

The defenses you have *not* yet built. Required, not aspirational — refusing to enumerate open risks is the failure mode this section exists to prevent. A SECURITY.md with no open-risks list is either a fresh greenfield product (fine, write "none currently identified" with the date and check back) or an aging document whose author has stopped looking.

<!-- KIT:FIELD name="known_open_risks" required="true" min_words="60" -->
[List risks the product has not yet closed, with what would be required to close them. Examples from the portfolio: "Files in data/ created with default umask, world-readable on shared host — hardening to 0o600 planned" (TOP); "No rate limiting on /api/voters/search — enumeration risk if ever exposed" (Custer); "Specialists have approve()/reject() tools — LLM malfunction could self-approve, scheduled for removal" (Operator). Each item names the risk, the impact, and the planned mitigation.]
<!-- KIT:END -->

---

## Surface-level structural gaps

Some gaps are not bugs to fix in the next sprint — they are structural properties of a surface this product depends on, and they will not close until that surface is replaced. The honest move is to name them as gaps, describe what they expose, and write the exit plan.

The reference example: TOP runs primarily on Telegram. Telegram bot chats are not end-to-end encrypted, the company's jurisdiction is non-US/EU, and the founder was arrested in France in 2024 on platform-content charges. None of that is fixable inside TOP; it is fixable by replacing Telegram (the Phase 5 native app). Until then, the gap is named and the pilot scope is gated on it.

<!-- KIT:FIELD name="surface_gaps" required="false" min_words="60" -->
[For any structural surface the product depends on that has known security limits you cannot remediate inside this codebase, describe: (a) the surface and its trust posture (jurisdiction, ownership, technical limits), (b) what flows through it that is sensitive, (c) any mitigation available today that is not yet adopted (and why deferred), (d) the exit plan that replaces the surface, (e) the acceptable-use scope today (which users this is okay for, which it is not). If no such gaps exist, mark N/A with reasoning. The honest "no gap" is a real answer; the dishonest "no gap" is the failure mode.]
<!-- KIT:END -->

---

## Reporting a vulnerability

The reporter contact, the channel, what to include, and the response-time commitment. The commitment is a promise the builder makes to the reporter; calibrate it to the posture (campaign-season campaign products commit faster acknowledgement than consumer products; medical-adjacent products commit faster notification of affected users).

<!-- KIT:FIELD name="vulnerability_reporting" required="true" min_words="60" -->
[Name the contact email or channel, what the reporter should include (description, repro, impact, contact), and the explicit response-time commitment: acknowledgement window (24h / 72h / 7d), assessment window, patch timeline. Include any posture-specific commitments — for financial-grade, "key rotation within 1 hour of confirmation"; for political-campaign, "same-day rotation, same-day legal-counsel notification on regulated-data exposure." State explicitly that public GitHub issues are not the channel.]
<!-- KIT:END -->

---

## Incident response

The runbook the operator follows when something has actually gone wrong. Numbered, terse, ordered by what must happen first. The shape is durable across products: contain → rotate → review → notify → preserve → remediate → post-mortem. The contents are product-specific.

<!-- KIT:FIELD name="incident_response_plan" required="true" min_words="80" -->
[Author the runbook. At minimum: (1) Contain — what gets disabled first; (2) Rotate — exact list of keys/tokens to rotate, in what order, where to rotate them; (3) Review — what audit trails to inspect (Stripe dashboard, Gmail Sent, Railway logs); (4) Notify — affected parties, channel, timeline; (5) Preserve — what state to snapshot before it rotates out; (6) Remediate — fix root cause, write regression test; (7) Post-mortem — where it gets documented. Posture-specific additions: financial → reverse unauthorized charges; regulated → legal-counsel review before public notification; medical-adjacent → user notification within 72h per GDPR-style principles.]
<!-- KIT:END -->

---

## Security-relevant dependencies

The third-party services the security posture depends on. If any one of them is compromised, the surface area of this product changes. Naming them lets a reader see the chain.

<!-- KIT:FIELD name="security_dependencies" required="true" min_words="40" -->
[List every third-party service whose compromise would degrade this product's security posture: LLM provider (Anthropic / OpenAI), messaging platform (Telegram / Twilio), payment processor (Stripe), email provider (Gmail SMTP / SES), hosting (Railway / Fly / self), data sources (Plaid, government APIs). For each, one phrase on what it provides.]
<!-- KIT:END -->

---

## Supported versions

Default: only `main` is supported; security fixes do not backport to feature branches or prior releases. Override only if your product has an LTS commitment.

<!-- KIT:FIELD name="supported_versions" required="false" min_words="20" -->
[State which branches/releases receive security patches. Default acceptable: "Only `main` is supported." If you maintain LTS branches or have a backport policy, document it here.]
<!-- KIT:END -->

---

## Operational security

The operator-side practices that complement the in-code defenses. Disk encryption, key storage, screen-share discipline, third-party file-hosting prohibitions. This section binds the operator, not the product — but the product's security posture depends on the operator following them.

<!-- KIT:FIELD name="operational_security" required="false" min_words="40" -->
[Name operator-side requirements: full-disk encryption (FileVault / BitLocker / LUKS), `.env` file mode (0o600), prohibitions on cloud-syncing sensitive directories, password manager use, MFA on dependency dashboards (GitHub, Anthropic, Stripe), screen-share discipline. Default to short and pointed; this is not a policy document.]
<!-- KIT:END -->

---

## Review cadence

- **On every change to data flow.** PRs that add a new data class, a new third-party service, a new inbound surface, or a new outbound action require this file's review checklist filled in and committed alongside the PR.
- **Quarterly drill.** The builder runs a key-rotation drill — rotate one credential end-to-end and verify the system reaches the same operational state. A rotation plan that has never been exercised is not a plan; it is a wish.
- **Annual posture review.** Re-read this file end to end, mark anything stale, update the open-risks list, confirm the surface-gap section still describes reality.

### Review checklist (for data-flow PRs)

- [ ] Does the new code path read or write a data class listed in the data inventory? If not, has the inventory been updated?
- [ ] Does it introduce a new third-party dependency? If so, has it been added to security-relevant dependencies?
- [ ] Does it add a new inbound surface? If so, is the crisis-floor wrap (CRISIS_TRIGGERS.md) applied if applicable?
- [ ] Does it add a new outbound action? If so, does it route through the approval queue per COMMANDMENTS.md?
- [ ] Does it expand cross-tenant or cross-user blast radius? If so, has data isolation been verified?

---

## What this file is not

- **Not a compliance certification.** Naming HIPAA / GDPR / CRS 1-2-305 here describes posture and obligation, not certification. Certification, where required, is a separate process.
- **Not exhaustive.** A SECURITY.md is a snapshot of *known* risks. The set of unknown risks is by definition not enumerable. Annual review is what keeps the document honest as the unknown becomes known.
- **Not gated.** No commandment, no feature flag, no operator preference can disable the open-risks enumeration or the incident-response runbook. The honesty of this file is what makes it useful.

---

## Changes to this policy

A dated record of every material modification to posture, data inventory, defenses, or open-risks list. Required.

| Date | Change | Author | Reason |
|---|---|---|---|
| YYYY-MM-DD | File created — bootstrap from kit template | builder | initial onboarding |

---

## Trace

- [STORY.md](STORY.md) `the_users` — the population whose data this file protects.
- [STORY.md](STORY.md) `formative_crisis` — what the builder has lived that justifies the posture calibration.
- [COMMANDMENTS.md](COMMANDMENTS.md) — the approval-gate and data-isolation commandments that this file operationalizes.
- [CRISIS_TRIGGERS.md](CRISIS_TRIGGERS.md) — the inbound-surface safety floor, which this file's review checklist enforces.
- [REFUSAL_LIST.md](REFUSAL_LIST.md) — the things the product will never do, including the surveillance/PII refusals this file's posture protects.
