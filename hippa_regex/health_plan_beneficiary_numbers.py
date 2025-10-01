"""Detector for health plan beneficiary number heuristics."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "health_plan_beneficiary_numbers"
DESCRIPTION = "Health plan beneficiary numbers treated as long mixed tokens."

PATTERNS: list[re.Pattern] = [
    # Example: AB123456789 or 1234567890
    re.compile(r"^(?=.*\d)[A-Za-z0-9]{9,}\Z", re.IGNORECASE),
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
    # TODO: Benefit IDs can include separators and institution-specific prefixes.
    return {"matched": False, "pattern": None}
