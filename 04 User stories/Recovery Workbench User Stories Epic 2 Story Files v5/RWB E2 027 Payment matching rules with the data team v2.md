# RWB-E2-027 Payment matching rules with the data team

SCB Collections and Recovery. Henka Group, 16 November 2026.

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
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E2-008, RWB-E2-042 |
| Status | Ready for build |

## 1. Story

As a **Credit Administration officer (RW-CREDITAD)**, I want **the matching rules for amount, date window and partial payments held as versioned rows of the PAYMENT_MATCH rule package and run by the matching engine, with the exception list for what does not match**, so that **most payments match without a person and the rest are listed**.

## 2. Business rationale

The exact rule of RWB-E2-008 leaves short and late installments on the exception list, and a person matches them by hand each morning. This story adds the PARTIAL and WINDOW rules as rows of the PAYMENT_MATCH rule package, applies them in row order, records each match in the decision log with the rule ID and the package version, and lets Credit Administration change a window or tolerance through a new approved package version with no code release.

The match type, the amount tolerance, the window, the grace and the partial floor are columns of the decision table, not code and not a reference table (D-RCV-36 T10). RWB-E2-042 authors the rows; RWB-E1-073 loads, checks, approves and rolls them back; this story runs them through RuleEvaluator and reports the exception list. It serves REQ-CHO-009, control CTL-41 and the FSD P8 measure "receipts matched the same day". The measure is that every match names its rule and package version, and unmatched receipts carry a reason.

## 3. Preconditions

- RWB-E2-008 is done: JOB-07, the proceeds table and the exception list are live, and a PAYMENT_MATCH version with the EXACT row in force decides the exact matches.
- RWB-E2-042 is done: the PAYMENT_MATCH package holds the EXACT, WINDOW and PARTIAL rows in the Drools template with at least 50 scenarios.
- RWB-E1-027 is done: the decision log writer accepts D5 entries with a rule ID and a rule version.
- TreatmentApi records an installment shortfall (RWB-E2-004).
- PAYMENT_MATCH version "PM-2026.12" is in force from 2026-12-01 with the EXACT, WINDOW and PARTIAL rows. It was loaded through POST /admin/rule-packages/PAYMENT_MATCH/versions by RW-COE and approved by RW-RISK (RWB-E1-073).
- The reader holds RW-CREDITAD or another role with Write-off and posting R.

## 4. Flow

1. RW-COE: authors the PARTIAL and WINDOW rows in the PAYMENT_MATCH workbook and loads a new version through POST /admin/rule-packages/PAYMENT_MATCH/versions with the valid from date.
2. System: RulePackageVersionService runs the Drools compile check, the schema check on the condition columns, the overlap and unreachable row checks, the scenario check and the dry run; any failure refuses the whole load (RWB-E1-073).
3. RW-RISK: approves the version; the author cannot approve it.
4. JOB-07: for the business date, calls `RuleEvaluator.evaluate("PAYMENT_MATCH", facts, businessDate)`, which picks the version in force on that date.
5. System: the package fires one row, the first match in row order (EXACT, then WINDOW, then PARTIAL), against each running plan on the case; the RuleResult names the rule ID of the row and the package version that decided.
6. System: writes the D5 decision log entry with the rule ID, the package version and the inputs; then writes the proceeds row and calls TreatmentApi.
7. System: for a PARTIAL match, passes the shortfall to TreatmentApi, which holds it on the plan.
8. System: a payment no row matches is written UNMATCHED with a D5 entry under R-UNI-03 and appears on the exception list.
9. Credit Administration officer: reads matched and unmatched receipts on SCR-28, with the rule and the package version that matched each one.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A partial payment below the partial floor | Unmatched; exception list | MSG-P8-001 | AC5 |
| X2 | A late payment one day past the window | Unmatched; exception list | MSG-P8-001 | AC4 |
| X3 | A package version load with two rows of the same row order or a tolerance above 100 | Load refused in full | MSG-P3-027 | AC6 |
| X4 | The decision log write fails for a match | The payment is not written; it is matched in the next run; incident | MSG-P7-003 | AC7 |
| X5 | A payment above the installment by more than the tolerance | Unmatched; exception list | MSG-P8-001 | AC8 |
| X6 | Two rows would match | The row with the lower row order decides | None | AC9 |
| X7 | No PAYMENT_MATCH version is in force on the business date | The run stops; no payment is matched and no proceeds row is written | MSG-P3-027 | AC10 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the PAYMENT_MATCH package and the matcher of RWB-E2-008 only |
| Negotiable | Every threshold is a rule row column; the story fixes the row order and the logging |
| Valuable | Short and late installments match without a person |
| Estimable | Two new match rows, one evaluator call and the decision log write |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against a synthetic ALS load and a loaded package version |

## 7. Acceptance criteria

```gherkin
Feature: Payment matching rules with the data team

  Background:
    Given PAYMENT_MATCH package version "PM-2026.12" is in force from 2026-12-01 with rows:
      | rule_id | row_order | match_type | amount_tolerance_pct | window_days_before | window_days_after | partial_floor_pct |
      | EXACT   | 1         | EXACT      | 0                    | 10                 | 0                 |                   |
      | WINDOW  | 2         | WINDOW     | 0                    | 10                 | 3                 |                   |
      | PARTIAL | 3         | PARTIAL    | 0                    | 10                 | 3                 | 90                |
    Given case "RC-2026-000555" has account "A-0555" and running plan "T-0701" with installment amount 12,500.00 THB and next installment date 2026-12-15

  Scenario: AC1 Exact match
    Given the ALS load for 2026-12-14 holds payment "PAY-91001" of 12,500.00 THB on the plan account "A-0555"
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91001" to "INSTALLMENT" for "T-0701" in that run
    Then the decision log entry for the match has decision code "D5", rule "EXACT" and rule version "PM-2026.12"

  Scenario: AC2 Partial
    Given the ALS load for 2026-12-14 holds payment "PAY-91002" of 11,875.00 THB on account "A-0555", 5 percent short
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91002" to "INSTALLMENT" for "T-0701" with rule "PARTIAL"
    Then the system calls treatmentApi.recordInstallmentPaid with amount 11,875.00 and shortfall 625.00
    Then plan "T-0701" shows a shortfall of 625.00 THB for due date 2026-12-15

  Scenario: AC3 Rule change
    Given PAYMENT_MATCH version "PM-2027.01" is loaded and approved with valid from 2027-01-01, changing WINDOW to 5 days after
    Given the ALS load for 2027-01-04 holds payment "PAY-91003" of 12,500.00 THB on account "A-0555" for due date 2026-12-31, 4 days late
    When JOB-07 runs on 2027-01-05
    Then the system matches "PAY-91003" to "INSTALLMENT" with rule "WINDOW"
    Then the decision log entry has rule version "PM-2027.01"
    Then the match of "PAY-91001" keeps rule version "PM-2026.12"

  Scenario: AC4 Late payment inside and outside the window
    Given the ALS load for 2026-12-18 holds payment "PAY-91004" of 12,500.00 THB on account "A-0555", 3 days after due date 2026-12-15
    Given the same load holds payment "PAY-91005" of 12,500.00 THB on account "A-0666" of plan "T-0702", 4 days after its due date 2026-12-14
    When JOB-07 runs on 2026-12-19
    Then the system matches "PAY-91004" with rule "WINDOW" and P3 receives PAYMENT_RECEIVED_LATE under R-RES-28
    Then the system matches "PAY-91005" to "UNMATCHED" with a decision log entry under rule "R-UNI-03"

  Scenario: AC5 Partial below the floor
    Given the ALS load for 2026-12-14 holds payment "PAY-91006" of 10,000.00 THB on account "A-0555", 80 percent of the installment
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91006" to "UNMATCHED"
    Then the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14

  Scenario: AC6 Invalid package version refused
    Given a PAYMENT_MATCH workbook for version "PM-2027.02" where rows "WINDOW" and "PARTIAL" both have row order 2 and "PARTIAL" has tolerance 120
    When it is loaded through POST /api/recovery/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then the response is status 422 with MSG-P3-027 for the schema check naming "PARTIAL" and the tolerance column
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

  Scenario: AC9 Lowest row order decides
    Given the ALS load for 2026-12-14 holds payment "PAY-91008" of 12,500.00 THB on account "A-0555", which both "EXACT" and "WINDOW" match
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91008" with rule "EXACT"
    Then the system writes one decision log entry for "PAY-91008"

  Scenario: AC10 No PAYMENT_MATCH version in force
    Given no PAYMENT_MATCH package version is in force on 2027-02-01
    When JOB-07 runs for business date 2027-02-01
    Then RuleEvaluator.evaluate("PAYMENT_MATCH", facts, 2027-02-01) throws NoPackageInForce
    Then the run stops with MSG-P3-027 for the package in force check
    Then no payment is matched and no proceeds row is written for 2027-02-01
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Rows are tried in row order and the first row that matches decides (first match) | D-RCV-36 T5; ADR-012 |
| BR2 | EXACT: plan account, amount within the tolerance, date inside the window before the due date | R-RES-26 |
| BR3 | WINDOW: as EXACT, with the window extended after the due date; a late match is a late payment for the plan | R-RES-28 |
| BR4 | PARTIAL: amount at or above the partial floor and below the installment; the shortfall is held on the plan | R-SET-15 pattern; REQ-CHO-009 |
| BR5 | A payment no row matches is held on the exception list | R-UNI-03; CTL-41 |
| BR6 | Each match decision is written to the decision log with the rule ID (EXACT, WINDOW or PARTIAL) and the package version in force on the business date; earlier matches keep their version | R-UNI-38; Principle 5; D-RCV-36 T5, T7 |
| BR7 | A package version with any invalid row is refused in full by RWB-E1-073 | Reference data change process, step 3; CTL-08 |
| BR8 | A match that cannot be written to the decision log is not made | Principle 5; R-UNI-39 |
| BR9 | No PAYMENT_MATCH version in force is a refusal (NoPackageInForce), never a default match | D-RCV-36 T3; R-UNI-41 |
| BR10 | The tolerance, window, grace and partial floor are condition and output columns of the PAYMENT_MATCH rows, not code and not a reference table | D-RCV-36 T10; REQ-CHO-009 |

## 9. State transitions

None. This story does not change a case status. P3 changes the plan route state on the results:

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | PLAN_RUNNING (R-RES-26) |
| PLAN_CURE_PERIOD | PAYMENT_RECEIVED_LATE | payment received inside the cure period | PLAN_RUNNING (R-RES-28) |

The package version moves LOADED to APPROVED to IN_FORCE, or to REFUSED, through RWB-E1-073.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, Credit Administration officer | Reads matches and the exception list (Write-off and posting CRUA); owns the matching values |
| RW-COE, center of excellence analyst | Authors the PARTIAL and WINDOW rows and loads the package version (Rules and parameters C) |
| RW-RISK | Approves the package version (Rules and parameters A) |
| RW-FINANCE, Finance and CFO delegate | Reads matches (Write-off and posting RA) |
| The recovery service identity | Runs JOB-07 |
| SY-RULES, Drools evaluator | Evaluates the PAYMENT_MATCH package and names the rule and the package version |
| SY-DECLOG, decision log writer | Writes the D5 entries |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent |

Separation of duty: the analyst who loads a version does not approve it; RW-RISK approves and the author cannot (RWB-E1-073).

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-043 | v_ace_payment | payment_code | Read |
| DF-ACE-044 | v_ace_payment | account_key | Read |
| DF-ACE-045 | v_ace_payment | payment_date | Read |
| DF-ACE-046 | v_ace_payment | payment_amount | Read |
| DF-ACE-028 | v_ace_account | next_installment_date | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-031 | treatment | installment_amount | Read |
| DF-TRT-033 | treatment | installment_shortfall | Write, through the treatment interface |
| DF-FIN-002 | proceeds | case_id | Write |
| DF-FIN-003 | proceeds | treatment_id | Write |
| DF-FIN-004 | proceeds | payment_code | Write |
| DF-FIN-006 | proceeds | amount | Write |
| DF-FIN-008 | proceeds | matched_to | Write |
| DF-REF-275 | rule_package | package_code | Read |
| DF-REF-281 | rule_package_version | version_label | Read |
| DF-REF-282 | rule_package_version | status | Read |
| DF-REF-286, DF-REF-287 | rule_package_version | valid_from, valid_to | Read |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-296 | rule_row | package_version_id | Read |
| DF-REF-297 | rule_row | drools_rule_name | Read |
| DF-REF-298 | rule_row | outputs | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

The tolerance, window, grace and partial floor are row columns of the PAYMENT_MATCH package and are read through RuleEvaluator and RuleCatalog; this story reads no payment_match_rule row. DF-REF-261 to DF-REF-273 are retired with payment_match_rule (D-RCV-36 T10). Field IDs are those in the Logical Data Model, Data Dictionary and Physical Schema v6.

## 12. Contract

**POST /api/recovery/v1/admin/rule-packages/PAYMENT_MATCH/versions** (P4)

| Item | Value |
|---|---|
| Request | multipart/form-data: file (xlsx workbook with the Rows and Tests tabs), validFrom (date). The version label is a cell in the workbook |
| Response | 201 RulePackageVersion: versionId, packageCode PAYMENT_MATCH, versionLabel, status LOADED, validFrom, author, checksum, testResult {total, passed, failed, failedScenarioIds}, dryRunCounts |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters C (MSG-P4-002); 404 unknown package code; 409 version label exists (MSG-GEN-004); 422 a check failed (MSG-P3-027 with the check, row and column in Problem.detail), empty file (MSG-GEN-001); 503 |
| Authorization | Rules and parameters, right C |
| Idempotency | Package code and version label; a repeat is refused with 409 |

**GET /api/recovery/v1/admin/rule-packages/PAYMENT_MATCH/versions** (P4)

| Item | Value |
|---|---|
| Request | Query: status (optional) |
| Response | 200 RulePackageVersion[]: versionId, versionLabel, status, validFrom, validTo, author, approver, checksum, testResult, dryRunCounts |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 404 unknown package code; 503 |
| Authorization | Rules and parameters, right R |
| Idempotency | Read only |

**GET /api/recovery/v1/proceeds** (P8): as in RWB-E2-008. Each Proceeds item is read with its decision log entry through GET /api/recovery/v1/decision-log on SCR-28 to show the rule and package version that matched.

**Job JOB-07 Payment matching**: as in RWB-E2-008, with the row order of BR1, the RuleEvaluator call of step 4 and the decision log write before each proceeds row. Idempotency key unchanged (payment_code). Restart: a payment whose decision log write failed has no proceeds row and is picked up by the next run.

**Published interfaces called**

```java
// P3, published in RWB-E1-072 (recovery.casewf.rules)
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
RuleRow RuleCatalog.row(String ruleId, String packageVersion);
// P7
DecisionLogRef DecisionLogApi.write(DecisionLogRequest request) throws DecisionLogWriteException;
// P3
void TreatmentApi.recordInstallmentPaid(UUID treatmentId, UUID proceedsId, LocalDate dueDate,
                                        BigDecimal amount, BigDecimal shortfall);
```

The reference-loads endpoint is not used for payment matching: the PAYMENT_MATCH package is loaded only through the rule package endpoint above (D-RCV-36 T10).

## 13. Solution plan

**Package.** folder `recovery/payments/matching`, Java package `recovery.payments.matching`.

| Component | Type | Responsibility |
|---|---|---|
| PaymentMatchFactsBuilder | Service | Builds the facts of the payment, the account, the installment and the business date |
| PaymentMatcher | Service | From RWB-E2-008; calls RuleEvaluator for PAYMENT_MATCH, applies the fired row, writes the decision log entry first |
| MatchDecisionWriter | Service | Builds the D5 DecisionLogRequest with the rule ID, the package version and the inputs |
| MatchOutcomeReader | Service | Maps the RuleResult outputs to the proceeds row and the shortfall passed to TreatmentApi |

**Database.** No migration and no table in this story. RWB-E1-072 and RWB-E2-042 create rule_package, rule_package_version and the rule_row columns; RWB-E2-008 drops payment_match_rule. The proceeds table is unchanged.

**Configuration and reference data.** PAYMENT_MATCH version PM-2026.12 with the three rows of the Background; the window of 3 days after and the partial floor of 90 percent are assumed values owned by Credit Administration. Match types EXACT, WINDOW and PARTIAL are the row names of the package (RWB-E2-042). The package code PAYMENT_MATCH is seeded by RWB-E2-042.

**Build steps**

1. Write PaymentMatchFactsBuilder and unit test the facts for AC1, AC2 and AC8.
2. Call RuleEvaluator for PAYMENT_MATCH in PaymentMatcher and map the RuleResult to the match outcome; test AC1, AC2, AC4, AC5, AC8, AC9.
3. Build MatchDecisionWriter with the rule ID and the package version from the result; put the decision log write before the proceeds write; test AC7.
4. Test AC3 with two approved versions and the business date boundary.
5. Test AC6 with a workbook that fails the schema check on load, through the endpoint of section 12.
6. Test AC10 with no version in force for the business date.
7. Pass the shortfall to TreatmentApi; test AC2 end to end with the P3 stub.

**Feature flag.** `rwb.payments.matching-rules`. Off: JOB-07 matches on the EXACT row only, as in RWB-E2-008. The load endpoint is behind `rwb.p3.drools` (RWB-E1-073).

**Done when.** The tests in section 16 pass, and a synthetic month of 1,000 payments runs with every decision log entry naming a rule ID and a package version.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P3-027 | A package version check fails, or no version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-001 | An empty file is loaded | Enter {field}. |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 the {check} value is compile, schema, scenario or package in force, and {detail} names the row ID, the column or the package code only, never a payment or a person. Thai text follows DL10.

## 15. Screens and states

SCR-28 Proceeds matching (states Loading; matched; unmatched) shows, for each matched receipt, the rule ID and the package version from its decision log entry, and for each unmatched receipt the reason. PAYMENT_MATCH versions show on SCR-39 Rules and parameters (Epic 8); until then the version list is read through GET /admin/rule-packages/PAYMENT_MATCH/versions. Reference data on SCR-40 holds no payment matching table.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-027-01 | AC1, BR2, BR6 | System | PAY-91001 12,500.00; PAYMENT_MATCH version PM-2026.12 |
| TC-E2-027-02 | AC2, BR4 | System | PAY-91002 11,875.00 |
| TC-E2-027-03 | AC3, BR6 | System | PM-2027.01 from 2027-01-01; PAY-91003 4 days late |
| TC-E2-027-04 | AC4, BR3, BR5 | System | PAY-91004 3 days late, PAY-91005 4 days late |
| TC-E2-027-05 | AC5, BR4, BR5 | System | PAY-91006 10,000.00 |
| TC-E2-027-06 | AC6, BR7 | System | PM-2027.02 with duplicate row order and tolerance 120 |
| TC-E2-027-07 | AC7, BR8 | System | Decision log stubbed unavailable |
| TC-E2-027-08 | AC8, BR2 | System | PAY-91007 13,000.00 |
| TC-E2-027-09 | AC9, BR1 | System | PAY-91008 matched by two rows |
| TC-E2-027-10 | AC10, BR9 | System | No PAYMENT_MATCH version in force on 2027-02-01 |
| TC-E2-027-11 | Access | Access | RW-CASEOWN calls GET /proceeds; refused with MSG-P4-002 |
| TC-E2-027-12 | Access | Access | RW-CASEOWN calls POST /admin/rule-packages/PAYMENT_MATCH/versions; refused with MSG-P4-002 |
| TC-E2-027-13 | Principle 5 | Resilience | Decision log write forced to fail for 50 payments; no proceeds row written |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: match type, row order, tolerance, window, grace and partial floor are columns of the PAYMENT_MATCH rule rows.
- No personal data in logs, tests, workflow history or prompts: decision log inputs hold payment code, amount, dates and rule ID only.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: payments, accounts and plans come through P1 and P3 interfaces.
- The decision log entry is written before the proceeds row; no match exists without its entry.
- One evaluator: the matching engine calls RuleEvaluator and reads no workbook, drl_source or rule_row directly.
- The package version in force is chosen at evaluation time from the business date, and no match is made without a version in force.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-RES-28, R-UNI-03, R-UNI-38, R-UNI-39, R-UNI-41 | TC-E2-027-01 to TC-E2-027-13 |

## 19. Out of scope

- Settlement payment matching and partial settlement installments (FEAT-PAY-03, Epic 4).
- Manual matching from SCR-28 (POST /proceeds/{proceedsId}/match, Epic 4).
- The reconciliation agent that works the exception list (Epic 4).
- Applying proceeds to the case balance in policy order (FEAT-PAY-10, Epic 4).
- Authoring the PAYMENT_MATCH rows, their scenarios and their approval (RWB-E2-042, RWB-E1-073).
- The retired payment_match_rule table and its reference loads (D-RCV-36 T10).
