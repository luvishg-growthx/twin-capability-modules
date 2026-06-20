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
