"""Detector for vehicle identifiers such as VINs."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "vehicle_identifiers"
DESCRIPTION = "Vehicle identifiers focused on 17-character VIN patterns."

PATTERNS: list[re.Pattern] = [
    re.compile(r"^[A-HJ-NPR-Z0-9]{17}\Z", re.IGNORECASE),
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
    # Example: details("1HGCM82633A004352") -> {"matched": True, ...}
    return {"matched": False, "pattern": None}
