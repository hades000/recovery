# RWB-P3-E1019-DB Roles, teams and queues as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1019-DB |
| Work type | DB (ACE DB) |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-H |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-008, FR-P3-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-019 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **ACE database engineer**, I want **the queue, queue membership, queue measure and reference tables of rwb-case created on the per-service Flyway sequence in schema `rwb_case`, with their keys, indexes, grants and a tested rollback, and with no foreign key into any other schema**, so that **the app story and the reference loads have a schema that is correct, granted, reversible and confined to the service's own schema**.

This is the database story of legacy RWB-E1-019. It delivers, in schema `rwb_case`:

- the migration that creates `queue_member` and `queue_measure` and adds `queue.table_version` (and `queue.rr_cursor_user_id` where the baseline does not already carry it), on the per-service sequence after the V0001 baseline (DP-15);
- the keys and indexes the legacy story names: the primary keys, the unique queue code, the two partial indexes on `queue_member` (`queue_id` where active, `user_id` where active), the overflow-queue foreign key inside the schema, and the measure index on `queue_id` and as-of;
- the grant script for the rwb-case login (DP-02), whose name is Not specified in the source documents (GAP-0678; ASM-1225);
- the rollback: the undo of each migration, in reverse order, with the queue rows and the queue IDs preserved;
- the assertion that the schema holds no foreign key into `rwb_access` or any other schema (DP-01), and that `role_code` and `team_code` are codes, not keys.

The reference tables `lov_value`, `reference_row` and `reference_version` are in the same schema and the same service, and their migration belongs to the reference-data story of the same legacy family. This story covers their key and index contract, extends the grant script to them, and creates nothing that the reference-data migration already creates — the sequencing is owned by RWB-PLT-E1044-CON.

### 2. Business rationale

The legacy story added one migration (`V019_1__queue_member.sql`) to a single recovery schema with 92 tables and one shared login. After the split, every service owns its schema, its migrations and its login, so a queue change and a reference-data change cannot collide with another service's release, and no service can read another's tables.

The queue tables carry the organization structure the case engines read on every allocation: if the schema is wrong, allocation, transfer and the case list are wrong. The indexes matter at the volumes the engines run at, when allocation sweeps every new case of the day and the case list reads depth and age per queue. The grants matter because the rwb-case login must be the only writer of the queue rows, and the absence of a cross-schema foreign key matters because a key into `rwb_access` would make one service's release block another's — the role code is checked over the rwb-access contract at load time, not by the database (DP-01, DP-08).

### 3. Preconditions

- The V0001 baseline of `rwb_case` exists on the per-service Flyway sequence, from RWB-PLT-E1044-CON and RWB-PLT-NF06-DB: the schema, the `flyway_schema_history` table and the standard record columns (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`) as defined in TSD P3 v3 T3.0.
- The ACE database and the per-service login policy are in place; the login of rwb-case is created by the platform DB work and its name is Not specified in the source documents (GAP-0678; ASM-1225).
- The ownership map is the only source of table ownership: `queue`, `queue_member`, `queue_measure`, `lov_value`, `reference_row`, `reference_version`, `assignment`, `task` and `recovery_case` are P3 and in `rwb_case`. `role`, `permission`, `masking_rule` and `delegation_limit` are P4 and in `rwb_access`, and no object of this story references them.
- The field identifiers are fixed by TSD P3 v3 T3.1: DF-WRK-001 to DF-WRK-008, DF-WRK-037, DF-WRK-038 for `queue`; DF-WRK-045 to DF-WRK-052 for `queue_member`; DF-RPT-020 to DF-RPT-030 for `queue_measure`; DF-REF-028 and DF-REF-029 for `lov_value`; DF-REF-159 to DF-REF-180 for `reference_version`; DF-REF-181 to DF-REF-184 for `reference_row`.
- The legacy story's physical statements are kept as the source of the new objects: `queue_member` (id, queue_id, user_id, capacity, skill_codes, table_version, valid_from, valid_to, standard columns; index on `(queue_id)` where `is_active`; index on `(user_id)` where `is_active`) and the added `queue.table_version`.
- No approval is required to run a Draft migration on a development database; the migration is released to SIT only after the tests in section 16 pass.

### 4. Flow

1. The ACE database engineer checks out the rwb-case migration folder and confirms the highest applied version on the sequence (the V0001 baseline).
2. The engineer adds the migration for this story after that version, with a repeatable check that the objects it creates do not already exist in the sequence.
3. The engineer writes the grant script for the rwb-case login, scoped to schema `rwb_case` and to the six tables of this legacy key, plus the sequence usage the tables need.
4. The engineer writes the rollback: the undo per migration, in reverse order, with data preservation for `queue` (a column drop only, never a table drop).
5. The migration pipeline applies the baseline and this story's migration to an empty schema, then to a copy of the SIT schema, and runs the schema checks: keys, indexes, grants, and a scan for any foreign key that names another schema.
6. The check for cross-schema keys is a query over the catalogue; any hit fails the build.
7. The rollback is exercised on a copy: the schema returns to its pre-migration shape, the `queue` rows keep their IDs and codes, and the `recovery_case.queue_id` values still resolve.
8. The migration is recorded in the release notes of the sequence, with its version number and its checksum.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | A migration runs before the V0001 baseline | Flyway refuses with an unresolved baseline and nothing is applied | Pipeline error, no message id |
| X2 | `queue_member` already exists in the sequence | The repeatable check refuses to re-create it; the migration is marked as already applied | Pipeline error, no message id |
| X3 | A foreign key names `rwb_access` or another schema | The catalogue check fails the build; the key is removed and the code is checked over the contract instead | Check finding, no message id |
| X4 | The grant script runs before the login exists | The script fails on the missing role; the platform DB story creates the login first | Database error, no message id |
| X5 | The grant script grants to a shared or legacy login | The review rejects the script: one login per service (DP-02) | Review finding, no message id |
| X6 | The rollback would drop `queue` and lose the queue IDs | The rollback drops only the added column; the table and its rows stay | Review finding, no message id |
| X7 | A column is needed but no field identifier exists | The column is not invented: it carries the placeholder and the gap is raised | GAP-0680 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Two migrations, one grant script and a rollback, on the service's own sequence; nothing to build against |
| Negotiable | Constraint and index names follow the platform naming library; the column set is fixed by the field identifiers |
| Valuable | The app story and the reference loads have a schema that is granted, indexed and reversible |
| Estimable | Five objects, six indexes, one grant script, one rollback |
| Small | Days, not weeks, with the schema checks |
| Testable | Every criterion is a catalogue query or a pipeline run in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: rwb_case schema for queues, queue membership, queue measures and reference data

  Background:
    Given the rwb-case schema is rwb_case and the baseline version is V0001
    Given the grantee is the rwb-case login (DP-02), whose name is Not specified in the source documents (GAP-0678; ASM-1225)

  Scenario: AC1 The migrations apply in sequence on an empty schema (new, D-RCV-60)
    Given an empty rwb_case schema with the V0001 baseline applied
    When this story's migration and grant script run in order
    Then each migration is recorded once on the service's Flyway history with its version and checksum
    Then a second run of the same pipeline changes nothing and reports no pending migration
    Then no migration in this story reuses a monolith migration name

  Scenario: AC2 queue_member is created with its keys and partial indexes (new, D-RCV-60)
    Given the migration for this story
    When it is applied
    Then queue_member has the columns of DF-WRK-045 to DF-WRK-052 plus the standard record columns
    Then the primary key is on id and queue_id carries a foreign key to queue
    Then a partial index on queue_id where is_active exists and a partial index on user_id where is_active exists
    Then table_version and valid_from are NOT NULL

  Scenario: AC3 queue carries the version column and its keys (new, D-RCV-60)
    Given the queue table of the baseline
    When the migration is applied
    Then queue has table_version and the round-robin cursor column of DF-WRK-037
    Then the primary key is on id and queue_code is unique
    Then overflow_queue_id carries a foreign key to queue inside the same schema
    Then the existing queue rows keep their id and queue_code values

  Scenario: AC4 queue_measure is created with its columns and index (new, D-RCV-60)
    Given the migration for this story
    When it is applied
    Then queue_measure has the columns of DF-RPT-020 to DF-RPT-030 plus the standard record columns
    Then depth, unassigned, breached and status are NOT NULL and as_of is NOT NULL
    Then queue_id carries a foreign key to queue and an index on queue_id and as_of exists

  Scenario: AC5 No object of rwb_case names another schema (new, D-RCV-60)
    Given the applied schema
    When the catalogue query for foreign keys runs
    Then no foreign key in rwb_case references a table in rwb_access or in any other schema
    Then role_code and team_code are code columns with no foreign key, checked over the rwb-access contract at load time
    Then no view, synonym or grant in this story names another schema

  Scenario: AC6 The grants and the rollback are complete and safe (new, D-RCV-60)
    Given the grant script and the rollback of this story
    When the grant script runs and then the rollback runs on a copy
    Then the rwb-case login has usage on the schema and select, insert, update and delete on the six tables of this legacy key
    Then no other login holds a grant on those tables and no grant on rwb_access is present
    Then the rollback drops queue_member, queue_measure and the added queue columns in reverse order
    Then the queue rows keep their id and queue_code, and the recovery_case.queue_id values still resolve
```

These criteria are new and test the database artefacts only: no legacy acceptance criterion is repeated, and every physical value (table, column, field identifier, index definition) is the legacy or technical-specification value, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every queue belongs to one team code and one role code, and both are codes, not keys into another schema | Legacy BR1; DF-WRK-004, DF-WRK-005; DP-01 |
| BR2 | The queue record ID never changes, so `recovery_case.queue_id` stays valid across a version apply and a rollback | Legacy BR3; A version applies whole or not at all |
| BR3 | A member row is active for a date range and is replaced, not updated in place, by a new version | DF-WRK-050 to DF-WRK-052 |
| BR4 | The capacity cap range of 1 to 500 is checked by the application parameter `queue.cap.max`, not by a database check constraint with a literal | Legacy BR8; DP-06 |
| BR5 | A queue may overflow to at most one other queue, and the overflow queue is a queue row | DF-WRK-008; TSD P3 v3 T3.3 |
| BR6 | A measure snapshot belongs to one queue and carries its status from LOV-SNAPSHOT-STATUS | DF-RPT-030; LOV-SNAPSHOT-STATUS |
| BR7 | Each service's objects live in its own schema under its own login; one login per service | DP-01, DP-02, DP-15 |
| BR8 | The roles, permissions, masking and delegation table are rwb-access objects and are never referenced by a key here | DP-01, DP-08; ownership map |

### 9. State transitions

None in the runtime sense: a table has no state machine. The states this story moves through are the migration states of the service's Flyway history (pending, applied, failed, undone), and the table-level states the schema exposes are the standard record columns of TSD P3 v3 T3.0: `is_active` and `state` on every row, plus the version states that `reference_version.status` carries (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) and the measure states of `queue_measure.status` (TAKEN, PUBLISHED, HELD).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The ACE database engineer (any team, per U3) | Writes and runs the migrations, the grant script and the rollback |
| The service owner of rwb-case | Approves a destructive change; none is planned here |
| The platform DB owner (RWB-PLT-E1044-CON, RWB-PLT-NF06-DB) | Owns the sequence, the baseline and the login policy |
| rwb-access (P4) | Owns the role and permission tables; this schema holds no key to them |
| No delegation of authority level applies | A schema change is not a credit decision |

The grantee is named only as the rwb-case login (DP-02); its name is Not specified in the source documents (GAP-0678; ASM-1225). No personal name and no credential appears in a migration, a script or a runbook.

### 11. Data

| Table | Schema | Field identifiers | This story |
|---|---|---|---|
| queue | rwb_case | DF-WRK-001 to DF-WRK-008, DF-WRK-037, DF-WRK-038 | Adds `table_version` and, where absent, the round-robin cursor; primary key, unique queue code, overflow-queue key |
| queue_member | rwb_case | DF-WRK-045 to DF-WRK-052 | Creates the table, its key and its two partial indexes |
| queue_measure | rwb_case | DF-RPT-020 to DF-RPT-030 | Creates the table, its key and its index |
| lov_value | rwb_case | DF-REF-028 (`lov_code`), DF-REF-029 (`value_code`); the remaining columns are Not specified in the source documents (GAP-0680; ASM-1227) | Covers the unique key on the two given columns and the grant; creates no duplicate of the reference-data migration |
| reference_row | rwb_case | DF-REF-181 to DF-REF-184 | Covers the key to `reference_version` and the grant |
| reference_version | rwb_case | DF-REF-159 to DF-REF-180 | Covers the unique key on table code and version number, the index on valid from, and the grant |
| assignment, task | rwb_case | DF-WRK-009 to DF-WRK-016, DF-WRK-039, DF-WRK-040; DF-WRK-017 to DF-WRK-026 | Read dependencies only: their keys on `queue_id` and `case_id` are created by their own stories |
| recovery_case | rwb_case | DF-CAS-005, DF-CAS-009, DF-CAS-010 | Read dependency: `ix_case_owner_status` is created by the case story, not here |
| role, permission, masking_rule, delegation_limit | rwb_access | — | **Not created and not referenced.** P4 owns them (DP-01); the column-level split of the legacy role and permission tables between the two services is not stated by any source (GAP-0679; ASM-1226) |

The measure column order and the remaining list columns are the two places where no source fixes every value; both carry the placeholder above rather than an invented name.

### 12. Contract

**12.1 REST operations provided**

None. This is a database story and publishes no operation.

**12.2 REST operations consumed**

None.

**12.3 Events published**

None.

**12.4 Events consumed**

None.

**12.5 Workflows and activities**

None.

**12.6 Schedules**

None. The migration runs in the release pipeline, not on a Temporal Schedule.

**12.7 Tables owned**

| Table | Owner (ownership map) | Created or altered here | Keys and indexes |
|---|---|---|---|
| queue | P3 | Altered: `table_version` (DF-WRK-038) and, where absent, `rr_cursor_user_id` (DF-WRK-037) | PK on id; unique on queue_code; index on team_code and role_code; foreign key overflow_queue_id to queue |
| queue_member | P3 | Created | PK on id; foreign key queue_id to queue; partial index on queue_id where is_active; partial index on user_id where is_active |
| queue_measure | P3 | Created | PK on id; foreign key queue_id to queue; index on queue_id and as_of |
| lov_value | P3 | Covered, not duplicated | Unique on list code and value code (DF-REF-028, DF-REF-029) |
| reference_row | P3 | Covered, not duplicated | PK on id; foreign key version_id to reference_version |
| reference_version | P3 | Covered, not duplicated | PK on id; unique on table code and version number (DF-REF-160, DF-REF-161); index on valid_from (DF-REF-163) |
| role, permission, masking_rule, delegation_limit | P4 | Not touched | None here; the schema holds no key to `rwb_access` |

**12.8 Contract fakes**

None. A database story uses no contract fake; it is tested against an empty schema and a copy of the SIT schema.

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic in this story |
| Temporal | None | None | No workflow or schedule |
| File | None | None | Migrations are deployed by the release pipeline, not by a file interface |

### 13. Solution plan

**Sequencing.** The service's Flyway sequence is owned by RWB-PLT-E1044-CON. The V0001 baseline creates the schema, the history table and the standard columns. This story adds the next versions after the baseline:

| Version | File | Contents |
|---|---|---|
| V0001 | baseline, from the platform DB story | Schema `rwb_case`, history table, standard columns |
| next after the baseline | `..._queue_member_queue_measure.sql` | Creates `queue_member` and `queue_measure`; adds `queue.table_version` and, where absent, `queue.rr_cursor_user_id` |
| next after that | `..._queue_reference_grants.sql` | Usage on the schema and the table grants for the rwb-case login |

The legacy migration name `V019_1__queue_member.sql` is recorded as the source of the `queue_member` object; the monolith name and number are not reused on the service sequence. The exact version numbers are assigned by the sequence owner at build time; the order above is fixed by this story.

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Table definitions**

`queue_member` — `id` uuid NOT NULL, `queue_id` uuid NOT NULL, `user_id` uuid NOT NULL, `capacity` integer NULL, `skill_codes` varchar(200) NULL, `table_version` integer NOT NULL, `valid_from` date NOT NULL, `valid_to` date NULL, plus the standard record columns of TSD P3 v3 T3.0. Primary key `(id)`; foreign key `queue_id` to `queue(id)`; partial index on `(queue_id)` where `is_active`; partial index on `(user_id)` where `is_active`.

`queue_measure` — `id` uuid NOT NULL, `queue_id` uuid NOT NULL, `as_of` timestamptz NOT NULL, `depth` integer NOT NULL, `unassigned` integer NOT NULL, `avg_age_days` numeric(7,2) NULL, `max_age_days` integer NULL, `owner_min` integer NULL, `owner_max` integer NULL, `breached` integer NOT NULL, `status` varchar(15) NOT NULL, plus the standard record columns. Primary key `(id)`; foreign key `queue_id` to `queue(id)`; index on `(queue_id, as_of)`.

`queue` — the baseline table gains `table_version` integer NULL (DF-WRK-038) and, where absent, `rr_cursor_user_id` uuid NULL (DF-WRK-037). Primary key `(id)`, unique `(queue_code)`, index on `(team_code, role_code)`, foreign key `overflow_queue_id` to `queue(id)`.

**No cross-schema key.** `role_code` and `team_code` are `varchar(20)` codes with no foreign key. The roles live in `rwb_access` and are checked over the rwb-access contract at load time (DP-01, DP-08). A catalogue query for foreign keys that name another schema is part of the pipeline.

**Grants.** `GRANT USAGE ON SCHEMA rwb_case TO <the rwb-case login>`; `GRANT SELECT, INSERT, UPDATE, DELETE ON queue, queue_member, queue_measure, lov_value, reference_row, reference_version TO <the rwb-case login>`; usage on the sequences those tables own. No grant to a shared login, no grant to another service's login, and no grant on `rwb_access`. The grantee name is Not specified in the source documents (GAP-0678; ASM-1225); the reference-data and parameter migrations of the same service grant to the same login.

**Rollback.** Per migration, in reverse order: the grant script is reversed by revoking the grants it made; the object migration is reversed by dropping the partial indexes, dropping `queue_measure`, dropping `queue_member`, and dropping the added `queue` columns. `queue` itself is never dropped and `queue_code` is never rewritten, so the queue IDs and `recovery_case.queue_id` survive a rollback (BR2). The rollback is exercised on a copy of the SIT schema and recorded in the runbook.

**Done when.** The migrations apply twice without a change, the catalogue checks pass, the grants are exactly as above, the rollback returns the schema to its pre-migration shape with the queue rows intact, and the tests in section 16 pass.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Database error, no message id | A migration runs before the baseline or finds an object already present | The migration fails and nothing is applied; the pipeline stops |
| Database error, no message id | A grant script runs before the login exists | The script fails on the missing role; the platform DB story creates the login first |
| Check finding, no message id | A foreign key names another schema | The pipeline check fails the build; the key is removed |
| MSG-GEN-001 | A reference load reaches the database with a NOT NULL column empty | Enter {field}. Raised by the application, not by a database constraint |
| MSG-GEN-002 | A reference load reaches the database with a cap outside 1 to 500 | {field} must be between {min} and {max}. Raised by the application from the parameter `queue.cap.max` |

The two business checks that a reader might expect as database constraints are deliberately in the application: the cap range comes from the parameter (DP-06) and the row-level load checks come from the reference registry (DP-07), so a business person can change them without a migration. The database enforces what does not change: keys, uniqueness, dates and the schema boundary. Messages and their IDs are the legacy ones and are raised by the app story.

### 15. Screens and states

No screen. The result of a migration is visible in the release pipeline and in the service's Flyway history: pending, applied, failed, undone, each with a version and a checksum. The tables expose the standard record columns and the version and measure states listed in section 9; nothing here is shown to a user directly, and SCR-42 in Epic 8 reads the tables through the rwb-case operations, never through SQL.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1019-DB-01 | AC1 | Component | Empty schema with V0001; this story's migrations; a second run; the Flyway history compared |
| TC-P3-E1019-DB-02 | AC2 | Component | queue_member catalogue: columns, NOT NULL, primary key, foreign key, the two partial indexes |
| TC-P3-E1019-DB-03 | AC3 | Component | queue before and after: two added columns, unique queue_code, self foreign key, row identities compared |
| TC-P3-E1019-DB-04 | AC4 | Component | queue_measure catalogue: DF-RPT-020 to DF-RPT-030, NOT NULL set, foreign key, index on queue_id and as_of |
| TC-P3-E1019-DB-05 | AC5 | Component | Catalogue query over rwb_case foreign keys; the role and team code columns; the reference tables' keys |
| TC-P3-E1019-DB-06 | AC6 | Component | Grant script and rollback on a copy of the SIT schema; grants listed per login; queue rows and queue IDs after the rollback |

### 17. Guardrails

- No business value in a constraint: the cap range and the row checks are application data, read from the parameter and the reference contracts (DP-06, DP-07).
- No personal data in a migration, a script, a test fixture or a runbook: members appear as user IDs only.
- No read of another schema and no key into another schema: `rwb_case` objects reference `rwb_case` objects only (DP-01).
- One login per service: the rwb-case login is the only grantee, and its name is Not specified in the source documents (GAP-0678; ASM-1225).
- No destructive change: no table drop of `queue`, no rewrite of `queue_code`, so the queue IDs that cases point at are never lost (BR2).
- The sequence is per service and linear: no monolith migration name is reused and no object is created twice (DP-15).
- No table of rwb-access is created, granted or referenced from here (DP-08).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-CWC-006 | Roles, teams, queues, membership and capacity as versioned data | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-06 | R-UNI-38 | TC-P3-E1019-DB-01 to TC-P3-E1019-DB-06 |
| REQ-ACA-002 | Roles held as data; a change without a release | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-03 | None | TC-P3-E1019-DB-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1019-APP | App development | X dependency tracked: the story that writes these tables |
| RWB-P3-E1019-CON | Contract | Sibling: the schema baseline in its section 12 must match this story |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence and its version allocation |
| RWB-PLT-NF06-DB | ACE DB | The schema split and the baseline of `rwb_case` |
| RWB-P3-E1043-CON | Contract | The reference-data migration that creates the three reference tables |

### 19. Out of scope

- The application code, the checks, the applier and the read interfaces: RWB-P3-E1019-APP.
- The test data set and the SIT queue set: the app story and the test pack.
- The role, permission, masking and delegation tables: rwb-access (P4).
- The parameter tables `parameter_catalog` and `parameter_value`: the E1-042 stories.
- The `assignment`, `task` and `recovery_case` tables and their indexes: their own P3 stories.
- The reference-data migration itself and its version store logic: the reference-data story of RWB-E1-043.
- Performance tuning beyond the indexes named here: the non-functional work.
