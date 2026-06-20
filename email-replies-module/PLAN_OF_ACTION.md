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
