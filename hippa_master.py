"""Master dispatcher for HIPAA-style regex detectors over single words."""

from __future__ import annotations

import json
import sys
from typing import Dict, Literal

from hippa_regex import DISCOVERED

Flag = Literal["sensitive", "non-sensitive"]


def classify_word(word: str) -> Dict[str, Flag]:
    """Run `word` through every detector and return a map of identifier to flag."""
    results: Dict[str, Flag] = {}
    for identifier in sorted(DISCOVERED.keys()):
        module = DISCOVERED[identifier]
        try:
            matched = bool(module.detect(word))  # type: ignore[attr-defined]
        except Exception:
            matched = False
        results[identifier] = "sensitive" if matched else "non-sensitive"
    return results


def _run_cli(args: list[str]) -> None:
    if args:
        output = classify_word(args[0])
        print(json.dumps(output, sort_keys=False))
        return

    samples = [
        "john",
        "GENEVA",
        "12/05",
        "+41791234567",
        "john@example.org",
        "123-45-6789",
        "1HGCM82633A004352",
        "192.168.0.1",
        "https://example.com",
    ]
    summary = {token: classify_word(token) for token in samples}
    print(json.dumps(summary, sort_keys=False, indent=2))


if __name__ == "__main__":
    _run_cli(sys.argv[1:])
