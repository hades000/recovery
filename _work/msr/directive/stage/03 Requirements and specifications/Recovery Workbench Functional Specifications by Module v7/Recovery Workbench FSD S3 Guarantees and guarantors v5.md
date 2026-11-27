SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench S3 Guarantees and guarantors

**Change log.** D-RCV-60, 26 November 2026: cross-document changes under the programme directive. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD S3 Guarantees and guarantors |
| Document ID | S3-RWB-FSD-v4 |
| Service | `rwb-guarantee` (Guarantee) |
| Version | 4 |
| Status | Draft |
| Classification | Confidential |
| Date | 15 November 2026 |
| Change note | v3, 15 November 2026: re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Constraint, freshness rule and trigger wording only. Everything else unchanged from v2. |
| FSD owner | Business analyst, S3 |
| Business owner | Business lead |
| Change | 4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

| Module code | Module name | First in |
|---|---|---|
| S3 | Guarantees and guarantors | E4 |

**Feature scope.** TCG and insurance claims, guarantor notices and pursuit.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification S3 Guarantees and guarantors | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |

### Note, Architecture v5 (D-RCV-60)

| Item | Value |
|---|---|
| Service | `rwb-guarantee` (Guarantee) |
| Owns in Architecture v5 | TCG and insurance claims, guarantor notices and pursuit |
| Service epic | `RWB-SVC-S3` |
| Wave | 3 |
| Schema | `rwb_guarantee` |
| REST base | `/api/recovery/guarantee/v1` |
| Kafka topic | `rwb.guarantee.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.guarantee.<Event>.v1` |
| Temporal task queue | `rwb-guarantee` |
| Java package | `th.co.scb.ace.workbench.recovery.guarantee` |

Version 4 adds the Service row, the Change row and this note above; nothing else in this document changes. Under Architecture v5 the module is delivered as the service `rwb-guarantee` of the 19 services inside ACE (ADR-013), with its own schema `rwb_guarantee` and login (ADR-014), in wave 3, service epic `RWB-SVC-S3`; the realignment is D-RCV-60 (DL44), and DL46 keeps team-type ownership soft. The functional content of this document is the content of version 3, kept word for word: every feature, requirement, rule, field, list, message, screen, count and date.

Every owner named in this document is the owner recorded in the Microservice Ownership Map v1, and where the map carries a ruling of Template and Rules §R3 the ruling is followed: parameters and reference data with `rwb-case` (DP-06, DP-07), the rule package registry with `rwb-decision` (DP-04), the interaction ledger with `rwb-source-data` (DP-18) and feature flags with the platform library. Where this document names a table, endpoint, event, job, workflow or screen that the map gives to another service, that service owns it and this module reaches it only through the owner's contract (DP-01, DP-11; ADR-020).

Release dates stay as written and are tentative (DL48). No approval of version 4 is recorded (ASM-3046); the version is Draft.

### Inherited change history (GAP-1735)

| Version | Date | Change note |
|---|---|---|
| 3 | 15 November 2026 | v3, 15 November 2026: re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Constraint, freshness rule and trigger wording only. Everything else unchanged from v2. |
| 2 | 28 October 2026 | Not specified in the source documents (GAP-1735) |
| 1 | Not specified in the source documents (GAP-1735) | Not specified in the source documents (GAP-1735) |

Open item (GAP-1735): the change history of versions 1 and 2 is incomplete and stays open until the FSD owner (Business analyst, S3) supplies it. The version 2 date is taken from the document control of the version 2 copy held in folder 13 (`requirement/legacy`), which records no change note.

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

**In scope.** TCG and insurance claims, guarantor notices and pursuit.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-DCM-16; FEAT-GUA-01; FEAT-GUA-02; FEAT-GUA-03; FEAT-GUA-05; FEAT-OCC-01; FEAT-VAL-01

**Constraints.** Built in the ACE service as part of the recovery module; source data read only from the ACE database through the SELECT-only `recovery.v_ace_*` views, landed by ACE's own ingestion, with no inbound load in the Workbench (D-RCV-35); every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| S3 | FEAT-GUA-01 | Prepare a TCG guarantee claim | System | Assembles the claim from the case facts and the documents the scheme requires. | E4 | A2.1 |
| S3 | FEAT-GUA-02 | Submit the claim to the TCG portal | System | Files the prepared claim and records the submission reference on the case. | E4 | A2.2 |
| S3 | FEAT-GUA-03 | Track the claim to payment | System | Follows the claim through its states and raises the service level breach if it stalls. | E4 | A2.3 |
| S3 | FEAT-GUA-04 | Record the subrogation position | System | Records what the guarantor may reclaim after payment, so the position is not lost. | E4 | A2.4 |
| S3 | FEAT-GUA-05 | Notify guarantors and co-borrowers | System | Sends the demand to every guarantor and co-borrower on the case, from the approved template. | E4 | A2.5 |
| S3 | FEAT-GUA-06 | Negotiate with a guarantor | User | Lets the case owner negotiate within the range and record the outcome against the party. | E4 | A2.6 |
| S3 | FEAT-GUA-07 | Close the case when a guarantee clears the debt | System | Closes the case and records the position when a guarantee payment clears the balance in full. | E4 | A2.7 |
| S3 | FEAT-GUA-08 | File an insurance claim on a collateral event | User | Files the claim where collateral is stolen, written off or damaged, and triggers re-appraisal. | E4 | A2.8 |

### A1.3 Background

Guarantee and TCG claims are late because deadlines are not tracked.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Prepare a TCG guarantee claim

#### A2.1.1 Intent

**Business objective.** Assembles the claim from the case facts and the documents the scheme requires.

**Problem.** Guarantee and TCG claims are late because deadlines are not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Claims filed inside the deadline | 100 percent | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Assembles the claim from the case facts and the documents the scheme requires.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Prepare a TCG guarantee claim | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, TCG portal

**Prerequisites.** FEAT-DCM-16

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S3-001-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-GUA-04 | The claim preparation agent assembles the claim against the scheme checklist, when days to claim_deadline <= the preparation window | Moves to CLAIM_PREPARATION |
| R-GUA-01 | Start the claim deadline timer from the date the default conditions are met, when guarantee_type = TCG scheme and scheme_code present | Moves to DEADLINE_TIMER_RUNNING |
| R-GUA-02 | Record that no claim arises and hold the guarantee, when the scheme default conditions are not satisfied | Moves to NOT_ELIGIBLE |
| BR-S3-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Guarantee officer | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S3-001-01 | Prepare a TCG guarantee claim | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S3-001-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S3-001-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Submit the claim to the TCG portal

#### A2.2.1 Intent

**Business objective.** Files the prepared claim and records the submission reference on the case.

**Problem.** Guarantee and TCG claims are late because deadlines are not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Claims filed inside the deadline | 100 percent | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Files the prepared claim and records the submission reference on the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Submit the claim to the TCG portal | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** TCG portal

**Prerequisites.** FEAT-GUA-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S3-002-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-GUA-12 | Submit the claim through the TCG claim channel, when the guarantee officer verifies the claim at D6.5 | Moves to CLAIM_SUBMITTED |
| R-GUA-21 | Submit the balance claim, when the unpaid share is still claimable inside the deadline | Moves to CLAIM_SUBMITTED |
| BR-S3-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Guarantee officer | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S3-002-01 | Submit the claim to the TCG portal | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S3-002-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S3-002-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Track the claim to payment

#### A2.3.1 Intent

**Business objective.** Follows the claim through its states and raises the service level breach if it stalls.

**Problem.** Guarantee and TCG claims are late because deadlines are not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Claims filed inside the deadline | 100 percent | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Follows the claim through its states and raises the service level breach if it stalls.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Track the claim to payment | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** TCG portal, Workbench

**Prerequisites.** FEAT-GUA-02

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S3-003-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-GUA-05 | Record the lost claim, the reason and the amount, and report the breach, when claim_deadline passed and claim_status is not submitted | Moves to DEADLINE_MISSED |
| R-GUA-09 | Record the lost claim and the reason, and report the breach, when claim_deadline passed before submission | Moves to DEADLINE_MISSED |
| R-GUA-12 | Submit the claim through the TCG claim channel, when the guarantee officer verifies the claim at D6.5 | Moves to CLAIM_SUBMITTED |
| BR-S3-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Guarantee officer | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S3-003-01 | Track the claim to payment | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S3-003-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S3-003-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Record the subrogation position

#### A2.4.1 Intent

**Business objective.** Records what the guarantor may reclaim after payment, so the position is not lost.

**Problem.** Guarantee and TCG claims are late because deadlines are not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Claims filed inside the deadline | 100 percent | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Records what the guarantor may reclaim after payment, so the position is not lost.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Record the subrogation position | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, Workbench

**Prerequisites.** FEAT-GUA-03

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S3-004-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-GUA-22 | Match the payment, post it, and set the subrogation position, when claim_amount_paid = guaranteed_amount | Moves to CLAIM_PAID |
| R-GUA-23 | Record the TCG share against the case for all future recoveries, when TCG holds a share of every later recovery | Moves to SUBROGATION_POSITION |
| R-GUA-24 | Record the TCG share against the case for all future recoveries, when TCG holds a share of every later recovery | Moves to SUBROGATION_POSITION |
| BR-S3-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Guarantee officer | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S3-004-01 | Record the subrogation position | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S3-004-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S3-004-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Notify guarantors and co-borrowers

#### A2.5.1 Intent

**Business objective.** Sends the demand to every guarantor and co-borrower on the case, from the approved template.

**Problem.** Guarantee and TCG claims are late because deadlines are not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Claims filed inside the deadline | 100 percent | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Sends the demand to every guarantor and co-borrower on the case, from the approved template.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Notify guarantors and co-borrowers | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** WIN, Workbench

**Prerequisites.** FEAT-OCC-01

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S3-005-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S3-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S3-005-01 | Notify guarantors and co-borrowers | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S3-005-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S3-005-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Negotiate with a guarantor

#### A2.6.1 Intent

**Business objective.** Lets the case owner negotiate within the range and record the outcome against the party.

**Problem.** Guarantee and TCG claims are late because deadlines are not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Claims filed inside the deadline | 100 percent | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Lets the case owner negotiate within the range and record the outcome against the party.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and negotiate with a guarantor | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-GUA-05

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S3-006-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-GUA-23 | Record the TCG share against the case for all future recoveries, when TCG holds a share of every later recovery | Moves to SUBROGATION_POSITION |
| R-GUA-24 | Record the TCG share against the case for all future recoveries, when TCG holds a share of every later recovery | Moves to SUBROGATION_POSITION |
| R-GUA-29 | Record the refusal and return the case to the route decision, when the guarantor refuses, or does not reply by the notice expiry | Moves to RESIDUAL_TO_ROUTE |
| BR-S3-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| guarantee_claim.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| guarantee_claim.claim_type | TCG, credit life insurance, mortgage insurance, collateral insurance | varchar(25) | Yes | LOV-CLAIM-TYPE | No |
| guarantee_claim.claim_deadline | Last date the claim can be filed | date | Yes | None | No |
| guarantee_claim.claimed_amount | Amount claimed, baht | numeric(18,2) | Yes | None | No |
| guarantee_claim.filed_at | Date filed | date | No | None | No |
| guarantee_claim.paid_amount | Amount paid, baht | numeric(18,2) | No | None | No |
| guarantee_claim.status | Preparing, filed, defect, paid, rejected | varchar(12) | Yes | LOV-CLAIM-STATUS | No |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Guarantee officer | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S3-006-01 | Negotiate with a guarantor | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S3-006-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S3-006-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Close the case when a guarantee clears the debt

#### A2.7.1 Intent

**Business objective.** Closes the case and records the position when a guarantee payment clears the balance in full.

**Problem.** Guarantee and TCG claims are late because deadlines are not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Claims filed inside the deadline | 100 percent | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Closes the case and records the position when a guarantee payment clears the balance in full.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Close the case when a guarantee clears the debt | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-GUA-03

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S3-007-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| R-GUA-19 | Close the guarantee and return the full balance to the route decision, when the reason is not curable, or claim_deadline has passed | Moves to RESIDUAL_TO_ROUTE |
| R-GUA-26 | Close the guarantee and close the case, when the balance after the guaranteed share is zero | Moves to GUARANTEE_CLOSED |
| R-GUA-27 | Return the full balance to the route decision and close the guarantee, when the loss amount and the reason are recorded | Moves to RESIDUAL_TO_ROUTE |
| BR-S3-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Guarantee officer | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S3-007-01 | Close the case when a guarantee clears the debt | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S3-007-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S3-007-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 File an insurance claim on a collateral event

#### A2.8.1 Intent

**Business objective.** Files the claim where collateral is stolen, written off or damaged, and triggers re-appraisal.

**Problem.** Guarantee and TCG claims are late because deadlines are not tracked.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Claims filed inside the deadline | 100 percent | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Files the claim where collateral is stolen, written off or damaged, and triggers re-appraisal.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and file an insurance claim on a collateral event | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, SVAF

**Prerequisites.** FEAT-VAL-01

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S3-008-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S3-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| guarantee_claim.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| guarantee_claim.claim_type | TCG, credit life insurance, mortgage insurance, collateral insurance | varchar(25) | Yes | LOV-CLAIM-TYPE | No |
| guarantee_claim.claim_deadline | Last date the claim can be filed | date | Yes | None | No |
| guarantee_claim.claimed_amount | Amount claimed, baht | numeric(18,2) | Yes | None | No |
| guarantee_claim.filed_at | Date filed | date | No | None | No |
| guarantee_claim.paid_amount | Amount paid, baht | numeric(18,2) | No | None | No |
| guarantee_claim.status | Preparing, filed, defect, paid, rejected | varchar(12) | Yes | LOV-CLAIM-STATUS | No |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Hardship and vulnerability specialist | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S3-008-01 | File an insurance claim on a collateral event | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S3-008-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S3-008-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-S3-001 | A guarantee claim is prepared from case data and submitted inside the guarantor's deadline. | Must | E4 |
| REQ-S3-002 | Claim status, payment and any shortfall are recorded on the case. | Must | E4 |
| REQ-S3-003 | A guarantee payment that clears the balance closes the case and records the subrogation position. | Must | E4 |
| REQ-S3-004 | Guarantor and co-borrower notices are generated by rule and sent on the same path as customer notices. | Must | E4 |
| REQ-S3-005 | A guarantor who answers a demand enters the same treatment paths as a borrower. | Must | E4 |
| REQ-S3-006 | A rejected or reduced claim raises a reason and routes the residual to the next decision. | Must | E4 |
| REQ-S3-007 | Claims are filtered for eligibility before submission so that ineligible claims are not filed. | Should | E4 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-17 Guarantee claim | The guarantee, the claim deadline, the checklist and the claim result | E4 |

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
| Guarantee claim | การยื่นขอรับค่าประกันชดเชย | A claim against a Thai Credit Guarantee Corporation guarantee or an insurer |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
