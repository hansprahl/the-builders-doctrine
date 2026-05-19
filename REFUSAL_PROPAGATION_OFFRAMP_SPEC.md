# Refusal Propagation Off-Ramp — Primitive Spec

**Status:** **DRAFT v0.1.** Spec only. No code. Phase 1 deliverable for v1.0 ship (target 2026-06-01 per [RELEASE_PLAN_v1.md](RELEASE_PLAN_v1.md)). Law VII applies: this spec is provisional doctrine until it has shipped through one full propagation cycle and produced at least one logged deviation or one logged silent-acceptance audit.

**Date opened:** 2026-05-18.
**Owns deliverable slot:** *Refusal-propagation off-ramp primitive spec — 2026-05-25 (8 hrs)* in `STARTUP.md` Phase 1.
**Sits alongside:** [CHASSIS_PROPOSED_EXTENSIONS.md](CHASSIS_PROPOSED_EXTENSIONS.md) (the LLM-reviewer adversarial chassis); same recursive discipline (Laws VII + X) applies.

---

## 1. Why this exists

### The current state

The canonical Refusal list lives at [THE_BUILDERS_DOCTRINE.md](THE_BUILDERS_DOCTRINE.md) §II.8. Three items as of v1.2 (2026-05-13):

1. Engagement-maximization apps (variable rewards, streaks-as-dopamine, dark patterns)
2. Surveillance products (behavioral tracking sold to third parties, consent-by-dark-pattern)
3. Parasocial replacements that erode real human terrain (wellness co-pilots augment; they do not supplant)

Each of the four downstream products carries a per-product audit at `<product>/REFUSAL_AUDIT.md` (TOP, Operator, Custer, RPR — confirmed extant 2026-05-18). The audit files quote the upstream list and apply the items to product-specific decisions in a per-feature template.

### The failure mode this spec exists to close

Today's propagation model is **silent inheritance**. When a refusal item is added, removed, or amended upstream in `THE_BUILDERS_DOCTRINE.md` §II.8, the four downstream `REFUSAL_AUDIT.md` files do not auto-update; the next Guardian audit cycle (or the next manual edit to the product file) is when the change surfaces in the product. Three failure modes follow.

| Failure mode | What happens today | Real-world example |
|---|---|---|
| **Silent drift** | Upstream changes; downstream products keep the stale list at the top of their audit. No mechanism forces re-acknowledgment. | A v1.5 amendment to refusal item 1 (say, narrowing "streaks-as-dopamine" to "streaks with variable-interval reinforcement") never lands in TOP's audit; TOP keeps the old text and audits new features against a stale rule. |
| **Silent over-inheritance** | Upstream adds a new item that is structurally incompatible with a product. Product silently fails the audit on its existing surface area (not just new features). | Hypothetical: doctrine adds "no habit-tracking surfaces of any kind." TOP's existing habits feature is suddenly out-of-doctrine; no mechanism names the conflict or proposes a deviation path. |
| **Silent non-applicability** | Upstream item is moot for a product (no vulnerable users, no consumer surface). Product carries audit text it cannot meaningfully apply. | Refusal item 3 (parasocial) on RPR (a B2B camo pattern generator with zero personal-relationship surface). Today RPR's audit either copies the text without context or omits it without explanation; either way the deviation is undeclared. |

The Refusal is doctrine. Today its propagation is character-of-builder, not mechanism — the same gap the stress test of v1.0 named for the Refusal itself (2026-04-30), one layer up. **This spec moves propagation from character-of-builder to audit surface.**

### Why a primitive rather than a one-time fix

Three triggers will keep recurring across the portfolio. Refusal items will be added (v1.5+ has at least one in flight — the parasocial item's tenant-downstream-user clause currently in Operator's audit (`5b301c8`) is a candidate for promotion upstream). Products will be added (Vibeloom, future ventures). Edge cases will surface where a product cannot literally comply and the right answer is a logged deviation, not a silent skip. A one-time fix per refusal change cannot scale; a named protocol with a deviation surface can.

---

## 2. What this is — and is not

### What this is

- A **named protocol** for moving refusal-list changes from upstream doctrine to downstream products with explicit re-acknowledgment at each product.
- A **deviation record** format for cases where a product cannot literally inherit a refusal item, with required fields (reason, scope, sunset, signer).
- A **portfolio-level visibility surface** for active deviations, so the four-product portfolio carries a countable deviation ledger rather than four uncorrelated audit files.
- A **pre-commit-hook spec** (provisional — actual chassis primitive lives downstream of validation) for catching propagation skips at the doctrine-repo edit boundary.

### What this is NOT

- **Not a chassis component yet.** This spec describes the *protocol*; the chassis primitive at `kit/chassis/refusal_propagation.py` is a downstream artifact gated by Validation §9. Until then the protocol runs by founder discipline + the audit log.
- **Not autonomous.** No tool in the protocol may block a commit or auto-edit a product file. Every state change requires founder acknowledgment. Off-ramps are *named*, not *granted by a chassis*.
- **Not a vehicle for weakening the Refusal.** The off-ramp exists so the Refusal can stay strict at the top of the doctrine while letting products name structural deviations honestly. A deviation that hollows the refusal item is a falsification of the refusal item, not a permitted off-ramp — see §8.
- **Not a Guardian replacement.** Existing per-product Guardian audits continue to score commandment drift. This protocol adds a refusal-propagation column to the Guardian's audit surface; it does not replace what Guardian already does.

---

## 3. Trigger surface — when the protocol engages

Three trigger classes. Each fires a propagation cycle.

### 3.1 Upstream edit (the dominant case)

Any commit in `~/Projects/the-builders-doctrine/` whose diff touches [THE_BUILDERS_DOCTRINE.md](THE_BUILDERS_DOCTRINE.md) §II.8 (the Refusal section). Detection: a regex match on the affected line range in the staged diff at pre-commit time, or — equivalently — a grep on the committed diff at the next propagation cycle.

The edit class determines downstream obligation:

| Edit class | Detection signal | Downstream obligation |
|---|---|---|
| **Add** — new refusal item appended | New numbered list item in §II.8 | All four products must acknowledge (re-audit) or file a deviation. |
| **Amend** — wording change to an existing item | Diff inside an existing item's body | All four products re-acknowledge against the amended text; prior audit entries are not retroactively invalidated but the *next* feature audit must use the new text. |
| **Remove** — item retracted | Item deleted from §II.8 | All four products record the retraction date in their audit history; existing audits against the removed item stand as historical record. |
| **Editorial** — typo / clarification only | No semantic change to scope | No downstream obligation. The doctrine-repo committer marks the edit `editorial` in the commit message; default is non-editorial until marked. |

### 3.2 New product introduced

A new product directory is added under `~/Projects/` and inherits the doctrine. The new product must initialize `REFUSAL_AUDIT.md` from the canonical template (per §5.1) and complete an initial product-specific acknowledgment against every active refusal item, including any structurally inapplicable items declared as deviations (§5.3).

### 3.3 Product surface-area change

A product's scope expands in a way that materially changes its refusal posture. Examples (not exhaustive):

- Operator gains consumer-facing growth surfaces (refusal item 3, parasocial, re-engages).
- TOP adds a habit-tracking variant (refusal item 1, engagement-max, re-engages on the new surface).
- RPR opens a B2C tier (refusal item 1 + 3 re-engage).

Trigger detection at this class is intentionally manual — there is no mechanical signal for "scope materially changed." Founder declares this trigger at the moment of scope change (typically during a STORY.md chapter, a CLAUDE.md edit, or a feature audit). The protocol does not attempt to mechanize what is fundamentally a judgment call.

---

## 4. Protocol — the steps from upstream edit to closed cycle

A single propagation cycle has five steps. The cycle is named in the doctrine-repo commit message that initiates it and is closed when all four products have either acknowledged the upstream change or filed a deviation.

### Step 1 — Upstream commit names the cycle

The doctrine-repo committer marks the propagation cycle in the commit message:

```
§II.8 propagation cycle <YYYY-MM-DD> — <ADD|AMEND|REMOVE|EDITORIAL>:
<one-sentence description of the change>

<body>
```

If the commit is editorial only, the marker is `EDITORIAL` and no downstream cycle opens. Any other class opens the cycle. The commit SHA is the cycle ID.

### Step 2 — Cycle ledger entry opened in the doctrine repo

The doctrine repo carries one file, `REFUSAL_PROPAGATION_LEDGER.md` (created on first use of this protocol), with one row per opened cycle:

```
| Cycle ID (SHA) | Date opened | Edit class | Summary | Status | Closed |
```

Status values: `open`, `acknowledged-all`, `deviations-pending`, `closed`.

The doctrine repo opens the row; products close it from their side.

### Step 3 — Per-product acknowledgment or deviation

For each of the four products, the founder (or Guardian at next audit cycle) appends one of two entries to that product's `REFUSAL_AUDIT.md` under a new top-level section `## Propagation log`:

**Acknowledgment** (the default, mandatory unless deviation is filed):

```
### Cycle <SHA-short> — <YYYY-MM-DD> — ACKNOWLEDGED
Edit class: <ADD|AMEND|REMOVE>
Summary: <copied from doctrine-repo commit message>
Product impact: <one or two sentences naming what changes in the product's audit surface>
Acknowledged by: <signer>
```

**Deviation** (required if and only if the product cannot literally inherit the change — see §5 for what qualifies):

```
### Cycle <SHA-short> — <YYYY-MM-DD> — DEVIATION FILED
Edit class: <ADD|AMEND|REMOVE>
Summary: <copied from doctrine-repo commit message>
Deviation type: <STRUCTURAL_INAPPLICABILITY|SCOPE_NARROWING|TIMING_DEFERRAL>
Reason: <why the product cannot literally inherit; cite product surface area>
Scope: <which features / surfaces the deviation covers; "all" must be defended>
Sunset: <date or condition that closes the deviation>
Signer: <founder name; deviations are not Guardian-grantable>
Linked artifacts: <commits, audit entries, STORY chapter if relevant>
```

### Step 4 — Cycle closure

The cycle closes when all four products have an entry of either type. The doctrine repo's `REFUSAL_PROPAGATION_LEDGER.md` row updates `Status: closed` with a `Closed` date.

A cycle that has been open >30 days without all four products acknowledging is **stale**. Stale cycles are surfaced at the next bandwidth-overlay weekly check (§7.2) and either closed or explicitly extended with a logged reason. Stale-without-extension blocks the next doctrine-repo release tag.

### Step 5 — Guardian inheritance at next audit cycle

The next time each product runs a Guardian audit, the audit reads the propagation log and confirms the most recent cycle is closed for that product. If the cycle is open, Guardian flags the gap in the audit report and the audit cannot pass-grade until the gap closes.

---

## 5. Deviation record — required fields and what qualifies

### 5.1 The three legitimate deviation types

A deviation is **not** a permission to weaken the Refusal. It is a structured admission that the product cannot literally inherit a refusal item for a specific named reason. Three types, each with strict criteria.

#### `STRUCTURAL_INAPPLICABILITY`

The refusal item is moot for the product because the product has no surface area where the refused pattern could exist.

- **Example:** RPR (B2B camo pattern generator) → refusal item 3 (parasocial). RPR has no human-relationship surface; the item cannot apply.
- **Required defense:** the product surface area is named explicitly; the deviation includes a one-line reasoning that survives a future surface-area change (i.e., "if RPR ever ships a consumer-facing chat surface, this deviation is invalidated automatically per §5.4").

#### `SCOPE_NARROWING`

The refusal item applies in some surfaces of the product but not all, and the product wishes to acknowledge for the in-scope surfaces while naming the out-of-scope surfaces explicitly.

- **Example:** Operator → refusal item 3 (parasocial). Applies to Archer's outreach surface when downstream users are consumer-grade; does not apply to internal staff specialists. Operator's existing 2026-05-05 audit entry (`5b301c8`) is exactly this shape, written before this protocol existed.
- **Required defense:** the in-scope and out-of-scope surfaces are named with the same specificity. "Most of the product" or "growth surfaces" without enumeration does not qualify.

#### `TIMING_DEFERRAL`

The product accepts the refusal item in principle but cannot apply it immediately because of in-flight work, and requires a dated sunset before full acknowledgment.

- **Example:** Hypothetical — doctrine adds a refusal item that conflicts with a feature already in production. Product files a `TIMING_DEFERRAL` with a sunset date by which the feature is brought into compliance or retired.
- **Required defense:** the sunset date is a calendar date, not a condition. A condition-based sunset converts the deviation to one of the other two types or to a falsification (§8.2).

### 5.2 What does NOT qualify as a deviation

- **Disagreement.** "I don't think this should be a refusal item" is not a deviation; it is a doctrine debate. Resolution path: amend the upstream doctrine (the deviation surface is for execution gaps, not philosophical disputes).
- **Inconvenience.** "Acknowledging this item would require feature work I do not want to do" is not a deviation; it is a `TIMING_DEFERRAL` with an explicit sunset, or it is a refusal to comply, which is a falsification of the product's adoption of the doctrine.
- **Vagueness.** A deviation without a named scope and a named sunset (or §5.1-qualifying surface argument) is not a deviation; it is a placeholder, and placeholders do not count toward cycle closure.

### 5.3 Initial-state deviations (new product onboarding)

When a new product is introduced (§3.2), the initial `REFUSAL_AUDIT.md` may include `STRUCTURAL_INAPPLICABILITY` deviations as part of its initial state. These follow the same template (§4 step 3) and are subject to the same auto-invalidation (§5.4).

### 5.4 Auto-invalidation

A `STRUCTURAL_INAPPLICABILITY` deviation auto-invalidates the moment the product's scope changes such that the surface argument no longer holds. The product's next Guardian audit catches the invalidation by reading the propagation log against the product's current scope and surface area.

Concretely: if RPR's audit says "no human-relationship surface exists" and a later commit adds a consumer-facing chat surface, the deviation is invalid from that commit forward. The next Guardian audit cycle on RPR flags the invalidation and the product owes a fresh acknowledgment or a new deviation type.

### 5.5 Sunset enforcement

A `TIMING_DEFERRAL` whose sunset date passes without resolution is **escalated**, not silently expired. The escalation lands as a high-severity Guardian audit finding on the product, the doctrine-repo ledger's row is flagged red, and the next bandwidth-overlay weekly check surfaces it explicitly. The deviation is closed only by acknowledgment-or-new-deviation; expiration alone does not close it.

---

## 6. Portfolio-level visibility — the deviation ledger

### 6.1 What gets centralized vs. what stays local

**Local to each product (in `<product>/REFUSAL_AUDIT.md`):**

- The full audit history per feature (pre-existing surface).
- The full propagation log (acknowledgments + deviations) for that product.
- The product-specific reasoning for any deviation.

**Centralized in the doctrine repo (in `REFUSAL_PROPAGATION_LEDGER.md`):**

- One row per cycle (open / closed status).
- One row per active deviation (pulled from per-product audits at audit time).
- Stale-cycle and overdue-sunset flags.

The doctrine repo's ledger is the only place where "how many deviations are live across the portfolio, against which items, with what sunsets" is countable in a single read. Without that surface, the four product files drift independently and the doctrine cannot answer "is the Refusal holding across the portfolio?" without grepping four repos.

### 6.2 How the centralized ledger stays current

Two paths.

**Manual (always available):** the founder reads each product's propagation log and updates the doctrine-repo ledger. Slow but always correct.

**Chassis-assisted (post-validation):** the chassis primitive at `kit/chassis/refusal_propagation.py` (downstream of §9) reads each product's `REFUSAL_AUDIT.md`, extracts the propagation log section, and emits a single ledger update commit on the doctrine repo. Read-only on the products; write-only on the doctrine repo. No autonomous edits to products. Failure mode: a parse error on a product audit file blocks the ledger update for that product and surfaces the parse failure; no silent omission.

### 6.3 Public-facing exposure

The ledger is internal until validated. The v1.0 public release (target 2026-06-01) ships the doctrine and the audit template, not the centralized deviation ledger. A v1.5 or later release may expose an aggregated count (e.g., "3 active deviations across 4 products, 0 overdue") as a trust signal. The active-deviations *text* itself is not externalized without per-deviation review (some deviations name product surfaces that are not yet public).

---

## 7. Defense against weaponized off-ramping

This is the load-bearing section. An off-ramp the founder can quietly walk through whenever the Refusal becomes inconvenient is worse than no off-ramp — it laundering "I changed my mind" as "structural deviation."

### 7.1 The substrate's predictable attack vectors

| Attack vector | What it looks like | Defense |
|---|---|---|
| **Vague-scope deviation** | "This refusal item does not apply to RPR's marketing surfaces." (No enumeration of which surfaces, what they do, what the actual refused pattern would look like there.) | §5.2 — vague deviations do not count toward cycle closure. The cycle stays open. Guardian audit cannot pass-grade until the deviation is specific. |
| **Sunset-as-fog** | A `TIMING_DEFERRAL` whose sunset is "when we have bandwidth." | §5.1 — sunset must be a calendar date or a §5.1-qualifying surface argument. Conditions are not sunsets. |
| **Quiet retraction upstream** | Founder edits §II.8 to remove an inconvenient refusal item without naming the retraction in commit class. | §4 step 1 — the commit must declare class. `EDITORIAL` is only valid for non-semantic edits; an item removal is `REMOVE` regardless of how the diff is framed. Adversarial review chassis (§ [CHASSIS_PROPOSED_EXTENSIONS.md](CHASSIS_PROPOSED_EXTENSIONS.md) §1) reads §II.8 diffs as a trigger surface; misclassification is exactly the pattern that primitive is built to catch. |
| **Carve-out construction** | "One-shot exception" deviation pattern, per the Law X failure mode named in `CHASSIS_PROPOSED_EXTENSIONS.md`. | A `STRUCTURAL_INAPPLICABILITY` that names "one product, one feature, one quarter" is not structural; it is timing. Guardian audit converts misclassified deviations to their true type and re-opens the cycle. |
| **Tame-Guardian drift** | The Guardian gradually softens its refusal-propagation scoring across audits. | Guardian's refusal-propagation column is read by adversarial-review chassis on the doctrine repo at every §II.8 edit; quarterly ground-truth audit (5 random recent cycles, manually re-reviewed) catches systematic softening. |
| **Founder override without log** | Founder dismisses a deviation requirement informally ("eh, doesn't apply") without a logged entry. | §4 step 3 — entries are required, not optional. Cycle does not close without all four entries. There is no "implicit acknowledgment" surface. |

### 7.2 Tripwires already in place

- **Weekly bandwidth-overlay check** ([BANDWIDTH_OVERLAY_2026-05-15.md](BANDWIDTH_OVERLAY_2026-05-15.md) §5 — first check 2026-05-21 EOD). Open cycles older than 30 days surface here.
- **Adversarial review chassis** ([CHASSIS_PROPOSED_EXTENSIONS.md](CHASSIS_PROPOSED_EXTENSIONS.md) §1). §II.8 diffs and refusal-audit diffs added to the trigger paths list when the chassis ships.
- **Law VII** — this spec is itself provisional doctrine, subject to retraction if the protocol produces no logged deviations and no logged silent-acceptance audits in its first six months. A protocol that produces no evidence of working is not load-bearing; it is decoration.

### 7.3 The honest answer about what this cannot defend

This protocol cannot stop a founder who is willing to **lie in writing.** A vague-scope deviation that names a fake surface, a sunset date the founder has no intention of meeting, a structural-inapplicability claim that misrepresents the product — none of these are caught by the protocol's mechanical surface. The defense for that failure mode is not this spec; it is the same defense the rest of the doctrine relies on: adversarial review, external readers, the Grok second-opinion workflow, and the fact that the entire audit trail is git-tracked and inspectable. The protocol moves the threshold of self-deception, not the ceiling.

---

## 8. Relationship to neighbors

### 8.1 To the Refusal itself (THE_BUILDERS_DOCTRINE.md §II.8)

This spec does not edit the Refusal. It adds a propagation layer beneath it. The Refusal's authority over the four products is not weakened by the existence of a deviation surface, because deviations are defenses *for the founder against the founder*, not concessions from the doctrine to the products.

### 8.2 To the adversarial review chassis (CHASSIS_PROPOSED_EXTENSIONS.md §1)

The adversarial review chassis, once validated and shipped, gains a `refusal_propagation_skip` pattern in its system prompt: any §II.8 edit committed without a propagation-cycle marker per §4 step 1 is flagged critical. The pattern's severity is critical because skipping the marker is precisely the founder-romance shape the chassis exists to catch — using one's own authorship as license to bypass one's own discipline.

### 8.3 To Guardian (per-product)

Each product's Guardian gains a *propagation-current* column in its audit surface. Scoring: a product passes the column at audit time if and only if (a) the most recent §II.8 cycle is closed for that product, and (b) no deviation is past its sunset. Failure on either condition is a high-severity audit finding.

### 8.4 To the v1.0 public release (RELEASE_PLAN_v1.md)

This spec ships in v1.0 as part of the doctrine repo's `kit/` documentation surface, **as a spec, not as enforced chassis.** The v1.0 release notes name the protocol; the `REFUSAL_PROPAGATION_LEDGER.md` file exists as a one-row demonstration (the bootstrapping cycle that retroactively logs Operator's 2026-05-05 parasocial scope-narrowing — see §11). The chassis primitive is a v1.5 or later artifact, downstream of validation.

### 8.5 To the chassis at large

The protocol is a candidate chassis component (`refusal_propagation.py`) but does not become one until §9 passes. Until then it runs as founder-discipline + git-tracked audit text, like the Refusal itself ran from v1.0 to v1.2 before the per-product `REFUSAL_AUDIT.md` files materialized.

---

## 9. Validation requirement — what earns the chassis its place

The protocol ships as a spec in v1.0. It earns chassis-primitive status (`kit/chassis/refusal_propagation.py`) when the following pass.

### 9.1 Bootstrap cycle

Retroactively log Operator's 2026-05-05 parasocial scope-narrowing (Sentinel audit, `5b301c8`) as the protocol's first cycle, with the upstream "edit" treated as the doctrine's v1.0 parasocial item. This is a single cycle, processed end-to-end against the protocol, producing one `DEVIATION FILED — SCOPE_NARROWING` entry on Operator and three `ACKNOWLEDGED` entries on TOP / Custer / RPR (where the existing audit files already covered the item with no deviation needed).

**Pass criterion:** the bootstrap cycle closes cleanly per §4 step 4, surfaces no spec ambiguities that require unplanned edits, and produces exactly one ledger row.

### 9.2 Forward cycle

At least one real upstream §II.8 edit between v1.0 ship (2026-06-01) and v1.5 release (target 2026-07-25) runs through the protocol live. The cycle closes with all four products acknowledged or deviation-filed.

**Pass criterion:** zero silent inheritances. Every change to §II.8 in that window produces a cycle entry; every cycle closes.

### 9.3 Adversarial review of the protocol itself

When the adversarial review chassis ships (per [CHASSIS_PROPOSED_EXTENSIONS.md](CHASSIS_PROPOSED_EXTENSIONS.md) §1), this spec is fed through it. Findings categorized:

- **Critical findings** must be addressed before the protocol earns chassis status.
- **Warnings** are logged in the protocol's revision history; the protocol may earn chassis status with warnings outstanding, but warnings count toward the v1.5 audit of the protocol's own discipline.

### 9.4 Migration criteria — when this becomes `kit/chassis/refusal_propagation.py`

All four of the following:

1. §9.1 bootstrap cycle closed cleanly.
2. §9.2 forward cycle closed cleanly with at least one cycle in production.
3. §9.3 adversarial review run; critical findings closed.
4. A second product (beyond the doctrine repo itself) has demonstrated read of the propagation log via Guardian's *propagation-current* column.

If any fails, the spec stays in this file and the protocol continues to run by founder discipline.

---

## 10. Cost — bandwidth and tracking

The spec itself costs founder discipline (per-cycle ~15–30 minutes for an `AMEND` cycle, ~45–60 minutes for an `ADD` cycle requiring per-product re-acknowledgment). No API cost.

The chassis primitive (post-validation) has minor inference cost only if it routes audit-file parsing through an LLM; the v0 implementation should be deterministic text parsing of the propagation-log section header. **Recommended:** ship the chassis with deterministic parsing and zero per-cycle inference cost; reserve LLM use for the adversarial-review side, not for protocol mechanics.

Cycle-time budget for the protocol at steady state:

| Edit class | Founder time per cycle | Justification |
|---|---|---|
| `EDITORIAL` | 0 | No downstream obligation. |
| `AMEND` | 15–30 min | Four product re-acknowledgments, mostly identical text. |
| `ADD` | 45–90 min | Four product entries with per-product impact framing; possible deviations. |
| `REMOVE` | 15–30 min | Four product retraction records, audit history annotation. |

A single `ADD` cycle in the v1.0 → v1.5 window costs less than one bandwidth-overlay weekly check. The protocol does not stress the schedule.

---

## 11. Bootstrap cycle (closes simultaneously with this spec's commit)

To validate §9.1 immediately, the protocol's first cycle is the one that ratifies the protocol's own existence and retroactively logs the parasocial scope-narrowing already on Operator (`5b301c8`, 2026-05-05).

### Cycle bootstrap-2026-05-18 — RETROACTIVE

**Edit class:** `AMEND` (retroactive; the doctrine's v1.0 parasocial wording is what is being acknowledged here, against four products that already existed when v1.0 shipped).

**Summary:** Doctrine v1.0 §II.8 item 3 (parasocial replacements) — initial portfolio-wide acknowledgment, with one scope-narrowing deviation on Operator already logged at `<operator>/REFUSAL_AUDIT.md:29` (the multi-user / tenant-downstream surface clause).

**Status:** Per-product entries to be filed in the same commit cycle that lands this spec. Cycle closes when:

- TOP: `ACKNOWLEDGED` (wellness co-pilot framing — refusal item 3 is load-bearing per `<top>/REFUSAL_AUDIT.md:29`; no deviation).
- Operator: `DEVIATION FILED — SCOPE_NARROWING` (retroactively migrating the existing audit-history entry into the propagation log format).
- Custer: `ACKNOWLEDGED` (campaign platform; no parasocial surface; existing audit covers).
- RPR: `DEVIATION FILED — STRUCTURAL_INAPPLICABILITY` (no human-relationship surface; auto-invalidates if RPR adds a consumer chat tier).

Once those four entries land on the respective product files and the cycle is recorded in `REFUSAL_PROPAGATION_LEDGER.md`, the protocol's bootstrap validation (§9.1) is complete.

**This commit does not file those entries.** Per Hans's preference (build one thing at a time, suggest options before building), the four product-file edits are a separate decision: ship them in one batch immediately, or file them at the next per-product Guardian audit. Recommendation: batch immediately, in four small commits, so the bootstrap cycle is closed inside the same 24-hour window as the spec.

---

## 12. Commit discipline

Per Law X applied recursively to this protocol:

1. **No section in this file is allowed to migrate to `kit/chassis/refusal_propagation.py` without passing §9 in full.**
2. **No external claim** (in pitches, README, EXPLAINER, v1.0 release notes) is allowed to reference a "refusal propagation chassis" until §9.4 is closed. v1.0 may reference the **spec and protocol**; it may not reference the **chassis component**.
3. **If the bootstrap cycle (§11) fails to close cleanly** — i.e., the protocol's first cycle surfaces ambiguities that require unplanned spec edits — the spec is revised, the bootstrap is re-run, and the validation clock resets. Failed bootstraps are doctrine evidence, not embarrassment.
4. **This file is a staging area, not a backlog.** Sections move out (to `kit/chassis/` or to retraction) when evidence arrives.

---

## 13. Open decisions — for Hans before close

Three named decisions where I picked a default but the choice is yours. Each is reversible; calling them out so the spec doesn't lock something silently.

| Decision | Default chosen | Alternative |
|---|---|---|
| **Where the centralized ledger lives** | `~/Projects/the-builders-doctrine/REFUSAL_PROPAGATION_LEDGER.md` (this repo, public-track) | A separate private file outside the public-release repo (e.g., in `~/.claude/projects/...`). Trade-off: public ledger is a trust signal (we publish our deviations); private ledger is operationally simpler but loses the trust-signal value. |
| **Whether v1.0 ships the bootstrap cycle as a worked example** | Yes — close the bootstrap cycle in one batch of four small commits within 24 hours of this spec landing, so v1.0 ships with a worked example of the protocol in motion. | Ship the spec only; let the protocol's first real run wait for the next §II.8 edit. Trade-off: worked example is concrete (Brad-shaped reader sees the protocol *running*, not just *described*); waiting is honest about not having stress-tested it yet. |
| **Whether `EDITORIAL` class needs a public-facing definition** | A short definition in §3.1 above is sufficient for v1.0. | Expand into a full §II.8.E "editorial-vs-semantic" guidance subsection in the doctrine itself. Trade-off: adds doctrine surface (Law X concern); but unambiguous classification is the load-bearing surface that this protocol depends on. |

---

## Adversarial Review — 2026-05-18 — Grok

Verbatim. Run via the manual Grok second-opinion workflow (per `~/.claude/projects/-Users-hansprahl-Projects/memory/feedback_grok_second_opinion_workflow.md`). Findings preserved here as evidence; response lives in the v0.2 revision (below).

> **§5 deviation categories are incomplete and carry romance risk.**
> STRUCTURAL_INAPPLICABILITY, SCOPE_NARROWING, and TIMING_DEFERRAL miss the fourth inevitable pattern: **DOCTRINAL_OBSOLESCENCE** (upstream refusal no longer survives contact with new empirical surface, e.g., a refusal written pre-2026 that breaks on frontier-model behavior in 2027). You defined three clean bins that let the founder feel architecturally rigorous while leaving the real escape hatch (quiet upstream rewrite when inconvenient) unaddressed. That is founder-romance laundering: the categories protect the Refusal's image more than its integrity. Second-order: sharp external reader sees three polite off-ramps and assumes the fourth is just rebranded disagreement. Incomplete.
>
> **§7 defense is theater describing honest-founder behavior.**
> It lists attack vectors and mechanical tripwires but provides zero binding enforcement when the founder (you) decides the vectors no longer apply. "We rely on adversarial review and git history" is exactly what every disciplined founder says right before the first convenient deviation. It misses the real weaponized path: founder self-reclassifies an edit as EDITORIAL, skips the cycle, then later claims the protocol was never triggered. The chassis-adversarial hook is vapor until validated. This section defends nothing; it documents what you already intend to do. Second-order: Law X cap exists because of this exact pattern. You wrote another guardrail you can step over.
>
> **§11 bootstrap is salvage, not validation.**
> Retroactively logging Operator's 2026-05-05 entry through a protocol that did not exist at the time is cooked data wearing uniform. You are manufacturing the "first cycle closed cleanly" evidence the validation gate demands. Same shape as the original Stage 7 N=3 claim and the Sarah Chen fiction. It lets you ship v1.0 with a green checkmark on §9.1 without ever running the protocol on a live upstream change. Second-order: this is precisely the observer-bias Law II and Law VII were built to kill. Bootstrap fails; delete the section or treat it as historical note only. No validation credit.
>
> **§13 open decisions — flip two defaults.**
> - Ledger: move to private file outside public repo. Public deviations become marketing theater the moment a hostile reader screenshots one. Trust signal is false until you have six months of real cycles with zero overdue.
> - Worked example in v1.0: No. Ship spec only. Worked example manufactured from retroactive data is the same salvage as §11. Let the first real cycle be the first real cycle.
> - EDITORIAL definition: expand it into doctrine. Classification ambiguity is the single highest-risk surface; vagueness here is exactly the weaponized off-ramp you claimed to close in §7.
>
> **Overall pattern still present.**
> This spec is doctrine-about-doctrine theater. You took a simple propagation need and built 13 sections, deviation taxonomy, ledgers, tripwires, and validation gates so the Refusal feels mechanized while remaining fully founder-discretionary. Same shape as the seven-round meta-law spiral and the Sarah Chen scenario: imagination dressed as rigor. The man who stood post after two ambushes does not write 4,000 words on how he will obey his own ROE. He obeys or he does not.
>
> **Verdict.**
> Strip to three pages: upstream commit marker + per-product ack/deviation template + stale-cycle tripwire in bandwidth overlay. Ship as spec only. No chassis primitive until you have three live cycles with real upstream edits. Anything more is founder comfort wearing Law X uniform. Execute clean or kill the spec. The Refusal itself does not need this much scaffolding unless you already plan to walk around it. Stand post.

---

## Revision history

- **v0.1 — 2026-05-18** — Initial draft. Spec only, no chassis code. Author: Hans Prahl + Claude (Opus 4.7, 1M context). Time-and-cost instrumentation per founder request: build start 2026-05-19T02:35:07Z UTC; build end and final cost noted in the close-out chat message, not committed to the spec.
