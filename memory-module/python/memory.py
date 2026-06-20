"""memory.py — long-term memory for your twin, powered by engram.

Wraps the `engram` CLI (from github:luvishg-growthx/engram-memory). Call this
around every turn to make your twin self-improving:
  - recall_context(msg) -> pull the most relevant past memories to inject
  - remember(text)      -> save what happened this turn
  - dream()             -> nightly maintenance (promote useful, forget noise)

Best-effort: if engram isn't installed or a call fails, these become no-ops so
the twin keeps working.

engram is a Node CLI, so install it once (Node >= 20):
    npm install -g github:luvishg-growthx/engram-memory
Then `engram` is on your PATH and this module just shells out to it.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

# `engram` global command by default; override with ENGRAM_BIN.
ENGRAM = os.environ.get("ENGRAM_BIN", "engram")
DB = os.environ.get("ENGRAM_DB", str(Path(__file__).resolve().parent / "memory" / "agent-memory.db"))


def available() -> bool:
    return shutil.which(ENGRAM) is not None or os.path.exists(ENGRAM)


def _run(args: list) -> subprocess.CompletedProcess:
    Path(DB).parent.mkdir(parents=True, exist_ok=True)  # engram needs the dir to exist
    return subprocess.run([ENGRAM, *args, "--db", DB], capture_output=True, text=True)


def recall_context(query: str, k: int = 5) -> str:
    """Recall top-k relevant memories as a context block ready to prepend to a prompt."""
    if not available() or not query:
        return ""
    try:
        r = _run(["recall", query, "--json", "-k", str(k), "--mark-used"])
        if r.returncode != 0:
            return ""
        hits = json.loads(r.stdout or "[]")
        if not hits:
            return ""
        lines = [
            f"{i + 1}. {' '.join(str(h.get('content', '')).split())[:300]}"
            for i, h in enumerate(hits)
        ]
        return "## Relevant memories (from past conversations)\n" + "\n".join(lines)
    except Exception:
        return ""


def remember(text: str, importance: int = 5, tier: str = "episodic") -> None:
    """Save a memory. importance is 1..10. tier defaults to episodic (a single event)."""
    if not available() or not text:
        return
    try:
        _run(["add", text, "--tier", tier, "--importance", str(importance)])
    except Exception:
        pass


def dream() -> None:
    """Nightly maintenance — promote proven memories, archive the noise."""
    if not available():
        return
    try:
        _run(["dream"])
    except Exception:
        pass
