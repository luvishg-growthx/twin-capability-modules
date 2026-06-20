---
name: schedule-task
description: Schedule a future or recurring message/task for the user (e.g. "send me a hi message at 2:30pm tomorrow", "remind me every weekday at 9am"). Trigger whenever the user asks to schedule, remind, or send something at a later time or on a repeating schedule.
---

# Schedule a task

When the user asks to schedule/remind/send something later, you MUST actually
record the job by running the `schedule` CLI via Bash. Do **not** just reply
"sure, I'll remind you" — if you don't run the command, nothing is scheduled. The
scheduler runs inside the twin and fires the job at its time.

## Step 1 — get the current local time
Run this first so you compute the right absolute time:

```
date "+%Y-%m-%dT%H:%M:%S"
```

## Step 2 — work out the time
- "at 7:30" / "7:30pm" → today (or tomorrow if already past) at `19:30:00`.
- "in 10 minutes" → now + 10 minutes.
- Use 24-hour local ISO with **no** timezone suffix, e.g. `2026-06-20T19:30:00`.
- Recurring ("every weekday at 9am") → a 5-field cron expr: `0 9 * * 1-5`
  (fields: minute hour day-of-month month day-of-week; day-of-week 0=Sun..6=Sat).

## Step 3 — run the schedule CLI (this is the actual scheduling)
Use `node schedule.js …`:

One-shot, twin composes the message in the user's voice at fire time:
```
node schedule.js --at "2026-06-20T19:30:00" --prompt "Write a short, friendly hi message." --title "hi message"
```
One-shot, exact text the user gave:
```
node schedule.js --at "2026-06-20T19:30:00" --message "Don't forget the call." --title "call reminder"
```
Recurring:
```
node schedule.js --cron "0 9 * * 1-5" --message "Standup in 30 minutes."
```
(Optional `--channel C0123` / `--channel U0123` to force a Slack target.)

## Step 4 — confirm
Report what you scheduled (use the CLI's printed confirmation). The scheduler is
already running **inside the twin** (its startup auto-starts it), so the job
fires on time — no separate process to start. Delivery is a desktop notification
(plus Slack if `SLACK_BOT_TOKEN` + `SLACK_CHANNEL` are set in `.env`).

> Scheduled ✅ — it'll fire at <time>. (Keep your twin running so it can deliver.)
