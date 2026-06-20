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
