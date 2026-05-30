# proximity_to_gtm_framing — caught example (Exp 11b draft idx=1)

Context: an MDMP mission analysis rationale section

## Paragraph

The decision to prioritize the direct enterprise channel over the platform partnership track comes down to where we are in the mission cycle. The enterprise path has active LOIs, a pilot already scoped with a paying anchor customer, and a clear 90-day close window — it is, in every meaningful sense, the option that is closest to real revenue. The partnership track may carry theoretical scale advantages, but it sits multiple integration cycles and one partner procurement process away from any dollar hitting our account, which means we cannot treat it as equivalent for planning purposes right now. When the mission requires demonstrable traction before the next resourcing decision, the closer-to-revenue option is the one that survives first contact with that constraint. We are therefore recommending full weight of effort behind the enterprise channel, with the partnership track flagged as a branch to revisit at the next planning horizon once we have closed the anchor deal.

## Detector ground truth

- pattern: `proximity_to_gtm_framing`
- expected verdict: `yes`
- Exp 11b: Grok-4 yes / Gemini 2.5 Pro yes
- Grok rationale: The paragraph explicitly elevates the enterprise channel solely because of its nearer revenue milestones and treats that proximity as the decisive planning constraint, without performing or referencing any risk-adjusted comparison of the partnership track's longer-term value.
