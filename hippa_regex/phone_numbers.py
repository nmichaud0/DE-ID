"""Detector for phone-number-like tokens."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "phone_numbers"
DESCRIPTION = "Telephone numbers, including international and dashed formats."

PATTERNS: list[re.Pattern] = [
    # Compact international style: +41791234567 or 0791234567
    re.compile(r"^\+?\d{7,15}\Z", re.IGNORECASE),
    # Grouped national patterns: (123) 456-7890, 044-123-4567
    re.compile(r"^\(?(?:\d{2,4})\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}\Z", re.IGNORECASE),
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
