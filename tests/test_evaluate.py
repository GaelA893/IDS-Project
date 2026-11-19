import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from evaluate import all_metrics, eer, tpr_at_fpr  # noqa: E402


def test_perfect_separation():
    y = np.array([0] * 100 + [1] * 10)
    s = np.r_[np.linspace(0, 1, 100), np.linspace(2, 3, 10)]
    m = all_metrics(y, s)
    assert m["auc"] == 1.0 and m["eer"] == 0.0 and m["tpr@fpr=0"] == 1.0


def test_random_scores_near_chance():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 20000)
    s = rng.random(20000)
    m = all_metrics(y, s)
    assert abs(m["auc"] - 0.5) < 0.02 and abs(m["eer"] - 0.5) < 0.02


def test_tpr_at_fpr_bound():
    y = np.array([0, 0, 0, 0, 1, 1])
    s = np.array([0.1, 0.2, 0.3, 0.9, 0.8, 0.95])  # one benign outscores one attack
    assert tpr_at_fpr(y, s, 0.0) == 0.5
    assert tpr_at_fpr(y, s, 0.25) == 1.0
    assert 0 <= eer(y, s) <= 0.5
