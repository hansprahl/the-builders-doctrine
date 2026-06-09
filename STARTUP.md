# STARTUP — The Builders' Doctrine (AI Tradecraft meta-repo)

> Last updated: 2026-05-15. When this file disagrees with the code, the code wins.

## Identity

Portfolio-meta repo for **AI Tradecraft, by Hans Prahl**. Holds the methodology (Builders' Doctrine), the Kit (coverage scorer + interview templates that walk a builder through it), and the Chassis (seven portable runtime components lifted from TOP/Operator/Custer + ported from Principle #12). Sits *above* every per-product `CLAUDE.md`. Private through public release; release gated on one external builder running the kit cold and producing a working instance.

**Stage:** **v1.2 tagged 2026-05-13** (ratifies the in-flight v1.2 changes that had been live since 2026-05-01). v1.0 + v1.1 tagged 2026-04-30 (initial draft + post-stress-test propagation cycle). v1.2 captures: Principle #1 rename ("code is the story"), Principle #12 *What else? Active extraction* (2026-05-06, `876f452`), Principle #13 *The Long Horizon* (2026-05-12, `ad0d125`), Mission Command Architecture (2026-05-12, `3a3bb0d`) with Authority Gradient + Scale-Up Role Taxonomy + Staff Channel sections added (2026-05-13, `82e26ff`), Amazon LP cross-map + Working Backwards methodology, Kit field surface brought current (88 fields across 8 templates), `pr_faq_interview.yaml`, `chassis/reflection_gate.py` (seventh chassis component, Principle #12 primitive, 29 tests), and `chassis/authority_gradient.py` (eighth chassis component, MCA Authority Gradient primitive, 43 tests, 2026-05-13 `992e1b1`). Public-release brand **LOCKED 2026-05-05 as Assayer**. MCA is empirically validated at Platoon scale across two experiments: Funkytown 01 (N=3 × 7 ablation stages, ~$64) and Funkytown 02 Authority Gradient (N=3, 2026-05-13, mean 61.1% in-unit resolution, 0 tier violations, 0 hard-floor breaches — ✅ validate). Company and Battalion scale-up taxonomy is doctrine, not validated architecture.

**Late evening + late-late evening 2026-05-13 — Grok adversarial review (7 rounds) + retractions + Laws V–X + ADP 6-0 translation + N=9 Company engineering scaffold:** Two over-claims caught and retracted: (a) Experiment 02b's "structured-uncertainty enforcement" reframe of the Reflection Gate (1/31 catches on engineered trigger is failure, not reframe-able win — gate's primary-detection claim deprecated pending redesign); (b) Funkytown 03 MVP smoke test mis-claimed as "first-contact validation of MCA at Company echelon" — N=3 simplified single-Sonnet platoons on a synthetic brief with a hand-placed trap is engineering scaffold, not doctrinal advance. Both retractions committed (`ed1eff7`). **`META_DOCTRINE.md` now holds six formal laws (V–X), cap stands.** Law V (Echelon Decay Gate), Law VI (Biographical Falsification Gate — Stage 7 Law I claim deprecated pending N≥9 across ≥3 briefs with blinded controls + external statistician audit), Law VII (Provisional Doctrine Rule — holds require dates not stance), Law VIII (Meta-Schedule Gate — bandwidth overlay before milestones), Law IX (Delegation Threshold — single-point-of-failure protection), Law X (Execution Threshold + cap — no new laws or deliverables added from adversarial review until prior actions ship with measurement surface; prose-only artifacts auto-truncate at date). **`ADP_6_0_TRANSLATION.md` shipped** (`37fde63`) closing the civilian-audience risk on Army vocabulary. **N=9 Haiku Company engineering scaffold:** mean $1.07/run, total $9.66 for N=9, mean wall 32 min — engineering scaffold only (hand-placed trap, Law V rejects). 4 hard-floor breaches discovered (PL-direct `send_email_mock` dispatch — measurement layer worked, enforcement layer either misclassified or in observe-only mode). Alpha-bug non-reproduction on Haiku confirmed (0/9). CC reflection gate fired on 5 of 8 declare_dones (62.5%) on natural prose. **Cost estimates $60K-120K, $200K-500K, and $10K-50K all withdrawn — ladder cost unmeasured above Platoon, per Law VI text.** Validated rungs: **Squad + Platoon (1, 2 of 9).** Rung 3 (Company) **not yet validated** — the harness for live cross-echelon conflict injection remains the prerequisite.

**2026-05-14 — Release-cadence reframe (RELEASE_PLAN_v1.md, `ab95bd7`):** Truncate-at-Platoon flips from contingency to **Plan A.** v1.0 ships what is proven now — 13 principles, MCA at Platoon scope, 8 chassis components *(updated 2026-05-21: now 9 after founder-romance detector v0.1 shipped 2026-05-20 `81dfbd7`)*, the Kit, Funkytown 01 + 02 results, ADP 6-0 translation, Laws V–X — with explicit Principle #1 deprecation notice and dated v1.5 roadmap. v1.5 carries the Law VI replication verdict (statistician + OSF pre-reg + 108 runs, target 2026-07-25). v2.0 carries Company-scale validation + community-replication study (Q4 2026). Same destination, standard versioned release cadence. **v1.0 ship target: 2026-06-01.** Bandwidth overlay populated 2026-05-14 — 219 hrs realistic productive capacity across 7 weeks *(later corrected to 105 hrs at 15 hr/wk — see 2026-05-21 paragraph below)*; deliverables #1–3 (overlay, weekly tripwires, Law VIII truncation criteria) shipped same day, one day early per Law VIII. The original 12-deliverable post-Grok schedule was front-loaded infeasibly (41 hrs needed Wk 05-15 vs. 29 capacity); Law IX re-cut at the gate produced the release-cadence reframe rather than per-week date slips. **Combined v1.0 + v1.5 budget at original scope: 176 hrs across 10 weeks vs. 219 hrs available** *(corrected 2026-05-21 to ~115 hrs remaining demand vs. 150-hr 10-week capacity at 15 hr/wk; see 2026-05-21 paragraph)*. `LAW_VI_PRE_REG_v1.md` founder-drafted same day (statistician sign-off blocks v1.5 release, not v1.0). `CHASSIS_PROPOSED_EXTENSIONS.md` originally staged Adversarial Review chassis spec — **RETRACTED 2026-05-19** by Grok cold-read KILL verdict on the pre-registration plan (killed artifact at `archived-prose/2026-05-19_adversarial_review_pre_reg_v1_KILLED.md`). The regex founder-romance detector reverts from fallback to primary for the 2026-05-25 Phase 1 deliverable slot. Fourth Grok catch in seven days (META spiral 05-13, Sarah Chen 05-15, REFUSAL_PROPAGATION v0.1 05-18, this pre-reg 05-19); the manual Grok workflow is now the empirically load-bearing audit gate that the chassis was trying to mechanize.

**2026-05-21 — First weekly bandwidth check-in + capacity re-cut + all Phase 1 deliverables shipped early:** First Thursday EOD weekly check-in executed end-to-end per BANDWIDTH_OVERLAY §4d (commit `5480322`). **All 5 Phase 1 + 3 Phase 2 deliverables shipped under estimate, 5–7 days early** (founder-romance detector v0.1 `81dfbd7` 2026-05-20 was the last; productize-vs-license LOCKED `712684a`, refusal-propagation FROZEN `f800b38`, framework-holds audit `4d24319`, EXPLAINER rewrite `9ffa65e`, release notes `4fe5afa`, landing page `dd2732b`, doctrine-repo CLAUDE.md `6bd8334`). Reshape discipline collapsed ~58 hrs of planned scope to ~9 hrs actual. **Capacity correction:** Hans-stated capacity is **15 hr/wk steady-state** with ~25 hr/wk crash ceiling for known windows; the 40%-of-raw heuristic's 29 hr/wk was 1.9× too generous. Same-session calibration walked 5 → 10 → 15 as forward demand was made explicit. **Tripwires fired:** §5#1 (doctrine workstream observable ~40–60 hrs vs. 15-hr capacity = 167–300% over the 25% threshold) and §4c.3 (utilization ~267–400%); both fire mechanically. **Action ratifies existing Plan A** — truncate-at-Platoon v1.0 ship 2026-06-01 was already locked per RELEASE_PLAN `ab95bd7`; no scope change. Overshoot is from unplanned empirical work (Operator dogfood asymptote N=1→N=20 across 2026-05-18 → 2026-05-19; Funkytown Exp 05–10 on 2026-05-20; 4 Grok pressure-tests in 7 days), not deliverable bloat. **Statistician delegation of Law VI execution by 2026-06-22 is now mandatory** (not optional) — at 15 hr/wk solo Law VI execution consumes the ~35-hr buffer; with delegation, v1.0 + v1.5 fit with margin. **Next move: next-gate re-cut 2026-05-28 (Thursday EOD) per §4c.3 prescribed action; Funkytown Exp 10b + 10 by 2026-05-30 (~6–8 hrs); v1.0 ship + landing-page deploy + Brad outreach 2026-06-01–06-02.**

## Commander's intent (north star)

> Lived experience compiled into AI-product behavior. Ethics encoded as commandments, refusals named explicitly, agents calibrated against truthful outcomes. Methodology ships free; operationalization (kit, hosted onboarding, audits) generates revenue downstream. The hard gate is one external builder running the kit cold and producing a working product instance. Until that happens, none of this goes public.

## Brand stack (locked 2026-05-05)

```
AI Tradecraft (umbrella, by Hans Prahl)
├── Assayer            — free public scorer + doctrine document
├── The Builders' Kit  — paid operationalization (this repo's kit/)
└── Operator           — patented closed-loop implementation
```

## Active phase — v1.0 SHIPPED 2026-05-21 (11 days early)

Operational plan: `RELEASE_PLAN_v1.md`. Public release flipped 2026-05-21 PM, 11 days ahead of the 2026-06-01 target. All Phase 1 + Phase 2 deliverables shipped under estimate, 5-10 days early. Repo flipped public + GitHub Pages enabled + v1.0-public tag pushed same evening. Brad outreach holds for 2026-06-02 per the v2-final draft framing ("three weeks after our 5/12 call").

Next live phase: v1.5 prep (2026-05-22 → 2026-07-25). v1.5 carries the Law VI biographical-substrate replication verdict. Statistician outreach sent 2026-05-21 to Philip Beaver (Daniels MSBA director) as the DU channel; awaiting reply. Bandwidth ledger continues at 15 hr/wk per the 2026-05-21 capacity correction.

**Phase 1 — Final v1.0 prep:**
- ~~2026-05-22 — All framework holds carry execution dates (Law VII compliance pass) [6 hrs]~~ — **SHIPPED 2026-05-15 (`4d24319`), 7 days early; 1.5 actual hrs; inline edits, no standalone artifact**
- ~~2026-05-25 — Productize-vs-license decision locked (10 hrs, Hans + counsel)~~ — **LOCKED 2026-05-20 (`712684a`), 5 days early; Option C (Hybrid); ~4 actual hrs counsel-free per scaffold reshape**
- ~~2026-05-25 — Refusal-propagation off-ramp primitive spec (8 hrs)~~ — **FROZEN 2026-05-20 (`f800b38`), 5 days early; v0.2-FROZEN; ~1 actual hr spot-check**
- ~~2026-05-25 — Founder-romance detector — pre-commit hook on doctrine repo (13 hrs)~~ — **SHIPPED 2026-05-20 (`81dfbd7`), 5 days early; v0.1 (regex + pre-commit hook + corpus); ~2 actual hrs vs 13 scoped. Adversarial Review chassis successor was retracted 2026-05-19 by Grok KILL verdict; regex implementation per original `feedback_close_up_this_session.md` round-7 spec.**

**Phase 2 — Public-facing artifacts:**
- ~~2026-05-27 — EXPLAINER rewrite — no biographical-moat causal claim~~ — **SHIPPED 2026-05-20 (`9ffa65e`), 7 days early; ~40 min actual.** Deprecation-as-trust-signal frame adopted; reshape collapsed 15-hr scope. (Remaining: per-product CLAUDE.md audience-tune and doctrine-root CLAUDE.md were separated as smaller items.)
- ~~2026-05-29 — v1.0 release notes draft~~ — **SHIPPED 2026-05-20 (`4fe5afa`), 9 days early; ~20 min actual.** First-ever logged founder-romance-detector override (Principle #4 verbatim name caught as FP).
- ~~2026-05-30 — Public landing page artifact~~ — **SHIPPED 2026-05-20 (`dd2732b`), 10 days early; ~1 hr actual.** One-pager static HTML at `docs/index.html` + `docs/style.css`. Carries deprecation-as-trust-signal frame. **Not deployed.** Deploy is gated to ship day (see "Ship-day deploy" below).
- ~~2026-06-01~~ **SHIPPED 2026-05-21** — **v1.0 git tag + public release announcement + landing-page deploy**

**Ship-day deploy (SHIPPED 2026-05-21) — two-step Pages enablement:**
1. **Flip repo public.** GitHub → Settings → General → Danger Zone → "Change repository visibility" → Public. Confirms the v1.0 ship is observable. *Why now and not earlier:* the repo is currently private and GitHub Pages on private repos requires Pro/Team/Enterprise. Keeping it private through Phase 1+2 also kept pre-ship drift (the strikethrough commits, the doctrine sweeps) invisible — landing page sits in `docs/` ready but unreachable until this flip.
2. **Enable Pages.** GitHub → Settings → Pages → Source = "Deploy from a branch" → Branch = `main` / Folder = `/docs` → Save. The page resolves at `https://hansprahl.github.io/the-builders-doctrine/` within ~1–2 minutes. Optional: register `assayerhq.com`, add a CNAME file to `docs/CNAME`, configure DNS A records per GitHub's published IPs.
3. **Tag** `git tag -a v1.0-public -m "..."` and `git push origin v1.0-public`.
4. **Brad Hampton outreach 2026-06-02** with the live URL.

**Wk 05-29 is fully protected** — EMBA finals + Exam 2 + Conceptual Quiz week, zero doctrine hours per the bandwidth overlay.

**v1.5 commitments (binding per Law VII):**
- 2026-06-22 — External statistician engaged *(resolves BANDWIDTH_OVERLAY §4c.1: the overlay's 2026-05-18 statistician-id deadline is superseded by the release-cadence reframe `ab95bd7`. Cascade does not fire; truncate-at-Platoon is already Plan A.)*
- 2026-07-01 — LAW_VI_PRE_REG_v2 with statistician sign-off
- 2026-07-05 — OSF.io public pre-registration
- 2026-07-15 — Law VI experiment complete (108 runs, 3 arms, 3 briefs)
- 2026-07-25 — **v1.5 release** (Law I earned, qualified, or retracted)

**Queued doctrine ports (post-gate, Law X — do not build before the statistician packet ships):**
- **Intelligence doctrine (ADP 2-0 / FM 2-0 / ATP 2-01.3 IPB / ATP 2-01 collection mgmt)** — next real doctrine port, Hans-selected 2026-06-05. Highest biographical-moat fit in the survey: the doctrine already speaks the MI dialect (PIR / EEI / RFI / CCIR / K-I-G) but never ported the grammar those terms come from; IPB is the analytic counterpart to MDMP, collection management is the RFI/PIR machinery already half-built in MCA. **Law X disposition:** deferred until the statistician packet ships (2026-06-22 per v1.5 commitments above) opens the execution threshold; queuing it now is not building it. **Scope guardrail:** port as *tradecraft documentation* (the FM 6-0 cross-map pattern — ships no new causal claim), NOT as biographical-moat evidence — precisely because Law VI has that thesis under falsification test until 2026-07-25. F3EAD / D3A targeting folds in as a sub-component, not a standalone port. Survey of the full doctrine landscape (Law of War→Refusal, ADP 5-0 assessment, ADP 6-22, etc.) captured in the 2026-06-05 session; runner-up was the Law-of-War→Refusal cross-map (deferred with this).

**Open from prior phase (carry over, not blockers for v1.0 ship):**
- **External validation** — three thesis letters sent 2026-05-05 (Myers, Brad, Whitaker). **Brad path is moving**: biographical-moat thesis endorsed 2026-05-06 (`quote_brad_hampton_biographical_moat.md`); 30-min call 2026-05-12 named a specific SMB market gap (TRD/BRD pairs for Gemini Enterprise, 7/10 of his recent calls). Brad is **channel, not customer** — intro offer conditional on a sharper pitch + sellable MVP. **v1.0 pitch lands on chassis + methodology + audit discipline; biographical-moat is v1.5 conditional.** Myers and Whitaker statuses not in memory; assume silence. Operator elevator pitch v1 captured 2026-05-12 (`quote_operator_elevator_pitch_v1_2026-05-12.md`). Brad outreach with v1.0 link scheduled 2026-06-02.
- **Chassis adoption** — chassis ships standalone at v1.0; downstream wiring is per-product follow-on, not gated to v1.0 ship. As of 2026-05-21: Guardian structural scoring layer Borg-ported to TOP (`8a47d39`) and Custer (`ca8aa33`) on 2026-05-09; Operator skipped. Authority Gradient referenced in all 4 product CLAUDE.mds but not yet imported. The wiring debt is a v1.5+ item, not a v1.0 ship blocker.
- **Custer STORY.md** — track on Custer side; not load-bearing for this repo.
- **Trademark queue** — Assayer (Class 9 + 42), AI Tradecraft, Builders' Kit, Operator. Peter Lemire owns.
- **Domain footprint** — `assayerhq.com` + defensives + `aitradecraft.io` not yet registered. Landing page deliverable 2026-05-30 forces the registration gate.
- **`assayer.dev` collision** — production-readiness-review tool in adjacent class. Decision: proceed; bet on substrate differentiation. Peter to confirm in formal sweep.

## Architecture (load-bearing)

- **`THE_BUILDERS_DOCTRINE.md`** — the prose. **Thirteen principles**: seven foundational ethics + six operational doctrines. Canonical doctrine artifact. (v1.0 shipped with 11; #12 and #13 folded in post-tag.)
- **`MISSION_COMMAND_ARCHITECTURE.md`** — portfolio-wide agentic architecture (2026-05-12). ADP 6-0's seven principles mapped to LLM-agent properties; 3-tier Platoon Pattern; recursive composability; context isolation between echelons. **Provisionally adopted** based on Funkytown Experiment 01 (Platoon scale, N=3 × 7 ablation stages, ~$64). Scale-up to Company/Battalion is the next falsification rung.
- **`SCHEDULER_SPEC_DRAFT.md`** — primitive spec paired with MCA (2026-05-12). Time-based intent injection into the running unit.
- **`WORKING_BACKWARDS.md`** + **`AMAZON_LP_CROSSMAP.md`** — Amazon's PR/FAQ-first product methodology adopted 2026-05-12 as the portfolio-shared scoping process. Operationalizes Principle #13 at the scoping layer. Vocabulary buys legitimacy in the SaaS/AWS channel (per Brad Hampton call 2026-05-12).
- **`PRINCIPLE_13_DRAFT.md`** — drafting workspace for Principle #13 (already folded into the doctrine prose; retained as scratchpad).
- **`PROMPT_DOCTRINE.md`** — universal prompt structural rules. The rubric every product's Guardian enforces.
- **`THE_BUILDERS_METHOD.md`** — the methodology in builder-facing form.
- **`kit/coverage.py`** — single-file scorer. Three CLI surfaces (`--score`, `--list`, `--interview`). As of v1.2: scores **88 fields across 8 templates** including the new MCA position fields (SPECIALIST_TEMPLATE), Principle #12 gate (AGENT_DOCTRINE), Principle #13 refusals (COMMANDMENTS), and the Working Backwards surface (PR_FAQ_TEMPLATE).
- **`kit/templates/`** — seven templates (STORY, COMMANDMENTS, REFUSAL_LIST, CRISIS_TRIGGERS, SPECIALIST_TEMPLATE, AGENT_DOCTRINE, SECURITY) with `KIT:FIELD` markers.
- **`kit/onboarding/`** — seven interviews with `depends_on` graphs that enforce authoring order (added `pr_faq_interview.yaml` in v1.2).
- **`kit/chassis/`** — **nine portable runtime components** (added `reflection_gate.py` + `authority_gradient.py` in v1.2; `founder_romance_detector.py` added 2026-05-20 `81dfbd7`): Crisis Floor, Approval Queue, Per-User Context (ContextVar with LookupError-on-unset), Named Specialists, AAR Loop, Prompt Guardian, **Reflection Gate** (Principle #12 primitive, scope-aware: operator_tool / wellness / founder; 29 unit tests), **Authority Gradient** (MCA primitive — Tier/Channel enums, overridable tool→class table, `on_world_boundary` callback hook composing with ApprovalQueue; 43 unit tests; ported from funkytown Experiment 02 validation), **Founder-Romance Detector** (regex linter for 7 observer-bias patterns; pre-commit hook on doctrine repo; field-validated against 49 doctrine .md files). 276 unit tests total; 8 parity tests against TOP's actual production constants.
- **`baselines/v1.1/`** — frozen baseline for the next stress-test propagation.

## Active risks

1. **Single-builder validation still pending.** Brad call 2026-05-12 named a market gap and offered conditional intros; no external builder has yet run the Kit cold. Brad is channel, not customer — the release gate has not moved. **Mitigated by release-cadence reframe:** v1.0 ships 2026-06-01 with public landing page + Brad outreach 2026-06-02, putting the Kit in front of external eyes by mid-June; if no external builder runs by 2026-07-31, v2.0 prep pauses and positioning gets re-evaluated (RELEASE_PLAN §6).
2. ~~**Doctrine–Kit drift.**~~ **CLOSED in v1.2 (2026-05-13).** Doctrine carries 13 principles + MCA + Working Backwards. The Kit's templates now score those layers explicitly.
3. **Public-launch attack surface on Principle #1 deprecation.** v1.0 ships the biographical-moat principle with explicit deprecation notice and v1.5 commitment to earn / qualify / retract via Law VI replication (2026-07-25 verdict). Risk is the obvious one: "your headline principle is deprecated." Mitigation per RELEASE_PLAN §7: lead with deprecation as trust signal — "we tested our most cited principle, found N=3 insufficient, named it publicly, running the proper study by 07-20." Honest before comfortable.
4. **MCA empirical claims governed by Law V (Echelon Decay Gate).** Squad + Platoon validated (Funkytown 01 + 02). Company is **not yet validated** — 2026-05-13 evening MVP smoke test is engineering scaffold per the post-Grok retraction. Law V requires N≥9 full-hierarchy runs with live cross-echelon conflict injected before any rung-N validation claim ships. v1.0 ships MCA at **Platoon scope only**, with rungs 3–9 named as hypothesis. Company validation deferred to v2.0 (Q4 2026).
5. **Soak debt on the chassis wiring** (carry-over, NOT a v1.0 ship blocker). 3,500 lines shipped 2026-05-01. As of 2026-05-21: chassis ships standalone at v1.0; per-product wiring is post-v1.0 follow-on. Founder-Romance Detector (the ninth chassis component, shipped `81dfbd7` 2026-05-20) IS wired live in this repo's pre-commit hook — the doctrine product is its own first adopter. Authority Gradient referenced in all 4 product CLAUDE.mds (Custer `356669a`, TOP `55e7a88`, Operator `376510c`, RPR `9943bcc`) but not yet imported by any product code; Operator queued first adopter. v1.0 ships the chassis as **engineering ports only** — biographical-moat causal claim explicitly withdrawn from chassis docs per RELEASE_PLAN §1.
6. **Bandwidth tripwires fired 2026-05-21 — action ratifies existing Plan A.** First Thursday EOD weekly check-in (commit `5480322`) found doctrine workstream observable ~40–60 hrs vs. corrected 15 hr/wk capacity. §5#1 fired (167–300% over 25% threshold) and §4c.3 fired (utilization ~267–400%). Prescribed action: truncate-at-Platoon v1.0 ship 2026-06-01 — **already Plan A** per RELEASE_PLAN `ab95bd7`, so the trigger firing ratified the existing plan rather than forcing a reversal. Next-gate re-cut 2026-05-28. **Statistician delegation of Law VI execution by 2026-06-22 is now load-bearing** for v1.5's ~35-hr buffer at 15 hr/wk. Pre-registered triggers in `BANDWIDTH_OVERLAY_2026-05-15.md §5` remain operative for subsequent weeks; auto-fallback B remains the floor mechanism if any deliverable miss re-cut date by ≥25%.
7. **Brand-collision in adjacent space.** `assayer.dev` is live in production-readiness-review. Acceptable but real; no silent re-litigation without new info.
8. **No CI on this repo.** All gates (gitleaks, prompt-injection scan, parity tests) live in product repos. Doctrine repo is doctrine + kit; treat changes here as carefully as any product repo because every product inherits at next Guardian audit.

## Hands-off

- **Material doctrine edits** — Hans approval + version bump. Editorial (typo, clarification, example) is fine.
- **Patent-adjacent text** — Subsystem A (the closed loop) is patent-pending. The split between free (Assayer scorer + doctrine) and paid (corrector, stash-and-rollback, two-corrector router, recommendations engine, CI gate) is load-bearing for IP. **Do not move features across that line without Hans + Peter Lemire.**
- **`OPERATOR_PATENT_DISCLOSURE.md` (in Operator repo)** — pre-filing legal doc. Bio verified correct as of 2026-05-20 at line 204 (*"U.S. Army retired First Sergeant (Colorado Army National Guard). 21 years total: 5 USMC active 1996–2001 + 16 ARNG"*). Do **not** unilaterally edit; any future bio or claim change goes through Hans + IP attorney.
- **The Refusal list** — canonical lives in `THE_BUILDERS_DOCTRINE.md II.8`. Per-product audit logs are downstream (`REFUSAL_AUDIT.md`). Don't fork.

## Recent significant changes

- **`5480322` Wk 05-15 bandwidth actuals + capacity re-cut 29 → 15 hr/wk — §5#1 + §4c.3 fired, ratified existing Plan A; statistician delegation by 2026-06-22 now mandatory; next-gate re-cut 2026-05-28 (2026-05-21)**
- **Entries 2026-05-15 → 2026-05-20 — see `git log --since=2026-05-15`; major items: founder-romance detector v0.1 SHIPPED (`81dfbd7`), Phase 1 + Phase 2 deliverables all shipped early (`4d24319`, `712684a`, `f800b38`, `9ffa65e`, `4fe5afa`, `dd2732b`, `6bd8334`), MCA v3 → v4 → v5 → v5-candidate (`9192ed3`, `69c1d2f`, `db637a3`, `17adecb`, `789e643`), Operator dogfood asymptote N=1 → N=20 + finding, PROMPT_DOCTRINE v1.1 → v1.3, Funkytown Exp 05 → Exp 10. Backfill in next dated-changes pass if needed.**
- **`114630e` Adversarial Review chassis RETRACTED 2026-05-19 — Grok cold-read KILL on pre-reg v1; regex founder-romance detector reverts to primary for 2026-05-25 slot; killed artifact archived at `archived-prose/2026-05-19_adversarial_review_pre_reg_v1_KILLED.md` (2026-05-19)**
- **`ab95bd7` RELEASE_PLAN_v1 — release-cadence reframe; truncate-at-Platoon becomes Plan A; v1.0 ship 2026-06-01 (2026-05-14)**
- **`4f4ba92` LAW_VI_PRE_REG_v1 — founder-drafted pre-registration; pending statistician review (2026-05-14)**
- **`44d6384` Overlay re-cut — Option A executed; deliverables #1, #2, #3 shipped (2026-05-14)**
- **`ccd526b` Bandwidth overlay populated 2026-05-14 — Law VIII deliverable shipped one day early (2026-05-14)**
- **`024f1cd` Adversarial Review chassis spec — staged in `CHASSIS_PROPOSED_EXTENSIONS.md`, replaces regex founder-romance detector at 2026-05-25 slot (2026-05-14)**
- **`2ba4f73` META_DOCTRINE Laws VI-X added; cost-line withdrawal; STARTUP refresh (2026-05-14)**
- **`4ebb65d` MCA proposed extensions — Medical, Signal, NCO Support Channel (unvalidated) (2026-05-14)**
- **`0702961` META_DOCTRINE Law V — soften budget line; ladder cost above Platoon is unmeasured (2026-05-14)**
- **`37fde63` ADP 6-0 civilian translation — close audience-risk gap on Army vocabulary; COCOM-as-destination explicit (2026-05-13 late eve)**
- **`ed1eff7` Retractions + Law V — Echelon Decay Gate seeded post-Grok review; 02b reframe + 03 MVP over-claim retracted (2026-05-13 late eve)**
- **`637f85a` Principle #12 — empirical posture paragraph from Experiment 02b (later retracted into Law V; see `ed1eff7`) (2026-05-13)**
- **`c899218` STORY coda — 2026-05-13 — "4 Star General with a COCOM of agents"; destination framing (2026-05-13)**
- **`9d27fee` STORY.md — 2026-05-13 chapter: The day the doctrine ran on itself (2026-05-13)**
- **`992e1b1` chassis/authority_gradient — eighth portable chassis component (MCA primitive); funkytown Experiment 02 closed ✅ (2026-05-13)**
- **`1755af2` chassis/reflection_gate — seventh portable chassis component (Principle #12) (2026-05-13)**
- **`6c9c3a6` Kit — close Doctrine drift; 88 fields across 8 templates, pr_faq interview lands (2026-05-13)**
- **`82e26ff` MCA — Authority Gradient + Scale-Up Role Taxonomy + Staff Channel; ratify v1.2 (2026-05-13)**
- **`f1ece26` STARTUP.md — refresh to current state (2026-05-13)**
- `3a3bb0d` Mission Command Architecture doctrine + Scheduler primitive spec + example task (2026-05-12)
- `ad0d125` Adopt Amazon LP cross-map + Working Backwards methodology; add Principle #13 Long Horizon (2026-05-12)
- `876f452` Add Principle #12 *What else? Active extraction* (2026-05-06)
- `07da6b8` STARTUP.md: scope memory pointers to portfolio-meta dir, not Custer-scoped (2026-05-06)
- `828ab0a` STARTUP.md + STORY chapter — Assayer brand lock, thesis outreach sent, reliability principle named (2026-05-06)
- `bfc3b6e` STORY.md origin chapter (2026-05-01)
- `21723c2` chassis: relative imports + lazy kit.coverage import in crisis_floor (2026-05-01)
- `ecc3c89` chassis/parity_top — integration tests vs. TOP's actual production data (2026-05-01)
- `7f87086` chassis/prompt_guardian — sixth and final Phase 2 component (2026-05-01)
- `b9bd07d` kit Phase 1 scoring engine + interview runner (2026-05-01)

## Pointer index

**Doctrine artifacts (this repo):**
- `RELEASE_PLAN_v1.md` — **operational plan for v1.0 ship (2026-06-01), v1.5 ship (2026-07-25), v2.0 provisional (Q4 2026).** Supersedes the post-Grok 12-deliverable schedule. Read this before proposing any deliverable re-cut.
- `BANDWIDTH_OVERLAY_2026-05-15.md` — weekly hours ledger + tripwires + truncation triggers. §1, §4, §5, §6, §7 are the operative weekly ledger; §2 + §3 superseded by RELEASE_PLAN_v1. First Thursday check 2026-05-21 EOD.
- `LAW_VI_PRE_REG_v1.md` — founder-drafted pre-registration for the biographical-moat replication study; statistician sign-off lands v2 by 2026-07-01; blocks v1.5 ship, not v1.0.
- `THE_BUILDERS_DOCTRINE.md` — the methodology prose, v1.2 (13 principles)
- `META_DOCTRINE.md` — methodological laws governing the doctrine itself (Laws I-IV implicit; **Laws V–X** seeded 2026-05-13 late eve post-Grok review, ratified 2026-05-14)
- `MISSION_COMMAND_ARCHITECTURE.md` — portfolio-wide agentic architecture (2026-05-12); civilian readers should hit `ADP_6_0_TRANSLATION.md` first
- `TRAINING_ARCHITECTURE.md` — **training/certification layer** (2026-06-05); ADP 7-0 ported as the pre-runtime certification companion to MCA (METL / T-C-S / crawl-walk-run / certify-to-standard / AAR). Names a discipline already live in production; the unification carries no separate empirical claim. Funkytown is the certification-harness candidate (T/C/S-as-eval = open experiment). Commits `afc8ea6` + `55a7d4b`
- `ADP_6_0_TRANSLATION.md` — civilian glossary for the Army vocabulary in MCA + doctrine (2026-05-13 late eve; v0.3 2026-06-05); spans all three ported layers — **philosophy** (ADP 6-0), **execution** (FM 6-0), **analysis** (ADP 2-0 / IPB)
- `FM_6_0_CROSSMAP.md` — **execution-layer** cross-map (2026-06-05); names FM 6-0 as the source of MCA's staff/protocol layer (OPORD/SITREP/COP/MDMP/AAR + the Staff Channel). Wired-vs-named-vs-absent inventory, Law VII disposition per row. Ships no new claim; gaps stay Law V/Law X gated. RDSP + rehearsals are the only genuinely-absent items
- `IPB_CROSSMAP.md` — **analysis-layer** cross-map (2026-06-05); names ADP 2-0 / IPB as the source of the intelligence grammar. Honest finding: the epistemic discipline (K/I/G, calibrated confidence, RFI gap-loop) is present and is the doctrine's spine; the IPB *method* (four-step drill, threat templates, MLCOA/MDCOA, NAI/TAI, collection plan) is the gap. Drake = IPB Step 3 with a callsign; the founder-romance/strategic-layer detectors = IPB turned inward. Ships no new claim; Law X gates any build to the 6/22 packet; **Law VI keeps it documentation, not moat evidence** (highest moat-romance-risk artifact in the repo)
- `MCA_PROPOSED_EXTENSIONS.md` — **PROPOSED / UNVALIDATED.** Doctrinal sketches for Medical channel, Signal channel, NCO Support Channel clarification (2026-05-13 late eve). Law V applies recursively; no extension migrates to MCA without a passing Funkytown experiment
- `CHASSIS_PROPOSED_EXTENSIONS.md` — staging area for chassis-primitive proposals. §1 Adversarial Review **RETRACTED 2026-05-19** by Grok cold-read KILL on the pre-registration plan; preserved verbatim under §1 banner as falsification evidence per Law VII. First section to reach terminal state. The regex founder-romance detector ships for the 2026-05-25 slot instead. The file's "staging area, not backlog" discipline is now empirically validated
- `SCHEDULER_SPEC_DRAFT.md` — primitive spec paired with MCA
- `WORKING_BACKWARDS.md` — Amazon PR/FAQ-first scoping methodology (adopted 2026-05-12)
- `AMAZON_LP_CROSSMAP.md` — Amazon Leadership Principles cross-map
- `PRINCIPLE_13_DRAFT.md` — scratchpad for Long Horizon (folded into main doctrine)
- `THE_BUILDERS_METHOD.md` — builder-facing method
- `PROMPT_DOCTRINE.md` — universal prompt structural rules (canonical upstream)
- `EXPLAINER.md` — public-facing explainer draft
- `WIRING_DIAGRAM.md` — how the chassis wires into a product
- `STRESS_TEST_v1.0.md` — propagation test results
- `ARTIFACT_AUDIT_2026-05-01.md` — audit at v1.0 lock
- `STORY.md` — founder narrative; tail before any new chapter

**Memory files (load on demand)** — all live in the portfolio-meta scope at `/Users/hansprahl/.claude/projects/-Users-hansprahl-Projects/memory/`:
- `reference_builders_doctrine_canonical.md` — canonical location, layer position, v1.0 contents
- `project_assayer_brand_lock.md` — public-release brand lock 2026-05-05
- `project_agentic_tuner_hypothesis.md` — parent hypothesis; Assayer is the locked name
- `reference_doctrine_naming.md` — three scales (brand / methodology / artifact / session)
- `feedback_doctrine_naming_convention.md` — never bare DOCTRINE.md
- `project_operator_chassis_wiring_branch.md` — `chassis/wire-approval-queue` soak status (re-verify)
- `project_thesis_outreach_sent_2026-05-05.md` — first external validation event
- `quote_brad_hampton_biographical_moat.md` — Brad's biographical-moat endorsement 2026-05-06
- `project_brad_smb_trd_brd_niche_2026-05-12.md` — Brad call 2026-05-12; SMB TRD/BRD market gap; channel-not-customer
- `quote_operator_elevator_pitch_v1_2026-05-12.md` — first customer-facing pitch
- `founding_principle_full_portfolio_pipeline_2026-05-11.md` — full portfolio pipeline + Mission Command scaling falsification ladder
- `quote_reliability.md` — four-lens reliability standard (audit/scale/promise/founder)
- `project_drake_premortem_2026-05-06.md` — scale-grade failure inventory
- `project_observability_spec_v0_1.md` — six emission categories, scale-grade gate
- `project_intake_pipeline_tier1.md` — self-serve inbox shipped in Operator 2026-05-06
- `project_guardian_structural_scoring_layer.md` — Guardian structural scoring Borg-ported to TOP/Custer 2026-05-09
- `feedback_session_as_reliability_checkpoint.md` — session-discipline principle
- `feedback_stoic_register_held_under_pull_2026-05-11.md` — voice discipline under pressure
- `feedback_grok_second_opinion_workflow.md` — Grok as second-opinion check before locking high-level decisions
- `feedback_audit_measurement_before_law.md` — Funkytown Stage 9 near-miss; audit metric code before doctrine
- `quote_biographical_reflection_substrate.md` — the moat is biographical, not technical
- `project_competitive_landscape.md` — read before any external Kit pitch
- `project_plugineval_competitor.md` — wshobson/agents PluginEval, direct Assayer competitor

**Cross-repo pointers (where the doctrine lives downstream):**
- `~/Projects/local-mcp/` — TOP (chassis parity baseline)
- `~/Projects/operator/` — Operator (first chassis wiring; patent-pending closed loop)
- `~/Projects/custer-mcp/` — Custer (Guardian recommendations engine origin)
- `~/Projects/RPR/` — RPR (first Agentic Tuner demo; score-only Borg port)
