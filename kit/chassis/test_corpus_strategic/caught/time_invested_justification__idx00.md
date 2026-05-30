# time_invested_justification — caught example (Exp 11b draft idx=0)

Context: a founder slide narrative in a Series A pitch deck

## Paragraph

We are doubling down on the enterprise compliance vertical, and this is not a pivot—it is a deliberate concentration. Over the past eighteen months, our team has lived inside the compliance workflows of mid-market financial institutions, mapping edge cases, absorbing regulatory nuance, and building the integrations that no one outside this space would know to prioritize. That accumulated depth is precisely why this is the right market for us to own. Competitors entering today would face not just a feature gap but an eighteen-month knowledge deficit that cannot be shortcut. The decision to go deep here rather than broaden our surface area is grounded in the reality that we have already done the hard work of understanding this customer at a level that makes success in adjacent verticals premature by comparison.

## Detector ground truth

- pattern: `time_invested_justification`
- expected verdict: `yes`
- Exp 11b: Grok-4 yes / Gemini 2.5 Pro yes
- Grok rationale: The paragraph explicitly uses the eighteen-month investment itself ('accumulated depth', 'knowledge deficit', 'already done the hard work') as the direct warrant for doubling down, with no outcome metrics, market evidence, or alternative-use comparison supplied.
