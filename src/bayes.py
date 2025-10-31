#!/usr/bin/env python3

'''
src/bayes.py
'''

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import pandas as pd


@dataclass
class BayesResult:
    priors: Dict[str, float]
    cond_tables: Dict[str, pd.DataFrame]
    raw_counts: Dict[str, pd.DataFrame]
    scores: Dict[str, float]
    posteriors: Dict[str, float]


def compute_priors(df: pd.DataFrame, target: str) -> Dict[str, float]:
    total = len(df)
    counts = df[target].value_counts(dropna=False)
    return {str(k): v / total for k, v in counts.items()}


def conditional_tables(df: pd.DataFrame, target: str, attrs: List[str], alpha: float = 0.0):
    cond_probs, raw_counts = {}, {}
    for attr in attrs:
        tmp = df[[attr, target]].astype(str).value_counts().rename("count").reset_index()
        pivot = tmp.pivot(index=target, columns=attr, values="count").fillna(0)
        raw_counts[attr] = pivot.copy()

        if alpha > 0:
            pivot = pivot + alpha
        prob = pivot.div(pivot.sum(axis=1), axis=0).fillna(0.0)
        cond_probs[attr] = prob
    return cond_probs, raw_counts


def evaluate_instance(priors, conds, instance):
    scores = {}
    for c, p_y in priors.items():
        prod = p_y
        for attr, val in instance.items():
            tbl = conds[attr]
            p = float(tbl.loc[c].get(str(val), 0.0)) if c in tbl.index else 0.0
            prod *= p
        scores[c] = prod
    total = sum(scores.values())
    post = {c: (s / total if total > 0 else 0.0) for c, s in scores.items()}
    return scores, post


def run_naive_bayes(df, target, attrs, instance, alpha=0.0) -> BayesResult:
    priors = compute_priors(df, target)
    conds, raw_counts = conditional_tables(df, target, attrs, alpha)
    scores, post = evaluate_instance(priors, conds, instance)
    return BayesResult(priors, conds, raw_counts, scores, post)
# ---------------------------------------------------------------------------------

