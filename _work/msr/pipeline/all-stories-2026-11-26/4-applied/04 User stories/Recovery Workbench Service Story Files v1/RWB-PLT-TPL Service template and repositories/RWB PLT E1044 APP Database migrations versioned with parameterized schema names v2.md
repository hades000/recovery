# RWB-PLT-E1044-APP Database migrations versioned with parameterized schema names

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1044-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-044 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Patterns applied | DP01, DP05, DP06, DP07, DP13, DP14, DP15, DP19 |
| Parallel lane | L-PLT-TPL-G |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-E1044-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-005, FR-PLT-006, FR-PLT-007) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: preserved from RWB-E1-044 word for word and re-pointed at the platform template; the microservice delta is RWB-PLT-E1044-APP-2 with the contract in RWB-PLT-E1044-CON and the deployment in RWB-PLT-E1044-OPS. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-PLT-E1044-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **every schema change applied by a versioned Flyway migration, one migration per story, forward-only in PROD, with the schema name taken from a parameter**, so that **the database in every environment is the sum of known migrations and nothing else**.

### 2. Business rationale

The recovery tables share the ACE database with the collection module, and two squads change it from one repository (DT07, DT08). A column added by hand in one environment makes SIT and UAT test a database that PROD does not have. This story makes every change a numbered, checksummed migration with no schema name written in the file, and fails the pipeline on drift. It supports REQ-RDF-001 (the 14 data products held in the ACE database) and REQ-RDF-014 (stage 2 tables exist before the first treatment goes live). The measure is zero schema differences between a clean build and each environment at every release.

### 3. Preconditions

- The recovery tables are defined in the Logical Data Model and Recovery Workbench Physical Schema v6.sql.
- The recovery module folder and boundary test exist (RWB-TE-001).
- Each environment has a database account for migrations and a read-only account for the drift check, held in the key store (NFR-052).
- The schema parameter `RWB_SCHEMA` is set per environment (DEV, SIT, UAT, PROD). Assumed value `recovery` in every environment, as in Recovery Workbench Physical Schema v6.sql.
- Deployment slots are booked (DL35).

### 4. Flow

1. Developer: adds one migration file for the story under `recovery/src/main/resources/db/migration/recovery/`, named `V<number>__<description>.sql`, with the header line `-- Story: <story key>`.
2. Pipeline: runs the migration lint: no literal schema name, no foreign key into `public`, exactly one story key per file, no story key in two files, no undo file.
3. Pipeline: starts a clean PostgreSQL container and applies all migrations with `RWB_SCHEMA` set.
4. Pipeline: runs the drift check: dumps the schema object list of the clean database and of the target environment, and compares them.
5. Deployment: on service start, Flyway applies each pending migration once, in version order, and writes its checksum to the history table.
6. Deployment: Flyway validates the checksums of applied migrations; a changed file stops the start.
7. Platform administrator: reads the migration run on SCR-44 Interface and job monitor.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An object in the target environment is not produced by the migrations | The pipeline fails and names each extra or missing object | MSG-P3-016 | AC2 |
| X2 | An applied migration file was edited after it ran | Flyway validation fails and the service does not start | MSG-P3-016 | AC4 |
| X3 | A migration contains a literal schema name | The lint fails the build and names the file and line | MSG-P3-016 | AC5 |
| X4 | Two migration files carry the same story key, or one carries none | The lint fails the build | MSG-P3-016 | AC6 |
| X5 | An undo migration or a clean command is used against PROD | Refused; PROD runs forward only | MSG-P3-016 | AC7 |
| X6 | A migration fails part way | The transaction rolls back; the history records the failure; the service does not start | MSG-P3-016 | AC8 |
| X7 | Two service instances start at the same time | One applies the migrations; the other waits for the lock and finds nothing pending | None | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the table definitions in the Logical Data Model; it comes first so every later table is a migration |
| Negotiable | The schema name and the history table name are parameters; the story fixes the process |
| Valuable | Every later story changes the database the same way, and environments stay equal |
| Estimable | Flyway configuration, two pipeline checks and a lint |
| Small | Fits in one week with its tests |
| Testable | Each criterion runs in the pipeline against PostgreSQL containers |

### 7. Acceptance criteria

```gherkin
Feature: Database migrations versioned with parameterized schema names

  Background:
    Given the schema parameter RWB_SCHEMA is "rwb_case"
    Given the Flyway history table is "flyway_schema_history_recovery"

  Scenario: AC1 Migration applied (legacy RWB-E1-044 AC1)
    Given migration V12__add_queue_to_case.sql with the header "-- Story: RWB-E1-020"
    When the deployment runs
    Then the migration applies once
    Then its version 12 and its checksum are recorded in "flyway_schema_history_recovery"
    Then a second deployment run applies nothing and changes no object

  Scenario: AC2 Drift detected (legacy RWB-E1-044 AC2)
    Given a column "note_x" added by hand to table "queue" in SIT
    When the migration check runs
    Then the pipeline fails with MSG-P3-016 naming "rwb_case.queue.note_x"
    Then no deployment to SIT starts

  Scenario: AC3 Schema name as parameter (legacy RWB-E1-044 AC3)
    Given RWB_SCHEMA set to "rwb_case" in DEV and in SIT
    When the migration V13__create_timer.sql runs in DEV and in SIT
    Then the table "timer" exists in schema "rwb_case" in both environments
    Then the file V13__create_timer.sql is byte for byte the same in both runs

  Scenario: AC4 Applied migration edited (legacy RWB-E1-044 AC4)
    Given V12__add_queue_to_case.sql applied in SIT with checksum 104553219
    Given the file changed in the repository so its checksum is 88120477
    When the service starts in SIT
    Then Flyway validation fails with MSG-P3-016 naming version 12
    Then the service does not start

  Scenario: AC5 Literal schema name (legacy RWB-E1-044 AC5)
    Given V14__add_index.sql contains the text "CREATE INDEX ix_a ON recovery.queue (team_code)"
    When the migration lint runs
    Then the build fails with MSG-P3-016 naming V14__add_index.sql line 1

  Scenario: AC6 One migration per story (legacy RWB-E1-044 AC6)
    Given V15__a.sql and V16__b.sql both carry the header "-- Story: RWB-E1-028"
    When the migration lint runs
    Then the build fails with MSG-P3-016 naming both files and RWB-E1-028

  Scenario: AC7 Forward only in PROD (legacy RWB-E1-044 AC7)
    Given the PROD configuration
    When a pipeline step calls Flyway clean or an undo migration U12__add_queue_to_case.sql is present
    Then the system refuses the step with MSG-P3-016
    Then no object in PROD changes

  Scenario: AC8 Migration fails part way (legacy RWB-E1-044 AC8)
    Given V17__add_two_columns.sql whose second statement refers to a table that does not exist
    When the deployment runs in DEV
    Then the system rolls the first statement back
    Then the history records version 17 as failed
    Then the service does not start and the run shows "failed" on the job monitor

  Scenario: AC9 Two instances start together (legacy RWB-E1-044 AC9)
    Given two service instances in SIT with migration V18__add_column.sql pending
    When both start within one second
    Then the system applies V18 exactly once
    Then both instances start
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every schema change is a versioned migration in the repository; no change is made by hand in any environment | ADR-002; DT08 |
| BR2 | No migration file contains a literal schema name; the schema comes from `RWB_SCHEMA` through the Flyway `${schema}` placeholder and the default schema | Principle 1 |
| BR3 | One migration file per story that changes the database, carrying the story key in its header | DL04 (merge owner per module) |
| BR4 | PROD runs forward only: clean is disabled, undo files are refused, a fix is a new compensating migration | DT11; NFR-027 |
| BR5 | An applied migration is never edited; checksums are validated on every start | DT11 (untested code is not merged) |
| BR6 | The recovery module keeps its own Flyway history table so its versions do not collide with the ACE and collection modules | DT07; DT08 |
| BR7 | The drift check runs before every deployment to SIT, UAT and PROD | CTL-02 (checks before use) |
| BR8 | No migration in the recovery schema declares a foreign key into `public`; an ACE row is held by its business key and ACE cascades deletes on `account`. The lint fails the build and names the file | ADR-010; D-RCV-35 U4 |

### 9. State transitions

None. This story does not change a case status. It changes the migration state of each environment: a migration moves from pending to applied (or failed) in `flyway_schema_history_recovery`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Runs deployments and reruns a failed migration job (Platform administration CRUD); reads migration runs on SCR-44 |
| RW-DATASTEW, data steward | Reads migration runs (Platform administration R) |
| RW-AUDIT, internal audit | Reads migration runs (Platform administration R) |
| Pipeline migration account | Applies migrations with the migration database account from the key store; not a Workbench role |

### 11. Data

No business field. The story writes the Flyway history table `flyway_schema_history_recovery`, which is a tool table and is not in the Logical Data Model. It reads the schema object list (`information_schema`) in each environment for the drift check.

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. This preserved story provides no REST operation: the governing migration contract is published by RWB-PLT-E1044-CON, the deployment behaviour is RWB-PLT-E1044-OPS, and the as-built contract is kept in the "As built (monolith)" section below.

#### 12.2 REST operations consumed

None. The only consumed operation of the as-built story is the P1 job view `GET /admin/jobs?type=MIGRATION`, which keeps its as-built description below and moves to RWB-PLT-E1044-APP-2 and RWB-PLT-E1044-OPS in the target.

#### 12.3 Events published

None. A migration publishes no event.

#### 12.4 Events consumed

None. A migration consumes no event.

#### 12.5 Workflows and activities

None. Migrations run at service start, not inside a Temporal workflow or activity.

#### 12.6 Schedules

None. There is no schedule: the run is triggered by service start and by the pipeline step.

#### 12.7 Tables owned

None. The only table the as-built story writes is the Flyway tool table `flyway_schema_history_recovery`, which is not a business table; the per-service history table is named in RWB-PLT-E1044-APP-2 and RWB-PLT-E1044-CON.

#### 12.8 Contract fakes

None. The migration fixture and the P1 job view fake are published by RWB-PLT-E1044-CON.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

None. This preserved story makes no REST, Kafka, Temporal or file call; the consumed job view keeps its as-built description below.

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**As-built component set unchanged.** The five components of the as-built plan stay as built: `RecoveryFlywayConfig`, `MigrationRunRecorder`, `MigrationLint`, `SchemaDriftCheck` and the `V0001__rwb_e1_001_recovery_schema.sql` baseline. This story changes none of them. The microservice delta starts in RWB-PLT-E1044-APP-2 (one sequence, one schema and one history table per service), is published as a contract by RWB-PLT-E1044-CON and is deployed through RWB-PLT-E1044-OPS.

**Done when.** The ten test cases of section 16 still pass against the platform template, and the delta is delivered by RWB-PLT-E1044-APP-2, RWB-PLT-E1044-CON and RWB-PLT-E1044-OPS. The legacy level `System` in section 16 maps to Component or End to end in the target; the delta test cases are in RWB-PLT-E1044-APP-2 and RWB-PLT-E1044-OPS.

The per-service history table name and the fields of the migration-run record are Not specified in the source documents (GAP-1420; ASM-2488); this story keeps `flyway_schema_history_recovery` exactly as built.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-016 | Drift found, checksum mismatch, lint failure, a refused clean or undo, or a failed migration | Schema check failed in {schema}: {object}. The deployment was stopped. |
| MSG-P4-002 | A role without Platform administration R reads migration runs | You cannot {action} here. Your role does not include it. |

MSG-P3-016 is new (see Additions). It is shown in the pipeline log and on SCR-44, not to business users.

### 15. Screens and states

SCR-44 Interface and job monitor, state Running, Failed or Complete: the platform administrator reads each migration run with its version, checksum and drift result. No new screen in this story.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-044-01 | AC1, BR1, BR5 | System | V12 fixture migration, two deployment runs |
| TC-E1-044-02 | AC2, BR7 | System | SIT container with a hand-added column |
| TC-E1-044-03 | AC3, BR2 | System | DEV and SIT containers with RWB_SCHEMA = rwb_case |
| TC-E1-044-04 | AC4, BR5 | System | V12 edited after it ran |
| TC-E1-044-05 | AC5, BR2 | System | V14 with a literal schema name |
| TC-E1-044-06 | AC6, BR3 | System | Two files with the same story key |
| TC-E1-044-07 | AC7, BR4 | System | PROD profile, clean call and an undo file |
| TC-E1-044-08 | AC8 | System | V17 with a broken second statement |
| TC-E1-044-09 | AC9 | System | Two instances, one pending migration |
| TC-E1-044-10 | Access | Access | RW-CASEOWN (Platform administration none) reads `GET /admin/jobs?type=MIGRATION`; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- One schema and one login per service: a migration writes only `rwb_<name>` and runs under that service's own login (DP-01, DP-02).
- No literal schema name in a migration or in a repository query; the schema is `${schema}` fed by `RWB_SCHEMA`, and the file stays byte for byte the same in every environment.
- No cross-schema join, view or foreign key; a service holds another service's ID and asks the owner through its contract.
- No business value in a migration; seed values are reference loads (RWB-PLT-E1043-CON), never migration inserts.
- No personal data in a migration, a test or a log; no migration copies production rows.
- ACE data only through the P1 rwb-source-data contract or the `v_ace_*` views; a service never reads an ACE table directly.
- Forward only: no clean, no undo file and no edit of an applied migration; a fix is a new version.
- No manual change in any environment; a hotfix is a new migration through the pipeline.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | Recovery data held in 14 data products in the ACE database | Business Requirements Epic 1, section 4; Program, section 5.1 | FEAT-CWC-24 | All recovery processes | CTL-02; DT08 | TC-E1-044-01 to TC-E1-044-10 |
| REQ-RDF-014 | Stage 2 data products exist before the first treatment goes live | Business Requirements Epic 2, section 4; Program, section 5.1 | FEAT-CWC-24 | All recovery processes | DT11 | TC-E1-044-01, TC-E1-044-03 |

### 19. Out of scope

- The table definitions themselves (RWB-E1-001 and each story that adds a table).
- Seed reference data (RWB-E1-043).
- Code owners and the browser test runner in the pipeline (DL37, RWB-TE-002).
- Deployment slots and release windows (DL34, DL35).

## As built (monolith)

#### 12. Contract

**GET /api/recovery/v1/admin/jobs** (P1 endpoint) lists migration runs with `type=MIGRATION`.

| Item | Value |
|---|---|
| Request | Query `type` = MIGRATION, `status`, `from`, `to` |
| Response | 200 `Job[]`: `id`, `type`, `businessDate`, `status` (APPLIED, FAILED), `startedAt`, `endedAt`, `checks` (version, checksum, drift result) |
| Errors | 401 (MSG-P4-001); 403 no Platform administration R (MSG-P4-002); 503 |
| Authorization | Platform administration, right R |
| Idempotency | Not applicable |

**Migration job**

| Item | Value |
|---|---|
| Trigger | Service start in each environment, and the pipeline step `migrate` |
| Job name | Not a scheduled job in batch.txt; it runs at deployment |
| Input | The files in `db/migration/recovery`, `RWB_SCHEMA`, the migration account |
| Output | Applied objects in schema `RWB_SCHEMA`; rows in `flyway_schema_history_recovery`; one `Job` record per run through the P1 job monitor |
| Events published | None |
| Idempotency key | Migration version. An applied version is never applied again |
| Restart behavior | A failed migration rolls back; after a fix is merged as a new version, the next start applies it |

**Configuration** (Spring Boot properties, values from the configuration service):

```properties
spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration/recovery
spring.flyway.schemas=${RWB_SCHEMA}
spring.flyway.default-schema=${RWB_SCHEMA}
spring.flyway.table=flyway_schema_history_recovery
spring.flyway.placeholders.schema=${RWB_SCHEMA}
spring.flyway.validate-on-migrate=true
spring.flyway.out-of-order=false
spring.flyway.clean-disabled=true
```

#### 13. Solution plan

**Package.** `recovery.casewf.migration` (configuration and checks); migration files in `recovery/src/main/resources/db/migration/recovery`; pipeline scripts in `recovery/build/migration-checks`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RecoveryFlywayConfig | Service | Builds the recovery Flyway instance from the properties above; refuses clean in every profile |
| MigrationRunRecorder | Service | Writes one job record per migration run through the P1 job monitor interface |
| MigrationLint | Job | Build step: refuses literal schema names (pattern on `<identifier>.` before a table name for every name in `sys_objects`), a foreign key into `public`, missing or repeated story keys, and `U*.sql` files |
| SchemaDriftCheck | Job | Pipeline step: applies all migrations to a clean container, lists tables, columns, types, constraints and indexes of `RWB_SCHEMA`, compares with the target environment through the read-only account, reports each difference |
| V0001__rwb_e1_001_recovery_schema.sql | RWB-E1-001 baseline | Built from Recovery Workbench Physical Schema v6.sql with the `${recoverySchema}` placeholder and `SET search_path` removed; applied by RWB-E1-001 (D-RCV-28) |

**Database.** No business table changes. Flyway creates `flyway_schema_history_recovery` in `RWB_SCHEMA`. The baseline migration creates the 92 tables of Recovery Workbench Physical Schema v6.sql; the 4 extension tables ship inside it as ordinary tables of the recovery schema, and the 30 `v_ace_*` views ship in two later migrations (Section A with RWB-E1-069, Section B after RWB-ACE-001). No migration in the recovery schema declares a foreign key into `public`: an ACE row is held by its business key. The initial seed rows (`lov_value`, `role`, `permission`, `delegation_limit`, `sys_objects`, `sys_fields`, `data_product`) ship with the RWB-E1-001 baseline `V0001__rwb_e1_001_recovery_schema.sql` (D-RCV-28, D-RCV-29); later dictionary changes are reference loads through RWB-E1-043, not migrations.

**Configuration and reference data.** The schema value is the placeholder `${recoverySchema}`, fixed to `recovery` in every environment (D-RCV-28); no per-environment override. Migration and read-only database accounts in the key store, set by the platform administrator.

**Build steps**

Ruled 2026-11-05 as D-RCV-28: recovery Flyway files are named `V<seq>__<story>_<name>.sql` with a four-digit sequence taken in merge order; line 1 is `-- Story: <story key>`; the schema is referenced only as `${recoverySchema}` and is `recovery` in every environment. The RWB-E1-001 baseline is `V0001__rwb_e1_001_recovery_schema.sql`; RWB-E1-044 ships no production migration file. Former open point: The rule in this story is a single rising number with the placeholder ${schema} fed by RWB_SCHEMA. The other 51 stories that name a migration file use four other rules, 30 of them V<epic>_<story>__<name>.sql with the placeholder ${recoverySchema} as in RWB-E1-001. The lint rule reports and fails the build for a name that breaks the rule.

1. Add Flyway to the recovery module and `RecoveryFlywayConfig` with the properties in section 12; prove start-up applies and records a test migration.
2. Convert Recovery Workbench Physical Schema v6.sql into the RWB-E1-001 baseline `V0001__rwb_e1_001_recovery_schema.sql` with the `${recoverySchema}` placeholder; prove it creates every table in the recovery schema.
3. Build `MigrationLint` and add it to the build; test each refusal with fixture files.
4. Build `SchemaDriftCheck` and add it before each deployment stage; test with a hand-added column.
5. Build `MigrationRunRecorder` and show runs on the job monitor.
6. Prove forward only: clean refused, undo files refused, failed migration rolls back.
7. Prove the lock with two instances starting together.

**Feature flag.** `rwb.p3.migration-drift-gate`. On in SIT, UAT and PROD: drift fails the deployment. Off in DEV: drift is reported and the deployment continues.

**Done when.** The tests in section 16 pass, and DEV and SIT show no drift against the baseline.
