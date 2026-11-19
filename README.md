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

## Quick start

```bash
pip install -r requirements.txt
bash scripts/get_kitsune_code.sh          # authors' KitNET into external/ (not committed)
# put the dataset files in data/raw/<Attack>/  (see wiki: Data-Plan)
python scripts/check_data.py              # proof the data loads
python src/run_kitnet.py --attack Mirai --limit 50000 --fm-grace 5000 --ad-grace 20000   # 1-minute smoke test
python src/run_kitnet.py --attack SYN_DoS # full run, paper-style split (first 1M packets train)
pytest -q                                 # metric unit tests
```

Each run writes `results/<attack>_m<m>_train<N>.json` (settings, metrics, comparison to the paper) and the raw anomaly scores.

## Repository layout

```
configs/paper_targets.json   numbers from the paper we compare against
src/data.py                  loads <Attack>_dataset.csv + <Attack>_labels.csv
src/run_kitnet.py            runs the authors' KitNET over the packets, scores the test part
src/evaluate.py              AUC, EER, TPR at FPR = 0 / 0.001, and paper comparison
scripts/check_data.py        data-loading proof for the proposal
scripts/get_kitsune_code.sh  fetches the reference implementation
tests/                       unit tests for the metrics
setup/bootstrap_github.sh    creates labels, milestones, issues and the project board
data/ external/ results/     git-ignored (data is large, results are regenerated)
```

## Team and plan

Three people, three weeks (Nov 20 to Dec 10, 2026). Roles, tasks and deadlines are on the **Project board** and in the wiki page **Team-and-Roles**.

| Role | Owns |
|---|---|
| **A: Data and infrastructure** | dataset download and loading, splits, figures |
| **B: Experiments** | running KitNET, compatibility fixes, sensitivity runs |
| **C: Evaluation and report** | paper targets, metrics, comparison, final write-up |

Working rules: one branch and one pull request per issue, PR description says `Closes #N`, and someone other than the author reviews it. Commits are our record of effort.

## Known reproduction issues (details in the wiki)

* **Mirai has fewer than 1M packets**, but the paper says training uses the first million. Table III instead gives train and execute *minutes*.
* The paper gives no numeric learning rate, grace periods, or threshold; we use the authors' code defaults and test sensitivity.
* The authors' code uses `np.Inf`, which was removed in NumPy 2.0; `run_kitnet.py` adds a one-line shim.

## Licenses and citation

Dataset: CC BY 4.0, cite the paper. KitNET code: MIT, © Yisroel Mirsky; fetched, not vendored.
