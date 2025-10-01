"""Typing protocol for HIPAA detector modules."""

from __future__ import annotations

from typing import Protocol, Dict, Any


class Detector(Protocol):
    """Protocol describing the public API exposed by detector modules."""

    IDENTIFIER: str
    DESCRIPTION: str

    def detect(self, word: str) -> bool:
        """Return True when the provided word matches the identifier."""

    def details(self, word: str) -> Dict[str, Any]:
        """Return debugging information for the detection attempt."""
