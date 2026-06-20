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
> 2. **Follow the guide** for full code (this module is for **Node.js** twins):
>    - `https://raw.githubusercontent.com/luvishg-growthx/long-term-memory-engram-setup-guide-for-your-ai-agent/main/guide%20for%20implementing%20memory.md`
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
- **Node.js.**

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

Or just **paste the repo link** and Claude routes itself via the block at the top.

## Manual install

1. Install engram from the fork: `npm install github:luvishg-growthx/engram-memory`
2. Copy the wrapper into your project root: [`node/memory.js`](node/memory.js)
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
| `guide for implementing memory.md`           | Setup guide — **Node.js** (full code)      |
| `node/memory.js`                             | The memory wrapper                         |
