#!/usr/bin/env bash
# Sets up GitHub for the Kitsune reproduction: labels, 3 weekly milestones, 16 issues,
# a Project board with every issue on it, and the wiki pages.
#
# Run from the repo root on your own machine:
#   gh auth login                       # once
#   gh auth refresh -s project          # once: lets gh create the Project board
#   ROLE_A=GaelA893 ROLE_B=<github-user> ROLE_C=<github-user> bash setup/bootstrap_github.sh
#
# Safe to re-run: existing labels, milestones and same-titled issues are skipped.
# ROLE_* are optional; leave empty to create issues unassigned. Teammates must be
# repo collaborators (Settings → Collaborators) before they can be assigned.
set -euo pipefail

REPO="${REPO:-GaelA893/IDS-Project}"
OWNER="${REPO%%/*}"
PROJECT_TITLE="${PROJECT_TITLE:-Kitsune Reproduction}"
ROLE_A="${ROLE_A:-}"; ROLE_B="${ROLE_B:-}"; ROLE_C="${ROLE_C:-}"
SKIP_PROJECT="${SKIP_PROJECT:-}"; SKIP_WIKI="${SKIP_WIKI:-}"

W1="Week 1: Setup and data";      W1_DUE="2026-11-26T23:59:00Z"
W2="Week 2: Reproduce";           W2_DUE="2026-12-03T23:59:00Z"
W3="Week 3: Analyze and report";  W3_DUE="2026-12-10T23:59:00Z"

echo "== Repo: $REPO"

# ---------- labels ----------
# REST only (gh api), so this also works where GraphQL is unavailable.
label() { gh api -X POST "repos/$REPO/labels" -f name="$1" -f color="$2" -f description="$3" >/dev/null 2>&1 && echo "label: $1" || echo "label exists: $1"; }
label "role:A" "1d76db" "Data and infrastructure"
label "role:B" "5319e7" "Experiments"
label "role:C" "0e8a16" "Evaluation and report"
label "team"   "fbca04" "Everyone"
label "data"   "c5def5" "Dataset and loading"
label "experiment" "d4c5f9" "KitNET runs"
label "analysis"   "bfdadc" "Metrics and comparison"
label "docs"       "0075ca" "Wiki, report, slides"

# ---------- milestones ----------
milestone() {
  if gh api "repos/$REPO/milestones?state=all&per_page=100" --jq '.[].title' | grep -Fxq "$1"; then
    echo "milestone exists: $1"
  else
    gh api -X POST "repos/$REPO/milestones" -f title="$1" -f due_on="$2" -f description="$3" >/dev/null && echo "milestone: $1"
  fi
}
milestone "$W1" "$W1_DUE" "Data loads, authors' code runs, paper targets confirmed. Aim for Tue Nov 25 (Thanksgiving)."
milestone "$W2" "$W2_DUE" "Full KitNET runs on Mirai, SYN DoS, ARP MitM with metrics."
milestone "$W3" "$W3_DUE" "Comparison vs paper, sensitivity runs, wiki report, presentation."

# ---------- issues ----------
EXISTING="$(gh api "repos/$REPO/issues?state=all&per_page=100" --paginate --jq '.[].title')"
ms_number() { gh api "repos/$REPO/milestones?state=all&per_page=100" --jq ".[] | select(.title==\"$1\") | .number"; }
issue() { # title milestone labels-csv assignee-csv body
  local title="$1" ms="$2" labels="$3" who="$4" body="$5"
  if grep -Fxq "$title" <<<"$EXISTING"; then echo "issue exists: $title"; return; fi
  local args=(-X POST "repos/$REPO/issues" -f title="$title" -f body="$body" -F milestone="$(ms_number "$ms")")
  local l; IFS=, read -ra L <<<"$labels"; for l in "${L[@]}"; do args+=(-f "labels[]=$l"); done
  if [ -n "$who" ]; then IFS=, read -ra A <<<"$who"; for l in "${A[@]}"; do args+=(-f "assignees[]=$l"); done; fi
  local url; url="$(gh api "${args[@]}" --jq '.html_url')"
  echo "issue: $title -> $url"
}
ALL="$(printf '%s,' $ROLE_A $ROLE_B $ROLE_C | sed 's/,$//')"

# Week 1
issue "[W1] Onboarding: clone, install, run tests, first PR" "$W1" "team" "$ALL" \
"Everyone does this, so everyone has a commit in week 1.
- [ ] Clone the repo, \`pip install -r requirements.txt\`, \`pytest -q\` passes
- [ ] Add your name, GitHub username and personality type to wiki **Team-and-Roles**
- [ ] Open a small PR (e.g. fix a typo or add yourself to the README team table); get it reviewed by someone else"

issue "[W1] Verify repo structure and environment on all laptops" "$W1" "role:A,data" "$ROLE_A" \
"- [ ] Confirm the layout in README works on Windows/macOS/Linux for all three of us
- [ ] Record each person's Python + NumPy version in Reproduction-Log
- [ ] Decide: shared venv instructions (\`python -m venv .venv\`) in README
- [ ] Close the placeholder issue #1 as superseded"

issue "[W1] Download Mirai, SYN DoS, ARP MitM feature CSVs + labels" "$W1" "role:A,data" "$ROLE_A" \
"See wiki **Data-Plan**. Proposal requirement: data must already load before approval.
- [ ] Download only \`*_dataset.csv\` and \`*_labels.csv\` for the 3 attacks (not the 18 GB archive)
- [ ] Place under \`data/raw/Mirai\`, \`data/raw/SYN_DoS\`, \`data/raw/ARP_MitM\`
- [ ] \`python scripts/check_data.py\` → paste output into Data-Plan
- [ ] Packet counts match Table III (764,137 / 2,771,276 / 2,504,267) or the difference is logged
- [ ] Share the files with the team via a drive link (never git)"

issue "[W1] Get the authors' KitNET running (smoke test)" "$W1" "role:B,experiment" "$ROLE_B" \
"- [ ] \`bash scripts/get_kitsune_code.sh\`; record the pinned Kitsune-py commit in Reproduction-Log
- [ ] Smoke test: \`python src/run_kitnet.py --attack Mirai --limit 50000 --fm-grace 5000 --ad-grace 20000\`
- [ ] Log every compatibility fix (R1 np.Inf is already handled) in Reproduction-Log
- [ ] Optional: run the authors' own \`example.py\` on their bundled mirai.zip and note its settings (U8)"

issue "[W1] Independently confirm paper targets (Fig. 9, Table III)" "$W1" "role:C,analysis" "$ROLE_C" \
"Two-person check so our targets aren't a misread.
- [ ] Without looking at configs/paper_targets.json, read Kitsune m=10 and m=1 AUC/EER for Mirai, SYN DoS, ARP from Fig. 9 (page 13 bar labels)
- [ ] Compare with \`configs/paper_targets.json\` and wiki **Paper-and-Claim**; fix any difference via PR
- [ ] Initial the confirmation line on Paper-and-Claim"

issue "[W1] Set up wiki and seed the Underspecification Register" "$W1" "role:C,docs" "$ROLE_C" \
"- [ ] Check all wiki pages render and the sidebar links work
- [ ] Read paper §V (Evaluation) and add any gaps not yet in **Underspecification-Register** (U1–U9 are seeded)
- [ ] Start Meeting-Notes with the first check-in"

# Week 2
issue "[W2] Full run: Mirai (both split rules)" "$W2" "role:B,experiment" "$ROLE_B" \
"Mirai has < 1M packets, so the paper's split can't apply as written (U1).
- [ ] \`python src/run_kitnet.py --attack Mirai --train-frac 0.437\` (Table III time ratio)
- [ ] Also m=1: add \`--m 1\`
- [ ] Commit the \`results/*.json\` files (scores .npy stay local); log in Reproduction-Log"

issue "[W2] Full runs: SYN DoS and ARP MitM" "$W2" "role:B,experiment" "$ROLE_B" \
"~35 to 40 min each at ~1,200 pkt/s; run overnight if needed.
- [ ] \`--attack SYN_DoS --train-packets 1000000\` for m=10 and m=1
- [ ] \`--attack ARP_MitM --train-packets 1000000\` for m=10 and m=1
- [ ] Commit results JSON; log each run"

issue "[W2] Record environment and timing for every run" "$W2" "role:B,experiment" "$ROLE_B" \
"- [ ] \`pip freeze > results/environment.txt\` from the machine used for final runs
- [ ] Table in Reproduction-Log: run, machine, seconds, pkt/s (compare with the paper's Pi/PC rates for discussion)"

issue "[W2] Validate metric code and score Mirai against the paper" "$W2" "role:C,analysis" "$ROLE_C" \
"- [ ] Review \`src/evaluate.py\` (AUC, EER, TPR@FPR); add a test against a hand-computed example
- [ ] Check that only the test portion (after training) is scored
- [ ] Fill the Mirai row of **Results** from the W2 run"

issue "[W2] Decide and document split rules (U1, U2)" "$W2" "role:A,data" "$ROLE_A" \
"- [ ] Write the final rule per attack in Underspecification-Register (packets vs Table III minutes)
- [ ] Stretch: get packet timestamps from the Mirai pcap to make a true time-based split, and give B the packet index"

# Week 3
issue "[W3] Paper-vs-ours comparison table" "$W3" "role:C,analysis" "$ROLE_C" \
"- [ ] Fill **Results** table for all 3 attacks, m=10 and m=1, with Δ and reproduced yes/no (±0.02)
- [ ] Link each row to its results JSON and log entry"

issue "[W3] Sensitivity runs on underspecified settings" "$W3" "role:B,experiment" "$ROLE_B" \
"Use Mirai (fastest) unless a mismatch on another attack needs explaining.
- [ ] FM grace: 5k / 50k / 10%-of-train (U3)
- [ ] Learning rate: 0.01 / 0.1 / 0.5 (U4)
- [ ] Hidden ratio 0.5 vs 0.75 (U5); authors' demo settings (U8)
- [ ] Summary table in Results → Sensitivity"

issue "[W3] Figures: ROC curves and RMSE over time" "$W3" "role:A,docs" "$ROLE_A" \
"- [ ] \`scripts/make_figures.py\`: ROC per attack from saved scores; RMSE vs packet index with attack window shaded (log scale)
- [ ] Save PNGs to \`figures/\`, embed in Results"

issue "[W3] Write the Results discussion" "$W3" "role:C,docs" "$ROLE_C" \
"- [ ] What reproduced, what didn't, most likely reasons (cite U-IDs)
- [ ] Lessons: what the paper should have reported
- [ ] Final pass on all wiki pages"

issue "[W3] Presentation slides and rehearsal" "$W3" "team,docs" "$ALL" \
"- [ ] Slides: problem, Kitsune in one diagram, claim, setup, results table, gaps, lessons
- [ ] Each person presents their own part
- [ ] One timed rehearsal before Dec 10"

# ---------- project board ----------
if [ -z "$SKIP_PROJECT" ]; then
  NUM="$(gh project list --owner "$OWNER" --format json --jq ".projects[] | select(.title==\"$PROJECT_TITLE\") | .number" 2>/dev/null || true)"
  if [ -z "$NUM" ]; then
    NUM="$(gh project create --owner "$OWNER" --title "$PROJECT_TITLE" --format json --jq '.number')"
    echo "project created: #$NUM"
  else
    echo "project exists: #$NUM"
  fi
  gh project link "$NUM" --owner "$OWNER" --repo "$REPO" 2>/dev/null || true
  # add every open issue (idempotent: adding twice is a no-op)
  for url in $(gh api "repos/$REPO/issues?state=open&per_page=100" --paginate --jq '.[] | select(.pull_request == null) | .html_url'); do
    gh project item-add "$NUM" --owner "$OWNER" --url "$url" >/dev/null && echo "board: $url"
  done
  echo "Board: https://github.com/users/$OWNER/projects/$NUM"
  echo "Tip: in the board, add a view grouped by Milestone and one grouped by Assignees."
fi

# ---------- wiki ----------
if [ -z "$SKIP_WIKI" ] && [ -d setup/wiki ]; then
  TMP="$(mktemp -d)"
  if git clone -q "https://github.com/$REPO.wiki.git" "$TMP/wiki" 2>/dev/null; then
    cp setup/wiki/*.md "$TMP/wiki/"
    git -C "$TMP/wiki" add -A
    if git -C "$TMP/wiki" diff --cached --quiet; then
      echo "wiki already up to date"
    elif git -C "$TMP/wiki" commit -qm "Wiki: Kitsune reproduction pages" && git -C "$TMP/wiki" push -q; then
      echo "wiki pushed: https://github.com/$REPO/wiki"
    else
      echo "!! Wiki push failed. Run this script from your own machine (logged in as a repo admin)."
    fi
  else
    echo "!! Wiki not reachable. Enable it (Settings → Features → Wikis), create any first page in the browser, then re-run."
  fi
fi
echo "== Done."
