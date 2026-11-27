# RWB-PLT-NF06-DB Create the 19 rwb_* schemas and logins

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-NF06-DB |
| Work type | DB (ACE DB) |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-DB |
| Wave | 0 |
| Business epic | NF |
| Release | None (new story) |
| Legacy key | NF-06 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-DB-B |
| Size | Small: fits two weeks; the squad confirms the point size at refinement (DOR-RWB-PLT-NF06-DB-16) |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: this is the platform DB story for legacy NF-06 (Moved, no impact). It builds the 19 `rwb_*` schemas and their 19 logins of Arch v5 slide 29 in wave 0, once for all 19 services, on the ACE PostgreSQL server: one schema and one login per service, each login owning its own schema and holding no grant on any other schema, PUBLIC holding nothing, and no table and no view created. The legacy NF-06 story text is absent from the source set, so the criteria are new under D-RCV-60 and derived from Arch v5 slides 11, 29, 38, 39 and 41 and from Template and Rules §R4 (GAP-1386; ASM-2422). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 21 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **ACE database administrator**, I want **the 19 `rwb_*` schemas of Arch v5 slide 29 and the 19 logins, one schema and one login per service and each login owning only the schema of its own name, with PUBLIC holding nothing anywhere**, so that **every Recovery service has a place to keep its own state on the one ACE PostgreSQL server from wave 0, no service can write in another service's schema, and a schema can later move to its own server by changing one connection string**.

This story delivers, once and only once:

- the 19 schemas `rwb_case`, `rwb_decision`, `rwb_access`, `rwb_deviation`, `rwb_valuation`, `rwb_treatment`, `rwb_guarantee`, `rwb_litigation`, `rwb_asset`, `rwb_debtsale`, `rwb_writeoff`, `rwb_document`, `rwb_comms`, `rwb_payment`, `rwb_partner`, `rwb_integration`, `rwb_source_data`, `rwb_reporting` and `rwb_agent` (Arch v5 slide 29; Template and Rules §R4);
- the 19 logins of the same 19 names, one per schema, each owning its own schema and holding no grant, no USAGE and no object privilege on any other `rwb_*` schema (Arch v5 slide 29: "each service has one database login that owns its schema and has no grant on any other schema");
- schema creation (GAP-1384): each schema is owned by its own login; the creation options of the schemas are Not specified in the source documents (GAP-1384);
- environments (GAP-1385): the environments that receive the 19 schemas and logins, and the role that runs the script, are Not specified in the source documents (GAP-1385);
- failover test (GAP-2066): the ACE database failover test is owned by this story with the ACE DBA; the restore test of documents and the database is owned by P5 rwb-document with RWB-PLT-DB;
- login names (GAP-0688, GAP-0758, GAP-1037): the rwb-case login is `rwb_case` and the rwb-document login is `rwb_document`, allocated in section 11 with their own-schema grants and the secret reference of RWB-PLT-NF04-OPS;
- the default privileges of each schema, granted to its own login only, and the PUBLIC revokes on all 19 schemas;
- the catalogue check that keeps the list closed at 19 and fails on a 20th schema, a misspelled name or a schema owned by the wrong login;
- one idempotent script that creates all of this in DEV and SIT in wave 0, and can be run again with no change.

It creates **no table, no view, no sequence, no function and no extension**. The tables of a schema arrive with that service's own DB story on that service's own Flyway sequence (Template and Rules §R5.5 DP-15), and the 30 `recovery.v_ace_*` views are ACE-owned under ADR-010 and are only asserted here, never altered.

### 2. Business rationale

Arch v5 makes the 19 schemas part of the platform that is built once in wave 0. Slide 38 lists "19 schemas + logins" among the wave 0 items next to the service template and Helm chart, the contract libraries, the workflow kit, the Kafka topics and ACLs and Temporal 1.30+, and its note names "the 19 schemas and logins". Slide 39 decision 2 fixes the shape and the owner: "A schema per service in the ACE database: 19 schemas and 19 logins on the ACE PostgreSQL server; connection budget per service; no cross-schema access (ACE team, DBA)". Slide 29 fixes the mechanics: "Data: one ACE database, one schema and one login per service"; "Ownership is enforced by grants, not by separate servers"; "each service has one database login that owns its schema and has no grant on any other schema; only rwb_source_data has SELECT on the views. No cross-schema joins, views or foreign keys ... Each service runs its own Flyway migrations. A boundary test in every build fails on any cross-schema reference"; and "a schema can move to its own server: change the connection string". Slide 20 and Temporal design slide 11 give every service the same shape, "its own Temporal worker and queue, an embedded Drools engine, its own schema", with outbox, inbox and decision record inside that schema.

Without this story, wave 1 starts with nine services that have nowhere to write. Each of them would then create "its" schema and "its" login in its own way, with its own name, its own owner and its own habits about PUBLIC, and the boundary that slide 29 relies on would be a review rule instead of a database fact. Build it once, name it from one list, and every later service DB story only adds objects inside a schema it already owns.

The 19 names are fixed twice over, from the same source: the service table of Template and Rules §R4 with its 19 short names (`source-data`, `integration`, `case`, `access`, `document`, `comms`, `decision`, `payment`, `reporting`, `agent`, `valuation`, `treatment`, `guarantee`, `litigation`, `asset`, `debtsale`, `writeoff`, `deviation`, `partner`) and the schema column of the Arch v5 slide 41 catalogue, one row per service, with the note "schema rwb_<name> in the ACE database with its own login". The catalogue order of slide 29 is the order of section 11.

Four requirements bear directly on the script. NFR-052 holds secrets in the key store and never in code or configuration files, so the script carries no password and no connection string. NFR-053 requires data encrypted at rest and in transit, which is a property of the server and of the connection, and the script asserts that no `sslmode=disable` credential path is introduced by it. NFR-054 makes the build pipeline block a change that carries a secret, personal data or an unapproved dependency, so this script passes the same gate as service code. REQ-DRI-006 fixes the boundary the schemas exist to enforce: no component calls a system of record directly, and source data is read only through the `recovery.v_ace_*` views.

This is Day-1 wave 0 work with no build dependency (Template and Rules §R5.7). It is the precondition of every service DB story and of RWB-PLT-N011-DB, which configures the pools, the migrator login and the grant check on these same login names. Which environments receive the 19 schemas in wave 0 and which role runs the script there is Not specified in the source documents (GAP-1385; ASM-2421).

### 3. Preconditions

- The 19-service list and the 19 short names of Template and Rules §R4 and Arch v5 slide 41 are agreed and frozen, because every schema name, every login name and every check in this story is derived from that list and the list is closed.
- The ACE PostgreSQL server exists in the environment where the script runs, the ACE DBA account holds the right to create a role and a schema on it, and the server's default encoding, collation and tablespace are the ones the DBA standard sets.
- Schema `recovery` exists and holds the 30 `recovery.v_ace_*` views, owned by the ACE side under ADR-010. This story asserts that it exists and does not create, alter or grant on it; the SELECT grant to `rwb_source_data` is RWB-P1-E1069-DB.
- The creation options of each schema are Not specified in the source documents (GAP-1384; ASM-2420): the owner, the encoding and collation, the tablespace, the `ALTER DEFAULT PRIVILEGES` set, the `search_path` and whether the DBA account creates all 19 in one run.
- The environment set is Not specified in the source documents (GAP-1385; ASM-2421): this story runs in DEV and SIT in wave 0, and in UAT and PROD by the same script at the release of the first service of each wave.
- Whether the service login applies its own migrations or a separate migrator does is Not specified in the source documents (GAP-1387; ASM-2423): the login owns its schema, the migrations are applied by the per-service migrator login of RWB-PLT-N011-DB, and this story grants no DDL beyond ownership.
- The legacy NF-06 story text, its acceptance criteria and its test cases are absent from the source set (the legacy index holds the title and zero characters, and no story file), so this story is stated from Arch v5 and from Template and Rules §R4 and its criteria are new (GAP-1386; ASM-2422).
- The credential of each login and its rotation are held outside this script by the credential policy and the key store of RWB-PLT-NF04-OPS (NFR-052); the script creates a login that can log in and carries no password.
- The Kafka topics, the Temporal namespace and the PgBouncer pools are not needed to create a schema and a login: this story has no build dependency and no contract dependency (Template and Rules §R5.7).
- No approval is required to run a Draft script on a development database; the script is released to SIT after the checks in section 16 pass, and each environment run carries its own change record.

### 4. Flow

1. The ACE database administrator takes the closed list of 19 schema names and 19 login names from section 11, which is the schema column of the Arch v5 slide 41 catalogue in the order of slide 29, and confirms the ACE PostgreSQL server, the server version and the account with the right to create a role and a schema.
2. The administrator writes one script, `db/schemas/19_schemas_and_logins.sql`, whose names are fixed literals: no `${...}` token, no environment name and no wildcard. The script has one block per service and the order of the blocks is the order of section 11.
3. For each of the 19 services the script creates the login, with LOGIN set and no password, no SUPERUSER, no CREATEDB, no CREATEROLE, no REPLICATION and no BYPASSRLS, and no membership of another login's role (NFR-052; Arch v5 slide 29).
4. For each of the 19 services the script creates the schema of the same name with that login as its owner, with UTF8 and the server default collation, in the default tablespace, and sets the login's `search_path` to its own schema (ASM-2420).
5. The script revokes PUBLIC on every one of the 19 schemas and sets each schema's default privileges for its own login only, so that an object created later by that login is not readable by PUBLIC and not readable by another login.
6. The script runs once per environment inside one transaction: a failure leaves no half-created schema and no orphan login behind, and a repeated run detects each object as already present and changes nothing (ASM-2421).
7. The administrator runs the catalogue check `db/checks/schema-catalogue.sql`, which reads the closed list from one file, compares the set of `rwb_*` schemas and `rwb_*` logins against it, and fails on a 20th schema, on a misspelled name and on a schema whose owner is not the login of the same name.
8. The administrator runs the privilege check and the emptiness check, records the run in the DBA run sheet with the environment, the count of schemas created, the count of logins created and the result of each check, and attaches the report to the change record of the environment.
9. The script is not run again to change anything: a later object belongs to a service's own Flyway sequence, a later privilege belongs to RWB-P1-E1069-DB or RWB-PLT-N011-DB, and a correction to the script is a new version, never an edit of an applied one.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A schema or a login of the list already exists at the first run in an environment | The script treats it as already present, makes no second object, records the name in the run sheet and continues; the catalogue check decides whether the existing one is right | None | AC5, AC6 |
| X2 | A login tries to create an object in another service's schema | The statement is refused by the database because the login holds no CREATE on that schema; nothing is written and the boundary test of the build would have failed the merge first | SQLSTATE 42501 permission denied for schema rwb_payment | AC2 |
| X3 | PUBLIC is found to hold a privilege in a schema, or a login carries a server-level attribute | The privilege check fails the run and names the schema, the grantee and the privilege; the schema is not declared ready | Check finding, no message id | AC3 |
| X4 | A 20th `rwb_*` schema, a misspelled name or a schema owned by the wrong login is present | The catalogue check fails, names the object, the fault and the expected value, and the environment is not promoted | Check finding, no message id | AC6 |
| X5 | The script or its log would carry a password, a secret or a credential-bearing connection string | The secret scan of the pipeline blocks the change before it runs (NFR-054), and the script is rewritten to hold the login name only (NFR-052) | Check finding, no message id | AC5 |
| X6 | The script fails part-way, on a role that cannot be created or a schema that cannot be owned | The transaction rolls back; no schema and no login of that run survives, and the error names the statement | SQLSTATE 42501 permission denied to create role | AC5 |
| X7 | A service's Flyway migration is pointed at another service's schema | The migration fails on the schema owner, and the boundary test of that service's build fails on the cross-schema reference | SQLSTATE 42501 permission denied for schema | AC7 |
| X8 | A second run of the script is made after a service has populated its schema | The script detects every schema and every login as present and changes nothing; no object of the service is touched and no privilege is reissued | None | AC5, AC7 |

X2 and X7 are the two refusals that make slide 29's boundary a database fact rather than a convention; X1, X4, X5, X6 and X8 are the paths the closed list, the pipeline gate and the idempotent script add.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One script, one closed list and two catalogue checks on the ACE PostgreSQL server; no build dependency, no contract, no application code and nothing to build against |
| Negotiable | The encoding, collation, tablespace, default privileges and `search_path` are agreed with the ACE DBA and the solution architect; the 19 names, the ownership rule, the PUBLIC revoke and the closed list are fixed |
| Valuable | Gives all 19 services a schema and a login on Day 1, turns the cross-schema boundary into a database refusal, and makes a later move of one schema to its own server a connection-string change |
| Estimable | 19 `CREATE ROLE`, 19 `CREATE SCHEMA`, 19 default-privilege sets, one PUBLIC revoke per schema, two catalogue checks and one run sheet |
| Small | Days, not weeks: one script, one list, two checks and a run per environment |
| Testable | Every criterion in section 7 is one catalogue query, one refused statement with its SQLSTATE, or one second run of the same script |

### 7. Acceptance criteria

```gherkin
Feature: The 19 rwb_* schemas and the 19 logins of the ACE database

  Background:
    Given the ACE PostgreSQL server of the environment and schema recovery holding the 30 recovery.v_ace_* views
    Given the 19 short names of Template and Rules section R4 and the 19 schema names of Arch v5 slide 29
    Given the ACE DBA account that creates the 19 schemas and the 19 logins once

  Scenario: AC1 The 19 schemas and the 19 logins exist, one each, with the names of section R4 (new, D-RCV-60)
    Given the script db/schemas/19_schemas_and_logins.sql applied once to the ACE PostgreSQL server
    When the catalogue is queried for every schema and every login whose name starts with rwb_
    Then exactly 19 schemas exist: rwb_case, rwb_decision, rwb_access, rwb_deviation, rwb_valuation, rwb_treatment, rwb_guarantee, rwb_litigation, rwb_asset, rwb_debtsale, rwb_writeoff, rwb_document, rwb_comms, rwb_payment, rwb_partner, rwb_integration, rwb_source_data, rwb_reporting and rwb_agent
    And exactly 19 logins exist with those same 19 names, one per schema
    And the name of each login is the name of the schema it owns
    And no schema rwb_* and no login rwb_* exists beyond those 19

  Scenario: AC2 Each login owns its own schema and holds nothing in any other (new, D-RCV-60)
    Given the 19 schemas and the 19 logins after the script
    When the catalogue is queried for schema ownership and for the USAGE, CREATE and object privileges of each login
    Then each login owns exactly one schema, the schema of its own name
    And has_schema_privilege('<login>', '<other schema>', 'USAGE') is false for each of the 19 logins and each of the other 18 schemas
    And no login holds SELECT, INSERT, UPDATE, DELETE, TRUNCATE or EXECUTE on any object of another rwb_* schema
    And no login is a member of another login's role
    When a session as the rwb_litigation login runs CREATE TABLE rwb_payment.probe (id integer)
    Then the statement fails with SQLSTATE 42501 permission denied for schema rwb_payment
    And the same statement from each of the other 18 logins against another schema is refused with SQLSTATE 42501

  Scenario: AC3 PUBLIC holds nothing and no login carries a server attribute (new, D-RCV-60)
    Given the 19 schemas and the 19 logins after the script
    When the catalogue is queried for the privileges of PUBLIC and for the attributes of every login
    Then PUBLIC holds no USAGE and no CREATE on any of the 19 schemas
    And PUBLIC holds no privilege on any object of those schemas, and no default privilege of any schema grants one to PUBLIC
    And no login has rolsuper, rolcreatedb, rolcreaterole, rolreplication or rolbypassrls set
    And no login holds a membership in another login's role or in a predefined role that reads all data
    When a session as a test role with no grant of its own selects from an object of schema rwb_case
    Then the statement fails with SQLSTATE 42501

  Scenario: AC4 No login reaches schema recovery until RWB-P1-E1069-DB grants it (new, D-RCV-60)
    Given schema recovery with the 30 recovery.v_ace_* views, owned by the ACE side under ADR-010
    When the catalogue is queried for USAGE on schema recovery and for SELECT on each of the 30 views
    Then no login holds USAGE on schema recovery until RWB-P1-E1069-DB grants it to rwb_source_data
    And no login holds SELECT on any recovery.v_ace_* view, because that grant is RWB-P1-E1069-DB and not this story
    When a session as rwb_case selects from recovery.v_ace_account
    Then the statement fails with SQLSTATE 42501 permission denied for schema recovery
    When RWB-P1-E1069-DB has granted USAGE on schema recovery and SELECT on the 30 views to rwb_source_data
    Then rwb_source_data reads each view, and the other 18 logins are still refused with SQLSTATE 42501
    And the script of this story writes no GRANT, no REVOKE and no ALTER on schema recovery, and creates no object in it

  Scenario: AC5 The script is idempotent and carries no credential (new, D-RCV-60)
    Given the script applied once, and its run log and run sheet
    When the same script is applied a second time on the same server
    Then the second run creates no schema, no login, no default privilege and no revoke, and reports every object as already present
    And the catalogue of the 19 schemas, the 19 logins and their privileges is identical before and after the second run
    And neither the script nor its log holds a password, a secret, a key or a connection string carrying a credential (NFR-052)
    And the script holds no environment name and no ${...} token: the 19 schema names and the 19 login names are fixed literals
    And a failure part-way leaves no schema and no login behind, because the run is one transaction

  Scenario: AC6 A 20th schema, a misspelled name or a wrong owner fails the catalogue check (new, D-RCV-60)
    Given the catalogue check db/checks/schema-catalogue.sql and the one closed list of 19 names it reads
    When the check runs against a server that carries a 20th schema rwb_archive, or a schema rwb_sourcedata, or a schema rwb_case owned by the rwb_payment login
    Then the check fails and names the object, the fault and the expected value
    And the check passes only when the set of rwb_* schemas and rwb_* logins is exactly the 19 of section 11, each schema owned by the login of the same name
    And the closed list holds 19 entries and no wildcard, and a 20th entry or a missing one fails the check as well

  Scenario: AC7 Every schema is empty at creation and receives objects only from its own service (new, D-RCV-60)
    Given the 19 schemas created by this story
    When the catalogue is queried for the objects of each schema
    Then no schema holds a table, a view, a materialised view, a sequence, a function, a type, a trigger or an extension
    And each schema holds only the default privileges set for its own login
    When a service's own Flyway sequence runs on its own schema
    Then that service's outbox, inbox and decision-record tables appear in its own schema only (DP-15; Arch v5 slide 20; Temporal and Drools design slide 11)
    And no table and no view of another service appears in a schema this story created, and this story creates none
    And a migration of one service pointed at another service's schema fails on the schema's owner and fails the boundary test of that service's build
```

The seven criteria prove only the deliverables of the title: the 19 schemas, the 19 logins, their ownership, the closed list and the emptiness of the schemas. They inherit no legacy criterion, because the legacy NF-06 story text is absent from the source set (GAP-1386; ASM-2422). AC4 asserts a privilege that belongs to another story: it proves that this story adds none of it, and that the 18 other logins are refused in schema `recovery` until RWB-P1-E1069-DB issues the SELECT grant to `rwb_source_data`.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One ACE database, one schema and one login per service: 19 schemas and 19 logins, and no 20th of either | Arch v5 slides 29, 38 and 39; Template and Rules §R4 |
| BR2 | A login owns the schema of its own name and holds no grant on any other schema; ownership is enforced by grants, not by separate servers | Arch v5 slide 29; ADR-014 |
| BR3 | PUBLIC holds no privilege of any kind in any of the 19 schemas, and no default privilege grants one | Arch v5 slide 29; Template and Rules §R7.2 s17 |
| BR4 | No login is a superuser, holds CREATEDB, CREATEROLE, REPLICATION or BYPASSRLS, or is a member of another login's role | Arch v5 slide 29; NFR-052 |
| BR5 | Only `rwb_source_data` reads ACE through the 30 `recovery.v_ace_*` views; the SELECT grant itself is RWB-P1-E1069-DB, and this story creates no view and no grant in schema `recovery` | Arch v5 slide 29; ADR-010; REQ-DRI-006 |
| BR6 | No cross-schema join, view or foreign key; a service holds another service's IDs and asks the owner through its contract, and the boundary test in every build fails on a cross-schema reference | Arch v5 slide 29 |
| BR7 | Each service runs its own Flyway migrations in its own schema; this story creates no object inside any of the 19 schemas | Template and Rules §R5.5 DP-15; ADR-021; Arch v5 slide 29 |
| BR8 | Every schema name and every login name is a fixed literal: no `${...}` token, no environment name and no wildcard, and the list is closed at 19 | Template and Rules §R4; Arch v5 slide 41 |
| BR9 | The script is idempotent and runs in one transaction: a second run changes nothing, and a failure leaves no schema and no login behind | This story; Arch v5 slide 38 (built once in wave 0) |
| BR10 | A schema can move to its own server later by changing its connection string, so nothing in this story binds a schema to a server beyond its login and the pool of RWB-PLT-N011-DB | Arch v5 slide 29 |

**Coverage of the rules.** BR1 by AC1 and TC-PLT-NF06-DB-01; BR2 and BR6 by AC2 and TC-PLT-NF06-DB-02; BR3 and BR4 by AC3 and TC-PLT-NF06-DB-03; BR5 by AC4 and TC-PLT-NF06-DB-04; BR7 by AC7 and TC-PLT-NF06-DB-06 and -07; BR8 by AC6 and TC-PLT-NF06-DB-06; BR9 by AC5 and TC-PLT-NF06-DB-05; BR10 only as the login binding, by AC2 and TC-PLT-NF06-DB-02, since no test here moves a schema to another server.

### 9. State transitions

None in the runtime sense: a schema has no state machine and this story changes no business row and no case state. The states it moves through are the states of a database object and of its script.

| Item | States |
|---|---|
| a schema of the 19 | Absent, present and empty (this story), populated by its own service's Flyway sequence (that service's DB story), moved to its own server by a connection-string change (BR10) |
| a login of the 19 | Absent, present with LOGIN and no password in the script, credential set by the key-store path of RWB-PLT-NF04-OPS, disabled on a rotation or a retirement |
| the script run | First run creates all 19, second run is a no-op, failed run rolls back to the state before it |
| the catalogue check | Pass (exactly the 19, each owned by its own login), fail (a 20th, a misspelling, a wrong owner) |
| a privilege | Held by the owning login, refused with SQLSTATE 42501 on any other schema, held by PUBLIC which is a failure in every schema |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| ACE database administrator | Owns the script, the closed list and the two catalogue checks; runs them in an environment and records the run in the run sheet |
| ACE team lead | Approves the 19-name list and the creation options of each schema, and accepts the run in DEV and SIT |
| Solution architect | Approves the ownership rule, the closed list and the boundary assertion against Arch v5 slides 29, 38, 39 and 41 |
| Platform administrator | Approves the run in an environment and the change record it carries, and confirms that the login names are the ones the service chart values and the pools will use (RWB-PLT-N011-DB) |
| Release role | Approves the promotion of the run from DEV to SIT to UAT to PROD; holds no write right on the script |
| RW-PLATADM | Reads the run result, the catalogue report and the privilege report for operations and break-glass support; holds no write right on the script or on a schema |
| RW-SECADM | Reads the privilege report and the secret-scan result of every run; writes nothing in the script and grants nothing |
| RW-AUDIT | Reads the closed list, the ownership of the 19 schemas and the run sheet of each environment |

Which role runs the script in UAT and PROD, and which change record each environment needs, is Not specified in the source documents (GAP-1385; ASM-2421). Whether the owning login or the per-service migrator of RWB-PLT-N011-DB applies the migrations is Not specified in the source documents (GAP-1387; ASM-2423); this story grants no DDL beyond ownership either way. No person appears in this story: every right above is held by a role.

### 11. Data

**The 19 schemas and the 19 logins.** One row per service, in the catalogue order of Arch v5 slide 29, with the schema column of the slide 41 catalogue and the "Owns" phrase of that row.

| # | Service (Arch v5 slide 41) | Schema | Login | Owns (slide 41) | Service wave |
|---|---|---|---|---|---|
| 1 | rwb-case | `rwb_case` | `rwb_case` | case, CMMN state, queues, tasks, allocation, timers | 1 |
| 2 | rwb-decision | `rwb_decision` | `rwb_decision` | approvals, central decision ledger, DMN model registry | 1 |
| 3 | rwb-access | `rwb_access` | `rwb_access` | Recovery roles as data, scope, masking policy, DoA table, access log | 1 |
| 4 | rwb-deviation | `rwb_deviation` | `rwb_deviation` | X1-X7 screening, pause, handling, return | 2 |
| 5 | rwb-valuation | `rwb_valuation` | `rwb_valuation` | valuations, D6 route decision, route agent output | 3 |
| 6 | rwb-treatment | `rwb_treatment` | `rwb_treatment` | treatments, contracts, settlement and deed-in-lieu agreements, plan timers | 2 |
| 7 | rwb-guarantee | `rwb_guarantee` | `rwb_guarantee` | TCG and insurance claims, guarantor notices and pursuit | 3 |
| 8 | rwb-litigation | `rwb_litigation` | `rwb_litigation` | legal actions, hearings, judgments, enforcement, LED auction ladder | 3 |
| 9 | rwb-asset | `rwb_asset` | `rwb_asset` | assets taken on, holding, floor price, listings, auction rounds | 2 |
| 10 | rwb-debtsale | `rwb_debtsale` | `rwb_debtsale` | lots, data room, buyer terms, bids, award, transfer | 3 |
| 11 | rwb-writeoff | `rwb_writeoff` | `rwb_writeoff` | eligibility, committee, posting, recovery after charge-off | 4 |
| 12 | rwb-document | `rwb_document` | `rwb_document` | metadata, custody, OCR text and fields, signatures, retention | 1 |
| 13 | rwb-comms | `rwb_comms` | `rwb_comms` | notices, templates, merge fields, proof of delivery | 1 |
| 14 | rwb-payment | `rwb_payment` | `rwb_payment` | payment and proceeds matching, fees, bookings, posting files | 2 |
| 15 | rwb-partner | `rwb_partner` | `rwb_partner` | panel, partner users, instructions, results, fees, scorecards | 4 |
| 16 | rwb-integration | `rwb_integration` | `rwb_integration` | interface config, file runs, outbound items, ACE integration paths | 1 |
| 17 | rwb-source-data | `rwb_source_data` | `rwb_source_data` | ACE view contract, extension tables, freshness, reconciliation | 1 |
| 18 | rwb-reporting | `rwb_reporting` | `rwb_reporting` | measures, snapshots, steering dashboard, regulatory reports | 1 |
| 19 | rwb-agent | `rwb_agent` | `rwb_agent` | agent policies, prompts, runs, guardrails, evaluations | 1 |

The names are copied character for character from the schema column of the slide 41 catalogue; the login of each service is the schema name, as Arch v5 slide 29 shows it (`login rwb_case` beside `schema rwb_case`, `login rwb_source_data` beside `recovery.v_ace_* views: SELECT only`). Schema `recovery` is not one of the 19: it is the ACE-owned schema that holds the 30 views (ADR-010), this story asserts that it exists and leaves it untouched (BR5).

**What the script sets for each of the 19.** The attributes below are the ones this story fixes; the value of an attribute in italics is the assumption ASM-2420, because the sources fix the shape and not the option (GAP-1384).

| Attribute | Value set by the script | Source |
|---|---|---|
| Login name | The schema name, `rwb_<short with _>` | Arch v5 slides 29 and 41; Template and Rules §R4 |
| Login attributes | LOGIN on; NOSUPERUSER, NOCREATEDB, NOCREATEROLE, NOREPLICATION, NOBYPASSRLS; no membership | Arch v5 slide 29; NFR-052 |
| Login credential | None in the script: no password, no secret, no connection string | NFR-052; RWB-PLT-NF04-OPS |
| Schema name | The same 19 fixed literals, no token and no environment name | Arch v5 slides 29 and 41; Template and Rules §R4 |
| Schema owner | The login of the same name | Arch v5 slide 29 |
| Encoding and collation | UTF8 with the server default collation | ASM-2420 |
| Tablespace | The default tablespace of the ACE database | ASM-2420 |
| `search_path` of the login | The service's own schema | ASM-2420 |
| Default privileges | For the owning login only; PUBLIC receives nothing | Arch v5 slide 29; ASM-2420 |
| Privilege on another `rwb_*` schema | None: no USAGE, no CREATE and no object privilege | Arch v5 slide 29 |
| Privilege on schema `recovery` | None from this story: the script grants and revokes nothing on schema `recovery`, and the USAGE and the SELECT grant to `rwb_source_data` are RWB-P1-E1069-DB | Arch v5 slide 29; ADR-010 |
| Objects inside the schema | None at creation | BR7; DP-15 |

**What the script never carries**

| Not in the script or its log | Why | Where it lives instead |
|---|---|---|
| A password, a secret, a key or a connection string with a credential | NFR-052: secrets are held in the key store and never in code or configuration files | The credential path and the key store of RWB-PLT-NF04-OPS |
| A business value, a threshold, a limit or a parameter | Template and Rules §R7.2 s17: no business value in code or configuration | The owning service's parameter and reference-data contract |
| Personal data of any kind, including in a test fixture or a log line | NFR-054 blocks a change that carries personal data in code, tests or logs | Synthetic names only, and no row of any table |
| Another service's schema name in a grant, a default privilege or a `search_path` | A cross-schema privilege would undo the boundary of Arch v5 slide 29 | The check of AC2 fails the run |
| An environment name, a `<schema>` placeholder or a `${...}` token | The 19 names are the same in every environment, so a token could point a run at the wrong schema | The closed list of section 11 |
| A table, a view, a sequence, a function, a type or an extension | The objects of a schema belong to that service's own Flyway sequence | That service's DB story (DP-15) |

The script holds 19 names, 19 owners and the privilege sets of those names, and nothing else. It holds no business value and no personal data, in line with the guardrail of Template and Rules §R7.2 s17 and with NFR-052, NFR-053 and NFR-054.

**BR Field ID.** No data row of this section carries a BR Field ID, because none of its items is a field or entity of LDM v9 or Data Classification v5. The schema and login names, the `search_path`, and the PostgreSQL catalogue names `pg_namespace`, `pg_class`, `pg_default_acl` and `pg_roles` are objects of the ACE PostgreSQL server, not business data (DOR-RWB-PLT-NF06-DB-7).

**Logins of rwb-case and rwb-document (GAP-0758, GAP-1037).** This story allocates the login `rwb_case` (row 1) and the login `rwb_document` (row 12), each the schema name of its row, as Arch v5 slide 29 shows. Each login holds the grants of this section only: its own schema, with no privilege on any other schema. Its secret reference is the credential path and key store of RWB-PLT-NF04-OPS; this story sets no password, secret or connection string.

### 12. Contract

This story publishes no REST operation, publishes and consumes no business event, runs no workflow and no Schedule, and owns no table. Its deliverable is 19 empty schemas, the 19 logins that own them and the privileges of those logins inside their own schemas.

#### 12.1 REST operations provided

None. This is a database story and publishes no operation; the REST base of each service, `/api/recovery/<short>/v1` (Template and Rules §R4), belongs to that service's own CON story.

#### 12.2 REST operations consumed

None. The script calls no service and reads no contract.

#### 12.3 Events published

None. Each service's topic `rwb.<short>.events.v1` (Template and Rules §R4; DP-14) is created by RWB-PLT-EVT, and this story publishes nothing on it.

#### 12.4 Events consumed

None. The script consumes no event and subscribes to no topic.

#### 12.5 Workflows and activities

None. Every service's Temporal worker and queue `rwb-<short>` belong to that service; this story defines no workflow and no activity (Arch v5 slide 20; Temporal design slide 11).

#### 12.6 Schedules

None. The script runs from the release pipeline of an environment, not on a Temporal Schedule.

#### 12.7 Tables owned

None. This story creates no table and no view. What it does own is the platform's database skeleton:

| Owned artefact | Count | State after this story |
|---|---|---|
| Schema `rwb_<short with _>` | 19 | Created, empty, owned by its own login |
| Login `rwb_<short with _>` | 19 | Created with LOGIN and no credential in the script, owning its own schema only |
| Schema ownership | 19 pairs | Each schema owned by the login of the same name, no other owner and no role membership |
| Default privileges | One set per schema | Granted to the owning login only, nothing to PUBLIC |
| PUBLIC revoke | One per schema | PUBLIC holds nothing in any of the 19 |
| Table, view, sequence, function, type, extension | 0 | Arrive with each service's own DB story on its own Flyway sequence |
| Privilege on schema `recovery` | 0 | The USAGE and SELECT grant to `rwb_source_data` is RWB-P1-E1069-DB |

No table of another service, no `recovery.v_ace_*` view and no object of schema `recovery` is created, altered or dropped here.

Owner and service of the rows above: service `platform`; owner the ACE database administrator for every row, except the table, view, sequence, function, type and extension row, which arrives with each service's own DB story.

#### 12.8 Contract fakes

None of this story's own contracts: it publishes no service contract. The Given lines of TC-PLT-NF06-DB-04 that name the 30 `recovery.v_ace_*` views are written against the rwb-source-data contract fake (version Not specified in the source documents (CG-ALL-1276)); the other checks run against a real PostgreSQL server and the delivered schemas.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation provided and none consumed |
| Kafka | None | No topic, no producer and no consumer; the topics are RWB-PLT-EVT's |
| Temporal | None | No workflow, activity or Schedule |
| File | None | One SQL script and one closed list, deployed by the release pipeline and not exchanged with a system |
| SQL | 19 `CREATE ROLE`, 19 `CREATE SCHEMA`, 19 default-privilege sets and the PUBLIC revokes | The whole deliverable: a schema and a login per service on the ACE PostgreSQL server, and catalogue queries only towards schema `recovery` |

### 13. Solution plan

**Artefacts.** Paths are relative to the ACE database release folder, and the section markers are the design of this story.

| Path | Artefact | What it holds |
|---|---|---|
| `db/schemas/19_schemas_and_logins.sql` | The one script | The 19 logins, the 19 schemas, the 19 default-privilege sets, the PUBLIC revokes and the `search_path` of each login, in one transaction, idempotent, with no credential and no token |
| `db/schemas/19-schemas.txt` | The closed list | The 19 schema names and the 19 login names, one per line, read by both checks; 19 entries and no wildcard |
| `db/checks/schema-catalogue.sql` | Catalogue check | The set of `rwb_*` schemas and `rwb_*` logins against the closed list, and the owner of each schema against the login of the same name (AC1, AC6) |
| `db/checks/schema-privileges.sql` | Privilege check | PUBLIC empty, no server attribute on a login, no grant and no USAGE on another `rwb_*` schema, the schema-`recovery` assertion of AC4 (AC2, AC3, AC4) |
| `db/checks/schema-empty.sql` | Emptiness check | No table, view, sequence, function, type, trigger or extension in any of the 19 schemas (AC7) |
| `db/runbook/19-schemas-and-logins-run-sheet.md` | The DBA run sheet | Environment, date, role that ran the script, count of schemas and logins created, count already present, result of each check, and the note that no credential is recorded (AC5) |

**Pattern application**

| DP | Pattern | Where it shows in this story |
|---|---|---|
| None | None of the DP table applies: this story introduces no legacy table, no legacy login of the monolith and no legacy call (`patterns` is empty) | — |

DP-01, DP-02 and DP-15 are the architectural patterns this platform story establishes, and none of them is listed in the metadata, because `patterns` is empty for a new platform story. DP-01 is the `rwb_<name>` schema that replaces `recovery.<table>` and is never read across a service; DP-02 is the one login per service that replaces `recovery_svc`; DP-15 is the per-service Flyway sequence that fills each of these schemas, with RWB-PLT-E1044-CON as its gate. This story creates the container that DP-01 names, the identity that DP-02 names and the empty schema in which DP-15 runs, and it adds no dependency of its own.

**Ordering note.** RWB-PLT-N011-DB configures the PgBouncer pool, the connection cap and the per-service migrator on exactly these 19 login names, so it reads the closed list of this story and creates no login of its own. RWB-P1-E1069-DB adds the USAGE and SELECT grant on the `recovery.v_ace_*` views to the login of row 17 of section 11, and the other 18 logins are refused there by design (AC4). RWB-PLT-E1044-CON owns the Flyway sequence and its lint and drift gate, which fill the schemas after this story. These are recorded here as a note and not as a metadata dependency, because the Work Package fixes "Depends on (build)" as None and this story can run before any of them.

**Cut of the built schema.** How the built recovery schema is cut into the 19 `rwb_*` schemas, and how each V0001 baseline is produced, is Not specified in the source documents (GAP-0285). This story creates no table and assigns only the schema names of section 11.

**Build steps**

1. Write the closed list `db/schemas/19-schemas.txt` with the 19 names of section 11, and make both checks read it and nothing else (AC1, AC6).
2. Write the script: one block per service, in the order of section 11, each with `CREATE ROLE ... LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS`, `CREATE SCHEMA ... AUTHORIZATION <login>`, the `ALTER ROLE ... SET search_path` and the default-privilege statements (AC1, AC2, AC3).
3. Add the PUBLIC revokes on all 19 schemas and prove that no default privilege names PUBLIC (AC3).
4. Make the script idempotent: an object that exists is detected and skipped, and the whole run is one transaction so a failure leaves nothing behind (AC5, X6).
5. Write the catalogue check with its three failing fixtures: a 20th schema, a misspelled name and a wrong owner (AC6).
6. Write the privilege check and the emptiness check, including the assertion that no login holds anything in schema `recovery` (AC2, AC3, AC4, AC7).
7. Run the script and the three checks in DEV, record the run sheet, then in SIT; attach the report to the change record of each environment (AC5).
8. Add the script to the pipeline gate of NFR-054 so that a seeded password, a personal-data line or an unapproved dependency blocks the change before it runs (AC5).

**Done when.** The script creates exactly 19 schemas and 19 logins with the names of section 11, each login owning its own schema and holding nothing in any other, PUBLIC holding nothing anywhere, no login carrying a server attribute, and no login holding anything in schema `recovery` except the USAGE of the login of row 17 of section 11; a second run changes nothing and leaves the catalogue identical; the three checks pass in DEV and SIT and fail on their three fixtures; the run sheet of each environment records the run and no credential; and no schema holds an object, because every object belongs to a service's own Flyway sequence.

The creation options of each schema (encoding, collation, tablespace, default privileges, `search_path`, and whether the DBA account creates all 19) are Not specified in the source documents (GAP-1384; ASM-2420), and so are the environments of wave 0 and the role that runs the script in each of them (GAP-1385; ASM-2421).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Catalogue check 1 | The set of `rwb_*` schemas is not the closed list of 19 | rwb_archive is present in schema set; the list is closed at 19 |
| Catalogue check 2 | A schema name is not the name of its service | rwb_sourcedata does not match the closed list; expected rwb_source_data |
| Catalogue check 3 | A schema is owned by the wrong login | rwb_case is owned by rwb_payment; expected owner rwb_case |
| Privilege check 1 | PUBLIC holds a privilege in a schema, or a default privilege grants one | PUBLIC holds USAGE on schema rwb_case; PUBLIC must hold nothing |
| Privilege check 2 | A login holds a privilege in another service's schema | rwb_litigation holds CREATE on schema rwb_payment; the login owns one schema only |
| Privilege check 3 | A login carries a server attribute | rwb_case has rolsuper set; a service login holds LOGIN only |
| Emptiness check | A schema holds an object at creation | rwb_case holds table case_probe; the objects of a schema arrive on its own Flyway sequence |
| SQLSTATE 42501 | A login creates an object in another service's schema, or a login other than rwb_source_data reads schema `recovery` | permission denied for schema rwb_payment |
| SQLSTATE 42501 | The account that runs the script may not create a role | permission denied to create role |
| Check finding, no message id | Any of the checks above fails in a run | The check names the object, the fault and the expected value, and the environment is not promoted |

No `MSG-` ID applies to this story: it has no user-facing message and shows nothing to a user. The texts above are pipeline and run-sheet findings for the ACE database administrator and are not part of the message standard. Neither the script nor a check log carries a credential or a personal data field (NFR-052, NFR-054).

### 15. Screens and states

None. This story adds no Workbench screen and no screen state. Its result is visible in the release pipeline of the environment, in the DBA run sheet of `db/runbook/19-schemas-and-logins-run-sheet.md` and in the three check reports, which the platform administrator reads under Platform administration R and the internal audit role reads as evidence. A service team never sees these objects directly: it sees its own schema through its own Flyway history and its own tables, which arrive in a later story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-NF06-DB-01 | AC1 | Component | Clean PostgreSQL container with the ACE DBA account: the script applied once; the catalogue returns exactly the 19 schemas and the 19 logins of section 11, each login named as its schema, with no 20th of either |
| TC-PLT-NF06-DB-02 | AC2 | Component | 19 sessions, one per login: each logs in, creates a table in its own schema, and is refused with SQLSTATE 42501 on `CREATE TABLE <other schema>.probe`; the catalogue shows one owned schema per login and no membership |
| TC-PLT-NF06-DB-03 | AC3 | NFR | Catalogue query over `pg_namespace`, `pg_class`, `pg_default_acl` and `pg_roles`: PUBLIC holds nothing in the 19 schemas, no default privilege names PUBLIC, and no login has rolsuper, rolcreatedb, rolcreaterole, rolreplication or rolbypassrls |
| TC-PLT-NF06-DB-04 | AC4 | Integration | Contract fake of rwb-source-data (§12.8) in place of the 30 `recovery.v_ace_*` views, with schema `recovery` on the server: `rwb_source_data` holds USAGE on `recovery` and no view privilege yet, the other 18 logins are refused with SQLSTATE 42501, and the script diff shows no statement on schema `recovery` |
| TC-PLT-NF06-DB-05 | AC5 | End to end | The script run twice on the same server, with a diff of the catalogue before and after; a log scan for a password, a secret, a key, a connection string, an environment name and a `${...}` token; a seeded failure mid-run that leaves no object |
| TC-PLT-NF06-DB-06 | AC6, AC7 | Unit | Three fixtures on top of the delivered server: a 20th schema `rwb_archive`, a schema `rwb_sourcedata`, and `rwb_case` owned by `rwb_payment`; the check fails on each and names the fault; the emptiness check passes on the delivered 19 and fails on a fixture with one table |
| TC-PLT-NF06-DB-07 | AC7 | Unit | Boundary of the table list of section 12.7 (Not specified in the source documents (DOR-RWB-PLT-NF06-DB-12)): the emptiness check on the delivered 19 schemas passes, and on one fixture per kind listed in section 12.7 (table, view, sequence, function, type, extension) it fails on each |


The seven rows are new under D-RCV-60 and inherit no legacy test case, because the legacy NF-06 story carries none (GAP-1386; ASM-2422). Each row is one catalogue query, one refused statement with its SQLSTATE or one second run of the same script, and none needs a service to be built.

### 17. Guardrails

- No business value in the script: it holds 19 names, 19 owners and privilege sets only, and every threshold, parameter and decision stays with the owning service's contract (Template and Rules §R7.2 s17).
- No personal data in the script, a log, a fixture or the run sheet: no row of any table is written, and every test name is synthetic (NFR-054).
- No credential in the script or in a log: no password, no secret, no key and no connection string, and the login's credential is set by the key-store path of RWB-PLT-NF04-OPS (NFR-052).
- No cross-schema grant: a login holds nothing on another `rwb_*` schema, no default privilege names another schema and no `search_path` points outside the service's own schema (Arch v5 slide 29; AC2).
- No `GRANT ... ON ALL TABLES`, `ON ALL SEQUENCES` or `ON ALL FUNCTIONS` in any statement of this story: the schemas are empty and PUBLIC receives a revoke, never a grant.
- PUBLIC holds nothing in any of the 19 schemas and no login is a superuser or holds CREATEDB, CREATEROLE, REPLICATION or BYPASSRLS (AC3).
- The schema is fixed: no `${...}` token, no environment name and no wildcard in the script or in the closed list, so a run cannot target the wrong schema (BR8).
- No object outside the service's own schema: this story creates no table, view, sequence, function, type or extension, and touches neither schema `recovery` nor an ACE schema (BR5, BR7).
- An applied script is never edited: a correction is a new version, because a schema and a login that already exist are changed by a later script and not by an edit of an applied one.

### 18. Traceability

| Requirement ID | Requirement (short) | Element of this story | Test cases |
|---|---|---|---|
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts | The script creates a login with no password, holds no connection string, and the credential is set by RWB-PLT-NF04-OPS | TC-PLT-NF06-DB-05 |
| NFR-053 | Data is encrypted at rest and in transit | The script introduces no `sslmode=disable` path and no plaintext credential; encryption is a server and connection property that the pools of RWB-PLT-N011-DB preserve | TC-PLT-NF06-DB-05 |
| NFR-054 | The build pipeline blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency | The script is a change under the same gate, and a seeded password or personal-data line blocks it before the run | TC-PLT-NF06-DB-05 |
| REQ-DRI-006 | No component calls a system of record directly; source data is read only through the `recovery.v_ace_*` views | The 19 schemas and the 19 logins that make the boundary a database fact; only `rwb_source_data` reaches schema `recovery`, and its view grant is RWB-P1-E1069-DB | TC-PLT-NF06-DB-02, TC-PLT-NF06-DB-04 |
| Arch v5 slide 29 | One ACE database, one schema and one login per service; ownership enforced by grants; no cross-schema joins, views or foreign keys; a schema can move to its own server | The 19 schemas, the 19 logins, the ownership rule, the default privileges and the refusals with SQLSTATE 42501 | TC-PLT-NF06-DB-01, TC-PLT-NF06-DB-02 |
| Arch v5 slide 38 | Wave 0 builds the platform once, including "19 schemas + logins" | The story is wave 0, Day 1, built once for all 19 services and no second time | TC-PLT-NF06-DB-01, TC-PLT-NF06-DB-05 |
| Arch v5 slide 39 | Decision 2: 19 schemas and 19 logins on the ACE PostgreSQL server, connection budget per service, no cross-schema access (ACE team, DBA) | The ACE DBA as the owner role, the closed list and the absence of a cross-schema privilege | TC-PLT-NF06-DB-02, TC-PLT-NF06-DB-03 |
| Arch v5 slide 41 | One row per service with its schema and the note "schema rwb_<name> in the ACE database with its own login" | The 19 names of section 11, copied from the schema column, in the catalogue order of slide 29 | TC-PLT-NF06-DB-01, TC-PLT-NF06-DB-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-N011-DB | ACE DB | Sibling of the platform DB epic: the PgBouncer pool, the connection cap, the per-service migrator login and the grant check on the same 19 login names; it creates no login and no schema |
| RWB-P1-E1069-DB | ACE DB | Adds the USAGE on schema `recovery` and the SELECT on each of the 30 `recovery.v_ace_*` views to `rwb_source_data`, on the login this story creates |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence, its lint and its drift gate: the only path by which an object enters one of the 19 schemas |
| RWB-PLT-NF04-OPS | DevOps | The credential policy, the key store and the rotation path of each login; this story holds no credential |
| RWB-E1-001 | Must change | The built monolith `recovery` schema; its split into the 19 `rwb_*` schemas is this story plus the per-service DB stories, recorded in the Change Register |
| RWB-ITG-E1069-ITG | Integration | Proves the grant matrix across the 19 logins end to end, including the refusal of the 18 non-owning logins in schema `recovery` |

### 19. Out of scope

- The USAGE on schema `recovery` and the SELECT on the 30 `recovery.v_ace_*` views to `rwb_source_data`: RWB-P1-E1069-DB, and this story asserts only that no other login reaches schema `recovery` and that no view privilege exists yet.
- The PgBouncer pool, the connection cap, the statement timeout, the per-service migrator login and the grant check across the 19 logins: RWB-PLT-N011-DB, on these same login names.
- The tables of each schema, including outbox, inbox, decision record and the idempotency table: each service's own DB story on that service's own Flyway sequence (Template and Rules §R5.5 DP-15).
- The Flyway sequence itself, its version allocation, its lint and its drift gate: RWB-PLT-E1044-CON.
- The credential of each login, the key-store object, the rotation interval and the overlap window: RWB-PLT-NF04-OPS (NFR-052).
- The 30 views, the helper functions and the grant block of schema `recovery`: ACE owns the views under ADR-010, and RWB-P1-E1069-APP and RWB-P1-E1069-DB own the view SQL and its grant.
- The migration of the built monolith `recovery` schema, its 92 tables and its dictionary rows into the 19 schemas: RWB-E1-001 (Must change) and the per-service DB stories.
- The ACE PostgreSQL server itself, its version, its backup, its replication, its encryption at rest and its network path: the ACE platform team's own infrastructure work and the ACE DBA standard, and no story of this epic provisions a server.
- The Kafka topics and ACLs, the Temporal namespace and the application code: RWB-PLT-EVT, RWB-PLT-WF and the service stories.
- Per-schema monitoring, alerting and the capacity review of the 19 schemas: the observability epic RWB-PLT-OBS.
- The creation options that the sources leave open (encoding, collation, tablespace, default privileges beyond the owning login, and whether UAT and PROD receive the schemas in wave 0): the gap GAP-1384 and the gap GAP-1385, for the ACE DBA and the solution architect to close before the first UAT run.
