"""Detector for U.S. Social Security numbers."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "ssn_numbers"
DESCRIPTION = "United States Social Security numbers with simple invalid-range guards."

PATTERNS: list[re.Pattern] = [
    re.compile(
        r"^(?!000|666|9\d\d)\d{3}[- ]?(?!00)\d{2}[- ]?(?!0000)\d{4}\Z",
        re.IGNORECASE,
    ),
]

_STRIP_CHARS = " \t\n\r\f\v\"'.,;:!?()[]{}<>"


def _clean(word: str) -> str:
    return word.strip(_STRIP_CHARS)


def detect(word: str) -> bool:
    """Return True if `word` matches this identifier by regex (single-token heuristic)."""
    cleaned = _clean(word)
    if not cleaned:
        return False
    return any(pattern.fullmatch(cleaned) for pattern in PATTERNS)


def details(word: str) -> Dict[str, Any]:
    """Return debugging info for the detection attempt."""
    cleaned = _clean(word)
    for pattern in PATTERNS:
        if pattern.fullmatch(cleaned):
            return {"matched": True, "pattern": pattern.pattern}
    return {"matched": False, "pattern": None}
