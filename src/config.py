#!/usr/bin/env python3

'''
src/config.py
'''

from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Optional
from .utils import parse_bool


class Config:
    def __init__(self, path: str):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"No se encontró el archivo de entrada: {path}")

        self.kv: Dict[str, str] = {}
        self.instances: List[Dict[str, str]] = []
        self._parse()

    def _parse(self):
        """Lee input.txt e interpreta pares clave=valor e instancias."""
        current_instance = None
        with self.path.open("r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue

                if line.endswith(":") and line[:-1].strip().upper().startswith("INSTANCE"):
                    # Nueva instancia
                    if current_instance is not None:
                        self.instances.append(current_instance)
                    current_instance = {}
                    continue

                if "=" not in line:
                    continue

                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip()

                if current_instance is not None:
                    current_instance[k] = v
                else:
                    self.kv[k] = v

        if current_instance:
            self.instances.append(current_instance)

    # === Claves globales ===
    @property
    def dataset(self) -> str:
        return self.kv.get("DATASET", "").strip()

    @property
    def sheet(self) -> Optional[str]:
        """
        Devuelve el nombre de la hoja (sheet/hoja), detectando tanto inglés como español.
        Acepta: SHEET, HOJA, SHEETS, HOJAS, sheet_name, pagina, tab.
        """
        # Normaliza todas las claves a mayúsculas para búsqueda flexible
        keys = {k.strip().upper(): v for k, v in self.kv.items()}
        posibles = ("SHEET", "HOJA", "SHEETS", "HOJAS", "SHEET_NAME", "PAGINA", "TAB")
        for key in posibles:
            if key in keys:
                return keys[key]
        return None

    @property
    def target_column(self) -> Optional[str]:
        return self.kv.get("TARGET_COLUMN")

    @property
    def use_all_attributes(self) -> bool:
        return parse_bool(self.kv.get("USE_ALL_ATTRIBUTES", "true"))

    @property
    def attributes(self) -> Optional[List[str]]:
        raw = self.kv.get("ATTRIBUTES")
        if not raw:
            return None
        return [c.strip() for c in raw.split(",") if c.strip()]

    @property
    def laplace_alpha(self) -> float:
        try:
            return float(self.kv.get("LAPLACE_ALPHA", "0"))
        except Exception:
            return 0.0

    @property
    def report_path(self) -> Optional[str]:
        return self.kv.get("REPORT")

    @property
    def numeric_mode(self) -> str:
        return self.kv.get("NUMERIC_MODE", "raw")

    @property
    def bins(self) -> int:
        try:
            return int(self.kv.get("BINS", "5"))
        except Exception:
            return 5

    @property
    def discretize_strategy(self) -> str:
        return self.kv.get("DISCRETIZE_STRATEGY", "quantile")

