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
