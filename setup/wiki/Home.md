# Reproducing Kitsune (NDSS 2018)

IDS capstone reproduction study. We rebuild the evaluation of **Kitsune** (Mirsky et al., NDSS 2018), an online unsupervised network intrusion detector, and check whether its AUC and EER in Fig. 9 hold up on three attacks: **Mirai, SYN DoS, ARP MitM**.

**Timeline:** Fri Nov 20 to Thu Dec 10, 2026 (3 weeks). **Team:** 3 people, roles A/B/C.

**New to the project?** Start with [Getting Started](https://github.com/GaelA893/IDS-Project/blob/main/docs/GETTING_STARTED.md) and [How to Contribute](https://github.com/GaelA893/IDS-Project/blob/main/docs/HOW_TO_CONTRIBUTE.md), then open your issue on the [Issues tab](https://github.com/GaelA893/IDS-Project/issues).

## Pages

| Page | What's in it | Owner |
|---|---|---|
| [[Paper-and-Claim]] | The paper, the exact claim, target numbers, success criteria | C |
| [[Data-Plan]] | Where the data comes from, how to download and load it, row-count checks | A |
| [[Team-and-Roles]] | Who does what, week by week, and working rules | All |
| [[Reproduction-Log]] | Dated log of every run, fix and decision | All |
| [[Underspecification-Register]] | Things the paper leaves out, and how we resolved each | C |
| [[Risk-Register]] | What could sink the project and our fallback | A |
| [[Results]] | Final comparison table, figures and discussion | C |
| [[Meeting-Notes]] | Short notes from each team check-in | rotating |

## Status

| Week | Milestone | Status |
|---|---|---|
| 1 (Nov 20 to 26) | Data loads, authors' code runs, targets extracted | ⬜ |
| 2 (Nov 27 to Dec 3) | Full runs on all 3 attacks, metrics computed | ⬜ |
| 3 (Dec 4 to 10) | Comparison, sensitivity runs, report, presentation | ⬜ |
