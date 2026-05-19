---
status: clean
patterns: []
provenance: excerpt
source: kit/chassis/prompt_guardian.py module docstring — technical prose, no biographical markers, no over-claim language
---

The Builders' Kit — Prompt Guardian.

Portable implementation of the adaptive prompt-optimization primitive specified
in TOP, Operator, and Custer. The Guardian periodically scores each specialist's
system prompt against a list of product-specific Commandments, flags drift,
generates a minimum-surgical correction, and queues that correction for human
approval. The same primitive runs across all three products with different
commandment sets.

Doctrine invariants this module preserves (non-negotiable):

  1. Source code is read-only with respect to the Guardian. Corrections
     never overwrite .py source.
  2. Hard-floor commandments only flag left drift. Drift "above" the hard
     floor is never a correction trigger — only drift below it.
  3. Corrections never auto-apply. Every correction routes through the
     ApprovalQueue chassis.
  4. The MINIMUM-SURGICAL-EDIT discipline is in the correction prompt,
     not in the chassis code.

This module is LLM-agnostic. The product passes a chat_completion callable
that takes (system_prompt, user_prompt) and returns raw text.
