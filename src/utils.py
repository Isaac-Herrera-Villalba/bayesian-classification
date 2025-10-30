#!/usr/bin/env python3

'''
src/utils.py
'''

from __future__ import annotations
from typing import Dict, Any


def normalize_colnames(cols):
    """Devuelve nombres tal cual (sin modificar)."""
    return list(cols)


def parse_bool(s: str) -> bool:
    return str(s).strip().lower() in {"1", "true", "yes", "y", "t", "si", "sí"}


def dotted(d: Dict[str, Any]) -> str:
    """Formatea un dict como 'k=v, k=v'."""
    return ", ".join(f"{k}={v}" for k, v in d.items())

