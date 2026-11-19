# Tasks — RWB-E1-042

| TASK ID | Description | Trace | BLOCKED_BY | Verification |
|---|---|---|---|---|
| `TASK-RWB-E1-042-00` | Plan precondition check: PRE-1, PRE-2, PRE-3, PRE-4, PRE-5 recorded with a date. Stop if PRE-3/PRE-4 are not approved. | SPEC-012; D-RCV-15 | NONE | Decisions in the increment card |
| `TASK-RWB-E1-042-01` | Copy the preserved migration `V0042__rwb_e1_042_parameter_catalog_and_seed.sql` into `backend/src/main/resources/db/modulemigration/recovery/`; confirm line 1, `${recoverySchema}`, no literal schema. | SPEC-003, -010 | 00 | `head -1`; `grep -n "recovery\\.\|ace\\.\|public\\."` only in comments; lint |
| `TASK-RWB-E1-042-02` | Copy `config/parameter-catalog.csv` and `config/messages-e1-042.csv`; add the six Temporal/Drools keys. | SPEC-002, -003 | 01 | CSV row count 19; keys unique |
| `TASK-RWB-E1-042-03` | Run `Generate-ParameterSeed.ps1` and `Assemble-V0042.ps1`; diff the output against the committed file. | SPEC-003 | 02 | `git diff --exit-code` on V0042 |
| `TASK-RWB-E1-042-04` | Generate `ParameterKeys` from the CSV; no hand-written key. | SPEC-002, -011 | 02 | `./gradlew generateParameterKeys`; no raw key string in `src/main` |
| `TASK-RWB-E1-042-05` | Entities, repositories and `ParameterSnapshot`; map the columns. | SPEC-002, -003 | 01 | `./gradlew compileJava`; repository test |
| `TASK-RWB-E1-042-06` | `ParameterService` typed read, cache, secret redaction, version resolution. | SPEC-002, -008, -011 | 04, 05 | Unit test T-042-01/08/09/11 |
| `TASK-RWB-E1-042-07` | `ParameterLoadChecks` and `ParameterLoadHandler`; CSV parse; type/range/environment/product/duplicate. | SPEC-004, -005 | 05 | Unit test T-042-05/06/12 |
| `TASK-RWB-E1-042-08` | `ParameterApprovalService` and `ParameterRollbackService`; author != approver; effective date; outbox; decision log. | SPEC-006, -010, -011 | 06, 07 | Unit test T-042-07/10/11 |
| `TASK-RWB-E1-042-09` | `ParameterStartupCheck`; readiness fails with `MSG-P3-032`. | SPEC-007 | 06 | Integration test T-042-04 |
| `TASK-RWB-E1-042-10` | `ParameterCatalogController` and the load/approve/rollback endpoints; method security. | SPEC-009, -012 | 06, 08 | Contract test; 401/403/409/422 |
| `TASK-RWB-E1-042-11` | `RwbMagicNumberCheck` and `CatalogCompletenessCheck` build checks. | SPEC-003, -004 | 04, 06 | Fixture fails/passes |
| `TASK-RWB-E1-042-12` | Wire the decision log and the interaction ledger; `ParameterVersionApproved` outbox. | SPEC-010, -011, -012 | 08 | Test: failed log write blocks approval |
| `TASK-RWB-E1-042-13` | Cache invalidation on approval; TTL from `cache.refresh.seconds`. | SPEC-011 | 06, 08 | Test: no restart, new value served on date |
| `TASK-RWB-E1-042-14` | Update the catalog completeness fixture and the message resolver. | SPEC-003, -009 | 02, 11 | Fixture test |
| `TASK-RWB-E1-042-15` | Run `tests/test_migrations.sh` on PostgreSQL 16: clean, re-run, baseline, negatives. | SPEC-003, -010 | 01, 03 | `evidence/migration-test-output.txt` |
| `TASK-RWB-E1-042-16` | Backend unit and integration tests; JaCoCo 80%. | SPEC-001..012 | 05..14 | `recoveryCoverageVerification` |
| `TASK-RWB-E1-042-17` | Evidence pack: logs, coverage, test results, migration output. | All | 15, 16 | `implement/report.md` |
| `TASK-RWB-E1-042-18` | Traceability and MR record; no commit/push unless asked. | All | 17 | Matrix refs; MR link recorded |

## Dependency graph

```
00 -> 01 -> 02 -> 03 -> 04 -> 11
        |      |            |
        v      v            v
        05 -> 06 -> 07 -> 08 -> 10 -> 12 -> 13
               |      |      |
               v      v      v
               09    14     15 -> 16 -> 17 -> 18
```

## Coverage

| SPEC | Tasks |
|---|---|
| 001 | 16 |
| 002 | 04, 05, 06 |
| 003 | 01, 02, 03, 05, 11, 14, 15 |
| 004 | 07, 11 |
| 005 | 07 |
| 006 | 08 |
| 007 | 09 |
| 008 | 06 |
| 009 | 10, 14 |
| 010 | 01, 08, 12, 15 |
| 011 | 06, 08, 13 |
| 012 | 10, 12, 18 |

## Pre-submit checks

| Check | Result |
|---|---|
| Every SPEC-001..012 maps to a task | YES (12/12) |
| Every task has `BLOCKED_BY` (`NONE` only for TASK-00) | YES |
| Migration is one file, D-RCV-28 name | YES |
| No frontend task | YES (UI NO) |
| No new dependency | YES |
| No question asked | YES |
