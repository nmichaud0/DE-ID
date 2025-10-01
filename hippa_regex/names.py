"""Detector stub for personal names (not regex-detectable)."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "names"
DESCRIPTION = "Personal names (not reliably detectable via regex in a single token)."

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
    # TODO: Requires contextual NLP to identify personal names.
    return {"matched": False, "pattern": None}
