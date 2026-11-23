# Edit log B-DATA-24 — Recovery Workbench Data Classification and Personal Data Inventory next version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source was converted once to text under the run scratch area with `compat/convert_sources.py`, read sheet
  by sheet, and never edited. It was then copied to v5 with `compat/office_write.py copy`, and only the copy was
  changed: `06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx`.
- `Read me` is a new first sheet. Rows 1 and 2 are the two header lines of Template and Rules §R8.1. Row 9 is
  the change-log row `v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek
  v4.1 Flash`. Rows 12 to 22 list the eleven changes, rows 25 and 26 what did not change, rows 29 and 30 the
  counts, and row 33 the open register rows.
- `Fields`: three columns are appended after the source's column J, on all 1,366 rows. `Owner (D-RCV-60)` gives
  the owning service and schema from the Ownership Map v1 sheet `Tables`, row by row;
  `Events and workflow inputs (D-RCV-60)` and `Logs (D-RCV-60)` give the rule for those two channels. Columns A
  to J keep their letters, positions, values and styles, and no v4 cell in the sheet changes. The auto-filter
  extends to `A4:M1370`.
- The owner of every entity comes from the map, per the WP instruction "Use the Ownership Map for every owner":
  91 of the 92 non-view entities are rows of the map's 93, the four extension tables are at P1, and the 30
  `recovery.v_ace_*` views read `P1 rwb-source-data (recovery view)` because the map lists tables and not views
  (GAP-0259; ASM-0349). `payment_match_rule` is the one entity with no map row, and it reads
  `P3 rwb-case (retired table)` (GAP-0260; ASM-0350). `lake_copy_watermark` reads
  `P1 rwb-source-data (retired table)` (GAP-0261; ASM-0351). The map's two rule_package tables are
  not entities of this inventory.
- The per-field rule follows the category, because every row is one of six category / classification / personal
  triples: 12 Direct identifier and 5 Sensitive at Restricted, 91 Indirect identifier and 364 Customer data at
  Confidential, 51 Staff identifier and 843 Not personal at Internal. A direct identifier and a sensitive field
  never travel; an indirect identifier travels as a reference only; customer data as a business fact only; a
  staff identifier as a user id only. Six fields carry a rule of their own because their content can hold
  personal data while their category does not say so: `outbox_event.payload`, `agent_prompt.body_text`,
  `agent_run.output`, `document_text.text_content`, `document_intake.file_name` and
  `document_intake.sender_address` (GAP-0262; ASM-0352).
- `Identifiers`: two columns are appended on the 108 rows, `Owner (D-RCV-60)` and
  `Events, workflow inputs and logs (D-RCV-60)`; the auto-filter extends to `A4:I112`. The seven source columns
  are unchanged.
- `Summary`: the 11-row category block and its COUNTIF formulas are untouched. A new block from row 13 counts
  the 1,366 fields and the 523 personal fields by owner: 19 service groups, one row for the 304 view fields, one
  row for each retired entity, and a Total row of 1,366 and 523.
- `Handling`: four cells change and no other source cell does. C5 (Restricted, Stored) names the owning
  service's `rwb_*` schema. C7 (Restricted, In logs) names the ACE Common PII logging path and states that the
  business topics are separate. C21 (Restricted, Contact values) names the P4 rwb-access masking policy. C22
  (Restricted, Every ACE read) gives SELECT on the 30 views to the `rwb_source_data` login alone
  (GAP-0263; ASM-0353; GAP-0264; ASM-0354). Column D `Owner (D-RCV-60)` is appended
  on all 24 rows and six rows are added for the channels the source did not cover
  (GAP-0266; ASM-0356); the other 14 rows keep their wording.
- `Who sees what`: one column is appended, `Enforced by (D-RCV-60)`, naming the P4 masking policy, the owning
  service, P10 rwb-agent or the P1 login on each of the 14 role rows (GAP-0265; ASM-0355). The
  four source columns are unchanged, including the note that the rule content waits on DL26.
- `Key`: five rows are appended for the event payload, the workflow input and history, logs, PII logging and
  the masking policy. The 11 source rows are unchanged.
- `PII controls` is a new last sheet: nine channels with what each may carry, what it never may, its owner and
  its control; the field count by category with the rule; and eight items this version changed or retired,
  including the interaction ledger at P1 (GAP-0267; ASM-0357).
- Nothing else moved. `verify_v5.py` compares every v4 cell with v5, value and style: exactly four changes, the
  four declared Handling cells, 0 problems; no sheet shrank, no sheet was renamed and the sheet order is
  `Read me`, the six source sheets, `PII controls`.
- The source holds no version number in its cells, no release date and no date cell at all (0 date cells), so
  no release date is marked "(tentative)" and no date is changed. No date is raised as a gap.
- The document properties of the copy carried a person's name in `creator` and `lastModifiedBy`. They are set
  to `Recovery Workbench programme` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, and `dc:title` to the v5
  file name, so no person name survives in the workbook (root rule 4). No content cell was touched for this.
- No person name, no e-mail address and no issue-tracker reference was written. No repository, wiki or web call
  was made; no commit was created.

## Files written

- `06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx`
- `_work/msr/gaps/B-DATA-24.jsonl`
- `_work/msr/assumptions/B-DATA-24.jsonl`
- `_work/msr/editlog/B-DATA-24.md`
- `_work/msr/docs/B-DATA-24/build_notes.md`
- `_work/msr/docs/B-DATA-24/build_v5.py`
- `_work/msr/docs/B-DATA-24/verify_v5.py`
- `_work/msr/docs/B-DATA-24/write_rows.py`
- `_work/msr/docs/B-DATA-24/dump_v4.py`
- `_work/msr/docs/B-DATA-24/v4_dump.json`
- `_work/msr/docs/B-DATA-24/verify_v5.json`

The converted source text is `_work/msr/extract/B-DATA-24/Recovery Workbench Data Classification and Personal
Data Inventory v4.md`, produced by the converter and read only.

## Rows

- Candidate gap rows: 9, `GAP-0259` to `GAP-0267`, in the gaps file, with every key of Template and
  Rules §R9. Types: 3 Missing (GAP-0259, -7, -8), 3 Outdated (-2, -3, -5), 2 Conflict (-4, -9) and 1
  Ambiguous (-6). Severity: 5 at P2 (-1, -2, -4, -5, -8) and 4 at P3 (-3, -6, -7, -9). All carry
  `needed_by_wave` 1 except -2 at wave 2. The legacy keys they reference are RWB-E1-069, RWB-E2-027, RWB-E1-014,
  RWB-E1-037, RWB-AD-004, RWB-E1-066 and RWB-E1-068; -8 is new under D-RCV-60.
- Candidate assumption rows: 9, `ASM-0349` to `ASM-0357`, in the assumptions file, one per gap,
  each with `gap` pointing at its CG row. Confidence High on 4 (-1, -2, -5, -8) and Medium on 5 (-3, -4, -6,
  -7, -9).
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1, as root rule 7 and Template and Rules §R9 require.

## Counts

- Fields: 1,366 rows over 122 entities; 523 personal and 843 not personal; 3 appended columns, 3 headers and
  4,098 values. Owners: 19 service codes plus the 304 view fields and the 19 retired fields; P1 207, P3 174,
  P5 152, P10 111, P7 75, PLT 46, P4 43, P6 37, P2 32, P9 28, S9 22, S2 21, S4 20, S5 19, S6 18, S7 11, S8 10,
  P8 9, S3 8.
- Identifiers: 108 rows, 2 appended columns, 2 headers and 216 values.
- Summary: 1 new block of 23 rows (header, 19 service rows, 1 view row, 2 retired rows, 1 Total).
- Handling: 4 changed cells, 1 appended column (18 + 6 values), 6 appended rows, 24 rows in all.
- Who sees what: 1 appended column, 14 values. Key: 5 appended rows, 21 rows in all. PII controls: 9 channel
  rows, 6 category rows and a total, 8 changed or retired rows.
- Gaps: 9 rows; assumptions: 9 rows.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-24 --quick`: C02, C03, C05, C12, C13
  and C18 PASS, 0 findings.
- `verify_v5.py`: 4 changed v4 cells, all declared; 0 problems; every owner cell equal to the Ownership Map;
  523 personal fields; the v4 COUNTIF formulas intact.
- C17 by hand over the same write set: every candidate gap and assumption row cited in `build_notes.md`, in
  this log and in the Read me sheet has a row in its register file, and no other candidate id is cited.
- C20 by hand: the tool line is present and no other tool is named as the author.

## Failures

None.
