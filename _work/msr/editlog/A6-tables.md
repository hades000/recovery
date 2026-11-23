# A6-tables — Ownership Map part: tables

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Agent: aisdlc-msr-worker
Date: 22 November 2026
WP: A6-tables (fanout: 0; no subagents used)

## Files written

The WP names its "Write only" files on one semicolon-separated line; they are tabled here, and no other file was written.

| # | File | Purpose |
|---|---|---|
| 1 | `_work/msr/plan/ownership_part_tables.json` | Owner, basis, ruling and assumption for each of the 93 tables |
| 2 | `_work/msr/gaps/A6-tables.jsonl` | 15 candidate Conflict gap rows (CG-A6-tables-1 to 15) |
| 3 | `_work/msr/assumptions/A6-tables.jsonl` | 15 candidate assumption rows (ASM-A6-tables-1 to 15) |
| 4 | `_work/msr/editlog/A6-tables.md` | This edit log |

## What was done

1. Read the `tables` section of `_work/msr/plan/ownership_skeleton.json`: 93 items, every `CREATE TABLE` in the Physical Schema v6 file named in `schema_file`.
2. Read the R-PREC order and the five default rulings in Appendix R §R3 of the implementation plan, the Template and Rules v1 (R3, R5.4–R5.5), the Architecture v5 text extract (contract slides 14–20 win over the narrative; catalogue slides 41–44), the Temporal and Drools design extract, and the extract set: FSD v6 and TSD v5 module files, Event and Messaging v4, Batch and Scheduling v4, Physical Schema v6, LDM v8.
3. Applied R-PREC in order for each table: Arch v5 catalogue first (slide 41 "Owns" column and the per-service DB lines on slides 14–20), then the Temporal and Drools design (rule registry governance), then the narrative slides, then the plan's default rulings, then TSD v5, then FSD v6, then the schema and LDM. The legacy `hint` counts were read only as a cross-check and never used to decide an owner.
4. Wrote one row per table with `id`, `owner`, `basis`, `ruling`, `asm`. Owner codes used: P1–P10, S2–S9 and PLT. No skeleton table maps to S1: the only valuation table in the schema, `valuation_ext`, is one of P1's four extension tables in FSD P1 v3 and TSD P1 v3, so S1's `rwb_valuation` tables are new work outside this map. S1 is therefore absent from the table owners without loss of a skeleton item.
5. Recorded 15 rulings where two sources name different owners. Each ruling has a Conflict gap row (severity P2) and an assumption row; 24 table rows cite one of the 15 assumptions, because the rule-registry, ledger, outbox, feature-flag and DP04 rulings each cover more than one table.

## Counts

- 93 of 93 skeleton tables, each exactly once.
- Owners: P1 18, P2 3, P3 15, P4 5, P5 12, P6 3, P7 6, P8 1, P9 3, P10 8, PLT 6, S2 1, S3 1, S4 2, S5 2, S6 2, S7 1, S8 1, S9 3.
- 24 rows carry a ruling; 69 rows cite the catalogue or a single lower source with no conflict.
- 15 gap rows (CG-A6-tables-1 to 15) and 15 assumption rows (ASM-A6-tables-1 to 15), one pair per ruling.

## Rulings in brief

| # | Tables | Decision |
|---|---|---|
| 1 | interaction, efs_ledger_outcome | P1 keeps the ledger and the EFS intake rule (default ruling, DP-18); P3 keeps the timeline API. |
| 2 | case_list_row | P1 builds the daily row projection; the case list API and screen stay P3. |
| 3 | rule_package, rule_package_version, rule_row, rule_test_case | P7 owns the registry, rows and test cases; services evaluate a local copy only. |
| 4 | delegation_limit | P4 owns the DoA table; P3 keeps only non-DoA reference data. |
| 5 | lov_value | P3 as reference data. |
| 6 | partner_user | S9 as partner users. |
| 7 | feature_flag, feature_flag_change | PLT library; P2 serves the admin API. |
| 8 | outbox_event, outbox_delivery, processed_event, idempotency_key | PLT library objects, one copy per service schema. |
| 9 | job_catalog | P2 keeps the register; Schedules live with each service. |
| 10 | retention_rule | P5, with JOB-17; P1 drops its copy. |
| 11 | signature_request | P5; P6 requests through P5's contract. |
| 12 | timer | P3 projection; the clock is a durable Temporal timer. |
| 13 | lake_copy_watermark | P1 legacy table, no target; data lake removed. |
| 14 | dp_treatment, dp_guarantee_claim | P1 keeps the dated DP04 copies; S2 and S3 keep the live records. |
| 15 | valuation_ext | P1 as an extension table; FSD P1 open question OQ-P1-05 stays open. |

## Verification

- Self-check in the generator: 93 rows, unique ids equal to the skeleton set, every owner in the 20 allowed codes, every ruling has an `asm`, every `asm` exists in the assumption rows, gap and assumption ids pair 1:1.
- Quick checks run: `python -I "22 Microservice Realignment/checks/run_all.py" --wp A6-tables --quick`. Results are in the report the script writes under `22 Microservice Realignment/checks/reports/`; the findings, if any, are listed in the run log below.
- No person names, no email addresses, no issue-tracker references. No file outside "Write only" was written.

## Not done, on purpose

- No numbers were allocated for gaps and assumptions beyond the WP-local `CG-A6-tables-n` and `ASM-A6-tables-n` candidates; step D1 does the GAP-nnnn and ASM-nnnn numbering and rewrites the citations.
- The merge into `ownership.json`, the xlsx and the FK-cut sheet belong to `compat/ownership.py merge` (Stage C); this WP writes only its part file.
- The WP line on jobs ("replacement": Temporal Schedule or event-started workflow) applies to the JOB-nn items, which sit in the flows part; the tables section has none, so no row here carries a `replacement` key. The Quartz retirement is recorded where it touches a table: `job_catalog` (ruling 9) and `timer` (ruling 12).
- No approval was sought; the part file stands as a Draft input to the merge.
