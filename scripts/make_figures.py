"""Make the report figures from the main runs.

    python scripts/make_figures.py

For every main run that still has its saved scores (results/*_scores.npy) and data, saves:
  figures/<run>_roc.png   ROC curve on the test packets, with AUC and EER in the title
  figures/<run>_rmse.png  anomaly score (RMSE) for every packet, attack packets in red,
                          training period shaded grey (this is the classic Kitsune plot)
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from sklearn.metrics import roc_curve  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from data import load_attack  # noqa: E402

out = ROOT / "figures"
out.mkdir(exist_ok=True)
made = 0
for f in sorted((ROOT / "results").glob("main_*.json")):
    r = json.loads(f.read_text())
    scores_file = f.with_name(f.stem + "_scores.npy")
    if not scores_file.exists():
        print(f"skip {f.name}: scores file not on this computer (only whoever ran it has it)")
        continue
    scores = np.load(scores_file)
    _, y = load_attack(r["attack"], limit=r["args"].get("limit"))
    y = y[: len(scores)]
    n_train = r["n_train"]
    m = r["metrics"]

    fpr, tpr, _ = roc_curve(y[n_train:], scores[n_train:])
    plt.figure(figsize=(5, 5))
    plt.plot(fpr, tpr, lw=2)
    plt.plot([0, 1], [0, 1], "--", color="grey", lw=1)
    plt.xlabel("False positive rate"); plt.ylabel("True positive rate")
    plt.title(f"{r['attack']} (m={r['m']})  AUC={m['auc']:.4f}  EER={m['eer']:.4f}")
    plt.tight_layout(); plt.savefig(out / f"{f.stem}_roc.png", dpi=150); plt.close()

    idx = np.arange(len(scores))
    step = max(1, len(scores) // 200_000)  # thin out points so the plot stays light
    plt.figure(figsize=(10, 4))
    plt.axvspan(0, n_train, color="grey", alpha=0.15, label="training period")
    scored = scores > 0  # KitNET outputs 0 while it is still training
    ben, mal = (y == 0) & scored, (y == 1) & scored
    plt.scatter(idx[ben][::step], scores[ben][::step], s=1, color="tab:blue", label="benign")
    plt.scatter(idx[mal][::step], scores[mal][::step], s=1, color="tab:red", label="malicious")
    plt.yscale("log"); plt.xlabel("Packet number"); plt.ylabel("Anomaly score (RMSE, log)")
    plt.title(f"Kitsune anomaly scores: {r['attack']} (m={r['m']})")
    plt.legend(markerscale=8, loc="upper left"); plt.tight_layout()
    plt.savefig(out / f"{f.stem}_rmse.png", dpi=150); plt.close()
    made += 1
    print(f"saved figures/{f.stem}_roc.png and _rmse.png")

print(f"Done: {made} run(s) plotted." if made else "No main runs with scores found. Run scripts/run_all.py first.")
