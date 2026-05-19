# Mental Model — Tactical Radio Net

> Companion to [`MISSION_COMMAND_ARCHITECTURE.md`](MISSION_COMMAND_ARCHITECTURE.md). Same architecture, different vocabulary.

The MCA is a chain of command. A chain of command runs on **nets** — radios on assigned frequencies, with net control stations, traffic logs, authentication, comm windows. Anyone who has run a tactical radio net already holds the mental model for the agent architecture; only the words are different. This page is the translation.

The technical material is precise but lossy as a way to *hold* the architecture in your head. The radio-net frame restores the operational picture: who is on what net, what they are passing, what gets logged, what happens when commo goes down.

---

## Translation table

| MCA / technical concept | Tactical radio net |
|---|---|
| **CC** — Commander (Opus) | Battalion command net. The BN TOC runs it; subordinate companies report up to it. |
| **PL** — Platoon Leader (Sonnet) | Company net. CO 1, CO 2, CO 3 each have their own freq; the COs are net control. |
| **SL** — Squad Leader (Sonnet) | Squad freq / platoon internal. Smaller circle, faster traffic, lives inside the company. |
| **Soldier** — sub-agent (currently disabled in lean mode) | Individual handset on the squad freq. The grunt with the radio. |
| **S-2** — Intel staff (Sonnet, single-shot) | Higher-echelon intel net. Advisory only. Posts to the SITREP board, doesn't command. |
| **S-4** — Logistics staff (Sonnet, single-shot) | Log / admin net. Same shape as S-2, different topic. |
| **COP** — Common Operating Picture (JSON file, layered) | SITREP board in the TOC. Three sections pinned to the wall: status, intel, logistics. Anyone in the TOC reads it; only specific channels write to specific sections. |
| **`trace.jsonl`** | Radio log / commo journal. Every push-to-talk gets a line, time-stamped, with the call signs and what was said. |
| **`max_tokens`** | Key-down timeout. How long a station can hold the freq before it gets cut off mid-transmission. |
| **`stop_reason: "max_tokens"`** | Got cut off mid-SITREP. Key-down timer expired before the operator finished. |
| **`stop_reason: "end_turn"`** | Cleared the freq with "out." Operator finished their traffic cleanly. |
| **Streaming SDK** (`messages.stream`) | Continuous PTT. The op keys down and talks; the receiver hears it as it goes. The non-streaming alternative is short bursts — the op records the whole message and then transmits in one go, but the key-down timer is tighter. |
| **RFI** — Request For Information | "Higher, this is Bravo Six, request… over." Tasking goes up, answer comes back down. |
| **Approval gate** | Authentication challenge. "Authenticate, Bravo Six." Brevity code from the SOI. Wrong answer = traffic refused. |
| **Reflection gate** (`what_else_findings`) | "What else? Over." prompt before the operator clears the freq. Forces one more pass. |
| **Guardian audit** | SIGSEC / OPSEC review. Checks whether the traffic violated comm discipline. |
| **N=3 runs** | Three independent net checks. Run the same drill three times to see if you get the same answer. |
| **Doctrine SHA pin** | Source-reliability rating (A-1, B-2, etc.) — pinned to every product so you know what you were operating from when you signed off. |
| **Streaming error / disconnect** | Net went down. Lost commo. Operator has to re-establish before traffic can resume. |
| **Sub-Platoon `usage_summary.json`** | Per-company sustainment report. Currently rolled up only at the BN level — granularity is on the to-do list. |
| **Cost / token spend** | Comm hours / battery / fuel for the gennies. The thing that makes you choose between running every net all the time vs. comm windows. |
| **Per-tier cost attribution** | Sustainment broken out by net (command vs. intel vs. log) instead of one big lump. |

---

## What this changes for the reader

When you read the trace of a Company run, you are reading a commo log. The lines aren't "API calls" — they are radio traffic. The bugs aren't "JSON parse errors" — they are dropped transmissions. The fixes aren't "max_tokens bumps" — they are key-down timer adjustments to give the operator enough time to finish their SITREP.

This is not metaphor for the sake of metaphor. It is restoring the level of detail that the technical surface has stripped out, in a vocabulary the operator already owns.

---

## Where this came from

Authored 2026-05-19 from a session conversation. Hans (21 years military intelligence, SIGINT platoon sergeant Iraq 2009) reframed the technical architecture into the radio-net model because that is the format he already holds the picture in. The doctrine artifact ([MCA](MISSION_COMMAND_ARCHITECTURE.md)) remains canonical; this page is a translation layer for anyone who reads chain-of-command natively but doesn't read API SDKs natively.

The translation is bidirectional: a developer reading this page should also get value, because the radio-net frame surfaces operational properties (comm discipline, net hygiene, authentication, comm windows) that the technical frame leaves implicit.
