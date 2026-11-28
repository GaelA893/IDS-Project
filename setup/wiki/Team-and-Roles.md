# Team and Roles

| Role | Name | GitHub | Personality type | Owns |
|---|---|---|---|---|
| **A: Data and infrastructure** | Gael Angulo | @GaelA893 | | Dataset, loading, splits, environment, figures |
| **B: Experiments** | | @L1PsterGram | | Running KitNET, compatibility fixes, sensitivity runs |
| **C: Evaluation and report** | | @meggy | | Paper targets, metrics, comparison, write-up |

Each person fills in their name and personality type (issue #2).

## Plan (each item is a GitHub issue on the Project board)

### Week 1: Setup and data (Fri Nov 20 to Thu Nov 26)
*Thanksgiving is Thu Nov 26; aim to finish Week 1 by Wednesday Nov 25.*
| Role | Task |
|---|---|
| All | Onboarding: clone, install, run tests, open first PR (add yourself to this page) |
| A | Verify repo structure and environment on all three laptops |
| A | Download Mirai, SYN DoS, ARP MitM CSVs; run `check_data.py`; fill [[Data-Plan]] |
| B | Fetch the authors' code, run the smoke test, log every compatibility fix |
| C | Independently re-read Fig. 9 / Table III targets; confirm [[Paper-and-Claim]] |
| C | Set up wiki pages and seed [[Underspecification-Register]] |

### Week 2: Reproduce (Fri Nov 27 to Thu Dec 3)
| Role | Task |
|---|---|
| B | Full runs on Mirai (m=10 and m=1) |
| B | Full runs on SYN DoS and ARP MitM |
| B | Record environment and timing for every run |
| C | Validate metric code; compute Mirai metrics vs paper |
| A | Decide and document the split rule for each attack (U1, U2) |

### Week 3: Analyze and report (Fri Dec 4 to Thu Dec 10)
| Role | Task |
|---|---|
| C | Paper-vs-ours comparison table in [[Results]] |
| B | Sensitivity runs on underspecified settings (grace periods, learning rate, m = 1) |
| A | Figures: ROC curves and RMSE-over-time per attack |
| C | Write [[Results]] discussion: what matched, what didn't, why |
| All | Presentation slides and one rehearsal |

## Working rules
- One issue → one branch (`w1-data-download`) → one pull request with `Closes #N`.
- Someone other than the author reviews and merges.
- Any decision that departs from the paper goes in [[Reproduction-Log]] the same day.
- Short check-ins (15 min) Monday and Thursday → [[Meeting-Notes]].
