# Guide: add cronjobs / scheduled messages to your agent (Python)

**You are Claude Code or Codex (or any coding agent), reading this file inside the user's agent project.** These files are ready-made — don't rebuild the feature from scratch; just install/wire them in as described below. Your
job: let their agent **schedule future and recurring messages** — "send me a hi
message at 7:30pm", "remind me every weekday at 9am" — and have it **just work**
with no manual steps. Everything you need is embedded.

> ## ⚠️ First: confirm the stack
> Check whether the user's agent is **Node.js** (`package.json` / `*.js`) or
> **Python** (`requirements.txt` / `*.py`) — ask if unclear. **This is the
> Python guide.** If their agent is **Node.js**, stop and follow
> `guide for implementing cronjobs.md` instead.

**Do all of this for the user — install deps, write files, AND wire the scheduler
to auto-start. Don't leave them a separate process to run.**

---

## The prompt the user pastes (for reference)

> Read `guide for implementing cronjobs.md` from
> `https://raw.githubusercontent.com/luvishg-growthx/cronjobs-and-reminders-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20cronjobs.md`
> and set up scheduled tasks / cronjobs for my agent.

(For a Python twin, point the same prompt at
`https://raw.githubusercontent.com/luvishg-growthx/cronjobs-and-reminders-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20cronjobs%20(python).md`.)

---

## How it works (no manual steps)

- The agent **creates** a job by running `schedule.py` (a deterministic CLI) when
  the user asks — scheduling never depends on the model hand-editing JSON.
- The **scheduler auto-starts inside the twin** in a background thread (you wire
  `start_scheduler()` into the twin's startup), so jobs fire in the same process
  — no second terminal.
- A `prompt` job runs the twin (`claude -p`, in the user's voice); a `message`
  job sends literal text. Delivery = desktop notification + console, and Slack if
  a token + channel are set.

---

## Step 1 — Dependency

```
pip install python-dotenv
```

(Add `python-dotenv>=1.0.0` to `requirements.txt`.)

---

## Step 2 — Create `schedule.py` (the job-creator CLI)

Create `schedule.py` in the project **root**:

```python
"""schedule.py — deterministically add a job to data/jobs.json."""
import json, os, sys, uuid
from pathlib import Path

JOBS_FILE = Path(os.environ.get("JOBS_FILE", Path(__file__).resolve().parent / "data" / "jobs.json"))


def parse_args(argv):
    flags, i = {}, 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--"):
            key = a[2:]
            nxt = argv[i + 1] if i + 1 < len(argv) else None
            if nxt is None or nxt.startswith("--"):
                flags[key] = True
            else:
                flags[key] = nxt; i += 1
        i += 1
    return flags


flags = parse_args(sys.argv[1:])
if not flags.get("at") and not flags.get("cron"):
    print('Need --at "<ISO local time>" or --cron "<expr>".', file=sys.stderr); sys.exit(1)
if not flags.get("message") and not flags.get("prompt"):
    print("Need --message <text> or --prompt <instruction>.", file=sys.stderr); sys.exit(1)

job = {
    "id": uuid.uuid4().hex[:8],
    "title": flags.get("title") or (str(flags["message"])[:40] if flags.get("message") else "scheduled task"),
    "status": "pending", "lastRun": None,
}
for k in ("at", "cron", "prompt", "message", "channel"):
    if flags.get(k):
        job["runAt" if k == "at" else k] = str(flags[k])

JOBS_FILE.parent.mkdir(parents=True, exist_ok=True)
jobs = []
try:
    raw = JOBS_FILE.read_text().strip()
    if raw: jobs = json.loads(raw)
    if not isinstance(jobs, list): jobs = []
except Exception:
    jobs = []
jobs.append(job)
JOBS_FILE.write_text(json.dumps(jobs, indent=2))
where = f'at {job["runAt"]}' if job.get("runAt") else f'on cron "{job["cron"]}"'
print(f'scheduled "{job["title"]}" {where} (id {job["id"]})')
```

---

## Step 3 — Create `scheduler.py` (the engine, auto-startable)

Create `scheduler.py` in the project **root**:

```python
"""scheduler.py — fires due jobs. Wired into the twin's startup (Step 4) via
start_scheduler() (background thread); can also run standalone."""
import json, os, subprocess, threading, time, urllib.request
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
TWIN_DIR = Path(os.environ.get("TWIN_DIR", Path(__file__).resolve().parent)).resolve()
JOBS_FILE = Path(os.environ.get("JOBS_FILE", Path(__file__).resolve().parent / "data" / "jobs.json"))
POLL_S = max(2, int(os.environ.get("POLL_MS", "30000")) // 1000)
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")


def load_jobs():
    try:
        raw = JOBS_FILE.read_text().strip()
        if not raw: return []
        d = json.loads(raw); return d if isinstance(d, list) else []
    except Exception:
        return []


def save_jobs(jobs):
    JOBS_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = JOBS_FILE.with_suffix(".tmp"); tmp.write_text(json.dumps(jobs, indent=2)); tmp.replace(JOBS_FILE)


def _field_match(field, value):
    if field == "*": return True
    for part in field.split(","):
        if "/" in part:
            rng, s = part.split("/"); step = int(s)
            if rng == "*":
                if step and value % step == 0: return True
            else:
                base = int(rng)
                if value >= base and step and (value - base) % step == 0: return True
        elif "-" in part:
            a, b = (int(x) for x in part.split("-"))
            if a <= value <= b: return True
        elif int(part) == value:
            return True
    return False


def cron_matches(expr, d):
    p = expr.strip().split()
    if len(p) != 5: return False
    cron_dow = (d.weekday() + 1) % 7
    return (_field_match(p[0], d.minute) and _field_match(p[1], d.hour) and _field_match(p[2], d.day)
            and _field_match(p[3], d.month) and _field_match(p[4], cron_dow))


def minute_key(d): return d.strftime("%Y-%m-%dT%H:%M")


def is_due(job, now):
    if job.get("status") == "done": return False
    if job.get("runAt"):
        try: return datetime.fromisoformat(job["runAt"]) <= now
        except ValueError: return False
    if job.get("cron"): return cron_matches(job["cron"], now) and job.get("lastRun") != minute_key(now)
    return False


def run_twin(prompt):
    try:
        res = subprocess.run(["claude", "-p", prompt, "--permission-mode", "bypassPermissions"],
                             cwd=str(TWIN_DIR), capture_output=True, text=True)
    except FileNotFoundError:
        return "(couldn't start `claude` — is Claude Code installed and logged in?)"
    if res.returncode != 0: return f"(twin error: {(res.stderr or 'unknown').strip()})"
    return res.stdout.strip()


def deliver(text, job):
    title = job.get("title", "reminder")
    print(f"\n\n⏰ twin (scheduled — {title}) ›\n{text}\n")
    try:
        safe = text.replace('"', '\\"'); st = f"Agent: {title}".replace('"', '\\"')
        subprocess.run(["osascript", "-e", f'display notification "{safe}" with title "{st}"'], check=False)
    except Exception:
        pass
    channel = job.get("channel") or SLACK_CHANNEL
    if SLACK_BOT_TOKEN and channel:
        try:
            req = urllib.request.Request("https://slack.com/api/chat.postMessage",
                data=json.dumps({"channel": channel, "text": text}).encode(),
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {SLACK_BOT_TOKEN}"})
            urllib.request.urlopen(req, timeout=10)
        except Exception as e:
            print(f"[slack] post failed: {e}")


def run_job(job):
    text = run_twin(job["prompt"]) if job.get("prompt") else job.get("message", "(empty job)")
    deliver(text, job)


def tick():
    jobs = load_jobs(); now = datetime.now(); changed = False
    for job in jobs:
        if not is_due(job, now): continue
        run_job(job); job["lastRun"] = minute_key(now)
        if job.get("runAt"): job["status"] = "done"
        changed = True
    if changed: save_jobs(jobs)


_started = False


def _loop():
    while True:
        try: tick()
        except Exception as e: print(f"[tick] error: {e}")
        time.sleep(POLL_S)


def start_scheduler():
    """Start the loop in a background daemon thread. Call once from the twin's startup."""
    global _started
    if _started: return
    _started = True
    print(f"⏰ Scheduler active (checks every {POLL_S}s).")
    threading.Thread(target=_loop, daemon=True).start()


if __name__ == "__main__":
    print(f"⏰ Scheduler running standalone. Jobs: {JOBS_FILE}")
    while True:
        try: tick()
        except Exception as e: print(f"[tick] error: {e}")
        time.sleep(POLL_S)
```

---

## Step 4 — AUTO-START it inside the twin (the important bit)

Find the twin's entry point — where it starts the chat loop (e.g. `if __name__
== "__main__":` / the `while True: input(...)` in `twin.py`). Add, before the
loop starts:

```python
from scheduler import start_scheduler
start_scheduler()
```

Now `python twin.py` runs the chat **and** the scheduler thread together — the
user never starts a second process.

> If there's truly no editable entry point, fall back to telling the user to run
> `python scheduler.py` in a second terminal — but prefer wiring it in.

---

## Step 4b — Make sure the twin can RUN the schedule command (critical)

The skill schedules by running `python schedule.py` via **Bash**. If the twin's
`claude -p` dispatch can't use Bash, that command is **blocked** — the twin will
then claim it "needs approval" and silently fail to schedule. Prevent this:

- If the twin's dispatch uses `--permission-mode bypassPermissions` → you're done.
- If it uses an `--allowedTools` allowlist → **add `Bash`** (and `Skill`) to it.

This is the #1 cause of "I scheduled it but nothing happened." The twin must
*actually run* the command, never ask the user to approve it.

## Step 5 — Install the schedule-task skill

Create `.claude/skills/schedule-task/SKILL.md`:

````markdown
---
name: schedule-task
description: Schedule a future or recurring message/task for the user (e.g. "send me a hi message at 2:30pm tomorrow", "remind me every weekday at 9am"). Trigger whenever the user asks to schedule, remind, or send something at a later time or on a repeating schedule.
---

# Schedule a task

When the user asks to schedule/remind/send something later, you MUST record the
job by running the `schedule.py` CLI via Bash. Don't just say "I'll remind you" —
if you don't run the command, nothing is scheduled. The scheduler runs inside the
twin and fires the job at its time.

## Step 1 — current time
Run: `date "+%Y-%m-%dT%H:%M:%S"`

## Step 2 — work out the time
- "at 7:30" / "7:30pm" → today (or tomorrow if already past) at `19:30:00`.
- "in 10 minutes" → now + 10 min. Use 24-hour local ISO, no timezone suffix.
- Recurring → 5-field cron: `minute hour day-of-month month day-of-week`
  (day-of-week 0=Sun..6=Sat). Every weekday 9am → `0 9 * * 1-5`.

## Step 3 — run the CLI (the actual scheduling)
```
python schedule.py --at "2026-06-20T19:30:00" --prompt "Write a short, friendly hi message." --title "hi message"
python schedule.py --at "2026-06-20T19:30:00" --message "Don't forget the call." --title "call reminder"
python schedule.py --cron "0 9 * * 1-5" --message "Standup in 30 minutes."
```

## Step 4 — confirm
Report what you scheduled. The scheduler is already running inside the twin, so it
fires automatically — no separate process. Delivery = desktop notification (plus
Slack if SLACK_BOT_TOKEN + SLACK_CHANNEL are set).
````

---

## Step 6 — Ignore runtime state, restart, & verify

1. Add `data/jobs.json` and `.env` to `.gitignore`.
2. **Restart the twin** so the running process picks up the new code (a twin
   started before this change won't have the scheduler or Bash permission).
3. End-to-end check: ask the twin "send me a hi message in 2 minutes". Confirm a
   job appears in `data/jobs.json`, and ~2 min later the scheduled message prints
   in the terminal + a notification. No second process needed, and the twin must
   NOT ask you to approve anything.

---

## Guardrails (do these, quietly)

- **Make it automatic.** Wire `start_scheduler()` into the twin's startup; never
  leave the user to run a separate scheduler.
- The skill **must run `schedule.py`** (deterministic) — never hand-edit JSON.
- One-shot = `runAt`; recurring = `cron`. Never both. Never both `prompt` and
  `message`. Times are local (no timezone suffix).
- Don't touch `CLAUDE.md` / persona — the voice stays the user's.

When done, summarize in 3 lines: files added, that the scheduler auto-starts with
the twin, and an example phrase to try.
