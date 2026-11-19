"""Proof that the data loads (Milestone 0 / proposal Section 5).

    python scripts/check_data.py            # all attacks found under data/raw
    python scripts/check_data.py Mirai      # one attack

Prints packet count, feature count and malicious share, and compares packet count to
Table III of the paper. Paste the output into the wiki page Data-Plan.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from data import DATA_ROOT, load_attack  # noqa: E402

targets = json.loads((ROOT / "configs" / "paper_targets.json").read_text())["attacks"]
attacks = sys.argv[1:]
if not attacks and DATA_ROOT.exists():
    attacks = sorted(d.name for d in DATA_ROOT.iterdir() if d.is_dir())
if not attacks:
    sys.exit(f"No attack folders in {DATA_ROOT}. See wiki: Data-Plan.")

print(f"{'attack':<10} {'packets':>10} {'paper':>10} {'feat':>5} {'malicious':>10}")
for att in attacks:
    X, y = load_attack(att)
    paper = targets.get(att, {}).get("packets")
    flag = "" if paper is None or paper == len(X) else "  <-- differs from paper"
    print(f"{att:<10} {len(X):>10,} {paper or '-':>10} {X.shape[1]:>5} {y.mean():>10.2%}{flag}")
