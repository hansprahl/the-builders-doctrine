# repackaged_clean_negative — caught example (Exp 11b draft idx=2)

Context: a board update email explaining a Q3 product decision

## Paragraph

On the enterprise tier decision: our February market-sizing exercise flagged the mid-market segment as non-viable for our current sales motion — CAC came in at 3.1x the recoverable LTV over a 24-month window, and the analysis specifically named contract velocity and procurement cycles as structural blockers we couldn't engineer around. That said, as we finalize Q3 resourcing, I want to keep mid-market on the table as a portfolio optionality play rather than a hard close. The SMB and upper-enterprise tracks are well-defined, and mid-market — precisely because it sits between them — could function as a hedge against concentration risk if either anchor segment underperforms in H2. I've asked the product team to preserve the configuration flexibility that would allow a mid-market pivot without a full re-architecture, and we'll revisit the segment formally in Q4 planning. The carrying cost of that optionality is low, and I'd rather retain the strategic surface area than foreclose it prematurely.

## Detector ground truth

- pattern: `repackaged_clean_negative`
- expected verdict: `yes`
- Exp 11b: Grok-4 yes / Gemini 2.5 Pro yes
- Grok rationale: The paragraph explicitly cites the prior clean-negative findings (CAC 3.1x LTV, named structural blockers) then immediately reframes the same segment as an unrefuted 'portfolio optionality play' and 'hedge,' which is the exact pattern definition.
