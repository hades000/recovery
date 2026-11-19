# Recovery Workbench user stories, Epic 2

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Stories | 35 |
| Acceptance criteria | 360 |
| Test cases | 415 |
| Modules | P1 (1), P2 (10), P3 (5), P4 (1), P5 (4), P6 (3), P7 (3), P8 (2), P9 (1), P10 (5) |

Release 31 December 2026. Epic 2 status: confirmed. The 3 agent stories at the end of this file go live with Epic 3, after the foundation.

Each story is written for build: the business rationale, preconditions, the main flow and its exception paths, acceptance criteria in Gherkin, business rules, state transitions, authority, the fields it reads and writes with their BR Field IDs, the contract, the solution plan, messages, screens, test cases and traceability to the business requirements. Field IDs are those in the Logical Data Model and Data Dictionary, endpoints those in the API Specification, messages those in the Error and Message Standard and requirement IDs those in the Business Requirements. The same stories are also supplied one file per story, to hand to a coding agent with the module specifications.

| Key | Title | Module | Requirements | Depends on |
|---|---|---|---|---|
| RWB-E2-001 | EFS hand-over with full history from the COLLINS load | P2 Integration | REQ-DRI-013, REQ-CHO-001, REQ-CHO-005, REQ-RDF-003 | RWB-E1-004, RWB-E1-007 |
| RWB-E2-002 | ACE plan status on the case | P2 Integration | REQ-DRI-013, REQ-CHO-002 | RWB-E2-001 |
| RWB-E2-003 | Customer's other products on the case | P2 Integration | REQ-CHO-003, REQ-RDF-010 | RWB-E1-007 |
| RWB-E2-004 | Treatment entity and plan timers data model | P3 Case and workflow, with P1 Recovery data engine for the data product | REQ-CHO-006, REQ-CHO-007, REQ-RDF-014 | RWB-E1-018, RWB-E1-028, RWB-E1-045 |
| RWB-E2-005 | Decision log query API for audit | P7 Decision center and log | REQ-DRI-012 | RWB-E1-008, RWB-E1-039 |
| RWB-E2-006 | Credit approval pack for NLEADS | P2 Integration | REQ-CHO-008, REQ-CHO-006 | RWB-E2-004, RWB-E1-007 |
| RWB-E2-007 | Booking confirmation from the ALS load | P2 Integration, with P8 Payments and posting | REQ-CHO-008 | RWB-E2-004, RWB-E1-007 |
| RWB-E2-008 | Payment matching with the missed payment event | P8 Payments and posting | REQ-CHO-007, REQ-CHO-009 | RWB-E2-004, RWB-E1-003 |
| RWB-E2-009 | Steering dashboard v1 data set | P9 Reporting | REQ-WKM-009, REQ-WKM-006 | RWB-E1-013, RWB-E1-063 |
| RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | P1 Recovery data engine | REQ-RDF-014 | RWB-E2-004, RWB-E1-016, RWB-E1-015 |
| RWB-E2-011 | Queue view screens: my queue, team queues, filters and ageing | P3 Case and workflow | REQ-WKM-001, REQ-WKM-002, REQ-WKM-006 | RWB-E1-020, RWB-E1-031 |
| RWB-E2-012 | Manual transfer and reassignment screen with reason | P3 Case and workflow | REQ-WKM-003, REQ-WKM-007, REQ-WKM-008 | RWB-E1-021, RWB-E2-011 |
| RWB-E2-013 | Approval routing with the delegation of authority table | P7 Decision center and log | REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010, REQ-APD-011 | RWB-E1-038, RWB-E1-028, RWB-E1-027, RWB-E1-037 |
| RWB-E2-014 | Approval screen for D7.1 demand and recall notices | P7 Decision center and log, with P6 Communications | REQ-APD-002, REQ-APD-006 | RWB-E2-013, RWB-E1-052 |
| RWB-E2-015 | Timers, escalation and the deviation flag on the case record view | P3 Case and workflow | REQ-WKM-004, REQ-WKM-005, REQ-DVH-002 | RWB-E1-028, RWB-E1-035 |
| RWB-E2-016 | Full case record view with the history timeline | P3 Case and workflow, with P7 Decision center and log | REQ-WKM-008, REQ-OCC-008 | RWB-E1-035, RWB-E2-015, RWB-E2-012 |
| RWB-E2-017 | Contract, CA and mortgage document generation screens | P5 Document hub | REQ-DCM-012, REQ-OCC-002 | RWB-E2-026, RWB-E1-034, RWB-E1-054, RWB-TE-012 |
| RWB-E2-018 | E-signature flow for customers and the bank | P6 Communications | REQ-OCC-009 | RWB-E2-017, RWB-E2-022 |
| RWB-E2-019 | Partner identities through the external gateway | P4 Access and administration | REQ-ACA-012 | RWB-E1-022, RWB-E1-037, RWB-E1-039 |
| RWB-E2-021 | Letter dispatch loop with proof of delivery from WIN | P6 Communications | REQ-OCC-003, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010 | RWB-E1-052, RWB-E1-055, RWB-E2-014 |
| RWB-E2-022 | SMS and LINE dispatch through NSS and LINE OA | P6 Communications | REQ-OCC-004, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010 | RWB-E1-052, RWB-E1-066 |
| RWB-E2-023 | Automated EFS file load | P2 Integration | REQ-RDF-007, REQ-RDF-006, REQ-CHO-001 | RWB-E2-001, RWB-E1-051 |
| RWB-E2-024 | Field app photos and bills into the document hub | P5 Document hub | REQ-DCM-013 | RWB-E1-057, RWB-E1-032, RWB-E1-053, RWB-E1-024, RWB-E1-041 |
| RWB-E2-025 | Extraction for the stage 2 and 3 document types | P5 Document hub | REQ-DCM-006, REQ-DCM-005 | RWB-E1-053, RWB-E1-050, RWB-E1-054 |
| RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | P5 Document hub | REQ-DCM-012, REQ-OCC-002 | RWB-E1-046, RWB-E1-034, RWB-E1-024, RWB-E1-027 |
| RWB-E2-027 | Payment matching rules with the data team | P8 Payments and posting | REQ-CHO-009 | RWB-E2-008 |
| RWB-E2-031 | Agent monitoring dashboard v2 [E3d] | P10 Agent runtime | REQ-DRI-009, REQ-APD-005 | RWB-E1-063, RWB-E2-005 |
| RWB-E2-032 | TDR offer-suggestion model through the model gateway [E3e] | P10 Agent runtime | REQ-CHO-006, REQ-DRI-001 | RWB-E1-058, RWB-E2-004, RWB-E1-027 |
| RWB-E2-033 | Case and queue list with status, owner and ageing | P2 Integration | REQ-WKM-002, REQ-DVH-006 | RWB-E1-018, RWB-E1-031, RWB-E2-011 |
| RWB-E2-034 | Interaction ledger on the case and from every channel | P2 Integration | REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013 | RWB-E1-027, RWB-E2-016, RWB-E1-004, RWB-E1-007, RWB-E1-066, RWB-E1-067, RWB-TE-006 |
| RWB-E2-035 | Next action on the case | P2 Integration | REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014, REQ-WKM-015 | RWB-E1-018, RWB-E1-031, RWB-E2-033 |
| RWB-E2-036 | Queue write interface for models and agents | P2 Integration | REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020 | RWB-E1-019, RWB-E1-020, RWB-E1-027 |
| RWB-E2-028 | Case intake agent live at L1 [E3a] | P10 Agent runtime | REQ-DRI-001, REQ-ACA-005 | RWB-E1-061, RWB-E1-035, RWB-E1-027, RWB-E2-031 |
| RWB-E2-029 | Deviation screening agent evaluation and L1 on one segment [E3b] | P10 Agent runtime | REQ-DVH-001, REQ-DVH-006 | RWB-E1-062, RWB-E2-015, RWB-E1-061, RWB-E2-028 |
| RWB-E2-030 | Legal document agent in shadow on Epic 1 data [E3c] | P10 Agent runtime |  | RWB-E1-058, RWB-E2-025, RWB-E1-061 |

---

## RWB-E2-001 EFS hand-over with full history from the COLLINS load

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

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case created or updated from the EFS data in the COLLINS daily load, with the contact and promise history attached**, so that **the case starts the morning after the account reaches 90 days past due and I can see what happened before day 90**.

### 2. Business rationale

Accounts move from collections to recovery by a weekly transfer today, and the case starts without its collection history. This story creates the case each morning from the COLLINS load, links the account to the customer's open case for the same product, and copies the EFS contact and promise history into the interaction ledger. It holds case creation when the load is late, so no case is built from stale data. It meets REQ-CHO-001, REQ-CHO-005, REQ-DRI-013 and REQ-RDF-003 and is measured by CTL-01 and REC-01 (accounts at 90 days past due against open cases, zero unexplained).

### 3. Preconditions

- RWB-E1-004 (EFS load into the data store) and RWB-E1-007 (adapters and IdempotencyGuard) are done; the case record (RWB-E1-018) and the decision log writer (RWB-E1-027) are in production.
- Parameter `case.entry.dpd_threshold` = 90 is in force (DL16).
- The product code to product group map (LOV-PRODUCT-CODE to LOV-PRODUCT) is loaded.
- The list of EFS action codes copied at hand-over is loaded (DL29, assumed: every action code of the current collection period from the first day past due).
- JOB-01 has passed its load checks for the business date.
- SY-DATALOAD, SY-CASEWF and SY-DECLOG hold their managed identities.

### 4. Flow

1. Scheduler: JOB-02 starts after JOB-01 publishes LoadCompleted (EV-26) for sources ALS and EFS with business date D.
2. SY-DATALOAD: the HandoverService checks that both data products carry business date D; if not, it holds the run (step X3).
3. SY-DATALOAD: reads through the P1 AccountQuery every account with days_past_due at or above the threshold and no open case link on business date D.
4. SY-DATALOAD: for each account, calls IdempotencyGuard.firstTime("handover", accountId + ":" + D); a repeat is skipped and counted.
5. SY-DATALOAD: groups the accounts by primary customer and product group (DL17).
6. SY-CASEWF: for each group, CaseCreation.createOrLink writes the decision log entry first, then creates the case with status New, case number RW-YYYY-NNNNNN and entry date D+1, or links the account to the customer's open case for the product group.
7. SY-CASEWF: publishes CaseCreated (EV-01) with the business date, in the same transaction.
8. SY-DATALOAD: reads the EFS contact and promise records for the account and appends them through InteractionLedger.appendEfsHistory with source system EFS.
9. SY-DATALOAD: writes the run summary: accounts read, cases created, accounts linked, repeats, held; JOB-03 allocation follows.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same business date is loaded or run twice | No second case or link; the repeat is counted in the run summary (R-UNI-40) | None | AC2 |
| X2 | The COLLINS load has not passed by 09:00 | JOB-02 does not run; the products show stale; the data steward is alerted; cases are created on the next good load | MSG-P1-001, MSG-P2-007 | AC3, AC6 |
| X3 | The account's customer is not in the party data | The account is not taken; it is listed in the data quality exceptions and tried with the next load | None | AC5 |
| X4 | The decision log write fails | The case is not created; an incident is raised (R-UNI-39); the account is tried in the next run | MSG-P7-003 | AC7 |
| X5 | The customer already has an open case for the product group | The account is linked to that case; no new case | None | AC4 |
| X6 | JOB-02 is started again while it runs | The rerun is refused | MSG-P2-006 | AC8 |
| X7 | A role without the right reruns JOB-02 | Refused; nothing changes | MSG-P4-002 | TC-E2-001-09 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the EFS load (RWB-E1-004) and the adapters (RWB-E1-007); the case record and log writer are in production |
| Negotiable | Threshold, product map and copied action codes are data rows |
| Valuable | Each case starts the morning after day 90 with its collection history |
| Estimable | One service, one job step, three interface calls |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

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

### 8. Business rules

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

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No case | CaseCreated (EV-01) from JOB-02 | days_past_due at or above 90 and no open case for the customer and product group | New |
| New, Assigned, In progress or any Waiting | Account linked by JOB-02 | Open case for the customer and product group | Status unchanged |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Reads accounts and EFS records; calls case creation and the ledger (Case record, CU) |
| SY-CASEWF, case workflow module | Creates the case and the account link; publishes CaseCreated |
| SY-DECLOG, decision log writer | Writes the entry (Decision log, C) |
| RW-CASEOWN, case owner | Reads the case and its history once allocated (Case record, R) |
| RW-DATASTEW, data steward | Receives the late load alert; reads the run summary (Platform administration, R) |
| RW-PLATADM, platform administrator | Reruns JOB-02 (Platform administration, U) |

### 11. Data

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

### 12. Contract

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

### 13. Solution plan

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

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | Data product stale after a late load | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-007 | Case creation held for a late load | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | Rerun while JOB-02 runs | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the right reruns JOB-02 | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

No new screen. The case owner sees the new case on SCR-02 Case list (states loading, list) and its EFS history on SCR-04 Case timeline (states loading, filtered) with source EFS. The data steward sees held runs and exceptions on SCR-45 Data quality.

### 16. Test cases

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

### 17. Guardrails

- No business value in code: the threshold, the product map and the copied action codes are rows.
- No personal data in logs, tests or prompts; the run summary holds counts and synthetic keys; interaction summaries are not logged.
- No read of another module's tables; accounts, cases and the ledger are reached through their published interfaces.
- No case is built from a load that did not pass its checks.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the COLLINS daily load | Program 5.2; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | R-UNI-40 | TC-E2-001-01, TC-E2-001-02 |
| REQ-CHO-001 | Case with full contact and promise history | Program 5.3; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-01, TC-E2-001-05 |
| REQ-CHO-005 | Workbench is the system of record for case state after hand-over | Program 5.3; Epic 2 3.2 | FEAT-CHO-04 | 6.1 Take over the case at 90 days past due | R-UNI-39 | TC-E2-001-04, TC-E2-001-07, TC-E2-001-10 |
| REQ-RDF-003 | EFS history transfers to the case | Program 5.1; Epic 2 3.2 | FEAT-CHO-05 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-03, TC-E2-001-06, TC-E2-001-08 |

### 19. Out of scope

- Allocation of the new case: RWB-E1-020.
- The ACE plan status on the case: RWB-E2-002.
- The daily reconciliation of hand-overs and retirement of the manual EFS file: RWB-E2-023.
- A same-day hand-over event: DL06.


---

## RWB-E2-002 ACE plan status on the case

| Item | Value |
|---|---|
| Story key | RWB-E2-002 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CHO-02 Read the ACE plan status |
| Requirement IDs | REQ-DRI-013, REQ-CHO-002 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.2 and 5.3 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D5 |
| Priority | Must |
| Depends on | RWB-E2-001 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the restructure plan status from the ACE common module (created, approved, booked, broken) on the case**, so that **a case with a live plan is never treated as if it had none, and a broken plan returns the case to me the next morning**.

### 2. Business rationale

Restructure plans are calculated and held in ACE (DL14). Without the plan status on the case, a recovery officer can start litigation on a customer who is paying a plan, or miss a plan that broke. This story reads the status from the ACE common module each morning and on each case view, keeps the last known status with its date when ACE returns none, and raises the broken plan to the restructure rules. It meets REQ-CHO-002 and REQ-DRI-013.

### 3. Preconditions

- RWB-E2-001 (case creation from the COLLINS load) is done.
- The ACE common module publishes RestructurePlanQuery in SIT and UAT (INT-34; DL14).
- The account number is the join key between the case and the ACE plan (DL21).
- The plan event map rows are loaded: ACE status BROKEN with route state PLAN_CURE_PERIOD maps to event CURE_PERIOD_EXPIRED; BROKEN with any other route state maps to TREATMENT_BROKEN.
- Parameter `restructure.max_breaks` = 2 is in force (Restructure route set: a second break bars a further restructure).
- The restructure rules R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are in force.

### 4. Flow

1. Scheduler: the plan status step runs in JOB-02 after the case creation step, once a day.
2. SY-DATALOAD: the PlanStatusService lists every open case with its account numbers through the P3 CaseQuery.
3. SY-DATALOAD: calls RestructurePlanQuery.statusFor with the account numbers in batches of 500 (assumed; DL11).
4. SY-DATALOAD: for each plan returned, compares status and status date with the stored values; an unchanged plan is skipped.
5. SY-CASEWF: writes plan_ref, plan_status and plan_status_as_of on the case through CasePlanStatus.update.
6. SY-DATALOAD: on a change to BROKEN, looks up the event in the plan event map and calls CaseEvents.raise with plan_status = broken and the break count.
7. SY-RULES and SY-CASEWF: evaluate the rule for the case's route state, write the decision log entry, move the route state and place the case in the case owner's queue with a task.
8. Case owner: opens the case record view; the front end calls GET /cases/{caseId}/plan-status, which reads ACE live with a 2-second timeout and falls back to the stored status.
9. SY-DATALOAD: for a case with a stored plan that ACE no longer returns, keeps the stored status and date and writes a data quality exception for the ACE team.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | ACE returns no status for a plan the case holds | The case keeps its last known status and date; a data quality exception lists the plan for the ACE team | MSG-P2-008 | AC3 |
| X2 | The ACE common module is unavailable or does not answer in 2 seconds | The daily step keeps every stored status and retries in the next run; the view shows the stored status | MSG-GEN-006, MSG-P2-008 | AC4 |
| X3 | ACE returns a status code not in the plan status list | The status is not stored; a data quality exception with check "Lists of values" is written | None | AC5 |
| X4 | The daily step runs twice for the same day | No status is written twice and no event is raised twice | None | AC6 |
| X5 | The decision log write fails during the broken plan move | The route state does not move; an incident is raised; the event is raised again in the next run | MSG-P7-003 | AC7 |
| X6 | A user reads the plan status of a case outside their scope | Refused | MSG-P4-003 | AC8 |
| X7 | A role without the Case record right reads the plan status | Refused; nothing changes | MSG-P4-002 | TC-E2-002-09 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the cases from RWB-E2-001 and the ACE interface |
| Negotiable | The event map, batch size, timeout and maximum breaks are data rows or properties |
| Valuable | No action is taken on a case with a live plan without the plan in view |
| Estimable | One service, one job step, one endpoint, one map table |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

```gherkin
Feature: ACE plan status on the case

  Background:
    Given case "RW-2026-000310" is open with synthetic account "A-0310"
    Given the ACE common module stub holds plan "TDR-SYN-0310" for "A-0310"

  Scenario: AC1 Plan status on the case
    Given plan "TDR-SYN-0310" has status "APPROVED" in ACE with status date 2026-12-10
    When the case record view loads on 2026-12-11
    Then the case shows plan "TDR-SYN-0310" with status "Approved" and date 2026-12-10
    Then the rules component reads plan_status "APPROVED" for the case
    Then rule R-LIT-02 does not fire for the case because plan_status is not broken

  Scenario: AC2 Broken plan
    Given the case is in route state "PLAN_CURE_PERIOD" with break count 0
    Given plan "TDR-SYN-0310" has status "BROKEN" in ACE with status date 2026-12-14
    When the daily case update runs on 2026-12-15
    Then the case plan status is "BROKEN" with date 2026-12-14
    Then the route state moves to "PLAN_BROKEN" by R-RES-29 and then to "BACK_TO_ROUTE_DECISION" by R-RES-30
    Then the case is in the case owner's queue with a task due in 5 working days
    Then the system writes a decision log entry for each move with the rule ID and version

  Scenario: AC3 Status not available
    Given the case holds plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01
    Given ACE returns no status for "TDR-SYN-0310"
    When the daily case update runs on 2026-12-15
    Then the case keeps status "BOOKED" with date 2026-12-01
    Then the case record view shows message MSG-P2-008 with the date 2026-12-01
    Then a data quality exception with product "DP04" lists plan "TDR-SYN-0310" for the ACE team

  Scenario: AC4 ACE unavailable
    Given the ACE common module does not answer within 2 seconds
    When the daily case update runs on 2026-12-16
    Then the system changes no plan status
    Then the run summary carries message MSG-GEN-006 with system "ACE common module"
    Then the next run retries every case

  Scenario: AC5 Unknown status code
    Given ACE returns status "SUSPENDED" for plan "TDR-SYN-0310"
    When the daily case update runs
    Then the stored status does not change
    Then a data quality exception with check "Lists of values" names the code "SUSPENDED"

  Scenario: AC6 Daily step run twice
    Given the daily case update on 2026-12-15 stored status "BROKEN" for plan "TDR-SYN-0310"
    When the step is rerun on 2026-12-15
    Then the system writes no status row
    Then the system raises no second CURE_PERIOD_EXPIRED event for the case

  Scenario: AC7 Decision log write fails on a broken plan
    Given the decision log store is unavailable
    When the daily case update finds plan "TDR-SYN-0310" broken
    Then the route state stays "PLAN_CURE_PERIOD"
    Then the system raises an incident with message MSG-P7-003
    Then the system raises the event again in the next run

  Scenario: AC8 Case outside the scope
    Given a case owner whose scope is "Own" and case "RW-2026-000310" is owned by another person
    When the case owner calls GET /cases/{caseId}/plan-status for it
    Then the response is 404 with message MSG-P4-003
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The plan status is read from the ACE common module through its published interface, never from ACE tables | INT-34; DL14; ADR-002 |
| BR2 | The account number is the join between the case and the ACE plan | DL21 |
| BR3 | Plan status values: CREATED, APPROVED, BOOKED, BROKEN; any other code is held as an exception | Story intent; ifspec Load checks, Lists of values |
| BR4 | A plan marked broken while the case is in the cure period marks the plan broken and records the break | R-RES-29, R-RES-30 |
| BR5 | A second break bars a further restructure | R-RES-31; parameter restructure.max_breaks |
| BR6 | A case on the litigation route with a broken plan returns to the legal route | R-LIT-02 |
| BR7 | When ACE returns no status, the last known status and its date stay on the case | FEAT-CHO-02; VR-P2-001-1 |
| BR8 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |
| BR9 | A repeat of the same status and date raises no event | R-UNI-40 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_CURE_PERIOD | CURE_PERIOD_EXPIRED | ACE plan status BROKEN | PLAN_BROKEN |
| PLAN_BROKEN | BREAK_RECORDED | break_count < max_breaks | BACK_TO_ROUTE_DECISION |
| PLAN_BROKEN | BREAK_RECORDED | break_count >= max_breaks | RESTRUCTURE_BARRED |
| LIT_ROUTE_APPROVED | TREATMENT_BROKEN | plan_status = broken and prior_route in (R1, R2) | NOTICE_GENERATED |

These are route states (recovery_case.route_state); the case status stays "In progress". The story also writes the stored plan status.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Calls the ACE interface and writes the stored plan status through P3 |
| SY-RULES, rules component | Evaluates R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 |
| SY-CASEWF, case workflow module | Moves the route state, places the case in the queue, raises the task |
| SY-DECLOG, decision log writer | Writes each entry (Decision log, C) |
| RW-CASEOWN, case owner | Reads the plan status on cases in scope (Case record, R) |
| RW-RESTRUCT, restructuring officer | Reads the plan status on cases in scope (Case record, R) |
| RW-DATASTEW, RW-PLATADM | Read the data quality exceptions for the ACE team (Platform administration, R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-007 | recovery_case | route_state | Write, through the P3 interface |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Write, through the P3 interface |
| DF-CAS-046 | recovery_case | plan_ref | Write |
| DF-CAS-047 | recovery_case | plan_status | Write |
| DF-CAS-048 | recovery_case | plan_status_as_of | Write |
| DF-CAS-026 | case_account | account_id | Read |
| DF-ACC-002 | loan_account | account_no | Read |
| DF-WRK-018 | task | case_id | Write, through the P3 interface |
| DF-WRK-019 | task | task_code | Write, through the P3 interface |
| DF-WRK-024 | task | due_at | Write, through the P3 interface |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Job step: plan status in JOB-02 Case creation.** Trigger: after the case creation step of JOB-02, daily. Input: open cases and their account numbers; ACE plan statuses. Output: stored plan status per case; rule events for broken plans; data quality exceptions. Events published: CaseStateChanged (EV-05) by P3 for each route move. Idempotency key: case ID + plan reference + status + status date. Restart: a rerun skips every case whose stored status and date equal the ACE values.

**Endpoint (new, recorded in additions).**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /cases/{caseId}/plan-status | Path: caseId | PlanStatus: planRef, status, statusDate, live (true when read from ACE now), messageCode | 401 (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 not found or out of scope (MSG-P4-003) | Case record, R | Read only; writes nothing |

**Published interfaces called.**

```java
// ACE common module
List<PlanStatusView> RestructurePlanQuery.statusFor(List<String> accountNos); // planRef, accountNo, status, statusDate
// P3 recovery.casewf.api
void CasePlanStatus.update(UUID caseId, String planRef, String status, LocalDate statusDate);
void CaseEvents.raise(UUID caseId, String eventCode, Map<String, Object> facts); // throws DecisionLogUnavailableException
```

### 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/aceplan`, Java package `recovery.integration.aceplan`; front end `src/modules/recovery/case/PlanStatusPanel.tsx`.

| Component | Type | Responsibility |
|---|---|---|
| PlanStatusController | Controller | GET /cases/{caseId}/plan-status with the scope check |
| PlanStatusService | Service | Daily compare and write; event lookup; exceptions; live read with timeout and fallback |
| AcePlanClient | Service | Wraps RestructurePlanQuery with batching and the 2-second timeout |
| PlanEventMap | Rule table | Rows: ACE status, route state, rule event; versioned reference data |
| PlanStatusStep | Job | Step of JOB-02 |
| PlanStatusPanel | React component | Shows plan, status, date and MSG-P2-008 when not live |

- **Database:** the three new recovery_case columns plan_ref varchar(30), plan_status varchar(10), plan_status_as_of date are added by P3 in its migration for this story; no P2 table.
- **Configuration and reference data:** plan event map rows (RW-COE); new list LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED, BROKEN (RW-COE); parameter restructure.max_breaks = 2; properties `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 (assumed; DL11).
- **Build steps:**
  1. Build AcePlanClient against a stub of RestructurePlanQuery with batching and the timeout.
  2. Build PlanStatusService compare and write with the idempotency key.
  3. Build the event lookup with PlanEventMap and the CaseEvents.raise call; handle DecisionLogUnavailableException.
  4. Build the exception writes for no status and unknown codes.
  5. Build PlanStatusStep in JOB-02.
  6. Build the endpoint with live read and fallback, and PlanStatusPanel.
- **Feature flag:** `rwb.integration.ace-plan-status`.
- **Done when:** the tests in section 16 pass and the SIT run against the ACE stub moves a broken plan case to the case owner's queue.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-008 | Plan status shown from the stored value | The ACE plan status is from {date}. Today's status was not returned. |
| MSG-GEN-006 | ACE common module unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | Decision log write failed on a broken plan | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-03 Case record, states loading and read only: the plan status panel shows the plan reference, status, date and, when not live, MSG-P2-008. SCR-14 Treatment record, state broken, shows the broken plan once the case returns to the route decision.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-002-01 | AC1, BR1, BR2, BR6 | System | ACE stub plan TDR-SYN-0310 APPROVED |
| TC-E2-002-02 | AC2, BR4, BR5 | System | Case in PLAN_CURE_PERIOD; ACE plan BROKEN |
| TC-E2-002-03 | AC3, BR7 | System | ACE stub returns no plan |
| TC-E2-002-04 | AC4 | Resilience | ACE stub delayed 3 seconds |
| TC-E2-002-05 | AC5, BR3 | System | ACE stub returns SUSPENDED |
| TC-E2-002-06 | AC6, BR9 | System | Step run twice on 2026-12-15 |
| TC-E2-002-07 | AC7, BR8 | System | Decision log store stopped |
| TC-E2-002-08 | AC8 | System | Case owner with scope Own and a case of another owner |
| TC-E2-002-09 | Access | Access | RW-REFADM (no Case record right) calls GET /cases/{caseId}/plan-status; refused with MSG-P4-002 |
| TC-E2-002-10 | Principle 5 | Resilience | Decision log write forced to fail on the R-RES-29 move; route state unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: status codes, the event map, maximum breaks, batch size and timeout are rows or properties.
- No personal data in logs, tests or prompts; logs hold case IDs and plan references, never account numbers.
- No read of another module's tables or of ACE tables; ACE is reached only through RestructurePlanQuery.
- A read of the plan status writes nothing.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module | Program 5.2; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39, R-UNI-40 | TC-E2-002-01, TC-E2-002-04, TC-E2-002-06, TC-E2-002-07 |
| REQ-CHO-002 | Plan status change visible on the case | Program 5.3; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-29, R-RES-30, R-RES-31, R-LIT-02 | TC-E2-002-02, TC-E2-002-03, TC-E2-002-05, TC-E2-002-08 |

### 19. Out of scope

- Creating or changing a plan: ACE, under DL14.
- The treatment record and plan timers: RWB-E2-004.
- Booking confirmation of the plan: RWB-E2-007.
- The full restructure route in the Workbench: Epic 3.


---

## RWB-E2-003 Customer's other products on the case

| Item | Value |
|---|---|
| Story key | RWB-E2-003 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CHO-03 Read customer facts from the COLLINS batch |
| Requirement IDs | REQ-CHO-003, REQ-RDF-010 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.1 and 5.3 |
| L3 process | 06 Take over and own the case |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-007 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the customer's other products and their status on the case, from the customer profile ACE receives through COLLINS**, so that **I can see the whole relationship before I decide a route**.

### 2. Business rationale

A case owner deciding a route today looks up the customer's other loans and deposits in other systems. The customer profile already reaches ACE through COLLINS from UDP, SCBPDM and the core bank batch (DL20). This story shows the other products of each borrower on the case with their status and business date, marks them stale when the profile load is late and masks account numbers by role. It meets REQ-CHO-003 and REQ-RDF-010.

### 3. Preconditions

- RWB-E1-007 (adapters) is done; the case record view (SCR-03) is in production from Epic 1.
- The COLLINS customer profile (INT-04 SCBPDM and INT-05 UDP) carries the product block for each customer in SIT (DL20).
- P1 loads the product block into party_product through JOB-01, with business date in data_as_of.
- The masking rules for party_product.account_no are loaded (DL26; assumed: unmasked for RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL and RW-GUARANT, masked to the last four digits for every other role).
- The new list LOV-PRODUCT-STATUS is loaded (recorded in additions; assumed values: ACTIVE, DELINQUENT, CLOSED, WRITTEN_OFF).
- The ACE PII logging service is available.

### 4. Flow

1. Case owner: opens SCR-03 Case record for a case in scope.
2. Front end: calls GET /cases/{caseId}/customer-products.
3. System: checks the Case record right and the scope of the case.
4. System: reads the borrower and co-borrower parties of the case through the P3 CaseQuery.
5. System: reads each party's products through the P1 CustomerProfileQuery, excluding accounts already linked to the case.
6. System: compares data_as_of with the expected business date of DP02; if older, sets the stale marker.
7. System: applies the masking rule for the caller's role to each account number.
8. System: writes one PII access event (user, case, party IDs, fields shown) through the ACE PII logging service.
9. Front end: shows each product with product type, masked or clear account number, status and business date; a stale list shows MSG-P1-001.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The customer profile load is late | The last loaded products show with a stale marker; a stale read is logged | MSG-P1-001 | AC2 |
| X2 | The caller's role is not allowed to see account numbers | Account numbers are masked to the last four digits | None | AC3 |
| X3 | The customer holds no other product | An empty list shows | MSG-P2-017 | AC4 |
| X4 | The case is outside the caller's scope | Refused | MSG-P4-003 | AC5 |
| X5 | The PII access log cannot be written | The products are not returned; the request fails | MSG-GEN-006 | AC6 |
| X6 | A role without the Case record right calls the endpoint | Refused; nothing is shown | MSG-P4-002 | TC-E2-003-07 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the adapters and the P1 product load; no other Epic 2 story |
| Negotiable | Masking, product status codes and the parties shown are data rows |
| Valuable | The case owner sees the relationship without a lookup in another system |
| Estimable | One read service, one endpoint, one React panel, one P1 table |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

```gherkin
Feature: Customer's other products on the case

  Background:
    Given case "RW-2026-000410" has borrower "C-0410" and linked synthetic account "A-0410"
    Given the expected business date of the customer profile is 2026-12-14

  Scenario: AC1 Other products shown
    Given "C-0410" holds a revolving credit line "A-0411" with status "ACTIVE" and a personal loan "A-0412" with status "DELINQUENT", both with data as of 2026-12-14
    When the case record view loads for a case owner
    Then the other products panel shows 2 products with their type and status
    Then each product shows the business date 2026-12-14
    Then the system does not list account "A-0410" because it is on the case

  Scenario: AC2 Load late
    Given the customer profile load for 2026-12-14 has not arrived and the last load is for 2026-12-13
    When the view loads
    Then the 2 products show with data as of 2026-12-13
    Then the panel shows message MSG-P1-001 with product "Customer profile" and date 2026-12-13
    Then the system logs a stale read event with the case ID and the data product "DP02"

  Scenario: AC3 Masking
    Given a phone collector (RW-PHONECOL) with the case in scope
    Given product "A-0411" has synthetic account number "9900015678"
    When the view loads
    Then the other products show with the account number "XXXXXX5678"
    Then a case owner sees "9900015678"

  Scenario: AC4 No other products
    Given borrower "C-0420" of case "RW-2026-000420" holds no product other than the case account
    When the view loads
    Then the panel shows an empty list with message MSG-P2-017

  Scenario: AC5 Case outside the scope
    Given a case owner with scope "Own" and case "RW-2026-000410" owned by another person
    When the case owner calls GET /cases/{caseId}/customer-products
    Then the response is 404 with message MSG-P4-003

  Scenario: AC6 PII access log unavailable
    Given the ACE PII logging service does not accept the access event
    When the view loads
    Then the system returns no product
    Then the response is 503 with message MSG-GEN-006
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Customer facts come from the customer profile ACE receives through COLLINS from UDP, SCBPDM and the core bank batch | DL20; INT-04; INT-05 |
| BR2 | Products of every party with role borrower or co-borrower on the case are shown, except accounts already on the case | LOV-PARTY-ROLE; story intent |
| BR3 | Each product shows the business date of its load; a load older than the expected business date shows as stale | REQ-RDF-009; VR-P2-001-1 |
| BR4 | Account numbers are masked by role on the masking rules | REQ-RDF-010; CTL-11; DL26 |
| BR5 | Every read of customer data is logged to the PII log with who, what, when and which record | INT-22; REQ-RDF-010 |
| BR6 | Product status codes are those in LOV-PRODUCT-STATUS; an unknown code is held by the P1 load check | DQ-020, DQ-027 Lists of values |

### 9. State transitions

None. This story does not change a case status. It reads only; the PII access log receives one event per read.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads other products on cases in scope, account numbers clear (Case record, R) |
| RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Read other products on cases in scope, account numbers clear (assumed; DL26) |
| RW-PHONECOL, RW-CONDUCT and other roles with Case record R | Read other products on cases in scope, account numbers masked |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rule rows |
| SY-DATALOAD, data load | Loads the product block (P1) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-004 | recovery_case | primary_customer_id | Read |
| DF-CAS-031 | case_party | case_id | Read |
| DF-CAS-032 | case_party | party_id | Read |
| DF-CAS-033 | case_party | party_role | Read |
| DF-CAS-026 | case_account | account_id | Read |
| DF-PTY-001 | party | id | Read |
| DF-PTY-023 | party_product | party_id | Read |
| DF-PTY-024 | party_product | product_type | Read |
| DF-PTY-025 | party_product | account_no | Read |
| DF-PTY-026 | party_product | product_status | Read |
| DF-PTY-027 | party_product | data_as_of | Read |
| DF-REF-035 | role | role_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Endpoint (new, recorded in additions).**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /cases/{caseId}/customer-products | Path: caseId | CustomerProducts: dataAsOf, stale, messageCode, items (partyId, partyRole, productType, accountNo masked by role, productStatus, dataAsOf) | 401 (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 PII log unavailable (MSG-GEN-006) | Case record, R | Read only |

**Published interfaces called.**

```java
// P1 recovery.data.api
List<PartyProductView> CustomerProfileQuery.otherProducts(List<UUID> partyIds, Set<UUID> excludeAccountIds);
DataProductFreshness DataProductStatus.freshness(String dataProduct); // dataAsOf, expectedBusinessDate, stale
// P3 recovery.casewf.api
List<CasePartyView> CaseQuery.partiesOf(UUID caseId, Set<String> partyRoles);
// ACE common module
void PiiAccessLog.write(PiiAccessEvent event); // throws PiiLogUnavailableException
String Masking.apply(String field, String value, Set<String> roleCodes);
```

### 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/customer`, Java package `recovery.integration.customer`; front end `src/modules/recovery/case/OtherProductsPanel.tsx`.

| Component | Type | Responsibility |
|---|---|---|
| CustomerProductsController | Controller | GET /cases/{caseId}/customer-products with the scope check |
| CustomerProductsService | Service | Parties, products, freshness, masking, PII log, response |
| OtherProductsPanel | React component | List with product type, account number, status, date; stale banner MSG-P1-001; empty state MSG-P2-017 |

- **Database:** party_product (id, party_id, product_type, account_no, product_status, data_as_of, standard columns) is a P1 table in DP02, created in the P1 migration for this story, with an index on party_id. P2 reads it only through CustomerProfileQuery.
- **Configuration and reference data:** masking rule rows for party_product.account_no (RW-COMPLY, DL26); LOV-PRODUCT-STATUS (RW-DATASTEW); party roles shown, BORROWER and CO_BORROWER, as a property `rwb.customer.products.party-roles`.
- **Build steps:**
  1. Agree the PartyProductView and the P1 query with the P1 squad; build a stub for tests.
  2. Build CustomerProductsService with party selection and exclusion of case accounts.
  3. Add the freshness check and the stale marker.
  4. Add masking through the ACE Masking service and the PII access event; fail the call when the log fails.
  5. Build the endpoint with the access and scope checks.
  6. Build OtherProductsPanel with its loading, list, stale and empty states.
- **Feature flag:** `rwb.integration.customer-products`.
- **Done when:** the tests in section 16 pass and the panel shows synthetic products in SIT with masking for RW-PHONECOL.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | Customer profile load late | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-017 | No other product held | The customer holds no other product with the bank in the customer profile of {date}. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | PII access log unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-03 Case record, states loading and read only: the other products panel shows the list, a stale banner when the profile is late, and an empty state when there is none. A role with masking sees account numbers masked to the last four digits.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-003-01 | AC1, BR1, BR2, BR3 | System | Synthetic customer C-0410 with two other products |
| TC-E2-003-02 | AC2, BR3 | System | Customer profile last loaded 2026-12-13 |
| TC-E2-003-03 | AC3, BR4 | System | RW-PHONECOL and RW-CASEOWN read the same case |
| TC-E2-003-04 | AC4 | System | Customer C-0420 with no other product |
| TC-E2-003-05 | AC5 | System | Case owner with scope Own and a case of another owner |
| TC-E2-003-06 | AC6, BR5 | Resilience | PII logging stub refuses the event |
| TC-E2-003-07 | Access | Access | RW-REFADM (no Case record right) calls GET /cases/{caseId}/customer-products; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: masking, product status codes and the party roles shown are rows or properties.
- No personal data in logs, tests or prompts; test data is synthetic, application logs hold case and party IDs only.
- No read of another module's tables; party_product is read only through the P1 interface.
- No customer data is returned without its PII access event.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-003 | Customer and product facts from the COLLINS customer profile | Program 5.3; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | None | TC-E2-003-01, TC-E2-003-02, TC-E2-003-04, TC-E2-003-05 |
| REQ-RDF-010 | Access by role and masking under PDPA | Program 5.1; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | None | TC-E2-003-03, TC-E2-003-06 |

### 19. Out of scope

- Merging a duplicate case for the same customer and product (R-UNI-17, REQ-CHO-010): Epic 3 backlog.
- The role to masking rule table: RWB-E1-037.
- Balances of the other products: not in the customer profile today (DL20).


---

## RWB-E2-004 Treatment entity and plan timers data model

| Item | Value |
|---|---|
| Story key | RWB-E2-004 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow, with P1 Recovery data engine for the data product |
| Feature | FEAT-CHO-06 Hold the treatment entity and plan timers |
| Requirement IDs | REQ-CHO-006, REQ-CHO-007, REQ-RDF-014 |
| BRD section | Business Requirements Epic 2, sections 3.3 and 4; Business Requirements Program, sections 5.1 and 5.3 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D5, D6.4 |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-028, RWB-E1-045 |
| Status | Ready for build |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the treatment record (TDR, settlement, deed in lieu: terms, approval, booking, outcome) and its plan timers held in the Workbench, with the treatment data product for reporting**, so that **TDR and deed in lieu run inside the Workbench from Epic 2 and every plan has a record and a clock**.

### 2. Business rationale

Today a restructure plan is agreed in ACE and NLEADS, and nothing in recovery holds its terms or watches its payment dates, so a missed installment is found late. About 3,000 restructure accounts a month reach the restructure process (NFR-005) and deed in lieu is planned at 1,000 cases a month in 2027 (NFR-006). This story creates the treatment record with its terms and approval, starts the installment timer from the first due date and starts the cure period when a payment is missed. It meets REQ-CHO-006, REQ-CHO-007 and REQ-RDF-014. The measure is that every approved plan has one treatment row and a running installment timer the day it is recorded.

### 3. Preconditions

- RWB-E1-018 is done: the case record exists with its route state.
- RWB-E1-028 is done: the timer engine and JOB-05 Timer check run.
- RWB-E1-045 is done: CURE_PERIOD_DAYS and `plan.warn-days` are product parameters in force (values per DL22; `plan.warn-days` assumed 3).
- The decision log writer of RWB-E1-027 is available through the P7 published interface.
- LOV-TIMER carries the value INSTALLMENT_DUE (new list value, see Additions), loaded by the reference data administrator.
- The approval of the plan is already written to the decision log by its approver's flow (P7), so a decision log entry ID exists.
- The caller of `TreatmentRecords.recordApproved(...)` is the ACE plan status reader (RWB-E2-002) under SY-CASEWF, or a test harness in SIT.

### 4. Flow

1. ACE plan status reader (SY-CASEWF): calls `TreatmentRecords.recordApproved(...)` with the case ID, treatment type, terms, approval level, the approval's decision log entry ID and the first due date.
2. Treatment service: checks the case exists and is open through the P3 case interface, and that the decision log entry exists and names an approver through the P7 interface.
3. Treatment service: checks the required fields and the list values; writes one `treatment` row and the TreatmentApproved event (EV-10) in the outbox, in one transaction.
4. Plan timer listener (P3): consumes TreatmentApproved; finds the case in route state BOOKED_IN_ALS_NLEADS and the terms carrying a first due date (event SCHEDULE_SET).
5. Rules component: evaluates R-RES-25 and returns the action "start the plan timers" and the to state PLAN_RUNNING with the rule version.
6. Plan timer listener: writes the decision log entry with rule R-RES-25 and its version; only after that succeeds writes the INSTALLMENT_DUE timer and sets the route state to PLAN_RUNNING, and publishes CaseStateChanged (EV-05).
7. JOB-05 Timer check: at the timer's expiry publishes TimerDue (EV-18) with the timer type and the treatment ID, and sets the timer status to EXPIRED.
8. Payment matching (P8, JOB-07): publishes PaymentMissed (EV-12) when no payment matched the installment.
9. Plan timer listener: consumes PaymentMissed; applies R-RES-27; writes the decision log entry, then the CURE_PERIOD timer from CURE_PERIOD_DAYS for the product, and sets the route state to PLAN_CURE_PERIOD.
10. JOB-15 Reporting extract: each night reads changed treatments through `TreatmentRecords.changedSince(...)` and writes the treatment data product (DP04) with each treatment's status.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is missing (type, approval level, decision log entry, first due date for a restructure) | The record is refused; nothing is written | MSG-GEN-001 | AC4 |
| X2 | The decision log entry does not exist or has no approver | The record is refused | MSG-GEN-001 | AC5 |
| X3 | The first due date is before the proposed date | The record is refused | MSG-GEN-003 | AC6 |
| X4 | The case is not in route state BOOKED_IN_ALS_NLEADS when the event arrives | No timer; the case goes to the exception queue with the gap | MSG-P3-005 | AC7 |
| X5 | The same TreatmentApproved event arrives twice | The second is ignored and counted; one timer only | None | AC8 |
| X6 | The decision log write fails when the timer would start | No timer and no state change; the event is retried, then sent to the exception queue | MSG-P7-003 | AC9 |
| X7 | The nightly extract fails | The data product keeps the previous date and shows it as stale | MSG-P1-001 | AC10 |
| X8 | The case is closed | The record is refused | MSG-P3-005 | AC11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the case record, the timer engine and the product parameters, all in Epic 1 |
| Negotiable | Timer lengths and warning days are product parameters; the story fixes the record and the timer behavior |
| Valuable | Every approved plan has a record, a due date and a cure period that starts by rule |
| Estimable | One table, one service, one listener, one extract step |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion is one test against a PostgreSQL test container with a controlled clock |

### 7. Acceptance criteria

```gherkin
Feature: Treatment entity and plan timers data model

  Background:
    Given the business date is 2026-12-01
    Given case "RW-2026-000201" with product group "MORTGAGE", status "IN_PROGRESS" and route state "BOOKED_IN_ALS_NLEADS"
    Given decision log entry "DLE-9001" records the approval of a restructure at level "L4" by user "U-APR-01"
    Given CURE_PERIOD_DAYS for "MORTGAGE" is 30 calendar days and plan.warn-days is 3

  Scenario: AC1 Treatment created
    Given a TDR plan approved for "RW-2026-000201" with 36 installments, offer amount 850000.00 baht, approval level "L4" and decision log entry "DLE-9001"
    When the record is written
    Then one treatment exists with type "RESTRUCTURE", installments 36, offer amount 850000.00, approval level "L4", decision log entry "DLE-9001" and the case link
    Then booked at is empty until the booking is confirmed
    Then one TreatmentApproved event is in the outbox with the treatment ID and the case ID

  Scenario: AC2 Timer set
    Given a plan with the first payment due on 2026-12-31
    When the record is written and the plan timer listener processes TreatmentApproved
    Then one decision log entry with rule "R-RES-25" and its version is written first
    Then one "INSTALLMENT_DUE" timer exists with expires at 2026-12-31 23:59 Asia/Bangkok, warn at 2026-12-28 and status "RUNNING"
    Then the case route state is "PLAN_RUNNING" and its status stays "IN_PROGRESS"
    When the clock passes 2026-12-31 23:59 and the timer check runs
    Then the system publishes a TimerDue event with timer type "INSTALLMENT_DUE" and the treatment ID
    Then the timer status is "EXPIRED"

  Scenario: AC3 Data product
    Given ten treatments recorded on 2026-12-01 across "MORTGAGE", "HIRE_PURCHASE" and "SSME"
    Given two of them have a booked at date
    When the reporting extract runs at 01:30 on 2026-12-02
    Then the treatment data product holds ten rows for business date 2026-12-01
    Then eight show status "APPROVED" and two show status "BOOKED"

  Scenario: AC4 Required field missing
    Given a restructure plan for "RW-2026-000201" with no first due date
    When the record is written
    Then the system refuses it with MSG-GEN-001 naming "first due date"
    Then no treatment and no event are written

  Scenario: AC5 Approval not in the decision log
    Given a plan that names decision log entry "DLE-0000" which does not exist
    When the record is written
    Then the system refuses it with MSG-GEN-001 naming "decision log entry"

  Scenario: AC6 First due date before the proposal
    Given a plan proposed on 2026-12-01 with the first due date 2026-11-30
    When the record is written
    Then the system refuses it with MSG-GEN-003 naming "first due date" and "proposed at"

  Scenario: AC7 Case not in the booked state
    Given case "RW-2026-000202" in route state "WITH_FCR_OFFICER"
    When a TreatmentApproved event with a first due date arrives for it
    Then the system writes no timer
    Then the system places the case in the exception queue with MSG-P3-005 naming "PLAN_RUNNING" and "WITH_FCR_OFFICER"

  Scenario: AC8 Event delivered twice
    Given the TreatmentApproved event for the AC1 treatment was processed
    When the same event with the same event ID arrives again
    Then no second timer and no second decision log entry are written
    Then the system counts the repeat as an idempotency hit

  Scenario: AC9 Decision log write fails
    Given the decision log store is unavailable
    When the plan timer listener processes TreatmentApproved for "RW-2026-000201"
    Then the system writes no timer and the route state stays "BOOKED_IN_ALS_NLEADS"
    Then the system retries the event 3 times and then placed in the exception queue with an incident and MSG-P7-003

  Scenario: AC10 Extract fails
    Given the reporting extract of 2026-12-02 fails
    When a reporting and BI analyst reads the treatment data product
    Then it shows business date 2026-12-01 with MSG-P1-001

  Scenario: AC11 Case closed
    Given case "RW-2026-000203" with status "CLOSED"
    When a plan is recorded for it
    Then the system refuses it with MSG-P3-005

  Scenario: AC12 Payment missed starts the cure period
    Given the AC2 timer expired on 2026-12-31
    When a PaymentMissed event arrives for the treatment with due date 2026-12-31 on business date 2027-01-01
    Then the system writes a decision log entry with rule "R-RES-27" first
    Then one "CURE_PERIOD" timer exists with expires at 2027-01-31
    Then the case route state is "PLAN_CURE_PERIOD"
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every offer approved for a customer has one treatment row with its type, terms, approval level, the approval's decision log entry and its outcome | REQ-CHO-006; LOV-TREATMENT |
| BR2 | A restructure needs installments above 0 and a first due date on or after the proposed date | R-RES-25 (condition first_due_date set) |
| BR3 | The plan timers start when the schedule is set on a booked plan, and the case moves to PLAN_RUNNING | R-RES-25 |
| BR4 | When a due date passes with no payment matched, the cure period starts with CURE_PERIOD_DAYS from reference data | R-RES-27; RWB-E1-045 |
| BR5 | The warning is raised `plan.warn-days` before the due date (assumed 3; DL22) | REQ-CWC-011 |
| BR6 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR7 | A repeated event with the same key is ignored and counted | R-UNI-40; events.txt Rules |
| BR8 | The treatment data product carries one row per treatment with its status: APPROVED (no booked at), BOOKED, RUNNING, BROKEN, COMPLETED, CANCELED (from outcome) | REQ-RDF-014; LOV-TRT-OUTCOME |
| BR9 | A plan whose case is not in the state the rule expects goes to the exception queue for a person | R-RES-35 pattern; R-UNI-41 |

### 9. State transitions

The case status does not change (it stays In progress). The route state changes:

| From | Event | Condition | To |
|---|---|---|---|
| BOOKED_IN_ALS_NLEADS | SCHEDULE_SET | first_due_date set (R-RES-25) | PLAN_RUNNING |
| PLAN_RUNNING | PAYMENT_MISSED | due date passed and no payment matched (R-RES-27) | PLAN_CURE_PERIOD |

Timer status: RUNNING to EXPIRED when the INSTALLMENT_DUE timer passes its expiry (JOB-05).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Records the treatment through the published interface; writes timers and the route state (Case record CRU; Treatment and offer R through the interface) |
| SY-RULES, rules component | Evaluates R-RES-25 and R-RES-27 |
| SY-DECLOG, decision log writer | Writes the entries (Decision log C) |
| RW-RESTRUCT, restructuring officer | Reads the treatment (Treatment and offer CRUA) |
| RW-CASEOWN, case owner | Reads the treatment and the timers (Treatment and offer CRU; Case record R) |
| RW-BIANAL, reporting and BI analyst | Reads the treatment data product (Reporting CRUD) |

The approval itself is made at the level set by the delegation of authority (doa.txt, item 2.1.1, levels 1 to 6) before this story runs.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 to DF-TRT-014 | treatment | all fields | Write |
| DF-TRT-029 | treatment | first_due_date | Write |
| DF-WRK-027 to DF-WRK-036 | timer | all fields | Write |
| DF-WRK-042 | timer | treatment_id | Write |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-007 | recovery_case | route_state | Write |
| DF-CAS-021 | recovery_case | rule_version | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through the P7 interface |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read, through the P7 interface, for the approval entry |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/treatments/{treatmentId}** (S2 endpoint; reads this story's record)

| Item | Value |
|---|---|
| Request | Path `treatmentId` (uuid) |
| Response | 200 `Treatment`: `id`, `caseId`, `decisionLogId`, `treatmentType`, `proposedBy`, `proposedAt`, `offerAmount`, `haircutAmount`, `installments`, `validUntil`, `approvalLevel`, `bookedAt`, `outcome`, `outcomeAt` |
| Errors | 401 (MSG-P4-001); 403 no Treatment and offer R (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 |
| Authorization | Treatment and offer, right R |
| Idempotency | Not applicable |

**GET /api/recovery/v1/cases/{caseId}/timers** (P3) returns `Timer[]`; Case record R. Used to check AC2 and AC12.

**Published interface** (S2 package `recovery.treatment.record.api`; the treatment table belongs to S2 per TSD S2, and this story builds its first version):

```java
public interface TreatmentRecords {
    Treatment recordApproved(RecordTreatmentCommand command);
    Optional<Treatment> find(UUID treatmentId);
    List<TreatmentSnapshot> changedSince(LocalDate businessDate);
}

public record RecordTreatmentCommand(UUID caseId, String treatmentType, String proposedBy,
        Instant proposedAt, BigDecimal offerAmount, BigDecimal haircutAmount, Integer installments,
        LocalDate validUntil, String approvalLevel, UUID decisionLogId, LocalDate firstDueDate,
        UUID idempotencyKey) {}
```

**Events**

| Event | Direction | Payload used |
|---|---|---|
| TreatmentApproved (EV-10) | Published by the treatment service; consumed by the plan timer listener | treatmentId, caseId, terms (firstDueDate, installments) |
| CaseStateChanged (EV-05) | Published | caseId, fromState, toState, ruleId, decisionLogEntryId |
| TimerDue (EV-18) | Published by JOB-05 | timerId, caseId, timerType |
| PaymentMissed (EV-12) | Consumed | treatmentId, dueDate, amountDue |

**Jobs.** JOB-05 Timer check (every 5 minutes) raises TimerDue for INSTALLMENT_DUE timers with no change to the job. JOB-15 Reporting extract (nightly 01:30) adds the DP04 treatment extract; idempotency key is the business date; a rerun replaces that date's extract.

### 13. Solution plan

**Package.** S2 package `recovery.treatment.record` for the treatment record; P3 package `recovery.casewf.plan` for the plan timer listener; P1 package `recovery.data.products.treatment` for the extract step.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TreatmentEntity | Entity | Maps `treatment` with the standard columns and `first_due_date` |
| TreatmentRepository | Repository | Reads and writes `treatment` only |
| TreatmentRecordService | Service | Validates the command, writes the row and the TreatmentApproved outbox row in one transaction |
| TreatmentRecords | Published interface | The interface in section 12 |
| PlanTimerListener | Listener | Consumes TreatmentApproved and PaymentMissed; calls the rules component; writes the decision log entry, then the timer and the route state |
| PlanTimerService | Service | Builds the INSTALLMENT_DUE and CURE_PERIOD timers from the due date and the product parameters |
| TreatmentExtractStep | Job | Spring Batch step in JOB-15 writing DP04 rows with the derived status |

**Database.** Flyway migration `V<next>__rwb_e2_004_treatment.sql` creates `treatment` as in Recovery Workbench Physical Schema v4.sql plus `first_due_date date`, with `ix_treatment_case_id` and `ix_treatment_decision_log_id`; adds `timer.treatment_id uuid` with index `ix_timer_treatment_id`. Unique index `ix_timer_plan_due` on `(treatment_id, timer_type, expires_at)` stops a second timer for the same due date.

**Configuration and reference data.** LOV-TIMER value INSTALLMENT_DUE (reference data administrator). CURE_PERIOD_DAYS per product and `plan.warn-days` (center of excellence, RWB-E1-045; values DL22). Rule rows R-RES-25 and R-RES-27 in the Restructure route set (center of excellence, RWB-E1-029). Event consumer retry limit 3 (NFR-026).

**Build steps**

1. Write the migration; prove the table, the new columns and the unique timer index.
2. Build `TreatmentRecordService` with the checks of X1, X2, X3 and X8, the outbox write and the published interface.
3. Build `PlanTimerService` with the due date, warning and cure period calculation through `ProductParameterService`.
4. Build `PlanTimerListener` for TreatmentApproved: idempotency on the event ID, rule evaluation of R-RES-25, decision log first, then timer and route state, then CaseStateChanged.
5. Add the X4 path: no rule match sends the case to the exception queue with MSG-P3-005.
6. Add PaymentMissed handling with R-RES-27 and the cure period timer.
7. Build `TreatmentExtractStep` in JOB-15 with the status derivation of BR8.
8. Write the tests in section 16 with a controlled clock.

**Feature flag.** `rwb.p3.plan-timers`. Off: treatments are recorded and no plan timers start.

**Done when.** The tests in section 16 pass, and the SIT run of 50 synthetic plans shows 50 treatment rows, 50 INSTALLMENT_DUE timers and 50 DP04 rows the next morning.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field or the decision log entry is missing | Enter {field}. |
| MSG-GEN-003 | The first due date is before the proposed date | {field} cannot be before {other}. |
| MSG-P3-005 | The case is closed, or not in the state the rule expects | This case cannot move to {state} from {current}. |
| MSG-P7-003 | The decision log write fails | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The treatment data product is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-003 | The installment timer is inside its warning period, shown on the case | {timer} ends on {date}. |
| MSG-P4-002 | A role without Treatment and offer R reads a treatment | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

No new screen. SCR-14 Treatment record (Epic 2 record view) shows the treatment in state Approved or Booked; SCR-03 Case record shows the INSTALLMENT_DUE and CURE_PERIOD timers with their due dates (RWB-E2-015). A case sent to the exception queue under X4 shows on SCR-09.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-004-01 | AC1, BR1 | System | Restructure, 36 installments, 850000.00 baht, entry DLE-9001 |
| TC-E2-004-02 | AC2, BR3, BR5 | System | First due date 2026-12-31; clock moved past expiry |
| TC-E2-004-03 | AC3, BR8 | System | Ten treatments over three products, two booked |
| TC-E2-004-04 | AC4, BR2 | System | Restructure with no first due date |
| TC-E2-004-05 | AC5, BR1 | System | Unknown decision log entry DLE-0000 |
| TC-E2-004-06 | AC6, BR2 | System | First due date one day before the proposal |
| TC-E2-004-07 | AC7, BR9 | System | Case in route state WITH_FCR_OFFICER |
| TC-E2-004-08 | AC8, BR7 | System | Same TreatmentApproved event twice |
| TC-E2-004-09 | AC9, BR6 | System | Decision log store stopped in the test container |
| TC-E2-004-10 | AC10 | System | JOB-15 forced to fail on 2026-12-02 |
| TC-E2-004-11 | AC11 | System | Closed case |
| TC-E2-004-12 | AC12, BR4 | System | PaymentMissed for due date 2026-12-31 |
| TC-E2-004-13 | Access | Access | RW-PHONECOL (no Treatment and offer right) reads `GET /treatments/{treatmentId}`; refused with MSG-P4-002 |
| TC-E2-004-14 | Principle 5 | Resilience | Decision log write forced to fail at timer start; no timer, no state change |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. Periods, warning days and the rules are reference rows; treatment types and outcomes come from LOV-TREATMENT and LOV-TRT-OUTCOME.
- No personal data in logs, tests, events or the data product extract beyond the IDs in the payload. Amounts are synthetic in tests.
- No read of another module's tables. P3 reaches the treatment only through `TreatmentRecords`; S2 reaches the case only through the P3 case interface; P1 reads treatments only through `changedSince`.
- The decision log entry is written before the timer and the route state; never the other way round.
- The treatment row is never deleted; a cancellation is an outcome.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer with type, terms, approval and outcome | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25 | TC-E2-004-01, TC-E2-004-04 to TC-E2-004-06, TC-E2-004-11, TC-E2-004-13 |
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25, R-RES-27, R-UNI-39, R-UNI-40 | TC-E2-004-02, TC-E2-004-07 to TC-E2-004-09, TC-E2-004-12, TC-E2-004-14 |
| REQ-RDF-014 | Stage 2 data products for plans and treatments exist before the first treatment | Business Requirements Epic 2, section 4; Program, section 5.1 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-004-03, TC-E2-004-10 |

### 19. Out of scope

- The offer builder, treatment screens and submission for approval (S2, Epic 3, FEAT-TRT-01).
- Reading the ACE plan status that calls this interface (RWB-E2-002).
- Booking confirmation from the ALS load and the booked at date (RWB-E2-007).
- Payment matching that raises PaymentMissed (P8, JOB-07).
- Broken plan handling after the cure period (R-RES-29 to R-RES-32, Epic 3).


---

## RWB-E2-005 Decision log query API for audit

| Item | Value |
|---|---|
| Story key | RWB-E2-005 |
| Epic | E2, release 31 December 2026 |
| Module | P7 Decision center and log |
| Feature | FEAT-CHO-11 Query the decision log for audit |
| Requirement IDs | REQ-DRI-012 |
| BRD section | Business Requirements Epic 2, section 3.7; Business Requirements Program, section 5.7 |
| L3 process | 17 Run the decision center |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-008, RWB-E1-039 |
| Status | Ready for build |

### 1. Story

As an **internal auditor (RW-AUDIT)**, I want **to query the decision log by case or a population of cases, decision, approver, date and rule version, with the hash chain checked on every entry returned, and to export the result**, so that **an audit question is answered from the log in minutes, and I can rely on each entry I am given**.

### 2. Business rationale

Audit and the regulator ask for the decision history of a sample of cases: inputs, versions, approver and final call. Today this is assembled by hand from e-mails and files. This story gives one query over the append-only log, filtered by the caller's scope, with each returned entry checked against the chain and a flag on any entry that does not match. It meets REQ-DRI-012 and NFR-036 (an audit request answered inside its deadline). The measure is the time to answer an audit sample: the first page of a query over 10,000 matching entries in 3 seconds or less (assumed; DL11).

### 3. Preconditions

- RWB-E1-008 is done: the store, the canonical form and the verifier.
- RWB-E1-039 is done: access events are written to the decision log.
- RWB-E1-048 is done: the rule change audit report gives the count of decisions per rule version, for reconciliation.
- Test users hold RW-AUDIT (scope ALL), RW-CASEOWN (scope OWN) and RW-PHONECOL (no Decision log letter) in SIT.
- The SIT store holds the synthetic set used below.

### 4. Flow

1. Internal auditor: opens SCR-38 Decision log query and enters the filters: case or list of cases, decision, rule ID, rule version, approver, from and to.
2. ACE front end: calls GET /decision-log with the filters, page and size.
3. Workbench (DecisionLogQueryService): validates the filters; applies the caller's scope through the case of each entry; runs the query in chain_seq order.
4. Workbench (ResultChainCheck): for each entry on the page, recomputes entry_hash from the canonical form and compares prev_hash with the entry before it; sets chainVerified on the entry.
5. Workbench: where an entry does not verify, returns it with chainVerified false and the warning, and raises an incident to Compliance once per entry.
6. Workbench: writes one AC-READ access event with the filter and the row count.
7. Internal auditor: selects export; the Workbench returns the full result as CSV and writes one AC-EXPT access event with the filter and the row count.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without Decision log R queries | Refused with 403; refusal logged | MSG-P4-002 | AC3 |
| X2 | A returned entry does not match the chain | The entry is returned with chainVerified false; warning shown; incident to Compliance | MSG-P7-012 | AC5 |
| X3 | The caller's scope excludes some matching entries | Only entries of cases in scope return; the excluded count is not shown | None | AC6 |
| X4 | From is after to, or size is outside 1 to 500, or more than 500 case IDs are given | Refused with 422 naming the field | MSG-GEN-003, MSG-GEN-002 | AC7 |
| X5 | No entry matches | 200 with an empty page and total 0; the screen shows the empty state | None | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads the store from RWB-E1-008 and writes access events through RWB-E1-039 |
| Negotiable | Page size limits and the performance target are parameters (DL11) |
| Valuable | Audit samples are answered from the log with each entry checked |
| Estimable | One query service, one per-entry check, one export, one screen |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion below is one test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Decision log query API for audit

  Background:
    Given the environment is SIT with the synthetic decision log set "DL-AUDIT-01"
    Given test user "U-8101" holds RW-AUDIT with scope "ALL"

  Scenario: AC1 Query by case
    Given case "RW-2026-000123" has six entries with chain_seq 101, 155, 160, 230, 231 and 402
    When "U-8101" calls GET /decision-log with caseId of that case
    Then the six entries return in chain_seq order
    Then each entry carries chainVerified true

  Scenario: AC2 Query by rule version
    Given rule R-LIT-03 at version "LIT-2026.12" was used in 200 decisions
    When "U-8101" calls GET /decision-log with ruleId "R-LIT-03" and ruleVersion "LIT-2026.12" and size 500
    Then 200 entries return and total is 200
    Then the total equals the count for "LIT-2026.12" in the rule change audit report

  Scenario: AC3 Access
    Given test user "U-8102" holds only RW-PHONECOL, whose Decision log letter is "-"
    When the user calls GET /decision-log
    Then the system refuses the call with status 403 and message MSG-P4-002
    Then one entry with decision code "AC-DENY", area "DECISION_LOG" and right "R" is written

  Scenario: AC4 Query by approver and period
    Given approver "U-8103" approved 14 decisions between 1 and 31 December 2026 and 3 in November 2026
    When "U-8101" calls GET /decision-log with approver "U-8103", from "2026-12-01" and to "2026-12-31"
    Then 14 entries return with approverUserId "U-8103" and approvalLevel filled

  Scenario: AC5 An entry that does not match the chain is flagged
    Given the entry with chain_seq 230 was changed in the SIT database with the trigger disabled
    When "U-8101" queries case "RW-2026-000123"
    Then six entries return and entry 230 carries chainVerified false
    Then the response carries warning MSG-P7-012 naming entry 230
    Then the system raises one incident to the Compliance queue for entry 230

  Scenario: AC6 Scope limits the result
    Given test user "U-8104" holds RW-CASEOWN with scope "OWN" and owns 3 of the cases decided under "LIT-2026.12"
    When "U-8104" queries ruleVersion "LIT-2026.12"
    Then only the entries of those 3 cases return and total counts only them

  Scenario: AC7 Invalid filters are refused
    When "U-8101" calls GET /decision-log with from "2026-12-31" and to "2026-12-01"
    Then the call returns status 422 with message MSG-GEN-003 for field "from"
    Then when "U-8101" calls it with size 1000
    Then the call returns status 422 with message MSG-GEN-002 for field "size" with min 1 and max 500

  Scenario: AC8 Export
    Given the query of AC2 returns 200 entries
    When "U-8101" exports the result from SCR-38
    Then a CSV file with a header row and 200 entry rows is returned, with chainVerified on each row
    Then one entry with decision code "AC-EXPT", the filter and row count 200 is written

  Scenario: AC9 No match
    When "U-8101" queries approver "U-8199", who approved nothing
    Then the call returns status 200 with no items and total 0
    Then SCR-38 shows the empty state

  Scenario: AC10 A population of cases
    Given cases "RW-2026-000123", "RW-2026-000124" and "RW-2026-000125" have 6, 2 and 4 entries
    When "U-8101" calls GET /decision-log with caseIds for the three cases
    Then 12 entries return, grouped by case and in chain_seq order within each case
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Audit can query the log for a population of cases and receive inputs, versions, approver and final call | REQ-DRI-012 |
| BR2 | Scope filters entries through their case before any is returned; the excluded count is never shown | LOV-SCOPE; Admin and access model, section 4.3 |
| BR3 | Every returned entry is checked against the canonical form and the entry before it | REQ-DRI-003; canonical form, RWB-E1-008 |
| BR4 | An entry that does not verify is returned flagged, never hidden, and raises an incident to Compliance | NFR-035 |
| BR5 | Every query and export writes an access event with the filter and the row count | REQ-ACA-006; RWB-E1-039 |
| BR6 | Page size is 1 to 500; a population holds at most 500 cases | Parameters rwb.decision.query.max-size=500, rwb.decision.query.max-cases=500 (assumed; DL11) |
| BR7 | The log is read only through this service; nothing in the query path changes an entry | REQ-DRI-002; ADR-009 |

### 9. State transitions

None. This story does not change a case status, and it changes no entry.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT Internal audit | Queries and exports every entry (Decision log R, scope ALL) |
| RW-COMPLY Compliance and PDPA officer | Queries and exports (Decision log R, scope ALL); receives incidents for entries that do not verify |
| RW-RISK, RW-COE | Query and export (Decision log R, scope ALL) |
| RW-CASEOWN and other roles holding Decision log R | Query entries of cases in their scope |
| RW-PHONECOL and roles without Decision log R | Refused |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read |
| DF-DEC-028 | decision_log_entry | chain_seq | Read |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (AC-READ and AC-EXPT access events through the writer) |
| DF-CAS-009 | recovery_case | owner_user_id | Read by the P3 scope filter interface |
| DF-CAS-011 | recovery_case | team_code | Read by the P3 scope filter interface |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /decision-log** (API-P7-006)

| Item | Value |
|---|---|
| Request | Query: caseId, decision, ruleId, approver, from, to, page, size; added in this story: caseIds (comma separated, at most 500), ruleVersion; Accept text/csv for export (additions file) |
| Response | DecisionLogPage: items (DecisionLogEntry plus chainVerified, added in this story), page, size, total; warning MSG-P7-012 when any entry fails; CSV with the same columns for export |
| Errors | 401; 403 no Decision log R (MSG-P4-002); 422 invalid filter (MSG-GEN-002, MSG-GEN-003); 503 the access event cannot be written (MSG-P7-003) or the store is unavailable (MSG-GEN-006) |
| Authorization | Decision log, right R, scope applied |
| Idempotency | Not applicable, read only |

**GET /api/recovery/v1/decision-log/{entryId}** (API-P7-007): the same per-entry check and chainVerified flag.

**Published interface used:** ScopeService.scopeFor (P4, RWB-E1-037); the P3 interface `Set<UUID> casesInScope(ScopeFilter filter, Collection<UUID> caseIds)`.

### 13. Solution plan

- Package: folder `recovery/decision/audit` in the recovery module; Java package `recovery.decision.audit`. Front end: `recovery/decision/audit`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| DecisionCenterAndLogController | Controller | GET /decision-log with the new filters and the CSV export |
| DecisionLogQueryService | Service | Validates filters, applies scope, pages in chain_seq order |
| ResultChainCheck | Service | Per-entry recomputation with CanonicalEntryForm and the prev_hash check, one extra read per page for the entry before the first |
| ChainMismatchNotifier | Service | Raises one incident per entry that fails, to Compliance |
| DecisionLogCsvWriter | Service | Streams the CSV export |
| DecisionLogQueryScreen | React component | SCR-38 with the filters, results, chainVerified column and export |

- Database: reads decision_log_entry; uses ix_declog_case_time, ix_declog_rule and ix_declog_actor_time (RWB-E1-008); adds index ix_declog_approver_time on (approver_user_id, decided_at) with Flyway migration V_E2_005__declog_approver_index.sql.
- Configuration and reference data: parameters rwb.decision.query.max-size and rwb.decision.query.max-cases (500, assumed, DL11); Compliance incident queue.
- Build steps:
  1. Add the approver index migration.
  2. Build DecisionLogQueryService with the filters and validation; tests for AC2, AC4, AC7, AC9, AC10.
  3. Apply scope through the P3 interface; test AC6.
  4. Build ResultChainCheck and ChainMismatchNotifier; tests for AC1 and AC5.
  5. Write AC-READ and AC-EXPT access events through RWB-E1-039; tests for AC3 and AC8.
  6. Build DecisionLogCsvWriter; test AC8.
  7. Build SCR-38 with the loading, results, empty and export states.
  8. Run the performance check over 10,000 matching entries against the 3 second target.
- Feature flag: `rwb.decision.audit-query`.
- Done when: the tests in section 16 pass and the count in AC2 reconciles to the rule change audit report in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-012 | A returned entry does not match the chain (new) | Entry {entryId} does not match the decision log chain. Do not rely on it until Compliance has reviewed it. |
| MSG-P4-002 | Query without Decision log R | You cannot {action} here. Your role does not include it. |
| MSG-GEN-002 | Size or the case list outside the limit | {field} must be between {min} and {max}. |
| MSG-GEN-003 | From after to | {field} cannot be before {other}. |
| MSG-P7-003 | The access event cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows DL10; proposed Thai for MSG-P7-012 is in the additions file.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-38 Decision log query | Loading | Waits while the first page loads; skeleton rows |
| SCR-38 Decision log query | Results | Reads entries with case, decision, rule and version, approver, level, final call, decided at and chainVerified; pages through; sees MSG-P7-012 at the top when an entry fails |
| SCR-38 Decision log query | Export | Downloads the CSV of the full result |
| SCR-38 Decision log query | Empty (common state) | Sees a sentence saying no entry matches the filters |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-005-01 | AC1, BR1, BR3 | System | Case with six synthetic entries |
| TC-E2-005-02 | AC2, BR1 | System | 200 entries under LIT-2026.12 and the rule change audit report |
| TC-E2-005-03 | AC3, BR5 | System | RW-PHONECOL test user |
| TC-E2-005-04 | AC4, BR1 | System | Approver with 14 December and 3 November entries |
| TC-E2-005-05 | AC5, BR4 | System | One entry changed in SIT with the trigger disabled |
| TC-E2-005-06 | AC6, BR2 | System | RW-CASEOWN test user owning 3 of the cases |
| TC-E2-005-07 | AC7, BR6 | System | Reversed dates; size 1000 |
| TC-E2-005-08 | AC8, BR5 | System | Export of 200 entries |
| TC-E2-005-09 | AC9 | System | Approver with no entries |
| TC-E2-005-10 | AC10, BR1 | System | Three cases with 6, 2 and 4 entries |
| TC-E2-005-11 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E2-005-12 | Principle 5 | Resilience | The decision log write of the access event forced to fail; the query returns nothing |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: limits and the target are parameters.
- No personal data in logs, tests or prompts; the export holds references and codes, and personal fields in recommendation or actions are masked per the masking rules before export.
- No read of another module's tables; scope comes through the P3 interface.
- No write to any entry from the query path.
- An entry that fails the check is shown, never dropped.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-012 | Audit queries the log for a population of cases with inputs, versions, approver and final call | Epic 2, 3.7 | FEAT-CHO-11 | 17 Run the decision center | BR1 to BR7 | TC-E2-005-01 to TC-E2-005-12 |

### 19. Out of scope

- The nightly check of the whole chain (RWB-TE-008).
- The approval queue and the decision screen SCR-10 and SCR-11 (RWB-E2-013, RWB-E2-014).
- The QA sample against the rule version applied (Epic 8, FEAT-ADM-08).
- Analysis on the data lake copy (RWB-E1-014).


---

## RWB-E2-006 Credit approval pack for NLEADS

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

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the credit approval pack for an approved plan prepared from the case for submission in NLEADS, and the NLEADS reference and result recorded on the treatment**, so that **a plan reaches credit without re-keying the case facts and the case moves on the credit result**.

### 2. Business rationale

A restructure outside the approved range goes to credit approval (R-RES-10), which the bank decides in NLEADS. Officers re-key the case facts and the plan terms into NLEADS today and the result is not on the case. NLEADS has no interface (INT-26), so this story assembles the pack from the case for the officer to submit, and records the NLEADS reference, result and approval level on the treatment, which moves the case by R-RES-11 or R-RES-12. It meets REQ-CHO-008 and REQ-CHO-006 and supports CTL-04.

### 3. Preconditions

- RWB-E2-004 (treatment entity and plan timers) and RWB-E1-007 (adapters) are done.
- The case is in route state AWAITING_CREDIT_APPROVAL with an open RESTRUCTURE treatment, and its ACE plan status is APPROVED (RWB-E2-002).
- The NLEADS pack checklist is loaded as reference data (DL19; assumed items: CREDIT_APPLICATION, ID_COPY, TITLE_DEED, LATEST_APPRAISAL, INCOME_PROOF).
- The delegation of authority rows for item 2.1.1 are loaded (DL18).
- The input age limit for balances in a credit pack is 1 business day (assumed; DL22).
- The person holds RW-RESTRUCT with the case in scope.

### 4. Flow

1. Restructuring officer: opens SCR-14 Treatment record and selects the credit approval pack.
2. Front end: calls GET /treatments/{treatmentId}/credit-pack.
3. System: checks the Treatment and offer right and the case scope; reads the case, accounts, collateral, latest valuation, plan terms and documents through the owning modules' interfaces.
4. System: reads the required approval level for the plan from the P7 DelegationQuery and the pack checklist rows.
5. System: returns the pack with each field ready to copy, the documents present with links, each missing checklist item, and the age of each input.
6. Restructuring officer: submits the plan in NLEADS and receives the NLEADS reference and later the result.
7. Restructuring officer: records the NLEADS reference, result, approval level, result date and, for a refusal, the reason.
8. System: validates the input and the treatment version; writes the decision log entry with decision D5, final call and the NLEADS reference in the actions.
9. System: writes the reference, result, reason, approval level and state on the treatment and raises CREDIT_APPROVED or CREDIT_DECLINED to P3.
10. SY-RULES and SY-CASEWF: an approval releases the offer to the customer (R-RES-11); a refusal records the reason (R-RES-12) and returns the case to the route decision in the case owner's queue (R-RES-14).

### 5. Exception paths

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

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the treatment entity (RWB-E2-004) and the plan status (RWB-E2-002) |
| Negotiable | The checklist, age limit and levels are data rows |
| Valuable | Removes re-keying into NLEADS and puts the credit result on the case |
| Estimable | Two endpoints, one service, one React panel |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

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

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| AWAITING_CREDIT_APPROVAL | CREDIT_APPROVED | final_call = approved | OFFER_WITH_CUSTOMER |
| AWAITING_CREDIT_APPROVAL | CREDIT_DECLINED | final_call = rejected | DECLINED_BY_CREDIT |
| DECLINED_BY_CREDIT | DECLINE_RECORDED | Any | BACK_TO_ROUTE_DECISION |

The case status moves from "Waiting approval" to "In progress" (status transition: approver accepts or rejects). The treatment state moves from SUBMITTED to APPROVED or REFUSED.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer | Opens the pack and records the result (Treatment and offer, CRUA) |
| RW-CASEOWN, case owner | Opens the pack and records the result on cases in scope (Treatment and offer, CRU) |
| RW-CREDCOMM, RW-PRODHEAD | Read the pack and the result (Treatment and offer, RA); they approve in NLEADS, not in this story |
| SY-RULES, SY-CASEWF | Evaluate R-RES-11, R-RES-12, R-RES-14 and move the case |
| SY-DECLOG, decision log writer | Writes the entry (Decision log, C) |
| Approval levels L1 to L6 | As in doa.txt item 2.1.1, recorded from NLEADS |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-007 | recovery_case | route_state | Read; write through the P3 interface |
| DF-ACC-002 | loan_account | account_no | Read |
| DF-ACC-009 | loan_account | principal_outstanding | Read |
| DF-ACC-010 | loan_account | interest_outstanding | Read |
| DF-ACC-012 | loan_account | total_balance | Read |
| DF-ACC-014 | loan_account | days_past_due | Read |
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-COL-002 | collateral | collateral_no | Read |
| DF-COL-003 | collateral | collateral_type | Read |
| DF-COL-023 | valuation | appraised_value | Read |
| DF-COL-025 | valuation | appraisal_date | Read |
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

### 12. Contract

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

### 13. Solution plan

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

### 15. Screens and states

SCR-14 Treatment record. In state submitted, the officer opens the credit approval pack, copies each field into NLEADS and opens each document link; missing items and stale inputs show their messages. The officer records the result in the result form; the screen moves to state approved, or shows the refusal reason and the case leaves the officer's view for the case owner's queue.

### 16. Test cases

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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the checklist, age limit and levels are rows.
- No personal data in logs, tests or prompts; the refusal reason is not written to application logs.
- No read of another module's tables; every pack section comes from its owner's interface.
- No call to NLEADS from the Workbench; the officer submits.
- The decision log entry is written before the treatment or the case changes.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Plan submitted for credit approval recorded on the case | Program 5.3; Epic 2 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-RES-10, R-RES-11, R-RES-12, R-RES-14, R-UNI-39 | TC-E2-006-02, TC-E2-006-03, TC-E2-006-06 to TC-E2-006-11, TC-E2-006-13 |
| REQ-CHO-006 | Treatment holds type, terms, approval and outcome | Program 5.3; Epic 2 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-006-01, TC-E2-006-04, TC-E2-006-05 |

### 19. Out of scope

- Generating a credit application document from a template: RWB-E2-026.
- Booking the plan in NLEADS and ALS and its confirmation: RWB-E2-007 and Epic 3 (R-RES-21, R-RES-22).
- Approval inside the Workbench for decisions within the delegation: RWB-E2-013.


---

## RWB-E2-007 Booking confirmation from the ALS load

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

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the booked terms of each approved restructure or settlement matched from the next day's ALS load to the approved treatment, with a task when the booking is missing or differs**, so that **every approved decision is confirmed as booked in the core bank**.

### 2. Business rationale

The officer books restructures and settlements in ALS by hand (INT-03), and nothing checks today that the booked terms equal the approved terms. This story compares each approved treatment with the next ALS load, marks it booked when the terms match, and raises a task to the officer when the booking is missing or to Credit Administration when the terms differ. It meets REQ-CHO-008 and is measured by REC-03 (approved treatments against bookings, zero after two days).

### 3. Preconditions

- RWB-E2-004 (treatment entity) and RWB-E1-007 (adapters, IdempotencyGuard) are done.
- JOB-01 loads INT-01 with tdr_flag, last_tdr_date, interest_rate and principal_outstanding, and the two new settlement booking fields, for business date D.
- The booking match rows are loaded (versioned reference data): for RESTRUCTURE compare tdr_flag, last_tdr_date, principal_outstanding against offer_amount and interest_rate against the approved rate; for SETTLEMENT compare settlement_booked_date and settlement_booked_amount against offer_amount; tolerance 0.00 baht (DL25).
- Parameter `booking.missing.grace_loads` = 1 (one ALS load after approval).
- Rules R-RES-22 and R-SET-13 are in force.
- TreatmentApproved (EV-10) is published for each approved treatment.

### 4. Flow

1. Scheduler: JOB-08 starts after JOB-01 publishes LoadCompleted (EV-26) for ALS with business date D.
2. SY-DATALOAD: the BookingMatchService lists approved treatments of type RESTRUCTURE or SETTLEMENT not yet booked, through the treatment interface.
3. SY-DATALOAD: for each treatment, checks IdempotencyGuard on treatment ID + D; a repeat is skipped.
4. SY-DATALOAD: reads every account of the case through the P1 AccountQuery for business date D.
5. SY-DATALOAD: applies the booking match rows for the treatment type to each account.
6. SY-DATALOAD: when every account matches, calls TreatmentCommands.markBooked with the business date; P8 publishes TreatmentBooked (EV-11); P3 writes the decision log entry and moves the case by R-RES-22 or R-SET-13.
7. SY-DATALOAD: when no booking is found after the grace loads, raises one task WITH_OPS_BOOKING or WITH_OPS_SETTLEMENT for role RW-RESTRUCT with MSG-P2-011; the treatment stays approved.
8. SY-DATALOAD: when a booking is found with a different term, writes the difference on the treatment and raises one task UNMATCHED_EXCEPTION for role RW-CREDITAD with MSG-P2-012; the treatment stays approved.
9. SY-DATALOAD: writes the run summary: treatments read, booked, missing, differing; the P1 reconciliation REC-03 reads the same results.

### 5. Exception paths

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

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the treatment entity (RWB-E2-004) and the ALS load |
| Negotiable | Terms compared, tolerance and grace are data rows |
| Valuable | Every approved restructure and settlement is confirmed as booked or raised |
| Estimable | One matching service, one job, two task paths |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

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

### 8. Business rules

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

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| WITH_OPS_BOOKING | BOOKING_CONFIRMED | ALS and NLEADS both acknowledge: NLEADS result APPROVED recorded and every account matched | BOOKED_IN_ALS_NLEADS |
| WITH_OPS_SETTLEMENT | SETTLEMENT_BOOKED | Agreement signed and terms booked in ALS | AWAITING_PAYMENT |

The treatment state moves from APPROVED to BOOKED. A missing or differing booking leaves both the route state and the treatment state unchanged.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Runs JOB-08, reads accounts, marks bookings, raises tasks |
| SY-CASEWF, case workflow module | Moves the case on BOOKING_CONFIRMED or SETTLEMENT_BOOKED; raises the tasks |
| SY-DECLOG, decision log writer | Writes the entry (Decision log, C) |
| RW-RESTRUCT, restructuring officer | Receives the missing booking task and books in ALS (Treatment and offer, CRUA) |
| RW-CREDITAD, Credit Administration officer | Receives the differing terms task (Write-off and posting, CRUA) |
| RW-DATASTEW, data steward | Reads the REC-03 break list |
| RW-PLATADM, platform administrator | Reruns JOB-08 (Platform administration, U) |

### 11. Data

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

### 12. Contract

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

### 13. Solution plan

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

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-011 | Task text, booking missing | No booking for treatment {treatment} was found in the ALS load for {date}. Book it in ALS. Accounts not booked: {accounts}. |
| MSG-P2-012 | Task text and treatment note, term differs | The booked {term} is {booked}. The approved {term} is {approved}. |
| MSG-P1-001 | ALS load late or refused | {product} is from {date}. Today's load has not arrived. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | Rerun while JOB-08 runs | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the right reruns JOB-08 | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-14 Treatment record, states approved and booked: the officer sees booked at, or the booking difference with each term approved and booked. The officer and the Credit Administration officer see their tasks on SCR-01 My work. SCR-29 Posting, which shows the confirmation for all bookings, comes in Epic 4.

### 16. Test cases

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

### 17. Guardrails

- No business value in code: compared terms, tolerance and grace are rows or parameters.
- No personal data in logs, tests or prompts; the booking reference holds the account ID, not the account number.
- No read of another module's tables; accounts, treatments and tasks are reached through their interfaces.
- No call to ALS; the match reads only the loaded data.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Booking confirmed from the next day's ALS load | Program 5.3; Epic 2 3.2 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39 | TC-E2-007-01 to TC-E2-007-08, TC-E2-007-10 |

### 19. Out of scope

- Posting a settlement booking to ALS from the Workbench: FEAT-PAY-06, Epic 4.
- Payment matching to the plan or settlement: JOB-07 and FEAT-OCC-10, Epic 2.
- The SCR-29 Posting screen: Epic 4.


---

## RWB-E2-008 Payment matching with the missed payment event

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

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **payments from the ALS load matched to the running plans each day, with a missed payment event when a due installment has not arrived**, so that **a broken plan is known the day after it breaks**.

### 2. Business rationale

Payments are matched to plans by hand today, and a missed installment is found weeks later, after the cure period has gone. This story matches each payment in the daily ALS load (INT-02) to the plan installment it pays, keeps anything unmatched on the exception list, and raises PaymentMissed the morning after a due date passes with no payment, which the restructure rules (R-RES-27) and the transfer rules act on. It serves REQ-CHO-007 and REQ-CHO-009, control CTL-41 and the FSD P8 measure "receipts matched the same day".

### 3. Preconditions

- RWB-E1-003 is done: the ALS payments load into account_payment each morning through JOB-01, with checks DQ-008 to DQ-014.
- RWB-E2-004 is done: the treatment record holds running plans with installment amount and installments paid, readable and updatable through TreatmentApi.
- The next due date of each plan account comes from loan_account.next_installment_date in the same ALS load.
- The payment matching parameters are loaded as reference data: one EXACT row, version "PM-2026.12".
- JOB-01 has passed for the business date and published LoadCompleted (EV-26).
- P3 consumes PaymentMissed and applies R-RES-27 and the transfer rules (RWB-E1-021).

### 4. Flow

1. JOB-07 Payment matching: starts when LoadCompleted arrives for the ALS source and business date, after JOB-01.
2. System: reads the payments loaded for the business date through the P1 interface.
3. System: for each payment, finds the open case of the account through the P3 interface; a payment on an account with no open case goes to the data quality exception list.
4. System: reads the running plans on the case and the parameter row in force; a payment on the plan account for the installment amount, dated inside the window before the next due date, matches that installment.
5. System: writes a proceeds row with source CUSTOMER and matched_to INSTALLMENT, calls TreatmentApi.recordInstallmentPaid, and writes ProceedsMatched to the outbox in the same transaction.
6. System: a payment that matches no plan installment is written with matched_to UNMATCHED and appears on the exception list for the reconciliation agent (R-UNI-03).
7. System: after all payments, for each running plan whose next due date plus the grace days is before the business date and that has no matched payment for that due date, writes PaymentMissed with treatment ID, due date and amount due.
8. P3: applies R-RES-27 (plan to the cure period) and the transfer rule; the case owner sees the missed payment on the treatment record the same morning.
9. System: writes the run summary (payments read, matched, unmatched, missed events) to the job monitor and runs REC-04 (payments in the ALS load against proceeds).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A payment matches no plan installment | Proceeds row UNMATCHED on the exception list | MSG-P8-001 | AC3 |
| X2 | A payment is on an account with no open case | Held on the data quality exception list; no proceeds row | None | AC4 |
| X3 | The ALS load for the business date is refused or late | JOB-07 does not run; no missed payment is raised from stale data | MSG-P1-001 | AC5 |
| X4 | JOB-07 runs twice for one business date | No second proceeds row and no second event | None | AC6 |
| X5 | A payment arrives on the last day of the window | It matches | None | AC7 |
| X6 | A payment arrives one day before the window opens | It does not match | MSG-P8-001 | AC7 |
| X7 | No parameter row is in force on the business date | JOB-07 stops before matching; nothing is written | MSG-P8-002 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the payments load (RWB-E1-003) and the treatment record (RWB-E2-004); partial and window rules come in RWB-E2-027 |
| Negotiable | Window, grace days and amount rule are reference data |
| Valuable | A missed installment is known the morning after the due date |
| Estimable | One job, one matcher, one table, one event |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against a synthetic ALS load |

### 7. Acceptance criteria

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

### 8. Business rules

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

### 9. State transitions

None. This story does not change a case status. P3 changes the plan route state on the events this story writes:

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | PLAN_RUNNING (next due date advanced, R-RES-26) |
| PLAN_RUNNING | PAYMENT_MISSED | due_date passed and no payment matched | PLAN_CURE_PERIOD (R-RES-27) |

This story writes the proceeds match state (matched_to INSTALLMENT or UNMATCHED).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load from COLLINS | Runs JOB-07 (Write-off and posting U) |
| SY-CASEWF, case workflow module | Consumes PaymentMissed and ProceedsMatched |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent (Write-off and posting R) |
| RW-CREDITAD, Credit Administration officer | Reads matched and unmatched receipts on SCR-28 (Write-off and posting CRUA) |
| RW-CASEOWN, case owner | Reads the plan position on SCR-14 (Treatment and offer R) |
| RW-REFADM, reference data administrator | Loads the parameter rows (Reference data C) |

### 11. Data

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

### 12. Contract

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

### 13. Solution plan

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

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P8-002 | No parameter row in force | Payment matching for {date} did not run: no matching rule is in force. |
| MSG-P1-001 | The ALS load is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | The role lacks Write-off and posting R | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-28 Proceeds matching (skeleton in E2; states Loading; matched; unmatched) lists receipts from GET /proceeds for the Credit Administration officer, filtered by matched or unmatched. The case owner sees the plan position on SCR-14 Treatment record and the missed payment on SCR-04 Case timeline. SCR-44 shows the JOB-07 run summary.

### 16. Test cases

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

### 17. Guardrails

- No business value in code: window, tolerance, grace days and match types are rows in payment_match_rule.
- No personal data in logs, tests or prompts. Payments are identified by payment code and account ID; account numbers are never logged.
- No read of another module's tables. account_payment, loan_account, case_account and treatment are read through P1 and P3 interfaces; the treatment is updated only through TreatmentApi.
- Amounts use BigDecimal with scale 2 and are compared exactly.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-E2-008-02, TC-E2-008-05, TC-E2-008-06 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03, R-UNI-40 | TC-E2-008-01, TC-E2-008-03, TC-E2-008-04, TC-E2-008-07, TC-E2-008-08, TC-E2-008-09 |

### 19. Out of scope

- Partial payments, late payments inside a window after the due date and rule versions in the decision log (RWB-E2-027).
- Settlement, auction and enforcement proceeds (FEAT-PAY-03, FEAT-PAY-04, Epic 4).
- Manual matching of an unmatched receipt (POST /proceeds/{proceedsId}/match, Epic 4).
- The cure period and the broken plan rule (R-RES-28 to R-RES-31, FEAT-TRT-11, Epic 3).


---

## RWB-E2-009 Steering dashboard v1 data set

| Item | Value |
|---|---|
| Story key | RWB-E2-009 |
| Epic | E2, release 31 December 2026 |
| Module | P9 Reporting |
| Feature | FEAT-OCC-12 Publish the steering dashboard; FEAT-RPT-03 Publish the steering dashboard; FEAT-RPT-08 Refresh and publish the measure set |
| Requirement IDs | REQ-WKM-009, REQ-WKM-006 |
| BRD section | Business Requirements Epic 2, sections 3.9 and 4 |
| L3 process | 15 Manage performance, data and AI |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-013, RWB-E1-063 |
| Status | Ready for build |

### 1. Story

As the **Tribe lead (RW-TRIBE)**, I want **a data set for the steering dashboard with cases by stage, queue and age, decisions logged, treatments, letters sent and agent acceptance, published each morning and reconciled to the case list**, so that **the steering committee reads the same numbers the teams work with**.

### 2. Business rationale

The steering committee receives numbers counted by hand that differ from what the teams see in their queues. This story adds the steering measures to the nightly measure set, holds the publish when the dashboard case count differs from the case list, serves the values through GET /reports/measures to SCR-37 and through the data lake extract to Power BI, and adds agent acceptance and override rates. It serves REQ-WKM-009 and REQ-WKM-006, NFR-065 and NFR-066.

### 3. Preconditions

- RWB-E1-013 is done: measure_definition, measure_snapshot, MeasureCatalog and JOB-15 run, with the baseline of 2026-11-27 frozen.
- RWB-E1-063 is done: agent runs and their outcomes are readable through the P10 monitoring interface.
- The steering definitions, version "MD-2026.12", are loaded and approved by the Tribe lead.
- Notices, treatments and decision log entries are readable through the P6, P3 and P7 reporting interfaces.
- The reader holds a role with Reporting R and the case scope "All", or reads only the teams in their scope.

### 4. Flow

1. JOB-15 Reporting extract, nightly 01:30: reads the definitions in force, including the steering measures of MD-2026.12.
2. System: computes each steering measure for the previous business date from the owning modules' reporting interfaces.
3. System: compares the total of CASES_BY_STAGE with the open case count of the case list at the same cut-off (P3 interface).
4. System: if the counts are equal, writes the snapshot rows and the INT-19 extract with the freshness stamp; if not, holds the publish, keeps the previous day as the latest published and alerts the Reporting and BI analyst and the data steward.
5. Reporting and BI analyst: the Power BI data set refreshes at 07:30 from the extract.
6. Product head or team manager: opens SCR-37 Steering dashboard; the screen calls GET /reports/measures with product, route and date filters.
7. System: checks Reporting R and the scope, returns the published values with the business date and the freshness stamp, and shows the baseline beside each value.
8. System: computes agent acceptance and override rates per agent and version from the decision log and the agent runs; an agent with no runs shows "No runs" and no rate.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Dashboard case count differs from the case list | Publish held; previous day stays; alert | MSG-P9-002 | AC4 |
| X2 | A source load for the business date is stale | Previous day shown with its date | MSG-P1-001 | AC5 |
| X3 | Query with from after to | Refused | MSG-GEN-003 | AC6 |
| X4 | An agent has no runs on the day | No rate; "No runs" shown | None | AC7 |
| X5 | JOB-15 rerun for a published business date | Rows replaced with the same values; baseline unchanged | None | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Extends the measure set of RWB-E1-013; agent data from RWB-E1-063 |
| Negotiable | Steering measures are definition rows; layout of SCR-37 follows the ACE components |
| Valuable | One set of numbers for the committee and the teams |
| Estimable | Seven calculators, one reconciliation check, one endpoint, one screen |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against a synthetic day with known answers |

### 7. Acceptance criteria

```gherkin
Feature: Steering dashboard v1 data set

  Background:
    Given definition version "MD-2026.12" is in force with measures "CASES_BY_STAGE", "CASES_BY_QUEUE_AGE", "DECISIONS_LOGGED", "TREATMENTS", "LETTERS_SENT", "AGENT_ACCEPTANCE" and "AGENT_OVERRIDE"
    Given the synthetic day 2026-12-15 holds 240 open cases, 1,412 decision log entries, 38 treatments and 95 notices sent

  Scenario: AC1 Refresh
    Given the loads of business date 2026-12-15 passed their checks
    When JOB-15 runs at 01:30 on 2026-12-16
    Then GET /reports/measures?from=2026-12-15&to=2026-12-15 returns a value for each of the 7 measures with period "2026-12-15"
    Then the INT-19 extract for 2026-12-15 has freshness stamp 2026-12-15 for the 07:30 Power BI refresh

  Scenario: AC2 Reconciles
    Given the case list shows 240 open cases at the 2026-12-15 cut-off
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the sum of "CASES_BY_STAGE" for 2026-12-15 is 240
    Then "DECISIONS_LOGGED" for 2026-12-15 is 1,412, the count of decision log entries decided that day

  Scenario: AC3 Agent measures
    Given agent "case-intake" version "1.2.0" made 200 recommendations on 2026-12-15, of which 170 were accepted and 30 overridden with a reason
    When JOB-15 runs at 01:30 on 2026-12-16
    Then "AGENT_ACCEPTANCE" for "case-intake" "1.2.0" on 2026-12-15 is 85.0 percent
    Then "AGENT_OVERRIDE" for "case-intake" "1.2.0" on 2026-12-15 is 15.0 percent
    Then SCR-37 shows both rates by agent

  Scenario: AC4 Counts do not match
    Given the case list shows 240 open cases at the 2026-12-15 cut-off
    Given the case facts read for the dashboard total 239
    When JOB-15 runs at 01:30 on 2026-12-16
    Then no snapshot rows and no extract are published for 2026-12-15
    Then SCR-37 shows 2026-12-14 as the latest day with MSG-P9-002 naming 239, 240 and 2026-12-15
    Then an alert goes to the Reporting and BI analyst and the data steward

  Scenario: AC5 Stale source
    Given the notice data product is from 2026-12-14 because the 2026-12-15 load has not arrived
    When a product head opens SCR-37 on 2026-12-16
    Then "LETTERS_SENT" shows the value for 2026-12-14
    Then SCR-37 shows MSG-P1-001 naming "DP07 Legal" and 2026-12-14

  Scenario: AC6 Dates in the wrong order
    Given a team manager holds RW-TEAMMGR with Reporting R
    When a team manager sends GET /reports/measures?from=2026-12-15&to=2026-12-01
    Then the response is status 422 with MSG-GEN-003 naming "from" and "to"

  Scenario: AC7 Agent with no runs
    Given agent "deviation-screen" version "0.9.0" made no recommendations on 2026-12-15
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the system writes no "AGENT_ACCEPTANCE" value for "deviation-screen" on 2026-12-15
    Then SCR-37 shows "No runs" for "deviation-screen" on 2026-12-15

  Scenario: AC8 Filter by product
    Given the measures for 2026-12-15 are published and the case list shows 140 open Mortgage cases at the cut-off
    When a product head sends GET /reports/measures?measure=CASES_BY_STAGE&product=MORTGAGE&from=2026-12-15&to=2026-12-15
    Then the response holds only rows with product "MORTGAGE"
    Then their sum is 140

  Scenario: AC9 Rerun of a published day
    Given the measures for 2026-12-15 are published
    When JOB-15 is rerun for business date 2026-12-15 from SCR-44
    Then the rows for 2026-12-15 hold the same values
    Then the frozen baseline rows of 2026-11-27 are unchanged
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Steering measures are computed from Workbench records and the decision log, never from a separate count | NFR-065; REQ-WKM-009 |
| BR2 | The dashboard case count equals the case list count at the same cut-off, or the publish is held | REQ-WKM-006; DL25 (tolerance zero) |
| BR3 | Agent acceptance is accepted recommendations over all recommendations, and override is overridden over all, per agent and version | NFR-066; DF-DEC-007, DF-DEC-013 |
| BR4 | A measure is shown with its business date and freshness stamp; stale data shows its date | MSG-P1-001 rule; FEAT-RPT-08 |
| BR5 | Each value is shown beside the frozen baseline of 2026-11-27 | REQ-WKM-009; RWB-E1-013 BR2 |
| BR6 | A rate with no runs in the denominator is not computed | NFR-066 |
| BR7 | Every query applies the role's scope | CTL-09 |

### 9. State transitions

None. This story does not change a case status. It sets the publish status of a business date (published or held) and the JOB-15 run status.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, Tribe lead and squad members | Reads SCR-37 and the measures (Reporting R); approves the steering definitions |
| RW-PRODHEAD, product head | Reads SCR-37 (Reporting R) |
| RW-TEAMMGR, team manager | Reads SCR-37 for teams in scope (Reporting R) |
| RW-BIANAL, Reporting and BI analyst | Builds the Power BI report; receives the hold alert (Reporting CRUD) |
| RW-DATASTEW, data steward | Receives the hold alert; reads the reconciliation (Reporting CRU) |
| RW-FINANCE, Finance and CFO delegate | Reads SCR-37 (Reporting R) |
| RW-REFADM, reference data administrator | Loads the steering definitions (Reference data C) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-006 | recovery_case | stage_code | Read |
| DF-CAS-008 | recovery_case | route_code | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-LEG-018 | notice | notice_type | Read |
| DF-LEG-019 | notice | sent_date | Read |
| DF-LEG-022 | notice | delivery_status | Read |
| DF-DEC-003 | decision_log_entry | decision_code | Read |
| DF-DEC-007 | decision_log_entry | agent_version | Read |
| DF-DEC-012 | decision_log_entry | final_call | Read |
| DF-DEC-013 | decision_log_entry | override_reason | Read |
| DF-DEC-016 | decision_log_entry | decided_at | Read |
| DF-RPT-032 | measure_definition | measure_code | Read |
| DF-RPT-034 | measure_definition | formula | Read |
| DF-RPT-035 | measure_definition | data_product | Read |
| DF-RPT-037 | measure_definition | definition_version | Read |
| DF-RPT-042 | measure_snapshot | measure_code | Write |
| DF-RPT-043 | measure_snapshot | definition_version | Write |
| DF-RPT-044 | measure_snapshot | business_date | Write |
| DF-RPT-045 | measure_snapshot | product_group | Write |
| DF-RPT-046 | measure_snapshot | dimension_code | Write |
| DF-RPT-047 | measure_snapshot | dimension_value | Write |
| DF-RPT-048 | measure_snapshot | value | Write |
| DF-RPT-049 | measure_snapshot | case_count | Write |
| DF-RPT-052 | measure_snapshot | published_at | Write |
| DF-RPT-054 | measure_publish | business_date | Write |
| DF-RPT-055 | measure_publish | status | Write |
| DF-RPT-056 | measure_publish | case_list_count | Write |
| DF-RPT-057 | measure_publish | dashboard_count | Write |
| DF-RPT-058 | measure_publish | held_reason | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/reports/measures** (api.yaml, x-module P9)

| Item | Value |
|---|---|
| Request | Query: measure, product, route, from, to (dates, from on or before to) |
| Response | 200 array of Measure: measure, product, route, period, value, and the new dimension and baselineValue. The response header X-Data-As-Of carries the business date of the latest published day |
| Errors | 401 no session (MSG-P4-001); 403 role lacks Reporting R (MSG-P4-002); 422 dates in the wrong order (MSG-GEN-003); 503 store unavailable (MSG-GEN-006) |
| Authorization | Reporting, right R, scope applied |
| Idempotency | Not applicable |

The Measure schema in api.yaml has no dimension or baseline field. This story adds dimension (the dimension code and value, for example "agent:case-intake:1.2.0") and baselineValue to the Measure schema, recorded as missing fields in the additions file.

**Job JOB-15 Reporting extract**: as in RWB-E1-013, with the reconciliation step before publish. Idempotency key unchanged. Restart: rerun from SCR-44; a held day is published by the first run whose counts match.

**Published interfaces called**

```java
Stream<CaseFact> CaseReportingApi.caseFacts(LocalDate businessDate);                     // P3
long CaseReportingApi.openCaseCount(LocalDate cutOff, Optional<String> productGroup);   // P3, the case list count
Stream<DecisionFact> DecisionLogApi.decisionFacts(LocalDate businessDate);              // P7
Stream<TreatmentFact> TreatmentApi.treatmentFacts(LocalDate businessDate);              // P3
Stream<NoticeFact> NoticeApi.noticeFacts(LocalDate businessDate);                       // P6
Stream<AgentRunFact> AgentMonitorApi.runFacts(LocalDate businessDate);                  // P10, RWB-E1-063
```

### 13. Solution plan

- Package: folder `recovery/reporting/steering`, Java package `recovery.reporting.steering`; front end folder `recovery/reporting/steering`.

| Component | Type | Responsibility |
|---|---|---|
| SteeringCalculators | Service | One calculator per steering measure code |
| CountReconciliation | Service | BR2 check before publish; writes measure_publish |
| ReportingExtractJob | Job | From RWB-E1-013; adds the steering calculators and the reconciliation step |
| MeasureController | Controller | GET /reports/measures with filters, scope and X-Data-As-Of |
| MeasureQueryRepository | Repository | Reads published measure_snapshot rows by filter |
| SteeringDashboard | React component | SCR-37: filters by product, route and date; value beside baseline; agent rates; freshness and hold messages |

- Database: new table measure_publish (unique business_date). Index on measure_snapshot (measure_code, business_date, product_group). Flyway migration `V2_009__measure_publish.sql`.
- Configuration and reference data: steering definitions MD-2026.12 (Tribe lead approves; RW-REFADM loads); reconciliation tolerance zero (DL25); age bands from RWB-E1-013.
- Build steps:
  1. Write the migration and the measure_publish entity.
  2. Build the seven calculators against stub interfaces with the synthetic day; test AC1, AC2 values and AC3, AC7.
  3. Build CountReconciliation and wire it before publish in ReportingExtractJob; test AC4 and AC9.
  4. Build MeasureController with filters, date check, scope and X-Data-As-Of; test AC6 and AC8.
  5. Build SteeringDashboard with Loading and filtered states and the stale and held messages; test AC5 in the browser.
- Feature flag: `rwb.reporting.steering`.
- Done when: the tests in section 16 pass, and the Power BI report and SCR-37 show the same values for one SIT day.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P9-002 | The dashboard count differs from the case list | The case count on the dashboard ({count}) does not match the case list ({listCount}) for {date}. The publish is held. |
| MSG-P1-001 | A source is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-003 | Dates in the wrong order | {field} cannot be before {other}. |
| MSG-P4-002 | The role lacks Reporting R | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-37 Steering dashboard (module P9, capability area Reporting):

| State | What the user sees and does |
|---|---|
| Loading | Skeleton rows while GET /reports/measures returns |
| Filtered | Values for the chosen product, route and dates, each beside the baseline of 2026-11-27, with the business date; agent rates by agent and version; MSG-P9-002 or MSG-P1-001 when the latest day is held or stale |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-009-01 | AC1, BR1, BR4 | System | Synthetic day 2026-12-15 |
| TC-E2-009-02 | AC2, BR1, BR2 | System | 240 open cases; 1,412 decision log entries |
| TC-E2-009-03 | AC3, BR3 | System | case-intake 1.2.0: 200 recommendations, 170 accepted, 30 overridden |
| TC-E2-009-04 | AC4, BR2 | System | Case list 240, case facts 239 |
| TC-E2-009-05 | AC5, BR4 | System | Notice product dated 2026-12-14 |
| TC-E2-009-06 | AC6 | System | from 2026-12-15, to 2026-12-01 |
| TC-E2-009-07 | AC7, BR6 | System | deviation-screen 0.9.0 with no runs |
| TC-E2-009-08 | AC8, BR7 | System | Filter MORTGAGE |
| TC-E2-009-09 | AC9, BR5 | System | JOB-15 rerun for 2026-12-15 |
| TC-E2-009-10 | Access | Access | PT-LAWFIRM calls GET /reports/measures; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: measures, formulas, tolerance and bands are data.
- No personal data in logs, tests or prompts. Measures carry counts, rates, amounts and codes only; agent outputs are counted, never copied.
- No read of another module's tables. Every fact comes through the owning module's reporting interface.
- Counts on SCR-37 and in Power BI come from the same measure_snapshot rows.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-009 | Steering dashboard reports volume, ageing, route mix, turnaround and recovery against the baseline | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-OCC-12, FEAT-RPT-03, FEAT-RPT-08 | 15 Manage performance, data and AI | None; NFR-065 and NFR-066 apply | TC-E2-009-01, TC-E2-009-03, TC-E2-009-05, TC-E2-009-06, TC-E2-009-07, TC-E2-009-09, TC-E2-009-10 |
| REQ-WKM-006 | Queue counts and ageing reported daily and reconciled to the case list | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-RPT-08 | 15 Manage performance, data and AI | None; DL25 applies | TC-E2-009-02, TC-E2-009-04, TC-E2-009-08 |

### 19. Out of scope

- Queue measures and service level breaches for team managers (RWB-E1-030, RWB-E2-011).
- The agent monitoring dashboard with latency and cost (RWB-E2-031).
- Benefit realisation against the baseline (FEAT-RPT-06, Epic 6).
- Regulatory returns (FEAT-RPT-07, Epic 8).


---

## RWB-E2-010 Stage 2 data products: contracts, plans and treatments

| Item | Value |
|---|---|
| Story key | RWB-E2-010 |
| Epic | E2, release 31 December 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-CHO-09 Build the stage 2 data products |
| Requirement IDs | REQ-RDF-014 |
| BRD section | Business Requirements Epic 2, section 3.1 (story) and section 4 (REQ-RDF-014) |
| L3 process | 07 Route, settle and claim |
| Decision | D6.4 to D6.6 |
| Priority | Should |
| Depends on | RWB-E2-004, RWB-E1-016, RWB-E1-015 |
| Status | Ready for build |

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the stage 2 data products (treatments, plans, contracts and guarantees) added to the recovery data store with their systems of record**, so that **the settlement, TDR and DIL screens in Epic 3 read from one store**.

### 2. Business rationale

From Epic 3 the settlement, restructure and deed in lieu screens need each case's treatments, plan terms, loan contracts and guarantee claims in one checked place. The treatment record lives with the module that owns it (RWB-E2-004), plan terms come from the ACE restructure calculation, contract numbers come from ALS, and guarantee claims come from the guarantee module. A daily build of the DP04 Treatment product brings them into the data store with a catalog entry, a freshness stamp, access by role and checks that every row links to a case. Serves REQ-RDF-014: stage 2 data products exist before the first treatment goes live.

### 3. Preconditions

- RWB-E2-004 is done: the treatment entity exists and its module publishes TreatmentQuery (section 12).
- RWB-E1-016 is done: data_product_access and the data product read endpoint exist.
- RWB-E1-015 is done: freshness stamps and the stale check exist.
- RWB-E1-064 is done: data_product holds DP04 Treatment with system of record "Workbench" and owner RW-DATASTEW, and sys_fields holds treatment and guarantee_claim.
- data_product_access version "DPA-2026.12" gives DP04 read to RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD, RW-COE and RW-AUDIT.
- The guarantee module publishes GuaranteeClaimQuery; before it is built (Epic 4), the interface returns no claims.

### 4. Flow

1. JOB-01: after the COLLINS load for business date D passes its checks, starts the stage 2 product step.
2. Stage2ProductService: calls TreatmentQuery.changedBetween(start of D, end of D) and receives the treatments created or changed on D, with plan terms from the ACE restructure calculation.
3. Stage2ProductService: calls GuaranteeClaimQuery.changedBetween() for guarantee claims changed on D.
4. Stage2ProductService: resolves each case's primary account through CaseScopeQuery and reads its contract number and contract date from loan_account.
5. Stage2ProductService: holds in the data quality exception list any row whose case does not resolve (check References), and writes the other rows to dp_treatment and dp_guarantee_claim keyed by record ID.
6. Stage2ProductService: compares the count of active treatments in dp_treatment with TreatmentQuery.countActive(); a difference holds the publish (DL25).
7. FreshnessStampService: on a match, writes the DP04 stamp for business date D.
8. Case owner or restructuring officer: reads DP04 for a case through GET /data-products/DP04/records?caseId=.
9. Data steward: reads the DP04 catalog entry and any breaks.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without a DP04 access row reads the product | 403; refusal logged | MSG-P4-002 | AC3 |
| X2 | A guarantee claim names a case that does not exist | Claim held in the exception list with check References; retried with the next load | None | AC4 |
| X3 | TreatmentQuery is unavailable | Step fails; the previous DP04 rows and stamp stay; DP04 turns stale at its expected-by time | MSG-GEN-006, MSG-P1-001 | AC5 |
| X4 | The step runs again for the same business date | Rows replaced by record ID; no duplicate | None | AC6 |
| X5 | Active treatment counts differ | DP04 not stamped for D; break listed for the data steward | MSG-P1-002 | AC7 |
| X6 | A treatment changed at the end of business date D | Included in D; a change one second later goes to D+1 | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the treatment entity (RWB-E2-004), product access (RWB-E1-016) and freshness (RWB-E1-015); the guarantee interface may return no rows |
| Negotiable | Which roles read DP04 and the expected-by time are data rows; the story fixes the build, the link checks and the stamp |
| Valuable | The Epic 3 settlement, TDR and DIL screens read one checked store |
| Estimable | One job step, two read tables, two interface calls, one reconciliation |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments and claims through stub interfaces |

### 7. Acceptance criteria

```gherkin
Feature: Stage 2 data products: contracts, plans and treatments

  Background:
    Given business date 2026-12-14 and the COLLINS load for it passed its checks at 06:20
    Given the treatment module holds 40 active treatments, 12 of them restructure plans with installments from the ACE restructure calculation
    Given 9 of the 12 plans carry a credit approval recorded on the case by the restructuring officer

  Scenario: AC1 Products loaded
    Given treatments and plans in the case store, with credit approvals recorded from NLEADS by the officer
    When the stage 2 step of JOB-01 runs
    Then dp_treatment holds 40 rows for business date 2026-12-14, each with treatment type, approval level, installments, outcome and the contract number of the case's primary account
    Then DP04 carries a freshness stamp for business date 2026-12-14 with status "LOADED"
    Then the catalog entry for DP04 lists system of record "Workbench", owner RW-DATASTEW and the fields of treatment and guarantee_claim

  Scenario: AC2 Guarantee data
    Given 5 TCG guarantee claim records for 5 existing cases, claimed amounts from 180,000.00 to 1,250,000.00 baht
    When the stage 2 step runs
    Then dp_guarantee_claim holds 5 rows, each linked to its case
    Then a read of DP04 for case "RW-2026-000512" returns its TCG claim with claim deadline 2027-02-28

  Scenario: AC3 Access
    Given user "u-phone-02" holds RW-PHONECOL, which has no DP04 access row
    When the user calls GET /data-products/DP04/records?caseId=RW-2026-000512
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system logs the refusal with user "u-phone-02" and product "DP04"

  Scenario: AC4 A guarantee claim for a case that does not exist
    Given a TCG claim names case ID "00000000-0000-0000-0000-000000000997"
    When the stage 2 step runs
    Then the system does not writ the claim to dp_guarantee_claim
    Then the data quality exception list holds it with product "DP04" and check "References"

  Scenario: AC5 The treatment interface is unavailable
    Given TreatmentQuery returns an error
    When the stage 2 step runs for 2026-12-14
    Then the step ends "FAILED" with MSG-GEN-006 for system "Treatment"
    Then dp_treatment keeps the rows for 2026-12-13
    Then the system flags at 08:00 DP04 stale with MSG-P1-001 "Treatment is from 2026-12-13. Today's load has not arrived."

  Scenario: AC6 A repeat run for the same date
    Given the stage 2 step completed for 2026-12-14 with 40 treatment rows
    When it runs again for 2026-12-14
    Then dp_treatment still holds 40 rows for 2026-12-14

  Scenario: AC7 Active treatment counts differ
    Given TreatmentQuery.countActive() returns 41 and the build produced 40 active rows
    When the count check runs
    Then the system does not stamp DP04 for 2026-12-14
    Then a break with check "Active treatment count 40 against 41" is listed for the data steward with MSG-P1-002

  Scenario: AC8 A change at the end of the business date
    Given treatment "TRT-SYN-0601" changed at 2026-12-14T23:59:59+07:00 and treatment "TRT-SYN-0602" changed at 2026-12-15T00:00:00+07:00
    When the stage 2 step runs for 2026-12-14
    Then "TRT-SYN-0601" is in the build for 2026-12-14
    Then "TRT-SYN-0602" is not
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | DP04 holds treatments, plan terms, contract references and guarantee claims, with one system of record and one owner | REQ-RDF-014; data_product DP04; sys_objects |
| BR2 | Every stage 2 row links to an existing case, or it is held in the exception list and retried with the next load | DQ load check "References" (ifspec.txt) |
| BR3 | The product is stamped for the day only when the active count matches the owning module, with zero tolerance | DL25; RWB-E1-011 hold rule (FEAT-RDF-13) |
| BR4 | A role reads DP04 only through an access row in force | data_product_access; REQ-RDF-010 |
| BR5 | Credit approval for a restructure is recorded on the case by the officer; there is no interface to NLEADS | INT-26; DL12 |
| BR6 | Plan installments come from the ACE restructure calculation | DF-TRT-009 source ACE; INT-34 |

### 9. State transitions

None. This story does not change a case status. It changes the DP04 freshness status (LOADED or STALE) and the state of the stage 2 step on the JOB-01 run (Complete or Failed).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Runs the stage 2 step, writes dp_treatment and dp_guarantee_claim, writes exceptions and the stamp |
| RW-DATASTEW, data steward | Owns DP04; reads the catalog entry and the breaks |
| RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD | Read DP04 for cases in scope |
| RW-COE, RW-AUDIT | Read DP04 for all cases |
| RW-PHONECOL and roles with no DP04 access row | May not read DP04 |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-005 | treatment | proposed_by | Read |
| DF-TRT-006 | treatment | proposed_at | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-008 | treatment | haircut_amount | Read |
| DF-TRT-009 | treatment | installments | Read |
| DF-TRT-010 | treatment | valid_until | Read |
| DF-TRT-011 | treatment | approval_level | Read |
| DF-TRT-012 | treatment | booked_at | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-014 | treatment | outcome_at | Read |
| DF-TRT-015 | guarantee_claim | id | Read |
| DF-TRT-016 | guarantee_claim | case_id | Read |
| DF-TRT-017 | guarantee_claim | claim_type | Read |
| DF-TRT-018 | guarantee_claim | claim_deadline | Read |
| DF-TRT-019 | guarantee_claim | claimed_amount | Read |
| DF-TRT-020 | guarantee_claim | filed_at | Read |
| DF-TRT-021 | guarantee_claim | paid_amount | Read |
| DF-TRT-022 | guarantee_claim | status | Read |
| DF-ACC-003 | loan_account | contract_no | Read |
| DF-ACC-007 | loan_account | contract_date | Read |
| DF-TRT-034 to DF-TRT-051 | dp_treatment | all fields | Write |
| DF-TRT-052 to DF-TRT-061 | dp_guarantee_claim | all fields | Write |
| DF-OPS-001 to DF-OPS-009 | data_product_load | all fields | Write |

treatment and guarantee_claim fields are read through TreatmentQuery and GuaranteeClaimQuery, not from their tables. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Job step**

| Item | Value |
|---|---|
| Trigger | End of JOB-01 after the COLLINS load for business date D passes its checks |
| Job name | JOB-01 COLLINS load check and intake, stage 2 product step |
| Schedule | Daily, after the COLLINS load, before 07:00 (NFR-013) |
| Input | Treatments and guarantee claims changed on D through the published interfaces; contract number and date of each case's primary account |
| Output | dp_treatment and dp_guarantee_claim rows for D; exceptions with check References; DP04 freshness stamp; count check result on the job run |
| Events published | None |
| Idempotency key | Record ID and business date; a rerun replaces the rows for D |
| Restart behavior | The step writes in one transaction per product table; a failure leaves the previous day's rows; rerun from the job monitor with POST /admin/jobs/{jobId}/rerun |

**Published interfaces used**

```java
// Treatment module (RWB-E2-004)
public interface TreatmentQuery {
    List<TreatmentView> changedBetween(OffsetDateTime from, OffsetDateTime to);
    long countActive();
}

// Guarantee module (S3); returns an empty list until Epic 4
public interface GuaranteeClaimQuery {
    List<GuaranteeClaimView> changedBetween(OffsetDateTime from, OffsetDateTime to);
}

// P3 (RWB-E1-016), service call without a user scope
CaseLinks CaseScopeQuery.linksInScope(UUID caseId, UserContext systemContext);
```

**Endpoints used**

| Method and path | Use | Authorization | Errors |
|---|---|---|---|
| GET /api/recovery/v1/data-products/{productCode}/records | Read DP04 for a case (RWB-E1-016) | Case record, R, plus a DP04 access row | 403 (MSG-P4-002); 404 (MSG-P4-003); 503 (MSG-GEN-006) |
| GET /api/recovery/v1/admin/data-quality/exceptions | Read DP04 References exceptions and breaks | Platform administration, R | 401; 403; 503 |
| POST /api/recovery/v1/admin/jobs/{jobId}/rerun | Rerun the failed step | Platform administration, U | 404; 409 (MSG-P2-006) |

### 13. Solution plan

- Package: folder `recovery/dataengine/stage2`, Java package `recovery.dataengine.stage2`.

| Component | Type | Responsibility |
|---|---|---|
| Stage2ProductStep | Job | The stage 2 step of JOB-01 |
| Stage2ProductService | Service | Reads changes through the interfaces, resolves contracts, checks links, writes rows, runs the count check |
| DpTreatmentRepository, DpGuaranteeClaimRepository | Repository | Upsert by record ID and business date |
| DpTreatment, DpGuaranteeClaim | Entity | One row per record and business date |
| DP04 access rows | Rule table | data_product_access rows for DP04, version DPA-2026.12 |

- Database: tables dp_treatment and dp_guarantee_claim (new, Flyway migration in this story). dp_treatment mirrors the 14 treatment fields and adds business_date date, contract_no varchar(20), contract_date date; dp_guarantee_claim mirrors the 8 guarantee_claim fields and adds business_date date; both carry the standard columns, a unique key (record ID, business_date) and an index on case_id. Writes data_product_load for DP04 (RWB-E1-015) and exceptions (RWB-E1-006). Reads loan_account (P1).
- Configuration and reference data: DP04 row in data_product with expected-by 08:00 (assumed; DL11); DP04 access version DPA-2026.12 prepared by the data steward and loaded by the reference data administrator; dictionary rows for dp_treatment and dp_guarantee_claim added to sys_fields with the migration.
- Build steps:
  1. Flyway migration for dp_treatment and dp_guarantee_claim, with their sys_objects and sys_fields rows under DP04.
  2. Stage2ProductService reading changes for D through TreatmentQuery and GuaranteeClaimQuery; the business date window is [start of D, start of D+1).
  3. Contract resolution through CaseScopeQuery and loan_account.
  4. Link check with the References exception, and upsert of the other rows.
  5. Count check against countActive(); hold the stamp on a difference.
  6. Stamp DP04 through FreshnessStampService on a match.
  7. Stage2ProductStep wired into JOB-01 after the load checks.
  8. Tests for AC1 to AC8 with stub interfaces, and the access test.
- Feature flag: `rwb.dataengine.stage2-products`.
- Done when: the tests in section 16 pass and the DP04 catalog entry shows in GET /admin/data-products in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | Role without a DP04 access row | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | DP04 stale after a failed step | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Count check break held the publish | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | TreatmentQuery or GuaranteeClaimQuery unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | Rerun while JOB-01 is running | {job} is already running. Wait for it to finish before you rerun it. |

Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-45 Data quality (Epic 2): state Loading while the list arrives; state Breaks shows DP04 References exceptions and count breaks for the data steward. The case record view SCR-03 shows DP04 data for roles with access. The settlement, TDR and DIL screens that use DP04 come in Epic 3.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-010-01 | AC1, BR1, BR5, BR6 | System | 40 synthetic treatments, 12 plans, 9 approvals |
| TC-E2-010-02 | AC2, BR1 | System | 5 TCG claims for existing cases |
| TC-E2-010-03 | AC3, BR4 | System | RW-PHONECOL reads DP04 |
| TC-E2-010-04 | AC4, BR2 | System | TCG claim for an unknown case ID |
| TC-E2-010-05 | AC5 | System | TreatmentQuery stub returning errors |
| TC-E2-010-06 | AC6 | System | Step run twice for 2026-12-14 |
| TC-E2-010-07 | AC7, BR3 | System | countActive() 41 against 40 rows |
| TC-E2-010-08 | AC8 | System | Changes at 23:59:59 and 00:00:00 |
| TC-E2-010-09 | Access | Access | RW-TRIBE calls GET /admin/data-quality/exceptions; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: access, expected-by time and tolerance are data rows or decisions (DL25).
- No personal data in logs, tests or prompts: treatment and claim rows carry amounts and codes; test data is synthetic.
- No read of another module's tables: treatments and claims come through TreatmentQuery and GuaranteeClaimQuery; case links through CaseScopeQuery.
- No call to NLEADS or the Thai Credit Guarantee Corporation; their results arrive as recorded on the case.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Business Requirements Epic 2, sections 3.1 and 4 | FEAT-CHO-09 | 07 Route, settle and claim | DL25; DL12 | TC-E2-010-01 to TC-E2-010-08 |

### 19. Out of scope

- The treatment entity and its plan timers (RWB-E2-004).
- The credit approval pack for NLEADS (RWB-E2-006) and booking confirmation from the ALS load (RWB-E2-007).
- Settlement, TDR and DIL screens (Epic 3).
- Guarantee claim filing and the claim deadline timers (S3, Epic 4).


---

## RWB-E2-011 Queue view screens: my queue, team queues, filters and ageing

| Item | Value |
|---|---|
| Story key | RWB-E2-011 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-WKM-01 Show my queue with filters and ageing; FEAT-WKM-02 Show team queues |
| Requirement IDs | REQ-WKM-001, REQ-WKM-002, REQ-WKM-006 |
| BRD section | Business Requirements Epic 2, sections 3.3 and 4; Business Requirements Program, section 5.3 |
| L3 process | 06 Take over and own the case |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-020, RWB-E1-031 |
| Status | Ready for build |

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **screens for my queue and my team's queues with filters by stage, route, status and age, sorted by service level**, so that **every person sees their work in one place and the team manager sees the team's load**.

### 2. Business rationale

Cases are run from team spreadsheets and the team manager learns of a late case from email. With about 23,600 open cases at go-live (NFR-001), a case owner needs their own list ordered by the next service level date, and the team manager needs each queue's depth, oldest case and breaches without a report request. This story gives both views on the case list and the team queues screen. It meets REQ-WKM-001, REQ-WKM-002 and REQ-WKM-006. The measure is that the team queue counts equal the case list counts for the same team every day.

### 3. Preconditions

- RWB-E1-020 is done: every case has a queue and an owner by rule.
- RWB-E1-031 is done: the case list (SCR-02) shows queue and owner with filters by queue, team and status, and the export.
- RWB-E1-028 is done: each assigned case has a SERVICE_LEVEL timer.
- Queues are loaded with their team, role and caseload cap (RWB-E1-019; cap values DL23, assumed 150).
- The signed-in person holds RW-CASEOWN (scope Own) or RW-TEAMMGR (scope Team) with the scope set by RWB-E1-037.
- The COLLINS load for the business date has passed its checks, or the case list shows its date as stale.

### 4. Flow

1. Case owner: opens My queue from the menu.
2. Front end: calls `GET /cases` with `owner=me`, `sort=serviceLevelDueAt` and the filters kept for the session.
3. Case service: applies the scope, the filters and the sort; returns one page of cases with age, status and service level state.
4. Front end: shows the list in state List, or Empty with MSG-P3-017.
5. Case owner: sets the stage filter to Litigation; the front end keeps the filter in session storage and reloads the list in state Filtered.
6. Team manager: opens Team queues from the menu.
7. Front end: calls `GET /queues`.
8. Queue service: returns each queue in the manager's teams with the open case count, the oldest entry date, the breach count and the open cases per owner against the cap.
9. Team manager: selects a queue; the front end calls `GET /queues/{queueId}/cases` and shows the cases sorted by service level.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The person has no case in scope for the filters | Empty state | MSG-P3-017 | AC4 |
| X2 | Age from is greater than age to | The request is refused; the list is not reloaded | MSG-GEN-003 | AC5 |
| X3 | Page size above 200 | The request is refused | MSG-GEN-002 | AC6 |
| X4 | A team manager opens a queue of another team | Not found | MSG-P4-003 | AC7 |
| X5 | Today's COLLINS load has not arrived | The list shows with the stale banner and the date of the data | MSG-P1-001 | AC8 |
| X6 | A case's service level timer is paused by a deviation | The case shows "Paused" and sorts after running timers | MSG-P3-004 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads the case, queue and timer rows that Epic 1 already writes |
| Negotiable | Columns and filter order can change; the sort and the counts are fixed |
| Valuable | Each person works one ordered list; the team manager sees load and breaches |
| Estimable | Two endpoints extended, one endpoint used, two screens |
| Small | Fits in one sprint with its tests |
| Testable | API tests on a seeded database and browser tests on both screens |

### 7. Acceptance criteria

```gherkin
Feature: Queue view screens: my queue, team queues, filters and ageing

  Background:
    Given the business date is 2026-12-15
    Given team "MTG-BKK" has queues "MTG-BKK-CO" and "MTG-BKK-LIT" with a caseload cap of 150
    Given user "U-CO-01" holds RW-CASEOWN in team "MTG-BKK" and user "U-TM-01" holds RW-TEAMMGR for team "MTG-BKK"

  Scenario: AC1 My queue
    Given "U-CO-01" owns 40 open cases, 3 with an expired service level timer and 37 with running timers
    When "U-CO-01" opens My queue
    Then 40 cases list in one page
    Then the 3 breached cases come first, then the 37 by service level due date, earliest first
    Then each row shows the case number, product group, stage, status, age in days from the entry date and the service level due date

  Scenario: AC2 Team view
    Given "MTG-BKK-CO" holds 412 open cases with the oldest entered on 2026-09-02 and 9 breaches
    Given "MTG-BKK-LIT" holds 38 open cases with the oldest entered on 2026-10-20 and 0 breaches
    When "U-TM-01" opens Team queues
    Then "MTG-BKK-CO" shows count 412, oldest case age 104 days and 9 breaches
    Then "MTG-BKK-LIT" shows count 38, oldest case age 56 days and 0 breaches
    Then each owner in "MTG-BKK-CO" shows their open case count against the cap of 150

  Scenario: AC3 Filter
    Given "U-CO-01" owns 12 open cases on stage "LITIGATION" and 28 on other stages
    When the stage filter is set to "LITIGATION" and the list refreshes
    Then only the 12 litigation cases show
    Then after "U-CO-01" opens a case and returns to My queue the filter is still "LITIGATION"
    Then after sign-out and sign-in the filter is cleared

  Scenario: AC4 Empty queue
    Given "U-CO-02" owns no open case
    When "U-CO-02" opens My queue
    Then the screen shows the empty state with MSG-P3-017

  Scenario: AC5 Age range in the wrong order
    When "U-CO-01" sets age from 120 and age to 90
    Then the system refuses the request with MSG-GEN-003 naming "age to" and "age from"
    Then the list keeps its previous rows

  Scenario: AC6 Page size above the limit
    When the front end requests My queue with page size 500
    Then the system refuses the request with MSG-GEN-002 naming "size", 1 and 200

  Scenario: AC7 Queue of another team
    Given queue "SME-NTH-CO" belongs to team "SME-NTH"
    When "U-TM-01" requests the cases of "SME-NTH-CO"
    Then the system does not find the response with MSG-P4-003

  Scenario: AC8 Stale data
    Given the COLLINS load of 2026-12-15 has not arrived and the case data is from 2026-12-14
    When "U-CO-01" opens My queue
    Then the 40 cases show with the stale banner MSG-P1-001 naming the date 2026-12-14

  Scenario: AC9 Paused service level
    Given 2 of the 40 cases have a deviation "X1" open and their service level timers paused
    When "U-CO-01" opens My queue
    Then the 2 cases show "Paused" with MSG-P3-004 on hover and sort after the 37 running timers

  Scenario: AC10 Age boundary
    Given case "RW-2026-000301" entered on 2026-09-16 and case "RW-2026-000302" entered on 2026-09-17
    When "U-CO-01" sets age from 90 and age to 90
    Then only "RW-2026-000301" shows, with age 90 days

  Scenario: AC11 Counts reconcile to the case list
    When "U-TM-01" reads the count of "MTG-BKK-CO" on Team queues and the case list filtered by queue "MTG-BKK-CO" and status not "CLOSED"
    Then both show 412

  Scenario: AC12 Load time
    Given "U-CO-01" owns 500 open cases
    When "U-CO-01" opens My queue with page size 200
    Then the first page shows within 2 seconds at the 95th percentile over 20 runs
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | My queue shows the open cases whose owner is the signed-in person; Team queues shows only the queues of the manager's teams | roles.txt default scope (Own, Team); CTL-09 |
| BR2 | Sort order: breached service level first, then running by due date earliest first, then paused, then no service level timer | REQ-WKM-001; R-UNI-30 |
| BR3 | Age is the number of calendar days from the case entry date to the business date | DF-CAS-013; labels.txt Stage clock |
| BR4 | A breach is an open case whose SERVICE_LEVEL timer has status EXPIRED | R-UNI-30; REQ-CWC-011 |
| BR5 | The open case count of a queue is its cases with status not Closed, and equals the case list count for the same queue | REQ-WKM-006; NFR-018 |
| BR6 | An owner at or above the queue's caseload cap is shown at cap | Queue field capacity_cap; DL23 |
| BR7 | A timer paused by a deviation shows as paused; the prescription date keeps running | R-DEV-01; R-UNI-43 |
| BR8 | Filters are kept for the browser session only and are not stored on the server | Principle 1 (no business value stored per user) |

### 9. State transitions

None. This story does not change a case status. It reads cases, queues and timers only.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Opens My queue (Case record R, scope Own); reads queue rows of own queue (Queue and allocation R) |
| RW-TEAMMGR, team manager | Opens Team queues and My queue (Queue and allocation R, Case record R, scope Team) |
| RW-CAPACITY, capacity and workforce planner | Opens Team queues (Queue and allocation R, scope All) |
| RW-RESTRUCT, RW-LITOFF | Open My queue for the cases they own (Case record R) |
| RW-AUDIT, internal audit | Reads both views (R, scope All); changes nothing |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-006 | recovery_case | stage_code | Read |
| DF-CAS-008 | recovery_case | route_code | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-011 | recovery_case | team_code | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-003 | queue | queue_name | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-028 | timer | case_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-032 | timer | expires_at | Read |
| DF-WRK-034 | timer | paused | Read |
| DF-WRK-035 | timer | status | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /cases** (P3)

| Item | Value |
|---|---|
| Request | Query: `owner` (`me` or a user ID), `stage`, `route` (new), `status`, `ageFrom`, `ageTo`, `queue`, `page` (default 0), `size` (default 50, 1 to 200), `sort` (`serviceLevelDueAt` new; default for My queue) |
| Response | 200 `CasePage`: `items[]` of `Case` with the new computed fields `ageDays`, `serviceLevelDueAt`, `serviceLevelState` (BREACHED, RUNNING, PAUSED, NONE); `page`, `size`, `total`; header `X-Data-As-Of` with the business date of the case data |
| Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 422 age range in the wrong order (MSG-GEN-003) or size outside 1 to 200 (MSG-GEN-002); 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

**GET /queues** (P3)

| Item | Value |
|---|---|
| Request | None |
| Response | 200 `Queue[]` with the new computed fields `openCaseCount`, `oldestEntryDate`, `oldestAgeDays`, `breachCount`, `owners[]` (`ownerUserId`, `openCaseCount`, `atCap`) |
| Errors | 401; 403 no Queue and allocation R (MSG-P4-002); 503 |
| Authorization | Queue and allocation, right R, scope applied (queues of the caller's teams) |
| Idempotency | Not applicable |

**GET /api/recovery/v1/queues/{queueId}/cases** (P3)

| Item | Value |
|---|---|
| Request | Path `queueId`; query `page`, `size` (1 to 200), `sort` (`serviceLevelDueAt`) |
| Response | 200 `CasePage` as above |
| Errors | 401; 403 (MSG-P4-002); 404 queue unknown or outside scope (MSG-P4-003); 422 size (MSG-GEN-002); 503 |
| Authorization | Queue and allocation, right R, scope applied |
| Idempotency | Not applicable |

### 13. Solution plan

**Package.** `recovery.casewf.queueview` in the recovery module; front end folder `src/modules/recovery/casewf/queues`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseListQueryService | Service | Builds the scoped case query with filters, age and the service level sort; computes `ageDays` and `serviceLevelState` |
| QueueSummaryService | Service | Counts open cases, oldest entry date, breaches and open cases per owner for each queue in scope |
| CaseListRepository | Repository | One SQL query joining `recovery_case` with the SERVICE_LEVEL `timer` of each case |
| QueueSummaryRepository | Repository | Grouped counts by `queue_id` and `owner_user_id` |
| CaseAndWorkflowController | Controller | The three endpoints; parameter checks; problem responses |
| MyQueuePage | React component | SCR-02 in the My queue view with filters, sort and states |
| TeamQueuesPage | React component | SCR-07 with the queue rows, owner spread and drill down |
| useSessionFilters | React component | Hook that keeps filters in session storage, wrapped in try and catch, cleared at sign-out |

**Database.** Reads `recovery_case`, `queue` and `timer`. Uses `ix_case_owner_status`, `ix_case_status_queue` and `ix_timer_case_id`. Adds index `ix_timer_case_type_status` on `timer (case_id, timer_type, status)` in migration `V<next>__rwb_e2_011_queue_view_index.sql`.

**Configuration and reference data.** Page size limits (`queueview.page-size.default` 50, `queueview.page-size.max` 200) in the configuration service, loaded by the platform administrator. Stage, route and status labels from LOV-STAGE, LOV-ROUTE and LOV-CASE-STATUS through the P4 list interface. Caseload caps from the queue table (DL23).

**Build steps**

1. Add the index migration and `CaseListRepository` with the service level join; test the four sort groups.
2. Build `CaseListQueryService` with scope, filters, age and the new computed fields; add `route` and the sort to `GET /cases`.
3. Build `QueueSummaryService` and the computed fields on `GET /queues`; test the counts against `GET /cases` for the same queue.
4. Add the scope check to `GET /queues/{queueId}/cases`.
5. Build `MyQueuePage` with Loading, Empty, List and Filtered states and `useSessionFilters`.
6. Build `TeamQueuesPage` with Loading and List states and the drill down.
7. Add the stale banner from `X-Data-As-Of` and the paused marker.
8. Write the API, browser and load tests in section 16.

**Feature flag.** `rwb.p3.queue-views`. Off: the menu items My queue and Team queues are hidden and the endpoints return the Epic 1 fields only.

**Done when.** The tests in section 16 pass, and the browser accessibility check (RWB-TE-010) passes on both screens.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-017 | The list has no case for the person and filters | There are no cases in this queue. |
| MSG-GEN-003 | Age to is less than age from | {field} cannot be before {other}. |
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-P4-003 | A queue outside the caller's scope | This case is not in your scope. |
| MSG-P1-001 | The case data is from an earlier business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-004 | A case on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P4-002 | A role without the right opens a view | You cannot {action} here. Your role does not include it. |

MSG-P3-017 is new (see Additions). Thai text follows DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-02 Case list, My queue view | Loading | Sees skeleton rows |
| SCR-02 Case list, My queue view | Empty | Reads MSG-P3-017 |
| SCR-02 Case list, My queue view | List | Reads cases sorted by service level; opens a case on SCR-03 |
| SCR-02 Case list, My queue view | Filtered | Sets stage, route, status and age filters; clears them |
| SCR-07 Team queues | Loading | Sees skeleton rows |
| SCR-07 Team queues | List | Reads count, oldest age, breaches and owners against the cap; opens a queue's cases; goes to SCR-05 Transfer case (RWB-E2-012) |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-011-01 | AC1, BR1, BR2, BR3 | System | 40 cases for U-CO-01: 3 breached, 37 running |
| TC-E2-011-02 | AC2, BR4, BR6 | System | Queues MTG-BKK-CO (412 cases) and MTG-BKK-LIT (38 cases) |
| TC-E2-011-03 | AC3, BR8 | System | 12 litigation and 28 other cases; browser session kept and ended |
| TC-E2-011-04 | AC4 | System | U-CO-02 with no case |
| TC-E2-011-05 | AC5 | System | Age from 120, age to 90 |
| TC-E2-011-06 | AC6 | System | Page size 500 |
| TC-E2-011-07 | AC7, BR1 | System | Queue SME-NTH-CO requested by a MTG-BKK manager |
| TC-E2-011-08 | AC8 | System | Data as of 2026-12-14 on business date 2026-12-15 |
| TC-E2-011-09 | AC9, BR7 | System | Two cases with X1 open and paused timers |
| TC-E2-011-10 | AC10, BR3 | System | Entry dates 2026-09-16 and 2026-09-17 |
| TC-E2-011-11 | AC11, BR5 | System | Queue count against the case list count |
| TC-E2-011-12 | AC12 | System | 500 cases, 20 timed runs |
| TC-E2-011-13 | Access | Access | RW-WRITEOFF (no Queue and allocation right) calls `GET /queues`; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. Caps, page sizes, labels and list values are read from the queue table, the configuration service and the lists.
- No personal data in logs, tests or prompts. Rows show case numbers and codes; party names follow the masking rules of RWB-E1-037. Test data is synthetic.
- No read of another module's tables. List labels come through the P4 interface; deviation details come through the S8 interface.
- Browser storage holds only the filter values and is wrapped in try and catch; the page works without it.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-01 | 06 Take over and own the case | R-UNI-30 | TC-E2-011-01, TC-E2-011-03 to TC-E2-011-06, TC-E2-011-08 to TC-E2-011-10, TC-E2-011-12 |
| REQ-WKM-002 | A team manager sees every queue in the team with filters | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-02 | 06 Take over and own the case | R-UNI-30 | TC-E2-011-02, TC-E2-011-07, TC-E2-011-13 |
| REQ-WKM-006 | Queue counts, ageing and breaches reconcile to the case list | Business Requirements Epic 2, section 4; Program, section 5.3 | FEAT-WKM-02 | 06 Take over and own the case | R-UNI-30 | TC-E2-011-02, TC-E2-011-11 |

### 19. Out of scope

- The export of the case list (RWB-E1-031).
- Transfer and reassignment from the team queues screen (RWB-E2-012).
- Partner work in the same queue view (REQ-WKM-011, partner placements in Epic 6).
- The daily queue measures in Power BI (RWB-E1-030).
- The next action column (RWB-E2-035).


---

## RWB-E2-012 Manual transfer and reassignment screen with reason

| Item | Value |
|---|---|
| Story key | RWB-E2-012 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-WKM-03 Transfer a case manually with a reason; FEAT-WKM-04 Reassign a case to another owner; FEAT-WKM-10 Reallocate when an owner is unavailable |
| Requirement IDs | REQ-WKM-003, REQ-WKM-007, REQ-WKM-008 |
| BRD section | Business Requirements Epic 2, sections 3.3 and 4; Business Requirements Program, section 5.3 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-021, RWB-E2-011 |
| Status | Ready for build |

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a screen to transfer a case to another queue or reassign it to a person, with a reason code required and the transfer rules checked**, so that **a hand-off is one action with a record, not an email**.

### 2. Business rationale

Today ownership changes are agreed by email, and audit found debtors who met the criteria were not transferred to the responsible unit (CTL-03). A manual move must carry a coded reason, respect the caseload cap and the transfer rules, keep the case's state and clocks, and leave a decision log entry. This story gives the team manager one screen for a single or a bulk move. It meets REQ-WKM-003, REQ-WKM-007 and REQ-WKM-008. The measure is that every manual move has an assignment record with a reason code and a decision log entry.

### 3. Preconditions

- RWB-E1-021 is done: the transfer rule table and engine evaluate a manual transfer and return the rule row that allows or refuses it.
- RWB-E2-011 is done: team queues and the case list open SCR-05 for a case or a selection.
- RWB-E1-020 is done: `AssignmentEngine` picks an owner in a queue by its method and caseload cap.
- The decision log writer (RWB-E1-027) is available through the P7 interface.
- LOV-TRANSFER-REASON (new, see Additions) is loaded with the agreed reason codes. Assumed values: R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral, R06 Wrong queue (DL23).
- The person holds RW-TEAMMGR or RW-CAPACITY (Queue and allocation U) and the case is in their scope.

### 4. Flow

1. Team manager: opens SCR-05 Transfer case from SCR-03 Case record or from a selection on SCR-07 Team queues.
2. Team manager: chooses a target queue or a target owner, a reason code and an optional note, and confirms.
3. Front end: calls `POST /cases/{caseId}/transfer` with a new Idempotency-Key per case.
4. Transfer service: checks the reason code, that the case is open and not under a legal hold, and the scope.
5. Rules component: evaluates the transfer rule table for the case, the target and the reason; returns the allowing rule row or the refusing rule ID.
6. Transfer service: for a queue transfer, asks `AssignmentEngine` for the owner by the target queue's method; for a reassignment, checks the target owner is below the cap and, for reason R04, in the case's team.
7. Transfer service: writes the decision log entry through the P7 interface; on success, in one transaction ends the current assignment, writes the new assignment with reason, rule ID, queue and reason code, updates the case queue, owner and team, and writes CaseTransferred (EV-04) to the outbox.
8. Front end: shows state Saved with MSG-GEN-005; for a bulk move, one result per case and the summary.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No reason code | Refused; nothing changes | MSG-P3-001 | AC4 |
| X2 | A transfer rule row refuses the move | Refused with the rule ID | MSG-P3-033 | AC2 |
| X3 | The target owner is at the caseload cap, or every owner of the target queue is | At cap warning; refused | MSG-P3-002 | AC5 |
| X4 | Reason R04 and the target owner is outside the case's team | Refused naming R-UNI-18 | MSG-P3-033 | AC6 |
| X5 | The case is closed or under a legal hold | Refused | MSG-P3-005 | AC7 |
| X6 | Two transfers of one case at the same time | One succeeds; the other is refused | MSG-GEN-004 | AC8 |
| X7 | The same request is sent twice with the same Idempotency-Key | The first result is returned; no second record | None | AC9 |
| X8 | The decision log write fails | Nothing changes | MSG-P7-003 | AC10 |
| X9 | Some cases in a bulk move are refused | The others move; each refused case shows its message | MSG-P3-035 | AC11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the transfer engine and the assignment engine of Epic 1; adds the screen and the coded reason |
| Negotiable | Reason codes and the bulk limit are data; the checks are fixed |
| Valuable | Ends ownership changes by email; every move has a record |
| Estimable | One endpoint extended, one service, one screen |
| Small | Fits in one sprint with its tests |
| Testable | API tests on a seeded database and a browser test of SCR-05 |

### 7. Acceptance criteria

```gherkin
Feature: Manual transfer and reassignment screen with reason

  Background:
    Given the business date is 2026-12-15
    Given user "U-TM-01" holds RW-TEAMMGR for team "MTG-BKK"
    Given case "RW-2026-000401" in queue "MTG-BKK-CO" owned by "U-CO-01", status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    Given queue "LIT-BKK-01" uses "ROUND_ROBIN" with a caseload cap of 150 and owners "U-LO-01" with 80 cases and "U-LO-02" with 95 cases, next in turn "U-LO-02"

  Scenario: AC1 Transfer
    Given case "RW-2026-000401" in a queue of team "MTG-BKK"
    When "U-TM-01" transfers it to queue "LIT-BKK-01" with reason "R02" Customer deceased
    Then the case is in queue "LIT-BKK-01" with owner "U-LO-02"
    Then the previous assignment of "U-CO-01" has ended at the time of the transfer
    Then a new assignment has reason "TRANSFER", reason code "R02", queue "LIT-BKK-01" and the transfer rule ID
    Then one decision log entry holds the rule ID, the rule version, the from and to queue and owner and the reason code
    Then the case keeps status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    Then one CaseTransferred event is in the outbox

  Scenario: AC2 Rule blocks
    Given case "RW-2026-000402" with deviation "X1" open and owned by the complaint officer under rule "R-DEV-02"
    When "U-TM-01" tries to transfer it to queue "LIT-BKK-01" with reason "R05"
    Then the screen refuses with MSG-P3-033 naming rule "R-DEV-02"
    Then the case, its assignment and the decision log are unchanged

  Scenario: AC3 Bulk
    Given ten selected cases in queue "MTG-BKK-CO" owned by "U-CO-01"
    When "U-TM-01" reassigns them to owner "U-CO-03" with 60 open cases and reason "R04"
    Then all ten have owner "U-CO-03"
    Then ten assignments and ten decision log entries are written
    Then "U-CO-03" holds 70 open cases

  Scenario: AC4 No reason
    When "U-TM-01" submits a transfer of "RW-2026-000401" with no reason code
    Then the system refuses the transfer with MSG-P3-001
    Then nothing changes

  Scenario: AC5 Owner at the cap
    Given owner "U-CO-04" holds 150 open cases in queue "MTG-BKK-CO" with a cap of 150
    When "U-TM-01" reassigns "RW-2026-000401" to "U-CO-04" with reason "R01"
    Then the screen shows the at cap warning with MSG-P3-002 naming "U-CO-04"
    Then nothing changes

  Scenario: AC6 Absence reassignment outside the team
    Given owner "U-CO-09" belongs to team "SME-NTH"
    When "U-TM-01" reassigns "RW-2026-000401" to "U-CO-09" with reason "R04"
    Then the system refuses the transfer with MSG-P3-033 naming rule "R-UNI-18"

  Scenario: AC7 Case under legal hold
    Given case "RW-2026-000403" with legal hold true
    When "U-TM-01" transfers it to queue "LIT-BKK-01" with reason "R05"
    Then the system refuses the transfer with MSG-P3-005 naming "LIT-BKK-01" and "HELD_LEGAL"

  Scenario: AC8 Two transfers at once
    When "U-TM-01" and "U-TM-02" transfer "RW-2026-000401" to different queues in the same second
    Then the case ends in exactly one queue with one new assignment
    Then the system refuses the other request with MSG-GEN-004

  Scenario: AC9 Repeated request
    Given the AC1 transfer was made with Idempotency-Key "5b0c7a1e-0000-4000-8000-000000000001"
    When the same request is sent again with the same Idempotency-Key
    Then the response is the same assignment
    Then there is still one new assignment and one decision log entry

  Scenario: AC10 Decision log write fails
    Given the decision log store is unavailable
    When "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02"
    Then the system refuses the transfer with MSG-P7-003
    Then the case stays in queue "MTG-BKK-CO" with owner "U-CO-01" and no new assignment

  Scenario: AC11 Bulk with refusals
    Given ten selected cases, two of which are under a legal hold
    When "U-TM-01" reassigns them to "U-CO-03" with reason "R01"
    Then eight cases move
    Then the two held cases show MSG-P3-005
    Then the summary shows MSG-P3-035 with 8 of 10

  Scenario: AC12 Every owner of the target queue at the cap
    Given both owners of queue "LIT-BKK-01" hold 150 open cases
    When "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R05"
    Then the screen shows the at cap warning with MSG-P3-002 naming every owner of "LIT-BKK-01"
    Then nothing changes
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A manual move needs a reason code from LOV-TRANSFER-REASON | REQ-WKM-003; REQ-CWC-010 |
| BR2 | A move the transfer rule table refuses is not made, and the refusing rule ID is shown | REQ-CWC-010; RWB-E1-021 |
| BR3 | A queue transfer takes its owner from the target queue's assignment method | Queue field assignment_method; RWB-E1-020 |
| BR4 | An owner at or above the queue's cap cannot receive a case | Queue field capacity_cap; DL23 |
| BR5 | A reassignment for an absent owner stays inside the case's team | R-UNI-18 |
| BR6 | A move keeps the case status, route state, stage clock and timers | R-UNI-18; R-UNI-46 |
| BR7 | A case under a legal hold or closed is not moved | R-UNI-20 |
| BR8 | A move that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR9 | A repeated request with the same Idempotency-Key has no further effect | R-UNI-40 |
| BR10 | A case with an open deviation stays with the owner the deviation rule named | R-DEV-02; R-DEV-03 |

### 9. State transitions

None. This story does not change a case status. It changes the case's queue, owner and team, ends one assignment and writes the next. The route state and the clocks stay as they were (R-UNI-18, R-UNI-46).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Transfers and reassigns cases in the team's scope (Queue and allocation CRUA) |
| RW-CAPACITY, capacity and workforce planner | Reassigns cases for capacity (Queue and allocation RU, scope All) |
| SY-CASEWF, case workflow module | Writes the assignment and updates the case (Queue and allocation CRU) |
| SY-RULES, rules component | Evaluates the transfer rule table |
| SY-DECLOG, decision log writer | Writes the entry (Decision log C) |
| RW-CASEOWN, case owner | Reads the result only (Queue and allocation R); cannot transfer |

No approval level from the delegation of authority applies: a transfer moves work, not money.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-007 | recovery_case | route_state | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Write |
| DF-CAS-010 | recovery_case | queue_id | Write |
| DF-CAS-011 | recovery_case | team_code | Write |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-006 | queue | assignment_method | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Write |
| DF-WRK-039 | assignment | queue_id | Write |
| DF-WRK-040 | assignment | transfer_reason_code | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through the P7 interface |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /cases/{caseId}/transfer** (P3)

| Item | Value |
|---|---|
| Request | Header `Idempotency-Key` (uuid, required). Body `TransferRequest`: `toQueueId` or `toOwnerId` (one required), `reasonCode` (TRANSFER for a queue move, MANUAL for a reassignment), `transferReasonCode` (new, LOV-TRANSFER-REASON, required), `note` (max 500) |
| Response | 200 `Assignment`: `id`, `caseId`, `assigneeUserId`, `assignedAt`, `reason`, `ruleId` |
| Errors | 401 (MSG-P4-001); 403 no Queue and allocation U (MSG-P4-002); 404 case unknown or out of scope (MSG-P4-003); 409 case closed or held (MSG-P3-005), rule refuses (MSG-P3-033), record changed (MSG-GEN-004); 422 no reason (MSG-P3-001), owner at cap (MSG-P3-002); 503 decision log write failed (MSG-P7-003) |
| Authorization | Queue and allocation, right U, scope applied |
| Idempotency | `Idempotency-Key` header, kept 24 hours. A repeat returns the stored response |

**GET /api/recovery/v1/cases/{caseId}** (P3) reads the case after the move (Case record R).

**Published interfaces used**

```java
// P3, RWB-E1-020
Optional<UUID> AssignmentEngine.pickOwner(UUID queueId, UUID caseId, LocalDate businessDate);
// P3 rules component, RWB-E1-021
TransferDecision TransferRules.evaluate(UUID caseId, UUID toQueueId, UUID toOwnerId, String transferReasonCode);
// P7, RWB-E1-027
UUID DecisionLogWriter.record(DecisionLogEntryCommand command);
```

**Events.** CaseTransferred (EV-04) published with caseId, fromOwner, toOwner, reasonCode, in the same transaction as the change.

### 13. Solution plan

**Package.** `recovery.casewf.transfer` in the recovery module; front end folder `src/modules/recovery/casewf/transfer`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAndWorkflowController | Controller | `POST /cases/{caseId}/transfer`; idempotency; problem responses |
| ManualTransferService | Service | Checks, rule call, owner pick, decision log write, then the transaction |
| IdempotencyStore | Repository | Stores the key, the request hash and the response for 24 hours |
| AssignmentRepository | Repository | Ends the current assignment and writes the new one |
| OwnerLoadRepository | Repository | Counts open cases per owner in a queue for the cap check |
| TransferCasePage | React component | SCR-05 with the Form, At cap warning and Saved states, single and bulk |
| BulkTransferRunner | React component | Sends one request per selected case in sequence and collects the results |

**Database.** Migration `V<next>__rwb_e2_012_assignment_reason.sql` adds `assignment.queue_id uuid REFERENCES queue (id)` and `assignment.transfer_reason_code varchar(10)`, index `ix_assignment_case_open` on `(case_id) WHERE ended_at IS NULL`, and the idempotency table `idempotency_key (key uuid PK, endpoint varchar(100), request_hash char(64), response jsonb, created_at timestamptz)`. The case update uses the optimistic lock column `recovery_case.version`.

**Configuration and reference data.** LOV-TRANSFER-REASON values (center of excellence; DL23). `transfer.bulk.max` = 50 (assumed; DL23). The transfer rule table rows (center of excellence, RWB-E1-021). Queue caps (DL23).

**Build steps**

1. Write the migration and extend the assignment entity.
2. Build `IdempotencyStore` and the header handling in the controller.
3. Build `ManualTransferService` checks in this order: reason, case state and hold, scope, transfer rules, owner pick or cap check, team check for R04.
4. Add the decision log write before the transaction; map its failure to 503 with MSG-P7-003.
5. Write the transaction: end assignment, new assignment, case update with the version check, outbox row.
6. Build `TransferCasePage` with its three states and `BulkTransferRunner` with the per-row result and the MSG-P3-035 summary.
7. Write the tests in section 16, including two parallel requests.

**Feature flag.** `rwb.p3.manual-transfer`. Off: SCR-05 is hidden and the endpoint returns 403 for every role except SY-CASEWF.

**Done when.** The tests in section 16 pass, and a transfer made in SIT shows on the case timeline queue history (RWB-E2-016).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | No reason code | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner, or every owner of the target queue, at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Case closed or under a legal hold | This case cannot move to {state} from {current}. |
| MSG-P3-033 | A transfer rule refuses the move | Rule {rule} does not allow this transfer. |
| MSG-P3-035 | Bulk move with refusals | {done} of {total} cases were moved. The others show the reason on their row. |
| MSG-GEN-004 | Two moves of one case at once | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-005 | Move saved | Saved. |
| MSG-P4-002 | A role without Queue and allocation U | You cannot {action} here. Your role does not include it. |

MSG-P3-033 and MSG-P3-035 are new (see Additions). Thai text follows DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-05 Transfer case | Form | Chooses a queue or an owner, a reason code and a note; confirms |
| SCR-05 Transfer case | At cap warning | Reads MSG-P3-002; chooses another owner or the team queue |
| SCR-05 Transfer case | Saved | Reads MSG-GEN-005, or the per-case results and MSG-P3-035 for a bulk move |
| SCR-07 Team queues | List | Selects up to 50 cases and opens SCR-05 for them |
| SCR-09 Exception queue | List | Not used by this story; a refused move is not queued |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-012-01 | AC1, BR1, BR3, BR6 | System | RW-2026-000401 to LIT-BKK-01, reason R02 |
| TC-E2-012-02 | AC2, BR2, BR10 | System | RW-2026-000402 with X1 open under R-DEV-02 |
| TC-E2-012-03 | AC3, BR4, BR5 | System | Ten cases to U-CO-03 with 60 open cases, reason R04 |
| TC-E2-012-04 | AC4, BR1 | System | Request with no reason code |
| TC-E2-012-05 | AC5, BR4 | System | U-CO-04 at 150 of 150 |
| TC-E2-012-06 | AC6, BR5 | System | U-CO-09 in team SME-NTH, reason R04 |
| TC-E2-012-07 | AC7, BR7 | System | RW-2026-000403 with legal hold true |
| TC-E2-012-08 | AC8 | System | Two parallel requests for one case |
| TC-E2-012-09 | AC9, BR9 | System | Same Idempotency-Key twice |
| TC-E2-012-10 | AC10, BR8 | System | Decision log store stopped |
| TC-E2-012-11 | AC11 | System | Ten cases, two under a legal hold |
| TC-E2-012-12 | AC12, BR4 | System | Both LIT-BKK-01 owners at 150 |
| TC-E2-012-13 | Access | Access | RW-CASEOWN (Queue and allocation R) calls the transfer endpoint; refused with MSG-P4-002 |
| TC-E2-012-14 | Principle 5 | Resilience | Decision log write forced to fail; case, assignment and outbox unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. Reason codes, caps, the bulk limit and the transfer rules are data.
- No personal data in logs, tests, events or prompts. The note field is not logged; events carry IDs and codes only.
- No read of another module's tables. The decision log is written through the P7 interface; deviation ownership comes from the transfer rule table and the case flag.
- The decision log entry is written before the case changes; a failed write leaves the case as it was.
- Each case in a bulk move is its own request and its own transaction.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-003 | Manual transfer or reassignment only with a reason code from the agreed list | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-DEV-02, R-UNI-20, R-UNI-39, R-UNI-40 | TC-E2-012-01, TC-E2-012-02, TC-E2-012-04, TC-E2-012-07 to TC-E2-012-10, TC-E2-012-13, TC-E2-012-14 |
| REQ-WKM-007 | An absent or over-cap owner's cases reallocated inside the team, keeping state and clocks | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-04, FEAT-WKM-10 | All recovery processes | R-UNI-18, R-UNI-46 | TC-E2-012-03, TC-E2-012-05, TC-E2-012-06, TC-E2-012-11, TC-E2-012-12 |
| REQ-WKM-008 | Queue and transfer history visible on the case | Business Requirements Epic 2, section 4; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-UNI-18 | TC-E2-012-01, TC-E2-012-03 |

### 19. Out of scope

- Automatic reallocation when an owner is absent or over the cap (R-UNI-18 and R-UNI-19, JOB-06 Daily rebalancing, RWB-E1-030).
- The queue history view on the case (RWB-E2-016).
- Rule-driven transfers on stage change, route decision and timer expiry (RWB-E1-021).
- Partner placement and recall (Epic 6).


---

## RWB-E2-013 Approval routing with the delegation of authority table

| Item | Value |
|---|---|
| Story key | RWB-E2-013 |
| Epic | E2, release 31 December 2026 |
| Module | P7 Decision center and log |
| Feature | FEAT-APD-01 Route a recommendation to the approver by limit; FEAT-APD-02 Approve inside the limit; FEAT-APD-03 Change a recommendation before approving; FEAT-APD-04 Reject a recommendation with a reason; FEAT-APD-05 Escalate above the limit; FEAT-APD-06 Escalate an overdue approval; FEAT-APD-07 Record an override with a coded reason; FEAT-APD-09 Show the approval queue; FEAT-APD-10 Apply the delegation of authority limits; FEAT-APD-11 Record the outcome of an approved decision |
| Requirement IDs | REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010, REQ-APD-011 |
| BRD section | Business Requirements Epic 2, section 3.7; Business Requirements Program, section 5.7 |
| L3 process | 17 Run the decision center |
| Decision | D7.1 |
| Priority | Must |
| Depends on | RWB-E1-038, RWB-E1-028, RWB-E1-027, RWB-E1-037 |
| Status | Ready for build |

### 1. Story

As an **approver, for example a product head (RW-PRODHEAD)**, I want **every decision that needs approval routed to the approval level the delegation of authority table names, or to the role named for a decision with no amount limit, with one queue of what waits on me and escalation when an item passes its service level**, so that **the right person approves within the limit, nobody approves their own decision, and no item waits unseen**.

### 2. Business rationale

Approval and authority governance is an audit finding: approvals today are given by e-mail, sometimes above the approver's limit or by the person who prepared the decision. This story routes each approval by the versioned delegation table (RWB-E1-038), records the limit, the rule version and the approver with every outcome, refuses an approval above the caller's limit or by its preparer, and escalates rather than stalls when the service level passes or no holder exists. It meets REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010 and REQ-APD-011 and puts controls CTL-04, CTL-05 and CTL-07 in place. The measure is decisions within the delegation of authority: target 100 percent.

### 3. Preconditions

- RWB-E1-038 is done: delegation version DOA-2026.11 is in force and the lookup returns the lowest covering level; holders and substitutes are named test users in SIT and UAT (DL18).
- RWB-E1-028 is done: the P3 timer engine starts service level timers, and JOB-05 publishes EV-19 TimerBreached.
- RWB-E1-027 is done: the decision log writer; RWB-E1-037 is done: the permission matrix and scope.
- Approval route parameters are in the catalog for each decision with no amount limit, for D7.1 notices: rwb.approval.route.D7.1.area=LITIGATION, rwb.approval.route.D7.1.role=RW-LITOFF, rwb.approval.route.D7.1.escalation-role=RW-HEADLIT, rwb.approval.route.D7.1.service-level=1 working day (assumed; DL22).
- Service level for limit-based approvals: rwb.approval.service-level.default=3 working days (assumed from the 3 working day approval timers in R-RES-10 and R-SET-05; DL22).
- Capability area per decision code: D5 and D6.x Treatment and offer, D7.x Litigation, D8.2 and D8.3 Asset and disposal, D8.4 Debt sale, D9.x Write-off and posting (parameters rwb.approval.area.<code>).
- LOV-OVERRIDE-REASON is loaded with the coded override reasons (owner RW-COE; new list, recorded in the additions file).

### 4. Flow

1. Calling module (for example the litigation route after R-LIT-03 generates a notice): calls ApprovalRouter.request with the case, decision, regulation item, product, amounts, preparer, source reference and the rule ID and version that asked for approval.
2. Workbench (ApprovalRoutingService): for a decision with delegation rows, calls DelegationOfAuthority.lowestLevel and assigns the item to the holder of that level; for a decision with no amount limit, assigns it to the route role from the parameters.
3. Workbench: where the level has no holder and no substitute, moves the item one level up at once and records why; where the lookup returns NOT_COVERED, holds the item and raises the incident.
4. Workbench: stores the approval with status WAITING, the level, the delegation row and version, and the due time; asks P3 to open the decision task and start the service level timer; writes the routing entry to the decision log; publishes EV-09 ApprovalRequested.
5. Approver: opens SCR-10 Approval queue (GET /approvals) and sees the items waiting on them with decision, amount, level, limit and age.
6. Approver: approves, changes and approves, refuses or returns the item through the approval endpoints.
7. Workbench (ApprovalDecisionService): checks the A letter in the decision's capability area, the caller's level against the required level, that the caller did not prepare the item, the reason or coded reason where needed, and the record version.
8. Workbench: writes the decision entry with approver, approval level, limit version, rule ID and version and final call; sets the approval status; publishes EV-08 DecisionRecorded; P3 moves the case from Waiting approval to In progress and the source module acts (for a notice, release to dispatch, RWB-E2-014).
9. Workbench (ApprovalEscalationListener): on EV-19 TimerBreached for an approval, moves the item one level up, or to the escalation role for a role-routed item, restarts the timer, writes the escalation entry and tells the new approver.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The service level passes with no action | The item moves to the next level up or the escalation role; the case does not move; entry written | MSG-P7-011 | AC2 |
| X2 | The caller prepared the decision | Refused with 409 | MSG-P7-002 | AC6 |
| X3 | A change raises the amount above the caller's level | Not approved; the item is sent to the level that covers it | MSG-P7-001 | AC7 |
| X4 | Refuse or return without a reason | Refused with 422 | MSG-GEN-001 | AC8 |
| X5 | A change departs from the recommendation without a coded reason | Refused with 422 | MSG-P7-005 | AC10 |
| X6 | The required level has no holder and no substitute | The item moves one level up at once; it never waits on nobody | MSG-P7-011 | AC11 |
| X7 | A committee level is approved without a resolution reference or the members present | Refused with 422 | MSG-GEN-001 | AC12 |
| X8 | Two approvers act on one item at once | One succeeds; the other gets 409 and writes nothing | MSG-GEN-004 | AC13 |
| X9 | No delegation row covers the decision and product | The item is held; incident to Risk | MSG-P7-010 | AC14 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the delegation lookup (RWB-E1-038), timers (RWB-E1-028), the writer (RWB-E1-027) and the matrix (RWB-E1-037) |
| Negotiable | Levels, holders, route roles, service levels and override reasons are data |
| Valuable | Every Epic 2 approval follows the delegation table and is recorded with its limit |
| Estimable | One router, one decision service, one escalation listener, one queue screen |
| Small | Fits in two weeks with its tests; the notice screen is RWB-E2-014 |
| Testable | Each criterion below is one test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Approval routing with the delegation of authority table

  Background:
    Given the environment is SIT
    Given delegation version "DOA-2026.11" is in force with holder "U-9201" at L6, "U-9202" at L5 and "U-9203" at L4 for MORTGAGE, all holding RW-PRODHEAD
    Given test user "U-9210" holds RW-RESTRUCT and test users "U-9211" and "U-9212" hold RW-LITOFF and test user "U-9213" holds RW-HEADLIT

  Scenario: AC1 Routed
    Given a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211"
    When the router runs for decision D7.1 at 09:00 on 14 December 2026
    Then an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026
    Then the system does not show it to "U-9211", who prepared it
    Then the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role"
    Then the case status becomes "Waiting approval"

  Scenario: AC2 Escalated
    Given the approval of AC1 is still WAITING at 09:00 on 15 December 2026
    When JOB-05 publishes TimerBreached for its service level timer
    Then the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026
    Then the system writes one entry with final call "ESCALATED" and "U-9213" is told with MSG-P7-011
    Then the case stays "Waiting approval"

  Scenario: AC3 Limit changed
    Given approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11"
    Given version "DOA-2027.01" from 1 January 2027 moves that amount to L5
    When a new D6.4 approval with the same amounts routes on 2 January 2027
    Then the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01"
    Then approval "A-1" stays with L6 and "DOA-2026.11"

  Scenario: AC4 Routed by limit
    Given restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00
    When the router runs
    Then the system assigns the approval to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11"
    Then GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age

  Scenario: AC5 Approve inside the limit
    Given the approval of AC4 is WAITING
    When "U-9201" approves it with Idempotency-Key "k-501"
    Then the approval status becomes "APPROVED"
    Then the system writes one entry with approver "U-9201", approval level "L6", limit version "DOA-2026.11", the rule ID and version and final call "APPROVED"
    Then the system publishes decisionRecorded and the response shows MSG-P7-004 with state "In progress"

  Scenario: AC6 The preparer cannot approve
    Given "U-9210" also holds RW-PRODHEAD at L6 as substitute
    When "U-9210" approves the approval of AC4
    Then the system refuses the call with status 409 and message MSG-P7-002 and the approval stays "WAITING"

  Scenario: AC7 A change above the limit goes up
    Given the approval of AC4 is WAITING with "U-9201"
    When "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves
    Then the call returns MSG-P7-001 with level "L5" and approver "U-9202"
    Then the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded

  Scenario: AC8 Refuse needs a reason
    Given the approval of AC4 is WAITING
    When "U-9201" refuses it with no reason
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "reason"
    Then when "U-9201" refuses it with reason "Collateral appraisal older than one year"
    Then the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names

  Scenario: AC9 Return with a question
    Given the approval of AC4 is WAITING
    When "U-9201" returns it with reason "Attach the latest income statement"
    Then the system opens the status becomes "RETURNED", a task for preparer "U-9210", and the entry records the question

  Scenario: AC10 An override needs a coded reason
    Given the recommendation on the approval of AC4 is a settlement of 1,920,000.00
    When "U-9201" changes it to 1,800,000.00 and approves with no reason code
    Then the system refuses the call with status 422 and message MSG-P7-005

  Scenario: AC11 No holder means escalation, not a stall
    Given the L6 row for SSME has no holder and no substitute
    When an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes
    Then the system assigns it to the L5 holder at once
    Then the routing entry records reason "NO_HOLDER" for L6

  Scenario: AC12 A committee level needs the resolution
    Given an approval for D6.4 item 2.1.1, MORTGAGE, principal 800,000,000.00, loss 20.00 percent, routed to L3, Problem Asset Resolution Committee, whose recording holder is "U-9204"
    When "U-9204" approves it with no resolution reference
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "resolutionReference"
    Then when "U-9204" approves with resolution reference "PARC-2026-14" and members present "M-01, M-02, M-03, M-04"
    Then the entry records the resolution reference, the members present, level "L3" and final call "APPROVED"

  Scenario: AC13 Two approvals at once
    Given the approval of AC4 is WAITING and visible to holder "U-9201" and substitute "U-9205"
    When both approve it at the same moment
    Then one call succeeds and one entry is written
    Then the other call returns status 409 with message MSG-GEN-004

  Scenario: AC14 No limit covers the decision
    Given "DOA-2026.11" holds no row for HIRE_PURCHASE
    When an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes
    Then the system stores the approval with status "HELD_NO_LIMIT" and the case stays "Waiting approval"
    Then the system raises an incident to RW-RISK with message MSG-P7-010
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A decision with delegation rows routes to the lowest level whose row covers it on the routing date; the item keeps that delegation version | REQ-APD-001; REQ-APD-010; RWB-E1-038; Delegation of authority matrix, rule 9 |
| BR2 | A decision with no amount limit routes to the role named in its route parameters, for D7.1 notices RW-LITOFF | Parameters rwb.approval.route.*; DL22 |
| BR3 | The approver must hold the A letter in the decision's capability area and be the holder or substitute of the required level, or hold the route role | Permission matrix; Key sheet: A works within the delegation table; CTL-04 |
| BR4 | A person may not approve a decision they proposed or prepared | Admin and access model, section 6.2; CTL-05; Delegation of authority matrix, rule 10 |
| BR5 | An approval above the caller's level is refused and sent to the level that covers it, with no silent approval | REQ-APD-004; R-UNI-15 |
| BR6 | A change from the recommendation needs a coded reason; refuse and return need a reason | REQ-APD-005; R-UNI-14; CTL-07 |
| BR7 | An approval not answered inside its service level escalates one level up, or to the escalation role; the case does not move | REQ-APD-007; R-UNI-30; R-UNI-42 |
| BR8 | A level with no holder and no substitute passes the item one level up at once | REQ-APD-011 |
| BR9 | Levels L1 to L3 approve by committee resolution; the entry records the resolution reference, the date and the members present | REQ-APD-008; doa.txt, Levels sheet |
| BR10 | The limit, the rule version and the approver are written with every approval | REQ-APD-009; FEAT-DRI-04 |
| BR11 | A decision that no limit covers is held and raises an incident | Delegation of authority matrix, rule 8 |
| BR12 | An approval outcome that cannot be written to the decision log does not take effect | Principle 5; R-UNI-39 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| In progress | Recommendation routed for approval | Approval stored WAITING or HELD_NO_LIMIT | Waiting approval |
| Waiting approval | Approver accepts | Caller within the required level, not the preparer | In progress |
| Waiting approval | Approver changes and accepts | Changed terms within the caller's level, coded reason given | In progress |
| Waiting approval | Approver rejects | Reason given | In progress, at the state the rule names |
| Waiting approval | SLA_BREACHED (R-UNI-30) | Service level timer breached | Waiting approval, with the next approver |

The approval record moves WAITING to APPROVED, REFUSED or RETURNED, and stays WAITING with a new approver on escalation or on a change above the limit.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Holders and substitutes of levels L4 to L6 (named per DL18) | Approve, change, refuse or return items at their level in the Workbench |
| Recording holder of levels L1 to L3 | Records the committee resolution with its reference and members present |
| RW-LITOFF Litigation officer, RW-LEGAL Legal counsel, RW-HEADLIT Head of Litigation | Approve D7.x items routed to their role (Litigation A) |
| RW-PRODHEAD Product head | Approves items of their product at their level (A in Treatment and offer, Litigation, Asset and disposal, Debt sale, Write-off and posting) |
| RW-RESTRUCT, RW-CREDCOMM | Approve Treatment and offer items at their level (A) |
| RW-SALEOFF, RW-HEADNPA, RW-HEADASL, RW-DEBTSALE | Approve Asset and disposal or Debt sale items at their level (A) |
| RW-CREDITAD, RW-WOCOMM, RW-FINANCE | Approve Write-off and posting items at their level (A) |
| Preparer of an item | May not approve it |
| SY-RULES, SY-CASEWF | Call the router (Decision log C) |
| RW-AUDIT | Reads approvals through the decision log |
| Approval levels | L1 Board of Directors to L6 Recovery executive, department level, per doa.txt |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-032 | approval | id | Write |
| DF-DEC-033 | approval | case_id | Write |
| DF-DEC-034 | approval | decision_code | Write |
| DF-DEC-035 | approval | regulation_item | Write |
| DF-DEC-036 | approval | capability_area | Write |
| DF-DEC-037 | approval | route_role_code | Write |
| DF-DEC-038 | approval | approval_level | Write |
| DF-DEC-039 | approval | delegation_limit_id | Write |
| DF-DEC-040 | approval | limit_version | Write |
| DF-DEC-041 | approval | product_group | Write |
| DF-DEC-042 | approval | amount | Write |
| DF-DEC-043 | approval | terms | Write |
| DF-DEC-044 | approval | prepared_by | Write |
| DF-DEC-045 | approval | assigned_user_id | Write |
| DF-DEC-046 | approval | status | Write |
| DF-DEC-047 | approval | due_at | Write |
| DF-DEC-048 | approval | escalation_level | Write |
| DF-DEC-049 | approval | source_type | Write |
| DF-DEC-050 | approval | source_ref | Write |
| DF-DEC-051 | approval | rule_id | Write |
| DF-DEC-052 | approval | rule_version | Write |
| DF-DEC-053 | approval | decision_log_id | Write |
| DF-REF-018 | delegation_limit | approval_level | Read through the P4 DelegationOfAuthority interface |
| DF-REF-023 | delegation_limit | holder_user_id | Read through the P4 DelegationOfAuthority interface |
| DF-REF-024 | delegation_limit | substitute_user_id | Read through the P4 DelegationOfAuthority interface |
| DF-WRK-019 | task | task_code | Write through the P3 task interface |
| DF-WRK-020 | task | element_type | Write through the P3 task interface |
| DF-WRK-023 | task | owner_role | Write through the P3 task interface |
| DF-WRK-030 | timer | timer_type | Write through the P3 timer interface |
| DF-WRK-032 | timer | expires_at | Write through the P3 timer interface |
| DF-WRK-036 | timer | escalation_level | Read from EV-19 |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (routing, escalation and outcome entries) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/approvals** (API-P7-002)

| Item | Value |
|---|---|
| Request | Query: decision, product, page, size |
| Response | ApprovalPage of Approval: id, caseId, decision, preparedBy, level, amount, status |
| Errors | 401; 403 no A letter in any decision area (MSG-P4-002); 503 (MSG-GEN-006) |
| Authorization | api.yaml declares Decision log A, which no bank role holds; the A letter in the decision's capability area is checked instead (additions file) |
| Idempotency | Not applicable, read only |

**GET /approvals/{approvalId}** (new, additions file): Approval plus regulationItem, limitVersion, ruleId, ruleVersion, dueAt, escalationLevel, sourceType, sourceRef, terms; errors 401, 403, 404 (MSG-P4-003).

**POST /approvals/{approvalId}/approve** (API-P7-003)

| Item | Value |
|---|---|
| Request | ApprovalAction: reason, resolutionReference; added in this story: reasonCode (LOV-OVERRIDE-REASON), changes (the changed terms), membersPresent |
| Response | 200 DecisionLogEntry of the approval |
| Errors | 401; 403 no A in the area or not the holder, substitute or route role (MSG-P4-002); 404 (MSG-P4-003); 409 preparer (MSG-P7-002), above the caller's level (MSG-P7-001, the item has moved), record changed (MSG-GEN-004); 422 missing reason code, resolution reference or members (MSG-P7-005, MSG-GEN-001); 503 entry not written (MSG-P7-003) |
| Authorization | A in the decision's capability area, plus level or route role |
| Idempotency | Idempotency-Key header |

**POST /api/recovery/v1/approvals/{approvalId}/refuse** (API-P7-005): ApprovalAction with reason required; response DecisionLogEntry; errors as approve; Idempotency-Key.

**POST /api/recovery/v1/approvals/{approvalId}/return** (API-P7-004): ApprovalAction with reason required; response Approval with status RETURNED; errors as approve; Idempotency-Key.

**Events:** publishes EV-09 ApprovalRequested (approvalId, caseId, level, amount) and EV-08 DecisionRecorded; consumes EV-19 TimerBreached.

**Published interface ApprovalRouter** (package recovery.decision.approval):

```java
ApprovalRef request(ApprovalRequest request) throws DecisionLogUnavailableException;
// ApprovalRequest: caseId, decisionCode, regulationItem, productGroup, amounts (principal, lossPct, lossAmount, pricePctFmv),
//   recommendation, preparedBy, sourceType, sourceRef, ruleId, ruleVersion, idempotencyKey
```

### 13. Solution plan

- Package: folder `recovery/decision/approval` in the recovery module; Java package `recovery.decision.approval`. Front end: `recovery/decision/approval`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| DecisionCenterAndLogController | Controller | GET /approvals, GET /approvals/{approvalId}, approve, refuse, return |
| ApprovalRouter | Published interface | The request method above |
| ApprovalRoutingService | Service | Lookup or route role, no-holder rule, store, P3 task and timer, routing entry, EV-09 |
| ApprovalDecisionService | Service | BR3 to BR6 and BR9 checks, entry, status, EV-08 |
| ApprovalEscalationListener | Listener | EV-19 for approval timers; next level or escalation role; restart timer; entry; notification |
| ApprovalRepository | Repository | Reads and writes the approval table with optimistic locking |
| Approval | Entity | Maps the new approval table |
| ApprovalQueueScreen | React component | SCR-10 Approval queue: decision, case, amount, level, limit, age, due |

- Database: creates table approval (id uuid, case_id uuid, decision_code varchar(8), regulation_item varchar(10), capability_area varchar(30), route_role_code varchar(20), approval_level varchar(4), delegation_limit_id uuid, limit_version varchar(20), product_group varchar(15), amount numeric(18,2), terms jsonb, prepared_by uuid, assigned_user_id uuid, status varchar(20), due_at timestamptz, escalation_level integer default 0, source_type varchar(20), source_ref varchar(60), rule_id varchar(20), rule_version varchar(20), decision_log_id uuid, plus the standard columns) with Flyway migration V_E2_013__approval.sql; index ix_approval_assignee on (assigned_user_id, status); index ix_approval_role on (route_role_code, status); unique index on (source_type, source_ref) where status in ('WAITING','HELD_NO_LIMIT').
- Configuration and reference data: delegation version (RWB-E1-038; holders DL18); route, area and service level parameters (owner RW-COE; values DL22); LOV-OVERRIDE-REASON (RW-COE); notification template for MSG-P7-011 on the ACE notification path.
- Build steps:
  1. Create the approval migration, entity and repository with optimistic locking.
  2. Build ApprovalRoutingService for limit-based and role-based routes, the no-holder rule and the NOT_COVERED hold; tests for AC1, AC4, AC11, AC14.
  3. Wire the P3 task and timer interfaces and EV-09; test the case status in AC1.
  4. Build ApprovalDecisionService for approve, change, refuse and return with all checks; tests for AC5 to AC10 and AC12.
  5. Add idempotency and the concurrency test for AC13.
  6. Build ApprovalEscalationListener; test AC2 with a fixed clock.
  7. Test the version change for AC3 with two delegation versions.
  8. Build SCR-10 with the loading and list states and the queue endpoint.
- Feature flag: `rwb.decision.approval-routing`.
- Done when: the tests in section 16 pass and CTL-04 and CTL-05 tests (approve above the limit, approve own decision) pass in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-001 | Approval above the caller's level | This needs approval at level {level}. It has been sent to {approver}. |
| MSG-P7-002 | Preparer tries to approve | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | Entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-004 | Approved | Approved. The case moves to {state}. |
| MSG-P7-005 | Change from the recommendation without a coded reason | Enter the reason you are not following the recommendation. |
| MSG-P7-010 | No limit covers the decision and product | No approval limit covers {decision} for {product}. The item is held and Risk has been told. |
| MSG-P7-011 | Item escalated to a new approver (new) | {decision} on case {caseNo} passed its service level and is now with you for approval. |
| MSG-GEN-001 | Reason, resolution reference or members present missing | Enter {field}. |
| MSG-GEN-004 | Item changed by another approver | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | No A letter in the decision's area | You cannot {action} here. Your role does not include it. |

Thai text for each message follows DL10; proposed Thai for MSG-P7-011 is in the additions file.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-10 Approval queue | Loading | Waits while the items load |
| SCR-10 Approval queue | List | Sees each item waiting on them with decision, case, amount, level, limit version, age and due time; opens an item in SCR-11 |
| SCR-10 Approval queue | Empty (common state) | Sees that nothing is waiting |

SCR-11 Decision screen is built for its first use, the D7.1 notices, in RWB-E2-014.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-013-01 | AC1, BR2 | System | Synthetic demand notice under R-LIT-03 |
| TC-E2-013-02 | AC2, BR7 | System | Approval timer breached at 09:00 next day |
| TC-E2-013-03 | AC3, BR1 | System | Delegation versions DOA-2026.11 and DOA-2027.01 |
| TC-E2-013-04 | AC4, BR1 | System | D6.4 Mortgage at 2.4 million baht |
| TC-E2-013-05 | AC5, BR3, BR10 | System | L6 holder approving |
| TC-E2-013-06 | AC6, BR4 | System | Preparer who is also a substitute |
| TC-E2-013-07 | AC7, BR5 | System | Principal changed to 120 million baht |
| TC-E2-013-08 | AC8, BR6 | System | Refuse without and with a reason |
| TC-E2-013-09 | AC9, BR6 | System | Return with a question |
| TC-E2-013-10 | AC10, BR6 | System | Change without a reason code |
| TC-E2-013-11 | AC11, BR8 | System | SSME L6 row with no holder |
| TC-E2-013-12 | AC12, BR9 | System | L3 committee approval with resolution PARC-2026-14 |
| TC-E2-013-13 | AC13 | System | Holder and substitute approving at once |
| TC-E2-013-14 | AC14, BR11 | System | Hire purchase with no delegation rows |
| TC-E2-013-15 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E2-013-16 | Principle 5 | Resilience | The decision log write forced to fail during an approval |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: levels, limits, holders, route roles, areas, service levels and override reasons are data or parameters.
- No personal data in logs, tests or prompts; members present are recorded as member references, not names.
- No read of another module's tables: delegation through the P4 interface, tasks and timers through P3, source actions through the source module's interface.
- No approval without its decision log entry in the same transaction.
- No item may be assigned to its preparer.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-001 | Route to the approver named by the delegation table | Epic 2, 3.7 | FEAT-APD-01, FEAT-APD-10 | 17 Run the decision center | BR1, BR2 | TC-E2-013-01, TC-E2-013-04 |
| REQ-APD-003 | Accept, change, reject or return, each recorded | Epic 2, 3.7 | FEAT-APD-02, FEAT-APD-03, FEAT-APD-04 | 17 Run the decision center | BR3, BR6 | TC-E2-013-05, TC-E2-013-08, TC-E2-013-09 |
| REQ-APD-004 | Above the limit refused and raised, no silent approval | Epic 2, 3.7 | FEAT-APD-05 | 17 Run the decision center | BR4, BR5 | TC-E2-013-06, TC-E2-013-07 |
| REQ-APD-005 | Override needs a coded reason | Epic 2, 3.7 | FEAT-APD-07 | 17 Run the decision center | BR6 | TC-E2-013-10 |
| REQ-APD-007 | Unanswered approval escalates to the named role | Epic 2, 3.7 | FEAT-APD-06 | 17 Run the decision center | BR7 | TC-E2-013-02 |
| REQ-APD-008 | Committee decision recorded with members present | Epic 2, 3.7 | FEAT-APD-07 | 17 Run the decision center | BR9 | TC-E2-013-12 |
| REQ-APD-009 | Limit, rule version and approver written with every approval | Epic 2, 3.7 | FEAT-APD-11 | 17 Run the decision center | BR10, BR12 | TC-E2-013-05, TC-E2-013-13, TC-E2-013-16 |
| REQ-APD-010 | Open items keep the delegation version they were decided under | Epic 2, 3.7 | FEAT-APD-10 | 17 Run the decision center | BR1 | TC-E2-013-03, TC-E2-013-14 |
| REQ-APD-011 | Routing escalates rather than stalls with no person in a role | Epic 2, 3.7 | FEAT-APD-06 | 17 Run the decision center | BR8 | TC-E2-013-11 |

### 19. Out of scope

- The decision screen SCR-11 and the D7.1 notice approval with release to dispatch (RWB-E2-014).
- The committee pack screen SCR-12 with each member's vote (Epic 4).
- The recommendation with reasons and expected return by route (Epic 4, API-P7-001).
- The monthly override reason report (Epic 8, FEAT-ADM-08 QA sample; reporting stories).
- Names of level holders and substitutes (DL18) and service level values (DL22).


---

## RWB-E2-014 Approval screen for D7.1 demand and recall notices

| Item | Value |
|---|---|
| Story key | RWB-E2-014 |
| Epic | E2, release 31 December 2026 |
| Module | P7 Decision center and log, with P6 Communications |
| Feature | FEAT-APD-08 Approve demand and recall notices |
| Requirement IDs | REQ-APD-002, REQ-APD-006 |
| BRD section | Business Requirements Epic 2, section 3.7; Business Requirements Program, section 5.7 |
| L3 process | 8.1 Prepare pre-litigation |
| Decision | D7.1 |
| Priority | Must |
| Depends on | RWB-E2-013, RWB-E1-052 |
| Status | Ready for build |

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **one screen that shows the generated demand or recall notice, the case facts it was built from with their age, and the rule and version that proposed it, with approve, change or reject and a reason**, so that **the first decision in the Workbench runs with a person approving, and only an approved notice goes to dispatch**.

### 2. Business rationale

A demand fee notice sent to customers incomplete is a Bank of Thailand finding, and a wrong amount or address on a notice can void the notice period and delay litigation. Today notices are checked on paper with no record of who approved what. This story is the first production use of approval routing: the notice generated by rule R-LIT-03 waits for a litigation officer who did not prepare it, the officer sees the notice and its inputs on one screen, and the decision is recorded with the rule version and the approver before the notice can be dispatched. It meets REQ-APD-002 and REQ-APD-006 and supports controls CTL-05 and CTL-14. The measure is notices sent with an approval entry: target 100 percent.

### 3. Preconditions

- RWB-E2-013 is done: D7.1 approvals route to role RW-LITOFF with a 1 working day service level and escalate to RW-HEADLIT.
- RWB-E1-052 is done: NoticeApi generates DEMAND and RECALL notices from the current Approved template with state Generated and raises EV-13 NoticeGenerated.
- Templates DEMAND-MTG and DEMAND-MTG-B (a second Approved variant of the demand notice for Mortgage) and RECALL-MTG are Approved in language TH.
- Input age limits are parameters: rwb.decision.input-age-days.TOTAL_BALANCE=1, rwb.decision.input-age-days.POSTAL_ADDRESS=30 (assumed; owner RW-COE; DL22).
- LOV-OVERRIDE-REASON holds TEMPLATE_VARIANT and WRONG_PARTY (owner RW-COE).
- Test users in SIT hold RW-LITOFF; one holds RW-LEGAL; one holds RW-CASEOWN.

### 4. Flow

1. Notice module (P6): on EV-13 NoticeGenerated for a DEMAND or RECALL notice, calls ApprovalRouter.request with decision D7.1, source type NOTICE, the notice ID, the preparer and rule R-LIT-03 with its version.
2. Litigation officer: opens SCR-10 Approval queue and selects the D7.1 item.
3. ACE front end: opens SCR-11 Decision screen with the SCR-18 Notice approval panel; loads the approval (GET /approvals/{approvalId}), the notice (GET /notices/{noticeId}), the document content and the case facts with their business dates.
4. Workbench: shows the notice PDF, the case facts used in it (case number, product, total balance, the addressee's role, postal address masked per the masking rules), the business date of each input, the rule ID and version, the template code and version, and the preparer.
5. Workbench: checks each input's age against its limit and the template's current status; sets the screen state to Ready, Stale input or held.
6. Litigation officer: approves; or picks another Approved template variant, enters a coded reason and approves; or rejects with a reason.
7. Workbench: for a change, calls NoticeApi.regenerate with the chosen template; the new notice version replaces the proposed one on the approval.
8. Workbench: calls the approval endpoint (RWB-E2-013 checks: Litigation A, not the preparer, reason rules); writes the decision entry with inputs reference, rule version, template version, approver and time.
9. Workbench: on approval, calls NoticeApi.approve so the notice state becomes Approved for the 16:00 dispatch run (JOB-10, RWB-E2-021); on rejection, calls NoticeApi.hold with reason REFUSED_BY_APPROVER and opens a task in the case owner's queue with the reason.
10. Workbench: shows MSG-P7-004 and sets the screen state to Decided.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The approver prepared the notice | Approve and reject are not offered; a direct call is refused with 409 | MSG-P7-002 | AC4 |
| X2 | An input is past its age limit | Screen state Stale input; approve is refused until the input is refreshed | MSG-P7-006 | AC5 |
| X3 | The template was withdrawn after generation | The notice is held (R-LIT-04); approve is refused | MSG-P6-003 | AC6 |
| X4 | Reject without a reason | Refused with 422 | MSG-GEN-001 | AC7 |
| X5 | A change of variant without a coded reason | Refused with 422 | MSG-P7-005 | AC8 |
| X6 | Another approver decided the item first | Refused with 409; the screen reloads in state Decided | MSG-GEN-004 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on routing (RWB-E2-013) and notice generation (RWB-E1-052); dispatch is RWB-E2-021 |
| Negotiable | Input age limits, override reasons and templates are data |
| Valuable | The first Workbench decision with a person approving, and no unapproved notice sent |
| Estimable | One screen with one panel, three calls to the notice module |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion below is one test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Approval screen for D7.1 demand and recall notices

  Background:
    Given the environment is SIT
    Given demand notice "N-0201" for case "RW-2026-000123" was generated at 08:10 on 14 December 2026 from template "DEMAND-MTG" "TH" version 2 under rule "R-LIT-03" version "LIT-2026.12", prepared by "U-9211"
    Given its approval "A-0201" is WAITING for role RW-LITOFF
    Given test user "U-9212" holds RW-LITOFF and did not prepare it
    Given the total balance comes from the COLLINS load of business date 13 December 2026

  Scenario: AC1 Approve
    Given "U-9212" opens "A-0201" on SCR-11 at 10:00 on 14 December 2026
    When "U-9212" approves
    Then notice "N-0201" moves to state "Approved" and is in the 16:00 dispatch run
    Then the decision log entry holds the inputs reference with each input's business date, rule "R-LIT-03" version "LIT-2026.12", template "DEMAND-MTG" version 2, approver "U-9212" and decided at 10:00
    Then the screen shows MSG-P7-004 and state "Decided"

  Scenario: AC2 Change
    Given "U-9212" opens "A-0201"
    When "U-9212" picks template variant "DEMAND-MTG-B" with coded reason "TEMPLATE_VARIANT" and approves
    Then the system generates a new notice version from "DEMAND-MTG-B" and is the one approved
    Then the entry records final call "APPROVED_CHANGED", the proposed template "DEMAND-MTG", the chosen "DEMAND-MTG-B" and the reason code
    Then only the changed notice reaches the dispatch run

  Scenario: AC3 Reject
    Given "U-9212" opens "A-0201"
    When "U-9212" rejects with reason "Addressee is a guarantor; a guarantor notice is needed"
    Then the approval status becomes "REFUSED" and notice "N-0201" is held with reason "REFUSED_BY_APPROVER"
    Then a task with the reason appears in the case owner's queue
    Then the decision log entry shows final call "REFUSED" and the reason

  Scenario: AC4 The preparer cannot decide
    Given "U-9211" also sees "A-0201" through RW-LEGAL
    When "U-9211" opens it
    Then approve and reject are not shown and the screen states MSG-P7-002
    Then the system refuses a direct POST /approvals/{approvalId}/approve by "U-9211" with status 409 and message MSG-P7-002

  Scenario: AC5 A stale input blocks approval
    Given the total balance on the notice comes from business date 11 December 2026, 3 days before, above the 1 day limit
    When "U-9212" opens "A-0201"
    Then the screen state is "Stale input" with MSG-P7-006 for "Total balance" and 3 days
    Then the system refuses an approve call with status 409 and message MSG-P7-006

  Scenario: AC6 A withdrawn template blocks approval
    Given template "DEMAND-MTG" version 2 is withdrawn at 09:30 on 14 December 2026
    When "U-9212" opens "A-0201" at 10:00
    Then the screen shows MSG-P6-003 and the notice is held under R-LIT-04
    Then the system refuses an approve call with status 409 and message MSG-P6-003

  Scenario: AC7 Reject needs a reason
    When "U-9212" rejects "A-0201" with an empty reason
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "reason"
    Then the notice stays "Generated"

  Scenario: AC8 A change needs a coded reason
    When "U-9212" picks template variant "DEMAND-MTG-B" and approves with no reason code
    Then the system refuses the call with status 422 and message MSG-P7-005
    Then the system generates no new notice version

  Scenario: AC9 Another approver decided first
    Given test user "U-9214" holding RW-LITOFF approved "A-0201" at 10:01
    When "U-9212" approves it at 10:02 from a screen loaded at 10:00
    Then the system refuses the call with status 409 and message MSG-GEN-004
    Then the screen reloads in state "Decided" showing approver "U-9214"

  Scenario: AC10 One screen holds the notice, the facts and the rule
    When "U-9212" opens "A-0201"
    Then the screen shows the notice PDF, case "RW-2026-000123", product "MORTGAGE", total balance with business date 13 December 2026, the addressee role "BORROWER", the postal address masked per the masking rules, rule "R-LIT-03" version "LIT-2026.12", template "DEMAND-MTG" version 2 and preparer "U-9211"
    Then the screen state is "Ready"
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Demand and recall notices are approved through approval routing before dispatch; only an Approved notice is dispatched | REQ-APD-006; CTL-14 |
| BR2 | The approver sees the notice, the inputs with their age, the rule and the template version on one screen | REQ-APD-002 |
| BR3 | The person who prepared the notice may not approve or reject it | CTL-05; Admin and access model, section 6.2 |
| BR4 | An input past its age limit blocks the decision until refreshed | VR-P7-023-3; MSG-P7-006; parameters rwb.decision.input-age-days.* |
| BR5 | A notice is generated only from the current Approved template; a withdrawn template holds the notice | R-LIT-03; R-LIT-04 |
| BR6 | A change of template variant needs a coded reason and uses only an Approved variant of the same notice type and product | R-UNI-14; CTL-07; LOV-OVERRIDE-REASON |
| BR7 | A rejection needs a reason and returns the case to the case owner's queue | FEAT-APD-04 |
| BR8 | A decision that cannot be written to the decision log does not take effect | Principle 5; R-UNI-39 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| In progress | Recommendation routed for approval | Notice generated under R-LIT-03 | Waiting approval |
| Waiting approval | Approver accepts, or changes and accepts | Not the preparer; inputs inside their limits; template current | In progress |
| Waiting approval | Approver rejects | Reason given | In progress, with a task in the case owner's queue |

The notice state moves Generated to Approved on approval, and Generated to Held on rejection or a withdrawn template (R-LIT-04).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF Litigation officer | Approves, changes or rejects D7.1 notices they did not prepare (Litigation A) |
| RW-LEGAL Legal counsel | Approves, changes or rejects D7.1 notices they did not prepare (Litigation A) |
| RW-HEADLIT Head of Litigation | Receives escalated D7.1 notices and decides them (Litigation A) |
| RW-CASEOWN Case owner | Receives the rejected notice task; may not approve (Litigation R) |
| SY-CASEWF | Calls the router when the notice is generated |
| Approval level | None: a D7.1 notice carries no amount limit; delegation item 2.1.3 (delay of legal action) does not apply to issuing a notice |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice | id | Read through NoticeApi |
| DF-LEG-016 | notice | case_id | Read through NoticeApi |
| DF-LEG-017 | notice | document_id | Read through NoticeApi |
| DF-LEG-018 | notice | notice_type | Read through NoticeApi |
| DF-CAS-002 | recovery_case | case_no | Read through the P3 interface |
| DF-CAS-003 | recovery_case | product_group | Read through the P3 interface |
| DF-ACC-012 | loan_account | total_balance | Read through the P1 data product interface, with its business date |
| DF-PTY-016 | contact_point | value_token | Read masked through the owning module's DTO |
| DF-DEC-046 | approval | status | Write |
| DF-DEC-043 | approval | terms | Write |
| DF-DEC-053 | approval | decision_log_id | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (the decision entry) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/approvals/{approvalId}** (new in RWB-E2-013): the approval with sourceType NOTICE and sourceRef, rule, version, due time; Litigation A for D7.1.

**GET /api/recovery/v1/notices/{noticeId}** (P6): Notice; Litigation R; errors 401, 403, 404.

**POST /approvals/{approvalId}/approve** (API-P7-003)

| Item | Value |
|---|---|
| Request | ApprovalAction: reason, reasonCode, changes.templateCode (for a change of variant) |
| Response | 200 DecisionLogEntry |
| Errors | 401; 403 no Litigation A (MSG-P4-002); 404 (MSG-P4-003); 409 preparer (MSG-P7-002), stale input (MSG-P7-006), template withdrawn (MSG-P6-003), decided by another approver (MSG-GEN-004); 422 no reason code on a change (MSG-P7-005); 503 entry not written (MSG-P7-003) |
| Authorization | Litigation, right A, for decision D7.1 |
| Idempotency | Idempotency-Key header |

**POST /api/recovery/v1/approvals/{approvalId}/refuse** (API-P7-005): ApprovalAction with reason required; response DecisionLogEntry; errors as approve; Litigation A; Idempotency-Key.

**Published interface NoticeApi** (P6, RWB-E1-052), methods called by P7:

```java
void approve(UUID noticeId, UUID decisionLogEntryId);            // Generated -> Approved
NoticeRef regenerate(UUID noticeId, String templateCode);         // new version from another Approved variant
void hold(UUID noticeId, String reasonCode, UUID decisionLogEntryId); // Generated -> Held
```

**Events:** consumes EV-13 NoticeGenerated; publishes EV-08 DecisionRecorded.

### 13. Solution plan

- Package: folder `recovery/decision/approval/notice` in the recovery module; Java package `recovery.decision.approval.notice`. Front end: `recovery/decision/approval`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| NoticeGeneratedListener | Listener | On EV-13 for DEMAND and RECALL, calls ApprovalRouter.request for D7.1 |
| NoticeApprovalService | Service | Input age and template checks, variant change through NoticeApi, calls ApprovalDecisionService, then NoticeApi.approve or hold |
| InputFreshnessCheck | Service | Compares each input's business date with its age limit parameter |
| DecisionScreen | React component | SCR-11 shell with states Ready, Stale input and Decided |
| NoticeApprovalPanel | React component | SCR-18 panel: PDF viewer, case facts with dates, rule and template, variant picker, coded reason, approve and reject |
| DecisionCenterAndLogController | Controller | Uses the RWB-E2-013 endpoints; no new endpoint |

- Database: no new table; writes approval status, terms and decision_log_id (RWB-E2-013 table) and decision_log_entry through the writer.
- Configuration and reference data: input age parameters (RW-COE, DL22); LOV-OVERRIDE-REASON values TEMPLATE_VARIANT and WRONG_PARTY (RW-COE); templates and variants (Legal counsel, RWB-E1-046).
- Build steps:
  1. Build NoticeGeneratedListener and test routing of a generated notice to RW-LITOFF.
  2. Build InputFreshnessCheck with the parameters; test AC5.
  3. Build NoticeApprovalService for approve, change and reject with the NoticeApi calls in the same transaction as the decision entry; tests for AC1, AC2, AC3, AC6, AC7, AC8.
  4. Test the preparer rule and the concurrent decision for AC4 and AC9 through the RWB-E2-013 checks.
  5. Build DecisionScreen and NoticeApprovalPanel with masked fields from the DTOs; test AC10 with a browser test.
  6. Run the end-to-end SIT test: generate, approve, appear in the 16:00 file of RWB-E2-021.
- Feature flag: `rwb.decision.notice-approval`.
- Done when: the tests in section 16 pass and an end-to-end SIT run shows only approved notices in the WIN file.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-002 | The preparer opens or acts on the item | You prepared this decision, so you cannot approve it. |
| MSG-P7-006 | An input is past its age limit | {input} is {days} days old, past its limit. Refresh it before you decide. |
| MSG-P6-003 | The template was withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-005 | Change of variant without a coded reason | Enter the reason you are not following the recommendation. |
| MSG-GEN-001 | Reject without a reason | Enter {field}. |
| MSG-GEN-004 | Another approver decided first | Someone else changed this record. Reload it to see their change. |
| MSG-P7-004 | Approved | Approved. The case moves to {state}. |
| MSG-P7-003 | Entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-10 Approval queue | List | Selects a D7.1 item |
| SCR-11 Decision screen | Ready | Reads the notice and the facts; approves, changes the variant or rejects |
| SCR-11 Decision screen | Stale input | Sees MSG-P7-006 for the input; approve is disabled |
| SCR-11 Decision screen | Decided | Sees the outcome, the approver and the time; no action is offered |
| SCR-18 Notice approval | Generated | The panel inside SCR-11 shows the notice waiting for a decision |
| SCR-18 Notice approval | Approved | The notice shows as approved and waiting for the dispatch run |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-014-01 | AC1, BR1 | System | Synthetic demand notice N-0201 from DEMAND-MTG version 2 |
| TC-E2-014-02 | AC2, BR6 | System | Variant DEMAND-MTG-B with reason TEMPLATE_VARIANT |
| TC-E2-014-03 | AC3, BR7 | System | Rejection with a reason |
| TC-E2-014-04 | AC4, BR3 | System | Preparer who also holds RW-LEGAL |
| TC-E2-014-05 | AC5, BR4 | System | Total balance from a load 3 days old |
| TC-E2-014-06 | AC6, BR5 | System | Template withdrawn after generation |
| TC-E2-014-07 | AC7, BR7 | System | Rejection with an empty reason |
| TC-E2-014-08 | AC8, BR6 | System | Variant change with no reason code |
| TC-E2-014-09 | AC9 | System | Two litigation officers deciding one item |
| TC-E2-014-10 | AC10, BR2 | System | Decision screen content check |
| TC-E2-014-11 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E2-014-12 | Principle 5 | Resilience | The decision log write forced to fail during an approval; the notice stays Generated |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: age limits, override reasons, templates and route roles are data.
- No personal data in logs, tests or prompts; the address on screen is masked per the masking rules, and tests use synthetic tokenized values.
- No read of another module's tables: the notice through NoticeApi, the case through the P3 interface.
- No notice reaches dispatch without an approval entry.
- The approval entry and the notice state change commit in one transaction.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-002 | Recommendation, reasons, inputs and limit on one screen | Epic 2, 3.7 | FEAT-APD-08 | 8.1 Prepare pre-litigation | BR2, BR4 | TC-E2-014-05, TC-E2-014-10 |
| REQ-APD-006 | Demand and recall notices approved through approval routing | Epic 2, 3.7 | FEAT-APD-08 | 8.1 Prepare pre-litigation | BR1, BR3, BR5, BR6, BR7, BR8 | TC-E2-014-01 to TC-E2-014-04, TC-E2-014-06 to TC-E2-014-09, TC-E2-014-11, TC-E2-014-12 |

### 19. Out of scope

- Dispatch to WIN, proof of delivery and the notice period (RWB-E2-021).
- Guarantor notices and statutory sale notices (later litigation and asset stories, Epic 5).
- Approval of decisions with an amount limit on SCR-11 (Epic 3 settlement and restructure stories).
- Template authoring and Legal approval of templates (RWB-E1-034, RWB-E1-046).


---

## RWB-E2-015 Timers, escalation and the deviation flag on the case record view

| Item | Value |
|---|---|
| Story key | RWB-E2-015 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-WKM-05 Show timers and the service level on the case; FEAT-WKM-06 Show the deviation flag on the case; FEAT-WKM-07 Show escalation state on the case; FEAT-DVH-02 Pause the stage clock on a deviation; FEAT-DVH-03 Keep the prescription clock running during a deviation; FEAT-DVH-05 Apply a contact stop for X1 to X3; FEAT-DVH-06 Clear a deviation and resume the timers; FEAT-DVH-09 Handle two deviations on one case |
| Requirement IDs | REQ-WKM-004, REQ-WKM-005, REQ-DVH-002 |
| BRD section | Business Requirements Epic 2, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.15 |
| L3 process | All recovery processes; 11 Handle customer care and deviations |
| Decision | X1 to X7 |
| Priority | Must |
| Depends on | RWB-E1-028, RWB-E1-035 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case record view to show every timer with its due date, the escalation path, the prescription date and any deviation flag with its approver**, so that **the next deadline and the reason a case left its path are visible on the case**.

### 2. Business rationale

Deadlines are agreed by email today, and litigation was not filed for debtors who met the criteria because nobody saw the prescription date in time (CTL-18). A deviation pauses the stage clock but never the prescription clock (REQ-DVH-002), so the case owner must see both, with who holds the deviation and where the case returns. This story puts every timer, escalation and deviation on the case record view. It meets REQ-WKM-004, REQ-WKM-005 and REQ-DVH-002. The measure is that every open case's record view shows its next due date and its prescription date.

### 3. Preconditions

- RWB-E1-028 is done: timers, warnings, escalations and prescription dates are written for each case, and JOB-05 Timer check runs every 5 minutes.
- RWB-E1-035 is done: the case record view SCR-03 exists with its timeline.
- The deviation handling module (S8) publishes `DeviationQuery` with the open and cleared deviations of a case.
- The decision log query interface (P7) returns the approver of a deviation decision (decision codes X1 to X7).
- SERVICE_LEVEL rows carry the escalation role for each status (RWB-E1-045; values DL22).
- `prescription.warning-days` is in force (assumed 90; DL22).
- The person holds a role with Case record R and the case is in scope.

### 4. Flow

1. Case owner: opens SCR-03 Case record for a case.
2. Front end: calls `GET /cases/{caseId}` and `GET /cases/{caseId}/timers`.
3. Case service: reads the case, its timers and, for each timer with a task, the owner role of the task.
4. Case service: reads the open deviations from `DeviationQuery` and the approver of each from the P7 decision log query.
5. Case service: reads the escalation role for the case's product and status from `ProductParameterService.serviceLevel(...)`.
6. Front end: shows the timers ordered by due date, each with status, due date, warning state, escalation level, escalated to and the next escalation point.
7. Front end: shows the prescription date with the warning when the business date is on or after the prescription timer's warn at.
8. Front end: when a deviation is open, shows state On hold with MSG-P3-004, each deviation's code, handler, approver, raised date, contact stop and return point.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case has no running timer | The timers section shows the empty sentence | MSG-P3-018 | AC8 |
| X2 | The case is outside the person's scope | Not found | MSG-P4-003 | AC9 |
| X3 | The deviation module does not answer inside the timeout | The timers show; the deviation section shows that it could not be read and the on hold banner still shows from the case flag | MSG-GEN-006 | AC10 |
| X4 | Two deviations are open | Both show; the case stays on hold until both clear | MSG-P3-004 | AC5 |
| X5 | Prescription date is 91 days away with a 90 day warning | No warning | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads what the timer engine and the deviation module already write |
| Negotiable | The layout and the warning days are negotiable; the content is fixed by REQ-WKM-005 |
| Valuable | The next deadline, the escalation and the deviation are on one screen |
| Estimable | Two read endpoints extended, two published interfaces read, one screen section |
| Small | Fits in one sprint with its tests |
| Testable | API tests on seeded timers and deviations and a browser test of SCR-03 |

### 7. Acceptance criteria

```gherkin
Feature: Timers, escalation and the deviation flag on the case record view

  Background:
    Given the business date is 2026-12-15
    Given user "U-CO-01" holds RW-CASEOWN and owns case "RW-2026-000501" with product group "HIRE_PURCHASE" and status "IN_PROGRESS"
    Given prescription.warning-days is 90

  Scenario: AC1 Timers shown
    Given case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF"
    When "U-CO-01" opens the case record
    Then the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer"

  Scenario: AC2 Deviation flag
    Given case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true
    When "U-CO-01" opens the case record
    Then the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date
    Then the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped"

  Scenario: AC3 Prescription
    Given case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date
    When "U-CO-01" opens the case record
    Then the prescription date 2027-02-13 shows with the warning MSG-P3-003
    Then for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows

  Scenario: AC4 Escalation state
    Given case "RW-2026-000501" has a "SERVICE_LEVEL" timer that expired on 2026-12-12 with escalation level 1, escalated to "RW-TEAMMGR" at 2026-12-12 09:05
    Given the SERVICE_LEVEL row for "HIRE_PURCHASE" status "IN_PROGRESS" names the next escalation role "RW-PRODHEAD"
    When "U-CO-01" opens the case record
    Then the timer shows status "Expired", escalated to "Team manager" at 2026-12-12 09:05 and next escalation point "Product head"
    Then the case stays in queue and status as before

  Scenario: AC5 Two deviations
    Given case "RW-2026-000504" has deviations "X1" raised on 2026-12-05 and "X3" raised on 2026-12-08, both open
    When "U-CO-01" opens the case record
    Then both deviations show with their own handler and approver
    Then the screen stays in state "On hold"
    When "X1" is cleared on 2026-12-14 and "X3" stays open
    Then the screen stays in state "On hold" with only "X3" open and "X1" shown as cleared on 2026-12-14

  Scenario: AC6 Stage clock paused and prescription running
    Given case "RW-2026-000502" with deviation "X3" open since 2026-12-10
    Given its "SERVICE_LEVEL" timer paused on 2026-12-10 and its "PRESCRIPTION" timer running
    When "U-CO-01" opens the case record
    Then the service level timer shows "Paused since 2026-12-10"
    Then the prescription timer shows "Running" with its date

  Scenario: AC7 Deviation cleared and timers resumed
    Given case "RW-2026-000505" had deviation "X1" cleared on 2026-12-14 and its "SERVICE_LEVEL" timer resumed with a new expiry of 2026-12-22
    When "U-CO-01" opens the case record
    Then the screen is not on hold
    Then the service level timer shows "Running" with due date 2026-12-22
    Then the deviation shows as cleared on 2026-12-14 with outcome "Returned"

  Scenario: AC8 No running timer
    Given case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED"
    When "U-CO-01" opens the case record
    Then the timers section shows MSG-P3-018

  Scenario: AC9 Case outside scope
    Given case "RW-2026-000507" belongs to team "SME-NTH" and "U-CO-01" has scope Own in team "MTG-BKK"
    When "U-CO-01" opens it
    Then the system does not find the response with MSG-P4-003

  Scenario: AC10 Deviation module does not answer
    Given the deviation query does not answer within 2 seconds for case "RW-2026-000502"
    When "U-CO-01" opens the case record
    Then the timers and the prescription date show
    Then the deviation section shows MSG-GEN-006 naming "Deviation handling"
    Then the on hold banner shows from the case's deviation flag
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every timer of the case with status Running, Paused or Expired shows with type, due date, status and the owner role of its task | REQ-WKM-005; LOV-TIMER |
| BR2 | A breached service level shows the role it was escalated to, when, and the next escalation point. The case does not move | R-UNI-30; REQ-WKM-004 |
| BR3 | A deviation pauses the stage clock and keeps the prescription clock running | R-DEV-01; REQ-DVH-002 |
| BR4 | A case with a deviation open shows as on hold with the deviation and the prescription date | casemodel.txt Case status (On hold); R-UNI-04; R-UNI-05 |
| BR5 | X1, X2 and X3 show the contact stop | R-UNI-04; R-UNI-05; R-UNI-06; CTL-16 |
| BR6 | The case leaves on hold only when every open deviation is cleared | R-UNI-43; FEAT-DVH-09 |
| BR7 | The prescription date shows a warning from `prescription.warning-days` before it (assumed 90; DL22) | R-UNI-31; CTL-18 |
| BR8 | The return point of a deviation is the routing state the case was in when it paused | DF-CAS-041; R-DEV-08 |
| BR9 | The approver of a deviation is the approver on its decision log entry | REQ-DRI-001 |

### 9. State transitions

None. This story does not change a case status. It shows the timer statuses (Running, Paused, Expired) and the On hold status that other stories set. It adds two fields that the escalation step of JOB-05 Timer check (RWB-E1-028) writes when a timer escalates.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the case record view (Case record R, scope Own) |
| RW-TEAMMGR, team manager | Reads (Case record R, scope Team) |
| RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL | Read the case and its deviations (Case record R) |
| RW-AUDIT, internal audit | Reads (Case record R, scope All) |
| SY-CASEWF, case workflow module | Writes the escalation fields in JOB-05 |

Reading the approver needs no Decision log right: the case service returns the approver's user ID only, not the decision log entry.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-017 | recovery_case | prescription_date | Read |
| DF-CAS-018 | recovery_case | stage_clock_start | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-WRK-027 | timer | id | Read |
| DF-WRK-029 | timer | task_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-031 | timer | started_at | Read |
| DF-WRK-032 | timer | expires_at | Read |
| DF-WRK-033 | timer | warn_at | Read |
| DF-WRK-034 | timer | paused | Read |
| DF-WRK-035 | timer | status | Read |
| DF-WRK-036 | timer | escalation_level | Read |
| DF-WRK-043 | timer | escalated_to_role | Write (JOB-05 escalation step), Read |
| DF-WRK-044 | timer | escalated_at | Write (JOB-05 escalation step), Read |
| DF-WRK-023 | task | owner_role | Read |
| DF-CAS-038 | deviation | deviation_code | Read, through the S8 interface |
| DF-CAS-039 | deviation | raised_at | Read, through the S8 interface |
| DF-CAS-041 | deviation | paused_state | Read, through the S8 interface |
| DF-CAS-042 | deviation | handler_user_id | Read, through the S8 interface |
| DF-CAS-043 | deviation | contact_stop | Read, through the S8 interface |
| DF-CAS-044 | deviation | cleared_at | Read, through the S8 interface |
| DF-CAS-045 | deviation | outcome | Read, through the S8 interface |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read, through the P7 interface |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/cases/{caseId}** (P3)

| Item | Value |
|---|---|
| Request | Path `caseId` (uuid) |
| Response | 200 `Case` with `prescriptionDate`, `stageClockStart`, `deviationOpen`, `legalHold`, and the new `deviations[]` (`deviationCode`, `raisedAt`, `handlerUserId`, `approverUserId`, `pausedState`, `contactStop`, `clearedAt`, `outcome`) and `deviationsAvailable` (boolean) |
| Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 unknown or out of scope (MSG-P4-003); 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

**GET /api/recovery/v1/cases/{caseId}/timers** (P3)

| Item | Value |
|---|---|
| Request | Path `caseId` (uuid) |
| Response | 200 `Timer[]` with `timerType`, `startedAt`, `expiresAt`, `warnAt`, `paused`, `status`, `escalationLevel`, and the new `nextStepOwnerRole`, `escalatedToRole`, `escalatedAt`, `nextEscalationRole`, `inWarning` |
| Errors | 401; 403 (MSG-P4-002); 404 (MSG-P4-003); 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

**Published interfaces used**

```java
// S8
List<DeviationView> DeviationQuery.forCase(UUID caseId);
// P7
Optional<UUID> DecisionLogQuery.approverOf(UUID caseId, String decisionCode, Instant raisedAt);
// P3, RWB-E1-045
ServiceLevel ProductParameterService.serviceLevel(String productGroup, String caseStatus, LocalDate businessDate);
```

`DeviationQuery.forCase` is called with a 2 second timeout (NFR-008). No events are published.

### 13. Solution plan

**Package.** `recovery.casewf.caseview` in the recovery module; front end folder `src/modules/recovery/casewf/caserecord`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseViewService | Service | Builds the case with deviations, approvers and the availability flag |
| TimerViewService | Service | Builds the timers with the task owner role, escalation fields, next escalation point and warning state |
| TimerRepository | Repository | Reads the case's timers and their tasks |
| EscalationRecorder | Service | Change to the RWB-E1-028 escalation step: writes `escalated_to_role` and `escalated_at` |
| CaseAndWorkflowController | Controller | The two endpoints with the new fields |
| CaseClocksPanel | React component | Timers, prescription date and warnings on SCR-03 |
| DeviationPanel | React component | Deviations, handler, approver, contact stop, return point; on hold banner |

**Database.** Migration `V<next>__rwb_e2_015_timer_escalation.sql` adds `timer.escalated_to_role varchar(20)` and `timer.escalated_at timestamptz`. Reads use `ix_timer_case_id` and `ix_task_case_id`.

**Configuration and reference data.** `prescription.warning-days` = 90 (assumed; DL22), `caseview.deviation-timeout-ms` = 2000, both in the configuration service. SERVICE_LEVEL escalation roles (business lead; DL22). Timer and deviation labels from LOV-TIMER and LOV-DEVIATION through the P4 list interface.

**Build steps**

1. Write the migration; change the escalation step of JOB-05 to write the two fields.
2. Build `TimerViewService` with the owner role, escalation and warning fields; test each timer status.
3. Build `CaseViewService` with the S8 and P7 calls, the timeout and the availability flag.
4. Extend the two endpoints and the generated types.
5. Build `CaseClocksPanel` and `DeviationPanel` with the On hold state and the warnings.
6. Write the tests in section 16 with seeded timers and stubbed S8 and P7 interfaces in system tests, and real ones in SIT.

**Feature flag.** `rwb.p3.case-clocks`. Off: SCR-03 shows the Epic 1 read only fields.

**Done when.** The tests in section 16 pass, and SCR-03 for a case with 50 documents and 6 timers loads within 2 seconds (NFR-009).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-003 | A timer or the prescription date is inside its warning period | {timer} ends on {date}. |
| MSG-P3-004 | The case is on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-018 | The case has no running, paused or expired timer | There are no running timers on this case. |
| MSG-GEN-006 | The deviation module does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-003 | The case is outside the person's scope | This case is not in your scope. |
| MSG-P4-002 | A role without Case record R opens the view | You cannot {action} here. Your role does not include it. |

MSG-P3-018 is new (see Additions). Thai text follows DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-03 Case record | Loading | Sees skeleton rows in the clocks and deviation panels |
| SCR-03 Case record | Read only | Reads timers, due dates, escalation, prescription date and warnings |
| SCR-03 Case record | Editable | Same panels; edits elsewhere on the record are not part of this story |
| SCR-03 Case record | On hold | Reads the banner with MSG-P3-004 and each open deviation with handler, approver, contact stop and return point |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-015-01 | AC1, BR1 | System | NOTICE_PERIOD timer on a task owned by RW-LITOFF |
| TC-E2-015-02 | AC2, BR4, BR5, BR8, BR9 | System | X3 with handler, approver, paused state and contact stop |
| TC-E2-015-03 | AC3, BR7 | System | Prescription 60 and 91 days ahead |
| TC-E2-015-04 | AC4, BR2 | System | SERVICE_LEVEL expired, level 1, escalated to RW-TEAMMGR |
| TC-E2-015-05 | AC5, BR6 | System | X1 and X3 open, then X1 cleared |
| TC-E2-015-06 | AC6, BR3 | System | Paused service level and running prescription |
| TC-E2-015-07 | AC7, BR6 | System | X1 cleared and timer resumed |
| TC-E2-015-08 | AC8 | System | Case with only stopped timers |
| TC-E2-015-09 | AC9 | System | Case of team SME-NTH opened by an MTG-BKK owner |
| TC-E2-015-10 | AC10 | System | Stubbed deviation query delayed 3 seconds |
| TC-E2-015-11 | Access | Access | RW-REFADM (no Case record right) calls `GET /cases/{caseId}/timers`; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. Warning days, escalation roles, timeouts and labels are data.
- No personal data in logs, tests or prompts. The panels show staff user IDs resolved to display names by the ACE common module, and no customer data. Test data is synthetic.
- No read of another module's tables. Deviations come from `DeviationQuery` (S8) and approvers from `DecisionLogQuery` (P7).
- The view never changes a timer, a deviation or the case.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-004 | A breached service level visible to the escalation role without the case moving | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-07 | All recovery processes | R-UNI-30 | TC-E2-015-04, TC-E2-015-11 |
| REQ-WKM-005 | Timers, escalation state and the deviation flag on the case record view | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-05, FEAT-WKM-06 | All recovery processes | R-UNI-31, R-UNI-04, R-UNI-05 | TC-E2-015-01 to TC-E2-015-03, TC-E2-015-08 to TC-E2-015-10 |
| REQ-DVH-002 | A deviation pauses the stage clock and keeps the prescription clock running | Business Requirements Epic 2, section 4; Program, section 5.15 | FEAT-DVH-02, FEAT-DVH-03, FEAT-DVH-05, FEAT-DVH-06, FEAT-DVH-09 | 11 Handle customer care and deviations | R-DEV-01, R-UNI-43 | TC-E2-015-02, TC-E2-015-05 to TC-E2-015-07 |

### 19. Out of scope

- Raising, handling and clearing deviations (S8, SCR-06 and SCR-08).
- Starting, pausing and resuming timers, and the escalation itself (RWB-E1-028).
- The history timeline on the case (RWB-E2-016).
- The next action panel (RWB-E2-035).


---

## RWB-E2-016 Full case record view with the history timeline

| Item | Value |
|---|---|
| Story key | RWB-E2-016 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow, with P7 Decision center and log |
| Feature | FEAT-WKM-08 Show the full case record view with the history timeline; FEAT-WKM-09 Show queue history on the case |
| Requirement IDs | REQ-WKM-008, REQ-OCC-008 |
| BRD section | Business Requirements Epic 2, sections 3.3 and 4; Business Requirements Program, section 5.3 |
| L3 process | 06 Take over and own the case; All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-035, RWB-E2-015, RWB-E2-012 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case record view to show every action, decision, transfer, letter and document on one timeline with filters, and the queue history with the reason for each move**, so that **I read the whole case in one place**.

### 2. Business rationale

A case lives for months or years and passes through several teams, partners and courts. Today a new owner reads email threads and spreadsheets to learn what happened. This story puts the decision log entries, assignments and transfers, contacts, notices, documents and timer events of a case on one timeline, filtered by type and date, with a queue history that shows every queue and owner and the reason for each move. It meets REQ-WKM-008. The measure is that a case history with 30 events reads in under 2 seconds (NFR-009) and stays under 2 seconds at the 2031 data size (NFR-070).

### 3. Preconditions

- RWB-E1-035 is done: the timeline v1.1 on SCR-03 shows contacts, documents, assignments, transfers and status changes.
- RWB-E2-015 is done: the clocks and deviations panels on SCR-03.
- RWB-E2-012 is done: each assignment carries its queue and its transfer reason code.
- P7 publishes `DecisionLogQuery.forCase(...)`; P5 publishes `DocumentQuery.forCase(...)`; P6 publishes `NoticeQuery.forCase(...)`.
- The person holds a role with Case record R and the case is in scope. Decision, document and notice items need Decision log R, Documents R and Litigation R.

### 4. Flow

1. Case owner: opens SCR-04 Case timeline from SCR-03 Case record.
2. Front end: calls `GET /cases/{caseId}/timeline` with the filters kept for the session.
3. Timeline service: checks the scope and the caller's rights in Decision log, Documents and Litigation.
4. Timeline service: reads assignments, interactions and timer events from the P3 tables, and in parallel calls the P7, P5 and P6 interfaces for the sources the caller may read, each with a 2 second timeout.
5. Timeline service: maps each record to a timeline item with time, type, summary, actor and reference, merges them newest first and returns one page.
6. Front end: shows the timeline in state Loading, then the list; the filter by type and date reloads it in state Filtered.
7. Case owner: opens Queue history; the front end calls the timeline with type ASSIGNMENT and TRANSFER and shows from queue, to queue, from owner, to owner, reason code and rule ID for each move.
8. Case owner: opens a decision item; the front end opens the entry through `GET /decision-log/{entryId}` (P7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A source module does not answer within 2 seconds | The other items show; a notice names the missing source | MSG-GEN-006 | AC6 |
| X2 | The caller lacks Decision log R, Documents R or Litigation R | Those item types are left out without an error | None | AC5 |
| X3 | Date from is after date to | Refused | MSG-GEN-003 | AC7 |
| X4 | No item matches the filter | Empty sentence | MSG-P3-019 | AC8 |
| X5 | An assignment written before RWB-E2-012 has no queue | The move shows with "Queue not recorded" | None | AC9 |
| X6 | The case is outside the caller's scope | Not found | MSG-P4-003 | AC10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads what other stories write; needs the queue on the assignment from RWB-E2-012 |
| Negotiable | Item wording and filter layout can change; the sources and the rights are fixed |
| Valuable | A new owner reads the case without asking the previous one |
| Estimable | One endpoint, one merge service, three interface calls, one screen |
| Small | Fits in one sprint with its tests |
| Testable | API tests with seeded P3 rows and stubbed interfaces; one load test |

### 7. Acceptance criteria

```gherkin
Feature: Full case record view with the history timeline

  Background:
    Given the business date is 2026-12-20
    Given user "U-CO-01" holds RW-CASEOWN and owns case "RW-2026-000601"

  Scenario: AC1 Timeline
    Given case "RW-2026-000601" has 30 events: 4 assignments, 3 transfers, 8 contacts, 6 decision log entries, 2 notices, 5 documents and 2 timer events
    When "U-CO-01" opens the case timeline
    Then the 30 items show newest first, each with type, actor and time
    Then the first page loads within 2 seconds at the 95th percentile over 20 runs

  Scenario: AC2 Filter
    Given the filter set to "DECISION"
    When the timeline refreshes
    Then only the 6 decision items show
    Then each carries its decision log entry ID and opens that entry

  Scenario: AC3 Queue history
    Given case "RW-2026-000601" was allocated to "MTG-BKK-CO" on 2026-11-30 and transferred three times: to "LIT-BKK-01" with reason "R05" on 2026-12-05, to "MTG-BKK-CO" with reason "R06" on 2026-12-08 and to "LIT-BKK-02" with reason "R01" on 2026-12-12
    When "U-CO-01" opens queue history
    Then the three moves show newest first with from queue, to queue, from owner, to owner, reason code and rule ID
    Then the allocation on 2026-11-30 shows as the first entry with reason "ALLOCATION"

  Scenario: AC4 Date filter
    Given the filter from 2026-12-05 to 2026-12-08
    When the timeline refreshes
    Then only items dated 2026-12-05 to 2026-12-08 inclusive show

  Scenario: AC5 Items the role may not read
    Given user "U-PC-01" holds RW-PHONECOL with case "RW-2026-000601" in scope
    When "U-PC-01" opens the case timeline
    Then no decision item and no notice item shows
    Then contacts, assignments, transfers, documents and timer events show

  Scenario: AC6 A source does not answer
    Given the document query does not answer within 2 seconds
    When "U-CO-01" opens the case timeline
    Then the 25 items from the other sources show
    Then a notice shows MSG-GEN-006 naming "Document hub"

  Scenario: AC7 Dates in the wrong order
    When "U-CO-01" sets the filter from 2026-12-10 to 2026-12-01
    Then the system refuses the request with MSG-GEN-003 naming "to" and "from"

  Scenario: AC8 Nothing matches
    Given the filter set to "NOTICE" and the dates 2026-11-01 to 2026-11-15
    When the timeline refreshes
    Then the screen shows MSG-P3-019

  Scenario: AC9 Assignment written before the queue was recorded
    Given case "RW-2026-000602" has an assignment from 2026-11-30 with no queue recorded
    When "U-CO-01" opens its queue history
    Then the move shows with "Queue not recorded" and its reason "ALLOCATION"

  Scenario: AC10 Case outside scope
    Given case "RW-2026-000603" belongs to team "SME-NTH" and "U-CO-01" has scope Own in team "MTG-BKK"
    When "U-CO-01" opens its timeline
    Then the system does not find the response with MSG-P4-003

  Scenario: AC11 Large history
    Given case "RW-2026-000604" has 4,000 timeline items
    When "U-CO-01" opens the case timeline with page size 50
    Then the first 50 items show within 2 seconds
    Then the total shows 4,000
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The timeline holds every assignment, transfer, contact, decision log entry, notice, document and timer event of the case | REQ-WKM-008; casemodel.txt Case file |
| BR2 | Items are ordered newest first; items at the same time keep the order of their sources' sequence | events.txt Rules (ordering) |
| BR3 | A decision item shows only to a role with Decision log R, a document item only with Documents R, a notice item only with Litigation R | roles.txt Permissions; CTL-09 |
| BR4 | Queue history shows each assignment with its from and to queue, from and to owner, reason, reason code and rule ID | REQ-WKM-008; REQ-CWC-016 |
| BR5 | A decision item links to its decision log entry, which is never changed; a correction shows as a further entry | R-UNI-24; REQ-DRI-002 |
| BR6 | Personal data in a contact summary is masked by role | CTL-11; DL26 |
| BR7 | A source that does not answer in time does not stop the timeline | NFR-008 |

### 9. State transitions

None. This story does not change a case status. It reads records only.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the timeline and queue history (Case record R; Decision log R; Documents R; Litigation R) |
| RW-TEAMMGR, team manager | Reads the timeline and queue history (Case record R; Decision log R) |
| RW-PHONECOL, phone collector | Reads the timeline without decisions and notices (Case record R; Documents R) |
| RW-CONDUCT, conduct and QA officer | Reads every item (R in all areas) |
| RW-AUDIT, internal audit | Reads every item (R in all areas); changes nothing |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-011 | recovery_case | team_code | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-010 | assignment | case_id | Read |
| DF-WRK-012 | assignment | assignee_user_id | Read |
| DF-WRK-013 | assignment | assigned_at | Read |
| DF-WRK-014 | assignment | ended_at | Read |
| DF-WRK-015 | assignment | reason | Read |
| DF-WRK-016 | assignment | rule_id | Read |
| DF-WRK-039 | assignment | queue_id | Read |
| DF-WRK-040 | assignment | transfer_reason_code | Read |
| DF-INT-002 | interaction | case_id | Read |
| DF-INT-004 | interaction | occurred_at | Read |
| DF-INT-005 | interaction | channel | Read |
| DF-INT-006 | interaction | direction | Read |
| DF-INT-008 | interaction | contact_result | Read |
| DF-INT-011 | interaction | summary | Read, masked by role |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-031 | timer | started_at | Read |
| DF-WRK-035 | timer | status | Read |
| DF-DEC-001 | decision_log_entry | id | Read, through the P7 interface |
| DF-DEC-003 | decision_log_entry | decision_code | Read, through the P7 interface |
| DF-DEC-004 | decision_log_entry | rule_id | Read, through the P7 interface |
| DF-DEC-012 | decision_log_entry | final_call | Read, through the P7 interface |
| DF-DEC-016 | decision_log_entry | decided_at | Read, through the P7 interface |
| DF-DOC-001 | document | id | Read, through the P5 interface |
| DF-DOC-004 | document | document_type | Read, through the P5 interface |
| DF-DOC-005 | document | source | Read, through the P5 interface |
| DF-LEG-015 | notice | id | Read, through the P6 interface |
| DF-LEG-018 | notice | notice_type | Read, through the P6 interface |
| DF-LEG-019 | notice | sent_date | Read, through the P6 interface |
| DF-LEG-022 | notice | delivery_status | Read, through the P6 interface |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /cases/{caseId}/timeline** (P3)

| Item | Value |
|---|---|
| Request | Path `caseId`; query `type` (comma separated: DECISION, ASSIGNMENT, TRANSFER, INTERACTION, NOTICE, DOCUMENT, TIMER), `from` (date), `to` (date), `page` (new, default 0), `size` (new, default 50, 1 to 200) |
| Response | 200 `TimelinePage`: `items[]` of `TimelineItem` (`at`, `type`, `summary`, `by`, `reference`, and the new `reasonCode`, `fromQueueCode`, `toQueueCode`, `ruleId`), `page`, `size`, `total`, and the new `unavailableSources[]` |
| Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 unknown or out of scope (MSG-P4-003); 422 `to` before `from` (MSG-GEN-003) or size outside 1 to 200 (MSG-GEN-002); 503 |
| Authorization | Case record, right R, scope applied; item types filtered by Decision log R, Documents R and Litigation R |
| Idempotency | Not applicable |

**GET /api/recovery/v1/decision-log/{entryId}** (P7) opens a decision item (Decision log R).

**Published interfaces used**

```java
// P7
List<DecisionSummary> DecisionLogQuery.forCase(UUID caseId, Instant from, Instant to);
// P5
List<DocumentSummary> DocumentQuery.forCase(UUID caseId, Instant from, Instant to);
// P6
List<NoticeSummary> NoticeQuery.forCase(UUID caseId, Instant from, Instant to);
```

Each call runs in parallel with a 2 second timeout. No events are published.

### 13. Solution plan

**Package.** `recovery.casewf.timeline` in the recovery module; front end folder `src/modules/recovery/casewf/timeline`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TimelineService | Service | Checks rights, calls the sources in parallel, merges, sorts, pages |
| TimelineItemMapper | Service | Maps assignments, interactions, timers, decisions, documents and notices to `TimelineItem`, with summaries built from codes |
| AssignmentHistoryRepository | Repository | Reads assignments with their queue codes for a case |
| InteractionRepository | Repository | Reads the case's interactions in the date range |
| CaseAndWorkflowController | Controller | The timeline endpoint and its parameter checks |
| CaseTimelinePage | React component | SCR-04 with Loading and Filtered states, type and date filters, the source notice |
| QueueHistoryTab | React component | The queue history view on SCR-04 |

**Database.** Reads `assignment`, `interaction`, `timer` and `queue`. Uses `ix_assignment_case_id`, `ix_interaction_case_time` and `ix_timer_case_id`. No new table.

**Configuration and reference data.** `timeline.source-timeout-ms` = 2000 and the page size limits in the configuration service. Type labels and reason code labels from LOV-ASSIGN-REASON and LOV-TRANSFER-REASON through the P4 list interface. Masking rules (Compliance, DL26).

**Build steps**

1. Build the two repositories and `TimelineItemMapper` for P3 records; unit test each item type.
2. Build `TimelineService` with the rights filter, parallel calls, timeouts and `unavailableSources`.
3. Add paging, the type and date filters and the new item fields to the endpoint.
4. Build `CaseTimelinePage` with filters kept in session storage and `QueueHistoryTab`.
5. Add the masking call for contact summaries through the ACE common module.
6. Write the tests in section 16, including the 4,000 item load test.

**Feature flag.** `rwb.p3.full-timeline`. Off: SCR-03 shows the RWB-E1-035 timeline.

**Done when.** The tests in section 16 pass, and the query plan for the 4,000 item case uses the case indexes only.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-019 | No item matches the filter | Nothing on this case matches the filter. |
| MSG-GEN-006 | A source module does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-GEN-003 | Date to is before date from | {field} cannot be before {other}. |
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | A role without Case record R opens the timeline | You cannot {action} here. Your role does not include it. |

MSG-P3-019 is new (see Additions). Thai text follows DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-04 Case timeline | Loading | Sees skeleton rows |
| SCR-04 Case timeline | Filtered | Filters by type and date; opens a decision, a document or a notice; reads the queue history |
| SCR-03 Case record | Read only | Opens the timeline from the record |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-016-01 | AC1, BR1, BR2 | System | 30 items over seven types; 20 timed runs |
| TC-E2-016-02 | AC2, BR5 | System | Filter DECISION over the AC1 case |
| TC-E2-016-03 | AC3, BR4 | System | One allocation and three transfers with reasons R05, R06, R01 |
| TC-E2-016-04 | AC4 | System | Date filter 2026-12-05 to 2026-12-08 |
| TC-E2-016-05 | AC5, BR3 | System | RW-PHONECOL on the AC1 case |
| TC-E2-016-06 | AC6, BR7 | System | Stubbed document query delayed 3 seconds |
| TC-E2-016-07 | AC7 | System | From 2026-12-10, to 2026-12-01 |
| TC-E2-016-08 | AC8 | System | NOTICE filter in November |
| TC-E2-016-09 | AC9 | System | Assignment with no queue |
| TC-E2-016-10 | AC10 | System | Case of team SME-NTH |
| TC-E2-016-11 | AC11 | System | 4,000 synthetic items, page size 50 |
| TC-E2-016-12 | Access | Access | RW-REFADM (no Case record right) calls the timeline; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. Type lists, labels, timeouts and page sizes are data.
- No personal data in logs, tests or prompts. Summaries are built from codes; contact summaries are masked by role and never logged. Test data is synthetic.
- No read of another module's tables. Decisions, documents and notices come only through the P7, P5 and P6 interfaces.
- The timeline never writes; it does not copy other modules' records into P3 tables.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-008 | Queue and transfer history visible on the case | Business Requirements Epic 2, sections 3.3 and 4; Program, section 5.3 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case | R-UNI-24; CTL-09; CTL-11 | TC-E2-016-01 to TC-E2-016-12 |
| REQ-OCC-008 | History timeline of every state change, transfer, contact, document and decision | Business Requirements Epic 2, sections 3.3 and 4 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case; All recovery processes | None | TC-E2-016-01 |

### 19. Out of scope

- The next action on the case and in every queue view (REQ-WKM-014, RWB-E2-035).
- The clocks and deviations panels (RWB-E2-015).
- The decision log query screen for audit (SCR-38, P7).
- Accounts, parties and collateral sections of the record view (RWB-E1-023, P4 FEAT-ACA-12).


---

## RWB-E2-017 Contract, CA and mortgage document generation screens

| Item | Value |
|---|---|
| Story key | RWB-E2-017 |
| Epic | E2, release 31 December 2026 |
| Module | P5 Document hub |
| Feature | FEAT-OCC-07 Generate contract, credit approval and mortgage documents |
| Requirement IDs | REQ-DCM-012, REQ-OCC-002 |
| BRD section | Business Requirements Epic 2, section 3.5 |
| L3 process | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence |
| Decision | D6.4, D6.5 |
| Priority | Must |
| Depends on | RWB-E2-026, RWB-E1-034, RWB-E1-054, RWB-TE-012 |
| Status | Ready for build |

### 1. Story

As a **restructuring officer (FCR)**, I want **screens to generate the agreement, the credit approval and the mortgage documents from templates with the case facts, review them and send them for signature**, so that **deed in lieu and restructure documents are produced without re-keying**.

### 2. Business rationale

The officer today copies case facts into three Word files, prints them and walks them to signature, and a late change is made by hand on the printed copy with no record. These screens produce the set from the approved treatment through the generation engine, let the officer correct an allowed value with a recorded reason, and send the reviewed set for signature as write-once documents. It meets REQ-DCM-012 and REQ-OCC-002, applies CTL-12 and CTL-14 to the set, and shortens the restructure turnaround, which the program targets at 5 days from 23 days.

### 3. Preconditions

- RWB-E2-026 (generation engine), RWB-E1-034 (template versions with Legal approval), RWB-E1-054 (review endpoint) and RWB-TE-012 (write-once container) are done.
- RWB-E2-018 provides SignatureRequests in P6; until it is merged the send step is behind its flag.
- The document set per treatment type is in reference data: DEED_IN_LIEU uses DIL-CONTRACT, DIL-CA and DIL-MORTGAGE; RESTRUCTURE uses RES-AGREEMENT (assumed; DL28).
- The merge field catalog marks each merge field as overridable or locked. Amounts, parties, title numbers and the treatment terms are locked; dates of signing and witness details are overridable (assumed; DL28).
- CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT are legal types in the document type table (assumed; DL19).
- The officer holds RW-RESTRUCT (Documents CRU, Treatment and offer CRUA) with scope over the case.

### 4. Flow

1. Restructuring officer: opens SCR-14 Treatment record for an approved deed in lieu treatment and chooses Generate documents.
2. System: shows the document set for the treatment type and product, with the current approved version of each template.
3. Restructuring officer: confirms; the system calls the generation engine (RWB-E2-026) and shows the three drafts with their merge values.
4. Restructuring officer: opens a draft; the system shows the PDF next to the list of merge values, with locked values read only.
5. Restructuring officer: corrects an overridable value and enters the reason.
6. System: writes a decision log entry with the override and its reason, regenerates the draft as the next doc_version, and keeps the earlier version readable.
7. Restructuring officer: marks each draft reviewed; the system sets state REVIEWED.
8. Restructuring officer: chooses Send for signature.
9. System: checks every document of the set is REVIEWED, copies each final file to the write-once container, writes the decision log entry for the send, starts the signature request in P6 and sets each document to state SENT with write_once true.
10. System: shows MSG-P5-012; the documents show as sent on SCR-30 Case documents.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The treatment is not approved or is closed | Generate is refused | MSG-P5-011 | AC4 |
| X2 | A correction has no reason | 422; nothing changes | MSG-GEN-001 | AC5 |
| X3 | The value is locked in the merge field catalog | 422; nothing changes | MSG-P5-014 | AC6 |
| X4 | Send with a document of the set not reviewed | 422; nothing sent | MSG-P5-013 | AC7 |
| X5 | A change to a document already sent | 409; nothing changes | MSG-P5-002 | AC8 |
| X6 | The decision log write fails on a correction or a send | 503; nothing changes | MSG-P7-003 | AC9 |
| X7 | Send is chosen twice | One signature request; the second call returns the first result | None | AC10 |
| X8 | Two officers correct the same draft | The second save gets 409 | MSG-GEN-004 | AC11 |
| X9 | The signature service refuses the request | 503; documents stay REVIEWED | MSG-GEN-006 | AC12 |
| X10 | The template version changed after the drafts were made | Send is refused; the officer regenerates | MSG-P5-013 | AC13 |
| X11 | The user holds Documents R only | Actions hidden; a direct call gets 403 | MSG-P4-002 | Access test TC-E2-017-14 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the engine (RWB-E2-026) in the same epic and the write-once container from Epic 1 |
| Negotiable | The set per treatment type and which fields may be overridden are data owned by Legal |
| Valuable | The officer produces and sends the set without re-keying |
| Estimable | Two new endpoints, one reused endpoint, one panel on SCR-14, one review view on SCR-30 |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic data |

### 7. Acceptance criteria

```gherkin
Feature: Contract, CA and mortgage document generation screens

  Background:
    Given case "RW-2026-000401" with product group "MORTGAGE" in team "FCR-BKK"
    Given treatment "TRT-0401" of type "DEED_IN_LIEU" approved at D6.4 with no outcome
    Given the set for "DEED_IN_LIEU" is "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, all approved by Legal
    Given a restructuring officer with role RW-RESTRUCT and scope team "FCR-BKK"

  Scenario: AC1 Generate
    Given the officer opens SCR-14 for "TRT-0401"
    When the officer chooses Generate documents and confirms
    Then the system produces three documents from the current template versions with the case facts filled
    Then they show as drafts of types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT" with template versions 2, 1 and 1

  Scenario: AC2 Review
    Given the contract draft "DOC-0411" at doc_version 1 has contract_date "2026-12-10"
    When the officer corrects contract_date to "2026-12-12" with reason "Signing appointment moved by the customer"
    Then the system writes a decision log entry with decision code "D6.4", the old and new value and the reason as override_reason
    Then the system regenerates "DOC-0411" as doc_version 2 showing "12 ธันวาคม 2569"
    Then doc_version 1 stays readable

  Scenario: AC3 Send
    Given the three drafts of "TRT-0401" are in state "REVIEWED"
    When the officer chooses Send for signature
    Then each file is in the write-once container and each document has write_once true and state "SENT"
    Then the system starts one signature request for the three documents in P6
    Then the system writes a decision log entry with final_call "SENT_FOR_SIGNATURE"
    Then the screen shows MSG-P5-012 with count 3

  Scenario: AC4 Generate for a treatment that is not approved
    Given treatment "TRT-0402" of type "DEED_IN_LIEU" has no decision_log_id
    When the officer opens SCR-14 for "TRT-0402"
    Then the system disables generate documents with MSG-P5-011
    Then a direct call to POST generated-documents returns 409 with MSG-P5-011

  Scenario: AC5 A correction without a reason
    Given the draft "DOC-0411"
    When the officer corrects contract_date with an empty reason
    Then the response is 422 with MSG-GEN-001 naming "Reason"
    Then "DOC-0411" stays at its doc_version

  Scenario: AC6 A locked value cannot be corrected
    Given transfer_price is locked in the merge field catalog
    When the officer tries to change transfer_price on "DOC-0411" from 1250000.00 to 1200000.00
    Then the response is 422 with MSG-P5-014 naming "Transfer price"
    Then nothing changes

  Scenario: AC7 Send with a draft not reviewed
    Given two drafts of "TRT-0401" are "REVIEWED" and "DIL-MORTGAGE" is still "DRAFT"
    When the officer chooses Send for signature
    Then the response is 422 with MSG-P5-013 naming the mortgage document
    Then the system copies no document to the write-once container and no signature request starts

  Scenario: AC8 A sent document cannot be changed
    Given "DOC-0411" is in state "SENT"
    When the officer tries to correct contract_date
    Then the response is 409 with MSG-P5-002
    Then "DOC-0411" is unchanged

  Scenario: AC9 The decision log write fails on a correction
    Given the decision log store does not accept writes
    When the officer corrects contract_date on "DOC-0411" with a reason
    Then the response is 503 with MSG-P7-003
    Then "DOC-0411" stays at its doc_version and no file is added

  Scenario: AC10 Send chosen twice
    Given the officer chose Send for signature for "TRT-0401" with Idempotency-Key "S-0401"
    When the same request with Idempotency-Key "S-0401" arrives again
    Then the response returns the same three documents in state "SENT"
    Then only one signature request exists for "TRT-0401"

  Scenario: AC11 Two officers correct the same draft
    Given two officers opened "DOC-0411" at version 4
    Given the first officer saved a correction, so the record is at version 5
    When the second officer saves a correction with version 4
    Then the response is 409 with MSG-GEN-004

  Scenario: AC12 The signature service refuses the request
    Given SignatureRequests in P6 returns "UNAVAILABLE"
    When the officer chooses Send for signature for the three reviewed drafts
    Then the response is 503 with MSG-GEN-006 naming "e-signature"
    Then the documents stay in state "REVIEWED"
    Then a second send after the service returns completes with one signature request

  Scenario: AC13 The template changed after the drafts were made
    Given the three drafts were made from "DIL-CONTRACT" version 2
    Given "DIL-CONTRACT" version 3 became current after the drafts were made
    When the officer chooses Send for signature
    Then the response is 422 with MSG-P5-013 naming the contract and "template version 3"
    Then the system sends no document
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The set of templates for a treatment comes from reference data by treatment type and product group | Template catalog (RWB-E1-046); DL28 |
| BR2 | Only an approved, open treatment can have its set generated | DF-TRT-003, DF-TRT-013; R-DIL-14; R-DIL-16 |
| BR3 | Only an overridable merge field can be corrected, and only with a reason | Merge field catalog; R-UNI-14 (coded reason when departing from the system result) |
| BR4 | Each correction is written to the decision log with the old value, the new value and the reason before the draft is regenerated | Principle 5; CTL-07 |
| BR5 | A correction creates the next doc_version; earlier versions stay readable | FEAT-DCM-20; DF-DOC-011 |
| BR6 | A set is sent only when every document is REVIEWED and every document was made from the current template version | CTL-14; R-LIT-03 |
| BR7 | On send, legal types are copied to the write-once container and cannot be changed after | CTL-12; VR-P5-001-2; RWB-TE-012 |
| BR8 | The signature path (e-signature or wet ink) is chosen by P6 by product and Legal rule | R-DIL-18; R-RES-16; REQ-OCC-009 |
| BR9 | A send that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR10 | A repeat send with the same Idempotency-Key returns the first result | R-UNI-40 |

### 9. State transitions

None. This story does not change a case status. It changes the document state.

| From | Event | Condition | To |
|---|---|---|---|
| document state DRAFT | Correction saved | Overridable field, reason given, decision log written | DRAFT, doc_version + 1 |
| document state DRAFT | Marked reviewed | None | REVIEWED |
| document state REVIEWED | Correction saved | As above | DRAFT, doc_version + 1 |
| document state REVIEWED | Send for signature | All of the set REVIEWED, current template version, decision log written, signature request accepted | SENT, write_once true |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Generates, corrects, marks reviewed and sends in scope (Documents CRU) |
| RW-CASEOWN, case owner | Generates, corrects, marks reviewed and sends in scope (Documents CRU) |
| RW-TEAMMGR, team manager | Reads the drafts and sent documents (Documents R) |
| RW-LEGAL, legal counsel | Reads the set; owns which fields are overridable (Documents CRUA) |
| SY-DECLOG, decision log writer | Writes the correction and send entries |

No approval level from the delegation of authority applies; the treatment was approved at D6.4 before generation.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-003 | treatment | decision_log_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-REF-046 | template | template_code | Read |
| DF-REF-047 | template | template_version | Read |
| DF-REF-051 | template | approved_by_legal | Read |
| DF-DOC-001 | document | id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-006 | document | storage_ref | Write |
| DF-DOC-008 | document | review_status | Write |
| DF-DOC-010 | document | write_once | Write |
| DF-DOC-011 | document | doc_version | Write |
| DF-DOC-032 | document | template_id | Read |
| DF-DOC-033 | document | treatment_id | Read |
| Standard column | document | state, version | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /api/recovery/v1/cases/{caseId}/generated-documents** (defined in RWB-E2-026): used for step 3.

**POST /documents/{documentId}/regenerate** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | RegenerateRequest: overrides (array of mergeField, value, reason; 1 to 10), version (integer) |
| Response | Document at the new doc_version |
| Errors | 401; 403 no Documents U (MSG-P4-002); 404 (MSG-P4-003); 409 document SENT (MSG-P5-002) or stale version (MSG-GEN-004); 422 empty reason (MSG-GEN-001), locked field (MSG-P5-014), missing value after override (MSG-P5-009); 503 decision log write failed (MSG-P7-003) |
| Authorization | Documents, right U, scope applied |
| Idempotency | Idempotency-Key header |

**POST /api/recovery/v1/documents/{documentId}/review** (new in RWB-E1-054), action COMPLETE: sets a generated draft to state REVIEWED.

**POST /treatments/{treatmentId}/signature-requests** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | SendForSignatureRequest: treatmentId (uuid), documentIds (array of uuid), header Idempotency-Key (required) |
| Response | 200 DocumentPage with the sent documents |
| Errors | 401; 403 no Documents U (MSG-P4-002); 404 (MSG-P4-003); 409 a document already SENT (MSG-P5-002); 422 a document not REVIEWED or not on the current template version (MSG-P5-013); 503 decision log write failed (MSG-P7-003) or signature service unavailable (MSG-GEN-006) |
| Authorization | Documents, right U, scope applied |
| Idempotency | Idempotency-Key header, kept 24 hours |

**Published interface called (P6, RWB-E2-018)**

```java
package recovery.comms.signature;
public interface SignatureRequests {
    SignatureStart start(UUID caseId, UUID treatmentId, List<UUID> documentIds, String idempotencyKey); // ACCEPTED with requestId, or UNAVAILABLE
}
```

**Published interface called (P5, RWB-E2-026):** DocumentGenerator.generate(GenerationRequest) with overrides for the regenerate step.

### 13. Solution plan

**Package.** folder `recovery/dochub/generation/ui` for the controller and service, Java package `recovery.dochub.generation`; front end folder `recovery/dochub/generation`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| GeneratedDocumentController | Controller | Adds POST /documents/{documentId}/regenerate and POST /cases/{caseId}/generated-documents/send |
| DocumentSetService | Service | Regenerate with overrides (BR3 to BR5), mark reviewed, send (BR6, BR7, BR9, BR10) |
| BlobStorageAdapter | Service | From RWB-E1-024; copies final files to the write-once container, idempotent by file hash through ContentHashGuard (RWB-TE-012) |
| DocumentHubRepository | Repository | Document state, version and write_once updates |
| GenerateDocumentsPanel | React component | On SCR-14: the set, template versions, Generate and Send buttons, disabled states |
| GeneratedDocumentReview | React component | On SCR-30: PDF preview, merge values with locked ones read only, correction form with reason, Mark reviewed |

**Database**

- Updates document (storage_ref, review_status, write_once, doc_version, state, version, updated_at, updated_by). Reads template_code, template_version, treatment_id added by RWB-E2-026.
- Writes decision_log_entry through DecisionLogWriter only. No new table.

**Configuration and reference data**

- Template set per treatment type and product, and overridable or locked per merge field (P6 template catalog, RWB-E1-046; owner legal counsel; DL28).
- Legal flag per document type (document type table, DL19).
- document_hub_parameter row GEN_IDEMPOTENCY_HOURS 24 (assumed), from RWB-E2-026.

**Build steps**

1. Build the regenerate endpoint: version check, SENT check, locked and reason checks, decision log write, call DocumentGenerator with overrides, store as next doc_version.
2. Extend POST /documents/{documentId}/review action COMPLETE for GENERATED drafts: set state REVIEWED and review_status CONFIRMED or CORRECTED.
3. Build the send endpoint: idempotency, BR6 checks, write-once copy, decision log write, SignatureRequests.start, state SENT, in that order with the failure handling of AC9 and AC12.
4. Build GenerateDocumentsPanel on SCR-14 with the disabled state and MSG-P5-011.
5. Build GeneratedDocumentReview on SCR-30 with the correction form and the read-only state for locked fields and for RW-TEAMMGR.
6. Add contract tests for the two new endpoints (RWB-TE-003) and browser tests (RWB-TE-010).

**Feature flag:** `rwb.dochub.generation-screens`, with `rwb.dochub.generation-screens.send` for the send step until RWB-E2-018 is merged. Off: the panel is hidden.

**Done when:** the tests in section 16 pass and a restructuring officer generates, corrects and sends one synthetic deed in lieu set in UAT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-011 | Treatment not approved or not open | Documents can be generated only for an approved {treatment} that is still open. |
| MSG-P5-012 | Set sent for signature (new) | {count} documents were sent for signature. |
| MSG-P5-013 | Send with a document not reviewed or on an old template version (new) | {document} cannot be sent yet: {reason}. |
| MSG-P5-014 | Correction to a locked merge field (new) | {field} comes from the approved treatment and cannot be changed here. |
| MSG-P5-002 | Change to a sent document | Legal documents cannot be changed. Add a new version instead. |
| MSG-GEN-001 | Correction without a reason | Enter {field}. |
| MSG-GEN-004 | Saved against an old version | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | Signature service unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without Documents U | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-14 Treatment record | Approved | Sees the document set with template versions; chooses Generate documents; Send for signature when all are reviewed |
| SCR-14 Treatment record | Draft, submitted | Generate documents is disabled with MSG-P5-011 |
| SCR-30 Case documents | List | Opens a draft, sees the PDF and the merge values, corrects an overridable value with a reason, marks it reviewed |
| SCR-30 Case documents | Read only (common state) | A sent document, or any document for RW-TEAMMGR, shows without edit controls |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-017-01 | AC1, BR1, BR2 | System | Synthetic mortgage DIL treatment, three approved templates |
| TC-E2-017-02 | AC2, BR3, BR4, BR5 | System | Contract date moved by two days |
| TC-E2-017-03 | AC3, BR6, BR7, BR8 | System | Three reviewed drafts; P6 stub returns ACCEPTED |
| TC-E2-017-04 | AC4, BR2 | System | Treatment with no decision_log_id |
| TC-E2-017-05 | AC5, BR3 | System | Empty reason |
| TC-E2-017-06 | AC6, BR3 | System | Locked transfer price |
| TC-E2-017-07 | AC7, BR6 | System | One draft not reviewed |
| TC-E2-017-08 | AC8, BR7 | System | Document in state SENT |
| TC-E2-017-09 | AC9, BR4 | System | Decision log stub refusing writes on a correction |
| TC-E2-017-10 | AC10, BR10 | System | Same send key twice |
| TC-E2-017-11 | AC11 | System | Two sessions on one draft |
| TC-E2-017-12 | AC12 | System | P6 stub returns UNAVAILABLE, then ACCEPTED |
| TC-E2-017-13 | AC13, BR6 | System | Template version 3 made current after the drafts |
| TC-E2-017-14 | Access | Access | RW-TEAMMGR user (Documents R) calls POST generated-documents/send; refused with MSG-P4-002 |
| TC-E2-017-15 | Principle 5 | Resilience | Decision log write forced to fail on send; nothing sent, documents stay REVIEWED, MSG-P7-003, incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the set per treatment type, the locked and overridable fields and the legal flag are data.
- No personal data in logs, tests or prompts: merge values, reasons and file names are not logged; tests use synthetic parties.
- No read of another module's tables: treatments, templates and signature requests are reached through published interfaces.
- A document copied to the write-once container is never changed; a later change is a new document version created before send only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-DIL-18, R-UNI-39, R-UNI-40 | TC-E2-017-01 to TC-E2-017-12, TC-E2-017-14, TC-E2-017-15 |
| REQ-OCC-002 | Templates versioned with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03 | TC-E2-017-01, TC-E2-017-13 |

### 19. Out of scope

- The generation engine, template selection and merge rules (RWB-E2-026).
- The e-signature flow, the wet ink path and the return of the signed copy (RWB-E2-018).
- Rule-driven generation on the deed in lieu route (FEAT-TRT-18, Epic 3).
- Settlement offer letters (R-SET-04, Epic 3).


---

## RWB-E2-018 E-signature flow for customers and the bank

| Item | Value |
|---|---|
| Story key | RWB-E2-018 |
| Epic | E2, release 31 December 2026 |
| Module | P6 Communications |
| Feature | FEAT-OCC-08 Run the e-signature flow for the customer and the bank; FEAT-OCC-09 Record the signature result on the case |
| Requirement IDs | REQ-OCC-009 |
| BRD section | Business Requirements Epic 2, sections 3.6 and 4 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D6.4 |
| Priority | Must |
| Depends on | RWB-E2-017, RWB-E2-022 |
| Status | Ready for build |

### 1. Story

As a **customer (CU-BORROW)**, I want **to sign the agreement on EasyApp or at a branch, with the bank signature added and the signed document returned to the case**, so that **a settlement completes without paper where the law allows**.

### 2. Business rationale

Agreements are printed, signed and couriered today, and the case waits days for the signed copy before booking can start. This story sends the generated agreement for e-signature where Legal permits it, takes branch and paper signatures where Legal requires wet ink, stores the signed copy on the case and records signed or not signed on the treatment, which is the event the routing rules R-RES-16, R-SET-10 and R-DIL-18 act on. It serves REQ-OCC-009.

### 3. Preconditions

- RWB-E2-017 is done: the agreement, credit approval and mortgage documents are generated on the case and stored in the document hub.
- RWB-E2-022 is done: the conduct check for outbound contact is available.
- Each agreement template carries its signature basis: E_SIGNATURE_ALLOWED or WET_INK_REQUIRED, approved by Legal counsel (RWB-E1-046).
- The treatment exists with type, offer validity date and state Offer with customer (RWB-E2-004).
- EasyApp e-signature is reached through the ACE common module (INT-34) with the bank signing certificate held in the key store, assumed; DL12 and DL06. It is not yet in the integration inventory.
- The requester holds RW-RESTRUCT or RW-CASEOWN (Treatment and offer C and U).

### 4. Flow

1. Restructuring officer: on SCR-14 Treatment record chooses Send for signature on a generated agreement.
2. System: reads the signature basis of the agreement's template; offers E-signature only when the basis is E_SIGNATURE_ALLOWED, otherwise Branch or Paper.
3. System: runs the conduct check for the customer (RWB-E2-022); a contact stop or legal hold refuses the request.
4. System: creates the signature request (method, document, party, expiry equal to the treatment's offer validity) and, for E-signature, writes the send to the outbox for the ACE path to EasyApp.
5. Customer: signs in EasyApp; EasyApp adds the bank signature with the bank certificate and returns the signed PDF through the ACE path.
6. System: stores the signed PDF as a new write-once version of the agreement on the case, sets the request Signed and calls TreatmentApi.recordSignature, which raises CUSTOMER_SIGNED in P3.
7. Customer at a branch: signs the paper agreement; the branch scan arrives through JOB-12 Document intake; the restructuring officer links the scan and records Signed.
8. For a deed in lieu with WET_INK_REQUIRED: the officer records the paper signature with the scan; P3 receives CUSTOMER_ACCEPTED with signature basis wet ink and routes to the field inspection and then the Land Office transfer (R-DIL-18, R-DIL-27).
9. System: a decline in EasyApp sets the request Declined and records not signed; an expiry from P3 cancels the request.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | E-signature requested for a document whose template requires wet ink | Refused | MSG-P6-009 | AC4 |
| X2 | The customer declines in EasyApp | Request Declined; treatment not signed | None | AC5 |
| X3 | The offer validity passes with no signature | Request Expired; a later result is refused | None | AC6 |
| X4 | A contact stop is in force | Request refused | MSG-P6-001 | AC7 |
| X5 | The ACE path to EasyApp is unavailable | Send queued and retried | MSG-GEN-006 | AC8 |
| X6 | The same signing result arrives twice | Ignored and counted | None | AC9 |
| X7 | A signing result names no known request | Held on the exception queue | None | AC10 |
| X8 | A branch or paper signature recorded with no scan | Refused | MSG-GEN-001 | AC11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses documents from RWB-E2-017 and the conduct check from RWB-E2-022; booking after signature is Epic 3 |
| Negotiable | The signature basis per template and the expiry are data; the EasyApp path is the bank's |
| Valuable | A signed copy is on the case within a minute of signing, and routing starts from it |
| Estimable | Three endpoints, one result listener, one table |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs with the EasyApp path stubbed |

### 7. Acceptance criteria

```gherkin
Feature: E-signature flow for customers and the bank

  Background:
    Given case "RC-2026-000888" has settlement treatment "T-0501" with offer validity 2026-12-20 and state "OFFER_WITH_CUSTOMER_SET"
    Given agreement document "D-0601" on the case was generated from template "SET-AGREE" "TH" with signature basis "E_SIGNATURE_ALLOWED"
    Given the borrower is party "P-0088" with no contact stop

  Scenario: AC1 Customer signs
    Given "RS-0301" sent "D-0601" for e-signature to party "P-0088" on 2026-12-10
    When EasyApp returns signing result "SIGNED" with the bank signature applied at 2026-12-11 10:15:00
    Then within 60 seconds version 2 of "D-0601" holding the signed PDF is stored on case "RC-2026-000888" with write_once true
    Then the signature request has status "SIGNED" and signed at 2026-12-11 10:15:00
    Then the system calls treatmentApi.recordSignature for "T-0501" with signed true and method "E_SIGNATURE"

  Scenario: AC2 Branch
    Given "RS-0301" created a signature request for "D-0601" with method "BRANCH"
    Given the branch scan "D-0602" of the signed agreement arrived through document intake on 2026-12-12
    When "RS-0301" records result "SIGNED" with signed document "D-0602" and signed date 2026-12-12
    Then the signature request has status "SIGNED" and method "BRANCH"
    Then the system links "D-0602" to the case as the signed agreement
    Then the system calls treatmentApi.recordSignature for "T-0501" with signed true and method "BRANCH"

  Scenario: AC3 DIL paper
    Given case "RC-2026-000889" has deed in lieu treatment "T-0502" for product "MORTGAGE"
    Given its contract document "D-0701" was generated from template "DIL-CONTRACT-MTG" with signature basis "WET_INK_REQUIRED"
    Given "RS-0301" created a signature request for "D-0701" with method "PAPER"
    When "RS-0301" records result "SIGNED" with scan "D-0702" and signed date 2026-12-14
    Then the signature request has status "SIGNED" and method "PAPER"
    Then the system calls treatmentApi.recordSignature for "T-0502" with signed true and method "PAPER"
    Then P3 receives event CUSTOMER_ACCEPTED with signature basis "WET_INK" and moves the case to "WITH_FIELD_INSPECTION" under R-DIL-18

  Scenario: AC4 E-signature refused where Legal requires wet ink
    Given document "D-0701" has signature basis "WET_INK_REQUIRED"
    When "RS-0301" sends POST /treatments/T-0502/signature-requests with method "E_SIGNATURE" for "D-0701"
    Then the response is status 409 with MSG-P6-009 naming "DIL-CONTRACT-MTG"
    Then the system sends no request to EasyApp

  Scenario: AC5 Customer declines
    Given "D-0601" was sent for e-signature on 2026-12-10
    When EasyApp returns signing result "DECLINED" on 2026-12-11
    Then the signature request has status "DECLINED"
    Then the system calls treatmentApi.recordSignature for "T-0501" with signed false

  Scenario: AC6 Offer validity passes with no signature
    Given "D-0601" was sent for e-signature on 2026-12-10 and has status "SENT"
    Given P3 raised OFFER_EXPIRED for "T-0501" on 2026-12-21 and called SignatureApi.cancel
    When EasyApp returns signing result "SIGNED" for that request on 2026-12-21
    Then the signature request keeps status "EXPIRED"
    Then the system holds the result on the exception queue
    Then the system does not call treatmentApi.recordSignature

  Scenario: AC7 Contact stop
    Given case "RC-2026-000888" has an open deviation "X2" with contact stop on
    When "RS-0301" sends "D-0601" for e-signature
    Then the response is status 409 with MSG-P6-001 naming "X2 Vulnerable customer or hardship"
    Then the system sends no request to EasyApp

  Scenario: AC8 EasyApp path unavailable
    Given the ACE path to EasyApp returns "unavailable"
    When "RS-0301" sends "D-0601" for e-signature
    Then the response is status 201 with status "QUEUED" and MSG-GEN-006 naming "EasyApp"
    Then JOB-11 retries the send until it is accepted or the retry limit of 5 is reached

  Scenario: AC9 Signing result repeated
    Given the signing result "SIGNED" for request reference "EA-30001" was applied
    When the same result for "EA-30001" arrives again
    Then the system stores no second document
    Then the system calls treatmentApi.recordSignature once
    Then the system counts the repeat under rule R-UNI-40

  Scenario: AC10 Unknown request reference
    Given no signature request has external reference "EA-99999"
    When EasyApp returns a signing result for reference "EA-99999" that matches no request
    Then the system holds the result on the exception queue with reason "unknown signature request"
    Then the system stores no document

  Scenario: AC11 Branch result without a scan
    Given a signature request for "D-0601" with method "BRANCH"
    When "RS-0301" records result "SIGNED" with no signed document
    Then the response is status 422 with MSG-GEN-001 naming "signed document"
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A customer signs electronically only where the template's signature basis allows it, and by wet ink where Legal requires it | REQ-OCC-009; template signature basis approved by Legal |
| BR2 | A signed offer routes to operations for booking | R-RES-16, R-SET-10 |
| BR3 | A mortgage deed in lieu with a wet ink signature goes to the collateral inspection before the Land Office transfer | R-DIL-18, R-DIL-27 |
| BR4 | A decline returns the case under the route set's decline rule | R-RES-17 |
| BR5 | No signature by the end of the offer validity ends the offer | R-RES-18, R-SET-11 |
| BR6 | A signature request to the customer is an outbound contact and passes the conduct check | CTL-16; R-SET-12 |
| BR7 | The signed document is write-once on the case | CTL-12; DT06 |
| BR8 | The same result twice has one effect | R-UNI-40 |
| BR9 | A system that is unavailable queues the send and retries | R-UNI-33 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Waiting customer | Customer responds, or the validity timer expires | Signature recorded, decline recorded, or OFFER_EXPIRED | In progress |

P3 makes the case status change on the treatment update this story sends. This story sets the signature request status: Queued, Sent, Signed, Declined, Expired.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| CU-BORROW, customer (borrower) | Signs or declines in EasyApp, or signs at a branch; no Workbench login |
| RW-RESTRUCT, restructuring officer (FCR) | Creates signature requests and records branch and paper results (Treatment and offer CRUA) |
| RW-CASEOWN, case owner | Creates requests and records results on own cases (Treatment and offer CRU) |
| RW-LEGAL, Legal counsel | Sets the signature basis on the template (Documents A, RWB-E1-034); reads requests (Treatment and offer R) |
| SY-CASEWF, case workflow module | Receives the treatment update; calls cancel on offer expiry |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-PTY-001 | party | id | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-010 | treatment | valid_until | Read |
| DF-TRT-030 | treatment | signature_status | Write, through the treatment interface |
| DF-DOC-105 | signature_request | signed_at | Write, through the treatment interface |
| DF-DOC-001 | document | id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-011 | document | doc_version | Write, through the document hub interface |
| DF-DOC-006 | document | storage_ref | Write, through the document hub interface |
| DF-DOC-010 | document | write_once | Write, through the document hub interface |
| DF-REF-068 | template | signature_basis | Read |
| DF-DOC-096 | signature_request | id | Write |
| DF-DOC-097 | signature_request | case_id | Write |
| DF-DOC-098 | signature_request | treatment_id | Write |
| DF-DOC-099 | signature_request | document_id | Write |
| DF-DOC-100 | signature_request | party_id | Write |
| DF-DOC-101 | signature_request | method | Write |
| DF-DOC-102 | signature_request | status | Write |
| DF-DOC-103 | signature_request | external_ref | Write |
| DF-DOC-104 | signature_request | sent_at | Write |
| DF-DOC-105 | signature_request | signed_at | Write |
| DF-DOC-106 | signature_request | signed_document_id | Write |
| DF-DOC-107 | signature_request | expires_at | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

All three endpoints are new and recorded in the additions file. Base path /api/recovery/v1.

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| POST /treatments/{treatmentId}/signature-requests | SignatureRequestCreate: documentId, partyId, method (E_SIGNATURE, BRANCH, PAPER) | 201 SignatureRequest | 401; 403 (MSG-P4-002); 404 (MSG-P4-003); 409 wet ink required (MSG-P6-009), contact stop (MSG-P6-001), legal hold (MSG-P3-004), treatment not with the customer (MSG-P3-005); 422 (MSG-GEN-001); 503 (MSG-GEN-006) | Treatment and offer C | Idempotency-Key header |
| GET /treatments/{treatmentId}/signature-requests | None | 200 SignatureRequest[] | 401, 403, 404, 503 | Treatment and offer R | Not applicable |
| POST /signature-requests/{requestId}/result | SignatureResultRequest: result (SIGNED, DECLINED), signedDocumentId, signedAt | 200 SignatureRequest | 401; 403; 404; 409 request not open (MSG-P3-005); 422 scan missing (MSG-GEN-001); 503 | Treatment and offer U | Idempotency-Key header |

SignatureRequest schema: id, caseId, treatmentId, documentId, partyId, method, status, externalRef, sentAt, signedAt, signedDocumentId, expiresAt.

**Published interfaces**

```java
// P6, called by the ACE common module when EasyApp returns a result
void SignatureResultListener.onEasyAppResult(String externalRef, String result, byte[] signedPdf, Instant signedAt);
// P6, called by P3 on OFFER_EXPIRED
void SignatureApi.cancel(UUID treatmentId, String reasonCode);
// Owned elsewhere
EsignAck EsignPort.send(EsignRequest request);                                         // ACE common module, INT-34
void TreatmentApi.recordSignature(UUID treatmentId, boolean signed, String method, Instant at); // P3, RWB-E2-004
DocumentRef DocumentHubApi.addVersion(UUID documentId, byte[] pdf, String reason);         // P5, signed copy as a new version
void DocumentHubApi.linkSigned(UUID sourceDocumentId, UUID signedDocumentId);           // P5
```

Target: the signed document is on the case within 60 seconds of the result reaching the Workbench, assumed; DL11. Sends go through JOB-11 Outbox sender with a retry limit of 5 (DL11).

### 13. Solution plan

- Package: folder `recovery/comms/esign`, Java package `recovery.comms.esign`; front end folder `recovery/comms/esign`.

| Component | Type | Responsibility |
|---|---|---|
| SignatureRequestEntity | Entity | Maps table signature_request |
| SignatureRequestRepository | Repository | Reads and writes signature_request; finds by external_ref |
| SignatureController | Controller | The three endpoints |
| SignatureService | Service | Method check against the signature basis, conduct check, outbox write, result recording |
| SignatureResultListener | Published interface | Applies EasyApp results: signed copy as a new document version, treatment update; idempotent on external_ref and result |
| SignatureApiService | Published interface | Implements SignatureApi.cancel |
| SendForSignatureDialog | React component | On SCR-14: method choice limited by the basis, result recording with scan picker |

- Database: new table signature_request with unique index on external_ref and index on (treatment_id, status); check constraint on method and status. Flyway migration `V2_018__signature_request.sql`.
- Configuration and reference data: signature basis per template (Legal counsel, RWB-E1-034); lists for method (E_SIGNATURE, BRANCH, PAPER) and request status (QUEUED, SENT, SIGNED, DECLINED, EXPIRED), recorded as additions; retry limit 5 and the 60-second target (DL11).
- Build steps:
  1. Write the migration and the entity; test the constraints.
  2. Build SignatureService.create with the basis and conduct checks; test AC4 and AC7.
  3. Add the outbox send through EsignPort with retry; test AC8 with the port stubbed.
  4. Build SignatureResultListener with addVersion, recordSignature and idempotency; test AC1, AC5, AC9, AC10.
  5. Build the branch and paper result endpoint; test AC2, AC3 and AC11.
  6. Build SignatureApi.cancel and the expired-result handling; test AC6.
  7. Build SendForSignatureDialog on SCR-14; browser test of the method choice for both bases.
- Feature flag: `rwb.comms.esign`.
- Done when: the tests in section 16 pass, and one end-to-end signature with the EasyApp test tenant passes in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-009 | E-signature asked for a document that needs wet ink | Legal requires a wet ink signature for {document}. Use the branch or paper path. |
| MSG-P6-001 | A contact stop is in force | Contact with this customer is stopped for {reason}. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-GEN-006 | The EasyApp path is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-GEN-001 | A branch or paper result has no scan | Enter {field}. |
| MSG-P3-005 | The request is not open, or the treatment is not with the customer | This case cannot move to {state} from {current}. |

### 15. Screens and states

SCR-14 Treatment record (states Draft; submitted; approved; booked; broken): in state approved, while the offer is with the customer, the officer sees Send for signature and the request list with status. SCR-30 Case documents shows the signed copy linked to the generated agreement. SCR-09 Exception queue lists held signing results. The customer sees EasyApp only.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-018-01 | AC1, BR2, BR7 | System | T-0501 settlement; D-0601 E_SIGNATURE_ALLOWED; EasyApp stub SIGNED |
| TC-E2-018-02 | AC2, BR1 | System | Branch scan D-0602 |
| TC-E2-018-03 | AC3, BR1, BR3 | System | T-0502 DIL Mortgage; D-0701 WET_INK_REQUIRED; scan D-0702 |
| TC-E2-018-04 | AC4, BR1 | System | E_SIGNATURE on D-0701; method list offered for WET_INK_REQUIRED |
| TC-E2-018-05 | AC5, BR4 | System | EasyApp stub DECLINED |
| TC-E2-018-06 | AC6, BR5 | System | Cancel on 2026-12-21, then SIGNED result |
| TC-E2-018-07 | AC7, BR6 | System | Open X2 with contact stop |
| TC-E2-018-08 | AC8, BR9 | System | EsignPort stub unavailable |
| TC-E2-018-09 | AC9, BR8 | System | Result EA-30001 twice |
| TC-E2-018-10 | AC10 | System | Result EA-99999 |
| TC-E2-018-11 | AC11 | System | Branch SIGNED with no document |
| TC-E2-018-12 | Access | Access | RW-PHONECOL sends POST /treatments/{treatmentId}/signature-requests; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: signature basis, methods, statuses, expiry and the retry limit are data or configuration.
- No personal data in logs, tests or prompts. The signed PDF is stored, never logged; tests use synthetic PDFs.
- No read of another module's tables. Treatment, case, documents and deviations go through their interfaces; treatment fields are written only by P3.
- The bank signing certificate stays in the key store (NFR-052); the Workbench never holds the private key.
- No direct call to EasyApp; only the ACE common module path.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-009 | Electronic signature where Legal permits it, wet ink where Legal requires it | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-08, FEAT-OCC-09 | 7.3 Negotiate settlement or deed in lieu | R-RES-16, R-RES-17, R-RES-18, R-SET-10, R-SET-11, R-SET-12, R-DIL-18, R-DIL-27, R-UNI-33, R-UNI-40 | TC-E2-018-01 to TC-E2-018-12 |

### 19. Out of scope

- Booking the signed treatment in ALS and NLEADS (R-RES-22, Epic 3).
- The deed in lieu field inspection and Land Office transfer screens (Epic 3).
- Signature in customer self-service (FEAT-COM-02, Epic 4).
- Generating the documents to be signed (RWB-E2-017, RWB-E2-026).


---

## RWB-E2-019 Partner identities through the external gateway

| Item | Value |
|---|---|
| Story key | RWB-E2-019 |
| Epic | E2, release 31 December 2026 |
| Module | P4 Access and administration |
| Feature | FEAT-OCC-13 Give partners identities through the external gateway |
| Requirement IDs | REQ-ACA-012 |
| BRD section | Business Requirements Epic 2, section 3.4; Business Requirements Program, section 5.4 |
| L3 process | 12 Manage partners |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-022, RWB-E1-037, RWB-E1-039 |
| Status | Ready for build |

### 1. Story

As a **partner and agency manager (RW-AGENCYMG)**, I want **law firms, valuers and collection agencies to sign in to the partner portal with partner identities through the external gateway, with multi-factor authentication, one role per partner type and access limited to the work placed with their firm**, so that **partners can work in the Workbench from Epic 5 without SCB accounts, and a firm that leaves the panel loses access the same day**.

### 2. Business rationale

Partners today use separate channels (the LIT lawyer web, the OA portal, SVAF and SFTP), and the bank cannot show one record of what a firm could see. This story gives each partner user a partner identity separate from bank identities, binds it to one firm and one partner role, limits it to cases placed with that firm and to the instruction types of the role, and refuses access when the firm is suspended, exits the panel or reaches its contract end. It meets REQ-ACA-012 and NFR-050. Opening the Workbench to users outside the bank needs the architecture change under DL03, so the story is built and tested in SIT and UAT with the feature off in PROD until DL03 is approved; law firms are first needed at Epic 5 in March 2027.

### 3. Preconditions

- RWB-E1-022, RWB-E1-037 and RWB-E1-039 are done: sessions, the permission matrix with scope, and access events in the decision log.
- The partner role rows PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER and PT-RAMC are loaded with role class PARTNER_USER and their Entra ID groups, for example RWB-SIT-PT-LAWFIRM (Single sign-on sheet; names DL40). PT-LED has no login.
- The partner identity directory is reachable from the external gateway in SIT and UAT (INT-24); in PROD it waits for DL03.
- The partner table holds the panel firms with partner_type, panel_status and contract_end (S9 Partner management), read through the S9 published interface.
- Parameters in the catalog: rwb.access.partner.instruction-types.PT-LAWFIRM=FILE_SUIT,ENFORCE; rwb.access.partner.instruction-types.PT-VALUER=APPRAISE; rwb.access.partner.instruction-types.PT-AGENCY=COLLECT (assumed; owner RW-AGENCYMG); rwb.refload.approver.partner_user=RW-SECADM.

### 4. Flow

1. Partner and agency manager (RW-AGENCYMG): requests a partner user in the bank IAM, naming the firm, the partner role and the person's business e-mail at the firm.
2. Role owner: approves the request; access administrator creates the partner identity in the partner directory and adds it to the group of the partner role.
3. Reference data administrator (RW-REFADM): loads the partner user binding (partner identity, partner ID, role, valid from, valid to) with POST /admin/reference-loads table "partner_user"; RW-SECADM approves it.
4. Partner user: opens the partner portal through the external gateway and signs in with password and second factor.
5. Workbench (SessionResolver): checks the token comes from the partner directory, holds "mfa" in the amr claim and maps to exactly one partner role; finds the active binding for the identity.
6. Workbench (PartnerAccessService): asks the S9 interface for the firm's panel status and contract end; refuses the session unless the status is ACTIVE or ON_NOTICE and the contract end is today or later.
7. Workbench: resolves the session with scope PLACED, the partner ID and the instruction types of the role; writes an AC-SIGN entry.
8. Partner portal PRT-01 Partner home: lists the open instructions through GET /partner/instructions; the S9 handler applies the PLACED scope filter, so only instructions of the partner's firm and of the role's instruction types return.
9. Workbench: on each request, checks the binding and the firm status again (refreshed at most every 5 minutes, assumed; DL38) and ends the session when either has ended.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The firm is suspended or has exited the panel, or its contract end has passed | Sign-in refused; an open session ends at the next request; refusal logged | MSG-P4-008 | AC3 |
| X2 | The partner identity has no active binding to a firm | Session refused with 401; refusal logged | MSG-P4-001 | AC4 |
| X3 | The token has no second factor | Session refused with 401 | MSG-P4-005 | AC5 |
| X4 | A partner requests an instruction placed with another firm | Refused with 404; nothing returned | MSG-P4-003 | AC6 |
| X5 | A partner identity is in two partner role groups, or in a bank role group | Session refused; incident raised to the security administrator | MSG-P4-006 | AC7 |
| X6 | A partner calls an endpoint outside the partner role's letters, for example the case list | Refused with 403 | MSG-P4-002 | AC8 |
| X7 | A bank identity tries to sign in through the external gateway | Refused; bank users sign in only through the bank route | MSG-P4-001 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the session, the matrix and the access log from Epic 1; the partner instruction endpoints are S9's |
| Negotiable | Partner roles, instruction types and the binding are data; the PROD date follows DL03 |
| Valuable | One controlled way for partners into the Workbench, ready for law firms at Epic 5 |
| Estimable | One binding table, one partner check in the resolver, one scope type |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion below is one test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Partner identities through the external gateway

  Background:
    Given the environment is UAT and feature "rwb.access.partner-signin" is on
    Given partner "LF-0012" is a LAW_FIRM with panel status "ACTIVE" and contract end 30 June 2027
    Given partner "LF-0019" is a LAW_FIRM with panel status "ACTIVE"
    Given partner "VL-0004" is a VALUER with panel status "ACTIVE"

  Scenario: AC1 Partner sign-in
    Given partner identity "P-5101" is in group "RWB-UAT-PT-LAWFIRM" and bound to "LF-0012"
    Given 5 open instructions are placed with "LF-0012" and 3 with "LF-0019"
    When "P-5101" signs in through the external gateway with password and second factor
    Then the session holds role "PT-LAWFIRM", scope "PLACED" and partner "LF-0012"
    Then PRT-01 Partner home lists the 5 instructions of "LF-0012" and none of "LF-0019"
    Then one entry with decision code "AC-SIGN" and actor "P-5101" is written

  Scenario: AC2 Role per partner
    Given partner identity "P-5102" is in group "RWB-UAT-PT-VALUER" and bound to "VL-0004"
    Given "VL-0004" holds 2 instructions of type "APPRAISE" and 1 of type "LIST"
    When "P-5102" signs in
    Then PRT-01 Partner home lists the 2 "APPRAISE" instructions only

  Scenario: AC3 Revoked
    Given partner identity "P-5101" is bound to "LF-0012"
    Given "LF-0012" moves to panel status "EXITED" at 11:00 on 4 January 2027
    When "P-5101" tries to sign in at 11:20
    Then the system refuses access with message MSG-P4-008
    Then one entry with decision code "AC-DENY" and reason "PARTNER_NOT_ACTIVE" is written
    Then the system ends a session of "P-5101" opened at 10:00 at its first request after 11:05

  Scenario: AC4 A partner identity with no binding is refused
    Given partner identity "P-5103" is in group "RWB-UAT-PT-LAWFIRM" and has no active binding
    When "P-5103" signs in
    Then the system refuses the session with status 401 and message MSG-P4-001
    Then one entry with decision code "AC-DENY" and reason "NO_PARTNER_BINDING" is written

  Scenario: AC5 A partner without a second factor is refused
    Given partner identity "P-5101" signs in with a token whose amr claim holds "pwd" only
    When the token reaches the Workbench
    Then the system refuses the session with status 401 and message MSG-P4-005

  Scenario: AC6 An instruction of another firm is not returned
    Given "P-5101" is signed in for "LF-0012"
    When "P-5101" requests instruction "INS-2027-000431" placed with "LF-0019"
    Then the call returns status 404 with message MSG-P4-003 and no instruction data

  Scenario: AC7 Two partner roles or a bank role are refused
    Given partner identity "P-5104" is in groups "RWB-UAT-PT-LAWFIRM" and "RWB-UAT-PT-VALUER"
    When "P-5104" signs in
    Then the system refuses the session with message MSG-P4-006 and an incident is raised to the security administrator queue

  Scenario: AC8 A partner cannot reach bank screens
    Given "P-5101" is signed in with role "PT-LAWFIRM", whose Queue and allocation letter is "-"
    When "P-5101" calls GET /queues
    Then the system refuses the call with status 403 and message MSG-P4-002

  Scenario: AC9 A bank identity cannot use the external gateway
    Given test user "U-5105" holds RW-LITOFF with a bank identity
    When "U-5105" signs in through the external gateway
    Then the system refuses the session with message MSG-P4-001
    Then one entry with decision code "AC-DENY" and reason "BANK_IDENTITY_ON_PARTNER_ROUTE" is written
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A partner user holds a partner identity separate from bank identities, signs in only through the external gateway and only with multi-factor authentication | NFR-050; INT-24; Admin and access model, section 8.1; REQ-ACA-012 |
| BR2 | A partner user holds exactly one partner role and is bound to exactly one firm | Partner binding table (new); separation of duty |
| BR3 | A partner user sees only cases and instructions placed with their firm (scope PLACED) | Key sheet, roles.txt, scope "Placed cases" |
| BR4 | A partner role sees only the instruction types named for it | Parameters rwb.access.partner.instruction-types.*; LOV-INSTRUCTION |
| BR5 | Access ends when the firm's panel status is SUSPENDED or EXITED, or its contract end has passed | partner.panel_status (DF-PRT-005), partner.contract_end (DF-PRT-006); LOV-PANEL; R-UNI-26 |
| BR6 | The permission matrix, masking and the access log apply to partner users as to bank users | Admin and access model, section 8.1 |
| BR7 | No partner reaches the Workbench in PROD until the architecture change for external access is approved | DL03 |
| BR8 | Partner users are requested by the partner and agency manager, approved by the role owner and created by the access administrator | Admin and access model, section 8.1 |

### 9. State transitions

None. This story does not change a case status. A partner session moves from Resolved to Ended when the firm's status or the binding ends.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG Partner and agency manager | Requests partner users in the bank IAM; sets the firm's panel status in S9 |
| Role owner (bank IAM, level 2) | Approves each partner user request |
| Access administrator (bank IAM, level 3) | Creates the partner identity and adds it to the partner role group |
| RW-REFADM Reference data administrator | Loads the partner user binding (Reference data C) |
| RW-SECADM Security administrator | Approves the binding version; maintains the partner role groups; receives conflict incidents |
| PT-LAWFIRM, PT-VALUER, PT-AGENCY | Sign in and work their firm's instructions with the letters of their role (Partner portal RU) |
| Architecture team | Approves external access before PROD (DL03) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-213 | partner_user | identity_ref | Write, read |
| DF-REF-214 | partner_user | partner_id | Write, read |
| DF-REF-215 | partner_user | role_code | Write, read |
| DF-REF-216 | partner_user | valid_from | Write, read |
| DF-REF-217 | partner_user | valid_to | Write, read |
| DF-PRT-001 | partner | id | Read through the S9 published interface |
| DF-PRT-004 | partner | partner_type | Read through the S9 published interface |
| DF-PRT-005 | partner | panel_status | Read through the S9 published interface |
| DF-PRT-006 | partner | contract_end | Read through the S9 published interface |
| DF-PRT-010 | partner_instruction | partner_id | Read by the S9 repository applying the PLACED scope filter |
| DF-PRT-011 | partner_instruction | instruction_type | Read by the S9 repository applying the PLACED scope filter |
| DF-REF-035 | role | role_code | Read |
| DF-REF-037 | role | role_class | Read |
| DF-REF-039 | role | entra_group | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (sign-in and refusal access events) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/partner/instructions** (owned by S9; this story supplies the scope filter)

| Item | Value |
|---|---|
| Request | Query: status, page, size |
| Response | InstructionPage of PartnerInstruction |
| Errors | 401 no session or partner not active (MSG-P4-001, MSG-P4-008); 403 role without Partner portal R (MSG-P4-002); 503 (MSG-GEN-006) |
| Authorization | Partner portal, right R, scope PLACED |
| Idempotency | Not applicable, read only |

**POST /api/recovery/v1/admin/reference-loads** (API-P4-005) with table "partner_user"; Reference data C; Idempotency-Key header. Approve with POST /admin/reference-loads/{loadId}/approve by RW-SECADM (approver role for the table).

**GET /api/recovery/v1/me/session** (new in RWB-E1-022) returns partnerId and scope PLACED for a partner session.

**Published interfaces**

```java
// P4, package recovery.access.partner
ScopeFilter scopeFor(SessionContext session); // type PLACED, partnerId, instructionTypes
// S9, called by P4
PartnerStatus partnerStatus(UUID partnerId);  // panelStatus, contractEnd
```

### 13. Solution plan

- Package: folder `recovery/access/partner` in the recovery module; Java package `recovery.access.partner`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| AccessAndAdministrationController | Controller | Reference load for table partner_user (shared load endpoint) |
| PartnerAccessService | Service | Checks token issuer and route, one partner role, active binding and firm status; builds the PLACED scope |
| PartnerUserLoader | Service | Validates a binding file: known partner IDs through S9, partner role codes only, no identity bound twice in one period |
| PartnerSessionRevalidation | Service | Rechecks binding and firm status on each request after the refresh interval |
| PartnerUserRepository | Repository | Reads and writes partner_user rows |
| PartnerUser | Entity | Maps the new partner_user table |
| PartnerSignInPage | React component | Partner sign-in entry in the partner portal with MSG-P4-008 and MSG-P4-001 states |

- Database: creates table partner_user (id uuid, identity_ref varchar(64), partner_id uuid, role_code varchar(20), valid_from date, valid_to date, plus the standard columns) with Flyway migration V_E2_019__partner_user.sql; unique index on (identity_ref, valid_from); no foreign key to partner, which is S9's table.
- Configuration and reference data: partner role rows and groups (DL40); the binding version (RW-REFADM loads, RW-SECADM approves); instruction types per partner role (parameters, owner RW-AGENCYMG); rwb.access.membership-refresh-minutes=5 (assumed, DL38); external gateway route for the partner portal (INT-24, DL03).
- Build steps:
  1. Create the partner_user migration, entity and loader with validation.
  2. Extend SessionResolver to tell the partner route from the bank route and to refuse a bank identity on the partner route (AC9) and a partner identity on the bank route.
  3. Build PartnerAccessService with the binding and the S9 status call; tests for AC1, AC3, AC4, AC7.
  4. Add scope type PLACED with partner ID and instruction types to ScopeFilter; give S9 a repository test for AC1, AC2 and AC6.
  5. Build PartnerSessionRevalidation; test the session end in AC3.
  6. Confirm AC5 and AC8 through the RWB-E1-022 checks with partner tokens.
  7. Put the partner route behind the feature flag, off in PROD until DL03.
- Feature flag: `rwb.access.partner-signin`.
- Done when: the tests in section 16 pass in UAT through the external gateway test route, and the flag is off in PROD.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-008 | The firm is suspended, exited or past its contract end (new) | Your firm's access to the Recovery Workbench has ended. Contact your SCB partner manager. |
| MSG-P4-001 | No binding, or a bank identity on the partner route | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-005 | No second factor | Sign in again with your second factor. The Workbench needs multi-factor authentication. |
| MSG-P4-006 | Two partner roles, or a partner and a bank role | Your roles {role} and {otherRole} cannot be held together. Access is refused and the security administrator has been told. |
| MSG-P4-003 | An instruction of another firm | This case is not in your scope. |
| MSG-P4-002 | An endpoint outside the partner role's letters | You cannot {action} here. Your role does not include it. |

Thai text for each message follows DL10; proposed Thai for MSG-P4-008 is in the additions file.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| PRT-01 Partner home | Loading | Waits while the firm's open instructions load |
| PRT-01 Partner home | List | Sees only the firm's instructions of the role's types, with due dates |

A refused partner sees the partner sign-in page with MSG-P4-008 or MSG-P4-001 and no data.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-019-01 | AC1, BR1, BR3 | System | Synthetic firms LF-0012 and LF-0019 with 5 and 3 instructions |
| TC-E2-019-02 | AC2, BR4 | System | Valuer VL-0004 with APPRAISE and LIST instructions |
| TC-E2-019-03 | AC3, BR5 | System | Firm moved to EXITED during an open session |
| TC-E2-019-04 | AC4, BR2 | System | Partner identity with no binding |
| TC-E2-019-05 | AC5, BR1 | System | Partner token without a second factor |
| TC-E2-019-06 | AC6, BR3 | System | Instruction of another firm |
| TC-E2-019-07 | AC7, BR2 | System | Partner identity in two partner role groups |
| TC-E2-019-08 | AC8, BR6 | System | Partner calling GET /queues |
| TC-E2-019-09 | AC9, BR1 | System | Bank test user on the partner route |
| TC-E2-019-10 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E2-019-11 | Principle 5 | Resilience | The decision log write forced to fail during a partner sign-in |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: partner roles, instruction types, the binding and the refresh interval are data.
- No personal data in logs, tests or prompts; partner identities are referenced by their directory ID, never by e-mail or name.
- No read of another module's tables: partner status comes from the S9 interface and the instruction filter is applied by the S9 repository.
- No partner route in PROD while DL03 is open.
- A partner session never holds a bank role.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-012 | Partners only through the external gateway, with MFA, scoped to their own cases | Epic 2, 3.4 | FEAT-OCC-13 | 12 Manage partners | BR1 to BR8 | TC-E2-019-01 to TC-E2-019-11 |

### 19. Out of scope

- The architecture change that makes the partner portal reachable from outside the bank (DL03).
- Partner work screens PRT-02 to PRT-06 and the instruction endpoints (Epic 4 to Epic 6, S9 and S6 stories).
- Partner panel management, contracts and scorecards (SCR-34 in Epic 2 for identities; Epic 6 for the full panel).
- Customers, guarantors, heirs and bidders, who do not sign in to the Workbench.


---

## RWB-E2-021 Letter dispatch loop with proof of delivery from WIN

| Item | Value |
|---|---|
| Story key | RWB-E2-021 |
| Epic | E2, release 31 December 2026 |
| Module | P6 Communications |
| Feature | FEAT-OCC-01 Generate a letter from an approved template; FEAT-OCC-02 Dispatch a letter through WIN and capture proof of delivery; FEAT-OCC-05 Run the conduct check before every outbound contact; FEAT-OCC-06 Block an outbound contact when a contact stop is in force; FEAT-ILG-07 Bring dispatch outcomes into the ledger |
| Requirement IDs | REQ-OCC-003, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010 |
| BRD section | Business Requirements Epic 2, sections 3.6 and 4 |
| L3 process | 13 Manage documents and correspondence; 16 Manage risk, control and compliance; 06 to 10 Recovery case processes |
| Decision | D7.1 |
| Priority | Must |
| Depends on | RWB-E1-052, RWB-E1-055, RWB-E2-014 |
| Status | Ready for build |

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **every approved letter sent to WIN after the conduct check, with the dispatch and the proof of delivery returned to the case and the notice period started from delivery**, so that **the notice period is counted from proof of delivery and not from printing**.

### 2. Business rationale

A notice period counted from the print date can be challenged, and a letter sent to a customer under a contact stop is a conduct breach. This story adds the conduct check before every letter, handles refused, undeliverable and unproven letters, writes every outcome to the interaction ledger and gives the litigation officer an endpoint to request and read a notice. It serves REQ-OCC-003, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010, controls CTL-15 and CTL-16, and the FSD P6 measure "notices with proof of delivery, 100 percent".

### 3. Preconditions

- RWB-E1-052 and RWB-E1-055 are done: generation, the WIN file, the acknowledgment and the INT-15 load run.
- RWB-E2-014 is done: notices are approved on SCR-18 and reach state Approved.
- The dispatch-eligible notice states are set to Approved (`rwb.comms.dispatch.eligible-states` = APPROVED).
- Open deviations and their contact stop flags are readable through the S8 interface (RWB-E2-015).
- The proof window is loaded as reference data: 7 days from sending (R-LIT-08).
- The requester holds RW-LITOFF or RW-ENFORCE (Litigation C) for POST and any role with Litigation R for GET.

### 4. Flow

1. Litigation officer: requests a notice through POST /cases/{caseId}/notices; the system calls NoticeApi.generate (RWB-E1-052) and returns the notice in state Generated.
2. Approver: approves the notice on SCR-18 (RWB-E2-014); state Approved.
3. JOB-10, daily 16:00: for each Approved notice runs the conduct check: legal hold on the case, open deviation with contact stop, current template still Approved, statutory status of the notice type.
4. System: a notice that fails the check is held, the reason is written to the decision log and to the ledger with conduct check Blocked, and the case goes to the deviation owner (R-LIT-05) or the hold owner; it is not written to the file.
5. System: a notice that passes is written to the INT-14 file with conduct check Passed; the WIN acknowledgment sets Sent with the barcode (RWB-E1-055) and the ledger entry carries the barcode.
6. JOB-09: loads the INT-15 file; a Delivered record sets Delivered and publishes NoticeDelivered; P3 starts the notice period from the delivery date (R-LIT-07).
7. System: a Refused or Undeliverable record sets Unserved, writes the decision log entry under R-LIT-09, writes the ledger entry and raises DELIVERY_FAILED to P3, which transfers the case to the owner's queue with reason NOTICE_UNSERVED.
8. JOB-10, at the start of each run: a Sent notice with no proof 7 days after its sent date becomes Unserved under R-LIT-08; the notice period does not start.
9. Litigation officer: reads the notice, its dispatch and its proof through GET /notices/{noticeId} and on SCR-18.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | WIN returns Refused or Undeliverable | Notice Unserved; case to the owner's queue with the reason | MSG-P6-008 | AC3 |
| X2 | An open X1 or X2 deviation has the contact stop on | Notice held; case to the deviation owner | MSG-P6-001 | AC4 |
| X3 | Consent for the postal channel is withdrawn | A statutory notice is still sent | None | AC5 |
| X4 | No proof 7 days after sending | Notice Unserved; notice period not started | MSG-P6-008 | AC6 |
| X5 | A legal hold is on the case | Notice held; nothing sent | MSG-P3-004 | AC7 |
| X6 | The template of an approved notice is withdrawn before dispatch | Notice held | MSG-P6-003 | AC8 |
| X7 | The decision log write fails for a held or unserved notice | Notice unchanged; retried on the next run; incident raised | MSG-P7-003 | AC9 |
| X8 | POST repeated with the same Idempotency-Key | The first notice is returned | None | AC10 |
| X9 | GET for a notice outside the caller's scope | Refused | MSG-P4-003 | AC11 |
| X10 | POST with no notice type | Refused | MSG-GEN-001 | AC12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the v1 dispatch and generation; approval (RWB-E2-014) is a prior story |
| Negotiable | The proof window, statutory notice types and eligible states are data |
| Valuable | Every letter carries a conduct result and the notice period starts only from proof |
| Estimable | Two endpoints, one check service, two result handlers, one daily window check |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs with synthetic notices and WIN files |

### 7. Acceptance criteria

```gherkin
Feature: Letter dispatch loop with proof of delivery from WIN

  Background:
    Given the dispatch-eligible notice states are "APPROVED"
    Given the proof window is 7 days
    Given notice "N-0101" for case "RC-2026-000321" is "Approved" with notice type "DEMAND" and template "DEMAND-SSME" "TH" version 1 Approved
    Given case "RC-2026-000321" has no legal hold and no open deviation

  Scenario: AC1 Dispatch
    Given JOB-10 runs at 16:00 on 2026-12-14
    When the conduct check passes and WIN acknowledges contract "CT-88001" with barcode "RR223344556TH" and sent date 15122026
    Then notice "N-0101" is "Sent" with barcode "RR223344556TH" and sent date 2026-12-15
    Then the ledger entry for the letter has conduct check "PASSED" and summary naming barcode "RR223344556TH"
    Then GET /notices/N-0101 returns sentDate 2026-12-15 and barcode "RR223344556TH"

  Scenario: AC2 Proof back
    Given notice "N-0101" is "Sent" on 2026-12-15
    When the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "DELIVERED" and call-back date 18122026
    Then notice "N-0101" is "Delivered" with callback date 2026-12-18
    Then the ledger has an entry "Delivered" for case "RC-2026-000321" on 2026-12-18
    Then case "RC-2026-000321" has a running "NOTICE_PERIOD" timer started on 2026-12-18

  Scenario: AC3 Undelivered
    Given notice "N-0101" is "Sent" on 2026-12-15
    When the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "UNDELIVERABLE"
    Then notice "N-0101" is "Unserved" with delivery status "UNDELIVERABLE"
    Then one decision log entry exists with decision code "D7.1" and rule "R-LIT-09"
    Then the system transfers case "RC-2026-000321" to its owner's queue with reason "NOTICE_UNSERVED"
    Then the owner sees MSG-P6-008 naming "DEMAND" and "UNDELIVERABLE"
    Then the system starts no notice period timer

  Scenario: AC4 Contact stop blocks the letter
    Given case "RC-2026-000321" has an open deviation "X1" with contact stop on
    When JOB-10 runs on 2026-12-14
    Then the system does not writ notice "N-0101" to the WIN file
    Then notice "N-0101" is "Held" with hold reason "CONTACT_STOP_X1"
    Then the ledger entry has conduct check "BLOCKED"
    Then one decision log entry exists with rule "R-LIT-05"
    Then the system routes the case to the complaint officer with MSG-P6-001 naming "X1 Dispute or complaint"

  Scenario: AC5 Consent withdrawn does not stop a statutory notice
    Given the borrower's postal address contact point has consent status "WITHDRAWN"
    Given notice type "DEMAND" is a statutory notice
    When JOB-10 runs on 2026-12-14
    Then the system writes notice "N-0101" to the WIN file
    Then the ledger entry has conduct check "PASSED" and summary "Statutory notice, consent withdrawn"

  Scenario: AC6 Proof window expires
    Given notice "N-0102" for case "RC-2026-000654" is "Sent" with sent date 2026-12-15 and no proof returned
    Given notice "N-0103" for case "RC-2026-000655" is "Sent" with sent date 2026-12-16 and no proof returned
    When JOB-10 runs on 2026-12-22
    Then notice "N-0102" is "Unserved" with delivery status "PENDING"
    Then one decision log entry exists for "N-0102" with rule "R-LIT-08"
    Then the system starts no notice period timer for case "RC-2026-000654"
    Then notice "N-0103" stays "Sent"

  Scenario: AC7 Legal hold stops dispatch
    Given case "RC-2026-000321" has legal hold true
    When JOB-10 runs on 2026-12-14
    Then notice "N-0101" is "Held" with hold reason "LEGAL_HOLD" and is not in the WIN file
    Then the case record shows MSG-P3-004

  Scenario: AC8 Template withdrawn after approval
    Given template "DEMAND-SSME" "TH" version 1 was withdrawn on 2026-12-13
    When JOB-10 runs on 2026-12-14
    Then notice "N-0101" is "Held" with hold reason "TEMPLATE_WITHDRAWN" and is not in the WIN file
    Then the system raises a task to the litigation officer team with MSG-P6-003

  Scenario: AC9 Decision log write fails on a held notice
    Given case "RC-2026-000321" has an open deviation "X2" with contact stop on
    Given the decision log store is unavailable
    When JOB-10 runs on 2026-12-14
    Then notice "N-0101" stays "Approved" and is not in the WIN file
    Then the job record shows MSG-P7-003 for "N-0101"
    Then the system raises an incident under rule R-UNI-39

  Scenario: AC10 Repeated request
    Given "LIT-0101" sent POST /cases/RC-2026-000321/notices with notice type "RECALL" and Idempotency-Key "a1b2c3d4-0001"
    When the same request is sent again with Idempotency-Key "a1b2c3d4-0001"
    Then the response is the first notice with status 201
    Then case "RC-2026-000321" has one RECALL notice

  Scenario: AC11 Notice outside the caller's scope
    Given notice "N-0200" belongs to a case outside the scope of "LIT-0101"
    When "LIT-0101" sends GET /notices/N-0200
    Then the response is status 404 with MSG-P4-003

  Scenario: AC12 Notice type missing
    Given "LIT-0101" holds RW-LITOFF and case "RC-2026-000321" is in scope
    When "LIT-0101" sends POST /cases/RC-2026-000321/notices with no notice type
    Then the response is status 422 with MSG-GEN-001 naming "notice type"
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every letter is checked before it is written to the WIN file, and the result is on the ledger entry | REQ-OCC-005; FEAT-OCC-05 |
| BR2 | A contact stop from X1 or X2 holds the notice and routes the case to the deviation owner | R-LIT-05; CTL-16 |
| BR3 | A legal hold stops every outbound action | R-UNI-20 |
| BR4 | Withdrawn consent removes the channel from the contact plan, and statutory notices continue | R-UNI-10; REQ-OCC-006; CTL-16 |
| BR5 | The notice period starts from the delivery date on the proof | R-LIT-07; CTL-15 |
| BR6 | A refused, returned or undeliverable letter records the result and queues an alternate service method | R-LIT-09 |
| BR7 | No proof inside the proof window marks the notice unserved, and the notice period does not start | R-LIT-08 |
| BR8 | A withdrawn template holds the notice | R-LIT-04 |
| BR9 | A held or unserved result that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |
| BR10 | Which notice types are statutory is a list held as reference data | Principle 1; LOV-NOTICE |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| In progress | Offer or notice sent to the customer | WIN acknowledges the notice | Waiting customer |
| In progress | Deviation flagged or legal hold placed | Contact stop or legal hold found at the check | On hold (set by P3 under R-DEV-01 or R-UNI-20; this story holds the notice only) |

The case status moves are made by P3 on the events this story raises. This story changes the notice state: Approved to Sent, Approved to Held, Sent to Delivered, Sent to Unserved (DELIVERY_FAILED, PROOF_WINDOW_EXPIRED).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Requests a notice (Litigation C); reads it (Litigation R) |
| RW-ENFORCE, enforcement owner | Requests and reads a notice (Litigation CRU) |
| RW-CASEOWN, RW-LEGAL, RW-HEADLIT and other roles with Litigation R | Read the notice, its dispatch and proof |
| RW-CONDUCT, Conduct and QA officer | Reads blocked contacts on the ledger (Case record R) |
| SY-DATALOAD, data load from COLLINS | Runs JOB-10 and the INT-15 step |
| SY-CASEWF, case workflow module | Applies DELIVERY_FAILED and the transfer; starts the timer |
| SY-DECLOG, decision log writer | Writes the D7.1 entries |

No approval level from the delegation of authority applies in this story; notice approval is RWB-E2-014.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice | id | Read |
| DF-LEG-016 | notice | case_id | Read |
| DF-LEG-018 | notice | notice_type | Read |
| DF-LEG-019 | notice | sent_date | Read |
| DF-LEG-020 | notice | barcode | Read |
| DF-LEG-021 | notice | callback_date | Write |
| DF-LEG-022 | notice | delivery_status | Write |
| Standard column | notice | state | Write |
| DF-LEG-032 | notice | hold_reason | Write |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-CAS-038 | deviation | deviation_code | Read |
| DF-CAS-043 | deviation | contact_stop | Read |
| DF-CAS-044 | deviation | cleared_at | Read |
| DF-PTY-015 | contact_point | channel | Read |
| DF-PTY-018 | contact_point | consent_status | Read |
| DF-INT-005 | interaction | channel | Write, through the ledger writer |
| DF-INT-011 | interaction | summary | Write, through the ledger writer |
| DF-INT-012 | interaction | conduct_check | Write, through the ledger writer |
| DF-WRK-030 | timer | timer_type | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /api/recovery/v1/cases/{caseId}/notices** (api.yaml, x-module P6)

| Item | Value |
|---|---|
| Request | NoticeRequest: noticeType (required), partyId (defaults to the borrower), language (defaults to TH) |
| Response | 201 Notice: id, caseId, documentId, noticeType, sentDate, barcode, callbackDate, deliveryStatus, sentType |
| Errors | 401 no session; 403 role lacks Litigation C (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 409 template not approved (MSG-P6-005) or a notice of this type already in progress (MSG-P3-005); 422 field fails (MSG-GEN-001); 503 decision not recorded (MSG-P7-003) |
| Authorization | Litigation, right C, scope applied |
| Idempotency | Idempotency-Key header, kept 24 hours |

**GET /api/recovery/v1/notices/{noticeId}** (api.yaml, x-module P6)

| Item | Value |
|---|---|
| Response | 200 Notice |
| Errors | 401; 403 (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 |
| Authorization | Litigation, right R, scope applied |
| Idempotency | Not applicable |

**Jobs.** JOB-10 WIN outbound notices (daily 16:00) gets two steps: the proof window step first, then the conduct check before each file record. JOB-09 File loads adds the Refused and Undeliverable results to the INT-15 step. Idempotency for each: notice ID and business date; a rerun from SCR-44 skips notices already Unserved, Held or in a file of that date.

**Events published.** NoticeDispatched (EV-14), NoticeDelivered (EV-15) with status DELIVERED, REFUSED or UNDELIVERABLE.

**Published interfaces called**

```java
List<ContactStopView> DeviationApi.activeContactStops(UUID caseId);            // S8
CaseSummary CaseWorkflowApi.getCaseSummary(UUID caseId);                        // P3, carries legalHold
void CaseWorkflowApi.applyEvent(UUID caseId, String eventCode, Map<String,String> facts); // P3, DELIVERY_FAILED, PROOF_WINDOW_EXPIRED, CONTACT_STOP_APPLIED
UUID InteractionLedgerApi.record(InteractionRecord record);                     // ledger writer
DecisionLogRef DecisionLogApi.write(DecisionLogRequest request) throws DecisionLogWriteException; // P7
```

### 13. Solution plan

- Package: folders `recovery/comms/dispatch` and `recovery/comms/notices`, Java packages `recovery.comms.dispatch` and `recovery.comms.notices`.

| Component | Type | Responsibility |
|---|---|---|
| NoticeController | Controller | POST /cases/{caseId}/notices and GET /notices/{noticeId} |
| ConductCheckService | Service | Legal hold, contact stop, template state and statutory rule for one outbound contact; returns Passed or Blocked with the reason and rule ID |
| WinNoticeFileJob | Job | From RWB-E1-055; calls ConductCheckService before writing each record |
| DeliveryResultHandler | Service | Applies Delivered, Refused and Undeliverable from INT-15; writes the decision log, ledger and P3 event |
| ProofWindowStep | Job | First step of JOB-10: Sent notices past the proof window become Unserved under R-LIT-08 |
| StatutoryNoticeTypes | Rule table | Reads the statutory notice type list from reference data |

- Database: table notice (columns from RWB-E1-052 and RWB-E1-055). Index ix_notice_state_sent supports the window check. No new table.
- Configuration and reference data: `rwb.comms.dispatch.eligible-states` = APPROVED; proof window 7 days as a timer row (R-LIT-08, business lead, DL22); statutory notice types DEMAND, RECALL, STATUTORY_SALE_NOTICE, GUARANTOR_NOTICE, assumed, owner Legal counsel; INT-15 result codes mapped to LOV-DELIVERY in the code map (data steward).
- Build steps:
  1. Add the INT-15 result column to the file reader and the code map to LOV-DELIVERY; test the mapping.
  2. Build ConductCheckService with the four checks in order: legal hold, contact stop, template, consent with the statutory rule; unit test each branch.
  3. Wire ConductCheckService into WinNoticeFileJob with the decision log and ledger writes; test AC1, AC4, AC5, AC7, AC8, AC9.
  4. Build DeliveryResultHandler for the three results; test AC2 and AC3.
  5. Build ProofWindowStep in JOB-10; test AC6 with the 6-day and 7-day boundary.
  6. Build NoticeController on NoticeApi with Idempotency-Key and scope; test AC10, AC11, AC12.
- Feature flag: `rwb.comms.win-dispatch-loop`.
- Done when: the tests in section 16 pass, and REC-05 shows no break for the synthetic month of notices.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-008 | A notice is refused, undeliverable or has no proof in the window | {notice} for case {case} was not served: {reason}. The case is in your queue to choose another service method. |
| MSG-P6-001 | A contact stop blocks the letter | Contact with this customer is stopped for {reason}. |
| MSG-P3-004 | A legal hold or deviation blocks the letter | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P6-003 | The template was withdrawn before dispatch | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-003 | The notice is outside the caller's scope | This case is not in your scope. |
| MSG-GEN-001 | Notice type missing | Enter {field}. |
| MSG-P6-004 | WIN acknowledged the notice | {notice} was sent for registered mail on {date}. |

### 15. Screens and states

SCR-18 Notice approval (built in RWB-E2-014) shows the states this story sets:

| State | What the user sees and does |
|---|---|
| Sent | Sent date and barcode; the litigation officer waits for proof |
| Delivered | Callback date and the notice period end date from the timer |
| Unserved | The result and MSG-P6-008; the litigation officer chooses an alternate service method on the case (R-LIT-10, Epic 5) |

SCR-04 Case timeline shows each ledger entry with its conduct check result.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-021-01 | AC1, BR1 | System | N-0101 Approved; acknowledgment RR223344556TH |
| TC-E2-021-02 | AC2, BR5 | System | INT-15 DELIVERED, call-back 18122026 |
| TC-E2-021-03 | AC3, BR6 | System | INT-15 UNDELIVERABLE |
| TC-E2-021-04 | AC4, BR2 | System | Open X1 with contact stop |
| TC-E2-021-05 | AC5, BR4, BR10 | System | Postal consent WITHDRAWN, DEMAND notice |
| TC-E2-021-06 | AC6, BR7 | System | N-0102 sent 2026-12-15 and N-0103 sent 2026-12-16; JOB-10 on 2026-12-22 |
| TC-E2-021-07 | AC7, BR3 | System | Legal hold true |
| TC-E2-021-08 | AC8, BR8 | System | DEMAND-SSME TH v1 withdrawn 2026-12-13 |
| TC-E2-021-09 | AC9, BR9 | System | Open X2 with stop; decision log stubbed unavailable |
| TC-E2-021-10 | AC10 | System | POST repeated with one Idempotency-Key |
| TC-E2-021-11 | AC11 | System | N-0200 outside scope |
| TC-E2-021-12 | AC12 | System | POST with no notice type |
| TC-E2-021-13 | Access | Access | RW-CASEOWN sends POST /cases/{caseId}/notices; refused with MSG-P4-002 |
| TC-E2-021-14 | Principle 5 | Resilience | Decision log write forced to fail on 10 unserved results; no notice changes |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: proof window, statutory notice types, eligible states and result code mappings are data.
- No personal data in logs, tests or prompts. Ledger summaries carry codes and barcodes, never names or addresses.
- No read of another module's tables. Deviations, case hold, contact points, timers and the transfer go through the owning interfaces.
- The conduct check runs inside the same transaction that selects the notice for the file, so a stop raised after the check reaches the next run.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-02 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-LIT-09 | TC-E2-021-01, TC-E2-021-02, TC-E2-021-03, TC-E2-021-06, TC-E2-021-10, TC-E2-021-11, TC-E2-021-12 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05, FEAT-OCC-06 | 16 Manage risk, control and compliance | R-LIT-05, R-UNI-20, R-LIT-04, R-UNI-39 | TC-E2-021-04, TC-E2-021-07, TC-E2-021-08, TC-E2-021-09, TC-E2-021-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel; statutory notices continue | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05 | 16 Manage risk, control and compliance | R-UNI-10 | TC-E2-021-05 |
| REQ-ILG-010 | Dispatch results, including proof of delivery, written to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-LIT-07, R-LIT-09 | TC-E2-021-01, TC-E2-021-02, TC-E2-021-03, TC-E2-021-13 |

### 19. Out of scope

- Alternate service methods and substituted service (R-LIT-10, R-LIT-11, Epic 5).
- SMS and LINE dispatch (RWB-E2-022).
- The breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7).
- Notice approval (RWB-E2-014).


---

## RWB-E2-022 SMS and LINE dispatch through NSS and LINE OA

| Item | Value |
|---|---|
| Story key | RWB-E2-022 |
| Epic | E2, release 31 December 2026 |
| Module | P6 Communications |
| Feature | FEAT-OCC-03 Dispatch SMS through NSS; FEAT-OCC-04 Dispatch a LINE message through LINE OA; FEAT-ILG-07 Bring dispatch outcomes into the ledger |
| Requirement IDs | REQ-OCC-004, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010 |
| BRD section | Business Requirements Epic 2, sections 3.6 and 4 |
| L3 process | 13 Manage documents and correspondence; 06 to 10 Recovery case processes |
| Decision | X6 |
| Priority | Must |
| Depends on | RWB-E1-052, RWB-E1-066 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **messages sent from approved templates through NSS and the LINE official account, with the contact rules applied before sending and the delivery status on the case**, so that **the customer is reached on the channel they use and every contact is recorded**.

### 2. Business rationale

Case owners send SMS and LINE messages outside the Workbench today, so a message can reach a customer under a contact stop or without consent, and the case has no record of it. This story sends from Legal-approved templates through the ACE notification path (INT-17, INT-18), refuses a message when a contact stop, a legal hold or missing consent applies, and writes every attempt and its delivery result to the interaction ledger. It serves REQ-OCC-004, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010, and controls CTL-16 and CTL-17.

### 3. Preconditions

- RWB-E1-052 is done; RWB-E1-046 provides Approved SMS and LINE templates (channel SMS or LINE) in TH and EN.
- RWB-E1-066 is done: the interaction ledger writer accepts entries.
- The ACE notification path to NSS and LINE OA is available in the environment (DL30).
- Contact points with consent status are loaded through COLLINS (INT-04).
- The list of deviation codes that block SMS and LINE is loaded as reference data.
- The sender holds RW-CASEOWN or another role with Case record C, and the case is in the sender's scope.

### 4. Flow

1. Case owner: on SCR-03 Case record chooses Send message, the channel (SMS or LINE), the template and the party.
2. System: checks the role (Case record C) and the scope; reads the current template for the channel and language through TemplateCatalog.
3. System: runs the conduct check: legal hold on the case, open deviation with contact stop, open deviation in the blocking list for the channel, and consent GIVEN on a verified contact point of that channel.
4. System: if the check fails, refuses, writes the decision log entry and a ledger entry with conduct check Blocked; stops.
5. System: merges the template, writes the ledger entry with conduct check Passed and delivery status Sent, and writes the send request to the outbox in the same transaction.
6. JOB-11 Outbox sender: sends the request to the ACE notification path; NSS or LINE OA returns an accepted reference, which the system stores on the ledger entry.
7. ACE notification path: returns the delivery result (NSS result code; LINE delivered and read); the system updates the ledger entry to Delivered, Read or Failed.
8. System: on Failed, adds one to the failed count of the contact point through the P1 interface.
9. Case owner: sees the message and its status on SCR-04 Case timeline.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case has an open X6 lost contact | Refused and logged | MSG-P6-001 | AC3 |
| X2 | An open deviation has the contact stop on | Refused and logged | MSG-P6-001 | AC4 |
| X3 | No consent GIVEN on the channel | Refused and logged | MSG-P6-002 | AC5 |
| X4 | The template is withdrawn | Refused | MSG-P6-003 | AC6 |
| X5 | NSS or LINE OA is unavailable | Queued and retried; after the retry limit to the exception queue | MSG-GEN-006 | AC7 |
| X6 | NSS returns a failure code | Ledger entry Failed; contact point failed count raised | None | AC8 |
| X7 | The same request with the same Idempotency-Key | One message only | None | AC9 |
| X8 | The decision log write fails on a refusal | Nothing sent; refusal not recorded; incident | MSG-P7-003 | AC10 |
| X9 | A legal hold is on the case | Refused and logged | MSG-P3-004 | AC11 |
| X10 | No channel given | Refused | MSG-GEN-001 | AC12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the template catalog and the ledger writer; the notification path is ACE's |
| Negotiable | Templates, blocking deviation codes and the retry limit are data |
| Valuable | Every SMS and LINE message is checked and recorded on the case |
| Estimable | One endpoint, one check service shared with letters, one result listener |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs with the notification path stubbed |

### 7. Acceptance criteria

```gherkin
Feature: SMS and LINE dispatch through NSS and LINE OA

  Background:
    Given template "SMS-REMIND" "TH" version 1 with channel "SMS" is Approved and current
    Given template "LINE-REMIND" "TH" version 1 with channel "LINE" is Approved and current
    Given case "RC-2026-000777" is owned by "CO-0201" with borrower party "P-0077"
    Given case "RC-2026-000777" has no legal hold and no open deviation

  Scenario: AC1 SMS sent
    Given party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN"
    When "CO-0201" sends POST /cases/RC-2026-000777/messages with channel "SMS", template "SMS-REMIND", language "TH" and party "P-0077"
    When NSS accepts the message with reference "NSS-7781" and returns result "DELIVERED"
    Then the response is status 202 with an interaction of channel "SMS", direction "OUTBOUND" and conduct check "PASSED"
    Then the interaction has delivery status "DELIVERED" and reference "NSS-7781"
    Then NSS received one message

  Scenario: AC2 LINE
    Given party "P-0077" has a verified "LINE" contact point with consent "GIVEN"
    When "CO-0201" sends a message with channel "LINE" and template "LINE-REMIND"
    When LINE OA reports the message delivered and then read
    Then the interaction has channel "LINE", conduct check "PASSED" and delivery status "READ"
    Then LINE OA received one message

  Scenario: AC3 Contact stop on lost contact
    Given case "RC-2026-000777" has an open deviation "X6" lost contact
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 409 with MSG-P6-001 naming "X6 Lost contact"
    Then the system sends nothing to NSS
    Then the system writes an interaction with conduct check "BLOCKED"
    Then one decision log entry exists with decision code "X6" and final call "contact refused"

  Scenario: AC4 Contact stop from a dispute
    Given case "RC-2026-000777" has an open deviation "X1" with contact stop on
    When "CO-0201" sends a message with channel "LINE"
    Then the response is status 409 with MSG-P6-001 naming "X1 Dispute or complaint"
    Then the system sends nothing to LINE OA
    Then the system writes an interaction with conduct check "BLOCKED"

  Scenario: AC5 No consent on the channel
    Given party "P-0077" has a "MOBILE" contact point with consent "WITHDRAWN"
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 409 with MSG-P6-002 naming "SMS"
    Then the system sends nothing to NSS
    Then the system writes an interaction with conduct check "BLOCKED"

  Scenario: AC6 Template withdrawn
    Given template "SMS-REMIND" "TH" version 1 is Withdrawn and no later version is Approved
    When "CO-0201" sends a message with channel "SMS" and template "SMS-REMIND"
    Then the response is status 409 with MSG-P6-003 naming "SMS-REMIND"

  Scenario: AC7 NSS unavailable
    Given the ACE notification path returns "unavailable" for NSS
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 202 with MSG-GEN-006 naming "NSS"
    Then JOB-11 retries the send on its schedule
    Then after the retry limit of 5 the send is in the exception queue under rule R-UNI-34 and the interaction has delivery status "FAILED"

  Scenario: AC8 NSS failure result
    Given party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN" and failed count 0
    When NSS returns result "FAILED" for the message
    Then the interaction has delivery status "FAILED"
    Then the contact point has failed count 1

  Scenario: AC9 Repeated request
    Given "CO-0201" sent a message with Idempotency-Key "c0ffee00-0001"
    When the same request is sent again with Idempotency-Key "c0ffee00-0001"
    Then the response is the first response
    Then NSS received one message

  Scenario: AC10 Decision log write fails on a refusal
    Given case "RC-2026-000777" has an open deviation "X6"
    Given the decision log store is unavailable
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 503 with MSG-P7-003
    Then the system sends nothing to NSS
    Then the system raises an incident under rule R-UNI-39

  Scenario: AC11 Legal hold
    Given case "RC-2026-000777" has legal hold true
    When "CO-0201" sends a message with channel "LINE"
    Then the response is status 409 with MSG-P3-004
    Then the system sends nothing to LINE OA

  Scenario: AC12 Channel missing
    Given template "SMS-REMIND" "TH" is current and party "P-0077" has a verified "MOBILE" contact point
    When "CO-0201" sends POST /cases/RC-2026-000777/messages with no channel
    Then the response is status 422 with MSG-GEN-001 naming "channel"
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every outbound message carries a conduct check result on its ledger entry | REQ-OCC-005; FEAT-OCC-05 |
| BR2 | No message is sent while a contact stop is in force | CTL-16; R-UNI-04, R-UNI-05 |
| BR3 | Deviation codes that block SMS and LINE are a reference list; X6 blocks both until a contact point is verified | R-DEV-16; R-UNI-12; Principle 1 |
| BR4 | Messages go only to a verified contact point with consent GIVEN for that channel | CTL-17; R-UNI-10 |
| BR5 | A legal hold stops every outbound action | R-UNI-20 |
| BR6 | A system that is unavailable queues the send and retries; after the limit it goes to the exception queue | R-UNI-33, R-UNI-34, R-UNI-36 |
| BR7 | A refusal that cannot be written to the decision log is not completed | Principle 5; R-UNI-39 |
| BR8 | Only the current Approved template for the channel is used | R-LIT-03; CTL-14 |
| BR9 | The same request twice sends one message | R-UNI-40 |

### 9. State transitions

None. This story does not change a case status. It sets the delivery status on the ledger entry: Sent, then Delivered, Read or Failed; and the outbox record: queued, sent, retried, exception.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Sends a message on a case in scope (Case record C) |
| RW-TEAMMGR, team manager | Reads messages on team cases (Case record R) |
| RW-CONDUCT, Conduct and QA officer | Reads blocked contacts on the ledger (Case record R) |
| RW-COMPLAIN, complaint officer | Reads the contact history of a disputed case (Case record R) |
| SY-DECLOG, decision log writer | Writes the refusal entry |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-CAS-038 | deviation | deviation_code | Read |
| DF-CAS-043 | deviation | contact_stop | Read |
| DF-CAS-044 | deviation | cleared_at | Read |
| DF-PTY-014 | contact_point | party_id | Read |
| DF-PTY-015 | contact_point | channel | Read |
| DF-PTY-016 | contact_point | value_token | Read |
| DF-PTY-018 | contact_point | consent_status | Read |
| DF-PTY-019 | contact_point | verified_at | Read |
| DF-PTY-020 | contact_point | failed_count | Write, through the P1 interface |
| DF-REF-046 | template | template_code | Read |
| DF-REF-047 | template | template_version | Read |
| DF-REF-066 | template | channel | Read |
| DF-INT-002 | interaction | case_id | Write, through the ledger writer |
| DF-INT-003 | interaction | party_id | Write, through the ledger writer |
| DF-INT-004 | interaction | occurred_at | Write, through the ledger writer |
| DF-INT-005 | interaction | channel | Write, through the ledger writer |
| DF-INT-006 | interaction | direction | Write, through the ledger writer |
| DF-INT-011 | interaction | summary | Write, through the ledger writer |
| DF-INT-012 | interaction | conduct_check | Write, through the ledger writer |
| DF-INT-013 | interaction | source_system | Write, through the ledger writer |
| DF-INT-028 | interaction | delivery_status | Write, through the ledger writer |
| DF-INT-029 | interaction | external_ref | Write, through the ledger writer |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /cases/{caseId}/messages** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | MessageRequest: channel (SMS or LINE, required), templateCode (required), language (TH or EN, default TH), partyId (default the borrower) |
| Response | 202 Interaction: id, caseId, partyId, occurredAt, channel, direction, conductCheck, summary, sourceSystem, deliveryStatus, externalRef |
| Errors | 401 no session; 403 role lacks Case record C (MSG-P4-002); 404 case out of scope (MSG-P4-003); 409 contact stop (MSG-P6-001), no consent (MSG-P6-002), template withdrawn (MSG-P6-003), legal hold (MSG-P3-004); 422 field missing (MSG-GEN-001); 503 decision not recorded (MSG-P7-003) |
| Authorization | Case record, right C, scope applied |
| Idempotency | Idempotency-Key header, kept 24 hours |

The current GET /api/recovery/v1/cases/{caseId}/interactions (P3) returns the entries with their status.

**Job JOB-11 Outbox sender**: every minute; sends queued messages to the ACE notification path; idempotency key the interaction ID; retry limit 5, assumed; DL11; after the limit the send goes to the exception queue (R-UNI-34).

**Published interfaces**

```java
// ACE common module notification path (INT-17, INT-18)
NotificationAck NotificationPort.send(NotificationRequest request);   // channel, contactPointToken, templateRef, language, caseRef
// P6, called by the ACE notification path with each result
void MessageResultListener.onResult(String externalRef, String channel, String result, Instant at);
// Owned elsewhere
List<ContactStopView> DeviationApi.activeContactStops(UUID caseId);                    // S8
List<ContactPointView> PartyApi.contactPoints(UUID partyId, String channel);            // P1
void PartyApi.recordFailedContact(UUID contactPointId, Instant at);                    // P1
UUID InteractionLedgerApi.record(InteractionRecord record);                            // ledger writer
void InteractionLedgerApi.updateDelivery(UUID interactionId, String status, String externalRef); // ledger writer
```

### 13. Solution plan

- Package: folder `recovery/comms/messaging`, Java package `recovery.comms.messaging`; front end folder `recovery/comms/messaging`.

| Component | Type | Responsibility |
|---|---|---|
| MessageController | Controller | POST /cases/{caseId}/messages |
| MessageService | Service | Template, conduct check, merge, ledger entry and outbox write in one transaction |
| ConductCheckService | Service | From RWB-E2-021, extended with the channel blocking list and the consent check |
| MessageOutboxSender | Job | Handler of JOB-11 for message sends |
| MessageResultListener | Published interface | Maps NSS and LINE OA results to delivery status |
| SendMessageDialog | React component | Send message on SCR-03: channel, template and party, with the refusal message shown |

- Database: no new table. The outbox table of the ACE pattern holds the send requests. The ledger gets delivery_status and external_ref through the ledger writer (additions).
- Configuration and reference data: blocking deviation codes per channel, SMS and LINE: X1, X2, X3 when contact stop is on, and X6, assumed, owner Conduct and QA officer; NSS result code map to SENT, DELIVERED, FAILED and LINE OA status map to DELIVERED, READ (data steward); retry limit 5 (DL11).
- Build steps:
  1. Add MessageRequest and the Interaction fields to the OpenAPI file; generate the controller interface.
  2. Extend ConductCheckService with the blocking list and consent; unit test AC3, AC4, AC5, AC11.
  3. Build MessageService with the template check, the decision log write on refusal and the outbox write; test AC6, AC10, AC12.
  4. Build MessageOutboxSender with the retry and exception path; test AC7 with the notification path stubbed.
  5. Build MessageResultListener and the failed count call; test AC1, AC2, AC8.
  6. Add the Idempotency-Key store; test AC9.
  7. Build SendMessageDialog; browser test of a send and a refusal.
- Feature flag: `rwb.comms.sms-line`.
- Done when: the tests in section 16 pass, and the NSS and LINE OA stubs are replaced by the ACE notification path in SIT with one SMS and one LINE message to test numbers.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-001 | A contact stop applies | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | No consent for the channel | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-GEN-006 | NSS or LINE OA is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Channel or template missing | Enter {field}. |

### 15. Screens and states

SCR-03 Case record (state editable) gets the Send message action for roles with Case record C. SCR-04 Case timeline (states Loading; filtered) shows each message with channel, template, conduct check and delivery status. SCR-09 Exception queue lists sends that failed after the retry limit.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-022-01 | AC1, BR1, BR4, BR8 | System | P-0077 MOBILE consent GIVEN; NSS stub reference NSS-7781 |
| TC-E2-022-02 | AC2, BR4 | System | P-0077 LINE consent GIVEN; LINE OA stub delivered and read |
| TC-E2-022-03 | AC3, BR3 | System | Open X6 |
| TC-E2-022-04 | AC4, BR2 | System | Open X1 with contact stop |
| TC-E2-022-05 | AC5, BR4 | System | MOBILE consent WITHDRAWN |
| TC-E2-022-06 | AC6, BR8 | System | SMS-REMIND TH v1 Withdrawn |
| TC-E2-022-07 | AC7, BR6 | System | Notification path stub unavailable for 6 attempts |
| TC-E2-022-08 | AC8 | System | NSS result FAILED, failed count 0 |
| TC-E2-022-09 | AC9, BR9 | System | Same Idempotency-Key twice |
| TC-E2-022-10 | AC10, BR7 | System | Open X6; decision log stubbed unavailable |
| TC-E2-022-11 | AC11, BR5 | System | Legal hold true |
| TC-E2-022-12 | AC12 | System | No channel |
| TC-E2-022-13 | Access | Access | RW-PHONECOL sends POST /cases/{caseId}/messages; refused with MSG-P4-002 |
| TC-E2-022-14 | Principle 5 | Resilience | Decision log write forced to fail on 10 refusals; none recorded as sent |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: templates, blocking codes, result code maps and the retry limit are data.
- No personal data in logs, tests or prompts. The phone number and LINE identifier stay tokens in the Workbench; the ACE notification path detokenizes them. Test data uses synthetic tokens and test numbers only.
- No read of another module's tables. Deviations, contact points and the ledger go through their interfaces.
- No direct call to NSS or LINE OA; only the ACE notification path (REQ-DRI-006).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-004 | SMS and LINE through the bank's channel platforms, result on the case | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | R-UNI-33, R-UNI-34, R-UNI-40 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-06, TC-E2-022-07, TC-E2-022-08, TC-E2-022-09, TC-E2-022-12, TC-E2-022-13 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | R-UNI-04, R-UNI-05, R-UNI-20, R-DEV-16, R-UNI-39 | TC-E2-022-03, TC-E2-022-04, TC-E2-022-10, TC-E2-022-11, TC-E2-022-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | R-UNI-10 | TC-E2-022-05 |
| REQ-ILG-010 | Messages dispatched write their result to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-34 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-08 |

### 19. Out of scope

- Letters through WIN (RWB-E2-021).
- Messages sent automatically by route rules, for example the offer letter of R-RES-09 (Epic 3).
- The breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7).
- Self-service on LINE and HOME.SCB (FEAT-COM-01 to FEAT-COM-04, Epic 4).


---

## RWB-E2-023 Automated EFS file load

| Item | Value |
|---|---|
| Story key | RWB-E2-023 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CHO-10 Automate the EFS file load |
| Requirement IDs | REQ-RDF-007, REQ-RDF-006, REQ-CHO-001 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.1 and 5.3 |
| L3 process | 6.1 Take over the case at 90 days past due |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E2-001, RWB-E1-051 |
| Status | Ready for build |

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the EFS hand-over load automated end to end and reconciled each day, with the manual EFS file handling retired after ten clean days in a row**, so that **one checked path remains for every account handed over from collections**.

### 2. Business rationale

The EFS hand-over moves today by a manual file as well as the COLLINS load. Two paths give two answers and no one checks the difference. This story reconciles each day the accounts EFS hands over at 90 days past due against the cases created or linked, lists every difference, alerts above the threshold, and lets the data steward retire the manual path with a recorded sign-off after ten clean days. It meets REQ-RDF-007, REQ-RDF-006 and REQ-CHO-001.

### 3. Preconditions

- RWB-E2-001 (case creation from the COLLINS load) and RWB-E1-051 (feed jobs on Control-M) are done.
- JOB-04 Daily reconciliation runs after JOB-02.
- Parameter `recon.efs.alert_pct` = 0.1 percent (assumed; DL25 recommends zero) and parameter `recon.efs.clean_days_required` = 10.
- The manual EFS upload path is behind flag `rwb.integration.efs-manual-upload`, on until sign-off.
- The builder of the EFS file automation is the Workbench squad (DL30, option A assumed).
- The person holds RW-DATASTEW.

### 4. Flow

1. Scheduler: JOB-04 starts after JOB-02 for business date D.
2. SY-DATALOAD: the EfsReconService reads the count and the list of accounts EFS handed over at 90 days past due on D through the P1 EfsHandoverQuery.
3. SY-DATALOAD: reads the cases created and the accounts linked by JOB-02 for D from the hand-over run summary.
4. SY-DATALOAD: compares the two lists by account ID; each account on one side only is a difference with a reason (no case, held in the exception list, case without a hand-over).
5. SY-DATALOAD: writes each difference as a data quality exception with product DP05 and check "EFS hand-over reconciliation", and writes the day result (counts, difference percent, clean or not) to the run record.
6. SY-DATALOAD: when the difference is above the alert threshold, alerts the data steward and the platform administrator with MSG-P2-013.
7. Data steward: after ten clean days in a row, signs off the retirement of the manual EFS file handling.
8. System: checks the clean days, writes the sign-off record and switches flag `rwb.integration.efs-manual-upload` off for the environment.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Difference above 0.1 percent | Data steward and platform administrator alerted | MSG-P2-013 | AC3 |
| X2 | Difference at or below the threshold but not zero | Differences listed; no alert; the day is not clean | None | AC4 |
| X3 | Sign-off with fewer than ten clean days in a row | Refused; the manual path stays on | MSG-P2-014 | AC5 |
| X4 | JOB-02 did not run for D (late load) | No reconciliation for D; the day is not clean; the clean count restarts | MSG-P1-001 | AC6 |
| X5 | JOB-04 runs twice for D | The second run writes no new exception and no second alert | None | AC7 |
| X6 | A role without the right signs off | Refused; nothing changes | MSG-P4-002 | TC-E2-023-09 |
| X7 | Sign-off for an interface already retired | Refused; nothing changes | MSG-P2-019 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the hand-over run (RWB-E2-001) and the feeds (RWB-E1-051) |
| Negotiable | Threshold and clean days are parameters |
| Valuable | One checked path for the hand-over; the manual file ends |
| Estimable | One reconciliation step, one table, one endpoint |
| Small | Within one week with its tests |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

```gherkin
Feature: Automated EFS file load

  Background:
    Given parameter "recon.efs.alert_pct" is 0.1 and "recon.efs.clean_days_required" is 10

  Scenario: AC1 Reconciled
    Given the EFS data of business date 2026-12-14 in the COLLINS load hands over 104 accounts
    Given JOB-02 created 98 cases and linked 4 accounts for 2026-12-14
    When the reconciliation job runs
    Then the system compares the count of 104 accounts handed over with 102 accounts on cases
    Then the system lists the 2 differences as data quality exceptions with the account ID and the reason

  Scenario: AC2 Manual step retired
    Given the days 2026-12-03 to 2026-12-12 each reconciled with no difference
    When the data steward signs off on 2026-12-13
    Then the sign-off record holds the interface "INT-07", the dates 2026-12-03 to 2026-12-12, 10 clean days, the user and the time
    Then flag "rwb.integration.efs-manual-upload" is off in the environment
    Then the response carries message MSG-P2-015

  Scenario: AC3 Alert
    Given 2,000 accounts handed over on 2026-12-15 and 1,997 on cases, a difference of 0.15 percent
    When the job runs
    Then the data steward and the platform administrator are alerted with message MSG-P2-013

  Scenario: AC4 Small difference listed without an alert
    Given 2,000 accounts handed over on 2026-12-16 and 1,999 on cases, a difference of 0.05 percent
    When the job runs
    Then the system lists 1 difference
    Then the system sends no alert
    Then the system records the day as not clean

  Scenario: AC5 Sign-off too early
    Given 7 clean days in a row ending 2026-12-12
    When the data steward signs off
    Then the response is 409 with message MSG-P2-014
    Then flag "rwb.integration.efs-manual-upload" stays on

  Scenario: AC6 No hand-over run for the day
    Given JOB-02 did not run for business date 2026-12-17 because the load was late
    When the reconciliation job runs on 2026-12-18
    Then the system records no reconciliation for 2026-12-17
    Then 2026-12-17 counts as not clean and the clean count restarts at 0

  Scenario: AC7 Job run twice
    Given the reconciliation for 2026-12-15 listed 3 differences and sent 1 alert
    When the job is rerun for 2026-12-15
    Then the exception list still holds 3 differences for 2026-12-15
    Then the system sends no second alert

  Scenario: AC8 Sign-off after retirement refused
    Given the manual EFS file handling for "INT-07" was retired on 2026-12-13
    When the data steward signs off again on 2026-12-20
    Then the response is 409 with message MSG-P2-019
    Then the system writes no second sign-off record
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every account handed over from EFS has exactly one open case each day, reconciled each day | CTL-01; REC-01; REQ-RDF-007 |
| BR2 | Every difference is listed with its account and reason for the data steward | REC-01, Break goes to; REQ-RDF-008 |
| BR3 | A difference above the alert threshold alerts the data steward and the platform administrator; threshold 0.1 percent, assumed | DL25 |
| BR4 | A clean day is a day with a reconciliation and no difference | Story intent |
| BR5 | The manual EFS file handling ends only after ten clean days in a row and the data steward's sign-off, and the sign-off is kept | REQ-RDF-006 |
| BR6 | A repeat run for the same business date adds nothing | R-UNI-40 |
| BR7 | Threshold and clean days are parameters, never code | Principle 1 |

### 9. State transitions

None. This story does not change a case status. It writes the day result (clean or not) per business date, the sign-off record, and turns flag `rwb.integration.efs-manual-upload` from on to off.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Reads the differences; signs off the retirement (Reference data, RU) |
| RW-PLATADM, platform administrator | Receives alerts; reruns JOB-04 (Platform administration, U) |
| SY-DATALOAD, data load | Runs the reconciliation and writes the exceptions and the day result |
| RW-AUDIT, RW-COMPLY | Read the sign-off record (Platform administration, R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-001 | loan_account | id | Read |
| DF-ACC-014 | loan_account | days_past_due | Read |
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-CAS-026 | case_account | account_id | Read |
| DF-CAS-028 | case_account | linked_from | Read |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-OPS-158 | interface_run | checks | Write |
| DF-OPS-161 to DF-OPS-167 | interface_signoff | all fields | Write |
| DF-OPS-162 | interface_signoff | interface_id | Write |
| DF-OPS-163 | interface_signoff | from_date | Write |
| DF-OPS-164 | interface_signoff | to_date | Write |
| DF-OPS-165 | interface_signoff | clean_days | Write |
| DF-OPS-166 | interface_signoff | signed_by | Write |
| DF-OPS-167 | interface_signoff | signed_at | Write |
| DF-OPS-215 | feature_flag | uat_on | Write |
| DF-OPS-216 | feature_flag | prod_on | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Job step: EFS hand-over reconciliation in JOB-04 Daily reconciliation.** Trigger: daily after JOB-02. Input: EFS hand-over accounts for D; JOB-02 run summary for D. Output: data quality exceptions, the day result, the alert. Events: none. Idempotency key: "INT-07:" + business date. Restart: a rerun replaces the day result and writes only exceptions not already listed for D; the alert is sent once per business date.

**Endpoints.**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /admin/data-quality/exceptions?product=DP05&from=2026-12-14 | Query: product, from, to | Array of DataQualityException: id, product, check, record, raisedOn | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 | Platform administration, R | Read only |
| POST /admin/interfaces/{interfaceCode}/manual-retirement (new, recorded in additions) | ManualRetirementRequest: note (up to 500 characters) | 201 InterfaceSignoff: interfaceId, fromDate, toDate, cleanDays, signedBy, signedAt | 401; 403 (MSG-P4-002); 404 unknown interface (MSG-P4-003); 409 too few clean days (MSG-P2-014) or already retired (MSG-P2-019) | Reference data, U | One sign-off per interface; a repeat returns 409 |

**Published interfaces called.**

```java
// P1 recovery.data.api
List<UUID> EfsHandoverQuery.handedOver(LocalDate businessDate);
void DataQualityExceptions.add(String dataProduct, String check, String recordKey, LocalDate businessDate, String reason);
// P2 recovery.integration.handover.api (RWB-E2-001)
HandoverSummary HandoverRun.summary(LocalDate businessDate);
```

### 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/efsrecon`, Java package `recovery.integration.efsrecon`.

| Component | Type | Responsibility |
|---|---|---|
| EfsReconService | Service | Compares the two lists, writes exceptions, the day result and the alert |
| EfsReconStep | Job | Step of JOB-04 |
| CleanDayCounter | Service | Counts clean days in a row back from the last business date; a missing day breaks the count |
| ManualRetirementController | Controller | POST /admin/interfaces/{interfaceCode}/manual-retirement |
| ManualRetirementService | Service | Checks clean days, writes the sign-off, switches the flag off through FeatureFlagService |
| InterfaceSignoffRepository | Repository | interface_signoff only |

- **Database:** Flyway migration `V2026_12_23__p2_interface_signoff.sql` creates interface_signoff with the standard columns and a unique constraint on interface_id.
- **Configuration and reference data:** parameters recon.efs.alert_pct = 0.1 (assumed; DL25) and recon.efs.clean_days_required = 10 (RW-COE); flag rwb.integration.efs-manual-upload (RW-PLATADM).
- **Build steps:**
  1. Build EfsReconService with the compare and the reasons, with tests for each reason.
  2. Build EfsReconStep in JOB-04 with the idempotency key and the once-per-date alert.
  3. Build CleanDayCounter with tests for a gap day and a day with one difference.
  4. Write the migration and InterfaceSignoffRepository.
  5. Build ManualRetirementService and the endpoint with the flag switch and the ACE audit write.
- **Feature flag:** `rwb.integration.efs-recon`.
- **Done when:** the tests in section 16 pass and ten synthetic clean days in SIT allow the sign-off.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-013 | Difference above the alert threshold | {count} EFS hand-overs for {date} do not match a case ({pct} percent). See the data quality exceptions. |
| MSG-P2-014 | Sign-off refused | {count} clean days in a row so far. Sign-off needs {required}. |
| MSG-P2-019 | Sign-off for an interface already retired | Manual handling for {interface} was already retired on {date}. |
| MSG-P2-015 | Sign-off accepted | Manual EFS file handling ended on {date}. The sign-off is recorded. |
| MSG-P1-001 | No hand-over run for a late load | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the right signs off | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-45 Data quality, states loading and breaks: the data steward sees the EFS hand-over differences per business date. The sign-off is made through the endpoint from the same screen in Epic 2; alerts arrive by email.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-023-01 | AC1, BR1, BR2 | System | 104 synthetic hand-overs, 102 on cases |
| TC-E2-023-02 | AC2, BR5 | System | Ten clean synthetic days |
| TC-E2-023-03 | AC3, BR3 | System | 2,000 hand-overs, 3 differences |
| TC-E2-023-04 | AC4, BR4 | System | 2,000 hand-overs, 1 difference |
| TC-E2-023-05 | AC5, BR5 | System | Seven clean days |
| TC-E2-023-06 | AC6, BR4 | System | No JOB-02 run for 2026-12-17 |
| TC-E2-023-07 | AC7, BR6 | System | JOB-04 rerun for 2026-12-15 |
| TC-E2-023-08 | AC8, BR5 | System | Sign-off record for INT-07 already present |
| TC-E2-023-09 | Access | Access | RW-PLATADM (no Reference data U right) calls POST /admin/interfaces/{interfaceCode}/manual-retirement; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: threshold and clean days are parameters.
- No personal data in logs, tests or prompts; differences hold account IDs and reasons only.
- No read of another module's tables; hand-overs and exceptions go through the P1 interfaces.
- The manual path is switched off only through the sign-off.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Daily reconciliation with no variance | Program 5.1; Epic 2 3.2 | FEAT-CHO-10 | 6.1 Take over the case at 90 days past due | R-UNI-40 | TC-E2-023-01, TC-E2-023-03, TC-E2-023-04, TC-E2-023-07 |
| REQ-RDF-006 | Local copy retired with the owner's confirmation | Program 5.1; Epic 2 3.2 | FEAT-CHO-10 | 6.1 Take over the case at 90 days past due | None | TC-E2-023-02, TC-E2-023-05, TC-E2-023-08 |
| REQ-CHO-001 | Hand-over reaches the Workbench with its history | Program 5.3; Epic 2 3.2 | FEAT-CHO-10 | 6.1 Take over the case at 90 days past due | None | TC-E2-023-06 |

### 19. Out of scope

- The reconciliation of all accounts at 90 days past due against open cases (REC-01): RWB-E1-003.
- Retiring the Excel and SharePoint trackers: RWB-E1-012.
- A same-day hand-over event: DL06.


---

## RWB-E2-024 Field app photos and bills into the document hub

| Item | Value |
|---|---|
| Story key | RWB-E2-024 |
| Epic | E2, release 31 December 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-21 Take field app photos and bills into the OCR intake |
| Requirement IDs | REQ-DCM-013 |
| BRD section | Business Requirements Epic 2, section 3.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | D6.5 |
| Priority | Must |
| Depends on | RWB-E1-057, RWB-E1-032, RWB-E1-053, RWB-E1-024, RWB-E1-041 |
| Status | Ready for build |

### 1. Story

As a **field collector**, I want **photos, bills and checklists captured in the field app to enter the document hub against the case, with location and time**, so that **an inspection is on the case the same day it is made**.

### 2. Business rationale

Inspection photos and utility bills are sent today by chat or carried back to the office, and the date and place of an inspection cannot be shown when it is questioned. This story takes each capture from the field app into the same malware scan, store, OCR and extraction path as other documents, attached to the case with the capture time and the GPS position, including captures made with no signal. It meets REQ-DCM-013 and gives the deed in lieu inspection step (WITH_FIELD_INSPECTION, R-DIL-22) and the repossessed vehicle photo record (CTL-38) their evidence on the case.

### 3. Preconditions

- RWB-E1-041 (MalwareScanService.scanNow), RWB-E1-024 (DocumentStore.store), RWB-E1-049 (DocumentStoredListener creates the intake item for OCR) and RWB-E1-053 (extractStep for attached documents) are done; RWB-E1-057 and RWB-E1-032 give the same intake path for files with no case.
- The field app is a bank-managed mobile app that signs in with Entra ID as role RW-FIELDCOL and calls the Workbench API. This platform is assumed: no open decision covers it. Agency field teams reach the Workbench only through the external gateway (DL03), which is not in this story.
- The document type table holds INSPECTION_PHOTO (no fields), INSPECTION_CHECKLIST (no fields) and UTILITY_BILL (bill_amount, due_date, account_ref), loaded through the RWB-E1-025 loader (assumed; DL19).
- Rows in document_hub_parameter: CAPTURE_CLOCK_SKEW_MINUTES 5; CAPTURE_MAX_AGE_DAYS 30; CAPTURE_MAX_FILES 50; INTAKE_MAX_FILE_MB 25. Values assumed (DL11).
- The field collector has a task on the case, so the case is in Own scope.

### 4. Flow

1. Field collector: captures photos, bills and the checklist in the field app; the app records for each file the device time and GPS position, and a client file ID.
2. Field app: when a signal is available, sends the captures for the case to POST /cases/{caseId}/field-captures with a manifest of the items.
3. System: checks the role, the right and the case scope, and that every manifest item has one file and every file has one manifest item.
4. System: for each item, checks the client file ID against items already received for the case; a repeat returns the earlier result.
5. System: checks file type, size, capture time and position, writes the file to the intake container, and calls MalwareScanService.scanNow.
6. System: calls DocumentStore.store with the case, the type from the item kind (photo, bill, checklist), source UPLOAD, the file and its hash; the store writes the document, the DOCATT decision log entry and DocumentStored (EV-16).
7. System: in the same transaction sets on the document captured_at, capture_latitude, capture_longitude, client_file_id and capture_kind.
8. System: DocumentStoredListener (RWB-E1-049) creates the intake item for OCR; for a UTILITY_BILL, extractStep (RWB-E1-053) writes bill_amount and due_date on the document.
9. System: returns a result per item (accepted, duplicate, refused with the message).
10. Case owner: sees the inspection photos, bills and the bill fields on SCR-30 Case documents with capture time and position.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same client file ID is sent again | The earlier result is returned; nothing new is stored | None | AC4, AC5 |
| X2 | A capture has no GPS position | Stored without position; warning returned and shown | MSG-P5-015 | AC6 |
| X3 | Capture time later than receipt time plus the clock skew | Item refused; the other items are accepted | MSG-GEN-002 | AC7 |
| X4 | Capture time before the case entry date, or older than the age limit | Item refused | MSG-GEN-003 | AC8, AC9 |
| X5 | File type not allowed | Item refused | MSG-P5-001 | AC10 |
| X6 | Malware found | Item quarantined; incident raised | MSG-P5-016 | AC11 |
| X7 | The case is outside the collector's scope | 404; nothing stored | MSG-P4-003 | AC12 |
| X8 | A bill field is below the confidence threshold | Document in the review queue | MSG-P5-003 | AC13 |
| X9 | A manifest item without a file, or a file without an item | 422; nothing stored | MSG-GEN-001 | AC14 |
| X10 | More files than the limit in one request | 413; nothing stored | MSG-GEN-002 | AC15 |
| X11 | A role without Documents C sends captures | 403 | MSG-P4-002 | Access test TC-E2-024-16 |
| X12 | The decision log write fails for an item | Item refused; nothing stored for it | MSG-P7-003 | Principle 5 test TC-E2-024-17 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reuses the Epic 1 scan, store, OCR and extraction path; needs no other Epic 2 story |
| Negotiable | Types, fields, limits and the clock skew are data and parameters |
| Valuable | The inspection evidence is on the case the day it is made, with time and place |
| Estimable | One endpoint, one service, five columns on document, one panel change on SCR-30 |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic files |

### 7. Acceptance criteria

```gherkin
Feature: Field app photos and bills into the document hub

  Background:
    Given case "RW-2026-000501" with entry date 2026-10-02 and a field inspection task for field collector "FC-01" with role RW-FIELDCOL
    Given the clock skew is 5 minutes and the age limit is 30 days

  Scenario: AC1 Capture
    Given an inspection with eight photos and two bills, each with a client file ID, a capture time and a GPS position
    When the officer syncs at 2026-12-15 14:20
    Then ten documents are on case "RW-2026-000501" with source "UPLOAD": eight "INSPECTION_PHOTO" and two "UTILITY_BILL"
    Then each document shows its capture time and its latitude and longitude, for example 13.7563 and 100.5018
    Then the two bills have intake items for OCR
    Then ten DocumentStored events are in the outbox

  Scenario: AC2 Offline
    Given no signal during the visit and photos captured at 2026-12-14 10:05
    When the officer syncs later at 2026-12-15 08:30
    Then each document has captured_at 2026-12-14 10:05 and its stored date 2026-12-15 08:30

  Scenario: AC3 Bill extracted
    Given a utility bill photo showing amount "1,284.50" and due date "28/12/2569"
    When extraction runs
    Then bill_amount "1284.50" and due_date "2026-12-28" are on the case in the document index

  Scenario: AC4 The same sync sent twice
    Given the ten items of AC1 were received
    When the app sends the same ten client file IDs again
    Then the response marks all ten as "DUPLICATE"
    Then the case still has ten documents from this inspection

  Scenario: AC5 A sync cut off and resent
    Given six of ten items were received before the connection dropped
    When the app sends all ten again
    Then six items are "DUPLICATE" and four are "ACCEPTED"
    Then the case has ten documents from this inspection

  Scenario: AC6 A capture with no position
    Given a photo with capture time 2026-12-15 13:58 and no GPS position
    When the officer syncs
    Then the document is on the case with no latitude and longitude
    Then the response and SCR-30 show MSG-P5-015 with count 1

  Scenario: AC7 A capture time in the future
    Given the server receives the sync at 2026-12-15 14:20
    Given one photo has capture time 2026-12-15 14:26 and another 2026-12-15 14:25
    When the officer syncs
    Then the system refuses the photo at 14:26 with MSG-GEN-002
    Then the system accepts the photo at 14:25

  Scenario: AC8 A capture time before the case entry date
    Given a photo with capture time 2026-10-01 09:00, before the entry date 2026-10-02
    When the officer syncs
    Then the system refuses the item with MSG-GEN-003 naming "Capture time" and "Case entry date"

  Scenario: AC9 A capture older than the age limit
    Given the sync is at 2026-12-15 14:20
    Given one photo was captured at 2026-11-14 14:19, 31 days earlier, and another at 2026-11-15 14:20
    When the officer syncs
    Then the system refuses the first photo with MSG-GEN-003 naming "Capture time" and the age limit date 2026-11-15
    Then the system accepts the second photo

  Scenario: AC10 A file type not allowed
    Given a photo in HEIC format
    When the officer syncs
    Then the system refuses the item with MSG-P5-001
    Then the system accepts the other items in the same sync

  Scenario: AC11 Malware in a capture
    Given a file carrying the EICAR test signature
    When the officer syncs
    Then the system quarantines the item with MSG-P5-016 and an incident is raised
    Then the system writes no document for it

  Scenario: AC12 A case outside the collector's scope
    Given case "RW-2026-000502" where "FC-01" has no task
    When the app sends captures for "RW-2026-000502"
    Then the response is 404 with MSG-P4-003
    Then no file or document is stored

  Scenario: AC13 A bill field below the threshold
    Given the bill amount is read with confidence 0.5500 and the threshold is 0.80
    When extraction runs
    Then bill_amount has state "REVIEW" and the document is in the review queue
    Then SCR-30 shows MSG-P5-003 on the bill

  Scenario: AC14 A manifest that does not match the files
    Given a manifest of three items and two files
    When the officer syncs
    Then the response is 422 with MSG-GEN-001 naming the client file ID with no file
    Then the system stores nothing

  Scenario: AC15 Too many files in one sync
    Given 51 files in one sync and a limit of 50
    When the officer syncs
    Then the response is 413 with MSG-GEN-002 naming "Files", 1 and 50
    Then the system stores nothing
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every field capture goes through the same checks as other documents: type, size, malware scan before storage | REQ-DCM-013; RWB-E1-041; RWB-E1-024 |
| BR2 | The capture time is the device time recorded at capture; the receipt time is the server time | FEAT-DCM-21 |
| BR3 | A capture time later than receipt plus the clock skew, before the case entry date, or older than the age limit is refused | CAPTURE_CLOCK_SKEW_MINUTES (5), CAPTURE_MAX_AGE_DAYS (30), assumed; DF-CAS-013 |
| BR4 | The client file ID is unique per case; a repeat returns the earlier result | R-UNI-40 |
| BR5 | The item kind sets the document type: photo to INSPECTION_PHOTO, bill to UTILITY_BILL, checklist to INSPECTION_CHECKLIST; no classification runs | Document types reference table; DL19 |
| BR6 | A capture is attached to the case named in the request; no case matching runs | FEAT-DCM-12 is not needed when the case is known |
| BR7 | Bills are extracted with the UTILITY_BILL field list; a low-confidence field goes to review | RWB-E1-053 BR2; RWB-E1-054 |
| BR8 | A capture with no position is stored and flagged | FEAT-DCM-21 |
| BR9 | GPS position and photos of a home are personal data: masked by role and never logged | CTL-11; DL26 |
| BR10 | A capture that cannot be written to the decision log through the store is not stored | Principle 5; R-UNI-39 |

### 9. State transitions

None. This story does not change a case status. It stores documents with review_status NOT_NEEDED, or PENDING when a bill field is in review. The inspection task and the R-DIL-22 move to ASSET_UNLOCK_DECISION are in Epic 3.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-FIELDCOL, field collector | Sends captures for cases in Own scope (Documents CR) |
| RW-CASEOWN, case owner | Reads the captures and bill fields on the case (Documents CRU) |
| RW-RESTRUCT, restructuring officer (FCR) | Reads the captures on deed in lieu cases (Documents CRU) |
| SY-OCR, OCR and extraction pipeline | Runs OCR and extraction on bills and checklists (Documents CRU) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry through DocumentStore |
| RW-PHONECOL, phone collector | Reads only (Documents R); cannot send captures |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read, through CaseDirectory |
| DF-CAS-013 | recovery_case | entry_date | Read, through CaseDirectory |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Write, through DocumentStore |
| DF-DOC-027 | document | captured_at | Write |
| DF-DOC-028 | document | capture_latitude | Write |
| DF-DOC-029 | document | capture_longitude | Write |
| DF-DOC-030 | document | client_file_id | Write |
| DF-DOC-031 | document | capture_kind | Write |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Write, through RWB-E1-053 |
| DF-REF-219 | document_type | doc_type_code | Read |
| DF-REF-224 | document_type | field_definitions | Read |
| DF-REF-246 | document_hub_parameter | param_value | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through DocumentStore and DecisionLogWriter |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /cases/{caseId}/field-captures** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | multipart/form-data: manifest (JSON: inspectionRef, items of clientFileId, kind PHOTO, BILL or CHECKLIST, capturedAt date-time with offset, latitude, longitude, fileName) and one file part per item named by clientFileId |
| Response | 201 FieldCaptureResult: items of clientFileId, status (ACCEPTED, DUPLICATE, REFUSED, QUARANTINED), documentId, messageCode |
| Errors | 401 (MSG-P4-001); 403 no Documents C (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 413 too many files (MSG-GEN-002); 422 manifest and files do not match (MSG-GEN-001); 503 store or scanning service unavailable (MSG-GEN-006) |
| Authorization | Documents, right C, scope applied |
| Idempotency | clientFileId unique per case; a repeated item returns DUPLICATE with the first documentId |

Item-level refusals (MSG-GEN-002, MSG-GEN-003, MSG-P5-001, MSG-P5-016, MSG-P5-017, MSG-P7-003) do not fail the request; each is returned on its item. Warning MSG-P5-015 is returned when any accepted item has no position.

**Events published:** DocumentStored (EV-16) per accepted item, through DocumentStore; DocumentFieldsExtracted (EV-17) for bills through RWB-E1-053.

**Published interfaces called**

```java
// P5, RWB-E1-041
ScanResult MalwareScanService.scanNow(BlobRef file, Duration timeout);
// P5, RWB-E1-024
StoredDocument DocumentStore.store(StoreRequest request);
// P3
Optional<CaseSummary> CaseDirectory.findById(UUID caseId);
```

### 13. Solution plan

**Package.** folder `recovery/dochub/fieldcapture`, Java package `recovery.dochub.fieldcapture`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| FieldCaptureController | Controller | POST /cases/{caseId}/field-captures; manifest parsing and matching to file parts |
| FieldCaptureService | Service | BR1 to BR10 per item: duplicate check, type, size, time and position checks, scan, store, capture columns |
| DocumentHubRepository | Repository | Sets the capture columns on the stored document; looks up client_file_id per case |
| CaptureDetails | React component | On SCR-30: capture time, position and a map link for each capture; MSG-P5-015 flag |

**Database**

- Flyway migration `V2_5_024__field_capture.sql` adds to document: captured_at timestamptz, capture_latitude numeric(9,6), capture_longitude numeric(9,6), client_file_id varchar(64), capture_kind varchar(12).
- Constraint `ux_document_client_file ON document (case_id, client_file_id) WHERE client_file_id IS NOT NULL`.
- Reads recovery_case.entry_date through CaseDirectory.

**Configuration and reference data**

- Document type rows INSPECTION_PHOTO, INSPECTION_CHECKLIST, UTILITY_BILL with the UTILITY_BILL fields, loaded through the RWB-E1-025 loader (DL19).
- document_hub_parameter rows CAPTURE_CLOCK_SKEW_MINUTES 5, CAPTURE_MAX_AGE_DAYS 30, CAPTURE_MAX_FILES 50 (assumed; DL11); INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB from RWB-E1-057.

**Build steps**

1. Write the migration and the client file ID constraint; repository tests.
2. Build manifest parsing and file-part matching with the 422 and 413 checks.
3. Build FieldCaptureService per item: duplicate check, type, size, time and position checks, write to the intake container, scanNow, DocumentStore.store, capture columns in the same transaction.
4. Check that DocumentStoredListener (RWB-E1-049) creates the intake item with the given type, so classifyStep skips it and extractStep reads the UTILITY_BILL fields.
5. Build CaptureDetails on SCR-30 with masking of the position for roles without the right to see it.
6. Add the contract test for the new endpoint (RWB-TE-003) and an offline replay test with a cut-off sync.

**Feature flag:** `rwb.dochub.field-capture`. Off: the endpoint returns 404.

**Done when:** the tests in section 16 pass and a synthetic inspection of ten files is on the case within 5 minutes of sync in SIT (target assumed; DL11).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-015 | Captures accepted with no GPS position (new) | {count} files have no location. They are on the case without a position. |
| MSG-P5-001 | File type not allowed | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-003 | A bill field needs checking | Some fields need checking. The document is in the review queue. |
| MSG-P5-016 | A capture with malware | This file was not stored because the malware scan found a threat. It is held in quarantine. |
| MSG-P5-017 | A capture above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-P7-003 | Decision log write failed for an item | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Manifest and files do not match | Enter {field}. |
| MSG-GEN-002 | Capture time in the future; too many files | {field} must be between {min} and {max}. |
| MSG-GEN-003 | Capture time before the case entry date or the age limit | {field} cannot be before {other}. |
| MSG-P4-002 | Role without Documents C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the collector's scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-30 Case documents | List | Sees inspection photos, checklists and bills with capture time and position; bill fields with confidence; MSG-P5-015 on captures without position |
| SCR-31 Document review queue | List | Sees a bill with a low-confidence field (RWB-E1-054) |

The field app screens belong to the field app and are not in this story.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-024-01 | AC1, BR1, BR5, BR6 | System | Ten synthetic files with positions in Bangkok |
| TC-E2-024-02 | AC2, BR2 | System | Capture one day before sync |
| TC-E2-024-03 | AC3, BR7 | System | Synthetic utility bill image |
| TC-E2-024-04 | AC4, BR4 | System | Same ten client file IDs twice |
| TC-E2-024-05 | AC5, BR4 | System | Six of ten received, then all ten resent |
| TC-E2-024-06 | AC6, BR8 | System | Photo with no position |
| TC-E2-024-07 | AC7, BR3 | System | Capture times 6 and 5 minutes after receipt |
| TC-E2-024-08 | AC8, BR3 | System | Capture one day before the entry date |
| TC-E2-024-09 | AC9, BR3 | System | Captures 31 days and 30 days before sync |
| TC-E2-024-10 | AC10, BR1 | System | HEIC file |
| TC-E2-024-11 | AC11, BR1 | System | EICAR test file |
| TC-E2-024-12 | AC12 | System | Case with no task for FC-01 |
| TC-E2-024-13 | AC13, BR7 | System | Bill amount at confidence 0.55 |
| TC-E2-024-14 | AC14 | System | Three items, two files |
| TC-E2-024-15 | AC15 | System | 51 files |
| TC-E2-024-16 | Access | Access | RW-PHONECOL user (Documents R) calls POST field-captures; refused with MSG-P4-002 |
| TC-E2-024-17 | Principle 5 | Resilience | Decision log write forced to fail during a sync of three files; no document stored, items returned with MSG-P7-003, incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: types, fields, the clock skew, the age limit and the file limit are data and parameters.
- No personal data in logs, tests or prompts: positions, file names and bill values are not logged; test photos show no person or real address.
- No read of another module's tables: the case entry date and scope come through the P3 case interface and the ACE common access check.
- The device time is stored as sent, with its offset; the server never replaces it.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-21 | 13 Manage documents and correspondence | R-DIL-22, R-UNI-39, R-UNI-40 | TC-E2-024-01 to TC-E2-024-17 |

### 19. Out of scope

- The field app itself and its offline store.
- Agency field teams reaching the Workbench through the external gateway (DL03; FEAT-PRM-15, Epic 7).
- The inspection task, the checklist rule and the asset unlock rule (FEAT-TRT-15 and R-DIL-22, Epic 3).
- The repossessed vehicle photo standard (CTL-38, Epic 7).


---

## RWB-E2-025 Extraction for the stage 2 and 3 document types

| Item | Value |
|---|---|
| Story key | RWB-E2-025 |
| Epic | E2, release 31 December 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-22 Extend extraction to the stage 2 and 3 document types |
| Requirement IDs | REQ-DCM-006, REQ-DCM-005 |
| BRD section | Business Requirements Epic 2, section 3.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | D7.2 |
| Priority | Must |
| Depends on | RWB-E1-053, RWB-E1-050, RWB-E1-054 |
| Status | Ready for build |

### 1. Story

As a **litigation officer**, I want **field extraction extended to the stage 2 and 3 types: contracts, credit approvals, mortgage documents, court filings, hearing notices and judgments**, so that **the litigation pack and the treatment record fill themselves**.

### 2. Business rationale

The litigation pack and the treatment record need the contract amount, the mortgage registration, the black and red case numbers, the hearing dates and the judgment amount, which officers read from paper and type in today. This story adds five document types to classification and extraction and extends the hearing notice fields, using the Epic 1 extraction and review path, so these values reach the case index with a confidence and a person checks only the uncertain ones. It meets REQ-DCM-006 and REQ-DCM-005 for the stage 2 and 3 types, and prepares the pack assembly of R-LIT-16 and the treatment documents of FEAT-TRT-18.

### 3. Preconditions

- RWB-E1-050 (classifyStep), RWB-E1-053 (extractStep, extractors, normalizer, evaluation runner) and RWB-E1-054 (review queue) are done.
- A document type table version DOCTYPE-2026.12 is prepared through the RWB-E1-025 loader with the five new types, their classify_threshold and their field_definitions (section 13), signed by legal counsel and the Head of NPA (assumed list; DL19). Hearing notices stay under the Epic 1 type COURT_NOTICE.
- A labeled sample of 60 documents, 10 for each of the five new types and 10 court notices, is in the SIT test data store, masked (RWB-TE-004).
- The classifier version that knows the new types is trained on the sample and selected through the agent runtime (P10).
- The pass mark for field accuracy is 0.90 per field on the sample (document_hub_parameter EXTRACT_ACCURACY_PASS, assumed; DL11).
- DL30 names the Workbench squads as the builder of stage 2 and 3 extraction where no bank-wide service exists; this story assumes option A.

### 4. Flow

1. Reference data administrator: loads DOCTYPE-2026.12 with valid from 2026-12-31 after approval.
2. JOB-12 Document intake: an inbound contract, credit approval, mortgage document, court filing, hearing notice or judgment passes scanStep and ocrStep (RWB-E1-041, RWB-E1-049).
3. ClassifyStep (RWB-E1-050): the classifier version for the eleven types returns a type and a confidence; below the classify_threshold of the type the item goes to the review queue with reason LOW_CONFIDENCE.
4. ExtractStep (RWB-E1-053): reads the field definitions of the type from DocumentTypeCatalog for the version in force and calls the extractor named by extraction_method.
5. System: normalizes each value, checks it against the field pattern held in the type table, and writes document_field rows with confidence and state.
6. System: a field below the threshold, failing its pattern or marked review-only gets state REVIEW and the document goes to the review queue.
7. MatchStep (RWB-E1-032): stores the document with its fields through DocumentStore; DocumentFieldsExtracted (EV-17) is written for documents already attached.
8. Litigation officer: sees the fields on SCR-30, and checks the marked ones on SCR-31.
9. S4 and S2 modules: read confirmed field values through DocumentFieldReader to fill the pack and the treatment record (from Epic 3 and Epic 5).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field is below the threshold | Field state REVIEW; document in the review queue with the field marked | MSG-P5-003 | AC3 |
| X2 | A field's accuracy on the sample is below the pass mark | Field proposed as review-only in the next table version | None | AC4 |
| X3 | A value does not match the field pattern | Field state REVIEW | MSG-P5-003 | AC8 |
| X4 | A document arrives before the new table version is in force | Classified against the earlier version; goes to review with reason UNKNOWN_TYPE | MSG-P5-003 | AC6 |
| X5 | A reader asks for fields still in REVIEW | Only fields in state OK, CONFIRMED or CORRECTED are returned | None | AC9 |
| X6 | The document is write-once | Fields are written; the file and write_once are unchanged | None | AC10 |
| X7 | The document is outside the caller's scope | 404 | MSG-P4-003 | AC11 |
| X8 | A role without Documents R reads the document | 403 | MSG-P4-002 | Access test TC-E2-025-12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reuses the Epic 1 extraction and review path; adds data, a classifier version and one reader |
| Negotiable | Types, fields, patterns and pass marks are data |
| Valuable | Pack and treatment values reach the case without typing |
| Estimable | One table version, one classifier version, field patterns, one published reader |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with the labeled sample or synthetic documents |

### 7. Acceptance criteria

```gherkin
Feature: Extraction for the stage 2 and 3 document types

  Background:
    Given the document type table version "DOCTYPE-2026.12" is in force from 2026-12-31
    Given the field threshold is 0.80 and the accuracy pass mark is 0.90
    Given the labeled sample holds 60 documents: 10 each of CONTRACT, CREDIT_APPROVAL, MORTGAGE_DOCUMENT, COURT_FILING, JUDGMENT and COURT_NOTICE

  Scenario: AC1 Court notice
    Given the 10 scanned court notices of the sample with 30 labeled values of court_name, black_case_no and hearing_date
    When extraction runs
    Then court, case number and hearing date are on the index
    Then at least 27 of the 30 values match the labels, which is 90% field accuracy on the sample

  Scenario: AC2 Contract
    Given a signed contract "DOC-0601" on case "RW-2026-000601" classified "CONTRACT" with confidence 0.9300
    Given its text names two parties, amount "2,400,000.00 บาท" and date "1 พฤศจิกายน 2569"
    When extraction runs
    Then party_names holds the two party names, masked in responses for roles without the right
    Then contract_amount is "2400000.00" and contract_date is "2026-11-01"

  Scenario: AC3 Low confidence
    Given a judgment "DOC-0602" whose judgment_amount is read with confidence 0.7100
    When extraction runs
    Then judgment_amount has state "REVIEW"
    Then the document is in the review queue on SCR-31 with judgment_amount marked
    Then SCR-30 shows MSG-P5-003 on "DOC-0602"

  Scenario: AC4 A field below the pass mark is proposed as review-only
    Given judgment_amount matches the labels on 8 of the 10 sample judgments
    When the extraction evaluation run processes the sample
    Then the report lists judgment_amount at 0.80, below the pass mark 0.90
    Then the proposed table version marks judgment_amount review_only = true
    Then the version in force does not change until it is loaded

  Scenario: AC5 Classification into the new types
    Given the 50 sample documents of the five new types
    When classification runs with the new classifier version
    Then the system gives each document one of the eleven types with a confidence
    Then the report shows the confusion matrix and at least 45 of 50 correct

  Scenario: AC6 A document before the new version is in force
    Given a judgment "DOC-0603" received on 2026-12-26, before the valid-from date of "DOCTYPE-2026.12"
    When it is classified and extracted
    Then the system classifies it against the six types of "DOCTYPE-2026.11"
    Then the classifier returns "JUDGMENT", which is not in that version, so the item goes to the review queue with review_reason "UNKNOWN_TYPE"

  Scenario: AC7 A Thai judgment date in Buddhist Era
    Given a judgment whose text reads "พิพากษา ณ วันที่ 5 มีนาคม 2570"
    When extraction runs
    Then judgment_date is "2027-03-05"

  Scenario: AC8 A value that does not match its pattern
    Given the pattern for red_case_no is two to four letters, a space, digits, "/" and four digits
    Given the extractor reads red_case_no "Por345-2570" with confidence 0.9200
    When extraction runs
    Then red_case_no has state "REVIEW"
    Then a value "Por 345/2570" with confidence 0.9200 has state "OK"

  Scenario: AC9 Readers get only checked or confident values
    Given judgment "DOC-0602" has red_case_no in state "OK" and judgment_amount in state "REVIEW"
    When the litigation module calls DocumentFieldReader for case "RW-2026-000601" and type "JUDGMENT"
    Then the system returns red_case_no
    Then the system does not return judgment_amount until it is confirmed or corrected

  Scenario: AC10 A write-once document is not altered
    Given judgment "DOC-0604" is held write-once with write_once true
    When extraction runs
    Then the system writes four document_field rows
    Then the stored file hash, storage_ref and write_once are unchanged

  Scenario: AC11 A document outside the caller's scope
    Given a litigation officer with scope team "LIT-BKK"
    Given document "DOC-0605" belongs to a case of team "LIT-NE"
    When the officer calls GET /api/recovery/v1/documents/DOC-0605
    Then the response is 404 with MSG-P4-003
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The stage 2 and 3 types and their fields are those of the document type table version in force on the extraction date | Document types reference table; DL19; R-UNI-38 |
| BR2 | A field below the threshold, failing its pattern, or marked review-only has state REVIEW and sends the document to the review queue | RWB-E1-053 BR2, BR3; REQ-DCM-005 |
| BR3 | A field whose accuracy on the sample is below the pass mark is proposed as review-only; the proposal takes effect only when loaded | EXTRACT_ACCURACY_PASS (0.90 assumed); DL11; CTL-08 |
| BR4 | Each field may carry a pattern in field_definitions; the pattern is data | Principle 1; RWB-E1-053 BR5 |
| BR5 | Readers in other modules receive only fields in state OK, CONFIRMED or CORRECTED | FEAT-DCM-10 |
| BR6 | Extraction never changes the stored file of a write-once document | CTL-12 |
| BR7 | Party names and other personal field values are masked unless the role may see them | DF-DOC-015; CTL-11; DL26 |
| BR8 | Dates read in Buddhist Era are stored as ISO dates | RWB-E1-053 BR6 |

### 9. State transitions

None. This story does not change a case status. It sets document_field.state and document.review_status as in RWB-E1-053.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Classifies and extracts the new types (Documents CRU) |
| RW-LITOFF, litigation officer | Reads and checks the fields in scope (Documents CRU) |
| RW-RESTRUCT, restructuring officer (FCR) | Reads and checks contract, credit approval and mortgage fields in scope (Documents CRU) |
| RW-REFADM, reference data administrator | Loads DOCTYPE-2026.12 (Reference data CRUD) |
| Business lead with Legal | Approves the new type and field list (DL19) |
| RW-COE, center of excellence analyst | Reads the evaluation report |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Read |
| DF-DOC-002 | document | case_id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-006 | document | storage_ref | Read |
| DF-DOC-008 | document | review_status | Write |
| DF-DOC-010 | document | write_once | Read |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Write |
| DF-DOC-034 | document_field | extracted_value | Write |
| DF-DOC-035 | document_field | extractor_version | Write |
| Standard column | document_field | state, is_active | Write |
| DF-DOC-070 | document_intake | predicted_type | Write (by classifyStep with the new classifier version) |
| DF-DOC-071 | document_intake | classification_confidence | Write (by classifyStep with the new classifier version) |
| DF-DOC-080 | document_intake | review_reason | Write (by classifyStep with the new classifier version) |
| DF-DOC-077 | document_intake | extracted_fields | Write |
| DF-DOC-078 | document_intake | extract_status | Write |
| DF-REF-219 | document_type | doc_type_code | Read |
| DF-REF-233 | document_type | classify_threshold | Read |
| DF-REF-224 | document_type | field_definitions | Read |
| DF-REF-246 | document_hub_parameter | param_value | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Published interface (P5) for S4 and S2**

```java
package recovery.dochub.extract;
public interface DocumentFieldReader {
    List<CheckedField> checkedFields(UUID caseId, String documentType);
}
// CheckedField: documentId, docVersion, fieldName, value, state (OK, CONFIRMED, CORRECTED), confidence
```

The caller passes its own service identity; values are returned unmasked only to a module whose purpose needs them (SY-CASEWF, SY-AGENT), and never logged.

**Event published:** DocumentFieldsExtracted (EV-17), as in RWB-E1-053.

**Endpoint read:** GET /api/recovery/v1/documents/{documentId}, as in RWB-E1-053 (Documents R, scope applied; 401, 403 MSG-P4-002, 404 MSG-P4-003, 503 MSG-GEN-006).

**Idempotency:** document ID, doc_version and table version, as in RWB-E1-053.

### 13. Solution plan

**Package.** folder `recovery/dochub/extract`, Java package `recovery.dochub.extract` (extends RWB-E1-053).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ExtractStep, FieldExtractionService | Job, Service | From RWB-E1-053; no change in code for the new types |
| DocumentFieldReader | Published interface | Checked fields for a case and type (BR5) |
| DocumentFieldReaderImpl | Service | Implements the reader with masking rules |
| ExtractionEvaluationRunner | Job | Adds field accuracy against the pass mark and the confusion matrix for the classifier |
| DocumentFieldRepository | Repository | Query by case, type and state |

**Database**

- No new table or column. Reads and writes document_field as in RWB-E1-053.
- Index `ix_document_type_case ON document (case_id, document_type)` for the reader.

**Configuration and reference data**

- Document type table version DOCTYPE-2026.12 (RWB-E1-025 loader), loaded by RW-REFADM, signed by legal counsel and the Head of NPA (DL19). Assumed new types and fields: CONTRACT (contract_no, party_names, contract_amount, contract_date); CREDIT_APPROVAL (approval_no, approved_amount, approval_date, approval_level); MORTGAGE_DOCUMENT (title_doc_no, mortgage_amount, registration_date, land_office); COURT_FILING (court_name, black_case_no, filing_date, claim_amount); JUDGMENT (court_name, red_case_no, judgment_date, judgment_amount). COURT_NOTICE keeps court_name, black_case_no, notice_date and hearing_date from DOCTYPE-2026.11. Each field has data type, method, review_only and an optional pattern.
- document_hub_parameter row EXTRACT_ACCURACY_PASS 0.90 (assumed; DL11), loaded by the reference data administrator.
- Classifier version for the eleven types, selected through the agent runtime (P10).

**Build steps**

1. Prepare the load file for DOCTYPE-2026.12 with a test case per new row; validate it in SIT.
2. Add the patterns of the new fields to the load file; unit tests for AC8 against ValueNormalizer (RWB-E1-053).
3. Add the new types to the TemplateFieldExtractor and ModelFieldExtractor configuration through the type table only; no code per type.
4. Extend ExtractionEvaluationRunner with field accuracy and the confusion matrix; run it on the 60-document sample.
5. Build DocumentFieldReader with the state filter and masking; contract test from the S4 side.
6. Run the regression set of RWB-E1-053 to show the six Epic 1 types are unchanged.

**Feature flag:** `rwb.dochub.extraction-stage23`. Off: the new types are not offered to classification and DocumentFieldReader returns nothing for them.

**Done when:** the tests in section 16 pass and the evaluation report for the 60-document sample is attached to the story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | A document has a field in REVIEW | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | Caller lacks Documents R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Document outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | The document store is unavailable | {system} is not available. Your request is queued and will be retried. |

Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-30 Case documents | List | Sees the new types with their fields and confidence; MSG-P5-003 on documents with fields in review |
| SCR-31 Document review queue | List; reviewed | Checks and corrects marked fields of the new types (RWB-E1-054) |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-025-01 | AC1, BR1 | System | 10 masked court notices from the sample |
| TC-E2-025-02 | AC2, BR7, BR8 | System | Synthetic signed contract with two parties |
| TC-E2-025-03 | AC3, BR2 | System | Judgment with amount at confidence 0.71 |
| TC-E2-025-04 | AC4, BR3 | System | 10 sample judgments, 8 amounts correct |
| TC-E2-025-05 | AC5 | System | 50 sample documents of the new types |
| TC-E2-025-06 | AC6, BR1 | System | Judgment received the day before the valid-from date |
| TC-E2-025-07 | AC7, BR8 | System | Judgment dated 5 March 2570 |
| TC-E2-025-08 | AC8, BR4 | System | Red case numbers with and without the pattern |
| TC-E2-025-09 | AC9, BR5 | System | Judgment with one OK and one REVIEW field |
| TC-E2-025-10 | AC10, BR6 | System | Write-once judgment |
| TC-E2-025-11 | AC11 | System | Document of team LIT-NE |
| TC-E2-025-12 | Access | Access | RW-REFADM user (Documents -) calls GET /documents/{documentId}; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: types, fields, patterns, thresholds and pass marks are data and parameters; no class per document type.
- No personal data in logs, tests or prompts: party names and amounts never enter a log or an event; the sample is masked.
- No read of another module's tables: S4 and S2 read through DocumentFieldReader; P5 writes nothing to legal_action, hearing or treatment.
- The Epic 1 types keep their results: the RWB-E1-053 tests run unchanged in the regression suite.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted into the index for the agreed types, in Thai and English | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38, R-LIT-16 | TC-E2-025-01, TC-E2-025-02, TC-E2-025-04 to TC-E2-025-12 |
| REQ-DCM-005 | Classified with a confidence; below the threshold to the review queue | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38 | TC-E2-025-03, TC-E2-025-05, TC-E2-025-06, TC-E2-025-09 |

### 19. Out of scope

- Writing extracted values into legal_action, hearing or treatment (S4 in Epic 5, S2 in Epic 3).
- Litigation pack assembly and the defect list check (FEAT-LIT-04, FEAT-LIT-05, Epic 5).
- Generation of contract, credit approval and mortgage documents (RWB-E2-026).
- Electronic discovery and court evidence attributes (REQ-DCM-017, REQ-DCM-018).


---

## RWB-E2-026 Document generation engine for contract, CA and mortgage templates

| Item | Value |
|---|---|
| Story key | RWB-E2-026 |
| Epic | E2, release 31 December 2026 |
| Module | P5 Document hub |
| Feature | FEAT-OCC-07 Generate contract, credit approval and mortgage documents |
| Requirement IDs | REQ-DCM-012, REQ-OCC-002 |
| BRD section | Business Requirements Epic 2, section 3.5 |
| L3 process | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence |
| Decision | D6.4, D6.5 |
| Priority | Must |
| Depends on | RWB-E1-046, RWB-E1-034, RWB-E1-024, RWB-E1-027 |
| Status | Ready for build |

### 1. Story

As a **restructuring officer (FCR)**, I want **the generation engine that fills the contract, credit approval and mortgage templates from the case facts with the merge field catalog and Legal-approved versions**, so that **the documents the screens generate are correct and versioned**.

### 2. Business rationale

Deed in lieu and restructure document sets are typed today from the case file into Word templates, and a wrong amount or an old template wording reaches the customer. This engine fills each Legal-approved template version from the case facts held in the Workbench, refuses to produce a document with a missing value or an unapproved template, and records which template version and which inputs produced each document. It meets REQ-DCM-012 and REQ-OCC-002, applies control CTL-14 to the deed in lieu and restructure documents, and supports the target of 1,000 deed in lieu cases a month in 2027 (NFR-006).

### 3. Preconditions

- RWB-E1-046 (template and merge field catalog as data) and RWB-E1-034 (template versions with the Legal approval record) are done.
- RWB-E1-027 (decision log writer) and RWB-E1-024 (document store) are done.
- Templates DIL-CONTRACT, DIL-CA and DIL-MORTGAGE, and RES-AGREEMENT for restructure, are loaded in Thai with approved_by_legal = true (template codes assumed; DL28).
- The template-to-document-type mapping is in the document type table: DIL-CONTRACT to CONTRACT, DIL-CA to CREDIT_APPROVAL, DIL-MORTGAGE to MORTGAGE_DOCUMENT, RES-AGREEMENT to CONTRACT (assumed; DL19).
- The case has a treatment of type DEED_IN_LIEU or RESTRUCTURE with decision_log_id set (approved at D6.4) and no outcome yet.
- The merge field providers of P3 (case), S2 (treatment), P1 (party and collateral) are listed in the MergeFieldResolver configuration.
- The caller holds Documents C (RW-RESTRUCT or RW-CASEOWN), or is the service identity SY-CASEWF for rule-driven generation from Epic 3.

### 4. Flow

1. Restructuring officer or SY-CASEWF: requests generation for a case, a treatment and a list of template codes.
2. System: reads the treatment through TreatmentReader and checks it is approved and open.
3. System: for each template code, reads the current version from the template catalog for the language and product group: approved by Legal, active, highest version valid on the request date.
4. System: reads the merge field list of that version and asks each owning module's MergeFieldProvider for the values.
5. System: checks that every required merge field has a value; formats each value by its catalog format (Thai long date in Buddhist Era, amount with two decimals, amount in Thai words).
6. System: renders each template body to PDF/A-2b with the Thai fonts embedded, and stores each file and the merge snapshot in the draft area of the standard container.
7. System: writes one decision log entry with decision code D6.4, the inputs reference (merge snapshot), and per document the template code and version.
8. System: in the same transaction writes one document row per file with source GENERATED, state DRAFT, template code, template version and treatment ID, and one DocumentStored event (EV-16) per document.
9. System: returns the generated documents; the screens of RWB-E2-017 show them for review.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required merge field has no value | Generation stops; nothing stored; the field is named | MSG-P5-009 | AC2 |
| X2 | The current template version is not approved by Legal | Generation stops; nothing stored | MSG-P5-010 | AC4 |
| X3 | The template is withdrawn | Generation stops; a task goes to the restructuring officer, as R-LIT-04 does for notices | MSG-P6-003 | AC5 |
| X4 | The treatment is not approved, is closed, or is of another type | 409; nothing stored | MSG-P5-011 | AC6 |
| X5 | The decision log write fails | Nothing stored; draft files removed; incident raised | MSG-P7-003 | AC7 |
| X6 | The same request is repeated with the same Idempotency-Key | The first result is returned; nothing new is stored | None | AC8 |
| X7 | Two requests for the same treatment and template run at once | One succeeds; the other gets 409 | MSG-GEN-004 | AC9 |
| X8 | A template body cannot be rendered | 503; nothing stored; incident raised | MSG-GEN-006 | AC10 |
| X9 | No template exists for the product group or language | Generation stops and names the template | MSG-P5-010 | AC11 |
| X10 | The case is outside the caller's scope | 404 | MSG-P4-003 | AC12 |
| X11 | One template of a set fails its check | Nothing of the set is stored | MSG-P5-010 | AC14 |
| X12 | The caller lacks Documents C | 403 | MSG-P4-002 | Access test TC-E2-026-15 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the template catalog (RWB-E1-046), template versions (RWB-E1-034) and the decision log writer (RWB-E1-027), all in Epic 1 |
| Negotiable | Templates, merge fields, formats and the type mapping are data owned by Legal and the product owner |
| Valuable | Ends re-keying of deed in lieu and restructure documents |
| Estimable | One service, one renderer, one resolver, one endpoint, no screen |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic case data |

### 7. Acceptance criteria

```gherkin
Feature: Document generation engine for contract, CA and mortgage templates

  Background:
    Given case "RW-2026-000301" with product group "MORTGAGE"
    Given treatment "TRT-0301" of type "DEED_IN_LIEU" on that case with decision_log_id set and no outcome
    Given template "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" with approved_by_legal true
    Given the merge fields of "DIL-CONTRACT" version 2 are case_no, borrower_name, title_doc_no, transfer_price and contract_date
    Given a restructuring officer with role RW-RESTRUCT in scope of the case

  Scenario: AC1 Generate
    Given the case facts give transfer_price 1250000.00, title_doc_no "12345" and contract_date 2026-12-10
    When the engine runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the system stores one document with document_type "CONTRACT", source "GENERATED", state "DRAFT" and write_once false
    Then the document carries template_code "DIL-CONTRACT", template_version 2 and treatment_id "TRT-0301"
    Then the PDF shows "1,250,000.00 บาท (หนึ่งล้านสองแสนห้าหมื่นบาทถ้วน)" and "10 ธันวาคม 2569"
    Then the system writes one decision log entry with decision code "D6.4" and an inputs reference to the merge snapshot
    Then one DocumentStored event is in the outbox

  Scenario: AC2 Missing field
    Given the case has no title_doc_no
    When the engine runs for template "DIL-CONTRACT"
    Then the response is 422 with MSG-P5-009 naming "DIL-CONTRACT" and "title_doc_no"
    Then no document, no file and no decision log entry is stored

  Scenario: AC3 Version
    Given template "DIL-CONTRACT" version 3 is approved by Legal and valid from 2026-12-15
    Given document "DOC-0310" was generated on 2026-12-10 from version 2
    When the engine runs on 2026-12-15
    Then the new document carries template_version 3
    Then "DOC-0310" still carries template_version 2 and its file opens
    Then template version 2 stays readable in the template catalog

  Scenario: AC4 A version not approved by Legal is refused
    Given template "DIL-CA" has only version 1 with approved_by_legal false
    When the engine runs for template "DIL-CA"
    Then the response is 422 with MSG-P5-010 naming "DIL-CA" version 1
    Then the system stores nothing

  Scenario: AC5 A withdrawn template holds generation
    Given template "DIL-MORTGAGE" version 1 is withdrawn and no later version is approved
    When the engine runs for template "DIL-MORTGAGE"
    Then the response is 422 with MSG-P6-003 naming "DIL-MORTGAGE"
    Then the system raises a task to the restructuring officer who requested it

  Scenario: AC6 A treatment that is not approved is refused
    Given treatment "TRT-0302" of type "DEED_IN_LIEU" with no decision_log_id
    When the engine runs for treatment "TRT-0302"
    Then the response is 409 with MSG-P5-011
    Then the system stores nothing

  Scenario: AC7 The decision log write fails
    Given the decision log store does not accept writes
    When the engine runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the response is 503 with MSG-P7-003
    Then no document row exists for "TRT-0301" and the draft file is removed from the container
    Then the system raises an incident as in R-UNI-39

  Scenario: AC8 A repeated request
    Given a request with Idempotency-Key "K-0301" generated document "DOC-0311"
    When the same request with Idempotency-Key "K-0301" arrives again
    Then the response is 201 with document "DOC-0311"
    Then no second document or decision log entry is written

  Scenario: AC9 Two requests at the same time
    Given two requests for treatment "TRT-0301" and template "DIL-CONTRACT" with different keys arrive together
    When both run
    Then one returns 201 with one DRAFT document
    Then the other returns 409 with MSG-GEN-004

  Scenario: AC10 A template body that cannot be rendered
    Given the body of "DIL-CONTRACT" version 2 is a damaged file
    When the engine runs
    Then the response is 503 with MSG-GEN-006 naming "document generation"
    Then the system stores nothing and an incident is raised

  Scenario: AC11 No template for the product group
    Given template "DIL-CONTRACT" exists only for product group "MORTGAGE"
    Given case "RW-2026-000305" has product group "HIRE_PURCHASE"
    When the engine runs for that case and "DIL-CONTRACT"
    Then the response is 422 with MSG-P5-010 naming "DIL-CONTRACT" for "HIRE_PURCHASE"

  Scenario: AC12 A case outside the caller's scope
    Given case "RW-2026-000306" is in team "HP-NE" and the officer's scope is team "FCR-BKK"
    When the officer requests generation for that case
    Then the response is 404 with MSG-P4-003

  Scenario: AC13 A set of three documents in one request
    Given templates "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE" are current and approved
    When the engine runs for treatment "TRT-0301" with the three template codes
    Then the system stores three documents with types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT"
    Then one decision log entry names the three template codes and versions

  Scenario: AC14 A set is stored whole or not at all
    Given templates "DIL-CONTRACT" and "DIL-MORTGAGE" are current and approved
    Given template "DIL-CA" has no version approved by Legal
    When the engine runs for treatment "TRT-0301" with the three template codes
    Then the response is 422 with MSG-P5-010 naming "DIL-CA"
    Then the system stores none of the three documents and no decision log entry is written
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A document is generated only from the current template version: approved by Legal, active and valid on the request date; the most specific product group match wins over a template for all products | DF-REF-047, DF-REF-049, DF-REF-051; CTL-14; R-LIT-03 |
| BR2 | A withdrawn template with no approved successor holds generation and raises a task | R-LIT-04; R-LIT-06 |
| BR3 | Every required merge field must have a value; otherwise nothing is generated and the field is named | Merge field catalog (RWB-E1-046); FEAT-OCC-07 |
| BR4 | Values are formatted by the catalog format: Thai long date in Buddhist Era, amounts with two decimals and in Thai words | Merge field catalog; Principle 1 |
| BR5 | Generation is allowed only for an approved, open treatment of type DEED_IN_LIEU or RESTRUCTURE | DF-TRT-003, DF-TRT-004, DF-TRT-013; R-DIL-14; R-DIL-16 |
| BR6 | A generated document carries the template code and version, the treatment and the source GENERATED; it is a DRAFT and not write-once until it is sent (RWB-E2-017) | DF-DOC-005, DF-DOC-010; CTL-12 |
| BR7 | Generation that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR8 | A set is generated whole or not at all | Events rule "Transactions" |
| BR9 | A repeat with the same Idempotency-Key returns the first result | R-UNI-40 |
| BR10 | A new template version applies to documents generated from its valid-from date; earlier documents keep their version | R-UNI-38 |
| BR11 | A national ID number is filled from the token service at render time; the clear value exists only inside the stored PDF | DF-PTY-007; CTL-11; DL26 |

### 9. State transitions

None. This story does not change a case status. It creates documents in state DRAFT.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | Generation requested | BR1, BR3 and BR5 pass and the decision log write succeeds | document state DRAFT |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Requests generation for a treatment in scope (Documents C) |
| RW-CASEOWN, case owner | Requests generation for a treatment in scope (Documents C) |
| SY-CASEWF, case workflow module | Calls DocumentGenerator for rule-driven generation from Epic 3 (R-DIL-14, R-DIL-16) |
| SY-DECLOG, decision log writer | Writes the decision log entry |
| RW-LEGAL, legal counsel | Approves template versions (Documents CRUA; RWB-E1-034); approval is a precondition, not part of this story |
| RW-TEAMMGR, team manager | Reads generated documents (Documents R); cannot generate |

No approval level from the delegation of authority applies in this story. The treatment itself was approved at D6.4 before generation.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-004 | recovery_case | primary_customer_id | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-003 | treatment | decision_log_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-PTY-004 | party | first_name | Read |
| DF-PTY-005 | party | last_name | Read |
| DF-COL-004 | collateral | title_doc_no | Read |
| DF-REF-045 to DF-REF-051 | template | all fields | Read |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Write |
| DF-DOC-032 | document | template_id | Write |
| DF-DOC-032 | document | template_id | Write |
| DF-DOC-033 | document | treatment_id | Write |
| Standard column | document | state | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /cases/{caseId}/generated-documents** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | GenerateRequest: treatmentId (uuid, required), templateCodes (array of string, 1 to 10, required), language (TH or EN, default TH); header Idempotency-Key (required) |
| Response | 201 DocumentPage with the generated documents |
| Errors | 401 (MSG-P4-001); 403 no Documents C (MSG-P4-002); 404 case or treatment not found or out of scope (MSG-P4-003); 409 treatment not approved or open (MSG-P5-011), or a concurrent request (MSG-GEN-004); 422 missing merge value (MSG-P5-009), template not approved or not found (MSG-P5-010), template withdrawn (MSG-P6-003), empty templateCodes (MSG-GEN-001); 503 decision log write failed (MSG-P7-003) or render failed (MSG-GEN-006) |
| Authorization | Documents, right C, scope applied |
| Idempotency | Idempotency-Key header, kept 24 hours (document_hub_parameter GEN_IDEMPOTENCY_HOURS) |

**Published interface (P5)**

```java
package recovery.dochub.generation;
public interface DocumentGenerator {
    GenerationResult generate(GenerationRequest request);
}
// GenerationRequest: caseId, treatmentId, templateCodes, language, requestedBy, idempotencyKey, overrides (List<MergeOverride>, used by RWB-E2-017)
// GenerationResult: decisionLogEntryId, documents (documentId, templateCode, templateVersion, documentType)
```

**Published interfaces called**

```java
// P6, RWB-E1-046
TemplateVersion TemplateCatalog.current(String templateCode, String language, String productGroup, LocalDate asOf);
List<MergeField> TemplateCatalog.mergeFields(UUID templateId);
// P7, RWB-E1-027
UUID DecisionLogWriter.write(DecisionRecord record);
// S2
TreatmentSummary TreatmentReader.find(UUID treatmentId);
// P3, S2, P1 each implement
Map<String, Object> MergeFieldProvider.resolve(UUID caseId, UUID treatmentId, Set<String> mergeFieldCodes);
```

**Events published:** DocumentStored (EV-16) per document, payload documentId, caseId, type, source.

### 13. Solution plan

**Package.** folder `recovery/dochub/generation`, Java package `recovery.dochub.generation`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| GeneratedDocumentController | Controller | POST /cases/{caseId}/generated-documents |
| DocumentGenerator | Published interface | Generation entry point for the controller, RWB-E2-017 and SY-CASEWF |
| DocumentGenerationService | Service | Steps 2 to 8; BR1 to BR10; one transaction; removes draft files on failure |
| TemplateSelector | Service | Picks the current version by language, product group and date (BR1, BR2) |
| MergeFieldResolver | Service | Calls each MergeFieldProvider listed in its configuration; checks required fields (BR3) |
| ValueFormatter | Service | Thai dates, amounts and amounts in words (BR4) |
| TemplateRenderer | Service | Renders the template body with merge tags in the form {{merge_field_code}} to PDF/A-2b with embedded Thai fonts |
| BlobStorageAdapter | Service | From RWB-E1-024; writes draft files and the merge snapshot to the standard container (RWB-TE-012). Drafts do not go through DocumentStore.store, which would place a legal type in the write-once container at once |
| DocumentHubRepository | Repository | Writes document rows |
| IdempotencyRepository | Repository | Holds the request key and result |

**Database**

- Writes document (all fields, state DRAFT, source GENERATED) and the new columns template_code varchar(30), template_version integer, treatment_id uuid.
- Flyway migration in this story for the three columns, with index `ux_document_draft_per_template ON document (treatment_id, template_code) WHERE state = 'DRAFT' AND is_active` for AC9.
- Writes decision_log_entry only through DecisionLogWriter. Reads template only through TemplateCatalog. The uk_template constraint on template_code alone allows one row per code; AC3 needs one row per version, so the constraint must be on (template_code, template_version). This is raised with the P6 owner of RWB-E1-046.

**Configuration and reference data**

- Templates and merge field catalog (P6, RWB-E1-046), owner legal counsel (DL28).
- Template-to-document-type mapping and retention class per type in the document type table (RWB-E1-025, DL19).
- document_hub_parameter rows GEN_IDEMPOTENCY_HOURS 24, GEN_MAX_TEMPLATES 10, GEN_FONT "TH Sarabun New", loaded by the reference data administrator. Values assumed.

**Build steps**

1. Add the Flyway migration and the partial unique index; repository tests.
2. Build TemplateSelector against a stub TemplateCatalog for approved, unapproved, withdrawn, product-specific and all-product templates, and a valid-from date.
3. Build MergeFieldResolver and its list of providers; unit tests for a missing required field.
4. Build ValueFormatter with tests for Buddhist Era dates and amounts in Thai words.
5. Build TemplateRenderer with a sample Thai template; check PDF/A-2b conformance and embedded fonts.
6. Build DocumentGenerationService: order of checks, render, store drafts, write the decision log, write documents and outbox, remove drafts on any failure.
7. Build the controller with Idempotency-Key handling and the error mapping in section 12.
8. Add the contract test for the new endpoint (RWB-TE-003).

**Feature flag:** `rwb.dochub.generation-engine`. Off: the endpoint returns 404 and DocumentGenerator refuses calls.

**Done when:** the tests in section 16 pass; a sample deed in lieu set is checked by legal counsel against the approved wording.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-009 | A required merge field has no value (new) | {template} cannot be generated. {field} has no value on the case. |
| MSG-P5-010 | No current template version approved by Legal (new) | {template} has no version approved by Legal for {product} in {language}. |
| MSG-P5-011 | The treatment is not approved or not open (new) | Documents can be generated only for an approved {treatment} that is still open. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | templateCodes is empty | Enter {field}. |
| MSG-GEN-004 | A concurrent request for the same treatment and template | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The renderer fails | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Caller lacks Documents C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. The restructuring officer reaches the engine through the screens of RWB-E2-017. Generated documents appear on SCR-30 Case documents in the list state with state DRAFT.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-026-01 | AC1, BR1, BR4, BR6 | System | Synthetic mortgage case and DIL treatment, template DIL-CONTRACT v2 |
| TC-E2-026-02 | AC2, BR3 | System | Case with no title deed number |
| TC-E2-026-03 | AC3, BR10 | System | Template v3 valid from 2026-12-15 |
| TC-E2-026-04 | AC4, BR1 | System | DIL-CA v1 not approved |
| TC-E2-026-05 | AC5, BR2 | System | DIL-MORTGAGE withdrawn |
| TC-E2-026-06 | AC6, BR5 | System | Treatment with no decision_log_id |
| TC-E2-026-07 | AC7, BR7 | System | Decision log stub refusing writes |
| TC-E2-026-08 | AC8, BR9 | System | Same Idempotency-Key twice |
| TC-E2-026-09 | AC9 | System | Two parallel requests |
| TC-E2-026-10 | AC10 | System | Damaged template body |
| TC-E2-026-11 | AC11, BR1 | System | Hire purchase case, mortgage-only template |
| TC-E2-026-12 | AC12 | System | Case of team HP-NE, officer of team FCR-BKK |
| TC-E2-026-13 | AC13 | System | Three current templates |
| TC-E2-026-14 | AC14, BR8 | System | Three templates, DIL-CA not approved |
| TC-E2-026-15 | Access | Access | RW-TEAMMGR user (Documents R) calls POST generated-documents; refused with MSG-P4-002 |
| TC-E2-026-16 | Principle 5 | Resilience | Decision log write forced to fail during a three-document set; no document, no file, MSG-P7-003, incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: template codes, merge fields, formats, type mapping and fonts are data and parameters.
- No personal data in logs, tests or prompts: merge values and the snapshot are never logged; tests use synthetic parties; the clear ID number is used only at render time.
- No read of another module's tables: templates, treatments, case facts, parties and collateral come through published interfaces.
- No document is produced from a template version without approved_by_legal = true.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-UNI-39, R-UNI-40 | TC-E2-026-01, TC-E2-026-02, TC-E2-026-06 to TC-E2-026-16 |
| REQ-OCC-002 | Letter templates versioned, with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06, R-UNI-38 | TC-E2-026-03 to TC-E2-026-05, TC-E2-026-11 |

### 19. Out of scope

- The generation, review and send screens (RWB-E2-017).
- The e-signature flow (RWB-E2-018).
- Rule-driven generation when the deed in lieu route reaches TRANSFER_PRICE_SET (FEAT-TRT-18, Epic 3).
- Template upload and Legal approval (RWB-E1-034) and the merge field catalog (RWB-E1-046).
- Debt sale agreements and notices (FEAT-DBS-10, Epic 6).


---

## RWB-E2-027 Payment matching rules with the data team

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

### 1. Story

As a **Credit Administration officer (RW-CREDITAD)**, I want **the matching rules for amount, date window and partial payments held as versioned data and run by the matching engine, with the exception list for what does not match**, so that **most payments match without a person and the rest are listed**.

### 2. Business rationale

The exact rule of RWB-E2-008 leaves short and late installments on the exception list, and a person matches them by hand each morning. This story adds the PARTIAL and WINDOW rules as rows in payment_match_rule, applies them in priority order, records each match in the decision log with the rule version, and lets Credit Administration change a window or tolerance through a reference load with no code release. It serves REQ-CHO-009, control CTL-41 and the FSD P8 measure "receipts matched the same day".

### 3. Preconditions

- RWB-E2-008 is done: JOB-07, the proceeds table, payment_match_rule with the EXACT row and the exception list are live.
- RWB-E1-027 is done: the decision log writer accepts D5 entries.
- TreatmentApi records an installment shortfall (RWB-E2-004).
- Parameter version "PM-2026.12" is in force with rows EXACT, WINDOW and PARTIAL, loaded by the reference data administrator and approved by Credit Administration.
- The reader holds RW-CREDITAD or another role with Write-off and posting R.

### 4. Flow

1. Reference data administrator: loads a parameter version through POST /admin/reference-loads with table "payment_match_rule" and a valid from date.
2. System: checks each row: match type in the list, tolerance between 0 and 100, window days 0 or more, unique priority within the version, approver present; any failure refuses the whole load.
3. JOB-07: for the business date, reads the parameter version in force on that date.
4. System: for each payment, tries the rows in priority order (EXACT, then WINDOW, then PARTIAL) against each running plan on the case; the first row that matches decides.
5. System: writes the D5 decision log entry with rule R-RES-26, rule version equal to the parameter version, the row code and the inputs; then writes the proceeds row and calls TreatmentApi.
6. System: for a PARTIAL match, passes the shortfall to TreatmentApi, which holds it on the plan.
7. System: a payment no row matches is written UNMATCHED with a D5 entry under R-UNI-03 and appears on the exception list.
8. Credit Administration officer: reads matched and unmatched receipts on SCR-28, with the row that matched each one.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A partial payment below the partial floor | Unmatched; exception list | MSG-P8-001 | AC5 |
| X2 | A late payment one day past the window | Unmatched; exception list | MSG-P8-001 | AC4 |
| X3 | A parameter load with two rows of the same priority or a tolerance above 100 | Load refused in full | MSG-GEN-002 | AC6 |
| X4 | The decision log write fails for a match | The payment is not written; it is matched in the next run; incident | MSG-P7-003 | AC7 |
| X5 | A payment above the installment by more than the tolerance | Unmatched; exception list | MSG-P8-001 | AC8 |
| X6 | Two rows would match | The row with the lowest priority number decides | None | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Extends the matcher of RWB-E2-008 only |
| Negotiable | Every threshold is a row value; the story fixes the order and the logging |
| Valuable | Short and late installments match without a person |
| Estimable | Two new match types, a load check and the decision log write |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against a synthetic ALS load and parameter file |

### 7. Acceptance criteria

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

### 8. Business rules

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

### 9. State transitions

None. This story does not change a case status. P3 changes the plan route state on the results:

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | PLAN_RUNNING (R-RES-26) |
| PLAN_CURE_PERIOD | PAYMENT_RECEIVED_LATE | payment received inside the cure period | PLAN_RUNNING (R-RES-28) |

The reference load moves from loaded to refused or in force.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, Credit Administration officer | Reads matches and the exception list (Write-off and posting CRUA); approves a parameter version as list owner |
| RW-REFADM, reference data administrator | Loads parameter versions (Reference data C) |
| RW-FINANCE, Finance and CFO delegate | Reads matches (Write-off and posting RA) |
| SY-DATALOAD, data load from COLLINS | Runs JOB-07 |
| SY-DECLOG, decision log writer | Writes the D5 entries |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent |

Separation of duty: the reference data administrator who loads a version does not approve it (roles.txt).

### 11. Data

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

### 12. Contract

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

### 13. Solution plan

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

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-GEN-002 | A parameter value outside its range, or a duplicate priority | {field} must be between {min} and {max}. |
| MSG-GEN-001 | A required parameter value is empty | Enter {field}. |
| MSG-P1-002 | A repeated parameter load | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

### 15. Screens and states

SCR-28 Proceeds matching (states Loading; matched; unmatched) shows, for each matched receipt, the row code and rule version from its decision log entry, and for each unmatched receipt the reason. Parameter versions show on SCR-40 Reference data (states Versions; load) when it is built; until then the load result is on the reference load record.

### 16. Test cases

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

### 17. Guardrails

- No business value in code: priorities, tolerances, windows and floors are rows in payment_match_rule.
- No personal data in logs, tests or prompts. Decision log inputs hold payment code, amount, dates and row code only.
- No read of another module's tables. Payments, accounts and plans come through P1 and P3 interfaces.
- The decision log entry is written before the proceeds row; no match exists without its entry.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-RES-28, R-UNI-03, R-UNI-38, R-UNI-39 | TC-E2-027-01 to TC-E2-027-11 |

### 19. Out of scope

- Settlement payment matching and partial settlement installments (FEAT-PAY-03, Epic 4).
- Manual matching from SCR-28 (POST /proceeds/{proceedsId}/match, Epic 4).
- The reconciliation agent that works the exception list (Epic 4).
- Applying proceeds to the case balance in policy order (FEAT-PAY-10, Epic 4).


---

## RWB-E2-031 Agent monitoring dashboard v2 [E3d]

| Item | Value |
|---|---|
| Story key | RWB-E2-031 |
| Epic | E2, release 31 December 2026 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-06 Publish the agent monitoring dashboard |
| Requirement IDs | REQ-DRI-009, REQ-APD-005 |
| BRD section | Business Requirements Epic 2, section 3.10; Business Requirements Program, section 5.7 |
| L3 process | 15 Manage performance, data and AI |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-063, RWB-E2-005 |
| Status | Ready for build |

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the agent monitor screen to show acceptance, override, fallback, latency and cost per agent, version and segment, with a drift alert when acceptance falls**, so that **every agent at L1 is watched daily and a fall in acceptance is acted on within a day**.

### 2. Business rationale

At L1 a case owner reads the agent's output and accepts, corrects or rejects it. A fall in acceptance on one segment is the first sign that a prompt, a model version or the data has changed. This story puts acceptance, override, fallback, latency and cost per agent, version and segment on the agent monitor screen SCR-46, reconciles tokens and cost to the per-call figures the endpoint returns, reports override reasons (REQ-APD-005) and checks drift daily from the same copied figures used for reporting (REQ-DRI-009).

### 3. Preconditions

- RWB-E1-063 is done: agent_run_daily is written by JOB-15 and agent_alert exists.
- RWB-E2-005 is done: the P7 decision log query interface returns entries by agent version and date.
- Agent runs carry the segment (product group and region) of their case.
- Feedback on L1 output is recorded in agent_feedback (verdict ACCEPTED, CORRECTED or REJECTED) by RWB-E2-028; until then acceptance shows "no L1 runs".
- Each L1 policy holds watch_measures with drift_points 10 (assumed) and minimum feedback 20 per week per segment (assumed).
- The user holds Platform administration R.

### 4. Flow

1. RW-COE: opens SCR-46 Agent monitor from the Administration menu.
2. System: checks Platform administration R, then calls GET /admin/agent-metrics for the last 30 days.
3. System: returns one row per agent, policy version, prompt version, model version, segment and day: runs, fallback rate, acceptance rate, correction rate, override rate, median and 95th percentile latency, tokens and cost.
4. RW-COE: filters by agent, segment and date range; the screen shows the state of each agent: Shadow, live (L1) or paused (mode OFF).
5. JOB-15 Reporting extract: after the daily rows, runs the drift check for each L1 agent and segment: acceptance of the last 7 days against the 7 days before.
6. System: on a fall of 10 points or more, writes one DRIFT alert and sends MSG-P10-006 to the policy alert role and RW-RISK.
7. RW-COE: opens the override reasons for an agent and month and sees the count per coded reason.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Fewer than 20 feedback entries in either week for a segment | No drift check for that segment; the screen shows "not enough feedback" | None to a user | AC4 |
| X2 | Filter "from" after "to" | Refused with 422 | MSG-GEN-003 | AC5 |
| X3 | Filter range longer than 92 days | Refused with 422 | MSG-GEN-002 | AC6 |
| X4 | Drift check runs again for the same date | No second alert (unique key) | None to a user | AC7 |
| X5 | Token sum in agent_run_daily does not match the sum of agent_run for a month | The month shows "not reconciled" with the difference | None to a user | AC3 |
| X6 | A role without Platform administration R opens SCR-46 | Refused with 403 | MSG-P4-002 | TC-E2-031-08 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the daily rows of RWB-E1-063 and the decision log query of RWB-E2-005 |
| Negotiable | Drift points, minimum feedback and window are policy values |
| Valuable | Turns acceptance and override into a daily alert for each L1 agent and segment |
| Estimable | One endpoint, one screen, one daily check, one reconciliation query |
| Small | One back end and one front end developer for one week |
| Testable | Each criterion uses fixed runs, feedback and decisions over two weeks |

### 7. Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v2 [E3d]

  Background:
    Given agents "INTAKE" (policy "P2", mode "L1") and "SCREENING" (policy "P2", mode "L1" for segment MORTGAGE and BKK) are live
    Given the drift rule is a fall of 10 points or more with at least 20 feedback entries in each week

  Scenario: AC1 Per agent
    Given two agents at L1
    When the dashboard loads for 2026-12-01 to 2026-12-14
    Then acceptance, override, fallback, latency and cost show per agent, version and segment
    Then "INTAKE" for segment MORTGAGE and BKK shows 140 feedback entries with 119 accepted, acceptance rate 0.8500
    Then "SCREENING" shows state "live" for MORTGAGE and BKK and "Shadow" for every other segment

  Scenario: AC2 Drift
    Given "INTAKE" acceptance for MORTGAGE and BKK is 0.8600 for 2026-12-01 to 2026-12-07 and 0.7500 for 2026-12-08 to 2026-12-14
    When the check runs after JOB-15 for 2026-12-14
    Then one alert of type "DRIFT" for "INTAKE", segment "MORTGAGE/BKK" and date 2026-12-14 holds measured 0.7500 and threshold 0.7600
    Then MSG-P10-006 goes to the holders of RW-COE and RW-RISK

  Scenario: AC3 Cost
    Given a month of calls in November 2026 for "INTAKE": 3,100 runs with 2,945,000 input tokens and 465,000 output tokens
    When the dashboard loads for November 2026
    Then tokens and cost per agent match the sum of the agent runs, which hold the token counts the endpoint returned on each call
    Then "INTAKE" shows 3,410,000 tokens and cost 170.5000 baht at 0.0500 baht per 1,000 tokens
    Then a month where the daily rows and the runs differ shows "not reconciled" with the token difference

  Scenario: AC4 Not enough feedback
    Given "SCREENING" for MORTGAGE and BKK has 12 feedback entries in the week to 2026-12-14
    When the check runs
    Then the system raises no drift alert for that segment and the screen shows "not enough feedback"

  Scenario: AC5 Dates in the wrong order
    When RW-COE filters from 2026-12-14 to 2026-12-01
    Then the system refuses the request with 422 and MSG-GEN-003

  Scenario: AC6 A range that is too long
    When RW-COE filters from 2026-08-01 to 2026-12-14
    Then the system refuses the request with 422 and MSG-GEN-002 naming 1 and 92 days

  Scenario: AC7 The check runs twice
    Given the DRIFT alert for "INTAKE", "MORTGAGE/BKK" and 2026-12-14 exists
    When JOB-15 is rerun for 2026-12-14
    Then no second alert row or notification exists
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Acceptance rate = accepted / (accepted + corrected + rejected) of L1 feedback; correction rate = corrected / the same total | agent_feedback.verdict (New) |
| BR2 | Override rate = decisions with the agent version where final_call differs from the recommendation / decisions with the agent version; reasons counted from override_reason codes | REQ-APD-005; decision_log_entry.override_reason; CTL-07 |
| BR3 | Drift = acceptance of the last 7 days at least 10 points below the 7 days before, with at least 20 feedback entries in each week (assumed values in watch_measures) | agent_policy.watch_measures (New) |
| BR4 | Token and cost totals come from agent_run; a month is reconciled when the daily rows equal the run sums | REQ-DRI-009; DL25 |
| BR5 | One alert per agent, type, segment and business date | agent_alert unique key (New) |
| BR6 | A segment is the case product group and region at run time | recovery_case.product_group, recovery_case.region_code |

### 9. State transitions

None. This story does not change a case status. It writes agent alerts of type DRIFT and shows each agent's mode as Shadow, live or paused.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Open SCR-46 and call GET /admin/agent-metrics (Platform administration R) |
| RW-RISK | Receives drift alerts; reads the Power BI copy (Reporting R); does not hold Platform administration |
| SY-AGENT | None in this story |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-007 | decision_log_entry | agent_version | Read (through the P7 query interface) |
| DF-DEC-009 | decision_log_entry | recommendation | Read |
| DF-DEC-012 | decision_log_entry | final_call | Read |
| DF-DEC-013 | decision_log_entry | override_reason | Read |
| DF-DEC-016 | decision_log_entry | decided_at | Read |
| DF-AGT-037 | agent_run | agent_code | Read |
| DF-AGT-038 | agent_run | agent_version | Read |
| DF-AGT-040 | agent_run | model_version | Read |
| DF-AGT-043 | agent_run | autonomy_mode | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-047 | agent_run | fallback | Read |
| DF-AGT-051 | agent_run | latency_ms | Read |
| DF-AGT-052 | agent_run | tokens_in | Read |
| DF-AGT-053 | agent_run | tokens_out | Read |
| DF-AGT-054 | agent_run | cost_thb | Read |
| DF-AGT-056 | agent_run | run_at | Read |
| DF-AGT-098 | agent_feedback | agent_run_id | Read |
| DF-AGT-100 | agent_feedback | verdict | Read |
| Standard column | agent_feedback | created_at | Read |
| DF-AGT-059 | agent_run | segment_product_group | Write (set at run time by the orchestrator) |
| DF-AGT-060 | agent_run | segment_region_code | Write (set at run time by the orchestrator) |
| DF-AGT-008 | agent_policy | autonomy_mode | Read |
| DF-AGT-009 | agent_policy | segment_product_group | Read |
| DF-AGT-010 | agent_policy | segment_region_code | Read |
| DF-AGT-019 | agent_policy | watch_measures | Read |
| DF-AGT-015 | agent_policy | alert_role | Read |
| DF-AGT-103 | agent_alert | id | Write |
| DF-AGT-104 | agent_alert | agent_code | Write |
| DF-AGT-105 | agent_alert | alert_type | Write |
| DF-AGT-106 | agent_alert | segment | Write |
| DF-AGT-107 | agent_alert | business_date | Write |
| DF-AGT-108 | agent_alert | measured_value | Write |
| DF-AGT-109 | agent_alert | threshold_value | Write |
| DF-AGT-110 | agent_alert | sent_to_role | Write |
| DF-AGT-111 | agent_alert | sent_at | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/admin/agent-metrics** (new, see additions)
- Request: query agent, segment (for example "MORTGAGE/BKK"), from, to (dates), version.
- Response: 200, array of AgentMetric (agent, policyVersion, promptVersion, modelVersion, segment, mode, date, runs, fallbackRate, acceptanceRate, correctionRate, overrideRate, feedbackCount, latencyP50Ms, latencyP95Ms, tokens, costThb, reconciled).
- Errors: 401; 403 (MSG-P4-002); 422 from after to (MSG-GEN-003) or range over 92 days (MSG-GEN-002); 503.
- Authorization: Platform administration, R, scope applied.
- Idempotency: read only.

**GET /api/recovery/v1/admin/agent-runs** (api.yaml): drill-down to runs from a metric row; Platform administration R.

**Job:** JOB-15 Reporting extract, nightly 01:30; this story adds step "agentDrift" after "agentRunDaily". Input: agent_feedback rows of the last 14 days per L1 agent and segment. Output: agent_alert rows type DRIFT and MSG-P10-006 through the P6 notification interface. Idempotency key: agent_code, alert_type, segment, business_date. Restart: the step reruns for the date with no new alert where one exists.

**Interface called:** P7 DecisionLogQuery.byAgentVersion(agentVersion, from, to), from RWB-E2-005.

### 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/monitor/`; front end `src/modules/recovery/agent/monitor/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentMetricsController | Controller | GET /admin/agent-metrics with filter checks |
| AgentMetricsService | Service | Builds metric rows from agent_run_daily, agent_feedback and the P7 override counts |
| DriftCheckStep | Job | Step in JOB-15 applying BR3 per L1 agent and segment |
| CostReconciliationQuery | Repository | Compares daily rows with run sums per month |
| AgentMonitorPage | React component | SCR-46 with agent, segment and date filters, state badges Shadow, live and paused |
| OverrideReasonPanel | React component | Count of override reasons per agent and month |

**Database:** migration `V10_007__agent_run_segment.sql` adds segment_product_group varchar(15) and segment_region_code varchar(10) to agent_run, with index (agent_code, segment_product_group, segment_region_code, run_at). Reads agent_run, agent_policy, agent_alert.

**Configuration and reference data:** watch_measures in each L1 policy (drift_points 10, min_feedback 20, window_days 7), loaded by RW-COE and approved by RW-RISK.

**Build steps**
1. Add the segment columns and set them in AgentRuntimeService from the case read (BR6).
2. Build AgentMetricsService and its rates on a two-week fixture (AC1).
3. Build AgentMetricsController with the filter checks (AC5, AC6).
4. Build CostReconciliationQuery (AC3).
5. Build DriftCheckStep with the minimum feedback rule and the unique alert key (AC2, AC4, AC7).
6. Build AgentMonitorPage and OverrideReasonPanel with Radix components and the common states.

**Feature flag:** `rwb.agent.monitor-v2`. Off: SCR-46 shows runs and fallbacks only, and the drift step is skipped.

**Done when:** the tests in section 16 pass and SCR-46 shows the fixture figures.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-006 | Acceptance falls by 10 points or more | {agent} acceptance for {segment} fell from {from} to {to} percent in the week to {date}. |
| MSG-GEN-003 | Filter dates in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-002 | Filter range above 92 days | {field} must be between {min} and {max}. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-46 Agent monitor, from the Administration menu. States per agent and segment: Shadow (mode SHADOW: runs, fallbacks and evaluation scores, no acceptance), live (mode L1: all measures), paused (mode OFF: history only). Common states: loading (skeleton rows), empty ("No agent runs in this period."), error (message at the top). The user filters by agent, segment and dates, opens a row to see the runs through GET /admin/agent-runs, and opens the override reasons.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-031-01 | AC1, BR1, BR2, BR6 | System | INTAKE MORTGAGE/BKK 140 feedback, 119 accepted |
| TC-E2-031-02 | AC2, BR3 | System | Acceptance 0.8600 then 0.7500 |
| TC-E2-031-03 | AC3, BR4 | System | November 2026: 3,100 runs, 2,945,000 and 465,000 tokens |
| TC-E2-031-04 | AC4, BR3 | System | 12 feedback entries in the week |
| TC-E2-031-05 | AC5 | System | From 2026-12-14 to 2026-12-01 |
| TC-E2-031-06 | AC6 | System | From 2026-08-01 to 2026-12-14 |
| TC-E2-031-07 | AC7, BR5 | System | JOB-15 rerun for 2026-12-14 |
| TC-E2-031-08 | Access | Access | RW-CASEOWN opens SCR-46; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: drift points, minimum feedback and window are policy values.
- No personal data in logs, tests or the screen; metrics hold counts, rates, times and amounts.
- No read of another module's tables; override figures come through the P7 query interface.
- The screen shows no prompt text and no agent output content.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-009 | Copied daily for reporting, with row counts matched | Business Requirements Program, section 5.7 | FEAT-AGT-06 | 15 Manage performance, data and AI | R-UNI-40 | TC-E2-031-01, TC-E2-031-02, TC-E2-031-03, TC-E2-031-04, TC-E2-031-05, TC-E2-031-06, TC-E2-031-07, TC-E2-031-08 |
| REQ-APD-005 | An override needs a coded reason, reported monthly | Business Requirements Program, section 5.7 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-01 |

### 19. Out of scope

- Drift detection that raises a decision with an owner and a date (FEAT-AGT-13, Epic 3).
- Changing an autonomy level from SCR-46 (FEAT-AGT-12, Epic 3; FEAT-AGT-15, Epic 8).
- Agent risk review at the committee (FEAT-AGT-16, Epic 8).


---

## RWB-E2-032 TDR offer-suggestion model through the model gateway [E3e]

| Item | Value |
|---|---|
| Story key | RWB-E2-032 |
| Epic | E2, release 31 December 2026 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-10 Expose the TDR offer-suggestion model through the gateway |
| Requirement IDs | REQ-CHO-006, REQ-DRI-001 |
| BRD section | Business Requirements Epic 2, section 3.10; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D5 |
| Priority | Could |
| Depends on | RWB-E1-058, RWB-E2-004, RWB-E1-027 |
| Status | Ready for build |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the TDR team's offer-suggestion model called through the model gateway so the treatment record carries its suggestion when the model exists**, so that **one gateway serves every model the Workbench uses and every suggestion is recorded with its model version**.

### 2. Business rationale

The restructuring officer builds each restructure offer by hand from the balance, the arrears and the payment history. If the TDR team's offer-suggestion model is in service, its suggestion appears on the treatment record and is recorded with the model version (REQ-DRI-001), so the treatment record holds what was suggested next to what was offered (REQ-CHO-006). If the model is not in service, the gateway returns no suggestion and the officer works as today. The officer decides the offer in every case.

### 3. Preconditions

- RWB-E1-058 is done: ModelGatewayClient, agent_policy and agent_run exist.
- RWB-E2-004 is done: the treatment record exists and the P3 treatment service calls P10 when a restructure treatment is opened.
- RWB-E1-027 is done: the P7 DecisionLogWriter is available.
- A policy row "TDR_OFFER" exists. Until the TDR team deploys the model, it has mode OFF and review date 2027-02-28 (assumed; DL33). When deployed, a new version with mode L1, the model code and version, the output schema "tdr-offer-v1" and timeout 60 seconds is loaded by RW-COE and approved by RW-RISK.

### 4. Flow

1. Restructuring officer: opens a restructure treatment on case "RW-2026-001001" on SCR-14 Treatment record.
2. P3 treatment service: calls ModelSuggestionClient.suggestOffer with the case ID and treatment ID.
3. System: reads the TDR_OFFER policy in force; if the mode is OFF, returns no suggestion and makes no call.
4. System: reads the account balance, arrears and the last 12 months of payments through the P3 interface and masks personal fields.
5. System: calls the model through ModelGatewayClient with the policy timeout, and checks the answer against "tdr-offer-v1".
6. System: writes one decision log entry (decision D5, model version, suggestion, final call SUGGESTION_RECORDED) and one agent run row.
7. System: returns the suggestion and the decision log entry ID to the treatment service.
8. Restructuring officer: sees the suggestion on SCR-14 with the model code and version, and builds the offer.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The model is not in service (mode OFF) | No call, no decision log entry; the treatment shows the message | MSG-P10-007 | AC2 |
| X2 | The model does not answer within 60 seconds | Run TIMED_OUT; no suggestion; no decision log entry; treatment continues (R-UNI-32) | MSG-P10-007 | AC4 |
| X3 | The answer fails the output schema | Run GUARDRAIL_FAILED; no suggestion | MSG-P10-007 | AC5 |
| X4 | The decision log write fails | No suggestion returned; run kept without a decision link; incident raised (R-UNI-39) | MSG-P7-003 | AC6 |
| X5 | The same treatment asks again | The first suggestion is returned; no second call (R-UNI-40) | None to a user | AC7 |
| X6 | The treatment type is not RESTRUCTURE | No call; no suggestion | None to a user | AC8 |
| X7 | A role without the right reads the agent runs | Refused with 403 | MSG-P4-002 | TC-E2-032-09 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the gateway (RWB-E1-058) and is called by the treatment service (RWB-E2-004); it ships with mode OFF if the model is not built |
| Negotiable | The model, its version, the inputs and the review date are policy values |
| Valuable | Puts a recorded suggestion on the treatment record without a second integration path |
| Estimable | One interface, one schema, one decision log mapping |
| Small | Under one week |
| Testable | Each criterion runs against a stub of the TDR model |

### 7. Acceptance criteria

```gherkin
Feature: TDR offer-suggestion model through the model gateway [E3e]

  Background:
    Given restructure treatment "T-1001" is open on case "RW-2026-001001"
    Given the account has principal outstanding 1,250,000.00 baht and 120 days past due

  Scenario: AC1 Exposed
    Given the model deployed by the TDR team with policy "TDR_OFFER" version "P2", mode "L1" and model version "TDR-OFFER-1.0"
    When the gateway calls it
    Then the suggestion returns with 84 installments of 18,900.00 baht and model version "TDR-OFFER-1.0"
    Then one agent run row and one decision log entry with decision "D5", model version "TDR-OFFER-1.0" and final call "SUGGESTION_RECORDED" are written

  Scenario: AC2 Not available
    Given the model not yet built and policy "TDR_OFFER" version "P1" with mode "OFF" and review date 2027-02-28
    When the treatment service asks for a suggestion
    Then the gateway stub returns no suggestion and makes no model call
    Then SCR-14 shows MSG-P10-007 and no decision log entry is written
    Then GET /admin/agent-configs shows version "P1" with review date 2027-02-28

  Scenario: AC3 Logged
    Given a suggestion on treatment "T-1001"
    When the record is read
    Then the decision log entry linked to the suggestion holds model version "TDR-OFFER-1.0", the inputs reference and the suggested terms
    Then SCR-14 shows "Suggested by TDR_OFFER, version TDR-OFFER-1.0"

  Scenario: AC4 The model does not answer
    Given the TDR model stub does not answer for 61 seconds
    When the treatment service asks for a suggestion
    Then the agent run holds status "TIMED_OUT" and fallback true
    Then no suggestion and no decision log entry exist and SCR-14 shows MSG-P10-007

  Scenario: AC5 An answer that fails the schema
    Given the model returns installments -12
    When the guardrail runs
    Then the agent run holds status "GUARDRAIL_FAILED" with check "SCHEMA" and no suggestion is returned

  Scenario: AC6 The decision cannot be recorded
    Given the decision log writer fails
    When the model answers
    Then the system returns no suggestion and the treatment service receives DecisionNotRecordedException with MSG-P7-003
    Then the agent run has no decision log entry ID

  Scenario: AC7 The same treatment asks twice
    Given a suggestion was recorded for treatment "T-1001"
    When the treatment service asks again for "T-1001"
    Then the first suggestion and its decision log entry ID return and no second model call is made

  Scenario: AC8 Not a restructure
    Given treatment "T-1002" has type "SETTLEMENT"
    When the treatment service asks for a suggestion
    Then the system makes no model call and no suggestion returns
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The TDR model is reached only through ModelGatewayClient on the private endpoint | DL33; integration INT-23 |
| BR2 | Mode OFF returns no suggestion and makes no call; the review date is held on the policy row | agent_policy.autonomy_mode, review_date (New) |
| BR3 | A suggestion is returned only after its decision log entry is written | Principle 5; R-UNI-39; CTL-06 |
| BR4 | A timeout or a failed check gives no suggestion and the treatment continues | R-UNI-32 |
| BR5 | One suggestion per treatment; the key is "TDR_OFFER:<treatmentId>" | R-UNI-40 |
| BR6 | The model is called only for treatment type RESTRUCTURE | treatment.treatment_type |
| BR7 | The suggestion is advice; the officer builds and submits the offer | Agent catalog, settlement and restructure agent; R-RES-09, R-RES-10 |

### 9. State transitions

None. This story does not change a case status or a treatment status. It writes an agent run and, when a suggestion is returned, one decision log entry.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT | Reads the suggestion on SCR-14 (Treatment and offer R) |
| RW-CASEOWN | Reads the suggestion on SCR-14 (Treatment and offer R) |
| SY-CASEWF | Calls ModelSuggestionClient from the treatment service |
| SY-AGENT | Reads the account and payments (Case record R, Treatment and offer R) |
| SY-DECLOG | Writes the entry |
| RW-COE, RW-RISK | Load and approve the TDR_OFFER policy (Rules and parameters C and A) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-ACC-009 | loan_account | principal_outstanding | Read |
| DF-ACC-012 | loan_account | total_balance | Read |
| DF-ACC-014 | loan_account | days_past_due | Read |
| DF-ACC-008 | loan_account | interest_rate | Read |
| DF-ACC-025 | account_payment | payment_date | Read |
| DF-ACC-026 | account_payment | payment_amount | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (through the P7 DecisionLogWriter) |
| DF-AGT-008 | agent_policy | autonomy_mode | Read |
| DF-AGT-004 | agent_policy | model_code | Read |
| DF-AGT-005 | agent_policy | model_version | Read |
| DF-AGT-006 | agent_policy | output_schema_ref | Read |
| DF-AGT-012 | agent_policy | timeout_seconds | Read |
| DF-AGT-016 | agent_policy | review_date | Read |
| DF-AGT-036 | agent_run | id | Write |
| DF-AGT-037 | agent_run | agent_code | Write |
| DF-AGT-040 | agent_run | model_version | Write |
| DF-AGT-041 | agent_run | case_id | Write |
| DF-AGT-042 | agent_run | subject_id | Write |
| DF-AGT-043 | agent_run | autonomy_mode | Write |
| DF-AGT-045 | agent_run | idempotency_key | Write |
| DF-AGT-046 | agent_run | status | Write |
| DF-AGT-047 | agent_run | fallback | Write |
| DF-AGT-048 | agent_run | guardrail_result | Write |
| DF-AGT-049 | agent_run | output | Write |
| DF-AGT-051 | agent_run | latency_ms | Write |
| DF-AGT-056 | agent_run | run_at | Write |
| DF-AGT-058 | agent_run | decision_log_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Published interface**

```java
package recovery.agent.api;

public interface ModelSuggestionClient {
    Optional<OfferSuggestion> suggestOffer(UUID caseId, UUID treatmentId) throws DecisionNotRecordedException;
}

public record OfferSuggestion(UUID agentRunId, UUID decisionLogEntryId, String modelCode, String modelVersion,
                              int installments, BigDecimal monthlyAmountThb, BigDecimal interestRate,
                              BigDecimal confidence) {}
```

**Decision log mapping:** case_id; decision_code "D5"; model_version; agent_version null; inputs_ref = masked inputs snapshot; recommendation = the suggestion; final_call "SUGGESTION_RECORDED"; actions = {"treatmentId", "agentRunId"}.

**External call:** INT-23 through ModelGatewayClient; request: model code, masked inputs, output schema "tdr-offer-v1"; per request.

**GET /api/recovery/v1/admin/agent-runs** (api.yaml): runs of TDR_OFFER with outcome and fallback; Platform administration R.

**GET /api/recovery/v1/admin/agent-configs** (new, RWB-E1-058): shows the TDR_OFFER version, mode and review date; Rules and parameters R.

**Events:** EV-28 AgentRunCompleted published; no event consumed.

**Idempotency:** "TDR_OFFER:<treatmentId>".

### 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/tdr/`, Java package `recovery.agent.tdr`; interface in `recovery.agent.api`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ModelSuggestionClient | Published interface | Called by the P3 treatment service |
| TdrSuggestionService | Service | Mode check, inputs, gateway call, checks, decision log write, run row |
| TdrInputAssembler | Service | Account, arrears and 12 months of payments through the P3 interface, masked |
| tdr-offer-v1.json | Rule table | Output schema: installments 1 to 360, monthly amount above 0, interest rate 0 to 30, confidence |
| TreatmentSuggestionPanel | React component | On SCR-14: the suggestion with model code and version, or MSG-P10-007 |

**Database:** no new table; writes agent_run.

**Configuration and reference data:** TDR_OFFER policy P1 (mode OFF, review date 2027-02-28) loaded by RW-COE and approved by RW-RISK; P2 when the TDR team deploys the model.

**Build steps**
1. Write the output schema and the P1 policy file; load them in DEV.
2. Build TdrSuggestionService with the mode OFF path (AC2, AC8).
3. Add the gateway call, the schema check and the timeout path against a stub (AC1, AC4, AC5).
4. Add the decision log write before return and the idempotent repeat (AC3, AC6, AC7).
5. Build TreatmentSuggestionPanel for SCR-14.

**Feature flag:** `rwb.agent.tdr-suggestion`. Off: suggestOffer returns empty with no call.

**Done when:** the tests in section 16 pass with mode OFF in SIT; the AC1 test passes against the stub until the TDR model is deployed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-007 | No suggestion: model not in service, timeout or failed check | No offer suggestion is available for this treatment. The TDR model is not in service. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-14 Treatment record (states draft, submitted, approved, booked, broken) gains a suggestion area in the draft state: suggestion shown (terms, model code and version) or not available (MSG-P10-007). The officer edits the offer fields as before; the suggestion is not copied into them.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-032-01 | AC1, BR1, BR3 | System | Treatment T-1001, stub answer 84 installments of 18,900.00 baht |
| TC-E2-032-02 | AC2, BR2 | System | Policy TDR_OFFER P1 mode OFF, review date 2027-02-28 |
| TC-E2-032-03 | AC3 | System | Suggestion recorded on T-1001 |
| TC-E2-032-04 | AC4, BR4 | System | Stub silent for 61 seconds |
| TC-E2-032-05 | AC5, BR4 | System | Answer with installments -12 |
| TC-E2-032-06 | AC6, BR3 | System | Decision log writer fails |
| TC-E2-032-07 | AC7, BR5 | System | Second request for T-1001 |
| TC-E2-032-08 | AC8, BR6 | System | Treatment T-1002 of type SETTLEMENT |
| TC-E2-032-09 | Access | Access | RW-RESTRUCT calls GET /admin/agent-runs; refused with MSG-P4-002 |
| TC-E2-032-10 | Principle 5 | Resilience | Decision log write forced to fail after the model answers; no suggestion; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: model code, version, schema limits and review date are data.
- No personal data in logs, tests or the model request; account numbers are masked.
- No read of another module's tables; the account and treatment come through the P3 interface.
- The suggestion is never written into the offer fields or the treatment status.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record holds every offer's type, terms, approval and outcome | Business Requirements Program, section 5.3 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-32, R-UNI-40 | TC-E2-032-02, TC-E2-032-04, TC-E2-032-05, TC-E2-032-07, TC-E2-032-08 |
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-032-01, TC-E2-032-03, TC-E2-032-06, TC-E2-032-09, TC-E2-032-10 |

### 19. Out of scope

- Building or training the TDR model (TDR team, outside the Workbench).
- The settlement and restructure agent proposing plan terms (shadow from Epic 2 and live from Epic 3, per the agent catalog).
- Affordability and plan calculation (ACE restructure calculator, R-RES-06).


---

## RWB-E2-033 Case and queue list with status, owner and ageing

| Item | Value |
|---|---|
| Story key | RWB-E2-033 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-WKM-002, REQ-DVH-006 |
| BRD section | Business Requirements Epic 2, section 3.2 |
| L3 process | All recovery processes |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-031, RWB-E2-011 |
| Status | Ready for build |

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **every case in every queue in my scope on the case list with its identifier, product, queue, owner, status, age in state, stage and prescription clock states and service level breach flag, with a breach filter and an extract**, so that **I can see where work is waiting without asking anyone**.

### 2. Business rationale

Today a team manager learns where cases wait by asking each owner or by building a spreadsheet. RWB-E1-031 puts the queue and owner on the case list with an export, and RWB-E2-011 adds the age and the service level state for the queue screens. This story completes the case list for every queue in the manager's scope: a breach filter, the prescription clock beside the stage clock so a paused case is not read as safe, and the same columns in the extract. It meets REQ-WKM-002 (every queue in the team, filtered by status, product and ageing, with an export) and REQ-DVH-006 (the deviation flag is visible in every queue view). The business measure is the count of cases past their service level per queue, which the manager can read every morning.

### 3. Preconditions

- RWB-E1-018 (case record), RWB-E1-031 (queue and owner on the case list, GET /cases/export) and RWB-E2-011 (ageDays, serviceLevelDueAt and serviceLevelState on GET /cases) are done. RWB-E1-028 writes the SERVICE_LEVEL and PRESCRIPTION timer rows.
- The queues table (RWB-E1-019) and the service levels and timers reference table (DL22) are loaded.
- Parameter caselist.export.maxrows = 10,000 (assumed; DL11) from RWB-E1-042.
- The role to permission matrix (RWB-E1-037) gives RW-TEAMMGR the Case record right R with Team scope.
- The caller is signed in through Entra ID and holds a role with Case record R.
- Feature flag `rwb.casewf.case-list-ageing` is on.

### 4. Flow

1. Team manager: opens the case list (SCR-02).
2. Front end: calls GET /api/recovery/v1/cases with the filters chosen, including breached when set.
3. CaseAndWorkflowController: checks Case record R through the common module access check and applies the caller's scope (CTL-09).
4. CaseAndWorkflowController: validates each filter value against its list of values and the page size against 1 to 200.
5. CaseListQueryService (RWB-E2-011): reads the cases in scope with their queue, owner and SERVICE_LEVEL timer, and computes ageDays and serviceLevelState.
6. PrescriptionClockReader (this story): adds prescriptionClockStatus from the PRESCRIPTION timer and applies the breached filter (BR3, BR4).
7. CaseListQueryService: orders the rows by breach, then age in state descending, then case number, and returns one page.
8. Front end: shows the columns in section 15 and marks each breached case.
9. Team manager: chooses Extract; the front end calls GET /api/recovery/v1/cases/export with the same filters.
10. CaseExportService (RWB-E1-031): writes the matching rows with the ageing and clock columns to an Excel file, after the export is written to the access log.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A filter value is not in its list of values, for example product CAR | Request refused with 422; nothing is read | MSG-GEN-007 | AC6 |
| X2 | Page size below 1 or above 200 | Request refused with 422 | MSG-GEN-002 | AC7 |
| X3 | No case matches the filters | Empty state; the extract holds the header row only | MSG-P3-020 | AC8 |
| X4 | A queue filter names a queue outside the caller's scope | Only cases in scope are returned, so the result is empty | MSG-P3-020 | AC9 |
| X5 | A case has no SERVICE_LEVEL timer yet (status New) | serviceLevelState NONE; breached false | None | AC5 |
| X6 | The service level due time equals the current time | Not breached; breached from the next minute | None | AC4 |
| X7 | The extract would hold more than 10,000 rows | Extract refused | MSG-P3-021 | AC10 |
| X8 | A case changes between two page requests | Order is stable by case number | None | AC11 |
| X9 | The caller's role does not hold Case record R | Refused with 403; nothing is read | MSG-P4-002 | Access test TC-E2-033-12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the case list and export of RWB-E1-031 and the ageing of RWB-E2-011; no new endpoint |
| Negotiable | Columns and filters are listed; their values are data. The layout belongs to the designer (DL31) |
| Valuable | Replaces the manager's daily round of questions and spreadsheets with one list |
| Estimable | One filter, one computed field, extract columns, one list change |
| Small | No write to any business table |
| Testable | Each criterion below has one test case with fixed synthetic data |

### 7. Acceptance criteria

```gherkin
Feature: Case and queue list with status, owner and ageing

  Background:
    Given today is 10 December 2026 at 09:00 Asia/Bangkok
    Given the team manager holds role RW-TEAMMGR with Team scope for team "MTG-BKK"
    Given queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN
    Given queue "MTG-BKK-LIT" belongs to team "MTG-BKK" and role RW-LITOFF

  Scenario: AC1 Every case is visible
    Given case "RW-2026-000101", product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, stage clock start 1 December 2026, service level due 8 December 2026 17:00
    Given case "RW-2026-000102", product MORTGAGE, queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, stage clock start 8 December 2026, service level due 15 December 2026 17:00
    Given case "RW-2026-000103", product MORTGAGE, queue "MTG-BKK-CO", no owner, status NEW, entry date 10 December 2026
    When the manager opens the list
    Then 3 rows show
    Then row "RW-2026-000101" shows product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, age in state 9 days and service level state BREACHED
    Then row "RW-2026-000102" shows queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, age in state 2 days and service level state RUNNING
    Then row "RW-2026-000103" shows owner "Unassigned", status NEW, age in state 0 days and service level state NONE
    Then the rows are in the order "RW-2026-000101", "RW-2026-000102", "RW-2026-000103"

  Scenario: AC2 Ageing is correct when a clock is paused
    Given case "RW-2026-000104" with deviation X1 raised on 9 December 2026
    Given its SERVICE_LEVEL timer has paused true and status PAUSED
    Given its PRESCRIPTION timer has status RUNNING and expires 30 June 2028
    When the list is read
    Then row "RW-2026-000104" shows service level state PAUSED, prescription clock RUNNING with date 30 June 2028 and deviation open Yes
    Then the system does not count the case as breached

  Scenario: AC3 It can be filtered and extracted
    Given the 4 cases above
    When the manager filters by queue "MTG-BKK-CO", product MORTGAGE and breached Yes
    Then 1 row shows, "RW-2026-000101"
    When the manager chooses Extract with the same filters
    Then an Excel file downloads with a header row and 1 data row for "RW-2026-000101" with columns age in state, service level state, service level due, prescription date, prescription clock and deviation open
    Then the access log holds one export entry with the user, the time, the 3 filters and row count 1

  Scenario: AC4 Breach at the boundary of the service level
    Given case "RW-2026-000105" with a RUNNING SERVICE_LEVEL timer due 10 December 2026 09:00
    When the list is read at 10 December 2026 09:00
    Then row "RW-2026-000105" shows service level state RUNNING
    When the list is read at 10 December 2026 09:01
    Then row "RW-2026-000105" shows service level state BREACHED

  Scenario: AC5 A case with no service level timer
    Given case "RW-2026-000103" with status NEW and no SERVICE_LEVEL timer
    When the list is read with breached No
    Then row "RW-2026-000103" shows service level state NONE and is in the result

  Scenario: AC6 A filter value outside its list is refused
    When the manager requests the list with product "CAR"
    Then the response is 422 with message MSG-GEN-007 for field product
    Then the system reads no case

  Scenario: AC7 Page size outside its limits is refused
    When the manager requests the list with page size 500
    Then the response is 422 with message MSG-GEN-002 naming page size, minimum 1 and maximum 200

  Scenario: AC8 No case matches
    When the manager filters by product SSME
    Then the list shows the empty state with message MSG-P3-020
    When the manager chooses Extract with the same filter
    Then an Excel file downloads with the header row and no data row

  Scenario: AC9 Scope limits the list
    Given case "RW-2026-000201" in queue "HP-NE-CO" of team "HP-NE"
    When the manager of team "MTG-BKK" filters by queue "HP-NE-CO"
    Then the list shows the empty state with message MSG-P3-020
    Then case "RW-2026-000201" does not appear in any page of the unfiltered list

  Scenario: AC10 The extract limit
    Given 10,001 cases in the manager's scope match breached No
    When the manager chooses Extract with breached No
    Then the response is 422 with message MSG-P3-021 naming 10,000 rows
    Then the system produces no file

  Scenario: AC11 Order is stable across pages
    Given 120 cases in scope with no breach and the same age in state
    When the manager reads page 1 and page 2 with page size 50
    Then page 1 holds the 50 lowest case numbers and page 2 the next 50
    Then no case appears on both pages
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The list holds only cases in the caller's scope: Own, Team or All, from the role's default scope | role.default_scope; CTL-09 |
| BR2 | Age in state is the whole number of calendar days from stage_clock_start (or entry_date when it is empty) to today in Asia/Bangkok | recovery_case.stage_clock_start, entry_date; RWB-E2-011 ageDays |
| BR3 | A case is breached when its SERVICE_LEVEL timer has status EXPIRED, or has status RUNNING with expires_at earlier than now. A breach does not move the case | R-UNI-30; timer.status |
| BR4 | A deviation pauses the stage clock and keeps the prescription clock running; the list shows both; a paused SERVICE_LEVEL timer is never breached | R-DEV-01; timer.paused |
| BR5 | prescriptionClockStatus is RUNNING or EXPIRED from the PRESCRIPTION timer, and NONE when the case has no such timer | timer.timer_type; LOV-TIMER-STATUS |
| BR6 | Filter values are checked against LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE and the queue codes in force | Lists of values; queue table |
| BR7 | The extract holds at most caselist.export.maxrows rows, carries no customer personal field, and is written to the access log before the file is made | RWB-E1-031; CTL-11; REQ-ACA-006 |

### 9. State transitions

None. This story does not change a case status. It reads case, queue and timer records and, through RWB-E1-031, writes one access log entry per extract.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Reads and extracts the list for the team's queues (Case record R, Team scope) |
| RW-CASEOWN, case owner | Reads and extracts the list for the cases they own (Case record R, Own scope) |
| RW-PRODHEAD, RW-AUDIT, RW-CONDUCT and other roles with Case record R | Read and extract the list in their scope |
| RW-REFADM, reference data administrator | No Case record right; refused with MSG-P4-002 |
| No approval applies | The story takes no decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-006 | recovery_case | stage_code | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-011 | recovery_case | team_code | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-CAS-017 | recovery_case | prescription_date | Read |
| DF-CAS-018 | recovery_case | stage_clock_start | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-028 | timer | case_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-032 | timer | expires_at | Read |
| DF-WRK-034 | timer | paused | Read |
| DF-WRK-035 | timer | status | Read |
| DF-REF-038 | role | default_scope | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/cases** (operationId getCases; extended by RWB-E1-031 and RWB-E2-011; this story's change recorded in the additions file)

| Item | Value |
|---|---|
| Query parameters used | product, stage, status, owner, queue, page, size, sort; and the new parameter breached (true or false) |
| Response 200 | CasePage of Case. Each item carries ageDays, serviceLevelDueAt and serviceLevelState (BREACHED, RUNNING, PAUSED, NONE) from RWB-E2-011, and the new field prescriptionClockStatus (RUNNING, EXPIRED, NONE) |
| 401 | No valid session (MSG-P4-001) |
| 403 | Role lacks Case record R (MSG-P4-002) |
| 422 | Filter value outside its list (MSG-GEN-007) or page size outside 1 to 200 (MSG-GEN-002) |
| 503 | Database unavailable (E503) |
| Authorization | Case record, right R; scope filters every row |
| Idempotency | Read only. The same request on unchanged data returns the same rows in the same order |

**GET /api/recovery/v1/cases/export** (from RWB-E1-031; this story's change recorded in the additions file)

| Item | Value |
|---|---|
| Query parameters | The same as GET /cases, including breached, without page and size |
| Response 200 | Excel file with the RWB-E1-031 columns plus age in state, service level state, service level due, prescription date, prescription clock and deviation open |
| 422 | Above caselist.export.maxrows (MSG-P3-021) |
| 503 | Access event not recorded (MSG-P7-003) |
| Authorization | Case record, right R; scope applies |
| Idempotency | Each export writes its own access log entry |

No event is published. The access log entry is written through the RWB-E1-039 interface that RWB-E1-031 already calls.

### 13. Solution plan

**Package.** The story is in the P2 backlog. The endpoints belong to P3 in the API specification and the tables to P3, so under the boundary rule the code is in the P3 package: folder `recovery/casewf/caselist`, Java package `<ACE base package>.recovery.casewf.caselist`, extending the classes of RWB-E1-031 and RWB-E2-011. Front end folder `src/modules/recovery/caselist`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAndWorkflowController | Controller | Adds the breached parameter and the filter value check to getCases and the export |
| CaseListQueryService | Service | From RWB-E2-011; adds the breached predicate and the order of step 7 |
| PrescriptionClockReader | Service | Computes prescriptionClockStatus from the PRESCRIPTION timer (BR5) |
| AgeingCalculator | Service | Pure functions for BR2 to BR4, unit tested without a database |
| CaseExportService | Service | From RWB-E1-031; adds the ageing and clock columns |
| CaseListPage | React component | SCR-02 columns, breach filter, breach marker and empty state |

**Database.** Reads recovery_case (id, case_no, product_group, status, stage_code, owner_user_id, queue_id, team_code, entry_date, prescription_date, stage_clock_start, deviation_open), queue (queue_code, team_code) and timer (case_id, timer_type, expires_at, paused, status). Writes nothing. Index needed: `CREATE INDEX ix_timer_case_type ON timer (case_id, timer_type) WHERE status IN ('RUNNING','PAUSED','EXPIRED')`, added by a Flyway migration in the P3 migration folder. ix_case_status_queue and ix_case_owner_status serve the other filters.

**Configuration and reference data.** LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE through the P4 reference data interface; the queues table (RWB-E1-019); caselist.export.maxrows (RWB-E1-042, assumed 10,000; DL11), loaded by RW-REFADM.

**Build steps**

1. Add the breached parameter and prescriptionClockStatus to the API specification; regenerate types (RWB-TE-003).
2. Write AgeingCalculator and PrescriptionClockReader with unit tests for BR2 to BR5, including AC2 and AC4.
3. Add the breached predicate, the filter value check and the stable order to CaseListQueryService; add the index migration; test AC1, AC5, AC6, AC7, AC9 and AC11.
4. Add the ageing and clock columns to CaseExportService; test AC3, AC8 and AC10.
5. Add the columns, the breach filter and the breach marker to CaseListPage.
6. Add the contract test for the changed operations and the access test for a role without Case record R.

**Feature flag.** `rwb.casewf.case-list-ageing`. Off: the breached parameter is ignored and the list and export keep the RWB-E2-011 and RWB-E1-031 columns.

**Done when.** The tests in section 16 pass; page 1 of the list over 23,600 synthetic cases returns in under 2 seconds at the 95th percentile in SIT (NFR-008).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-007 | A filter value is not in its list (new) | {value} is not a valid value for {field}. |
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-P3-020 | No case matches the filters | No cases match these filters. Change a filter to see more. |
| MSG-P3-021 | Extract above the row limit | The export holds at most {max} rows. Narrow the filters and try again. |
| MSG-P4-001 | No valid session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The export access event cannot be recorded | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-02 Case list, states Loading, Empty, List and Filtered. The team manager sets filters for queue, product, status, stage, owner and breached; reads the columns case number, product, queue, owner, status, stage, age in state, service level state, service level due, prescription date, prescription clock and deviation; and chooses Extract. A breached row carries the text "Breached", not color alone; a paused stage clock shows "Paused". The Empty state shows MSG-P3-020.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-033-01 | AC1, BR1, BR2, BR3 | System | Three cases in team MTG-BKK as in AC1 |
| TC-E2-033-02 | AC2, BR4, BR5 | System | Case with X1 raised, paused SERVICE_LEVEL timer, running PRESCRIPTION timer |
| TC-E2-033-03 | AC3, BR7 | System | Four cases; filters queue, product and breached; extract file and access log |
| TC-E2-033-04 | AC4, BR3 | System | Timer due 10 December 2026 09:00, read at 09:00 and 09:01 |
| TC-E2-033-05 | AC5 | System | NEW case with no SERVICE_LEVEL timer |
| TC-E2-033-06 | AC6, BR6 | System | Product filter CAR |
| TC-E2-033-07 | AC7 | System | Page size 500 |
| TC-E2-033-08 | AC8 | System | Filter product SSME with no SSME case |
| TC-E2-033-09 | AC9, BR1 | System | Case in team HP-NE read by the MTG-BKK manager |
| TC-E2-033-10 | AC10, BR7 | System | 10,001 matching cases |
| TC-E2-033-11 | AC11 | System | 120 cases with equal age, pages of 50 |
| TC-E2-033-12 | Access | Access | RW-REFADM calls the list; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: page size limits, the export limit, lists and service levels are read from the parameter catalog and reference tables.
- No personal data in logs, tests or prompts; the extract carries no customer field.
- No read of another module's tables: the query reads P3 tables only; owner names come from the common module interface.
- The breach flag is computed at read time; the story never changes a timer or a case.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-002 | Team manager sees every team queue, filters by status, product and ageing, exports the view | Business Requirements Epic 2, section 3.2 | None | All recovery processes | R-UNI-30 | TC-E2-033-01, TC-E2-033-03 to TC-E2-033-12 |
| REQ-DVH-006 | Deviation flag visible in every queue view | Business Requirements Epic 2, section 3.2 | None | All recovery processes | R-DEV-01 | TC-E2-033-02 |

### 19. Out of scope

- Next action columns and the overdue mark: RWB-E2-035.
- My queue and team queue screens with counts, oldest case and cap use: RWB-E2-011.
- Escalation when a service level is breached: RWB-E1-028 and RWB-E2-015.
- Manual transfer from the list: RWB-E2-012.
- The service level values per state: DL22.


---

## RWB-E2-034 Interaction ledger on the case and from every channel

| Item | Value |
|---|---|
| Story key | RWB-E2-034 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-ILG-06 Bring contact outcomes into the ledger; FEAT-ILG-07 Bring dispatch outcomes into the ledger; FEAT-ILG-08 Record a hand-over in the ledger; FEAT-ILG-09 Read the ledger as a timeline on the case; FEAT-ILG-10 Set the retention class for ledger entries |
| Requirement IDs | REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013 |
| BRD section | Business Requirements Epic 2, section 3.2 |
| L3 process | 06 to 10 Recovery case processes; All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-027, RWB-E2-016, RWB-E1-004, RWB-E1-007, RWB-E1-066, RWB-E1-067, RWB-TE-006 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every contact, letter, delivery, offer, payment and hand-over on the case recorded in one ledger, from the Workbench, from EFS and from the partner portal**, so that **contactability is not found and then lost again**.

### 2. Business rationale

Contact outcomes from collections, letters sent through WIN and work held by partners are recorded in different systems today, so a case owner who picks up a case does not know which number answered or who held the case last. This story brings each of these into the one ledger built in Epic 1 (RWB-E1-066 and RWB-E1-067), adds who held the case before and after each hand-over, gives each entry a retention class, and shows the ledger as an ordered timeline on the case. It meets REQ-ILG-009 to REQ-ILG-013. The business measure is the share of open cases whose last right-party contact is visible on the case, which today is zero for cases that came from EFS.

### 3. Preconditions

- RWB-E1-066 (ledger store and InteractionLedgerWriter), RWB-E1-067 (Workbench events into the ledger), RWB-E1-027 (decision log writer), RWB-E2-016 (case record timeline), RWB-E1-004 (EFS extract load) and RWB-TE-006 (outbox delivery) are done.
- The EFS ledger outcome list (the action codes that enter the ledger, with their channel) is loaded. Until the business lead names the list (DL29, option B), every action code in LOV-ACTION-CODE with a call result enters the ledger with channel CALL (assumed).
- The Retention classes reference table holds a class per ledger event code. Until Compliance sets the periods (DL26), every event code takes class "ILG-STD" (assumed).
- LOV-LEDGER-EVENT (RWB-E1-066) holds the added values PARTNER_RESULT and OFFER (addition).
- The case exists and is open; the reader holds a role with Case record R.
- Feature flag `rwb.integration.ledger-channels` is on.

### 4. Flow

1. Outbox (RWB-TE-006): delivers to consumer "ledger-channels" the events InstructionIssued, PartnerResultSubmitted, NoticeDispatched, NoticeDelivered, TreatmentApproved, ProceedsMatched, and LoadCompleted for the COLLINS load.
2. LedgerChannelListener: checks the event's idempotency key through IdempotencyGuard (RWB-E1-007) and passes the event to LedgerChannelMapper.
3. LedgerChannelMapper: maps the event to one LedgerEntryCommand with event code, channel, direction, occurred time, source, holder references and links (BR1 to BR5), reading the facts it needs through the owning module's published interface.
4. EfsContactOutcomeImporter (for LoadCompleted): reads the day's EFS contact outcomes for accounts linked to open cases through the P1 EFS interface, keeps the action codes on the EFS ledger outcome list and maps each to a CONTACT entry with source EFS.
5. HolderEnricher: for CaseAllocated and CaseTransferred, which RWB-E1-067 maps to CASE_ALLOCATED and CASE_TRANSFERRED, adds the holder before and after the move to the same entry.
6. RetentionClassResolver: sets the retention class from the Retention classes reference table by event code, for every entry the writer appends.
7. LedgerChannelListener: calls InteractionLedgerWriter.append for each entry inside the delivery's transaction; the writer refuses a repeated idempotency key and counts the repeat (R-UNI-40).
8. Case owner: opens the case record (SCR-03) and the timeline (SCR-04).
9. Front end: calls GET /api/recovery/v1/cases/{caseId}/interactions with the channel, actor and date filters.
10. Front end: shows the entries in case sequence order with time, channel, contact point reached (masked by role), outcome, promise, offer or payment link, holder change and source.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same event arrives twice with the same key | One entry exists; the repeat is counted | None | AC5 |
| X2 | An EFS row has an action code that is not on the EFS ledger outcome list | No entry; counted as excluded in the import summary | None | AC6 |
| X3 | An EFS row is for an account on no open case | No entry; counted as not on a case | None | AC6 |
| X4 | The ledger store cannot be written | The delivery fails and stays in the outbox for retry; an incident is raised; no entry is lost | None | AC7 |
| X5 | An event names a case that does not exist | No entry; after the retry limit the delivery goes to the exception queue with a task for the platform administrator | None | AC8 |
| X6 | An EFS row arrives after a later Workbench entry for the same case | The entry takes its own occurred time; the timeline orders by occurred time | None | AC9 |
| X7 | The case has no entry yet | Empty state on the timeline | MSG-P3-024 | AC10 |
| X8 | The reader's role does not hold Case record R | Refused with 403 | MSG-P4-002 | Access test TC-E2-034-12 |
| X9 | The case is outside the reader's scope | Refused with 404 | MSG-P4-003 | AC11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the Epic 1 ledger writer, the outbox and the published events; no change to the modules that publish them |
| Negotiable | The EFS outcome list and the retention classes are data (DL29, DL26); the mapping rules are fixed here |
| Valuable | The case owner sees which number answered and who held the case, without asking EFS or the partner |
| Estimable | One listener, one mapper, one import step, six added columns and a timeline section |
| Small | Each event type is one mapping with one test |
| Testable | Each criterion below has one test with fixed synthetic events |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger on the case and from every channel

  Background:
    Given open case "RW-2026-000301" with account "ACC-SYN-0301" and owner "U-2001"
    Given the EFS ledger outcome list holds action code "PTP" with channel CALL
    Given the retention class for every event code is "ILG-STD"

  Scenario: AC1 An interaction is recorded
    Given the COLLINS load for business date 14 December 2026 holds an EFS row for account "ACC-SYN-0301" with action code "PTP", call result RIGHT_PARTY, contact time 14 December 2026 10:15, promise amount 12,500.00 and promise date 20 December 2026
    Given case owner "U-2001" records a call on 15 December 2026 09:30 to contact point "CP-SYN-0301-M" with result NO_ANSWER
    When the load completes and the call is saved
    Then the ledger holds a CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and retention class "ILG-STD"
    Then the ledger holds a CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30, contact point "CP-SYN-0301-M" and result NO_ANSWER

  Scenario: AC2 A hand-over is recorded
    Given case "RW-2026-000301" is transferred from "U-2001" to "U-2002" on 16 December 2026 11:00
    Given instruction "INS-SYN-0301" is issued to partner "LF-SYN-01" on 17 December 2026 14:00
    When both moves complete
    Then the CASE_TRANSFERRED entry of 16 December 2026 11:00 holds from "USER:U-2001" and to "USER:U-2002"
    Then the ledger holds a HANDOVER entry with channel PORTAL, direction OUTBOUND, from "USER:U-2002", to "PARTNER:LF-SYN-01", occurred 17 December 2026 14:00

  Scenario: AC3 The ledger is one place
    Given the EFS entry of 14 December 2026, the Workbench call of 15 December 2026 and a partner result from "LF-SYN-01" entered in the partner portal on 18 December 2026 16:00
    When the case is read
    Then GET /cases/{caseId}/interactions returns the 3 entries in the order 14, 15 and 18 December 2026
    Then each entry names its source: EFS, WORKBENCH, and WORKBENCH with channel PORTAL and event code PARTNER_RESULT

  Scenario: AC4 Letter, delivery, offer and payment are recorded
    Given notice "NT-SYN-0301" is dispatched on 19 December 2026 with barcode "EV000000001TH"
    Given WIN returns delivered for it on 22 December 2026
    Given treatment "TRT-SYN-0301" is approved on 23 December 2026
    Given proceeds "PRC-SYN-0301" of 5,000.00 are matched to the case on 24 December 2026
    When the four events are processed
    Then the ledger holds a LETTER entry with delivery status SENT and external reference "EV000000001TH"
    Then a LETTER entry with delivery status DELIVERED on 22 December 2026
    Then an OFFER entry linked to "TRT-SYN-0301" and a PAYMENT entry linked to "PRC-SYN-0301"

  Scenario: AC5 Nothing is written twice
    Given event NoticeDispatched with event ID "EVT-SYN-0001" has been processed by "ledger-channels"
    When the same event is delivered again
    Then the ledger holds one entry for "EVT-SYN-0001"
    Then the hit count for that key becomes 2

  Scenario: AC6 EFS rows outside the list or outside a case are not written
    Given the EFS rows for 14 December 2026 hold 3 rows: action code "PTP" for "ACC-SYN-0301", action code "SYS" not on the list for "ACC-SYN-0301", and action code "PTP" for account "ACC-SYN-0999" on no open case
    When the load completes
    Then the ledger holds 1 new EFS entry
    Then the import summary shows 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case

  Scenario: AC7 A ledger write failure loses nothing
    Given the ledger store is unavailable
    When event NoticeDispatched for "NT-SYN-0301" is delivered
    Then the system writes no entry , the delivery stays in the outbox with status RETRYING and an incident is raised
    When the ledger store is available again and the outbox retries
    Then the ledger holds one LETTER entry for "NT-SYN-0301"

  Scenario: AC8 An event for an unknown case goes to the exception queue
    Given event InstructionIssued names an instruction whose case does not exist
    When the outbox has retried the delivery 3 times
    Then the system writes no entry
    Then the delivery is in the exception queue with a task for role RW-PLATADM

  Scenario: AC9 A late EFS row reads in time order
    Given the ledger holds the Workbench call of 15 December 2026 09:30
    When the EFS row with contact time 14 December 2026 10:15 is processed on 15 December 2026 at 10:00
    Then the timeline shows the EFS entry before the call

  Scenario: AC10 A case with no entry
    Given open case "RW-2026-000302" with no ledger entry
    When the case owner opens the timeline
    Then the timeline shows the empty state with message MSG-P3-024

  Scenario: AC11 A case outside the reader's scope is refused
    Given case "RW-2026-000301" is owned by "U-2002" in team "MTG-BKK"
    When case owner "U-3001" of team "HP-NE" with Own scope reads its ledger
    Then the response is 404 with message MSG-P4-003
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Event to ledger event code: InstructionIssued to HANDOVER; PartnerResultSubmitted to PARTNER_RESULT; NoticeDispatched and NoticeDelivered to LETTER; TreatmentApproved to OFFER; ProceedsMatched to PAYMENT; an EFS contact row to CONTACT | events.txt EV-10, EV-14, EV-15, EV-20, EV-21, EV-25, EV-26; LOV-LEDGER-EVENT |
| BR2 | A hand-over between bank owners is the CASE_ALLOCATED or CASE_TRANSFERRED entry of RWB-E1-067, with no channel, enriched with the holder before and after; a hand-over to a partner has channel PORTAL and direction OUTBOUND; a partner result has channel PORTAL and direction INBOUND | REQ-ILG-011; LOV-CHANNEL; LOV-DIRECTION |
| BR3 | An EFS row enters the ledger only when its action code is on the EFS ledger outcome list, and only for an account linked to an open case | DL29; INT-07 |
| BR4 | Entries from EFS carry source_system EFS; every other entry carries WORKBENCH, including partner portal entries, which are entered on Workbench screens | LOV-SOURCE; INT-24 |
| BR5 | The contact point is stored as a reference to contact_point; the number or address is never copied into the entry | REQ-ILG-014; CTL-11 |
| BR6 | Each entry carries the retention class of its event code from the Retention classes reference table, set independently of the decision log | REQ-ILG-013; NFR-075; DL26 |
| BR7 | One entry per idempotency key; a repeat is ignored and counted | R-UNI-40; REQ-ILG-007 |
| BR8 | A failed ledger write raises an incident and the delivery is retried; no entry is discarded | REQ-ILG-008; NFR-077 |
| BR9 | The timeline orders entries by occurred time, then by case sequence | REQ-ILG-006 |

### 9. State transitions

None. This story does not change a case status. It creates interaction records and changes the state of the "ledger-channels" outbox deliveries.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs the "ledger-channels" consumer and appends entries (Case record C) |
| SY-DATALOAD, data load from COLLINS | Runs the EFS import step after the COLLINS load (Case record C) |
| RW-CASEOWN, case owner | Reads the ledger of cases in scope (Case record R) |
| RW-TEAMMGR, RW-CONDUCT | Read the ledger of cases in scope (Case record R) |
| RW-COMPLY, Compliance and PDPA officer | Sets the retention class per event code through a reference data change (Reference data U) |
| RW-REFADM, reference data administrator | Loads the EFS ledger outcome list and the retention classes (Reference data C) |
| No approval applies | The story takes no decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-INT-014 | interaction | event_code | Write |
| DF-INT-018 | interaction | idempotency_key | Write |
| DF-INT-028 | interaction | delivery_status | Write |
| DF-INT-029 | interaction | external_ref | Write |
| DF-INT-022 | interaction | contact_point_id | Write |
| DF-INT-023 | interaction | from_holder_ref | Write |
| DF-INT-024 | interaction | to_holder_ref | Write |
| DF-INT-025 | interaction | treatment_id | Write |
| DF-INT-026 | interaction | proceeds_id | Write |
| DF-INT-027 | interaction | retention_class | Write |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-022 | recovery_case | closed_date | Read |
| DF-CAS-025 | case_account | case_id | Read |
| DF-CAS-026 | case_account | account_id | Read |
| DF-PTY-013 | contact_point | id | Read |
| DF-LEG-015 | notice | id | Read |
| DF-LEG-016 | notice | case_id | Read |
| DF-LEG-020 | notice | barcode | Read |
| DF-LEG-022 | notice | delivery_status | Read |
| DF-PRT-002 | partner | partner_code | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-FIN-001 | proceeds | id | Read |
| DF-ACC-002 | loan_account | account_no | Read |

Reads of other modules' records go through their published interfaces, never their tables. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Events consumed** (outbox consumer "ledger-channels", RWB-TE-006): EV-10 TreatmentApproved, EV-14 NoticeDispatched, EV-15 NoticeDelivered, EV-20 InstructionIssued, EV-21 PartnerResultSubmitted, EV-25 ProceedsMatched, EV-26 LoadCompleted (source COLLINS). EV-02 CaseAllocated and EV-04 CaseTransferred stay with the RWB-E1-067 consumer, which this story extends with the holder fields. Delivery is at least once; the consumer is idempotent by key. No event is published.

**Published interfaces called**

```java
// recovery.dataengine.ledger.api, RWB-E1-066; must run in the caller's transaction
LedgerEntryRef InteractionLedgerWriter.append(LedgerEntryCommand command);
//   This story adds to LedgerEntryCommand: UUID contactPointId, String fromHolderRef, String toHolderRef,
//   UUID treatmentId, UUID proceedsId, String retentionClass (deliveryStatus and externalRef come from RWB-E2-022)
// RWB-E1-007
boolean IdempotencyGuard.firstTime(String consumer, String idempotencyKey);
// P1 EFS data, RWB-E1-004
List<EfsContactOutcome> EfsContactHistory.outcomesFor(LocalDate businessDate);
// P3 case facts
Optional<CaseSummary> CaseQuery.byId(UUID caseId);
List<UUID> CaseQuery.openCaseIdsForAccount(UUID accountId);
// P6 notice facts
Optional<NoticeSummary> NoticeQuery.byId(UUID noticeId);   // caseId, contactPointId, noticeType, barcode
// S9 instruction facts
Optional<InstructionSummary> InstructionQuery.byId(UUID instructionId); // caseId, partnerCode
```

**GET /api/recovery/v1/cases/{caseId}/interactions** (operationId getCasesCaseidInteractions, existing)

| Item | Value |
|---|---|
| Parameters used | caseId (path), channel, actor, from, to, page, size |
| Response 200 | InteractionPage of Interaction, with the fields of RWB-E1-068 and RWB-E2-022 plus contactPointId, fromHolderRef, toHolderRef, treatmentId, proceedsId and retentionClass (recorded in the additions file) |
| 403 | Role lacks Case record R (MSG-P4-002) |
| 404 | Case does not exist or is outside scope (MSG-P4-003) |
| Authorization | Case record, right R; summary masked by role |
| Idempotency | Read only |

**EFS import step**

| Item | Value |
|---|---|
| Trigger | LoadCompleted for the COLLINS load, after JOB-01 passes its checks |
| Job | A step of JOB-01 COLLINS load check and intake, run under SY-DATALOAD |
| Input | The day's EFS contact outcomes (INT-07) |
| Output | Ledger entries; an import summary with read, written, excluded and not-on-a-case counts |
| Idempotency key | "EFS:" + account ID + action code + contact time |
| Restart | A rerun for the same business date writes only the entries not yet written |

### 13. Solution plan

**Package.** Folder `recovery/integration/ledger`, Java package `<ACE base package>.recovery.integration.ledger`, for the channel consumer and the EFS import. The holder enrichment is a change to the RWB-E1-067 mapper in `recovery.dataengine.ledger`, reviewed by its code owners. Front end folder `src/modules/recovery/caserecord/ledger`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LedgerChannelListener | Listener | Outbox consumer "ledger-channels" for the seven events; idempotency check; calls the mapper and the writer |
| LedgerChannelMapper | Service | One method per event type implementing BR1, BR2, BR4 and BR5 |
| EfsContactOutcomeImporter | Job | Import step after the COLLINS load; applies BR3; writes the import summary |
| EfsLedgerOutcomeList | Rule table | Reference rows: action code, channel, in ledger; loaded by RW-REFADM (DL29) |
| HolderEnricher | Service | Adds fromHolderRef and toHolderRef to the CASE_ALLOCATED and CASE_TRANSFERRED commands of RWB-E1-067 |
| RetentionClassResolver | Service | Retention class by event code (BR6), called by InteractionLedgerWriter for every entry |
| InteractionLedgerWriter | Published interface | From RWB-E1-066; this story extends its command |
| LedgerTimelineSection | React component | The ledger section of SCR-03 and the ledger filters on SCR-04: channel, source, actor, date range |

**Database.** Migration in the P1 ledger migration folder adds to interaction: contact_point_id uuid, from_holder_ref varchar(60), to_holder_ref varchar(60), treatment_id uuid, proceeds_id uuid, retention_class varchar(10). The unique key on idempotency_key comes from RWB-E1-066; the append-only trigger tr_interaction_append_only stays in place; the index ix_interaction_case_time serves the read.

**Configuration and reference data.** EFS ledger outcome list (DL29; assumed default as in section 3); Retention classes reference table (DL26; assumed "ILG-STD"); LOV-LEDGER-EVENT with the added values PARTNER_RESULT and OFFER; LOV-CHANNEL, LOV-DIRECTION, LOV-SOURCE. All loaded by RW-REFADM through the reference data service (RWB-E1-043). Consumer "ledger-channels" listed in rwb.integration.outbox.consumers (RWB-TE-006), not holding a case step, owner role RW-PLATADM.

**Build steps**

1. Add the migration for the six columns; extend LedgerEntryCommand and the Interaction schema in the API specification; regenerate types.
2. Write LedgerChannelMapper with one unit test per event type (BR1, BR2, BR4, BR5).
3. Write RetentionClassResolver against the reference data interface and call it from the writer (BR6).
4. Write LedgerChannelListener with the idempotency check and the failure path that fails the delivery and raises an incident (AC5, AC7, AC8).
5. Write HolderEnricher in the RWB-E1-067 mapper (AC2).
6. Write EfsContactOutcomeImporter as a step after JOB-01 with the import summary (AC1, AC6, AC9).
7. Add the ledger section to SCR-03 and the filters to SCR-04 with the empty state (AC3, AC10); run the access and scope tests (AC11).

**Feature flag.** `rwb.integration.ledger-channels`. Off: the consumer acknowledges the seven events without writing, the import step does not run and the holder fields stay empty; the Epic 1 ledger is unchanged.

**Done when.** The tests in section 16 pass; a case with 500 entries reads its first page in under 2 seconds (NFR-070).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-024 | The case has no ledger entry (new) | No interactions are recorded on this case yet. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-03 Case record, states Loading, Read only, Editable and On hold: the ledger section shows the latest 20 entries. SCR-04 Case timeline, states Loading and Filtered: the case owner filters by channel, source, actor and date range and reads each entry's time, channel, contact point (masked by role), outcome, promise, linked offer or payment, delivery status, holder change and source. The Empty state shows MSG-P3-024.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-034-01 | AC1, BR3, BR4, BR5, BR6 | System | One EFS row with a promise; one Workbench call |
| TC-E2-034-02 | AC2, BR2 | System | One transfer; one instruction to partner LF-SYN-01 |
| TC-E2-034-03 | AC3, BR4, BR9 | System | Entries from EFS, Workbench and the partner portal |
| TC-E2-034-04 | AC4, BR1 | System | NoticeDispatched, NoticeDelivered, TreatmentApproved, ProceedsMatched |
| TC-E2-034-05 | AC5, BR7 | System | NoticeDispatched delivered twice with one event ID |
| TC-E2-034-06 | AC6, BR3 | System | Three EFS rows: listed, unlisted, no open case |
| TC-E2-034-07 | AC7, BR8 | System | Ledger store stopped, then restarted |
| TC-E2-034-08 | AC8 | System | InstructionIssued for a case that does not exist |
| TC-E2-034-09 | AC9, BR9 | System | EFS row processed after a later Workbench call |
| TC-E2-034-10 | AC10 | System | Case with no entry |
| TC-E2-034-11 | AC11 | System | Reader of team HP-NE with Own scope |
| TC-E2-034-12 | Access | Access | RW-REFADM reads the ledger; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the EFS outcome list, event codes, channels and retention classes are reference data.
- No personal data in logs, tests or prompts; the contact point is a reference and the summary is masked by role.
- No read of another module's tables: case, notice, instruction, treatment, proceeds and EFS facts come through published interfaces.
- The ledger is append only; the story never updates or deletes an entry.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-009 | Contact outcomes from collections reach the ledger | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | R-UNI-40 | TC-E2-034-01, TC-E2-034-06, TC-E2-034-09 |
| REQ-ILG-010 | Dispatched letters write their result, including proof of delivery | Business Requirements Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-40 | TC-E2-034-04, TC-E2-034-05, TC-E2-034-07 |
| REQ-ILG-011 | A hand-over names who held the case, who holds it now and when | Business Requirements Epic 2, section 3.2 | FEAT-ILG-08 | 06 to 10 Recovery case processes | None | TC-E2-034-02, TC-E2-034-08 |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline | Business Requirements Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | None | TC-E2-034-03, TC-E2-034-10, TC-E2-034-11, TC-E2-034-12 |
| REQ-ILG-013 | Ledger entries carry their own retention class | Business Requirements Epic 2, section 3.2 | FEAT-ILG-10 | All recovery processes | None | TC-E2-034-01 |

### 19. Out of scope

- Contact and promise history attached at case creation: RWB-E2-001.
- SMS and LINE dispatch results: RWB-E2-022, which writes them through the same InteractionLedgerWriter.
- Proof of delivery capture from WIN and the notice period timer: RWB-E2-021.
- Ledger entries for Workbench actions such as creation, allocation and decisions: RWB-E1-067.
- Retention periods and disposal of ledger entries: DL26 and the retention job JOB-17.
- Masking rules by role: RWB-E1-037.


---

## RWB-E2-035 Next action on the case

| Item | Value |
|---|---|
| Story key | RWB-E2-035 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CWC-27 Show the next action and its due date on a case; FEAT-CWC-28 Set the next action from the routing rules |
| Requirement IDs | REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014, REQ-WKM-015 |
| BRD section | Business Requirements Epic 2, section 3.2 |
| L3 process | 06 to 10 Recovery case processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-031, RWB-E2-033 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every active case to show one next action, its owner and its due date, taken from the routing rule that moved the case into its current state**, so that **I never open a case and have to work out what it needs**.

### 2. Business rationale

A case owner today reads the case history to decide what is owed next, and a case can wait for weeks with nobody owing anything on it. The routing rules already hold the action, the owner of the next state and the timer for every move, so the Workbench copies these onto the case at each move and shows them on the case and in the case list. A case with no next action is raised to the team manager as an exception. It meets REQ-WKM-012, REQ-WKM-013 and REQ-WKM-016; the business measure is the count of active cases with no next action, with a target of zero.

### 3. Preconditions

- RWB-E1-018 (case record and transitions), RWB-E1-031 (case list) and RWB-E2-033 (case list with ageing) are done.
- The rule rows for the route sets in force are loaded with action_text, owner_role and timer_spec (RWB-E1-029; DL24).
- The service levels and timers reference table holds a time per state (DL22). Until the business values are loaded it is seeded with 5 working days for each state of the route sets in force (assumed); a state left out of the seed has no row.
- The bank holiday list is loaded in the configuration service under key rwb.calendar.bank-holidays (RWB-E1-042), by RW-REFADM.
- The reader holds a role with Case record R; the transition runs under SY-CASEWF.
- Feature flag `rwb.casewf.next-action` is on.

### 4. Flow

1. SY-RULES: evaluates the route set and returns the firing rule row for the case's state and event.
2. SY-CASEWF: moves the case to the rule's to_state and, in the same transaction, calls NextActionAssigner with the firing rule.
3. NextActionAssigner: copies the rule's action_text, owner_role and rule_id to the case.
4. TimerSpecResolver: turns the rule's timer_spec into a due date (BR3); when the spec has no fixed duration it reads the service levels and timers reference table for the to_state (BR4).
5. NextActionAssigner: sets next_action_waiting when the owner role belongs to a customer party or a partner user (BR5).
6. NextActionAssigner: when no due date can be found, leaves the due date empty and raises task NEXT_ACTION_MISSING on the exception queue for the team manager (BR7).
7. JOB-05 timer check: every 5 minutes finds active cases with no next action, resolves them from the latest state change in the decision log, or raises the same task once.
8. Case owner: opens the case record (SCR-03); the front end calls GET /api/recovery/v1/cases/{caseId}/next-action and shows the action, the owner and the due date, or the waiting text.
9. Team manager: opens the case list (SCR-02); the next action, its owner and due date are columns and an overdue action is marked (BR6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The rule's timer_spec is None or has no fixed duration | Due date taken from the service levels and timers table for the to_state | None | AC5 |
| X2 | No due date can be found from the rule or the table | Due date empty; task NEXT_ACTION_MISSING raised once for the team manager; warning on the case | MSG-P2-023 | AC6 |
| X3 | The due date falls on a weekend or a bank holiday | Working days skip Saturday, Sunday and the holiday list | None | AC7 |
| X4 | The case closes | Next action cleared; the case leaves the exception list | None | AC8 |
| X5 | The same transition is delivered twice | Next action unchanged; no second task | None | AC9 |
| X6 | Two transitions on one case commit at the same time | The optimistic lock refuses the second; it is retried and the next action is that of the last committed rule | MSG-GEN-004 | AC10 |
| X7 | An active case from before the flag was switched on has no next action | JOB-05 sets it from the latest state change in the decision log | None | AC11 |
| X8 | The reader's role does not hold Case record R | Refused with 403 | MSG-P4-002 | Access test TC-E2-035-13 |
| X9 | The rule's timer is "same day" | Due date is the business date of the move | None | AC12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the transition, rule rows and case list that exist after RWB-E1-018 and RWB-E2-033 |
| Negotiable | Action text, owner and timer are rule data; durations for states without a timer are DL22 values |
| Valuable | Every active case states what is owed, by whom and by when |
| Estimable | One assigner, one timer resolver, one job step, one read endpoint, two screen elements |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below has one test with fixed rule rows and dates |

### 7. Acceptance criteria

```gherkin
Feature: Next action on the case

  Background:
    Given rule R-RES-04 version "RES-2026.12" moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER with action "Assign the case to a restructuring officer and start the offer clock", owner role RW-RESTRUCT and timer "2 working days"
    Given rule R-SET-13 version "SET-2026.12" moves WITH_OPS_SETTLEMENT on SETTLEMENT_BOOKED to AWAITING_PAYMENT with action "Set the payment due date and wait for the money", owner role CU-BORROW and timer "payment due 30 days"
    Given the bank holiday list holds 31 December 2026 and 1 January 2027

  Scenario: AC1 Every active case carries a next action
    Given case "RW-2026-000401" with status IN_PROGRESS moved by R-RES-04 on 11 December 2026
    When the case is opened
    Then it shows action "Assign the case to a restructuring officer and start the offer clock", owner "Restructuring officer (FCR)" and due date 15 December 2026

  Scenario: AC2 The routing rules set it
    Given case "RW-2026-000402" in state IN_FCR_QUEUE
    When event CASE_PICKED_UP fires R-RES-04 on Friday 11 December 2026
    Then the case holds next action text from R-RES-04, owner role RW-RESTRUCT, rule ID R-RES-04 and due date Tuesday 15 December 2026
    Then the system writes the values in the same transaction as the move to WITH_FCR_OFFICER

  Scenario: AC3 Waiting is a valid next action
    Given case "RW-2026-000403" moved by R-SET-13 on 14 December 2026
    When the case is opened
    Then the next action reads "Waiting for Customer (borrower): Set the payment due date and wait for the money"
    Then the wait ends on 13 January 2027
    Then next action waiting is true

  Scenario: AC4 It is visible on the list
    Given case "RW-2026-000401" with due date 15 December 2026
    Given case "RW-2026-000403" with due date 13 January 2027
    When a manager reads the list on 16 December 2026
    Then next action, next action owner and due date are columns
    Then the system marks row "RW-2026-000401" Overdue
    Then the system does not mark row "RW-2026-000403" Overdue

  Scenario: AC5 A rule with no timer takes the state's service level
    Given rule R-RES-03 moves the case to BACK_TO_ROUTE_DECISION with owner role RW-CASEOWN and timer "None"
    Given the service levels and timers table holds 5 working days for BACK_TO_ROUTE_DECISION
    When R-RES-03 fires on Monday 14 December 2026
    Then the due date is Monday 21 December 2026
    Then the owner shown is the case owner named on the case

  Scenario: AC6 No due date can be found
    Given rule R-DEV-05 moves the case to DEV_WITH_OWNER with owner role RW-LEGAL and timer "deadline driven"
    Given the service levels and timers table holds no row for DEV_WITH_OWNER
    When the rule fires on case "RW-2026-000404" of team "MTG-BKK"
    Then the case holds the action and owner of R-DEV-05 with no due date
    Then the system raises one task NEXT_ACTION_MISSING on the exception queue for role RW-TEAMMGR of team "MTG-BKK"
    Then the case record shows warning MSG-P2-023

  Scenario: AC7 Working days skip weekends and bank holidays
    When R-RES-04 fires on Wednesday 30 December 2026
    Then the due date is Tuesday 5 January 2027

  Scenario: AC8 A closed case has no next action
    Given case "RW-2026-000404" with task NEXT_ACTION_MISSING open
    When the case closes with closure reason SETTLED
    Then the next action fields are empty
    Then the system cancels the task
    Then the case is not in the list of active cases with no next action

  Scenario: AC9 A repeated transition changes nothing
    Given case "RW-2026-000402" was moved by R-RES-04 on 11 December 2026 with decision log entry "DLE-SYN-0402"
    When the same transition with "DLE-SYN-0402" is processed again
    Then the next action and due date are unchanged
    Then the system raises no task

  Scenario: AC10 Two transitions at the same time
    Given case "RW-2026-000405" at version 7
    When two transitions commit against version 7 at the same time
    Then one commits and the other is refused with MSG-GEN-004 and retried against version 8
    Then the next action is that of the rule committed last

  Scenario: AC11 Cases open before the switch-on are filled
    Given 3 active cases with no next action, each with a state change in the decision log by R-RES-04 on 11 December 2026
    When JOB-05 runs on 14 December 2026
    Then each of the 3 cases holds the next action of R-RES-04 with due date 15 December 2026

  Scenario: AC12 A same day timer
    Given a rule with timer "same day" fires on 14 December 2026
    Then the due date is 14 December 2026
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On every move, the next action text, the owner role and the rule ID come from the firing rule row: action_text, owner_role, rule_id | FEAT-CWC-28; REQ-WKM-013; rule_row |
| BR2 | The next action is never entered by a person | REQ-WKM-013 |
| BR3 | timer_spec "n working days" adds n working days; "n days" with any label before it adds n calendar days; "same day", "Same day" and "immediate" give the date of the move; "next working day" adds 1 working day | rule_row.timer_spec |
| BR4 | Any other timer_spec, including "None", takes the time for the to_state from the service levels and timers table | DL22 |
| BR5 | The next action is a wait when the owner role is of class Customer party or Partner user; the text starts "Waiting for {owner}:" | role.role_class |
| BR6 | A next action is overdue when its due date is earlier than today and the case is not closed | REQ-WKM-012 |
| BR7 | An active case with no due date or no next action raises one NEXT_ACTION_MISSING task to the team manager | REQ-WKM-016 |
| BR8 | Working days are Monday to Friday, excluding the dates in the bank holiday list | Configuration key rwb.calendar.bank-holidays |
| BR9 | When the owner role is the role of the case's queue, the owner shown is the case owner; otherwise the role name | queue.role_code |

### 9. State transitions

None. This story does not change a case status. It writes the next action fields on the case in the same transaction as each move made by RWB-E1-018 and RWB-E1-021, and creates or cancels NEXT_ACTION_MISSING tasks (task status OPEN to CANCELED).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Writes the next action fields and the exception task (Case record U, Queue and allocation C) |
| SY-RULES, rules component | Returns the firing rule row |
| RW-CASEOWN, case owner | Reads the next action of cases in scope (Case record R) |
| RW-TEAMMGR, team manager | Reads the list and works NEXT_ACTION_MISSING tasks on the exception queue |
| RW-COE, center of excellence analyst | Owns the action, owner and timer columns of the rule rows (Rules and parameters CRUD) |
| RW-REFADM, reference data administrator | Loads the service levels and timers table and the bank holiday list |
| No approval applies | The story takes no decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-049 | recovery_case | next_action_text | Write |
| DF-CAS-050 | recovery_case | next_action_owner_role | Write |
| DF-CAS-051 | recovery_case | next_action_due_date | Write |
| DF-CAS-052 | recovery_case | next_action_rule_id | Write |
| DF-CAS-053 | recovery_case | next_action_waiting | Write |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-007 | recovery_case | route_state | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-011 | recovery_case | team_code | Read |
| DF-CAS-022 | recovery_case | closed_date | Read |
| DF-WRK-005 | queue | role_code | Read |
| DF-WRK-017 to DF-WRK-026 | task | all fields | Write |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-008 | rule_row | action_text | Read |
| DF-REF-009 | rule_row | to_state | Read |
| DF-REF-010 | rule_row | owner_role | Read |
| DF-REF-011 | rule_row | timer_spec | Read |
| DF-REF-036 | role | role_name | Read |
| DF-REF-037 | role | role_class | Read |
| DF-DEC-004 | decision_log_entry | rule_id | Read |
| DF-DEC-005 | decision_log_entry | rule_version | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/cases/{caseId}/next-action** (new; recorded in the additions file)

| Item | Value |
|---|---|
| Parameters | caseId (path, uuid) |
| Response 200 | NextAction: text, ownerRole, ownerName, ownerUserId (when BR9 names the case owner), dueDate, waiting, overdue, missing, ruleId, ruleVersion |
| 401 | No valid session (MSG-P4-001) |
| 403 | Role lacks Case record R (MSG-P4-002) |
| 404 | Case does not exist or is outside scope (MSG-P4-003) |
| Authorization | Case record, right R |
| Idempotency | Read only |

**GET /api/recovery/v1/cases** and **GET /api/recovery/v1/cases/export** (change recorded in the additions file): each Case item and each export row gains nextAction, nextActionOwner, nextActionDueDate and nextActionOverdue, read from the same fields. Authorization and errors are unchanged from RWB-E2-033.

**Interface inside P3** (called by the transition service of RWB-E1-018 in the same transaction)

```java
void NextActionAssigner.assign(UUID caseId, RuleRowRef firedRule, LocalDate businessDate);
Optional<LocalDate> TimerSpecResolver.dueDate(String timerSpec, String toState, LocalDate from);
```

**Published interfaces called**

```java
// P7 decision log, for cases with no next action
Optional<RuleRowRef> DecisionLogQuery.latestStateChange(UUID caseId);
// P4 reference data
RoleInfo ReferenceData.role(String roleCode);          // roleName, roleClass
Optional<Duration> ReferenceData.serviceLevel(String state);
```

**Job step**

| Item | Value |
|---|---|
| Trigger | JOB-05 Timer check, every 5 minutes |
| Step | Next action check: active cases with next_action_rule_id empty or next_action_due_date empty |
| Input | Case rows of P3; the latest state change from P7 |
| Output | Filled next action fields, or one NEXT_ACTION_MISSING task |
| Events published | None |
| Idempotency key | Case ID and task code NEXT_ACTION_MISSING: at most one open task per case |
| Restart | The next run picks up any case the last run missed |

### 13. Solution plan

**Package.** The story is in the P2 backlog. The fields, the rule rows and the transitions belong to P3, so the code is in folder `recovery/casewf/nextaction`, Java package `<ACE base package>.recovery.casewf.nextaction`. Front end folder `src/modules/recovery/caserecord/nextaction`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NextActionAssigner | Service | BR1, BR5, BR7 and BR9, called inside the transition |
| TimerSpecResolver | Service | BR3, BR4 and BR8, pure functions with a holiday list input |
| NextActionCheckStep | Job | The JOB-05 step for cases with no next action (BR7, AC11) |
| NextActionController | Controller | GET /cases/{caseId}/next-action |
| NextActionRepository | Repository | Reads and writes the next action fields on recovery_case |
| NextActionPanel | React component | Next action on the SCR-03 header with the waiting text, the overdue marker and the MSG-P2-023 warning |

**Database.** Migration in the P3 migration folder adds to recovery_case: next_action_text varchar(1000), next_action_owner_role varchar(20), next_action_due_date date, next_action_rule_id varchar(20), next_action_waiting boolean NOT NULL DEFAULT false; and `CREATE INDEX ix_case_next_action_missing ON recovery_case (team_code) WHERE closed_date IS NULL AND next_action_due_date IS NULL`. Writes task rows (task_code NEXT_ACTION_MISSING, element_type HUMAN_TASK, discretion REQUIRED, owner_role RW-TEAMMGR). Reads rule_row and queue.

**Configuration and reference data.** Rule rows (RW-COE, RWB-E1-029); service levels and timers table (DL22; assumed 5 working days); bank holiday list rwb.calendar.bank-holidays (RW-REFADM); role names and classes (P4).

**Build steps**

1. Add the migration and extend the generated types with the NextAction schema and the new operation.
2. Write TimerSpecResolver with a table of timer_spec cases taken from the 448 rule rows, and unit tests for AC5, AC7 and AC12.
3. Write NextActionAssigner and call it from the transition service in the same transaction; test AC1, AC2, AC3, AC9 and AC10.
4. Add the exception task and its cancel on closure (AC6, AC8).
5. Add NextActionCheckStep to JOB-05 (AC11).
6. Write NextActionController and NextActionPanel; add the next action fields to the Case items of GET /cases and to the export columns (AC4).
7. Add the access test and the contract test for the new operation.

**Feature flag.** `rwb.casewf.next-action`. Off: the assigner is not called, the step does not run and the panel and columns are hidden.

**Done when.** The tests in section 16 pass and the report of active cases with no next action reads zero on the SIT data set after JOB-05 has run.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-023 | The case has no next action or no due date (new) | This case has no next action. It is on the exception list for {team}. |
| MSG-GEN-004 | A transition commits against a changed version | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-03 Case record, states Read only, Editable and On hold: the header shows the next action, its owner and its due date; a wait shows "Waiting for {owner}" and the wait end date; an overdue action carries the text "Overdue"; a missing action shows MSG-P2-023. SCR-02 Case list: next action, next action owner and due date columns with the overdue marker. SCR-09 Exception queue: the team manager sees NEXT_ACTION_MISSING tasks.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-035-01 | AC1, BR1, BR9 | System | Case moved by R-RES-04 on 11 December 2026 |
| TC-E2-035-02 | AC2, BR1, BR2, BR3 | System | CASE_PICKED_UP on Friday 11 December 2026 |
| TC-E2-035-03 | AC3, BR5 | System | Case moved by R-SET-13 on 14 December 2026 |
| TC-E2-035-04 | AC4, BR6 | System | Two cases read on 16 December 2026 |
| TC-E2-035-05 | AC5, BR4, BR9 | System | R-RES-03 with timer None; table row of 5 working days |
| TC-E2-035-06 | AC6, BR7 | System | R-DEV-05 with timer "deadline driven" and no table row |
| TC-E2-035-07 | AC7, BR8 | System | Move on 30 December 2026 with two holidays |
| TC-E2-035-08 | AC8 | System | Case with an open NEXT_ACTION_MISSING task closes |
| TC-E2-035-09 | AC9 | System | Same transition processed twice |
| TC-E2-035-10 | AC10 | System | Two transitions against version 7 |
| TC-E2-035-11 | AC11 | System | Three cases with no next action before JOB-05 |
| TC-E2-035-12 | AC12, BR3 | System | Rule with timer "same day" |
| TC-E2-035-13 | Access | Access | RW-REFADM reads the next action; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: action text, owner, timer, service levels and holidays are data.
- No personal data in logs, tests or prompts; the next action holds rule text only.
- No read of another module's tables: the decision log and the role table are read through P7 and P4 interfaces.
- The parser recognizes timer patterns; it never holds a duration for a named state.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-012 | Every open case carries one next action with owner and due date | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-RES-04, R-SET-13 | TC-E2-035-01, TC-E2-035-03, TC-E2-035-04, TC-E2-035-08, TC-E2-035-13 |
| REQ-WKM-013 | The next action comes from the rule that moved the case | Business Requirements Epic 2, section 3.2 | FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-03, R-RES-04, R-SET-13 | TC-E2-035-02, TC-E2-035-05, TC-E2-035-07, TC-E2-035-09, TC-E2-035-10, TC-E2-035-12 |
| REQ-WKM-016 | A case with no next action is reported as an exception | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-DEV-05 | TC-E2-035-06, TC-E2-035-11 |
| REQ-WKM-014 | Next action visible on the case record and every queue view | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01 |
| REQ-WKM-015 | An overdue next action escalates like a service level breach | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01 |

### 19. Out of scope

- Escalation when a next action passes its due date: RWB-E2-015 (REQ-WKM-015).
- The next action column in the queue view screens: RWB-E2-011.
- The values of the service levels per state: DL22.
- Loading the route set rule rows beyond allocation, assignment and transfer: DL24.


---

## RWB-E2-036 Queue write interface for models and agents

| Item | Value |
|---|---|
| Story key | RWB-E2-036 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CWC-29 Accept a queue placement from a model or an agent |
| Requirement IDs | REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020 |
| BRD section | Business Requirements Epic 2, section 3.2 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-019, RWB-E1-020, RWB-E1-027 |
| Status | Ready for build |

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **an interface through which an approved model or agent places a case on a queue, under its own service identity and the queue's own rules**, so that **analytical output reaches a person the next working day instead of through a weekly manual step**.

### 2. Business rationale

Model scores and agent findings reach the queues today through a weekly file that a person loads by hand, so a case flagged on Monday is worked the following week. The interface lets an approved caller place a case on a queue the day the decision is made, while the queue's allocation method, caseload cap and the role to permission matrix apply as they do to any case, and every placement is written to the decision log with the caller and its version. It meets REQ-CWC-017, REQ-CWC-018 and REQ-CWC-019; the business measure is the time from a model decision to the case reaching a queue, from up to 7 days today to the same day.

### 3. Preconditions

- RWB-E1-019 (roles, teams and queues as data), RWB-E1-020 (allocation and assignment engine) and RWB-E1-027 (decision log writer) are done.
- The caller is listed in the approved callers list (configuration key rwb.casewf.placement.approved-callers) with its caller code, its type MODEL or AGENT and its service identity. The list is empty at go-live (assumed); RW-COE requests an entry and RW-RISK approves it.
- The permission matrix in force gives the caller's service identity Queue and allocation C. The matrix today gives SY-AGENT R only, so a matrix version change by RW-SECADM is needed before the first caller is switched on.
- The target queue exists with its assignment method, caseload cap and overflow queue (DL23; caseload cap 150, assumed).
- Feature flag `rwb.casewf.queue-placement` is off in every environment except DEV and SIT test runs.

### 4. Flow

1. Caller (model job or agent under its service identity): sends POST /api/recovery/v1/queues/{queueId}/placements with caseId, reason, modelOrAgent and version.
2. PlacementController: returns 404 with MSG-P2-025 when the feature flag is off.
3. PlacementController: checks Queue and allocation C through the common module access check.
4. PlacementController: validates the four fields and checks that modelOrAgent is in the approved callers list for this service identity.
5. PlacementService: reads the queue and the case; refuses a closed case, a case with an open deviation and a case already in this queue.
6. PlacementService: builds the decision log record with the caller, reason, model or agent version and target queue (BR5).
7. PlacementService: sets the case queue and calls AllocationService.assignInQueue, which applies the queue's method and caseload cap and uses the overflow queue when every owner is at the cap.
8. PlacementService: ends any previous assignment, writes the new assignment with reason ALLOCATION, publishes CaseAllocated (and CaseTransferred when the case had an owner) to the outbox and calls DecisionLogWriter.write as the last step, all in one transaction. If the write fails, nothing commits.
9. PlacementController: returns 201 with the placement result.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Feature flag off | 404; nothing changes | MSG-P2-025 | AC4 |
| X2 | Caller is not in the approved callers list | 422; nothing changes | MSG-P2-020 | AC5 |
| X3 | caseId, reason, modelOrAgent or version empty | 422 naming the field | MSG-GEN-001 | AC6 |
| X4 | The case is already in the target queue, including a repeated call | 409; no second entry | MSG-P2-024 | AC7 |
| X5 | The case is closed | 409 | MSG-P3-005 | AC8 |
| X6 | The case has an open deviation | 409; the case stays with the deviation handler (R-DEV-01) | MSG-P2-021 | AC9 |
| X7 | The queue or the case does not exist | 404 | MSG-P4-003 | AC10 |
| X8 | Every owner in the queue is at the caseload cap | Case placed in the overflow queue with status unchanged | None | AC2 |
| X9 | Two placements of the same case commit at the same time | One commits; the other gets 409 | MSG-GEN-004 | AC11 |
| X10 | The caller's identity lacks Queue and allocation C | 403 | MSG-P4-002 | Access test TC-E2-036-13 |
| X11 | The decision log write fails | 503; nothing changes; incident raised (R-UNI-39) | MSG-P7-003 | Principle 5 test TC-E2-036-14 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the allocation engine and decision log writer of Epic 1; no model is needed to build or test it |
| Negotiable | Which callers are approved is configuration; caps and methods are queue data |
| Valuable | A daily model decision reaches a person the same day |
| Estimable | One endpoint, one service, one configuration list, reuse of the allocation engine |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below has one test with a synthetic caller |

### 7. Acceptance criteria

```gherkin
Feature: Queue write interface for models and agents

  Background:
    Given feature flag "rwb.casewf.queue-placement" is on
    Given the permission matrix version "PM-SIT-02" gives service identity SY-AGENT Queue and allocation C
    Given the approved callers list holds caller "MDL-SYN-PRIORITY" of type MODEL for service identity SY-AGENT
    Given queue "MTG-BKK-PRI" of team "MTG-BKK" uses method ROUND_ROBIN with caseload cap 150 and overflow queue "MTG-BKK-OVF"
    Given case "RW-2026-000501" has status NEW, no owner, no open deviation

  Scenario: AC1 A non-engine writer can place a case
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0"
    Then the response is 201
    Then the case is in queue "MTG-BKK-PRI"
    Then the assignment and the case record show SY-AGENT as the identity that made the change

  Scenario: AC2 The same rules still apply
    Given queue "MTG-BKK-PRI" holds owners "U-5001" with 150 open cases and "U-5002" with 149 open cases
    When the model places case "RW-2026-000501" on it
    Then the system gives the case to "U-5002" by round robin, skipping "U-5001" at the cap
    Then the case status becomes ASSIGNED
    When both owners hold 150 open cases and the model places case "RW-2026-000502"
    Then case "RW-2026-000502" is in queue "MTG-BKK-OVF" with no owner and status NEW

  Scenario: AC3 Every placement is logged
    When the model places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then one decision log entry exists with decision code D6, model version "MDL-SYN-PRIORITY 1.4.0", the reason "High cure score", the caller identity SY-AGENT and final call "PLACED MTG-BKK-PRI"
    Then the entry, the case change, the assignment and the events commit in one transaction

  Scenario: AC4 It is off until a consumer exists
    Given feature flag "rwb.casewf.queue-placement" is off
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the response is 404 with message MSG-P2-025
    Then the case and the decision log are unchanged

  Scenario: AC5 A caller that is not approved is refused
    When SY-AGENT places a case with modelOrAgent "MDL-SYN-UNLISTED"
    Then the response is 422 with message MSG-P2-020
    Then nothing changes

  Scenario: AC6 A required field is empty
    When SY-AGENT places case "RW-2026-000501" with no reason
    Then the response is 422 with message MSG-GEN-001 for field reason
    Then nothing changes

  Scenario: AC7 A case already in the queue
    Given case "RW-2026-000501" was placed on queue "MTG-BKK-PRI" at 08:10
    When the same request is sent again at 08:11
    Then the response is 409 with message MSG-P2-024
    Then there is still one assignment and one decision log entry for the placement

  Scenario: AC8 A closed case is refused
    Given case "RW-2026-000503" has status CLOSED
    When the model places it on queue "MTG-BKK-PRI"
    Then the response is 409 with message MSG-P3-005
    Then nothing changes

  Scenario: AC9 A case with an open deviation stays with its handler
    Given case "RW-2026-000504" has deviation X2 open and is in the deviation handler's queue
    When the model places it on queue "MTG-BKK-PRI"
    Then the response is 409 with message MSG-P2-021
    Then the case stays in the deviation handler's queue

  Scenario: AC10 An unknown queue or case
    When the model places case "RW-2026-000501" on a queue ID that does not exist
    Then the response is 404 with message MSG-P4-003

  Scenario: AC11 Two placements at the same time
    When two placements of case "RW-2026-000501" to queues "MTG-BKK-PRI" and "MTG-BKK-CO" commit at the same time
    Then one succeeds with 201
    Then the system refuses the other with 409 and message MSG-GEN-004
    Then the case is in exactly one queue with one open assignment

  Scenario: AC12 A case that already has an owner
    Given case "RW-2026-000505" has status IN_PROGRESS, owner "U-5100" and queue "MTG-BKK-CO"
    When the model places it on queue "MTG-BKK-PRI"
    Then the assignment of "U-5100" ends and a new owner is chosen by the queue's method
    Then the case status stays IN_PROGRESS
    Then events CaseAllocated and CaseTransferred are written to the outbox
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a caller in the approved callers list, under the service identity listed for it, may place a case | REQ-CWC-019; configuration key rwb.casewf.placement.approved-callers |
| BR2 | The caller passes the same access check as a person: Queue and allocation C in the permission matrix in force | REQ-CWC-018; REQ-ACA-010; CTL-09 |
| BR3 | The owner is chosen by the queue's assignment method within its caseload cap; when every owner is at the cap the case goes to the overflow queue | queue.assignment_method, capacity_cap, overflow_queue_id; DL23 |
| BR4 | A case with an open deviation stays with the deviation handler | R-DEV-01 |
| BR5 | Every placement writes one decision log entry in the same transaction as the change, with the caller identity, the reason and the model or agent version | NFR-078; Principle 5; CTL-06 |
| BR6 | A decision that cannot be written to the decision log does not proceed | R-UNI-39; Principle 5 |
| BR7 | A case closed or already in the target queue is not placed | LOV-CASE-STATUS; MSG-P3-005 |
| BR8 | The interface is off by feature flag until the first caller is approved | REQ-CWC-019; DT11 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| New | Allocation rule matched (placement) | An owner below the cap | Assigned |
| New | Allocation rule matched (placement) | Every owner at the cap | New, in the overflow queue |
| Assigned, In progress, Waiting customer, Waiting partner, Waiting approval | Placement on another queue | An owner below the cap | Unchanged status, new owner |
| On hold | Placement | deviation_open = true | On hold, refused (MSG-P2-021) |
| Closed | Placement | Always | Closed, refused (MSG-P3-005) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | Places cases once the matrix gives it Queue and allocation C and its caller is approved |
| SY-CASEWF, case workflow module | Updates the case, writes the assignment, publishes the events |
| SY-DECLOG, decision log writer | Writes the placement entry |
| RW-TEAMMGR, team manager | Holds Queue and allocation CRUA; reads placed cases in team queues |
| RW-COE, center of excellence analyst | Requests a caller entry in the approved callers list |
| RW-RISK, risk and model risk officer | Approves a caller entry before it is loaded |
| RW-PLATADM, platform administrator | Switches the feature flag on after approval |
| RW-SECADM, security administrator | Loads the permission matrix version that grants the caller's identity Queue and allocation C |
| No approval level from the delegation of authority applies | A placement moves work; it does not approve a treatment |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-005 | recovery_case | status | Read and write |
| DF-CAS-009 | recovery_case | owner_user_id | Write |
| DF-CAS-010 | recovery_case | queue_id | Read and write |
| DF-CAS-011 | recovery_case | team_code | Write |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-022 | recovery_case | closed_date | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-006 | queue | assignment_method | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-008 | queue | overflow_queue_id | Read |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |
| DF-REF-042 | permission | capability_area | Read |
| DF-REF-043 | permission | letters | Read |

The service identity of the caller is written to the standard column created_by of the assignment and to updated_by of the case. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /api/recovery/v1/queues/{queueId}/placements** (operationId postQueuesQueueidPlacements)

| Item | Value |
|---|---|
| Path | queueId (uuid) |
| Request | PlacementRequest: caseId (uuid, required), reason (text, required, 1 to 1,000 characters), modelOrAgent (required, a caller code in the approved list), version (required, 1 to 40 characters) |
| Response 201 | Assignment of the new owner. When every owner is at the cap no owner is set; the response is then the placement result with the overflow queue ID and no assignment (response change recorded in the additions file) |
| 401 | No valid session (MSG-P4-001) |
| 403 | Identity lacks Queue and allocation C (MSG-P4-002) |
| 404 | Flag off (MSG-P2-025); queue or case not found (MSG-P4-003) |
| 409 | Case already in the queue (MSG-P2-024), case closed (MSG-P3-005), open deviation (MSG-P2-021), version changed (MSG-GEN-004) |
| 422 | Field empty (MSG-GEN-001), length out of range (MSG-GEN-002), caller not approved (MSG-P2-020) |
| 503 | Decision log write failed (MSG-P7-003) |
| Authorization | Queue and allocation, right C; scope All for service identities |
| Idempotency | One placement per case and queue while the case is in that queue; a repeat returns 409 MSG-P2-024 and writes nothing |
| Events published | EV-02 CaseAllocated; EV-04 CaseTransferred when the case had an owner; both through the outbox in the same transaction |

**Interfaces called**

```java
// P7, package recovery.decision.writer (RWB-E1-027); Propagation.MANDATORY
DecisionLogEntryRef DecisionLogWriter.write(DecisionLogRecord record)
    throws DecisionLogRecordInvalidException, DecisionLogUnavailableException;
// P3, package recovery.casewf.allocation (RWB-E1-020); this story adds the method below,
// reusing the owner choice, cap and overflow logic of allocate()
AllocationOutcome AllocationService.assignInQueue(UUID caseId, UUID queueId, String sourceIdentity);
```

### 13. Solution plan

**Package.** The story is in the P2 backlog. The endpoint is P3 in the API specification and the queue and case tables are P3's, so the code is in folder `recovery/casewf/placement`, Java package `<ACE base package>.recovery.casewf.placement`. No front end change.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PlacementController | Controller | Implements postQueuesQueueidPlacements; flag check, validation, error mapping |
| PlacementService | Service | BR1 and BR4 to BR7; the case, the assignment, the events and the decision log entry in one transaction |
| ApprovedCallerList | Service | Reads the approved callers list from the configuration service |
| AllocationService | Published interface | From RWB-E1-020; this story adds assignInQueue for a given queue |
| DecisionLogWriter | Published interface | From RWB-E1-027 |
| PlacementRepository | Repository | Reads and writes recovery_case and assignment with the optimistic lock version |

**Database.** Reads queue; reads and writes recovery_case (status, owner_user_id, queue_id, team_code, version); writes assignment. Adds `CREATE UNIQUE INDEX uk_assignment_open_case ON assignment (case_id) WHERE ended_at IS NULL AND task_id IS NULL` through a migration in the P3 folder, so a case has one open case assignment. No new table.

**Configuration and reference data.** Approved callers list rwb.casewf.placement.approved-callers (empty at go-live, assumed; loaded by RW-REFADM after RW-RISK approval); queue table with methods, caps and overflow queues (DL23); permission matrix version (RW-SECADM); LOV-DECISION value D6.

**Build steps**

1. Regenerate the server interface for postQueuesQueueidPlacements with the result variant for overflow.
2. Write ApprovedCallerList and the controller validation (AC5, AC6) and the flag check (AC4).
3. Write PlacementService with the decision log write in the same transaction and the refusals (AC3, AC7 to AC10).
4. Add AllocationService.assignInQueue and test the cap and overflow (AC2) and the case with an owner (AC12).
5. Add the unique open assignment index and the optimistic lock test (AC11).
6. Add the access test with the matrix in force and the decision log failure test.

**Feature flag.** `rwb.casewf.queue-placement`, default off. Off returns 404 with MSG-P2-025 and touches nothing.

**Done when.** The tests in section 16 pass with the flag on in SIT, and the flag is off in UAT and production at the release.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field is empty | Enter {field}. |
| MSG-GEN-002 | reason or version outside its length | {field} must be between {min} and {max}. |
| MSG-P2-024 | The case is already in the target queue (new) | This case is already in {queue}. |
| MSG-P2-025 | The feature flag is off (new) | Queue placement by models and agents is switched off. |
| MSG-P2-020 | The caller is not in the approved callers list (new) | {caller} is not approved to place cases on queues. |
| MSG-P2-021 | The case has an open deviation (new) | This case has an open deviation and stays with the deviation handler. |
| MSG-P3-005 | The case is closed | This case cannot move to {state} from {current}. |
| MSG-GEN-004 | The case changed during the placement | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Identity lacks Queue and allocation C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Queue or case not found | This case is not in your scope. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. A placed case appears in its queue on SCR-07 Team queues and SCR-02 Case list like any other case; the decision log query (SCR-38) shows the placement entry with the caller and version.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-036-01 | AC1, BR1, BR2 | System | Approved caller MDL-SYN-PRIORITY under SY-AGENT; NEW case |
| TC-E2-036-02 | AC2, BR3 | System | Owners at 150 and 149; then both at 150 |
| TC-E2-036-03 | AC3, BR5 | System | One placement; decision log entry fields checked |
| TC-E2-036-04 | AC4, BR8 | System | Flag off |
| TC-E2-036-05 | AC5, BR1 | System | Caller MDL-SYN-UNLISTED |
| TC-E2-036-06 | AC6 | System | Request with no reason |
| TC-E2-036-07 | AC7, BR7 | System | Same request sent twice |
| TC-E2-036-08 | AC8, BR7 | System | CLOSED case |
| TC-E2-036-09 | AC9, BR4 | System | Case with X2 open |
| TC-E2-036-10 | AC10 | System | Queue ID that does not exist |
| TC-E2-036-11 | AC11 | System | Two placements against one case version |
| TC-E2-036-12 | AC12, BR3 | System | IN_PROGRESS case with owner U-5100 |
| TC-E2-036-13 | Access | Access | SY-AGENT under the production matrix (Queue and allocation R); refused with MSG-P4-002 |
| TC-E2-036-14 | Principle 5 | Resilience | Decision log write forced to fail; 503 MSG-P7-003; case, assignment and outbox unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: approved callers, caps, methods and overflow queues are data.
- No personal data in logs, tests or prompts; the reason text is the caller's code or phrase and holds no customer data.
- No read of another module's tables: the decision log is written through DecisionLogWriter.
- A model or agent never bypasses the allocation engine or the access check.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-017 | A queue accepts a write from a model or an agent with the case and the reason | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-DEV-01 | TC-E2-036-01, TC-E2-036-02, TC-E2-036-06 to TC-E2-036-12 |
| REQ-CWC-018 | A model or agent passes the same permission checks and its write is logged with its version | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-UNI-39 | TC-E2-036-03, TC-E2-036-13, TC-E2-036-14 |
| REQ-CWC-019 | The interface ships behind a feature flag | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-04, TC-E2-036-05 |
| REQ-CWC-020 | Model and rule work in the same queue, in one priority order | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-01 |

### 19. Out of scope

- Score and priority on the placement and queue order by priority (REQ-CWC-020): added with the first approved model consumer, in the epic that switches the flag on.
- The model or agent that calls the interface: the P10 agent runtime stories, for example RWB-E2-028.
- Granting SY-AGENT Queue and allocation C in the production matrix: a permission matrix change under RWB-E1-037.


---

## RWB-E2-028 Case intake agent live at L1 [E3a]

| Item | Value |
|---|---|
| Story key | RWB-E2-028 |
| Epic | E3, release 31 January 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-07 Run the case intake agent at L1 |
| Requirement IDs | REQ-DRI-001, REQ-ACA-005 |
| BRD section | Business Requirements Program, sections 5.7 and 5.4 |
| L3 process | 06 Take over and own the case |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-061, RWB-E1-035, RWB-E1-027, RWB-E2-031 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case intake summary and gap flags shown on the case record for every new case, marked as agent output, with a control to accept, correct or reject it**, so that **I start from a summary instead of reading every file, and the bank measures how often the summary is right**.

### 2. Business rationale

A case owner reads accounts, documents, appraisals and contact points before the first action on a new case. After the shadow results and the approved L1 proposal (RWB-E1-061), the intake summary is shown to the owner, who decides what to do with it. Each accept, correction or rejection is recorded as a decision with the agent and prompt versions (REQ-DRI-001), so acceptance and correction rates are measured by segment. Personal data stays masked in the agent call and in the stored summary (REQ-ACA-005).

### 3. Preconditions

- RWB-E1-061 is done and policy "INTAKE" version "P2" with mode L1 is approved by RW-RISK, valid from 2027-01-25.
- RWB-E1-035 is done: SCR-03 Case record shows the history timeline.
- RWB-E1-027 is done: the P7 DecisionLogWriter is available.
- RWB-E2-031 is done: GET /admin/agent-metrics and SCR-46 show acceptance by segment.
- The case owner holds RW-CASEOWN with Case record CRU and the case is in their scope.

### 4. Flow

1. SY-CASEWF: creates case "RW-2027-000501" and writes EV-01 CaseCreated.
2. System: runs agent "INTAKE" in mode L1 through the orchestrator and stores the summary and gap flags on the agent run.
3. Case owner: opens SCR-03 Case record for the case.
4. System: loads the case record and, without waiting on the model, calls GET /cases/{caseId}/agent-outputs for the stored L1 output.
5. System: shows the panel "Agent summary" with the agent name, the version "INTAKE@P2/PR3", the gap flags with reasons and the controls Accept, Correct and Reject.
6. Case owner: chooses Accept, or Correct or Reject with a reason.
7. System: writes one decision log entry (decision D6, agent version, recommendation reference, final call ACCEPTED, CORRECTED or REJECTED, reason), then stores the feedback on the agent run.
8. System: the panel shows the recorded verdict; the next JOB-15 run counts it in the acceptance and correction rates by segment.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent timed out or failed a guardrail for the case | The case record loads with no summary; the panel shows the message; the miss is on the agent run | MSG-P10-005 | AC3 |
| X2 | The owner corrects or rejects without a reason | Refused with 422; nothing stored | MSG-P7-005 | AC4 |
| X3 | The decision log write fails on feedback | Feedback not stored; panel keeps the controls; incident raised (R-UNI-39) | MSG-P7-003 | AC5 |
| X4 | Feedback already given, or two owners send at once | Second request refused with 409 | MSG-GEN-004 | AC6 |
| X5 | The case is outside the user's scope | Refused with 404 | MSG-P4-003 | AC7 |
| X6 | The agent's mode is SHADOW for the case segment | No output returned; no panel | None to a user | AC8 |
| X7 | The run used data older than the business date | Panel shows the stale warning with the data date | MSG-P1-001 | AC9 |
| X8 | A role without Case record U sends feedback | Refused with 403 | MSG-P4-002 | TC-E2-028-10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the stored runs of RWB-E1-059, the approved L1 policy of RWB-E1-061 and the metrics of RWB-E2-031 |
| Negotiable | Panel layout and wording follow the design system; verdicts and the mode per segment are data |
| Valuable | Saves the owner the first read of every file on a new case and measures the summary's accuracy |
| Estimable | Two endpoints, one panel, one decision log mapping, one migration |
| Small | One back end and one front end developer for two weeks |
| Testable | Each criterion is a system or browser test with synthetic cases |

### 7. Acceptance criteria

```gherkin
Feature: Case intake agent live at L1 [E3a]

  Background:
    Given policy "INTAKE" version "P2" with mode "L1" and prompt "PR3" is in force from 2027-01-25
    Given case owner "owner.user07" holds RW-CASEOWN and owns case "RW-2027-000501"

  Scenario: AC1 Summary shown
    Given a new case "RW-2027-000501" with an ANSWERED intake run and gap flags MISSING_DOCUMENT and NO_VALID_APPRAISAL
    When the case record view loads
    Then the panel "Agent summary" shows the summary, the two gap flags with reasons, agent "INTAKE", version "INTAKE@P2/PR3" and the marker "Agent output"
    Then the controls Accept, Correct and Reject are shown
    Then the case record loads in under 2 seconds whether or not the panel has data

  Scenario: AC2 Acceptance measured
    Given a month of summaries in January 2027 for segment MORTGAGE and BKK: 300 with feedback, 240 accepted, 45 corrected and 15 rejected
    When the dashboard refreshes after JOB-15
    Then SCR-46 shows for "INTAKE" and MORTGAGE/BKK acceptance rate 0.8000 and correction rate 0.1500
    Then each feedback has one decision log entry with decision "D6" and agent version "INTAKE@P2/PR3"

  Scenario: AC3 Fallback
    Given the agent timed out for case "RW-2027-000502"
    When the view loads
    Then the case shows without a summary and the panel shows MSG-P10-005
    Then the agent run holds status "TIMED_OUT" and fallback true

  Scenario: AC4 Correction without a reason
    When "owner.user07" chooses Correct on case "RW-2027-000501" with an empty reason
    Then the system refuses the request with 422 and MSG-P7-005
    Then no decision log entry and no feedback are stored

  Scenario: AC5 The decision cannot be recorded
    Given the decision log writer fails
    When "owner.user07" chooses Accept
    Then the system refuses the request with 503 and MSG-P7-003
    Then no agent_feedback row exists for the run and the controls stay on the panel

  Scenario: AC6 Feedback given twice
    Given "owner.user07" accepted the summary of case "RW-2027-000501"
    When a second feedback request for the same run arrives
    Then the system refuses it with 409 and MSG-GEN-004
    Then one decision log entry exists for the run

  Scenario: AC7 A case outside the user's scope
    Given case "RW-2027-000601" belongs to team "HP-NE" outside the scope of "owner.user07"
    When "owner.user07" requests GET /cases/{caseId}/agent-outputs for it
    Then the system refuses the request with 404 and MSG-P4-003

  Scenario: AC8 A segment still in shadow
    Given the INTAKE policy for segment UNSECURED is mode "SHADOW"
    When the owner opens unsecured case "RW-2027-000701"
    Then GET /cases/{caseId}/agent-outputs returns an empty list and no panel is shown

  Scenario: AC9 Stale input
    Given the run for case "RW-2027-000503" used data as of 2027-01-26 and the business date is 2027-01-28
    When the view loads
    Then the panel shows MSG-P1-001 with the date 2027-01-26 above the summary
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only runs in mode L1 for the case segment are returned to a user; shadow output is never returned | agent_policy.autonomy_mode, segment fields (New) |
| BR2 | Agent output is marked "Agent output" with the agent name and version | REQ-DRI-001; labels "Agent version" |
| BR3 | Feedback writes one decision log entry before it is stored: decision D6 (LOV-DECISION, assumed code), agent version, recommendation reference, final call, reason | Principle 5; R-UNI-39; CTL-06 |
| BR4 | A correction or a rejection needs a reason | CTL-07; MSG-P7-005 |
| BR5 | One feedback per run and item; the intake summary is item "SUMMARY" | agent_feedback unique key (New) |
| BR6 | The case record never waits for the model; the panel reads stored output | NFR-009; R-UNI-32 |
| BR7 | The summary holds masking tokens only | CTL-11 |

### 9. State transitions

None. This story does not change a case status. It writes one agent_feedback row (verdict ACCEPTED, CORRECTED or REJECTED) and one decision log entry per feedback.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Reads the panel for cases in scope (Case record R); gives feedback (Case record U) |
| RW-TEAMMGR | Reads the panel for team cases (Case record R); no feedback |
| SY-AGENT | Runs the agent (read only) |
| SY-DECLOG | Writes the entry |
| RW-COE | Reads acceptance on SCR-46 (Platform administration R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-011 | recovery_case | team_code | Read (scope) |
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-WRK-012 | assignment | assignee_user_id | Read (owner check through P3) |
| DF-DOC-004 | document | document_type | Read (gap reasons) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (through the P7 DecisionLogWriter) |
| DF-AGT-036 | agent_run | id | Read |
| DF-AGT-037 | agent_run | agent_code | Read |
| DF-AGT-038 | agent_run | agent_version | Read |
| DF-AGT-043 | agent_run | autonomy_mode | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-049 | agent_run | output | Read |
| DF-AGT-050 | agent_run | confidence | Read |
| DF-AGT-055 | agent_run | data_as_of | Read |
| DF-AGT-056 | agent_run | run_at | Read |
| DF-AGT-097 | agent_feedback | id | Write |
| DF-AGT-098 | agent_feedback | agent_run_id | Write |
| DF-AGT-099 | agent_feedback | item_key | Write |
| DF-AGT-100 | agent_feedback | verdict | Write |
| DF-AGT-101 | agent_feedback | reason | Write |
| Standard column | agent_feedback | created_by | Write |
| Standard column | agent_feedback | created_at | Write |
| DF-AGT-102 | agent_feedback | decision_log_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/cases/{caseId}/agent-outputs** (new, see additions)
- Request: path caseId (uuid).
- Response: 200, array of AgentOutput (runId, agent, agentVersion, mode "L1", status, summary, gaps[{gapType, reason}], confidence, dataAsOf, feedback). Empty array when no L1 output exists.
- Errors: 401; 403 (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 503.
- Authorization: Case record, R, scope applied. Idempotency: read only.

**POST /api/recovery/v1/agent-runs/{runId}/feedback** (new)
- Request: AgentFeedbackRequest (itemKey, default "SUMMARY"; verdict ACCEPTED, CORRECTED or REJECTED; reason, required for CORRECTED and REJECTED, at most 1,000 characters); header If-Match with the run row version.
- Response: 200 AgentOutput with feedback set.
- Errors: 401; 403; 404; 409 feedback exists or row changed (MSG-GEN-004); 422 reason missing (MSG-P7-005); 503 decision not recorded (MSG-P7-003).
- Authorization: Case record, U, scope applied. Idempotency: one feedback per run and item (itemKey, default "SUMMARY"); a repeat returns 409.

**Decision log mapping:** case_id; decision_code "D6"; agent_version "INTAKE@P2/PR3"; model_version; inputs_ref = agent run reference; recommendation = {"runId", "gaps"}; final_call = verdict; override_reason = reason; approver_user_id = the owner.

**Events:** EV-01 CaseCreated consumed; EV-28 AgentRunCompleted published by the orchestrator; EV-08 DecisionRecorded published by P7.

### 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/intake/`; front end `src/modules/recovery/agent/intake/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAgentOutputController | Controller | GET /cases/{caseId}/agent-outputs and POST /agent-runs/{runId}/feedback |
| AgentFeedbackService | Service | Validates, writes the decision log entry, then stores feedback in one transaction |
| AgentOutputQueryService | Service | Returns L1 outputs for a case after the P3 scope check |
| IntakeShadowListener | Listener | Extended: uses the mode of the policy in force for the segment (SHADOW or L1) |
| AgentSummaryPanel | React component | Panel on SCR-03 with marker, version, gaps, controls and states |

**Database:** migration `V10_008__agent_feedback.sql` creates agent_feedback (id, agent_run_id, item_key varchar(20), verdict varchar(10), reason varchar(1000), created_by uuid, created_at timestamptz, decision_log_id uuid, standard record columns) with unique (agent_run_id, item_key) and check verdict in ('ACCEPTED','CORRECTED','REJECTED').

**Configuration and reference data:** policy INTAKE P2 (mode L1 per segment) loaded by RW-COE and approved by RW-RISK; panel labels in the label standard (DL10 for Thai).

**Build steps**
1. Create the agent_feedback table with its unique key and check constraint.
2. Build AgentOutputQueryService with the P3 scope check and the mode filter (AC1, AC7, AC8).
3. Build AgentFeedbackService with the decision log write first (AC2, AC4, AC5, AC6).
4. Build CaseAgentOutputController and the problem responses.
5. Build AgentSummaryPanel: loading, empty, unavailable (MSG-P10-005), stale (MSG-P1-001), feedback given (AC1, AC3, AC9).
6. Browser test: case record load time with the panel under 2 seconds on 50 documents.

**Feature flag:** `rwb.agent.intake-l1`. Off: GET /cases/{caseId}/agent-outputs returns an empty list and the panel is hidden.

**Done when:** the tests in section 16 pass and SCR-46 shows acceptance by segment for the UAT cases.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-005 | No L1 summary for the case because the run failed | The agent summary is not available for this case. Work from the case record. |
| MSG-P7-005 | Correct or Reject with no reason | Enter the reason you are not following the recommendation. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | Feedback already given or row changed | Someone else changed this record. Reload it to see their change. |
| MSG-P4-003 | Case outside scope | This case is not in your scope. |
| MSG-P1-001 | Summary built on stale data | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-03 Case record (states loading, read only, editable, on hold) gains the panel "Agent summary". Panel states: loading (skeleton), empty (no panel when no L1 output), unavailable (MSG-P10-005), stale (MSG-P1-001 above the summary), ready (summary, gaps, Accept, Correct, Reject), recorded (verdict and date, no controls). In the read only state of SCR-03 the controls are hidden. SCR-46 Agent monitor (state live) shows the acceptance and correction rates.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-028-01 | AC1, BR1, BR2, BR6 | System | Case RW-2027-000501 with an ANSWERED run and two gaps |
| TC-E2-028-02 | AC2, BR3 | System | January 2027, MORTGAGE/BKK: 300 feedback, 240, 45, 15 |
| TC-E2-028-03 | AC3, BR6 | System | Case RW-2027-000502 with a TIMED_OUT run |
| TC-E2-028-04 | AC4, BR4 | System | Correct with an empty reason |
| TC-E2-028-05 | AC5, BR3 | System | Decision log writer fails on Accept |
| TC-E2-028-06 | AC6, BR5 | System | Second feedback on the same run |
| TC-E2-028-07 | AC7 | System | Case RW-2027-000601 in team HP-NE |
| TC-E2-028-08 | AC8, BR1 | System | Unsecured case RW-2027-000701, segment in SHADOW |
| TC-E2-028-09 | AC9 | System | Data as of 2027-01-26, business date 2027-01-28 |
| TC-E2-028-10 | Access | Access | RW-PHONECOL (Case record R only) sends feedback; refused with MSG-P4-002 |
| TC-E2-028-11 | Principle 5 | Resilience | Decision log write forced to fail on feedback; no feedback stored; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the mode per segment and the verdict list are data.
- No personal data in logs, tests or prompts; the summary shows masking tokens.
- No read of another module's tables; scope and owner come through the P3 interface.
- Agent output never changes the case: no status, task or field is set from the summary.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records the agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-32, R-UNI-39 | TC-E2-028-01, TC-E2-028-02, TC-E2-028-03, TC-E2-028-04, TC-E2-028-05, TC-E2-028-06, TC-E2-028-09, TC-E2-028-11 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Business Requirements Program, section 5.4 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E2-028-07, TC-E2-028-08, TC-E2-028-10 |

### 19. Out of scope

- Agent actions taken without the owner (autonomy L2 and above, Epic 8).
- Editing the summary text in the Workbench; a correction records the reason only.
- Intake document classification (P5 stories).


---

## RWB-E2-029 Deviation screening agent evaluation and L1 on one segment [E3b]

| Item | Value |
|---|---|
| Story key | RWB-E2-029 |
| Epic | E3, release 31 January 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-DVH-07 Screen for deviations with the agent at L1 on one segment; FEAT-AGT-08 Run the deviation screening agent at L1 |
| Requirement IDs | REQ-DVH-001, REQ-DVH-006 |
| BRD section | Business Requirements Program, section 5.15 |
| L3 process | 11 Handle customer care and deviations |
| Decision | X1 to X7 |
| Priority | Must |
| Depends on | RWB-E1-062, RWB-E2-015, RWB-E1-061, RWB-E2-028 |
| Status | Ready for build |

### 1. Story

As a **conduct and QA officer (RW-CONDUCT)**, I want **the deviation screening agent scored on 500 shadow cases and switched to L1 for Mortgage cases in Bangkok, with its proposed X flags shown to the case owner to confirm or reject**, so that **deviations on that segment are flagged from the first day a sign appears and the error rate per flag is known**.

### 2. Business rationale

A deviation found weeks late means contact that should have stopped and clocks that should have paused. The shadow results of RWB-E1-062 give a measured precision and recall per code. This story scores a larger shadow run, records the proposal to go to L1 on one segment, and then shows the agent's proposals to the owner of each Mortgage case in Bangkok, who confirms or rejects each one. A confirmed proposal raises the deviation through the S8 deviation service, so the flag shows on the case and in every queue (REQ-DVH-006), and detection draws on case data, call notes and documents (REQ-DVH-001). Every other segment stays in shadow.

### 3. Preconditions

- RWB-E1-062 is done: SCREENING runs in shadow and scores per code.
- RWB-E2-015 is done: the S8 deviation service raises a deviation, applies R-DEV-01 and shows the flag on SCR-03 and the queues.
- RWB-E1-061 is done: the L1 proposal checks exist in the policy loader.
- RWB-E2-028 is done: GET /cases/{caseId}/agent-outputs, POST /agent-runs/{runId}/feedback and agent_feedback exist.
- Sample "SCREEN-S2" version 1 holds the business analysts' review of 500 shadow cases.
- The case owner holds RW-CASEOWN (Case record CRU) and the case is in scope.

### 4. Flow

1. RW-COE: starts the evaluation of "SCREENING" on "SCREEN-S2" version 1.
2. System: stores precision and recall per code X1 to X7 with sample size 500.
3. RW-COE: loads policy "SCREENING" version "P2" with mode L1 for segment MORTGAGE and BKK, the evaluation run, the conditions, the fallback and the measures; RW-RISK approves it.
4. System: on EV-01 or EV-16 for a Mortgage case in region BKK, runs SCREENING in mode L1; for any other segment, runs it in shadow.
5. Case owner: opens SCR-03 Case record; the panel "Proposed deviations" lists each proposed code with reasons, sources, confidence and the marker "Agent output".
6. Case owner: confirms a proposal; the system calls the S8 deviation service, which raises the deviation with raised_by SCREENING_AGENT and applies R-DEV-01.
7. System: stores feedback ACCEPTED for that code, linked to the decision log entry S8 wrote.
8. Case owner: rejects a proposal with a reason; the system writes a decision log entry with final call REJECTED and stores feedback REJECTED.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case is not Mortgage in region BKK | The run is in shadow; nothing is shown | None to a user | AC3 |
| X2 | Reject with no reason | Refused with 422 | MSG-P7-005 | AC5 |
| X3 | A proposal is below the confidence floor 0.80 | Shown with the marker "Low confidence" | None to a user | AC6 |
| X4 | The proposed code is already open on the case | The proposal is not shown | None to a user | AC7 |
| X5 | Two confirmations of the same proposal at once | One deviation; the second is refused with 409 | MSG-GEN-004 | AC8 |
| X6 | The decision log write fails on a rejection | Nothing stored; incident raised (R-UNI-39) | MSG-P7-003 | AC9 |
| X7 | The L1 proposal names scores below a stated condition | Policy load refused | MSG-P10-001 | AC10 |
| X8 | A role without Case record U confirms or rejects | Refused with 403 | MSG-P4-002 | TC-E2-029-11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reuses the screening agent (RWB-E1-062), the deviation service (RWB-E2-015) and the output and feedback endpoints (RWB-E2-028) |
| Negotiable | The segment, the floor and the conditions are values in the policy row |
| Valuable | Flags deviations on Mortgage cases in Bangkok when the sign appears, with a person deciding each one |
| Estimable | One panel, one confirm path through S8, one reject path, one evaluation |
| Small | Two developers for two weeks |
| Testable | Each criterion runs on synthetic cases in two segments |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent evaluation and L1 on one segment [E3b]

  Background:
    Given policy "SCREENING" version "P2" with prompt "PR2" has mode "L1" for segment MORTGAGE and BKK and mode "SHADOW" for every other segment
    Given case owner "owner.user07" holds RW-CASEOWN

  Scenario: AC1 Evaluation
    Given the shadow run on 500 cases in sample "SCREEN-S2" version 1
    When the evaluation runs
    Then precision and recall per flag X1 to X7 are stored with sample size 500
    Then for X1 with 41 true positives, 4 false positives and 5 false negatives precision is 0.9111 and recall is 0.8913
    Then the system records the L1 proposal as policy "SCREENING" version "P2" with status "LOADED", segment MORTGAGE and BKK and the evaluation run ID

  Scenario: AC2 L1 on one segment
    Given Mortgage case "RW-2027-000801" in region BKK and a complaint note on 2027-01-26
    When the agent runs
    Then the panel "Proposed deviations" shows X1 with its reasons, the preceding contact and the marker "Agent output"
    Then when the owner confirms X1 the S8 service raises deviation X1 with raised_by "SCREENING_AGENT" under rule R-DEV-01
    Then the case status becomes "On hold" and agent_feedback holds verdict "ACCEPTED" for item "X1" with the S8 decision log entry ID

  Scenario: AC3 Other segments
    Given hire purchase case "RW-2027-000802" in region BKK
    When the agent runs
    Then the result stays in shadow and GET /cases/{caseId}/agent-outputs returns no screening output

  Scenario: AC4 The owner rejects a proposal
    Given the agent proposes X6 on case "RW-2027-000801"
    When the owner rejects X6 with reason "Customer answered on 2027-01-25"
    Then one decision log entry holds decision "X6", agent version "SCREENING@P2/PR2", final call "REJECTED" and the reason
    Then the system raises no deviation and agent_feedback holds "REJECTED" for item "X6"

  Scenario: AC5 Reject without a reason
    When the owner rejects X6 with an empty reason
    Then the system refuses the request with 422 and MSG-P7-005

  Scenario: AC6 A low-confidence proposal
    Given the agent proposes X2 with confidence 0.72 on case "RW-2027-000803"
    When the panel loads
    Then X2 shows with the marker "Low confidence"

  Scenario: AC7 A code already open
    Given deviation X1 is open on case "RW-2027-000801"
    When the agent proposes X1 again
    Then the panel does not show X1

  Scenario: AC8 Two confirmations at once
    Given two sessions of "owner.user07" confirm X1 on case "RW-2027-000804" at the same time
    When both requests arrive
    Then one deviation X1 exists and the second request is refused with 409 and MSG-GEN-004

  Scenario: AC9 The rejection cannot be recorded
    Given the decision log writer fails
    When the owner rejects X6 with a reason
    Then the system refuses the request with 503 and MSG-P7-003 and no agent_feedback row exists

  Scenario: AC10 A proposal with scores below its condition
    Given X4 has recall 0.6000 in the evaluation of "SCREEN-S2"
    When RW-COE loads an L1 proposal with condition "recall at least 0.75 for every code"
    Then the system refuses the load with 422 and MSG-P10-001 naming "X4 recall 0.6000 below 0.75"
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Mode L1 applies only where the case product group and region match the policy segment; elsewhere the mode is SHADOW | agent_policy.segment_product_group, segment_region_code (New) |
| BR2 | The agent raises nothing itself; a deviation is raised only when a person confirms the proposal | Agent catalog, screening agent "May decide alone: Nothing"; role SY-AGENT has no Case record U |
| BR3 | A confirmed proposal is raised through S8 with raised_by SCREENING_AGENT, and R-DEV-01 pauses the stage clock and routes the case | R-DEV-01; LOV-RAISED-BY |
| BR4 | A rejection needs a reason and writes a decision log entry before the feedback is stored | CTL-07; Principle 5; R-UNI-39 |
| BR5 | A proposal for a code already open is not shown | deviation.deviation_code |
| BR6 | A proposal below the floor 0.80 is shown with the marker "Low confidence" | agent_policy.confidence_floor (New); FEAT-DVH-08 |
| BR7 | An L1 proposal must meet its stated conditions on the named evaluation | Principle 1; CTL-08 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ANY_STATE | DEVIATION_FLAGGED | The owner confirms a proposal; deviation_code in X1 to X7 (R-DEV-01, applied by S8) | DEV_FLAGGED |
| New, Assigned, In progress, any Waiting | Deviation flagged | As above | On hold |

A rejected proposal changes no case status.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Reads proposals for cases in scope (Case record R); confirms or rejects (Case record U) |
| SY-AGENT | Runs the agent (read only) |
| S8 deviation service, under the owner's identity | Raises the deviation and writes its decision log entry |
| RW-COE | Runs the evaluation and loads the L1 proposal (Rules and parameters C) |
| RW-RISK | Approves the L1 proposal (Rules and parameters A) |
| RW-CONDUCT | Reads scores (Rules and parameters R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-CAS-037 | deviation | case_id | Write (through the S8 interface) |
| DF-CAS-038 | deviation | deviation_code | Write (through the S8 interface) |
| DF-CAS-040 | deviation | raised_by | Write (through the S8 interface) |
| DF-WRK-012 | assignment | assignee_user_id | Read (owner check through P3) |
| DF-COL-025 | valuation | appraisal_date | Read (X7 collateral event inputs) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (rejections, through the P7 DecisionLogWriter) |
| DF-AGT-036 | agent_run | id | Read |
| DF-AGT-038 | agent_run | agent_version | Read |
| DF-AGT-043 | agent_run | autonomy_mode | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-049 | agent_run | output | Read |
| DF-AGT-050 | agent_run | confidence | Read |
| DF-AGT-059 | agent_run | segment_product_group | Read |
| DF-AGT-060 | agent_run | segment_region_code | Read |
| DF-AGT-098 | agent_feedback | agent_run_id | Write |
| DF-AGT-099 | agent_feedback | item_key | Write |
| DF-AGT-100 | agent_feedback | verdict | Write |
| DF-AGT-101 | agent_feedback | reason | Write |
| Standard column | agent_feedback | created_by | Write |
| Standard column | agent_feedback | created_at | Write |
| DF-AGT-102 | agent_feedback | decision_log_id | Write |
| DF-AGT-003 | agent_policy | policy_version | Write |
| DF-AGT-008 | agent_policy | autonomy_mode | Write |
| DF-AGT-009 | agent_policy | segment_product_group | Write |
| DF-AGT-010 | agent_policy | segment_region_code | Write |
| DF-AGT-017 | agent_policy | evaluation_run_id | Write |
| DF-AGT-018 | agent_policy | promotion_conditions | Write |
| DF-AGT-089 | agent_evaluation | label_key | Write |
| DF-AGT-090 | agent_evaluation | sample_size | Write |
| DF-AGT-095 | agent_evaluation | precision_value | Write |
| DF-AGT-096 | agent_evaluation | recall_value | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**GET /api/recovery/v1/cases/{caseId}/agent-outputs** (new, RWB-E2-028): returns AgentOutput items for SCREENING in mode L1 with proposals[{code, reasons, sourceRefs, precedingContactId, confidence, lowConfidence, feedback}]; Case record R; errors 401, 403, 404 (MSG-P4-003), 503.

**POST /api/recovery/v1/agent-runs/{runId}/feedback** (new, RWB-E2-028): AgentFeedbackRequest with itemKey = the code (for example "X1"), verdict ACCEPTED or REJECTED, reason (required for REJECTED); 200 AgentOutput; errors 401, 403, 404, 409 (MSG-GEN-004), 422 (MSG-P7-005), 503 (MSG-P7-003); Case record U; one feedback per run and item.

**Published interface called on ACCEPTED:**

```java
// S8, from RWB-E2-015
DeviationRaised DeviationService.raise(UUID caseId, String deviationCode, String reason,
                                       List<UUID> documentIds, String raisedBy, UUID agentRunId);
// returns deviationId and decisionLogEntryId
```

**POST /api/recovery/v1/admin/agent-evaluations** and **POST /api/recovery/v1/admin/agent-configs** (new, RWB-E1-058): evaluation of SCREEN-S2 and the L1 proposal; Rules and parameters C; approval through POST /admin/agent-configs/{versionId}/approve, Rules and parameters A.

**Events:** EV-01 CaseCreated and EV-16 DocumentStored consumed; EV-28 AgentRunCompleted published; EV-06 DeviationRaised published by S8 on confirmation.

### 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/screening/`; front end `src/modules/recovery/agent/screening/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ScreeningShadowListener | Listener | Extended: mode per segment from the policy in force |
| ScreeningFeedbackHandler | Service | ACCEPTED: calls DeviationService.raise, stores feedback with the S8 entry ID; REJECTED: writes the decision log entry, then feedback |
| ScreeningOutputFilter | Service | Removes proposals for codes already open; sets lowConfidence |
| ProposedDeviationsPanel | React component | Panel on SCR-03: code, reasons, sources, confidence, Confirm and Reject with reason |
| AgentFeedbackService | Service | Extended with item keys for codes |

**Database:** no new table; uses agent_feedback (RWB-E2-028) and agent_policy segment fields (RWB-E1-058).

**Configuration and reference data:** policy SCREENING P2 with segment MORTGAGE and BKK, loaded by RW-COE, approved by RW-RISK; sample SCREEN-S2 loaded by RW-COE.

**Build steps**
1. Run the evaluation on SCREEN-S2 and load the L1 proposal in SIT (AC1, AC10).
2. Extend the listener for the mode per segment (AC2, AC3).
3. Build ScreeningOutputFilter (AC6, AC7).
4. Build ScreeningFeedbackHandler for both verdicts with the decision log first on rejection (AC2, AC4, AC5, AC9).
5. Add the unique key test for parallel confirmations (AC8).
6. Build ProposedDeviationsPanel with the common states.

**Feature flag:** `rwb.agent.screening-l1`. Off: every segment runs in shadow and the panel is hidden.

**Done when:** the tests in section 16 pass and UAT confirms the panel on Mortgage cases in Bangkok only.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-005 | Reject without a reason | Enter the reason you are not following the recommendation. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | Second confirmation of the same proposal | Someone else changed this record. Reload it to see their change. |
| MSG-P10-001 | L1 proposal fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-S8-001 | Deviation raised after confirmation | {deviation} was raised. The case is with {handler}. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-03 Case record gains the panel "Proposed deviations" with states: empty (no panel), ready (proposals with Confirm and Reject), low confidence (marker on the proposal), recorded (verdict and date). After a confirmation SCR-03 shows the on hold banner of the deviation, and SCR-08 Deviation queue lists it for the named handler. SCR-46 Agent monitor shows SCREENING as live for MORTGAGE/BKK and Shadow elsewhere.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-029-01 | AC1, BR7 | System | SCREEN-S2 version 1, 500 cases; X1 counts 41, 4, 5 |
| TC-E2-029-02 | AC2, BR1, BR2, BR3 | System | Mortgage case RW-2027-000801 in BKK, complaint note 2027-01-26 |
| TC-E2-029-03 | AC3, BR1 | System | Hire purchase case RW-2027-000802 in BKK |
| TC-E2-029-04 | AC4, BR4 | System | Reject X6 with a reason |
| TC-E2-029-05 | AC5, BR4 | System | Reject X6 with an empty reason |
| TC-E2-029-06 | AC6, BR6 | System | X2 with confidence 0.72 |
| TC-E2-029-07 | AC7, BR5 | System | X1 already open on the case |
| TC-E2-029-08 | AC8 | System | Two parallel confirmations of X1 |
| TC-E2-029-09 | AC9, BR4 | System | Decision log writer fails on rejection |
| TC-E2-029-10 | AC10, BR7 | System | X4 recall 0.6000, condition 0.75 |
| TC-E2-029-11 | Access | Access | RW-PHONECOL confirms X1; refused with MSG-P4-002 |
| TC-E2-029-12 | Principle 5 | Resilience | Decision log write forced to fail on a rejection; nothing stored; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the segment, floor and conditions are policy values.
- No personal data in logs, tests or prompts; reasons shown on the panel hold masking tokens.
- No read of another module's tables; deviations are raised only through the S8 interface.
- The agent never raises a deviation without a person's confirmation.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Business Requirements Program, section 5.15 | FEAT-AGT-08, FEAT-DVH-07 | 11 Handle customer care and deviations | R-UNI-39 | TC-E2-029-01, TC-E2-029-03, TC-E2-029-04, TC-E2-029-05, TC-E2-029-06, TC-E2-029-09, TC-E2-029-10, TC-E2-029-12 |
| REQ-DVH-006 | A deviation flag is visible on the case and in every queue | Business Requirements Program, section 5.15 | FEAT-DVH-07 | 11 Handle customer care and deviations | R-DEV-01 | TC-E2-029-02, TC-E2-029-07, TC-E2-029-08, TC-E2-029-11 |

### 19. Out of scope

- L1 on further segments (a later policy version; FEAT-AGT-12, Epic 3).
- The deviation flows after the flag (S8, Epic 7).
- The agent handling X6 and X7 within policy (R-DEV-06, Epic 7).


---

## RWB-E2-030 Legal document agent in shadow on Epic 1 data [E3c]

| Item | Value |
|---|---|
| Story key | RWB-E2-030 |
| Epic | E3, release 31 January 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-09 Run the legal document agent in shadow |
| Requirement IDs | REQ-S4-002 |
| BRD section | Business Requirements Program, section 5.11 |
| L3 process | 8.2 Instruct and file |
| Decision | D7.2 |
| Priority | Should |
| Depends on | RWB-E1-058, RWB-E2-025, RWB-E1-061 |
| Status | Ready for build |

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the legal document agent to assemble litigation packs and completeness lists in shadow on real Epic 1 cases, scored against the packs the legal officers built**, so that **the agent goes to Epic 5 with a known accuracy per pack item**.

### 2. Business rationale

A litigation pack that reaches the law firm with a missing or defective document is returned, and the filing waits. From Epic 5 the legal document agent assembles the pack and checks it against the defect list before the officer verifies it (R-LIT-16, R-LIT-17, CTL-19). This story runs the agent in shadow on 50 cases whose packs the officers have already built, scores agreement per checklist item, and records the decision to promote or keep it in shadow as a policy version. It serves REQ-S4-002: a pack assembled and checked against the document checklist, with missing documents named.

### 3. Preconditions

- RWB-E1-058 is done: platform, sample loader and evaluation harness.
- RWB-E2-025 is done: court filings, hearing notices, judgments, contracts and mortgage documents are classified and their fields extracted.
- RWB-E1-061 is done: the policy loader checks a promotion proposal against its evaluation.
- The document checklist per case type is loaded as reference data (RWB-E1-040).
- Approved policy "LEGAL_DOC" version "P1": mode SHADOW, timeout 60 seconds, allowed tools read_case, read_legal_actions, read_documents, read_document_fields, read_checklist; output schema "legal-pack-v1".
- Sample "LEGAL-S1" version 1: for 50 Epic 1 litigation cases, the officers' pack, one row per case and checklist item with expected status PRESENT, MISSING or DEFECT.

### 4. Flow

1. RW-COE: loads sample "LEGAL-S1" and starts the evaluation of "LEGAL_DOC" through POST /admin/agent-evaluations.
2. System: for each sample case, runs the agent in shadow: reads the case, the legal action, the documents with their fields and the checklist for the case type.
3. System: checks the answer: every checklist item has a status, every document ID belongs to the case, and every DEFECT has a reason.
4. System: stores the pack (document IDs per item) and the completeness list on the agent run; nothing is shown to a user and no document, pack or legal action changes.
5. System: scores agreement with the officers' pack per checklist item and stores it with sample size.
6. RW-COE: reads the scores and loads policy version "P2": mode L1 with conditions to promote, or mode SHADOW with a review date to keep shadow.
7. RW-RISK: approves the version; the decision and its date are recorded on the policy row.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent names a document that belongs to another case | Check SCHEMA_RULE fails; run GUARDRAIL_FAILED; scored as wrong for every item | None to a user | AC4 |
| X2 | A checklist item has no status in the answer | Check SCHEMA fails | None to a user | AC5 |
| X3 | The document interface is unavailable during a run | Run status TOOL_UNAVAILABLE, fallback true; the case is scored as not run and listed (R-UNI-33) | None to a user | AC6 |
| X4 | Fewer than 50 scored cases | A promotion to L1 is refused; keeping shadow is allowed | MSG-P10-001 | AC7 |
| X5 | Keep shadow without a review date | Load refused | MSG-P10-001 | AC8 |
| X6 | The loader approves their own decision | Refused with 409 | MSG-P7-002 | AC9 |
| X7 | A role without the right | Refused with 403 | MSG-P4-002 | TC-E2-030-10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the platform and harness; reads S4 and P5 data through their interfaces; no S4 workflow is needed |
| Negotiable | Checklist items come from reference data; the minimum sample and conditions are policy values |
| Valuable | Gives the item accuracy that decides whether the agent assembles packs in Epic 5 |
| Estimable | One prompt, one output schema, one scorer, one proposal |
| Small | One developer and one litigation officer for review |
| Testable | Each criterion runs on fixture cases with known officer packs |

### 7. Acceptance criteria

```gherkin
Feature: Legal document agent in shadow on Epic 1 data [E3c]

  Background:
    Given policy "LEGAL_DOC" version "P1" with mode "SHADOW" and prompt "PR1"
    Given the checklist for case type "MORTGAGE_CIVIL" has 9 items including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF"

  Scenario: AC1 Shadow pack
    Given litigation case "RW-2026-000901" with 14 documents and an open legal action
    When the agent runs
    Then a pack listing document IDs for each of the 9 items and a completeness list with PRESENT, MISSING or DEFECT per item are stored on the agent run
    Then no document, legal action, task or case field changes
    Then no user-facing endpoint returns the pack

  Scenario: AC2 Scored
    Given 50 shadow packs for sample "LEGAL-S1" version 1
    When the evaluation runs
    Then the system stores agreement with the officers' packs per item with sample size 50
    Then for "DEMAND_NOTICE_PROOF" with 46 agreeing cases the agreement rate is 0.9200

  Scenario: AC3 Promotion proposal
    Given the score
    When RW-COE loads policy "LEGAL_DOC" version "P2" with mode "SHADOW", review date 2027-03-15 and the evaluation run ID, and RW-RISK approves it
    Then the system records the decision to keep shadow on version "P2" with the approver and the approval date
    Then the system accepts a proposal with mode "L1" only when every stated condition is met by the evaluation

  Scenario: AC4 A document from another case
    Given the model stub names document "D-7001" of case "RW-2026-000902" in the pack of case "RW-2026-000901"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED" and check "SCHEMA_RULE"

  Scenario: AC5 An item without a status
    Given the answer has no status for item "MORTGAGE_DEED"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED" and check "SCHEMA"

  Scenario: AC6 The document interface is down
    Given the P5 document interface is unavailable for case "RW-2026-000903"
    When the agent runs
    Then the run holds status "TOOL_UNAVAILABLE" and fallback true
    Then the evaluation lists the case as not run and scores 49 cases

  Scenario: AC7 Too few cases to promote
    Given the evaluation scored 49 cases
    When RW-COE loads a proposal with mode "L1"
    Then the system refuses the load with 422 and MSG-P10-001 naming check "sample size at least 50"

  Scenario: AC8 Keep shadow without a review date
    When RW-COE loads version "P2" with mode "SHADOW" and no review date
    Then the system refuses the load with 422 and MSG-P10-001 naming check "review date present"

  Scenario: AC9 The loader cannot approve
    Given user "coe.user01" loaded version "P2"
    When user "coe.user01" approves it
    Then the system refuses the approval with 409 and MSG-P7-002
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | In SHADOW mode the pack and completeness list are stored only; no pack, document or legal action changes | agent_policy.autonomy_mode (New) |
| BR2 | Checklist items come from the document checklist for the case type | Reference table document checklist; REQ-DCM-011 |
| BR3 | Every item has a status PRESENT, MISSING or DEFECT, and every DEFECT has a reason | R-LIT-16, R-LIT-17; CTL-19 |
| BR4 | A pack may name only documents of the same case | CTL-19; CTL-11 |
| BR5 | Agreement per item = cases where the agent status equals the officer status / scored cases, 4 decimals | agent_evaluation.agreement_rate (New) |
| BR6 | A promotion to L1 needs at least 50 scored cases (assumed); keeping shadow needs a review date | agent_policy.review_date (New) |
| BR7 | The loader and the approver are different people | Separation of duty, center of excellence analyst and risk and model risk officer |

### 9. State transitions

None. This story does not change a case status and does not move a case into PACK_ASSEMBLY. It writes agent runs, one evaluation run (RUNNING to DONE) and one policy version (LOADED to APPROVED).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT | Reads case, legal actions, documents, fields and checklist (Case record R, Litigation R, Documents R, Reference data R) |
| RW-COE | Loads the sample, runs the evaluation, loads the decision version (Rules and parameters CRUD) |
| RW-RISK | Approves the decision version (Rules and parameters A) |
| RW-LITOFF | Supplies the officers' packs for the sample; reads scores through the export |
| RW-HEADLIT | Reads scores through the export |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-017 | recovery_case | prescription_date | Read |
| DF-LEG-001 | legal_action | id | Read |
| DF-LEG-004 | legal_action | action_type | Read |
| DF-LEG-014 | legal_action | status | Read |
| DF-DOC-001 | document | id | Read |
| DF-DOC-002 | document | case_id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-010 | document | write_once | Read |
| DF-DOC-014 | document_field | field_name | Read |
| DF-DOC-015 | document_field | field_value | Read (masked) |
| DF-AGT-036 | agent_run | id | Write |
| DF-AGT-037 | agent_run | agent_code | Write |
| DF-AGT-038 | agent_run | agent_version | Write |
| DF-AGT-041 | agent_run | case_id | Write |
| DF-AGT-042 | agent_run | subject_id | Write |
| DF-AGT-043 | agent_run | autonomy_mode | Write |
| DF-AGT-044 | agent_run | trigger_event | Write |
| DF-AGT-046 | agent_run | status | Write |
| DF-AGT-047 | agent_run | fallback | Write |
| DF-AGT-048 | agent_run | guardrail_result | Write |
| DF-AGT-049 | agent_run | output | Write |
| DF-AGT-051 | agent_run | latency_ms | Write |
| DF-AGT-052 | agent_run | tokens_in | Write |
| DF-AGT-053 | agent_run | tokens_out | Write |
| DF-AGT-054 | agent_run | cost_thb | Write |
| DF-AGT-056 | agent_run | run_at | Write |
| DF-AGT-057 | agent_run | evaluation_run_id | Write |
| DF-AGT-063 | agent_sample | sample_code | Read |
| DF-AGT-064 | agent_sample | sample_version | Read |
| DF-AGT-066 | agent_sample | subject_id | Read |
| DF-AGT-067 | agent_sample | label_key | Read |
| DF-AGT-068 | agent_sample | expected_value | Read |
| DF-AGT-087 | agent_evaluation | evaluation_run_id | Write |
| DF-AGT-089 | agent_evaluation | label_key | Write |
| DF-AGT-090 | agent_evaluation | sample_size | Write |
| DF-AGT-094 | agent_evaluation | agreement_rate | Write |
| DF-AGT-003 | agent_policy | policy_version | Write |
| DF-AGT-008 | agent_policy | autonomy_mode | Write |
| DF-AGT-016 | agent_policy | review_date | Write |
| DF-AGT-017 | agent_policy | evaluation_run_id | Write |
| DF-AGT-018 | agent_policy | promotion_conditions | Write |
| DF-AGT-021 | agent_policy | status | Write |
| DF-AGT-025 | agent_policy | approved_by | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /api/recovery/v1/admin/agent-samples**, **POST /api/recovery/v1/admin/agent-evaluations**, **GET /api/recovery/v1/admin/agent-evaluations** (new, RWB-E1-058): agent "LEGAL_DOC", sample "LEGAL-S1"; Rules and parameters C and R; errors 401, 403, 409 (MSG-P10-003), 422 (MSG-P10-001, MSG-P10-002), 503.

**POST /api/recovery/v1/admin/agent-configs** and **POST /api/recovery/v1/admin/agent-configs/{versionId}/approve** (new): the promote or keep version; Rules and parameters C and A; errors 409 (MSG-P7-002, MSG-GEN-004), 422 (MSG-P10-001).

**Output schema "legal-pack-v1":** items (array of {itemCode from the checklist, status PRESENT, MISSING or DEFECT, documentIds, defectReason}), confidence.

**Interfaces called:** S4 LegalActionQueryService.listByCase(caseId); P5 DocumentQueryService.listByCase, getFields and getChecklist(caseType); all as SY-AGENT. A call that fails returns TOOL_UNAVAILABLE (R-UNI-33).

**Event published:** EV-28 AgentRunCompleted.

### 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/legal/`, Java package `recovery.agent.legal`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LegalPackInputAssembler | Service | Builds masked inputs from the case, legal actions, documents, fields and checklist |
| LegalPackRuleChecks | Service | SCHEMA_RULE checks: same-case documents, defect reasons, all items present |
| LegalPackScorer | Service | Agreement per checklist item for the harness |
| legal-pack-v1.json, prompt LEGAL_DOC PR1 | Rule table | Output schema and prompt, loaded through the configuration endpoint |
| PromotionProposalValidator | Service | Extended with the review date rule for SHADOW decisions |

**Database:** no new table. Writes agent_run, agent_evaluation_run, agent_evaluation and agent_policy; reads agent_sample.

**Configuration and reference data:** policy LEGAL_DOC P1 (minimum sample 50) loaded by RW-COE and approved by RW-RISK; checklist reference data maintained by RW-REFADM; sample LEGAL-S1 built from the officers' packs.

**Build steps**
1. Write the output schema and the prompt; load them in DEV.
2. Build LegalPackInputAssembler over the S4 and P5 interfaces (AC1).
3. Build LegalPackRuleChecks (AC4, AC5) and the TOOL_UNAVAILABLE path (AC6).
4. Build LegalPackScorer on a 10-case fixture with known agreement (AC2).
5. Extend PromotionProposalValidator for the sample minimum and the review date (AC3, AC7, AC8, AC9).

**Feature flag:** `rwb.agent.legal-shadow`. Off: evaluations of LEGAL_DOC are refused with 422.

**Done when:** the tests in section 16 pass and the 50-case evaluation is approved as promote or keep.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | The decision version fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | Evaluation on an empty sample | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P7-002 | Loader approves own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

No user screen shows a pack in this story. SCR-46 Agent monitor shows LEGAL_DOC in state Shadow with its runs, fallbacks and the evaluation score. Scores are exported through GET /admin/agent-evaluations.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-030-01 | AC1, BR1, BR2 | System | Case RW-2026-000901, 14 documents, 9 checklist items |
| TC-E2-030-02 | AC2, BR5 | System | Sample LEGAL-S1 version 1, 50 cases; 46 agree on DEMAND_NOTICE_PROOF |
| TC-E2-030-03 | AC3, BR6 | System | Version P2 SHADOW with review date 2027-03-15 |
| TC-E2-030-04 | AC4, BR4 | System | Document D-7001 of another case in the pack |
| TC-E2-030-05 | AC5, BR3 | System | No status for MORTGAGE_DEED |
| TC-E2-030-06 | AC6 | System | P5 interface down for case RW-2026-000903 |
| TC-E2-030-07 | AC7, BR6 | System | 49 scored cases, proposal L1 |
| TC-E2-030-08 | AC8, BR6 | System | SHADOW version with no review date |
| TC-E2-030-09 | AC9, BR7 | System | Loader coe.user01 approves P2 |
| TC-E2-030-10 | Access | Access | RW-LITOFF calls POST /admin/agent-evaluations; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: checklist items, minimum sample and review date are data.
- No personal data in logs, tests or prompts; field values are masked before the model call.
- No read of another module's tables; legal actions and documents come through the S4 and P5 interfaces.
- The agent never changes a write-once legal document or a pack.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested | Business Requirements Program, section 5.11 | FEAT-AGT-09 | 8.2 Instruct and file | R-LIT-16, R-LIT-17, R-UNI-33 | TC-E2-030-01, TC-E2-030-02, TC-E2-030-03, TC-E2-030-04, TC-E2-030-05, TC-E2-030-06, TC-E2-030-07, TC-E2-030-08, TC-E2-030-09, TC-E2-030-10 |

### 19. Out of scope

- Pack assembly, retrieval requests and officer verification in the litigation flow (Epic 5, S4).
- Showing packs to officers at L1 (Epic 5).
- Extraction for the stage 2 and 3 document types (RWB-E2-025).


---
