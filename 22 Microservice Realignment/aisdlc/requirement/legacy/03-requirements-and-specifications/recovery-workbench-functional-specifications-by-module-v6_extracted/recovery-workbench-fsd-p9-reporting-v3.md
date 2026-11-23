<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6.zip!Recovery Workbench FSD P9 Reporting v3.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6.zip!Recovery Workbench FSD P9 Reporting v3.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P9 Reporting

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P9 Reporting |
| Document ID | P9-RWB-FSD-v3 |
| Version | 3 |
| Status | In review |
| Classification | Confidential |
| Date | 15 November 2026 |
| Change note | v3, 15 November 2026: re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Reconciliation to `v_ace_account`; INT-01 and COLLINS load wording removed; `dq_exception` replaced by `reconciliation_result` break rows. Everything else unchanged from v2. |
| FSD owner | Business analyst, P9 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| P9 | Reporting | E1 baseline; E2 dashboard |

**Feature scope.** Baseline measures, steering dashboard, operational and regulatory reports.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P9 Reporting | TSD | Pair |
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

**In scope.** Baseline measures, steering dashboard, operational and regulatory reports.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-CWC-18; FEAT-OCC-12; FEAT-RDF-03; FEAT-RDF-10; FEAT-RDF-11; FEAT-RDF-14; FEAT-RDF-19; FEAT-RDF-20

**Constraints.** Built in the ACE service as part of the recovery module; source data read only from the ACE database through the SELECT-only `recovery.v_ace_*` views, landed by ACE's own ingestion, with no inbound load in the Workbench (D-RCV-35); every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P9 | FEAT-RPT-01 | Publish the reporting baseline | System | Produces the first measure set the benefit model is tracked against. | E1 | A2.1 |
| P9 | FEAT-RPT-02 | Publish queue and ageing measures | System | Publishes queue depth, ageing and the owner spread for every team. | E1 | A2.2 |
| P9 | FEAT-RPT-03 | Publish the steering dashboard | User | Gives the steering committee the monthly view of volume, outcome and decision quality. | E2 | A2.3 |
| P9 | FEAT-RPT-04 | Publish operations reporting from the decision log | System | Builds the operational reporting from the log, so reporting and audit read the same record. | E2 | A2.4 |
| P9 | FEAT-RPT-05 | Reconcile case counts across sources | System | Compares case counts between the Workbench, the data store and ALS and reports the difference. | E2 | A2.5 |
| P9 | FEAT-RPT-06 | Track benefit realisation | User | Tracks the measures in the benefit model against the baseline, monthly. | E6 | A2.6 |
| P9 | FEAT-RPT-07 | Produce regulatory returns | System | Builds the regulatory extracts from the data products and the decision log. | E8 | A2.7 |
| P9 | FEAT-RPT-08 | Refresh and publish the measure set | System | Runs the measure refresh on schedule and publishes with a freshness stamp. | E2 | A2.8 |
| P9 | FEAT-RPT-09 | Manage a data quality break | Admin | Works an open data quality break to closure, with an owner and a date. | E2 | A2.9 |
| P9 | FEAT-RPT-10 | Classify, stage and re-age an account | System | Applies the classification and re-ageing rules and recomputes the segment when they change. | E8 | A2.10 |

### A1.3 Background

Measures are counted by hand from spreadsheets at month end.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Publish the reporting baseline

#### A2.1.1 Intent

**Business objective.** Produces the first measure set the benefit model is tracked against.

**Problem.** Measures are counted by hand from spreadsheets at month end.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Measures read from the decision log | 100 percent | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Produces the first measure set the benefit model is tracked against.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Publish the reporting baseline | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Power BI, Data lake

**Prerequisites.** FEAT-RDF-19

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P9-001-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P9-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Reporting and BI analyst | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P9-001-01 | Definitions agreed | a definition file of 6 rows for "CASES_BY_ROUTE", "CASES_BY_AGE", "CASES_BY_QUEUE", "REALIZED_RECOVERY", "TIME_IN_STAGE" and "TAT_BY_ROUTE" And each row names its data product, formula, unit and approver "TRB-0001" with approval date 2026-11-20 | it is loaded with valid from 2026-11-21 | definition version "MD-2026.11" is in force with 6 measures And each measure returns its data product and formula through MeasureCatalog | RWB-E1-013 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P9-001-01 | Baseline published | the ACE batches of business date 2026-11-27 are COMPLETED in `v_ace_batch_status` | JOB-15 runs at 01:30 on 2026-11-28 | measure_snapshot holds rows for business date 2026-11-27 marked baseline and frozen with definition version "MD-2026.11" And "CASES_BY_ROUTE" totals 120 cases, of which 60 are Mortgage And "REALIZED_RECOVERY" equals the sum of synthetic payments since entry, 4,350,000.00 THB | RWB-E1-013 |
| AC-ALT-P9-001-02 | Power BI data set | the baseline measures are published | JOB-15 runs at 01:30 on 2026-12-02 | the INT-19 extract for business date 2026-12-01 is in the data lake with freshness stamp 2026-12-01 and the record count in its trailer And the extract holds the baseline rows of 2026-11-27 unchanged And the job monitor records the JOB-15 run with its row count, start and end time | RWB-E1-013 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P9-001-01 | Definition without a formula refused | a definition file where row "TIME_IN_STAGE" has no formula | it is loaded | the load is refused whole with MSG-GEN-001 naming "formula" And no definition version is put in force | RWB-E1-013 |
| AC-EXC-P9-001-02 | ACE batch of the baseline date not complete | the ACE batch for business date 2026-11-27 is not COMPLETED in `v_ace_batch_status` | JOB-15 runs at 01:30 on 2026-11-28 | no baseline rows are written for 2026-11-27 And the run record shows MSG-P1-001 naming "DP03 Case" and 2026-11-26 And the baseline is published by the first JOB-15 run after the ACE batch of 2026-11-27 completes | RWB-E1-013 |
| AC-EXC-P9-001-03 | Data lake unavailable | the data lake load area does not answer | JOB-15 runs at 01:30 on 2026-11-30 | measure_snapshot rows for 2026-11-28 are written in the Workbench And the extract is held and an alert goes to the operations channel with MSG-GEN-006 naming "Data lake" And the extract is sent by the next JOB-15 run | RWB-E1-013 |
| AC-EXC-P9-001-04 | Measure with no definition in force | the extract configuration lists measure "COST_PER_CASE" with no definition in force | JOB-15 runs at 01:30 on 2026-11-30 | no value for "COST_PER_CASE" is written And the run record shows MSG-P9-003 naming "COST_PER_CASE" | RWB-E1-013 |
| AC-EXC-P9-001-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P9-001-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Publish queue and ageing measures

#### A2.2.1 Intent

**Business objective.** Publishes queue depth, ageing and the owner spread for every team.

**Problem.** Measures are counted by hand from spreadsheets at month end.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Measures read from the decision log | 100 percent | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Publishes queue depth, ageing and the owner spread for every team.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Publish queue and ageing measures | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Power BI

**Prerequisites.** FEAT-CWC-18

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P9-002-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P9-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P9-002-01 | Rebalance | queue "TDR-BKK-CO" has 12 cases with no owner And members U-61 and U-62 hold 140 and 144 open cases | JOB-06 runs | the 12 cases are assigned, 8 to U-61 and 4 to U-62, by lowest load with ties going to the member first in the queue list And each assignment has reason "REBALANCE" and a decision log entry | RWB-E1-030 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P9-002-01 | Measures reconcile | the snapshot taken at 2026-12-02 06:52 | the queue report refreshes | the depth of each queue equals the case list count for that queue at 06:52 And queue "TDR-BKK-CO" shows depth 296, unassigned 0 and an average age of 41 days | RWB-E1-030 |
| AC-ALT-P9-002-02 | A count difference holds the snapshot | the snapshot depth for "DIL-BKK-CO" is 88 and the case count at the same time is 87 | the snapshot is checked | it is not published And the data steward receives MSG-P3-029 with check "queue depth against case list" | RWB-E1-030 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P9-002-01 | Breach alert | case RW-2026-000501 in queue "TDR-BKK-CO" passes its service level | the timer check raises the breach | the team manager of "TDR-BKK" receives MSG-P3-028 with count 1 and queue "TDR-BKK-CO" And the next snapshot shows 1 breach for "TDR-BKK-CO" in Power BI | RWB-E1-030 |
| AC-EXC-P9-002-02 | No member has capacity | every member of "TDR-BKK-CO" holds 150 open cases and 5 cases have no owner | JOB-06 runs | the 5 cases keep no owner And the team manager receives MSG-P3-011 with count 5 | RWB-E1-030 |
| AC-EXC-P9-002-03 | No cap loaded | queue "WO-BKK-CO" has no capacity cap | JOB-06 runs | no case in "WO-BKK-CO" is moved And the snapshot still reports "WO-BKK-CO" | RWB-E1-030 |
| AC-EXC-P9-002-04 | Decision log unavailable for one case | owner U-63 holds 153 open cases and the decision log write fails for the second of the 3 newest cases | JOB-06 runs | 2 cases are moved off U-63 and 1 stays And the job record lists the case that stayed with MSG-P7-003 | RWB-E1-030 |
| AC-EXC-P9-002-05 | A repeated run | JOB-06 has balanced "TDR-BKK-CO" on 2026-12-02 | JOB-06 runs again on 2026-12-02 | no case is moved And no decision log entry is written | RWB-E1-030 |
| AC-EXC-P9-002-06 | Held cases are not moved | owner U-64 holds 152 open cases and the 2 newest have deviation_open = true | JOB-06 runs | those 2 cases stay with U-64 and the next 2 newest are moved | RWB-E1-030 |
| AC-EXC-P9-002-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P9-002-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Publish the steering dashboard

#### A2.3.1 Intent

**Business objective.** Gives the steering committee the monthly view of volume, outcome and decision quality.

**Problem.** Measures are counted by hand from spreadsheets at month end.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Measures read from the decision log | 100 percent | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Gives the steering committee the monthly view of volume, outcome and decision quality.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Reporting and BI analyst | Opens the screen and publish the steering dashboard | Checks the role, the capability area and the scope |
| 2 | Reporting and BI analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Power BI

**Prerequisites.** FEAT-OCC-12

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P9-003-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P9-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| measure_definition.measure_code | Measure code | varchar(40) | Yes | None | No |
| measure_definition.name | Measure name | varchar(120) | Yes | None | No |
| measure_definition.formula | Formula in plain terms | varchar(1000) | Yes | None | No |
| measure_definition.data_product | Data product the measure reads | varchar(25) | Yes | LOV-DATA-PRODUCT | No |
| measure_definition.unit | Count, baht, days or percent | varchar(10) | Yes | LOV-MEASURE-UNIT | No |
| measure_definition.definition_version | Definition version, for example MD-2026.11 | varchar(20) | Yes | None | No |
| measure_definition.approved_by | Tribe lead who approved | uuid | No | None | No |
| measure_definition.approved_at | Approval time | timestamptz | No | None | No |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| Reporting and BI analyst | Primary |
| Tribe lead and squad members | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P9-003-01 | Refresh | the ACE batches of business date 2026-12-15 are COMPLETED in `v_ace_batch_status` | JOB-15 runs at 01:30 on 2026-12-16 | GET /reports/measures?from=2026-12-15&to=2026-12-15 returns a value for each of the 7 measures with period "2026-12-15" And the INT-19 extract for 2026-12-15 has freshness stamp 2026-12-15 for the 07:30 Power BI refresh | RWB-E2-009 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P9-003-01 | Reconciles | the case list shows 240 open cases at the 2026-12-15 cut-off | JOB-15 runs at 01:30 on 2026-12-16 | the sum of "CASES_BY_STAGE" for 2026-12-15 is 240 And "DECISIONS_LOGGED" for 2026-12-15 is 1,412, the count of decision log entries decided that day | RWB-E2-009 |
| AC-ALT-P9-003-02 | Agent measures | agent "case-intake" version "1.2.0" made 200 recommendations on 2026-12-15, of which 170 were accepted and 30 overridden with a reason | JOB-15 runs at 01:30 on 2026-12-16 | "AGENT_ACCEPTANCE" for "case-intake" "1.2.0" on 2026-12-15 is 85.0 percent And "AGENT_OVERRIDE" for "case-intake" "1.2.0" on 2026-12-15 is 15.0 percent And SCR-37 shows both rates by agent | RWB-E2-009 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P9-003-01 | Counts do not match | the case list shows 240 open cases at the 2026-12-15 cut-off And the case facts read for the dashboard total 239 | JOB-15 runs at 01:30 on 2026-12-16 | no snapshot rows and no extract are published for 2026-12-15 And SCR-37 shows 2026-12-14 as the latest day with MSG-P9-002 naming 239, 240 and 2026-12-15 And an alert goes to the Reporting and BI analyst and the data steward | RWB-E2-009 |
| AC-EXC-P9-003-02 | Agent with no runs | agent "deviation-screen" version "0.9.0" made no recommendations on 2026-12-15 | JOB-15 runs at 01:30 on 2026-12-16 | no "AGENT_ACCEPTANCE" value is written for "deviation-screen" on 2026-12-15 And SCR-37 shows "No runs" for "deviation-screen" on 2026-12-15 | RWB-E2-009 |
| AC-EXC-P9-003-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P9-003-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Publish operations reporting from the decision log

#### A2.4.1 Intent

**Business objective.** Builds the operational reporting from the log, so reporting and audit read the same record.

**Problem.** Measures are counted by hand from spreadsheets at month end.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Measures read from the decision log | 100 percent | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Builds the operational reporting from the log, so reporting and audit read the same record.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Publish operations reporting from the decision log | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Power BI, Data lake

**Prerequisites.** FEAT-RDF-20

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P9-004-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P9-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Reporting and BI analyst | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P9-004-01 | Daily copy | 380 entries were written on business date 2026-11-30 | JOB-13 runs at 01:00 on 2026-12-01 | the partition "business_date=2026-11-30" holds 380 rows And the manifest shows cumulative count 12,480 and last hash "a3f1...09c2" And the data lake copy has the same row count and the same last hash as the live log And the watermark moves to 12,480 and "a3f1...09c2" | RWB-E1-014 |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P9-004-01 | Retention rule | lake partitions for business dates 2024-11-29 and 2024-11-30 exist | the retention step of JOB-13 runs on 2026-12-01 | the partition "business_date=2024-11-29" moves to the archive tier And the job run records 1 partition archived under rule version "RET-2026.11" | RWB-E1-014 |
| AC-ALT-P9-004-02 | Two runs at the same time | JOB-13 is running for 2026-11-30 | a platform administrator posts a rerun of JOB-13 | the rerun is refused with status 409 and MSG-P2-006 And one run continues | RWB-E1-014 |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P9-004-01 | A copy that does not match is not published | the lake write for 2026-11-30 stops after 379 of 380 rows | the reconciliation step compares the copy with the live log | the partition is not marked complete And the watermark stays at 12,100 and "77be...41d0" And the job run shows check "REC-08" failed with MSG-P1-019 | RWB-E1-014 |
| AC-EXC-P9-004-02 | A repeat run for the same date writes no duplicates | JOB-13 completed for 2026-11-30 with 380 rows | JOB-13 is rerun for 2026-11-30 | the partition "business_date=2026-11-30" still holds 380 rows And the cumulative count stays 12,480 | RWB-E1-014 |
| AC-EXC-P9-004-03 | The decision log interface is unavailable | DecisionLogExport returns an error for every call | JOB-13 runs for 2026-11-30 | the job run ends with status "FAILED" and MSG-GEN-006 for system "Decision log" And the watermark and the previous partitions are unchanged | RWB-E1-014 |
| AC-EXC-P9-004-04 | A day with no new decisions | no entry was written after "77be...41d0" | JOB-13 runs for 2026-11-30 | the partition holds 0 rows and the manifest shows cumulative count 12,100 And check "REC-08" passes | RWB-E1-014 |
| AC-EXC-P9-004-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P9-004-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Reconcile case counts across sources

#### A2.5.1 Intent

**Business objective.** Compares case counts between the Workbench, the data store and ALS and reports the difference.

**Problem.** Measures are counted by hand from spreadsheets at month end.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Measures read from the decision log | 100 percent | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Compares case counts between the Workbench, the data store and ALS and reports the difference.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Reconcile case counts across sources | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Power BI, Data lake

**Prerequisites.** FEAT-RDF-11

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P9-005-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P9-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Reporting and BI analyst | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P9-005-01 | Variance under limit | the accounts in `v_ace_account` at 90 days past due or more less the exclusions are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903 And the case list rows at 90 days past due or more are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, with equal balance sums | the reconciliation step of JOB-04 runs | six reconciliation_result rows are written, REC-01 and REC-02 for each product, each with variance 0 and result PASS And the case list extract for 2026-11-30 is released for publish And the report after the 07:30 refresh shows all three products green | RWB-E1-011 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P9-005-01 | Variance over limit | the `v_ace_account` count for SSME is 2,903 and the case list holds 2,891 SSME rows at 90 days past due or more, a variance of 12 accounts, 0.41 percent | the reconciliation step runs | the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41 And 12 reconciliation_result break rows are written with check code "REC-01" and the 12 account numbers And the case list publish for 2026-11-30 is held and the lake keeps the case list of 2026-11-27 And the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ACE for SSME: a difference of 12 accounts, 0.41 percent." And the report shows SSME red with the 12 break rows, and MORTGAGE and HIRE_PURCHASE green | RWB-E1-011 |
| AC-ALT-P9-005-02 | Variance equal to the tolerance | the parameter recon.tolerance.pct for REC-01 is changed by a reference load to 0.10 from 2026-11-30 And the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent | the reconciliation step runs | the MORTGAGE result is PASS and the SSME result is BREAK | RWB-E1-011 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P9-005-01 | Account data not in ACE | the ACE batch for source ALS for 2026-11-30 is LATE and not COMPLETED in `v_ace_batch_status` | JOB-04 reaches the reconciliation step | no reconciliation_result for 2026-11-30 is written And the case list publish for 2026-11-30 is held And the report shows every product as not run with the reason "DP01 is from 2026-11-27" | RWB-E1-011 |
| AC-EXC-P9-005-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P9-005-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Track benefit realisation

#### A2.6.1 Intent

**Business objective.** Tracks the measures in the benefit model against the baseline, monthly.

**Problem.** Measures are counted by hand from spreadsheets at month end.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Measures read from the decision log | 100 percent | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Tracks the measures in the benefit model against the baseline, monthly.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Finance and CFO delegate | Opens the screen and track benefit realisation | Checks the role, the capability area and the scope |
| 2 | Finance and CFO delegate | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Power BI

**Prerequisites.** FEAT-RPT-01

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P9-006-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P9-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| measure_definition.measure_code | Measure code | varchar(40) | Yes | None | No |
| measure_definition.name | Measure name | varchar(120) | Yes | None | No |
| measure_definition.formula | Formula in plain terms | varchar(1000) | Yes | None | No |
| measure_definition.data_product | Data product the measure reads | varchar(25) | Yes | LOV-DATA-PRODUCT | No |
| measure_definition.unit | Count, baht, days or percent | varchar(10) | Yes | LOV-MEASURE-UNIT | No |
| measure_definition.definition_version | Definition version, for example MD-2026.11 | varchar(20) | Yes | None | No |
| measure_definition.approved_by | Tribe lead who approved | uuid | No | None | No |
| measure_definition.approved_at | Approval time | timestamptz | No | None | No |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| Finance and CFO delegate | Primary |
| Reporting and BI analyst, Tribe lead and squad members | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P9-006-01 | Track benefit realisation | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P9-006-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P9-006-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Produce regulatory returns

#### A2.7.1 Intent

**Business objective.** Builds the regulatory extracts from the data products and the decision log.

**Problem.** Measures are counted by hand from spreadsheets at month end.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Measures read from the decision log | 100 percent | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Builds the regulatory extracts from the data products and the decision log.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Produce regulatory returns | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Power BI, Data lake

**Prerequisites.** FEAT-RPT-04

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P9-007-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P9-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Compliance and PDPA officer | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P9-007-01 | Produce regulatory returns | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P9-007-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P9-007-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 Refresh and publish the measure set

#### A2.8.1 Intent

**Business objective.** Runs the measure refresh on schedule and publishes with a freshness stamp.

**Problem.** Measures are counted by hand from spreadsheets at month end.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Measures read from the decision log | 100 percent | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Runs the measure refresh on schedule and publishes with a freshness stamp.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Refresh and publish the measure set | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Power BI, Data lake

**Prerequisites.** FEAT-RDF-14

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P9-008-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P9-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Reporting and BI analyst | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P9-008-01 | Refresh | the ACE batches of business date 2026-12-15 are COMPLETED in `v_ace_batch_status` | JOB-15 runs at 01:30 on 2026-12-16 | GET /reports/measures?from=2026-12-15&to=2026-12-15 returns a value for each of the 7 measures with period "2026-12-15" And the INT-19 extract for 2026-12-15 has freshness stamp 2026-12-15 for the 07:30 Power BI refresh | RWB-E2-009 |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P9-008-01 | Reconciles | the case list shows 240 open cases at the 2026-12-15 cut-off | JOB-15 runs at 01:30 on 2026-12-16 | the sum of "CASES_BY_STAGE" for 2026-12-15 is 240 And "DECISIONS_LOGGED" for 2026-12-15 is 1,412, the count of decision log entries decided that day | RWB-E2-009 |
| AC-ALT-P9-008-02 | Agent measures | agent "case-intake" version "1.2.0" made 200 recommendations on 2026-12-15, of which 170 were accepted and 30 overridden with a reason | JOB-15 runs at 01:30 on 2026-12-16 | "AGENT_ACCEPTANCE" for "case-intake" "1.2.0" on 2026-12-15 is 85.0 percent And "AGENT_OVERRIDE" for "case-intake" "1.2.0" on 2026-12-15 is 15.0 percent And SCR-37 shows both rates by agent | RWB-E2-009 |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P9-008-01 | Counts do not match | the case list shows 240 open cases at the 2026-12-15 cut-off And the case facts read for the dashboard total 239 | JOB-15 runs at 01:30 on 2026-12-16 | no snapshot rows and no extract are published for 2026-12-15 And SCR-37 shows 2026-12-14 as the latest day with MSG-P9-002 naming 239, 240 and 2026-12-15 And an alert goes to the Reporting and BI analyst and the data steward | RWB-E2-009 |
| AC-EXC-P9-008-02 | Agent with no runs | agent "deviation-screen" version "0.9.0" made no recommendations on 2026-12-15 | JOB-15 runs at 01:30 on 2026-12-16 | no "AGENT_ACCEPTANCE" value is written for "deviation-screen" on 2026-12-15 And SCR-37 shows "No runs" for "deviation-screen" on 2026-12-15 | RWB-E2-009 |
| AC-EXC-P9-008-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P9-008-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.9 Manage a data quality break

#### A2.9.1 Intent

**Business objective.** Works an open data quality break to closure, with an owner and a date.

**Problem.** Measures are counted by hand from spreadsheets at month end.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Measures read from the decision log | 100 percent | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Works an open data quality break to closure, with an owner and a date.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Data steward and data product owner | Opens the screen and manage a data quality break | Checks the role, the capability area and the scope |
| 2 | Data steward and data product owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** ACE database

**Prerequisites.** FEAT-RDF-10

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P9-009-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P9-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| measure_definition.measure_code | Measure code | varchar(40) | Yes | None | No |
| measure_definition.name | Measure name | varchar(120) | Yes | None | No |
| measure_definition.formula | Formula in plain terms | varchar(1000) | Yes | None | No |
| measure_definition.data_product | Data product the measure reads | varchar(25) | Yes | LOV-DATA-PRODUCT | No |
| measure_definition.unit | Count, baht, days or percent | varchar(10) | Yes | LOV-MEASURE-UNIT | No |
| measure_definition.definition_version | Definition version, for example MD-2026.11 | varchar(20) | Yes | None | No |
| measure_definition.approved_by | Tribe lead who approved | uuid | No | None | No |
| measure_definition.approved_at | Approval time | timestamptz | No | None | No |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| Data steward and data product owner | Primary |
| Platform administrator | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P9-009-01 | Variance under limit | the accounts in `v_ace_account` at 90 days past due or more less the exclusions are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903 And the case list rows at 90 days past due or more are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, with equal balance sums | the reconciliation step of JOB-04 runs | six reconciliation_result rows are written, REC-01 and REC-02 for each product, each with variance 0 and result PASS And the case list extract for 2026-11-30 is released for publish And the report after the 07:30 refresh shows all three products green | RWB-E1-011 |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P9-009-01 | Variance over limit | the `v_ace_account` count for SSME is 2,903 and the case list holds 2,891 SSME rows at 90 days past due or more, a variance of 12 accounts, 0.41 percent | the reconciliation step runs | the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41 And 12 reconciliation_result break rows are written with check code "REC-01" and the 12 account numbers And the case list publish for 2026-11-30 is held and the lake keeps the case list of 2026-11-27 And the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ACE for SSME: a difference of 12 accounts, 0.41 percent." And the report shows SSME red with the 12 break rows, and MORTGAGE and HIRE_PURCHASE green | RWB-E1-011 |
| AC-ALT-P9-009-02 | Variance equal to the tolerance | the parameter recon.tolerance.pct for REC-01 is changed by a reference load to 0.10 from 2026-11-30 And the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent | the reconciliation step runs | the MORTGAGE result is PASS and the SSME result is BREAK | RWB-E1-011 |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P9-009-01 | Account data not in ACE | the ACE batch for source ALS for 2026-11-30 is LATE and not COMPLETED in `v_ace_batch_status` | JOB-04 reaches the reconciliation step | no reconciliation_result for 2026-11-30 is written And the case list publish for 2026-11-30 is held And the report shows every product as not run with the reason "DP01 is from 2026-11-27" | RWB-E1-011 |
| AC-EXC-P9-009-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P9-009-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.10 Classify, stage and re-age an account

#### A2.10.1 Intent

**Business objective.** Applies the classification and re-ageing rules and recomputes the segment when they change.

**Problem.** Measures are counted by hand from spreadsheets at month end.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Measures read from the decision log | 100 percent | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Applies the classification and re-ageing rules and recomputes the segment when they change.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Classify, stage and re-age an account | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, Workbench

**Prerequisites.** FEAT-RDF-03

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P9-010-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P9-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Risk and model risk officer | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P9-010-01 | Classify, stage and re-age an account | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P9-010-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P9-010-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-37 Steering dashboard | Inflow, stock, cures, recovery, turnaround and cost, by product and route | E2 |

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
| See the glossary | | |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
