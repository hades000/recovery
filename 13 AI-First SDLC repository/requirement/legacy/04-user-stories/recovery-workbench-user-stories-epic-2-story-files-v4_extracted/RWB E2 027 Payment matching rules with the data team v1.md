<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 027 Payment matching rules with the data team v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 027 Payment matching rules with the data team v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-027 Payment matching rules with the data team

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-027 |
| Epic | E2, release 31 December 2026 |
| Module | P8 Payments and posting |
| Feature | FEAT-OCC-10 Match a payment to the plan; FEAT-PAY-01 Match a payment to a plan installment |
| Requirement IDs | REQ-CHO-009 |
| BRD section | Business Requirements Epic 2, sections 3.8 and 4 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D5 |
| Priority | Must |
| Depends on | RWB-E2-008 |
| Status | Ready for build |

## 1. Story

As a **Credit Administration officer (RW-CREDITAD)**, I want **the matching rules for amount, date window and partial payments held as versioned data and run by the matching engine, with the exception list for what does not match**, so that **most payments match without a person and the rest are listed**.

## 2. Business rationale

The exact rule of RWB-E2-008 leaves short and late installments on the exception list, and a person matches them by hand each morning. This story adds the PARTIAL and WINDOW rules as rows in payment_match_rule, applies them in priority order, records each match in the decision log with the rule version, and lets Credit Administration change a window or tolerance through a reference load with no code release. It serves REQ-CHO-009, control CTL-41 and the FSD P8 measure "receipts matched the same day".

## 3. Preconditions

- RWB-E2-008 is done: JOB-07, the proceeds table, payment_match_rule with the EXACT row and the exception list are live.
- RWB-E1-027 is done: the decision log writer accepts D5 entries.
- TreatmentApi records an installment shortfall (RWB-E2-004).
- Parameter version "PM-2026.12" is in force with rows EXACT, WINDOW and PARTIAL, loaded by the reference data administrator and approved by Credit Administration.
- The reader holds RW-CREDITAD or another role with Write-off and posting R.

## 4. Flow

1. Reference data administrator: loads a parameter version through POST /admin/reference-loads with table "payment_match_rule" and a valid from date.
2. System: checks each row: match type in the list, tolerance between 0 and 100, window days 0 or more, unique priority within the version, approver present; any failure refuses the whole load.
3. JOB-07: for the business date, reads the parameter version in force on that date.
4. System: for each payment, tries the rows in priority order (EXACT, then WINDOW, then PARTIAL) against each running plan on the case; the first row that matches decides.
5. System: writes the D5 decision log entry with rule R-RES-26, rule version equal to the parameter version, the row code and the inputs; then writes the proceeds row and calls TreatmentApi.
6. System: for a PARTIAL match, passes the shortfall to TreatmentApi, which holds it on the plan.
7. System: a payment no row matches is written UNMATCHED with a D5 entry under R-UNI-03 and appears on the exception list.
8. Credit Administration officer: reads matched and unmatched receipts on SCR-28, with the row that matched each one.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A partial payment below the partial floor | Unmatched; exception list | MSG-P8-001 | AC5 |
| X2 | A late payment one day past the window | Unmatched; exception list | MSG-P8-001 | AC4 |
| X3 | A parameter load with two rows of the same priority or a tolerance above 100 | Load refused in full | MSG-GEN-002 | AC6 |
| X4 | The decision log write fails for a match | The payment is not written; it is matched in the next run; incident | MSG-P7-003 | AC7 |
| X5 | A payment above the installment by more than the tolerance | Unmatched; exception list | MSG-P8-001 | AC8 |
| X6 | Two rows would match | The row with the lowest priority number decides | None | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Extends the matcher of RWB-E2-008 only |
| Negotiable | Every threshold is a row value; the story fixes the order and the logging |
| Valuable | Short and late installments match without a person |
| Estimable | Two new match types, a load check and the decision log write |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against a synthetic ALS load and parameter file |

## 7. Acceptance criteria

```gherkin
Feature: Payment matching rules with the data team

  Background:
    Given parameter version "PM-2026.12" is in force from 2026-12-01 with rows:
      | rule_code | priority | match_type | amount_tolerance_pct | window_days_before | window_days_after | partial_floor_pct |
      | EXACT     | 1        | EXACT      | 0                    | 10                 | 0                 |                   |
      | WINDOW    | 2        | WINDOW     | 0                    | 10                 | 3                 |                   |
      | PARTIAL   | 3        | PARTIAL    | 0                    | 10                 | 3                 | 90                |
    Given case "RC-2026-000555" has account "A-0555" and running plan "T-0701" with installment amount 12,500.00 THB and next installment date 2026-12-15

  Scenario: AC1 Exact match
    Given the ALS load for 2026-12-14 holds payment "PAY-91001" of 12,500.00 THB on the plan account "A-0555"
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91001" to "INSTALLMENT" for "T-0701" in that run
    Then the decision log entry for the match has decision code "D5", rule "R-RES-26", rule version "PM-2026.12" and row "EXACT"

  Scenario: AC2 Partial
    Given the ALS load for 2026-12-14 holds payment "PAY-91002" of 11,875.00 THB on account "A-0555", 5 percent short
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91002" to "INSTALLMENT" for "T-0701" with row "PARTIAL"
    Then the system calls treatmentApi.recordInstallmentPaid with amount 11,875.00 and shortfall 625.00
    Then plan "T-0701" shows a shortfall of 625.00 THB for due date 2026-12-15

  Scenario: AC3 Rule change
    Given parameter version "PM-2027.01" is loaded and approved with valid from 2027-01-01, changing WINDOW to 5 days after
    Given the ALS load for 2027-01-04 holds payment "PAY-91003" of 12,500.00 THB on account "A-0555" for due date 2026-12-31, 4 days late
    When JOB-07 runs on 2027-01-05
    Then the system matches "PAY-91003" to "INSTALLMENT" with row "WINDOW"
    Then the decision log entry has rule version "PM-2027.01"
    Then the match of "PAY-91001" keeps rule version "PM-2026.12"

  Scenario: AC4 Late payment inside and outside the window
    Given the ALS load for 2026-12-18 holds payment "PAY-91004" of 12,500.00 THB on account "A-0555", 3 days after due date 2026-12-15
    Given the same load holds payment "PAY-91005" of 12,500.00 THB on account "A-0666" of plan "T-0702", 4 days after its due date 2026-12-14
    When JOB-07 runs on 2026-12-19
    Then the system matches "PAY-91004" with row "WINDOW" and P3 receives PAYMENT_RECEIVED_LATE under R-RES-28
    Then the system matches "PAY-91005" to "UNMATCHED" with a decision log entry under rule "R-UNI-03"

  Scenario: AC5 Partial below the floor
    Given the ALS load for 2026-12-14 holds payment "PAY-91006" of 10,000.00 THB on account "A-0555", 80 percent of the installment
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91006" to "UNMATCHED"
    Then the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14

  Scenario: AC6 Invalid parameter load refused
    Given a parameter file for version "PM-2027.02" where rows "WINDOW" and "PARTIAL" both have priority 2 and "PARTIAL" has tolerance 120
    When it is loaded through POST /admin/reference-loads
    Then the response is status 422 with MSG-GEN-002 naming "amount_tolerance_pct", 0 and 100
    Then the system refuses the load in full and "PM-2026.12" stays in force

  Scenario: AC7 Decision log write fails
    Given the decision log store is unavailable during JOB-07 on 2026-12-15
    When "PAY-91001" is matched
    Then the system writes no proceeds row for "PAY-91001"
    Then the run summary shows MSG-P7-003 for "PAY-91001"
    Then the system raises an incident under rule R-UNI-39
    Then the next run of JOB-07 for 2026-12-14 matches "PAY-91001"

  Scenario: AC8 Overpayment beyond the tolerance
    Given the ALS load for 2026-12-14 holds payment "PAY-91007" of 13,000.00 THB on account "A-0555"
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91007" to "UNMATCHED" and appears in GET /proceeds?matched=false

  Scenario: AC9 Lowest priority number decides
    Given the ALS load for 2026-12-14 holds payment "PAY-91008" of 12,500.00 THB on account "A-0555", which both "EXACT" and "WINDOW" match
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91008" with row "EXACT"
    Then the system writes one decision log entry for "PAY-91008"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Rows are tried in priority order and the first row that matches decides | ADR-004 decision tables; hit policy first |
| BR2 | EXACT: plan account, amount within the tolerance, date inside the window before the due date | R-RES-26 |
| BR3 | WINDOW: as EXACT, with the window extended after the due date; a late match is a late payment for the plan | R-RES-28 |
| BR4 | PARTIAL: amount at or above the partial floor and below the installment; the shortfall is held on the plan | R-SET-15 pattern; REQ-CHO-009 |
| BR5 | A payment no row matches is held on the exception list | R-UNI-03; CTL-41 |
| BR6 | Each match decision is written to the decision log with the parameter version in force on the business date; earlier matches keep their version | R-UNI-38; Principle 5 |
| BR7 | A parameter load with any invalid row is refused in full | refdata.txt change process, step 3; CTL-08 |
| BR8 | A match that cannot be written to the decision log is not made | Principle 5; R-UNI-39 |

## 9. State transitions

None. This story does not change a case status. P3 changes the plan route state on the results:

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | PLAN_RUNNING (R-RES-26) |
| PLAN_CURE_PERIOD | PAYMENT_RECEIVED_LATE | payment received inside the cure period | PLAN_RUNNING (R-RES-28) |

The reference load moves from loaded to refused or in force.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, Credit Administration officer | Reads matches and the exception list (Write-off and posting CRUA); approves a parameter version as list owner |
| RW-REFADM, reference data administrator | Loads parameter versions (Reference data C) |
| RW-FINANCE, Finance and CFO delegate | Reads matches (Write-off and posting RA) |
| SY-DATALOAD, data load from COLLINS | Runs JOB-07 |
| SY-DECLOG, decision log writer | Writes the D5 entries |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent |

Separation of duty: the reference data administrator who loads a version does not approve it (roles.txt).

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-022 | account_payment | id | Read |
| DF-ACC-023 | account_payment | account_id | Read |
| DF-ACC-025 | account_payment | payment_date | Read |
| DF-ACC-026 | account_payment | payment_amount | Read |
| DF-ACC-018 | loan_account | next_installment_date | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-031 | treatment | installment_amount | Read |
| DF-TRT-033 | treatment | installment_shortfall | Write, through the treatment interface |
| DF-FIN-002 | proceeds | case_id | Write |
| DF-FIN-003 | proceeds | treatment_id | Write |
| DF-FIN-004 | proceeds | account_payment_id | Write |
| DF-FIN-006 | proceeds | amount | Write |
| DF-FIN-008 | proceeds | matched_to | Write |
| DF-REF-262 | payment_match_rule | rule_code | Write |
| DF-REF-263 | payment_match_rule | rule_version | Write |
| DF-REF-270 | payment_match_rule | priority | Write |
| DF-REF-264 | payment_match_rule | match_type | Write |
| DF-REF-265 | payment_match_rule | amount_tolerance_pct | Write |
| DF-REF-266 | payment_match_rule | window_days_before | Write |
| DF-REF-267 | payment_match_rule | window_days_after | Write |
| DF-REF-269 | payment_match_rule | partial_floor_pct | Write |
| DF-REF-271 | payment_match_rule | valid_from | Write |
| DF-REF-272 | payment_match_rule | valid_to | Write |
| DF-REF-273 | payment_match_rule | approved_by | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/reference-loads** (P4) with table "payment_match_rule"

| Item | Value |
|---|---|
| Request | multipart: file, table, validFrom |
| Response | 201 ReferenceLoad |
| Errors | 401; 403 (MSG-P4-002); 409 repeat of a load (MSG-P1-002); 422 row invalid (MSG-GEN-001, MSG-GEN-002); 503 |
| Authorization | Reference data, right C |
| Idempotency | File hash per table |

**GET /api/recovery/v1/proceeds** (P8): as in RWB-E2-008. Each Proceeds item is read with its decision log entry through GET /api/recovery/v1/decision-log on SCR-28 to show the row that matched.

**Job JOB-07 Payment matching**: as in RWB-E2-008, with the rule order of BR1 and the decision log write before each proceeds row. Idempotency key unchanged (account_payment_id). Restart: a payment whose decision log write failed has no proceeds row and is picked up by the next run.

**Published interfaces called**

```java
DecisionLogRef DecisionLogApi.write(DecisionLogRequest request) throws DecisionLogWriteException; // P7
void TreatmentApi.recordInstallmentPaid(UUID treatmentId, UUID proceedsId, LocalDate dueDate,
                                        BigDecimal amount, BigDecimal shortfall);              // P3
```

## 13. Solution plan

- Package: folder `recovery/payments/matching`, Java package `recovery.payments.matching`.

| Component | Type | Responsibility |
|---|---|---|
| PaymentMatchRuleLoadHandler | Service | ReferenceLoadHandler for table payment_match_rule with the BR7 checks |
| MatchRuleEvaluator | Rule table | Evaluates the rows of the version in force in priority order |
| ExactMatch, WindowMatch, PartialMatch | Service | One evaluator per match type |
| PaymentMatcher | Service | From RWB-E2-008; delegates to MatchRuleEvaluator and writes the decision log entry first |
| MatchDecisionWriter | Service | Builds the D5 DecisionLogRequest with rule, version, row code and inputs |

- Database: table payment_match_rule (created in RWB-E2-008) gets partial_floor_pct numeric(5,2) and a check that amount_tolerance_pct is between 0 and 100; unique (rule_version, priority). Migration `V2_027__match_rule_partial.sql`.
- Configuration and reference data: version PM-2026.12 with the three rows of the Background; window 3 days after and partial floor 90 percent are assumed values, owner Credit Administration; match types EXACT, WINDOW, PARTIAL as a new list (additions).
- Build steps:
  1. Write the migration; extend the load handler with the BR7 checks; test AC6.
  2. Build MatchRuleEvaluator and the three evaluators; unit test AC1, AC2, AC4, AC5, AC8, AC9.
  3. Build MatchDecisionWriter and put the decision log write before the proceeds write in PaymentMatcher; test AC7.
  4. Select the version in force by business date; test AC3.
  5. Pass the shortfall to TreatmentApi; test AC2 end to end with the P3 stub.
- Feature flag: `rwb.payments.matching-rules`.
- Done when: the tests in section 16 pass, and a synthetic month of 1,000 payments runs with every decision log entry naming a rule version.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-GEN-002 | A parameter value outside its range, or a duplicate priority | {field} must be between {min} and {max}. |
| MSG-GEN-001 | A required parameter value is empty | Enter {field}. |
| MSG-P1-002 | A repeated parameter load | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

## 15. Screens and states

SCR-28 Proceeds matching (states Loading; matched; unmatched) shows, for each matched receipt, the row code and rule version from its decision log entry, and for each unmatched receipt the reason. Parameter versions show on SCR-40 Reference data (states Versions; load) when it is built; until then the load result is on the reference load record.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-027-01 | AC1, BR2, BR6 | System | PAY-91001 12,500.00 |
| TC-E2-027-02 | AC2, BR4 | System | PAY-91002 11,875.00 |
| TC-E2-027-03 | AC3, BR6 | System | PM-2027.01 from 2027-01-01; PAY-91003 4 days late |
| TC-E2-027-04 | AC4, BR3, BR5 | System | PAY-91004 3 days late, PAY-91005 4 days late |
| TC-E2-027-05 | AC5, BR4, BR5 | System | PAY-91006 10,000.00 |
| TC-E2-027-06 | AC6, BR7 | System | PM-2027.02 with duplicate priority and tolerance 120 |
| TC-E2-027-07 | AC7, BR8 | System | Decision log stubbed unavailable |
| TC-E2-027-08 | AC8, BR2 | System | PAY-91007 13,000.00 |
| TC-E2-027-09 | AC9, BR1 | System | PAY-91008 matched by two rows |
| TC-E2-027-10 | Access | Access | RW-CASEOWN calls GET /proceeds; refused with MSG-P4-002 |
| TC-E2-027-11 | Principle 5 | Resilience | Decision log write forced to fail for 50 payments; no proceeds row written |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: priorities, tolerances, windows and floors are rows in payment_match_rule.
- No personal data in logs, tests or prompts. Decision log inputs hold payment code, amount, dates and row code only.
- No read of another module's tables. Payments, accounts and plans come through P1 and P3 interfaces.
- The decision log entry is written before the proceeds row; no match exists without its entry.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-RES-28, R-UNI-03, R-UNI-38, R-UNI-39 | TC-E2-027-01 to TC-E2-027-11 |

## 19. Out of scope

- Settlement payment matching and partial settlement installments (FEAT-PAY-03, Epic 4).
- Manual matching from SCR-28 (POST /proceeds/{proceedsId}/match, Epic 4).
- The reconciliation agent that works the exception list (Epic 4).
- Applying proceeds to the case balance in policy order (FEAT-PAY-10, Epic 4).
