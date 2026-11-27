# RWB-PLT-E1044-APP-2 Database migrations versioned with parameterized schema names

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1044-APP-2 |
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
| Parallel lane | L-PLT-TPL-F |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-PLT-E1044-APP-2-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-005, FR-PLT-006, FR-PLT-007) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: delta copy of RWB-E1-044 for the platform template, one Flyway sequence, schema, login and history table per service (Arch v5 slide 29; ADR-021; DP-15). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (6 resolved, 18 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one Flyway sequence per service in that service's own `rwb_<name>` schema, under its own login and its own `flyway_schema_history`, with the schema named only as `${schema}` fed by `RWB_SCHEMA` and one `V0001` baseline per service**, so that **the 19 services migrate independently and a change in one service can never reach another service's schema**.

### 2. Business rationale

The as-built story runs one Flyway sequence for the whole recovery schema: one `recovery` schema, one `V0001` baseline and one `flyway_schema_history_recovery` table shared by every module. Arch v5 slide 29 replaces that with 19 schemas, one login each, Flyway per service in its own pipeline, no cross-schema joins or keys, and a boundary test in every build that fails on a cross-schema reference. ADR-021 makes per-service Flyway and migration ownership the decision of record and DP-15 is the pattern. One shared history table serialises 19 pipelines on one lock and lets one bad file stop every service; one sequence per service keeps "the database in every environment is the sum of known migrations and nothing else" true for each service and keeps the blast radius inside one schema. It supports REQ-RDF-001 (the 14 data products held in the ACE database) and REQ-RDF-014 (stage 2 tables exist before the first treatment goes live).

### 3. Preconditions

- The service template of RWB-PLT-TPL provides the Flyway module and the migration lint, the drift gate and the boundary test.
- Each of the 19 services has its own schema `rwb_<name>` and its own login in the ACE database (Arch v5 slides 29 and 41); creating them is database work outside this story.
- ADR-021 (per-service Flyway and migration ownership) is the decision in force.
- Each service pipeline has a clean PostgreSQL container and a read-only account for the drift check.
- `RWB_SCHEMA` is set per environment (DEV, SIT, UAT, PROD) to the schema of the service that is being deployed.
- No build dependency: the story has no build dependency and is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Take the Flyway module from the platform template into the service and set `spring.flyway.locations=classpath:db/migration/<service>`, `spring.flyway.schemas=${schema}`, `spring.flyway.default-schema=${schema}`, `spring.flyway.placeholders.schema=${schema}`, `spring.flyway.table=flyway_schema_history`, `spring.flyway.validate-on-migrate=true`, `spring.flyway.out-of-order=false` and `spring.flyway.clean-disabled=true`.
2. Add the service's `V0001` baseline from that service's part of the physical schema; the other services' tables are not in it.
3. Set `RWB_SCHEMA` per environment to the schema of the service; no migration file carries a schema literal.
4. Run the lint: file name `V<seq>__<story>_<name>.sql`, line 1 `-- Story: <story key>`, exactly one story key per file, a story key never in two services' files, no literal schema name, no foreign key into `public`, no `U*.sql` file.
5. Run the boundary test: a cross-schema join, view or foreign key fails the build.
6. Run the drift gate with the service's read-only account before the deployment.
7. Start two services at the same time in SIT and prove each migrates through its own login and its own history table, within the PgBouncer cap of that login.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A migration file contains a literal schema name | The lint fails the build and names the file and the line | MSG-P3-016 | AC3 |
| X2 | A migration references another service's schema in a join, a view or a foreign key | The boundary test fails the build and names the file and the line | MSG-P3-016 | AC2 |
| X3 | One story key appears in the files of two services, or a file carries none | The lint fails the build and names both files and the story key | MSG-P3-016 | AC4 |
| X4 | An applied file was edited after it ran | Flyway validation fails and the service does not start | MSG-P3-016 | AC5 |
| X5 | An object in the service's schema is not produced by its migrations | The drift gate fails and no deployment starts | MSG-P3-016 | AC5 |
| X6 | Two instances of one service start together | One applies the pending migrations; the other waits for the lock and finds nothing pending | None | AC6 |
| X7 | Two services migrate at the same time | Each uses its own login and history table; no shared lock is taken and both finish inside the connection cap | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the platform template and the 19 schemas and logins; it reads no other story's code |
| Negotiable | The migration folder name and the baseline content per service are settled per service; the rule is fixed |
| Valuable | Each service owns its migrations and no pipeline can block another |
| Estimable | Flyway module wiring, one baseline per service and the three gates |
| Small | Fits in one sprint with its tests, one service at a time |
| Testable | Each criterion runs in a pipeline against PostgreSQL containers |

### 7. Acceptance criteria

```gherkin
Feature: One Flyway sequence per service in its own schema

  Background:
    Given the platform template supplies the Flyway module with the schema placeholder ${schema} fed by RWB_SCHEMA
    Given each service has its own schema rwb_<name> and its own login

  Scenario: AC1 Each service has its own sequence, schema and history table (new, D-RCV-60)
    Given the service rwb-case with schema rwb_case and its own login
    When the service starts with RWB_SCHEMA set to rwb_case
    Then Flyway applies the service's V0001 baseline from db/migration/case
    Then the history rows are written to the default flyway_schema_history inside schema rwb_case
    Then no object is created in another schema and no other history table is written

  Scenario: AC2 A run against rwb_case creates nothing in rwb_payment (new, D-RCV-60)
    Given a migration file for rwb-case that references schema rwb_payment
    When the lint and the boundary test run in the build
    Then the boundary test fails on the cross-schema reference and names the file and the line
    Then the build stops and no deployment runs
    When a build runs only the migrations of rwb-case
    Then the object list of schema rwb_payment is unchanged

  Scenario: AC3 The same file applies in DEV and SIT (new, D-RCV-60)
    Given one migration file that names the schema only as ${schema}
    When it runs in DEV and in SIT with RWB_SCHEMA set to rwb_case
    Then the object is created in schema rwb_case in both environments
    Then the file is byte for byte the same in both runs
    Then no literal schema name is present in the file

  Scenario: AC4 One migration file per story per service (new, D-RCV-60)
    Given a story that changes the database of rwb-case
    When it adds two files for the same story, or a file whose story key is already in a file of rwb-payment
    Then the lint fails with MSG-P3-016 naming both files and the story key
    Then a story key appears in the files of exactly one service

  Scenario: AC5 Forward-only and drift guards carry over per service (new, D-RCV-60)
    Given the service rwb-case in SIT with its migrations applied
    When an undo file is added, or a column is added to rwb_case by hand
    Then the build or the drift gate fails with MSG-P3-016 naming the file or the object
    Then PROD refuses clean and undo and no object in PROD changes

  Scenario: AC6 Two services migrate concurrently through their own logins (new, D-RCV-60)
    Given rwb-case and rwb-payment both have pending migrations in SIT
    When both services start at the same moment with their own logins and history tables
    Then both apply their own migrations and neither waits for the other's lock
    Then each set of history rows is in its own schema
    Then the connections of the two logins stay within their PgBouncer caps
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One Flyway sequence per service, in the service's own schema; the files live in the service's own folder `db/migration/<service>` and run in its own pipeline | ADR-021; DP-15; Arch v5 slide 29 | AC1; TC-PLT-E1044-APP2-01 |
| BR2 | Each service has one login that owns `rwb_<name>` and holds no grant on another schema; the migration account is that service's login | Arch v5 slide 29; DP-02 | AC1, AC6; TC-PLT-E1044-APP2-01, TC-PLT-E1044-APP2-06 |
| BR3 | The schema is referenced only as `${schema}` and fed by `RWB_SCHEMA`; no migration file carries a literal schema name | DP-01; Arch v5 slide 29 | AC3; TC-PLT-E1044-APP2-03 |
| BR4 | The history table is Flyway's default `flyway_schema_history` inside the service's own schema; no shared history table across services | ADR-021; Arch v5 slide 29 | AC1, AC6; TC-PLT-E1044-APP2-01, TC-PLT-E1044-APP2-06 |
| BR5 | Each service has one `V0001` baseline that creates its own objects and is applied once per environment | DP-15 | AC1; TC-PLT-E1044-APP2-01 |
| BR6 | No cross-schema join, view or foreign key; a cross-schema reference fails the boundary test in every build | Arch v5 slide 29 notes | AC2; TC-PLT-E1044-APP2-02 |
| BR7 | One migration file per story per service, named `V<seq>__<story>_<name>.sql` with line 1 `-- Story: <story key>` | RWB-E1-044 build rule (D-RCV-28); RWB-PLT-E1044-CON | AC4; TC-PLT-E1044-APP2-04 |
| BR8 | Forward only in PROD and no edit of an applied file; the drift gate runs before SIT, UAT and PROD | RWB-E1-044 BR4, BR5, BR7; RWB-PLT-E1044-OPS | AC5; TC-PLT-E1044-APP2-05 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Pending | Service start | The version is next in the service's own sequence | Applied |
| Pending | Migration fails | A statement fails, or the checksum differs | Failed (rolled back, the service does not start) |
| Applied | Validation on start | The file and its checksum are unchanged | Applied |
| Applied | A fix is merged | A new version is added; the applied version is never edited | Pending (new version) |
| Applied | Drift found in the environment | An object is not produced by the migrations | Drift reported, deployment stopped |

The state of one service's sequence has no effect on the state of another service's sequence.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Configures `RWB_SCHEMA`, runs and reruns the migration of a service, reads the run on SCR-44 |
| RW-DATASTEW, data steward | Reads the migration runs (Platform administration R) |
| RW-AUDIT, internal audit | Reads the migration runs (Platform administration R) |
| Pipeline migration account of the service | Applies the migrations of that service with that service's login from the key store |
| ACE database administrator | Creates and grants the per-service login; not a Workbench role |

### 11. Data

No business field. The story writes the Flyway tool table `flyway_schema_history` inside each service's own schema; that table is not in the Logical Data Model. It reads the object list of the service's own schema from `information_schema` for the drift gate, and it reads nothing from another schema.

| Object | Type | Schema | Use | In LDM v9 |
|---|---|---|---|---|
| `flyway_schema_history` | Flyway tool table | Own service schema `rwb_<name>` | Migration history of the service | No; tool table outside the LDM |
| `information_schema` | Database catalog view | Not specified in the source documents (DOR-RWB-PLT-E1044-APP-2-7) | Object list for the drift gate | No; catalog view outside the LDM |

The migration-run record carries the service and the schema as its keys; its other fields are the legacy `Job` response of RWB-E1-044 until RWB-PLT-E1044-CON publishes the field list. Each service starts its sequence at `V0001` in its own folder `db/migration/<service>`; the 19 baselines have no cross-service order. The alert threshold and the owner of the drift feature flag `rwb.p3.migration-drift-gate` after the split are Not specified in the source documents (GAP-1423).

Field IDs are those in the Logical Data Model and Data Dictionary.

The migration contract document and the Flyway configuration module are owned by the platform template. Each service keeps only its folder `db/migration/<service>` and its `V0001` baseline.

### 12. Contract

#### 12.1 REST operations provided

None. The story provides no REST operation; the governing migration contract is published by RWB-PLT-E1044-CON.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/admin/jobs` | P1 rwb-source-data | Writes and reads one migration-run record per service run, with `type=MIGRATION` |

#### 12.3 Events published

None. A migration publishes no event; the outbox is not involved.

#### 12.4 Events consumed

None. A migration consumes no event.

#### 12.5 Workflows and activities

None. The run happens at service start, in the Flyway module of the service, not in a Temporal workflow or activity.

#### 12.6 Schedules

None. There is no schedule; the run is triggered by service start and by the pipeline step.

#### 12.7 Tables owned

None. The story owns no business table; Flyway creates `flyway_schema_history` in each service's own schema and that table is a tool table outside the Logical Data Model.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Migration fixture of RWB-PLT-E1044-CON | One valid parameter set per service and the six forbidden fixtures | The pipeline of every service, contract tests |
| P1 job view fake | `GET /api/recovery/source-data/v1/admin/jobs` answering one `Job` with `type=MIGRATION` and status APPLIED or FAILED | Component and integration tests of this story |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | 1 consumed | The P1 job view for the migration-run record |
| Kafka | None | No event is published or consumed |
| Temporal | None | The run is not a workflow |
| File | None | The migration files are read from the classpath of the service |

### 13. Solution plan

**Deliverables.** The Flyway module wiring in the platform template for one service, the per-service `V0001` baseline and migration folder, the lint, drift and boundary gates wired into the golden pipeline, and the run-record call to the P1 job view.

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

**Build steps**

1. Wire the Flyway module in the platform template with the properties of section 4 and the `${schema}` placeholder; prove a start applies one test migration in the service's own schema.
2. Add the per-service `V0001` baseline and the `db/migration/<service>` folder; prove the service's objects are created and no other schema receives an object.
3. Wire the lint with the six refusals of section 5 and test each refusal with a fixture.
4. Wire the boundary test and prove it fails on a cross-schema join, view or foreign key.
5. Wire the drift gate before SIT, UAT and PROD with the read-only account of the service.
6. Write the migration-run record through the P1 job view and show one record per service.
7. Prove two services migrate at the same time through their own logins and history tables, inside the connection cap.

**Done when.** The six test cases of section 16 pass for two services (rwb-case and rwb-payment), every service in the template applies its own `V0001` baseline in a clean container, and no build produces a cross-schema reference.

The order of the baselines and the sequence start across the 19 services, and the fields of the migration-run record, are Not specified in the source documents (GAP-1421; ASM-2489); the template takes `V0001` in each service and the legacy `Job` shape until the point is closed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-016 | Drift found, checksum mismatch, lint failure, a cross-schema reference, or a failed migration | Schema check failed in {schema}: {object}. The deployment was stopped. |
| MSG-P4-002 | A role without Platform administration R reads the migration runs | You cannot {action} here. Your role does not include it. |

MSG-P3-016 is the message of RWB-E1-044, carried unchanged; the schema and the object in the text are those of the service that owns the migration.

### 15. Screens and states

No new screen. SCR-44 Interface and job monitor shows one migration run per service through the P1 job view, in state Running, Failed or Complete, with the service, the schema, the version and the drift result. A run of one service never changes the state of another service's run.

Empty, loading, error and no access states: Not specified in the source documents (CG-ALL-1501).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1044-APP2-01 | AC1 | Contract | Two services with their own schema, login and `V0001`; history rows land in the own schema only |
| TC-PLT-E1044-APP2-02 | AC2 | Component | A cross-schema fixture; the boundary test fails and `rwb_payment` is unchanged |
| TC-PLT-E1044-APP2-03 | AC3 | Component | One file with `${schema}` in DEV and SIT; byte-for-byte equal, no literal schema |
| TC-PLT-E1044-APP2-04 | AC4 | Contract | Duplicate story key across two services and a file without a header; both refused |
| TC-PLT-E1044-APP2-05 | AC5 | Component | Undo file and a hand-added column; both refused |
| TC-PLT-E1044-APP2-06 | AC6 | Integration | Two services starting together in SIT; own logins, own history tables, inside the cap |

### 17. Guardrails

- One schema and one login per service: a migration writes only `rwb_<name>` and runs under that service's own login (DP-01, DP-02).
- No literal schema name in a migration or in a repository query; the schema is `${schema}` fed by `RWB_SCHEMA`.
- No cross-schema join, view or foreign key; a service holds another service's ID and asks the owner through its contract.
- No business value in a migration; seed values are reference loads (RWB-PLT-E1043-CON), never migration inserts.
- No personal data in a migration, a test or a log; no migration copies production rows.
- ACE data only through the P1 rwb-source-data contract or the `v_ace_*` views.
- Forward only: no clean, no undo file and no edit of an applied migration.
- No manual change in any environment; a hotfix is a new migration through the pipeline.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-RDF-001 | Recovery data held in 14 data products in the ACE database | Per-service schema `rwb_<name>`, per-service `V0001` baseline, per-service history table | TC-PLT-E1044-APP2-01, TC-PLT-E1044-APP2-03 | Not specified in the source documents (DOR-RWB-PLT-E1044-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-E1044-APP-2-2) |
| REQ-RDF-014 | Stage 2 data products exist before the first treatment goes live | Per-service baseline applied in each environment before the service starts | TC-PLT-E1044-APP2-01, TC-PLT-E1044-APP2-05 | Not specified in the source documents (DOR-RWB-PLT-E1044-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-E1044-APP-2-2) |
| ADR-021 | Per-service Flyway and migration ownership | One sequence, one login and one history table per service; boundary test on every build | TC-PLT-E1044-APP2-02, TC-PLT-E1044-APP2-04, TC-PLT-E1044-APP2-06 | Not specified in the source documents (DOR-RWB-PLT-E1044-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-E1044-APP-2-2) |

### 19. Out of scope

- The split of the 92 monolith tables into the 19 `rwb_<name>` schemas: that is RWB-PLT-NF06-DB and the per-service database stories of each service epic.
- The migration contract document, its fixtures and its contract tests (RWB-PLT-E1044-CON).
- The deployment pipeline, the drift gate scheduling, the key-store reading and the feature flag (RWB-PLT-E1044-OPS).
- The as-built monolith behaviour, kept word for word in RWB-PLT-E1044-APP.
- Seed reference data and dictionary changes (RWB-PLT-E1043-CON).
