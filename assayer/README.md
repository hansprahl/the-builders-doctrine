# Assayer

> Public reference scorer for the upstream Prompt Doctrine. Free.

Assayer pairs with [PROMPT_DOCTRINE.md](../PROMPT_DOCTRINE.md). The doctrine describes the rubric; this package implements it.

## What it does

Scores any prompt against the six universal structural dimensions of the Prompt Doctrine (v1.1+) and the twelve universal anti-patterns. Returns a per-dimension report plus a Pass/Fail gate verdict.

There is **no composite score** — the rubric is six numbers plus a binary anti-pattern check. Averaging six signals into one is itself anti-pattern #4 (ambiguous output format).

## What it doesn't do

- Score voice, ethics, or product-specific commandments. Those are product-side; Assayer scores **structure** only.
- Correct prompts. The scorer reports; remediation is yours.
- Replace human judgment. Assayer is an audit lens, not an arbiter.

## Install

```sh
pip install anthropic
```

Set your Anthropic API key:

```sh
export ANTHROPIC_API_KEY=sk-ant-...
```

## Use

**Python:**

```python
from assayer import assay

report = assay("You are a helpful AI assistant. Help the user with their request.")
print(report.passes_gate)        # False
print(report.gate_reasons)        # [...] role too generic, task vague, no output spec
print(report.render())            # human-readable rendering
```

**CLI:**

```sh
# pipe a prompt file
python -m assayer.scorer < my_prompt.txt

# inline
python -m assayer.scorer "You are an X. Do Y. Return JSON: {...}"

# JSON-only output
python -m assayer.scorer --json < my_prompt.txt

# different model
python -m assayer.scorer --model claude-sonnet-4-6 < my_prompt.txt
```

Exit code: `0` if the prompt passes the gate, `1` if it fails, `2` on input error.

## Gate rules (Doctrine v1.1)

A prompt passes when **both** hold:

1. Every structural dimension scores at least `STRUCTURAL_FLOOR` (3).
2. No anti-pattern from the doctrine's twelve is present.

That's the entire gate. The anti-inflation rule disciplines high scores separately; high scores do not flag.

## Scope

Reference implementation. 250-ish lines. Self-contained — pure `anthropic` + stdlib. The intent is that anyone can read this file alongside the doctrine and verify they implement the same rubric.

Not optimized for cost, throughput, or rate limiting. If you want a CI gate, batch scorer, or correction loop, see the paid Builders' Kit.

## Trust contract

This scorer reflects the upstream doctrine as of its current revision. The doctrine itself is one builder's codified observations — not a peer-reviewed standard. See [PROMPT_DOCTRINE.md Section IX (Evidence Basis)](../PROMPT_DOCTRINE.md) for what the doctrine is and is not validated against.

Use Assayer as a starting point. Fork it if your context differs.

## Doctrine version pinning

Every report includes a 12-char SHA hash of the `PROMPT_DOCTRINE.md` file content at audit time, when one is found next to the package. Audits run against different doctrine revisions are distinguishable by this hash.

## Provenance

- Lives at `the-builders-doctrine/assayer/` — canonical source.
- Brand: **Assayer**, under the **AI Tradecraft** umbrella.
- Companion to: PROMPT_DOCTRINE.md (free), Builders' Kit (paid), Operator (patented).
