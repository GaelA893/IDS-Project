"""Undo the Nov 25 consolidated-plan changes to issues and milestones.

    python setup/backups/restore_v3.py            # dry run: shows what it would change
    python setup/backups/restore_v3.py --apply    # actually restore (needs gh, logged in)

Restores every issue and milestone to the snapshot taken just before the changes
(issues-2026-11-25.json, milestones-2026-11-25.json): title, body, open/closed state,
milestone, labels, assignees. Issues created by the plan (listed in v3-applied.json)
are closed with a comment. Nothing is deleted. Code changes are separate pull requests;
undo those by closing or reverting the PR on GitHub.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = "GaelA893/IDS-Project"
HERE = Path(__file__).resolve().parent
APPLY = "--apply" in sys.argv

issues = json.loads((HERE / "issues-2026-11-25.json").read_text(encoding="utf-8"))
milestones = json.loads((HERE / "milestones-2026-11-25.json").read_text(encoding="utf-8"))
applied_file = HERE / "v3-applied.json"
applied = json.loads(applied_file.read_text(encoding="utf-8")) if applied_file.exists() else {"created_issues": []}


def gh(method, path, payload):
    print(f"{'APPLY' if APPLY else 'dry-run'}: {method} {path} {list(payload)}")
    if APPLY:
        subprocess.run(["gh", "api", "-X", method, f"repos/{REPO}/{path}", "--input", "-"],
                       input=json.dumps(payload), text=True, check=True, stdout=subprocess.DEVNULL)


for m in milestones:
    gh("PATCH", f"milestones/{m['number']}",
       {"title": m["title"], "description": m["description"] or "", "due_on": m["due_on"], "state": m["state"]})

for i in issues:
    payload = {"title": i["title"], "body": i["body"] or "", "state": i["state"],
               "milestone": i["milestone"], "labels": i["labels"], "assignees": i["assignees"]}
    if i["state"] == "closed" and i.get("state_reason"):
        payload["state_reason"] = i["state_reason"]
    gh("PATCH", f"issues/{i['number']}", payload)

for n in applied.get("created_issues", []):
    gh("POST", f"issues/{n}/comments", {"body": "Reverted: the Nov 25 consolidated plan was rolled back."})
    gh("PATCH", f"issues/{n}", {"state": "closed", "state_reason": "not_planned"})

print("\nDone." if APPLY else "\nDry run only. Re-run with --apply to restore.")
