# RWB-P4-E1022-DB Sign-on with SSO, MFA and the first roles

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: database slice split from RWB-E1-022 for rwb-access — the role, permission and conflict tables, the library objects, the login and the grants in `rwb_access`, with no session, password or token in the schema. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 19 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E1022-DB |
| Work type | DB (ACE DB) |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | To be sized by the squad at refinement; Small means it fits two weeks |
| Patterns applied | DP01, DP03, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P4-S |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (path /v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-001, FR-P4-002, FR-P4-003, FR-P4-004, FR-P4-006, FR-P4-007, FR-P4-019, FR-P4-033, FR-P4-035, FR-P4-037) |
| Status | Draft (directive resolutions) |

### 1. Story

As an **ACE database engineer**, I want **the role, permission and conflict tables of this key created on the per-service Flyway sequence in schema `rwb_access`, with the library objects the event platform needs in that schema, the login and grants of the service, a tested rollback, and an explicit statement that the schema holds no session, no password, no token and no local account**, so that **the sign-on story has a schema that is correct, granted, reversible and confined to the service's own schema, and nobody looks for a Workbench credential that does not exist**.

This is the database story of legacy RWB-E1-022. It delivers, in schema `rwb_access`:

- the migration that creates `role`, `permission` and `role_conflict` after the V0001 baseline, on the per-service sequence (DP-15);
- the keys and indexes this key's sign-in needs: the primary keys, the unique role code, the partial index on `role.entra_group` where `is_active` that the resolution reads on every sign-in, the unique key on `permission` per role, area and matrix version, and the unique key on the conflict pair per conflict version;
- the three library objects `outbox_event`, `processed_event` and `idempotency_key` created in this schema from the template of the event platform, because every service writes its own outbox and inbox in its own schema (DP-09's library, applied per service);
- the grant script for the rwb-access login (DP-02), whose name is Not specified in the source documents (GAP-0777; ASM-1405);
- the rollback: the undo of each migration, in reverse order, with the role and matrix rows preserved where a later migration only added a column;
- the explicit statement, in the migration and in the tests, that the schema holds **no session table, no password column, no token column and no local account row**: staff sign-in is ACE Common through gateway-bff, with the session in the gateway's Redis store (RWB-PLT-N006-INF; ADR-010);
- the statement that the ACE group facts behind a mapping row are read through the P1 contract or `RWB-P1-E1069-APP`, never from a table or view of the ACE schema and never from `public.*`.

`role` is written by the role story of this service, `permission` by the permission-matrix story, and this key's sign-in reads all three. This story creates the objects and the grants and writes no business row at run time.

### 2. Business rationale

The legacy story added one migration, `V_E1_022__role_conflict.sql`, to a single recovery schema of 92 tables with one shared login, and it relied on `role` and `permission` having been created by RWB-E1-001. After the split every service owns its schema, its migrations and its login, so the three tables that decide who may see a case cannot be changed by another service's release, and no other service can read them: the roles are read over the published contract of this key, one hop away (DP-01, DP-08; Architecture v5 slides 10 and 29).

Three details make the schema a design statement and not only plumbing. The partial index on `role.entra_group` where the row is active is what makes the resolution a lookup on a small index at every sign-in, and it is the legacy index kept exactly. The absence of a session table, a password column and a token column is not an omission: the target has no Workbench credential at all, the identity is ACE Common's and the session is gateway-bff's, so a schema that grew one would be the one place where the architecture could quietly be undone (ADR-010; Architecture v5 slide 35). And the three library objects must exist in this schema before the service can publish any event or consume one idempotently, which is why the event platform's template is applied here and not left to a story that owns no schema.

Where no source fixes a value this story depends on, it carries the placeholder: the name of the rwb-access login, the source of the ACE group facts behind a mapping row, and the column set of the three library objects — Not specified in the source documents (GAP-0777; ASM-1405), (GAP-0777; ASM-1406) and (GAP-0777; ASM-1407).

### 3. Preconditions

- The V0001 baseline of `rwb_access` exists on the per-service Flyway sequence, from RWB-PLT-E1044-CON and RWB-PLT-NF06-DB: the schema, the `flyway_schema_history` table and the standard record columns of TSD P4 v3 T3.0 (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`).
- The ACE database and the per-service login policy are in place; the grant goes to the login `rwb_access`, the section R4 pattern, and the platform DB work sets its connection pool (ASM-1405).
- The ownership map is the only source of table ownership: `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` are P4 and in `rwb_access`; `lov_value`, `reference_row` and `reference_version` are P3 and in `rwb_case`; the ACE views are P1's. This story creates no object of another service.
- The field identifiers are fixed by TSD P4 v3 T3.1: DF-REF-034 to DF-REF-039 for `role`, DF-REF-040 to DF-REF-044 for `permission`, DF-REF-205 to DF-REF-211 for `role_conflict`.
- The legacy physical statements are the source of the objects: the `role` columns with `entra_group varchar(120)` and the partial index `ix_role_entra_group` on `(entra_group)` where `is_active`; the `permission` columns with `letters varchar(5)` and `matrix_version`; and `role_conflict` with `id uuid, role_code varchar(20), conflicts_with varchar(30), reason varchar(200), conflict_version varchar(20), valid_from date, valid_to date` plus the standard columns.
- The three library objects follow the template of the event platform (RWB-PLT-TE006-CON) unchanged; their column set is the template's column set (ASM-1407).
- The ACE group facts behind a mapping row — `v_ace_iam_group.entra_group` in FSD P4 v3 — are read through the P1 contract or `RWB-P1-E1069-APP`; the mapping rows stay in `role.entra_group`, with TSD P4 v3 taking precedence over FSD P4 v3 under R-PREC. No object of this schema reads an ACE schema, the `recovery` schema or `public`.
- No approval is required to run a Draft migration on a development database; the migration is released to SIT only after the tests in section 16 pass.

### 4. Flow

1. The ACE database engineer checks out the rwb-access migration folder and confirms the highest applied version on the sequence (the V0001 baseline).
2. The engineer adds the migration for this story after that version, with a repeatable check that the objects it creates do not already exist in the sequence.
3. The engineer creates `role`, `permission` and `role_conflict` with their columns from DF-REF-034 to DF-REF-039, DF-REF-040 to DF-REF-044 and DF-REF-205 to DF-REF-211, plus the standard record columns.
4. The engineer adds the keys and indexes: the primary key on each table, the unique role code, the partial index on `entra_group` where `is_active`, the unique key on `permission` per role, area and matrix version, and the unique key on the conflict pair per conflict version.
5. The engineer applies the event platform's template for `outbox_event`, `processed_event` and `idempotency_key` in `rwb_access`, unchanged: this schema is the producer's and the consumer's own, so the outbox and the inbox live here (DP-09's library, per service).
6. The engineer writes the grant script for the rwb-access login, scoped to schema `rwb_access` and to the six tables of this key, plus the sequence usage the tables need.
7. The engineer writes the rollback: the undo per migration, in reverse order, with data preservation for `role` and `permission` where a later change only adds a column.
8. The pipeline applies the baseline and this story's migrations to an empty schema, then to a copy of the SIT schema, and runs the schema checks: keys, indexes, grants, and a scan for any foreign key, synonym, view or grant that names another schema or `public`.
9. The check that no session, password, token or local-account column exists is a catalogue query over the schema: any hit fails the build (ADR-010).
10. The rollback is exercised on a copy: the schema returns to its pre-migration shape, and the role and matrix rows that were loaded between the two runs keep their identifiers.
11. The migration is recorded in the release notes of the sequence, with its version number and its checksum.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A migration runs before the V0001 baseline | Flyway refuses with an unresolved baseline and nothing is applied | Pipeline error, no message id | AC1 |
| X2 | `role`, `permission` or `role_conflict` already exists in the sequence | The repeatable check refuses to re-create it; the migration is marked as already applied | Pipeline error, no message id | AC1 |
| X3 | A foreign key, view, synonym or grant names another schema or `public` | The catalogue check fails the build; the object is removed and the value is read over a contract instead | Check finding, no message id | AC6 |
| X4 | The grant script runs before the login exists | The script fails on the missing role; the platform DB story creates the login first | Database error, no message id | AC7 |
| X5 | The grant script grants to a shared or legacy login | The review rejects the script: one login per service (DP-02) | Review finding, no message id | AC7 |
| X6 | A session, password, token or local-account column appears in the schema | The catalogue check fails the build and the column is removed: the identity and the session are not this schema's (ADR-010) | Check finding, no message id | AC6 |
| X7 | The rollback would drop `role` and lose the role identifiers the matrix rows point at | The rollback drops only what the migration added and keeps the table and its rows | Review finding, no message id | AC7 |
| X8 | A column is needed but no field identifier exists | The column is not invented: it carries the placeholder and the gap is raised | GAP-0777 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Three migrations, one grant script and a rollback, on the service's own sequence; nothing to build against |
| Negotiable | Constraint and index names follow the platform naming library; the column set is fixed by the field identifiers and the legacy statements |
| Valuable | The sign-on story, the role story and the matrix story have a schema that is granted, indexed, reversible and free of any credential |
| Estimable | Six tables, five indexes and keys, one grant script, one rollback |
| Small | Days, not weeks, with the schema checks |
| Testable | Every criterion is a catalogue query or a pipeline run in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: rwb_access schema for roles, permissions, conflicts and the event library

  Background:
    Given the rwb-access schema is rwb_access and the baseline version is V0001
    Given the grantee is the rwb-access login (DP-02), whose name is Not specified in the source documents (GAP-0777; ASM-1405)

  Scenario: AC1 The migrations apply in sequence on an empty schema (new, D-RCV-60)
    Given an empty rwb_access schema with the V0001 baseline applied
    When this story's migrations and grant script run in order
    Then each migration is recorded once on the service's Flyway history with its version and checksum
    Then a second run of the same pipeline changes nothing and reports no pending migration
    Then no migration in this story reuses the monolith migration name V_E1_022__role_conflict.sql

  Scenario: AC2 role is created with its columns, keys and the sign-in index (new, D-RCV-60)
    Given the migration for role
    When it is applied
    Then role has id, role_code, role_name, role_class, default_scope and entra_group of DF-REF-034 to DF-REF-039 plus the standard record columns
    Then the primary key is on id, role_code is unique, and role_class, default_scope and role_code are NOT NULL
    Then a partial index ix_role_entra_group exists on entra_group where is_active
    Then entra_group is varchar(120) and nullable, because a row holds no group in an environment where no group is mapped

  Scenario: AC3 permission is created and is read only by this key's sign-in (new, D-RCV-60)
    Given the migration for permission
    When it is applied
    Then permission has id, role_id, capability_area, letters and matrix_version of DF-REF-040 to DF-REF-044 plus the standard record columns
    Then the primary key is on id and role_id carries a foreign key to role inside the same schema
    Then a unique key exists on role_id, capability_area and matrix_version
    Then letters is varchar(5) and matrix_version is varchar(20) and both are NOT NULL

  Scenario: AC4 role_conflict is created with its columns and its version key (new, D-RCV-60)
    Given the migration for role_conflict, the legacy V_E1_022__role_conflict.sql of RWB-E1-022
    When it is applied
    Then role_conflict has id, role_code, conflicts_with, reason, conflict_version, valid_from and valid_to of DF-REF-205 to DF-REF-211 plus the standard record columns
    Then the primary key is on id and a unique key exists on role_code, conflicts_with and conflict_version
    Then conflicts_with is varchar(30), because it holds a role code or the class value ANY_BUSINESS_ROLE or ANY_OTHER_ROLE, and no check constraint carries those values
    Then valid_from is NOT NULL and valid_to is nullable

  Scenario: AC5 The three library objects exist in rwb_access from the event platform template (new, D-RCV-60)
    Given the event platform template published by RWB-PLT-TE006-CON
    When this story's migration for the library objects is applied
    Then outbox_event, processed_event and idempotency_key exist in schema rwb_access
    Then each object is created from the template unchanged, with no column renamed, added or dropped in this story
    Then the three objects carry their own keys and no foreign key into role, permission or role_conflict
    Then no other schema holds this service's outbox or inbox row

  Scenario: AC6 The schema holds no session, password, token or local account, and no object names another schema (new, D-RCV-60)
    Given the applied schema
    When the catalogue query for columns, foreign keys, views, synonyms and grants runs
    Then no table, column or row holds a session, a password, a token or a local account, because staff sign-in is ACE Common through gateway-bff and the session lives in the gateway's Redis store (RWB-PLT-N006-INF; ADR-010)
    Then no foreign key, view, synonym or grant in rwb_access names rwb_case, the recovery schema, an ACE schema or public
    Then the ACE group facts behind a mapping row are read through the P1 contract or RWB-P1-E1069-APP and never by SQL from this schema
    Then the only grantee of the six tables is the rwb-access login

  Scenario: AC7 The grants and the rollback are complete and safe (new, D-RCV-60)
    Given the grant script and the rollback of this story
    When the grant script runs and then the rollback runs on a copy
    Then the rwb-access login has usage on the schema and select, insert, update and delete on role, permission, role_conflict, outbox_event, processed_event and idempotency_key
    Then no other login holds a grant on those tables, and no grant on rwb_case or on an ACE schema is present
    Then the rollback drops the library objects, then role_conflict, then permission, then role, in reverse order
    Then a role row loaded between the two runs keeps its id and role_code where the rollback only reverses an added object

  Scenario: AC8 Each business rule of section 8 holds in the applied schema (new, D-RCV-60)
    Given the applied schema and the rules BR1 to BR9 of section 8
    When the schema checks of AC2 to AC7 run
    Then BR1: the lookup of a role by its group is the indexed entra_group column of role
    Then BR2: permission holds one letter set per capability area and matrix version, and no inheritance column exists
    Then BR3: a conflicting pair is held once per conflict version and valid_from
    Then BR4: no check constraint carries a business value
    Then BR5: the objects are in rwb_access under the rwb-access login only
    Then BR6: no session, password, token or local account exists
    Then BR7: outbox_event, processed_event and idempotency_key exist in rwb_access
    Then BR8: no object names another schema or public
    Then BR9: the rollback keeps every role, permission and conflict identifier
```

These criteria are new and test the database artefacts only: no legacy acceptance criterion is repeated, and every physical value — table, column, field identifier, index definition and the legacy migration name — is the legacy or technical-specification value, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Membership of the Entra ID group mapped to a role is the only way to hold the role, so the mapping is a column of `role` and its lookup is indexed | role.entra_group (DF-REF-039); Legacy BR1; DT07 |
| BR2 | One role has one letter set per capability area at a matrix version, and no role inherits from another | permission.letters (DF-REF-043); DF-REF-044; Legacy BR3 |
| BR3 | A role pair listed as a conflict may not be held in one session, and the pair is versioned by the conflict version and its valid from date | role_conflict (DF-REF-205 to DF-REF-211); Legacy BR5 |
| BR4 | Group names, roles, letters, conflicts and versions are rows; no database check constraint carries a business value | Legacy BR8; Principle 1; DT02 |
| BR5 | Each service's objects live in its own schema under its own login; one login per service | DP-01, DP-02, DP-15; Architecture v5 slide 29 |
| BR6 | The schema holds no session, no password, no token and no local account; the identity is ACE Common's and the session is the gateway's | ADR-010; Architecture v5 slide 35 |
| BR7 | Every service writes its own outbox and inbox in its own schema, so the three library objects are created here | Ownership Map ruling on outbox_event, processed_event and idempotency_key; Architecture v5 slides 11 and 20 |
| BR8 | The ACE group facts are read through the owner's contract and never by SQL from this schema, and no object names `public` | DP-01; DP-05's boundary rule; FSD P4 v3 A2.1 |
| BR9 | A role, a permission row and a conflict pair keep their identifiers across a rollback, so a later migration never rewrites a key | Legacy BR3; version applies whole or not at all |

### 9. State transitions

None in the runtime sense: a table has no state machine. The states this story moves through are the migration states of the service's Flyway history — pending, applied, failed, undone — and the row-level states the schema exposes are the standard record columns of TSD P4 v3 T3.0: `is_active` and `state` on every row, plus the validity window of a conflict pair (`valid_from`, `valid_to`). The sign-on states of a session — RESOLVED and REFUSED — are the app story's and leave no row here, because the schema holds no session.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The ACE database engineer (any team, per U3) | Writes and runs the migrations, the grant script and the rollback |
| The service owner of rwb-access | Approves a destructive change; none is planned here |
| The platform DB owner (RWB-PLT-E1044-CON, RWB-PLT-NF06-DB, RWB-PLT-N011-DB) | Owns the sequence, the baseline, the login policy and the connection pool per login |
| RW-SECADM Security administrator | Owns the role-to-group mapping rows the schema stores, under RWB-P4-AD001-CON; loads none of them here |
| RW-REFADM Reference data administrator | Loads an approved role or matrix version through the service's operations, never through SQL |
| No delegation of authority level applies | A schema change is not a credit decision |

The grantee is named only as the rwb-access login (DP-02); its name is Not specified in the source documents (GAP-0777; ASM-1405). No personal name and no credential appears in a migration, a script or a runbook.

### 11. Data

| Table | Schema | Field identifiers | This story |
|---|---|---|---|
| role | rwb_access | DF-REF-034 to DF-REF-039 | Creates the table, the unique role code and the partial index `ix_role_entra_group` on `entra_group` where `is_active` |
| permission | rwb_access | DF-REF-040 to DF-REF-044 | Creates the table, the foreign key to `role`, the unique key per role, area and matrix version; the sign-in of this key reads it and writes none of it |
| role_conflict | rwb_access | DF-REF-205 to DF-REF-211 | Creates the table, the unique key per role, conflicting value and conflict version; the legacy `V_E1_022__role_conflict.sql` is its source |
| outbox_event | rwb_access | No field identifier in this read set (GAP-0777; ASM-1407) | Creates the object from the event platform template, unchanged |
| processed_event | rwb_access | No field identifier in this read set (GAP-0777; ASM-1407) | Creates the object from the event platform template, unchanged |
| idempotency_key | rwb_access | No field identifier in this read set (GAP-0777; ASM-1407) | Creates the object from the event platform template, unchanged |
| masking_rule, delegation_limit | rwb_access | DF-REF-198 to DF-REF-204; DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 | **Not created here**: P4 owns them and their migrations are the masking and delegation stories' |
| lov_value, reference_row, reference_version | rwb_case | DF-REF-027 to DF-REF-033; DF-REF-181 to DF-REF-184; DF-REF-159 to DF-REF-180 | **Not created and not referenced.** P3 owns them (DP-07); the values arrive over the reference-data contract |
| v_ace_iam_group | ACE, behind P1 | The `entra_group` value; the column set is not in this read set (GAP-0777; ASM-1406) | **Not read by SQL.** The group facts arrive through the P1 contract or RWB-P1-E1069-APP; FSD P4 v3 names the view while the mapping rows stay `role.entra_group` data |
| No session, no password, no token, no local account | — | Not specified in the source documents (DOR-RWB-P4-E1022-DB-7) | **None, by design.** The session is gateway-bff's in its Redis store (RWB-PLT-N006-INF); the identity is ACE Common's (ADR-010) |

Field IDs are those in the Logical Data Model and Data Dictionary. The three library objects carry no field identifier in this read set, so this story applies the published template and restates none of its columns. FSD P4 v3 reads the group mapping from `v_ace_iam_group`, while the legacy story and the mapping contract keep the mapping rows in `role.entra_group`; this story keeps `role.entra_group` as the mapping row and takes the ACE group facts only over the P1 contract.

### 12. Contract

#### 12.1 REST operations provided

None. This is a database story and publishes no operation.

#### 12.2 REST operations consumed

None by this story. The values the tables carry arrive through the service's own operations, and the ACE group facts arrive through the P1 contract.

#### 12.3 Events published

None. The outbox object is created here so that the service can publish later; this story writes no event row and publishes nothing.

#### 12.4 Events consumed

None. The inbox object is created here so that the service can consume idempotently later; this story consumes nothing.

#### 12.5 Workflows and activities

None.

#### 12.6 Schedules

None. The migration runs in the release pipeline, not on a Temporal Schedule.

#### 12.7 Tables owned

| Table | Owner (ownership map) | Created or altered here | Keys and indexes |
|---|---|---|---|
| role | P4 | Created | PK on id; unique on role_code; partial index ix_role_entra_group on entra_group where is_active |
| permission | P4 | Created | PK on id; foreign key role_id to role; unique on role_id, capability_area, matrix_version |
| role_conflict | P4 | Created | PK on id; unique on role_code, conflicts_with, conflict_version; index on valid_from |
| outbox_event | PLT (library object, created in this schema) | Created from the event platform template | The template's keys, unchanged |
| processed_event | PLT (library object, created in this schema) | Created from the event platform template | The template's keys, unchanged |
| idempotency_key | PLT (library object, created in this schema) | Created from the event platform template | The template's keys, unchanged |
| masking_rule, delegation_limit | P4 | Not touched | Their own stories' migrations |
| lov_value, reference_row, reference_version | P3 | Not touched and not referenced | No key, no view and no grant names `rwb_case` |

#### 12.8 Contract fakes

None. A database story uses no contract fake; it is tested against an empty schema and a copy of the SIT schema.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic in this story; the outbox and inbox objects are created for later use |
| Temporal | None | None | No workflow or Schedule |
| File | None | None | Migrations are deployed by the release pipeline, not by a file interface |

### 13. Solution plan

**Sequencing.** The service's Flyway sequence is owned by RWB-PLT-E1044-CON. The V0001 baseline creates the schema, the history table and the standard columns. This story adds the next versions after the baseline:

| Version | File | Contents |
|---|---|---|
| V0001 | baseline, from the platform DB story | Schema `rwb_access`, history table, standard columns |
| next after the baseline | `..._role_permission_conflict.sql` | Creates `role`, `permission` and `role_conflict` with their keys and indexes |
| next after that | `..._event_library_objects.sql` | Creates `outbox_event`, `processed_event` and `idempotency_key` from the event platform template |
| next after that | `..._access_grants.sql` | Usage on the schema and the table grants for the rwb-access login |

The legacy migration name `V_E1_022__role_conflict.sql` is recorded as the source of the `role_conflict` object; the monolith name and number are not reused on the service sequence. The exact version numbers are assigned by the sequence owner at build time; the order above is fixed by this story.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The three business tables and the three library objects live in `rwb_access` | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. The library writes its record into this schema's own tables, which the writer of RWB-P4-E1039-APP owns | H RWB-PLT-E1027-CON (carried by the writer's story; named here) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. `lov_value` is never created or read here: the values arrive over the contract | referred to; the consuming story carries the dependency |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library. The tables this story creates are the data that answer the guard, and no other service reads them | referred to; the consuming story carries the dependency |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The schema holds no call; the answers are the app story's | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The schema name follows the same short name: `rwb_access` under `/api/recovery/access/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. This story adds three migrations after the baseline and reuses no monolith name | H RWB-PLT-E1044-CON (the sequence owner; named here) |
| DP-19 | Screen, ace-web | gateway-bff composite route. No screen reads this schema; the edge reads the answers of the app story. SCR-43 and SCR-47 are P3 screens: their empty, loading, error and no-access states are not this story's | referred to; the consuming story carries the dependency |

**Table definitions**

`role` — `id` uuid NOT NULL, `role_code` varchar(20) NOT NULL, `role_name` varchar(80) NOT NULL, `role_class` varchar(15) NOT NULL, `default_scope` varchar(8) NOT NULL, `entra_group` varchar(120) NULL, plus the standard record columns of TSD P4 v3 T3.0. Primary key `(id)`; unique `(role_code)`; partial index `ix_role_entra_group` on `(entra_group)` where `is_active`.

`permission` — `id` uuid NOT NULL, `role_id` uuid NOT NULL, `capability_area` varchar(30) NOT NULL, `letters` varchar(5) NOT NULL, `matrix_version` varchar(20) NOT NULL, plus the standard record columns. Primary key `(id)`; foreign key `role_id` to `role(id)`; unique `(role_id, capability_area, matrix_version)`.

`role_conflict` — `id` uuid NOT NULL, `role_code` varchar(20) NOT NULL, `conflicts_with` varchar(30) NOT NULL, `reason` varchar(200) NOT NULL, `conflict_version` varchar(20) NOT NULL, `valid_from` date NOT NULL, `valid_to` date NULL, plus the standard record columns. Primary key `(id)`; unique `(role_code, conflicts_with, conflict_version)`; index on `(valid_from)`.

**No business value in a constraint.** `role_class`, `default_scope`, the letters and the two class values of `conflicts_with` are values of a list or of a matrix row. No check constraint carries them: a new area, a new letter set or a new class value must be a data change, not a migration (BR4). The application validates against `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` read over the reference-data contract.

**Library objects.** `outbox_event`, `processed_event` and `idempotency_key` are created in `rwb_access` from the template published by the event platform (RWB-PLT-TE006-CON) and are not modified here. Every service writes its own outbox and inbox in its own schema, so this is the only place where this service's events and inbox rows can live (Ownership Map ruling; ASM-1407).

**No session, password, token or local account.** The migration creates no session table, no password column, no token column and no local-account row, and the catalogue check of AC6 fails the build if one appears. Staff sign-in is ACE Common through gateway-bff, the session is in the gateway's Redis store (RWB-PLT-N006-INF), and there is no token store in the target (ADR-010; Architecture v5 slide 35).

**Grants.** `GRANT USAGE ON SCHEMA rwb_access TO <the rwb-access login>`; `GRANT SELECT, INSERT, UPDATE, DELETE ON role, permission, role_conflict, outbox_event, processed_event, idempotency_key TO <the rwb-access login>`; usage on the sequences those tables own. No grant to a shared login, no grant to another service's login, and no grant on any schema other than `rwb_access`. The grantee name is Not specified in the source documents (GAP-0777; ASM-1405); the other migrations of the same service grant to the same login.

**Rollback.** Per migration, in reverse order: the grant script is reversed by revoking the grants it made; the library objects, then `role_conflict`, then `permission`, then `role` are dropped. A role row loaded between the two runs keeps its `id` and `role_code` where the rollback only reverses an added object, so a later matrix load is never orphaned (BR9). The rollback is exercised on a copy of the SIT schema and recorded in the runbook.

**Done when.** The migrations apply twice without a change, the catalogue checks pass, the grants are exactly as above, no session, password or token column exists, the rollback returns the schema to its pre-migration shape, and the tests in section 16 pass.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Database error, no message id | A migration runs before the baseline or finds an object already present | The migration fails and nothing is applied; the pipeline stops |
| Database error, no message id | A grant script runs before the login exists | The script fails on the missing role; the platform DB story creates the login first |
| Check finding, no message id | A foreign key, view or grant names another schema or `public` | The pipeline check fails the build; the object is removed |
| Check finding, no message id | A session, password, token or local-account column appears | The pipeline check fails the build; the column is removed |
| MSG-GEN-001 | A role or matrix load reaches the database with a NOT NULL column empty | Enter {field}. Raised by the application, not by a database constraint |
| MSG-P1-002 | A matrix load names a role code the reference list does not know | The value you chose is not in the list. Raised by the application from the reference-data contract |

The business checks a reader might expect as database constraints are deliberately in the application: the class, area and scope values come from the reference contract (DP-07), and the letters are checked by the loading story, so a business person can change them without a migration. The database enforces what does not change: keys, uniqueness, dates and the schema boundary.

### 15. Screens and states

No screen. The result of a migration is visible in the release pipeline and in the service's Flyway history: pending, applied, failed, undone, each with a version and a checksum. The tables expose the standard record columns and the validity window of a conflict pair listed in section 9; nothing here is shown to a user directly, and the administration screens SCR-43 and SCR-47 in Epic 8 read the tables through the service's operations, never through SQL.

SCR-43 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-4958). SCR-47 states: empty, error and no access are Not specified in the source documents (CG-ALL-4959); its loading state is as defined in Screen Specifications v1 section SCR-47.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P4-E1022-DB-01 | AC1 | Component | Empty schema with V0001; this story's three migrations; a second run; the Flyway history compared |
| TC-P4-E1022-DB-02 | AC2 | Component | role catalogue: DF-REF-034 to DF-REF-039, the NOT NULL set, the unique role code, the partial index on entra_group where is_active |
| TC-P4-E1022-DB-03 | AC3 | Component | permission catalogue: DF-REF-040 to DF-REF-044, the foreign key to role, the unique key per role, area and matrix version |
| TC-P4-E1022-DB-04 | AC4 | Component | role_conflict catalogue: DF-REF-205 to DF-REF-211, the unique key per pair and version, the nullable valid_to, and the absence of a check constraint holding a class value |
| TC-P4-E1022-DB-05 | AC5 | Component | The three library objects after the template is applied; their columns compared with the template; the absence of a key into the three business tables |
| TC-P4-E1022-DB-06 | AC6 | Component | Catalogue queries over columns, foreign keys, views, synonyms and grants; the search for a session, a password, a token and a local account; the search for `rwb_case`, `recovery`, an ACE schema and `public` |
| TC-P4-E1022-DB-07 | AC7 | Component | Grant script and rollback on a copy of the SIT schema; grants listed per login; the role identifiers after the rollback |
| TC-P4-E1022-DB-08 | §12.7 tables (ASM-3438) | Component | Boundary of each table in §12.7: the keys and indexes of role, permission and role_conflict at their limits, and the three library objects at the template's keys |
| TC-P4-E1022-DB-09 | AC8 | Component | Each business rule BR1 to BR9 checked against the applied schema, with the check named in AC8 |

### 17. Guardrails

- No business value in a constraint: the class, area and scope values and the letters are application and reference data, read over their contracts (DP-07).
- No personal data in a migration, a script, a test fixture or a runbook: a role, a group name and a matrix version are identifiers, and a user appears as a reference only.
- No session, password, token or local account in the schema, by design and by catalogue check (ADR-010).
- No read of another schema, no key into another schema and no grant that names one: `rwb_access` objects reference `rwb_access` objects only (DP-01).
- The ACE group facts come through the P1 contract or `RWB-P1-E1069-APP`; no view, synonym or statement in this schema names an ACE schema or `public`.
- One login per service: the rwb-access login is the only grantee, and its name is Not specified in the source documents (GAP-0777; ASM-1405).
- The sequence is per service and linear: no monolith migration name is reused and no object is created twice (DP-15).
- The library objects are applied from the published template and never edited in this story, so a change to the outbox shape is one change in one place.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-ACA-001 | Single sign-on through Entra ID with MFA | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-01, FEAT-ACA-02 | BR1, BR6 | TC-P4-E1022-DB-02, TC-P4-E1022-DB-06 |
| REQ-ACA-002 | Roles as data, changed without a code release | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-03 | BR2, BR3, BR4 | TC-P4-E1022-DB-03, TC-P4-E1022-DB-04 |
| REQ-ACA-010 | Service identities under the same role checks | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-02 | BR5, BR7, BR8 | TC-P4-E1022-DB-05, TC-P4-E1022-DB-07 |
| Legacy TC-E1-022-01, TC-E1-022-02, TC-E1-022-03, TC-E1-022-04, TC-E1-022-05, TC-E1-022-06, TC-E1-022-07, TC-E1-022-08, TC-E1-022-09, TC-E1-022-10 | The ten legacy test cases of RWB-E1-022, at component and end-to-end level | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-01, FEAT-ACA-02, FEAT-ACA-03 | BR1 to BR9 | Executed by RWB-P4-E1022-APP and RWB-ITG-E1022-ITG |

The ten legacy test cases of RWB-E1-022 are executed by RWB-P4-E1022-APP, which owns legacy AC2, AC4, AC5, AC6, AC7, AC8 and AC9, and by RWB-ITG-E1022-ITG, which owns legacy AC1 and legacy AC3. This database story copies no legacy acceptance criterion and lists no legacy test case of its own; its tests are the schema checks of section 16.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1022-APP | App development | X dependency tracked: the story that reads these tables and answers the two operations |
| RWB-P4-E1022-CON | Contract | Sibling: the shapes its section 12 publishes must match the columns created here |
| RWB-P4-E1019-APP | App development | The role story that loads `role` and `role_conflict` rows after this migration |
| RWB-P4-E1037-APP | App development | The matrix story that loads `permission` rows after this migration |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence and its version allocation |
| RWB-PLT-NF06-DB, RWB-PLT-N011-DB | ACE DB | The schema and baseline of `rwb_access`, the login, and the connection pool per login |
| RWB-PLT-TE006-CON | Contract | The event platform template of the three library objects |
| RWB-P1-E1069-APP | App development | The P1 story that owns the ACE views; the group facts of a mapping row are read through it |

### 19. Out of scope

- The application code, the resolver and the two operations: RWB-P4-E1022-APP.
- The contract of the two operations: RWB-P4-E1022-CON.
- The role, group-mapping and conflict rows themselves: RWB-P4-E1019-APP and the mapping contract RWB-P4-AD001-CON.
- The permission matrix rows: RWB-P4-E1037-APP.
- `masking_rule`: the masking story of this service.
- `delegation_limit`: RWB-P4-E1038-APP.
- `lov_value`, `reference_row` and `reference_version`: rwb-case (P3), read over the reference-data contract.
- The ACE views, their grants and the boundary rule: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- The access log, the decision record and the break-glass path: RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB.
- The event schema itself: RWB-PLT-TE006-CON and the event platform story; this story applies the template.
- Performance tuning beyond the indexes named here: the non-functional work.
