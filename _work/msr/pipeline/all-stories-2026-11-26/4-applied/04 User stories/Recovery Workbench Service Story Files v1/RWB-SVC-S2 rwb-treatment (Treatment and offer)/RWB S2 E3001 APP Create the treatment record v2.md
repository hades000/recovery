# RWB-S2-E3001-APP Create the treatment record

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-001 for rwb-treatment (S2). The stage becomes `TreatmentWorkflow`, the child of `CaseWorkflow` on this service's own task queue, opened by the `openTreatment` activity; the treatment row and its local decision record are written in one `rwb_treatment` transaction through the RWB-PLT-E1027-CON library (DP-03); the base becomes `/api/recovery/treatment/v1` (DP-13) and SCR-14 and SCR-15 are reached through the gateway-bff composite route (DP-19). The four legacy acceptance criteria are copied verbatim with one contract mock line added to AC2 and AC3. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E3001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S2-L |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3001-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the Workbench to open the treatment for the chosen route as the first step of `TreatmentWorkflow` on task queue `rwb-treatment` — holding the treatment type, the proposer and the dates in one `treatment` row of `rwb_treatment`, holding the approval and the outcome as columns of the same row, writing the local decision record with the rule ID and the rule version in the same transaction, and reporting the R-RES-01 or R-RES-10 outcome to the parent `CaseWorkflow` that owns and moves the case status**, so that **restructures, settlements and deeds in lieu reach booking in days instead of the 23 to 26 days they take today**.

This is the application slice of legacy RWB-E3-001, and it opens the treatment stage of the epic. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules R-RES-01 and R-RES-10, the messages, the screens and the data rows they depend on;
- `TreatmentWorkflow`, the stage child of `CaseWorkflow` (rwb-case), started on this service's own queue `rwb-treatment` in namespace `rwb-recovery`, with its `openTreatment` and `recordAndApply` activities (DP-12; Architecture v5 slide 18; Temporal and Drools Design slides 13 and 18);
- `POST /cases/{caseId}/treatments` (right C, `Idempotency-Key`) and `GET /treatments/{treatmentId}` (right R) on base `/api/recovery/treatment/v1`, which write and read the `treatment` row (DP-13);
- the writer of `treatment` in schema `rwb_treatment`, from DF-TRT-001 to DF-TRT-033, created by this story's Flyway version (DP-01);
- the local decision record of the open, written through the RWB-PLT-E1027-CON library inside the caller's transaction, with the rule ID and the rule version the evaluated package returned (DP-03);
- the outcome report of the stage to the parent `CaseWorkflow`: the case status the stage's rules imply, handed to the parent, which moves it; this service writes no case table (DP-01).

It does not own: the published shape of the two operations and the `treatment` DDL template, which are RWB-S2-E3001-CON; the settlement offer and its range, which are RWB-S2-E3002-APP; the approval of an offer below the floor, which is RWB-S2-E3003-APP; the TDR plan, its installments and its plan timers, which are RWB-S2-E3004-APP; the ACE affordability pre-assessment, which is RWB-S2-E3005-APP; the case status, the `CaseWorkflow` and the case table, which are rwb-case's (P3); the RESTRUCTURE, SETTLEMENT and DEEDINLIEU packages and their rows, which are rwb-decision's (P7); the roles, rights and scope data, which are rwb-access's (P4); the gateway-bff composite route and the screen field list, which are the platform edge story's and the screen owners'.

### 2. Business rationale

A restructure, a settlement and a deed in lieu are the three ways a case leaves collections with a promise instead of a loss, and each of them begins with one decision: which treatment is opened for the route the case is on. The legacy story opened that record inside the monolith: the treatment row, the decision-log row, the case state and the case's business tables were all in the one `recovery` schema and all written by one service method. Its business objective is fixed and unchanged — open the treatment for the chosen route, holding the terms, the approval and the outcome, with a restructure turnaround target of 5 days measured from the decision log and the Workbench records (FSD S2 A2.1.1).

What D-RCV-60 changes is where the record lives, who moves the case and how the answer is reached. In the target the treatment is a row of `rwb_treatment`, owned by rwb-treatment (S2), and the stage that opens it is `TreatmentWorkflow` on task queue `rwb-treatment`, the child of `CaseWorkflow` (Architecture v5 slides 18 and 41; Temporal and Drools Design slides 13 and 18). The case status is not this service's: rwb-treatment reports the stage outcome to the parent `CaseWorkflow` on rwb-case, and the parent moves the status (ASM-3062). That single ruling is what keeps the case of record in one place, and it is why the legacy lines of AC2 and AC3 that describe a case moving are asserted against the parent and not against a case table here.

The decision record moves with the write. The monolith wrote `decision_log_entry` in the same schema and copied it to the data lake; the target writes a local `decision_record` in the service's own schema, in the same transaction as the treatment row, and publishes it through the shared topic to the central ledger of rwb-decision (DP-03; Architecture v5 slides 20 and 28; ADR-022). A treatment that could be stored without its record is exactly what REQ-DRI-005 forbids, so the record write is part of this story and not a later step.

The third change is the base and the screen. The legacy `/api/recovery/v1` base becomes `/api/recovery/treatment/v1` (DP-13), so treatment calls no longer share a path namespace with the case, the payment and the guarantee services, and SCR-14 Treatment record and SCR-15 Settlement offer are composed by the gateway-bff composite route rather than by a screen reading one database (DP-19).

Serves REQ-S2-001: a restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench. No business value is invented or moved: the states, the rules, the list values, the message texts and the rights are the values the FSD, the rule workbook and the TSD already carry, read in force.

### 3. Preconditions

- RWB-S2-E3001-CON is published: base `/api/recovery/treatment/v1`, `POST /cases/{caseId}/treatments` with `TreatmentRequest` and `Treatment`, `GET /treatments/{treatmentId}` with `Treatment`, the error set with the RFC 9457 problem body, the `Idempotency-Key` header, the `treatment` DDL template and the fakes. This story builds against that contract and its fake and never against rwb-case or rwb-decision.
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter.record(DecisionRecord)` declared with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003, and the `decision_record` DDL template applied in this service's own schema (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14 and SCR-15 from the case read and the treatment read, one hop each, read only (DP-19).
- The `rwb_treatment` schema and login exist from the platform database story, and this service's Flyway sequence is at the version that carries the library tables; this story adds `treatment` on the same sequence and never edits an applied migration (DP-15).
- The workflow kit is in place on task queue `rwb-treatment` in namespace `rwb-recovery`, and `CaseWorkflow` of rwb-case starts this stage as a child on that queue with parent close policy ABANDON (ASM-3064; Temporal and Drools Design slide 13).
- Package RESTRUCTURE is in force for the business date with rows R-RES-01 and R-RES-10, each row carrying its condition, its action text and its timer spec; the package and its version arrive from rwb-decision on `rwb.decision.RulePackageInForce.v1` and are evaluated by the embedded Drools runtime of the service template, which adds no build dependency of its own (ASM-3063; Temporal and Drools Design slides 13 and 15).
- The lists LOV-TREATMENT, LOV-PROPOSER, LOV-TRT-OUTCOME, LOV-APPROVAL-LEVEL and LOV-TRT-SIGNATURE are values in force and are read as data with their version; no member of any list is written in code (BR-S2-001; TSD S2 T3.2).
- The case status of a case is readable only as the case signal the parent `CaseWorkflow` forwards to this stage; this service reads no case row and holds no case table (ASM-3062; DP-01).
- No approval is needed to build against a Draft contract baseline, and a CON story is Day 1 by rule: this story starts on Day 1 with only CON build dependencies (§R5.7).

### 4. Flow

1. The route decision of rwb-valuation ends with the case in ROUTE_APPROVED_RESTRUCTURE for route R1, ROUTE_APPROVED_SETTLEMENT for R2 or ROUTE_APPROVED_DIL for R3; the case router of rwb-case signals `CaseWorkflow`, which starts the treatment stage as a child workflow on queue `rwb-treatment` (Architecture v5 slide 18; Temporal and Drools Design slides 13 and 14).
2. `TreatmentWorkflow` starts with the case ID, the route, the business date and the package in force; the workflow ID is derived from the case ID and the stage, so a redelivered start raises no second execution.
3. The workflow asks the embedded Drools runtime for the RESTRUCTURE package version in force and evaluates it with the case facts the case signal carries: the state, the route, the decision and the deviation flag.
4. R-RES-01 fires on a case in ROUTE_APPROVED_RESTRUCTURE with the event ROUTE_APPROVED and the condition `decision.approved and route = R1`; its action is to open the treatment record, and its target state is PROPOSED_IN_COLLINS.
5. `openTreatment` activity: builds the `TreatmentRequest` and calls the service's own create operation in process — `treatment_type` from LOV-TREATMENT, `proposed_by` from LOV-PROPOSER, `proposed_at` the business time, `case_id` the case of the signal, `installments_paid` zero for a plan that has not started — so the row is written by the same service method the officer's screen uses and there is one write path.
6. `recordAndApply` activity: writes, in one `rwb_treatment` transaction, the `treatment` row with the reviewed values, its `state`, its standard columns, the `decision_record` row through `DecisionRecordWriter.record` with the rule ID R-RES-01 and the package version, the outbox rows and the idempotency row of the request.
7. The activity returns the stage outcome to the parent `CaseWorkflow`: the rule ID, the package version, the treatment ID and the target state the rule names. The parent moves the case status to PROPOSED_IN_COLLINS; this service writes nothing to a case table. The shape of that outcome report is Not specified in the source documents (GAP-1869; ASM-3065), and this story adopts the returned child-workflow result as its working read.
8. R-RES-10 fires on a case in WITH_FCR_OFFICER with the event OFFER_PREPARED and the condition `offer outside the range or deviation_flag = Y`; its action is to route the offer to credit approval, and its target state is AWAITING_CREDIT_APPROVAL. The stage reports that target state to the parent in the same way; the offer body itself is built by RWB-S2-E3002-APP.
9. The officer, or the case owner, reads the treatment through `GET /treatments/{treatmentId}`; the read is answered from `rwb_treatment` and carries the terms, the state and the references the row holds.
10. The parent `CaseWorkflow` continues with the next stage while this child waits; at the stage end the child completes and the parent's Continue-As-New keeps the case run inside the history limits of the design.
11. A repeated request with the same `Idempotency-Key` returns the first answer and writes no second row, no second record and no second outbox row.
12. SCR-14 and SCR-15 read the treatment through the gateway-bff composite route, which composes the case read of rwb-case and this service's treatment read in one hop each (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without Treatment and offer C calls the create operation | 403; the refusal is the platform guard library's answer and the service log records the role and the operation, never a personal field | MSG-P4-002 | AC1, AC4 |
| X2 | A case ID that does not answer on the case signal, or a treatment ID that does not exist | 404 with the problem body; nothing is written and no record is created | MSG-P4-003 | Section 12.1 |
| X3 | The local decision record cannot be written | The transaction rolls back: no treatment row, no outbox row, no idempotency row; the user sees MSG-P7-003 and the call is retried with the same key | MSG-P7-003 | AC4 |
| X4 | A field of the request is missing or outside its list | 422 with MSG-P7-009 naming the field; the row is not written | MSG-P7-009, MSG-GEN-001 | AC1 |
| X5 | The same `Idempotency-Key` arrives twice | The first answer is returned and the repeat is counted; no second row, record or event | None | AC1 |
| X6 | No RESTRUCTURE version is in force for the business date | The stage ends with the package refusal it received, reports no target state and writes nothing; the case keeps its status | MSG-P7-003 | AC2 |
| X7 | The case signal names a status other than the one a rule expects | No rule fires, no treatment is opened and the stage waits on the next signal; nothing is written | None | AC2, AC3 |
| X8 | The COLLINS side of R-RES-01 is not reachable | Nothing is asked of COLLINS: no live COLLINS call is published for S2, so the approved route with its expected-return facts is taken from the case signal, and the proposal step of R-RES-02 follows in rwb-case's flow | None | AC2, section 19 |

X1 to X5 are the paths of the legacy story carried onto the split; X6 and X7 are the refusal and the unmatched-signal paths the workflow model adds; X8 is the realignment of the COLLINS call, which the target does not make from this service (GAP-1869; ASM-3065). A refusal under X1, X2 or X4 writes nothing at all, because the guard and the validator run before the transaction opens.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-S2-E3001-CON fake, the decision-record writer fake and the composite-route fake; needs no live rwb-case, rwb-decision or COLLINS |
| Negotiable | The activity names, the workflow ID derivation, the module split and the flag name are this story's choice; the rules, the states, the lists, the rights and the messages are fixed |
| Valuable | The treatment is opened in days, on the right case, with the record that says which rule and which version decided it, and the case status stays in one place |
| Estimable | One child workflow, two activities, one resource with two operations, one repository, one migration, one library adapter |
| Small | Fits two weeks with its tests |
| Testable | Each criterion of section 7 is one automated test; the parent, the package and the guard are stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Create the treatment record

  Scenario: AC1 Create the treatment record (legacy RWB-E3-001 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then opens the treatment for the chosen route, holding the terms, the approval and the outcome
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-01 (legacy RWB-E3-001 AC2)
    Given the rwb-case contract mock returns case status ROUTE_APPROVED_RESTRUCTURE
    Given a case in state ROUTE_APPROVED_RESTRUCTURE
    When route approved
    Then open the treatment record and ask COLLINS for the restructure proposal
    Then the case moves to PROPOSED_IN_COLLINS

  Scenario: AC3 Rule R-RES-10 (legacy RWB-E3-001 AC3)
    Given the rwb-case contract mock returns case status WITH_FCR_OFFICER
    Given a case in state WITH_FCR_OFFICER
    When offer prepared
    Then route the offer to credit approval; 44% of TDR cases deviate today
    Then the case moves to AWAITING_CREDIT_APPROVAL

  Scenario: AC4 Not recorded (legacy RWB-E3-001 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line is kept character for character, including the legacy repetition of `Then`; what changes is who produces each fact and where it is asserted. The trigger of AC1 is no longer a monolith request but the start of `TreatmentWorkflow` on task queue `rwb-treatment`, the child of `CaseWorkflow` (Temporal and Drools Design slides 13 and 18; Architecture v5 slide 18), and "the data and the rule version this feature needs are in place" is the RESTRUCTURE package version announced on `rwb.decision.RulePackageInForce.v1` and the list values in force (ASM-3063). "The system writes the result to the decision log with the rule version" is the local `decision_record` row written in the same `rwb_treatment` transaction through the RWB-PLT-E1027-CON library, hash-linked and published to the central ledger of P7 (DP-03; ASM-3065). In AC2 and AC3 the state is the case's, so the line that names a case state is asserted against the parent `CaseWorkflow` of rwb-case, which the added `Given the rwb-case contract mock returns case status ...` line stands in for; this service holds no case table and no status column (ASM-3062; DP-01). The COLLINS half of AC2 is a realignment point: no live COLLINS call is published for S2, so the approved route and its expected-return facts arrive on the case signal, and the restructure proposal itself is asked by the rwb-case flow that owns R-RES-02 (GAP-1869; ASM-3065). The approval of AC3 — "route the offer to credit approval" — is reported to the parent as the target state AWAITING_CREDIT_APPROVAL and the approval record is RWB-S2-E3003-APP's. The decision-log failure of AC4 is the library's MSG-P7-003, and the "nothing changes" is the rollback of one transaction that also holds the treatment row and the outbox rows (DP-03). Both operations sit on base `/api/recovery/treatment/v1` (DP-13), and SCR-14 and SCR-15 reach them through the gateway-bff composite route (DP-19).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The stage opens the treatment for the route the case is on: R1 restructure, R2 settlement, R3 deed in lieu, with `treatment_type` taken from LOV-TREATMENT | FEAT-TRT-01; FSD S2 A2.1.1, A2.1.2; TSD S2 T3.2 |
| BR2 | A case in ROUTE_APPROVED_RESTRUCTURE with ROUTE_APPROVED and `decision.approved and route = R1` opens the treatment record; its target state is PROPOSED_IN_COLLINS | R-RES-01; TSD S2 T4 |
| BR3 | A case in WITH_FCR_OFFICER with OFFER_PREPARED and `offer outside the range or deviation_flag = Y` routes the offer to credit approval; its target state is AWAITING_CREDIT_APPROVAL | R-RES-10; TSD S2 T4 |
| BR4 | The result is written to the decision record with the rule ID and the rule version the evaluated package returned | legacy RWB-E3-001 AC1; DP-03 |
| BR5 | A decision that cannot be recorded does not proceed: the record, the row and the outbox rows are one transaction, and the user sees MSG-P7-003 | Principle 5; legacy RWB-E3-001 AC4; REQ-DRI-005 |
| BR6 | The case status stays rwb-case's: this stage reports its outcome to the parent `CaseWorkflow`, which moves the status, and this service writes no case table | ASM-3062; DP-01 |
| BR7 | No value a business person may change is written in code: the rules, the states, the timers and the lists are values in force read with their version | BR-S2-001; FSD S2 A2.1.3.1 |
| BR8 | No treatment row exists without its decision record, and a repeated request key writes one row, one record and one outbox row | DP-03; legacy RWB-E3-001 AC1, AC4 |
| BR9 | The right is declared and not re-implemented: create needs Treatment and offer C, read needs Treatment and offer R, and the check is the platform guard library's | TSD S2 T6.1; Template and Rules §R5.5 DP-08, the guard being a template capability (ASM-3064) |
| BR10 | The decision code of a treatment event carries no published list; the rule ID and the rule version are carried instead, as values in force | GAP-1869; ASM-3065 |

**Where each rule lives in the target.** BR1 and BR2 are the `openTreatment` activity and the `R-RES-01` row of the evaluated package. BR3 is the report the stage makes after the offer step; the offer terms themselves are written by RWB-S2-E3002-APP, so this story carries the outcome and not the offer. BR4 and BR5 are the `recordAndApply` activity and the library. BR6 is the child-workflow return and the parent. BR7 is the reference-data reads and the Drools runtime. BR8 is the idempotency key and the one transaction. BR9 is the contract's `security` section and the guard, and no check is written in this service. BR10 records that the decision code of an event has no published code list, so the rule ID and the rule version stand in its place.

### 9. State transitions

None of the transitions below is a case status owned here: each row is the stage outcome this service reports, and the status itself is moved by the parent `CaseWorkflow` on rwb-case (ASM-3062; DP-01).

| From (case status on the signal) | Event | Condition | Reported target state |
|---|---|---|---|
| ROUTE_APPROVED_RESTRUCTURE | ROUTE_APPROVED | R-RES-01: `decision.approved and route = R1` | PROPOSED_IN_COLLINS |
| WITH_FCR_OFFICER | OFFER_PREPARED | R-RES-10: `offer outside the range or deviation_flag = Y` | AWAITING_CREDIT_APPROVAL |
| WITH_FCR_OFFICER | OFFER_PREPARED | R-RES-09: `offer inside the approved range and deviation_flag = N` | OFFER_WITH_CUSTOMER, by RWB-S2-E3002-APP |
| ROUTE_APPROVED_SETTLEMENT, ROUTE_APPROVED_DIL | ROUTE_APPROVED | R-SET-01, R-DIL-01: the same open step on the other two routes | Set by the settlement and deed-in-lieu rows, not by this story |
| any of the above | no rule fired | The signal names a state or an event no row expects | None reported; the stage waits |

The `treatment` row has its own lifecycle in the `state` column: the legacy screen states Draft, submitted, approved, booked and broken are the names SCR-14 shows, and this story writes Draft at open. The stage execution itself is RUNNING, COMPLETED or FAILED in the workflow history, and a failed execution is retried on the platform policy, 1 s initial interval with back-off 2 and 10 attempts, with the package refusal non-retryable.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-treatment squad, service identity of `rwb_treatment` | Runs the stage, writes the treatment row, the decision record and the outbox rows |
| RW-CASEOWN, case owner (CRU) | Opens and reads a treatment on cases in scope |
| RW-RESTRUCT, restructuring officer (CRUA) | Opens, reads, changes and submits a treatment on cases in scope; the primary role of the story |
| RW-SPECIAL, hardship and vulnerability specialist (CRU) | Opens and reads a treatment on cases in scope |
| RW-GUARANT, guarantee officer (CRU) | Opens and reads a treatment on the guarantee claims in scope |
| RW-TEAMMGR, team manager (R) | Reads the treatments of the team's cases |
| RW-PRODHEAD, product head (RA); RW-CREDCOMM, credit approval committee member (RA) | Reads and approves within the delegation of authority; the approval itself is RWB-S2-E3003-APP's |
| The other reading roles of TSD S2 T6.1 — RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE (R) | Read the treatment on cases in scope |
| SY-CASEWF, SY-RULES, SY-AGENT (R) | Read as service identities through the same checks |
| rwb-case (P3) | Owns `CaseWorkflow`, the case status and the case signal; moves the status this stage reports |
| rwb-decision (P7) | Owns the RESTRUCTURE package, its rows and its version, and publishes `RulePackageInForce` |
| rwb-access (P4) | Owns the rights, the roles and the scope data the guard library answers with |
| No delegation of authority level applies | The story opens a record and reports an outcome; it approves nothing |

No credential and no personal name appears in the request, the row, the workflow input, the record or the logs. Where a person must be named the row carries the user identifier of the proposer, never a name, and the masking of the personal fields of the case is the platform edge's.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Write |
| DF-TRT-002 | treatment | case_id | Write |
| DF-TRT-003 | treatment | decision_log_id (the ID of the local decision record of this write) | Write |
| DF-TRT-004 | treatment | treatment_type | Write |
| DF-TRT-005 | treatment | proposed_by | Write |
| DF-TRT-006 | treatment | proposed_at | Write |
| DF-TRT-007 | treatment | offer_amount | Write, nullable: left null at open and set by RWB-S2-E3002-APP |
| DF-TRT-008 | treatment | haircut_amount | Write, nullable: set by the settlement story |
| DF-TRT-009 | treatment | installments | Write, nullable: set by RWB-S2-E3004-APP |
| DF-TRT-010 | treatment | valid_until | Write, nullable: set by the offer story |
| DF-TRT-011 | treatment | approval_level | Write through RWB-S2-E3003-APP |
| DF-TRT-012 | treatment | booked_at | Not written here: set when operations confirm the booking |
| DF-TRT-013 | treatment | outcome | Write, nullable: set when the outcome is recorded |
| DF-TRT-014 | treatment | outcome_at | Write, nullable: set with the outcome |
| DF-TRT-023 | treatment | nleads_ref | Not written here: recorded with the NLEADS submission |
| DF-TRT-024, DF-TRT-025, DF-TRT-026 | treatment | credit_result, credit_result_reason, credit_result_at | Not written here: the credit result is the credit-approval story's |
| DF-TRT-027, DF-TRT-028, DF-TRT-029 | treatment | interest_rate, booking_difference, first_due_date | Not written here: the plan and booking stories write them |
| DF-TRT-030 | treatment | signature_status | Not written here: the signature story writes it |
| DF-TRT-031, DF-TRT-032, DF-TRT-033 | treatment | installment_amount, installments_paid, installment_shortfall | Write: `installments_paid` is required and is written as zero at open; the other two are null until the plan starts |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, in `rwb_treatment`) | all fields through `DecisionRecordWriter.record` | Write, in the same transaction (DP-03) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (`rwb_case`, owner P3) | the case and its status | Not read and not written: the status arrives on the case signal (ASM-3062) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (`rwb_decision`, owner P7) | the central ledger entry | Not written and not read here: P7 seals it from the shared topic (DP-03) |
| DF-REF-001 to DF-REF-015 | rule_row (`rwb_decision`, owner P7) | the rule row of R-RES-01 and R-RES-10 | Not read directly: the evaluated package returns the row outputs |

`treatment` is the only table this story creates, from DF-TRT-001 to DF-TRT-033 as TSD S2 T3.1 lists them. Architecture v5 slide 41 also places contracts, settlement and deed-in-lieu agreements and plan timers in `rwb_treatment`, but the TSD gives them no table and no field list; their shape is Not specified in the source documents (GAP-1869; ASM-3065) and they are created by the sibling stories that own them, RWB-S2-E3002-APP and RWB-S2-E3004-APP. DF-TRT-015 to DF-TRT-022 name the guarantee claim, which is rwb-guarantee's table in `rwb_guarantee` and is neither read nor written here. No foreign key crosses a schema and no row of another service's table is joined (DP-01).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story supplies both operations and their handlers; their published shape, their error set and their fakes are declared by RWB-S2-E3001-CON.

| Method | Path | Request and response | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/treatments` | `TreatmentRequest` in, `Treatment` out, with the elements named after DF-TRT-001 to DF-TRT-033 | Treatment and offer C, scope applied, through the guard library | `Idempotency-Key` header required |
| GET | `/treatments/{treatmentId}` | `Treatment` out | Treatment and offer R, scope applied, through the guard library | Not applicable |

The errors are 401, 403, 404, 409, 422 and 503 with the RFC 9457 problem body; 403 carries MSG-P4-002, 404 carries MSG-P4-003, 422 carries MSG-P7-009 with the field name and 503 carries MSG-GEN-006. The treatment resource declares no offer operation, no approval envelope and no plan body: those belong to RWB-S2-E3002-CON, RWB-S2-E3003-CON and RWB-S2-E3004-CON.

#### 12.2 REST operations consumed

None. The case status arrives on the case signal the parent `CaseWorkflow` forwards (12.4), the rule package arrives through the workflow's own package read and the queue, and the lists and the rights arrive through the template's client libraries; this story makes no REST call to another service, which is why the Work Package carries no contract and no integration dependency for it. The composite route of DP-19 is consumed by the browser and by gateway-bff, not by this service.

#### 12.3 Events published

None. The topic of the service is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its two event types `TreatmentApproved` and `TreatmentClosed` belong to RWB-S2-E3003-APP and to the closing story. This story writes no outbox row of its own beyond the `DecisionRecorded` row the library writes inside the transaction (DP-03; Architecture v5 slides 18 and 43).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | Announces the RESTRUCTURE package version in force; the stage swaps it in and stamps it on the decision record |
| CaseEvent (EV-29), the case signal | no topic: the case router and the parent `CaseWorkflow` of rwb-case | P3 rwb-case | Carries the case status, the route and the case facts the stage evaluates; forwarded to this child by the parent |

The package event is consumed through the inbox of the outbox library, so a redelivery starts no second swap. The case signal is a Temporal signal forwarded by the parent and is not a Kafka subscription of this service; a replayed workflow reuses the recorded signal (Temporal and Drools Design slide 13; Architecture v5 slide 43).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, route, business date, package in force; output: the stage outcome of 12.1 and section 9 |
| `openTreatment` | Activity | `rwb-treatment` | The `TreatmentRequest` of the case; the created `Treatment` and its ID out; one service method shared with the screen's create call |
| `recordAndApply` | Activity | `rwb-treatment` | The treatment row, the local decision record, the outbox rows and the idempotency row in one transaction (the `RecordAndApply` activity contract of the design) |

The package evaluation itself is the embedded Drools runtime's, asked by the workflow inside its own step, and the kit's `EvaluateRules` contract is the design's name for that call; this story adds no activity of its own for it (ASM-3063; Temporal and Drools Design slide 13). The workflow and activity names outside the design's `TreatmentWorkflow` and `RecordAndApply` are a target design choice and are fixed by no source document (GAP-1869; ASM-3065).

#### 12.6 Schedules

None. The stage is started by the parent `CaseWorkflow` with a case signal and owns no Temporal Schedule and no legacy Quartz job; the plan timers of the restructure route are durable timers of the stage that owns them and belong to RWB-S2-E3004-APP (DP-10).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Created by this story's Flyway version and written by `recordAndApply` and by the create operation; DF-TRT-001 to DF-TRT-033 |
| `decision_record` | `rwb_treatment` | PLT library object applied in this schema | Written through `DecisionRecordWriter.record` in the caller's transaction; the central `decision_log_entry` is P7's and is never touched |

The outbox, inbox and idempotency tables are the service template's and are not restated here (ASM-3064). No contract, agreement or plan-timer table is created by this story: Arch v5 slide 41 names them without a field list and their shape is Not specified in the source documents (GAP-1869; ASM-3065).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3001-CON treatment fake | The two operations of 12.1 | A created `Treatment` with its ID and state; a refused create with 403 and 422; a read of the same treatment; a 404 for an unknown ID; a repeated key answering the first result |
| RWB-PLT-E1027-CON writer fake | `DecisionRecordWriter.record` | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable store raising MSG-P7-003 |
| RWB-PLT-N001-CON composite-route fake | SCR-14 and SCR-15 | The composed case read and treatment read in one hop each |
| rwb-case case-signal fixture | The mock line of AC2 and AC3 | A signal carrying ROUTE_APPROVED_RESTRUCTURE for R1 and one carrying WITH_FCR_OFFICER with a deviation flag |
| RESTRUCTURE package fixture | The evaluated package | Version "RES-2026.11" with rows R-RES-01 and R-RES-10, their conditions, action texts and timer specs; a version with no row for the state |

The treatment fake is the published contract of RWB-S2-E3001-CON, and the case-signal fixture is test-only: it stands where the parent `CaseWorkflow` and the case of rwb-case would be, and it is recorded with GAP-1869 and ASM-3065.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/treatment/v1` | 0 | OpenAPI 3.1; the browser reaches them through gateway-bff (DP-19) |
| Kafka | None | 1 event (`rwb.decision.RulePackageInForce.v1`) | Own topic used by the sibling stories; inbox dedupe by cloud event id |
| Temporal | None | `TreatmentWorkflow` and 2 activities on `rwb-treatment` | Namespace `rwb-recovery`; one child per case; no Schedule |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `stage` and `treatment`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the pattern the story is built on: the record is a local row in `rwb_treatment` and a shared event, and no service writes the central ledger. DP-13 is the base and the two paths, and DP-19 is the only route the two screens use. DP-01 stands behind section 11 and BR6 as the schema rule, and the case status crosses no schema because it arrives on the signal; it adds no dependency and no row of its own. The embedded Drools runtime and the packages, the guard, the inbox and the workflow kit are the service template's and add no build dependency (ASM-3063, ASM-3064).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` | Workflow | The stage child: receives the signal, asks the package, calls the two activities, reports the outcome, waits |
| `openTreatment` | Activity | Builds the `TreatmentRequest` from the rule outputs and the case signal and creates the row through the service method |
| `recordAndApply` | Activity | One transaction: the row, the decision record, the outbox rows and the idempotency row |
| `TreatmentController` | Controller | The two operations of 12.1, the validation, the problem body and the guard |
| `TreatmentService` | Service | The open and the read, the list values in force and the state of a new row |
| `TreatmentRepository` | Repository | Reads and writes `treatment` in `rwb_treatment` only |
| `TreatmentOutcomeReporter` | Service | Builds the stage outcome of section 9 and returns it to the parent workflow |
| `DecisionRecordAdapter` | Library adapter | Calls `DecisionRecordWriter.record` with the rule ID and the package version (DP-03) |
| `Migrations` | Migration | `treatment` on the per-service Flyway sequence, without a cross-schema key |

**Database.** `treatment` is created with the standard columns of TSD S2 T3.0 — `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` — on the primary key `id`, with `case_id` and `decision_log_id` held as cross references and no foreign key across a schema. The column types are those of TSD S2 T3.1: `treatment_type` varchar(20), `proposed_by` varchar(10), `approval_level` varchar(4), `outcome` varchar(12), `nleads_ref` varchar(30), `credit_result` varchar(10), `credit_result_reason` varchar(1000), `signature_status` varchar(12), the amounts numeric(18,2), `interest_rate` numeric(7,4), `booking_difference` jsonb, the counts integer and the dates timestamptz or date as the table states. No contract, agreement or plan-timer table is created here, and no row of another service's table is copied (DP-01).

**Configuration and reference data.** The lists LOV-TREATMENT, LOV-PROPOSER, LOV-TRT-OUTCOME, LOV-APPROVAL-LEVEL, LOV-CREDIT-RESULT and LOV-TRT-SIGNATURE are values in force read with their version, and no member is a constant (BR-S2-001; BR7). The RESTRUCTURE package and its rows are rwb-decision's and arrive on `RulePackageInForce`; the story stores no rule text. The capability area "Treatment and offer" and its rights are rwb-access data, and the story declares the right only. The offer validity, the credit-approval clock and the deviation threshold are the row values of the rules and are never parameters of this service.

**Build steps**

1. The Flyway version with `treatment` and its standard columns (DP-15; section 13 database).
2. `TreatmentController` and `TreatmentService` for the two operations, with the validation, the problem body, the guard and the `Idempotency-Key` path (AC1).
3. `TreatmentRepository` and the migration test against the contract's DDL template (AC1).
4. `DecisionRecordAdapter` and the one transaction of `recordAndApply`, with the rollback path (AC1, AC4).
5. `TreatmentWorkflow` registered on `rwb-treatment` with its input record and its child registration on `CaseWorkflow` (AC2, AC3).
6. `openTreatment` against the package fixture and the case-signal fixture, with the row built from the rule outputs (AC2).
7. `TreatmentOutcomeReporter` and the outcome returned to the parent, with the COLLINS line of AC2 answered by the signal (AC2, AC3).
8. Tests for AC1 to AC4 against the fakes of 12.8.

**Feature flag.** `rwb.treatment.create-record`.

**Done when.** The tests in section 16 pass, the RWB-S2-E3001-CON contract tests stay green, a synthetic case signal opens one `treatment` row with its `decision_record` in the same transaction in SIT, the parent moves the case to PROPOSED_IN_COLLINS and to AWAITING_CREDIT_APPROVAL on the two signals, a forced record failure leaves no row and no outbox row, and SCR-14 shows the opened treatment through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-001 | An offer below the floor is submitted | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | The payoff shown on the treatment screen is from an earlier date | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | An offer with an end date is shown | The offer to the customer ends on {date}. |
| MSG-GEN-001 | A required field is missing | Enter {field}. |
| MSG-P4-002 | A role without the right for the operation | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |

MSG-S2-001, MSG-S2-002, MSG-S2-003, MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are the six legacy texts carried unchanged. MSG-P4-002 is the guard library's answer, MSG-P7-003 and MSG-P7-009 are the library's and are declared by RWB-PLT-E1027-CON, and MSG-GEN-001 is used for a missing field before the transaction opens. MSG-S2-001 and MSG-S2-003 are shown by the settlement offer, which is RWB-S2-E3002-APP's, and are listed here because the legacy story carries them. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | States | What this story puts on it |
|---|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken | The opened treatment with its type, its proposer, its dates and its state Draft; the record reference and the rule that opened it |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted | The treatment the offer is built on, read only from this story; the offer itself is RWB-S2-E3002-APP's |

Both screens are served by the gateway-bff composite route, which composes the case read of rwb-case with the treatment read of this service, one hop each, read only (DP-19); the browser calls no owner service directly. The screen field list, the composite route specification and the layout belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-001-01 | AC1 | End to end | Create the treatment record |
| TC-E3-001-02 | AC2 | End to end | Rule R-RES-01 |
| TC-E3-001-03 | AC3 | End to end | Rule R-RES-10 |
| TC-E3-001-04 | AC4 | End to end | Not recorded |
| TC-E3-001-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-001-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and the "Access" and "Principle 5" cases to "Component", as in the other stories of this run. Where Covers names `Access`, the criterion is the guard's published answer on the two operations, and where it names `Principle 5` the criterion is the rollback of the one transaction. The fakes of section 12.8 stand behind every case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these six cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the rules, the states, the timers, the thresholds and every list are values in force read with their version (BR-S2-001; the lists are template data, no dependency added).
- No personal data in logs, tests, workflow inputs or prompts: the request, the row, the record and the logs carry case IDs, treatment IDs, codes, dates and amounts only, and the profile codec is on every payload.
- No read of another module's tables: the case status arrives on the case signal, the package through its event, the lists through the template, and `rwb_treatment` holds no foreign key into another schema (DP-01, ASM-3062).
- ACE data only through the owner's contract or the `v_ace_*` views: this story reads no ACE view and calls no ACE interface, and the expected-return facts it evaluates arrive on the case signal.
- No live COLLINS call: no COLLINS interface is published for S2, so the proposal facts of AC2 are taken from the case signal and the following proposal step stays with rwb-case's flow.
- The decision record is written in the same transaction as the treatment row, and a failed write rolls the whole call back with MSG-P7-003 (DP-03).
- The central ledger is never written or read here: `decision_log_entry` belongs to P7 and is reached only through the shared topic.
- An applied migration is never edited: a correction to `treatment` is a new version on the service sequence (DP-15).
- No right is re-implemented: the capability area and the right are declared, and the guard library answers.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-001 | A restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench | Business Requirements Program v5, section 5.9 | FEAT-TRT-01 | 07 Route, settle and claim | R-RES-01, R-RES-10 | TC-E3-001-01 to TC-E3-001-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3001-CON | Contract | H: declares the two operations, the `TreatmentRequest` and `Treatment` shapes, the `treatment` DDL template, the error set and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the record is written through in the same transaction |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that serves SCR-14 and SCR-15 |
| RWB-S2-E3002-APP | App development | Sibling: the settlement offer, its range and the offer terms of a treatment |
| RWB-S2-E3003-APP | App development | Sibling: the approval of an offer below the floor, the approval level and `TreatmentApproved` |
| RWB-S2-E3004-APP | App development | Sibling: the TDR plan, its installments and its plan timers |
| RWB-S2-E3005-APP | App development | Sibling: the ACE affordability pre-assessment |
| P3 rwb-case | App development | The parent `CaseWorkflow`, the case status and the case signal the AC2 and AC3 mock stands for; owns R-RES-02 to R-RES-09 and R-RES-11 to R-RES-25 |
| P7 rwb-decision | App development | The RESTRUCTURE package, its rows and its version, announced on `RulePackageInForce` |
| RWB-ITG-W2 | Integration | The cross-service proof of the stage against the live parent and the live package, held by the wave 2 harness |

### 19. Out of scope

- The published shape of the two operations, the element names, the `treatment` DDL template, the error set and the fakes: RWB-S2-E3001-CON.
- The settlement offer, its range, the floor and MSG-S2-001: RWB-S2-E3002-APP and RWB-S2-E3002-CON.
- The approval of an offer below the floor, the delegation of authority applied and the `TreatmentApproved` event: RWB-S2-E3003-APP and RWB-S2-E3003-CON.
- The TDR plan, its installments, the plan timers and the `TreatmentClosed` event: RWB-S2-E3004-APP and RWB-S2-E3004-CON.
- The ACE affordability pre-assessment and the restructure calculator: RWB-S2-E3005-APP.
- The case status, the `CaseWorkflow`, the case table, the case signal and the restructure proposal step R-RES-02: rwb-case (P3).
- The RESTRUCTURE, SETTLEMENT and DEEDINLIEU packages, their rows and their versions: rwb-decision (P7).
- The rights, the roles and the scope data, and the guard library that answers them: rwb-access (P4) and the platform library stories.
- The gateway-bff composite route, the screen field list and the layout: the platform edge story and the screen owners (DP-19).
- The contracts, settlement and deed-in-lieu agreements and plan timers that Arch v5 slide 41 places in `rwb_treatment` but no source gives a field list for (GAP-1869; ASM-3065).
- The live COLLINS call of the legacy R-RES-01: no COLLINS interface is published for S2 in this wave, and the approved route with its expected-return facts arrives on the case signal.
- The real cross-service proof of the stage against the live parent and the live package: the wave 2 integration harness.
- The deployment of this build: chart values, the queue and topic provisioning, the flag, dashboards and the runbook.
