# Paper and Claim

## Paper
Y. Mirsky, T. Doitshman, Y. Elovici, A. Shabtai. **"Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection."** Network and Distributed System Security Symposium (NDSS), 2018.
PDF: https://www.ndss-symposium.org/wp-content/uploads/2018/02/ndss2018_03A-3_Mirsky_paper.pdf · DOI: 10.14722/ndss.2018.23204

**What Kitsune does:** extracts 115 incremental traffic statistics per packet (damped windows over 5 time scales), clusters the features into small groups (Feature Mapper), trains one small autoencoder per group plus an output autoencoder (KitNET), and uses reconstruction error (RMSE) as the anomaly score. It trains on benign traffic only, with no labels.

## Exact claim
> We will reproduce Kitsune's detection performance (AUC and EER, Fig. 9) with ensemble size m = 10 on three attacks from the Kitsune dataset: Mirai, SYN DoS and ARP MitM. Following Section V, we train on the start of each capture and evaluate on the remainder. An attack counts as reproduced if our AUC and our EER are each within 0.02 of the paper's values.

## Target numbers (Fig. 9, bar labels for Kitsune)

| Attack | AUC (m=10) | EER (m=10) | AUC (m=1) | EER (m=1) |
|---|---:|---:|---:|---:|
| Mirai | 0.99919 | 0.00317 | 0.99857 | 0.00320 |
| SYN DoS | 0.95024 | 0.07735 | 0.92289 | 0.13557 |
| ARP MitM | 0.58423 | 0.45239 | 0.79499 | 0.23152 |

Read from the bar labels on page 13 of the PDF. **Task (issue W1):** a second team member re-reads these independently and initials here: ______

Note: ARP MitM is a *weak* result in the paper (AUC 0.58 for m=10). Reproducing a weak number is still a reproduction. It's also a good discussion point.

## Experimental setup stated in the paper
| Item | Paper says | Where |
|---|---|---|
| Features | 115 per packet (Section IV-B); experiments on Pi/PC mention n = 198 | §IV, §V-C |
| Train/test | "trained on the first million packets, then executed on the remainder" | §V-A |
| Train/execute time per dataset | Table III (minutes) | Table III |
| Ensemble size | m = 1 and m = 10 | §V-A |
| Metrics | AUC, EER, TPR/FNR at FPR = 0 and 0.001 | §V-B, Fig. 9 |
| Learning rate, grace periods, hidden ratio | **not given as numbers** | (see [[Underspecification-Register]]) |

## Packet counts (Table III)
| Attack | Packets | Train [min] | Execute [min] |
|---|---:|---:|---:|
| Mirai | 764,137 | 52.0 | 66.9 |
| SYN DoS | 2,771,276 | 18.7 | 34.1 |
| ARP MitM | 2,504,267 | 8.05 | 20.1 |
