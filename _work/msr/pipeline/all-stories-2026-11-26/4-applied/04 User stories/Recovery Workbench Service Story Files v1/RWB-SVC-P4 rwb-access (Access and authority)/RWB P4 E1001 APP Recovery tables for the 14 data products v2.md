# RWB-P4-E1001-APP Recovery tables for the 14 data products

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-001 |
| Legacy disposition | Must change |
| Build status | In build |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP11, DP14, DP15, DP19 |
| Parallel lane | L-P4-K |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-RDF-001, REQ-RDF-014) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-001 is realigned into rwb-access. The built migration `V0001__rwb_e1_001_recovery_schema.sql` and the 92-table estate with its dictionary are kept as built; this story carries P4's share of that estate — the five authority tables `role`, `permission`, `role_conflict`, `masking_rule` and `delegation_limit` — into the service's own schema `rwb_access` (DP-01, DP-15), with their keys, constraints, indexes and the 44 dictionary rows DF-REF-016 to DF-REF-026, DF-REF-034 to DF-REF-044, DF-REF-055 to DF-REF-062 and DF-REF-198 to DF-REF-211. It provides no REST operation and publishes no event. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E1001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM) and the access service that holds the Recovery roles, the permission matrix, the separation-of-duty pairs, the masking policy and the delegation of authority table as data**, I want **P4's five authority tables created in the service's own schema `rwb_access` with their keys, constraints, indexes and the 44 dictionary rows that describe them, on the service's own Flyway sequence**, so that **the authority data of the Workbench has one home in one schema, no service has to read another service's table to reach it, and every later rwb-access story reads one baseline instead of a table it created for itself**.

The legacy story built the estate as one schema, `recovery`, with 92 tables. D-RCV-60 keeps that build and moves the ownership:

- **Kept as built (§R6, "Must change"; U2):** the migration `V0001__rwb_e1_001_recovery_schema.sql` and the 92 tables it creates in schema `recovery` are the as-built baseline. This story does not rewrite them, does not drop one of them and does not re-open the legacy `recoverySchema` parameter. The legacy `role`, `permission`, `role_conflict`, `masking_rule` and `delegation_limit` tables of that schema are the legacy marker; they are not a target and nothing in this story reads them.
- **The new work is the schema split:** every service now writes its own schema `rwb_<name>`, with its own login and its own Flyway sequence, forward only (DP-01, DP-15; Arch v5 slides 29, 41 and 45). P4's share lands in `rwb_access`; the tables of the other 18 services land with their owners' DB stories. No service reads another service's tables (DP-01); a call goes to the owner's contract, one hop, 2 s timeout (DP-11).
- **The five tables are the authority part of the estate:** `role` (6 business fields, DF-REF-034 to DF-REF-039), `permission` (5, DF-REF-040 to DF-REF-044), `role_conflict` (7, DF-REF-205 to DF-REF-211), `masking_rule` (7, DF-REF-198 to DF-REF-204) and `delegation_limit` (19, DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062). That is 44 business fields and, with the 7 standard columns of the service template on each table, 79 columns.
- **The rest of the estate is not P4's:** `lov_value` is reference data of `rwb-case` (P3) under the ownership ruling and is reached through the reference-data contract (DP-07), not through a table of `rwb_access`; `partner_user` is `rwb-partner`'s (S9); the four rule tables `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are `rwb-decision`'s (P7) under the rule-package registry ruling; the four extension tables are `rwb-source-data`'s (P1). None of them is created, read or referenced here.
- **No rows are loaded here.** This story creates the tables and writes no row of any of them: the role, permission and conflict rows are loaded by RWB-P4-E1019-APP, the policy pack that carries the masking rows by the service's own administration path, and the delegation versions by RWB-P4-E1038-APP. `delegation_limit` is created empty, because the legacy baseline seeded no row of it either.
- **Bases and names:** REST base `/api/recovery/access/v1`, schema and login `rwb_access`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access` (DP-13, DP-14; Arch v5 slides 29 and 41). This story provides no REST operation, publishes no event and starts no workflow; section 12 says which story does.
- **Screens and the edge:** the service route through the gateway-bff composite route exists (DP-19; RWB-PLT-N001-CON) and this story serves no screen through it. No screen is built or asserted here.

### 2. Business rationale

The Workbench keeps its authority data as data, not as code: the role list, the letters of each role in each capability area, the pairs of roles one person may not hold together, the fields a role may see unmasked, and the approval limit per decision, level and product. Legacy RWB-E1-001 created the 92 tables that hold that data, together with the dictionary that describes them and the catalog of the 14 data products DP01 to DP14. Every later story of the module — the role matrix, the masking policy, the delegation table, the access log, the catalog entries — reads those five tables, so the estate's authority part is the floor every P4 story stands on.

**What D-RCV-60 changes.** Not the rationale, not the columns and not the 92-table estate: the built migration is the as-built baseline and stays as built. What changes is the ownership boundary inside the same ACE database. The 92 tables were one schema with one login; they are now 19 `rwb_*` schemas, one per service, each with its own login, its own Flyway sequence and its own grants, and each checked by a test that fails the build on a cross-schema reference (DP-01, DP-15; Arch v5 slides 29, 41 and 45). This story is P4's share of that move: the five tables the authority of every other service is decided against.

**Why these five tables are one slice.** They are the authority answer and nothing else. `role` and `permission` are what `POST /authorise` reads to decide whether a caller holds a letter in a capability area. `role_conflict` is the separation-of-duty rule the same answer applies at sign-in. `masking_rule` is the answer to which personal field a role sees unmasked, at a version. `delegation_limit` is the approval limit the decision centre routes an approval against. Four of the five are versioned by a version column and a `valid_from`/`valid_to` window, so a policy change is a row and never a release. Split away from `rwb_access` they would be four or five cross-schema reads per authorise call, which is exactly what DP-01 forbids.

**Why the catalog and the data dictionary do not move here.** The dictionary is one dictionary over 14 data products and 122 objects, and it stays in `rwb_source_data` with the catalog (RWB-P1-E1001-APP). A second copy in `rwb_access` would answer a second way, and a read of `rwb_source_data.sys_fields` from this service would be a cross-schema read. This story therefore declares its 44 field rows as a build artefact, which the one dictionary carries, and proves them matched by a conformance test; it writes no dictionary row of its own (see GAP-0977 and ASM-1715).

**What the split does not change.** The columns, their physical types, the Field IDs, the version columns and the lists are the ones the technical specification already fixes. The account numbers, customer identities and other personal values stay out of this schema entirely: a delegation row names a holder by user reference, and the masking rows describe fields by Field ID. The measure the module serves is unchanged — rule and limit changes made without a code release, target 100 percent.

### 3. Preconditions

- RWB-PLT-E1044-CON is in place: Flyway runs in the `rwb-access` pipeline and takes the schema name of the service's own schema from the deployment configuration. The legacy parameter `recoverySchema = recovery` and the built `V0001__rwb_e1_001_recovery_schema.sql` are the as-built baseline and are not re-opened.
- The schema `rwb_access` and its login exist, and the pipeline service identity may run migrations in that schema only (RWB-PLT-NF06-DB; DP-01, DP-15). The other 18 `rwb_*` schemas exist with their own logins, and this login holds no grant on any of them.
- The service baseline of `rwb-access` is applied: the service template, the guard library (RWB-PLT-E1037-CON) and the authorise contract stub (RWB-P4-E1037-CON). Those platform contracts are the baseline's, so this story adds no build dependency of its own.
- The DEV and SIT databases of the ACE service exist, with a container database available for the migration test that holds `rwb_access` and no other `rwb_*` schema.
- RWB-P4-E1037-CON is in place as a contract only: the authorise operation and its refusal shape. This story adds no path to it and changes no part of it.
- The dictionary is RWB-P1-E1001-APP's, in `rwb_source_data`. The declaration of this story's 44 field rows is handed to that seed as a build artefact; no runtime read of `rwb_source_data` is made by this story (GAP-0977; ASM-1715).
- The built baseline is in force and stays in force: schema `recovery`, 92 tables, its dictionary and the 30 `recovery.v_ace_*` views, of which only `rwb-source-data` holds a grant (DP-05; Arch v5 slide 29).
- The exact file name and sequence number of this story's migration are fixed at merge under the naming rule of D-RCV-28 (GAP-0978; ASM-1712).
- The constraint names and the index set beyond the read paths of section 13 are Not specified in the source documents (GAP-0979; ASM-1713).

### 4. Flow

1. Pipeline: applies this story's Flyway file on `rwb-access`'s own sequence, in DEV first (DP-15).
2. Migration: creates `role` in `rwb_access` — `id` uuid primary key (DF-REF-034), `role_code` varchar(20) not null (DF-REF-035), `role_name` varchar(80) not null (DF-REF-036), `role_class` varchar(15) not null (DF-REF-037), `default_scope` varchar(8) not null (DF-REF-038), `entra_group` varchar(120) nullable (DF-REF-039) — with `role_code` unique and the 7 standard columns of the service template.
3. Migration: creates `permission` — `id` uuid primary key (DF-REF-040), `role_id` uuid not null with a foreign key to `role.id` (DF-REF-041), `capability_area` varchar(30) not null (DF-REF-042), `letters` varchar(5) not null (DF-REF-043), `matrix_version` varchar(20) not null (DF-REF-044) — with the 7 standard columns.
4. Migration: creates `role_conflict` — `id` (DF-REF-205), `role_code` varchar(20) not null (DF-REF-206), `conflicts_with` varchar(30) not null (DF-REF-207), `reason` varchar(200) not null (DF-REF-208), `conflict_version` varchar(20) not null (DF-REF-209), `valid_from` date not null (DF-REF-210), `valid_to` date nullable (DF-REF-211) — with the 7 standard columns.
5. Migration: creates `masking_rule` — `id` (DF-REF-198), `role_code` varchar(20) not null (DF-REF-199), `field_id` varchar(16) not null (DF-REF-200), `unmasked` boolean not null (DF-REF-201), `masking_version` varchar(20) not null (DF-REF-202), `valid_from` date not null (DF-REF-203), `valid_to` date nullable (DF-REF-204) — with the 7 standard columns.
6. Migration: creates `delegation_limit` — `id` (DF-REF-016), `decision_code` varchar(8) not null (DF-REF-017), `approval_level` varchar(4) not null (DF-REF-018), `product_group` varchar(15) not null (DF-REF-019), `principal_limit` numeric(18,2) (DF-REF-020), `loss_pct_limit` numeric(5,2) (DF-REF-021), `min_price_pct_fmv` numeric(5,2) (DF-REF-022), `holder_user_id` uuid (DF-REF-023), `substitute_user_id` uuid (DF-REF-024), `valid_from` date not null (DF-REF-025), `valid_to` date (DF-REF-026), `limit_version` varchar(20) not null (DF-REF-055), `regulation_item` varchar(10) not null (DF-REF-056), `applies_when` varchar(40) (DF-REF-057), `max_loss_amount` numeric(18,2) (DF-REF-058), `max_delay_count` integer (DF-REF-059), `min_price_pct_principal` numeric(5,2) (DF-REF-060), `min_received_pct` numeric(5,2) (DF-REF-061), `max_term_years` numeric(4,1) (DF-REF-062) — with the 7 standard columns.
7. Migration: creates the indexes of the four read paths of the service — `permission` by `(role_id, capability_area)` under the matrix version, `masking_rule` by `(role_code, field_id, masking_version)`, `role_conflict` by `(role_code, conflict_version)`, and `delegation_limit` by `(decision_code, regulation_item, product_group, valid_from)`. No index names a column of another schema and no index is built for a read this service does not make.
8. Migration: writes no row. `delegation_limit` is created empty, exactly as the legacy baseline created it, and the 24 legacy placeholder rows are not seeded (BR9).
9. Pipeline: runs the conformance test, which compares `information_schema.columns` of the five tables with this story's 44-row declaration in both directions, ignoring the 7 standard columns, and the boundary test, which reads every statement of the migration and fails on any name that is not `rwb_access`.
10. Pipeline: runs the platform index-plan check over the four read paths with the SIT policy pack in place, so the plans of AC10 are asserted in the build and not on a laptop.
11. Pipeline: repeats steps 1 to 10 in SIT.
12. A later story of the service loads rows: RWB-P4-E1019-APP writes the role, permission and conflict rows of an approved matrix file, the administration path writes the masking rows of a policy pack, and RWB-P4-E1038-APP writes delegation version DOA-2026.11 with its 218 rows. This story writes none of them and is complete before any of them runs.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A statement in the migration fails | The transaction rolls back; `rwb_access` is left with none of the five tables of that migration; the pipeline stage fails with the statement named | None (pipeline log) | AC5 |
| X2 | A business column of the five tables has no declaration row, or a declaration row has no column or a different physical type | The conformance test fails and names the table, the column and the Field ID | None (pipeline log) | AC3 |
| X3 | A statement of the migration, a repository or a test names a schema other than `rwb_access` | The boundary test fails and names the statement and the schema it found | None (pipeline log) | AC7 |
| X4 | The migration is applied a second time on a schema where it is already applied | Flyway skips it; no table, column, index or row changes | None | AC6 |
| X5 | The migration reuses a version that the service baseline or the built baseline already holds | The pipeline refuses to apply it; the Flyway history is unchanged | None (pipeline log) | AC4 |
| X6 | A login without a grant on `rwb_access`, or without the right in the capability area, attempts the read | The read is refused before a row is returned; no data leaves the schema | MSG-P4-002 | AC7 |
| X7 | The service asks `rwb-source-data` for ACE data and the contract is unavailable | The answer is withheld; no copy of the data exists in `rwb_access` to fall back on | MSG-P7-003 (produced by the caller) | AC8 |
| X8 | A row of `delegation_limit` is expected after the migration | There is none: the story writes no row, and a test that expects 218 rows is RWB-P4-E1038-APP's | None | AC9 |
| X9 | A new policy version is proposed | It is a row under a new version value with its `valid_from`; no migration, no enum and no build change is needed | None | AC11 |

No exception path of this story changes a case, an approval, a task or a policy answer: this service creates a schema, and the answers the schema serves belong to the stories that read it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the per-service Flyway sequence (RWB-PLT-E1044-CON) and the service baseline of `rwb-access`, both already build dependencies of the service's own stories; every later P4 story reads these five tables |
| Negotiable | The columns and Field IDs are fixed by the technical specification; the constraint names, the index names and the file sequence are agreed at merge (section 13) |
| Valuable | Gives the authority data of the whole Workbench one home, one login and one baseline, and removes the last reason for a service to read another service's table |
| Estimable | One migration, one conformance test, one boundary test, one index-plan check; no endpoint, no event, no workflow |
| Small | Fits two weeks or less with its tests, and it unblocks the service's other stories rather than waiting on them |
| Testable | Each criterion below is one automated test, and the four read paths have a plan assertion |

### 7. Acceptance criteria

```gherkin
Feature: Recovery tables for the 14 data products

  Background:
    Given the environment is SIT
    Given the service is rwb-access, its schema is rwb_access and its REST base is /api/recovery/access/v1
    Given the built baseline holds schema recovery with its 92 tables and its 30 recovery.v_ace_* views

  Scenario: AC1 The five authority tables exist and nothing else does (new, D-RCV-60)
    Given an empty container database with the schema rwb_access and the service's own login, and no other rwb_* schema
    When the pipeline applies the migration "V<seq>__rwb_p4_e1001_access_schema.sql" on rwb-access's own Flyway sequence
    Then rwb_access holds exactly five tables: role, permission, role_conflict, masking_rule and delegation_limit
    Then it holds none of the other 87 tables of the 92-table estate: no recovery_case, no approval, no decision_log_entry, no document, no notice, no lov_value, no partner_user, no rule_package, no rule_package_version, no rule_row and no rule_test_case
    Then it holds no copy of an ACE table: no account, no party, no account_ext and no iam_group
    Then the five tables hold 79 columns: the 44 business fields of section 11 with their Field IDs and the 7 standard columns of the service template on each
    Then no table, view, trigger or constraint of the migration names schema public or any other rwb_* schema
    Then the legacy marker recovery.role is not created, not read and not dropped

  Scenario: AC2 Keys and constraints stay inside rwb_access (new, D-RCV-60)
    Given the five tables created by AC1's migration
    When the keys and constraints of rwb_access are read from the catalogue
    Then each of the five tables has a primary key on id and the 7 standard columns are present with the types of the service template
    Then role.role_code is unique, and permission.role_id holds a foreign key to role.id, both inside rwb_access
    Then no foreign key of rwb_access points at schema public and none points at another rwb_* schema
    Then role_conflict.conflicts_with is varchar(30) and masking_rule.field_id is varchar(16), each a business key by value with no foreign key
    Then delegation_limit carries decision_code, approval_level, product_group, valid_from and limit_version as not null, and principal_limit, loss_pct_limit, min_price_pct_fmv, max_loss_amount, max_delay_count, min_price_pct_principal, min_received_pct and max_term_years as nullable
    Then the constraint names and the index order are Not specified in the source documents (GAP-0979; ASM-1713)

  Scenario: AC3 The 44 dictionary rows are complete and matched (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the 44 dictionary rows of this story's declaration: entity role with DF-REF-034 to DF-REF-039, permission with DF-REF-040 to DF-REF-044, role_conflict with DF-REF-205 to DF-REF-211, masking_rule with DF-REF-198 to DF-REF-204, and delegation_limit with DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062
    When the conformance test compares information_schema.columns of rwb_access with the declaration
    Then it reports 44 of 44 business fields matched by name and physical type
    Then each row names its entity, its field, its data type, its physical type and data product "DP14" (Reference data)
    Then changing the declared physical type of DF-REF-201 from boolean to text fails the test with "DF-REF-201 physical type boolean expected, text found"
    Then adding the column role.branch_code with no declaration row fails the test with "role.branch_code has no data dictionary entry"

  Scenario: AC4 The baseline applies on the service's own Flyway sequence (new, D-RCV-60)
    Given the service baseline of rwb-access is applied and its Flyway history holds the service's own versions only
    When the pipeline applies the migration in DEV and then in SIT
    Then the Flyway history of rwb_access records the version once, and line 1 of the file is "-- Story: RWB-P4-E1001-APP"
    Then the version is later than every version of the service baseline, and no version of the legacy 1.001 line of the built recovery baseline is reused
    Then the migration creates no view, no trigger on a table of another schema, and no grant to another service's login
    Then the file name and its sequence number are fixed at merge under the naming rule of D-RCV-28 (GAP-0978; ASM-1712)

  Scenario: AC5 A failed statement leaves none of the five tables (new, D-RCV-60)
    Given a copy of the migration in which the statement creating table masking_rule fails
    When the pipeline applies it in DEV
    Then the pipeline stage fails and names the failing statement
    Then rwb_access holds none of the five tables of that migration, and role and permission are absent with the rest
    Then the Flyway history of rwb_access has no successful row for that version

  Scenario: AC6 A second run of the same version changes nothing (new, D-RCV-60)
    Given the migration applied in SIT
    When the pipeline runs again in SIT
    Then Flyway reports the version as already applied and applies no statement
    Then rwb_access still holds five tables, 79 columns and the same four indexes
    Then delegation_limit still holds no row

  Scenario: AC7 No table of another service and no ACE table is read (new, D-RCV-60)
    Given the login rwb_access holds grants on schema rwb_access only
    When the build runs the boundary check over the migration, the repositories of the service and the pipeline tests
    Then every statement names rwb_access, and no statement names rwb_source_data, rwb_case, rwb_decision or any other rwb_* schema
    Then a direct SELECT on rwb_source_data.sys_fields through the login rwb_access is refused with insufficient_privilege
    Then a SELECT on recovery.v_ace_iam_group through the login rwb_access is refused with insufficient_privilege, because the 30 recovery.v_ace_* views are granted to rwb-source-data only
    Then a caller without the right in the capability area is refused with MSG-P4-002 by the guard library, before any row of role or permission is returned

  Scenario: AC8 The ACE extension data is reached through the rwb-source-data contract (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the Entra ID group "RWB-SIT-RW-CASEOWN" mapped to role "RW-CASEOWN" from v_ace_iam_group
    Given the rwb-source-data contract mock returns the account_ext row of account "ACC-000123" with its dispute flag and its open date
    When a caller reads its session through the authorise path of rwb-access
    Then the answer names role "RW-CASEOWN" and the group, in one hop with a 2 s timeout
    Then rwb_access holds no copy of the group mapping and no column of account_ext, and the contract answer is the only source
    Then no request is made from rwb-access to a recovery.v_ace_* view, and the field IDs the answer masks come from masking_rule

  Scenario: AC9 delegation_limit is created and stays empty (new, D-RCV-60)
    Given the migration applied in SIT and delegation version DOA-2026.11 not yet loaded
    When delegation_limit is counted
    Then it holds 0 rows and its 19 business columns and 7 standard columns are present
    Then the migration inserted no baseline row and the 24 legacy placeholder rows of the legacy story are not seeded
    Then the load of DOA-2026.11 through RWB-P4-E1038-APP writes its 218 rows, 109 for MORTGAGE and 109 for SSME, and this story writes none of them

  Scenario: AC10 The indexes serve the four read paths (new, D-RCV-60)
    Given the five tables hold the rows of the SIT policy pack, under matrix version "PM-2026.11" and masking version "MASK-SIT-01"
    When the four read paths of the service run with EXPLAIN: the permission rows of a role in one capability area, the masking rows of a role and a field under the masking version in force, the conflicting pairs of a role at the conflict version in force, and the delegation rows of a decision and a product on a date
    Then each plan uses an index whose leading column is the one section 13 names for that path
    Then no plan is a sequential scan of a table that carries a version column
    Then dropping the index of the delegation path makes the plan check fail, so the check cannot pass by accident

  Scenario: AC11 A new version of a policy is a row and not a build (new, D-RCV-60)
    Given the five tables created by AC1's migration
    When a policy change is proposed for matrix version "PM-2026.12", masking version "MASK-SIT-02", conflict version "CONFLICT-2027.01" and delegation version "DOA-2027.01"
    Then each is carried by the version and valid_from columns of permission, masking_rule, role_conflict and delegation_limit
    Then no Java enum, no constant, no check constraint on a list value and no migration change is needed for any of the four
    Then the build is unchanged and the 44 dictionary rows are unchanged
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `rwb_access` holds P4's five authority tables and no other table of the estate; every table, key, index and constraint names `rwb_access` only | DP-01; Arch v5 slides 29, 41 and 45; Ownership Map |
| BR2 | Every business column of the five tables has exactly one dictionary row with its Field ID, data type, physical type and data product, and no column exists without one | Logical Data Model and Data Dictionary v9; TSD P4 v3 T3.1; RWB-P1-E1001-APP |
| BR3 | Every list of values is reference data and is read through the reference-data contract of `rwb-case` with the version in force; no list value is a column, a check constraint or a constant in `rwb_access` | DP-07; R5 default ruling; BR-P4-001, BR-P4-003, BR-P4-004 |
| BR4 | A key by value stays a key by value: `permission.role_id` is the only foreign key and it stays inside `rwb_access`, while `masking_rule.field_id` and `role_conflict.conflicts_with` are business keys with no foreign key | legacy AC1 rule on business keys; TSD P4 v3 T3.3 |
| BR5 | Schema names come from configuration; one migration per story; forward only in PROD; never drop a table in PROD | RWB-E1-044; D-RCV-28; DP-15 |
| BR6 | The built baseline is kept as built: the monolith's `V0001__rwb_e1_001_recovery_schema.sql`, its 92 tables and its dictionary are not rewritten, dropped or re-opened by this story | Template and Rules §R6 "Must change"; U2 |
| BR7 | ACE data is reached only through the contract of its owner: this service holds no grant on the 30 `recovery.v_ace_*` views and no copy of any ACE table | DP-05; ADR-010; D-RCV-35 U4 |
| BR8 | No personal data in the schema: the five tables hold role codes, capability areas, Field IDs, decision codes, amounts and versions, and a delegation holder is a user reference (uuid), never a name, an e-mail address or an identity number | NFR-039; NFR-040; legacy §17 |
| BR9 | `delegation_limit` is created empty; its rows are a versioned load of RWB-P4-E1038-APP and the 24 legacy placeholder rows are not seeded | legacy §11; D-RCV-34; RWB-E1-038 |
| BR10 | Separation of duty and masking are data with a version: `role_conflict`, `masking_rule` and `delegation_limit` carry their version column and their `valid_from`/`valid_to` window, so a change is a row and never a release | BR-P4-003, BR-P4-004, BR-P4-006; Principle 1 |
| BR11 | One writer per table and one reader per path: this story creates the five tables and writes no row; the role, permission and conflict rows are RWB-P4-E1019-APP's, the masking rows belong to the service's policy-pack load, and the delegation versions are RWB-P4-E1038-APP's | Ownership Map; RWB-P4-E1019-APP; RWB-P4-E1038-APP |

Where each rule lives in the target: BR1 is the migration and the boundary test, and it is the rule that turns one schema into 19. BR2 is the 44-row declaration and the conformance test; the dictionary rows themselves stay in `rwb_source_data`, because one dictionary over 14 data products cannot be split (GAP-0977). BR3 is the absence of `lov_value` from `rwb_access`: the lists are `rwb-case`'s and arrive through the contract, so a new capability area or a new level is a row of a list and not a change here (AC11). BR4 keeps `permission.role_id` as the only foreign key, which is why the schema has one relationship and no join to another schema. BR5 is the per-service sequence and the file naming. BR6 is the boundary between this story and the built baseline: the monolith keeps its version and this story starts a new line. BR7 is the grant test of AC7. BR8 is the reason the schema is safe to log: nothing in it is personal. BR9 is the empty table of AC9. BR10 is the version columns of AC11. BR11 is the reason this story has no write method and no load path.

### 9. State transitions

This story changes no case, approval, task or policy state and answers no request. It changes the Flyway version of `rwb_access` and nothing else.

| From | To | Trigger |
|---|---|---|
| `rwb_access` at the service baseline, without P4's authority tables | `rwb_access` at the version this story applies: five tables, 79 columns, four indexes, no row | The pipeline applies the migration in DEV, then in SIT |
| The version applied | The version applied, no change | The same file runs again; Flyway skips it and no object changes (AC6) |
| `delegation_limit` empty | `delegation_limit` holding DOA-2026.11 with 218 rows | RWB-P4-E1038-APP's load; not this story (AC9) |
| `permission` at matrix version PM-2026.11 | `permission` at matrix version PM-2026.12 | RWB-P4-E1019-APP's load; not this story (AC11) |
| `masking_rule` at masking version MASK-SIT-01 | `masking_rule` at masking version MASK-SIT-02 | The service's policy-pack load; not this story (AC11) |
| The built baseline at version 1.001 | The built baseline at version 1.001, unchanged | Never: this story does not touch the monolith line (BR6) |

The rows of the five tables move under their own version columns and windows; the schema's version moves only on a migration.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Pipeline service identity (`rwb-access` pipeline) | Runs the migration, the conformance test, the boundary test and the plan check in DEV and SIT, in `rwb_access` only |
| ACE team (suggested; any team may pick up this story) | Reviews the DDL, the keys, the constraints and the grants, and creates the schema and the login with RWB-PLT-NF06-DB |
| RW-SECADM, security administrator | Owns the schema change as the data owner of the roles, the conflicts and the masking policy; approves it through the change process; holds no DDL right in PROD outside the pipeline |
| RW-COE, center of excellence analyst | Reads the structure of the tables and the declaration to answer a policy question; writes no row and changes no DDL |
| RW-AUDIT, internal audit | Reads the dictionary rows and the migration to verify that the authority data has one home; writes nothing |
| The other services' logins | Hold no grant on `rwb_access`: a table read is refused with insufficient_privilege, and the supported path is the contract of RWB-P4-E1037-CON |
| `rwb-access` itself | Reads its own five tables and writes no row of them in this story (BR11) |

No approval level from the delegation of authority applies to this story: it creates a schema and approves no limit. Every "who" here is a role code; the roles, their permissions and the separation-of-duty pairs are held as data in the tables this story creates.

### 11. Data

| # | Table in `rwb_access` | BR Field IDs | Business fields | Read or write in this story |
|---:|---|---|---:|---|
| 1 | `role` | DF-REF-034 to DF-REF-039 | 6 | Create (table only) with `role_code` unique; read |
| 2 | `permission` | DF-REF-040 to DF-REF-044 | 5 | Create (table only) with the foreign key to `role.id`; read |
| 3 | `role_conflict` | DF-REF-205 to DF-REF-211 | 7 | Create (table only); read |
| 4 | `masking_rule` | DF-REF-198 to DF-REF-204 | 7 | Create (table only); read |
| 5 | `delegation_limit` | DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 | 19 | Create (table only), empty; read |

The five tables hold 44 business fields and 79 columns with the 7 standard columns of the service template on each: `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at` and `updated_by`. The exact Field IDs of those 35 standard columns are Not specified in the source documents (GAP-0977; ASM-1711): they are carried by the one dictionary's seed, and the 44 business Field IDs above are the ones this story declares and cites. Field IDs are those in the Logical Data Model and Data Dictionary v9 and in TSD P4 v3 T3.1; the physical types are TSD P4 v3 T3.1 character for character.

**What is not in the schema.** `lov_value` and the reference tables are reference data of `rwb-case` (P3) under the ownership ruling and are reached through DP-07; `partner_user` is `rwb-partner`'s (S9); the four rule tables are `rwb-decision`'s (P7) under the rule-package registry ruling; the four extension tables are `rwb-source-data`'s (P1). None of them is created, read or referenced here, and none of their columns appears in the dictionary rows of this schema. The Ownership Map is the only source of this list (GAP-0976; ASM-1710).

**Collections and views.** The service owns no collection and no view. The read model `v_data_dictionary` is RWB-P1-E1001-APP's and is not created here; the masking answer is a read of `masking_rule`, not a view. `entra_group` on `role` is kept because TSD P4 v3 T3.1 gives it Field ID DF-REF-039, although FSD P4 v3 describes the group as read from `v_ace_iam_group` and not as a Workbench column; the technical specification outranks the functional one, so the column exists and the runtime read comes from the contract (GAP-0980; ASM-1714).

**Rows.** No row of any of the five tables is written by this story. `delegation_limit` holds no baseline row and its content is loaded as version DOA-2026.11 through RWB-P4-E1038-APP (legacy §11; D-RCV-34). The role, permission and conflict rows arrive with RWB-P4-E1019-APP, and the masking rows with the service's policy-pack load.

### 12. Contract

#### 12.1 REST operations provided

None. This story provides no REST operation. The operations of the schema — `POST /api/recovery/access/v1/authorise`, `GET /api/recovery/access/v1/me/permissions`, `GET /api/recovery/access/v1/doa-limits` and the masking-policies read — are RWB-P4-E1037-CON's and RWB-P4-E2013-APP's, and this story only makes the tables they read exist.

#### 12.2 REST operations consumed

None. This story calls no REST operation of any service. The ACE group mapping it names in AC8 is read at run time by the service through the `rwb-source-data` contract (DP-05), not by this story, and nothing in the migration reaches another service.

#### 12.3 Events published

None. This story produces no event. The topic `rwb.access.events.v1` with the events `AccessPolicyChanged` and `DoaLimitChanged` is named by DP-14 and resolved by the topic-naming library, and the events themselves are published by the stories that change a policy row (RWB-P4-E1019-APP, RWB-P4-E1038-APP). A schema migration is not a policy change and publishes nothing.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14, whose event subscription is "none", and this story adds no subscription. No event starts a migration.

#### 12.5 Workflows and activities

None. No Temporal workflow and no activity is in this story, and nothing is registered on task queue `rwb-access` in namespace `rwb-recovery`. The six-monthly access review Schedule (JOB-18) is the service's own and is not part of a schema baseline.

#### 12.6 Schedules

None. The migration runs on a deployment, not on a Schedule, and this story creates or changes no Temporal Schedule (DP-10 is not in this story's pattern set).

#### 12.7 Tables owned

| Table | Schema | Owner (Ownership Map) | This story |
|---|---|---|---|
| `role` | `rwb_access` | P4 | Creates with `role_code` unique and its index; read only otherwise |
| `permission` | `rwb_access` | P4 | Creates with the foreign key to `role.id` and its read index; read only otherwise |
| `role_conflict` | `rwb_access` | P4 | Creates with its conflict-version index; read only otherwise |
| `masking_rule` | `rwb_access` | P4 | Creates with its masking-version index; read only otherwise |
| `delegation_limit` | `rwb_access` | P4 | Creates empty with its delegation read index; writes no row |
| `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` | `rwb_source_data` | P1 | **Never read and never written.** The dictionary and the catalog are RWB-P1-E1001-APP's; this story declares its 44 field rows as a build artefact |
| `lov_value`, the reference tables | `rwb_case` | P3 | **Never read.** Reached through the reference-data contract of DP-07 |
| `partner_user` | `rwb_partner` | S9 | **Never read** |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | `rwb_decision` | P7 | **Never read.** Reached through the rule-package registry of DP-04, which this story does not use |
| `approval`, `decision_log_entry` | `rwb_decision` | P7 | **Never read and never written** |
| `recovery_case`, `task`, `queue` | `rwb_case` | P3 | **Never read and never written** |
| the other tables of the 92-table estate | their owners' schemas | the 18 other services | **Never read.** No grant, no join, no constraint, no view (DP-01) |

The 19 service schemas of the estate are never read by `rwb-access`, and `rwb-access` writes nothing outside `rwb_access`. The database login is the service's own, with grants on `rwb_access` and on no other schema and no grant on the 30 `recovery.v_ace_*` views, which are `rwb-source-data`'s (DP-01, DP-05; Arch v5 slides 29 and 41). The five-table list, the constraint set and the sequence assignment are recorded as GAP-0975 to GAP-0980 with ASM-1709 to ASM-1715.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| rwb-source-data contract fake | DP-05 (no H and no C dependency: the contract is `rwb-source-data`'s) | The `v_ace_iam_group` mapping and the `account_ext` row of AC8, and the 44 dictionary rows of AC3 |
| Flyway sequence fake (RWB-PLT-E1044-CON) | The per-service Flyway sequence | AC4, AC5 and AC6 on a container database: the apply, the rollback and the skip |
| guard library fake (RWB-PLT-E1037-CON, the service baseline) | The guard library that carries the authorise answer | The MSG-P4-002 refusal of AC7 |
| topic-naming library fake (RWB-PLT-E1047-CON, the service baseline) | The naming library of DP-14 | The topic and event names are resolved, never typed, so no test asserts a literal |
| schema and login fixture (RWB-PLT-NF06-DB) | The 19 `rwb_*` schemas and the one login each | AC7's grant test: `rwb_access` holds a grant on its own schema only |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0, consumed 0 | The base `/api/recovery/access/v1` is named; no operation is added |
| Kafka | Published 0, consumed 0 | Topic `rwb.access.events.v1` named for DP-14; this story produces nothing on it |
| Temporal | 0 workflows, 0 activities, 0 schedules | Queue `rwb-access` is not used |
| File | 1 build-time, 0 at run time | The dictionary field declaration of the 44 rows, read by the conformance test and handed to the one dictionary's seed |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/schema`, Java package `th.co.scb.ace.workbench.recovery.access.schema`. Service base `/api/recovery/access/v1`, schema and login `rwb_access`, topic `rwb.access.events.v1`, task queue `rwb-access` (not used here). The migration sits on the service's own Flyway sequence, in `rwb-access`'s pipeline (DP-15).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy marker this slice replaces is one schema with one login and one `V0001` baseline (DP-01 and DP-15): the split is the new work, and it is the change §R6 records. The table names of the monolith — `recovery.role`, `recovery.permission`, `recovery.role_conflict`, `recovery.masking_rule` and `recovery.delegation_limit` — are legacy marker text only: they are the as-built objects of the built baseline, they stay as built, and they are not the target and not a read path. DP-03, DP-05, DP-06, DP-07, DP-11, DP-14 and DP-19 are carried by the legacy key and their work on the runtime path sits with the stories that read or change the tables: the decision record is written by the stories that change a policy row (DP-03), the ACE data is read through `rwb-source-data` at run time (DP-05), the authorise answer reads the parameter and the reference lists through their contracts (DP-06, DP-07) in one hop with a 2 s timeout (DP-11), the topic names are resolved by the library (DP-14) and the screens come through the gateway-bff route (DP-19). This story creates a schema, so none of them adds a call of its own.

This secondary slice adds no new build dependency of its own (metadata "Depends on (build)" is None): the platform libraries, the per-service Flyway baseline, the naming library and the edge route are already build dependencies of the P4 service's own stories, in particular RWB-P4-E1037-CON and RWB-P4-E1038-APP, and this story builds against the service baseline's published contracts and their fakes. The dependency column above is the DP table's canonical row, not a new H edge from this story.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<seq>__rwb_p4_e1001_access_schema.sql` | Flyway migration | Creates the five tables in `rwb_access` with their keys, constraints, indexes and the 7 standard columns; writes no row; creates no view, no trigger and no grant |
| `AccessFieldDeclaration` | Build artefact and test fixture | The 44-row declaration of the five tables' business fields, with entity, field, Field ID, data type, physical type and data product; the single source of the declaration the conformance test compares against |
| `AccessDictionaryConformanceTest` | Test (pipeline) | Compares `information_schema.columns` of `rwb_access` with the declaration in both directions, ignoring the 7 standard columns; names any column without a row and any row without a column or with a different physical type |
| `AccessSchemaBoundaryTest` | Test (pipeline) | Reads every statement of the migration and every repository of the service and fails on a schema name other than `rwb_access`, on a grant to another login and on a foreign key that leaves the schema |
| `AccessIndexPlanTest` | Test (pipeline) | Asserts the four read paths' plans against the SIT policy pack, and fails when an index of a read path is dropped |
| `AccessGrantFixture` | Test fixture | The `rwb_access` login with grants on its own schema only, used by the refusal assertions of AC7 |

**Database and migrations**

- Creates the five tables of section 11 in `rwb_access` and nothing else: no `lov_value`, no `partner_user`, no rule table, no extension table, no case, decision, document, notice, payment or reporting table, and no `lake_copy_watermark` (DP-17 is not this story's).
- The migration is one transaction: a failing statement leaves none of the five tables (AC5), and a second run is a skip (AC6).
- `permission.role_id` is the only foreign key and it points at `role.id` in the same schema. `role_conflict.conflicts_with` and `masking_rule.field_id` are business keys by value, with no foreign key, exactly as the estate's links to an ACE record are business keys with no foreign key (BR4).
- No constraint, index or default names schema `public` or another `rwb_*` schema. A link to an ACE record — the `field_id` of a masking row, the `holder_user_id` of a delegation row — is a value, never a foreign key (AC7, BR7).
- Indexes, in the order the read paths need them: `permission (role_id, capability_area)`; `masking_rule (role_code, field_id, masking_version)`; `role_conflict (role_code, conflict_version)`; `delegation_limit (decision_code, regulation_item, product_group, valid_from)`. Their names follow the platform naming convention; the names and the column order beyond the leading column are Not specified in the source documents (GAP-0979; ASM-1713).
- The migration writes no row, and `delegation_limit` is created empty (BR9, AC9).

**Migrations in order** (the service's own sequence, forward only)

1. The service baseline: the schema, the login and the service template's standard columns (RWB-P4-E1037-CON; RWB-PLT-NF06-DB). Already applied.
2. This story: `V<seq>__rwb_p4_e1001_access_schema.sql`, the five tables, their keys, constraints and indexes. Nothing else.
3. After it, the row loads of the service's own stories: the matrix file (RWB-P4-E1019-APP), the policy pack's masking rows, and delegation version DOA-2026.11 (RWB-P4-E1038-APP). This story neither creates nor depends on them.

**Configuration and reference data.** The schema name of the service's own schema comes from the deployment configuration of `rwb-access` (RWB-PLT-E1044-CON); the legacy parameter `recoverySchema` stays the as-built value of the baseline and is not read by this story. Every list the five columns are checked against — LOV-ROLE, LOV-ROLE-CLASS, LOV-SCOPE, LOV-CAPABILITY, LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT — is read through the reference-data contract of `rwb-case` with the version in force (DP-07), never stored as a check constraint or a Java enum, which is why a new role or a new capability area needs no migration (AC11). No value the business may change is written in this story's code or in its migration.

**Build steps**

1. Write `V<seq>__rwb_p4_e1001_access_schema.sql` from TSD P4 v3 T3.1, with the schema taken from configuration; run it on an empty PostgreSQL container that holds `rwb_access` and no other `rwb_*` schema, and prove it creates exactly five tables, 79 columns and four indexes.
2. Prove the boundary: the migration names `rwb_access` only, creates no view, no trigger and no grant, and a direct read of `rwb_source_data.sys_fields` and of `recovery.v_ace_iam_group` through the service login is refused (AC7).
3. Write `AccessFieldDeclaration` with the 44 rows and `AccessDictionaryConformanceTest`; prove the test fails on an extra column and on a changed physical type (AC3).
4. Prove the rollback and the skip: a copy that fails on `masking_rule` leaves none of the five tables and no successful version (AC5); a second run changes nothing (AC6).
5. Prove the version line: the file records its version once, the version is later than every baseline version, no legacy 1.001 version is reused, and line 1 carries the story key (AC4).
6. Write `AccessIndexPlanTest` over the four read paths with the SIT policy pack; prove it fails when an index is dropped (AC10).
7. Prove no row is written: `delegation_limit` holds 0 rows after the migration, and the 24 legacy placeholder rows are not seeded (AC9).
8. Prove that a new version value, a new capability area and a new level need no build: a row with `PM-2026.12`, `MASK-SIT-02`, `CONFLICT-2027.01` or `DOA-2027.01` is accepted as data (AC11).
9. Hand the 44-row declaration to the one dictionary's seed (RWB-P1-E1001-APP) as a build artefact and record the handover in the change register; write no row of `rwb_source_data` from this service (GAP-0977).

**Feature switch.** None of this story's own. A migration is not behind a flag: the five tables either exist at the version or the pipeline has not applied it (BR5, BR6). The service-level flag of the authorise path belongs to RWB-P4-E1037-CON, and the policy answers behind it are switched by their version rows, not by a flag.

**Done when.** The tests in section 16 pass; the migration runs clean in DEV and SIT on `rwb-access`'s own sequence; `rwb_access` holds exactly the five tables with 79 columns, four indexes and no row; the conformance test reports 44 of 44 business fields matched; the boundary test reports no statement, no constraint and no grant outside `rwb_access`; and the four read paths use their indexes.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-002 | A caller without the right in the capability area, or a login without a grant, attempts the read | You cannot {action} here. Your role does not include it. | The guard library (RWB-P4-E1037-CON); this story asserts the refusal and creates none of it |
| MSG-P7-003 | The `rwb-source-data` contract is unavailable and the answer cannot be completed | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The caller; this story holds no fallback copy of the data |
| None (pipeline log) | A migration statement fails | The stage fails and names the failing statement and its line | The pipeline (AC5) |
| None (pipeline log) | A column has no declaration row, or a row has no column or a different physical type | "{table}.{column} has no data dictionary entry" or "{fieldId} physical type {expected} expected, {found} found" | The conformance test (AC3) |
| None (pipeline log) | A statement, a constraint or a grant names a schema other than `rwb_access` | The statement and the schema found are named | The boundary test (AC7) |
| None (pipeline log) | A read path has no index, or its plan is a sequential scan | The read path and the plan are named | The plan check (AC10) |

Every error that reaches a caller from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. This story's own failures never reach a caller: they stop the pipeline, and the log line carries the statement, the table or the Field ID. No message of this story carries a personal value, a name or an e-mail address.

### 15. Screens and states

No screen is built in this story, and no screen state is asserted here. The five tables are read by screens and answers that other stories build:

| Screen or answer | State | Where it is |
|---|---|---|
| SCR-10 Approval queue | Loading, list, empty | `rwb-decision` (RWB-P7-E2013-APP); reads the delegation answer of `rwb-access` |
| Authorise answer and session | Allowed, refused | `rwb-access` (RWB-P4-E1037-CON, and the role matrix story RWB-P4-E1019-APP); reads `role`, `permission` and `role_conflict` |
| Role matrix administration | Version in force, loaded, refused | `rwb-access` (RWB-P4-E1019-APP) |
| DoA table load and approval | Loaded, approved, rolled back | `rwb-access` (RWB-P4-E1038-APP) |
| Access log search and export | List over a period | `rwb-access` (the access-log story of the module) |

The gateway-bff composite route of DP-19 exists for those screens (RWB-PLT-N001-CON) and this story serves none of them through it: a schema has no route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-001-11 | AC7, BR1, BR8 | Component | The `rwb_access` login reads `rwb_source_data.sys_fields` and `recovery.v_ace_iam_group` and is refused with insufficient_privilege; the guard library refuses with MSG-P4-002 |
| TC-E1-001-01 | AC1, BR1, BR6 | End to end | Empty DEV and SIT container with `rwb_access` only, no other `rwb_*` schema; the built baseline present and untouched |
| TC-E1-001-02 | AC3, BR2 | Component | The 44-row declaration; the dictionary answer of the `rwb-source-data` contract mock |
| TC-E1-001-03 | AC2, AC11, BR4, BR10 | Component | Keys and constraints of the five tables; a row at `PM-2026.12`, `MASK-SIT-02`, `CONFLICT-2027.01` and `DOA-2027.01` |
| TC-E1-001-04 | AC5, BR5 | End to end | A copy of the migration whose `CREATE TABLE masking_rule` fails |
| TC-E1-001-05 | AC3, BR1 | Component | A branch that adds `role.branch_code`; the declared physical type of DF-REF-201 changed to text |
| TC-E1-001-06 | AC6, BR5 | Component | SIT schema at this story's version, the migration applied twice |
| TC-E1-001-07 | AC10, BR10 | NFR | The SIT policy pack at `PM-2026.11` and `MASK-SIT-01`; the four read paths with EXPLAIN, and each index dropped in turn |
| TC-E1-001-08 | AC9, BR9 | Component | `delegation_limit` after the migration, before any load |
| TC-E1-001-09 | AC8, BR4 | Contract | The `rwb-source-data` contract mock answering the group "RWB-SIT-RW-CASEOWN" and the `account_ext` row of "ACC-000123"; one hop, 2 s timeout |
| TC-E1-001-10 | AC4, BR5 | End to end | The service baseline's version line in SIT; the legacy 1.001 line of the built baseline |
| TC-E1-001-12 | AC1, AC7, BR1, BR7 | End to end | A statement that names `rwb_case`, a foreign key that points at `public`, and a grant to another service's login, each refused by the boundary test |

The 12 legacy TC IDs of the key are kept, one row each, in the legacy order, because the whole set was raised against the one migration this story's slice comes from; the Legacy level System maps to Component or End to end as the row shows, and Access maps to Component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The ITG copy of the set is RWB-ITG-E1001-ITG and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the role codes, capability areas, decision codes, levels, product groups, Field IDs and version labels are rows; the lists are reference data with a version and arrive through DP-07 (BR3, AC11).
- No personal data anywhere: the five tables hold codes, Field IDs, amounts, dates and user references; no test fixture, log line or prompt of this story carries a name, an e-mail address or an identity number (BR8).
- No cross-schema read and no cross-schema key (DP-01): every statement names `rwb_access`, the login holds a grant on `rwb_access` only, and no constraint or index points at `public` or at another service's schema.
- ACE data only through the owner's contract: the service holds no grant on the 30 `recovery.v_ace_*` views, which are `rwb-source-data`'s, and keeps no copy of an ACE table (DP-05, ADR-010; BR7).
- The built baseline is never rewritten: the monolith's `V0001` and its 92 tables keep their version, their names and their rows, and this story adds a new line rather than editing an applied version (BR6).
- The migration changes nothing outside `rwb_access`, creates no grant, never drops a table in PROD and is forward only (DP-15; BR5).
- One writer per table: this story creates the five tables and writes no row, so a migration cannot silently seed a policy (BR11).
- One hop and a 2 s timeout on every call to another service; this story makes none at run time (DP-11).
- The declaration and the dictionary cannot drift: the conformance test compares both directions, so a column added by hand fails the build and a dictionary row without a column fails it too (AC3).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record, one read path and one owner | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-01, FEAT-RDF-02 | All recovery processes | CTL-08; Principle 1; D-RCV-35 U1, U4 | TC-E1-001-01, TC-E1-001-02, TC-E1-001-03, TC-E1-001-05 |
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Epic 2, 4; Program, 5.1 | FEAT-RDF-01 | All recovery processes | REQ-RDF-001; D-RCV-35 U1 | TC-E1-001-03, TC-E1-001-12 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1037-CON | Contract | The service baseline and the authorise contract whose tables this story creates; the baseline states that it delivers the `rwb_access` baseline, which this story's split assignment makes this story's DDL (GAP-0975; ASM-1709) |
| RWB-P4-E1019-APP | App development | Loads the role, permission and conflict rows into the tables this story creates |
| RWB-P4-E1038-APP | App development | Creates and loads the delegation versions in `delegation_limit`; the table is created here, the rows are that story's |
| RWB-P4-E1016-APP | App development | The catalog entries and the masking policy of a data product, read from `masking_rule` |
| RWB-P4-E2013-APP | App development | The delegation lookup that reads `delegation_limit`, `role` and `permission` |
| RWB-P1-E1001-APP | App development | The one catalog and the one dictionary in `rwb_source_data`; this story hands it the 44-row declaration and writes no row of it |
| RWB-PLT-E1044-CON | Contract | H, carried by the service baseline: the per-service Flyway sequence (DP-15) |
| RWB-PLT-E1047-CON | Contract | H, carried by the service baseline: the topic naming library (DP-14) |
| RWB-PLT-N001-CON | Contract | H, carried by the service baseline: the gateway-bff composite route (DP-19) |
| RWB-PLT-NF06-DB | ACE DB | The schema split itself: the 19 `rwb_*` schemas, the logins and the grants; this story is P4's share of it (DP-01) |
| RWB-ITG-E1001-ITG | Integration | The integration harness of the key; no `-ITG` case is written here |

### 19. Out of scope

- The other 87 tables of the 92-table estate and the DB stories that create them in their owners' schemas (RWB-PLT-NF06-DB and the per-service DB stories).
- The built baseline itself: schema `recovery`, its `V0001`, its 92 tables and its dictionary stay as built and are not re-opened (BR6; Template and Rules §R6).
- The 30 read-only ACE views, their grants and the boundary rule (RWB-P1-E1069-APP, RWB-P1-E1069-DB); this service holds no grant on them (DP-05).
- The catalog, the data product rows, the dictionary rows and the dictionary endpoint: RWB-P1-E1001-APP and RWB-P1-E1064-APP. This story declares its 44 rows and writes none.
- `lov_value` and the reference tables: reference data of `rwb-case` (P3) under the ownership ruling, reached through DP-07 (RWB-P3-E1042-CON, RWB-P3-E1043-CON).
- `partner_user`: `rwb-partner`'s (S9); the internal role model is the only role model in this schema.
- The four rule tables and the rule-package registry: `rwb-decision`'s (P7) under the rule-package registry ruling (DP-04 is not in this story's pattern set).
- The row loads: the matrix file (RWB-P4-E1019-APP), the policy pack's masking rows, and delegation version DOA-2026.11 with its 218 rows (RWB-P4-E1038-APP). This story writes no row.
- The REST operations, the events and the screens that read these tables (`POST /authorise`, `GET /me/permissions`, `GET /doa-limits`, `/masking-policies`, `AccessPolicyChanged`, `DoaLimitChanged`, SCR-10 and the administration screens): RWB-P4-E1037-CON, RWB-P4-E2013-APP and the module's screen stories.
- The integration harness RWB-ITG-E1001-ITG and the `-ITG` copies of the test cases.
- The Helm chart, the metrics, the alerts and the runbook of the schema (an OPS story of this key).
