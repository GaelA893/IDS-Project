"""Sensitivity runs: how much do the settings the paper never gave change the result?

    python scripts/sensitivity.py              # Mirai (fastest, ~10 min per run, 7 runs ≈ 1 to 1.5 h)
    python scripts/sensitivity.py SYN_DoS      # another attack (slower)

Each run changes ONE setting from the default (m=10, FM grace = 10 % of training,
learning rate 0.1, hidden ratio 0.75). Results get group "sensitivity" and show up
in the second table of scripts/compare_results.py.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
attack = sys.argv[1] if len(sys.argv) > 1 else "Mirai"
extra = sys.argv[2:]
split = ["--train-frac", "0.437"] if attack.lower() == "mirai" else ["--train-packets", "1000000"]

VARIANTS = {
    "U3 feature-map grace 5,000 (authors' demo value)": ["--fm-grace", "5000"],
    "U3 feature-map grace 50,000": ["--fm-grace", "50000"],
    "U4 learning rate 0.01": ["--lr", "0.01"],
    "U4 learning rate 0.5": ["--lr", "0.5"],
    "U5 hidden ratio 0.5": ["--hidden-ratio", "0.5"],
    "U8 authors' demo settings (FM 5,000 + AD 50,000)": ["--fm-grace", "5000", "--ad-grace", "50000"],
    "baseline (all defaults)": [],
}
for label, args in VARIANTS.items():
    cmd = [sys.executable, str(ROOT / "src" / "run_kitnet.py"), "--attack", attack, "--group", "sensitivity",
           *split, *args, *extra]
    print(f"\n>>> {label}\n    {' '.join(cmd[1:])}", flush=True)
    if subprocess.call(cmd) != 0:
        print(f"!! '{label}' failed; continuing with the next one. Note it in your issue.")
print("\nDone. Next: python scripts/compare_results.py")
