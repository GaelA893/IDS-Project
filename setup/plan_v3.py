"""Apply the Nov 25 consolidated plan (one phase, due Wed Dec 3) to GitHub issues and milestones.

    python setup/plan_v3.py            # dry run: print what would change
    python setup/plan_v3.py --apply    # do it (needs gh, logged in with write access)

Undo with setup/backups/restore_v3.py (uses the snapshot taken before this ran).
Created issue numbers are written to setup/backups/v3-applied.json.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue_bodies import BLOB, GS, HC, WIKI, body  # noqa: E402

ACT = ("*(open a terminal, `cd ~/Documents/IDS-Project`, and activate the environment: Windows PowerShell "
       "`.\\.venv\\Scripts\\Activate.ps1` (Git Bash: `source .venv/Scripts/activate`), Mac `source .venv/bin/activate`)*")

REPO = "GaelA893/IDS-Project"
APPLY = "--apply" in sys.argv
APPLIED = Path(__file__).resolve().parent / "backups" / "v3-applied.json"
GAEL, L1P, MEG = "GaelA893", "L1PsterGram", "megifrausto-design"
PHASE1, PHASE2, WEEK3 = 1, 2, 3  # milestone numbers


def api(method, path, payload=None):
    print(f"{'APPLY' if APPLY else 'dry-run'}: {method} {path}" + (f"  {payload.get('title', '')}" if payload else ""))
    if not APPLY:
        return {"number": f"<new:{payload.get('title', '')[:20]}>"} if method == "POST" and path == "issues" else {}
    out = subprocess.run(["gh", "api", "-X", method, f"repos/{REPO}/{path}", "--input", "-"],
                         input=json.dumps(payload or {}), text=True, check=True, capture_output=True).stdout
    return json.loads(out) if out.strip() else {}


def finish(n, text):
    return text.replace("{n}", str(n))


# ---------------------------------------------------------------- new issues
def attack_issue(name, slug, cmd_name, owner, reviewer, runtime, extra_first, overnight):
    sleep = ("\n2. Plug the laptop in and turn off sleep (Windows: Settings → System → Power → Sleep: Never; "
             "Mac: System Settings → Battery/Energy). Start it in the evening; it runs overnight.") if overnight else \
            "\n2. Plug the laptop in. Each run takes a few minutes."
    return body(
        f"Run the official experiments on **{name}** (Kitsune m = 10 and m = 1), make its two figures, and write its results section. "
        f"This is the core of our reproduction for {name}.",
        f"~2 h of your time ({runtime} of computer time)",
        f"{extra_first}; PR #28 merged (lower-memory loader)",
        f"""
**Part 1: results (by Sun Nov 30)**
1. Get the latest code {ACT}:
   ```
   git checkout main
   git pull
   git checkout -b {slug}-results
   ```{sleep}
3. Run both official runs:
   ```
   python scripts/run_all.py {cmd_name}
   ```
   It prints progress every 100,000 packets and ends with `Done.` You should see two lines starting `Saved results/main_...`.
4. See how you did against the paper: `python scripts/compare_results.py`
5. Make your figures: `python scripts/make_figures.py`. Open the two new PNGs per run in `figures/`; the red (attack) points should mostly sit above the blue ones after the grey training period.
6. Add a Reproduction-Log entry on the wiki: date, command, AUC/EER for m = 10 and m = 1, run time (the `"seconds"` value in each results JSON).
7. Save to GitHub:
   ```
   git add results/*.json results/comparison.md figures
   git commit -m "{name} main runs and figures (#{{n}})"
   git push -u origin {slug}-results
   ```
   Open the pull request with **`Part of #{{n}}`** (not Closes yet) and request **{reviewer}** as reviewer.

**Part 2: write-up (by Tue Dec 2)**
8. `git checkout main`, `git pull`, `git checkout -b {slug}-writeup`.
9. Open `report/results-{slug}.md` and replace the *italic prompts* with your own text: your two table rows, the two figures, and 3 to 5 sentences on what you see.
10. Commit, push, pull request with `Closes #{{n}}`.
""",
        f"- Two `results/main_{cmd_name.split('_')[0]}*` JSON files and their figures are merged (Sun).\n"
        f"- `report/results-{slug}.md` is written and merged (Tue).",
        "- `MemoryError` or the computer freezes: close other apps and rerun; make sure PR #28 is merged (`git pull`).\n"
        "- A run stopped halfway: just rerun the same command; it overwrites that run's files.",
        reviewer=reviewer,
    )


NEW = [
    dict(key="mirai", title="[P2] Mirai: main runs, figures, results section", assignees=[GAEL],
         labels=["role:A", "experiment"],
         body=attack_issue("Mirai", "mirai", "Mirai", GAEL, "meggy", "a few minutes per run",
                           "#27 merged (Mirai trains on its first 55,000 packets)", False)),
    dict(key="syn", title="[P2] SYN DoS: main runs, figures, results section", assignees=[L1P],
         labels=["role:B", "experiment"],
         body=attack_issue("SYN DoS", "syn-dos", "SYN_DoS", L1P, "Gael", "~1 to 2 h per run",
                           "#5 (code runs) and the SYN DoS files in `data/raw/SYN_DoS/`", True)),
    dict(key="arp", title="[P2] ARP MitM: main runs, figures, results section", assignees=[MEG],
         labels=["role:C", "experiment"],
         body=attack_issue("ARP MitM", "arp-mitm", "ARP_MitM", MEG, "L1PsterGram", "~1 to 2 h per run",
                           "#5 says the code runs, and the ARP MitM files in `data/raw/ARP_MitM/`", True)),
    dict(key="intro", title="[P2] Report: introduction and method", assignees=[GAEL], labels=["role:A", "docs"],
         body=body(
             "Write the two report sections that explain what we reproduced and exactly how, so a reader could repeat it.",
             "2 to 3 h", "#12 decided (it's part of the method); ideally #6 confirmed",
             f"""
1. `git checkout main`, `git pull`, `git checkout -b report-intro-method`.
2. Open `report/intro.md` (~300 words) and `report/method.md` (~400 to 500 words). Each has *italic prompts* saying what goes where; replace them with your own text.
3. Sources you already have: the paper (§I to V), the wiki [Data-Plan]({WIKI}/Data-Plan) and [Reproduction-Log]({WIKI}/Reproduction-Log), `results/check_data.txt`, `results/split_check.txt`, #12, `src/evaluate.py`.
4. Cite the paper as "Mirsky et al. (2018)" and refer to our issues and PRs by number.
5. Commit both files, push, pull request with `Closes #{{n}}`, reviewer **meggy**. Target: **Mon Dec 1** (meggy's discussion builds on your method).
""",
             "- `report/intro.md` and `report/method.md` are written and merged.",
             reviewer="meggy")),
]

# ---------------------------------------------------------------- rewritten issues
EDITS = {
    11: dict(title="[P2] Metric check and paper-vs-ours comparison table", milestone=PHASE2, body=body(
        "Double-check that our scoring measures what the paper measures, then build the headline table: did each of the 6 numbers reproduce?",
        "1.5 h", "all three attack issues have results merged (Sun Nov 30 checkpoint)",
        f"""
**Metric check (any time)**
1. `git checkout main`, `git pull`, `git checkout -b metrics-comparison`.
2. Read `src/evaluate.py` (short). **AUC** = how well scores rank attacks above normal traffic (1.0 perfect, 0.5 coin-flip). **EER** = the error rate where false alarms equal missed attacks (0 perfect, 0.5 coin-flip).
3. Open `tests/test_evaluate.py` and paste this at the bottom:
   ```python
   def test_hand_example():
       # 4 normal packets, 4 attacks; exactly one normal packet scores above one attack
       y = np.array([0, 0, 0, 0, 1, 1, 1, 1])
       s = np.array([1, 2, 3, 6, 5, 7, 8, 9])
       m = all_metrics(y, s)
       assert abs(m["auc"] - 15 / 16) < 1e-9   # 15 of the 16 (normal, attack) pairs ranked correctly
       assert abs(m["eer"] - 0.25) < 1e-9      # at threshold 6: 1 of 4 normals flagged, 1 of 4 attacks missed
   ```
   Run `pytest -q` {ACT}. You should see `4 passed`.

**Comparison table (Mon Dec 1, after all results are merged)**
4. `git pull` to get everyone's results.
5. Open any `results/main_*.json`. Check that `metrics.n` equals `n_packets − n_train` (only test packets are scored). Write the three numbers in a comment here.
6. `python scripts/compare_results.py`. Copy the **Main results** table into `report/comparison.md` and add 2 to 3 sentences: how many of the 6 rows reproduced, which was closest, which was furthest.
7. Commit (`tests`, `report/comparison.md`, `results/comparison.md`), push, pull request with `Closes #{{n}}`, reviewer **L1PsterGram**.
""",
        "- `pytest -q` shows 4 passed on `main`.\n- `report/comparison.md` has all 6 rows with ✅/❌ and your sentences.",
        reviewer="L1PsterGram")),
    14: dict(title="[P2] Sensitivity runs (Mirai) and environment record", milestone=PHASE2, body=body(
        "Measure how much the settings the paper never gave us change the result, and record the computer and software behind our numbers.",
        "~1.5 h of your time (4 short Mirai runs)", "PR #29 merged (new sensitivity runs) and the Mirai files in `data/raw/Mirai/` (shared drive)",
        f"""
**Sensitivity (Sun Nov 30 or Mon Dec 1)**
1. `git checkout main`, `git pull`, `git checkout -b sensitivity`.
2. Run {ACT}:
   ```
   python scripts/sensitivity.py
   ```
   4 Mirai runs, a few minutes each: baseline, learning rate 0.01, hidden ratio 0.5, and the old 43.7 % split (which trains on attack traffic). If one fails, it says so and continues; paste that message here.
3. `python scripts/compare_results.py` and copy the **Sensitivity runs** table into `report/sensitivity.md`. Fill in the prompts there: one line per run, and which setting matters most. The old-split run shows what training on attack traffic does, a key point for the discussion.

**Environment record**
4. Save your installed packages:
   - **Windows PowerShell:** `pip freeze --all --local | Out-File -Encoding utf8 results/environment.txt`
   - **Mac / Git Bash:** `pip freeze --all --local > results/environment.txt`
5. In `report/sensitivity.md` under *Environment and run time*: your computer (Windows Settings → System → About, or About This Mac), Python version (`python --version`), and a table of each main run's time. Get the `"seconds"` and `"n_packets"` values from every `results/main_*.json`; packets/second = n_packets ÷ seconds.
6. Commit (`results/*.json`, `results/environment.txt`, `report/sensitivity.md`), push, pull request with `Closes #{{n}}`, reviewer **Gael**. Target: **Mon Dec 1**.
""",
        "- 4 sensitivity results merged.\n- `report/sensitivity.md` has the table, the explanation and the environment/timing section.",
        reviewer="Gael")),
    16: dict(title="[P2] Report: discussion", milestone=PHASE2, body=body(
        "Write the conclusion of our study: what reproduced, what didn't, and why.",
        "2 to 3 h", "#11 (comparison) and #14 (sensitivity) merged; Gael's method section helps",
        f"""
1. `git checkout main`, `git pull`, `git checkout -b report-discussion`.
2. Read `report/comparison.md`, `report/sensitivity.md`, the three `report/results-*.md` files and the Underspecification Register.
3. Fill in `report/discussion.md` (~500 to 700 words). It has five headings with prompts: what reproduced, what didn't (and the most likely reason, with a register ID and sensitivity result), surprises, what the authors should have reported, limitations.
4. Ask Gael and L1PsterGram to read it (comment on the pull request) and fix what they flag.
5. Commit, push, pull request with `Closes #{{n}}`, reviewer **L1PsterGram**. Target: **Tue Dec 2**.
""",
        "- `report/discussion.md` complete with all five headings, merged.",
        reviewer="L1PsterGram")),
    17: dict(title="[P2] Presentation slides (due Wed Dec 3)", milestone=PHASE2, body=body(
        "Have the slides ready for the presentation on Wed Dec 3. Each person makes the slides for their own part. No rehearsal needed.",
        "~1 h each", "your results section (attack issues) mostly done",
        """
1. One person makes a shared deck (Google Slides or PowerPoint online) and posts the edit link in the team chat.
2. Each person builds their own slides by **Tue Dec 2** (~10 slides total):
   | # | Slide | Who |
   |---|---|---|
   | 1 | Title, team, paper citation | Gael |
   | 2 | What a network IDS is; how Kitsune works (Fig. 1 of the paper, cited) | Gael |
   | 3 | The claim we tested + target numbers | Gael |
   | 4 | Mirai: split decision (#12) + results + one figure | Gael |
   | 5 | Data and setup: 3 attacks, our pipeline | L1PsterGram |
   | 6 | SYN DoS: results + one figure | L1PsterGram |
   | 7 | Sensitivity: what moved the numbers | L1PsterGram |
   | 8 | ARP MitM: results + one figure | meggy |
   | 9 | Comparison table (✅/❌) | meggy |
   | 10 | Lessons: what the paper didn't tell us | meggy |
3. Add 2 to 3 sentences of speaker notes per slide.
4. Export to PDF and commit it as `slides/presentation.pdf` (branch, commit, pull request with `Closes #{n}`).
""",
        "- `slides/presentation.pdf` merged by Wed Dec 3.")),
}

PREPEND_5 = ("> **Updated Nov 25 (consolidated plan):** due **Fri Nov 28**. You can run the smoke test on your own attack: "
             "in step 2, use `--attack SYN_DoS` instead of `--attack Mirai` (put the SYN DoS files in `data/raw/SYN_DoS/`). "
             "Get the data from the team's shared drive.\n\n")

CLOSE = {  # issue -> comment template (uses created issue numbers)
    8: "Replaced by #{mirai} (Mirai, Gael) under the consolidated plan: each person runs their own attack.",
    9: "Replaced by #{syn} (SYN DoS, L1PsterGram) and #{arp} (ARP MitM, meggy) under the consolidated plan.",
    10: "Merged into #14: the environment and timing record is now part of the sensitivity task.",
    13: "Merged into #11: the comparison table is now part of the metric check.",
    15: "Each person now makes the figures for their own attack: #{mirai}, #{syn}, #{arp}.",
    19: "Duplicate of #8 (created when the setup script was re-run).",
}


def main():
    # 1. milestones
    api("PATCH", "milestones/1", {"title": "Phase 1: Setup", "due_on": "2026-11-28T08:00:00Z",
        "description": "Data on the shared drive, training split decided (#12), smoke test works (#5), targets confirmed (#6). "
                       "Checkpoint Fri Nov 28: everyone can run a 50k-packet test on their own attack."})
    api("PATCH", "milestones/2", {"title": "Phase 2: Reproduce and report", "due_on": "2026-12-03T08:00:00Z",
        "description": "Checkpoints: Sun Nov 30 all main results merged · Mon Dec 1 comparison + figures + sensitivity · "
                       "Tue Dec 2 report sections + slides · Wed Dec 3 present. "
                       "If behind, cut: sensitivity to 2 runs → m = 1 for SYN DoS / ARP MitM → ARP MitM. Mirai m = 10 is never cut."})

    # 2. new issues
    created = {}
    for spec in NEW:
        r = api("POST", "issues", {"title": spec["title"], "body": spec["body"], "labels": spec["labels"],
                                   "assignees": spec["assignees"], "milestone": PHASE2})
        n = r.get("number")
        created[spec["key"]] = n
        if APPLY:
            api("PATCH", f"issues/{n}", {"body": finish(n, spec["body"])})
    if APPLY:
        APPLIED.write_text(json.dumps({"created_issues": list(created.values()), "by_key": created}, indent=2))

    # 3. edits
    for n, e in EDITS.items():
        api("PATCH", f"issues/{n}", {"title": e["title"], "milestone": e["milestone"], "body": finish(n, e["body"])})
    api("PATCH", "issues/12", {"milestone": PHASE1})
    if APPLY:
        cur = json.loads(subprocess.run(["gh", "api", f"repos/{REPO}/issues/5"], text=True, check=True,
                                        capture_output=True).stdout)["body"]
        if not cur.startswith("> **Updated Nov 25"):
            api("PATCH", "issues/5", {"body": PREPEND_5 + cur})
    else:
        api("PATCH", "issues/5", {"body": "(prepend update note)"})

    # 4. closures
    for n, text in CLOSE.items():
        api("POST", f"issues/{n}/comments", {"body": text.format(**created)})
        api("PATCH", f"issues/{n}", {"state": "closed", "state_reason": "not_planned"})

    # 5. retire the empty Week 3 milestone (closed, not deleted)
    api("PATCH", f"milestones/{WEEK3}", {"state": "closed"})
    print("\nDone." if APPLY else "\nDry run only.")


if __name__ == "__main__":
    main()
