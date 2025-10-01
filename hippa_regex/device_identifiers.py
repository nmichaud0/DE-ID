"""Detector for device identifier heuristics."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "device_identifiers"
DESCRIPTION = "Medical device identifiers approximated via serial-like tokens."

PATTERNS: list[re.Pattern] = [
    # Example: A12B-34CD or SN12345678
    re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9-]{8,}\Z", re.IGNORECASE),
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
    # TODO: Device identifiers frequently include structured delimiters.
    return {"matched": False, "pattern": None}
