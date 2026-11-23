# RWB-P1-E1065-DB Sandbox database with synthetic recovery data - ACE DB

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1065-DB |
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
| Parallel lane | L-P1-O |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-006, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-029, FR-P1-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for the ACE database work of rwb-source-data. The single `recovery` schema of the monolith becomes three schemas of one DEV database on the one ACE PostgreSQL server — `public` as the ACE test double, `recovery` for the 30 read-only `v_ace_*` views and `rwb_source_data` for this service's own tables and the four extension tables — with one read-only role `rwb_sandbox_read` and a deployment gate that refuses any target other than DEV (DP-01, DP-02; Architecture v5 slides 8, 9, 29 and 41). The legacy build's database create, DDL apply, verifier, rename and advisory lock move here as database objects and checks. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **ACE database engineer**, I want **the sandbox database `rwb_sandbox` of rwb-source-data created from the same DDL as SIT with its three schemas and its read-only role, the ACE-shaped tables held in schema `public` as a test double with synthetic rows only, the grants that give `rwb_sandbox_read` SELECT on schema `recovery` and schema `rwb_source_data` and nothing else, a deployment gate that refuses any target other than DEV, a data-pattern check that refuses a clear identity number outside `public`, and a build that runs in `rwb_sandbox_next`, verifies, then renames under an advisory lock**, so that **the sandbox is one DEV database per service release, a breach is refused by the database and the pipeline instead of by a review, and a failed build never leaves a half-built sandbox behind**.

This is the database slice of legacy RWB-E1-065. It delivers:

- the database `rwb_sandbox` and the build database `rwb_sandbox_next`, with schema `public`, schema `recovery` and schema `rwb_source_data`;
- the read-only role `rwb_sandbox_read` and its grant set: SELECT on schema `recovery` and schema `rwb_source_data`, no INSERT, UPDATE or DELETE, no grant on schema `public`, PUBLIC empty;
- the DEV-only deployment gate and the synthetic-rows-only rule for the ACE-shaped test double;
- the data-pattern check over every column tagged `is_personal` outside schema `public`, and the check that the 20 absent tables exist in no schema of the database;
- the build sequence: create `rwb_sandbox_next`, apply the DDL set, seed, verify, rename, grant, under one PostgreSQL advisory lock;
- the assertion of the four extension tables, the 30 views and the 122 object and 1,366 field dictionary rows that three sibling stories deliver, and no re-creation of any of them.

It builds no generator, no verifier logic and no export tool: those are RWB-P1-E1065-APP. It creates no view, no extension table and no service table: RWB-P1-E1069-APP, RWB-P1-E1069-DB and RWB-P1-E1001-APP deliver them. It writes no application code and no REST operation.

### 2. Business rationale

The legacy story asked one pipeline to stand up one schema of one database and prove it with a verifier and a rename. In the target the sandbox is one service's, on the one ACE PostgreSQL server, beside 19 service schemas, and the ownership rule is enforced by grants and not by separate servers (Architecture v5 slide 29). That changes the work from "build a schema" to "build a database whose three schemas each have one owner and one audience": schema `public` belongs to ACE and is only ever a test double, schema `recovery` holds the 30 views that only rwb-source-data may read, and schema `rwb_source_data` holds this service's own tables and the four extension tables.

The grant and gate half is what makes the sandbox safe to exist at all. A database that could be deployed to SIT would put synthetic ACE-shaped rows next to real ones, so the gate refuses any target but DEV. A role that could write would let a test corrupt the fixture it is testing, so the role is read only. A clear identity number anywhere but the test double would breach BR9 before anyone noticed, so the pattern check fails the build. And a build without the rename step could publish a half-built sandbox, so the verifier and the rename are one step under an advisory lock. Serves REQ-RDF-001 (the 14 data products with one system of record and one owner) and REQ-RDF-010 (no personal data outside its permitted use). The measure is the legacy one: 100 percent of pipeline runs in which the built sandbox passes every check (FSD P1 A2.1.1).

### 3. Preconditions

- The one ACE PostgreSQL server is reachable from the pipeline, and the migration account holds the ACE DBA role for the release window, so it can create a database, create a role, and grant on schema `public` (RWB-E1-044 in the legacy set; legacy RWB-E1-065 §3).
- The per-service Flyway sequence of rwb-source-data exists with its own history table in schema `rwb_source_data`, and the baseline version has been applied on it (DP-15; RWB-PLT-E1044-CON).
- The ACE schema DDL `15 ACE DB Alignment/ACE Schema PostgreSQL v1.sql` is in the repository, and the RWB-ACE-001 DDL for the 14 Tier 2 tables is available as a fixture (DL43).
- Schema `recovery` and the 30 `recovery.v_ace_*` views with their three helper functions are created by RWB-P1-E1069-APP on the same sequence; this story's checks run after them.
- The four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` are created by RWB-P1-E1069-DB, and the 122 `sys_objects` rows and 1,366 `sys_fields` rows with them.
- The read-only role name and the database scope of the sandbox are not fixed by any source document for the 19-service target: they are read as one DEV database per service release, `rwb_sandbox` for rwb-source-data with the build database `rwb_sandbox_next`, and the role `rwb_sandbox_read`. That reading is Not specified in the source documents (GAP-0503; ASM-0695).
- The credential of the role and its rotation are held by the platform DB owner, and no credential appears in a migration, a script or a runbook.
- No approval is required to run a Draft migration on a development database; the setup is released to the pipeline only after the tests of section 16 pass.

### 4. Flow

1. The ACE database engineer confirms the highest applied version on the service sequence (the baseline) and checks that the DEV target is named in the pipeline parameters.
2. The engineer writes the deployment gate: the stage refuses any environment other than DEV and any host other than the DEV instance, before a database is created.
3. The engineer writes the database build step: create `rwb_sandbox_next` with schema `public`, schema `recovery` and schema `rwb_source_data`, owned as the ownership rule says.
4. The engineer writes the DDL apply step: the ACE schema file and the Tier 2 fixture into schema `public`, then the per-service baseline and the two view migrations into their schemas in the fixed order (DP-15).
5. The engineer writes the role step: create `rwb_sandbox_read`, grant USAGE and SELECT on schema `recovery` and schema `rwb_source_data`, grant nothing on schema `public`, revoke PUBLIC, and grant no INSERT, UPDATE or DELETE.
6. The engineer writes the two checks: the data-pattern check over every column tagged `is_personal` outside schema `public`, and the absence check over the 20 tables that left the schema.
7. The engineer writes the delivered-objects check: the 30 views compile, the four extension tables hold their 49 columns and the dictionary holds 122 objects and 1,366 fields — asserted, never re-created.
8. The pipeline runs the verifier on `rwb_sandbox_next`, then renames the database to `rwb_sandbox` under one advisory lock and re-applies the grants.
9. A failed verifier leaves `rwb_sandbox` as it was and drops `rwb_sandbox_next`; the pipeline reports the failure with the object it named.
10. The engineer records the build step, the role and the gates in the release notes of the sequence.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | The stage is pointed at a target that is not DEV | The gate stops the stage before a database is created and names the target | Pipeline error, no message id |
| X2 | A clear identity number appears outside schema `public` in a column tagged `is_personal` | The data-pattern check fails and names the schema, the table and the column | Pipeline error, no message id |
| X3 | One of the 20 absent tables exists in any schema of the database | The absence check fails and names the table and the schema | Pipeline error, no message id |
| X4 | The verifier fails on a delivered object — a view that does not compile, a missing extension table, a dictionary count that is not 122 and 1,366 | The rename does not run, the previous sandbox stays in use and `rwb_sandbox_next` is dropped | Pipeline error, no message id |
| X5 | A second build starts while one runs | The second build waits on the advisory lock and runs after the first | None |
| X6 | The role `rwb_sandbox_read` already exists | The create is skipped, the grants are re-applied and nothing changes | None |
| X7 | A session as `rwb_sandbox_read` runs an INSERT, UPDATE or DELETE | The statement is refused | SQLSTATE 42501 permission denied for schema rwb_source_data (or for the object named) |
| X8 | A session as `rwb_sandbox_read` selects from a table in schema `public` | The statement is refused | SQLSTATE 42501 permission denied for schema public |
| X9 | The rename runs while a session still holds a connection to `rwb_sandbox` | The rename waits for the connection cap and then fails cleanly; the previous sandbox stays | Pipeline error, no message id |

X1, X2, X3, X5, X7 and X8 are the legacy paths X1, X4, X6 and the access rule of RWB-E1-065 carried onto the three-schema database; X4, X6 and X9 are the paths the delivered objects, the reusable role and the rename add.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One build step, one role step and three checks, on the service's own sequence; nothing to build against and no application code |
| Negotiable | The order of the grants and the check harness are the engineer's choice; the three schemas, the role, the gate and the two checks are fixed by this story and the contract |
| Valuable | The sandbox exists once, in DEV only, and a breach is refused by the database and the pipeline |
| Estimable | One build step, one role step, one gate, three checks and the rename under the lock |
| Small | Days, not weeks, with the catalogue checks |
| Testable | Every criterion in section 7 is one catalogue query, one refused statement with its SQLSTATE, or one pipeline run |

### 7. Acceptance criteria

```gherkin
Feature: The sandbox database, its three schemas and its read-only role

  Background:
    Given the one ACE PostgreSQL server and the DEV instance of it
    Given the per-service Flyway baseline of rwb-source-data has been applied on its own sequence

  Scenario: AC1 rwb_sandbox is built from the same DDL as SIT into three schemas (new, D-RCV-60)
    Given the ACE schema DDL, the RWB-ACE-001 Tier 2 DDL fixture, the baseline and the two view migrations
    When the build step runs in DEV
    Then the database "rwb_sandbox_next" exists with schema "public", schema "recovery" and schema "rwb_source_data"
    Then schema "public" holds the Tier 1 tables and the 14 Tier 2 tables of the fixture
    Then schema "recovery" holds the 30 v_ace_* views and the three helper functions
    Then schema "rwb_source_data" holds this service's 13 tables and the four extension tables
    Then the login "rwb_source_data" of the service has USAGE on its own schema and SELECT on schema "recovery"
    Then no schema other than the three exists in the database

  Scenario: AC2 The ACE-shaped tables are a test double in schema public only (new, D-RCV-60)
    Given the Tier 1 tables and the 14 Tier 2 tables in schema "public"
    When the catalogue is queried for their rows and for the target of the build
    Then every row in schema "public" is synthetic and no production row is loaded
    Then no table of schema "public" exists in schema "recovery" or in schema "rwb_source_data"
    Then the deployment gate refuses a target other than DEV before a database is created
    Then the pipeline records the target environment in the build report
    Then no batch job of any service loads a service table from schema "public"

  Scenario: AC3 The read-only role holds SELECT and nothing else (new, D-RCV-60)
    Given the role "rwb_sandbox_read"
    When the catalogue is queried for its grants
    Then it holds USAGE and SELECT on schema "recovery" and on schema "rwb_source_data"
    Then it holds no INSERT, UPDATE, DELETE or TRUNCATE on any object of either schema
    Then it holds no privilege of any kind on schema "public"
    Then PUBLIC holds nothing on any object of the three schemas
    Then the role is mapped to the DEV group RWB-DEV-RW-TRIBE and to no other group

  Scenario: AC4 The data-pattern and absence checks refuse a breach (new, D-RCV-60)
    Given every column of the database tagged is_personal outside schema "public"
    When a generated value matches the 13-digit national ID pattern with a valid check digit
    Then the data-pattern check fails and names the schema, the table and the column
    Then a clear identity number in schema "public" is not a failure, because ACE holds it there
    When the catalogue is queried for the 20 tables that left the schema
    Then none of them exists in schema "public", schema "recovery" or schema "rwb_source_data"
    Then the build publishes no sandbox when either check fails

  Scenario: AC5 The delivered objects are present and asserted, never re-created (new, D-RCV-60)
    Given the four extension tables, the 30 views and the dictionary rows delivered by their own stories
    When the verifier runs on "rwb_sandbox_next"
    Then the 30 v_ace_* views compile and each returns at least one row
    Then party_ext, contact_point_ext, account_ext and valuation_ext hold their 49 columns and their primary keys
    Then the dictionary holds 122 objects and 1,366 fields, and 49 of those fields sit on the four extension tables
    Then the build creates no view, no extension table and no dictionary row of its own
    Then a missing delivered object fails the build and no object is created to replace it

  Scenario: AC6 The build is verified, renamed and locked, and a failure leaves the previous sandbox (new, D-RCV-60)
    Given a sandbox "rwb_sandbox" in use and a build of "rwb_sandbox_next"
    When the verifier passes
    Then the database is renamed to "rwb_sandbox" and the grants are re-applied in the same step
    Then the previous database is gone and no partial database remains
    When the verifier fails
    Then no rename happens, "rwb_sandbox" still answers, and "rwb_sandbox_next" is dropped
    When a second build starts while one runs
    Then the second waits on the PostgreSQL advisory lock and runs after the first
```

These six criteria are new and prove only the database artefacts in the story title: the database with its three schemas, the test double, the role and its grants, the two checks, the delivered objects and the build sequence. No legacy acceptance criterion text is repeated here. The legacy criteria these objects answer are AC1, AC2, AC3 and AC7 of RWB-E1-065 and they are owned by RWB-P1-E1065-APP; AC4, AC5, AC6, AC8 and AC9 are the verifier, the idempotency, the constraint, the boundary and the lock, and they are proven by RWB-P1-E1065-APP against these objects.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; the sandbox holds synthetic data only and the ACE-shaped tables are a test double | legacy BR1, BR7; NFR-045; CTL-11 |
| BR2 | The sandbox is built from the same DDL as SIT: the ACE schema, the RWB-ACE-001 Tier 2 DDL fixture, the per-service baseline and the two view migrations | legacy BR2; ADR-001; DP-15 |
| BR3 | Three schemas and no more: `public` as the ACE test double, `recovery` for the 30 read-only views, `rwb_source_data` for this service's tables and the four extension tables | DP-01, DP-02, DP-05; Architecture v5 slides 15 and 29 |
| BR4 | One read-only role, `rwb_sandbox_read`: SELECT on `recovery` and on `rwb_source_data`, nothing on `public`, no write on any object, PUBLIC empty | legacy BR9; DP-02 |
| BR5 | A clear identity number is allowed only in the ACE-shaped tables; every column tagged `is_personal` outside `public` is refused a matching value | legacy BR9; D-RCV-35 U4 |
| BR6 | None of the 20 tables that left the schema exists in any schema of the sandbox, and no service table is loaded from the test double | legacy BR8; D-RCV-35; ADR-010 |
| BR7 | A build publishes by rename only after the verifier passes, under one advisory lock; a failed build leaves the previous sandbox | legacy §5 X1, X3, X4, X6 |
| BR8 | The delivered objects — the 30 views, the four extension tables and the dictionary rows — are asserted, never re-created | ownership and delivery split of this run |
| BR9 | The sandbox is DEV only: the gate refuses any other target before a database is created, and no copy is promoted | NFR-045; D-RCV-35 U1 |

**Where each rule lives in the target.** BR1, BR6 and BR9 are this story's gates and checks: the target gate, the absence check and the synthetic-only rule. BR2 is the DDL set the build applies. BR3 and BR4 are the schemas and the role this story creates, and their names come from the platform naming rule and the ownership map. BR5 is the data-pattern check. BR7 is the rename and the lock. BR8 is the delivered-objects check, which names the three sibling stories and creates nothing of theirs. The seed values, the exception shapes and the volumes are the app story's profile and do not live here; this story only gives them a database to be written into.

### 9. State transitions

None in the runtime sense: a database has no case state machine and this story changes no business row. The states this story moves through are the build states of the sandbox and the grant states of the role.

| Item | States |
|---|---|
| the sandbox | Absent, Building in `rwb_sandbox_next`, Verified, Published as `rwb_sandbox`, Failed with the previous sandbox kept |
| the role | Absent, present and granted, present and refused with SQLSTATE 42501; never a member of another service's login role |
| a grant | Held on a schema or an object, refused with SQLSTATE 42501, or held by PUBLIC, which is a failure |
| a personal column outside `public` | Clean, or matching a pattern, which fails the build |
| one of the 20 absent tables | Absent, or present, which fails the build |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The ACE database engineer (any team, per U3) | Writes and runs the build step, the role step, the gate and the checks |
| ACE team lead and ACE DBA | Own schema `public`; approve the Tier 1 table list and the Tier 2 fixture; supply the ACE DBA role for the release window |
| Platform DB owner | Owns the credential of `rwb_sandbox_read` and the environment gate |
| Recovery tech lead and data architect | Approve a change to the three schemas, the role name or the delivered-objects list |
| Recovery migration account | Applies the baseline, the two view migrations and this story's build in DEV |
| RW-PLATADM, platform administrator | Reads the build result on SCR-44 Migration runs and on the pipeline run (Platform administration R); may not change a grant |
| RW-AUDIT, internal audit | Reads the role's grants and the build report (Platform administration R) |
| No approval level from the delegation of authority applies | A database change is not a credit decision |

The role is named `rwb_sandbox_read` and the database `rwb_sandbox`; the platform DB owner holds the credential and the rotation policy, and no personal name and no credential appears in a migration, a script or a runbook.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-EXT-001 to DF-EXT-012 | party_ext | person_key and the 11 other fields | Not created here; asserted |
| DF-EXT-013 to DF-EXT-026 | contact_point_ext | contact_key and the 13 other fields | Not created here; asserted |
| DF-EXT-027 to DF-EXT-035 | account_ext | account_key and the 8 other fields | Not created here; asserted |
| DF-EXT-036 to DF-EXT-049 | valuation_ext | valuation_key and the 13 other fields | Not created here; asserted |
| DF-ACE-001 to DF-ACE-304 | the 30 recovery.v_ace_* views | all 304 fields, 177 Section A and 127 Section B | Not created here; SELECT granted to `rwb_sandbox_read` |
| DF-REF-097, DF-REF-098, DF-REF-105 | sys_fields | field_name, data_type, is_personal | Read by the two checks |
| None | the 20 tables that left the schema | loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory, tracker_row | Asserted absent in every schema |
| None | schema `public` | the Tier 1 tables and the 14 Tier 2 tables of the fixture | Created as a test double by the build step; synthetic rows only |

Field IDs are those in the Logical Data Model and Data Dictionary. The 49 extension-table fields, the 304 view fields and the 1,366 dictionary fields are other stories' deliveries, which this story asserts and never writes. The only rows this story creates are the structural rows of the two checks and the build report; it writes no business row anywhere.

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

No table is created by this story. The objects of the sandbox and their owners:

| Object | Schema or scope | Owner (ownership map) | Created or altered here |
|---|---|---|---|
| the database `rwb_sandbox` and the build database `rwb_sandbox_next` | database | P1 (sandbox); the server is ACE's | Created, renamed and dropped by this story's build step |
| the ACE-shaped test double, the Tier 1 and 14 Tier 2 tables | `public` | ACE team | Created from the ACE schema file and the Tier 2 fixture as a test double; synthetic rows only, DEV only |
| the 30 `v_ace_*` views and the three helper functions | `recovery` | View owner `ace_view_owner`; contract owner P1 | Not created here: RWB-P1-E1069-APP creates them; this story grants on them and asserts them |
| `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | `rwb_source_data` | P1 | Not created here: RWB-P1-E1069-DB creates them; this story asserts them |
| this service's 13 tables, among them `case_list_row`, `interaction`, `sys_objects`, `sys_fields` and `data_product` | `rwb_source_data` | P1 | Not created here: the baseline creates them; this story applies the baseline and writes no row |
| the read-only role `rwb_sandbox_read` and its grants | database | P1 (sandbox), credential by the platform DB owner | Created and granted here |
| `lake_copy_watermark` | no target | P1, no target | Not created: the data lake is removed (DP-17) |

No table of another service is created, altered or read, and no foreign key crosses a schema (DP-01). `lake_copy_watermark` is in the ownership map but has no target, so it is absent from the sandbox and is not seeded.

#### 12.8 Contract fakes

| Fixture | Serves | Used by |
|---|---|---|
| ACE head fixture | `ACE Schema PostgreSQL v1.sql` | The Tier 1 tables of the test double |
| Tier 2 DDL fixture | The RWB-ACE-001 DDL (DL43) | The 14 Tier 2 tables while RWB-ACE-001 is not deployed in DEV |
| Delivered-views fixture | RWB-P1-E1069-APP | A container with schema `recovery`, the 30 views and the three helper functions, so the grants and the compile check run against the real views |
| Delivered-tables fixture | RWB-P1-E1001-APP and RWB-P1-E1069-DB | A container with the baseline, the 13 tables, the four extension tables and the dictionary rows |
| No-grant role | The test role `rwb_no_grant` with no grant anywhere | AC3 |

A database story uses no service contract fake; the five fixtures above stand in for the ACE head and the two neighbouring stories.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic in this story |
| Temporal | None | None | No workflow, activity or Schedule |
| File | None | The DDL files and the build report | The ACE schema file, the Tier 2 fixture and the migrations are read by the pipeline |
| SQL view | The 30 `recovery.v_ace_*` views, SELECT granted to `rwb_sandbox_read` | The ACE-shaped test double behind them | SELECT only, never a write, and no statement of this story reads another service's schema |

### 13. Solution plan

**Sequencing.** rwb-source-data's Flyway sequence is owned by the platform; the V0001 baseline creates the schema, the history table and the standard record columns (DP-15). This story adds no migration of its own: it adds the build step, the role step and the checks that run around the sequence.

| Position in the build | Step | Contents |
|---|---|---|
| 0 | deployment gate | Refuse any target other than DEV and any host other than the DEV instance; record the target in the build report |
| 1 | create | Database `rwb_sandbox_next` with schema `public`, schema `recovery` and schema `rwb_source_data` |
| 2 | DDL apply | The ACE schema file and the Tier 2 fixture into `public`; the baseline and the two view migrations into their schemas in the fixed order |
| 3 | seed | The generator of RWB-P1-E1065-APP, under the seed profile of RWB-P1-E1065-CON |
| 4 | role and grants | Create `rwb_sandbox_read`, grant USAGE and SELECT on `recovery` and `rwb_source_data`, grant nothing on `public`, revoke PUBLIC, grant no write |
| 5 | checks | The personal-data pattern check, the 20-table absence check and the delivered-objects check |
| 6 | verify and publish | The verifier of RWB-P1-E1065-APP, then the rename to `rwb_sandbox` and the re-application of the grants under one advisory lock |
| 7 | failure | No rename, the previous `rwb_sandbox` kept, `rwb_sandbox_next` dropped |

The exact version numbers of the migrations this story applies are assigned by the sequence owner at build time, and no monolith version number is reused. The platform dependency of the sequence is `RWB-PLT-E1044-CON`: it is not in this story's "Depends on (build)" list, which the Work Package fixes as None, so it is recorded here as a note and not as a metadata dependency.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01, DP-02, DP-05 and DP-15 are the subject of this story: three schemas with one owner each, one login per service, one read path and one sequence. DP-03, DP-04, DP-07, DP-13 and DP-19 are named for completeness of the pattern set: this story writes no decision record, evaluates no rule, calls no contract, serves no path and serves no screen, and their build dependencies stay with the application story.

**Grant block**

```sql
GRANT USAGE ON SCHEMA recovery TO rwb_sandbox_read;
GRANT USAGE ON SCHEMA rwb_source_data TO rwb_sandbox_read;
GRANT SELECT ON ALL TABLES IN SCHEMA recovery TO rwb_sandbox_read;
GRANT SELECT ON ALL TABLES IN SCHEMA rwb_source_data TO rwb_sandbox_read;
REVOKE ALL ON SCHEMA public FROM rwb_sandbox_read;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA rwb_source_data FROM PUBLIC;
```

The `ALL TABLES` form is used here on purpose and only for the two read-only schemas: the sandbox role is a reader of the whole sandbox and holds no write, and a table added later must be readable without a second grant. The write revocation is explicit, so a later grant of `ALL` on the same schema cannot silently add a write:

```sql
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA recovery FROM rwb_sandbox_read;
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA rwb_source_data FROM rwb_sandbox_read;
```

No grantee other than `rwb_sandbox_read` appears in this block, `rwb_source_data` keeps its own DML on its own schema through the baseline, and PUBLIC receives nothing in any of the three schemas. The schema-wide SELECT is not a migration on the service sequence and grants no write, so the rule that the service login is granted one view at a time, in RWB-P1-E1069-DB, is unaffected: the sandbox reader is a DEV reader of a whole schema, the service login is the production reader of 30 named views.

**Checks**

| Check | Rule | Failure |
|---|---|---|
| `SandboxTargetGate` | The target is DEV and the host is the DEV instance | The stage stops before a database is created |
| `PersonalPatternCheck` | No column tagged `is_personal` outside `public` holds a value matching the national ID, mobile or email pattern | The build fails and names the schema, the table and the column |
| `AbsentTableCheck` | None of the 20 tables that left the schema exists in any schema | The build fails and names the table and the schema |
| `DeliveredObjectsCheck` | The 30 views compile and return a row; the four extension tables hold 49 columns; the dictionary holds 122 objects and 1,366 fields | The build fails and names the missing object |
| `SandboxGrantCheck` | `rwb_sandbox_read` holds SELECT on the two schemas and no write; PUBLIC empty; `rwb_no_grant` refused | The build fails and names the privilege |
| `SandboxBuildLock` | One advisory lock for create, verify and rename | The second build waits, then runs |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `sandbox_build.sql` | Build script | Creates the database and the three schemas, applies the DDL and the migrations, renames and drops |
| `sandbox_role.sql` | Build script | Creates `rwb_sandbox_read`, issues the grants and the revokes, re-applied after the rename |
| `SandboxTargetGate` | Pipeline check | Refuses any target other than DEV before a database is created |
| `PersonalPatternCheck` | Pipeline check | The personal-data pattern rule over every column tagged `is_personal` outside `public` |
| `AbsentTableCheck` | Pipeline check | The 20 tables that left the schema are absent in every schema |
| `DeliveredObjectsCheck` | Pipeline check | The 30 views, the four extension tables and the dictionary counts, asserted and not created |
| `SandboxGrantCheck` | Pipeline check | The role's grants, the two refusals with SQLSTATE 42501 and PUBLIC empty |

**Build steps**

1. The `SandboxTargetGate` with a fixture pointed at a non-DEV target (AC2, AC6).
2. `sandbox_build.sql` with the create, the DDL apply, the verify, the rename and the drop-on-failure, and a failing fixture for each branch (AC1, AC6).
3. `sandbox_role.sql` with the grants, the revokes and the re-application after the rename, and a fixture that asserts no write and no privilege in `public` (AC3).
4. `PersonalPatternCheck` with an injected 13-digit value outside `public` and a clear value in `public.customer` (AC4).
5. `AbsentTableCheck` with a fixture that creates one of the 20 tables (AC4).
6. `DeliveredObjectsCheck` against the delivered-views and delivered-tables fixtures, with a missing object in each (AC5).
7. `SandboxGrantCheck` with sessions as `rwb_sandbox_read`, `rwb_source_data` and `rwb_no_grant` (AC3).
8. The repeated build on a second run for the same commit and seed, and the advisory-lock test with two builds (AC6).

**Done when.** The build applies twice without a change, the three schemas exist with their owners, `rwb_sandbox_read` holds SELECT on `recovery` and `rwb_source_data` and nothing else, the gate refuses a non-DEV target, the pattern and absence checks fail on their fixtures, a failed verifier leaves the previous sandbox and drops `rwb_sandbox_next`, and the tests in section 16 pass.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| SQLSTATE 42501 | A session as `rwb_sandbox_read` selects from schema `public` | permission denied for schema public |
| SQLSTATE 42501 | A session as `rwb_sandbox_read` runs INSERT, UPDATE or DELETE on a sandbox object | permission denied for schema rwb_source_data |
| Pipeline error, no message id | The target is not DEV | The gate names the target and the host refused |
| Pipeline error, no message id | A personal column outside `public` matches a pattern | The check names the schema, the table and the column |
| Pipeline error, no message id | One of the 20 absent tables exists | The check names the table and the schema |
| Pipeline error, no message id | A delivered object is missing | The check names the object and the story that delivers it |

These are pipeline and database texts for developers and are not part of the message standard. No `MSG-` ID of this story is new: the two texts of the access test are the legacy texts MSG-P4-002 and MSG-P4-003 raised by the guard library on the DEV service, and they are tested in RWB-P1-E1065-APP. A build failure returns no body from this story, because it has no service.

### 15. Screens and states

No screen. The result of a build is visible in the pipeline run and in the service's Flyway history (pending, applied, failed, undone, each with a version and a checksum). The platform administrator reads the build result under Platform administration R and on SCR-44 Interface and job monitor, and the data steward reads the dictionary counts of the sandbox. Nothing in this story is shown to a user directly: the sandbox is read with SQL and the export script of the app story, never through a screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1065-DB-01 | AC1 | Integration | A DEV instance, the ACE schema file, the Tier 2 fixture, the baseline and the two view migrations; the three schemas and their owners checked in the catalogue |
| TC-P1-E1065-DB-02 | AC2 | Component | A build pointed at a non-DEV target; the row provenance of schema `public`; the same table names looked for in the other two schemas |
| TC-P1-E1065-DB-03 | AC3 | Component | Sessions as `rwb_sandbox_read`, `rwb_source_data` and `rwb_no_grant`; the grant catalogue of the three schemas |
| TC-P1-E1065-DB-04 | AC4 | Component | An injected 13-digit value outside `public` and a clear value in `public.customer`; a fixture that creates one of the 20 tables |
| TC-P1-E1065-DB-05 | AC5 | Integration | The delivered-views and delivered-tables fixtures; a missing view, a missing extension table and a dictionary count of 121 |
| TC-P1-E1065-DB-06 | AC6 | Integration | A published sandbox and a second build; a failing verifier; two builds started together on the advisory lock |
| TC-E1-065-01 | Regression evidence for legacy AC1 on the objects this story builds | End to end | The Tier 1 and 14 Tier 2 tables; the baseline and the two view migrations; seed 20261128; 2,812 cases plus shapes |
| TC-E1-065-02 | Regression evidence for legacy AC2 and the access rule | End to end | Read-only role query, CSV export and refused UPDATE |
| TC-E1-065-03 | Regression evidence for legacy AC3 on the dictionary-driven fill | End to end | Test migration adding recovery_case.risk_tier with its dictionary row |
| TC-E1-065-04 | Regression evidence for legacy AC4 on the verifier | End to end | Dictionary fixture without the DF-CAS-023 row for recovery_case.closure_reason |
| TC-E1-065-05 | Regression evidence for legacy AC5 on the rename | End to end | Two builds for commit a1b2c3d and seed 20261128 |
| TC-E1-065-06 | Regression evidence for legacy AC6 on the constraint failure | End to end | Empty LOV-PRODUCT seed |
| TC-E1-065-07 | Regression evidence for legacy AC7 and the pattern check | End to end | Injected 13-digit value in recovery.document_field.extracted_value; a clear value in public.customer |
| TC-E1-065-08 | Regression evidence for legacy AC8 on the boundary accounts | End to end | Boundary accounts at 89 and 90 days past due in v_ace_account |
| TC-E1-065-09 | Regression evidence for legacy AC9 on the advisory lock | End to end | Two builds started together |
| TC-E1-065-10 | Regression evidence for the access test | Component | Test user with RW-REFADM calls the case read path on the sandbox; refused with MSG-P4-002 |

The six new cases prove the database artefacts of this story. The ten legacy cases are carried as regression evidence: their IDs are kept, their Data is carried onto the split, the Covers text is qualified as regression evidence, the legacy level "System" maps to "End to end" and "Access" to "Component", and the legacy criteria themselves are owned by RWB-P1-E1065-APP. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in a script: the seed, the volumes, the shape count and the pattern rule are the profile of the app story and the contract; this story's scripts hold names, grants and checks only.
- No personal data in a migration, a script, a test fixture or a runbook: the test double holds synthetic rows, the pattern check blocks a real-looking value outside `public`, and the test values are synthetic.
- No read of another schema and no key into another schema: no foreign key of the sandbox crosses a schema, and no statement of this story reads another service's table (DP-01).
- One read-only role: `rwb_sandbox_read` is the only grantee of the sandbox, it holds no write, and it is mapped to one DEV group (DP-02).
- No privilege for PUBLIC anywhere, and no write granted on any object of the three schemas.
- DEV only: the gate refuses any other target before a database is created, and no copy of the sandbox is promoted.
- The delivered objects are asserted and never re-created: a missing view, extension table or dictionary row fails the build instead of being created here.
- An applied migration is never edited: a correction is a new version on the service sequence (DP-15), and a wrong grant is revoked by a later step, never by an edit.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner | The three schemas of 12.7, the DDL set of section 13 and the delivered-objects check | TC-P1-E1065-DB-01, TC-P1-E1065-DB-05, TC-P1-E1065-DB-06 |
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | The read-only role of 12.7, the grant block of section 13 and the personal-data pattern check | TC-P1-E1065-DB-02, TC-P1-E1065-DB-03, TC-P1-E1065-DB-04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1065-APP | App development | Sibling of the same legacy key: the generator, the verifier and the export tool that write into this database and read it back |
| RWB-P1-E1065-CON | Contract | The stage, database, role and failure contract this story implements |
| RWB-P1-E1001-APP | App development | Delivers the baseline, the 13 tables and the dictionary rows this story asserts |
| RWB-P1-E1069-APP | App development | Delivers the 30 views and the three helper functions this story grants on |
| RWB-P1-E1013-APP | App development | Sibling: the freshness reads and the two events of the service |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence and its version allocation, recorded as a note in section 13 |
| RWB-PLT-NF06-DB | ACE DB | The 19 schemas, the 19 logins and the credential policy of the platform |

### 19. Out of scope

- The generator, the verifier, the export tool, the seed profile values and the pipeline stage: RWB-P1-E1065-APP.
- The contract baseline of the build, the seed profile schema and the failure contract: RWB-P1-E1065-CON.
- The 30 `recovery.v_ace_*` views, their helper functions and their conformance test: RWB-P1-E1069-APP.
- The per-service baseline, this service's 13 tables and the dictionary rows: RWB-P1-E1001-APP; the four extension tables: RWB-P1-E1069-DB.
- The 19 schemas and 19 logins of the platform, and the credential policy of the service login `rwb_source_data`: RWB-PLT-NF06-DB.
- The ACE ingestion itself and the 14 Tier 2 tables: the ACE team owns them in RWB-ACE-001, and this story holds their DDL as a fixture only.
- Masked copies of production data in SIT and UAT, the rule scenario build gate, the performance test harness and the PDPA lint: their own stories in the legacy set.
- Any change to the three schema names, the read-only role or the delivered-object list: the data architect and the recovery tech lead, with a new baseline.
- Performance tuning beyond the indexes the baseline creates: the non-functional work.
