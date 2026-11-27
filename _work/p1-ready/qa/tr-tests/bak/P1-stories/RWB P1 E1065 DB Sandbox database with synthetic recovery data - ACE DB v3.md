# RWB-P1-E1065-DB Sandbox database with synthetic recovery data - ACE DB

**Version 3 changes**

- One shared rwb_sandbox that P1 creates only if absent and never drops, renames or recreates; the build database, the rename step and the wording "one database per service release" are removed (RD-P1-046; findings 3 and 11).
- The extension tables, the view grants and their migrations stay with RWB-P1-E1069-DB; this story keeps the shared database, the test double, the DEV read role rwb_sandbox_read, the target gate, the two data checks, the apply order and the build lock (findings 6, 8 and 9).
- Absent-table check limited to recovery and rwb_source_data, pattern scan limited to base tables of rwb_source_data, seeding between apply and verify, and AC9 to AC12 added (findings 1, 2, 4, 5, 7, 12 to 20).
- Names and versions aligned to Physical Schema v9, LDM v11, Security and Access Design v6, Environment and Deployment Design v7 and Test Cases v9 (findings 14, 15 and 21).
- Batch D: failed builds keep the previous sandbox and tests never reset ledger rows (RD-P1-073); test case IDs TC-P1-E1065-DB-10 to -13 cited.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1065-DB |
| Version | 3 |
| Work type | DB (ACE DB) |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-065 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP13, DP15, DP19 |
| Open decisions | DL43 remains with the ACE team lead; recommended answer A (scope and dates as in RWB-ACE-001) is the planning basis (RD-P1-043) |
| Parallel lane | L-P1-O |
| Ready to start | After RWB-PLT-NF06-DB, RWB-PLT-E1044-CON, RWB-P1-E1001-APP and the RWB-P1-E1069-APP view migrations |
| Size | Not specified in the source documents (DOR-RWB-P1-E1065-DB-16); small, fits within a two-week sprint (DOR-RWB-P1-E1065-DB-15); the squad sizes it at refinement |
| Depends on (build) | RWB-PLT-NF06-DB, RWB-PLT-N011-DB, RWB-PLT-E1044-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP, RWB-P1-E1065-CON |
| Contract dependencies | RWB-P1-E1065-CON stage and fixture contract; fixture package version Pending under NEW-ASM-A1 |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1069-DB (extension tables and view grants); RWB-P1-E1065-APP (generator and verifier); RWB-P1-ACE001-DB (Section B outside DEV and pipeline test) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-006, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-029, FR-P1-030) |
| Readiness decisions | RD-P1-011, RD-P1-021, RD-P1-024, RD-P1-043, RD-P1-045, RD-P1-046, RD-P1-048, RD-P1-073 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for the ACE database work of rwb-source-data. The single `recovery` schema of the monolith becomes three schemas of one DEV database on the one ACE PostgreSQL server — `public` as the ACE test double, `recovery` for the 30 read-only `v_ace_*` views and `rwb_source_data` for this service's own tables and the four extension tables — with one read-only role `rwb_sandbox_read` and a deployment gate that refuses any target other than DEV (DP-01, DP-02; Architecture v5 slides 8, 9, 29 and 41). The legacy build's database create, DDL apply, verifier, rename and advisory lock move here as database objects and checks. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1065-DB). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 27 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: shared sandbox database, P1-owned schema boundary, DEV read role, data checks and delivery ordering. Agent: S7-stories.

### 1. Story

As a **recovery developer (RW-TRIBE) acting as the ACE database engineer**, I want **the P1 part of the shared sandbox database `rwb_sandbox`: the database created if it is absent, schema `public` as the ACE-shaped test double with synthetic rows only, schemas `recovery` and `rwb_source_data` filled by the P1 migrations, the DEV-only read role `rwb_sandbox_read`, a target gate, a data-pattern check and an absent-table check, and one build lock**, so that **P1 reads can be built and tested before ACE interfaces are available, a breach is refused by the database and the pipeline, and no other service's schema is touched**.

This is the database slice of legacy RWB-E1-065. It delivers:

- the shared database `rwb_sandbox`, created only if absent and never dropped, renamed or recreated (RD-P1-046), and the schemas `public`, `recovery` and `rwb_source_data` in it;
- the apply order: ACE schema file and `tier2-ddl.sql` into `public`, the P1 baseline, the Section A views, the Section B views over the fixture, and the extension tables and view grants of RWB-P1-E1069-DB;
- the DEV-only read role `rwb_sandbox_read` with SELECT on `recovery` and `rwb_source_data`, no write and no grant on `public`;
- the target gate for DEV and pipeline test, and the synthetic-rows-only rule for the test double;
- the data-pattern check over the base tables of `rwb_source_data` and the absent-table check over `recovery` and `rwb_source_data`;
- the delivered-objects check and one PostgreSQL advisory lock in `rwb_sandbox` for the P1 build.

It builds no generator and no export tool (RWB-P1-E1065-APP, which seeds between apply and verify). It creates no view (RWB-P1-E1069-APP), no extension table and no view grant to a service login (RWB-P1-E1069-DB) and no service table (RWB-P1-E1001-APP). It seeds no other service's schema and publishes no operation.

### 2. Business rationale

The DEV and pipeline-test database is shared: it holds `public`, `recovery` and one `rwb_<short>` schema per service. This story creates `rwb_sandbox` only if absent, builds only `public`, `recovery` and `rwb_source_data`, and never drops, renames or recreates the database. Other `rwb_*` schemas may exist and are not P1's (RD-P1-046; Environment and Deployment Design v7).

In every environment the ACE views are read by the service login `rwb_source_data` only. The sandbox read role is the one DEV exception, documented in Security and Access Design v6 and excluded from the production single-reader assertion. Case records and case status belong to rwb-case (RD-P1-021, RD-P1-024).

### 3. Preconditions

- RWB-PLT-NF06-DB has created the service logins; this story creates no service login.
- `rwb_sandbox` is present or is created by the first P1 build. The ACE team owns the database (ASM-0695); the ASM-0695 build database `rwb_sandbox_next` is not used (RD-P1-046).
- RWB-P1-E1001-APP provides the P1 baseline. Which legacy V0001 file is applied remains Pending under GAP-0566 and the Tier 1 table count under GAP-3168; the Tier 2 set is 14 tables and 12 columns from `tier2-ddl.sql` of RWB-P1-E1065-CON.
- RWB-P1-E1069-APP provides the helper functions and views; RWB-P1-E1069-DB provides the four extension tables and the view grants to `ace_view_owner` and `rwb_source_data`.
- The principal that runs the statements on `public` and `recovery` and creates the database is Pending, owner ACE DBA with platform DB owner, tracked as NEW-GAP-S7-05 (GAP-0568).
- Section B is built against the fixture in DEV and pipeline test. In SIT, UAT and PROD it waits for RWB-ACE-001 with feature flags off (RD-P1-043).
- Pending: the pipeline parameter and the allow-listed host source of the target gate, owner platform DB owner, tracked as NEW-GAP-S7-04.
- Pending: the attributes of `rwb_sandbox_read` (LOGIN or group role), how a member of the DEV group RWB-DEV-RW-TRIBE obtains it and where its credential is held, owner platform DB owner, tracked as NEW-GAP-S7-07.

### 4. Flow

1. The target gate checks the pipeline target and host against the DEV and pipeline-test allow-list before any database operation.
2. The build creates `rwb_sandbox` only if absent, takes the P1 advisory lock in it, and creates `public`, `recovery` and `rwb_source_data` only if absent. No other schema is touched.
3. Apply in order: the ACE schema file and `tier2-ddl.sql` to `public`; the P1 baseline; the Section A views; the Section B views over the fixture; then the extension tables and view grants of RWB-P1-E1069-DB (RD-P1-046; Environment and Deployment Design v7). Applied Flyway versions are skipped.
4. The generator of RWB-P1-E1065-APP seeds `public` and `rwb_source_data`. When this story is tested alone, it seeds from `case-seed-list.csv` and `seed-profile.json`.
5. In DEV only, create `rwb_sandbox_read` if absent and re-apply its grants; the step runs after every apply, so objects added by a later migration stay readable.
6. Run the data-pattern check, the absent-table check and the delivered-objects check.
7. Release the lock and record the build state (Verified or Failed), commit and check results in the pipeline run.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The target or host is not on the allow-list | Stop before any database operation; report target and host | Pipeline result | AC2 |
| X2 | A session as `rwb_sandbox_read` writes, or selects from `public` | The statement is refused | SQLSTATE 42501 | AC3 |
| X3 | A clear identity value matches a pattern in a base table of `rwb_source_data` | The check fails naming schema.table.column; the value is not logged | Pipeline result | AC4 |
| X4 | One of the absent tables exists as a table in `recovery` or `rwb_source_data` | The check fails naming schema.table | Pipeline result | AC4 |
| X5 | A delivered view or extension table is missing, or a view does not compile | The build fails naming the object; nothing is created to replace it | Pipeline result | AC5 |
| X6 | A second P1 build starts while one runs | It waits on the advisory lock | None | AC6 |
| X7 | `tier2-ddl.sql` is absent in DEV or pipeline test | The build fails; no partial Section B is accepted | Pipeline result | AC7 |
| X8 | A DDL file fails | The build stops naming the file, is recorded Failed and does not seed; other schemas are unchanged | Pipeline result | AC8 |
| X9 | A wrong grant or object needs correction | A new forward version or a re-run of the grant step; no undo script (RD-P1-045) | Pipeline result | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the platform logins, the P1 baseline and the P1 view and extension-table migrations |
| Negotiable | Exact sequence numbers and privileged grant identity remain with the sequence owner and ACE DBA |
| Valuable | One owner controls P1's schema boundary on a shared synthetic database |
| Estimable | The executing principal, gate allow-list and role mapping remain Pending |
| Small | Size is Not specified and remains for squad refinement |
| Testable | Catalog privileges, check results, build state and lock behaviour are asserted per criterion |

### 7. Acceptance criteria

~~~gherkin
Feature: Shared sandbox database and P1 database boundary

Scenario: AC1 P1 uses the shared database without replacing it
  Given rwb_sandbox may already contain schemas owned by other services
  When the P1 database build runs in DEV or pipeline test
  Then rwb_sandbox is created only if absent
  And it is never dropped, renamed or recreated and no database rwb_sandbox_next is created
  And this slice creates or changes only public, recovery and rwb_source_data
  And every other rwb_* schema remains unchanged
  And public has the ACE schema fixture and the 14 Tier 2 tables with 12 added columns
  And the Tier 1 table count remains Pending under GAP-3168 and legacy V0001 selection under GAP-0566
  # TC-P1-E1065-DB-01

Scenario: AC2 The target gate refuses any other environment
  Given a pipeline target or host outside the DEV and pipeline-test allow-list
  When the stage starts
  Then it exits non-zero before any database operation, including CREATE DATABASE
  And it reports the target and host
  And the allow-list parameter and host source remain Pending under NEW-GAP-S7-04
  # TC-P1-E1065-DB-02

Scenario: AC3 The DEV read role reads two schemas and writes nothing
  Given the grant step has run in DEV
  When the catalogue is queried for rwb_sandbox_read
  Then it holds USAGE and SELECT on recovery and rwb_source_data and no privilege on any table of public
  And it holds no INSERT, UPDATE, DELETE or TRUNCATE on any object
  When a session with that role selects from public.customer or inserts into rwb_source_data.interaction
  Then each statement fails with SQLSTATE 42501
  And no grant of this role exists in SIT, UAT or PROD
  # TC-P1-E1065-DB-03

Scenario: AC4 The data-pattern and absent-table checks refuse a breach
  Given a seeded rwb_sandbox
  When a value matching a 13-digit national ID with a valid check digit is injected into a text or jsonb column of a base table of rwb_source_data
  Then the check fails naming schema.table.column, the value is not logged and the build is recorded Failed
  And a clear identity value in public is not a failure, and recovery views are not scanned
  When a table named loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory or tracker_row is added to recovery or rwb_source_data
  Then the check fails naming schema.table, while ACE tables of the same names in public are not a failure
  And mobile and email patterns and their synthetic formats remain Pending under ASM-5269
  # TC-P1-E1065-DB-04

Scenario: AC5 Delivered objects are asserted and never re-created
  Given the 30 views, the four extension tables and the dictionary rows delivered by their own stories
  When one view or party_ext is dropped and the verifier runs
  Then the build fails naming the missing object and creates no object to replace it
  And no other schema of rwb_sandbox changes
  # TC-P1-E1065-DB-05

Scenario: AC6 Two P1 builds do not overlap
  Given a P1 build holds the P1 advisory lock in rwb_sandbox
  When a second P1 build starts
  Then it writes nothing until the first releases the lock, and then runs
  # TC-P1-E1065-DB-06

Scenario: AC7 Section B in the sandbox follows the fixture
  Given a DEV or pipeline-test build
  When tier2-ddl.sql is present
  Then the 14 Section B views exist and compile after Section A
  When tier2-ddl.sql is absent
  Then the build fails and is not recorded Verified
  And no Section B object is applied in SIT, UAT or PROD by this stage
  # TC-P1-E1065-DB-08

Scenario: AC8 The apply order is fixed and a failure stops the build
  Given a DDL fixture with a syntax error in the Section A step
  When the build runs
  Then the steps run in the order ACE schema, tier2-ddl.sql, baseline, Section A, Section B, extension tables and grants
  And it stops naming the failing file, is recorded Failed and seeds nothing
  And every other rwb_* schema is unchanged
  And a correction is a new forward version and no undo file exists
  # TC-P1-E1065-DB-09

Scenario: AC9 The reader keeps access after a later migration
  Given the grant step has run in DEV
  When a later migration adds a table to rwb_source_data and the build runs
  Then rwb_sandbox_read can select the new table and cannot insert into it
  # TC-P1-E1065-DB-10

Scenario: AC10 The other grants are the ones RWB-P1-E1069-DB delivers
  Given the built sandbox
  When the catalogue is queried for the view grants
  Then ace_view_owner owns the views, rwb_source_data holds SELECT on them and no table privilege in public
  And no other service login holds a privilege on a view
  # TC-P1-E1065-DB-11

Scenario: AC11 The first build and a build beside other services
  Given no database rwb_sandbox, or one holding a schema rwb_case with rows
  When the P1 build ends Verified
  Then rwb_sandbox exists with public, recovery and rwb_source_data
  And an existing rwb_case schema and its row counts are unchanged
  # TC-P1-E1065-DB-12

Scenario: AC12 No credential is stored
  Given the repository and the pipeline log of a build
  When the secret scan runs
  Then it finds no password of rwb_sandbox_read or of any login
  # TC-P1-E1065-DB-13
~~~

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | rwb_sandbox is shared; P1 creates it only if absent and never drops, renames or recreates it | RD-P1-046 |
| BR2 | This slice changes only public, recovery and rwb_source_data; other rwb_* schemas may exist | RD-P1-046 |
| BR3 | rwb_source_data is the only service login that reads ACE views; rwb_sandbox_read is a DEV-only exception | D-RCV-60; Security and Access Design v6 |
| BR4 | rwb_sandbox_read holds SELECT on recovery and rwb_source_data, no write and no grant on public | GAP-0503; Security and Access Design v6 |
| BR5 | public holds synthetic rows only, is never deployed to SIT, UAT or PROD by this stage, and no service table is loaded from it by a batch job | D-RCV-35 U1; NFR-045 |
| BR6 | A clear identity number is allowed only in public; base tables of rwb_source_data hold masked or synthetic values | D-RCV-35 U4; CTL-11 |
| BR7 | Section B is built over the fixture in DEV and pipeline test and gated by RWB-ACE-001 elsewhere | RD-P1-043 |
| BR8 | Migrations are forward-only; applied files are never edited and there is no undo script | RD-P1-045 |

### 9. State transitions

No business record changes state. The P1 build is recorded in the pipeline run:

| State | Next | When |
|---|---|---|
| Waiting | Building | The P1 advisory lock is taken |
| Building | Verified | Apply, seed and every check pass |
| Building | Failed | Any apply step, seed step or check fails |
| Failed or Verified | Waiting | A new build starts |

A migration is Pending, Applied or Failed (RD-P1-045).

### 10. Authority

| Role | Authority |
|---|---|
| ACE team | Owns the database rwb_sandbox and schema public (ASM-0695) |
| Platform DB owner | Owns login credentials, the target gate and the sandbox read role mapping (NEW-GAP-S7-04, NEW-GAP-S7-07) |
| ACE DBA | Runs operations needing rights on public or recovery; principal Pending under NEW-GAP-S7-05 |
| Recovery developer (RW-TRIBE) | Starts a build manually and reads the sandbox through rwb_sandbox_read |
| Platform administrator (RW-PLATADM) | Starts a build manually and reads the build result |
| ACE team lead | Owns DL43; recommended answer A is the planning basis only |
| Product owner | Owns epic design sign-off; sign-off remains Pending |

### 11. Data

| Object | Fields or privilege | This story |
|---|---|---|
| public ACE test double | ACE schema file; 14 Tier 2 tables and 12 columns of `tier2-ddl.sql` | Applies; the generator seeds synthetic rows; Tier 1 count Pending under GAP-3168 |
| recovery | 16 Section A and 14 Section B views, three helper functions | Asserts; created by RWB-P1-E1069-APP |
| rwb_source_data | P1 tables of the baseline, library tables and the four extension tables (DF-EXT-001 to DF-EXT-049) | Asserts; created by RWB-P1-E1001-APP, later P1 migrations and RWB-P1-E1069-DB |
| rwb_sandbox_read | SELECT on recovery and rwb_source_data | Creates in DEV and grants |
| case records | Owned by rwb-case; `case_list_row` is retired | Not created |

### 12. Contract

#### 12.1 REST operations provided

None. This is a database story and publishes no operation.

#### 12.2 REST operations consumed

None. The build step reads files and the catalogue, not a REST contract; the one reference-data read of the build belongs to RWB-P1-E1065-APP.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and this story publishes nothing on it.

#### 12.4 Events consumed

None.

#### 12.5 Workflows and activities

None.

#### 12.6 Schedules

None. The build runs in the release pipeline and on a manual start, not on a Temporal Schedule, and the pipeline stage contract itself is RWB-P1-E1065-CON's.

#### 12.7 Tables owned

This story creates no table. It names these shared objects:

| Object | Owner | This story |
|---|---|---|
| database rwb_sandbox | ACE team (ASM-0695) | Creates only if absent; never drops, renames or recreates |
| schema public | ACE team | Applies the test double; synthetic rows only |
| schema recovery | rwb-source-data sequence; views owned by ace_view_owner | Creates the schema if absent |
| schema rwb_source_data | P1 | Creates the schema if absent |
| role rwb_sandbox_read | Platform DB owner | Creates in DEV and grants |
| other rwb_* schemas | Each owning service | Never touched |

#### 12.8 Contract fakes

| Fixture | Serves | Used by |
|---|---|---|
| ACE schema file | public ACE source tables | Apply step |
| `tier2-ddl.sql` (RWB-P1-E1065-CON) | 14 Tier 2 tables and 12 added columns | Section B in DEV and pipeline test |
| `case-seed-list.csv` and `seed-profile.json` (RWB-P1-E1065-CON) | Seed rows when this story is tested alone | AC4, AC5 |
| Delivered-objects fixture | Physical Schema v9 `rwb_source_data.sql` and `recovery_views.sql` | AC5 |
| Test roles | Created and dropped by the test | AC3, AC10 |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic in this story |
| Temporal | None | None | No workflow, activity or Schedule |
| File | Build result in the pipeline run | DDL files and fixtures | Versioned fixtures of RWB-P1-E1065-CON |
| SQL view | None | 30 `recovery.v_ace_*` views | Asserted; DEV SELECT through rwb_sandbox_read |

### 13. Solution plan

**Apply order.** ACE schema file and `tier2-ddl.sql` to `public`; P1 baseline (RWB-P1-E1001-APP); Section A views; Section B views over the fixture; extension tables and view grants (RWB-P1-E1069-DB). Flyway applies only pending versions of the rwb-source-data sequence and no legacy V0001 to V0003 number is reused. This story adds no service migration.

**Lock.** One PostgreSQL advisory lock for the P1 build, taken in `rwb_sandbox` because the database is never replaced; the key is a constant of the P1 build stage. No other service's lock is taken.

**Grant step (DEV only, re-run after every apply).**

```sql
GRANT USAGE ON SCHEMA recovery, rwb_source_data TO rwb_sandbox_read;
GRANT SELECT ON ALL TABLES IN SCHEMA recovery TO rwb_sandbox_read;
GRANT SELECT ON ALL TABLES IN SCHEMA rwb_source_data TO rwb_sandbox_read;
```

No other grant is made to `rwb_sandbox_read`: no write, no sequence use and nothing on `public`. The `ALL TABLES` form is used only for this DEV reader; service migrations grant one view at a time (RWB-P1-E1069-DB).

**Checks.**

| Check | Rule | Failure text |
|---|---|---|
| `SandboxTargetGate` | Target and host are on the DEV and pipeline-test allow-list | Target {target} on {host} is not allowed |
| `PersonalPatternCheck` | No match in text or jsonb columns of base tables of rwb_source_data | {schema}.{table}.{column} holds a value matching {pattern name} |
| `AbsentTableCheck` | None of the 20 names is a table in recovery or rwb_source_data | {schema}.{table} must not exist |
| `DeliveredObjectCheck` | 30 views compile, the four extension tables exist and every view and extension column has a sys_fields row | {object} is missing or does not compile |

**Recovery.** A failed build changes no other schema. Applied migrations are corrected by a new forward version; the data load of RWB-P1-E1065-APP is one transaction, so a failed load leaves the previous rows. A failed sandbox build leaves the previous sandbox in place and fails the pipeline, and each schema is seeded by its owner's E1065 story (RD-P1-073). No test or harness step deletes or resets ledger rows; tests isolate by their own cases and a fresh UUID per run in business keys, and the only reset is the sandbox rebuild between suites (RD-P1-073).

### 14. Validation and messages

Results are pipeline and database results with no `MSG-` ID. Privilege assertions use SQLSTATE 42501 and catalog predicates, not server message text. Check failures use the texts of section 13 and never print a matched value.

### 15. Screens and states

No screen. The build result is visible in the pipeline run. This story feeds no SCR-44 panel; any screen state belongs to the story that builds that screen.

### 16. Test cases

| Acceptance criteria | Test case (Test Cases v9) |
|---|---|
| AC1 to AC6 | TC-P1-E1065-DB-01 to -06 |
| AC7 | TC-P1-E1065-DB-08 |
| AC8 | TC-P1-E1065-DB-09 |
| AC9 to AC12 | TC-P1-E1065-DB-10 to -13 |

The data of TC-P1-E1065-DB-03 to -09 follows the revised criteria in the test case update. TC-P1-E1065-DB-07 and the legacy rows that use recovery_svc, V0001 and V0002 files or case tables are not evidence for these criteria.

### 17. Guardrails

- Never drop, rename or recreate the shared database, and never touch a schema outside public, recovery and rwb_source_data.
- Synthetic rows only; never copy production or SIT data into the sandbox.
- Run only against the allow-listed DEV and pipeline-test targets.
- rwb_sandbox_read is DEV only, read only, and has no grant on public.
- Never print a matched personal value or a credential; keep no credential in files.

### 18. Traceability

| Reference | Use |
|---|---|
| RD-P1-021; RD-P1-024 | P1 table ownership; case records stay with rwb-case |
| RD-P1-043 | Section B fixture and deployment gate |
| RD-P1-045 | Forward-only migrations |
| RD-P1-046 | Shared sandbox, no database replacement, seed fixtures |
| Physical Schema v9; LDM v11; RTM v9 | Current schema, fields and traceability |
| Security and Access Design v6; Environment and Deployment Design v7 | DEV read role and apply order |
| GAP-0501, GAP-0502, GAP-2137, GAP-3086 | Closed by RD-P1-046 |
| GAP-0503; ASM-0695 | Read role name and database owner |
| GAP-0566; GAP-3168; GAP-0568; ASM-5269 | Baseline file, Tier 1 count, executing principal, patterns |
| NEW-GAP-S7-04; NEW-GAP-S7-05; NEW-GAP-S7-07 | Target allow-list, executing principal, role mapping |

### 19. Out of scope

- The generator, seed values, verifier code, export tool and pipeline stage: RWB-P1-E1065-APP; the stage and fixture contract: RWB-P1-E1065-CON.
- The four extension tables, ace_view_owner and the view grants: RWB-P1-E1069-DB; the views and helper functions: RWB-P1-E1069-APP.
- The P1 baseline tables and dictionary rows: RWB-P1-E1001-APP; the schemas and service logins: RWB-PLT-NF06-DB.
- Seeding other services' schemas: their own E1065 slices; case records and case status: rwb-case.
- The ACE ingestion and the Tier 2 tables in ACE environments: RWB-P1-ACE001-DB.

### 20. Remaining delivery steps

- Size: Not specified; owner squad lead at refinement.
- Epic design sign-off: Pending; owner product owner and design authority.
- CON Done: Pending acceptance of RWB-P1-E1065-CON; owner service contract owner.
- Fake published: Pending versioned fixture publication under fakes/rwb-source-data/<contract version>/; owner service contract owner and QA lead.
- Test data in DEV: Pending the first sandbox build and the executing principal (NEW-GAP-S7-05); owner platform DB owner and ACE DBA.
- Gate allow-list and read role mapping (NEW-GAP-S7-04, NEW-GAP-S7-07): owner platform DB owner.
