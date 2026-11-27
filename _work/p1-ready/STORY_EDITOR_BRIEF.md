# Story editor brief (Phase 5 – P1 stories; Phase 4 – affected stories)

Read `RUN_BRIEF.md` (same folder) first – its hard rules apply in full.

## What you produce
For each story file in your task: the next version in STAGE at
`STAGE\04 User stories\Recovery Workbench Service Story Files v3\<service folder>\<same file name with v2 → v3>`
(copy the v2 file there first, then edit the copy). Never edit the v2 file. Edit only the stories in your task.

## Authority, in order
1. `SET\24 P1 Developer Readiness v1\Recovery Workbench P1 Decision Register v1.md` – the "Final ruling" paragraph of every RD-P1 decision that names this story, its service, or any artefact it touches (operation, event, table, workflow, message, role, parameter). The register's conflict table (X-01 … X-28) is binding too: e.g. the case list leaves P1 (RD-P1-024 / X-01); RWB-P1-E1002-CON is retired with a pointer (X-27).
2. The story's review: `C:\Users\SahilMore\Downloads\RWB Story Review P1\stories\<STORY KEY>\<STORY KEY> review.md` and `... findings.csv` (sections C, D, E: gaps, AC rewrites, missing ACs) plus blocker verdicts in `REVIEW\_verify\*.csv` (Confirmed / Downgrade). (Affected stories outside P1 have no review yet in phase 4 – your task says what to do.)
3. The sources the review cites (Service Story Files v2 siblings, registers, design documents – use REVIEW\_reference extracts for xlsx/docx).

## How to edit
- Fix every real finding in the story: apply the AC rewrites from section D (make each Then check data written, status, event, decision/audit record and message as applicable, with concrete values), add the missing ACs from section E with the next free AC/X IDs, resolve ambiguous wording from section 4 of the review with a precise rewrite, correct names/paths/codes/fields to the final rulings and the published sources, remove legacy markers the review lists (old views, extension tables, old schema, old test IDs) or mark them "as-built regression only" where a ruling says so.
- Header table: keep keys; update "Contract version" (e.g. rwb-source-data.yaml 5.1.0 per RD-P1-005 where the story consumes/publishes the P1 contract), "Depends on" / "Contract dependencies" per the rulings, add a row "Readiness decisions" listing the RD-P1 IDs applied. Do NOT mark delivery-only items done: Size, epic design sign-off, CON Done, fake published, test data in DEV stay "Not specified"/"Pending" and are listed in a new final section "Remaining delivery steps" (one bullet each, owner role).
- Test cases: cite TC IDs that exist in Test Cases v8, or (if the AC is new/changed) write "TC: to be added in Test Cases v9 (W2-tests)" – the test writer is adding rows in parallel; do not invent TC IDs.
- Gaps/assumptions: cite existing GAP-/ASM- IDs exactly. For new ones raised by the register use the temp IDs from `SET\24 P1 Developer Readiness v1\New gaps and assumptions from decisions v1.csv` (e.g. NEW-GAP-X1) – they are replaced with real numbers by script later. If you find a gap no ruling or source settles, write "Pending: <what>, owner <role>" and log NEW-GAP.
- Keep the story's structure and all unchanged text identical. Add at the top a short "Version 3 changes" note (2–6 bullets) naming the RD-P1 decisions and the finding refs fixed.
- Sentence case, roles not names, no personal data.

## Log
Append every change to `SET\_work\p1-ready\editlog\<your agent name>.csv` (format in RUN_BRIEF; file = story path; finding_refs = `<KEY>#<gap_no>`). Log `REQUEST` rows for document changes you need (target document in `file`) and `CLOSE-GAP`/`CLOSE-ASM` rows for gap/assumption rows your edit settles (with the ID and the reason).

## Self-check before you finish (per story)
Re-read your v3 file: every Confirmed blocker of the story is fixed or explicitly "Pending … GAP/temp id"; no AC uses "correct/valid/as expected"; every AC has Given/When/Then and an ID; no reference to case_list_row/CaseListBuildWorkflow/DailyCaseList in P1 except as removed; event types and topic names match RD-P1-003/008; error answers match RD-P1-001/004/006.
Reply with one line per story: key, v3 path, findings fixed / left (count), open pending items.
