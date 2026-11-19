<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6.zip!Recovery Workbench FSD S8 Deviation handling v3.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6.zip!Recovery Workbench FSD S8 Deviation handling v3.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S8 Deviation handling

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD S8 Deviation handling |
| Document ID | S8-RWB-FSD-v3 |
| Version | 3 |
| Status | In review |
| Classification | Confidential |
| Date | 15 November 2026 |
| Change note | v3, 15 November 2026: re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Constraint, freshness rule and trigger wording only. Everything else unchanged from v2. |
| FSD owner | Business analyst, S8 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| S8 | Deviation handling | E2 screening; E7 |

**Feature scope.** X1 to X7: screening, pause, handling, return.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification S8 Deviation handling | TSD | Pair |
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

**In scope.** X1 to X7: screening, pause, handling, return.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-AGT-08; FEAT-APD-07; FEAT-CWC-03; FEAT-CWC-12; FEAT-DVF-01; FEAT-DVH-01; FEAT-DVH-02; FEAT-DVH-04

**Constraints.** Built in the ACE service as part of the recovery module; source data read only from the ACE database through the SELECT-only `recovery.v_ace_*` views, landed by ACE's own ingestion, with no inbound load in the Workbench (D-RCV-35); every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| S8 | FEAT-DVH-01 | Flag a deviation X1 to X7 on the case | System | Raises the deviation flag with its code and reasons, from the screening agent or from an officer. | E2 | A2.1 |
| S8 | FEAT-DVH-02 | Pause the stage clock on a deviation | System | Stops the stage service level while the deviation is open, so the case is not counted as late. | E2 | A2.2 |
| S8 | FEAT-DVH-03 | Keep the prescription clock running during a deviation | System | Leaves the legal clock running while the stage clock is paused, because the law does not pause. | E2 | A2.3 |
| S8 | FEAT-DVH-04 | Route the deviation to the named owner | System | Sends each deviation code to the role that owns it: complaint officer, specialist, fraud team or Legal. | E2 | A2.4 |
| S8 | FEAT-DVH-05 | Apply a contact stop for X1 to X3 | System | Stops outbound contact on a disputed, vulnerable or deceased case, and holds it until the stop is lifted. | E2 | A2.5 |
| S8 | FEAT-DVH-06 | Clear a deviation and resume the timers | System | Records the outcome, lifts the stop and resumes the stage clock at the state the case paused in. | E2 | A2.6 |
| S8 | FEAT-DVH-07 | Screen for deviations with the agent at L1 on one segment | System | Runs the deviation screening agent live at autonomy level 1 on one segment, with its flags visible. | E2 | A2.7 |
| S8 | FEAT-DVH-08 | Review a flagged deviation below the confidence threshold | User | Puts a low-confidence flag in front of a person before it changes the case. | E2 | A2.8 |
| S8 | FEAT-DVH-09 | Handle two deviations on one case | System | Holds more than one open deviation on a case, each with its own owner, and resumes only when all are cleared. | E2 | A2.9 |
| S8 | FEAT-DVF-01 | Run X1 dispute and complaint end to end | User | Takes the dispute from detection through the evidence pack to resolution and the return point. | E7 | A2.10 |
| S8 | FEAT-DVF-02 | Run X2 vulnerability and hardship end to end | User | Takes the case to the specialist queue with contact limits, through to the hardship decision. | E7 | A2.11 |
| S8 | FEAT-DVF-03 | Run X3 deceased customer end to end | User | Stops contact, notifies heirs, files the insurance claim and settles the estate position. | E7 | A2.12 |
| S8 | FEAT-DVF-04 | Run X4 fraud end to end | User | Refers to the fraud team, tracks the investigation and routes the case on the outcome. | E7 | A2.13 |
| S8 | FEAT-DVF-05 | Run X5 bankruptcy and seizure end to end | User | Stops direct collection and files the claim with the receiver or the LED before the deadline. | E7 | A2.14 |
| S8 | FEAT-DVF-06 | Run X6 lost contact and skip trace end to end | System | Runs the skip trace through the bureau, internal data and agency sources and routes on the result. | E7 | A2.15 |
| S8 | FEAT-DVF-07 | Run X7 collateral event end to end | User | Files the insurance claim, re-appraises the collateral and returns the case to the route decision. | E7 | A2.16 |
| S8 | FEAT-DVF-08 | Review an override | User | Puts overrides in front of the review forum, with the reason and the outcome of each. | E7 | A2.17 |
| S8 | FEAT-DVF-09 | Match a complaint to the preceding contact | User | Links each complaint to the contact that caused it, which is how conduct is measured. | E7 | A2.18 |
| S8 | FEAT-DVF-10 | Handle a contact sent while a block is on | User | Opens the breach path when a message goes out against a contact stop. | E7 | A2.19 |

### A1.3 Background

Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Flag a deviation X1 to X7 on the case

#### A2.1.1 Intent

**Business objective.** Raises the deviation flag with its code and reasons, from the screening agent or from an officer.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Raises the deviation flag with its code and reasons, from the screening agent or from an officer.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Flag a deviation X1 to X7 on the case | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-03

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-001-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S8-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Conduct and QA officer, Case owner | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-001-01 | Shadow flags | 200 cases with their call notes and documents | the agent runs | each run stores its proposed codes with reasons and source references in mode "SHADOW" And no deviation record exists, deviation_open stays false on every case and no contact stop is set And no user-facing endpoint returns a proposal | RWB-E1-062 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-S8-001-01 | Compared | the business analysts' flags for the same 200 cases in sample "SCREEN-S1" version 1 | the comparison runs | one score row per code X1 to X7 holds precision, recall and sample size 200 And for X6 with 18 true positives, 2 false positives and 6 false negatives precision is 0.9000 and recall is 0.7500 | RWB-E1-062 |
| AC-ALT-S8-001-02 | A new document starts a run | open case "RW-2026-000401" receives a document of type "DEATH_CERTIFICATE" | EV-16 DocumentStored is processed | one shadow run exists with key "SCREENING:<caseId>:<eventId>" and trigger "DocumentStored" | RWB-E1-062 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-001-01 | A repeated event | EV-16 for document "D-1001" on case "RW-2026-000401" was processed | the same event ID arrives again | one run exists for the case and event and the repeat is counted (R-UNI-40) | RWB-E1-062 |
| AC-EXC-S8-001-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-001-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Pause the stage clock on a deviation

#### A2.2.1 Intent

**Business objective.** Stops the stage service level while the deviation is open, so the case is not counted as late.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Stops the stage service level while the deviation is open, so the case is not counted as late.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Pause the stage clock on a deviation | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Quartz scheduler

**Prerequisites.** FEAT-DVH-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-002-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-DEV-01 | Pause the stage clock, keep the prescription clock running, route to the named owner, when deviation_code in (X1..X7) | Moves to DEV_FLAGGED |
| R-DEV-18 | Resume the stage clock and return the case, when the event occurs | Moves to RESUMED |
| BR-S8-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-002-01 | Timers shown | case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF" | "U-CO-01" opens the case record | the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer" | RWB-E2-015 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-S8-002-01 | Deviation flag | case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true | "U-CO-01" opens the case record | the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date And the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped" | RWB-E2-015 |
| AC-ALT-S8-002-02 | Prescription | case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date | "U-CO-01" opens the case record | the prescription date 2027-02-13 shows with the warning MSG-P3-003 And for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows | RWB-E2-015 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-002-01 | No running timer | case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED" | "U-CO-01" opens the case record | the timers section shows MSG-P3-018 | RWB-E2-015 |
| AC-EXC-S8-002-02 | Deviation module does not answer | the deviation query does not answer within 2 seconds for case "RW-2026-000502" | "U-CO-01" opens the case record | the timers and the prescription date show And the deviation section shows MSG-GEN-006 naming "Deviation handling" And the on hold banner shows from the case's deviation flag | RWB-E2-015 |
| AC-EXC-S8-002-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-002-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Keep the prescription clock running during a deviation

#### A2.3.1 Intent

**Business objective.** Leaves the legal clock running while the stage clock is paused, because the law does not pause.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Leaves the legal clock running while the stage clock is paused, because the law does not pause.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Keep the prescription clock running during a deviation | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Quartz scheduler

**Prerequisites.** FEAT-CWC-12

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-003-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-DEV-01 | Pause the stage clock, keep the prescription clock running, route to the named owner, when deviation_code in (X1..X7) | Moves to DEV_FLAGGED |
| R-DEV-08 | Return the case to the state it paused in, when the event occurs | Moves to RESUMED |
| R-DEV-18 | Resume the stage clock and return the case, when the event occurs | Moves to RESUMED |
| BR-S8-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Legal counsel | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-003-01 | Timers shown | case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF" | "U-CO-01" opens the case record | the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer" | RWB-E2-015 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-S8-003-01 | Deviation flag | case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true | "U-CO-01" opens the case record | the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date And the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped" | RWB-E2-015 |
| AC-ALT-S8-003-02 | Prescription | case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date | "U-CO-01" opens the case record | the prescription date 2027-02-13 shows with the warning MSG-P3-003 And for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows | RWB-E2-015 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-003-01 | No running timer | case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED" | "U-CO-01" opens the case record | the timers section shows MSG-P3-018 | RWB-E2-015 |
| AC-EXC-S8-003-02 | Deviation module does not answer | the deviation query does not answer within 2 seconds for case "RW-2026-000502" | "U-CO-01" opens the case record | the timers and the prescription date show And the deviation section shows MSG-GEN-006 naming "Deviation handling" And the on hold banner shows from the case's deviation flag | RWB-E2-015 |
| AC-EXC-S8-003-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-003-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Route the deviation to the named owner

#### A2.4.1 Intent

**Business objective.** Sends each deviation code to the role that owns it: complaint officer, specialist, fraud team or Legal.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Sends each deviation code to the role that owns it: complaint officer, specialist, fraud team or Legal.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Route the deviation to the named owner | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Rules component

**Prerequisites.** FEAT-DVH-01

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-004-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-DEV-01 | Pause the stage clock, keep the prescription clock running, route to the named owner, when deviation_code in (X1..X7) | Moves to DEV_FLAGGED |
| R-DEV-02 | Assign to the complaint officer, when deviation_code = X1 | Moves to DEV_WITH_OWNER |
| R-DEV-03 | Assign to the specialist; Legal joins X3 for the estate claim, when deviation_code in (X2,X3) | Moves to DEV_WITH_OWNER |
| BR-S8-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Complaint officer, Hardship and vulnerability specialist, Fraud investigator, Legal counsel | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-004-01 | Shadow flags | 200 cases with their call notes and documents | the agent runs | each run stores its proposed codes with reasons and source references in mode "SHADOW" And no deviation record exists, deviation_open stays false on every case and no contact stop is set And no user-facing endpoint returns a proposal | RWB-E1-062 |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-S8-004-01 | Compared | the business analysts' flags for the same 200 cases in sample "SCREEN-S1" version 1 | the comparison runs | one score row per code X1 to X7 holds precision, recall and sample size 200 And for X6 with 18 true positives, 2 false positives and 6 false negatives precision is 0.9000 and recall is 0.7500 | RWB-E1-062 |
| AC-ALT-S8-004-02 | A new document starts a run | open case "RW-2026-000401" receives a document of type "DEATH_CERTIFICATE" | EV-16 DocumentStored is processed | one shadow run exists with key "SCREENING:<caseId>:<eventId>" and trigger "DocumentStored" | RWB-E1-062 |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-004-01 | A repeated event | EV-16 for document "D-1001" on case "RW-2026-000401" was processed | the same event ID arrives again | one run exists for the case and event and the repeat is counted (R-UNI-40) | RWB-E1-062 |
| AC-EXC-S8-004-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-004-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Apply a contact stop for X1 to X3

#### A2.5.1 Intent

**Business objective.** Stops outbound contact on a disputed, vulnerable or deceased case, and holds it until the stop is lifted.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Stops outbound contact on a disputed, vulnerable or deceased case, and holds it until the stop is lifted.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Apply a contact stop for X1 to X3 | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DVH-01

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-005-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S8-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Conduct and QA officer, Complaint officer | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-005-01 | Timers shown | case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF" | "U-CO-01" opens the case record | the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer" | RWB-E2-015 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-S8-005-01 | Deviation flag | case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true | "U-CO-01" opens the case record | the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date And the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped" | RWB-E2-015 |
| AC-ALT-S8-005-02 | Prescription | case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date | "U-CO-01" opens the case record | the prescription date 2027-02-13 shows with the warning MSG-P3-003 And for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows | RWB-E2-015 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-005-01 | No running timer | case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED" | "U-CO-01" opens the case record | the timers section shows MSG-P3-018 | RWB-E2-015 |
| AC-EXC-S8-005-02 | Deviation module does not answer | the deviation query does not answer within 2 seconds for case "RW-2026-000502" | "U-CO-01" opens the case record | the timers and the prescription date show And the deviation section shows MSG-GEN-006 naming "Deviation handling" And the on hold banner shows from the case's deviation flag | RWB-E2-015 |
| AC-EXC-S8-005-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-005-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Clear a deviation and resume the timers

#### A2.6.1 Intent

**Business objective.** Records the outcome, lifts the stop and resumes the stage clock at the state the case paused in.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Records the outcome, lifts the stop and resumes the stage clock at the state the case paused in.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Clear a deviation and resume the timers | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Quartz scheduler

**Prerequisites.** FEAT-DVH-02

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-006-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-DEV-01 | Pause the stage clock, keep the prescription clock running, route to the named owner, when deviation_code in (X1..X7) | Moves to DEV_FLAGGED |
| R-DEV-07 | Clear the flag, record the reason, resume the clock, when owner marks the flag as not a deviation | Moves to DEV_REJECTED |
| R-DEV-08 | Return the case to the state it paused in, when the event occurs | Moves to RESUMED |
| BR-S8-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-006-01 | Timers shown | case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF" | "U-CO-01" opens the case record | the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer" | RWB-E2-015 |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-S8-006-01 | Deviation flag | case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true | "U-CO-01" opens the case record | the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date And the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped" | RWB-E2-015 |
| AC-ALT-S8-006-02 | Prescription | case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date | "U-CO-01" opens the case record | the prescription date 2027-02-13 shows with the warning MSG-P3-003 And for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows | RWB-E2-015 |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-006-01 | No running timer | case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED" | "U-CO-01" opens the case record | the timers section shows MSG-P3-018 | RWB-E2-015 |
| AC-EXC-S8-006-02 | Deviation module does not answer | the deviation query does not answer within 2 seconds for case "RW-2026-000502" | "U-CO-01" opens the case record | the timers and the prescription date show And the deviation section shows MSG-GEN-006 naming "Deviation handling" And the on hold banner shows from the case's deviation flag | RWB-E2-015 |
| AC-EXC-S8-006-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-006-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Screen for deviations with the agent at L1 on one segment

#### A2.7.1 Intent

**Business objective.** Runs the deviation screening agent live at autonomy level 1 on one segment, with its flags visible.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Runs the deviation screening agent live at autonomy level 1 on one segment, with its flags visible.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Screen for deviations with the agent at L1 on one segment | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Model gateway

**Prerequisites.** FEAT-AGT-08

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-007-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S8-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Conduct and QA officer | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-007-01 | Evaluation | the shadow run on 500 cases in sample "SCREEN-S2" version 1 | the evaluation runs | precision and recall per flag X1 to X7 are stored with sample size 500 And for X1 with 41 true positives, 4 false positives and 5 false negatives precision is 0.9111 and recall is 0.8913 And the L1 proposal is recorded as policy "SCREENING" version "P2" with status "LOADED", segment MORTGAGE and BKK and the evaluation run ID | RWB-E2-029 |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-S8-007-01 | L1 on one segment | Mortgage case "RW-2027-000801" in region BKK and a complaint note on 2027-01-26 | the agent runs | the panel "Proposed deviations" shows X1 with its reasons, the preceding contact and the marker "Agent output" And when the owner confirms X1 the S8 service raises deviation X1 with raised_by "SCREENING_AGENT" under rule R-DEV-01 And the case status becomes "On hold" and agent_feedback holds verdict "ACCEPTED" for item "X1" with the S8 decision log entry ID | RWB-E2-029 |
| AC-ALT-S8-007-02 | Other segments | hire purchase case "RW-2027-000802" in region BKK | the agent runs | the result stays in shadow and GET /cases/{caseId}/agent-outputs returns no screening output | RWB-E2-029 |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-007-01 | The rejection cannot be recorded | the decision log writer fails | the owner rejects X6 with a reason | the request is refused with 503 and MSG-P7-003 and no agent_feedback row exists | RWB-E2-029 |
| AC-EXC-S8-007-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-007-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 Review a flagged deviation below the confidence threshold

#### A2.8.1 Intent

**Business objective.** Puts a low-confidence flag in front of a person before it changes the case.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Puts a low-confidence flag in front of a person before it changes the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Conduct and QA officer | Opens the screen and review a flagged deviation below the confidence threshold | Checks the role, the capability area and the scope |
| 2 | Conduct and QA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-DVH-07

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-008-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DEV-01 | Pause the stage clock, keep the prescription clock running, route to the named owner, when deviation_code in (X1..X7) | Moves to DEV_FLAGGED |
| BR-S8-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| deviation.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | No |
| deviation.handler_user_id | The named handler | uuid | No | None | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | No |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| Conduct and QA officer | Primary |
| Case owner | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-008-01 | Shadow flags | 200 cases with their call notes and documents | the agent runs | each run stores its proposed codes with reasons and source references in mode "SHADOW" And no deviation record exists, deviation_open stays false on every case and no contact stop is set And no user-facing endpoint returns a proposal | RWB-E1-062 |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-S8-008-01 | Compared | the business analysts' flags for the same 200 cases in sample "SCREEN-S1" version 1 | the comparison runs | one score row per code X1 to X7 holds precision, recall and sample size 200 And for X6 with 18 true positives, 2 false positives and 6 false negatives precision is 0.9000 and recall is 0.7500 | RWB-E1-062 |
| AC-ALT-S8-008-02 | A new document starts a run | open case "RW-2026-000401" receives a document of type "DEATH_CERTIFICATE" | EV-16 DocumentStored is processed | one shadow run exists with key "SCREENING:<caseId>:<eventId>" and trigger "DocumentStored" | RWB-E1-062 |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-008-01 | A repeated event | EV-16 for document "D-1001" on case "RW-2026-000401" was processed | the same event ID arrives again | one run exists for the case and event and the repeat is counted (R-UNI-40) | RWB-E1-062 |
| AC-EXC-S8-008-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-008-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.9 Handle two deviations on one case

#### A2.9.1 Intent

**Business objective.** Holds more than one open deviation on a case, each with its own owner, and resumes only when all are cleared.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Holds more than one open deviation on a case, each with its own owner, and resumes only when all are cleared.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Handle two deviations on one case | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DVH-06

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-009-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-DEV-01 | Pause the stage clock, keep the prescription clock running, route to the named owner, when deviation_code in (X1..X7) | Moves to DEV_FLAGGED |
| R-DEV-09 | Record the outcome; the same decision resumes, when deviation_code in (X1,X7) | Moves to DEV_RESOLVED |
| BR-S8-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-009-01 | Timers shown | case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF" | "U-CO-01" opens the case record | the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer" | RWB-E2-015 |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-S8-009-01 | Deviation flag | case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true | "U-CO-01" opens the case record | the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date And the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped" | RWB-E2-015 |
| AC-ALT-S8-009-02 | Prescription | case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date | "U-CO-01" opens the case record | the prescription date 2027-02-13 shows with the warning MSG-P3-003 And for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows | RWB-E2-015 |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-009-01 | No running timer | case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED" | "U-CO-01" opens the case record | the timers section shows MSG-P3-018 | RWB-E2-015 |
| AC-EXC-S8-009-02 | Deviation module does not answer | the deviation query does not answer within 2 seconds for case "RW-2026-000502" | "U-CO-01" opens the case record | the timers and the prescription date show And the deviation section shows MSG-GEN-006 naming "Deviation handling" And the on hold banner shows from the case's deviation flag | RWB-E2-015 |
| AC-EXC-S8-009-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-009-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.10 Run X1 dispute and complaint end to end

#### A2.10.1 Intent

**Business objective.** Takes the dispute from detection through the evidence pack to resolution and the return point.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Takes the dispute from detection through the evidence pack to resolution and the return point.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Complaint officer | Opens the screen and run X1 dispute and complaint end to end | Checks the role, the capability area and the scope |
| 2 | Complaint officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, Document hub

**Prerequisites.** FEAT-DVH-04

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-010-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S8-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| deviation.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | No |
| deviation.handler_user_id | The named handler | uuid | No | None | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | No |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| Complaint officer | Primary |
| Conduct and QA officer | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-010-01 | Run X1 dispute and complaint end to end | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-010-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-010-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.11 Run X2 vulnerability and hardship end to end

#### A2.11.1 Intent

**Business objective.** Takes the case to the specialist queue with contact limits, through to the hardship decision.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Takes the case to the specialist queue with contact limits, through to the hardship decision.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Hardship and vulnerability specialist | Opens the screen and run X2 vulnerability and hardship end to end | Checks the role, the capability area and the scope |
| 2 | Hardship and vulnerability specialist | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, EFS

**Prerequisites.** FEAT-DVH-04

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-011-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DEV-17 | Route to escalation or to the route decision, when deviation_code = X6 and skip trace exhausted | Moves to DEV_REROUTE |
| BR-S8-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| deviation.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | No |
| deviation.handler_user_id | The named handler | uuid | No | None | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | No |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| Hardship and vulnerability specialist | Primary |
| Conduct and QA officer | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-011-01 | Run X2 vulnerability and hardship end to end | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-011-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-011-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.12 Run X3 deceased customer end to end

#### A2.12.1 Intent

**Business objective.** Stops contact, notifies heirs, files the insurance claim and settles the estate position.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Stops contact, notifies heirs, files the insurance claim and settles the estate position.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Hardship and vulnerability specialist | Opens the screen and run X3 deceased customer end to end | Checks the role, the capability area and the scope |
| 2 | Hardship and vulnerability specialist | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, the Workbench document hub

**Prerequisites.** FEAT-DVH-04

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-012-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DEV-03 | Assign to the specialist; Legal joins X3 for the estate claim, when deviation_code in (X2,X3) | Moves to DEV_WITH_OWNER |
| R-DEV-06 | Agent handles within policy; a person approves an insurance claim, when deviation_code in (X6,X7) | Moves to DEV_WITH_OWNER |
| BR-S8-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| deviation.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | No |
| deviation.handler_user_id | The named handler | uuid | No | None | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | No |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| Hardship and vulnerability specialist | Primary |
| Legal counsel | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-012-01 | Run X3 deceased customer end to end | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-012-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-012-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.13 Run X4 fraud end to end

#### A2.13.1 Intent

**Business objective.** Refers to the fraud team, tracks the investigation and routes the case on the outcome.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Refers to the fraud team, tracks the investigation and routes the case on the outcome.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Fraud investigator | Opens the screen and run X4 fraud end to end | Checks the role, the capability area and the scope |
| 2 | Fraud investigator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Aric, Workbench

**Prerequisites.** FEAT-DVH-04

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-013-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S8-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| deviation.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | No |
| deviation.handler_user_id | The named handler | uuid | No | None | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | No |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| Fraud investigator | Primary |
| Case owner | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-013-01 | Run X4 fraud end to end | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-013-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-013-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.14 Run X5 bankruptcy and seizure end to end

#### A2.14.1 Intent

**Business objective.** Stops direct collection and files the claim with the receiver or the LED before the deadline.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Stops direct collection and files the claim with the receiver or the LED before the deadline.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Legal counsel | Opens the screen and run X5 bankruptcy and seizure end to end | Checks the role, the capability area and the scope |
| 2 | Legal counsel | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** LIT, Workbench

**Prerequisites.** FEAT-DVH-04

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-014-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DEV-05 | Assign to Legal; file with the official receiver or the LED before the deadline, when deviation_code = X5 | Moves to DEV_WITH_OWNER |
| R-DEV-15 | Route to litigation, then to write-off after the receiver reports, when deviation_code = X5 | Moves to DEV_REROUTE |
| BR-S8-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| deviation.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | No |
| deviation.handler_user_id | The named handler | uuid | No | None | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | No |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| Legal counsel | Primary |
| Enforcement owner | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-014-01 | Run X5 bankruptcy and seizure end to end | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-014-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-014-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.15 Run X6 lost contact and skip trace end to end

#### A2.15.1 Intent

**Business objective.** Runs the skip trace through the bureau, internal data and agency sources and routes on the result.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Runs the skip trace through the bureau, internal data and agency sources and routes on the result.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run X6 lost contact and skip trace end to end | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** NCB, EFS, Partner portal

**Prerequisites.** FEAT-DVF-01

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-015-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S8-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-015-01 | Run X6 lost contact and skip trace end to end | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-015-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-015-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.16 Run X7 collateral event end to end

#### A2.16.1 Intent

**Business objective.** Files the insurance claim, re-appraises the collateral and returns the case to the route decision.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Files the insurance claim, re-appraises the collateral and returns the case to the route decision.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and run X7 collateral event end to end | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** SVAF, Workbench

**Prerequisites.** FEAT-GUA-08

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-016-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DEV-06 | Agent handles within policy; a person approves an insurance claim, when deviation_code in (X6,X7) | Moves to DEV_WITH_OWNER |
| R-DEV-12 | Return to the route decision against the estate, when deviation_code = X3 and insurance does not clear | Moves to DEV_REROUTE |
| R-DEV-17 | Route to escalation or to the route decision, when deviation_code = X6 and skip trace exhausted | Moves to DEV_REROUTE |
| BR-S8-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| deviation.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | No |
| deviation.handler_user_id | The named handler | uuid | No | None | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Hardship and vulnerability specialist | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-016-01 | Run X7 collateral event end to end | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-016-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-016-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.17 Review an override

#### A2.17.1 Intent

**Business objective.** Puts overrides in front of the review forum, with the reason and the outcome of each.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.17.2 Description

**Functional overview.** Puts overrides in front of the review forum, with the reason and the outcome of each.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Risk and model risk officer | Opens the screen and review an override | Checks the role, the capability area and the scope |
| 2 | Risk and model risk officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-07

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-017-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S8-017 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.17.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| deviation.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | No |
| deviation.handler_user_id | The named handler | uuid | No | None | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | No |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| Risk and model risk officer | Primary |
| Conduct and QA officer, Center of excellence analyst | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-017-01 | Review an override | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-017-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-017-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.18 Match a complaint to the preceding contact

#### A2.18.1 Intent

**Business objective.** Links each complaint to the contact that caused it, which is how conduct is measured.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.18.2 Description

**Functional overview.** Links each complaint to the contact that caused it, which is how conduct is measured.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Conduct and QA officer | Opens the screen and match a complaint to the preceding contact | Checks the role, the capability area and the scope |
| 2 | Conduct and QA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, EFS

**Prerequisites.** FEAT-OCC-05

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-018-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S8-018 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.18.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| deviation.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | No |
| deviation.handler_user_id | The named handler | uuid | No | None | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | No |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| Conduct and QA officer | Primary |
| Complaint officer | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-018-01 | Match a complaint to the preceding contact | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-018-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-018-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.19 Handle a contact sent while a block is on

#### A2.19.1 Intent

**Business objective.** Opens the breach path when a message goes out against a contact stop.

**Problem.** Complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly |

#### A2.19.2 Description

**Functional overview.** Opens the breach path when a message goes out against a contact stop.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Conduct and QA officer | Opens the screen and handle a contact sent while a block is on | Checks the role, the capability area and the scope |
| 2 | Conduct and QA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-OCC-06

#### A2.19.3 Business rules and structure

##### A2.19.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S8-019-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S8-019 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.19.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| deviation.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | No |
| deviation.handler_user_id | The named handler | uuid | No | None | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | No |

##### A2.19.3.3 Roles and permissions

| Role | Use |
|---|---|
| Conduct and QA officer | Primary |
| Compliance and PDPA officer | Also uses |

#### A2.19.4 Acceptance criteria

##### A2.19.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S8-019-01 | Handle a contact sent while a block is on | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.19.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.19.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S8-019-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S8-019-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.19.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-DVH-001 | Deviations X1 to X7 are detected by rule from case data, call notes, documents and external flags. | Must | E2 |
| REQ-DVH-002 | A deviation pauses the stage clock, keeps the prescription clock running, and does not replace the case state. | Must | E2 |
| REQ-DVH-003 | Each deviation code routes to its named owner, and a code with no owner routes to the team manager and is recorded as unmapped. | Must | E2 |
| REQ-DVH-004 | Contact stops apply automatically for a dispute or complaint, a vulnerable or hardship case, and a deceased customer. | Must | E2 |
| REQ-DVH-005 | A resolved deviation returns the case to the state it paused in, or to the route decision where the outcome changes the route. | Must | E2 |
| REQ-DVH-006 | A deviation flag is visible on the case record view and in every queue view. | Must | E2 |
| REQ-DVH-007 | A complaint is matched to the contact that preceded it. | Must | E2 |
| REQ-DVH-008 | A death stops all contact, notifies the heirs and the estate, and starts the insurance claim path. | Must | E3 |
| REQ-DVH-009 | A bankruptcy or external seizure stops direct collection and starts the claim deadline clock. | Must | E2 |
| REQ-DVH-010 | A fraud flag refers the case to the fraud team and holds recovery action until it is confirmed or cleared. | Must | E2 |
| REQ-DVH-011 | The full deviation flows with their approvers, contact stops and return points run end to end. | Must | E7 |
| REQ-S8-001 | Each of X1 to X7 runs end to end with its own flow, approver, contact rules and return point. | Must | E7 |
| REQ-S8-002 | A hardship or vulnerability case follows the contact limits set for it and reaches a hardship or relief decision. | Must | E7 |
| REQ-S8-003 | A complaint is resolved inside its service level and the case returns to the same decision with its timers resumed. | Must | E7 |
| REQ-S8-004 | A lost contact case runs skip tracing and returns to a decision whether or not contact is restored. | Must | E7 |
| REQ-S8-005 | A collateral event triggers an insurance claim and a re-appraisal before the next decision. | Must | E7 |
| REQ-S8-006 | Override and deviation patterns are reviewed monthly by the center of excellence. | Must | E7 |
| REQ-S8-007 | A data subject request holds automated processing on the case and routes to Compliance inside the statutory period. | Must | E7 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-06 Raise deviation | Raise X1 to X7 on a case with the reason and the evidence | E2 |
| SCR-08 Deviation queue | Open deviations by type, handler and age | E2 |

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
| Deviation | เหตุผิดปกติ | An event that stops the normal route: X1 to X7 |
| Contact stop | การระงับการติดต่อลูกหนี้ | An instruction that no one contacts the customer while it is in force |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
