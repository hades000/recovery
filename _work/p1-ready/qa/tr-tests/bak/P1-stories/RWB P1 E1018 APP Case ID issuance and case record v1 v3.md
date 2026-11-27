# RWB-P1-E1018-APP Case ID issuance and case record v1

### Version 3 changes

- RD-P1-010: `GET /entry-candidates` is withdrawn; this story builds the Temporal activity `listEligibleAccounts` with its request, page, candidate, break and failure types and its provider fake (findings #1, #5, #6, #8, #17, #19).
- RD-P1-041 and RD-P1-043: one batch gate (DailyCompletenessGate for DP01, status COMPLETED) with defined answers for an absent view and for the flag off (#7, #8, #9, #11).
- RD-P1-004 and RD-P1-006: the two extension-fact writes take If-Match, with one status table (#2, #12, #13, #20).
- The break set, borrower edges, paging order, log rules and acceptance criteria AC1 to AC20 are rewritten or added (#3, #10, #14, #15, #16, #18, #21 to #25).
- Pending: right and screen owner of the writes (NEW-GAP-S1-6), primary borrower rule (NEW-GAP-S1-7), reading the current version before a write (NEW-GAP-S1-8), deployment verification of the activity (NEW-GAP-S1-9), unit of the balance (NEW-GAP-S1-4), first-write If-Match (NEW-GAP-W1-contracts-1).
- Finishing pass (requests S11-stories-0363, W2-tests-1067, W3-messages-0044; test case backfill): every criterion cites its Test Cases v9 row, TC-ACE-001-09 is carried with AC14, and message texts follow Error and Message Standard v6.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P1-L |
| Ready to start | After RWB-P1-E1015-CON |
| Size | Not specified in the source documents (DOR-RWB-P1-E1018-APP-16) |
| Depends on (build) | RWB-P1-E1015-CON, RWB-PLT-E1071-CON |
| Contract dependencies | RWB-P1-E1015-CON (DailyCompletenessGate); RWB-PLT-E1071-CON (workflow kit). This story publishes the `listEligibleAccounts` interface and its provider fake; the consumer is RWB-P3-E1018-APP |
| Contract version | rwb-source-data 5.1.0: the contract jar (activity) and rwb-source-data.yaml of API Specification v7 (the two PUT operations, base path /api/recovery/source-data/v1) |
| Readiness decisions | RD-P1-002, RD-P1-004, RD-P1-005, RD-P1-006, RD-P1-010, RD-P1-011, RD-P1-041, RD-P1-043, RD-P1-045 |
| Integration dependencies | None |
| External dependencies | None |
| Open decisions | DL10 (message IDs and English texts built now, Thai text from the standard); DL16 (entry at 90 days past due, sent by the caller as the threshold); DL43 (build against the Section B fixture, flag off until RWB-ACE-001; ASM-0816). Working reads of this story: ASM-0813 to ASM-0818 |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v3.md (FR-P1-008, FR-P1-010, FR-P1-016) |
| Status | Draft (P1 developer readiness) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-018 for rwb-source-data. The in-process `AceSourceQuery` reads of the monolith — `accountsAtOrAbove(daysPastDue, businessDate)`, `relationsFor(accountKey)` and `customer(personKey)` — become one REST read of this service, `GET /api/recovery/source-data/v1/entry-candidates` on base `/api/recovery/source-data/v1` (DP-05, DP-11, DP-13), which returns the entry candidates for a business date and a threshold together with the exclusion facts of the four owners joined by business key, behind the ALS batch gate read from `v_ace_batch_status` (DP-05), and writes the two extension facts of case creation 1:1 by business key in schema `rwb_source_data` (DP-01, DP-15). The case ID, the case record, the ENTRY and EXCLUSION packages and the entry decision stay with rwb-case and rwb-decision, and `AceDataReady` and `AceDataLate` stay with RWB-P1-E1015-APP. Gaps GAP-0571 to GAP-0576 and their assumptions are carried in sections 3, 4, 12, 13 and 16. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (27 resolved, 27 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: the entry read becomes the activity `listEligibleAccounts` and the confirmed review findings are fixed or recorded as pending. Where an earlier change log line names `GET /entry-candidates`, version 3 replaces it. Agent: S1-stories.

### 1. Story

As a **case-creation job of rwb-case (SY-CASEWF)**, I want **one activity of rwb-source-data for a business date and a threshold that returns every account in the ACE account view at or above that threshold with its exclusion facts, each fact read from the owner of the field, behind a gate that answers nothing until the ALS batch for that date is complete**, so that **the entry decision is taken on one set of ACE facts that has one owner, one date and no copy, and no case is created from a day whose ACE batch has not arrived**.

This is the source-fact slice of legacy RWB-E1-018. It delivers five things and nothing else:

- **the activity `listEligibleAccounts`** on task queue `rwb-source-data`, namespace `rwb-recovery`: one candidate per account in `v_ace_account` whose `days_past_due` is at or above the threshold and whose `data_as_of` is the business date, carrying `accountKey`, `accountCode`, `productGroup` (the ACE `product_category`), `daysPastDue`, `totalBalance`, `contractNo`, `dataAsOf`, `tdrFlag`, `deceasedFlag` (from `v_ace_customer`), `disputeOpen` (from `account_ext`), `deceasedOverride`, `bankruptcy` and `fraudFlag` (from `party_ext`), and the BORROWER `personKey` resolved through `v_ace_ca_relation` (RD-P1-010; DP-05);
- **the exclusion facts joined by business key only**, each value read in the table or view of its owner — `v_ace_account`, `v_ace_customer`, `account_ext`, `party_ext` — and never copied into another table (DP-01, DP-05);
- **the extension part of case creation**: `account_ext.dispute_open` and the `party_ext` flags — `vulnerable` with `deceased_override`, `bankruptcy` and `fraud_flag` — written 1:1 by business key, with no `id`, no foreign key and no copy of an ACE column (FSD AC-ALT-P1-001-03; DP-01, DP-15);
- **the ALS batch gate**: no fact for a business date whose ALS batch is not COMPLETED in `v_ace_batch_status`; the activity fails non-retryable with `AceBatchNotComplete` carrying MSG-P1-001 (RD-P1-010, RD-P1-041);
- **the break list**: a key the activity reads that has no view row is returned in `breaks[]`, never invented and never turned into a case. The check is REC-05 of the Workbench numbering, which is REC-09 in Data Quality and Reconciliation Rules v4 (GAP-0273).

It does **not** claim the other criteria of the legacy key. It issues and formats no case ID and draws no sequence, writes no `recovery_case`, `case_account` or `case_party` row, and evaluates no ENTRY or EXCLUSION package: the packages belong to rwb-decision and the entry decision, the case row, the links, the primary account and the exclusion record belong to rwb-case (legacy AC1, AC2, AC3, AC4, AC6, AC8, AC10, AC11, AC12, AC15). It serves no case attribute of any kind: case number, status, stage, owner, queue and exposure band are rwb-case's, and this story has no field for them. Legacy AC5 (the state model as data) is owned by the rwb-case slice, legacy AC7 (the threshold boundary) and AC12 (two products, two cases) are proved here only for the facts, legacy AC9 (no cases before the batch is complete) is proved here as the gate of the read, legacy AC13 (a key with no view row) is proved here as the listing, and legacy AC14 (a refused read) belongs to the rwb-access slice and to RWB-ITG-E1018-ITG.

### 2. Business rationale

Every account at 90 days past due or more has to become a case the morning the ACE batch lands, and an account that is deceased, in bankruptcy, under fraud investigation, on an active restructure plan or in an open dispute must not. Today that decision is taken inside one monolith that holds the account copy, the customer copy and the exclusion flags in the same schema, so nobody can say which copy a given answer came from. Under D-RCV-35 the Workbench holds no source copy at all: ACE ingests ALS and SCBPDM, and the Workbench reads them through the 30 `recovery.v_ace_*` views. One read that returns the facts and one owner for each fact is what makes the entry decision auditable; REQ-CWC-001, REQ-CWC-004 and REQ-CHO-004 are answered by it.

**Why the facts are a service of their own.** The views may be read by one login only — `rwb_source_data` (Architecture v5 slides 11 and 29; TSD P1 v3 T6.3) — and no other service may read a `v_ace_*` view at all (Architecture v5 slide 11, the "SQL view" column: "Any other service reading the views" is in the *Never* row). So the facts cannot be assembled by the case service, and an activity of rwb-source-data is the only way the case creation job can see an account, a customer and a relation at all. Keeping that read on the owner side also keeps the four extension tables honest: they are P1's tables (ownership map; TSD P1 v3 T3.5), they are 1:1 with an ACE record, and only the service that owns them may write them.

**Why the read is not the decision.** The ENTRY and EXCLUSION packages are authored by RW-COE, approved by RW-RISK and evaluated by rwb-decision (Temporal and Drools design, slide 15; the package in force check, MSG-P3-027). Handing the case creation job a set of facts, and leaving the threshold, the package and the reason code on the decision side, is what keeps a rule change free of a release: this service returns the same row whether the threshold is 90 or 120, and it returns `dispute_open` whether or not OPEN_DISPUTE is in force. The threshold therefore arrives in the request, not in this service's code, and this story reads no parameter catalog (DP-06 applied as a prohibition).

**Why the gate is here.** CTL-02 and legacy BR7 say that no case is created from an incomplete day, and the record of completeness is the ACE batch record, read through `v_ace_batch_status` — which only this service may read. The gate is therefore on the read, not on the job: a job that asks for a date whose ALS batch is not complete receives the failure `AceBatchNotComplete` with MSG-P1-001 and no facts, and cannot create a case by accident. `v_ace_batch_status` is a Section B view of RWB-ACE-001 (DL43), so the gate has a defined behaviour before the view lands (GAP-0574), and the stamp that names DP01 STALE on a late batch is RWB-P1-E1015-APP's, not this story's.

### 3. Preconditions

- The extension tables `party_ext` and `account_ext` exist in `rwb_source_data` with their business-key primary keys, the seven standard columns including `version`, and no foreign key (RWB-P1-E1001-APP seeds their dictionary rows; RWB-P1-E1069-DB creates them). Build and test use a container with that baseline.
- The Section A views `v_ace_account`, `v_ace_customer` and `v_ace_ca_relation` and the Section B view `v_ace_batch_status` exist as fixtures in DEV and the pipeline; in SIT, UAT and PROD the Section B view and the feature flag wait for RWB-ACE-001 (RD-P1-043; DL43).
- RWB-P1-E1015-CON publishes `DailyCompletenessGate.check(businessDate, productCodes)`; with the product-to-source seed, DP01 is the ALS source (RD-P1-041, RD-P1-021).
- RWB-PLT-E1071-CON is in place: the workflow kit registers activities on task queue `rwb-source-data` in namespace `rwb-recovery` with the payload codec (AES-GCM).
- The login `rwb_source_data` holds SELECT on the `recovery.v_ace_*` views, write rights on its own schema only, and no right on `public` or another `rwb_*` schema (DP-02).
- The parameter `case.entry.dpd` (90, Parameter Catalog v1) is read by the caller, rwb-case. This story reads no parameter.
- The only caller of the activity is `DailyCaseRun` of rwb-case under the rwb-case worker identity. The extension writes are called by the exclusion screen through gateway-bff with the user's token.

### 4. Flow

1. `DailyCaseRun` of rwb-case calls `listEligibleAccounts` with `EligibleAccountsRequest {businessDate, threshold, pageToken, pageSize}`: `businessDate` a date, `threshold` 0 to 999, `pageToken` null for the first page, `pageSize` default 500 and at most 1000.
2. `ListEligibleAccountsActivity` checks the feature flag and the request bounds.
3. It calls `DailyCompletenessGate.check(businessDate, [DP01])`: the ALS row of `v_ace_batch_status` for the business date must have status COMPLETED. Otherwise the activity fails non-retryable with type `AceBatchNotComplete` and details `{productCode: "DP01", messageCode: "MSG-P1-001", lastCompleteBusinessDate}`; `lastCompleteBusinessDate` is null when the view is absent or holds no complete row.
4. A `businessDate` older than the `data_as_of` the views now hold fails non-retryable with type `BusinessDateNotCurrent`. The business date is the `business_date` of the ACE batch record; the views hold current state only.
5. `EntryCandidateService` reads `v_ace_account`, set based, for `days_past_due >= threshold AND data_as_of = businessDate`, ordered by `account_key` ascending, one page of `pageSize` rows after the key held in `pageToken` (keyset paging). Rows with another or empty `data_as_of`, or an empty `days_past_due`, are not candidates; their count is written to the run log.
6. For the accounts of the page it reads the rows of `v_ace_ca_relation` with `relation_type` "BORROWER". Exactly one row gives the `personKey`. No row, or more than one different `personKey`, makes the account no candidate and one break (`keyType` ACCOUNT, `viewName` v_ace_ca_relation). Pending: the rule that picks the borrower among several, owner business analyst, tracked as NEW-GAP-S1-7.
7. It reads `v_ace_customer` once for the borrower keys of the page and takes `deceased_flag`. A borrower with no customer row keeps its candidate with `personKey`, leaves `deceasedFlag` empty and adds a break (`keyType` PERSON, `viewName` v_ace_customer); rwb-case creates no case for it.
8. It reads `account_ext.dispute_open` by `account_key` and `party_ext.deceased_override`, `bankruptcy` and `fraud_flag` by `person_key`. A missing extension row leaves its fields empty (null), never false, and nothing is written.
9. On the first page only, it adds the orphan relations: every BORROWER row of `v_ace_ca_relation` whose `account_key` has no `v_ace_account` row gives an ACCOUNT break (`viewName` v_ace_account), and its `person_key`, when `v_ace_customer` has no row for it, a PERSON break. A break carries `keyType`, `businessKey`, `viewName` and the requested `businessDate`.
10. It answers `EligibleAccountsPage {businessDate, threshold, asOf, candidates[], breaks[], nextPageToken}`; `asOf` is the `completed_at` of the ALS row and `nextPageToken` is null on the last page. No case attribute is served.
11. Exclusion evaluation, the open-case filter and grouping are done by the caller (RD-P1-010 rule 7; GAP-0592).
12. Separately, the exclusion screen calls `PUT /api/recovery/source-data/v1/extension-facts/parties/{personKey}` or `.../accounts/{accountKey}` through gateway-bff with `If-Match`; `ExtensionFactService` writes the one row by business key and answers 200 with the stored row and its `ETag`. ACE is untouched.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An account is below the threshold | Not a candidate | None | AC1 |
| X2 | No `party_ext` or `account_ext` row | The fields are empty, never false; nothing is written | None | AC11 |
| X3 | A key the activity reads has no view row, or the borrower is not exactly one | Returned in `breaks[]` as section 4 steps 6, 7 and 9 say; nothing invented | None | AC5 |
| X4 | The ALS batch is not COMPLETED, or `v_ace_batch_status` does not exist | Non-retryable `AceBatchNotComplete`; no page | MSG-P1-001 | AC4, AC14 |
| X5 | A view raises an error or a statement passes the 5 s statement timeout | The activity fails retryable with messageCode MSG-GEN-006 and no partial page; the retry policy of the catalog applies (1 s initial interval, back-off 2, 10 attempts) | MSG-GEN-006 | AC7 |
| X6 | A write arrives without a credential or without the right | 401 or 403; nothing written | MSG-P4-001, MSG-P4-002 | AC9 |
| X7 | A statement names `public.account` or writes another schema | Refused by the database grant; the conformance test fails the build | None | AC6 |
| X8 | `businessDate` older than the data the views hold | Non-retryable `BusinessDateNotCurrent` | None | AC15 |
| X9 | Request out of bounds | The activity fails non-retryable; details carry MSG-GEN-001 for a missing value or MSG-GEN-002 for a value out of range | MSG-GEN-001, MSG-GEN-002 | AC12 |
| X10 | The flag `rwb.dataengine.entry-candidates` is off | Non-retryable `AceBatchNotComplete` with `lastCompleteBusinessDate` null; no view is read | MSG-P1-001 | AC16 |
| X11 | A write has a missing flag, no `If-Match`, a stale `If-Match`, or the database is down | 422, 428, 409 or 503; nothing written | MSG-GEN-001, MSG-GEN-004, MSG-GEN-006 | AC17, AC18 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the E1015 gate interface, the workflow kit and view fixtures; the consumer builds against this story's fake |
| Negotiable | The internal class split and the page token encoding are the squad's choice; request, page, fields and failure types are fixed by RD-P1-010 |
| Valuable | One read of the day's entry facts with one owner per fact, behind the batch gate |
| Estimable | One activity, one service, two repositories, one writer with two operations, one fake |
| Small | Fits one sprint |
| Testable | Every criterion is one activity call or one write against synthetic rows |

### 7. Acceptance criteria

```gherkin
Feature: Entry candidates and extension facts

  Background:
    Given the flag rwb.dataengine.entry-candidates is on
    Given the business date is 2026-12-01 and v_ace_batch_status holds the ALS row for it with status COMPLETED
    Given the rows of the views are synthetic, with data_as_of 2026-12-01

  Scenario: AC1 Candidates at or above the threshold, one per account
    Given accounts A-5006 at 89 days past due and A-5007 at 90, A-5007 with BORROWER P-0101
    Given mortgage account A-5011 and hire purchase account A-5012 at 91, both with BORROWER P-0103
    Given v_ace_customer rows for P-0101 and P-0103
    When listEligibleAccounts is called with businessDate 2026-12-01, threshold 90, pageToken null, pageSize 500
    Then candidates holds A-5007, A-5011 and A-5012 in that order and not A-5006
    Then A-5007 carries daysPastDue 90, dataAsOf 2026-12-01 and personKey P-0101
    Then A-5011 has productGroup "MORTGAGE", A-5012 "HIRE_PURCHASE", both personKey P-0103
    Then asOf equals completed_at of the ALS row, breaks is empty and nextPageToken is null

  Scenario: AC2 Each fact from its owner
    Given account A-5002 at 92 with tdr_flag true, product_category "HIRE_PURCHASE", contract_no "CN-5002", total_balance 300000 and BORROWER P-0101
    Given P-0101 with deceased_flag true in v_ace_customer
    Given account_ext A-5002 with dispute_open true
    Given party_ext P-0101 with vulnerable false, deceased_override false, bankruptcy true, fraud_flag false
    When the activity is called at threshold 90
    Then the candidate A-5002 carries the account_code of its row, contractNo "CN-5002", totalBalance 300000, tdrFlag true, deceasedFlag true, disputeOpen true, deceasedOverride false, bankruptcy true and fraudFlag false
    Then the candidate has no vulnerable member and no table of rwb_source_data has received an ACE value

  Scenario: AC3 One row per business key, ACE untouched
    Given person "P0000123" and account "A-5005" exist in the views and have no extension row
    When the right-holder puts parties/P0000123 with vulnerable false, deceasedOverride false, bankruptcy false, fraudFlag true
    Then the answer is 200 with the stored row and ETag "1", and party_ext holds one row with fraud_flag true and the seven standard columns
    When the right-holder puts accounts/A-5005 with disputeOpen true
    Then the answer is 200 and account_ext holds one row with dispute_open true
    Then the ACE rows are unchanged, no foreign key links either table to public, and neither table has an id or an ACE column
    # the If-Match value of these first writes is pending, NEW-GAP-W1-contracts-1

  Scenario: AC4 Nothing before the batch is complete
    Given the ALS row for 2026-12-02 has status RUNNING and the latest COMPLETED row is 2026-12-01
    When the activity is called for 2026-12-02
    Then it fails non-retryable with type AceBatchNotComplete and details productCode "DP01", messageCode "MSG-P1-001", lastCompleteBusinessDate 2026-12-01
    Then no candidate or break is returned and no extension row, outbox row or freshness stamp is written
    When the ALS row for 2026-12-02 becomes COMPLETED and data_as_of is 2026-12-02
    Then the same call returns the page for 2026-12-02

  Scenario: AC5 Breaks are listed and never invented
    Given a BORROWER relation of P-0105 on A-5013 with no v_ace_account row for A-5013 and no v_ace_customer row for P-0105
    Given account A-5014 at 91 with BORROWER P-0106 and no customer row for P-0106
    Given account A-5015 at 91 with no BORROWER row, and account A-5016 at 91 with BORROWER rows for P-0107 and P-0108
    When the first page is read
    Then breaks holds ACCOUNT A-5013 v_ace_account, PERSON P-0105 v_ace_customer, PERSON P-0106 v_ace_customer, ACCOUNT A-5015 v_ace_ca_relation and ACCOUNT A-5016 v_ace_ca_relation, each with businessDate 2026-12-01
    Then A-5014 is a candidate with personKey P-0106 and no deceasedFlag value
    Then A-5013, A-5015 and A-5016 are not candidates, and the run log holds the number of breaks by keyType and no key

  Scenario: AC6 No direct ACE read and no case attribute
    Given the service runs as login rwb_source_data
    When it runs SELECT on public.account
    Then the statement is refused with permission denied
    Then EligibleAccountsPage and its candidate have no case number, status, stage, owner, queue or region member
    Then rwb_source_data holds no recovery_case, case_account or case_party table and the login has no privilege on rwb_case

  Scenario Outline: AC7 View failure
    Given <fault> on v_ace_account
    When the activity is called
    Then it fails retryably with messageCode MSG-GEN-006 in its details, returns no partial page and writes nothing
    Then after the view recovers within the 10 attempts the retry returns the whole page
    Examples:
      | fault |
      | the view raises an error |
      | the statement runs longer than 5 s |

  Scenario: AC8 No ACE value is stored
    Given the schema rwb_source_data after its migrations
    When the columns of party_ext and account_ext are compared with DF-EXT-001 to DF-EXT-012 and DF-EXT-027 to DF-EXT-035
    Then the sets are equal and no other table has received a column from v_ace_account, v_ace_customer or v_ace_ca_relation through this story

  Scenario: AC9 Refused callers and withdrawn paths
    Given party_ext "P0000123" and account_ext "A-5005" each hold one row
    When each PUT is sent with no token
    Then it answers 401 with messageCode MSG-P4-001
    When each PUT is sent by a signed-in user without the write right
    Then it answers 403 with messageCode MSG-P4-002 and the row is unchanged
    When GET /entry-candidates and GET /entry-candidate-facts are called
    Then each answers 404
    Then no REST operation reaches listEligibleAccounts and it is registered on task queue rwb-source-data only

  Scenario: AC10 Equal body writes nothing
    Given party_ext "P0000123" holds vulnerable false, deceasedOverride false, bankruptcy false, fraudFlag true at version 1
    When the same four values are put with If-Match "1"
    Then the answer is 200 with the stored row and ETag "1"
    Then version, updated_at and updated_by are unchanged and there is one row

  Scenario: AC11 Absent extension rows stay absent
    Given candidate A-5007 has no account_ext row and P-0101 has no party_ext row
    When the activity is called
    Then disputeOpen, deceasedOverride, bankruptcy and fraudFlag of A-5007 are null and not false
    Then no extension row is written

  Scenario: AC12 Request bounds
    Given one qualifying account for 2026-12-01
    When the activity is called with threshold -1, then 1000, then pageSize 1001
    Then each call fails non-retryable with MSG-GEN-002 in its details and reads no view
    When it is called without businessDate, then without threshold
    Then each fails non-retryable with MSG-GEN-001
    When it is called with threshold 0, threshold 999 and with no pageSize
    Then each is accepted and the last uses pageSize 500

  Scenario: AC13 Paging is complete and stable
    Given 1,201 qualifying accounts, each with one BORROWER and a customer row
    When pages of 500 are read by following nextPageToken
    Then the pages hold 500, 500 and 201 candidates in account_key order, each account once
    Then the third page has nextPageToken null and every page has the same asOf

  Scenario: AC14 Batch view absent
    Given v_ace_batch_status does not exist
    When the activity is called
    Then it fails non-retryable with AceBatchNotComplete, messageCode MSG-P1-001 and lastCompleteBusinessDate null, and returns no page

  Scenario: AC15 Past business date
    Given the views hold data_as_of 2026-12-01
    When the activity is called for 2026-11-30, whose ALS row is COMPLETED
    Then it fails non-retryable with type BusinessDateNotCurrent

  Scenario: AC16 Flag off
    Given rwb.dataengine.entry-candidates is off
    When the activity is called
    Then it fails non-retryable with AceBatchNotComplete and lastCompleteBusinessDate null, and no view is read
    Then the two PUT operations still behave as AC3, AC10 and AC17

  Scenario: AC17 Write validation and failure
    Given party_ext "P0000123" at version 1
    When it is put without fraudFlag, then without If-Match, then with the database unavailable
    Then the answers are 422 with MSG-GEN-001 naming fraudFlag, 428 with MSG-GEN-004 and 503 with MSG-GEN-006
    Then the stored row is unchanged each time

  Scenario: AC18 Concurrent change
    Given two users hold ETag "1" of account_ext "A-5005" with dispute_open false
    When the first puts disputeOpen true and then the second puts disputeOpen false, both with If-Match "1"
    Then the first gets 200 with ETag "2" and the second 409 with MSG-GEN-004
    Then dispute_open stays true

  Scenario: AC19 Personal data is not logged
    Given the calls of AC2, AC3, AC5 and AC17
    When service logs, access logs, metrics, traces and Temporal history are inspected
    Then no clear personKey, accountKey, contract number or flag value is found, keys in PUT paths are masked in access logs and activity payloads are encrypted by the codec

  Scenario: AC20 Rows outside the date predicate
    Given an account at 95 days past due with data_as_of 2026-11-30 and an account with data_as_of 2026-12-01 and no days_past_due
    When the activity is called for 2026-12-01
    Then neither is a candidate and the run log records 2 skipped rows
```

**Where these come from.** AC1 to AC10 keep the scenarios and fixture keys of version 2, restated from the REST read to the activity; AC11 to AC20 are new. The insert into `rwb_case.recovery_case` and the case-number sequence assertions of version 2 AC6 need rwb-case objects and belong to RWB-ITG-E1018-ITG. Legacy criteria owned by the rwb-case, rwb-decision, rwb-access and rwb-document slices stay theirs.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An account is a candidate when `days_past_due` in `v_ace_account` for the ACE business date is at or above the entry threshold; an account below it is never a candidate | Legacy RWB-E1-018 BR1; parameter case.entry.dpd = 90 (DL16); DF-ACE-018 |
| BR2 | The exclusion facts are read from the owner of each field — `v_ace_account.tdr_flag`, `v_ace_customer.deceased_flag`, `account_ext.dispute_open`, `party_ext.deceased_override`, `.bankruptcy` and `.fraud_flag` — by business key, and are never copied | Legacy §3 and BR3; FSD P1 v3 BR-P1-001-2 and BR-P1-001-5; TSD P1 v3 T3.5 |
| BR3 | An extension row is 1:1 with its ACE record, keyed by the business key, with no `id`, no foreign key and no column ACE already holds | FSD P1 v3 BR-P1-001-3, BR-P1-001-5 and AC-ALT-P1-001-03; TSD P1 v3 T3.5 |
| BR4 | No fact is returned for a business date whose ALS batch is not COMPLETED in `v_ace_batch_status`; the activity fails with `AceBatchNotComplete`. That no data job starts for the date is the rule of RWB-P1-E1015-APP and of the caller | Legacy BR7; CTL-02; RD-P1-010; RD-P1-041 |
| BR5 | A key with no view row is returned in `breaks[]` and never invented; it is read again on the next complete batch. How the data steward sees it beyond the run-log count is the REC-05 detail of RWB-P1-E1011-APP (Pending, GAP-1508) | Legacy BR11; D-RCV-35 U4; ADR-010; REC-05 |
| BR6 | This service serves and stores no case attribute: the case number, the status, the stage, the owner and the queue belong to rwb-case | D-RCV-35 U4; Architecture v5 slide 41 (P3 owns case, CMMN state, queues, tasks, allocation, timers) |
| BR7 | The product group of a candidate is the ACE `product_category` value it read; it is returned unvalidated and never coerced into a list value | DF-ACE-010; TSD P1 v3 T3.4; §13 GAP-0576 |

**Coverage.** BR1 by AC1, AC13 and AC20; BR2 by AC2, AC8 and AC11; BR3 by AC3 and AC10; BR4 by AC4 and AC14; BR5 by AC5; BR6 by AC6; BR7 by AC1 and AC2.

**Where each rule lives in the target.** BR1 is the predicate of section 4 step 5 with the caller's threshold, so 90 is never a constant of this service. BR2 and BR3 are the separate owner reads of steps 6 to 8 and the two extension tables. BR4 is the gate of step 3. BR5 is the `breaks` of the page. BR6 is an absence the response types and schema keep. BR7 is a pass-through with no mapping table (GAP-0576).

### 9. State transitions

None in the business sense. This story changes no case status and holds no case. It reads ACE facts and it writes one row per ACE record in two extension tables; a change of an extension row is a version increment on the same key, never a new row.

| From | Event | Condition | To |
|---|---|---|---|
| an account at 89 days past due | the next complete ALS batch | `days_past_due` reaches the threshold for the business date | the account is a candidate row of that date |
| a candidate with no `party_ext` row | the exclusion screen records a flag | The key resolves to a `v_ace_customer` row or is listed by REC-05 | one `party_ext` row for the `person_key` |
| a `party_ext` row with a flag false | the exclusion screen records the same flag true | The caller holds the write right and sends the current `If-Match` | the same row, the flag true, `version` plus one (RD-P1-006) |
| a `party_ext` row | a write with an equal body | None | the same row, `version` unchanged |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case worker identity (`DailyCaseRun`) | The only caller of `listEligibleAccounts` (namespace mTLS); no staff role calls it |
| Exclusion-screen right-holder | Writes the extension facts through gateway-bff with their token. Pending: the roles, permission letter, authorise check code and the story that owns the screen, its confirmation, audit and masking of the answer, owner product owner with compliance, tracked as NEW-GAP-S1-6 (GAP-0573 leaves the right to the screen owner) |
| RW-DATASTEW and ACE team lead | Receive key breaks through the REC-05 work of RWB-P1-E1011-APP (detail store Pending, GAP-1508); change no row |
| RW-PLATADM | Alerted on activity failure by the platform workflow alerts |
| RW-AUDIT | Reads; may not record an exclusion fact |
| rwb-decision (P7) | Owns and evaluates the ENTRY and EXCLUSION packages |
| rwb-case (P3) | Owns the case, entry decision, exclusion record and region and branch attributes |

Each write is authorised by the rwb-access authorise check (DP-08) on the caller's token; no role is allowed until NEW-GAP-S1-6 names one, so tests use the authorise fake granting and refusing a synthetic right. The write sets `updated_by` to the user of the token. The body carries all four party flags, so `vulnerable` is always written by the caller and never defaulted.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-002 | v_ace_account | account_code | Read |
| DF-ACE-006 | v_ace_account | contract_no | Read |
| DF-ACE-010 | v_ace_account | product_category (returned as `productGroup`) | Read |
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
| DF-ACE-181 | v_ace_batch_status | completed_at | Read (the `asOf` of the page) |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-EXT-027 | account_ext | account_key | Read and write |
| DF-EXT-028 | account_ext | dispute_open | Read and write |
| DF-EXT-029 to DF-EXT-035 | account_ext | the seven standard columns | Write |
| DF-EXT-001 | party_ext | person_key | Read and write |
| DF-EXT-002 | party_ext | vulnerable | Read and write |
| DF-EXT-003 | party_ext | deceased_override | Read and write |
| DF-EXT-004 | party_ext | bankruptcy | Read and write |
| DF-EXT-005 | party_ext | fraud_flag | Read and write |
| DF-EXT-006 to DF-EXT-012 | party_ext | the seven standard columns | Write |

Field IDs are those in the Logical Data Model and Data Dictionary, and the view fields those of TSD P1 v3 T3.4.

**Which side is this story's.** `DF-ACE-001` to `DF-ACE-186` are ACE's own columns, read through four `recovery.v_ace_*` views and never stored: the service schema holds no account, customer or relation column at all (DP-05; FSD BR-P1-001-2). `DF-EXT-001` to `DF-EXT-005` and `DF-EXT-027` to `DF-EXT-028` are this story's write surface, with the seven standard columns of each table; `contact_point_ext` (DF-EXT-013 to DF-EXT-026) and `valuation_ext` (DF-EXT-036 to DF-EXT-049) are owned by P1 as well and are untouched here because case creation needs neither a contact point nor an appraisal. Values are passed in the type the view gives: `daysPastDue` and `totalBalance` integers (DF-ACE-018, DF-ACE-020), `tdrFlag` and `deceasedFlag` booleans as the view converts them, keys, codes and `contractNo` strings, dates as ISO dates. Pending: the unit and scale of `totalBalance`, owner ACE team lead, tracked as NEW-GAP-S1-4. No `DF-CAS-*` field appears in this table: the recovery case, its account links and its party links are written by rwb-case in `rwb_case` and read by nobody here (BR6, AC6). No `DF-REF-*` row and no `DF-DEC-*` row is read or written: this story loads no reference data, takes no parameter and records no decision (DP-03 applied as a prohibition, DP-06 and DP-07 applied as prohibitions).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/source-data/v1`, published in rwb-source-data.yaml 5.1.0 (API Specification v7). `GET /entry-candidates` and `GET /entry-candidate-facts` are not published (RD-P1-010).

| Method | Path | Body and answer | Access |
|---|---|---|---|
| PUT | `/extension-facts/parties/{personKey}` | `PartyExtFacts` (`vulnerable`, `deceasedOverride`, `bankruptcy`, `fraudFlag`, all required); 200 stored row with `ETag` | Exclusion-screen right-holder through gateway-bff (right Pending, NEW-GAP-S1-6) |
| PUT | `/extension-facts/accounts/{accountKey}` | `AccountExtFacts` (`disputeOpen`, required); 200 stored row with `ETag` | The same |

Both require `If-Match` (RD-P1-006) and take no Idempotency-Key. An equal body writes nothing. Pending: the `If-Match` value of the first write of a key (NEW-GAP-W1-contracts-1), and how a caller reads the current version of an existing row, since no GET of these rows is published, owner API contract owner, tracked as NEW-GAP-S1-8.

| Condition | Status | messageCode |
|---|---|---|
| Body fails the schema (malformed) | 400 | MSG-GEN-001 |
| A required flag is missing (well-formed) | 422 | MSG-GEN-001 |
| No credential | 401 | MSG-P4-001 |
| No right | 403 | MSG-P4-002 |
| `If-Match` not the current version | 409 | MSG-GEN-004 |
| `If-Match` missing | 428 | MSG-GEN-004 |
| Row cannot be written | 503 | MSG-GEN-006 |

A blank key does not match the path and is not an operation. Errors use the shared `Problem` schema (RD-P1-004). The write answers inside the 2 s budget of DP-11: its statement timeout is not longer than that budget.

#### 12.2 REST operations consumed

`POST` authorise of rwb-access for the two writes (DP-08), faked. No other REST operation: the ACE reads are SQL over `recovery.v_ace_*` through this service's own login (DP-05), and the gate is an in-service interface.

#### 12.3 Events published

None of its own. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (Architecture v5 slides 15 and 41; DP-09). This story reads the same batch row that raises them and publishes no message of its own; it writes no outbox row, and a caller that needs the readiness fact reads the freshness stamp through RWB-P1-E1015-APP's contract.

#### 12.4 Events consumed

None. The activity is called by `DailyCaseRun`; the gate reads `v_ace_batch_status` on each call, so a late batch needs no replay.

#### 12.5 Workflows and activities

| Name | Type | Task queue and namespace | Caller | Retry |
|---|---|---|---|---|
| `listEligibleAccounts` | Activity | `rwb-source-data`, `rwb-recovery` | `DailyCaseRun` of rwb-case (JOB-02) | 1 s initial interval, back-off 2, 10 attempts; `AceBatchNotComplete`, `BusinessDateNotCurrent` and request errors are non-retryable. Pending: start-to-close timeout and heartbeat, tracked as GAP-0143 |

Interface, `EligibleAccountsRequest`, `EligibleAccountsPage`, candidate and break types are published in the rwb-source-data contract jar; payloads pass the codec (AES-GCM). This story registers no workflow; `snapshot(page)`, `AceIngestCheck` and `ReconciliationWorkflow` belong to other P1 stories.

#### 12.6 Schedules

None. The morning run that calls the activity is rwb-case's.

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `party_ext` | `rwb_source_data` | P1 rwb-source-data | 1:1 by `person_key`: the activity reads `deceased_override`, `bankruptcy` and `fraud_flag`; the write sets those and `vulnerable` and the standard columns. `vulnerable` is not returned by the activity |
| `account_ext` | `rwb_source_data` | P1 rwb-source-data | 1:1 by `account_key`: `dispute_open` is read and written the same way. No `id`, no foreign key, no ACE column |
| `contact_point_ext` | `rwb_source_data` | P1 rwb-source-data | Owned by P1, keyed by `contact_key`; untouched here, because case creation reads no contact point |
| `valuation_ext` | `rwb_source_data` | P1 rwb-source-data | Owned by P1, keyed by `valuation_key`; untouched here, because case creation reads no appraisal |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_source_data` | PLT library, in this service's schema | Not written: this story publishes and consumes no message and takes no Idempotency-Key |
| `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation`, `v_ace_batch_status` | `recovery` (ACE-owned schema) | ACE team, read only | SELECT only through the `rwb_source_data` login, one method per view. No copy, no foreign key, no write (DP-05) |

No table of another service is read and no foreign key crosses a schema (DP-01). `recovery_case`, `case_account`, `case_party` and `case_entry_exclusion` stay in `rwb_case` and are neither read nor written here; `v_ace_*` rows are never stored, so there is no table of this service that holds an account, a customer or a relation.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| `listEligibleAccounts` provider fake, published by this story under `fakes/rwb-source-data/5.1.0/` (RD-P1-011; publication pending) | RWB-P3-E1018-APP and RWB-P3-E1018-CON | Two pages, breaks of each kind, `AceBatchNotComplete` with and without a last complete date, `BusinessDateNotCurrent` |
| rwb-access authorise fake | The two writes | Granted and refused calls |
| ACE view fixture | `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation`, `v_ace_batch_status` | The rows of AC1 to AC20, including the absent batch view |
| Extension fixture | `rwb_source_data` | Container with `party_ext` and `account_ext` and their keys |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 PUT operations | rwb-access authorise | `Problem` errors, If-Match |
| Kafka | None | None | |
| Temporal | 1 activity | None | `listEligibleAccounts` |
| File | None | None | |

The four view reads are SELECT only through the `rwb_source_data` login with a 5 s statement timeout (DP-02, DP-05).

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `casefacts`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), Temporal task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P3-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency column is quoted from Template and Rules §R5.5, except the C dependency of DP-04: the contract story of that capability is RWB-P3-E1073-CON, which states the rwb-decision rule operations as consumed, and it is named here in place of the key §R5.5 gives, which has no story file. The metadata of this story carries no build dependency, because it is a Day-1 story of the Wave 1 baseline and builds against the published baseline of rwb-source-data, the published view contract and the RWB-P3-E1018-CON fake before the stories that deliver those three land: the platform contracts in the column above are part of the service template and the Wave 1 cut, not waits of this story (§R5.7 rules 2 and 8). Of the C dependencies in the column above, only DP-11's is named in the metadata of this story, beside the rwb-source-data contract (no story key in the set), and a C dependency never blocks a build.

DP-05 is this story's own pattern: the three `AceSourceQuery` calls of the monolith become one read of P1's own views through P1's own login, and no other service may read a view (Architecture v5 slides 11 and 29). DP-01 applies twice, once to the views (nothing is copied) and once to the two extension tables (P1 writes its own schema, and no foreign key crosses it). DP-02 is the single `rwb_source_data` login that makes both true. DP-15 applies on the service's own sequence, which carries the key assertion of the two extension tables and never a monolith version number.

**DP-03 applies as a prohibition.** The legacy story wrote a decision log entry per created case (legacy step 11, BR8, AC10). That entry is a decision of rwb-case and is recorded in the tenant of rwb-case through the decision-record library of RWB-PLT-E1027-CON; a read of ACE facts is not a decision and this story records none. It holds no `DecisionLogWriter` dependency and publishes nothing on `rwb.decision-record.v1`.

**DP-04 applies as a prohibition.** No Drools kit, no `RuleEvaluator`, no package and no `rule_row` read exists in this story. The ENTRY and EXCLUSION packages are rwb-decision's, evaluated in rwb-decision, and the reason code, the rule ID and the package version are recorded by rwb-case in `case_entry_exclusion`. This story hands over facts only, which is what keeps a package change free of a release on this side.

**DP-06 applies as a prohibition and a boundary.** The threshold is a parameter of rwb-case (`case.entry.dpd`, DL16) and is read by rwb-case; it reaches this service only as the `threshold` argument of one call. This story reads no parameter catalog and holds no default of its own, so a parameter change is invisible here.

**DP-07 applies as a prohibition.** No list is loaded, written or validated here. The product group is returned as the ACE `product_category` value it read (BR7; GAP-0576), and a caller that needs the LOV-PRODUCT label resolves it through the rwb-case reference-data contract.

**DP-09 applies as a statement.** The outbox, inbox and idempotency library objects exist in `rwb_source_data` because every schema of the platform has them, and this story writes none of them: it publishes no event, consumes none, and a GET keeps no stored response. The batch-readiness events belong to RWB-P1-E1015-APP, which owns the outbox rows that raise them.

**DP-10 applies as a statement.** The Quartz job of the monolith becomes rwb-case's event-started `DailyCaseRun` (Architecture v5 slide 44, JOB-02), which is the caller of this read. This story runs nothing on a schedule: the only clock in the flow is the ACE batch record, read per call.

**DP-11 applies as the shape of the read.** What was an in-process interface is a REST operation with a published schema, one hop and a 2 s budget on the caller's side, and a breaker on the caller's side; the read itself answers from the views in one statement set and never calls another service, so no chain of depth greater than one can form.

**DP-14 applies as a statement.** The topic name `rwb.source-data.events.v1` follows the naming library, and this story publishes nothing on it; the two event names it does not own follow the same pattern as `rwb.source-data.<Event>.v1`.

**DP-19 applies to the screens this story serves and does not build.** The exclusion screen of the rwb-case slice arrives through gateway-bff and calls the two extension writes; it never calls this service directly and this story renders nothing.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ListEligibleAccountsActivity` | Temporal activity | The published interface: flag, bounds, gate, failure types |
| `EntryCandidateService` | Service | Predicate, borrower resolution, fact joins, breaks, keyset page (implements the activity, RD-P1-010) |
| `AceSourceReadRepository` | Repository | SELECT only on the views, set based; names no `public` table |
| `ExtensionFactController` | REST adapter | The two PUT operations, guard, `If-Match`, `Problem` mapping |
| `ExtensionFactService`, `ExtensionFactRepository` | Service, repository | One row per business key, version check, equal-body no-op, read-back |

**Migrations (DP-15).** This story adds no migration: `party_ext` and `account_ext`, with `version`, are created by RWB-P1-E1069-DB (RD-P1-021). The conformance test asserts their primary keys, mandatory columns and absence of a foreign key into `public`.

**Database.** Only `party_ext` and `account_ext` are written. No view row is copied and no foreign key crosses a schema (DP-01, DP-05).

**Configuration and reference data**

- The bounds of `threshold` (0 to 999), the page size (default 500, at most 1000; RD-P1-010) and the 5 s statement timeout of the view reads are properties of the service, not business values. The threshold value itself is the caller's parameter (DP-06). About 28,100 accounts qualify on the active inventory, which is 57 pages of 500.
- The source code `ALS` is the value of `v_ace_batch_status.source_system` the gate reads, held as configuration per source and never as a second completeness rule (DP-07 applied as a prohibition).
- The flag `rwb.dataengine.entry-candidates` gates the activity only: off, it fails with `AceBatchNotComplete` and reads no view; in SIT and later it stays off until RWB-ACE-001 is deployed (RD-P1-043).
- No list of values is loaded by this story: the product group is passed through and the reason codes, the packages and the exposure bands stay with rwb-decision and rwb-case (DP-07).

**Build steps**

1. Publish the activity interface, request, page and failure types in the contract jar, and the provider fake.
2. Write `AceSourceReadRepository` with set-based statements and the architecture test that no statement names `public` (AC6).
3. Write the flag, bounds, gate and date checks (AC4, AC12, AC14 to AC16).
4. Write the predicate, keyset paging, borrower and fact joins and breaks (AC1, AC2, AC5, AC11, AC13, AC20).
5. Add the failure mapping, retry options and log rules (AC7, AC19).
6. Write the two PUT operations with `If-Match` and the equal-body rule (AC3, AC8 to AC10, AC17, AC18).
7. Register the activity on the `rwb-source-data` worker and run the contract tests with the consumer fake expectations.

**Feature flag.** `rwb.dataengine.entry-candidates`, as above. Rollback is flag off, then the previous image (RD-P1-045).

**Done when.** AC1 to AC20 pass on the fixtures, the fake is published and no `GET /entry-candidates` exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | Batch not COMPLETED, view absent or flag off (in the failure details) | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A required value is missing | Enter {field}. |
| MSG-GEN-002 | A value is out of range | Per Error and Message Standard v6 |
| MSG-GEN-004 | `If-Match` missing or stale | Per Error and Message Standard v6 |
| MSG-GEN-006 | A view or table cannot be read or written | {system} is not available. Try again in a few minutes. |
| MSG-P4-001 | No credential | Per Error and Message Standard v6 |
| MSG-P4-002 | No right | You cannot {action} here. Your role does not include it. |

{product} is "DP01 Account and arrears" and {date} is `lastCompleteBusinessDate`. When that is null the details carry the code with no date, and the screen text for that case is the reader's: the activity renders no message. {system} is "ACE database". Thai text follows DL10. A synchronous write uses the standard MSG-GEN-006 text as RD-P1-004 assigns it.

### 15. Screens and states

No screen in this story. The exclusion screen that calls the two writes is not built by any story named so far (NEW-GAP-S1-6). The run states of case creation, including the refusal with MSG-P1-001, are rwb-case's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-018-07, TC-E1-018-24, TC-P1-E1018-APP-01, TC-P1-E1018-APP-03, TC-P1-E1018-APP-10 | AC1, AC2, AC11, AC13, AC20 | Component | Accounts A-5002 to A-5012, P-0101, P-0103; 1,201 accounts for paging |
| TC-E1-018-17, TC-E1-018-22, TC-E1-018-23, TC-P1-E1018-APP-07, TC-P1-E1018-APP-08 | AC3, AC9, AC10, AC17, AC18 | Component | "P0000123", "A-5005"; refused users; stale and missing If-Match |
| TC-E1-018-09, TC-P1-E1018-APP-02, TC-P1-E1018-APP-04 to TC-P1-E1018-APP-06 | AC4, AC12, AC14 to AC16 | Component | RUNNING and absent batch rows; out-of-bounds requests; flag off |
| TC-E1-018-13 | AC5 | Component | A-5013 to A-5016, P-0105 to P-0108 |
| TC-E1-018-21, TC-E1-018-25, TC-P1-E1018-APP-09 | AC6, AC8, AC19 | Component | Grants, schema listing, log capture |
| TC-E1-018-20 | AC7 | Component | View error and slow statement |
| TC-E1-018-18, TC-E1-018-19 | Contract of section 12.1; tables of section 12.7 | Component | Contract fake and OpenAPI fragment; `party_ext` and `account_ext` |
| TC-ACE-001-09 | AC14 | Component | `v_ace_batch_status` absent: the activity fails with MSG-P1-001, no page |

The rows above are the Test Cases v9 rows that prove these criteria. TC-ACE-001-09 carries the batch-gate rule removed from RWB-P1-ACE001-DB; here the gate answers the activity failure `AceBatchNotComplete`, not an HTTP 409. TC-E1-018-15 is retired; other TC-E1-018 rows belong to the other slices of the legacy key and are not evidence for these criteria.

### 17. Guardrails

- No business value in code: the threshold arrives in the request and the parameter `case.entry.dpd` is rwb-case's; the source code `ALS` is configuration; no list value, band or reason code is written here (DP-06, DP-07).
- Personal data is carried and is kept out of logs, tests and prompts (Data Classification and Personal Data Inventory v5): `person_key`, `account_key` and `contract_no` are indirect identifiers (Confidential); `deceased_flag`, `vulnerable`, `deceased_override` and `bankruptcy` are Sensitive (Restricted), masked unless the role handles the deviation, never logged, and their read is audited through the ACE Common PII path; `fraud_flag`, `dispute_open`, `days_past_due` and `total_balance` are customer data (Confidential). The read returns no name, address, identity number or contact value, the run log carries counts and key types and never a clear key or a flag value; access logs mask the key segment of the PUT paths, activity payloads are encrypted by the codec, and the audit of a write and the masking of its answer are part of NEW-GAP-S1-6, and test data is synthetic.
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: four SELECT-only view reads through the `rwb_source_data` login, with no `public` table named in any statement and no copy of an ACE column anywhere (DP-05; FSD BR-P1-001-2).
- No foreign key crosses a schema and no extension table carries an `id`: the two writes are 1:1 by business key and the conformance test fails the build on a foreign key into `public` (DP-01, DP-15; FSD AC-EXC-P1-001-04).
- No case attribute is served or stored: the response schema, the entities and schema `rwb_source_data` hold no case number, status, stage, owner, queue or band, and the grant refuses a write into `rwb_case` (BR6; AC6).
- No package is evaluated and no decision is recorded: ENTRY and EXCLUSION stay in rwb-decision and the decision record in the tenant of the story that takes the decision (DP-03, DP-04).
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only, and an applied migration version is never edited (DP-02, DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due (this slice: the facts) | Business Requirements Epic 1, sections 3.3 and 4; Program, section 5.3 | FEAT-CWC-04 | 6.1 Take over the case at 90 days past due | R-UNI-16 | TC-E1-018-07, TC-E1-018-09, TC-E1-018-13, TC-E1-018-17, TC-E1-018-20 to TC-E1-018-25, TC-P1-E1018-APP-01 to TC-P1-E1018-APP-10: AC1, AC4 |
| REQ-CWC-004 | Exclusion rules as data (this slice: the facts and extension writes) | Business Requirements Epic 1, sections 3.3 and 4; Program, section 5.3 | FEAT-CWC-05 | 6.1 | None | TC-E1-018-07, TC-E1-018-09, TC-E1-018-13, TC-E1-018-17, TC-E1-018-20 to TC-E1-018-25, TC-P1-E1018-APP-01 to TC-P1-E1018-APP-10: AC2, AC3 |
| REQ-CHO-004 | One agreed hand-over point in days past due (this slice: the threshold of the request) | Business Requirements Epic 1, section 3.3 | FEAT-CWC-04 | 6.1 Take over the case at 90 days past due | None | TC-E1-018-07, TC-E1-018-09, TC-E1-018-13, TC-E1-018-17, TC-E1-018-20 to TC-E1-018-25, TC-P1-E1018-APP-01 to TC-P1-E1018-APP-10: AC1, AC12 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1018-CON | Contract | Consumer: states `listEligibleAccounts` as consumed and tests against this story's fake |
| RWB-P3-E1018-APP | App development | Consumer: `DailyCaseRun` calls the activity and creates the case |
| RWB-P7-E1018-APP | App development | Sibling: the ENTRY and EXCLUSION packages and their evaluation, which consume the facts this read returns |
| RWB-P4-E1018-APP | App development | Sibling: the access right and the refusal of legacy AC14 |
| RWB-P5-E1018-APP | App development | Sibling: the document slice of this key, which reads the case this read makes possible |
| RWB-P3-E1018-OPS | DevOps | Deployment of the case creation run |
| RWB-P1-E2001-APP | App development | Uses the activity output for the hand-over; `GET /entry-candidate-facts` is withdrawn (RD-P1-010) |
| RWB-ITG-E1018-ITG | Integration | The cross-service proof, including the activity call, the extension writes and the insert refusal on `rwb_case` |
| RWB-P1-E1015-APP | App development | Sibling in the same service: the freshness stamp and the `AceDataReady` and `AceDataLate` events this read relies on and does not own |
| RWB-P1-E1011-APP | App development | Sibling in the same service: JOB-04 Reconciliation, which keeps the durable REC-05 break list this read reports per call |
| RWB-P1-E1001-APP, RWB-P1-E1069-APP | App development, ACE DB | The published baseline and the view contract this story builds against with no build dependency (§3) |

### 19. Out of scope

- Issuing, formatting or reserving a case ID, the yearly number range and the RW-YYYY-NNNNNN rule (RWB-P3-E1018-APP; legacy AC1, AC4, AC11).
- Writing `recovery_case`, `case_account`, `case_party` and `case_entry_exclusion`, the primary account rule, the total outstanding at entry and the exposure band (RWB-P3-E1018-APP; legacy AC1, AC2, AC3, AC12).
- Grouping accounts into a case, skipping an account that already sits on an open case, and the one-case-per-customer-and-product rule (RWB-P3-E1018-APP; legacy AC3, AC8, AC12).
- Evaluating package ENTRY or EXCLUSION, the reason codes, the package-in-force check and the exclusion record (RWB-P7-E1018-APP and RWB-P3-E1018-APP; legacy AC2, AC6, AC15).
- The decision log write for a created case (RWB-P3-E1018-APP; legacy AC10, AC14).
- The case status list, the state model and the refusal of a read without Case record R (RWB-P3-E1018-APP and RWB-P4-E1018-APP; legacy AC5, AC14).
- The freshness stamp of DP01, the STALE flag, `AceDataReady`, `AceDataLate` and the cut-off alert (RWB-P1-E1015-APP).
- JOB-04 Reconciliation, `reconciliation_result` and the durable REC-05 break list (RWB-P1-E1011-APP); this story reports the breaks of one call and keeps no table of them.
- The extension facts beyond case creation — consent and contact quality in `contact_point_ext`, the appraisal decision in `valuation_ext`, and the screens that record a death, a bankruptcy, a fraud or a dispute (the P1 and rwb-case slices of those keys).
- The case record view, the case list and every case attribute (RWB-P3-E1018-APP, RWB-P1-E1002-APP).
- The retention class of the extension rows and the archive of any record (RWB-P1-E1017-APP).

### 20. Remaining delivery steps

- Roles, permission letter, authorise check code and screen story of the two writes, with audit and masking: Pending, NEW-GAP-S1-6; owner product owner with compliance.
- Rule for an account with several BORROWER rows: Pending, NEW-GAP-S1-7; owner business analyst.
- Reading the current version before a write (NEW-GAP-S1-8) and the first-write If-Match value (NEW-GAP-W1-contracts-1): Pending; owner API contract owner.
- Deployment story that verifies the activity registration on the worker (there is no P1 OPS story for this key): Pending, NEW-GAP-S1-9; owner delivery lead.
- Unit and scale of `totalBalance`: Pending, NEW-GAP-S1-4; owner ACE team lead.
- Start-to-close timeout and heartbeat of the activity: Pending, GAP-0143; owner rwb-source-data service owner.
- Source of `region_code` and `branch_code` for the caller: Pending, NEW-GAP-F11-6; owner rwb-case service owner.
- Size: Not specified (DOR-RWB-P1-E1018-APP-16); owner delivery lead.
- Epic design sign-off: Pending; owner solution architect and business analyst.
- CON Done (contract jar and PUT operations) and fake published: Pending; owner contract owner and platform library owner.
- Test data in DEV: Pending; owner QA lead.
