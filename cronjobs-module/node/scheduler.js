// scheduler.js — the cronjobs engine for your twin.
//
// You normally DON'T run this separately. The integration wires
// `startScheduler()` into your twin's startup so it runs in the SAME process as
// your chat/bot — no second process to remember. (It can also run standalone
// with `node scheduler.js`.)
//
// Every POLL_MS it reads data/jobs.json and fires due jobs. A job with `prompt`
// runs your twin (`claude -p`, so it's in your voice); with `message` sends
// literal text. Delivery = console + macOS notification, and Slack if a token +
// channel are configured. Jobs are created via the schedule-task skill →
// schedule.js (never hand-edited).

const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");
require("dotenv").config();

const TWIN_DIR = process.env.TWIN_DIR ? path.resolve(process.env.TWIN_DIR) : __dirname;
const JOBS_FILE = process.env.JOBS_FILE
  ? path.resolve(process.env.JOBS_FILE)
  : path.join(__dirname, "data", "jobs.json");
const POLL_MS = Number(process.env.POLL_MS || 30000);
const SLACK_BOT_TOKEN = process.env.SLACK_BOT_TOKEN;
const SLACK_CHANNEL = process.env.SLACK_CHANNEL;

function loadJobs() {
  try {
    const raw = fs.readFileSync(JOBS_FILE, "utf8").trim();
    if (!raw) return [];
    const data = JSON.parse(raw);
    return Array.isArray(data) ? data : [];
  } catch (_) {
    return [];
  }
}
function saveJobs(jobs) {
  fs.mkdirSync(path.dirname(JOBS_FILE), { recursive: true });
  const tmp = JOBS_FILE + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(jobs, null, 2));
  fs.renameSync(tmp, JOBS_FILE);
}

function fieldMatch(field, value) {
  if (field === "*") return true;
  for (const part of field.split(",")) {
    if (part.includes("/")) {
      const [range, stepStr] = part.split("/");
      const step = Number(stepStr);
      if (range === "*") {
        if (step && value % step === 0) return true;
      } else {
        const base = Number(range);
        if (value >= base && step && (value - base) % step === 0) return true;
      }
    } else if (part.includes("-")) {
      const [a, b] = part.split("-").map(Number);
      if (value >= a && value <= b) return true;
    } else if (Number(part) === value) {
      return true;
    }
  }
  return false;
}
function cronMatches(expr, d) {
  const parts = expr.trim().split(/\s+/);
  if (parts.length !== 5) return false;
  const [mi, ho, dom, mo, dow] = parts;
  return (
    fieldMatch(mi, d.getMinutes()) &&
    fieldMatch(ho, d.getHours()) &&
    fieldMatch(dom, d.getDate()) &&
    fieldMatch(mo, d.getMonth() + 1) &&
    fieldMatch(dow, d.getDay())
  );
}
function minuteKey(d) {
  return d.toISOString().slice(0, 16);
}
function isDue(job, now) {
  if (job.status === "done") return false;
  if (job.runAt) return new Date(job.runAt) <= now;
  if (job.cron) return cronMatches(job.cron, now) && job.lastRun !== minuteKey(now);
  return false;
}

// Self-contained: run the twin via `claude -p` in the project dir (loads
// CLAUDE.md/persona). No need to import the twin's code.
function runTwin(prompt) {
  const res = spawnSync("claude", ["-p", prompt, "--permission-mode", "bypassPermissions"], {
    cwd: TWIN_DIR,
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 10,
  });
  if (res.status !== 0) {
    return `(twin error: ${(res.stderr || res.error || "unknown").toString().trim()})`;
  }
  return res.stdout.trim();
}

async function deliver(text, job) {
  const title = job.title || "reminder";
  // Print as a visible block so it shows up right in the terminal chat.
  process.stdout.write(`\n\n⏰ twin (scheduled — ${title}) ›\n${text}\n`);
  try {
    spawnSync("osascript", [
      "-e",
      `display notification ${JSON.stringify(text)} with title ${JSON.stringify("Agent: " + title)}`,
    ]);
  } catch (_) {}
  const channel = job.channel || SLACK_CHANNEL;
  if (SLACK_BOT_TOKEN && channel) {
    try {
      await fetch("https://slack.com/api/chat.postMessage", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${SLACK_BOT_TOKEN}` },
        body: JSON.stringify({ channel, text }),
      });
    } catch (e) {
      console.error("[slack] post failed:", e.message);
    }
  }
}

async function runJob(job) {
  const text = job.prompt ? runTwin(job.prompt) : job.message || "(empty job)";
  await deliver(text, job);
}

async function tick() {
  const jobs = loadJobs();
  const now = new Date();
  let changed = false;
  for (const job of jobs) {
    if (!isDue(job, now)) continue;
    await runJob(job);
    job.lastRun = minuteKey(now);
    if (job.runAt) job.status = "done";
    changed = true;
  }
  if (changed) saveJobs(jobs);
}

// Start the polling loop. Call this once from your twin's startup so scheduled
// jobs fire in the same process as your twin. Returns the interval handle.
let started = false;
function startScheduler() {
  if (started) return null; // guard against double-start
  started = true;
  console.log(`⏰ Scheduler active (checks every ${Math.round(POLL_MS / 1000)}s). Jobs: ${JOBS_FILE}`);
  tick().catch((e) => console.error("[tick] error:", e.message));
  return setInterval(
    () => tick().catch((e) => console.error("[tick] error:", e.message)),
    POLL_MS,
  );
}

module.exports = { startScheduler };

// Standalone mode (optional): `node scheduler.js`.
if (require.main === module) {
  startScheduler();
}
