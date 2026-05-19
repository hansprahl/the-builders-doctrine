"""Assayer — public reference scorer for the upstream Prompt Doctrine.

Pairs with the canonical PROMPT_DOCTRINE.md (this repo, Section IV).
The doctrine describes the rubric; this package implements it.
"""

from .scorer import (
    assay,
    STRUCTURAL_DIMENSIONS,
    STRUCTURAL_FLOOR,
    ANTI_PATTERNS,
    AssayReport,
)

__all__ = [
    "assay",
    "AssayReport",
    "STRUCTURAL_DIMENSIONS",
    "STRUCTURAL_FLOOR",
    "ANTI_PATTERNS",
]

__version__ = "0.1.0"
