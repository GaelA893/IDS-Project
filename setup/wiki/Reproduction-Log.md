# Reproduction Log

Dated, append-only. One entry per run, fix or decision. Newest at the bottom.

**Template:**
```
### YYYY-MM-DD: short title (who)
- What: command / change
- Settings: attack, m, split, fm_grace, ad_grace, lr, git commit, Kitsune-py commit
- Result: AUC / EER (or error)
- Decision / next step:
```

---

### 2026-11-19: Starter pipeline tested on synthetic data (setup)
- What: `src/run_kitnet.py` run end to end on a fake 30,000-packet attack with the authors' KitNET.
- Result: pipeline works; about 1,200 packets/s on one CPU core, so the estimates are Mirai ~10 min, SYN DoS / ARP ~35 to 40 min per run.
- **R1, compatibility fix:** the authors' `KitNET/dA.py` uses `numpy.Inf`, which was removed in NumPy 2.0. `run_kitnet.py` sets `np.Inf = np.inf` before import. No change to the math.
- Next: run on real data (Week 1).
