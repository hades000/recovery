---
title: "Implementation Plan — RWB-E1-042 Central configuration service and parameter catalog"
run_id: "INC-003-epic-1-RWB-E1-042"
story: "RWB-E1-042"
status: "SUCCESS"
---

# Implementation Plan — RWB-E1-042 Central configuration service and parameter catalog

Design Source: NOT_REQUIRED (`UI In Scope: NO`, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`).

| Field | Value |
|---|---|
| Story | `RWB-E1-042` Central configuration service and parameter catalog |
| RUN_ID | `INC-003-epic-1-RWB-E1-042` |
| Input spec | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` (`SPEC-RWB-E1-042-001..012`, 11 ACs, 10 exception paths) |
| Preserved implementation | `output/INC-003-epic-1-RWB-E1-042/implement/` (10 Nov 2026 pack) |
| Governing decisions | D-RCV-28, D-RCV-35, D-RCV-36, D-RCV-49, D-RCV-50 |
| Baseline | Document set v14, 16 November 2026; Physical Schema v6; API Specification v4 |
| Prepared | 2026-11-16, Implementation Planner (agent run) |
| Approval | Plan gate pending human; no question asked |

## Plan approval preconditions

| ID | Precondition | Owner | State | Evidence when met |
|---|---|---|---|---|
| PRE-1 | Specification approval (backlog and specification gate) | Product Owner | APPROVED for v2 baseline 2026-11-16 | `specify/compliance-validation.md` `PASS` |
| PRE-2 | Preserve the 10 Nov migration pack as the build baseline | Recovery tech lead | APPROVED (pack is in `../implement/`) | `implement/README.md` |
| PRE-3 | Plan approval | Forward Deployed Architect | **PENDING HUMAN** | Approval comment in the increment card |
| PRE-4 | Task approval | Forward Deployed Engineer | **PENDING HUMAN** | Approval comment in the increment card |
| PRE-5 | Jenkins Flyway second step (`db-migrate,db-migrate-recovery`) | K. Tee | OPEN-019 | Jenkins change record |

`TASK-RWB-E1-042-00` checks PRE-1..PRE-5. If PRE-3/PRE-4 are not approved, the plan is complete but
the build does not start. This is a gate, not a question to the user.

## Change scope

| Field | Value |
|---|---|
| Change type | `NEW_STORY` |
| UI in scope | NO |
| Logic in scope | YES — catalog, typed read, load checks, approval, effective dating, rollback, cache, startup check |
| API in scope | YES — `GET /admin/parameters` and the `PARAMETER` load/approve/rollback handlers |
| Frontend changes | NO |
| Backend changes | YES |
| Migration | YES — `V0042__rwb_e1_042_parameter_catalog_and_seed.sql` |
| New dependency | None; existing stack only |

## Scope

### In scope

1. `parameter_catalog` and `parameter_value` tables in schema `recovery` (guarded against V0001).
2. 13 bootstrap catalog rows and 28 value rows from `config/parameter-catalog.csv`.
3. Generated `ParameterKeys` constants; no hand-written key string in code.
4. `ParameterService` typed read (`getInt`, `getString`, `getBoolean`, `getDecimal`, `getDuration`).
5. `ParameterLoadChecks` and `ParameterLoadHandler` for `table=PARAMETER`.
6. `ParameterCatalogController` (`GET /api/recovery/v1/admin/parameters`).
7. Load, approve and rollback endpoints for the reference-load pattern.
8. `ParameterStartupCheck` and readiness gate.
9. Cache with `cache.refresh.seconds`, event-driven invalidation on approval.
10. `RwbMagicNumberCheck` and `CatalogCompletenessCheck` build checks.
11. `ParameterVersionApproved` outbox event and decision-log entry.
12. The six Temporal/Drools parameters from the v2 baseline.

### Out of scope

- The parameter admin screen SCR-39 (Epic 8).
- Secret value storage; secrets stay in the ACE secret store.
- A new API version; the contract is additive in v1.
- An inbound source load or tracker (D-RCV-35).
- A Temporal or Drools call from this story.

## Backend plan

### B-1 Migration

| Item | Value |
|---|---|
| File | `backend/src/main/resources/db/modulemigration/recovery/V0042__rwb_e1_042_parameter_catalog_and_seed.sql` |
| Header | `-- Story: RWB-E1-042` |
| Content | `CREATE TABLE IF NOT EXISTS parameter_catalog` and `parameter_value`; guarded constraints, FK, indexes; seed from the CSV |
| Schema | `${recoverySchema}`; no literal schema; no `SET search_path` |
| Baseline overlap | V0001 already creates both tables; the `DO` blocks add only missing constraints; `CREATE INDEX IF NOT EXISTS` |
| Corrective file | None planned; if needed, `V0043__rwb_e1_042_<name>.sql` with `-- Fix:` |
| Verification | `tests/test_migrations.sh` on PostgreSQL 16: clean, re-run, baseline overlap, 8 negatives, deployment guard |

The file in `../implement/sql/V0042__...sql` is the source. The plan does not rewrite it; the builder
copies it into the ACE path and runs the test.

### B-2 Domain and repository

| Class | Package | Responsibility |
|---|---|---|
| `ParameterCatalog` | `recovery.casewf.internal.config` | Entity, `parameter_catalog` |
| `ParameterValue` | `recovery.casewf.internal.config` | Entity, `parameter_value` |
| `ParameterCatalogRepository` | `...internal.config` | Spring Data JPA |
| `ParameterValueRepository` | `...internal.config` | Current-value query by key/environment/product/date |
| `ParameterKey` | `...api` | Value object for a dotted key |
| `ParameterSnapshot` | `...api` | Value, version, valid-from, unit, secret flag |

### B-3 Service and checks

| Class | Responsibility |
|---|---|
| `ParameterService` | Typed read, cache, version resolution, secret redaction |
| `ParameterCache` | Caffeine/ConcurrentMap with TTL from `cache.refresh.seconds`; invalidated by `ParameterVersionApproved` |
| `ParameterLoadChecks` | Type, range, environment, product, required, duplicate, version, author/approver |
| `ParameterLoadHandler` | `PARAMETER` table code: parse CSV `key,environment,value`, validate, write VALIDATED version |
| `ParameterApprovalService` | Approve (not author), effective date, outbox event, decision log |
| `ParameterRollbackService` | Restore the previous approved version; one call |
| `ParameterStartupCheck` | Every required key has a value or default; fail readiness |
| `ParameterKeysGenerator` | Build-time CSV → `ParameterKeys` |
| `RwbMagicNumberCheck` | Build-time scan for literal business values |
| `CatalogCompletenessCheck` | Build-time scan for keys read but not in the catalog |

### B-4 API

| Method | Path | Auth | Response |
|---|---|---|---|
| GET | `/api/recovery/v1/admin/parameters` | Rules and parameters R | `Parameter[]`; `valueInForce` absent for a secret |
| POST | `/api/recovery/v1/admin/reference-loads` (`table=PARAMETER`) | Reference data C | `LoadResult` with `loadId`, status VALIDATED |
| POST | `/api/recovery/v1/admin/reference-loads/{loadId}/approve` | Reference data A | `LoadResult` APPROVED; 409 if author |
| POST | `/api/recovery/v1/admin/reference-loads/{loadId}/rollback` | Reference data U | `LoadResult` ROLLED_BACK; 409 if no prior version |

Error mapping: 400 `MSG-GEN-001`, 401 `MSG-P4-001`, 403 `MSG-P4-002`, 409 `MSG-P7-002`/`MSG-P3-015`,
422 `MSG-GEN-002`/`MSG-P1-002`, 503 `MSG-P3-032`.

### B-5 Events and audit

| Event | When | Consumer |
|---|---|---|
| `ParameterVersionApproved` | After approval commit | Cache invalidation; decision log; reporting |

Every approve/rollback writes a `decision_log_entry` with `rule_id = PARAMETER`, `rule_version =
<versionNo>`, actor and outcome. A failed decision-log write rolls back the approval.

### B-6 Configuration

| Key | Default | Use |
|---|---|---|
| `cache.refresh.seconds` | 60 | Cache TTL |
| `parameter.catalog.path` | `config/parameter-catalog.csv` | Build-time catalog |
| `temporal.target` | per env | E1-070/071 |
| `temporal.namespace` | `rwb-recovery` | E1-070/071 |
| `temporal.taskqueue.platform` | `rwb-platform` | E1-070/071 |
| `temporal.retention.days` | 30 | E2-039 |
| `drools.kiebase.cache.max` | 20 | E1-072 |
| `rules.testcases.min` | 50 | E1-073 |

## Frontend plan

None. `UI In Scope: NO`; no route, component or i18n key. No frontend task.

## Integration and cross-layer

| Item | Plan |
|---|---|
| Flyway | The migration is applied by the recovery Flyway bean; the core bean is unchanged |
| Config | `application.yaml` gets no new literal; values come from the catalog or env |
| Jenkins | OPEN-019 second step; the recovery migration runs with `db-migrate,db-migrate-recovery` |
| ACE review | MR into `develop-recovery`; shared-file edits limited to the migration folder and config |
| Telemetry | `parameter.read`, `parameter.approved`, `parameter.rollback` metrics; no key value in the log |

## Unit test applicability

| Surface | Changes required | Unit tests | Coverage gate | References | Evidence |
|---|---|---|---|---|---|
| Backend | YES | REQUIRED | 80% lines/branches on `recovery` config package | SPEC-001..012 | JaCoCo `recoveryCoverageReport` |
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | UI NO | No frontend change |

## Requirement-to-task coverage

| SPEC | Tasks |
|---|---|
| 001 | 02, 03 |
| 002 | 04, 05, 12 |
| 003 | 05, 06, 14 |
| 004 | 07, 13 |
| 005 | 07, 12 |
| 006 | 08, 12 |
| 007 | 09, 12 |
| 008 | 04, 12 |
| 009 | 10, 12 |
| 010 | 11, 12 |
| 011 | 04, 08, 12 |
| 012 | 10, 12 |

Every task maps to at least one SPEC. No orphan task.

## Functional test scenarios

| ID | Scenario | AC |
|---|---|---|
| T-042-01 | Entry decision reads `case.entry.dpd` and records version 1 | AC1 |
| T-042-02 | Hard-coded literal in a fixture fails `RwbMagicNumberCheck` | AC2 |
| T-042-03 | Uncatalogued key fails `CatalogCompletenessCheck` | AC3 |
| T-042-04 | Required key missing in UAT fails readiness with `MSG-P3-032` | AC4 |
| T-042-05 | Value 366 for a 1..365 key is refused with min/max | AC5 |
| T-042-06 | "ninety" for an INTEGER key is refused with the failed check | AC6 |
| T-042-07 | Author approves their own version → 409 `MSG-P7-002` | AC7 |
| T-042-08 | SIT and PROD return their own value for the same key | AC8 |
| T-042-09 | Secret row is listed with no value | AC9 |
| T-042-10 | Rollback version 2 returns version 1 and its value | AC10 |
| T-042-11 | A value effective tomorrow is not served today; it is served tomorrow without restart | AC11 |
| T-042-12 | A new key requires a reviewed PR; a new value requires a load and approval | BR3, Flow 2 |
| T-042-13 | Baseline overlap: apply on top of V0001 adds only the missing constraints | Migration |
| T-042-14 | Re-run the migration is idempotent | Migration |

## Security, privacy and compliance

- Auth: Rules and parameters R (read), Reference data C/A/U (load/approve/rollback).
- Secret: `secret=true` rows never return a value; the secret is read from the secret store by the
  consumer, not by this service.
- Audit: approve and rollback write the decision log and the interaction ledger.
- PDPA: no personal data; the only sensitive value is a secret, which is redacted.
- No production data in tests; synthetic parameter values only.
- No new dependency; no new secret.

## Risks

| ID | Risk | Mitigation |
|---|---|---|
| R-01 | V0001 baseline overlap fails | Guarded DDL; baseline test in the pack |
| R-02 | A required key is missing at start-up | `ParameterStartupCheck` fails readiness; catalog completeness build check |
| R-03 | An author approves their own value | Approver != author check; 409 |
| R-04 | A stale cache serves an old value after approval | Event-driven invalidation + TTL |
| R-05 | A secret leaks through the read API | `secret` filter in the mapper; test |
| R-06 | A literal slips into code | `RwbMagicNumberCheck` build failure |

## Out of scope

- UI screen SCR-39; Epic 8.
- Secret value storage.
- Temporal/Drools runtime (only their parameter rows).
- A new API version.
- A second migration file.

## Assumptions

| ID | Assumption | Basis |
|---|---|---|
| `ASM-009` | The 10 Nov migration pack is the implementation baseline. | Preserved evidence |
| `ASM-011` | The four extension-table names are not used here. | D-RCV-35 U3 |
| `ASM-015` | Decision-log retention is 10 years. | Controls Catalog v3 |
| `L-RCV-03` | No question was asked; the six new parameters come from D-RCV-36 §3.1. | No-question rule |

## Status reporting

```text
PLAN_STATUS: SUCCESS
TASKS: 19
SCOPE: one module (recovery.casewf) + migration + named config; no other ACE module
BLOCKED_TASKS: 0 (PRE-3/PRE-4 are human gates, not blockers to plan completion)
ASSUMPTIONS: 4
NEXT_STEP: Human plan approval, then start the Implementation Builder with TASK-01 (copy the preserved migration) and TASK-02..18.
```
