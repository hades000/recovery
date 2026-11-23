SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Build note B-DATA-18 - Recovery Workbench Source to Target Mapping v5

Decision D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Source and output

- Source (read only, never edited): `06 Data/Recovery Workbench Source to Target Mapping v4.xlsx`, 4 sheets.
- Output: `06 Data/Recovery Workbench Source to Target Mapping v5.xlsx`, 5 sheets (Read me added first).
- The copy was made with `compat/office_write.py copy`; only the copy was changed.

## What the realignment changed

1. `Mapping`: two columns appended at the end, `Target schema` (rwb_<name>) and `Owning service` (P1 to S7), one value per row from the Ownership Map sheet Tables. Columns A to N are untouched.
2. `ACE gaps`: the same two columns appended at the end. All 80 rows read through rwb-source-data, so the target schema is rwb_source_data and the owner is P1 (ADR-010, DP-05).
3. `By source`: one cell changed, the ACE table(s) cell of the Aric via COLLINS row, from `recovery` to `rwb_source_data.party_ext`; counts and the Total row are unchanged.
4. `Mapping rules`: eight rules appended after the ten v4 rules, which are unchanged word for word.
5. `Read me`: new first sheet with the Template and Rules section R8.1 header lines and the change-log row `v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.

## Every section, ID, number and date is kept

- The source carries no date anywhere in the four sheets, so no release date is marked (tentative) and none is changed.
- All 133 Field IDs, the 80 ACE gap row Field IDs, the 17 source-system names and the Total row are copied unchanged.
- `verify_v5.py` compares every v4 cell with v5: exactly one v4 cell differs, the Aric via COLLINS ACE table(s) cell named in CG-B-DATA-18-3.

## Target schema and owner per entity

| Workbench entity | Fields | Target schema | Owner | Basis |
|---|---|---|---|---|
| loan_account | 22 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| asset | 10 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| collateral | 10 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| legal_action | 9 | rwb_litigation | S4 | Ownership Map sheet Tables |
| party | 9 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| collections_history | 8 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| asset_sale | 7 | rwb_asset | S5 | Ownership Map sheet Tables |
| recovery_case | 6 | rwb_case | P3 | Ownership Map sheet Tables |
| score | 6 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| treatment | 6 | rwb_treatment | S2 | Ownership Map sheet Tables |
| account_payment | 5 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| notice | 5 | rwb_comms | P6 | Ownership Map sheet Tables |
| valuation | 5 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| write_off | 5 | rwb_writeoff | S7 | Ownership Map sheet Tables |
| party_product | 4 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| hearing | 3 | rwb_litigation | S4 | Ownership Map sheet Tables |
| proceeds | 3 | rwb_payment | P8 | Ownership Map sheet Tables |
| dp_treatment | 2 | rwb_source_data | P1 | Ownership Map sheet Tables |
| interaction | 2 | rwb_source_data | P1 | Ownership Map sheet Tables |
| account_collateral | 1 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| contact_point | 1 | rwb_source_data | P1 | ACE entity read through rwb-source-data (ADR-010) |
| debt_sale_account | 1 | rwb_debtsale | S6 | Ownership Map sheet Tables |
| decision_log_entry | 1 | rwb_decision | P7 | Ownership Map sheet Tables |
| role | 1 | rwb_access | P4 | Ownership Map sheet Tables |
| signature_request | 1 | rwb_document | P5 | Ownership Map sheet Tables |

Total: 133 field rows over 25 entities; 81 rows are ACE-side entities that read through rwb_source_data, and 4 further rows (interaction, dp_treatment) are P1 Workbench tables, so rwb_source_data holds 85 rows in all.

## Counts

- Mapping: 133 field rows, 25 entities, 17 source systems, target schemas rwb_source_data (85), rwb_litigation (12), rwb_asset (7), rwb_case (6), rwb_treatment (6), rwb_comms (5), rwb_writeoff (5), rwb_payment (3), rwb_access (1), rwb_debtsale (1), rwb_decision (1), rwb_document (1).
- ACE gaps: 80 rows. All read through rwb-source-data.
- By source: 17 source rows plus the Total row; 133 fields, 52 ACE reuse, 80 ACE new, 1 extension.
- Mapping rules: 10 v4 rules plus 8 new rules.

## Register rows raised by this WP

| Row | Type or confidence | Subject |
|---|---|---|
| CG-B-DATA-18-1 | Ambiguous, P2 | eleven ACE entities named as Workbench entities (ASM-B-DATA-18-1) |
| CG-B-DATA-18-2 | Missing, P2 | no owner and no target schema in v4 (ASM-B-DATA-18-2) |
| CG-B-DATA-18-3 | Outdated, P3 | extension field counted against ACE table 'recovery' (ASM-B-DATA-18-3) |
| CG-B-DATA-18-4 | Outdated, P3 | five rows cite Interface Specifications v3 (ASM-B-DATA-18-4) |
| CG-B-DATA-18-5 | Ambiguous, P3 | 80 Status cells carry the legacy key RWB-ACE-001 (ASM-B-DATA-18-5) |
| CG-B-DATA-18-6 | Missing, P3 | three extension tables absent from the mapping (ASM-B-DATA-18-6) |
| CG-B-DATA-18-7 | Missing, P3 | 81 field rows without a data product (ASM-B-DATA-18-7) |

Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules section R9 require.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-18 --quick` - C02, C03, C05, C12, C13 and C18.

## Scratch files

- `dump_v4.py`, `v4_dump.json`: the v4 workbook read out cell by cell.
- `build_v5.py`: the v5 builder.
- `verify_v5.py`: the v4-to-v5 cell comparison.
- `gen_notes.py`: this note.
- `probe_entities.py`, `probe2.py`, `probe3.py`, `probe4.py`, `probe_ownmap.py`, `probe_svc.py`, `probe_props.py`: source probes.
- `check_cites.py`, `show_v5.py`, `show_v5b.py`: citation check and read-back of the finished workbook.
