# Data Plan

## Source
**Kitsune Network Attack Dataset**, Mirsky et al., UCI Machine Learning Repository, CC BY 4.0.
https://archive.ics.uci.edu/dataset/516/kitsune+network+attack+dataset
The same files are also on Kaggle ("Kitsune Network Attack Dataset", uploaded by Yisroel Mirsky), where you can download **individual files** instead of the whole archive.

Each attack has its own folder with three files:
- `<Attack>_dataset.csv`: 115 features per packet, one row per packet, in time order. **This is what we use.**
- `<Attack>_labels.csv`: 0 = benign, 1 = malicious
- `<Attack>_pcap.pcapng`: raw capture, optional (only needed to re-extract features)

**Do not download the full dataset** (about 18 GB). Get only the CSVs for our three attacks.

## Local layout (git-ignored)
Rename folders to have no spaces so the loader finds them:
```
data/raw/Mirai/Mirai_dataset.csv
data/raw/Mirai/Mirai_labels.csv
data/raw/SYN_DoS/SYN_DoS_dataset.csv
data/raw/SYN_DoS/SYN_DoS_labels.csv
data/raw/ARP_MitM/ARP_MitM_dataset.csv
data/raw/ARP_MitM/ARP_MitM_labels.csv
```
The loader matches `*_dataset.csv` and `*_labels.csv`, so the exact file prefix doesn't matter.

## Proof of loading
Step-by-step download instructions: [docs/GETTING_STARTED.md, step 6](https://github.com/GaelA893/IDS-Project/blob/main/docs/GETTING_STARTED.md#step-6-get-the-dataset).

Run `python scripts/check_data.py --save` and paste the output here:

```
(paste output: attack, packets, paper count, features, malicious share)
```

Expected: packet counts equal Table III (764,137 / 2,771,276 / 2,504,267) and 115 features. If not, log it in [[Reproduction-Log]].

## Why we use the feature CSVs rather than the pcaps
The authors provide the exact features used in the paper. Using them (1) removes the slowest step, (2) removes a source of mismatch (our feature extraction vs theirs), and (3) keeps the study focused on the detector. *Stretch goal:* re-extract features from the Mirai pcap with the authors' `FeatureExtractor` and compare.

## Storage rules
- Never commit data (GitHub rejects files > 100 MB). `.gitignore` already blocks `data/`.
- Share the files inside the team via a shared drive link, not git.
