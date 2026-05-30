# proximity_to_gtm_framing — caught example (Exp 11b draft idx=0)

Context: a founder slide narrative in a Series A pitch deck

## Paragraph

We've made a deliberate choice to concentrate our near-term engineering resources on the customer-facing workflow layer rather than continuing to deepen the underlying data pipeline infrastructure. The workflow layer is where the contract conversations are happening right now — three enterprise pilots are mid-negotiation, and every feature we ship there translates directly into signed paper. The infrastructure work is real and we'll return to it, but it sits two or three quarters away from any customer-visible impact, which means it sits two or three quarters away from anything we can show a paying customer or close against. Prioritizing the workflow layer isn't just a tactical call; it's the only sequencing that keeps us in the room with the buyers we've spent six months cultivating. When you're this close to revenue, pulling engineers off the work that closes deals to invest in foundational plumbing that won't surface in a demo for another year is a trade we're not willing to make at this stage.

## Detector ground truth

- pattern: `proximity_to_gtm_framing`
- expected verdict: `yes`
- Exp 11b: Grok-4 yes / Gemini 2.5 Pro yes
- Grok rationale: The paragraph explicitly elevates the workflow option solely because of its nearer-term proximity to pilots, contracts, and revenue while dismissing infrastructure work on the basis of its greater distance, without any risk-adjusted comparison of the two paths.
