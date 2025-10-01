"""Detector for dates excluding standalone years."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "dates_except_year"
DESCRIPTION = "Date expressions without four-digit years (e.g., 12/05, jan)."

PATTERNS: list[re.Pattern] = [
    # Numeric day/month combos: 12/05, 1-2, 03.14
    re.compile(r"^(?:0?[1-9]|[12][0-9]|3[01])[-/.](?:0?[1-9]|1[0-2])\Z", re.IGNORECASE),
    # Month abbreviations excluding common words like 'may'
    re.compile(r"^(jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)\Z", re.IGNORECASE),
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
