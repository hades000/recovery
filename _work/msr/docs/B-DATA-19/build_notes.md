# Build notes B-DATA-19 — Reference Data and Lists of Values v5

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What this version is

`06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx` is the next version of
`v4.xlsx`, produced by copying the source with `compat/office_write.py copy` and changing only the copy.
The source was read once and never edited.

The two changes the WP asks for are:

1. **Refdata starter** — a new sheet `Reference data starter`, 179 rows, the lists and reference tables
   each service loads or reads at its first deployment, with the mode (Load or Read), the route, the
   service wave and the basis.
2. **Shared lists via rwb-case** — every list is held once, in the service the Ownership Map gives its
   table, and read by the others through that holder's contract. Four columns are appended to `Lists`
   (G to J) and four to `Reference tables` (F to I); `Change process` gains step 9 and `Key` gains four
   rows.

## Derivation rule (applied by `derive.py`, written out in the workbook)

`Ownership Map v1` sheets `Services` (code, name, wave, schema) and `Tables` (93 rows) are the only
owner sources.

- **Owning service of a list.** A closed list is held in `lov_value`, a P3 table of `rwb_case`, so P3
  holds all 124 closed lists. A source list is held where its `Source` cell points: `v_ace_*` means ACE
  data read through P1 (7 lists); `document_type` and `retention_rule` mean P5 (2); `role` means P4 (1);
  `rule_row` means P7 (1); `lov_value`, `parameter_catalog` and `queue` mean P3 (3).
  Total: P3 126, P1 7, P5 2, P7 2, P4 1 = 138.
- **Shared-list route.** Closed lists: `rwb-case list read, RWB-P3-E1043-CON (DP-07)`. ACE source lists:
  `ACE read through the P1 contract, not loaded (DP-05)`. Held source lists: the holder's contract that
  serves the named table (`rwb-document contract` P5, `rwb-access contract RWB-P4-E1037-CON` P4,
  `rwb-decision rule packages RWB-P7-E1073-CON` P7, `rwb-case parameters contract RWB-P3-E1042-CON` for
  `parameter_catalog`, the rwb-case queue resource for `queue`, and the rwb-case list read for `lov_value`).
- **Starter row.** One per (service, item) where the service owns a table whose column the list's
  `Used by` cell names, or the ACE view it names (P1), or owns a reference table of the
  `Reference tables` sheet. 11 closed lists have no live field after D-RCV-35 and give no row;
  S1 rwb-valuation owns no table in the map and no list names `write_off`, so S1 and S7 give no row
  (CG-B-DATA-19-3).
- **LOV-MATCH-TYPE.** Its `Used by` cell names `payment_match_rule`, which has no Ownership Map row and
  which ADR-012 drops. The row is held by P7 as a `PAYMENT_MATCH` package column and read by P8
  (CG-B-DATA-19-2; ASM-B-DATA-19-2).

## Counts

| Item | Count |
|---|---|
| Lists rows | 138 (124 closed, 14 source) |
| Lists appended cells | 552 (4 columns x 138 rows) |
| Owning service | P3 126, P1 7, P5 2, P7 2, P4 1 |
| Shared-list route | rwb-case list read 124, rwb-case parameters contract 1, rwb-case queue resource 1, ACE read through P1 7, rwb-decision 2, rwb-document 2, rwb-access 1 |
| Values rows | 598, no cell changed |
| Reference tables rows | 14, 56 appended cells |
| Reference data starter rows | 179 (171 Load, 8 Read) over 18 codes |
| Starter by wave | 0: 3, 1: 147, 2: 13, 3: 10, 4: 6 |
| Change process | 8 rows plus step 9 |
| Key | 12 rows plus 4 |
| Read me | 31 lines |

## Verification (`verify_v5.py`)

- `Lists`, `Values`, `Reference tables`, `Change process`, `Key`: every v4 cell compared with v5, value,
  number format, font and fill. 0 differences.
- Shapes: `Lists` 142 x 10, `Reference tables` 18 x 9, starter 179 data rows, `Change process` 13,
  `Key` 16.
- Auto-filters extended to the new columns (`A4:J142`, `A4:I18`); starter filter `A6:H185`, freeze `A7`.
- Read me line 1 and 2 are the Template and Rules §R8.1 header; the change-log row is
  `v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
- Document properties: creator set to a team string (the v4 creator was a person name), lastModifiedBy
  to the tool line, title to the v5 title.
- No cell anywhere carries an issue-tracker word, an e-mail address or a person name.

## Files in this scratch folder

`derive.py` (derivation), `derive.json` (derived rows), `build_v5.py` (workbook builder),
`verify_v5.py` (v4 to v5 comparison), `verify_v5.json` (result), `probe_lists.py` (first parse probe),
`tables_owner.json` (map dump).
