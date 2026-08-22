# The Collection Pipeline

**UU → KU → KK → RATIFIED → INGESTED.**

> **Status: IN USE on one surface, GENERALIZED 2026-08-12, unvalidated off that surface.**
> The state machine, the multi-source bar and the trust line have run on the agent-recon
> surface since 2026-08-11 with working code and live queues. The claim that the same loop
> serves every surface — engagements, builds, coursework, our own instruments — is one day
> old and has not been tested. Treat the machinery as proven and the generality as a
> hypothesis.
>
> Parent frame: [HANS_METHOD.md](HANS_METHOD.md). This is the operational loop for
> Sweep → Admit → Hold. It is not a second method.

---

## In plain English

You can read something and still not know it. Knowing it takes chewing on it, connecting it
to things you already know, and trying to break it. That applies to what other people tell
you, what a machine tells you, and what you tell yourself.

So nothing goes straight from *noticed* to *true*. It sits in a holding state first, where
the job is to attack it. Only what survives gets called known, and only Hans decides that a
known thing becomes part of how the portfolio operates.

The failure this prevents is specific and it is not laziness. It is reading a confident
list, feeling it click, and promoting it the same afternoon. **A misread list becomes
portfolio truth that way**, and it is nearly impossible to walk back once other decisions
have been built on it.

**Source (Hans, 2026-08-11):** *Just like learning something new — you can read it, but to
understand it you have to chew on it a bit and connect it with other things to make sure it
is FACT and TRUTH. You don't just take someone's word for it… even your own.*

**Source (Hans, 2026-08-11):** *I can make mistakes and not read or understand everything
and still sound 100% correct. That is why it sits in KU for a while so we can implement and
test.*

---

## States

| State | Meaning | Who moves it |
|---|---|---|
| **UU** | We did not know to ask | A probe discovers it, or a human names it |
| **KU** | Named claim or gap, with evidence, **implement/test still owed** | The local loop |
| **KK** | Survived implement/test or sealed re-probe — a *proposed* known known | Build and test evidence, never chat approval alone |
| **RATIFIED** | Hans accepts the KK | **Hans only** |
| **INGESTED** | In memory or doctrine | Agent, after ratification |

```
   intake  →  UU  →  KU  →  KK + TRUST  →  RATIFIED  →  INGESTED
                      │        │
                      │        └── GREEN → hold in silence
                      │            AMBER/RED → raise to Hans
                      └── chew loop: what-else · murder-board · implement · autopsy
```

**Forbidden:** intake → KK → ratify → memory in one afternoon because the list looked good.

**Also forbidden:** one product, one run, one lineage → portfolio change. That is
single-source reporting wearing confidence as a costume.

### Fact is not a known known (stamped 2026-08-18)

Hans, 2026-08-18: do not convert known knowns into facts. Two bowls.

A known unknown is something heard or read. It goes through the chew. Hans says yes
or no. Then it is a belief. That belief is a **KK**. It can still carry judgment. It
is not proven the way two plus two is four.

A **FACT** must be shown. A date in the store. A name the code will not drop. A test
that fails if the line is wrong. No chew required for the truth of it. Weight above
a KK.

- Do not rename the pipeline UU → FACT. Facts sit beside the chew loop, not on it.
- A **KU** that can be shown becomes a FACT. It does not have to become a KK first.
  If it cannot be shown, it stays on the chew loop toward KK.
- An **unknown known** (held in the record, not surfaced) that can be shown becomes
  a FACT. That is Notice with a proof, not a new belief.
- Do not convert a KK into a FACT. Belief does not graduate to proof by renaming.
- Do not call the vault "thousands of known knowns." The ratified KK ledger is
  empty until Hans accepts a KK. The state store is the small fact floor. The rest
  is record.
- A pin is a fact the machine will not drop. Quiet in the mouth. Loud in CODE.
- 2026-08-10 folded "buckets of truth" into KK as MEASURED. This stamp pulls FACT
  back out. Measured-and-shown is a fact. Chewed-and-believed is a KK.

stamped 2026-08-20: a Fact has to be able to be proven, and relevant.

### Enforcement is derived — Pinned/Unpinned (ratified 2026-08-18)

A ratified KK has an enforcement status, and **no hand ever writes it**. Hans named
the axis (UP/KP/PP); a three-lineage murder board (grok/gpt/gemini, Fable excluded)
killed the manual letters 3/3 — a hand-written tag can lie about an automated state —
and Hans stamped the rewrite:

- **Source of truth = test results.** A checkable KK is **Pinned** when a machine
  re-verifies it (a battery case, a heartbeat check, a provoked guard) and the latest
  run contains it; **Unpinned** otherwise. Prose is a read-only client of this truth.
- **The report is the ritual.** `~/.claude/tools/knowledge_census.py` derives the
  Knowledge Enforcement Report (house_check, dated); it is the agenda for the daily
  "turning out the lights" segment. A **behavioral** finding closes by becoming a pin.
- **DESYNC is a first-class state:** a ledger that claims cases no tape contains is
  the predicted lie; each instance resolves by finding the case or striking the claim.
- **Pin-theater guard:** the first time a claim becomes Pinned, a second reviewer
  audits the test for substance ("does it meaningfully fail?"). Instruments that
  measure ship a runnable positive control, run by the gate — the census itself
  calibrates on planted fixtures and exits 2 rather than print an untrusted report.
- **Scope guard:** applies to checkable claims only. Biography and world lines that
  can be shown are **FACTS**, not KKs. Decisions stay KK with review-by dates.

First census (2026-08-18): 51 behavioral classes — 32 pinned / 15 DESYNC / 4 unpinned;
instruments 6 watched / 33 unwatched / 3 dark; ratified-KK ledger empty. The panel
transcript and plan live with the 2026-08-18 session artifacts.

---

## Entry points

The loop was written on the agent-recon surface. Binding it there means every unknown
produced by ordinary work dies in the file that named it.

| Intake | Enters at | Where it queues |
|---|---|---|
| Recon probe or field note | UU | the running experiment's `UU_REGISTER.md` |
| Recon after implement/test | KU | the same experiment's `KU_QUEUE.md` via `promote.py` |
| **Commander-ratified problem STATEMENT** | card | `operator/PROBLEM_CARDS/` (CRs may spawn portfolio KUs) |
| **AAR routing section** | KU | portfolio queue |
| **Decision memo "could not verify"** | KU | portfolio queue |
| **Autopsy residual** | KU | portfolio queue |
| **A session noticing its own blind spot** | KU | portfolio queue |

**The AAR is the main non-recon intake.** Every AAR closes with a routing section that
sorts each finding into a bin — doctrine, feedback memory, task ledger, ideas inbox, or
this queue — and says plainly when a finding has no bin, which is itself a finding.

### The meta-rule: findings about our own instruments are first-class UUs

A discovery about the pipeline, or about any instrument the pipeline depends on, enters
here like anything else. It does not get a private channel because it is about us.

**Source (Hans, 2026-08-12):** *when we discover stuff like this… we need to add it to the
original collection pipeline.*

This is the recursion closing: the loop collects its own defects. It is not decoration —
see the worked example, where the instrument enforcing a doctrine rule was the thing
defeating it, and nothing in the system was positioned to notice.

---

## The multi-source bar

**A single independent source ceilings at KU.** Never KK, never ratified, never a doctrine
or production-wall change from one reporter alone.

**Source (Hans, 2026-08-12):** *We cannot rely on single-source reporting to make decisions
and changes… Single source gives us a KU — we chew it and need at least two more sources we
trust saying the same type of stuff. Not hunting for evidence to support our hypothesis —
rich research that competes hypotheses; we try to disprove the evidence we find. ACH.*

| Independent (counts) | Not independent (does not count) |
|---|---|
| Different product, harness, or wall mechanism | Three summaries of the same transcript |
| Different model family or blind author lineage | Same model, same prompt, N=3 |
| Disk, sealed key, or live state vs a chat claim | An agent saying "done" three ways |
| A separate instrument | The same probe re-run without new design |
| Adversarial half vs control half | You wrote the test, the inputs, and the score |

*Same type of stuff* means the same **claim class** — the same mechanism or decision rule —
not the same wording.

### The floor for leaving KU

One of:

| Path | Requirement |
|---|---|
| **A. Multi-source** | Original source plus **≥2 more independent sources** of the same claim class, after ACH chew |
| **B. Implement/test** | A live implement or test **that can fail**, with the residual named |

Load-bearing walls — send, pay, cage, the trust line, portfolio doctrine — want **A and B**.
Narrow reversible lab claims may use B alone, and must log that multi-source was not met.

### ACH posture, not confirmation hunting

Open with two or three competing hypotheses and collect for each. Prefer evidence that
could kill the favorite. Score external fact over agent assertion. Name the residual
conflict on the card.

**Wrong:** research that logically concludes to our hypothesis.
**Right:** research that forces a choice between hypotheses. The survivor is what gets
promoted.

If every new source only ever supports the prior favorite, you built a confirmation engine
with extra steps. Demote to KU and reopen the rivals.

---

## The chew loop

**Source (Hans, 2026-08-11):** *collect UU hypothesis → what-else → murder board → autopsy
→ findings. Now it is a KK for me to decide on, with a confidence rating from you that I
can trust.*

| Step | Instrument | Job |
|---|---|---|
| 1. Collect | intake | Name the UU, land evidence, open KU |
| 2. What-else | `what-else` | Competing hypotheses; kill favorites |
| 3. Murder board | `murder-board` | Cross-family adversarial panel |
| 4. Implement / re-probe | build + sealed probe | Does it hold in *our* stack? |
| 5. Autopsy | `autopsy` | If a pre-registered test ran: cause of death against the chart |
| 6. Findings | FINDINGS / AAR | Sustain and improve; residual gaps |
| 7. Propose KK | agent | One plain claim, calibrated confidence, evidence, falsifier |
| 8. Decide | **Hans only** | Ratify, reject, or send back to KU |

Not every KU needs every instrument. The minimum before KU → KK:

1. Evidence you can re-run or re-open
2. At least one adversarial pass — what-else or murder board
3. The multi-source bar, path A or B
4. Implement/test or sealed re-probe when path B is in play; always for load-bearing claims

---

## The trust line

```
Above this line, I can trust it and move on.
│
Below it, I dig or wait.
```

Trust is not built by high numbers. **Trust is built when the line never lies.** Better to
hold a claim below the line than wave a false green above it.

| TRUST | Meaning |
|---|---|
| **GREEN** | Ratify from the card alone — only when every hard gate passes |
| **AMBER** | Second look even at a high score |
| **RED** | Never auto-trust — money, send, people, production bolt-ons |

**GREEN hard gates, all required, score cannot override:**

1. A live test report showing PASS, re-runnable
2. A falsifier in plain English you could watch fail
3. A residual that does not expand the claim past the test
4. Adversarial chew actually ran
5. The claim is a decision rule, not "the universe is safe"
6. The multi-source bar met — single-source stays AMBER at best

A score supports the line; it does not define it. A full method stack often maxes near 0.92.
**That number means the stack is full, not that the answer is yes.**

### KK proposal shape

```text
TRUST: GREEN | AMBER | RED
CLAIM: <one sentence>
SCORE: 0.xx  (supports the line; does not define it)
EVIDENCE: <paths>
SOURCES: <≥3 independent instruments, or implement/test path B — list them>
CHEW: what-else | murder-board | autopsy | implement | none
FALSIFIER: <what would make this false>
RIVAL HYPS: <what we tried to kill, and what survived>
RESIDUAL: <what we still don't know — must not expand past the test>
DECISION OWED: ratify | reject | re-chew
```

---

## Worked example — the instrument that defeated its own rule

2026-08-12. `multi_search`, the tool that exists to clear confident negatives under the
two-man rule, had two independent live defects:

1. **Phrase-not-terms.** Every strategy passed the whole query to `rg`/`find` as one literal
   contiguous pattern. A one-word query returned 17 hits; the same word plus a second term
   returned zero, with both terms present in the same tree. Since multi-word is how anyone
   asks, false negatives were the default behavior.
2. **Gitignore blindness.** ripgrep honors `.gitignore` while recursing, and the portfolio
   convention is *code tracked, all data ignored*. So the tool searched **code** and was
   blind to **data** — which is where "did this ever happen" is answered. Session
   transcripts returned 0 hits against 77 with the ignore rules off; memory files 0 against
   7. One strategy had reported `0 hits in 0.0s` for three days: silent, not an error,
   reading as *searched and clean*. Memory files were covered by **zero** strategies.

**Consequence:** a collection queue was declared nonexistent on the tool's word and a
duplicate was built from scratch, while the real one sat fully specified with working code.
The discipline fired correctly. The instrument lied.

**Two testing traps surfaced in the same repair, both general:**

- **Live-session contamination.** Once transcript search worked, the conversation asking
  *does X exist?* wrote X to disk within seconds and the search found its own question. A
  control of three invented words came back FOUND.
- **Control string on disk.** The nonsense control was then written into the tool's own
  docstring as the example, so the tool found itself and the control passed forever after.
  **Keep invented control terms in the command, never in a file under the search roots.**

Both are the no-self-grading rule in a new costume: **the author's own artifacts contaminate
the author's own test.** Neither was caught by care. Both were caught by a control that
could fail.

---

## Why the dwell state exists

| Failure mode | What KU blocks |
|---|---|
| Skimming a long ratify list | Nothing is known until tested |
| Over-claiming from one demo | An implement/test note is required on the ticket |
| It *feels* true | Feeling is not a known known |
| An automated PASS | PASS is evidence *toward* KU, not a finished KK |
| One recon rewiring the portfolio | Single source ceilings at KU |
| Confirmation hunting dressed as research | ACH: rivals named, favorites attacked |

---

## Doctrine fit

- **Force-multiplier:** implement and test is the work; ratification is judgment
- **Chain of command:** KK → memory is a one-way door, so it is Hans's
- **Two-man rule / no self-grading:** sealed probes and external evidence before KK
- **Multi-source and ACH:** independent instruments, disconfirm before promoting
- **Honesty:** *"I ratified a list I didn't fully read"* is a known human failure mode, and
  KU is the control for it

## Instances

| Surface | Queue |
|---|---|
| Agent recon | `funkytown/experiments/NN_*/KU_QUEUE.md`, driven by the `lightbulb` skill |
| Portfolio — engagements, builds, coursework, our own instruments | `~/.claude/collection_requirements.md` |

Skill-level mechanics, commands and per-experiment queues live with the instance. This file
holds only what is true on every surface.

## Two products, one epistemology (named 2026-08-22)

The loop above is the epistemology. It is not one machine.

| Product | Job | What may wear KK |
|---|---|---|
| **Wall pipeline** | A behavioral rule survives chew + a test that can fail; Hans ratifies; a machine re-verifies | Path-jail, secret channel, no-invent COMPLETE, continuity-is-disk. GREEN holds. |
| **Decision queue** | Named unknowns dwell. Only RAISE (decision + owner + trigger + consequence) reaches Hans | A proposed KK card. Quotes and biography that can be *shown* are FACTS, not KKs. |

Do not unify them by stuffing founder quotes, rehearsal fuel (REH-*), or
field notes without a live PASS into the wall state machine. That costume is
how twelve stamped lines became "ratified KKs" the census could not enforce.

**Generality remains a hypothesis** until a second surface completes a Hold
cycle (chew → live PASS → Hans ratifies → ingest). OpenMaus KU-OM-015 was
sent back to KU on 2026-08-22 (no live PASS on our gates). That cycle is
not finished.

LB-P010 soak closed the same day: KEEP the RAISE/HOLD filter.

### Panel stamp (2026-08-22)

Murder board: grok / gpt / gemini. No Fable. Cost $0.15.
Transcript: `operator/output/murder_board_collection_pipeline_2026-08-22/`.

Hans stamped the staff rec on the panel:

- **KILL** ingest of this file as portfolio Law (H1a).
- **KILL** cutting the machinery back to `multi_search` (H1c).
- Epistemology and the RAISE/HOLD filter **KEEP**, file stays **KU**.
- Do not fork an `EPISTEMOLOGY.md` and ingest it as Law.
- `fact_pager` is a probe, not the ratification engine. CR-3 still speaks
  2026-08-24.
- `decide_check.join_line` is retrieval at the cut, not a grader and not
  an organ (NOTICE-PS-001 crown kill).
- No 25-fire sample this sitting.

This file is still not Law. A second-surface Hold cycle with a live PASS
is still owed before ingest.
