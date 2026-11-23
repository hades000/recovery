# Edit log B-ARCH-DB — Physical Schema folder v-next, LDM v-next, ERD v-next

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## What was done

- Read the source once and split it by statement, not by line: 93 `CREATE TABLE`, 31 `CREATE VIEW`, 92 `ALTER TABLE ... FOREIGN KEY`, 112 `CREATE INDEX`, 89 table comments, 1026 column comments, 2584 seed `INSERT` and 3 helper functions.
- Wrote the Physical Schema v7 as a new folder with exactly the 19 service files, `recovery_views.sql` and `README.md`. No source folder was copied and the v6 `.sql` was not edited.
- Owner for every table is the Ownership Map sheet Tables. Each file creates its own `rwb_<name>` schema, sets its search path and carries the two §R8.1 header lines and the change-log row.
- Foreign keys: 44 kept (same owner, 42 of them drawn by ERD v5 plus the 2 v6 metadata keys), 48 cut at an owner boundary. A cut column keeps its name and type, gains a trailing comment and is repeated in a note block at the end of the file.
- Platform library: `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` are emitted in all 19 schemas, because DP-09 and Architecture v5 slide 20 put them in every service schema. `feature_flag` and `feature_flag_change` are emitted once in `rwb_integration.sql`, because rwb-integration serves the feature-flag admin API (ruling ASM-0039).
- Views: the data dictionary view moves to `rwb_source_data`; the 30 `recovery.v_ace_*` views and the three helper functions stay in schema `recovery`, read only, following Architecture v5 slide 29. The append-only trigger `refuse_change()` and its two triggers stay with P7 and P1.
- LDM v9: v8 is copied to v9 and the original nine sheets are unchanged. Five sheets are added: `Read me` (first, carrying the §R8.1 header and the change-log row), `Service ownership` (123 entities), `Schema map` (19 services), `Cross-service references` (48) and `Realignment change log`.
- ERD v6: the source is `Recovery Workbench Entity Relationship Diagram v5.pdf` (97 pages). A PDF cannot be written by the office helper, so v6 is Markdown with one Mermaid `erDiagram` per service (19), one for the platform library and one for the ACE boundary, plus two reference tables. The v5 numbers are repeated: 123 objects, 108 references (90 foreign keys, 18 business-key links), 54 cross data-product and 54 inside, 14 data products plus OPS, AGT and RPT.
- Gaps and assumptions: 10 candidate gap rows and 10 candidate assumption rows, one assumption per gap. No person name, no e-mail address, no issue-tracker reference.

## Files written

- `06 Data/Recovery Workbench Physical Schema v7/rwb_source_data.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_integration.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_case.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_access.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_document.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_comms.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_decision.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_payment.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_reporting.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_agent.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_valuation.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_treatment.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_guarantee.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_litigation.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_asset.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_debtsale.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_writeoff.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_deviation.sql`
- `06 Data/Recovery Workbench Physical Schema v7/rwb_partner.sql`
- `06 Data/Recovery Workbench Physical Schema v7/recovery_views.sql`
- `06 Data/Recovery Workbench Physical Schema v7/README.md`
- `06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx`
- `06 Data/Recovery Workbench Entity Relationship Diagram v6.md`
- `_work/msr/gaps/B-ARCH-DB.jsonl`
- `_work/msr/assumptions/B-ARCH-DB.jsonl`
- `_work/msr/editlog/B-ARCH-DB.md`
- `_work/msr/docs/B-ARCH-DB/gen_schema.py`
- `_work/msr/docs/B-ARCH-DB/gen_views.py`
- `_work/msr/docs/B-ARCH-DB/gen_readme.py`
- `_work/msr/docs/B-ARCH-DB/gen_ldm.py`
- `_work/msr/docs/B-ARCH-DB/gen_erd.py`
- `_work/msr/docs/B-ARCH-DB/gen_rows.py`
- `_work/msr/docs/B-ARCH-DB/verify_schema.py`
- `_work/msr/docs/B-ARCH-DB/schema_report.json`

## Rows

- Candidate gaps: 10 rows, `GAP-0107` to `GAP-0116`.
- Candidate assumptions: 10 rows, `ASM-0178` to `ASM-0187`, one per gap, confidence High (7) and Medium (3).

## Counts

- Physical Schema: 19 `rwb_<name>.sql` files. 165 `CREATE TABLE` statements for 93 distinct tables (89 once plus the 4 library objects 19 times); 80 foreign-key statements (44 kept plus the 2 library keys repeated 18 more times); 184 index statements for 112 source indexes; 161 table comments for 89 source comments; 1548 column comments for 1026 source comments; 2584 seed rows. The extra counts are the 18 additional copies of the four library objects.
- `recovery_views.sql`: 31 views (30 ACE plus the data dictionary), 3 helper functions and the grants template.
- LDM: 9 source sheets unchanged plus 5 new sheets (123 ownership rows, 19 schema rows, 48 cross-service rows).
- ERD: 123 objects, 108 v5 references (90 foreign keys and 18 business-key links), 48 cut references.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ARCH-DB --quick`: C02, C03, C05, C12, C13 and C18 PASS with zero findings.
- C14, C15, C16, C17 and C20 over the same 35-file set: PASS with zero findings. C19 is a run-wide queue check over other WPs' planned outputs and is not part of this WP.
- Scratch verifier `verify_schema.py`: every one of the 93 tables appears in exactly one service file except the four library objects (19 each); every index, comment and seed row points to a table in the same file; every kept foreign key points to a table in the same file; 0 problems.
- Citation check: every `CG-B-ARCH-DB-n` and `ASM-B-ARCH-DB-n` written in the folder, the LDM and the ERD has a row.

## Failures

None.
