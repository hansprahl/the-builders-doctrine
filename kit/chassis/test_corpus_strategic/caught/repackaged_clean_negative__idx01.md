# repackaged_clean_negative — caught example (Exp 11b draft idx=1)

Context: an MDMP mission analysis rationale section

## Paragraph

During the mission analysis phase, the logistics-forward basing option (Course of Action Bravo) was evaluated against four viability criteria and returned unfavorable on three: projected sustainment costs exceeded threshold by 34%, the single line of communication created an unacceptable culmination risk under moderate threat pressure, and the facility acquisition timeline conflicted with the operational window by an estimated 11 weeks. These findings are noted. That said, given the fluidity in the operational environment and the possibility that threat assumptions may shift, the staff recommends retaining COA Bravo as a portfolio option — specifically, as a hedge against the scenario where COA Alpha's host-nation basing agreements fall through in the final coordination phase. The intent is not to resource Bravo at this stage but to preserve decision space and avoid foreclosing what may prove to be the only fallback available if primary assumptions erode. Commanders should treat it as a low-cost optionality hold rather than a committed line of effort, with a named decision point at D-21 to reassess.

## Detector ground truth

- pattern: `repackaged_clean_negative`
- expected verdict: `yes`
- Exp 11b: Grok-4 yes / Gemini 2.5 Pro yes
- Grok rationale: The paragraph explicitly lists three quantified kill signals from the prior analysis, then immediately re-frames the same COA as a retained 'portfolio option' and 'hedge' without any refutation or mitigation of those signals, which is the exact pattern.
