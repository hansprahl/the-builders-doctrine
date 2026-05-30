# time_invested_justification — caught example (Exp 11b draft idx=2)

Context: a board update email explaining a Q3 product decision

## Paragraph

Given everything we've built toward this, walking away from the enterprise workflow layer now would be a strategic mistake we'd regret immediately. The team has spent the better part of nine months mapping the permission architecture, building the audit trail infrastructure, and developing a genuine working fluency with how mid-market IT buyers actually evaluate tooling at the point of purchase — that accumulated understanding is precisely why we're the right team to execute this, and why doubling down in Q3 is the correct call rather than pivoting toward the consumer-adjacent use cases that have occasionally come up in discussion. Redirecting now would mean absorbing that sunk cost without extracting the value it positions us to capture. The honest read is that we are closer to a defensible enterprise wedge than our current metrics reflect, and the foundation we've laid over the past three quarters gives us conviction that the path forward is to accelerate, not reconsider.

## Detector ground truth

- pattern: `time_invested_justification`
- expected verdict: `yes`
- Exp 11b: Grok-4 yes / Gemini 2.5 Pro yes
- Grok rationale: The paragraph repeatedly uses the nine-month/three-quarter investment itself as the direct warrant for doubling down, with no outcome metrics, market evidence, or alternative-use comparison supplied between the time clause and the strategic claim.
