# Guide: add cronjobs / scheduled messages to your agent (Node.js)

**You are Claude Code or Codex (or any coding agent), reading this file inside the user's agent project.** These files are ready-made — don't rebuild the feature from scratch; just install/wire them in as described below. Your
job: let their agent **schedule future and recurring messages** — "send me a hi
message at 7:30pm", "remind me every weekday at 9am" — and have it **just work**
with no manual steps. Everything you need is embedded.

> This module is for **Node.js** twins.

**Do all of this for the user — install deps, write files, AND wire the scheduler
to auto-start. Don't leave them a separate process to run.**

---

## The prompt the user pastes (for reference)

> Read `guide for implementing cronjobs.md` from
> `https://raw.githubusercontent.com/luvishg-growthx/cronjobs-and-reminders-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20cronjobs.md`
> and set up scheduled tasks / cronjobs for my agent.

---

## How it works (no manual steps)

- The agent **creates** a job by running `schedule.js` (a deterministic CLI) when
  the user asks — so scheduling never depends on the model hand-editing JSON.
- The **scheduler auto-starts inside the twin** (you wire `startScheduler()` into
  the twin's startup), so jobs fire in the same process — no second terminal.
- A job with a `prompt` runs the twin (`claude -p`, in the user's voice); a job
  with a `message` sends literal text. Delivery = desktop notification + console,
  and Slack too if a token + channel are set.

---

## Step 1 — Install the dependency

```
npm install dotenv
```

(No `package.json`? `npm init -y` first.) Requires **Node ≥ 18**.

---

## Step 2 — Create `schedule.js` (the job-creator CLI)

Create `schedule.js` in the project **root**:

```javascript
// schedule.js — deterministically add a job to data/jobs.json.
const fs = require("fs");
const path = require("path");
const { randomUUID } = require("crypto");

const JOBS_FILE = process.env.JOBS_FILE
  ? path.resolve(process.env.JOBS_FILE)
  : path.join(__dirname, "data", "jobs.json");

function parseArgs(argv) {
  const flags = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith("--")) flags[key] = true;
      else { flags[key] = next; i++; }
    }
  }
  return flags;
}
const flags = parseArgs(process.argv.slice(2));
if (!flags.at && !flags.cron) { console.error('Need --at "<ISO local time>" or --cron "<expr>".'); process.exit(1); }
if (!flags.message && !flags.prompt) { console.error("Need --message <text> or --prompt <instruction>."); process.exit(1); }

const job = {
  id: randomUUID().slice(0, 8),
  title: flags.title || (flags.message ? String(flags.message).slice(0, 40) : "scheduled task"),
  status: "pending",
  lastRun: null,
};
if (flags.at) job.runAt = String(flags.at);
if (flags.cron) job.cron = String(flags.cron);
if (flags.prompt) job.prompt = String(flags.prompt);
if (flags.message) job.message = String(flags.message);
if (flags.channel) job.channel = String(flags.channel);

fs.mkdirSync(path.dirname(JOBS_FILE), { recursive: true });
let jobs = [];
try { const raw = fs.readFileSync(JOBS_FILE, "utf8").trim(); if (raw) jobs = JSON.parse(raw); if (!Array.isArray(jobs)) jobs = []; } catch (_) { jobs = []; }
jobs.push(job);
fs.writeFileSync(JOBS_FILE, JSON.stringify(jobs, null, 2));
console.log(`scheduled "${job.title}" ${job.runAt ? `at ${job.runAt}` : `on cron "${job.cron}"`} (id ${job.id})`);
```

---

## Step 3 — Create `scheduler.js` (the engine, auto-startable)

Create `scheduler.js` in the project **root**:

```javascript
// scheduler.js — fires due jobs. Wired into the twin's startup (Step 4) so it
// runs in the same process; can also run standalone with `node scheduler.js`.
const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");
require("dotenv").config();

const TWIN_DIR = process.env.TWIN_DIR ? path.resolve(process.env.TWIN_DIR) : __dirname;
const JOBS_FILE = process.env.JOBS_FILE ? path.resolve(process.env.JOBS_FILE) : path.join(__dirname, "data", "jobs.json");
const POLL_MS = Number(process.env.POLL_MS || 30000);
const SLACK_BOT_TOKEN = process.env.SLACK_BOT_TOKEN;
const SLACK_CHANNEL = process.env.SLACK_CHANNEL;

function loadJobs() {
  try { const raw = fs.readFileSync(JOBS_FILE, "utf8").trim(); if (!raw) return []; const d = JSON.parse(raw); return Array.isArray(d) ? d : []; } catch (_) { return []; }
}
function saveJobs(jobs) { fs.mkdirSync(path.dirname(JOBS_FILE), { recursive: true }); const tmp = JOBS_FILE + ".tmp"; fs.writeFileSync(tmp, JSON.stringify(jobs, null, 2)); fs.renameSync(tmp, JOBS_FILE); }

function fieldMatch(field, value) {
  if (field === "*") return true;
  for (const part of field.split(",")) {
    if (part.includes("/")) { const [r, s] = part.split("/"); const step = Number(s); if (r === "*") { if (step && value % step === 0) return true; } else { const b = Number(r); if (value >= b && step && (value - b) % step === 0) return true; } }
    else if (part.includes("-")) { const [a, b] = part.split("-").map(Number); if (value >= a && value <= b) return true; }
    else if (Number(part) === value) return true;
  }
  return false;
}
function cronMatches(expr, d) {
  const p = expr.trim().split(/\s+/); if (p.length !== 5) return false;
  return fieldMatch(p[0], d.getMinutes()) && fieldMatch(p[1], d.getHours()) && fieldMatch(p[2], d.getDate()) && fieldMatch(p[3], d.getMonth() + 1) && fieldMatch(p[4], d.getDay());
}
const minuteKey = (d) => d.toISOString().slice(0, 16);
function isDue(job, now) {
  if (job.status === "done") return false;
  if (job.runAt) return new Date(job.runAt) <= now;
  if (job.cron) return cronMatches(job.cron, now) && job.lastRun !== minuteKey(now);
  return false;
}
function runTwin(prompt) {
  const res = spawnSync("claude", ["-p", prompt, "--permission-mode", "bypassPermissions"], { cwd: TWIN_DIR, encoding: "utf8", maxBuffer: 1024 * 1024 * 10 });
  if (res.status !== 0) return `(twin error: ${(res.stderr || res.error || "unknown").toString().trim()})`;
  return res.stdout.trim();
}
async function deliver(text, job) {
  const title = job.title || "reminder";
  process.stdout.write(`\n\n⏰ twin (scheduled — ${title}) ›\n${text}\n`);
  try { spawnSync("osascript", ["-e", `display notification ${JSON.stringify(text)} with title ${JSON.stringify("Agent: " + title)}`]); } catch (_) {}
  const channel = job.channel || SLACK_CHANNEL;
  if (SLACK_BOT_TOKEN && channel) {
    try { await fetch("https://slack.com/api/chat.postMessage", { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${SLACK_BOT_TOKEN}` }, body: JSON.stringify({ channel, text }) }); } catch (e) { console.error("[slack] post failed:", e.message); }
  }
}
async function runJob(job) { const text = job.prompt ? runTwin(job.prompt) : job.message || "(empty job)"; await deliver(text, job); }
async function tick() {
  const jobs = loadJobs(); const now = new Date(); let changed = false;
  for (const job of jobs) { if (!isDue(job, now)) continue; await runJob(job); job.lastRun = minuteKey(now); if (job.runAt) job.status = "done"; changed = true; }
  if (changed) saveJobs(jobs);
}
let started = false;
function startScheduler() {
  if (started) return null; started = true;
  console.log(`⏰ Scheduler active (checks every ${Math.round(POLL_MS / 1000)}s).`);
  tick().catch((e) => console.error("[tick] error:", e.message));
  return setInterval(() => tick().catch((e) => console.error("[tick] error:", e.message)), POLL_MS);
}
module.exports = { startScheduler };
if (require.main === module) startScheduler();
```

---

## Step 4 — AUTO-START it inside the twin (the important bit)

Find the twin's entry point — where it starts the terminal chat / Slack bot
(e.g. the `main()` / readline setup in `twin.js`, or the startup in
`slack-bot.js`). Add this so the scheduler runs in the same process:

```javascript
require("./scheduler.js").startScheduler();
```

Put it at startup (e.g. just before the readline prompt, or right after the Slack
app starts). Now `node twin.js` (or the bot) runs the chat **and** the scheduler
together — the user never starts a second process.

> If the twin truly has no single entry point you can edit, fall back to telling
> the user to run `node scheduler.js` in a second terminal — but prefer wiring
> it in.

---

## Step 4b — Make sure the twin can RUN the schedule command (critical)

The skill schedules by running `node schedule.js` via **Bash**. If the twin's
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
job by running the `schedule.js` CLI via Bash. Don't just say "I'll remind you" —
if you don't run the command, nothing is scheduled. The scheduler runs inside
the twin and fires the job at its time.

## Step 1 — current time
Run: `date "+%Y-%m-%dT%H:%M:%S"`

## Step 2 — work out the time
- "at 7:30" / "7:30pm" → today (or tomorrow if already past) at `19:30:00`.
- "in 10 minutes" → now + 10 min. Use 24-hour local ISO, no timezone suffix.
- Recurring → 5-field cron: `minute hour day-of-month month day-of-week`
  (day-of-week 0=Sun..6=Sat). Every weekday 9am → `0 9 * * 1-5`.

## Step 3 — run the CLI (the actual scheduling)
```
node schedule.js --at "2026-06-20T19:30:00" --prompt "Write a short, friendly hi message." --title "hi message"
node schedule.js --at "2026-06-20T19:30:00" --message "Don't forget the call." --title "call reminder"
node schedule.js --cron "0 9 * * 1-5" --message "Standup in 30 minutes."
```

## Step 4 — confirm
Report what you scheduled. The scheduler is already running inside the twin, so
it fires automatically — no separate process. Delivery = desktop notification
(plus Slack if SLACK_BOT_TOKEN + SLACK_CHANNEL are set).
````

---

## Step 6 — Ignore runtime state, restart, & verify

1. Add `data/jobs.json` and `.env` to `.gitignore`.
2. **Restart the twin** so the running process picks up the new code (a twin
   started before this change won't have the scheduler or Bash permission).
3. End-to-end check: ask the twin "send me a hi message in 2 minutes". Confirm a
   job appears in `data/jobs.json` (via `schedule.js`), and ~2 min later the
   scheduled message prints in the terminal + a notification appears. No second
   process should be needed, and the twin must NOT ask you to approve anything.

---

## Guardrails (do these, quietly)

- **Make it automatic.** Wire `startScheduler()` into the twin's startup; never
  leave the user to run a separate scheduler.
- The skill **must run `schedule.js`** (deterministic) — never hand-edit JSON.
- One-shot = `runAt`; recurring = `cron`. Never both. Never both `prompt` and
  `message`. Times are local (no timezone suffix).
- Don't touch `CLAUDE.md` / persona — the voice stays the user's.

When done, summarize in 3 lines: files added, that the scheduler auto-starts with
the twin, and an example phrase to try.
