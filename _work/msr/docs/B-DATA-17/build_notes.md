# Build notes — B-DATA-17 Conceptual Data Model v7

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was produced

`06 Data/Recovery Workbench Conceptual Data Model v7.xlsx`, the next version of v6. v6 was read once, cell by cell, and never edited. It was copied with `compat/office_write.py copy` and only the copy was changed.

Sheets of v7, in order: `Read me` (new), `Subject areas`, `Data products`, `Entities`, `Relationships`, `Gaps`, `Key`, `Service ownership` (new).

## The change, sheet by sheet

| Sheet | Change | Rows |
|---|---|---|
| Read me | new first sheet; rows 1 and 2 are the two header lines of Template and Rules §R8.1, row 9 is the change-log row `v7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash` | 31 |
| Subject areas | one column appended, F `Owning services` (codes, `; ` separated); 10 of the 17 areas span more than one service | 17 + Total |
| Data products | one column appended, K `Owning service(s)`; the Entities column J and its `COUNTIF` formula are untouched | 14 + Total |
| Entities | three columns appended, H `Owning service`, I `Target schema`, J `Ownership basis`; columns A to G keep their letters, values and the field counts | 122 |
| Relationships | three columns appended, F `Owning service (entity)`, G `Owning service (refers to)`, H `Cross-service reference` | 104 |
| Gaps | unchanged, G1 to G14 and the 17 ACE rows, word for word | 43 |
| Key | five `Term` rows appended at rows 22 to 26: Owning service, Target schema, PLT, Cross-service reference, Service contract | 16 + 5 |
| Service ownership | new sheet; 19 service rows, a PLT row and a Total row, with schema, entity count, table and view split and a note where the owner is unusual | 21 |

Nothing else moved: `verify_v7.py` compares all six v6 sheets with v7 cell by cell and reports 0 differences outside the appended cells, 0 lost rows and 0 lost columns.

## Where the owners come from

The owner of every entity is the Ownership Map v1 sheet `Tables`, row by row, keyed on the table name. 91 of the 92 Workbench entities resolve this way:

- 85 by the table name built from the entity name,
- 4 extension tables (party_ext, contact_point_ext, account_ext, valuation_ext) by name in the same sheet,
- `List value` to `lov_value` (P3) and `Rule` to `rule_row` (P7) by name; the LDM v8 dictionary states that `rule_row` is the entity "Rule" and its 18 fields match.

The remaining entity is `Payment match rule`. It has no row in the map because D-RCV-36 T10 dropped the table and moved payment matching into the PAYMENT_MATCH rule package; the owner is P7 and the basis says so (CG-B-DATA-17-2, ASM-B-DATA-17-2).

The 30 `v_ace_*` views are not in the map at all. Architecture v5 slides 15 and 41 and the SQL view standard say only rwb-source-data reads them and it owns the view contract, so their owner is P1 and their target schema is the read-only `recovery` schema, not `rwb_source_data` (CG-B-DATA-17-1, ASM-B-DATA-17-1).

Owned per service: P1 48 (30 views and 18 tables), P3 15, P5 12, P10 8, PLT 6, P4 5, P7 5, P2 3, P6 3, P9 3, S9 3, S4 2, S5 2, S6 2, S2 1, S3 1, S7 1, S8 1, S1 0. Total 122.

## The relationships

104 rows, resolved against the 122 entities with no unmatched name:

- 45 stay inside one schema;
- 11 point at an ACE view, which v6 already calls a business key with no foreign key;
- 48 are a Workbench table in one service pointing at a Workbench table in another, so the foreign key is cut and the column keeps the business key only (DP-01; CG-B-DATA-17-5, ASM-B-DATA-17-5).

## Dates

The workbook carries no release date, so no date is marked "(tentative)" and no date is changed. The one date in the source, the 21 November date in the Gaps note on DL43, is a decision date and is copied character for character.

## Rows

- 8 candidate gap rows, `CG-B-DATA-17-1` to `CG-B-DATA-17-8`, with every key of Template and Rules §R9. Severity: 2 at P2 (CG-B-DATA-17-3, CG-B-DATA-17-5) and 6 at P3. Types: 4 Missing, 2 Ambiguous, 1 Conflict, 1 Outdated.
- 8 candidate assumption rows, `ASM-B-DATA-17-1` to `ASM-B-DATA-17-8`, one per gap, each with `gap` pointing at its CG row. Confidence: 5 High, 3 Medium.
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1.

## Checks

`verify_v7.py` asserts: same sheet order; every v6 cell unchanged; no new cell outside the appended columns and Key rows; 122 entity rows all carrying an owner and a schema; 30 rows marked as read-only ACE views; every other schema matching `rwb_<name>` or the platform-library wording; the `COUNTIF` formulas of the Data products sheet intact; 104 complete relationship rows; the two header lines and the change-log row present; no e-mail address, no issue-tracker reference, no old API base. Result: 0 problems.
