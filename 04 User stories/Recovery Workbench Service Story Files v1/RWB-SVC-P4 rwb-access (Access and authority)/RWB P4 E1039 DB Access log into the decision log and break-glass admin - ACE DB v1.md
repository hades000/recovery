# RWB-P4-E1039-DB Access log into the decision log and break-glass admin

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: ACE DB slice of legacy RWB-E1-039 for rwb-access — the Flyway sequence for the four tables of the key, the grants to the `rwb-access` login, and the retention and partitioning of the access log as data. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E1039-DB |
| Work type | DB (ACE DB) |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-039 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP17, DP19 |
| Parallel lane | L-P4-W |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-023, FR-P4-024, FR-P4-025, FR-P4-026, FR-P4-027, FR-P4-028, FR-P4-029, FR-P4-030, FR-P4-031) |
| Status | Draft (realignment v1) |

### 1. Story

As an **ACE database engineer**, I want **the four tables this legacy key needs created on the per-service Flyway sequence in schema `rwb_access` — the outbox, the inbox and the idempotency store of the decision-record library and the break-glass grant table with its two-person constraint — with the grants to the `rwb-access` login, the log partitioned by month and retained as data, and an explicit guarantee that no entry holds a personal value**, so that **the writer, the grant and the read of the app story run on a schema that is correct, granted, reversible and confined to this service's own schema**.

This is the database story of legacy key RWB-E1-039 under epic RWB-SVC-P4. It delivers, in schema `rwb_access`:

- the migration that applies the decision-record library DDL of RWB-PLT-E1027-CON and creates the three library objects this key writes through — `outbox_event`, `processed_event` and `idempotency_key` — on the per-service sequence after the V0001 baseline (DP-03, DP-15);
- the migration that creates `break_glass_grant`, the table behind the grant, the end and the read operations of the contract, with its keys and the two-person constraint;
- the grant script for the `rwb-access` login (DP-02), whose name is Not specified in the source documents (GAP-0782; ASM-1427);
- the retention and partitioning of the access log **as data**: the month partition on `decided_at`, the retention class and the archive rule, held as parameter rows and never as a job in this story;
- the rollback of each migration, in reverse order, with the appended chain preserved;
- the explicit assertion that **no entry holds a personal value** — only the case id, the field id and the flag, with the actor as a staff user reference and never a name.

**The division of this legacy key is fixed and is the same in all four stories.** **RWB-P4-E1039-APP** owns the ten legacy acceptance criteria and implements the writer, the grant and the read. **RWB-P4-E1039-CON** owns the published contract of the four operations, the entry shape, the two-person rule, the time box, the refusal vocabulary and the fail-closed rule. **This story** owns the schema, the four tables, the grants, the retention and the partitioning, and it changes no business rule. **RWB-P4-E1039-OPS** owns the deployment: the Helm values, the Kafka ACLs, the secrets, the alerting and the run book, and it provisions no database object. **The end-to-end proof is RWB-ITG-E1039-ITG**, and the two neighbours of the same legacy key are **RWB-P5-E1039-APP** on the document side and **RWB-P7-E1039-APP** on the ledger side.

### 2. Business rationale

The legacy story added one index (`ix_declog_actor_time`) to a single `decision_log_entry` table in one recovery schema with one shared login, and wrote the access events of every module into the P7 writer inside the same process. After the split there is no shared table to index: every service owns a schema, a login and a Flyway sequence, and the access entry is written in the schema of the service that served the read (DP-01, DP-03, DP-15).

**The division is fixed and is the same in all four stories.** The entry shape is **RWB-P4-E1039-CON**'s, the writer and the grant are **RWB-P4-E1039-APP**'s, the deployment and the alerts are **RWB-P4-E1039-OPS**'s, and **RWB-ITG-E1039-ITG** proves the key end to end; **RWB-P5-E1039-APP** records the document side and **RWB-P7-E1039-APP** owns the central ledger. **RWB-P4-E1039-DB** owns only what the database must enforce so that the other three can be true: the four tables exist and nothing else is created, the login is the only writer, the log is partitioned and retained as data rather than by an application job, and no entry can hold a personal value because there is nowhere to put one.

The four tables matter for four different reasons. The `outbox_event` row is written in the same transaction as the access entry, so the record and its publication can never disagree; without it the fail-closed rule of the app story would have nothing to fail on. The `idempotency_key` row is what makes AC10 true — the same `k-001` returns the first grant answer and writes no second entry, while `k-002` is refused with 409 — so the table is a correctness requirement of the story and not a library formality. The `processed_event` table is created by the library DDL so that every service schema has the same shape; this key subscribes to no event, so no row is written to it and the inbox stays empty, which is stated rather than left to be discovered. And `break_glass_grant` is the one table this key adds of its own: it holds the grant, its start and its end, the IAM request and the incident, and the constraint that a person has at most one active grant.

The negative side is the reason the retention is a story and not a footnote. An access log that keeps a personal value would become the largest personal-data store in the workbench, so **the schema holds no personal value at all**: the case id, the document id, the field id and the flag are the clearest facts an entry can carry, the actor is a staff user reference, and the reason text of a grant is free text that the application checks and the run book tells the operator never to fill with customer data (NFR-040, BR7 of the app story). Partitioning by month keeps the retention rule enforceable by a partition drop instead of a mass delete, and the retention period itself is a parameter, because no source fixes it (DL26).

The values copied from the sources are the table names of the library and of the key, the service schema `rwb_access`, the login `rwb_access`, and the field ids of the decision record: DF-DEC-002 for the case id, DF-DEC-003 for the decision code, DF-DEC-014 for the actions, DF-DEC-016 for the decided at and DF-DEC-030 for the actor. Where no source names the break-glass grant table, its constraint, the retention period or the partition granularity, the migration carries the placeholder and the assumption in force (GAP-0782; ASM-1428) and (GAP-0782; ASM-1429).

### 3. Preconditions

- The V0001 baseline of `rwb_access` exists on the per-service Flyway sequence, from RWB-PLT-E1044-CON and RWB-PLT-NF06-DB: the schema, the `flyway_schema_history` table and the standard record columns (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`).
- The ACE database and the per-service login policy are in place; the login of rwb-access is created by the platform DB work and its name is Not specified in the source documents (GAP-0782; ASM-1427).
- RWB-PLT-E1027-CON is published: the DDL template of the decision-record library, with its local table, its outbox, its inbox and its idempotency store, and the `prev_hash` and `entry_hash` columns of the chain.
- The ownership map is the only source of table ownership: `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` are P4 and in `rwb_access`; `outbox_event`, `processed_event` and `idempotency_key` are PLT library objects created in each service schema by that service's own DB story; `decision_log_entry` and `approval` are P7's and `lov_value` is P3's.
- The parameter contract is available for the retention and partition rows (DP-06), and the retention decision DL26 is still open, so the retention period is carried as a parameter with the placeholder of this story.
- The field ids are those of the Logical Data Model and Data Dictionary, and the library DDL fixes the column names of its three objects; the grant table has no field id in any source and its columns are named after the legacy request and response fields.
- No approval is required to run a Draft migration on a development database; the migration is released to SIT only after the tests in section 16 pass.

### 4. Flow

1. The ACE database engineer checks out the rwb-access migration folder and confirms the highest applied version on the sequence (the V0001 baseline).
2. The engineer adds three migrations after that version, in this order: the library DDL application with its three objects, the `break_glass_grant` table with its constraint, and the grants with the partition and retention rows.
3. The engineer proves on an empty schema that each migration applies once, records its version and checksum, and that a second run reports no pending migration.
4. The engineer writes the grant script for the `rwb-access` login, scoped to schema `rwb_access` and to the four tables, plus the sequence usage the idempotency store needs.
5. The engineer creates the month partition of the access log on `decided_at`, with a default partition for a late-arriving entry and the retention class read from the parameter.
6. The migration pipeline applies the baseline and this story's migrations to an empty schema, then to a copy of the SIT schema, and runs the schema checks: keys, the two-person constraint, partitioning, grants, and a scan for any foreign key that names another schema.
7. The pipeline scans the chain's columns and a fixture of entries for a personal field: only the case id, the document id, the field id, the flag, the codes, the references, the versions and the times may appear.
8. The rollback is exercised on a copy: the four objects drop in reverse order, the appended chain keeps its rows, and a sequence re-apply returns the same shape.
9. The migrations are recorded in the release notes of the sequence, with their version numbers and their checksums, and the retention row is handed to the parameter load of RWB-P3-E1042-CON.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | A migration runs before the V0001 baseline | Flyway refuses with an unresolved baseline and nothing is applied | Pipeline error, no message id |
| X2 | An object of this story already exists in the sequence | The repeatable check refuses to re-create it and the migration is marked as already applied | Pipeline error, no message id |
| X3 | A foreign key names `rwb_decision` or another schema | The catalogue check fails the build; the key is removed and the reference is kept as a value | Check finding, no message id |
| X4 | The grant script runs before the login exists | The script fails on the missing role; the platform DB story creates the login first | Database error, no message id |
| X5 | The grant script grants to a shared or legacy login | The review rejects the script: one login per service (DP-02) | Review finding, no message id |
| X6 | A second active grant row is inserted for the same person | The two-person constraint refuses it; the application maps it to 409 with MSG-GEN-004 | MSG-GEN-004 through the application |
| X7 | The chain table is written with a column that could hold a personal value | The personal-data scan fails the build and the column is removed | Check finding, no message id |
| X8 | The rollback would drop the chain and lose committed entries | The rollback of this story drops only the objects it created; the chain's rows are never deleted | Review finding, no message id |
| X9 | The retention period is still open at release | The retention row carries the placeholder and the gap; the partition still exists with the default class | GAP-0782 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Three migrations, one grant script, one rollback and the partition rows on the service's own sequence; nothing to build against |
| Negotiable | Constraint and index names follow the platform naming library; the column set of the grant table is fixed by the legacy request and response fields |
| Valuable | The writer, the grant and the read have a schema that is granted, partitioned, retained and free of personal values |
| Estimable | Four tables, one constraint, two indexes, one partition scheme, one grant script and one rollback |
| Small | Days, not weeks, with the schema checks |
| Testable | Every criterion is a catalogue query or a pipeline run in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: rwb_access schema for the decision-record library objects and the break-glass grant

  Background:
    Given the rwb-access schema is rwb_access and the baseline version is V0001
    Given the grantee is the rwb-access login (DP-02), whose name is Not specified in the source documents (GAP-0782; ASM-1427)

  Scenario: AC1 The migrations apply in sequence on an empty schema (new, D-RCV-60)
    Given an empty rwb_access schema with the V0001 baseline applied
    When this story's three migrations and the grant script run in order
    Then each migration is recorded once on the service's Flyway history with its version and checksum
    Then a second run of the same pipeline changes nothing and reports no pending migration
    Then no migration in this story reuses a monolith migration name

  Scenario: AC2 The three library objects exist as the library DDL declares them (new, D-RCV-60)
    Given the library DDL of RWB-PLT-E1027-CON applied by this story
    When the catalogue is read
    Then outbox_event, processed_event and idempotency_key exist in rwb_access with the columns and the keys of the library template
    Then outbox_event holds the message id, the topic, the payload, the created time and the published time of each access entry
    Then idempotency_key holds the key, the request hash and the stored answer of the grant and end operations
    Then processed_event exists and holds no row, because this key consumes no event

  Scenario: AC3 break_glass_grant is created with its keys and the two-person constraint (new, D-RCV-60)
    Given the migration for the grant table
    When it is applied
    Then break_glass_grant has the columns of the legacy grant request and answer: grant_id, actor_user_id, incident_reference, iam_request_id, capability_area, right_code, scope_code, reason, state, starts_at and ends_at, plus the standard record columns
    Then the primary key is on grant_id and an index on actor_user_id and starts_at exists
    Then a constraint refuses a second row in state ACTIVE for the same actor_user_id
    Then ends_at is NOT NULL and state is limited to ACTIVE and ENDED
    Then no column of the table can hold a personal value, and reason is free text checked by the application

  Scenario: AC4 The grants belong to the rwb-access login and to no other (new, D-RCV-60)
    Given the grant script of this story
    When it runs
    Then the rwb-access login has usage on schema rwb_access and select, insert, update and delete on the four tables of this key
    Then no other login holds a grant on those tables and no grant on rwb_decision or on any other schema is present
    Then the login holds no right to alter the chain beyond insert, and no right to delete an appended entry

  Scenario: AC5 The access log is partitioned by month and retained as data (new, D-RCV-60)
    Given the decision-record table of the library applied by this story
    When the catalogue is read
    Then the table is partitioned by range on decided_at with one partition per month and a default partition
    Then the retention class and the retention period are parameter rows, and the period is Not specified in the source documents (GAP-0782; ASM-1429)
    Then the index on actor_user_id and decided_at exists, so the access read of a user and a period is indexed
    Then a partition drop is the only retention action and no row is deleted individually

  Scenario: AC6 No entry holds a personal value (new, D-RCV-60)
    Given the chain table and a fixture of access entries
    When the column list and the fixture are scanned
    Then no column of the chain holds a name, an identity number, a contact value or an address
    Then the clearest facts an entry carries are the case id, the document id, the field id and the flag clear or masked
    Then the actor is a staff user reference and the reason text of a grant is the only free text in the four tables
    Then the scan fails the build if a column or a fixture value of another kind appears

  Scenario: AC7 The rollback is complete and preserves the chain (new, D-RCV-60)
    Given the grant script and the rollback of this story
    When the rollback runs on a copy of the SIT schema
    Then the grants it made are revoked and the objects it created drop in reverse order
    Then the appended entries of the chain keep their rows, their hashes and their times
    Then a re-apply of the sequence returns the same shape and the same constraint
```

These criteria are new and test the database artefacts only: no legacy acceptance criterion is repeated, and every physical value (table, column, field id, constraint) is the legacy or library value, copied character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each service's objects live in its own schema under its own login; one login per service | DP-01, DP-02, DP-15 |
| BR2 | The access entry and its outbox row are committed in one transaction, so the record and its publication can never disagree | DP-03; Architecture v5 slide 28 |
| BR3 | The grant and the end operation are idempotent by key, and a repeated key returns the stored answer without a second entry | RWB-E1-039 AC10; DP-09 |
| BR4 | A person holds at most one active grant, and the database refuses a second active row for the same actor | Admin and access model, section 5.3; RWB-E1-039 BR5 |
| BR5 | An entry is append only: it is never updated and never deleted, and the retention action is a partition drop | RWB-E1-039 BR1; Architecture v5 slide 28 |
| BR6 | An access entry holds no personal value: the case id, the document id, the field id and the flag are its clearest facts | NFR-040; RWB-E1-039 BR3 |
| BR7 | The retention period and the partition granularity are parameter rows, never literals in a migration | DP-06; DL26 |
| BR8 | The tables of rwb-decision and of rwb-case are never referenced by a key here; the incident, the case and the document are values | DP-01; Ownership Map v1 |
| BR9 | The inbox table exists in every service schema and holds no row where the service consumes no event | DP-09; RWB-PLT-TE006-CON |

### 9. State transitions

None in the runtime sense: a table has no state machine. The states this story moves through are the migration states of the service's Flyway history (pending, applied, failed, undone), and the row states the schema exposes are the standard record columns plus the grant state ACTIVE and ENDED, which the application moves at `endsAt` or on an explicit end. A partition has the states ATTACHED, DETACHED and DROPPED, and the retention rule moves a month partition from ATTACHED to DROPPED after the period in force.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The ACE database engineer (any team, per U3) | Writes and runs the migrations, the grant script, the partition scheme and the rollback |
| The service owner of rwb-access | Approves a destructive change; none is planned here |
| The platform DB owner (RWB-PLT-E1044-CON, RWB-PLT-NF06-DB) | Owns the sequence, the baseline and the login policy |
| The owner of the retention rule (P5 rwb-document, per the ownership map) | Confirms the retention class and the period used by the parameter row |
| rwb-decision (P7) | Owns `decision_log_entry` and the central ledger; this schema holds no key to them |
| No delegation of authority level applies | A schema change is not a credit decision |

The grantee is named only as the rwb-access login (DP-02); its name is Not specified in the source documents (GAP-0782; ASM-1427). No personal name and no credential appears in a migration, a script or a runbook.

### 11. Data

| Table | Schema | Field identifiers | This story |
|---|---|---|---|
| the local decision-record table of the DP-03 library | rwb_access | DF-DEC-001 to DF-DEC-018, DF-DEC-030; the case id DF-DEC-002, the code DF-DEC-003, the actions DF-DEC-014 and the time DF-DEC-016 | Applies the library DDL, partitions it by month on decided_at, indexes actor and time, and grants it; the table name is the library's and no source names it in the ownership map (GAP-0782; ASM-1423) |
| outbox_event | rwb_access | The library template's columns; no field id in this story's source | Creates it through the library DDL; one row per access entry and per grant event, committed with the entry |
| idempotency_key | rwb_access | The library template's columns; no field id in this story's source | Creates it through the library DDL; the stored answer of the grant and end operations |
| processed_event | rwb_access | The library template's columns; no field id in this story's source | Creates it through the library DDL; holds no row for this key |
| break_glass_grant | rwb_access | None in the source: the columns are named after the legacy request and answer fields, and the field ids are Not specified in the source documents (GAP-0782; ASM-1428) | Creates the table, its keys, its two-person constraint and its index |
| role, permission, masking_rule, role_conflict, delegation_limit | rwb_access | DF-REF-034 to DF-REF-044, DF-REF-198 to DF-REF-204, DF-REF-016 to DF-REF-062 | Read dependencies of the app story: they are created by their own stories of this service and this story grants them without altering them |
| decision_log_entry, approval | rwb_decision | DF-DEC-001 to DF-DEC-030 | **Not created, not granted and not referenced.** P7 owns them; the central ledger consumes `rwb.decision-record.v1` and this schema holds no key to it |
| lov_value, reference_row, reference_version, parameter_catalog, parameter_value | rwb_case | DF-REF-027 to DF-REF-033; the reference tables | **Not created and not referenced.** P3 owns them (DP-06, DP-07) |

**No entry holds a personal value.** The chain table has no column for a name, an identity number, a contact value or an address; it carries the case id, the document id, the field id and the flag, the codes, the references, the versions and the times, and the actor as a staff user reference. The only free text in the four tables is the reason of a grant, which the application bounds and the run book tells the operator never to fill with customer data.

### 12. Contract

#### 12.1 REST operations provided

None. This is a database story and publishes no operation.

#### 12.2 REST operations consumed

None. The parameter load of the retention and partition rows is made by the platform reference-data path, not by this story.

#### 12.3 Events published

None. The outbox rows this story enables carry `rwb.decision-record.DecisionRecorded.v1`, which is the app story's publication through the DP-03 library and not an event of this story.

#### 12.4 Events consumed

None. The `processed_event` table is created empty because this key consumes no event.

#### 12.5 Workflows and activities

None.

#### 12.6 Schedules

None. The migration runs in the release pipeline and the retention action is a partition drop, not a Temporal Schedule; the six-monthly access review list (JOB-18) belongs to RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner (ownership map) | Created or altered here | Keys, indexes and constraints |
|---|---|---|---|
| the local decision-record table of the DP-03 library | P4, in rwb_access, under the library DDL | Applied as the library declares it, then partitioned by month on decided_at | Primary key on the entry id; index on actor_user_id and decided_at; month range partitions with a default partition; `prev_hash` and `entry_hash` NOT NULL |
| outbox_event | PLT library object, created in rwb_access | Created | Primary key on the message id; index on the published time for the relay |
| idempotency_key | PLT library object, created in rwb_access | Created | Primary key on the key; the stored answer and its request hash |
| processed_event | PLT library object, created in rwb_access | Created | Primary key on the event id and the consumer group; holds no row |
| break_glass_grant | P4, in rwb_access | Created | Primary key on grant_id; index on actor_user_id and starts_at; unique partial constraint on actor_user_id where state is ACTIVE; check on state ACTIVE or ENDED; ends_at NOT NULL |
| decision_log_entry, approval | P7 | Not touched | None here; the schema holds no key to `rwb_decision` |
| lov_value, reference_row, reference_version, parameter_catalog, parameter_value | P3 | Not touched | None here; the parameters and lists are read over their contract |

**`decision_log_entry` and the central ledger stay with P7 rwb-decision and this story creates nothing of theirs.** The four tables of this key are the three library objects and `break_glass_grant`; the chain table is the library's and this story applies it, partitions it and grants it. That the chain table has no name in the ownership map and that the grant table has no name in any source are the two open points of this story (GAP-0782; ASM-1423) and (GAP-0782; ASM-1428).

#### 12.8 Contract fakes

None. A database story uses no contract fake; it is tested against an empty schema and a copy of the SIT schema.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic is provisioned here; the outbox rows the schema enables are the app story's |
| Temporal | None | None | No workflow or Schedule |
| File | None | None | Migrations are deployed by the release pipeline, not by a file interface |

### 13. Solution plan

**Sequencing.** The service's Flyway sequence is owned by RWB-PLT-E1044-CON. The V0001 baseline creates the schema, the history table and the standard columns. This story adds the next versions after the baseline:

| Version | File | Contents |
|---|---|---|
| V0001 | baseline, from the platform DB story | Schema `rwb_access`, history table, standard columns |
| next after the baseline | `..._decision_record_library.sql` | Applies the DP-03 library DDL: the chain table, `outbox_event`, `processed_event` and `idempotency_key` |
| next after that | `..._break_glass_grant.sql` | Creates `break_glass_grant`, its index and the two-person constraint |
| next after that | `..._access_log_partitions_grants.sql` | The month partition scheme, the parameter rows of the retention class and the grants to the rwb-access login |

The legacy index `ix_declog_actor_time` on `decision_log_entry` is the source of the actor and time index of this story; the monolith name and number are not reused on the service sequence, and the index is created on the chain table of `rwb_access` instead. The exact version numbers are assigned by the sequence owner at build time; the order above is fixed by this story.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. This story applies the library DDL and creates the outbox, inbox and idempotency objects | referred to; the consuming story carries the dependency H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. The retention class and the retention period are parameter rows | referred to; the consuming story carries the dependency H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The event codes and the areas the entry carries are reference values and no copy is created here | referred to; the consuming story carries the dependency H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. No call is made by this story; the keys it creates support the app story's one-hop calls | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. No path is served here, and the schema serves the base of the app story only | none |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. No lake copy table, no lake watermark and no lake export object is created | none; no lake data is retained |
| DP-19 | Screen, ace-web | gateway-bff composite route. The screen reads the entries through the access-log operation and never through SQL | referred to; the consuming story carries the dependency H RWB-PLT-N001-CON |

**Table definitions**

`break_glass_grant` — `grant_id` uuid NOT NULL, `actor_user_id` uuid NOT NULL, `incident_reference` varchar(20) NOT NULL, `iam_request_id` varchar(40) NOT NULL, `capability_area` varchar(30) NOT NULL, `right_code` varchar(5) NOT NULL, `scope_code` varchar(8) NOT NULL, `reason` varchar(1000) NOT NULL, `state` varchar(10) NOT NULL, `starts_at` timestamptz NOT NULL, `ends_at` timestamptz NOT NULL, plus the standard record columns of the V0001 baseline. Primary key `(grant_id)`; index on `(actor_user_id, starts_at)`; a unique partial constraint on `(actor_user_id)` where `state = 'ACTIVE'`, so that a person holds at most one active grant and a second activation is refused by the database; check `state IN ('ACTIVE','ENDED')`; `ends_at` NOT NULL, because a grant without an end is not a grant (BR4, BR7).

The chain table, `outbox_event`, `processed_event` and `idempotency_key` take the column names, types and keys of the RWB-PLT-E1027-CON DDL template and are not restated here; the only addition this story makes to the chain is the month range partition on `decided_at` and the index on `(actor_user_id, decided_at)` that the legacy `ix_declog_actor_time` stands for.

**Retention and partitioning as data.**

| Item | Value |
|---|---|
| Partition key | `decided_at`, range, one partition per calendar month, with a default partition for a late entry |
| Index | `(actor_user_id, decided_at)`, so the access read of a user and a period is indexed and the ledger's five-minute collection is a range scan |
| Retention class | A parameter row of the rwb-case catalogue, read by the retention job of the platform and never by a literal |
| Retention period | Not specified in the source documents (GAP-0782; ASM-1429); DL26 is open |
| Retention action | Detach and drop a month partition older than the period in force; no row is deleted individually, so the append-only rule survives |
| Archive | The partition is archived under the decision log's rule before it is dropped; the archive target is the platform's and not this schema's |

**Grants.** `GRANT USAGE ON SCHEMA rwb_access TO <the rwb-access login>`; `GRANT SELECT, INSERT, UPDATE, DELETE ON break_glass_grant, outbox_event, processed_event, idempotency_key TO <the rwb-access login>`; `GRANT SELECT, INSERT ON` the chain table, with no `UPDATE` and no `DELETE`, so that an appended entry cannot be rewritten from the service (BR5); usage on the sequences those tables own. No grant to a shared login, no grant to another service's login, and no grant on `rwb_decision` or `rwb_case`. The grantee name is Not specified in the source documents (GAP-0782; ASM-1427).

**Rollback.** Per migration, in reverse order: the partition and grant migration is reversed by revoking the grants it made and dropping the parameter rows it added; the grant-table migration is reversed by dropping the constraint, the index and `break_glass_grant`; the library migration is reversed by dropping the three library objects, while the chain table keeps its rows and is never dropped by this story's rollback because it holds the appended entries (BR5, AC7). The rollback is exercised on a copy of the SIT schema and recorded in the runbook.

**Done when.** The migrations apply twice without a change, the catalogue checks pass, the two-person constraint refuses a second active grant, the personal-data scan finds no personal field, the grants are exactly as above, the rollback returns the schema to its pre-migration shape with the chain intact, and the tests in section 16 pass.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-004 | A second active grant row is inserted for the same actor; the application maps the constraint to 409 | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-002 | A grant reason reaches the database outside the 20 to 1000 bound | {field} must be between {min} and {max}. Raised by the application, not by a database constraint |
| Database error, no message id | A migration runs before the baseline or finds an object already present | The migration fails and nothing is applied; the pipeline stops |
| Database error, no message id | A grant script runs before the login exists | The script fails on the missing role; the platform DB story creates the login first |
| Check finding, no message id | A foreign key names another schema, or a column could hold a personal value | The pipeline check fails the build; the key or the column is removed |

The reason bound is deliberately in the application: it comes from the parameter `rwb.access.breakglass.reason-min` and its 1000 maximum, so a business person can change it without a migration (BR7). The database enforces what does not change: the keys, the two-person constraint, the partition, the append-only grant set and the schema boundary. Every message and its id is the legacy one and is raised by the app story.

### 15. Screens and states

No screen. The result of a migration is visible in the release pipeline and in the service's Flyway history: pending, applied, failed, undone, each with a version and a checksum. The partition list and the retention class are visible on the platform database dashboard. Nothing here is shown to a user directly, and SCR-43 Roles and access reads the entries through the access-log operation, never through SQL.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-039-DB-01 | AC1 | Component | Empty schema with V0001; the three migrations and the grant script; a second run; the Flyway history compared |
| TC-E1-039-DB-02 | AC2 | Component | Catalogue of outbox_event, processed_event and idempotency_key against the library DDL template; the empty inbox |
| TC-E1-039-DB-03 | AC3 | Component | Catalogue of break_glass_grant: columns, NOT NULL, primary key, index, the unique partial constraint on the active grant, the state check |
| TC-E1-039-DB-04 | AC4 | Component | Grant script run per login; the privileges listed per table; the refusal of update and delete on the chain |
| TC-E1-039-DB-05 | AC5 | Component | Partition list of the chain table, the default partition, the actor and time index, the retention parameter rows and the drop of an old month |
| TC-E1-039-DB-06 | AC6 | Component | Column scan and a fixture of access entries: the case id, the document id, the field id and the flag, and the refusal of any other kind of column |
| TC-E1-039-DB-07 | AC7 | Component | Rollback on a copy of the SIT schema; grants revoked; the chain rows, hashes and times preserved; the re-apply |

### 17. Guardrails

- No business value in a constraint: the reason bounds and the retention period are parameter data, read through the parameter contract (DP-06, BR7).
- No personal data in a migration, a script, a fixture or a runbook: the case id, the document id, the field id and the flag only, and the actor as a staff user reference (BR6).
- No read of another schema and no key into another schema: `rwb_access` objects reference `rwb_access` objects only (DP-01, BR8).
- One login per service: the rwb-access login is the only grantee, and its name is Not specified in the source documents (GAP-0782; ASM-1427).
- No destructive change: an appended entry is never updated or deleted, the chain is never dropped by a rollback of this story, and the retention action is a partition drop (BR5).
- The sequence is per service and linear: no monolith migration name is reused and no object is created twice (DP-15).
- No table of rwb-decision or rwb-case is created, granted or referenced from here (BR8).
- The obligations of the bank IAM, the SOC logging path and the alerts are not database objects and are not created here.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-ACA-006 | Every read of the case store and the document store written to the access log | Epic 1, 3.4 | FEAT-ACA-007, FEAT-ACA-008 | BR2, BR5, BR6, BR9 | TC-E1-039-DB-01, TC-E1-039-DB-02, TC-E1-039-DB-05, TC-E1-039-DB-06 |
| REQ-ACA-008 | Break-glass with its own approval, written to the access log | Epic 1, 3.4 | FEAT-ACA-009, FEAT-ACA-010 | BR3, BR4, BR7 | TC-E1-039-DB-03, TC-E1-039-DB-04, TC-E1-039-DB-07 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1039-APP | App development | X dependency tracked: the story that writes the four tables and reads the chain |
| RWB-P4-E1039-CON | Contract | Sibling: the entry and grant shapes in its section 11 must match this schema |
| RWB-P4-E1039-OPS | DevOps | X dependency tracked: the deployment of the migration job, and the alerts of a failed grant or entry write |
| RWB-PLT-E1027-CON | Contract | The library DDL template of the chain, the outbox, the inbox and the idempotency store |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence and its version allocation |
| RWB-PLT-NF06-DB | ACE DB | The schema split and the baseline of `rwb_access` |
| RWB-P7-E1039-APP | App development | Neighbour of the same legacy key on the ledger side: owns the table this schema must never hold |
| RWB-P5-E1039-APP | App development | Neighbour of the same legacy key on the document side: writes its entry to this shape in its own schema |
| RWB-ITG-E1039-ITG | Integration | The end-to-end proof that reads the entries this schema holds |

The legacy test cases of this key — TC-E1-039-01, TC-E1-039-02, TC-E1-039-03, TC-E1-039-04, TC-E1-039-05, TC-E1-039-06, TC-E1-039-07, TC-E1-039-08, TC-E1-039-09, TC-E1-039-10, TC-E1-039-11 and TC-E1-039-12 — are executed by RWB-P4-E1039-APP and, as the cross-service copy, by RWB-ITG-E1039-ITG; this story proves the schema beneath them.

### 19. Out of scope

- The application code of the writer, the grant and the read: RWB-P4-E1039-APP.
- The published contract of the four operations and its fakes: RWB-P4-E1039-CON.
- The Helm chart, the migration job, the Kafka ACLs, the secrets, the alerts and the run book: RWB-P4-E1039-OPS.
- The chain table's own DDL, its hash columns and its library behaviour: RWB-PLT-E1027-CON; this story applies it and does not redefine it.
- `decision_log_entry`, `approval`, the central ledger, the five-minute collection and the chain verification: P7 rwb-decision and RWB-P7-E1039-APP.
- `lov_value`, `reference_row`, `reference_version`, `parameter_catalog` and `parameter_value`: P3 rwb-case; the retention and partition rows are loaded over that contract.
- The role, permission, masking and delegation tables and their migrations: the other stories of RWB-SVC-P4.
- The retention job implementation and the archive target of the platform: the platform DB and retention work.
- Data migration from the monolith's `decision_log_entry` and its reconciliation: the migration work of the programme, not this story.
- Performance tuning beyond the index on actor and time and the month partition: the non-functional work.
