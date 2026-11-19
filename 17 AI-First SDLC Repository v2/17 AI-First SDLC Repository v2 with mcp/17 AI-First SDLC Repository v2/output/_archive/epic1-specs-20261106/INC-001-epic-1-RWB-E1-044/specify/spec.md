# Technical Specification — RWB-E1-044 Database migrations versioned with parameterized schema names

| Field | Value |
|---|---|
| Story | RWB-E1-044 — Database migrations versioned with parameterized schema names |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-001-epic-1-RWB-E1-044` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-001, FR-RWB-020); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 044 Database migrations versioned with parameterized schema names v1.md` |
| Upstream IDs | BRD-RWB-001, BRD-RWB-020; FR-RWB-001, FR-RWB-020; REQ-RDF-001, REQ-RDF-014; US-RWB-E1-044; CTX-FEATURE-020; CTX-CONSTRAINT-006; DT07, DT08, DT11; NFR-027, NFR-052 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — SCR-44 Interface and job monitor already exists and only displays migration runs. No screen, component, route, label or state is added. |
| Logic In Scope | `YES` — migration lifecycle, lint, checksum validation, drift gate, forward-only guard, cluster lock and run recording. |
| API In Scope | `NO` — no new or changed contract. The story reuses `GET /api/recovery/v1/admin/jobs?type=MIGRATION` (P1). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `JOB` run record (P1 job monitor); SCR-44 Interface and job monitor; ACE Quartz/deployment pipeline. |
| New Nodes Required | `YES` — `RecoveryFlywayConfig`, `MigrationRunRecorder`, `MigrationLint`, `SchemaDriftCheck`, baseline `V1__rwb_e1_001_baseline.sql`. |
| Inherited Existing Behavior | RWB-TE-001 module folder and boundary test; RWB-E1-001 physical schema; RWB-E1-043 reference loads; ACE deployment pipeline and job monitor (RWB-E1-056). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every schema change is a versioned migration in the repository; no change is made by hand in any environment. | SPEC-RWB-E1-044-001, SPEC-RWB-E1-044-002, SPEC-RWB-E1-044-013 | DIRECT | Flyway is the only writer; baseline V1 is generated from Physical Schema v4; seed rows are excluded. | COVERED |
| BR2 | No migration file contains a literal schema name; the schema comes from `RWB_SCHEMA` through `${schema}` and the default schema. | SPEC-RWB-E1-044-001, SPEC-RWB-E1-044-004 | DIRECT | `spring.flyway.schemas`, `default-schema` and `placeholders.schema` all read `RWB_SCHEMA`; lint rejects `<name>.` before a known object. | COVERED |
| BR3 | One migration file per story that changes the database, carrying the story key in its header. | SPEC-RWB-E1-044-003 | DIRECT | Lint enforces exactly one `-- Story:` line, no key in two files, no `U*.sql`. | COVERED |
| BR4 | PROD runs forward only: clean disabled, undo files refused, a fix is a new compensating migration. | SPEC-RWB-E1-044-006 | DIRECT | `clean-disabled=true` in every profile; the PROD pipeline step refuses clean and any undo file. | COVERED |
| BR5 | An applied migration is never edited; checksums are validated on every start. | SPEC-RWB-E1-044-005 | DIRECT | `validate-on-migrate=true`; mismatch stops start with MSG-P3-016. | COVERED |
| BR6 | The recovery module keeps its own Flyway history table so versions do not collide with ACE and collection. | SPEC-RWB-E1-044-001 | DIRECT | `spring.flyway.table=flyway_schema_history_recovery`. | COVERED |
| BR7 | The drift check runs before every deployment to SIT, UAT and PROD. | SPEC-RWB-E1-044-008 | DIRECT | Pipeline step compares clean-container objects with the target through the read-only account. | COVERED |
| X1..X7 | Exceptional paths in the table below map one-to-one to SPEC-003..009. | SPEC-RWB-E1-044-003..009 | DIRECT | Drift, checksum, lint, duplicate key, clean/undo, partial failure and two-instance lock. | COVERED |

> **AC cleanup (4 November 2026):** all previous acceptance criteria in this story were development-process criteria and were removed from story §7. This engineering enabler has no business acceptance criteria; the coverage table above maps the business rules and exception paths only.

## User story intent interpretation

As a **platform administrator (RW-PLATADM)**, I want **every schema change applied by a versioned Flyway migration, one per story, forward-only in PROD, with the schema name taken from a parameter**, so that **the database in every environment is the sum of known migrations and nothing else**.

The story is a delivery-pipeline capability, not a business feature. It gives every later story a single way to change the recovery schema, makes SIT and UAT structurally equal to PROD, and stops a hand-made change from reaching an environment. The platform administrator reads migration runs on SCR-44; the pipeline performs the work.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Service start in each environment and the pipeline step `migrate`; a failed migration is rerun from the job monitor after a compensating migration is merged. |
| Preconditions | Physical Schema v4 is the baseline source; RWB-TE-001 module folder and boundary test exist; migration and read-only database accounts are in the key store (NFR-052); `RWB_SCHEMA` is set per environment; deployment slots are booked (DL35). |
| Input | Files in `recovery/src/main/resources/db/migration/recovery`, `RWB_SCHEMA`, the migration account, the target environment object list. |
| Output | Applied objects in `RWB_SCHEMA`; rows in `flyway_schema_history_recovery`; one job record per run; a drift report. |
| Feature flag | `rwb.p3.migration-drift-gate`. On in SIT, UAT and PROD: drift fails the deployment. Off in DEV: drift is reported and the deployment continues. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `flyway_schema_history_recovery` | `version`, `checksum`, `success` | Written by Flyway at apply time | Tool-managed, never edited | Unique `installed_rank`; `success=false` blocks the next start until a new version is merged. |
| `flyway_schema_history_recovery` | `script`, `description` | Migration file name | Tool-managed | File name `V<number>__<description>.sql`. |
| Migration file | `-- Story:` header | Author writes the story key | Author only, before merge | Exactly one key per file; a key may not appear in two files. |
| Migration file | `${schema}` placeholder | `RWB_SCHEMA` at run time | Never edited per environment | No literal schema name anywhere in the file. |
| Job record | `type`, `businessDate`, `status`, `checks` | `MigrationRunRecorder` | Read-only on SCR-44 | `type=MIGRATION`; status `APPLIED` or `FAILED`; checks hold version, checksum and drift result. |
| Drift report | object list and differences | `SchemaDriftCheck` | Read-only in the pipeline log | Names every extra and missing object; no PII. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Pending | Deployment start | Migration validates and applies | Applied | History row written with checksum; job record `APPLIED`. |
| Pending | Deployment start | Any statement fails | Failed | Transaction rolled back; history row `success=false`; service does not start; job record `FAILED`. |
| Applied | Deployment start | Checksum matches | Applied (unchanged) | Nothing applied; start continues. |
| Applied | Deployment start | Checksum differs | Blocked | Validation error MSG-P3-016; service does not start. |
| Applied | Drift check | Object list differs | Blocked deployment | Drift report; no deployment to SIT/UAT/PROD. |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Target object not produced by migrations | Drift gate fails; each extra or missing object named | MSG-P3-016 |
| X2 | Applied migration edited | Flyway validation fails; start blocked | MSG-P3-016 |
| X3 | Literal schema name in a migration | Lint fails the build with file and line | MSG-P3-016 |
| X4 | Duplicate or missing story key | Lint fails the build naming both files | MSG-P3-016 |
| X5 | Clean or undo against PROD | Refused; no object changes | MSG-P3-016 |
| X6 | Migration fails part way | Transaction rollback; failed history row; service does not start | MSG-P3-016 |
| X7 | Two instances start together | One applies; the other waits on the lock and finds nothing pending | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoint used | `GET /api/recovery/v1/admin/jobs?type=MIGRATION` (P1 job monitor). |
| Contract delta | None. `Job` already carries `id`, `type`, `businessDate`, `status`, `startedAt`, `endedAt` and `checks`. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R; 401 MSG-P4-001; 403 MSG-P4-002; 503. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | SCR-44 is an existing screen; no component, route, state or label changes. | Existing SCR-44 tests remain green. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-001, FR-RWB-020; SPEC-RWB-E1-044-001..013 | New Flyway configuration, lint, drift check and run recorder. | Positive, negative, boundary and error-path tests: apply once, re-apply, edited checksum, literal schema, duplicate story key, clean refused, partial failure, drift, two-instance lock. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `RecoveryFlywayConfig` | Service | Builds the recovery Flyway instance from the properties; refuses clean in every profile. |
| `MigrationRunRecorder` | Service | Writes one job record per migration run through the P1 job monitor interface. |
| `MigrationLint` | Build job | Refuses literal schema names, missing or repeated story keys, and `U*.sql` files; reports non-conforming names under DL42 without failing. |
| `SchemaDriftCheck` | Pipeline job | Applies all migrations to a clean PostgreSQL container, lists tables, columns, types, constraints and indexes, and compares them with the target through the read-only account. |
| `V1__rwb_e1_001_baseline.sql` | Migration | Baseline built from Physical Schema v4 with `recovery.` replaced by `${schema}` and `SET search_path` removed. |

### Package and boundaries

`recovery.casewf.migration` holds configuration and checks. Migration files live in
`recovery/src/main/resources/db/migration/recovery`; pipeline scripts in
`recovery/build/migration-checks`. The recovery history table holds recovery versions only; ACE and
collection keep their own. No module reads another module's tables.

### Data and migration

- No business table is added. Flyway creates `flyway_schema_history_recovery` in `RWB_SCHEMA`.
- The baseline creates the 43 tables of Physical Schema v4. Seed rows (`lov_value`, `role`,
  `permission`, `delegation_limit`, `sys_objects`, `sys_fields`) are reference loads under
  RWB-E1-043, never migration inserts.
- Every later story adds one `V<number>__<description>.sql`; the number is unique and rising.
- The migration account is used only by Flyway; the drift check uses the read-only account.

### Migration lifecycle

1. Lint the file set: one story key, no literal schema, no undo file, no duplicate key.
2. Start a clean PostgreSQL container and apply all migrations with `RWB_SCHEMA`.
3. Run the drift check against the target environment.
4. On deployment, Flyway takes the database lock, validates checksums and applies pending versions in
   order, each in one transaction.
5. Write the job record with version, checksum and drift result.
6. On failure, roll back the migration, record `success=false` and stop the service.

### Naming under DL42

The story fixes one rising number with `${schema}`. Until DL42 is recorded, `MigrationLint` reports
a non-conforming name without failing the build; the one-story-key, no-literal-schema and no-undo
checks still fail. This is the story's explicit interim instruction, not a new convention. No
application event is published; the run is visible through the job record.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-PLATADM | Platform administration CRUD | All |
| RW-DATASTEW | Platform administration R | All |
| RW-AUDIT | Platform administration R | All |
| Pipeline migration account | Apply migrations | Environment only |

The migration account is held in the key store and is not a Workbench role. `GET /admin/jobs` uses
Platform administration R; a role without it receives 403 MSG-P4-002.

### Observability and operations

- Job record: id, type `MIGRATION`, business date, status, start/end, checks (version, checksum, drift).
- SCR-44: state Running, Failed or Complete; version, checksum and drift result per run.
- Pipeline log: lint findings and drift differences with object names only.
- Alerts: failed migration, checksum mismatch, drift, lock timeout.
- Run book: restart after a compensating migration; never edit an applied file (RWB-E1-056).

### Performance

- Migrations run at deployment, not in the request path.
- One transaction per migration; the baseline is the only large transaction and runs once.
- The lock serialises concurrent starts; the second instance waits and then finds nothing pending.

### Feature flag and rollback

- `rwb.p3.migration-drift-gate`: on in SIT/UAT/PROD, off in DEV.
- Rollback: turn the gate off only in DEV; in higher environments a fix is a new compensating
  migration. Migrations are forward-only; the previous application tag is redeployed without
  reversing the schema.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-044-01 | BR1, BR5 | System | V12 fixture, two deployment runs | Applied once; version 12 and checksum recorded; second run no change |
| TC-E1-044-02 | BR7 | System | SIT container with hand-added `queue.note_x` | Drift gate fails; object named; no SIT deployment |
| TC-E1-044-03 | BR2 | System | DEV and SIT with `RWB_SCHEMA=rwb_case` | `timer` in `rwb_case` in both; file identical |
| TC-E1-044-04 | BR5 | System | V12 edited after apply | Validation fails; service does not start; MSG-P3-016 names version 12 |
| TC-E1-044-05 | BR2 | System | V14 with `ON recovery.queue` | Lint fails; file and line named |
| TC-E1-044-06 | BR3 | System | V15 and V16 both `-- Story: RWB-E1-028` | Lint fails; both files named |
| TC-E1-044-07 | BR4 | System | PROD profile, clean call and `U12` file | Refused; no object changes |
| TC-E1-044-08 | X6 | System | V17 with a broken second statement | First statement rolled back; history failed; service stops |
| TC-E1-044-09 | X7 | System | Two instances, V18 pending | V18 applied once; both start |
| TC-E1-044-10 | Authority | Security | RW-CASEOWN calls `GET /admin/jobs?type=MIGRATION` | 403; MSG-P4-002 |
| TC-E1-044-11 | BR3, DL42 | Unit | Fixture file with `V042_1__name.sql` | Reported, build does not fail |

## Guardrails and out of scope

- No business value in code or in a migration; seed values are reference loads (RWB-E1-043).
- No personal data in migrations, tests or logs; no migration copies production rows.
- No literal schema name in any migration or repository query; no manual change in any environment.
- Out of scope: the table definitions (RWB-E1-001 and later stories), seed reference data
  (RWB-E1-043), code owners and the browser runner (DL37, RWB-TE-002), deployment slots (DL34, DL35).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR2, SPEC-001 | Is `RWB_SCHEMA` `recovery` or `rwb_case`? The precondition says `recovery`; the scenario background says `rwb_case`. | The value is environment data; no file changes. | It is a parameter. The test uses `rwb_case` as the test value; production may use another. No code or file change. | RESOLVED | SPEC-001 |
| CLAR-002 | BR3, §13; SPEC-003, SPEC-012 | DL42 leaves five migration naming patterns in use. Which one wins? | The lint must not fail valid stories before the ruling. | Use one rising number with `${schema}` in this story. Until DL42 is recorded, report other patterns without failing; keep the other lint checks fatal. | RESOLVED | SPEC-003, SPEC-012 |
| CLAR-003 | BR4; SPEC-006 | Does "forward only" forbid a manual database restore? | It forbids clean and undo through the pipeline, not an approved disaster-recovery restore. | The story forbids clean and undo migrations; disaster recovery follows the ACE run book. | RESOLVED | SPEC-006 |
| CLAR-004 | BR6; SPEC-001 | Must the history table sit in `RWB_SCHEMA`? | Determines object ownership and drift scope. | Yes — `spring.flyway.table=flyway_schema_history_recovery` and the schema from `RWB_SCHEMA`. | RESOLVED | SPEC-001 |
| CLAR-005 | SPEC-010 | Does a second deployment write a second job record? | Affects SCR-44 noise and audit. | Yes, one record per run; the second shows `APPLIED` with no pending version and no object change. | RESOLVED | SPEC-010 |
| CLAR-006 | SPEC-007 | Is a failed migration retried automatically? | Determines restart behaviour. | No. The service does not start; a fix is merged as a new version, then the next start applies it. | RESOLVED | SPEC-007 |
| CLAR-007 | §12; SPEC-011 | Does the migration job need a new API? | Would create a contract delta. | No — `GET /admin/jobs?type=MIGRATION` is the existing P1 read. | RESOLVED | SPEC-011 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the architecture or
DL42's interim instruction. No item changes a business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend delivery story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New delivery-pipeline capability; no UI or API contract change; the existing job monitor endpoint is reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: versioned migrations and drift gate with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: No business acceptance criteria (story §7); all 7 business rules, 7 exception paths and 5 migration states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
