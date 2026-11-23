# Build note B-DATA-24 — Data Classification and Personal Data Inventory v5

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## Source and output

- Source, read only: `06 Data/Recovery Workbench Data Classification and Personal Data Inventory v4.xlsx`,
  six sheets `Fields` (1,370 rows by 10 columns, 1,366 field rows from row 5), `Summary`, `Identifiers`,
  `Handling`, `Who sees what`, `Key`. One conversion to text, no edit.
- Output: `06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx`, a copy of v4
  with the changes below. Sheet order: `Read me`, `Fields`, `Summary`, `Identifiers`, `Handling`,
  `Who sees what`, `Key`, `PII controls`.
- Scripts in this folder: `dump_v4.py` (cell dump), `build_v5.py` (the build), `verify_v5.py` (the check),
  `write_rows.py` (the register rows).

## What the realignment needs

The WP names three things: no personal data in events, workflow inputs or logs; every owner from the
Ownership Map; new decisions under the ids in `_work/msr/plan/ids.json` (here D-RCV-60 and the architecture
decisions it points at). Everything else in the source is kept, cell for cell.

Architecture v5 (Text Extract v1) is the basis: events carry IDs and business facts only (lines 833, 1618 and
2936); workflow inputs and history carry IDs, payloads are encrypted by the codec and the search attributes are
CaseId, Stage, ProductGroup and QueueCode only (lines 2533, 2562 and 3064; Temporal and Drools Design Text
Extract v1 lines 522 and 1885); audit and personal-data access logs go through the ACE Common PII logging path
to the SOC (lines 511, 1503, 2179 to 2183 and 2537); only rwb-source-data reads the 30 views (lines 707, 850
and 909); one login and one schema per service (lines 2051, 2126, 2143 and 2147); the masking policy is P4
rwb-access data (lines 1020, 2562 and 2882).

## Changes, sheet by sheet

### Fields

Three columns appended after the source's column J, on all 1,366 rows. Columns A to J keep their letters,
positions, values and styles.

- `K Owner (D-RCV-60)`: `<code> <service> (<schema>)` from the Ownership Map v1 sheet `Tables`, row by row.
  The 30 `recovery.v_ace_*` views are not table rows, so they read `P1 rwb-source-data (recovery view)` under
  the ACE view contract (CG-B-DATA-24-1; ASM-B-DATA-24-1). `lake_copy_watermark` reads
  `P1 rwb-source-data (retired table)` (CG-B-DATA-24-3; ASM-B-DATA-24-3) and `payment_match_rule` reads
  `P3 rwb-case (retired table)` (CG-B-DATA-24-2; ASM-B-DATA-24-2).
- `L Events and workflow inputs (D-RCV-60)` and `M Logs (D-RCV-60)`: one rule per category, because every row
  is one of six category / classification / personal triples (12 + 5 + 91 + 364 + 51 + 843 = 1,366, checked in
  the build). A direct identifier and a sensitive field never travel; an indirect identifier travels as a
  reference only; customer data travels as a business fact only; a staff identifier as a user id only; not
  personal data as a fact or a code.
- Six fields carry a rule of their own because their content can hold personal data while their category does
  not say so: `outbox_event.payload`, `agent_prompt.body_text`, `agent_run.output`,
  `document_text.text_content`, `document_intake.file_name`, `document_intake.sender_address`
  (CG-B-DATA-24-4; ASM-B-DATA-24-4).
- The auto-filter extends from `A4:J1370` to `A4:M1370`. No v4 cell in the sheet changes.

### Summary

The category block in A1:C11 is untouched, formulas included. A new block from row 13 counts the 1,366 fields
and the 523 personal fields by owner: 19 service groups, one row for the 304 view fields and one row for each
retired entity, with a Total row of 1,366 and 523. Every number is static, computed in the build and checked
against the map in `verify_v5.py`.

### Identifiers

Two columns appended on the 108 rows: `H Owner (D-RCV-60)` as in Fields, and
`I Events, workflow inputs and logs (D-RCV-60)` with the same category rule in one cell. Auto-filter extends to
`A4:I112`. The seven source columns are unchanged.

### Handling

Four cells change, all because the single identity and the unnamed PII path are gone:

| Cell | Row | v5 |
|---|---|---|
| C5 | Restricted, Stored | Encrypted at rest in the owning service's `rwb_*` schema |
| C7 | Restricted, In logs | Read by rwb-source-data and logged through the ACE Common PII logging path; business topics separate |
| C21 | Restricted, Contact values | The P4 rwb-access masking policy applied by rwb-source-data at the API |
| C22 | Restricted, Every ACE read | The `rwb_source_data` login holds SELECT on the 30 views only; no other login has a grant |

(CG-B-DATA-24-5; ASM-B-DATA-24-5; CG-B-DATA-24-6; ASM-B-DATA-24-6.)

Column D `Owner (D-RCV-60)` is appended on all 24 rows, and six rows are added for the channels the source did
not cover: Restricted in events and workflow inputs, Confidential in events and workflow inputs, Internal in
logs, All in events, All in workflow history, All in PII logging (CG-B-DATA-24-8; ASM-B-DATA-24-8). The other
14 source rows keep their wording.

### Who sees what

Column E `Enforced by (D-RCV-60)` is appended on the 14 role rows: P4 masking policy, the owning service, P10
rwb-agent or the P1 login, row by row. The four source columns are unchanged, including the note that the rule
content waits on DL26 (CG-B-DATA-24-7; ASM-B-DATA-24-7).

### Key

Five rows appended: Rule / Event payload, Rule / Workflow input and history, Rule / Logs, Class / PII logging,
Category / Masking policy. The 11 source rows are unchanged.

### PII controls (new last sheet)

Three blocks. (1) `Where personal data may travel`: nine channels (REST through gateway-bff, the service
topics, `rwb.decision-record.v1`, Temporal input and history, logs and traces, agent prompt and answer,
document storage, partner files, the database), each with what it carries, what it never may, its owner and
its control. (2) `Field count by category and channel rule`: the six categories with the rule and the counts.
(3) `Changed or retired in v5`: eight rows with the v4 state, the v5 state and the source that decides it,
including the interaction ledger (CG-B-DATA-24-9; ASM-B-DATA-24-9).

## What did not change

Every field ID, entity name, field name, category, classification, personal flag, on-screen rule, lawful
basis, retention value and meaning; the 108 identifier rows; the 14 role rows; the 11 key rows; the 22
handling rows except the four cells above; the 11-row category block and its COUNTIF formulas. 122 entities
and 1,366 fields, as in the source.

The source holds no version number in its cells, no release date and no date cell at all, so nothing is marked
"(tentative)" and no date is changed or raised.

## Workbook properties

`dc:title` is set to the v5 file name; `creator` is set to `Recovery Workbench programme` and
`lastModifiedBy` to `T3 Code / OpenCode / DeepSeek v4.1 Flash`, because the source copy carried a person's name
in both. No content cell is touched for this.

## Verification

`verify_v5.py` compares every v4 cell with v5, value and style: exactly four changes, the four declared
Handling cells; 0 problems. It also checks that no sheet shrank, the sheet order, both header lines, the
change-log row, that every appended cell is filled, that every owner cell equals the Ownership Map row, the
523 personal fields, the Summary total, the untouched COUNTIF, the 24 handling owners, the 14 enforcement
cells, the five key rows, the PII controls totals and the three properties.
