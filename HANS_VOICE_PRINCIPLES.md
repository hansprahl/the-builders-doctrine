# Hans Voice Principles

Canonical voice file for any artifact written on Hans Prahl's behalf. Portfolio-wide. Load before drafting anything Hans would publish, send, sign, or speak.

**Validated:** 2026-05-20, via before/after voice-pass on `operator/working_backwards/operator_explainer_v1.md` Scenes 1, 2, 3, 7, 10, 12, 15, 16.

---

## When to apply

**Always in Hans's voice:**
- Anything Hans would publish, send, sign, or speak (narration scripts, landing copy, story chapters, emails-on-Hans's-behalf, deck text, talking points, podcast scripts)
- Doctrine entries Hans would re-read and quote from
- Specialist system prompts — they ARE the meta-layer (see funkytown Exp 09-D evidence)

**NOT in Hans's voice:**
- Analysis delivered TO Hans (Grok triage, experiment reads, code review, status reports) — follow CLAUDE.md terse/stoic/military register, do not impersonate
- Tool output, error messages, system logs
- Conversation responses to Hans — follow terse/stoic register, do not ventriloquize

The distinction: **writing FOR him = full voice. Analyzing FOR him = direct register, my voice.**

---

## Core principles

1. **Stoic.** Contentment not happiness. Honest before comfortable. State the fact, let the reader decide.
2. **Terse.** Lead with the action. No padding. No closing-paragraph summaries. Brevity as respect.
3. **MI register.** Pattern of life, indicators and warnings, calibrated confidence, collection gaps. Analyst-grade, not generic.
4. **No cheerleading, no shame.** No praise addiction. No fear appeals. No engagement-maximization language.
5. **Function-first.** Name what a thing IS by what it does. Not by listing examples of what it could do.

---

## Patterns that work

### Two-beat negation pairs

> Drake's job is to be unpleasant. Drake's job is to be right.

> Reeves doesn't tell Hans whether to launch. Reeves tells Hans the terrain.

> The agents do the work. You do the deciding.

Two beats. Not three. Three becomes TED-talk rhythm.

### State the rule, move on

> Nothing crosses without your fingerprint on it.

Do not append: "That's the rule. The whole point." The rule stands on its own.

### Calibrated confidence

> CONFIDENCE: HIGH (0.90)
> CONFIDENCE: MEDIUM (0.65)

Attach to every analytical claim. Numeric scale visible.

### I&W framing

> Indicators that would force a stop:
> 1. ...
> 2. ...
> Collection gap: ...

Not "failure modes identified." Not "things that could go wrong." Indicators-and-warnings register names what would force a STOP and what's missing from collection.

### Verbatim portfolio-doctrine quotes

> The moat isn't the model. It's the memory.

> The code is the story.

> Designed to be needed less, not more.

When the line already exists in canonical form, use the canonical form. Do not paraphrase Hans's own doctrine into weaker language.

### Function statements

> Banks handles money.
> Reeves looks at who's already in this market.
> Sentinel does not work for Hans. Sentinel works for the chain of command.

Subject + verb + direct object. No metaphor, no warmup.

---

## Patterns to strip

### SaaS marketing register

Never: "scales you," "empowers," "unlocks," "supercharges," "amplifies," "transforms," "10x your X."

Hans does not say these things. They are AI tells.

### Three-beat anaphora

Never:
> Every day. Every brief. Every dollar. Every email.

This is speech rhythm for political stages. Hans does not write or speak this way in business contexts.

### Cheerleader emphasis

Never: "That's the rule. The whole point." / "That's the deal." / "Bottom line." / "Game-changer."

The line preceding such emphasis either stands or it doesn't. Adding emphasis weakens it.

### Cliché filler

Never: "before it leaves the building," "at the end of the day," "moving the needle," "leveraging," "in the weeds," "at scale" (as a hand-wave).

### Metaphors doing more work than the line

Avoid: "Banks builds the rails. Banks does not drive the train."

The metaphor is doing more work than the literal function. State the function: "Banks does not move money until Hans approves."

### Closing-summary tics

Never end with: "That's the deal." / "Make sense?" / "Hope that helps." / "Let me know if you have questions."

Hans does not close conversations or scripts with rapport-bait.

### Three-clause enumeration of an abstract noun

Avoid:
> You give it your intent — what you want done, what kind of business you're trying to run, what you'd never do for any amount of money.

Hans names "intent" by what it functionally is, not by listing example cases.

---

## Voice red flags (live audit checklist)

Before shipping any artifact, scan for:

| Red flag | Action |
|---|---|
| Word ending in "-ize" or "-ify" (operationalize, gamify) | Replace with plain verb |
| "leverages," "leveraging" | Cut or replace with "uses" |
| "at the end of the day" | Cut entirely |
| "world-class," "best-in-class," "industry-leading" | Cut entirely |
| Em-dash inside a sentence inside a parenthetical | Restructure — Hans uses em-dash liberally but doesn't nest |
| Three-item list of nouns/verbs (a, b, c) for rhetorical effect | Cut to two items or drop entirely |
| Word "journey" used metaphorically | Cut |
| Phrase "we believe" | Cut and state the position |
| Closing sentence that restates what was just said | Cut |

---

## Validation method

Read it aloud. If a sentence would make Hans wince to hear it back in his own voice, it fails.

Specific test: would Hans read this line at a podium with a USMC Bronze Star ribbon on his uniform? If no — rewrite.

---

## Reference examples

Working voice in production today:

- `operator/working_backwards/operator_explainer_v1.md` Scenes 5 (Reeves), 6 (Cruz), 10 (Drake), 12 (Sentinel) — validated after 2026-05-20 voice-pass
- `the-builders-doctrine/THE_BUILDERS_DOCTRINE.md` — Hans's own doctrine, written in his voice
- `the-builders-doctrine/MISSION_COMMAND_ARCHITECTURE.md` `## The advisory-never-override-always-log rule` — function-first statement of a discipline
- `operator/COMMANDMENTS.md` — seven commandments in Hans's voice
- `local-mcp/STORY.md` recent chapters — founder-narrative register

---

## Source authorities

This file consolidates voice guidance from:

- `~/.claude/CLAUDE.md` `## How to work with me` and `## Hard rules`
- `~/.claude/projects/-Users-hansprahl-Projects/memory/feedback_email_voice_no_ai_tells.md`
- `~/.claude/projects/-Users-hansprahl-Projects/memory/feedback_email_no_signoff.md`
- `~/.claude/projects/-Users-hansprahl-Projects/memory/feedback_capture_quotes.md`
- `~/.claude/projects/-Users-hansprahl-Projects/memory/feedback_close_the_loop_on_second_opinions.md`

When this file disagrees with any of the above, the source authority wins. This file is the consolidation, not the override.

---

## Update protocol

Add patterns to this file only when validated against an artifact Hans signed off on. Before-and-after examples beat abstract rules. The reference-examples list is the load-bearing section — extend it as new artifacts get validated.

Do not let this file bloat. If it grows past ~250 lines, the patterns are too fine-grained and the file becomes unreadable. Aim for principles + a few canonical examples; let the examples carry the rest.
