#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
src/main.py
'''

from __future__ import annotations
import sys
import unicodedata
from .config import Config
from .loader import load_dataset
from .preprocess import discretize
from .bayes import run_naive_bayes
from .report_latex import render_pdf


# ------------------------------------------------------------
def normalize_str(s: str) -> str:
    """Normaliza cadenas para comparación (quita tildes, minúsculas, sin espacios extra)."""
    s = str(s).strip().lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def select_columns(df, cfg):
    """Selecciona atributos y columna objetivo."""
    cols = list(df.columns)
    normalized_cols = {normalize_str(c): c for c in cols}

    # Determinar columna objetivo (target)
    if cfg.target_column:
        target_key = normalize_str(cfg.target_column)
        if target_key not in normalized_cols:
            raise ValueError(
                f"La columna objetivo '{cfg.target_column}' no existe en el dataset.\n"
                f"Columnas disponibles: {list(df.columns)}"
            )
        target = normalized_cols[target_key]
    else:
        target = cols[-1]  # Última columna por defecto

    # Determinar atributos
    attrs = [c for c in cols if c != target]
    if not cfg.use_all_attributes and cfg.attributes:
        attrs = [normalized_cols[normalize_str(c)]
                 for c in cfg.attributes if normalize_str(c) in normalized_cols]

    if len(attrs) < 1:
        raise ValueError("Se requieren ≥ 2 columnas (1 atributo + 1 clase)")

    return attrs, target, normalized_cols


# ------------------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("Uso: python -m src.main input.txt")
        sys.exit(1)

    cfg = Config(sys.argv[1])
    df = load_dataset(cfg.dataset, cfg.sheet)
    df = df.astype(str)

    attrs, target, normalized_cols = select_columns(df, cfg)

    # Normalizar valores de instancia según columnas reales
    if cfg.numeric_mode == "discretize":
        df = discretize(df, attrs, bins=cfg.bins, strategy=cfg.discretize_strategy)

    for idx, inst in enumerate(cfg.instances, 1):
        # Normaliza nombres de atributos de la instancia
        inst_norm = {}
        for k, v in inst.items():
            nk = normalize_str(k)
            if nk in normalized_cols:
                inst_norm[normalized_cols[nk]] = v
            else:
                print(f"[WARN] Atributo '{k}' no encontrado en las columnas del dataset, se ignora.")

        print(f"\n===== INSTANCIA {idx}: {inst_norm} =====")

        try:
            res = run_naive_bayes(df, target, attrs, inst_norm, alpha=cfg.laplace_alpha)
        except KeyError as e:
            print(f"[ERROR] Atributo faltante o incorrecto: {e}")
            continue

        pred = max(res.posteriors, key=res.posteriors.get)
        print(f">>> Predicción: {pred}")

        if cfg.report_path:
            out = cfg.report_path.replace(".pdf", f"_{idx}.pdf")
            render_pdf(out, df, target, attrs, res.priors, res.cond_tables, inst_norm, res.posteriors, res.raw_counts)

            print(f"[OK] Reporte: {out}")

    print("[OK] Ejecución completada. Si el .tex fue generado, puedes compilarlo con 'make latex'.")


# ------------------------------------------------------------
if __name__ == "__main__":
    main()
# ---------------------------------------------------------------------------------

