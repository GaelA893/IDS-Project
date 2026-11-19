# How to Contribute (Git and GitHub, step by step)

Your **commits and pull requests are how the instructor sees your effort**, so every task ends with a pull request (PR). This page shows exactly how. Do [GETTING_STARTED.md](GETTING_STARTED.md) first.

## The loop for every task

**1. Pick your issue.** Go to https://github.com/GaelA893/IDS-Project/issues and open an issue assigned to you. Note its number, for example **#4**.

**2. Get the latest code and make a branch** (a private copy of the project for this task):
```
cd ~/Documents/IDS-Project
git checkout main
git pull
git checkout -b issue-4-download-data
```
Name your branch `issue-<number>-<two-or-three-words>`.

**3. Do the work** by following the steps in the issue. Tick each checkbox on the issue page as you go (just click the box).

**4. Save your work as a commit:**
```
git status
```
This lists the files you changed. Check that **no data files** (`.csv`, `.gz`, `.pcapng`) appear. They shouldn't, because `.gitignore` blocks them. Then:
```
git add .
git commit -m "Short description of what you did (#4)"
```
Commit as often as you like; small commits are good.

**5. Upload your branch:**
```
git push -u origin issue-4-download-data
```
The output shows a link like `https://github.com/GaelA893/IDS-Project/pull/new/issue-4-download-data`. Open it.

**6. Open the pull request.** On that page:
- Title: what you did.
- The description is pre-filled from a template. Fill in each section, and write `Closes #4` at the top (this links the PR to the issue and closes the issue when merged).
- On the right, under **Reviewers**, pick a teammate.
- Click **Create pull request**.

**7. Review and merge.** Your teammate opens the PR, clicks the **Files changed** tab, reads it, and either:
- clicks **Review changes → Approve**, then the green **Merge pull request** button, or
- leaves a comment asking for a fix. You fix it on the same branch, then `git add .`, `git commit -m "..."` and `git push` again, and the PR updates automatically.

Never merge your own PR. When reviewing someone else's, it's fine to only check that it does what the issue asked and the commands in "How I checked it" make sense.

## Tasks that are only writing (wiki pages)

The wiki can be edited in the browser: open the **Wiki** tab, open the page, click **Edit**, change it, write a short message in **Edit message**, and click **Save page**. The wiki keeps its own history, so these edits count too.
Then comment on the issue with a link to the page you edited, so it's on record.

## Uploading results

When a script tells you it saved `results/....json`, those small files **should** be committed (step 4); they are the evidence. The big `..._scores.npy` files are not committed: upload them to the team's shared drive folder `scores/` instead (the person making figures needs them).

## Golden rules
1. One issue → one branch → one PR.
2. Never commit data files or anything over a few MB.
3. Anything that differs from the paper (a setting you had to choose, a fix, a surprise) gets a dated entry in the wiki **Reproduction-Log** the same day.
4. Stuck for more than 20 minutes → comment on the issue with the command and full error, then ping the team chat.

## Undo buttons
| Problem | Fix |
|---|---|
| Committed to `main` by accident (before pushing) | `git branch issue-N-name` then `git reset --hard origin/main`, then `git checkout issue-N-name` |
| `git pull` says there are local changes | `git stash`, then `git pull`, then `git stash pop` |
| Committed a data file by mistake (before pushing) | `git reset --soft HEAD~1`, then `git restore --staged <file>`, then commit again |
| Anything scarier | Stop and ask in the team chat before running more commands |
