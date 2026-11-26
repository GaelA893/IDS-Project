"""Run the official ("main") experiments for one attack: Kitsune with m = 10 and m = 1.

    python scripts/run_all.py Mirai
    python scripts/run_all.py SYN_DoS
    python scripts/run_all.py ARP_MitM

Split rules are fixed here so everyone runs exactly the same thing
(see wiki Underspecification-Register U1/U2):
  * Mirai -> train on the first 55,000 packets (feature-map grace 5,000 + anomaly-detector grace 50,000),
    the authors' own settings for this capture in Kitsune-py. The attack starts at packet 121,621 and never
    stops, so the paper's "first 1M packets" (or 43.7 %) would train on attack traffic and leave no benign
    packets to test on. Decided in issue #12; see results/split_check.txt.
  * every other attack -> train on the first 1,000,000 packets (paper Section V-A)

Each run takes ~10 min (Mirai) to ~40 min (SYN DoS / ARP MitM). Leave the window open.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPLITS = {"mirai": ["--train-packets", "55000", "--fm-grace", "5000", "--ad-grace", "50000"]}
DEFAULT_SPLIT = ["--train-packets", "1000000"]

if len(sys.argv) < 2:
    sys.exit(__doc__)
attack = sys.argv[1]
extra = sys.argv[2:]  # e.g. --limit 50000 for a quick test
split = SPLITS.get("".join(c for c in attack.lower() if c.isalnum()), DEFAULT_SPLIT)

for m in (10, 1):
    cmd = [sys.executable, str(ROOT / "src" / "run_kitnet.py"), "--attack", attack,
           "--m", str(m), "--group", "main", *split, *extra]
    print("\n>>>", " ".join(cmd[1:]), flush=True)
    if subprocess.call(cmd) != 0:
        sys.exit(f"Run failed for m={m}. Copy the error above into your issue and ask in the team chat.")
print("\nDone. Next: python scripts/compare_results.py")
