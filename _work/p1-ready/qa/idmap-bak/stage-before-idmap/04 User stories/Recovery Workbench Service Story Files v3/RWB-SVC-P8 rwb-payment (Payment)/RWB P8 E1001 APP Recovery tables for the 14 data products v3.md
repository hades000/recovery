# RWB-P8-E1001-APP Recovery tables for the 14 data products

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-025: Align the dictionary minimums.
- Backfill the published Test Cases v9 cross-references.
- RD-P1-066: Align the ownership of JOB-07 and JOB-08 with the job register amendment.
- The matching run starts only on `AceDataReady` with `sourceSystem` ALS and `status` COMPLETED; events for other source systems start nothing (RD-P1-003, RD-P1-040).

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-001 is realigned into `rwb-payment`. The built migration `V0001__rwb_e1_001_recovery_schema.sql`, the 92-table estate and its dictionary are kept as built; this story carries P8's one table of that estate — `proceeds`, the receipt and what it was matched to — into the service's own schema `rwb_payment` (DP-01, DP-15), with its key, its read indexes and the 7 standard record columns, on a forward-only Flyway sequence of its own. It loads no row, provides no REST operation, publishes no event and starts no workflow. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P8-E1001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (34 resolved, 52 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

| Item | Value |
|---|---|
| Story key | RWB-P8-E1001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 1 |
| Wave note | Wave 1 kept for rwb-payment, whose Arch v5 wave is 2; the service wave governs its later stories (GAP-3171) |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-001 |
| Legacy disposition | Must change |
| Build status | In build |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP11, DP14, DP15, DP19 |
| Parallel lane | L-P8-B |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement; the size value is Not specified in the source documents (DOR-RWB-P8-E1001-APP-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract published | Not applicable: the story provides no REST operation, so no contract story is needed; its baseline contracts are the six platform contracts named in the Background |
| Contract fake library | Not specified in the source documents (DOR-RWB-P8-E1001-APP-22); the rwb-source-data contract fake of §12.8 is used by TC-E1-001-11 |
| Contract version | Not applicable: the story builds against no contract version |
| Readiness decisions | RD-P1-003, RD-P1-025, RD-P1-040, RD-P1-066 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to REQ-RDF-001, REQ-RDF-014) |
| Status | Draft (directive resolutions) |

### 1. Story
As a **data steward and data product owner (RW-DATASTEW) of DP13, the reconciliation officer (RW-CREDITAD) and the `rwb-payment` service**, I want **P8's one table of the 92-table estate, `proceeds`, created in the service's own schema `rwb_payment` with its primary key, its read indexes and the 7 standard record columns, on the service's own forward-only Flyway sequence, and no row of it loaded**, so that **every receipt and every match has one home in one schema, the matched and unmatched reads have one baseline, and no service reads another service's table to reach the money on a case**.

The legacy story built the estate as one schema, `recovery`, with 92 tables. D-RCV-60 keeps that build and moves the ownership.

- **Kept as built (§R6 "Must change"; U2):** the migration `V0001__rwb_e1_001_recovery_schema.sql`, the 92 tables in schema `recovery`, at least 1,379 `sys_fields` rows, at least 123 `sys_objects` rows and the 14 `data_product` rows. This story rewrites none of them, drops none of them and writes no dictionary or catalog row.
- **The new work is the schema split:** one schema, one login and one Flyway sequence per service, forward only (DP-01, DP-15). The estate's 92 tables sit in one `rwb_*` schema each; the Ownership Map gives P8 one of them, `proceeds`.
- **Why `proceeds`:** it is the row of TSD P8 T3.1 that holds a receipt and its match (DF-FIN-001 to DF-FIN-009), and the write of step 5 of the journey, "Collect: money matched to the case and posted" (Architecture v5 slide 3). It belongs to DP13 Money and closure.
- **`payment_match_rule` is not created at all.** TSD P8 T3.1 lists it as the module's second table (DF-REF-261 to DF-REF-273) and it is retired under D-RCV-36 T10: the match rules are rows of a rule package of `rwb-decision` (GAP-2535; ASM-4193).
- **No rows are loaded.** The receipts are written by the matching stories from the P1 payments operation, one row per receipt with its decision record and its outbox row (DP-03, DP-05). A seeded receipt would be a money row with no source, no match and no record.
- **The dictionary is one dictionary and it is not P8's.** The `sys_fields` and `sys_objects` rows belong to RWB-P1-E1001-APP in `rwb_source_data`; this story declares its 9 field rows as a build artefact, hands them to that seed and proves them matched by a conformance test (GAP-2537; ASM-4195).
- **Bases and names:** `/api/recovery/payment/v1`, schema and login `rwb_payment`, topic `rwb.payment.events.v1` with event names `rwb.payment.<Event>.v1`, queue `rwb-payment` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.payment` (DP-13, DP-14). This story provides no operation, publishes and consumes no event, starts no workflow, creates no Schedule and serves no screen (DP-19, RWB-PLT-N001-CON).

### 2. Business rationale
Money is the step where a case stops arguing and starts closing: a plan instalment, a settlement instalment, an auction or enforcement receipt, the money a buyer pays for a lot. Each is one receipt that must be matched to exactly one case, and the module records why that is hard today — payments are matched to plans and settlements by hand, and broken plans are found late (FSD P8 A1.3). The measure is receipts matched the same day, rising each month, read from the decision log and the Workbench records (FSD P8 A2.1.1). Legacy RWB-E1-001 created the table that holds the answer as one of 92 tables in one schema, with one dictionary and one catalog of DP01 to DP14; every later story of this module reads that row, so it is the floor the service stands on.

**What D-RCV-60 changes.** Not the rationale and not the columns: the built migration is the baseline and stays as built. The 92 tables were one schema with one login; they are now 19 `rwb_*` schemas, one per service, each with its own login, sequence and grants, checked by a test that fails the build on a cross-schema reference (DP-01, DP-15). P8's share is the money table, and it is a story of its own because it is the one place where the match gets its keys, its indexes, its empty baseline and its row in the one dictionary; split away from `rwb_payment`, the write of a receipt with its record and its event would be three cross-schema writes on the money path. P8 is a wave 2 service and Epic 1's wave is 1, so the story keeps the earlier wave under §R5.6 and the conflict is recorded once for this service and business epic, never as a date (GAP-2541; ASM-4199).

**One system of record, and the row it cannot answer for.** DP13 is catalogued as "ACE (ingested from ALS and GL)" and holds two kinds of fact: the money the ACE batch reports and the match this service decides. Legacy BR3 allows one sentence naming both; the catalog row names ACE only, so the conflict is recorded here and the wording stays P1's to correct (GAP-2539; ASM-4197).

### 3. Preconditions
- RWB-PLT-E1044-CON is in place and the schema `rwb_payment` with its login exists, so Flyway migrates in the `rwb-payment` pipeline, takes the schema name from the deployment configuration and migrates only there (DP-15; RWB-PLT-NF06-DB). The legacy parameter and the built `V0001` are the baseline and are not re-opened.
- The other 18 `rwb_*` schemas exist with their own logins, and `rwb_payment` holds no grant on any of them and none on the 30 `recovery.v_ace_*` views, which are `rwb-source-data`'s (DP-05).
- The service baseline is applied: the template, the decision-record library and `rwb.decision-record.v1` (RWB-PLT-E1027-CON), the naming library (RWB-PLT-E1047-CON), the gateway-bff route (RWB-PLT-N001-CON) and the parameters and reference-data libraries (RWB-PLT-E1042-CON, RWB-PLT-E1043-CON). Those six contracts are the baseline's: "Depends on (build)" is None and Ready is Day 1, so they are carried here and in GAP-2540 with ASM-4198, not in an H row.
- The DEV and SIT databases exist, with a container database for the migration test that holds `rwb_payment` and no other `rwb_*` schema.
- The dictionary is RWB-P1-E1001-APP's, in `rwb_source_data`; the declaration of these field rows is handed to that seed as a build artefact and no run-time read of it is made here (GAP-2537).
- The built baseline is in force: schema `recovery`, its 92 tables, its dictionary, its append-only triggers and the 30 views.
- The match rules in force are rows of a rule package of `rwb-decision`, and no tolerance, window or grace value is held here (D-RCV-36 T10; BR-P8-001).
- The migration file name is `V<seq>__rwb_p8_e1001_payment_schema.sql` under D-RCV-28. The sequence is taken at merge in the rwb-payment pipeline, and the applied version is later than every service-baseline version and never 0001 of the legacy line (GAP-0978; ASM-4192). The primary key name, the two index names and the index columns beyond the leading one are fixed at merge under the platform naming convention (GAP-2534; ASM-4192).

### 4. Flow
1. Pipeline: applies this story's Flyway file on `rwb-payment`'s own sequence, in DEV first (DP-15).
2. Migration: creates `proceeds` with the 9 business columns DF-FIN-001 to DF-FIN-009 and the 7 standard columns of TSD P8 T3.0, and a primary key on `id`.
3. Migration: fixes the types character for character — `source` varchar(12), `amount` numeric(18,2), `received_date` date, `matched_to` varchar(15), `posting_ref` varchar(40) — and creates no enum and no check constraint on a list value (BR3).
4. Migration: creates the two read indexes — the unmatched list of a business date, indexed on `matched_to` and `received_date`, and the receipts of a case, indexed on `case_id` and `received_date` (section 13).
5. Migration: adds no foreign key; `case_id`, `treatment_id` and `account_payment_id` are values (BR5; GAP-2538).
6. Migration: writes no row, creates no view and no grant, and touches no object of schema `recovery` (BR7, BR10).
7. Pipeline: runs the conformance test (both directions against the declaration, ignoring the 7 standard columns), the boundary test (any schema name other than `rwb_payment`, any grant to another login) and the index-plan check over the two read paths with the SIT rule set.
8. Pipeline: repeats in SIT, where the baseline is present and must be unchanged.
9. A later story of the service writes rows: the matching stories write one row per receipt with its record and its outbox row in one transaction (DP-03, DP-09; RWB-P8-E2008-APP, RWB-P8-E2027-APP). This story writes none.

### 5. Exception paths
| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A statement in the migration fails | The transaction rolls back; no `proceeds` table; the stage fails with the statement named | None (pipeline log) | AC4 |
| X2 | A business column has no declaration row, or a row has no column or a different physical type | The conformance test fails and names the table, the column and the Field ID | None (pipeline log) | AC3 |
| X3 | A statement, a repository or a test names another schema, or the migration grants to another login | The boundary test fails and names the statement, the schema or the grant | None (pipeline log) | AC6 |
| X4 | The migration is applied twice, or reuses a version the service or the built baseline holds, including 1.001 | Flyway skips it, or the pipeline refuses the reused version; no object and no row changes | None (pipeline log) | AC5 |
| X5 | A login without a grant on `rwb_payment` reads `proceeds` | Refused before a row is returned; no money fact leaves the schema | insufficient_privilege | AC6 |
| X6 | A row is expected after the migration | There is none; a test that expects a receipt is the matching story's | None | AC7 |
| X7 | The declaration is not handed to the one seed, or it drifts from the columns | The conformance test fails the build and names the entity, field and Field ID; the dictionary is never patched at run time | None (pipeline log) | AC3, AC9 |
| X8 | A new proceeds source, match value or posting state is proposed | It is a list value under a new version, or a row of a receipt; no migration is needed | None | AC11 |

No exception path here changes a case, a receipt, a match or a posting: this story creates one table, and the answers it serves belong to the stories that write and read it.

### 6. INVEST check
| Test | Result |
|---|---|
| Independent | Needs the per-service Flyway sequence and the service baseline, both already build dependencies of the service's own stories; every later P8 story writes or reads this one table |
| Negotiable | Columns and Field IDs are fixed by TSD P8 T3.1; the key, the index and the file sequence are agreed at merge (section 13) |
| Valuable | Gives the receipt and its match one home, one login and one empty baseline, and ends the shared-schema write on the money path |
| Estimable | One migration, one declaration, one conformance test, one boundary test, one plan check; no endpoint, no event, no workflow |
| Small | Two weeks or less with its tests, and it unblocks the service's matching stories rather than waiting on them |
| Testable | Each criterion below is one automated test, and the two read paths have a plan assertion |

### 7. Acceptance criteria
No legacy criterion is owned verbatim by this story: `acs` is empty for RWB-E1-001, and every legacy criterion tests the monolith's single `recovery` schema, its one `V0001` line, its 92-table count, its dictionary seed and its catalog load, which belong to RWB-P1-E1001-APP, the per-service DB stories and RWB-PLT-NF06-DB. The thirteen below are new for the `rwb_payment` slice and test only `proceeds`. The legacy values reused are those of legacy AC1 (the 92-table estate, the 20 tables that left it, the no-`public`-reference rule, the five business keys with no foreign key, the 1,062-field count), legacy AC2 (Field ID, data type, physical type, data product), legacy AC3 and AC10 (the catalog rows, DP13 among them), legacy AC4 (a failed statement leaves no partial schema and no successful version row), legacy AC5 (the two conformance failure texts) and legacy AC6 (a second run changes nothing). Where a cross-service answer is needed the Given names the owner's contract mock, and every legacy value is kept character for character.

```gherkin
Feature: The proceeds table in rwb_payment

  Background:
    Given the environment is SIT
    Given the service is rwb-payment, its schema is rwb_payment and its REST base is /api/recovery/payment/v1
    Given the built baseline holds schema recovery with its 92 tables, at least 1,379 sys_fields rows and its 14 data_product rows
    Given the six platform contracts RWB-PLT-E1044-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON and RWB-PLT-N001-CON are the service baseline and its fakes

  Scenario: AC1 The proceeds table exists and nothing else does (new, D-RCV-60)
    Given an empty container database with the schema rwb_payment and the service's own login, and no other rwb_* schema
    When the pipeline applies the migration "V<seq>__rwb_p8_e1001_payment_schema.sql" on rwb-payment's own Flyway sequence
    Then rwb_payment holds exactly one table, proceeds, with DF-FIN-001 to DF-FIN-009 and the 7 standard columns of TSD P8 T3.0
    Then it holds none of the other 91 tables of the estate: no recovery_case, no task, no queue, no treatment, no document, no notice, no lov_value, no role, no delegation_limit, no decision_log_entry, no payment_match_rule and no extension table
    Then it holds no copy of an ACE table: no account, no party, no account_payment and no v_ace_* view, and the legacy marker recovery.proceeds is not created, not read and not dropped

  Scenario: AC2 Keys and constraints stay inside rwb_payment (new, D-RCV-60)
    Given the proceeds table created by AC1's migration
    When the keys and constraints of rwb_payment are read from the catalogue
    Then proceeds has a primary key on id, source is varchar(12), amount is numeric(18,2), received_date is date, matched_to is varchar(15) and posting_ref is varchar(40)
    Then case_id, treatment_id and account_payment_id carry no foreign key, because their owners are rwb_case, rwb_treatment and the ACE payment fact
    Then no foreign key, index or default names schema public or another rwb_* schema, and no check constraint holds a value of LOV-MATCH or LOV-PROCEEDS-SRC
    Then the constraints and indexes follow the platform naming convention, with the read paths of section 13 as their leading columns

  Scenario: AC3 The declared field rows are complete and matched (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the dictionary rows of the declaration: proceeds with DF-FIN-001 to DF-FIN-009, data product "DP13"
    When the conformance test compares information_schema.columns of rwb_payment with the declaration
    Then it reports all 9 declared business fields matched by name, data type, physical type and Field ID, one for one in both directions
    Then changing the declared physical type of DF-FIN-006 to text fails it with "DF-FIN-006 physical type numeric expected, text found", and adding proceeds.branch_code with no row fails it with "proceeds.branch_code has no data dictionary entry"

  Scenario: AC4 A failed statement leaves no table (new, D-RCV-60)
    Given a copy of the migration in which the statement creating the unmatched-list index fails
    When the pipeline applies it in DEV
    Then the stage fails and names the failing statement
    Then rwb_payment holds no proceeds table and no index, and the Flyway history has no successful row for that version

  Scenario: AC5 A second run of the same version changes nothing (new, D-RCV-60)
    Given this story's migration applied in SIT
    When the pipeline runs again in SIT
    Then Flyway reports the version as already applied and applies no statement
    Then rwb_payment still holds proceeds with its 9 business columns, its 7 standard columns, its key and its two indexes, and no row
    Then the built baseline's version 1.001, its 92 tables, at least 123 sys_objects rows and at least 1,379 sys_fields rows are unchanged

  Scenario: AC6 No table of another service and no ACE table is read (new, D-RCV-60)
    Given the login rwb_payment holds grants on schema rwb_payment only
    When the build runs the boundary check over the migration, the repositories and the pipeline tests
    Then every statement names rwb_payment, and no statement names rwb_case, rwb_treatment, rwb_source_data or any other rwb_* schema
    Then a direct SELECT on rwb_case.recovery_case and on rwb_source_data.sys_fields through this login is refused with insufficient_privilege
    Then a SELECT on recovery.v_ace_payment through this login is refused, because the 30 views are granted to rwb-source-data only

  Scenario: AC7 The table is created empty (new, D-RCV-60)
    Given this story's migration applied in SIT
    When proceeds is counted
    Then it holds 0 rows and its 9 business columns and 7 standard columns are present
    Then the migration inserted no receipt, no match and no posting reference, and the 14 data_product rows stay the baseline's and RWB-P1-E1001-APP's

  Scenario: AC8 The indexes serve the two money reads (new, D-RCV-60)
    Given proceeds holds the matched and unmatched receipts of one SIT day for a set of cases
    When the two read paths run with EXPLAIN: the unmatched receipts of a business date in received_date order, and the receipts of one case
    Then each plan uses an index whose leading column is the one section 13 names, and no plan is a sequential scan
    Then dropping the index of the unmatched-list path makes the plan check fail, so it cannot pass by accident

  Scenario: AC9 The built estate stays as built (new, D-RCV-60)
    Given the built baseline at version 1.001 with its 92 tables, its dictionary and its 14 data_product rows
    When this story's migration is applied in SIT
    Then schema recovery still holds the 88 Workbench tables and the four extension tables party_ext, contact_point_ext, account_ext and valuation_ext
    Then it still holds none of the 20 tables that left it: loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory and tracker_row
    Then this story writes no data_product, sys_objects or sys_fields row, and the 92 tables still hold 1,062 fields and the dictionary holds at least 123 objects and at least 1,379 fields

  Scenario: AC10 DP13 stays one data product with one catalog row (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the DP13 row with the system of record "ACE (ingested from ALS and GL)", refresh cycle "DAILY" and expected by "08:00"
    When a receipt is matched and its proceeds row is written by the matching story
    Then the receipt carries DP13, the row is read through the reference-data contract in one hop with a 2 s timeout, and this migration writes no catalog row
    Then DP13 is not split into a second product for the match, because the match travels with the money on the same row (GAP-2539)

  Scenario: AC11 A new list value needs no migration (new, D-RCV-60)
    Given proceeds created by AC1's migration, and LOV-MATCH and LOV-PROCEEDS-SRC at the version in force
    When one value is added to each list with its version, and a receipt is written with the new source and match
    Then no enum, constant or check constraint on a list value is needed, no migration changes and the declared field rows are unchanged
    Then the two values are read as rows through the reference-data contract of rwb-case in one hop with a 2 s timeout

  Scenario: AC12 The migration writes no receipt, no decision and no posting, and no fixture holds personal data (new, D-RCV-60)
    Given this story's migration applied in SIT
    When the pipeline runs the migration and the fixtures of the table's tests are read
    Then the migration writes no receipt, no match row, no decision record and no posting reference (BR4, BR11)
    Then every fixture is synthetic and the table holds only references, a source, an amount, a date, a match value and a posting reference (BR9)

  Scenario: AC13 No provided operation answers 401, 403 or 404 (new, D-RCV-60)
    Given the story provides no REST operation under /api/recovery/payment/v1
    When the build runs the boundary check over the migration and the pipeline tests
    Then no route is registered by this story, and no 401, 403 or 404 answer is defined by it
```

### 8. Business rules
| ID | Rule | Source |
|---|---|---|
| BR1 | `rwb_payment` holds `proceeds` and no other table of the estate; every table, key, index and constraint names `rwb_payment` only | DP-01; Ownership Map |
| BR2 | Every business column has exactly one dictionary row with its Field ID, data type, physical type and data product, and no column exists without one | LDM and Data Dictionary; TSD P8 T3.1; RWB-P1-E1001-APP |
| BR3 | Every list of values is reference data read through the reference-data contract of `rwb-case` with the version in force; no list value is a column type, a check constraint or a constant | DP-07; R5 default ruling; BR-P8-001 |
| BR4 | A receipt is one row and one home: the row, its decision record and its outbox row are written in one transaction by a matching story, and a migration never writes one | FSD P8 A2.1; DP-03, DP-09; R-UNI-39 |
| BR5 | A key by value stays a key by value: `case_id`, `treatment_id` and `account_payment_id` carry no foreign key, as the estate's links to an ACE record are business keys with no foreign key | Legacy BR8; TSD P8 T3.3 (GAP-2538) |
| BR6 | Schema names come from configuration; one migration per story; forward only in PROD; never drop a table in PROD | RWB-E1-044; D-RCV-28; DP-15 |
| BR7 | The built baseline is kept as built: the monolith's `V0001`, its 92 tables, its dictionary and its 14 data product rows are not rewritten, dropped or re-opened | §R6 "Must change"; U2 |
| BR8 | ACE data is reached only through the contract of its owner: this service holds no grant on the 30 views and no copy of an ACE payment, account or party table | DP-05; ADR-010; D-RCV-35 U4 |
| BR9 | No personal data in the table and its tests: a receipt holds references, a source, an amount, a date, a match value and a posting reference, and every fixture is synthetic | NFR-039; NFR-040; FSD P8 T6.2 |
| BR10 | The table is created empty and the match rules are not a table: `payment_match_rule` is retired and the rules in force are rows of a rule package of `rwb-decision` | D-RCV-36 T10; Ownership Map (GAP-2535) |
| BR11 | No posting is made from this schema: the row records what was matched, and the booking and the ledger post are the next ACE batch and the owner's postings | FSD P8 A2.7; TSD P8 T5.1 INT-03, INT-16 |

BR1 is the migration and the boundary test. BR2 is the declaration and the conformance test; the rows stay in `rwb_source_data` (GAP-2537), and the field-row declaration is handed to the one dictionary seed through the Change Register as a build artefact proved by the conformance test. BR3 is why `source` and `matched_to` are varchars with no check constraint, so a new value is a row of the closed list in the reference data and not a column change. BR4 is the empty table of AC7. BR5 is the absence of three foreign keys (GAP-2538). BR6 is the per-service sequence. BR7 is the boundary with the baseline (AC9). BR8 is the grant test of AC6. BR9 is why the table is safe to log. BR10 is the retired rule table. BR11 is why no ledger column is copied here, and AC12 tests BR4, BR9 and BR11.

### 9. State transitions
This story changes no case, receipt, match or posting state and answers no request. It changes the Flyway version of `rwb_payment` and nothing else.

| From | To | Trigger |
|---|---|---|
| `rwb_payment` at the service baseline, without `proceeds` | The version this story applies: one table, its key, its two indexes, no row | The pipeline applies the migration in DEV, then SIT |
| The version applied | The version applied, no change | The same file runs again; Flyway skips it (AC5) |
| `proceeds` absent | A row per receipt with `matched_to` INSTALLMENT, SETTLEMENT, FEE, SALE_PROCEEDS or UNMATCHED | The matching stories, with their record and outbox row; not this story |
| A row | The same row, matched or re-matched under the operation's idempotency key and its rule version | `POST /proceeds/{proceedsId}/match` of RWB-P8-E4044-APP; never a migration |
| The baseline at 1.001 | The baseline at 1.001, unchanged | Never (BR7) |

### 10. Authority
| Who | What they may do in this story |
|---|---|
| Pipeline service identity (`rwb-payment` pipeline) | Runs the migration, the conformance test, the boundary test and the plan check in DEV and SIT, in `rwb_payment` only |
| ACE team (suggested; any team may pick up this story) | Reviews the DDL, the key, the indexes and the grants, and creates the schema and the login with RWB-PLT-NF06-DB |
| RW-DATASTEW, data steward and data product owner | Owns DP13 and confirms the table belongs to it; writes no row and changes no DDL here |
| RW-CREDITAD, Credit Administration officer | Owns the reconciliation of the matched and unmatched lists on SCR-28 in later stories; holds no DDL right here |
| RW-FINANCE, Finance and CFO delegate | Confirms no ledger posting column is copied here and the posting reference is the ACE answer |
| RW-AUDIT, internal audit; RW-PLATADM, platform administrator | RW-AUDIT verifies that every receipt has one home; RW-PLATADM owns the schema, the login and the grants through RWB-PLT-NF06-DB |
| The other services' logins | Hold no grant on `rwb_payment`: a table read is refused, and the supported path is this service's contract |

No approval level from the delegation of authority applies: this story creates a table and approves no limit and no posting. Every "who" is a role code; the roles and the delegation rows are data in `rwb-access`. This story exposes no REST operation, so the `rwb-access` authorise check of DP-08 is not called here.

### 11. Data
| # | Table in `rwb_payment` | BR Field IDs | Business fields | Read or write in this story |
|---:|---|---|---:|---|
| 1 | `proceeds` | DF-FIN-001 to DF-FIN-009 | 9 | Create (table only) with the primary key and the two read indexes; read |

| Field ID | Field | Data type | Physical type | Required | Source |
|---|---|---|---|---|---|
| DF-FIN-001 | `id` | TEXT | uuid | Yes | Workbench |
| DF-FIN-002 | `case_id` | CROSS_REF | uuid | Yes | Workbench |
| DF-FIN-003 | `treatment_id` | CROSS_REF | uuid | No | Workbench |
| DF-FIN-004 | `account_payment_id` | CROSS_REF | uuid | No | Workbench |
| DF-FIN-005 | `source` | LOV | varchar(12) | Yes | `LOV-PROCEEDS-SRC` |
| DF-FIN-006 | `amount` | NUMBER | numeric(18,2) | Yes | Core bank (ALS) via COLLINS |
| DF-FIN-007 | `received_date` | DATE | date | Yes | Core bank (ALS) via COLLINS |
| DF-FIN-008 | `matched_to` | LOV | varchar(15) | Yes | `LOV-MATCH` |
| DF-FIN-009 | `posting_ref` | TEXT | varchar(40) | No | Core bank (ALS) via COLLINS |

The table also carries the 7 standard columns of TSD P8 T3.0: `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at` and `updated_by`. Their Field IDs are Not specified in the source documents (GAP-2534; ASM-4192) and are carried by the one dictionary's seed. The lists are `LOV-MATCH` (INSTALLMENT, SETTLEMENT, FEE, SALE_PROCEEDS, UNMATCHED) and `LOV-PROCEEDS-SRC` (CUSTOMER, LED, AUCTION, BUYER, AGENCY, INSURER, GUARANTOR) of TSD P8 T3.2, read as closed lists of reference data.

**What is not in the schema.** `recovery_case`, `task` and `queue` are `rwb-case`'s (P3); `treatment` is `rwb-treatment`'s (S2); the rule tables and `decision_log_entry` are `rwb-decision`'s (P7); `sys_objects`, `sys_fields`, `data_product` and the four extension tables are `rwb-source-data`'s (P1); `lov_value` and the parameter tables are reference data of `rwb-case`; `role`, `permission`, `role_conflict`, `masking_rule` and `delegation_limit` are `rwb-access`'s (P4); `document` is `rwb-document`'s (P5); `template` and `merge_field` are `rwb-comms`'s (P6). None is created, read or referenced here, and `account_payment` — the table legacy TSD P8 T3.3 points at — left the estate and is a value. `payment_match_rule` is retired (BR10).

**Rows.** This story writes none. The receipts are written by the matching stories from the P1 payments operation through the owner's contract (DP-05), one row per receipt with its record and its outbox row (DP-03); at least 123 `sys_objects` rows, at least 1,379 `sys_fields` rows and the 14 `data_product` rows stay the baseline's and RWB-P1-E1001-APP's.

### 12. Contract
#### 12.1 REST operations provided
| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| — | — | This story provides no operation. The two operations of the service — `GET /api/recovery/payment/v1/proceeds` and `POST /api/recovery/payment/v1/proceeds/{proceedsId}/match` (API-P8-001, API-P8-002) — are declared by the P8 contract stories and behave in RWB-P8-E2027-APP and RWB-P8-E4044-APP | None | None |

#### 12.2 REST operations consumed
| Method | Path | Owner | Use in this story |
|---|---|---|---|
| None | None | None | No operation is called at run time; the two lists are read by the later stories through DP-07 with a 2 s timeout, and nothing in the migration reaches another service |

#### 12.3 Events published
| Event | Topic | Owner | Trigger |
|---|---|---|---|
| None | `rwb.payment.events.v1` | P8 `rwb-payment` | This story publishes nothing. The topic with `TreatmentBooked`, `PaymentMissed` and `ProceedsMatched` (EV-11, EV-12, EV-25) is named by DP-14 and resolved by the naming library; a migration publishes nothing |

#### 12.4 Events consumed
| Event | Topic | Owner | Handler |
|---|---|---|---|
| None | None | None | No consumer is registered. `AceDataReady` (`sourceSystem` ALS, `status` COMPLETED) starts the payment-matching run of the service's own stories, and no event starts a migration |

#### 12.5 Workflows and activities
| Workflow or activity | Queue | Purpose |
|---|---|---|
| None | `rwb-payment` | No workflow and no activity is registered on queue `rwb-payment` in namespace `rwb-recovery`. The event-started matching run and its activities of JOB-07 belong to rwb-payment. JOB-08 belongs to rwb-integration. |

#### 12.6 Schedules
| Schedule | Queue | When | Purpose |
|---|---|---|---|
| None | `rwb-payment` | None | No Temporal Schedule is created: a migration runs on a deployment, not on a clock. JOB-07 in rwb-payment and JOB-08 in rwb-integration are event-started runs triggered by `AceDataReady` (`sourceSystem` ALS, `status` COMPLETED) |

#### 12.7 Tables owned
| Table | Schema | Owner (Ownership Map) | This story |
|---|---|---|---|
| `proceeds` | `rwb_payment` | P8 | Creates with its primary key, its two read indexes and its 7 standard columns; writes no row |
| `outbox_event`, `inbox_event`, `decision_record`, `idempotency_key` | `rwb_payment` | Platform library, created in this schema | **Not created here.** They arrive with the service baseline and their first writer is a matching story (DP-03, DP-09) |
| `sys_objects`, `sys_fields`, `data_product`, the four extension tables | `rwb_source_data` | P1 | **Never read and never written.** The dictionary is RWB-P1-E1001-APP's and this story hands it a declaration |
| `recovery_case`, `task`, `queue`; `treatment`; the rule tables and `decision_log_entry` | `rwb_case`; `rwb_treatment`; `rwb_decision` | P3; S2; P7 | **Never read and never written.** Three columns are values, not foreign keys |
| `lov_value`, `parameter_catalog`, `parameter_value`; `role`, `permission`, `role_conflict`, `masking_rule`, `delegation_limit` | `rwb_case`; `rwb_access` | P3; P4 | **Never read.** The two lists arrive through DP-07 |
| the other tables of the 92-table estate, and `payment_match_rule` | their owners' schemas; none | the 18 other services; retired | **Never read.** No grant, no join, no constraint, no view (DP-01); the rule table is retired under D-RCV-36 T10 |

`rwb-payment` writes nothing outside `rwb_payment`, its login holds no grant on another schema and none on the 30 views, which are `rwb-source-data`'s (DP-01, DP-05). The table list, the constraint set, the sequence assignment, the index columns and the retirement of the rule table are recorded in GAP-2534 to -3 with ASM-4192 to -3.

#### 12.8 Contract fakes
| Fake | Serves | Used for |
|---|---|---|
| rwb-source-data contract fake | DP-05 and DP-07 (no H and no C: the contracts are its own) | The dictionary rows of AC3, the DP13 catalog row of AC10 and the refusals of AC6 |
| rwb-case reference-data fake | DP-07 (no H: the contract is `rwb-case`'s) | `LOV-MATCH` and `LOV-PROCEEDS-SRC` at the version in force in AC11 |
| Flyway sequence fake (RWB-PLT-E1044-CON, the baseline) | The per-service sequence of DP-15 | The apply, the rollback and the skip of AC4, AC5 |
| schema and login fixture (RWB-PLT-NF06-DB); naming library fake (RWB-PLT-E1047-CON, the baseline) | The 19 schemas with one login each; the topic and event naming of DP-14 | AC6's grant test; the names are resolved, never typed |

Each fake is replaced by the real service as its story lands, without a change to the scenarios.

#### 12.9 Call-type summary
| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0, consumed 0 | The base `/api/recovery/payment/v1` is named; nothing is added and nothing is called |
| Kafka | Published 0, consumed 0 | `rwb.payment.events.v1` is named for DP-14; nothing is produced or consumed |
| Temporal | 0 workflows, 0 activities, 0 schedules | Queue `rwb-payment` in namespace `rwb-recovery` is not used |
| File | 1 build-time, 0 at run time | The field declaration of section 11, read by the conformance test and handed to the one seed |

### 13. Solution plan
**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `schema`. Base `/api/recovery/payment/v1`, schema and login `rwb_payment`, topic `rwb.payment.events.v1`, queue `rwb-payment` in namespace `rwb-recovery`, on the service's own Flyway sequence (DP-15).

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy marker this slice replaces is one schema with one login and one `V0001` baseline (DP-01, DP-15): the split is the new work §R6 records. The monolith name `recovery.proceeds` is marker text only: it stays as built and is neither the target nor a read path. The other seven DPs are carried by the key and their runtime work sits with the stories that write and read the table: the record with the row and the outbox row (DP-03), the ACE payment through the owner's contract or the service's view (DP-05), the lists and parameters through their contracts (DP-06, DP-07) in one hop with a 2 s timeout (DP-11), the topic names from the library (DP-14) and SCR-28 through the gateway-bff route (DP-19). This story creates a table, so none of them adds a call of its own. It adds no build edge either: the six platform contracts are the service baseline and are traced in section 18 rather than in an H row (GAP-2540; ASM-4198).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<seq>__rwb_p8_e1001_payment_schema.sql` | Flyway migration | Creates `proceeds` with its key, its two indexes and the 7 standard columns; writes no row, creates no view and no grant |
| `PaymentFieldDeclaration` | Build artefact and test fixture | The field-row declaration of `proceeds`; the source the conformance test compares against and hands to the one seed |
| `PaymentDictionaryConformanceTest` | Test (pipeline) | Compares `information_schema.columns` with the declaration in both directions, ignoring the 7 standard columns |
| `PaymentSchemaBoundaryTest` | Test (pipeline) | Fails on another schema name, on a grant to another login and on a foreign key that leaves the schema |
| `PaymentIndexPlanTest`, `PaymentGrantFixture` | Test and fixture | Assert the two read paths' plans with the SIT rule set, and the refusals of AC6 through a login with grants on `rwb_payment` only |

**Database and migrations.** One transaction creates `proceeds` and nothing else: `id` uuid primary key, `case_id` uuid not null, `treatment_id` uuid, `account_payment_id` uuid, `source` varchar(12) not null, `amount` numeric(18,2) not null, `received_date` date not null, `matched_to` varchar(15) not null, `posting_ref` varchar(40), plus the 7 standard columns. No check constraint holds a list value (BR3, AC11). Three columns are values, so the three relationships of TSD P8 T3.3 become references by value (BR5). The indexes are `proceeds (matched_to, received_date)` for the unmatched and matched list of a business date and `proceeds (case_id, received_date DESC)` for the receipts of a case and the daily reconciliation; their names and the column order beyond the leading column are Not specified in the source documents (GAP-2536; ASM-4194). No constraint, index or default names `public` or another `rwb_*` schema (BR1, BR8).

**Migrations in order** (forward only). 1. The service baseline: schema, login, the template's standard columns and the library objects (RWB-PLT-NF06-DB; RWB-PLT-E1027-CON), already applied. 2. This story: `V<seq>__rwb_p8_e1001_payment_schema.sql`, `proceeds` with its key and indexes and nothing else. 3. The service's own stories: the matching stories that write receipts, the contract and operation stories, and the settlement, auction, fees, ALS booking, ledger post and reconciliation stories; this story neither creates nor depends on them.

**Configuration and reference data.** The schema name comes from the deployment configuration of `rwb-payment` (RWB-PLT-E1044-CON); the legacy `recoverySchema` parameter stays the baseline's and is not read here. `LOV-MATCH` and `LOV-PROCEEDS-SRC` are read through the reference-data contract of `rwb-case` with the version in force (DP-07), never stored as a check constraint or a Java enum, which is why a new value needs no migration (AC11). No value the business may change is written in this story's code or migration.

**Build steps**

1. Write the migration from TSD P8 T3.1 and T3.0 with the schema from configuration; run it on an empty container that holds `rwb_payment` and no other `rwb_*` schema, and prove one table, its key and its two indexes (AC1, AC2).
2. Write `PaymentFieldDeclaration` and `PaymentDictionaryConformanceTest`; prove the test fails on an extra column and on a changed physical type (AC3).
3. Prove the rollback and the skip: a copy that fails on the unmatched-list index leaves no table and no successful version (AC4); a second run changes nothing (AC5).
4. Prove the boundary: the migration names `rwb_payment` only, creates no view and no grant, and a read of `rwb_case.recovery_case`, of `rwb_source_data.sys_fields` and of `recovery.v_ace_payment` through the service login is refused (AC6).
5. Hand the declaration to the one seed (RWB-P1-E1001-APP) and record the handover in the Change Register, writing no row of `rwb_source_data` (AC9; GAP-2537); prove no row is written (AC7); write `PaymentIndexPlanTest` and prove it fails when an index is dropped (AC8); confirm the DP13 row through the reference-data fake (AC10); and prove that a new list value needs no build (AC11).

**Feature switch.** None of its own: a migration is not behind a flag, the table either exists at the version or the pipeline has not applied it (BR6, BR7). The matching switches belong to the service's own stories.

**Done when.** The tests in section 16 pass; the migration runs clean in DEV and SIT; `rwb_payment` holds exactly `proceeds` with its key, its two indexes and no row; the declaration is matched; the boundary test reports nothing outside `rwb_payment`; and the read paths use their indexes.

**Screens and states.** This story serves no screen. SCR-28 and SCR-29 and their empty, loading, error and no-access states are carried by their own stories; this story writes no screen state.

**Ownership.** `rwb_case` is P3's and `rwb_source_data` is P1's; this story names them only as the refused targets of AC6 and never reads or writes them (§12.7).

### 14. Validation and messages
| ID | When | Message | Where it is produced |
|---|---|---|---|
| insufficient_privilege | A login without a grant on `rwb_payment`, or a read of `rwb_case`, `rwb_source_data` or a `recovery.v_ace_*` view through this login | The database's own refusal | PostgreSQL, asserted by AC6 |
| None (pipeline log) | A statement fails, a column has no declaration row, a row has no column or another physical type, a statement or grant names another schema, or a read path has no index | The stage fails and names the statement and its line, "{table}.{column} has no data dictionary entry", "{fieldId} physical type {expected} expected, {found} found", the schema found, or the read path and its plan | The pipeline, the conformance test, the boundary test and the plan check (AC3, AC4, AC6, AC8) |
| None | A receipt is matched, refused or left unmatched | MSG-P1-001, MSG-P8-001, MSG-P8-002, MSG-P4-002, MSG-P7-003 and MSG-GEN-001 are the matching and operation stories' (FSD P8 A2.1, A2.2; RWB-P8-E2008-APP); this story makes the store answer and produces no message | Not this story |

Every error that reaches a caller is an RFC 9457 problem response with `messageId`, `detail` and `instance`; the IDs are the service's later stories', because this story provides no operation. Its own failures stop the pipeline, and the log line carries the statement, the table or the Field ID. No message or log line carries a personal value.

### 15. Screens and states
No screen is built and no state is asserted here; the table is read by screens other stories build.

| Screen or answer | State | Where it is |
|---|---|---|
| SCR-28 Proceeds matching | Loading, matched, unmatched; empty, error, no access: Not specified in the source documents (CG-ALL-7503) | `rwb-payment` (matching and operation stories); reads `proceeds` and the case reference of `rwb-case`, merged by the gateway-bff route |
| SCR-29 Posting | Loading, approved booking, confirmation from the next ACE batch; empty, error, no access: Not specified in the source documents (CG-ALL-7504) | `rwb-payment` (ALS booking and ledger post stories); reads `proceeds.posting_ref` only |
| The daily money reconciliation answer | Loading, in balance, exceptions | `rwb-payment` (reconciliation story); reads `proceeds` against the ACE answers |

The composite route of DP-19 exists for those screens (RWB-PLT-N001-CON) and this story serves none of them: a table has no route. Their field lists, panel ids and layouts are Not specified in the source documents for this slice (GAP-2536).

### 16. Test cases
| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-001-02 | AC3, BR2 | Component | The 9-row field declaration handed through the Change Register; the dictionary answer of the rwb-source-data mock |
| TC-E1-001-03 | AC10, BR2, BR3 | Component | The DP13 catalog row of AC10; the rwb-source-data mock |
| TC-E1-001-07 | AC2, BR5 | Component | Keys and constraints; the three value columns `case_id`, `treatment_id` and `account_payment_id` as uuid values with no foreign key; the three relationships of TSD P8 T3.3 |
| TC-E1-001-11 | AC6, BR1, BR8 | Component | The `rwb_payment` login reads `rwb_case.recovery_case`, `rwb_source_data.sys_fields` and `recovery.v_ace_payment` through the rwb-source-data contract fake (§12.8); refused |
| TC-E1-001-12 | AC6, AC8, BR1 | End to end | A statement naming `rwb_case`, a foreign key at `public`, a grant to another login, and the two read paths with each index dropped |
| TC-E1-001-13 | AC6, BR1 | Component | Each table of §12.7 read and written through the `rwb_payment` login; refused outside `rwb_payment` |
| TC-E1-001-14 | AC12, BR4, BR9, BR11 | Component | Not specified in the source documents (NEWAC-RWB-P8-E1001-APP-AC12) |
| TC-E1-001-15 | AC13 | Component | Not specified in the source documents (NEWAC-RWB-P8-E1001-APP-AC13) |
| TC-E1-001-16 | BR6, BR7 | Component | The version of this story's file: later than every service-baseline version and never 0001 of the legacy line |
| TC-P8-E1001-APP-01 | AC1 | Component | Empty DEV and SIT schemas; schema parameter "recovery" |
| TC-P8-E1001-APP-02 | AC4 | Component | Migration copy with a failing CREATE VIEW v_ace_account |
| TC-P8-E1001-APP-03 | AC5 | Component | Branch with v_ace_account.legacy_bucket; changed type on DF-ACE-018 |
| TC-P8-E1001-APP-04 | AC6 | Component | SIT schema at version 0001 |
| TC-P8-E1001-APP-05 | AC8 | Component | Catalog file of 13 rows without DP09 |
| TC-P8-E1001-APP-06 | AC9 | Component | Catalog file with owner role DP_OWNER and refresh cycle HOURLY |
| TC-P8-E1001-APP-07 | AC10 | Component | Same catalog file loaded twice |

TC-P8-E1001-APP-01 to -07 are the Test Cases v9 rows of AC1, AC4 to AC6 and AC8 to AC10; the other legacy TC IDs are kept, one row each, answered here on the schema side. The legacy level System maps to Component or End to end as shown, and Access maps to Component. The `-ITG` copies belong to RWB-ITG-E1001-ITG and no `-ITG` id is written here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails
- No business value in code: the sources, the match values, the Field IDs and the lengths are specification or list values, and the lists arrive through DP-07 with a version, so a new value needs no migration (BR3, AC11).
- No personal data anywhere: the table holds references, a source, an amount, a date, a match value and a posting reference; every fixture, log line and prompt is synthetic (BR9).
- No cross-schema read and no cross-schema key (DP-01): every statement names `rwb_payment` and no constraint or index points at `public` or another service's schema (BR1, BR5).
- ACE data only through the owner's contract: this service holds no grant on the 30 views and this story reads no ACE data (DP-05, ADR-010; BR8).
- The baseline is never rewritten: the monolith's `V0001`, its 92 tables, its dictionary and its 14 catalog rows keep their version and rows, and this story adds a line rather than editing an applied version (BR7; AC9). It never drops a table in PROD and is forward only (BR6).
- One writer per row and no invented money fact: this story writes no row, so no receipt, match or posting reference can be seeded (BR4, BR10), and no ledger column is copied (BR11).
- One hop and a 2 s timeout on every call to another service, and none at run time here (DP-11); the declaration cannot drift from the dictionary because the conformance test compares both directions (BR2, AC3); and one base and one topic — `/api/recovery/payment/v1` and `rwb.payment.events.v1` with `rwb-payment` in namespace `rwb-recovery` — with no monolith base and no other service's base declared as this service's own.

### 18. Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record, one read path and one owner | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-01, FEAT-RDF-02; FEAT-PAY-01 | All recovery processes | CTL-08; Principle 1; D-RCV-35 U1, U4 | TC-P8-E1001-APP-01, TC-P8-E1001-APP-07, TC-E1-001-02, TC-E1-001-03, TC-E1-001-13 |
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Epic 2, 4; Program, 5.1 | FEAT-RDF-01 | All recovery processes | REQ-RDF-001; D-RCV-35 U1 | TC-P8-E1001-APP-06, TC-E1-001-03, TC-E1-001-12 |

Both requirements are carried only for the schema share: `proceeds` belongs to DP13 Money and closure, whose row is ACE's for the money and the Workbench's for the match (GAP-2539). The catalog, the dictionary and the endpoint are RWB-P1-E1001-APP's, and this story writes none of them. The 9-row field declaration is a build artefact of this story, handed to the one seed through the Change Register; TC-E1-001-02 proves it matched.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1001-APP | App development | The one catalog and dictionary in `rwb_source_data`; this story hands it the declaration and writes no row |
| RWB-PLT-NF06-DB | ACE DB | The schema split — 19 schemas, logins and grants; this story is P8's share (DP-01) |
| RWB-P8-E2008-APP, RWB-P8-E2027-APP | App development | The matching and the match rules that write the first `proceeds` rows, with their record and outbox row |
| RWB-P8-E4043-APP, RWB-P8-E4044-APP, RWB-P8-E4048-APP | App development | The settlement, auction and rental stories that match on the row this table holds |
| RWB-P8-E4043-CON, RWB-P8-E4044-CON, RWB-P8-E2027-CON | Contract | The two operations, the `Proceeds` element group, the three event schemas and the fakes of this table |
| RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-E1047-CON, RWB-PLT-N001-CON | Contract | The baseline: decision-record library, two client libraries, Flyway sequence, naming library and edge route (DP-03, -06, -07, -15, -14, -19) |
| RWB-ITG-E1001-ITG | Integration | The harness of the key; no `-ITG` case is written here |

| Legacy reference | Where it is kept |
|---|---|
| P8's one table of the estate, `proceeds`, with DF-FIN-001 to DF-FIN-009 | Metadata, sections 1, 4, 11, 12.7 |
| The 92-table estate, the 20 tables that left it, the no-`public` rule, the five business keys and the 1,062-field count (legacy AC1) | Sections 1, 2, 7 (AC1, AC9), 8 (BR5, BR7) |
| The dictionary row and its Field ID, type, physical type and product (legacy AC2); the DP13 catalog row (legacy AC3, AC10) | Sections 2, 7 (AC3, AC10), 8 (BR2), 11 |
| A failed statement leaves no partial schema (legacy AC4); the two conformance texts (legacy AC5); a repeat changes nothing (legacy AC6) | Sections 5 (X1, X2, X4), 7 (AC3, AC4, AC5), 8 (BR6), 14 |
| Values reused: `proceeds`, DF-FIN-001 to DF-FIN-009, "DP13", "ACE (ingested from ALS and GL)", "DAILY", "08:00", `LOV-MATCH`, `LOV-PROCEEDS-SRC`, 92 tables, at least 123 `sys_objects`, at least 1,379 `sys_fields`, 14 `data_product`, version 1.001; messages MSG-P1-001, MSG-P8-001, MSG-P8-002, MSG-P4-002, MSG-P7-003, MSG-GEN-001; TCs TC-P8-E1001-APP-01 to TC-P8-E1001-APP-07, TC-E1-001-02, -03, -07, -11, -12; patterns DP01, DP03, DP05, DP06, DP07, DP11, DP14, DP15, DP19 | Sections 3, 7, 11, 12, 13, 14, 16, metadata |

The other slices of the key answer the rest: RWB-P1-E1001-APP the catalog, the data product rows and the one dictionary; RWB-P4-E1001-APP the five authority tables; RWB-P7-E1001-APP the six decision-and-rules tables; RWB-PLT-NF06-DB the 19 schemas, logins and grants; and RWB-ITG-E1001-ITG the cross-service harness and the `-ITG` copies.

### 19. Out of scope
- The other 91 tables of the estate and the DB stories that create them (RWB-PLT-NF06-DB and the per-service DB stories), and the baseline itself: schema `recovery`, its `V0001`, its 92 tables, its dictionary and its 14 data product rows stay as built (BR7).
- The catalog, the data product rows, the dictionary rows, the field versions and the dictionary endpoint: RWB-P1-E1001-APP and RWB-P1-E1064-APP; this story declares its 9 field rows and writes none.
- The 30 read-only ACE views, their grants and the boundary rule (RWB-P1-E1069-APP, RWB-P1-E1069-DB); this service holds no grant on them (DP-05).
- The row writes and the matching: the payment-to-plan matching, the missed-payment event, the exception list, the settlement payment, the auction and enforcement proceeds, the fees, the ALS booking, the ledger post, the rental and the daily reconciliation, which are RWB-P8-E2008-APP, RWB-P8-E2027-APP, RWB-P8-E4043-APP, RWB-P8-E4044-APP and RWB-P8-E4048-APP.
- The two operations (API-P8-001, API-P8-002), the three events, the `Proceeds` element group and the fakes: RWB-P8-E2027-CON, RWB-P8-E4043-CON and RWB-P8-E4044-CON; and the event-started runs of JOB-07: the service's application stories. JOB-08 is covered by rwb-integration.
- The match rules, their packages, versions and evaluation: `rwb-decision` (P7) and the embedded Drools kit (DP-04, RWB-PLT-E1072-CON); `payment_match_rule` is created nowhere (D-RCV-36 T10).
- The case of record and its states, tasks and timers (rwb-case, P3); the treatment (rwb-treatment, S2); the roles, scopes and masking (rwb-access, P4 and the template guard).
- SCR-28 and SCR-29 as built screens and the composite route: the screen stories and RWB-PLT-N001-CON; and the harness RWB-ITG-E1001-ITG with the `-ITG` copies, the Helm chart, the metric, alert and runbook set of the schema (an OPS story of this key).

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
