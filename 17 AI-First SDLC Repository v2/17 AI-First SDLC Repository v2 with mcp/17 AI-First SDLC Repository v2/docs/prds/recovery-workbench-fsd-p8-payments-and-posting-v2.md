<!-- working-copy-of: requirement/legacy/03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v4_extracted/recovery-workbench-fsd-p8-payments-and-posting-v2.md -->
> **Working copy.** Canonical source: `requirement/legacy/03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v4_extracted/recovery-workbench-fsd-p8-payments-and-posting-v2.md`. Edit the source, not this copy.

# Recovery Workbench P8 Payments and posting

Functional specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P8 Payments and posting |
| Document ID | P8-RWB-FSD-v2 |
| Version | 2 |
| Status | In review |
| Classification | Confidential |
| Date | 28 October 2026 |
| FSD owner | Business analyst, P8 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| P8 | Payments and posting | E2 matching; E4 |

**Feature scope.** Payment and proceeds matching, fees, posting files.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P8 Payments and posting | TSD | Pair |
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

**In scope.** Payment and proceeds matching, fees, posting files.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-CHO-08; FEAT-CWC-23; FEAT-OCC-10; FEAT-PAY-01; FEAT-PAY-04; FEAT-PAY-06; FEAT-PAY-07; FEAT-RDF-11

**Constraints.** Built in the ACE service as part of the recovery module; data through COLLINS and file loads; every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P8 | FEAT-PAY-01 | Match a payment to a plan installment | System | Matches money received to the installment it pays and updates the plan position. | E2 | A2.1 |
| P8 | FEAT-PAY-02 | Hold an unmatched payment on the exception list | System | Puts money that matches no plan, sale or lot on the exception list for the reconciliation agent. | E2 | A2.2 |
| P8 | FEAT-PAY-03 | Match a settlement payment | System | Matches a settlement payment to the treatment and closes the money side. | E4 | A2.3 |
| P8 | FEAT-PAY-04 | Match auction and enforcement proceeds | System | Matches money from an auction, a broker or the LED to the right case. | E4 | A2.4 |
| P8 | FEAT-PAY-05 | Calculate fees and charges | System | Works out partner fees, court fees and charges from the fee tables held as data. | E4 | A2.5 |
| P8 | FEAT-PAY-06 | Post a settlement booking to ALS | System | Writes the agreed settlement terms to ALS and reads the booked position back. | E4 | A2.6 |
| P8 | FEAT-PAY-07 | Post to the general ledger | System | Posts the accounting entries for settlements, sales and write-offs to the ledger. | E4 | A2.7 |
| P8 | FEAT-PAY-08 | Produce provision inputs | System | Builds the provision inputs Finance needs from the case and asset positions. | E6 | A2.8 |
| P8 | FEAT-PAY-09 | Run the deed in lieu rental auto-debit | System | Takes the rental by auto-debit, issues the receipt and follows up arrears. | E4 | A2.9 |
| P8 | FEAT-PAY-10 | Apply proceeds to the case balance | System | Applies every receipt to the balance in the order the policy sets. | E4 | A2.10 |
| P8 | FEAT-PAY-11 | Reconcile money movements daily | System | Compares what the Workbench matched to what ALS and the ledger show, every day. | E4 | A2.11 |

### A1.3 Background

Payments are matched to plans and settlements by hand; broken plans are found late.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Match a payment to a plan installment

#### A2.1.1 Intent

**Business objective.** Matches money received to the installment it pays and updates the plan position.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Matches money received to the installment it pays and updates the plan position.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Match a payment to a plan installment | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-OCC-10

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-001-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-001-01 | Payment matched | the ALS load for business date 2026-12-14 holds payment "PAY-90001" of 12,500.00 THB on account "A-0555" dated 2026-12-14 | JOB-07 runs on 2026-12-15 | a proceeds row exists for case "RC-2026-000555" with treatment "T-0701", source "CUSTOMER", amount 12,500.00 and matched to "INSTALLMENT" And TreatmentApi.recordInstallmentPaid is called for "T-0701" with due date 2026-12-15 And ProceedsMatched is written to the outbox And after the ALS load of 2026-12-15 the plan shows installments paid 4 and next due date 2027-01-15 | RWB-E2-008 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P8-001-01 | Missed payment | no payment on account "A-0555" was loaded between 2026-12-05 and 2026-12-15 | JOB-07 runs on 2026-12-16 for business date 2026-12-15 | PaymentMissed is written to the outbox with treatment "T-0701", due date 2026-12-15 and amount due 12,500.00 And P3 moves plan "T-0701" from "PLAN_RUNNING" to "PLAN_CURE_PERIOD" under rule R-RES-27 And the transfer rule records the case movement for reason "payment missed" | RWB-E2-008 |
| AC-ALT-P8-001-02 | Window boundary | plan "T-0702" on account "A-0666" of case "RC-2026-000566" has installment amount 12,500.00 THB and next installment date 2026-12-16 And the ALS load for business date 2026-12-05 holds payment "PAY-90004" of 12,500.00 THB on account "A-0555" dated 2026-12-05 And the same load holds payment "PAY-90005" of 12,500.00 THB on account "A-0666" dated 2026-12-05 | JOB-07 runs on 2026-12-06 | "PAY-90004", 10 days before its due date, is matched to "INSTALLMENT" for "T-0701" And "PAY-90005", 11 days before its due date, is matched to "UNMATCHED" | RWB-E2-008 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-001-01 | Exception | the ALS load for business date 2026-12-14 holds payment "PAY-90002" of 3,000.00 THB on account "A-0555" | JOB-07 runs on 2026-12-15 | a proceeds row exists for "PAY-90002" with matched to "UNMATCHED" and no treatment And GET /proceeds?matched=false returns "PAY-90002" for the Credit Administration officer And the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14 | RWB-E2-008 |
| AC-EXC-P8-001-02 | Payment on an account with no open case | the ALS load holds payment "PAY-90003" on account "A-0999" that is on no open case | JOB-07 runs on 2026-12-15 | no proceeds row is written for "PAY-90003" And "PAY-90003" is held on the data quality exception list with check "References" | RWB-E2-008 |
| AC-EXC-P8-001-03 | ALS load refused | the ALS load for business date 2026-12-15 was refused at check "control total" | the scheduled time for JOB-07 on 2026-12-16 passes | JOB-07 does not run for business date 2026-12-15 And no PaymentMissed is written for due date 2026-12-15 And the plan view shows MSG-P1-001 naming "DP01 Account and arrears" and 2026-12-14 | RWB-E2-008 |
| AC-EXC-P8-001-04 | Repeated run | JOB-07 completed for business date 2026-12-14 with 1 matched and 1 unmatched payment | JOB-07 is rerun for business date 2026-12-14 from SCR-44 | the proceeds table still has 2 rows for business date 2026-12-14 And no second ProceedsMatched or PaymentMissed is written | RWB-E2-008 |
| AC-EXC-P8-001-05 | No parameter row in force | no payment matching parameter row is valid on 2026-12-15 | JOB-07 starts for business date 2026-12-15 | it stops before matching with MSG-P8-002 And no proceeds row and no event is written And the job monitor shows JOB-07 as failed with an alert to Credit Administration | RWB-E2-008 |
| AC-EXC-P8-001-06 | Late payment inside and outside the window | the ALS load for 2026-12-18 holds payment "PAY-91004" of 12,500.00 THB on account "A-0555", 3 days after due date 2026-12-15 And the same load holds payment "PAY-91005" of 12,500.00 THB on account "A-0666" of plan "T-0702", 4 days after its due date 2026-12-14 | JOB-07 runs on 2026-12-19 | "PAY-91004" is matched with row "WINDOW" and P3 receives PAYMENT_RECEIVED_LATE under R-RES-28 And "PAY-91005" is matched to "UNMATCHED" with a decision log entry under rule "R-UNI-03" | RWB-E2-027 |
| AC-EXC-P8-001-07 | Invalid parameter load refused | a parameter file for version "PM-2027.02" where rows "WINDOW" and "PARTIAL" both have priority 2 and "PARTIAL" has tolerance 120 | it is loaded through POST /admin/reference-loads | the response is status 422 with MSG-GEN-002 naming "amount_tolerance_pct", 0 and 100 And the load is refused whole and "PM-2026.12" stays in force | RWB-E2-027 |
| AC-EXC-P8-001-08 | Decision log write fails | the decision log store is unavailable during JOB-07 on 2026-12-15 | "PAY-91001" is matched | no proceeds row is written for "PAY-91001" And the run summary shows MSG-P7-003 for "PAY-91001" And an incident is raised under rule R-UNI-39 And the next run of JOB-07 for 2026-12-14 matches "PAY-91001" | RWB-E2-027 |
| AC-EXC-P8-001-09 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-001-10 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-001-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

### A2.2 Hold an unmatched payment on the exception list

#### A2.2.1 Intent

**Business objective.** Puts money that matches no plan, sale or lot on the exception list for the reconciliation agent.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Puts money that matches no plan, sale or lot on the exception list for the reconciliation agent.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Hold an unmatched payment on the exception list | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, Workbench

**Prerequisites.** FEAT-PAY-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-002-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-002-01 | Payment matched | the ALS load for business date 2026-12-14 holds payment "PAY-90001" of 12,500.00 THB on account "A-0555" dated 2026-12-14 | JOB-07 runs on 2026-12-15 | a proceeds row exists for case "RC-2026-000555" with treatment "T-0701", source "CUSTOMER", amount 12,500.00 and matched to "INSTALLMENT" And TreatmentApi.recordInstallmentPaid is called for "T-0701" with due date 2026-12-15 And ProceedsMatched is written to the outbox And after the ALS load of 2026-12-15 the plan shows installments paid 4 and next due date 2027-01-15 | RWB-E2-008 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P8-002-01 | Missed payment | no payment on account "A-0555" was loaded between 2026-12-05 and 2026-12-15 | JOB-07 runs on 2026-12-16 for business date 2026-12-15 | PaymentMissed is written to the outbox with treatment "T-0701", due date 2026-12-15 and amount due 12,500.00 And P3 moves plan "T-0701" from "PLAN_RUNNING" to "PLAN_CURE_PERIOD" under rule R-RES-27 And the transfer rule records the case movement for reason "payment missed" | RWB-E2-008 |
| AC-ALT-P8-002-02 | Window boundary | plan "T-0702" on account "A-0666" of case "RC-2026-000566" has installment amount 12,500.00 THB and next installment date 2026-12-16 And the ALS load for business date 2026-12-05 holds payment "PAY-90004" of 12,500.00 THB on account "A-0555" dated 2026-12-05 And the same load holds payment "PAY-90005" of 12,500.00 THB on account "A-0666" dated 2026-12-05 | JOB-07 runs on 2026-12-06 | "PAY-90004", 10 days before its due date, is matched to "INSTALLMENT" for "T-0701" And "PAY-90005", 11 days before its due date, is matched to "UNMATCHED" | RWB-E2-008 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-002-01 | Exception | the ALS load for business date 2026-12-14 holds payment "PAY-90002" of 3,000.00 THB on account "A-0555" | JOB-07 runs on 2026-12-15 | a proceeds row exists for "PAY-90002" with matched to "UNMATCHED" and no treatment And GET /proceeds?matched=false returns "PAY-90002" for the Credit Administration officer And the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14 | RWB-E2-008 |
| AC-EXC-P8-002-02 | Payment on an account with no open case | the ALS load holds payment "PAY-90003" on account "A-0999" that is on no open case | JOB-07 runs on 2026-12-15 | no proceeds row is written for "PAY-90003" And "PAY-90003" is held on the data quality exception list with check "References" | RWB-E2-008 |
| AC-EXC-P8-002-03 | ALS load refused | the ALS load for business date 2026-12-15 was refused at check "control total" | the scheduled time for JOB-07 on 2026-12-16 passes | JOB-07 does not run for business date 2026-12-15 And no PaymentMissed is written for due date 2026-12-15 And the plan view shows MSG-P1-001 naming "DP01 Account and arrears" and 2026-12-14 | RWB-E2-008 |
| AC-EXC-P8-002-04 | Repeated run | JOB-07 completed for business date 2026-12-14 with 1 matched and 1 unmatched payment | JOB-07 is rerun for business date 2026-12-14 from SCR-44 | the proceeds table still has 2 rows for business date 2026-12-14 And no second ProceedsMatched or PaymentMissed is written | RWB-E2-008 |
| AC-EXC-P8-002-05 | No parameter row in force | no payment matching parameter row is valid on 2026-12-15 | JOB-07 starts for business date 2026-12-15 | it stops before matching with MSG-P8-002 And no proceeds row and no event is written And the job monitor shows JOB-07 as failed with an alert to Credit Administration | RWB-E2-008 |
| AC-EXC-P8-002-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-002-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-002-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

### A2.3 Match a settlement payment

#### A2.3.1 Intent

**Business objective.** Matches a settlement payment to the treatment and closes the money side.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Matches a settlement payment to the treatment and closes the money side.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Match a settlement payment | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-PAY-01

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-003-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-003-01 | Match a settlement payment | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-003-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-003-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-003-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

### A2.4 Match auction and enforcement proceeds

#### A2.4.1 Intent

**Business objective.** Matches money from an auction, a broker or the LED to the right case.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Matches money from an auction, a broker or the LED to the right case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Match auction and enforcement proceeds | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, LED portal

**Prerequisites.** FEAT-PAY-01

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-004-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-004-01 | Match auction and enforcement proceeds | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-004-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-004-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-004-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

### A2.5 Calculate fees and charges

#### A2.5.1 Intent

**Business objective.** Works out partner fees, court fees and charges from the fee tables held as data.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Works out partner fees, court fees and charges from the fee tables held as data.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Calculate fees and charges | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, ALS and GL

**Prerequisites.** FEAT-CWC-23

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-005-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Finance and CFO delegate | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-005-01 | Calculate fees and charges | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-005-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-005-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-005-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

### A2.6 Post a settlement booking to ALS

#### A2.6.1 Intent

**Business objective.** Writes the agreed settlement terms to ALS and reads the booked position back.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Writes the agreed settlement terms to ALS and reads the booked position back.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Post a settlement booking to ALS | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-CHO-08

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-006-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Credit Administration officer | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-006-01 | Post a settlement booking to ALS | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-006-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-006-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-006-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

### A2.7 Post to the general ledger

#### A2.7.1 Intent

**Business objective.** Posts the accounting entries for settlements, sales and write-offs to the ledger.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Posts the accounting entries for settlements, sales and write-offs to the ledger.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Post to the general ledger | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-PAY-06

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-007-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Credit Administration officer | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-007-01 | Post to the general ledger | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-007-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-007-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-007-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

### A2.8 Produce provision inputs

#### A2.8.1 Intent

**Business objective.** Builds the provision inputs Finance needs from the case and asset positions.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Builds the provision inputs Finance needs from the case and asset positions.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Produce provision inputs | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-PAY-07

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-008-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Finance and CFO delegate | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-008-01 | Produce provision inputs | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-008-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-008-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-008-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

### A2.9 Run the deed in lieu rental auto-debit

#### A2.9.1 Intent

**Business objective.** Takes the rental by auto-debit, issues the receipt and follows up arrears.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Takes the rental by auto-debit, issues the receipt and follows up arrears.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the deed in lieu rental auto-debit | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ATS, AMIS

**Prerequisites.** FEAT-TRT-16

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-009-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-009-01 | Run the deed in lieu rental auto-debit | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-009-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-009-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-009-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

### A2.10 Apply proceeds to the case balance

#### A2.10.1 Intent

**Business objective.** Applies every receipt to the balance in the order the policy sets.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Applies every receipt to the balance in the order the policy sets.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Apply proceeds to the case balance | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-PAY-04

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-010-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-010-01 | Apply proceeds to the case balance | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-010-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-010-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-010-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

### A2.11 Reconcile money movements daily

#### A2.11.1 Intent

**Business objective.** Compares what the Workbench matched to what ALS and the ledger show, every day.

**Problem.** Payments are matched to plans and settlements by hand; broken plans are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Receipts matched the same day | Rising each month | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Compares what the Workbench matched to what ALS and the ledger show, every day.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Reconcile money movements daily | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-RDF-11

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P8-011-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P8-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Credit Administration officer | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P8-011-01 | Reconcile money movements daily | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P8-011-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P8-011-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P8-011-01 | Payment matching | Load complete | Daily | Matches payments to plans | Missed payments raised the next morning | Broken plans are found the day after |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-28 Proceeds matching | Receipts matched to cases and the unmatched list | E2 skeleton; E4 full |
| SCR-29 Posting | Approved bookings and postings with the confirmation from the next load | E4 |

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
| Proceeds | เงินที่ได้รับ | Money received on a case and what it was matched to |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
