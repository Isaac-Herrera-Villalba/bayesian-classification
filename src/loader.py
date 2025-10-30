#!/usr/bin/env python3

'''
src/loader.py
'''

from __future__ import annotations
from pathlib import Path
import pandas as pd


def load_dataset(path: str, sheet: str | None = None) -> pd.DataFrame:
    """
    Carga el dataset desde un archivo CSV, XLSX o ODS.
    Si sheet (o hoja) está definido, lo usa para seleccionar la hoja;
    de lo contrario, carga la primera hoja disponible.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset no encontrado: {path}")

    ext = p.suffix.lower()
    if ext == ".csv":
        df = pd.read_csv(p)

    elif ext in {".xlsx", ".xls"}:
        try:
            if sheet:
                df = pd.read_excel(p, sheet_name=sheet, engine="openpyxl")
            else:
                df = pd.read_excel(p, sheet_name=0, engine="openpyxl")
        except ValueError as e:
            raise ValueError(f"No se encontró la hoja '{sheet}' en el archivo Excel.") from e

    elif ext == ".ods":
        try:
            if sheet:
                df = pd.read_excel(p, sheet_name=sheet, engine="odf")
            else:
                df = pd.read_excel(p, sheet_name=0, engine="odf")
        except ValueError as e:
            raise ValueError(f"No se encontró la hoja '{sheet}' en el archivo ODS.") from e

    else:
        raise ValueError(f"Formato no soportado: {ext}")

    # Convertimos todas las columnas a string por consistencia
    df.columns = [str(c) for c in df.columns]
    return df

