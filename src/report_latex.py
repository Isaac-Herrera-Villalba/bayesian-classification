#!/usr/bin/env python3

'''
src/report_latex.py
'''

from __future__ import annotations
import subprocess
from pathlib import Path
from typing import Dict, List
import pandas as pd


LATEX_TEMPLATE = r"""
\documentclass[11pt]{article}
\usepackage[margin=2.5cm]{geometry}
\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{siunitx}
\sisetup{output-decimal-marker={,}}
\begin{document}

\section*{Clasificación Bayesiana}

\subsection*{Resumen del dataset}
Filas: %(rows)d, Columnas: %(cols)d\\
Atributos usados: %(attrs)s\\
Columna de clase: %(target)s

\subsection*{Probabilidades a priori}
\begin{tabular}{l r}
\toprule
Clase & $P(y)$ \\
\midrule
%(priors_rows)s
\bottomrule
\end{tabular}

\subsection*{Verosimilitudes $P(A{=}v|y)$}
%(likelihoods_tables)s

\subsection*{Cálculo para la instancia}
Instancia: %(instance)s

%(trace)s

\subsection*{Posteriores normalizados}
\begin{tabular}{l r}
\toprule
Clase & $P(y|\mathbf{x})$ \\
\midrule
%(post_rows)s
\bottomrule
\end{tabular}

\subsection*{Predicción}
La clase predicha es: \textbf{%(pred)s}.

\end{document}
"""


def _tabular_from_df(df: pd.DataFrame, title: str) -> str:
    df = df.copy()
    df.index = [str(i) for i in df.index]
    df.columns = [str(c) for c in df.columns]

    header = " ".join(["l"] + ["r"] * len(df.columns))
    lines = [f"\\subsubsection*{{{title}}}", f"\\begin{{tabular}}{{{header}}}", "\\toprule"]
    lines.append("Clase & " + " & ".join(df.columns) + " \\\\")
    lines.append("\\midrule")
    for idx, row in df.iterrows():
        vals = " & ".join(f"{float(v):.6f}" for v in row.values)
        lines.append(f"{idx} & {vals} \\\\")
    lines.append("\\bottomrule\n\\end{tabular}")
    return "\n".join(lines)


def build_trace(priors: Dict[str, float], conds: Dict[str, pd.DataFrame], instance: Dict[str, str]) -> str:
    """Construye las expresiones del cálculo paso a paso en formato LaTeX."""
    attrs = list(instance.keys())
    lines = []
    for c, p_y in priors.items():
        expr_parts = [f"P({c})={p_y:.4f}"]
        for a in attrs:
            val = str(instance[a])
            prob = conds[a].loc[c, val] if (c in conds[a].index and val in conds[a].columns) else 0.0
            expr_parts.append(f"P({a}={val}|{c})={prob:.4f}")
        lines.append("\\[" + " \\times ".join(expr_parts) + "\\]")
    return "\n".join(lines)


def render_pdf(
    out_pdf: str,
    df: pd.DataFrame,
    target: str,
    attrs: List[str],
    priors: Dict[str, float],
    conds: Dict[str, pd.DataFrame],
    instance: Dict[str, str],
    posteriors: Dict[str, float],
):
    """Genera el archivo .tex y compila a PDF con LaTeX."""
    rows, cols = df.shape
    priors_rows = "\n".join(f"{c} & {p:.6f} \\\\" for c, p in priors.items())
    like_tables = "\n\n".join(_tabular_from_df(conds[a], f"Atributo: {a}") for a in attrs)
    post_rows = "\n".join(f"{c} & {p:.6f} \\\\" for c, p in posteriors.items())
    pred = max(posteriors, key=posteriors.get) if posteriors else "—"

    tex_content = LATEX_TEMPLATE % {
        "rows": rows,
        "cols": cols,
        "attrs": ", ".join(attrs),
        "target": target,
        "priors_rows": priors_rows,
        "likelihoods_tables": like_tables,
        "instance": ", ".join(f"{k}={v}" for k, v in instance.items()),
        "trace": build_trace(priors, conds, instance),
        "post_rows": post_rows,
        "pred": pred,
    }

    out_pdf_path = Path(out_pdf)
    out_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    tex_path = out_pdf_path.with_suffix(".tex")
    tex_path.write_text(tex_content, encoding="utf-8")

    # Compilar PDF con xelatex o pdflatex
    for binname in ("xelatex", "pdflatex"):
        try:
            subprocess.run(
                [binname, "-interaction=nonstopmode", tex_path.name],
                cwd=tex_path.parent,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            return
        except Exception:
            continue

    print(f"[WARN] No se pudo compilar PDF, se dejó el archivo TEX en: {tex_path}")
# ---------------------------------------------------------------------------------

