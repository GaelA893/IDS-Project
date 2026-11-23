"""Proof that the data loads (Milestone 0 / proposal Section 5).

    python scripts/check_data.py            # all attacks found under data/raw
    python scripts/check_data.py Mirai      # one attack
    python scripts/check_data.py --save     # also write results/check_data.txt (commit this)

Prints packet count, feature count and malicious share, and compares packet count to
Table III of the paper. Paste the output into the wiki page Data-Plan.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from data import DATA_ROOT, _norm, load_attack  # noqa: E402

targets = json.loads((ROOT / "configs" / "paper_targets.json").read_text())["attacks"]
save = "--save" in sys.argv
attacks = [a for a in sys.argv[1:] if a != "--save"]
if not attacks and DATA_ROOT.exists():
    attacks = sorted(d.name for d in DATA_ROOT.iterdir() if d.is_dir())
if not attacks:
    sys.exit(f"No attack folders in {DATA_ROOT}. See wiki: Data-Plan.")

lines = [f"{'attack':<10} {'packets':>10} {'paper':>10} {'feat':>5} {'malicious':>10}"]
print(lines[0])
for att in attacks:
    X, y = load_attack(att)
    key = next((k for k in targets if _norm(k) == _norm(att)), None)
    paper = targets.get(key, {}).get("packets")
    flag = "" if paper is None or paper == len(X) else "  <-- differs from paper"
    lines.append(f"{att:<10} {len(X):>10,} {paper or '-':>10} {X.shape[1]:>5} {y.mean():>10.2%}{flag}")
    print(lines[-1], flush=True)
if save:
    out = ROOT / "results" / "check_data.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved {out.relative_to(ROOT)}")
