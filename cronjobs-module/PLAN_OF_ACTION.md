# Plan of action — add cronjobs / scheduled messages to this agent

**Audience: the coding agent (Claude Code, Codex, or any similar agent) doing the work.** These files are ready-made — integrate them as-is; don't rebuild the feature.
Ordered execution plan. Full source is in the Node.js guide — copy code from it:

- `guide for implementing cronjobs.md`

**The whole point: make it automatic. Install deps, write files, AND wire the
scheduler to auto-start inside the twin. The user must NOT have to run a separate
process or hand-edit anything.** Each step has a ✅ done-check.

---

## Goal
"send me a hi message at 7:30pm" (or recurring) just works: the agent records a
job via a CLI, and a scheduler that auto-starts inside the twin fires it on time
(console + desktop notification, and Slack if configured).

## Preconditions
- [ ] Inside the user's agent project (a `CLAUDE.md` / persona is present).
- [ ] `claude --version` works. Node ≥ 18.

---

## Steps

### 1. Install the dependency
- [ ] `npm install dotenv`.
- ✅ Done when: installed.

### 2. Create the job-creator CLI
- [ ] `schedule.js` in the project root, from the guide. This is what the skill
      runs to record jobs reliably.
- ✅ Done when: `node schedule.js --at "2020-01-01T00:00:00" --message test`
      writes a job to `data/jobs.json`.

### 3. Create the scheduler engine
- [ ] `scheduler.js` in the project root, from the guide. It exports
      `startScheduler()`.
- ✅ Done when: the file exists and exports the start function.

### 4. AUTO-START it inside the twin  ← the critical step
- [ ] Find the twin's startup (terminal chat `main()` / readline, or the bot
      start) and add the start call so the scheduler runs in the same process:
      - `require("./scheduler.js").startScheduler();`
- [ ] Only if there's truly no editable entry point: fall back to telling the
      user to run the scheduler standalone — but prefer wiring it in.
- ✅ Done when: starting the twin prints `⏰ Scheduler active …` (no separate
      process needed).

### 4b. Make sure the twin can RUN the schedule command (critical)
- [ ] The skill runs `schedule.js` via **Bash**. If the twin's
      `claude -p` dispatch can't use Bash, the command is blocked and the twin
      will falsely claim it "needs approval" → scheduling silently fails.
- [ ] If the dispatch uses `--permission-mode bypassPermissions` → fine. If it
      uses an `--allowedTools` allowlist → add `Bash` (and `Skill`).
- ✅ Done when: the twin can run a Bash command without an approval prompt.

### 5. Install the schedule-task skill
- [ ] `.claude/skills/schedule-task/SKILL.md` from the guide — it tells the twin
      to run the `schedule` CLI (never hand-edit JSON).
- ✅ Done when: the skill file exists with correct frontmatter.

### 6. Ignore runtime state & verify end-to-end
- [ ] Add `data/jobs.json` + `.env` to `.gitignore`.
- [ ] Ask the twin "send me a hi message in 2 minutes". Confirm a job lands in
      `data/jobs.json`, and ~2 min later the scheduler logs `[fire] …` + a
      notification — with no second process running.
- ✅ Done when: a scheduled message fires from the twin alone.

### 7. Report
- [ ] 3-line summary: files added, that the scheduler auto-starts with the twin,
      an example phrase to try.

---

## Guardrails (hold throughout)
- **Automatic, not manual** — wire `startScheduler()` into the twin; never leave
  the user to run a separate scheduler.
- The skill **runs the `schedule` CLI**; never hand-edit `data/jobs.json`.
- One-shot = `runAt`; recurring = `cron`. Never both. Never both `prompt`/`message`.
- Times are local (no timezone suffix). Don't touch `CLAUDE.md` / persona.
