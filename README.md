# IDS Capstone: Reproducing Kitsune (NDSS 2018)

We reproduce the detection results of **Kitsune**, an online, unsupervised network intrusion detector:

> Y. Mirsky, T. Doitshman, Y. Elovici, A. Shabtai. *Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection.* NDSS 2018.
> [Paper (PDF)](https://www.ndss-symposium.org/wp-content/uploads/2018/02/ndss2018_03A-3_Mirsky_paper.pdf) · [Authors' code](https://github.com/ymirsky/Kitsune-py) · [Dataset (UCI)](https://archive.ics.uci.edu/dataset/516/kitsune+network+attack+dataset)

## The claim we are testing

Kitsune with ensemble size *m* = 10 reaches the AUC and EER in **Fig. 9** on three attacks:

| Attack | Packets | Paper AUC | Paper EER |
|---|---:|---:|---:|
| Mirai botnet | 764,137 | 0.99919 | 0.00317 |
| SYN DoS | 2,771,276 | 0.95024 | 0.07735 |
| ARP MitM | 2,504,267 | 0.58423 | 0.45239 |

An attack counts as **reproduced** if our AUC and our EER are each within **0.02** of the paper's value.
Targets live in [`configs/paper_targets.json`](configs/paper_targets.json). The *m* = 1 values are recorded there too.

## New here? Start with these
1. **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)**: install everything and run your first test, step by step (Windows and Mac).
2. **[docs/HOW_TO_CONTRIBUTE.md](docs/HOW_TO_CONTRIBUTE.md)**: branch, commit, pull request, review.
3. Open **your issue** on the [Issues tab](https://github.com/GaelA893/IDS-Project/issues) and follow its numbered steps.

## Main commands

```bash
python scripts/check_data.py              # proof the data loads
python scripts/run_all.py Mirai           # official runs (m=10 and m=1) for one attack
python scripts/sensitivity.py             # vary the settings the paper doesn't give
python scripts/compare_results.py         # paper-vs-ours table (Markdown, ready for the wiki)
python scripts/make_figures.py            # ROC and anomaly-score plots into figures/
pytest -q                                 # metric unit tests
```

Each run writes `results/<group>_<attack>_m<m>_...json` (settings, metrics, comparison to the paper) and the raw anomaly scores (`.npy`, not committed).

## Repository layout

```
configs/paper_targets.json   numbers from the paper we compare against
src/data.py                  loads <Attack>_dataset.csv + <Attack>_labels.csv
src/run_kitnet.py            runs the authors' KitNET over the packets, scores the test part
src/evaluate.py              AUC, EER, TPR at FPR = 0 / 0.001, and paper comparison
scripts/check_data.py        data-loading proof for the proposal
scripts/run_all.py           official m=10 and m=1 runs with the agreed split
scripts/sensitivity.py       one-setting-at-a-time variations
scripts/compare_results.py   builds the paper-vs-ours table
scripts/make_figures.py      ROC + anomaly-score figures
docs/                        beginner setup and Git guides
scripts/get_kitsune_code.sh  fetches the reference implementation
tests/                       unit tests for the metrics
setup/bootstrap_github.sh    creates labels, milestones, issues and the project board
data/ external/ results/     git-ignored (data is large, results are regenerated)
```

## Team and plan

Three people, one phase, due **Wed Dec 3, 2026** (presentation day). Each person owns one attack from start to finish
(runs, figures, results section, slides) plus one cross-cutting task, so the work is split evenly. Tasks are GitHub issues.

| Person | Attack | Cross-cutting task | Report sections |
|---|---|---|---|
| Gael (@GaelA893) | Mirai | Training split per attack (#12) | intro, method, results-mirai |
| L1PsterGram (@L1PsterGram) | SYN DoS | Smoke test (#5), sensitivity + environment (#14) | results-syn-dos, sensitivity |
| meggy (@megifrausto-design) | ARP MitM | Paper targets (#6), metrics + comparison (#11) | results-arp-mitm, comparison, discussion |

Checkpoints: **Fri Nov 28** everyone can run a 50k test · **Sun Nov 30** all main results merged ·
**Mon Dec 1** comparison + figures merged · **Tue Dec 2** report + slides done.
If behind, cut in this order: sensitivity to 2 runs → m = 1 runs for SYN DoS / ARP MitM → ARP MitM. Mirai m = 10 is never cut.

Working rules: one branch and one pull request per issue, PR description says `Closes #N`, and someone other than the author
reviews it (Gael reviews L1PsterGram, L1PsterGram reviews meggy, meggy reviews Gael). Commits are our record of effort.

## Known reproduction issues (details in the wiki)

* **Mirai can't use the paper's "first 1M packets" training rule**: it has 764,137 packets and its attack runs from packet 121,621 to the end. We train on its first 55,000 packets (the authors' own Kitsune-py settings), which are all benign and leave benign packets for testing (#12).
* The paper gives no numeric learning rate, grace periods, or threshold; we use the authors' code defaults and test sensitivity.
* The authors' code uses `np.Inf`, which was removed in NumPy 2.0; `run_kitnet.py` adds a one-line shim.

## Licenses and citation

Dataset: CC BY 4.0, cite the paper. KitNET code: MIT, © Yisroel Mirsky; fetched, not vendored.
