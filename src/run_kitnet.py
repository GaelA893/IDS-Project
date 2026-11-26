"""Run the authors' KitNET (anomaly detector) on the pre-extracted Kitsune feature CSVs.

Uses the feature CSVs instead of re-extracting features from the pcap, which skips the
slowest step. The KitNET code itself is the authors' (MIT): run scripts/get_kitsune_code.sh
first so it lives in external/Kitsune-py.

Examples:
    python src/run_kitnet.py --attack Mirai --limit 50000 --fm-grace 5000 --ad-grace 20000   # smoke test
    python src/run_kitnet.py --attack SYN_DoS --train-packets 1000000 --m 10                # paper-style split
    python src/run_kitnet.py --attack Mirai --train-packets 55000 --fm-grace 5000 --ad-grace 50000   # Mirai split (issue #12)
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "external" / "Kitsune-py"))
sys.path.insert(0, str(ROOT / "src"))

from data import load_attack  # noqa: E402
from evaluate import all_metrics, compare_to_paper  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--attack", required=True, help="Folder name under data/raw, e.g. Mirai, SYN_DoS, ARP_MitM")
    p.add_argument("--m", type=int, default=10, help="max autoencoder size (paper uses 10 and 1)")
    split = p.add_mutually_exclusive_group()
    split.add_argument("--train-packets", type=int, default=None, help="train on the first N packets (paper: 1,000,000)")
    split.add_argument("--train-frac", type=float, default=None, help="train on this fraction of packets")
    p.add_argument("--fm-grace", type=int, default=None, help="feature-mapping grace period (default: 10%% of training)")
    p.add_argument("--ad-grace", type=int, default=None, help="anomaly-detector grace period (default: rest of training)")
    p.add_argument("--lr", type=float, default=0.1, help="learning rate (KitNET code default; paper gives no number)")
    p.add_argument("--hidden-ratio", type=float, default=0.75, help="KitNET code default")
    p.add_argument("--limit", type=int, default=None, help="only load the first N packets (for quick tests)")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--group", default="adhoc", help="main | sensitivity | adhoc (used by compare_results.py)")
    p.add_argument("--out", type=Path, default=ROOT / "results")
    a = p.parse_args()

    # Compatibility shim: the 2018 KitNET code uses np.Inf, removed in NumPy 2.0.
    # Logged as R1 in the wiki Reproduction-Log. Does not change any math.
    if not hasattr(np, "Inf"):
        np.Inf = np.inf
    try:
        from KitNET.KitNET import KitNET
    except ImportError:
        sys.exit("KitNET not found. Run: git clone --depth 1 https://github.com/ymirsky/Kitsune-py external/Kitsune-py  (docs/GETTING_STARTED.md step 7)")

    np.random.seed(a.seed)
    X, y = load_attack(a.attack, limit=a.limit)
    n = len(X)

    if a.train_packets is not None:
        n_train = min(a.train_packets, n)
    elif a.train_frac is not None:
        n_train = int(n * a.train_frac)
    else:
        n_train = min(1_000_000, n)
    if n_train >= n:
        sys.exit(f"Training split ({n_train}) leaves no test packets out of {n}. "
                 "Use --train-frac (see wiki: Underspecification-Register, U1).")

    fm = a.fm_grace if a.fm_grace is not None else max(1, n_train // 10)
    if fm >= n_train:
        sys.exit(f"--fm-grace ({fm:,}) must be smaller than the training split ({n_train:,}).")
    ad = a.ad_grace if a.ad_grace is not None else n_train - fm
    if fm + ad != n_train:
        print(f"[note] fm_grace + ad_grace = {fm + ad}, training split = {n_train}")

    print(f"{a.attack}: {n:,} packets | train {n_train:,} (FM {fm:,} + AD {ad:,}) | test {n - n_train:,} | m={a.m}")
    det = KitNET(X.shape[1], a.m, fm, ad, a.lr, a.hidden_ratio)

    scores = np.zeros(n, dtype=np.float64)
    t0 = time.time()
    for i in range(n):
        scores[i] = det.process(X[i])
        if i and i % 100_000 == 0:
            rate = i / (time.time() - t0)
            print(f"  {i:,}/{n:,} packets  ({rate:,.0f} pkt/s)")
    elapsed = time.time() - t0

    test_y, test_s = y[n_train:], scores[n_train:]
    metrics = all_metrics(test_y, test_s)
    try:
        metrics["vs_paper"] = compare_to_paper(a.attack, metrics, f"kitsune_m{a.m}")
    except (KeyError, StopIteration):
        pass

    safe = "".join(c if c.isalnum() else "_" for c in a.attack)
    tag = (f"{a.group}_{safe}_m{a.m}_train{n_train}_fm{fm}_ad{ad}_lr{a.lr}_hr{a.hidden_ratio}"
           + (f"_limit{a.limit}" if a.limit else ""))
    a.out.mkdir(parents=True, exist_ok=True)
    np.save(a.out / f"{tag}_scores.npy", scores)
    run = {"tag": tag, "group": a.group, "attack": a.attack, "m": a.m, "args": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(a).items()},
           "n_packets": n, "n_train": n_train, "fm_grace": fm, "ad_grace": ad,
           "seconds": round(elapsed, 1), "python": platform.python_version(), "metrics": metrics}
    (a.out / f"{tag}.json").write_text(json.dumps(run, indent=2))
    print(json.dumps(metrics, indent=2))
    print(f"Saved results/{tag}.json")


if __name__ == "__main__":
    main()
