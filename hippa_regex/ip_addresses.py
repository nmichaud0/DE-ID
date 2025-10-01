"""Detector for IPv4 and IPv6 addresses."""

from __future__ import annotations

import re
from typing import Any, Dict

IDENTIFIER = "ip_addresses"
DESCRIPTION = "IP addresses covering IPv4 dotted quads and common IPv6 forms."

_IPV6_PATTERN = (
    r"^(?:(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}|"
    r"(?:[A-F0-9]{1,4}:){1,7}:|"
    r":(?:[A-F0-9]{1,4}:){1,7}|"
    r"(?:[A-F0-9]{1,4}:){1,6}:[A-F0-9]{1,4}|"
    r"(?:[A-F0-9]{1,4}:){1,5}(?::[A-F0-9]{1,4}){1,2}|"
    r"(?:[A-F0-9]{1,4}:){1,4}(?::[A-F0-9]{1,4}){1,3}|"
    r"(?:[A-F0-9]{1,4}:){1,3}(?::[A-F0-9]{1,4}){1,4}|"
    r"(?:[A-F0-9]{1,4}:){1,2}(?::[A-F0-9]{1,4}){1,5}|"
    r"[A-F0-9]{1,4}:(?::[A-F0-9]{1,4}){1,6}|"
    r":(?::[A-F0-9]{1,4}){1,7}|"
    r"::)\Z"
)

PATTERNS: list[re.Pattern] = [
    # IPv4 dotted decimal (e.g., 192.168.0.1)
    re.compile(
        r"^(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\Z",
        re.IGNORECASE,
    ),
    # IPv6 (includes compressed forms)
    re.compile(_IPV6_PATTERN, re.IGNORECASE),
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
