"""Metrics used in Kitsune Fig. 9: AUC, EER, and TPR at a fixed FPR (0 and 0.001)."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve

TARGETS = Path(__file__).resolve().parents[1] / "configs" / "paper_targets.json"


def eer(y_true, scores) -> float:
    """Equal error rate: the point on the ROC curve where FPR == FNR (1 - TPR)."""
    fpr, tpr, _ = roc_curve(y_true, scores)
    fnr = 1 - tpr
    i = np.nanargmin(np.abs(fnr - fpr))
    return float((fpr[i] + fnr[i]) / 2)


def tpr_at_fpr(y_true, scores, max_fpr: float) -> float:
    """Highest TPR achievable with a threshold whose FPR <= max_fpr."""
    fpr, tpr, _ = roc_curve(y_true, scores)
    ok = fpr <= max_fpr
    return float(tpr[ok].max()) if ok.any() else 0.0


def all_metrics(y_true, scores) -> dict:
    y_true = np.asarray(y_true)
    scores = np.asarray(scores, dtype=float)
    return {
        "n": int(len(y_true)),
        "malicious_frac": float(y_true.mean()),
        "auc": float(roc_auc_score(y_true, scores)),
        "eer": eer(y_true, scores),
        "tpr@fpr=0": tpr_at_fpr(y_true, scores, 0.0),
        "tpr@fpr=0.001": tpr_at_fpr(y_true, scores, 0.001),
    }


def compare_to_paper(attack: str, metrics: dict, variant: str = "kitsune_m10") -> dict:
    cfg = json.loads(TARGETS.read_text())
    tol = cfg["_tolerance"]
    paper = cfg["attacks"][attack][variant]
    d_auc = metrics["auc"] - paper["auc"]
    d_eer = metrics["eer"] - paper["eer"]
    return {
        "paper_auc": paper["auc"], "ours_auc": metrics["auc"], "delta_auc": d_auc,
        "paper_eer": paper["eer"], "ours_eer": metrics["eer"], "delta_eer": d_eer,
        "reproduced": abs(d_auc) <= tol["auc_abs"] and abs(d_eer) <= tol["eer_abs"],
    }
