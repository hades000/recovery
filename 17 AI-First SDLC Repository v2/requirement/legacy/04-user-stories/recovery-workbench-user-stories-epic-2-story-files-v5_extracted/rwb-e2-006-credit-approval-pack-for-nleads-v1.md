<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 006 Credit approval pack for NLEADS v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 006 Credit approval pack for NLEADS v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-006 Credit approval pack for NLEADS

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-006 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CHO-07 Prepare the credit approval pack for NLEADS |
| Requirement IDs | REQ-CHO-008, REQ-CHO-006 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, section 5.3 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D5, D6.4 |
| Priority | Must |
| Depends on | RWB-E2-004, RWB-E1-007 |
| Status | Ready for build |

## 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the credit approval pack for an approved plan prepared from the case for submission in NLEADS, and the NLEADS reference and result recorded on the treatment**, so that **a plan reaches credit without re-keying the case facts and the case moves on the credit result**.

## 2. Business rationale

A restructure outside the approved range goes to credit approval (R-RES-10), which the bank decides in NLEADS. Officers re-key the case facts and the plan terms into NLEADS today and the result is not on the case. NLEADS has no interface (INT-26), so this story assembles the pack from the case for the officer to submit, and records the NLEADS reference, result and approval level on the treatment, which moves the case by R-RES-11 or R-RES-12. It meets REQ-CHO-008 and REQ-CHO-006 and supports CTL-04.

## 3. Preconditions

- RWB-E2-004 (treatment entity and plan timers) and RWB-E1-007 (adapters) are done.
- The case is in route state AWAITING_CREDIT_APPROVAL with an open RESTRUCTURE treatment, and its ACE plan status is APPROVED (RWB-E2-002).
- The NLEADS pack checklist is loaded as reference data (DL19; assumed items: CREDIT_APPLICATION, ID_COPY, TITLE_DEED, LATEST_APPRAISAL, INCOME_PROOF).
- The delegation of authority rows for item 2.1.1 are loaded (DL18).
- The input age limit for balances in a credit pack is 1 business day (assumed; DL22).
- The person holds RW-RESTRUCT with the case in scope.

## 4. Flow

1. Restructuring officer: opens SCR-14 Treatment record and selects the credit approval pack.
2. Front end: calls GET /treatments/{treatmentId}/credit-pack.
3. System: checks the Treatment and offer right and the case scope; reads the case, accounts, collateral, latest valuation, plan terms and documents through the owning modules' interfaces and the P1 interfaces over the ACE views.
4. System: reads the required approval level for the plan from the P7 DelegationQuery and the pack checklist rows.
5. System: returns the pack with each field ready to copy, the documents present with links, each missing checklist item, and the age of each input.
6. Restructuring officer: submits the plan in NLEADS and receives the NLEADS reference and later the result.
7. Restructuring officer: records the NLEADS reference, result, approval level, result date and, for a refusal, the reason.
8. System: validates the input and the treatment version; writes the decision log entry with decision D5, final call and the NLEADS reference in the actions.
9. System: writes the reference, result, reason, approval level and state on the treatment and raises CREDIT_APPROVED or CREDIT_DECLINED to P3.
10. SY-RULES and SY-CASEWF: an approval releases the offer to the customer (R-RES-11); a refusal records the reason (R-RES-12) and returns the case to the route decision in the case owner's queue (R-RES-14).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A checklist document is not on the case | The pack shows the item as missing | MSG-P2-009 | AC4 |
| X2 | A balance in the pack is older than its age limit | The pack shows the input age | MSG-P7-006 | AC5 |
| X3 | Reference empty, or a refusal without a reason | Refused; nothing changes | MSG-GEN-001 | AC6 |
| X4 | Result date after today | Refused | MSG-GEN-002 | AC6 |
| X5 | The NLEADS approval level is below the level the plan needs | Refused; nothing changes | MSG-P2-018 | AC7 |
| X6 | A result is already recorded on the treatment | Refused | MSG-P2-010 | AC8 |
| X7 | The case is not in AWAITING_CREDIT_APPROVAL or the treatment is not a restructure | Refused | MSG-P3-005 | AC9 |
| X8 | The treatment changed between read and write | Refused | MSG-GEN-004 | AC10 |
| X9 | The decision log write fails | Nothing changes; an incident is raised | MSG-P7-003 | AC11 |
| X10 | A role without the Treatment and offer right opens the pack or records a result | Refused; nothing changes | MSG-P4-002 | TC-E2-006-12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the treatment entity (RWB-E2-004) and the plan status (RWB-E2-002) |
| Negotiable | The checklist, age limit and levels are data rows |
| Valuable | Removes re-keying into NLEADS and puts the credit result on the case |
| Estimable | Two endpoints, one service, one React panel |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: Credit approval pack for NLEADS

  Background:
    Given case "RW-2026-000610" is in route state "AWAITING_CREDIT_APPROVAL"
    Given treatment "TRT-SYN-0610" of type "RESTRUCTURE" has offer amount 2,400,000.00 baht, haircut 0.00 baht and 84 installments
    Given the ACE plan status of the case is "APPROVED"
    Given the plan needs approval at level "L6" or higher under item 2.1.1

  Scenario: AC1 Pack prepared
    Given an approved restructure plan on treatment "TRT-SYN-0610"
    When the officer opens the credit approval pack on 2026-12-15
    Then the pack holds case number "RW-2026-000610", product group "MORTGAGE", 2 accounts with balances as of 2026-12-14 and 1 collateral with its latest appraisal
    Then the pack holds the plan terms: offer amount 2,400,000.00 baht, haircut 0.00 baht, 84 installments, valid until 2026-12-29
    Then the pack lists the 5 checklist documents with a link to each one on the case
    Then the system shows the required approval level "L6"
    Then no field in the pack needs to be typed by the officer

  Scenario: AC2 Result recorded
    Given the officer has submitted the pack in NLEADS
    When the officer records NLEADS reference "NL-SYN-000610", result "APPROVED", approval level "L5" and result date 2026-12-17
    Then the treatment carries the reference "NL-SYN-000610" and its state is "APPROVED"
    Then a decision log entry with decision "D5" and final call "approved" holds the NLEADS reference
    Then the route state moves to "OFFER_WITH_CUSTOMER" by R-RES-11

  Scenario: AC3 Refused
    Given NLEADS refuses the plan with reason "Income does not cover 84 installments"
    When the officer records reference "NL-SYN-000611", result "REFUSED" and the reason
    Then the treatment state is "REFUSED" and the treatment shows the reason
    Then the route state moves to "DECLINED_BY_CREDIT" by R-RES-12 and then to "BACK_TO_ROUTE_DECISION" by R-RES-14
    Then the case is in the case owner's queue

  Scenario: AC4 Missing checklist document
    Given the case holds no document of type "INCOME_PROOF"
    When the officer opens the pack
    Then the pack shows "INCOME_PROOF" as missing with message MSG-P2-009
    Then the other 4 documents show as present

  Scenario: AC5 Stale balance
    Given the last account load for the case is for business date 2026-12-12 and today is 2026-12-15
    When the officer opens the pack
    Then each balance shows message MSG-P7-006 with 3 days

  Scenario: AC6 Invalid input
    When the officer records result "REFUSED" with reference "NL-SYN-000612" and an empty reason
    Then the response is 422 with message MSG-GEN-001 for field "reason"
    Then a result with result date 2026-12-31 on 2026-12-17 returns 422 with message MSG-GEN-002
    Then the treatment does not change

  Scenario: AC7 Approval level below the required level
    When the officer records result "APPROVED" with approval level "L6" for a plan that needs level "L5"
    Then the response is 409 with message MSG-P2-018
    Then the treatment does not change

  Scenario: AC8 Result recorded twice
    Given the treatment holds result "APPROVED" with reference "NL-SYN-000610" recorded on 2026-12-17
    When the officer records a result again
    Then the response is 409 with message MSG-P2-010
    Then the system writes no second decision log entry

  Scenario: AC9 Case not awaiting credit approval
    Given case "RW-2026-000620" is in route state "PLAN_RUNNING"
    When the officer records a result for its treatment
    Then the response is 409 with message MSG-P3-005

  Scenario: AC10 Two officers record at once
    Given two officers read treatment "TRT-SYN-0610" at version 3
    When both record a result with If-Match version 3
    Then the system saves one result
    Then the system refuses the other with 409 and message MSG-GEN-004

  Scenario: AC11 Decision log write fails
    Given the decision log store is unavailable
    When the officer records result "APPROVED" with reference "NL-SYN-000613" and approval level "L5"
    Then the response is 503 with message MSG-P7-003
    Then the treatment and the route state do not change
    Then the system raises an incident
```

## 8. Business rules

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

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| AWAITING_CREDIT_APPROVAL | CREDIT_APPROVED | final_call = approved | OFFER_WITH_CUSTOMER |
| AWAITING_CREDIT_APPROVAL | CREDIT_DECLINED | final_call = rejected | DECLINED_BY_CREDIT |
| DECLINED_BY_CREDIT | DECLINE_RECORDED | Any | BACK_TO_ROUTE_DECISION |

The case status moves from "Waiting approval" to "In progress" (status transition: approver accepts or rejects). The treatment state moves from SUBMITTED to APPROVED or REFUSED.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer | Opens the pack and records the result (Treatment and offer, CRUA) |
| RW-CASEOWN, case owner | Opens the pack and records the result on cases in scope (Treatment and offer, CRU) |
| RW-CREDCOMM, RW-PRODHEAD | Read the pack and the result (Treatment and offer, RA); they approve in NLEADS, not in this story |
| SY-RULES, SY-CASEWF | Evaluate R-RES-11, R-RES-12, R-RES-14 and move the case |
| SY-DECLOG, decision log writer | Writes the entry (Decision log, C) |
| Approval levels L1 to L6 | As in doa.txt item 2.1.1, recorded from NLEADS |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-007 | recovery_case | route_state | Read; write through the P3 interface |
| DF-ACE-002 | v_ace_account | account_code | Read |
| DF-ACC-009 | v_ace_account | principal_outstanding | Read (Section B, RWB-ACE-001) |
| DF-ACC-010 | v_ace_account | interest_outstanding | Read (Section B, RWB-ACE-001) |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-091 | v_ace_collateral | collateral_no | Read |
| DF-ACE-097 | v_ace_collateral | collateral_type | Read |
| DF-ACE-191 | v_ace_valuation | appraised_value | Read |
| DF-ACE-193 | v_ace_valuation | appraisal_date | Read |
| DF-DOC-001 | document | id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-008 | treatment | haircut_amount | Read |
| DF-TRT-009 | treatment | installments | Read |
| DF-TRT-010 | treatment | valid_until | Read |
| DF-TRT-011 | treatment | approval_level | Write |
| DF-TRT-023 | treatment | nleads_ref | Write |
| DF-TRT-024 | treatment | credit_result | Write |
| DF-TRT-025 | treatment | credit_result_reason | Write |
| DF-TRT-026 | treatment | credit_result_at | Write |
| Standard column | treatment | state | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

Both endpoints are new and recorded in the additions file.

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /treatments/{treatmentId}/credit-pack | Path: treatmentId | CreditPack: caseNo, productGroup, accounts (accountNo, principal, interest, totalBalance, daysPastDue, dataAsOf, ageDays), collateral (collateralNo, type, appraisedValue, appraisalDate), terms (offerAmount, haircutAmount, installments, validUntil), requiredLevel, documents (type, documentId or missing), messages | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 a source interface unavailable (MSG-GEN-006) | Treatment and offer, R | Read only |
| POST /treatments/{treatmentId}/credit-result | CreditResult: nleadsRef (1 to 30 letters, digits and dashes; format assumed until SCB IT confirms, DL12), result (APPROVED or REFUSED), approvalLevel (L1 to L6), resultDate, reason (1 to 1,000 characters, required when REFUSED); header If-Match | 200 Treatment | 401; 403 (MSG-P4-002); 404 (MSG-P4-003); 409 state (MSG-P3-005), already recorded (MSG-P2-010), level too low (MSG-P2-018), version (MSG-GEN-004); 422 (MSG-GEN-001, MSG-GEN-002); 503 decision log (MSG-P7-003) | Treatment and offer, U | One result per treatment; a repeat returns 409 and writes nothing |

**Published interfaces called.**

```java
// P7 recovery.decision.api
String DelegationQuery.requiredLevel(String decisionCode, String productGroup, BigDecimal amount);
UUID DecisionLogWriter.write(DecisionLogRequest request); // throws DecisionLogUnavailableException
// P3 recovery.casewf.api
void CaseEvents.raise(UUID caseId, String eventCode, Map<String, Object> facts);
// S2 or P3 treatment interface from RWB-E2-004
TreatmentView TreatmentQuery.get(UUID treatmentId);
TreatmentView TreatmentCommands.recordCreditResult(UUID treatmentId, CreditResultCommand command, int expectedVersion);
// P5 recovery.documents.api
List<DocumentRef> CaseDocuments.byTypes(UUID caseId, Set<String> documentTypes);
```

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/nleads`, Java package `recovery.integration.nleads`; front end `src/modules/recovery/treatment/CreditPackPanel.tsx`.

| Component | Type | Responsibility |
|---|---|---|
| CreditPackController | Controller | The two endpoints; validation; problem responses |
| CreditPackService | Service | Assembles the pack from the P1, P3, P5 and treatment interfaces; checklist and input age |
| CreditResultService | Service | Validates the result, checks the level, writes the decision log entry first, records the result, raises the rule event |
| NleadsChecklist | Rule table | Versioned rows of the document types in the pack |
| CreditPackPanel | React component | Read-only pack with a copy action per field, missing items and input ages |
| CreditResultForm | React component | Reference, result, level, date and reason, with field errors |

- **Database:** the four new treatment columns (nleads_ref varchar(30), credit_result varchar(10), credit_result_reason varchar(1000), credit_result_at timestamptz) are added by the treatment owner in its migration for this story, with a check that credit_result_reason is not null when credit_result = 'REFUSED'. No P2 table.
- **Configuration and reference data:** NLEADS pack checklist rows (business lead with Legal, DL19); delegation rows for item 2.1.1 (Risk, DL18); input age limit for balances 1 business day (assumed; DL22).
- **Build steps:**
  1. Build CreditPackService against stubs of the source interfaces, with a test per pack section.
  2. Add the checklist and input age messages.
  3. Build CreditResultService validation and the level check with DelegationQuery.
  4. Write the decision log entry before the treatment change; handle DecisionLogUnavailableException with no change.
  5. Record the result through TreatmentCommands with the version check; raise CREDIT_APPROVED or CREDIT_DECLINED, then DECLINE_RECORDED on a refusal.
  6. Build the two endpoints with the access and scope checks.
  7. Build CreditPackPanel and CreditResultForm on SCR-14.
- **Feature flag:** `rwb.integration.nleads-pack`.
- **Done when:** the tests in section 16 pass and a SIT tester submits a synthetic plan to the NLEADS test system from the pack alone.

## 14. Validation and messages

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

## 15. Screens and states

SCR-14 Treatment record. In state submitted, the officer opens the credit approval pack, copies each field into NLEADS and opens each document link; missing items and stale inputs show their messages. The officer records the result in the result form; the screen moves to state approved, or shows the refusal reason and the case leaves the officer's view for the case owner's queue.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-006-01 | AC1, BR6, BR9 | System | Synthetic case with 2 accounts, 1 collateral and 5 checklist documents |
| TC-E2-006-02 | AC2, BR2 | System | Result APPROVED at level L5 |
| TC-E2-006-03 | AC3, BR3 | System | Result REFUSED with a reason |
| TC-E2-006-04 | AC4, BR6 | System | No INCOME_PROOF document |
| TC-E2-006-05 | AC5, BR7 | System | Account load of 2026-12-12 |
| TC-E2-006-06 | AC6 | System | Empty reason; result date in the future |
| TC-E2-006-07 | AC7, BR5 | System | Level L6 for a plan that needs L5 |
| TC-E2-006-08 | AC8 | System | Result recorded twice |
| TC-E2-006-09 | AC9, BR1 | System | Case in PLAN_RUNNING |
| TC-E2-006-10 | AC10 | System | Two results with If-Match version 3 |
| TC-E2-006-11 | AC11, BR8 | System | Decision log store stopped during a result |
| TC-E2-006-12 | Access | Access | RW-PHONECOL calls POST /treatments/{treatmentId}/credit-result; refused with MSG-P4-002 |
| TC-E2-006-13 | Principle 5 | Resilience | Decision log write forced to fail; treatment and route state unchanged; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the checklist, age limit and levels are rows.
- No personal data in logs, tests or prompts; the refusal reason is not written to application logs.
- No read of another module's tables; every pack section comes from its owner's interface.
- No call to NLEADS from the Workbench; the officer submits.
- The decision log entry is written before the treatment or the case changes.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Plan submitted for credit approval recorded on the case | Program 5.3; Epic 2 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-RES-10, R-RES-11, R-RES-12, R-RES-14, R-UNI-39 | TC-E2-006-02, TC-E2-006-03, TC-E2-006-06 to TC-E2-006-11, TC-E2-006-13 |
| REQ-CHO-006 | Treatment holds type, terms, approval and outcome | Program 5.3; Epic 2 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-006-01, TC-E2-006-04, TC-E2-006-05 |

## 19. Out of scope

- Generating a credit application document from a template: RWB-E2-026.
- Booking the plan in NLEADS and ALS and its confirmation: RWB-E2-007 and Epic 3 (R-RES-21, R-RES-22).
- Approval inside the Workbench for decisions within the delegation: RWB-E2-013.
