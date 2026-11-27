# RWB-P1-E1002-APP Case list v1 with case ID, owner and queue

### Version 3 changes

- RD-P1-024 with X-27: the case list leaves P1. rwb-case serves it; this story is re-scoped to build the account-page read that rwb-case calls, published in RWB-P1-E1015-CON (findings #1, #2, #3, #4, #5, #7, #8, #9, #11, #17, #18, #22, #23, #25, #26).
- RD-P1-010 and X-06: `listEligibleAccounts` belongs to RWB-P1-E1018-APP and `snapshot(page)` to RWB-P1-E1013-APP; neither is part of this story (findings #6, #20).
- RD-P1-004, RD-P1-005 and RD-P1-011: error answers, contract version 5.1.0 and fake set (findings #10, #14, #15, #19).
- Legacy acceptance criteria AC2 and AC6 to AC17 are withdrawn with the case list; AC18 to AC29 are new for the read (findings #10, #21).
- Pending: the path, schema and maximum keys per call of the read (NEW-GAP-B3) and the unit and scale of the ACE balance (NEW-GAP-S1-4).
- Finishing pass (requests W6-registers-0503, S3-stories-0150, W3-messages-0033; test case backfill): the Test Cases v9 IDs are cited, the retired version 2 rows are stated as retired and the related gaps are cited.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-E1002-APP-16) |
| Patterns applied | DP01, DP02, DP05, DP11, DP14, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1015-CON, RWB-P1-E1069-APP |
| Depends on (build) | RWB-P1-E1015-CON, RWB-P1-E1069-APP, RWB-PLT-N009-CON |
| Contract dependencies | RWB-P1-E1015-CON (publishes the account-page read, section 12.11) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7); the account-page read is added to it once its path is fixed (NEW-GAP-B3) |
| Readiness decisions | RD-P1-004, RD-P1-005, RD-P1-010, RD-P1-011, RD-P1-024, RD-P1-045 |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1002-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v3.md (CAP-P1-010 retired and FR-P1-022 withdrawn; P1 supplies the account-page read, for which the PRD holds no requirement ID of its own) |
| Status | Draft (P1 developer readiness) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-002 for rwb-source-data. The story keeps the case-list build behaviour of the legacy story and moves the builder from the JOB-04 Spring Batch step and its Quartz chain into the Temporal workflow `CaseListBuildWorkflow` on task queue `rwb-source-data`, reads the case through the rwb-case case query contract and ACE data through P1's own views, writes `case_list_row` in schema `rwb_source_data`, and drops the extract file, the outbound file adapter and the Power BI data set under DP-17. Gaps GAP-0485 to GAP-0487 and their assumptions are carried in §12, §13 and §16. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: re-scoped from the case-list build to the account-page read (RD-P1-024, X-27). Agent: S1-stories.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **the case list that rwb-case shows me to carry each account's number, product, total balance, days past due, last contact and last action as the ACE batch holds them, with the date they are true for**, so that **every recovery team works from the same account values and sees how old they are**.

P1 builds one read for this: a page of account keys and a business date in; one entry per account with an ACE row for that date out, from `recovery.v_ace_account` and `recovery.v_ace_efs_action`, in one hop with a 2 s budget (RD-P1-024; DP-05, DP-11). rwb-case calls it. The title and key of the story are kept from the legacy case list.

The case list itself, its screen, its schedule, its feature flag `rwb.p1.case-list` and its freshness line are rwb-case's (RWB-P3-E1002-APP). P1 holds no case list, no `case_list_row` table and no copy of the account values.

### 2. Business rationale

Each recovery team keeps its own list of accounts today, and the lists do not agree with each other or with the source. The one list is composed at read time by rwb-case from its own case rows and P1's account values, so no service stores a copy of another owner's data (RD-P1-024; REQ-RDF-007, REQ-RDF-009).

Only rwb-source-data may read `recovery.v_ace_*` (DP-05, ADR-010), so the account values reach rwb-case only through this read.

**Related gaps.** GAP-0335 (target read of the case list), GAP-1549 (the P3 FSD still describes a direct ACE view read; rwb-case takes these values through this read), GAP-1991 (lake copy; this story keeps no lake path) and GAP-2228 (target form of the case list; GAP-2228 drops the table).

**What changed after version 2.** Version 2 built a daily projection, `case_list_row`, with `CaseListBuildWorkflow` and two case-list operations. Architecture v5 places no case list in P1 and Gap Register v2 GAP-2228 drops the table; the reading of GAP-0048 that kept it in P1 is registered for confirmation (NEW-GAP-X1). GAP-0485 and GAP-0486 are superseded by RD-P1-024.

### 3. Preconditions

- RWB-P1-E1069-APP is done: the Section A views `recovery.v_ace_account` and `recovery.v_ace_efs_action` exist. Both are Section A (Tier 1) views, so the read does not wait for RWB-ACE-001.
- RWB-P1-E1015-CON publishes the account-page read in rwb-source-data.yaml 5.1.0 and its fake. Pending: path, query, request and response schema and maximum keys per call, owner solution architect, tracked as NEW-GAP-B3. The query service and its tests are built now; the REST adapter follows the published path.
- The service login `rwb_source_data` holds SELECT on the `recovery.v_ace_*` views and no privilege on `public` or on any other `rwb_*` schema (DP-02).
- The rwb-case workload identity exists in the environment and the platform guard library can tell it from other callers.

### 4. Flow

1. rwb-case: reads the DP01 freshness answer (RWB-P1-E1015-CON) and takes its business date.
2. rwb-case: calls the account-page read with the account keys of one page of cases and that business date, under its workload identity, with a 2 s timeout.
3. System: refuses a caller that is not authenticated or is not the rwb-case workload identity, and a request with no business date or no account key.
4. System: reads `recovery.v_ace_account` for the requested keys where `data_as_of` equals the business date.
5. System: for the accounts found, reads from `recovery.v_ace_efs_action` the latest row per `account_key`, ordered by `contact_at` and then `efs_record_key`, with `contact_at` at or before the business date 23:59:59 Asia/Bangkok.
6. System: answers one entry per account found: account number (`account_code`), product (`product_category`), total balance (`total_balance`), days past due (`days_past_due`), last contact time (`contact_at`), last action code (`action_code`) and `dataAsOf`.
7. rwb-case: merges the entries with its case rows and shows an account with no entry without ACE values.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A requested key has no `v_ace_account` row for the business date | The answer holds no entry for that key and no zero value; the other entries are returned with status 200; the break is listed by REC-05 (RWB-P1-E1011-APP) | None | AC20, AC22 |
| X2 | An account has no EFS action at or before the business date | The entry is returned with no last contact time and no last action code | None | AC21 |
| X3 | No credential | 401 Problem | MSG-P4-001 | AC24 |
| X4 | A caller other than the rwb-case workload identity | 403 Problem; the refusal is logged; no ACE view is read | MSG-P4-002 | AC25 |
| X5 | The business date is missing or malformed, or no account key is given | 400 Problem naming the field; no ACE view is read | MSG-GEN-001 | AC26 |
| X6 | The ACE database cannot be read, or the read passes the 2 s budget | 503 Problem; no partial page | MSG-GEN-006 | AC27 |
| X7 | More keys than the maximum per call | Pending: maximum and answer, owner solution architect, tracked as NEW-GAP-B3 | Pending | Not covered |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads only P1's two ACE views; its one consumer, rwb-case, builds against the published fake |
| Negotiable | Path and page limit are open (NEW-GAP-B3); the values returned are fixed by RD-P1-024 |
| Valuable | The only way the case list can show ACE account values |
| Estimable | One query service, one REST adapter, one contract test |
| Small | Fits two weeks with its tests |
| Testable | Each criterion below is one automated test on synthetic ACE rows |

### 7. Acceptance criteria

```gherkin
Feature: Account-page read for the rwb-case case list

  Background:
    Given synthetic rows behind recovery.v_ace_account and recovery.v_ace_efs_action with data_as_of 2026-11-30
    Given the caller is the rwb-case workload identity

  Scenario: AC18 One entry per account with its ACE values
    Given account ACC0000123 has product_category MORTGAGE, total_balance 1250000 and days_past_due 96
    Given its EFS actions are one on 2026-11-28 10:00 and one with action_code PTP on 2026-11-30 15:42 Asia/Bangkok
    When the page read is called with business date 2026-11-30 and key ACC0000123
    Then the answer is 200 with one entry holding the account_code of that row, MORTGAGE, 1250000, 96, last contact 2026-11-30 15:42 Asia/Bangkok, last action code PTP and dataAsOf 2026-11-30
    Then no table of rwb_source_data is written and no event is published

  Scenario: AC19 Two actions at the same time are ordered by record key
    Given account ACC0000124 has two actions with the same contact_at, efs_record_key "E-1" with action_code "A1" and "E-2" with action_code "A2"
    When the page read is called for ACC0000124
    Then the last action code of its entry is "A2"

  Scenario: AC20 A key with no ACE row has no entry
    Given account key ACC0000456 has no v_ace_account row
    When the page read is called with keys ACC0000123 and ACC0000456
    Then the answer is 200 with the entry of ACC0000123 only
    Then no entry and no zero balance or zero days past due is returned for ACC0000456

  Scenario: AC21 An account with no contact
    Given account ACC0000125 has a v_ace_account row and no v_ace_efs_action row
    When the page read is called for ACC0000125
    Then its entry holds the account values with no last contact time and no last action code

  Scenario: AC22 Only rows of the requested business date
    Given the views hold data_as_of 2026-11-30
    When the page read is called with business date 2026-11-27 and key ACC0000123
    Then the answer is 200 with no entry
    Then no value of 2026-11-30 is returned under 2026-11-27

  Scenario: AC23 Only the requested keys, whatever their days past due
    Given ACC0000123 at 96 days past due, ACC0000126 at 89 days past due and ACC0000127 not requested
    When the page read is called with keys ACC0000123 and ACC0000126
    Then both are returned and ACC0000127 is not
    Then the entries hold no case number, stage, status, owner, queue or route

  Scenario: AC24 No credential
    Given synthetic rows behind both views for ACC0000123
    When the page read is called without a token
    Then the answer is 401 application/problem+json with messageCode MSG-P4-001
    Then no ACE view is read

  Scenario: AC25 Another caller is refused
    Given a user token of role RW-TEAMMGR and, separately, the rwb-reporting workload identity
    When each calls the page read
    Then each gets 403 with messageCode MSG-P4-002, the refusal is logged and no ACE view is read

  Scenario: AC26 Invalid request
    Given the caller is authenticated as the rwb-case workload identity
    When the page read is called without a business date, then with business date "30-11-2026", then with no account key
    Then each answer is 400 with messageCode MSG-GEN-001 naming the field
    Then no ACE view is read

  Scenario: AC27 ACE database down or too slow
    Given the ACE database refuses the connection, and separately the account query runs longer than 2 s
    When the page read is called
    Then the answer is 503 with messageCode MSG-GEN-006 and holds no entry

  Scenario: AC28 No account key or account number in logs
    Given the calls of AC18, AC20 and AC27
    When the service logs and traces are inspected
    Then they hold the trace ID, the business date and counts, and no account key or account number in clear

  Scenario: AC29 The case list is absent from the build
    Given the release build of rwb-source-data
    When the build, the migrations, the Temporal registrations and the contract jar of rwb-source-data are inspected
    Then there is no case_list_row table, case-list operation, CaseListBuildWorkflow, DailyCaseList Schedule or publish status
    Then the boundary test shows that this read names only recovery.v_ace_account and recovery.v_ace_efs_action
```

**Legacy and version 2 criteria.** AC1, AC3, AC4, AC5 and AC10 stay listed with RWB-ITG-E1002-ITG and are re-scoped there to the rwb-case list (finding #2). AC2, AC6 to AC9 and AC11 to AC17 are withdrawn: they test the case-list build, its run records and the job list. The job list and rerun belong to RWB-P1-AD018-CON (RD-P1-012). The numbers are not reused.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR11 | The account values are read from `recovery.v_ace_account` and `recovery.v_ace_efs_action` at request time; P1 stores no copy | RD-P1-024; DP-05 |
| BR12 | An entry is returned only for a requested key with a row whose `data_as_of` equals the requested business date; missing values are never filled with zero | RD-P1-024 |
| BR13 | Product is ACE `product_category`, passed unchanged | RD-P1-010 rule 5; DF-ACE-010 |
| BR14 | The last contact is per account: the last row in `contact_at`, then `efs_record_key` order, at or before the business date | `GET /efs-history` ordering, rwb-source-data.yaml 5.1.0 |
| BR15 | Account number is `account_code` at its full varchar(255) width; total balance is `total_balance` as the view holds it, with no rounding or rescaling. Pending: unit and scale, owner ACE team lead, tracked as NEW-GAP-S1-4 | DF-ACE-002, DF-ACE-020 |
| BR16 | Only the rwb-case workload identity may call the read; row scope by team is applied by rwb-case before it asks for keys | RD-P1-024; X-27 |

BR1 to BR10 of version 2 are withdrawn with the case list; their IDs are not reused. The entry threshold, the reconciliation tolerance and the allocation wait are not read by this story.

### 9. State transitions

None. The read changes no record and no state.

### 10. Authority

| Who | What they may do |
|---|---|
| rwb-case workload identity | Call the account-page read for the account keys of the cases on the page it is serving |
| Any user token, any other service identity | Refused with 403 MSG-P4-002 |
| rwb-source-data runtime login `rwb_source_data` | SELECT on the two views |

Users reach the values only through rwb-case, which applies the role and team scope of SCR-02 (RWB-P3-E1002-APP).

### 11. Data

| Entity | Fields | Read or write | BR Field ID |
|---|---|---|---|
| v_ace_account | account_key, account_code, product_category, days_past_due, total_balance, data_as_of | Read | DF-ACE-001, DF-ACE-002, DF-ACE-010, DF-ACE-018, DF-ACE-020, DF-ACE-036 |
| v_ace_efs_action | efs_record_key, account_key, action_code, contact_at | Read | DF-ACE-109, DF-ACE-111, DF-ACE-114 for account_key, action_code and contact_at |

No table is created or written. `case_list_row` is not created (RWB-P1-E1001-APP keeps its dictionary rows marked retired). `contact_at` is answered as a date-time, as `contactAt` of `GET /efs-history` is.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`; contract rwb-source-data.yaml 5.1.0, published by RWB-P1-E1015-CON.

| Operation | Request | Answer | Access |
|---|---|---|---|
| Account-page read (path pending, NEW-GAP-B3) | Account keys of one page, one business date | 200 with one entry per account found: account number, product, total balance, days past due, last contact time, last action code, `dataAsOf`; 400 MSG-GEN-001; 401 MSG-P4-001; 403 MSG-P4-002; 503 MSG-GEN-006 | rwb-case workload identity |

Errors use the shared `Problem` schema as `application/problem+json` (RD-P1-004). The read is a query: it needs no Idempotency-Key. `GET /accounts/{id}` of Architecture v5 is the single-account form and is not built here. The operations `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` of version 2 move to RWB-P1-AD018-CON; `GET /case-list/dates/{businessDate}` and `GET /case-list/rows` are withdrawn.

#### 12.2 REST operations consumed

None. The read calls no other service. The case query, allocation, parameter and reference-data calls of version 2 are withdrawn.

#### 12.3 Events published

None.

#### 12.4 Events consumed

None. `rwb.source-data.AceDataReady.v1` does not start anything in this story, and rwb-source-data consumes no event of its own topic (RD-P1-040).

#### 12.5 Workflows and activities

None. `CaseListBuildWorkflow` is withdrawn. `listEligibleAccounts` is the case-entry activity of RWB-P1-E1018-APP and `snapshot(page)` belongs to RWB-P1-E1013-APP.

#### 12.6 Schedules

None. The `DailyCaseList` Schedule is withdrawn; the morning schedule of the list is `rwb-case-caselist-daily` in rwb-case.

#### 12.7 Tables owned

None. The story owns, creates and writes no table.

#### 12.8 Contract fakes

| Fake | Serves | Fixtures |
|---|---|---|
| rwb-source-data account-page fake, published by RWB-P1-E1015-CON once the path is fixed | rwb-case | 200, 400, 401, 403 and 503 (RD-P1-011) |

This story consumes no fake. Its provider tests run against synthetic rows behind the two views and verify the answers against the published contract.

#### 12.9 Call-type summary

| Call type | Provided | Consumed |
|---|---|---|
| REST | 1 (path pending) | None |
| Kafka | None | None |
| Temporal | None | None |
| File | None | None |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.account`, with the published types in the contract module of rwb-source-data.

| Component | Type | Responsibility |
|---|---|---|
| AccountPageQuery | Service | Takes account keys and a business date; returns the entries of section 4; one query per view, set based, never one per account |
| AccountPageRepository | Repository | Reads `recovery.v_ace_account` and `recovery.v_ace_efs_action` with a 2 s statement timeout |
| AccountPageController | REST adapter | Maps the published operation, applies the guard and the Problem mapping; written when NEW-GAP-B3 fixes the path |

**Database.** No migration.

**Feature flag.** The read has no flag of its own: its only caller is behind `rwb.p1.case-list`, which rwb-case owns (RD-P1-024 item 2). Rollback is that flag off first, then the previous image tag (RD-P1-045).

**Build steps**

1. Write AccountPageRepository and AccountPageQuery and test them on a PostgreSQL container with synthetic rows behind both views (AC18 to AC23).
2. Add the 2 s budget, the failure mapping and the log rules (AC27, AC28).
3. Add the REST adapter from the published contract with the guard and the validation (AC24 to AC26).
4. Run the contract test against rwb-source-data.yaml 5.1.0 and the removal and boundary checks (AC29).

**Done when.** The tests of section 16 pass, the published operation answers as its contract says, and no case-list object exists in the build.

### 14. Validation and messages

| ID | When | Status |
|---|---|---|
| MSG-GEN-001 | Business date missing or malformed, or no account key | 400 |
| MSG-P4-001 | No credential | 401 |
| MSG-P4-002 | Caller is not the rwb-case workload identity | 403 |
| MSG-GEN-006 | ACE database unreadable or the 2 s budget passed | 503 |

Texts are those of the Error and Message Standard. MSG-P1-001 and MSG-P1-011 are not raised by this story: the list's freshness message is rwb-case's (RD-P1-024 item 2).

### 15. Screens and states

No Workbench screen is built in this story. The values appear on SCR-02 Case list, which rwb-case builds (RWB-P3-E1002-APP).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1002-APP-01 to TC-P1-E1002-APP-06 | AC18 to AC23 | Integration | Synthetic rows for ACC0000123 to ACC0000127; none for ACC0000456 |
| TC-P1-E1002-APP-07 to TC-P1-E1002-APP-09 | AC24 to AC26 | Contract | No token; RW-TEAMMGR token; rwb-reporting identity; malformed requests |
| TC-P1-E1002-APP-10, TC-P1-E1002-APP-11 | AC27, AC28 | Component | Database refused; slow query; log capture |
| TC-P1-E1002-APP-12 | AC29 | Component | Build, migration, registration and boundary inspection |

The version 2 rows TC-E1-002-01 to TC-E1-002-19 are retired in Test Cases v9. The end-to-end proofs are the TC-E1-002-nn-ITG rows of RWB-ITG-E1002-ITG.

### 17. Guardrails

- ACE data only through `recovery.v_ace_account` and `recovery.v_ace_efs_action`; no statement names `public` or another `rwb_*` schema (DP-01, DP-02, DP-05).
- No copy of ACE values is stored, cached across requests or published.
- Account keys and account numbers are indirect identifiers, Confidential: never written in clear to logs, traces or metrics. If the published path carries keys in the URL, access logs must mask them; the path choice is part of NEW-GAP-B3.
- One hop, 2 s budget; the read calls no further service (DP-11).
- Every fixture is synthetic.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | One case list that agrees with `v_ace_account` | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-18 | 06 Take over and own the case | BR11, BR12 | TC-P1-E1002-APP-01 to TC-P1-E1002-APP-12 |
| REQ-RDF-009 | Source data is shown with its business date | Epic 1, 3.1 | FEAT-RDF-18 | 06 Take over and own the case | BR12 | TC-P1-E1002-APP-01 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1015-CON | Contract | H: publishes the account-page read and its fake |
| RWB-P1-E1069-APP | App development | H: the two views |
| RWB-P1-E1002-OPS | DevOps | X: deploys the read as a delta on RWB-P1-E1015-OPS |
| RWB-P1-E1002-CON | Contract | Retired with a pointer (X-27) |
| RWB-P3-E1002-APP | App development | The consumer: the case list and SCR-02 |
| RWB-P1-E1011-APP | App development | REC-01 and REC-05 against the account views and rwb-case keys |
| RWB-ITG-E1002-ITG | Integration | I: runs the list end to end |

### 19. Out of scope

- The case list, its API, screen, schedule, flag, run record and publish status: rwb-case (RWB-P3-E1002-APP).
- The contract documents and fakes: RWB-P1-E1015-CON.
- The deployment and alerts: RWB-P1-E1002-OPS.
- Reconciliation of the account count and the key breaks: RWB-P1-E1011-APP.
- The job list and rerun operations: RWB-P1-AD018.
- The case-entry activity: RWB-P1-E1018-APP.
- The data lake, extract file, outbound adapter and Power BI data set (DP-17).

### 20. Remaining delivery steps

- Path, query, request and response schema, maximum keys per call and over-limit answer: Pending, NEW-GAP-B3; owner solution architect.
- Unit and scale of ACE `total_balance`: Pending, NEW-GAP-S1-4; owner ACE team lead.
- Size: Not specified (DOR-RWB-P1-E1002-APP-16); owner delivery lead.
- Epic design sign-off: Pending; owner solution architect and business analyst.
- CON Done (RWB-P1-E1015-CON): Pending; owner rwb-source-data contract owner.
- Contract fake published: Pending; owner platform library owner.
- Test data in DEV: Pending; owner QA lead.
