"""Sensitivity runs: how much do the settings the paper never gave change the result?

    python scripts/sensitivity.py              # Mirai (4 runs, a few minutes each)
    python scripts/sensitivity.py SYN_DoS      # another attack (slower, ~30 to 60 min per run)

Each run changes ONE thing from the baseline (the same settings as the main run in
scripts/run_all.py: m = 10, learning rate 0.1, hidden ratio 0.75, and the issue #12 split).
Results get group "sensitivity" and show up in the second table of scripts/compare_results.py.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
attack = sys.argv[1] if len(sys.argv) > 1 else "Mirai"
extra = sys.argv[2:]
is_mirai = "".join(c for c in attack.lower() if c.isalnum()) == "mirai"

# Same split as scripts/run_all.py (issue #12)
if is_mirai:
    split = ["--train-packets", "55000", "--fm-grace", "5000", "--ad-grace", "50000"]
else:
    split = ["--train-packets", "1000000"]

# label -> (extra arguments, replaces the split?)
VARIANTS = {
    "baseline (same settings as the main run)": ([], False),
    "U4 learning rate 0.01 (paper gives no value; code default 0.1)": (["--lr", "0.01"], False),
    "U5 hidden ratio 0.5 (paper gives no value; code default 0.75)": (["--hidden-ratio", "0.5"], False),
}
if is_mirai:
    VARIANTS["U1 old split: first 43.7 % (trains on 212,306 attack packets)"] = (["--train-frac", "0.437"], True)

for label, (args, replaces_split) in VARIANTS.items():
    cmd = [sys.executable, str(ROOT / "src" / "run_kitnet.py"), "--attack", attack, "--group", "sensitivity",
           *([] if replaces_split else split), *args, *extra]
    print(f"\n>>> {label}\n    {' '.join(cmd[1:])}", flush=True)
    if subprocess.call(cmd) != 0:
        print(f"!! '{label}' failed; continuing with the next one. Note it in your issue.")
print("\nDone. Next: python scripts/compare_results.py")
