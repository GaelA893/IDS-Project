"""Step-by-step bodies for issues #2 to #17 (source of truth for the issue text).

    python setup/issue_bodies.py            # print them
    python setup/issue_bodies.py --apply    # update the issues on GitHub (needs gh)
"""
import subprocess
import sys

REPO = "GaelA893/IDS-Project"
BLOB = f"https://github.com/{REPO}/blob/main"
WIKI = f"https://github.com/{REPO}/wiki"
GS = f"[Getting Started]({BLOB}/docs/GETTING_STARTED.md)"
HC = f"[How to Contribute]({BLOB}/docs/HOW_TO_CONTRIBUTE.md)"
ACT = "*(open a terminal, `cd ~/Documents/IDS-Project`, and activate the environment: Windows `.venv\\Scripts\\Activate.ps1`, Mac `source .venv/bin/activate`)*"


def body(goal, time, needs, steps, done, extra_stuck="", reviewer=""):
    parts = [
        f"**Goal:** {goal}",
        "",
        f"⏱ **Time:** {time} · 🔗 **Do first:** {needs}" + (f" · 👀 **Reviewer:** {reviewer}" if reviewer else ""),
        "",
        "### Steps",
        steps.strip(),
        "",
        "### Done when",
        done.strip(),
        "",
        "### If you get stuck",
        (extra_stuck.strip() + "\n") if extra_stuck else "",
        f"- Check the error table at the bottom of {GS}.",
        "- Stuck > 20 min: comment here with the **exact command** and the **full error text** (copy-paste), then post this issue's link in the team chat.",
        "",
        "---",
        f"_New to Git? Follow {HC} to branch, commit and open your pull request. Write `Closes #{{n}}` in the PR._",
    ]
    return "\n".join(p for p in parts if p is not None)


ISSUES = {}

# ---------------- WEEK 1 ----------------
ISSUES[2] = body(
    "Everyone gets the project running on their own computer and makes a first commit, so nobody is blocked later.",
    "45 to 60 min", "accept the repo invite (check email)",
    f"""
1. Follow {GS} **steps 1 to 5** (install Python, Git, GitHub CLI; clone; set up the environment; `pytest -q` shows `3 passed`).
   You can skip steps 6 to 8 for now if the data isn't shared yet.
2. Make a branch for this issue:
   ```
   git checkout main
   git pull
   git checkout -b issue-2-<your-github-username>
   ```
3. In the `team/` folder, create a file named `<your-github-username>.md` (in VS Code or Notepad/TextEdit) and paste the template from `team/README.md`. Fill it in.
   - Personality type: take the test the course asked for and put your real result.
4. Save it to GitHub:
   ```
   git add team
   git commit -m "Add <your name> to team (#2)"
   git push -u origin issue-2-<your-github-username>
   ```
5. Open the link Git prints, create the pull request (write `Part of #2`, **not** `Closes`, so the issue stays open for the others), and request a review from a teammate.
6. Review one teammate's #2 pull request: open it, check the file looks right, click **Review changes → Approve → Submit**, then **Merge pull request**.
7. Tick your name below.

- [ ] Gael
- [ ] L1PsterGram
- [ ] meggy
""",
    "- All three `team/<username>.md` files are merged into `main`.\n- Each person's `pytest -q` printed `3 passed`.\n- Last person to finish closes this issue.",
)

ISSUES[3] = body(
    "Make sure the project works the same way on all three computers before real runs start, and clean up the placeholder issue.",
    "30 min (spread over the week)", "#2 for each teammate",
    f"""
1. Merge pull request #18 into `main` if it isn't already (Pull requests tab → #18 → **Merge pull request**).
2. Ask each teammate to run these two commands and paste the output as a comment here:
   ```
   python --version
   python -c "import numpy, sklearn, pandas; print('numpy', numpy.__version__, '| sklearn', sklearn.__version__, '| pandas', pandas.__version__)"
   ```
3. Add a dated entry to the wiki page [Reproduction-Log]({WIKI}/Reproduction-Log) (Edit → paste at the bottom → Save):
   ```
   ### 2026-11-XX: Team environments (Gael)
   - Gael: Windows/Mac, Python 3.x, numpy x, sklearn x
   - L1PsterGram: ...
   - meggy: ...
   ```
4. If someone's Python is older than 3.10, help them install a newer one ({GS} step 1).
5. Close the old placeholder issue **#1** with the comment "Superseded by #2 to #17."
""",
    "- Three environments listed in Reproduction-Log.\n- Everyone can run `pytest -q` successfully.\n- Issue #1 is closed.",
)

ISSUES[4] = body(
    "Get the dataset onto our computers and prove it loads. **The proposal requires this before approval**, so this is the most urgent task.",
    "1 to 2 h (mostly download time)", "your own setup from #2",
    f"""
1. Follow {GS} **step 6** exactly: download the 6 files (Mirai, SYN DoS, ARP MitM; `_dataset` and `_labels` for each) and put them in `data/raw/Mirai`, `data/raw/SYN_DoS`, `data/raw/ARP_MitM`.
2. Run the check and save its output {ACT}:
   ```
   python scripts/check_data.py --save
   ```
3. Compare with the paper: you should see **764,137**, **2,771,276** and **2,504,267** packets and **115** features. If a number differs, say so in a comment here (that's a finding, not a failure).
4. Share the data with the team: make a shared drive folder (Google Drive or OneDrive) called `IDS-Project data`, upload the 6 files into `Mirai/`, `SYN_DoS/`, `ARP_MitM/` subfolders, add a `scores/` subfolder (for later), and share it with both teammates. Paste the link in the team chat (**not** in GitHub, since the repo is public).
5. Paste the check output into the wiki page [Data-Plan]({WIKI}/Data-Plan) under "Proof of loading".
6. Commit the proof file (it's tiny; the data itself is blocked by `.gitignore`):
   ```
   git checkout main
   git pull
   git checkout -b issue-4-data
   git add results/check_data.txt
   git commit -m "Data loads: check_data output (#4)"
   git push -u origin issue-4-data
   ```
   Open the pull request with `Closes #4`.
""",
    "- `results/check_data.txt` is merged and shows 3 attacks with 115 features.\n- Data-Plan wiki page has the output.\n- Teammates have the shared-drive link.",
    "- Download is very slow: start it before bed; campus Wi-Fi can be slow for GB files.\n- `check_data` takes minutes on SYN DoS: that's normal (2.7M rows).",
    reviewer="L1PsterGram",
)

ISSUES[5] = body(
    "Prove the authors' Kitsune code runs on a modern computer, and record any fixes needed. This de-risks all of Week 2.",
    "1 h", "#2 (your setup) and the Mirai files (from #4's shared drive)",
    f"""
1. Put the 2 Mirai files in `data/raw/Mirai/` (download from the team's shared drive).
2. Follow {GS} **steps 7 and 8**: clone the authors' code, then run the 1-minute test {ACT}:
   ```
   python src/run_kitnet.py --attack Mirai --limit 50000 --fm-grace 5000 --ad-grace 20000
   ```
   You should see lines like `Feature-Mapper: train-mode`, then a block with `"auc"` and `"eer"`, then `Saved results/adhoc_Mirai_...json`.
3. Record which version of the authors' code we use:
   ```
   git -C external/Kitsune-py rev-parse HEAD
   ```
   It prints a long code (a commit hash). Copy it.
4. Add an entry to the wiki [Reproduction-Log]({WIKI}/Reproduction-Log):
   ```
   ### 2026-11-XX: KitNET smoke test (L1PsterGram)
   - Kitsune-py commit: <paste hash>
   - Command: (paste the command from step 2)
   - Result: AUC = ..., EER = ..., time = ... seconds (from the JSON file's "seconds")
   - Problems / fixes: none (or describe)
   ```
5. Commit the result file:
   ```
   git checkout -b issue-5-smoke-test
   git add results/*.json
   git commit -m "KitNET smoke test on 50k Mirai packets (#5)"
   git push -u origin issue-5-smoke-test
   ```
   Open the pull request with `Closes #5`.
""",
    "- Smoke-test JSON is merged.\n- Reproduction-Log has the Kitsune-py commit hash and result.",
    "- `np.Inf was removed`: already fixed in our code; make sure you pulled the latest `main`.\n- `KitNET not found`: you skipped step 7, or ran it from a different folder.",
    reviewer="meggy",
)

ISSUES[6] = body(
    "Make sure the target numbers we compare against are read correctly from the paper. A second pair of eyes avoids a whole project built on a typo.",
    "45 min", "nothing (good first task)",
    f"""
1. Open the paper PDF: https://www.ndss-symposium.org/wp-content/uploads/2018/02/ndss2018_03A-3_Mirsky_paper.pdf
2. Go to **page 13**, **Figure 9**. Zoom in to 300 % or more. It has four big panels; you need the **bottom two**:
   - bottom-left: **Area Under the Curve (AUC)**
   - bottom-right: **Equal Error Rate (EER)**
3. Each panel has small boxes per attack. Use the boxes labelled **ARP**, **Mirai** and **SYN DoS**.
4. In each box there are 7 bars. From left to right: Suricata, Iso. Forest, GMM, Inc. GMM, pcStream, **Kitsune (m=10)** (6th bar), **Kitsune (m=1)** (7th, darkest bar). The number is printed sideways on each bar.
5. **Without looking at our files first**, write the 12 numbers in a comment on this issue:
   | Attack | AUC m=10 | EER m=10 | AUC m=1 | EER m=1 |
   |---|---|---|---|---|
   | Mirai | | | | |
   | SYN DoS | | | | |
   | ARP MitM | | | | |
6. Now compare with the wiki [Paper-and-Claim]({WIKI}/Paper-and-Claim) table (and `configs/paper_targets.json`).
   - All match → edit Paper-and-Claim and put your name on the confirmation line.
   - Something differs → comment which one; Gael or you fix `configs/paper_targets.json` in a pull request.
7. While you're in the paper, check **Table III** (page 11): packet counts 764,137 (Mirai), 2,771,276 (SYN DoS), 2,504,267 (ARP MitM).
""",
    "- Your 12 numbers are in a comment here.\n- Paper-and-Claim has your confirmation (or a fix PR is merged).",
)

ISSUES[7] = body(
    "Get the wiki in shape (it's our report) and add any gaps in the paper we haven't spotted yet.",
    "1 to 1.5 h", "the wiki pages exist (Gael pushes them with the setup script). If the Wiki tab is empty, see step 1",
    f"""
1. Open the [Wiki tab]({WIKI}). If it's empty or only has a placeholder page: for each file in the repo folder `setup/wiki/`, click **New page**, use the file name without `.md` as the title (e.g. `Data-Plan`), paste the file's contents, and **Save page**. `_Sidebar` makes the menu on the right.
2. Click every link in the sidebar and on Home. Fix any that are broken.
3. Read paper **Section V (Evaluation)**, pages 10 to 13. For each sentence that leaves a setting vague (no exact number, or two places that disagree), check whether it's already in [Underspecification-Register]({WIKI}/Underspecification-Register) (U1 to U9). If not, add a row: what's missing, what the paper says (quote ≤ 1 sentence + page), and "open".
4. Start [Meeting-Notes]({WIKI}/Meeting-Notes): set up the first 15-minute check-in (suggest Mon and Thu), and write notes after it using the template on that page.
5. Comment here with a list of the rows you added (or "none new found").
""",
    "- All wiki links work.\n- Underspecification-Register reviewed (new rows added or 'none found').\n- First meeting notes written.",
)

# ---------------- WEEK 2 ----------------
ISSUES[8] = body(
    "Run the real experiment on Mirai (the smallest attack) for both versions of Kitsune.",
    "~30 min of computer time, 15 min of your time", "#5 (code runs) and Mirai files in `data/raw/Mirai/`",
    f"""
1. Get the latest code: `git checkout main` then `git pull`.
2. Plug the laptop in and turn off sleep while it runs (Windows: Settings → System → Power → Sleep: Never; Mac: System Settings → Battery/Energy → prevent sleeping).
3. Run both official Mirai runs (m = 10 and m = 1) {ACT}:
   ```
   python scripts/run_all.py Mirai
   ```
   It prints progress every 100,000 packets and ends with `Done.` About 10 to 15 min per run.
4. See the comparison:
   ```
   python scripts/compare_results.py
   ```
5. Upload the two big files `results/main_Mirai_..._scores.npy` to the shared drive folder `scores/` (Gael needs them for figures).
6. Add a Reproduction-Log entry (wiki): date, command, AUC and EER for m=10 and m=1, how long it took.
7. Commit the small result files:
   ```
   git checkout -b issue-8-mirai
   git add results/*.json results/comparison.md
   git commit -m "Main Mirai runs m=10 and m=1 (#8)"
   git push -u origin issue-8-mirai
   ```
   Pull request with `Closes #8`.
""",
    "- Two `results/main_Mirai_*.json` files are merged.\n- Scores uploaded to the shared drive.\n- Reproduction-Log entry written.",
    "- It seems frozen: it prints only every 100,000 packets; wait 2 min before worrying.\n- `MemoryError`: close the browser and other apps and rerun.",
    reviewer="meggy",
)

ISSUES[9] = body(
    "Run the real experiment on the two larger attacks. These are long, so run them overnight.",
    "~3 h of computer time (overnight), 20 min of your time", "#8 done (so you know the process works); SYN DoS and ARP MitM files in `data/raw/`",
    f"""
1. `git checkout main` then `git pull`. Laptop plugged in, sleep off (see #8 step 2).
2. Before bed, start both attacks one after the other with one line {ACT}:
   - **Windows:** `python scripts/run_all.py SYN_DoS; python scripts/run_all.py ARP_MitM`
   - **Mac:** `python scripts/run_all.py SYN_DoS && python scripts/run_all.py ARP_MitM`
3. In the morning, scroll up: each of the 4 runs should end with `Saved results/main_...json`. If one failed, copy the error into a comment here and rerun just that attack.
4. `python scripts/compare_results.py` to see all main results together.
5. Upload the 4 new `..._scores.npy` files to the shared drive `scores/` folder.
6. Reproduction-Log entry: date, AUC/EER for each run, time taken.
7. Commit:
   ```
   git checkout -b issue-9-syn-arp
   git add results/*.json results/comparison.md
   git commit -m "Main SYN DoS and ARP MitM runs (#9)"
   git push -u origin issue-9-syn-arp
   ```
   Pull request with `Closes #9`.
""",
    "- Four new `results/main_*.json` files (SYN DoS and ARP MitM × m=10, m=1) are merged.\n- Scores uploaded; log written.",
    "- Running out of time: do only m=10 with `python src/run_kitnet.py --attack SYN_DoS --group main --train-packets 1000000` and note it in the log.",
    reviewer="meggy",
)

ISSUES[10] = body(
    "Record exactly what computer and software produced our numbers, so anyone can repeat them. That's the point of a reproduction study.",
    "20 min", "#8 and #9 (do it on the computer that made the main runs)",
    f"""
1. On the computer that made the main runs {ACT}:
   ```
   pip freeze --all --local
   ```
   Copy the output into a new file `results/environment.txt` (in VS Code or a text editor; save it as UTF-8 text).
2. Find your computer details: Windows Settings → System → About (Processor, Installed RAM); Mac → About This Mac (Chip, Memory).
3. For each `results/main_*.json`, open it and copy `"seconds"` and `"n_packets"`. Packets per second = n_packets ÷ seconds.
4. Add this table to the wiki [Reproduction-Log]({WIKI}/Reproduction-Log):
   | Run | Computer | Seconds | Packets/s |
   |---|---|---|---|
   | Mirai m=10 | e.g. i5-1135G7, 16 GB | | |
   For the report: the paper's runtime test (§V-C, Fig. 10) used a C++ version with 198 features and got roughly 1,000 to 5,400 packets/s on a Raspberry Pi and 7,500 to 37,300 on a PC, depending on ensemble size. Ours is the Python version, so expect slower.
5. Commit `results/environment.txt` (branch `issue-10-env`, pull request `Closes #10`).
""",
    "- `results/environment.txt` merged.\n- Timing table in Reproduction-Log.",
)

ISSUES[11] = body(
    "Double-check that our scoring code measures what the paper measures, then fill in the first real result.",
    "1 h", "#8 (Mirai results merged)",
    f"""
1. `git checkout main`, `git pull`, then `git checkout -b issue-11-metrics`.
2. Read `src/evaluate.py` top to bottom (it's short). In plain words: **AUC** = how well scores rank attacks above normal traffic (1.0 perfect, 0.5 coin-flip). **EER** = the error rate at the threshold where false alarms equal missed attacks (0 perfect, 0.5 coin-flip).
3. Add one more test. Open `tests/test_evaluate.py` and paste this at the bottom:
   ```python
   def test_hand_example():
       # 4 normal packets, 4 attacks; exactly one normal packet scores above one attack
       y = np.array([0, 0, 0, 0, 1, 1, 1, 1])
       s = np.array([1, 2, 3, 6, 5, 7, 8, 9])
       m = all_metrics(y, s)
       assert abs(m["auc"] - 15 / 16) < 1e-9   # 15 of the 16 (normal, attack) pairs are ranked correctly
       assert abs(m["eer"] - 0.25) < 1e-9      # at threshold 6: 1 of 4 normals flagged, 1 of 4 attacks missed
   ```
   Run `pytest -q`. You should see `4 passed`.
4. Check that only the **test** packets are scored: open `results/main_Mirai_m10_*.json`. `metrics.n` must equal `n_packets − n_train`. Write the three numbers in a comment here.
5. Fill the **Mirai rows** of the wiki [Results]({WIKI}/Results) table: run `python scripts/compare_results.py` and copy the Mirai lines.
6. Commit the test (`git add tests`, commit, push), pull request with `Closes #11`.
""",
    "- `pytest -q` shows 4 passed on `main`.\n- Comment with n / n_packets / n_train.\n- Mirai rows filled in Results.",
    reviewer="Gael",
)

ISSUES[12] = body(
    "Write down, once and for all, how we split each recording into training and testing, and why. The paper's rule doesn't work for Mirai.",
    "45 min", "#6 (targets confirmed)",
    f"""
1. Background: the paper says it trained on "the first million packets" (§V-A), but **Mirai only has 764,137**. Table III gives Mirai's **train time 52.0 min** and **execute time 66.9 min** instead. 52.0 ÷ (52.0 + 66.9) = **0.437**, so we train on the first 43.7 % of Mirai packets. Every other attack uses the first 1,000,000. This is already built into `scripts/run_all.py`.
2. Check the arithmetic yourself and confirm Table III's numbers in the paper.
3. In the wiki [Underspecification-Register]({WIKI}/Underspecification-Register), update rows **U1** and **U2**:
   - "Our default" column: write the final rule in one sentence.
   - Add the reasoning (the calculation above) and the limitation: *packet share is only an approximation of time share, because packet rate isn't constant.*
   - Change status from "open" to "decided".
4. Optional, only if you're comfortable: use Wireshark on the Mirai pcap file (Statistics → Capture File Properties) to note the capture's first and last timestamps, and add them to U1.
5. Comment here linking the wiki page.
""",
    "- U1 and U2 say 'decided' with the rule and reasoning.",
)

# ---------------- WEEK 3 ----------------
ISSUES[13] = body(
    "Produce the headline result of the whole project: did each number reproduce?",
    "45 min", "#8 and #9 merged",
    f"""
1. `git checkout main`, `git pull` (gets everyone's result files).
2. {ACT}
   ```
   python scripts/compare_results.py
   ```
   It prints a Markdown table, with ✅ meaning within 0.02 of the paper, and saves `results/comparison.md`.
3. Open the wiki [Results]({WIKI}/Results) page → Edit → replace the empty "Paper vs ours" table with the printed **Main results** table → Save.
4. Under the table, write 2 to 3 plain sentences: how many of the 6 rows reproduced, which was closest, which was furthest.
5. Commit `results/comparison.md` (branch `issue-13-comparison`, pull request `Closes #13`).
""",
    "- Results page shows all 6 main rows (3 attacks × m=10, m=1) with ✅/❌.",
)

ISSUES[14] = body(
    "Measure how much the settings the paper never gave us change the result. This is what explains any mismatch.",
    "~1.5 h computer time, 15 min your time", "#8 done",
    f"""
1. `git checkout main`, `git pull`. Laptop plugged in, sleep off.
2. {ACT}
   ```
   python scripts/sensitivity.py
   ```
   It runs Mirai 7 times, changing one setting each time (each run labelled with its U-number from the Underspecification-Register). About 10 min per run.
3. If one variant fails, it says so and moves on. Copy that message into a comment here.
4. `python scripts/compare_results.py` → copy the **Sensitivity runs** table into the wiki [Results]({WIKI}/Results) under "Sensitivity".
5. Write 2 to 3 sentences: which setting moved AUC/EER the most, and by how much compared to the "baseline (all defaults)" row.
6. *If* #13 shows SYN DoS or ARP MitM did **not** reproduce and there's time, run the same for that attack overnight: `python scripts/sensitivity.py SYN_DoS`.
7. Commit the new JSON files (branch `issue-14-sensitivity`, pull request `Closes #14`).
""",
    "- Sensitivity table and summary sentences are in Results.\n- Sensitivity JSON files merged.",
    reviewer="meggy",
)

ISSUES[15] = body(
    "Make the pictures for the report and presentation: a ROC curve and an anomaly-score timeline per attack.",
    "45 min", "#8 and #9 (scores uploaded to the shared drive)",
    f"""
1. `git checkout main`, `git pull`.
2. Download all `main_*_scores.npy` files from the shared drive `scores/` folder into your `results/` folder. You also need the data in `data/raw/` (from #4).
3. {ACT}
   ```
   python scripts/make_figures.py
   ```
   It saves two PNGs per run into `figures/`. Open a few and check they look sensible: the red (attack) points should mostly sit above the blue ones after the grey training period.
4. Commit the figures (they're small images):
   ```
   git checkout -b issue-15-figures
   git add figures
   git commit -m "ROC and anomaly-score figures (#15)"
   git push -u origin issue-15-figures
   ```
   Pull request with `Closes #15` and merge it.
5. After merging, add them to the wiki [Results]({WIKI}/Results) page under "Figures", one line per image:
   ```
   ![Mirai m=10 ROC](https://github.com/GaelA893/IDS-Project/blob/main/figures/FILE_NAME.png?raw=true)
   ```
   (Replace `FILE_NAME` with the real file name.)
""",
    "- `figures/` merged with ROC and RMSE images for every main run.\n- Images visible on the Results wiki page.",
    "- `skip ...: scores file not on this computer`: the `.npy` file isn't in `results/`; download it from the drive.",
    reviewer="L1PsterGram",
)

ISSUES[16] = body(
    "Write the conclusion of our study: what reproduced, what didn't, and why.",
    "2 to 3 h", "#13 and #14 (and ideally #15)",
    f"""
1. Read the finished Results tables and the [Underspecification-Register]({WIKI}/Underspecification-Register).
2. In the wiki [Results]({WIKI}/Results) page under **Discussion**, write about 400 to 700 words with these 4 headings:
   - **What reproduced:** list each ✅ row with its numbers.
   - **What didn't:** each ❌ row, the gap (Δ), and the most likely reason. Point to a U-number and the sensitivity result that supports it (e.g. "U1: Mirai's split…").
   - **Surprises:** e.g. ARP MitM is weak even in the paper (AUC 0.58 for m=10, worse than m=1), plus the NumPy fix (R1 in Reproduction-Log).
   - **What the authors should have reported:** the settings we had to guess (from the register).
3. Proofread every other wiki page once (typos, empty sections, broken links).
4. Ask Gael and L1PsterGram to read it and comment here; fix what they flag.
""",
    "- Discussion section complete with the 4 headings.\n- Both teammates commented that they've read it.",
)

ISSUES[17] = body(
    "Present the study. Each person presents the part they did.",
    "3 to 4 h total (split between 3)", "#13, #15, #16 mostly done",
    """
1. Make one shared slide deck (Google Slides or PowerPoint online) and share the edit link in the team chat.
2. Use this outline (~10 slides, ~10 min):
   | # | Slide | Who |
   |---|---|---|
   | 1 | Title, team, paper citation | anyone |
   | 2 | What a network IDS is and why anomaly detection | C |
   | 3 | How Kitsune works (use Fig. 1 from the paper (page 2, cite it), or a simple 3-box diagram: features → autoencoders → score) | C |
   | 4 | The claim we tested + targets table | C |
   | 5 | Data: 3 attacks, packet counts, how we loaded them | A |
   | 6 | Setup: splits, settings, the Mirai problem (U1) | A |
   | 7 | Results table (✅/❌) | B |
   | 8 | One RMSE timeline + one ROC figure | B |
   | 9 | Sensitivity: what moved the numbers | B |
   | 10 | Lessons: what was missing from the paper + takeaways | C |
3. Each person builds their own slides and writes speaker notes (2 to 3 sentences per slide).
4. Do one timed run-through together at least 2 days before Dec 10. Note what to cut if you go over time.
5. Export to PDF, put it in the repo as `slides/presentation.pdf` (branch, commit, pull request `Closes #17`).
""",
    "- PDF of the slides is merged.\n- One rehearsal done (note it in Meeting-Notes).",
)


def main():
    for n, b in ISSUES.items():
        ISSUES[n] = b.replace("{n}", str(n))
    ISSUES[2] = ISSUES[2].replace("Write `Closes #2` in the PR.", "Write `Part of #2` in the PR (see step 5).")
    if "--apply" not in sys.argv:
        for n, b in ISSUES.items():
            print(f"\n===== #{n} =====\n{b}")
        return
    for n, b in ISSUES.items():
        subprocess.run(["gh", "api", "-X", "PATCH", f"repos/{REPO}/issues/{n}", "-f", f"body={b}",
                        "--jq", '"#\\(.number) updated: \\(.title)"'], check=True)


if __name__ == "__main__":
    main()
