"""Detector for certificate or license number heuristics."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "certificate_license_numbers"
DESCRIPTION = "Professional certificate or license numbers with mixed characters."

PATTERNS: list[re.Pattern] = [
    # Example: ABC-12345 or RN123456
    re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9-]{6,}\Z", re.IGNORECASE),
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
    # TODO: State-specific license formats may include prefixes or suffixes.
    return {"matched": False, "pattern": None}
