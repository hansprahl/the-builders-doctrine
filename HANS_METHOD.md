# The HANS Method

**Hold. Admit. Notice. Sweep.**

> **Status: HYPOTHESIS-GRADE, not ratified doctrine.** Named 2026-08-10. The underlying
> frame has survived one real falsification test against three years of portfolio data and
> one prior-art sweep that took a piece of it away. It has not been murder-boarded, and the
> claim that closing the cells produces better outcomes than spending the same effort
> elsewhere is **unmeasured**. Law VII execution dates attach at ratification, not here.
> Prior work: `[[hypothesis-sovereignty-four-cells-2026-08-10]]`,
> `[[ach-sovereignty-four-cells-2026-08-10]]`.

---

## In plain English

You are not in control of a system because it runs on your hardware. You are in control of
it when you know four things: what it actually knows, what it's missing, what it's holding
but never brings up, and what nobody has thought to ask it. Each of those needs a different
kind of work, and doing one does not cover the others.

The dangerous two are the first and the third — because in both, the system tells you it's
fine. A guardrail you believe is wired reports protected. A model that never retrieves the
right file still answers fluently. **The report is the failure.** Not an absence — an
assertion sitting in the slot the truth would have occupied.

---

## The four moves

The letters are the method, and the method is a loop. Each move addresses one cell of the
known/unknown matrix, and each requires machinery the others cannot supply.

> ### ⚠ RETRACTED 2026-08-10 — the Hold cell's mechanism claim
>
> **"Reading confirms the lie; only provocation is verification" is
> DISCONFIRMED and withdrawn.** Retracted by the pre-committed decision rule of
> the first live test, six hours after this file was written.
>
> Thirteen guardrails Operator's own documents claim are active, two blind arms.
> An independent reader with no session context found **every failure the
> planted violations found, plus one they missed** — an SMS channel that sends
> model-written replies with no approval queue. **Disagreements where reading
> said sound and provocation said dead: zero.** The frozen rule assigned that
> outcome to "the Hold premise is dead" before any data existed.
>
> *(Severity correction, same day: that SMS finding was first written up as
> "replies to strangers." False — an allowlist of three gates it. The verdict
> held; the severity did not. It was the fifth instrument error of the exercise
> and the only one published before being caught.)*
>
> Full pathology: `operator/eval/guardrail_verification/RESULT_2026-08-10.md`.
> Chart frozen at `979855f`; provoke arm locked at `2fc78e3` before the reader
> was seen.
>
> **What survives.** The *cell* stands — false known-knowns are real and 4 of 13
> claimed controls were not in force. What died is the claim that provocation is
> the privileged instrument for finding them.
>
> **The differential, run the same night, names the broken link precisely.** The
> chain was: docs make claims → doc-reading cannot detect falsity → **code-reading
> cannot either** → therefore only provocation works. **Link three is what broke.**
> The cell's real foil was reading the *documentation*, which fails badly and
> decisively — a doc-reader would have scored at least 4 of 13 wrong. That got
> generalized to *reading*, and instructed code-reading went untested until it
> wasn't: it caught **3 of 4 dead controls outright** and **never once called a
> dead control healthy.** Naive code-reading is still untested — the cell may yet
> be right about a reader who skims for a definition rather than a call site.
>
> **Candidate replacement, sharpened by the differential, needing its own chart:
> reading DETECTS, provoking REFUTES — a pipeline, not a contest.** Provocation
> found nothing reading missed, but it killed the reader's one false positive.
> The two arms did different jobs. **This is a new hypothesis and does not get to
> rescue the dead one** — it earns doctrine only with a frozen chart and its own
> successor named in advance.
>
> Full pathology and fix routing: the DIFFERENTIAL section of
> `operator/eval/guardrail_verification/RESULT_2026-08-10.md`.
>
> Recorded honestly rather than quietly amended: the prover was also sloppy —
> four instrument errors, one of which decided the result. A better prover might
> have tied. That is a limitation, not a defense.

| | cell | what it is | how it fails | **the move** |
|---|---|---|---|---|
| **H** | Known Known | what you know you know | the **false** known-known — the guardrail you believe is wired | **HOLD.** ~~Provocation. Reading the code confirms the lie.~~ **Mechanism claim retracted — see above.** Verification of some adversarial kind is still required; which kind is now an open question. |
| **A** | Known Unknown | the named gap | gaps go unowned and rot back into unknown-unknown | **ADMIT.** Tasking. Method, owner, done-when. A gap without an owner is a wish. |
| **N** | Unknown Known | held but never surfaced | present in the corpus, not retrieved at the moment of decision | **NOTICE.** Selection at the point of decision. Put it where the decision happens; choose what governs rather than dumping everything in. |
| **S** | Unknown Unknown | not enumerable | invisible by construction | **SWEEP.** External provocation. An adversary who is not you, and a record of what got killed. |

**The loop:** Sweep converts unknown-unknown into a named gap. Admit converts a named gap
into tasked collection. Collection converts it into something you Hold. And Hold decays back
into a false known-known the moment nobody re-provokes it. **There is no terminal state** —
which is why the method is four verbs and not a four-square chart. A map produced once is a
document. What survives is continuous mechanical maintenance.

---

## Operationalization — lightbulb chew pipeline (2026-08-11)

**Hans named the agent-recon / finding pipeline as this method in action** (Funkytown Exp 26
session; Grok Bot access blocked → Claude Cowork recon → UU hunt → Heuer-gated promotion).

Same four cells; concrete verbs on the lightbulb surface:

| HANS cell | Lightbulb state / move | Machinery |
|-----------|------------------------|-----------|
| **S Sweep** | Collect **UU** hypothesis | lightbulb recon, `uu_loop`, external product probes, cold-read |
| **A Admit** | Land **KU** — named gap + owner + done-when; **dwell** | `KU_QUEUE.md`, implement/test owed; *chew before FACT* |
| **A+ clean** | **Clean the register before you chew the batch** | EMBA analyst process (copy first, drop noise, protect list, manifest) — see below |
| **H Hold** | After chew → **KK** + TRUST line → Hans / COS-GREEN | what-else, murder board, live test, `kk_cards/`; ratify/ingest; COS Hold GREEN only |
| **N Notice** | Mine / connect latent patterns at decision time | collection mine (next), memory-rag over ingested KKs |

**Triggerable chew loop (Hans):** UU hypothesis → what-else → murder board → implement/re-probe
→ autopsy (if charted) → findings → **KK for Hans to decide**, with agent **confidence he can
trust** (earned from that stack, not a skim).

**Epistemology (Hans, same session):** *You can read something new, but to understand it you
have to chew on it and connect it with other things to make sure it is FACT and TRUTH. You
don't take someone's word for it — even your own.* That is Admit dwell + Hold verification,
not a skip from Sweep to "I ratified a list."

**Heuer alignment:** ACH / anti-satisficing / diagnosticity / confidence caps live in
`promote.py --ku-to-kk` gates. Source text: home-ai corpus
`Psychology_of_Intelligence_Analysis.md`.

**Artifacts:** `~/.claude/skills/lightbulb/`, funkytown
`experiments/26_claude_cowork_recon/` (SYNTHESIS, KU_QUEUE, kk_cards, loop/).

**Status of this section:** descriptive map of a working pipeline onto HANS cells. It does
**not** by itself ratify the whole HANS Method hypothesis above. The Hold-mechanism
retraction (2026-08-10) still stands.

**First full Hold cycle completed (2026-08-11):** LB-015 path-jail — Sweep/Admit/chew →
live demo → KK conf 0.92 → Hans ratify → permanent rule `PATH_JAIL_RULE.md` +
`~/.claude/tools/path_jail.py`. Template for future HANS Hold promotions.

**Trust line on Hold cards (2026-08-11):** `TRUST: GREEN|AMBER|RED` is the product;
score supports it. See funkytown `experiments/26_claude_cowork_recon/TRUST_LINE.md`.

**COS Green Hold tested (Exp 28):** Hege desk auto-Hold GREEN only; issues escalate via
**Operator SMS** (Hege does not SMS). Working Hold only — not permanent doctrine marriage.

**Loop test PASS (2026-08-11 evening):** Arm A silence + Arm B interrupt + collection pull
on cleaned set → 5 HOLD, 0 RAISE, Operator dry-drain empty. Real `--send` still Hans-gated.

### Data clean is part of the method (Hans 2026-08-11)

> *we are cleaning our data right… we have a process for this* — EMBA (Beaver XMBA 4364),
> lived in Operator (yahoo-archive / WMT clean 2026-06-30).

**Not optional hygiene theater.** A dirty UU/KU register is a false known-known factory:
noise gets chewed as if it were a real gap. Cleaning is **Admit-adjacent instrument work** —
prepare the ledger before the chew loop and before COS pull.

| Step | Rule (every time you get data) |
|------|--------------------------------|
| 1 | **Copy first** — archive sheet / `collection_pre_clean_*.jsonl` |
| 2 | Drop useless (template, parse-noise ids) |
| 3 | Protect list (INGESTED / RATIFIED / GREEN never dropped) |
| 4 | Ambiguous real KUs **kept** (dwell, not invent COMPLETE) |
| 5 | Manifest: kept/dropped + policy (`_manifest/clean_stats.json`) |

Code: funkytown `experiments/26_claude_cowork_recon/clean_collection.py`  
Pattern twin: `~/Projects/yahoo-archive/README.md` + `_manifest/clean_stats.json`

```
Sweep UU → [CLEAN register] → Admit KU dwell → chew → live test → TRUST
  → GREEN: Hege working Hold (silence)
  → AMBER/RED: raise → Operator SMS (Hans; --send is one-way)
  → Hans replies: re-chew | reject | hold
  → hold = HANS Hold cell (write verified KK memory)
  → permanent doctrine / prod bolt-on still needs ratify path
```

### Commander SMS replies (final, 2026-08-11)

| Verb | HANS cell / meaning |
|------|---------------------|
| **re-chew** | Stay in Admit dwell — more work, no memory written |
| **reject** | Kill the claim — closed, no Hold |
| **hold** | **Hold** — write verified KK into working memory |

Not override (bypass). Not remember (passive recall). Not memorize (thesaurus).  
**Hold** is the method’s own verb for making the known-known memory.

Operator: `tools/hege_exception_sms.py` + commander verbs in `sms_commander.py`.  
Hege raises; Operator SMS; Hans decides. Channel split is load-bearing.

### Hold is not fact until measured (Hans 2026-08-11)

> *Before we go all the way… test what we claim as Held. Does it improve
> process? Is it truth and fact? By what degree? Measure, measure, measure.*

| Layer | What it is |
|-------|------------|
| Method score / TRUST GREEN | Process package complete — not calibrated truth odds |
| Working Hold | Candidate known known after line |
| **MEASURED_PASS** | Live demo re-test passed — claim still holds under its control |
| Process improvement | **Control chart:** with hard mechanism vs soft control on fixed bank |

Battery: funkytown `experiments/28_cos_green_hold/hold_verify.py`  
Process chart: `process_improvement_ablation.py`  
Pre-reg: `PREREG_HOLD_MEASUREMENT.md` + `PREREG_PROCESS_IMPROVEMENT.md`  

**First process chart (2026-08-12):** 4/4 rules IMPROVES_PROCESS on bank  
(path jail, no invent, secret channel, continuity disk). Soft arm fails; hard arm clean.  
Does **not** prove prompt-only LLM compliance.

### Bottom-up staff push (Hans 2026-08-11)

> *I shouldn't have to sit in front of the computer all day and find new things.
> Hege/Operator… the stack does all of that and pushes me data like a staff would.
> Not top-down. Bottom-up.*

| Layer | Does |
|-------|------|
| Bottom | Sweep, clean, chew, score, Hold GREEN in silence |
| Push | AMBER/RED flags to phone (SO WHAT + COAs + Q&A) |
| Top | Hans: COA only, permanent ratify, prod bolt-on |

Scheduled: `com.operator.cos-lightbulb-pull` runs the bottom and the push.  
Hans does not have to open a laptop to learn there is a decision.

---

## Do not marry the method (standing order — Hans 2026-08-11)

> *I'm in love with this HANS Doctrine… you have to make sure I don't marry it.*

Love is allowed. **Marriage is forbidden.** Marriage means the method becomes identity,
unfalsifiable, or the default answer to every problem. An instrument you cannot kill is
already a false known-known in the Hold cell.

### What marriage looks like (observable)

| Sign | What it sounds like | Intervention |
|------|---------------------|--------------|
| Identity merge | "I am a HANS Method person" / branding before evidence | Interrupt; restate **hypothesis-grade** |
| Universal hammer | Running chew/trust line on a problem that needs a knife, a nap, or a no | Ask: *is this the wrong tool?* |
| Sacred cow | Blocking a kill or simplification because "it violates HANS" | Prefer kill evidence over loyalty |
| Ritual over result | Full UU→KU→KK theater when a 10-minute live test would decide | Collapse to the cheapest falsifier |
| Score worship | "0.92 so we ship" without the trust line | Point at TRUST line, not the decimal |
| Autopilot COS | Hege Holds AMBER/RED or bolts prod because "the method said" | Hard stop; one-way doors stay Hans |
| Unfalsifiable frame | No kill criteria, no review date, no successor named | Refuse to treat as settled |

### What love looks like (allowed)

- Using the four cells when the failure mode matches
- Chewing before calling something FACT
- Preferring a line that cannot lie over a flattering score
- Naming residual and residual *limits*
- Killing a piece of HANS when a frozen test kills it (already done once: Hold mechanism 2026-08-10)

### Hard floors for agents

1. **Status on every serious use:** this file is still **HYPOTHESIS-GRADE** until murder-boarded and outcome-measured. Do not speak as if it were Law.
2. **Dependency test applies to HANS itself:** if the method makes Hans *less* able to decide without the ritual, the method is failing. Designed to be needed less, not more.
3. **Named kill criteria (any one is enough to demote):**
   - A cheaper instrument (read code, one sealed test, one honest no) beats full HANS stack on the same decision class three times running
   - Marriage signs appear and Hans does not correct when interrupted
   - Method is used to *avoid* a one-way-door judgment he owes
   - External murder board kills non-substitutability or sovereignty claim without a pre-named successor
4. **Agent duty when marriage signs fire:** say so in the first line. Do not flatter. Offer the smaller move. Prefer delete over elaborate HANS ceremony.
5. **Review-by:** 2026-11-11 — re-read this section cold; if no marriage signs and no kill criteria met, keep hypothesis-grade; if signs met, demote language in products to "optional checklist."
6. **Surname is not a wedding:** naming it HANS does not make it permanent. The first Hold mechanism already died under its own rule. Keep that as the model.

### One sentence

**Use it. Do not become it. Kill the part that fails.**

Canonical short form: `DONT_MARRY_HANS_METHOD.md`.

---

## Why H and N are the hard ones

In **Admit** and **Sweep** you already know you are ignorant. You are suspicious by default,
so the instruments get built and used.

In **Hold** and **Notice** the system reports that it is fine. Those are the two cells that
go bad silently, and they are where the failures actually land.

---

## Non-substitutability — the load-bearing claim

**Applying one cell's mechanism to another cell's failure does nothing.** This is the part
of the method that is a claim rather than a vocabulary.

You can plant violations all day — a Hold-class fix — and it will never make a retrieval
system surface the right pin at the right moment. Direct measured evidence: on the same
corpus, retrieving the **full** profile scored **under 75%** accuracy while retrieving
**only the relevant pins** scored **over 99%**. More correct information, worse ruling. That
is a Notice failure, and no amount of Hold work touches it.

If a Hold-class fix is ever shown to repair a Notice-class failure, the cells are not
separable and this claim collapses.

---

## The measured record

Everything below is Hans Prahl's own portfolio data. It is the part of this method that
belongs to nobody else.

**Failure clustering — the falsification test that ran.** Corpus defined by an existing
field rather than chosen: all **121** memories tagged `type: feedback`, classification rule
written before looking. Pre-stated falsifier: *if failures scatter evenly across cells, the
frame is decoration.*

| cell | failure count | |
|---|---|---|
| **H** — Known Known | **~19** | hook installed but inert · quality gates dark, one call in 24 days · guard keyed on a name so siblings are exempt · a tool named *reply* that sends · metric not counting what it is named for |
| **N** — Unknown Known | **~5** | a solved problem rediscovered over four rounds · recon-before-scoping cuts estimates 50–90% and gets skipped |
| **S** — Unknown Unknown | **~2** | an author's own coding habits sanitize the author's own tests |
| **A** — Known Unknown | **0** | none recorded |

**N replication — +6 in one session, 2026-08-13 evening.** Independent of the corpus
above (that run classified `type: feedback` memories; these are live findings from a
single build session, collected before the frame was consulted). Full table and
citations: `home-ai/dogfood/AAR_2026-08-13_evening_voice_and_brain.md`.

1. A second-seat chain had already run at 02:07 that morning; the examiner argued for
   hours it had never been demonstrated.
2. `serve._VOCAL_NOISE` had blocked inbound sniff/cough/pffft since 2026-08-03; Hans
   asked for the capability it already had.
3. The unified `MEMORY.md` states *"the per-project memory dirs are symlinks to this
   dir"*; home-ai sat out of compliance while sessions hand-copied around it.
4. `test_tts_plain.py:147` already asserted `"Saint Louis"`; the examiner reasoned
   about the corpus instead and was corrected by the gate going red.
5. **No-self-grading rule 5 (positive control) was ratified 2026-08-11 and not applied
   2026-08-13** — a published verdict rested on a test that could not move.
6. **The N cell itself** — the examiner told Hans there was no Unknown-Known cell,
   while `HANS_METHOD.md` sat in the auto-loading `MEMORY.md` active threads.

**The sharpest instance is #5 paired with #6, and it points at a delivery defect
rather than a doctrine gap.** Two constraints ratified within 48 hours — positive
control and DIRECT TO SOURCE — were written, filed, and indexed, and **neither fired
at the decision point.** N is not a knowledge problem. It is a *selection* problem,
which is why the move is NOTICE and not COLLECT. Contributing factor now measured:
`~/.claude/memory-rag/index.py:50` embeds `[:1500]` head-only, leaving **65.2% of the
corpus structurally unretrievable** and biased against the newest material because
close-ups append — an N generator running continuously
([[project-hege-memory-recall-measurement-2026-08-11]]).

**~23 of 28 failure-derived memories land in the two cells the method predicts fail
silently.** They did not scatter. The clustering holds across memories written long before
the frame existed.

**Who finds unknown-unknowns.** All 64 kill headstones in the graveyard, classified by the
objective `Killer:` field:

| count | instrument |
|---|---|
| 27 | cross-family cold read |
| 20 | Hans himself |
| 8 | murder board / panel |
| **1** | **the AI inside the system** |

**One in sixty-four.** The component holding all the context, with every file readable,
produced essentially none of its own unknown-unknowns. That is a quantified instance of the
method's own claim, with a denominator.

**Corpus bias, named rather than buried.** Zero in Admit may mean a strong cell or an
unrecorded one — "we knew and didn't do it" teaches nothing new, so it may never get written
down. Sweep is under-counted in the feedback corpus because its conversions get filed as
kills instead; the 64 headstones are where they went.

---

## The inversion — whose knowledge is actually broken

Read the Hold column again: hook inert, gates dark, code ships unused, doctrine mistaken for
capability, subagents over-claiming.

**Almost every one is a false belief held by the operator about the system — not by the
system about the world.** Only the Notice column is squarely about the system's own
knowledge.

This is the most useful thing the analysis produced, and it reframes the whole method. The
epistemic ledger is not primarily an instrument you point at your AI. It is one you point at
your own model of your AI.

---

## The Sweep problem, and why it is a sovereignty argument

**Sweep structurally cannot be run locally.** The data says so: the component inside the
system finds 1 in 64. An unknown-unknown requires a mind that is not yours, and in practice
that means a model from a different lineage — a different company, a different training
corpus, a different set of blind spots.

Hold, Admit, and Notice can all be closed on your own hardware. Sweep cannot.

The naive reading is that this defeats sovereignty. It does not. **The sovereign move is not
to avoid the outside mind — it is to gate exactly what crosses.** The standing rule already
in force: build-level input only — hypotheses, code, architecture, decisions. Never the
private corpus, never the personal data.

So Sweep **breaches locality without breaching sovereignty**, because what crosses the
boundary is a deliberate, bounded choice. That is a stronger and more defensible position
than local-purism, which cannot explain how it would ever find what it isn't looking for.

**The four cells have different sovereignty postures, not merely different mechanisms.**

---

## Prior art — what is taken, stated plainly

A deep-research sweep on 2026-08-10 took real pieces of this away. They are recorded here
rather than quietly dropped.

**TAKEN — do not claim these.**
- **The four-cell known/unknown matrix applied to AI systems.** CogniSwitch, *"The Matrix of
  Knowns: Understanding Knowledge Debt."* Commercialized, not merely published.
- **"Confident failure is the dangerous mode."** Also CogniSwitch, explicitly. An earlier
  in-house claim that this diagnosis was original was **wrong and is retracted.**
- **Unknown-knowns as a named category needing extraction.** Theirs is organizational tribal
  knowledge; the Notice move here is retrieval-at-decision-time. Related, not identical.
- **"Formal control is not real control."** Cruzes, *AI Infrastructure Sovereignty*
  (arXiv:2602.10900) makes the same structural move first — but its epistemic object is
  compute, power and cooling telemetry, never the model's own knowledge.
- **The knowing-doing gap.** Named in a paper title (arXiv:2605.14038) and by DeepMind
  thirteen months earlier.

**NOT FOUND IN THIS SWEEP — and the sweep did not cover everything.**
1. The connection between four-cell epistemic accounting and AI **sovereignty**.
2. **Non-substitutability** — that each cell needs a different mechanism.
3. The **operator-versus-system** inversion.
4. The **Sweep-requires-an-outsider** tension and its resolution by gating.
5. The **measured evidence** — 28 classified failure records, 64 headstones with instrument
   attribution, a 1-in-64 self-catch rate.

**Three of five claim areas were never actually searched** — a verifier exhausted its search
budget and the harness returned NOT FOUND anyway. Under the two-man rule the only defensible
phrasing is *"not found in this sweep, which did not cover assurance cases, ISO 26262 /
DO-178C verification-and-validation, chaos engineering, detection-as-code, or the
automation-bias literature."* Prior expectation, stated so it is not mistaken for a result:
two of those three are very likely already taken.

> The instrument sent to sweep for false known-knowns produced confident NOT FOUND verdicts
> for three things it never looked for. The pathology reproduced itself inside its own audit.

**Honest position: known frame, unclaimed application, original evidence.**

---

## THE LOAD-BEARING GAP — is any of this portable? Named 2026-08-10, untested.

**In plain English: Hans may have built something only he can use, and has never checked.**

Two lines in this doctrine pull against each other, and the tension has never been examined.
*Sovereignty requires an epistemic ledger.* And *the method is portable to any builder; the
moat belongs to whoever's biography is doing the building.*

**Three possible states. Nobody can currently tell which one is true.**

| | state | what it makes this |
|---|---|---|
| **A** | portable and cheap — someone reads the page, runs a cell, finds something real | a genuine contribution; the market is everyone with a system they cannot verify |
| **B** | portable but expensive — needs a graveyard, a panel, multiple vendor subscriptions for the Sweep cell, and pre-registration discipline | a consulting practice, not a movement. Viable, but a different business than this artifact implies |
| **C** | not portable — it works because of twenty-one years of collection instinct, 800 hours of machinery, and a temperament that pre-registers predictions it expects to lose | true and useless to anyone else |

**2026-08-10 made C more plausible, not less.** With the doctrine repo, the graveyard, the
ledger, and the discipline all in place, the first guardrail pilot found **four of the
author's own thirteen claimed controls dead.** Not from sloppiness — from the ordinary
silent decay this method exists to catch. If the person who invented it, holding the most
machinery, runs a 31% failure rate on his own cells, *"build an epistemic ledger"* is not
advice a normal person can act on.

**This outranks the prior-art question.** Prior art decides whether the idea can be
*claimed*. Portability decides whether it is *worth anything to anyone but its author*. A
99-agent sweep went to the first; zero minutes have gone to the second.

### The decomposition that makes it testable

The method has two halves that have been treated as one:

- **Building the frame** — deciding what the cells are, what counts as a control, what the
  decision rule is. Where the 800 hours went. Almost certainly not portable.
- **Running the frame** — taking a defined list and verifying it. Mechanical.

**Evidence already in hand on the second half, and it is encouraging.** In the 2026-08-10
pilot an agent with **zero context, zero hours, and no biography** was handed a frame and
one instruction — *do not trust the docstrings, find the enforcing call site* — and
**outperformed the person who built the system.** Running a cell may be far cheaper than
800 hours implies. What that does **not** test is whether anyone can *construct* a frame:
the reader was handed a list Hans built and a rule Claude wrote.

### The cheap test

One person who is not Hans, with a real system they cannot verify. Hand them the artifact
and nothing else — no coaching, no author in the room. Have them run **Hold**: list what
the system claims to protect, plant a violation for each, record what fired.

Measure four things: did they finish · how long · did they find anything real · and did they
do it correctly, or make the prover's mistake of grepping for a name, finding nothing, and
declaring a surface nonexistent.

**One person, one afternoon, and it discriminates A from B from C directly.**

## Positioning — open weights are necessary and not sufficient

**2026-08-10, and the exhibit is lived rather than argued.** Meta published *"The Future Is
for Everyone"* — Muse Glimmer released under a permissive open license, Muse Spark 1.2 for
developers, a $1B fund, and a policy push against concentration of AI power.

The same day, on the same machine, Hans **downloaded those open weights within hours and
could not run them.** 19.7 GiB required against a 17.3 GiB Metal ceiling. And when the
hardware does arrive, the other wall is already measured: local models produced 21–24
confabulations on a frozen 49-question bank, raw.

**A model you own, on hardware you own, under a license nobody can revoke, that still makes
things up.** Openness was never the constraint.

Three things this clarifies, and the first is the commercially useful one:

1. **Open weights externalize verification onto the user.** Closed providers absorb that
   cost centrally. Open the weights and the responsibility goes to people with no eval
   infrastructure. **Every open-weight deployment is a system whose owner cannot verify
   it** — which enlarges the problem this method addresses rather than solving it.
2. **Distributing weights does not distribute judgment.** The manifesto argues against
   concentration of *power*. It does not address concentration of *error*: a model that
   confabulates, copied ten million times, is a confident liar with ten million owners who
   cannot tell.
3. **Open weights are only liberating for those who can verify.** For everyone else it is a
   downgrade — a vendor's imperfect guardrails traded for none, and the difference is
   imperceptible, because a confabulating model feels exactly like a working one.

**Sovereignty without verification is unsupervised failure with better branding.** Position
public work here — not against open weights, which are good, but on the layer they leave
open. Note the clock: as "AI sovereignty" becomes a marketing term for open weights, the
more precise meaning gets harder to claim, not easier.

## What this method does NOT claim

- **Not that four cells are exhaustive.** Four is inherited and convenient. No argument has
  been offered that it is complete.
- **Not that closing the cells is sufficient for sovereignty.** Custody and portability are
  the other two legs and are already covered elsewhere in this doctrine. This names the leg
  nobody covers — it does not replace the table.
- **Not that any individual mechanism is novel.** Provocation, tasking, retrieval selection
  and red-teaming are all known under other names. **The novelty claimed is the ledger, not
  the entries.**
- **Not that this beats spending the same effort on money, time, or model capability.** That
  is the live threat to the whole frame and it is unmeasured.

---

## On the name

Eponymous by design. The four moves are not a backronym fitted to the letters afterward —
each is a distinct discipline with a distinct failure mode, and the mnemonic survives being
explained, which is the test most backronyms fail.

The Notice cell exists in this method because of twenty-one years of running collection,
where "we already have that, nobody pulled it" is a recognized failure with a name. Most
engineering cultures have no word for it, and the most famous version of this matrix skips
it entirely. That is the biographical argument doing real work rather than decorating a
slide: **the moat is not the model, it is the memory** — and a method carries the name of
the memory that produced it.

It also puts a name on the liability. If the method is wrong, it is wrong in public with an
owner attached.

---

## How to disprove this and end up with something better

**The rule that turns a kill into an upgrade: pre-register the SUCCESSOR, not just the
falsifier.** Before running a test, write down *"if this dies, the next version says X."*
On 2026-08-10 that was not done — the Hold cell died and its replacement hypothesis was
written twenty minutes later, after the data, which is exactly when rationalization walks
in. Name the successor first and the kill hands you the next version instead of leaving you
improvising in the rubble.

| claim | what kills it | the successor, named in advance |
|---|---|---|
| **Sweep needs an outside LINEAGE** | Give a same-lineage agent a genuinely adversarial task on a real target | **Sovereignty becomes fully local** — the one cell thought to require an outside vendor runs at home |
| **Portability** | One person, one page, one cell, no coaching | contribution → consulting practice → private habit |
| **Non-substitutability** | 2×2 crossover: an H-class and an N-class failure, each fix applied to each | **The method collapses to one sentence: verify adversarially, repeatedly.** Simpler, possibly correct |
| **Operator-vs-system inversion** | Classify failures by whose belief was wrong, on a corpus that is not Hans's | the method points at the AI rather than at its operator — a different product, a different buyer |
| **Binding-ness** | Measured cell-closure against the same effort spent on money, time, or model tier | true but not worth doing — a checklist, not a strategy |

### Order, and it is not the obvious one

**Decomposition before parts.** If non-substitutability is false there are not four steps,
there is one step wearing four hats — and three iterations would have gone into polishing
cells that are not separate things. The crossover is cheap and belongs at step zero.

Then **Sweep-lineage**, because it is cheap, its failure is *good news*, and **it is already
half-disconfirmed by evidence nobody has examined.** The 1-in-64 self-catch rate was
measured under conditions where the inside model was never *tasked* to hunt
unknown-unknowns. In the 2026-08-10 pilot an agent of the **same lineage**, given one
adversarial instruction, found what the prover missed. That is an outside **seat**, not an
outside **lineage** — and if the cell is about role isolation rather than model provenance,
the "sovereignty requires calling an outside vendor" tension dissolves entirely.

Then **portability**, then **non-substitutability**, then the expensive one last.

### The whole-loop test must measure interaction, not repetition

Running the four steps again in sequence is four unit tests in a trench coat. The
integration test earns its name by measuring whether closing one cell degrades another,
and whether the loop converges or oscillates. Its natural form is already requirement 3:
run the method end to end on an untouched domain and show a decision made with the map
beating the same decision without it.

### Two disciplines that keep the loop from becoming a trap

**Delete, do not qualify.** Doctrine's failure mode is accretion — a claim dies, gets hedged
into a footnote, and the page becomes armor. The 2026-08-10 retraction was clean. Keep that.

**At least one pre-registered successor must be the empty set** — *"this frame is wrong, use
something else."* This method self-applies: attacking it with Sweep, tasking the gap with
Admit, retrieving what was already known with Notice, holding what survives. That is a
genuine strength, and it is also exactly how a system becomes unfalsifiable — every attack
gets processed *through* the frame, every counterexample becomes evidence the frame works.
**If every branch terminates in another version of HANS, this is not a falsification
program. It is an immune system for a belief.**

### Phases are for establishing it, not for running it

Decay is concurrent. While Hold is being perfected, Notice is rotting — the Prompt Guardian
ran correctly until 2026-05-15 and then stopped for three months while attention was
elsewhere. Once established, the loop cannot stay phased. It stops being a project and
becomes a heartbeat.

## Before ratification

Four things are owed. Execution dates attach when Hans sets them; until then this artifact
stays hypothesis-grade and Law VII is not yet in force against it.

| # | requirement | why it matters |
|---|---|---|
| **1** | **THE PORTABILITY TEST — one person who is not Hans runs the Hold cell from this page alone.** Reordered to first 2026-08-10. | **The load-bearing assumption.** Decides whether this is a contribution, a consulting practice, or a private habit. One person, one afternoon, and it discriminates all three. Nothing else on this list matters if the answer is C. |
| 2 | **Guardrail inventory with planted violations**, portfolio-wide | Converts the largest cell from belief to fact. **Partially run 2026-08-10** on Operator: 13 controls, 4 dead, and it retracted the Hold cell's mechanism. Never run on any other product. |
| 3 | **One measured cell-closure** in a bounded domain | The only thing that answers "is this binding, or just true?" Show a decision made with the map beating the same decision without. |
| 4 | **Finish the prior-art sweep** for the three unsearched claim areas | Cheap, still outstanding — but **demoted below portability**: prior art decides whether the idea can be claimed, portability decides whether it is worth claiming. |
| **2b** | **EXTERNAL MURDER BOARD — moved up from #5 on 2026-08-10.** Multi-lineage panel, run after portability. | **Reason for the move:** the original deferral was *"a panel grading a frame with no evidence attached grades the prose"* — and the artifact now carries a measured pilot, a same-day retraction rendered by a frozen rule, 64 classified kills, and an honest prior-art section. The evidence bar is met. **The reason to hurry is sunk cost:** a cold read is cheapest when the author is least attached, and this frame already has a day and a surname invested in it. The retraction is the strongest exhibit to hand a panel and it did not exist that morning. |
| 5 | ~~External murder board, last~~ | Superseded by 2b. **Standing indictment while it remains unrun: every attack on this method so far — the ACH, the graveyard classification, the prior-art sweep, the guardrail pilot — was run by an agent of one lineage, from inside. The Sweep cell's own measured claim is that an inside attacker finds 1 unknown-unknown in 64. By its own argument, the frame has barely been tested.** |

**Falsification indicators, pre-committed:** graveyard headstones scattering evenly across
cells · a prior-art hit describing the sovereignty connection · a Hold-class fix repairing a
Notice-class failure · a measured cell-closure showing no decision improvement.
