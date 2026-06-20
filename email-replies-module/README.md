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
