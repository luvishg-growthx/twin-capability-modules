// memory.js — long-term memory for your twin, powered by engram.
//
// Wraps the `engram` CLI (installed from github:luvishg-growthx/engram-memory).
// Call this around every turn to make your twin self-improving:
//   - recallContext(msg)  → pull the most relevant past memories to inject
//   - remember(text)      → save what happened this turn
//   - dream()             → nightly maintenance (promote useful, forget noise)
//
// Best-effort: if engram isn't installed or a call fails, these become no-ops so
// the twin keeps working.

const { spawnSync } = require("child_process");
const path = require("path");
const fs = require("fs");

// Local install puts the bin here. Override with ENGRAM_BIN (e.g. a global install).
const ENGRAM =
  process.env.ENGRAM_BIN || path.join(__dirname, "node_modules", ".bin", "engram");
const DB = process.env.ENGRAM_DB || path.join(__dirname, "memory", "agent-memory.db");

function available() {
  return process.env.ENGRAM_BIN ? true : fs.existsSync(ENGRAM);
}

function run(args) {
  fs.mkdirSync(path.dirname(DB), { recursive: true }); // engram needs the dir to exist
  return spawnSync(ENGRAM, [...args, "--db", DB], {
    cwd: __dirname,
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 10,
  });
}

// Recall top-k relevant memories as a context block ready to prepend to a prompt.
function recallContext(query, k = 5) {
  if (!available() || !query) return "";
  try {
    const r = run(["recall", query, "--json", "-k", String(k), "--mark-used"]);
    if (r.status !== 0) return "";
    const hits = JSON.parse(r.stdout || "[]");
    if (!Array.isArray(hits) || hits.length === 0) return "";
    const lines = hits.map(
      (h, i) => `${i + 1}. ${String(h.content || "").replace(/\s+/g, " ").slice(0, 300)}`,
    );
    return ["## Relevant memories (from past conversations)", ...lines].join("\n");
  } catch (_) {
    return "";
  }
}

// Save a memory. importance is 1..10. tier defaults to episodic (a single event).
function remember(text, importance = 5, tier = "episodic") {
  if (!available() || !text) return;
  try {
    run(["add", text, "--tier", tier, "--importance", String(importance)]);
  } catch (_) {}
}

// Nightly maintenance — promote proven memories, archive the noise.
function dream() {
  if (!available()) return;
  try {
    run(["dream"]);
  } catch (_) {}
}

module.exports = { recallContext, remember, dream, available, DB };
