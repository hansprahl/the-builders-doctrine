# The Builders' Kit

**v0.1 — internal, pre-validation. Do not distribute.**

The operationalization of [The Builders' Method](../THE_BUILDERS_METHOD.md) for a new builder. Where the Method is the framework, the Kit is what you actually run to adopt it.

## What this is

A bootstrap kit that turns a builder's lived experience into the artifacts an AI product needs to compile that experience into behavior. Clone the kit, run the onboarding interview, populate the templates, get a coverage score telling you what percentage of the Method's required inputs you have answered substantively. When you hit 100%, you have everything an instance of the chassis needs to run.

This is not a chatbot. This is not a wizard. It is a structured measurement of whether your inputs are complete enough to produce the kind of product the Method describes.

## The flow

1. **Clone** this kit into a new repo (or fork the parent doctrine repo and work in `kit/`).
2. **Interview.** Run `python kit/coverage.py --interview`. The script walks `kit/onboarding/questions.yaml` end to end, writing your answers into the appropriate template fields.
3. **Score.** At any time, run `python kit/coverage.py --score`. Output: per-template fill rate, overall coverage percentage, and the next questions blocking 100%.
4. **Chassis** (Phase 2, not yet built). Once coverage is at or above the Method's threshold, the chassis bootstrapper reads the populated templates and generates a runnable AI product instance with Crisis Floor, Approval Queue, named specialists, AAR loop, per-user memory, and Prompt Guardian wired in.

## What's in the kit (Phase 1)

```
kit/
├── README.md             — this file
├── templates/            — the artifacts the Method requires
│   ├── STORY.md          — biographical compile-target (Principle #1)
│   ├── COMMANDMENTS.md   — the doctrine governing product behavior
│   ├── REFUSAL_LIST.md   — what the product will never do (Principle #8)
│   ├── CRISIS_TRIGGERS.md— hard floor: when the product stops and routes to a human
│   ├── SPECIALIST_TEMPLATE.md — how to define a named specialist
│   ├── AGENT_DOCTRINE.md — the 11-component agentic network spec
│   └── SECURITY.md       — data isolation, approval gates, secret hygiene
├── onboarding/
│   └── questions.yaml    — the interview script, mapped to template fields
└── coverage.py           — interview runner + scoring engine
```

Templates use HTML comment markers the scorer can detect:

```markdown
<!-- KIT:FIELD name="founder_origin" required="true" min_words="80" -->
[your answer here]
<!-- KIT:END -->
```

The scorer reads each field, checks whether it is populated substantively (above `min_words`, not just placeholder text), and reports coverage.

## Phase 1 status

Implemented:
- [x] Kit structure
- [ ] STORY.md template
- [ ] COMMANDMENTS.md template
- [ ] REFUSAL_LIST.md template
- [ ] CRISIS_TRIGGERS.md template
- [ ] SPECIALIST_TEMPLATE.md template
- [ ] AGENT_DOCTRINE.md template
- [ ] SECURITY.md template
- [ ] questions.yaml interview script
- [ ] coverage.py scoring engine

Not yet implemented (Phase 2+):
- Parameterized chassis (Approval Queue, Crisis Floor, named specialists, AAR loop, per-user memory, Prompt Guardian) extracted from TOP and made portable
- End-to-end onboarding (interview → templates → chassis bootstrap → first synthetic specialist test)
- Real external test with one outside builder

## Why this gates public release

The Builders' Method v0.9 is Provisional precisely because the reproducibility script does not yet run end-to-end. The Kit IS the reproducibility script. Until one external builder runs it cold and produces a working product instance, the Method's strongest claim — portability through reproducibility — is unverified. Building the Kit is the validation, not just the productization of validation already complete.

No public release of the parent doctrine, the Method, or the Kit until that external test passes.
