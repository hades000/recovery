# P1 developer-readiness run: brief for every agent

Goal: make every story of service epic RWB-SVC-P1 (rwb-source-data) developer ready, fix the review findings and assumptions, keep the whole document set consistent, and register every decision so later service fixes reuse it instead of redoing it. The user approved this run end to end; do not stop for review – take the best-supported approach and record it.

## Paths
- SET = `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\`
- REVIEW = `C:\Users\SahilMore\Downloads\RWB Story Review P1\` – findings (`all findings.csv`, 1,198 rows; `RWB P1 Review Findings.xlsx`), `themes.csv` / `themes.md` (75 themes), `_verify\` (blocker verdicts: Confirmed / Downgrade), `stories\<KEY>\` (per-story review.md + findings.csv), `_reference\` (text extracts of every xlsx/docx, INDEX.md), `_bundles\` (per-story pointers into registers), `_scripts\REVIEWER_BRIEF.md` + `BRIEF_NONAPP_ADDENDUM.md` (the reviewer prompt).
- STAGE = `SET\_work\p1-ready\stage\` – next versions of changed files, at the SAME relative path they will have in SET (e.g. `STAGE\05 Technical architecture\Recovery Workbench Service Contract Catalog v3.md`).
- LOG = `SET\24 P1 Developer Readiness v1\` – the change-log folder (decision register, edit log, closed gaps/assumptions, affected stories, re-review results, delivery steps, recommendation).
- PACKETS = `SET\_work\p1-ready\packets\` – work packets the orchestrator gives you.
- EDITLOG = `SET\_work\p1-ready\editlog\` – each agent appends to its OWN file `<agent-name>.csv` (never another agent's file).

## Hard rules
1. Never edit an existing file in SET. Copy the highest version to STAGE as the next version number (`... v7.md` → `... v8.md`; folders such as `API Specification v6\` → `v7\`) and edit the copy. If the next version already exists in STAGE (another phase made it), edit that staged file only if your packet says you own that document; otherwise do not touch it.
2. Targeted edits only. Never regenerate a whole document to fix one thing. Keep every unchanged line byte-identical. Update the version/date line and the document's own change log or version table with one row naming "D-RCV-60 P1 developer readiness (RD-P1 register)".
3. One writer per document. Edit only the documents your packet names. If you need a change in a document you do not own, write it as a row in your edit log with `action=REQUEST` and the target document; the orchestrator routes it.
4. When an .md and .xlsx twin exist, make the same change in both (edit the xlsx cell-by-cell with openpyxl, preserving other cells, sheets and styles; never rebuild the workbook). Story files are .md only.
5. Copy IDs, numbers and dates character for character. Do not invent business rules, values, field names, message texts or IDs. A new ID must follow the document's existing scheme and the next free number (check the whole document first). If a value is genuinely missing from every source and no RD-P1 decision gives it, do not make it up: leave the story/document stating "Pending: <what>, owner <role>, tracked as GAP-nnnn" and register the gap.
6. Precedence: D-RCV-60 and Architecture v5 (SET\22 Microservice Realignment) > RD-P1 decisions (this run) > 16 Temporal and Drools Adoption (D-RCV-36) > 15 ACE DB Alignment (D-RCV-35, ADR-010) > 14 Story Updates > all other documents. ACE rule: only rwb-source-data reads `recovery.v_ace_*`; every other service reads ACE data only through the rwb-source-data contract.
7. No names of people; use roles. No git commands. No web. Sentence case in prose.
8. Context hygiene: never read a whole file larger than about 30 KB in one go; read in chunks of at most 250 lines; grep narrowly (`-n`, `-m 20`) and read matched line ranges. Large xlsx: use the text extracts in REVIEW\_reference for reading, openpyxl for writing.
9. Decision IDs are **RD-P1-nnn** (Readiness Decision for P1). `R-P1-nnn` is already used inside Assumptions Register v2 and must not be reused.

## Edit log format (EDITLOG\<agent-name>.csv, UTF-8, every field double-quoted)
`edit_id,action,file,old_version,new_version,section,before,after,finding_refs,decision_refs,gap_asm_refs,model,agent`
- action: EDIT / ADD / REMOVE / REQUEST / CLOSE-GAP / CLOSE-ASM / NEW-GAP / NEW-ASM
- before/after: the exact text (trim to 400 chars with "…" if longer); finding_refs = `<story_key>#<gap_no>` list; decision_refs = RD-P1-nnn list.
- edit_id = `<agent-name>-nnnn`.

## Decision register format (written by decision agents to LOG\decisions\)
Per decision: `RD-P1-nnn` · title · question · options considered · sources (document, version, section/sheet-row) · precedence applied · ruling (precise, buildable: names, values, codes, paths, owners) · rationale · affected services, stories (full keys) and documents · findings/themes settled (theme IDs and `story#gap` refs) · GAP/ASM rows closed or changed · status "Proposed – Claude Opus 5.5 (applied)" (or the model that made it) · reuse note (what a later service fix must take from this ruling).
