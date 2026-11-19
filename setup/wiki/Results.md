# Results

*Filled in during Week 3.*

## Paper vs ours (m = 10)

| Attack | Paper AUC | Our AUC | Δ | Paper EER | Our EER | Δ | Reproduced (±0.02)? |
|---|---:|---:|---:|---:|---:|---:|:-:|
| Mirai | 0.99919 | | | 0.00317 | | | |
| SYN DoS | 0.95024 | | | 0.07735 | | | |
| ARP MitM | 0.58423 | | | 0.45239 | | | |

Settings used for each row: link the `results/*.json` file and the Reproduction-Log entry.

## Sensitivity to underspecified settings
(table: setting varied → AUC/EER per attack)

## Figures
- ROC curve per attack
- RMSE anomaly score over time, with the attack window shaded

## Discussion
- What reproduced, what didn't
- Most likely causes of differences (link Underspecification Register IDs)
- What the authors should have reported to make this easier
