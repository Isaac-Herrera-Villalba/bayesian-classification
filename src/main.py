#!/usr/bin/env python3

'''
src/report_latex.py
'''

from __future__ import annotations
import sys
from .config import Config
from .loader import load_dataset
from .preprocess import discretize
from .bayes import run_naive_bayes
from .report_latex import render_pdf


def select_columns(df, cfg):
    cols = list(df.columns)
    target = cfg.target_column if cfg.target_column in cols else cols[-1]
    attrs = [c for c in cols if c != target]
    if not cfg.use_all_attributes and cfg.attributes:
        attrs = [c for c in cfg.attributes if c in attrs]
    if len(attrs) < 1:
        raise ValueError("Se requieren >=2 columnas (1 atributo + 1 clase)")
    return attrs, target


def main():
    if len(sys.argv) != 2:
        print("Uso: python -m src.main input.txt")
        sys.exit(1)

    cfg = Config(sys.argv[1])
    df = load_dataset(cfg.dataset, cfg.sheet)
    attrs, target = select_columns(df, cfg)

    if cfg.numeric_mode == "discretize":
        df = discretize(df, attrs, bins=cfg.bins, strategy=cfg.discretize_strategy)

    df = df.astype(str)
    for idx, inst in enumerate(cfg.instances, 1):
        print(f"\\n===== INSTANCIA {idx}: {inst} =====")
        res = run_naive_bayes(df, target, attrs, inst, alpha=cfg.laplace_alpha)
        pred = max(res.posteriors, key=res.posteriors.get)
        print(f">>> Predicción: {pred}")
        if cfg.report_path:
            out = cfg.report_path.replace(".pdf", f"_{idx}.pdf")
            render_pdf(out, df, target, attrs, res.priors, res.cond_tables, inst, res.posteriors)
            print(f"[OK] Reporte: {out}")


if __name__ == "__main__":
    main()

