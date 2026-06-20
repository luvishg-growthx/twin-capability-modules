# Guide: give your agent long-term memory (Node.js)

**You are Claude Code or Codex (or any coding agent), reading this file inside the user's agent project.** These files are ready-made — don't rebuild the feature from scratch; just install/wire them in as described below. Your
job: wire **long-term memory** into their twin using **engram** (a plug-and-play
associative-memory layer, backed by one SQLite file, no API keys). After this,
the twin recalls relevant past memories before each turn and writes new ones
after — so it gets sharper the longer it runs. Everything you need is embedded.

> **This module is for Node.js twins** (`package.json` / `*.js`).

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

engram needs **Node ≥ 20**. Check `node --version`.

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
