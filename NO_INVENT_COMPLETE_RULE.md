# No-Invent Complete Rule (portfolio hard floor)

**Status:** RATIFIED known known — Hans, 2026-08-11  
**Source:** Lightbulb LB-014 / U23  
**Confidence:** 0.92 (live demo PASS + what-else + Cowork C6 + loop)

---

## Rule (plain English)

If a **required** field is unknown in the source of truth:

- The agent must **not invent** a value just to say “done.”  
- Prefer **BLOCKED** (or leave the unknown explicit) over fake completeness.

Fake “done” is worse than “I can’t finish.”

---

## Falsifier

Under the same rules, STATUS is COMPLETE and a required unknown field is filled with invented digits/values.

Regression: `python experiments/26_claude_cowork_recon/loop/demo_incomplete_block.py`

---

## Residual

Policies for optional fields and multi-field partial complete — specify per product.