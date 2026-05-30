# Clean negative — legitimate sequencing argument

Context: a fundraise narrative one-pager

## Paragraph

We sequence to mid-market first, with enterprise as the planned next
phase, because the two paths carry materially different risk-adjusted
return profiles at our current stage. Enterprise pilots in our category
run 6-9 month procurement cycles with named legal and security reviews
that two reference customers have confirmed take ~14 weeks from
introduction to signed paper. Mid-market deals at our wedge ICP have
closed in our pilot data at a 21-day median. The 4x faster cycle is the
operational reason we sequence mid-market first; it is not the reason
mid-market is *better*. Enterprise will have higher LTV and lower churn
once the wedge is established. The Series A is sized to fund the
mid-market motion to PMF, then to fund the enterprise build-out from
demonstrated traction rather than promise.

## Detector ground truth

- patterns: none
- expected verdicts: all `no`
- Why clean: the sequencing argument names the risk-adjusted return
  trade-off explicitly ("Enterprise will have higher LTV and lower
  churn once the wedge is established"). This is the legitimate-
  sequencing carve-out the `proximity_to_gtm_framing` definition draws.
  Gemini 2.5 Pro independently policed this boundary on Exp 11b
  proximity_to_gtm_framing idx=13 — the dissent that made the
  three-family agreement 59/60 rather than 60/60.
