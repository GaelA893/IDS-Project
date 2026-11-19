"""Load the Kitsune Network Attack Dataset feature CSVs and labels.

Expected layout (one folder per attack, file names as distributed on UCI/Kaggle):

    data/raw/<Attack>/<Attack>_dataset.csv   # 115 features per packet, one row per packet
    data/raw/<Attack>/<Attack>_labels.csv    # 0 = benign, 1 = malicious
    data/raw/<Attack>/<Attack>_pcap.pcapng   # optional, not needed when using the CSVs

The CSVs differ slightly in whether they carry a header row or an index column, so
the loader detects and drops those instead of assuming a format.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA_ROOT = Path(__file__).resolve().parents[1] / "data" / "raw"
N_FEATURES = 115  # paper, Section IV-B


def _norm(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())


def find_attack_dir(attack: str, root: Path = DATA_ROOT) -> Path:
    """Find the folder for an attack, ignoring case, spaces and underscores
    (so 'SYN_DoS', 'syn_dos' and 'SYN DoS' all work)."""
    if root.exists():
        for d in root.iterdir():
            if d.is_dir() and _norm(d.name) == _norm(attack):
                return d
    raise FileNotFoundError(
        f"No folder for '{attack}' in {root}. Expected e.g. data/raw/{attack}/ "
        "containing the _dataset.csv(.gz) and _labels.csv(.gz) files. See docs/GETTING_STARTED.md step 6.")


def _find(attack_dir: Path, suffix: str) -> Path:
    # Accept plain or gzipped CSVs (UCI serves .csv.gz; pandas reads both).
    matches = sorted(attack_dir.glob(f"*{suffix}")) + sorted(attack_dir.glob(f"*{suffix}.gz"))
    if not matches:
        raise FileNotFoundError(f"No *{suffix} or *{suffix}.gz in {attack_dir}. See docs/GETTING_STARTED.md step 6.")
    return matches[0]


def _drop_header_and_index(df: pd.DataFrame) -> pd.DataFrame:
    # Header row: first row not numeric.
    first = pd.to_numeric(df.iloc[0], errors="coerce")
    if first.isna().any():
        df = df.iloc[1:].reset_index(drop=True)
    df = df.apply(pd.to_numeric, errors="coerce")
    # Index column: first column equals 0..n-1 (or 1..n).
    col0 = df.iloc[:, 0].to_numpy()
    n = len(col0)
    if n and (np.array_equal(col0, np.arange(n)) or np.array_equal(col0, np.arange(1, n + 1))):
        df = df.iloc[:, 1:]
    return df


def load_attack(attack: str, root: Path = DATA_ROOT, limit: int | None = None):
    """Return (X, y) as float32 features [n_packets, 115] and int labels [n_packets]."""
    attack_dir = find_attack_dir(attack, root)
    X = pd.read_csv(_find(attack_dir, "_dataset.csv"), header=None, nrows=limit)
    X = _drop_header_and_index(X)
    y = pd.read_csv(_find(attack_dir, "_labels.csv"), header=None, nrows=limit)
    y = _drop_header_and_index(y).iloc[:, -1]

    if X.shape[1] != N_FEATURES:
        print(f"[warn] {attack}: expected {N_FEATURES} features, got {X.shape[1]}")
    n = min(len(X), len(y))
    if len(X) != len(y):
        print(f"[warn] {attack}: {len(X)} feature rows vs {len(y)} labels; truncating to {n}")
    return X.iloc[:n].to_numpy(np.float32), y.iloc[:n].to_numpy(np.int8)
