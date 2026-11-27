# RWB-P3-E1018-APP Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1073-APP |
| Depends on (build) | RWB-P3-E1018-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1073-APP |
| Contract dependencies | RWB-P7-E1027-CON; the `listEligibleAccounts` activity of the rwb-source-data contract jar (contract 5.1.0; provider fake of RWB-P1-E1018-APP) |
| Integration dependencies | None |
| External dependencies | RWB-P3-E1018-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-001, FR-P3-002, FR-P3-003, FR-P3-004, FR-P3-005, FR-P3-006, FR-P3-007, FR-P3-012, FR-P3-030, FR-P3-031, FR-P3-035) |
| Status | Draft (directive resolutions) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P3-E1018-APP-14) |
| Size | Not specified in the source documents (DOR-RWB-P3-E1018-APP-16) |
| Contract fake version | Not specified in the source documents (DOR-RWB-P3-E1018-APP-22) |
| Contract version | Own contract Not specified in the source documents (DOR-RWB-P3-E1018-APP-23); consumes rwb-source-data 5.1.0 |
| Readiness decisions | RD-P1-003, RD-P1-005, RD-P1-010, RD-P1-024, RD-P1-040 |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- D-RCV-60 finishing pass: requests W2-tests-3494, W2-tests-4632, W9-governance-0174; Test Cases v9 mappings.

- RD-P1-010: the entry read is the activity `listEligibleAccounts` (published in the rwb-source-data contract jar, implemented by RWB-P1-E1018-APP) with its request, page, candidate fields, breaks and failure types; the three unpublished REST reads are removed (findings #1, #2).
- RD-P1-003 and RD-P1-040: DailyCaseRun starts only on AceDataReady for ALS with status COMPLETED; key and payload stated (finding #3).
- AC7 restated; X13, X14 and AC19 to AC22 added (findings #4, #6, #7).
- Source of `region_code` and `branch_code` is open as NEW-GAP-F11-6 (finding #5).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-018 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (40 resolved, 36 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **product owner**, I want **every account at 90 days past due or more that rwb-source-data publishes from the ACE account view, and that no exclusion rule blocks, placed on one recovery case per customer and product inside rwb-case, with a case number in the form RW-YYYY-NNNNNN issued from a per-service sequence at creation and never reused, a status and its linked accounts and parties held in the rwb_case schema, created by the DailyCaseRun workflow on AceDataReady for the business date**, so that **every team, letter and document refers to one case ID held by one owner service**.

### 2. Business rationale

Recovery teams keep their own lists today, so one account can be on several trackers under different references, and some accounts at 90 days past due have no owner at all (control CTL-01 answers this audit finding). In the target, ACE ingests the ALS account, the SCBPDM customer and the EFS collections history, and rwb-source-data publishes the thirty `recovery.v_ace_*` views through its contract; rwb-case never reads an ACE view or another service's tables (DP-01, DP-05). This story creates the case by rule when the ACE batch for the business date is complete, blocks an excluded account with a logged reason, and gives the case a number that every later document carries.

Under D-RCV-36 the entry and exclusion rules are the Drools packages ENTRY and EXCLUSION. In the target the governance of a package (authoring, tests, four-eyes approval, effective dating) is central in rwb-decision (P7), the version in force is fetched by rwb-case through `GET /rule-models/{n}/{v}` and executed by the embedded Drools kit inside an activity (DP-04), so a rule change needs no release and every decision names the rule ID and the package version. It meets REQ-CWC-001 to REQ-CWC-005 and REQ-CWC-016, and supports reconciliation REC-01 (accounts at 90 days past due against open cases, zero unexplained) and REC-05 (every business key on a P3 table resolves to its source row).

### 3. Preconditions

- RWB-P3-E1018-CON is published: the case resource schemas, the six `rwb.case.events.v1` event schemas with the CloudEvents envelope, the error envelope, the Idempotency-Key rule and the contract fakes.
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions (DP-15). The rwb_case tables `recovery_case`, `case_account`, `case_party` and `case_entry_exclusion` exist before this story runs its own migrations.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). RWB-P7-E1027-CON publishes the central ledger contract behind it.
- RWB-PLT-E1072-CON is published: the embedded Drools kit, with one KieBase per package version, first-match semantics and the `NoPackageInForce` outcome (DP-04).
- RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the parameters contract and the reference-data contract, both owned by rwb-case, with the client library (DP-06, DP-07).
- RWB-PLT-TE006-CON is published: the outbox and inbox library with CloudEvents (DP-09). RWB-PLT-E1047-CON is published: the topic and event naming library (DP-14). RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery` (DP-10).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves the case screen (DP-19), also recorded under GAP-0674.
- RWB-P3-E1073-APP is done: package ENTRY version "ENTRY-2026.11" and package EXCLUSION version "EXCL-2026.11" are approved by RW-RISK, who is not the author, and are in force from 2026-11-30, each with at least 50 passing scenarios. The EXCLUSION rows carry reason codes DECEASED, FRAUD, BANKRUPTCY, ACTIVE_PLAN and OPEN_DISPUTE (REQ-CWC-004).
- Parameter `case.entry.dpd` = 90 is in force in `parameter_value` (DL16), owned by RW-COE.
- The exposure band table LOV-EXPOSURE, the status list LOV-CASE-STATUS and LOV-PRODUCT are held in the rwb-case reference tables `lov_value`, `reference_row` and `reference_version` (DP-07).
- The daily case run starts only on AceDataReady (EV-26) with `sourceSystem` ALS and `status` COMPLETED for the business date, or on its Schedule fallback, where the activity gate applies.
- The login is the rwb-case login (DP-02): Not specified in the source documents (GAP-0675; ASM-1222).
- The extension rows party_ext and account_ext are written and read by rwb-source-data; their flags reach this story only in the candidates of `listEligibleAccounts`, which RWB-P1-E1018-APP implements.
- Seeded exclusion decision records use the code of RWB-P3-E1019-APP or the exclusion rule; both codes are confirmed at the decision-record contract review (GAP-2252).

### 4. Flow

1. rwb-source-data: the ALS batch for business date 2026-12-01 completes, its `AceIngestCheck` workflow stamps freshness, and it publishes AceDataReady (EV-26) on `rwb.source-data.events.v1`, record key `ALS:2026-12-01`, payload `sourceSystem`, `businessDate`, `status`, `completedAt`, one event per source system and business date. While `v_ace_batch_status` does not exist or holds no COMPLETED ALS row for the date, the entry read fails with `AceBatchNotComplete`: no candidate, no break and no case for that date.
2. rwb-case: the case router consumes the event through its inbox (one action per event) and, only when `sourceSystem` is ALS and `status` is COMPLETED, calls `signalWithStart` and starts DailyCaseRun on task queue `rwb-case` for the payload `businessDate`. An event for another source system is ignored.
3. DailyCaseRun: reads parameter `case.entry.dpd` through the parameters contract of rwb-case, with the version in force.
4. DailyCaseRun: calls the activity `listEligibleAccounts` (published in the rwb-source-data contract jar, implemented by RWB-P1-E1018-APP) (task queue `rwb-source-data`, namespace `rwb-recovery`, rwb-case worker identity) with `EligibleAccountsRequest {businessDate, threshold, pageToken, pageSize}`: `threshold` is the value of `case.entry.dpd`, `pageToken` is null on the first page and `pageSize` is 500 by default and at most 1000. It follows `nextPageToken` until it is null. Each answer is `EligibleAccountsPage {businessDate, threshold, asOf, candidates[], breaks[], nextPageToken}`; a candidate carries `accountKey`, `accountCode`, `productGroup`, `daysPastDue`, `totalBalance`, `contractNo`, `dataAsOf`, `tdrFlag`, `deceasedFlag`, `disputeOpen`, `deceasedOverride`, `bankruptcy`, `fraudFlag` and `personKey`. `region_code` is a rwb-case attribute and is not served; its source and that of `branch_code` are Pending (owner rwb-case service owner, NEW-GAP-F11-6). An account that already has an open `case_account` row (`linked_to` is null) is skipped.
5. DailyCaseRun: takes the BORROWER `personKey` from the candidate; an account whose borrower key is reported in `breaks[]` with `keyType` PERSON is not grouped and gets no case. No per-account call is made to rwb-source-data.
6. EvaluateRules activity: the embedded Drools kit evaluates package EXCLUSION on the facts built from the candidate fields and flags; an excluded account gets a `case_entry_exclusion` row with the reason code, the rule ID and the package version, and no case. The package version is the one in force on the business date and is verified against the checksum returned by rwb-decision.
7. EvaluateRules activity: package ENTRY is evaluated on `days_past_due`, the product group and the entry threshold; an account the package does not match gets no case and is counted as not entered; the ENTER rule ID (Not specified in the source documents (GAP-2436)) and package version are carried to the decision record.
8. Grouping: the remaining accounts are grouped by the borrower `person_key` and the product group read from the account row; an existing open case for the same pair receives a new `case_account` row with the `account_key` instead of a new case.
9. Case number: the per-service sequence for the entry year in `rwb_case` is drawn and formatted RW-2026-000123; a number is never reused, including for a closed case.
10. RecordAndApply activity: in one rwb_case transaction the service writes `recovery_case` with status NEW, the primary customer key, `dpd_at_entry`, `total_outstanding_at_entry` and the exposure band, the `case_account` rows with `account_key` and `is_primary`, the BORROWER `case_party` row with `person_key`, and CaseCreated (EV-01) in the outbox. The primary account is the linked account with the highest `total_balance` on the business date; a tie breaks on the lowest `account_key`.
11. RecordAndApply activity: as the last step before commit, the local decision-record library writes decision code "D6", final call "CASE_CREATED", the ENTRY rule ID and package version and the ALS business date, and publishes DecisionRecorded on `rwb.decision-record.v1` through the outbox; a failed write rolls the whole transaction back, so no number is consumed by a visible case.
12. DailyCaseRun: records the counts (accounts read, excluded, not entered, linked, created, failed) on the run record and starts the next step, the morning allocation (JOB-03, carried by RWB-P3-E1020-APP).
13. CaseWorkflow is started once per case with the workflow ID equal to the case ID, on task queue `rwb-case`, and takes the case from entry to closure.
14. Case owner: opens the case through gateway-bff, which calls `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/accounts` on rwb-case and, in parallel, rwb-source-data `GET /api/recovery/source-data/v1/data-products/{productCode}/records` for DP01 and DP02 with that `caseId` for the account and customer fields, then merges the two answers into the screen model.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The account matches an EXCLUSION rule | No case; `case_entry_exclusion` row with reason code, rule ID and package version | None | AC2, AC6 |
| X2 | The borrower already has an open case for the same product group | The account is linked to that case by `account_key`; no new case | None | AC3 |
| X3 | Days past due is 89 in the account row of the business date | No case; the account is read again on the next complete ALS batch | None | AC7 |
| X4 | DailyCaseRun runs again for the same business date | No duplicate case, link or number; the inbox drops the second event and the run skips a linked account | None | AC8 |
| X5 | The ALS batch for the business date is not complete | No AceDataReady for ALS is published, so DailyCaseRun does not start from an event; no case from an incomplete day; it starts when AceDataReady for ALS with status COMPLETED is raised for the date | MSG-P1-001 | AC9 |
| X6 | The decision record write fails | The case is not created and no number is consumed by a visible case; the account is retried in the next run | MSG-P7-003 | AC10 |
| X7 | The yearly number range RW-2026-999999 is used | Creation stops for the year's remaining accounts; an incident is raised | MSG-P3-025 | AC11 |
| X8 | The same borrower has a mortgage and a hire purchase account at 90 days past due | Two cases, one per product group | None | AC12 |
| X9 | A business key on a case or in the intake has no row in the source contract | The intake creates no case or party link from the missing row; an existing link is unchanged; the activity reports the key in `breaks[]` (`keyType`, `businessKey`, `viewName`, `businessDate`) and REC-05 lists it for the data steward and the ACE team; the key is read again on the next complete batch | None | AC13 |
| X10 | A role without Case record R reads a case | Refused with 403 by the rwb-access authorise check behind the endpoint | MSG-P4-002 | AC14 |
| X11 | No EXCLUSION version is in force on the business date | DailyCaseRun creates no case for the date; the run record carries MSG-P3-027 for the package-in-force check; the accounts are held for the next run | MSG-P3-027 | AC15 |
| X12 | The `listEligibleAccounts` activity fails with a retryable error or passes its timeout | The page is retried under the retry parameters in force; the accounts not read are left for the next run and counted as failed, never created from a partial record | None | AC9, AC10, AC18 |
| X13 | The activity fails non-retryable with `AceBatchNotComplete` (details `productCode` DP01, `messageCode` MSG-P1-001, `lastCompleteBusinessDate`, null when there is none) | No case, link, exclusion row, decision record or event for the date; the run record carries the failure type and MSG-P1-001 | MSG-P1-001 | AC20 |
| X14 | The activity fails non-retryable with `BusinessDateNotCurrent` (the requested date is older than the current ACE data) | No case, link, exclusion row, decision record or event; the run record carries the failure type | None | AC21 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contracts: the case CON story, the platform contract stories and RWB-P3-E1073-APP. The rwb-source-data, rwb-access and rwb-decision answers come from their contract fakes. Allocation follows in RWB-P3-E1020-APP |
| Negotiable | Threshold, exclusion reasons and exposure bands are data values in the parameters, the reference tables and the rule packages; the story fixes the behaviour |
| Valuable | Gives about 28,100 accounts at 90 days past due one case each at go-live (DL15) |
| Estimable | One DailyCaseRun step, one numbering service, one entry and exclusion evaluation through the Drools kit, three read endpoints, one contract surface |
| Small | Fits two weeks with its tests |
| Testable | Every owned criterion has a test case in section 16; every cross-service answer is stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Case ID issuance and case record v1

  Background:
    Given parameter "case.entry.dpd" is 90
    Given package ENTRY version "ENTRY-2026.11" is in force
    Given package EXCLUSION version "EXCL-2026.11" is in force
    Given the business date is 2026-12-01
    Given rwb-source-data reports the ALS batch for 2026-12-01 with status "COMPLETED" and is_complete true
    Given the rwb-source-data contract mock is the provider fake of the activity listEligibleAccounts

  Scenario: AC2 Exclusion applied (legacy RWB-E1-018 AC2)
    Given the rwb-source-data contract mock returns account A-5002 at days_past_due 92 with tdr_flag true
    Given the rwb-decision contract mock returns package code "EXCLUSION" with version "EXCL-2026.11" and rule ID "Not specified in the source documents (CG-ALL-3440)"
    When the entry rule runs
    Then the system creates no case for A-5002
    Then case_entry_exclusion holds account_key A-5002, business date 2026-12-01, reason "ACTIVE_PLAN", rule ID "Not specified in the source documents (CG-ALL-3440)" and package version "EXCL-2026.11"

  Scenario: AC3 One case per customer and product (legacy RWB-E1-018 AC3)
    Given the rwb-source-data contract mock returns for borrower P-0102 hire purchase accounts A-5003 with total_balance 300,000.00 and A-5004 with total_balance 112,350.00, both at days_past_due 95
    When the entry rule runs
    Then one case exists for P-0102 and "HIRE_PURCHASE" with both account_keys linked
    Then total_outstanding_at_entry is the sum of the two balances, THB 412,350.00
    Then case_account holds A-5003 with is_primary true and A-5004 with is_primary false

  Scenario: AC4 ID never reused (legacy RWB-E1-018 AC4)
    Given case RW-2026-000123 was closed on 2026-12-15
    When a new case is created on 2026-12-16
    Then it receives RW-2026-000124
    Then case RW-2026-000123 is still returned by a search on its case number

  Scenario: AC5 State model as data (legacy RWB-E1-018 AC5)
    Given the list LOV-CASE-STATUS gains the value "WAITING_COURT" through a list load with valid from 2027-01-01
    When a case moves to "WAITING_COURT" on 2027-01-02
    Then the case service accepts the value without a code change
    Then the decision record for the move carries the list version in force

  Scenario: AC6 Exclusion rules as data (legacy RWB-E1-018 AC6)
    Given the EXCLUSION package includes reason "OPEN_DISPUTE"
    Given account A-5005 at days_past_due 90 has dispute_open true in account_ext
    Given the rwb-decision contract mock returns package code "EXCLUSION" with version "EXCL-2026.11" and rule ID "Not specified in the source documents (CG-ALL-3441)"
    When the entry rule runs
    Then the system creates no case for A-5005
    Then the exclusion record for A-5005 holds reason "OPEN_DISPUTE" and rule ID "Not specified in the source documents (CG-ALL-3441)"

  Scenario: AC7 The entry threshold boundary (legacy RWB-E1-018 AC7)
    Given the rwb-source-data contract mock holds account A-5006 at days_past_due 89 and account A-5007 at days_past_due 90, both with no exclusion
    Given listEligibleAccounts called with threshold 90 answers account A-5007 only
    Given the rwb-decision contract mock returns package code "ENTRY" with version "ENTRY-2026.11"
    When the entry rule runs
    Then the system creates a case for A-5007
    Then the system creates no case for A-5006

  Scenario: AC8 A repeated run creates nothing new (legacy RWB-E1-018 AC8)
    Given DailyCaseRun has created case RW-2026-000125 for account A-5008 on 2026-12-01
    When DailyCaseRun runs again for 2026-12-01
    Then account A-5008 has one case link
    Then the system issues no case number in the second run

  Scenario: AC10 The decision log write fails (legacy RWB-E1-018 AC10)
    Given the decision record store is unavailable
    When the entry rule runs for account A-5009
    Then no case exists for A-5009
    Then the run record lists A-5009 as failed with MSG-P7-003
    Then the system takes A-5009 again in the next run

  Scenario: AC11 The yearly number range is used up (legacy RWB-E1-018 AC11)
    Given the last case number issued in 2026 is RW-2026-999999
    When account A-5010 qualifies for a new case on 2026-12-30
    Then the system creates no case for A-5010
    Then the run record carries MSG-P3-025 with year 2026
    Then the system raises an incident to the platform administrator

  Scenario: AC12 Two products give two cases (legacy RWB-E1-018 AC12)
    Given the rwb-source-data contract mock returns mortgage account A-5011 and hire purchase account A-5012 for borrower P-0103, both at days_past_due 91
    When the entry rule runs
    Then two cases exist for P-0103, one with product group "MORTGAGE" and one with "HIRE_PURCHASE"

  Scenario: AC14 A role without Case record R is refused (legacy RWB-E1-018 AC14)
    Given user "U-5001" holds RW-REFADM, which has no Case record right
    Given the rwb-access contract mock returns no Case record right for role "RW-REFADM"
    When "U-5001" calls GET /cases/{caseId} for case RW-2026-000123
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system writes one AC-DENY event with area "CASE_RECORD" and right "R"

  Scenario: AC16 Band, cancel by rule and checksum rules (BR9, BR10, BR14) (new, D-RCV-60)
    Given the band table in force is the table for the business date
    When a case is created with a total outstanding at entry
    Then its exposure_band is the band in the band table in force that contains that total
    Given a case was created on bad data
    When the case is canceled by rule
    Then the case is canceled and is not deleted
    Given the rwb-decision contract mock returns package code "ENTRY" with a version whose checksum does not verify
    When the entry rule runs
    Then the KieBase for that version is not used

  Scenario: AC17 Error answers 401 and 404 of the provided operations (new, D-RCV-60)
    Given a caller sends GET /cases/{caseId} without a valid credential
    When the call is made
    Then the system answers with status 401
    Given a caller sends GET /cases/{caseId} for a case ID that does not exist
    When the call is made
    Then the system answers with status 404

  Scenario: AC18 A retried or timed-out activity creates nothing twice (new, D-RCV-60)
    Given an activity of DailyCaseRun fails with a retryable error
    When the activity is retried under the retry parameters in force
    Then the retry creates no second case and issues no second case number
    Given an activity of DailyCaseRun exceeds the timeout in force
    When the timeout is reached
    Then the run record lists the account as failed and the account is taken again in the next run

  Scenario: AC19 Only the ALS completion starts the run (new, D-RCV-60)
    Given rwb.source-data.AceDataReady.v1 arrives with record key "EFS:2026-12-01", sourceSystem EFS and status COMPLETED
    When the case router consumes it
    Then no DailyCaseRun starts and listEligibleAccounts is not called
    Then no case, link, exclusion row, decision record or event is written

  Scenario: AC20 The activity reports the batch not complete (new, D-RCV-60)
    Given listEligibleAccounts fails non-retryable with type AceBatchNotComplete and details productCode "DP01", messageCode "MSG-P1-001" and lastCompleteBusinessDate 2026-11-30
    When DailyCaseRun runs for 2026-12-01
    Then the activity is not retried
    Then no case, link, exclusion row, decision record or CaseCreated event is written
    Then the run record carries the type AceBatchNotComplete and MSG-P1-001

  Scenario: AC21 The requested business date is no longer current (new, D-RCV-60)
    Given listEligibleAccounts fails non-retryable with type BusinessDateNotCurrent for 2026-11-30
    When DailyCaseRun runs for 2026-11-30
    Then the activity is not retried and no case, link, exclusion row, decision record or event is written
    Then the run record carries the type BusinessDateNotCurrent

  Scenario: AC22 Every page of eligible accounts is read (new, D-RCV-60)
    Given listEligibleAccounts answers a first page with nextPageToken "P2" and a second page with nextPageToken null, each with one eligible account of a different borrower and no exclusion
    When DailyCaseRun runs for 2026-12-01
    Then the activity is called twice, first with pageToken null and then with pageToken "P2", each with businessDate 2026-12-01, threshold 90 and pageSize 500
    Then two cases are created, each with its CaseCreated event and decision record
```

AC1, AC9, AC13 and AC15 are cited in the flow and the exception table but are owned by the integration story RWB-ITG-E1018-ITG of this legacy key, where the real cross-service behaviour and the batch gate are proved; the eleven criteria above are the ones this story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An account enters recovery when `days_past_due` for the ACE business date is at or above the entry threshold and package ENTRY returns ENTER | Parameter case.entry.dpd = 90; package ENTRY; DL16; DF-ACE-018 |
| BR2 | One case per borrower `person_key` and product group, with every qualifying account linked by `account_key` | DL17; REQ-CWC-003 |
| BR3 | An account matching an EXCLUSION rule gets no case; the reason, rule ID and package version are recorded in `case_entry_exclusion` | Package EXCLUSION; REQ-CWC-004 |
| BR4 | The case number is RW, the entry year and a six-digit number from the per-service yearly sequence; it is issued once and never reused, including after closure | `recovery_case.case_no` (DF-CAS-002); the unique key on the case number |
| BR5 | A new case has status NEW and no owner until allocation | casemodel.txt Case status "New" |
| BR6 | Status values are read from the reference list, not from code; a new list value is accepted with its version in force | LOV-CASE-STATUS; DP-07 |
| BR7 | No case is created before the ACE batch for the business date is complete; a late or failed batch is carried by AceDataLate and the case is created on the next complete batch | CTL-02; DailyCaseRun "No cases from an incomplete day" |
| BR8 | Every case creation writes its decision record, with the ENTRY rule ID and package version, in the same transaction as the case rows and the outbox row; a failed write rolls the creation back | Principle 5; R-UNI-39; REQ-CWC-016 |
| BR9 | The exposure band is set from the total outstanding at entry using the band table in force | `recovery_case.exposure_band` (DF-CAS-015); LOV-EXPOSURE |
| BR10 | A case created on bad data is canceled by rule, never deleted | R-UNI-16 (Epic 2 handling) |
| BR11 | The case links to its source by business key (`primary_customer_id`, `account_key`, `person_key`) with no foreign key across services. A key with no source row is listed by REC-05 and never invented from a partial record | DP-01; D-RCV-35 U4; ADR-010; REC-05 |
| BR12 | The primary account is the linked account with the highest `total_balance` on the business date; a tie breaks on the lowest `account_key` | `case_account.is_primary` (DF-CAS-027); Data Tier Map section 5 |
| BR13 | Entry and exclusion decisions come only from the embedded Drools kit on packages ENTRY and EXCLUSION, using the version in force. A version not in force holds creation with MSG-P3-027 and is never a default decision | R-UNI-41; D-RCV-36 T3, T5; DP-04 |
| BR14 | The package version is fetched from rwb-decision, its checksum is verified before the KieBase is used, and a version is never edited in place | D-RCV-36 T4; DP-04 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | AceDataReady (EV-26), package ENTRY returns ENTER | `days_past_due` at or above 90 for the complete ALS business date, package EXCLUSION returns no match, no open case for the borrower and product group | New |
| New | Allocation rule matched | Handled by RWB-P3-E1020-APP | Assigned |

`WAITING_COURT` is a list value added to LOV-CASE-STATUS by a list load with valid from 2027-01-01 (AC5); it is accepted as data through the reference-data contract and needs no code change.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Runs DailyCaseRun; calls `listEligibleAccounts` of rwb-source-data under the rwb-case worker identity (namespace mTLS), whose candidates carry the borrower key and the exclusion flags; creates the case, the account links, the party link, the exclusion rows and the decision record |
| ACE batch record through rwb-source-data | Raises AceDataReady (EV-26); no case write in this story |
| Drools evaluator (SY-RULES identity) | Evaluates the ENTRY and EXCLUSION packages through the embedded kit (Rules and parameters R) |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL and every role with Case record R | Read the case and its accounts through the endpoints, within their scope |
| RW-COE | Owns the ENTRY and EXCLUSION packages and the threshold parameter; loads the packages through RWB-P3-E1073-APP and the parameter through the parameters contract |
| RW-RISK | Approves a package version; the author cannot approve |
| Platform administrator | Extends the yearly number range when MSG-P3-025 is raised |
| RW-REFADM | Has no Case record right; refused on the read endpoints |

The per-service login name is Not specified in the source documents (GAP-0675; ASM-1222); the story names it "the rwb-case login (DP-02)" until it is agreed.

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Write |
| DF-CAS-024 to DF-CAS-029 | case_account | all fields | Write |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |
| DF-CAS-056 to DF-CAS-061 | case_entry_exclusion | all fields, including rule_id and rule_version | Write |
| DF-CAS-002 | recovery_case | case_no (RW-YYYY-NNNNNN) | Write |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | `case.entry.dpd` and its version in force | Read |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | LOV-CASE-STATUS, LOV-EXPOSURE, LOV-PRODUCT versions | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) | all fields | Write |

Source facts are read only through the `listEligibleAccounts` activity of rwb-source-data: `accountKey`, `accountCode`, `productGroup` (ACE `product_category`, unvalidated), `daysPastDue`, `totalBalance`, `contractNo`, `dataAsOf`, `tdrFlag`, `deceasedFlag`, `personKey` and the extension flags `disputeOpen`, `deceasedOverride`, `bankruptcy` and `fraudFlag` (DF-ACE-001, DF-ACE-002, DF-ACE-010, DF-ACE-018, DF-ACE-020, DF-ACE-036, DF-ACE-056, DF-ACE-061, DF-EXT-001, DF-EXT-003, DF-EXT-004, DF-EXT-005, DF-EXT-027, DF-EXT-028). The BORROWER relation is resolved by rwb-source-data (DF-ACE-084, DF-ACE-085, DF-ACE-086). `branch_code` (DF-ACE-012) and `region_code` are not served by the activity (NEW-GAP-F11-6). No copy of a source row is written into rwb_case.

Field IDs are those in the Logical Data Model and Data Dictionary v9. `case_entry_exclusion.rule_id` holds the Drools rule name and `case_entry_exclusion.rule_version` holds the package version label (D-RCV-36 T5); both are inside DF-CAS-056 to DF-CAS-061, so no field ID is added. rwb-case reads no rule row; the package is fetched as a model from rwb-decision.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases` | List cases in the caller's scope, including the case-number search used by AC4 | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}` | Read one case with status, entry date, exposure band and totals | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/accounts` | Read the linked accounts with the primary flag and link dates | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/parties` | Read the parties on the case, masked by role | Case record R, scope applied | Not applicable |

Response fields per the case CON story: case `id`, `caseNo`, `productGroup`, `primaryPersonKey`, `status`, `entryDate`, `dpdAtEntry`, `exposureBand`, `totalOutstandingAtEntry`, `deviationOpen`, `legalHold`; account `id`, `caseId`, `accountKey`, `isPrimary`, `linkedFrom`, `linkedTo`. Errors: 401 no session (MSG-P4-001), 403 no Case record R (MSG-P4-002), 404 not found or out of scope (MSG-P4-003), 503 store down (Not specified in the source documents (CG-ALL-3434)).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/rule-models/{n}/{v}` | rwb-decision (P7) | Package model, checksum and version label (DP-04) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Role, scope and right check before a read (AC14) | One hop, 2 s (DP-11) |

DailyCaseRun calls no REST operation of rwb-source-data: account, borrower, flag and batch facts come from the activity `listEligibleAccounts` (published in the rwb-source-data contract jar, implemented by RWB-P1-E1018-APP) (12.5). `GET /entry-candidates` and `GET /entry-candidate-facts` are not published.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 | caseId | caseId, caseNo, productGroup, accounts, businessDate |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 | caseId | decision code "D6", final call "CASE_CREATED", rule ID, rule version, business date, record reference |

Both are written to the outbox in the same transaction as the state change and relayed with the CloudEvents envelope. The personal-data class of each field sent is the one held in the Logical Data Model and Data Dictionary v9 (DP-09).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | P1 | Case router, inbox dedupe; record key `{sourceSystem}:{businessDate}`, payload `sourceSystem`, `businessDate`, `status`, `completedAt`; `signalWithStart` of DailyCaseRun for the business date only when `sourceSystem` is ALS and `status` is COMPLETED |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 | Drops the cached KieBase for the package so the next evaluation fetches the version in force |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Takes the case from entry to closure; stage work runs as child workflows in the owning services |
| DailyCaseRun | Workflow started by AceDataReady (ALS, COMPLETED), with a daily Schedule fallback; workflow ID and duplicate-start policy: Not specified in the source documents (CG-ALL-3439) | `rwb-case` | Runs case creation (legacy JOB-02) and the morning allocation step (legacy JOB-03) |
| `listEligibleAccounts` | Activity of rwb-source-data (consumed) | `rwb-source-data` | `EligibleAccountsRequest` to `EligibleAccountsPage`; non-retryable failure types `AceBatchNotComplete` and `BusinessDateNotCurrent` |
| allocate | Activity | `rwb-case` | Places a case on a queue and an owner (owned by RWB-P3-E1020-APP) |
| transfer | Activity | `rwb-case` | Moves a case between owners and queues (owned by RWB-P3-E1021-APP) |
| rebalance | Activity | `rwb-case` | Rebalances a queue (owned by RWB-P3-E1020-APP) |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Calls the embedded Drools kit with a package code, facts and the business date |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Writes the decision record, the state change and the outbox rows in one transaction |

#### 12.6 Schedules

| Schedule | Cadence | Trigger | Legacy reference |
|---|---|---|---|
| DailyCaseRun | Daily, when the ALS batch for the business date completes, with a daily fallback | AceDataReady (EV-26) plus a Temporal Schedule with overlap policy SKIP and a catch-up window | JOB-02 Case creation |
| Allocation step inside DailyCaseRun | After case creation, by 07:00 | DailyCaseRun step | JOB-03 Morning allocation (RWB-P3-E1020-APP) |

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | Case header, status, entry date, totals, exposure band, hold flags |
| case_account | P3 (rwb_case) | Account link with `account_key`, `is_primary`, `linked_from`, `linked_to` |
| case_party | P3 (rwb_case) | Party link with `person_key` and party role |
| case_entry_exclusion | P3 (rwb_case) | One row per account and business date with reason, rule ID and package version |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency objects (DP-09) |

rwb-case reads no table of another service and holds no foreign key across services (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data activity fake | The P1 contract 5.1.0 (provider fake of RWB-P1-E1018-APP) | `listEligibleAccounts` pages with candidates and breaks, the failure types `AceBatchNotComplete` and `BusinessDateNotCurrent`, and EV-26 samples for ALS and another source |
| rwb-decision WireMock | The P7 contract | `GET /rule-models/{n}/{v}` for ENTRY "ENTRY-2026.11", EXCLUSION "EXCL-2026.11" and rule IDs Not specified in the source documents (CG-ALL-3440) and Not specified in the source documents (CG-ALL-3441) |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R and refusing it for RW-REFADM |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 2 consumed | Case reads provided; decision models and authorise consumed; one hop, 2 s timeout |
| Kafka | 2 published, 2 consumed | `rwb.case.events.v1` and `rwb.decision-record.v1` published; `rwb.source-data.events.v1` and `rwb.decision.events.v1` consumed |
| Temporal | 2 workflows, 5 activities | CaseWorkflow and DailyCaseRun; allocate, transfer, rebalance, EvaluateRules, RecordAndApply; consumes `listEligibleAccounts` of rwb-source-data |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `casecreation`, Java package `th.co.scb.ace.workbench.recovery.case.casecreation`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P3-E1073-APP |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract only | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DailyCaseRun | Workflow | Started by AceDataReady with a daily Schedule fallback; carries case creation (legacy JOB-02) and the allocation step (legacy JOB-03); records the run counts |
| CaseEntryActivity | Activity | Builds the exclusion and entry facts and calls the embedded Drools kit for EXCLUSION then ENTRY; returns EXCLUDE with reason, rule ID and package version, or ENTER |
| RulePackageClient | Client | Fetches the package model and checksum from rwb-decision, verifies it, and hands it to the KieBase registry (DP-04) |
| CaseGrouping | Service | Groups accounts by the BORROWER `person_key` and product group; finds an open case to link to |
| CaseNumberIssuer | Service | Draws from the per-service yearly sequence in rwb_case and formats RW-YYYY-NNNNNN; refuses above 999999 |
| CaseCreationService | Service | Writes the decision record, then the case, the account links, the primary flag, the party link and the outbox row in one transaction |
| SourceDataClient | Client | Activity stub of `listEligibleAccounts` on task queue `rwb-source-data`; pages until `nextPageToken` is null and maps the two failure types to the run record |
| CaseRepository | Repository | `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion`; writes only schema rwb_case |
| CaseController | Controller | `GET /cases`, `GET /cases/{caseId}`, `GET /cases/{caseId}/accounts`, `GET /cases/{caseId}/parties`; the case-number search on `GET /cases` |
| CaseStatusCatalog | Service | Reads LOV-CASE-STATUS through the reference-data contract; no Java enum of statuses |
| AccessCheckClient | Client | Calls the rwb-access authorise contract (cached) before a read |

**Database and migrations**

- Writes `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion` and the outbox in schema rwb_case.
- Constraint: partial unique index `ux_case_open_customer_product ON recovery_case (primary_person_key, product_group) WHERE closed_date IS NULL`.
- Constraint: partial unique index `ux_case_account_open ON case_account (account_key) WHERE linked_to IS NULL`, so an account is on one open case.
- Constraint: one `case_entry_exclusion` row per `account_key` and business date, with the reason code, the rule ID and the package version, which the run and TC-E1-018-02 assert.
- Migrations in this story: the `case_creation` migration takes the next free number of the rwb-case Flyway sequence V0001..Vnnnn (DP-15; the number is Not specified in the source documents (CG-ALL-3450)); it creates the yearly sequences `case_no_seq_2026` and `case_no_seq_2027` (created ahead by a December step) and the two partial unique indexes above. The four tables arrive with the rwb_case baseline; no column is added for source data.

**Configuration and reference data**

- Parameter `case.entry.dpd` = 90 through the parameters contract, owner RW-COE (DL16).
- Package ENTRY version "ENTRY-2026.11" and package EXCLUSION version "EXCL-2026.11" with the five reason codes, loaded, tested and approved through RWB-P3-E1073-APP (D-RCV-36 T4).
- LOV-EXPOSURE bands, LOV-CASE-STATUS and LOV-PRODUCT through the reference-data contract.

**Build steps**

1. CaseNumberIssuer with the per-service yearly sequence and the 999999 limit; unit and integration tests for AC4 and AC11.
2. SourceDataClient over the `listEligibleAccounts` activity stub with paging and the two failure types; tests the join by `accountKey` and `personKey` for AC3 and AC12, and AC20 to AC22.
3. CaseEntryActivity with the embedded Drools kit for EXCLUSION and ENTRY, the checksum check and the hold when no version is in force; tests for AC2, AC6 and AC7.
4. CaseGrouping with the open-case lookup and the primary-account rule; tests for AC3 and AC12.
5. CaseCreationService: the decision record and outbox row with the case rows in one transaction; test for AC10.
6. DailyCaseRun on AceDataReady (ALS, COMPLETED) with the inbox dedupe and the idempotent skip; tests for AC8 and AC19.
7. CaseStatusCatalog reading statuses and list versions from the reference-data contract; test for AC5.
8. Controller endpoints with the access check and scope, and the case-number search; test for AC14.
9. Contract-fake run of every cross-service answer in isolation, so the story builds before the other services exist.

**Feature switch.** The legacy flag name `rwb.p3.casecreation` is kept as the legacy reference. In the target the switch is a parameter read through the parameters contract: off means DailyCaseRun creates no case. The batch gate depends on rwb-source-data freshness, so it is on only when rwb-source-data publishes AceDataReady for the environment.

**Done when.** The tests in section 16 pass, REC-01 shows zero unexplained difference on the SIT data set, every decision record names the ENTRY rule ID and package version, and the contract tests of RWB-P3-E1018-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | DailyCaseRun waiting for a complete ALS batch | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-027 | No ENTRY or EXCLUSION version is in force on the business date | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P7-003 | Decision record write failed for an account | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-025 | Yearly case number range used up | Case numbers for {year} are used up. New cases are on hold until the range is extended. |
| MSG-P4-002 | Read without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |
| MSG-P4-001 | A request arrives with no session | Not specified in the source documents (DOR-RWB-P3-E1018-APP-9) |

For MSG-P3-027 the {check} value is "package in force" and the {table} names the package code only.

### 15. Screens and states

SCR-02 Case list (Loading; empty; list; filtered; error and no access states: Not specified in the source documents (CG-ALL-3453)) shows each new case with its case number, product, status NEW and entry date, and the account number and balance read from the rwb-source-data account-page read (path Pending, GAP-3274). SCR-03 Case record (Loading; read only; empty, error and no access states: Not specified in the source documents (CG-ALL-3454)) shows the case and its linked accounts by `account_key`.

Both screens are served by the gateway-bff composite route, which calls rwb-case and rwb-source-data in parallel, one hop each, and merges the two answers into the screen model. The screen fields, the field-level masking of customer fields and the composite route specification are Not specified in the source documents (GAP-0674; ASM-1221); the full read-only view is RWB-P3-E1023-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-018-02 | AC2, BR3 | End to end | rwb-source-data fake account A-5002 with `tdr_flag` true; package EXCLUSION "EXCL-2026.11" |
| TC-E1-018-01 | AC1, BR1, BR2, BR4, BR5, BR11, BR12, BR13 | End to end; run by RWB-ITG-E1018-ITG | rwb-source-data fake account A-5001 at 90 days past due, borrower P-0101, last number RW-2026-000122 |
| TC-E1-018-03 | AC3, BR2, BR12 | End to end | Borrower P-0102 with two HP accounts of 300,000.00 and 112,350.00 |
| TC-E1-018-04 | AC4, BR4 | End to end | Closed case RW-2026-000123 |
| TC-E1-018-05 | AC5, BR6 | End to end | New status value WAITING_COURT in LOV-CASE-STATUS |
| TC-E1-018-06 | AC6, BR3 | End to end | rwb-source-data fake account A-5005 with `dispute_open` true; EXCLUSION rule Not specified in the source documents (CG-ALL-3441) |
| TC-P3-E1018-APP-01 | AC7, BR1 | End to end | Accounts at 89 and 90 days past due in the rwb-source-data fake |
| TC-E1-018-08 | AC8 | End to end | DailyCaseRun run twice for 2026-12-01 |
| TC-E1-018-09 | AC9, BR7 | End to end; run by RWB-ITG-E1018-ITG | ALS batch for 2026-12-02 at status RUNNING |
| TC-E1-018-10 | AC10, BR8 | End to end | Decision record store unavailable for one account |
| TC-E1-018-11 | AC11, BR4 | End to end | Sequence at 999999 |
| TC-P3-E1018-APP-06 | AC12, BR2 | End to end | Borrower P-0103 with a mortgage and an HP account |
| TC-E1-018-13 | AC14, BR11 | Component | RW-REFADM reads GET /cases/{caseId} and is refused with MSG-P4-002 |
| TC-E1-018-14 | Principle 5 | NFR | Decision record write forced to fail for the whole run |
| TC-E1-018-15 | AC13, BR11 | End to end; run by RWB-ITG-E1018-ITG | Case links A-5013 and P-0105 with no view row for 2026-12-01 |
| TC-E1-018-16 | AC15, BR13 | End to end; run by RWB-ITG-E1018-ITG | No EXCLUSION version in force on 2026-12-01 |
| TC-E1-018-17 | Section 12 operations, events and activities | Contract | rwb-source-data, rwb-decision and rwb-access fakes (section 12.8) |
| TC-E1-018-18 | Tables of section 12.7 | Component | Boundary values for each table of section 12.7 |
| TC-E1-018-19 | BR9 | End to end | Total outstanding at entry in each band of the band table in force |
| TC-E1-018-20 | BR10 | End to end | Case created on bad data, then canceled by rule and not deleted |
| TC-E1-018-21 | BR14 | End to end | ENTRY version whose checksum from rwb-decision does not verify |
| TC-E1-018-22 | AC16, BR9, BR10, BR14 | End to end | Band table in force; case created on bad data; ENTRY version whose checksum from rwb-decision does not verify |
| TC-E1-018-23 | AC17 | Component | GET /cases/{caseId} with no valid credential and for a case ID that does not exist |
| TC-E1-018-24 | AC18, BR4 | End to end | DailyCaseRun activity that fails and is retried, and one that times out |
| TC-P3-E1018-APP-02 | AC19 | Component | AceDataReady for a source system other than ALS |
| TC-P3-E1018-APP-03 | AC20, BR7 | Component | Activity failure AceBatchNotComplete |
| TC-P3-E1018-APP-04 | AC21 | Component | Activity failure BusinessDateNotCurrent |
| TC-P3-E1018-APP-05 | AC22 | Component | Two pages of eligible accounts |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. The ALS batch for a test is seeded through the W1J01 harness, and the tests assert the Kafka `rwb.case.CaseCreated.v1` event and the P7 DecisionRecorded ledger entry on `rwb.decision-record.v1` (GAP-0343).

### 17. Guardrails

- No business value in code: the threshold, the exclusion reasons, the bands and the status list are data in the parameters, the reference tables and the rule packages.
- No personal data in logs, tests, workflow history or prompts. The run reads `account_key` and `person_key` only: no name, address or identity number is read or written. Workflow payloads pass the payload codec; test data uses synthetic account and customer keys only.
- No read of another service's tables and no ACE view: account, customer, relation, extension and freshness data come only through the rwb-source-data contract (DP-01, DP-05). The rwb_case schema holds no foreign key into another schema.
- One evaluator: ENTRY and EXCLUSION are evaluated only through the embedded Drools kit on the package version fetched from rwb-decision; no code reads a workbook, a DRL source or a rule row directly (D-RCV-36 T3, T6; DP-04).
- `case_entry_exclusion` stores the rule ID (Drools rule name) and the package version label; the decision record table is written by the library and its schema is not changed (D-RCV-36 T5).
- The case links to its source by business key (`primary_customer_id`, `account_key`, `person_key`) with no foreign key; REC-05 lists a key with no source row and nothing is invented from a partial record.
- The case number is printed on every outbound document; other services take it from the case contract, never from a copy.
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-04 | 6.1 | R-UNI-16 | TC-E1-018-01, TC-P3-E1018-APP-01, TC-E1-018-09 |
| REQ-CWC-002 | Case ID RW-YYYY-NNNNNN, never reused | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-01 | 6.1 | None | TC-E1-018-01, TC-E1-018-04, TC-E1-018-11 |
| REQ-CWC-003 | One case per customer and product | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-02 | 6.1 | R-UNI-17 | TC-E1-018-03, TC-E1-018-08, TC-P3-E1018-APP-06 |
| REQ-CWC-004 | Exclusion rules as data | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-05 | 6.1 | None | TC-E1-018-02, TC-E1-018-06, TC-E1-018-16 |
| REQ-CWC-005 | State model with one state at a time | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-03 | 6.1 | None | TC-E1-018-05 |
| REQ-CWC-016 | Every workflow event logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-21 | 6.1 | R-UNI-39 | TC-E1-018-10, TC-E1-018-14 |
| REQ-CHO-004 | One agreed hand-over point in days past due for every rule and report | Business Requirements Epic 1, section 3.3 | FEAT-CWC-01, FEAT-CWC-02, FEAT-CWC-03, FEAT-CWC-04, FEAT-CWC-05, FEAT-CWC-20, FEAT-CWC-21 | 6.1 Take over the case at 90 days past due | None | TC-E1-018-01 |
| D-RCV-35 U4 | The case links to its source by business key and reads account, customer and relation data only through the owner's contract | Decision log, D-RCV-35 section 6.1; ADR-010 | FEAT-CWC-02 | 6.1 | ADR-010; CTL-02 | TC-E1-018-01, TC-E1-018-15 |

### 19. Out of scope

- Allocation to a queue and an owner (RWB-P3-E1020-APP).
- Prescription date at creation (RWB-E1-028).
- The EFS collections history hand-over in Epic 2 (RWB-E2-001); the history itself is read through the rwb-source-data contract, not copied.
- Merging a duplicate case (R-UNI-17) and canceling a case created in error (R-UNI-16), Epic 2.
- The read-only case record view (RWB-P3-E1023-APP).
- The load, approval and rollback of the ENTRY and EXCLUSION packages (RWB-P3-E1073-APP).
- The rwb_case schema baseline, the ACE view contract and the reconciliation run (other epics).
- The deployment of this capability: Helm values, topic and queue provisioning, dashboards and the runbook (RWB-P3-E1018-OPS).

### 20. Remaining delivery steps

- Size the story (delivery lead).
- Epic design sign-off (solution architect).
- `listEligibleAccounts` published in the rwb-source-data contract jar and its provider fake published (rwb-source-data service owner, RWB-P1-E1018-APP).
- RWB-P3-E1018-CON done (rwb-case service owner).
- Test data loaded in DEV and Test Cases v9 rows confirmed (QA lead).
