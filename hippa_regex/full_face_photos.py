"""Detector stub for full-face photographic images."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "full_face_photos"
DESCRIPTION = "Full-face photographs cannot be detected from text tokens."

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
    # TODO: Requires image analysis outside the scope of regex heuristics.
    return {"matched": False, "pattern": None}
