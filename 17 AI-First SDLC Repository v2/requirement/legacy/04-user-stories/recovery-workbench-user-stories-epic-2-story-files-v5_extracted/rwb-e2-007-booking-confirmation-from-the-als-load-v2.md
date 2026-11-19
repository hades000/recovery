<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 007 Booking confirmation from the ALS load v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 007 Booking confirmation from the ALS load v2.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-007 Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-007 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration, with P8 Payments and posting |
| Feature | FEAT-CHO-08 Confirm booked terms from the ALS load |
| Requirement IDs | REQ-CHO-008 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, section 5.3 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E2-004, RWB-E1-069, RWB-E1-007, RWB-E1-072, RWB-E2-042 |
| Status | Ready for build |

## 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the booked terms of each approved restructure or settlement compared with the account as ACE holds it after the next ALS batch, with a task when the booking is missing or differs**, so that **every approved decision is confirmed as booked in the core bank without a file the Workbench has to load**.

## 2. Business rationale

The officer books restructures and settlements in ALS by hand (INT-03), and nothing checks today that the booked terms equal the approved terms. ACE ingests the ALS batch and the booked terms appear on the account. This story compares each approved treatment with v_ace_account for the business date once the ACE batch for ALS is COMPLETE, marks the treatment booked when the terms match, and raises a task to the officer when the booking is missing or to Credit Administration when the terms differ. It meets REQ-CHO-008 and is measured by REC-03 (approved treatments against bookings, zero after two days).

The compared terms, the tolerance and the outcomes are rows of package BOOKING_MATCH under ADR-012, fixed by D-RCV-36 on 16 November 2026. SY-RULES evaluates the package through RuleEvaluator for each treatment and account, the result names the row and the package version, and the service holds no comparison code of its own.

## 3. Preconditions

- RWB-E2-004 (treatment entity) and RWB-E1-069 (read-only ACE source views) are done; v_ace_account is granted SELECT to the recovery service identity.
- RWB-E1-007 (adapters and IdempotencyGuard) is done; the recovery service identity reads the views only.
- RWB-E1-072 is done: RuleEvaluator and the rule package store exist.
- RWB-E2-042 is done: package BOOKING_MATCH is in force with version "BKG-2026.12" and rows for RESTRUCTURE and SETTLEMENT: for RESTRUCTURE compare tdr_flag, last_tdr_date and principal_outstanding against offer_amount, and interest_rate against the approved rate; for SETTLEMENT compare settlement_booked_date and settlement_booked_amount against offer_amount; tolerance 0.00 baht (DL25).
- v_ace_batch_status (V0003, RWB-ACE-001, DL43) carries the ALS business date and the COMPLETED status that trigger the match.
- The Section B columns settlement_booked_date and settlement_booked_amount of v_ace_account ship in V0003 with RWB-ACE-001; a settlement is confirmed only once V0003 is applied and the flag is on. A restructure is confirmed from Section A columns alone.
- Parameter `booking.missing.grace_loads` = 1 (one ALS batch after approval).
- Rules R-RES-22 and R-SET-13 are in force.
- TreatmentApproved (EV-10) is published for each approved treatment.

## 4. Flow

1. Scheduler: JOB-08 starts when AceDataReady (EV-26) arrives for ALS with business date D.
2. BookingMatchService: lists approved treatments of type RESTRUCTURE or SETTLEMENT not yet booked, through the treatment interface.
3. BookingMatchService: for each treatment, checks IdempotencyGuard on treatment ID + D; a repeat is skipped.
4. BookingMatchService: reads every account of the case from v_ace_account at business date D through the P1 AccountQuery.
5. BookingMatchService: builds BookingMatchFacts for the treatment and each account (treatment type, approved terms, account fields) and calls RuleEvaluator.evaluate("BOOKING_MATCH", facts, D); the result names the row that decided, the outcome BOOKED, NO_BOOKING or TERMS_DIFFER, the difference terms and the package version.
6. BookingMatchService: when the outcome is BOOKED for every account, calls TreatmentCommands.markBooked with the business date; P8 publishes TreatmentBooked (EV-11); P3 writes the decision log entry and moves the case by R-RES-22 or R-SET-13.
7. BookingMatchService: when the outcome is NO_BOOKING after the grace batches, raises one task WITH_OPS_BOOKING or WITH_OPS_SETTLEMENT for role RW-RESTRUCT with MSG-P2-011; the treatment stays approved.
8. BookingMatchService: when the outcome is TERMS_DIFFER, writes the difference on the treatment and raises one task UNMATCHED_EXCEPTION for role RW-CREDITAD with MSG-P2-012; the treatment stays approved.
9. BookingMatchService: writes the run summary (treatments read, booked, missing, differing) and the REC-03 result to reconciliation_result.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No booking in the next batch | Task to the officer; treatment stays approved | MSG-P2-011 | AC2 |
| X2 | A booked term differs from the approved term | Difference written on the treatment; task to Credit Administration | MSG-P2-012 | AC3 |
| X3 | Only some accounts of the case are booked | The treatment stays approved; the task names the accounts without a booking | MSG-P2-011 | AC4 |
| X4 | The ACE batch for ALS and business date D is not COMPLETE | JOB-08 does not run for D; no missing booking is raised for D | MSG-P1-001 | AC5 |
| X5 | JOB-08 runs twice for the same business date | No second booking, event or task | None | AC6 |
| X6 | A booking is still missing on the next batch | No second task; the open task stays | None | AC7 |
| X7 | The decision log write fails when the booking is confirmed | The treatment stays approved; an incident is raised; the match runs again with the next batch | MSG-P7-003 | AC8 |
| X8 | A role without the right reruns JOB-08 | Refused; nothing changes | MSG-P4-002 | TC-E2-007-10 |
| X9 | No BOOKING_MATCH version is IN_FORCE on the business date | NoPackageInForce; no treatment is marked booked, no difference is written and no task is raised; the run ends as failed | MSG-P3-027 | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the treatment entity (RWB-E2-004), the ACE account view, the evaluator of RWB-E1-072 and the BOOKING_MATCH package of RWB-E2-042 |
| Negotiable | Terms compared, tolerance and grace are package rows or parameters |
| Valuable | Every approved restructure and settlement is confirmed as booked or raised |
| Estimable | One matching service, one job, two task paths, one rule package |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: Booking confirmation from the ALS load

  Background:
    Given package "BOOKING_MATCH" version "BKG-2026.12" is in force with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht
    Given the ACE batch for ALS with business date 2026-12-16 is COMPLETED

  Scenario: AC1 Booking confirmed
    Given settlement treatment "TRT-SYN-0701" on case "RW-2026-000701" was approved on 2026-12-15 with offer amount 650,000.00 baht
    Given the officer booked the settlement in ALS on 2026-12-16
    Given v_ace_account shows settlement booked date 2026-12-16 and settlement booked amount 650,000.00 baht for synthetic account "A-0701" at business date 2026-12-16
    When the next day's ALS batch is complete and JOB-08 runs on 2026-12-17
    Then the SETTLEMENT row of package "BOOKING_MATCH" version "BKG-2026.12" decides that the account is booked
    Then the booked terms match the approved treatment and the treatment state is "BOOKED" with booked at 2026-12-16
    Then the system publishes treatmentBooked with business date 2026-12-16
    Then the route state moves from "WITH_OPS_SETTLEMENT" to "AWAITING_PAYMENT" by R-SET-13 with a decision log entry

  Scenario: AC2 Booking missing
    Given restructure treatment "TRT-SYN-0702" was approved on 2026-12-15
    Given v_ace_account at business date 2026-12-16 shows tdr_flag false for synthetic account "A-0702"
    When the match runs
    Then the RESTRUCTURE row of package "BOOKING_MATCH" returns the outcome "NO_BOOKING"
    Then the system raises a task "WITH_OPS_BOOKING" for role "RW-RESTRUCT" with message MSG-P2-011
    Then the treatment stays "APPROVED"

  Scenario: AC3 Terms differ
    Given restructure treatment "TRT-SYN-0703" was approved with offer amount 1,800,000.00 baht and rate 4.2500 percent
    Given v_ace_account shows tdr_flag true, last TDR date 2026-12-16, principal 1,800,000.00 baht and rate 4.5000 percent for "A-0703"
    When the match runs
    Then the RESTRUCTURE row of package "BOOKING_MATCH" returns the outcome "TERMS_DIFFER" with approved rate 4.2500 and booked rate 4.5000
    Then the treatment shows the difference: interest rate approved 4.2500, booked 4.5000
    Then a task "UNMATCHED_EXCEPTION" goes to role "RW-CREDITAD" with message MSG-P2-012
    Then the treatment stays "APPROVED"

  Scenario: AC4 Only some accounts booked
    Given restructure treatment "TRT-SYN-0704" covers synthetic accounts "A-0704" and "A-0705"
    Given only "A-0704" shows the booking in v_ace_account at business date 2026-12-16
    When the match runs
    Then the treatment stays "APPROVED"
    Then the task for "RW-RESTRUCT" names account "A-0705" as not booked

  Scenario: AC5 ACE batch not complete
    Given the ACE batch for ALS with business date 2026-12-17 ended "FAILED"
    When JOB-08 is due on 2026-12-18
    Then JOB-08 does not run for 2026-12-17
    Then the system raises no missing booking task for 2026-12-17

  Scenario: AC6 Match run twice
    Given JOB-08 marked "TRT-SYN-0701" booked for business date 2026-12-16
    When JOB-08 is rerun for 2026-12-16
    Then the system publishes no second TreatmentBooked event
    Then the system raises no task

  Scenario: AC7 Booking still missing on the next batch
    Given task "WITH_OPS_BOOKING" is open for "TRT-SYN-0702" from the batch of 2026-12-16
    When the batch of 2026-12-17 still shows no booking
    Then the system raises no second task
    Then the REC-03 break list for the data steward shows "TRT-SYN-0702" as missing for 2 days

  Scenario: AC8 Decision log write fails on confirmation
    Given the decision log store is unavailable
    When the match finds "TRT-SYN-0701" booked
    Then the treatment stays "APPROVED" and no TreatmentBooked event is published
    Then the system raises an incident with message MSG-P7-003
    Then the match runs again with the next batch

  Scenario: AC9 No BOOKING_MATCH version in force
    Given no BOOKING_MATCH version is IN_FORCE on 2026-12-17
    When JOB-08 starts for business date 2026-12-16
    Then NoPackageInForce is thrown with MSG-P3-027 for package "BOOKING_MATCH"
    Then no treatment is marked booked, no difference is written and no task is raised
    Then the run ends as failed and alerts role "RW-PLATADM"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Bookings are made by the officer in ALS and confirmed only from the next ACE batch | INT-03; DL12; D-RCV-35 U1 |
| BR2 | A restructure is booked when every account matches the RESTRUCTURE rows of package BOOKING_MATCH: tdr_flag true with a last TDR date on or after the approval date and the terms equal | DF-ACE-031; DF-ACE-030; CTL-26; D-RCV-36 T5 |
| BR3 | A settlement is booked when the account matches the SETTLEMENT rows of package BOOKING_MATCH: a settlement booked date on or after the approval date and a booked amount equal to the offer amount | R-SET-13; D-RCV-36 T5 |
| BR4 | The tolerance on amounts and rates is zero in the row of package BOOKING_MATCH in force | DL25 |
| BR5 | A missing booking after the grace batches raises one task to the officer | REC-03; parameter booking.missing.grace_loads |
| BR6 | A difference in terms raises one task to Credit Administration | REC-03; FEAT-CHO-08 |
| BR7 | A confirmed booking moves the case | R-RES-22, R-SET-13 |
| BR8 | No missing booking is raised for a business date whose ACE batch for ALS is not COMPLETE | JOB-08; CTL-02 |
| BR9 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |
| BR10 | The match is decided by package BOOKING_MATCH through RuleEvaluator; the result names the row and the package version, and the story holds no comparison code and no rule table | D-RCV-36 T3, T5; ADR-012 |
| BR11 | No BOOKING_MATCH version in force is a refusal (NoPackageInForce), never a default match | R-UNI-41; D-RCV-36 T7 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| WITH_OPS_BOOKING | BOOKING_CONFIRMED | NLEADS result APPROVED recorded and every account matched | BOOKED_IN_ALS_NLEADS |
| WITH_OPS_SETTLEMENT | SETTLEMENT_BOOKED | Agreement signed and terms booked in ALS | AWAITING_PAYMENT |

The treatment state moves from APPROVED to BOOKED. A missing or differing booking leaves both the route state and the treatment state unchanged.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery service identity, JOB-08 | Reads the ACE views, calls the rule evaluator, marks bookings, raises tasks |
| SY-RULES, Drools evaluator | Evaluates package BOOKING_MATCH for each treatment and account and returns the row, the outcome and the package version |
| SY-CASEWF, case workflow module | Moves the case on BOOKING_CONFIRMED or SETTLEMENT_BOOKED; raises the tasks |
| SY-DECLOG, decision log writer | Writes the entry (Decision log, C) |
| RW-RESTRUCT, restructuring officer | Receives the missing booking task and books in ALS (Treatment and offer, CRUA) |
| RW-CREDITAD, Credit Administration officer | Receives the differing terms task (Write-off and posting, CRUA) |
| RW-DATASTEW, data steward | Reads the REC-03 break list |
| RW-PLATADM, platform administrator | Reruns JOB-08 (Platform administration, U) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-012 | treatment | booked_at | Write |
| DF-TRT-027 | treatment | interest_rate | Read |
| DF-TRT-028 | treatment | booking_difference | Write |
| Standard column | treatment | state | Write |
| DF-CAS-026 | case_account | account_key | Read |
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-025 | v_ace_account | interest_rate | Read |
| DF-ACC-009 | v_ace_account | principal_outstanding | Read (Section B, RWB-ACE-001) |
| DF-ACE-031 | v_ace_account | tdr_flag | Read |
| DF-ACE-030 | v_ace_account | last_tdr_date | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACC-030 | v_ace_account | settlement_booked_date | Read (Section B, RWB-ACE-001) |
| DF-ACC-031 | v_ace_account | settlement_booked_amount | Read (Section B, RWB-ACE-001) |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-WRK-018 | task | case_id | Write, through the P3 interface |
| DF-WRK-019 | task | task_code | Write, through the P3 interface |
| DF-WRK-022 | task | status | Write, through the P3 interface |
| DF-WRK-023 | task | owner_role | Write, through the P3 interface |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | all fields | Write (REC-03) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary. The two Section B fields keep their frozen field-gap IDs until the LDM assigns DF-ACE IDs to the 12 added columns. The matching row and its version are read through RuleEvaluator; this story reads no rule_row column directly, no drl_source and no workbook.

## 12. Contract

**Job JOB-08 Booking confirmation.** Trigger: Quartz, on AceDataReady (EV-26) for ALS with business date D. Input: approved RESTRUCTURE and SETTLEMENT treatments not booked; v_ace_account rows for business date D; the BOOKING_MATCH version in force. Output: booked treatments, differences, tasks, the REC-03 result. Rule evaluation: RuleEvaluator.evaluate("BOOKING_MATCH", facts, D) for each treatment and account. The package is loaded, approved and rolled back through RWB-E1-073 and RWB-E2-042; this story only evaluates it. Events consumed: TreatmentApproved (EV-10), AceDataReady (EV-26). Events published: TreatmentBooked (EV-11) by P8 with treatmentId, bookingRef (account_key + business date) and businessDate; CaseStateChanged (EV-05) by P3. Idempotency key: treatment ID + business date. Restart: POST /admin/jobs/{jobId}/rerun; treatments already handled for D are skipped.

**Endpoints used.**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| POST /api/recovery/v1/admin/jobs/{jobId}/rerun | Path: jobId | Job | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-P4-003); 409 running (MSG-P2-006); 503 (MSG-P7-003) | Platform administration, U | Per treatment and business date |
| GET /api/recovery/v1/treatments/{treatmentId} | Path: treatmentId | Treatment, with booked at and the booking difference | 401; 403; 404; 503 | Treatment and offer, R | Read only |

**Published interfaces called.**

```java
// treatment interface from RWB-E2-004
List<TreatmentView> TreatmentQuery.approvedNotBooked(Set<String> treatmentTypes);
void TreatmentCommands.markBooked(UUID treatmentId, LocalDate businessDate, String bookingRef); // writes the decision log entry first; throws DecisionLogUnavailableException
void TreatmentCommands.recordBookingDifference(UUID treatmentId, List<TermDifference> differences);
// P3 recovery.casewf.rules (published, RWB-E1-072)
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
// P1 recovery.data.api, over recovery.v_ace_account
List<AccountView> AccountQuery.forCase(UUID caseId, LocalDate businessDate);
// P1 recovery.data.api, over recovery.v_ace_batch_status
BatchStatus BatchStatusQuery.forSource(String sourceSystem, LocalDate businessDate); // status, isComplete
// P3 recovery.casewf.api
UUID TaskApi.raiseTask(UUID caseId, String taskCode, String ownerRole, String messageId, Map<String, String> params); // returns the open task when one exists for the same case, code and treatment
```

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/booking`, Java package `recovery.integration.booking`.

| Component | Type | Responsibility |
|---|---|---|
| BookingMatchService | Service | Builds BookingMatchFacts, calls RuleEvaluator("BOOKING_MATCH") and decides booked, missing, partly booked or differing from the result |
| BookingMatchJob | Job | JOB-08; runs on AceDataReady for business date D only when the batch is COMPLETE |
| BookingMatchFacts | Fact builder | Builds the facts for one treatment and account: treatment type, approved terms, account fields and the business date |
| TreatmentApprovedListener | Listener | Consumes EV-10 through IdempotencyGuard and records the approval date used by the match |
| BookingRunSummaryWriter | Service | Writes the REC-03 result to reconciliation_result |

- **Database:** no P2 table. The treatment columns interest_rate numeric(7,4) and booking_difference jsonb are added by the treatment owner in RWB-E2-004. No copy of account data is written: the booked terms are read from v_ace_account on each run.
- **Configuration and reference data:** package BOOKING_MATCH rows (RW-COE, RWB-E2-042); tolerance 0.00 (DL25) as a column of the row in force; parameter booking.missing.grace_loads = 1; the Section B columns settlement_booked_date and settlement_booked_amount arrive with V0003 (RWB-ACE-001). The package version in force per environment is recorded in `config/rule-packages.lock`; the values in this story are as at 16 November 2026.
- **Build steps:**
  1. Build BookingMatchFacts and the RuleEvaluator call with a test per package row; the service holds no comparison code and no rule table.
  2. Build BookingMatchService for one account and then for several accounts per case.
  3. Wire TreatmentCommands.markBooked and handle DecisionLogUnavailableException with no change.
  4. Wire the two task paths through TaskApi with one open task per treatment.
  5. Build BookingMatchJob with the AceDataReady trigger, the batch COMPLETE check, the no-package path and the idempotency key.
  6. Write the REC-03 result for the data steward.
- **Feature flag:** `rwb.integration.booking-confirmation`.
- **Done when:** the tests in section 16 pass and REC-03 for a SIT week shows every synthetic approved treatment booked or raised, with no comparison code in the service.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-011 | Task text, booking missing | No booking for treatment {treatment} was found in the ALS batch for {date}. Book it in ALS. Accounts not booked: {accounts}. |
| MSG-P2-012 | Task text and treatment note, term differs | The booked {term} is {booked}. The approved {term} is {approved}. |
| MSG-P1-001 | ACE batch late or not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No BOOKING_MATCH version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P2-006 | Rerun while JOB-08 runs | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the right reruns JOB-08 | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "BOOKING_MATCH" and the business date only, never a case or account fact.

## 15. Screens and states

SCR-14 Treatment record, states approved and booked: the officer sees booked at, or the booking difference with each term approved and booked. The officer and the Credit Administration officer see their tasks on SCR-01 My work. SCR-29 Posting, which shows the confirmation for all bookings, comes in Epic 4.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-007-01 | AC1, BR1, BR3, BR7, BR10 | System | Synthetic settlement booked 2026-12-16 at 650,000.00 baht |
| TC-E2-007-02 | AC2, BR5 | System | Restructure with tdr_flag false in v_ace_account |
| TC-E2-007-03 | AC3, BR2, BR4, BR6 | System | Rate 4.5000 booked against 4.2500 approved |
| TC-E2-007-04 | AC4, BR2 | System | Two accounts, one booked |
| TC-E2-007-05 | AC5, BR8 | System | ACE batch failed for 2026-12-17 |
| TC-E2-007-06 | AC6 | System | JOB-08 rerun for 2026-12-16 |
| TC-E2-007-07 | AC7, BR5 | System | Booking missing on two batches |
| TC-E2-007-08 | AC8, BR9 | System | Decision log store stopped |
| TC-E2-007-09 | AC9, BR11 | System | No BOOKING_MATCH version in force on 2026-12-17 |
| TC-E2-007-10 | Access | Access | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun for JOB-08; refused with MSG-P4-002 |
| TC-E2-007-11 | Principle 5 | Resilience | Decision log write forced to fail on markBooked; treatment stays APPROVED, no event |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: compared terms, tolerance and grace are rows of package BOOKING_MATCH or parameters.
- No personal data in logs, tests, workflow history or prompts; the booking reference holds the account_key, not the account number.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the match reads v_ace_account and v_ace_batch_status through the P1 interfaces (boundary rule, RWB-E1-069).
- No call to ALS; the match reads only what ACE holds for the completed batch.
- No comparison code and no rule table in the service: package BOOKING_MATCH decides, through RuleEvaluator.
- The rule package is loaded and approved through RWB-E1-073; this story evaluates it and never reads drl_source or the workbook.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Booking confirmed from the next day's ALS batch | Program 5.3; Epic 2 3.2 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39 | TC-E2-007-01 to TC-E2-007-09, TC-E2-007-11 |

## 19. Out of scope

- Posting a settlement booking to ALS from the Workbench: FEAT-PAY-06, Epic 4.
- Payment matching to the plan or settlement: JOB-07 and FEAT-OCC-10, Epic 2.
- The SCR-29 Posting screen: Epic 4.
- Authoring, approval and rollback of package BOOKING_MATCH (RWB-E2-042 and RWB-E1-073).
