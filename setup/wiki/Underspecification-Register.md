# Underspecification Register

Everything the paper doesn't pin down, what we chose, and how sensitive the result is to that choice. This page is a core part of the grade for a reproduction study.

| ID | Gap | Paper says | Our default | How we test it | Status |
|---|---|---|---|---|---|
| U1 | **Training length for Mirai** | "first million packets", but Mirai has only 764,137 packets. Table III gives 52.0 min train / 66.9 min execute | Train on the first 43.7 % of packets (52.0 / 118.9 of capture time, approximated by packet share): `--train-frac 0.437` | Also try a time-based split using packet timestamps from the pcap, if time allows | open |
| U2 | Train split for SYN DoS and ARP MitM | First 1M packets; Table III also gives minutes | First 1,000,000 packets (`--train-packets 1000000`) | Compare with time-based split from Table III | open |
| U3 | Feature-mapping vs anomaly-detector grace periods | Not given | 10 % of training for FM, rest for AD | Try FM = 5k / 50k / 100k | open |
| U4 | Learning rate | Not given as a number | 0.1 (KitNET code default) | Try 0.01 and 0.5 | open |
| U5 | Hidden-layer ratio β | Defined, value not given in experiments | 0.75 (code default) | Try 0.5 | open |
| U6 | Number of features | 115 (§IV) vs n = 198 (§V-C runtime tests) | 115, matching the provided CSVs | None needed; note the inconsistency | resolved |
| U7 | Anomaly threshold φ | Not needed for AUC/EER (threshold-free); needed for TPR@FPR | Report threshold-free metrics as primary | n/a | resolved |
| U8 | Authors' code differs from paper | Demo uses FM 5,000 / AD 50,000 grace | We follow the paper's split, not the demo | Run the demo settings once for comparison | open |
| U9 | Feature source | Paper extracted features in its own C++/Python pipeline | Use the authors' provided CSVs | Stretch: re-extract Mirai from pcap | open |

Add new rows as you find gaps. Link the issue or PR that resolved each one.
