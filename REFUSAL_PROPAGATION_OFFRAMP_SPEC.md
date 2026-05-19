# Refusal Propagation Off-Ramp — Primitive Spec

**Status:** **v0.2 — STRIPPED.** Spec only, no chassis code, no validation gate, no portfolio ledger. Reduced from 396 lines / 13 sections (v0.1) to the smallest mechanism that actually does work, per Grok adversarial review (preserved in §5). Law VII applies: provisional doctrine until at least three live §II.8 cycles have run through it.

**Date opened:** 2026-05-18.
**Owns deliverable slot:** *Refusal-propagation off-ramp primitive spec — 2026-05-25 (8 hrs)* in `STARTUP.md` Phase 1, shipped 7 days early.

---

## 1. Why this exists

The canonical Refusal lives at [THE_BUILDERS_DOCTRINE.md](THE_BUILDERS_DOCTRINE.md) §II.8 (three items as of v1.2). The four downstream products (TOP, Operator, Custer, RPR) carry per-product audits at `<product>/REFUSAL_AUDIT.md`. Today's propagation model is silent inheritance — when §II.8 is edited upstream, downstream audits do not auto-update and no mechanism forces re-acknowledgment.

This spec adds three things, and only three things:

1. A **commit-message marker** on every §II.8 edit that names the propagation class.
2. A **per-product entry** (acknowledgment or deviation) appended to each product's audit.
3. A **stale-cycle tripwire** that blocks the next release tag if any product has been silent on a cycle for more than 30 days.

That is the entire scope. The v0.1 draft grew past this and was stripped after Grok identified the same founder-romance pattern that produced Funkytown 03 (over-claim N=3) and Sarah Chen (imagined user treated as evidence).

---

## 2. The protocol

### Step 1 — Upstream commit marker

Any commit in `~/Projects/the-builders-doctrine/` whose diff touches [THE_BUILDERS_DOCTRINE.md](THE_BUILDERS_DOCTRINE.md) §II.8 includes a line in the commit message of the form:

```
§II.8 propagation cycle <YYYY-MM-DD> — <ADD|AMEND|REMOVE|EDITORIAL>:
<one-sentence description of the change>
```

`EDITORIAL` means no semantic change. Any other class opens a propagation cycle. The commit SHA is the cycle ID. Self-classifying a semantic edit as `EDITORIAL` to bypass the protocol is a falsification of the doctrine, not a permissible shortcut — Grok flagged this as the highest-risk weaponized path in §5 below. An expanded `EDITORIAL` definition belongs in the doctrine itself; it is open work pointed at upstream (§4 item 1).

### Step 2 — Per-product entry

For each of the four products, append one entry to that product's `REFUSAL_AUDIT.md` under a top-level `## Propagation log` section. Two templates; one is mandatory.

**Acknowledgment** (default, mandatory unless deviation is filed):

```
### Cycle <SHA-short> — <YYYY-MM-DD> — ACKNOWLEDGED
Edit class: <ADD|AMEND|REMOVE>
Summary: <copied from doctrine-repo commit message>
Product impact: <one or two sentences naming what changes>
Acknowledged by: <signer>
```

**Deviation** (required if and only if the product cannot literally inherit):

```
### Cycle <SHA-short> — <YYYY-MM-DD> — DEVIATION FILED
Edit class: <ADD|AMEND|REMOVE>
Summary: <copied from doctrine-repo commit message>
Reason: <why the product cannot literally inherit; cite product surface area>
Scope: <which features / surfaces the deviation covers; "all" must be defended>
Sunset: <calendar date — conditions do not qualify as sunsets>
Signer: <founder name; deviations are not Guardian-grantable>
```

No deviation taxonomy. No structured types. The reason field must do the work. Earlier drafts tried to pre-name the legitimate deviation patterns (STRUCTURAL_INAPPLICABILITY, SCOPE_NARROWING, TIMING_DEFERRAL); Grok showed the taxonomy was both incomplete and a romance surface, so the taxonomy is removed and prose-with-required-fields stands in its place.

### Step 3 — Stale-cycle tripwire

A cycle that has been open more than 30 days without all four product entries surfaces at the next weekly bandwidth-overlay check ([BANDWIDTH_OVERLAY_2026-05-15.md](BANDWIDTH_OVERLAY_2026-05-15.md) §5; first check 2026-05-21 EOD) and blocks the next doctrine-repo release tag until closed. No centralized ledger; the tripwire is a grep across the four product files.

---

## 3. What this does not pretend to do

Three honest negatives. They matter more than the protocol itself.

- **Does not bind a founder willing to lie in writing.** A vague-scope deviation that names a fake surface, a sunset date the founder has no intent to meet, a `STRUCTURAL_INAPPLICABILITY` argument that misrepresents the product — none are caught by the protocol's mechanical surface. The defense for that failure mode is adversarial review (Grok second-opinion workflow), git-tracked audit trails, and external readers. Not this spec. The v0.1 draft pretended otherwise in its §7 "weaponized off-ramping" surface; that section was theater and is removed.
- **Does not earn chassis status from a bootstrap.** The protocol does **not** retroactively log Operator's 2026-05-05 parasocial scope-narrowing as a "first closed cycle." That would be manufactured evidence — the same shape as the original Stage 7 N=3 over-claim. Operator's existing audit entry stays as it was written, on its own merits. This protocol applies forward from 2026-05-18 only.
- **Does not become `kit/chassis/refusal_propagation.py` until three real upstream §II.8 cycles have run through it live.** Until then it runs by founder discipline plus the git-tracked audit text. No chassis primitive. No portfolio-aggregation tooling. No automation. v1.0 ships the spec, not the chassis.

---

## 4. Open work pointed at upstream doctrine

Two items belong in `THE_BUILDERS_DOCTRINE.md` itself, not in this spec. Tracked for v1.5 doctrine work; not blocking v1.0.

1. **Expanded `EDITORIAL` definition** in §II.8 — explicit examples of what is and is not editorial. Classification ambiguity is the single highest-risk surface in this protocol (Grok, §5 below); leaving it tacit is exactly the weaponized off-ramp the v0.1 §7 claimed to close and did not.
2. **Doctrinal-obsolescence discipline** — what happens when the Refusal itself needs to change because empirical surface has overtaken it (e.g., a refusal written pre-2026 that breaks on frontier-model behavior in 2027). This spec covers downstream deviation; it does not cover upstream revision discipline. Grok caught this as the missing fourth deviation type. The right home is the doctrine's own revision protocol, not a category bin in this spec.

---

## 5. Adversarial Review — 2026-05-18 — Grok

Verbatim. Run via the manual Grok second-opinion workflow (per `~/.claude/projects/-Users-hansprahl-Projects/memory/feedback_grok_second_opinion_workflow.md`). Findings drove the v0.1 → v0.2 strip.

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

### Response to Grok (v0.2 reconciliation)

| Finding | Disposition |
|---|---|
| §5 incomplete — missing DOCTRINAL_OBSOLESCENCE | **Accepted in shape, redirected upstream.** Deviation taxonomy removed entirely (prose-with-required-fields stands). Upstream-revision discipline tracked as §4 item 2 for v1.5 doctrine work. |
| §7 weaponized-off-ramping defense is theater | **Accepted.** Section deleted. Replaced by §3 honest negative: "Does not bind a founder willing to lie in writing." |
| §11 bootstrap is salvage | **Accepted in full.** Bootstrap section deleted. §3 honest negative names this explicitly: Operator's 2026-05-05 entry is not retroactively run through this protocol. Protocol applies forward from 2026-05-18 only. |
| §13 ledger — move to private | **Deferred to founder.** v0.2 removes the centralized ledger entirely; the stale-cycle tripwire is a grep across product files. If a ledger surface returns later, the public-vs-private decision returns with it. |
| §13 worked example in v1.0 | **Accepted.** Spec only ships. No worked example. |
| §13 EDITORIAL definition expanded into doctrine | **Accepted in shape, redirected upstream.** Tracked as §4 item 1 for v1.5 doctrine work. |
| Overall — strip to three pages | **Accepted.** v0.2 is this file. |

The one finding I do not fully accept: Grok closed with *"Execute clean or kill the spec."* The kill option was offered; I chose strip-to-scope instead. The minimal mechanism (commit marker + per-product entry + tripwire) is small enough to be load-bearing without scaffolding, and Phase 1's silent-inheritance failure mode is real. The strip is not founder-comfort-in-uniform; it is the smallest thing that solves the named gap.

---

## Revision history

- **v0.1 — 2026-05-18T02:35Z** — Initial draft. 396 lines, 13 sections. Author: Hans Prahl + Claude (Opus 4.7, 1M context). Committed `803b917`.
- **v0.1+grok — 2026-05-18** — Grok adversarial review appended verbatim (commit `5ef9ad0`) before strip, preserving the v0.1 surface and the critique as a single artifact in git history.
- **v0.2 — 2026-05-18** — Stripped to scope per Grok adversarial review (§5 above). Removed: deviation taxonomy (old §5), portfolio ledger (old §6), weaponized-off-ramping defense (old §7), validation gate (old §9), cost table (old §10), bootstrap cycle (old §11), commit-discipline meta-section (old §12), open-decisions table (old §13). Added: §3 honest negatives (what this protocol cannot do); §4 upstream-doctrine open work. Net: 396 lines → this file. Same Phase 1 deliverable slot, smaller surface.
