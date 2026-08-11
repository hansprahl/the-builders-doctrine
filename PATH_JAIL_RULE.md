# Path Jail Rule (portfolio hard floor)

**Status:** RATIFIED known known — Hans, 2026-08-11  
**Source finding:** Lightbulb LB-015  
**Confidence:** 0.92 (sealed probes n=2 + what-else + live demo battery + agent exfil blocked)

---

## Rule (plain English)

If an AI agent can touch files on a machine we care about, it only gets a **box** we chose.

- **Inside the box:** work is allowed.  
- **Outside the box:** read/write must **fail by construction** — not because we asked nicely.  
- Soft prompts (“please don’t open other folders”) are **not** the wall.

---

## Rule (technical)

Agent file tools MUST resolve all paths through a **path jail / mount root**:

1. Relative paths resolve under the mount and must remain under the mount after `resolve()`.  
2. Absolute paths outside the mount are rejected.  
3. `../` traversal that escapes the mount is rejected.  
4. Prefer missing capability over soft policy.

Reference implementation (canonical for now):

- `funkytown/experiments/26_claude_cowork_recon/loop/path_jail.py`  
- Live demo: `.../loop/demo_path_jail.py`  
- Result: `.../artifacts/PATH_JAIL_DEMO_RESULT.md`

---

## Falsifier (re-open if true)

Under portfolio path-jail config, agent tools read or write host paths **outside** the mounted workspace without a deliberate allowlist change.

Regression: re-run `python demo_path_jail.py` (and optionally `--agent`).

---

## Residual (not claimed by this rule)

- Operator production tools not fully migrated yet (bolt-on next)  
- Pay / delete / send walls (separate capability graph — see LB-011 class)  
- Real GUI computer-use  
- Container OS image files (LB-018) — different cell from host mount  

---

## Portfolio products

Apply when building or reviewing file tools in: Operator, Hege/home-ai, Grok Build workflows, Funkytown harnesses, any agent with host FS access.

**Do not ship** host-file agents that only prompt-limit scope.

---

## Process note (also permanent)

Hans clarified 2026-08-11: *“permanent meant for the testing before getting to me.”*

The path-jail **rule** is permanent. The **live-test-before-ratify** gate is also permanent portfolio process for any future KK that reaches Hans (`promote.py` requires `--live-test-report` with PASS).