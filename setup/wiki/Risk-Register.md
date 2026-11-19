# Risk Register

| ID | Risk | Likelihood | Impact | Mitigation / fallback | Owner |
|---|---|---|---|---|---|
| K1 | Dataset download is slow or a source goes offline | Medium | High | Download CSVs only (not pcaps); keep one team copy on a shared drive; UCI and Kaggle are both sources | A |
| K2 | Authors' 2018 code breaks on modern Python/NumPy | **Happened** (np.Inf) | Medium | Small shims logged in Reproduction-Log; fall back to `numpy<2` in a venv | B |
| K3 | Full runs too slow on a laptop | Low | Medium | ~1,200 pkt/s measured; worst case ~40 min per run. Run overnight; use `--limit` for debugging | B |
| K4 | Our numbers don't match the paper | Medium | Low (it's a finding) | Work through the Underspecification Register; document the closest settings | C |
| K5 | Thanksgiving week cuts Week 1–2 time | High | Medium | Finish Week 1 by Tue Nov 25; Week 2 runs can go overnight unattended | All |
| K6 | One member unavailable | Medium | High | Every task has a PR and a log entry, so anyone can pick it up; drop ARP MitM before dropping the write-up | All |
| K7 | Memory limits loading 2.7M × 115 floats | Low | Medium | float32 arrays ≈ 1.2 GB; use `--limit` or close other apps | A |

**Scope cut if behind on Dec 3:** keep Mirai + SYN DoS, drop ARP MitM, and say so in Results.
