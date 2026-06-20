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
