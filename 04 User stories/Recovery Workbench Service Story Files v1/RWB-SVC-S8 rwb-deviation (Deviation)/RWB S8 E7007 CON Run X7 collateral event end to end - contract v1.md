# RWB-S8-E7007-CON Run X7 collateral event end to end - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7007-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the X7 collateral-event outcome of rwb-deviation, split from RWB-E7-007. It fixes the outcome branch of `PATCH /deviations/{deviationId}` on `/api/recovery/deviation/v1` (DP-13), the `DeviationOutcome` and `Deviation` elements over the fields DF-CAS-036 to DF-CAS-045 with the three lists of TSD S8 T3.2, the six consumed rows — the rwb-case case read and case-move answer, the rwb-decision package read, the rwb-guarantee claim answer, the rwb-valuation re-appraisal answer and the rwb-source-data collateral read (DP-05) — the decision-record element of DP-03, the rights of TSD S8 T6.1, one published event and the fakes. Six consumed rows sit behind a C row of None, the outbox library of DP-09 is absent from the pattern set, and the operation and element shapes carry placeholders (GAP-3064; ASM-5191, ASM-5193 to ASM-5196, ASM-5200). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the X7 collateral-event outcome of rwb-deviation — the outcome operation on `/api/recovery/deviation/v1`, the deviation and outcome elements with their required flags and lists, the six consumed rows, the decision-record element, the one published event, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-06, SCR-08 and the wave 4 harness build against one fixed, testable contract on Day 1, and a field, a consumed row or an answer shape can never drift between rwb-deviation, rwb-case, rwb-decision, rwb-guarantee, rwb-valuation and rwb-source-data without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy X7 flow of RWB-E7-007 crossed five boundaries at once — the case of record, the rule version, the insurance claim, the appraisal and the collateral data — and the monolith served all of them in one process under one base, so no contract existed between them. The target splits them: rwb-case owns the case and its states, rwb-decision owns the DEV package, rwb-guarantee owns the claim, rwb-valuation owns the appraisal, rwb-source-data owns the ACE collateral data, and rwb-deviation owns the deviation row, its outcome and the record. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_deviation`, base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with its retry and `.dlt` topics, task queue `rwb-deviation` in namespace `rwb-recovery`, event name `rwb.deviation.<Event>.v1` and Java package `th.co.scb.ace.workbench.recovery.deviation` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, `rwb_decision`, `rwb_guarantee`, `rwb_valuation` or `rwb_source_data`, so DP-05 is declared in its contract form.

Four points are carried as gaps and assumptions rather than decided quietly: the operation and element shapes of the outcome have no published schema beyond TSD S8 T-A.2, so the baseline fixes them and marks the placeholders (ASM-5200); six consumed rows sit behind a plan C row of None, and their operation names are published nowhere (ASM-5191, ASM-5193 to ASM-5195); the outbox and inbox library of DP-09 is not in the pattern set although the step publishes an event (ASM-5196); and no source gives the claim, the appraisal or the return-point properties of the deviation answer (GAP-3064).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `deviation` is S8's, `recovery_case`, `assignment` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, the claim is S3's, the appraisal is S1's, `document` is P5's, `notice` is P6's and `payment` is P8's. This document never declares another service's table or operation as its own.
- The rwb-case case read and case-move answer, the rwb-decision package read, the rwb-guarantee claim answer, the rwb-valuation re-appraisal answer and the rwb-source-data collateral read are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3064; ASM-5191, ASM-5193 to ASM-5195).
- TSD S8 T-A.1 publishes API-S8-001 and API-S8-002 only, with the request `DeviationOutcome` and the answer `Deviation` on API-S8-002; the element properties beyond the fields of T3.1 are this baseline's, and the placeholders stand until the solution architect confirms them (GAP-3064; ASM-5200).
- The DEV package and its rows for R-DEV-06, R-DEV-12 and R-DEV-19 are governed in rwb-decision (P7); this baseline names them and declares none of them (ASM-5193).
- The `deviation` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-deviation for the X7 outcome: the outcome branch of API-S8-002 with its request and answer elements, the rights and the error responses.
2. Fix the `Deviation` element over the deviation columns of DF-CAS-036 to DF-CAS-045 and the `DeviationOutcome` element with the assignment, the claim reference, the outcome and the request reference.
3. Fix the six consumed rows: the case read and the case-move answer of rwb-case, the package read of rwb-decision with its version, the claim answer of rwb-guarantee, the re-appraisal answer of rwb-valuation and the collateral read of rwb-source-data, marking with the placeholder what the sources do not give.
4. Record the decision-record element of DP-03, written before the row changes and before the move leaves the service.
5. Record the one published event of the step, `DeviationCleared` (`EV-07`), with its payload and its producer group, and state that EV-06 belongs to the raise step.
6. Record the rights of the operation and the naming baseline, and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a case write, the drift between a fake and the document, and the absence of a consumed event and of a Schedule.
9. Tag the baseline and hand it to RWB-S8-E7007-APP, SCR-06, SCR-08 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC6 |
| X5 | The outcome is declared as a free string, or a code list is inlined | The vocabulary test fails the build: `outcome`, `deviation_code` and `raised_by` take the lists of TSD S8 T3.2 | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a claim or an appraisal property | The review fails the baseline and the boundary test fails the build | None | AC3, AC7 |
| X7 | The document declares a second topic, a consumed event or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of the operation are not the ones TSD S8 T6.1 gives the capability area for a change | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S8 appendices and the published owner contracts of rwb-case, rwb-decision, rwb-guarantee, rwb-valuation and rwb-source-data only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the base, the rights, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S8-E7007-APP, SCR-06, SCR-08 and the wave 4 harness on Day 1, and the five consuming teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, eight fakes and twelve contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the X7 collateral-event outcome of rwb-deviation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of deviation is S8, of recovery_case, assignment and timer is P3, of every v_ace_* view is P1, of decision_log_entry and rule_row is P7, of the claim is S3 and of the appraisal is S1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The outcome operation is declared on the deviation base with its shape and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-deviation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares PATCH /deviations/{deviationId} with a DeviationOutcome body in and a Deviation answer of status 200, under the base /api/recovery/deviation/v1 and owned by rwb-deviation
    Then the operation declares the path parameter deviationId and the Idempotency-Key rule for a repeated request
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then the request and answer element names carry the placeholder Not specified in the source documents (GAP-3064; ASM-5200) until the solution architect confirms them
    Then no operation of the raise or of the screening of a deviation is declared by this document

  Scenario: AC2 The deviation and outcome elements and the three lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S8 T3.1 and T3.2
    Then the Deviation element declares the properties of DF-CAS-036 to DF-CAS-045: id, case_id, deviation_code, raised_at, raised_by, paused_state, handler_user_id, contact_stop, cleared_at and outcome
    Then it declares the outcome properties: the rule ID R-DEV-06, R-DEV-12 or R-DEV-19 with its rule version, the from state, the to state, the decided-at time and the return point
    Then the DeviationOutcome element declares the assignment, the claim reference, the outcome and the request reference, with the assignment and the outcome required
    Then outcome declares the enumeration RETURNED, RE_ROUTED and CASE_ENDED, deviation_code declares X1 to X7 and raised_by declares SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, exactly as TSD S8 T3.2 lists them
    Then no property is added for a claim amount, an appraised value, a timer, an ACE extract or a ledger row

  Scenario: AC3 The six consumed rows are declared and the facts stay with their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case read is declared as consumed from P3 rwb-case, with the case reference, the case number, the product group, the stage and the case state
    Then the case-move answer is declared as consumed from P3 rwb-case, with the moves DEV_WITH_OWNER, DEV_REROUTE and ROUTE_D6 carrying the rule ID and its version
    Then the package read is declared as consumed from P7 rwb-decision, with the DEV package, its version and its 22 rules over 9 states
    Then the claim is declared as consumed from S3 rwb-guarantee, with the claim of the collateral event, its status and the approving identity of FEAT-GUA-08
    Then the appraisal is declared as consumed from S1 rwb-valuation, with the re-appraisal order and the accepted value of FEAT-VAL-01 and FEAT-VAL-02
    Then the collateral read is declared as consumed from P1 rwb-source-data, with the collateral record of DF-ACE-091 to DF-ACE-098 and the appraised value of DF-ACE-187 to DF-ACE-195
    Then the operation names of the six rows are Not specified in the source documents (GAP-3064; ASM-5191, ASM-5193 to ASM-5195)
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no claim or appraisal property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S8 T-A.1 and T6.1
    Then the outcome declares Case record right U with the scope applied, because it records an outcome and moves no authority of its own
    Then RW-CASEOWN holds CRU on the capability area and is the primary role of the operation
    Then RW-SPECIAL and RW-GUARANT hold RU and read the outcome without a wider right, and RW-LEGAL holds R
    Then every other role and every SY-* service identity of TSD S8 T6.1 holds R or U as the matrix gives it
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and written before the case moves (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S8 T2
    Then one decision record is declared per rule outcome with the case reference, the deviation reference, the rule ID R-DEV-06 or R-DEV-12, the package version in force, the outcome, the from state, the to state and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the row changes and before the case-move answer leaves the service, and a failed write leaves everything unchanged with MSG-P7-003
    Then the record carries no rule row, no state threshold as a literal and no personal data

  Scenario: AC6 The eight fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case case fake answers the case at DEV_FLAGGED and at DEV_WITH_OWNER, a case that has moved and a case that is not in scope
    Then the rwb-case case-move fake answers the three moves accepted and a move refused
    Then the rwb-decision fake answers the DEV package at its version with R-DEV-06, R-DEV-12 and R-DEV-19
    Then the rwb-guarantee fake answers a claim approved by a person and one still open, the rwb-valuation fake answers the order and the accepted value, and the rwb-source-data fake answers the collateral record and the appraised value
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-08 and SCR-06 answers
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline, the boundary and the one event are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_deviation, the login is rwb_deviation, the base is /api/recovery/deviation/v1, the topic is rwb.deviation.events.v1 with its retry and .dlt topics, the queue is rwb-deviation in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.deviation
    Then the tables named as owned are deviation and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, assignment, timer, every v_ace_* view, decision_log_entry, rule_row, the claim and the appraisal are named as other owners' and consumed only through their contracts
    Then DeviationCleared (EV-07) is declared on rwb.deviation.events.v1 with caseId, deviationCode and outcome, and DeviationRaised (EV-06) is named as the raise step's
    Then the document declares no consumed event, no second topic and no Schedule
    Then the absence test fails a build that adds a consumed event, a second topic, a Schedule or a v_ace_* read (ASM-5196)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S8-E7007-APP and copy no criterion of the legacy story, whose three criteria stay with the app story word for word. The baseline moves no case, approves no claim and orders no appraisal (ASM-5194, ASM-5200).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The X7 outcome is rwb-deviation's, and the contract declares the fields and the required flags on the `Deviation` element and on the `DeviationOutcome` element only | TSD S8 T3.1, T-A.2; context pack ownership rows (table `deviation`) |
| BR2 | The decision record is declared as an element written before the row changes and before the move is answered, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S8 T2; legacy RWB-E7-007 AC4 |
| BR3 | The case stays with rwb-case: the contract declares the case read and the case-move answer as consumed, declares no `recovery_case` property and describes no case row write | ASM-5191; TSD S8 T4 |
| BR4 | The package is rwb-decision's: the contract declares the package read as consumed and declares no rule row, no threshold and no rule version as a property | ASM-5193 |
| BR5 | The claim is rwb-guarantee's and the appraisal rwb-valuation's: the contract declares both as consumed rows and declares no claim amount and no appraised value as a property of its own | ASM-5194; FEAT-GUA-08, FEAT-VAL-01, FEAT-VAL-02 |
| BR6 | ACE data stays with rwb-source-data: the collateral record and the appraised value are declared as a consumed row, and no `v_ace_*` path, property or view is declared | DP-05; ASM-5195 |
| BR7 | One event is declared, `DeviationCleared` (`EV-07`), with the payload of the event set; `DeviationRaised` (`EV-06`) is the raise step's, and the outbox library of DP-09 is recorded as an absent H row | ASM-5196; Event and Messaging Design v4 |
| BR8 | The outcome, the deviation code and the raised-by value are declared as the enumerations TSD S8 T3.2 lists, never as free strings and never as inline constants | TSD S8 T3.2 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, dates, an outcome and a rule version only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S8 T6.2 |
| BR10 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR12 | The document lists only operations owned by rwb-deviation; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR13 | The request and answer element names and the return-point property are placeholders fixed by this baseline, not copied from a source, because only the two element names and the field list are published | GAP-3064; ASM-5200 |
| BR14 | The rights of the operation are the capability area's change right U, held by the case owner and the roles the legacy permission table names | TSD S8 T6.1; legacy permission table of RWB-E7-007 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the elements, the lists, the consumed rows, the decision element, the event and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-06, SCR-08, the wave 4 harness and the owners of rwb-case, rwb-decision, rwb-guarantee, rwb-valuation and rwb-source-data accept the document and the fakes | Baselined |
| Baselined | The placeholders are confirmed | The solution architect replaces the element names and the return-point property inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional reference or a new filter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a code list becomes a free string | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a claim or appraisal property, a consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's and rwb-case's: `DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_REROUTE` and `ROUTE_D6` are route states of rwb-case (TSD S8 T4, T-A.1). This baseline fixes the vocabulary and the answer shape and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-deviation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves the placeholder element names and the return-point property, a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the six consumed rows and the absent DP-09 row |
| Consuming teams (the app story, SCR-06, SCR-08, the wave 4 harness and the owners of rwb-case, rwb-decision, rwb-guarantee, rwb-valuation, rwb-source-data and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-deviation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Deviation element | The columns of DF-CAS-036 to DF-CAS-045: `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state`, `handler_user_id`, `contact_stop`, `cleared_at` and `outcome` |
| Outcome element | The assignment, the claim reference, the outcome, the request reference, the rule ID, the rule version, the from state, the to state, the decided-at time and the return point |
| Required flags | The assignment and the outcome required on the request; `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state` and `contact_stop` required on the element, as TSD S8 T3.1 gives them; the other properties optional |
| Lists | `outcome`: RETURNED, RE_ROUTED, CASE_ENDED; `deviation_code`: X1 to X7; `raised_by`: SCREENING_AGENT, RULE, OFFICER, CUSTOMER_CONTACT (TSD S8 T3.2) |
| Event data | `DeviationCleared` (`EV-07`) with `caseId`, `deviationCode` and `outcome`; no personal data and no free text beyond the code and the outcome |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03) |
| Case, claim, appraisal and ACE facts | DF-CAS-001 to DF-CAS-023 and DF-WRK-009 to DF-WRK-036 in P3, DF-REF-001 to DF-REF-015 in P7, the claim in S3, the appraisal in S1 and DF-ACE-091 to DF-ACE-098 with DF-ACE-187 to DF-ACE-195 in P1, read only through the owners' rows and never written, copied or joined here |
| Not declared here | `recovery_case`, `assignment`, `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8), the claim (S3) and the appraisal (S1) |
| Consumed fields with no source | The operation names of the six consumed rows, the claim status and approving-identity properties, the appraisal value property and the return-point property: Not specified in the source documents (GAP-3064; ASM-5191, ASM-5194, ASM-5200) |

The field-level types, lengths and required flags of the added properties are settled in the baseline review; this story fixes the element names, the three lists of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/deviations/{deviationId}` (API-S8-002) | `DeviationOutcome` in with the assignment, the claim reference and the outcome; `Deviation` of status 200 out, carrying the rule `R-DEV-06` or `R-DEV-12` with its version, the handler, the outcome and the state | Case record, right U, scope applied | `Idempotency-Key` header for a repeated request; TSD S8 T-A.2 publishes "Not applicable" and the baseline keeps the rule (ASM-5198) |

The operation answers 400, 401, 403 with MSG-P4-002, 404 for a deviation that is not this service's, 409 for a case that has left `DEV_FLAGGED`, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. TSD S8 T-A.2 publishes the operation as API-S8-002 with the request `DeviationOutcome`, the answer `Deviation`, the right U and the error set 401, 403, 404, 409, 422 and 503; the properties beyond T3.1 carry the placeholder (GAP-3064; ASM-5200). The raise operation of the module, `POST /cases/{caseId}/deviations` (API-S8-001, right U), belongs to the deviation-raise slice and is not declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3064; ASM-5191)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state of the case at `DEV_FLAGGED` and `DEV_WITH_OWNER`; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3064; ASM-5191)) | rwb-case (P3) | P3 rwb-case | The moves `DEV_WITH_OWNER`, `DEV_REROUTE` and `ROUTE_D6` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3064; ASM-5193)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEV package at its version, with R-DEV-06, R-DEV-12 and R-DEV-19 among its 22 rules over 9 states; faked |
| The insurance-claim read (operation name Not specified in the source documents (GAP-3064; ASM-5194)) | `/api/recovery/guarantee/v1` | S3 rwb-guarantee | The claim of the collateral event on FEAT-GUA-08, its status and the approving identity; faked |
| The re-appraisal read (operation name Not specified in the source documents (GAP-3064; ASM-5194)) | `/api/recovery/valuation/v1` | S1 rwb-valuation | The re-appraisal order and the accepted value of FEAT-VAL-01 and FEAT-VAL-02; faked |
| The collateral and appraisal read (operation name Not specified in the source documents (GAP-3064; ASM-5195)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The collateral record of DF-ACE-091 to DF-ACE-098 and the appraised value of DF-ACE-187 to DF-ACE-195, read only; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3064; ASM-5191, ASM-5193 to ASM-5195).

#### 12.3 Events published

| Event | Name | Payload | Producer group | Consumer |
|---|---|---|---|---|
| EV-07 | `rwb.deviation.DeviationCleared.v1` on `rwb.deviation.events.v1` | `caseId`, `deviationCode`, `outcome` | rwb-deviation X7 outcome | Timers and communications, per the event set of the Event and Messaging Design v4 |

One row, with a CloudEvents envelope and the retry and `.dlt` topics of the platform (DP-14). `DeviationRaised` (`EV-06`) belongs to the deviation-raise slice and is named, not declared. The outbox that relays the row is a library object created in `rwb_deviation`, and the outbox and inbox library `RWB-PLT-TE006-CON` that DP-09 would add is absent from the plan's H row; the absence is recorded (GAP-3064; ASM-5196).

#### 12.4 Events consumed

None. The trigger of the step is the owner's decision on SCR-06 or SCR-08 through the composite route, because the FSD declares no background event for the feature (FSD S8 A2.16.4.4: "No background event"). The service listens to the rwb-source-data and rwb-case events in its screening and timer slices (context pack connection matrix, row S8), not in this step. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, starts at any time for a case, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-deviation` in namespace `rwb-recovery` | The stage that hosts the X7 step; its signals and its outcome for the parent are declared, not built |
| `recordCollateralOutcome` | Activity, the one X7 outcome step | `rwb-deviation` | The deviation reference, the assignment, the claim reference and the package version in; the rule ID with its version, the record written, the row updated and the case move out |

No child workflow for the case, the claim or the appraisal exists in this service. The activity name is a target design choice, and the step runs from the owner's request. No activity is registered by this story, and no timer is declared: R-DEV-06 and R-DEV-12 carry none, and the stage clock is rwb-case's (ASM-5192).

#### 12.6 Schedules

None. The service owns no job (context pack jobs row: 0), the step is owner-driven, and this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The clock the deviation pauses and resumes is the `timer` row that rwb-case owns under R-DEV-18, named here only as another service's.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | The deviation X1 to X7 raised on a case, its code, its handler, its outcome and its return point; the table the answer element is drawn from |
| decision_record | PLT library, created in `rwb_deviation` | The local hash-linked decision record of the outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_deviation` | The key of the repeated request and the answer it holds |
| outbox_event | PLT library, created in `rwb_deviation` | The row that relays `DeviationCleared` (`EV-07`) (§12.3) |

`recovery_case`, `assignment` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), the claim (S3), the appraisal (S1), `document` (P5), `notice` (P6) and `payment` (P8) are not owned by this baseline; it names them only as answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | The case at `DEV_FLAGGED` and at `DEV_WITH_OWNER` for `RW-2026-000702`; a case that has moved; a case that is not in scope | AC1, AC3, AC6 |
| rwb-case case-move fake | The moves `DEV_WITH_OWNER`, `DEV_REROUTE` and `ROUTE_D6` accepted with the rule version, and a move refused | AC3, AC6 |
| rwb-decision rule-package fake | The DEV package at its version in force with R-DEV-06, R-DEV-12 and R-DEV-19 among its 22 rules over 9 states | AC2, AC3, AC6 |
| rwb-guarantee claim fake | The insurance claim of `COL-2026-000702` approved by a person, and one still open | AC3, AC6 |
| rwb-valuation re-appraisal fake | The re-appraisal order and the accepted value of `COL-2026-000702`; an appraisal still open | AC3, AC6 |
| rwb-source-data collateral fake | The collateral record and the appraised value of `COL-2026-000702`, read only | AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-08 and SCR-06 answers for `RW-2026-000702`, in their flagged and handled states | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the six consumed rows carry the placeholder until their owners confirm them (GAP-3064; ASM-5191, ASM-5193 to ASM-5195).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed | The outcome branch of API-S8-002 on `/api/recovery/deviation/v1`; the case read, the case-move answers, the package read, the claim read, the re-appraisal read and the collateral read; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `DeviationCleared` (`EV-07`) on `rwb.deviation.events.v1` with its retry and `.dlt` topics; EV-06 is the raise step's (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `DeviationWorkflow` and `recordCollateralOutcome` on `rwb-deviation`; no Schedule and no timer |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no claim and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and eight fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the row changes and before the move is answered. DP-05 is declared in its contract form, because S8 owns no `v_ace_*` view. DP-13 moves the base of the legacy path and gives the outcome operation its home. DP-19 sits behind SCR-06 and SCR-08, whose screen model is the edge contract's. DP-09 is not in the pattern set: the outbox is declared as a library object and the row it needs is recorded as an absent H row (GAP-3064; ASM-5196).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the published event needs. The six consumed rows are C dependencies in fact and not in the metadata row, whose value is None.

**Deliverables and build steps**

1. Write the outcome operation of API-S8-002 and validate the additive rule of AC1 in the pipeline.
2. Write the `Deviation` and `DeviationOutcome` elements, their required flags and the three lists of AC2, with the placeholder where a property is unstated.
3. Record the six consumed rows of AC3 with their owner, their budget and their placeholders.
4. Record the rights and the error envelope of AC4.
5. Record the decision-record element of AC5 and validate it against the library schema.
6. Record the one published event of AC7 and its payload, and the absence of a consumed event and of a Schedule.
7. Publish the eight fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-deviation-v1.yaml`, the two elements, the contract README rows for the six consumed rows and their placeholders, and the eight fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the twelve contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-06, SCR-08 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | Carried from the legacy message set of RWB-E7-007: the deviation and its handler are named in the answer and on the screen after the action | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required field of a request is absent or invalid, the assignment and the outcome among them, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Case record right U the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row changes and the move is answered | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-08 Deviation queue and SCR-06 Raise deviation in their "Loading; list" and "Form; saved" states through the gateway-bff composite route (DP-19). The route calls rwb-deviation for the deviation and its outcome, rwb-case for the case and its route state, and rwb-guarantee for the claim; this baseline fixes the rwb-deviation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. This story adds no screen and no state: the flagged, handled and re-routed states are rwb-case's and are shown read only, and the refusal, invalid-request and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-007-01 | AC1, AC3 | Contract | `RW-2026-000702` with the X7 deviation; the contract half answers the outcome operation, the case read and the package read |
| TC-E7-007-02 | AC2, AC3 | Contract | The claim approved and the appraisal accepted; the contract half answers the two elements, the three lists and the `DEV_WITH_OWNER` move shape |
| TC-E7-007-03 | AC3, AC5 | Contract | The estate confirmed; the contract half answers the `DEV_REROUTE` and `ROUTE_D6` move shapes and the decision-record element |
| TC-E7-007-04 | AC5, AC7 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the event payload |
| TC-E7-007-05 | AC4 | Contract | A role without the right U; the contract half answers the 403 with MSG-P4-002 |
| TC-E7-007-06 | AC4, AC7 | Contract | A forced record failure and a malformed request; the contract half answers the 400 of the envelope and the absence tests |
| TC-S8-E7007-CON-01 | AC1 | Contract | The document validates; the operation, the base, the path parameter, the `Idempotency-Key` and the seven error answers are present |
| TC-S8-E7007-CON-02 | AC2 | Contract | The two elements validate with their ten deviation properties, the outcome properties, the required flags and the three lists |
| TC-S8-E7007-CON-03 | AC3, AC4 | Contract | The six consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case`, no-claim and no-appraisal boundary; the rights |
| TC-S8-E7007-CON-04 | AC5, AC6 | Contract | The decision-record element matches the library schema; the eight fakes match the document and a drifted fake fails the build |
| TC-S8-E7007-CON-05 | AC7 | Contract | The naming baseline, the tables owned, the one published event and the absence of a consumed event, a second topic and a Schedule |

The six legacy cases are those of RWB-E7-007 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S8-E7007-APP and, for the end-to-end journey, by RWB-ITG-E7007-ITG. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S8-E7007-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: R-DEV-06, R-DEV-12 and R-DEV-19, their states, the three lists and the package version stay rule rows and reference data, never a schema default, an enumeration member invented here or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, dates, an outcome and a rule version only, and every example is synthetic.
- The case stays with rwb-case: the document declares no `recovery_case` property, no case row write, no `assignment` row and no `timer` row (BR3).
- The claim stays with rwb-guarantee and the appraisal with rwb-valuation: the document declares both as consumed rows and no claim amount or appraised value as its own (BR5).
- ACE data stays with rwb-source-data: the document declares no `v_ace_*` path, no `v_ace_*` property and no ACE table read (BR6).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-deviation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a consumed event, a second topic, a Schedule or a Quartz row.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S8-005 | A collateral event triggers an insurance claim and a re-appraisal before the next decision | The claim row, the re-appraisal row and the two moves of the answer | TC-E7-007-02, TC-E7-007-03, TC-S8-E7007-CON-03 |
| REQ-DVH-005 | A resolved deviation returns the case to the state it paused in, or to the route decision where the outcome changes the route | The return-point property and the `DEV_REROUTE` and `ROUTE_D6` vocabulary | TC-E7-007-03, TC-S8-E7007-CON-02 |
| Not specified in the source documents (GAP-3064; ASM-5200) | The split plan carries no requirement id for the contract slice, and no source publishes the element properties beyond TSD S8 T3.1 and T-A.2 | The operation, the two elements and the six consumed rows | TC-S8-E7007-CON-01, TC-S8-E7007-CON-02 |
| ADR-014 | Schema and login per service | `rwb_deviation` and its own login | TC-S8-E7007-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | `DeviationCleared` and the outbox library object | TC-S8-E7007-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-S8-E7007-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S8-E7007-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-007, disposition Split (rework); feature FEAT-DVF-07 |
| Legacy criteria | AC1 to AC4 of the legacy story: AC2 to AC4 owned word for word by RWB-S8-E7007-APP, AC1 by RWB-ITG-E7007-ITG; this baseline copies none of them |
| Source text | Legacy RWB-E7-007; FSD S8 Deviation handling v3 A2.16, A2.16.2, A2.16.3 and A2.16.4; TSD S8 Deviation handling v2 T2, T3.1, T3.2, T3.3, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-DEV-06, R-DEV-12 and R-DEV-19; Event and Messaging Design v4 rows EV-06 and EV-07 |
| Test cases | The six legacy cases as the contract half, and the five new contract cases TC-S8-E7007-CON-01 to -05 |
| Feature and screens | FEAT-DVF-07, SCR-08 Deviation queue, SCR-06 Raise deviation |
| Rules | R-DEV-06, R-DEV-12 and R-DEV-19, governed in rwb-decision; R-DEV-01 and R-DEV-18 named |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the outcome operation, the evaluation of R-DEV-06 and R-DEV-12, the decision record, the row update and the case-move answers: RWB-S8-E7007-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-5191).
- The authoring, testing, approval and versioning of the DEV package and of the rule rows: rwb-decision (P7) (ASM-5193).
- The insurance claim of the collateral event and its approval: rwb-guarantee (S3), FEAT-GUA-08 (ASM-5194).
- The appraisal order, the valuer and the accepted value: rwb-valuation (S1), FEAT-VAL-01 and FEAT-VAL-02, and the route decision at D6 that receives the re-routed case (ASM-5194).
- The collateral and appraisal data of ACE and their ingestion: rwb-source-data (P1) and ACE ingestion (ASM-5195).
- The raise of a deviation and the screening slices of this service: the raise and screening stories of RWB-SVC-S8, and `DeviationRaised` (`EV-06`) as theirs.
- The other handler stories: X1 to X6 are RWB-S8-E7001-APP to RWB-S8-E7006-APP.
- The gateway-bff composite route and the screen field list of SCR-06 and SCR-08: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
- The end-to-end cross-service journey and its `-ITG` test copies: RWB-ITG-E7007-ITG and the wave 4 harness.
