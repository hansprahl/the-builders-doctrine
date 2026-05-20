---
status: LOCKED 2026-05-20 — Option C (Hybrid); provisional with mandatory re-review 2026-07-31
gate: Phase 1 deliverable #7 per RELEASE_PLAN_v1.md (reshaped to 4 hrs counsel-free, was 10 hrs) — SHIPPED 5 days early
owner: Hans Prahl (founder-only — no counsel engagement required for v1.0 lock)
parent: RELEASE_PLAN_v1.md §5 (Phase 1)
---

# Productize-vs-License decision — v1.0 scaffold

> The question: at v1.0 public release (2026-06-01), does the commercial vehicle for *AI Tradecraft / Assayer / Builders' Kit / Operator* run as a **Hans-owned productization** (build, sell, host, audit it ourselves), a **third-party licensing model** (license methodology + chassis + brand to a productizer, take royalty/equity), or a **hybrid** (license downstream commercial surfaces while Hans keeps the audit / certification / Operator core)?
>
> **The 2026-05-25 lock is provisional, not permanent.** Hans authors a position paper picking A / B / C provisionally and names the legal-instrument-signing-gated questions that defer to counsel later (when there's an actual licensee, an actual contract to draft, or a USPTO deadline). v1.0 release notes communicate the provisional structure transparently. No counsel engagement is required for the lock itself.

---

## 1. Why this is a v1.0-blocking decision

- **Pitch language differs.** Productize → "we build it for you." License → "we built the methodology; certified implementers run it." Hybrid → "free doctrine + paid Hans-owned audits + licensed downstream tooling."
- **Brand stack assignment differs.** Productize → all four marks (AI Tradecraft / Assayer / Builders' Kit / Operator) flow through one entity. License → Assayer/Builders' Kit may live under a licensee while AI Tradecraft (the umbrella) and Operator (patent-pending) stay with Hans.
- **Patent strategy informs but does not gate.** Subsystem A (Operator closed loop) is patent-pending. The lock just has to commit that Operator + Subsystem A stay carved out of any license. Detailed claim-language counsel is a separate v1.5+ workstream driven by USPTO timing, not by v1.0 ship.
- **Brad Hampton channel-not-customer relationship pivots on this.** Brad's intro offer (2026-05-12) is conditional on a sellable MVP. Whether Brad is introducing Hans's products to SMBs *or* introducing a licensee's productized version of Hans's methodology is two different conversations.

---

## 2. The three options, clean

### Option A — Productize (Hans-owned)
Hans builds the company. Assayer is the free scorer + doctrine; Builders' Kit is the paid operationalization product; Operator is the patent-pending closed-loop implementation; hosted audits + certification are services. One brand stack, one cap table, one founder.

**Pro:** Maximum founder upside; biographical moat lands on the same entity that sells the product; chain of command preserved end-to-end; aligns with Operator's patent-pending status. Counsel spend stays minimal because no licensing instruments are needed.
**Con:** Hans's time is the constraint; sales/support/SOC2/customer success all become Hans's problem; revenue gated on Hans's bandwidth which is already at-cap per BANDWIDTH_OVERLAY.

### Option B — License (third-party operationalization)
A licensee productizes Builders' Kit + Assayer downstream services (hosted onboarding, audits, certification). Hans retains methodology authorship + Operator + the AI Tradecraft umbrella. Royalty or equity in exchange.

**Pro:** Hans's bandwidth freed for doctrine + Operator; sales/support is licensee's problem; faster scaling if right licensee found.
**Con:** Loses operational control of the customer experience; biographical moat dilutes (the licensee's people, not Hans, run the audits); reputational exposure if licensee ships a compromised version of the doctrine; revenue ceiling lower; pick-the-wrong-licensee risk is existential; counsel spend (IP licensing + corporate transaction) becomes real before any revenue lands.

### Option C — Hybrid
Hans keeps Assayer (free), AI Tradecraft umbrella, Operator (patent-pending), and the audit + certification function (the high-trust + high-margin layer). License Builders' Kit operationalization (hosted onboarding, fielding deployments, customer success) to a third party who specializes in B2B implementation.

**Pro:** Hans keeps the brand-defining layers and the patent-protected layer; offloads the high-bandwidth low-leverage layers; biographical moat stays attached to the audit + certification function (the part that visibly requires the author).
**Con:** Three-way contract (Hans + licensee + customer) is more complex to draft *when the time comes*; quality control on the licensed implementation function requires audit gates; IP boundary line gets harder to police as Hans's audits surface licensee-shipped product behaviors. None of this is a v1.0 lock problem — it's a "before signing a real license" problem.

---

## 3. Founder-side analysis (the core work — Hans-authored, no counsel needed)

The decision-lock is built on five founder-side inputs. Hans drafts each before 2026-05-25 lock. No outside engagement required.

### 3.1 Bandwidth honest budget
What is Hans's realistic weekly hours-available for sales + support + customer success if Option A wins?
- Pull current values from `BANDWIDTH_OVERLAY_2026-05-15.md §1` capacity table
- Subtract committed weekly load (EMBA + Custer + Family + Health + Other)
- Remainder = productization budget per week
- If sustained remainder is <10 hrs/wk, Option A is bandwidth-failing as a v1.0 commitment

Honest note: Hans is already at-cap on doctrine work through 2026-07-25. The productization workstream cannot start in earnest until v1.0 ships AND the EMBA term load drops AND Custer's primary cycle resolves (June primary). Sequence-aware framing of Option A: "Hans-owned productization, sales motion begins post-Custer-primary (~July 2026)."

### 3.2 Brad Hampton channel framing
Re-read `project_brad_smb_trd_brd_niche_2026-05-12.md`. Brad named SMB TRD/BRD pairs as a 7/10 demand signal in his recent calls. The channel question:
- (A) Brad introduces Hans-direct for the v1 Operator SMB-spec product (already happening — Brian Friedman pilot in flight)
- (B) Brad introduces a third-party licensee who productizes the Builders' Kit operationalization layer
- (C) Brad introduces Hans-direct for audits + a future licensee for operationalization

Answer changes v1.0 outreach pitch on 2026-06-02. The Brian-pilot is the live evidence — if it converts to a real deliverable Hans can show Brad, Option A or C are both supportable. If the pilot stalls, Option B becomes more attractive but the lack-of-evidence problem becomes acute.

### 3.3 Biographical-moat-vs-licensee tension
The core doctrinal claim is that the moat is biographical — Hans's lived experience compiled into product behavior. A licensee operationalizes someone else's biography running someone else's product. Where is the line where the biographical moat dilutes too far to matter?

Default position (founder-named, subject to lock-week pressure-test): **audits and certifications stay with Hans because those are where the biographical signal is provably load-bearing. Operationalization (templates, hosted onboarding, sales) can be licensee-run because biographical signal there is reputational, not load-bearing.** This default biases toward Option C.

### 3.4 Operator carve-out is non-negotiable
Subsystem A is patent-pending. Operator stays Hans's regardless of decision A/B/C. The decision is about Assayer + Builders' Kit + audits — NOT Operator. The lock should state this carve-out in one sentence so the v1.0 release notes and any future licensing conversation inherit the boundary cleanly.

### 3.5 First-external-builder gate gates this decision
Per `RELEASE_PLAN_v1.md §6`, if no external builder runs the Kit by 2026-07-31, v2.0 prep pauses and positioning re-evaluates. If the Kit cannot be run cold, the productize-vs-license question is *premature*: there is nothing yet to productize and nothing yet to license. The 2026-05-25 lock is therefore **provisional, with mandatory re-review at 2026-07-31 release-gate check.** Re-review may confirm, re-shape, or retract the v1.0 lock — all three are doctrinally legitimate per Law VII.

---

## 4. Decision criteria (the rubric used 2026-05-25)

Score each option (A/B/C) on the four lenses Hans uses for reliability calls (`quote_reliability.md`):

| Lens | Question | A — Productize | B — License | C — Hybrid |
|---|---|---|---|---|
| **Audit** | If a buyer audits this in 12 months, which option's claims hold up? | Strong (Hans signs every audit; biographical signal lands on the same entity) | **Weak** (licensee signatures dilute biographical signal; audits become other-people's-work) | Strong (audits stay Hans-signed; the visibly-author-required layer stays with the author) |
| **Scale** | Which option survives 10× user volume without Hans being the bottleneck? | **Weak** (Hans is the bottleneck; bandwidth-failing per §3.1) | Strong (licensee absorbs sales/CS/operationalization load) | Strong (operationalization scales via licensee; audits cap at Hans's calendar, which is acceptable for a high-margin layer) |
| **Promise** | Which option lets Hans honor the doctrinal commitments (chain of command, biographical moat, "designed to be needed less") to customers? | Strong (chain of command end-to-end; one entity owns the promise) | **Weak** (licensee runs CX; chain of command breaks at the operationalization boundary; "designed to be needed less" hard to enforce through a third party) | Strong (Hans owns the high-trust + patent-pending layers; licensee bound by audit gates on the operationalization layer) |
| **Founder** | Which option does Hans want to operate inside for the next 5 years? | Acceptable but bandwidth-failing pre-July 2026 | Not chosen (no named counterparty in the data) | **Acceptable** — matches the operating shape Hans chose 2026-05-20 |

**LOCKED: Option C (Hybrid).** Three lenses favor C with no lens below "acceptable." A wins Audit + Promise narrowly but fails Scale hard against §3.1 bandwidth reality. B fails Audit AND has no named counterparty — locking B would be a paper commitment against zero counterparty (a Sarah-Chen-shape, per `feedback_grok_second_opinion_workflow.md`). The tiebreaker question — least-sure-Hans-can-honor lens — is Scale-for-C: capacity to operate the audit function at 10× user volume depends on whether the certification function admits sub-Hans signers later. That's the real risk and is recorded explicitly so the 2026-07-31 re-review can score it against actual evidence.

---

## 5. Sequencing — what happens between now and 2026-05-25

All hours are Hans-only. No counsel coordination required.

| Date | Action | Hours |
|---|---|---|
| 2026-05-20 | Draft §3.1 bandwidth honest budget against BANDWIDTH_OVERLAY actuals | 0.5 |
| 2026-05-21 | Draft §3.2 Brad channel framing; cross-check Brian-pilot status | 0.5 |
| 2026-05-22 | Draft §3.3 biographical-moat dilution line + §3.4 Operator carve-out statement | 1 |
| 2026-05-23 | Draft §3.5 provisional-vs-permanent framing; populate §6 counsel-gated appendix dates | 0.5 |
| 2026-05-24 | Score §4 rubric for A/B/C; identify lens with weakest score (tiebreaker / risk lens) | 0.5 |
| 2026-05-25 | **Lock provisional decision.** Write v1.0 release-notes paragraph reflecting the lock. Update RELEASE_PLAN §5 deliverable status. Commit. | 1 |

**Total Hans hours: ~4** (down from 10; the counsel-coordination hours fall away).
**Critical path: none external.** Founder-only work, parallelizable across the week.
**Slip risk:** zero counsel dependency. Worst case is Hans's own bandwidth — but the budget is 4 hrs across 6 days, with EMBA + Custer + Family + Health + Other absorbing the dominant weekly load.

---

## 6. Counsel-gated questions appendix (dated, deferred until trigger fires)

These are the questions that DO need outside counsel — just not for the v1.0 lock. Each carries a triggering event that determines when the question must be answered.

### 6a. IP counsel (Peter Lemire) — fires when a real licensee is identified

| Question | Triggering event | Target answer date |
|---|---|---|
| Trademark license structure (Builders' Kit + Assayer marks) — single license or split-by-mark? | A named third-party licensee proposes a deal | Within 30 days of licensee identification |
| Copyright license over templates + scorer code — exclusive, non-exclusive, sub-licensable? | Same | Within 30 days of licensee identification |
| Trade-secret protection language for Operator runtime / chassis internals if any licensed surface touches them | Same | Within 30 days of licensee identification |
| Carve-out language for Subsystem A patent-pending claims — confirm license terms preserve Hans's entity ownership | Same | Within 30 days of licensee identification |
| `assayer.dev` collision — does the licensing structure change the survivability calculus? | Same (only if Option B or C wins) | Same window |

**Estimated counsel scope when triggered:** Memo or 1-hr structured call. Peter is already engaged (2026-05-05); engagement letter outstanding; this is incremental scope under existing relationship, not a new engagement.

### 6b. Corporate counsel + fractional GC (Justin Vaughn) — fires when a real instrument needs drafting

| Question | Triggering event | Target answer date |
|---|---|---|
| Entity structure — does Hans need a separate co to receive royalties, or do they flow through Prahl Investments LLC? | A licensee deal moves past LOI / term-sheet stage | Before signing the license agreement |
| Royalty / equity / license-fee transactional structure — Justin's actual instrument-drafting work | Same | Before signing the license agreement |
| Sub-licensability and termination provisions | Same | Before signing the license agreement |

**Estimated counsel scope when triggered:** Drafting + review of the license agreement itself. Real spend; gated by a real revenue path, not by v1.0 ship.

### 6c. Patent attorney (TBD via Peter's referral) — fires on USPTO timeline, NOT on v1.0 ship

| Question | Triggering event | Target answer date |
|---|---|---|
| Provisional → non-provisional conversion for Subsystem A | USPTO 12-month provisional clock | Per provisional filing date + 11 months |
| Claim-language scope vs. Builders' Kit license (carve-out preservation) | Above + any licensee deal in motion | Before non-provisional filing |
| Continuation strategy if early claims reject | First office action | Per USPTO response window |

**Estimated counsel scope when triggered:** Full prosecution engagement — the large spend, $10K–30K+ range, no v1.0 dependency. **This is the engagement Hans cannot afford right now and does not need for v1.0.** It defers to v1.5 prep at earliest, gated by traction signal under the existing release-cadence pattern.

### 6d. CPA or tax attorney — fires when royalty income lands

| Question | Triggering event | Target answer date |
|---|---|---|
| Tax treatment of license royalties vs. operating revenue | First royalty payment received OR first license agreement signed | Within 30 days of trigger |
| Pass-through vs. retain in Prahl Investments LLC | Same | Same |

**Estimated counsel scope when triggered:** 1–2 hour engagement with existing CPA or tax-focused attorney; not a strategic dependency on v1.0.

---

## 7. What the 2026-05-25 lock produces

Three artifacts, committed same day:

1. **Updated §4 rubric scored** in this file with A / B / C scores, the locked option named, and a one-paragraph rationale.
2. **v1.0 release-notes paragraph** (drafted same day, used in `RELEASE_NOTES_v1.0` round-4) — communicates the provisional structure transparently. Sample shape: *"v1.0 ships under [Option X] structure. Operator (Subsystem A patent-pending) remains a Hans-owned carve-out under all scenarios. Legal instruments for licensing (if any) defer to counsel review at the point a third-party deal is named. The structure is re-reviewed at the 2026-07-31 release-gate check per the release-cadence framework."*
3. **RELEASE_PLAN_v1.md §5 row updated** — deliverable #7 status: SHIPPED, hours actual ~4, scope counsel-free per scaffold reshape 2026-05-18.

---

## 8. What this scaffold does NOT do

- Does not lock the answer pre-2026-05-25. Options A/B/C remain open until §4 rubric is scored and Hans signs the call.
- Does not engage any outside counsel. All counsel-gated questions live in §6 appendix with explicit triggering events.
- Does not commit Hans to permanent framing. §3.5 anchors the provisional-with-2026-07-31-re-review framing.
- Does not address Operator's `PATENT_DISCLOSURE.md` inventor-bio error (line 160 — "USMC retired" should be "Army NG retired"). That's flagged elsewhere for first patent-attorney contact, not blocked by #7.
- Does not address the "raise money" workstream. That is a separate strategic question, parallel to #7, with its own scope-and-options conversation needed before any scaffold.

---

## 9. Lock decision — 2026-05-20

**Decision:** Option C (Hybrid). Shipped 5 days early against 2026-05-25 target.

**Locked structure:**

```
Hans-owned (under all scenarios):
├── Operator               — Subsystem A patent-pending; non-negotiable carve-out per §3.4
├── AI Tradecraft          — umbrella mark
├── Assayer                — free public scorer + doctrine document
└── Audit + certification function — high-trust, biographically-load-bearing per §3.3

Open to license when a real counterparty surfaces:
└── Builders' Kit operationalization — hosted onboarding, fielding deployments, customer success
```

**Rationale.** Three of four rubric lenses (Audit, Scale, Promise) favor C with no lens below acceptable. Option A failed Scale against §3.1 bandwidth honest budget — sustained productization budget pre-July 2026 is effectively zero per BANDWIDTH_OVERLAY actuals; locking A would commit to a 2026-06-01 sales motion Hans cannot staff. Option B failed Audit (licensee-run audits dilute biographical signal at the layer where biographical signal is provably load-bearing) AND had no named counterparty in the data — locking B would be a paper commitment against zero counterparty.

**Provisional, not permanent.** Per §3.5 first-external-builder gate, mandatory re-review at 2026-07-31 release-gate check. The lock may be confirmed, re-shaped, or retracted at re-review — all three are doctrinally legitimate per Law VII.

**Signer:** Hans Prahl, 2026-05-20.

**Scale-of-audit-function risk (recorded):** Capacity to operate the certification function at 10× user volume depends on whether the function admits sub-Hans signers later (apprentice-certifier or third-party-attested-by-Hans patterns). This is the named risk lens for C. Re-evaluate at 2026-07-31 against actual user-volume evidence.

**No counsel engagement triggered.** Lock is founder-only per §6 — every counsel-gated question stays in §6 appendix until its triggering event fires.

---

## 10. Cross-references

- `~/Projects/the-builders-doctrine/RELEASE_PLAN_v1.md` §5 Phase 1 — deliverable #7 timing; update estimate from 10 hrs → 4 hrs on lock day
- `~/Projects/the-builders-doctrine/STARTUP.md` "Brand stack (locked 2026-05-05)" + "Hands-off" section — IP boundaries
- `~/Projects/the-builders-doctrine/BANDWIDTH_OVERLAY_2026-05-15.md` — Wk 05-22 capacity (28 hrs) vs. three converging deliverables on 2026-05-25; the 6-hr reduction from #7 buys margin against Law IX threshold
- `~/Projects/operator/PATENT_DISCLOSURE.md` — patent-pending Subsystem A; inventor-bio error flag
- `reference_peter_lemire_ip_counsel.md` — Peter's engagement scope and the patent-attorney-vs-IP-counsel taxonomy that drives §6
- `quote_brad_hampton_biographical_moat.md` — biographical-moat thesis endorsement, relevant to §3.3 + §4 Promise scoring
- `project_brad_smb_trd_brd_niche_2026-05-12.md` — Brad channel framing input for §3.2
- `project_brian_friedman_operator_test_candidate_2026-05-15.md` — live evidence stream for §3.2 channel scoring
- `quote_reliability.md` — four-lens reliability rubric used in §4
- `quote_how_can_this_make_money.md` — commerce-axis doctrine; every option must name a revenue path, not posture
