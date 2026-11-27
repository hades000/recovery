# RWB-P1-AD019-APP Data quality and reconciliation console

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Applied RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-021, RD-P1-022, RD-P1-024, RD-P1-040 and RD-P1-042: a delta on the E1011 reconciliation that uses the published result reads, with the case list in rwb-case.
- Fixed the review findings AD019-APP#1–27: REC-05 storage, published reads and schema, errors, dependencies, access, personal data, flag behaviour, test cases and traceability. Added AC8–AC13.
- Open: GAP-1508 and NEW-GAP-S2B-03 (break and orphan detail), NEW-GAP-S2B-02 (page envelope), NEW-GAP-B2 (rwb-case key list), NEW-GAP-S9-4 (data-steward actions), NEW-GAP-S9-5 (flag scope).
- Applied RD-P1-069 (REC-04 and REC-06 computed by rwb-payment, break detail pending and counts asserted), cited the Test Cases v9 IDs of AC8–AC13 and moved the message standard citation to version 6.

| Item | Value |
|---|---|
| Story key | RWB-P1-AD019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP10, DP19 |
| Parallel lane | L-P1-A |
| Size | Not specified |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P1-AD019-APP-14); confirm against the epic design record |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-004; RD-P1-005; RD-P1-011; RD-P1-012; RD-P1-020; RD-P1-021; RD-P1-022; RD-P1-024; RD-P1-040; RD-P1-042; RD-P1-069 |
| Contract fake library | RWB-PLT-LIB `fakes/rwb-source-data/5.1.0/` (RD-P1-011) |
| Ready to start | After RWB-P1-E1011-APP, RWB-P1-E1015-APP and RWB-P1-E1069-APP |
| Depends on (build) | RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1015-APP |
| Contract dependencies | RWB-P1-E1011-CON; RWB-P1-E1015-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-AD019-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v3.md (no FR mapped; no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-019 for rwb-source-data: the JOB-04 reconciliation as an event-started workflow, the result rows in `reconciliation_result`, the REC-05 orphan list, the reconciliation result read API-P1-003 on `/api/recovery/source-data/v1`, and the freshness of every data product consumed from RWB-P1-E1015-APP in-service rather than stamped here. The screen SCR-45 is the rwb-case slice and is mocked; AC3 is proved at the freshness answer and at the STALE marking (DP05, DP10, DP19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-AD019-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 16 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: P1 developer readiness (RD-P1 register); story editor S9-stories.

### 1. Story

As a **data steward (RW-DATASTEW)**, I want **the stored reconciliation results of the existing P1 reconciliation to be available to the data-quality console**, so that **I can inspect a dated break and follow it through the rwb-case list**.

This is a delta on RWB-P1-E1011-APP. E1011-APP owns `ReconciliationWorkflow`, REC-01, REC-02, REC-05 and the writes to `reconciliation_result`; E1011-CON publishes the two result reads, `GET /admin/reconciliation/results` and `GET /admin/reconciliation/results/{resultId}`. AD019-APP adds no operation of its own: it delivers the console behaviour over those reads and, once published, the data-steward actions (RD-P1-022). REC-01 and REC-02 aggregates are stored; REC-05 writes no `reconciliation_result` row. Pending: the store and read of break and orphan detail, owner P1 data architect with the contract owner, tracked as GAP-1508 and NEW-GAP-S2B-03. This story set numbers the business-key orphan check REC-05; it is REC-09 in Data Quality and Reconciliation Rules v4 (GAP-0273, ASM-0363). The case list is owned by rwb-case; P1 has no `case_list_row`, `CaseListBuildWorkflow`, `DailyCaseList`, case-list checks or publish state (RD-P1-022, RD-P1-024). P1 computes REC-01, REC-02 and REC-05 only; REC-04 and REC-06 are computed by the daily reconciliation of rwb-payment, and the held proof-of-delivery rows and the REC-09 break have no published read in P1 version 1 (pending, GAP-0577 and GAP-1508). Until GAP-1508 closes, the result reads answer aggregates and the console and its tests assert counts (RD-P1-069).

Pending: data-steward action contract over reconciliation results (operation, authorisation and audit), owner product owner, tracked as NEW-GAP-S9-4.

### 2. Business rationale

The reconciliation run and its stored results already belong to RWB-P1-E1011-APP. AD019-APP is the console delta over that result contract; it does not start a workflow, write result rows or own the case list.

The reconciliation boundary, built by E1011-APP: REC-01 and REC-02 compare the ACE accounts and balances at or above `case.entry.dpd` with the open case accounts of rwb-case; tolerance is `recon.tolerance.pct` 0.00 version 1, inclusive, with results PASS or BREAK only (RD-P1-042). REC-05 resolves `account_ext.account_key`, `party_ext.person_key`, `contact_point_ext.contact_key`, `valuation_ext.valuation_key`, `interaction.person_key` and `interaction.contact_key` against their `recovery.v_ace_*` views, and `case_account.account_key` and `case_party.person_key` of open cases from a paged rwb-case key-list read (path Pending, owner rwb-case service owner, NEW-GAP-B2). `asset_key` and `payment_code` are outside P1 REC-05 (RD-P1-021, RD-P1-022).

The list and its Schedule belong to rwb-case. No P1 table, copied list or publish state is used. SCR-45 is the composite route of RWB-P3-AD019-APP: gateway-bff calls rwb-case reads, and rwb-case calls the P1 result read.

### 3. Preconditions

- RWB-P1-E1011-APP is the build dependency and owns the reconciliation workflow, `reconciliation_result`, REC-01, REC-02 and REC-05.
- RWB-P1-E1011-CON publishes the two result reads in `rwb-source-data.yaml` 5.1.0 (API Specification v7); the `ReconciliationResult` properties are published, the page envelope is Pending under NEW-GAP-S2B-02.
- RWB-P1-E1015-APP owns freshness stamping, `AceDataReady` and `AceDataLate`; RWB-P1-E1015-CON publishes `GET /data-products/freshness`. AD019 duplicates no write and consumes no event.
- `ReconciliationWorkflow` (workflow ID `recon-{businessDate}`) is started by `AceIngestCheck` as a child with ParentClosePolicy ABANDON after the ALS stamp, with conflict policy USE_EXISTING and reuse policy ALLOW_DUPLICATE; it waits for rwb-case allocation until `caselist.allocation.wait.until` (07:15) (RD-P1-040). No event of another source system starts it.
- The rwb-case reads of REC-01, REC-02 and REC-05 are called by the E1011-APP activity, not by this delta.
- rwb-case owns the case list, `GET /cases`, the list Schedule and its status. P1 has no direct read of P3 tables and no case-list table.
- Data-steward actions are Pending under NEW-GAP-S9-4; this delta adds no write until their contract is published.

### 4. Flow

1. RWB-P1-E1011-APP's existing `ReconciliationWorkflow` runs once per business date as a child of `AceIngestCheck` after the ALS stamp, with ID `recon-{businessDate}` (RD-P1-022, RD-P1-024).
2. The existing activity `reconciliation` writes the REC-01 and REC-02 aggregates to `reconciliation_result`. REC-05 writes no result row: its count is held in the run summary, the decision record and the `job_run_check` row REC-05. A clean or breaking run changes no case-list state. MSG-P1-012 and the Reconciliation break alert are raised by E1011; Pending: alert destination and the balance-break placeholders, tracked as NEW-GAP-S2B-08.
3. The console reads the results with `GET /admin/reconciliation/results`, filtered by `recCode`, `product`, `result`, `from` and `to` (inclusive business dates), and one result with `/{resultId}`. A date with no result row (run not yet complete, FAILED or held) answers 200 with no results. Pending: page envelope, sort, date defaults and limits, tracked as NEW-GAP-S2B-02.
4. Beside the results the console shows freshness from `GET /data-products/freshness` (RWB-P1-E1015-CON): a product with no completed batch for the expected date has status STALE with the business date of its last completed batch and MSG-P1-001.
5. SCR-45 is composed by the route of RWB-P3-AD019-APP; rwb-case calls the P1 result read behind it. P1 does not serve the case list or read `recovery_case`, `case_account` or `case_party` by table.
6. A FAILED reconciliation run is rerun through `POST /admin/jobs/{jobId}/rerun` (RWB-P1-AD018-CON); E1011-APP replaces the rows of the date in one transaction. Data-steward writes are Pending under NEW-GAP-S9-4 and no result row is changed by this delta.
7. `rwb.source-data.reconciliation-run` (registered by RWB-P1-AD019-OPS) starts, stops and skips no reconciliation run: the run is gated by `rwb.source-data.daily-gate` of E1011. No date is consumed by this delta, so none needs catch-up. Pending: which operations the AD019 switch gates, because AD019 publishes none of its own, owner solution architect, tracked as NEW-GAP-S9-5.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Result read is unavailable | The E1011-CON Problem response is returned; no partial result is presented as complete | Per E1011-CON | AC2 |
| X2 | No session; or caller lacks Platform administration R | Refused before repository access | MSG-P4-001; MSG-P4-002 | AC3, AC11 |
| X3 | Malformed date or id; filter value outside its list; `from` later than `to` | 400, 400 or 422 with the failing field | MSG-GEN-001; MSG-GEN-007; MSG-GEN-003 | AC4 |
| X4 | rwb-case key-list operation is not published | The REC-05 open-case comparison of E1011-APP stays blocked; no orphan list is shown | Pending NEW-GAP-B2; owner rwb-case service owner | AC5 |
| X5 | A data-steward write is requested before its contract is published | No write is performed | Pending NEW-GAP-S9-4; owner product owner | AC6 |
| X6 | `rwb.source-data.reconciliation-run` is off | The reconciliation run is unaffected | None | AC13 |
| X7 | `resultId` is not stored | 404 | MSG-P4-003 | AC8 |
| X8 | No result for the date, or the product is stale | 200 with no results; freshness shows STALE | MSG-P1-001 | AC10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds as a delta on E1011-APP and E1011-CON |
| Negotiable | Console behaviour is bounded by RD-P1-022 and RD-P1-024; data-steward actions await NEW-GAP-S9-4 |
| Valuable | Makes existing P1 reconciliation results available to the data-quality console |
| Estimable | Console behaviour over two published reads and the freshness read, with component tests |
| Small | Adds no workflow, migration or copied case list |
| Testable | 13 criteria assert query output, error answers, access, ownership and data minimisation |

### 7. Acceptance criteria

```gherkin
Feature: AD019 reconciliation console delta

  Scenario: AC1 Console query uses the E1011 result contract
    Given REC-01 and REC-02 rows exist in `reconciliation_result` for 2026-11-30
    When the console requests results for that business date with `recCode`, `product`, `result`, `from` and `to` filters
    Then the P1 query uses the RWB-P1-E1011-CON schema and returns the matching stored rows
    And no result is recomputed by the console delta
    And no REC-05 row is returned; orphan detail stays Pending under GAP-1508 and NEW-GAP-S2B-03

  Scenario: AC2 Result read failure uses the published Problem response
    Given the E1011 result store is unavailable
    When the console result query is made
    Then the response matches the E1011-CON Problem schema and no partial response is marked complete

  Scenario: AC3 Read authorization is checked first
    Given the caller lacks Platform administration R
    When the reconciliation result read is requested
    Then 403 MSG-P4-002 is returned before the result repository is read

  Scenario: AC4 Malformed and out-of-list filters are rejected
    Given the queries `from=2026-13-01`, `recCode=REC-05` and `from=2026-11-30&to=2026-11-01`
    When each result read is requested
    Then the answers are 400 `MSG-GEN-001`, 400 `MSG-GEN-007` and 422 `MSG-GEN-003` naming the field
    And no result is returned

  Scenario: AC5 Case-list and case-key data stay with rwb-case
    Given the console composes P1 results with rwb-case case data
    When case-list rows and open-case account/person keys are requested
    Then the list and keys come from rwb-case contracts
    And P1 reads no `case_list_row`, `recovery_case`, `case_account` or `case_party` table
    And the paged key-list path remains Pending under NEW-GAP-B2

  Scenario: AC6 No unsettled data-steward write is performed
    Given a user requests a data-steward action on a reconciliation result
    When NEW-GAP-S9-4 has no published operation, authorisation and audit contract
    Then this delta performs no write and leaves the result unchanged

  Scenario: AC7 Existing workflow remains owned by E1011
    Given a business date is processed
    When reconciliation runs
    Then the only workflow is E1011's `ReconciliationWorkflow`, child of `AceIngestCheck`, with ID `recon-{businessDate}`
    And no second workflow or activity is registered by AD019

  Scenario: AC8 Read one result
    Given a stored REC-01 result of 2026-11-30 for SSME
    When RW-DATASTEW reads it by its resultId, and then reads a UUID that is not stored
    Then the first answer is 200 with resultId, recCode, businessDate, productGroup, sourceCount, workbenchCount, varianceCount, variancePct, tolerancePct and result
    And the second is 404 `MSG-P4-003`

  Scenario: AC9 Filtered read returns only matching rows
    Given PASS and BREAK results of REC-01 and REC-02 for 2026-11-28, 2026-11-29 and 2026-11-30
    When the read is called with recCode=REC-02, result=BREAK, from=2026-11-29 and to=2026-11-30
    Then only REC-02 BREAK rows of those two dates are returned with the stored values

  Scenario: AC10 Stale product and a date with no result
    Given DP01 has no COMPLETED ALS batch for 2026-11-30 and its last completed business date is 2026-11-29
    When the console reads the results and the freshness for 2026-11-30
    Then the result read answers 200 with no results
    And freshness shows DP01 with status STALE and businessDate 2026-11-29 and the console shows MSG-P1-001

  Scenario: AC11 No session and store unavailable
    Given a request with no session, and an authorised request while the result store is down
    When each is sent
    Then the first answers 401 `MSG-P4-001` and the second 503 `MSG-GEN-006`

  Scenario: AC12 No personal data in results or logs
    Given a run with breaks and REC-05 orphans
    When the result answers and the service logs are inspected
    Then they hold counts, percentages, amounts per product group and codes only
    And no account key, person key, contact key or customer name appears

  Scenario: AC13 The AD019 switch does not affect the run
    Given `rwb.source-data.reconciliation-run` is off and `rwb.source-data.daily-gate` is on
    When `AceIngestCheck` commits the ALS stamp of 2026-11-30
    Then the reconciliation child starts as `recon-2026-11-30`
```

Test references: AC1 TC-P1-AD019-APP-01; AC2 TC-P1-AD019-APP-02; AC3 TC-AD-019-03; AC4 TC-AD-019-05; AC5 TC-AD-019-06; AC6 TC-AD-019-07; AC7 TC-AD-019-04. Test Cases v9 holds the rows for the changed texts of AC1, AC4 and AC6.

AC8 TC-P1-AD019-APP-03; AC9 TC-P1-AD019-APP-04; AC10 TC-P1-AD019-APP-05; AC11 TC-P1-AD019-APP-06; AC12 TC-P1-AD019-APP-07; AC13 TC-P1-AD019-APP-08 (Test Cases v9).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | E1011-APP owns the only reconciliation workflow and activity, the REC-01 and REC-02 rows and the REC-05 check | RD-P1-022; X-08 |
| BR2 | AD019-APP is a console delta over `reconciliation_result`; E1011-CON owns the read contract | RD-P1-022 |
| BR3 | The reconciliation workflow is a child of `AceIngestCheck` (ParentClosePolicy ABANDON), starts after the ALS stamp and uses `recon-{businessDate}` | RD-P1-022; RD-P1-040 |
| BR4 | Case list and open-case case keys come from rwb-case contracts; P1 creates no copied case list | RD-P1-024 |
| BR5 | REC-05 checks P1-owned keys and open case account/person keys only; `asset_key` and `payment_code` are excluded | RD-P1-021; RD-P1-022 |
| BR6 | Any data-steward write is Pending until its contract is published | NEW-GAP-S9-4 |
| BR7 | `rwb.source-data.reconciliation-run` gates no reconciliation run; the operations it gates are Pending | RD-P1-022; NEW-GAP-S9-5 |
| BR8 | Tolerance is `recon.tolerance.pct` 0.00 version 1, inclusive; results are PASS or BREAK only, with no NOT_RUN value; a run that cannot proceed writes no row (DL25 option A) | RD-P1-042 |
| BR9 | Result answers, logs and alerts of this delta hold no account, person or contact key and no customer name; such keys are Confidential identifiers | Data Classification and Personal Data Inventory v5 |

### 9. State transitions

This delta adds no workflow state machine. The existing `ReconciliationWorkflow` and its result states are owned by RWB-P1-E1011-APP and follow its contract and the RD-P1-020 `job_run` / `job_run_check` records. There is no publish status; this story changes no case-list status and no reconciliation result.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM (Platform administration R) | Read reconciliation results |
| RWB-P1-E1011-APP | Own workflow, result rows and REC checks |
| RWB-P1-E1011-CON | Publish the reconciliation result read |
| rwb-case | Own case list, open case rows and paged case key list |
| AD019-APP | Implement console query integration over the E1011 result contract |
| No role | Mutates a result through this delta until NEW-GAP-S9-4 settles its action contract |

### 11. Data

| Entity | Owner | Use in this delta |
|---|---|---|
| `reconciliation_result` (DF-OPS-118 to DF-OPS-129) | P1, RWB-P1-E1011-APP | Read through E1011-CON; REC-01 and REC-02 aggregates per business date and product group; no REC-05 row |
| `job_run`, `job_run_check` | P1, RWB-P1-AD018-APP | Existing run status and check evidence per RD-P1-020 |
| P1 business keys listed in section 2 | P1-owned extension and interaction tables | REC-05 input of E1011-APP; not read or returned by this delta |
| Open-case account and party keys | P3 rwb-case | REC-05 input of E1011-APP through the paged key-list contract; path Pending NEW-GAP-B2 |
| Case list | P3 rwb-case | Composed by gateway-bff; not copied into P1 |

P1 reads ACE only through `recovery.v_ace_*`. P1 does not access `recovery_case`, `case_account`, `case_party`, or a case-list table directly. The `asset_key` and `payment_code` REC-05 checks are excluded (RD-P1-021, RD-P1-022).

### 12. Contract

#### 12.1 REST operations

AD019-APP publishes no separate contract. The reconciliation result read is published by RWB-P1-E1011-CON under `rwb-source-data.yaml` 5.1.0.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/admin/reconciliation/results` | RWB-P1-E1011-CON | Filters `recCode` (REC-01, REC-02), `product`, `result` (PASS, BREAK), `from`, `to`; Platform administration R; errors 400, 401, 403, 422, 503 |
| GET | `/admin/reconciliation/results/{resultId}` | RWB-P1-E1011-CON | One `ReconciliationResult`; errors 400, 401, 403, 404, 503 |

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| None by this delta | — | The reconciliation's rwb-case reads belong to E1011-APP; the freshness read is published by RWB-P1-E1015-CON and called by the console side |

The SCR-45 route calls rwb-case reads; rwb-case calls the P1 result read.

#### 12.3 Events published

None by AD019.

#### 12.4 Events consumed

None by AD019. `AceDataReady` is consumed by the E1015/E1011 workflow chain under their own stories.

#### 12.5 Workflows and activities

No workflow or activity is added by AD019. E1011-APP owns `ReconciliationWorkflow` and its single registered activity `reconciliation`. It is a child of `AceIngestCheck` after the ALS stamp with workflow ID `recon-{businessDate}` (RD-P1-022, RD-P1-024). Legacy internal step names are not catalog activities.

#### 12.6 Schedules

None in AD019. P1 has no `DailyCaseList` schedule; rwb-case owns its list schedule.

#### 12.7 Tables

AD019 adds no table or migration. It reads E1011-owned `reconciliation_result` and the P1 run records already specified in RD-P1-020. It creates no case-list table or `publish_status` column.

#### 12.8 Contract fakes

Use the E1011-CON provider fake and the E1015-CON freshness fake pinned to `rwb-source-data.yaml` 5.1.0 at `fakes/rwb-source-data/5.1.0/` (RD-P1-011): page and single results, empty page, 400, 401, 403, 404, 422, 503, and freshness LOADED and STALE.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | Two result reads of E1011-CON; the E1015-CON freshness read | No duplicate P1 endpoint |
| Kafka | None by AD019 | No duplicate consumer |
| Temporal | None added | E1011 owns the reconciliation workflow |
| File | None | No extract or data lake output |

### 13. Solution plan

**Package.** Extend the existing reconciliation result query integration in the P1 application; do not create a second reconciliation module or workflow.

**Components**

| Component | Responsibility |
|---|---|
| ReconciliationResultsQuery | Console filter, by-id and empty-date behaviour over the E1011-CON reads |
| Existing E1011 reconciliation worker | Remains owned and deployed by E1011 stories |

**Database.** No AD019 migration or table. Read `reconciliation_result` as owned by E1011-APP. Do not create `case_list_row`, a break table, or a publish-state field.

**Build steps.** Pin the E1011-CON and E1015-CON fakes; prove the filtered, by-id, empty-date and error answers; prove freshness beside the results; prove the data minimisation; add data-steward actions only once their contract is published.

**Done when.** AC1–AC13 pass against the stored E1011 results, and no workflow, migration, copied list or new operation is introduced by AD019.

### 14. Validation and messages

| Condition | Response |
|---|---|
| Malformed date or id; value outside its list | 400 `MSG-GEN-001`; 400 `MSG-GEN-007` |
| `from` later than `to` | 422 `MSG-GEN-003` |
| No session; unknown `resultId` | 401 `MSG-P4-001`; 404 `MSG-P4-003` |
| Stale product | MSG-P1-001 beside the freshness status |
| Caller lacks Platform administration R | 403 `MSG-P4-002` |
| Result store unavailable | 503 `MSG-GEN-006` |
| Missing P3 key-list path | Pending NEW-GAP-B2; no fallback to a P1 case-list table |
| Unsettled data-steward write | No write; Pending NEW-GAP-S9-4 |

Problem properties and message text follow the shared Problem schema and Error and Message Standard v6; this story adds no message ID or text.

### 15. Screens and states

SCR-45 is the composite route of RWB-P3-AD019-APP; AD019-APP adds no screen. A BREAK result is shown with its stored variance; no case-list HELD or RELEASED state exists in P1. A date with no result shows the empty state and a stale product shows STALE. Pending: SCR-45 empty, error and no-access presentation, owner UX lead, tracked as CG-ALL-2061.

### 16. Test cases

| AC | Test reference |
|---|---|
| AC1, AC2, AC3 | TC-P1-AD019-APP-01, TC-P1-AD019-APP-02, TC-AD-019-03 |
| AC4, AC5, AC6, AC7 | TC-AD-019-05, TC-AD-019-06, TC-AD-019-07, TC-AD-019-04 |
| Section 12 operations and tables | TC-AD-019-19, TC-AD-019-20 |
| AC8, AC9, AC10 | TC-P1-AD019-APP-03, TC-P1-AD019-APP-04, TC-P1-AD019-APP-05 |
| AC11, AC12, AC13 | TC-P1-AD019-APP-06, TC-P1-AD019-APP-07, TC-P1-AD019-APP-08 |

Test Cases v9 holds the rows of the changed criteria (AC1, AC4, AC6). Retired rows TC-AD-019-08 to -18 are not reused.

### 17. Guardrails

- E1011-APP remains the only owner of P1 reconciliation calculations and writes.
- E1011-CON remains the only publisher of the reconciliation result read.
- The case list and case keys are sourced from rwb-case contracts; no P1 copy or direct P3 table read.
- REC-05 covers P1-owned keys plus open-case account/person keys only; no `asset_key` or `payment_code` scope.
- No AD019 workflow, activity, consumer group, Schedule, migration or table is added.
- Pending actions are not implemented without their published contract and audit behaviour.

### 18. Traceability

| Requirement | Source | Test reference |
|---|---|---|
| REQ-RDF-007 (FEAT-RDF-03): reconciliation results reach the console | RD-P1-022; E1011-CON | TC-P1-AD019-APP-01 |
| REQ-RDF-008 (FEAT-RDF-16): reconciliation breaks and referential completeness | RD-P1-022; GAP-1508 | TC-P1-AD019-APP-01 |
| REQ-RDF-009 (FEAT-RDF-14): stale data products are visible | RWB-P1-E1015-CON; AC10 | TC-P1-AD019-APP-05 |
| Case list remains with rwb-case | RD-P1-024 | TC-AD-019-06 |
| P1 case-key comparison uses the rwb-case contract | RD-P1-022; NEW-GAP-B2 | TC-AD-019-06 |
| ACE reads only through source-data views | D-RCV-60; RD-P1-021 | TC-AD-019-20 |

### 19. Out of scope

- Building or changing `ReconciliationWorkflow`, REC-01/02/05 calculations, or `reconciliation_result` writes (RWB-P1-E1011-APP).
- Publishing the reconciliation result contract (RWB-P1-E1011-CON).
- Owning case lists, case keys, case-list schedules, or case tables (rwb-case; RD-P1-024).
- Implementing data-steward write actions before NEW-GAP-S9-4 is resolved.
- Console page and SCR-45 composite route (RWB-P3-AD019-APP, RWB-PLT-N001-CON).
- ACE freshness stamps and events (RWB-P1-E1015-APP).

### Remaining delivery steps

- Size: Pending squad refinement; owner delivery lead.
- Epic design sign-off: Pending; owner solution architect.
- CON Done: Pending; owner contract owner.
- Contract fake published at the approved version: Pending; owner contract owner.
- Synthetic test data in DEV: Pending; owner test data owner.