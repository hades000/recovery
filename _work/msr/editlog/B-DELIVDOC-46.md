# Edit log B-DELIVDOC-46

Work package: WP B-DELIVDOC-46, Recovery Workbench Cutover and Go Live Plan next version.
Decision: D-RCV-60. Agent: aisdlc-msr-worker. Fanout: 0, so no subagent was started.
Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v4.docx` - the next version of the cutover and go-live plan, written from the text file below
- `_work/msr/docs/B-DELIVDOC-46/Recovery Workbench Cutover and Go Live Plan v4.md` - the full text of version 4, the source for the docx
- `_work/msr/docs/B-DELIVDOC-46/template-fixed.docx` - a copy of the version 3 file with the heading style names lowercased and a List Bullet style added, because compat/office_write.py md-docx raises KeyError on Heading 1 in this family; the source file is unchanged
- `_work/msr/docs/B-DELIVDOC-46/_fix_template.py` - the script that makes template-fixed.docx
- `_work/msr/docs/B-DELIVDOC-46/_set_props.py` - the script that replaces the person name and the version in the core properties of the new docx only
- `_work/msr/docs/B-DELIVDOC-46/verify/Recovery Workbench Cutover and Go Live Plan v4.md` - the converted text of the new docx, read back to confirm every section, table and citation
- `_work/msr/docs/B-DELIVDOC-46/_peek.py` - scratch script that reads split_plan.json stats and legacy
- `_work/msr/docs/B-DELIVDOC-46/_peek2.py` - scratch script that reads ownership.json
- `_work/msr/docs/B-DELIVDOC-46/_peek3.py` - scratch script that lists the Ownership Map v1 sheets
- `_work/msr/docs/B-DELIVDOC-46/_peek4.py` - scratch script that prints the Services sheet and the Read me sheet
- `_work/msr/docs/B-DELIVDOC-46/_styles.py` - scratch script that lists the heading and list styles of the version 3 file
- `_work/msr/docs/B-DELIVDOC-46/_props.py` - scratch script that reads the core properties of the source and the new file
- `_work/msr/docs/B-DELIVDOC-46/_check.py` - scratch script that checks the jsonl rows, the citations and the header lines
- `_work/msr/gaps/B-DELIVDOC-46.jsonl` - 11 gap rows, GAP-0299 to GAP-0291
- `_work/msr/assumptions/B-DELIVDOC-46.jsonl` - 11 assumption rows, ASM-0390 to ASM-0400

No file that already existed was edited; the version 3 source and both masters are unchanged.

## What changed in version 4

Sections 1 to 9 of version 3 are kept, with every ID, number, date, team code and figure: 30 November 2026, 26 November 2026, 21 November, the 30 SELECT-only views, the 16 Section A and 14 Section B views, the 80 appendix fields, the 14 tables and 12 columns of RWB-ACE-001, the 21 ACE tables, the 20 trackers with 14 LOAD and 6 RETIRE, the six teams, DL12, DL34, DL39, DL43, D-RCV-35, ADR-010, JOB-02, RWB-E1-005, RWB-E1-010, RWB-E1-012 and G6. The only change the realignment needs is the cutover per wave, in new sections 10 to 12 and in the marked rows: the wave roster and cutover order from Architecture v5 slide 38 and the Ownership Map v1 Services sheet, the per-service gates, the per-service rollback with Worker Versioning and the one-call rule rollback, the view grant moved to the rwb_source_data login, and the BOT approval as a Wave 1 gate. Every release date is marked (tentative).

Gap rows: 11. Assumption rows: 11. Highest severity: P1, GAP-0304 (BOT approval not in the source plan). New decision IDs used: none beyond D-RCV-60; the document cites the existing DL12, DL34, DL39 and DL43 and raises no new DL or ADR ID.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DELIVDOC-46 --quick` at the end of the work package: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS, no findings. Checked by hand as well: the two header lines of Template and Rules R8.1 are the first two paragraphs of the docx, the 22 citations in the text each resolve to a jsonl row, every jsonl row is cited, and no person name is left in the document properties.

## Failures

None.
