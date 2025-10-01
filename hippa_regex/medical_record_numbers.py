"""Detector for medical record number heuristics."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "medical_record_numbers"
DESCRIPTION = "Medical record numbers heuristically treated as long digit strings."

PATTERNS: list[re.Pattern] = [
    # Example: 123456 or 000123456789
    re.compile(r"^\d{6,}\Z", re.IGNORECASE),
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
    # TODO: Many institutions use alphanumeric or formatted MRNs.
    return {"matched": False, "pattern": None}
