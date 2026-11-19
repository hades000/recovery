<!-- working-copy-of: requirement/legacy/03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v4_extracted/Recovery Workbench FSD P1 Recovery data engine v2.md -->
> **Working copy.** Canonical source: `requirement/legacy/03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v4_extracted/Recovery Workbench FSD P1 Recovery data engine v2.md`. Edit the source, not this copy.

# Recovery Workbench P1 Recovery data engine

Functional specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P1 Recovery data engine |
| Document ID | P1-RWB-FSD-v2 |
| Version | 2 |
| Status | In review |
| Classification | Confidential |
| Date | 28 October 2026 |
| FSD owner | Business analyst, P1 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| P1 | Recovery data engine | E1 |

**Feature scope.** COLLINS and file loads, load checks, reconciliation, freshness.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P1 Recovery data engine | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | No build in this module |
| Case record and shared entities | REUSE | ACE common module; Case and Workflow Model | Read through the P3 interfaces |
| Notification path | REUSE | ACE notification path | Recovery templates only |
| Workflow and state machine | REUSE | Workflow Engine Design | Stages and sentries from P3 |
| Decision record and audit trail | REUSE | Audit and Logging Design | Writes through P7 |
| Attachments and evidence | REUSE | Document Management Design | Through P5 |
| Role and permission matrix | REUSE | Users Roles and Permissions | Capability areas from P4 |
| Restructure calculator | REUSE | ACE common module | Not used |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** COLLINS and file loads, load checks, reconciliation, freshness.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-DRI-01; FEAT-RDF-01; FEAT-RDF-02; FEAT-RDF-03; FEAT-RDF-03, FEAT-CWC-01; FEAT-RDF-07; FEAT-RDF-08; FEAT-RDF-11

**Constraints.** Built in the ACE service as part of the recovery module; data through COLLINS and file loads; every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P1 | FEAT-RDF-01 | Create the recovery tables in the ACE database | System | Creates the recovery tables in the ACE database, with the schema for the 14 data products. | E1 | A2.1 |
| P1 | FEAT-RDF-02 | Define the 14 data products and their systems of record | Admin | Names each data product, its owner, its system of record and its definition, so one number has one source. | E1 | A2.2 |
| P1 | FEAT-RDF-03 | Load account and arrears daily from ALS | System | Runs the daily batch load of balances, arrears, days past due and classification from ALS into the data store. | E1 | A2.3 |
| P1 | FEAT-RDF-04 | Load collections status and contact history from EFS | System | Takes the daily EFS extract of cases, contacts and promises into the contact and promises data product. | E1 | A2.4 |
| P1 | FEAT-RDF-05 | Load collateral records from CCMS | System | Loads collateral records, title and registration data, and encumbrance status into the collateral data product. | E1 | A2.5 |
| P1 | FEAT-RDF-06 | Load appraisal values from SVAF | System | Loads appraisal values, dates and appraiser into the collateral and valuation data product. | E1 | A2.6 |
| P1 | FEAT-RDF-07 | Inventory the Excel and SharePoint trackers | Admin | Lists every local tracker the recovery teams keep, with its owner, its fields and the feed that will replace it. | E1 | A2.7 |
| P1 | FEAT-RDF-08 | Load the tracker data into the data store | System | Loads the inventoried tracker content into the matching data product so the list stops being local. | E1 | A2.8 |
| P1 | FEAT-RDF-09 | Retire a local tracker copy | Admin | Records that a tracker has been replaced, withdraws the local copy and logs any field no feed carries. | E1 | A2.9 |
| P1 | FEAT-RDF-10 | Run data quality rules on every load | System | Applies the agreed completeness, format and range rules to each load and writes the breaks to an exception list. | E1 | A2.10 |
| P1 | FEAT-RDF-11 | Reconcile the data store to ALS daily | System | Compares balances and case counts in the data store to ALS every day and reports the difference. | E1 | A2.11 |
| P1 | FEAT-RDF-12 | Publish the daily reconciliation and data quality report | System | Produces the daily report of reconciliation results and open data quality breaks for the data steward. | E1 | A2.12 |
| P1 | FEAT-RDF-13 | Hold the publish when reconciliation breaks tolerance | System | Stops the data product being published when the reconciliation difference is over tolerance, and raises the exception list. | E1 | A2.13 |
| P1 | FEAT-RDF-14 | Stamp each data product with its freshness | System | Writes a freshness stamp on every data product so a decision carries the age of the data it used. | E1 | A2.14 |
| P1 | FEAT-RDF-15 | Set access control per data product for PDPA | Admin | Sets who can read each data product and which fields are masked, under the PDPA minimization rule. | E1 | A2.15 |
| P1 | FEAT-RDF-16 | Maintain the data catalog entry per data product | Admin | Keeps the catalog entry for each data product: definition, owner, source, refresh, quality rules and access. | E1 | A2.16 |
| P1 | FEAT-RDF-17 | Apply the retention and archive rule to the data store | Admin | Applies the retention class to each data product and archives records past their period. | E1 | A2.17 |
| P1 | FEAT-RDF-18 | Show the case list with case ID, owner and queue | User | Gives every recovery team one list of all 90 plus days past due accounts across Mortgage, HP and SSME. | E1 | A2.18 |
| P1 | FEAT-RDF-19 | Publish baseline measures for the recovery portfolio | System | Calculates and publishes the starting measures the benefit model is tracked against. | E1 | A2.19 |
| P1 | FEAT-RDF-20 | Copy the decision log to the lake | System | Streams decision log entries to the data lake so reporting and audit read them without touching the log store. | E1 | A2.20 |
| P1 | FEAT-RDF-22 | Run legacy feed jobs on ADF and Control-M | System | Schedules and runs the batch feed jobs that carry data from the legacy systems into the data store. | E1 | A2.21 |

### A1.3 Background

Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Create the recovery tables in the ACE database

#### A2.1.1 Intent

**Business objective.** Creates the recovery tables in the ACE database, with the schema for the 14 data products.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Creates the recovery tables in the ACE database, with the schema for the 14 data products.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Create the recovery tables in the ACE database | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database, ACE

**Prerequisites.** None

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-001-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner, Platform administrator | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-001-01 | Schema deployed | the migration V0001__rwb_e1_001_recovery_schema.sql and the parameter recoverySchema = "recovery" | the pipeline applies it in DEV and then in SIT | the recovery schema in each environment holds 44 tables: the 43 tables of the physical schema and data_product And the table loan_account has the 24 columns DF-ACC-001 to DF-ACC-021 and DF-ACC-029 to DF-ACC-031, plus the 7 standard columns And the conformance test matches the 44 deployed tables against the full dictionary (D-RCV-29: 108 sys_objects rows and 1,256 sys_fields rows) | RWB-E1-001 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-001-01 | Dictionary published | the data dictionary and the data product seed loaded by the migration, and the catalog loaded for DP01 | a developer queries v_data_dictionary for entity "loan_account" and field "days_past_due" | the row holds field ID "DF-ACC-014", data type "NUMBER", physical type "integer" And source system "Core bank (ALS) via COLLINS", source field "DELAY_DAYS" And data product "DP01", refresh cycle "DAILY", owner role "RW-DATASTEW" and the owner user ID of DP01 | RWB-E1-001 |
| AC-ALT-P1-001-02 | One system of record | a catalog load file with the 14 rows DP01 to DP14, each with one system of record and one owner user ID | the reference data administrator loads it with valid from 2026-11-20 | data_product holds 14 rows And each row has exactly one system of record and one owner user ID And the catalog for DP06 names system of record "CCMS" and refresh cycle "WEEKLY" | RWB-E1-001 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-001-01 | Failed migration leaves no partial schema | a copy of the migration in which the statement creating table valuation fails | the pipeline applies it in DEV | the pipeline stage fails and names the failing statement And the recovery schema holds none of the tables of that migration And the Flyway history has no successful row for version 1.001 | RWB-E1-001 |
| AC-EXC-P1-001-02 | Column without a dictionary entry fails the build | a branch that adds the column loan_account.branch_code with no sys_fields row | the conformance test runs in the pipeline | the test fails with "loan_account.branch_code has no data dictionary entry" And a sys_fields row DF-ACC-021 whose column is changed to type text fails the test with "DF-ACC-021 physical type date expected, text found" | RWB-E1-001 |
| AC-EXC-P1-001-03 | Repeated migration has no effect | the migration version 1.001 already applied in SIT | the pipeline runs again in SIT | Flyway reports version 1.001 as already applied And the row counts of sys_objects (41) and sys_fields (413) are unchanged | RWB-E1-001 |
| AC-EXC-P1-001-04 | Catalog row with two systems of record is refused | a catalog load file in which DP06 names system of record "CCMS; SVAF" And DP11 has no owner user ID | the reference data administrator loads it | the load is refused whole with MSG-P1-003 for DP06 and for DP11 And data_product keeps the rows of the version in force | RWB-E1-001 |
| AC-EXC-P1-001-05 | Catalog with a missing product is refused | a catalog load file with 13 rows and no row for DP09 | the reference data administrator loads it | the load is refused whole with MSG-P1-004 naming "DP09" And no row is written | RWB-E1-001 |
| AC-EXC-P1-001-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-001-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-001-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-001-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.2 Define the 14 data products and their systems of record

#### A2.2.1 Intent

**Business objective.** Names each data product, its owner, its system of record and its definition, so one number has one source.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Names each data product, its owner, its system of record and its definition, so one number has one source.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Data steward and data product owner | Opens the screen and define the 14 data products and their systems of record | Checks the role, the capability area and the scope |
| 2 | Data steward and data product owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** ACE database

**Prerequisites.** FEAT-RDF-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-002-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| VR-P1-002-2 | Load refused at a check | MSG-P1-002 The {source} load for {date} was refused: {check}. The previous load is still in use. |
| BR-P1-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| loan_account.account_no | Account number | varchar(20) | Yes | None | No |
| loan_account.contract_no | Contract number | varchar(20) | No | None | No |
| loan_account.product_code | Core bank product code | varchar(10) | Yes | LOV-PRODUCT-CODE | No |
| loan_account.product_category_efs | Product category in EFS | varchar(60) | No | None | No |
| loan_account.business_unit | Owning business unit | varchar(10) | No | LOV-BU | No |
| loan_account.contract_date | Contract date | date | No | None | No |
| loan_account.interest_rate | Contract interest rate, percent | numeric(7,4) | No | None | No |
| loan_account.principal_outstanding | Principal outstanding, baht | numeric(18,2) | Yes | None | No |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| Data steward and data product owner | Primary |
| Center of excellence analyst | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-002-01 | Schema deployed | the migration V0001__rwb_e1_001_recovery_schema.sql and the parameter recoverySchema = "recovery" | the pipeline applies it in DEV and then in SIT | the recovery schema in each environment holds 44 tables: the 43 tables of the physical schema and data_product And the table loan_account has the 24 columns DF-ACC-001 to DF-ACC-021 and DF-ACC-029 to DF-ACC-031, plus the 7 standard columns And the conformance test matches the 44 deployed tables against the full dictionary (D-RCV-29: 108 sys_objects rows and 1,256 sys_fields rows) | RWB-E1-001 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-002-01 | Dictionary published | the data dictionary and the data product seed loaded by the migration, and the catalog loaded for DP01 | a developer queries v_data_dictionary for entity "loan_account" and field "days_past_due" | the row holds field ID "DF-ACC-014", data type "NUMBER", physical type "integer" And source system "Core bank (ALS) via COLLINS", source field "DELAY_DAYS" And data product "DP01", refresh cycle "DAILY", owner role "RW-DATASTEW" and the owner user ID of DP01 | RWB-E1-001 |
| AC-ALT-P1-002-02 | One system of record | a catalog load file with the 14 rows DP01 to DP14, each with one system of record and one owner user ID | the reference data administrator loads it with valid from 2026-11-20 | data_product holds 14 rows And each row has exactly one system of record and one owner user ID And the catalog for DP06 names system of record "CCMS" and refresh cycle "WEEKLY" | RWB-E1-001 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-002-01 | Failed migration leaves no partial schema | a copy of the migration in which the statement creating table valuation fails | the pipeline applies it in DEV | the pipeline stage fails and names the failing statement And the recovery schema holds none of the tables of that migration And the Flyway history has no successful row for version 1.001 | RWB-E1-001 |
| AC-EXC-P1-002-02 | Column without a dictionary entry fails the build | a branch that adds the column loan_account.branch_code with no sys_fields row | the conformance test runs in the pipeline | the test fails with "loan_account.branch_code has no data dictionary entry" And a sys_fields row DF-ACC-021 whose column is changed to type text fails the test with "DF-ACC-021 physical type date expected, text found" | RWB-E1-001 |
| AC-EXC-P1-002-03 | Repeated migration has no effect | the migration version 1.001 already applied in SIT | the pipeline runs again in SIT | Flyway reports version 1.001 as already applied And the row counts of sys_objects (41) and sys_fields (413) are unchanged | RWB-E1-001 |
| AC-EXC-P1-002-04 | Catalog row with two systems of record is refused | a catalog load file in which DP06 names system of record "CCMS; SVAF" And DP11 has no owner user ID | the reference data administrator loads it | the load is refused whole with MSG-P1-003 for DP06 and for DP11 And data_product keeps the rows of the version in force | RWB-E1-001 |
| AC-EXC-P1-002-05 | Catalog with a missing product is refused | a catalog load file with 13 rows and no row for DP09 | the reference data administrator loads it | the load is refused whole with MSG-P1-004 naming "DP09" And no row is written | RWB-E1-001 |
| AC-EXC-P1-002-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-002-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-002-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-002-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.3 Load account and arrears daily from ALS

#### A2.3.1 Intent

**Business objective.** Runs the daily batch load of balances, arrears, days past due and classification from ALS into the data store.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Runs the daily batch load of balances, arrears, days past due and classification from ALS into the data store.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Load account and arrears daily from ALS | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, COLLINS, Control-M

**Prerequisites.** FEAT-RDF-01

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-003-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-003-01 | Daily load | COLLINS completed the staging records for 2026-11-30 at 04:40 with 184,500 INT-01 accounts and 2,310 INT-02 payments, each with a matching trailer | JOB-01 runs at 05:00 | loan_account holds 184,500 rows with data_as_of 2026-11-30 before 07:00 And the load_run for INT-01 shows 184,500 read, 184,500 loaded and 0 held, with status COMPLETED And the load_run for INT-02 shows 2,310 read, 2,310 loaded and 0 held And one LoadCompleted event is in the outbox for each interface with business date 2026-11-30 | RWB-E1-003 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-003-01 | Sample matches | the INT-01 load for 2026-11-30 is complete | the sample check picks 50 accounts at random | for all 50 the total_balance, days_past_due and classification equal the INT-01 staging values after mapping And the load_run check results show "SAMPLE" = "50 of 50" | RWB-E1-003 |
| AC-ALT-P1-003-02 | Wrong business date | the INT-01 staging records and trailer carry business date 2026-11-27 | JOB-01 runs for 2026-11-30 | the load is refused at DQ-001 with MSG-P1-002 naming "business date" And no loan_account row changes | RWB-E1-003 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-003-01 | Failure alerts | the INT-01 trailer states 184,500 records and the staging holds 184,498 | JOB-01 runs | the INT-01 load is refused at DQ-003 and no loan_account row changes And loan_account keeps data_as_of 2026-11-27 And the data steward and platform administrator groups receive MSG-P1-002 "The INT-01 load for 2026-11-30 was refused: control total. The previous load is still in use." And one LoadRefused event is in the outbox with failedCheck "DQ-003" | RWB-E1-003 |
| AC-EXC-P1-003-02 | Duplicate account key | account key "ACC0000017" appears twice in the INT-01 staging records | JOB-01 runs | the load is refused at DQ-004 with MSG-P1-002 naming "keys" And no loan_account row changes | RWB-E1-003 |
| AC-EXC-P1-003-03 | Unmatched payments above the tolerance refuse the load | 13 of the 2,310 INT-02 payments name an account key not in loan_account, which is 0.56 percent | JOB-01 runs | the INT-02 load is refused at DQ-012 with MSG-P1-002 And no account_payment row for 2026-11-30 is written | RWB-E1-003 |
| AC-EXC-P1-003-04 | Code missing from the code map is held | 3 INT-01 records carry bucket code "Z9", which is not in the code map for LOV-BUCKET | JOB-01 runs | the 3 records are held in dq_exception with check code "DQ-006" And 184,497 accounts are loaded | RWB-E1-003 |
| AC-EXC-P1-003-05 | Late delivery | COLLINS has not completed the INT-01 staging records for 2026-11-30 by 09:00 | the last JOB-01 attempt runs at 09:00 | the INT-01 load_run status is LATE and loan_account keeps data_as_of 2026-11-27 And one LoadRefused event is in the outbox with failedCheck "LATE" And the data steward group receives MSG-P1-002 "The INT-01 load for 2026-11-30 was refused: no delivery by 09:00. The previous load is still in use." | RWB-E1-003 |
| AC-EXC-P1-003-06 | Database failure during the write | the database connection is cut after 90,000 of 184,500 accounts are written in the transaction | the write step fails | no loan_account row carries data_as_of 2026-11-30 And the load_run status is FAILED And the attempt at 06:00 loads 184,500 accounts and sets the status to COMPLETED | RWB-E1-003 |
| AC-EXC-P1-003-07 | Rerun after a refused load | the INT-01 load for 2026-11-30 was refused at DQ-003 And COLLINS has delivered corrected staging records with a matching trailer | the platform administrator calls POST /admin/jobs/{jobId}/rerun for that load | the response is 200 with a Job of status RUNNING And the load completes with 184,500 accounts and one LoadCompleted event is in the outbox | RWB-E1-003 |
| AC-EXC-P1-003-08 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-003-09 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-003-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-003-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.4 Load collections status and contact history from EFS

#### A2.4.1 Intent

**Business objective.** Takes the daily EFS extract of cases, contacts and promises into the contact and promises data product.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Takes the daily EFS extract of cases, contacts and promises into the contact and promises data product.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Load collections status and contact history from EFS | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** EFS, COLLINS

**Prerequisites.** FEAT-RDF-01

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-004-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-004-01 | Start-of-day file | COLLINS completes the INT-07 staging records at 06:30 with 9,450 contact records for 2026-11-30 and a matching trailer | the JOB-01 attempt at 07:00 runs the INT-07 step | collections_history holds 9,450 new rows with business date 2026-11-30, of which 1,320 carry a promise amount and date And the INT-07 load_run shows 9,450 read, 9,450 loaded, status COMPLETED And after the case list step, the row of case "RW-2026-000123" shows last contact 2026-11-30 15:42 and action code "PTP" | RWB-E1-004 |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-004-01 | Mapping signed | the INT-07 load for 2026-11-30 is COMPLETED | the data steward calls GET /admin/jobs with type "INT-07" and from 2026-11-30 | the Job shows mapping version "EFS-MAP-1" And the mapping version in source_field_map carries approved_on 2026-11-18 and approval reference "EFS-SIGN-2026-11-18" | RWB-E1-004 |
| AC-ALT-P1-004-02 | Unknown account keys within the tolerance | 40 of the 9,450 records name an account key not in loan_account, which is 0.42 percent | the INT-07 step runs | 9,410 rows are written And 40 dq_exception rows are written with check code "DQ-040" | RWB-E1-004 |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-004-01 | Late file | COLLINS has not completed the INT-07 staging records for 2026-11-30 by 08:00 | the INT-07 window check runs at 08:00 | the INT-07 load_run status is LATE And one LoadRefused event is in the outbox with failedCheck "LATE" And FreshnessQuery returns DP05 with business date 2026-11-27 and status STALE And the data steward group receives MSG-P1-001 "DP05 Interaction is from 2026-11-27. Today's load has not arrived." And collections_history keeps every row for 2026-11-27 unchanged | RWB-E1-004 |
| AC-EXC-P1-004-02 | Mapping not approved | the INT-07 mapping version in force is "EFS-MAP-2" with no approval | the INT-07 step runs | the load is refused with MSG-P1-002 "The INT-07 load for 2026-11-30 was refused: mapping version EFS-MAP-2 not approved. The previous load is still in use." And no collections_history row is written | RWB-E1-004 |
| AC-EXC-P1-004-03 | Code missing from the code map | 6 records carry call result "R99", which is not in the code map for LOV-CONTACT-RESULT | the INT-07 step runs | the 6 records are held in dq_exception with check code "DQ-041" And 9,444 rows are written | RWB-E1-004 |
| AC-EXC-P1-004-04 | Blocking check fails | the INT-07 staging records have no column "Call Result" | the INT-07 step runs | the load is refused at DQ-037 with MSG-P1-002 naming "structure" And one LoadRefused event is in the outbox with failedCheck "DQ-037" | RWB-E1-004 |
| AC-EXC-P1-004-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-004-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-004-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-004-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.5 Load collateral records from CCMS

#### A2.5.1 Intent

**Business objective.** Loads collateral records, title and registration data, and encumbrance status into the collateral data product.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Loads collateral records, title and registration data, and encumbrance status into the collateral data product.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Load collateral records from CCMS | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** CCMS

**Prerequisites.** FEAT-RDF-01

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-005-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-005-01 | Daily load of the weekly files | the adapter has passed the CCMS file with 31,200 collateral records and 33,050 account links, and the SVAF file with 2,140 appraisals | JOB-09 calls the CCMS and SVAF loaders at 04:00 | collateral holds 31,200 rows from the file and account_collateral holds 33,050 links to loan_account rows And valuation holds 2,140 appraisals written through ValuationRecordApi, each linked to its collateral And an appraisal date "15/03/2569" in the file is stored as 2026-03-15 And both load_runs show status COMPLETED and FreshnessQuery returns DP06 with business date 2026-11-27 | RWB-E1-009 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-005-01 | Sample matches | both loads for 2026-11-27 are complete | the sample check picks 50 cases at random that have collateral | for all 50 the collateral type, the title deed number and the latest appraised value equal the CCMS and SVAF file values after mapping And the INT-11 load_run check results show "SAMPLE" = "50 of 50" | RWB-E1-009 |
| AC-ALT-P1-005-02 | Appraisal age | appraisal "APR-0045521" has appraisal date 2025-11-26, which is 366 days before 2026-11-27 And appraisal "APR-0045522" has appraisal date 2025-11-27, which is 365 days before 2026-11-27 | the SVAF loader runs | "APR-0045521" is stored with stale_flag true and age_days 366 And "APR-0045522" is stored with stale_flag false and age_days 365 | RWB-E1-009 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-005-01 | CCMS file refused by the adapter | the adapter refuses the CCMS file for 2026-11-27 at DQ-059 control total | JOB-09 runs | the CCMS loader is not called and no collateral or account_collateral row changes And the SVAF loader is still called, and appraisals for collateral not yet in DP06 are held with check code "DQ-068" | RWB-E1-009 |
| AC-EXC-P1-005-02 | Appraisal for an unknown collateral | 4 appraisals name collateral numbers not in collateral | the SVAF loader runs | the 4 appraisals are held in dq_exception with check code "DQ-068" And 2,136 appraisals are written | RWB-E1-009 |
| AC-EXC-P1-005-03 | Collateral type missing from the code map | 2 CCMS records carry collateral type code "K7", which is not in the code map for LOV-COLL-TYPE | the CCMS loader runs | the 2 records are held in dq_exception with check code "DQ-062" And 31,198 collateral rows are written | RWB-E1-009 |
| AC-EXC-P1-005-04 | Unknown references above the tolerance | 180 of the 33,050 account links name an account key not in loan_account, which is 0.54 percent | the CCMS loader runs | the INT-10 load is refused at DQ-061 and no collateral or account_collateral row changes And one LoadRefused event is in the outbox with failedCheck "DQ-061" And the data steward group receives MSG-P1-002 "The INT-10 load for 2026-11-27 was refused: references. The previous load is still in use." | RWB-E1-009 |
| AC-EXC-P1-005-05 | SVAF file not received | no SVAF file for 2026-11-27 has passed the adapter by Tuesday 2026-12-01 04:00 | the data steward lists the jobs for INT-11 | there is no INT-11 load_run for 2026-11-27 and valuation keeps the appraisals of 2026-11-20 And FreshnessQuery returns DP06 with status STALE, and the data steward group has received MSG-P1-001 from the freshness check | RWB-E1-009 |
| AC-EXC-P1-005-06 | Valuation write fails | ValuationRecordApi raises an error after 1,000 of 2,140 appraisals | the SVAF loader runs | no appraisal from the file is stored And the INT-11 load_run status is FAILED And a rerun by the platform administrator stores 2,140 appraisals | RWB-E1-009 |
| AC-EXC-P1-005-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-005-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-005-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-005-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.6 Load appraisal values from SVAF

#### A2.6.1 Intent

**Business objective.** Loads appraisal values, dates and appraiser into the collateral and valuation data product.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Loads appraisal values, dates and appraiser into the collateral and valuation data product.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Load appraisal values from SVAF | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** SVAF

**Prerequisites.** FEAT-RDF-01

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-006-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-006-01 | Daily load of the weekly files | the adapter has passed the CCMS file with 31,200 collateral records and 33,050 account links, and the SVAF file with 2,140 appraisals | JOB-09 calls the CCMS and SVAF loaders at 04:00 | collateral holds 31,200 rows from the file and account_collateral holds 33,050 links to loan_account rows And valuation holds 2,140 appraisals written through ValuationRecordApi, each linked to its collateral And an appraisal date "15/03/2569" in the file is stored as 2026-03-15 And both load_runs show status COMPLETED and FreshnessQuery returns DP06 with business date 2026-11-27 | RWB-E1-009 |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-006-01 | Sample matches | both loads for 2026-11-27 are complete | the sample check picks 50 cases at random that have collateral | for all 50 the collateral type, the title deed number and the latest appraised value equal the CCMS and SVAF file values after mapping And the INT-11 load_run check results show "SAMPLE" = "50 of 50" | RWB-E1-009 |
| AC-ALT-P1-006-02 | Appraisal age | appraisal "APR-0045521" has appraisal date 2025-11-26, which is 366 days before 2026-11-27 And appraisal "APR-0045522" has appraisal date 2025-11-27, which is 365 days before 2026-11-27 | the SVAF loader runs | "APR-0045521" is stored with stale_flag true and age_days 366 And "APR-0045522" is stored with stale_flag false and age_days 365 | RWB-E1-009 |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-006-01 | CCMS file refused by the adapter | the adapter refuses the CCMS file for 2026-11-27 at DQ-059 control total | JOB-09 runs | the CCMS loader is not called and no collateral or account_collateral row changes And the SVAF loader is still called, and appraisals for collateral not yet in DP06 are held with check code "DQ-068" | RWB-E1-009 |
| AC-EXC-P1-006-02 | Appraisal for an unknown collateral | 4 appraisals name collateral numbers not in collateral | the SVAF loader runs | the 4 appraisals are held in dq_exception with check code "DQ-068" And 2,136 appraisals are written | RWB-E1-009 |
| AC-EXC-P1-006-03 | Collateral type missing from the code map | 2 CCMS records carry collateral type code "K7", which is not in the code map for LOV-COLL-TYPE | the CCMS loader runs | the 2 records are held in dq_exception with check code "DQ-062" And 31,198 collateral rows are written | RWB-E1-009 |
| AC-EXC-P1-006-04 | Unknown references above the tolerance | 180 of the 33,050 account links name an account key not in loan_account, which is 0.54 percent | the CCMS loader runs | the INT-10 load is refused at DQ-061 and no collateral or account_collateral row changes And one LoadRefused event is in the outbox with failedCheck "DQ-061" And the data steward group receives MSG-P1-002 "The INT-10 load for 2026-11-27 was refused: references. The previous load is still in use." | RWB-E1-009 |
| AC-EXC-P1-006-05 | SVAF file not received | no SVAF file for 2026-11-27 has passed the adapter by Tuesday 2026-12-01 04:00 | the data steward lists the jobs for INT-11 | there is no INT-11 load_run for 2026-11-27 and valuation keeps the appraisals of 2026-11-20 And FreshnessQuery returns DP06 with status STALE, and the data steward group has received MSG-P1-001 from the freshness check | RWB-E1-009 |
| AC-EXC-P1-006-06 | Valuation write fails | ValuationRecordApi raises an error after 1,000 of 2,140 appraisals | the SVAF loader runs | no appraisal from the file is stored And the INT-11 load_run status is FAILED And a rerun by the platform administrator stores 2,140 appraisals | RWB-E1-009 |
| AC-EXC-P1-006-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-006-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-006-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-006-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.7 Inventory the Excel and SharePoint trackers

#### A2.7.1 Intent

**Business objective.** Lists every local tracker the recovery teams keep, with its owner, its fields and the feed that will replace it.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Lists every local tracker the recovery teams keep, with its owner, its fields and the feed that will replace it.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Data steward and data product owner | Opens the screen and inventory the Excel and SharePoint trackers | Checks the role, the capability area and the scope |
| 2 | Data steward and data product owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** SharePoint, Excel

**Prerequisites.** None

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-007-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P1-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| loan_account.account_no | Account number | varchar(20) | Yes | None | No |
| loan_account.contract_no | Contract number | varchar(20) | No | None | No |
| loan_account.product_code | Core bank product code | varchar(10) | Yes | LOV-PRODUCT-CODE | No |
| loan_account.product_category_efs | Product category in EFS | varchar(60) | No | None | No |
| loan_account.business_unit | Owning business unit | varchar(10) | No | LOV-BU | No |
| loan_account.contract_date | Contract date | date | No | None | No |
| loan_account.interest_rate | Contract interest rate, percent | numeric(7,4) | No | None | No |
| loan_account.principal_outstanding | Principal outstanding, baht | numeric(18,2) | Yes | None | No |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| Data steward and data product owner | Primary |
| Center of excellence analyst, Team manager | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-007-01 | Inventory covers six teams | an inventory file "TRK-2026.11" with 23 rows: 5 for TDR, 3 for DIL, 6 for LIT, 4 for NPA, 2 for DEBT_SALE and 3 for WRITE_OFF And each row has tracker code, tracker name, location type, location, owner user ID, field list, update cycle, decision and reason | the reference data administrator loads it and the data steward confirms it | tracker_inventory holds 23 rows for version "TRK-2026.11" And GET /admin/trackers with team "LIT" returns 6 trackers, among them "LIT-07 Litigation case tracker" on SharePoint, update cycle WEEKLY, with its owner and 18 fields | RWB-E1-005 |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-007-01 | Decision per file | the loaded version "TRK-2026.11" | the data steward calls GET /admin/trackers | every one of the 23 trackers has a decision LOAD, RETIRE or KEEP and a reason And the 14 LOAD trackers each name a target data product, for example "LIT-07" names DP07 And the 14 LOAD and 6 RETIRE trackers have status LISTED and the 3 KEEP trackers have status KEPT | RWB-E1-005 |
| AC-ALT-P1-007-02 | A row without a decision | an inventory file whose row 7 has no decision | the reference data administrator loads it | the load is refused whole with MSG-GEN-001 "Enter decision." for row 7 | RWB-E1-005 |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-007-01 | A team is missing | an inventory file with no row for team DEBT_SALE | the reference data administrator loads it | the load is refused whole with MSG-P1-016 "The inventory has no row for team DEBT_SALE. List its trackers, or add one row with location type NONE." And no tracker_inventory row is written | RWB-E1-005 |
| AC-EXC-P1-007-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-007-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-007-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-007-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.8 Load the tracker data into the data store

#### A2.8.1 Intent

**Business objective.** Loads the inventoried tracker content into the matching data product so the list stops being local.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Loads the inventoried tracker content into the matching data product so the list stops being local.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Load the tracker data into the data store | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** SharePoint, ACE database

**Prerequisites.** FEAT-RDF-07

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-008-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-008-01 | File loaded | the file "LIT-07 Litigation tracker 2026-11-20.xlsx" with 1,240 rows, each with an account number found in loan_account | the data steward calls POST /admin/trackers/{trackerId}/loads with the file | the response is 202 with a Job of type "TRACKER" and status RUNNING And tracker_row holds 1,240 rows for LIT-07 with target data product DP07 and source file name "LIT-07 Litigation tracker 2026-11-20.xlsx" And the tracker shows 1,240 file rows, 1,240 loaded, 0 rejected and status LOADED | RWB-E1-010 |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-008-01 | Reconciled | the LIT-07 load shows 1,240 file rows, 1,240 loaded and 0 rejected | the team manager of team LIT calls POST /admin/trackers/{trackerId}/sign-off with confirmed row count 1,240 | the tracker status is SIGNED_OFF with the team manager's user ID and the sign-off time | RWB-E1-010 |
| AC-ALT-P1-008-02 | Rejected rows | the LIT-07 file has 1,240 rows, of which 17 have no account number | the load runs | 1,223 rows are written to tracker_row And 17 dq_exception rows are written with check code "TRK-01" and record keys "LIT-07 row 14" to "LIT-07 row 1,205" And the data steward and the LIT team manager receive MSG-P1-008 "1,223 rows loaded from LIT-07 Litigation tracker 2026-11-20.xlsx. 17 rows rejected; the reject list is on the load." And GET /admin/data-quality/exceptions with product "DP07" returns the 17 rejected rows | RWB-E1-010 |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-008-01 | Account number not found | 5 rows of the LIT-07 file carry account numbers not in loan_account | the load runs | the 5 rows are rejected with check code "TRK-02" And 1,235 rows are written | RWB-E1-010 |
| AC-EXC-P1-008-02 | Counts do not match at sign-off | the LIT-07 load shows 1,240 file rows, 1,223 loaded and 17 rejected | the team manager of team LIT signs off with confirmed row count 1,251 | the sign-off is refused with MSG-P1-009 "The counts do not match: 1,251 rows confirmed, 1,240 rows in the file, 1,223 loaded, 17 rejected. Sign-off is not allowed." And the tracker status stays LOADED | RWB-E1-010 |
| AC-EXC-P1-008-03 | The person who loaded cannot sign off | a user who holds RW-DATASTEW and RW-TEAMMGR for team LIT loaded the LIT-07 file | the same user signs off | the sign-off is refused with MSG-P7-002 "You prepared this decision, so you cannot approve it." | RWB-E1-010 |
| AC-EXC-P1-008-04 | File type not allowed | a file "LIT-07 tracker.pdf" | the data steward uploads it for LIT-07 | the response is 415 with MSG-P1-018 "Use an .xlsx or .csv file of at most 20 MB for a tracker load." | RWB-E1-010 |
| AC-EXC-P1-008-05 | Header does not match the field list | the LIT-07 file has no column "Court name", which is in the field list | the load runs | the load is refused at structure with MSG-P1-002 "The LIT-07 load for 2026-11-20 was refused: structure. The previous load is still in use." And no tracker_row for that file is written | RWB-E1-010 |
| AC-EXC-P1-008-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-008-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-008-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-008-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.9 Retire a local tracker copy

#### A2.9.1 Intent

**Business objective.** Records that a tracker has been replaced, withdraws the local copy and logs any field no feed carries.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Records that a tracker has been replaced, withdraws the local copy and logs any field no feed carries.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Data steward and data product owner | Opens the screen and retire a local tracker copy | Checks the role, the capability area and the scope |
| 2 | Data steward and data product owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** SharePoint

**Prerequisites.** FEAT-RDF-08

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-009-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P1-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| loan_account.account_no | Account number | varchar(20) | Yes | None | No |
| loan_account.contract_no | Contract number | varchar(20) | No | None | No |
| loan_account.product_code | Core bank product code | varchar(10) | Yes | LOV-PRODUCT-CODE | No |
| loan_account.product_category_efs | Product category in EFS | varchar(60) | No | None | No |
| loan_account.business_unit | Owning business unit | varchar(10) | No | LOV-BU | No |
| loan_account.contract_date | Contract date | date | No | None | No |
| loan_account.interest_rate | Contract interest rate, percent | numeric(7,4) | No | None | No |
| loan_account.principal_outstanding | Principal outstanding, baht | numeric(18,2) | Yes | None | No |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| Data steward and data product owner | Primary |
| Team manager | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-009-01 | Team confirmation | the LIT team has worked from the case list on Monday 2026-11-23 and Tuesday 2026-11-24 | the LIT team manager calls POST /admin/trackers/{trackerId}/retire on 2026-11-25 with archive location "https://sharepoint.example/sites/lit/archive/LIT-07" | the tracker status is RETIRED with retired_at 2026-11-25, the team manager's user ID and the archive location And the stored tracker file in the write-once store is kept unchanged | RWB-E1-012 |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-009-01 | Archive location | LIT-07 was retired on 2026-11-25 | the data steward calls GET /admin/trackers with status RETIRED | the row for LIT-07 shows archive location "https://sharepoint.example/sites/lit/archive/LIT-07", retired on 2026-11-25, the confirming user and the stored file reference And it lists the 3 fields "Hearing note", "Firm contact" and "Court room" as fields no feed carries | RWB-E1-012 |
| AC-ALT-P1-009-02 | Business sign-off | the six teams TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF have retired all their LOAD and RETIRE trackers by 2026-11-26 | the Tribe lead calls GET /admin/trackers/retirement-report on 2026-11-26 | the report holds six team rows, each with the number of trackers, the number retired, the team manager who confirmed each retirement and the date And every team row shows outstanding 0 And the report is filed with the release checklist of 30 November 2026 | RWB-E1-012 |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-009-01 | Tracker not signed off | tracker "NPA-02 Asset holding list" has decision LOAD and status LOADED | the NPA team manager calls the retirement for NPA-02 | the retirement is refused with MSG-P1-013 "NPA-02 cannot be retired: its decision is LOAD and its status is LOADED." | RWB-E1-012 |
| AC-EXC-P1-009-02 | Parallel period not yet complete | LIT-07 was signed off on 2026-11-20 | the LIT team manager calls the retirement on Monday 2026-11-23 | the retirement is refused with MSG-P1-014 "LIT-07 can be retired from 2026-11-25, after 2 working days of use of the case list." And the status stays SIGNED_OFF | RWB-E1-012 |
| AC-EXC-P1-009-03 | No archive location | LIT-07 can be retired | the LIT team manager calls the retirement with no archive location | the response is 400 with MSG-GEN-001 "Enter archive location." | RWB-E1-012 |
| AC-EXC-P1-009-04 | Retirement repeated | LIT-07 was retired on 2026-11-25 | the LIT team manager calls the retirement again on 2026-11-26 | the response is 200 with retired_at 2026-11-25 and no field changes | RWB-E1-012 |
| AC-EXC-P1-009-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-009-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-009-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-009-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.10 Run data quality rules on every load

#### A2.10.1 Intent

**Business objective.** Applies the agreed completeness, format and range rules to each load and writes the breaks to an exception list.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Applies the agreed completeness, format and range rules to each load and writes the breaks to an exception list.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run data quality rules on every load | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database

**Prerequisites.** FEAT-RDF-03

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-010-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-010-01 | Rules run daily | the case list for 2026-11-30 holds three accounts "ACC0000301", "ACC0000302" and "ACC0000303", each linked to two open cases | the case list step of JOB-04 completes and the rules for DP03 run | three dq_exception rows are written with check code and reason code "DQ02", rule version "DQR-2026.11" and raised_on 2026-11-30 And GET /admin/data-quality/exceptions with product "DP03" and from 2026-11-30 returns the three rows And the load_run check results show "DQ02" = 3 | RWB-E1-006 |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-010-01 | Report in Power BI | the rules for 2026-11-30 wrote 3 DQ02, 14 DQ05 and 2 DQ06 exceptions | the JOB-04 publish step writes the data quality extract for 2026-11-30 | the extract holds 19 rows with rule code, rule name, data product, business date and record key And the Power BI data quality report shows failures by rule, by data product and by day for 2026-11-30 | RWB-E1-006 |
| AC-ALT-P1-010-02 | Rule as data | the reference data administrator loads rule version "DQR-2026.12" adding rule DQ11 of type RANGE on loan_account.interest_rate with maximum 30.0000, valid from 2026-12-01 And the data steward approves the version | the INT-01 load for 2026-12-01 completes | DQ11 runs with no deployment and writes 2 exceptions for the 2 accounts with interest rate 32.5000 And DQ01 to DQ10 run unchanged | RWB-E1-006 |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-010-01 | One rule fails at run time | the statement for DQ05 times out after the 60 second limit | the rules for DP03 run | DQ05 is shown as ERROR on the load_run and the other rules for DP03 write their exceptions And the data steward group receives MSG-P1-015 "Rule DQ05 did not run for 2026-11-30: statement timeout. The other rules ran." | RWB-E1-006 |
| AC-EXC-P1-010-02 | Exception cleared when the record passes | an OPEN DQ01 exception for case account "ACC0000777" raised on 2026-11-27 And the case of "ACC0000777" now has an owner | the rules for DP03 run for 2026-11-30 | the exception is set CLEARED with cleared_on 2026-11-30 | RWB-E1-006 |
| AC-EXC-P1-010-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-010-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-010-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-010-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.11 Reconcile the data store to ALS daily

#### A2.11.1 Intent

**Business objective.** Compares balances and case counts in the data store to ALS every day and reports the difference.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Compares balances and case counts in the data store to ALS every day and reports the difference.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Reconcile the data store to ALS daily | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, ACE database

**Prerequisites.** FEAT-RDF-03

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-011-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-011-01 | Variance under limit | the ALS accounts at 90 days past due or more less the exclusions are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903 And the case list rows at 90 days past due or more are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, with equal balance sums | the reconciliation step of JOB-04 runs | six reconciliation_result rows are written, REC-01 and REC-02 for each product, each with variance 0 and result PASS And the case list extract for 2026-11-30 is released for publish And the report after the 07:30 refresh shows all three products green | RWB-E1-011 |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-011-01 | Variance over limit | the ALS count for SSME is 2,903 and the case list holds 2,891 SSME rows at 90 days past due or more, a variance of 12 accounts, 0.41 percent | the reconciliation step runs | the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41 And 12 dq_exception rows are written with check code "REC-01" and the 12 account numbers And the case list publish for 2026-11-30 is held and the lake keeps the case list of 2026-11-27 And the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ALS for SSME: a difference of 12 accounts, 0.41 percent." And the report shows SSME red with the 12 break rows, and MORTGAGE and HIRE_PURCHASE green | RWB-E1-011 |
| AC-ALT-P1-011-02 | Variance equal to the tolerance | the parameter recon.tolerance.pct for REC-01 is changed by a reference load to 0.10 from 2026-11-30 And the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent | the reconciliation step runs | the MORTGAGE result is PASS and the SSME result is BREAK | RWB-E1-011 |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-011-01 | Account data not loaded | the INT-01 load for 2026-11-30 is LATE and not COMPLETED | JOB-04 reaches the reconciliation step | no reconciliation_result for 2026-11-30 is written And the case list publish for 2026-11-30 is held And the report shows every product as not run with the reason "DP01 is from 2026-11-27" | RWB-E1-011 |
| AC-EXC-P1-011-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-011-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-011-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-011-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.12 Publish the daily reconciliation and data quality report

#### A2.12.1 Intent

**Business objective.** Produces the daily report of reconciliation results and open data quality breaks for the data steward.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Produces the daily report of reconciliation results and open data quality breaks for the data steward.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Publish the daily reconciliation and data quality report | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Power BI, Data lake

**Prerequisites.** FEAT-RDF-11

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-012-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner, Reporting and BI analyst | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-012-01 | Variance under limit | the ALS accounts at 90 days past due or more less the exclusions are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903 And the case list rows at 90 days past due or more are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, with equal balance sums | the reconciliation step of JOB-04 runs | six reconciliation_result rows are written, REC-01 and REC-02 for each product, each with variance 0 and result PASS And the case list extract for 2026-11-30 is released for publish And the report after the 07:30 refresh shows all three products green | RWB-E1-011 |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-012-01 | Variance over limit | the ALS count for SSME is 2,903 and the case list holds 2,891 SSME rows at 90 days past due or more, a variance of 12 accounts, 0.41 percent | the reconciliation step runs | the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41 And 12 dq_exception rows are written with check code "REC-01" and the 12 account numbers And the case list publish for 2026-11-30 is held and the lake keeps the case list of 2026-11-27 And the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ALS for SSME: a difference of 12 accounts, 0.41 percent." And the report shows SSME red with the 12 break rows, and MORTGAGE and HIRE_PURCHASE green | RWB-E1-011 |
| AC-ALT-P1-012-02 | Variance equal to the tolerance | the parameter recon.tolerance.pct for REC-01 is changed by a reference load to 0.10 from 2026-11-30 And the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent | the reconciliation step runs | the MORTGAGE result is PASS and the SSME result is BREAK | RWB-E1-011 |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-012-01 | Account data not loaded | the INT-01 load for 2026-11-30 is LATE and not COMPLETED | JOB-04 reaches the reconciliation step | no reconciliation_result for 2026-11-30 is written And the case list publish for 2026-11-30 is held And the report shows every product as not run with the reason "DP01 is from 2026-11-27" | RWB-E1-011 |
| AC-EXC-P1-012-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-012-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-012-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-012-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.13 Hold the publish when reconciliation breaks tolerance

#### A2.13.1 Intent

**Business objective.** Stops the data product being published when the reconciliation difference is over tolerance, and raises the exception list.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Stops the data product being published when the reconciliation difference is over tolerance, and raises the exception list.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Hold the publish when reconciliation breaks tolerance | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database

**Prerequisites.** FEAT-RDF-11

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-013-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-013-01 | Variance under limit | the ALS accounts at 90 days past due or more less the exclusions are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903 And the case list rows at 90 days past due or more are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, with equal balance sums | the reconciliation step of JOB-04 runs | six reconciliation_result rows are written, REC-01 and REC-02 for each product, each with variance 0 and result PASS And the case list extract for 2026-11-30 is released for publish And the report after the 07:30 refresh shows all three products green | RWB-E1-011 |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-013-01 | Variance over limit | the ALS count for SSME is 2,903 and the case list holds 2,891 SSME rows at 90 days past due or more, a variance of 12 accounts, 0.41 percent | the reconciliation step runs | the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41 And 12 dq_exception rows are written with check code "REC-01" and the 12 account numbers And the case list publish for 2026-11-30 is held and the lake keeps the case list of 2026-11-27 And the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ALS for SSME: a difference of 12 accounts, 0.41 percent." And the report shows SSME red with the 12 break rows, and MORTGAGE and HIRE_PURCHASE green | RWB-E1-011 |
| AC-ALT-P1-013-02 | Variance equal to the tolerance | the parameter recon.tolerance.pct for REC-01 is changed by a reference load to 0.10 from 2026-11-30 And the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent | the reconciliation step runs | the MORTGAGE result is PASS and the SSME result is BREAK | RWB-E1-011 |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-013-01 | Account data not loaded | the INT-01 load for 2026-11-30 is LATE and not COMPLETED | JOB-04 reaches the reconciliation step | no reconciliation_result for 2026-11-30 is written And the case list publish for 2026-11-30 is held And the report shows every product as not run with the reason "DP01 is from 2026-11-27" | RWB-E1-011 |
| AC-EXC-P1-013-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-013-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-013-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-013-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.14 Stamp each data product with its freshness

#### A2.14.1 Intent

**Business objective.** Writes a freshness stamp on every data product so a decision carries the age of the data it used.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Writes a freshness stamp on every data product so a decision carries the age of the data it used.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Stamp each data product with its freshness | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database

**Prerequisites.** FEAT-RDF-02

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-014-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-014-01 | Freshness on the row | the account and arrears product for business date 2026-11-30 loaded at 06:50 on 2026-12-01 from an extract taken at 23:30 on 2026-11-30 And loan account "ACC-SYN-000101" has data_as_of 2026-11-30 | the row is read through FreshnessQuery.stampForRow("DP01", 2026-11-30) and GET /data-products/freshness?product=DP01 | the row carries source time 2026-11-30T23:30+07:00 and load time 2026-12-01T06:50+07:00 And the status is "LOADED" | RWB-E1-015 |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-014-01 | Stale product flagged | no DP01 load for business date 2026-11-30 exists at 08:00 on 2026-12-01 | the freshness step runs at 08:00 | the product is flagged "STALE" And a data quality exception with product "DP01" and check "FRESHNESS" is raised on 2026-12-01 And the alert goes to the operations channel And the case record view shows the stamp in the data panel with "Account and arrears is from 2026-11-30. Today's load has not arrived." | RWB-E1-015 |
| AC-ALT-P1-014-02 | Freshness in the decision log | a decision log entry for case "RW-2026-000101" read DP01 for 2026-11-30 and DP06 for 2026-11-23 | the entry and its inputs snapshot are read | the snapshot lists DP01 with load time 2026-12-01T06:50+07:00 and status "LOADED" And the snapshot lists DP06 with load time 2026-11-24T04:40+07:00 and status "LOADED" | RWB-E1-015 |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-014-01 | A refused load marks the product stale at once | the DP01 load for 2026-11-30 is refused at check "Control totals" at 05:20 | LoadRefused is processed | DP01 is "STALE" from 05:20 And the stamp for business date 2026-11-30 stays the one in use | RWB-E1-015 |
| AC-EXC-P1-014-02 | A late load clears the stale flag | DP01 was flagged "STALE" at 08:00 on 2026-12-01 | the DP01 load for 2026-11-30 commits at 08:40 | DP01 status is "LOADED" with load time 2026-12-01T08:40+07:00 And the FRESHNESS exception for DP01 on 2026-12-01 is closed | RWB-E1-015 |
| AC-EXC-P1-014-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-014-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-014-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-014-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.15 Set access control per data product for PDPA

#### A2.15.1 Intent

**Business objective.** Sets who can read each data product and which fields are masked, under the PDPA minimization rule.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Sets who can read each data product and which fields are masked, under the PDPA minimization rule.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Data steward and data product owner | Opens the screen and set access control per data product for PDPA | Checks the role, the capability area and the scope |
| 2 | Data steward and data product owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** ACE database, Entra ID

**Prerequisites.** FEAT-RDF-02

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-015-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| loan_account.account_no | Account number | varchar(20) | Yes | None | No |
| loan_account.contract_no | Contract number | varchar(20) | No | None | No |
| loan_account.product_code | Core bank product code | varchar(10) | Yes | LOV-PRODUCT-CODE | No |
| loan_account.product_category_efs | Product category in EFS | varchar(60) | No | None | No |
| loan_account.business_unit | Owning business unit | varchar(10) | No | LOV-BU | No |
| loan_account.contract_date | Contract date | date | No | None | No |
| loan_account.interest_rate | Contract interest rate, percent | numeric(7,4) | No | None | No |
| loan_account.principal_outstanding | Principal outstanding, baht | numeric(18,2) | Yes | None | No |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| Data steward and data product owner | Primary |
| Compliance and PDPA officer, Security administrator | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-015-01 | Role access | user "u-audit-01" holds read-only role RW-AUDIT, which reads DP02 | the user calls GET /data-products/DP02/records?caseId=RW-2026-000102 | the mobile number shows as "******5678" and the national ID token is returned as "MASKED" And the PII access log holds one entry with user "u-audit-01", product "DP02", case "RW-2026-000102" and the time of the read | RWB-E1-016 |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-015-01 | Catalog entry | the 14 data products DP01 to DP14 | a data steward calls GET /admin/data-products | 14 entries are returned And each has an owner role, a system of record, a refresh cycle, an expected-by time, a retention class and the field list with PDPA tags And the DP02 entry lists 20 fields of which 9 are tagged personal | RWB-E1-016 |
| AC-ALT-P1-015-02 | Access denied | user "u-phone-01" holds RW-PHONECOL, which has no access row for DP06 | the user calls GET /data-products/DP06/records?caseId=RW-2026-000102 | the call is refused with status 403 and MSG-P4-002 And the refusal is written to the access log with user "u-phone-01" and product "DP06" | RWB-E1-016 |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-015-01 | An access load with an unknown role is refused | an access load version "DPA-2026.12" with a row for role "RW-UNKNOWN" and product "DP02" | the load is validated | the load is refused whole with MSG-P1-002 and check "unknown role RW-UNKNOWN" And version "DPA-2026.11" stays in force | RWB-E1-016 |
| AC-EXC-P1-015-02 | No masking rule loaded keeps every personal field masked | user "u-comply-01" holds RW-COMPLY, which reads DP02 | the user calls GET /data-products/DP02/records?caseId=RW-2026-000102 | first_name, last_name, cif_no, date_of_birth and the contact value are returned masked | RWB-E1-016 |
| AC-EXC-P1-015-03 | The PII access log is unavailable | the PII access log rejects every write | user "u-audit-01" calls GET /data-products/DP02/records?caseId=RW-2026-000102 | the call is refused with status 503 and MSG-GEN-006 for system "PII access log" And no personal field is returned | RWB-E1-016 |
| AC-EXC-P1-015-04 | An access row not yet in force | access version "DPA-2026.12" gives RW-PHONECOL read on DP06 from 2026-12-15 And today is 2026-12-14 | user "u-phone-01" calls GET /data-products/DP06/records?caseId=RW-2026-000102 | the call is refused with status 403 and MSG-P4-002 | RWB-E1-016 |
| AC-EXC-P1-015-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-015-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-015-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-015-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.16 Maintain the data catalog entry per data product

#### A2.16.1 Intent

**Business objective.** Keeps the catalog entry for each data product: definition, owner, source, refresh, quality rules and access.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Keeps the catalog entry for each data product: definition, owner, source, refresh, quality rules and access.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Data steward and data product owner | Opens the screen and maintain the data catalog entry per data product | Checks the role, the capability area and the scope |
| 2 | Data steward and data product owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** ACE database

**Prerequisites.** FEAT-RDF-02

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-016-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| VR-P1-016-2 | Load refused at a check | MSG-P1-002 The {source} load for {date} was refused: {check}. The previous load is still in use. |
| BR-P1-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| loan_account.account_no | Account number | varchar(20) | Yes | None | No |
| loan_account.contract_no | Contract number | varchar(20) | No | None | No |
| loan_account.product_code | Core bank product code | varchar(10) | Yes | LOV-PRODUCT-CODE | No |
| loan_account.product_category_efs | Product category in EFS | varchar(60) | No | None | No |
| loan_account.business_unit | Owning business unit | varchar(10) | No | LOV-BU | No |
| loan_account.contract_date | Contract date | date | No | None | No |
| loan_account.interest_rate | Contract interest rate, percent | numeric(7,4) | No | None | No |
| loan_account.principal_outstanding | Principal outstanding, baht | numeric(18,2) | Yes | None | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Data steward and data product owner | Primary |
| Center of excellence analyst | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-016-01 | Role access | user "u-audit-01" holds read-only role RW-AUDIT, which reads DP02 | the user calls GET /data-products/DP02/records?caseId=RW-2026-000102 | the mobile number shows as "******5678" and the national ID token is returned as "MASKED" And the PII access log holds one entry with user "u-audit-01", product "DP02", case "RW-2026-000102" and the time of the read | RWB-E1-016 |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-016-01 | Catalog entry | the 14 data products DP01 to DP14 | a data steward calls GET /admin/data-products | 14 entries are returned And each has an owner role, a system of record, a refresh cycle, an expected-by time, a retention class and the field list with PDPA tags And the DP02 entry lists 20 fields of which 9 are tagged personal | RWB-E1-016 |
| AC-ALT-P1-016-02 | Access denied | user "u-phone-01" holds RW-PHONECOL, which has no access row for DP06 | the user calls GET /data-products/DP06/records?caseId=RW-2026-000102 | the call is refused with status 403 and MSG-P4-002 And the refusal is written to the access log with user "u-phone-01" and product "DP06" | RWB-E1-016 |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-016-01 | An access load with an unknown role is refused | an access load version "DPA-2026.12" with a row for role "RW-UNKNOWN" and product "DP02" | the load is validated | the load is refused whole with MSG-P1-002 and check "unknown role RW-UNKNOWN" And version "DPA-2026.11" stays in force | RWB-E1-016 |
| AC-EXC-P1-016-02 | No masking rule loaded keeps every personal field masked | user "u-comply-01" holds RW-COMPLY, which reads DP02 | the user calls GET /data-products/DP02/records?caseId=RW-2026-000102 | first_name, last_name, cif_no, date_of_birth and the contact value are returned masked | RWB-E1-016 |
| AC-EXC-P1-016-03 | The PII access log is unavailable | the PII access log rejects every write | user "u-audit-01" calls GET /data-products/DP02/records?caseId=RW-2026-000102 | the call is refused with status 503 and MSG-GEN-006 for system "PII access log" And no personal field is returned | RWB-E1-016 |
| AC-EXC-P1-016-04 | An access row not yet in force | access version "DPA-2026.12" gives RW-PHONECOL read on DP06 from 2026-12-15 And today is 2026-12-14 | user "u-phone-01" calls GET /data-products/DP06/records?caseId=RW-2026-000102 | the call is refused with status 403 and MSG-P4-002 | RWB-E1-016 |
| AC-EXC-P1-016-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-016-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-016-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-016-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.17 Apply the retention and archive rule to the data store

#### A2.17.1 Intent

**Business objective.** Applies the retention class to each data product and archives records past their period.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.17.2 Description

**Functional overview.** Applies the retention class to each data product and archives records past their period.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Compliance and PDPA officer | Opens the screen and apply the retention and archive rule to the data store | Checks the role, the capability area and the scope |
| 2 | Compliance and PDPA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** ACE database

**Prerequisites.** FEAT-RDF-01

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-017-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-017 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.17.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| loan_account.account_no | Account number | varchar(20) | Yes | None | No |
| loan_account.contract_no | Contract number | varchar(20) | No | None | No |
| loan_account.product_code | Core bank product code | varchar(10) | Yes | LOV-PRODUCT-CODE | No |
| loan_account.product_category_efs | Product category in EFS | varchar(60) | No | None | No |
| loan_account.business_unit | Owning business unit | varchar(10) | No | LOV-BU | No |
| loan_account.contract_date | Contract date | date | No | None | No |
| loan_account.interest_rate | Contract interest rate, percent | numeric(7,4) | No | None | No |
| loan_account.principal_outstanding | Principal outstanding, baht | numeric(18,2) | Yes | None | No |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| Compliance and PDPA officer | Primary |
| Data steward and data product owner | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-017-01 | Retention rule applied | 1,250 interaction rows with occurred_at before 2024-12-06 and 4,800 rows from 2024-12-06 onward | JOB-17 runs | 1,250 rows move to the archive container under "retention/2026-12-06/interaction/" And the 1,250 rows are no longer in the live interaction table And the job run logs count 1,250 for DP05 interaction under rule version "RET-2026.11" | RWB-E1-017 |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-017-01 | Rule changed as data | retention rule version "RET-2027.01" changes DP05 interaction to 36 months, approved and valid from 2027-01-01 And interaction rows with occurred_at on 2024-01-15 and on 2023-12-20 | JOB-17 runs on Sunday 2027-01-03 | the row from 2024-01-15 stays in the live table And the row from 2023-12-20 moves to the archive container And the job run logs rule version "RET-2027.01" | RWB-E1-017 |
| AC-ALT-P1-017-02 | Legal hold | case "RW-2024-000311" is marked legal hold and has 40 interaction rows older than 24 months | JOB-17 runs | its 40 rows are kept in the live table And the hold report lists case "RW-2024-000311" with 40 rows kept And the summary alert to Compliance reads MSG-P1-020 with 1 case on legal hold kept | RWB-E1-017 |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-017-01 | The archive write fails | the archive container refuses writes | JOB-17 runs | no interaction row is deleted And the job run ends "FAILED" with MSG-GEN-006 for system "Archive container" | RWB-E1-017 |
| AC-EXC-P1-017-02 | A repeat run in the same month | JOB-17 archived 1,250 rows on 2026-12-06 | JOB-17 is rerun on 2026-12-06 | 0 rows are archived And the archive container still holds one set of the 1,250 rows | RWB-E1-017 |
| AC-EXC-P1-017-03 | A rule for the decision log is refused | a retention load version "RET-2026.12" with a row for product "DP12", table "decision_log_entry" | the load is validated | the load is refused whole with MSG-P1-002 and check "decision_log_entry is not archived by the retention job" | RWB-E1-017 |
| AC-EXC-P1-017-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-017-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-017-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-017-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.18 Show the case list with case ID, owner and queue

#### A2.18.1 Intent

**Business objective.** Gives every recovery team one list of all 90 plus days past due accounts across Mortgage, HP and SSME.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.18.2 Description

**Functional overview.** Gives every recovery team one list of all 90 plus days past due accounts across Mortgage, HP and SSME.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and show the case list with case ID, owner and queue | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, ACE database

**Prerequisites.** FEAT-RDF-03, FEAT-CWC-01

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-018-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P1-018 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.18.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| loan_account.account_no | Account number | varchar(20) | Yes | None | No |
| loan_account.contract_no | Contract number | varchar(20) | No | None | No |
| loan_account.product_code | Core bank product code | varchar(10) | Yes | LOV-PRODUCT-CODE | No |
| loan_account.product_category_efs | Product category in EFS | varchar(60) | No | None | No |
| loan_account.business_unit | Owning business unit | varchar(10) | No | LOV-BU | No |
| loan_account.contract_date | Contract date | date | No | None | No |
| loan_account.interest_rate | Contract interest rate, percent | numeric(7,4) | No | None | No |
| loan_account.principal_outstanding | Principal outstanding, baht | numeric(18,2) | Yes | None | No |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Team manager, Phone collector | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-018-01 | List reconciles | loan_account holds 28,140 accounts at 90 days past due or more for 2026-11-30 And P3 excluded 21 of them at entry, so the ALS count to match is 28,119 And the open cases link 28,119 accounts at 90 days past due or more and 37 accounts below 90 days past due | the case list step of JOB-04 runs | case_list_row holds 28,156 rows for 2026-11-30 And the count check compares 28,119 with 28,119 and the load_run check COUNT is PASS And the check results show 37 rows below 90 days past due | RWB-E1-002 |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-018-01 | Columns present | the case list for 2026-11-30 is built | the extract file for 2026-11-30 is written | each row holds case number, account number, product, stage, status, owner, queue, route, total balance and days past due, in that order And each row also holds team, business date and refresh time And the Power BI data set "Case list v1" offers filters on team, queue and product And the row for case "RW-2026-000123" shows account "ACC0000123", product "MORTGAGE", status "ASSIGNED", queue "MTG-BKK-CO", total balance 1,250,000.00 and days past due 96 | RWB-E1-002 |
| AC-ALT-P1-018-02 | Daily refresh | the 07:00 loads are complete and JOB-03 completed at 06:52 | the case list step runs and completes at 07:12 | every row for 2026-11-30 carries refresh time 2026-12-01 07:12 And the report after the 07:30 data set refresh shows "Refreshed 1 Dec 2026 07:12, data as of 30 Nov 2026" | RWB-E1-002 |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-018-01 | Account data not loaded | the INT-01 load for 2026-11-30 was refused and is not COMPLETED | JOB-04 reaches the case list step | the step does not run and no case_list_row for 2026-11-30 is written And the lake keeps the extract file for 2026-11-27 And the load_run for the step shows status REFUSED with failed check "INT-01 not complete" And the team manager group receives MSG-P1-001 "DP01 Account and arrears is from 2026-11-27. Today's load has not arrived." | RWB-E1-002 |
| AC-EXC-P1-018-02 | Allocation not finished | JOB-03 for 2026-11-30 has not completed at 07:15 | the case list step starts at 07:15 | the list is built with the owner and queue as they are at 07:15 And the load_run check ALLOCATION_COMPLETE is NO And the report shows "Owners and queues may be incomplete for 30 Nov 2026" | RWB-E1-002 |
| AC-EXC-P1-018-03 | Run repeated for the same date | the case list for 2026-11-30 holds 28,156 rows | the platform administrator reruns the step for 2026-11-30 | case_list_row still holds 28,156 rows for 2026-11-30 and no case account appears twice And the refresh time is the time of the rerun | RWB-E1-002 |
| AC-EXC-P1-018-04 | Case interface error | CaseQueryApi raises an error after 12,000 accounts are read | the case list step runs | no case_list_row for 2026-11-30 is written And the load_run status is FAILED And the rows for 2026-11-27 are unchanged | RWB-E1-002 |
| AC-EXC-P1-018-05 | Transfer to the lake fails | the outbound file adapter fails all its retries for the 2026-11-30 extract file | the case list step completes | the load_run status is COMPLETED with check PUBLISHED = NO And the transfer is in the exception queue with a task for the platform administrator | RWB-E1-002 |
| AC-EXC-P1-018-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-018-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-018-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-018-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.19 Publish baseline measures for the recovery portfolio

#### A2.19.1 Intent

**Business objective.** Calculates and publishes the starting measures the benefit model is tracked against.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.19.2 Description

**Functional overview.** Calculates and publishes the starting measures the benefit model is tracked against.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Publish baseline measures for the recovery portfolio | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Power BI, Data lake

**Prerequisites.** FEAT-RDF-11

#### A2.19.3 Business rules and structure

##### A2.19.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-019-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-019 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.19.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Reporting and BI analyst, Finance and CFO delegate | Also uses |

#### A2.19.4 Acceptance criteria

##### A2.19.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-019-01 | Definitions agreed | a definition file of 6 rows for "CASES_BY_ROUTE", "CASES_BY_AGE", "CASES_BY_QUEUE", "REALIZED_RECOVERY", "TIME_IN_STAGE" and "TAT_BY_ROUTE" And each row names its data product, formula, unit and approver "TRB-0001" with approval date 2026-11-20 | it is loaded with valid from 2026-11-21 | definition version "MD-2026.11" is in force with 6 measures And each measure returns its data product and formula through MeasureCatalog | RWB-E1-013 |

##### A2.19.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-019-01 | Baseline published | the loads of business date 2026-11-27 passed their checks | JOB-15 runs at 01:30 on 2026-11-28 | measure_snapshot holds rows for business date 2026-11-27 marked baseline and frozen with definition version "MD-2026.11" And "CASES_BY_ROUTE" totals 120 cases, of which 60 are Mortgage And "REALIZED_RECOVERY" equals the sum of synthetic payments since entry, 4,350,000.00 THB | RWB-E1-013 |
| AC-ALT-P1-019-02 | Power BI data set | the baseline measures are published | JOB-15 runs at 01:30 on 2026-12-02 | the INT-19 extract for business date 2026-12-01 is in the data lake with freshness stamp 2026-12-01 and the record count in its trailer And the extract holds the baseline rows of 2026-11-27 unchanged And the job monitor records the JOB-15 run with its row count, start and end time | RWB-E1-013 |

##### A2.19.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-019-01 | Definition without a formula refused | a definition file where row "TIME_IN_STAGE" has no formula | it is loaded | the load is refused whole with MSG-GEN-001 naming "formula" And no definition version is put in force | RWB-E1-013 |
| AC-EXC-P1-019-02 | Loads of the baseline date failed | the COLLINS load for 2026-11-27 was refused at check "control total" | JOB-15 runs at 01:30 on 2026-11-28 | no baseline rows are written for 2026-11-27 And the run record shows MSG-P1-001 naming "DP03 Case" and 2026-11-26 And the baseline is published by the first JOB-15 run after the 2026-11-27 load passes | RWB-E1-013 |
| AC-EXC-P1-019-03 | Data lake unavailable | the data lake load area does not answer | JOB-15 runs at 01:30 on 2026-12-01 | measure_snapshot rows for 2026-11-30 are written in the Workbench And the extract is held and an alert goes to the operations channel with MSG-GEN-006 naming "Data lake" And the extract is sent by the next JOB-15 run | RWB-E1-013 |
| AC-EXC-P1-019-04 | Measure with no definition in force | the extract configuration lists measure "COST_PER_CASE" with no definition in force | JOB-15 runs at 01:30 on 2026-11-30 | no value for "COST_PER_CASE" is written And the run record shows MSG-P9-003 naming "COST_PER_CASE" | RWB-E1-013 |
| AC-EXC-P1-019-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-019-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.19.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-019-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-019-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.20 Copy the decision log to the lake

#### A2.20.1 Intent

**Business objective.** Streams decision log entries to the data lake so reporting and audit read them without touching the log store.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.20.2 Description

**Functional overview.** Streams decision log entries to the data lake so reporting and audit read them without touching the log store.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Copy the decision log to the lake | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Data lake

**Prerequisites.** FEAT-DRI-01

#### A2.20.3 Business rules and structure

##### A2.20.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-020-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-020 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.20.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit, Reporting and BI analyst | Also uses |

#### A2.20.4 Acceptance criteria

##### A2.20.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-020-01 | Daily copy | 380 entries were written on business date 2026-11-30 | JOB-13 runs at 01:00 on 2026-12-01 | the partition "business_date=2026-11-30" holds 380 rows And the manifest shows cumulative count 12,480 and last hash "a3f1...09c2" And the data lake copy has the same row count and the same last hash as the live log And the watermark moves to 12,480 and "a3f1...09c2" | RWB-E1-014 |

##### A2.20.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-020-01 | Retention rule | lake partitions for business dates 2024-11-29 and 2024-11-30 exist | the retention step of JOB-13 runs on 2026-12-01 | the partitions "business_date=2024-11-29" and "business_date=2024-11-30" move to the archive tier And the job run records 2 partitions archived under rule version "RET-2026.11" | RWB-E1-014 |
| AC-ALT-P1-020-02 | Two runs at the same time | JOB-13 is running for 2026-11-30 | a platform administrator posts a rerun of JOB-13 | the rerun is refused with status 409 and MSG-P2-006 And one run continues | RWB-E1-014 |

##### A2.20.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-020-01 | A copy that does not match is not published | the lake write for 2026-11-30 stops after 379 of 380 rows | the reconciliation step compares the copy with the live log | the partition is not marked complete And the watermark stays at 12,100 and "77be...41d0" And the job run shows check "REC-08" failed with MSG-P1-019 | RWB-E1-014 |
| AC-EXC-P1-020-02 | A repeat run for the same date writes no duplicates | JOB-13 completed for 2026-11-30 with 380 rows | JOB-13 is rerun for 2026-11-30 | the partition "business_date=2026-11-30" still holds 380 rows And the cumulative count stays 12,480 | RWB-E1-014 |
| AC-EXC-P1-020-03 | The decision log interface is unavailable | DecisionLogExport returns an error for every call | JOB-13 runs for 2026-11-30 | the job run ends with status "FAILED" and MSG-GEN-006 for system "Decision log" And the watermark and the previous partitions are unchanged | RWB-E1-014 |
| AC-EXC-P1-020-04 | A day with no new decisions | no entry was written after "77be...41d0" | JOB-13 runs for 2026-11-30 | the partition holds 0 rows and the manifest shows cumulative count 12,100 And check "REC-08" passes | RWB-E1-014 |
| AC-EXC-P1-020-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-020-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.20.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-020-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-020-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.21 Run legacy feed jobs on ADF and Control-M

#### A2.21.1 Intent

**Business objective.** Schedules and runs the batch feed jobs that carry data from the legacy systems into the data store.

**Problem.** Recovery data is held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Loads on time and complete | 99 percent of days | Decision log and Workbench records | Monthly |

#### A2.21.2 Description

**Functional overview.** Schedules and runs the batch feed jobs that carry data from the legacy systems into the data store.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run legacy feed jobs on ADF and Control-M | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** COLLINS, Control-M, SFTP

**Prerequisites.** FEAT-RDF-21

#### A2.21.3 Business rules and structure

##### A2.21.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-021-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-021 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.21.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.21.4 Acceptance criteria

##### A2.21.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-021-01 | Four jobs scheduled | the Control-M definitions for the ALS and EFS extracts and the ADF pipelines for CCMS and SVAF are deployed in SIT | business date 2026-11-15 runs, with the CCMS and SVAF files moved on Sunday 2026-11-15 | JOB-01 writes run rows for "INT-01" and "INT-07" with status "LOADED" and start times from 05:00 And JOB-09 writes run rows for "INT-10" and "INT-11" on Monday 2026-11-16 with status "LOADED" and start times from 04:00 And each run row holds the business date, the record count and the start and end time | RWB-E1-051 |

##### A2.21.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-021-01 | Run book | the four feed jobs | the run book check runs in the pipeline | a run book exists for each of JOB-01 and JOB-09 with the sections purpose, schedule, owner, failure signs, restart steps and escalation And the restart steps name the Control-M or ADF job for each of the four feeds | RWB-E1-051 |
| AC-ALT-P1-021-02 | Contract tests | the layout file for "INT-11" SVAF declares "Appraised Value" as a number of 18 digits with 2 decimals And the sample file carries "Appraised Value" as text | the contract tests run in the pipeline | the "INT-11" test fails with message MSG-P2-002 naming field "Appraised Value" And the merge is blocked | RWB-E1-051 |

##### A2.21.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-021-01 | Alert on failure | the ADF pipeline for CCMS fails on Sunday 2026-11-22 | JOB-09 runs on Monday 2026-11-23 at 04:00 | the "INT-10" run row shows status "MISSING" And the data steward and the platform administrator receive message MSG-P2-004 within 15 minutes (assumed; DL11) | RWB-E1-051 |
| AC-EXC-P1-021-02 | COLLINS load late | no COLLINS load for business date 2026-11-24 has arrived | JOB-01 retries at 06:00, 07:00, 08:00 and 09:00 | after the 09:00 attempt the run rows for "INT-01" and "INT-07" show status "MISSING" And the account and arrears data product shows MSG-P1-001 with the date 2026-11-23 | RWB-E1-051 |
| AC-EXC-P1-021-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-021-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.21.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-021-01 | COLLINS load check | COLLINS end of day | Daily 05:00 | Checks and loads the recovery data | Data products current by 07:00 | Every decision uses checked data |
| AC-BG-P1-021-02 | Daily reconciliation | Load complete | Daily | Compares accounts at 90 days past due with open cases | Breaks listed for the data steward | No account is left without a case |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-RDF-001 | Recovery data is held in 14 data products, each with exactly one named system of record and one named owner. | Must | E1 |
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are current to the previous working day. | Must | E1 |
| REQ-RDF-003 | Collections contact history, promises and case status transfer from EFS so that the case carries what happened before day 90. | Must | E1 |
| REQ-RDF-004 | Collateral records and appraisal values are available on the case without a person looking them up in CCMS or SVAF. | Must | E1 |
| REQ-RDF-005 | Every recovery team's Excel file, SharePoint list and local file is listed with its owner, fields and update cycle, and each one has a decision to load it or record it as out of scope. | Must | E1 |
| REQ-RDF-006 | Every file with a load decision is loaded, its row counts reconciled, and its local copy retired with the owner's confirmation and a read-only archive kept. | Must | E1 |
| REQ-RDF-007 | The case list reconciles daily to the ALS count of accounts at 90 or more days past due, with no variance (DL25). | Must | E1 |
| REQ-RDF-008 | Data quality rules run on every load, and every failed row carries a reason code visible to the data product owner. | Must | E1 |
| REQ-RDF-009 | Every data product carries a freshness stamp, and every decision records the freshness of the data it used. | Must | E1 |
| REQ-RDF-010 | Access to each data product is controlled per role, and personal data is masked by role in line with PDPA. | Must | E1 |
| REQ-RDF-011 | Every data product has a catalog entry stating its definition, owner, system of record, refresh cycle and retention. | Must | E1 |
| REQ-RDF-012 | Baseline measures for cases by route, age and queue, realized recovery, time in stage and turnaround per route are published, with definitions agreed by the Tribe. | Must | E1 |
| REQ-RDF-013 | Recovery data carries a retention and archive rule by record class. | Should | E1 |
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live. | Must | E2 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-44 Interface and job monitor | Loads, files, jobs and outbound actions with status and reruns | E2; E8 full |
| SCR-45 Data quality | Load check results, reconciliation breaks and stale data products | E2; E8 full |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| FSD owner, business analyst | | | |
| Business owner | | | |
| Solution architect | | | |
| QA lead | | | |

## Appendix A. Business glossary

Terms follow the Recovery Workbench Business Glossary.

| Term | Thai | Meaning |
|---|---|---|
| Score | คะแนนจากแบบจำลอง | A value COLLINS returns for an account or a case, such as a risk score or a price estimate |
| Return by route | ผลตอบแทนตามแนวทาง | The expected recovery after cost of each route for a case |
| Party | บุคคลที่เกี่ยวข้อง | A person or company with a role on a case |
| Borrower | ผู้กู้ | The party the loan was made to |
| Co-borrower | ผู้กู้ร่วม | A party who borrowed jointly with the borrower |
| Guarantor | ผู้ค้ำประกัน | A party who guaranteed the loan |
| Heir | ทายาท | A party who represents a deceased borrower's estate |
| Vulnerable customer | ลูกหนี้กลุ่มเปราะบาง | A customer with hardship or vulnerability confirmed, treated under X2 |
| Contact point | ช่องทางการติดต่อ | A way to reach a party, with its consent and whether it works |
| Loan account | บัญชีสินเชื่อ | An account in the core bank |
| Days past due | จำนวนวันค้างชำระ | Days since the oldest unpaid installment fell due |
| Non-performing loan | หนี้ที่ไม่ก่อให้เกิดรายได้ | A loan at 90 days past due or more |
| Total balance | ยอดหนี้คงค้างรวม | Principal, interest and fees outstanding |
| Collateral | หลักประกัน | Property or a vehicle securing one or more accounts |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
