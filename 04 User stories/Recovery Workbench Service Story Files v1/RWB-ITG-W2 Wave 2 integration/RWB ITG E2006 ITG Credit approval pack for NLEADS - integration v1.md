# RWB-ITG-E2006-ITG Credit approval pack for NLEADS

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2006-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP11, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2004-APP, RWB-P2-E2006-APP, RWB-P7-E2006-APP, RWB-S2-E2006-APP, RWB-P3-E2006-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-CHO-008, REQ-CHO-006, REQ-RDF-009) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-006 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness for the credit approval pack and the credit result for NLEADS, across rwb-integration, rwb-decision, rwb-treatment, rwb-case, rwb-document and rwb-access**, so that **the journey is proven end to end before release**.

This story builds the harness and the evidence only. It builds no production endpoint, no screen, no table, no migration, no workflow and no schedule, it serves no operation, it owns no table and it starts no workflow. The real behaviour is owned by the five I stories: RWB-P3-E2004-APP (the treatment entity, the route state model and the plan timers the journey starts from), RWB-P2-E2006-APP (the credit-pack and credit-result operations of rwb-integration), RWB-P7-E2006-APP (the required level from the delegation of authority and the D5 decision record), RWB-S2-E2006-APP (the treatment state and the credit result fields of rwb-treatment) and RWB-P3-E2006-APP (the case route state move on the result), and those five stories block the ITG run.

### 2. Business rationale

The legacy RWB-E2-006 journey prepared the credit approval pack for NLEADS, placed it in the officer's hands and recorded the NLEADS reference, result and approval level on the treatment, which moved the case by R-RES-11 or R-RES-12 (legacy sections 2 and 4). The split keeps every business rule, message, screen behaviour and field where the owning stories put it: the pack assembly and the result recording in RWB-P2-E2006-APP, the treatment state and result fields in RWB-S2-E2006-APP, the level and the decision record in RWB-P7-E2006-APP, the treatment entity in RWB-P3-E2004-APP and the case route state in RWB-P3-E2006-APP. None of the five can prove on its own that the pack an officer copies into NLEADS is assembled from the owning records, that the credit result is recorded once, and that the decision record precedes every change it causes.

The harness proves, on synthetic data and one business date per run:

- the composite credit-pack route composes the pack from the owning contracts, one hop per call, with no cross-schema read: the case and plan terms from rwb-case and rwb-treatment, the accounts, collateral and valuation through the owning contracts, the 5 checklist documents from rwb-document, and the required level from rwb-access and rwb-decision (legacy AC1);
- the pack carries case RW-2026-000610, product group MORTGAGE, 2 accounts with balances as of 2026-12-14, 1 collateral, the plan terms 2,400,000.00 baht offer, 0.00 baht haircut, 84 installments and valid until 2026-12-29, the 5 checklist documents and required level L6;
- the D5 decision record with final call approved is written before the treatment state change and the route move, exactly one CaseStateChanged event and one TreatmentApproved event leave the change, and exactly one outbox row exists (legacy AC2, BR2, BR8);
- every refusal leaves the treatment, the route state, the decision log and the outbox unchanged (legacy AC3, AC6, AC7, AC8, AC9, AC10, BR3, BR5);
- a failure in rwb-decision is isolated, answers MSG-P7-003 and changes nothing, and the run records the incident assertion (legacy AC11, BR8, Principle 5).

It meets REQ-CHO-008, REQ-CHO-006 and REQ-RDF-009 at the integration level. REQ-CHO-008 is the plan submitted for credit approval recorded on the case, REQ-CHO-006 is the treatment record holding type, terms, approval and outcome, and REQ-RDF-009 is the freshness of every input shown with its age and the freshness recorded on the decision. The harness asserts them across the service boundaries and restates none of them; it is the place where the pack, the result, the record and the events are checked against each other, so a broken boundary is found in SIT rather than by a plan that reaches credit with a pack built from the wrong record.

### 3. Preconditions

- The five I stories are published and deployed in the SIT environment, or their published contracts and the §12.8 fakes stand in for them: RWB-P3-E2004-APP (rwb-case treatment entity and route state), RWB-P2-E2006-APP (rwb-integration credit-pack and credit-result), RWB-P7-E2006-APP (rwb-decision level and decision record), RWB-S2-E2006-APP (rwb-treatment result fields) and RWB-P3-E2006-APP (rwb-case route move).
- gateway-bff is deployed with the composite credit-pack route of DP-19 available. The gateway-bff composite credit-pack route path and its merge order: Not specified in the source documents (GAP-0394; ASM-0569).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs from Day 1 before the five I stories land.
- The seeded NLEADS checklist rows are the 5 legacy items CREDIT_APPLICATION, ID_COPY, TITLE_DEED, LATEST_APPRAISAL and INCOME_PROOF (legacy section 3, DL19), loaded by the owning story; the delegation rows for item 2.1.1 are loaded (DL18), and the input age limit for balances in a credit pack is 1 business day (legacy section 3, DL22).
- Case RW-2026-000610 is in route state AWAITING_CREDIT_APPROVAL with treatment TRT-SYN-0610 of type RESTRUCTURE at version 3, the ACE plan status APPROVED, and a synthetic officer holding RW-RESTRUCT for the case in scope.
- The harness environment, its test-data seeding, its evidence format and retention, and its pass/fail gate: Not specified in the source documents (GAP-0394; ASM-0569).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment, records the build ID, the business date and the versions of the contracts it is about to exercise, and seeds the case RW-2026-000610, treatment TRT-SYN-0610 at version 3, the 2 accounts, the 1 collateral with its latest appraisal, plan terms 2,400,000.00 baht / 0.00 baht haircut / 84 installments / valid until 2026-12-29 and the 5 checklist documents through the owning contracts or their fakes, then reads the state back to assert the seed.
2. Harness: seeds the NLEADS checklist rows and the delegation rows for item 2.1.1 through the owning contracts (rwb-case reference data and rwb-access, with the level expected from rwb-decision), so the run starts from data rows and not from constants.
3. Harness: calls the gateway-bff composite credit-pack route for treatment TRT-SYN-0610 and asserts one hop per call with the 2 s budget and no cross-schema read in the trace.
4. Harness: asserts the pack holds case RW-2026-000610, product group MORTGAGE, 2 accounts with balances as of 2026-12-14, 1 collateral with its latest appraisal, the plan terms 2,400,000.00 baht offer / 0.00 baht haircut / 84 installments / valid until 2026-12-29, the 5 checklist documents with a link to each one on the case, and required level L6 (legacy AC1).
5. Harness: records the result through POST /api/recovery/integration/v1/treatments/{treatmentId}/credit-result with reference NL-SYN-000610, result APPROVED, approval level L5 and result date 2026-12-17, and reads the result back through the GET form of the same path.
6. Harness: asserts the D5 decision record with final call approved is written before the treatment state change and the route move by timestamp order, that the treatment carries NL-SYN-000610 with state APPROVED, and that the route state moved AWAITING_CREDIT_APPROVAL to OFFER_WITH_CUSTOMER by R-RES-11 (legacy AC2, BR2).
7. Harness: asserts one CaseStateChanged event on rwb.case.events.v1 and one TreatmentApproved event on rwb.treatment.events.v1 for the change, exactly one outbox row, and that the harness itself wrote none of them.
8. Harness: drives the refusals of §5 in turn — level L6 for a plan that needs L5, a second result, an empty refusal reason, a result date after today, and a case in PLAN_RUNNING — and asserts the message ID with its substituted values and that the treatment, the route state, the decision log and the outbox are unchanged (legacy AC3, AC6 to AC9).
9. Harness: forces the decision-log failure, asserts 503 with MSG-P7-003 and that nothing changed, returns the fake or the service to healthy, records the result once, and asserts exactly one D5 decision record and one event after recovery (legacy AC11, BR8).
10. Harness: repeats the whole journey from the reset state, compares the two runs, writes one run report per business date keyed by story and business date with the trace and the per-assertion result, and evaluates the pass/fail gate; the evidence format, retention and gate: Not specified in the source documents (GAP-0394; ASM-0569).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A checklist document is not on the case (no INCOME_PROOF) | The pack shows INCOME_PROOF as missing with the message and the other 4 documents as present; the case, the treatment and the decision log are unchanged | MSG-P2-009 | TC-E2-006-04-ITG |
| X2 | A balance in the pack is older than its age limit | The pack shows each balance with its age in days from the owning read; no result is recorded by the harness | MSG-P7-006 | TC-E2-006-05-ITG |
| X3 | The reference is empty, or a refusal carries no reason | 422 for the named field; the treatment does not change | MSG-GEN-001 | TC-E2-006-06-ITG |
| X4 | The result date is after today | 422 for the date field; the treatment does not change | MSG-GEN-002 | TC-E2-006-06-ITG |
| X5 | The NLEADS approval level is below the level the plan needs | 409 with the level and the required level substituted; no treatment change, no decision record, no event | MSG-P2-018 | TC-E2-006-07-ITG |
| X6 | A result is already recorded on the treatment | 409 naming the recorded date; no second decision record and no second event | MSG-P2-010 | TC-E2-006-08-ITG |
| X7 | The case is not in AWAITING_CREDIT_APPROVAL, or the treatment is not a restructure | 409 naming the target state and the current state; nothing changes | MSG-P3-005 | TC-E2-006-09-ITG |
| X8 | The treatment changed between read and write | 409 with If-Match version 3; one result saved, the other refused, still one decision record and one event | MSG-GEN-004 | TC-E2-006-10-ITG |
| X9 | The decision-log store is unavailable | 503; the treatment, the route state and the outbox are unchanged and the run records the incident assertion | MSG-P7-003 | TC-E2-006-11-ITG, TC-E2-006-13-ITG |
| X10 | A role without the Treatment and offer right opens the pack or records a result | 403 on a direct call and the composite route hides the action; nothing changes | MSG-P4-002 | TC-E2-006-12-ITG |
| X11 | The seed cannot be loaded, another run holds the environment lock, or the evidence cannot be written | The run refuses to start and names the missing seed item or the lock holder, or is marked failed with the local evidence kept for the rerun; no scenario is reported as passed | None | All |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the five I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the seed data and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The pack, the result, the decision record and the events are proven together across six services instead of per service |
| Estimable | One harness project, one journey specification, one fake pack and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey on synthetic data with a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Credit approval pack for NLEADS - wave 2 integration harness

  Background:
    Given case "RW-2026-000610" is in route state "AWAITING_CREDIT_APPROVAL" with treatment "TRT-SYN-0610" at version 3
    Given treatment "TRT-SYN-0610" is of type "RESTRUCTURE" with offer amount 2,400,000.00 baht, haircut 0.00 baht, 84 installments and valid until 2026-12-29
    Given the ACE plan status of the case is "APPROVED"
    Given the plan needs approval at level "L6" or higher under item 2.1.1
    Given the case holds 2 accounts, 1 collateral with its latest appraisal and the 5 checklist documents

  Scenario: AC1 The composite credit-pack route through gateway-bff returns the pack composed from the owning services (new, D-RCV-60)
    Given the harness calls the composite credit-pack route at "Not specified in the source documents (GAP-0394; ASM-0569)" for treatment "TRT-SYN-0610"
    When gateway-bff composes the answer from rwb-integration, rwb-case, rwb-treatment, rwb-document and rwb-access
    Then the route returns the pack with case "RW-2026-000610", product group "MORTGAGE", 2 accounts with balances as of 2026-12-14, 1 collateral, the plan terms 2,400,000.00 baht offer / 0.00 baht haircut / 84 installments / valid until 2026-12-29, the 5 checklist documents and required level "L6"
    And every call in the composition is one hop with the 2 s budget
    And no service reads another service's schema
    And the run report holds one trace spanning the gateway and each owning service

  Scenario: AC2 The result is recorded once, after the D5 decision record, and moves the treatment and the route (new, D-RCV-60)
    Given the business date is 2026-12-17
    When the harness records result "APPROVED" with reference "NL-SYN-000610", approval level "L5" and result date 2026-12-17 for treatment "TRT-SYN-0610"
    Then one D5 decision record with final call "approved" exists before the treatment state and the route state change
    And the treatment carries reference "NL-SYN-000610" and its state is "APPROVED"
    And the route state moves from "AWAITING_CREDIT_APPROVAL" to "OFFER_WITH_CUSTOMER" by R-RES-11
    And one CaseStateChanged event and one TreatmentApproved event exist and one outbox row exists
    And the harness wrote none of the record, the state, the route, the events or the outbox row itself

  Scenario: AC3 Refusals leave the treatment, the route state, the decision log and the outbox unchanged (new, D-RCV-60)
    Given case "RW-2026-000620" is in route state "PLAN_RUNNING"
    When the harness records result "APPROVED" with approval level "L6" for a plan that needs level "L5"
    Then the answer is 409 with MSG-P2-018
    When the harness records a second result on a treatment that already holds "APPROVED" with reference "NL-SYN-000610" recorded on 2026-12-17
    Then the answer is 409 with MSG-P2-010
    When the harness records result "REFUSED" with reference "NL-SYN-000612" and an empty reason
    Then the answer is 422 with MSG-GEN-001 for field "reason"
    When the harness records a result with result date 2026-12-31 on 2026-12-17
    Then the answer is 422 with MSG-GEN-002
    When the harness records a result for the treatment of case "RW-2026-000620"
    Then the answer is 409 with MSG-P3-005
    And no treatment change, no second decision record and no event exist for any of the five

  Scenario: AC4 Failure isolation and the single successful result after recovery (new, D-RCV-60)
    Given rwb-decision returns "UNAVAILABLE" for the decision-log write
    When the harness records result "APPROVED" with reference "NL-SYN-000613" and approval level "L5" for treatment "TRT-SYN-0610"
    Then the answer is 503 with MSG-P7-003
    And the treatment, the route state and the outbox are unchanged
    When the same result is recorded once after rwb-decision recovers
    Then the result is recorded once and exactly one D5 decision record and one event exist
    And the run report records the incident assertion
```

These four criteria are new for the ITG harness. The legacy "acs" list of RWB-E2-006 is empty, and all 11 legacy criteria are owned by RWB-P2-E2006-APP and the other app stories; this story restates no app criterion and re-implements no business behaviour.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A restructure outside the approved range or with a deviation goes to credit approval | R-RES-10 |
| BR2 | Credit approval releases the offer to the customer with a 14-day validity | R-RES-11 |
| BR3 | A credit refusal records the reason, then returns the case to the route decision for the case owner | R-RES-12, R-RES-14 |
| BR4 | NLEADS has no interface; the officer submits and records the result | INT-26; DL12 |
| BR5 | The approval level must be at or above the level the delegation of authority sets for the decision, product and amount | doa.txt item 2.1.1; CTL-04; DL18 |
| BR6 | The pack documents are those of the NLEADS pack checklist | Document types reference table; DL19 |
| BR7 | An input past its age limit is shown with its age | MSG-P7-006; REQ-RDF-009 |
| BR8 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR9 | A restructure covers every account of the customer in the case | CTL-26 |

The harness asserts these nine rules against the owning services and re-implements none of them, so no BR row is changed by this story. The level, the checklist rows and the age limit stay rows of the owning services; the harness reads them and holds no copy.

### 9. State transitions

None for the case. The harness changes no case status, route state, treatment state, field or outbox row; it writes no decision record and publishes no event. The tables below are what it observes after a call to the owning service.

| From | Event | Condition | To |
|---|---|---|---|
| AWAITING_CREDIT_APPROVAL | CREDIT_APPROVED | final_call = approved | OFFER_WITH_CUSTOMER |
| AWAITING_CREDIT_APPROVAL | CREDIT_DECLINED | final_call = rejected | DECLINED_BY_CREDIT |
| DECLINED_BY_CREDIT | DECLINE_RECORDED | Any | BACK_TO_ROUTE_DECISION |

| Observed on the treatment | Before the call | After an approved result | After a refused result |
|---|---|---|---|
| state | SUBMITTED | APPROVED | REFUSED |
| nleads_ref, approval_level, credit_result_at | empty | NL-SYN-000610, L5, 2026-12-17 | the recorded reference, level and date |
| credit_result_reason | empty | empty | the refusal reason |

The run has states of its own only: Not started, Seeding, Running, Passed, Failed, with the latest run for a build deciding the gate. A failed run leaves every observed row exactly as it was before the call.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer | The synthetic user the harness drives: opens the pack and records the result (Treatment and offer, CRUA) |
| RW-CASEOWN, case owner | Opens the pack and records the result on cases in scope (Treatment and offer, CRU); used for the case in PLAN_RUNNING |
| RW-CREDCOMM, RW-PRODHEAD | Read the pack and the result only (Treatment and offer, RA); they approve in NLEADS, not in this story |
| SY-RULES, Drools evaluator | Supplies the required level and the rule answer through the rwb-decision contract; the harness asserts it, it does not act for it |
| SY-CASEWF, case workflow module | Moves the case route state and writes the event and the outbox row (Queue and allocation CRU); the harness asserts the result |
| SY-DECLOG, decision log writer | Writes the D5 entry the harness reads back (Decision log C) |
| RW-ADMIN, Platform administrator | Runs the pipeline and the rerun, holds the environment lock and the report access; no business action |
| Approval levels L1 to L6 | As in doa.txt item 2.1.1, recorded from NLEADS; the harness seeds the level, it never approves |

No approval level is exercised as an approval in this story: the officer records the level NLEADS returned. Authorisation is answered by rwb-access through the authorise operation of §12.2, and the harness never acts for a role.

### 11. Data

The harness owns no table. It seeds and reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read through rwb-case contract |
| DF-CAS-003 | recovery_case | product_group | Read through rwb-case contract |
| DF-CAS-007 | recovery_case | route_state | Read through rwb-case contract; written by rwb-case on the result, never by the harness |
| DF-ACE-002 | v_ace_account | account_code | Read through the owning service's contract |
| DF-ACC-009 | v_ace_account | principal_outstanding | Read through the owning service's contract (Section B, RWB-ACE-001) |
| DF-ACC-010 | v_ace_account | interest_outstanding | Read through the owning service's contract (Section B, RWB-ACE-001) |
| DF-ACE-020 | v_ace_account | total_balance | Read through the owning service's contract |
| DF-ACE-018 | v_ace_account | days_past_due | Read through the owning service's contract |
| DF-ACE-036 | v_ace_account | data_as_of | Read through the owning service's contract |
| DF-ACE-091 | v_ace_collateral | collateral_no | Read through the owning service's contract |
| DF-ACE-097 | v_ace_collateral | collateral_type | Read through the owning service's contract |
| DF-ACE-191 | v_ace_valuation | appraised_value | Read through the owning service's contract |
| DF-ACE-193 | v_ace_valuation | appraisal_date | Read through the owning service's contract |
| DF-DOC-001 | document | id | Read through rwb-document contract |
| DF-DOC-004 | document | document_type | Read through rwb-document contract |
| DF-TRT-001 | treatment | id | Read through rwb-treatment contract |
| DF-TRT-003 | treatment | decision_log_id | Read through rwb-treatment contract; written by the owner |
| DF-TRT-004 | treatment | treatment_type | Read through rwb-treatment contract |
| DF-TRT-007 | treatment | offer_amount | Read through rwb-treatment contract |
| DF-TRT-008 | treatment | haircut_amount | Read through rwb-treatment contract |
| DF-TRT-009 | treatment | installments | Read through rwb-treatment contract |
| DF-TRT-010 | treatment | valid_until | Read through rwb-treatment contract |
| DF-TRT-011 | treatment | approval_level | Read through rwb-treatment contract; written by the owner on the result |
| DF-TRT-023 | treatment | nleads_ref | Read through rwb-treatment contract; written by the owner on the result |
| DF-TRT-024 | treatment | credit_result | Read through rwb-treatment contract; written by the owner on the result |
| DF-TRT-025 | treatment | credit_result_reason | Read through rwb-treatment contract; written by the owner on the result |
| DF-TRT-026 | treatment | credit_result_at | Read through rwb-treatment contract; written by the owner on the result |
| Standard column | treatment | state | Read through rwb-treatment contract; written by the owner |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through rwb-decision contract |

No service reads another service's schema and the harness reads no schema at all. The ACE account, collateral and valuation data is read only through the owning contract, never from a view directly, and synthetic data only is used. No production case, account, party or document is copied, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/integration/v1/treatments/{treatmentId}/credit-pack` | P2 rwb-integration | The composite credit pack for treatment TRT-SYN-0610: case, accounts, collateral, valuation, plan terms, documents and required level (AC1) |
| POST | `/api/recovery/integration/v1/treatments/{treatmentId}/credit-result` | P2 rwb-integration | Records reference NL-SYN-000610, result APPROVED, approval level L5 and result date 2026-12-17 (AC2, AC3, AC4) |
| GET | `/api/recovery/integration/v1/treatments/{treatmentId}/credit-result` | P2 rwb-integration | Reads back the recorded result, the reference and the level after the call (AC2, AC4) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The D5 decision record with final call approved, read to assert it precedes the treatment and the route change (AC2, AC4) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment state, type, terms, reference, result, level and reason after the call (AC1, AC2, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case number, product group and route state before and after the result (AC1, AC2, AC3) |
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` | P5 rwb-document | The 5 checklist documents, each present with its link or shown as missing (AC1, AC3) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The document link target of each present checklist item (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and Treatment and offer right used by the composite route and by the direct call (AC1, AC3, TC-E2-006-12-ITG) |

The composite credit-pack route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0394; ASM-0569).

#### 12.3 Events published

None. The harness produces no event; its fixtures produce none either.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision (shared ledger) | The D5 record of the result reaches the shared topic inside the run window and names final call approved and the NLEADS reference (AC2, AC4) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | One event per successful result with the case, the from and to route state and the rule R-RES-11 (AC2, AC3, AC4) |
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 rwb-treatment | One event per successful approval carrying the treatment, the reference and the level (AC2, AC3, AC4) |

Consumers dedupe through their own inbox table; the harness consumes with its own group and never asserts a producer's outbox row except the single outbox row of the change, which it reads through the owning contract.

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity or Nexus operation; it drives REST only and observes the treatment and route change of the case workflow through the owning contracts.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-integration | credit-pack, credit-result (POST and GET) | The pack of AC1 with case RW-2026-000610, product group MORTGAGE, 2 accounts with balances as of 2026-12-14, 1 collateral, the plan terms, the 5 documents and required level L6; 200 with the recorded result on POST; 409 for MSG-P2-018, MSG-P2-010, MSG-P3-005 and MSG-GEN-004; 422 for MSG-GEN-001 and MSG-GEN-002; 503 with MSG-P7-003 for the decision-log failure |
| rwb-decision | decision-log | The D5 record with final call approved and the NLEADS reference; a forced decision-log write failure for the 503 case; a healthy answer after recovery |
| rwb-treatment | treatments/{treatmentId} | TRT-SYN-0610 of type RESTRUCTURE, state SUBMITTED at version 3, offer amount 2,400,000.00 baht, haircut 0.00 baht, 84 installments, valid until 2026-12-29; APPROVED with NL-SYN-000610 after the call; REFUSED with the reason for the refusal case |
| rwb-case | cases/{caseId} | RW-2026-000610 in AWAITING_CREDIT_APPROVAL with product group MORTGAGE, and OFFER_WITH_CUSTOMER after the approved result; RW-2026-000620 in PLAN_RUNNING |
| rwb-document | cases/{caseId}/document-checklist, documents/{documentId} | The 5 checklist documents with their links; INCOME_PROOF shown as missing for the X1 case |
| rwb-access | authorise | Allow RW-RESTRUCT with Treatment and offer U in scope; refuse RW-PHONECOL with MSG-P4-002 |

The fakes are replaced by the real service as each of the five I stories lands, contract by contract. The harness repository, environment, seeding, evidence format and gate: Not specified in the source documents (GAP-0394; ASM-0569).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | The nine consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.decision-record.DecisionRecorded.v1, rwb.case.CaseStateChanged.v1 and rwb.treatment.TreatmentApproved.v1; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity; it observes the treatment and route change through the owning contracts |
| File | No | Reads and writes no file itself; the run report is written by the reporter of §13, not by a service file path |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the five I stories, and each fake is replaced by the real service as its I story lands.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs the ten flow steps for one scenario and one business date, holds the run lock, records the build ID and stops at the first failed assertion with the trace |
| CompositeRouteClient | Harness adapter | Calls the gateway-bff composite credit-pack route and the nine consumed operations of §12.2, with the 2 s budget per call and If-Match version 3 on the result POST |
| FakePack | WireMock project | Serves rwb-integration, rwb-decision, rwb-treatment, rwb-case, rwb-document and rwb-access from the published OpenAPI documents of §12.8 |
| DecisionOrderCheck | Assertion | Reads the D5 decision record, the treatment and the route state and fails the run when the record does not precede the two changes, or when there is more than one record for one result |
| RefusalCheck | Assertion | Drives the refusals of §5 and fails the run on any change to the treatment, the route state, the decision log or the outbox |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0394; ASM-0569) |

**Environment and test data**

- Environment: SIT, one namespace, the owning services deployed from their wave 2 builds or replaced by the §12.8 fakes, with gateway-bff in front. Harness repository, environment and data seeding: Not specified in the source documents (GAP-0394; ASM-0569).
- Data: synthetic case RW-2026-000610 and case RW-2026-000620, treatment TRT-SYN-0610 of type RESTRUCTURE at version 3, 2 accounts with balances as of 2026-12-14, 1 collateral with its latest appraisal, the plan terms 2,400,000.00 baht offer / 0.00 baht haircut / 84 installments / valid until 2026-12-29, the 5 checklist documents CREDIT_APPLICATION, ID_COPY, TITLE_DEED, LATEST_APPRAISAL and INCOME_PROOF, required level L6, recorded level L5, references NL-SYN-000610, NL-SYN-000611, NL-SYN-000612 and NL-SYN-000613, result dates 2026-12-17 and 2026-12-31, and the business dates 2026-12-15 and 2026-12-17. No production record is copied.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and CompositeRouteClient against the published OpenAPI documents of the owning services, with the run lock and the build ID.
2. Publish FakePack for the six services from the same documents, and prove the harness runs green from Day 1 on the fakes with the reset state.
3. Add the composite route assertion of AC1 with the one-hop and 2 s budget check, the no-cross-schema check and the single trace in the run report.
4. Add the result journey of AC2 with DecisionOrderCheck: the D5 record first, then the treatment state, the reference and the level, then the route move, then one event of each kind and one outbox row.
5. Add the refusal set of AC3 with RefusalCheck for MSG-P2-018, MSG-P2-010, MSG-GEN-001, MSG-GEN-002 and MSG-P3-005, and add the version conflict of X8 with If-Match version 3.
6. Add the failure isolation of AC4 with a forced decision-log failure, then the single successful result after recovery, keeping the incident assertion in the report.
7. Add the missing-document and stale-balance assertions of X1 and X2, and the access refusal of X10.
8. Replace each fake with the real service as its I story lands, then publish the run report per business date and the pass/fail gate; the gate definition: Not specified in the source documents (GAP-0394; ASM-0569).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.integration.nleads-pack` from the legacy solution plan; with it off the credit-pack and credit-result operations are not offered and the composite route hides the action, and the harness asserts that disabled state and the enabled state.

**Done when:** the journey runs green against the five deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, the D5 record precedes the treatment and route change with one event of each kind and one outbox row, and the pass/fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-009 | A checklist document is missing from the pack | The credit approval pack is missing {item}. Add it to the case before you submit in NLEADS. |
| MSG-P7-006 | An input is past its age limit | {input} is {days} days old, past its limit. Refresh it before you decide. |
| MSG-GEN-001 | Reference or refusal reason empty | Enter {field}. |
| MSG-GEN-002 | Result date after today | {field} must be between {min} and {max}. |
| MSG-P2-018 | NLEADS approval level below the required level | The NLEADS approval is at level {level}. This plan needs level {required} or higher. |
| MSG-P2-010 | Result already recorded | The NLEADS result for this treatment was recorded on {date}. |
| MSG-P3-005 | Case not awaiting credit approval | This case cannot move to {state} from {current}. |
| MSG-GEN-004 | Treatment changed by someone else | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values; it does not own the message text. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-14 Treatment record | Submitted | The composite route returns the pack panel with case RW-2026-000610, 2 accounts, 1 collateral, the plan terms, the 5 documents and required level L6, and the result form is offered to RW-RESTRUCT |
| SCR-14 Treatment record | Missing items | The pack shows INCOME_PROOF as missing with MSG-P2-009 and the other 4 items as present |
| SCR-14 Treatment record | Stale inputs | Each balance past its age limit carries MSG-P7-006 with its age in days |
| SCR-14 Treatment record | Approved | The answer carries the treatment with state APPROVED, reference NL-SYN-000610 and level L5, and the route state OFFER_WITH_CUSTOMER |
| SCR-14 Treatment record | Refused | The answer carries the treatment with state REFUSED, the reason, and the route DECLINED_BY_CREDIT then BACK_TO_ROUTE_DECISION |

The harness opens no screen and renders no page; it asserts the composite route answer and the owning contracts that the screen consumes. Screen-level behaviour remains with the owning APP stories. The harness environment and evidence detail: Not specified in the source documents (GAP-0394; ASM-0569).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-006-01-ITG | AC1, BR6, BR9 | Integration | Synthetic case with 2 accounts, 1 collateral and 5 checklist documents |
| TC-E2-006-02-ITG | AC2, BR2 | Integration | Result APPROVED at level L5 |
| TC-E2-006-03-ITG | AC3, BR3 | Integration | Result REFUSED with a reason |
| TC-E2-006-04-ITG | AC4, BR6 | Integration | No INCOME_PROOF document |
| TC-E2-006-05-ITG | AC5, BR7 | Integration | Account load of 2026-12-12 |
| TC-E2-006-06-ITG | AC6 | Integration | Empty reason; result date in the future |
| TC-E2-006-07-ITG | AC7, BR5 | Integration | Level L6 for a plan that needs L5 |
| TC-E2-006-08-ITG | AC8 | Integration | Result recorded twice |
| TC-E2-006-09-ITG | AC9, BR1 | Integration | Case in PLAN_RUNNING |
| TC-E2-006-10-ITG | AC10 | Integration | Two results with If-Match version 3 |
| TC-E2-006-11-ITG | AC11, BR8 | Integration | Decision log store stopped during a result |
| TC-E2-006-12-ITG | Access | Component | RW-PHONECOL calls POST /treatments/{treatmentId}/credit-result; refused with MSG-P4-002 |
| TC-E2-006-13-ITG | Principle 5 | NFR | Decision log write forced to fail; treatment and route state unchanged; MSG-P7-003 |

The full legacy test, with its Given, When and Then, is in the legacy test case workbook under the legacy test case ID; the Covers column names the legacy AC of RWB-E2-006 that the ITG copy is derived from. The Level column maps the legacy System level to Integration, the legacy Access level to Component and the legacy Resilience level to NFR. The four ACs of §7 are the harness's own and are exercised across these thirteen copies.

### 17. Guardrails

- No business value in code: the checklist, the age limit and the levels are rows of the owning services; the harness reads them and holds no copy.
- No personal data in logs, events, workflow inputs, traces or reports: the refusal reason is not logged, the events carry identifiers and codes only, and the harness uses synthetic parties.
- No read of another service's schema and no direct ACE read: every read goes through the owner's contract, the trace check fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No second rule engine: the required level and the rule answer are read through the rwb-decision contract, and no caller reads the workbook, the DRL source or a rule row.
- The decision record is written before the treatment or the route state changes; DecisionOrderCheck fails the run when it is not, so a result that cannot be logged does not proceed.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner, or a call that exceeds the 2 s budget.
- No call to NLEADS from the Workbench and none from the harness: the officer submits outside the system and records the result; the harness records only the synthetic reference and result.
- No production data and no outside system: the harness calls only the owning services and their fakes, never an outside gateway, UAT or production.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Plan submitted for credit approval recorded on the case | Business Requirements Program, section 5.3; Epic 2, section 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-RES-10, R-RES-11, R-RES-12, R-RES-14, R-UNI-39 | TC-E2-006-02-ITG, TC-E2-006-03-ITG, TC-E2-006-06-ITG to TC-E2-006-11-ITG, TC-E2-006-13-ITG |
| REQ-CHO-006 | Treatment holds type, terms, approval and outcome | Business Requirements Program, section 5.3; Epic 2, section 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-006-01-ITG, TC-E2-006-04-ITG, TC-E2-006-05-ITG |
| REQ-RDF-009 | Every decision records the freshness of the data it used | Business Requirements Epic 1, section 4 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | None (asserted through BR7 and MSG-P7-006) | TC-E2-006-01-ITG, TC-E2-006-05-ITG |

REQ-CHO-008 and REQ-CHO-006 are carried at the integration level by the pack, the result and the events this harness asserts; REQ-RDF-009 is carried by the input age in the pack and the freshness the owning services record. This story adds no requirement ID of its own and restates no rule.

### 19. Out of scope

- The five owning I stories RWB-P3-E2004-APP, RWB-P2-E2006-APP, RWB-P7-E2006-APP, RWB-S2-E2006-APP and RWB-P3-E2006-APP, and every screen, endpoint, table, migration, rule and workflow they build.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-integration, rwb-decision, rwb-treatment, rwb-case, rwb-document and rwb-access, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- NLEADS itself: the submission of the plan, its approval and any interface to NLEADS (INT-26).
- Generating a credit application document from a template (RWB-E2-026).
- Booking the plan in NLEADS and ALS and its confirmation (RWB-E2-007 and Epic 3).
- Approval inside the Workbench for decisions within the delegation (RWB-E2-013).
- The other legacy journeys of this wave, and the CON and OPS stories of the same legacy key.
