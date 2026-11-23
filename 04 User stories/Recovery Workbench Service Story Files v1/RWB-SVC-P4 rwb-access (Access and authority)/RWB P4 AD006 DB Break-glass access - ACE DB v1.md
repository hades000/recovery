# RWB-P4-AD006-DB Break-glass access

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: ACE DB slice of legacy RWB-AD-006 for rwb-access — the `break_glass_grant` table in `rwb_access`, its one-active-grant constraint, its window and reason checks, its read and expiry indexes, its retention as data and the grant to the `rwb-access` login. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD006-DB |
| Work type | DB (ACE DB) |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P4-E |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As an **ACE database engineer**, I want **the `break_glass_grant` table created on the per-service Flyway sequence in schema `rwb_access` — with the grant id, the actor reference, the incident reference, the capability area, the right, the scope, the reason, the window start and end, the approver reference, the state, the break-glass marker and the created and ended times, the constraint that a person holds at most one active grant, the check that the window ends after it starts and that the reason is at least 20 characters, the indexes for the read and the expiry predicate, the retention held as data and the grant to the `rwb-access` login**, so that **the activation, the guard, the end and the self-expiry of the app story run on a schema that enforces the bound of a grant, cannot hold two active grants for one person and never reaches outside this service's own schema**.

This is the database story of legacy key RWB-AD-006 under epic RWB-SVC-P4. It delivers, in schema `rwb_access`:

- the migration that creates `break_glass_grant`, the table behind the activation, the guard, the end and the settle of the contract (DP-15);
- its keys: the primary key on `grant_id`, the unique partial constraint that keeps at most one `ACTIVE` grant per actor, the check that `ends_at` is after `starts_at`, the check on the reason length and the check on the state vocabulary;
- its indexes: one for the guard and the read of a caller's grants, and one for the expiry predicate the guard applies on every call;
- the retention **as data**: the retention class and the period are parameter rows of the parameters catalogue, never a literal in a migration, and the period in force is **Not specified in the source documents (GAP-0799; ASM-1498)**;
- the grant script for the per-service `rwb-access` login (DP-02), whose name is **Not specified in the source documents (GAP-0799; ASM-1493)**;
- the rollback of the migration, and the assertion that no object outside `rwb_access` is created, granted or referenced.

**The division of this key is fixed.** **RWB-P4-AD006-APP** owns the three legacy acceptance criteria and implements the activation, the checks, the window, the marking, the guard extension and the settle. **RWB-P4-AD006-CON** owns the published contract of the three operations, the two schemas, the session field, the auto-expiry rule and the fakes. **This story** owns the table, its constraints, its indexes, its retention and the login grant, and it changes no business rule. **RWB-P4-E1039-APP**, **RWB-P4-E1039-CON** and **RWB-P4-E1039-DB** own the access log of legacy RWB-E1-039 and the administration surface that lists the grants, and **RWB-P4-AD007-APP** owns the search and the export of that log.

**The table is this story's own working decision, and the overlap with RWB-P4-E1039-DB is stated rather than hidden.** TSD P4 v3 T3.1 has no grant table, and the ownership map gives P4 `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` and nothing else: `role_conflict` and `masking_rule` are the only extra P4 tables beyond the catalogue. The legacy RWB-E1-039 slice names a `break_glass_grant` in its DDL, and **this story is the one definition of that table**: the grant is the lifecycle of legacy RWB-AD-006, its columns are fixed here, and the E1039-DB step that names the same table is superseded by this definition — **Not specified in the source documents (GAP-0799; ASM-1493)**.

### 2. Business rationale

The legacy monolith held emergency access in the same recovery schema as the access log, the roles and the decision record, under one shared login, and nothing in the database said that a person cannot hold two emergency grants at once. After the split every service owns a schema, a login and a Flyway sequence, and the grant is a table of `rwb_access` alone (DP-01, DP-02, DP-15).

The table matters because three of this key's properties are only true if the database makes them true. **The bound** — one area, one right, one scope, one window — is a column set, and a column set that the application alone respects is a convention. **The one active grant per person** is a uniqueness rule the application checks and a second caller can race; the partial unique constraint is what makes AC1's "the system grants access for the window" a single grant and not two. **The self-expiry** needs an end that is always there: `ends_at` is `NOT NULL`, so a grant without an end cannot exist, and the guard's predicate over `(state, ends_at)` is what makes a grant out of force the moment its window passes, with no job and no person (BR5, BR6 of the app story). The window check and the reason check are copied from the legacy criterion, and the reason floor of 20 characters is the one value the legacy story fixes exactly.

The retention is a story and not a footnote because a grant is evidence. It is the entitlement behind an access-log entry, so it must outlive the window by the audit period; and an access log whose grant rows vanished would show actions with a marker that points at nothing. The period, however, is fixed by no source in this read set — DL26 is open and no retention table names a grant — so it is carried as a parameter row with no value in force, and the table is not partitioned: it is one row per grant, small by construction, and a partition would buy nothing but a maintenance surface. The access log is the table that gets the month partitions, and that table is RWB-P4-E1039-DB's.

The values copied from the sources are the schema `rwb_access`, the login `rwb-access`, the state vocabulary `ACTIVE` and `ENDED` that the E1039-DB slice already gives the table, the reason minimum of 20 characters and maximum of 1000 of FSD P4 v3 AC-EXC-P4-007-02, the incident reference shape `INC0004521` and the four-hour window of AC-ALT-P4-009-01, and the decision-record field ids of the entry the app story writes. Where no source names the table's columns, its retention or its field ids, the migration carries the placeholder and the assumption in force (GAP-0799; ASM-1493) and (GAP-0799; ASM-1498).

### 3. Preconditions

- The V0001 baseline of `rwb_access` exists on the per-service Flyway sequence, from RWB-PLT-E1044-CON and RWB-PLT-NF06-DB: the schema, the `flyway_schema_history` table and the standard record columns (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`).
- The ACE database and the per-service login policy are in place; the login of rwb-access is created by the platform DB work and its name is **Not specified in the source documents (GAP-0799; ASM-1493)**.
- The ownership map is the only source of table ownership: `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` are P4 and in `rwb_access`; `outbox_event`, `processed_event` and `idempotency_key` are PLT library objects created in each service schema by that service's own DB story; `decision_log_entry` and `approval` are P7's; `lov_value`, `reference_row`, `reference_version`, `parameter_catalog` and `parameter_value` are P3's.
- RWB-PLT-E1027-CON is published: the decision-record library DDL, whose outbox row the app story writes in the same transaction as the grant. This story creates no library object of its own and applies no library DDL — RWB-P4-E1039-DB owns that migration for this schema.
- The contract of the grant is RWB-P4-AD006-CON's: the three operations, the `BreakGlassActivation` and `BreakGlassGrant` schemas, the state vocabulary and the auto-expiry rule. The field names of this migration answer that contract.
- The parameter contract (DP-06) is available to the platform for the retention rows; the codes and the period are **Not specified in the source documents (GAP-0799; ASM-1498)**.
- The field ids are those of the Logical Data Model and Data Dictionary; the grant table has no field id in any source, and its columns are named after the legacy request and the contract's schema fields.
- No approval is required to run a Draft migration on a development database; the migration is released to SIT only after the tests in section 16 pass.

### 4. Flow

1. The ACE database engineer checks out the rwb-access migration folder and confirms the highest applied version on the sequence (the V0001 baseline).
2. The engineer adds one migration after that version: the `break_glass_grant` table with its primary key, its unique partial constraint, its three check constraints and its two indexes.
3. The engineer proves on an empty schema that the migration applies once, records its version and checksum, and that a second run reports no pending migration.
4. The engineer writes the grant script for the `rwb-access` login, scoped to schema `rwb_access` and to the table, with the rights the guard needs (`SELECT`, `INSERT`, `UPDATE`) and no right that would let the service rewrite an ended grant's history (`DELETE` is granted only if the retention rule of the table needs it, and it does not).
5. The engineer adds the retention class and the retention period as parameter rows through the platform reference-data path, with the period carried as a placeholder, and stamps no retention literal in the migration.
6. The migration pipeline applies the baseline and this story's migration to an empty schema, then to a copy of the SIT schema, and runs the schema checks: columns, `NOT NULL`, the primary key, the partial unique constraint, the three checks and the two indexes.
7. The pipeline inserts the fixture rows that must fail — a second `ACTIVE` grant for the same actor, a window that ends before it starts, a reason of 19 characters, a state outside the vocabulary — and asserts that each is refused.
8. The pipeline scans the catalogue for any foreign key that names another schema and any statement that names a table outside `rwb_access`; it also asserts that the access-log table of RWB-P4-E1039-DB is neither read nor joined.
9. The rollback is exercised on a copy: the table drops with its constraints and indexes, the grants are revoked, and a re-apply of the sequence returns the same shape.
10. The migration is recorded in the release notes of the sequence, with its version number and its checksum, and the retention row is handed to the parameter load.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | The migration runs before the V0001 baseline | Flyway refuses with an unresolved baseline and nothing is applied | Pipeline error, no message id |
| X2 | The table already exists in the sequence | The repeatable check refuses to re-create it and the migration is marked as already applied | Pipeline error, no message id |
| X3 | A foreign key names `rwb_decision`, `rwb_case` or another schema | The catalogue check fails the build; the key is removed and the reference is kept as a value | Check finding, no message id |
| X4 | The grant script runs before the login exists | The script fails on the missing role; the platform DB story creates the login first | Database error, no message id |
| X5 | The grant script grants to a shared or legacy login | The review rejects the script: one login per service (DP-02) | Review finding, no message id |
| X6 | A second `ACTIVE` grant is inserted for the same actor | The partial unique constraint refuses it; the application maps it to 409 with MSG-GEN-004 | MSG-GEN-004 through the application |
| X7 | A row is inserted with `ends_at` not after `starts_at`, with a reason shorter than 20 characters, or with a state outside `ACTIVE` and `ENDED` | The check constraint refuses it; the application maps the reason to 422 with MSG-GEN-002 | MSG-GEN-002 through the application |
| X8 | The retention period is still open at release | The parameter row carries the placeholder and the gap; the table still exists with the default class and no delete | GAP-0799 |
| X9 | A statement of the service read joins the access-log table | The boundary check fails the build; the marker is a value on the entry and never a join | Check finding, no message id |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One migration, one grant script, one rollback and two parameter rows on the service's own sequence; nothing to build against |
| Negotiable | Constraint and index names follow the platform naming library; the column set is fixed by the legacy request and the contract's schema fields |
| Valuable | The lifecycle of a grant has a schema that enforces the bound, the single active grant and the window, and that never reaches outside `rwb_access` |
| Estimable | One table, four constraints, two indexes, one grant script, two parameter rows and one rollback |
| Small | Days, not weeks, with the schema checks |
| Testable | Every criterion is a catalogue query or a pipeline run in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: rwb_access schema for the break-glass grant

  Background:
    Given the rwb-access schema is rwb_access and the baseline version is V0001
    Given the grantee is the rwb-access login (DP-02), whose name is Not specified in the source documents (GAP-0799; ASM-1493)

  Scenario: AC1 The migration applies on the sequence and is repeatable (new, D-RCV-60)
    Given an empty rwb_access schema with the V0001 baseline applied
    When this story's migration and the grant script run in order
    Then the migration is recorded once on the service's Flyway history with its version and checksum
    Then a second run of the same pipeline changes nothing and reports no pending migration
    Then the migration reuses no monolith migration name and creates no object outside rwb_access

  Scenario: AC2 break_glass_grant exists with its columns (new, D-RCV-60)
    Given the migration of this story applied to an empty schema
    When the catalogue is read
    Then break_glass_grant has grant_id, actor_user_id, incident_reference, iam_request_id, approver_user_id, capability_area, right_code, scope_code, reason, starts_at, ends_at, ended_at, state and break_glass_marker
    Then the standard record columns of the V0001 baseline are present and grant_id is the primary key
    Then ends_at is NOT NULL and started_at is NOT NULL, because a grant without a window is not a grant
    Then state is limited to ACTIVE and ENDED, and break_glass_marker is NOT NULL and true

  Scenario: AC3 The constraints enforce the one active grant, the window and the reason (new, D-RCV-60)
    Given the constraints of break_glass_grant
    When a second row in state ACTIVE is inserted for the same actor_user_id
    Then the unique partial constraint on actor_user_id where state is ACTIVE refuses it
    Then a row whose ends_at is not after its starts_at is refused by a check constraint
    Then a row whose reason is shorter than 20 characters is refused by a check constraint
    Then a row whose state is neither ACTIVE nor ENDED is refused by a check constraint
    Then no constraint carries a business value other than the 20 characters of legacy AC1 and the 1000 characters of the column

  Scenario: AC4 The read and the expiry predicate are indexed (new, D-RCV-60)
    Given the indexes of break_glass_grant
    When the query plans of the guard and of the read are examined
    Then an index on actor_user_id and starts_at serves the read of a caller's grants
    Then a partial index on ends_at where state is ACTIVE serves the expiry predicate state = ACTIVE and now() before ends_at
    Then the plan of the expiry predicate is an index scan and not a sequential scan
    Then no index duplicates the primary key

  Scenario: AC5 The retention is data and the table is not partitioned (new, D-RCV-60)
    Given the retention decision of this story
    When the catalogue and the parameter rows are read
    Then break_glass_grant is not partitioned and no partition key is declared
    Then the retention class and the retention period are parameter rows of the parameters catalogue and not literals in the migration
    Then the retention period in force is Not specified in the source documents (GAP-0799; ASM-1498)
    Then no delete of a grant row is performed by the table's own rule inside the audit window

  Scenario: AC6 The table belongs to the rwb-access login and to no other (new, D-RCV-60)
    Given the grant script of this story
    When it runs
    Then the rwb-access login has usage on schema rwb_access and select, insert and update on break_glass_grant
    Then the login holds no delete on break_glass_grant and no grant on any table of rwb_decision, rwb_case or the access log
    Then no other login holds a grant on break_glass_grant

  Scenario: AC7 The rollback is complete and the boundary holds (new, D-RCV-60)
    Given the grant script and the rollback of this story
    When the rollback runs on a copy of the SIT schema
    Then the grants it made are revoked and break_glass_grant drops with its constraints and indexes
    Then a re-apply of the sequence returns the same shape, the same constraints and the same indexes
    Then no object of another schema was created, granted or referenced, and the access-log table of RWB-P4-E1039-DB is neither read nor joined
```

These criteria are new and test the database artefacts only: no legacy acceptance criterion is repeated, and every physical value (table, column, field id, constraint, window, minimum length) is the legacy, contract or library value, copied character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each service's objects live in its own schema under its own login; one login per service | DP-01, DP-02, DP-15 |
| BR2 | A person holds at most one active grant, and the database refuses a second `ACTIVE` row for the same actor | Legacy RWB-AD-006 AC1; FSD P4 v3 AC-EXC-P4-007-05; ASM-1500 |
| BR3 | A grant has a window: `starts_at` and `ends_at` are `NOT NULL` and `ends_at` is after `starts_at`, because a grant without an end is not a grant | Legacy RWB-AD-006 AC3; FSD P4 v3 AC-ALT-P4-009-01 |
| BR4 | The reason is at least **20 characters** and at most 1000, and the minimum is the legacy rule the database enforces | Legacy RWB-AD-006 AC1; FSD P4 v3 AC-EXC-P4-007-02; ASM-1497 |
| BR5 | The state vocabulary is `ACTIVE` and `ENDED`; a refused request writes no row, so no third state exists | RWB-P4-E1039-DB constraint; ASM-1496 |
| BR6 | The marker is a column of the grant and is true, so a grant row is never confusable with a row of another table under a union or a join | Legacy RWB-AD-006 AC1; ASM-1493 |
| BR7 | The retention class and the period are parameter rows, never literals in a migration, and the period is open | DP-06; GAP-0799; ASM-1498 |
| BR8 | The table is not partitioned: it is one row per grant, and the month partitions belong to the access log of RWB-P4-E1039-DB | ASM-1498; ownership map |
| BR9 | The tables of rwb-decision, rwb-case and the access log are never referenced by a key here; the incident, the case and the entry are values | DP-01; ownership map |
| BR10 | An ended grant keeps its rows: the migration grants no delete, so the evidence of a window is never removed by the service | Legacy RWB-AD-006 AC3; ASM-1498 |

### 9. State transitions

None in the runtime sense: a table has no state machine. The states this story moves through are the migration states of the service's Flyway history (pending, applied, failed, undone), and the row state the schema exposes is `ACTIVE` or `ENDED`, which the application moves at `ends_at` through the settle or on the explicit end. The transition from `ACTIVE` to `ENDED` is one `UPDATE` in the application's transaction; the database guarantees only that an ended row can never be a second `ACTIVE` row for the same actor and that the window it carries is a real one.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The ACE database engineer (any team, per U3) | Writes and runs the migration, the grant script, the parameter rows and the rollback |
| The service owner of rwb-access | Approves a destructive change; none is planned here, and the table's drop only happens in the rollback of a copy |
| The platform DB owner (RWB-PLT-E1044-CON, RWB-PLT-NF06-DB) | Owns the sequence, the baseline and the login policy |
| The owner of the retention rule | Confirms the retention class and the period used by the parameter row; the owner is **Not specified in the source documents (GAP-0799; ASM-1498)** |
| rwb-decision (P7) | Owns `decision_log_entry` and the central ledger; this schema holds no key to them |
| No delegation of authority level applies | A schema change is not a credit decision |

The grantee is named only as the rwb-access login (DP-02); its name is **Not specified in the source documents (GAP-0799; ASM-1493)**. No personal name and no credential appears in a migration, a script or a runbook.

### 11. Data

| Table | Schema | Field identifiers | This story |
|---|---|---|---|
| `break_glass_grant` | `rwb_access` | None in the source: the columns are named after the legacy request and the contract's schema fields, and the field ids are **Not specified in the source documents (GAP-0799; ASM-1493)** | Creates the table, its four constraints and its two indexes, and grants it |
| `role` | `rwb_access` | DF-REF-034 to DF-REF-038 | The role and its default scope, read by the app story: created by its own story of this service, and this story alters nothing |
| `permission` | `rwb_access` | DF-REF-040 to DF-REF-044 | The Platform administration letters and the capability areas, read by the app story: created by its own story, and this story alters nothing |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_access` | The library template's columns; no field id in this story's source | **Not created here.** RWB-P4-E1039-DB applies the library DDL, and this story names none of their columns |
| the access log of RWB-P4-E1039-DB | `rwb_access` | The entry's field ids are that story's | **Not created, not read and not joined.** The marker on an entry is a value the writer of RWB-P4-E1039-APP stamps |
| `decision_log_entry`, `approval` | `rwb_decision` | DF-DEC-001 to DF-DEC-030 | **Not created, not granted and not referenced.** P7 owns them |
| `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | `rwb_case` | DF-REF-027 to DF-REF-033 and the parameter tables | **Not created and not referenced.** P3 owns them; the retention rows are loaded over the parameters contract (DP-06) |
| `masking_rule`, `role_conflict`, `delegation_limit` | `rwb_access` | DF-REF-198 to DF-REF-204 and DF-REF-016 to DF-REF-062 | Not touched by this story |

**No row of this table holds a personal value.** The actor and the approver are staff user references, the incident is a reference, the area, the right and the scope are codes, and the only free text is the reason, which the application bounds at 20 to 1000 characters and the review of RWB-P4-E1039-APP reads. No name, no e-mail address and no identity number can be stored in a column of this table, because there is no column of that kind.

### 12. Contract

#### 12.1 REST operations provided

None. This is a database story and publishes no operation.

#### 12.2 REST operations consumed

None. The retention rows are loaded by the platform reference-data path, not by this story.

#### 12.3 Events published

None. The grants this table holds produce the decision-record entries of the app story through the library of DP-03, and that message is the library's, not this story's.

#### 12.4 Events consumed

None. This story creates no inbox row and subscribes to no topic.

#### 12.5 Workflows and activities

None.

#### 12.6 Schedules

None. The migration runs in the release pipeline, and nothing about a grant runs on a clock in this story: the expiry predicate is a query the application runs, and the six-monthly access review list (JOB-18) belongs to RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner (ownership map) | Created or altered here | Keys, indexes and constraints |
|---|---|---|---|
| `break_glass_grant` | P4, in `rwb_access`; no row in the ownership map — **Not specified in the source documents (GAP-0799; ASM-1493)** | Created | Primary key on `grant_id`; index on `(actor_user_id, starts_at)`; partial unique constraint on `(actor_user_id)` where `state = 'ACTIVE'`; check `ends_at > starts_at`; check `char_length(reason) >= 20 and char_length(reason) <= 1000`; check `state IN ('ACTIVE','ENDED')`; `break_glass_marker` NOT NULL and true; partial index on `ends_at` where `state = 'ACTIVE'` |
| `role`, `permission` | P4 | Not touched | None here; read by the app story under its own grants |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library | Not touched | Created by RWB-P4-E1039-DB's library migration |
| the access log of RWB-P4-E1039-DB | P4, RWB-P4-E1039-DB | Not touched | No key, no read and no join from this table |
| `decision_log_entry`, `approval` | P7 | Not touched | None here; the schema holds no key to `rwb_decision` |
| `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | P3 | Not touched | None here; the retention rows are read over the parameters contract |

**The grant table is the one table this story adds, and it is the only one it names.** That it has no row in the ownership map and no field ids in any source is the open point of this story (GAP-0799; ASM-1493), and that the legacy RWB-E1-039 slice names a table of the same name is settled by this story holding the one definition (ASM-1493).

#### 12.8 Contract fakes

None. A database story uses no contract fake; it is tested against an empty schema, a copy of the SIT schema and a fixture set of rows that must be refused.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic is provisioned here; the outbox rows the app story writes are its own |
| Temporal | None | None | No workflow or Schedule |
| File | None | None | Migrations are deployed by the release pipeline, not by a file interface |

### 13. Solution plan

**Sequencing.** The service's Flyway sequence is owned by RWB-PLT-E1044-CON. The V0001 baseline creates the schema, the history table and the standard columns. This story adds the next version after the baseline:

| Version | File | Contents |
|---|---|---|
| V0001 | baseline, from the platform DB story | Schema `rwb_access`, history table, standard columns |
| next after the baseline, e.g. `V4003_1__break_glass_grant.sql` | `..._break_glass_grant.sql` | The `break_glass_grant` table, its four constraints and its two indexes |
| the grant script of the same change | `..._break_glass_grant_grants.sql` | Usage on the schema and `SELECT`, `INSERT` and `UPDATE` on the table for the rwb-access login |
| the parameter rows of the same change | the reference-data load | The retention class and the retention period, with the period carried as a placeholder |

The order above is fixed by this story and the exact version numbers are assigned by the sequence owner at build time. The monolith migration name and number are not reused on the service sequence.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. The grant and its entry are committed together by the app story | referred to; the consuming story carries H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. This table reads no ACE view | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. No path is served here; the schema serves the base of the app story only | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route. The screen reads grants through the read operation and never through SQL | referred to; the consuming story carries H RWB-PLT-N001-CON |

**Table definition**

`break_glass_grant` — `grant_id` uuid NOT NULL, `actor_user_id` uuid NOT NULL, `incident_reference` varchar(20) NOT NULL, `iam_request_id` varchar(40) NOT NULL, `approver_user_id` uuid NOT NULL, `capability_area` varchar(30) NOT NULL, `right_code` varchar(5) NOT NULL, `scope_code` varchar(8) NOT NULL, `reason` varchar(1000) NOT NULL, `starts_at` timestamptz NOT NULL, `ends_at` timestamptz NOT NULL, `ended_at` timestamptz NULL, `state` varchar(10) NOT NULL, `break_glass_marker` boolean NOT NULL, plus the standard record columns of the V0001 baseline. Constraints:

- primary key `(grant_id)`;
- unique partial constraint on `(actor_user_id)` where `state = 'ACTIVE'`, so that a person holds at most one active grant and a second activation is refused by the database (BR2);
- check `(ends_at > starts_at)`, so that a window that ends before it starts cannot be stored (BR3);
- check `(char_length(reason) >= 20 and char_length(reason) <= 1000)`, the **20 characters** of legacy RWB-AD-006 AC1 and the column width of FSD P4 v3 AC-EXC-P4-007-02 (BR4);
- check `(state in ('ACTIVE','ENDED'))` (BR5);
- check `(break_glass_marker)` true, so that the row declares itself a break-glass grant (BR6).

Indexes: `ix_bgg_actor_start` on `(actor_user_id, starts_at)` for the read of a caller's grants and for the guard; `ix_bgg_expiry` on `(ends_at)` where `state = 'ACTIVE'`, which serves the expiry predicate `state = 'ACTIVE' and now() < ends_at` that the guard applies on every call and the settle applies on the next read. Both are created by the same migration; no index duplicates the primary key.

The incident reference is `varchar(20)` and the IAM request reference is `varchar(40)`, sized to the references the FSD uses (`INC0004521`, `IAM-778812`); the reference formats themselves are values of the incident and the IAM, not of this schema. The reason is the only free text, and the reason maximum of 1000 is the column width.

**Retention and partitioning as data.**

| Item | Value |
|---|---|
| Partition | None. The table is one row per grant and is small by construction; the month partitions belong to the access log of RWB-P4-E1039-DB (BR8) |
| Retention class | A parameter row of the parameters catalogue, read by the platform retention job and never by a literal |
| Retention period | **Not specified in the source documents (GAP-0799; ASM-1498)**; DL26 is open and no source names the period of a grant |
| Retention action | The platform retention job acts on the row; this schema grants no delete to the service, so the evidence of a window is never removed by the service (BR10) |
| Archive | The archive target is the platform's, not this schema's, and no archive object is created here |

**Grants.** `GRANT USAGE ON SCHEMA rwb_access TO <the rwb-access login>`; `GRANT SELECT, INSERT, UPDATE ON break_glass_grant TO <the rwb-access login>`, with no `DELETE` and no `TRUNCATE`; no grant on `rwb_decision`, on `rwb_case`, on the access-log table or on a `public` table. The grantee name is **Not specified in the source documents (GAP-0799; ASM-1493)**.

**Rollback.** The migration is reversed by dropping the two indexes and the table with its constraints; the grant script is reversed by revoking the grants it made; the parameter rows are removed by the reference-data rollback. The rollback is exercised on a copy of the SIT schema and recorded in the runbook. The access-log table of RWB-P4-E1039-DB is not touched by this rollback, because this story never created it.

**Done when.** The migration applies twice without a change, the catalogue checks pass, the partial unique constraint refuses a second active grant, the window check and the reason check refuse their rows, the two indexes serve the read and the expiry predicate, the grants are exactly as above, the boundary scan finds no object outside `rwb_access`, the rollback returns the schema to its pre-migration shape, and the tests in section 16 pass.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-004 | A second `ACTIVE` grant row is inserted for the same actor; the application maps the constraint to 409 | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-002 | A grant reason reaches the database outside the 20 to 1000 bounds; the application maps it to 422 | {field} must be between {min} and {max}. |
| Database error, no message id | A migration runs before the baseline or finds an object already present | The migration fails and nothing is applied; the pipeline stops |
| Database error, no message id | A grant script runs before the login exists | The script fails on the missing role; the platform DB story creates the login first |
| Check finding, no message id | A foreign key names another schema, or a statement reads the access-log table | The pipeline check fails the build; the key or the statement is removed |

The database enforces what does not change: the keys, the one active grant, the window, the reason floor of 20 characters and the state vocabulary. The reason **maximum** and any stricter minimum are the application's, read from the parameter `rwb.access.breakglass.reason-min` that RWB-P4-E1039-DB already records, so a business person can raise the floor without a migration (ASM-1497). Every message and its id is the legacy one and is raised by the app story.

### 15. Screens and states

No screen. The result of the migration is visible in the release pipeline and in the service's Flyway history: pending, applied, failed, undone, each with a version and a checksum. The retention row is visible on the platform database dashboard. Nothing here is shown to a user directly, and SCR-43 Roles and access reads the grants through the read operation of RWB-P4-AD006-APP, never through SQL.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-006-01 | AC1 | Component | Legacy test "Granted with an incident" as the ground of the schema: the fixture row is the grant of `INC0004521`, approved by `IAM-778812`, area `CASE_RECORD`, right `U`, scope `ALL`, reason of 46 characters, window 10:30 to 14:30; the row is stored and read back with its state `ACTIVE` |
| TC-AD-006-02 | AC2 | Component | Legacy test "Refused without an incident" as the ground of the schema: a grant row cannot be stored without an incident reference, because the column is `NOT NULL`; the empty fixture is refused |
| TC-AD-006-03 | AC3 | Component | Legacy test "Ends on its own" as the ground of the schema: the window is a stored pair of times, the check refuses an end before the start, and the settle to `ENDED` keeps the row and its window |
| TC-AD-006-04 | Access | Component | Legacy test "A role without the right is refused with MSG-P4-002" as the ground of the schema: the grant script gives the rwb-access login no more than select, insert and update, so no caller's refusal can be undone by a wider grant |
| TC-AD-006-05 | Principle 5 | Contract | Legacy test "A forced decision log write failure stops the action with MSG-P7-003" as the ground of the schema: the grant row and its outbox row are one transaction, so a failed entry leaves no grant row |

The five legacy test cases are kept with their IDs and their legacy Covers values, and the legacy test name is written in the Data column. The Level column follows Template and Rules §R7.2: the schema's ground for each case is tested at Component, and the transaction ground of the record-before-change rule at Contract. The behaviour of each case in the running service is RWB-P4-AD006-APP's at End to end, and the full test with its Given, When and Then is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The ITG copy of the set is RWB-ITG-AD006-ITG's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in a constraint beyond the legacy rule: the reason floor is the 20 characters of legacy AC1, the maximum is the column width, and the retention period is parameter data (BR4, BR7).
- No personal data in a migration, a script, a fixture or a runbook: the actor and the approver are staff user references, the incident is a reference, and no column of the table can hold a name, an e-mail address or an identity number.
- No read of another schema and no key into another schema: `rwb_access` objects reference `rwb_access` objects only, and the access-log table of RWB-P4-E1039-DB is never read or joined (DP-01, BR9).
- One login per service: the rwb-access login is the only grantee, and its name is **Not specified in the source documents (GAP-0799; ASM-1493)**.
- No destructive change: an ended grant keeps its row, the service holds no delete, and the retention action is the platform's (BR10).
- The sequence is per service and linear: no monolith migration name is reused and no object is created twice (DP-15).
- No object of RWB-P4-E1039-DB is created here: the library objects and the access-log table are that story's, and this migration names neither.
- The one active grant and the window are enforced by the database, so no caller, queue or retry can produce two active grants or a grant with no end (BR2, BR3).

### 18. Traceability

The Work Package carries the requirement list of this key as empty, and TSD P4 v3 T8 maps REQ-ACA-008 to the sign-in story RWB-E1-022; FSD P4 v3 records REQ-ACA-008 as "A break-glass path exists for an emergency, needs its own approval, and writes to the access log", must, first in E1, with FEAT-ACA-09 and FEAT-ACA-10. This story proves the schema beneath the path and its approval; the access log itself is RWB-P4-E1039-DB's.

| Feature | Where this story answers it | Test cases |
|---|---|---|
| FEAT-ACA-09, use break-glass access with an incident reference | The incident reference, the actor, the area, the right, the scope and the window as columns with their constraints (sections 11, 13) | TC-AD-006-01, TC-AD-006-02 |
| The own-approval rule of REQ-ACA-008 | The IAM request reference and the approver reference as `NOT NULL` columns (BR2 of the contract, section 13) | TC-AD-006-01 |
| The self-expiry the legacy criterion asks for | The stored window, the `ends_at` NOT NULL rule and the partial index of the expiry predicate (BR3, section 13) | TC-AD-006-03 |
| The record-before-change rule | The grant row and its outbox row as one transaction, and the write rights the script grants (section 13) | TC-AD-006-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-AD006-APP | App development | The story that writes, reads and settles the rows this schema holds |
| RWB-P4-AD006-CON | Contract | Sibling: the `BreakGlassActivation` and `BreakGlassGrant` schemas of its section 11 must match this table |
| RWB-P4-E1039-DB | ACE DB | Sibling of the same legacy module: the library objects and the access-log table. Its DDL names a grant table; this story holds the one definition (ASM-1493) |
| RWB-P4-E1039-APP, RWB-P4-E1039-CON | App development, Contract | The access log that stamps the marker, and its contract |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence and its version allocation |
| RWB-PLT-NF06-DB | ACE DB | The schema split and the baseline of `rwb_access` |
| RWB-PLT-E1027-CON | Contract | The library DDL whose outbox row the app story commits with the grant |
| RWB-P4-E1019-APP, RWB-P4-E1037-APP | App development | The role and permission rows the app story reads, created by their own stories |
| RWB-ITG-AD006-ITG | Integration | The end-to-end proof that a marked action reaches the access log |

The legacy test cases of this key — TC-AD-006-01, TC-AD-006-02, TC-AD-006-03, TC-AD-006-04 and TC-AD-006-05 — are executed by RWB-P4-AD006-APP and, as the cross-service copy, by RWB-ITG-AD006-ITG; this story proves the schema beneath them.

### 19. Out of scope

- The application code of the activation, the checks, the window, the marking, the guard extension and the settle: RWB-P4-AD006-APP.
- The published contract of the three operations and its fakes: RWB-P4-AD006-CON.
- The access log, its entry shape, its writer, its partitions, its retention and the administration surface: RWB-P4-E1039-CON, RWB-P4-E1039-APP and RWB-P4-E1039-DB. This story neither creates nor reads the access-log table.
- The access-log search and export: RWB-P4-AD007-APP.
- The library objects `outbox_event`, `processed_event` and `idempotency_key`, and the decision-record table: RWB-P4-E1039-DB and RWB-PLT-E1027-CON.
- The role, permission, masking and delegation tables and their migrations: the other stories of RWB-SVC-P4.
- `decision_log_entry`, `approval` and the central ledger: P7 rwb-decision and RWB-P7-E1039-APP.
- `lov_value`, `reference_row`, `reference_version`, `parameter_catalog` and `parameter_value`: P3 rwb-case; the retention rows are loaded over that contract.
- The retention job implementation and the archive target of the platform: the platform DB and retention work; the period is **Not specified in the source documents (GAP-0799; ASM-1498)**.
- The incident register and its open state: its owner is not fixed by any source (GAP-0797; ASM-1491).
- Data migration from the monolith and its reconciliation: the migration work of the programme, not this story.
- Performance tuning beyond the two indexes of section 13: the non-functional work.
