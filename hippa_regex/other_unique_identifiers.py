"""Detector stub for miscellaneous unique identifiers."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "other_unique_identifiers"
DESCRIPTION = "Other unique identifiers that require contextual analysis."

PATTERNS: list[re.Pattern] = []

_STRIP_CHARS = " \t\n\r\f\v\"'.,;:!?()[]{}<>"


def _clean(word: str) -> str:
    return word.strip(_STRIP_CHARS)


def detect(word: str) -> bool:
    """Return True if `word` matches this identifier by regex (single-token heuristic)."""
    _clean(word)
    return False


def details(word: str) -> Dict[str, Any]:
    """Return debugging info for the detection attempt."""
    _clean(word)
    # TODO: Define case-specific heuristics for additional identifier categories.
    return {"matched": False, "pattern": None}
