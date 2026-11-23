# RWB-PLT-N011-DB PgBouncer pools, migrator role and grant check

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N011-DB |
| Work type | DB (ACE DB) |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-DB |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N011 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-DB-A |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new platform story (N011, created by the realignment — no legacy story text exists for this key). It protects ACE with one PgBouncer pool per login, one migrator login per service and a grant check that runs in every build: the 19 pools are configured on the 19 fixed login names, the 19 migrator logins hold DDL on their own schema only, and the grant check is a pipeline stage beside the migration lint and drift gate of RWB-PLT-E1044-CON. The story creates no schema, no table and no business object. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **ACE database engineer**, I want **one PgBouncer pool per service login with its own connection cap and its own statement timeout, one migrator login per service that holds DDL on that service's own schema only, and a grant check that passes or fails in every build of the platform**, so that **no service can exhaust the ACE PostgreSQL server, no migration can reach a schema it does not own, and a grant that breaks the one-schema-one-login rule is refused by the pipeline instead of being found in production**.

This is a new platform story. It creates no schema (RWB-PLT-NF06-DB creates the 19 `rwb_*` schemas and the 19 logins and their own-schema privileges), no table and no business object. It delivers:

- **Capped connections.** The PgBouncer configuration in front of the ACE PostgreSQL server, with one pool entry per service login — 19 entries, one per login of Template and Rules §R4 and Arch v5 slide 41 — and with its own connection cap and its own statement timeout on each entry (Arch v5 slide 29: "PgBouncer pool and connection cap per login"; "each login goes through its own PgBouncer pool with a connection cap and statement timeout"). The statement timeout of a pool is the 5 s of the SQL view standard of Arch v5 slide 11.
- **Own migrations, one owner.** The 19 migrator logins, one per service, named after the service's schema with the suffix `_migrator`: each owns nothing, is a member of no service login, and holds DDL on its own schema only (Arch v5 slide 29: "each service has one database login that owns its schema and has no grant on any other schema ... Each service runs its own Flyway migrations"; Template and Rules §R5.5 DP-15).
- **Checked in every build.** The grant check — catalogue queries and sessions, held as `db/checks/grant-check.sql` or an equivalent script — that verifies the 19 pools, the 19 service logins, the 19 migrator logins, the own-schema grants and the PUBLIC revokes on every build, and that fails the build when any of them is wrong (Arch v5 slide 29: "Checked in every build — boundary test fails on a cross-schema reference").
- **Nothing that looks like a secret.** Every pool and every migrator login reaches its credential by a key-store reference, and no password, connection string or credential appears in a configuration file, a migration or a pipeline log (NFR-052, NFR-054).
- **Statistics for the platform.** The pool statistics that RWB-PLT-N005-OPS reads for its dashboards and alerts; this story exposes them and builds no dashboard and no alert of its own.

It does not create or drop a schema, a role or a grant of the 19 service logins (RWB-PLT-NF06-DB), it does not issue the SELECT grant on the 30 `recovery.v_ace_*` views (RWB-P1-E1069-DB), and it does not write the migration lint or the drift gate (RWB-PLT-E1044-CON): its check asserts the result across all 19 logins and changes no grant.

### 2. Business rationale

The 19 services share one ACE PostgreSQL server, and Arch v5 makes the sharing safe by two mechanisms that are easy to state and easy to lose in a build: a cap on the connections each service may take, and a grant set that confines each service to its own schema. Slide 29 puts the first in the diagram title — "ACE POSTGRESQL SERVER · PgBouncer pool and connection cap per login" — and in its notes: "each login goes through its own PgBouncer pool with a connection cap and statement timeout; heavy reporting runs from rwb-reporting's own projections, not from ACE tables. Per-schema monitoring." Slide 39 makes it decision 2 of the six decisions the architecture team owes before wave 0: "19 schemas and 19 logins on the ACE PostgreSQL server; connection budget per service; no cross-schema access (ACE team, DBA)". The same slide 29 fixes the second mechanism: "each service has one database login that owns its schema and has no grant on any other schema ... Each service runs its own Flyway migrations", and adds "Ownership is enforced by grants, not by separate servers".

Two availability requirements rest on the connection budget. NFR-020 asks for availability in business hours and NFR-021 for availability outside them, when batch, dispatch and partner exchange run; a capped connection budget is how one service under a burst — or one badly written report — cannot take the server away from the other eighteen, and a statement timeout is how one long query cannot hold a pool slot for the whole of a batch window. Two further requirements rest on the check and on the credential handling. NFR-053 requires data encrypted at rest and in transit, so every pool connects to the server over TLS and no pool offers a plaintext path. NFR-052 requires secrets in the key store and never in code or configuration files, so a pool entry and a migrator login carry a key-store reference and never a password; and NFR-054 requires the pipeline to block a change that carries a secret, personal data or an unapproved dependency, so the grant check is a blocking stage and not a report.

The reason this is a story and not a line in another one is that all three parts fail silently. A missing pool is invisible until a service is throttled by another; a migrator login with a grant outside its own schema is invisible until a migration writes in the wrong schema; a grant to PUBLIC is invisible until a session with no grant reads a table it should not see. Arch v5 answers this with one sentence — "Checked in every build — boundary test fails on a cross-schema reference" — and this story builds the check that carries it, beside the migration lint and the drift gate that RWB-PLT-E1044-CON owns. Template and Rules §R5.7 rule 6 makes wave-0 platform work the Day-1 work of the ACE team, so this story has no build dependency and starts on Day 1.

### 3. Preconditions

- The 19 schema names and the 19 login names of Template and Rules §R4 and Arch v5 slide 41 are fixed: `rwb_source_data`, `rwb_integration`, `rwb_case`, `rwb_access`, `rwb_document`, `rwb_comms`, `rwb_decision`, `rwb_payment`, `rwb_reporting`, `rwb_agent`, `rwb_valuation`, `rwb_treatment`, `rwb_guarantee`, `rwb_litigation`, `rwb_asset`, `rwb_debtsale`, `rwb_writeoff`, `rwb_deviation`, `rwb_partner`. The login of a service is its schema name, so `rwb_case` is both the schema and the login of rwb-case (Arch v5 slides 11, 29 and 41).
- RWB-PLT-NF06-DB creates the 19 schemas and the 19 logins and their own-schema privileges; this story configures the pools on those fixed login names, creates the 19 migrator logins and builds the check, and re-grants nothing. Where a login does not yet exist when the check runs, the check reports it as a precondition finding and does not create it (AC5, §13 ordering note).
- The ACE PostgreSQL server is the Azure Database for PostgreSQL server of Arch v5 slide 29 and accepts a TLS connection from the pool. Whether the cap is delivered by the managed PgBouncer of that service or by a PgBouncer deployment the platform runs is Not specified in the source documents (GAP-1390; ASM-2426).
- The key store of the platform exists and is reachable from the pool deployment and from the migration pipeline at run time, because every credential of this story is a key-store reference and no credential is written anywhere (NFR-052).
- The statement timeout of a pool is the 5 s statement timeout of the SQL view standard in the Arch v5 slide 11 standards table (Transport "PostgreSQL TLS; read-only login", Identity "One login: rwb_source_data", timeout column "5 s statement timeout"). It is the only number in this story that a source fixes.
- The pool mode, the default pool size, the connection cap per login, the idle and connection timeouts and the server-side reserve are Not specified in the source documents (GAP-1388; ASM-2424).
- The migrator login naming, its number and the role that creates it are Not specified in the source documents (GAP-1389; ASM-2425).
- Where the grant check runs, what it publishes and how long the result is kept are Not specified in the source documents (GAP-1391; ASM-2427).
- RWB-P1-E1069-DB holds the grant block that gives `rwb_source_data` SELECT on the 30 `recovery.v_ace_*` views; this story's check asserts that grant as one row of its matrix and never re-issues it.
- RWB-PLT-E1044-CON publishes the migration lint and the drift gate of the per-service Flyway sequence (DP-15); this story's grant check is a separate stage that runs beside them.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Take the 19 login names and the 19 schema names of §R4 and Arch v5 slide 41 into one list that the configuration, the migrations and the check all read, so that no name is typed twice.
2. Write the pool configuration with one entry per service login and no shared entry: 19 entries, each carrying its own connection cap, its own statement timeout of 5 s (Arch v5 slide 11) and the server it connects to.
3. Put TLS on every pool entry and keep the credential of the entry as a key-store reference resolved at run time; no password, no connection string and no other credential is written into the configuration file (NFR-052, NFR-053).
4. Write the migrator role migration on the platform's own sequence: one login per service, `rwb_<name>_migrator`, owning nothing, a member of no service login, with DDL on its own schema only and with no right on any other `rwb_*` schema, on `public` or on schema `recovery`.
5. Give each migrator login its credential as a key-store reference and create it once per service; a repeated run of the role migration reports the role as present and changes nothing.
6. Write the grant check as one script — `db/checks/grant-check.sql` or an equivalent — with the catalogue queries of AC5 and the sessions of AC1 to AC4, one result per login per run, and a non-zero exit on any finding.
7. Wire the grant check as a stage of the platform pipeline, beside the migration lint and the drift gate of RWB-PLT-E1044-CON and not inside them, and make the stage blocking: a finding stops the deploy and names the login, the object and the rule.
8. Expose the pool statistics — the counters each pool holds about its clients, its waiting queue and its server connections — on the platform's metrics path for RWB-PLT-N005-OPS to read, and record no credential in a metric label.
9. Run the whole set twice against the same server, confirm that a repeated run changes nothing, and confirm that no password, connection string or credential appears in the configuration file, in a migration or in a pipeline log (NFR-052, NFR-054).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A login of the 19 has no pool entry, or a pool entry serves two logins | The grant check fails the build and names the login with no pool and the login the shared pool also serves; a shared pool is refused because a cap on it is not a cap per login | Pool check finding, no message id | AC1, AC5 |
| X2 | A pool entry has no connection cap, or no statement timeout, or a statement timeout other than 5 s | The grant check fails the build and names the pool and the missing or unexpected value; the platform default does not stand in for a per-login value | Pool check finding, no message id | AC5 |
| X3 | The connections of one login pass its cap | The pool refuses the connection past the cap and the refusal names the pool; the other 18 pools are unaffected | Pool <name> has no free connection (max connections reached) | AC2 |
| X4 | A statement running in a pool takes longer than the pool's statement timeout | The statement is cancelled and the session is free again; the transaction is not left open | SQLSTATE 57014 canceling statement due to statement timeout | AC2 |
| X5 | A migrator login creates, alters or drops an object outside its own schema, in `public` or in schema `recovery` | The statement is refused and no object changes | SQLSTATE 42501 permission denied for schema <name> | AC3 |
| X6 | A migrator login holds ownership, a membership of a service login, or an elevated attribute | The grant check fails the build and names the login, the membership or the attribute; the login is recreated without it | Grant check finding, no message id | AC4 |
| X7 | A service login holds a grant on another `rwb_*` schema, or a privilege is held by PUBLIC | The grant check fails the build and names the login, the schema and the privilege; the check never revokes it, because the grant belongs to the platform DB story and to the service | Grant check finding, no message id | AC5 |
| X8 | A credential for a pool or a migrator login is written into the configuration file, a migration or a log | The secret scan of the pipeline blocks the stage and names the file and the line without printing the value; the change does not reach the database (NFR-052, NFR-054) | Secret scan finding, value never printed | AC6 |
| X9 | A login named in the pool list does not exist yet when the check runs | The check reports the login as a precondition finding and fails the stage without creating the login; when RWB-PLT-NF06-DB has created it the same run passes (the ordering note of §13) | Precondition finding, no message id | AC5 |

X3, X4 and X9 are the paths the shared server adds to a schema-per-service design; X5, X6 and X7 are the paths that the grant rule of Arch v5 slide 29 makes possible and that the check turns into a failed build; X8 is the NFR-052 path.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the 19 fixed login and schema names, the PgBouncer configuration, the migrator role migrations and the check script only |
| Negotiable | The pool mode, the pool size, the cap, the idle and connection timeouts and the server-side reserve are agreed with the ACE DBA, and the product that delivers the per-login cap with the solution architect; the 5 s statement timeout, the one-pool-per-login rule, the own-schema-only migrator rule and the blocking check are fixed |
| Valuable | Keeps one service from taking the ACE server away from the other eighteen, keeps a migration inside the schema it owns, and turns a cross-schema grant into a failed build instead of an incident |
| Estimable | One PgBouncer configuration with 19 entries, 19 migrator logins, one check script with four catalogue queries and four session proofs, one pipeline stage; six acceptance criteria |
| Small | Days, not weeks: the entries and the logins are generated from one name list, and the check is the only piece of logic |
| Testable | Every criterion is one catalogue query, one refused statement with its SQLSTATE, one connection attempt past a cap, or one pipeline run against a seeded defect |

### 7. Acceptance criteria

```gherkin
Feature: PgBouncer pools, migrator logins and the grant check of the ACE database

  Background:
    Given the 19 schemas and the 19 logins of Template and Rules section R4 and Architecture v5 slide 41
    Given the ACE PostgreSQL server of Architecture v5 slide 29 and a PgBouncer configuration in front of it
    Given the 19 schemas and 19 service logins created by RWB-PLT-NF06-DB, and the SELECT grant of RWB-P1-E1069-DB on the 30 recovery.v_ace_* views

  Scenario: AC1 One PgBouncer pool per service login with its own cap and statement timeout (new, D-RCV-60)
    Given the PgBouncer configuration and the 19 login names of section R4 and Architecture v5 slide 41
    When the configuration is parsed for its pool entries
    Then it holds exactly 19 pool entries, one per service login, and one login per entry
    And no entry serves two logins and no login is served by two entries
    And each entry carries its own connection cap and its own statement timeout of 5 s, per Architecture v5 slide 11
    And each entry connects to the ACE PostgreSQL server over TLS, per NFR-053
    And no entry carries a password, a connection string or any other credential: each carries a key-store reference, per NFR-052

  Scenario: AC2 The cap refuses the connection past it and the statement timeout cancels a long statement with SQLSTATE 57014 (new, D-RCV-60)
    Given one pool entry whose connection cap is a test value (the number is Not specified in the source documents: GAP-1388; ASM-2424)
    When connections are opened through that pool up to and past its cap
    Then the connections up to the cap are accepted and the next one is refused
    And the refusal names the pool and no other pool is refused
    And the other 18 pools accept a connection while the first pool is at its cap
    When a statement runs in that pool for longer than the 5 s statement timeout
    Then the statement is cancelled with SQLSTATE 57014
    And the transaction is not left open and the pool releases the session, per NFR-020 and NFR-021

  Scenario: AC3 A migrator login holds DDL on its own schema only and is refused elsewhere with SQLSTATE 42501 (new, D-RCV-60)
    Given the migrator login of one service and the schema that carries the same name
    When the migrator login creates, alters and drops an object in its own schema
    Then each of the three statements succeeds
    When the same login runs the same three statements in any other rwb_* schema
    Then each statement fails with SQLSTATE 42501
    When the same login runs a statement in schema public and in schema recovery
    Then each statement fails with SQLSTATE 42501
    And the refusal names the schema and no object of that schema changes

  Scenario: AC4 A migrator login owns nothing, holds no elevated attribute and its credential is a key-store reference (new, D-RCV-60)
    Given the 19 migrator logins in the catalogue
    When the catalogue is queried for ownership, memberships and role attributes of each one
    Then no migrator login owns a schema, a table, a sequence, a function or a view
    And no migrator login is a member of a service login of section R4
    And no migrator login holds SUPERUSER, CREATEDB, CREATEROLE, REPLICATION or BYPASSRLS
    And each migrator login holds DDL on its own schema only and no right on any other rwb_* schema, on public or on recovery
    And the credential of each migrator login is a key-store reference and appears in no migration, no configuration file and no log, per NFR-052

  Scenario: AC5 The grant check runs in every build and fails on an extra pool, a missing cap or a grant outside the own schema (new, D-RCV-60)
    Given the grant check as one stage of the platform pipeline, beside the migration lint and the drift gate of RWB-PLT-E1044-CON
    When a build runs on a configuration and a catalogue that satisfy section 11
    Then the stage passes and publishes one result per login for that run
    When the same build runs with any one of these seeded defects: an extra pool, a pool entry missing from the 19, a pool without a connection cap, a pool without a statement timeout, a service login holding a grant on another rwb_* schema, a privilege granted to PUBLIC, a migrator login holding a right outside its own schema
    Then the stage fails and names the pool, the login, the schema or the privilege that carries the defect
    And the deploy of that run does not proceed
    And the stage is not optional and cannot be skipped or reordered in a service's pipeline
    And a login named in the list that does not exist yet is reported as a precondition finding and is never created by the check

  Scenario: AC6 A repeated run changes nothing and no credential appears in a configuration file, a migration or a log (new, D-RCV-60)
    Given the pool configuration and the migrator role migration applied once
    When both are run a second time against the same server
    Then the second run reports the entries and the roles as present and changes no entry, no role and no grant
    And the catalogue shows the same 19 pools, the same 19 migrator logins and the same privileges as after the first run
    When the configuration file, the migrations and the pipeline log of the run are scanned
    Then no password, no connection string and no other credential appears in any of them
    And every credential is a key-store reference resolved at run time, per NFR-052
    And the pipeline blocks the run when a credential is seeded into a configuration file or a migration, per NFR-054
```

These six criteria are new and prove only the deliverable in the title: the 19 pools, the 19 migrator logins and the grant check. No legacy acceptance criterion text exists for this key and none is repeated here. The 19 schemas, the 19 service logins and their own-schema privileges are proven by RWB-PLT-NF06-DB; the SELECT grant on the 30 `recovery.v_ace_*` views is proven by RWB-P1-E1069-DB and merely asserted here as one row of the matrix of AC5.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One PgBouncer pool per service login: 19 entries, one login per entry, no shared entry and no default entry that serves more than one login | Arch v5 slide 29 (pool and connection cap per login); Arch v5 slide 39 decision 2 (connection budget per service) |
| BR2 | Every pool entry carries its own connection cap and its own statement timeout; the statement timeout is 5 s | Arch v5 slide 29 (rule text); Arch v5 slide 11 (SQL view row, "5 s statement timeout") |
| BR3 | Every pool entry connects to the ACE PostgreSQL server over TLS, and no entry offers a plaintext path | NFR-053; Arch v5 slide 11 (SQL view transport "PostgreSQL TLS; read-only login") |
| BR4 | The credential of a pool entry and of a migrator login is a key-store reference; no password, connection string or credential is written into a configuration file, a migration or a log | NFR-052; NFR-054 |
| BR5 | Each service has one migrator login that owns nothing, is a member of no service login and holds DDL on its own schema only: no right on another `rwb_*` schema, on `public` or on schema `recovery` | Arch v5 slide 29 ("one database login that owns its schema and has no grant on any other schema"; "Each service runs its own Flyway migrations"); Template and Rules §R5.5 DP-15 |
| BR6 | A service login holds a grant on its own schema only, and a privilege held by PUBLIC on a Workbench object is a defect in every schema | Arch v5 slide 29; Template and Rules §R5.5 DP-02 |
| BR7 | The grant check runs as a blocking stage in every build of the platform, beside the migration lint and the drift gate of RWB-PLT-E1044-CON and never inside them | Arch v5 slide 29 ("Checked in every build"); NFR-054; Template and Rules §R5.5 DP-15 |
| BR8 | The check asserts the grants of the 19 logins and never issues, revokes or repairs one: the grant set belongs to RWB-PLT-NF06-DB and to the service DB stories | Arch v5 slides 29 and 39 decision 2 (ACE team, DBA own the grants); this story |
| BR9 | A schema may later move to its own server by changing the connection string, so the pool entry of a login is the only place the server of that schema is named | Arch v5 slide 29 ("a schema can move to its own server: change the connection string") |

### 9. State transitions

None in the business sense: this story holds no case and changes no business row. The states it moves through are the states of a pool entry, of a migrator role and of a check run.

| Item | States |
|---|---|
| a pool entry | Absent, present and within its cap, present and at its cap; a removed entry is a new configuration version, never an edit |
| a connection through a pool | Accepted, refused at the cap, cancelled at the statement timeout |
| a migrator login | Absent, present without an elevated attribute, present with a defect that fails the build; never a member of a service login |
| a grant check run | Passed, failed with findings, precondition finding; one result per login per run |
| the pipeline stage | Present and blocking, or absent, which fails the stage-list check of RWB-PLT-N004-OPS |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| ACE database engineer (any team, per U3) | Owns the pool configuration, the migrator role migrations and the check; changes no grant of a service login and no schema |
| ACE DBA | Owns the ACE PostgreSQL server; approves the pool mode, the cap, the pool size, the timeouts, the server-side reserve and the creation of each migrator login (Arch v5 slide 39 decision 2: "ACE team, DBA") |
| Solution architect | Approves the per-login cap shape against Arch v5 slides 11, 29 and 39, and the 5 s statement timeout as the pool value |
| Platform administrator | Approves the key-store reference convention of a pool entry and of a migrator login, and the metrics path the pool statistics are published on |
| DevOps lead | Approves the pipeline stage that runs the grant check, its blocking behaviour and the retention of its result |
| RW-PLATADM | Reads the pool statistics, the login list and the check result for operations and break-glass support; holds no write right on a pool entry, a migrator login or a grant |
| RW-SECADM | Reads the secret-scan and grant-check results of every run; writes nothing in the configuration or in a migration |
| RW-AUDIT | Reads the check result of a run and the login list; changes nothing |
| No approval level from the delegation of authority applies | A connection cap and a grant are not a credit decision |

Every right above is held by a role and never by a person. Where a pool name, a cap value or a migrator credential path would sit, it is Not specified in the source documents (GAP-1388; ASM-2424 and ASM-2425).

### 11. Data

**The 19 pools.** One row per service login, one pool per login. The cap and the pool name are configuration values that no source fixes; the statement timeout is the 5 s of the SQL view standard of Arch v5 slide 11 and is the same value on every pool.

| Login | Schema | Pool | Connection cap | Statement timeout | Notes |
|---|---|---|---|---|---|
| rwb_source_data | rwb_source_data | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Read-only login: its SELECT on the 30 recovery.v_ace_* views is asserted by the check and granted by RWB-P1-E1069-DB |
| rwb_integration | rwb_integration | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only; no grant on any other schema |
| rwb_case | rwb_case | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only; case, CMMN state, queues, tasks, allocation and timers (Arch v5 slide 41) |
| rwb_access | rwb_access | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_document | rwb_document | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only; documents themselves are in Blob storage, not in the database |
| rwb_comms | rwb_comms | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_decision | rwb_decision | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only; the central decision ledger is read and written here and by nobody else |
| rwb_payment | rwb_payment | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_reporting | rwb_reporting | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Heavy reporting runs from rwb-reporting's own projections, not from ACE tables (Arch v5 slide 29) |
| rwb_agent | rwb_agent | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_valuation | rwb_valuation | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_treatment | rwb_treatment | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_guarantee | rwb_guarantee | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_litigation | rwb_litigation | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only; the slide 29 example of a refused cross-schema read is this login on rwb_payment |
| rwb_asset | rwb_asset | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_debtsale | rwb_debtsale | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_writeoff | rwb_writeoff | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_deviation | rwb_deviation | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only |
| rwb_partner | rwb_partner | Not specified in the source documents (GAP-1388; ASM-2424) | Not specified in the source documents (GAP-1388; ASM-2424) | 5 s (Arch v5 slide 11) | Own schema only; partner users reach the service through the partner gateway in the DMZ (Arch v5 slide 29 note) |

The pool mode, the default pool size, the idle and connection timeouts and the server-side reserve are Not specified in the source documents (GAP-1388; ASM-2424) and are held as configuration values, never as code.

**The 19 migrator logins.** One row per service, named after the schema with the suffix `_migrator` by ASM-2425. The privilege list of a migrator login and the object path of its credential are the open values.

| Migrator login | Schema it may change | Privileges | Credential |
|---|---|---|---|
| rwb_source_data_migrator | rwb_source_data | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_integration_migrator | rwb_integration | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_case_migrator | rwb_case | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_access_migrator | rwb_access | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_document_migrator | rwb_document | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_comms_migrator | rwb_comms | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_decision_migrator | rwb_decision | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_payment_migrator | rwb_payment | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_reporting_migrator | rwb_reporting | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_agent_migrator | rwb_agent | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_valuation_migrator | rwb_valuation | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_treatment_migrator | rwb_treatment | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_guarantee_migrator | rwb_guarantee | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_litigation_migrator | rwb_litigation | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_asset_migrator | rwb_asset | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_debtsale_migrator | rwb_debtsale | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_writeoff_migrator | rwb_writeoff | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_deviation_migrator | rwb_deviation | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |
| rwb_partner_migrator | rwb_partner | Not specified in the source documents (GAP-1389; ASM-2425) | Key-store reference (NFR-052); object path Not specified in the source documents (GAP-1389; ASM-2425) |

What the privilege column does not fix is the enumerated list of DDL rights; what it does fix is the rule of AC3: create, alter and drop inside the own schema succeed, and the same statements in another `rwb_*` schema, in `public` and in schema `recovery` fail with SQLSTATE 42501. A migrator login owns nothing and is a member of no service login (AC4).

**What this story holds, and what it does not.** It holds names, references and configuration values: 19 login names, 19 schema names, 19 pool entries with a cap and a timeout each, 19 migrator login names and their own schema, the key-store reference of each credential, and the check that compares all of it against the catalogue. It holds no business value, no personal data and no credential value, in line with §R7.2 s17 and NFR-052.

### 12. Contract

This story provides no REST operation, publishes and consumes no business event, runs no workflow and no Schedule, and owns no table. Its deliverable is one PgBouncer configuration, 19 migrator logins and one check script, all three held as code and all three versioned.

#### 12.1 REST operations provided

None. The ACE database server speaks the PostgreSQL protocol and this story adds no HTTP surface to it.

#### 12.2 REST operations consumed

None. The pipeline calls the platform services it deploys with and the catalogue of the server; neither is a REST contract of this story.

#### 12.3 Events published

None. The pools carry no event and the check publishes to the pipeline only; the topics of the 19 services are owned by RWB-PLT-EVT and by each service (Template and Rules §R4).

#### 12.4 Events consumed

None.

#### 12.5 Workflows and activities

None. No Temporal workflow or activity of this story exists, and the migration pipeline runs on a commit and not in the Temporal namespace `rwb-recovery`.

#### 12.6 Schedules

None. The pool configuration is applied by the deployment and the check is run by the pipeline, not on a Temporal Schedule.

#### 12.7 Tables owned

Tables owned: **None**. This story creates no table, no view and no materialised view, and it reads no business row: every statement it runs is a catalogue query or a session check.

What it does own, and what a reader should look for instead of a table:

| Owned artefact | Where it lives | What it decides |
|---|---|---|
| 19 pool entries, one per service login | The PgBouncer configuration of the platform | The connection cap and the 5 s statement timeout of each service login |
| 19 migrator logins | The role migrations on the platform's own migration sequence | That a service may change its own schema and no other |
| The grant check | `db/checks/grant-check.sql` or an equivalent script, wired as a pipeline stage | Whether a build may proceed |

#### 12.8 Contract fakes

None. This story publishes no service contract and therefore needs no service contract fake. The fixtures the check is proven against stand in for the neighbouring stories and for the ACE head:

| Fixture | Serves | Used by |
|---|---|---|
| `19-schemas-and-logins` container | RWB-PLT-NF06-DB | One PostgreSQL container with the 19 schemas, the 19 service logins and the ownership of section 11, so the check is proven against the real login list |
| `pgbouncer-under-test` container | This story | A PgBouncer process in front of that container, with the configuration under test and its 19 entries |
| `migrator-roles` migration | This story | The 19 migrator logins of section 11, created by this story's own migration on the platform sequence |
| Seeded-defect fixture | This story | An extra pool, a missing pool, a pool without a cap, a pool without a statement timeout, a foreign grant and a privilege for PUBLIC, one per run of AC5 |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic and no ACL in this story |
| Temporal | None | None | No workflow, activity or Schedule |
| File | None | None | The configuration and the check are code in a repository, deployed by the pipeline |
| SQL | 19 PgBouncer pool entries and 19 migrator logins | The catalogue of the ACE PostgreSQL server, through catalogue queries and short sessions | SQL only on the catalogue and on the own schema of a migrator login; no business row is read or written, and no statement of this story reaches another service's schema |

### 13. Solution plan

**Artefacts.** Paths are relative to the platform repository, and the section markers are the design of this story.

| Path | Artefact | What it holds |
|---|---|---|
| `db/pgbouncer/pgbouncer.ini` | The PgBouncer configuration | The listening settings, the TLS requirement of every entry (NFR-053) and the general pool settings; the pool mode is Not specified in the source documents (GAP-1388; ASM-2424) |
| `db/pgbouncer/pools/<login>.ini` or the per-login section of the same file | The 19 pool entries | One entry per service login of section 11: its connection cap, its 5 s statement timeout and its key-store credential reference |
| `db/pgbouncer/names.json` | The one name list | The 19 login names and the 19 schema names of §R4 and Arch v5 slide 41, read by the configuration, the migrations and the check |
| `db/migration/platform/<version>__rwb_platform_migrator_roles.sql` | The migrator role migration | The 19 migrator logins of section 11, each with DDL on its own schema only and no other right |
| `db/checks/grant-check.sql` or an equivalent script | The grant check | The catalogue queries of AC5 and the session proofs of AC1 to AC4; one result per login and a non-zero exit on a finding |
| `pipeline/stages/grant-check.yml` | The stage wiring | The stage that runs the check in every build, beside the migration lint and the drift gate of RWB-PLT-E1044-CON, and blocks the deploy on a finding |
| `observability/pool-stats.md` or the metrics declaration | The statistics exposure | The pool counters that RWB-PLT-N005-OPS reads, with no credential in a label |

**Pattern application**

| DP | Pattern | Where it shows in this story |
|---|---|---|
| None | None of the DP table applies as a named pattern in the metadata: this story introduces no legacy table, no legacy login, no legacy topic and no legacy call, and `patterns` is empty | — |

Two rules of the DP table are nevertheless enforced here and the enforcement is the point of the story. DP-02 (one login per service, replacing the legacy `recovery_svc` login) is what the 19 pool entries and the 19 migrator logins assume and what the grant check asserts: one login per service, a grant on its own schema only and no cross-schema access. DP-15 (per-service Flyway sequence in the service's own schema, on an H dependency to RWB-PLT-E1044-CON) is what the migrator login exists for: each service runs its own sequence in its own schema, and the login that runs it holds DDL there and nowhere else. Neither pattern is applied by this story in the sense of the DP table — no legacy object is moved — so neither is listed under "Patterns applied"; the patterns stay with the service DB stories, and RWB-PLT-E1044-CON keeps the migration lint and the drift gate that DP-15 names.

**Ordering.** The 19 login names and the 19 schema names are fixed by Template and Rules §R4 and by Arch v5 slides 29 and 41, so this story can be configured, migrated and checked on Day 1 without waiting for any other story. Where a login of the list does not yet exist — because RWB-PLT-NF06-DB has not created it in that environment — the check reports the login as a precondition finding and fails the stage; it never creates a service login and never grants on one. This ordering is a note and not a dependency: the Work Package fixes "Depends on (build)" as None, so no H dependency is recorded for RWB-PLT-NF06-DB, RWB-PLT-E1044-CON or RWB-P1-E1069-DB.

**Build steps**

1. Write the one name list of the 19 logins and the 19 schemas, and read the configuration, the migrations and the check from it (AC1).
2. Write the pool configuration with one entry per login, the cap and the 5 s statement timeout on each entry, TLS on every entry and a key-store reference in place of every credential (AC1, AC2, AC6).
3. Write the migrator role migration for the 19 `_migrator` logins, each one with DDL on its own schema only, no ownership, no membership and no elevated attribute (AC3, AC4).
4. Write `db/checks/grant-check.sql`: the catalogue queries for the pools, the logins, the ownership, the attributes, the grants and the PUBLIC revokes, and the session proofs for a refused connection, a cancelled statement and a refused DDL statement (AC1 to AC5).
5. Wire the check as a blocking stage beside the RWB-PLT-E1044-CON migration lint and drift gate, with one result per login per run attached to the pipeline run (AC5).
6. Seed each defect of AC5 in turn — an extra pool, a missing pool, a pool without a cap, a pool without a statement timeout, a foreign grant on a service login, a privilege for PUBLIC, a migrator right outside its own schema — and prove that each one fails the stage and names what carries it (AC5).
7. Expose the pool statistics for RWB-PLT-N005-OPS and confirm that no metric label carries a credential (AC6).
8. Run the configuration and the migration twice against the same container and prove that the second run changes nothing, then scan the configuration, the migrations and the log for a credential (AC6).

**Done when.** The PgBouncer configuration holds exactly 19 pool entries, one per login of §R4 and Arch v5 slide 41, each with its own connection cap and its 5 s statement timeout, over TLS and with a key-store reference in place of every credential; a connection past a cap is refused and names its pool, and a statement longer than the timeout is cancelled with SQLSTATE 57014; the 19 migrator logins create, alter and drop in their own schema and are refused with SQLSTATE 42501 in every other `rwb_*` schema, in `public` and in schema `recovery`; no migrator login owns anything, is a member of a service login or holds an elevated attribute; the grant check runs as a blocking stage in every build and fails on each seeded defect of AC5; a repeated run changes nothing; and the tests of section 16 pass.

The pool name, the pool mode, the pool size, the cap per login, the idle and connection timeouts and the server-side reserve (GAP-1388; ASM-2424), the migrator login privilege list and credential path (GAP-1389; ASM-2425), the product that delivers the per-login cap (GAP-1390; ASM-2426) and the stage's result retention (GAP-1391; ASM-2427) are Not specified in the source documents and are closed by the ACE DBA, the solution architect and the DevOps lead before the first release.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Pool check 1 | A login of the 19 has no pool entry, or one entry serves two logins | Pool check finding, no message id: the check names the login with no pool and the logins a shared entry serves |
| Pool check 2 | A pool entry has no connection cap, no statement timeout, or a timeout other than 5 s | Pool check finding, no message id: the check names the pool and the missing or unexpected value |
| POOL-CAP | A connection is opened past the cap of a pool | Pool <name> has no free connection (max connections reached) |
| SQLSTATE 57014 | A statement runs longer than the statement timeout of its pool | canceling statement due to statement timeout |
| SQLSTATE 42501 | A migrator login runs DDL outside its own schema, in `public` or in schema `recovery` | permission denied for schema <name> |
| Grant check 1 | A service login holds a grant on another `rwb_*` schema, or a privilege is held by PUBLIC | Grant check finding, no message id: the check names the login, the schema and the privilege, and revokes nothing |
| Grant check 2 | A migrator login owns something, is a member of a service login or holds an elevated attribute | Grant check finding, no message id: the check names the login and the attribute |
| Precondition finding | A login named in the list does not exist yet in the environment the check runs against | Precondition finding, no message id: the check names the login and does not create it |
| Secret scan finding | A credential is seeded into the configuration, a migration or the log | Secret scan finding, the value is never printed (NFR-052, NFR-054) |

The pool refusal text and the two SQLSTATE texts are the texts the database itself raises, quoted and not rewritten; the check findings are pipeline texts for engineers and are not part of the message standard. No `MSG-` ID applies to this story: it has no user-facing message, and the messages of the application layer are raised by each service and by the error library of RWB-PLT-LIB. No pipeline log of this story carries a password, a connection string or a personal data field (NFR-052, NFR-054).

### 15. Screens and states

No screen. The result of the check is visible in the pipeline run and in the platform administrator's deployment view, one result per login per run, and the pool statistics are read by the dashboards and alerts of RWB-PLT-N005-OPS. Nothing in this story is shown to a user directly and no Workbench screen state changes: a pool at its cap and a cancelled statement are operational facts of the pipeline and of the observability platform, not states of a case.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N011-DB-01 | AC1 | Component | One PostgreSQL container with the 19 schemas and 19 service logins, a PgBouncer configuration under test: 19 entries parsed, one login per entry, a cap and a 5 s statement timeout on each, TLS required, key-store references only |
| TC-PLT-N011-DB-02 | AC2 | Integration | A pool whose cap is set to a test value: connections up to the cap accepted, the next refused with the pool named and the other 18 pools unaffected; a statement of more than 5 s cancelled with SQLSTATE 57014 and the transaction not left open |
| TC-PLT-N011-DB-03 | AC3 | Component | Sessions as each of the 19 migrator logins: create, alter and drop in the own schema succeed; the same three statements in another rwb_* schema, in public and in recovery each fail with SQLSTATE 42501 and change no object |
| TC-PLT-N011-DB-04 | AC4 | NFR | Catalogue queries over the 19 migrator logins for ownership, membership and the five attributes; the credential path of each from the key store; a scan of the migrations and the configuration for a credential |
| TC-PLT-N011-DB-05 | AC5 | End to end | A pipeline run per seeded defect: an extra pool, a missing pool, a pool without a cap, a pool without a timeout, a foreign grant, a privilege for PUBLIC, a migrator right outside its own schema; each fails the stage and names what carries it, and the stage cannot be skipped |
| TC-PLT-N011-DB-06 | AC6 | Unit | The configuration and the migration applied twice to the same container: the second run reports entries and roles as present and changes nothing; a seeded credential in the configuration and in a migration blocks the run and the value is not printed |

The full test, with its Given, When and Then, sits with the test case register under the same test case ID. No level is "Contract", because this story publishes no contract and the check is proven on a container fixture.

### 17. Guardrails

- No business value in a configuration file: a pool entry holds a login name, a cap, a timeout, a server and a key-store reference, and every business parameter stays with the owning service's contract (Template and Rules §R7.2 s17).
- No personal data anywhere in this story: the configuration, the migrations, the check and its fixtures hold names, counts and roles only, and the fixtures are synthetic.
- No credential in a configuration file, a migration or a log: every pool entry and every migrator login carries a key-store reference resolved at run time (NFR-052), and the pipeline blocks a change that carries one (NFR-054).
- No grant beyond the own schema: a service login holds a grant on its own schema only, a migrator login holds DDL on its own schema only, and the check fails a build that breaks either rule (Arch v5 slide 29).
- No privilege for PUBLIC on a Workbench object, in any schema, and no `GRANT ... ON ALL TABLES IN SCHEMA` anywhere.
- TLS on every pool: no entry offers a plaintext path to the ACE server (NFR-053).
- No change to an ACE schema: this story reads the catalogue and writes no row of an ACE table, and schema `recovery` and schema `public` are read-only to every migrator login.
- No second way for a service to reach another service's schema: no direct connection string, no second pool and no grant is introduced beside the 19 entries and the 19 own-schema privileges (DP-01, DP-02).
- The check asserts and never repairs: it issues no `GRANT` and no `REVOKE`, so a finding is fixed by the story that owns the grant and not by the checker.
- An applied migration is never edited: a correction to a migrator login is a new version on the platform sequence.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts | The key-store reference of each of the 19 pool entries and of each of the 19 migrator logins, and the secret scan of AC6 | TC-PLT-N011-DB-01, TC-PLT-N011-DB-04, TC-PLT-N011-DB-06 |
| NFR-053 | Data is encrypted at rest and in transit | TLS required on every pool entry, and no plaintext path to the ACE server | TC-PLT-N011-DB-01 |
| NFR-054 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency | The blocking grant-check stage and the secret scan of AC6 | TC-PLT-N011-DB-05, TC-PLT-N011-DB-06 |
| NFR-020 | The Workbench is available during business hours | A capped connection budget per service login, so one service cannot exhaust the server in business hours | TC-PLT-N011-DB-02 |
| NFR-021 | Availability outside business hours, when batch, dispatch and partner exchange run | The same caps and the 5 s statement timeout, so one long statement cannot hold a pool slot through a batch window | TC-PLT-N011-DB-02 |
| Arch v5 slide 11 | The SQL view standard: PostgreSQL TLS, one login rwb_source_data, 5 s statement timeout | The 5 s statement timeout of every pool and the TLS requirement of every entry | TC-PLT-N011-DB-01, TC-PLT-N011-DB-02 |
| Arch v5 slide 29 | One PgBouncer pool and connection cap per login; one login per service with a grant on its own schema only; Flyway per service; a boundary test in every build; a schema can move by changing its connection string | The 19 pool entries, the 19 migrator logins, the grant check and the server named only in the pool entry | TC-PLT-N011-DB-01, TC-PLT-N011-DB-03, TC-PLT-N011-DB-05 |
| Arch v5 slide 39 | Decision 2: 19 schemas and 19 logins on the ACE PostgreSQL server, a connection budget per service and no cross-schema access, owned by the ACE team and the DBA | The cap per login and the own-schema-only rule that the check enforces, with the ACE DBA as the approver of every value | TC-PLT-N011-DB-02, TC-PLT-N011-DB-03 |
| Arch v5 slide 41 | One schema rwb_<name> and its own login per service, 19 rows | The one name list the configuration, the migrations and the check read | TC-PLT-N011-DB-01, TC-PLT-N011-DB-03 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-NF06-DB | ACE DB | Sibling of the same platform epic: it creates the 19 schemas, the 19 service logins and their own-schema privileges; this story configures a pool on each of those logins, adds the 19 migrator logins and checks the result. It is not a build dependency, because the login names are fixed by §R4 and a missing login is a precondition finding (the ordering note of §13) |
| RWB-P1-E1069-DB | ACE DB | Holds the SELECT grant of rwb_source_data on the 30 recovery.v_ace_* views and its own grant block; this story's check asserts that grant as one row of its matrix and re-grants nothing |
| RWB-PLT-E1044-CON | Contract | Owns the migration lint and the drift gate of the per-service Flyway sequence (DP-15); this story's grant check is a separate stage that runs beside them and never inside them |
| RWB-PLT-N005-OPS | DevOps | Owns the dashboards and alerts; this story only exposes the pool statistics for them to read and builds no dashboard and no alert |
| The 19 per-service DB stories | ACE DB | Each owns the tables, indexes and grants of its own schema and the Flyway versions that create them; this story owns the pool its login connects through, the migrator login its migrations run as, and the check that refuses a grant outside its schema |

### 19. Out of scope

- The 19 `rwb_*` schemas, the 19 service logins and their own-schema privileges, the credential policy of a service login and the grant set of each service: RWB-PLT-NF06-DB creates them and each service's DB story extends them; this story neither creates a schema nor grants on one.
- The SELECT grant of `rwb_source_data` on the 30 `recovery.v_ace_*` views and the whole grant block of rwb-source-data: RWB-P1-E1069-DB; this story asserts the result and issues no grant.
- The migration lint, the drift gate and the version allocation of the per-service Flyway sequence: RWB-PLT-E1044-CON (DP-15); this story's check is a separate stage.
- The tables, indexes, constraints and dictionary rows of the 19 schemas: the per-service DB stories, each on its own Flyway sequence; this story creates none of them and grants nothing inside a schema.
- The dashboards, alerts, SLOs and the alert thresholds over a saturated pool: RWB-PLT-N005-OPS; this story exposes the counters only.
- The connection pool of the application inside a service (its own HikariCP-style pool and its fetch size): each service's application story; this story governs the pool in front of the database and not the pool inside the JVM.
- The sizing of the ACE PostgreSQL server, its tier, its storage and its server-side connection limit: RWB-PLT-NF03-OPS and the ACE DBA.
- The key store itself, its naming and its rotation policy: RWB-PLT-NF04-OPS; this story references the store and holds no secret.
- The actor catalogue, the screens and the message catalogue: this story adds no screen, no actor and no user-facing message.
- The choice of the product that delivers the per-login cap and every configuration value the ACE DBA owns: GAP-1388, GAP-1389, GAP-1390 and GAP-1391, closed before the first release.
