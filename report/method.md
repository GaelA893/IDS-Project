# 2. Method

**Owner:** Gael

## Data
*Dataset, source and license; the 3 attacks and their packet counts (match Table III); why we use the authors' feature CSVs. Source: wiki Data-Plan, `results/check_data.txt`.*

## Training and test split
*The paper's rule (first 1M packets, §V-A), why it can't apply to Mirai, and our rule per attack (first 55,000 for Mirai, first 1,000,000 for the others). Source: #12, `results/split_check.txt`.*

## Detector settings
*Authors' KitNET code (pinned commit from #5), m = 10 and m = 1, learning rate 0.1, hidden ratio 0.75, grace periods. Note which values the paper doesn't give (Underspecification Register).*

## Metrics and success criterion
*AUC and EER, computed only on test packets; reproduced = both within ±0.02 of Fig. 9. Source: `src/evaluate.py`, #11.*

## Environment
*Python/NumPy versions and the NumPy 2 compatibility fix (R1). Source: Reproduction-Log, #14.*
