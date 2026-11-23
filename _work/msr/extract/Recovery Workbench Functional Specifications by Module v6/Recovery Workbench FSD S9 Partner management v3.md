# Recovery Workbench S9 Partner management

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD S9 Partner management |
| Document ID | S9-RWB-FSD-v3 |
| Version | 3 |
| Status | In review |
| Classification | Confidential |
| Date | 15 November 2026 |
| Change note | v3, 15 November 2026: re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Constraint, freshness rule and trigger wording only. Everything else unchanged from v2. |
| FSD owner | Business analyst, S9 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| S9 | Partner management | E6 panel; E7 scoring |

**Feature scope.** Panel, allocation, fees, scorecards, conduct.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification S9 Partner management | TSD | Pair |
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

**In scope.** Panel, allocation, fees, scorecards, conduct.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-AST-07; FEAT-CWC-23; FEAT-DCM-21; FEAT-OCC-13; FEAT-PAY-01; FEAT-PRM-02; FEAT-PRM-03; FEAT-PRM-05

**Constraints.** Built in the ACE service as part of the recovery module; source data read only from the ACE database through the SELECT-only `recovery.v_ace_*` views, landed by ACE's own ingestion, with no inbound load in the Workbench (D-RCV-35); every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| S9 | FEAT-PRM-01 | Onboard a partner and set terms | User | Takes a partner onto the panel with its contract, fee schedule, service levels and scope. | E6 | A2.1 |
| S9 | FEAT-PRM-02 | Hold the partner panel and fee schedule as data | Admin | Keeps every panel, fee schedule and service level as versioned reference data. | E6 | A2.2 |
| S9 | FEAT-PRM-03 | Allocate work by measured return | System | Places work with the partner the scorecard rule picks, not by rotation or habit. | E6 | A2.3 |
| S9 | FEAT-PRM-04 | Override an allocation with a reason | User | Lets the partner manager place work differently, with the reason recorded. | E6 | A2.4 |
| S9 | FEAT-PRM-05 | Receive a partner result into the case | System | Takes contact, promise and cash results from the portal onto the case the same day. | E6 | A2.5 |
| S9 | FEAT-PRM-06 | Place a charged-off account with an agency | User | Places post charge-off accounts with an agency under the placement rule. | E6 | A2.6 |
| S9 | FEAT-PRM-07 | Match a recovery and calculate the agency fee | System | Matches money recovered by an agency to the case and works out the fee due. | E6 | A2.7 |
| S9 | FEAT-PRM-08 | Score partners monthly | System | Builds the scorecard from the measured results and publishes it to the panel. | E7 | A2.8 |
| S9 | FEAT-PRM-09 | Approve partner fees | User | Checks the fee claim against the schedule and the result, and approves it. | E7 | A2.9 |
| S9 | FEAT-PRM-10 | Hold a partner review | User | Runs the review against the six points every partner type is managed on, and records the actions. | E7 | A2.10 |
| S9 | FEAT-PRM-11 | Issue a notice on a missed target | User | Sends the contractual notice when a partner misses its targets, and starts the cure period. | E7 | A2.11 |
| S9 | FEAT-PRM-12 | End a partner contract and recall the work | User | Closes the contract and pulls every open case back for re-selection. | E7 | A2.12 |
| S9 | FEAT-PRM-13 | Check partner conduct | System | Samples partner contacts and complaints against the conduct rules and raises breaches. | E7 | A2.13 |
| S9 | FEAT-PRM-14 | Manage extra costs and services on an asset | User | Records and approves additional partner costs on a held asset. | E7 | A2.14 |
| S9 | FEAT-PRM-15 | Capture field work through the field app | User | Lets the field collector record visits, photos and bills against the case from the field. | E7 | A2.15 |

### A1.3 Background

Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Onboard a partner and set terms

#### A2.1.1 Intent

**Business objective.** Takes a partner onto the panel with its contract, fee schedule, service levels and scope.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Takes a partner onto the panel with its contract, fee schedule, service levels and scope.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Partner and agency manager | Opens the screen and onboard a partner and set terms | Checks the role, the capability area and the scope |
| 2 | Partner and agency manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal

**Prerequisites.** FEAT-OCC-13

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-001-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | No |
| partner.contract_end | Contract end date | date | No | None | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | No |
| partner_instruction.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| partner_instruction.partner_id | The partner this record belongs to | uuid | Yes | None | No |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| Partner and agency manager | Primary |
| Head of Litigation, Head of Asset Liquidity | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-001-01 | Onboard a partner and set terms | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-001-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-001-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Hold the partner panel and fee schedule as data

#### A2.2.1 Intent

**Business objective.** Keeps every panel, fee schedule and service level as versioned reference data.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Keeps every panel, fee schedule and service level as versioned reference data.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Reference data administrator | Opens the screen and hold the partner panel and fee schedule as data | Checks the role, the capability area and the scope |
| 2 | Reference data administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-23

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-002-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | No |
| partner.contract_end | Contract end date | date | No | None | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | No |
| partner_instruction.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| partner_instruction.partner_id | The partner this record belongs to | uuid | Yes | None | No |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| Reference data administrator | Primary |
| Partner and agency manager | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-002-01 | Hold the partner panel and fee schedule as data | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-002-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-002-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Allocate work by measured return

#### A2.3.1 Intent

**Business objective.** Places work with the partner the scorecard rule picks, not by rotation or habit.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Places work with the partner the scorecard rule picks, not by rotation or habit.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Allocate work by measured return | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal, Rules component

**Prerequisites.** FEAT-PRM-02

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-003-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S9-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Partner and agency manager | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-003-01 | Allocate work by measured return | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-003-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-003-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Override an allocation with a reason

#### A2.4.1 Intent

**Business objective.** Lets the partner manager place work differently, with the reason recorded.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Lets the partner manager place work differently, with the reason recorded.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Partner and agency manager | Opens the screen and override an allocation with a reason | Checks the role, the capability area and the scope |
| 2 | Partner and agency manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal

**Prerequisites.** FEAT-PRM-03

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-004-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | No |
| partner.contract_end | Contract end date | date | No | None | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | No |
| partner_instruction.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| partner_instruction.partner_id | The partner this record belongs to | uuid | Yes | None | No |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| Partner and agency manager | Primary |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-004-01 | Override an allocation with a reason | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-004-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-004-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Receive a partner result into the case

#### A2.5.1 Intent

**Business objective.** Takes contact, promise and cash results from the portal onto the case the same day.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Takes contact, promise and cash results from the portal onto the case the same day.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Receive a partner result into the case | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal

**Prerequisites.** FEAT-PRM-03

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-005-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S9-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-005-01 | Receive a partner result into the case | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-005-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-005-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Place a charged-off account with an agency

#### A2.6.1 Intent

**Business objective.** Places post charge-off accounts with an agency under the placement rule.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Places post charge-off accounts with an agency under the placement rule.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Partner and agency manager | Opens the screen and place a charged-off account with an agency | Checks the role, the capability area and the scope |
| 2 | Partner and agency manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal

**Prerequisites.** FEAT-PRM-03

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-006-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | No |
| partner.contract_end | Contract end date | date | No | None | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | No |
| partner_instruction.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| partner_instruction.partner_id | The partner this record belongs to | uuid | Yes | None | No |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| Partner and agency manager | Primary |
| Credit Administration officer | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-006-01 | Place a charged-off account with an agency | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-006-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-006-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Match a recovery and calculate the agency fee

#### A2.7.1 Intent

**Business objective.** Matches money recovered by an agency to the case and works out the fee due.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Matches money recovered by an agency to the case and works out the fee due.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Match a recovery and calculate the agency fee | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, Partner portal

**Prerequisites.** FEAT-PAY-01

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-007-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S9-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Partner and agency manager | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-007-01 | Match a recovery and calculate the agency fee | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-007-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-007-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 Score partners monthly

#### A2.8.1 Intent

**Business objective.** Builds the scorecard from the measured results and publishes it to the panel.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Builds the scorecard from the measured results and publishes it to the panel.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Score partners monthly | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal, Power BI

**Prerequisites.** FEAT-PRM-05

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-008-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S9-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Partner and agency manager | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-008-01 | Score partners monthly | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-008-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-008-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.9 Approve partner fees

#### A2.9.1 Intent

**Business objective.** Checks the fee claim against the schedule and the result, and approves it.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Checks the fee claim against the schedule and the result, and approves it.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Partner and agency manager | Opens the screen and approve partner fees | Checks the role, the capability area and the scope |
| 2 | Partner and agency manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal

**Prerequisites.** FEAT-PRM-07

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-009-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | No |
| partner.contract_end | Contract end date | date | No | None | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | No |
| partner_instruction.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| partner_instruction.partner_id | The partner this record belongs to | uuid | Yes | None | No |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| Partner and agency manager | Primary |
| Finance and CFO delegate | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-009-01 | Approve partner fees | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-009-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-009-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.10 Hold a partner review

#### A2.10.1 Intent

**Business objective.** Runs the review against the six points every partner type is managed on, and records the actions.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Runs the review against the six points every partner type is managed on, and records the actions.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Partner and agency manager | Opens the screen and hold a partner review | Checks the role, the capability area and the scope |
| 2 | Partner and agency manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal

**Prerequisites.** FEAT-PRM-08

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-010-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | No |
| partner.contract_end | Contract end date | date | No | None | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | No |
| partner_instruction.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| partner_instruction.partner_id | The partner this record belongs to | uuid | Yes | None | No |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| Partner and agency manager | Primary |
| Head of Litigation, Head of Asset Liquidity | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-010-01 | Hold a partner review | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-010-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-010-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.11 Issue a notice on a missed target

#### A2.11.1 Intent

**Business objective.** Sends the contractual notice when a partner misses its targets, and starts the cure period.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Sends the contractual notice when a partner misses its targets, and starts the cure period.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Partner and agency manager | Opens the screen and issue a notice on a missed target | Checks the role, the capability area and the scope |
| 2 | Partner and agency manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal

**Prerequisites.** FEAT-PRM-08

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-011-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | No |
| partner.contract_end | Contract end date | date | No | None | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | No |
| partner_instruction.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| partner_instruction.partner_id | The partner this record belongs to | uuid | Yes | None | No |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| Partner and agency manager | Primary |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-011-01 | Issue a notice on a missed target | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-011-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-011-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.12 End a partner contract and recall the work

#### A2.12.1 Intent

**Business objective.** Closes the contract and pulls every open case back for re-selection.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Closes the contract and pulls every open case back for re-selection.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Partner and agency manager | Opens the screen and end a partner contract and recall the work | Checks the role, the capability area and the scope |
| 2 | Partner and agency manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal

**Prerequisites.** FEAT-PRM-11

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-012-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | No |
| partner.contract_end | Contract end date | date | No | None | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | No |
| partner_instruction.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| partner_instruction.partner_id | The partner this record belongs to | uuid | Yes | None | No |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| Partner and agency manager | Primary |
| Head of Litigation, Head of Asset Liquidity | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-012-01 | End a partner contract and recall the work | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-012-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-012-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.13 Check partner conduct

#### A2.13.1 Intent

**Business objective.** Samples partner contacts and complaints against the conduct rules and raises breaches.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Samples partner contacts and complaints against the conduct rules and raises breaches.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Check partner conduct | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal

**Prerequisites.** FEAT-PRM-08

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-013-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S9-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Conduct and QA officer | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-013-01 | Check partner conduct | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-013-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-013-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.14 Manage extra costs and services on an asset

#### A2.14.1 Intent

**Business objective.** Records and approves additional partner costs on a held asset.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Records and approves additional partner costs on a held asset.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Partner and agency manager | Opens the screen and manage extra costs and services on an asset | Checks the role, the capability area and the scope |
| 2 | Partner and agency manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal, AMIS

**Prerequisites.** FEAT-AST-07

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-014-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | No |
| partner.contract_end | Contract end date | date | No | None | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | No |
| partner_instruction.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| partner_instruction.partner_id | The partner this record belongs to | uuid | Yes | None | No |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| Partner and agency manager | Primary |
| NPA and asset manager | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-014-01 | Manage extra costs and services on an asset | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-014-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-014-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.15 Capture field work through the field app

#### A2.15.1 Intent

**Business objective.** Lets the field collector record visits, photos and bills against the case from the field.

**Problem.** Partners are instructed and paid by email and spreadsheet; allocation is not based on performance.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Lets the field collector record visits, photos and bills against the case from the field.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Field collector | Opens the screen and capture field work through the field app | Checks the role, the capability area and the scope |
| 2 | Field collector | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Field app, the Workbench document hub

**Prerequisites.** FEAT-DCM-21

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-015-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | No |
| partner.contract_end | Contract end date | date | No | None | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | No |
| partner_instruction.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| partner_instruction.partner_id | The partner this record belongs to | uuid | Yes | None | No |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| Field collector | Primary |
| Partner and agency manager | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S9-015-01 | Capture field work through the field app | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S9-015-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S9-015-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-S9-001 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit. | Must | E6 |
| REQ-S9-002 | Each partner type has one named owner. | Must | E6 |
| REQ-S9-003 | Work is allocated to partners by measured return against a scorecard, not by a fixed share. | Must | E6 |
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results. | Must | E6 |
| REQ-S9-005 | A partner that misses its service level is chased once and then has the work recalled. | Must | E7 |
| REQ-S9-006 | A partner panel exit, a declared conflict of interest, insolvency or an upheld conduct breach recalls every open case held by that partner. | Must | E7 |
| REQ-S9-007 | Partner performance, conduct and complaint data are reported to the partner review forum. | Must | E7 |
| REQ-S9-008 | Partners exchange data through the partner portal and the external gateway, and not by email. | Must | E6 |
| REQ-S9-009 | Field work and its evidence reach the case through the field application. | Should | E7 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-34 Partner list | Partners, contracts, panel status and scorecards | E2 identities; E6 full |
| SCR-35 Placement and allocation | Work placed with partners by rule, with recalls and re-selection | E6 |
| SCR-36 Partner scorecard | Monthly score per partner against its measures | E7 |
| PRT-01 Partner home | The partner's open instructions, due dates and messages | E2 |
| PRT-02 Instruction | One instruction with its documents, due dates and the result to record | E4 |
| PRT-03 Upload result | Record a result and upload its documents | E4 |
| PRT-04 Invoice | Submit a fee invoice against completed instructions | E6 |

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
| Partner | คู่ค้า | An outside firm the bank places work with |
| Collection agency | บริษัทติดตามหนี้ | A firm placed with accounts to collect |
| Law firm | สำนักงานกฎหมาย | A firm instructed to file and run lawsuits |
| Partner instruction | คำสั่งงานคู่ค้า | Work placed with a partner on a case |
| Partner portal | หน้าจอสำหรับคู่ค้า | The Workbench screens partners use for their placed cases |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
