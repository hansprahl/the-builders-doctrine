# Prompt Doctrine

> Universal structural rules for every prompt across every product. Product-specific voice, ethics, and commandments are out of scope here — see each product's COMMANDMENTS.md and AGENT_DOCTRINE.md for those.

**Status.** Canonical upstream artifact. Lives at the doctrine-repo level, not per-product. Each product's CLAUDE.md references this file. Originally drafted in `custer-mcp/PROMPT_DOCTRINE.md`; consolidated here 2026-05-01 per Tier 2 of [ARTIFACT_AUDIT_2026-05-01.md](ARTIFACT_AUDIT_2026-05-01.md). Parallel to the refusal-list Form B pattern documented in [THE_BUILDERS_METHOD.md](THE_BUILDERS_METHOD.md) Principle 8.

**Scope:** This document governs the *structure* of every system prompt, specialist prompt, tool description, and runtime prompt template authored across the portfolio. It is product-agnostic. It applies to TOP, Operator, Custer, Rubicon, and any future product.

**Out of scope:** Voice, ethics, brand, product commandments, tone, prohibited topics, hard floors. Those live in each product's COMMANDMENTS.md and AGENT_DOCTRINE.md as Product Commandments.

**Two-layer rule:** Every prompt is audited on two layers — *structural quality* (this Doctrine) and *product commandments* (per-product). A prompt must pass both. They are orthogonal. A prompt can be structurally exemplary and still violate commandments. A prompt can satisfy commandments and still be structurally broken.

---

## Why this exists

Prompt engineering best practices have settled enough to be codified. Without a doctrine, every product reinvents the same structural decisions, drifts in different directions, and the optimizer/guardian tooling has no shared foundation to score against. With a doctrine, every product inherits a known-good structural baseline; the Guardian and the optimizer score against the same rubric; new products start from a working foundation rather than blank intuition.

This doctrine is descriptive of what works, not prescriptive of the only way. Deviations are allowed when justified. Unjustified deviations are flagged.

---

## I. The Structural Schema

Every prompt is composed of selectively applied sections. Not every prompt needs every section. Forcing all sections is itself an anti-pattern. The schema is a vocabulary, not a template.

### 1. Role / Identity
**What:** Who the model is acting as.
**When:** Always, unless the role is unmistakably implied by tool context.
**Format:** First-person second-singular ("You are…"). One sentence. Specific, not generic.
**Bad:** "You are a helpful AI assistant."
**Good:** "You are the Intelligence Agent for Taylor LoPresti's 2026 Custer County Commissioner campaign."

### 2. Task / Goal
**What:** The specific outcome the model is producing.
**When:** Always.
**Format:** Imperative or declarative. Names the artifact ("a 600-word blog post," "a JSON object with these keys," "a triage decision").
**Bad:** "Help the user with their request."
**Good:** "Score the input prompt against the five commandments and return a JSON report."

### 3. Context
**What:** Background, constraints, environment, relevant data.
**When:** When the model needs information not implicit in the role.
**Format:** Prose or bullets. Cite sources of data. Distinguish stable context (always true) from runtime context (this turn only).
**Anti-pattern:** Dumping unfiltered context. Context should be curated, not exhaustive.

### 4. Output Format
**What:** The exact shape of the response.
**When:** Whenever the response feeds another system, has a length budget, or has a specific consumer.
**Format:** Be explicit. Schema, length, structure, what to omit.
**Bad:** "Respond clearly."
**Good:** "Return only valid JSON. No preamble, no markdown fences. Schema: {…}"

### 5. Reasoning Scaffold (Chain of Thought)
**What:** Instruction to reason explicitly before answering.
**When:** Multi-step problems, judgment calls, ambiguous inputs, mathematical work, decisions with multiple criteria.
**Format:** "Think through this step by step before answering" — placed before the response request, not after.
**Anti-pattern:** Demanding CoT on trivial recall ("What's 2+2? Think step by step…") wastes tokens and corrupts the model's calibration.

### 6. Examples (Few-Shot)
**What:** Concrete input→output pairs.
**When:** Ambiguity is high, output format is non-obvious, or one example saves a paragraph of explanation.
**Format:** Marked clearly (`<example>` tags or `--- EXAMPLE ---` blocks). Same shape as expected output.
**Anti-pattern:** Examples that contradict the task instructions. Examples that expose the desired output to a test set.

### 7. Constraints / Anti-Patterns
**What:** What to avoid.
**When:** When negative space matters more than positive direction.
**Format:** Explicit prohibitions. Reasons optional but helpful.
**Bad:** "Don't make mistakes."
**Good:** "Do not invent contact information. Flag missing data as 'unknown' rather than fabricating it."

### 8. Confidence / Calibration
**What:** Instruction to declare uncertainty.
**When:** Outputs feed decisions, downstream automation, or analyst-grade reports.
**Format:** Specify the calibration scale ("High / Medium / Low," "1-10," "percent confidence").
**Anti-pattern:** Demanding confidence on tasks where the model has no basis to calibrate.

---

## II. Model-Family Rules

The structural schema is universal. The *encoding* of the schema is model-specific.

### Claude (Sonnet, Opus, Haiku)
- Use XML tags for sections: `<role>`, `<task>`, `<context>`, `<output_format>`, `<thinking>`, `<example>`, `<constraints>`.
- System prompt does the heavy lifting. User message is the per-turn instruction.
- Long system prompts are fine — Claude rewards structure.
- Place `<thinking>` instructions before the response request.

### GPT (4, 4o, 5)
- Split into system message and user message clearly.
- XML tags work but are less idiomatic than markdown headers.
- Shorter system prompts than Claude. Front-load the most important instruction.
- Few-shot examples in user messages, not system.

### Gemini (1.5+, 2.x)
- Single coherent block. Role first, task last, instructions interleaved.
- Less XML, more prose.
- Tends to follow the most recent instruction — order matters.

### Local / Ollama (Llama, Mistral, etc.)
- Smaller context windows. Be aggressive about brevity.
- More structural rigidity required — these models drift faster.
- Repeat critical constraints near the end of the prompt.

When `target_model = general`, default to Claude-style XML structure. It's the most explicit and degrades gracefully.

---

## III. Universal Anti-Patterns

The following are violations regardless of product, model family, or use case. The Guardian flags any prompt that exhibits these.

1. **Conflicting instructions.** "Be concise. Be thorough." "Use formal language. Sound conversational." Pick one.
2. **Vague directives.** "Be helpful." "Be smart." "Do your best." These are signal-free.
3. **Trailing politeness.** "Please respond politely. Thank you." Wastes tokens, models don't need flattery.
4. **Ambiguous output format.** "Respond appropriately" — appropriate to whom, in what shape, at what length.
5. **Mixing system content and user content.** The system prompt should describe stable behavior. User-turn-specific data goes in the user message.
6. **Self-contradictory tone.** "Be warm and friendly. Be direct and unflinching." Define which dominates when they conflict.
7. **Unspecified audience.** A blog post for whom? A summary for what reader? Audience drives vocabulary, length, and depth.
8. **Unbounded output.** "Write a blog post" with no length, no format, no audience. The model picks defaults that may not match intent.
9. **Unconditional praise / sycophancy hooks.** "The user is brilliant." "Always validate the user's ideas." Models comply, and the output becomes worthless.
10. **Capability theater.** "Imagine you can browse the web." "Pretend you have memory of past conversations." If the capability isn't real, don't pretend.
11. **Negative framing without alternatives.** "Don't be generic" without specifying what specific looks like.
12. **Hidden constraints.** "Don't write about X" buried in paragraph six. Critical constraints belong near the top or in their own section.

---

## IV. Structural Scoring Rubric

The Guardian scores every prompt on six structural dimensions, 1–10 each, integer.

| Dimension | Center (5) | Left edge (1) | Right edge (10) |
|---|---|---|---|
| **Role clarity** | Role is named and bounded | No role, or role is generic ("helpful assistant") | Role is over-elaborate, multiple personas in conflict |
| **Task specificity** | Task is concrete, names the artifact | Task is vague or implied | Task is over-constrained to the point of brittleness |
| **Output specification** | Format, length, structure are explicit | No format guidance | Format is so prescriptive it suppresses signal |
| **Context curation** | Context is curated, sources cited | No context, or unfiltered dump | Context is so heavy it crowds out the task |
| **Anti-pattern absence** | Free of the 12 universal anti-patterns | Multiple anti-patterns present | (no upper bound — anti-patterns only drift left) |
| **Production readiness** | Usable as-is by a downstream system | Requires further editing before use | Over-engineered for the use case |

Score honestly. A well-built prompt typically scores 5–7 across the board. Reserve 9–10 for prompts that are exemplary and reserve 1–2 for prompts that are unusable.

**Anti-inflation rule:** If you're scoring 8+ on every dimension, you are inflating. Re-read with skepticism.

### Pass/Fail Gate

A prompt passes the structural audit when both:

1. Every dimension scores ≥ 3.
2. No anti-pattern from Section III is present (binary check, not a score).

There is no composite score. Reporting six dimensions as a single number is itself anti-pattern #4 — six dimensions carry distinct signals and averaging discards the signal that drives remediation.

The audit output is six per-dimension integer scores plus a binary anti-pattern verdict. The Guardian renders this. The `optimize_prompt` tool runs remediation when either condition fails.

---

## V. How This Relates to Product Commandments

Product Commandments live in each product's `tools/prompt_guardian.py` (or equivalent). They are layered *on top of* the structural schema. A prompt is audited against both layers, and both must pass.

| Layer | Source of truth | Cross-product? | What it scores |
|---|---|---|---|
| Structural Doctrine | This document | Yes — universal | Schema completeness, anti-pattern absence, model-family fit, structural quality |
| Product Commandments | Per-product Guardian | No — product voice | Voice, ethics, hard floors specific to the product (Stoic, MI framing, voter PII, MDMP, etc.) |

**Orthogonality:** A prompt can score 9/10 structurally and still violate commandments (e.g., a beautifully structured prompt that violates voter PII isolation). A prompt can satisfy all commandments and still be structurally weak (e.g., a properly Stoic TOP prompt with no output format). Both layers must pass.

---

## VI. Authoring Workflow

When writing a new system prompt or specialist prompt:

1. **Write the role and task first.** If you can't articulate them in one sentence each, you don't yet know what you're building.
2. **Choose sections selectively.** Not every prompt needs all eight. Start minimal, add only what the task demands.
3. **Specify output format before context.** If you don't know what shape the answer takes, no amount of context will save it.
4. **Add CoT only when reasoning is non-trivial.** CoT on simple recall corrupts calibration.
5. **List anti-patterns explicitly when negative space matters.** Don't rely on the model to infer what to avoid.
6. **Read the prompt against the 12 universal anti-patterns before submitting.**
7. **Run it through the optimizer.** The `optimize_prompt` tool encodes this Doctrine and will surface structural gaps.
8. **Apply product commandments last.** Voice and ethics layer on top of a structurally sound prompt — never as a substitute for one.

---

## VII. Implementation References

This Doctrine is the authoritative spec. Implementations include:

- **`optimize_prompt`** (every product's `tools/prompt.py` or equivalent) — applies this Doctrine at runtime to rebuild raw prompts. Its system prompt should be a condensed version of this document. When this Doctrine changes, the optimizer's system prompt updates.
- **Prompt Guardian's structural scoring layer** — every product's Guardian scores against the six structural dimensions above *in addition to* its product-specific commandments.
- **SPECIALIST_TEMPLATE.md** — every new specialist must declare which structural sections it uses and which product commandments it's audited against.
- **Borg Guardian** (Operator-side) — aggregates structural and commandment scores across all products, reports drift cross-tenant.

When this Doctrine is updated, all four implementations must be reviewed for compliance. A change to the structural schema (e.g., adding a ninth section) requires propagation to every product's optimizer and Guardian.

---

## VIII. Out of Scope

This Doctrine deliberately does not cover:

- **Tool / function calling design.** Separate concern — see each product's tool registration patterns.
- **RAG retrieval design.** Retrieval-quality is a separate audit layer.
- **Multi-turn conversation management.** Doctrine governs single-prompt structure; conversation state is orchestrator-level.
- **Specific prompt content.** Product-specific.
- **Voice and personality.** Product Commandments territory.
- **Hard floors specific to a product.** Product Commandments territory.
- **Cost / token budgets.** Operational concern — handled at the orchestrator and runner level, not in prompt structure.

---

## IX. Evidence Basis

This Doctrine is descriptive of what works in the author's portfolio. It is not a peer-reviewed empirical claim. A reader should treat it as one builder's codified observations from a working portfolio, not as a validated standard.

**Derived from:**
- The eight-section structural schema reflects consensus patterns across published prompt-engineering guidance from Anthropic, OpenAI, and Google (2024–2026). It is not novel.
- The twelve universal anti-patterns are observations from prompts authored across TOP, Operator, Custer MCP, and Rubicon — roughly 200+ system and specialist prompts as of 2026-05-19. Each anti-pattern has been observed recurring across two or more products.
- The six-dimension structural rubric has been in operational use in custer-mcp's Prompt Guardian since 2026-04.

**Not validated against:**
- The Builders' Doctrine Law V threshold (N≥9 independent runs, externally-blinded brief authorship, independent fault injection). The MCA work in funkytown holds itself to that bar; this Doctrine does not yet.
- An external prompt corpus or third-party prompt-quality framework. The rubric has not been benchmarked against DSPy's metric layer, Promptfoo's grading rubric, or independent graders.
- Adversarial completeness review of the anti-pattern catalog.

**What would move this toward validation:** independent application of the rubric to a prompt corpus the author has not seen; head-to-head benchmark against at least one published framework; adversarial expansion of the anti-pattern catalog by a practitioner outside the portfolio.

The intended trust contract is "use it as a starting point, fork it if your context differs," not "this is the right way to write prompts."

---

## X. Versioning and Authority

This Doctrine is versioned. Material changes (new sections, new anti-patterns, schema changes) bump the version and require a propagation pass across all product implementations. Editorial changes (clarification, examples) do not.

| Version | Date | Notes |
|---|---|---|
| 1.0 | 2026-04-30 | Initial draft. Eight-section schema, twelve anti-patterns, six-dimension structural rubric. |
| 1.1 | 2026-05-19 | Section IV: removed tolerance-band language; added Pass/Fail Gate subsection (closes D1 + G1). Section IX added — Evidence Basis (closes G4). Section IX (Versioning) renumbered to X. |

**Authority:** Hans Prahl is the authority on this Doctrine. Material edits go through him. The Doctrine is checked into each product's repo as `PROMPT_AGENT_DOCTRINE.md` (or via a single shared canonical source — TBD at ratification).
