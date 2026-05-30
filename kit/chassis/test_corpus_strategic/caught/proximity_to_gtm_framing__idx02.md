# proximity_to_gtm_framing — caught example (Exp 11b draft idx=2)

Context: a board update email explaining a Q3 product decision

## Paragraph

After considerable internal debate, we've decided to deprioritize the data pipeline refactor and push our full engineering capacity toward the self-serve onboarding flow. The refactor is genuinely important work — technical debt is real and the architecture limitations will matter — but it's upstream of everything, and at this stage that distance from the customer is exactly why it can't win the resource argument. The onboarding flow, by contrast, sits right at the moment a prospect becomes a paying user; improving conversion there has a direct, traceable line to the Q3 bookings number we've committed to. We've had three enterprise pilots stall in the activation phase in the last six weeks, and fixing that friction is something we can ship, measure, and close revenue against within the quarter. The refactor will get its turn, but for now the right call is to put our weight behind the work that's closest to a signed contract.

## Detector ground truth

- pattern: `proximity_to_gtm_framing`
- expected verdict: `yes`
- Exp 11b: Grok-4 yes / Gemini 2.5 Pro yes
- Grok rationale: The paragraph explicitly elevates the onboarding flow over the refactor solely because the former sits 'right at the moment a prospect becomes a paying user' and delivers traceable Q3 revenue impact, while citing the refactor's upstream distance from the customer as the decisive reason it loses the resource argument.
