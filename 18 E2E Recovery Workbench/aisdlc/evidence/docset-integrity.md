# Document set integrity check

| Field | Value |
|---|---|
| Checked | 19 Nov 2026, by the orchestrator (Claude Code, Opus 5.5), read only |
| Baseline | `document-set-baseline.sha256`, written 17 Nov 2026 23:03 (+07:00) before the first stage. It has 4,832 files |
| Re-hash | `document-set-final.sha256`. Every file under the document set root except `18 E2E Recovery Workbench` (this repository) and `rwb-wt` (story worktrees). It has 14,069 files |
| Method | SHA-256 of each file, compared by path |

## Result

| Check | Count | Meaning |
|---|---|---|
| Baseline files with the same hash today | 4,831 | Unchanged |
| Baseline files with a different hash | 0 | No document was edited |
| Baseline files missing at their path | 1 | `recovery-architecture.pptx` (document set root) |
| Files present now but not in the baseline | 9,238 | See below |

**No document in the baseline was changed.** The one missing file was moved, not edited. It is now at
`Proposed Arch/recovery-architecture.pptx`, with the same SHA-256 as the baseline
(`f2138e09…c8cb3a`). The `Proposed Arch` folder was last changed at 18 Nov 19:24. No log row, stage
artefact or agent session record from this run shows a write to that folder. The opencode session
records only list it.

## Files added since the baseline, by folder

| Folder | Files | Created (18 Nov unless stated) | Assessment |
|---|---|---|---|
| `17 AI-First SDLC Repository v2/17 AI-First SDLC Repository v2 with mcp/` and `... with mcp.zip` | 5,048 | 12:03 to 12:08; zip 16:49 | A copy of the v2 workspace with MCP set-up. It is not used by this run, and no run record writes it |
| `17 AI-First SDLC Repository v2/mcp/` | 3,924 | 12:03 to 12:04 | Same as above |
| `17 AI-First SDLC Repository v2/.claude/` | 18 | 16 Nov | Older than the baseline. It was outside the baseline's scope, and was not written by this run |
| `19 Jira Open Questions/` | 6 | 13:41 to 13:45 | Programme work outside this run |
| `20 RWB-E1-056 Jira Comments/` | 2 | 20:08 to 20:15 | Programme work outside this run |
| `21 Jira Export E2E Workbench/` and `_work/scripts/jira_export.py` | 216 | 20:31 to 20:41 | A Jira export and its script. Not part of this run; no run log row refers to it |
| `Proposed Arch/` | 5 | 16 Nov to 18 Nov | Architecture drafts, plus the moved `.pptx` above |
| `aisdlc-toolkit-main/mcp.zip`, `aisdlc-toolkit-main/repo-template/` | 15 | 18 Nov 11:24; 16 Nov | Toolkit additions. Not written by this run |
| `.mcp.json`, `.vscode/settings.json` (root) | 2 | 12:43 | Editor and MCP settings |
| **`RecoveryMigrationIT.java`** (root) | 1 | **12:06:45** | **Empty file (0 bytes).** Created during the opencode period, while RWB-E1-044 was being built. It is most likely a stray shell redirect by that session. The real file is in this repository under `backend/src/test/...` |
| **`parameter-catalog.csv`** (root) | 1 | **15:08:35** | **Empty file (0 bytes).** Created during the opencode period, while RWB-E1-042 was being built. Same likely cause |

## What this means

- The rule "the document set is read only" held for every document in the baseline: none was changed.
- Two empty files were left at the document set root by the opencode session (D-RUN-26 period 2). They hold
  no content and change no document. They are left in place for the owner to delete, because the
  orchestrator does not write to the document set.
- The other new folders are the programme team's own work during the same days. This run neither used nor
  wrote them, as far as its records show: no stage artefact cites them, and no run record writes to them.
