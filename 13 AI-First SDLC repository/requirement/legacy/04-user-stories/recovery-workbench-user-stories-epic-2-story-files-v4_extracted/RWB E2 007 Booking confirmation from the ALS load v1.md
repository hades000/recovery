<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 007 Booking confirmation from the ALS load v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 007 Booking confirmation from the ALS load v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-007 Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group, 28 October 2026.

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
| Decision | D6.4 |
| Priority | Must |
| Depends on | RWB-E2-004, RWB-E1-007 |
| Status | Ready for build |

## 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the booked terms of each approved restructure or settlement matched from the next day's ALS load to the approved treatment, with a task when the booking is missing or differs**, so that **every approved decision is confirmed as booked in the core bank**.

## 2. Business rationale

The officer books restructures and settlements in ALS by hand (INT-03), and nothing checks today that the booked terms equal the approved terms. This story compares each approved treatment with the next ALS load, marks it booked when the terms match, and raises a task to the officer when the booking is missing or to Credit Administration when the terms differ. It meets REQ-CHO-008 and is measured by REC-03 (approved treatments against bookings, zero after two days).

## 3. Preconditions

- RWB-E2-004 (treatment entity) and RWB-E1-007 (adapters, IdempotencyGuard) are done.
- JOB-01 loads INT-01 with tdr_flag, last_tdr_date, interest_rate and principal_outstanding, and the two new settlement booking fields, for business date D.
- The booking match rows are loaded (versioned reference data): for RESTRUCTURE compare tdr_flag, last_tdr_date, principal_outstanding against offer_amount and interest_rate against the approved rate; for SETTLEMENT compare settlement_booked_date and settlement_booked_amount against offer_amount; tolerance 0.00 baht (DL25).
- Parameter `booking.missing.grace_loads` = 1 (one ALS load after approval).
- Rules R-RES-22 and R-SET-13 are in force.
- TreatmentApproved (EV-10) is published for each approved treatment.

## 4. Flow

1. Scheduler: JOB-08 starts after JOB-01 publishes LoadCompleted (EV-26) for ALS with business date D.
2. SY-DATALOAD: the BookingMatchService lists approved treatments of type RESTRUCTURE or SETTLEMENT not yet booked, through the treatment interface.
3. SY-DATALOAD: for each treatment, checks IdempotencyGuard on treatment ID + D; a repeat is skipped.
4. SY-DATALOAD: reads every account of the case through the P1 AccountQuery for business date D.
5. SY-DATALOAD: applies the booking match rows for the treatment type to each account.
6. SY-DATALOAD: when every account matches, calls TreatmentCommands.markBooked with the business date; P8 publishes TreatmentBooked (EV-11); P3 writes the decision log entry and moves the case by R-RES-22 or R-SET-13.
7. SY-DATALOAD: when no booking is found after the grace loads, raises one task WITH_OPS_BOOKING or WITH_OPS_SETTLEMENT for role RW-RESTRUCT with MSG-P2-011; the treatment stays approved.
8. SY-DATALOAD: when a booking is found with a different term, writes the difference on the treatment and raises one task UNMATCHED_EXCEPTION for role RW-CREDITAD with MSG-P2-012; the treatment stays approved.
9. SY-DATALOAD: writes the run summary: treatments read, booked, missing, differing; the P1 reconciliation REC-03 reads the same results.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No booking in the next load | Task to the officer; treatment stays approved | MSG-P2-011 | AC2 |
| X2 | A booked term differs from the approved term | Difference written on the treatment; task to Credit Administration | MSG-P2-012 | AC3 |
| X3 | Only some accounts of the case are booked | The treatment stays approved; the task names the accounts without a booking | MSG-P2-011 | AC4 |
| X4 | The ALS load for D was refused or is late | JOB-08 does not run for D; no missing booking is raised for D | MSG-P1-001 | AC5 |
| X5 | JOB-08 runs twice for the same business date | No second booking, event or task | None | AC6 |
| X6 | A booking is still missing on the next load | No second task; the open task stays | None | AC7 |
| X7 | The decision log write fails when the booking is confirmed | The treatment stays approved; an incident is raised; the match runs again with the next load | MSG-P7-003 | AC8 |
| X8 | A role without the right reruns JOB-08 | Refused; nothing changes | MSG-P4-002 | TC-E2-007-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the treatment entity (RWB-E2-004) and the ALS load |
| Negotiable | Terms compared, tolerance and grace are data rows |
| Valuable | Every approved restructure and settlement is confirmed as booked or raised |
| Estimable | One matching service, one job, two task paths |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: Booking confirmation from the ALS load

  Background:
    Given the booking match rows version "BKG-2026.12" are in force with tolerance 0.00 baht
    Given the ALS load for business date 2026-12-16 passed its checks

  Scenario: AC1 Booking confirmed
    Given settlement treatment "TRT-SYN-0701" on case "RW-2026-000701" was approved on 2026-12-15 with offer amount 650,000.00 baht
    Given the officer booked the settlement in ALS on 2026-12-16
    Given the ALS load shows settlement booked date 2026-12-16 and settlement booked amount 650,000.00 baht for synthetic account "A-0701"
    When the next day's ALS load arrives and JOB-08 runs on 2026-12-17
    Then the booked terms match the approved treatment and the treatment state is "BOOKED" with booked at 2026-12-16
    Then the system publishes treatmentBooked with business date 2026-12-16
    Then the route state moves from "WITH_OPS_SETTLEMENT" to "AWAITING_PAYMENT" by R-SET-13 with a decision log entry

  Scenario: AC2 Booking missing
    Given restructure treatment "TRT-SYN-0702" was approved on 2026-12-15
    Given the ALS load of 2026-12-16 shows tdr_flag false for synthetic account "A-0702"
    When the match runs
    Then the system raises a task "WITH_OPS_BOOKING" for role "RW-RESTRUCT" with message MSG-P2-011
    Then the treatment stays "APPROVED"

  Scenario: AC3 Terms differ
    Given restructure treatment "TRT-SYN-0703" was approved with offer amount 1,800,000.00 baht and rate 4.2500 percent
    Given the ALS load shows tdr_flag true, last TDR date 2026-12-16, principal 1,800,000.00 baht and rate 4.5000 percent for "A-0703"
    When the match runs
    Then the treatment shows the difference: interest rate approved 4.2500, booked 4.5000
    Then a task "UNMATCHED_EXCEPTION" goes to role "RW-CREDITAD" with message MSG-P2-012
    Then the treatment stays "APPROVED"

  Scenario: AC4 Only some accounts booked
    Given restructure treatment "TRT-SYN-0704" covers synthetic accounts "A-0704" and "A-0705"
    Given only "A-0704" shows the booking in the ALS load
    When the match runs
    Then the treatment stays "APPROVED"
    Then the task for "RW-RESTRUCT" names account "A-0705" as not booked

  Scenario: AC5 ALS load refused
    Given the ALS load for business date 2026-12-17 was refused at "DQ-003 Control total"
    When JOB-08 is due on 2026-12-18
    Then JOB-08 does not run for 2026-12-17
    Then the system raises no missing booking task for 2026-12-17

  Scenario: AC6 Match run twice
    Given JOB-08 marked "TRT-SYN-0701" booked for business date 2026-12-16
    When JOB-08 is rerun for 2026-12-16
    Then the system publishes no second TreatmentBooked event
    Then the system raises no task

  Scenario: AC7 Booking still missing on the next load
    Given task "WITH_OPS_BOOKING" is open for "TRT-SYN-0702" from the load of 2026-12-16
    When the load of 2026-12-17 still shows no booking
    Then the system raises no second task
    Then the REC-03 break list for the data steward shows "TRT-SYN-0702" as missing for 2 days

  Scenario: AC8 Decision log write fails on confirmation
    Given the decision log store is unavailable
    When the match finds "TRT-SYN-0701" booked
    Then the treatment stays "APPROVED" and no TreatmentBooked event is published
    Then the system raises an incident with message MSG-P7-003
    Then the match runs again with the next load
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Bookings are made by the officer in ALS and confirmed only from the next ALS load | INT-03; DL12 |
| BR2 | A restructure is booked when every account shows tdr_flag true with a last TDR date on or after the approval date and the terms match | Booking match rows; DF-ACC-019; DF-ACC-020; CTL-26 |
| BR3 | A settlement is booked when the account shows a settlement booked date on or after the approval date and the booked amount equals the offer amount | Booking match rows; R-SET-13 |
| BR4 | The tolerance on amounts and rates is zero | DL25 |
| BR5 | A missing booking after the grace loads raises one task to the officer | REC-03; parameter booking.missing.grace_loads |
| BR6 | A difference in terms raises one task to Credit Administration | REC-03; FEAT-CHO-08 |
| BR7 | A confirmed booking moves the case | R-RES-22, R-SET-13 |
| BR8 | No missing booking is raised for a business date without a good ALS load | JOB-08 depends on JOB-01; CTL-02 |
| BR9 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| WITH_OPS_BOOKING | BOOKING_CONFIRMED | ALS and NLEADS both acknowledge: NLEADS result APPROVED recorded and every account matched | BOOKED_IN_ALS_NLEADS |
| WITH_OPS_SETTLEMENT | SETTLEMENT_BOOKED | Agreement signed and terms booked in ALS | AWAITING_PAYMENT |

The treatment state moves from APPROVED to BOOKED. A missing or differing booking leaves both the route state and the treatment state unchanged.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Runs JOB-08, reads accounts, marks bookings, raises tasks |
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
| DF-CAS-026 | case_account | account_id | Read |
| DF-ACC-001 | loan_account | id | Read |
| DF-ACC-008 | loan_account | interest_rate | Read |
| DF-ACC-009 | loan_account | principal_outstanding | Read |
| DF-ACC-019 | loan_account | tdr_flag | Read |
| DF-ACC-020 | loan_account | last_tdr_date | Read |
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-ACC-030 | loan_account | settlement_booked_date | Read |
| DF-ACC-031 | loan_account | settlement_booked_amount | Read |
| DF-WRK-018 | task | case_id | Write, through the P3 interface |
| DF-WRK-019 | task | task_code | Write, through the P3 interface |
| DF-WRK-022 | task | status | Write, through the P3 interface |
| DF-WRK-023 | task | owner_role | Write, through the P3 interface |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job JOB-08 Booking confirmation.** Trigger: Quartz, daily after JOB-01 publishes LoadCompleted (EV-26) for ALS. Input: approved RESTRUCTURE and SETTLEMENT treatments not booked; accounts for business date D; booking match rows. Output: booked treatments, differences, tasks, run summary. Events consumed: TreatmentApproved (EV-10), LoadCompleted (EV-26). Events published: TreatmentBooked (EV-11) by P8 with treatmentId, bookingRef (account ID + business date) and businessDate; CaseStateChanged (EV-05) by P3. Idempotency key: treatment ID + business date. Restart: POST /admin/jobs/{jobId}/rerun; treatments already handled for D are skipped.

**Endpoints used.**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| POST /admin/jobs/{jobId}/rerun | Path: jobId | Job | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-P4-003); 409 running (MSG-P2-006); 503 (MSG-P7-003) | Platform administration, U | Per treatment and business date |
| GET /treatments/{treatmentId} | Path: treatmentId | Treatment, with booked at and the booking difference | 401; 403; 404; 503 | Treatment and offer, R | Read only |

**Published interfaces called.**

```java
// treatment interface from RWB-E2-004
List<TreatmentView> TreatmentQuery.approvedNotBooked(Set<String> treatmentTypes);
void TreatmentCommands.markBooked(UUID treatmentId, LocalDate businessDate, String bookingRef); // writes the decision log entry first; throws DecisionLogUnavailableException
void TreatmentCommands.recordBookingDifference(UUID treatmentId, List<TermDifference> differences);
// P1 recovery.data.api
List<AccountView> AccountQuery.forCase(UUID caseId, LocalDate businessDate);
// P3 recovery.casewf.api
UUID TaskApi.raiseTask(UUID caseId, String taskCode, String ownerRole, String messageId, Map<String, String> params); // returns the open task when one exists for the same case, code and treatment
```

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/booking`, Java package `recovery.integration.booking`.

| Component | Type | Responsibility |
|---|---|---|
| BookingMatchService | Service | Applies the match rows per account; decides booked, missing, partly booked or differing |
| BookingMatchJob | Job | JOB-08; runs after JOB-01 for business date D only when the load passed |
| BookingMatchRules | Rule table | Versioned rows: treatment type, ALS field, treatment field, comparison, tolerance |
| TreatmentApprovedListener | Listener | Consumes EV-10 through IdempotencyGuard and records the approval date used by the match |
| BookingRunSummaryWriter | Service | Writes counts to interface_run.checks for REC-03 |

- **Database:** no P2 table. The new treatment columns interest_rate numeric(7,4) and booking_difference jsonb are added by the treatment owner; the new loan_account columns settlement_booked_date date and settlement_booked_amount numeric(18,2) are added by P1 with the INT-01 mapping.
- **Configuration and reference data:** booking match rows (RW-COE, CTL-08); tolerance 0.00 (DL25); parameter booking.missing.grace_loads = 1; ALS source fields for the two settlement booking columns to confirm with the system owner (DL12).
- **Build steps:**
  1. Build BookingMatchRules and the comparison evaluator with a test per row.
  2. Build BookingMatchService for one account and then for several accounts per case.
  3. Wire TreatmentCommands.markBooked and handle DecisionLogUnavailableException with no change.
  4. Wire the two task paths through TaskApi with one open task per treatment.
  5. Build BookingMatchJob with the dependency on a passed JOB-01 load and the idempotency key.
  6. Write the run summary for REC-03.
- **Feature flag:** `rwb.integration.booking-confirmation`.
- **Done when:** the tests in section 16 pass and REC-03 for a SIT week shows every synthetic approved treatment booked or raised.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-011 | Task text, booking missing | No booking for treatment {treatment} was found in the ALS load for {date}. Book it in ALS. Accounts not booked: {accounts}. |
| MSG-P2-012 | Task text and treatment note, term differs | The booked {term} is {booked}. The approved {term} is {approved}. |
| MSG-P1-001 | ALS load late or refused | {product} is from {date}. Today's load has not arrived. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | Rerun while JOB-08 runs | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the right reruns JOB-08 | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-14 Treatment record, states approved and booked: the officer sees booked at, or the booking difference with each term approved and booked. The officer and the Credit Administration officer see their tasks on SCR-01 My work. SCR-29 Posting, which shows the confirmation for all bookings, comes in Epic 4.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-007-01 | AC1, BR1, BR3, BR7 | System | Synthetic settlement booked 2026-12-16 at 650,000.00 baht |
| TC-E2-007-02 | AC2, BR5 | System | Restructure with tdr_flag false |
| TC-E2-007-03 | AC3, BR2, BR4, BR6 | System | Rate 4.5000 booked against 4.2500 approved |
| TC-E2-007-04 | AC4, BR2 | System | Two accounts, one booked |
| TC-E2-007-05 | AC5, BR8 | System | ALS load refused for 2026-12-17 |
| TC-E2-007-06 | AC6 | System | JOB-08 rerun for 2026-12-16 |
| TC-E2-007-07 | AC7, BR5 | System | Booking missing on two loads |
| TC-E2-007-08 | AC8, BR9 | System | Decision log store stopped |
| TC-E2-007-09 | Access | Access | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun for JOB-08; refused with MSG-P4-002 |
| TC-E2-007-10 | Principle 5 | Resilience | Decision log write forced to fail on markBooked; treatment stays APPROVED, no event |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: compared terms, tolerance and grace are rows or parameters.
- No personal data in logs, tests or prompts; the booking reference holds the account ID, not the account number.
- No read of another module's tables; accounts, treatments and tasks are reached through their interfaces.
- No call to ALS; the match reads only the loaded data.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Booking confirmed from the next day's ALS load | Program 5.3; Epic 2 3.2 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39 | TC-E2-007-01 to TC-E2-007-08, TC-E2-007-10 |

## 19. Out of scope

- Posting a settlement booking to ALS from the Workbench: FEAT-PAY-06, Epic 4.
- Payment matching to the plan or settlement: JOB-07 and FEAT-OCC-10, Epic 2.
- The SCR-29 Posting screen: Epic 4.
