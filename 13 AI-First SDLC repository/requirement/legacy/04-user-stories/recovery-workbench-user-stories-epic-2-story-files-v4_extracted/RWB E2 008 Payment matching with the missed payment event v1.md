<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 008 Payment matching with the missed payment event v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 008 Payment matching with the missed payment event v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-008 Payment matching with the missed payment event

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-008 |
| Epic | E2, release 31 December 2026 |
| Module | P8 Payments and posting |
| Feature | FEAT-OCC-10 Match a payment to the plan; FEAT-OCC-11 Raise the plan payment missed event; FEAT-PAY-01 Match a payment to a plan installment; FEAT-PAY-02 Hold an unmatched payment on the exception list |
| Requirement IDs | REQ-CHO-007, REQ-CHO-009 |
| BRD section | Business Requirements Epic 2, sections 3.8 and 4 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D5 |
| Priority | Must |
| Depends on | RWB-E2-004, RWB-E1-003 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **payments from the ALS load matched to the running plans each day, with a missed payment event when a due installment has not arrived**, so that **a broken plan is known the day after it breaks**.

## 2. Business rationale

Payments are matched to plans by hand today, and a missed installment is found weeks later, after the cure period has gone. This story matches each payment in the daily ALS load (INT-02) to the plan installment it pays, keeps anything unmatched on the exception list, and raises PaymentMissed the morning after a due date passes with no payment, which the restructure rules (R-RES-27) and the transfer rules act on. It serves REQ-CHO-007 and REQ-CHO-009, control CTL-41 and the FSD P8 measure "receipts matched the same day".

## 3. Preconditions

- RWB-E1-003 is done: the ALS payments load into account_payment each morning through JOB-01, with checks DQ-008 to DQ-014.
- RWB-E2-004 is done: the treatment record holds running plans with installment amount and installments paid, readable and updatable through TreatmentApi.
- The next due date of each plan account comes from loan_account.next_installment_date in the same ALS load.
- The payment matching parameters are loaded as reference data: one EXACT row, version "PM-2026.12".
- JOB-01 has passed for the business date and published LoadCompleted (EV-26).
- P3 consumes PaymentMissed and applies R-RES-27 and the transfer rules (RWB-E1-021).

## 4. Flow

1. JOB-07 Payment matching: starts when LoadCompleted arrives for the ALS source and business date, after JOB-01.
2. System: reads the payments loaded for the business date through the P1 interface.
3. System: for each payment, finds the open case of the account through the P3 interface; a payment on an account with no open case goes to the data quality exception list.
4. System: reads the running plans on the case and the parameter row in force; a payment on the plan account for the installment amount, dated inside the window before the next due date, matches that installment.
5. System: writes a proceeds row with source CUSTOMER and matched_to INSTALLMENT, calls TreatmentApi.recordInstallmentPaid, and writes ProceedsMatched to the outbox in the same transaction.
6. System: a payment that matches no plan installment is written with matched_to UNMATCHED and appears on the exception list for the reconciliation agent (R-UNI-03).
7. System: after all payments, for each running plan whose next due date plus the grace days is before the business date and that has no matched payment for that due date, writes PaymentMissed with treatment ID, due date and amount due.
8. P3: applies R-RES-27 (plan to the cure period) and the transfer rule; the case owner sees the missed payment on the treatment record the same morning.
9. System: writes the run summary (payments read, matched, unmatched, missed events) to the job monitor and runs REC-04 (payments in the ALS load against proceeds).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A payment matches no plan installment | Proceeds row UNMATCHED on the exception list | MSG-P8-001 | AC3 |
| X2 | A payment is on an account with no open case | Held on the data quality exception list; no proceeds row | None | AC4 |
| X3 | The ALS load for the business date is refused or late | JOB-07 does not run; no missed payment is raised from stale data | MSG-P1-001 | AC5 |
| X4 | JOB-07 runs twice for one business date | No second proceeds row and no second event | None | AC6 |
| X5 | A payment arrives on the last day of the window | It matches | None | AC7 |
| X6 | A payment arrives one day before the window opens | It does not match | MSG-P8-001 | AC7 |
| X7 | No parameter row is in force on the business date | JOB-07 stops before matching; nothing is written | MSG-P8-002 | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the payments load (RWB-E1-003) and the treatment record (RWB-E2-004); partial and window rules come in RWB-E2-027 |
| Negotiable | Window, grace days and amount rule are reference data |
| Valuable | A missed installment is known the morning after the due date |
| Estimable | One job, one matcher, one table, one event |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against a synthetic ALS load |

## 7. Acceptance criteria

```gherkin
Feature: Payment matching with the missed payment event

  Background:
    Given payment matching parameters "PM-2026.12" are in force with rule "EXACT": amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days
    Given case "RC-2026-000555" has account "A-0555" and running restructure plan "T-0701" with installment amount 12,500.00 THB, installments 24 and installments paid 3
    Given account "A-0555" has next installment date 2026-12-15

  Scenario: AC1 Payment matched
    Given the ALS load for business date 2026-12-14 holds payment "PAY-90001" of 12,500.00 THB on account "A-0555" dated 2026-12-14
    When JOB-07 runs on 2026-12-15
    Then a proceeds row exists for case "RC-2026-000555" with treatment "T-0701", source "CUSTOMER", amount 12,500.00 and matched to "INSTALLMENT"
    Then the system calls treatmentApi.recordInstallmentPaid for "T-0701" with due date 2026-12-15
    Then the system writes proceedsMatched to the outbox
    Then after the ALS load of 2026-12-15 the plan shows installments paid 4 and next due date 2027-01-15

  Scenario: AC2 Missed payment
    Given no payment on account "A-0555" was loaded between 2026-12-05 and 2026-12-15
    When JOB-07 runs on 2026-12-16 for business date 2026-12-15
    Then the system writes paymentMissed to the outbox with treatment "T-0701", due date 2026-12-15 and amount due 12,500.00
    Then P3 moves plan "T-0701" from "PLAN_RUNNING" to "PLAN_CURE_PERIOD" under rule R-RES-27
    Then the transfer rule records the case movement for reason "payment missed"

  Scenario: AC3 Exception
    Given the ALS load for business date 2026-12-14 holds payment "PAY-90002" of 3,000.00 THB on account "A-0555"
    When JOB-07 runs on 2026-12-15
    Then a proceeds row exists for "PAY-90002" with matched to "UNMATCHED" and no treatment
    Then GET /proceeds?matched=false returns "PAY-90002" for the Credit Administration officer
    Then the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14

  Scenario: AC4 Payment on an account with no open case
    Given the ALS load holds payment "PAY-90003" on account "A-0999" that is on no open case
    When JOB-07 runs on 2026-12-15
    Then the system writes no proceeds row for "PAY-90003"
    Then the system holds "PAY-90003" on the data quality exception list with check "References"

  Scenario: AC5 ALS load refused
    Given the ALS load for business date 2026-12-15 was refused at check "control total"
    When the scheduled time for JOB-07 on 2026-12-16 passes
    Then JOB-07 does not run for business date 2026-12-15
    Then the system writes no PaymentMissed for due date 2026-12-15
    Then the plan view shows MSG-P1-001 naming "DP01 Account and arrears" and 2026-12-14

  Scenario: AC6 Repeated run
    Given JOB-07 completed for business date 2026-12-14 with 1 matched and 1 unmatched payment
    When JOB-07 is rerun for business date 2026-12-14 from SCR-44
    Then the proceeds table still has 2 rows for business date 2026-12-14
    Then no second ProceedsMatched or PaymentMissed is written

  Scenario: AC7 Window boundary
    Given plan "T-0702" on account "A-0666" of case "RC-2026-000566" has installment amount 12,500.00 THB and next installment date 2026-12-16
    Given the ALS load for business date 2026-12-05 holds payment "PAY-90004" of 12,500.00 THB on account "A-0555" dated 2026-12-05
    Given the same load holds payment "PAY-90005" of 12,500.00 THB on account "A-0666" dated 2026-12-05
    When JOB-07 runs on 2026-12-06
    Then "PAY-90004", 10 days before its due date, is matched to "INSTALLMENT" for "T-0701"
    Then "PAY-90005", 11 days before its due date, is matched to "UNMATCHED"

  Scenario: AC8 No parameter row in force
    Given no payment matching parameter row is valid on 2026-12-15
    When JOB-07 starts for business date 2026-12-15
    Then it stops before matching with MSG-P8-002
    Then no proceeds row and no event is written
    Then the job monitor shows JOB-07 as failed with an alert to Credit Administration
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A payment on the plan account for the installment amount, dated inside the window before the next due date, matches that installment | R-RES-26; payment_match_rule row EXACT |
| BR2 | A due date that passes, plus the grace days, with no matched payment raises PaymentMissed once | R-RES-27; REQ-CHO-007 |
| BR3 | A payment that matches no plan, sale or lot is held on the exception list for the reconciliation agent | R-UNI-03; CTL-41 |
| BR4 | A payment on an account with no open case is held as a reference exception | DQ-012 |
| BR5 | Matching runs only on a load that passed its checks; no missed payment is raised from stale data | JOB-07 depends on JOB-01; CTL-02 |
| BR6 | One proceeds row per ALS payment; one PaymentMissed per plan and due date | R-UNI-40; uk_account_payment |
| BR7 | Window, tolerance and grace days are reference data with a version | Principle 1; DT02 |
| BR8 | Payments in the ALS load reconcile to proceeds by count and amount daily | REC-04 |

## 9. State transitions

None. This story does not change a case status. P3 changes the plan route state on the events this story writes:

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | PLAN_RUNNING (next due date advanced, R-RES-26) |
| PLAN_RUNNING | PAYMENT_MISSED | due_date passed and no payment matched | PLAN_CURE_PERIOD (R-RES-27) |

This story writes the proceeds match state (matched_to INSTALLMENT or UNMATCHED).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load from COLLINS | Runs JOB-07 (Write-off and posting U) |
| SY-CASEWF, case workflow module | Consumes PaymentMissed and ProceedsMatched |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent (Write-off and posting R) |
| RW-CREDITAD, Credit Administration officer | Reads matched and unmatched receipts on SCR-28 (Write-off and posting CRUA) |
| RW-CASEOWN, case owner | Reads the plan position on SCR-14 (Treatment and offer R) |
| RW-REFADM, reference data administrator | Loads the parameter rows (Reference data C) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-022 | account_payment | id | Read |
| DF-ACC-023 | account_payment | account_id | Read |
| DF-ACC-024 | account_payment | payment_code | Read |
| DF-ACC-025 | account_payment | payment_date | Read |
| DF-ACC-026 | account_payment | payment_amount | Read |
| DF-ACC-028 | account_payment | data_as_of | Read |
| DF-ACC-018 | loan_account | next_installment_date | Read |
| DF-CAS-025 | case_account | case_id | Read |
| DF-CAS-026 | case_account | account_id | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-009 | treatment | installments | Read |
| DF-TRT-031 | treatment | installment_amount | Read |
| DF-TRT-032 | treatment | installments_paid | Write, through the treatment interface |
| DF-FIN-001 to DF-FIN-009 | proceeds | all fields | Write |
| DF-REF-261 | payment_match_rule | id | Read |
| DF-REF-262 | payment_match_rule | rule_code | Read |
| DF-REF-263 | payment_match_rule | rule_version | Read |
| DF-REF-264 | payment_match_rule | match_type | Read |
| DF-REF-265 | payment_match_rule | amount_tolerance_pct | Read |
| DF-REF-266 | payment_match_rule | window_days_before | Read |
| DF-REF-267 | payment_match_rule | window_days_after | Read |
| DF-REF-268 | payment_match_rule | grace_days | Read |
| DF-REF-270 | payment_match_rule | priority | Read |
| DF-REF-271 | payment_match_rule | valid_from | Read |
| DF-REF-272 | payment_match_rule | valid_to | Read |
| DF-REF-273 | payment_match_rule | approved_by | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job JOB-07 Payment matching**

| Item | Value |
|---|---|
| Trigger | LoadCompleted (EV-26) for the ALS source with all checks passed; daily after JOB-01 |
| Input | Payments of the business date; running plans; parameter rows in force |
| Output | proceeds rows; treatment installment updates through TreatmentApi; run summary |
| Events published | ProceedsMatched (EV-25): proceedsId, caseId, amount; PaymentMissed (EV-12): treatmentId, dueDate, amountDue |
| Idempotency key | Proceeds: account_payment_id (unique). PaymentMissed: treatmentId and dueDate |
| Restart | Rerun from SCR-44 for the business date; rows already written are skipped |

**GET /api/recovery/v1/proceeds** (api.yaml, x-module P8)

| Item | Value |
|---|---|
| Request | Query: matched (true or false), from, to, page, size |
| Response | 200 ProceedsPage: items of Proceeds, page, size, total |
| Errors | 401; 403 role lacks Write-off and posting R (MSG-P4-002); 503 |
| Authorization | Write-off and posting, right R, scope applied |
| Idempotency | Not applicable |

**Published interfaces called**

```java
List<PaymentView> RecoveryDataApi.paymentsLoaded(LocalDate businessDate);              // P1
Optional<UUID> CaseWorkflowApi.openCaseForAccount(UUID accountId);                     // P3
List<RunningPlanView> TreatmentApi.runningPlans(UUID caseId);                          // P3, RWB-E2-004
void TreatmentApi.recordInstallmentPaid(UUID treatmentId, UUID proceedsId, LocalDate dueDate, BigDecimal amount); // P3
LocalDate RecoveryDataApi.nextInstallmentDate(UUID accountId);                         // P1
```

**Published interface offered**

```java
public interface PaymentsApi {
    List<ProceedsView> proceedsForCase(UUID caseId, LocalDate from, LocalDate to);
}
```

## 13. Solution plan

- Package: folder `recovery/payments/matching`, Java package `recovery.payments.matching`.

| Component | Type | Responsibility |
|---|---|---|
| ProceedsEntity | Entity | Maps table proceeds |
| ProceedsRepository | Repository | Reads and writes proceeds |
| PaymentMatchRuleEntity | Entity | Maps table payment_match_rule |
| PaymentMatchRuleRepository | Repository | Finds the rows in force on a date |
| PaymentMatchingJob | Job | JOB-07 as a Spring Batch job started on LoadCompleted |
| PaymentMatcher | Service | Applies BR1 to one payment against the running plans |
| MissedPaymentDetector | Service | Applies BR2 to running plans after matching |
| PaymentEventPublisher | Service | Writes ProceedsMatched and PaymentMissed to the outbox |
| ProceedsController | Controller | GET /proceeds |
| PaymentsApiService | Published interface | Implements PaymentsApi |

- Database: table proceeds (Recovery Workbench Physical Schema v4.sql); add unique index ux_proceeds_account_payment on (account_payment_id) where account_payment_id is not null, and index on (matched_to, received_date). New table payment_match_rule with unique (rule_code, rule_version); new table payment_missed_event_key with unique (treatment_id, due_date) for the event idempotency. Flyway migration `V2_008__payment_matching.sql`.
- Configuration and reference data: parameter row EXACT, version PM-2026.12: tolerance 0 percent, window 10 days before and 0 after, grace 0 days, assumed, owner Credit Administration as the list owner of LOV-MATCH; loaded by RW-REFADM through POST /admin/reference-loads with table "payment_match_rule"; LOV-MATCH and LOV-PROCEEDS-SRC.
- Build steps:
  1. Write the migration and the two entities; test the unique indexes.
  2. Add the payment_match_rule load handler to the P4 reference load service; test a valid and a refused file.
  3. Build PaymentMatcher for the EXACT rule; unit test AC1, AC3 and the AC7 boundaries.
  4. Build MissedPaymentDetector; unit test AC2 and the grace boundary.
  5. Build PaymentMatchingJob with the LoadCompleted trigger, the reference exception path and the run summary; test AC4, AC5, AC8.
  6. Add the idempotency keys and the restart; test AC6.
  7. Build ProceedsController for SCR-28 skeleton; test AC3 read and the access test.
- Feature flag: `rwb.payments.matching`.
- Done when: the tests in section 16 pass, and REC-04 for a synthetic month shows every ALS payment as a proceeds row or a held reference exception.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P8-002 | No parameter row in force | Payment matching for {date} did not run: no matching rule is in force. |
| MSG-P1-001 | The ALS load is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | The role lacks Write-off and posting R | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-28 Proceeds matching (skeleton in E2; states Loading; matched; unmatched) lists receipts from GET /proceeds for the Credit Administration officer, filtered by matched or unmatched. The case owner sees the plan position on SCR-14 Treatment record and the missed payment on SCR-04 Case timeline. SCR-44 shows the JOB-07 run summary.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-008-01 | AC1, BR1 | System | PAY-90001 12,500.00 on A-0555 dated 2026-12-14; T-0701 due 2026-12-15 |
| TC-E2-008-02 | AC2, BR2 | System | No payment 2026-12-05 to 2026-12-15 |
| TC-E2-008-03 | AC3, BR3 | System | PAY-90002 3,000.00 |
| TC-E2-008-04 | AC4, BR4 | System | PAY-90003 on A-0999 with no open case |
| TC-E2-008-05 | AC5, BR5 | System | ALS load of 2026-12-15 refused |
| TC-E2-008-06 | AC6, BR6 | System | JOB-07 rerun for 2026-12-14 |
| TC-E2-008-07 | AC7, BR1, BR7 | System | PAY-90004 10 days and PAY-90005 11 days before their due dates |
| TC-E2-008-08 | AC8, BR7 | System | No parameter row valid on 2026-12-15 |
| TC-E2-008-09 | Access | Access | RW-CASEOWN calls GET /proceeds; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: window, tolerance, grace days and match types are rows in payment_match_rule.
- No personal data in logs, tests or prompts. Payments are identified by payment code and account ID; account numbers are never logged.
- No read of another module's tables. account_payment, loan_account, case_account and treatment are read through P1 and P3 interfaces; the treatment is updated only through TreatmentApi.
- Amounts use BigDecimal with scale 2 and are compared exactly.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-E2-008-02, TC-E2-008-05, TC-E2-008-06 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03, R-UNI-40 | TC-E2-008-01, TC-E2-008-03, TC-E2-008-04, TC-E2-008-07, TC-E2-008-08, TC-E2-008-09 |

## 19. Out of scope

- Partial payments, late payments inside a window after the due date and rule versions in the decision log (RWB-E2-027).
- Settlement, auction and enforcement proceeds (FEAT-PAY-03, FEAT-PAY-04, Epic 4).
- Manual matching of an unmatched receipt (POST /proceeds/{proceedsId}/match, Epic 4).
- The cure period and the broken plan rule (R-RES-28 to R-RES-31, FEAT-TRT-11, Epic 3).
