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
