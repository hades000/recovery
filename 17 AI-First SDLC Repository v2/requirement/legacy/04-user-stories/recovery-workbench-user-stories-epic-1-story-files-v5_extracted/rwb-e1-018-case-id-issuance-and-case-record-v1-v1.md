<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 018 Case ID issuance and case record v1 v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 018 Case ID issuance and case record v1 v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-018 Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-018 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-01 Generate the case ID; FEAT-CWC-02 Create one case per customer and product; FEAT-CWC-03 Hold the case state in the ACE database; FEAT-CWC-04 Apply the entry rule at 90 days past due; FEAT-CWC-05 Apply the exclusion rules as data; FEAT-CWC-20 Expose the workflow admin API; FEAT-CWC-21 Log every workflow event |
| Requirement IDs | REQ-CWC-001, REQ-CWC-002, REQ-CWC-003, REQ-CWC-004, REQ-CWC-005, REQ-CWC-016, REQ-CHO-004 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
| L3 process | 6.1 Take over the case at 90 days past due |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-016, RWB-E1-027, RWB-E1-042 |
| Status | Ready for build |

## 1. Story

As a **product owner**, I want **every account at 90 days past due or more that is not excluded placed on one recovery case per customer and product, with a case ID in the form RW-YYYY-NNNNNN issued at creation and never reused, a status and its linked accounts, created by rule from the daily load**, so that **every team, letter and document refers to one case ID**.

## 2. Business rationale

Recovery teams keep their own lists today, so one account can be on several trackers under different references, and some accounts at 90 days past due have no owner at all (control CTL-01 answers this audit finding). This story creates the case by rule the morning after the account reaches 90 days past due, blocks excluded accounts with a logged reason, and gives the case an ID that every later document carries. It meets REQ-CWC-001 to REQ-CWC-005 and REQ-CWC-016, and supports reconciliation REC-01 (accounts at 90 days past due against open cases, zero unexplained).

## 3. Preconditions

- RWB-E1-016 is done: the account, arrears and party data products are readable by SY-CASEWF through the P1 published interface.
- RWB-E1-027 is done: the decision log writer is available.
- RWB-E1-042 is done: parameter `case.entry.dpd` = 90 is in force (DL16).
- The exclusion rows (rule table EXCLUSION) are loaded with reason codes DECEASED, FRAUD, BANKRUPTCY, ACTIVE_PLAN and OPEN_DISPUTE (REQ-CWC-004).
- The exposure band table is served by the reference data service (RWB-E1-043, LOV-EXPOSURE).
- JOB-01 has passed its load checks for the business date and published LoadCompleted (EV-26).
- The job runs as SY-CASEWF. Readers hold Case record R (roles.txt permission matrix).

## 4. Flow

1. JOB-01: publishes LoadCompleted for source COLLINS and business date 2026-12-01.
2. CaseCreationJob (JOB-02): starts on LoadCompleted and reads the entry threshold parameter `case.entry.dpd`.
3. CaseCreationJob: asks the P1 interface for every account with days_past_due at or above 90 on the business date that has no open case link.
4. EntryRuleEvaluator (SY-RULES): evaluates the exclusion rows in force for each account; an excluded account gets an exclusion record with the reason code, rule ID and version, and no case.
5. CaseGrouping: groups the remaining accounts by primary customer and product group; an existing open case for the same pair receives the new account link instead of a new case.
6. CaseNumberIssuer: takes the next number from the sequence for the entry year and formats RW-2026-000123.
7. CaseCreationService: in one transaction writes recovery_case with status NEW, case_account rows, the BORROWER case_party row and CaseCreated (EV-01) in the outbox.
8. CaseCreationService: as the last step before commit, calls DecisionLogWriter.write with decision code "D6", final call "CASE_CREATED", the entry rule version and the inputs; a failed write rolls the transaction back.
9. CaseCreationJob: records counts (accounts read, excluded, linked, created, failed) on the job record; JOB-03 starts after it.
10. Case owner: opens the case through GET /cases/{caseId} and its accounts through GET /cases/{caseId}/accounts.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The account matches an exclusion row | No case; exclusion record with reason code and rule version | None | AC2, AC6 |
| X2 | The account's customer already has an open case for the same product | The account is linked to that case; no new case | None | AC3 |
| X3 | Days past due is 89 | No case; the account is read again the next day | None | AC7 |
| X4 | JOB-02 runs again for the same business date | No duplicate case, link or number | None | AC8 |
| X5 | The COLLINS load was refused or is late | JOB-02 does not start; no case from stale data; runs after the next good load | MSG-P1-001 | AC9 |
| X6 | Decision log write fails | The case is not created and no number is consumed by a visible case; the account is retried in the next run | MSG-P7-003 | AC10 |
| X7 | The yearly number range RW-2026-999999 is used | Creation stops for the year's remaining accounts; incident raised | MSG-P3-025 | AC11 |
| X8 | The same customer has a Mortgage and a hire purchase account at 90 days past due | Two cases, one per product | None | AC12 |
| X9 | A role without Case record R reads a case | Refused with 403 | MSG-P4-002 | Access test TC-E1-018-13 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the data products (RWB-E1-016), the decision log writer (RWB-E1-027) and the parameter service (RWB-E1-042); allocation follows in RWB-E1-020 |
| Negotiable | Threshold, exclusion reasons and exposure bands are data values; the story fixes the behavior |
| Valuable | Gives about 28,100 accounts at 90 days past due one case each at go-live (DL15) |
| Estimable | One job, one numbering service, one entry evaluator, two read endpoints |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Case ID issuance and case record v1

  Background:
    Given parameter "case.entry.dpd" is 90
    Given the exclusion rows version "EXCL-2026.11" are in force
    Given the business date is 2026-12-01
    Given the COLLINS load for 2026-12-01 has passed its checks

  Scenario: AC1 Case created at 90 days past due
    Given account A-5001 of customer P-0101, product group "HIRE_PURCHASE", reaches 90 days past due in the load with no exclusion
    Given the last case number issued in 2026 is RW-2026-000122
    When the entry rule runs
    Then case RW-2026-000123 exists with status "NEW", no stage code and entry date 2026-12-01
    Then the system links account A-5001 as the primary account and P-0101 as "BORROWER"
    Then the system publishes caseCreated with case number RW-2026-000123

  Scenario: AC2 Exclusion applied
    Given account A-5002 at 92 days past due with tdr_flag = true
    When the entry rule runs
    Then the system creates no case for A-5002
    Then an exclusion record holds account A-5002, reason "ACTIVE_PLAN", the exclusion rule ID and version "EXCL-2026.11"

  Scenario: AC3 One case per customer and product
    Given customer P-0102 has two hire purchase accounts A-5003 and A-5004, both at 95 days past due
    When the entry rule runs
    Then one case exists for P-0102 and "HIRE_PURCHASE" with both accounts linked
    Then total outstanding at entry is the sum of the two balances, THB 412,350.00

  Scenario: AC4 ID never reused
    Given case RW-2026-000123 was closed on 2026-12-15
    When a new case is created on 2026-12-16
    Then it receives RW-2026-000124
    Then case RW-2026-000123 is still returned by a search on its case number

  Scenario: AC5 State model as data
    Given the list LOV-CASE-STATUS gains the value "WAITING_COURT" through a list load with valid from 2027-01-01
    When a case moves to "WAITING_COURT" on 2027-01-02
    Then the case service accepts the value without a code change
    Then the decision log entry for the move carries the list version in force

  Scenario: AC6 Exclusion rules as data
    Given the exclusion rows include reason "OPEN_DISPUTE"
    When account A-5005 at 90 days past due with an open dispute arrives
    Then the system creates no case
    Then the exclusion record for A-5005 holds reason "OPEN_DISPUTE"

  Scenario: AC7 The entry threshold boundary
    Given account A-5006 at 89 days past due and account A-5007 at 90 days past due, both with no exclusion
    When the entry rule runs
    Then the system creates a case for A-5007
    Then the system creates no case for A-5006

  Scenario: AC8 A repeated run creates nothing new
    Given JOB-02 has created case RW-2026-000125 for account A-5008 on 2026-12-01
    When JOB-02 runs again for 2026-12-01
    Then account A-5008 has one case link
    Then the system issues no case number in the second run

  Scenario: AC9 No cases from a refused load
    Given the COLLINS load for 2026-12-02 was refused at the control total check
    When the morning schedule runs
    Then JOB-02 does not start for 2026-12-02
    Then the job monitor shows MSG-P1-001 for the account data product
    Then JOB-02 runs for 2026-12-02 after the next load passes

  Scenario: AC10 The decision log write fails
    Given the decision log store is unavailable
    When the entry rule runs for account A-5009
    Then no case exists for A-5009
    Then the job record lists A-5009 as failed with MSG-P7-003
    Then the system takes A-5009 again in the next run

  Scenario: AC11 The yearly number range is used up
    Given the last case number issued in 2026 is RW-2026-999999
    When account A-5010 qualifies for a new case on 2026-12-30
    Then the system creates no case for A-5010
    Then the job record carries MSG-P3-025 with year 2026
    Then the system raises an incident to the platform administrator

  Scenario: AC12 Two products give two cases
    Given customer P-0103 has mortgage account A-5011 and hire purchase account A-5012, both at 91 days past due
    When the entry rule runs
    Then two cases exist for P-0103, one with product group "MORTGAGE" and one with "HIRE_PURCHASE"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An account enters recovery when days past due is at or above the entry threshold | Parameter case.entry.dpd = 90; DL16 |
| BR2 | One case per customer and product, with every qualifying account linked | DL17; REQ-CWC-003 |
| BR3 | An account matching an exclusion row gets no case; the reason is recorded | Exclusion rows (rule table EXCLUSION); REQ-CWC-004 |
| BR4 | The case number is RW, the entry year and a six-digit number from a yearly sequence; it is issued once and never reused | recovery_case.case_no (DF-CAS-002); uk_recovery_case |
| BR5 | A new case has status NEW and no owner until allocation | casemodel.txt Case status "New" |
| BR6 | Status values are read from the list, not from code | LOV-CASE-STATUS; Principle 1 |
| BR7 | No case is created from a load that failed its checks | CTL-02; JOB-02 "No cases from stale data" |
| BR8 | Every case creation writes its decision log entry in the same transaction; a failed write rolls the creation back | Principle 5; R-UNI-39 |
| BR9 | Exposure band is set from the total outstanding at entry using the band table in force | recovery_case.exposure_band (DF-CAS-015); LOV-EXPOSURE |
| BR10 | A case created on bad data is canceled by rule, never deleted | R-UNI-16 (Epic 2 handling) |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | LoadCompleted (EV-26), entry rule | days_past_due at or above 90, no exclusion, no open case for the customer and product | New |
| New | Allocation rule matched | Handled by RWB-E1-020 | Assigned |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD | Publishes LoadCompleted; no case write in this story |
| SY-CASEWF | Creates the case, the account links and the party link (Case record CRU) |
| SY-RULES | Evaluates the exclusion rows (Rules and parameters R) |
| SY-DECLOG | Writes the decision log entry (Decision log C) |
| RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL and every role with Case record R | Read the case and its accounts, within their scope |
| RW-COE | Owns the exclusion rows and the threshold parameter; loads them through RWB-E1-029 and RWB-E1-042 |
| RW-REFADM | Has no Case record right; refused on the read endpoints |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Write |
| DF-CAS-024 to DF-CAS-029 | case_account | all fields | Write |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |
| DF-ACC-001 | loan_account | id | Read |
| DF-ACC-012 | loan_account | total_balance | Read |
| DF-ACC-014 | loan_account | days_past_due | Read |
| DF-ACC-019 | loan_account | tdr_flag | Read |
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-ACC-029 | loan_account | dispute_open | Read |
| DF-PTY-001 | party | id | Read |
| DF-PTY-011 | party | deceased_flag | Read |
| DF-PTY-012 | party | bankruptcy_flag | Read |
| DF-PTY-021 | party | fraud_flag | Read |
| DF-CAS-056 to DF-CAS-061 | case_entry_exclusion | all fields | Write |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-007 | rule_row | condition_expr | Read |
| DF-REF-052 | rule_row | rule_table | Read |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | LoadCompleted (EV-26) for source COLLINS with all checks passed |
| Job name | JOB-02 Case creation |
| Schedule | Daily after JOB-01 |
| Input | Account snapshots at or above the threshold from the P1 interface; exclusion rows in force; exposure band table |
| Output | recovery_case, case_account, case_party and case_entry_exclusion rows; decision log entries; job record counts |
| Events published | CaseCreated (EV-01: caseId, caseNo, productGroup, accounts, businessDate) |
| Idempotency key | accountId and businessDate for the entry decision; uniqueness of an open case per primary customer and product group |
| Restart | Rerun from the job monitor; accounts already linked or excluded for the date are skipped; a failed account is retried |

**Endpoints**

| Item | GET /api/recovery/v1/cases/{caseId} | GET /api/recovery/v1/cases/{caseId}/accounts |
|---|---|---|
| Request | Path caseId (uuid) | Path caseId (uuid) |
| Response | Case: id, caseNo, productGroup, primaryCustomerId, status, entryDate, dpdAtEntry, exposureBand, totalOutstandingAtEntry, deviationOpen, legalHold | CaseAccount[]: id, caseId, accountId, isPrimary, linkedFrom, linkedTo |
| Errors | 401 no session (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 store down | Same |
| Authorization | Case record, right R, scope applied | Case record, right R, scope applied |
| Idempotency | Not applicable | Not applicable |

GET /api/recovery/v1/cases is used for the case number search in AC4 with a new query parameter caseNo (see additions).

**Published interfaces**

```java
// P3, package recovery.casewf.casecreation (published)
public interface CaseRecordService {
    Optional<CaseView> findByCaseNo(String caseNo);
    Optional<CaseView> findOpenCase(UUID primaryCustomerId, String productGroup);
}

// P1, used by this story (RWB-E1-016)
public interface RecoveryDataQuery {
    List<AccountEntrySnapshot> accountsAtOrAbove(int daysPastDue, LocalDate businessDate);
}
public record AccountEntrySnapshot(UUID accountId, UUID primaryPartyId, String productGroup,
        String regionCode, int daysPastDue, BigDecimal totalBalance, boolean tdrFlag,
        boolean disputeOpen, boolean deceased, boolean bankrupt, boolean fraud, LocalDate dataAsOf) {}

// P7, used by this story (RWB-E1-027)
// package recovery.decision.writer; called inside the caller's transaction as the last step before commit
public interface DecisionLogWriter {
    DecisionLogEntryRef write(DecisionLogRecord record)
        throws DecisionLogRecordInvalidException, DecisionLogUnavailableException;
}
```

## 13. Solution plan

**Package.** `recovery/casewf/casecreation`, Java package `recovery.casewf.casecreation`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseCreationJob | Job | JOB-02; listens for LoadCompleted; runs the entry rule per account; writes job counts |
| EntryRuleEvaluator | Service | Applies the threshold and the exclusion rows; returns ENTER or EXCLUDE with reason and rule version |
| CaseGrouping | Service | Groups accounts by primary customer and product group; finds an open case to link to |
| CaseNumberIssuer | Service | Draws from sequence case_no_seq_YYYY and formats RW-YYYY-NNNNNN; refuses above 999999 |
| CaseCreationService | Service | Decision log write, then case, account links, party link and outbox event in one transaction |
| CaseAndWorkflowRepository | Repository | recovery_case, case_account, case_party, case_entry_exclusion |
| CaseAndWorkflowController | Controller | GET /cases/{caseId}, GET /cases/{caseId}/accounts, caseNo search on GET /cases |
| CaseStatusCatalog | Service | Reads LOV-CASE-STATUS through the P4 list interface; no Java enum of statuses |
| ExclusionRuleTable | Rule table | Rule rows with rule table EXCLUSION, read through RuleTableReader (P4) |

**Database**

- Writes recovery_case (all columns), case_account (all columns), case_party (all columns), case_entry_exclusion (new), outbox.
- Constraint: partial unique index `ux_case_open_customer_product ON recovery_case (primary_customer_id, product_group) WHERE closed_date IS NULL`.
- Constraint: unique `case_account (account_id) WHERE linked_to IS NULL`, so an account is on one open case.
- Migration in this story: `V018_1__case_creation.sql` creates table case_entry_exclusion (id, account_id, business_date, reason_code, rule_id, rule_version, standard columns, unique (account_id, business_date)), the yearly sequences case_no_seq_2026 and case_no_seq_2027 (created ahead by the job each December), and the two indexes above.

**Configuration and reference data**

- Parameter `case.entry.dpd` = 90 (RWB-E1-042; DL16), owner RW-COE.
- Exclusion rows "EXCL-2026.11" with the five reason codes, loaded by RW-COE through RWB-E1-029.
- LOV-EXPOSURE bands and LOV-CASE-STATUS from the reference data service (RWB-E1-043).

**Build steps**

1. CaseNumberIssuer with the yearly sequence and the 999999 limit; unit and integration tests for AC1, AC4, AC11.
2. EntryRuleEvaluator over the threshold parameter and the exclusion rows; tests for AC2, AC6, AC7.
3. CaseGrouping with the open case lookup; tests for AC3, AC12.
4. CaseCreationService: the case, links and outbox row, then the decision log write as the last step in the same transaction; test for AC10.
5. CaseCreationJob on LoadCompleted with idempotent skip; tests for AC8, AC9.
6. CaseStatusCatalog reading statuses from the list; test for AC5.
7. Controller endpoints with access check and scope; caseNo search; access test.

**Feature flag.** `rwb.p3.casecreation`. Off: JOB-02 does not create cases.

**Done when.** The tests in section 16 pass and REC-01 shows zero unexplained difference on the SIT data set.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | JOB-02 waiting for a passed load | {product} is from {date}. Today's load has not arrived. |
| MSG-P7-003 | Decision log write failed for an account | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-025 | Yearly case number range used up | Case numbers for {year} are used up. New cases are on hold until the range is extended. |
| MSG-P4-002 | Read without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

## 15. Screens and states

SCR-02 Case list (Loading; empty; list; filtered) shows each new case with its case number, product, status NEW and entry date. SCR-03 Case record (Loading; read only) shows the case and its linked accounts. The full read-only view is RWB-E1-023.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-018-01 | AC1, BR1, BR4, BR5 | System | Account A-5001 at 90 days past due, last number RW-2026-000122 |
| TC-E1-018-02 | AC2, BR3 | System | Account A-5002 with tdr_flag = true |
| TC-E1-018-03 | AC3, BR2 | System | Customer P-0102 with two HP accounts |
| TC-E1-018-04 | AC4, BR4 | System | Closed case RW-2026-000123 |
| TC-E1-018-05 | AC5, BR6 | System | New status value WAITING_COURT in LOV-CASE-STATUS |
| TC-E1-018-06 | AC6, BR3 | System | Account A-5005 with an open dispute |
| TC-E1-018-07 | AC7, BR1 | System | Accounts at 89 and 90 days past due |
| TC-E1-018-08 | AC8 | System | JOB-02 run twice for 2026-12-01 |
| TC-E1-018-09 | AC9, BR7 | System | Load refused at the control total check |
| TC-E1-018-10 | AC10, BR8 | System | Decision log store unavailable for one account |
| TC-E1-018-11 | AC11, BR4 | System | Sequence at 999999 |
| TC-E1-018-12 | AC12, BR2 | System | Customer P-0103 with a mortgage and an HP account |
| TC-E1-018-13 | Access | Access | RW-REFADM reads GET /cases/{caseId} and is refused with MSG-P4-002 |
| TC-E1-018-14 | Principle 5 | Resilience | Decision log write forced to fail for the whole run |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the threshold, the exclusion reasons, the bands and the status list are data.
- No personal data in logs, tests, events or prompts. Test data uses synthetic account and customer IDs only.
- No read of another module's tables: account and party data come through RecoveryDataQuery (P1); rules through RuleTableReader (P4).
- The case number is printed on every outbound document; other modules take it from CaseRecordService, never from a copy.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-04 | 6.1 | R-UNI-16 | TC-E1-018-01, TC-E1-018-07, TC-E1-018-09 |
| REQ-CWC-002 | Case ID RW-YYYY-NNNNNN, never reused | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-01 | 6.1 | None | TC-E1-018-01, TC-E1-018-04, TC-E1-018-11 |
| REQ-CWC-003 | One case per customer and product | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-02 | 6.1 | R-UNI-17 | TC-E1-018-03, TC-E1-018-08, TC-E1-018-12 |
| REQ-CWC-004 | Exclusion rules as data | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-05 | 6.1 | None | TC-E1-018-02, TC-E1-018-06 |
| REQ-CWC-005 | State model with one state at a time | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-03 | 6.1 | None | TC-E1-018-05 |
| REQ-CWC-016 | Every workflow event logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-21 | 6.1 | R-UNI-39 | TC-E1-018-10, TC-E1-018-14 |
| REQ-CHO-004 | One agreed hand-over point in days past due for every rule and report | Business Requirements Epic 1, section 3.3 | FEAT-CWC-01, FEAT-CWC-02, FEAT-CWC-03, FEAT-CWC-04, FEAT-CWC-05, FEAT-CWC-20, FEAT-CWC-21 | 6.1 Take over the case at 90 days past due | None | TC-E1-018-01 |

## 19. Out of scope

- Allocation to a queue and an owner (RWB-E1-020).
- Prescription date at creation (RWB-E1-028).
- Hand-over of collections history from EFS (RWB-E2-001).
- Merging a duplicate case (R-UNI-17) and canceling a case created in error (R-UNI-16), Epic 2.
- The read-only case record view (RWB-E1-023).
