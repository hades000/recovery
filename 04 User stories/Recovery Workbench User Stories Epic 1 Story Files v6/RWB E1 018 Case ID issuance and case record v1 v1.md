# RWB-E1-018 Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group, 15 November 2026.

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
| Decision | D6 entry; D-RCV-35 (U1, U4); ADR-010; DL43 open |
| Priority | Must |
| Depends on | RWB-E1-001, RWB-E1-016, RWB-E1-027, RWB-E1-042, RWB-E1-069 |
| Status | Ready for build, the batch gate behind a flag until RWB-ACE-001 lands (DL43) |

## 1. Story

As a **product owner**, I want **every account at 90 days past due or more in the ACE account view that is not excluded placed on one recovery case per customer and product, with a case ID in the form RW-YYYY-NNNNNN issued at creation and never reused, a status and its linked accounts read from ACE by business key, created by rule when the ACE ALS batch for the business date is complete**, so that **every team, letter and document refers to one case ID**.

## 2. Business rationale

Recovery teams keep their own lists today, so one account can be on several trackers under different references, and some accounts at 90 days past due have no owner at all (control CTL-01 answers this audit finding). Under D-RCV-35 the Workbench loads nothing: ACE ingests the ALS account, the SCBPDM customer and the EFS collections history, and P3 reads them through `v_ace_account`, `v_ace_customer` and `v_ace_ca_relation`. This story creates the case by rule when the ALS batch for the business date reaches COMPLETED in `v_ace_batch_status`, blocks excluded accounts with a logged reason, and gives the case an ID that every later document carries. It meets REQ-CWC-001 to REQ-CWC-005 and REQ-CWC-016, and supports reconciliation REC-01 (accounts at 90 days past due against open cases, zero unexplained) and REC-05 (every `account_key`, `person_key` and `primary_person_key` on a P3 table resolves to its ACE view row).

## 3. Preconditions

- RWB-E1-001 is done: `recovery_case`, `case_account`, `case_party` and `case_entry_exclusion` exist in the V0001 baseline.
- RWB-E1-069 is done: the Section A views exist, including `v_ace_account`, `v_ace_customer` and `v_ace_ca_relation`. `v_ace_batch_status` is a Section B view, so the batch gate stays behind its flag until RWB-ACE-001 lands (DL43).
- RWB-E1-016 is done: the P1 ACE source query is published and returns the view rows by business key.
- RWB-E1-027 is done: the decision log writer is available.
- RWB-E1-042 is done: parameter `case.entry.dpd` = 90 is in force (DL16).
- The exclusion rows (rule table EXCLUSION) are loaded with reason codes DECEASED, FRAUD, BANKRUPTCY, ACTIVE_PLAN and OPEN_DISPUTE (REQ-CWC-004). Their inputs are read from `v_ace_account.tdr_flag`, `v_ace_customer.deceased_flag`, `recovery.account_ext.dispute_open` and `recovery.party_ext.deceased_override`, `.bankruptcy` and `.fraud_flag`, all by business key.
- The exposure band table is served by the reference data service (RWB-E1-043, LOV-EXPOSURE).
- The ALS batch for the business date is COMPLETED in `v_ace_batch_status`, and RWB-E1-015 has raised AceDataReady (EV-26).
- JOB-02 runs as `recovery_svc`, which holds SELECT on `recovery.v_ace_*` and no privilege on `public`. Readers hold Case record R (roles.txt permission matrix).

## 4. Flow

1. ACE: the ALS batch for business date 2026-12-01 completes, and `v_ace_batch_status` holds the row with status "COMPLETED" and `is_complete` true.
2. RWB-E1-015: raises AceDataReady (EV-26) for source ALS and business date 2026-12-01.
3. CaseCreationJob (JOB-02): starts on AceDataReady and reads the entry threshold parameter `case.entry.dpd`.
4. CaseCreationJob: reads `v_ace_account` for every account with `days_past_due` at or above 90 and `data_as_of` equal to the business date, and skips an account that already has an open `case_account` row (`linked_to` is null).
5. CaseCreationJob: for each account reads `v_ace_ca_relation` for the BORROWER `person_key` and `v_ace_customer` for that key; an account whose borrower key has no `v_ace_customer` row is not grouped and gets no case.
6. EntryRuleEvaluator (SY-RULES): evaluates the exclusion rows in force for each account over `v_ace_account.tdr_flag`, `v_ace_customer.deceased_flag`, `account_ext.dispute_open` and `party_ext`; an excluded account gets a `case_entry_exclusion` row with the reason code, rule ID and version, and no case.
7. CaseGrouping: groups the remaining accounts by the borrower `person_key` and the product group read from `v_ace_account.product_category`; an existing open case for the same pair receives a new `case_account` row with the `account_key` instead of a new case.
8. CaseNumberIssuer: takes the next number from the sequence for the entry year and formats RW-2026-000123.
9. CaseCreationService: in one transaction writes `recovery_case` with status NEW, `primary_person_key`, `dpd_at_entry`, `total_outstanding_at_entry` and the exposure band, the `case_account` rows with `account_key` and `is_primary`, the BORROWER `case_party` row with `person_key`, and CaseCreated (EV-01) in the outbox. The primary account is the linked account with the highest `total_balance` on the business date; a tie breaks on the lowest `account_key`.
10. CaseCreationService: as the last step before commit, calls DecisionLogWriter.write with decision code "D6", final call "CASE_CREATED", the entry rule version and the ALS business date; a failed write rolls the transaction back.
11. CaseCreationJob: records counts (accounts read, excluded, linked, created, failed) on the job record; JOB-03 starts after it.
12. Case owner: opens the case through GET /cases/{caseId} and its accounts through GET /cases/{caseId}/accounts.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The account matches an exclusion row | No case; `case_entry_exclusion` row with reason code and rule version | None | AC2, AC6 |
| X2 | The borrower already has an open case for the same product group | The account is linked to that case by `account_key`; no new case | None | AC3 |
| X3 | Days past due is 89 in `v_ace_account` | No case; the account is read again on the next complete ALS batch | None | AC7 |
| X4 | JOB-02 runs again for the same business date | No duplicate case, link or number | None | AC8 |
| X5 | The ALS batch for the business date is not COMPLETED | JOB-02 does not start; no case from an incomplete day; it starts when AceDataReady is raised for the date | MSG-P1-001 | AC9 |
| X6 | The decision log write fails | The case is not created and no number is consumed by a visible case; the account is retried in the next run | MSG-P7-003 | AC10 |
| X7 | The yearly number range RW-2026-999999 is used | Creation stops for the year's remaining accounts; incident raised | MSG-P3-025 | AC11 |
| X8 | The same borrower has a mortgage and a hire purchase account at 90 days past due | Two cases, one per product group | None | AC12 |
| X9 | A business key on a case or in the intake has no row in `v_ace_account` or `v_ace_customer` | The intake creates no case or party link from the missing row; an existing link is unchanged; REC-05 lists the key for the data steward and the ACE team; the key is read again on the next complete batch | None | AC13 |
| X10 | A role without Case record R reads a case | Refused with 403 | MSG-P4-002 | AC14 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the ACE views (RWB-E1-069), the P1 ACE source query (RWB-E1-016), the decision log writer (RWB-E1-027) and the parameter service (RWB-E1-042); allocation follows in RWB-E1-020 |
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
    Given v_ace_batch_status holds the ALS batch for 2026-12-01 with status "COMPLETED" and is_complete true

  Scenario: AC1 Case created at 90 days past due
    Given v_ace_account holds account A-5001 with product_category "HIRE_PURCHASE", days_past_due 90 and data_as_of 2026-12-01, with no exclusion
    Given v_ace_ca_relation holds person_key P-0101 on account A-5001 as "BORROWER" and v_ace_customer holds P-0101
    Given the last case number issued in 2026 is RW-2026-000122
    When AceDataReady is raised for ALS and 2026-12-01 and JOB-02 runs
    Then case RW-2026-000123 exists with status "NEW", no stage code, entry date 2026-12-01 and primary_person_key P-0101
    Then case_account holds account_key A-5001 on that case with is_primary true
    Then case_party holds person_key P-0101 as "BORROWER"
    Then the system publishes caseCreated with case number RW-2026-000123

  Scenario: AC2 Exclusion applied
    Given v_ace_account holds account A-5002 at days_past_due 92 with tdr_flag true
    When the entry rule runs
    Then the system creates no case for A-5002
    Then case_entry_exclusion holds account_key A-5002, business date 2026-12-01, reason "ACTIVE_PLAN", the exclusion rule ID and version "EXCL-2026.11"

  Scenario: AC3 One case per customer and product
    Given v_ace_account holds hire purchase accounts A-5003 with total_balance 300,000.00 and A-5004 with total_balance 112,350.00 for borrower P-0102, both at days_past_due 95
    When the entry rule runs
    Then one case exists for P-0102 and "HIRE_PURCHASE" with both account_keys linked
    Then total_outstanding_at_entry is the sum of the two balances, THB 412,350.00
    Then case_account holds A-5003 with is_primary true and A-5004 with is_primary false

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
    Given account A-5005 at days_past_due 90 has dispute_open true in account_ext
    When the entry rule runs
    Then the system creates no case for A-5005
    Then the exclusion record for A-5005 holds reason "OPEN_DISPUTE"

  Scenario: AC7 The entry threshold boundary
    Given v_ace_account holds account A-5006 at days_past_due 89 and account A-5007 at days_past_due 90, both with no exclusion
    When the entry rule runs
    Then the system creates a case for A-5007
    Then the system creates no case for A-5006

  Scenario: AC8 A repeated run creates nothing new
    Given JOB-02 has created case RW-2026-000125 for account A-5008 on 2026-12-01
    When JOB-02 runs again for 2026-12-01
    Then account A-5008 has one case link
    Then the system issues no case number in the second run

  Scenario: AC9 No cases before the ALS batch is complete
    Given v_ace_batch_status shows the ALS batch for 2026-12-02 with status "RUNNING" at the 09:00 cut-off
    When the morning check runs
    Then JOB-02 does not start for 2026-12-02
    Then the job monitor shows MSG-P1-001 for "DP01 Account and arrears" with date 2026-12-01
    Then JOB-02 starts for 2026-12-02 when AceDataReady is raised for ALS and 2026-12-02

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
    Given v_ace_account holds mortgage account A-5011 and hire purchase account A-5012 for borrower P-0103, both at days_past_due 91
    When the entry rule runs
    Then two cases exist for P-0103, one with product group "MORTGAGE" and one with "HIRE_PURCHASE"

  Scenario: AC13 A key with no view row is listed, never invented
    Given case RW-2026-000126 links account_key A-5013 and person_key P-0105
    Given v_ace_account has no row for A-5013 on 2026-12-01 and v_ace_customer has no row for P-0105
    When JOB-02 runs for 2026-12-01 and the intake reads the case links
    Then the system creates no case and no party link from a missing view row
    Then case RW-2026-000126 keeps its existing links unchanged
    Then REC-05 lists account_key A-5013 and person_key P-0105 for the data steward and the ACE team
    Then both keys are read again on the next complete ALS batch

  Scenario: AC14 A role without Case record R is refused
    Given user "U-5001" holds RW-REFADM, which has no Case record right
    When "U-5001" calls GET /cases/{caseId} for case RW-2026-000123
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system writes one AC-DENY event with area "CASE_RECORD" and right "R"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An account enters recovery when `days_past_due` in `v_ace_account` for the ACE business date is at or above the entry threshold | Parameter case.entry.dpd = 90; DL16; DF-ACE-018 |
| BR2 | One case per borrower `person_key` and product group, with every qualifying account linked by `account_key` | DL17; REQ-CWC-003 |
| BR3 | An account matching an exclusion row gets no case; the reason, rule ID and version are recorded in `case_entry_exclusion` | Exclusion rows (rule table EXCLUSION); REQ-CWC-004 |
| BR4 | The case number is RW, the entry year and a six-digit number from a yearly sequence; it is issued once and never reused | recovery_case.case_no (DF-CAS-002); uk_recovery_case |
| BR5 | A new case has status NEW and no owner until allocation | casemodel.txt Case status "New" |
| BR6 | Status values are read from the list, not from code | LOV-CASE-STATUS; Principle 1 |
| BR7 | No case is created before the ALS batch for the business date is COMPLETED in `v_ace_batch_status`. A late or failed batch raises AceDataLate (EV-27), and the case is created on the next complete batch | CTL-02; JOB-02 "No cases from an incomplete day"; RWB-E1-015 |
| BR8 | Every case creation writes its decision log entry in the same transaction; a failed write rolls the creation back | Principle 5; R-UNI-39 |
| BR9 | Exposure band is set from the total outstanding at entry using the band table in force | recovery_case.exposure_band (DF-CAS-015); LOV-EXPOSURE |
| BR10 | A case created on bad data is canceled by rule, never deleted | R-UNI-16 (Epic 2 handling) |
| BR11 | The case links to ACE by business key (`primary_person_key`, `account_key`, `person_key`) with no foreign key. A key with no view row is listed by REC-05 and never invented from a partial record | D-RCV-35 U4; ADR-010; REC-05 |
| BR12 | The primary account is the linked account with the highest `total_balance` on the business date; a tie breaks on the lowest `account_key` | case_account.is_primary (DF-CAS-027); Data Tier Map section 5 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | AceDataReady (EV-26), entry rule | `days_past_due` at or above 90 in `v_ace_account` for the completed ALS business date, no exclusion, no open case for the borrower and product group | New |
| New | Allocation rule matched | Handled by RWB-E1-020 | Assigned |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| recovery_svc, recovery service identity | Runs JOB-02; reads `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation` and `v_ace_batch_status`; creates the case, the account links and the party link |
| ACE batch record | Raises AceDataReady; no case write in this story |
| SY-RULES | Evaluates the exclusion rows (Rules and parameters R) |
| SY-DECLOG | Writes the decision log entry (Decision log C) |
| RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL and every role with Case record R | Read the case and its accounts, within their scope |
| RW-COE | Owns the exclusion rows and the threshold parameter; loads them through RWB-E1-029 and RWB-E1-042 |
| ACE team lead | Owns the ACE tables and columns behind `v_ace_account`, `v_ace_customer` and `v_ace_ca_relation`; reads no Workbench table |
| RW-REFADM | Has no Case record right; refused on the read endpoints |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Write |
| DF-CAS-024 to DF-CAS-029 | case_account | all fields | Write |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |
| DF-CAS-056 to DF-CAS-061 | case_entry_exclusion | all fields | Write |
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-002 | v_ace_account | account_code | Read |
| DF-ACE-010 | v_ace_account | product_category | Read |
| DF-ACE-012 | v_ace_account | branch_code | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-031 | v_ace_account | tdr_flag | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-061 | v_ace_customer | deceased_flag | Read |
| DF-ACE-084 | v_ace_ca_relation | person_key | Read |
| DF-ACE-085 | v_ace_ca_relation | account_key | Read |
| DF-ACE-086 | v_ace_ca_relation | relation_type | Read |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-EXT-001 | party_ext | person_key | Read |
| DF-EXT-003 | party_ext | deceased_override | Read |
| DF-EXT-004 | party_ext | bankruptcy | Read |
| DF-EXT-005 | party_ext | fraud_flag | Read |
| DF-EXT-027 | account_ext | account_key | Read |
| DF-EXT-028 | account_ext | dispute_open | Read |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-007 | rule_row | condition_expr | Read |
| DF-REF-052 | rule_row | rule_table | Read |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary v7. DF-ACE-* are the `recovery.v_ace_*` view fields of Physical Schema v5.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | AceDataReady (EV-26) for source ALS and the business date, raised by RWB-E1-015 from a COMPLETED row in `v_ace_batch_status` |
| Job name | JOB-02 Case creation |
| Schedule | Daily, when the ALS batch completes |
| Input | Accounts at or above the threshold from `v_ace_account` for the business date; borrower `person_key` from `v_ace_ca_relation`; customer from `v_ace_customer`; `account_ext` and `party_ext` flags; exclusion rows in force; exposure band table |
| Output | recovery_case, case_account, case_party and case_entry_exclusion rows; decision log entries; job record counts |
| Events published | CaseCreated (EV-01: caseId, caseNo, productGroup, accounts, businessDate) |
| Idempotency key | accountKey and businessDate for the entry decision; uniqueness of an open case per primary_person_key and product group |
| Restart | Rerun from the job monitor; accounts already linked or excluded for the date are skipped; a failed account is retried |

**Endpoints**

| Item | GET /api/recovery/v1/cases/{caseId} | GET /api/recovery/v1/cases/{caseId}/accounts |
|---|---|---|
| Request | Path caseId (uuid) | Path caseId (uuid) |
| Response | Case: id, caseNo, productGroup, primaryPersonKey, status, entryDate, dpdAtEntry, exposureBand, totalOutstandingAtEntry, deviationOpen, legalHold | CaseAccount[]: id, caseId, accountKey, isPrimary, linkedFrom, linkedTo |
| Errors | 401 no session (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 store down | Same |
| Authorization | Case record, right R, scope applied | Case record, right R, scope applied |
| Idempotency | Not applicable | Not applicable |

GET /api/recovery/v1/cases is used for the case number search in AC4 with a new query parameter caseNo (see additions).

**Published interfaces**

```java
// P3, package recovery.casewf.casecreation (published)
public interface CaseRecordService {
    Optional<CaseView> findByCaseNo(String caseNo);
    Optional<CaseView> findOpenCase(String primaryPersonKey, String productGroup);
}

// P1, used by this story (RWB-E1-016); every method reads recovery.v_ace_*
public interface AceSourceQuery {
    List<AccountEntrySnapshot> accountsAtOrAbove(int daysPastDue, LocalDate businessDate);
    List<AccountRelation> relationsFor(String accountKey);        // v_ace_ca_relation
    Optional<AceCustomer> customer(String personKey);             // v_ace_customer
}
public record AccountEntrySnapshot(String accountKey, String accountCode, String productGroup,
        String regionCode, int daysPastDue, BigDecimal totalBalance, boolean tdrFlag, LocalDate dataAsOf) {}
public record AccountRelation(String personKey, String relationType) {}
public record AceCustomer(String personKey, String cifNo, boolean deceased) {}

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
| CaseCreationJob | Job | JOB-02; listens for AceDataReady; checks the ALS batch row for the business date; runs the entry rule per `account_key`; writes job counts |
| EntryRuleEvaluator | Service | Applies the threshold and the exclusion rows over `v_ace_account`, `v_ace_customer`, `account_ext` and `party_ext`; returns ENTER or EXCLUDE with reason and rule version |
| CaseGrouping | Service | Groups accounts by the BORROWER `person_key` and product group; finds an open case to link to |
| CaseNumberIssuer | Service | Draws from sequence case_no_seq_YYYY and formats RW-YYYY-NNNNNN; refuses above 999999 |
| CaseCreationService | Service | Decision log write, then case, account links, primary flag, party link and outbox event in one transaction |
| AceSourceReader | Repository | Reads `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation` and `v_ace_batch_status` by business key; SELECT only |
| CaseAndWorkflowRepository | Repository | recovery_case, case_account, case_party, case_entry_exclusion, account_ext, party_ext |
| CaseAndWorkflowController | Controller | GET /cases/{caseId}, GET /cases/{caseId}/accounts, caseNo search on GET /cases |
| CaseStatusCatalog | Service | Reads LOV-CASE-STATUS through the P4 list interface; no Java enum of statuses |
| ExclusionRuleTable | Rule table | Rule rows with rule table EXCLUSION, read through RuleTableReader (P4) |

**Database**

- Writes recovery_case (all columns), case_account (all columns), case_party (all columns), case_entry_exclusion, outbox.
- Reads recovery.account_ext and recovery.party_ext by business key; no copy of an ACE row is written.
- Constraint: partial unique index `ux_case_open_customer_product ON recovery_case (primary_person_key, product_group) WHERE closed_date IS NULL`.
- Constraint: partial unique index `ux_case_account_open ON case_account (account_key) WHERE linked_to IS NULL`, so an account is on one open case.
- One `case_entry_exclusion` row per `account_key` and business date, which the job and TC-E1-018-02 assert.
- Migration in this story: `V018_1__case_creation.sql` creates the yearly sequences case_no_seq_2026 and case_no_seq_2027 (created ahead by the job each December) and the two partial unique indexes above. The four tables come from V0001 (RWB-E1-001) and no column is added for source data.

**Configuration and reference data**

- Parameter `case.entry.dpd` = 90 (RWB-E1-042; DL16), owner RW-COE.
- Exclusion rows "EXCL-2026.11" with the five reason codes, loaded by RW-COE through RWB-E1-029.
- LOV-EXPOSURE bands, LOV-CASE-STATUS and LOV-PRODUCT from the reference data service (RWB-E1-043).

**Build steps**

1. CaseNumberIssuer with the yearly sequence and the 999999 limit; unit and integration tests for AC1, AC4, AC11.
2. AceSourceReader over `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation` and `v_ace_batch_status`; test the join by `account_key` and `person_key` for AC1, AC13.
3. EntryRuleEvaluator over the threshold parameter, the exclusion rows and the extension flags; tests for AC2, AC6, AC7.
4. CaseGrouping with the open case lookup and the primary account rule; tests for AC3, AC12.
5. CaseCreationService: the case, links, primary flag and outbox row, then the decision log write as the last step in the same transaction; test for AC10.
6. CaseCreationJob on AceDataReady with the batch gate and idempotent skip; tests for AC8, AC9.
7. CaseStatusCatalog reading statuses from the list; test for AC5.
8. Controller endpoints with access check and scope; caseNo search; test for AC14.

**Feature flag.** `rwb.p3.casecreation`. Off: JOB-02 does not create cases. The batch gate reads a Section B view, so the flag is on only after RWB-ACE-001 lands and V0003 creates `v_ace_batch_status` (DL43).

**Done when.** The tests in section 16 pass and REC-01 shows zero unexplained difference on the SIT data set.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | JOB-02 waiting for a COMPLETED ALS batch | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P7-003 | Decision log write failed for an account | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-025 | Yearly case number range used up | Case numbers for {year} are used up. New cases are on hold until the range is extended. |
| MSG-P4-002 | Read without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

## 15. Screens and states

SCR-02 Case list (Loading; empty; list; filtered) shows each new case with its case number, product, status NEW and entry date, and the account number and balance read from `v_ace_account`. SCR-03 Case record (Loading; read only) shows the case and its linked accounts by `account_key`. The full read-only view is RWB-E1-023.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-018-01 | AC1, BR1, BR2, BR4, BR5, BR11, BR12 | System | `v_ace_account` A-5001 at 90 days past due, borrower P-0101, last number RW-2026-000122 |
| TC-E1-018-02 | AC2, BR3 | System | `v_ace_account` A-5002 with `tdr_flag` true |
| TC-E1-018-03 | AC3, BR2, BR12 | System | Borrower P-0102 with two HP accounts of 300,000.00 and 112,350.00 |
| TC-E1-018-04 | AC4, BR4 | System | Closed case RW-2026-000123 |
| TC-E1-018-05 | AC5, BR6 | System | New status value WAITING_COURT in LOV-CASE-STATUS |
| TC-E1-018-06 | AC6, BR3 | System | A-5005 with `dispute_open` true in account_ext |
| TC-E1-018-07 | AC7, BR1 | System | Accounts at 89 and 90 days past due in `v_ace_account` |
| TC-E1-018-08 | AC8 | System | JOB-02 run twice for 2026-12-01 |
| TC-E1-018-09 | AC9, BR7 | System | ALS batch for 2026-12-02 at status RUNNING |
| TC-E1-018-10 | AC10, BR8 | System | Decision log store unavailable for one account |
| TC-E1-018-11 | AC11, BR4 | System | Sequence at 999999 |
| TC-E1-018-12 | AC12, BR2 | System | Borrower P-0103 with a mortgage and an HP account |
| TC-E1-018-13 | AC14, BR11 | Access | RW-REFADM reads GET /cases/{caseId} and is refused with MSG-P4-002 |
| TC-E1-018-14 | Principle 5 | Resilience | Decision log write forced to fail for the whole run |
| TC-E1-018-15 | AC13, BR11 | System | Case links A-5013 and P-0105 with no view row for 2026-12-01 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the threshold, the exclusion reasons, the bands and the status list are data.
- No personal data in logs, tests, events or prompts. JOB-02 reads `account_key` and `person_key` only: no name, address or identity number is read or written. Test data uses synthetic account and customer keys only.
- ACE data only through the `recovery.v_ace_*` views: account, customer, relation and batch data come from `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation` and `v_ace_batch_status`. The recovery schema holds no foreign key into a `public` table.
- The case links to ACE by business key (`primary_person_key`, `account_key`, `person_key`) with no foreign key; REC-05 lists a key with no view row and nothing is invented from a partial record.
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
| D-RCV-35 U4 | The case links to ACE by business key and reads account, customer and relation data only through the `recovery.v_ace_*` views | Decision log, D-RCV-35 section 6.1; ADR-010 | FEAT-CWC-02 | 6.1 | ADR-010; CTL-02 | TC-E1-018-01, TC-E1-018-15 |

## 19. Out of scope

- Allocation to a queue and an owner (RWB-E1-020).
- Prescription date at creation (RWB-E1-028).
- The EFS collections history hand-over in Epic 2 (RWB-E2-001); the history itself is read from `v_ace_efs_action`, not copied.
- Merging a duplicate case (R-UNI-17) and canceling a case created in error (R-UNI-16), Epic 2.
- The read-only case record view (RWB-E1-023).
