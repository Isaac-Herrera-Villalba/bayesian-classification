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
        self._validate_duplicates()

    # ------------------------------------------------------------

    def _parse(self):
        # Lee input.txt e interpreta pares clave=valor e instancias, con soporte para comentarios de bloque y línea.
        current_instance = None
        in_block_comment = False

        with self.path.open("r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()

                # Manejo de comentarios de bloque /* ... */
                if "/*" in line and "*/" in line:
                    # Comentario de una sola línea
                    line = line.split("/*", 1)[0] + line.split("*/", 1)[1]
                elif "/*" in line:
                    in_block_comment = True
                    line = line.split("/*", 1)[0]
                elif "*/" in line:
                    in_block_comment = False
                    line = line.split("*/", 1)[1]
                    # si algo queda después del cierre, seguimos procesando esa parte

                if in_block_comment:
                    continue  # Ignorar líneas dentro del bloque

                # Ignorar líneas vacías o con comentario de línea
                if not line or line.startswith("#"):
                    continue

                # Inicia bloque de instancia
                if line.endswith(":") and line[:-1].strip().upper().startswith("INSTANCE"):
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
                    if k in self.kv:
                        prev = self.kv[k]
                        if not isinstance(prev, list):
                            self.kv[k] = [prev, v]
                        else:
                            self.kv[k].append(v)
                    else:
                        self.kv[k] = v

        if current_instance:
            self.instances.append(current_instance)

    # ------------------------------------------------------------
    def _validate_duplicates(self):
        """Verifica si hay claves críticas duplicadas como DATASET o TARGET_COLUMN."""
        critical = ("DATASET", "TARGET_COLUMN")
        for key in critical:
            val = self.kv.get(key)
            if isinstance(val, list):
                msg = (
                    f"[ERROR] Se detectaron múltiples definiciones de '{key}' en {self.path.name}:\n"
                    f"         {val}\n"
                    f"         Mantén solo una definición válida."
                )
                raise ValueError(msg)

    # ------------------------------------------------------------
    # === Claves globales ===
    @property
    def dataset(self) -> str:
        v = self.kv.get("DATASET", "")
        if isinstance(v, list):
            v = v[-1]  # seguridad extra (nunca debería llegar aquí)
        return v.strip()

    @property
    def sheet(self) -> Optional[str]:
        """
        Devuelve el nombre de la hoja (sheet/hoja), detectando tanto inglés como español.
        Acepta: SHEET, HOJA, SHEETS, HOJAS, sheet_name, pagina, tab.
        """
        keys = {k.strip().upper(): v for k, v in self.kv.items()}
        posibles = ("SHEET", "HOJA", "SHEETS", "HOJAS", "SHEET_NAME", "PAGINA", "TAB")
        for key in posibles:
            if key in keys:
                val = keys[key]
                if isinstance(val, list):
                    val = val[-1]
                return val
        return None

    @property
    def target_column(self) -> Optional[str]:
        v = self.kv.get("TARGET_COLUMN")
        if isinstance(v, list):
            v = v[-1]
        return v

    @property
    def use_all_attributes(self) -> bool:
        return parse_bool(self.kv.get("USE_ALL_ATTRIBUTES", "true"))

    @property
    def attributes(self) -> Optional[List[str]]:
        raw = self.kv.get("ATTRIBUTES")
        if not raw:
            return None
        if isinstance(raw, list):
            raw = raw[-1]
        return [c.strip() for c in raw.split(",") if c.strip()]

    @property
    def laplace_alpha(self) -> float:
        try:
            v = self.kv.get("LAPLACE_ALPHA", "0")
            if isinstance(v, list):
                v = v[-1]
            return float(v)
        except Exception:
            return 0.0

    @property
    def report_path(self) -> Optional[str]:
        v = self.kv.get("REPORT")
        if isinstance(v, list):
            v = v[-1]
        return v

    @property
    def numeric_mode(self) -> str:
        v = self.kv.get("NUMERIC_MODE", "raw")
        if isinstance(v, list):
            v = v[-1]
        return v

    @property
    def bins(self) -> int:
        try:
            v = self.kv.get("BINS", "5")
            if isinstance(v, list):
                v = v[-1]
            return int(v)
        except Exception:
            return 5

    @property
    def discretize_strategy(self) -> str:
        v = self.kv.get("DISCRETIZE_STRATEGY", "quantile")
        if isinstance(v, list):
            v = v[-1]
        return v
# ---------------------------------------------------------------------------------

