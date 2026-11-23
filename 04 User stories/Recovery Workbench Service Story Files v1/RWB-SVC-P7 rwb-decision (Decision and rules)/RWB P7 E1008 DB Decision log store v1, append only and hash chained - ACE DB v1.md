# RWB-P7-E1008-DB Decision log store v1, append only and hash chained

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: database slice of RWB-E1-008 for rwb-decision — `decision_log_entry` in schema `rwb_decision` on the per-service Flyway sequence, the append-only enforcement of grant plus trigger, the chain columns, the indexes, the grants, the login and the three library objects. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E1008-DB |
| Work type | DB (ACE DB) |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P7-D |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-001, FR-P7-003, FR-P7-004, FR-P7-005, FR-P7-006, FR-P7-009, FR-P7-010, FR-P7-011, FR-P7-012, FR-P7-013, FR-P7-029, FR-P7-036) |
| Status | Draft (realignment v1) |

### 1. Story

As an **ACE database engineer**, I want **the central decision ledger created in schema `rwb_decision` on the per-service Flyway sequence — `decision_log_entry` with its thirty columns, its chain columns, its keys and its indexes, the append-only enforcement of a missing UPDATE and DELETE grant plus the trigger `tr_declog_append_only` and the function `refuse_change`, the three library objects of the event platform, the grants of the `rwb-decision` login and a tested rollback — **so that** the ledger of legacy RWB-E1-008 can hold every entry of every service immutably in its own schema, no other service can reach it, and a change made outside the service is impossible or detectable.

This is the database slice of RWB-E1-008. It delivers, in schema `rwb_decision`:

- the migration that creates `decision_log_entry` after the V0001 baseline, with the twenty-two columns and physical types of the legacy `Recovery Workbench Physical Schema v6.sql` and of TSD P7 v2 T3.1 (DF-DEC-001 to DF-DEC-031) plus the seven standard record columns;
- the **append-only guarantee** in its three parts: no UPDATE and no DELETE grant for the service login, the trigger `tr_declog_append_only BEFORE UPDATE OR DELETE ON decision_log_entry FOR EACH ROW EXECUTE FUNCTION refuse_change()`, and the owner separated from the service it serves so that the trigger is the owner's own guard;
- the **hash-chain columns** `chain_seq bigint NOT NULL`, `prev_hash char(64) NOT NULL` and `entry_hash char(64) NOT NULL`, with the unique key on `chain_seq` that makes a chain position single, and the unique key on `idempotency_key` that makes a record single;
- the **indexes** the two reads and the verifier need: the primary key on `id`, the unique `chain_seq`, `ix_declog_case_time` on `(case_id, decided_at)`, the legacy `ix_declog_actor_time` on `(actor_user_id, decided_at)`, the legacy `ix_declog_rule` on `(rule_id, rule_version)`, `ix_decision_log_entry_case_id` and `ix_decision_log_entry_corrects_entry_id`;
- the **three library objects** `outbox_event`, `processed_event` and `idempotency_key` created from the event platform template in this schema, because every service writes its own outbox and inbox in its own schema;
- the **grants and the login** of the service (DP-02, DP-15), whose name is Not specified in the source documents (GAP-1232; ASM-2196);
- the explicit statement that the schema holds **no foreign key, no view and no grant that names another schema**: `case_id` is a plain uuid and not a key into `rwb_case` (DP-01), and `delegation_limit`, `parameter_catalog`, `reference_row`, `approval` and `rule_*` are not created here.

The eight legacy acceptance criteria stay with `RWB-P7-E1008-APP`; every criterion in section 7 is new (D-RCV-60) and tests only the schema deliverable.

### 2. Business rationale

The legacy story added one migration, `V_E1_008__declog_chain.sql`, to a single `recovery` schema of 92 tables with one shared login, and it relied on `decision_log_entry` having been created by RWB-E1-001. Two of its three guarantees were database statements — the missing grant and the trigger — and the third was code. After the split the table moves to `rwb_decision` (Ownership Map, `decision_log_entry`, P7; Architecture v5 slide 41), and the same three guarantees must survive the move intact, because they are the reason Audit can rely on the log at all (REQ-DRI-002, CTL-06, ADR-009 and ADR-022).

The append-only pair is deliberately two mechanisms and not one. A grant alone is defeated by the owner of the table, and a trigger alone is defeated by anyone who may disable it; together they cover the two roles that could change a row (legacy AC1 tests both in one scenario, and the chain check of AC4 covers the third route, a change made with the trigger disabled). This story therefore creates the table under a schema owner that the service never uses to write, grants the service login INSERT and SELECT only, and installs `refuse_change` as the owner's guard.

The chain columns are the contract with the algorithm. `char(64)` is fixed by DF-DEC-017 and DF-DEC-018 and by the DDL of the legacy schema; the unique key on `chain_seq` is what makes "the entry before" unambiguous in a parallel append, and the unique key on `idempotency_key` is what makes a repeated envelope a repeat and not a second decision. The index set is the legacy set plus the two the two reads add, so the query by case and date and the query by actor and date are both indexed and the verifier's sequential walk is a primary-key scan.

Three deltas are the schema's own statement of the target. `case_id` loses its foreign key: a key into `rwb_case` would be a cross-schema key, which DP-01 forbids and the boundary test fails, so the case is an identifier and its existence is checked over P3's contract. The three library objects exist here and not in `rwb_integration`, because the outbox and the inbox are the producer's and the consumer's own. And no data-lake object, no watermark and no partition table appears: the copy is retired (DP-17) and the ledger keeps its chain and its daily seal instead.

### 3. Preconditions

- The V0001 baseline of `rwb_decision` exists on the per-service Flyway sequence from RWB-PLT-E1044-CON and the platform DB work: the schema, the `flyway_schema_history` table and the standard record columns of TSD P7 v2 T3.0 (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`).
- The ACE database and the per-service login policy are in place; the login of `rwb-decision` is created by the platform DB work and its name is Not specified in the source documents (GAP-1232; ASM-2196).
- The ownership map is the only source of table ownership: `decision_log_entry`, `approval`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7 and in `rwb_decision`; `delegation_limit` is P4 and in `rwb_access`; `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` and `lov_value` are P3 and in `rwb_case`; the ACE views are P1's.
- The column set, the types and the constraints are the legacy physical schema's, character for character, and the field identifiers are TSD P7 v2 T3.1's (DF-DEC-001 to DF-DEC-031).
- The trigger body is the legacy one: `RAISE EXCEPTION '% is append only: % refused', TG_TABLE_NAME, TG_OP`, which is what makes the message read `decision_log_entry is append only` in AC1.
- The three library objects follow the template of the event platform (RWB-PLT-TE006-CON); their column set is not restated here and is not fixed by any source of this read set (GAP-1232; ASM-2196).
- No approval is required to run a Draft migration on a development database; the migration is released to SIT only after the checks of section 16 pass.

### 4. Flow

1. The ACE database engineer checks out the `rwb-decision` migration folder and confirms the highest applied version on the sequence (the V0001 baseline).
2. The engineer adds this story's migration after that version, with a guard that refuses to run before the baseline.
3. The engineer creates `decision_log_entry` with the twenty-two columns of section 13 and the seven standard record columns, in the order of the physical schema.
4. The engineer adds the keys: primary key on `id`, unique `uk_decision_log_entry (entry_hash, chain_seq, idempotency_key)`, unique `uk_decision_log_entry_chain_seq (chain_seq)`, unique `uk_decision_log_entry_idempotency_key (idempotency_key)`.
5. The engineer adds the indexes: `ix_decision_log_entry_case_id`, `ix_decision_log_entry_corrects_entry_id`, `ix_declog_case_time (case_id, decided_at)`, `ix_declog_actor_time (actor_user_id, decided_at)` and `ix_declog_rule (rule_id, rule_version)`.
6. The engineer creates the function `refuse_change()` and the trigger `tr_declog_append_only` on `decision_log_entry` only; the interaction ledger's trigger of the same function is P1's and is not created here.
7. The engineer applies the event platform's template for `outbox_event`, `processed_event` and `idempotency_key` in `rwb_decision`, unchanged.
8. The engineer writes the grant script for the `rwb-decision` login: usage on the schema, `SELECT, INSERT` on `decision_log_entry`, `SELECT, INSERT, UPDATE, DELETE` on the three library objects, and usage on the sequences those objects own; no UPDATE and no DELETE on the ledger, and nothing to any other login.
9. The engineer writes the rollback: the undo per migration in reverse order, with the ledger rows preserved where a later change only adds an object.
10. The pipeline applies the baseline and this story's migrations to an empty schema and then to a copy of the SIT schema, and runs the catalogue checks: keys, indexes, trigger, function, grants, and a scan for any foreign key, view, synonym or grant that names another schema or `public`.
11. The check that the ledger has no UPDATE and no DELETE grant for the service login and no write path through a view is a catalogue query: any hit fails the build (BR2).
12. The append-only pair is exercised: an UPDATE and a DELETE as the service login fail on the grant, and the same two as the schema owner fail with `decision_log_entry is append only: UPDATE refused`.
13. The rollback is exercised on a copy: the schema returns to its pre-migration shape and the library objects are dropped last.
14. The migration is recorded in the release notes of the sequence with its version and its checksum.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | A migration runs before the V0001 baseline | Flyway refuses with an unresolved baseline and nothing is applied | Pipeline error, no message id |
| X2 | `decision_log_entry` already exists in the sequence | The repeatable guard refuses to re-create it and the migration is marked as already applied | Pipeline error, no message id |
| X3 | A foreign key, view, synonym or grant names another schema or `public` | The catalogue check fails the build; the object is removed and the value is read over a contract instead | Check finding, no message id |
| X4 | The grant script grants UPDATE or DELETE on `decision_log_entry` | The grant check fails the build; the ledger is append only (BR2) | Check finding, no message id |
| X5 | The trigger `tr_declog_append_only` is missing or disabled on a fresh apply | The object check fails the build; the trigger is part of the migration | Check finding, no message id |
| X6 | The grant script runs before the login exists | The script fails on the missing role; the platform DB story creates the login first | Database error, no message id |
| X7 | `case_id` carries a foreign key into `rwb_case`, or `delegation_limit` is created here | The boundary and ownership checks fail the build; both are other owners' | Check finding, no message id |
| X8 | A column is needed but no field identifier exists | The column is not invented: it carries the placeholder and the gap is raised | GAP-1232 |
| X9 | The rollback would drop `decision_log_entry` and lose the chain | The rollback drops only what this migration added and keeps the table and its rows | Review finding, no message id |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One migration, one trigger, one grant script and a rollback on the service's own sequence; nothing to build against |
| Negotiable | Constraint and index names follow the platform naming library; the column set is fixed by the field identifiers and the legacy physical schema |
| Valuable | The ledger has a schema that is granted, indexed, append-only three ways and reversible, and no other service can reach it |
| Estimable | One table, one function and one trigger, five indexes, one grant script, three library objects, one rollback |
| Small | Days, not weeks, with the catalogue checks |
| Testable | Every criterion is a catalogue query or a pipeline run in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: rwb_decision schema for the central decision ledger

  Background:
    Given the rwb-decision schema is rwb_decision and the baseline version is V0001
    Given the grantee is the rwb-decision login (DP-02), whose name is Not specified in the source documents (GAP-1232; ASM-2196)

  Scenario: AC1 The migration applies in sequence on an empty schema (new, D-RCV-60)
    Given an empty rwb_decision schema with the V0001 baseline applied
    When this story's migrations and grant script run in order
    Then each migration is recorded once on the service's Flyway history with its version and its checksum
    Then a second run of the same pipeline changes nothing and reports no pending migration
    Then no migration of this story reuses the monolith migration name V_E1_008__declog_chain.sql

  Scenario: AC2 decision_log_entry is created with its columns and physical types (new, D-RCV-60)
    Given the migration for decision_log_entry
    When it is applied
    Then the table carries id, case_id, decision_code, rule_id, rule_version, model_version, agent_version, inputs_ref, recommendation, approver_user_id, approval_level, final_call, override_reason, actions, outcome, decided_at, prev_hash, entry_hash, chain_seq, corrects_entry_id, actor_user_id and idempotency_key of DF-DEC-001 to DF-DEC-031
    Then it carries the standard record columns is_active, state, version, created_at, created_by, updated_at and updated_by
    Then the types are the legacy physical types: decision_code varchar(8) NOT NULL, inputs_ref varchar(400) NOT NULL, final_call varchar(40) NOT NULL, override_reason varchar(1000), recommendation, actions and outcome jsonb, decided_at timestamptz NOT NULL, prev_hash and entry_hash char(64) NOT NULL, chain_seq bigint NOT NULL, idempotency_key varchar(80)
    Then the primary key is on id, and there is no foreign key on case_id and no key into another schema
    Then the structural check constraint ck_declog_case allows a row when case_id is not null or decision_code starts with "AC-", and carries no list of decision codes

  Scenario: AC3 The append-only guarantee holds for the service login and for the schema owner (new, D-RCV-60)
    Given the grant script and the trigger tr_declog_append_only of this story
    When an UPDATE and a DELETE are attempted as the rwb-decision login and again as the schema owner
    Then the login is refused all four statements by the missing UPDATE and DELETE grant
    Then the schema owner is refused with the message "decision_log_entry is append only: UPDATE refused" and "... DELETE refused" from the function refuse_change
    Then an INSERT as the login succeeds and the row is readable
    Then the catalogue shows no UPDATE grant and no DELETE grant on decision_log_entry for any login other than the schema owner, and no view with a write rule

  Scenario: AC4 The chain columns are constrained and indexed (new, D-RCV-60)
    Given the applied table
    When the catalogue is read for constraints and indexes
    Then chain_seq is bigint NOT NULL with a unique key, so one chain position exists once
    Then prev_hash and entry_hash are char(64) NOT NULL
    Then idempotency_key has a unique key, and a repeated key is refused with a unique violation
    Then the indexes ix_declog_case_time on (case_id, decided_at), ix_declog_actor_time on (actor_user_id, decided_at) and ix_declog_rule on (rule_id, rule_version) exist, with ix_decision_log_entry_case_id and ix_decision_log_entry_corrects_entry_id
    Then a first entry can be inserted with prev_hash of 64 zeros and an entry_hash of 64 lower-case hexadecimal characters, and a second with prev_hash equal to the first entry_hash

  Scenario: AC5 The three library objects exist in rwb_decision from the event platform template (new, D-RCV-60)
    Given the event platform template published by RWB-PLT-TE006-CON
    When this story's migration for the library objects is applied
    Then outbox_event, processed_event and idempotency_key exist in schema rwb_decision
    Then each object is created from the template unchanged, with no column renamed, added or dropped in this story
    Then the three objects carry their own keys and no foreign key into decision_log_entry
    Then no other schema holds this service's outbox or inbox row

  Scenario: AC6 The schema holds no object of another owner and no cross-schema key (new, D-RCV-60)
    Given the applied schema
    When the catalogue query for tables, columns, foreign keys, views, synonyms and grants runs
    Then no foreign key, view, synonym or grant in rwb_decision names rwb_case, rwb_access, the recovery schema, an ACE schema or public
    Then delegation_limit, parameter_catalog, parameter_value, reference_row, reference_version and lov_value are absent from the schema
    Then approval, rule_package, rule_package_version, rule_row and rule_test_case are absent from this story's migration
    Then no data-lake object, watermark table or partition table exists, because the copy is retired under DP-17

  Scenario: AC7 The grants and the rollback are complete and safe (new, D-RCV-60)
    Given the grant script and the rollback of this story
    When the grant script runs and then the rollback runs on a copy
    Then the rwb-decision login has usage on the schema, SELECT and INSERT on decision_log_entry, SELECT and INSERT and UPDATE and DELETE on outbox_event, processed_event and idempotency_key, and usage on the sequences those objects own
    Then no other login holds a grant on any of the four objects
    Then the rollback drops the library objects, then the trigger and the function, then the table, in reverse order
    Then the ledger rows inserted between the two runs keep their id and chain_seq where the rollback only reverses an added object
```

These criteria are new and test the database artefacts only: no legacy acceptance criterion is repeated, and every physical value — table, column, type, constraint name, index name, trigger name, function name, migration name and the refusal message — is the legacy or technical-specification value, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The ledger row carries the seven field groups of REQ-DRI-001 with the field identifiers and physical types of TSD P7 v2 T3.1 | REQ-DRI-001; DF-DEC-001 to DF-DEC-031 |
| BR2 | A stored entry is never updated or deleted: the service login has no UPDATE and no DELETE grant, and the trigger `tr_declog_append_only` refuses both for the schema owner | REQ-DRI-002; R-UNI-24; legacy AC1; ADR-009 |
| BR3 | `chain_seq` is unique and `prev_hash` is the `entry_hash` of the entry before, 64 zeros for the first; `entry_hash` and `prev_hash` are 64 characters | REQ-DRI-003; DF-DEC-017, DF-DEC-018, DF-DEC-028 |
| BR4 | A repeated `idempotency_key` is refused by a unique key, so a repeated envelope cannot become a second entry | R-UNI-40; DF-DEC-031 |
| BR5 | Each service's objects live in its own schema under its own login; one login per service | DP-01, DP-02, DP-15; Architecture v5 slide 29 |
| BR6 | No foreign key, view or grant crosses a schema boundary: `case_id` is an identifier and the case exists in P3's contract | DP-01; Architecture v5 slide 29 |
| BR7 | Every service writes its own outbox and inbox in its own schema, so the three library objects are created here | Ownership Map ruling on `outbox_event`, `processed_event` and `idempotency_key`; Architecture v5 slides 11 and 20 |
| BR8 | No business value is fixed by a constraint: the decision codes, approval levels and limits are rows of other owners, and no check constraint carries them | DP-07; Principle 1 |
| BR9 | The retention class is a property of the bank schedule and not of the schema; no row is deleted by a job of this story | DL26; BR2 |

### 9. State transitions

None in the runtime sense: a table has no state machine, and a stored entry has no states. The states this story moves through are the migration states of the service's Flyway history — pending, applied, failed, undone — and the row-level columns the schema exposes are the standard ones of TSD P7 v2 T3.0. The ingest states of an envelope and the chain-check states of a business date are the app story's and leave no additional column here.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | Migration applied | The baseline is present and the objects do not exist | Applied (table, trigger, function, indexes, library objects, grants) |
| Applied | Migration fails part way | A statement fails | Failed (rolled back, the pod does not become ready) |
| Applied | Rollback run on a copy | The reverse order is followed | Undone (the library objects, the trigger, the function, then the table) |
| Applied | A second pipeline run | Nothing is pending | Applied (no change, no new checksum) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The ACE database engineer (any team, per U3) | Writes and runs the migration, the trigger, the grant script and the rollback |
| The service owner of rwb-decision | Approves a destructive change; none is planned here |
| The platform DB owner (RWB-PLT-E1044-CON, the platform DB story) | Owns the sequence, the baseline, the login policy and the connection pool per login |
| RW-PLATADM Platform administrator | Reads the migration runs on the job monitor; the ledger itself is not theirs to change |
| RW-AUDIT Internal audit | Reads ledger rows through the service's two operations, never through SQL |
| The schema owner | Owns the objects and is refused an update or a delete by its own trigger |
| No delegation of authority level applies | A schema change is not a credit decision |

The grantee is named only as the `rwb-decision` login (DP-02); its name is Not specified in the source documents (GAP-1232; ASM-2196). No personal name and no credential appears in a migration, a script or a run book.

### 11. Data

| Table | Schema | Field identifiers | This story |
|---|---|---|---|
| `decision_log_entry` | `rwb_decision` | DF-DEC-001 to DF-DEC-031 | Creates the table, the four keys, the five indexes, the trigger and the function; the app story writes and reads the rows |
| `outbox_event` | `rwb_decision` | No field identifier in this read set (GAP-1232; ASM-2196) | Creates the object from the event platform template, unchanged |
| `processed_event` | `rwb_decision` | No field identifier in this read set (GAP-1232; ASM-2196) | Creates the object from the event platform template, unchanged |
| `idempotency_key` | `rwb_decision` | No field identifier in this read set (GAP-1232; ASM-2196) | Creates the object from the event platform template, unchanged |
| `approval`, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | `rwb_decision` | DF-DEC-032 to DF-DEC-053 for `approval` | **Not created here**: P7 owns them and their migrations are the approval and rule-registry stories' |
| `delegation_limit` | `rwb_access` | DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 | **Not created and not referenced.** P4 owns the DoA table (Ownership Map ruling); the ledger stores `approval_level`, not a limit |
| `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version`, `lov_value` | `rwb_case` | DF-REF-027 to DF-REF-033; DF-REF-181 to DF-REF-184; DF-REF-159 to DF-REF-180 | **Not created and not referenced.** P3 owns them (DP-07); the values arrive over the reference-data contract |
| `recovery_case`, `task`, `timer`, `queue` | `rwb_case` | Not in this read set | **Not created and not referenced.** `case_id` is a plain uuid with no key across the boundary |
| No lake object, no watermark, no partition table | — | — | **None, by design**: the copy to the data lake is retired (DP-17, ADR-018) |

Field IDs are those in the Logical Data Model and Data Dictionary. The three library objects carry no field identifier in this read set, so this story applies the published template and restates none of its columns.

### 12. Contract

#### 12.1 REST operations provided

None. This is a database story and publishes no operation.

#### 12.2 REST operations consumed

None by this story. The values the table carries arrive through the ingest of the app story, and the codes and levels arrive over P3's reference-data contract, which the app story consumes.

#### 12.3 Events published

None. The outbox object is created here so that the service can publish later; this story writes no event row and publishes nothing.

#### 12.4 Events consumed

None. The inbox object is created here so that the service can consume idempotently later; this story consumes nothing.

#### 12.5 Workflows and activities

None. The migration runs in the release pipeline and not on a Temporal workflow.

#### 12.6 Schedules

None. The migration runs in the release pipeline; the 02:00 chain check is a Schedule of the app story and writes no table of this story.

#### 12.7 Tables owned

| Table | Owner (ownership map) | Created or altered here | Keys and indexes |
|---|---|---|---|
| `decision_log_entry` | P7 | Created | PK on `id`; unique `uk_decision_log_entry (entry_hash, chain_seq, idempotency_key)`; unique `uk_decision_log_entry_chain_seq (chain_seq)`; unique `uk_decision_log_entry_idempotency_key (idempotency_key)`; `ix_declog_case_time (case_id, decided_at)`; `ix_declog_actor_time (actor_user_id, decided_at)`; `ix_declog_rule (rule_id, rule_version)`; `ix_decision_log_entry_case_id`; `ix_decision_log_entry_corrects_entry_id` |
| `outbox_event` | PLT (library object, created in this schema) | Created from the event platform template | The template's keys, unchanged |
| `processed_event` | PLT (library object, created in this schema) | Created from the event platform template | The template's keys, unchanged |
| `idempotency_key` | PLT (library object, created in this schema) | Created from the event platform template | The template's keys, unchanged |
| `approval`, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 | Not touched | Their own stories' migrations |
| `delegation_limit` | P4 | Not touched and not referenced | No key and no view names `rwb_access` |
| `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version`, `lov_value` | P3 | Not touched and not referenced | No key, no view and no grant names `rwb_case` |

#### 12.8 Contract fakes

None. A database story uses no contract fake; it is tested against an empty schema and a copy of the SIT schema.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic in this story; the outbox and inbox objects are created for later use |
| Temporal | None | None | No workflow and no Schedule |
| File | None | None | Migrations are deployed by the release pipeline, not by a file interface |

### 13. Solution plan

**Sequencing.** The service's Flyway sequence is owned by RWB-PLT-E1044-CON. The V0001 baseline creates the schema, the history table and the standard columns. This story adds the next versions after the baseline:

| Version | File | Contents |
|---|---|---|
| V0001 | baseline, from the platform DB story | Schema `rwb_decision`, history table, standard columns |
| next after the baseline | `..._decision_log_entry.sql` | Creates `decision_log_entry` with its columns, keys and indexes |
| next after that | `..._declog_append_only.sql` | Creates the function `refuse_change()` and the trigger `tr_declog_append_only` |
| next after that | `..._event_library_objects.sql` | Creates `outbox_event`, `processed_event` and `idempotency_key` from the event platform template |
| next after that | `..._decision_grants.sql` | Usage on the schema, the ledger grants and the library grants for the `rwb-decision` login |

The legacy migration name `V_E1_008__declog_chain.sql` is recorded as the source of the chain columns; the monolith name and number are not reused on the service sequence. The exact version numbers are assigned by the sequence owner at build time; the order above is fixed by this story.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The table and the three library objects live in `rwb_decision` | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. The library writes its record into the service's own tables, which the writer stories own | H RWB-PLT-E1027-CON (carried by the writer's story; named here) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. `lov_value` and the reference tables are never created or read here | referred to; the consuming story carries the dependency |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit. The chain check is a Schedule and writes no table of this story | referred to; the consuming story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The schema name follows the same short name: `rwb_decision` under `/api/recovery/decision/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. This story adds four migrations after the baseline and reuses no monolith name | H RWB-PLT-E1044-CON (the sequence owner; named here) |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. No lake object, watermark or partition exists | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route. No screen reads this schema; the edge reads the two operations | referred to; the consuming story carries the dependency |

The patterns **not claimed** here are DP-02 (one login per service — delivered by the platform DB work and used, not designed, here), DP-04, DP-05, DP-06, DP-08, DP-09 (the library objects are applied from the template and the platform contract is not a dependency of this story), DP-11, DP-12, DP-14, DP-16, DP-18 and DP-20.

**Table definition.** `decision_log_entry` — `id uuid PRIMARY KEY DEFAULT gen_random_uuid()`, `case_id uuid`, `decision_code varchar(8) NOT NULL`, `rule_id varchar(20)`, `rule_version varchar(20)`, `model_version varchar(40)`, `agent_version varchar(40)`, `inputs_ref varchar(400) NOT NULL`, `recommendation jsonb`, `approver_user_id uuid`, `approval_level varchar(4)`, `final_call varchar(40) NOT NULL`, `override_reason varchar(1000)`, `actions jsonb`, `outcome jsonb`, `decided_at timestamptz NOT NULL DEFAULT now()`, `prev_hash char(64) NOT NULL`, `entry_hash char(64) NOT NULL`, `chain_seq bigint NOT NULL`, `corrects_entry_id uuid`, `actor_user_id uuid`, `idempotency_key varchar(80)`, plus `is_active boolean NOT NULL DEFAULT true`, `state varchar(40)`, `version integer NOT NULL DEFAULT 1`, `created_at timestamptz NOT NULL DEFAULT now()`, `created_by uuid`, `updated_at timestamptz NOT NULL DEFAULT now()`, `updated_by uuid`. The three unique constraints are `UNIQUE (entry_hash, chain_seq, idempotency_key)`, `UNIQUE (chain_seq)` and `UNIQUE (idempotency_key)`.

**Append-only enforcement.** `CREATE OR REPLACE FUNCTION refuse_change() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION '% is append only: % refused', TG_TABLE_NAME, TG_OP; END; $$;` and `CREATE TRIGGER tr_declog_append_only BEFORE UPDATE OR DELETE ON decision_log_entry FOR EACH ROW EXECUTE FUNCTION refuse_change();`. The function is created once in `rwb_decision`; the interaction ledger's trigger of the same function is P1's and is not this story's. The service login receives `SELECT, INSERT` and nothing else on the table, which is the first half of AC1; the trigger is the second half, and the chain check of the app story is the third.

**No cross-schema key.** `case_id` is a uuid and carries no foreign key, although the legacy schema declared `fk_decision_log_entry_case_id` to `recovery_case` and TSD P7 v2 T3.3 declares the relationship: in the target the case is P3's row in another schema, so the key would cross a boundary that DP-01 forbids and the boundary test fails. The case is verified through P3's contract on the read (GAP-1231; ASM-2195). `corrects_entry_id` names an entry of the same table and keeps its self-reference at the application level, not as a database key, for the same reason the chain is advisory-locked rather than key-enforced.

**No business value in a constraint.** The decision codes, the approval levels and the rule identifiers are values of a list or a rule package of another owner. No check constraint carries them: a new code must be a data change, not a migration (BR8). The one check the legacy story added — `ck_declog_case (case_id IS NOT NULL OR decision_code LIKE 'AC-%')` — is kept as a business-free structural rule: an entry either names a case or is an access event, and an access event is any code that starts with `AC-`.

**Library objects.** `outbox_event`, `processed_event` and `idempotency_key` are created in `rwb_decision` from the template published by the event platform (RWB-PLT-TE006-CON) and are not modified here.

**Grants.** `GRANT USAGE ON SCHEMA rwb_decision TO <the rwb-decision login>`; `GRANT SELECT, INSERT ON decision_log_entry TO <the rwb-decision login>`; `GRANT SELECT, INSERT, UPDATE, DELETE ON outbox_event, processed_event, idempotency_key TO <the rwb-decision login>`; usage on the sequences those objects own. No UPDATE and no DELETE on the ledger, no grant to a shared login, no grant to another service's login, and no grant on `rwb_case`, `rwb_access` or an ACE schema. The grantee name is Not specified in the source documents (GAP-1232; ASM-2196).

**Rollback.** Per migration, in reverse order: the grant script is reversed by revoking the grants it made; the library objects, then the trigger and the function, then the table are dropped. A ledger row inserted between the two runs keeps its `id` and `chain_seq` where the rollback only reverses an added object, so a later re-apply never rewrites a chain position (BR9). The rollback is exercised on a copy of the SIT schema and recorded in the run book.

**Done when.** The migrations apply twice without a change, the catalogue checks pass, the append-only pair is proven for the login and for the owner, no cross-schema object exists, the rollback returns the schema to its pre-migration shape, and the tests in section 16 pass.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Database error, no message id | A migration runs before the baseline or finds an object already present | The migration fails and nothing is applied; the pipeline stops |
| Database error, no message id | A grant script runs before the login exists | The script fails on the missing role; the platform DB story creates the login first |
| Check finding, no message id | A foreign key, view or grant names another schema or `public` | The pipeline check fails the build; the object is removed |
| Check finding, no message id | The ledger carries an UPDATE or a DELETE grant, or the trigger is absent | The pipeline check fails the build |
| `decision_log_entry is append only: UPDATE refused` | An UPDATE is attempted by the schema owner | Raised by `refuse_change`; the attempt is written to the ACE audit and SOC log by the caller |
| `decision_log_entry is append only: DELETE refused` | A DELETE is attempted by the schema owner | Raised by `refuse_change`; the same audit path |
| MSG-P7-009 | A record reaches the database with a required field empty | The decision record was refused: {field} is missing or not valid. Raised by the application, not by a database constraint |
| MSG-P7-003 | The ingest cannot insert the row | The action was not taken because the decision could not be recorded. Try again in a few minutes. Raised by the application |

The database enforces what does not change: keys, uniqueness, the chain position, the refusal of an update and a delete, and the schema boundary. The business checks — a known decision code, a rule ID with its version, a final call in force — stay in the application, so a business person can change them without a migration.

### 15. Screens and states

No screen. The result of a migration is visible in the release pipeline and in the service's Flyway history: pending, applied, failed, undone, each with a version and a checksum. The table exposes the standard record columns of section 9 and no state of its own; the audit screens read entries through the two operations of the service and never through SQL.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P7-E1008-DB-01 | AC1 | Component | Empty schema with V0001; this story's four migrations; a second run; the Flyway history compared |
| TC-P7-E1008-DB-02 | AC2 | Component | `decision_log_entry` catalogue: the twenty-two columns and the standard seven, the physical types, the four keys, the structural check, the absence of a foreign key |
| TC-P7-E1008-DB-03 | AC3 | Component | An UPDATE and a DELETE as the login and as the schema owner; the grant catalogue; the insert and read as the login; the refusal message |
| TC-P7-E1008-DB-04 | AC4 | Component | The chain columns, the unique keys, the five indexes; a first entry with 64 zeros and a second linked to it |
| TC-P7-E1008-DB-05 | AC5 | Component | The three library objects after the template is applied; their columns compared with the template; the absence of a key into the ledger |
| TC-P7-E1008-DB-06 | AC6 | Component | Catalogue queries over tables, keys, views, synonyms and grants; the search for `rwb_case`, `rwb_access`, the recovery schema, an ACE schema and `public`; the exclusion list |
| TC-P7-E1008-DB-07 | AC7 | Component | Grant script and rollback on a copy of the SIT schema; grants listed per login; the ledger identifiers after the rollback |

### 17. Guardrails

- No business value in a constraint: the decision codes, approval levels and limits are other owners' rows, read over their contracts (DP-07, BR8).
- No personal data in a migration, a script, a test fixture or a run book: an entry names a case, a user reference and a rule.
- No UPDATE and no DELETE grant on the ledger, and no delete method in any story's repository; the trigger stays installed (BR2).
- No read of another schema, no key into another schema and no grant that names one: `rwb_decision` objects reference `rwb_decision` objects only (DP-01, BR6).
- One login per service: the `rwb-decision` login is the only grantee, and its name is Not specified in the source documents (GAP-1232; ASM-2196).
- The sequence is per service and linear: no monolith migration name is reused and no object is created twice (DP-15).
- The library objects are applied from the published template and never edited here.
- No lake object, watermark or partition is created: the copy is retired (DP-17, BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-DRI-001 | One record per decision with the seven field groups | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-01 | BR1 | TC-P7-E1008-DB-02 |
| REQ-DRI-002 | Append only; a correction is a new record naming the one it corrects | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-01 | BR2, BR4 | TC-P7-E1008-DB-03, TC-P7-E1008-DB-07 |
| REQ-DRI-003 | Hash chained, checked, break reported to Compliance the same day | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-01 | BR3 | TC-P7-E1008-DB-04 |
| Legacy TC-E1-008-01, TC-E1-008-02, TC-E1-008-03, TC-E1-008-04, TC-E1-008-05, TC-E1-008-06, TC-E1-008-07, TC-E1-008-08, TC-E1-008-09, TC-E1-008-10 | The ten legacy test cases of RWB-E1-008, at end-to-end and component level | Epic 1, 3.7 | FEAT-DRI-01 | BR1 to BR9 | Executed by RWB-P7-E1008-APP and RWB-ITG-E1008-ITG |

The ten legacy test cases are executed by RWB-P7-E1008-APP, which owns AC1 to AC8. This database story copies no legacy acceptance criterion and lists no legacy test case of its own; its tests are the schema checks of section 16.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P7-E1008-APP | App development | X dependency tracked: the story that ingests the shared topic, writes and reads these rows and runs the chain check |
| RWB-P7-E1008-CON | Contract | Sibling: the shapes its section 12 publishes must match the columns created here |
| RWB-P7-E1008-OPS | DevOps | Sibling: the pipeline that applies these migrations at start and the restore run book of this ledger |
| RWB-P7-E1027-APP | App development | The writer story that writes this service's own records into this table |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence and its version allocation |
| RWB-PLT-TE006-CON | Contract | The event platform template of the three library objects |
| RWB-PLT-NF06-DB | ACE DB | The schema and baseline of `rwb_decision`, the login and the connection pool per login |

### 19. Out of scope

- The application code, the ingest, the chain and the two operations: RWB-P7-E1008-APP.
- The contract of the two operations: RWB-P7-E1008-CON.
- The pipeline, the Flyway run at start, the alerts and the restore run book: RWB-P7-E1008-OPS.
- `approval` and the delegation of authority: RWB-P7-E2013-APP and RWB-P7-E2013-CON.
- The rule registry tables `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case`: the rule stories of this service, including RWB-P7-E1073-APP.
- `delegation_limit`: P4 rwb-access, read over its contract.
- `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` and `lov_value`: rwb-case (P3), read over the reference-data contract.
- The ACE views, their grants and the boundary rule: P1 rwb-source-data.
- The interaction ledger and its own append-only trigger: P1 rwb-source-data (DP-18).
- The event schema itself: RWB-PLT-TE006-CON; this story applies the template.
- Retention periods and their scheduling (DL26).
