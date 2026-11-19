<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6.zip!Recovery Workbench FSD S7 Write-off and recovery v3.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6.zip!Recovery Workbench FSD S7 Write-off and recovery v3.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S7 Write-off and recovery

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD S7 Write-off and recovery |
| Document ID | S7-RWB-FSD-v3 |
| Version | 3 |
| Status | In review |
| Classification | Confidential |
| Date | 15 November 2026 |
| Change note | v3, 15 November 2026: re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Write-off eligibility waits on the ACE ALS batch; write_off mirrored GL fields left for DEF-05. Everything else unchanged from v2. |
| FSD owner | Business analyst, S7 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| S7 | Write-off and recovery | E6 |

**Feature scope.** Eligibility, committee, posting, recovery after charge-off.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification S7 Write-off and recovery | TSD | Pair |
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

**In scope.** Eligibility, committee, posting, recovery after charge-off.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-APD-02; FEAT-CWC-14; FEAT-DBS-09; FEAT-DCM-17; FEAT-DRI-07; FEAT-PAY-01; FEAT-WOF-01; FEAT-WOF-03

**Constraints.** Built in the ACE service as part of the recovery module; source data read only from the ACE database through the SELECT-only `recovery.v_ace_*` views, landed by ACE's own ingestion, with no inbound load in the Workbench (D-RCV-35); every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| S7 | FEAT-WOF-01 | Run the monthly eligibility scan on both tracks | System | Scans the portfolio each month against the eligibility rules and proposes the write-off population. | E6 | A2.1 |
| S7 | FEAT-WOF-02 | Apply the tax criteria | System | Tests each proposed account against the tax criteria and records the result. | E6 | A2.2 |
| S7 | FEAT-WOF-03 | Prepare the write-off pack | System | Assembles the committee pack from the case facts, the documents and the recovery history. | E6 | A2.3 |
| S7 | FEAT-WOF-04 | Remove a case from the proposed population | User | Lets the write-off team take a case out of the population before committee, with a reason. | E6 | A2.4 |
| S7 | FEAT-WOF-05 | Route the population to the committee and schedule it | System | Sends the pack to the committee queue and books it into the monthly meeting. | E6 | A2.5 |
| S7 | FEAT-WOF-06 | Approve a write-off inside the limit | User | Lets the committee approve within its delegation and records the limit applied. | E6 | A2.6 |
| S7 | FEAT-WOF-07 | Reject a write-off | User | Lets the committee reject, with a reason that returns the case to recovery. | E6 | A2.7 |
| S7 | FEAT-WOF-08 | Defer a write-off | User | Lets the committee defer with a review date, and holds the case until then. | E6 | A2.8 |
| S7 | FEAT-WOF-09 | Post an approved write-off | System | Posts the write-off to ALS and the general ledger and releases the provision. | E6 | A2.9 |
| S7 | FEAT-WOF-10 | Send provision inputs to Finance | System | Produces the provision file Finance needs from the posted population. | E6 | A2.10 |
| S7 | FEAT-WOF-11 | Reconcile the approved and posted populations | System | Compares what the committee approved to what was posted, and raises every difference. | E6 | A2.11 |
| S7 | FEAT-WOF-12 | Work the write-off exception loop | User | Opens the exception path for a case the rules cannot clear. This loop has no owner today. | E6 | A2.12 |
| S7 | FEAT-WOF-13 | Close the case after the retention period | System | Closes the case once the retention period has run and no action is open. | E6 | A2.13 |
| S7 | FEAT-WOF-14 | Change the eligibility or tax criteria | Admin | Lets the center of excellence change the criteria as a versioned rule load. | E6 | A2.14 |
| S7 | FEAT-WOF-15 | Record a customer payment after charge-off | System | Takes a payment on a charged-off balance, applies it and records the recovery. | E6 | A2.15 |
| S7 | FEAT-WOF-16 | Sell a post charge-off population | User | Opens the sale of charged-off accounts, with the approval the limit requires. | E6 | A2.16 |

### A1.3 Background

Write-off populations are assembled by hand each month.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Run the monthly eligibility scan on both tracks

#### A2.1.1 Intent

**Business objective.** Scans the portfolio each month against the eligibility rules and proposes the write-off population.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Scans the portfolio each month against the eligibility rules and proposes the write-off population.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the monthly eligibility scan on both tracks | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, Workbench

**Prerequisites.** FEAT-DRI-07

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-001-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| R-WO-01 | Test every open case against the eligibility rule on both tracks and the tax criteria, when cut_off_date reached and the ACE batch for source ALS is COMPLETED in `v_ace_batch_status` | Moves to POPULATION_PROPOSED |
| BR-S7-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Write-off team member | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-001-01 | Run the monthly eligibility scan on both tracks | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-001-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-001-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-001-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.2 Apply the tax criteria

#### A2.2.1 Intent

**Business objective.** Tests each proposed account against the tax criteria and records the result.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Tests each proposed account against the tax criteria and records the result.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Apply the tax criteria | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-WOF-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-002-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| R-WO-01 | Test every open case against the eligibility rule on both tracks and the tax criteria, when cut_off_date reached and the ACE batch for source ALS is COMPLETED in `v_ace_batch_status` | Moves to POPULATION_PROPOSED |
| R-WO-51 | Record the remittance against the sold account and close the item, when the buyer confirms receipt | Moves to CASE_CLOSED |
| BR-S7-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Write-off team member | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-002-01 | Apply the tax criteria | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-002-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-002-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-002-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.3 Prepare the write-off pack

#### A2.3.1 Intent

**Business objective.** Assembles the committee pack from the case facts, the documents and the recovery history.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Assembles the committee pack from the case facts, the documents and the recovery history.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Prepare the write-off pack | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, the Workbench document hub

**Prerequisites.** FEAT-WOF-01

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-003-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| R-WO-05 | Write-off agent prepares the pack: balance, provision carried, route history, legal and asset state, residual, when the event occurs | Moves to PACK_PREPARED |
| BR-S7-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Write-off team member | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-003-01 | Prepare the write-off pack | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-003-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-003-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-003-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.4 Remove a case from the proposed population

#### A2.4.1 Intent

**Business objective.** Lets the write-off team take a case out of the population before committee, with a reason.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Lets the write-off team take a case out of the population before committee, with a reason.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Write-off team member | Opens the screen and remove a case from the proposed population | Checks the role, the capability area and the scope |
| 2 | Write-off team member | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-WOF-03

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-004-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| R-WO-07 | Remove the case from the proposed population with the reason recorded, when removal_reason present | Moves to CASE_REMOVED_BY_TEAM |
| BR-S7-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| write_off.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| write_off.decision_log_id | The decision_log_entry this record belongs to | uuid | No | None | No |
| write_off.amount | Amount written off, baht | numeric(18,2) | Yes | None | No |
| write_off.tax_criteria_met | True when the tax criteria are met | boolean | Yes | None | No |
| write_off.committee_date | Committee approval date | date | No | None | No |
| write_off.posted_date | Posting date | date | No | None | No |
| write_off.responsibility_center | Responsibility center | varchar(10) | No | None | No |
| write_off.cost_center | Operating cost center | varchar(10) | No | None | No |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| Write-off team member | Primary |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-004-01 | Remove a case from the proposed population | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-004-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-004-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-004-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.5 Route the population to the committee and schedule it

#### A2.5.1 Intent

**Business objective.** Sends the pack to the committee queue and books it into the monthly meeting.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Sends the pack to the committee queue and books it into the monthly meeting.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Route the population to the committee and schedule it | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-WOF-03

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-005-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-WO-11 | Route the pack to the committee and schedule the meeting, when amount inside the write-off committee limit | Moves to WITH_COMMITTEE |
| R-WO-06 | Hold the case out of the population and route it to the deviation handler, when deviation_open in (X1 to X7) | Moves to CASE_REMOVED_BY_TEAM |
| R-WO-10 | Route the pack to the committee, when provision_carried and the pack document are present | Moves to WITH_COMMITTEE |
| BR-S7-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Write-off committee member | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-005-01 | Route the population to the committee and schedule it | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-005-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-005-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-005-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.6 Approve a write-off inside the limit

#### A2.6.1 Intent

**Business objective.** Lets the committee approve within its delegation and records the limit applied.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Lets the committee approve within its delegation and records the limit applied.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Write-off committee member | Opens the screen and approve a write-off inside the limit | Checks the role, the capability area and the scope |
| 2 | Write-off committee member | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-02

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-006-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| R-WO-15 | Record the final call, the approver and the limit applied, and release to posting, when approved inside the delegation | Moves to APPROVED |
| R-WO-12 | Route the pack to the credit approval committee chaired by the product head with Risk, when amount above the write-off committee limit | Moves to ESCALATED_TO_CREDIT_COMMITTEE |
| R-WO-24 | Raise the write-off exception for correction, when retry_count at or above the retry limit | Moves to WRITEOFF_EXCEPTION |
| BR-S7-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| write_off.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| write_off.decision_log_id | The decision_log_entry this record belongs to | uuid | No | None | No |
| write_off.amount | Amount written off, baht | numeric(18,2) | Yes | None | No |
| write_off.tax_criteria_met | True when the tax criteria are met | boolean | Yes | None | No |
| write_off.committee_date | Committee approval date | date | No | None | No |
| write_off.posted_date | Posting date | date | No | None | No |
| write_off.responsibility_center | Responsibility center | varchar(10) | No | None | No |
| write_off.cost_center | Operating cost center | varchar(10) | No | None | No |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| Write-off committee member | Primary |
| Finance and CFO delegate | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-006-01 | Approve a write-off inside the limit | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-006-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-006-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-006-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.7 Reject a write-off

#### A2.7.1 Intent

**Business objective.** Lets the committee reject, with a reason that returns the case to recovery.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Lets the committee reject, with a reason that returns the case to recovery.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Write-off committee member | Opens the screen and reject a write-off | Checks the role, the capability area and the scope |
| 2 | Write-off committee member | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-WOF-06

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-007-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| BR-S7-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| write_off.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| write_off.decision_log_id | The decision_log_entry this record belongs to | uuid | No | None | No |
| write_off.amount | Amount written off, baht | numeric(18,2) | Yes | None | No |
| write_off.tax_criteria_met | True when the tax criteria are met | boolean | Yes | None | No |
| write_off.committee_date | Committee approval date | date | No | None | No |
| write_off.posted_date | Posting date | date | No | None | No |
| write_off.responsibility_center | Responsibility center | varchar(10) | No | None | No |
| write_off.cost_center | Operating cost center | varchar(10) | No | None | No |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| Write-off committee member | Primary |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-007-01 | Reject a write-off | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-007-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-007-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-007-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.8 Defer a write-off

#### A2.8.1 Intent

**Business objective.** Lets the committee defer with a review date, and holds the case until then.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Lets the committee defer with a review date, and holds the case until then.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Write-off committee member | Opens the screen and defer a write-off | Checks the role, the capability area and the scope |
| 2 | Write-off committee member | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-WOF-06

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-008-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| R-WO-17 | Set the review timer and hold the case for the next scan, when review_date present | Moves to DEFERRED |
| BR-S7-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| write_off.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| write_off.decision_log_id | The decision_log_entry this record belongs to | uuid | No | None | No |
| write_off.amount | Amount written off, baht | numeric(18,2) | Yes | None | No |
| write_off.tax_criteria_met | True when the tax criteria are met | boolean | Yes | None | No |
| write_off.committee_date | Committee approval date | date | No | None | No |
| write_off.posted_date | Posting date | date | No | None | No |
| write_off.responsibility_center | Responsibility center | varchar(10) | No | None | No |
| write_off.cost_center | Operating cost center | varchar(10) | No | None | No |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| Write-off committee member | Primary |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-008-01 | Defer a write-off | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-008-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-008-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-008-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.9 Post an approved write-off

#### A2.9.1 Intent

**Business objective.** Posts the write-off to ALS and the general ledger and releases the provision.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Posts the write-off to ALS and the general ledger and releases the provision.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Post an approved write-off | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-WOF-06

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-009-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| R-WO-05 | Write-off agent prepares the pack: balance, provision carried, route history, legal and asset state, residual, when the event occurs | Moves to PACK_PREPARED |
| R-WO-23 | Re-post to ALS and the general ledger, when retry_count below the retry limit and the cause is cleared | Moves to POSTING_PENDING |
| R-WO-44 | Re-post to ALS and the general ledger, when the owner decides to re-post | Moves to POSTING_PENDING |
| BR-S7-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Credit Administration officer | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-009-01 | Post an approved write-off | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-009-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-009-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-009-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.10 Send provision inputs to Finance

#### A2.10.1 Intent

**Business objective.** Produces the provision file Finance needs from the posted population.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Produces the provision file Finance needs from the posted population.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Send provision inputs to Finance | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-WOF-09

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-010-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| R-WO-26 | Send the provision inputs and the tax file to Finance, when the event occurs | Moves to FINANCE_FEED_SENT |
| BR-S7-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Finance and CFO delegate | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-010-01 | Send provision inputs to Finance | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-010-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-010-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-010-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.11 Reconcile the approved and posted populations

#### A2.11.1 Intent

**Business objective.** Compares what the committee approved to what was posted, and raises every difference.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Compares what the committee approved to what was posted, and raises every difference.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Reconcile the approved and posted populations | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, Workbench

**Prerequisites.** FEAT-WOF-09

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-011-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-WO-13 | Record the final call and release the case to posting, when approved inside the delegation with Risk | Moves to APPROVED |
| R-WO-15 | Record the final call, the approver and the limit applied, and release to posting, when approved inside the delegation | Moves to APPROVED |
| BR-S7-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Credit Administration officer | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-011-01 | Reconcile the approved and posted populations | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-011-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-011-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-011-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.12 Work the write-off exception loop

#### A2.12.1 Intent

**Business objective.** Opens the exception path for a case the rules cannot clear. This loop has no owner today.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Opens the exception path for a case the rules cannot clear. This loop has no owner today.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Write-off committee member | Opens the screen and work the write-off exception loop | Checks the role, the capability area and the scope |
| 2 | Write-off committee member | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-WOF-11

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-012-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| VR-S7-012-2 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| R-WO-24 | Raise the write-off exception for correction, when retry_count at or above the retry limit | Moves to WRITEOFF_EXCEPTION |
| BR-S7-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| write_off.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| write_off.decision_log_id | The decision_log_entry this record belongs to | uuid | No | None | No |
| write_off.amount | Amount written off, baht | numeric(18,2) | Yes | None | No |
| write_off.tax_criteria_met | True when the tax criteria are met | boolean | Yes | None | No |
| write_off.committee_date | Committee approval date | date | No | None | No |
| write_off.posted_date | Posting date | date | No | None | No |
| write_off.responsibility_center | Responsibility center | varchar(10) | No | None | No |
| write_off.cost_center | Operating cost center | varchar(10) | No | None | No |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| Write-off committee member | Primary |
| Write-off team member, Finance and CFO delegate | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-012-01 | Work the write-off exception loop | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-012-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-012-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-012-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.13 Close the case after the retention period

#### A2.13.1 Intent

**Business objective.** Closes the case once the retention period has run and no action is open.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Closes the case once the retention period has run and no action is open.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Close the case after the retention period | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DCM-17

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-013-1 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| R-WO-36 | Close the placement and start the retention timer, when ends_at passed and recovered_amount = 0 | Moves to RETENTION_RUNNING |
| R-WO-47 | Close the case, stop every timer and write the closing entry with cash recovered and loss, when no open placement, no open sale, no open exception, and a retention class on every document | Moves to CASE_CLOSED |
| BR-S7-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Credit Administration officer | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-013-01 | Close the case after the retention period | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-013-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-013-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-013-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.14 Change the eligibility or tax criteria

#### A2.14.1 Intent

**Business objective.** Lets the center of excellence change the criteria as a versioned rule load.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Lets the center of excellence change the criteria as a versioned rule load.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and change the eligibility or tax criteria | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, Rules component

**Prerequisites.** FEAT-CWC-14

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-014-1 | Write-off without the tax criteria version (R-WO-03) | MSG-S7-001 The scan is on hold until Finance publishes the tax criteria. |
| R-WO-01 | Test every open case against the eligibility rule on both tracks and the tax criteria, when cut_off_date reached and the ACE batch for source ALS is COMPLETED in `v_ace_batch_status` | Moves to POPULATION_PROPOSED |
| BR-S7-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| write_off.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| write_off.decision_log_id | The decision_log_entry this record belongs to | uuid | No | None | No |
| write_off.amount | Amount written off, baht | numeric(18,2) | Yes | None | No |
| write_off.tax_criteria_met | True when the tax criteria are met | boolean | Yes | None | No |
| write_off.committee_date | Committee approval date | date | No | None | No |
| write_off.posted_date | Posting date | date | No | None | No |
| write_off.responsibility_center | Responsibility center | varchar(10) | No | None | No |
| write_off.cost_center | Operating cost center | varchar(10) | No | None | No |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Finance and CFO delegate, Risk and model risk officer | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-014-01 | Change the eligibility or tax criteria | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-014-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-014-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-014-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.15 Record a customer payment after charge-off

#### A2.15.1 Intent

**Business objective.** Takes a payment on a charged-off balance, applies it and records the recovery.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Takes a payment on a charged-off balance, applies it and records the recovery.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Record a customer payment after charge-off | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-PAY-01

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-015-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-WO-37 | Post the recovery as post charge-off income and calculate the agency fee, when the payment matches the case and the placement | Moves to PAYMENT_MATCHED |
| R-WO-49 | Post the recovery as post charge-off income against the closed case, when the payment matches a closed case with no placement | Moves to PAYMENT_MATCHED |
| R-WO-50 | Record the post charge-off sale and close the case, when buyer settles and the data transfer completes | Moves to CASE_CLOSED |
| BR-S7-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Credit Administration officer | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-015-01 | Record a customer payment after charge-off | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-015-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-015-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-015-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

### A2.16 Sell a post charge-off population

#### A2.16.1 Intent

**Business objective.** Opens the sale of charged-off accounts, with the approval the limit requires.

**Problem.** Write-off populations are assembled by hand each month.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Opens the sale of charged-off accounts, with the approval the limit requires.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Debt sale officer | Opens the screen and sell a post charge-off population | Checks the role, the capability area and the scope |
| 2 | Debt sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal, ALS and GL

**Prerequisites.** FEAT-DBS-09

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S7-016-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-WO-12 | Route the pack to the credit approval committee chaired by the product head with Risk, when amount above the write-off committee limit | Moves to ESCALATED_TO_CREDIT_COMMITTEE |
| R-WO-32 | Hand the charged-off population to the debt sale route, when placement_type = sale | Moves to SOLD_POST_CHARGEOFF |
| BR-S7-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| write_off.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| write_off.decision_log_id | The decision_log_entry this record belongs to | uuid | No | None | No |
| write_off.amount | Amount written off, baht | numeric(18,2) | Yes | None | No |
| write_off.tax_criteria_met | True when the tax criteria are met | boolean | Yes | None | No |
| write_off.committee_date | Committee approval date | date | No | None | No |
| write_off.posted_date | Posting date | date | No | None | No |
| write_off.responsibility_center | Responsibility center | varchar(10) | No | None | No |
| write_off.cost_center | Operating cost center | varchar(10) | No | None | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Debt sale officer | Primary |
| Head of Asset Liquidity | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S7-016-01 | Sell a post charge-off population | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S7-016-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S7-016-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-S7-016-01 | Write-off scan | Schedule | Monthly | Tests open cases against eligibility | Population for the committee | No eligible case is missed |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-S7-001 | Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks. | Must | E6 |
| REQ-S7-002 | The committee pack is prepared from case and provision data with no manual assembly. | Must | E6 |
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account. | Must | E6 |
| REQ-S7-004 | The write-off exception loop has one named owner and a time limit. | Must | E6 |
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published. | Must | E6 |
| REQ-S7-006 | Post charge-off treatment is set by rule, including placement with an agency. | Must | E6 |
| REQ-S7-007 | Recoveries after charge-off are matched to the account, with income and agency fees recorded. | Must | E6 |
| REQ-S7-008 | A case closes after its retention period, and reopening a closed case needs a written rule, a reason and an approver. | Must | E6 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-27 Write-off proposal | The monthly population, the pack per case and removals with reasons | E6 |

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
| Write-off | การตัดหนี้สูญ | Removing the balance from the books after approval |
| Recovery after charge-off | การติดตามหนี้หลังตัดหนี้สูญ | Money collected after a write-off |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
