<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 001 EFS hand over with full history from the COLLINS load v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 001 EFS hand over with full history from the COLLINS load v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-001 EFS hand-over with full history from the COLLINS load

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-001 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CHO-01 Take the case hand-over from EFS with full history; FEAT-CHO-04 Create a case the morning after it reaches 90 days past due; FEAT-CHO-05 Hold case creation when the COLLINS load is late |
| Requirement IDs | REQ-DRI-013, REQ-CHO-001, REQ-CHO-005, REQ-RDF-003 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.1, 5.2 and 5.3 |
| L3 process | 6.1 Take over the case at 90 days past due |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-004, RWB-E1-007 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case created or updated from the EFS data in the COLLINS daily load, with the contact and promise history attached**, so that **the case starts the morning after the account reaches 90 days past due and I can see what happened before day 90**.

## 2. Business rationale

Accounts move from collections to recovery by a weekly transfer today, and the case starts without its collection history. This story creates the case each morning from the COLLINS load, links the account to the customer's open case for the same product, and copies the EFS contact and promise history into the interaction ledger. It holds case creation when the load is late, so no case is built from stale data. It meets REQ-CHO-001, REQ-CHO-005, REQ-DRI-013 and REQ-RDF-003 and is measured by CTL-01 and REC-01 (accounts at 90 days past due against open cases, zero unexplained).

## 3. Preconditions

- RWB-E1-004 (EFS load into the data store) and RWB-E1-007 (adapters and IdempotencyGuard) are done; the case record (RWB-E1-018) and the decision log writer (RWB-E1-027) are in production.
- Parameter `case.entry.dpd_threshold` = 90 is in force (DL16).
- The product code to product group map (LOV-PRODUCT-CODE to LOV-PRODUCT) is loaded.
- The list of EFS action codes copied at hand-over is loaded (DL29, assumed: every action code of the current collection period from the first day past due).
- JOB-01 has passed its load checks for the business date.
- SY-DATALOAD, SY-CASEWF and SY-DECLOG hold their managed identities.

## 4. Flow

1. Scheduler: JOB-02 starts after JOB-01 publishes LoadCompleted (EV-26) for sources ALS and EFS with business date D.
2. SY-DATALOAD: the HandoverService checks that both data products carry business date D; if not, it holds the run (step X3).
3. SY-DATALOAD: reads through the P1 AccountQuery every account with days_past_due at or above the threshold and no open case link on business date D.
4. SY-DATALOAD: for each account, calls IdempotencyGuard.firstTime("handover", accountId + ":" + D); a repeat is skipped and counted.
5. SY-DATALOAD: groups the accounts by primary customer and product group (DL17).
6. SY-CASEWF: for each group, CaseCreation.createOrLink writes the decision log entry first, then creates the case with status New, case number RW-YYYY-NNNNNN and entry date D+1, or links the account to the customer's open case for the product group.
7. SY-CASEWF: publishes CaseCreated (EV-01) with the business date, in the same transaction.
8. SY-DATALOAD: reads the EFS contact and promise records for the account and appends them through InteractionLedger.appendEfsHistory with source system EFS.
9. SY-DATALOAD: writes the run summary: accounts read, cases created, accounts linked, repeats, held; JOB-03 allocation follows.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same business date is loaded or run twice | No second case or link; the repeat is counted in the run summary (R-UNI-40) | None | AC2 |
| X2 | The COLLINS load has not passed by 09:00 | JOB-02 does not run; the products show stale; the data steward is alerted; cases are created on the next good load | MSG-P1-001, MSG-P2-007 | AC3, AC6 |
| X3 | The account's customer is not in the party data | The account is not taken; it is listed in the data quality exceptions and tried with the next load | None | AC5 |
| X4 | The decision log write fails | The case is not created; an incident is raised (R-UNI-39); the account is tried in the next run | MSG-P7-003 | AC7 |
| X5 | The customer already has an open case for the product group | The account is linked to that case; no new case | None | AC4 |
| X6 | JOB-02 is started again while it runs | The rerun is refused | MSG-P2-006 | AC8 |
| X7 | A role without the right reruns JOB-02 | Refused; nothing changes | MSG-P4-002 | TC-E2-001-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the EFS load (RWB-E1-004) and the adapters (RWB-E1-007); the case record and log writer are in production |
| Negotiable | Threshold, product map and copied action codes are data rows |
| Valuable | Each case starts the morning after day 90 with its collection history |
| Estimable | One service, one job step, three interface calls |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: EFS hand-over with full history from the COLLINS load

  Background:
    Given parameter "case.entry.dpd_threshold" is 90
    Given the COLLINS load for business date 2026-12-14 passed its checks at 05:20

  Scenario: AC1 Case from the load
    Given synthetic account "A-0001" for customer "C-0001", product group "MORTGAGE", reached 90 days past due in the EFS data of business date 2026-12-14
    Given the EFS data holds 14 contact records and 2 promises for the account in its collection period
    When the morning case creation runs on 2026-12-15
    Then a case exists with status "NEW", product group "MORTGAGE", entry date 2026-12-15 and days past due at entry 90
    Then the case holds 16 interaction entries with source system "EFS"
    Then the decision log entry for the creation holds business date 2026-12-14 in its inputs snapshot
    Then the system publishes caseCreated with business date 2026-12-14

  Scenario: AC2 Repeat load
    Given the run for business date 2026-12-14 created the case for "A-0001"
    When case creation runs again for business date 2026-12-14
    Then the system creates no second case and no interaction entry is added
    Then the run summary shows 1 repeat for "A-0001"

  Scenario: AC3 Late load
    Given the COLLINS load for business date 2026-12-15 has not arrived by 09:00 on 2026-12-16
    When case creation is due
    Then the system creates no case from the data of 2026-12-14
    Then the data products show message MSG-P1-001 with the date 2026-12-14
    Then the system alerts the data steward with message MSG-P2-007

  Scenario: AC4 Account linked to the open case
    Given customer "C-0002" has open case "RW-2026-000210" for product group "SSME"
    Given synthetic account "A-0002" of "C-0002", product group "SSME", reaches 90 days past due on 2026-12-14
    When case creation runs
    Then the system creates no new case
    Then the system links "A-0002" to "RW-2026-000210" with linked from 2026-12-15 and is primary false

  Scenario: AC5 Customer not in the party data
    Given synthetic account "A-0003" reaches 90 days past due and its customer is not in the party data
    When case creation runs
    Then the system creates no case for "A-0003"
    Then a data quality exception with check "References" lists "A-0003"
    Then "A-0003" is tried again with the next load

  Scenario: AC6 Cases created on the next good load
    Given no case creation ran for business date 2026-12-15
    Given the COLLINS load for business date 2026-12-16 passes at 05:15 on 2026-12-17
    When case creation runs
    Then accounts that reached 90 days past due on 2026-12-15 or 2026-12-16 get cases with entry date 2026-12-17
    Then the run summary names the gap date 2026-12-15

  Scenario: AC7 Decision log write fails
    Given the decision log store is unavailable
    When case creation runs for "A-0004"
    Then the system creates no case for "A-0004"
    Then the system raises an incident and the run summary carries message MSG-P7-003
    Then the system takes "A-0004" in the next run

  Scenario: AC8 Second start refused
    Given JOB-02 is running for business date 2026-12-14
    When a platform administrator requests a rerun of JOB-02
    Then the response is 409 with message MSG-P2-006
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case enters at 90 days past due | DL16; parameter case.entry.dpd_threshold |
| BR2 | One case per customer per product group; a further account of the same customer and product group is linked to the open case | DL17; REQ-CHO-005 |
| BR3 | Hand-over data arrives only in the COLLINS daily load | REQ-DRI-013; DT12; INT-07 |
| BR4 | No case is created from data that failed its checks or is not for the business date | JOB-02; CTL-02; FEAT-CHO-05 |
| BR5 | The EFS contact and promise history of the collection period is copied to the interaction ledger with source system EFS | DL29; LOV-SOURCE; REQ-CHO-001 |
| BR6 | A repeat hand-over for the same account and business date is ignored and counted | R-UNI-40 |
| BR7 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR8 | An account whose customer cannot be matched is held in the exception list and tried with the next load | ifspec Load checks, References; DQ-040 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No case | CaseCreated (EV-01) from JOB-02 | days_past_due at or above 90 and no open case for the customer and product group | New |
| New, Assigned, In progress or any Waiting | Account linked by JOB-02 | Open case for the customer and product group | Status unchanged |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Reads accounts and EFS records; calls case creation and the ledger (Case record, CU) |
| SY-CASEWF, case workflow module | Creates the case and the account link; publishes CaseCreated |
| SY-DECLOG, decision log writer | Writes the entry (Decision log, C) |
| RW-CASEOWN, case owner | Reads the case and its history once allocated (Case record, R) |
| RW-DATASTEW, data steward | Receives the late load alert; reads the run summary (Platform administration, R) |
| RW-PLATADM, platform administrator | Reruns JOB-02 (Platform administration, U) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-001 | loan_account | id | Read |
| DF-ACC-004 | loan_account | product_code | Read |
| DF-ACC-012 | loan_account | total_balance | Read |
| DF-ACC-014 | loan_account | days_past_due | Read |
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-PTY-001 | party | id | Read |
| DF-CAS-002 | recovery_case | case_no | Write |
| DF-CAS-003 | recovery_case | product_group | Write |
| DF-CAS-004 | recovery_case | primary_customer_id | Write |
| DF-CAS-005 | recovery_case | status | Write |
| DF-CAS-013 | recovery_case | entry_date | Write |
| DF-CAS-014 | recovery_case | dpd_at_entry | Write |
| DF-CAS-016 | recovery_case | total_outstanding_at_entry | Write |
| DF-CAS-025 | case_account | case_id | Write |
| DF-CAS-026 | case_account | account_id | Write |
| DF-CAS-027 | case_account | is_primary | Write |
| DF-CAS-028 | case_account | linked_from | Write |
| DF-INT-002 | interaction | case_id | Write |
| DF-INT-004 | interaction | occurred_at | Write |
| DF-INT-005 | interaction | channel | Write |
| DF-INT-006 | interaction | direction | Write |
| DF-INT-007 | interaction | action_code | Write |
| DF-INT-008 | interaction | contact_result | Write |
| DF-INT-009 | interaction | promise_amount | Write |
| DF-INT-010 | interaction | promise_date | Write |
| DF-INT-013 | interaction | source_system | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |
| DF-OPS-178 to DF-OPS-183 | processed_event | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job JOB-02 Case creation.** Trigger: Quartz, daily after JOB-01 publishes LoadCompleted (EV-26) for ALS and EFS with the same business date. Input: accounts at or above the threshold on business date D; EFS contact and promise records. Output: cases with status New, account links, interaction entries, decision log entries, run summary. Events published: CaseCreated (EV-01) by P3 through the outbox. Events consumed: LoadCompleted (EV-26). Idempotency key: account ID + business date. Restart: POST /admin/jobs/{jobId}/rerun; accounts already handled for D are skipped through the key.

**Endpoints used.**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| POST /admin/jobs/{jobId}/rerun | Path: jobId | Job | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-P4-003); 409 running (MSG-P2-006); 503 (MSG-P7-003) | Platform administration, U | Per account and business date |
| GET /cases/{caseId}/timeline | Query: type, from, to | TimelinePage | 401; 403; 404 out of scope (MSG-P4-003); 503 | Case record, R | Read only |

**Published interfaces called.**

```java
// P1 recovery.data.api
List<EntryCandidate> AccountQuery.findAtOrAboveDpd(int threshold, LocalDate businessDate);
List<EfsHistoryRecord> EfsHistoryQuery.forAccount(UUID accountId, LocalDate businessDate);
// P3 recovery.casewf.api
CaseRef CaseCreation.createOrLink(CaseEntryRequest request); // writes the decision log entry first; throws DecisionLogUnavailableException
// P7 recovery.decision.api
int InteractionLedger.appendEfsHistory(UUID caseId, List<EfsHistoryRecord> records);
```

**Published interface built (package recovery.integration.handover.api).**

```java
public interface HandoverRun {
    HandoverSummary run(LocalDate businessDate); // summary: read, created, linked, repeats, held, gapDates
}
```

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/handover`, Java package `recovery.integration.handover`.

| Component | Type | Responsibility |
|---|---|---|
| HandoverService | Service | Freshness check, candidate read, idempotency, grouping, calls to P3 and P7, run summary |
| HandoverJob | Job | JOB-02 step; listens for LoadCompleted and starts after JOB-01 |
| HandoverGroupBuilder | Service | Groups candidates by customer and product group with the product map |
| HandoverSummaryRepository | Repository | Writes the run summary to interface_run.checks |
| LoadCompletedListener | Listener | Consumes EV-26 through IdempotencyGuard |

- **Database:** no new table. Writes processed_event and interface_run (RWB-E1-007). Case, account link, interaction and decision log rows are written by P3 and P7 through their interfaces.
- **Configuration and reference data:** parameter case.entry.dpd_threshold = 90 (RW-COE, DL16); product code map (RW-REFADM); EFS action codes copied at hand-over (RW-DATASTEW, DL29); JOB-01 retry window to 09:00 (RWB-E1-051).
- **Build steps:**
  1. Build HandoverGroupBuilder with tests for one and two accounts per customer and product group.
  2. Build HandoverService with the freshness hold and the gap dates taken from the last good run.
  3. Wire IdempotencyGuard on account ID and business date.
  4. Call CaseCreation.createOrLink; on DecisionLogUnavailableException stop the account, count it and raise the incident.
  5. Call InteractionLedger.appendEfsHistory with the records of the collection period.
  6. Build HandoverJob and LoadCompletedListener; chain JOB-03 after it.
  7. Write the run summary and the MSG-P2-007 alert for a held run.
- **Feature flag:** `rwb.integration.efs-handover`.
- **Done when:** the tests in section 16 pass and REC-01 for SIT business date 2026-12-14 shows zero unexplained difference.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | Data product stale after a late load | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-007 | Case creation held for a late load | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | Rerun while JOB-02 runs | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the right reruns JOB-02 | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No new screen. The case owner sees the new case on SCR-02 Case list (states loading, list) and its EFS history on SCR-04 Case timeline (states loading, filtered) with source EFS. The data steward sees held runs and exceptions on SCR-45 Data quality.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-001-01 | AC1, BR1, BR3, BR5 | System | Synthetic account A-0001 with 14 contacts and 2 promises |
| TC-E2-001-02 | AC2, BR6 | System | Same business date run twice |
| TC-E2-001-03 | AC3, BR4 | System | No COLLINS load for 2026-12-15 |
| TC-E2-001-04 | AC4, BR2 | System | Customer C-0002 with an open SSME case |
| TC-E2-001-05 | AC5, BR8 | System | Account A-0003 with no party record |
| TC-E2-001-06 | AC6, BR4 | System | Good load on 2026-12-17 after a missed day |
| TC-E2-001-07 | AC7, BR7 | System | Decision log store stopped |
| TC-E2-001-08 | AC8 | System | JOB-02 running |
| TC-E2-001-09 | Access | Access | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |
| TC-E2-001-10 | Principle 5 | Resilience | Decision log write forced to fail during a run of 50 synthetic accounts; no case is created without its entry |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the threshold, the product map and the copied action codes are rows.
- No personal data in logs, tests or prompts; the run summary holds counts and synthetic keys; interaction summaries are not logged.
- No read of another module's tables; accounts, cases and the ledger are reached through their published interfaces.
- No case is built from a load that did not pass its checks.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the COLLINS daily load | Program 5.2; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | R-UNI-40 | TC-E2-001-01, TC-E2-001-02 |
| REQ-CHO-001 | Case with full contact and promise history | Program 5.3; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-01, TC-E2-001-05 |
| REQ-CHO-005 | Workbench is the system of record for case state after hand-over | Program 5.3; Epic 2 3.2 | FEAT-CHO-04 | 6.1 Take over the case at 90 days past due | R-UNI-39 | TC-E2-001-04, TC-E2-001-07, TC-E2-001-10 |
| REQ-RDF-003 | EFS history transfers to the case | Program 5.1; Epic 2 3.2 | FEAT-CHO-05 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-03, TC-E2-001-06, TC-E2-001-08 |

## 19. Out of scope

- Allocation of the new case: RWB-E1-020.
- The ACE plan status on the case: RWB-E2-002.
- The daily reconciliation of hand-overs and retirement of the manual EFS file: RWB-E2-023.
- A same-day hand-over event: DL06.
