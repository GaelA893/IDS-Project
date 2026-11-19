"""Build the paper-vs-ours table from every results/*.json file.

    python scripts/compare_results.py

Prints two Markdown tables (main runs, then sensitivity runs) and saves them to
results/comparison.md. Copy-paste the output straight into the wiki Results page.
Quick test runs (made with --limit) are skipped.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOL = json.loads((ROOT / "configs" / "paper_targets.json").read_text())["_tolerance"]

runs = []
for f in sorted((ROOT / "results").glob("*.json")):
    r = json.loads(f.read_text())
    if r.get("args", {}).get("limit"):
        continue
    runs.append((f.name, r))

lines = []
main = [(n, r) for n, r in runs if r.get("group") == "main"]
lines += ["## Main results: paper vs ours", "",
          f"Reproduced = AUC and EER both within ±{TOL['auc_abs']} of the paper.", "",
          "| Attack | m | Train packets | Paper AUC | Our AUC | Δ AUC | Paper EER | Our EER | Δ EER | Reproduced? | File |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|:-:|---|"]
for name, r in main:
    v = r["metrics"].get("vs_paper")
    if not v:
        continue
    lines.append(f"| {r['attack']} | {r['m']} | {r['n_train']:,} | {v['paper_auc']:.5f} | {v['ours_auc']:.5f} | "
                 f"{v['delta_auc']:+.4f} | {v['paper_eer']:.5f} | {v['ours_eer']:.5f} | {v['delta_eer']:+.4f} | "
                 f"{'✅' if v['reproduced'] else '❌'} | `{name}` |")
if not main:
    lines.append("| *(no main runs yet: run `python scripts/run_all.py <Attack>`)* |||||||||||")

sens = [(n, r) for n, r in runs if r.get("group") == "sensitivity"]
lines += ["", "## Sensitivity runs", "",
          "| Attack | m | FM grace | AD grace | Learning rate | Hidden ratio | AUC | EER | File |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
for name, r in sens:
    a, m = r["args"], r["metrics"]
    lines.append(f"| {r['attack']} | {r['m']} | {r['fm_grace']:,} | {r['ad_grace']:,} | {a['lr']} | {a['hidden_ratio']} | "
                 f"{m['auc']:.5f} | {m['eer']:.5f} | `{name}` |")
if not sens:
    lines.append("| *(none yet: run `python scripts/sensitivity.py`)* |||||||||")

text = "\n".join(lines) + "\n"
print(text)
(ROOT / "results" / "comparison.md").write_text(text, encoding="utf-8")
print("Saved results/comparison.md")
