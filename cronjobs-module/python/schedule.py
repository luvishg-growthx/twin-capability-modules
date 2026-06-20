"""schedule.py — deterministically add a job to data/jobs.json.

Your twin calls THIS (via Bash, from the schedule-task skill) instead of
hand-editing JSON, so scheduling is reliable. scheduler.py fires the job.

Usage:
  python schedule.py --at "2026-06-20T19:15:00" --message "hi!"
  python schedule.py --at "2026-06-20T19:15:00" --prompt "Write me a hi message"
  python schedule.py --cron "30 9 * * 1-5" --message "standup!"
  optional: --title "label"  --channel "C0123 or U0123"

--at is LOCAL time, ISO, no timezone suffix. --prompt lets the twin compose the
message in your voice at fire time; --message is exact text.
"""

import json
import os
import sys
import uuid
from pathlib import Path

JOBS_FILE = Path(os.environ.get("JOBS_FILE", Path(__file__).resolve().parent / "data" / "jobs.json"))


def parse_args(argv):
    flags = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--"):
            key = a[2:]
            nxt = argv[i + 1] if i + 1 < len(argv) else None
            if nxt is None or nxt.startswith("--"):
                flags[key] = True
            else:
                flags[key] = nxt
                i += 1
        i += 1
    return flags


flags = parse_args(sys.argv[1:])

if not flags.get("at") and not flags.get("cron"):
    print('Need --at "<ISO local time>" or --cron "<expr>".', file=sys.stderr)
    sys.exit(1)
if not flags.get("message") and not flags.get("prompt"):
    print("Need --message <text> or --prompt <instruction>.", file=sys.stderr)
    sys.exit(1)

job = {
    "id": uuid.uuid4().hex[:8],
    "title": flags.get("title") or (str(flags["message"])[:40] if flags.get("message") else "scheduled task"),
    "status": "pending",
    "lastRun": None,
}
if flags.get("at"):
    job["runAt"] = str(flags["at"])
if flags.get("cron"):
    job["cron"] = str(flags["cron"])
if flags.get("prompt"):
    job["prompt"] = str(flags["prompt"])
if flags.get("message"):
    job["message"] = str(flags["message"])
if flags.get("channel"):
    job["channel"] = str(flags["channel"])

JOBS_FILE.parent.mkdir(parents=True, exist_ok=True)
jobs = []
try:
    raw = JOBS_FILE.read_text().strip()
    if raw:
        jobs = json.loads(raw)
    if not isinstance(jobs, list):
        jobs = []
except Exception:
    jobs = []
jobs.append(job)
JOBS_FILE.write_text(json.dumps(jobs, indent=2))

where = f'at {job["runAt"]}' if job.get("runAt") else f'on cron "{job["cron"]}"'
print(f'scheduled "{job["title"]}" {where} (id {job["id"]})')
