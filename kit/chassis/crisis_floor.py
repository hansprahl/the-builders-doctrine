"""
The Builders' Kit — Crisis Floor.

Portable implementation of the safety floor specified in the kit's
CRISIS_TRIGGERS.md template. Lifts the proven shape from TOP's
agents/telegram_bot.py and parameterizes it so any kit-bootstrapped
product can wire it in without reinventing the substring match,
the fixed-response semantics, the admin alert hook, or the WARNING
log line.

Doctrine invariants this module preserves (non-negotiable):

  1. No LLM dependency. The check is `phrase in lowered_text`.
  2. Deterministic. Same input → same output, every time.
  3. Fail-open. The check runs *before* any other logic on the
     inbound surface; nothing upstream can disable it.
  4. The response is fixed text. No model generation, no
     personalization beyond mechanical templating.
  5. Admin alert fires. The machine cannot help; the human might.
  6. WARNING log line lands locally; never transmitted off-host.

This module is sync core. Products that need async (Telegram bots,
async webhooks) wrap the sync calls.

Usage:

    from kit.chassis import CrisisFloor

    def my_admin_alert(event):
        send_sms(my_phone, f"CRISIS [{event.user_id}]: {event.excerpt}")

    floor = CrisisFloor(
        phrases={"kill myself", "want to die", ...},
        response="Stop.\\n...",
        admin_alert=my_admin_alert,
    )

    # On every inbound message, before anything else:
    if floor.is_crisis(message_text):
        reply = floor.handle_crisis(user_id="hans", text=message_text)
        send_to_user(reply)
        return  # short-circuit; no further specialist routing

Or load from a populated CRISIS_TRIGGERS.md:

    floor = CrisisFloor.from_kit_template(
        Path("path/to/your/CRISIS_TRIGGERS.md"),
        admin_alert=my_admin_alert,
    )
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Optional

# NOTE: The KIT:FIELD parser (kit.coverage.parse_template) is imported lazily
# inside from_kit_template() so this chassis module can be vendored or
# packaged independently of the kit's onboarding tooling. The chassis core
# (CrisisFloor + CrisisEvent) has no dependency on coverage.py.

DEFAULT_LOG_MARKER = "CRISIS DETECTED"
DEFAULT_EXCERPT_LEN = 120

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CrisisEvent:
    """A single crisis detection. Passed to the admin_alert callback."""
    user_id: str
    text: str               # the full message that triggered
    excerpt: str            # truncated for logs / alerts
    matched_phrase: str     # which trigger phrase fired (first match)
    timestamp: datetime     # UTC, ISO-serializable
    log_marker: str = DEFAULT_LOG_MARKER

    def log_line(self) -> str:
        return (f"{self.log_marker} [{self.user_id}] "
                f"matched={self.matched_phrase!r}: {self.excerpt}")


class CrisisFloor:
    """
    Parameterizable crisis floor. One instance per product.

    The class is intentionally small. It owns three things:
      1. a frozenset of lowercased phrases,
      2. a fixed response string,
      3. an optional admin_alert callback called on every detection.

    It does NOT own:
      - transport (Telegram, SMS, email — caller's problem)
      - approval queue (responses are unconditional, not approval-gated)
      - LLM routing (the floor runs before any LLM call)
    """

    def __init__(
        self,
        phrases: Iterable[str],
        response: str,
        *,
        admin_alert: Optional[Callable[[CrisisEvent], None]] = None,
        log_marker: str = DEFAULT_LOG_MARKER,
        excerpt_len: int = DEFAULT_EXCERPT_LEN,
        log_handler: Optional[logging.Logger] = None,
    ) -> None:
        # Normalize once at construction so runtime check is O(n) substring.
        self.phrases = frozenset(p.lower().strip() for p in phrases if p.strip())
        if not self.phrases:
            raise ValueError("CrisisFloor requires at least one phrase")
        if not response.strip():
            raise ValueError("CrisisFloor requires a non-empty response")

        self.response = response
        self.admin_alert = admin_alert
        self.log_marker = log_marker
        self.excerpt_len = excerpt_len
        self.logger = log_handler or logger

    # ── Detection ────────────────────────────────────────────────────────────

    def is_crisis(self, text: str) -> bool:
        """True if any trigger phrase appears as a substring in lowered text."""
        if not text:
            return False
        lowered = text.lower()
        return any(phrase in lowered for phrase in self.phrases)

    def matched_phrase(self, text: str) -> Optional[str]:
        """Return the first triggering phrase, or None. For audit/logging."""
        if not text:
            return None
        lowered = text.lower()
        for phrase in self.phrases:
            if phrase in lowered:
                return phrase
        return None

    # ── Response + side effects ──────────────────────────────────────────────

    def handle_crisis(self, user_id: str, text: str) -> str:
        """
        Run the full crisis-floor handler:
          1. Build a CrisisEvent.
          2. Log the WARNING line.
          3. Fire admin_alert if configured.
          4. Return the fixed response string.

        Returns the response string. Caller is responsible for delivering
        it via whatever transport (Telegram, SMS, etc.).

        This method NEVER raises on admin_alert failure — the alert is
        best-effort; the user-facing response and the local log are the
        load-bearing guarantees.
        """
        event = CrisisEvent(
            user_id=user_id,
            text=text,
            excerpt=text[: self.excerpt_len],
            matched_phrase=self.matched_phrase(text) or "<unknown>",
            timestamp=datetime.now(timezone.utc),
            log_marker=self.log_marker,
        )

        self.logger.warning(event.log_line())

        if self.admin_alert is not None:
            try:
                self.admin_alert(event)
            except Exception as exc:
                self.logger.error(
                    f"crisis admin_alert raised; response still delivered: "
                    f"{exc!r}"
                )

        return self.response

    # ── Construction from kit artifacts ──────────────────────────────────────

    @classmethod
    def from_kit_template(
        cls,
        template_path: Path,
        *,
        admin_alert: Optional[Callable[[CrisisEvent], None]] = None,
        **kwargs,
    ) -> "CrisisFloor":
        """
        Build a CrisisFloor from a populated CRISIS_TRIGGERS.md.

        Reads two KIT:FIELD blocks:
          - trigger_phrases: parsed into a phrase list (one per line,
            comments and blanks ignored)
          - response_template: used verbatim as the response string

        Raises ValueError if either field is unpopulated (still a
        bracketed placeholder) or the applicability gate is N/A.
        """
        if not template_path.exists():
            raise FileNotFoundError(f"template not found: {template_path}")

        # Lazy import — only required when loading from a kit template.
        from kit.coverage import parse_template
        fields = {f.name: f for f in parse_template(template_path)}

        # Applicability gate. If the file is N/A, the floor does not apply.
        appl = fields.get("crisis_applicability")
        if appl and ("n/a" in appl.body.lower() or
                     "does not apply" in appl.body.lower()):
            raise ValueError(
                f"{template_path} marks crisis_applicability as N/A; "
                f"this product does not require a crisis floor"
            )

        phrases_field = fields.get("trigger_phrases")
        response_field = fields.get("response_template")

        if not phrases_field or _is_placeholder(phrases_field.body):
            raise ValueError(
                f"trigger_phrases not populated in {template_path}"
            )
        if not response_field or _is_placeholder(response_field.body):
            raise ValueError(
                f"response_template not populated in {template_path}"
            )

        phrases = _extract_phrases(phrases_field.body)
        if not phrases:
            raise ValueError(
                f"trigger_phrases in {template_path} is populated but "
                f"contained no extractable phrases"
            )

        return cls(
            phrases=phrases,
            response=response_field.body.strip(),
            admin_alert=admin_alert,
            **kwargs,
        )


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

_PLACEHOLDER_RE = re.compile(r'^\s*\[.*\]\s*$', re.DOTALL)


def _is_placeholder(body: str) -> bool:
    stripped = body.strip()
    return bool(stripped) and bool(_PLACEHOLDER_RE.match(stripped))


_PHRASE_LINE_RE = re.compile(r'^[\s\-\*\d\.\)]*"?([^"#]+?)"?\s*(#.*)?$')


def _extract_phrases(body: str) -> list[str]:
    """
    Pull trigger phrases out of a populated trigger_phrases field.

    Accepts a few common authoring shapes:
      - one phrase per line, plain
      - bullet-listed (-, *, 1., etc.)
      - quoted ("phrase here")
      - inline comments after `#`

    Section headers (markdown-style ### or paragraphs ending in `:`) are
    skipped. Empty lines skipped. The result is a list of lowercased
    phrases with whitespace collapsed.
    """
    phrases: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        # Skip markdown headers and bracketed instructions.
        if line.startswith("#") or line.startswith("["):
            continue
        # Skip paragraph lead-ins like "Direct ideation triggers:"
        if line.endswith(":") and len(line.split()) <= 6:
            continue

        m = _PHRASE_LINE_RE.match(line)
        if not m:
            continue
        candidate = m.group(1).strip().lower()
        if not candidate or len(candidate) < 3:
            continue
        # Reject anything that's clearly prose, not a phrase entry.
        # Heuristic: too many words = probably explanatory text.
        if len(candidate.split()) > 12:
            continue
        phrases.append(candidate)

    # Dedupe while preserving order.
    seen: set[str] = set()
    deduped: list[str] = []
    for p in phrases:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped
