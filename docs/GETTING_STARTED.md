# Getting Started (no experience needed)

Follow these steps once, in order. Total time: about 30 to 45 minutes, mostly waiting for installs and downloads.
Every command goes in a **terminal**:
- **Windows:** press Start, type `PowerShell`, open it.
- **Mac:** press Cmd+Space, type `Terminal`, open it.

Type or paste one command at a time and press Enter. If a step's output doesn't look like the "you should see" line, stop and see **If you get stuck** at the bottom.

---

## Step 1. Install Python
1. Go to https://www.python.org/downloads/ and click the big yellow **Download Python 3.x** button.
2. Run the installer.
   - **Windows:** on the first screen, **tick "Add python.exe to PATH"** before clicking Install. This is the most common mistake.
3. Close and reopen your terminal, then run:
   ```
   python --version
   ```
   You should see `Python 3.10` or higher. (On Mac, if that fails, use `python3` everywhere this guide says `python`.)

## Step 2. Install Git
- **Windows:** https://git-scm.com/download/win → run the installer → click Next on every screen (the defaults are fine).
- **Mac:** run `git --version`. If it isn't installed, a pop-up offers to install it; click **Install**.

Close and reopen the terminal, then:
```
git --version
```
You should see `git version 2.x`.

**Also install the GitHub CLI** so pushing to GitHub works without passwords (GitHub no longer accepts your account password for Git):
1. Download it from https://cli.github.com and install it (Mac users with Homebrew can run `brew install gh` instead).
2. Close and reopen the terminal, then run `gh auth login` and answer: **GitHub.com** → **HTTPS** → **Yes** (authenticate Git) → **Login with a web browser**. Copy the one-time code it shows, press Enter, paste the code in the browser, and approve.

Tell Git who you are (use the email on your GitHub account):
```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Step 3. Accept the repo invite
Check your email (or https://github.com/notifications) for the invite to **GaelA893/IDS-Project** and click **Accept**. You can't push or be assigned issues until you do.

## Step 4. Download the project
Pick a folder you'll remember (here, Documents):
```
cd ~/Documents
git clone https://github.com/GaelA893/IDS-Project.git
cd IDS-Project
```
If Git ever asks for a username or password, redo the `gh auth login` part of Step 2.

> **Every time** you open a new terminal to work on the project, first run `cd ~/Documents/IDS-Project`.

## Step 5. Set up Python for the project
Create a private Python environment so this project's packages don't clash with anything else:

**Windows:**
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If you see *"running scripts is disabled on this system"*, run this once, answer `Y`, and then try the activate line again:
```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Mac:**
```
python3 -m venv .venv
source .venv/bin/activate
```

Using **Git Bash** instead of PowerShell? Activate with `source .venv/Scripts/activate`.

You should now see `(.venv)` at the start of your terminal line. **Activate it every time you open a new terminal** (just the second line).

Install the packages and run the tests:
```
pip install -r requirements.txt
pytest -q
```
You should see `3 passed`.

## Step 6. Get the dataset
You need **6 files**, 2 per attack. Don't download the whole 18 GB dataset.

1. Open https://archive.ics.uci.edu/dataset/516/kitsune+network+attack+dataset
2. Find the file list on the page and download only these (names may end in `.csv` or `.csv.gz`; either works, so **don't unzip**):
   - Mirai: `Mirai_dataset.csv.gz`, `Mirai_labels.csv.gz`
   - SYN DoS: `SYN DoS_dataset.csv.gz`, `SYN DoS_labels.csv.gz`
   - ARP MitM: `ARP MitM_dataset.csv.gz`, `ARP MitM_labels.csv.gz`

   If the page only offers one giant zip, use Kaggle instead: search Kaggle for **"Kitsune Network Attack Dataset"** (uploaded by Yisroel Mirsky), sign in, open the attack's folder in the file browser, and download single files with the download icon next to each file.
3. Inside the `IDS-Project` folder, make this layout (create the folders in File Explorer/Finder):
   ```
   IDS-Project/
     data/
       raw/
         Mirai/      ← both Mirai files here
         SYN_DoS/    ← both SYN DoS files here
         ARP_MitM/   ← both ARP MitM files here
   ```
   Folder names are flexible (`syn dos`, `SYN_DoS` and `syn_dos` all work).
4. Check it:
   ```
   python scripts/check_data.py
   ```
   You should see 3 rows with **764,137**, **2,771,276** and **2,504,267** packets and **115** features. This takes a minute or two; the big files are slow to read.

> Once one person has the files, they can share them with the team through a shared drive link. **Never** commit them to Git; `.gitignore` already blocks the `data/` folder.

**Computer requirements:** about 8 GB of RAM and 5 GB of free disk space.

## Step 7. Get the authors' Kitsune code
```
git clone --depth 1 https://github.com/ymirsky/Kitsune-py external/Kitsune-py
```
You should see `Cloning into 'external/Kitsune-py'...`

## Step 8. Run a 1-minute test
```
python src/run_kitnet.py --attack Mirai --limit 50000 --fm-grace 5000 --ad-grace 20000
```
You should see progress lines, then a block with `"auc"` and `"eer"`, then `Saved results/...json`. The numbers won't match the paper yet, because this run uses only the first 50,000 packets. If you got this far, you're fully set up.

---

## Cheat sheet: commands you'll use

| What | Command |
|---|---|
| Go to the project | `cd ~/Documents/IDS-Project` |
| Turn on the environment | Windows: `.\.venv\Scripts\Activate.ps1` · Mac: `source .venv/bin/activate` |
| Check data loads | `python scripts/check_data.py` |
| Official runs for one attack | `python scripts/run_all.py Mirai` (or `SYN_DoS`, `ARP_MitM`) |
| Sensitivity runs | `python scripts/sensitivity.py` |
| Paper-vs-ours table | `python scripts/compare_results.py` |
| Figures | `python scripts/make_figures.py` |
| Unit tests | `pytest -q` |

To save your work to GitHub, see **docs/HOW_TO_CONTRIBUTE.md**.

## If you get stuck
1. Read the last 3 to 5 lines of the error; they usually say what's wrong.
2. Common fixes:
   | Error says | Fix |
   |---|---|
   | `'python' is not recognized` | Python isn't on PATH: reinstall and tick "Add python.exe to PATH" (Step 1) |
   | `The module '.venv' could not be loaded` | The environment doesn't exist in this folder yet: run `python -m venv .venv` first (Step 5), then `.\.venv\Scripts\Activate.ps1` (keep the `.\` at the start) |
   | `No module named ...` | You forgot to activate `.venv` (Step 5), or run `pip install -r requirements.txt` again |
   | `No folder for 'Mirai'` / `No *_dataset.csv` | Data isn't in `data/raw/<Attack>/` (Step 6) |
   | `KitNET not found` | Do Step 7 |
   | `MemoryError` or the computer freezes | Close other apps; or test with `--limit 200000` |
3. Still stuck after 20 minutes? Comment on your GitHub issue with the **command you ran** and the **full error text** (copy-paste, not a photo), then post the issue link in the team chat.
