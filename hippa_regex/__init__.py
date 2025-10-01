"""Dynamic discovery of HIPAA-style regex detectors."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Dict, Any

DISCOVERED: Dict[str, Any] = {}

_package_path = Path(__file__).resolve().parent

for module_info in iter_modules([str(_package_path)]):
    name = module_info.name
    if name in {"__init__", "base"}:
        continue
    module = import_module(f"{__name__}.{name}")
    identifier = getattr(module, "IDENTIFIER", None)
    detect = getattr(module, "detect", None)
    details = getattr(module, "details", None)
    if not identifier or not callable(detect) or not callable(details):
        continue
    DISCOVERED[identifier] = module

__all__ = ["DISCOVERED"]
