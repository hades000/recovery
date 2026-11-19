<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6.zip!Recovery Workbench FSD S4 Litigation and enforcement v3.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6.zip!Recovery Workbench FSD S4 Litigation and enforcement v3.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S4 Litigation and enforcement

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD S4 Litigation and enforcement |
| Document ID | S4-RWB-FSD-v3 |
| Version | 3 |
| Status | In review |
| Classification | Confidential |
| Date | 15 November 2026 |
| Change note | v3, 15 November 2026: re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Constraint, freshness rule and trigger wording only; legal_action mirrored LIT fields left for DEF-05. Everything else unchanged from v2. |
| FSD owner | Business analyst, S4 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| S4 | Litigation and enforcement | E2 notices; E5 |

**Feature scope.** Notices, law firm instruction, hearings, judgment, enforcement.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification S4 Litigation and enforcement | TSD | Pair |
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

**In scope.** Notices, law firm instruction, hearings, judgment, enforcement.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-AGT-01; FEAT-APD-01; FEAT-CWC-11; FEAT-DCM-02; FEAT-DRI-14; FEAT-DRI-17; FEAT-LIT-04, FEAT-DCM-16; FEAT-LIT-05

**Constraints.** Built in the ACE service as part of the recovery module; source data read only from the ACE database through the SELECT-only `recovery.v_ace_*` views, landed by ACE's own ingestion, with no inbound load in the Workbench (D-RCV-35); every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| S4 | FEAT-LIT-01 | Issue demand and recall notices | System | Produces and sends the statutory notices by rule, with no person in the path. | E5 | A2.1 |
| S4 | FEAT-LIT-02 | Record proof of delivery on a notice | System | Writes the delivery confirmation onto the case, which the notice period timer starts from. | E5 | A2.2 |
| S4 | FEAT-LIT-03 | Run the notice period timer | System | Starts and tracks the statutory notice period and raises it when it expires. | E5 | A2.3 |
| S4 | FEAT-LIT-04 | Assemble the litigation pack | System | Builds the pack from the document index and the case facts, ready for the officer to verify. | E5 | A2.4 |
| S4 | FEAT-LIT-05 | Check the pack against the defect list | System | Tests the pack against the known defect list and names what is missing. | E5 | A2.5 |
| S4 | FEAT-LIT-06 | Recover a missing or lost document | User | Opens the recovery path for a document the pack needs and the bank cannot find. | E5 | A2.6 |
| S4 | FEAT-LIT-07 | Verify the pack and approve filing | User | Lets the litigation officer confirm the pack and authorize the filing. | E5 | A2.7 |
| S4 | FEAT-LIT-08 | Select the law firm from the panel | System | Picks the firm by the panel rule: scorecard, capacity, court and conflict. | E5 | A2.8 |
| S4 | FEAT-LIT-09 | Instruct the firm through the portal | System | Sends the instruction and the pack to the firm and starts the partner clock. | E5 | A2.9 |
| S4 | FEAT-LIT-10 | Record the court filing and receipt | User | Takes the filing confirmation and the court case number from the firm onto the case. | E5 | A2.10 |
| S4 | FEAT-LIT-11 | Track hearings, deadlines and fees | System | Follows the court calendar, raises each deadline and accrues the fees against the case. | E5 | A2.11 |
| S4 | FEAT-LIT-12 | Recommend the next litigation step | System | Proposes the next step with reasons, for the officer or the approver to decide. | E5 | A2.12 |
| S4 | FEAT-LIT-13 | Settle before judgment | User | Takes a settlement during the case to the approver named by the limit, and books it if approved. | E5 | A2.13 |
| S4 | FEAT-LIT-14 | Decide and manage an appeal | User | Records the appeal decision, the grounds and the approval, and tracks it to its end. | E5 | A2.14 |
| S4 | FEAT-LIT-15 | Pay court fees and legal expenses | System | Checks the fee against the schedule, routes it for approval where needed and pays it. | E5 | A2.15 |
| S4 | FEAT-LIT-16 | Record the judgment | System | Writes the judgment date and amount onto the case and opens the enforcement step. | E5 | A2.16 |
| S4 | FEAT-LIT-17 | Trace assets for enforcement | System | Searches the bureau, registries and insurers for assets to enforce against, and reports what it finds. | E5 | A2.17 |
| S4 | FEAT-LIT-18 | Apply for the writ and seizure | User | Instructs the writ and the seizure through the firm and tracks it to execution. | E5 | A2.18 |
| S4 | FEAT-LIT-19 | Follow the LED auction ladder | System | Tracks the enforcement auction through the 100, 90, 80 and 70 percent steps of official value. | E5 | A2.19 |
| S4 | FEAT-LIT-20 | Record an enforcement deferral with its reason | User | Lets the enforcement owner defer with a coded reason and a review date. Enforcement after judgment has no owner today. | E5 | A2.20 |
| S4 | FEAT-LIT-21 | File a bankruptcy petition | User | Takes the petition to the approver and files it through the firm. | E5 | A2.21 |
| S4 | FEAT-LIT-22 | Match enforcement proceeds to the case | System | Matches money from the LED or the firm to the case and applies it to the balance. | E5 | A2.22 |

### A1.3 Background

Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Issue demand and recall notices

#### A2.1.1 Intent

**Business objective.** Produces and sends the statutory notices by rule, with no person in the path.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Produces and sends the statutory notices by rule, with no person in the path.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Issue demand and recall notices | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** WIN, Workbench

**Prerequisites.** FEAT-DRI-14

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-001-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-03 | Generate the demand and recall notices from the Legal-approved template, when template_status = current for product and notice_type | Moves to NOTICE_DISPATCHED |
| BR-S4-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-001-01 | Issue demand and recall notices | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-001-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-001-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Record proof of delivery on a notice

#### A2.2.1 Intent

**Business objective.** Writes the delivery confirmation onto the case, which the notice period timer starts from.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Writes the delivery confirmation onto the case, which the notice period timer starts from.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Record proof of delivery on a notice | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** WIN

**Prerequisites.** FEAT-DRI-17

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-002-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-07 | Attach the proof and start the notice period from delivered_at, when served_result = delivered | Moves to WITH_CUSTOMER_NOTICE_PERIOD |
| R-LIT-08 | Mark the notice unserved; the notice period does not start, when no proof returned inside the proof window | Moves to NOTICE_UNSERVED |
| R-LIT-09 | Record the result and queue an alternate service method, when served_result in (refused, returned, undeliverable) | Moves to NOTICE_UNSERVED |
| BR-S4-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-002-01 | Record proof of delivery on a notice | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-002-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-002-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Run the notice period timer

#### A2.3.1 Intent

**Business objective.** Starts and tracks the statutory notice period and raises it when it expires.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Starts and tracks the statutory notice period and raises it when it expires.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the notice period timer | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Quartz scheduler

**Prerequisites.** FEAT-CWC-11

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-003-1 | Prescription date near | MSG-S4-002 The claim on this case expires on {date}. File before then. |
| R-LIT-07 | Attach the proof and start the notice period from delivered_at, when served_result = delivered | Moves to WITH_CUSTOMER_NOTICE_PERIOD |
| R-LIT-08 | Mark the notice unserved; the notice period does not start, when no proof returned inside the proof window | Moves to NOTICE_UNSERVED |
| R-LIT-15 | Open pack assembly, when no cure and no dispute at period_expires_at | Moves to PACK_ASSEMBLY |
| BR-S4-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-003-01 | Run the notice period timer | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-003-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-003-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Assemble the litigation pack

#### A2.4.1 Intent

**Business objective.** Builds the pack from the document index and the case facts, ready for the officer to verify.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Builds the pack from the document index and the case facts, ready for the officer to verify.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Assemble the litigation pack | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, the Workbench document hub, CCMS

**Prerequisites.** FEAT-DCM-02

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-004-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-04 | Hold generation and raise a task to the litigation officer, when template_status = withdrawn | Moves to NOTICE_BLOCKED |
| R-LIT-16 | Present the pack to the litigation officer for verification, when every defect list item present | Moves to PACK_VERIFIED |
| R-LIT-21 | Return the pack to the legal document agent for rework, when the officer rejects the pack at verification | Moves to PACK_ASSEMBLY |
| BR-S4-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-004-01 | Assemble the litigation pack | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-004-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-004-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Check the pack against the defect list

#### A2.5.1 Intent

**Business objective.** Tests the pack against the known defect list and names what is missing.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Tests the pack against the known defect list and names what is missing.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Check the pack against the defect list | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-LIT-04, FEAT-DCM-16

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-005-1 | Pack incomplete at filing | MSG-S4-001 The pack is missing {item}. Add it before filing. |
| R-LIT-18 | Re-run the defect list check, when missing items supplied, re-signed or re-created | Moves to PACK_ASSEMBLY |
| R-LIT-32 | Re-run the defect list check and re-file, when the defect is corrected | Moves to PACK_ASSEMBLY |
| BR-S4-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-005-01 | Check the pack against the defect list | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-005-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-005-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Recover a missing or lost document

#### A2.6.1 Intent

**Business objective.** Opens the recovery path for a document the pack needs and the bank cannot find.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Opens the recovery path for a document the pack needs and the bank cannot find.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Litigation officer | Opens the screen and recover a missing or lost document | Checks the role, the capability area and the scope |
| 2 | Litigation officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** the Workbench document hub, CCMS

**Prerequisites.** FEAT-LIT-05

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-006-1 | Pack incomplete at filing | MSG-S4-001 The pack is missing {item}. Add it before filing. |
| VR-S4-006-2 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| BR-S4-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| legal_action.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| legal_action.law_firm_id | The law firm instructed | uuid | No | None | No |
| legal_action.action_type | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction | varchar(20) | Yes | LOV-LEGAL-TYPE | No |
| legal_action.lawsuit_no | Lawsuit reference in LIT | varchar(30) | No | None | No |
| legal_action.black_case_no | Court black case number | varchar(30) | No | None | No |
| legal_action.red_case_no | Court red case number after judgment | varchar(30) | No | None | No |
| legal_action.court_name | Court | varchar(120) | No | None | No |
| legal_action.claim_amount | Amount sued for, baht | numeric(18,2) | No | None | No |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| Litigation officer | Primary |
| Legal counsel | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-006-01 | Recover a missing or lost document | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-006-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-006-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Verify the pack and approve filing

#### A2.7.1 Intent

**Business objective.** Lets the litigation officer confirm the pack and authorize the filing.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Lets the litigation officer confirm the pack and authorize the filing.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Litigation officer | Opens the screen and verify the pack and approve filing | Checks the role, the capability area and the scope |
| 2 | Litigation officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-LIT-05

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-007-1 | Pack incomplete at filing | MSG-S4-001 The pack is missing {item}. Add it before filing. |
| R-LIT-04 | Hold generation and raise a task to the litigation officer, when template_status = withdrawn | Moves to NOTICE_BLOCKED |
| R-LIT-11 | Head of Litigation approves substituted service or filing where the law allows, when prescription_days_remaining <= 90 | Moves to PACK_ASSEMBLY |
| R-LIT-16 | Present the pack to the litigation officer for verification, when every defect list item present | Moves to PACK_VERIFIED |
| BR-S4-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| legal_action.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| legal_action.law_firm_id | The law firm instructed | uuid | No | None | No |
| legal_action.action_type | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction | varchar(20) | Yes | LOV-LEGAL-TYPE | No |
| legal_action.lawsuit_no | Lawsuit reference in LIT | varchar(30) | No | None | No |
| legal_action.black_case_no | Court black case number | varchar(30) | No | None | No |
| legal_action.red_case_no | Court red case number after judgment | varchar(30) | No | None | No |
| legal_action.court_name | Court | varchar(120) | No | None | No |
| legal_action.claim_amount | Amount sued for, baht | numeric(18,2) | No | None | No |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| Litigation officer | Primary |
| Head of Litigation | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-007-01 | Verify the pack and approve filing | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-007-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-007-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 Select the law firm from the panel

#### A2.8.1 Intent

**Business objective.** Picks the firm by the panel rule: scorecard, capacity, court and conflict.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Picks the firm by the panel rule: scorecard, capacity, court and conflict.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Select the law firm from the panel | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Rules component

**Prerequisites.** FEAT-PRM-02

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-008-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-23 | Select the law firm by rule from the panel, when pack_verified_at set | Moves to FIRM_SELECTION |
| R-LIT-27 | Record the decline and re-select the next firm on the scorecard, when the firm declines, or does not accept inside the window | Moves to FIRM_DECLINED |
| BR-S4-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-008-01 | Select the law firm from the panel | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-008-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-008-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.9 Instruct the firm through the portal

#### A2.9.1 Intent

**Business objective.** Sends the instruction and the pack to the firm and starts the partner clock.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Sends the instruction and the pack to the firm and starts the partner clock.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Instruct the firm through the portal | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal, LIT

**Prerequisites.** FEAT-LIT-08

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-009-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-24 | Issue the instruction with the pack through the portal, when panel firm covers the court region and case type and passes the conflict check | Moves to FIRM_INSTRUCTED |
| R-LIT-26 | Issue the instruction with the pack through the portal, when the Head of Litigation nominates a firm or widens the panel | Moves to FIRM_INSTRUCTED |
| R-LIT-28 | Mark the instruction breached, notify the partner manager and re-select, when the instruction is past due with no filing | Moves to FIRM_DECLINED |
| BR-S4-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-009-01 | Instruct the firm through the portal | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-009-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-009-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.10 Record the court filing and receipt

#### A2.10.1 Intent

**Business objective.** Takes the filing confirmation and the court case number from the firm onto the case.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Takes the filing confirmation and the court case number from the firm onto the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Law firm user | Opens the screen and record the court filing and receipt | Checks the role, the capability area and the scope |
| 2 | Law firm user | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal, LIT

**Prerequisites.** FEAT-LIT-09

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-010-1 | Pack incomplete at filing | MSG-S4-001 The pack is missing {item}. Add it before filing. |
| R-LIT-31 | Record the defect and return the pack for rework, when the court returns the filing for a defect | Moves to FILING_REJECTED |
| R-LIT-30 | Write the court case number to the Legal Action and set the hearing timers, when the firm uploads the receipt and the court case number | Moves to FILED_IN_COURT |
| BR-S4-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| legal_action.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| legal_action.law_firm_id | The law firm instructed | uuid | No | None | No |
| legal_action.action_type | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction | varchar(20) | Yes | LOV-LEGAL-TYPE | No |
| legal_action.lawsuit_no | Lawsuit reference in LIT | varchar(30) | No | None | No |
| legal_action.black_case_no | Court black case number | varchar(30) | No | None | No |
| legal_action.red_case_no | Court red case number after judgment | varchar(30) | No | None | No |
| legal_action.court_name | Court | varchar(120) | No | None | No |
| legal_action.claim_amount | Amount sued for, baht | numeric(18,2) | No | None | No |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| Law firm user | Primary |
| Litigation officer | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-010-01 | Record the court filing and receipt | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-010-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-010-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.11 Track hearings, deadlines and fees

#### A2.11.1 Intent

**Business objective.** Follows the court calendar, raises each deadline and accrues the fees against the case.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Follows the court calendar, raises each deadline and accrues the fees against the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Track hearings, deadlines and fees | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** LIT, Partner portal

**Prerequisites.** FEAT-LIT-10

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-011-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S4-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-011-01 | Track hearings, deadlines and fees | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-011-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-011-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.12 Recommend the next litigation step

#### A2.12.1 Intent

**Business objective.** Proposes the next step with reasons, for the officer or the approver to decide.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Proposes the next step with reasons, for the officer or the approver to decide.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Recommend the next litigation step | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Model gateway

**Prerequisites.** FEAT-LIT-11

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-012-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-04 | Hold generation and raise a task to the litigation officer, when template_status = withdrawn | Moves to NOTICE_BLOCKED |
| R-LIT-16 | Present the pack to the litigation officer for verification, when every defect list item present | Moves to PACK_VERIFIED |
| R-LIT-36 | The agent proposes the step with its cost and effect, and routes it to the approver, when the customer or the firm proposes a settlement before judgment | Moves to SETTLEMENT_OFFERED_AT_COURT |
| BR-S4-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-012-01 | Recommend the next litigation step | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-012-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-012-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.13 Settle before judgment

#### A2.13.1 Intent

**Business objective.** Takes a settlement during the case to the approver named by the limit, and books it if approved.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Takes a settlement during the case to the approver named by the limit, and books it if approved.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Litigation officer | Opens the screen and settle before judgment | Checks the role, the capability area and the scope |
| 2 | Litigation officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-01

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-013-1 | Pack incomplete at filing | MSG-S4-001 The pack is missing {item}. Add it before filing. |
| VR-S4-013-2 | Prescription date near | MSG-S4-002 The claim on this case expires on {date}. File before then. |
| R-LIT-36 | The agent proposes the step with its cost and effect, and routes it to the approver, when the customer or the firm proposes a settlement before judgment | Moves to SETTLEMENT_OFFERED_AT_COURT |
| R-LIT-37 | Book the treatment and hold the litigation rather than withdraw it, when inside the D7.4 limit, or the committee approves above it | Moves to LITIGATION_HELD |
| R-LIT-38 | Continue the case to judgment, when the approver rejects with a reason | Moves to IN_HEARING |
| BR-S4-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| legal_action.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| legal_action.law_firm_id | The law firm instructed | uuid | No | None | No |
| legal_action.action_type | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction | varchar(20) | Yes | LOV-LEGAL-TYPE | No |
| legal_action.lawsuit_no | Lawsuit reference in LIT | varchar(30) | No | None | No |
| legal_action.black_case_no | Court black case number | varchar(30) | No | None | No |
| legal_action.red_case_no | Court red case number after judgment | varchar(30) | No | None | No |
| legal_action.court_name | Court | varchar(120) | No | None | No |
| legal_action.claim_amount | Amount sued for, baht | numeric(18,2) | No | None | No |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| Litigation officer | Primary |
| Head of Litigation, Product head (Mortgage, HP, SSME) | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-013-01 | Settle before judgment | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-013-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-013-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.14 Decide and manage an appeal

#### A2.14.1 Intent

**Business objective.** Records the appeal decision, the grounds and the approval, and tracks it to its end.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Records the appeal decision, the grounds and the approval, and tracks it to its end.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Litigation officer | Opens the screen and decide and manage an appeal | Checks the role, the capability area and the scope |
| 2 | Litigation officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** LIT, Workbench

**Prerequisites.** FEAT-LIT-12

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-014-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S4-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| legal_action.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| legal_action.law_firm_id | The law firm instructed | uuid | No | None | No |
| legal_action.action_type | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction | varchar(20) | Yes | LOV-LEGAL-TYPE | No |
| legal_action.lawsuit_no | Lawsuit reference in LIT | varchar(30) | No | None | No |
| legal_action.black_case_no | Court black case number | varchar(30) | No | None | No |
| legal_action.red_case_no | Court red case number after judgment | varchar(30) | No | None | No |
| legal_action.court_name | Court | varchar(120) | No | None | No |
| legal_action.claim_amount | Amount sued for, baht | numeric(18,2) | No | None | No |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| Litigation officer | Primary |
| Head of Litigation | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-014-01 | Decide and manage an appeal | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-014-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-014-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.15 Pay court fees and legal expenses

#### A2.15.1 Intent

**Business objective.** Checks the fee against the schedule, routes it for approval where needed and pays it.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Checks the fee against the schedule, routes it for approval where needed and pays it.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Pay court fees and legal expenses | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal, ALS and GL

**Prerequisites.** FEAT-PAY-05

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-015-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-30 | Write the court case number to the Legal Action and set the hearing timers, when the firm uploads the receipt and the court case number | Moves to FILED_IN_COURT |
| BR-S4-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-015-01 | Pay court fees and legal expenses | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-015-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-015-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.16 Record the judgment

#### A2.16.1 Intent

**Business objective.** Writes the judgment date and amount onto the case and opens the enforcement step.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Writes the judgment date and amount onto the case and opens the enforcement step.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Record the judgment | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** LIT, Workbench

**Prerequisites.** FEAT-LIT-11

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-016-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-44 | Record the judgment date and amount and open the enforcement task, when judgment_type in (full, partial, default) | Moves to JUDGMENT_RECORDED |
| R-LIT-45 | Record the dismissal and open the appeal window, when judgment_type = dismissed | Moves to JUDGMENT_DISMISSED |
| R-LIT-51 | Match the payment, close the enforcement and close the case, when a payment after judgment covers the balance and costs | Moves to CASE_CLOSED |
| BR-S4-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Enforcement owner | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-016-01 | Record the judgment | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-016-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-016-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.17 Trace assets for enforcement

#### A2.17.1 Intent

**Business objective.** Searches the bureau, registries and insurers for assets to enforce against, and reports what it finds.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.17.2 Description

**Functional overview.** Searches the bureau, registries and insurers for assets to enforce against, and reports what it finds.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Trace assets for enforcement | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** NCB, Model gateway

**Prerequisites.** FEAT-AGT-01

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-017-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-50 | Trace assets across NCB, internal data, registries and insurers, when a judgment is recorded against the debtor | Moves to ASSET_TRACE |
| R-LIT-52 | Present the enforcement decision with the traced assets, when one or more assets traced | Moves to ENFORCEMENT_DECISION |
| BR-S4-017 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Enforcement owner | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-017-01 | Trace assets for enforcement | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-017-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-017-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.18 Apply for the writ and seizure

#### A2.18.1 Intent

**Business objective.** Instructs the writ and the seizure through the firm and tracks it to execution.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.18.2 Description

**Functional overview.** Instructs the writ and the seizure through the firm and tracks it to execution.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Law firm user | Opens the screen and apply for the writ and seizure | Checks the role, the capability area and the scope |
| 2 | Law firm user | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal, LIT

**Prerequisites.** FEAT-LIT-17

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-018-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-LIT-54 | Instruct the firm to apply for the writ and seizure, when an asset is traced and enforcement is economic | Moves to WRIT_AND_SEIZURE |
| BR-S4-018 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.18.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| legal_action.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| legal_action.law_firm_id | The law firm instructed | uuid | No | None | No |
| legal_action.action_type | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction | varchar(20) | Yes | LOV-LEGAL-TYPE | No |
| legal_action.lawsuit_no | Lawsuit reference in LIT | varchar(30) | No | None | No |
| legal_action.black_case_no | Court black case number | varchar(30) | No | None | No |
| legal_action.red_case_no | Court red case number after judgment | varchar(30) | No | None | No |
| legal_action.court_name | Court | varchar(120) | No | None | No |
| legal_action.claim_amount | Amount sued for, baht | numeric(18,2) | No | None | No |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| Law firm user | Primary |
| Enforcement owner | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-018-01 | Apply for the writ and seizure | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-018-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-018-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.19 Follow the LED auction ladder

#### A2.19.1 Intent

**Business objective.** Tracks the enforcement auction through the 100, 90, 80 and 70 percent steps of official value.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.19.2 Description

**Functional overview.** Tracks the enforcement auction through the 100, 90, 80 and 70 percent steps of official value.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Follow the LED auction ladder | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** LED portal, LIT

**Prerequisites.** FEAT-LIT-18

#### A2.19.3 Business rules and structure

##### A2.19.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-019-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-67 | Record the unsold result and refer it to the enforcement owner, when round_result = no bid and auction_price_basis = 70 percent | Moves to NO_BID_AT_70 |
| BR-S4-019 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.19.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Enforcement owner | Also uses |

#### A2.19.4 Acceptance criteria

##### A2.19.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-019-01 | Follow the LED auction ladder | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.19.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.19.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-019-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-019-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.19.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.20 Record an enforcement deferral with its reason

#### A2.20.1 Intent

**Business objective.** Lets the enforcement owner defer with a coded reason and a review date. Enforcement after judgment has no owner today.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.20.2 Description

**Functional overview.** Lets the enforcement owner defer with a coded reason and a review date. Enforcement after judgment has no owner today.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Enforcement owner | Opens the screen and record an enforcement deferral with its reason | Checks the role, the capability area and the scope |
| 2 | Enforcement owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-LIT-16

#### A2.20.3 Business rules and structure

##### A2.20.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-020-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-LIT-55 | Record the deferral and re-queue the case on the review date, when deferral_reason and deferral_review_date are both present | Moves to DEFERRAL_RECORDED |
| R-LIT-44 | Record the judgment date and amount and open the enforcement task, when judgment_type in (full, partial, default) | Moves to JUDGMENT_RECORDED |
| R-LIT-51 | Match the payment, close the enforcement and close the case, when a payment after judgment covers the balance and costs | Moves to CASE_CLOSED |
| BR-S4-020 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.20.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| legal_action.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| legal_action.law_firm_id | The law firm instructed | uuid | No | None | No |
| legal_action.action_type | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction | varchar(20) | Yes | LOV-LEGAL-TYPE | No |
| legal_action.lawsuit_no | Lawsuit reference in LIT | varchar(30) | No | None | No |
| legal_action.black_case_no | Court black case number | varchar(30) | No | None | No |
| legal_action.red_case_no | Court red case number after judgment | varchar(30) | No | None | No |
| legal_action.court_name | Court | varchar(120) | No | None | No |
| legal_action.claim_amount | Amount sued for, baht | numeric(18,2) | No | None | No |

##### A2.20.3.3 Roles and permissions

| Role | Use |
|---|---|
| Enforcement owner | Primary |
| Head of Litigation | Also uses |

#### A2.20.4 Acceptance criteria

##### A2.20.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-020-01 | Record an enforcement deferral with its reason | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.20.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.20.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-020-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-020-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.20.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.21 File a bankruptcy petition

#### A2.21.1 Intent

**Business objective.** Takes the petition to the approver and files it through the firm.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.21.2 Description

**Functional overview.** Takes the petition to the approver and files it through the firm.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Enforcement owner | Opens the screen and file a bankruptcy petition | Checks the role, the capability area and the scope |
| 2 | Enforcement owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** LIT, Partner portal

**Prerequisites.** FEAT-APD-01

#### A2.21.3 Business rules and structure

##### A2.21.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-021-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-LIT-58 | Route the petition to the approver at D7.5, when enforcement exhausted and the bankruptcy test is met | Moves to BANKRUPTCY_PETITION |
| BR-S4-021 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.21.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| legal_action.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| legal_action.law_firm_id | The law firm instructed | uuid | No | None | No |
| legal_action.action_type | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction | varchar(20) | Yes | LOV-LEGAL-TYPE | No |
| legal_action.lawsuit_no | Lawsuit reference in LIT | varchar(30) | No | None | No |
| legal_action.black_case_no | Court black case number | varchar(30) | No | None | No |
| legal_action.red_case_no | Court red case number after judgment | varchar(30) | No | None | No |
| legal_action.court_name | Court | varchar(120) | No | None | No |
| legal_action.claim_amount | Amount sued for, baht | numeric(18,2) | No | None | No |

##### A2.21.3.3 Roles and permissions

| Role | Use |
|---|---|
| Enforcement owner | Primary |
| Head of Litigation, Legal counsel | Also uses |

#### A2.21.4 Acceptance criteria

##### A2.21.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-021-01 | File a bankruptcy petition | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.21.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.21.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-021-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-021-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.21.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.22 Match enforcement proceeds to the case

#### A2.22.1 Intent

**Business objective.** Matches money from the LED or the firm to the case and applies it to the balance.

**Problem.** Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Litigation turnaround | 6 days | Decision log and Workbench records | Monthly |

#### A2.22.2 Description

**Functional overview.** Matches money from the LED or the firm to the case and applies it to the balance.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Match enforcement proceeds to the case | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, LED portal

**Prerequisites.** FEAT-PAY-04

#### A2.22.3 Business rules and structure

##### A2.22.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S4-022-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-LIT-51 | Match the payment, close the enforcement and close the case, when a payment after judgment covers the balance and costs | Moves to CASE_CLOSED |
| R-LIT-65 | Match the proceeds to the case, when round_result = sold at 100, 90, 80 or 70 percent of official value | Moves to PROCEEDS_MATCHED |
| R-LIT-70 | Close the enforcement and the case, and retain the record after close, when proceeds cover the judgment total and the costs | Moves to CASE_CLOSED |
| BR-S4-022 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.22.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Enforcement owner | Also uses |

#### A2.22.4 Acceptance criteria

##### A2.22.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S4-022-01 | Match enforcement proceeds to the case | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.22.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.22.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S4-022-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S4-022-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.22.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-S4-001 | Demand and recall notices are generated by rule, approved, dispatched, and their notice periods are timed. | Must | E5 |
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested. | Must | E5 |
| REQ-S4-003 | The litigation officer verifies the pack against the defect list before filing is approved. | Must | E5 |
| REQ-S4-004 | A law firm is selected from the panel by rule using panel performance, and instructed through the partner portal. | Must | E5 |
| REQ-S4-005 | Court state, hearing dates, deadlines and fees are tracked on the case without a person reading an email. | Must | E5 |
| REQ-S4-006 | Settlement before judgment, an appeal and fee payment each need approval inside the delegation. | Must | E5 |
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement. | Must | E5 |
| REQ-S4-008 | A deferred enforcement step carries a coded reason and a review date. | Must | E5 |
| REQ-S4-009 | Prescription warnings force a litigation review ahead of every other open action on the case. | Must | E5 |
| REQ-S4-010 | Proceeds from enforcement are matched to the case and posted. | Must | E5 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-18 Notice approval | Generated demand and recall notices for approval before dispatch | E2 |
| SCR-19 Litigation workspace | Pack, instruction, court dates, hearings and judgment for a case | E5 |
| SCR-20 Enforcement workspace | Enforcement steps with the Legal Execution Department and the result | E5 |

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
| Lawsuit | การฟ้องร้องคดี | A civil case filed against the borrower or guarantor |
| Black case number | หมายเลขคดีดำ | The court number given when a case is filed |
| Red case number | หมายเลขคดีแดง | The court number given at judgment |
| Judgment | คำพิพากษา | The court's decision on the claim |
| Enforcement | การบังคับคดี | Steps after judgment to seize and sell assets |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
