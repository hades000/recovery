# Recovery Workbench user stories, Epic 2

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Stories | 41 |
| Acceptance criteria | 415 |
| Test cases | 479 |
| Modules | P1 (1), P2 (12), P3 (8), P4 (2), P5 (4), P6 (3), P7 (3), P8 (2), P9 (1), P10 (5) |

Release 31 December 2026. Epic 2 status: confirmed. The 3 agent stories at the end of this file go live with Epic 3, after the foundation.

This version also applies decision D-RCV-36 and ADR-011 and ADR-012, agreed on 16 November 2026: case workflows run on Temporal from Epic 3 with case data kept in the ACE database, rules are evaluated by embedded Drools from versioned rule packages, and RWB-E1-029, RWB-TE-005 and RWB-E1-048 are retired (new homes RWB-E1-073 and RWB-E2-041). The configuration stories RWB-E1-070 to RWB-E1-073 and RWB-E2-037 to RWB-E2-043 are added.

Each story is written for build: the business rationale, preconditions, the main flow and its exception paths, acceptance criteria in Gherkin, business rules, state transitions, authority, the fields it reads and writes with their BR Field IDs, the contract, the solution plan, messages, screens, test cases and traceability to the business requirements. Field IDs are those in the Logical Data Model and Data Dictionary and Physical Schema v6, endpoints those in the API Specification v4, messages those in the Error and Message Standard and requirement IDs those in the Business Requirements. The same stories are also supplied one file per story, to hand to a coding agent with the module specifications.

| Key | Title | Module | Requirements | Depends on |
|---|---|---|---|---|
| RWB-E2-001 | EFS hand-over with full history | P2 Integration | REQ-DRI-013, REQ-CHO-001, REQ-CHO-005, REQ-RDF-003 | RWB-E1-069, RWB-E1-015, RWB-E1-007 |
| RWB-E2-002 | ACE plan status on the case | P2 Integration | REQ-DRI-013, REQ-CHO-002 | RWB-E2-001, RWB-E1-072, RWB-E2-042 |
| RWB-E2-003 | Customer's other products on the case | P2 Integration | REQ-CHO-003, REQ-RDF-010 | RWB-E1-069, RWB-E1-007 |
| RWB-E2-004 | Treatment entity and plan timers data model | P3 Case and workflow, with P1 Recovery data engine for the data product | REQ-CHO-006, REQ-CHO-007, REQ-RDF-014 | RWB-E1-018, RWB-E1-028, RWB-E1-045, RWB-E1-072, RWB-E2-042 |
| RWB-E2-005 | Decision log query API for audit | P7 Decision center and log | REQ-DRI-012 | RWB-E1-008, RWB-E1-039, RWB-E2-041 |
| RWB-E2-006 | Credit approval pack for NLEADS | P2 Integration | REQ-CHO-008, REQ-CHO-006 | RWB-E2-004, RWB-E1-007 |
| RWB-E2-007 | Booking confirmation from the ALS load | P2 Integration, with P8 Payments and posting | REQ-CHO-008 | RWB-E2-004, RWB-E1-069, RWB-E1-007, RWB-E1-072, RWB-E2-042 |
| RWB-E2-008 | Payment matching with the missed payment event | P8 Payments and posting | REQ-CHO-007, REQ-CHO-009 | RWB-E2-004, RWB-E1-069, RWB-E1-072, RWB-E2-042 |
| RWB-E2-009 | Steering dashboard v1 data set | P9 Reporting | REQ-WKM-009, REQ-WKM-006 | RWB-E1-013, RWB-E1-063 |
| RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | P1 Recovery data engine | REQ-RDF-014 | RWB-E2-004, RWB-E1-069, RWB-E1-016, RWB-E1-015 |
| RWB-E2-011 | Queue view screens: my queue, team queues, filters and ageing | P3 Case and workflow | REQ-WKM-001, REQ-WKM-002, REQ-WKM-006 | RWB-E1-020, RWB-E1-031 |
| RWB-E2-012 | Manual transfer and reassignment screen with reason | P3 Case and workflow | REQ-WKM-003, REQ-WKM-007, REQ-WKM-008 | RWB-E1-021, RWB-E1-072, RWB-E2-011 |
| RWB-E2-013 | Approval routing with the delegation of authority table | P7 Decision center and log | REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010, REQ-APD-011 | RWB-E1-038, RWB-E1-028, RWB-E1-027, RWB-E1-037 |
| RWB-E2-014 | Approval screen for D7.1 demand and recall notices | P7 Decision center and log, with P6 Communications | REQ-APD-002, REQ-APD-006 | RWB-E2-013, RWB-E1-052 |
| RWB-E2-015 | Timers, escalation and the deviation flag on the case record view | P3 Case and workflow | REQ-WKM-004, REQ-WKM-005, REQ-DVH-002 | RWB-E1-028, RWB-E1-035 |
| RWB-E2-016 | Full case record view with the history timeline | P3 Case and workflow, with P7 Decision center and log | REQ-WKM-008, REQ-OCC-008 | RWB-E1-035, RWB-E2-015, RWB-E2-012 |
| RWB-E2-017 | Contract, CA and mortgage document generation screens | P5 Document hub | REQ-DCM-012, REQ-OCC-002 | RWB-E2-026, RWB-E1-034, RWB-E1-054, RWB-TE-012 |
| RWB-E2-018 | E-signature flow for customers and the bank | P6 Communications | REQ-OCC-009 | RWB-E2-017, RWB-E2-022 |
| RWB-E2-019 | Partner identities through the external gateway | P4 Access and administration | REQ-ACA-012 | RWB-E1-022, RWB-E1-037, RWB-E1-039 |
| RWB-E2-021 | Letter dispatch loop with proof of delivery from WIN | P6 Communications | REQ-OCC-003, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010 | RWB-E1-052, RWB-E1-055, RWB-E2-014 |
| RWB-E2-022 | SMS and LINE dispatch through NSS and LINE OA | P6 Communications | REQ-OCC-004, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010 | RWB-E1-052, RWB-E1-066 |
| RWB-E2-024 | Field app photos and bills into the document hub | P5 Document hub | REQ-DCM-013 | RWB-E1-057, RWB-E1-032, RWB-E1-053, RWB-E1-024, RWB-E1-041 |
| RWB-E2-025 | Extraction for the stage 2 and 3 document types | P5 Document hub | REQ-DCM-006, REQ-DCM-005 | RWB-E1-053, RWB-E1-050, RWB-E1-054 |
| RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | P5 Document hub | REQ-DCM-012, REQ-OCC-002 | RWB-E1-046, RWB-E1-034, RWB-E1-024, RWB-E1-027 |
| RWB-E2-027 | Payment matching rules with the data team | P8 Payments and posting | REQ-CHO-009 | RWB-E2-008, RWB-E2-042 |
| RWB-E2-031 | Agent monitoring dashboard v2 [E3d] | P10 Agent runtime | REQ-DRI-009, REQ-APD-005 | RWB-E1-063, RWB-E2-005 |
| RWB-E2-032 | TDR offer-suggestion model through the model gateway [E3e] | P10 Agent runtime | REQ-CHO-006, REQ-DRI-001 | RWB-E1-058, RWB-E2-004, RWB-E1-027 |
| RWB-E2-033 | Case and queue list with status, owner and ageing | P2 Integration | REQ-WKM-002, REQ-DVH-006 | RWB-E1-018, RWB-E1-031, RWB-E2-011 |
| RWB-E2-034 | Interaction ledger on the case and from every channel | P2 Integration | REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013 | RWB-E1-027, RWB-E2-016, RWB-E1-069, RWB-E1-007, RWB-E1-066, RWB-E1-067, RWB-TE-006 |
| RWB-E2-035 | Next action on the case | P2 Integration | REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014, REQ-WKM-015 | RWB-E1-018, RWB-E1-031, RWB-E1-072, RWB-E2-033, RWB-E2-042 |
| RWB-E2-036 | Queue write interface for models and agents | P2 Integration | REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020 | RWB-E1-019, RWB-E1-020, RWB-E1-027 |
| RWB-E2-037 | Temporal observability and run books | P2 Integration | REQ-DRI-007 | RWB-E1-070, RWB-E1-071, RWB-E1-056 |
| RWB-E2-038 | Temporal security, codec server and admin audit | P4 Access and administration | REQ-DRI-001, REQ-DRI-005 | RWB-E1-070, RWB-E1-071, RWB-E1-039 |
| RWB-E2-039 | Temporal resilience: backup, failover, upgrade and archive | P2 Integration | REQ-DRI-007 | RWB-E1-070, RWB-E2-037 |
| RWB-E2-040 | Workflow versioning and replay test gate | P2 Integration | REQ-DRI-005 | RWB-E1-071 |
| RWB-E2-041 | Rule change governance and audit report | P3 Case and workflow | REQ-CWC-013, REQ-DRI-011 | RWB-E1-073, RWB-E1-037 |
| RWB-E2-042 | Epic 2 rule packages in Drools | P3 Case and workflow | REQ-CWC-013, REQ-CWC-014 | RWB-E1-073 |
| RWB-E2-043 | Temporal and Drools integration pattern and reference case workflow | P3 Case and workflow | REQ-DRI-001, REQ-DRI-005, REQ-CWC-016 | RWB-E1-071, RWB-E1-072, RWB-TE-006 |
| RWB-E2-028 | Case intake agent live at L1 [E3a] | P10 Agent runtime | REQ-DRI-001, REQ-ACA-005 | RWB-E1-061, RWB-E1-035, RWB-E1-027, RWB-E2-031 |
| RWB-E2-029 | Deviation screening agent evaluation and L1 on one segment [E3b] | P10 Agent runtime | REQ-DVH-001, REQ-DVH-006 | RWB-E1-062, RWB-E2-015, RWB-E1-061, RWB-E2-028 |
| RWB-E2-030 | Legal document agent in shadow on Epic 1 data [E3c] | P10 Agent runtime | REQ-S4-002 | RWB-E1-058, RWB-E2-025, RWB-E1-061 |

## RWB-E2-001 EFS hand-over with full history

| Item | Value |
|---|---|
| Story key | RWB-E2-001 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CHO-01 Take the case hand-over from EFS with full history; FEAT-CHO-04 Create a case the morning after it reaches 90 days past due; FEAT-CHO-05 Hold case creation when the ACE batch is late |
| Requirement IDs | REQ-DRI-013, REQ-CHO-001, REQ-CHO-005, REQ-RDF-003 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.1, 5.2 and 5.3 |
| L3 process | 6.1 Take over the case at 90 days past due |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-069, RWB-E1-015, RWB-E1-007 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case created or linked from the ACE record of the ALS hand-over, with the contact and promise history read from v_ace_efs_action**, so that **the case starts the morning after the account reaches 90 days past due and I can see what happened before day 90**.

### 2. Business rationale

Accounts move from collections to recovery by a weekly transfer today, and the case starts without its collection history. ACE ingests the ALS hand-over and the EFS action history (D-RCV-35 U1). This story creates the case each morning from the account rows ACE holds for the business date, links a further account of the same customer and product group to the open case, and appends the EFS contact and promise history read from v_ace_efs_action to the interaction ledger. It holds case creation while the ACE batch for the business date is incomplete, so no case is built from stale data. It meets REQ-CHO-001, REQ-CHO-005, REQ-DRI-013 and REQ-RDF-003 and is measured by CTL-01 and REC-01 (accounts at 90 days past due against open cases, zero unexplained).

### 3. Preconditions

- RWB-E1-069 (read-only ACE source views, grants and boundary rule) is done: v_ace_account, v_ace_customer and v_ace_efs_action are granted SELECT to the recovery service identity in V0002.
- RWB-E1-015 (freshness stamp per data product) is done: data_product_load carries the ACE business date and P1 publishes AceDataReady (EV-26) from the ACE batch record.
- RWB-E1-007 (adapters and IdempotencyGuard), the case record (RWB-E1-018) and the decision log writer (RWB-E1-027) are in production.
- Parameter `case.entry.dpd_threshold` = 90 is in force (DL16).
- The product code to product group map (LOV-PRODUCT-CODE to LOV-PRODUCT) is loaded.
- The EFS action codes copied at hand-over are rows in efs_ledger_outcome (DL29, RWB-E2-034).
- The hold time `handover.hold_until` = 09:00 is in force.
- SY-CASEWF and SY-DECLOG hold their managed identities; the recovery service identity holds SELECT on the views only.

### 4. Flow

1. Scheduler: JOB-02 starts when AceDataReady (EV-26) arrives for the ALS source with business date D, once the EFS source carries the same business date D.
2. The recovery service identity: HandoverService reads the data_product_load stamps of DP01 Account and arrears and DP05 Contact and promises at business date D; if either is STALE, it holds the run (step X2).
3. The recovery service identity: reads v_ace_account for business date D and selects every account with days_past_due at or above the threshold and no open case link.
4. HandoverService: for each account, calls IdempotencyGuard.firstTime("handover", accountKey + ":" + D); a repeat is skipped and counted.
5. HandoverService: groups the accounts by primary person_key (v_ace_customer) and product group (DL17).
6. SY-CASEWF: for each group, CaseCreation.createOrLink writes the decision log entry first, then creates the case with status New, case number RW-YYYY-NNNNNN and entry date D+1, or links the account to the customer's open case for the product group.
7. SY-CASEWF: publishes CaseCreated (EV-01) with the business date, in the same transaction.
8. HandoverService: reads the v_ace_efs_action rows of the account_key whose contact_at falls inside the collection period, keeps the action codes that are in efs_ledger_outcome, and appends them through InteractionLedger.appendEfsHistory with source system EFS; each entry is keyed on efs_record_key, so a row the daily read of RWB-E2-034 already wrote is skipped.
9. HandoverService: writes the run summary (accounts read, cases created, accounts linked, repeats, held) and the REC-01 result to reconciliation_result; JOB-03 allocation follows.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same business date is run twice | No second case or link; the repeat is counted in the run summary (R-UNI-40) | None | AC2 |
| X2 | The ACE batch for ALS and business date D is not COMPLETE by 09:00 | JOB-02 does not run; the data products show stale; the data steward is alerted; cases are created on the next good business date | MSG-P1-001, MSG-P2-007 | AC3, AC6 |
| X3 | The account's person_key has no row in v_ace_customer | The account is not taken; the REC-05 business-key break lists the account_key and it is tried with the next run | None | AC5 |
| X4 | The decision log write fails | The case is not created; an incident is raised (R-UNI-39); the account is tried in the next run | MSG-P7-003 | AC7 |
| X5 | The customer already has an open case for the product group | The account is linked to that case; no new case | None | AC4 |
| X6 | JOB-02 is started again while it runs | The rerun is refused | MSG-P2-006 | AC8 |
| X7 | A role without the right reruns JOB-02 | Refused; nothing changes | MSG-P4-002 | TC-E2-001-09 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the ACE views (RWB-E1-069), the freshness stamp (RWB-E1-015) and the adapters (RWB-E1-007); the case record and log writer are in production |
| Negotiable | Threshold, product map, copied action codes and the hold time are data rows |
| Valuable | Each case starts the morning after day 90 with its collection history |
| Estimable | One service, one job step, three view reads and two interface calls |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

```gherkin
Feature: EFS hand-over with full history

  Background:
    Given parameter "case.entry.dpd_threshold" is 90
    Given the ACE batch for ALS with business date 2026-12-14 is COMPLETED at 05:20

  Scenario: AC1 Case from the ACE data
    Given synthetic account "A-0001" for customer "C-0001", product group "MORTGAGE", reached 90 days past due in v_ace_account at business date 2026-12-14
    Given v_ace_efs_action holds 14 contact rows and 2 promise rows for "A-0001" in its collection period
    When the morning case creation runs on 2026-12-15
    Then a case exists with status "NEW", product group "MORTGAGE", entry date 2026-12-15 and days past due at entry 90
    Then the case holds 16 interaction entries with source system "EFS" and the action code of each row
    Then the decision log entry for the creation holds business date 2026-12-14 in its inputs snapshot
    Then the system publishes caseCreated with business date 2026-12-14

  Scenario: AC2 Repeat run
    Given the run for business date 2026-12-14 created the case for "A-0001"
    When case creation runs again for business date 2026-12-14
    Then the system creates no second case and no interaction entry is added
    Then the run summary shows 1 repeat for "A-0001"

  Scenario: AC3 Late ACE batch
    Given the ACE batch for ALS with business date 2026-12-15 is not COMPLETE by 09:00 on 2026-12-16
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

  Scenario: AC5 Customer not in the ACE customer data
    Given synthetic account "A-0003" reaches 90 days past due and v_ace_customer holds no row for its person_key
    When case creation runs
    Then the system creates no case for "A-0003"
    Then the REC-05 business-key break lists "A-0003" for the data steward
    Then "A-0003" is tried again with the next run

  Scenario: AC6 Cases created on the next good batch
    Given no case creation ran for business date 2026-12-15
    Given the ACE batch for ALS with business date 2026-12-16 is COMPLETED at 05:15 on 2026-12-17
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
| BR3 | The hand-over set is read from v_ace_account for the ACE business date; the Workbench loads no source file | D-RCV-35 U1; ADR-010; REQ-DRI-013 |
| BR4 | No case is created from a business date whose ACE batch is not COMPLETE | JOB-02; CTL-02; FEAT-CHO-05 |
| BR5 | The EFS contact and promise history of the collection period is read from v_ace_efs_action and appended to the interaction ledger with source system EFS, one entry per efs_record_key | DL29; LOV-SOURCE; REQ-CHO-001; R-UNI-40 |
| BR6 | A repeat hand-over for the same account and business date is ignored and counted | R-UNI-40 |
| BR7 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR8 | An account whose person_key has no row in v_ace_customer is held on the REC-05 business-key break and tried with the next run | REC-05; DQ-040; D-RCV-35 U2 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No case | CaseCreated (EV-01) from JOB-02 | days_past_due at or above 90 and no open case for the customer and product group | New |
| New, Assigned, In progress or any Waiting | Account linked by JOB-02 | Open case for the customer and product group | Status unchanged |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery service identity, JOB-02 | Reads the ACE views; calls case creation and the ledger (Case record, CU) |
| SY-CASEWF, case workflow module | Creates the case and the account link; publishes CaseCreated |
| SY-DECLOG, decision log writer | Writes the entry (Decision log, C) |
| RW-CASEOWN, case owner | Reads the case and its history once allocated (Case record, R) |
| RW-DATASTEW, data steward | Receives the late batch alert; reads the run summary and the REC-05 break (Platform administration, R) |
| RW-PLATADM, platform administrator | Reruns JOB-02 (Platform administration, U) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-008 | v_ace_account | product_key | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-108 | v_ace_efs_action | efs_record_key | Read |
| DF-ACE-111 | v_ace_efs_action | action_code | Read |
| DF-ACE-114 | v_ace_efs_action | contact_at | Read |
| DF-ACE-119 | v_ace_efs_action | is_ptp | Read |
| DF-ACE-122 | v_ace_efs_action | promise_date | Read |
| DF-ACE-123 | v_ace_efs_action | promise_amount | Read |
| DF-CAS-002 | recovery_case | case_no | Write |
| DF-CAS-003 | recovery_case | product_group | Write |
| DF-CAS-004 | recovery_case | primary_person_key | Write |
| DF-CAS-005 | recovery_case | status | Write |
| DF-CAS-013 | recovery_case | entry_date | Write |
| DF-CAS-014 | recovery_case | dpd_at_entry | Write |
| DF-CAS-016 | recovery_case | total_outstanding_at_entry | Write |
| DF-CAS-025 | case_account | case_id | Write |
| DF-CAS-026 | case_account | account_key | Write |
| DF-CAS-027 | case_account | is_primary | Write |
| DF-CAS-028 | case_account | linked_from | Write |
| DF-INT-002 | interaction | case_id | Write |
| DF-INT-003 | interaction | person_key | Write |
| DF-INT-004 | interaction | occurred_at | Write |
| DF-INT-005 | interaction | channel | Write |
| DF-INT-006 | interaction | direction | Write |
| DF-INT-007 | interaction | action_code | Write |
| DF-INT-008 | interaction | contact_result | Write |
| DF-INT-009 | interaction | promise_amount | Write |
| DF-INT-010 | interaction | promise_date | Write |
| DF-INT-013 | interaction | source_system | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | all fields | Write |
| DF-OPS-178 to DF-OPS-183 | processed_event | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary. The view rows are read through the published P1 interfaces and never from a public table.

### 12. Contract

**Job JOB-02 Case creation.** Trigger: Quartz, daily on AceDataReady (EV-26) for ALS when the EFS source carries the same business date. Input: v_ace_account rows at or above the threshold for business date D; v_ace_customer for the person_key; v_ace_efs_action for the collection period. Output: cases with status New, account links, interaction entries, decision log entries, the REC-01 result. Events published: CaseCreated (EV-01) by P3 through the outbox. Events consumed: AceDataReady (EV-26). Idempotency key: account_key + business date. Restart: POST /admin/jobs/{jobId}/rerun; accounts already handled for D are skipped through the key.

**Endpoints used.**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| POST /admin/jobs/{jobId}/rerun | Path: jobId | Job | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-P4-003); 409 running (MSG-P2-006); 503 (MSG-P7-003) | Platform administration, U | Per account and business date |
| GET /cases/{caseId}/timeline | Query: type, from, to | TimelinePage | 401; 403; 404 out of scope (MSG-P4-003); 503 | Case record, R | Read only |

**Published interfaces called.**

```java
// P1 recovery.data.api, over recovery.v_ace_account
List<EntryCandidate> AccountQuery.findAtOrAboveDpd(int threshold, LocalDate businessDate);
// P1 recovery.data.api, over recovery.v_ace_efs_action
List<EfsHistoryRecord> EfsHistoryQuery.forAccount(String accountKey, LocalDate businessDate);
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
| HandoverJob | Job | JOB-02 step; starts on AceDataReady after the DP01 and DP05 stamps |
| HandoverGroupBuilder | Service | Groups candidates by person_key and product group with the product map |
| HandoverSummaryWriter | Service | Writes the REC-01 result to reconciliation_result and the counts to the batch step |
| AceDataReadyListener | Listener | Consumes EV-26 through IdempotencyGuard |

- **Database:** no new table. Writes processed_event and reconciliation_result (REC-01). Case, account link, interaction and decision log rows are written by P3 and P7 through their interfaces.
- **Configuration and reference data:** parameter case.entry.dpd_threshold = 90 (RW-COE, DL16); product code map (RW-REFADM); efs_ledger_outcome rows for the history (RW-DATASTEW, DL29); parameter handover.hold_until = 09:00 (RW-COE).
- **Build steps:**
  1. Build HandoverGroupBuilder with tests for one and two accounts per customer and product group.
  2. Build HandoverService with the freshness hold and the gap dates taken from the last good stamp.
  3. Wire IdempotencyGuard on account_key and business date.
  4. Call CaseCreation.createOrLink; on DecisionLogUnavailableException stop the account, count it and raise the incident.
  5. Call InteractionLedger.appendEfsHistory with the v_ace_efs_action rows of the collection period.
  6. Build HandoverJob and AceDataReadyListener; chain JOB-03 after it.
  7. Write the REC-01 result and the MSG-P2-007 alert for a held run.
- **Feature flag:** `rwb.integration.efs-handover`.
- **Done when:** the tests in section 16 pass and REC-01 for SIT business date 2026-12-14 shows zero unexplained difference.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | Data product stale after an incomplete ACE batch | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-007 | Case creation held for an incomplete ACE batch | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | Rerun while JOB-02 runs | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the right reruns JOB-02 | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

No new screen. The case owner sees the new case on SCR-02 Case list (states loading, list) and its EFS history on SCR-04 Case timeline (states loading, filtered) with source EFS. The data steward sees held runs and the REC-05 break on SCR-45 Data quality.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-001-01 | AC1, BR1, BR3, BR5 | System | Synthetic account A-0001 with 14 contact rows and 2 promise rows in v_ace_efs_action |
| TC-E2-001-02 | AC2, BR6 | System | Same business date run twice |
| TC-E2-001-03 | AC3, BR4 | System | ACE batch for ALS of 2026-12-15 not COMPLETE |
| TC-E2-001-04 | AC4, BR2 | System | Customer C-0002 with an open SSME case |
| TC-E2-001-05 | AC5, BR8 | System | Account A-0003 with no row in v_ace_customer |
| TC-E2-001-06 | AC6, BR4 | System | Good batch on 2026-12-17 after a missed day |
| TC-E2-001-07 | AC7, BR7 | System | Decision log store stopped |
| TC-E2-001-08 | AC8 | System | JOB-02 running |
| TC-E2-001-09 | Access | Access | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |
| TC-E2-001-10 | Principle 5 | Resilience | Decision log write forced to fail during a run of 50 synthetic accounts; no case is created without its entry |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the threshold, the product map, the copied action codes and the hold time are rows.
- No personal data in logs, tests or prompts; the run summary holds counts and synthetic keys; interaction summaries are not logged.
- No read of ACE tables: the read path is v_ace_account, v_ace_customer and v_ace_efs_action through the published interfaces (boundary rule, RWB-E1-069).
- No case is built from a business date whose ACE batch is not COMPLETE.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the daily ALS batch | Program 5.2; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | R-UNI-40 | TC-E2-001-01, TC-E2-001-02 |
| REQ-CHO-001 | Case with full contact and promise history | Program 5.3; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-01, TC-E2-001-05 |
| REQ-CHO-005 | Workbench is the system of record for case state after hand-over | Program 5.3; Epic 2 3.2 | FEAT-CHO-04 | 6.1 Take over the case at 90 days past due | R-UNI-39 | TC-E2-001-04, TC-E2-001-07, TC-E2-001-10 |
| REQ-RDF-003 | EFS history transfers to the case | Program 5.1; Epic 2 3.2 | FEAT-CHO-05 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-03, TC-E2-001-06, TC-E2-001-08 |

### 19. Out of scope

- Allocation of the new case: RWB-E1-020.
- The ACE plan status on the case: RWB-E2-002.
- The daily reconciliation of hand-overs against open cases and the REC-01 break list: RWB-E1-011.
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
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E2-001, RWB-E1-072, RWB-E2-042 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the restructure plan status from the ACE common module (created, approved, booked, broken) on the case**, so that **a case with a live plan is never treated as if it had none, and a broken plan returns the case to me the next morning**.

### 2. Business rationale

Restructure plans are calculated and held in ACE (DL14). Without the plan status on the case, a recovery officer can start litigation on a customer who is paying a plan, or miss a plan that broke. This story reads the status from the ACE common module each morning and on each case view, keeps the last known status with its date when ACE returns none, and raises the broken plan to the restructure rules. It meets REQ-CHO-002 and REQ-DRI-013.

The restructure rules R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are rows of package RESTRUCTURE under ADR-012, fixed by D-RCV-36 on 16 November 2026. SY-RULES evaluates them through RuleEvaluator, the result names the rule and the package version, and the decision log records both. The action text, the owner role and the timer spec of the row are read from RuleCatalog. The measure is that a broken plan is back with the case owner the next morning and no case with a live plan is treated as if it had none.

### 3. Preconditions

- RWB-E2-001 (case creation from the ACE data) is done.
- RWB-E1-072 is done: RuleEvaluator, RuleCatalog and the rule package store exist, and DecisionLogWriter records the rule ID and the package version.
- RWB-E2-042 is done: package RESTRUCTURE is in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02, and each row carries action_text, owner_role and timer_spec.
- The ACE common module publishes RestructurePlanQuery in SIT and UAT (INT-34; DL14).
- The account number is the join key between the case and the ACE plan (DL21).
- The plan event map rows are loaded: ACE status BROKEN with route state PLAN_CURE_PERIOD maps to event CURE_PERIOD_EXPIRED; BROKEN with any other route state maps to TREATMENT_BROKEN.
- Parameter `restructure.max_breaks` = 2 is in force (Restructure route set: a second break bars a further restructure).

### 4. Flow

1. Scheduler: the plan status step runs in JOB-02 after the case creation step, once a day.
2. The recovery service identity: the PlanStatusService lists every open case with its account numbers through the P3 CaseQuery.
3. The recovery service identity: calls RestructurePlanQuery.statusFor with the account numbers in batches of 500 (assumed; DL11).
4. The recovery service identity: for each plan returned, compares status and status date with the stored values; an unchanged plan is skipped.
5. SY-CASEWF: writes plan_ref, plan_status and plan_status_as_of on the case through CasePlanStatus.update.
6. The recovery service identity: on a change to BROKEN, looks up the event in the plan event map and calls CaseEvents.raise with plan_status = broken and the break count.
7. SY-RULES and SY-CASEWF: SY-RULES builds RestructureFacts for the case (route state, plan_status, break_count, prior_route) and calls RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate); the result names the rule, the package version and the outputs. SY-CASEWF writes the decision log entry with that rule ID and package version, then reads action_text, owner_role and timer_spec from RuleCatalog.row(ruleId, packageVersion), moves the route state and places the case in the case owner's queue with a task due by the timer spec.
8. Case owner: opens the case record view; the front end calls GET /cases/{caseId}/plan-status, which reads ACE live with a 2-second timeout and falls back to the stored status.
9. The recovery service identity: for a case with a stored plan that ACE no longer returns, keeps the stored status and date and writes a break for the data steward and the ACE team.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | ACE returns no status for a plan the case holds | The case keeps its last known status and date; a break on the data quality console lists the plan for the ACE team | MSG-P2-008 | AC3 |
| X2 | The ACE common module is unavailable or does not answer in 2 seconds | The daily step keeps every stored status and retries in the next run; the view shows the stored status | MSG-GEN-006, MSG-P2-008 | AC4 |
| X3 | ACE returns a status code not in the plan status list | The status is not stored; a break with check "Lists of values" is written | None | AC5 |
| X4 | The daily step runs twice for the same day | No status is written twice and no event is raised twice | None | AC6 |
| X5 | The decision log write fails during the broken plan move | The route state does not move; an incident is raised; the event is raised again in the next run | MSG-P7-003 | AC7 |
| X6 | A user reads the plan status of a case outside their scope | Refused | MSG-P4-003 | AC8 |
| X7 | A role without the Case record right reads the plan status | Refused; nothing changes | MSG-P4-002 | TC-E2-002-10 |
| X8 | No RESTRUCTURE version is IN_FORCE on the business date | NoPackageInForce; no decision log entry is written and the route state does not move; the case goes to the exception queue for a person | MSG-P3-027 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the cases from RWB-E2-001, the ACE interface, the evaluator of RWB-E1-072 and the RESTRUCTURE package of RWB-E2-042 |
| Negotiable | The event map, batch size, timeout, maximum breaks and package version are data rows or properties |
| Valuable | No action is taken on a case with a live plan without the plan in view |
| Estimable | One service, one job step, one endpoint, one map table, one rule package |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

```gherkin
Feature: ACE plan status on the case

  Background:
    Given case "RW-2026-000310" is open with synthetic account "A-0310"
    Given the ACE common module stub holds plan "TDR-SYN-0310" for "A-0310"
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02

  Scenario: AC1 Plan status on the case
    Given plan "TDR-SYN-0310" has status "APPROVED" in ACE with status date 2026-12-10
    When the case record view loads on 2026-12-11
    Then the case shows plan "TDR-SYN-0310" with status "Approved" and date 2026-12-10
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2026-12-11) reads plan_status "APPROVED" for the case
    Then rule R-LIT-02 does not fire for the case because plan_status is not broken

  Scenario: AC2 Broken plan
    Given the case is in route state "PLAN_CURE_PERIOD" with break count 0
    Given plan "TDR-SYN-0310" has status "BROKEN" in ACE with status date 2026-12-14
    When the daily case update runs on 2026-12-15
    Then the case plan status is "BROKEN" with date 2026-12-14
    Then the route state moves to "PLAN_BROKEN" by R-RES-29 and then to "BACK_TO_ROUTE_DECISION" by R-RES-30
    Then the case is in the case owner's queue with a task due in 5 working days, from timer_spec "5 working days" of row R-RES-30 of version "RES-2026.12"
    Then the system writes a decision log entry for each move with the rule ID and the package version "RES-2026.12"

  Scenario: AC3 Status not available
    Given the case holds plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01
    Given ACE returns no status for "TDR-SYN-0310"
    When the daily case update runs on 2026-12-15
    Then the case keeps status "BOOKED" with date 2026-12-01
    Then the case record view shows message MSG-P2-008 with the date 2026-12-01
    Then a break with product "DP04" lists plan "TDR-SYN-0310" for the ACE team

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
    Then a break with check "Lists of values" names the code "SUSPENDED"

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

  Scenario: AC9 No RESTRUCTURE version in force
    Given no RESTRUCTURE version is IN_FORCE on 2026-12-15
    When the daily case update finds plan "TDR-SYN-0310" broken on that date
    Then NoPackageInForce is thrown with MSG-P3-027 for package "RESTRUCTURE"
    Then no decision log entry is written and the route state stays "PLAN_CURE_PERIOD"
    Then the case goes to the exception queue for role "RW-TEAMMGR" with the gap
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
| BR10 | R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are rows of package RESTRUCTURE, evaluated by RuleEvaluator; the result names the rule and the package version, and the action text, owner role and timer spec come from RuleCatalog | D-RCV-36 T5, T6, T7; ADR-012 |
| BR11 | No RESTRUCTURE version in force is a refusal (NoPackageInForce), never a default move | R-UNI-41; D-RCV-36 T7 |

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
| The recovery service identity | Calls the ACE interface and writes the stored plan status through P3 |
| SY-RULES, Drools evaluator | Evaluates package RESTRUCTURE (R-RES-29, R-RES-30, R-RES-31 and R-LIT-02) and reads the catalog row |
| SY-CASEWF, case workflow module | Writes the decision log entry, moves the route state, places the case in the queue, raises the task |
| SY-DECLOG, decision log writer | Writes each entry (Decision log, C) |
| RW-CASEOWN, case owner | Reads the plan status on cases in scope (Case record, R) |
| RW-RESTRUCT, restructuring officer | Reads the plan status on cases in scope (Case record, R) |
| RW-DATASTEW, RW-PLATADM | Read the breaks for the ACE team (Platform administration, R) |

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
| DF-CAS-026 | case_account | account_key | Read |
| DF-ACE-002 | v_ace_account | account_code | Read |
| DF-WRK-018 | task | case_id | Write, through the P3 interface |
| DF-WRK-019 | task | task_code | Write, through the P3 interface |
| DF-WRK-024 | task | due_at | Write, through the P3 interface |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-008 | rule_row | action_text | Read |
| DF-REF-010 | rule_row | owner_role | Read |
| DF-REF-011 | rule_row | timer_spec | Read |
| DF-REF-296 | rule_row | package_version_id | Read |
| DF-REF-298 | rule_row | outputs | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary. The rule_row fields are read by rule ID and package version through RuleCatalog.row and the evaluation result; the story reads no drl_source and no workbook, and it holds no rule table of its own.

### 12. Contract

**Job step: plan status in JOB-02 Case creation.** Trigger: after the case creation step of JOB-02, daily. Input: open cases and their account numbers; ACE plan statuses. Output: stored plan status per case; rule events for broken plans; breaks for the data steward. Rule evaluation: RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate) for each case whose status changed, with the rule ID and the package version written to the decision log. The package is loaded, approved and rolled back through RWB-E1-073 and RWB-E2-042; this story only evaluates it. Events published: CaseStateChanged (EV-05) by P3 for each route move. Idempotency key: case ID + plan reference + status + status date. Restart: a rerun skips every case whose stored status and date equal the ACE values.

**Endpoint (new, recorded in additions).**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /api/recovery/v1/cases/{caseId}/plan-status | Path: caseId | PlanStatus: planRef, status, statusDate, live (true when read from ACE now), messageCode | 401 (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 not found or out of scope (MSG-P4-003) | Case record, R | Read only; writes nothing |

**Published interfaces called.**

```java
// P3 recovery.casewf.rules (published, RWB-E1-072)
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
RuleRow RuleCatalog.row(String ruleId, String packageVersion);
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
| PlanEventMap | Reference table | Rows: ACE status, route state, rule event; versioned reference data, not a rule table |
| PlanStatusStep | Job | Step of JOB-02 |
| RestructureFacts | Fact builder | Builds the facts for one case: route state, plan_status, break_count and prior_route |
| PlanStatusPanel | React component | Shows plan, status, date and MSG-P2-008 when not live |

- **Database:** the three new recovery_case columns plan_ref varchar(30), plan_status varchar(10), plan_status_as_of date are added by P3 in its migration for this story; no P2 table.
- **Configuration and reference data:** plan event map rows (RW-COE); new list LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED, BROKEN (RW-COE); parameter restructure.max_breaks = 2; package RESTRUCTURE rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 (RW-COE, RWB-E2-042); properties `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 (assumed; DL11). The package version in force per environment is recorded in `config/rule-packages.lock`; the values in this story are as at 16 November 2026.
- **Build steps:**
  1. Build AcePlanClient against a stub of RestructurePlanQuery with batching and the timeout.
  2. Build PlanStatusService compare and write with the idempotency key.
  3. Build RestructureFacts and the RuleEvaluator call with the catalog read for action text, owner role and timer spec.
  4. Build the event lookup with PlanEventMap and the CaseEvents.raise call; handle DecisionLogUnavailableException and NoPackageInForce.
  5. Build the exception writes for no status, unknown codes and the no-package path.
  6. Build PlanStatusStep in JOB-02.
  7. Build the endpoint with live read and fallback, and PlanStatusPanel.
- **Feature flag:** `rwb.integration.ace-plan-status`.
- **Done when:** the tests in section 16 pass and the SIT run against the ACE stub moves a broken plan case to the case owner's queue, with the rule ID and the package version on every decision log entry.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-008 | Plan status shown from the stored value | The ACE plan status is from {date}. Today's status was not returned. |
| MSG-GEN-006 | ACE common module unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | Decision log write failed on a broken plan | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "RESTRUCTURE" and the business date only, never a case fact.

### 15. Screens and states

SCR-03 Case record, states loading and read only: the plan status panel shows the plan reference, status, date and, when not live, MSG-P2-008. SCR-14 Treatment record, state broken, shows the broken plan once the case returns to the route decision.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-002-01 | AC1, BR1, BR2, BR6, BR10 | System | ACE stub plan TDR-SYN-0310 APPROVED |
| TC-E2-002-02 | AC2, BR4, BR5, BR10 | System | Case in PLAN_CURE_PERIOD; ACE plan BROKEN |
| TC-E2-002-03 | AC3, BR7 | System | ACE stub returns no plan |
| TC-E2-002-04 | AC4 | Resilience | ACE stub delayed 3 seconds |
| TC-E2-002-05 | AC5, BR3 | System | ACE stub returns SUSPENDED |
| TC-E2-002-06 | AC6, BR9 | System | Step run twice on 2026-12-15 |
| TC-E2-002-07 | AC7, BR8 | System | Decision log store stopped |
| TC-E2-002-08 | AC8 | System | Case owner with scope Own and a case of another owner |
| TC-E2-002-09 | AC9, BR11 | System | No RESTRUCTURE version in force on 2026-12-15 |
| TC-E2-002-10 | Access | Access | RW-REFADM (no Case record right) calls GET /cases/{caseId}/plan-status; refused with MSG-P4-002 |
| TC-E2-002-11 | Principle 5 | Resilience | Decision log write forced to fail on the R-RES-29 move; route state unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: status codes, the event map, maximum breaks, batch size, timeout, rule rows and package versions are rows or properties.
- No personal data in logs, tests, workflow history or prompts: logs hold case IDs and plan references, never account numbers.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the plan comes from RestructurePlanQuery and no ACE table is read.
- A read of the plan status writes nothing.
- The rule package is loaded and approved through RWB-E1-073; this story evaluates it and never reads drl_source or the workbook.
- The decision log entry is written before the route state moves.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module | Program 5.2; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39, R-UNI-40 | TC-E2-002-01, TC-E2-002-04, TC-E2-002-06, TC-E2-002-07 |
| REQ-CHO-002 | Plan status change visible on the case | Program 5.3; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-29, R-RES-30, R-RES-31, R-LIT-02 | TC-E2-002-02, TC-E2-002-03, TC-E2-002-05, TC-E2-002-08, TC-E2-002-09 |

### 19. Out of scope

- Creating or changing a plan: ACE, under DL14.
- The treatment record and plan timers: RWB-E2-004.
- Booking confirmation of the plan: RWB-E2-007.
- Authoring, approval and rollback of package RESTRUCTURE: RWB-E2-042 and RWB-E1-073.
- The full restructure route in the Workbench: Epic 3.
---

## RWB-E2-003 Customer's other products on the case

| Item | Value |
|---|---|
| Story key | RWB-E2-003 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CHO-03 Read customer facts from ACE |
| Requirement IDs | REQ-CHO-003, REQ-RDF-010 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.1 and 5.3 |
| L3 process | 06 Take over and own the case |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-069, RWB-E1-007 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the customer's other products and their status on the case, read from the product holding ACE holds for each person**, so that **I can see the whole relationship before I decide a route**.

### 2. Business rationale

A case owner deciding a route today looks up the customer's other loans and deposits in other systems. ACE holds the customer product holding it receives from SCBPDM (DL20, INT-04), keyed by person_key. This story reads v_ace_party_product for the borrowers and co-borrowers of the case, shows each product with its status and business date, marks the list stale when the holding is older than the expected business date, and masks account numbers by role. Nothing is copied into a Workbench table; the view is the record. It meets REQ-CHO-003 and REQ-RDF-010.

### 3. Preconditions

- RWB-E1-069 (read-only ACE source views, grants and boundary rule) and RWB-E1-007 (adapters) are done; the case record view (SCR-03) is in production from Epic 1.
- v_ace_party_product ships in V0003, the Section B migration of RWB-ACE-001 (DL43); the feature stays behind its flag until V0003 is applied in the environment.
- v_ace_customer and v_ace_contact are granted SELECT to the recovery service identity.
- The masking rules for v_ace_party_product.account_no are loaded (DL26; assumed: unmasked for RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL and RW-GUARANT, masked to the last four digits for every other role).
- The list LOV-PRODUCT-STATUS is loaded (values: ACTIVE, DELINQUENT, CLOSED, WRITTEN_OFF).
- The ACE PII logging service is available.

### 4. Flow

1. Case owner: opens SCR-03 Case record for a case in scope.
2. Front end: calls GET /cases/{caseId}/customer-products (API-P2-011).
3. System: checks the Case record right and the scope of the case.
4. System: reads the borrower and co-borrower parties of the case through the P3 CaseQuery.
5. System: reads each person's rows from v_ace_party_product by person_key through the P2 CustomerProductsReader, excluding the account_key values already linked to the case.
6. System: compares data_as_of of the holding with the expected business date of DP02; if older, sets the stale marker.
7. System: applies the masking rule for the caller's role to each account_no.
8. System: writes one PII access event (user, case, person keys, fields shown) through the ACE PII logging service.
9. Front end: shows each product with product type, masked or clear account number, status and business date; a stale list shows MSG-P1-001.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The customer product holding is older than the expected business date | The last loaded products show with a stale marker; a stale read is logged | MSG-P1-001 | AC2 |
| X2 | The caller's role is not allowed to see account numbers | Account numbers are masked to the last four digits | None | AC3 |
| X3 | The customer holds no other product | An empty list shows | MSG-P2-017 | AC4 |
| X4 | The case is outside the caller's scope | Refused | MSG-P4-003 | AC5 |
| X5 | The PII access log cannot be written | The products are not returned; the request fails | MSG-GEN-006 | AC6 |
| X6 | A role without the Case record right calls the endpoint | Refused; nothing is shown | MSG-P4-002 | TC-E2-003-07 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the ACE views (RWB-E1-069) and the case record view; no other Epic 2 story |
| Negotiable | Masking, product status codes and the parties shown are data rows |
| Valuable | The case owner sees the relationship without a lookup in another system |
| Estimable | One read service, one endpoint, one React panel, one view |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

```gherkin
Feature: Customer's other products on the case

  Background:
    Given case "RW-2026-000410" has borrower "C-0410" and linked synthetic account "A-0410"
    Given the expected business date of the customer product holding is 2026-12-14

  Scenario: AC1 Other products shown
    Given "C-0410" holds a revolving credit line "A-0411" with status "ACTIVE" and a personal loan "A-0412" with status "DELINQUENT" in v_ace_party_product, both with data as of 2026-12-14
    When the case record view loads for a case owner
    Then the other products panel shows 2 products with their type and status
    Then each product shows the business date 2026-12-14
    Then the system does not list account "A-0410" because its account_key is on the case

  Scenario: AC2 Holding older than the business date
    Given v_ace_party_product holds no row for 2026-12-14 and its last rows are for 2026-12-13
    When the view loads
    Then the 2 products show with data as of 2026-12-13
    Then the panel shows message MSG-P1-001 with product "Customer products" and date 2026-12-13
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
| BR1 | Customer product facts are read from v_ace_party_product, which ACE holds from SCBPDM | DL20; INT-04; RWB-ACE-001 |
| BR2 | Products of every party with role borrower or co-borrower on the case are shown, except accounts already on the case, matched on account_key | LOV-PARTY-ROLE; story intent |
| BR3 | Each product shows the business date of its holding; a holding older than the expected business date shows as stale | REQ-RDF-009; VR-P2-001-1 |
| BR4 | Account numbers are masked by role on the masking rules | REQ-RDF-010; CTL-11; DL26 |
| BR5 | Every read of customer data is logged to the PII log with who, what, when and which record | INT-22; REQ-RDF-010 |
| BR6 | Product status codes are those in LOV-PRODUCT-STATUS; an unknown code is held on the data quality break list | DQ-020, DQ-027 Lists of values |
| BR7 | The products are not copied into a Workbench table; the view is read on each request | D-RCV-35 U1; tier map section 9.1 |

### 9. State transitions

None. This story does not change a case status. It reads only; the PII access log receives one event per read.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads other products on cases in scope, account numbers clear (Case record, R) |
| RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Read other products on cases in scope, account numbers clear (assumed; DL26) |
| RW-PHONECOL, RW-CONDUCT and other roles with Case record R | Read other products on cases in scope, account numbers masked |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rule rows |
| The recovery service identity | Reads v_ace_party_product for the endpoint (Case record, R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-004 | recovery_case | primary_person_key | Read |
| DF-CAS-031 | case_party | case_id | Read |
| DF-CAS-032 | case_party | person_key | Read |
| DF-CAS-033 | case_party | party_role | Read |
| DF-CAS-026 | case_account | account_key | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-280 | v_ace_party_product | person_key | Read |
| DF-ACE-281 | v_ace_party_product | account_no | Read |
| DF-ACE-282 | v_ace_party_product | account_key | Read |
| DF-ACE-283 | v_ace_party_product | product_type | Read |
| DF-ACE-284 | v_ace_party_product | product_status | Read |
| DF-ACE-285 | v_ace_party_product | data_as_of | Read |
| DF-REF-035 | role | role_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. v_ace_party_product is read through the P2 CustomerProductsReader, never from a public table.

### 12. Contract

**Endpoint (API-P2-011).**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /cases/{caseId}/customer-products | Path: caseId | CustomerProducts: dataAsOf, stale, messageCode, items (personKey, partyRole, productType, accountNo masked by role, productStatus, dataAsOf) | 401 (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 PII log unavailable (MSG-GEN-006) | Case record, R | Read only |

**Published interfaces called.**

```java
// P2 recovery.integration.ace, reads recovery.v_ace_party_product
List<PartyProductView> CustomerProductsReader.otherProducts(List<String> personKeys, Set<String> excludeAccountKeys);
// P1 recovery.data.api
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
| CustomerProductsReader | Repository | Read-only select from v_ace_party_product by person_key; no other ACE access |
| OtherProductsPanel | React component | List with product type, account number, status, date; stale banner MSG-P1-001; empty state MSG-P2-017 |

- **Database:** no new table. The product holding stays in ACE and is read through v_ace_party_product; no copy is written to the recovery schema.
- **Configuration and reference data:** masking rule rows for v_ace_party_product.account_no (RW-COMPLY, DL26); LOV-PRODUCT-STATUS (RW-DATASTEW); party roles shown, BORROWER and CO_BORROWER, as a property `rwb.customer.products.party-roles`.
- **Build steps:**
  1. Agree the PartyProductView and the reader with the P2 squad; build a stub of v_ace_party_product for tests.
  2. Build CustomerProductsService with party selection and exclusion of case accounts by account_key.
  3. Add the freshness check and the stale marker.
  4. Add masking through the ACE Masking service and the PII access event; fail the call when the log fails.
  5. Build the endpoint with the access and scope checks.
  6. Build OtherProductsPanel with its loading, list, stale and empty states.
- **Feature flag:** `rwb.integration.customer-products`.
- **Done when:** the tests in section 16 pass and the panel shows synthetic products in SIT with masking for RW-PHONECOL.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | Customer product holding older than the expected business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-017 | No other product held | The customer holds no other product with the bank in the customer product holding of {date}. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | PII access log unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-03 Case record, states loading and read only: the other products panel shows the list, a stale banner when the holding is older than the expected business date, and an empty state when there is none. A role with masking sees account numbers masked to the last four digits.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-003-01 | AC1, BR1, BR2, BR3 | System | Synthetic customer C-0410 with two other products in v_ace_party_product |
| TC-E2-003-02 | AC2, BR3 | System | Holding last loaded 2026-12-13 |
| TC-E2-003-03 | AC3, BR4 | System | RW-PHONECOL and RW-CASEOWN read the same case |
| TC-E2-003-04 | AC4 | System | Customer C-0420 with no other product |
| TC-E2-003-05 | AC5 | System | Case owner with scope Own and a case of another owner |
| TC-E2-003-06 | AC6, BR5 | Resilience | PII logging stub refuses the event |
| TC-E2-003-07 | Access | Access | RW-REFADM (no Case record right) calls GET /cases/{caseId}/customer-products; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: masking, product status codes and the party roles shown are rows or properties.
- No personal data in logs, tests or prompts; test data is synthetic, application logs hold case and person keys only.
- No read of another module's tables: v_ace_party_product and v_ace_customer are read through the reader over the views; parties through the P3 interface.
- No customer data is returned without its PII access event.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-003 | Customer and product facts from the ACE customer profile | Program 5.3; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | None | TC-E2-003-01, TC-E2-003-02, TC-E2-003-04, TC-E2-003-05 |
| REQ-RDF-010 | Access by role and masking under PDPA | Program 5.1; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | None | TC-E2-003-03, TC-E2-003-06 |

### 19. Out of scope

- Merging a duplicate case for the same customer and product (R-UNI-17, REQ-CHO-010): Epic 3 backlog.
- The role to masking rule table: RWB-E1-037.
- Balances of the other products: v_ace_party_product carries the product type and status only (DL20).
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
| Decision | D-RCV-36; ADR-011; ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-028, RWB-E1-045, RWB-E1-072, RWB-E2-042 |
| Status | Ready for build |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the treatment record (TDR, settlement, deed in lieu: terms, approval, booking, outcome) and its plan timers held in the Workbench, with the treatment data product for reporting**, so that **TDR and deed in lieu run inside the Workbench from Epic 2 and every plan has a record and a clock**.

### 2. Business rationale

Today a restructure plan is agreed in ACE and NLEADS, and nothing in recovery holds its terms or watches its payment dates, so a missed installment is found late. About 3,000 restructure accounts a month reach the restructure process (NFR-005) and deed in lieu is planned at 1,000 cases a month in 2027 (NFR-006). This story creates the treatment record with its terms and approval, starts the installment timer from the first due date and starts the cure period when a payment is missed. It meets REQ-CHO-006, REQ-CHO-007 and REQ-RDF-014. The measure is that every approved plan has one treatment row and a running installment timer the day it is recorded.

The plan rules R-RES-25 and R-RES-27 are rows of package RESTRUCTURE under ADR-012, fixed by D-RCV-36 on 16 November 2026, and the plan timers are scheduled through the TimerScheduler port (D-RCV-36 T2). JOB-05 stays the Quartz implementation in Epics 1 and 2, so Epic 3 can swap in Temporal durable timers (ADR-011) without changing a caller.

### 3. Preconditions

- RWB-E1-018 is done: the case record exists with its route state.
- RWB-E1-028 is done: the timer engine runs and JOB-05 Timer check is the Quartz implementation of TimerScheduler, so every caller schedules, pauses, resumes and cancels through TimerScheduler.
- RWB-E1-045 is done: CURE_PERIOD_DAYS and `plan.warn-days` are product parameters in force (values per DL22; `plan.warn-days` assumed 3).
- RWB-E1-072 is done: RuleEvaluator, RuleCatalog and the rule package store exist.
- RWB-E2-042 is done: package RESTRUCTURE is in force with rows R-RES-25 and R-RES-27, and each row carries action_text, owner_role and timer_spec.
- The decision log writer of RWB-E1-027 is available through the P7 published interface.
- LOV-TIMER carries the value INSTALLMENT_DUE (new list value, see Additions), loaded by the reference data administrator.
- The approval of the plan is already written to the decision log by its approver's flow (P7), so a decision log entry ID exists.
- The caller of `TreatmentRecords.recordApproved(...)` is the ACE plan status reader (RWB-E2-002) under SY-CASEWF, or a test harness in SIT.

### 4. Flow

1. ACE plan status reader (SY-CASEWF): calls `TreatmentRecords.recordApproved(...)` with the case ID, treatment type, terms, approval level, the approval's decision log entry ID and the first due date.
2. Treatment service: checks the case exists and is open through the P3 case interface, and that the decision log entry exists and names an approver through the P7 interface.
3. Treatment service: checks the required fields and the list values; writes one `treatment` row and the TreatmentApproved event (EV-10) in the outbox, in one transaction.
4. Plan timer listener (P3): consumes TreatmentApproved; finds the case in route state BOOKED_IN_ALS_NLEADS and the terms carrying a first due date (event SCHEDULE_SET).
5. SY-RULES: builds PlanTimerFacts for the case (treatment type, product group, route state, first due date, installments) and calls RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate); the R-RES-25 row returns the action "start the plan timers", the to state PLAN_RUNNING, the package version and the timer spec.
6. Plan timer listener: writes the decision log entry with rule R-RES-25 and the package version; only after that succeeds calls TimerScheduler.schedule with the INSTALLMENT_DUE TimerSpec, sets the route state to PLAN_RUNNING and publishes CaseStateChanged (EV-05).
7. JOB-05 Timer check, the Quartz implementation of TimerScheduler: at the timer's expiry publishes TimerDue (EV-18) with the timer type and the treatment ID, and sets the timer status to EXPIRED.
8. Payment matching (P8, JOB-07): publishes PaymentMissed (EV-12) when no payment matched the installment.
9. Plan timer listener: consumes PaymentMissed; calls RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate) for R-RES-27; writes the decision log entry with the rule ID and the package version, then calls TimerScheduler.schedule with the CURE_PERIOD TimerSpec built from CURE_PERIOD_DAYS for the product, and sets the route state to PLAN_CURE_PERIOD.
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
| X9 | No RESTRUCTURE version is IN_FORCE on the business date | NoPackageInForce; no decision log entry, no timer and no route state change; the case goes to the exception queue for a person | MSG-P3-027 | AC13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the case record, the timer engine, the product parameters, the evaluator of RWB-E1-072 and the RESTRUCTURE package of RWB-E2-042 |
| Negotiable | Timer lengths and warning days are product parameters; the story fixes the record and the timer behavior |
| Valuable | Every approved plan has a record, a due date and a cure period that starts by rule |
| Estimable | One table, one service, one listener, one extract step, one rule package |
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
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-25 and R-RES-27

  Scenario: AC1 Treatment created
    Given a TDR plan approved for "RW-2026-000201" with 36 installments, offer amount 850000.00 baht, approval level "L4" and decision log entry "DLE-9001"
    When the record is written
    Then one treatment exists with type "RESTRUCTURE", installments 36, offer amount 850000.00, approval level "L4", decision log entry "DLE-9001" and the case link
    Then booked at is empty until the booking is confirmed
    Then one TreatmentApproved event is in the outbox with the treatment ID and the case ID

  Scenario: AC2 Timer set
    Given a plan with the first payment due on 2026-12-31
    When the record is written and the plan timer listener processes TreatmentApproved
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2026-12-01) returns rule R-RES-25 and package version "RES-2026.12"
    Then one decision log entry with rule "R-RES-25" and version "RES-2026.12" is written first
    Then one "INSTALLMENT_DUE" timer exists with expires at 2026-12-31 23:59 Asia/Bangkok, warn at 2026-12-28 and status "RUNNING", scheduled through TimerScheduler
    Then the case route state is "PLAN_RUNNING" and its status stays "IN_PROGRESS"
    Then when the clock passes 2026-12-31 23:59 and JOB-05, the Quartz implementation of TimerScheduler, runs, the system publishes a TimerDue event with timer type "INSTALLMENT_DUE" and the treatment ID
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
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2027-01-01) returns rule R-RES-27 and package version "RES-2026.12"
    Then the system writes a decision log entry with rule "R-RES-27" and version "RES-2026.12" first
    Then one "CURE_PERIOD" timer exists with expires at 2027-01-31, scheduled through TimerScheduler
    Then the case route state is "PLAN_CURE_PERIOD"

  Scenario: AC13 No RESTRUCTURE version in force
    Given no RESTRUCTURE version is IN_FORCE on 2026-12-01
    When the plan timer listener processes TreatmentApproved for "RW-2026-000201"
    Then NoPackageInForce is thrown with MSG-P3-027 for package "RESTRUCTURE"
    Then no decision log entry, no timer and no route state change are written
    Then the case goes to the exception queue for role "RW-TEAMMGR" with the gap

  Scenario: AC14 Plan timers go only through TimerScheduler
    Given the plan timer listener holds an "INSTALLMENT_DUE" TimerSpec for case "RW-2026-000201"
    When the listener schedules the timer
    Then the timer is created by TimerScheduler and carries the case ID, the treatment ID, the timer type and the expiry
    Then a component that inserts into the timer table without TimerScheduler fails the boundary test and the build
    Then JOB-05, the Quartz implementation of TimerScheduler, is the only code that expires the timer
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
| BR10 | R-RES-25 and R-RES-27 are rows of package RESTRUCTURE, evaluated by RuleEvaluator; the result names the rule and the package version, and the action text, owner role and timer spec come from RuleCatalog | D-RCV-36 T5, T6, T7; ADR-012 |
| BR11 | A plan timer is scheduled, paused, resumed and cancelled only through TimerScheduler; JOB-05 is its Quartz implementation in Epics 1 and 2 | D-RCV-36 T2; RWB-E1-028 |
| BR12 | No RESTRUCTURE version in force is a refusal (NoPackageInForce), never a default timer or move | R-UNI-41; D-RCV-36 T7 |

### 9. State transitions

The case status does not change (it stays In progress). The route state changes:

| From | Event | Condition | To |
|---|---|---|---|
| BOOKED_IN_ALS_NLEADS | SCHEDULE_SET | first_due_date set (R-RES-25) | PLAN_RUNNING |
| PLAN_RUNNING | PAYMENT_MISSED | due date passed and no payment matched (R-RES-27) | PLAN_CURE_PERIOD |

Timer status: RUNNING to EXPIRED when the INSTALLMENT_DUE timer passes its expiry, through TimerScheduler and its Quartz implementation JOB-05.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Records the treatment through the published interface; schedules the plan timers through TimerScheduler and writes the route state (Case record CRU; Treatment and offer R through the interface) |
| SY-RULES, Drools evaluator | Evaluates R-RES-25 and R-RES-27 in package RESTRUCTURE and reads the catalog row |
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
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-296 | rule_row | package_version_id | Read |
| DF-REF-298 | rule_row | outputs | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through the P7 interface |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read, through the P7 interface, for the approval entry |

Field IDs are those in the Logical Data Model and Data Dictionary. The rule_row fields are read by rule ID and package version through the evaluation result and RuleCatalog; the story reads no drl_source and no workbook.

### 12. Contract

**GET /api/recovery/v1/treatments/{treatmentId}** (S2 endpoint; reads this story's record)

| Item | Value |
|---|---|
| Request | Path `treatmentId` (uuid) |
| Response | 200 `Treatment`: `id`, `caseId`, `decisionLogId`, `treatmentType`, `proposedBy`, `proposedAt`, `offerAmount`, `haircutAmount`, `installments`, `validUntil`, `approvalLevel`, `bookedAt`, `outcome`, `outcomeAt` |
| Errors | 401 (MSG-P4-001); 403 no Treatment and offer R (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 |
| Authorization | Treatment and offer, right R |
| Idempotency | Not applicable |

**GET /api/recovery/v1/cases/{caseId}/timers** (P3) returns `Timer[]`; Case record R. Used to check AC2, AC12 and AC14.

**Rule evaluation.** RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate) for R-RES-25 and R-RES-27, with the rule ID and the package version written to the decision log. The package is loaded, approved and rolled back through RWB-E1-073 and RWB-E2-042; this story only evaluates it.

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

**Published interfaces called** (package recovery.casewf.rules and package recovery.casewf.timers):

```java
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
RuleRow RuleCatalog.row(String ruleId, String packageVersion);
void TimerScheduler.schedule(TimerSpec t);
void TimerScheduler.cancel(UUID timerId);
```

**Events**

| Event | Direction | Payload used |
|---|---|---|
| TreatmentApproved (EV-10) | Published by the treatment service; consumed by the plan timer listener | treatmentId, caseId, terms (firstDueDate, installments) |
| CaseStateChanged (EV-05) | Published | caseId, fromState, toState, ruleId, decisionLogEntryId |
| TimerDue (EV-18) | Published by JOB-05 | timerId, caseId, timerType |
| PaymentMissed (EV-12) | Consumed | treatmentId, dueDate, amountDue |

**Jobs.** JOB-05 Timer check (every 5 minutes) is the Quartz implementation of TimerScheduler and raises TimerDue for INSTALLMENT_DUE timers. JOB-15 Reporting extract (nightly 01:30) adds the DP04 treatment extract; idempotency key is the business date; a rerun replaces that date's extract.

### 13. Solution plan

**Package.** S2 package `recovery.treatment.record` for the treatment record; P3 package `recovery.casewf.plan` for the plan timer listener; P1 package `recovery.data.products.treatment` for the extract step.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TreatmentEntity | Entity | Maps `treatment` with the standard columns and `first_due_date` |
| TreatmentRepository | Repository | Reads and writes `treatment` only |
| TreatmentRecordService | Service | Validates the command, writes the row and the TreatmentApproved outbox row in one transaction |
| TreatmentRecords | Published interface | The interface in section 12 |
| PlanTimerListener | Listener | Consumes TreatmentApproved and PaymentMissed; calls RuleEvaluator; writes the decision log entry, then the timer through TimerScheduler and the route state |
| PlanTimerService | Service | Builds the INSTALLMENT_DUE and CURE_PERIOD TimerSpecs from the due date and the product parameters and schedules them through TimerScheduler |
| PlanTimerFacts | Fact builder | Builds the facts for one case: treatment type, product group, route state, first due date and installments |
| TreatmentExtractStep | Job | Spring Batch step in JOB-15 writing DP04 rows with the derived status |

**Database.** Flyway migration `V<next>__rwb_e2_004_treatment.sql` creates `treatment` as in Recovery Workbench Physical Schema v6 plus `first_due_date date`, with `ix_treatment_case_id` and `ix_treatment_decision_log_id`; adds `timer.treatment_id uuid` with index `ix_timer_treatment_id`. Unique index `ix_timer_plan_due` on `(treatment_id, timer_type, expires_at)` stops a second timer for the same due date.

**Configuration and reference data.** LOV-TIMER value INSTALLMENT_DUE (reference data administrator). CURE_PERIOD_DAYS per product and `plan.warn-days` (center of excellence, RWB-E1-045; values DL22). Package RESTRUCTURE rows R-RES-25 and R-RES-27 (center of excellence, RWB-E2-042). Event consumer retry limit 3 (NFR-026). The package version in force per environment is recorded in `config/rule-packages.lock`; the values in this story are as at 16 November 2026.

**Build steps**

1. Write the migration; prove the table, the new columns and the unique timer index.
2. Build `TreatmentRecordService` with the checks of X1, X2, X3 and X8, the outbox write and the published interface.
3. Build `PlanTimerService` with the due date, warning and cure period calculation through `ProductParameterService`, returning TimerSpecs for TimerScheduler.
4. Build `PlanTimerListener` for TreatmentApproved: idempotency on the event ID, RuleEvaluator evaluation of R-RES-25, decision log first, then TimerScheduler.schedule, the route state and CaseStateChanged.
5. Add the X4 path and the X9 path: no rule match or no package in force sends the case to the exception queue with MSG-P3-005 or MSG-P3-027.
6. Add PaymentMissed handling with R-RES-27 through RuleEvaluator and the cure period timer through TimerScheduler.
7. Build `TreatmentExtractStep` in JOB-15 with the status derivation of BR8.
8. Add the boundary test that refuses a direct write to the timer table outside TimerScheduler.
9. Write the tests in section 16 with a controlled clock.

**Feature flag.** `rwb.p3.plan-timers`. Off: treatments are recorded and no plan timers start.

**Done when.** The tests in section 16 pass, and the SIT run of 50 synthetic plans shows 50 treatment rows, 50 INSTALLMENT_DUE timers and 50 DP04 rows the next morning, with the rule ID and the package version on every plan decision log entry.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field or the decision log entry is missing | Enter {field}. |
| MSG-GEN-003 | The first due date is before the proposed date | {field} cannot be before {other}. |
| MSG-P3-005 | The case is closed, or not in the state the rule expects | This case cannot move to {state} from {current}. |
| MSG-P7-003 | The decision log write fails | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The treatment data product is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-003 | The installment timer is inside its warning period, shown on the case | {timer} ends on {date}. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P4-002 | A role without Treatment and offer R reads a treatment | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "RESTRUCTURE" and the business date only, never a case fact.

### 15. Screens and states

No new screen. SCR-14 Treatment record (Epic 2 record view) shows the treatment in state Approved or Booked; SCR-03 Case record shows the INSTALLMENT_DUE and CURE_PERIOD timers with their due dates (RWB-E2-015). A case sent to the exception queue under X4 or X9 shows on SCR-09.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-004-01 | AC1, BR1 | System | Restructure, 36 installments, 850000.00 baht, entry DLE-9001 |
| TC-E2-004-02 | AC2, BR3, BR5, BR10, BR11 | System | First due date 2026-12-31; clock moved past expiry |
| TC-E2-004-03 | AC3, BR8 | System | Ten treatments over three products, two booked |
| TC-E2-004-04 | AC4, BR2 | System | Restructure with no first due date |
| TC-E2-004-05 | AC5, BR1 | System | Unknown decision log entry DLE-0000 |
| TC-E2-004-06 | AC6, BR2 | System | First due date one day before the proposal |
| TC-E2-004-07 | AC7, BR9 | System | Case in route state WITH_FCR_OFFICER |
| TC-E2-004-08 | AC8, BR7 | System | Same TreatmentApproved event twice |
| TC-E2-004-09 | AC9, BR6 | System | Decision log store stopped in the test container |
| TC-E2-004-10 | AC10 | System | JOB-15 forced to fail on 2026-12-02 |
| TC-E2-004-11 | AC11 | System | Closed case |
| TC-E2-004-12 | AC12, BR4, BR10 | System | PaymentMissed for due date 2026-12-31 |
| TC-E2-004-13 | AC13, BR12 | System | No RESTRUCTURE version in force on 2026-12-01 |
| TC-E2-004-14 | AC14, BR11 | System | A component that inserts into the timer table without TimerScheduler |
| TC-E2-004-15 | Access | Access | RW-PHONECOL (no Treatment and offer right) reads `GET /treatments/{treatmentId}`; refused with MSG-P4-002 |
| TC-E2-004-16 | Principle 5 | Resilience | Decision log write forced to fail at timer start; no timer, no state change |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. Periods, warning days and the rules are reference rows or package rows; treatment types and outcomes come from LOV-TREATMENT and LOV-TRT-OUTCOME.
- No personal data in logs, tests, workflow history or prompts beyond the IDs in the payload. Amounts are synthetic in tests.
- No read of another module's tables; ACE data only through recovery.v_ace_* views. P3 reaches the treatment only through `TreatmentRecords`; S2 reaches the case only through the P3 case interface; P1 reads treatments only through `changedSince`.
- The decision log entry is written before the timer and the route state; never the other way round.
- Plan timers are scheduled, paused, resumed and cancelled only through TimerScheduler; no class writes the timer table directly.
- The treatment row is never deleted; a cancellation is an outcome.
- The rule package is loaded and approved through RWB-E1-073; this story evaluates it and never reads drl_source or the workbook.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer with type, terms, approval and outcome | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25 | TC-E2-004-01, TC-E2-004-04 to TC-E2-004-06, TC-E2-004-11, TC-E2-004-15 |
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25, R-RES-27, R-UNI-39, R-UNI-40 | TC-E2-004-02, TC-E2-004-07 to TC-E2-004-09, TC-E2-004-12 to TC-E2-004-14, TC-E2-004-16 |
| REQ-RDF-014 | Stage 2 data products for plans and treatments exist before the first treatment | Business Requirements Epic 2, section 4; Program, section 5.1 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-004-03, TC-E2-004-10 |

### 19. Out of scope

- The offer builder, treatment screens and submission for approval (S2, Epic 3, FEAT-TRT-01).
- Reading the ACE plan status that calls this interface (RWB-E2-002).
- Booking confirmation from the ALS load and the booked at date (RWB-E2-007).
- Payment matching that raises PaymentMissed (P8, JOB-07).
- Broken plan handling after the cure period (R-RES-29 to R-RES-32, Epic 3).
- Temporal durable timers that replace the Quartz implementation in Epic 3 (ADR-011); the TimerScheduler port is the seam.
- Authoring, approval and rollback of package RESTRUCTURE (RWB-E2-042 and RWB-E1-073).
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
| Depends on | RWB-E1-008, RWB-E1-039, RWB-E2-041 |
| Status | Ready for build |

### 1. Story

As an **internal auditor (RW-AUDIT)**, I want **to query the decision log by case or a population of cases, decision, approver, date and rule version, with the hash chain checked on every entry returned, and to export the result**, so that **an audit question is answered from the log in minutes, and I can rely on each entry I am given**.

### 2. Business rationale

Audit and the regulator ask for the decision history of a sample of cases: inputs, versions, approver and final call. Today this is assembled by hand from e-mails and files. This story gives one query over the append-only log, filtered by the caller's scope, with each returned entry checked against the chain and a flag on any entry that does not match. It meets REQ-DRI-012 and NFR-036 (an audit request answered inside its deadline). The measure is the time to answer an audit sample: the first page of a query over 10,000 matching entries in 3 seconds or less (assumed; DL11).

### 3. Preconditions

- RWB-E1-008 is done: the store, the canonical form and the verifier.
- RWB-E1-039 is done: access events are written to the decision log.
- RWB-E2-041 is done: the rule change report gives the count of decisions per rule package version, for reconciliation.
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
3. System: checks the Treatment and offer right and the case scope; reads the case, accounts, collateral, latest valuation, plan terms and documents through the owning modules' interfaces and the P1 interfaces over the ACE views.
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E2-004, RWB-E1-069, RWB-E1-007, RWB-E1-072, RWB-E2-042 |
| Status | Ready for build |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the booked terms of each approved restructure or settlement compared with the account as ACE holds it after the next ALS batch, with a task when the booking is missing or differs**, so that **every approved decision is confirmed as booked in the core bank without a file the Workbench has to load**.

### 2. Business rationale

The officer books restructures and settlements in ALS by hand (INT-03), and nothing checks today that the booked terms equal the approved terms. ACE ingests the ALS batch and the booked terms appear on the account. This story compares each approved treatment with v_ace_account for the business date once the ACE batch for ALS is COMPLETE, marks the treatment booked when the terms match, and raises a task to the officer when the booking is missing or to Credit Administration when the terms differ. It meets REQ-CHO-008 and is measured by REC-03 (approved treatments against bookings, zero after two days).

The compared terms, the tolerance and the outcomes are rows of package BOOKING_MATCH under ADR-012, fixed by D-RCV-36 on 16 November 2026. SY-RULES evaluates the package through RuleEvaluator for each treatment and account, the result names the row and the package version, and the service holds no comparison code of its own.

### 3. Preconditions

- RWB-E2-004 (treatment entity) and RWB-E1-069 (read-only ACE source views) are done; v_ace_account is granted SELECT to the recovery service identity.
- RWB-E1-007 (adapters and IdempotencyGuard) is done; the recovery service identity reads the views only.
- RWB-E1-072 is done: RuleEvaluator and the rule package store exist.
- RWB-E2-042 is done: package BOOKING_MATCH is in force with version "BKG-2026.12" and rows for RESTRUCTURE and SETTLEMENT: for RESTRUCTURE compare tdr_flag, last_tdr_date and principal_outstanding against offer_amount, and interest_rate against the approved rate; for SETTLEMENT compare settlement_booked_date and settlement_booked_amount against offer_amount; tolerance 0.00 baht (DL25).
- v_ace_batch_status (V0003, RWB-ACE-001, DL43) carries the ALS business date and the COMPLETED status that trigger the match.
- The Section B columns settlement_booked_date and settlement_booked_amount of v_ace_account ship in V0003 with RWB-ACE-001; a settlement is confirmed only once V0003 is applied and the flag is on. A restructure is confirmed from Section A columns alone.
- Parameter `booking.missing.grace_loads` = 1 (one ALS batch after approval).
- Rules R-RES-22 and R-SET-13 are in force.
- TreatmentApproved (EV-10) is published for each approved treatment.

### 4. Flow

1. Scheduler: JOB-08 starts when AceDataReady (EV-26) arrives for ALS with business date D.
2. BookingMatchService: lists approved treatments of type RESTRUCTURE or SETTLEMENT not yet booked, through the treatment interface.
3. BookingMatchService: for each treatment, checks IdempotencyGuard on treatment ID + D; a repeat is skipped.
4. BookingMatchService: reads every account of the case from v_ace_account at business date D through the P1 AccountQuery.
5. BookingMatchService: builds BookingMatchFacts for the treatment and each account (treatment type, approved terms, account fields) and calls RuleEvaluator.evaluate("BOOKING_MATCH", facts, D); the result names the row that decided, the outcome BOOKED, NO_BOOKING or TERMS_DIFFER, the difference terms and the package version.
6. BookingMatchService: when the outcome is BOOKED for every account, calls TreatmentCommands.markBooked with the business date; P8 publishes TreatmentBooked (EV-11); P3 writes the decision log entry and moves the case by R-RES-22 or R-SET-13.
7. BookingMatchService: when the outcome is NO_BOOKING after the grace batches, raises one task WITH_OPS_BOOKING or WITH_OPS_SETTLEMENT for role RW-RESTRUCT with MSG-P2-011; the treatment stays approved.
8. BookingMatchService: when the outcome is TERMS_DIFFER, writes the difference on the treatment and raises one task UNMATCHED_EXCEPTION for role RW-CREDITAD with MSG-P2-012; the treatment stays approved.
9. BookingMatchService: writes the run summary (treatments read, booked, missing, differing) and the REC-03 result to reconciliation_result.

### 5. Exception paths

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

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the treatment entity (RWB-E2-004), the ACE account view, the evaluator of RWB-E1-072 and the BOOKING_MATCH package of RWB-E2-042 |
| Negotiable | Terms compared, tolerance and grace are package rows or parameters |
| Valuable | Every approved restructure and settlement is confirmed as booked or raised |
| Estimable | One matching service, one job, two task paths, one rule package |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

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

### 8. Business rules

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

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| WITH_OPS_BOOKING | BOOKING_CONFIRMED | NLEADS result APPROVED recorded and every account matched | BOOKED_IN_ALS_NLEADS |
| WITH_OPS_SETTLEMENT | SETTLEMENT_BOOKED | Agreement signed and terms booked in ALS | AWAITING_PAYMENT |

The treatment state moves from APPROVED to BOOKED. A missing or differing booking leaves both the route state and the treatment state unchanged.

### 10. Authority

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

### 12. Contract

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

### 13. Solution plan

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

### 14. Validation and messages

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

### 15. Screens and states

SCR-14 Treatment record, states approved and booked: the officer sees booked at, or the booking difference with each term approved and booked. The officer and the Credit Administration officer see their tasks on SCR-01 My work. SCR-29 Posting, which shows the confirmation for all bookings, comes in Epic 4.

### 16. Test cases

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

### 17. Guardrails

- No business value in code: compared terms, tolerance and grace are rows of package BOOKING_MATCH or parameters.
- No personal data in logs, tests, workflow history or prompts; the booking reference holds the account_key, not the account number.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the match reads v_ace_account and v_ace_batch_status through the P1 interfaces (boundary rule, RWB-E1-069).
- No call to ALS; the match reads only what ACE holds for the completed batch.
- No comparison code and no rule table in the service: package BOOKING_MATCH decides, through RuleEvaluator.
- The rule package is loaded and approved through RWB-E1-073; this story evaluates it and never reads drl_source or the workbook.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Booking confirmed from the next day's ALS batch | Program 5.3; Epic 2 3.2 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39 | TC-E2-007-01 to TC-E2-007-09, TC-E2-007-11 |

### 19. Out of scope

- Posting a settlement booking to ALS from the Workbench: FEAT-PAY-06, Epic 4.
- Payment matching to the plan or settlement: JOB-07 and FEAT-OCC-10, Epic 2.
- The SCR-29 Posting screen: Epic 4.
- Authoring, approval and rollback of package BOOKING_MATCH (RWB-E2-042 and RWB-E1-073).
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
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E2-004, RWB-E1-069, RWB-E1-072, RWB-E2-042 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **payments posted in ALS and read from v_ace_payment matched to the running plans each day, with a missed payment event when a due installment has not arrived by the time the ACE batch completes**, so that **a broken plan is known the day after it breaks**.

### 2. Business rationale

Payments are matched to plans by hand today, and a missed installment is found weeks later, after the cure period has gone. ACE ingests the ALS payments and the Workbench reads them through v_ace_payment, keyed by payment_code and account_key. This story matches each payment to the plan installment it pays, keeps anything unmatched on the exception list, and raises PaymentMissed the morning after a due date passes with no payment in a completed ACE batch, which the restructure rules (R-RES-27) and the transfer rules act on. It serves REQ-CHO-007 and REQ-CHO-009, control CTL-41 and the FSD P8 measure "receipts matched the same day".

Payment matching is package PAYMENT_MATCH under ADR-012, fixed by D-RCV-36 T10 on 16 November 2026. The EXACT, PARTIAL and WINDOW rows carry match type, amount tolerance, window, grace and partial floor as decision-table columns, SY-RULES evaluates them through RuleEvaluator, and the decision log names rule R-RES-26 with the package version.

### 3. Preconditions

- RWB-E1-069 is done: v_ace_payment is granted SELECT to the recovery service identity and holds payment_code, account_key, payment_date, payment_amount and data_as_of (V0002).
- v_ace_batch_status (V0003, RWB-ACE-001, DL43) carries the ALS business date and completion; the flag `rwb.payments.matching` stays off in an environment without V0003.
- RWB-E2-004 is done: the treatment record holds running plans with installment amount and installments paid, readable and updatable through TreatmentApi.
- RWB-E1-072 is done: RuleEvaluator, RuleCatalog and the rule package store exist.
- RWB-E2-042 is done: package PAYMENT_MATCH is in force with version "PM-2026.12" and one EXACT row: amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days (assumed).
- The next due date of each plan account is read from v_ace_account.next_installment_date at the same business date.
- P1 has stamped DP01 for the business date and published AceDataReady (EV-26).
- P3 consumes PaymentMissed and applies R-RES-27 and the transfer rules (RWB-E1-021).

### 4. Flow

1. JOB-07 Payment matching: starts when AceDataReady (EV-26) arrives for the ALS source with business date D, and the ACE batch status for ALS is COMPLETE.
2. System: reads the payments posted for business date D from v_ace_payment through the P1 interface: payment_code, account_key, payment_date, payment_amount.
3. System: for each payment, finds the open case of the account_key through the P3 interface; a payment on an account with no open case is listed on the REC-05 business-key break and gets no proceeds row.
4. System: reads the running plans on the case, builds PaymentMatchFacts (installment amount, next due date, payment date, payment amount, treatment type) and calls RuleEvaluator.evaluate("PAYMENT_MATCH", facts, D); a payment on the plan account for the installment amount, dated inside the window before the next due date, matches that installment through the EXACT row.
5. System: writes the decision log entry with rule R-RES-26 and the package version returned in the result; only after that succeeds writes a proceeds row with source CUSTOMER, payment_code and matched_to INSTALLMENT, calls TreatmentApi.recordInstallmentPaid, and writes ProceedsMatched to the outbox in the same transaction.
6. System: a payment that matches no plan installment is written with matched_to UNMATCHED and appears on the exception list for the reconciliation agent (R-UNI-03).
7. System: after all payments, for each running plan whose next due date plus the grace days is before the business date of the completed ACE batch and that has no matched payment for that due date, writes PaymentMissed with treatment ID, due date and amount due.
8. P3: applies R-RES-27 (plan to the cure period) and the transfer rule; the case owner sees the missed payment on the treatment record the same morning.
9. System: writes the run summary (payments read, matched, unmatched, missed events) and the REC-04 result to reconciliation_result.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A payment matches no plan installment | Proceeds row UNMATCHED on the exception list | MSG-P8-001 | AC3 |
| X2 | A payment is on an account with no open case | Listed on the REC-05 business-key break; no proceeds row | None | AC4 |
| X3 | The ACE batch for ALS is not COMPLETE for the business date | JOB-07 does not run; no missed payment is raised from stale data | MSG-P1-001 | AC5 |
| X4 | JOB-07 runs twice for one business date | No second proceeds row and no second event | None | AC6 |
| X5 | A payment arrives on the last day of the window or one day before it opens | The first matches the installment; the second does not match and is held | MSG-P8-001 | AC7 |
| X6 | No PAYMENT_MATCH version is IN_FORCE on the business date | NoPackageInForce; JOB-07 stops before matching and writes no proceeds row and no event | MSG-P3-027, MSG-P8-002 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the ACE payment view (RWB-E1-069), the treatment record (RWB-E2-004), the evaluator of RWB-E1-072 and the PAYMENT_MATCH package of RWB-E2-042 |
| Negotiable | Window, grace days, tolerance and the amount rule are package rows with a version |
| Valuable | A missed installment is known the morning after the due date |
| Estimable | One job, one matcher, one table, one event, one rule package |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against synthetic rows in v_ace_payment |

### 7. Acceptance criteria

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

### 8. Business rules

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
| The recovery service identity, JOB-07 | Runs JOB-07, calls the rule evaluator and reads the ACE views (Write-off and posting U) |
| SY-RULES, Drools evaluator | Evaluates package PAYMENT_MATCH for each payment and returns the row, the outputs and the package version |
| SY-CASEWF, case workflow module | Consumes PaymentMissed and ProceedsMatched |
| SY-DECLOG, decision log writer | Writes the match entry (Decision log C) |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent (Write-off and posting R) |
| RW-CREDITAD, Credit Administration officer | Reads matched and unmatched receipts on SCR-28 (Write-off and posting CRUA) |
| RW-CASEOWN, case owner | Reads the plan position on SCR-14 (Treatment and offer R) |
| RW-COE, center of excellence analyst | Owns package PAYMENT_MATCH and loads a new version through RWB-E1-073 (Rules and parameters CRUD) |

### 11. Data

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

### 12. Contract

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

### 13. Solution plan

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

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P8-002 | No PAYMENT_MATCH version in force | Payment matching for {date} did not run: no matching rule is in force. |
| MSG-P3-027 | No PAYMENT_MATCH version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P1-001 | The ACE batch is late or not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | The role lacks Write-off and posting R | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "PAYMENT_MATCH" and the business date only, never a payment or account fact.

### 15. Screens and states

SCR-28 Proceeds matching (skeleton in E2; states Loading; matched; unmatched) lists receipts from GET /proceeds for the Credit Administration officer, filtered by matched or unmatched. The case owner sees the plan position on SCR-14 Treatment record and the missed payment on SCR-04 Case timeline. SCR-44 shows the JOB-07 run summary.

### 16. Test cases

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

### 17. Guardrails

- No business value in code: window, tolerance, grace days, partial floor and match types are columns of the rows of package PAYMENT_MATCH.
- No personal data in logs, tests, workflow history or prompts. Payments are identified by payment_code and account_key; account numbers are never logged.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the payments, the next installment date and the batch status come through the P1 interfaces over the views; case and treatment facts through P3.
- Amounts use BigDecimal with scale 2 and are compared exactly.
- The rule package is loaded and approved through RWB-E1-073; this story evaluates it and never reads drl_source or the workbook.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-E2-008-02, TC-E2-008-05, TC-E2-008-06 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03, R-UNI-40 | TC-E2-008-01, TC-E2-008-03, TC-E2-008-04, TC-E2-008-07, TC-E2-008-08, TC-E2-008-09, TC-E2-008-10 |

### 19. Out of scope

- Partial payments and late payments inside a window after the due date (RWB-E2-027).
- Settlement, auction and enforcement proceeds (FEAT-PAY-03, FEAT-PAY-04, Epic 4).
- Manual matching of an unmatched receipt (POST /proceeds/{proceedsId}/match, Epic 4).
- The cure period and the broken plan rule (R-RES-28 to R-RES-31, FEAT-TRT-11, Epic 3).
- Authoring, approval and rollback of package PAYMENT_MATCH (RWB-E2-042 and RWB-E1-073).
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
| Depends on | RWB-E2-004, RWB-E1-069, RWB-E1-016, RWB-E1-015 |
| Status | Ready for build |

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the stage 2 data products (treatments, plans, contracts and guarantees) served from the Workbench treatment record and the ACE account and plan views, with each system of record named**, so that **the settlement, TDR and DIL screens in Epic 3 read from one place and nothing is copied out of ACE**.

### 2. Business rationale

From Epic 3 the settlement, restructure and deed in lieu screens need each case's treatments, plan terms, loan contracts and guarantee claims in one checked place. The treatment record lives with the module that owns it (RWB-E2-004), plan terms are in v_ace_plan, contract numbers and dates are on v_ace_account, and guarantee claims come from the guarantee module. DP04 therefore has two kinds of content: the Workbench snapshot of treatments and claims, stamped for the business date, and the ACE facts read from the views at request time. No table copies a contract, a plan or an account. A daily build brings the Workbench rows to the data store with a catalog entry, a freshness stamp, access by role and checks that every row links to a case. Serves REQ-RDF-014: stage 2 data products exist before the first treatment goes live.

### 3. Preconditions

- RWB-E2-004 is done: the treatment entity exists and its module publishes TreatmentQuery (section 12).
- RWB-E1-069 is done: v_ace_account and v_ace_plan are granted SELECT to the recovery service identity (V0002).
- RWB-E1-016 is done: data_product_access and the data product read endpoint exist.
- RWB-E1-015 is done: freshness stamps and the stale check exist.
- RWB-E1-064 is done: data_product holds DP04 Treatment with owner RW-DATASTEW, and sys_fields holds treatment, guarantee_claim, dp_treatment and dp_guarantee_claim.
- data_product_access version "DPA-2026.12" gives DP04 read to RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD, RW-COE and RW-AUDIT.
- The guarantee module publishes GuaranteeClaimQuery; before it is built (Epic 4), the interface returns no claims.

### 4. Flow

1. JOB-02: the stage 2 step runs after the case creation step, once P1 has stamped DP01 for business date D from a COMPLETE ACE batch.
2. Stage2ProductService: calls TreatmentQuery.changedBetween(start of D, end of D) and receives the treatments created or changed on D.
3. Stage2ProductService: calls GuaranteeClaimQuery.changedBetween() for guarantee claims changed on D.
4. Stage2ProductService: resolves each case's primary account_key through CaseScopeQuery, then resolves it in v_ace_account; the contract number and contract date are read from v_ace_account at request time and are not written to any table.
5. Stage2ProductService: holds on the data quality break list any snapshot row whose case does not resolve (check References), and writes the other rows to dp_treatment and dp_guarantee_claim keyed by record ID and business date.
6. Stage2ProductService: compares the count of active treatments in dp_treatment with TreatmentQuery.countActive(); a difference holds the publish (DL25).
7. FreshnessStampService: on a match, writes the DP04 stamp for business date D.
8. Case owner or restructuring officer: reads DP04 for a case through GET /data-products/DP04/records?caseId=; the response joins dp_treatment and dp_guarantee_claim to v_ace_account and v_ace_plan for the contract and plan facts.
9. Data steward: reads the DP04 catalog entry and any breaks.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without a DP04 access row reads the product | 403; refusal logged | MSG-P4-002 | AC3 |
| X2 | A guarantee claim names a case that does not exist | Claim held on the break list with check References; retried with the next build | None | AC4 |
| X3 | TreatmentQuery is unavailable | Step fails; the previous DP04 rows and stamp stay; DP04 turns stale at its expected-by time | MSG-GEN-006, MSG-P1-001 | AC5 |
| X4 | The step runs again for the same business date | Rows replaced by record ID; no duplicate | None | AC6 |
| X5 | Active treatment counts differ | DP04 not stamped for D; break listed for the data steward | MSG-P1-002 | AC7 |
| X6 | A treatment changed at the end of business date D | Included in D; a change one second later goes to D+1 | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the treatment entity (RWB-E2-004), the ACE views (RWB-E1-069), product access (RWB-E1-016) and freshness (RWB-E1-015); the guarantee interface may return no rows |
| Negotiable | Which roles read DP04 and the expected-by time are data rows; the story fixes the build, the link checks and the stamp |
| Valuable | The Epic 3 settlement, TDR and DIL screens read one checked place |
| Estimable | One job step, two snapshot tables, two view reads, one reconciliation |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments and claims through stub interfaces |

### 7. Acceptance criteria

```gherkin
Feature: Stage 2 data products: contracts, plans and treatments

  Background:
    Given business date 2026-12-14 and the ACE batch for ALS for it is COMPLETE at 06:20
    Given the treatment module holds 40 active treatments, 12 of them restructure plans with installments published in v_ace_plan
    Given 9 of the 12 plans carry a credit approval recorded on the case by the restructuring officer

  Scenario: AC1 Products loaded
    Given treatments and plans in the case store, with credit approvals recorded from NLEADS by the officer
    When the stage 2 step of JOB-02 runs
    Then dp_treatment holds 40 rows for business date 2026-12-14, each with treatment type, approval level, installments, outcome and its case
    Then the DP04 read for any of the 40 cases shows the contract number and contract date of its primary account from v_ace_account and the plan terms from v_ace_plan
    Then DP04 carries a freshness stamp for business date 2026-12-14 with status "LOADED"
    Then the catalog entry for DP04 lists system of record "Workbench" for treatment and guarantee claim and names v_ace_account and v_ace_plan for the contract and plan facts

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
    Then the system does not write the claim to dp_guarantee_claim
    Then the data quality break list holds it with product "DP04" and check "References"

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
| BR1 | DP04 holds treatments and guarantee claims from the Workbench, and contract and plan facts read from v_ace_account and v_ace_plan, with one system of record and one owner for each part | REQ-RDF-014; data_product DP04; sys_objects |
| BR2 | No Workbench table copies a contract, a plan or an account; the views are read at request time | D-RCV-35 U1; tier map section 9 |
| BR3 | Every snapshot row links to an existing case, or it is held on the break list and retried with the next build | DQ load check "References" |
| BR4 | The product is stamped for the day only when the active count matches the owning module, with zero tolerance | DL25; RWB-E1-011 hold rule (FEAT-RDF-13) |
| BR5 | A role reads DP04 only through an access row in force | data_product_access; REQ-RDF-010 |
| BR6 | Credit approval for a restructure is recorded on the case by the officer; there is no interface to NLEADS | INT-26; DL12 |
| BR7 | Plan installments come from the ACE plan published calculation | DF-ACE-174 source ACE; INT-34 |

### 9. State transitions

None. This story does not change a case status. It changes the DP04 freshness status (LOADED or STALE) and the state of the stage 2 step on the JOB-02 run (Complete or Failed).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery service identity, stage 2 step | Reads the ACE views, writes dp_treatment and dp_guarantee_claim, writes breaks and the stamp |
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
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-006 | v_ace_account | contract_no | Read |
| DF-ACE-007 | v_ace_account | contract_date | Read |
| DF-ACE-160 | v_ace_plan | plan_ref | Read |
| DF-ACE-174 | v_ace_plan | installments | Read |
| DF-ACE-175 | v_ace_plan | recommended_installment | Read |
| DF-ACE-168 | v_ace_plan | booked_at | Read |
| DF-TRT-034 to DF-TRT-051 | dp_treatment | all fields | Write |
| DF-TRT-052 to DF-TRT-061 | dp_guarantee_claim | all fields | Write |
| DF-OPS-001 to DF-OPS-009 | data_product_load | all fields | Write |

treatment and guarantee_claim fields are read through TreatmentQuery and GuaranteeClaimQuery, not from their tables. v_ace_account and v_ace_plan are read through the P1 reader. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Job step**

| Item | Value |
|---|---|
| Trigger | JOB-02 after the case creation step, once DP01 is stamped for business date D from a COMPLETE ACE batch |
| Job name | JOB-02 Case creation, stage 2 product step |
| Schedule | Daily, after the ACE batch for ALS, before 07:00 (NFR-013) |
| Input | Treatments and guarantee claims changed on D through the published interfaces; contract and plan facts read from v_ace_account and v_ace_plan at request time |
| Output | dp_treatment and dp_guarantee_claim rows for D; breaks with check References; DP04 freshness stamp; count check result on the job run |
| Events published | None |
| Idempotency key | Record ID and business date; a rerun replaces the rows for D |
| Restart behavior | The step writes in one transaction per snapshot table; a failure leaves the previous day's rows; rerun from the job monitor with POST /admin/jobs/{jobId}/rerun |

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

// P1 recovery.data.api, over recovery.v_ace_account and recovery.v_ace_plan
Optional<AccountContract> AceAccountQuery.contractOf(String accountKey);
List<PlanView> AcePlanQuery.forAccount(String accountKey);
```

**Endpoints used**

| Method and path | Use | Authorization | Errors |
|---|---|---|---|
| GET /api/recovery/v1/data-products/{productCode}/records | Read DP04 for a case (RWB-E1-016) | Case record, R, plus a DP04 access row | 403 (MSG-P4-002); 404 (MSG-P4-003); 503 (MSG-GEN-006) |
| GET /api/recovery/v1/admin/data-quality/exceptions | Read DP04 References breaks | Platform administration, R | 401; 403; 503 |
| POST /api/recovery/v1/admin/jobs/{jobId}/rerun | Rerun the failed step | Platform administration, U | 404; 409 (MSG-P2-006) |

### 13. Solution plan

- Package: folder `recovery/dataengine/stage2`, Java package `recovery.dataengine.stage2`.

| Component | Type | Responsibility |
|---|---|---|
| Stage2ProductStep | Job | The stage 2 step of JOB-02 |
| Stage2ProductService | Service | Reads changes through the interfaces, resolves case links, writes rows, runs the count check |
| DpTreatmentRepository, DpGuaranteeClaimRepository | Repository | Upsert by record ID and business date |
| DpTreatment, DpGuaranteeClaim | Entity | One row per record and business date |
| Dp04ReadService | Service | Joins the snapshot to v_ace_account and v_ace_plan for the contract and plan facts |
| DP04 access rows | Rule table | data_product_access rows for DP04, version DPA-2026.12 |

- Database: dp_treatment and dp_guarantee_claim hold the Workbench snapshot per business date; this story drops dp_treatment.contract_no and dp_treatment.contract_date, because a contract is read from v_ace_account and is never copied (rule 1 of the tier map). No table holds a plan, a contract or an account row. Writes data_product_load for DP04 (RWB-E1-015) and the case-link breaks. Reads v_ace_account and v_ace_plan through P1.
- Configuration and reference data: DP04 row in data_product with expected-by 08:00 (assumed; DL11); DP04 access version DPA-2026.12 prepared by the data steward and loaded by the reference data administrator; dictionary rows for dp_treatment and dp_guarantee_claim under DP04.
- Build steps:
  1. Flyway migration for the two snapshot tables and the two dropped columns, with their sys_objects and sys_fields rows under DP04.
  2. Stage2ProductService reading changes for D through TreatmentQuery and GuaranteeClaimQuery; the business date window is [start of D, start of D+1).
  3. Case link resolution through CaseScopeQuery; the account and plan facts through the P1 reader.
  4. References break path, and upsert of the other rows.
  5. Count check against countActive(); hold the stamp on a difference.
  6. Stamp DP04 through FreshnessStampService on a match.
  7. Stage2ProductStep wired into JOB-02 after the case creation step.
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
| MSG-P2-006 | Rerun while JOB-02 is running | {job} is already running. Wait for it to finish before you rerun it. |

Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-45 Data quality (Epic 2): state Loading while the list arrives; state Breaks shows DP04 References breaks and count breaks for the data steward. The case record view SCR-03 shows DP04 data for roles with access. The settlement, TDR and DIL screens that use DP04 come in Epic 3.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-010-01 | AC1, BR1, BR2, BR6, BR7 | System | 40 synthetic treatments, 12 plans, 9 approvals |
| TC-E2-010-02 | AC2, BR1 | System | 5 TCG claims for existing cases |
| TC-E2-010-03 | AC3, BR5 | System | RW-PHONECOL reads DP04 |
| TC-E2-010-04 | AC4, BR3 | System | TCG claim for an unknown case ID |
| TC-E2-010-05 | AC5 | System | TreatmentQuery stub returning errors |
| TC-E2-010-06 | AC6 | System | Step run twice for 2026-12-14 |
| TC-E2-010-07 | AC7, BR4 | System | countActive() 41 against 40 rows |
| TC-E2-010-08 | AC8 | System | Changes at 23:59:59 and 00:00:00 |
| TC-E2-010-09 | Access | Access | RW-TRIBE calls GET /admin/data-quality/exceptions; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: access, expected-by time and tolerance are data rows or decisions (DL25).
- No personal data in logs, tests or prompts: treatment and claim rows carry amounts and codes; test data is synthetic.
- No copy of ACE data: contracts and plans are read from v_ace_account and v_ace_plan at request time; treatments and claims come through TreatmentQuery and GuaranteeClaimQuery; case links through CaseScopeQuery.
- No call to NLEADS or the Thai Credit Guarantee Corporation; their results arrive as recorded on the case.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Business Requirements Epic 2, sections 3.1 and 4 | FEAT-CHO-09 | 07 Route, settle and claim | DL25; DL12 | TC-E2-010-01 to TC-E2-010-08 |

### 19. Out of scope

- The treatment entity and its plan timers (RWB-E2-004).
- The credit approval pack for NLEADS (RWB-E2-006) and booking confirmation from the ALS batch (RWB-E2-007).
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
- The ACE batch for the business date is COMPLETE, or the case list shows its date as stale.

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
| X5 | Today's ACE batch has not arrived | The list shows with the stale banner and the date of the data | MSG-P1-001 | AC8 |
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
    Given the ACE batch of 2026-12-15 has not arrived and the case data is from 2026-12-14
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-021, RWB-E1-072, RWB-E2-011 |
| Status | Ready for build |

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a screen to transfer a case to another queue or reassign it to a person, with a reason code required and the TRANSFER rule package checked**, so that **a hand-off is one action with a record, not an email**.

### 2. Business rationale

Today ownership changes are agreed by email, and audit found debtors who met the criteria were not transferred to the responsible unit (CTL-03). A manual move must carry a coded reason, respect the caseload cap and the transfer rules, keep the case's state and clocks, and leave a decision log entry. This story gives the team manager one screen for a single or a bulk move.

The transfer rules are rows of the TRANSFER rule package (RWB-E1-021). The manual move is evaluated by RuleEvaluator, so the screen shows the rule ID that refused the move and the decision log names the rule and the package version that decided (D-RCV-36 T3, T5). The manual transfer API does not change: the endpoint, the request, the response and the errors are the same as RWB-E1-021.

It meets REQ-WKM-003, REQ-WKM-007 and REQ-WKM-008. The measure is that every manual move has an assignment record with a reason code, a decision log entry with a rule ID and a package version, and a rule ID on the screen when the move is refused.

### 3. Preconditions

- RWB-E1-021 is done: the TRANSFER rule package is in force, and a manual transfer is evaluated by `RuleEvaluator.evaluate("TRANSFER", facts, businessDate)`, which returns the allowing rule or refuses with the rule ID that blocks the move.
- RWB-E1-072 is done: the published RuleEvaluator and RuleCatalog exist, and the rule package store holds the TRANSFER versions.
- RWB-E2-011 is done: team queues and the case list open SCR-05 for a case or a selection.
- RWB-E1-020 is done: `AssignmentEngine` picks an owner in a queue by its method and caseload cap.
- The decision log writer (RWB-E1-027) is available through the P7 interface and accepts a rule ID with its rule version.
- LOV-TRANSFER-REASON (new, see Additions) is loaded with the agreed reason codes. Assumed values: R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral, R06 Wrong queue (DL23).
- The person holds RW-TEAMMGR or RW-CAPACITY (Queue and allocation U) and the case is in their scope.

### 4. Flow

1. Team manager: opens SCR-05 Transfer case from SCR-03 Case record or from a selection on SCR-07 Team queues.
2. Team manager: chooses a target queue or a target owner, a reason code and an optional note, and confirms.
3. Front end: calls `POST /api/recovery/v1/cases/{caseId}/transfer` with a new Idempotency-Key per case.
4. Transfer service: checks the reason code, that the case is open and not under a legal hold, and the scope.
5. SY-RULES: builds TransferFacts from the case, the target queue or owner, the reason code and the business date, and calls `RuleEvaluator.evaluate("TRANSFER", facts, businessDate)`. The RuleResult names the rule ID that allows or refuses the move and the package version that decided.
6. Transfer service: on a refusal, stops and shows MSG-P3-033 with the rule ID from the result; otherwise, for a queue transfer, asks `AssignmentEngine` for the owner by the target queue's method, and for a reassignment checks the target owner is below the cap and, for reason R04, in the case's team.
7. Transfer service: writes the decision log entry through the P7 interface with the rule ID and the package version; on success, in one transaction ends the current assignment, writes the new assignment with reason, rule ID, queue and reason code, updates the case queue, owner and team, and writes CaseTransferred (EV-04) to the outbox.
8. Front end: shows state Saved with MSG-GEN-005; for a bulk move, one result per case and the summary.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No reason code | Refused; nothing changes | MSG-P3-001 | AC4 |
| X2 | A TRANSFER package rule refuses the move | Refused; the refusing rule ID from RuleEvaluator is shown | MSG-P3-033 | AC2 |
| X3 | The target owner is at the caseload cap | At cap warning; refused | MSG-P3-002 | AC5 |
| X4 | Every owner of the target queue is at the caseload cap | At cap warning naming every owner; refused | MSG-P3-002 | AC12 |
| X5 | Reason R04 and the target owner is outside the case's team | Refused naming R-UNI-18 | MSG-P3-033 | AC6 |
| X6 | The case is closed or under a legal hold | Refused | MSG-P3-005 | AC7 |
| X7 | Two transfers of one case at the same time | One succeeds; the other is refused | MSG-GEN-004 | AC8 |
| X8 | The same request is sent twice with the same Idempotency-Key | The first result is returned; no second record | None | AC9 |
| X9 | The decision log write fails | Nothing changes | MSG-P7-003 | AC10 |
| X10 | Some cases in a bulk move are refused | The others move; each refused case shows its message | MSG-P3-035 | AC11 |
| X11 | No TRANSFER package version is in force on the business date | Refused; nothing changes and no decision log entry is written | MSG-P3-027 | AC13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the TRANSFER package and the assignment engine of Epic 1; adds the screen and the coded reason |
| Negotiable | Reason codes, the bulk limit and the rule rows are data; the checks are fixed |
| Valuable | Ends ownership changes by email; every move has a record and a meaningful refusal |
| Estimable | One endpoint extended, one service, one screen |
| Small | Fits in one sprint with its tests |
| Testable | API tests on a seeded database and a browser test of SCR-05 |

### 7. Acceptance criteria

```gherkin
Feature: Manual transfer and reassignment screen with reason

  Background:
    Given the business date is 2026-12-15
    Given TRANSFER package version "TRF-2026.12" is in force, and row "TRF-010" refuses a move while a deviation is open
    Given user "U-TM-01" holds RW-TEAMMGR for team "MTG-BKK"
    Given case "RW-2026-000401" in queue "MTG-BKK-CO" owned by "U-CO-01", status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    Given queue "LIT-BKK-01" uses "ROUND_ROBIN" with a caseload cap of 150 and owners "U-LO-01" with 80 cases and "U-LO-02" with 95 cases, next in turn "U-LO-02"

  Scenario: AC1 Transfer
    Given case "RW-2026-000401" in a queue of team "MTG-BKK"
    When "U-TM-01" transfers it to queue "LIT-BKK-01" with reason "R02" Customer deceased
    Then the case is in queue "LIT-BKK-01" with owner "U-LO-02"
    Then the previous assignment of "U-CO-01" has ended at the time of the transfer
    Then a new assignment has reason "TRANSFER", reason code "R02", queue "LIT-BKK-01" and the rule ID from TRANSFER version "TRF-2026.12"
    Then one decision log entry holds the rule ID, the rule version "TRF-2026.12", the from and to queue and owner and the reason code
    Then the case keeps status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    Then one CaseTransferred event is in the outbox

  Scenario: AC2 Rule blocks
    Given case "RW-2026-000402" with deviation "X1" open and owned by the complaint officer under rule "R-DEV-02"
    When "U-TM-01" tries to transfer it to queue "LIT-BKK-01" with reason "R05"
    Then RuleEvaluator.evaluate("TRANSFER", facts, 2026-12-15) returns ruleId "TRF-010" and no allowing output
    Then the screen refuses with MSG-P3-033 naming rule "TRF-010"
    Then the case, its assignment and the decision log are unchanged

  Scenario: AC3 Bulk
    Given ten selected cases in queue "MTG-BKK-CO" owned by "U-CO-01"
    When "U-TM-01" reassigns them to owner "U-CO-03" with 60 open cases and reason "R04"
    Then all ten have owner "U-CO-03"
    Then ten assignments and ten decision log entries are written, each with its rule ID and rule version
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

  Scenario: AC13 No TRANSFER package in force
    Given no TRANSFER package version is in force on 2026-12-20
    When "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02" on 2026-12-20
    Then RuleEvaluator.evaluate("TRANSFER", facts, 2026-12-20) throws NoPackageInForce
    Then the system refuses the transfer with MSG-P3-027 for the package in force check
    Then the case, its assignment and the decision log are unchanged
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A manual move needs a reason code from LOV-TRANSFER-REASON | REQ-WKM-003; REQ-CWC-010 |
| BR2 | A move the TRANSFER package refuses is not made, and the refusing rule ID returned by RuleEvaluator is shown | REQ-CWC-010; RWB-E1-021; D-RCV-36 T5 |
| BR3 | A queue transfer takes its owner from the target queue's assignment method | Queue field assignment_method; RWB-E1-020 |
| BR4 | An owner at or above the queue's cap cannot receive a case | Queue field capacity_cap; DL23 |
| BR5 | A reassignment for an absent owner stays inside the case's team | R-UNI-18 |
| BR6 | A move keeps the case status, route state, stage clock and timers | R-UNI-18; R-UNI-46 |
| BR7 | A case under a legal hold or closed is not moved | R-UNI-20 |
| BR8 | A move that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR9 | A repeated request with the same Idempotency-Key has no further effect | R-UNI-40 |
| BR10 | A case with an open deviation stays with the owner the deviation rule named | R-DEV-02; R-DEV-03 |
| BR11 | The TRANSFER version in force on the business date decides the move, and the decision log records the rule ID and that package version; a case keeps the version it was moved under | D-RCV-36 T5, T7; R-UNI-38 |
| BR12 | No TRANSFER version in force is a refusal (NoPackageInForce), never a default decision | D-RCV-36 T3; R-UNI-41 |

### 9. State transitions

None. This story does not change a case status. It changes the case's queue, owner and team, ends one assignment and writes the next. The route state and the clocks stay as they were (R-UNI-18, R-UNI-46).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Transfers and reassigns cases in the team's scope (Queue and allocation CRUA) |
| RW-CAPACITY, capacity and workforce planner | Reassigns cases for capacity (Queue and allocation RU, scope All) |
| SY-CASEWF, case workflow module | Writes the assignment and updates the case (Queue and allocation CRU) |
| SY-RULES, Drools evaluator | Evaluates the TRANSFER package and returns the rule ID and the package version |
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
| DF-REF-002 | rule_row | rule_id | Read, through RuleEvaluator |
| DF-REF-281 | rule_package_version | version_label | Read, through RuleEvaluator |
| DF-REF-282 | rule_package_version | status | Read, through RuleEvaluator |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through the P7 interface |

The rule row is read only through RuleEvaluator; this story reads no workbook, no drl_source and no rule_row row directly. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /api/recovery/v1/cases/{caseId}/transfer** (P3; the endpoint and payload of RWB-E1-021, unchanged)

| Item | Value |
|---|---|
| Request | Header `Idempotency-Key` (uuid, required). Body `TransferRequest`: `toQueueId` or `toOwnerId` (one required), `reasonCode` (TRANSFER for a queue move, MANUAL for a reassignment), `transferReasonCode` (new, LOV-TRANSFER-REASON, required), `note` (max 500) |
| Response | 200 `Assignment`: `id`, `caseId`, `assigneeUserId`, `assignedAt`, `reason`, `ruleId` |
| Errors | 401 (MSG-P4-001); 403 no Queue and allocation U (MSG-P4-002); 404 case unknown or out of scope (MSG-P4-003); 409 case closed or held (MSG-P3-005), rule refuses (MSG-P3-033), record changed (MSG-GEN-004); 422 no reason (MSG-P3-001), owner at cap (MSG-P3-002), no package in force (MSG-P3-027); 503 decision log write failed (MSG-P7-003) |
| Authorization | Queue and allocation, right U, scope applied |
| Idempotency | `Idempotency-Key` header, kept 24 hours. A repeat returns the stored response |

**GET /api/recovery/v1/cases/{caseId}** (P3) reads the case after the move (Case record R).

**Published interfaces used**

```java
// P3, RWB-E1-020
Optional<UUID> AssignmentEngine.pickOwner(UUID queueId, UUID caseId, LocalDate businessDate);
// P3, published in RWB-E1-072 (recovery.casewf.rules)
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
// P7, RWB-E1-027
UUID DecisionLogWriter.record(DecisionLogEntryCommand command);
```

`RuleResult` carries packageCode, packageVersion, ruleId and outputs (RWB-E1-072). The rule ID shown with MSG-P3-033 is `RuleResult.ruleId`; the rule version written to the decision log is `RuleResult.packageVersion`. No caller receives a KieBase, a KieSession or a Drools type.

**Events.** CaseTransferred (EV-04) published with caseId, fromOwner, toOwner, reasonCode, ruleId, in the same transaction as the change.

### 13. Solution plan

**Package.** `recovery.casewf.transfer` in the recovery module; front end folder `src/modules/recovery/casewf/transfer`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAndWorkflowController | Controller | `POST /api/recovery/v1/cases/{caseId}/transfer`; idempotency; problem responses |
| ManualTransferService | Service | Checks, RuleEvaluator call, owner pick, decision log write, then the transaction |
| TransferFactsBuilder | Service | Builds the TransferFacts of the case, the target queue or owner, the reason code and the business date |
| IdempotencyStore | Repository | Stores the key, the request hash and the response for 24 hours |
| AssignmentRepository | Repository | Ends the current assignment and writes the new one |
| OwnerLoadRepository | Repository | Counts open cases per owner in a queue for the cap check |
| TransferCasePage | React component | SCR-05 with the Form, At cap warning and Saved states, single and bulk |
| BulkTransferRunner | React component | Sends one request per selected case in sequence and collects the results |

**Database.** Migration `V<next>__rwb_e2_012_assignment_reason.sql` adds `assignment.queue_id uuid REFERENCES queue (id)` and `assignment.transfer_reason_code varchar(10)`, index `ix_assignment_case_open` on `(case_id) WHERE ended_at IS NULL`, and the idempotency table `idempotency_key (key uuid PK, endpoint varchar(100), request_hash char(64), response jsonb, created_at timestamptz)`. The case update uses the optimistic lock column `recovery_case.version`. No table holds a transfer rule; the rules are rows of the TRANSFER package (RWB-E1-072, RWB-E1-073).

**Configuration and reference data.** LOV-TRANSFER-REASON values (center of excellence; DL23). `transfer.bulk.max` = 50 (assumed; DL23). The TRANSFER package rows are authored and loaded by RW-COE through RWB-E1-073; this story loads none. Queue caps (DL23).

**Build steps**

1. Write the migration and extend the assignment entity.
2. Build `IdempotencyStore` and the header handling in the controller.
3. Build `TransferFactsBuilder` and `ManualTransferService` checks in this order: reason, case state and hold, scope, `RuleEvaluator.evaluate("TRANSFER", facts, businessDate)`, owner pick or cap check, team check for R04.
4. Map `NoPackageInForce` to 422 with MSG-P3-027 and a refusal result to 409 with MSG-P3-033 carrying the rule ID.
5. Add the decision log write with the rule ID and the package version before the transaction; map its failure to 503 with MSG-P7-003.
6. Write the transaction: end assignment, new assignment, case update with the version check, outbox row.
7. Build `TransferCasePage` with its three states and `BulkTransferRunner` with the per-row result and the MSG-P3-035 summary.
8. Write the tests in section 16, including two parallel requests and the refusal of AC2.

**Feature flag.** `rwb.p3.manual-transfer`. Off: SCR-05 is hidden and the endpoint returns 403 for every role except SY-CASEWF. The rule evaluation is also behind `rwb.p3.drools` (RWB-E1-072); with that flag off the transfer endpoint refuses every move with MSG-P3-027.

**Done when.** The tests in section 16 pass, and a transfer made in SIT shows on the case timeline queue history (RWB-E2-016) with the rule ID and the package version on its decision log entry.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | No reason code | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner, or every owner of the target queue, at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Case closed or under a legal hold | This case cannot move to {state} from {current}. |
| MSG-P3-027 | No TRANSFER package version in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-033 | A TRANSFER rule refuses the move | Rule {rule} does not allow this transfer. |
| MSG-P3-035 | Bulk move with refusals | {done} of {total} cases were moved. The others show the reason on their row. |
| MSG-GEN-004 | Two moves of one case at once | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-005 | Move saved | Saved. |
| MSG-P4-002 | A role without Queue and allocation U | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story {check} is "package in force" and {detail} names the package code TRANSFER and the business date only. MSG-P3-033 and MSG-P3-035 are new (see Additions); the {rule} value is the rule ID from RuleEvaluator. Thai text follows DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-05 Transfer case | Form | Chooses a queue or an owner, a reason code and a note; confirms |
| SCR-05 Transfer case | At cap warning | Reads MSG-P3-002; chooses another owner or the team queue |
| SCR-05 Transfer case | Refused | Reads MSG-P3-033 with the rule ID, or MSG-P3-027 when no TRANSFER version is in force |
| SCR-05 Transfer case | Saved | Reads MSG-GEN-005, or the per-case results and MSG-P3-035 for a bulk move |
| SCR-07 Team queues | List | Selects up to 50 cases and opens SCR-05 for them |
| SCR-09 Exception queue | List | Not used by this story; a refused move is not queued |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-012-01 | AC1, BR1, BR3, BR6, BR11 | System | RW-2026-000401 to LIT-BKK-01, reason R02, TRANSFER version TRF-2026.12 |
| TC-E2-012-02 | AC2, BR2, BR10 | System | RW-2026-000402 with X1 open under R-DEV-02; row TRF-010 refuses |
| TC-E2-012-03 | AC3, BR4, BR5, BR11 | System | Ten cases to U-CO-03 with 60 open cases, reason R04 |
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
| TC-E2-012-15 | AC13, BR12 | System | No TRANSFER version in force on 2026-12-20; NoPackageInForce and MSG-P3-027 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: reason codes, caps, the bulk limit and the transfer rows are data.
- No personal data in logs, tests, workflow history or prompts: the note field is not logged, and events carry IDs and codes only.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the decision log is written through the P7 interface, and deviation ownership comes from the TRANSFER package and the case flag.
- The decision log entry is written before the case changes; a failed write leaves the case as it was.
- Each case in a bulk move is its own request, its own rule evaluation and its own transaction.
- No second rule engine: the transfer rules are read only through RuleEvaluator, and no caller reads the workbook, drl_source or rule_row.
- The endpoint, the request and the response are those of RWB-E1-021; this story adds no field to the API.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-003 | Manual transfer or reassignment only with a reason code from the agreed list | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-DEV-02, R-UNI-20, R-UNI-39, R-UNI-40 | TC-E2-012-01, TC-E2-012-02, TC-E2-012-04, TC-E2-012-07 to TC-E2-012-10, TC-E2-012-13, TC-E2-012-14, TC-E2-012-15 |
| REQ-WKM-007 | An absent or over-cap owner's cases reallocated inside the team, keeping state and clocks | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-04, FEAT-WKM-10 | All recovery processes | R-UNI-18, R-UNI-46 | TC-E2-012-03, TC-E2-012-05, TC-E2-012-06, TC-E2-012-11, TC-E2-012-12 |
| REQ-WKM-008 | Queue and transfer history visible on the case | Business Requirements Epic 2, section 4; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-UNI-18 | TC-E2-012-01, TC-E2-012-03 |

The rule ID and the package version on the decision log entry satisfy REQ-CWC-016 through RWB-E1-072; this story adds no requirement ID of its own.

### 19. Out of scope

- Automatic reallocation when an owner is absent or over the cap (R-UNI-18 and R-UNI-19, JOB-06 Daily rebalancing, RWB-E1-030).
- The queue history view on the case (RWB-E2-016).
- Rule-driven transfers on stage change, route decision and timer expiry (RWB-E1-021).
- The TRANSFER package rows themselves, their scenarios and their approval (RWB-E1-073).
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
    Given the total balance comes from the ACE account data of business date 13 December 2026

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
| DF-ACE-020 | v_ace_account | total_balance | Read through the P1 data product interface, with its business date |
| DF-ACE-078 | v_ace_contact | contact_value | Read masked through the owning module's DTO |
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
    Then when "X1" is cleared on 2026-12-14, the screen stays in state "On hold" with only "X3" open and "X1" shown as cleared on 2026-12-14

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

None. This story does not change a case status. It shows the timer statuses (Running, Paused, Expired) and the On hold status that other stories set. It adds two fields that the escalation step of JOB-05 Timer check behind TimerScheduler (RWB-E1-028) writes when a timer escalates.

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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
    Then the system regenerates "DOC-0411" as doc_version 2 showing "12 December 2569 BE"
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
| DF-ACE-056 | v_ace_customer | person_key | Read |
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
| DF-DOC-100 | signature_request | person_key | Write |
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
| DF-ACE-301 | v_ace_iam_group | entra_group | Read |
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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

- RWB-E1-052 and RWB-E1-055 are done: generation, the WIN file and the acknowledgment run, and ACE ingests the INT-15 proof file.
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
6. The proof read: DeliveryResultReader reads the day's proof rows from v_ace_pod by barcode (INT-15 is ingested by ACE); a Delivered record sets Delivered and publishes NoticeDelivered; P3 starts the notice period from the delivery date (R-LIT-07).
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
| The recovery service identity | Runs JOB-10 and reads the proof rows from v_ace_pod |
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
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-EXT-015 | contact_point_ext | consent_given | Read through the P1 interface |
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

**Jobs.** JOB-10 WIN outbound notices (daily 16:00) gets two steps: the proof window step first, then the conduct check before each file record. The INT-15 results are not a Workbench load: ACE ingests them, and DeliveryResultReader takes the Refused and Undeliverable results from v_ace_pod. Idempotency for each: notice ID and business date; a rerun from SCR-44 skips notices already Unserved, Held or in a file of that date.

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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
- Contact points and consent are held in ACE, which receives them from SCBPDM (INT-04).
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
    When "CO-0201" sends POST /cases/RC-2026-000777/messages with channel "SMS", template "SMS-REMIND", language "TH" and party "P-0077", and NSS accepts it with reference "NSS-7781" returning result "DELIVERED"
    Then the response is status 202 with an interaction of channel "SMS", direction "OUTBOUND" and conduct check "PASSED"
    Then the interaction has delivery status "DELIVERED" and reference "NSS-7781"
    Then NSS received one message

  Scenario: AC2 LINE
    Given party "P-0077" has a verified "LINE" contact point with consent "GIVEN"
    When "CO-0201" sends a message with channel "LINE" and template "LINE-REMIND", and LINE OA reports it delivered and then read
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
| DF-ACE-077 | v_ace_contact | person_key | Read |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-078 | v_ace_contact | contact_value | Read |
| DF-EXT-015 | contact_point_ext | consent_given | Read through the P1 interface |
| DF-EXT-017 | contact_point_ext | verified_at | Read through the P1 interface |
| DF-EXT-018 | contact_point_ext | failed_count | Write, through the P1 interface |
| DF-REF-046 | template | template_code | Read |
| DF-REF-047 | template | template_version | Read |
| DF-REF-066 | template | channel | Read |
| DF-INT-002 | interaction | case_id | Write, through the ledger writer |
| DF-INT-003 | interaction | person_key | Write, through the ledger writer |
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
    Given its text names two parties, amount "2,400,000.00 baht" and date "1 December 2569 BE"
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
    Given a judgment whose text reads "Judgment at 5 March 2570 BE"
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
    Then the PDF shows "1,250,000.00 baht (one million two hundred fifty thousand baht)" and "10 December 2569 BE"
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
| DF-CAS-004 | recovery_case | primary_person_key | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-003 | treatment | decision_log_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-ACE-057 | v_ace_customer | first_name | Read |
| DF-ACE-058 | v_ace_customer | last_name | Read |
| DF-ACE-197 | v_ace_collateral_detail | title_doc_no | Read |
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E2-008, RWB-E2-042 |
| Status | Ready for build |

### 1. Story

As a **Credit Administration officer (RW-CREDITAD)**, I want **the matching rules for amount, date window and partial payments held as versioned rows of the PAYMENT_MATCH rule package and run by the matching engine, with the exception list for what does not match**, so that **most payments match without a person and the rest are listed**.

### 2. Business rationale

The exact rule of RWB-E2-008 leaves short and late installments on the exception list, and a person matches them by hand each morning. This story adds the PARTIAL and WINDOW rules as rows of the PAYMENT_MATCH rule package, applies them in row order, records each match in the decision log with the rule ID and the package version, and lets Credit Administration change a window or tolerance through a new approved package version with no code release.

The match type, the amount tolerance, the window, the grace and the partial floor are columns of the decision table, not code and not a reference table (D-RCV-36 T10). RWB-E2-042 authors the rows; RWB-E1-073 loads, checks, approves and rolls them back; this story runs them through RuleEvaluator and reports the exception list. It serves REQ-CHO-009, control CTL-41 and the FSD P8 measure "receipts matched the same day". The measure is that every match names its rule and package version, and unmatched receipts carry a reason.

### 3. Preconditions

- RWB-E2-008 is done: JOB-07, the proceeds table and the exception list are live, and a PAYMENT_MATCH version with the EXACT row in force decides the exact matches.
- RWB-E2-042 is done: the PAYMENT_MATCH package holds the EXACT, WINDOW and PARTIAL rows in the Drools template with at least 50 scenarios.
- RWB-E1-027 is done: the decision log writer accepts D5 entries with a rule ID and a rule version.
- TreatmentApi records an installment shortfall (RWB-E2-004).
- PAYMENT_MATCH version "PM-2026.12" is in force from 2026-12-01 with the EXACT, WINDOW and PARTIAL rows. It was loaded through POST /admin/rule-packages/PAYMENT_MATCH/versions by RW-COE and approved by RW-RISK (RWB-E1-073).
- The reader holds RW-CREDITAD or another role with Write-off and posting R.

### 4. Flow

1. RW-COE: authors the PARTIAL and WINDOW rows in the PAYMENT_MATCH workbook and loads a new version through POST /admin/rule-packages/PAYMENT_MATCH/versions with the valid from date.
2. System: RulePackageVersionService runs the Drools compile check, the schema check on the condition columns, the overlap and unreachable row checks, the scenario check and the dry run; any failure refuses the whole load (RWB-E1-073).
3. RW-RISK: approves the version; the author cannot approve it.
4. JOB-07: for the business date, calls `RuleEvaluator.evaluate("PAYMENT_MATCH", facts, businessDate)`, which picks the version in force on that date.
5. System: the package fires one row, the first match in row order (EXACT, then WINDOW, then PARTIAL), against each running plan on the case; the RuleResult names the rule ID of the row and the package version that decided.
6. System: writes the D5 decision log entry with the rule ID, the package version and the inputs; then writes the proceeds row and calls TreatmentApi.
7. System: for a PARTIAL match, passes the shortfall to TreatmentApi, which holds it on the plan.
8. System: a payment no row matches is written UNMATCHED with a D5 entry under R-UNI-03 and appears on the exception list.
9. Credit Administration officer: reads matched and unmatched receipts on SCR-28, with the rule and the package version that matched each one.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A partial payment below the partial floor | Unmatched; exception list | MSG-P8-001 | AC5 |
| X2 | A late payment one day past the window | Unmatched; exception list | MSG-P8-001 | AC4 |
| X3 | A package version load with two rows of the same row order or a tolerance above 100 | Load refused in full | MSG-P3-027 | AC6 |
| X4 | The decision log write fails for a match | The payment is not written; it is matched in the next run; incident | MSG-P7-003 | AC7 |
| X5 | A payment above the installment by more than the tolerance | Unmatched; exception list | MSG-P8-001 | AC8 |
| X6 | Two rows would match | The row with the lower row order decides | None | AC9 |
| X7 | No PAYMENT_MATCH version is in force on the business date | The run stops; no payment is matched and no proceeds row is written | MSG-P3-027 | AC10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the PAYMENT_MATCH package and the matcher of RWB-E2-008 only |
| Negotiable | Every threshold is a rule row column; the story fixes the row order and the logging |
| Valuable | Short and late installments match without a person |
| Estimable | Two new match rows, one evaluator call and the decision log write |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against a synthetic ALS load and a loaded package version |

### 7. Acceptance criteria

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

### 8. Business rules

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

### 9. State transitions

None. This story does not change a case status. P3 changes the plan route state on the results:

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | PLAN_RUNNING (R-RES-26) |
| PLAN_CURE_PERIOD | PAYMENT_RECEIVED_LATE | payment received inside the cure period | PLAN_RUNNING (R-RES-28) |

The package version moves LOADED to APPROVED to IN_FORCE, or to REFUSED, through RWB-E1-073.

### 10. Authority

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

### 11. Data

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

### 12. Contract

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

### 13. Solution plan

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

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P3-027 | A package version check fails, or no version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-001 | An empty file is loaded | Enter {field}. |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 the {check} value is compile, schema, scenario or package in force, and {detail} names the row ID, the column or the package code only, never a payment or a person. Thai text follows DL10.

### 15. Screens and states

SCR-28 Proceeds matching (states Loading; matched; unmatched) shows, for each matched receipt, the rule ID and the package version from its decision log entry, and for each unmatched receipt the reason. PAYMENT_MATCH versions show on SCR-39 Rules and parameters (Epic 8); until then the version list is read through GET /admin/rule-packages/PAYMENT_MATCH/versions. Reference data on SCR-40 holds no payment matching table.

### 16. Test cases

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

### 17. Guardrails

- No business value in code: match type, row order, tolerance, window, grace and partial floor are columns of the PAYMENT_MATCH rule rows.
- No personal data in logs, tests, workflow history or prompts: decision log inputs hold payment code, amount, dates and rule ID only.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: payments, accounts and plans come through P1 and P3 interfaces.
- The decision log entry is written before the proceeds row; no match exists without its entry.
- One evaluator: the matching engine calls RuleEvaluator and reads no workbook, drl_source or rule_row directly.
- The package version in force is chosen at evaluation time from the business date, and no match is made without a version in force.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-RES-28, R-UNI-03, R-UNI-38, R-UNI-39, R-UNI-41 | TC-E2-027-01 to TC-E2-027-13 |

### 19. Out of scope

- Settlement payment matching and partial settlement installments (FEAT-PAY-03, Epic 4).
- Manual matching from SCR-28 (POST /proceeds/{proceedsId}/match, Epic 4).
- The reconciliation agent that works the exception list (Epic 4).
- Applying proceeds to the case balance in policy order (FEAT-PAY-10, Epic 4).
- Authoring the PAYMENT_MATCH rows, their scenarios and their approval (RWB-E2-042, RWB-E1-073).
- The retired payment_match_rule table and its reference loads (D-RCV-36 T10).
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
| DF-ACC-009 | v_ace_account | principal_outstanding | Read (Section B, RWB-ACE-001) |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-025 | v_ace_account | interest_rate | Read |
| DF-ACE-045 | v_ace_payment | payment_date | Read |
| DF-ACE-046 | v_ace_payment | payment_amount | Read |
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
    When the manager filters by queue "MTG-BKK-CO", product MORTGAGE and breached Yes and then chooses Extract with the same filters
    Then 1 row shows, "RW-2026-000101"
    Then an Excel file downloads with a header row and 1 data row for "RW-2026-000101" with columns age in state, service level state, service level due, prescription date, prescription clock and deviation open
    Then the access log holds one export entry with the user, the time, the 3 filters and row count 1

  Scenario: AC4 Breach at the boundary of the service level
    Given case "RW-2026-000105" with a RUNNING SERVICE_LEVEL timer due 10 December 2026 09:00
    When the list is read at 10 December 2026 09:00
    Then row "RW-2026-000105" shows service level state RUNNING
    Then when the list is read again at 10 December 2026 09:01, row "RW-2026-000105" shows service level state BREACHED

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
    When the manager filters by product SSME and then chooses Extract with the same filter
    Then the list shows the empty state with message MSG-P3-020
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
| Depends on | RWB-E1-027, RWB-E2-016, RWB-E1-069, RWB-E1-007, RWB-E1-066, RWB-E1-067, RWB-TE-006 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every contact, letter, delivery, offer, payment and hand-over on the case recorded in one ledger, from the Workbench, from the EFS history ACE holds and from the partner portal**, so that **contactability is not found and then lost again**.

### 2. Business rationale

Contact outcomes from collections, letters sent through WIN and work held by partners are recorded in different systems today, so a case owner who picks up a case does not know which number answered or who held the case last. This story brings each of these into the one ledger built in Epic 1 (RWB-E1-066 and RWB-E1-067), reads the EFS history from v_ace_efs_action instead of a Workbench load, adds who held the case before and after each hand-over, gives each entry a retention class, and shows the ledger as an ordered timeline on the case. It meets REQ-ILG-009 to REQ-ILG-013. The business measure is the share of open cases whose last right-party contact is visible on the case, which today is zero for cases that came from EFS.

### 3. Preconditions

- RWB-E1-066 (ledger store and InteractionLedgerWriter), RWB-E1-067 (Workbench events into the ledger), RWB-E1-027 (decision log writer), RWB-E2-016 (case record timeline), RWB-E1-069 (read-only ACE source views) and RWB-TE-006 (outbox delivery) are done.
- v_ace_efs_action, v_ace_efs_action_code and v_ace_contact are granted SELECT to the recovery service identity (V0002).
- v_ace_efs_action carries contact_result and action_contact_status from Section B (V0003, RWB-ACE-001, DL43); the flag stays off in an environment without V0003.
- The EFS ledger outcome list (the action codes that enter the ledger, with their channel) is loaded in efs_ledger_outcome. Until the business lead names the list (DL29, option B), every action code in LOV-ACTION-CODE with a call result enters the ledger with channel CALL (assumed).
- The Retention classes reference table holds a class per ledger event code. Until Compliance sets the periods (DL26), every event code takes class "ILG-STD" (assumed).
- LOV-LEDGER-EVENT (RWB-E1-066) holds the added values PARTNER_RESULT and OFFER (addition).
- The case exists and is open; the reader holds a role with Case record R.
- Feature flag `rwb.integration.ledger-channels` is on.

### 4. Flow

1. Outbox (RWB-TE-006): delivers to consumer "ledger-channels" the events InstructionIssued, PartnerResultSubmitted, NoticeDispatched, NoticeDelivered, TreatmentApproved and ProceedsMatched.
2. LedgerChannelListener: checks the event's idempotency key through IdempotencyGuard (RWB-E1-007) and passes the event to LedgerChannelMapper.
3. LedgerChannelMapper: maps the event to one LedgerEntryCommand with event code, channel, direction, occurred time, source, holder references and links (BR1 to BR5), reading the facts it needs through the owning module's published interface.
4. EfsContactOutcomeReader (on AceDataReady, EV-26, for EFS): reads the day's EFS action rows for accounts linked to open cases from v_ace_efs_action, keeps the action codes in efs_ledger_outcome, and maps each row to a CONTACT entry with source EFS and the person_key of the row; the contact_key of a Workbench or notice entry is the one v_ace_contact holds.
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
| X2 | An EFS row has an action code that is not in efs_ledger_outcome | No entry; counted as excluded in the read summary | None | AC6 |
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
| Independent | Uses the Epic 1 ledger writer, the outbox, the ACE views and the published events; no change to the modules that publish them |
| Negotiable | The EFS outcome list and the retention classes are data (DL29, DL26); the mapping rules are fixed here |
| Valuable | The case owner sees which number answered and who held the case, without asking EFS or the partner |
| Estimable | One listener, one mapper, one read step, six added columns and a timeline section |
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
    Given the ACE batch for EFS with business date 14 December 2026 holds an action row for account "ACC-SYN-0301" with action code "PTP", call result RIGHT_PARTY, contact time 14 December 2026 10:15, promise amount 12,500.00 and promise date 20 December 2026
    Given case owner "U-2001" records a call on 15 December 2026 09:30 to contact key "PHONE:CP-SYN-0301-M" with result NO_ANSWER
    When the EFS batch is complete and the call is saved
    Then the ledger holds a CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and retention class "ILG-STD"
    Then the ledger holds a CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30, contact key "PHONE:CP-SYN-0301-M" and result NO_ANSWER

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
    Given the EFS rows for 14 December 2026 hold 3 rows: action code "PTP" for "ACC-SYN-0301", action code "SYS" not in the outcome list for "ACC-SYN-0301", and action code "PTP" for account "ACC-SYN-0999" on no open case
    When the EFS batch is complete
    Then the ledger holds 1 new EFS entry
    Then the read summary shows 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case

  Scenario: AC7 A ledger write failure loses nothing
    Given the ledger store is unavailable
    When event NoticeDispatched for "NT-SYN-0301" is delivered
    Then the system writes no entry and the delivery stays in the outbox with status RETRYING
    Then an incident is raised
    Then when the store is available the retry delivers the event and the ledger holds one LETTER entry for "NT-SYN-0301"

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
| BR1 | Event to ledger event code: InstructionIssued to HANDOVER; PartnerResultSubmitted to PARTNER_RESULT; NoticeDispatched and NoticeDelivered to LETTER; TreatmentApproved to OFFER; ProceedsMatched to PAYMENT; an EFS action row to CONTACT | events.txt EV-10, EV-14, EV-15, EV-20, EV-21, EV-25, EV-26; LOV-LEDGER-EVENT |
| BR2 | A hand-over between bank owners is the CASE_ALLOCATED or CASE_TRANSFERRED entry of RWB-E1-067, with no channel, enriched with the holder before and after; a hand-over to a partner has channel PORTAL and direction OUTBOUND; a partner result has channel PORTAL and direction INBOUND | REQ-ILG-011; LOV-CHANNEL; LOV-DIRECTION |
| BR3 | An EFS row enters the ledger only when its action code is in efs_ledger_outcome, and only for an account linked to an open case | DL29; INT-07 |
| BR4 | Entries from EFS carry source_system EFS; every other entry carries WORKBENCH, including partner portal entries, which are entered on Workbench screens | LOV-SOURCE; INT-24 |
| BR5 | The contact point is stored as a reference to v_ace_contact.contact_key; the number or address is never copied into the entry | REQ-ILG-014; CTL-11 |
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
| The recovery service identity, EFS read step | Reads v_ace_efs_action and v_ace_contact after the EFS batch (Case record C) |
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
| DF-INT-022 | interaction | contact_key | Write |
| DF-INT-023 | interaction | from_holder_ref | Write |
| DF-INT-024 | interaction | to_holder_ref | Write |
| DF-INT-025 | interaction | treatment_id | Write |
| DF-INT-026 | interaction | proceeds_id | Write |
| DF-INT-027 | interaction | retention_class | Write |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-022 | recovery_case | closed_date | Read |
| DF-CAS-025 | case_account | case_id | Read |
| DF-CAS-026 | case_account | account_key | Read |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-076 | v_ace_contact | contact_key | Read |
| DF-ACE-077 | v_ace_contact | person_key | Read |
| DF-ACE-108 | v_ace_efs_action | efs_record_key | Read |
| DF-ACE-109 | v_ace_efs_action | account_key | Read |
| DF-ACE-110 | v_ace_efs_action | person_key | Read |
| DF-ACE-111 | v_ace_efs_action | action_code | Read |
| DF-ACE-114 | v_ace_efs_action | contact_at | Read |
| DF-ACE-122 | v_ace_efs_action | promise_date | Read |
| DF-ACE-123 | v_ace_efs_action | promise_amount | Read |
| DF-INT-036 | v_ace_efs_action | contact_result | Read (Section B, RWB-ACE-001) |
| DF-LEG-015 | notice | id | Read |
| DF-LEG-016 | notice | case_id | Read |
| DF-LEG-020 | notice | barcode | Read |
| DF-LEG-022 | notice | delivery_status | Read |
| DF-PRT-002 | partner | partner_code | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-FIN-001 | proceeds | id | Read |
| DF-ACE-002 | v_ace_account | account_code | Read |

Reads of other modules' records go through their published interfaces; the ACE rows are read through the P1 interfaces over the views, never from a public table. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Events consumed** (outbox consumer "ledger-channels", RWB-TE-006): EV-10 TreatmentApproved, EV-14 NoticeDispatched, EV-15 NoticeDelivered, EV-20 InstructionIssued, EV-21 PartnerResultSubmitted and EV-25 ProceedsMatched. EV-02 CaseAllocated and EV-04 CaseTransferred stay with the RWB-E1-067 consumer, which this story extends with the holder fields. The EFS read step starts on EV-26 AceDataReady for the EFS source; it is not an outbox delivery. Delivery is at least once; the consumer is idempotent by key. No event is published.

**Published interfaces called**

```java
// recovery.dataengine.ledger.api, RWB-E1-066; must run in the caller's transaction
LedgerEntryRef InteractionLedgerWriter.append(LedgerEntryCommand command);
//   This story adds to LedgerEntryCommand: String contactKey, String fromHolderRef, String toHolderRef,
//   UUID treatmentId, UUID proceedsId, String retentionClass (deliveryStatus and externalRef come from RWB-E2-022)
// RWB-E1-007
boolean IdempotencyGuard.firstTime(String consumer, String idempotencyKey);
// P1 EFS data, over recovery.v_ace_efs_action (RWB-E1-069)
List<EfsContactOutcome> EfsContactHistory.outcomesFor(LocalDate businessDate);
// P1 contact facts, over recovery.v_ace_contact
Optional<ContactView> ContactQuery.byKey(String contactKey);
// P3 case facts
Optional<CaseSummary> CaseQuery.byId(UUID caseId);
List<UUID> CaseQuery.openCaseIdsForAccount(String accountKey);
// P6 notice facts
Optional<NoticeSummary> NoticeQuery.byId(UUID noticeId);   // caseId, contactKey, noticeType, barcode
// S9 instruction facts
Optional<InstructionSummary> InstructionQuery.byId(UUID instructionId); // caseId, partnerCode
```

**GET /api/recovery/v1/cases/{caseId}/interactions** (operationId getCasesCaseidInteractions, existing)

| Item | Value |
|---|---|
| Parameters used | caseId (path), channel, actor, from, to, page, size |
| Response 200 | InteractionPage of Interaction, with the fields of RWB-E1-068 and RWB-E2-022 plus contactKey, fromHolderRef, toHolderRef, treatmentId, proceedsId and retentionClass (recorded in the additions file) |
| 403 | Role lacks Case record R (MSG-P4-002) |
| 404 | Case does not exist or is outside scope (MSG-P4-003) |
| Authorization | Case record, right R; summary masked by role |
| Idempotency | Read only |

**EFS contact read step**

| Item | Value |
|---|---|
| Trigger | AceDataReady (EV-26) for the EFS source, after P1 stamps DP05 |
| Job | A step of JOB-02 after the case creation step, run under the recovery service identity |
| Input | The v_ace_efs_action rows of the business date for accounts linked to open cases |
| Output | Ledger entries; a read summary with read, written, excluded and not-on-a-case counts |
| Idempotency key | "EFS:" + efs_record_key |
| Restart | A rerun for the same business date writes only the entries not yet written |

### 13. Solution plan

**Package.** Folder `recovery/integration/ledger`, Java package `<ACE base package>.recovery.integration.ledger`, for the channel consumer and the EFS read step. The holder enrichment is a change to the RWB-E1-067 mapper in `recovery.dataengine.ledger`, reviewed by its code owners. Front end folder `src/modules/recovery/caserecord/ledger`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LedgerChannelListener | Listener | Outbox consumer "ledger-channels" for the six events; idempotency check; calls the mapper and the writer |
| LedgerChannelMapper | Service | One method per event type implementing BR1, BR2, BR4 and BR5 |
| EfsContactOutcomeReader | Job | Read step after the EFS batch; applies BR3; writes the read summary |
| EfsLedgerOutcomeList | Rule table | Reference rows: action code, channel, in ledger; loaded by RW-REFADM (DL29) |
| HolderEnricher | Service | Adds fromHolderRef and toHolderRef to the CASE_ALLOCATED and CASE_TRANSFERRED commands of RWB-E1-067 |
| RetentionClassResolver | Service | Retention class by event code (BR6), called by InteractionLedgerWriter for every entry |
| InteractionLedgerWriter | Published interface | From RWB-E1-066; this story extends its command |
| LedgerTimelineSection | React component | The ledger section of SCR-03 and the ledger filters on SCR-04: channel, source, actor, date range |

**Database.** Migration in the P1 ledger migration folder adds to interaction: contact_key varchar(255), from_holder_ref varchar(60), to_holder_ref varchar(60), treatment_id uuid, proceeds_id uuid, retention_class varchar(10). The unique key on idempotency_key comes from RWB-E1-066; the append-only trigger tr_interaction_append_only stays in place; the index ix_interaction_case_time serves the read. No import table and no load table are created: the EFS rows are read from v_ace_efs_action.

**Configuration and reference data.** efs_ledger_outcome rows (DL29; assumed default as in section 3); Retention classes reference table (DL26; assumed "ILG-STD"); LOV-LEDGER-EVENT with the added values PARTNER_RESULT and OFFER; LOV-CHANNEL, LOV-DIRECTION, LOV-SOURCE. All loaded by RW-REFADM through the reference data service (RWB-E1-043). Consumer "ledger-channels" listed in rwb.integration.outbox.consumers (RWB-TE-006), not holding a case step, owner role RW-PLATADM.

**Build steps**

1. Add the migration for the six columns; extend LedgerEntryCommand and the Interaction schema in the API specification; regenerate types.
2. Write LedgerChannelMapper with one unit test per event type (BR1, BR2, BR4, BR5).
3. Write RetentionClassResolver against the reference data interface and call it from the writer (BR6).
4. Write LedgerChannelListener with the idempotency check and the failure path that fails the delivery and raises an incident (AC5, AC7, AC8).
5. Write HolderEnricher in the RWB-E1-067 mapper (AC2).
6. Write EfsContactOutcomeReader as a step after the EFS batch, reading v_ace_efs_action and v_ace_contact, with the read summary (AC1, AC6, AC9).
7. Add the ledger section to SCR-03 and the filters to SCR-04 with the empty state (AC3, AC10); run the access and scope tests (AC11).

**Feature flag.** `rwb.integration.ledger-channels`. Off: the consumer acknowledges the six events without writing, the EFS read step does not run and the holder fields stay empty; the Epic 1 ledger is unchanged.

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
| TC-E2-034-01 | AC1, BR3, BR4, BR5, BR6 | System | One EFS action row with a promise; one Workbench call |
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the EFS outcome list, event codes, channels and retention classes are reference data.
- No personal data in logs, tests or prompts; the contact point is a reference and the summary is masked by role.
- No read of another module's tables: case, notice, instruction, treatment, proceeds and EFS facts come through published interfaces; the ACE rows come through the P1 interfaces over the views (boundary rule, RWB-E1-069).
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
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-031, RWB-E1-072, RWB-E2-033, RWB-E2-042 |
| Status | Ready for build |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every active case to show one next action, its owner and its due date, taken from the rule package that moved the case into its current state**, so that **I never open a case and have to work out what it needs**.

### 2. Business rationale

A case owner today reads the case history to decide what is owed next, and a case can wait for weeks with nobody owing anything on it. The route-set rules already hold the action, the owner of the next state and the timer for every move, as rows of the RESTRUCTURE rule package. The Workbench copies these onto the case at each move and shows them on the case and in the case list. A case with no next action is raised to the team manager as an exception.

SY-RULES evaluates the package for the case's state and event through RuleEvaluator, and the action text, the owner role and the timer spec are read from the catalog through `RuleCatalog.row(ruleId, packageVersion)`. The next action therefore names the rule and the package version that set it, and no reader touches the workbook or the generated DRL (D-RCV-36 T3, T5, T6). It meets REQ-WKM-012, REQ-WKM-013 and REQ-WKM-016; the business measure is the count of active cases with no next action, with a target of zero.

### 3. Preconditions

- RWB-E1-018 (case record and transitions), RWB-E1-031 (case list) and RWB-E2-033 (case list with ageing) are done.
- RWB-E1-072 is done: RuleEvaluator and RuleCatalog are published, and the rule package store holds the RESTRUCTURE versions.
- RWB-E2-042 is done: the RESTRUCTURE package rows for the route sets are loaded with action_text, owner_role and timer_spec, pass the scenarios and are in force (RWB-E1-073; DL24).
- The service levels and timers reference table holds a time per state (DL22). Until the business values are loaded it is seeded with 5 working days for each state of the route sets in force (assumed); a state left out of the seed has no row.
- The bank holiday list is loaded in the configuration service under key rwb.calendar.bank-holidays (RWB-E1-042), by RW-REFADM.
- The reader holds a role with Case record R; the transition runs under SY-CASEWF.
- Feature flag `rwb.casewf.next-action` is on.

### 4. Flow

1. SY-RULES: builds the facts for the case's state and event and calls `RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate)`. The result names the package version, the fired rule ID and the outputs, including to_state.
2. SY-CASEWF: moves the case to the to_state in the outputs and, in the same transaction, calls NextActionAssigner with the rule ID and the package version.
3. NextActionAssigner: reads `RuleCatalog.row(ruleId, packageVersion)` and copies the rule's action_text, owner_role and rule_id to the case.
4. TimerSpecResolver: turns the same catalog row's timer_spec into a due date (BR3); when the spec has no fixed duration it reads the service levels and timers reference table for the to_state (BR4).
5. NextActionAssigner: sets next_action_waiting when the owner role belongs to a customer party or a partner user (BR5).
6. NextActionAssigner: when no due date can be found, leaves the due date empty and raises task NEXT_ACTION_MISSING on the exception queue for the team manager (BR7).
7. JOB-05 timer check: every 5 minutes finds active cases with no next action, resolves the rule ID and the rule version from the latest state change in the decision log, and fills the next action from the catalog, or raises the same task once.
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
| X8 | The rule's timer is "same day" | Due date is the business date of the move | None | AC12 |
| X9 | The reader's role does not hold Case record R | Refused with 403 | MSG-P4-002 | AC13 |
| X10 | No RESTRUCTURE package version is in force on the business date | The move is refused; no next action is written | MSG-P3-027 | AC14 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the transitions of RWB-E1-018, the RuleEvaluator and RuleCatalog of RWB-E1-072 and the case list of RWB-E2-033 |
| Negotiable | Action text, owner and timer are rule data; durations for states without a timer are DL22 values |
| Valuable | Every active case states what is owed, by whom and by when |
| Estimable | One assigner, one timer resolver, one job step, one read endpoint, two screen elements |
| Small | Fits one sprint with its tests |
| Testable | Each criterion below has one test with fixed rule rows and dates |

### 7. Acceptance criteria

```gherkin
Feature: Next action on the case

  Background:
    Given the RESTRUCTURE package version "RES-2026.12" is in force and holds rule R-RES-04, which moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER with action "Assign the case to a restructuring officer and start the offer clock", owner role RW-RESTRUCT and timer "2 working days"
    Given the same version holds rule R-SET-13, which moves WITH_OPS_SETTLEMENT on SETTLEMENT_BOOKED to AWAITING_PAYMENT with action "Set the payment due date and wait for the money", owner role CU-BORROW and timer "payment due 30 days"
    Given the bank holiday list holds 31 December 2026 and 1 January 2027

  Scenario: AC1 Every active case carries a next action
    Given case "RW-2026-000401" with status IN_PROGRESS moved by R-RES-04 on 11 December 2026
    When the case is opened
    Then it shows action "Assign the case to a restructuring officer and start the offer clock", owner "Restructuring officer (FCR)" and due date 15 December 2026
    Then the next action names rule R-RES-04 of version "RES-2026.12"

  Scenario: AC2 The routing rules set it
    Given case "RW-2026-000402" in state IN_FCR_QUEUE
    When event CASE_PICKED_UP fires R-RES-04 on Friday 11 December 2026
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2026-12-11) returns ruleId "R-RES-04" and packageVersion "RES-2026.12"
    Then the case holds next action text from R-RES-04, owner role RW-RESTRUCT, rule ID R-RES-04, rule version "RES-2026.12" and due date Tuesday 15 December 2026
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
    Given RESTRUCTURE rule R-RES-03 moves the case to BACK_TO_ROUTE_DECISION with owner role RW-CASEOWN and timer "None"
    Given the service levels and timers table holds 5 working days for BACK_TO_ROUTE_DECISION
    When R-RES-03 fires on Monday 14 December 2026
    Then its catalog row returns timerSpec "None" through RuleCatalog.row("R-RES-03", "RES-2026.12")
    Then the due date is Monday 21 December 2026
    Then the owner shown is the case owner named on the case

  Scenario: AC6 No due date can be found
    Given RESTRUCTURE rule R-DEV-05 moves the case to DEV_WITH_OWNER with owner role RW-LEGAL and timer "deadline driven"
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
    Then each reads the text from RuleCatalog.row("R-RES-04", "RES-2026.12")

  Scenario: AC12 A same day timer
    Given RESTRUCTURE rule R-RES-07 with timer "same day" moves case "RW-2026-000406" on 14 December 2026
    When the next action is set from that rule
    Then the due date is 14 December 2026

  Scenario: AC13 A role without Case record R
    Given user "U-REF-01" holds RW-REFADM and no role with Case record R
    When they call GET /api/recovery/v1/cases/{caseId}/next-action
    Then the response is 403 with MSG-P4-002
    Then no next action data is returned

  Scenario: AC14 No RESTRUCTURE version in force
    Given no RESTRUCTURE package version is in force on 2027-01-04
    When event CASE_PICKED_UP fires for case "RW-2026-000407" on 2027-01-04
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2027-01-04) throws NoPackageInForce
    Then the move is refused with MSG-P3-027 for the package in force check
    Then the case keeps its state and holds no next action from this move
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On every move, the next action text, the owner role and the rule ID come from the catalog row of the firing rule: `RuleCatalog.row(ruleId, packageVersion)` returns action_text, owner_role and timer_spec | FEAT-CWC-28; REQ-WKM-013; D-RCV-36 T6 |
| BR2 | The next action is never entered by a person | REQ-WKM-013 |
| BR3 | timer_spec "n working days" adds n working days; "n days" with any label before it adds n calendar days; "same day", "Same day" and "immediate" give the date of the move; "next working day" adds 1 working day | rule_row.timer_spec through RuleCatalog |
| BR4 | Any other timer_spec, including "None", takes the time for the to_state from the service levels and timers table | DL22 |
| BR5 | The next action is a wait when the owner role is of class Customer party or Partner user; the text starts "Waiting for {owner}:" | role.role_class |
| BR6 | A next action is overdue when its due date is earlier than today and the case is not closed | REQ-WKM-012 |
| BR7 | An active case with no due date or no next action raises one NEXT_ACTION_MISSING task to the team manager | REQ-WKM-016 |
| BR8 | Working days are Monday to Friday, excluding the dates in the bank holiday list | Configuration key rwb.calendar.bank-holidays |
| BR9 | When the owner role is the role of the case's queue, the owner shown is the case owner; otherwise the role name | queue.role_code |
| BR10 | The rule version is the package version label of the RuleResult, and the next action records the version of the move that set it; a later version does not rewrite an action already set | D-RCV-36 T5, T7; R-UNI-38 |
| BR11 | No RESTRUCTURE version in force is a refusal (NoPackageInForce), never a default move and never an empty next action | D-RCV-36 T3; R-UNI-41 |

### 9. State transitions

None. This story does not change a case status. It writes the next action fields on the case in the same transaction as each move made by RWB-E1-018 and RWB-E1-021, and creates or cancels NEXT_ACTION_MISSING tasks (task status OPEN to CANCELED).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Writes the next action fields and the exception task (Case record U, Queue and allocation C) |
| SY-RULES, Drools evaluator | Evaluates the RESTRUCTURE package and serves the catalog row of the firing rule |
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
| DF-REF-296 | rule_row | package_version_id | Read |
| DF-REF-297 | rule_row | drools_rule_name | Read |
| DF-REF-298 | rule_row | outputs | Read |
| DF-REF-036 | role | role_name | Read |
| DF-REF-037 | role | role_class | Read |
| DF-DEC-004 | decision_log_entry | rule_id | Read |
| DF-DEC-005 | decision_log_entry | rule_version | Read |

The rule row is read only through `RuleCatalog.row(ruleId, packageVersion)`; this story reads no workbook and no drl_source. Field IDs are those in the Logical Data Model and Data Dictionary.

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
void NextActionAssigner.assign(UUID caseId, String ruleId, String packageVersion, LocalDate businessDate);
Optional<LocalDate> TimerSpecResolver.dueDate(String timerSpec, String toState, LocalDate from);
```

**Published interfaces called**

```java
// P3, published in RWB-E1-072 (recovery.casewf.rules)
public interface RuleEvaluator {
    RuleResult evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
}
public record RuleResult(String packageCode, String packageVersion, String ruleId, Map<String, Object> outputs) {}
public interface RuleCatalog {
    RuleRow row(String ruleId, String packageVersion);
}
// P7 decision log, for cases with no next action
Optional<RuleRef> DecisionLogQuery.latestStateChange(UUID caseId); // ruleId, ruleVersion
// P4 reference data
RoleInfo ReferenceData.role(String roleCode);          // roleName, roleClass
Optional<Duration> ReferenceData.serviceLevel(String state);
```

`RuleRef` holds the rule ID and the rule version of the decision log entry, and NextActionAssigner passes both to `RuleCatalog.row`. No caller receives a KieBase, a KieSession or a Drools type.

**Job step**

| Item | Value |
|---|---|
| Trigger | JOB-05 Timer check, every 5 minutes |
| Step | Next action check: active cases with next_action_rule_id empty or next_action_due_date empty |
| Input | Case rows of P3; the latest state change from P7; the catalog row through RuleCatalog |
| Output | Filled next action fields, or one NEXT_ACTION_MISSING task |
| Events published | None |
| Idempotency key | Case ID and task code NEXT_ACTION_MISSING: at most one open task per case |
| Restart | The next run picks up any case the last run missed |

### 13. Solution plan

**Package.** The story is in the P2 backlog. The fields, the rule rows and the transitions belong to P3, so the code is in folder `recovery/casewf/nextaction`, Java package `<ACE base package>.recovery.casewf.nextaction`. Front end folder `src/modules/recovery/caserecord/nextaction`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NextActionAssigner | Service | BR1, BR5, BR7, BR9 and BR10; reads the catalog row through RuleCatalog and is called inside the transition |
| TimerSpecResolver | Service | BR3, BR4 and BR8, pure functions with a holiday list input |
| NextActionCheckStep | Job | The JOB-05 step for cases with no next action (BR7, AC11) |
| NextActionController | Controller | GET /cases/{caseId}/next-action |
| NextActionRepository | Repository | Reads and writes the next action fields on recovery_case |
| NextActionPanel | React component | Next action on the SCR-03 header with the waiting text, the overdue marker and the MSG-P2-023 warning |

**Database.** Migration in the P3 migration folder adds to recovery_case: next_action_text varchar(1000), next_action_owner_role varchar(20), next_action_due_date date, next_action_rule_id varchar(20), next_action_waiting boolean NOT NULL DEFAULT false; and `CREATE INDEX ix_case_next_action_missing ON recovery_case (team_code) WHERE closed_date IS NULL AND next_action_due_date IS NULL`. Writes task rows (task_code NEXT_ACTION_MISSING, element_type HUMAN_TASK, discretion REQUIRED, owner_role RW-TEAMMGR). Reads rule_row through RuleCatalog and queue through the P3 repository.

**Configuration and reference data.** Rule rows in the RESTRUCTURE package (RW-COE; RWB-E1-073 and RWB-E2-042); service levels and timers table (DL22; assumed 5 working days); bank holiday list rwb.calendar.bank-holidays (RW-REFADM); role names and classes (P4). JOB-05 stays on Quartz behind the TimerScheduler port (D-RCV-36 T2).

**Build steps**

1. Add the migration and extend the generated types with the NextAction schema and the new operation.
2. Write TimerSpecResolver with a table of timer_spec cases taken from the route-set rows, and unit tests for AC5, AC7 and AC12.
3. Write NextActionAssigner against `RuleCatalog.row(ruleId, packageVersion)` and call it from the transition service in the same transaction; test AC1, AC2, AC3, AC9 and AC10.
4. Add the exception task and its cancel on closure (AC6, AC8).
5. Add NextActionCheckStep to JOB-05 (AC11).
6. Write NextActionController and NextActionPanel; add the next action fields to the Case items of GET /cases and to the export columns (AC4).
7. Add the access test, the no-version test and the contract test for the new operation (AC13, AC14).

**Feature flag.** `rwb.casewf.next-action`. Off: the assigner is not called, the step does not run and the panel and columns are hidden. The rule evaluation is also behind `rwb.p3.drools` (RWB-E1-072).

**Done when.** The tests in section 16 pass and the report of active cases with no next action reads zero on the SIT data set after JOB-05 has run.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-023 | The case has no next action or no due date (new) | This case has no next action. It is on the exception list for {team}. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-004 | A transition commits against a changed version | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

For MSG-P3-027 in this story {check} is "package in force" and {detail} names the package code RESTRUCTURE and the business date only. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-03 Case record, states Read only, Editable and On hold: the header shows the next action, its owner, its due date and the rule ID with its version; a wait shows "Waiting for {owner}" and the wait end date; an overdue action carries the text "Overdue"; a missing action shows MSG-P2-023. SCR-02 Case list: next action, next action owner and due date columns with the overdue marker. SCR-09 Exception queue: the team manager sees NEXT_ACTION_MISSING tasks.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-035-01 | AC1, BR1, BR9, BR10 | System | Case moved by R-RES-04 on 11 December 2026 |
| TC-E2-035-02 | AC2, BR1, BR2, BR3, BR10 | System | CASE_PICKED_UP on Friday 11 December 2026 |
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
| TC-E2-035-13 | AC13, Access | Access | RW-REFADM reads the next action; refused with MSG-P4-002 |
| TC-E2-035-14 | AC14, BR11 | System | No RESTRUCTURE version in force on 2027-01-04; NoPackageInForce and MSG-P3-027 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: action text, owner, timer, service levels and holidays are data.
- No personal data in logs, tests, workflow history or prompts: the next action holds rule text only.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the decision log and the role table are read through P7 and P4 interfaces.
- The parser recognizes timer patterns; it never holds a duration for a named state.
- The rule row is read only through RuleCatalog; the workbook, drl_source and the rule_row row are never read by this story.
- One evaluator: the move calls RuleEvaluator and no second rule engine decides the to_state.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-012 | Every open case carries one next action with owner and due date | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-RES-04, R-SET-13 | TC-E2-035-01, TC-E2-035-03, TC-E2-035-04, TC-E2-035-08, TC-E2-035-13 |
| REQ-WKM-013 | The next action comes from the rule that moved the case | Business Requirements Epic 2, section 3.2 | FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-03, R-RES-04, R-SET-13 | TC-E2-035-02, TC-E2-035-05, TC-E2-035-07, TC-E2-035-09, TC-E2-035-10, TC-E2-035-12, TC-E2-035-14 |
| REQ-WKM-016 | A case with no next action is reported as an exception | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-DEV-05 | TC-E2-035-06, TC-E2-035-11 |
| REQ-WKM-014 | Next action visible on the case record and every queue view | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01 |
| REQ-WKM-015 | An overdue next action escalates like a service level breach | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01 |

### 19. Out of scope

- Escalation when a next action passes its due date: RWB-E2-015 (REQ-WKM-015).
- The next action column in the queue view screens: RWB-E2-011.
- The values of the service levels per state: DL22.
- Loading the route set rule rows beyond allocation, assignment and transfer: DL24; the RESTRUCTURE rows are RWB-E2-042.
- The RESTRUCTURE package checks, scenarios and approval (RWB-E1-073).
- Temporal durable timers that replace JOB-05 in Epic 3 (ADR-011).
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
    Then when both owners hold 150 open cases and the model places case "RW-2026-000502", that case is in queue "MTG-BKK-OVF" with no owner and status NEW

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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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

## RWB-E2-037 Temporal observability and run books

| Item | Value |
|---|---|
| Story key | RWB-E2-037 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None (platform enabler) |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, section 6.12 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-070, RWB-E1-071, RWB-E1-056 |
| Status | Ready for build |

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **Temporal metrics, an alert for every failed or stuck workflow and a dashboard that shows workflow volume by type and status, each alert with its own run book**, so that **a workflow problem is seen before a case waits**.

### 2. Business rationale

Case workflows from Epic 3 wait for days on durable timers, and a workflow that has stopped moving looks exactly like a workflow that is waiting. Nothing in the Workbench watches a workflow execution today: the job monitor of RWB-E1-056 watches Quartz jobs, and the platform dashboard of RWB-E1-070 watches the five Temporal services, not the workflows those services run. Without this story the first sign of a workflow that cannot progress is a case owner asking why the case has not moved.

This story adds the three signals that cover the ways a workflow stops: an execution that closes FAILED or TIMED_OUT, an execution with no progress for temporal.stuck.hours (24, assumed), and a schedule-to-start latency above its threshold. It adds one Grafana dashboard grouped by workflow type and status with no personal data, and a run book for each alert so that the platform administrator acts without the developer. It meets REQ-DRI-007 (a named owner and a tested way back for every failure). The measure is that every alert reaches the on-call rota within 5 minutes in SIT and names a run book.

### 3. Preconditions

- RWB-E1-070 is done: the Temporal cluster, the namespace rwb-recovery, mTLS, the Web UI and the metrics scrape to the ACE monitoring stack exist in DEV and SIT.
- RWB-E1-071 is done: the worker polls rwb-platform, carries a build ID, runs PlatformSmokeWorkflow daily and writes its PLATFORM_SMOKE decision log entry.
- RWB-E1-056 is done: job_catalog, the run book catalog, RunbookCompletenessTest and its eight run book headings exist and accept a new job and a new run book.
- Prometheus, Alertmanager and Grafana run in the ACE monitoring namespace, and the platform on-call rota and the incident queue of the operations team exist.
- The parameter temporal.stuck.hours = 24 is in the catalog through RWB-E1-042; the value is assumed until the platform administrator confirms it with the operations team.
- The SIT worker registers the test-only workflow CaseHoldWorkflow on rwb-platform, which can be held with no progress or left on a timer; it is not deployed to UAT or PROD.
- The scanner runs as SY-CASEWF with the client certificate of RWB-E1-070 and holds no grant on the Temporal databases.
- Feature flag rwb.p3.temporal is on in SIT.

### 4. Flow

1. Prometheus: scrapes the Temporal server metrics of RWB-E1-070 and the worker SDK metrics of RWB-E1-071 every 15 seconds.
2. TemporalAlertRules: evaluate TemporalWorkflowFailed when an execution closes FAILED or TIMED_OUT, and TemporalScheduleToStartLatency when the p95 schedule-to-start latency on a task queue is above 60 seconds for 10 minutes.
3. StuckWorkflowScanner (Quartz, every 15 minutes): calls ListWorkflowExecutions for RUNNING workflows whose StartTime is older than temporal.stuck.hours, then reads the history summary of each candidate through the frontend.
4. StuckWorkflowScanner: marks a candidate stuck only when it has no history event for temporal.stuck.hours, no open timer and no activity in retry, and publishes the count as workflow_stuck by workflow type.
5. TemporalWorkflowStuck: fires on a stuck count above zero with MSG-P3-037, the workflow ID and the hours since the last event.
6. Alertmanager: routes each alert to the platform on-call rota and the incident queue, with the run book path in the annotation and one alert per workflow and condition.
7. Platform administrator: opens the dashboard, reads the workflow type, task queue and build ID, and follows the run book for the check, restart or drain step.
8. Dashboard "Temporal workflows": shows running, failed, completed and timed-out counts by type, schedule-to-start latency by task queue, task queue backlog, stuck workflows and worker build IDs, all from the four search attributes.
9. StuckWorkflowScanner: records its last successful run; a failed scan marks the stuck panel stale and raises an incident, and never publishes a zero.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The Temporal frontend is unreachable from the scanner, so the visibility query fails | No stuck value is published and no stuck alert is raised; the scanner failure counter rises; the stuck panel shows data stale since the last good scan; an incident reaches RW-PLATADM | None (incident and metric only) | AC6 |
| X2 | An alert rule has no run book, or its run book lacks one of the eight sections | The pipeline fails naming the alert and the missing section; the rule file is not deployed | None (build log) | AC7 |
| X3 | A workflow makes progress between the scan and the delivery of its alert | The alert resolves at the next evaluation; no page is sent and no incident is opened | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds alerts, one Quartz scanner, one dashboard and three run books on the platform of RWB-E1-070 and the worker of RWB-E1-071 |
| Negotiable | Thresholds, the stuck window, the repeat interval, the panels and the routing rota are configuration; the three signals and the run book rule are fixed |
| Valuable | A workflow problem reaches a named owner before a case owner notices the case has stopped |
| Estimable | Three alert rules, one scanner, one dashboard, one run book map and three run books |
| Small | Fits two weeks with its checks |
| Testable | Each criterion in section 7 has one test in section 16, on fixed workflows and fixed thresholds |

### 7. Acceptance criteria

```gherkin
Feature: Temporal observability and run books

  Background:
    Given the Temporal cluster of RWB-E1-070 runs in SIT with namespace rwb-recovery
    Given the worker of RWB-E1-071 polls rwb-platform with build ID "9f3c2a1-418"
    Given the parameter temporal.stuck.hours is 24
    Given Alertmanager routes the Workbench platform alerts to the platform on-call rota

  Scenario: AC1 A failed workflow raises an alert within five minutes
    Given workflow "platform-smoke-20261116" started at 07:00 on 16 November 2026 on task queue rwb-platform
    When the workflow closes FAILED at 10:12
    Then the rule TemporalWorkflowFailed is FIRING at the 10:13 evaluation with severity "page"
    Then the alert annotation carries MSG-P3-037 with workflowId "platform-smoke-20261116" and hours 3
    Then Alertmanager delivers the alert to the platform on-call rota within 5 minutes of the close
    Then the dashboard count of failed PlatformSmokeWorkflow executions for the day is 1

  Scenario: AC2 A workflow with no progress raises an alert, and a timed wait does not
    Given workflow "case-RW-2026-000123" of type CaseHoldWorkflow on task queue rwb-platform is RUNNING
    Given its last history event is at 09:00 on 15 November 2026 and it has no open timer and no activity in retry
    Given workflow "case-RW-2026-000124" of the same type is RUNNING and started timer "wait-30-days" at 10:00 on 14 November 2026
    When StuckWorkflowScanner runs at 09:05 on 16 November 2026
    Then "case-RW-2026-000123" is marked stuck with 24 hours since its last progress
    Then TemporalWorkflowStuck is FIRING with MSG-P3-037, workflowId "case-RW-2026-000123" and hours 24
    Then "case-RW-2026-000124" is not marked stuck and no alert exists for it

  Scenario: AC3 Schedule-to-start latency raises an alert
    Given the worker stops polling rwb-platform at 11:00 on 16 November 2026
    Given the rule threshold is a p95 schedule-to-start latency of 60 seconds for 10 minutes
    When 12 tasks wait on rwb-platform and the p95 reaches 120 seconds at 11:12
    Then TemporalScheduleToStartLatency is FIRING with taskQueue "rwb-platform" and p95 "120s"
    Then Alertmanager delivers the alert to the platform on-call rota
    Then the dashboard panel "Schedule-to-start latency" shows the spike for rwb-platform
    When the worker resumes at 11:20 and the p95 returns below 60 seconds
    Then the alert resolves at the next evaluation

  Scenario: AC4 The dashboard shows volume by type and status with no personal data
    Given the dashboard "Temporal workflows" is provisioned from ops/monitoring/temporal/workflow-dashboard.json
    When U-70 opens it for the rwb-recovery namespace
    Then it shows running, failed, completed and timed-out counts by workflow type
    Then it shows schedule-to-start latency by task queue, task queue backlog, stuck workflows and worker build IDs
    Then every panel query uses the search attributes CaseId, Stage, ProductGroup and QueueCode only
    Then DashboardPersonalDataCheck finds no person field and no payload field in the 40 panel queries
    Then no panel shows a workflow input, a workflow output or a history event payload

  Scenario: AC5 Every alert has a run book
    Given the rule file holds TemporalWorkflowFailed, TemporalWorkflowStuck and TemporalScheduleToStartLatency
    When RunbookCompletenessTest runs in the pipeline
    Then each alert names a run book in docs/operations/runbooks with the eight sections
    Then each run book names the alert, the check, the restart or drain step and the escalation
    Then the build passes with the three run books

  Scenario: AC6 The scanner cannot reach the frontend
    Given the Temporal frontend is unreachable from the scanner at 09:05 on 16 November 2026
    When StuckWorkflowScanner runs
    Then it publishes no workflow_stuck value and raises no TemporalWorkflowStuck alert
    Then temporal_scanner_failures_total increases by one
    Then the dashboard panel "Stuck workflows" shows "data stale since 09:05"
    Then an incident reaches RW-PLATADM naming the scanner error
    Then no workflow is marked stuck

  Scenario: AC7 An alert with no run book fails the build
    Given a branch adds the alert TemporalWorkerDown to the rule file with no entry in the alert-to-run-book map
    When RunbookCompletenessTest runs
    Then the build fails naming "TemporalWorkerDown" and the missing run book
    Then the rule file is not deployed to SIT or PROD

  Scenario: AC8 An alert clears before it is delivered
    Given TemporalWorkflowStuck is PENDING for "case-RW-2026-000125" at 09:05 with 25 hours since its last event
    When the worker picks up the workflow and it records a new history event at 09:06
    Then the alert resolves at the 09:10 evaluation
    Then Alertmanager sends no page and opens no incident
    Then the alert history keeps the PENDING and RESOLVED states with their times
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A workflow that closes FAILED or TIMED_OUT raises TemporalWorkflowFailed with MSG-P3-037, and the alert reaches the on-call rota within 5 minutes of the close | REQ-DRI-007; AC1 |
| BR2 | A RUNNING workflow with no history event for temporal.stuck.hours (24, assumed), no open timer and no activity in retry raises TemporalWorkflowStuck; a workflow that waits on a durable timer is never stuck | AC2 |
| BR3 | A p95 schedule-to-start latency above 60 seconds for 10 minutes on a task queue raises TemporalScheduleToStartLatency; both values are rule-file configuration | AC3 |
| BR4 | The dashboard groups by workflow type and status and reads the four search attributes only; no panel reads a payload, a history event or a case table | D-RCV-36 T1; AC4 |
| BR5 | Every alert names a run book with the eight sections of RWB-E1-056; RunbookCompletenessTest fails the build when one is missing or incomplete | RWB-E1-056; AC5 |
| BR6 | The scanner reads visibility and history through the Temporal frontend API over mTLS and never reads the Temporal databases; it holds no grant on them | D-RCV-36 T1 |
| BR7 | A failed scan publishes no stuck value and marks the panel stale; it never publishes zero in place of a result | AC6 |
| BR8 | One alert per workflow and condition; a repeated evaluation updates the same alert and opens no second incident | AC8 |
| BR9 | An alert resolves when its condition clears, and a resolved alert leaves no open incident and no open page | AC8 |
| BR10 | Thresholds, the stuck window, the repeat interval, the panel list and the routing rota are configuration, never code | REQ-DRI-007 |

### 9. State transitions

None for a case. This story changes the status of an alert and reads the status of a workflow execution.

| From | Event | Condition | To |
|---|---|---|---|
| None | Rule evaluates true | A workflow closes FAILED or TIMED_OUT | FIRING |
| None | Rule evaluates true | No progress for 24 hours, no open timer, no activity in retry | FIRING |
| None | Rule evaluates true | p95 latency above 60 seconds for 10 minutes | FIRING |
| PENDING | Rule evaluates true | Condition still true at delivery | FIRING |
| PENDING | Rule evaluates false | Condition cleared before delivery | RESOLVED, no page |
| FIRING | Rule evaluates false | Condition cleared | RESOLVED |
| RUNNING | Execution closes | A workflow ends | COMPLETED, FAILED or TIMED_OUT; alert state follows the rule |

The workflow states COMPLETED, FAILED and TIMED_OUT are Temporal's; no recovery case status changes.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM | Reads the alerts, the dashboard and the scanner status; works the incident and follows the run book; silences an alert for the duration of an open incident and records the silence in it (Platform administration, R) |
| RW-AUDIT | Reads the dashboard and the alert history (Platform administration, R) |
| RW-TRIBE | Writes the rule file, the dashboard JSON and the run books through the change process; may not silence an alert in PROD |
| RW-CASEOWN and the other case roles | No access to the alerts or the dashboard; they see the case, not the engine |
| SY-CASEWF | Runs the scanner and publishes the metrics; holds no screen right |
| SY-RULES | No part in this story |
| No delegation of authority level applies | An operational alert is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| None (platform enabler) | None in the recovery schema | None | None |

Alert state lives in Prometheus and Alertmanager, and workflow, timer and task state lives in Temporal persistence and visibility (RWB-E1-070). The scanner's last run, its owner and the alert-to-run-book map live in job_catalog through RWB-E1-056. No DF-REF, DF-CAS or DF-DEC field is added or changed, and the dashboard reads the search attributes CaseId, Stage, ProductGroup and QueueCode only. The Physical Schema v6 is unchanged.

### 12. Contract

No Workbench endpoint. This story adds no path under /api/recovery/v1. The interfaces are the monitoring stack and the Temporal frontend.

| Interface | Method | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| Prometheus scrape | HTTPS GET /metrics, port 9090 | Scrape of the Temporal server and worker SDK metrics | OpenMetrics text | None | Network policy from the ACE monitoring namespace only | Read only |
| Alertmanager | HTTPS POST /api/v2/alerts | Alert name, labels, annotations with MSG-P3-037 and the run book path | 200 when accepted | 400 malformed alert; 503 receiver down | Alertmanager API from the Prometheus pods only | Alert fingerprint: a repeat updates the same alert and opens no second incident |
| Temporal frontend | gRPC over mTLS, port 7233: ListWorkflowExecutions, GetWorkflowExecutionHistory, DescribeWorkflowExecution | namespace rwb-recovery, query RUNNING and StartTime older than 24 hours, workflow ID | WorkflowExecution and history summary | TLS handshake failure; PERMISSION_DENIED; NOT_FOUND namespace; UNAVAILABLE | Client certificate of SY-CASEWF with the namespace claim | Read only |
| Grafana provisioning | HTTPS 443, dashboard JSON from the repository | Dashboard definition and the data sources | 200 when provisioned | 400 malformed JSON; 403 data source refused | Grafana administrator through the pipeline; viewers RW-PLATADM and RW-AUDIT | Repeat provisioning of the same JSON changes nothing |

The scanner never receives a Workbench JWT and never reads the Temporal databases. The dashboard reads Prometheus and the Temporal data source, not a Workbench table.

### 13. Solution plan

**Package.** No Java business package. The rule file and the dashboard live in `ops/monitoring/temporal/`; the scanner lives in `recovery/integration/ops/temporal` (Java package `recovery.integration.ops.temporal`); the run books live in `docs/operations/runbooks/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemporalAlertRules | Prometheus rule file | The three alerts, their thresholds, their annotations and the repeat interval (BR1 to BR3, BR8) |
| AlertRoutingConfig | Alertmanager configuration | Routes each alert to the platform on-call rota and the incident queue with the run book path |
| WorkflowVisibilityClient | Client | Lists RUNNING workflows and reads a history summary through the frontend gRPC with mTLS; reads no database (BR6) |
| StuckWorkflowScanner | Job | Quartz, every 15 minutes: the candidate query, the stuck test and the workflow_stuck metric (BR2, BR7) |
| TemporalScannerMetrics | Service | Publishes workflow_stuck by workflow type, temporal_scanner_failures_total and the last successful scan time |
| TemporalWorkflowDashboard | Dashboard | Grafana JSON for the five panel groups, from the four search attributes (BR4) |
| DashboardPersonalDataCheck | Test | Scans every panel query and the provisioned JSON for a person field or a payload field and fails the build (BR4) |
| AlertRunBookMap | Configuration | Alert name to run book path, read by RunbookCompletenessTest (BR5) |
| TemporalObservabilityRunBooks | Document | Three run books with the eight sections of RWB-E1-056 |
| CaseHoldWorkflow | Test workflow | Test scope only: a workflow that can be held with no progress or left on a 30-day timer, for the scanner tests and the SIT fixture (AC2, AC8) |

**Database.** No migration. The scanner gets one job_catalog row through RWB-E1-056 as a data change, with its owner role, schedule, run book path and alert threshold. No table is created or changed.

**Configuration and reference data**

- Parameter through RWB-E1-042: temporal.stuck.hours = 24 (assumed).
- Rule-file values: the 5-minute failure window, the 60-second p95 latency threshold and the 10-minute duration, owned by RW-PLATADM.
- Alertmanager route, repeat interval and on-call rota from the ACE monitoring configuration.
- No business parameter and no reference table in this story.

**Build steps**

1. Add the three alert rules and the run book annotations; unit test the expressions with synthetic metric series for AC1 and AC3.
2. Build WorkflowVisibilityClient against the SIT frontend with mTLS; prove it reads no database and returns the candidate list.
3. Build StuckWorkflowScanner with the candidate query, the timer and retry exclusions and the stale marker; test AC2 and AC6.
4. Add the workflow_stuck and scanner failure metrics and the last-successful-run time.
5. Import the dashboard, run DashboardPersonalDataCheck over every panel query, and test AC4.
6. Write the three run books, add the alert-to-run-book map and pass RunbookCompletenessTest; test AC5 and AC7.
7. Run the alert drill in SIT: fail a smoke workflow, hold a test workflow, stop the worker and clear each alert; test AC8.

**Feature flag.** None. The alerts and the dashboard are operations assets; with rwb.p3.temporal off, no workflow starts and the scanner reports zero stuck workflows from a successful scan.

**Done when.** The tests in section 16 pass in SIT, the three alerts fire and resolve on the test fixtures, each alert names a complete run book, and the dashboard passes the personal-data check.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-037 | A workflow has failed, or has not moved for the stuck window | Workflow {workflowId} has failed or has not moved for {hours} hours. |

MSG-P3-037 is new and is added to Error and Message Standard v4. It is carried in the annotation of TemporalWorkflowFailed and TemporalWorkflowStuck, with {hours} read from the workflow age at failure or from the scanner. The latency alert has its own summary text and names the task queue and the p95; it uses no new message ID. A failed scan is reported through the incident and the metric, not through a message.

### 15. Screens and states

No Workbench screen in this story. The operational view is the Grafana dashboard "Temporal workflows" with two data states: current, and data stale since the last successful scan. The dashboard shows running, failed, completed and timed-out counts by workflow type, schedule-to-start latency, task queue backlog, stuck workflows and worker build IDs. Alertmanager shows the alert states PENDING, FIRING and RESOLVED. The Workbench job monitor of RWB-E1-056 shows the scanner's last run, status and duration. The platform screens of Epic 8 do not repeat this data.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-037-01 | AC1, BR1 | System | platform-smoke-20261116 failed at 10:12; alert evaluated at 10:13 |
| TC-E2-037-02 | AC2, BR2 | System | case-RW-2026-000123 held 24 hours; case-RW-2026-000124 on a 30-day timer |
| TC-E2-037-03 | AC3, BR3 | System | Worker stopped 11:00 to 11:20; p95 120 seconds at 11:12 |
| TC-E2-037-04 | AC4, BR4 | System | Dashboard JSON with 40 panel queries; search attributes only |
| TC-E2-037-05 | AC5, BR5 | System | Three alert rules and three run books |
| TC-E2-037-06 | AC6, BR7 | System | Frontend unreachable at 09:05; scanner run |
| TC-E2-037-07 | AC7, BR5 | System | Branch adds TemporalWorkerDown with no run book |
| TC-E2-037-08 | AC8, BR8, BR9 | System | Stuck alert PENDING at 09:05; progress at 09:06; delivery at 09:10 |
| TC-E2-037-09 | Operational | Operational | Rule files loaded in the ACE Prometheus; a worker stop raises and clears the latency alert |
| TC-E2-037-10 | Operational | Operational | DashboardPersonalDataCheck over all panel queries and the provisioned JSON |

The checks are run by the platform administrator in SIT and recorded in the release evidence; there is no Workbench endpoint and no Access test in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the stuck window, the thresholds, the repeat interval and the routing rota are configuration.
- No personal data in logs, tests, workflow history or prompts: the dashboard reads the four search attributes only; the tests use synthetic workflow IDs.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: this story reads no case and no ACE table.
- The scanner reads visibility and history through the frontend API and holds no grant on the Temporal databases.
- No panel reads a payload, a history event or a case field, and no alert annotation carries a payload.
- A failed scan never publishes zero, and the panel says the data is stale.
- No alert without a run book, and no run book that names a person.
- No silencing of an alert outside an open incident.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner and has a tested way back | Epic 2, 3.2; Program, 6.12 | None (platform enabler) | All recovery processes | R-UNI-40 | TC-E2-037-01, TC-E2-037-02, TC-E2-037-03, TC-E2-037-05, TC-E2-037-06, TC-E2-037-07, TC-E2-037-08 |

### 19. Out of scope

- The Temporal cluster, namespace, mTLS, Web UI and platform dashboard (RWB-E1-070).
- The worker, the codec and the smoke workflow (RWB-E1-071).
- The codec server, decode and the Temporal admin audit (RWB-E2-038).
- Backup, point-in-time restore, zone failover, upgrade procedure and archive (RWB-E2-039).
- The replay gate, history export for tests and build ID rollout (RWB-E2-040).
- Case-level service level alerts and the next action overdue marker (RWB-E2-015).
- Application performance monitoring of the Workbench API and the Quartz job alerts (RWB-E1-056).
- Temporal Schedules and any Temporal alerting on a schedule (Epic 3).
---

## RWB-E2-038 Temporal security, codec server and admin audit

| Item | Value |
|---|---|
| Story key | RWB-E2-038 |
| Epic | E2, release 31 December 2026 |
| Module | P4 Access and administration |
| Feature | None (platform enabler) |
| Requirement IDs | REQ-DRI-001, REQ-DRI-005 |
| BRD section | Business Requirements Epic 2, section 3.4; Business Requirements Program, sections 6.7 and 6.9 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-070, RWB-E1-071, RWB-E1-039 |
| Status | Ready for build |

### 1. Story

As a **security administrator (RW-SECADM)**, I want **decode of workflow payloads limited to an open break-glass grant and every decode, terminate, reset and signal written to the decision log**, so that **workflow history cannot leak personal data and no administrative action on a case workflow is unrecorded**.

### 2. Business rationale

The history is encrypted by PdpaPayloadCodec (RWB-E1-071), which protects it at rest, but the Temporal Web UI needs a codec server to show a payload. A codec server that answers any Workbench session turns the encryption into a display setting: every history the user can open becomes clear personal data, and no log names the reader. At the same time, terminate, reset and signal change the path of a live case, and today the only record is the frontend audit log inside the Temporal namespace, which a Workbench audit query by case cannot read.

This story puts both behind one rule: a decode is allowed only for RW-SECADM with an open break-glass grant against an incident, and every administrative call writes a decision log entry before the frontend executes it. It meets REQ-DRI-001 (one record per decision) and REQ-DRI-005 (no action without its entry), and it supports NFR-045 for personal data in workflow history. The measure is that no clear payload leaves the codec server without an AC-READ entry naming the grant, and that the daily reconciliation finds no administrative action without an entry.

### 3. Preconditions

- RWB-E1-070 is done: the cluster, the namespace rwb-recovery, mTLS, and the Web UI behind Entra ID OIDC with RW-PLATADM operate and RW-AUDIT read.
- RWB-E1-071 is done: PdpaPayloadCodec encrypts every payload with a Key Vault key and records the key version in the payload metadata.
- RWB-E1-039 is done: break-glass grants through POST /admin/break-glass-grants, the AC-BGON entry, the grant end time, GET /admin/access-log and LOV-DECISION with AC-READ, AC-DENY and AC-BGON.
- LOV-DECISION gains PLATFORM_ADMIN as a system event code through the versioned reference load of RWB-E1-043, loaded by RW-DATASTEW; the addition is recorded in the additions file.
- The codec server runs inside the recovery module behind the internal ingress, and the Web UI codec endpoint setting names it per environment.
- Key Vault holds the codec key with versions 1, 2 and 3, version 2 current at the start of the test and version 3 after the rotation drill; SY-CASEWF holds unwrap on every enabled version.
- The Temporal frontend loads the authorizer plugin from the values file of RWB-E1-070 and can reach the internal audit endpoint over mTLS.
- Feature flag rwb.p3.temporal is on in SIT.

### 4. Flow

1. RW-SECADM: raises a break-glass request in the bank IAM against an open incident for area PLATFORM_ADMINISTRATION and right R; the IAM approves it, and the account joins the break-glass group until the window ends (RWB-E1-039).
2. RW-SECADM: calls POST /admin/break-glass-grants with the incident reference, the IAM request ID, area PLATFORM_ADMINISTRATION, right R, the scope and the reason; the grant is ACTIVE with an end time.
3. RW-SECADM: opens a workflow in the Temporal Web UI and asks for a payload; the Web UI calls the codec server POST /decode, the Temporal codec server protocol, with the namespace, workflow ID, run ID and the encoded payloads.
4. BreakGlassGrantChecker: checks the session, the role RW-SECADM, the ACTIVE grant, its area and its right; a missing, ended or wrong-area grant is a refusal.
5. PayloadGuard: checks the payload count and size and that every payload carries codec metadata with a key version; a payload without metadata is refused whole.
6. CodecKeyResolver: resolves the key version from the metadata and unwraps it in Key Vault; it never guesses a version and never falls back to a clear read.
7. TemporalAdminAuditWriter: writes the AC-READ entry with the actor, operation DECODE, workflow ID, run ID, payload count, grant and incident through DecisionLogApi; the controller returns the clear payloads only after the entry commits.
8. RW-PLATADM: terminates, resets or signals a workflow from the Web UI or the CLI; the Temporal authorizer plugin passes the operation, workflow ID, run ID, actor, grant or reason and the frontend request ID to the audit writer over mTLS.
9. TemporalAdminAuditWriter: writes the PLATFORM_ADMIN entry and returns its ID; the authorizer allows the frontend call only on 201, and a 503 denies it with PERMISSION_DENIED, so the workflow is unchanged.
10. TemporalAdminAuditListener: every day at 02:00 reads the frontend audit log, matches each terminate, reset and signal to an entry, and raises an incident for any gap without writing an entry of its own.
11. RW-AUDIT: reads the AC-READ, AC-DENY and PLATFORM_ADMIN entries through GET /admin/access-log and holds no decode right.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A history payload carries no codec metadata, because a test or a job wrote it without the codec | The whole request is refused; no payload is returned; one AC-DENY entry records the payload index and the reason; an incident reaches RW-SECADM and RW-PLATADM; no key is guessed | None (422 refusal text) | AC5 |
| X2 | The decision log store is unavailable when an administrative call arrives | The authorizer receives 503 and denies the call with PERMISSION_DENIED; the workflow is unchanged and no entry exists | None (503 refusal text) | AC6 |
| X3 | The frontend audit log holds a terminate, reset or signal with no decision log entry | The reconciliation reports the gap and raises an incident; no entry is invented | None (incident only) | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the cluster and Web UI of RWB-E1-070, the codec of RWB-E1-071 and the break-glass grant of RWB-E1-039; it adds the decode path and the audit path only |
| Negotiable | Payload limits, the reconciliation time, the key version list and the refusal texts are configuration; the role rule and the write-before-act rule are fixed |
| Valuable | A clear payload is one grant and one log entry away, and no administrative action on a case workflow is invisible to audit |
| Estimable | One controller, one grant check, one key resolver, one authorizer plugin, one audit writer and one daily reconciliation |
| Small | Fits two weeks with its tests |
| Testable | Each criterion in section 7 is one test in section 16 on fixed grants, key versions and workflows |

### 7. Acceptance criteria

```gherkin
Feature: Temporal security, codec server and admin audit

  Background:
    Given the Temporal Web UI of RWB-E1-070 uses the codec server of the recovery module as its codec endpoint
    Given the codec key has versions 1 and 2 enabled, and version 2 is current
    Given workflow "case-RW-2026-000301" holds a salary slip payload encrypted with key version 2

  Scenario: AC1 Decode needs RW-SECADM and an open grant
    Given U-88 holds RW-SECADM and the ACTIVE break-glass grant "BG-2026-0042" for area PLATFORM_ADMINISTRATION, right R, ending at 12:00 on 16 November 2026
    When U-88 asks the Web UI to decode the payload at 11:40
    Then the Web UI calls the codec server POST /decode and receives 200 with the clear payload
    Then one decision_log_entry exists with decision code AC-READ, actor U-88, operation DECODE, grant "BG-2026-0042" and incident "INC0004521"
    Then the entry is committed before the response carries the payload
    When U-88 asks again at 12:05, after the grant ended
    Then the response is 403 with MSG-P4-002 and no payload is returned
    When U-53 holds RW-PLATADM with an active grant and asks at 11:50
    Then the request is refused with 403 and MSG-P4-002 because decode needs RW-SECADM

  Scenario: AC2 Every decode and every administrative call writes an entry
    Given U-70 holds RW-PLATADM and no break-glass grant
    Given U-88 holds RW-SECADM with grant "BG-2026-0042"
    When U-88 decodes a payload of "case-RW-2026-000301"
    When U-70 terminates "case-RW-2026-000302" with reason "stuck on a bad activity"
    When U-70 resets "case-RW-2026-000303" to event 12
    When U-70 sends signal CaseEvent to "case-RW-2026-000304"
    Then four decision_log_entry rows exist: AC-READ for the decode and PLATFORM_ADMIN for TERMINATE, RESET and SIGNAL
    Then each row carries namespace rwb-recovery, the workflow ID, the run ID, the actor and the reason, and the grant where one applies
    Then the TERMINATE row is committed before the frontend reports "case-RW-2026-000302" TERMINATED
    Then no row holds a payload or a clear personal data field

  Scenario: AC3 Other roles are refused
    Given U-53 holds RW-AUDIT with an active grant for area PLATFORM_ADMINISTRATION, right R
    Given U-62 holds RW-CASEOWN and no grant
    When U-53 calls the decode endpoint for "case-RW-2026-000301"
    Then the response is 403 with MSG-P4-002 because RW-AUDIT reads the log and does not decode
    When U-62 calls the decode endpoint
    Then the response is 403 with MSG-P4-002 and no payload is returned
    Then one AC-DENY entry records each refusal with the actor and the area, and no payload

  Scenario: AC4 A key rotation keeps old histories decodable
    Given "case-RW-2026-000301" was written when key version 1 was current
    Given "case-RW-2026-000304" was written when key version 2 is current
    When the key is rotated to version 3 and versions 1 and 2 stay enabled
    Then a decode of "case-RW-2026-000301" with a grant returns the clear payload using version 1
    Then a decode of "case-RW-2026-000304" uses version 2
    Then a workflow started after the rotation writes payloads with version 3
    Then the run book keeps every version that a history inside the retention or the archive of RWB-E2-039 names

  Scenario: AC5 A payload without codec metadata is refused
    Given a SIT test wrote the history of "case-RW-2026-000305" with the codec off, so its payload carries no codec metadata
    When U-88 decodes that payload with an active grant
    Then the response is 422 and no payload is returned
    Then one AC-DENY entry records the payload index and the reason
    Then an incident reaches RW-SECADM and RW-PLATADM
    Then the codec does not guess a key and does not fall back to a clear read

  Scenario: AC6 A failed audit write blocks the administrative call
    Given the decision log store is unavailable at 13:00 on 16 November 2026
    When U-70 terminates "case-RW-2026-000306" from the Web UI
    Then the authorizer receives 503 from the audit writer and denies the call with PERMISSION_DENIED
    Then "case-RW-2026-000306" stays RUNNING and no TERMINATE entry exists
    Then the Web UI shows that the action was not taken because the decision could not be recorded
    Then an incident reaches RW-PLATADM

  Scenario: AC7 The reconciliation finds an action with no entry
    Given the frontend audit log holds a signal on "case-RW-2026-000307" at 13:02 with no decision_log_entry
    When TemporalAdminAuditListener runs at 02:00 on 17 November 2026
    Then it reports one gap with the workflow ID, the operation and the time
    Then an incident reaches RW-SECADM and RW-PLATADM
    Then the incident stays open until the security administrator records the finding in the bank IAM
    Then the job writes no entry of its own
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Decode is allowed only for RW-SECADM with an ACTIVE break-glass grant for area PLATFORM_ADMINISTRATION and right R; there is no standing decode right | RWB-E1-039; REQ-DRI-001 |
| BR2 | The codec server is the only path to a clear payload; the Web UI names it per environment, and no key or codec runs on a workstation | D-RCV-36 T1 |
| BR3 | The AC-READ entry is written before the clear payload is returned; a failed write returns no payload | REQ-DRI-005 |
| BR4 | Terminate, reset and signal are recorded by the Temporal authorizer before the frontend executes them; a failed write denies the call and leaves the workflow unchanged | REQ-DRI-005 |
| BR5 | Every entry carries the operation, namespace, workflow ID, run ID, actor, reason and, where one applies, the grant and the incident | REQ-DRI-001 |
| BR6 | A decode is recorded with AC-READ and an administrative call with PLATFORM_ADMIN; no entry carries a payload or a personal data field | LOV-DECISION; NFR-045 |
| BR7 | The codec resolves the key version from the payload metadata; a rotation keeps every earlier version enabled for the retention and the archive period, so old histories stay decodable | D-RCV-36 T1 |
| BR8 | A payload without codec metadata is refused and raises an incident; the codec never guesses a key and never returns a payload it cannot attribute to a version | NFR-045 |
| BR9 | The daily reconciliation compares the frontend audit log with decision_log_entry and raises an incident on any gap; it never writes a missing entry | REQ-DRI-001 |
| BR10 | RW-AUDIT reads the entries through GET /admin/access-log and has no decode right | RWB-E1-039 |

### 9. State transitions

None for a case. A break-glass grant and a workflow execution change state, and the story records the change.

| From | Event | Condition | To |
|---|---|---|---|
| ACTIVE (grant) | End time reached, or the grant is revoked in the bank IAM | - | ENDED |
| RUNNING (workflow) | TerminateWorkflowExecution | The PLATFORM_ADMIN entry is committed | TERMINATED |
| RUNNING (workflow) | ResetWorkflowExecution | The PLATFORM_ADMIN entry is committed | The current run closes and a new run starts at the reset point |
| RUNNING (workflow) | SignalWorkflowExecution | The PLATFORM_ADMIN entry is committed | RUNNING, with the signal handled |
| RUNNING (workflow) | TerminateWorkflowExecution with the decision log unavailable | The entry cannot be written | RUNNING, unchanged; the call is denied |

A refusal writes AC-DENY and changes no workflow state.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SECADM | Requests break-glass in the bank IAM; decodes a payload under an ACTIVE grant; reads the access log (Platform administration, R) |
| RW-PLATADM | Terminates, resets and signals a workflow (Platform administration, U); reads the entries; receives the reconciliation incident |
| RW-AUDIT | Reads the AC-READ, AC-DENY and PLATFORM_ADMIN entries; holds no decode right (Platform administration and Decision log, R) |
| RW-TRIBE | Maintains the authorizer plugin configuration and the key rotation run book; may not decode |
| RW-CASEOWN and the other case roles | No decode right and no administrative call on a workflow |
| SY-CASEWF | Runs the codec server and the audit writer; connects to the frontend with its certificate (Decision log C) |
| SY-RULES | No part in this story; a call to the audit endpoint with its certificate is refused |
| No delegation of authority level applies | A decode or an administrative call is not a credit decision |

Separation of duty: the security administrator who decodes is not the author of the case decision the payload supports, and no person reviews their own break-glass use (RWB-E1-039).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (one entry per decode, refusal and administrative call) |
| DF-DEC-002 | decision_log_entry | case_id | Write; empty for an access event, as RWB-E1-039 sets it, with the workflow ID in the actions field |
| DF-DEC-003 | decision_log_entry | decision_code | Write, read |
| DF-DEC-014 | decision_log_entry | actions | Write (operation, workflow ID, run ID, payload count, grant, incident) |
| DF-DEC-016 | decision_log_entry | decided_at | Write, read |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write, read |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write, read |

No field is added. The PLATFORM_ADMIN value is a LOV-DECISION data row loaded through RWB-E1-043 and recorded in the additions file. No payload, no history event and no clear personal data field is written to the decision log. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**No Workbench API endpoint is added.** The codec server and the authorizer audit writer are internal Temporal services; they are not part of the Workbench API Specification v4.

**Codec server: POST /decode and POST /encode (Temporal codec server protocol)**

| Item | Value |
|---|---|
| Service | The codec server of the recovery module, called by the Temporal Web UI over mTLS at its own service URL |
| Request | namespace, workflowId, runId, requestId, payloads: an array of { metadata: { encoding, keyVersion }, data: base64 } |
| Response 200 | payloads: an array of { metadata, data: base64 } in the same order, and entryId |
| Errors | 401 no session; 403 role, grant or area (MSG-P4-002); 413 more than 100 payloads or 1 MB; 422 a payload without codec metadata or a key version that is not enabled; 503 Key Vault unavailable or the entry could not be written (no payload returned) |
| Authorization | Platform administration, right R, plus an ACTIVE break-glass grant for area PLATFORM_ADMINISTRATION |
| Idempotency | requestId from the Web UI; a repeat with the same requestId returns the same payloads and entryId and writes no second entry |

**Authorizer audit: TemporalAdminAuditWriter (internal mTLS call, no HTTP path)**

| Item | Value |
|---|---|
| Caller | The Temporal frontend authorizer plugin, configured in deploy/temporal/plugins/ |
| Request | operation (TERMINATE, RESET or SIGNAL), namespace, workflowId, runId, actorRef, grantId (nullable), reason, requestId |
| Response | entryId, read as 201 by the plugin |
| Failure | Any non-201 response denies the call with PERMISSION_DENIED; the workflow is unchanged |
| Authorization | mTLS client certificate of the Temporal frontend and the network policy of the frontend pods only |
| Idempotency | requestId from the frontend request; one entry per operation on one run |

**Temporal frontend** (gRPC over mTLS, port 7233): TerminateWorkflowExecution, ResetWorkflowExecution and SignalWorkflowExecution pass through the authorizer plugin, which calls TemporalAdminAuditWriter before allowing the call. A decode is not a Temporal API call; it is the codec server path above.

**GET /api/recovery/v1/admin/access-log** (existing, RWB-E1-039): reads the entries with event codes AC-READ, AC-DENY and PLATFORM_ADMIN. Authorization and errors are unchanged.

**Published interfaces called**

```java
// P7 decision log
DecisionLogRef DecisionLogApi.write(DecisionLogRequest request) throws DecisionLogWriteException;
```

The active grant is read through the published break-glass interface of RWB-E1-039; this story adds no method to it.

### 13. Solution plan

**Package.** The codec server, the grant check, the audit writer and the reconciliation in `recovery/accessadmin/temporal` (Java package `recovery.accessadmin.temporal`); the authorizer plugin configuration in `deploy/temporal/plugins/`; the key rotation run book in `docs/operations/runbooks/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CodecServerController | Controller | POST /decode on the codec server with the access check and the response after the entry (BR2, BR3) |
| BreakGlassGrantChecker | Service | Reads the ACTIVE grant and checks role, area and right (BR1) |
| PayloadGuard | Service | Payload count and size limits; codec metadata and key version check (BR8) |
| CodecKeyResolver | Service | Resolves the key version from the metadata and unwraps it in Key Vault (BR7) |
| TemporalAdminAuditWriter | Service | Builds and writes the AC-READ, AC-DENY and PLATFORM_ADMIN entries through DecisionLogApi (BR5, BR6) |
| TemporalAuthorizerPlugin | Configuration | The Temporal frontend Authorizer and ClaimMapper: calls TemporalAdminAuditWriter and denies on any non-201 response (BR4) |
| TemporalAdminAuditReceiver | Service | Receives the authorizer audit record over mTLS and writes it through TemporalAdminAuditWriter (BR4) |
| TemporalAdminAuditListener | Job | Daily reconciliation of the frontend audit log against decision_log_entry (BR9) |
| KeyRotationRunBook | Document | The rotation steps, the version list and the version retention rule (BR7) |

**Database.** No migration. The entries go to decision_log_entry through the existing writer in the caller's transaction. LOV-DECISION gains PLATFORM_ADMIN as a data row through RWB-E1-043; no table and no column is added.

**Configuration and reference data**

- Codec endpoint URL per environment in the Web UI; the codec server is reachable only from the Web UI ingress and the internal network.
- Limits: 100 payloads and 1 MB per request; the reconciliation runs daily at 02:00.
- Key versions: every version named by a history inside the retention (30 days, assumed) or the archive of RWB-E2-039 stays enabled.
- Feature flag rwb.p3.temporal through RWB-E1-047.
- No business parameter and no reference table beyond the LOV value in this story.

**Build steps**

1. Add the PLATFORM_ADMIN LOV value through the versioned reference load and confirm the decision log writer accepts it as a system event.
2. Build PayloadGuard and CodecKeyResolver with the version from the metadata; test AC4 with versions 1 and 2 and a rotation to 3.
3. Build BreakGlassGrantChecker and the codec endpoint with the write-before-return order; tests AC1, AC3 and AC5.
4. Build TemporalAdminAuditWriter and its mTLS receiver; test AC2 for the four operations.
5. Configure the authorizer plugin to call the writer and deny on 503; test AC6 with the decision log stopped.
6. Build TemporalAdminAuditListener and its incident; test AC7 with a planted frontend audit entry.
7. Run the two access tests, the key rotation drill in SIT, and record the version list in the release evidence.

**Feature flag.** `rwb.p3.temporal`. Off: the codec endpoint returns 404, the authorizer plugin is not configured and the reconciliation does not run; the cluster and the Web UI are unchanged.

**Done when.** The tests in section 16 pass, the rotation drill decodes a history written under an earlier key version, the reconciliation finds no gap over seven days, and the access log shows every decode with its grant and incident.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The role is not RW-SECADM, the grant is missing, ended or for another area, or the caller is not SY-CASEWF on the internal endpoint | You cannot {action} here. Your role does not include it. |

A 401 returns the standard no-session text. A 422 names the payload index and the missing codec metadata, but never the payload. A 503 says the action was not taken because the decision could not be recorded. Neither case adds a message ID. MSG-P4-002 exists and is reused unchanged, with {action} set to "decode this workflow payload" or "record this workflow action".

### 15. Screens and states

No new Workbench screen. The decode result appears in the payload panel of the Temporal Web UI, which shows the states encoded, decoding and decoded for a user with a grant, and refused with MSG-P4-002 for every other user. The entries appear on the access log read of RWB-E1-039 and on SCR-38 Decision log query (RWB-E2-005) with the operation in the actions field. SCR-43 Roles and access in Epic 8 shows the grant rule; this story adds no panel to it.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-038-01 | AC1, BR1, BR3 | System | U-88 RW-SECADM, grant BG-2026-0042 ending 12:00; decode at 11:40 and 12:05 |
| TC-E2-038-02 | AC2, BR4, BR5, BR6 | System | One decode, one terminate, one reset and one signal |
| TC-E2-038-03 | AC3, BR1, BR10 | Access | RW-AUDIT and RW-CASEOWN call the decode endpoint; refused with MSG-P4-002 |
| TC-E2-038-04 | AC4, BR7 | System | Histories under key versions 1 and 2; rotation to version 3 |
| TC-E2-038-05 | AC5, BR8 | System | Payload without codec metadata |
| TC-E2-038-06 | AC6, BR4 | System | Decision log stopped; terminate attempted on case-RW-2026-000306 |
| TC-E2-038-07 | AC7, BR9 | Operational | Planted frontend audit entry; reconciliation at 02:00 |
| TC-E2-038-08 | Operational | Operational | Key rotation drill in SIT: rotate to version 3, decode a version 1 history |
| TC-E2-038-09 | Access | Access | SY-RULES calls the codec server /decode with its own certificate; refused with MSG-P4-002 and no entry |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the payload limits, the reconciliation time, the key version list and the refusal texts are configuration.
- No personal data in logs, tests, workflow history or prompts: the test payloads are synthetic, and no payload or clear field is written to the decision log or a log line.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: this story reads no case and no ACE table.
- Decode is never a standing right: no grant, no clear payload, and every decode names its grant and incident.
- No entry, no action: a terminate, reset or signal the authorizer cannot record is denied, not retried after the fact.
- The codec never guesses a key version and never falls back to a clear read.
- No key version is disabled while a history inside the retention or the archive names it.
- The reconciliation never writes a missing entry: it reports the gap and leaves the record to the security administrator.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | One record per decision, with the seven field groups | Epic 2, 3.4; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-038-01, TC-E2-038-02, TC-E2-038-05, TC-E2-038-07 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Epic 2, 3.4; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-038-02, TC-E2-038-06 |

### 19. Out of scope

- The Temporal cluster, mTLS, Web UI sign-in and platform roles (RWB-E1-070).
- The codec itself, the worker and the smoke workflow (RWB-E1-071).
- The break-glass request, approval, review and access log writer (RWB-E1-039).
- Alerts, the stuck scanner and the workflow dashboard (RWB-E2-037).
- Backup, failover, upgrade and archive (RWB-E2-039).
- The replay gate and build ID rollout (RWB-E2-040).
- A Workbench screen for workflow payloads or for the admin audit (Epic 8, SCR-43 Roles and access).
- Key Vault provisioning, key escrow and the bank key management standard (SCB IT platform).
---

## RWB-E2-039 Temporal resilience: backup, failover, upgrade and archive

| Item | Value |
|---|---|
| Story key | RWB-E2-039 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None (platform enabler) |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, section 6.4 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-070, RWB-E2-037 |
| Status | Ready for build |

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the Temporal databases backed up, the zone failover and a minor upgrade tested, and closed histories archived before retention removes them**, so that **the engine meets the ACE availability targets and an audit can still read a closed workflow after its history has left Temporal**.

### 2. Business rationale

From Epic 3 every live case waits inside a Temporal workflow, so the engine becomes part of the case record: a lost history is a lost case step, and an engine that cannot be restored inside the ACE recovery time objective stops the recovery desk. RWB-E1-070 installs the cluster and RWB-E2-037 alerts when a workflow stops, but neither proves that the data comes back, that a zone loss is survived, that a minor upgrade keeps a running workflow, or that a closed history survives the 30-day retention.

This story adds the four proofs and the one archive: a point-in-time restore of both Temporal databases to one timestamp, a zone failover that completes the smoke workflow, a one-minor upgrade with no lost workflow, and a daily export of closed histories to write-once Blob storage before retention removes them. It meets REQ-DRI-007 (a named owner and a tested way back for every failure). The measure is that every drill passes in SIT inside the ACE recovery time objective, that a history closed 31 days ago is readable in the archive, and that no archived file holds clear personal data.

### 3. Preconditions

- RWB-E1-070 is done: the databases temporal and temporal_visibility on the zone-redundant PostgreSQL flexible server, the namespace rwb-recovery, mTLS, the metrics scrape and the platform run book exist.
- RWB-E2-037 is done: the failed, stuck and latency alerts, the dashboard and their run books exist, so a drill is observed like a live incident.
- The PostgreSQL flexible server has automated backups and point-in-time restore enabled with a window of at least 35 days (assumed); the platform administrator holds the restore right through the operations group.
- The Blob container rwb-temporal-archive exists with a write-once policy for the archive period, and RW-AUDIT holds Storage Blob Data Reader on it.
- Retention is 30 days (temporal.retention.days = 30; assumed, DL26) and the archive lead time is 7 days (assumed), so a history is exported before retention removes it.
- The SIT namespace holds the smoke workflow of RWB-E1-071 and synthetic histories for the drill; no production data is used.
- The approved server version is recorded in Environment and Deployment Design v4, and the next minor version is available to SIT.
- The Quartz scheduler is available for the daily archive job (D-RCV-36 T2); no Temporal Schedule is created.

### 4. Flow

1. Backup policy: automated backups and point-in-time restore run on both databases, and the window, the schedule and the owner are recorded as configuration.
2. Restore drill: note the workflows running at the restore point; restore temporal and temporal_visibility to one timestamp on a new server; repoint the frontend; start the workers; compare the workflow count and the last event of each workflow; record the elapsed time against the ACE recovery time objective.
3. Zone failover drill: fail the primary availability zone of the flexible server; the server fails over; the frontend reconnects; start and complete the smoke workflow; compare the running count before and after.
4. Upgrade: read the upgrade run book; drain the workers; upgrade the server by one minor version with Helm; run the schema tool; start the workers with the matching SDK; run the smoke workflow; sample the running workflows; record the pinned version in Environment and Deployment Design v4.
5. Archive job (Quartz, daily at 02:00): lists CLOSED workflows whose close time is older than the archive lead time, exports each history through the Temporal API, checks the payloads, writes the file and the manifest row to Blob, reads the file back and compares the checksum.
6. Archive job: marks a written row VERIFIED on a matching checksum; a failed write, a failed read-back or a failed payload check marks it FAILED, retries up to three times in the run, and raises an incident; retention is left to remove the visibility record.
7. RW-AUDIT: lists the archive and opens a verified history file; the payloads stay encrypted and are decoded only through RWB-E2-038.
8. Platform administrator: records each drill and the archive totals as release evidence; a failed drill blocks the release.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A drill restores temporal and temporal_visibility to different timestamps | The consistency check reports workflows in visibility with no history; no worker starts against the pair; the drill is recorded as failed with both timestamps | None (drill evidence) | AC6 |
| X2 | The archive read-back checksum differs, or the Blob write fails | The row is marked FAILED and not VERIFIED; the job retries the export up to three times in the run; an incident reaches RW-PLATADM and RW-AUDIT | None (incident only) | AC7 |
| X3 | An upgrade proposes a target two minor versions later | The version step check refuses the upgrade before any pod is replaced and names the missing intermediate version | None (pipeline failure) | AC8 |
| X4 | An exported history holds a payload that is not codec-encrypted | The payload check finds the pattern, the file is not written, the row is FAILED and an incident reaches RW-SECADM and RW-PLATADM | None (incident only) | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the cluster and databases of RWB-E1-070 and the alerts of RWB-E2-037; it adds the drills, the upgrade check and the archive job |
| Negotiable | The backup window, the archive lead time, the container, the immutability period and the retry count are configuration; the one-timestamp restore and the write-once archive are fixed |
| Valuable | The engine comes back after a zone loss, a restore or an upgrade, and a closed history outlives the retention |
| Estimable | One backup policy, three drill run books, one version check and one archive job |
| Small | Fits two weeks with its drills |
| Testable | Each criterion in section 7 is one test or one recorded drill in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Temporal resilience: backup, failover, upgrade and archive

  Background:
    Given the Temporal cluster of RWB-E1-070 runs in SIT with databases temporal and temporal_visibility on the zone-redundant PostgreSQL flexible server
    Given the worker of RWB-E1-071 polls rwb-platform and runs the smoke workflow
    Given retention is 30 days and the archive lead time is 7 days

  Scenario: AC1 A point-in-time restore brings the workflows back
    Given workflow "case-RW-2026-000201" started at 09:40 on 16 November 2026 and completed activity "ReadAceSnapshot" at 09:42
    Given it waits on a timer that fires at 10:00 and was RUNNING at the restore point 09:55
    Given workflow "case-RW-2026-000202" started at 10:00, after the restore point
    When the platform administrator restores temporal and temporal_visibility to 09:55 on a new server in SIT
    Then the namespace rwb-recovery is REGISTERED and the frontend points at the new server
    Then the workers reconnect and "case-RW-2026-000201" continues when its timer fires
    Then its history holds one WorkflowExecutionStarted, one TimerStarted, one ActivityTaskCompleted and one TimerFired
    Then activity "ReadAceSnapshot" wrote one row under its idempotency key and did not run twice
    Then "case-RW-2026-000202" is absent and the run book says the caller starts it again, inside the recovery point objective
    Then the drill records the elapsed time against the ACE recovery time objective (NFR-023)

  Scenario: AC2 A zone failover completes the smoke workflow
    Given 12 workflows are RUNNING in rwb-recovery at 14:00 on 16 November 2026
    When the primary availability zone of the PostgreSQL flexible server fails at 14:00 and the server fails over
    Then the frontend reconnects without a manual change and the namespace is REGISTERED
    Then the smoke workflow "platform-smoke-20261116" starts at 14:06 and ends COMPLETED
    Then the count of RUNNING workflows at 14:10 is 12
    Then no history holds a gap or a duplicate event
    Then the drill records the failover time against the ACE recovery time objective (NFR-023)

  Scenario: AC3 A one-minor upgrade loses no workflow
    Given SIT runs the approved server version and the next minor version is available
    Given 5 workflows are RUNNING on task queue rwb-platform
    When the run book is followed: the workers are drained, the server is upgraded with Helm, the schema tool runs, and the workers start with the matching SDK
    Then the 5 workflows are RUNNING or COMPLETED after the upgrade with the same workflow ID and run ID
    Then no history holds a gap or a duplicate event
    Then the smoke workflow completes after the upgrade
    Then Environment and Deployment Design v4 records the next minor version as the pinned version

  Scenario: AC4 A closed history is archived and readable by RW-AUDIT
    Given workflow "case-RW-2026-000101" closed COMPLETED on 16 October 2026
    When the archive job runs at 02:00 on 23 October 2026
    Then the history is written to Blob at dt=2026-10-23/case-RW-2026-000101/<runId>.json.gz
    Then the manifest row names the workflow ID, run ID, workflow type, close time, archive time, path and checksum, and its status is VERIFIED
    Then the visibility record is left to the 30-day retention and is gone on 15 November 2026
    When RW-AUDIT lists the archive on 16 November 2026
    Then the file is listed and readable and its checksum matches the manifest

  Scenario: AC5 The archive holds no clear personal data
    Given the archived history of "case-RW-2026-000101" holds a salary slip payload with the synthetic national ID "1101700203456"
    When RW-AUDIT opens the file
    Then the payload is binary ciphertext with codec metadata naming key version 2
    Then the string "1101700203456" appears nowhere in the file, the manifest or the archive log
    Then the manifest holds the workflow ID, type and timestamps and no personal data field
    Then a clear read needs the codec server of RWB-E2-038 with an open break-glass grant

  Scenario: AC6 The two databases are restored to one timestamp
    Given a drill restores temporal to 09:55 and temporal_visibility to 10:05
    When the frontend starts against the restored pair
    Then the consistency check reports workflows in visibility with no history in the history store
    Then no worker is started against the pair
    Then the run book says to restore both databases to one timestamp and repeat the drill
    Then the drill is recorded as failed with both timestamps

  Scenario: AC7 The archive verifies every file
    Given the archive job writes the history of "case-RW-2026-000102" and the read-back checksum differs
    When verification runs
    Then the manifest row is FAILED with the reason and the file is not marked VERIFIED
    Then the job retries the export up to three times in the same run
    Then an incident reaches RW-PLATADM and RW-AUDIT
    Then the next run re-exports the history and the row becomes VERIFIED

  Scenario: AC8 An upgrade skips no minor version
    Given SIT runs the approved server version and the proposed target is two minor versions later
    When the version step check runs in the pipeline and the run book is read
    Then the upgrade is refused before any pod is replaced
    Then the error names the missing intermediate version
    Then the approved path is one minor version, verify, then the next

  Scenario: AC9 A history with a clear payload is not archived
    Given a SIT test workflow wrote its payload with the codec off, so its history holds the national ID "1101700203456" in clear text
    When the archive job exports that history
    Then the payload check finds the pattern and the file is not written
    Then the manifest row is FAILED and an incident reaches RW-SECADM and RW-PLATADM
    Then the test workflow is deleted and the test profile is corrected before the next run
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Automated backups and point-in-time restore run on both Temporal databases, and a restore goes to a new server at one timestamp for both databases, never in place on the live server | D-RCV-36 T1; AC1, AC6 |
| BR2 | A restore and a failover are measured against the ACE recovery point objective and recovery time objective; the values are DL11 and are not set in code | NFR-022, NFR-023 |
| BR3 | The server is zone redundant, and a zone failover is tested in SIT at each release with the smoke workflow as the proof | AC2 |
| BR4 | An upgrade moves one minor version at a time: workers drained, server upgraded, schema tool run, workers started with the matching SDK, version pinned and recorded in Environment and Deployment Design v4 | AC3, AC8 |
| BR5 | A closed history is exported before retention removes it; the archive lead time is 7 days against a 30-day retention, and both are parameters (assumed) | AC4 |
| BR6 | The archive is write-once for its period, checksummed and indexed by one manifest row with its status | AC4, AC7 |
| BR7 | The archive holds codec-encrypted payloads only; a history that fails the payload check is not written and raises an incident to RW-SECADM | NFR-045; AC9 |
| BR8 | RW-AUDIT lists and reads the archive; decode stays with RWB-E2-038 and its break-glass grant | RWB-E1-039; AC5 |
| BR9 | A drill result is release evidence with its timestamps and counts, and a failed drill blocks the release | REQ-DRI-007 |
| BR10 | The backup window, the archive lead time, the container, the immutability period, the retry count and the version are configuration, never code | REQ-DRI-007 |

### 9. State transitions

None for a case. The engine, a workflow execution and an archive row change state.

| From | Event | Condition | To |
|---|---|---|---|
| RUNNING (server) | Zone failover | - | RUNNING on the secondary zone |
| RUNNING (server) | Minor upgrade | Workers drained | RUNNING at the next minor version |
| RUNNING (workflow) | Restore to an earlier point | The workflow started before the point | RUNNING at the restored point |
| CLOSED (workflow) | Archive export | 7 days after close | Manifest row WRITTEN |
| WRITTEN | Verification | The checksum matches | VERIFIED |
| WRITTEN | Verification | The checksum differs or the payload check fails | FAILED, and retried |
| CLOSED (workflow) | Retention 30 days | Archived or not | Removed from visible history and visibility |
| VERIFIED | Archive retention ends | The immutability period has passed | Disposed by the archive retention decision |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM | Runs the backup, restore, failover and upgrade steps; runs the archive job and reads its result (Platform administration, U) |
| RW-AUDIT | Lists and reads the archive and the manifest (Platform administration and Decision log, R) |
| RW-SECADM | Receives a payload-check incident and decodes an archived history through RWB-E2-038 only |
| RW-TRIBE | Maintains the backup policy, the drill scripts and the run books through the change process; may not restore PROD |
| SY-CASEWF | Runs the archive job and writes the Blob files and manifest rows |
| SY-RULES | No part in this story |
| The operations group | Holds the restore right on the PostgreSQL flexible server and the Blob data roles; the platform administrator acts through it |
| No delegation of authority level applies | A restore or an upgrade is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| None (platform enabler) | None in the recovery schema | None | None |

Backup and restore state lives in the PostgreSQL flexible server and its backup store, workflow and timer state lives in Temporal persistence and visibility (RWB-E1-070), and the archived histories and the manifest live in Blob storage, container rwb-temporal-archive. The archive job's schedule, owner and run book path live in job_catalog through RWB-E1-056. No DF-REF, DF-CAS or DF-DEC field is added or changed, the Physical Schema v6 is unchanged, and Temporal's own tables are not in the Physical Schema.

### 12. Contract

No Workbench endpoint. This story adds no path under /api/recovery/v1. The interfaces are the database backup service, the Temporal frontend, Blob storage and the deployment tooling.

| Interface | Method | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| PostgreSQL flexible server backup and restore | Azure control plane: restore to a new server at a point in time | Resource group, source server, target server, one timestamp for both databases | New server with both databases at the timestamp | Restore outside the window; target name in use; quota | Operations group right on the resource group; no Workbench role | A restore to the same timestamp gives the same result; the target server name is the key |
| Restore consistency check | Read-only comparison through the Temporal frontend | namespace rwb-recovery, visibility records and history presence | Count of workflows in visibility with no history, and the reverse | PERMISSION_DENIED; UNAVAILABLE | Client certificate of SY-CASEWF | Read only |
| Temporal frontend | gRPC over mTLS, port 7233: DescribeNamespace, ListWorkflowExecutions, GetWorkflowExecutionHistory | namespace rwb-recovery, workflow ID, run ID | Namespace, workflow and history summary | TLS handshake failure; NOT_FOUND; UNAVAILABLE | Client certificate of SY-CASEWF with the namespace claim | Read only |
| Blob storage (archive) | HTTPS PUT, GET and LIST on container rwb-temporal-archive | path dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz, file, manifest row | 201 on write; 200 on read; manifest rows on list | 403 role; 409 or 412 immutability; 404 no such file | SY-CASEWF writes; RW-AUDIT reads with Storage Blob Data Reader | The workflow ID and run ID path is the key; a repeated write is refused while the immutability policy holds the file |
| Helm and Temporal schema tool | Deployment pipeline against the SIT and UAT clusters | Chart version, image tag, schema tool at the target version | Release at the target version | Schema version mismatch; pod not ready | RW-PLATADM through the pipeline; no PROD step without the release approval | A second run at the same version changes nothing |

The archive job never writes to the ACE database, and the restore never writes to the live server. RW-AUDIT reads no Temporal database.

### 13. Solution plan

**Package.** No Java business package. The backup policy and the drill scripts live in `deploy/temporal/resilience/`; the archive job lives in `recovery/integration/ops/temporal`; the run books live in `docs/operations/runbooks/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemporalBackupPolicy | Configuration as code | The backup schedule, the point-in-time window and the owner on the flexible server (BR1) |
| RestoreRunBook | Document | The one-timestamp restore steps, the frontend repoint, the worker start and the count comparison |
| RestoreConsistencyCheck | Service | Compares visibility records with history presence and refuses a mismatched pair (AC6) |
| ZoneFailoverDrill | Script | Fails the primary zone, waits for the server, starts the smoke workflow and records the time (BR3) |
| UpgradeRunBook | Document | Drain, upgrade, schema tool, worker start, verification and the pinned version record (BR4) |
| VersionStepCheck | Pipeline check | Refuses a target more than one minor version ahead (AC8) |
| HistoryArchiveJob | Job | Quartz, daily at 02:00: list, export, check, write, verify and raise the incident (BR5 to BR7) |
| ArchivePayloadCheck | Service | Refuses a history that holds a payload without codec metadata or a clear personal data pattern (BR7) |
| ArchiveManifestStore | Repository | Writes and reads the manifest rows and their status in Blob |
| ArchiveReadRole | Configuration | The Storage Blob Data Reader assignment for RW-AUDIT on the archive container (BR8) |

**Database.** No migration and no new table. The archive job gets one job_catalog row through RWB-E1-056 as a data change. The archive and the manifest live in Blob storage.

**Configuration and reference data**

- temporal.retention.days = 30 (assumed, DL26) and the archive lead time of 7 days (assumed), through RWB-E1-042.
- The backup schedule and the point-in-time window on the flexible server.
- The container rwb-temporal-archive, its write-once period and the retry count of three.
- The approved server version and the next minor version, recorded in Environment and Deployment Design v4.
- Feature flag rwb.p3.temporal through RWB-E1-047; with it off, no workflow runs and the archive job finds nothing to export.

**Build steps**

1. Write the backup policy and prove the point-in-time window on the SIT server.
2. Build RestoreConsistencyCheck and the restore run book; drill AC1 and AC6.
3. Build the zone failover drill and run AC2 in SIT with the smoke workflow.
4. Write the upgrade run book and the version step check; drill AC3 and AC8.
5. Build HistoryArchiveJob and ArchivePayloadCheck; test AC4, AC5, AC7 and AC9 on synthetic histories.
6. Create the container, the write-once policy and the RW-AUDIT read role; prove a listed and readable file.
7. Run the full drill set in SIT and record every result as release evidence with its timestamps and counts.

**Feature flag.** `rwb.p3.temporal`. Off: no workflow runs, the archive job finds nothing, and the drills are not run in that environment. The cluster, the backups and the archive container stay in place.

**Done when.** The restore, failover and upgrade drills pass in SIT, a history closed 31 days ago is readable in the archive, the archive passes the payload check, and the drill evidence is in the release record.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-037 | A drill leaves a workflow failed or not moving, as any other workflow failure | Workflow {workflowId} has failed or has not moved for {hours} hours. |

This story adds no message. A failed drill is recorded in the release evidence and raised as an incident to RW-PLATADM, and a failed archive row is raised as an incident to RW-PLATADM and RW-AUDIT. The workflow alerts are those of RWB-E2-037 and reuse MSG-P3-037 unchanged.

### 15. Screens and states

No Workbench screen in this story. The operational views are the Temporal Web UI, the Grafana dashboard of RWB-E2-037 and the Azure portal listing of the archive container with the manifest. The manifest row has the states WRITTEN, VERIFIED and FAILED; a drill has the states Planned, Passed and Failed with its timestamps. The Workbench job monitor of RWB-E1-056 shows the archive job's last run, status and duration. The platform screens of Epic 8 do not repeat this data.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-039-01 | AC1, BR1, BR2 | Operational | Restore point 09:55; case-RW-2026-000201 started 09:40; case-RW-2026-000202 started 10:00 |
| TC-E2-039-02 | AC2, BR3 | Operational | Zone failover at 14:00; 12 running workflows; smoke workflow started 14:06 |
| TC-E2-039-03 | AC3, BR4 | Operational | One-minor upgrade in SIT; 5 workflows running on rwb-platform |
| TC-E2-039-04 | AC4, BR5, BR6 | System | History closed 16 October 2026; export on 23 October 2026; read on 16 November 2026 |
| TC-E2-039-05 | AC5, BR7, BR8 | System | Archived salary slip payload with national ID 1101700203456 |
| TC-E2-039-06 | AC6, BR1 | Operational | Restore temporal to 09:55 and temporal_visibility to 10:05 |
| TC-E2-039-07 | AC7, BR6 | System | Read-back checksum changed; three retries |
| TC-E2-039-08 | AC8, BR4 | System | Target two minor versions ahead of the approved version |
| TC-E2-039-09 | AC9, BR7 | System | History written with the codec off; clear national ID in the payload |
| TC-E2-039-10 | Operational | Operational | Archive reconciliation: every closed workflow older than the retention has a VERIFIED row |
| TC-E2-039-11 | Operational | Operational | Restore drill evidence recorded with the ACE recovery time objective measured |

The drills are run by the platform administrator and the operations group in SIT and recorded in the release evidence; there is no Workbench endpoint and no Access test in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the backup window, the retention, the archive lead time, the container and the retry count are configuration.
- No personal data in logs, tests, workflow history or prompts: the archive holds codec-encrypted payloads only, and the drill data is synthetic.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: this story reads no case and no ACE table.
- A restore is never made in place on the live server, and both databases are restored to one timestamp.
- No upgrade by more than one minor version, and no upgrade without draining the workers first.
- No archived file without a manifest row and a matching checksum; no file with a clear payload is written.
- Retention is never extended or shortened by this story; the archive runs before retention and leaves the deletion to Temporal.
- No drill result is recorded as passed without its timestamps and counts.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner and has a tested way back | Epic 2, 3.2; Program, 6.4 | None (platform enabler) | All recovery processes | R-UNI-40 | TC-E2-039-01, TC-E2-039-02, TC-E2-039-03, TC-E2-039-04, TC-E2-039-06, TC-E2-039-07, TC-E2-039-08, TC-E2-039-09, TC-E2-039-10 |

### 19. Out of scope

- The Temporal cluster, namespace, mTLS and Web UI (RWB-E1-070).
- The worker, codec and smoke workflow (RWB-E1-071).
- Alerts, the stuck scanner and the dashboard (RWB-E2-037).
- The codec server, decode and the administrative audit (RWB-E2-038).
- The replay gate, history export for tests and build ID rollout (RWB-E2-040).
- Disaster recovery of the ACE AKS cluster itself and the region pair, which follow the ACE platform plan (SCB IT).
- The retention period itself, which is DL26, and the disposal decision after the archive period.
- Case-level restoration of a single case and any manual replay of a case workflow (Epic 3).
---

## RWB-E2-040 Workflow versioning and replay test gate

| Item | Value |
|---|---|
| Story key | RWB-E2-040 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None (platform enabler) |
| Requirement IDs | REQ-DRI-005 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, section 5.7 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1, T7); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-071 |
| Status | Ready for build |

### 1. Story

As a **developer**, I want **every workflow change replayed against recorded histories in the pipeline, and workers rolled out by build ID**, so that **a change never breaks a case already in flight**.

### 2. Business rationale

Temporal workflow code must replay: a worker that picks up a running workflow re-executes its code against the recorded history, and any change in the order of commands makes the replay fail with a non-determinism error. The workflow then stops, the case waits, and the failure appears in production rather than in the pipeline. Epic 3 will change case workflows release after release while cases are open, so the gate that catches this must exist before the first case workflow is written, not after the first incident.

This story adds gate 10 to the pipeline: a nightly export of SIT histories, a replay of every affected history against the branch build, time-skipping tests for timers, and a build ID rollout that lets running workflows finish on the build they started on. It meets REQ-DRI-005: a replay that reaches the same decisions proves that the recorded decision path still matches the code, and a change that would make a recorded decision unreproducible is refused before it reaches a case. The measure is that no workflow change merges without a gate 10 result and that no build is retired with a running workflow.

### 3. Preconditions

- RWB-E1-071 is done: the worker, WorkflowGateway, WorkerBuildIdProvider, the smoke workflow and the build ID format `<git-sha>-<build-number>` exist, and the worker polls rwb-platform.
- The Temporal Java SDK test kit, WorkflowReplayer and TestWorkflowEnvironment, is on the test classpath at the pinned SDK version and in test scope only.
- The SIT namespace rwb-recovery holds histories for the workflow types under test: PlatformSmokeWorkflow and the test-only CaseHoldWorkflow, and from Epic 3 CaseWorkflow.
- The Blob container rwb-temporal-replay exists with a 90-day retention, and the nightly export job runs in SIT only.
- The pipeline runs the nine checks of Recovery Workbench Engineering Practices, and the merge checklist and pull request template are held in the repository.
- No production history is exported and no production data is used in a test or a prompt (NFR-045).
- Feature flag rwb.p3.temporal is on in SIT; the gate itself has no flag.

### 4. Flow

1. HistoryExportJob (Quartz, nightly at 01:00, SIT only): exports the last 200 closed histories per workflow type through the Temporal API, checks each payload, writes the file and the index row to Blob, and records the export time.
2. Developer: changes a workflow class, an activity signature or the order of commands, and raises a pull request.
3. Pipeline gate 10 (ReplayTestGate): reads the index for the affected workflow types and replays every history against the branch build with WorkflowReplayer.
4. ReplayTestGate: on a non-determinism error, reports the workflow type, history ID, event ID and the first mismatch, and fails the gate with MSG-P3-038.
5. ReplayTestGate: runs the time-skipping tests in TestWorkflowEnvironment, including a workflow that waits on a 30-day timer.
6. Developer: on a failure, restores the old path or guards the change with Workflow.getVersion, then runs the gate again.
7. Reviewer: merges only with a passing gate 10 result on the pull request; a workflow change with no result cannot merge.
8. Deploy: the pipeline registers the new build ID as the default for the task queue; new workflows start on it and running workflows stay on their build.
9. Rollout report: counts running workflows per build; the script refuses to retire a build with a running workflow and retires it when the count reaches zero.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The nightly export failed, a workflow type has no history, or the newest history is more than 24 hours old | The gate fails closed with no replay; the merge is blocked and the failure names the export job and its last successful run | MSG-P3-038 | AC6 |
| X2 | The rollout script is asked to retire a build that still has a running workflow | The script refuses and names the workflow IDs; the build stays REGISTERED and its workers stay up | None (script refusal) | AC7 |
| X3 | A replay history holds a clear personal data pattern, because a test wrote it without the codec | The file is not written to the replay store, the index row is FAILED, an incident is raised, and the gate fails closed for that workflow type | None (incident only) | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the worker, build ID and gateway of RWB-E1-071; it adds the export, the gate, the time-skipping tests and the rollout script |
| Negotiable | The history count, the freshness limit, the time budget and the retention are configuration; the replay rule and the build ID rule are fixed |
| Valuable | A workflow change that would strand a live case is stopped in the pipeline, not in production |
| Estimable | One export job, one gate, two test bases, one rollout script and one document update |
| Small | Fits two weeks with its tests |
| Testable | Each criterion in section 7 is one test in section 16 on fixed histories and build IDs |

### 7. Acceptance criteria

```gherkin
Feature: Workflow versioning and replay test gate

  Background:
    Given the replay store holds 200 histories exported from SIT on 16 November 2026, including 40 of workflow type PlatformSmokeWorkflow
    Given the export timestamp is 01:00 on 16 November 2026 and the gate runs at 09:00 on 16 November 2026
    Given rwb.p3.temporal is on in SIT

  Scenario: AC1 A non-deterministic change fails the gate
    Given build ID "9f3c2a1-418" produced the 40 PlatformSmokeWorkflow histories
    Given a branch removes the activity call from PlatformSmokeWorkflow and completes at once
    When pipeline gate 10 replays the 40 histories against the branch build
    Then the replay fails with a non-determinism error at the first mismatched event "ActivityTaskScheduled", event ID 4
    Then the gate fails and the merge is blocked with MSG-P3-038 naming the workflow type, history ID and event ID
    Then no build ID is registered for the branch and no worker takes a workflow with that code

  Scenario: AC2 A change guarded by Workflow.getVersion passes
    Given the same 40 PlatformSmokeWorkflow histories
    Given the branch adds a second activity and guards it with Workflow.getVersion("smoke-step-2", Workflow.DEFAULT_VERSION, 2)
    When gate 10 replays the 40 histories
    Then every history takes the pre-version path and replays to the end without error
    Then a new execution takes version 2 and runs the second activity
    Then a history recorded under version 2 replays on the branch build with version 2
    Then the gate passes and the pull request may merge

  Scenario: AC3 Time skipping runs a 30-day timer in under a minute
    Given a test workflow waits on a 30-day timer and then calls one activity
    When the time-skipping test runs in TestWorkflowEnvironment
    Then the timer fires and the workflow completes in under 60 seconds of wall-clock time
    Then the test reports the simulated elapsed time of 30 days
    Then the gate's total run stays inside its 10-minute budget
    Then a run over the budget is reported as failed and never as passed

  Scenario: AC4 A new build ID takes new workflows and old ones drain
    Given build ID "9f3c2a1-418" is the default for rwb-platform and 12 workflows are RUNNING on it
    When the pipeline deploys build ID "7b1d4e0-419" and registers it as the new default
    Then a workflow started after the deploy runs on "7b1d4e0-419"
    Then the 12 running workflows finish on "9f3c2a1-418"
    Then the rollout report shows 12 draining on the old build and 1 running on the new build
    Then the old build is retired only when its running count is zero

  Scenario: AC5 The gate is pipeline gate 10
    Given Recovery Workbench Engineering Practices lists the nine pipeline checks
    When this story is merged
    Then gate 10, "Workflow replay and time-skipping tests", is listed with its owner, its pass rule, its budget and its failure message MSG-P3-038
    Then the merge checklist and the pull request template name gate 10
    Then a pull request that changes a class under recovery.casewf.workflow without a gate 10 result cannot merge

  Scenario: AC6 A stale or missing history export fails the gate closed
    Given the nightly history export failed and the newest history in the replay store is 36 hours old
    When gate 10 runs for a branch that changes PlatformSmokeWorkflow
    Then the gate fails closed with "history export stale" and runs no replay
    Then the merge is blocked and the failure names the export job and its last successful run
    Then no result is reported as a pass
    Then the gate passes only after a fresh export exists

  Scenario: AC7 A build with a running workflow is not retired
    Given build ID "9f3c2a1-418" still has 2 RUNNING workflows
    When the rollout script is asked to retire it
    Then the script refuses and names the 2 workflow IDs
    Then the build stays REGISTERED, its workers stay up and new workflows do not start on it
    Then the retire command succeeds only after both workflows close

  Scenario: AC8 A replay history with a clear payload is refused
    Given a replay history file holds a salary slip payload with the national ID "1101700203456" in clear text, because a SIT test wrote it with the codec off
    When the export job validates the file
    Then the file is not written to the replay store and the index row is FAILED
    Then an incident reaches RW-SECADM and RW-PLATADM
    Then gate 10 fails closed for that workflow type until a clean export exists
    Then the test profile is corrected and the history is deleted at the source
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Workflow code is deterministic, and every change is replayed against the recorded histories of the affected workflow types before merge | D-RCV-36 T7; ADR-011 |
| BR2 | A non-deterministic change fails gate 10 with MSG-P3-038 and blocks the merge; no label, flag or reviewer waives the gate | AC1 |
| BR3 | A behaviour change is guarded with Workflow.getVersion; an old history takes the old path and a new execution takes the new one | AC2 |
| BR4 | Time-skipping tests run every timer in the changed workflow; a 30-day timer completes in under a minute, and a gate run over its 10-minute budget fails | AC3 |
| BR5 | Gate 10 is listed in Recovery Workbench Engineering Practices with its owner, pass rule, budget and failure message, and is part of the merge checklist | AC5 |
| BR6 | Replay histories come from SIT only, are codec-encrypted, are kept 90 days and hold no clear personal data; a history that fails the check is not used | NFR-045; AC8 |
| BR7 | The gate fails closed when the export is missing, stale by more than 24 hours, or refused; it never passes on an empty set | AC6 |
| BR8 | Workers register a build ID; a new workflow goes to the newest default build and a running workflow stays on the build it started on | AC4 |
| BR9 | A build is retired only when it has no running or open workflow, and the rollout script refuses otherwise | AC7 |
| BR10 | The histories per type, the freshness limit, the time budget, the history retention and the build ID format are configuration, never code | REQ-DRI-005 |

### 9. State transitions

None for a case. A build ID and a gate run change state.

| From | Event | Condition | To |
|---|---|---|---|
| None | Deploy and register | The gate passed | REGISTERED |
| REGISTERED | Register as the default for the task queue | It is the newest build | CURRENT; the previous build becomes DRAINING |
| DRAINING | The last running workflow closes | Running count is zero | RETIRED |
| DRAINING | Retire requested | A workflow is still running | DRAINING, refused with the workflow IDs |
| None | Gate run | A history mismatches or the export is stale | FAILED; the merge is blocked |
| None | Gate run | Every history replays and the tests pass | PASSED; the merge may proceed |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Developer, squad member (RW-TRIBE) | Changes workflow code, runs gate 10, reads the replay report (Platform administration, R) |
| Reviewer | Approves the merge only with a passing gate 10 result |
| RW-PLATADM | Runs the rollout, registers a build as the default, retires a build when its count is zero (Platform administration, U) |
| RW-AUDIT | Reads the gate result, the export manifest and the build registry (Platform administration, R) |
| RW-COE | Reads the gate result for a workflow that evaluates a rule package; may not change the gate |
| RW-SECADM | Receives a clear-payload incident from the export; decode stays with RWB-E2-038 |
| No delegation of authority level applies | A pipeline gate is not a credit decision |

Separation of duty: the developer who changes the workflow does not approve the merge.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| None (platform enabler) | None in the recovery schema | None | None |

Replay histories and their index live in Blob storage, container rwb-temporal-replay; the build registry lives in Temporal; the gate result lives in the pipeline and on the pull request; the export job's schedule, owner and run book path live in job_catalog through RWB-E1-056. No DF-REF, DF-CAS or DF-DEC field is added or changed, and the Physical Schema v6 is unchanged.

### 12. Contract

No Workbench endpoint. This story adds no path under /api/recovery/v1. The interfaces are the SDK test kit, Blob storage, the Temporal build ID API and the pipeline.

| Interface | Method | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| WorkflowReplayer | In-process Java call at the pinned SDK version | Workflow class, workflow type, a recorded history | Replay result, or a NonDeterministicException with the event ID | Non-determinism; unknown workflow type | Build and test process only | Read only; replaying the same history twice gives the same result |
| TestWorkflowEnvironment | In-process time-skipping test | Test workflow, timer, activities | Result and the elapsed wall-clock time | Assertion failure; budget exceeded | Build and test process only | Each test run is independent |
| Blob storage (replay) | HTTPS GET and LIST on container rwb-temporal-replay | Index prefix, workflow type, history ID | Index rows and history files | 403 role; 404 no such history; 409 immutability | SY-CASEWF writes in SIT; the build reads | The workflow ID and run ID path is the key |
| Temporal build ID API | gRPC over mTLS, port 7233: UpdateWorkerBuildIdCompatibility, DescribeNamespace | Task queue rwb-platform, build ID set, default build ID | The compatibility set and the default | PERMISSION_DENIED; FAILED_PRECONDITION | Client certificate of SY-CASEWF from the pipeline | Registering the same build ID twice changes nothing |
| Pipeline gate 10 | Pipeline step on the pull request | Branch build, affected workflow types, replay index | PASSED or FAILED, with the report and MSG-P3-038 | A failed replay; a stale export; a budget overrun | The pipeline identity; the result is visible to the reviewer | A re-run on the same commit gives the same result |

The export job never reads a Workbench table or the ACE database. No production history is exported, and the replay store holds SIT data only.

### 13. Solution plan

**Package.** The gate and the test bases in `src/test/java/recovery/casewf/replay`; the export job in `recovery/integration/ops/temporal`; the pipeline step in `.github/workflows/`; the rollout script in `deploy/temporal/rollout/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReplayTestGate | Test and pipeline step | Selects the affected types, replays every history, reports the first mismatch and fails with MSG-P3-038 (BR1, BR2, BR7) |
| HistoryExportJob | Job | Quartz, nightly in SIT: exports 200 closed histories per type, validates and writes the file and the index (BR6) |
| ReplayPayloadCheck | Service | Refuses a history whose payload is not codec-encrypted or holds a clear personal data pattern (BR6) |
| ReplayHistoryStore | Repository | Writes and lists the replay files and the index rows in Blob |
| TestWorkflowEnvironmentBase | Test base | Starts the SDK test environment at the pinned version and applies the shared timeouts |
| TimeSkippingTimerTest | Test | The 30-day timer test and the gate budget check (BR4) |
| BuildIdRolloutScript | Script | Registers a build, reports the running count per build and refuses a premature retirement (BR8, BR9) |
| GateReportPublisher | Service | Attaches the gate result and the replay report to the pull request |

**Database.** No migration and no new table. The export job gets one job_catalog row through RWB-E1-056 as a data change. The replay files and the index live in Blob storage.

**Configuration and reference data**

- 200 histories per workflow type, a 24-hour freshness limit, a 10-minute gate budget and a 90-day replay retention.
- The build ID format `<git-sha>-<build-number>` from RWB-E1-071.
- The list of workflow packages the gate watches: `recovery.casewf.workflow`, from the boundary test of RWB-E1-071.
- Feature flag rwb.p3.temporal for the worker only; the gate has no flag and cannot be switched off.

**Build steps**

1. Build HistoryExportJob and ReplayPayloadCheck; test AC8 and the index with 200 synthetic histories.
2. Build ReplayTestGate over WorkflowReplayer and prove it fails on a deliberate non-deterministic change; test AC1.
3. Add a getVersion guard to the test workflow and prove the old histories pass; test AC2.
4. Build TestWorkflowEnvironmentBase and TimeSkippingTimerTest; test AC3 and the budget.
5. Build BuildIdRolloutScript with the running count and the refusal; test AC4 and AC7.
6. Add the pipeline step, the report and the merge rule; test AC5 and AC6.
7. Add the gate to Engineering Practices, the merge checklist and the pull request template; run the gate on a real pull request in SIT.

**Feature flag.** None on the gate. With rwb.p3.temporal off, no workflow runs, the export finds no history and the gate fails closed; the gate is on in every environment where a workflow class can change.

**Done when.** A deliberate non-deterministic change fails gate 10 in SIT, a getVersion change passes, the 30-day timer test completes in under a minute, a build drains and retires with no lost workflow, and gate 10 is listed in Engineering Practices.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-038 | A workflow change fails the replay test against the recorded histories | The workflow change fails the replay test against recorded histories: {detail}. |

MSG-P3-038 is new and is added to Error and Message Standard v4. {detail} names the workflow type, the history ID, the event ID and the first mismatch, and never a payload. The same message is used for a stale export, with {detail} naming the export job and its last successful run. The gate report carries the same text; no other message ID is added.

### 15. Screens and states

No Workbench screen in this story. The views are the pipeline gate report on the pull request, with the states PASSED, FAILED and Running, and the build registry in the rollout report, with the states REGISTERED, CURRENT, DRAINING and RETIRED. The reviewer sees the gate result on the pull request and in the merge checklist. The platform screens of Epic 8 do not repeat this data.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-040-01 | AC1, BR1, BR2 | System | 40 PlatformSmokeWorkflow histories; branch removes the activity call |
| TC-E2-040-02 | AC2, BR3 | System | The same 40 histories; getVersion "smoke-step-2" version 2 |
| TC-E2-040-03 | AC3, BR4 | System | Test workflow with a 30-day timer; 60-second and 10-minute budgets |
| TC-E2-040-04 | AC4, BR8 | Operational | Build IDs 9f3c2a1-418 and 7b1d4e0-419; 12 running workflows |
| TC-E2-040-05 | AC5, BR5 | Operational | Engineering Practices, merge checklist and pull request template |
| TC-E2-040-06 | AC6, BR7 | System | Replay index 36 hours old; branch changes PlatformSmokeWorkflow |
| TC-E2-040-07 | AC7, BR9 | System | Build 9f3c2a1-418 with 2 running workflows; retire requested |
| TC-E2-040-08 | AC8, BR6 | System | History written with the codec off; clear national ID 1101700203456 |
| TC-E2-040-09 | Operational | Operational | Nightly export in SIT writes 200 encrypted histories per type and the index |
| TC-E2-040-10 | Operational | Operational | Full rollout in SIT: new build takes new workflows, old build drains and retires |

The checks are run by the developer, the reviewer and the platform administrator in SIT and recorded on the pull request and in the release evidence; there is no Workbench endpoint and no Access test in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the history count, the freshness limit, the time budget, the retention and the build ID format are configuration.
- No personal data in logs, tests, workflow history or prompts: the replay store holds codec-encrypted SIT histories only, and a clear payload is refused.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: this story reads no case and no ACE table.
- No production history is exported, and no production data is used in a test or a prompt.
- No workflow change merges without a passing gate 10 result, and no label or flag waives the gate.
- A stale, missing or refused export fails the gate closed; an empty replay set is never a pass.
- No build is retired while it has a running workflow, and no new workflow starts on a draining build.
- No change to the pinned SDK version without the gate run at the new version.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Epic 2, 3.2; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-040-01, TC-E2-040-02, TC-E2-040-03, TC-E2-040-04, TC-E2-040-06, TC-E2-040-08 |

### 19. Out of scope

- The Temporal cluster, namespace and Web UI (RWB-E1-070).
- The worker, codec, gateway and smoke workflow (RWB-E1-071).
- Case workflow code and the reference skeleton (Epic 3, RWB-E2-043).
- Alerts, the stuck scanner and the dashboard (RWB-E2-037).
- The codec server, decode and the administrative audit (RWB-E2-038).
- Backup, failover, upgrade and archive (RWB-E2-039).
- The other nine pipeline checks and the release gates (Recovery Workbench Engineering Practices).
- Load, performance and soak testing of workflow executions (RWB-E1-056, Epic 3).
- Production history export and replay against production data.
---

## RWB-E2-041 Rule change governance and audit report

| Item | Value |
|---|---|
| Story key | RWB-E2-041 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-16 Report every rule change for audit |
| Requirement IDs | REQ-CWC-013, REQ-DRI-011 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 14 Set strategy, policy and decision rules |
| Decision | D-RCV-36 (T4, T5, T8); ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-073, RWB-E1-037 |
| Status | Ready for build |

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the rule change checklist (request, impact, test result, approver, load, verify, rollback plan) recorded on every rule package version and reported for audit**, so that **a rule change is as controlled as a code change**.

### 2. Business rationale

Audit found the collection procedure was not followed because rules lived in documents (CTL-08). Rules are data now: one wrong row in a rule package changes every case that reaches it, so each package version needs the same evidence as a code change: who asked, what it affects, the test result, who approved, when it took effect and how to undo it. This story makes the checklist fields required before a version can be approved and gives audit one report of every package change and of the decisions each version made. It meets REQ-CWC-013 and REQ-DRI-011. The measure is that every package version in force has a complete checklist in the report, and that RWB-E2-005 can reconcile the count of decisions per package version from the same report.

### 3. Preconditions

- RWB-E1-073 is done: `POST /admin/rule-packages/{packageCode}/versions`, approve and rollback exist, and `rule_package_version` carries DF-REF-295 `change_checklist`.
- RWB-E1-037 is done: the permission matrix gives Rules and parameters R to RW-COE, RW-RISK and RW-AUDIT.
- Package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows, loaded by U-41 and approved by U-51.
- The decision log writer (RWB-E1-027, reached through RWB-E1-072) writes `rule_id` DF-DEC-004 and `rule_version` DF-DEC-005 on every package decision, and `rule_version` holds the package version label.
- The checklist JSON schema is agreed on 16 November 2026: `changeRequestRef`, `impactSummary`, `verifyNote`, `verifiedAt`, `rollbackPlan`. The service fills `testResult`, `loadedAt`, `author`, `approver` and `checksum`.
- The reader holds RW-AUDIT or RW-COE with Rules and parameters R.
- Feature flag `rwb.p3.rule-change-report` is on in DEV and SIT.

### 4. Flow

1. Center of excellence analyst: raises the change request in the bank's request tool and receives its reference, for example CR-2026-0042.
2. Center of excellence analyst: fills the package workbook for ALLOCATION version "ALLOC-2026.12" and the checklist: request reference, impact summary "412 open Mortgage cases in the BKK queue", verify note and date from SIT, rollback plan "Roll back to ALLOC-2026.11".
3. Center of excellence analyst: loads the workbook and the checklist through `POST /admin/rule-packages/ALLOCATION/versions` with valid from 2026-12-10.
4. RulePackageVersionService: stores the checklist in DF-REF-295 with the author, `loaded_at`, the checksum and the scenario test result; a verify date before the load is refused.
5. Risk officer: approves through `POST /admin/rule-package-versions/{versionId}/approve`; the service refuses the approval unless the request, impact, verify and rollback plan are present, the test result is PASSED and the approver is not the author.
6. RulePackageEffectiveDateJob: at 00:01 on the valid from date moves the version to IN_FORCE and the previous version to SUPERSEDED.
7. Center of excellence analyst: if the version is wrong, rolls back by one call; the report shows the rollback as its own entry naming the version it returns to.
8. Internal audit or the center of excellence analyst: reads `GET /admin/rule-packages/change-report` for a period and a package, as JSON or CSV; the entry shows the decisions per package version for RWB-E2-005.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A package version reaches its valid from date with no approver | It is not served; the report shows it as LOADED | None | AC2 |
| X2 | Approval with a checklist item missing | Refused; the version stays LOADED | MSG-P3-022 | AC3 |
| X3 | Approval of a version whose test result is FAILED | Refused | MSG-P3-022 | AC4 |
| X4 | The report period has no changes | An empty list is returned | None | AC6 |
| X5 | The verify date is before the load time | Load refused | MSG-GEN-003 | AC7 |
| X6 | The report period ends before it starts | Refused | MSG-GEN-003 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds the checklist fields and one report to the package version of RWB-E1-073 |
| Negotiable | The checklist items are fixed by the Engineering Standards; the report columns can change |
| Valuable | Audit can test every rule change without asking the team, and E2-005 reconciles from one source |
| Estimable | Four checklist fields, three approval checks, one report, two formats |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion is an API test on a PostgreSQL test container |

### 7. Acceptance criteria

```gherkin
Feature: Rule change governance and audit report

  Background:
    Given the business date is 2026-12-01
    Given package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows
    Given user "U-41" holds RW-COE, "U-51" holds RW-RISK and "U-AUD-01" holds RW-AUDIT

  Scenario: AC1 Change by checklist
    Given a request "CR-2026-0042" to change ALLOCATION row "ALLOC-031" from queue "MTG-BKK-CO" to "MTG-CEN-CO" from 2026-12-10
    Given "U-41" loads ALLOCATION version "ALLOC-2026.12" with impact summary "412 open Mortgage cases in the BKK queue" and rollback plan "Roll back to ALLOC-2026.11"
    Given the load checks and the 50 scenarios pass
    Given "U-51" approves version "ALLOC-2026.12" on 2026-12-02
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31
    Then one entry shows package "ALLOCATION", version "ALLOC-2026.12", request "CR-2026-0042", test result "PASSED", author "U-41", approver "U-51", approved on 2026-12-02 and valid from 2026-12-10
    Then the entry shows 1 row changed, 0 added and 0 removed against "ALLOC-2026.11"
    Then the approval time is before the valid from date

  Scenario: AC2 Checklist skipped
    Given ALLOCATION version "ALLOC-2026.13" loaded by "U-41" with a complete checklist, valid from 2026-12-15 and never approved
    When the business date reaches 2026-12-15
    Then the rule package service still serves version "ALLOC-2026.12"
    Then the change report shows version "ALLOC-2026.13" with status "LOADED" and approver empty

  Scenario: AC3 Checklist item missing at approval
    Given RESTRUCTURE version "RES-2026.12" loaded with no rollback plan
    When "U-51" approves it
    Then the system refuses the approval with MSG-P3-022 naming "rollback plan"
    Then version "RES-2026.12" stays "LOADED"

  Scenario: AC4 Failed test result
    Given PAYMENT_MATCH version "PMT-2026.12" whose scenario result is "FAILED" with 2 of 58 scenarios failing
    When "U-51" approves it
    Then the system refuses the approval with MSG-P3-022 naming "test result"

  Scenario: AC5 Verify item recorded before approval
    Given ALLOCATION version "ALLOC-2026.12" loaded on 2026-12-08 with verify note "SIT run 2026-12-08: 50 of 50 scenarios pass and the dry run covers 412 open cases" and verify date 2026-12-08
    When "U-51" approves it on 2026-12-09
    Then the change report shows verify date 2026-12-08, the verify note, the load time 2026-12-08 and checksum "9f2c...e1b4"
    Then the checklist holds all seven items: request, impact, test result, approver, load, verify and rollback plan

  Scenario: AC6 Period with no changes
    When "U-AUD-01" reads the change report for 2026-11-01 to 2026-11-15
    Then the response is an empty list with total 0

  Scenario: AC7 Verify date before the load
    Given ALLOCATION version "ALLOC-2026.14" with verify date 2026-12-07 and load time 2026-12-08
    When "U-41" loads it
    Then the system refuses the load with MSG-GEN-003 naming "verifiedAt" and "loadedAt"

  Scenario: AC8 Period in the wrong order
    When "U-AUD-01" reads the change report from 2026-12-31 to 2026-12-01
    Then the system refuses the call with MSG-GEN-003 naming "to" and "from"

  Scenario: AC9 Report as CSV
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31 with format "csv"
    Then the response is a CSV file with one header row and one row per package version
    Then it carries no party identifier and no case data

  Scenario: AC10 Decisions per package version
    Given ALLOCATION version "ALLOC-2026.11" was in force until 2026-12-09 and "ALLOC-2026.12" from 2026-12-10
    Given the decision log holds 96 entries with package version "ALLOC-2026.11" and 1,204 with "ALLOC-2026.12" in December 2026
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31
    Then version "ALLOC-2026.11" shows 96 decisions and version "ALLOC-2026.12" shows 1,204
    Then the entry shows the decisions per rule ID across both versions: "ALLOC-031" 700 and "ALLOC-032" 600
    Then the total matches GET /api/recovery/v1/decision-log for the same period and package version
    Then RWB-E2-005 reconciles the count per package version from this report
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A package version can be approved only when it carries a change request reference, an impact summary, a verify record, a rollback plan and a test result of PASSED | CTL-08; rule package change process steps 1 to 4 |
| BR2 | The approver is not the author | roles.txt Separation of duty; CTL-08 |
| BR3 | A version that is not approved never takes effect | R-UNI-38; REQ-CWC-013 |
| BR4 | The verify item is dated on or after the load and before the approval | rule package change process step 6 |
| BR5 | The report lists every package version whose load, approval, valid from, verification or rollback falls in the period | REQ-DRI-011 |
| BR6 | The effect of a version is the count of rows added, changed and removed against the version it replaces, by Drools rule name and row order, and the rule IDs changed | D-RCV-36 T4, T5; ADR-012 |
| BR7 | A rollback appears as its own entry naming the version it returns to | REQ-CWC-013; R-UNI-38 |
| BR8 | The decisions per package version are counted from decision_log_entry rule_id and rule_version; the report never recomputes a decision | REQ-DRI-011; D-RCV-36 T5 |
| BR9 | The checklist is one JSON object in DF-REF-295; this story adds no table and no column | D-RCV-36 T4; RWB-E1-072 |

### 9. State transitions

None. This story changes no case status. In the package version statuses of RWB-E1-073, LOADED to APPROVED now needs a complete checklist (BR1), and the report reads every later status without changing it.

| From | Event | Condition | To |
|---|---|---|---|
| LOADED | Approve | Checklist complete, test result PASSED, approver is not the author | APPROVED |
| LOADED | Approve | Any item missing or test result FAILED | LOADED (refused) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads a package version with its checklist; reads the report (Rules and parameters CRUD; read) |
| RW-RISK, risk and model risk officer | Approves package versions (Rules and parameters A); reads the report |
| RW-AUDIT, internal audit | Reads and exports the report (Rules and parameters R). Changes nothing |
| RW-PLATADM, platform administrator | Reads the report (Rules and parameters R) |
| SY-RULES, Drools evaluator | Evaluates the package version and writes its rule ID and version to the decision log |
| No delegation of authority level applies | A package version is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 | rule_package | id | Read |
| DF-REF-275 | rule_package | package_code | Read |
| DF-REF-276 | rule_package | title | Read |
| DF-REF-277 | rule_package | owner_role | Read |
| DF-REF-279 | rule_package_version | id | Read |
| DF-REF-280 | rule_package_version | package_id | Read |
| DF-REF-281 | rule_package_version | version_label | Read |
| DF-REF-282 | rule_package_version | status | Read |
| DF-REF-283 | rule_package_version | source_blob_ref | Read |
| DF-REF-285 | rule_package_version | checksum | Read |
| DF-REF-286 | rule_package_version | valid_from | Read |
| DF-REF-287 | rule_package_version | valid_to | Read |
| DF-REF-288 | rule_package_version | author | Read |
| DF-REF-289 | rule_package_version | approver | Read |
| DF-REF-290 | rule_package_version | loaded_at | Read |
| DF-REF-291 | rule_package_version | approved_at | Read |
| DF-REF-292 | rule_package_version | test_result | Read |
| DF-REF-293 | rule_package_version | dry_run_counts | Read |
| DF-REF-294 | rule_package_version | rollback_of | Read |
| DF-REF-295 | rule_package_version | change_checklist | Write, read |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-296 | rule_row | package_version_id | Read |
| DF-REF-297 | rule_row | drools_rule_name | Read |
| DF-DEC-004 | decision_log_entry | rule_id | Read, through the P7 query interface |
| DF-DEC-005 | decision_log_entry | rule_version | Read, through the P7 query interface |

Field IDs are those in the Logical Data Model and Data Dictionary. The checklist JSON holds the seven items of section 1; the service writes `testResult`, `loadedAt`, `author`, `approver` and `checksum` from the package version row, so no item is typed twice.

### 12. Contract

**POST /api/recovery/v1/admin/rule-packages/{packageCode}/versions** (existing endpoint of RWB-E1-073, one field added): multipart gains `checklist` (JSON object, max 8 KB) with `changeRequestRef` (max 30), `impactSummary` (max 1000), `verifyNote` (max 1000), `verifiedAt` (date) and `rollbackPlan` (max 1000). Missing fields do not refuse the load; they refuse the approval (BR1).

**POST /api/recovery/v1/admin/rule-package-versions/{versionId}/approve** (existing): 409 with MSG-P3-022 naming the missing item when BR1 fails; otherwise as RWB-E1-073.

**GET /api/recovery/v1/admin/rule-packages/change-report** (new, P3)

| Item | Value |
|---|---|
| Request | Query: `from` (date, required), `to` (date, required), `packageCode` (optional), `format` (`json` default or `csv`), `page`, `size` (default 50, max 200) |
| Response | 200 `ChangeReportPage`: `items[]` of `RulePackageChangeEntry` (`packageCode`, `packageTitle`, `versionLabel`, `status`, `validFrom`, `validTo`, `changeRequestRef`, `impactSummary`, `verifyNote`, `verifiedAt`, `testResult`, `author`, `loadedAt`, `approver`, `approvedAt`, `checksum`, `rollbackPlan`, `rulesChanged[]`, `decisions`, `decisionsByRule[]`, `rolledBackTo`), `page`, `size`, `total`; or `text/csv` with the same columns |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 422 `to` before `from` (MSG-GEN-003); 503 |
| Authorization | Rules and parameters, right R |
| Idempotency | Not applicable |

**Published interface** (added to the P4 `RulePackageVersionService`, used by the report and by RWB-E2-005):

```java
Page<RulePackageChangeEntry> changeReport(LocalDate from, LocalDate to, Optional<String> packageCode, Pageable page);
```

No events are published.

### 13. Solution plan

**Package.** `recovery.casewf.rules.audit` in the recovery module; the endpoint and the version writes in the P4 package `recovery.accessadmin.rulepackages`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ChangeChecklistValidator | Service | The BR1 and BR2 checks called by `approve(...)` |
| ChangeEffectCalculator | Service | Compares the rule_row rows of a version with the version it replaces by `drools_rule_name` and row order; lists the rule IDs changed |
| DecisionCountReader | Service | Reads the count per rule ID and package version from the P7 decision log query interface |
| RuleChangeReportService | Service | Builds the report for a period and a package; paging; CSV writer |
| RuleChangeReportController | Controller | `GET /admin/rule-packages/change-report`; problem responses |
| RulePackageVersionRepository | Repository | Extended with the period query on loaded, approved, valid from and verify dates |

**Database.** Flyway migration `V<next>__rwb_e2_041_change_report_index.sql` adds `ix_rpv_loaded_at` on `rule_package_version (loaded_at)`, `ix_rpv_approved_at` on `(approved_at)` and `ix_rpv_valid_from` on `(valid_from)`. No new column: DF-REF-295 exists from V072_1 of RWB-E1-072.

**Configuration and reference data.** None beyond RWB-E1-073. The checklist items come from the Engineering Standards rule package change checklist. The report reads the package version rows and the decision log; it never recomputes a version from the live rule rows.

**Build steps**

1. Write the index migration and the repository period query.
2. Extend the load handler to accept the `checklist` part and store it in DF-REF-295; test the verify date check (AC7).
3. Build `ChangeChecklistValidator` and call it from `approve(...)`; return MSG-P3-022 naming the first missing item (AC3, AC4).
4. Build `ChangeEffectCalculator` and test it on versions with added, changed and removed rows (AC1).
5. Build `DecisionCountReader` against the P7 query interface and test the counts (AC10).
6. Build `RuleChangeReportService` and `RuleChangeReportController` with JSON and CSV output (AC6, AC8, AC9).
7. Test the skipped approval and the valid from path (AC2, AC5).
8. Add the access test and the contract test for the new operation (TC-E2-041-11).

**Feature flag.** `rwb.p3.rule-change-report`. Off: the report endpoint returns 404 and approval runs the RWB-E1-073 checks only.

**Done when.** The tests in section 16 pass, the report for the SIT load period lists every package version loaded in SIT with a complete checklist, and its decision counts reconcile with RWB-E2-005.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-022 | Approval with a missing checklist item or a FAILED test result | The change cannot be approved: {item} is missing or failed. |
| MSG-GEN-003 | Verify date before the load, or a report period in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-001 | A required checklist value is empty | Enter {field}. |
| MSG-P7-002 | The author approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | A role without the right reads the report | You cannot {action} here. Your role does not include it. |

MSG-P3-022 moves here from RWB-E1-048 with the story (D-RCV-36 T8). Thai text for each message follows DL10.

### 15. Screens and states

No screen in this story. Internal audit and the center of excellence read the report through the endpoint and open the CSV in Excel. The rules and parameters screen SCR-39 shows the same entries from Epic 8.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-041-01 | AC1, BR1, BR5, BR6 | System | ALLOCATION v11 to v12, request CR-2026-0042, one changed row |
| TC-E2-041-02 | AC2, BR3 | System | ALLOCATION v13 never approved |
| TC-E2-041-03 | AC3, BR1 | System | RESTRUCTURE v12 with no rollback plan |
| TC-E2-041-04 | AC4, BR1 | System | PAYMENT_MATCH v12 with a FAILED scenario result |
| TC-E2-041-05 | AC5, BR1, BR4 | System | Verify date 2026-12-08, approval 2026-12-09 |
| TC-E2-041-06 | AC6 | System | Period 2026-11-01 to 2026-11-15 with no versions |
| TC-E2-041-07 | AC7, BR4 | System | Verify date one day before the load |
| TC-E2-041-08 | AC8 | System | Period end before start |
| TC-E2-041-09 | AC9 | System | CSV export of December versions |
| TC-E2-041-10 | AC10, BR8 | System | 96 and 1,204 decisions in December 2026 |
| TC-E2-041-11 | Access | Access | RW-CASEOWN (no Rules and parameters right) reads the change report; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. The checklist items are data; the report computes from rows.
- No personal data in logs, tests, workflow history or prompts. The report carries staff user IDs and no customer or case data.
- No read of another module's tables; ACE data only through recovery.v_ace_* views. The decision counts come through the P7 query interface.
- The report reads the package version registry and the decision log; it never recomputes a version from the live rule rows.
- The approver is never the author; the service checks it, not only the screen.
- Forbidden: any change to an existing version. A rollback is a new entry that names the version it returns to.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated package version with a checklist and rollback | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E2-041-01 to TC-E2-041-04, TC-E2-041-11 |
| REQ-DRI-011 | Versioned tables with author and approver, and a count of decisions per version | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | CTL-08 | TC-E2-041-01, TC-E2-041-05 to TC-E2-041-10 |

### 19. Out of scope

- The load, checks, scenarios, approval and rollback mechanics of a rule package version (RWB-E1-073).
- The reference table checklist fields and their report (RWB-E1-043); this report covers rule package versions only.
- The rules and parameters screen (SCR-39, Epic 8).
- The QA sample against the rule package version applied (FEAT-ADM-08, Epic 8).
- The decision log store and its read API (RWB-E1-008, RWB-E1-027).
---

## RWB-E2-042 Epic 2 rule packages in Drools

| Item | Value |
|---|---|
| Story key | RWB-E2-042 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-14 Load a rule package version with validation |
| Requirement IDs | REQ-CWC-013, REQ-CWC-014 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Epic 2, sections 3.2 and 3.8; Business Requirements Program, section 5.3 |
| L3 process | 14 Set strategy, policy and decision rules |
| Decision | D-RCV-36 (T3, T4, T5, T10); ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-073 |
| Status | Ready for build |

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH packages authored in the Drools template, with scenarios, and loaded through RWB-E1-073**, so that **the Epic 2 engines decide by versioned rule packages**.

### 2. Business rationale

Epic 2 rules live in three places today: reference rule rows, the payment_match_rule table and the BookingMatchRules class. D-RCV-36 T10 drops payment_match_rule, and the Epic 2 engines that read these rules would each need their own loader unless one authored, tested and versioned form exists. This story puts every Epic 2 rule in three Drools packages, each with at least 50 scenarios, and loads them through the path that RWB-E1-073 already controls. It meets REQ-CWC-013 and REQ-CWC-014 and gives RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035 one catalog to read. The measure is that three package versions are in force with 174 passing scenarios, and the physical schema has no payment_match_rule table.

### 3. Preconditions

- RWB-E1-073 is done: the Drools XLS template, `POST /admin/rule-packages/{packageCode}/versions`, the version list, approve and rollback, the scenario runner and RuleScenarioBuildGate.
- RWB-E1-072 is done: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` with DF-REF-296 to DF-REF-299, `RuleEvaluator` and `RuleCatalog`.
- The five Epic 1 package codes are seeded by RWB-E1-072. The three Epic 2 package codes are not seeded; this story seeds them in `rule_package` (DF-REF-274 to DF-REF-278).
- RW-COE holds the current Epic 2 rules: R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02, the route-set rows with action_text, owner_role and timer_spec, R-RES-26 with EXACT, PARTIAL and WINDOW, and the BookingMatchRules rows.
- The version labels are agreed on 16 November 2026: "RES-2026.12", "PMT-2026.12" and "BKG-2026.12", all valid from 2026-12-15 (assumed).
- The scenario counts are agreed: 62 for RESTRUCTURE, 58 for PAYMENT_MATCH and 54 for BOOKING_MATCH (assumed), all at or above `rules.testcases.min` = 50.
- The Blob container rule-packages exists and the recovery module identity has write and read rights on that container only.
- RW-COE and RW-RISK are separate people; `rwb.p3.drools` is on in DEV and SIT.

### 4. Flow

1. Center of excellence analyst: reads the current Epic 2 rules from the rule catalog, `payment_match_rule` and BookingMatchRules, and writes one workbook per package.
2. Center of excellence analyst: fills the Rows tab (RuleSet = package code, NAME = rule ID, default row last) and the Tests tab with 62, 58 and 54 scenarios.
3. Center of excellence analyst: loads each workbook through `POST /admin/rule-packages/{packageCode}/versions` with valid from 2026-12-15.
4. RulePackageVersionService: runs the compile, schema, overlap, unreachable row, default row, scenario and dry run checks of RWB-E1-073.
5. Risk officer: approves each version; the author cannot approve.
6. RulePackageEffectiveDateJob: at 00:01 on 2026-12-15 moves each APPROVED version to IN_FORCE and the previous version, if any, to SUPERSEDED.
7. Build: RuleScenarioBuildGate runs 174 scenarios from the three in-force versions; the schema check asserts that no table named payment_match_rule exists.
8. Engines: RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035 read the rows by rule ID and package version through RuleCatalog.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A RESTRUCTURE workbook holds fewer than 50 scenarios, or a scenario fails | Load refused; the failing scenario IDs named | MSG-P3-027 | AC1 |
| X2 | A PAYMENT_MATCH row has a match_type outside EXACT, PARTIAL and WINDOW | Load refused; row and cell named | MSG-P3-027 | AC2 |
| X3 | Two BOOKING_MATCH rows match the same booking key at the same row order | Load refused; both rule IDs named | MSG-P3-027 | AC3 |
| X4 | The PAYMENT_MATCH row order puts PARTIAL before WINDOW | Load refused at the schema check; the priority cells named | MSG-P3-027 | AC4 |
| X5 | A RESTRUCTURE route-set row has an empty action_text, owner_role or timer_spec | Load refused; row and column named | MSG-P3-027 | AC5 |
| X6 | A migration in the release creates payment_match_rule | The schema check fails and the build is blocked | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the template, loader, scenario runner and build gate of RWB-E1-073; this story adds three workbooks, two checks and one seed |
| Negotiable | Rows, scenarios, package codes and version labels are data; the checks are fixed |
| Valuable | Every Epic 2 rule is authored, tested and versioned in one place, and payment_match_rule is gone |
| Estimable | Three workbooks, 174 scenarios, two load checks, one schema check and one seed migration |
| Small | Fits two sprints with its tests |
| Testable | Each criterion is a load test or a schema test on a Testcontainers database |

### 7. Acceptance criteria

```gherkin
Feature: Epic 2 rule packages in Drools

  Background:
    Given the loader U-41 holds RW-COE and the approver U-51 holds RW-RISK
    Given package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH are seeded with owner role RW-COE
    Given rules.testcases.min is 50 and the business date is 2026-12-10

  Scenario: AC1 RESTRUCTURE package
    Given a RESTRUCTURE workbook version "RES-2026.12" with 38 rows and 62 scenarios
    When U-41 loads it with valid from 2026-12-15
    Then the compile, schema, overlap, unreachable row and default row checks pass
    Then the test result is "62 of 62 scenarios passed"
    When U-51 approves it
    Then version "RES-2026.12" is APPROVED and in force from 2026-12-15
    Then rule_row holds 38 rows under version "RES-2026.12", including R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02

  Scenario: AC2 PAYMENT_MATCH package
    Given a PAYMENT_MATCH workbook version "PMT-2026.12" with 3 rows and 58 scenarios
    When U-41 loads it with valid from 2026-12-15
    Then the test result is "58 of 58 scenarios passed"
    When U-51 approves it
    Then version "PMT-2026.12" is APPROVED and in force from 2026-12-15
    Then rule_row holds the rows EXACT, WINDOW and PARTIAL under version "PMT-2026.12"

  Scenario: AC3 BOOKING_MATCH package
    Given a BOOKING_MATCH workbook version "BKG-2026.12" with 21 rows and 54 scenarios
    When U-41 loads it with valid from 2026-12-15
    Then the test result is "54 of 54 scenarios passed"
    When U-51 approves it
    Then version "BKG-2026.12" is APPROVED and in force from 2026-12-15
    Then rule_row holds 21 rows under version "BKG-2026.12" and the comparison evaluator of RWB-E2-007 is no longer used

  Scenario: AC4 PAYMENT_MATCH keeps the priority order of RWB-E2-027
    Given PAYMENT_MATCH version "PMT-2026.12" is in force on 2026-12-15
    When JOB-07 matches payments for that date
    Then the rows are tried in the order EXACT priority 1, WINDOW priority 2, PARTIAL priority 3
    Then payment "PAY-91008" of 12,500.00 THB that both EXACT and WINDOW match is decided by EXACT
    Then payment "PAY-91002" of 11,875.00 THB is decided by PARTIAL with a shortfall of 625.00 THB
    Then the decision log entry names rule "R-RES-26" and rule version "PMT-2026.12"
    Then the order matches RWB-E2-027 BR1 and its "PM-2026.12" row order

  Scenario: AC5 RESTRUCTURE rows feed RWB-E2-035
    Given RESTRUCTURE version "RES-2026.12" is in force on 2026-12-15
    When SY-RULES evaluates R-RES-04 for case "RW-2026-000777"
    Then RuleCatalog.row("R-RES-04", "RES-2026.12") returns action_text "Assign the case to a restructuring officer and start the offer clock", owner_role "RW-RESTRUCT" and timer_spec "2 working days"
    Then every route-set row that RWB-E2-035 reads carries the three fields
    Then RWB-E2-035 sets the next action, the owner and the due date from these values

  Scenario: AC6 payment_match_rule is not created
    Given a database migrated from empty with the release migrations on 2026-12-10
    When the schema check runs
    Then no table named payment_match_rule exists
    Then no column of DF-REF-261 to DF-REF-273 exists
    Then the table count is 93
    Then the build fails if any migration in the release creates payment_match_rule
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each Epic 2 package is authored in the Drools XLS template and loaded only through RWB-E1-073; no direct SQL and no second load path | D-RCV-36 T3, T4 |
| BR2 | Each package version carries at least `rules.testcases.min` (50) scenarios, and every scenario passes before approval | REQ-CWC-014; D-RCV-36 T4 |
| BR3 | PAYMENT_MATCH has one row per match type, and the row order is EXACT then WINDOW then PARTIAL, as in RWB-E2-027 | R-RES-26; D-RCV-36 T10 |
| BR4 | RESTRUCTURE route-set rows carry action_text, owner_role and timer_spec; RWB-E2-035 reads them only from the catalog | D-RCV-36 T6; FEAT-CWC-28 |
| BR5 | payment_match_rule is not created, and DF-REF-261 to DF-REF-273 stay retired; no code, rule row or test reads or writes them | D-RCV-36 T10 |
| BR6 | The package code is the RuleSet; the version labels are RES-, PMT- and BKG-yyyy.MM | D-RCV-36 T5 |
| BR7 | First match, exactly one row decides, and the default row is last | D-RCV-36 T5 |
| BR8 | Open cases keep the package version they were decided under | R-UNI-38 |
| BR9 | RuleScenarioBuildGate runs every in-force package's scenarios in every build | REQ-CWC-014; D-RCV-36 T4 |

### 9. State transitions

None. This story changes no case status. It adds three package versions to the status model of RWB-E1-073.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every check passes and at least 50 scenarios pass | LOADED |
| LOADED | Approve | Approver is not the author | APPROVED |
| APPROVED | RULE_PACKAGE_EFFECTIVE (00:01 job) | Valid from reached | IN_FORCE; the earlier version SUPERSEDED |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Authors and loads the three workbooks (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Approves each package version (Rules and parameters A); may not hold RW-COE |
| RW-AUDIT, internal audit | Reads versions, scenarios and dry run counts (Rules and parameters R) |
| SY-RULES, Drools evaluator | Evaluates the three packages for Epic 2 engines |
| The build pipeline, no user role | Runs RuleScenarioBuildGate and the schema check; no PROD data in the build |
| No delegation of authority level applies | A rule package version is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 | rule_package | id | Write, seed |
| DF-REF-275 | rule_package | package_code | Write, seed |
| DF-REF-276 | rule_package | title | Write, seed |
| DF-REF-277 | rule_package | owner_role | Write, seed |
| DF-REF-278 | rule_package | hit_policy | Write, seed |
| DF-REF-279 | rule_package_version | id | Write |
| DF-REF-280 | rule_package_version | package_id | Write |
| DF-REF-281 | rule_package_version | version_label | Write |
| DF-REF-282 | rule_package_version | status | Write |
| DF-REF-283 | rule_package_version | source_blob_ref | Write |
| DF-REF-284 | rule_package_version | drl_source | Write |
| DF-REF-285 | rule_package_version | checksum | Write |
| DF-REF-286 | rule_package_version | valid_from | Write |
| DF-REF-287 | rule_package_version | valid_to | Write |
| DF-REF-288 | rule_package_version | author | Write |
| DF-REF-289 | rule_package_version | approver | Write |
| DF-REF-290 | rule_package_version | loaded_at | Write |
| DF-REF-291 | rule_package_version | approved_at | Write |
| DF-REF-292 | rule_package_version | test_result | Write |
| DF-REF-293 | rule_package_version | dry_run_counts | Write |
| DF-REF-294 | rule_package_version | rollback_of | Write |
| DF-REF-295 | rule_package_version | change_checklist | None in this story (RWB-E2-041) |
| DF-REF-296 | rule_row | package_version_id | Write |
| DF-REF-297 | rule_row | drools_rule_name | Write |
| DF-REF-298 | rule_row | outputs | Write |
| DF-REF-001 to DF-REF-015 | rule_row | all rule fields | Write |
| DF-REF-052 to DF-REF-054 | rule_row | rule_table, row_order, target_queue_code | Write |
| DF-REF-008 | rule_row | action_text | Write, read by RWB-E2-035 |
| DF-REF-010 | rule_row | owner_role | Write, read by RWB-E2-035 |
| DF-REF-011 | rule_row | timer_spec | Write, read by RWB-E2-035 |
| DF-REF-185 to DF-REF-197 | rule_test_case | all fields | Write |
| DF-REF-299 | rule_test_case | package_version_id | Write |

DF-REF-261 to DF-REF-273 belong to payment_match_rule and are retired by D-RCV-36 T10. No migration creates the table, no rule row uses those IDs, and Physical Schema v6 counts 93 tables without it. The load writes `rule_row` and `rule_test_case` through the package version id; the engines read only through RuleCatalog. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /api/recovery/v1/admin/rule-packages/{packageCode}/versions** (existing endpoint of RWB-E1-073), called with `packageCode` = RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH

| Item | Value |
|---|---|
| Request | multipart/form-data: file (xlsx with Rows and Tests), validFrom (date) |
| Response | 201 RulePackageVersion: versionId, packageCode, versionLabel, status LOADED, validFrom, author, checksum, testResult, dryRunCounts |
| Errors | 401; 403 no Rules and parameters C (MSG-P4-002); 404 unknown package code; 409 version label exists (MSG-GEN-004); 422 a check failed (MSG-P3-027), empty file (MSG-GEN-001), date order (MSG-GEN-003); 503 |
| Authorization | Rules and parameters, right C |
| Idempotency | Package code and version label; a repeat is refused with 409 |

**GET /api/recovery/v1/admin/rule-packages/{packageCode}/versions** and **POST /api/recovery/v1/admin/rule-package-versions/{versionId}/approve**: as in RWB-E1-073, with no field added.

**Published read interface**

```java
RuleRow RuleCatalog.row(String ruleId, String packageVersion);  // DF-REF-008, 010, 011 and outputs
```

No new Workbench endpoint, no event and no published write interface. The three package codes are the only new rows in `rule_package`.

### 13. Solution plan

**Package.** `recovery.casewf.rules.epic2` for the checks; the seed and the schema test in the P3 migration and test folders.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Epic2PackageSeed | Migration | Inserts the three rule_package rows with package_code, title, owner_role RW-COE and hit_policy FIRST |
| PaymentMatchOrderCheck | Validator extension | BR3: one row per match type and the order EXACT, WINDOW, PARTIAL; called from RuleLoadValidator |
| RestructureCatalogCheck | Validator extension | BR4: action_text, owner_role and timer_spec are present on every route-set row; called from RuleLoadValidator |
| PaymentMatchRuleAbsentCheck | Schema test | Fails the build when payment_match_rule, or any column of DF-REF-261 to DF-REF-273, exists |
| Epic2PackageWorkbooks | Configuration | The three xlsx files and their Tests tabs, owned by RW-COE |
| RuleScenarioBuildGate | Build gate (existing) | Runs the 174 scenarios of the three in-force versions |
| Epic2LoadRunbook | Run book | The load order, the approver, the valid from and the rollback for each package |

**Database and Blob**

- `V2_042_1__epic2_rule_packages.sql` inserts RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH into `rule_package` (DF-REF-274 to DF-REF-278). It writes no `rule_package_version` row; the versions come from the load.
- `V2_042_2__drop_payment_match_rule.sql` runs `DROP TABLE IF EXISTS payment_match_rule` and its indexes, for DEV and SIT builds that created it before D-RCV-36 T10. The load runbook archives the rows to a CSV before the migration runs. No migration in the release creates the table.
- Blob paths `RESTRUCTURE/RES-2026.12.xlsx`, `PAYMENT_MATCH/PMT-2026.12.xlsx` and `BOOKING_MATCH/BKG-2026.12.xlsx`; write-once, checksum in the object metadata and DF-REF-285.

**Configuration and reference data**

- The three workbooks and their Tests tabs (RW-COE).
- Version labels and valid from 2026-12-15 (assumed; RW-COE).
- `rules.testcases.min` = 50 through RWB-E1-042.

**Build steps**

1. Write the seed migration and the three package rows (AC1 to AC3, first step).
2. Add PaymentMatchOrderCheck to RuleLoadValidator; test a wrong order and the accepted order (AC4 and section 5 X4).
3. Add RestructureCatalogCheck; test a blank action_text (AC5).
4. Author the three workbooks and their 174 scenarios; load and approve them in SIT (AC1 to AC3).
5. Add PaymentMatchRuleAbsentCheck and the table count assertion (AC6).
6. Run RuleScenarioBuildGate over the three versions and add the lock manifest entries.
7. Write the load runbook and the rollback step for each package.

**Feature flag.** `rwb.p3.drools`. Off: the three package endpoints and the row reads return 404 or NoPackageInForce and nothing else changes.

**Done when.** The tests in section 16 pass, the three versions are in force in SIT with 174 passing scenarios, and the migrated schema has 93 tables and no payment_match_rule.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A workbook check fails, including the match order and the catalog completeness | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-002 | The approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-001 | An empty workbook | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-P4-002 | A role without the right calls a package endpoint | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 the {check} value is compile, schema, overlap, unreachable row, default row or scenario; the match order and the catalog completeness are part of the schema check. The {detail} names row IDs, cells or scenario IDs only, never a case fact or a person. This story adds no message.

### 15. Screens and states

No screen in this story. The three package versions are read through `GET /admin/rule-packages/{packageCode}/versions`; SCR-39 Rules and parameters shows the same versions from Epic 8. The states LOADED, APPROVED, IN_FORCE, SUPERSEDED and REFUSED are shown in the version list.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-042-01 | AC1, BR2, BR7, BR9 | System | RESTRUCTURE RES-2026.12, 38 rows, 62 scenarios |
| TC-E2-042-02 | AC2, BR2, BR3 | System | PAYMENT_MATCH PMT-2026.12, 3 rows, 58 scenarios |
| TC-E2-042-03 | AC3, BR2, BR7 | System | BOOKING_MATCH BKG-2026.12, 21 rows, 54 scenarios |
| TC-E2-042-04 | AC4, BR3, BR7 | System | PAY-91008 matched by EXACT and WINDOW; PAY-91002 5 percent short |
| TC-E2-042-05 | AC5, BR4 | System | R-RES-04 and the route-set rows of RES-2026.12 |
| TC-E2-042-06 | AC6, BR5 | Schema | Migrated database, table count 93, no payment_match_rule |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. Rows, conditions, match types, tolerances, windows, action text, owner roles and timers are data.
- No personal data in logs, tests, workflow history or prompts. Scenarios use synthetic case facts and payment codes.
- No read of another module's tables; ACE data only through recovery.v_ace_* views.
- Every package version goes through RWB-E1-073; no direct SQL load and no second loader.
- payment_match_rule is never created, and DF-REF-261 to DF-REF-273 are never referenced.
- No package version is edited in place; a change is a new version and a rollback moves the pointer.
- The build gate reads a release manifest and a Testcontainers database; it never connects to SIT, UAT or PROD.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version and rollback by one call | Epic 1, 3.3; Epic 2, 3.2 and 3.8; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-UNI-38; R-RES-26 | TC-E2-042-01, TC-E2-042-02, TC-E2-042-03, TC-E2-042-06 |
| REQ-CWC-014 | Schema, overlap, unreachable, default and scenario checks before a rule takes effect | Epic 1, 3.3; Epic 2, 3.2 and 3.8; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-RES-26; R-RES-04 | TC-E2-042-01 to TC-E2-042-05 |

### 19. Out of scope

- The load, scenario, approval and rollback mechanics (RWB-E1-073).
- The PAYMENT_MATCH evaluation order in JOB-07 and the partial floor behaviour (RWB-E2-027).
- The RESTRUCTURE evaluation and the next-action copy (RWB-E2-002, RWB-E2-004, RWB-E2-035).
- The BOOKING_MATCH engine wiring (RWB-E2-007).
- The remaining 448 routing rules and the UNIVERSAL package (Epic 3; DL24).
- The rules and parameters screen (SCR-39, Epic 8).
---

## RWB-E2-043 Temporal and Drools integration pattern and reference case workflow

| Item | Value |
|---|---|
| Story key | RWB-E2-043 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-DRI-07 Run the Drools evaluator on versioned rule packages |
| Requirement IDs | REQ-DRI-001, REQ-DRI-005, REQ-CWC-016 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.2 and 5.7 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1, T2, T7); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-071, RWB-E1-072, RWB-TE-006 |
| Status | Ready for build |

### 1. Story

As a **developer**, I want **a reference case-workflow skeleton that shows signal handling, rule evaluation in an activity, the decision log before the action, state rows updated by an activity and outbound work through the outbox**, so that **Epic 3 builds every case workflow the same way**.

### 2. Business rationale

Epic 3 will add a workflow per case, and each squad would otherwise invent its own order of steps. A workflow that applies a state change before its decision log entry breaks Principle 5, and a workflow that calls Drools outside an activity breaks replay. This story fixes both in one small skeleton: the signal arrives, the rule is evaluated in an activity, the decision log entry is written in its own activity, the state is applied in a third, and a failure at any step stops the next. It is test-only and runs with no live case, so Epic 3 can copy it without a production risk. It meets REQ-DRI-001, REQ-DRI-005 and REQ-CWC-016. The measure is that every Epic 3 workflow is a copy of the skeleton and passes the replay gate of RWB-E2-040.

### 3. Preconditions

- RWB-E1-071 is done: the worker on `rwb-platform`, PdpaPayloadCodec, WorkflowGateway, PlatformSmokeWorkflow and the boundary test.
- RWB-E1-072 is done: `RuleEvaluator.evaluate`, `RuleResult` with `packageVersion` and `RuleCatalog.row`.
- RWB-TE-006 is done: `outbox_event`, `outbox_delivery` and the JOB-11 sender step.
- RWB-E1-027 is done: `DecisionLogWriter.write` runs in the caller's transaction with an idempotency key.
- Package RESTRUCTURE version "RES-2026.12" is in force from 2026-12-01, with R-RES-04 moving IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER.
- The synthetic case "RW-2026-000777" exists in the DEV and SIT test data and is marked synthetic; no live case is used.
- The Temporal server and Java SDK versions approved by SCB IT are pinned in Environment and Deployment Design v4.
- Feature flag `rwb.p3.temporal` is on in DEV and SIT; `rwb.p3.drools` is on.

### 4. Flow

1. Test harness: starts ReferenceCaseWorkflow with workflow ID "ref-case-RW-2026-000777" on task queue `rwb-platform`, with the synthetic case and the reference package code.
2. Workflow: waits for the CaseEvent signal; no activity runs before it.
3. CaseEventSignalRelay: reads the outbox event "EV-CASE-0777-01" and calls `WorkflowGateway.signal(workflowId, "CaseEvent", payload)`.
4. Workflow: calls EvaluateRulesActivity with the package code, the case facts and the business date; the activity calls `RuleEvaluator.evaluate` and returns `RuleResult` with the rule ID, the package version and the outputs.
5. Workflow: calls WriteDecisionLogActivity with the event key; the activity calls `DecisionLogWriter.write` in its own transaction and returns the entry reference.
6. Workflow: only after a successful entry calls ApplyStateActivity with the same key; the activity calls the P3 case state service and writes one state row.
7. Workflow: completes. A failed decision log write leaves the state untouched, fails the workflow with MSG-P7-003 and raises an incident.
8. Platform administrator: reads the run in the Temporal Web UI; internal audit reads the same history and sees encrypted payloads only.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision log write fails | The state activity is not called; the workflow fails after its retries; an incident | MSG-P7-003 | AC2 |
| X2 | Temporal is unavailable when the signal is sent | The signal fails; the outbox event and its delivery stay for the next attempt | MSG-P3-036 | AC5 |
| X3 | An activity commits and then times out before it returns | The retry uses the same idempotency key and finds the first row | None | AC3 |
| X4 | A new package version is in force while the workflow waits | The recorded activity result keeps the version chosen at evaluation time; replay takes the same path | None | AC4 |
| X5 | `rwb.p3.temporal` is off | No worker and no reference workflow; nothing runs | None | AC6 |
| X6 | A second CaseEvent arrives while the first is processing | Temporal buffers it and the first path completes in signal order | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the worker of RWB-E1-071, the evaluator of RWB-E1-072 and the outbox of RWB-TE-006; it adds one test-only workflow and three activities |
| Negotiable | Retry values are configuration; the step order is fixed |
| Valuable | Epic 3 copies one proven order instead of inventing one per workflow |
| Estimable | One workflow, three activities, one signal record, one relay, one retry policy |
| Small | Fits one sprint with its tests |
| Testable | Each criterion runs with TestWorkflowEnvironment time skipping and a synthetic case |

### 7. Acceptance criteria

```gherkin
Feature: Temporal and Drools integration pattern and reference case workflow

  Background:
    Given the environment is SIT with synthetic data and no live case
    Given rwb.p3.temporal is on and the worker polls "rwb-platform"
    Given RESTRUCTURE version "RES-2026.12" is in force from 2026-12-01
    Given rule R-RES-04 moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER
    Given the synthetic case "RW-2026-000777" has status IN_PROGRESS and route state IN_FCR_QUEUE

  Scenario: AC1 The four steps run in order
    Given the reference workflow "ref-case-RW-2026-000777" is running and waits for a CaseEvent
    Given outbox event "EV-CASE-0777-01" of type CASE_PICKED_UP
    When CaseEventSignalRelay calls WorkflowGateway.signal with "CaseEvent" and the event payload
    Then the workflow history shows EvaluateRulesActivity, then WriteDecisionLogActivity, then ApplyStateActivity
    Then EvaluateRulesActivity returns rule "R-RES-04" and package version "RES-2026.12"
    Then WriteDecisionLogActivity writes one entry with rule "R-RES-04" and rule version "RES-2026.12"
    Then ApplyStateActivity moves the route state to "WITH_FCR_OFFICER"
    Then no case row is written before the decision log entry

  Scenario: AC2 A failed decision log write stops the state change
    Given the decision log store is unavailable
    When the CaseEvent "EV-CASE-0777-02" is processed
    Then WriteDecisionLogActivity throws DecisionLogUnavailableException
    Then the workflow does not call ApplyStateActivity
    Then the route state of "RW-2026-000777" stays "IN_FCR_QUEUE"
    Then the workflow fails with MSG-P7-003 after its retries and an incident is raised

  Scenario: AC3 Activity retries are idempotent
    Given ApplyStateActivity commits the state row and then times out before it returns
    When Temporal retries the activity with idempotency key "CASE_EVENT:EV-CASE-0777-03"
    Then the second attempt returns the first result and changes nothing
    Then one case state row exists for "EV-CASE-0777-03"
    Then WriteDecisionLogActivity ran once and one decision_log_entry row exists with that key
    Then the workflow completes once

  Scenario: AC4 The rule version is pinned in the result and replay is stable
    Given EvaluateRulesActivity returned package version "RES-2026.12" and rule "R-RES-04" for "EV-CASE-0777-04"
    Given package version "RES-2027.01" is in force from 2027-01-01 while the workflow waits for the next event
    When the workflow is replayed from its recorded history on 2027-01-05
    Then the recorded result still carries "RES-2026.12" and "R-RES-04"
    Then the replay reads the recorded activity result and never calls RuleEvaluator again
    Then the replay reaches the same activity path and the same state move

  Scenario: AC5 Temporal unavailable keeps the case event in the outbox
    Given the Temporal frontend is unreachable
    When the outbox sender delivers "EV-CASE-0777-05"
    Then WorkflowGateway.signal fails with MSG-P3-036
    Then outbox event "EV-CASE-0777-05" stays in the outbox and its delivery is RETRYING with the next attempt time
    Then the sender retries on its schedule
    When Temporal is available at the next attempt
    Then the signal is delivered and the delivery is DELIVERED

  Scenario: AC6 The skeleton runs behind the flag with no live case
    Given rwb.p3.temporal is off in DEV
    When the application starts
    Then no worker is registered on "rwb-platform" and ReferenceCaseWorkflow is not deployed
    When the flag is on and the reference harness starts "ref-case-RW-2026-000777" with synthetic "true"
    Then the skeleton runs the four steps with no live case
    Then no recovery_case row outside the synthetic fixture is read or written
    Then the workflow ID starts "ref-case-" and never "case-"
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Workflow code is deterministic: no clock, random or I/O; Drools is called only inside EvaluateRulesActivity | D-RCV-36 T7; ADR-011 |
| BR2 | The order is signal, evaluate, decision log, state; no state row is written without its decision log entry | REQ-DRI-005; Principle 5; R-UNI-39 |
| BR3 | Every activity is idempotent by the event idempotency key; a retry gives one row | REQ-DRI-005; R-UNI-40 |
| BR4 | The package version is chosen at evaluation time, pinned in RuleResult and written to the decision log; replay uses the recorded result | D-RCV-36 T7; R-UNI-38 |
| BR5 | Payloads are encrypted by PdpaPayloadCodec; history and logs hold references and codes only | D-RCV-36 T1; NFR-034 |
| BR6 | When Temporal is unavailable the signal fails with MSG-P3-036 and the outbox event stays for retry | REQ-DRI-007; RWB-TE-006 |
| BR7 | The reference skeleton is test-only: it runs only under `rwb.p3.temporal` and only with a synthetic case | D-RCV-36 T1; ADR-011 |
| BR8 | Retry policy: initial interval 1s, backoff 2, max attempts 10; NoPackageInForce is non-retryable | D-RCV-36 T1, T7 |
| BR9 | State change goes through ApplyStateActivity and the P3 case state service; no direct table write | REQ-DRI-005; D-RCV-36 T1 |

### 9. State transitions

This story changes no live case. It writes the route state of the synthetic fixture through the P3 service and moves the workflow through its own states.

| From | Event | Condition | To |
|---|---|---|---|
| RUNNING | CaseEvent | Evaluate, log and apply all succeed | COMPLETED |
| RUNNING | CaseEvent | Decision log write fails after 10 attempts | FAILED |
| RUNNING | CaseEvent | NoPackageInForce | FAILED, no retry |
| IN_FCR_QUEUE | CASE_PICKED_UP | R-RES-04 fires | WITH_FCR_OFFICER |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs ReferenceCaseWorkflow and its three activities |
| SY-RULES, Drools evaluator | Evaluates the package inside EvaluateRulesActivity |
| SY-DECLOG, decision log writer | Writes the entry inside WriteDecisionLogActivity |
| RW-PLATADM, platform administrator | Runs the worker and reads the Temporal Web UI (Platform administration CRUD) |
| RW-AUDIT, internal audit | Reads the recorded history with encrypted payloads (Platform administration R) |
| RW-COE, center of excellence analyst | Owns the RESTRUCTURE version used by the reference |
| No delegation of authority level applies | The skeleton takes no credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through the P7 writer |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write, read |
| DF-OPS-189 to DF-OPS-197 | outbox_event | all fields | Read, by the relay |
| DF-OPS-198 to DF-OPS-206 | outbox_delivery | all fields | Read and write status, through RWB-TE-006 |
| DF-CAS-001 | recovery_case | id | Read, synthetic fixture only |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-007 | recovery_case | route_state | Write, through the P3 case state service |

Field IDs are those in the Logical Data Model and Data Dictionary. The skeleton writes no table of its own and no new field. The fixture row is inserted by the test harness in DEV and SIT only and removed after the test.

### 12. Contract

**No Workbench endpoint.** The skeleton is started by the reference test harness in DEV and SIT only; it has no REST path, no schedule and no admin operation.

**Workflow interface** (package `recovery.casewf.workflow.reference`)

```java
@WorkflowInterface
public interface ReferenceCaseWorkflow {
    @WorkflowMethod void run(ReferenceCaseInput input);
    @SignalMethod void onCaseEvent(CaseEventSignal event);
}
// ReferenceCaseInput: caseId, packageCode, businessDate, synthetic (true only)
// CaseEventSignal: eventId, caseId, eventType, occurredAt, idempotencyKey, synthetic
```

**Activities** (package `recovery.casewf.workflow.reference.activities`)

```java
RuleResult EvaluateRulesActivity.evaluate(String packageCode, CaseFacts facts, LocalDate onDate);
DecisionLogRef WriteDecisionLogActivity.write(DecisionLogRequest request);   // throws DecisionLogUnavailableException
void ApplyStateActivity.apply(CaseStateChange change, String idempotencyKey); // returns the first result when the key exists
```

**Signal path.** `CaseEventSignalRelay` implements the RWB-TE-006 `OutboxConsumer` for the case event types and calls `WorkflowGateway.signal(workflowId, "CaseEvent", payload)` from RWB-E1-071. A failed call returns FAILED and leaves the delivery for the next attempt.

**Retry policy**

| Item | Value |
|---|---|
| Initial interval | 1 second |
| Backoff coefficient | 2 |
| Maximum attempts | 10 |
| Non-retryable | NoPackageInForce |
| Applies to | EvaluateRulesActivity, WriteDecisionLogActivity, ApplyStateActivity |

**Published interfaces called**

```java
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate);  // P3
RuleRow RuleCatalog.row(String ruleId, String packageVersion);                          // P3
DecisionLogRef DecisionLogWriter.write(DecisionLogRecord record);                       // P7
void WorkflowGateway.signal(String workflowId, String signal, Object payload);           // P3
```

No events are published by the skeleton; the outbox events it reads belong to RWB-TE-006.

### 13. Solution plan

**Package.** `recovery.casewf.workflow.reference` and `.activities`; the relay in `recovery.integration.outbox.reference`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReferenceCaseWorkflow | Workflow (test-only scope) | Waits for CaseEvent, calls the three activities in order, completes |
| EvaluateRulesActivity | Activity | Calls RuleEvaluator and returns RuleResult; reads no case row and writes none |
| WriteDecisionLogActivity | Activity | Calls DecisionLogWriter in its own transaction and returns the entry reference |
| ApplyStateActivity | Activity | Calls the P3 case state service with the idempotency key; one state row |
| CaseEventSignal | Record | eventId, caseId, eventType, occurredAt, idempotencyKey, synthetic |
| CaseEventSignalRelay | Outbox consumer | Reads the delivery, signals the workflow, leaves the event on failure |
| ActivityRetryPolicies | Configuration | Initial 1s, backoff 2, max attempts 10, non-retryable NoPackageInForce |
| ReferenceCaseFixture | Test fixture | Synthetic case row and RESTRUCTURE version for DEV and SIT |
| ReferenceCaseWorkflowTest | Test | Time-skipping, signal order, failure and replay tests |
| No controller | - | The skeleton has no endpoint |

**Database.** No migration and no new table. The skeleton writes `decision_log_entry` through RWB-E1-027 and the case route state through the P3 case state service. The fixture is a JSON seed in the test resources; it is inserted and removed by the harness.

**Configuration and reference data**

- Task queue `rwb-platform` and workflow ID prefix `ref-case-` for the skeleton; Epic 3 case workflows use `rwb-case` and `case-{caseId}`.
- Retry values of section 12 (assumed; confirmed with DL11).
- `rwb.p3.temporal` and `rwb.p3.drools` flags.
- The RESTRUCTURE version is owned by RW-COE.

**Build steps**

1. Define ReferenceCaseWorkflow, ReferenceCaseInput and CaseEventSignal; test that no activity runs before the signal (AC1).
2. Build EvaluateRulesActivity against RuleEvaluator; test the rule ID and package version in the result (AC1, AC4).
3. Build WriteDecisionLogActivity; test the refusal when the store is down (AC2).
4. Build ApplyStateActivity with the idempotency key; test the timeout after commit and the retry (AC3).
5. Add ActivityRetryPolicies and the NoPackageInForce do-not-retry rule; test the failure path (AC2).
6. Build CaseEventSignalRelay and test the Temporal-unavailable path with the outbox (AC5).
7. Add the flag checks and the synthetic guard; test AC6 and the worker registration.
8. Add the replay test with a recorded history and a later package version (AC4).

**Feature flag.** `rwb.p3.temporal`. Off: no worker on `rwb-platform`, ReferenceCaseWorkflow is not deployed and the relay does not run; outbox deliveries stay PENDING. Nothing else changes.

**Done when.** The tests in section 16 pass, a recorded reference history replays with the same path, and SIT shows no live case read or written by the skeleton.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-036 | The Temporal frontend is unreachable at signal time | The workflow service is not available. Try again in a few minutes. |
| MSG-P7-003 | The decision log write fails | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No package is in force at evaluation time (NoPackageInForce) | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-009 | The decision record is refused for a missing field | The decision record was refused: {field} is missing or not valid. |

MSG-P3-027 is not retried by ActivityRetryPolicies; the workflow fails at once. Thai text for each message follows DL10.

### 15. Screens and states

No screen in this story. The reference workflow is read in the Temporal Web UI by RW-PLATADM and RW-AUDIT, by workflow ID "ref-case-RW-2026-000777"; payloads are decoded only through the codec server (RWB-E2-038). The workflow states RUNNING, COMPLETED and FAILED and the activity attempt count are shown there. SCR-44 Interface and job monitor is not used.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-043-01 | AC1, BR1, BR2 | System | Signal EV-CASE-0777-01, R-RES-04, RES-2026.12 |
| TC-E2-043-02 | AC2, BR2, BR9 | System | Decision log store unavailable |
| TC-E2-043-03 | AC3, BR3 | Resilience | ApplyStateActivity timeout after commit, key CASE_EVENT:EV-CASE-0777-03 |
| TC-E2-043-04 | AC4, BR4 | System | Replay on 2027-01-05 with RES-2027.01 in force |
| TC-E2-043-05 | AC5, BR6 | System | Temporal frontend unreachable, then available |
| TC-E2-043-06 | AC6, BR7 | System | Flag off, then on with a synthetic case |
| TC-E2-043-07 | AC6, BR7, BR8 | Operational | Worker registration and task queue rwb-platform with the flag off and on; no live case |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. Action text, owner role and timer come from rule packages; retry values are configuration.
- No personal data in logs, tests, workflow history or prompts. Payloads are encrypted by PdpaPayloadCodec and the reference case is synthetic.
- No read of another module's tables; ACE data only through recovery.v_ace_* views.
- Workflow code is deterministic: no clock, random or I/O; every call to Drools, the decision log or the case service is in an activity.
- The decision log entry is written before the state change; no state row without its entry.
- Every activity is idempotent by the event key; a retry never writes a second row.
- The skeleton is test-only: it never runs against a live case and never writes a non-synthetic case row.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision is recorded with the rule and version that made it | Epic 2, 3.2; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-RES-04; R-UNI-38 | TC-E2-043-01, TC-E2-043-04 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Epic 2, 3.2; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-39 | TC-E2-043-02, TC-E2-043-03 |
| REQ-CWC-016 | Rules are evaluated by Drools from a versioned package | Epic 2, 3.2; Program, 5.3 | FEAT-DRI-07 | All recovery processes | R-RES-04 | TC-E2-043-01, TC-E2-043-04, TC-E2-043-05 |

### 19. Out of scope

- The case workflows, their timers and their outbound chains (Epic 3).
- Workflow versioning and the replay test gate (RWB-E2-040).
- The worker, the payload codec and the smoke workflow (RWB-E1-071).
- Rule package authoring and approval (RWB-E1-073); the Epic 2 package content (RWB-E2-042).
- The outbox sender schedule and the consumer list (RWB-TE-006).
- The Temporal platform, its observability and its DR (RWB-E1-070, RWB-E2-037, RWB-E2-039).
- The case lifecycle and the full state model (Epic 3).
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
| DF-ACE-193 | v_ace_valuation | appraisal_date | Read (X7 collateral event inputs) |
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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

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
