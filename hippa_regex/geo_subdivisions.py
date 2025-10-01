"""Detector for limited geographic subdivisions such as postal codes."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "geo_subdivisions"
DESCRIPTION = "Geographic subdivisions detectable via postal code heuristics."

PATTERNS: list[re.Pattern] = [
    # US ZIP codes (12345 or 12345-6789)
    re.compile(r"^\d{5}(?:-\d{4})?\Z", re.IGNORECASE),
    # Swiss-style 4-digit postal codes avoiding leading zero.
    re.compile(r"^[1-9]\d{3}\Z", re.IGNORECASE),
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
    # TODO: City and street names require richer context than a single token.
    return {"matched": False, "pattern": None}
