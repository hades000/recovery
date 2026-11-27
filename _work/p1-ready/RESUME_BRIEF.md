# Resume brief (for agents restarting work that a Codex run left part-way)

Read `RUN_BRIEF.md` and your phase brief (WRITER_BRIEF.md or STORY_EDITOR_BRIEF.md) first; they apply in full.

1. The earlier run (model gpt-6-luna or gpt-6.2-sol) stopped on a usage limit. Its staged files in STAGE are your starting point. NEVER re-copy from SET over a staged file.
2. Reconstruct the log first: read the earlier agent's edit log in EDITLOG (if any). Then compare each staged file with its SET predecessor (python difflib on text; for xlsx compare cell values sheet by sheet with openpyxl; for docx compare paragraph and table-cell text with python-docx). For every changed block that has no log row, append a row to the SAME agent's log file with model "gpt-6-luna (reconstructed by <your model>)" and action EDIT/ADD/REMOVE. Keep the reconstruction compact: one row per changed section, not per character.
3. Check the earlier run's work against the final rulings (register in SET\24 P1 Developer Readiness v1\) and fix anything wrong (e.g. broken table formatting, "?" characters replacing separators, stale version labels, numbering clashes).
4. Finish the remaining work of the original task (quoted in your task), log every new edit under the same agent name with your own model, and run the brief's self-check.
5. Gap numbers: new gaps get temp IDs `NEW-GAP-<agent>-n` in the story/document and a NEW-GAP log row. Do NOT assign real GAP/ASM numbers yourself; the register writer assigns them later. Where an earlier run assigned real numbers itself (e.g. GAP-3283..3287), check them against STAGE\23 Document Gaps\Recovery Workbench Gap Register v3.md – if the number is not in the register with the same subject, replace it with a temp ID and log it.
