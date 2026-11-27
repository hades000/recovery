# RWB-P7-E1001-APP Recovery tables for the 14 data products

**Version 3 changes.**

- RD-P1-025: Align the dictionary minimums.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-001 is realigned into `rwb-decision`. The built migration `V0001__rwb_e1_001_recovery_schema.sql` and the 92-table estate with its dictionary are kept as built; this story carries P7's share — the six decision-and-rules tables `approval`, `decision_log_entry`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` — into the service's own schema `rwb_decision` (DP-01, DP-15), with their keys, constraints, read indexes and the append-only trigger on `decision_log_entry`. It loads no row, provides no REST operation and publishes no event. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E1001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (27 resolved, 55 cross-document, 7 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E1001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-001 |
| Legacy disposition | Must change |
| Build status | In build |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP11, DP14, DP15, DP19 |
| Parallel lane | L-P7-A |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P7-E1001-APP-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract story | Not applicable (no contract dependency; this story provides no REST operation) |
| Contract version | Not applicable (no contract dependency) |
| Readiness decisions | RD-P1-025 |
| Contract fake library version | Not applicable (no contract dependency) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-RDF-001, REQ-RDF-014) |
| Status | Draft (directive resolutions) |

### 1. Story
As a **centre of excellence analyst (RW-COE) who authors rule packages, a risk and model risk officer (RW-RISK) who approves them, a data product owner (RW-DATASTEW) of DP12 and DP14, and the `rwb-decision` service that keeps the central ledger and the rule registry**, I want **P7's six decision-and-rules tables created in the service's own schema `rwb_decision`, with their keys, constraints, read indexes and the append-only trigger on `decision_log_entry`, on the service's own forward-only Flyway sequence, and no row of any of them loaded**, so that **the decision record, the approval item and the rule package of every service have one home in one schema, no service reads another service's table to reach them, and every later `rwb-decision` story reads one baseline instead of a table it created for itself**.

The legacy story built the estate as one schema, `recovery`, with 92 tables. D-RCV-60 keeps that build and moves the ownership.

- **Kept as built (Template and Rules §R6, "Must change"; U2):** the migration `V0001__rwb_e1_001_recovery_schema.sql`, the 92 tables in schema `recovery`, the `sys_fields` rows and the 14 `data_product` rows are the as-built baseline. This story rewrites none of them, drops none of them, re-opens no legacy parameter and writes no `data_product`, `sys_objects` or `sys_fields` row.
- **The new work is the schema split:** one schema, one login and one Flyway sequence per service, forward only (DP-01, DP-15). P7's share lands in `rwb_decision`; the other 86 tables land with their owners' DB stories. No service reads another service's tables (DP-01); a call goes to the owner's contract, one hop, 2 s timeout (DP-11).
- **The six tables are the decision-and-rules part of the estate,** and the Ownership Map gives all six to P7: `decision_log_entry` (the central ledger), `approval` (an item waiting for approval), `rule_package`, `rule_package_version` (the DMN model registry), `rule_row` (the parsed, queryable rule catalogue) and `rule_test_case` (the test case of the rule-table harness).
- **The rest of the estate is not P7's:** `lov_value` is reference data of `rwb-case` (P3), reached through the reference-data contract (DP-07); `role`, `permission`, `role_conflict`, `masking_rule` and `delegation_limit` are `rwb-access`'s (P4); `partner_user` is `rwb-partner`'s (S9); the four extension tables are `rwb-source-data`'s (P1). None is created, read or referenced here.
- **No rows are loaded here.** The approval items are written by the decision-centre stories, and the rule packages, versions, rows and test cases by the rule-registry stories that load, test and approve a version: a migration that seeded a rule would be a rule change with no author, no test and no four-eyes approval.
- **The dictionary is one dictionary and it is not P7's.** The `sys_fields` and `sys_objects` rows belong to RWB-P1-E1001-APP. This story declares its field rows as a build artefact handed to that one seed and proves them matched by a conformance test; it writes no dictionary row and reads no `rwb_source_data` table at run time (GAP-1279; ASM-2268).
- **Bases and names:** REST base `/api/recovery/decision/v1`, schema and login `rwb_decision`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, shared topic `rwb.decision-record.v1` (DP-13, DP-14). This story provides no REST operation, publishes and consumes no event, starts no workflow, creates no Schedule and serves no screen through the gateway-bff route of DP-19 (RWB-PLT-N001-CON).

### 2. Business rationale
The Workbench keeps its decisions as records and its rules as data. Every decision the Workbench or a person takes — a route, an allocation, a transfer, an approval, an outcome, an access event — is one `decision_log_entry` that cannot be altered, each record hashed to the one before it, so an auditor can ask why a case went where it went and get one answer with the rule, the version and the inputs on it. Every item that waits for a signature is one `approval`, routed to the level the delegation of authority requires. Every Drools package is one `rule_package` with its versions, its workbook reference, its DRL, its checksum, its valid-from date and its approver; its rows are the parsed catalogue a reader queries by rule ID and version; and its test cases are the proof that a version may go live. Legacy RWB-E1-001 created the tables that hold all six, with the dictionary that describes them and the catalog of the 14 data products DP01 to DP14. Every later story of the module reads those six tables, so they are the floor every P7 story stands on.

**What D-RCV-60 changes.** Not the rationale and not the columns: the built migration is the as-built baseline and stays as built. What changes is the ownership boundary inside the same ACE database. The 92 tables were one schema with one login; they are now 19 `rwb_*` schemas, one per service, each with its own login, its own Flyway sequence and its own grants, checked by a test that fails the build on a cross-schema reference (DP-01, DP-15). This story is P7's share of that move: the ledger, the approval item and the rule registry that the other 18 services write through their contracts and read through this service's operations.

**Why these six tables are one slice.** They are the decision and the rule and nothing else. `decision_log_entry` is what every service's decision record is collected into and what the auditor reads; `approval` is the queue item the decision centre routes and the officer signs; the four rule tables are the governed registry, where authoring, testing, four-eyes approval, effective dating and the audit of every version are central in `rwb-decision` while evaluation stays local in the service that owns each model (DP-04). Split away from `rwb_decision`, the append of a record and the load of a version would each be a cross-schema write on a hot path, which DP-01 forbids.

**Why the catalog and the dictionary do not move here.** The dictionary is one dictionary over 14 data products and at least 123 objects, and it stays in `rwb_source_data` with the catalog. A second copy in `rwb_decision` would answer a second way, and a read of `rwb_source_data.sys_fields` from here would be a cross-schema read. This story therefore declares its field rows as a build artefact and proves them matched by a conformance test (GAP-1279; ASM-2268). The columns, physical types, Field IDs, version columns, lists and hash chain are the ones the specifications already fix, no personal value enters this schema, and the measures stay as NFR-033 and NFR-034 state them.

### 3. Preconditions
- RWB-PLT-E1044-CON is in place and the schema `rwb_decision` with its login exists, so Flyway runs in the `rwb-decision` pipeline, takes the schema name from the deployment configuration and migrates only there (DP-15; RWB-PLT-NF06-DB). The legacy parameter and the built `V0001` are the as-built baseline and are not re-opened.
- The other 18 `rwb_*` schemas exist with their own logins, and this login holds no grant on any of them.
- The service baseline of `rwb-decision` is applied: the service template, the decision-record library and shared topic `rwb.decision-record.v1` (RWB-PLT-E1027-CON, DP-03), the naming library (RWB-PLT-E1047-CON, DP-14), the gateway-bff composite route (RWB-PLT-N001-CON, DP-19), and the parameters and reference-data client libraries (RWB-PLT-E1042-CON and RWB-PLT-E1043-CON, DP-06 and DP-07). Those six platform contracts are the service baseline's: the metadata "Depends on (build)" row is None and Ready to start is Day 1, so they are carried here and in GAP-1279 with ASM-3987, not in an H row.
- The DEV and SIT databases of the ACE service exist, with a container database for the migration test that holds `rwb_decision` and no other `rwb_*` schema.
- The dictionary is RWB-P1-E1001-APP's, in `rwb_source_data`; the declaration of this story's field rows is handed to that seed as a build artefact, and no run-time read of `rwb_source_data` is made here (GAP-1279; ASM-2268).
- The built baseline is in force and stays in force: schema `recovery`, 92 tables, its dictionary, its append-only trigger and the 30 `recovery.v_ace_*` views, of which only `rwb-source-data` holds a grant (DP-05).
- The authority data this slice refers to but does not own is P4's: `delegation_limit` lives in `rwb_access`, and an approval names a limit row by value (GAP-2401; ASM-3985).
- The migration file name and its sequence number are fixed at merge under the naming rule of D-RCV-28 (GAP-1279; ASM-2263), and the constraint names and the index columns beyond the leading one are Not specified in the source documents (GAP-1279; ASM-2264).

### 4. Flow
1. Pipeline: applies this story's Flyway file on `rwb-decision`'s own sequence, in DEV first (DP-15).
2. Migration: creates `decision_log_entry` with the 22 business columns DF-DEC-001 to DF-DEC-018 and DF-DEC-028 to DF-DEC-031 of section 11, the 7 standard columns of TSD P7 T3.0, a primary key on `id` and a unique key on `chain_seq`, on `entry_hash` and on `idempotency_key`.
3. Migration: creates `approval` with the 22 business columns DF-DEC-032 to DF-DEC-053, the 7 standard columns and the foreign key from `decision_log_id` to `decision_log_entry.id`.
4. Migration: creates `rule_package` with the 5 business columns DF-REF-274 to DF-REF-278, `package_code` unique, and the 7 standard columns.
5. Migration: creates `rule_package_version` with the 17 business columns DF-REF-279 to DF-REF-295, `version_label` unique, the 7 standard columns and the foreign keys to `rule_package.id` and to itself through `rollback_of`.
6. Migration: creates `rule_row` with the 21 business columns DF-REF-001 to DF-REF-015, DF-REF-052 to DF-REF-054 and DF-REF-296 to DF-REF-298, the 7 standard columns, a unique key on the pair `rule_id` and `rule_version` and the foreign key from `package_version_id` to `rule_package_version.id`.
7. Migration: creates `rule_test_case` with the 13 business columns DF-REF-185 to DF-REF-197, `test_case_id` unique and the 7 standard columns. Physical types and lengths are those of section 11, character for character.
8. Migration: creates the read indexes of the two read paths this schema serves — the decision log by case, decision code and date, and by rule and version; the approval queue by status, level and due date; the registry by package and by version label; the catalogue by `package_version_id` and row order; the test cases by rule and version (section 13).
9. Migration: adds the append-only rule to `decision_log_entry` — the trigger `tr_declog_append_only`, which refuses an UPDATE and a DELETE with "decision_log_entry is append only", and the grant set that withholds UPDATE and DELETE from the service login (BR4).
10. Migration: writes no row of any of the six tables (BR10).
11. Pipeline: runs the conformance test, which compares `information_schema.columns` of the six tables with this story's declaration in both directions, ignoring the 7 standard columns; the boundary test, which reads every statement and fails on any schema name that is not `rwb_decision`; and the index-plan check over the read paths of section 13 with the SIT rule set in place. Then it repeats steps 1 to 11 in SIT.
12. A later story of the service writes rows: the decision-centre stories append `decision_log_entry` rows and route `approval` rows, and the rule-registry stories load `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` rows with their tests and their four-eyes approval (FSD P7 A2.7). This story writes none of them and is complete before any of them runs.

### 5. Exception paths
| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A statement in the migration fails | The transaction rolls back; `rwb_decision` is left with none of the six tables of that migration; the pipeline stage fails with the statement named | None (pipeline log) | AC5 |
| X2 | A business column of the six tables has no declaration row, or a declaration row has no column or a different physical type | The conformance test fails and names the table, the column and the Field ID | None (pipeline log) | AC3 |
| X3 | A statement of the migration, a repository or a test names a schema other than `rwb_decision` | The boundary test fails and names the statement and the schema it found | None (pipeline log) | AC7 |
| X4 | The migration is applied a second time, or it reuses a version the service baseline or the built baseline already holds, including the legacy 1.001 line | Flyway skips the applied version, or the pipeline refuses the reused one; no object and no row changes and the Flyway history is unchanged | None (pipeline log) | AC6 |
| X5 | A login without a grant on `rwb_decision` attempts a read | The read is refused before a row is returned; no data leaves the schema | None (database refusal `insufficient_privilege`) | AC7 |
| X6 | An UPDATE or a DELETE of a `decision_log_entry` row is attempted, through the service login or the schema owner | The statement is refused by the missing grant and by `tr_declog_append_only`; the entry is unchanged and the attempt is audited | decision_log_entry is append only | AC4 |
| X7 | A row is expected in one of the six tables after the migration | There is none: the story writes no row, and a test that expects an approval item or a rule version is the decision-centre or rule-registry story's | None | AC9 |
| X8 | The declaration is not handed to the one seed, or it drifts from the columns | The conformance test fails the build and names the entity, the field and the Field ID; the dictionary is never patched at run time from this service | None (pipeline log) | AC3, AC8 |
| X9 | A new rule version, decision code, approval level, capability area or product group is proposed | It is a row under a new version value and its `valid_from`; no migration, no enum and no check constraint on a list value is needed | None | AC11 |

No exception path of this story changes a case, an approval answer, a rule answer or a decision: this story creates a schema, and the answers the schema serves belong to the stories that read and write it.

### 6. INVEST check
| Test | Result |
|---|---|
| Independent | Needs the per-service Flyway sequence (RWB-PLT-E1044-CON) and the service baseline of `rwb-decision`, both already build dependencies of the service's own stories; every later P7 story reads these six tables |
| Negotiable | The columns and Field IDs are fixed by the specifications; the constraint names, the index names and the file sequence are agreed at merge (section 13) |
| Valuable | Gives the decision ledger, the approval item and the rule registry of the whole Workbench one home, one login and one baseline, and removes the last reason for a service to read another service's table |
| Estimable | One migration, one declaration, one conformance test, one boundary test, one append-only check, one index-plan check; no endpoint, no event, no workflow |
| Small | Fits two weeks or less with its tests, and it unblocks the service's other stories rather than waiting on them |
| Testable | Each criterion below is one automated test, and the read paths have a plan assertion |

### 7. Acceptance criteria
No legacy acceptance criterion is owned verbatim by this story: `acs` is empty for RWB-E1-001, and every legacy criterion of the key tests the monolith's single `recovery` schema, its one `V0001` line, its dictionary seed and its catalog load, which belong to RWB-P1-E1001-APP, RWB-P4-E1001-APP, the per-service DB stories and RWB-PLT-NF06-DB. The thirteen criteria below are new for the `rwb-decision` slice and test only the six tables, their keys, their indexes and their append-only rule; each keeps the legacy values of RWB-E1-001 and adds no business value. The legacy values reused are those of legacy AC4 (a failed statement leaves no partial schema, and the Flyway history holds no successful row for the version), legacy AC5 (the two conformance failure texts) and legacy AC6 (a second run of the same version changes nothing); legacy AC7 to legacy AC11 test the catalog load of `data_product`, which this slice does not perform, so their values appear here only in the statement that no `data_product`, `sys_objects` or `sys_fields` row is written. Where a cross-service answer is needed the Given names the contract mock of its owner, and every legacy value is kept character for character.

```gherkin
Feature: Decision and rules tables in rwb_decision

  Background:
    Given the environment is SIT
    Given the service is rwb-decision, its schema is rwb_decision and its REST base is /api/recovery/decision/v1
    Given the built baseline holds schema recovery with its 92 tables, its dictionary and its append-only trigger on decision_log_entry
    Given the six platform contracts RWB-PLT-E1044-CON, RWB-PLT-NF06-DB, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON and RWB-PLT-N001-CON are the service baseline, and the schema, the rwb-decision login (DP-02) and the Flyway sequence come from them

  Scenario: AC1 The six decision and rules tables exist and nothing else does (new, D-RCV-60)
    Given an empty container database with the schema rwb_decision and the rwb-decision login (DP-02), and no other rwb_* schema
    When the pipeline applies the migration "V<seq>__rwb_p7_e1001_decision_schema.sql" on rwb-decision's own Flyway sequence
    Then rwb_decision holds exactly six tables: approval, decision_log_entry, rule_package, rule_package_version, rule_row and rule_test_case
    Then it holds none of the other 86 tables of the 92-table estate: no recovery_case, no task, no queue, no document, no notice, no lov_value, no role, no permission, no role_conflict, no masking_rule, no delegation_limit, no partner_user and no extension table
    Then it holds no copy of an ACE table: no account, no party, no account_ext and no v_ace_* view, and no table, view, index, trigger or constraint of the migration names schema public or any other rwb_* schema
    Then the six tables carry the field rows of section 11 with their Field IDs and the 7 standard columns of TSD P7 T3.0 on each, and the legacy marker recovery.decision_log_entry is not created, not read and not dropped

  Scenario: AC2 Keys and constraints stay inside rwb_decision (new, D-RCV-60)
    Given the six tables created by AC1's migration
    When the keys and constraints of rwb_decision are read from the catalogue
    Then each of the six tables has a primary key on id and the 7 standard columns are present with the types of TSD P7 T3.0
    Then decision_log_entry holds a unique key on chain_seq, one on entry_hash and one on idempotency_key, rule_package.package_code is unique, rule_package_version.version_label is unique, rule_test_case.test_case_id is unique and rule_row is unique on the pair rule_id and rule_version
    Then approval.decision_log_id holds a foreign key to decision_log_entry.id, rule_package_version.package_id a foreign key to rule_package.id, and decision_log_entry.corrects_entry_id, rule_package_version.rollback_of and rule_row.package_version_id their foreign keys inside rwb_decision
    Then no foreign key points at schema public or at another rwb_* schema, approval.case_id, approval.delegation_limit_id, approval.prepared_by and decision_log_entry.case_id are values with no foreign key, because their owners are rwb_case, rwb_access and the case reference, and the constraint and index names follow the platform naming convention, and each index leads with the read-path column that section 13 names (GAP-1279; ASM-2264)

  Scenario: AC3 The declared field rows are complete and matched (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the dictionary rows of this story's declaration: decision_log_entry with DF-DEC-001 to DF-DEC-018 and DF-DEC-028 to DF-DEC-031, approval with DF-DEC-032 to DF-DEC-053, rule_package with DF-REF-274 to DF-REF-278, rule_package_version with DF-REF-279 to DF-REF-295, rule_row with DF-REF-001 to DF-REF-015, DF-REF-052 to DF-REF-054 and DF-REF-296 to DF-REF-298, and rule_test_case with DF-REF-185 to DF-REF-197
    When the conformance test compares information_schema.columns of rwb_decision with the declaration
    Then it reports every declared business field matched by name and physical type, one for one in both directions, each row naming its entity, its field, its data type, its physical type and its data product, "DP12" for decision_log_entry and approval and "DP14" for the four rule tables
    Then changing the declared physical type of DF-DEC-042 from numeric(18,2) to text fails the test with "DF-DEC-042 physical type numeric expected, text found", and adding the column approval.branch_code with no declaration row fails it with "approval.branch_code has no data dictionary entry"

  Scenario: AC4 The ledger is append only through the trigger and the grant (new, D-RCV-60)
    Given an entry with chain_seq 1 and final call "OWNER_ASSIGNED" is stored for case "RW-2026-000123"
    When an UPDATE setting final_call to "CASE_TRANSFERRED" and a DELETE of the entry are attempted through the rwb-decision login and again through the schema owner role
    Then all four statements are refused: by the missing grant for the service login, and with "decision_log_entry is append only" from tr_declog_append_only for the schema owner, and the entry is unchanged and the refused attempts are written to the ACE audit log with the table, the operation and the entry ID
    When a correction of the entry is taken
    Then a new entry is appended with corrects_entry_id naming the entry it corrects, and the corrected entry is still unchanged

  Scenario: AC5 A failed statement leaves none of the six tables (new, D-RCV-60)
    Given a copy of the migration in which the statement creating table rule_package_version fails
    When the pipeline applies it in DEV
    Then the pipeline stage fails and names the failing statement
    Then rwb_decision holds none of the six tables of that migration, and decision_log_entry and rule_package are absent with the rest, and the Flyway history of rwb_decision has no successful row for that version

  Scenario: AC6 A second run of the same version changes nothing (new, D-RCV-60)
    Given this story's migration applied in SIT
    When the pipeline runs again in SIT
    Then Flyway reports the version as already applied and applies no statement
    Then rwb_decision still holds six tables, their columns, their foreign keys, their indexes and the trigger tr_declog_append_only, the six tables still hold no row, and the built baseline's version 1.001 and its 92 tables are unchanged

  Scenario: AC7 No table of another service and no ACE table is read (new, D-RCV-60)
    Given the login rwb_decision holds grants on schema rwb_decision only
    When the build runs the boundary check over the migration, the repositories of the service and the pipeline tests
    Then every statement names rwb_decision, and no statement names rwb_source_data, rwb_case, rwb_access or any other rwb_* schema
    Then a direct SELECT on rwb_source_data.sys_fields through the login rwb_decision is refused with insufficient_privilege
    Then a SELECT on recovery.v_ace_account through the login rwb_decision is refused with insufficient_privilege, because the 30 recovery.v_ace_* views are granted to rwb-source-data only, and no repository of the service issues a statement against decision_log_entry of schema recovery

  Scenario: AC8 The dictionary is declared as a build artefact and handed to rwb_source_data (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the dictionary rows of the declaration, with entity decision_log_entry, field final_call and data product "DP12"
    Given the rwb-case contract mock returns LOV-DECISION with the value "D6" and LOV-APPROVAL-LEVEL with the value "L6" at the version in force
    When the declaration is handed to the one dictionary's seed of RWB-P1-E1001-APP
    Then the handover carries every entity, field, Field ID, data type, physical type and data product of section 11 and no row of its own, and the migration writes no sys_fields row, no sys_objects row and no data_product row
    Then no run-time path of the service reads rwb_source_data, the two lists are read through the reference-data contract of DP-07 in one hop with a 2 s timeout, and no list value of LOV-DECISION or LOV-APPROVAL-LEVEL is written as a check constraint, an enum or a constant in rwb_decision

  Scenario: AC9 The six tables are created empty (new, D-RCV-60)
    Given this story's migration applied in SIT
    When each of the six tables is counted
    Then each holds 0 rows and its business columns and its 7 standard columns are present, and the migration inserted no baseline rule, no approval item, no decision entry and no test case
    Then at least 123 sys_objects rows, at least 1,379 sys_fields rows and the 14 data_product rows stay the built baseline's and RWB-P1-E1001-APP's, and the 24 legacy placeholder rows of delegation_limit are not seeded here, because that table is rwb-access's

  Scenario: AC10 The indexes serve the decision-log and registry reads (new, D-RCV-60)
    Given the six tables hold the decision entries and the rule versions of a SIT day, with version "ALLOC-2026.12" in force
    When the read paths of the service run with EXPLAIN: the decision entries of a case and a decision code in decidedAt order, the entries of a rule and a version, the approval items of a status and a level by due date, the version of a package by its version label, the rows of a package version by row order, and the test cases of a rule and a version
    Then each plan uses an index whose leading column is the one section 13 names for that path, and no plan is a sequential scan of decision_log_entry or of rule_row
    Then dropping the index of the decision-log case path makes the plan check fail, so the check cannot pass by accident

  Scenario: AC11 A new rule version and a new decision code are rows and not a build (new, D-RCV-60)
    Given the six tables created by AC1's migration
    When a rule version "ALLOC-2026.13" with 26 rows and 50 test cases is loaded and approved, and a new decision code and a new capability area are added to their lists
    Then the version is carried by rule_package_version.version_label, its valid_from and its status, and its rows by rule_row.rule_version and rule_package_version_id
    Then no Java enum, no constant and no check constraint on a list value is needed for the version, the decision code or the capability area, and no migration of this story changes and the declared field rows are unchanged

  Scenario: AC12 No list value and no personal data is written into rwb_decision (new, D-RCV-60)
    Given the six tables created by AC1's migration
    When the boundary check reads every column, check constraint, enum and constant of rwb_decision, and every fixture and log line of the tests
    Then no column, check constraint or constant of rwb_decision holds a list value of LOV-DECISION, LOV-APPROVAL-LEVEL or any other list of BR12, and no fixture or log line carries a name, an e-mail address or an identity number

  Scenario: AC13 The story provides no REST answer, so it writes no 401, 403 or 404 (new, D-RCV-60)
    Given the service is rwb-decision, its REST base is /api/recovery/decision/v1 and this story provides no REST operation
    When the build lists the routes of the service at this story's version
    Then no route of this story exists, so this story writes no answer with status 401, 403 or 404 for a provided operation, and those answers belong to the stories that provide the operations
```

### 8. Business rules
| ID | Rule | Source |
|---|---|---|
| BR1 | `rwb_decision` holds P7's six decision-and-rules tables and no other table of the estate; every table, key, index, trigger and constraint names `rwb_decision` only | DP-01; Ownership Map |
| BR2 | Every business column of the six tables has exactly one dictionary row with its Field ID, data type, physical type and data product, and no column exists without one | LDM and Data Dictionary; TSD P7 T3.1; RWB-P1-E1001-APP |
| BR3 | Every list of values is reference data read through the reference-data contract of `rwb-case` with the version in force; no list value is a column, a check constraint or a constant in `rwb_decision` | DP-07; R5 default ruling; BR-P7-001; AC11 |
| BR4 | The decision log is append only and hash chained: an entry is never updated and never deleted, the trigger `tr_declog_append_only` and the missing grant refuse both, a correction is a new entry naming the one it corrects in `corrects_entry_id`, and `chain_seq`, `prev_hash` and `entry_hash` carry the chain | FSD P7 AC-P7-001-01 and A2.1; REQ-DRI-002; REQ-DRI-003 |
| BR5 | A key by value stays a key by value: the five foreign keys of `rwb_decision` stay inside it, and a case reference, a delegation limit, a user reference and a package of another schema are values | TSD P7 T3.3; DP-01 (GAP-2401; ASM-3985) |
| BR6 | Schema names come from configuration; one migration per story; forward only in PROD; never drop a table in PROD | RWB-E1-044; D-RCV-28; DP-15 |
| BR7 | The built baseline is kept as built: the monolith's `V0001`, its 92 tables, its dictionary and its 14 data product rows are not rewritten, dropped or re-opened by this story | Template and Rules §R6 "Must change"; U2 |
| BR8 | ACE data is reached only through the contract of its owner: this service holds no grant on the 30 `recovery.v_ace_*` views and no copy of any ACE table | DP-05; ADR-010; D-RCV-35 U4 |
| BR9 | No personal data in the schema and in its tests: the six tables hold codes, references, versions, amounts and dates, a rule test case holds synthetic facts, and no fixture or log line carries a name, an e-mail address or an identity number | NFR-039; NFR-040; legacy §17 |
| BR10 | The six tables are created empty; the entries, approval items, rule packages, versions, rows and test cases are written by the service's own later stories, so a migration can never seed a rule or a decision | Ownership Map; FSD P7 A2.2 and A2.7 |
| BR11 | A rule version is data with a state and a date: `status` carries LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK or REFUSED, `valid_from` and `valid_to` carry the window, and the author and the approver are two different references | Temporal and Drools Design slide 15 (T4); LDM |
| BR12 | The decision code, the final call, the approval level, the product group, the capability area and the route set are data rows read at the version in force, never literals of this schema | FSD P7 BR-P7-001; TSD P7 T3.2 |
| BR13 | The declaration, the columns and the one dictionary cannot drift: the conformance test compares both directions, so a column added by hand fails the build and a dictionary row without a column fails it too | RWB-P1-E1001-APP; legacy AC5 (GAP-1279; ASM-2268) |

Where each rule lives in the target: BR1 is the migration and the boundary test, and it is the rule that turns one schema into 19. BR2 and BR13 are the declaration and the conformance test; the dictionary rows themselves stay in `rwb_source_data`, because one dictionary over 14 data products cannot be split (GAP-1279). BR3 is the absence of `lov_value` from `rwb_decision`: a new decision code or capability area is a row of a list and not a change here (AC11). BR4 is the trigger, the grant and the three chain columns. BR5 keeps the five foreign keys inside the schema and turns the cross-schema references of TSD P7 T3.3 into values (GAP-2401). BR6 is the per-service sequence and the file naming. BR7 is the boundary between this story and the built baseline. BR8 is the grant test of AC7. BR9 is the reason the schema is safe to log. BR10 is the empty tables of AC9. BR11 is the version row of AC11. BR12 is the reason no list value is a check constraint.

### 9. State transitions
This story changes no case, approval, rule or decision state and answers no request. It changes the Flyway version of `rwb_decision` and nothing else. It serves no screen, so the empty, loading, error and no-access states of SCR-10, SCR-11 and SCR-38 are not carried here. Open decision DL10 is still open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 hold until it closes.

| From | To | Trigger |
|---|---|---|
| `rwb_decision` at the service baseline, without P7's decision-and-rules tables | `rwb_decision` at the version this story applies: six tables, their foreign keys, their indexes, the trigger `tr_declog_append_only`, no row | The pipeline applies the migration in DEV, then in SIT |
| The version applied | The version applied, no change | The same file runs again; Flyway skips it and no object changes (AC6) |
| `rule_package_version` absent, then in force | A version in state LOADED, then APPROVED, then IN_FORCE; later SUPERSEDED, ROLLED_BACK, or REFUSED at load | The rule-registry stories: the load, the tests, the four-eyes approval and the promote Schedule; not this story (BR11) |
| `approval` absent | An item in state WAITING, then APPROVED, REFUSED, RETURNED or HELD_NO_LIMIT | The decision-centre and approval stories of this service; not this story |
| `decision_log_entry` absent | Appended entries in `chain_seq` order | The append path of DP-03, in the decision-centre stories and in the ingest of `rwb.decision-record.v1`; not this story (BR4) |
| An appended entry | The same entry, unchanged | Never: an UPDATE and a DELETE are refused by the grant and by `tr_declog_append_only` (AC4) |
| The built baseline at version 1.001 | The built baseline at version 1.001, unchanged | Never: this story does not touch the monolith line (BR7) |

The rows of the six tables move under their own version columns, states and windows; the schema's version moves only on a migration.

### 10. Authority
| Who | What they may do in this story |
|---|---|
| Pipeline service identity (`rwb-decision` pipeline) | Runs the migration, the conformance test, the boundary test and the plan check in DEV and SIT, in `rwb_decision` only |
| ACE team (suggested; any team may pick up this story) | Reviews the DDL, the keys, the constraints, the trigger and the grants, and creates the schema and the login with RWB-PLT-NF06-DB |
| RW-COE, center of excellence analyst | Owns the shape of the rule registry as its authoring role and reviews that the package, version, row and test-case columns answer the load and approval path of FSD P7 A2.7; writes no row and changes no DDL in this story |
| RW-RISK, risk and model risk officer | Reviews that the version carries its author, its approver, its checksum, its test result and its valid-from date, because the four-eyes approval is decided against them; writes no row here |
| RW-DATASTEW, data steward and data product owner | Owns DP12 and DP14 and confirms that the six tables belong to those products; writes no row and holds no DDL right in PROD outside the pipeline |
| RW-AUDIT, internal audit; RW-PLATADM, platform administrator | RW-AUDIT reads the declaration, the migration and the append-only rule to verify that every decision has one home, and RW-PLATADM owns the schema, the login and the grants through RWB-PLT-NF06-DB; neither writes a row and neither changes a table of this story |
| The other services' logins | Hold no grant on `rwb_decision`: a table read is refused with insufficient_privilege, and the supported path is this service's contract |
| `rwb-decision` itself | Reads and writes its own six tables in the later stories of the service; in this story it creates them and writes no row (BR10) |

No approval level from the delegation of authority applies to this story: it creates a schema and approves no limit and no rule version. This story provides no REST operation, so it calls no rwb-access authorise check (DP-08); the roles above bind the pipeline and the reviews, and the service's own stories carry the check for their operations. Every "who" here is a role code; the roles, their permissions and the delegation rows are held as data in `rwb-access`, and the approver of a rule version is a user reference in `rule_package_version.approver`.

### 11. Data
| # | Table in `rwb_decision` | BR Field IDs | Business fields | Read or write in this story |
|---:|---|---|---:|---|
| 1 | `decision_log_entry` | DF-DEC-001 to DF-DEC-018, DF-DEC-028 to DF-DEC-031 | 22 | Create (table only) with the unique keys on `chain_seq`, `entry_hash` and `idempotency_key` and the append-only trigger; read |
| 2 | `approval` | DF-DEC-032 to DF-DEC-053 | 22 | Create (table only) with the foreign key to `decision_log_entry.id`; read |
| 3 | `rule_package` | DF-REF-274 to DF-REF-278 | 5 | Create (table only) with `package_code` unique; read |
| 4 | `rule_package_version` | DF-REF-279 to DF-REF-295 | 17 | Create (table only) with the foreign keys to `rule_package.id` and to itself; read |
| 5 | `rule_row` | DF-REF-001 to DF-REF-015, DF-REF-052 to DF-REF-054, DF-REF-296 to DF-REF-298 | the field rows the LDM lists | Create (table only) with the unique key on `rule_id` and `rule_version` and the foreign key to `rule_package_version.id`; read |
| 6 | `rule_test_case` | DF-REF-185 to DF-REF-197 | 13 | Create (table only) with `test_case_id` unique; read |

The six tables carry the business fields above and the 7 standard columns of TSD P7 T3.0 on each: `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at` and `updated_by`. The exact Field IDs of the standard columns are Not specified in the source documents (GAP-1279; ASM-3986): they are carried by the one dictionary's seed, and the business Field IDs above are the ones this story declares and cites. Field IDs, physical types and lengths are those of TSD P7 T3.1 for `decision_log_entry` and `approval` and of the LDM fields sheet for the four rule tables, character for character; the entity sheet's count for `rule_row` and its relationships sheet's `package_version_id` disagree with its fields sheet, which is why the fifth row names its ranges and no total (GAP-2401; ASM-2269; ASM-3988).

**What is not in the schema.** `lov_value`, `reference_row`, `reference_version` and the parameter tables are reference data of `rwb-case` (P3) and are reached through DP-07; `role`, `permission`, `role_conflict`, `masking_rule` and `delegation_limit` are `rwb-access`'s (P4); `partner_user` is `rwb-partner`'s (S9); `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and the four extension tables are `rwb-source-data`'s (P1); `recovery_case`, `task` and `queue` are `rwb-case`'s (P3); `template` and `merge_field` are `rwb-comms`'s (P6); `document` and its tables are `rwb-document`'s (P5). None of them is created, read or referenced here. The service owns no collection and no view: `v_data_dictionary` is RWB-P1-E1001-APP's answer, never a table of this schema.

**Rows.** No row of any of the six tables is written by this story. The decision entries are written by the append path of DP-03, the approval items by the approval stories, and the rule packages, versions, rows and test cases by the rule-registry stories with their tests and their four-eyes approval (FSD P7 A2.7; BR10). The 24 legacy placeholder rows of `delegation_limit` are not seeded here, and neither are at least 123 `sys_objects` rows, at least 1,379 `sys_fields` rows or the 14 `data_product` rows, which stay the built baseline's and RWB-P1-E1001-APP's.

**Names that are not fields.** `tr_declog_append_only`, `insufficient_privilege` and `v_data_dictionary` are a trigger, a database refusal and a read model; none is a field or entity of the LDM or the Data Classification, so none carries a Field ID and none is declared in the table above. The ACE views named in AC7 are refusal targets only: the criterion asserts that they are refused and reads no row from them, and any dictionary answer comes from the contract fake.

### 12. Contract
#### 12.1 REST operations provided
| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| Not applicable | Not applicable | This story provides no REST operation. The operations of the schema — API-P7-001 to API-P7-008: `GET /api/recovery/decision/v1/decision-log`, `GET /api/recovery/decision/v1/decision-log/{entryId}`, `GET /api/recovery/decision/v1/approvals`, `GET /api/recovery/decision/v1/approvals/{approvalId}`, `POST /api/recovery/decision/v1/approvals/{approvalId}/approve`, `/return`, `/refuse` and `GET /api/recovery/decision/v1/cases/{caseId}/recommendation` — are the service's own later and contract stories' | None | None |

#### 12.2 REST operations consumed
| Method | Path | Owner | Use in this story |
|---|---|---|---|
| None | None | None | This story calls no REST operation at run time. The reference lists and the parameters it names are read by the later stories through DP-07 and DP-06 with a 2 s timeout, and nothing in the migration reaches another service |

#### 12.3 Events published
| Event | Topic | Owner | Trigger |
|---|---|---|---|
| None | `rwb.decision.events.v1` | P7 `rwb-decision` | This story publishes no event. The topic with the events `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` (events EV-08, EV-09 and EV-30) and the shared topic `rwb.decision-record.v1` are named by DP-14 and resolved by the naming library; the events are published by the stories that change an approval or promote a rule version, and a schema migration publishes nothing |

#### 12.4 Events consumed
| Event | Topic | Owner | Handler |
|---|---|---|---|
| None | None | None | This story consumes no event and registers no consumer. `DecisionRecorded` on `rwb.decision-record.v1` is consumed by the ledger ingest of the service's decision-centre stories, and no event starts a migration |

#### 12.5 Workflows and activities
| Workflow or activity | Queue | Purpose |
|---|---|---|
| None | `rwb-decision` | This story registers no workflow and no activity on task queue `rwb-decision` in namespace `rwb-recovery`. The approval workflow of the kit template and the schedules of the service are its own later stories' |

#### 12.6 Schedules
| Schedule | Queue | When | Purpose |
|---|---|---|---|
| None | `rwb-decision` | None | This story creates and changes no Temporal Schedule: the migration runs on a deployment, not on a clock. The rule promote Schedule JOB-20 at 00:01 and the hash-chain check JOB-14 at 02:00 are the service's later stories' and the decision-log baseline's (jobs JOB-13, JOB-14 and JOB-20 are named by the service row) |

#### 12.7 Tables owned
| Table | Schema | Owner (Ownership Map) | This story |
|---|---|---|---|
| `decision_log_entry` | `rwb_decision` | P7 | Creates with its unique keys on `chain_seq`, `entry_hash` and `idempotency_key`, the append-only trigger `tr_declog_append_only`, the missing UPDATE and DELETE grant and its read indexes; no row |
| `approval` | `rwb_decision` | P7 | Creates with its foreign key to `decision_log_entry.id` and its queue read index; no row |
| `rule_package` | `rwb_decision` | P7 | Creates with `package_code` unique and its registry read index; no row |
| `rule_package_version` | `rwb_decision` | P7 | Creates with `version_label` unique, its two foreign keys and its registry read index; no row |
| `rule_row` | `rwb_decision` | P7 | Creates with its unique key on `rule_id` and `rule_version`, its foreign key to `rule_package_version.id` and its catalogue read index; no row |
| `rule_test_case` | `rwb_decision` | P7 | Creates with `test_case_id` unique and its test read index; no row |
| `sys_objects`, `sys_fields`, `sys_field_version`, `data_product`; `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | `rwb_source_data`; `rwb_case` | P1; P3 | **Never read and never written.** The dictionary and the catalog are RWB-P1-E1001-APP's and this story declares its field rows as a build artefact; the lists and parameters arrive through DP-07 and DP-06 |
| `role`, `permission`, `role_conflict`, `masking_rule`, `delegation_limit`; `partner_user`; `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | `rwb_access`; `rwb_partner`; `rwb_source_data` | P4; S9; P1 | **Never read.** `approval.delegation_limit_id` is a value, not a foreign key |
| `recovery_case`, `task`, `queue`, `case_party` | `rwb_case` | P3 | **Never read and never written.** `approval.case_id` and `decision_log_entry.case_id` are values |
| the other tables of the 92-table estate | their owners' schemas | the 18 other services | **Never read.** No grant, no join, no constraint, no view (DP-01) |

The 19 service schemas of the estate are never read by `rwb-decision`, and `rwb-decision` writes nothing outside `rwb_decision`. The database login is the service's own, with grants on `rwb_decision` and on no other schema and no grant on the 30 `recovery.v_ace_*` views, which are `rwb-source-data`'s (DP-01, DP-05). The six-table list, the constraint set, the sequence assignment, the cross-schema references and the `rule_row` field count are recorded in GAP-1279 and GAP-2401 with ASM-2262 to ASM-3988.

#### 12.8 Contract fakes
| Fake | Serves | Used for |
|---|---|---|
| rwb-source-data contract fake | DP-05 (no H and no C dependency: the contract is `rwb-source-data`'s) | The dictionary rows of the declaration in AC3 and AC8, and the refusal of a direct read in AC7 |
| rwb-case contract fake | DP-07 and DP-06 (no H on this story: the contract is `rwb-case`'s) | LOV-DECISION with the value "D6" and LOV-APPROVAL-LEVEL with the value "L6" at the version in force in AC8 |
| Flyway sequence fake (RWB-PLT-E1044-CON, the service baseline) | The per-service Flyway sequence of DP-15 | The apply, the rollback and the skip of AC5, AC6 and the version line |
| schema and login fixture (RWB-PLT-NF06-DB) and the naming library fake (RWB-PLT-E1047-CON, the service baseline) | The 19 `rwb_*` schemas with the one login each, and the topic and event naming library of DP-14 | AC7's grant test, where `rwb_decision` holds a grant on its own schema only; the topic and event names are resolved, never typed, so no test asserts a literal |

Each fake is replaced by the real service as its own story lands, without a change to the scenarios.

#### 12.9 Call-type summary
| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0, consumed 0 | The base `/api/recovery/decision/v1` is named; no operation is added and none is called |
| Kafka | Published 0, consumed 0 | Topic `rwb.decision.events.v1` and shared topic `rwb.decision-record.v1` are named for DP-14; this story produces and consumes nothing on them |
| Temporal | 0 workflows, 0 activities, 0 schedules | Queue `rwb-decision` in namespace `rwb-recovery` is not used |
| File | 1 build-time, 0 at run time | The dictionary field declaration of section 11, read by the conformance test and handed to the one dictionary's seed |

### 13. Solution plan
**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `decision/schema`. Service base `/api/recovery/decision/v1`, schema and login `rwb_decision`, topic `rwb.decision.events.v1`, shared topic `rwb.decision-record.v1`, task queue `rwb-decision` in namespace `rwb-recovery`. The migration sits on the service's own Flyway sequence, in `rwb-decision`'s pipeline (DP-15).

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

The legacy marker this slice replaces is one schema with one login and one `V0001` baseline (DP-01 and DP-15): the split is the new work, and it is the change §R6 records. The monolith names — `recovery.decision_log_entry`, `recovery.approval`, `recovery.rule_package`, `recovery.rule_package_version`, `recovery.rule_row` and `recovery.rule_test_case` — are legacy marker text only: they are the as-built objects, they stay as built, and they are not the target and not a read path. DP-03, DP-05, DP-06, DP-07, DP-11, DP-14 and DP-19 are carried by the legacy key and their work on the runtime path sits with the stories that read or change the tables: the record is appended by the decision-centre and record-ingest stories (DP-03), the ACE data is read through `rwb-source-data` (DP-05), the lists and parameters arrive through their contracts (DP-06, DP-07) in one hop with a 2 s timeout (DP-11), the topic names are resolved by the library (DP-14) and the screens come through the gateway-bff route (DP-19). This story creates a schema, so none of them adds a call of its own.

This secondary slice adds no new build dependency (metadata "Depends on (build)" is None): the platform libraries, the Flyway baseline, the naming library, the decision-record library and the edge route are already build dependencies of the P7 service's own stories, and this story builds against the service baseline's published contracts and their fakes; the dependency column above is the DP table's canonical row, not a new H edge (GAP-1279; ASM-3987).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<seq>__rwb_p7_e1001_decision_schema.sql` | Flyway migration | Creates the six tables with their keys, constraints, indexes, the 7 standard columns and the trigger `tr_declog_append_only`; writes no row; creates no view and no grant to another login |
| `DecisionFieldDeclaration` | Build artefact and test fixture | The field-row declaration of the six tables, with entity, field, Field ID, data type, physical type and data product; the source the conformance test compares against and hands to the one dictionary's seed |
| `DecisionDictionaryConformanceTest` | Test (pipeline) | Compares `information_schema.columns` of `rwb_decision` with the declaration in both directions, ignoring the 7 standard columns |
| `DecisionSchemaBoundaryTest` | Test (pipeline) | Fails on a schema name other than `rwb_decision`, on a grant to another login and on a foreign key that leaves the schema |
| `DecisionAppendOnlyTest` | Test (pipeline and component) | Asserts the four refusals of AC4 and that the correction path appends a new entry |
| `DecisionIndexPlanTest` | Test (pipeline) | Asserts the read paths' plans against the SIT rule set, and fails when an index of a read path is dropped |
| `DecisionGrantFixture` | Test fixture | The `rwb_decision` login with grants on its own schema only, used by the refusal assertions of AC7 |

**Database and migrations**

- Creates the six tables of section 11 in `rwb_decision` and nothing else: no `lov_value`, no `role` or `delegation_limit`, no `partner_user`, no extension table, no case, document, notice, payment, treatment or reporting table, and no lake watermark (DP-17 is not this story's). The migration is one transaction: a failing statement leaves none of the six tables (AC5), and a second run is a skip (AC6).
- The five foreign keys stay inside `rwb_decision`: `approval.decision_log_id`, `decision_log_entry.corrects_entry_id`, `rule_package_version.package_id`, `rule_package_version.rollback_of` and `rule_row.package_version_id`. `approval.case_id`, `approval.delegation_limit_id`, `approval.prepared_by` and `decision_log_entry.case_id` are values with no foreign key, as the estate's links to an ACE record are business keys with no foreign key (BR5; GAP-2401; ASM-3985).
- No constraint, index or default names schema `public` or another `rwb_*` schema, and the service login holds no UPDATE and no DELETE grant on `decision_log_entry`, so the trigger and the grant both refuse (BR4, BR8).
- The other schemas named in this section, `rwb_source_data` and `recovery`, are named only as the targets of the refusals of AC7 and of the dictionary handover of build step 5; each belongs to its own service (`rwb-source-data`, P1; the built baseline), and this story holds no right on either.
- Indexes, in the order the read paths need them: `decision_log_entry (case_id, decision_code, decided_at DESC)`; `decision_log_entry (rule_id, rule_version)`; `approval (status, approval_level, due_at)`; `rule_package_version (package_id, valid_from DESC)`; `rule_package_version (version_label)`; `rule_row (package_version_id, row_order)`; `rule_row (rule_id, rule_version)`; `rule_test_case (rule_version, rule_id)`. Their names follow the platform naming convention; the names and the column order beyond the leading column are Not specified in the source documents (GAP-1279; ASM-2264). The migration writes no row (BR10, AC9).

**Migrations in order** (the service's own sequence, forward only). 1. The service baseline: the schema, the login and the service template's standard columns (RWB-PLT-NF06-DB; the decision-record library RWB-PLT-E1027-CON), already applied. 2. This story: `V<seq>__rwb_p7_e1001_decision_schema.sql`, the six tables, their keys, constraints, indexes and the append-only trigger, and nothing else. 3. After it, the service's own stories: the decision-centre and approval stories that write entries and approval items, and the rule-registry stories that load, test, approve and promote rule versions; this story neither creates nor depends on them.

**Configuration and reference data.** The schema name of the service's own schema comes from the deployment configuration of `rwb-decision` (RWB-PLT-E1044-CON); the legacy parameter stays the as-built value of the baseline and is not read by this story. Every list the columns are checked against — LOV-DECISION, LOV-APPROVAL-LEVEL, LOV-APPROVAL-STATUS, LOV-CAPABILITY, LOV-PRODUCT, LOV-ROLE, LOV-ROUTE-SET and LOV-TEST-RESULT — is read through the reference-data contract of `rwb-case` with the version in force (DP-07), never stored as a check constraint or a Java enum, which is why a new decision code, approval level, capability area or rule version needs no migration (AC11). The six states of `rule_package_version.status` are LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED (BR11). No value the business may change is written in this story's code or in its migration.

**Build steps**

1. Write `V<seq>__rwb_p7_e1001_decision_schema.sql` from TSD P7 T3.1 and the LDM fields sheet, with the schema taken from configuration; run it on an empty PostgreSQL container that holds `rwb_decision` and no other `rwb_*` schema, and prove it creates exactly six tables and their indexes (AC1, AC2).
2. Write `DecisionFieldDeclaration` and `DecisionDictionaryConformanceTest`; prove the test fails on an extra column and on a changed physical type (AC3), then `DecisionAppendOnlyTest` for the four refusals, the audit line and the correction entry (AC4).
3. Prove the rollback and the skip: a copy that fails on `rule_package_version` leaves none of the six tables and no successful version (AC5); a second run changes nothing (AC6).
4. Prove the boundary: the migration names `rwb_decision` only, creates no view and no grant, and a direct read of `rwb_source_data.sys_fields` and of `recovery.v_ace_account` through the service login is refused (AC7).
5. Hand the declaration to the one dictionary's seed (RWB-P1-E1001-APP) as a build artefact and record the handover in the change register, writing no row of `rwb_source_data` (AC8; GAP-1279); prove no row is written (AC9); write `DecisionIndexPlanTest` over the read paths with the SIT rule set and prove it fails when an index is dropped (AC10); and prove that a new version label, decision code and capability area need no build (AC11).

**Feature switch.** None of this story's own. A migration is not behind a flag: the six tables either exist at the version or the pipeline has not applied it (BR6, BR7). The service-level flag of the decision centre belongs to the service's own stories, and the rule evaluation switch belongs to the embedded Drools kit of the owning service (DP-04).

**Done when.** The tests in section 16 pass; the migration runs clean in DEV and SIT on `rwb-decision`'s own sequence; `rwb_decision` holds exactly the six tables with their keys, their five foreign keys, their read indexes and the append-only trigger; the conformance test reports every declared field row matched; the boundary test reports no statement, no constraint and no grant outside `rwb_decision`; and the read paths use their indexes.

### 14. Validation and messages
| ID | When | Message | Where it is produced |
|---|---|---|---|
| decision_log_entry is append only | An UPDATE or a DELETE of an entry is attempted | decision_log_entry is append only | The trigger `tr_declog_append_only` (AC4) |
| MSG-P7-003 | The central ledger cannot be written while a producing service appends its record | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The record path of the producing service; this story makes the store answer and produces no message of its own |
| None (pipeline log) | A migration statement fails, a column has no declaration row, a row has no column or a different physical type, a statement or grant names another schema, or a read path has no index | The stage fails and names the statement and its line, "{table}.{column} has no data dictionary entry", "{fieldId} physical type {expected} expected, {found} found", the schema found, or the read path and its plan | The pipeline, the conformance test, the boundary test and the plan check (AC3, AC5, AC7, AC10) |
| insufficient_privilege | A login without a grant on `rwb_decision`, or a read of `rwb_source_data` or of a `recovery.v_ace_*` view through this login, is attempted | The database's own refusal | PostgreSQL, asserted by AC7 |

Every error that reaches a caller from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request; the IDs those responses carry are the service's own later stories', because this story provides no operation. This story's own failures never reach a caller: they stop the pipeline, and the log line carries the statement, the table or the Field ID. No message of this story carries a personal value, a name or an e-mail address, and Thai text for each message of the service follows decision DL10 in the story that raises it.

### 15. Screens and states
No screen is built in this story, and no screen state is asserted here. The six tables are read by screens and answers that other stories build:

| Screen or answer | State | Where it is |
|---|---|---|
| SCR-10 Approval queue | Loading, list; empty, error and no access: Not specified in the source documents (CG-ALL-6818) | `rwb-decision` (the service's approval and queue stories); reads `approval`, `decision_log_entry` and the delegation answer of `rwb-access` |
| SCR-11 Decision screen and the recommendation read | One recommendation, refused; empty, loading, error and no access: Not specified in the source documents (CG-ALL-6819) | `rwb-decision` (the decision-centre stories); reads `decision_log_entry` and `approval` |
| SCR-38 Decision log query | Loading, list, one entry; empty, error and no access: Not specified in the source documents (CG-ALL-6820) | `rwb-decision` (the decision-log read story); reads `decision_log_entry` through `GET /api/recovery/decision/v1/decision-log` |
| Rule administration, the version in force, and the rule model load in an owning service | Loaded, tested, approved, in force, refused, rolled back; and on the service side loaded, checksum verified, last good model kept | `rwb-decision` (the rule-registry stories) for the four rule tables; the owning service's story reads the version and its rows through this service's rule-model contract, never as a table |

The gateway-bff composite route of DP-19 exists for those screens (RWB-PLT-N001-CON) and this story serves none of them through it: a schema has no route. The field list of each screen, its panel ids and its layout are Not specified in the source documents for this slice (GAP-1279; ASM-2262) and belong to the stories that build them.

### 16. Test cases
| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-001-11 | AC7, BR1, BR8; legacy Covers "Access" | Component | The direct reads of `rwb_source_data.sys_fields` and `recovery.v_ace_account` through the login `rwb_decision` are refused with insufficient_privilege; any dictionary answer comes from the `rwb-source-data` contract fake (§12.8), never from an ACE view |
| TC-E1-001-01 | AC1, AC2, BR1, BR7 | End to end | Empty DEV and SIT container with `rwb_decision` only, no other `rwb_*` schema; the built baseline present and untouched |
| TC-E1-001-02 | AC2, BR2 | Component | The field-row declaration of 9 field rows, proven matched to the dictionary seed by the conformance test; the dictionary answer of the `rwb-source-data` contract mock |
| TC-E1-001-03 | AC3, BR5, BR11 | Component | Keys and constraints of the six tables; a rule version "ALLOC-2026.13" with 26 rows and 50 test cases, a new decision code and a new capability area |
| TC-E1-001-04 | AC4, BR6 | End to end | A copy of the migration whose `CREATE TABLE rule_package_version` fails |
| TC-E1-001-05 | AC5, BR13 | Component | A branch that adds `approval.branch_code`; the declared physical type of DF-DEC-042 changed to text |
| TC-E1-001-06 | AC6, BR6 | Component | SIT schema at this story's version, the migration applied twice; the built baseline at version 1.001 |
| TC-E1-001-07 | AC7, BR4 | NFR | The SIT decision entries and rule versions of one day; the read paths with EXPLAIN, and each index dropped in turn |
| TC-E1-001-08 | AC9, BR10 | Component | The six tables after the migration, before any write |
| TC-E1-001-09 | AC8, BR12 | Contract | The `rwb-source-data` and `rwb-case` contract mocks answering the declaration, "D6" and "L6"; one hop, 2 s timeout |
| TC-E1-001-10 | AC10, BR4 | Component | An entry with chain_seq 1 and final call "OWNER_ASSIGNED"; an UPDATE to "CASE_TRANSFERRED" and a DELETE, through the service login and the schema owner |
| TC-E1-001-12 | AC1, AC7, BR1 | End to end | A statement that names `rwb_case`, a foreign key that points at `public`, and a grant to another service's login, each refused by the boundary test |
| TC-E1-001-13 | AC1, BR1 | End to end | The six tables of §12.7 each in `rwb_decision`; the boundary test finds no statement or grant that names any of the other 86 tables of the estate |
| TC-E1-001-14 | AC12, BR3, BR9 | Component | Not specified in the source documents (NEWAC-RWB-P7-E1001-APP-AC12) |
| TC-E1-001-15 | AC13 | Component | Not specified in the source documents (NEWAC-RWB-P7-E1001-APP-AC13) |

The twelve legacy TC IDs of the key are kept, one row each, and each is answered here on the schema side: the six tables, their keys, their indexes, the append-only trigger and the declaration. The legacy level System maps to Component or End to end as the row shows, and Access maps to Component. The `-ITG` copies of these test cases belong to RWB-ITG-E1001-ITG, which runs the same values across the service contracts; no `-ITG` id is written here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails
- No business value in code: the decision codes, final calls, approval levels, capability areas, product groups, route sets, rule-table codes, test results, Field IDs and version labels are rows; the lists are reference data with a version and arrive through DP-07 (BR3, BR12, AC11).
- No personal data anywhere: the six tables hold codes, references, versions, amounts, dates and user references; a rule test case holds synthetic facts; no test fixture, log line or prompt carries a name, an e-mail address or an identity number (BR9).
- No cross-schema read and no cross-schema key (DP-01): every statement names `rwb_decision`, the login holds a grant on `rwb_decision` only, and no constraint or index points at `public` or at another service's schema (BR5).
- ACE data only through the owner's contract or `v_ace_*` views: the service holds no grant on the 30 `recovery.v_ace_*` views, which are `rwb-source-data`'s, and this story reads no ACE data at all (DP-05, ADR-010; BR8).
- The built baseline is never rewritten: the monolith's `V0001`, its 92 tables, its dictionary and its 14 data product rows keep their version, their names and their rows, and this story adds a new line rather than editing an applied version (BR7). The migration changes nothing outside `rwb_decision`, creates no grant to another login, never drops a table in PROD and is forward only (DP-15; BR6).
- Append only and hash chained: no UPDATE and no DELETE on `decision_log_entry`, the trigger and the missing grant both refuse them, and a correction is a new entry with `corrects_entry_id` (BR4).
- One writer per table: this story creates the six tables and writes no row, so a migration cannot silently seed a rule, an approval or a decision (BR10).
- One hop and a 2 s timeout on every call to another service, and none at run time here (DP-11); the declaration and the dictionary cannot drift, because the conformance test compares both directions (BR13, AC3); and one base and one topic — `/api/recovery/decision/v1` and `rwb.decision.events.v1` with `rwb-decision` in namespace `rwb-recovery`, with no monolith base and no other service's base or topic declared here as this service's own.

### 18. Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record, one read path and one owner | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-01, FEAT-RDF-02 | All recovery processes | CTL-08; Principle 1; D-RCV-35 U1, U4 | TC-E1-001-01, TC-E1-001-02, TC-E1-001-03, TC-E1-001-05, TC-E1-001-08 |
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Epic 2, 4; Program, 5.1 | FEAT-RDF-01 | All recovery processes | REQ-RDF-001; D-RCV-35 U1 | TC-E1-001-03, TC-E1-001-09, TC-E1-001-12 |

REQ-RDF-001 and REQ-RDF-014 are carried on this story only for the schema share of the estate: DP12 (Decision log) is the data product of `decision_log_entry` and `approval`, DP14 (Reference data) is the data product of the four rule tables, and the one system of record of both is the Recovery Workbench. The catalog rows, the dictionary rows and the dictionary endpoint are RWB-P1-E1001-APP's, and this story writes none of them.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1001-APP | App development | The one catalog and the one dictionary in `rwb_source_data`; this story hands it the field-row declaration and writes no row of it |
| RWB-P4-E1001-APP | App development | The five authority tables in `rwb_access`, `delegation_limit` among them, which `approval` names by value |
| RWB-P1-E1069-APP, RWB-P1-E1069-DB | App development, ACE DB | The 30 read-only ACE views and their grants; this service holds no grant on them |
| RWB-PLT-NF06-DB | ACE DB | The schema split itself: the 19 `rwb_*` schemas, the logins and the grants; this story is P7's share of it (DP-01) |
| RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-E1047-CON, RWB-PLT-N001-CON | Contract | H, carried by the service baseline: the decision-record library and `rwb.decision-record.v1`, the two client libraries, the per-service Flyway sequence, the naming library and the gateway-bff route (DP-03, DP-06, DP-07, DP-15, DP-14, DP-19) |
| RWB-P7-E2017-APP, RWB-P7-E2019-APP, RWB-P7-E2021-APP, RWB-P7-E2022-APP | App development | The other four slices of the P7 work package; none of them creates or reads a table of this story |
| RWB-ITG-E1001-ITG | Integration | The integration harness of the key; no `-ITG` case is written here |

| Legacy reference | Where it is kept |
|---|---|
| The six tables of the legacy estate that the Ownership Map gives to P7 | Metadata, sections 1, 4, 11, 12.7 |
| The append-only trigger on `decision_log_entry`, and the hash chain with `chain_seq`, `prev_hash` and `entry_hash` | Sections 4, 5 (X6), 7 (AC4), 8 (BR4), 9, 13 |
| Keys and constraints inside one schema, business keys by value; and the dictionary held as one dictionary in the data product schema | Sections 1, 2, 7 (AC2, AC3, AC8), 8 (BR2, BR5, BR13), 11 |
| The 14 data products DP01 to DP14 and their one system of record (legacy AC1, AC3, AC7 to AC11) | Sections 1, 2, 7, 11, 18 |
| A failed statement leaves no partial schema and the version line (legacy AC4); the two conformance failure texts (legacy AC5); a repeated migration changes nothing (legacy AC6) | Sections 5 (X1, X2, X4), 7 (AC3, AC5, AC6), 8 (BR6), 14 |
| The rule version with its workbook, DRL, checksum, tests, approver and valid-from date | Sections 4, 8 (BR11), 11, 13 |
| Values reused: case "RW-2026-000123", decision "D6", rule "R-UNI-14", level "L6", "OWNER_ASSIGNED", "CASE_TRANSFERRED", chain_seq 1, `tr_declog_append_only`, "ALLOC-2026.12", "ALLOC-2026.13", version 1.001, 92 tables, at least 123 `sys_objects`, at least 1,379 `sys_fields`, 14 `data_product` | Sections 3, 7, 11, 16 |
| Messages MSG-P7-003 and the trigger text "decision_log_entry is append only"; legacy key RWB-E1-001 and story RWB-P7-E1001-APP; test cases TC-E1-001-01 to TC-E1-001-12; patterns DP01, DP03, DP05, DP06, DP07, DP11, DP14, DP15, DP19 | Sections 12, 13, 14, 16, metadata |

The other slices of the key answer the rest: RWB-P1-E1001-APP the catalog, the data product rows and the one dictionary; RWB-P1-E1069-APP and RWB-P1-E1069-DB the 30 ACE views and their grants; RWB-P4-E1001-APP the five authority tables and `delegation_limit`; RWB-P3-E1001-APP `lov_value` and the reference tables; RWB-S9-E1001-APP `partner_user`; RWB-PLT-NF06-DB the 19 schemas, the logins and the grants; and RWB-ITG-E1001-ITG the cross-service harness and the `-ITG` copies.

### 19. Out of scope
- The other 86 tables of the 92-table estate and the DB stories that create them in their owners' schemas (RWB-PLT-NF06-DB and the per-service DB stories), and the built baseline itself: schema `recovery`, its `V0001`, its 92 tables, its dictionary and its 14 data product rows stay as built and are not re-opened (BR7; Template and Rules §R6).
- The catalog, the data product rows, the dictionary rows, the field versions and the dictionary endpoint: RWB-P1-E1001-APP and RWB-P1-E1064-APP. This story declares its field rows and writes none.
- The 30 read-only ACE views, their grants and the boundary rule (RWB-P1-E1069-APP, RWB-P1-E1069-DB); this service holds no grant on them (DP-05).
- `lov_value`, `reference_row`, `reference_version` and the parameter tables: reference data of `rwb-case` (P3) under the ownership ruling, reached through DP-07 and DP-06; and `role`, `permission`, `role_conflict`, `masking_rule` and `delegation_limit`: `rwb-access`'s (P4) and RWB-P4-E1001-APP's, with `approval.delegation_limit_id` staying a value. `partner_user` is `rwb-partner`'s (S9) and the four extension tables are `rwb-source-data`'s (P1).
- The row writes: the decision entries and their ingest on `rwb.decision-record.v1`, the approval items and their routing, and the rule packages, versions, rows and test cases with their load checks, their four-eyes approval and their rollback. Those are the decision-centre, approval and rule-registry stories of this service.
- The REST operations of the schema (API-P7-001 to API-P7-008), the events `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce`, the approval workflow and the schedules: the service's own later stories' and the contract stories'; and the embedded Drools kit, the rule evaluation inside an activity, the model cache and the checksum verification in the owning service (DP-04; RWB-PLT-E1072-CON): the services that evaluate a package.
- The data-lake copy of the log, JOB-13 and lake retention: retired with the data lake (DP-17); the ingest of the central ledger is continuous Kafka.
- The screens SCR-10, SCR-11 and SCR-38 as built screens, the rule administration screens and the composite route: the screen stories and RWB-PLT-N001-CON; and the integration harness RWB-ITG-E1001-ITG with the `-ITG` copies of the test cases and the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of the schema (an OPS story of this legacy key).
