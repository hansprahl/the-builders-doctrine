# repackaged_clean_negative — caught example (Exp 11b draft idx=0)

Context: a founder slide narrative in a Series A pitch deck

## Paragraph

Our go-to-market sequencing prioritizes the mid-market SaaS vertical, where we have three signed LOIs and a clear wedge into procurement workflows. We are also retaining the enterprise direct channel as a portfolio option within our broader distribution architecture — it surfaces periodically in investor conversations and represents a ceiling on ACV expansion that we want to preserve optionality around. To be clear, our Q3 channel analysis flagged enterprise direct as non-viable at current headcount, citing an 18-month average sales cycle, CAC that runs 4.1x our mid-market baseline, and a named dependency on a six-person field team we have not yet hired; those findings informed our decision to concentrate resources on the mid-market wedge through at least Series B. That said, given the macro environment and the conversations we are having with two Fortune 500 procurement leads, we believe it is prudent to hold enterprise direct as a live strategic option rather than formally closing it — treating it as asymmetric upside that does not require near-term capital commitment and that a larger balance sheet post-Series A could activate on an opportunistic basis.

## Detector ground truth

- pattern: `repackaged_clean_negative`
- expected verdict: `yes`
- Exp 11b: Grok-4 yes / Gemini 2.5 Pro yes
- Grok rationale: The paragraph explicitly cites the prior Q3 analysis's named kill signals (18-month cycle, 4.1x CAC, unfilled six-person team) then immediately reframes the same channel as a retained 'portfolio option' and 'live strategic option' with 'asymmetric upside' without any refutation, matching the pattern definition exactly.
