"""scheduler.py — the cronjobs engine for your twin.

You normally DON'T run this separately. The integration wires `start_scheduler()`
into your twin's startup so it runs in the SAME process as your chat/bot (in a
background thread) — no second process to remember. It can also run standalone
with `python scheduler.py`.

Every POLL_S it reads data/jobs.json and fires due jobs. A job with `prompt` runs
your twin (`claude -p`, in your voice); with `message` sends literal text.
Delivery = console + macOS notification, and Slack if a token + channel are set.
Jobs are created via the schedule-task skill -> schedule.py (never hand-edited).
"""

import json
import os
import subprocess
import threading
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TWIN_DIR = Path(os.environ.get("TWIN_DIR", Path(__file__).resolve().parent)).resolve()
JOBS_FILE = Path(os.environ.get("JOBS_FILE", Path(__file__).resolve().parent / "data" / "jobs.json"))
POLL_S = max(2, int(os.environ.get("POLL_MS", "30000")) // 1000)
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")


def load_jobs() -> list:
    try:
        raw = JOBS_FILE.read_text().strip()
        if not raw:
            return []
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_jobs(jobs: list) -> None:
    JOBS_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = JOBS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(jobs, indent=2))
    tmp.replace(JOBS_FILE)


def _field_match(field: str, value: int) -> bool:
    if field == "*":
        return True
    for part in field.split(","):
        if "/" in part:
            rng, step_str = part.split("/")
            step = int(step_str)
            if rng == "*":
                if step and value % step == 0:
                    return True
            else:
                base = int(rng)
                if value >= base and step and (value - base) % step == 0:
                    return True
        elif "-" in part:
            a, b = (int(x) for x in part.split("-"))
            if a <= value <= b:
                return True
        elif int(part) == value:
            return True
    return False


def cron_matches(expr: str, d: datetime) -> bool:
    parts = expr.strip().split()
    if len(parts) != 5:
        return False
    mi, ho, dom, mo, dow = parts
    cron_dow = (d.weekday() + 1) % 7
    return (
        _field_match(mi, d.minute) and _field_match(ho, d.hour)
        and _field_match(dom, d.day) and _field_match(mo, d.month)
        and _field_match(dow, cron_dow)
    )


def minute_key(d: datetime) -> str:
    return d.strftime("%Y-%m-%dT%H:%M")


def is_due(job: dict, now: datetime) -> bool:
    if job.get("status") == "done":
        return False
    if job.get("runAt"):
        try:
            return datetime.fromisoformat(job["runAt"]) <= now
        except ValueError:
            return False
    if job.get("cron"):
        return cron_matches(job["cron"], now) and job.get("lastRun") != minute_key(now)
    return False


def run_twin(prompt: str) -> str:
    try:
        res = subprocess.run(
            ["claude", "-p", prompt, "--permission-mode", "bypassPermissions"],
            cwd=str(TWIN_DIR), capture_output=True, text=True,
        )
    except FileNotFoundError:
        return "(couldn't start `claude` — is Claude Code installed and logged in?)"
    if res.returncode != 0:
        return f"(twin error: {(res.stderr or 'unknown').strip()})"
    return res.stdout.strip()


def deliver(text: str, job: dict) -> None:
    title = job.get("title", "reminder")
    # Print as a visible block so it shows up right in the terminal chat.
    print(f"\n\n⏰ twin (scheduled — {title}) ›\n{text}\n")
    try:
        safe = text.replace('"', '\\"')
        safe_title = f"Agent: {title}".replace('"', '\\"')
        subprocess.run(["osascript", "-e", f'display notification "{safe}" with title "{safe_title}"'], check=False)
    except Exception:
        pass
    channel = job.get("channel") or SLACK_CHANNEL
    if SLACK_BOT_TOKEN and channel:
        try:
            req = urllib.request.Request(
                "https://slack.com/api/chat.postMessage",
                data=json.dumps({"channel": channel, "text": text}).encode(),
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception as e:
            print(f"[slack] post failed: {e}")


def run_job(job: dict) -> None:
    text = run_twin(job["prompt"]) if job.get("prompt") else job.get("message", "(empty job)")
    deliver(text, job)


def tick() -> None:
    jobs = load_jobs()
    now = datetime.now()
    changed = False
    for job in jobs:
        if not is_due(job, now):
            continue
        run_job(job)
        job["lastRun"] = minute_key(now)
        if job.get("runAt"):
            job["status"] = "done"
        changed = True
    if changed:
        save_jobs(jobs)


_started = False


def _loop() -> None:
    while True:
        try:
            tick()
        except Exception as e:
            print(f"[tick] error: {e}")
        time.sleep(POLL_S)


def start_scheduler() -> None:
    """Start the polling loop in a background daemon thread. Call once from your
    twin's startup so scheduled jobs fire in the same process as your twin."""
    global _started
    if _started:
        return
    _started = True
    print(f"⏰ Scheduler active (checks every {POLL_S}s). Jobs: {JOBS_FILE}")
    threading.Thread(target=_loop, daemon=True).start()


if __name__ == "__main__":
    # Standalone mode (optional): blocks here running the loop in the foreground.
    print(f"⏰ Scheduler running standalone. Jobs: {JOBS_FILE}")
    while True:
        try:
            tick()
        except Exception as e:
            print(f"[tick] error: {e}")
        time.sleep(POLL_S)
