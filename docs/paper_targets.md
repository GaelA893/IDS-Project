# Kitsune Paper Reproduction Targets

> **Reference Paper:** Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, *"Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection,"* NDSS 2018.

## 1. One-Sentence Reproduction Claim
> "We reproduce the anomaly detection performance of KitNET on the Mirai, SYN DoS, and ARP MitM datasets, targeting the paper's reported ROC-AUC scores of 0.999 (Mirai), 0.999 (SYN DoS), and 0.997 (ARP MitM) under identical 100-feature incremental extraction."

## 2. Target Numbers Recorded from the Paper (Table III)
| Dataset / Attack | Kitsune (Paper) | Baseline (GMM) | Baseline (PCA) | Baseline (IsoForest) | Citation |
| :--- | :--- | :--- | :--- | :--- |
| **Mirai Botnet** | **0.999** | 0.884 | 0.852 | 0.901 | Section V-B, Table III |
| **SYN DoS** | **0.999** | 0.762 | 0.741 | 0.825 | Section V-B, Table III |
| **ARP MitM** | **0.997** | 0.791 | 0.785 | 0.841 | Section V-B, Table III |

## 3. Paper vs. Ours Comparison Table
| Dataset | Paper ROC-AUC | Our Reproduction | Absolute Difference (Δ) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Mirai** | 0.999 | Pending W2 run | Pending | In progress |
| **SYN DoS** | 0.999 | Pending W2 run | Pending | In progress |
| **ARP MitM** | 0.997 | Pending W2 run | Pending | In progress |
