# RWB-E2-008 Payment matching with the missed payment event

SCB Collections and Recovery. Henka Group, 16 November 2026.

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
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E2-004, RWB-E1-069, RWB-E1-072, RWB-E2-042 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **payments posted in ALS and read from v_ace_payment matched to the running plans each day, with a missed payment event when a due installment has not arrived by the time the ACE batch completes**, so that **a broken plan is known the day after it breaks**.

## 2. Business rationale

Payments are matched to plans by hand today, and a missed installment is found weeks later, after the cure period has gone. ACE ingests the ALS payments and the Workbench reads them through v_ace_payment, keyed by payment_code and account_key. This story matches each payment to the plan installment it pays, keeps anything unmatched on the exception list, and raises PaymentMissed the morning after a due date passes with no payment in a completed ACE batch, which the restructure rules (R-RES-27) and the transfer rules act on. It serves REQ-CHO-007 and REQ-CHO-009, control CTL-41 and the FSD P8 measure "receipts matched the same day".

Payment matching is package PAYMENT_MATCH under ADR-012, fixed by D-RCV-36 T10 on 16 November 2026. The EXACT, PARTIAL and WINDOW rows carry match type, amount tolerance, window, grace and partial floor as decision-table columns, SY-RULES evaluates them through RuleEvaluator, and the decision log names rule R-RES-26 with the package version.

## 3. Preconditions

- RWB-E1-069 is done: v_ace_payment is granted SELECT to the recovery service identity and holds payment_code, account_key, payment_date, payment_amount and data_as_of (V0002).
- v_ace_batch_status (V0003, RWB-ACE-001, DL43) carries the ALS business date and completion; the flag `rwb.payments.matching` stays off in an environment without V0003.
- RWB-E2-004 is done: the treatment record holds running plans with installment amount and installments paid, readable and updatable through TreatmentApi.
- RWB-E1-072 is done: RuleEvaluator, RuleCatalog and the rule package store exist.
- RWB-E2-042 is done: package PAYMENT_MATCH is in force with version "PM-2026.12" and one EXACT row: amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days (assumed).
- The next due date of each plan account is read from v_ace_account.next_installment_date at the same business date.
- P1 has stamped DP01 for the business date and published AceDataReady (EV-26).
- P3 consumes PaymentMissed and applies R-RES-27 and the transfer rules (RWB-E1-021).

## 4. Flow

1. JOB-07 Payment matching: starts when AceDataReady (EV-26) arrives for the ALS source with business date D, and the ACE batch status for ALS is COMPLETE.
2. System: reads the payments posted for business date D from v_ace_payment through the P1 interface: payment_code, account_key, payment_date, payment_amount.
3. System: for each payment, finds the open case of the account_key through the P3 interface; a payment on an account with no open case is listed on the REC-05 business-key break and gets no proceeds row.
4. System: reads the running plans on the case, builds PaymentMatchFacts (installment amount, next due date, payment date, payment amount, treatment type) and calls RuleEvaluator.evaluate("PAYMENT_MATCH", facts, D); a payment on the plan account for the installment amount, dated inside the window before the next due date, matches that installment through the EXACT row.
5. System: writes the decision log entry with rule R-RES-26 and the package version returned in the result; only after that succeeds writes a proceeds row with source CUSTOMER, payment_code and matched_to INSTALLMENT, calls TreatmentApi.recordInstallmentPaid, and writes ProceedsMatched to the outbox in the same transaction.
6. System: a payment that matches no plan installment is written with matched_to UNMATCHED and appears on the exception list for the reconciliation agent (R-UNI-03).
7. System: after all payments, for each running plan whose next due date plus the grace days is before the business date of the completed ACE batch and that has no matched payment for that due date, writes PaymentMissed with treatment ID, due date and amount due.
8. P3: applies R-RES-27 (plan to the cure period) and the transfer rule; the case owner sees the missed payment on the treatment record the same morning.
9. System: writes the run summary (payments read, matched, unmatched, missed events) and the REC-04 result to reconciliation_result.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A payment matches no plan installment | Proceeds row UNMATCHED on the exception list | MSG-P8-001 | AC3 |
| X2 | A payment is on an account with no open case | Listed on the REC-05 business-key break; no proceeds row | None | AC4 |
| X3 | The ACE batch for ALS is not COMPLETE for the business date | JOB-07 does not run; no missed payment is raised from stale data | MSG-P1-001 | AC5 |
| X4 | JOB-07 runs twice for one business date | No second proceeds row and no second event | None | AC6 |
| X5 | A payment arrives on the last day of the window or one day before it opens | The first matches the installment; the second does not match and is held | MSG-P8-001 | AC7 |
| X6 | No PAYMENT_MATCH version is IN_FORCE on the business date | NoPackageInForce; JOB-07 stops before matching and writes no proceeds row and no event | MSG-P3-027, MSG-P8-002 | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the ACE payment view (RWB-E1-069), the treatment record (RWB-E2-004), the evaluator of RWB-E1-072 and the PAYMENT_MATCH package of RWB-E2-042 |
| Negotiable | Window, grace days, tolerance and the amount rule are package rows with a version |
| Valuable | A missed installment is known the morning after the due date |
| Estimable | One job, one matcher, one table, one event, one rule package |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against synthetic rows in v_ace_payment |

## 7. Acceptance criteria

```gherkin
Feature: Payment matching with the missed payment event

  Background:
    Given package "PAYMENT_MATCH" version "PM-2026.12" is in force with row "EXACT": amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days
    Given case "RC-2026-000555" has account "A-0555" and running restructure plan "T-0701" with installment amount 12,500.00 THB, installments 24 and installments paid 3
    Given account "A-0555" has next installment date 2026-12-15

  Scenario: AC1 Payment matched
    Given the ACE batch for ALS with business date 2026-12-14 is COMPLETED
    Given v_ace_payment holds payment "PAY-90001" of 12,500.00 THB on account "A-0555" dated 2026-12-14
    When JOB-07 runs on 2026-12-15
    Then the EXACT row of package "PAYMENT_MATCH" version "PM-2026.12" matches "PAY-90001" to the installment
    Then the decision log entry names rule "R-RES-26" and rule version "PM-2026.12"
    Then a proceeds row exists for case "RC-2026-000555" with treatment "T-0701", payment code "PAY-90001", source "CUSTOMER", amount 12,500.00 and matched to "INSTALLMENT"
    Then the system calls treatmentApi.recordInstallmentPaid for "T-0701" with due date 2026-12-15
    Then the system writes proceedsMatched to the outbox
    Then after the ALS batch of 2026-12-15 the plan shows installments paid 4 and next due date 2027-01-15

  Scenario: AC2 Missed payment
    Given no payment on account "A-0555" appears in v_ace_payment between 2026-12-05 and 2026-12-15
    When JOB-07 runs on 2026-12-16 for business date 2026-12-15
    Then the system writes paymentMissed to the outbox with treatment "T-0701", due date 2026-12-15 and amount due 12,500.00
    Then P3 moves plan "T-0701" from "PLAN_RUNNING" to "PLAN_CURE_PERIOD" under rule R-RES-27
    Then the transfer rule records the case movement for reason "payment missed"

  Scenario: AC3 Exception
    Given the ACE batch for ALS with business date 2026-12-14 is COMPLETED
    Given v_ace_payment holds payment "PAY-90002" of 3,000.00 THB on account "A-0555"
    When JOB-07 runs on 2026-12-15
    Then a proceeds row exists for "PAY-90002" with matched to "UNMATCHED" and no treatment
    Then GET /proceeds?matched=false returns "PAY-90002" for the Credit Administration officer
    Then the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14

  Scenario: AC4 Payment on an account with no open case
    Given v_ace_payment holds payment "PAY-90003" on account "A-0999" that is on no open case
    When JOB-07 runs on 2026-12-15
    Then the system writes no proceeds row for "PAY-90003"
    Then the REC-05 business-key break lists "PAY-90003" for the data steward

  Scenario: AC5 ACE batch not complete
    Given the ACE batch for ALS with business date 2026-12-15 ended "FAILED"
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
    Given v_ace_payment holds payment "PAY-90004" of 12,500.00 THB on account "A-0555" dated 2026-12-05
    Given v_ace_payment holds payment "PAY-90005" of 12,500.00 THB on account "A-0666" dated 2026-12-05
    When JOB-07 runs on 2026-12-06
    Then "PAY-90004", 10 days before its due date, is matched to "INSTALLMENT" for "T-0701" by the EXACT row
    Then "PAY-90005", 11 days before its due date, is matched to "UNMATCHED"

  Scenario: AC8 No PAYMENT_MATCH version in force
    Given no PAYMENT_MATCH version is IN_FORCE on 2026-12-15
    When JOB-07 starts for business date 2026-12-15
    Then the evaluation refuses with NoPackageInForce and MSG-P3-027 for package "PAYMENT_MATCH"
    Then it stops before matching with MSG-P8-002
    Then no proceeds row and no event is written
    Then the job monitor shows JOB-07 as failed with an alert to Credit Administration

  Scenario: AC9 Decision log names the rule and the package version
    Given payment "PAY-90001" matches the installment of "T-0701" on 2026-12-15
    When JOB-07 writes the match
    Then the decision log entry holds decision code "D5", rule "R-RES-26" and rule version "PM-2026.12"
    Then the proceeds row is written only after the decision log entry succeeds
    Then the run summary counts the match under version "PM-2026.12"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A payment on the plan account for the installment amount, dated inside the window before the next due date, matches that installment | R-RES-26; row EXACT of package PAYMENT_MATCH |
| BR2 | A due date that passes, plus the grace days, with no matched payment raises PaymentMissed once | R-RES-27; REQ-CHO-007 |
| BR3 | A payment that matches no plan, sale or lot is held on the exception list for the reconciliation agent | R-UNI-03; CTL-41 |
| BR4 | A payment on an account with no open case is listed on the REC-05 business-key break and gets no proceeds row | REC-05; DQ-012 |
| BR5 | Matching runs only on a COMPLETE ACE batch; no missed payment is raised from stale data | JOB-07; CTL-02 |
| BR6 | One proceeds row per payment_code; one PaymentMissed per plan and due date | R-UNI-40; ux_proceeds_payment_code |
| BR7 | Window, tolerance, grace days, partial floor and match types are columns of the package rows with a version | Principle 1; D-RCV-36 T10 |
| BR8 | Payments in v_ace_payment reconcile to proceeds by count and amount daily | REC-04 |
| BR9 | The match is decided by package PAYMENT_MATCH through RuleEvaluator; the result names rule R-RES-26 and the package version, and the decision log records both | D-RCV-36 T5, T7; ADR-012 |
| BR10 | No PAYMENT_MATCH version in force is a refusal (NoPackageInForce), never a default match | R-UNI-41; D-RCV-36 T7 |

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
| The recovery service identity, JOB-07 | Runs JOB-07, calls the rule evaluator and reads the ACE views (Write-off and posting U) |
| SY-RULES, Drools evaluator | Evaluates package PAYMENT_MATCH for each payment and returns the row, the outputs and the package version |
| SY-CASEWF, case workflow module | Consumes PaymentMissed and ProceedsMatched |
| SY-DECLOG, decision log writer | Writes the match entry (Decision log C) |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent (Write-off and posting R) |
| RW-CREDITAD, Credit Administration officer | Reads matched and unmatched receipts on SCR-28 (Write-off and posting CRUA) |
| RW-CASEOWN, case owner | Reads the plan position on SCR-14 (Treatment and offer R) |
| RW-COE, center of excellence analyst | Owns package PAYMENT_MATCH and loads a new version through RWB-E1-073 (Rules and parameters CRUD) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-043 | v_ace_payment | payment_code | Read |
| DF-ACE-044 | v_ace_payment | account_key | Read |
| DF-ACE-045 | v_ace_payment | payment_date | Read |
| DF-ACE-046 | v_ace_payment | payment_amount | Read |
| DF-ACE-054 | v_ace_payment | data_as_of | Read |
| DF-ACE-028 | v_ace_account | next_installment_date | Read |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-CAS-025 | case_account | case_id | Read |
| DF-CAS-026 | case_account | account_key | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-009 | treatment | installments | Read |
| DF-TRT-031 | treatment | installment_amount | Read |
| DF-TRT-032 | treatment | installments_paid | Write, through the treatment interface |
| DF-FIN-001 to DF-FIN-009 | proceeds | all fields | Write |
| DF-FIN-004 | proceeds | payment_code | Write |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-296 | rule_row | package_version_id | Read |
| DF-REF-297 | rule_row | drools_rule_name | Read |
| DF-REF-298 | rule_row | outputs | Read |
| DF-REF-297 | rule_row | drools_rule_name | Read |
| DF-REF-298 | rule_row | outputs | Read |
| DF-DEC-004 | decision_log_entry | rule_id | Write |
| DF-DEC-005 | decision_log_entry | rule_version | Write |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | all fields | Write (REC-04) |

Field IDs are those in the Logical Data Model and Data Dictionary. The payment rows are read through the P1 interface over v_ace_payment. The rule_row fields are read by rule ID and package version through the evaluation result; this story reads no drl_source and no workbook.

DF-REF-261 to DF-REF-273 were the payment_match_rule fields (id, rule_code, rule_version, match_type, amount_tolerance_pct, window_days_before, window_days_after, grace_days, partial_floor_pct, priority, valid_from, valid_to, approved_by). They are retired by D-RCV-36 (T10) and are not in Physical Schema v6; no story reads or writes them.

## 12. Contract

**Job JOB-07 Payment matching**

| Item | Value |
|---|---|
| Trigger | AceDataReady (EV-26) for the ALS source with the batch COMPLETE; daily |
| Input | Payments of the business date from v_ace_payment; running plans; the PAYMENT_MATCH version in force |
| Rule evaluation | RuleEvaluator.evaluate("PAYMENT_MATCH", facts, businessDate); rule R-RES-26; the package version is chosen at evaluation time and written to the decision log |
| Output | proceeds rows; treatment installment updates through TreatmentApi; the REC-04 result |
| Events published | ProceedsMatched (EV-25): proceedsId, caseId, amount; PaymentMissed (EV-12): treatmentId, dueDate, amountDue |
| Idempotency key | Proceeds: payment_code (unique). PaymentMissed: treatmentId and dueDate |
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
// P3 recovery.casewf.rules (published, RWB-E1-072)
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
List<PaymentView> RecoveryDataApi.paymentsLoaded(LocalDate businessDate);              // P1, over v_ace_payment
Optional<UUID> CaseWorkflowApi.openCaseForAccount(String accountKey);                  // P3
List<RunningPlanView> TreatmentApi.runningPlans(UUID caseId);                          // P3, RWB-E2-004
void TreatmentApi.recordInstallmentPaid(UUID treatmentId, UUID proceedsId, LocalDate dueDate, BigDecimal amount); // P3
LocalDate RecoveryDataApi.nextInstallmentDate(String accountKey);                      // P1, over v_ace_account
BatchStatus BatchStatusQuery.forSource(String sourceSystem, LocalDate businessDate);   // P1, over v_ace_batch_status
```

The package is loaded, approved and rolled back through RWB-E1-073 and RWB-E2-042; this story only evaluates it.

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
| PaymentMatchFacts | Fact builder | Builds the facts for one payment and one running plan: installment amount, due date, payment date, payment amount and treatment type |
| PaymentMatchingJob | Job | JOB-07 as a Spring Batch job started on AceDataReady |
| PaymentMatcher | Service | Builds PaymentMatchFacts and calls RuleEvaluator("PAYMENT_MATCH"); applies BR1 to one payment against the running plans |
| MissedPaymentDetector | Service | Applies BR2 to running plans after matching |
| PaymentEventPublisher | Service | Writes ProceedsMatched and PaymentMissed to the outbox |
| ProceedsController | Controller | GET /proceeds |
| PaymentsApiService | Published interface | Implements PaymentsApi |

- Database: table proceeds (Physical Schema v6); add unique index ux_proceeds_payment_code on (payment_code) where payment_code is not null, and index on (matched_to, received_date). New table payment_missed_event_key with unique (treatment_id, due_date) for the event idempotency. Flyway migration `V2_008__payment_matching.sql`. The migration does not create payment_match_rule: that table is retired by D-RCV-36 (T10), and Physical Schema v6 counts 93 tables with rule_package and rule_package_version in its place.
- Configuration and reference data: package PAYMENT_MATCH version PM-2026.12, row EXACT with tolerance 0 percent, window 10 days before and 0 after and grace 0 days (assumed; DL25), owned by RW-COE; loaded and approved through POST /api/recovery/v1/admin/rule-packages/PAYMENT_MATCH/versions (RWB-E1-073) by RWB-E2-042, not through a reference load; LOV-MATCH and LOV-PROCEEDS-SRC. The package version in force per environment is recorded in `config/rule-packages.lock`; the values in this story are as at 16 November 2026.
- Build steps:
  1. Write the migration and the proceeds entity; test the unique indexes.
  2. Check the PAYMENT_MATCH version PM-2026.12 and its EXACT row in SIT; the version is loaded and approved through RWB-E1-073 by RWB-E2-042, and this story builds no load handler.
  3. Build PaymentMatcher with PaymentMatchFacts and the RuleEvaluator call for the EXACT row; unit test AC1, AC3, AC9 and the AC7 boundaries.
  4. Build MissedPaymentDetector; unit test AC2 and the grace boundary.
  5. Build PaymentMatchingJob with the AceDataReady trigger, the REC-05 break path, the no-package path and the run summary; test AC4, AC5, AC8.
  6. Add the idempotency keys and the restart; test AC6.
  7. Build ProceedsController for the SCR-28 skeleton; test AC3 read and the access test.
- Feature flag: `rwb.payments.matching`.
- Done when: the tests in section 16 pass, and REC-04 for a synthetic month shows every payment in v_ace_payment as a proceeds row or a held exception, with R-RES-26 and the package version on every match decision log entry.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P8-002 | No PAYMENT_MATCH version in force | Payment matching for {date} did not run: no matching rule is in force. |
| MSG-P3-027 | No PAYMENT_MATCH version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P1-001 | The ACE batch is late or not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | The role lacks Write-off and posting R | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "PAYMENT_MATCH" and the business date only, never a payment or account fact.

## 15. Screens and states

SCR-28 Proceeds matching (skeleton in E2; states Loading; matched; unmatched) lists receipts from GET /proceeds for the Credit Administration officer, filtered by matched or unmatched. The case owner sees the plan position on SCR-14 Treatment record and the missed payment on SCR-04 Case timeline. SCR-44 shows the JOB-07 run summary.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-008-01 | AC1, BR1, BR9 | System | PAY-90001 12,500.00 on A-0555 dated 2026-12-14 in v_ace_payment; T-0701 due 2026-12-15 |
| TC-E2-008-02 | AC2, BR2 | System | No payment 2026-12-05 to 2026-12-15 |
| TC-E2-008-03 | AC3, BR3 | System | PAY-90002 3,000.00 |
| TC-E2-008-04 | AC4, BR4 | System | PAY-90003 on A-0999 with no open case |
| TC-E2-008-05 | AC5, BR5 | System | ACE batch for ALS of 2026-12-15 failed |
| TC-E2-008-06 | AC6, BR6 | System | JOB-07 rerun for 2026-12-14 |
| TC-E2-008-07 | AC7, BR1, BR7 | System | PAY-90004 10 days and PAY-90005 11 days before their due dates |
| TC-E2-008-08 | AC8, BR10 | System | No PAYMENT_MATCH version in force on 2026-12-15 |
| TC-E2-008-09 | AC9, BR9 | System | PAY-90001 matched under version PM-2026.12 |
| TC-E2-008-10 | Access | Access | RW-CASEOWN calls GET /proceeds; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: window, tolerance, grace days, partial floor and match types are columns of the rows of package PAYMENT_MATCH.
- No personal data in logs, tests, workflow history or prompts. Payments are identified by payment_code and account_key; account numbers are never logged.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the payments, the next installment date and the batch status come through the P1 interfaces over the views; case and treatment facts through P3.
- Amounts use BigDecimal with scale 2 and are compared exactly.
- The rule package is loaded and approved through RWB-E1-073; this story evaluates it and never reads drl_source or the workbook.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-E2-008-02, TC-E2-008-05, TC-E2-008-06 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03, R-UNI-40 | TC-E2-008-01, TC-E2-008-03, TC-E2-008-04, TC-E2-008-07, TC-E2-008-08, TC-E2-008-09, TC-E2-008-10 |

## 19. Out of scope

- Partial payments and late payments inside a window after the due date (RWB-E2-027).
- Settlement, auction and enforcement proceeds (FEAT-PAY-03, FEAT-PAY-04, Epic 4).
- Manual matching of an unmatched receipt (POST /proceeds/{proceedsId}/match, Epic 4).
- The cure period and the broken plan rule (R-RES-28 to R-RES-31, FEAT-TRT-11, Epic 3).
- Authoring, approval and rollback of package PAYMENT_MATCH (RWB-E2-042 and RWB-E1-073).
