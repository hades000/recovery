# Story finishing task (shared by groups G1–G9)

Read FINISH_BRIEF.md, RUN_BRIEF.md and STORY_EDITOR_BRIEF.md (this folder) first.

Scope: the story files of your group (your task names the service folder(s) and file-name prefixes). Work on the staged v3 files in `STAGE\04 User stories\Recovery Workbench Service Story Files v3\<service folder>\`. If a story of your group must change but has no v3 yet, copy its v2 from SET to that folder as v3 first.

A story in your group needs work when ANY of these is true:
1. It is named in a batch-D decision's affected stories (batch-D.csv `affected_stories` column) or batch-D.md text, or a register amendment changes something it states.
2. A row in `packets\requests all agents.csv` targets its file (match the file base name without version).
3. `tc-backfill.csv` has rows for its story_key (replace "TC: to be added in Test Cases v9 (W2-tests)" and stale TC citations with the mapped TC IDs; do not invent IDs).
4. It is listed under "Extra stories to edit" in ESCALATIONS.md.
5. It still contains a known stale item: 122/1,366 dictionary counts without "at least" (RD-P1-025: at least 123 / 1,379); old DecisionRecorded name rwb.decision-record.DecisionRecorded; rwb_sandbox_next or a sandbox rename; case_list_row / CaseListBuildWorkflow / DailyCaseList in a P1 story except as removed; GAP-3283..3299 citations (not in the register); v5 English of MSG-GEN-006 / MSG-P4-001 where Error and Message Standard v6 changed it.

For each such story make the targeted edits, add the batch-D IDs to its "Readiness decisions" header row and one bullet to its "Version 3 changes" note, and log every edit (finding_refs = request edit_id or `RD-P1-0xx`). Answer every request row for your files with REQUEST-DONE or REQUEST-REJECTED (reason). Keep context small: one story at a time, grep before reading.
Reply with: stories changed, requests done / rejected, TC IDs inserted, new gaps.
