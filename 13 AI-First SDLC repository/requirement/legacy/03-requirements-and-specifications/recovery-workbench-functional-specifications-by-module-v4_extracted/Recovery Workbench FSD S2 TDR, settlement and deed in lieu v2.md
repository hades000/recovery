<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v4.zip!Recovery Workbench FSD S2 TDR, settlement and deed in lieu v2.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v4.zip!Recovery Workbench FSD S2 TDR, settlement and deed in lieu v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S2 TDR, settlement and deed in lieu

Functional specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD S2 TDR, settlement and deed in lieu |
| Document ID | S2-RWB-FSD-v2 |
| Version | 2 |
| Status | In review |
| Classification | Confidential |
| Date | 28 October 2026 |
| FSD owner | Business analyst, S2 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| S2 | TDR, settlement and deed in lieu | E2 foundations; E3 |

**Feature scope.** Treatment record, contracts, booking, plan timers.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification S2 TDR, settlement and deed in lieu | TSD | Pair |
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
| Restructure calculator | REUSE | ACE common module | Called from the treatment record |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** Treatment record, contracts, booking, plan timers.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-APD-01; FEAT-CHO-02; FEAT-CHO-06; FEAT-CHO-07, FEAT-CHO-08; FEAT-CHO-08; FEAT-DCM-12; FEAT-OCC-01, FEAT-TRT-04; FEAT-OCC-07

**Constraints.** Built in the ACE service as part of the recovery module; data through COLLINS and file loads; every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| S2 | FEAT-TRT-01 | Create the treatment record | System | Opens the treatment for the chosen route, holding the terms, the approval and the outcome. | E3 | A2.1 |
| S2 | FEAT-TRT-02 | Offer a settlement inside the range | User | Lets the officer build and send a settlement offer within the calculated range. | E3 | A2.2 |
| S2 | FEAT-TRT-03 | Approve a settlement below the floor | User | Routes a settlement below the floor price to the approver or the committee named in the matrix. | E3 | A2.3 |
| S2 | FEAT-TRT-04 | Offer a TDR plan | User | Lets the restructuring officer build and send the plan offer, with the band and the rule version applied. | E3 | A2.4 |
| S2 | FEAT-TRT-05 | Pre-assess affordability through ACE | System | Calls the ACE affordability calculation and records the result against the offer. | E3 | A2.5 |
| S2 | FEAT-TRT-06 | Calculate the plan installment | System | Produces the model installment and the range the officer may move within. | E3 | A2.6 |
| S2 | FEAT-TRT-07 | Send the offer and start the validity timer | System | Sends the offer to the customer and starts the validity clock. The wait is a timer, not a routed state. | E3 | A2.7 |
| S2 | FEAT-TRT-08 | Route the signed offer to operations for booking | System | Moves the case to operations when the customer signs inside the validity period. | E3 | A2.8 |
| S2 | FEAT-TRT-09 | Return the case to its prior status on no signature | System | Sends the case back to the status it held in COLLINS when the customer declines or the offer expires. | E3 | A2.9 |
| S2 | FEAT-TRT-10 | Book the plan and set the schedule | System | Writes the plan to NLEADS and ALS, sets the payment schedule and starts the plan timers. | E3 | A2.10 |
| S2 | FEAT-TRT-11 | Detect and handle a broken plan | System | Counts missed payments against the break rule and moves the case to the point the rule names. | E3 | A2.11 |
| S2 | FEAT-TRT-12 | Run a deed in lieu to ownership transfer | User | Takes the deed in lieu from offer through inspection, documents and transfer to the asset record. | E3 | A2.12 |
| S2 | FEAT-TRT-13 | Check encumbrance and eligibility before negotiation | System | Runs the encumbrance and title checks early, so a deed in lieu is not negotiated on an asset that cannot transfer. | E3 | A2.13 |
| S2 | FEAT-TRT-14 | Unlock the asset as a non performing asset by rule | System | Applies the auto-unlock rule so the asset moves to the asset list without a person for the cases that qualify. | E3 | A2.14 |
| S2 | FEAT-TRT-15 | Capture the collateral inspection in the field | User | Lets the field officer record the inspection, the checklist and the bills against the case. | E3 | A2.15 |
| S2 | FEAT-TRT-16 | Set up a deed in lieu buy-back rental | System | Opens the rental record, the auto-debit and the receipt loop where the customer buys back. | E3 | A2.16 |
| S2 | FEAT-TRT-17 | Release the collateral after settlement | System | Tells CCMS to release the security once the settlement has cleared, and records the release. | E3 | A2.17 |
| S2 | FEAT-TRT-18 | Generate the treatment document set | System | Produces the agreement, contract, credit approval and mortgage documents for the treatment chosen. | E3 | A2.18 |

### A1.3 Background

Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Create the treatment record

#### A2.1.1 Intent

**Business objective.** Opens the treatment for the chosen route, holding the terms, the approval and the outcome.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Opens the treatment for the chosen route, holding the terms, the approval and the outcome.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Create the treatment record | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-CHO-06

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-001-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-RES-01 | Open the treatment record and ask COLLINS for the restructure proposal, when decision.approved and route = R1 | Moves to PROPOSED_IN_COLLINS |
| R-RES-10 | Route the offer to credit approval; 44% of TDR cases deviate today, when offer outside the range or deviation_flag = Y | Moves to AWAITING_CREDIT_APPROVAL |
| R-SET-02 | Open the treatment record and place the case in the FCR queue, when payoff_as_at inside the freshness limit | Moves to WITH_FCR_OFFICER_SET |
| BR-S2-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-001-01 | Create the treatment record | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-001-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-001-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Offer a settlement inside the range

#### A2.2.1 Intent

**Business objective.** Lets the officer build and send a settlement offer within the calculated range.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Lets the officer build and send a settlement offer within the calculated range.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Restructuring officer (FCR) | Opens the screen and offer a settlement inside the range | Checks the role, the capability area and the scope |
| 2 | Restructuring officer (FCR) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, COLLINS

**Prerequisites.** FEAT-TRT-01, FEAT-VAL-06

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-002-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-RES-07 | Return the calculated plan to the officer and build the offer, when affordability_result = pass | Moves to WITH_FCR_OFFICER |
| R-RES-04 | Assign the case to a restructuring officer and start the offer clock, when allocation rule matched and officer available | Moves to WITH_FCR_OFFICER |
| R-RES-15 | Return the case to the officer with the counter-offer and the gap, when counter_amount outside the current range | Moves to WITH_FCR_OFFICER |
| BR-S2-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| treatment.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| treatment.decision_log_id | The decision that approved it | uuid | No | None | No |
| treatment.treatment_type | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental | varchar(20) | Yes | LOV-TREATMENT | No |
| treatment.proposed_by | Agent, rule, person | varchar(10) | Yes | LOV-PROPOSER | No |
| treatment.proposed_at | When proposed | timestamptz | Yes | None | No |
| treatment.offer_amount | Amount offered or agreed, baht | numeric(18,2) | No | None | No |
| treatment.haircut_amount | Amount forgiven, baht | numeric(18,2) | No | None | No |
| treatment.installments | Number of installments in a plan | integer | No | None | No |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| Restructuring officer (FCR) | Primary |
| Case owner | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-002-01 | Offer a settlement inside the range | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-002-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-002-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Approve a settlement below the floor

#### A2.3.1 Intent

**Business objective.** Routes a settlement below the floor price to the approver or the committee named in the matrix.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Routes a settlement below the floor price to the approver or the committee named in the matrix.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Product head (Mortgage, HP, SSME) | Opens the screen and approve a settlement below the floor | Checks the role, the capability area and the scope |
| 2 | Product head (Mortgage, HP, SSME) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-01

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-003-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-DIL-15 | Route the price for a second signature, when transfer_price < floor_price | Moves to AWAITING_SECOND_SIGNATURE |
| R-DIL-17 | Return the case to the route decision with reason price_below_floor, when final_call = rejected | Moves to RETURNED_TO_ROUTE_DIL |
| R-SET-05 | Route the offer to the approver with the gap to the floor, when offer_amount < floor_price | Moves to AWAITING_APPROVAL_SET |
| BR-S2-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| treatment.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| treatment.decision_log_id | The decision that approved it | uuid | No | None | No |
| treatment.treatment_type | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental | varchar(20) | Yes | LOV-TREATMENT | No |
| treatment.proposed_by | Agent, rule, person | varchar(10) | Yes | LOV-PROPOSER | No |
| treatment.proposed_at | When proposed | timestamptz | Yes | None | No |
| treatment.offer_amount | Amount offered or agreed, baht | numeric(18,2) | No | None | No |
| treatment.haircut_amount | Amount forgiven, baht | numeric(18,2) | No | None | No |
| treatment.installments | Number of installments in a plan | integer | No | None | No |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| Product head (Mortgage, HP, SSME) | Primary |
| Credit approval committee member | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-003-01 | Approve a settlement below the floor | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-003-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-003-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Offer a TDR plan

#### A2.4.1 Intent

**Business objective.** Lets the restructuring officer build and send the plan offer, with the band and the rule version applied.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Lets the restructuring officer build and send the plan offer, with the band and the rule version applied.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Restructuring officer (FCR) | Opens the screen and offer a TDR plan | Checks the role, the capability area and the scope |
| 2 | Restructuring officer (FCR) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** COLLINS, EFS, ACE and TDR

**Prerequisites.** FEAT-TRT-01

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-004-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-RES-04 | Assign the case to a restructuring officer and start the offer clock, when allocation rule matched and officer available | Moves to WITH_FCR_OFFICER |
| R-RES-07 | Return the calculated plan to the officer and build the offer, when affordability_result = pass | Moves to WITH_FCR_OFFICER |
| R-RES-15 | Return the case to the officer with the counter-offer and the gap, when counter_amount outside the current range | Moves to WITH_FCR_OFFICER |
| BR-S2-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| treatment.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| treatment.decision_log_id | The decision that approved it | uuid | No | None | No |
| treatment.treatment_type | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental | varchar(20) | Yes | LOV-TREATMENT | No |
| treatment.proposed_by | Agent, rule, person | varchar(10) | Yes | LOV-PROPOSER | No |
| treatment.proposed_at | When proposed | timestamptz | Yes | None | No |
| treatment.offer_amount | Amount offered or agreed, baht | numeric(18,2) | No | None | No |
| treatment.haircut_amount | Amount forgiven, baht | numeric(18,2) | No | None | No |
| treatment.installments | Number of installments in a plan | integer | No | None | No |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| Restructuring officer (FCR) | Primary |
| Case owner | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-004-01 | Offer a TDR plan | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-004-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-004-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Pre-assess affordability through ACE

#### A2.5.1 Intent

**Business objective.** Calls the ACE affordability calculation and records the result against the offer.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Calls the ACE affordability calculation and records the result against the offer.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Pre-assess affordability through ACE | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE and TDR

**Prerequisites.** FEAT-CHO-02

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-005-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-RES-06 | Send the case to ACE for affordability and plan calculation, when treatment_type = TDR | Moves to AFFORDABILITY_IN_ACE |
| R-RES-07 | Return the calculated plan to the officer and build the offer, when affordability_result = pass | Moves to WITH_FCR_OFFICER |
| BR-S2-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-005-01 | Pre-assess affordability through ACE | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-005-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-005-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Calculate the plan installment

#### A2.6.1 Intent

**Business objective.** Produces the model installment and the range the officer may move within.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Produces the model installment and the range the officer may move within.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Calculate the plan installment | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE and TDR, COLLINS

**Prerequisites.** FEAT-TRT-05

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-006-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-SET-01 | Calculate the payoff from ALS and set the range from reference data, when decision.approved and route = R2 | Moves to PAYOFF_AND_RANGE_SET |
| BR-S2-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-006-01 | Calculate the plan installment | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-006-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-006-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Send the offer and start the validity timer

#### A2.7.1 Intent

**Business objective.** Sends the offer to the customer and starts the validity clock. The wait is a timer, not a routed state.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Sends the offer to the customer and starts the validity clock. The wait is a timer, not a routed state.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Send the offer and start the validity timer | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, WIN, NSS, LINE OA

**Prerequisites.** FEAT-OCC-01, FEAT-TRT-04

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-007-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-RES-04 | Assign the case to a restructuring officer and start the offer clock, when allocation rule matched and officer available | Moves to WITH_FCR_OFFICER |
| R-RES-11 | Release the offer and send it to the customer, when final_call = approved | Moves to OFFER_WITH_CUSTOMER |
| R-RES-15 | Return the case to the officer with the counter-offer and the gap, when counter_amount outside the current range | Moves to WITH_FCR_OFFICER |
| BR-S2-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-007-01 | Send the offer and start the validity timer | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-007-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-007-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 Route the signed offer to operations for booking

#### A2.8.1 Intent

**Business objective.** Moves the case to operations when the customer signs inside the validity period.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Moves the case to operations when the customer signs inside the validity period.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Route the signed offer to operations for booking | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, the Workbench document hub, ALS and GL

**Prerequisites.** FEAT-OCC-09

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-008-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-RES-16 | Route the case to operations to complete the booking, when signed = Y and signature verified | Moves to WITH_OPS_BOOKING |
| R-SET-10 | Route the case to operations and raise the payment instruction, when signed = Y | Moves to WITH_OPS_SETTLEMENT |
| R-RES-10 | Route the offer to credit approval; 44% of TDR cases deviate today, when offer outside the range or deviation_flag = Y | Moves to AWAITING_CREDIT_APPROVAL |
| BR-S2-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-008-01 | Route the signed offer to operations for booking | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-008-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-008-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.9 Return the case to its prior status on no signature

#### A2.9.1 Intent

**Business objective.** Sends the case back to the status it held in COLLINS when the customer declines or the offer expires.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Sends the case back to the status it held in COLLINS when the customer declines or the offer expires.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Return the case to its prior status on no signature | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** COLLINS, Workbench

**Prerequisites.** FEAT-TRT-07

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-009-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-RES-17 | Return the case to its prior status in COLLINS, when declined = Y | Moves to RETURNED_TO_COLLINS |
| R-RES-18 | Return the case to its prior status in COLLINS, when signed = N and offer_validity passed | Moves to RETURNED_TO_COLLINS |
| R-RES-15 | Return the case to the officer with the counter-offer and the gap, when counter_amount outside the current range | Moves to WITH_FCR_OFFICER |
| BR-S2-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-009-01 | Return the case to its prior status on no signature | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-009-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-009-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.10 Book the plan and set the schedule

#### A2.10.1 Intent

**Business objective.** Writes the plan to NLEADS and ALS, sets the payment schedule and starts the plan timers.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Writes the plan to NLEADS and ALS, sets the payment schedule and starts the plan timers.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Book the plan and set the schedule | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** NLEADS, ALS and GL

**Prerequisites.** FEAT-CHO-07, FEAT-CHO-08

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-010-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-RES-22 | Record the booking reference and set the payment schedule, when ALS and NLEADS both acknowledge | Moves to BOOKED_IN_ALS_NLEADS |
| R-RES-25 | Start the plan timers and move the plan to running, when first_due_date set | Moves to PLAN_RUNNING |
| BR-S2-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-010-01 | Book the plan and set the schedule | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-010-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-010-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.11 Detect and handle a broken plan

#### A2.11.1 Intent

**Business objective.** Counts missed payments against the break rule and moves the case to the point the rule names.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Counts missed payments against the break rule and moves the case to the point the rule names.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Detect and handle a broken plan | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, Workbench

**Prerequisites.** FEAT-OCC-11

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-011-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-RES-29 | Increment the break count and mark the plan broken, when no payment and cure_period passed | Moves to PLAN_BROKEN |
| R-RES-30 | Return the case to the route decision with reason broken_plan, when break_count < max_breaks | Moves to BACK_TO_ROUTE_DECISION |
| BR-S2-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-011-01 | Detect and handle a broken plan | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-011-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-011-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.12 Run a deed in lieu to ownership transfer

#### A2.12.1 Intent

**Business objective.** Takes the deed in lieu from offer through inspection, documents and transfer to the asset record.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Takes the deed in lieu from offer through inspection, documents and transfer to the asset record.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Restructuring officer (FCR) | Opens the screen and run a deed in lieu to ownership transfer | Checks the role, the capability area and the scope |
| 2 | Restructuring officer (FCR) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, CCMS, AMIS

**Prerequisites.** FEAT-TRT-01

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-012-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-DIL-28 | Record the asset in AMIS, settle the debt and release the registration, when product = HP and registration transferred in SCIS | Moves to ASSET_ON_BOOKS |
| R-DIL-16 | Generate the documents and put the offer to the customer, when final_call = approved | Moves to OFFER_WITH_CUSTOMER_DIL |
| R-DIL-18 | Schedule the collateral inspection before transfer, when product = MTG and signature is wet ink per Legal | Moves to WITH_FIELD_INSPECTION |
| BR-S2-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| treatment.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| treatment.decision_log_id | The decision that approved it | uuid | No | None | No |
| treatment.treatment_type | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental | varchar(20) | Yes | LOV-TREATMENT | No |
| treatment.proposed_by | Agent, rule, person | varchar(10) | Yes | LOV-PROPOSER | No |
| treatment.proposed_at | When proposed | timestamptz | Yes | None | No |
| treatment.offer_amount | Amount offered or agreed, baht | numeric(18,2) | No | None | No |
| treatment.haircut_amount | Amount forgiven, baht | numeric(18,2) | No | None | No |
| treatment.installments | Number of installments in a plan | integer | No | None | No |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| Restructuring officer (FCR) | Primary |
| Sale officer, Legal counsel | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-012-01 | Run a deed in lieu to ownership transfer | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-012-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-012-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.13 Check encumbrance and eligibility before negotiation

#### A2.13.1 Intent

**Business objective.** Runs the encumbrance and title checks early, so a deed in lieu is not negotiated on an asset that cannot transfer.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Runs the encumbrance and title checks early, so a deed in lieu is not negotiated on an asset that cannot transfer.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Check encumbrance and eligibility before negotiation | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** CCMS, Land Office

**Prerequisites.** FEAT-TRT-12

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-013-1 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| R-SET-22 | Raise a task to re-create the title set before release, when title documents not found | Moves to COLLATERAL_RELEASE_REQUESTED |
| R-DIL-01 | Prioritize the lead and start the early readiness checks, when decision.approved and route = R3 | Moves to EARLY_READINESS_CHECK |
| R-DIL-04 | Block the route and hold the case until the check clears, when product = MTG and encumbrance_status = unresolved | Moves to ENCUMBRANCE_BLOCKED |
| BR-S2-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-013-01 | Check encumbrance and eligibility before negotiation | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-013-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-013-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.14 Unlock the asset as a non performing asset by rule

#### A2.14.1 Intent

**Business objective.** Applies the auto-unlock rule so the asset moves to the asset list without a person for the cases that qualify.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Applies the auto-unlock rule so the asset moves to the asset list without a person for the cases that qualify.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Unlock the asset as a non performing asset by rule | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, AMIS

**Prerequisites.** FEAT-TRT-13

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-014-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-DIL-22 | Run the asset unlock rule, when checklist, photographs and bills captured | Moves to ASSET_UNLOCK_DECISION |
| R-DIL-23 | Release the asset for transfer, when unlock rule passes, about 95% of cases | Moves to AWAITING_TRANSFER |
| BR-S2-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-014-01 | Unlock the asset as a non performing asset by rule | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-014-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-014-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.15 Capture the collateral inspection in the field

#### A2.15.1 Intent

**Business objective.** Lets the field officer record the inspection, the checklist and the bills against the case.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Lets the field officer record the inspection, the checklist and the bills against the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Field collector | Opens the screen and capture the collateral inspection in the field | Checks the role, the capability area and the scope |
| 2 | Field collector | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Field app, the Workbench document hub

**Prerequisites.** FEAT-DCM-12

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-015-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-RES-12 | Record the reason against the limit applied, when final_call = rejected | Moves to DECLINED_BY_CREDIT |
| R-SET-09 | Return the case to the officer and re-test against the floor, when counter_amount < floor_price | Moves to WITH_FCR_OFFICER_SET |
| R-SET-23 | Re-open the case and record the reversal against the treatment, when reversal received after release | Moves to PAYMENT_REVERSED |
| BR-S2-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| treatment.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| treatment.decision_log_id | The decision that approved it | uuid | No | None | No |
| treatment.treatment_type | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental | varchar(20) | Yes | LOV-TREATMENT | No |
| treatment.proposed_by | Agent, rule, person | varchar(10) | Yes | LOV-PROPOSER | No |
| treatment.proposed_at | When proposed | timestamptz | Yes | None | No |
| treatment.offer_amount | Amount offered or agreed, baht | numeric(18,2) | No | None | No |
| treatment.haircut_amount | Amount forgiven, baht | numeric(18,2) | No | None | No |
| treatment.installments | Number of installments in a plan | integer | No | None | No |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| Field collector | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-015-01 | Capture the collateral inspection in the field | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-015-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-015-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.16 Set up a deed in lieu buy-back rental

#### A2.16.1 Intent

**Business objective.** Opens the rental record, the auto-debit and the receipt loop where the customer buys back.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Opens the rental record, the auto-debit and the receipt loop where the customer buys back.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Set up a deed in lieu buy-back rental | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** AMIS, ATS

**Prerequisites.** FEAT-TRT-12

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-016-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIL-32 | Create the rental record and set the auto-debit, when customer rents the asset back | Moves to RENTAL_RUNNING |
| BR-S2-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-016-01 | Set up a deed in lieu buy-back rental | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-016-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-016-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.17 Release the collateral after settlement

#### A2.17.1 Intent

**Business objective.** Tells CCMS to release the security once the settlement has cleared, and records the release.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.17.2 Description

**Functional overview.** Tells CCMS to release the security once the settlement has cleared, and records the release.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Release the collateral after settlement | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** CCMS, ALS and GL

**Prerequisites.** FEAT-CHO-08

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-017-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-RES-33 | Close the treatment, release the collateral and close the case, when installments_paid = installments_due | Moves to PLAN_COMPLETED |
| R-SET-20 | Close the account in ALS and request the collateral release, when funds cleared | Moves to COLLATERAL_RELEASE_REQUESTED |
| R-DIL-27 | Record the NPA in AMIS, settle the debt and release the collateral in CCMS, when product = MTG and ownership transferred at the Land Office | Moves to ASSET_ON_BOOKS |
| BR-S2-017 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-017-01 | Release the collateral after settlement | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-017-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-017-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.18 Generate the treatment document set

#### A2.18.1 Intent

**Business objective.** Produces the agreement, contract, credit approval and mortgage documents for the treatment chosen.

**Problem.** Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Restructure turnaround | 5 days | Decision log and Workbench records | Monthly |

#### A2.18.2 Description

**Functional overview.** Produces the agreement, contract, credit approval and mortgage documents for the treatment chosen.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Generate the treatment document set | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, the Workbench document hub

**Prerequisites.** FEAT-OCC-07

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S2-018-1 | Settlement below the floor without approval (R-SET-05) | MSG-S2-001 The offer is below the floor of {floor}. It has been sent for approval. |
| R-DIL-14 | Generate the credit approval, the contract and the mortgage documents, when transfer_price >= floor_price | Moves to OFFER_WITH_CUSTOMER_DIL |
| R-RES-10 | Route the offer to credit approval; 44% of TDR cases deviate today, when offer outside the range or deviation_flag = Y | Moves to AWAITING_CREDIT_APPROVAL |
| R-RES-13 | Escalate to the head of credit, when approval_age > approval_escalation_limit | Moves to AWAITING_CREDIT_APPROVAL |
| BR-S2-018 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR), Legal counsel | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S2-018-01 | Generate the treatment document set | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S2-018-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S2-018-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-S2-001 | A restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench. | Must | E3 |
| REQ-S2-002 | An offer to a customer carries a validity period, and expiry returns the case to the status it came from. | Must | E3 |
| REQ-S2-003 | A signed offer routes to operations for booking, and an unsigned or declined offer returns the case to its prior status. | Must | E3 |
| REQ-S2-004 | Settlement terms are negotiated inside a rule-set range, and anything outside the range needs approval. | Must | E3 |
| REQ-S2-005 | Deed in lieu readiness, including the encumbrance check and an early valuation, is established before negotiation starts. | Must | E3 |
| REQ-S2-006 | The credit application, contract and mortgage documents for a deed in lieu are generated from templates. | Must | E3 |
| REQ-S2-007 | An asset accepted under a deed in lieu is unlocked as a non performing asset by rule, with exceptions summarized for the approver. | Must | E3 |
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying. | Must | E3 |
| REQ-S2-009 | A broken plan raises an event and returns the case to a decision rather than leaving it in a plan state. | Must | E3 |
| REQ-S2-010 | Buyback rental, auto-debit, receipts and arrears follow-up run without a person for a standard arrangement. | Should | E3 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-14 Treatment record | The restructure, settlement or deed in lieu offer, its terms, its status and the booking confirmation | E2 record; E3 full |
| SCR-15 Settlement offer | Payoff, offer range, floor and the gap to the floor | E3 |
| SCR-16 Deed in lieu | Readiness checks, appraisal order, transfer and asset take-on | E3 |

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
| Payoff | ยอดปิดบัญชี | The amount that settles the account on a given date |
| Treatment | แนวทางการแก้ไขที่เสนอ | A resolution put to the customer or carried out on the case |
| Restructure | การปรับโครงสร้างหนี้ | New terms for the debt agreed with the customer |
| Settlement | การชำระหนี้เพื่อปิดบัญชี | Payment of an agreed amount that closes the debt |
| Haircut | ส่วนลดหนี้ | The amount forgiven in a settlement |
| Deed in lieu | การโอนทรัพย์ชำระหนี้ | Transfer of the collateral to the bank in settlement of the debt |
| Buy-back | การซื้อทรัพย์คืน | The customer buying back an asset transferred in lieu |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
