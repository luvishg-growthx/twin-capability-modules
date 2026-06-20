# Twin Capability Modules — All-in-One

Drop-in **capability modules** for a personal AI twin (the GrowthX Buildathon
agent). Each module turns a single feature on by pasting a repo link into a
Claude Code **or** Codex session — the agent installs/wires it in; you don't
rebuild anything. Every module works whether your twin is **Python or JS** (it
checks first).

This repo bundles all four modules' folders **and** combines every one of their
README + setup + guide + plan files into this single document, in order.

## Modules & source repos

| Module | What it adds | Source repo |
|--------|--------------|-------------|
| 💬 **Slack** | Twin replies to DMs/mentions in your voice; send/edit/delete/list messages | https://github.com/luvishg-growthx/upgrading-your-bot-to-being-a-slack-bot |
| 📧 **Email (Gmail)** | Read the inbox and draft replies in your voice (read-only) | https://github.com/luvishg-growthx/reading-your-emails-and-drafting-a-reply-for-them-setup-guide-for-your-ai-agent |
| ⏰ **Scheduler (Cronjobs)** | Timed & recurring messages/reminders; auto-starts in the twin | https://github.com/luvishg-growthx/cronjobs-and-reminders-setup-guide-for-your-ai-agent |
| 🧠 **Long-term Memory (Engram)** | Recall the most relevant memories across every past chat | https://github.com/luvishg-growthx/long-term-memory-engram-setup-guide-for-your-ai-agent |

> The actual files for each module live in the folders alongside this README
> (`slack-twin-module/`, `email-replies-module/`, `cronjobs-module/`,
> `memory-module/`). Everything below is those modules' docs, combined.



<br>

# ═══ 💬 SLACK MODULE ═══


---

> 📄 **`slack-twin-module/README.md`**

# Twin → Slack Module

> ## 🤖 If you are Claude Code or Codex (any coding agent), read this first
>
> **Ready-made — don't rebuild anything.** You do **not** need to write or
> reinvent this feature. Just install/wire in the files as described and the bot
> gains the capability. These files work the same with Claude Code or Codex.
>
> The user pasted this repo because they want to **upgrade their existing
> terminal twin into a Slack bot** (same brain — `claude -p` — new face: Slack).
> Do this, in order:
>
> 1. **Follow `PLAN_OF_ACTION.md`** — the ordered execution checklist (works for
>    Claude *or* Codex). It tells you exactly what to do and links to the code.
> 2. **Detect the stack** of the twin in the current project: Node (a
>    `twin.js`/`*.js`, `package.json`) or Python (a `twin.py`/`*.py`,
>    `requirements.txt`). If unclear, ask the user one question.
> 3. **Fetch and follow the matching guide** for the full code and steps:
>    - **Node:** `https://raw.githubusercontent.com/luvishg-growthx/upgrading-your-bot-to-being-a-slack-bot/main/guide%20for%20implementing%20slack.md`
>    - **Python:** `https://raw.githubusercontent.com/luvishg-growthx/upgrading-your-bot-to-being-a-slack-bot/main/guide%20for%20implementing%20slack%20(python).md`
> 4. The plan + guide tell you to **upgrade `twin.js`/`twin.py` in place** into
>    the Slack bot (don't create a parallel file), install deps, and walk the
>    user through creating the Slack app + tokens. Follow them exactly.
>
> Everything below is human-facing context.

---

**Upgrade your terminal twin into a Slack bot.** Your existing `twin.js` /
`twin.py` (the one that chats in your terminal via `claude -p`) gets rewritten
*in place* into a Slack app — same brain, new face. People @mention or DM it in
Slack, and your twin replies in its own voice — using your `CLAUDE.md` and
handbook — right inside the thread.

- **No API key.** It dispatches `claude -p` against your logged-in Claude Code
  session, exactly like your terminal twin did.
- **No server / no public URL.** Uses Slack **Socket Mode**.
- **Per-thread memory.** Each Slack thread keeps its own Claude session.
- **One file, not two.** The terminal twin *becomes* the Slack bot — it doesn't
  get a second bot file bolted on beside it.
- **Sends, edits & deletes too.** Beyond replying, the twin can post, edit,
  delete, and list Slack messages on its own (via `slack-actions` + the
  `slack-message` skill).
- **Node *or* Python.** Pick whichever your twin is built in.

## How it works

```
Slack message ──► your twin (upgraded) ──► claude -p "<message>"  (runs in your project)
   (mention/DM)                                │  loads CLAUDE.md + handbook/persona
                                               ▼
Slack thread  ◄────── post reply ◄──────── twin's answer
```

The bot is a thin bridge wrapped around your existing brain. Your twin's
personality and knowledge come entirely from the `CLAUDE.md` + handbook files in
your project — this module adds no persona of its own. It's **neutral**: point
it at any twin and it speaks in that twin's voice.

## The fastest way to install it (recommended)

Don't wire it up by hand. Open **Claude Code inside your twin's project folder**
and paste this:

```
Read this file and set up the Slack feature for my twin:
https://raw.githubusercontent.com/luvishg-growthx/upgrading-your-bot-to-being-a-slack-bot/main/guide%20for%20implementing%20slack.md
```

Claude will read the guide, upgrade your `twin.js` into `slack-bot.js`, install
dependencies, and walk you through creating the Slack app.

**Python twin?** Point the same prompt at the Python guide instead:

```
Read this file and set up the Slack feature for my twin:
https://raw.githubusercontent.com/luvishg-growthx/upgrading-your-bot-to-being-a-slack-bot/main/guide%20for%20implementing%20slack%20(python).md
```

Or just **paste the repo link** and Claude will figure out the rest (see the
instruction block at the top of this file).

## Manual install

1. Use the reference bot for your stack as the target shape and rewrite your
   terminal twin into it:
   - Node: [`node/slack-bot.js`](node/slack-bot.js) → `slack-bot.js` in your root
   - Python: [`python/slack_bot.py`](python/slack_bot.py) → `slack_bot.py` in your root
   - Also copy the actions CLI ([`node/slack-actions.js`](node/slack-actions.js)
     / [`python/slack_actions.py`](python/slack_actions.py)) +
     [`.claude/skills/slack-message/SKILL.md`](.claude/skills/slack-message/SKILL.md)
     for send/edit/delete.
2. Remove the old terminal `twin.js` / `twin.py` (its logic now lives in the bot).
3. Create the Slack app and get two tokens — see
   **[`SLACK_APP_SETUP.md`](SLACK_APP_SETUP.md)**.
4. `cp .env.example .env` and paste your tokens in.
5. Install deps and run:
   - Node: `npm install @slack/bolt dotenv && node slack-bot.js`
   - Python: `pip install slack_bolt python-dotenv && python slack_bot.py`
6. In Slack, `@mention` the bot or DM it.

## Files

| Path                                       | What it is                                   |
| ------------------------------------------ | -------------------------------------------- |
| `PLAN_OF_ACTION.md`                        | Ordered execution checklist (Claude/Codex)   |
| `guide for implementing slack.md`          | Paste-into-Claude guide — **Node** twin      |
| `guide for implementing slack (python).md` | Paste-into-Claude guide — **Python** twin    |
| `SLACK_APP_SETUP.md`                       | One-time Slack app creation (scopes, tokens) |
| `.claude/skills/slack-message/SKILL.md`    | Teaches the twin to send/edit/delete/list    |
| `node/`                                     | Reference Node bot + `slack-actions.js` + env |
| `python/`                                   | Reference Python bot + `slack_actions.py` + env |


---

> 📄 **`slack-twin-module/PLAN_OF_ACTION.md`**

# Plan of action — upgrade this twin into a Slack bot

**Audience: the coding agent (Claude Code, Codex, or any similar agent) doing the work.** These files are ready-made — integrate them as-is; don't rebuild the feature.
This is the ordered execution plan. The full source + token setup lives in the
guides — open the one for the detected stack and copy code from it:

- Node: `guide for implementing slack.md`
- Python: `guide for implementing slack (python).md`

Work top to bottom. Don't skip steps. Each step has a ✅ done-check.

---

## Goal
Turn the user's existing terminal twin (`twin.js` / `twin.py`, which dispatches
`claude -p`) **into a Slack bot, in place** — same brain, new face. End state:
one bot file, no leftover terminal twin, replies posting into Slack threads in
the twin's voice, **plus** the twin can send / edit / delete Slack messages on
its own (Step 8).

## Preconditions (verify first)
- [ ] You are inside the user's twin project (a `CLAUDE.md` / persona is present).
- [ ] `claude --version` works (Claude Code installed + logged in). If not, stop
      and tell the user to install/login first.
- [ ] An existing terminal twin file exists. If none, stop — this plan *upgrades*
      one; it doesn't invent a twin.

---

## Steps

### 1. Detect the stack
- [ ] Node if `package.json` / `*.js` (twin usually `twin.js`).
- [ ] Python if `requirements.txt`/`pyproject.toml` / `*.py` (twin usually `twin.py`).
- [ ] If ambiguous, ask the user once. Announce the detected stack.
- ✅ Done when: you've stated "Detected: Node" or "Detected: Python".

### 2. Read the existing twin's brain
- [ ] Open the terminal twin file. Record its `claude -p` invocation: working
      directory, session flags (`--session-id`/`--resume`), and any extra flags
      (`--allowedTools`, `--model`, etc.).
- ✅ Done when: you can list the exact flags the current twin passes.

### 3. Write the bot file (upgrade in place)
- [ ] Create `slack-bot.js` (Node) or `slack_bot.py` (Python) in the project
      **root**, using the code from the matching guide.
- [ ] Merge in the custom flags from Step 2 so the Slack twin behaves identically
      to the terminal one.
- [ ] Confirm `TWIN_DIR` resolves to the project root (where `CLAUDE.md` lives).
- ✅ Done when: the bot file exists and contains the user's brain logic.

### 4. Remove the old terminal twin
- [ ] Delete `twin.js` / `twin.py` (or rename to `*.bak` if the user wants a
      backup). Update any `package.json`/run script that pointed at it.
- ✅ Done when: only the new bot file remains as the app entry point.

### 5. Install dependencies
- [ ] Node: `npm install @slack/bolt dotenv`
- [ ] Python: `pip install slack_bolt python-dotenv` (and add to `requirements.txt`)
- ✅ Done when: deps install without error.

### 6. Slack app + tokens (USER does this — you can't)
- [ ] Print the Slack-app steps from the guide (create app → Socket Mode →
      App-Level Token `connections:write` → bot scopes → event subscriptions →
      install → bot token → `/invite`).
- [ ] Wait for the user to paste back `SLACK_BOT_TOKEN` (xoxb-) and
      `SLACK_APP_TOKEN` (xapp-).
- [ ] Write them into `.env`; ensure `.env` is git-ignored.
- ✅ Done when: `.env` has both tokens and is ignored by git.

### 7. Run & verify
- [ ] Start the bot from the project root (`node slack-bot.js` / `python slack_bot.py`).
- [ ] Confirm the startup log prints the bot identity + twin dir.
- [ ] In Slack, `@mention` the bot; confirm it reacts 👀 and replies in-thread in
      the twin's voice; confirm a follow-up in that thread works without a mention.
- ✅ Done when: a real Slack message gets a correct in-voice reply.

### 8. Outbound actions — send / edit / delete messages
- [ ] Create `slack-actions.js` / `slack_actions.py` (from the guide's Step 6) in
      the project root — a CLI for `send` / `edit` / `delete` / `list`.
- [ ] Create `.claude/skills/slack-message/SKILL.md` (from the guide) so the twin
      knows it can act on Slack and calls the CLI via Bash.
- [ ] No new scopes needed: `chat:write` covers send/edit/delete of the bot's own
      messages; `*:history` covers `list` (both already added in Step 6 tokens).
- ✅ Done when: `node slack-actions.js send <channel> "test"` posts a message and
      prints its ts (and `delete`/`edit` work on it).

### 9. Report
- [ ] Give the user a 3-line summary: twin upgraded → bot file, send/edit/delete
      added, and the exact start command.

---

## Guardrails (hold throughout)
- Upgrade in place — never leave two `claude -p` dispatchers behind.
- Preserve the brain (flags + working dir) so replies match the terminal twin.
- Don't modify `CLAUDE.md` / persona — the voice stays the user's.
- Never print or commit token values.


---

> 📄 **`slack-twin-module/guide for implementing slack.md`**

# Guide: upgrade your twin into a Slack bot (Node.js)

**You are Claude Code or Codex (or any coding agent), reading this file inside the user's twin project.** These files are ready-made — don't rebuild the feature from scratch; just install/wire them in as described below. The
user already has a terminal twin — a Node file (usually `twin.js`) that chats by
dispatching `claude -p`. Your job is to **upgrade that file in place into a
Slack bot**: same brain, new face. Do **not** create a second bot file sitting
awkwardly next to `twin.js`. You are transforming `twin.js` itself into
`slack-bot.js`.

> ## ⚠️ First: confirm the stack
> Check whether the user's agent is **Node.js** (`package.json` / `*.js`) or
> **Python** (`requirements.txt` / `*.py`) — ask if unclear. **This is the
> Node.js guide.** If their agent is **Python**, stop and follow
> `guide for implementing slack (python).md` instead, so you install the files
> for the right language.

---

## The prompt the user pastes (for reference)

> Read `guide for implementing slack.md` from
> `https://raw.githubusercontent.com/luvishg-growthx/upgrading-your-bot-to-being-a-slack-bot/main/guide%20for%20implementing%20slack.md`
> and set up the Slack feature for my twin.

---

## What "upgrade in place" means

- **Keep the brain** — the `claude -p` dispatch the user already has: the flags
  they pass, the project folder it runs in (so it loads their `CLAUDE.md` +
  handbook/persona), and the session-continuity logic that gives it memory.
- **Replace the face** — delete the terminal `readline` chat loop and put a
  Slack **Socket Mode** app in its place.
- **One change to the memory model** — instead of ONE global session for the
  terminal, keep **one Claude session per Slack thread**, so each Slack thread
  has its own memory.
- **End state: one file.** The old `twin.js` is gone; `slack-bot.js` is the
  twin now. No duplicate dispatch logic anywhere.

The result: no API key (uses the logged-in Claude Code session), no public URL
(Socket Mode), replies posted back into the Slack thread in the twin's voice.

---

## Step 0 — Read the existing twin

1. Find the user's terminal twin file. It's usually `twin.js`; if it's named
   something else (`main.js`, `index.js`, …), use that.
2. Read it and note **how it calls `claude -p`** — specifically:
   - the working directory it runs in (so the persona/handbook loads),
   - any extra flags it passes (`--allowedTools`, `--model`, etc.),
   - how it does session continuity (`--session-id` / `--resume`).
   You will carry these into the upgraded file so the Slack twin replies exactly
   like the terminal twin did.
3. If you can't find any terminal twin, tell the user — this guide upgrades an
   existing twin; it assumes one exists.

---

## Step 1 — Write `slack-bot.js`

Create `slack-bot.js` in the **project root** (next to `CLAUDE.md`) with the
content below. This is the canonical shape. **Merge in** any custom flags you
found in Step 0 (e.g. add the user's `--allowedTools` / `--model` to the `args`
array) so behavior matches their twin.

```javascript
// slack-bot.js — your twin, upgraded from a terminal chat into a Slack app.
// Same brain (claude -p, with memory); new face (Slack). Lives in project root
// next to CLAUDE.md so `claude -p` loads your persona/handbook automatically.

const { App } = require("@slack/bolt");
const { spawn } = require("child_process");
const { randomUUID } = require("crypto");
const path = require("path");
require("dotenv").config();

// Project root (this file's folder) — `claude -p` runs here so it loads your
// CLAUDE.md + handbook. Override with TWIN_DIR in .env only if needed.
const TWIN_DIR = process.env.TWIN_DIR ? path.resolve(process.env.TWIN_DIR) : __dirname;
const CLAUDE_TIMEOUT_MS = Number(process.env.CLAUDE_TIMEOUT_MS || 300000);
const SLACK_CHUNK = 3500; // Slack caps messages near 4000 chars

// One UUID per Slack thread: first msg creates the session, later msgs resume
// it. This is the same session-continuity idea your terminal twin used, but
// keyed per thread instead of one global session.
const threadSessions = new Map();
function sessionFor(threadId) {
  let s = threadSessions.get(threadId);
  if (!s) {
    s = { id: randomUUID(), started: false };
    threadSessions.set(threadId, s);
  }
  return s;
}

// THE BRAIN — carried over from your terminal twin. Add any custom flags your
// old twin.js passed (e.g. "--allowedTools", ..., "--model", "...") here.
function askTwin(threadId, message) {
  return new Promise((resolve) => {
    const session = sessionFor(threadId);
    const sessionFlag = session.started
      ? ["--resume", session.id]
      : ["--session-id", session.id];
    session.started = true;

    const args = [
      "-p",
      message,
      ...sessionFlag,
      "--permission-mode",
      "bypassPermissions", // bot is unattended — it can't answer prompts
    ];

    const child = spawn("claude", args, { cwd: TWIN_DIR, env: process.env });
    let out = "";
    let err = "";
    child.stdout.on("data", (d) => (out += d));
    child.stderr.on("data", (d) => (err += d));

    const timer = setTimeout(() => {
      child.kill("SIGKILL");
      resolve("(the twin took too long and was stopped)");
    }, CLAUDE_TIMEOUT_MS);

    child.on("close", (code) => {
      clearTimeout(timer);
      if (code !== 0) {
        console.error("[claude] exit", code, err);
        resolve("(the twin hit an error — check the bot's logs)");
        return;
      }
      resolve(out.trim() || "(the twin had nothing to say)");
    });
    child.on("error", (e) => {
      clearTimeout(timer);
      console.error("[claude] spawn failed:", e.message);
      resolve("(couldn't start `claude` — is Claude Code installed and logged in?)");
    });
  });
}

function chunk(text) {
  if (text.length <= SLACK_CHUNK) return [text];
  const parts = [];
  let buf = "";
  for (const line of text.split("\n")) {
    if ((buf + "\n" + line).length > SLACK_CHUNK && buf) {
      parts.push(buf);
      buf = "";
    }
    buf = buf ? buf + "\n" + line : line;
  }
  if (buf) parts.push(buf);
  return parts;
}

// THE FACE — Slack instead of the terminal readline loop.
const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  appToken: process.env.SLACK_APP_TOKEN,
  socketMode: true,
});
let selfUserId = null;

async function handle({ text, channel, threadId, say, client }) {
  const clean = text.replace(/<@[A-Z0-9]+>/g, "").trim();
  if (!clean) return;
  console.log(`[slack] thread=${threadId} msg="${clean.slice(0, 80)}"`);
  try {
    await client.reactions.add({ channel, name: "eyes", timestamp: threadId });
  } catch (_) {}
  const reply = await askTwin(threadId, clean);
  for (const part of chunk(reply)) await say({ text: part, thread_ts: threadId });
}

app.event("app_mention", async ({ event, say, client }) => {
  const threadId = event.thread_ts || event.ts;
  await handle({ text: event.text, channel: event.channel, threadId, say, client });
});

app.event("message", async ({ event, say, client }) => {
  if (event.bot_id || event.subtype) return;
  if (event.user && event.user === selfUserId) return;
  const isDM = event.channel_type === "im";
  const threadId = event.thread_ts || event.ts;
  const isFollowUp = event.thread_ts && threadSessions.has(event.thread_ts);
  if (!isDM && !isFollowUp) return;
  await handle({ text: event.text, channel: event.channel, threadId, say, client });
});

(async () => {
  await app.start();
  const auth = await app.client.auth.test();
  selfUserId = auth.user_id;
  console.log(`⚡️ Twin Slack bot running as @${auth.user} (${selfUserId})`);
  console.log(`   twin dir: ${TWIN_DIR}`);
})();
```

---

## Step 2 — Remove the old terminal twin

The terminal `readline` chat now lives nowhere — its job moved into
`slack-bot.js`. Delete the old `twin.js` (or, if the user wants a safety copy,
rename it to `twin.js.bak`). The point is a clean single app, not two files.

If `package.json` has a `start`/`twin` script that ran `node twin.js`, update it
to `"start": "node slack-bot.js"`.

---

## Step 3 — Dependencies

Add the two libraries the Slack face needs:

```
npm install @slack/bolt dotenv
```

(If there's no `package.json`, create one first with `npm init -y`.)

---

## Step 4 — Slack app + tokens (have the USER do this)

You (Claude) **cannot** create the Slack app — it needs a human in a browser.
Print these steps and wait for the user to paste back the two tokens. Socket
Mode means no public URL is needed.

1. <https://api.slack.com/apps> → **Create New App** → **From scratch**; name
   it, pick the workspace.
2. **Socket Mode** → enable. Generate an **App-Level Token** with scope
   `connections:write`. Copy it → `SLACK_APP_TOKEN` (starts `xapp-`).
3. **OAuth & Permissions** → **Bot Token Scopes**, add: `app_mentions:read`,
   `chat:write`, `im:history`, `channels:history`, `groups:history`,
   `reactions:write`.
4. **Event Subscriptions** → enable → **Subscribe to bot events**:
   `app_mention`, `message.im`, `message.channels`, `message.groups`.
5. **Install App** → **Install to Workspace** → **Allow**. Copy the **Bot User
   OAuth Token** → `SLACK_BOT_TOKEN` (starts `xoxb-`).
6. In Slack: `/invite @YourBotName` into a channel (DMs need no invite).

Then create `.env` in the project root (and make sure `.env` is git-ignored):

```
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
# Optional: TWIN_DIR=/abs/path/to/twin   (default = this project root)
# Optional: CLAUDE_TIMEOUT_MS=300000
```

---

## Step 5 — Run & verify

1. Confirm Claude Code is installed/logged in: `claude --version`. If it fails,
   tell the user to install/login first.
2. Start the bot from the project root: `node slack-bot.js` (or `npm start`).
3. Expect: `⚡️ Twin Slack bot running as @… — twin dir: …`.
4. In Slack, `@mention` the bot in the invited channel (`@YourBot say hi`).
   Within seconds it should react 👀 and reply in a thread, in the twin's voice.
   Follow-ups inside that thread don't need another mention.

---

## Step 6 — Outbound actions: send / edit / delete messages

The bot above *replies* to people. To also let the twin **send, edit, delete,
and list** Slack messages on its own (e.g. "post 'standup in 5' to #general",
"delete that last message"), install the actions CLI + a skill.

**6a. Create `slack-actions.js`** in the project root:

```javascript
#!/usr/bin/env node
// slack-actions.js — send / edit / delete / list Slack messages from your agent.
// Uses SLACK_BOT_TOKEN from .env. Slack only lets a bot edit/delete its OWN msgs.
const path = require("path");
require("dotenv").config({ path: path.join(__dirname, ".env") });

const TOKEN = process.env.SLACK_BOT_TOKEN;
if (!TOKEN) { console.error("Missing SLACK_BOT_TOKEN (set it in .env)."); process.exit(1); }

async function slack(method, payload) {
  const res = await fetch(`https://slack.com/api/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8", Authorization: `Bearer ${TOKEN}` },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!data.ok) throw new Error(`${method} failed: ${data.error}`);
  return data;
}

async function main() {
  const [action, channel, ...rest] = process.argv.slice(2);
  if (!action || !channel) {
    console.error("usage: node slack-actions.js <send|edit|delete|list> <channel> [...]");
    process.exit(1);
  }
  switch (action) {
    case "send": {
      const text = rest.join(" ");
      if (!text) throw new Error("send needs message text");
      const r = await slack("chat.postMessage", { channel, text });
      console.log(`sent ts=${r.ts}`);
      break;
    }
    case "edit": {
      const [ts, ...textParts] = rest;
      const text = textParts.join(" ");
      if (!ts || !text) throw new Error("edit needs <ts> <text>");
      await slack("chat.update", { channel, ts, text });
      console.log(`edited ts=${ts}`);
      break;
    }
    case "delete": {
      const [ts] = rest;
      if (!ts) throw new Error("delete needs <ts>");
      await slack("chat.delete", { channel, ts });
      console.log(`deleted ts=${ts}`);
      break;
    }
    case "list": {
      const limit = Number(rest[0] || 10);
      const r = await slack("conversations.history", { channel, limit });
      for (const m of r.messages || []) {
        const text = (m.text || "").replace(/\s+/g, " ").slice(0, 100);
        console.log(`${m.ts} | ${m.user || m.bot_id || "?"} | ${text}`);
      }
      break;
    }
    default:
      console.error(`unknown action: ${action}`);
      process.exit(1);
  }
}
main().catch((e) => { console.error(e.message); process.exit(1); });
```

**6b. Create `.claude/skills/slack-message/SKILL.md`** so the twin knows it has
these powers and calls the CLI via Bash:

````markdown
---
name: slack-message
description: Send, edit, delete, or list Slack messages on the user's behalf. Trigger whenever the user asks to post/send a Slack message, edit/update a message already sent, delete/remove a message, or look up recent messages in a channel.
---

# Act on Slack (send / edit / delete / list)

Use the project's CLI via Bash (Node: `slack-actions.js`). Slack only lets the
bot **edit/delete messages it posted itself.**

```
node slack-actions.js send   <channel> <text...>      # prints the ts — save it
node slack-actions.js edit   <channel> <ts> <text...>
node slack-actions.js delete <channel> <ts>
node slack-actions.js list   <channel> [limit]        # "ts | user | text"
```

`<channel>` = channel ID (`C…`) or user ID (`U…`) for a DM.

- "Send X to <channel>" → `send`, then report the ts.
- "Edit/delete that message" → reuse the ts from a recent `send`, or `list` the
  channel to find the bot's message first. Confirm before deleting if ambiguous.
- Keep wording in the agent's voice unless the user gave exact text.
````

**6c.** Make sure the bot's Slack scopes include `chat:write` (send/edit/delete
of its own messages) and the `*:history` scopes (for `list`) — they're already in
the Step 4 scope list, so no change is needed. The twin runs with
`bypassPermissions`, so it can already call the CLI via Bash.

---

## Guardrails (do these, quietly)

- **Upgrade in place — don't duplicate.** End with one app file (`slack-bot.js`)
  and no leftover terminal twin running its own `claude -p`.
- **Preserve the brain.** Carry over the user's existing `claude -p` flags and
  working directory so the Slack twin answers exactly like the terminal one.
- **Don't touch** `CLAUDE.md`, the persona/handbook, or other source — the
  personality stays 100% the user's. This bot adds no voice of its own.
- **Never print or commit token values.** Ensure `.env` is git-ignored.
- If `claude -p` isn't found at runtime, it's almost always Claude Code not being
  installed / on PATH for the shell that launched the bot.

When finished, give the user a 3-line summary: that `twin.js` was upgraded into
`slack-bot.js`, that you added send/edit/delete via `slack-actions.js` + the
`slack-message` skill, and the exact command to start the bot.


---

> 📄 **`slack-twin-module/guide for implementing slack (python).md`**

# Guide: upgrade your twin into a Slack bot (Python)

**You are Claude Code or Codex (or any coding agent), reading this file inside the user's twin project.** These files are ready-made — don't rebuild the feature from scratch; just install/wire them in as described below. The
user already has a terminal twin — a Python file (usually `twin.py`) that chats
by dispatching `claude -p`. Your job is to **upgrade that file in place into a
Slack bot**: same brain, new face. Do **not** create a second bot file sitting
awkwardly next to `twin.py`. You are transforming `twin.py` itself into
`slack_bot.py`.

> ## ⚠️ First: confirm the stack
> Check whether the user's agent is **Node.js** (`package.json` / `*.js`) or
> **Python** (`requirements.txt` / `*.py`) — ask if unclear. **This is the
> Python guide.** If their agent is **Node.js**, stop and follow
> `guide for implementing slack.md` instead, so you install the files for the
> right language.

---

## The prompt the user pastes (for reference)

> Read `guide for implementing slack.md` from
> `https://raw.githubusercontent.com/luvishg-growthx/upgrading-your-bot-to-being-a-slack-bot/main/guide%20for%20implementing%20slack.md`
> and set up the Slack feature for my twin.

(For a Python twin, point the same prompt at
`https://raw.githubusercontent.com/luvishg-growthx/upgrading-your-bot-to-being-a-slack-bot/main/guide%20for%20implementing%20slack%20(python).md`
instead.)

---

## What "upgrade in place" means

- **Keep the brain** — the `claude -p` dispatch the user already has: the flags
  they pass, the project folder it runs in (so it loads their `CLAUDE.md` +
  handbook/persona), and the session-continuity logic that gives it memory.
- **Replace the face** — delete the terminal input loop and put a Slack
  **Socket Mode** app in its place.
- **One change to the memory model** — instead of ONE global session for the
  terminal, keep **one Claude session per Slack thread**, so each Slack thread
  has its own memory.
- **End state: one file.** The old `twin.py` is gone; `slack_bot.py` is the twin
  now. No duplicate dispatch logic anywhere.

The result: no API key (uses the logged-in Claude Code session), no public URL
(Socket Mode), replies posted back into the Slack thread in the twin's voice.

---

## Step 0 — Read the existing twin

1. Find the user's terminal twin file. It's usually `twin.py`; if it's named
   something else (`main.py`, `bot.py`, …), use that.
2. Read it and note **how it calls `claude -p`** — specifically:
   - the working directory it runs in (so the persona/handbook loads),
   - any extra flags it passes (`--allowedTools`, `--model`, etc.),
   - how it does session continuity (`--session-id` / `--resume`).
   Carry these into the upgraded file so the Slack twin replies exactly like the
   terminal twin did.
3. If you can't find any terminal twin, tell the user — this guide upgrades an
   existing twin; it assumes one exists.

---

## Step 1 — Write `slack_bot.py`

Create `slack_bot.py` in the **project root** (next to `CLAUDE.md`) with the
content below. This is the canonical shape. **Merge in** any custom flags you
found in Step 0 (add the user's `--allowedTools` / `--model` to the `args` list)
so behavior matches their twin.

```python
"""slack_bot.py — your twin, upgraded from a terminal chat into a Slack app.
Same brain (claude -p, with memory); new face (Slack). Lives in project root
next to CLAUDE.md so `claude -p` loads your persona/handbook automatically.
"""

import os
import re
import subprocess
import uuid
from pathlib import Path

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

# Project root (this file's folder) — `claude -p` runs here so it loads your
# CLAUDE.md + handbook. Override with TWIN_DIR in .env only if needed.
TWIN_DIR = Path(os.environ.get("TWIN_DIR", Path(__file__).resolve().parent)).resolve()
CLAUDE_TIMEOUT_S = int(os.environ.get("CLAUDE_TIMEOUT_MS", "300000")) // 1000
SLACK_CHUNK = 3500  # Slack caps messages near 4000 chars

# One UUID per Slack thread: first msg creates the session, later msgs resume
# it. Same session-continuity idea your terminal twin used, but keyed per thread.
_thread_sessions: dict[str, dict] = {}


def _session_for(thread_id: str) -> dict:
    s = _thread_sessions.get(thread_id)
    if s is None:
        s = {"id": str(uuid.uuid4()), "started": False}
        _thread_sessions[thread_id] = s
    return s


# THE BRAIN — carried over from your terminal twin. Add any custom flags your
# old twin.py passed (e.g. "--allowedTools", ..., "--model", "...") here.
def ask_twin(thread_id: str, message: str) -> str:
    session = _session_for(thread_id)
    session_flag = (
        ["--resume", session["id"]] if session["started"] else ["--session-id", session["id"]]
    )
    session["started"] = True
    args = [
        "claude", "-p", message, *session_flag,
        "--permission-mode", "bypassPermissions",  # unattended bot
    ]
    try:
        result = subprocess.run(
            args, cwd=str(TWIN_DIR), capture_output=True, text=True, timeout=CLAUDE_TIMEOUT_S
        )
    except subprocess.TimeoutExpired:
        return "(the twin took too long and was stopped)"
    except FileNotFoundError:
        return "(couldn't start `claude` — is Claude Code installed and logged in?)"
    if result.returncode != 0:
        print("[claude] exit", result.returncode, result.stderr)
        return "(the twin hit an error — check the bot's logs)"
    return result.stdout.strip() or "(the twin had nothing to say)"


def chunk(text: str) -> list[str]:
    if len(text) <= SLACK_CHUNK:
        return [text]
    parts, buf = [], ""
    for line in text.split("\n"):
        if buf and len(buf) + 1 + len(line) > SLACK_CHUNK:
            parts.append(buf)
            buf = ""
        buf = line if not buf else buf + "\n" + line
    if buf:
        parts.append(buf)
    return parts


# THE FACE — Slack instead of the terminal input loop.
app = App(token=os.environ["SLACK_BOT_TOKEN"])
SELF_USER_ID = app.client.auth_test()["user_id"]
_MENTION_RE = re.compile(r"<@[A-Z0-9]+>")


def _handle(text, channel, thread_id, say, client):
    clean = _MENTION_RE.sub("", text or "").strip()
    if not clean:
        return
    print(f'[slack] thread={thread_id} msg="{clean[:80]}"')
    try:
        client.reactions_add(channel=channel, name="eyes", timestamp=thread_id)
    except Exception:
        pass
    reply = ask_twin(thread_id, clean)
    for part in chunk(reply):
        say(text=part, thread_ts=thread_id)


@app.event("app_mention")
def on_mention(event, say, client):
    thread_id = event.get("thread_ts") or event["ts"]
    _handle(event.get("text", ""), event["channel"], thread_id, say, client)


@app.event("message")
def on_message(event, say, client):
    if event.get("bot_id") or event.get("subtype"):
        return
    if event.get("user") == SELF_USER_ID:
        return
    is_dm = event.get("channel_type") == "im"
    thread_ts = event.get("thread_ts")
    thread_id = thread_ts or event["ts"]
    is_follow_up = bool(thread_ts and thread_ts in _thread_sessions)
    if not is_dm and not is_follow_up:
        return
    _handle(event.get("text", ""), event["channel"], thread_id, say, client)


if __name__ == "__main__":
    print(f"⚡️ Twin Slack bot starting (twin dir: {TWIN_DIR})")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

---

## Step 2 — Remove the old terminal twin

The terminal input loop now lives nowhere — its job moved into `slack_bot.py`.
Delete the old `twin.py` (or, if the user wants a safety copy, rename it to
`twin.py.bak`). The point is a clean single app, not two files.

---

## Step 3 — Dependencies

```
pip install slack_bolt python-dotenv
```

Add them to `requirements.txt` (create it if missing):

```
slack_bolt>=1.18.0
python-dotenv>=1.0.0
```

---

## Step 4 — Slack app + tokens (have the USER do this)

You (Claude) **cannot** create the Slack app — it needs a human in a browser.
Print these steps and wait for the user to paste back the two tokens. Socket
Mode means no public URL is needed.

1. <https://api.slack.com/apps> → **Create New App** → **From scratch**; name
   it, pick the workspace.
2. **Socket Mode** → enable. Generate an **App-Level Token** with scope
   `connections:write`. Copy it → `SLACK_APP_TOKEN` (starts `xapp-`).
3. **OAuth & Permissions** → **Bot Token Scopes**, add: `app_mentions:read`,
   `chat:write`, `im:history`, `channels:history`, `groups:history`,
   `reactions:write`.
4. **Event Subscriptions** → enable → **Subscribe to bot events**:
   `app_mention`, `message.im`, `message.channels`, `message.groups`.
5. **Install App** → **Install to Workspace** → **Allow**. Copy the **Bot User
   OAuth Token** → `SLACK_BOT_TOKEN` (starts `xoxb-`).
6. In Slack: `/invite @YourBotName` into a channel (DMs need no invite).

Then create `.env` in the project root (and make sure `.env` is git-ignored):

```
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
# Optional: TWIN_DIR=/abs/path/to/twin   (default = this project root)
# Optional: CLAUDE_TIMEOUT_MS=300000
```

---

## Step 5 — Run & verify

1. Confirm Claude Code is installed/logged in: `claude --version`. If it fails,
   tell the user to install/login first.
2. Start the bot from the project root: `python slack_bot.py`.
3. Expect: `⚡️ Twin Slack bot starting (twin dir: …)`.
4. In Slack, `@mention` the bot in the invited channel (`@YourBot say hi`).
   Within seconds it should react 👀 and reply in a thread, in the twin's voice.
   Follow-ups inside that thread don't need another mention.

---

## Step 6 — Outbound actions: send / edit / delete messages

The bot above *replies* to people. To also let the twin **send, edit, delete,
and list** Slack messages on its own (e.g. "post 'standup in 5' to #general",
"delete that last message"), install the actions CLI + a skill.

**6a. Create `slack_actions.py`** in the project root:

```python
#!/usr/bin/env python3
"""slack_actions.py — send / edit / delete / list Slack messages from your agent.
Uses SLACK_BOT_TOKEN from .env. Slack only lets a bot edit/delete its OWN msgs."""
import json, os, re, sys, urllib.request
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
TOKEN = os.environ.get("SLACK_BOT_TOKEN")
if not TOKEN:
    print("Missing SLACK_BOT_TOKEN (set it in .env).", file=sys.stderr)
    sys.exit(1)


def slack(method: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"https://slack.com/api/{method}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8", "Authorization": f"Bearer {TOKEN}"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    if not data.get("ok"):
        raise RuntimeError(f"{method} failed: {data.get('error')}")
    return data


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        print("usage: python slack_actions.py <send|edit|delete|list> <channel> [...]", file=sys.stderr)
        sys.exit(1)
    action, channel, rest = args[0], args[1], args[2:]
    if action == "send":
        text = " ".join(rest)
        if not text:
            raise RuntimeError("send needs message text")
        r = slack("chat.postMessage", {"channel": channel, "text": text})
        print(f"sent ts={r['ts']}")
    elif action == "edit":
        if len(rest) < 2:
            raise RuntimeError("edit needs <ts> <text>")
        ts, text = rest[0], " ".join(rest[1:])
        slack("chat.update", {"channel": channel, "ts": ts, "text": text})
        print(f"edited ts={ts}")
    elif action == "delete":
        if not rest:
            raise RuntimeError("delete needs <ts>")
        ts = rest[0]
        slack("chat.delete", {"channel": channel, "ts": ts})
        print(f"deleted ts={ts}")
    elif action == "list":
        limit = int(rest[0]) if rest else 10
        r = slack("conversations.history", {"channel": channel, "limit": limit})
        for m in r.get("messages", []):
            text = re.sub(r"\s+", " ", m.get("text", ""))[:100]
            print(f"{m.get('ts')} | {m.get('user') or m.get('bot_id') or '?'} | {text}")
    else:
        print(f"unknown action: {action}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
```

**6b. Create `.claude/skills/slack-message/SKILL.md`** so the twin knows it has
these powers and calls the CLI via Bash:

````markdown
---
name: slack-message
description: Send, edit, delete, or list Slack messages on the user's behalf. Trigger whenever the user asks to post/send a Slack message, edit/update a message already sent, delete/remove a message, or look up recent messages in a channel.
---

# Act on Slack (send / edit / delete / list)

Use the project's CLI via Bash (Python: `slack_actions.py`). Slack only lets the
bot **edit/delete messages it posted itself.**

```
python slack_actions.py send   <channel> <text...>      # prints the ts — save it
python slack_actions.py edit   <channel> <ts> <text...>
python slack_actions.py delete <channel> <ts>
python slack_actions.py list   <channel> [limit]        # "ts | user | text"
```

`<channel>` = channel ID (`C…`) or user ID (`U…`) for a DM.

- "Send X to <channel>" → `send`, then report the ts.
- "Edit/delete that message" → reuse the ts from a recent `send`, or `list` the
  channel to find the bot's message first. Confirm before deleting if ambiguous.
- Keep wording in the agent's voice unless the user gave exact text.
````

**6c.** The Slack scopes from Step 4 already cover this (`chat:write` for
send/edit/delete of the bot's own messages, `*:history` for `list`), so no scope
change is needed. The twin runs with `bypassPermissions`, so it can call the CLI
via Bash.

---

## Guardrails (do these, quietly)

- **Upgrade in place — don't duplicate.** End with one app file (`slack_bot.py`)
  and no leftover terminal twin running its own `claude -p`.
- **Preserve the brain.** Carry over the user's existing `claude -p` flags and
  working directory so the Slack twin answers exactly like the terminal one.
- **Don't touch** `CLAUDE.md`, the persona/handbook, or other source — the
  personality stays 100% the user's. This bot adds no voice of its own.
- **Never print or commit token values.** Ensure `.env` is git-ignored.
- If `claude -p` isn't found at runtime, it's almost always Claude Code not being
  installed / on PATH for the shell that launched the bot.

When finished, give the user a 3-line summary: that `twin.py` was upgraded into
`slack_bot.py`, that you added send/edit/delete via `slack_actions.py` + the
`slack-message` skill, and the exact command to start the bot.


---

> 📄 **`slack-twin-module/SLACK_APP_SETUP.md`**

# Create your Slack app (one-time, ~3 minutes)

This bot uses **Socket Mode**, so you do **not** need a public URL, ngrok, or a
server. You just need two tokens. Do this once.

## 1. Create the app

1. Go to <https://api.slack.com/apps> → **Create New App** → **From scratch**.
2. Name it (e.g. "My Twin") and pick your workspace.

## 2. Turn on Socket Mode

1. Left sidebar → **Socket Mode** → toggle **Enable Socket Mode** on.
2. When prompted, create an **App-Level Token**:
   - Name it anything (e.g. `socket`).
   - Add the scope **`connections:write`**.
   - Click **Generate**, then copy the token. It starts with **`xapp-`**.
   - This is your **`SLACK_APP_TOKEN`**.

## 3. Add bot permissions (scopes)

Left sidebar → **OAuth & Permissions** → **Scopes** → **Bot Token Scopes**, add:

| Scope               | Why                                            |
| ------------------- | ---------------------------------------------- |
| `app_mentions:read` | see when someone @mentions the bot             |
| `chat:write`        | post replies                                   |
| `im:history`        | read direct messages sent to the bot           |
| `channels:history`  | read thread replies in public channels         |
| `groups:history`    | read thread replies in private channels        |
| `reactions:write`   | add the 👀 "on it" reaction (optional)         |

## 4. Subscribe to events

Left sidebar → **Event Subscriptions** → toggle on. Under
**Subscribe to bot events**, add:

- `app_mention`
- `message.im`     (DMs)
- `message.channels`  (public channel threads)
- `message.groups`    (private channel threads)

(With Socket Mode on, you do **not** need a Request URL.)

## 5. Install the app & get the bot token

1. Left sidebar → **Install App** → **Install to Workspace** → **Allow**.
2. Copy the **Bot User OAuth Token**. It starts with **`xoxb-`**.
   - This is your **`SLACK_BOT_TOKEN`**.

## 6. Invite the bot to a channel

In Slack, open a channel and type:

```
/invite @YourBotName
```

(DMs work without an invite.)

## 7. Put the tokens in `.env`

Paste both tokens into your `.env` file:

```
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
```

That's it. Start the bot, then `@mention` it in the channel or DM it.

> If you change scopes later, you must **reinstall the app** (step 5) for the
> new permissions to take effect.


<br>

# ═══ 📧 EMAIL (GMAIL) MODULE ═══


---

> 📄 **`email-replies-module/README.md`**

# Email Replies Module

> ## 🤖 If you are Claude Code or Codex (any coding agent), read this first
>
> **Ready-made — don't rebuild anything.** You do **not** need to write or
> reinvent this feature. Just install/wire in the files as described and the bot
> gains the capability. These files work the same with Claude Code or Codex.
>
> The user pasted this repo because they want to give their AI agent the ability
> to **read their unread Gmail and draft replies in the agent's own voice**. Do
> this:
>
> 1. **Confirm the stack first** — check whether the user's agent is Node.js
>    (`package.json`/`*.js`) or Python (`requirements.txt`/`*.py`). The skill +
>    `/reply` files here are identical for both; only the optional
>    dispatcher-allowlist step differs (Node vs Python).
> 2. **Follow `PLAN_OF_ACTION.md`** — the ordered execution checklist (works for
>    Claude *or* Codex). It links to the guide below for the full code.
> 2. **Fetch and follow the setup guide** end-to-end — it has the full skill +
>    command code and every step:
>    `https://raw.githubusercontent.com/luvishg-growthx/reading-your-emails-and-drafting-a-reply-for-them-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20email%20replies.md`
> 3. It installs a skill (`.claude/skills/email-replies/SKILL.md`) and a
>    `/reply` command (`.claude/commands/reply.md`) into the current project, and
>    tells you to have the user **connect Gmail at claude.ai** (web-only auth —
>    required).
> 4. Follow them exactly. The reply voice comes from the user's own `CLAUDE.md` /
>    `PERSONA.md` — add no persona of your own.
>
> Everything below is human-facing context.

---

Give your Claude Code agent an inbox assistant: ask it to "read my emails and
draft replies" and it reads your **unread** Gmail, drafts a reply to each one
**in your agent's voice**, and saves them all to a dated file you can review.

- **No API key.** Uses your logged-in Claude Code session + Claude's Gmail
  connector.
- **Read-only by design.** Never sends, never marks mail as read. It only drafts.
- **Your voice.** Drafts follow your `CLAUDE.md` / `PERSONA.md` — neutral module,
  your personality.
- **Runtime-agnostic.** Works whether your twin is Node or Python (it's a Claude
  Code skill, not dispatcher code).

## How it works

```
"read my emails and draft replies"
        │
        ▼
 email-replies skill ──► Gmail connector ──► reads unread mail (read-only)
        │
        ▼
 drafts each reply in YOUR voice (CLAUDE.md / PERSONA.md)
        │
        ▼
 writes drafts/replies-<date>.md   ← you review & send yourself
```

## The fastest way to install it (recommended)

Open **Claude Code inside your agent's project folder** and paste this:

```
Read this and set up email reading + reply drafting for my agent:
https://raw.githubusercontent.com/luvishg-growthx/reading-your-emails-and-drafting-a-reply-for-them-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20email%20replies.md
```

Or just **paste the repo link** and Claude will route itself via the instruction
block at the top of this file.

## Manual install

1. Copy `.claude/skills/email-replies/SKILL.md` and `.claude/commands/reply.md`
   into your project's `.claude/`.
2. Connect Gmail — see **[`GMAIL_CONNECTOR_SETUP.md`](GMAIL_CONNECTOR_SETUP.md)**.
3. (Optional) Add `drafts/` to `.gitignore`.
4. In Claude Code: "read my emails and draft replies".

## Files

| Path                                       | What it is                                  |
| ------------------------------------------ | ------------------------------------------- |
| `PLAN_OF_ACTION.md`                        | Ordered execution checklist (Claude/Codex)  |
| `guide for implementing email replies.md`  | Paste-into-Claude setup guide (full code)   |
| `GMAIL_CONNECTOR_SETUP.md`                 | One-time Gmail connector auth (claude.ai)   |
| `.claude/skills/email-replies/SKILL.md`    | The inbox → drafts skill                     |
| `.claude/commands/reply.md`                | `/reply <message>` single-reply command      |


---

> 📄 **`email-replies-module/PLAN_OF_ACTION.md`**

# Plan of action — add email reading + reply drafting to this agent

**Audience: the coding agent (Claude Code, Codex, or similar) doing the work.**
These files are ready-made — integrate them as-is; don't rebuild the feature.
This is the ordered execution plan. The full skill/command source lives in the
guide — open it and copy code from it:

- `guide for implementing email replies.md`

Work top to bottom. Don't skip steps. Each step has a ✅ done-check.

---

## Goal
Give the user's agent the ability to **read their unread Gmail and draft replies
in the agent's own voice**, saved to `drafts/replies-<date>.md`. Read-only:
never send, never mark as read. End state: a working skill + `/reply` command,
Gmail connected, verified on the real inbox.

## Preconditions (verify first)
- [ ] You are inside the user's agent project (a `CLAUDE.md` is present; a
      `PERSONA.md` may be too — that's the voice source).
- [ ] `claude --version` works (Claude Code installed + logged in).

---

## Steps

### 0. Confirm the stack
- [ ] Check whether the user's agent is **Node.js** (`package.json`/`*.js`) or
      **Python** (`requirements.txt`/`*.py`); ask if unclear. The skill +
      `/reply` files are identical for both — the stack only matters for the
      optional dispatcher-allowlist step (Step 4).
- ✅ Done when: stack noted.

### 1. Install the skill
- [ ] Create `.claude/skills/email-replies/SKILL.md` (create folders as needed)
      with the exact content from the guide.
- ✅ Done when: the file exists with the correct YAML frontmatter (`name`,
      `description`).

### 2. Install the `/reply` command
- [ ] Create `.claude/commands/reply.md` with the exact content from the guide.
- ✅ Done when: the file exists.

### 3. Connect Gmail (USER does this — you can't)
- [ ] Print the connector steps: go to <https://claude.ai/customize/connectors>
      → connect **Gmail** → sign in → allow read access → confirm **Connected**.
- [ ] Tell the user this is web-only auth (not `/mcp`) and is **required** —
      without it the `mcp__claude_ai_Gmail__*` tools won't exist.
- [ ] Wait for the user to confirm Gmail shows Connected.
- ✅ Done when: the user confirms the connector is connected.

### 4. Dispatcher tool access (only if run unattended)
- [ ] If the agent is invoked via a `claude -p` script (`twin.js`/`twin.py`/Slack
      bot): if it uses `--permission-mode bypassPermissions`, do nothing. If it
      uses an `--allowedTools` list, add: `mcp__claude_ai_Gmail`, `Skill`,
      `Read`, `Write`.
- [ ] If the user only runs the skill interactively, skip this step.
- ✅ Done when: the dispatcher (if any) can use Gmail + Skill + Read/Write.

### 5. Keep drafts out of git (optional)
- [ ] Add `drafts/` to `.gitignore`.
- ✅ Done when: `drafts/` is ignored (or the user declined).

### 6. Verify
- [ ] After Gmail is connected, in a Claude Code session in this project ask:
      "read my emails and draft replies".
- [ ] Confirm it reads unread mail (read-only) and reports
      `Drafted N replies → drafts/replies-<date>.md`.
- [ ] Open that file; confirm the voice matches `CLAUDE.md` / `PERSONA.md`.
- [ ] Optionally test `/reply <a pasted message>` for the single-reply path.
- ✅ Done when: a real draft file is produced in the right voice.

### 7. Report
- [ ] Give the user a 3-line summary: the two files added, the reminder that
      Gmail must be connected on the web, and the trigger phrase
      ("read my emails and draft replies").

---

## Guardrails (hold throughout)
- **Read-only.** Never send mail, never mark as read — keep those instructions
  in the skill intact.
- Don't modify `CLAUDE.md` / persona — the voice stays the user's.
- Never invent facts in drafts; use `[bracketed placeholders]`.
- If Gmail tools are missing at runtime, the connector isn't connected — re-do
  Step 3.


---

> 📄 **`email-replies-module/guide for implementing email replies.md`**

# Guide: add email-reading + reply-drafting to your agent

**You are Claude Code or Codex (or any coding agent), reading this file inside the user's agent project.** These files are ready-made — don't rebuild the feature from scratch; just install/wire them in as described below. Your
job: give their agent the ability to **read their unread Gmail and draft replies
in the agent's own voice**, saved to a local file. This is a Claude Code *skill*
plus a `/reply` command — it works the same whether their twin is Node or Python
(it runs inside the Claude session, not in their dispatcher code).

Everything you need is embedded below. Follow the steps in order.

> ## ⚠️ First: confirm the stack
> Check whether the user's agent is **Node.js** (`package.json` / `*.js`) or
> **Python** (`requirements.txt` / `*.py`) — ask if unclear. The skill +
> `/reply` command here are **the same for both languages** (they run inside the
> Claude session, not in dispatcher code). The stack only matters for the
> **optional** dispatcher-allowlist step (Step 4), which has a Node and a Python
> note — apply the one that matches their agent.

---

## The prompt the user pastes (for reference)

> Read `guide for implementing email replies.md` from
> `https://raw.githubusercontent.com/luvishg-growthx/reading-your-emails-and-drafting-a-reply-for-them-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20email%20replies.md`
> and set up email reading + reply drafting for my agent.

---

## What you're installing

1. A skill at `.claude/skills/email-replies/SKILL.md` — triggers when the user
   asks to read their inbox and draft replies; reads unread mail via the Gmail
   connector and writes drafts to `drafts/replies-<date>.md`. **Read-only**:
   never sends, never marks as read.
2. A command at `.claude/commands/reply.md` — `/reply <pasted message>` drafts a
   single reply in the agent's voice.

The voice comes from the user's own `CLAUDE.md` / `PERSONA.md`. This module adds
no persona of its own — it's neutral.

---

## Step 1 — Install the skill

Create `.claude/skills/email-replies/SKILL.md` in the project with **exactly**
this content (create the folders if needed):

````markdown
---
name: email-replies
description: Read the user's unread Gmail and draft replies in the agent's own voice, saved to a single file. Trigger this whenever the user asks to read their email/inbox and draft, write, or prepare replies to their mail.
---

# Email replies → file

When the user asks you to read their email and draft replies, do this:

## 1. Read the inbox
Use the Gmail tools to fetch the user's **unread** emails in the inbox
(up to 15, newest first). For each, get the sender, subject, and body.
**Do NOT send anything. Do NOT mark anything as read.**

Skip obvious no-reply / marketing / automated blasts unless the user asked for
"all" emails — only draft replies to mail a human would actually reply to.

## 2. Draft each reply in the agent's voice
For every email worth replying to, write a reply in **this agent's voice**. Read
the project's `CLAUDE.md` (and `PERSONA.md` if present) first — that is the
source of truth for tone. The reply must still land the real point, not just
match the vibe. If a reply needs a fact you don't have, leave a marked
placeholder like `[confirm the date]` — never invent.

> If the project has no persona/voice file, write clear, friendly, professional
> replies and note that the user can add a `PERSONA.md` to customize the voice.

## 3. Write everything to ONE file
Save all the drafts into a single Markdown file at:

```
drafts/replies-<today's date YYYY-MM-DD>.md
```

Create the `drafts/` folder if it doesn't exist. Use this layout per email:

```
## 1. <subject>
**From:** <sender>

<the drafted reply>

---
```

## 4. Report back
After writing the file, tell the user in one line how many drafts you wrote and
the exact file path, e.g.:

> Drafted 4 replies → drafts/replies-2026-06-19.md

If there were no unread emails worth replying to, say so plainly and don't
create an empty file.
````

---

## Step 2 — Install the `/reply` command

Create `.claude/commands/reply.md` with **exactly** this content:

```markdown
Draft a reply to the message below.

Write it in this agent's voice — read `CLAUDE.md` (and `PERSONA.md` if present)
for the tone. Output ONLY the reply text — no preamble, no explanation — ready
to copy and send. If a fact is missing, leave a marked placeholder like
`[confirm the date]` instead of inventing it.

Message to reply to:

$ARGUMENTS
```

---

## Step 3 — Connect Gmail (have the USER do this)

The Gmail tools come from Claude's **Gmail connector**, which must be authorized
on the **Claude website** — not inside Claude Code. You (Claude) can't do this;
print these steps and wait for the user to confirm.

1. Go to <https://claude.ai/customize/connectors> (same account as Claude Code).
2. Find **Gmail** → **Connect** → sign in to Google → **Allow** read access.
3. Confirm Gmail shows **Connected**.

> This is required. Without it, the `mcp__claude_ai_Gmail__*` tools won't exist
> and the skill can't read mail. The connector does **not** appear under `/mcp`
> in the terminal — it is web-only auth.

---

## Step 4 — If the agent runs unattended through a dispatcher

If the user invokes their agent through a script that calls `claude -p` (e.g. a
`twin.js` / `twin.py`, or a Slack bot), that dispatcher needs to allow the tools
this skill uses. Two cases:

- **If it already passes `--permission-mode bypassPermissions`** → nothing to do;
  all tools are allowed.
- **If it passes an `--allowedTools` list** → add these entries so the skill can
  run without prompts:
  `mcp__claude_ai_Gmail`, `Skill`, `Read`, `Write`.

  Example (Node): `const ALLOWED = ["mcp__claude_ai_Gmail", "Skill", "Read", "Write"];`

If the user only uses the skill by hand in an interactive Claude Code session,
you can skip this step.

---

## Step 5 — Keep drafts out of git (optional)

Add `drafts/` to `.gitignore` so drafted replies aren't committed.

---

## Step 6 — Verify

Ask the agent (in a Claude Code session in this project, after Gmail is
connected):

> read my emails and draft replies

Expect it to read unread mail and report something like
`Drafted N replies → drafts/replies-<date>.md`. Open that file to check the
voice matches the user's `CLAUDE.md` / `PERSONA.md`.

You can also test the single-message path:

> /reply Hi, are we still on for Thursday 3pm? — Sam

---

## Guardrails (do these, quietly)

- **Read-only.** The skill must never send mail or mark anything as read — keep
  those instructions intact.
- **Don't touch** the user's `CLAUDE.md` / persona — the voice stays theirs.
- **Don't invent facts** in drafts — use `[bracketed placeholders]`.
- The Gmail connector is web-authed; if tools are missing at runtime, that's the
  cause 99% of the time.

When finished, give the user a 3-line summary: the two files you added, the
reminder to connect Gmail on the web, and how to trigger it
("read my emails and draft replies").


---

> 📄 **`email-replies-module/GMAIL_CONNECTOR_SETUP.md`**

# Connect Gmail to your agent (one-time, ~2 minutes)

This feature reads your inbox through Claude's **Gmail connector**. The connector
is authorized on the **Claude website**, not inside Claude Code — so do this
once in your browser.

> Important: connecting Gmail in the Claude **web app** is what makes the
> `mcp__claude_ai_Gmail__*` tools available to Claude Code. You will **not** find
> it under `/mcp` in the terminal — it has to be authed on the web.

## Steps

1. Go to <https://claude.ai/customize/connectors> (log in with the same Claude
   account you use for Claude Code).
2. Find **Gmail** in the connectors list → click **Connect**.
3. A Google sign-in window opens → pick your Google account → **Allow** the
   requested read access.
4. Back on the connectors page, Gmail should show as **Connected**.

## Verify it's working

In a Claude Code session **in your agent's project folder**, ask:

> read my emails and draft replies

If the connector is wired up, Claude will use the Gmail tools to read your unread
mail and write drafts to `drafts/replies-<date>.md`. If it says it has no Gmail
access, re-check that Gmail shows **Connected** on the web page above, then start
a fresh Claude Code session.

## Privacy / safety notes

- The skill is **read-only by design**: it reads unread mail and writes drafts to
  a local file. It is instructed to **never send** anything and **never mark mail
  as read**.
- Drafts land in `drafts/` in your project. Add `drafts/` to `.gitignore` if you
  don't want them committed.


<br>

# ═══ ⏰ SCHEDULER (CRONJOBS) MODULE ═══


---

> 📄 **`cronjobs-module/README.md`**

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
> 2. **Detect the stack** (Node vs Python) and **follow the matching guide** for
>    full code:
>    - Node: `https://raw.githubusercontent.com/luvishg-growthx/cronjobs-and-reminders-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20cronjobs.md`
>    - Python: `https://raw.githubusercontent.com/luvishg-growthx/cronjobs-and-reminders-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20cronjobs%20(python).md`
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
- **Node *or* Python.**

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

(Python twin? swap in `guide%20for%20implementing%20cronjobs%20(python).md`.) Or
just **paste the repo link** and Claude routes itself via the block at the top.

## Manual install

1. Copy the scheduler for your stack into your project root:
   - Node: [`node/scheduler.js`](node/scheduler.js) (+ `npm install dotenv`)
   - Python: [`python/scheduler.py`](python/scheduler.py) (+ `pip install python-dotenv`)
2. Copy [`.claude/skills/schedule-task/SKILL.md`](.claude/skills/schedule-task/SKILL.md)
   into your project's `.claude/`.
3. (Optional) Set `SLACK_BOT_TOKEN` + `SLACK_CHANNEL` in `.env` for Slack delivery.
4. Start the daemon: `node scheduler.js` / `python scheduler.py` (keep it running).
5. Ask your agent to schedule something.

## Files

| Path                                          | What it is                                  |
| --------------------------------------------- | ------------------------------------------- |
| `PLAN_OF_ACTION.md`                           | Ordered execution checklist (Claude/Codex)  |
| `guide for implementing cronjobs.md`          | Setup guide — **Node** (full code)          |
| `guide for implementing cronjobs (python).md` | Setup guide — **Python** (full code)        |
| `.claude/skills/schedule-task/SKILL.md`       | Skill that records jobs (runs the CLI)      |
| `node/` · `python/`                           | `scheduler` (engine, auto-start) + `schedule` (CLI) + env + samples |


---

> 📄 **`cronjobs-module/PLAN_OF_ACTION.md`**

# Plan of action — add cronjobs / scheduled messages to this agent

**Audience: the coding agent (Claude Code, Codex, or any similar agent) doing the work.** These files are ready-made — integrate them as-is; don't rebuild the feature.
Ordered execution plan. Full source is in the guides — open the one for the
detected stack and copy code from it:

- Node: `guide for implementing cronjobs.md`
- Python: `guide for implementing cronjobs (python).md`

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
- [ ] `claude --version` works. Node ≥ 18 (Node twin) or Python 3 (Python twin).

---

## Steps

### 1. Detect the stack
- [ ] Node (`package.json`/`*.js`) or Python (`requirements.txt`/`*.py`). Ask
      once if unclear. Announce it.
- ✅ Done when: stack stated.

### 2. Install the dependency
- [ ] Node: `npm install dotenv`. Python: `pip install python-dotenv`.
- ✅ Done when: installed.

### 3. Create the job-creator CLI
- [ ] `schedule.js` (Node) or `schedule.py` (Python) in the project root, from
      the guide. This is what the skill runs to record jobs reliably.
- ✅ Done when: `node schedule.js --at "2020-01-01T00:00:00" --message test`
      writes a job to `data/jobs.json`.

### 4. Create the scheduler engine
- [ ] `scheduler.js` / `scheduler.py` in the project root, from the guide. It
      exports `startScheduler()` / `start_scheduler()`.
- ✅ Done when: the file exists and exports the start function.

### 5. AUTO-START it inside the twin  ← the critical step
- [ ] Find the twin's startup (terminal chat `main()` / readline, or the bot
      start) and add the start call so the scheduler runs in the same process:
      - Node: `require("./scheduler.js").startScheduler();`
      - Python: `from scheduler import start_scheduler; start_scheduler()`
- [ ] Only if there's truly no editable entry point: fall back to telling the
      user to run the scheduler standalone — but prefer wiring it in.
- ✅ Done when: starting the twin prints `⏰ Scheduler active …` (no separate
      process needed).

### 5b. Make sure the twin can RUN the schedule command (critical)
- [ ] The skill runs `schedule.js`/`schedule.py` via **Bash**. If the twin's
      `claude -p` dispatch can't use Bash, the command is blocked and the twin
      will falsely claim it "needs approval" → scheduling silently fails.
- [ ] If the dispatch uses `--permission-mode bypassPermissions` → fine. If it
      uses an `--allowedTools` allowlist → add `Bash` (and `Skill`).
- ✅ Done when: the twin can run a Bash command without an approval prompt.

### 6. Install the schedule-task skill
- [ ] `.claude/skills/schedule-task/SKILL.md` from the guide — it tells the twin
      to run the `schedule` CLI (never hand-edit JSON).
- ✅ Done when: the skill file exists with correct frontmatter.

### 7. Ignore runtime state & verify end-to-end
- [ ] Add `data/jobs.json` + `.env` to `.gitignore`.
- [ ] Ask the twin "send me a hi message in 2 minutes". Confirm a job lands in
      `data/jobs.json`, and ~2 min later the scheduler logs `[fire] …` + a
      notification — with no second process running.
- ✅ Done when: a scheduled message fires from the twin alone.

### 8. Report
- [ ] 3-line summary: files added, that the scheduler auto-starts with the twin,
      an example phrase to try.

---

## Guardrails (hold throughout)
- **Automatic, not manual** — wire `startScheduler()` into the twin; never leave
  the user to run a separate scheduler.
- The skill **runs the `schedule` CLI**; never hand-edit `data/jobs.json`.
- One-shot = `runAt`; recurring = `cron`. Never both. Never both `prompt`/`message`.
- Times are local (no timezone suffix). Don't touch `CLAUDE.md` / persona.


---

> 📄 **`cronjobs-module/guide for implementing cronjobs.md`**

# Guide: add cronjobs / scheduled messages to your agent (Node.js)

**You are Claude Code or Codex (or any coding agent), reading this file inside the user's agent project.** These files are ready-made — don't rebuild the feature from scratch; just install/wire them in as described below. Your
job: let their agent **schedule future and recurring messages** — "send me a hi
message at 7:30pm", "remind me every weekday at 9am" — and have it **just work**
with no manual steps. Everything you need is embedded.

> ## ⚠️ First: confirm the stack
> Check whether the user's agent is **Node.js** (`package.json` / `*.js`) or
> **Python** (`requirements.txt` / `*.py`) — ask if unclear. **This is the
> Node.js guide.** If their agent is **Python**, stop and follow
> `guide for implementing cronjobs (python).md` instead.

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


---

> 📄 **`cronjobs-module/guide for implementing cronjobs (python).md`**

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


<br>

# ═══ 🧠 LONG-TERM MEMORY (ENGRAM) MODULE ═══


---

> 📄 **`memory-module/README.md`**

# Long-Term Memory Module (engram)

> ## 🤖 If you are Claude Code or Codex (any coding agent), read this first
>
> **Ready-made — don't rebuild anything.** You do **not** need to write or
> reinvent this feature. Just install/wire in the files as described and the bot
> gains the capability. These files work the same with Claude Code or Codex.
>
> The user pasted this repo because they want to give their AI agent **long-term
> memory** — so it recalls relevant past conversations before answering and gets
> sharper over time. Do this:
>
> 1. **Follow `PLAN_OF_ACTION.md`** — the ordered execution checklist (works for
>    Claude *or* Codex).
> 2. **Detect the stack** (Node vs Python) and **follow the matching guide** for
>    full code:
>    - Node: `https://raw.githubusercontent.com/luvishg-growthx/long-term-memory-engram-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20memory.md`
>    - Python: `https://raw.githubusercontent.com/luvishg-growthx/long-term-memory-engram-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20memory%20(python).md`
> 3. It installs **engram** (from the fork) + a small `memory` wrapper and wires
>    `recall → inject → remember` into the twin's dispatch. Voice stays the
>    user's `CLAUDE.md` / `PERSONA.md` — add no persona of your own.
>
> Everything below is human-facing context.

---

Give your Claude Code agent a memory that compounds. Built on
[**engram**](https://github.com/luvishg-growthx/engram-memory) — a plug-and-play
associative-memory layer: hybrid (semantic + lexical) recall over a single SQLite
file, an associative graph, and "dreaming" consolidation. **Offline by default,
no API key.**

- **Recall before answering.** The most relevant past memories are injected into
  the prompt each turn.
- **Remember after answering.** Each turn is saved, tagged by importance.
- **Self-improving.** Nightly `dream()` promotes memories that prove useful and
  forgets the noise — recall sharpens the longer you run it.
- **Your voice stays yours.** Memory is additive; personality is still your
  `CLAUDE.md` / `PERSONA.md`.
- **Node *or* Python.** (Python shells out to the engram CLI.)

## How it works

```
incoming message
   │
   ▼  recall the top-k relevant past memories
engram recall ─────────────────────────────┐
   │                                        │ injected into the prompt
   ▼                                        ▼
your twin answers (claude -p) with that context
   │
   ▼  save what happened
engram add
   │
   … nightly: engram dream → promote proven memories, forget noise …
```

## The fastest way to install it (recommended)

Open **Claude Code inside your agent's project folder** and paste:

```
Read this and set up long-term memory for my agent:
https://raw.githubusercontent.com/luvishg-growthx/long-term-memory-engram-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20memory.md
```

(Python twin? swap in `guide%20for%20implementing%20memory%20(python).md`.) Or
just **paste the repo link** and Claude routes itself via the block at the top.

## Manual install

1. Install engram from the fork:
   - Node: `npm install github:luvishg-growthx/engram-memory`
   - Python: `npm install -g github:luvishg-growthx/engram-memory` (needs Node ≥ 20)
2. Copy the wrapper into your project root:
   - Node: [`node/memory.js`](node/memory.js)
   - Python: [`python/memory.py`](python/memory.py)
3. Wire `recall → inject → remember` into your twin's dispatch (see the guide).
4. Add `memory/*.db` to `.gitignore`.

## Credit

engram is MIT-licensed, by [@anmolm-growthx](https://github.com/anmolm-growthx/engram-memory);
this module uses a fork at
[`luvishg-growthx/engram-memory`](https://github.com/luvishg-growthx/engram-memory).

## Files

| Path                                         | What it is                                 |
| -------------------------------------------- | ------------------------------------------ |
| `PLAN_OF_ACTION.md`                          | Ordered execution checklist (Claude/Codex) |
| `guide for implementing memory.md`           | Setup guide — **Node** (full code)         |
| `guide for implementing memory (python).md`  | Setup guide — **Python** (full code)       |
| `node/memory.js` · `python/memory.py`        | The memory wrapper for each stack          |


---

> 📄 **`memory-module/PLAN_OF_ACTION.md`**

# Plan of action — give this agent long-term memory (engram)

**Audience: the coding agent (Claude Code, Codex, or any similar agent) doing the work.** These files are ready-made — integrate them as-is; don't rebuild the feature.
Ordered execution plan. Full source is in the guides — open the one for the
detected stack and copy code from it:

- Node: `guide for implementing memory.md`
- Python: `guide for implementing memory (python).md`

Work top to bottom. Each step has a ✅ done-check.

---

## Goal
Wire **engram** (SQLite associative memory, offline, no API key) into the twin so
it recalls relevant past memories before each turn and saves new ones after —
making it self-improving. Voice stays the user's `CLAUDE.md` / `PERSONA.md`.

## Preconditions
- [ ] Inside the user's agent project (a `CLAUDE.md` / persona is present).
- [ ] **Node ≥ 20** (`node --version`) — engram's CLI needs it even for Python twins.
- [ ] `claude --version` works.

---

## Steps

### 1. Detect the stack
- [ ] Node (`package.json`/`*.js`) or Python (`requirements.txt`/`*.py`). Ask
      once if unclear. Announce it.
- ✅ Done when: stack stated.

### 2. Install engram (from the fork)
- [ ] Node: `npm install github:luvishg-growthx/engram-memory` (local bin at
      `node_modules/.bin/engram`).
- [ ] Python: `npm install -g github:luvishg-growthx/engram-memory` (global
      `engram` on PATH). Confirm with `engram help`.
- ✅ Done when: the `engram` CLI runs.

### 3. Add the memory wrapper
- [ ] Create `memory.js` (Node) or `memory.py` (Python) in the project root,
      using the code from the matching guide.
- ✅ Done when: the wrapper file exists.

### 4. Wire it into the twin's dispatch
- [ ] Find where the twin calls `claude -p` (e.g. `ask()`).
- [ ] **Before** the call: `recallContext`/`recall_context(message)` → prepend to
      the prompt.
- [ ] **After** the reply: `remember(...)` the turn.
- [ ] If the twin has multiple faces (terminal, Slack), wire into the **shared**
      dispatch so all faces get memory. Keep edits additive — don't rewrite.
- ✅ Done when: dispatch recalls before and remembers after.

### 5. Nightly maintenance (optional)
- [ ] If a scheduler/cron exists, call `dream()` once a day (e.g. 03:00). Else
      note the user can cron `engram dream --db memory/agent-memory.db`.
- ✅ Done when: scheduled or explicitly skipped.

### 6. Ignore the DB & verify
- [ ] Add `memory/*.db` to `.gitignore`.
- [ ] Round-trip test (from the guide): `remember(...)` then `recallContext(...)`
      and confirm the memory comes back in a "Relevant memories" block.
- ✅ Done when: a saved memory is recalled.

### 7. Report
- [ ] 3-line summary: engram installed, wrapper added + wired into the dispatch,
      and how to verify.

---

## Guardrails (hold throughout)
- **Additive only** — add the wrapper + recall/remember lines; never rewrite the
  twin or touch `CLAUDE.md` / persona.
- **Best-effort** — memory failures must never break a reply (the wrapper no-ops).
- The `memory/*.db` index is a rebuildable cache; the user's notes/markdown stay
  the source of truth.


---

> 📄 **`memory-module/guide for implementing memory.md`**

# Guide: give your agent long-term memory (Node.js)

**You are Claude Code or Codex (or any coding agent), reading this file inside the user's agent project.** These files are ready-made — don't rebuild the feature from scratch; just install/wire them in as described below. Your
job: wire **long-term memory** into their twin using **engram** (a plug-and-play
associative-memory layer, backed by one SQLite file, no API keys). After this,
the twin recalls relevant past memories before each turn and writes new ones
after — so it gets sharper the longer it runs. Everything you need is embedded.

> ## ⚠️ First: confirm the stack
> Check whether the user's agent is **Node.js** (`package.json` / `*.js`) or
> **Python** (`requirements.txt` / `*.py`) — ask if unclear. **This is the
> Node.js guide.** If their agent is **Python**, stop and follow
> `guide for implementing memory (python).md` instead.

---

## The prompt the user pastes (for reference)

> Read `guide for implementing memory.md` from
> `https://raw.githubusercontent.com/luvishg-growthx/long-term-memory-engram-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20memory.md`
> and set up long-term memory for my agent.

---

## How it works (the loop)

```
incoming message
   │
   ▼
recallContext(msg) ──► engram recall ──► top-k past memories
   │                                       (injected into the prompt)
   ▼
your twin answers (claude -p) with that context
   │
   ▼
remember(...)  ──► engram add ──► this turn saved to the SQLite memory
   │
   … nightly: dream() promotes proven memories, forgets the noise …
```

engram is offline by default (no API key). The voice/personality stays the
user's `CLAUDE.md` / `PERSONA.md`; memory just gives it recall.

---

## Step 0 — Prerequisite

engram needs **Node ≥ 20**. Check `node --version`. (Even a Python twin needs
Node for the engram CLI — see the Python guide.)

---

## Step 1 — Install engram (from the fork)

```
npm install github:luvishg-growthx/engram-memory
```

This compiles on install and drops the `engram` CLI at
`node_modules/.bin/engram`. (The only native dep is `better-sqlite3`.)

---

## Step 2 — Add the memory wrapper

Create `memory.js` in the project **root** with this content:

```javascript
// memory.js — long-term memory for your twin, powered by engram. Best-effort:
// no-ops if engram isn't installed so the twin always keeps working.
const { spawnSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const ENGRAM = process.env.ENGRAM_BIN || path.join(__dirname, "node_modules", ".bin", "engram");
const DB = process.env.ENGRAM_DB || path.join(__dirname, "memory", "agent-memory.db");

function available() {
  return process.env.ENGRAM_BIN ? true : fs.existsSync(ENGRAM);
}
function run(args) {
  fs.mkdirSync(path.dirname(DB), { recursive: true });
  return spawnSync(ENGRAM, [...args, "--db", DB], {
    cwd: __dirname, encoding: "utf8", maxBuffer: 1024 * 1024 * 10,
  });
}
function recallContext(query, k = 5) {
  if (!available() || !query) return "";
  try {
    const r = run(["recall", query, "--json", "-k", String(k), "--mark-used"]);
    if (r.status !== 0) return "";
    const hits = JSON.parse(r.stdout || "[]");
    if (!Array.isArray(hits) || hits.length === 0) return "";
    const lines = hits.map((h, i) => `${i + 1}. ${String(h.content || "").replace(/\s+/g, " ").slice(0, 300)}`);
    return ["## Relevant memories (from past conversations)", ...lines].join("\n");
  } catch (_) { return ""; }
}
function remember(text, importance = 5, tier = "episodic") {
  if (!available() || !text) return;
  try { run(["add", text, "--tier", tier, "--importance", String(importance)]); } catch (_) {}
}
function dream() {
  if (!available()) return;
  try { run(["dream"]); } catch (_) {}
}
module.exports = { recallContext, remember, dream, available, DB };
```

---

## Step 3 — Wire it into the twin's dispatch

Find where the twin calls `claude -p` — usually a function like `ask(message)`
in `twin.js` / `slack-bot.js`. Make two small edits:

1. At the top of the file: `const memory = require("./memory.js");`
2. **Before** building the `claude -p` args, recall and prepend context:

```javascript
const recalled = memory.recallContext(message);
const prompt = recalled ? `${recalled}\n\n---\n\n${message}` : message;
// …then pass `prompt` to `claude -p` instead of the raw `message`.
```

3. **After** the reply comes back, save the turn:

```javascript
memory.remember(`User said: "${message.slice(0,200)}". Twin replied: "${reply.slice(0,200)}"`, 5);
```

Keep the edits minimal — don't rewrite the dispatch, just add recall before and
remember after. If the twin has multiple faces (terminal, Slack), wire it into
the **shared** `ask()` so every face gets memory.

---

## Step 4 — Nightly maintenance (optional but recommended)

If the user has the scheduler/cron module, add nightly `dream()`:

```javascript
// in scheduler.js tick(), once a day (e.g. 03:00):
if (now.getHours() === 3 && now.getMinutes() === 0) require("./memory.js").dream();
```

Otherwise they can run `node_modules/.bin/engram dream --db memory/agent-memory.db`
on a system cron.

---

## Step 5 — Ignore the DB & verify

1. Add `memory/*.db` to `.gitignore` (the index is a rebuildable local cache).
2. **Restart the twin** so the running process picks up the memory wiring (a twin
   started before this change has no memory layer).
3. Verify the round-trip:

```
node -e "const m=require('./memory.js'); m.remember('test memory: the demo worked', 7); console.log(m.recallContext('did the demo work?'))"
```

Expect the test memory to come back in a "Relevant memories" block. Then have a
real conversation and confirm later turns recall earlier ones.

---

## (Optional) Better semantic recall & reranking

- The default embedder is offline/lexical-ish. For true semantics, the user can
  set `OPENAI_API_KEY` and pass `--provider openai` (or edit the wrapper).
- engram can **rerank** with the Claude subscription (no API key) via
  `--llm claude --rerank`. Skip unless asked — the default is fast and offline.

---

## Guardrails (do these, quietly)

- **Additive only.** Add `memory.js` + the recall/remember lines; don't rewrite
  the twin or touch `CLAUDE.md` / persona.
- **Best-effort.** Memory failures must never break a reply (the wrapper no-ops).
- The SQLite file under `memory/` is a rebuildable cache — safe to gitignore.

When finished, give the user a 3-line summary: engram installed, `memory.js`
added + wired into `ask()`, and how to verify.


---

> 📄 **`memory-module/guide for implementing memory (python).md`**

# Guide: give your agent long-term memory (Python)

**You are Claude Code or Codex (or any coding agent), reading this file inside the user's agent project.** These files are ready-made — don't rebuild the feature from scratch; just install/wire them in as described below. Your
job: wire **long-term memory** into their twin using **engram** (a plug-and-play
associative-memory layer, backed by one SQLite file, no API keys). After this,
the twin recalls relevant past memories before each turn and writes new ones
after. Everything you need is embedded.

> ## ⚠️ First: confirm the stack
> Check whether the user's agent is **Node.js** (`package.json` / `*.js`) or
> **Python** (`requirements.txt` / `*.py`) — ask if unclear. **This is the
> Python guide.** If their agent is **Node.js**, stop and follow
> `guide for implementing memory.md` instead.

---

## The prompt the user pastes (for reference)

> Read `guide for implementing memory.md` from
> `https://raw.githubusercontent.com/luvishg-growthx/long-term-memory-engram-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20memory.md`
> and set up long-term memory for my agent.

(For a Python twin, point the same prompt at
`https://raw.githubusercontent.com/luvishg-growthx/long-term-memory-engram-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20memory%20(python).md`
instead.)

---

## How it works (the loop)

```
incoming message
   │
   ▼
recall_context(msg) ──► engram recall ──► top-k past memories (injected)
   │
   ▼
your twin answers (claude -p) with that context
   │
   ▼
remember(...) ──► engram add ──► this turn saved to SQLite
   │
   … nightly: dream() promotes proven memories, forgets the noise …
```

engram is offline by default (no API key). Voice/personality stays the user's
`CLAUDE.md` / `PERSONA.md`; memory just gives it recall.

---

## Step 0 — Prerequisite: install the engram CLI (needs Node ≥ 20)

engram is a Node tool. A Python twin shells out to it, so install it **globally**
once so `engram` is on PATH:

```
npm install -g github:luvishg-growthx/engram-memory
```

Check it: `engram help`. (No Node? Install Node ≥ 20 first.)

---

## Step 1 — Add the memory wrapper

Create `memory.py` in the project **root** with this content:

```python
"""memory.py — long-term memory for your twin, powered by engram (CLI).
Best-effort: no-ops if engram isn't installed so the twin always keeps working."""
import json, os, shutil, subprocess
from pathlib import Path

ENGRAM = os.environ.get("ENGRAM_BIN", "engram")
DB = os.environ.get("ENGRAM_DB", str(Path(__file__).resolve().parent / "memory" / "agent-memory.db"))


def available() -> bool:
    return shutil.which(ENGRAM) is not None or os.path.exists(ENGRAM)


def _run(args):
    Path(DB).parent.mkdir(parents=True, exist_ok=True)
    return subprocess.run([ENGRAM, *args, "--db", DB], capture_output=True, text=True)


def recall_context(query, k=5):
    if not available() or not query:
        return ""
    try:
        r = _run(["recall", query, "--json", "-k", str(k), "--mark-used"])
        if r.returncode != 0:
            return ""
        hits = json.loads(r.stdout or "[]")
        if not hits:
            return ""
        lines = [f"{i+1}. {' '.join(str(h.get('content','')).split())[:300]}" for i, h in enumerate(hits)]
        return "## Relevant memories (from past conversations)\n" + "\n".join(lines)
    except Exception:
        return ""


def remember(text, importance=5, tier="episodic"):
    if not available() or not text:
        return
    try:
        _run(["add", text, "--tier", tier, "--importance", str(importance)])
    except Exception:
        pass


def dream():
    if not available():
        return
    try:
        _run(["dream"])
    except Exception:
        pass
```

---

## Step 2 — Wire it into the twin's dispatch

Find where the twin calls `claude -p` (e.g. a `subprocess.run(["claude","-p",...])`
inside an `ask()` function). Make two small edits:

1. `import memory` at the top.
2. **Before** the `claude -p` call, recall and prepend context:

```python
recalled = memory.recall_context(message)
prompt = f"{recalled}\n\n---\n\n{message}" if recalled else message
# …pass `prompt` to claude -p instead of the raw `message`.
```

3. **After** the reply:

```python
memory.remember(f'User said: "{message[:200]}". Twin replied: "{reply[:200]}"', 5)
```

Keep edits minimal. If the twin has multiple faces (terminal, Slack), wire it
into the **shared** dispatch so every face gets memory.

---

## Step 3 — Nightly maintenance (optional but recommended)

If the user has the scheduler/cron module, call `memory.dream()` once a day
(e.g. at 03:00). Otherwise run `engram dream --db memory/agent-memory.db` on a
system cron.

---

## Step 4 — Ignore the DB & verify

1. Add `memory/*.db` to `.gitignore` (rebuildable local cache).
2. **Restart the twin** so the running process picks up the memory wiring (a twin
   started before this change has no memory layer).
3. Verify the round-trip:

```
python -c "import memory; memory.remember('test memory: the demo worked', 7); print(memory.recall_context('did the demo work?'))"
```

Expect the test memory back in a "Relevant memories" block.

---

## (Optional) Better semantic recall & reranking

- Default embedder is offline/lexical-ish. For true semantics, set
  `OPENAI_API_KEY` and pass `--provider openai` to engram.
- engram can rerank with the Claude subscription (no API key) via
  `--llm claude --rerank`. Skip unless asked.

---

## Guardrails (do these, quietly)

- **Additive only.** Add `memory.py` + the recall/remember lines; don't rewrite
  the twin or touch `CLAUDE.md` / persona.
- **Best-effort.** Memory failures must never break a reply (the wrapper no-ops).
- The SQLite file under `memory/` is a rebuildable cache — safe to gitignore.

When finished, give the user a 3-line summary: engram installed (global),
`memory.py` added + wired into the dispatch, and how to verify.
