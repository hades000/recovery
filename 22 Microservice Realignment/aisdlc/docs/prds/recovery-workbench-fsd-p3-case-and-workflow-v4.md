<!-- working-copy-of: requirement/legacy/03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v6_extracted/recovery-workbench-fsd-p3-case-and-workflow-v4.md -->
> **Working copy.** Canonical source: `requirement/legacy/03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v6_extracted/recovery-workbench-fsd-p3-case-and-workflow-v4.md`. Edit the source, not this copy.

# Recovery Workbench P3 Case and workflow

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P3 Case and workflow |
| Document ID | P3-RWB-FSD-v3 |
| Version | 3 |
| Status | In review |
| Classification | Confidential |
| Date | 15 November 2026 |
| FSD owner | Business analyst, P3 |
| Business owner | Business lead |
| Decision | D-RCV-35 (U1 to U5); ADR-010; open point DL43 |

| Module code | Module name | First in |
|---|---|---|
| P3 | Case and workflow | E1 core, E2 screens |

**Feature scope.** Case record, CMMN state, queues, allocation, timers, the Drools evaluator.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P3 Case and workflow | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |
| Recovery Workbench ACE DB Alignment Change Register v1 | Decision record | D-RCV-35, ADR-010, Appendix B re-keyed links |
| Recovery Workbench ACE Data Tier Map v1 | Frozen input | Views, extension tables, business keys |
| Recovery Workbench Event and Messaging Design v3 | Design | EV-26 AceDataReady, EV-27 AceDataLate |
| Recovery Workbench Batch and Scheduling Design v3 | Design | JOB-02, JOB-04, JOB-07, JOB-08 start on the ACE batch-complete record; JOB-01 and JOB-09 retired |

### Change note, version 3

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | Baseline: case creation from the COLLINS load and the file loads |
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 and ADR-010. Case creation (JOB-02) now starts on AceDataReady (EV-26), raised from the ACE batch record `ace_batch_run` read through `recovery.v_ace_batch_status`, instead of the COLLINS LoadCompleted event; a late batch raises AceDataLate (EV-27). Account, customer, contact, relation, collateral, collections history and plan data are read through `v_ace_account`, `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation`, `v_ace_collateral`, `v_ace_efs_action` and `v_ace_plan` instead of `loan_account`, `party`, `contact_point` and `collections_history`. Links to ACE records are business keys with no foreign key (Appendix B): `recovery_case.primary_person_key`, `case_account.account_key`, `case_party.person_key`, `case_list_row.account_key`, `case_entry_exclusion.account_key`. The case list reads its account columns from ACE. New section A1.5. FEAT-CHO-10 (A2.36, RWB-E2-023) is removed by D-RCV-35; later home: ACE ingestion. FEAT-CHO-03, FEAT-CHO-05 and FEAT-CHO-08 are renamed; their IDs are kept. NLEADS credit results are read from `v_ace_credit_decision`. Stale-data message MSG-P1-001 reworded. Plan-status and booking exception rows re-pointed from data quality exceptions to reconciliation breaks. No other section changed. |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | No build in this module |
| Case record and shared entities | EXTEND | ACE common module; Case and Workflow Model | Recovery fields added to the ACE case |
| Notification path | REUSE | ACE notification path | Recovery templates only |
| Workflow and state machine | NEW | Workflow Engine Design | Programmatic CMMN runtime in the recovery module (DT09) |
| Decision record and audit trail | REUSE | Audit and Logging Design | Writes through P7 |
| Attachments and evidence | REUSE | Document Management Design | Through P5 |
| Role and permission matrix | REUSE | Users Roles and Permissions | Capability areas from P4 |
| Restructure calculator | REUSE | ACE common module | Not used |
| Source data: account, customer, contact, relations, collateral, collections history, plan | REUSE | ACE database through `recovery.v_ace_*` views (D-RCV-35, ADR-010) | Read only. The Workbench loads, copies and transforms no source data and holds no foreign key into ACE |
| Batch business date and completion | REUSE | ACE batch record `ace_batch_run` (RWB-ACE-001), read through `v_ace_batch_status` | Triggers case creation through EV-26 AceDataReady |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** Case record, CMMN state, queues, allocation, timers, the Drools evaluator.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-ACA-12; FEAT-ACA-15; FEAT-CHO-01; FEAT-CHO-01, FEAT-CWC-04; FEAT-CHO-06; FEAT-CWC-01; FEAT-CWC-02; FEAT-CWC-03

**Constraints.** Built in the ACE service as part of the recovery module; source data is read from the ACE database through the read-only `recovery.v_ace_*` views and is never loaded or copied (D-RCV-35, ADR-010); a link to an ACE record is a business key with no foreign key; every value a business person may change is a versioned data row (principle 1). The features that read Tier 2 views (`v_ace_batch_status`, `v_ace_party_product`, `v_ace_credit_decision`) stay behind their flags until RWB-ACE-001 lands (DL43).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P3 | FEAT-CWC-01 | Generate the case ID | System | Issues the case identifier in the RW-YYYY-NNNNNN format when a case is created, and never reuses one. | E1 | A2.1 |
| P3 | FEAT-CWC-02 | Create one case per customer and product | System | Creates the recovery case as the master object and links every ACE account and customer to it by business key (`account_key`, `person_key`); collateral is read from `v_ace_collateral` by account. | E1 | A2.2 |
| P3 | FEAT-CWC-03 | Hold the case state in the ACE database | System | Holds the case state as rows and moves it by rule, so every state, move and clock is held in one place. | E1 | A2.3 |
| P3 | FEAT-CWC-04 | Apply the entry rule at 90 days past due | System | Runs the daily entry rule and creates a case for every account that reaches 90 days past due and is not excluded. | E1 | A2.4 |
| P3 | FEAT-CWC-05 | Apply the exclusion rules as data | System | Blocks case creation for deceased, fraud, bankruptcy, an active plan or an open dispute, and logs the reason. | E1 | A2.5 |
| P3 | FEAT-CWC-06 | Hold roles, teams and queues as data | Admin | Keeps the role, team and queue structure in versioned tables so it changes without a code release. | E1 | A2.6 |
| P3 | FEAT-CWC-07 | Run the allocation rule table | System | Picks the queue for a new case from product, region, exposure and workload rules held as data. | E1 | A2.7 |
| P3 | FEAT-CWC-08 | Run the assignment engine by load and continuity | System | Picks the one owner for the case from the assignment rules, favoring continuity and respecting the caseload cap. | E1 | A2.8 |
| P3 | FEAT-CWC-09 | Send a case to the overflow queue when no rule matches | System | Applies the default row when no allocation rule matches, so no case is left without a queue. | E1 | A2.9 |
| P3 | FEAT-CWC-10 | Run the transfer rule table and engine | System | Moves a case between queues and owners when a transfer rule fires, and records the reason. | E1 | A2.10 |
| P3 | FEAT-CWC-11 | Set service levels and stage timers | System | Starts the service level clock on every state the case enters, from the timer table held as data. | E1 | A2.11 |
| P3 | FEAT-CWC-12 | Set and track prescription dates | System | Reads the legal period from reference data, sets the prescription date and tracks it independently of stage clocks. | E1 | A2.12 |
| P3 | FEAT-CWC-13 | Escalate a breached timer to the named point | System | Raises a service level breach to the escalation point named in the table. The case does not move. | E1 | A2.13 |
| P3 | FEAT-CWC-14 | Load a rule version with validation | Admin | Takes a new rule version through a validated load, with a dry run against live cases before it takes effect. | E1 | A2.14 |
| P3 | FEAT-CWC-15 | Roll back a rule version | Admin | Returns the engine to the previous rule version and records what was in force when each decision was taken. | E1 | A2.15 |
| P3 | FEAT-CWC-16 | Report every rule change for audit | Admin | Produces the audit report of rule changes: who changed what, when, under which version, and the effect. | E1 | A2.16 |
| P3 | FEAT-CWC-17 | Rebalance queues daily | System | Moves cases between owners overnight to hold the caseload inside the cap and keep the spread even. | E1 | A2.17 |
| P3 | FEAT-CWC-18 | Publish queue measures | System | Calculates queue depth, ageing and the owner spread, and publishes them to the case list and Power BI. | E1 | A2.18 |
| P3 | FEAT-CWC-19 | Show queue and owner on the case list | User | Puts the queue and the named owner on every row of the case list, so the owner question is answered on one screen. | E1 | A2.19 |
| P3 | FEAT-CWC-20 | Expose the workflow admin API | Admin | Gives administration a programmatic way to move, reassign and correct a case with a reason code, before screens exist. | E1 | A2.20 |
| P3 | FEAT-CWC-21 | Log every workflow event | System | Writes every state change, timer, allocation and transfer as an event with its rule ID and version. | E1 | A2.21 |
| P3 | FEAT-CWC-22 | Hold the parameter catalog and configuration service | Admin | Keeps every limit, threshold, name and timer as a versioned parameter row that changes without a release. | E1 | A2.22 |
| P3 | FEAT-CWC-23 | Run the reference data service with versioned tables | Admin | Serves every reference table to the engines with its version, so a decision records which version it used. | E1 | A2.23 |
| P3 | FEAT-CWC-24 | Run versioned migrations with parameterized schema names | Admin | Applies database changes through versioned migrations with no hard-coded schema name. | E1 | A2.24 |
| P3 | FEAT-CWC-25 | Set product parameters without a code change | Admin | Lets Mortgage, HP and SSME carry different limits, timers and rules from parameter rows alone. | E1 | A2.25 |
| P3 | FEAT-CWC-26 | Control module release with dated feature flags | Admin | Turns a module on by environment behind a flag that carries the date it must be removed. | E1 | A2.26 |
| P3 | FEAT-CHO-01 | Take the case hand-over from EFS with full history | System | Takes the account at case entry and reads its contact and promise history from the EFS data ACE ingests, through `v_ace_efs_action`. | E2 | A2.27 |
| P3 | FEAT-CHO-02 | Read the ACE plan status | System | Reads the restructure plan status from the ACE common module, so an active plan is known on the case. | E2 | A2.28 |
| P3 | FEAT-CHO-03 | Read customer facts from ACE | System | Reads the customer profile and product holding ACE ingests from SCBPDM and the core bank, through `v_ace_customer` and `v_ace_party_product` (DL20 as amended by D-RCV-35). | E2 | A2.29 |
| P3 | FEAT-CHO-04 | Create a case the morning after it reaches 90 days past due | System | Replaces the weekly transfer with daily case creation on the ACE batch-complete record (EV-26 AceDataReady). | E2 | A2.30 |
| P3 | FEAT-CHO-05 | Hold case creation when the ACE batch is late | System | Keeps the last complete ACE business date in use, creates the cases on the next complete ACE batch, and logs the gap. | E2 | A2.31 |
| P3 | FEAT-CHO-06 | Hold the treatment entity and plan timers | System | Creates the treatment record and its timers, which the restructure and deed in lieu routes both build on. | E2 | A2.32 |
| P3 | FEAT-CHO-07 | Prepare the credit approval pack for NLEADS | System | Assembles the plan and its credit approval pack for the officer to submit in NLEADS, and records the result on the case. | E2 | A2.33 |
| P3 | FEAT-CHO-08 | Confirm booked terms from the ACE account data | System | Matches the approved terms or settlement to the booked position in `v_ace_account` for the next ACE business date, and raises a task when it is missing. | E2 | A2.34 |
| P3 | FEAT-CHO-09 | Build the stage 2 data products | System | Adds the contract, plan and treatment read models to the data store. | E2 | A2.35 |
| P3 | FEAT-CHO-10 | Automate the EFS file load (removed) | System | Removed by D-RCV-35 - later home: ACE ingestion. ACE ingests EFS; the Workbench reads it through `v_ace_efs_action`. | E2 | A2.36 |
| P3 | FEAT-CHO-11 | Query the decision log for audit | Admin | Gives audit a query API over the decision log, by case, decision, period or approver. | E2 | A2.37 |
| P3 | FEAT-WKM-01 | Show my queue with filters and ageing | User | Gives each user their own queue with filters, sort and the age of every case in it. | E2 | A2.38 |
| P3 | FEAT-WKM-02 | Show team queues | User | Gives the team manager every queue in the team, with depth, ageing and the spread across owners. | E2 | A2.39 |
| P3 | FEAT-WKM-03 | Transfer a case manually with a reason | User | Lets an authorized user move a case to another queue, with a coded reason recorded on the case. | E2 | A2.40 |
| P3 | FEAT-WKM-04 | Reassign a case to another owner | User | Moves a case to a named owner for capacity, skill or absence, keeping the state and the clocks. | E2 | A2.41 |
| P3 | FEAT-WKM-05 | Show timers and the service level on the case | User | Puts the stage clock, the service level and the prescription date on the case record view. | E2 | A2.42 |
| P3 | FEAT-WKM-06 | Show the deviation flag on the case | User | Shows which deviation is open on the case, who owns it and since when. | E2 | A2.43 |
| P3 | FEAT-WKM-07 | Show escalation state on the case | User | Shows that a service level has been breached, to whom it was escalated and when. | E2 | A2.44 |
| P3 | FEAT-WKM-08 | Show the full case record view with the history timeline | User | Completes the case record view: accounts, parties, collateral, documents, communications, decisions and history. | E2 | A2.45 |
| P3 | FEAT-WKM-09 | Show queue history on the case | User | Shows every queue and owner the case has had, with the reason for each move. | E2 | A2.46 |
| P3 | FEAT-WKM-10 | Reallocate when an owner is unavailable | System | Moves open cases to another owner in the same team when the owner leaves or is absent past the threshold. | E2 | A2.47 |
| P3 | FEAT-WKM-11 | Reallocate when the caseload cap is breached | System | Moves the newest cases off an owner who is over the cap, until the cap is met. | E2 | A2.48 |
| P3 | FEAT-WKM-12 | Run the Epic 2 release checklist and go-live readiness | Admin | Works the release checklist, training and readiness for the December release. | E2 | A2.49 |
| P3 | FEAT-CWC-27 | Show the next action and its due date on a case | User | Every active case carries a named action, an owner and a due date, taken from the routing rule that moved it into its current state. | E2 | A2.50 |
| P3 | FEAT-CWC-28 | Set the next action from the routing rules | System | On every state change the action, the owner of the next state and the timer from the firing rule become the case's next action. | E2 | A2.51 |
| P3 | FEAT-CWC-29 | Accept a queue placement from a model or an agent | System | A caller that is not the allocation engine may place a case on a queue. The queue's own allocation, caseload and permission rules still apply, and the placement is logged with the caller and the model version. Disabled by feature flag until a consumer exists. | E2 | A2.52 |

### A1.3 Background

Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale. Freshness comes from the ACE batch record, `v_ace_batch_status`.

### A1.5 Source data read path (D-RCV-35)

The module reads ACE through the `recovery.v_ace_*` views only. A direct read of a `public` table, a copy of a source record or a foreign key into ACE is a defect (Tier Map section 9).

| What P3 needs | View | Key the Workbench holds | Replaces (v2) |
|---|---|---|---|
| Account, days past due, balances, classification, tdr_flag, booked settlement, `data_as_of` | `v_ace_account` | `case_account.account_key`, `case_list_row.account_key`, `case_entry_exclusion.account_key` | `loan_account`, `case_account.account_id` |
| Customer, deceased flag, masked identity number | `v_ace_customer` | `recovery_case.primary_person_key`, `case_party.person_key` | `party`, `primary_customer_id`, `case_party.party_id` |
| Borrower, guarantor and co-borrower roles | `v_ace_ca_relation` | `account_key` + `person_key` | `party` roles from the load |
| Phone, email, address | `v_ace_contact` | `contact_key` (`contact_type:key`) | `contact_point` |
| Collateral and asset | `v_ace_collateral`, `v_ace_asset` | `account_key` | `collateral`, `account_collateral` |
| Collections contact and promise history | `v_ace_efs_action` | `account_key` | `collections_history` |
| Restructure plan status | `v_ace_plan` | plan reference | ACE common module read |
| Customer's other products | `v_ace_party_product` (Tier 2) | `person_key` | `party_product` |
| NLEADS credit result | `v_ace_credit_decision` (Tier 2) | treatment reference | `treatment.nleads_ref`, `credit_result`, `credit_result_reason`, `credit_result_at` |
| Batch business date and completion | `v_ace_batch_status` (Tier 2) | none | `load_run`, COLLINS LoadCompleted |
| Workbench flags about an ACE record | `recovery.party_ext`, `recovery.account_ext` | `person_key`, `account_key` | `party.fraud_flag` and Workbench columns on the copy tables |

**Trigger.** When the ACE batch record for ALS reaches status `COMPLETED` for the expected business date, EV-26 AceDataReady is raised and JOB-02 case creation, JOB-04 reconciliation, JOB-07 payment matching and JOB-08 booking confirmation start for that business date. If the cut-off passes first, EV-27 AceDataLate is raised. No P3 job reads a file or loads a row. JOB-01 and JOB-09 are retired.

**Case list.** SCR-02 and every queue view read the case, queue and owner from Workbench tables and the account columns (account number, days past due, balance, data as of) from `v_ace_account` by `case_list_row.account_key`. Reconciliation of the case list to `v_ace_account` is `reconciliation_result` (JOB-04); a business key with no ACE row is listed by REC-05.

**Links.** Each link is a `varchar(255)` business key with no foreign key, because ACE deletes on `account` cascade. Referential integrity is checked by the read model and by REC-05, not by the database.

## A2. Functional decomposition

### A2.1 Generate the case ID

#### A2.1.1 Intent

**Business objective.** Issues the case identifier in the RW-YYYY-NNNNNN format when a case is created, and never reuses one.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Issues the case identifier in the RW-YYYY-NNNNNN format when a case is created, and never reuses one.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Generate the case ID | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** None

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-001-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P3-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-001-01 | Case created at 90 days past due | account A-5001 of customer P-0101, product group "HIRE_PURCHASE", reaches 90 days past due in `v_ace_account` for the completed ACE business date with no exclusion And the last case number issued in 2026 is RW-2026-000122 | the entry rule runs | case RW-2026-000123 exists with status "NEW", no stage code and entry date 2026-12-01 And case_account holds account_key A-5001 as the primary account and case_party holds person_key P-0101 as "BORROWER" And recovery_case.primary_person_key is P-0101 And CaseCreated is published with case number RW-2026-000123 | RWB-E1-018 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-001-01 | Exclusion applied | account A-5002 at 92 days past due with tdr_flag = true | the entry rule runs | no case is created for A-5002 And an exclusion record holds account A-5002, reason "ACTIVE_PLAN", the exclusion rule ID and version "EXCL-2026.11" | RWB-E1-018 |
| AC-ALT-P3-001-02 | One case per customer and product | customer P-0102 has two hire purchase accounts A-5003 and A-5004, both at 95 days past due | the entry rule runs | one case exists for P-0102 and "HIRE_PURCHASE" with both accounts linked And total outstanding at entry is the sum of the two balances, THB 412,350.00 | RWB-E1-018 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-001-01 | A repeated run creates nothing new | JOB-02 has created case RW-2026-000125 for account A-5008 on 2026-12-01 | JOB-02 runs again for 2026-12-01 | account A-5008 has one case link And no case number is issued in the second run | RWB-E1-018 |
| AC-EXC-P3-001-02 | No cases before the ACE batch is complete | `v_ace_batch_status` shows the ALS batch for business date 2026-12-02 with a status other than "COMPLETED" | the morning schedule runs | JOB-02 does not start for 2026-12-02 And the job monitor shows MSG-P1-001 for the account data product And JOB-02 starts for 2026-12-02 when AceDataReady (EV-26) is raised for ALS and 2026-12-02 | RWB-E1-018 |
| AC-EXC-P3-001-03 | The decision log write fails | the decision log store is unavailable | the entry rule runs for account A-5009 | no case exists for A-5009 And the job record lists A-5009 as failed with MSG-P7-003 And A-5009 is taken again in the next run | RWB-E1-018 |
| AC-EXC-P3-001-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-001-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-001-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-001-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.2 Create one case per customer and product

#### A2.2.1 Intent

**Business objective.** Creates the recovery case as the master object and links every ACE account and customer to it by business key (`case_account.account_key`, `case_party.person_key`); collateral is read from `v_ace_collateral` by account.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Creates the recovery case as the master object and links every ACE account and customer to it by business key (`case_account.account_key`, `case_party.person_key`); collateral is read from `v_ace_collateral` by account.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Create one case per customer and product | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, ACE database (`v_ace_account`, `v_ace_customer`, `v_ace_ca_relation`, `v_ace_collateral`)

**Prerequisites.** FEAT-CWC-01; RWB-E1-069 (ACE source views)

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-002-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| R-UNI-01 | Close the recovery case, hand the account back to servicing, release any hold, when arrears cleared in full and days_past_due falls below 90 | Moves to CASE_CURED_CLOSED |
| R-UNI-47 | Stop every open action, close the case as sold, transfer the data, when the account is awarded in a debt sale lot while on another route | Moves to CASE_CLOSED_SOLD |
| BR-P3-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-002-01 | Case created at 90 days past due | account A-5001 of customer P-0101, product group "HIRE_PURCHASE", reaches 90 days past due in `v_ace_account` for the completed ACE business date with no exclusion And the last case number issued in 2026 is RW-2026-000122 | the entry rule runs | case RW-2026-000123 exists with status "NEW", no stage code and entry date 2026-12-01 And case_account holds account_key A-5001 as the primary account and case_party holds person_key P-0101 as "BORROWER" And recovery_case.primary_person_key is P-0101 And CaseCreated is published with case number RW-2026-000123 | RWB-E1-018 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-002-01 | Exclusion applied | account A-5002 at 92 days past due with tdr_flag = true | the entry rule runs | no case is created for A-5002 And an exclusion record holds account A-5002, reason "ACTIVE_PLAN", the exclusion rule ID and version "EXCL-2026.11" | RWB-E1-018 |
| AC-ALT-P3-002-02 | One case per customer and product | customer P-0102 has two hire purchase accounts A-5003 and A-5004, both at 95 days past due | the entry rule runs | one case exists for P-0102 and "HIRE_PURCHASE" with both accounts linked And total outstanding at entry is the sum of the two balances, THB 412,350.00 | RWB-E1-018 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-002-01 | A repeated run creates nothing new | JOB-02 has created case RW-2026-000125 for account A-5008 on 2026-12-01 | JOB-02 runs again for 2026-12-01 | account A-5008 has one case link And no case number is issued in the second run | RWB-E1-018 |
| AC-EXC-P3-002-02 | No cases before the ACE batch is complete | `v_ace_batch_status` shows the ALS batch for business date 2026-12-02 with a status other than "COMPLETED" | the morning schedule runs | JOB-02 does not start for 2026-12-02 And the job monitor shows MSG-P1-001 for the account data product And JOB-02 starts for 2026-12-02 when AceDataReady (EV-26) is raised for ALS and 2026-12-02 | RWB-E1-018 |
| AC-EXC-P3-002-03 | The decision log write fails | the decision log store is unavailable | the entry rule runs for account A-5009 | no case exists for A-5009 And the job record lists A-5009 as failed with MSG-P7-003 And A-5009 is taken again in the next run | RWB-E1-018 |
| AC-EXC-P3-002-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-002-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-002-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-002-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.3 Hold the case state in the ACE database

#### A2.3.1 Intent

**Business objective.** Holds the case state as rows and moves it by rule, so every state, move and clock is held in one place.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Holds the case state as rows and moves it by rule, so every state, move and clock is held in one place.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Hold the case state in the ACE database | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Quartz scheduler

**Prerequisites.** FEAT-CWC-02

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-003-1 | A move not allowed from the current state | MSG-P3-005 This case cannot move to {state} from {current}. |
| BR-P3-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-003-01 | Case created at 90 days past due | account A-5001 of customer P-0101, product group "HIRE_PURCHASE", reaches 90 days past due in `v_ace_account` for the completed ACE business date with no exclusion And the last case number issued in 2026 is RW-2026-000122 | the entry rule runs | case RW-2026-000123 exists with status "NEW", no stage code and entry date 2026-12-01 And case_account holds account_key A-5001 as the primary account and case_party holds person_key P-0101 as "BORROWER" And recovery_case.primary_person_key is P-0101 And CaseCreated is published with case number RW-2026-000123 | RWB-E1-018 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-003-01 | Exclusion applied | account A-5002 at 92 days past due with tdr_flag = true | the entry rule runs | no case is created for A-5002 And an exclusion record holds account A-5002, reason "ACTIVE_PLAN", the exclusion rule ID and version "EXCL-2026.11" | RWB-E1-018 |
| AC-ALT-P3-003-02 | One case per customer and product | customer P-0102 has two hire purchase accounts A-5003 and A-5004, both at 95 days past due | the entry rule runs | one case exists for P-0102 and "HIRE_PURCHASE" with both accounts linked And total outstanding at entry is the sum of the two balances, THB 412,350.00 | RWB-E1-018 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-003-01 | A repeated run creates nothing new | JOB-02 has created case RW-2026-000125 for account A-5008 on 2026-12-01 | JOB-02 runs again for 2026-12-01 | account A-5008 has one case link And no case number is issued in the second run | RWB-E1-018 |
| AC-EXC-P3-003-02 | No cases before the ACE batch is complete | `v_ace_batch_status` shows the ALS batch for business date 2026-12-02 with a status other than "COMPLETED" | the morning schedule runs | JOB-02 does not start for 2026-12-02 And the job monitor shows MSG-P1-001 for the account data product And JOB-02 starts for 2026-12-02 when AceDataReady (EV-26) is raised for ALS and 2026-12-02 | RWB-E1-018 |
| AC-EXC-P3-003-03 | The decision log write fails | the decision log store is unavailable | the entry rule runs for account A-5009 | no case exists for A-5009 And the job record lists A-5009 as failed with MSG-P7-003 And A-5009 is taken again in the next run | RWB-E1-018 |
| AC-EXC-P3-003-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-003-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-003-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-003-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.4 Apply the entry rule at 90 days past due

#### A2.4.1 Intent

**Business objective.** Runs the daily entry rule and creates a case for every account that reaches 90 days past due and is not excluded.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Runs the daily entry rule and creates a case for every account that reaches 90 days past due and is not excluded.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Apply the entry rule at 90 days past due | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, ACE database (`v_ace_account`, `v_ace_efs_action`, `v_ace_batch_status`)

**Prerequisites.** FEAT-CWC-02

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-004-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| R-UNI-47 | Stop every open action, close the case as sold, transfer the data, when the account is awarded in a debt sale lot while on another route | Moves to CASE_CLOSED_SOLD |
| BR-P3-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-004-01 | Case created at 90 days past due | account A-5001 of customer P-0101, product group "HIRE_PURCHASE", reaches 90 days past due in `v_ace_account` for the completed ACE business date with no exclusion And the last case number issued in 2026 is RW-2026-000122 | the entry rule runs | case RW-2026-000123 exists with status "NEW", no stage code and entry date 2026-12-01 And case_account holds account_key A-5001 as the primary account and case_party holds person_key P-0101 as "BORROWER" And recovery_case.primary_person_key is P-0101 And CaseCreated is published with case number RW-2026-000123 | RWB-E1-018 |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-004-01 | Exclusion applied | account A-5002 at 92 days past due with tdr_flag = true | the entry rule runs | no case is created for A-5002 And an exclusion record holds account A-5002, reason "ACTIVE_PLAN", the exclusion rule ID and version "EXCL-2026.11" | RWB-E1-018 |
| AC-ALT-P3-004-02 | One case per customer and product | customer P-0102 has two hire purchase accounts A-5003 and A-5004, both at 95 days past due | the entry rule runs | one case exists for P-0102 and "HIRE_PURCHASE" with both accounts linked And total outstanding at entry is the sum of the two balances, THB 412,350.00 | RWB-E1-018 |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-004-01 | A repeated run creates nothing new | JOB-02 has created case RW-2026-000125 for account A-5008 on 2026-12-01 | JOB-02 runs again for 2026-12-01 | account A-5008 has one case link And no case number is issued in the second run | RWB-E1-018 |
| AC-EXC-P3-004-02 | No cases before the ACE batch is complete | `v_ace_batch_status` shows the ALS batch for business date 2026-12-02 with a status other than "COMPLETED" | the morning schedule runs | JOB-02 does not start for 2026-12-02 And the job monitor shows MSG-P1-001 for the account data product And JOB-02 starts for 2026-12-02 when AceDataReady (EV-26) is raised for ALS and 2026-12-02 | RWB-E1-018 |
| AC-EXC-P3-004-03 | The decision log write fails | the decision log store is unavailable | the entry rule runs for account A-5009 | no case exists for A-5009 And the job record lists A-5009 as failed with MSG-P7-003 And A-5009 is taken again in the next run | RWB-E1-018 |
| AC-EXC-P3-004-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-004-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-004-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-004-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.5 Apply the exclusion rules as data

#### A2.5.1 Intent

**Business objective.** Blocks case creation for deceased, fraud, bankruptcy, an active plan or an open dispute, and logs the reason.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Blocks case creation for deceased, fraud, bankruptcy, an active plan or an open dispute, and logs the reason.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Apply the exclusion rules as data | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, ACE database (`v_ace_customer`, `v_ace_account`, `v_ace_plan`), `recovery.party_ext`, `recovery.account_ext`

**Prerequisites.** FEAT-CWC-04

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-005-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| R-UNI-06 | Raise X2, apply the vulnerable customer treatment rules, when hardship or vulnerability is recorded | Moves to HELD_DEVIATION |
| BR-P3-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.2 Where each exclusion input is read (D-RCV-35)

| Exclusion | Read from | Key |
|---|---|---|
| Deceased | `v_ace_customer.deceased_flag`, overridden by `recovery.party_ext.deceased_override` | `person_key` |
| Fraud | `recovery.party_ext.fraud_flag` | `person_key` |
| Bankruptcy | `recovery.party_ext.bankruptcy` | `person_key` |
| Active plan | `v_ace_account.tdr_flag` and `v_ace_plan` | `account_key` |
| Open dispute | `recovery.account_ext.dispute_open` | `account_key` |

The exclusion record is `case_entry_exclusion`, keyed by `account_key`.

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Center of excellence analyst | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-005-01 | Case created at 90 days past due | account A-5001 of customer P-0101, product group "HIRE_PURCHASE", reaches 90 days past due in `v_ace_account` for the completed ACE business date with no exclusion And the last case number issued in 2026 is RW-2026-000122 | the entry rule runs | case RW-2026-000123 exists with status "NEW", no stage code and entry date 2026-12-01 And case_account holds account_key A-5001 as the primary account and case_party holds person_key P-0101 as "BORROWER" And recovery_case.primary_person_key is P-0101 And CaseCreated is published with case number RW-2026-000123 | RWB-E1-018 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-005-01 | Exclusion applied | account A-5002 at 92 days past due with tdr_flag = true | the entry rule runs | no case is created for A-5002 And an exclusion record holds account A-5002, reason "ACTIVE_PLAN", the exclusion rule ID and version "EXCL-2026.11" | RWB-E1-018 |
| AC-ALT-P3-005-02 | One case per customer and product | customer P-0102 has two hire purchase accounts A-5003 and A-5004, both at 95 days past due | the entry rule runs | one case exists for P-0102 and "HIRE_PURCHASE" with both accounts linked And total outstanding at entry is the sum of the two balances, THB 412,350.00 | RWB-E1-018 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-005-01 | A repeated run creates nothing new | JOB-02 has created case RW-2026-000125 for account A-5008 on 2026-12-01 | JOB-02 runs again for 2026-12-01 | account A-5008 has one case link And no case number is issued in the second run | RWB-E1-018 |
| AC-EXC-P3-005-02 | No cases before the ACE batch is complete | `v_ace_batch_status` shows the ALS batch for business date 2026-12-02 with a status other than "COMPLETED" | the morning schedule runs | JOB-02 does not start for 2026-12-02 And the job monitor shows MSG-P1-001 for the account data product And JOB-02 starts for 2026-12-02 when AceDataReady (EV-26) is raised for ALS and 2026-12-02 | RWB-E1-018 |
| AC-EXC-P3-005-03 | The decision log write fails | the decision log store is unavailable | the entry rule runs for account A-5009 | no case exists for A-5009 And the job record lists A-5009 as failed with MSG-P7-003 And A-5009 is taken again in the next run | RWB-E1-018 |
| AC-EXC-P3-005-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-005-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-005-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-005-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.6 Hold roles, teams and queues as data

#### A2.6.1 Intent

**Business objective.** Keeps the role, team and queue structure in versioned tables so it changes without a code release.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Keeps the role, team and queue structure in versioned tables so it changes without a code release.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Reference data administrator | Opens the screen and hold roles, teams and queues as data | Checks the role, the capability area and the scope |
| 2 | Reference data administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** None

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-006-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| VR-P3-006-2 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| BR-P3-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| Reference data administrator | Primary |
| Center of excellence analyst, Team manager | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-006-01 | Tables loaded | the Queues template with 12 queues for the TDR, DIL, litigation, NPA, debt sale and write-off teams and 48 member rows | the QUEUE and QUEUE_MEMBER sheets are loaded as version 1 with valid from 2026-11-30 and approved | 12 queue rows are in force with table version 1 And each queue holds its team code and the role that works it, for example "LIT-BKK-OFF" with "LIT-BKK" and RW-LITOFF And 48 member rows are in force And the reference version holds the author, the approver and the approval time | RWB-E1-019 |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-006-01 | Rollback | QUEUE version 3 is in force with an error in queue "DIL-BKK-CO" And QUEUE version 2 was in force before it | rollback is called once for version 3 | QUEUE version 2 is in force for every queue row And each queue keeps its record ID, so cases in the queue keep their queue And the rollback is recorded with the caller, the time and the reason | RWB-E1-019 |
| AC-ALT-P3-006-02 | Capacity | member U-11 of queue "TDR-BKK-CO" has capacity 40 and holds 40 open cases | a 41st case is offered for U-11 | the capacity service answers "AT_CAP" for U-11 And names the overflow queue "TDR-BKK-OVF" for the case | RWB-E1-019 |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-006-01 | Author cannot approve | QUEUE version 4 was loaded by user U-90 | U-90 approves it | the approval is refused with MSG-P7-002 And version 4 stays VALIDATED and is not in force | RWB-E1-019 |
| AC-EXC-P3-006-02 | Rollback with no earlier version | QUEUE version 1 is the only version | rollback is called for version 1 | the call is refused with MSG-P3-015 And version 1 stays in force | RWB-E1-019 |
| AC-EXC-P3-006-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-006-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-006-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-006-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.7 Run the allocation rule table

#### A2.7.1 Intent

**Business objective.** Picks the queue for a new case from product, region, exposure and workload rules held as data.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Picks the queue for a new case from product, region, exposure and workload rules held as data.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the allocation rule table | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Drools evaluator

**Prerequisites.** FEAT-CWC-06

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-007-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| VR-P3-007-2 | Allocation not recorded (RWB-E1-020) | MSG-P3-013 The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| R-UNI-18 | Reallocate inside the same team by region and workload, keep the state and the clocks, when the owner leaves, is absent beyond the threshold, or the account is reassigned | Moves to REALLOCATED |
| BR-P3-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-007-01 | A new case is placed in the queue its row names | a new case RW-2026-000201 with status "NEW", product group "MORTGAGE", region "BKK" and exposure band "B2" And allocation row "ALLOC-014" matches product group "MORTGAGE", region "BKK" and any exposure band, with target queue "MTG-BKK-CO" | the morning allocation run starts | the case is placed in queue "MTG-BKK-CO" And the case team is "MTG-BKK" and the region is "BKK" | RWB-E1-020 |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-007-01 | The owner is chosen by the queue's method | queue "MTG-BKK-CO" holds three case owners U-01, U-02 and U-03 with 120, 95 and 140 open cases And the last owner given a case in the queue was U-02 | case RW-2026-000201 is placed in the queue | the case is given to U-03 And the case status becomes "ASSIGNED" And an assignment record is written with reason "ALLOCATION" and rule ID "ALLOC-014" | RWB-E1-020 |
| AC-ALT-P3-007-02 | An owner at the caseload cap is skipped | the last owner given a case was U-02 And U-03, the next owner in turn, holds 150 open cases And U-01 holds 120 open cases | case RW-2026-000202 is placed in the queue | the case is given to U-01, the following owner below the cap | RWB-E1-020 |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-007-01 | No allocation row matches | a new case RW-2026-000204 with product group "SSME" and region "NE3" that matches no allocation row | the morning allocation run starts | the case is placed in the exception queue "RWB-EXC" And the case status stays "NEW" And a decision log entry is written with final call "RULE_GAP", product group "SSME" and region "NE3" And CaseAllocationFailed is published with reason "NO_ROW_MATCHED" And the allocation summary carries MSG-P3-012 with count 1 | RWB-E1-020 |
| AC-EXC-P3-007-02 | A case with an open deviation is not allocated to a case owner | a new case RW-2026-000206 with deviation_open = true | the morning allocation run starts | the case is placed in the deviation handler queue "DEV-HANDLER" named by rule R-DEV-01 And no case owner is set and the status stays "NEW" | RWB-E1-020 |
| AC-EXC-P3-007-03 | A repeated run for the same date has no further effect | the morning allocation run for 2026-12-01 has assigned case RW-2026-000201 to U-03 | the run for 2026-12-01 is started again from the job monitor | case RW-2026-000201 keeps owner U-03 and its one assignment record And no second decision log entry is written for the case And the job record shows 1 case skipped as already allocated | RWB-E1-020 |
| AC-EXC-P3-007-04 | A run with no new cases | no case has status "NEW" on 2026-12-01 | the morning allocation run starts | the run completes with 0 cases read And the allocation summary for each team shows 0 in overflow and 0 in the exception queue | RWB-E1-020 |
| AC-EXC-P3-007-05 | A queue with no overflow queue sends the case to the exception queue | queue "HP-CEN-CO" has no overflow queue And every owner in queue "HP-CEN-CO" holds 150 open cases | case RW-2026-000209 is placed in queue "HP-CEN-CO" | the case is placed in the exception queue "RWB-EXC" with reason "NO_OVERFLOW_QUEUE" And the case status stays "NEW" | RWB-E1-020 |
| AC-EXC-P3-007-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-007-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-007-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-007-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.8 Run the assignment engine by load and continuity

#### A2.8.1 Intent

**Business objective.** Picks the one owner for the case from the assignment rules, favoring continuity and respecting the caseload cap.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Picks the one owner for the case from the assignment rules, favoring continuity and respecting the caseload cap.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the assignment engine by load and continuity | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Drools evaluator

**Prerequisites.** FEAT-CWC-07

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-008-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| R-UNI-19 | Reallocate the newest cases until the owner is inside the cap, when the owner is above the maximum caseload | Moves to REALLOCATED |
| BR-P3-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-008-01 | A new case is placed in the queue its row names | a new case RW-2026-000201 with status "NEW", product group "MORTGAGE", region "BKK" and exposure band "B2" And allocation row "ALLOC-014" matches product group "MORTGAGE", region "BKK" and any exposure band, with target queue "MTG-BKK-CO" | the morning allocation run starts | the case is placed in queue "MTG-BKK-CO" And the case team is "MTG-BKK" and the region is "BKK" | RWB-E1-020 |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-008-01 | The owner is chosen by the queue's method | queue "MTG-BKK-CO" holds three case owners U-01, U-02 and U-03 with 120, 95 and 140 open cases And the last owner given a case in the queue was U-02 | case RW-2026-000201 is placed in the queue | the case is given to U-03 And the case status becomes "ASSIGNED" And an assignment record is written with reason "ALLOCATION" and rule ID "ALLOC-014" | RWB-E1-020 |
| AC-ALT-P3-008-02 | An owner at the caseload cap is skipped | the last owner given a case was U-02 And U-03, the next owner in turn, holds 150 open cases And U-01 holds 120 open cases | case RW-2026-000202 is placed in the queue | the case is given to U-01, the following owner below the cap | RWB-E1-020 |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-008-01 | No allocation row matches | a new case RW-2026-000204 with product group "SSME" and region "NE3" that matches no allocation row | the morning allocation run starts | the case is placed in the exception queue "RWB-EXC" And the case status stays "NEW" And a decision log entry is written with final call "RULE_GAP", product group "SSME" and region "NE3" And CaseAllocationFailed is published with reason "NO_ROW_MATCHED" And the allocation summary carries MSG-P3-012 with count 1 | RWB-E1-020 |
| AC-EXC-P3-008-02 | A case with an open deviation is not allocated to a case owner | a new case RW-2026-000206 with deviation_open = true | the morning allocation run starts | the case is placed in the deviation handler queue "DEV-HANDLER" named by rule R-DEV-01 And no case owner is set and the status stays "NEW" | RWB-E1-020 |
| AC-EXC-P3-008-03 | A repeated run for the same date has no further effect | the morning allocation run for 2026-12-01 has assigned case RW-2026-000201 to U-03 | the run for 2026-12-01 is started again from the job monitor | case RW-2026-000201 keeps owner U-03 and its one assignment record And no second decision log entry is written for the case And the job record shows 1 case skipped as already allocated | RWB-E1-020 |
| AC-EXC-P3-008-04 | A run with no new cases | no case has status "NEW" on 2026-12-01 | the morning allocation run starts | the run completes with 0 cases read And the allocation summary for each team shows 0 in overflow and 0 in the exception queue | RWB-E1-020 |
| AC-EXC-P3-008-05 | A queue with no overflow queue sends the case to the exception queue | queue "HP-CEN-CO" has no overflow queue And every owner in queue "HP-CEN-CO" holds 150 open cases | case RW-2026-000209 is placed in queue "HP-CEN-CO" | the case is placed in the exception queue "RWB-EXC" with reason "NO_OVERFLOW_QUEUE" And the case status stays "NEW" | RWB-E1-020 |
| AC-EXC-P3-008-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-008-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-008-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-008-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.9 Send a case to the overflow queue when no rule matches

#### A2.9.1 Intent

**Business objective.** Applies the default row when no allocation rule matches, so no case is left without a queue.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Applies the default row when no allocation rule matches, so no case is left without a queue.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Send a case to the overflow queue when no rule matches | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-07

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-009-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| VR-P3-009-2 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| VR-P3-009-3 | Allocation not recorded (RWB-E1-020) | MSG-P3-013 The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| BR-P3-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-009-01 | A new case is placed in the queue its row names | a new case RW-2026-000201 with status "NEW", product group "MORTGAGE", region "BKK" and exposure band "B2" And allocation row "ALLOC-014" matches product group "MORTGAGE", region "BKK" and any exposure band, with target queue "MTG-BKK-CO" | the morning allocation run starts | the case is placed in queue "MTG-BKK-CO" And the case team is "MTG-BKK" and the region is "BKK" | RWB-E1-020 |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-009-01 | The owner is chosen by the queue's method | queue "MTG-BKK-CO" holds three case owners U-01, U-02 and U-03 with 120, 95 and 140 open cases And the last owner given a case in the queue was U-02 | case RW-2026-000201 is placed in the queue | the case is given to U-03 And the case status becomes "ASSIGNED" And an assignment record is written with reason "ALLOCATION" and rule ID "ALLOC-014" | RWB-E1-020 |
| AC-ALT-P3-009-02 | An owner at the caseload cap is skipped | the last owner given a case was U-02 And U-03, the next owner in turn, holds 150 open cases And U-01 holds 120 open cases | case RW-2026-000202 is placed in the queue | the case is given to U-01, the following owner below the cap | RWB-E1-020 |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-009-01 | No allocation row matches | a new case RW-2026-000204 with product group "SSME" and region "NE3" that matches no allocation row | the morning allocation run starts | the case is placed in the exception queue "RWB-EXC" And the case status stays "NEW" And a decision log entry is written with final call "RULE_GAP", product group "SSME" and region "NE3" And CaseAllocationFailed is published with reason "NO_ROW_MATCHED" And the allocation summary carries MSG-P3-012 with count 1 | RWB-E1-020 |
| AC-EXC-P3-009-02 | A case with an open deviation is not allocated to a case owner | a new case RW-2026-000206 with deviation_open = true | the morning allocation run starts | the case is placed in the deviation handler queue "DEV-HANDLER" named by rule R-DEV-01 And no case owner is set and the status stays "NEW" | RWB-E1-020 |
| AC-EXC-P3-009-03 | A repeated run for the same date has no further effect | the morning allocation run for 2026-12-01 has assigned case RW-2026-000201 to U-03 | the run for 2026-12-01 is started again from the job monitor | case RW-2026-000201 keeps owner U-03 and its one assignment record And no second decision log entry is written for the case And the job record shows 1 case skipped as already allocated | RWB-E1-020 |
| AC-EXC-P3-009-04 | A run with no new cases | no case has status "NEW" on 2026-12-01 | the morning allocation run starts | the run completes with 0 cases read And the allocation summary for each team shows 0 in overflow and 0 in the exception queue | RWB-E1-020 |
| AC-EXC-P3-009-05 | A queue with no overflow queue sends the case to the exception queue | queue "HP-CEN-CO" has no overflow queue And every owner in queue "HP-CEN-CO" holds 150 open cases | case RW-2026-000209 is placed in queue "HP-CEN-CO" | the case is placed in the exception queue "RWB-EXC" with reason "NO_OVERFLOW_QUEUE" And the case status stays "NEW" | RWB-E1-020 |
| AC-EXC-P3-009-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-009-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-009-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-009-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.10 Run the transfer rule table and engine

#### A2.10.1 Intent

**Business objective.** Moves a case between queues and owners when a transfer rule fires, and records the reason.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Moves a case between queues and owners when a transfer rule fires, and records the reason.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the transfer rule table and engine | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Drools evaluator

**Prerequisites.** FEAT-CWC-06

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-010-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| VR-P3-010-2 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| BR-P3-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-010-01 | Rule-driven transfer | case RW-2026-000301 is "IN_PROGRESS" in queue "TDR-BKK-CO" with owner U-21 And transfer row "TRF-007" moves a case to queue "LIT-BKK-OFF" when ROUTE_APPROVED carries route "R4" | the route decision approves route "R4" for the case | the case is in queue "LIT-BKK-OFF" with owner U-31, the member with the lowest load And the assignment of U-21 has an end time and a new assignment has reason "TRANSFER" and rule ID "TRF-007" And the decision log entry carries rule ID "TRF-007" and rule version "TRF-2026.11" | RWB-E1-021 |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-010-01 | Manual transfer | a team manager of team "TDR-BKK" | they call the transfer endpoint for case RW-2026-000302 with reason code "MANUAL", transfer reason "R03" and target owner U-22 | the case owner is U-22 And the assignment and the decision log entry carry transfer reason "R03" | RWB-E1-021 |
| AC-ALT-P3-010-02 | One queue only | case RW-2026-000303 is in queue "TDR-BKK-CO" with record version 7 | a rule transfer to "LIT-BKK-OFF" and a manual transfer to "DIL-BKK-CO" arrive in the same second "<event>" arrives for the case | the case ends in exactly one queue And the second transfer is refused with MSG-GEN-004 And a decision log entry records the second transfer with final call "TRANSFER_REJECTED" Scenario Outline: AC4 Eight triggers Given transfer row "<row>" moves a case to queue "<queue>" on trigger "<event>" And case RW-2026-000304 meets the row's condition When "<event>" arrives for the case the case is in queue "<queue>" And the decision log entry carries rule ID "<row>" Examples: | row     | event              | queue        | | TRF-001 | CaseStateChanged   | NPA-BKK-CO   | | TRF-002 | ROUTE_APPROVED     | LIT-BKK-OFF  | | TRF-003 | TimerDue           | LIT-BKK-OFF  | | TRF-004 | DeviationRaised    | DEV-HANDLER  | | TRF-005 | DeviationCleared   | TDR-BKK-CO   | | TRF-006 | ApprovalRequested  | TDR-BKK-APR  | | TRF-008 | DocumentStored     | DIL-BKK-CO   | | TRF-009 | PaymentMissed      | TDR-BKK-CO   | | RWB-E1-021 |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-010-01 | Decision log unavailable | the decision log store is unavailable | a team manager transfers case RW-2026-000309 with transfer reason "R03" | the call is refused with 503 and MSG-P7-003 And the case keeps its queue and owner | RWB-E1-021 |
| AC-EXC-P3-010-02 | A repeated event | PaymentMissed with event ID "EVT-88120" moved case RW-2026-000311 to "TDR-BKK-CO" | PaymentMissed with event ID "EVT-88120" arrives again | the case has one transfer for the event And the repeat is counted as an idempotency hit | RWB-E1-021 |
| AC-EXC-P3-010-03 | No owner below the cap in the target queue | every member of "LIT-BKK-OFF" holds 150 open cases | row "TRF-007" fires for case RW-2026-000312 | the case is in the overflow queue "LIT-BKK-OVF" with no owner And the team manager of "LIT-BKK" is told with MSG-P3-011 and count 1 | RWB-E1-021 |
| AC-EXC-P3-010-04 | No row matches | no transfer row matches DocumentStored for case RW-2026-000314 | DocumentStored arrives for the case | the case keeps its queue and owner And no decision log entry is written | RWB-E1-021 |
| AC-EXC-P3-010-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-010-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-010-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-010-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.11 Set service levels and stage timers

#### A2.11.1 Intent

**Business objective.** Starts the service level clock on every state the case enters, from the timer table held as data.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Starts the service level clock on every state the case enters, from the timer table held as data.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Set service levels and stage timers | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Quartz scheduler

**Prerequisites.** FEAT-CWC-03

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-011-1 | A timer will expire within its warning period | MSG-P3-003 {timer} ends on {date}. |
| VR-P3-011-2 | A move not allowed from the current state | MSG-P3-005 This case cannot move to {state} from {current}. |
| R-UNI-04 | Raise X1, pause the stage clock, apply the contact stop, when a complaint is logged against the case | Moves to HELD_DEVIATION |
| R-UNI-21 | Resume the case in the state it paused in, recompute the timers, when the hold is lifted | Moves to RESUME_STATE |
| R-UNI-43 | Resume the stage clock and return the case, when the deviation owner records the outcome | Moves to RESUME_STATE |
| BR-P3-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-011-01 | Timer starts | hire purchase case RW-2026-000401 is placed in queue "LIT-BKK-OFF" with status "ASSIGNED" at 2026-12-01 09:00 | the case arrives | a SERVICE_LEVEL timer is RUNNING with expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00 And GET /cases/{caseId}/timers returns the timer with its due date | RWB-E1-028 |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-011-01 | Warning and escalation | the SERVICE_LEVEL timer of case RW-2026-000401 passes warn_at and later expires_at | the timer check runs after each point | owner U-31 receives MSG-P3-003 at the warning point And at expiry the breach is raised to RW-TEAMMGR of team "LIT-BKK" with TimerBreached and escalation level 1 And the case keeps queue "LIT-BKK-OFF" and owner U-31 And both the warning and the breach have a decision log entry, the breach with rule R-UNI-30 | RWB-E1-028 |
| AC-ALT-P3-011-02 | Prescription date | a new hire purchase case RW-2026-000402 with one account whose last payment date is 2026-03-15 | the case is created | the prescription date is 2028-03-15 And a PRESCRIPTION timer expires on 2028-03-15 with warn_at 2027-09-17 And GET /cases/{caseId} shows prescription date 2028-03-15 | RWB-E1-028 |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-011-01 | No service level for the queue and status | no SERVICE_LEVEL version is in force on 2026-12-01 | case RW-2026-000403 is placed in queue "NPA-BKK-CO" with status "ASSIGNED" on 2026-12-01 | no SERVICE_LEVEL timer starts And the case is listed on the exception queue with MSG-P3-026 for "service level" and "HIRE_PURCHASE ASSIGNED" | RWB-E1-028 |
| AC-EXC-P3-011-02 | No legal period for the product | the LEGAL_PERIOD table has no row for "SSME" | SSME case RW-2026-000404 is created | the prescription date is empty And the case is listed on the exception queue with MSG-P3-026 for "legal period" and "SSME" | RWB-E1-028 |
| AC-EXC-P3-011-03 | No payment ever made | a hire purchase case RW-2026-000405 with an account that has no last payment date and contract date 2025-06-30 | the case is created | the prescription date is 2027-06-30 | RWB-E1-028 |
| AC-EXC-P3-011-04 | A breach is raised once | the SERVICE_LEVEL timer of case RW-2026-000406 is EXPIRED with escalation level 1 | JOB-05 runs again | no second TimerBreached is published for the timer And escalation level stays 1 | RWB-E1-028 |
| AC-EXC-P3-011-05 | Decision log unavailable at a breach | the decision log store is unavailable | the SERVICE_LEVEL timer of case RW-2026-000407 passes expires_at | the timer stays RUNNING with escalation level 0 And the job record carries MSG-P7-003 for the timer And the breach is raised by the first run after the store is back | RWB-E1-028 |
| AC-EXC-P3-011-06 | A deviation pauses the stage clock and not the prescription clock | case RW-2026-000408 has a RUNNING SERVICE_LEVEL timer and a PRESCRIPTION timer | DeviationRaised arrives on 2026-12-02 and DeviationCleared on 2026-12-04 | the SERVICE_LEVEL timer was PAUSED from 2026-12-02 to 2026-12-04 and its expires_at moved by 2 working days And the PRESCRIPTION timer stayed RUNNING with the same expires_at And the case record shows MSG-P3-004 with the prescription date while the deviation was open | RWB-E1-028 |
| AC-EXC-P3-011-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-011-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-011-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-011-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.12 Set and track prescription dates

#### A2.12.1 Intent

**Business objective.** Reads the legal period from reference data, sets the prescription date and tracks it independently of stage clocks.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Reads the legal period from reference data, sets the prescription date and tracks it independently of stage clocks.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Set and track prescription dates | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Quartz scheduler

**Prerequisites.** FEAT-CWC-11

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-012-1 | A timer will expire within its warning period | MSG-P3-003 {timer} ends on {date}. |
| R-UNI-20 | Stop every outbound action and every automated decision, keep the clocks visible, when a regulator, court or Legal places a hold | Moves to HELD_LEGAL |
| BR-P3-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Legal counsel, Litigation officer | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-012-01 | Timer starts | hire purchase case RW-2026-000401 is placed in queue "LIT-BKK-OFF" with status "ASSIGNED" at 2026-12-01 09:00 | the case arrives | a SERVICE_LEVEL timer is RUNNING with expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00 And GET /cases/{caseId}/timers returns the timer with its due date | RWB-E1-028 |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-012-01 | Warning and escalation | the SERVICE_LEVEL timer of case RW-2026-000401 passes warn_at and later expires_at | the timer check runs after each point | owner U-31 receives MSG-P3-003 at the warning point And at expiry the breach is raised to RW-TEAMMGR of team "LIT-BKK" with TimerBreached and escalation level 1 And the case keeps queue "LIT-BKK-OFF" and owner U-31 And both the warning and the breach have a decision log entry, the breach with rule R-UNI-30 | RWB-E1-028 |
| AC-ALT-P3-012-02 | Prescription date | a new hire purchase case RW-2026-000402 with one account whose last payment date is 2026-03-15 | the case is created | the prescription date is 2028-03-15 And a PRESCRIPTION timer expires on 2028-03-15 with warn_at 2027-09-17 And GET /cases/{caseId} shows prescription date 2028-03-15 | RWB-E1-028 |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-012-01 | No service level for the queue and status | no SERVICE_LEVEL version is in force on 2026-12-01 | case RW-2026-000403 is placed in queue "NPA-BKK-CO" with status "ASSIGNED" on 2026-12-01 | no SERVICE_LEVEL timer starts And the case is listed on the exception queue with MSG-P3-026 for "service level" and "HIRE_PURCHASE ASSIGNED" | RWB-E1-028 |
| AC-EXC-P3-012-02 | No legal period for the product | the LEGAL_PERIOD table has no row for "SSME" | SSME case RW-2026-000404 is created | the prescription date is empty And the case is listed on the exception queue with MSG-P3-026 for "legal period" and "SSME" | RWB-E1-028 |
| AC-EXC-P3-012-03 | No payment ever made | a hire purchase case RW-2026-000405 with an account that has no last payment date and contract date 2025-06-30 | the case is created | the prescription date is 2027-06-30 | RWB-E1-028 |
| AC-EXC-P3-012-04 | A breach is raised once | the SERVICE_LEVEL timer of case RW-2026-000406 is EXPIRED with escalation level 1 | JOB-05 runs again | no second TimerBreached is published for the timer And escalation level stays 1 | RWB-E1-028 |
| AC-EXC-P3-012-05 | Decision log unavailable at a breach | the decision log store is unavailable | the SERVICE_LEVEL timer of case RW-2026-000407 passes expires_at | the timer stays RUNNING with escalation level 0 And the job record carries MSG-P7-003 for the timer And the breach is raised by the first run after the store is back | RWB-E1-028 |
| AC-EXC-P3-012-06 | A deviation pauses the stage clock and not the prescription clock | case RW-2026-000408 has a RUNNING SERVICE_LEVEL timer and a PRESCRIPTION timer | DeviationRaised arrives on 2026-12-02 and DeviationCleared on 2026-12-04 | the SERVICE_LEVEL timer was PAUSED from 2026-12-02 to 2026-12-04 and its expires_at moved by 2 working days And the PRESCRIPTION timer stayed RUNNING with the same expires_at And the case record shows MSG-P3-004 with the prescription date while the deviation was open | RWB-E1-028 |
| AC-EXC-P3-012-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-012-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-012-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-012-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.13 Escalate a breached timer to the named point

#### A2.13.1 Intent

**Business objective.** Raises a service level breach to the escalation point named in the table. The case does not move.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Raises a service level breach to the escalation point named in the table. The case does not move.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Escalate a breached timer to the named point | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-11

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-013-1 | A timer will expire within its warning period | MSG-P3-003 {timer} ends on {date}. |
| R-UNI-30 | Raise the breach to the named escalation point. The case does not move, when time in the current state exceeds the service level | Moves to ESCALATED |
| BR-P3-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-013-01 | Timer starts | hire purchase case RW-2026-000401 is placed in queue "LIT-BKK-OFF" with status "ASSIGNED" at 2026-12-01 09:00 | the case arrives | a SERVICE_LEVEL timer is RUNNING with expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00 And GET /cases/{caseId}/timers returns the timer with its due date | RWB-E1-028 |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-013-01 | Warning and escalation | the SERVICE_LEVEL timer of case RW-2026-000401 passes warn_at and later expires_at | the timer check runs after each point | owner U-31 receives MSG-P3-003 at the warning point And at expiry the breach is raised to RW-TEAMMGR of team "LIT-BKK" with TimerBreached and escalation level 1 And the case keeps queue "LIT-BKK-OFF" and owner U-31 And both the warning and the breach have a decision log entry, the breach with rule R-UNI-30 | RWB-E1-028 |
| AC-ALT-P3-013-02 | Prescription date | a new hire purchase case RW-2026-000402 with one account whose last payment date is 2026-03-15 | the case is created | the prescription date is 2028-03-15 And a PRESCRIPTION timer expires on 2028-03-15 with warn_at 2027-09-17 And GET /cases/{caseId} shows prescription date 2028-03-15 | RWB-E1-028 |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-013-01 | No service level for the queue and status | no SERVICE_LEVEL version is in force on 2026-12-01 | case RW-2026-000403 is placed in queue "NPA-BKK-CO" with status "ASSIGNED" on 2026-12-01 | no SERVICE_LEVEL timer starts And the case is listed on the exception queue with MSG-P3-026 for "service level" and "HIRE_PURCHASE ASSIGNED" | RWB-E1-028 |
| AC-EXC-P3-013-02 | No legal period for the product | the LEGAL_PERIOD table has no row for "SSME" | SSME case RW-2026-000404 is created | the prescription date is empty And the case is listed on the exception queue with MSG-P3-026 for "legal period" and "SSME" | RWB-E1-028 |
| AC-EXC-P3-013-03 | No payment ever made | a hire purchase case RW-2026-000405 with an account that has no last payment date and contract date 2025-06-30 | the case is created | the prescription date is 2027-06-30 | RWB-E1-028 |
| AC-EXC-P3-013-04 | A breach is raised once | the SERVICE_LEVEL timer of case RW-2026-000406 is EXPIRED with escalation level 1 | JOB-05 runs again | no second TimerBreached is published for the timer And escalation level stays 1 | RWB-E1-028 |
| AC-EXC-P3-013-05 | Decision log unavailable at a breach | the decision log store is unavailable | the SERVICE_LEVEL timer of case RW-2026-000407 passes expires_at | the timer stays RUNNING with escalation level 0 And the job record carries MSG-P7-003 for the timer And the breach is raised by the first run after the store is back | RWB-E1-028 |
| AC-EXC-P3-013-06 | A deviation pauses the stage clock and not the prescription clock | case RW-2026-000408 has a RUNNING SERVICE_LEVEL timer and a PRESCRIPTION timer | DeviationRaised arrives on 2026-12-02 and DeviationCleared on 2026-12-04 | the SERVICE_LEVEL timer was PAUSED from 2026-12-02 to 2026-12-04 and its expires_at moved by 2 working days And the PRESCRIPTION timer stayed RUNNING with the same expires_at And the case record shows MSG-P3-004 with the prescription date while the deviation was open | RWB-E1-028 |
| AC-EXC-P3-013-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-013-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-013-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-013-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.14 Load a rule version with validation

#### A2.14.1 Intent

**Business objective.** Takes a new rule version through a validated load, with a dry run against live cases before it takes effect.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Takes a new rule version through a validated load, with a dry run against live cases before it takes effect.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and load a rule version with validation | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, Drools evaluator

**Prerequisites.** None

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-014-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-UNI-38 | Apply it to decisions taken from that date. Open cases keep the version they were decided under, when a new rule version reaches its effective date | Moves to RESUME_STATE |
| BR-P3-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Risk and model risk officer | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-014-01 | Valid load | a template for table ALLOCATION version "ALLOC-2026.12" with 26 rows and 50 test cases that passes every check | U-41 loads it with valid from 2026-12-15 and U-51 approves it | version "ALLOC-2026.12" is in force from 2026-12-15 And the change log records author U-41, approver U-51, the load and approval times, "50 of 50 test cases passed" and the dry run count | RWB-E1-073 |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-014-01 | Test cases | the 50 test cases with expected queues And test cases "TA-07" and "TA-19" expect queue "MTG-BKK-CO" and the new rows return "MTG-CEN-CO" | validation runs | the load is refused with MSG-P3-027 for the test case check naming "TA-07" and "TA-19" | RWB-E1-073 |
| AC-ALT-P3-014-02 | Rollback | version 7, "ALLOC-2026.13", is in force and version 6, "ALLOC-2026.12", was in force before it | U-41 calls rollback once for version 7 | version 6 is in force And the change log holds the rollback with U-41, the time and the reason And a case allocated under version 7 keeps rule version "ALLOC-2026.13" on its decision log entry | RWB-E1-073 |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-014-01 | Overlap refused | rows "ALLOC-031" and "ALLOC-032" both match product group "MORTGAGE" and region "BKK" at row order 12 | validation runs | the load is refused with MSG-P3-027 for the overlap check naming "ALLOC-031" and "ALLOC-032" And version "ALLOC-2026.11" stays in force | RWB-E1-073 |
| AC-EXC-P3-014-02 | Schema error | row 9 has assignment reason "QUICK" that is not in its list | validation runs | the load is refused with MSG-P3-027 for the schema check naming row 9 and its column | RWB-E1-073 |
| AC-EXC-P3-014-03 | Missing default | the allocation rows have no last row that matches every case | validation runs | the load is refused with MSG-P3-027 for the default row check | RWB-E1-073 |
| AC-EXC-P3-014-04 | Author cannot approve | U-41 loaded version "ALLOC-2026.12" | U-41 calls approve | the call is refused with MSG-P7-002 And the version stays LOADED | RWB-E1-073 |
| AC-EXC-P3-014-05 | Rollback with no earlier version | table TRANSFER has only version "TRF-2026.11" | rollback is called for "TRF-2026.11" | the call is refused with MSG-P3-015 And "TRF-2026.11" stays in force | RWB-E1-073 |
| AC-EXC-P3-014-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-014-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-014-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-014-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.15 Roll back a rule version

#### A2.15.1 Intent

**Business objective.** Returns the engine to the previous rule version and records what was in force when each decision was taken.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Returns the engine to the previous rule version and records what was in force when each decision was taken.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and roll back a rule version | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, Drools evaluator

**Prerequisites.** FEAT-CWC-14

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-015-1 | Allocation not recorded (RWB-E1-020) | MSG-P3-013 The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| R-UNI-38 | Apply it to decisions taken from that date. Open cases keep the version they were decided under, when a new rule version reaches its effective date | Moves to RESUME_STATE |
| BR-P3-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Platform administrator | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-015-01 | Valid load | a template for table ALLOCATION version "ALLOC-2026.12" with 26 rows and 50 test cases that passes every check | U-41 loads it with valid from 2026-12-15 and U-51 approves it | version "ALLOC-2026.12" is in force from 2026-12-15 And the change log records author U-41, approver U-51, the load and approval times, "50 of 50 test cases passed" and the dry run count | RWB-E1-073 |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-015-01 | Test cases | the 50 test cases with expected queues And test cases "TA-07" and "TA-19" expect queue "MTG-BKK-CO" and the new rows return "MTG-CEN-CO" | validation runs | the load is refused with MSG-P3-027 for the test case check naming "TA-07" and "TA-19" | RWB-E1-073 |
| AC-ALT-P3-015-02 | Rollback | version 7, "ALLOC-2026.13", is in force and version 6, "ALLOC-2026.12", was in force before it | U-41 calls rollback once for version 7 | version 6 is in force And the change log holds the rollback with U-41, the time and the reason And a case allocated under version 7 keeps rule version "ALLOC-2026.13" on its decision log entry | RWB-E1-073 |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-015-01 | Overlap refused | rows "ALLOC-031" and "ALLOC-032" both match product group "MORTGAGE" and region "BKK" at row order 12 | validation runs | the load is refused with MSG-P3-027 for the overlap check naming "ALLOC-031" and "ALLOC-032" And version "ALLOC-2026.11" stays in force | RWB-E1-073 |
| AC-EXC-P3-015-02 | Schema error | row 9 has assignment reason "QUICK" that is not in its list | validation runs | the load is refused with MSG-P3-027 for the schema check naming row 9 and its column | RWB-E1-073 |
| AC-EXC-P3-015-03 | Missing default | the allocation rows have no last row that matches every case | validation runs | the load is refused with MSG-P3-027 for the default row check | RWB-E1-073 |
| AC-EXC-P3-015-04 | Author cannot approve | U-41 loaded version "ALLOC-2026.12" | U-41 calls approve | the call is refused with MSG-P7-002 And the version stays LOADED | RWB-E1-073 |
| AC-EXC-P3-015-05 | Rollback with no earlier version | table TRANSFER has only version "TRF-2026.11" | rollback is called for "TRF-2026.11" | the call is refused with MSG-P3-015 And "TRF-2026.11" stays in force | RWB-E1-073 |
| AC-EXC-P3-015-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-015-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-015-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-015-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.16 Report every rule change for audit

#### A2.16.1 Intent

**Business objective.** Produces the audit report of rule changes: who changed what, when, under which version, and the effect.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Produces the audit report of rule changes: who changed what, when, under which version, and the effect.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and report every rule change for audit | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-14

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-016-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-UNI-22 | Recompute the segment, re-run the gates, record the change, when the account is re-aged or reclassified upstream | Moves to ROUTE_D6_REOPEN |
| R-UNI-38 | Apply it to decisions taken from that date. Open cases keep the version they were decided under, when a new rule version reaches its effective date | Moves to RESUME_STATE |
| BR-P3-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Internal audit, Risk and model risk officer | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-016-01 | Change by checklist | a request "CR-2026-0042" to change "MORTGAGE" status "IN_PROGRESS" to 8 working days from 2026-12-10 And "U-REF-01" loads SERVICE_LEVEL version 4 with impact summary "412 open Mortgage cases in IN_PROGRESS" and rollback plan "Reload version 3" And the load checks pass And "U-RSK-01" approves version 4 on 2026-12-02 | "U-AUD-01" reads the change log for 2026-12-01 to 2026-12-31 | one entry shows table "SERVICE_LEVEL", version 4, request "CR-2026-0042", test result "PASSED", author "U-REF-01", approver "U-RSK-01", approved on 2026-12-02 and valid from 2026-12-10 And the entry shows 1 row changed, 0 added and 0 removed against version 3 And the approval time is before the valid from date | RWB-E2-041 |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-016-01 | Checklist skipped | SERVICE_LEVEL version 5 loaded by "U-REF-01" with valid from 2026-12-15 and never approved | the business date reaches 2026-12-15 | the reference data service still serves version 4 And the change log shows version 5 with status "VALIDATED" and approver empty | RWB-E2-041 |
| AC-ALT-P3-016-02 | Verification after the change takes effect | SERVICE_LEVEL version 4 in force from 2026-12-10 | "U-REF-01" records the verification on 2026-12-10 with the note "Timer on RW-2026-000101 shows 8 working days" | the change log entry for version 4 shows verified by "U-REF-01" on 2026-12-10 | RWB-E2-041 |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-016-01 | Checklist item missing at approval | HOLIDAY version 2 loaded with no rollback plan | "U-RSK-01" approves it | the approval is refused with MSG-P3-022 naming "rollback plan" And version 2 stays "VALIDATED" | RWB-E2-041 |
| AC-EXC-P3-016-02 | Failed test result | rule version "RULE_UNIVERSAL_RULES" version 3 whose harness result is "FAILED" with 2 of 50 tests failing | "U-RSK-01" approves it | the approval is refused with MSG-P3-022 naming "test result" | RWB-E2-041 |
| AC-EXC-P3-016-03 | Period with no changes | None | "U-AUD-01" reads the change log for 2026-11-01 to 2026-11-15 | the response is an empty list with total 0 | RWB-E2-041 |
| AC-EXC-P3-016-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-016-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-016-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-016-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.17 Rebalance queues daily

#### A2.17.1 Intent

**Business objective.** Moves cases between owners overnight to hold the caseload inside the cap and keep the spread even.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.17.2 Description

**Functional overview.** Moves cases between owners overnight to hold the caseload inside the cap and keep the spread even.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Rebalance queues daily | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-08

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-017-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| R-UNI-19 | Reallocate the newest cases until the owner is inside the cap, when the owner is above the maximum caseload | Moves to REALLOCATED |
| BR-P3-017 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-017-01 | Rebalance | queue "TDR-BKK-CO" has 12 cases with no owner And members U-61 and U-62 hold 140 and 144 open cases | JOB-06 runs | the 12 cases are assigned, 8 to U-61 and 4 to U-62, by lowest load with ties going to the member first in the queue list And each assignment has reason "REBALANCE" and a decision log entry | RWB-E1-030 |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-017-01 | Measures reconcile | the snapshot taken at 2026-12-02 06:52 | the queue report refreshes | the depth of each queue equals the case list count for that queue at 06:52 And queue "TDR-BKK-CO" shows depth 296, unassigned 0 and an average age of 41 days | RWB-E1-030 |
| AC-ALT-P3-017-02 | A count difference holds the snapshot | the snapshot depth for "DIL-BKK-CO" is 88 and the case count at the same time is 87 | the snapshot is checked | it is not published And the data steward receives MSG-P3-029 with check "queue depth against case list" | RWB-E1-030 |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-017-01 | Breach alert | case RW-2026-000501 in queue "TDR-BKK-CO" passes its service level | the timer check raises the breach | the team manager of "TDR-BKK" receives MSG-P3-028 with count 1 and queue "TDR-BKK-CO" And the next snapshot shows 1 breach for "TDR-BKK-CO" in Power BI | RWB-E1-030 |
| AC-EXC-P3-017-02 | No member has capacity | every member of "TDR-BKK-CO" holds 150 open cases and 5 cases have no owner | JOB-06 runs | the 5 cases keep no owner And the team manager receives MSG-P3-011 with count 5 | RWB-E1-030 |
| AC-EXC-P3-017-03 | No cap loaded | queue "WO-BKK-CO" has no capacity cap | JOB-06 runs | no case in "WO-BKK-CO" is moved And the snapshot still reports "WO-BKK-CO" | RWB-E1-030 |
| AC-EXC-P3-017-04 | Decision log unavailable for one case | owner U-63 holds 153 open cases and the decision log write fails for the second of the 3 newest cases | JOB-06 runs | 2 cases are moved off U-63 and 1 stays And the job record lists the case that stayed with MSG-P7-003 | RWB-E1-030 |
| AC-EXC-P3-017-05 | A repeated run | JOB-06 has balanced "TDR-BKK-CO" on 2026-12-02 | JOB-06 runs again on 2026-12-02 | no case is moved And no decision log entry is written | RWB-E1-030 |
| AC-EXC-P3-017-06 | Held cases are not moved | owner U-64 holds 152 open cases and the 2 newest have deviation_open = true | JOB-06 runs | those 2 cases stay with U-64 and the next 2 newest are moved | RWB-E1-030 |
| AC-EXC-P3-017-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-017-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-017-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-017-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.18 Publish queue measures

#### A2.18.1 Intent

**Business objective.** Calculates queue depth, ageing and the owner spread, and publishes them to the case list and Power BI.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.18.2 Description

**Functional overview.** Calculates queue depth, ageing and the owner spread, and publishes them to the case list and Power BI.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Publish queue measures | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Power BI

**Prerequisites.** FEAT-CWC-17

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-018-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| R-UNI-34 | Move to the exception queue and raise a task for the owner, when an outbound call fails after the retry limit | Moves to EXCEPTION_QUEUE |
| BR-P3-018 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager, Reporting and BI analyst | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-018-01 | Rebalance | queue "TDR-BKK-CO" has 12 cases with no owner And members U-61 and U-62 hold 140 and 144 open cases | JOB-06 runs | the 12 cases are assigned, 8 to U-61 and 4 to U-62, by lowest load with ties going to the member first in the queue list And each assignment has reason "REBALANCE" and a decision log entry | RWB-E1-030 |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-018-01 | Measures reconcile | the snapshot taken at 2026-12-02 06:52 | the queue report refreshes | the depth of each queue equals the case list count for that queue at 06:52 And queue "TDR-BKK-CO" shows depth 296, unassigned 0 and an average age of 41 days | RWB-E1-030 |
| AC-ALT-P3-018-02 | A count difference holds the snapshot | the snapshot depth for "DIL-BKK-CO" is 88 and the case count at the same time is 87 | the snapshot is checked | it is not published And the data steward receives MSG-P3-029 with check "queue depth against case list" | RWB-E1-030 |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-018-01 | Breach alert | case RW-2026-000501 in queue "TDR-BKK-CO" passes its service level | the timer check raises the breach | the team manager of "TDR-BKK" receives MSG-P3-028 with count 1 and queue "TDR-BKK-CO" And the next snapshot shows 1 breach for "TDR-BKK-CO" in Power BI | RWB-E1-030 |
| AC-EXC-P3-018-02 | No member has capacity | every member of "TDR-BKK-CO" holds 150 open cases and 5 cases have no owner | JOB-06 runs | the 5 cases keep no owner And the team manager receives MSG-P3-011 with count 5 | RWB-E1-030 |
| AC-EXC-P3-018-03 | No cap loaded | queue "WO-BKK-CO" has no capacity cap | JOB-06 runs | no case in "WO-BKK-CO" is moved And the snapshot still reports "WO-BKK-CO" | RWB-E1-030 |
| AC-EXC-P3-018-04 | Decision log unavailable for one case | owner U-63 holds 153 open cases and the decision log write fails for the second of the 3 newest cases | JOB-06 runs | 2 cases are moved off U-63 and 1 stays And the job record lists the case that stayed with MSG-P7-003 | RWB-E1-030 |
| AC-EXC-P3-018-05 | A repeated run | JOB-06 has balanced "TDR-BKK-CO" on 2026-12-02 | JOB-06 runs again on 2026-12-02 | no case is moved And no decision log entry is written | RWB-E1-030 |
| AC-EXC-P3-018-06 | Held cases are not moved | owner U-64 holds 152 open cases and the 2 newest have deviation_open = true | JOB-06 runs | those 2 cases stay with U-64 and the next 2 newest are moved | RWB-E1-030 |
| AC-EXC-P3-018-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-018-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-018-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-018-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.19 Show queue and owner on the case list

#### A2.19.1 Intent

**Business objective.** Puts the queue and the named owner on every row of the case list, so the owner question is answered on one screen.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.19.2 Description

**Functional overview.** Puts the queue and the named owner on every row of the case list, so the owner question is answered on one screen.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and show queue and owner on the case list | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench; account columns from `v_ace_account` by `case_list_row.account_key`

**Prerequisites.** FEAT-RDF-18

#### A2.19.3 Business rules and structure

##### A2.19.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-019-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| R-UNI-34 | Move to the exception queue and raise a task for the owner, when an outbound call fails after the retry limit | Moves to EXCEPTION_QUEUE |
| BR-P3-019 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.19.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.19.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Team manager | Also uses |

#### A2.19.4 Acceptance criteria

##### A2.19.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-019-01 | Filter by queue | the case list | U-71 filters by queue "DIL-BKK-CO" | 64 cases show, each with its owner and status And no case from another queue shows | RWB-E1-031 |

##### A2.19.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-019-01 | Export | the list filtered by queue "DIL-BKK-CO" and status "ASSIGNED" with 51 cases | U-71 chooses Export | an Excel file with 51 rows downloads And the access log holds the export with user U-71, the time, the filters and 51 rows | RWB-E1-031 |
| AC-ALT-P3-019-02 | Queue outside the scope | None | U-71 filters by queue "LIT-BKK-OFF" of team "LIT-BKK" | no case shows And the list shows the empty state with MSG-P3-020 | RWB-E1-031 |

##### A2.19.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-019-01 | No case meets the filters | None | U-71 filters by queue "DIL-BKK-CO" and status "WAITING_PARTNER" and no case matches | the list shows the empty state with MSG-P3-020 | RWB-E1-031 |
| AC-EXC-P3-019-02 | Export above the limit | parameter "caselist.export.maxrows" is 10000 And a filtered list of 10,001 cases for a user with scope All | the user chooses Export | no file is made And MSG-P3-021 shows with maximum 10000 | RWB-E1-031 |
| AC-EXC-P3-019-03 | Access log unavailable | the access log store is unavailable | U-71 chooses Export on a list of 51 cases | no file is made And MSG-P7-003 shows | RWB-E1-031 |
| AC-EXC-P3-019-04 | A case with no owner | case RW-2026-000601 is in queue "DIL-BKK-OVF" with no owner | U-71 filters by queue "DIL-BKK-OVF" | case RW-2026-000601 shows with a blank owner cell | RWB-E1-031 |
| AC-EXC-P3-019-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-019-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.19.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-019-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-019-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.20 Expose the workflow admin API

#### A2.20.1 Intent

**Business objective.** Gives administration a programmatic way to move, reassign and correct a case with a reason code, before screens exist.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.20.2 Description

**Functional overview.** Gives administration a programmatic way to move, reassign and correct a case with a reason code, before screens exist.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Platform administrator | Opens the screen and expose the workflow admin API | Checks the role, the capability area and the scope |
| 2 | Platform administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-03

#### A2.20.3 Business rules and structure

##### A2.20.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-020-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| BR-P3-020 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.20.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.20.3.3 Roles and permissions

| Role | Use |
|---|---|
| Platform administrator | Primary |
| Team manager | Also uses |

#### A2.20.4 Acceptance criteria

##### A2.20.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-020-01 | Case created at 90 days past due | account A-5001 of customer P-0101, product group "HIRE_PURCHASE", reaches 90 days past due in `v_ace_account` for the completed ACE business date with no exclusion And the last case number issued in 2026 is RW-2026-000122 | the entry rule runs | case RW-2026-000123 exists with status "NEW", no stage code and entry date 2026-12-01 And case_account holds account_key A-5001 as the primary account and case_party holds person_key P-0101 as "BORROWER" And recovery_case.primary_person_key is P-0101 And CaseCreated is published with case number RW-2026-000123 | RWB-E1-018 |

##### A2.20.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-020-01 | Exclusion applied | account A-5002 at 92 days past due with tdr_flag = true | the entry rule runs | no case is created for A-5002 And an exclusion record holds account A-5002, reason "ACTIVE_PLAN", the exclusion rule ID and version "EXCL-2026.11" | RWB-E1-018 |
| AC-ALT-P3-020-02 | One case per customer and product | customer P-0102 has two hire purchase accounts A-5003 and A-5004, both at 95 days past due | the entry rule runs | one case exists for P-0102 and "HIRE_PURCHASE" with both accounts linked And total outstanding at entry is the sum of the two balances, THB 412,350.00 | RWB-E1-018 |

##### A2.20.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-020-01 | A repeated run creates nothing new | JOB-02 has created case RW-2026-000125 for account A-5008 on 2026-12-01 | JOB-02 runs again for 2026-12-01 | account A-5008 has one case link And no case number is issued in the second run | RWB-E1-018 |
| AC-EXC-P3-020-02 | No cases before the ACE batch is complete | `v_ace_batch_status` shows the ALS batch for business date 2026-12-02 with a status other than "COMPLETED" | the morning schedule runs | JOB-02 does not start for 2026-12-02 And the job monitor shows MSG-P1-001 for the account data product And JOB-02 starts for 2026-12-02 when AceDataReady (EV-26) is raised for ALS and 2026-12-02 | RWB-E1-018 |
| AC-EXC-P3-020-03 | The decision log write fails | the decision log store is unavailable | the entry rule runs for account A-5009 | no case exists for A-5009 And the job record lists A-5009 as failed with MSG-P7-003 And A-5009 is taken again in the next run | RWB-E1-018 |
| AC-EXC-P3-020-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-020-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.20.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-020-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-020-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.21 Log every workflow event

#### A2.21.1 Intent

**Business objective.** Writes every state change, timer, allocation and transfer as an event with its rule ID and version.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.21.2 Description

**Functional overview.** Writes every state change, timer, allocation and transfer as an event with its rule ID and version.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Log every workflow event | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-02

#### A2.21.3 Business rules and structure

##### A2.21.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-021-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| VR-P3-021-2 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| VR-P3-021-3 | A timer will expire within its warning period | MSG-P3-003 {timer} ends on {date}. |
| R-UNI-47 | Stop every open action, close the case as sold, transfer the data, when the account is awarded in a debt sale lot while on another route | Moves to CASE_CLOSED_SOLD |
| BR-P3-021 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.21.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit | Also uses |

#### A2.21.4 Acceptance criteria

##### A2.21.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-021-01 | Case created at 90 days past due | account A-5001 of customer P-0101, product group "HIRE_PURCHASE", reaches 90 days past due in `v_ace_account` for the completed ACE business date with no exclusion And the last case number issued in 2026 is RW-2026-000122 | the entry rule runs | case RW-2026-000123 exists with status "NEW", no stage code and entry date 2026-12-01 And case_account holds account_key A-5001 as the primary account and case_party holds person_key P-0101 as "BORROWER" And recovery_case.primary_person_key is P-0101 And CaseCreated is published with case number RW-2026-000123 | RWB-E1-018 |

##### A2.21.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-021-01 | Exclusion applied | account A-5002 at 92 days past due with tdr_flag = true | the entry rule runs | no case is created for A-5002 And an exclusion record holds account A-5002, reason "ACTIVE_PLAN", the exclusion rule ID and version "EXCL-2026.11" | RWB-E1-018 |
| AC-ALT-P3-021-02 | One case per customer and product | customer P-0102 has two hire purchase accounts A-5003 and A-5004, both at 95 days past due | the entry rule runs | one case exists for P-0102 and "HIRE_PURCHASE" with both accounts linked And total outstanding at entry is the sum of the two balances, THB 412,350.00 | RWB-E1-018 |

##### A2.21.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-021-01 | A repeated run creates nothing new | JOB-02 has created case RW-2026-000125 for account A-5008 on 2026-12-01 | JOB-02 runs again for 2026-12-01 | account A-5008 has one case link And no case number is issued in the second run | RWB-E1-018 |
| AC-EXC-P3-021-02 | No cases before the ACE batch is complete | `v_ace_batch_status` shows the ALS batch for business date 2026-12-02 with a status other than "COMPLETED" | the morning schedule runs | JOB-02 does not start for 2026-12-02 And the job monitor shows MSG-P1-001 for the account data product And JOB-02 starts for 2026-12-02 when AceDataReady (EV-26) is raised for ALS and 2026-12-02 | RWB-E1-018 |
| AC-EXC-P3-021-03 | The decision log write fails | the decision log store is unavailable | the entry rule runs for account A-5009 | no case exists for A-5009 And the job record lists A-5009 as failed with MSG-P7-003 And A-5009 is taken again in the next run | RWB-E1-018 |
| AC-EXC-P3-021-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-021-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.21.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-021-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-021-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.22 Hold the parameter catalog and configuration service

#### A2.22.1 Intent

**Business objective.** Keeps every limit, threshold, name and timer as a versioned parameter row that changes without a release.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.22.2 Description

**Functional overview.** Keeps every limit, threshold, name and timer as a versioned parameter row that changes without a release.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and hold the parameter catalog and configuration service | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** None

#### A2.22.3 Business rules and structure

##### A2.22.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-022-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| VR-P3-022-2 | A timer will expire within its warning period | MSG-P3-003 {timer} ends on {date}. |
| BR-P3-022 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.22.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.22.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Platform administrator | Also uses |

#### A2.22.4 Acceptance criteria

##### A2.22.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-022-01 | Parameter read at run time | the parameter "case.entry.dpd" set to 90 in PROD, version 1 | the case service evaluates entry on 2026-12-01 | it uses 90 from the service, not a constant in code And the entry decision records parameter version 1 | RWB-E1-042 |

##### A2.22.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-022-01 | Hard-coded value caught | code in package "recovery.casewf.casecreation" with a literal 90 in the entry rule | the lint rule for magic numbers runs in the build | the build fails And the output names the file, the line and the parameter "case.entry.dpd" | RWB-E1-042 |
| AC-ALT-P3-022-02 | Catalog complete | the parameter catalog And code that reads the key "allocation.retry.limit" which the catalog does not list | the pipeline compares the catalog with the parameters read by the services | the build fails naming "allocation.retry.limit" And every other parameter in use is in the catalog with an owner and a default | RWB-E1-042 |

##### A2.22.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-022-01 | Required value missing at start-up | "refdata.cache.ttl-seconds" is required and has no value and no default for UAT | the service starts in UAT | the health check fails with MSG-P3-032 for "refdata.cache.ttl-seconds" and "UAT" And the service takes no traffic | RWB-E1-042 |
| AC-EXC-P3-022-02 | Author cannot approve | RW-COE user U-41 loaded value version 3 | U-41 approves version 3 | the approval is refused with MSG-P7-002 | RWB-E1-042 |
| AC-EXC-P3-022-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-022-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.22.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-022-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-022-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.23 Run the reference data service with versioned tables

#### A2.23.1 Intent

**Business objective.** Serves every reference table to the engines with its version, so a decision records which version it used.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.23.2 Description

**Functional overview.** Serves every reference table to the engines with its version, so a decision records which version it used.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Reference data administrator | Opens the screen and run the reference data service with versioned tables | Checks the role, the capability area and the scope |
| 2 | Reference data administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-22

#### A2.23.3 Business rules and structure

##### A2.23.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-023-1 | Allocation not recorded (RWB-E1-020) | MSG-P3-013 The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| R-UNI-20 | Stop every outbound action and every automated decision, keep the clocks visible, when a regulator, court or Legal places a hold | Moves to HELD_LEGAL |
| BR-P3-023 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.23.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.23.3.3 Roles and permissions

| Role | Use |
|---|---|
| Reference data administrator | Primary |
| Center of excellence analyst | Also uses |

#### A2.23.4 Acceptance criteria

##### A2.23.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-023-01 | Versioned row | "U-REF-01" loads table "EXPOSURE_BAND" with bands "E1" to "E5" and valid from 2026-12-01 And "U-RSK-01" approves the load | the allocation engine reads "EXPOSURE_BAND" for business date 2026-11-30 | version 4 exists with status "APPROVED" and 5 rows And version 3 stays readable with its 4 rows and has valid to 2026-11-30 And the service returns version 3 for business date 2026-11-30 And the service returns version 4 for business date 2026-12-01 | RWB-E1-043 |

##### A2.23.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-023-01 | Approver recorded | "U-REF-01" loads table "DELEGATION_LIMIT" with 24 rows and valid from 2026-12-01 | "U-REF-01" tries to approve the same load | the approval is refused with MSG-P7-002 And the version stays "VALIDATED" with no approver And the service still returns the previous "DELEGATION_LIMIT" version for business date 2026-12-01 | RWB-E1-043 |
| AC-ALT-P3-023-02 | Read by services | approved versions are in force for "QUEUE" version 7, "SERVICE_LEVEL" version 2 and "HOLIDAY" version 1 | the case service and the allocation engine start for business date 2026-11-30 | each reads every table it uses from the reference data service And each writes one log line per table with the table code, the version number and the business date And no log line contains a party identifier | RWB-E1-043 |

##### A2.23.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-023-01 | Row fails the schema check | a "SERVICE_LEVEL" load file whose row 12 has the text "five" in the column "limit_days" | "U-REF-01" loads it | the load is refused with MSG-P3-027 naming row 12 and column "limit_days" And no version and no rows are written | RWB-E1-043 |
| AC-EXC-P3-023-02 | Approval with no approver | a "HOLIDAY" version 2 with status "VALIDATED" and valid from 2026-12-01 | the business date reaches 2026-12-01 with no approval recorded | the service returns "HOLIDAY" version 1 And version 2 stays "VALIDATED" | RWB-E1-043 |
| AC-EXC-P3-023-03 | No version in force | the table "TEAM" has no approved version with valid from on or before 2026-11-30 | the allocation engine starts for business date 2026-11-30 | the engine does not start its run And an alert names table "TEAM" and business date 2026-11-30 with MSG-P3-027 | RWB-E1-043 |
| AC-EXC-P3-023-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-023-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.23.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-023-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-023-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.24 Run versioned migrations with parameterized schema names

#### A2.24.1 Intent

**Business objective.** Applies database changes through versioned migrations with no hard-coded schema name.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.24.2 Description

**Functional overview.** Applies database changes through versioned migrations with no hard-coded schema name.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Platform administrator | Opens the screen and run versioned migrations with parameterized schema names | Checks the role, the capability area and the scope |
| 2 | Platform administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** PostgreSQL

**Prerequisites.** None

#### A2.24.3 Business rules and structure

##### A2.24.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-024-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P3-024 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.24.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.24.3.3 Roles and permissions

| Role | Use |
|---|---|
| Platform administrator | Primary |

#### A2.24.4 Acceptance criteria

##### A2.24.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-024-01 | Migration applied | migration V12__add_queue_to_case.sql with the header "-- Story: RWB-E1-020" | the deployment runs | the migration applies once And its version 12 and its checksum are recorded in "flyway_schema_history_recovery" And a second deployment run applies nothing and changes no object | RWB-E1-044 |

##### A2.24.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-024-01 | Drift detected | a column "note_x" added by hand to table "queue" in SIT | the migration check runs | the pipeline fails with MSG-P3-016 naming "rwb_case.queue.note_x" And no deployment to SIT starts | RWB-E1-044 |
| AC-ALT-P3-024-02 | Schema name as parameter | RWB_SCHEMA set to "rwb_case" in DEV and in SIT | the migration V13__create_timer.sql runs in DEV and in SIT | the table "timer" exists in schema "rwb_case" in both environments And the file V13__create_timer.sql is byte for byte the same in both runs | RWB-E1-044 |

##### A2.24.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-024-01 | Migration fails part way | V17__add_two_columns.sql whose second statement refers to a table that does not exist | the deployment runs in DEV | the first statement is rolled back And the history records version 17 as failed And the service does not start and the run shows "failed" on the job monitor | RWB-E1-044 |
| AC-EXC-P3-024-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-024-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.24.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-024-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-024-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.25 Set product parameters without a code change

#### A2.25.1 Intent

**Business objective.** Lets Mortgage, HP and SSME carry different limits, timers and rules from parameter rows alone.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.25.2 Description

**Functional overview.** Lets Mortgage, HP and SSME carry different limits, timers and rules from parameter rows alone.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and set product parameters without a code change | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-22

#### A2.25.3 Business rules and structure

##### A2.25.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-025-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| BR-P3-025 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.25.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.25.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Product head (Mortgage, HP, SSME) | Also uses |

#### A2.25.4 Acceptance criteria

##### A2.25.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-025-01 | Product value differs | case "RW-2026-000101" with product group "MORTGAGE" and case "RW-2026-000102" with product group "HIRE_PURCHASE" | the timer engine sets the notice timer on both cases on 2026-12-01 | the notice timer of "RW-2026-000101" expires on 2026-12-31 And the notice timer of "RW-2026-000102" expires on 2027-01-30 And each timer start records PRODUCT_PARAMETER version 2 | RWB-E1-045 |

##### A2.25.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-025-01 | New product added | PRODUCT version 2 adds product group "AUTO_LEASE" with valid from 2026-12-05 And PRODUCT_PARAMETER version 3 and SERVICE_LEVEL version 3 add every required row for "AUTO_LEASE" with valid from 2026-12-05 And all three versions are approved | `v_ace_account` for ACE business date 2026-12-05 carries an "AUTO_LEASE" account at 90 days past due | a case with product group "AUTO_LEASE" is created And its timers are set from the "AUTO_LEASE" rows And no deployment took place between 2026-12-01 and 2026-12-05 | RWB-E1-045 |
| AC-ALT-P3-025-02 | Value outside its range | the catalog range for NOTICE_PERIOD_DAYS is 1 to 365 | a PRODUCT_PARAMETER load sets NOTICE_PERIOD_DAYS to 0 for "SSME" | the load is refused with MSG-GEN-002 naming "NOTICE_PERIOD_DAYS", 1 and 365 | RWB-E1-045 |

##### A2.25.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-025-01 | Missing parameter blocked | a SERVICE_LEVEL load with valid from 2026-12-10 that has no row for "SSME" and status "WAITING_PARTNER" | the load validates | the load is refused with MSG-P3-034 naming "SSME" and "WAITING_PARTNER" And SERVICE_LEVEL version 3 stays in force | RWB-E1-045 |
| AC-EXC-P3-025-02 | Duplicate product row | a PRODUCT_PARAMETER load with two NOTICE_PERIOD_DAYS rows for "MORTGAGE", 30 and 45 | the load validates | the load is refused with MSG-P3-027 naming "MORTGAGE" and "NOTICE_PERIOD_DAYS" | RWB-E1-045 |
| AC-EXC-P3-025-03 | No parameter in force at run time | case "RW-2026-000140" with product group "SSME" and no NOTICE_PERIOD_DAYS row for "SSME" in force | the timer engine sets the notice timer on 2026-12-01 | no notice timer is written And the case is placed in the exception queue with MSG-P3-034 naming "SSME" and "NOTICE_PERIOD_DAYS" | RWB-E1-045 |
| AC-EXC-P3-025-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-025-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.25.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-025-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-025-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.26 Control module release with dated feature flags

#### A2.26.1 Intent

**Business objective.** Turns a module on by environment behind a flag that carries the date it must be removed.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.26.2 Description

**Functional overview.** Turns a module on by environment behind a flag that carries the date it must be removed.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Platform administrator | Opens the screen and control module release with dated feature flags | Checks the role, the capability area and the scope |
| 2 | Platform administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** None

#### A2.26.3 Business rules and structure

##### A2.26.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-026-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P3-026 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.26.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.26.3.3 Roles and permissions

| Role | Use |
|---|---|
| Platform administrator | Primary |
| Tribe lead and squad members | Also uses |

#### A2.26.4 Acceptance criteria

##### A2.26.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-026-01 | Flag off by default | the flag has no value set for UAT | the case list service starts in UAT | FeatureFlags.isOn("rwb.casewf.case-list-queue-column") returns false And the queue column is hidden on SCR-02 Case list | RWB-E1-047 |

##### A2.26.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-026-01 | Flag switched on | a platform administrator sets the flag to on in UAT with reason "UAT test of queue column" at 10:15 | the case list page is reloaded at 10:16 | the queue column shows without a deployment And a change row holds environment "UAT", old value off, new value on, the user and the time 10:15 And the ACE audit log holds the same change | RWB-E1-047 |
| AC-ALT-P3-026-02 | Flag expiry | flag "rwb.p5.ocr-intake" has removal date 2026-11-30 and owner team "P5 squad" And today is Monday 2026-12-07 | the weekly flag report runs at 08:00 | the flag is listed for removal with its owner and 7 days past its removal date And the report carries message MSG-P2-003 for the flag And flag "rwb.casewf.case-list-queue-column" with removal date 2027-01-31 is not listed | RWB-E1-047 |

##### A2.26.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-026-01 | Change without a reason refused | None | a platform administrator sets the flag to on in SIT with an empty reason | the response is 422 with message MSG-GEN-001 And the flag stays off in SIT | RWB-E1-047 |
| AC-EXC-P3-026-02 | Flag store unavailable | the flag is on in UAT and the cache holds the value from 10:20 | the flag table cannot be read at 10:21 | FeatureFlags.isOn returns true from the cache And after a restart with the table still unavailable it returns false | RWB-E1-047 |
| AC-EXC-P3-026-03 | Change to a key that does not exist | None | a platform administrator sends a change for flag "rwb.p9.unknown" | the response is 404 with message MSG-P2-016 | RWB-E1-047 |
| AC-EXC-P3-026-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-026-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.26.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-026-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-026-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.27 Take the case hand-over from EFS with full history

#### A2.27.1 Intent

**Business objective.** Takes the account at case entry and reads its contact and promise history from the EFS data ACE ingests, through `v_ace_efs_action`.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.27.2 Description

**Functional overview.** Takes the account at case entry and reads its contact and promise history from the EFS data ACE ingests, through `v_ace_efs_action`.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Take the case hand-over from EFS with full history | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database (`v_ace_account`, `v_ace_efs_action`, `v_ace_batch_status`), Workbench

**Prerequisites.** RWB-E1-069 (ACE source views); RWB-ACE-001 for `v_ace_batch_status`

#### A2.27.3 Business rules and structure

##### A2.27.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-027-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P3-027 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.27.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.27.4 Acceptance criteria

##### A2.27.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-027-01 | Case from the ACE data | synthetic account "A-0001" for customer "C-0001", product group "MORTGAGE", reached 90 days past due in `v_ace_account` for ACE business date 2026-12-14 And `v_ace_efs_action` holds 14 contact records and 2 promises for "A-0001" in its collection period | AceDataReady is raised for ALS and EFS business date 2026-12-14 and the morning case creation runs on 2026-12-15 | a case exists with status "NEW", product group "MORTGAGE", entry date 2026-12-15 and days past due at entry 90 And the case timeline shows the 16 EFS entries read from `v_ace_efs_action` by account_key with source system "EFS" And no copy of them is written to a Workbench table And the decision log entry for the creation holds business date 2026-12-14 in its inputs snapshot And CaseCreated is published with business date 2026-12-14 | RWB-E2-001 |

##### A2.27.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-027-01 | Account linked to the open case | customer "C-0002" has open case "RW-2026-000210" for product group "SSME" And synthetic account "A-0002" of "C-0002", product group "SSME", reaches 90 days past due on 2026-12-14 | case creation runs | no new case is created And "A-0002" is linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false | RWB-E2-001 |
| AC-ALT-P3-027-02 | Cases created on the next complete ACE batch | no case creation ran for business date 2026-12-15 And `v_ace_batch_status` shows the ALS batch for business date 2026-12-16 completed at 05:15 on 2026-12-17 | AceDataReady is raised and case creation runs | accounts that reached 90 days past due on 2026-12-15 or 2026-12-16 get cases with entry date 2026-12-17 And the run summary names the gap date 2026-12-15 | RWB-E2-001 |

##### A2.27.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-027-01 | Repeat run | the run for business date 2026-12-14 created the case for "A-0001" | AceDataReady for business date 2026-12-14 is received again and case creation runs again | no second case is created and nothing is written for "A-0001" And the run summary shows 1 repeat for "A-0001" | RWB-E2-001 |
| AC-EXC-P3-027-02 | Late ACE batch | `v_ace_batch_status` shows no completed ALS batch for business date 2026-12-15 at the 09:00 cut-off on 2026-12-16 | case creation is due | no case is created from the data of 2026-12-14 And the data products show message MSG-P1-001 with the date 2026-12-14 And AceDataLate (EV-27) is raised And the data steward is alerted with message MSG-P2-007 | RWB-E2-001 |
| AC-EXC-P3-027-03 | Customer not in ACE | synthetic account "A-0003" reaches 90 days past due and `v_ace_ca_relation` names a borrower person_key that `v_ace_customer` does not return | case creation runs | no case is created for "A-0003" And reconciliation rule REC-05 lists "A-0003" and the missing person_key for the data steward And "A-0003" is tried again on the next complete ACE batch | RWB-E2-001 |
| AC-EXC-P3-027-04 | Decision log write fails | the decision log store is unavailable | case creation runs for "A-0004" | no case is created for "A-0004" And an incident is raised and the run summary carries message MSG-P7-003 And "A-0004" is taken in the next run | RWB-E2-001 |
| AC-EXC-P3-027-05 | Second start refused | JOB-02 is running for business date 2026-12-14 | a platform administrator requests a rerun of JOB-02 | the response is 409 with message MSG-P2-006 | RWB-E2-001 |
| AC-EXC-P3-027-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-027-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.27.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-027-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-027-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.28 Read the ACE plan status

#### A2.28.1 Intent

**Business objective.** Reads the restructure plan status from the ACE common module, so an active plan is known on the case.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.28.2 Description

**Functional overview.** Reads the restructure plan status from the ACE common module, so an active plan is known on the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Read the ACE plan status | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE and TDR, read through `v_ace_plan`

**Prerequisites.** FEAT-CHO-01

#### A2.28.3 Business rules and structure

##### A2.28.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-028-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P3-028 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.28.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.28.4 Acceptance criteria

##### A2.28.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-028-01 | Plan status on the case | plan "TDR-SYN-0310" has status "APPROVED" in ACE with status date 2026-12-10 | the case record view loads on 2026-12-11 | the case shows plan "TDR-SYN-0310" with status "Approved" and date 2026-12-10 And the Drools evaluator reads plan_status "APPROVED" for the case And rule R-LIT-02 does not fire for the case because plan_status is not broken | RWB-E2-002 |

##### A2.28.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-028-01 | Broken plan | the case is in route state "PLAN_CURE_PERIOD" with break count 0 And plan "TDR-SYN-0310" has status "BROKEN" in ACE with status date 2026-12-14 | the daily case update runs on 2026-12-15 | the case plan status is "BROKEN" with date 2026-12-14 And the route state moves to "PLAN_BROKEN" by R-RES-29 and then to "BACK_TO_ROUTE_DECISION" by R-RES-30 And the case is in the case owner's queue with a task due in 5 working days And a decision log entry is written for each move with the rule ID and version | RWB-E2-002 |
| AC-ALT-P3-028-02 | Unknown status code | ACE returns status "SUSPENDED" for plan "TDR-SYN-0310" | the daily case update runs | the stored status does not change And a reconciliation break (reconciliation_result) with check "Lists of values" names the code "SUSPENDED" | RWB-E2-002 |

##### A2.28.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-028-01 | Status not available | the case holds plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01 And ACE returns no status for "TDR-SYN-0310" | the daily case update runs on 2026-12-15 | the case keeps status "BOOKED" with date 2026-12-01 And the case record view shows message MSG-P2-008 with the date 2026-12-01 And a reconciliation break (reconciliation_result) with product "DP04" lists plan "TDR-SYN-0310" for the ACE team | RWB-E2-002 |
| AC-EXC-P3-028-02 | ACE unavailable | `v_ace_plan` does not answer within 2 seconds | the daily case update runs on 2026-12-16 | no plan status is changed And the run summary carries message MSG-GEN-006 with system "ACE database" And the next run retries every case | RWB-E2-002 |
| AC-EXC-P3-028-03 | Decision log write fails on a broken plan | the decision log store is unavailable | the daily case update finds plan "TDR-SYN-0310" broken | the route state stays "PLAN_CURE_PERIOD" And an incident is raised with message MSG-P7-003 And the event is raised again in the next run | RWB-E2-002 |
| AC-EXC-P3-028-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-028-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.28.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-028-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-028-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.29 Read customer facts from ACE

#### A2.29.1 Intent

**Business objective.** Reads the customer profile and product holding ACE ingests from SCBPDM and the core bank, through `v_ace_customer` and `v_ace_party_product` (DL20 as amended by D-RCV-35).

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.29.2 Description

**Functional overview.** Reads the customer profile and product holding ACE ingests from SCBPDM and the core bank, through `v_ace_customer` and `v_ace_party_product` (DL20 as amended by D-RCV-35).

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Read customer facts from ACE | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database (`v_ace_customer`, `v_ace_party_product`, `v_ace_batch_status`)

**Prerequisites.** RWB-E1-069; RWB-ACE-001 for `v_ace_party_product` (behind its flag until it lands). FEAT-DRI-09 is removed by D-RCV-35

#### A2.29.3 Business rules and structure

##### A2.29.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-029-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P3-029 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.29.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.29.4 Acceptance criteria

##### A2.29.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-029-01 | Other products shown | `v_ace_party_product` shows that person_key "C-0410" holds a revolving credit line "A-0411" with status "ACTIVE" and a personal loan "A-0412" with status "DELINQUENT", both with data as of 2026-12-14 | the case record view loads for a case owner | the other products panel shows 2 products with their type and status And each product shows the business date 2026-12-14 And account "A-0410" is not listed because it is on the case | RWB-E2-003 |

##### A2.29.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-029-01 | Masking | a phone collector (RW-PHONECOL) with the case in scope And product "A-0411" has synthetic account number "9900015678" | the view loads | the other products show with the account number "XXXXXX5678" And a case owner sees "9900015678" | RWB-E2-003 |
| AC-ALT-P3-029-02 | Case outside the scope | a case owner with scope "Own" and case "RW-2026-000410" owned by another person | the case owner calls GET /cases/{caseId}/customer-products | the response is 404 with message MSG-P4-003 | RWB-E2-003 |

##### A2.29.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-029-01 | ACE batch late | `v_ace_batch_status` shows no completed SCBPDM batch for 2026-12-14 and the last completed batch is for 2026-12-13 | the view loads | the 2 products show with data as of 2026-12-13 And the panel shows message MSG-P1-001 with product "Customer profile" and date 2026-12-13 And a stale read event is logged with the case ID and the data product "DP02" | RWB-E2-003 |
| AC-EXC-P3-029-02 | No other products | borrower "C-0420" of case "RW-2026-000420" holds no product other than the case account | the view loads | the panel shows an empty list with message MSG-P2-017 | RWB-E2-003 |
| AC-EXC-P3-029-03 | PII access log unavailable | the ACE PII logging service does not accept the access event | the view loads | no product is returned And the response is 503 with message MSG-GEN-006 | RWB-E2-003 |
| AC-EXC-P3-029-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-029-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.29.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-029-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-029-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.30 Create a case the morning after it reaches 90 days past due

#### A2.30.1 Intent

**Business objective.** Replaces the weekly transfer with daily case creation on the ACE batch-complete record (EV-26 AceDataReady).

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.30.2 Description

**Functional overview.** Replaces the weekly transfer with daily case creation on the ACE batch-complete record (EV-26 AceDataReady).

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Create a case the morning after it reaches 90 days past due | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, ACE database (`v_ace_account`, `v_ace_efs_action`, `v_ace_batch_status`)

**Prerequisites.** FEAT-CHO-01, FEAT-CWC-04

#### A2.30.3 Business rules and structure

##### A2.30.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-030-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| VR-P3-030-2 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| BR-P3-030 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.30.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.30.4 Acceptance criteria

##### A2.30.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-030-01 | Case from the ACE data | synthetic account "A-0001" for customer "C-0001", product group "MORTGAGE", reached 90 days past due in `v_ace_account` for ACE business date 2026-12-14 And `v_ace_efs_action` holds 14 contact records and 2 promises for "A-0001" in its collection period | AceDataReady is raised for ALS and EFS business date 2026-12-14 and the morning case creation runs on 2026-12-15 | a case exists with status "NEW", product group "MORTGAGE", entry date 2026-12-15 and days past due at entry 90 And the case timeline shows the 16 EFS entries read from `v_ace_efs_action` by account_key with source system "EFS" And no copy of them is written to a Workbench table And the decision log entry for the creation holds business date 2026-12-14 in its inputs snapshot And CaseCreated is published with business date 2026-12-14 | RWB-E2-001 |

##### A2.30.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-030-01 | Account linked to the open case | customer "C-0002" has open case "RW-2026-000210" for product group "SSME" And synthetic account "A-0002" of "C-0002", product group "SSME", reaches 90 days past due on 2026-12-14 | case creation runs | no new case is created And "A-0002" is linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false | RWB-E2-001 |
| AC-ALT-P3-030-02 | Cases created on the next complete ACE batch | no case creation ran for business date 2026-12-15 And `v_ace_batch_status` shows the ALS batch for business date 2026-12-16 completed at 05:15 on 2026-12-17 | AceDataReady is raised and case creation runs | accounts that reached 90 days past due on 2026-12-15 or 2026-12-16 get cases with entry date 2026-12-17 And the run summary names the gap date 2026-12-15 | RWB-E2-001 |

##### A2.30.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-030-01 | Repeat run | the run for business date 2026-12-14 created the case for "A-0001" | AceDataReady for business date 2026-12-14 is received again and case creation runs again | no second case is created and nothing is written for "A-0001" And the run summary shows 1 repeat for "A-0001" | RWB-E2-001 |
| AC-EXC-P3-030-02 | Late ACE batch | `v_ace_batch_status` shows no completed ALS batch for business date 2026-12-15 at the 09:00 cut-off on 2026-12-16 | case creation is due | no case is created from the data of 2026-12-14 And the data products show message MSG-P1-001 with the date 2026-12-14 And AceDataLate (EV-27) is raised And the data steward is alerted with message MSG-P2-007 | RWB-E2-001 |
| AC-EXC-P3-030-03 | Customer not in ACE | synthetic account "A-0003" reaches 90 days past due and `v_ace_ca_relation` names a borrower person_key that `v_ace_customer` does not return | case creation runs | no case is created for "A-0003" And reconciliation rule REC-05 lists "A-0003" and the missing person_key for the data steward And "A-0003" is tried again on the next complete ACE batch | RWB-E2-001 |
| AC-EXC-P3-030-04 | Decision log write fails | the decision log store is unavailable | case creation runs for "A-0004" | no case is created for "A-0004" And an incident is raised and the run summary carries message MSG-P7-003 And "A-0004" is taken in the next run | RWB-E2-001 |
| AC-EXC-P3-030-05 | Second start refused | JOB-02 is running for business date 2026-12-14 | a platform administrator requests a rerun of JOB-02 | the response is 409 with message MSG-P2-006 | RWB-E2-001 |
| AC-EXC-P3-030-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-030-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.30.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-030-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-030-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.31 Hold case creation when the ACE batch is late

#### A2.31.1 Intent

**Business objective.** Keeps the last complete ACE business date in use, creates the cases on the next complete ACE batch, and logs the gap.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.31.2 Description

**Functional overview.** Keeps the last complete ACE business date in use, creates the cases on the next complete ACE batch, and logs the gap.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Hold case creation when the ACE batch is late | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database (`v_ace_batch_status`); EV-26 AceDataReady and EV-27 AceDataLate

**Prerequisites.** FEAT-CHO-01

#### A2.31.3 Business rules and structure

##### A2.31.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-031-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P3-031 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.31.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.31.4 Acceptance criteria

##### A2.31.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-031-01 | Case from the ACE data | synthetic account "A-0001" for customer "C-0001", product group "MORTGAGE", reached 90 days past due in `v_ace_account` for ACE business date 2026-12-14 And `v_ace_efs_action` holds 14 contact records and 2 promises for "A-0001" in its collection period | AceDataReady is raised for ALS and EFS business date 2026-12-14 and the morning case creation runs on 2026-12-15 | a case exists with status "NEW", product group "MORTGAGE", entry date 2026-12-15 and days past due at entry 90 And the case timeline shows the 16 EFS entries read from `v_ace_efs_action` by account_key with source system "EFS" And no copy of them is written to a Workbench table And the decision log entry for the creation holds business date 2026-12-14 in its inputs snapshot And CaseCreated is published with business date 2026-12-14 | RWB-E2-001 |

##### A2.31.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-031-01 | Account linked to the open case | customer "C-0002" has open case "RW-2026-000210" for product group "SSME" And synthetic account "A-0002" of "C-0002", product group "SSME", reaches 90 days past due on 2026-12-14 | case creation runs | no new case is created And "A-0002" is linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false | RWB-E2-001 |
| AC-ALT-P3-031-02 | Cases created on the next complete ACE batch | no case creation ran for business date 2026-12-15 And `v_ace_batch_status` shows the ALS batch for business date 2026-12-16 completed at 05:15 on 2026-12-17 | AceDataReady is raised and case creation runs | accounts that reached 90 days past due on 2026-12-15 or 2026-12-16 get cases with entry date 2026-12-17 And the run summary names the gap date 2026-12-15 | RWB-E2-001 |

##### A2.31.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-031-01 | Repeat run | the run for business date 2026-12-14 created the case for "A-0001" | AceDataReady for business date 2026-12-14 is received again and case creation runs again | no second case is created and nothing is written for "A-0001" And the run summary shows 1 repeat for "A-0001" | RWB-E2-001 |
| AC-EXC-P3-031-02 | Late ACE batch | `v_ace_batch_status` shows no completed ALS batch for business date 2026-12-15 at the 09:00 cut-off on 2026-12-16 | case creation is due | no case is created from the data of 2026-12-14 And the data products show message MSG-P1-001 with the date 2026-12-14 And AceDataLate (EV-27) is raised And the data steward is alerted with message MSG-P2-007 | RWB-E2-001 |
| AC-EXC-P3-031-03 | Customer not in ACE | synthetic account "A-0003" reaches 90 days past due and `v_ace_ca_relation` names a borrower person_key that `v_ace_customer` does not return | case creation runs | no case is created for "A-0003" And reconciliation rule REC-05 lists "A-0003" and the missing person_key for the data steward And "A-0003" is tried again on the next complete ACE batch | RWB-E2-001 |
| AC-EXC-P3-031-04 | Decision log write fails | the decision log store is unavailable | case creation runs for "A-0004" | no case is created for "A-0004" And an incident is raised and the run summary carries message MSG-P7-003 And "A-0004" is taken in the next run | RWB-E2-001 |
| AC-EXC-P3-031-05 | Second start refused | JOB-02 is running for business date 2026-12-14 | a platform administrator requests a rerun of JOB-02 | the response is 409 with message MSG-P2-006 | RWB-E2-001 |
| AC-EXC-P3-031-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-031-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.31.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-031-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-031-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.32 Hold the treatment entity and plan timers

#### A2.32.1 Intent

**Business objective.** Creates the treatment record and its timers, which the restructure and deed in lieu routes both build on.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.32.2 Description

**Functional overview.** Creates the treatment record and its timers, which the restructure and deed in lieu routes both build on.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Hold the treatment entity and plan timers | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Quartz scheduler

**Prerequisites.** FEAT-CWC-03

#### A2.32.3 Business rules and structure

##### A2.32.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-032-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P3-032 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.32.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.32.4 Acceptance criteria

##### A2.32.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-032-01 | Treatment created | a TDR plan approved for "RW-2026-000201" with 36 installments, offer amount 850000.00 baht, approval level "L4" and decision log entry "DLE-9001" | the record is written | one treatment exists with type "RESTRUCTURE", installments 36, offer amount 850000.00, approval level "L4", decision log entry "DLE-9001" and the case link And booked at is empty until the booking is confirmed And one TreatmentApproved event is in the outbox with the treatment ID and the case ID | RWB-E2-004 |

##### A2.32.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-032-01 | Timer set | a plan with the first payment due on 2026-12-31 | the record is written and the plan timer listener processes TreatmentApproved the clock passes 2026-12-31 23:59 and the timer check runs | one decision log entry with rule "R-RES-25" and its version is written first And one "INSTALLMENT_DUE" timer exists with expires at 2026-12-31 23:59 Asia/Bangkok, warn at 2026-12-28 and status "RUNNING" And the case route state is "PLAN_RUNNING" and its status stays "IN_PROGRESS" When the clock passes 2026-12-31 23:59 and the timer check runs a TimerDue event is published with timer type "INSTALLMENT_DUE" and the treatment ID And the timer status is "EXPIRED" | RWB-E2-004 |
| AC-ALT-P3-032-02 | Data product | ten treatments recorded on 2026-12-01 across "MORTGAGE", "HIRE_PURCHASE" and "SSME" And two of them have a booked at date | the reporting extract runs at 01:30 on 2026-12-02 | the treatment data product holds ten rows for business date 2026-12-01 And eight show status "APPROVED" and two show status "BOOKED" | RWB-E2-004 |

##### A2.32.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-032-01 | Required field missing | a restructure plan for "RW-2026-000201" with no first due date | the record is written | it is refused with MSG-GEN-001 naming "first due date" And no treatment and no event are written | RWB-E2-004 |
| AC-EXC-P3-032-02 | Approval not in the decision log | a plan that names decision log entry "DLE-0000" which does not exist | the record is written | it is refused with MSG-GEN-001 naming "decision log entry" | RWB-E2-004 |
| AC-EXC-P3-032-03 | Case not in the booked state | case "RW-2026-000202" in route state "WITH_FCR_OFFICER" | a TreatmentApproved event with a first due date arrives for it | no timer is written And the case is placed in the exception queue with MSG-P3-005 naming "PLAN_RUNNING" and "WITH_FCR_OFFICER" | RWB-E2-004 |
| AC-EXC-P3-032-04 | Decision log write fails | the decision log store is unavailable | the plan timer listener processes TreatmentApproved for "RW-2026-000201" | no timer is written and the route state stays "BOOKED_IN_ALS_NLEADS" And the event is retried 3 times and then placed in the exception queue with an incident and MSG-P7-003 | RWB-E2-004 |
| AC-EXC-P3-032-05 | Extract fails | the reporting extract of 2026-12-02 fails | a reporting and BI analyst reads the treatment data product | it shows business date 2026-12-01 with MSG-P1-001 | RWB-E2-004 |
| AC-EXC-P3-032-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-032-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.32.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-032-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-032-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.33 Prepare the credit approval pack for NLEADS

#### A2.33.1 Intent

**Business objective.** Assembles the plan and its credit approval pack for the officer to submit in NLEADS, and records the result on the case.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.33.2 Description

**Functional overview.** Assembles the plan and its credit approval pack for the officer to submit in NLEADS, and records the result on the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Prepare the credit approval pack for NLEADS | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** NLEADS through ACE, read through `v_ace_credit_decision` (RWB-ACE-001); `v_ace_account`, `v_ace_collateral`, `v_ace_valuation`

**Prerequisites.** FEAT-CHO-06

#### A2.33.3 Business rules and structure

##### A2.33.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-033-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P3-033 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.33.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.33.4 Acceptance criteria

##### A2.33.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-033-01 | Pack prepared | an approved restructure plan on treatment "TRT-SYN-0610" | the officer opens the credit approval pack on 2026-12-15 | the pack holds case number "RW-2026-000610", product group "MORTGAGE", 2 accounts with balances as of 2026-12-14 and 1 collateral with its latest appraisal And the pack holds the plan terms: offer amount 2,400,000.00 baht, haircut 0.00 baht, 84 installments, valid until 2026-12-29 And the pack lists the 5 checklist documents with a link to each one on the case And the required approval level "L6" is shown And no field in the pack needs to be typed by the officer | RWB-E2-006 |

##### A2.33.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-033-01 | Result read from ACE | the officer has submitted the pack in NLEADS | `v_ace_credit_decision` returns NLEADS reference "NL-SYN-000610", result "APPROVED", approval level "L5" and result date 2026-12-17 for the treatment | the treatment carries the reference "NL-SYN-000610" and its state is "APPROVED" And a decision log entry with decision "D5" and final call "approved" holds the NLEADS reference And the route state moves to "OFFER_WITH_CUSTOMER" by R-RES-11 | RWB-E2-006 |
| AC-ALT-P3-033-02 | Stale balance | `v_ace_account.data_as_of` for the case accounts is business date 2026-12-12 and today is 2026-12-15 | the officer opens the pack | each balance shows message MSG-P7-006 with 3 days | RWB-E2-006 |

##### A2.33.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-033-01 | Refused | NLEADS refuses the plan with reason "Income does not cover 84 installments" | `v_ace_credit_decision` returns reference "NL-SYN-000611", result "REFUSED" and the reason for the treatment | the treatment state is "REFUSED" and the treatment shows the reason And the route state moves to "DECLINED_BY_CREDIT" by R-RES-12 and then to "BACK_TO_ROUTE_DECISION" by R-RES-14 And the case is in the case owner's queue | RWB-E2-006 |
| AC-EXC-P3-033-02 | Missing checklist document | the case holds no document of type "INCOME_PROOF" | the officer opens the pack | the pack shows "INCOME_PROOF" as missing with message MSG-P2-009 And the other 4 documents show as present | RWB-E2-006 |
| AC-EXC-P3-033-03 | Case not awaiting credit approval | case "RW-2026-000620" is in route state "PLAN_RUNNING" | the officer records a result for its treatment | the response is 409 with message MSG-P3-005 | RWB-E2-006 |
| AC-EXC-P3-033-04 | Decision log write fails | the decision log store is unavailable | the officer records result "APPROVED" with reference "NL-SYN-000613" and approval level "L5" | the response is 503 with message MSG-P7-003 And the treatment and the route state do not change And an incident is raised | RWB-E2-006 |
| AC-EXC-P3-033-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-033-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.33.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-033-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-033-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.34 Confirm booked terms from the ACE account data

#### A2.34.1 Intent

**Business objective.** Matches the approved terms or settlement to the booked position in `v_ace_account` for the next ACE business date, and raises a task when it is missing.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.34.2 Description

**Functional overview.** Matches the approved terms or settlement to the booked position in `v_ace_account` for the next ACE business date, and raises a task when it is missing.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Confirm booked terms from the ACE account data | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database (`v_ace_account`, `v_ace_batch_status`); JOB-08 starts on EV-26 AceDataReady for ALS

**Prerequisites.** FEAT-CHO-06

#### A2.34.3 Business rules and structure

##### A2.34.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-034-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P3-034 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.34.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.34.4 Acceptance criteria

##### A2.34.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-034-01 | Booking confirmed | settlement treatment "TRT-SYN-0701" on case "RW-2026-000701" was approved on 2026-12-15 with offer amount 650,000.00 baht And the officer booked the settlement in ALS on 2026-12-16 And `v_ace_account` shows settlement_booked_date 2026-12-16 and settlement_booked_amount 650,000.00 baht for account_key "A-0701" | AceDataReady is raised for ALS business date 2026-12-16 and JOB-08 runs on 2026-12-17 | the booked terms match the approved treatment and the treatment state is "BOOKED" with booked at 2026-12-16 And TreatmentBooked is published with business date 2026-12-16 And the route state moves from "WITH_OPS_SETTLEMENT" to "AWAITING_PAYMENT" by R-SET-13 with a decision log entry | RWB-E2-007 |

##### A2.34.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-034-01 | Terms differ | restructure treatment "TRT-SYN-0703" was approved with offer amount 1,800,000.00 baht and rate 4.2500 percent And `v_ace_account` shows tdr_flag true, last_tdr_date 2026-12-16, principal_outstanding 1,800,000.00 baht and interest_rate 4.5000 percent for "A-0703" | the match runs | the treatment shows the difference: interest rate approved 4.2500, booked 4.5000 And a task "UNMATCHED_EXCEPTION" goes to role "RW-CREDITAD" with message MSG-P2-012 And the treatment stays "APPROVED" | RWB-E2-007 |
| AC-ALT-P3-034-02 | Only some accounts booked | restructure treatment "TRT-SYN-0704" covers synthetic accounts "A-0704" and "A-0705" And only "A-0704" shows the booking in `v_ace_account` | the match runs | the treatment stays "APPROVED" And the task for "RW-RESTRUCT" names account "A-0705" as not booked | RWB-E2-007 |

##### A2.34.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-034-01 | Booking missing | restructure treatment "TRT-SYN-0702" was approved on 2026-12-15 And `v_ace_account` for ACE business date 2026-12-16 shows tdr_flag false for account_key "A-0702" | the match runs | a task "WITH_OPS_BOOKING" is raised for role "RW-RESTRUCT" with message MSG-P2-011 And the treatment stays "APPROVED" | RWB-E2-007 |
| AC-EXC-P3-034-02 | ACE batch not complete | `v_ace_batch_status` shows the ALS batch for business date 2026-12-17 with a status other than "COMPLETED" | JOB-08 is due on 2026-12-18 | JOB-08 does not run for 2026-12-17 And no missing booking task is raised for 2026-12-17 | RWB-E2-007 |
| AC-EXC-P3-034-03 | Booking still missing on the next ACE business date | task "WITH_OPS_BOOKING" is open for "TRT-SYN-0702" from the ACE data of 2026-12-16 | `v_ace_account` for 2026-12-17 still shows no booking | no second task is raised And the REC-03 break list for the data steward shows "TRT-SYN-0702" as missing for 2 days | RWB-E2-007 |
| AC-EXC-P3-034-04 | Decision log write fails on confirmation | the decision log store is unavailable | the match finds "TRT-SYN-0701" booked | the treatment stays "APPROVED" and no TreatmentBooked event is published And an incident is raised with message MSG-P7-003 And the match runs again on the next complete ACE batch | RWB-E2-007 |
| AC-EXC-P3-034-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-034-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.34.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-034-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-034-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.35 Build the stage 2 data products

#### A2.35.1 Intent

**Business objective.** Adds the contract, plan and treatment read models to the data store.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.35.2 Description

**Functional overview.** Adds the contract, plan and treatment read models to the data store.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Build the stage 2 data products | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database

**Prerequisites.** FEAT-RDF-02

#### A2.35.3 Business rules and structure

##### A2.35.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-035-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P3-035 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.35.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.35.4 Acceptance criteria

##### A2.35.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-035-01 | Products loaded | treatments and plans in the case store, with credit approvals recorded from NLEADS by the officer | the stage 2 data product step runs on AceDataReady for ALS business date 2026-12-14 | dp_treatment holds 40 rows for business date 2026-12-14, each with treatment type, approval level, installments, outcome and the contract number read from `v_ace_account.contract_no` by the case's primary account_key And DP04 carries a freshness stamp for business date 2026-12-14 with status "LOADED" And the catalog entry for DP04 lists system of record "Workbench", owner RW-DATASTEW and the fields of treatment and guarantee_claim | RWB-E2-010 |

##### A2.35.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-035-01 | Guarantee data | 5 TCG guarantee claim records for 5 existing cases, claimed amounts from 180,000.00 to 1,250,000.00 baht | the stage 2 step runs | dp_guarantee_claim holds 5 rows, each linked to its case And a read of DP04 for case "RW-2026-000512" returns its TCG claim with claim deadline 2027-02-28 | RWB-E2-010 |
| AC-ALT-P3-035-02 | Access | user "u-phone-02" holds RW-PHONECOL, which has no DP04 access row | the user calls GET /data-products/DP04/records?caseId=RW-2026-000512 | the call is refused with status 403 and MSG-P4-002 And the refusal is logged with user "u-phone-02" and product "DP04" | RWB-E2-010 |

##### A2.35.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-035-01 | A guarantee claim for a case that does not exist | a TCG claim names case ID "00000000-0000-0000-0000-000000000997" | the stage 2 step runs | the claim is not written to dp_guarantee_claim And the reconciliation break list (reconciliation_result) holds it with product "DP04" and check "References" | RWB-E2-010 |
| AC-EXC-P3-035-02 | The treatment interface is unavailable | TreatmentQuery returns an error | the stage 2 step runs for 2026-12-14 | the step ends "FAILED" with MSG-GEN-006 for system "Treatment" And dp_treatment keeps the rows for 2026-12-13 And at 08:00 DP04 is flagged stale with MSG-P1-001 "Treatment is from 2026-12-13. Today's data is not yet complete." | RWB-E2-010 |
| AC-EXC-P3-035-03 | A repeat run for the same date | the stage 2 step completed for 2026-12-14 with 40 treatment rows | it runs again for 2026-12-14 | dp_treatment still holds 40 rows for 2026-12-14 | RWB-E2-010 |
| AC-EXC-P3-035-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-035-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.35.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-035-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-035-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.36 Automate the EFS file load (removed)

**Status.** Removed by D-RCV-35 - later home: ACE ingestion. RWB-E2-023 leaves the backlog (Change Register Appendix A). ACE ingests the EFS feed (INT-07, into ACE) and the Workbench reads it through `v_ace_efs_action`; there is no Workbench file load, run record, sign-off or manual-upload flag to retire. The hand-over count check moves to JOB-04 reconciliation of the case list to `v_ace_account` (`reconciliation_result`, REC-05).

The IDs are kept so that traceability does not break. None of them is built or tested.

| ID | v2 content | Disposition |
|---|---|---|
| FEAT-CHO-10 | Automate the EFS file load | Removed by D-RCV-35 - later home: ACE ingestion |
| VR-P3-036-1, BR-P3-036 | Stale data rule; no value in code | Removed by D-RCV-35 - later home: ACE ingestion |
| AC-P3-036-01 | Hand-over count reconciled against the COLLINS load | Removed by D-RCV-35 - later home: ACE ingestion; reconciliation in JOB-04 |
| AC-ALT-P3-036-01 | Manual step retired after 10 clean days, sign-off on INT-07 | Removed by D-RCV-35 - later home: ACE ingestion |
| AC-ALT-P3-036-02 | Alert on a hand-over difference | Removed by D-RCV-35 - later home: ACE ingestion |
| AC-EXC-P3-036-01 | No hand-over run for the day | Removed by D-RCV-35 - later home: ACE ingestion |
| AC-EXC-P3-036-02 | Sign-off after retirement refused | Removed by D-RCV-35 - later home: ACE ingestion |
| AC-EXC-P3-036-03, AC-EXC-P3-036-04 | Role without the right; decision cannot be recorded | Removed with the feature |
| AC-BG-P3-036-01, AC-BG-P3-036-02 | Morning allocation; timer check | Removed with the feature; covered in A2.30 |

---

### A2.37 Query the decision log for audit

#### A2.37.1 Intent

**Business objective.** Gives audit a query API over the decision log, by case, decision, period or approver.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.37.2 Description

**Functional overview.** Gives audit a query API over the decision log, by case, decision, period or approver.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Internal audit | Opens the screen and query the decision log for audit | Checks the role, the capability area and the scope |
| 2 | Internal audit | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, ACE database

**Prerequisites.** FEAT-DRI-01

#### A2.37.3 Business rules and structure

##### A2.37.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-037-1 | A timer will expire within its warning period | MSG-P3-003 {timer} ends on {date}. |
| VR-P3-037-2 | Allocation not recorded (RWB-E1-020) | MSG-P3-013 The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| BR-P3-037 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.37.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.37.3.3 Roles and permissions

| Role | Use |
|---|---|
| Internal audit | Primary |
| Compliance and PDPA officer | Also uses |

#### A2.37.4 Acceptance criteria

##### A2.37.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-037-01 | Query by case | case "RW-2026-000123" has six entries with chain_seq 101, 155, 160, 230, 231 and 402 | "U-8101" calls GET /decision-log with caseId of that case | the six entries return in chain_seq order And each entry carries chainVerified true | RWB-E2-005 |

##### A2.37.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-037-01 | Query by rule version | rule R-LIT-03 at version "LIT-2026.12" was used in 200 decisions | "U-8101" calls GET /decision-log with ruleId "R-LIT-03" and ruleVersion "LIT-2026.12" and size 500 | 200 entries return and total is 200 And the total equals the count for "LIT-2026.12" in the rule change audit report | RWB-E2-005 |
| AC-ALT-P3-037-02 | Access | test user "U-8102" holds only RW-PHONECOL, whose Decision log letter is "-" | the user calls GET /decision-log | the call is refused with status 403 and message MSG-P4-002 And one entry with decision code "AC-DENY", area "DECISION_LOG" and right "R" is written | RWB-E2-005 |

##### A2.37.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-037-01 | An entry that does not match the chain is flagged | the entry with chain_seq 230 was changed in the SIT database with the trigger disabled | "U-8101" queries case "RW-2026-000123" | six entries return and entry 230 carries chainVerified false And the response carries warning MSG-P7-012 naming entry 230 And one incident is raised to the Compliance queue for entry 230 | RWB-E2-005 |
| AC-EXC-P3-037-02 | Invalid filters are refused | None | "U-8101" calls GET /decision-log with from "2026-12-31" and to "2026-12-01" | the call returns status 422 with message MSG-GEN-003 for field "from" And when "U-8101" calls it with size 1000 the call returns status 422 with message MSG-GEN-002 for field "size" with min 1 and max 500 | RWB-E2-005 |
| AC-EXC-P3-037-03 | No match | None | "U-8101" queries approver "U-8199", who approved nothing | the call returns status 200 with no items and total 0 And SCR-38 shows the empty state | RWB-E2-005 |
| AC-EXC-P3-037-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-037-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.37.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-037-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-037-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.38 Show my queue with filters and ageing

#### A2.38.1 Intent

**Business objective.** Gives each user their own queue with filters, sort and the age of every case in it.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.38.2 Description

**Functional overview.** Gives each user their own queue with filters, sort and the age of every case in it.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and show my queue with filters and ageing | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-19

#### A2.38.3 Business rules and structure

##### A2.38.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-038-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| BR-P3-038 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.38.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.38.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Restructuring officer (FCR), Litigation officer | Also uses |

#### A2.38.4 Acceptance criteria

##### A2.38.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-038-01 | My queue | "U-CO-01" owns 40 open cases, 3 with an expired service level timer and 37 with running timers | "U-CO-01" opens My queue | 40 cases list in one page And the 3 breached cases come first, then the 37 by service level due date, earliest first And each row shows the case number, product group, stage, status, age in days from the entry date and the service level due date | RWB-E2-011 |

##### A2.38.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-038-01 | Team view | "MTG-BKK-CO" holds 412 open cases with the oldest entered on 2026-09-02 and 9 breaches And "MTG-BKK-LIT" holds 38 open cases with the oldest entered on 2026-10-20 and 0 breaches | "U-TM-01" opens Team queues | "MTG-BKK-CO" shows count 412, oldest case age 104 days and 9 breaches And "MTG-BKK-LIT" shows count 38, oldest case age 56 days and 0 breaches And each owner in "MTG-BKK-CO" shows their open case count against the cap of 150 | RWB-E2-011 |
| AC-ALT-P3-038-02 | Filter | "U-CO-01" owns 12 open cases on stage "LITIGATION" and 28 on other stages | the stage filter is set to "LITIGATION" and the list refreshes | only the 12 litigation cases show And after "U-CO-01" opens a case and returns to My queue the filter is still "LITIGATION" And after sign-out and sign-in the filter is cleared | RWB-E2-011 |

##### A2.38.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-038-01 | Page size above the limit | None | the front end requests My queue with page size 500 | the request is refused with MSG-GEN-002 naming "size", 1 and 200 | RWB-E2-011 |
| AC-EXC-P3-038-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-038-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.38.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-038-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-038-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.39 Show team queues

#### A2.39.1 Intent

**Business objective.** Gives the team manager every queue in the team, with depth, ageing and the spread across owners.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.39.2 Description

**Functional overview.** Gives the team manager every queue in the team, with depth, ageing and the spread across owners.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Team manager | Opens the screen and show team queues | Checks the role, the capability area and the scope |
| 2 | Team manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-WKM-01

#### A2.39.3 Business rules and structure

##### A2.39.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-039-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| BR-P3-039 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.39.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.39.3.3 Roles and permissions

| Role | Use |
|---|---|
| Team manager | Primary |
| Case owner | Also uses |

#### A2.39.4 Acceptance criteria

##### A2.39.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-039-01 | My queue | "U-CO-01" owns 40 open cases, 3 with an expired service level timer and 37 with running timers | "U-CO-01" opens My queue | 40 cases list in one page And the 3 breached cases come first, then the 37 by service level due date, earliest first And each row shows the case number, product group, stage, status, age in days from the entry date and the service level due date | RWB-E2-011 |

##### A2.39.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-039-01 | Team view | "MTG-BKK-CO" holds 412 open cases with the oldest entered on 2026-09-02 and 9 breaches And "MTG-BKK-LIT" holds 38 open cases with the oldest entered on 2026-10-20 and 0 breaches | "U-TM-01" opens Team queues | "MTG-BKK-CO" shows count 412, oldest case age 104 days and 9 breaches And "MTG-BKK-LIT" shows count 38, oldest case age 56 days and 0 breaches And each owner in "MTG-BKK-CO" shows their open case count against the cap of 150 | RWB-E2-011 |
| AC-ALT-P3-039-02 | Filter | "U-CO-01" owns 12 open cases on stage "LITIGATION" and 28 on other stages | the stage filter is set to "LITIGATION" and the list refreshes | only the 12 litigation cases show And after "U-CO-01" opens a case and returns to My queue the filter is still "LITIGATION" And after sign-out and sign-in the filter is cleared | RWB-E2-011 |

##### A2.39.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-039-01 | Page size above the limit | None | the front end requests My queue with page size 500 | the request is refused with MSG-GEN-002 naming "size", 1 and 200 | RWB-E2-011 |
| AC-EXC-P3-039-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-039-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.39.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-039-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-039-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.40 Transfer a case manually with a reason

#### A2.40.1 Intent

**Business objective.** Lets an authorized user move a case to another queue, with a coded reason recorded on the case.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.40.2 Description

**Functional overview.** Lets an authorized user move a case to another queue, with a coded reason recorded on the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Team manager | Opens the screen and transfer a case manually with a reason | Checks the role, the capability area and the scope |
| 2 | Team manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-10

#### A2.40.3 Business rules and structure

##### A2.40.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-040-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| VR-P3-040-2 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| VR-P3-040-3 | Allocation not recorded (RWB-E1-020) | MSG-P3-013 The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| R-UNI-14 | Record the coded reason, move the case to the chosen route, when an authorized user overrides the route inside the delegation | Moves to ROUTE_D6_REOPEN |
| BR-P3-040 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.40.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.40.3.3 Roles and permissions

| Role | Use |
|---|---|
| Team manager | Primary |
| Case owner | Also uses |

#### A2.40.4 Acceptance criteria

##### A2.40.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-040-01 | Transfer | case "RW-2026-000401" in a queue of team "MTG-BKK" | "U-TM-01" transfers it to queue "LIT-BKK-01" with reason "R02" Customer deceased | the case is in queue "LIT-BKK-01" with owner "U-LO-02" And the previous assignment of "U-CO-01" has ended at the time of the transfer And a new assignment has reason "TRANSFER", reason code "R02", queue "LIT-BKK-01" and the transfer rule ID And one decision log entry holds the rule ID, the rule version, the from and to queue and owner and the reason code And the case keeps status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01 And one CaseTransferred event is in the outbox | RWB-E2-012 |

##### A2.40.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-040-01 | Rule blocks | case "RW-2026-000402" with deviation "X1" open and owned by the complaint officer under rule "R-DEV-02" | "U-TM-01" tries to transfer it to queue "LIT-BKK-01" with reason "R05" | the screen refuses with MSG-P3-033 naming rule "R-DEV-02" And the case, its assignment and the decision log are unchanged | RWB-E2-012 |
| AC-ALT-P3-040-02 | Bulk | ten selected cases in queue "MTG-BKK-CO" owned by "U-CO-01" | "U-TM-01" reassigns them to owner "U-CO-03" with 60 open cases and reason "R04" | all ten have owner "U-CO-03" And ten assignments and ten decision log entries are written And "U-CO-03" holds 70 open cases | RWB-E2-012 |

##### A2.40.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-040-01 | No reason | None | "U-TM-01" submits a transfer of "RW-2026-000401" with no reason code | the transfer is refused with MSG-P3-001 And nothing changes | RWB-E2-012 |
| AC-EXC-P3-040-02 | Repeated request | the AC1 transfer was made with Idempotency-Key "5b0c7a1e-0000-4000-8000-000000000001" | the same request is sent again with the same Idempotency-Key | the response is the same assignment And there is still one new assignment and one decision log entry | RWB-E2-012 |
| AC-EXC-P3-040-03 | Decision log write fails | the decision log store is unavailable | "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02" | the transfer is refused with MSG-P7-003 And the case stays in queue "MTG-BKK-CO" with owner "U-CO-01" and no new assignment | RWB-E2-012 |
| AC-EXC-P3-040-04 | Bulk with refusals | ten selected cases, two of which are under a legal hold | "U-TM-01" reassigns them to "U-CO-03" with reason "R01" | eight cases move And the two held cases show MSG-P3-005 And the summary shows MSG-P3-035 with 8 of 10 | RWB-E2-012 |
| AC-EXC-P3-040-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-040-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.40.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-040-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-040-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.41 Reassign a case to another owner

#### A2.41.1 Intent

**Business objective.** Moves a case to a named owner for capacity, skill or absence, keeping the state and the clocks.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.41.2 Description

**Functional overview.** Moves a case to a named owner for capacity, skill or absence, keeping the state and the clocks.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Team manager | Opens the screen and reassign a case to another owner | Checks the role, the capability area and the scope |
| 2 | Team manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-WKM-03

#### A2.41.3 Business rules and structure

##### A2.41.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-041-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| VR-P3-041-2 | A move not allowed from the current state | MSG-P3-005 This case cannot move to {state} from {current}. |
| R-UNI-18 | Reallocate inside the same team by region and workload, keep the state and the clocks, when the owner leaves, is absent beyond the threshold, or the account is reassigned | Moves to REALLOCATED |
| R-UNI-46 | Resume the case in the same state with the same clocks, when the new owner accepts the case | Moves to RESUME_STATE |
| BR-P3-041 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.41.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.41.3.3 Roles and permissions

| Role | Use |
|---|---|
| Team manager | Primary |

#### A2.41.4 Acceptance criteria

##### A2.41.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-041-01 | Transfer | case "RW-2026-000401" in a queue of team "MTG-BKK" | "U-TM-01" transfers it to queue "LIT-BKK-01" with reason "R02" Customer deceased | the case is in queue "LIT-BKK-01" with owner "U-LO-02" And the previous assignment of "U-CO-01" has ended at the time of the transfer And a new assignment has reason "TRANSFER", reason code "R02", queue "LIT-BKK-01" and the transfer rule ID And one decision log entry holds the rule ID, the rule version, the from and to queue and owner and the reason code And the case keeps status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01 And one CaseTransferred event is in the outbox | RWB-E2-012 |

##### A2.41.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-041-01 | Rule blocks | case "RW-2026-000402" with deviation "X1" open and owned by the complaint officer under rule "R-DEV-02" | "U-TM-01" tries to transfer it to queue "LIT-BKK-01" with reason "R05" | the screen refuses with MSG-P3-033 naming rule "R-DEV-02" And the case, its assignment and the decision log are unchanged | RWB-E2-012 |
| AC-ALT-P3-041-02 | Bulk | ten selected cases in queue "MTG-BKK-CO" owned by "U-CO-01" | "U-TM-01" reassigns them to owner "U-CO-03" with 60 open cases and reason "R04" | all ten have owner "U-CO-03" And ten assignments and ten decision log entries are written And "U-CO-03" holds 70 open cases | RWB-E2-012 |

##### A2.41.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-041-01 | No reason | None | "U-TM-01" submits a transfer of "RW-2026-000401" with no reason code | the transfer is refused with MSG-P3-001 And nothing changes | RWB-E2-012 |
| AC-EXC-P3-041-02 | Repeated request | the AC1 transfer was made with Idempotency-Key "5b0c7a1e-0000-4000-8000-000000000001" | the same request is sent again with the same Idempotency-Key | the response is the same assignment And there is still one new assignment and one decision log entry | RWB-E2-012 |
| AC-EXC-P3-041-03 | Decision log write fails | the decision log store is unavailable | "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02" | the transfer is refused with MSG-P7-003 And the case stays in queue "MTG-BKK-CO" with owner "U-CO-01" and no new assignment | RWB-E2-012 |
| AC-EXC-P3-041-04 | Bulk with refusals | ten selected cases, two of which are under a legal hold | "U-TM-01" reassigns them to "U-CO-03" with reason "R01" | eight cases move And the two held cases show MSG-P3-005 And the summary shows MSG-P3-035 with 8 of 10 | RWB-E2-012 |
| AC-EXC-P3-041-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-041-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.41.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-041-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-041-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.42 Show timers and the service level on the case

#### A2.42.1 Intent

**Business objective.** Puts the stage clock, the service level and the prescription date on the case record view.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.42.2 Description

**Functional overview.** Puts the stage clock, the service level and the prescription date on the case record view.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and show timers and the service level on the case | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-11

#### A2.42.3 Business rules and structure

##### A2.42.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-042-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-UNI-04 | Raise X1, pause the stage clock, apply the contact stop, when a complaint is logged against the case | Moves to HELD_DEVIATION |
| R-UNI-43 | Resume the stage clock and return the case, when the deviation owner records the outcome | Moves to RESUME_STATE |
| BR-P3-042 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.42.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.42.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Team manager | Also uses |

#### A2.42.4 Acceptance criteria

##### A2.42.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-042-01 | Timers shown | case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF" | "U-CO-01" opens the case record | the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer" | RWB-E2-015 |

##### A2.42.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-042-01 | Deviation flag | case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true | "U-CO-01" opens the case record | the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date And the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped" | RWB-E2-015 |
| AC-ALT-P3-042-02 | Prescription | case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date | "U-CO-01" opens the case record | the prescription date 2027-02-13 shows with the warning MSG-P3-003 And for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows | RWB-E2-015 |

##### A2.42.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-042-01 | No running timer | case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED" | "U-CO-01" opens the case record | the timers section shows MSG-P3-018 | RWB-E2-015 |
| AC-EXC-P3-042-02 | Deviation module does not answer | the deviation query does not answer within 2 seconds for case "RW-2026-000502" | "U-CO-01" opens the case record | the timers and the prescription date show And the deviation section shows MSG-GEN-006 naming "Deviation handling" And the on hold banner shows from the case's deviation flag | RWB-E2-015 |
| AC-EXC-P3-042-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-042-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.42.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-042-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-042-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.43 Show the deviation flag on the case

#### A2.43.1 Intent

**Business objective.** Shows which deviation is open on the case, who owns it and since when.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.43.2 Description

**Functional overview.** Shows which deviation is open on the case, who owns it and since when.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and show the deviation flag on the case | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-DVH-01

#### A2.43.3 Business rules and structure

##### A2.43.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-043-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P3-043 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.43.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.43.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Complaint officer, Hardship and vulnerability specialist | Also uses |

#### A2.43.4 Acceptance criteria

##### A2.43.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-043-01 | Timers shown | case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF" | "U-CO-01" opens the case record | the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer" | RWB-E2-015 |

##### A2.43.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-043-01 | Deviation flag | case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true | "U-CO-01" opens the case record | the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date And the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped" | RWB-E2-015 |
| AC-ALT-P3-043-02 | Prescription | case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date | "U-CO-01" opens the case record | the prescription date 2027-02-13 shows with the warning MSG-P3-003 And for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows | RWB-E2-015 |

##### A2.43.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-043-01 | No running timer | case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED" | "U-CO-01" opens the case record | the timers section shows MSG-P3-018 | RWB-E2-015 |
| AC-EXC-P3-043-02 | Deviation module does not answer | the deviation query does not answer within 2 seconds for case "RW-2026-000502" | "U-CO-01" opens the case record | the timers and the prescription date show And the deviation section shows MSG-GEN-006 naming "Deviation handling" And the on hold banner shows from the case's deviation flag | RWB-E2-015 |
| AC-EXC-P3-043-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-043-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.43.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-043-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-043-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.44 Show escalation state on the case

#### A2.44.1 Intent

**Business objective.** Shows that a service level has been breached, to whom it was escalated and when.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.44.2 Description

**Functional overview.** Shows that a service level has been breached, to whom it was escalated and when.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and show escalation state on the case | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-13

#### A2.44.3 Business rules and structure

##### A2.44.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-044-1 | A move not allowed from the current state | MSG-P3-005 This case cannot move to {state} from {current}. |
| R-UNI-30 | Raise the breach to the named escalation point. The case does not move, when time in the current state exceeds the service level | Moves to ESCALATED |
| R-UNI-42 | Resume the case in the state it was in, record the intervention, when the escalation point acts | Moves to RESUME_STATE |
| BR-P3-044 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.44.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.44.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Team manager | Also uses |

#### A2.44.4 Acceptance criteria

##### A2.44.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-044-01 | Timers shown | case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF" | "U-CO-01" opens the case record | the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer" | RWB-E2-015 |

##### A2.44.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-044-01 | Deviation flag | case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true | "U-CO-01" opens the case record | the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date And the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped" | RWB-E2-015 |
| AC-ALT-P3-044-02 | Prescription | case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date | "U-CO-01" opens the case record | the prescription date 2027-02-13 shows with the warning MSG-P3-003 And for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows | RWB-E2-015 |

##### A2.44.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-044-01 | No running timer | case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED" | "U-CO-01" opens the case record | the timers section shows MSG-P3-018 | RWB-E2-015 |
| AC-EXC-P3-044-02 | Deviation module does not answer | the deviation query does not answer within 2 seconds for case "RW-2026-000502" | "U-CO-01" opens the case record | the timers and the prescription date show And the deviation section shows MSG-GEN-006 naming "Deviation handling" And the on hold banner shows from the case's deviation flag | RWB-E2-015 |
| AC-EXC-P3-044-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-044-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.44.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-044-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-044-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.45 Show the full case record view with the history timeline

#### A2.45.1 Intent

**Business objective.** Completes the case record view: accounts, parties, collateral, documents, communications, decisions and history.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.45.2 Description

**Functional overview.** Completes the case record view: accounts, parties, collateral, documents, communications, decisions and history.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and show the full case record view with the history timeline | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, ACE database (`v_ace_account`, `v_ace_customer`, `v_ace_ca_relation`, `v_ace_contact`, `v_ace_collateral`, `v_ace_efs_action`) by business key

**Prerequisites.** FEAT-ACA-12

#### A2.45.3 Business rules and structure

##### A2.45.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-045-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P3-045 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.45.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.45.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Conduct and QA officer, Internal audit | Also uses |

#### A2.45.4 Acceptance criteria

##### A2.45.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-045-01 | Timeline | case "RW-2026-000601" has 30 events: 4 assignments, 3 transfers, 8 contacts, 6 decision log entries, 2 notices, 5 documents and 2 timer events | "U-CO-01" opens the case timeline | the 30 items show newest first, each with type, actor and time And the first page loads within 2 seconds at the 95th percentile over 20 runs | RWB-E2-016 |

##### A2.45.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-045-01 | Filter | the filter set to "DECISION" | the timeline refreshes | only the 6 decision items show And each carries its decision log entry ID and opens that entry | RWB-E2-016 |
| AC-ALT-P3-045-02 | Queue history | case "RW-2026-000601" was allocated to "MTG-BKK-CO" on 2026-11-30 and transferred three times: to "LIT-BKK-01" with reason "R05" on 2026-12-05, to "MTG-BKK-CO" with reason "R06" on 2026-12-08 and to "LIT-BKK-02" with reason "R01" on 2026-12-12 | "U-CO-01" opens queue history | the three moves show newest first with from queue, to queue, from owner, to owner, reason code and rule ID And the allocation on 2026-11-30 shows as the first entry with reason "ALLOCATION" | RWB-E2-016 |

##### A2.45.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-045-01 | Items the role may not read | user "U-PC-01" holds RW-PHONECOL with case "RW-2026-000601" in scope | "U-PC-01" opens the case timeline | no decision item and no notice item shows And contacts, assignments, transfers, documents and timer events show | RWB-E2-016 |
| AC-EXC-P3-045-02 | A source does not answer | the document query does not answer within 2 seconds | "U-CO-01" opens the case timeline | the 25 items from the other sources show And a notice shows MSG-GEN-006 naming "Document hub" | RWB-E2-016 |
| AC-EXC-P3-045-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-045-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.45.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-045-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-045-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.46 Show queue history on the case

#### A2.46.1 Intent

**Business objective.** Shows every queue and owner the case has had, with the reason for each move.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.46.2 Description

**Functional overview.** Shows every queue and owner the case has had, with the reason for each move.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Team manager | Opens the screen and show queue history on the case | Checks the role, the capability area and the scope |
| 2 | Team manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-WKM-08

#### A2.46.3 Business rules and structure

##### A2.46.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-046-1 | A transfer without a reason | MSG-P3-001 Choose a reason for the transfer. |
| VR-P3-046-2 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| R-UNI-34 | Move to the exception queue and raise a task for the owner, when an outbound call fails after the retry limit | Moves to EXCEPTION_QUEUE |
| BR-P3-046 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.46.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.46.3.3 Roles and permissions

| Role | Use |
|---|---|
| Team manager | Primary |
| Internal audit | Also uses |

#### A2.46.4 Acceptance criteria

##### A2.46.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-046-01 | Timeline | case "RW-2026-000601" has 30 events: 4 assignments, 3 transfers, 8 contacts, 6 decision log entries, 2 notices, 5 documents and 2 timer events | "U-CO-01" opens the case timeline | the 30 items show newest first, each with type, actor and time And the first page loads within 2 seconds at the 95th percentile over 20 runs | RWB-E2-016 |

##### A2.46.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-046-01 | Filter | the filter set to "DECISION" | the timeline refreshes | only the 6 decision items show And each carries its decision log entry ID and opens that entry | RWB-E2-016 |
| AC-ALT-P3-046-02 | Queue history | case "RW-2026-000601" was allocated to "MTG-BKK-CO" on 2026-11-30 and transferred three times: to "LIT-BKK-01" with reason "R05" on 2026-12-05, to "MTG-BKK-CO" with reason "R06" on 2026-12-08 and to "LIT-BKK-02" with reason "R01" on 2026-12-12 | "U-CO-01" opens queue history | the three moves show newest first with from queue, to queue, from owner, to owner, reason code and rule ID And the allocation on 2026-11-30 shows as the first entry with reason "ALLOCATION" | RWB-E2-016 |

##### A2.46.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-046-01 | Items the role may not read | user "U-PC-01" holds RW-PHONECOL with case "RW-2026-000601" in scope | "U-PC-01" opens the case timeline | no decision item and no notice item shows And contacts, assignments, transfers, documents and timer events show | RWB-E2-016 |
| AC-EXC-P3-046-02 | A source does not answer | the document query does not answer within 2 seconds | "U-CO-01" opens the case timeline | the 25 items from the other sources show And a notice shows MSG-GEN-006 naming "Document hub" | RWB-E2-016 |
| AC-EXC-P3-046-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-046-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.46.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-046-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-046-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.47 Reallocate when an owner is unavailable

#### A2.47.1 Intent

**Business objective.** Moves open cases to another owner in the same team when the owner leaves or is absent past the threshold.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.47.2 Description

**Functional overview.** Moves open cases to another owner in the same team when the owner leaves or is absent past the threshold.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Reallocate when an owner is unavailable | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-08

#### A2.47.3 Business rules and structure

##### A2.47.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-047-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| R-UNI-18 | Reallocate inside the same team by region and workload, keep the state and the clocks, when the owner leaves, is absent beyond the threshold, or the account is reassigned | Moves to REALLOCATED |
| R-UNI-19 | Reallocate the newest cases until the owner is inside the cap, when the owner is above the maximum caseload | Moves to REALLOCATED |
| BR-P3-047 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.47.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.47.4 Acceptance criteria

##### A2.47.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-047-01 | Transfer | case "RW-2026-000401" in a queue of team "MTG-BKK" | "U-TM-01" transfers it to queue "LIT-BKK-01" with reason "R02" Customer deceased | the case is in queue "LIT-BKK-01" with owner "U-LO-02" And the previous assignment of "U-CO-01" has ended at the time of the transfer And a new assignment has reason "TRANSFER", reason code "R02", queue "LIT-BKK-01" and the transfer rule ID And one decision log entry holds the rule ID, the rule version, the from and to queue and owner and the reason code And the case keeps status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01 And one CaseTransferred event is in the outbox | RWB-E2-012 |

##### A2.47.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-047-01 | Rule blocks | case "RW-2026-000402" with deviation "X1" open and owned by the complaint officer under rule "R-DEV-02" | "U-TM-01" tries to transfer it to queue "LIT-BKK-01" with reason "R05" | the screen refuses with MSG-P3-033 naming rule "R-DEV-02" And the case, its assignment and the decision log are unchanged | RWB-E2-012 |
| AC-ALT-P3-047-02 | Bulk | ten selected cases in queue "MTG-BKK-CO" owned by "U-CO-01" | "U-TM-01" reassigns them to owner "U-CO-03" with 60 open cases and reason "R04" | all ten have owner "U-CO-03" And ten assignments and ten decision log entries are written And "U-CO-03" holds 70 open cases | RWB-E2-012 |

##### A2.47.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-047-01 | No reason | None | "U-TM-01" submits a transfer of "RW-2026-000401" with no reason code | the transfer is refused with MSG-P3-001 And nothing changes | RWB-E2-012 |
| AC-EXC-P3-047-02 | Repeated request | the AC1 transfer was made with Idempotency-Key "5b0c7a1e-0000-4000-8000-000000000001" | the same request is sent again with the same Idempotency-Key | the response is the same assignment And there is still one new assignment and one decision log entry | RWB-E2-012 |
| AC-EXC-P3-047-03 | Decision log write fails | the decision log store is unavailable | "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02" | the transfer is refused with MSG-P7-003 And the case stays in queue "MTG-BKK-CO" with owner "U-CO-01" and no new assignment | RWB-E2-012 |
| AC-EXC-P3-047-04 | Bulk with refusals | ten selected cases, two of which are under a legal hold | "U-TM-01" reassigns them to "U-CO-03" with reason "R01" | eight cases move And the two held cases show MSG-P3-005 And the summary shows MSG-P3-035 with 8 of 10 | RWB-E2-012 |
| AC-EXC-P3-047-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-047-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.47.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-047-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-047-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.48 Reallocate when the caseload cap is breached

#### A2.48.1 Intent

**Business objective.** Moves the newest cases off an owner who is over the cap, until the cap is met.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.48.2 Description

**Functional overview.** Moves the newest cases off an owner who is over the cap, until the cap is met.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Reallocate when the caseload cap is breached | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-17

#### A2.48.3 Business rules and structure

##### A2.48.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-048-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| R-UNI-19 | Reallocate the newest cases until the owner is inside the cap, when the owner is above the maximum caseload | Moves to REALLOCATED |
| R-UNI-18 | Reallocate inside the same team by region and workload, keep the state and the clocks, when the owner leaves, is absent beyond the threshold, or the account is reassigned | Moves to REALLOCATED |
| BR-P3-048 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.48.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.48.4 Acceptance criteria

##### A2.48.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-048-01 | Rebalance | queue "TDR-BKK-CO" has 12 cases with no owner And members U-61 and U-62 hold 140 and 144 open cases | JOB-06 runs | the 12 cases are assigned, 8 to U-61 and 4 to U-62, by lowest load with ties going to the member first in the queue list And each assignment has reason "REBALANCE" and a decision log entry | RWB-E1-030 |

##### A2.48.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-048-01 | Measures reconcile | the snapshot taken at 2026-12-02 06:52 | the queue report refreshes | the depth of each queue equals the case list count for that queue at 06:52 And queue "TDR-BKK-CO" shows depth 296, unassigned 0 and an average age of 41 days | RWB-E1-030 |
| AC-ALT-P3-048-02 | A count difference holds the snapshot | the snapshot depth for "DIL-BKK-CO" is 88 and the case count at the same time is 87 | the snapshot is checked | it is not published And the data steward receives MSG-P3-029 with check "queue depth against case list" | RWB-E1-030 |

##### A2.48.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-048-01 | Breach alert | case RW-2026-000501 in queue "TDR-BKK-CO" passes its service level | the timer check raises the breach | the team manager of "TDR-BKK" receives MSG-P3-028 with count 1 and queue "TDR-BKK-CO" And the next snapshot shows 1 breach for "TDR-BKK-CO" in Power BI | RWB-E1-030 |
| AC-EXC-P3-048-02 | No member has capacity | every member of "TDR-BKK-CO" holds 150 open cases and 5 cases have no owner | JOB-06 runs | the 5 cases keep no owner And the team manager receives MSG-P3-011 with count 5 | RWB-E1-030 |
| AC-EXC-P3-048-03 | No cap loaded | queue "WO-BKK-CO" has no capacity cap | JOB-06 runs | no case in "WO-BKK-CO" is moved And the snapshot still reports "WO-BKK-CO" | RWB-E1-030 |
| AC-EXC-P3-048-04 | Decision log unavailable for one case | owner U-63 holds 153 open cases and the decision log write fails for the second of the 3 newest cases | JOB-06 runs | 2 cases are moved off U-63 and 1 stays And the job record lists the case that stayed with MSG-P7-003 | RWB-E1-030 |
| AC-EXC-P3-048-05 | A repeated run | JOB-06 has balanced "TDR-BKK-CO" on 2026-12-02 | JOB-06 runs again on 2026-12-02 | no case is moved And no decision log entry is written | RWB-E1-030 |
| AC-EXC-P3-048-06 | Held cases are not moved | owner U-64 holds 152 open cases and the 2 newest have deviation_open = true | JOB-06 runs | those 2 cases stay with U-64 and the next 2 newest are moved | RWB-E1-030 |
| AC-EXC-P3-048-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-048-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.48.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-048-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-048-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.49 Run the Epic 2 release checklist and go-live readiness

#### A2.49.1 Intent

**Business objective.** Works the release checklist, training and readiness for the December release.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.49.2 Description

**Functional overview.** Works the release checklist, training and readiness for the December release.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Tribe lead and squad members | Opens the screen and run the Epic 2 release checklist and go-live readiness | Checks the role, the capability area and the scope |
| 2 | Tribe lead and squad members | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-15

#### A2.49.3 Business rules and structure

##### A2.49.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-049-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P3-049 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.49.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.49.3.3 Roles and permissions

| Role | Use |
|---|---|
| Tribe lead and squad members | Primary |
| Team manager, Platform administrator | Also uses |

#### A2.49.4 Acceptance criteria

##### A2.49.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-049-01 | Run the Epic 2 release checklist and go-live readiness | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.49.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.49.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-049-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-049-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.49.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-049-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-049-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.50 Show the next action and its due date on a case

#### A2.50.1 Intent

**Business objective.** Every active case carries a named action, an owner and a due date, taken from the routing rule that moved it into its current state.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.50.2 Description

**Functional overview.** Every active case carries a named action, an owner and a due date, taken from the routing rule that moved it into its current state.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and show the next action and its due date on a case | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-03

#### A2.50.3 Business rules and structure

##### A2.50.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-050-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| VR-P3-050-2 | A move not allowed from the current state | MSG-P3-005 This case cannot move to {state} from {current}. |
| VR-P3-050-3 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| R-UNI-18 | Reallocate inside the same team by region and workload, keep the state and the clocks, when the owner leaves, is absent beyond the threshold, or the account is reassigned | Moves to REALLOCATED |
| R-UNI-20 | Stop every outbound action and every automated decision, keep the clocks visible, when a regulator, court or Legal places a hold | Moves to HELD_LEGAL |
| R-UNI-31 | Force a litigation review ahead of every other open action, when prescription_days_remaining reaches the warning threshold | Moves to ROUTE_D6_REOPEN |
| BR-P3-050 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.50.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | No |
| recovery_case.primary_person_key | The borrower the case is opened for: the ACE customer business key (`v_ace_customer.person_key`), no foreign key | varchar(255) | Yes | None | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | No |

##### A2.50.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Team manager | Also uses |

#### A2.50.4 Acceptance criteria

##### A2.50.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-050-01 | Every active case carries a next action | case "RW-2026-000401" with status IN_PROGRESS moved by R-RES-04 on 11 December 2026 | the case is opened | it shows action "Assign the case to a restructuring officer and start the offer clock", owner "Restructuring officer (FCR)" and due date 15 December 2026 | RWB-E2-035 |

##### A2.50.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-050-01 | The routing rules set it | case "RW-2026-000402" in state IN_FCR_QUEUE | event CASE_PICKED_UP fires R-RES-04 on Friday 11 December 2026 | the case holds next action text from R-RES-04, owner role RW-RESTRUCT, rule ID R-RES-04 and due date Tuesday 15 December 2026 And the values are written in the same transaction as the move to WITH_FCR_OFFICER | RWB-E2-035 |
| AC-ALT-P3-050-02 | Waiting is a valid next action | case "RW-2026-000403" moved by R-SET-13 on 14 December 2026 | the case is opened | the next action reads "Waiting for Customer (borrower): Set the payment due date and wait for the money" And the wait ends on 13 January 2027 And next action waiting is true | RWB-E2-035 |

##### A2.50.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-050-01 | A rule with no timer takes the state's service level | rule R-RES-03 moves the case to BACK_TO_ROUTE_DECISION with owner role RW-CASEOWN and timer "None" And the service levels and timers table holds 5 working days for BACK_TO_ROUTE_DECISION | R-RES-03 fires on Monday 14 December 2026 | the due date is Monday 21 December 2026 And the owner shown is the case owner named on the case | RWB-E2-035 |
| AC-EXC-P3-050-02 | No due date can be found | rule R-DEV-05 moves the case to DEV_WITH_OWNER with owner role RW-LEGAL and timer "deadline driven" And the service levels and timers table holds no row for DEV_WITH_OWNER | the rule fires on case "RW-2026-000404" of team "MTG-BKK" | the case holds the action and owner of R-DEV-05 with no due date And one task NEXT_ACTION_MISSING is raised on the exception queue for role RW-TEAMMGR of team "MTG-BKK" And the case record shows warning MSG-P2-023 | RWB-E2-035 |
| AC-EXC-P3-050-03 | A closed case has no next action | case "RW-2026-000404" with task NEXT_ACTION_MISSING open | the case closes with closure reason SETTLED | the next action fields are empty And the task is canceled And the case is not in the list of active cases with no next action | RWB-E2-035 |
| AC-EXC-P3-050-04 | A repeated transition changes nothing | case "RW-2026-000402" was moved by R-RES-04 on 11 December 2026 with decision log entry "DLE-SYN-0402" | the same transition with "DLE-SYN-0402" is processed again | the next action and due date are unchanged And no task is raised | RWB-E2-035 |
| AC-EXC-P3-050-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-050-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.50.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-050-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-050-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.51 Set the next action from the routing rules

#### A2.51.1 Intent

**Business objective.** On every state change the action, the owner of the next state and the timer from the firing rule become the case's next action.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.51.2 Description

**Functional overview.** On every state change the action, the owner of the next state and the timer from the firing rule become the case's next action.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Set the next action from the routing rules | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-27

#### A2.51.3 Business rules and structure

##### A2.51.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-051-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| VR-P3-051-2 | A timer will expire within its warning period | MSG-P3-003 {timer} ends on {date}. |
| VR-P3-051-3 | A move not allowed from the current state | MSG-P3-005 This case cannot move to {state} from {current}. |
| R-UNI-18 | Reallocate inside the same team by region and workload, keep the state and the clocks, when the owner leaves, is absent beyond the threshold, or the account is reassigned | Moves to REALLOCATED |
| R-UNI-20 | Stop every outbound action and every automated decision, keep the clocks visible, when a regulator, court or Legal places a hold | Moves to HELD_LEGAL |
| R-UNI-31 | Force a litigation review ahead of every other open action, when prescription_days_remaining reaches the warning threshold | Moves to ROUTE_D6_REOPEN |
| BR-P3-051 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.51.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Center of excellence analyst | Also uses |

#### A2.51.4 Acceptance criteria

##### A2.51.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-051-01 | Every active case carries a next action | case "RW-2026-000401" with status IN_PROGRESS moved by R-RES-04 on 11 December 2026 | the case is opened | it shows action "Assign the case to a restructuring officer and start the offer clock", owner "Restructuring officer (FCR)" and due date 15 December 2026 | RWB-E2-035 |

##### A2.51.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-051-01 | The routing rules set it | case "RW-2026-000402" in state IN_FCR_QUEUE | event CASE_PICKED_UP fires R-RES-04 on Friday 11 December 2026 | the case holds next action text from R-RES-04, owner role RW-RESTRUCT, rule ID R-RES-04 and due date Tuesday 15 December 2026 And the values are written in the same transaction as the move to WITH_FCR_OFFICER | RWB-E2-035 |
| AC-ALT-P3-051-02 | Waiting is a valid next action | case "RW-2026-000403" moved by R-SET-13 on 14 December 2026 | the case is opened | the next action reads "Waiting for Customer (borrower): Set the payment due date and wait for the money" And the wait ends on 13 January 2027 And next action waiting is true | RWB-E2-035 |

##### A2.51.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-051-01 | A rule with no timer takes the state's service level | rule R-RES-03 moves the case to BACK_TO_ROUTE_DECISION with owner role RW-CASEOWN and timer "None" And the service levels and timers table holds 5 working days for BACK_TO_ROUTE_DECISION | R-RES-03 fires on Monday 14 December 2026 | the due date is Monday 21 December 2026 And the owner shown is the case owner named on the case | RWB-E2-035 |
| AC-EXC-P3-051-02 | No due date can be found | rule R-DEV-05 moves the case to DEV_WITH_OWNER with owner role RW-LEGAL and timer "deadline driven" And the service levels and timers table holds no row for DEV_WITH_OWNER | the rule fires on case "RW-2026-000404" of team "MTG-BKK" | the case holds the action and owner of R-DEV-05 with no due date And one task NEXT_ACTION_MISSING is raised on the exception queue for role RW-TEAMMGR of team "MTG-BKK" And the case record shows warning MSG-P2-023 | RWB-E2-035 |
| AC-EXC-P3-051-03 | A closed case has no next action | case "RW-2026-000404" with task NEXT_ACTION_MISSING open | the case closes with closure reason SETTLED | the next action fields are empty And the task is canceled And the case is not in the list of active cases with no next action | RWB-E2-035 |
| AC-EXC-P3-051-04 | A repeated transition changes nothing | case "RW-2026-000402" was moved by R-RES-04 on 11 December 2026 with decision log entry "DLE-SYN-0402" | the same transition with "DLE-SYN-0402" is processed again | the next action and due date are unchanged And no task is raised | RWB-E2-035 |
| AC-EXC-P3-051-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-051-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.51.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-051-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-051-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

### A2.52 Accept a queue placement from a model or an agent

#### A2.52.1 Intent

**Business objective.** A caller that is not the allocation engine may place a case on a queue. The queue's own allocation, caseload and permission rules still apply, and the placement is logged with the caller and the model version. Disabled by feature flag until a consumer exists.

**Problem.** Cases are run from team spreadsheets; ownership and deadlines are agreed by email.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Cases inside the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.52.2 Description

**Functional overview.** A caller that is not the allocation engine may place a case on a queue. The queue's own allocation, caseload and permission rules still apply, and the placement is logged with the caller and the model version. Disabled by feature flag until a consumer exists.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Accept a queue placement from a model or an agent | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-04

#### A2.52.3 Business rules and structure

##### A2.52.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P3-052-1 | Transfer to an owner at the caseload cap | MSG-P3-002 {owner} is at the caseload cap. Choose another owner or the team queue. |
| VR-P3-052-2 | Allocation not recorded (RWB-E1-020) | MSG-P3-013 The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| VR-P3-052-3 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| R-UNI-06 | Raise X2, apply the vulnerable customer treatment rules, when hardship or vulnerability is recorded | Moves to HELD_DEVIATION |
| R-UNI-19 | Reallocate the newest cases until the owner is inside the cap, when the owner is above the maximum caseload | Moves to REALLOCATED |
| R-UNI-38 | Apply it to decisions taken from that date. Open cases keep the version they were decided under, when a new rule version reaches its effective date | Moves to RESUME_STATE |
| BR-P3-052 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.52.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Center of excellence analyst, Risk and model risk officer | Also uses |

#### A2.52.4 Acceptance criteria

##### A2.52.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P3-052-01 | A non-engine writer can place a case | None | SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0" | the response is 201 And the case is in queue "MTG-BKK-PRI" And the assignment and the case record show SY-AGENT as the identity that made the change | RWB-E2-036 |

##### A2.52.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P3-052-01 | The same rules still apply | queue "MTG-BKK-PRI" holds owners "U-5001" with 150 open cases and "U-5002" with 149 open cases | the model places case "RW-2026-000501" on it both owners hold 150 open cases and the model places case "RW-2026-000502" | the case is given to "U-5002" by round robin, skipping "U-5001" at the cap And the case status becomes ASSIGNED When both owners hold 150 open cases and the model places case "RW-2026-000502" case "RW-2026-000502" is in queue "MTG-BKK-OVF" with no owner and status NEW | RWB-E2-036 |
| AC-ALT-P3-052-02 | Every placement is logged | None | the model places case "RW-2026-000501" on queue "MTG-BKK-PRI" | one decision log entry exists with decision code D6, model version "MDL-SYN-PRIORITY 1.4.0", the reason "High cure score", the caller identity SY-AGENT and final call "PLACED MTG-BKK-PRI" And the entry, the case change, the assignment and the events commit in one transaction | RWB-E2-036 |

##### A2.52.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P3-052-01 | A caller that is not approved is refused | None | SY-AGENT places a case with modelOrAgent "MDL-SYN-UNLISTED" | the response is 422 with message MSG-P2-020 And nothing changes | RWB-E2-036 |
| AC-EXC-P3-052-02 | A closed case is refused | case "RW-2026-000503" has status CLOSED | the model places it on queue "MTG-BKK-PRI" | the response is 409 with message MSG-P3-005 And nothing changes | RWB-E2-036 |
| AC-EXC-P3-052-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P3-052-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.52.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P3-052-01 | Morning allocation | Case creation complete | Daily by 07:00 | Places new cases by rule | Every new case has a queue and an owner | No case waits for a person to allocate it |
| AC-BG-P3-052-02 | Timer check | Schedule | Every 5 minutes | Raises warnings and escalations | No timer passes unseen | Service levels and prescription dates are kept |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-CWC-001 | Every account at 90 or more days past due that is not excluded carries one recovery case, created by rule from the daily feed. | Must | E1 |
| REQ-CWC-002 | Each case carries a case ID in the form RW-YYYY-NNNNNN, issued once, never reused, and printed on every letter and document. | Must | E1 |
| REQ-CWC-003 | One case covers one customer and one product, with its accounts linked to it. | Must | E1 |
| REQ-CWC-004 | Exclusion rules for deceased, fraud, bankruptcy, an active restructure plan and an open dispute are held as data and applied at creation. | Must | E1 |
| REQ-CWC-005 | The case state model covers stage, status within stage, route and the deviation flags X1 to X7, and a case holds exactly one state at a time. | Must | E1 |
| REQ-CWC-006 | Roles, teams, queues, queue membership and capacity are held as versioned reference data and change without a code release. | Must | E1 |
| REQ-CWC-007 | Every new case is placed in a queue and assigned to a person by rule, and no case is allocated by hand as a matter of course. | Must | E1 |
| REQ-CWC-008 | Allocation rules read product, region, exposure band, stage, route, deviation flag, customer segment and collateral type, apply first match, and always have a default row. | Must | E1 |
| REQ-CWC-009 | Assignment rules support round robin, lowest load and a named owner for continuity, with a capacity cap and an overflow queue. | Must | E1 |
| REQ-CWC-010 | Cases move between queues and roles by transfer rules on stage change, route decision, timer expiry, deviation raised or cleared, approval needed, document received, payment missed, and manual request with a reason code. | Must | E1 |
| REQ-CWC-011 | Service levels per queue and status, warning thresholds and escalation targets are held as data, and a breach raises an event without moving the case. | Must | E1 |
| REQ-CWC-012 | Prescription dates are set from the legal periods table at case creation and are visible at all times. | Must | E1 |
| REQ-CWC-013 | A rule change goes from a validated template load to production with a version stamp and no code release, and rolls back to the previous version by one call. | Must | E1 |
| REQ-CWC-014 | Rule loads are validated for schema, overlapping rows, unreachable rows, a missing default and a set of test cases before they take effect. | Must | E1 |
| REQ-CWC-015 | Unassigned and over-capacity cases are rebalanced daily, and queue counts, ageing and service level breaches are reported. | Must | E1 |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it. | Must | E1 |
| REQ-CWC-017 | A queue accepts a write from an analytical model or an agent, carrying the case, the score, the priority and the reason, so that a daily decision reaches a queue the day it is made. | Must | E2 |
| REQ-CWC-018 | A model or agent writing to a queue passes the same permission checks as a person, runs under a service identity, and its write is logged with the model or agent version. | Must | E2 |
| REQ-CWC-019 | The queue write interface ships behind a feature flag and is switched on when the first model is approved to use it. | Must | E2 |
| REQ-CWC-020 | A queue holds work written by a model and work allocated by rule in the same queue, ordered by the same priority, so a person works one list. | Must | E2 |
| REQ-CHO-001 | A case transferred from collections reaches the Workbench on the day of transfer, with its full contact and promise history. | Must | E2 |
| REQ-CHO-002 | A change to a restructure plan status in ACE is visible on the case through the ACE common module. | Must | E2 |
| REQ-CHO-003 | Customer, product and account facts reach the case from the ACE database, which ingests them from SCBPDM and the core bank, read through the `v_ace_*` views (DL20 as amended by D-RCV-35). | Must | E2 |
| REQ-CHO-004 | The hand-over point is one agreed number of days past due, used by every rule and every report. | Must | E2 |
| REQ-CHO-005 | The Workbench is the system of record for case state after hand-over. | Must | E2 |
| REQ-CHO-006 | A treatment record exists for every offer made to a customer, holding its type, terms, approval and outcome. | Must | E2 |
| REQ-CHO-007 | Plan timers run from the treatment record, and a missed payment raises an event. | Must | E2 |
| REQ-CHO-008 | A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from `v_ace_account` for the next ACE business date. | Must | E2 |
| REQ-CHO-009 | Payments received are matched to the plan, the settlement or the fee they belong to, and anything unmatched goes to an exception list. | Must | E2 |
| REQ-CHO-010 | A duplicate case for the same customer and product merges into the earlier case, carrying its documents and decision log. | Should | E2 |
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state. | Must | E2 |
| REQ-WKM-002 | A team manager sees every queue in their team, filters by status, product and ageing, and exports the view. | Must | E2 |
| REQ-WKM-003 | A case is transferred or reassigned manually only with a reason code from the agreed list. | Must | E2 |
| REQ-WKM-004 | A case that breaches its service level is visible to the named escalation role without the case moving. | Must | E2 |
| REQ-WKM-005 | Timers, escalation state and the deviation flag are visible on the case record view. | Must | E2 |
| REQ-WKM-006 | Queue counts, ageing and breaches are reported daily and reconcile to the case list. | Must | E2 |
| REQ-WKM-007 | An owner who leaves, is absent beyond the threshold or breaches the caseload cap has their cases reallocated inside the team, keeping the state and the clocks. | Must | E2 |
| REQ-WKM-008 | Queue and transfer history is visible on the case so that a reader sees where the case has been. | Must | E2 |
| REQ-WKM-009 | A steering dashboard reports volume, ageing, route mix, turnaround and recovery against the baseline. | Must | E2 |
| REQ-WKM-010 | A capacity view shows inflow by product, bucket and region against available capacity. | Could | E7 |
| REQ-WKM-011 | Work allocated to a partner is visible in the same queue view as internal work. | Should | E2 |
| REQ-WKM-012 | Every open case carries one next action: what has to happen, who owns it and the date it is due. | Must | E2 |
| REQ-WKM-013 | The next action is produced from the rule that moved the case, taking the action, the owner of the next state and the timer that rule already carries. It is not entered by hand as a matter of course. | Must | E2 |
| REQ-WKM-014 | The next action is visible to whoever picks the case up, on the case record and in every queue view, without opening the history. | Must | E2 |
| REQ-WKM-015 | A next action that passes its due date raises the same escalation as any other service level breach, and the case does not move. | Must | E2 |
| REQ-WKM-016 | A case with no next action is reported as an exception, because a case nobody owes anything on is the state this program exists to remove. | Must | E2 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-01 My work | The person's open tasks, cases near a deadline and approvals waiting | E2 |
| SCR-02 Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation; account columns read from `v_ace_account` by business key | E1 |
| SCR-03 Case record | One case: accounts and parties read from ACE through the `v_ace_*` views, stage, owner, clocks, deviations, documents, decisions and history on one timeline | E1 read only; E2 full |
| SCR-04 Case timeline | Every action, decision, transfer, letter and document on the case, with filters | E2 |
| SCR-05 Transfer case | Move a case to another owner or queue with a reason | E2 |
| SCR-07 Team queues | Cases by queue with age, cap use and overflow | E2 |
| SCR-09 Exception queue | Cases and records that no rule matched, failed outbound actions and held receipts | E1 |

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
| Recovery case | กรณีติดตามหนี้ | One case per customer per product, from 90 days past due to close, with its accounts linked |
| Case number | เลขที่กรณี | The identifier issued when a case is created, in the form RW-YYYY-NNNNNN, never reused |
| Case owner | ผู้รับผิดชอบกรณี | The person who holds the case from day 90 to close and answers for its outcome |
| Case status | สถานะกรณี | One of New, Assigned, In progress, Waiting customer, Waiting partner, Waiting approval, On hold, Closed |
| Stage | ขั้นตอนหลัก | A part of the case lifecycle, such as litigation or asset disposal, in CMMN 1.1 terms |
| Route | แนวทางการแก้ไขหนี้ | The resolution path chosen for a case: R1 restructure to R8 write-off |
| Route state | สถานะตามแนวทาง | The state in a route set's decision table that the case is in |
| Task | งาน | A unit of work on a case for a person, a customer, a partner or a decision |
| Queue | คิวงาน | A list of cases belonging to one team and one role |
| Allocation | การจัดสรรงาน | Placing a new case in a queue and giving it an owner by rule |
| Transfer | การโอนงาน | Moving a case to another owner or queue with a reason |
| Caseload cap | จำนวนกรณีสูงสุดต่อคน | The most open cases one person may hold in a queue |
| Service level | ระยะเวลามาตรฐาน | How long a case may stay in a state before it escalates |
| Stage clock | นาฬิกาขั้นตอน | The time a case has spent in its current state, paused while a deviation is open |
| Prescription date | วันขาดอายุความ | The earliest date a legal claim on the case expires. It never pauses |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
