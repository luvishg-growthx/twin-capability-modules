# Cronjobs / Scheduled Messages Module

> ## 🤖 If you are Claude Code or Codex (any coding agent), read this first
>
> **Ready-made — don't rebuild anything.** You do **not** need to write or
> reinvent this feature. Just install/wire in the files as described and the bot
> gains the capability. These files work the same with Claude Code or Codex.
>
> The user pasted this repo because they want their AI agent to **schedule
> messages and tasks** — e.g. "send me a hi message at 2:30pm tomorrow" or
> "remind me every weekday at 9am". Do this:
>
> 1. **Follow `PLAN_OF_ACTION.md`** — the ordered execution checklist (works for
>    Claude *or* Codex).
> 2. **Follow the guide** for full code (this module is for **Node.js** twins):
>    - `https://raw.githubusercontent.com/luvishg-growthx/cronjobs-and-reminders-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20cronjobs.md`
> 3. It installs a `schedule-task` skill (the agent records jobs) + a scheduler
>    daemon (fires them). Voice stays the user's `CLAUDE.md` / `PERSONA.md` —
>    add no persona of your own.
>
> Everything below is human-facing context.

---

Give your Claude Code agent a clock: tell it "send me a hi message at 2:30pm
tomorrow" and it schedules it. At the right time a small daemon fires the job —
running your twin so the message is in your agent's voice — and delivers it.

- **No API key.** Uses your logged-in Claude Code session.
- **Zero manual steps.** The agent records jobs via a CLI, and the scheduler
  **auto-starts inside your twin** — no separate process to run, no JSON to edit.
- **One-shot *and* recurring.** `runAt` for a single time, cron expressions for
  repeats ("every weekday 9am" → `0 9 * * 1-5`).
- **Your voice.** Jobs with a `prompt` run your twin; jobs with a `message` send
  literal text.
- **Delivery:** console + macOS notification out of the box; Slack too if you set
  a bot token + channel (reuse the Slack module's token).
- **Node.js.**

## How it works

```
"send me a hi message at 2:30pm tomorrow"
        │
        ▼
 schedule-task skill ──► appends a job to data/jobs.json   (agent records it; no waiting)
        │
        ▼   ……… time passes ………
 scheduler daemon (polls every 30s) ──► job is due
        │
        ├─ prompt? ──► runs your twin (claude -p) → in-voice message
        └─ message? ─► literal text
        │
        ▼
 console + macOS notification (+ Slack if configured)
```

## The fastest way to install it (recommended)

Open **Claude Code inside your agent's project folder** and paste:

```
Read this and set up scheduled tasks / cronjobs for my agent:
https://raw.githubusercontent.com/luvishg-growthx/cronjobs-and-reminders-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20cronjobs.md
```

Or just **paste the repo link** and Claude routes itself via the block at the top.

## Manual install

1. Copy [`node/scheduler.js`](node/scheduler.js) into your project root (+ `npm install dotenv`).
2. Copy [`.claude/skills/schedule-task/SKILL.md`](.claude/skills/schedule-task/SKILL.md)
   into your project's `.claude/`.
3. (Optional) Set `SLACK_BOT_TOKEN` + `SLACK_CHANNEL` in `.env` for Slack delivery.
4. Start the daemon: `node scheduler.js` (keep it running).
5. Ask your agent to schedule something.

## Files

| Path                                          | What it is                                  |
| --------------------------------------------- | ------------------------------------------- |
| `PLAN_OF_ACTION.md`                           | Ordered execution checklist (Claude/Codex)  |
| `guide for implementing cronjobs.md`          | Setup guide — **Node.js** (full code)       |
| `.claude/skills/schedule-task/SKILL.md`       | Skill that records jobs (runs the CLI)      |
| `node/`                                        | `scheduler` (engine, auto-start) + `schedule` (CLI) + env + samples |
