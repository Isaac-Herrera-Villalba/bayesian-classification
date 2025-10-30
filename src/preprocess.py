#!/usr/bin/env python3

'''
src/preprocess.py
'''

from __future__ import annotations
import pandas as pd


def discretize(df: pd.DataFrame, attrs: list[str], bins: int = 5, strategy: str = "quantile"):
    """Discretiza columnas numéricas según estrategia (quantile o uniform)."""
    df_copy = df.copy()
    for col in attrs:
        if pd.api.types.is_numeric_dtype(df_copy[col]):
            if strategy == "quantile":
                df_copy[col] = pd.qcut(df_copy[col], q=bins, duplicates="drop")
            else:
                df_copy[col] = pd.cut(df_copy[col], bins=bins)
    return df_copy

