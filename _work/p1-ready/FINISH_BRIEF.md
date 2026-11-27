# Finishing pass brief (requests + decision batch D)

Read `RUN_BRIEF.md` first (hard rules apply), then `WRITER_BRIEF.md` (documents) or `STORY_EDITOR_BRIEF.md` (stories).

Everything you edit already has a staged next version in STAGE (v3 stories, next-version documents). Edit those staged files in place; never touch SET originals. If a file you must change has NO staged version yet, copy its highest SET version to STAGE as the next version first.

## Authority (in order)
1. `SET\24 P1 Developer Readiness v1\decisions\batch-D.md` – rulings RD-P1-060..074 and their **amendments** to the first register (RD-P1-003/040 JOB-08 → rwb-integration; RD-P1-007 rule 7 externalRef = barcode else noticeRef, business key accordingly; RD-P1-010 rule 8 gate DP01 + DP05; RD-P1-020 rwb_source_data gets the library decision_record table; RD-P1-027 act-time CARRY fields, DF-LEG-005 key, DM002 clause moves to DM005; ASM-5391 changed). Batch D wins over the first register where it amends it.
2. `SET\24 P1 Developer Readiness v1\Recovery Workbench P1 Decision Register v1.md` – final rulings RD-P1-001..048.
3. Requests: `SET\_work\p1-ready\packets\requests all agents.csv` – filter rows whose `target`/`file` is one of your files (match by base name without version). Apply each request that a ruling or source supports; otherwise log why not.
4. Test-case backfill: `SET\_work\p1-ready\tc-backfill.csv` (story_key, ac_id, tc_id) – story editors replace "TC: to be added in Test Cases v9 (W2-tests)" and stale TC citations in section 16 / the AC rows with the mapped IDs. Do not invent TC IDs.
5. `SET\_work\p1-ready\ESCALATIONS.md` – "Extra stories to edit" and the check lists (batch D gives verdicts on them).

## Logging
Append to your own edit log `SET\_work\p1-ready\editlog\<agent>.csv` (RUN_BRIEF format). New gaps keep temp IDs `NEW-GAP-<agent>-n` (batch D's are NEW-GAP-D1..D5); the register writer numbers them later. Close or reference existing GAP/ASM IDs only after checking their text in STAGE\23 Document Gaps v3.

## Done means
Every request row for your files is applied or answered in your log (action REQUEST-DONE or REQUEST-REJECTED with reason, edit_id of the request in finding_refs), every batch-D ruling naming your files is applied, the brief's self-check passes. Reply with counts: rulings applied, requests done / rejected, new gaps, files touched.
