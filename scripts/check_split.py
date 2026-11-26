"""Issue #12: where does the attack start in each capture, and is our training split clean?

    python scripts/check_split.py            # all attacks in data/raw
    python scripts/check_split.py --save     # also write results/split_check.txt (commit this)

Kitsune learns "normal" from the training portion, so that portion should contain no attack
packets. This prints, per attack, where the first malicious packet is and how many attack
packets our current rule would put into training. It also checks that benign packets are
left for testing: AUC and EER need both classes in the test portion.
Only the labels files are read, so it runs in seconds.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from data import DATA_ROOT, _drop_header_and_index, _find, _norm, find_attack_dir  # noqa: E402

# Must match scripts/run_all.py: Mirai -> first 55,000 packets (issue #12), others -> first 1,000,000
CURRENT = {"mirai": ("packets", 55_000)}
DEFAULT = ("packets", 1_000_000)

save = "--save" in sys.argv
attacks = [a for a in sys.argv[1:] if a != "--save"]
if not attacks:
    attacks = sorted(d.name for d in DATA_ROOT.iterdir() if d.is_dir())

out = []
def say(s=""):
    print(s, flush=True)
    out.append(s)

for att in attacks:
    lab = pd.read_csv(_find(find_attack_dir(att), "_labels.csv"), header=None, dtype=str)
    y = _drop_header_and_index(lab).iloc[:, -1].to_numpy()
    y = (np.nan_to_num(y.astype(float)) > 0).astype(np.int8)
    n = len(y)
    mal = np.flatnonzero(y == 1)
    kind, val = CURRENT.get(_norm(att), DEFAULT)
    split = int(n * val) if kind == "frac" else min(val, n)
    rule = f"first {val:.1%} of packets" if kind == "frac" else f"first {val:,} packets"

    say(f"=== {att} ===")
    say(f"  packets total                 : {n:,}")
    say(f"  malicious packets             : {len(mal):,} ({y.mean():.2%})")
    if len(mal) == 0:
        say("  no malicious packets found (check the labels file)\n")
        continue
    first, last = int(mal[0]), int(mal[-1])
    # how many separate attack 'bursts' (benign -> malicious switches)
    bursts = int(np.sum((y[1:] == 1) & (y[:-1] == 0)) + (y[0] == 1))
    say(f"  first malicious packet index  : {first:,} ({first / n:.1%} of capture)")
    say(f"  last malicious packet index   : {last:,} ({last / n:.1%} of capture)")
    say(f"  attack bursts (benign->attack): {bursts:,}")
    in_train = int(y[:split].sum())
    test = y[split:]
    test_ben, test_mal = int((test == 0).sum()), int((test == 1).sum())
    say(f"  current rule                  : {rule} = packets 0..{split - 1:,}")
    say(f"  attack packets inside training: {in_train:,} ({in_train / split:.2%} of training)")
    say(f"  test portion                  : {len(test):,} packets = {test_ben:,} benign + {test_mal:,} malicious")
    if in_train == 0 and test_ben > 0 and test_mal > 0:
        say("  VERDICT: OK. Training is all benign and the test portion has both classes.")
    elif in_train > 0:
        say(f"  VERDICT: CONTAMINATED. Training would include {in_train:,} attack packets.")
        say(f"           Training must end before packet {first:,} AND leave benign packets for testing.")
    else:
        say("  VERDICT: UNUSABLE. The test portion has only one class, so AUC/EER can't be computed.")
    say()

if save:
    p = ROOT / "results" / "split_check.txt"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Saved {p.relative_to(ROOT)}")
