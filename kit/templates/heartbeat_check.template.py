"""Health heartbeat for <PRODUCT> — is the system alive and are its hard floors holding?

TEMPLATE (kit/templates/heartbeat_check.template.py). Copy to <product>/tools/heartbeat_check.py,
then REPLACE the product-authored checks below. The harness (this file's structure,
the H/L/G taxonomy, the check()/format_report/_send_alert/main plumbing, the
STATIC_FLOORS vs RUNTIME_CHECKS split) is PORTABLE — copy it verbatim. The CHECKS
are PRODUCT-AUTHORED — every product's floors differ. Do NOT copy another product's
checks; recon this product's own floors first (see the health-heartbeat skill).

This is NOT a doctrine-conformance linter (does code match doc claims — Grok killed
that: a hand-maintained claims manifest just becomes the next stale artifact). It is
a health heartbeat: it checks REAL behavior/wiring, deterministically, and it self-runs
when the system runs. Doc-vs-code drift that breaks nothing is not a health emergency.

Taxonomy — keep these three buckets; author the checks under them:
  HARD FLOOR (H) — "the safety floors are still wired per doctrine." The invariants
                   that, if they regress, betray the product's core promise. STATIC:
                   read committed code + git state. Examples across the portfolio:
                     approval/outreach gate still guards status before executing
                     crisis floor (988) present and above features   [life-safety in TOP]
                     per-user / PII isolation intact (no silent fallback; secrets gitignored)
                     no secret files tracked in git
  LIVENESS (L)  — "the system is actually running." RUNTIME: needs data/network/env.
                   SKIP gracefully when not applicable (shelved, off-deploy, no token).
                     DB reachable + counts above floor
                     scheduled-job / log freshness
                     bot single-poller healthy (getWebhookInfo, read-only)
  HYGIENE (G)   — "nothing is quietly rotting." Mix of static + runtime.
                     approval/draft queue not aging past SLA
                     (secrets → put under HARD FLOOR; it's static + a real safety floor)

Silent when green; Telegrams (or appends <alert log>) when any check goes red.
Exit 0 healthy, 1 degraded.

Usage:
    python -m tools.heartbeat_check            # full board, human-readable
    python -m tools.heartbeat_check --quiet    # silent on healthy, exit-code only
    python -m tools.heartbeat_check --alert    # Telegram/log on degraded
    python -m tools.heartbeat_check --floors   # STATIC hard-floor subset (pre-commit gate)
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"          # <-- adjust to product's data/output dir
ALERT_LOG = DATA_DIR / "heartbeat_alerts.log"


# ── Invariant helpers (PORTABLE — copy verbatim) ─────────────────────────────
def _inv(label: str, ok: bool, message: str, status: str | None = None) -> dict:
    return {"label": label, "status": status or ("OK" if ok else "FAIL"), "message": message}


def _skip(label: str, message: str) -> dict:
    # SKIP is not a failure — the check isn't applicable in this env.
    return {"label": label, "status": "SKIP", "message": message}


def _read(rel: str) -> str:
    p = PROJECT_ROOT / rel
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""


def _git_tracked() -> str:
    return subprocess.run(
        ["git", "ls-files"], cwd=PROJECT_ROOT,
        capture_output=True, text=True, timeout=15,
    ).stdout


# ─────────────────────────────────────────────────────────────────────────────
# PRODUCT-AUTHORED CHECKS — replace everything below with this product's floors.
# Each check() -> dict via _inv/_skip. Keep them deterministic + zero-side-effect.
# Examples are TOP's/Custer's; delete and author your own.
# ─────────────────────────────────────────────────────────────────────────────

# ── H1: approval/outreach gate present in the send paths (STATIC) ────────────
def check_approval_gate() -> dict:
    src = _read("tools/approvals.py")  # <-- product's gate file(s)
    guarded = ('== "pending"' in src) or ('!= "approved"' in src)  # <-- product's guard string
    executes = "execute_approved_action(" in src                    # <-- product's executor
    ok = guarded and executes
    return _inv(
        "H1 approval_gate", ok,
        "Send paths guard approval before executing." if ok else
        "APPROVAL GATE MISSING — the status guard/executor is absent. Irreversible "
        "actions could fire unapproved. See tests/test_approval_gate.py.",
    )


# ── H2: crisis floor hard-coded above features (STATIC) ──────────────────────
def check_crisis_floor() -> dict:
    src = _read("agents/telegram_bot.py")  # <-- product's user-facing entry
    ok = ("988" in src) and ("_is_crisis" in src)
    return _inv(
        "H2 crisis_floor", ok,
        "988 crisis floor present." if ok else
        "CRISIS FLOOR MISSING — 988 / _is_crisis not found. Life-safety floor; must never regress.",
    )


# ── H3: per-user / PII isolation config (STATIC) ─────────────────────────────
def check_pii_isolation() -> dict:
    gi = _read(".gitignore")
    needed = ["data/", "token.json", ".env"]  # <-- product's secret/data surface
    missing = [n for n in needed if n not in gi]
    ok = not missing
    return _inv(
        "H3 pii_isolation", ok,
        "secrets/data gitignored." if ok else
        f"PII ISOLATION DRIFT — not gitignored: {', '.join(missing)}",
    )


# ── G2: no secret files tracked in git (STATIC) ──────────────────────────────
def check_secrets() -> dict:
    try:
        tracked = _git_tracked()
    except Exception as e:
        return _skip("G2 secrets", f"git ls-files failed: {e}")
    bad = [
        line for line in tracked.splitlines()
        if line.endswith((".env", ".db", ".csv", ".xlsx"))
        or os.path.basename(line) in ("token.json", "google_client_secret.json")
    ]
    ok = not bad
    return _inv("G2 secrets", ok, "No secret files tracked in git." if ok else f"TRACKED SECRETS — {bad}")


# ── L-example: runtime liveness, SKIP when not applicable ────────────────────
def check_bot_poller() -> dict:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        return _skip("L3 bot_poller", "TELEGRAM_BOT_TOKEN not set (shelved / local).")
    try:
        url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
        with urllib.request.urlopen(url, timeout=10) as r:
            info = json.loads(r.read()).get("result", {})
    except Exception as e:
        return _inv("L3 bot_poller", False, f"getWebhookInfo failed: {e}")
    pending = info.get("pending_update_count", 0)
    last_err = info.get("last_error_message")
    webhook = info.get("url") or ""
    ok = (not webhook) and (not last_err) and pending < 20
    msg = f"pending={pending}, webhook={'set' if webhook else 'none'}, last_error={last_err or 'none'}"
    return _inv("L3 bot_poller", ok, msg if ok else "BOT UNHEALTHY — " + msg)


# Static code/git floors — meaningful even when shelved. The pre-commit gate runs
# ONLY these (a commit regresses code + git state, not runtime state).
STATIC_FLOORS = [
    check_approval_gate,   # H1
    check_crisis_floor,    # H2
    check_pii_isolation,   # H3
    check_secrets,         # G2
]

# Runtime liveness/hygiene — depend on data/network/env; SKIP cleanly when absent.
RUNTIME_CHECKS = [
    check_bot_poller,      # L3
    # ... add L1 db/data integrity, L2 job freshness, G1 queue-age, etc.
]


# ── Engine + CLI (PORTABLE — copy verbatim) ──────────────────────────────────
def check(floors_only: bool = False):
    """Run checks. Returns (all_healthy, results_list). SKIP never fails the run."""
    checks = STATIC_FLOORS if floors_only else (STATIC_FLOORS + RUNTIME_CHECKS)
    results = []
    all_healthy = True
    for fn in checks:
        try:
            r = fn()
        except Exception as e:
            r = _inv(fn.__name__, False, f"check raised: {e}")
        results.append(r)
        if r["status"] == "FAIL":
            all_healthy = False
    return (all_healthy, results)


def format_report(results: list[dict], floors_only: bool = False) -> str:
    scope = "hard-floor" if floors_only else "full"
    lines = [f"<PRODUCT> health heartbeat ({scope}) — {datetime.now().isoformat(timespec='seconds')}", ""]
    marker = {"OK": "  OK  ", "FAIL": " FAIL ", "SKIP": " SKIP "}
    for r in results:
        lines.append(f"  [{marker.get(r['status'], r['status'])}] {r['label']:18} — {r['message']}")
    return "\n".join(lines)


def _send_alert(message: str) -> None:
    """Alert via Telegram if configured, else append to ALERT_LOG."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    sent = False
    if bot_token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = urllib.parse.urlencode({"chat_id": chat_id, "text": f"[<PRODUCT> heartbeat]\n{message}"}).encode()
            with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=10):
                sent = True
        except Exception as e:
            print(f"[heartbeat_check] Telegram alert failed: {e}", file=sys.stderr)
    try:
        ALERT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(ALERT_LOG, "a") as f:
            f.write(f"\n=== {datetime.now().isoformat(timespec='seconds')} ===\n")
            f.write(f"telegram_sent={sent}\n{message}\n")
    except Exception as e:
        print(f"[heartbeat_check] Alert log write failed: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true", help="No output unless degraded.")
    parser.add_argument("--alert", action="store_true", help="Send Telegram/log on degraded.")
    parser.add_argument("--floors", action="store_true", help="Static hard-floor subset only (pre-commit gate).")
    args = parser.parse_args()

    healthy, results = check(floors_only=args.floors)
    report = format_report(results, floors_only=args.floors)

    if not args.quiet or not healthy:
        print(report)

    if not healthy and args.alert:
        degraded = [r for r in results if r["status"] == "FAIL"]
        summary = f"<PRODUCT> heartbeat degraded: {len(degraded)} check(s) red.\n"
        for r in degraded:
            summary += f"\n• {r['label']}: {r['message']}"
        _send_alert(summary)

    sys.exit(0 if healthy else 1)


if __name__ == "__main__":
    main()
