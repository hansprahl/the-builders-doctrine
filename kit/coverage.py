#!/usr/bin/env python3
"""
The Builders' Kit — coverage scoring + interview runner.

Two surfaces:
  * `python kit/coverage.py --score [--target DIR]`
      Scans every kit template in DIR (default: kit/templates/), parses the
      KIT:FIELD blocks, and reports per-template fill rate, overall coverage,
      and the next questions blocking 100%.

  * `python kit/coverage.py --interview SCRIPT [--target DIR]`
      Loads a YAML interview script (e.g. kit/onboarding/questions.yaml),
      walks sections in order, prompts the user for each field, and writes
      answers back into the matching KIT:FIELD blocks of the target template.

  * `python kit/coverage.py --list [--target DIR]`
      Prints the current field inventory and population state. Quick sanity
      check before running the score.

A field is "populated" when its body:
  - is non-empty,
  - is not still the bracketed placeholder text from the template,
  - reaches the field's min_words floor,
  - or is explicitly marked N/A with a reasoning paragraph (only for fields
    where N/A is allowed — conditional fields, applicability-gated fields,
    or fields whose interview marks na_acceptable).

Coverage is the percentage of populated fields out of the total non-skipped
field count. A field that is `required="conditional_on:OTHER"` is only
counted when OTHER itself triggers it.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("error: PyYAML is required. install with `pip install pyyaml`.",
          file=sys.stderr)
    sys.exit(2)


# ──────────────────────────────────────────────────────────────────────────────
# KIT:FIELD parsing
# ──────────────────────────────────────────────────────────────────────────────

FIELD_OPEN_RE = re.compile(
    r'<!--\s*KIT:FIELD\s+(?P<attrs>[^>]+?)\s*-->'
)
FIELD_CLOSE_RE = re.compile(r'<!--\s*KIT:END\s*-->')
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')

PLACEHOLDER_RE = re.compile(r'^\s*\[.*\]\s*$', re.DOTALL)
NA_RE = re.compile(r'\bN/?A\b|\bdoes not apply\b', re.IGNORECASE)


@dataclass
class KitField:
    """One KIT:FIELD block parsed out of a template."""
    name: str
    required: str           # "true" | "false" | "conditional_on:OTHER"
    min_words: int
    body: str
    file_path: Path
    line_start: int         # 1-indexed line of the KIT:FIELD opener
    line_end: int           # 1-indexed line of the KIT:END closer
    raw_attrs: dict = field(default_factory=dict)

    @property
    def is_required(self) -> bool:
        return self.required == "true"

    @property
    def conditional_on(self) -> Optional[str]:
        if self.required.startswith("conditional_on:"):
            return self.required.split(":", 1)[1].strip()
        return None

    @property
    def word_count(self) -> int:
        return len(self.body.split())

    @property
    def is_placeholder(self) -> bool:
        """True if the body still contains the original bracketed instructions."""
        stripped = self.body.strip()
        if not stripped:
            return False  # empty is a different state
        return bool(PLACEHOLDER_RE.match(stripped))

    @property
    def is_empty(self) -> bool:
        return not self.body.strip()

    @property
    def is_na_with_reasoning(self) -> bool:
        """Body marks N/A and includes a reasoning paragraph (>=30 words)."""
        if not NA_RE.search(self.body):
            return False
        return self.word_count >= 30


def parse_template(file_path: Path) -> list[KitField]:
    """Read a markdown file, return every KIT:FIELD block found in document order."""
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Build line-offset index so we can convert char offsets to line numbers.
    line_offsets = [0]
    for line in lines:
        line_offsets.append(line_offsets[-1] + len(line))

    def char_to_line(offset: int) -> int:
        # Binary-ish search; small enough that linear is fine.
        for i, off in enumerate(line_offsets):
            if off > offset:
                return i  # 1-indexed
        return len(lines)

    fields: list[KitField] = []
    pos = 0
    while True:
        m_open = FIELD_OPEN_RE.search(text, pos)
        if not m_open:
            break
        attrs = dict(ATTR_RE.findall(m_open.group("attrs")))
        m_close = FIELD_CLOSE_RE.search(text, m_open.end())
        if not m_close:
            print(
                f"warning: unclosed KIT:FIELD '{attrs.get('name', '?')}' in "
                f"{file_path}",
                file=sys.stderr,
            )
            break
        body = text[m_open.end():m_close.start()].strip("\n")

        try:
            min_words = int(attrs.get("min_words", "0"))
        except ValueError:
            min_words = 0

        fields.append(KitField(
            name=attrs.get("name", "<unnamed>"),
            required=attrs.get("required", "false"),
            min_words=min_words,
            body=body,
            file_path=file_path,
            line_start=char_to_line(m_open.start()),
            line_end=char_to_line(m_close.start()),
            raw_attrs=attrs,
        ))
        pos = m_close.end()

    return fields


# ──────────────────────────────────────────────────────────────────────────────
# Scoring
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class FieldScore:
    field: KitField
    state: str              # "populated" | "empty" | "placeholder" | "below_min" |
                            # "na_acceptable" | "skipped_conditional"
    reason: str             # human-readable

    @property
    def counts(self) -> bool:
        """True if this field counts toward the populated total."""
        return self.state in ("populated", "na_acceptable")

    @property
    def in_denominator(self) -> bool:
        """True if this field contributes to the score denominator."""
        return self.state != "skipped_conditional"


def score_field(f: KitField, all_fields: dict[str, KitField]) -> FieldScore:
    # Conditional gate first: if the gating field is N/A or empty, skip.
    cond = f.conditional_on
    if cond:
        gate = all_fields.get(cond)
        if gate is None:
            return FieldScore(f, "skipped_conditional",
                              f"conditional on missing field {cond!r}")
        # If the gate is empty/placeholder/N/A, this conditional is dormant.
        gate_state = _basic_state(gate)
        if gate_state in ("empty", "placeholder"):
            return FieldScore(
                f, "skipped_conditional",
                f"gating field {cond!r} not populated yet"
            )
        if gate.is_na_with_reasoning:
            return FieldScore(
                f, "skipped_conditional",
                f"gating field {cond!r} marked N/A — this branch does not apply"
            )

    # Order matters: a placeholder whose *instructions* mention N/A is still a
    # placeholder, not a real N/A. Empty and placeholder must short-circuit
    # before N/A can claim the field.
    if f.is_empty:
        return FieldScore(f, "empty", "field is empty")

    if f.is_placeholder:
        return FieldScore(f, "placeholder",
                          "field still contains the template's bracketed instructions")

    # N/A path is acceptable for any populated field that explicitly carries
    # reasoning. Conditional fields and otherwise-required fields can claim it;
    # the interview YAMLs are responsible for not letting builders abuse this.
    if f.is_na_with_reasoning:
        return FieldScore(f, "na_acceptable",
                          "N/A with reasoning — counted as populated")

    if f.min_words and f.word_count < f.min_words:
        return FieldScore(
            f, "below_min",
            f"{f.word_count} words; min_words is {f.min_words}",
        )

    return FieldScore(f, "populated", f"{f.word_count} words")


def _basic_state(f: KitField) -> str:
    if f.is_empty:
        return "empty"
    if f.is_placeholder:
        return "placeholder"
    return "populated"


@dataclass
class TemplateReport:
    file_path: Path
    field_scores: list[FieldScore]

    @property
    def total(self) -> int:
        return sum(1 for s in self.field_scores if s.in_denominator)

    @property
    def populated(self) -> int:
        return sum(1 for s in self.field_scores if s.counts)

    @property
    def fill_rate(self) -> float:
        return (self.populated / self.total * 100.0) if self.total else 100.0


def score_target(target_dir: Path) -> list[TemplateReport]:
    reports: list[TemplateReport] = []
    for md_path in sorted(target_dir.glob("*.md")):
        if md_path.name.lower() == "readme.md":
            continue
        fields = parse_template(md_path)
        if not fields:
            continue
        index = {f.name: f for f in fields}
        scores = [score_field(f, index) for f in fields]
        reports.append(TemplateReport(md_path, scores))
    return reports


# ──────────────────────────────────────────────────────────────────────────────
# Score reporting
# ──────────────────────────────────────────────────────────────────────────────

STATE_GLYPH = {
    "populated":           "[x]",
    "na_acceptable":       "[~]",
    "empty":               "[ ]",
    "placeholder":         "[ ]",
    "below_min":           "[!]",
    "skipped_conditional": "[-]",
}


def print_score_report(reports: list[TemplateReport]) -> None:
    if not reports:
        print("no kit templates found.")
        return

    overall_total = sum(r.total for r in reports)
    overall_populated = sum(r.populated for r in reports)
    overall = (overall_populated / overall_total * 100.0) if overall_total else 100.0

    print(f"\nThe Builders' Kit — coverage report")
    print(f"  scanned {len(reports)} template(s) in "
          f"{reports[0].file_path.parent}\n")

    for r in reports:
        bar = _bar(r.fill_rate)
        print(f"  {r.file_path.name:<26} {bar}  "
              f"{r.populated}/{r.total}  ({r.fill_rate:.0f}%)")

    print()
    print(f"  overall: {overall_populated}/{overall_total}  ({overall:.0f}%)")
    print()

    blockers = [
        s for r in reports for s in r.field_scores
        if s.in_denominator and not s.counts
    ]
    if blockers:
        print(f"next {min(5, len(blockers))} fields blocking 100%:")
        for s in blockers[:5]:
            f = s.field
            loc = f"{f.file_path.name}:{f.line_start}"
            print(f"  • {f.name}  ({loc})  — {s.reason}")
        if len(blockers) > 5:
            print(f"  …and {len(blockers) - 5} more (run --list for the full set)")
        print()


def _bar(pct: float, width: int = 20) -> str:
    filled = int(round(pct / 100.0 * width))
    return "▓" * filled + "░" * (width - filled)


def print_list(reports: list[TemplateReport]) -> None:
    for r in reports:
        print(f"\n# {r.file_path.name}  ({r.populated}/{r.total}  "
              f"{r.fill_rate:.0f}%)")
        for s in r.field_scores:
            f = s.field
            glyph = STATE_GLYPH.get(s.state, "[?]")
            req = (
                "required" if f.is_required
                else f"conditional_on:{f.conditional_on}" if f.conditional_on
                else "optional"
            )
            print(f"  {glyph}  {f.name:<32} "
                  f"min={f.min_words:<3} {req:<20} "
                  f"line {f.line_start:>3}  — {s.reason}")
    print()


# ──────────────────────────────────────────────────────────────────────────────
# Interview runner
# ──────────────────────────────────────────────────────────────────────────────

def run_interview(script_path: Path, target_dir: Path) -> None:
    with script_path.open("r", encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)

    settings = spec.get("settings", {}) or {}
    target_rel = settings.get("default_target", "")
    target_file = (script_path.parent.parent / target_rel) if target_rel \
        else None
    if target_file is None or not target_file.exists():
        # Fall back to scanning target_dir for a file referenced in any section
        target_file = _guess_target_for(spec, target_dir)
    if target_file is None or not target_file.exists():
        print(f"error: cannot resolve target template for "
              f"{script_path.name}", file=sys.stderr)
        sys.exit(1)

    print(f"\nThe Builders' Kit — interview: {script_path.name}")
    print(f"  target: {target_file}")
    print(f"  voice rule: this interview captures *your* words. The runner "
          f"does not paraphrase.")
    print()

    # Prerequisite display only — actual prerequisite enforcement is the
    # scorer's job and is run separately.
    prereqs = spec.get("prerequisites", []) or []
    if prereqs:
        print("prerequisites (verify before continuing):")
        for p in prereqs:
            print(f"  • {p.get('check', p)}")
        ans = input("\nproceed? [y/N]: ").strip().lower()
        if ans != "y":
            print("aborted.")
            return

    sections = spec.get("sections", []) or []
    answers: dict[str, str] = {}
    for section in sections:
        target_field = section.get("target_field")
        if not target_field:
            continue
        title = section.get("title", section.get("id", "(untitled)"))
        body = (section.get("body") or "").strip()
        sub_prompts = section.get("sub_prompts", []) or []

        print("\n" + "─" * 78)
        print(f"  {title}")
        print("─" * 78)
        if body:
            print(body)
            print()
        if sub_prompts:
            print("consider:")
            for p in sub_prompts:
                if isinstance(p, str):
                    print(f"  - {p.strip()}")

        existing_field = _existing_field(target_file, target_field)
        if existing_field and not existing_field.is_placeholder \
                and not existing_field.is_empty:
            print(f"\n(field already populated: "
                  f"{existing_field.word_count} words)")
            choice = input("overwrite? [y/N]: ").strip().lower()
            if choice != "y":
                continue

        print(f"\nenter your answer for {target_field}. "
              f"end with a single line containing only `.`")
        answer = _read_multiline()
        if not answer.strip():
            print("(skipped — empty answer)")
            continue
        answers[target_field] = answer

    if not answers:
        print("\nno answers captured. nothing written.")
        return

    write_answers_to_template(target_file, answers)
    print(f"\nwrote {len(answers)} field(s) to {target_file.name}")
    print()

    # Quick re-score so the user sees the impact.
    reports = score_target(target_dir)
    matching = [r for r in reports if r.file_path == target_file]
    if matching:
        print_score_report(matching)


def _read_multiline() -> str:
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == ".":
            break
        lines.append(line)
    return "\n".join(lines)


def _existing_field(file_path: Path, name: str) -> Optional[KitField]:
    for f in parse_template(file_path):
        if f.name == name:
            return f
    return None


def write_answers_to_template(file_path: Path,
                              answers: dict[str, str]) -> None:
    text = file_path.read_text(encoding="utf-8")
    new_text = text
    for name, answer in answers.items():
        pattern = re.compile(
            r'(<!--\s*KIT:FIELD\s+[^>]*?\bname="' + re.escape(name) +
            r'"[^>]*?-->\n)'
            r'(.*?)'
            r'(\n<!--\s*KIT:END\s*-->)',
            re.DOTALL,
        )
        m = pattern.search(new_text)
        if not m:
            print(f"warning: field {name!r} not found in {file_path.name}",
                  file=sys.stderr)
            continue
        replacement = m.group(1) + answer.rstrip() + "\n" + m.group(3)
        new_text = new_text[:m.start()] + replacement + new_text[m.end():]
    file_path.write_text(new_text, encoding="utf-8")


def _guess_target_for(spec: dict, target_dir: Path) -> Optional[Path]:
    """Best-effort fallback when default_target isn't resolvable."""
    # Look at the first section's hint or fall back to the script name.
    schema = (spec.get("schema") or "").lower()
    name_hint = ""
    if "story" in schema or "questions" in schema:
        name_hint = "STORY.md"
    for candidate in target_dir.glob("*.md"):
        if name_hint and candidate.name == name_hint:
            return candidate
    return None


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

def _default_target_dir() -> Path:
    return Path(__file__).resolve().parent / "templates"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="coverage.py",
        description="The Builders' Kit — coverage scoring + interview runner.",
    )
    parser.add_argument("--score", action="store_true",
                        help="Score every kit template and report coverage.")
    parser.add_argument("--list", action="store_true",
                        help="Print full field inventory and current state.")
    parser.add_argument("--interview", metavar="SCRIPT",
                        help="Run an interview YAML against the target dir.")
    parser.add_argument("--target", metavar="DIR", default=None,
                        help="Templates directory (default: kit/templates/).")
    args = parser.parse_args(argv)

    target_dir = Path(args.target).resolve() if args.target \
        else _default_target_dir()
    if not target_dir.is_dir():
        print(f"error: target directory not found: {target_dir}",
              file=sys.stderr)
        return 1

    if args.interview:
        script_path = Path(args.interview).resolve()
        if not script_path.is_file():
            print(f"error: interview script not found: {script_path}",
                  file=sys.stderr)
            return 1
        run_interview(script_path, target_dir)
        return 0

    reports = score_target(target_dir)

    if args.list:
        print_list(reports)
        return 0

    # Default action is --score.
    print_score_report(reports)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
