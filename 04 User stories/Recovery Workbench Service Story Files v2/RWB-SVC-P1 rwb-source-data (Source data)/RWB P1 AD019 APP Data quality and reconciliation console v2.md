# RWB-P1-AD019-APP Data quality and reconciliation console

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

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
| Size | Not specified in the source documents (DOR-RWB-P1-AD019-APP-16); the squad sizes it at refinement |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P1-AD019-APP-14); confirm against the epic design record |
| Contract version | Not specified in the source documents (DOR-RWB-P1-AD019-APP-23); the path is /api/recovery/source-data/v1 |
| Contract fake library | Not specified in the source documents (DOR-RWB-P1-AD019-APP-22) |
| Ready to start | After RWB-P1-E1015-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P1-E1015-APP, RWB-P1-E1069-APP, RWB-P1-E1011-CON |
| Contract dependencies | RWB-P1-E1011-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-AD019-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-019 for rwb-source-data: the JOB-04 reconciliation as an event-started workflow, the result rows in `reconciliation_result`, the REC-05 orphan list, the reconciliation result read API-P1-003 on `/api/recovery/source-data/v1`, and the freshness of every data product consumed from RWB-P1-E1015-APP in-service rather than stamped here. The screen SCR-45 is the rwb-case slice and is mocked; AC3 is proved at the freshness answer and at the STALE marking (DP05, DP10, DP19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-AD019-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 16 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW) and a data product owner of the reconciliation**, I want **the daily reconciliation of the case list to ACE to run as JOB-04 on the workflow kit for the business date of the ACE batch, to write one result per check and product group, to list every REC-05 orphan with its table, its column and its key, and to answer the results and the orphans on one read operation of rwb-source-data**, so that **a break, an orphan or a stale data product is named with its business date before a route decision uses it**.

The deliverable is the half of legacy RWB-AD-019 that the P1 Recovery data engine keeps under D-RCV-60: the run, the result and the read. It has four parts.

- **JOB-04 Reconciliation as an event-started Temporal workflow.** `ReconciliationWorkflow` runs on task queue `rwb-source-data` in namespace `rwb-recovery`, started by `AceDataReady` after the case list build of the business date, through the workflow kit (DP-10, H RWB-PLT-E1071-CON; Architecture v5 slide 44 records JOB-04 as an event-triggered workflow in rwb-source-data, and JOB-05 is retired). The P1 slice runs no Temporal Schedule of its own for the console; the 15-minute freshness Schedule stays with rwb-case. It reads `v_ace_account` for the business date in `data_as_of`, takes away the accounts excluded at entry, compares the result with `case_list_row` per product group, runs REC-01 count, REC-02 balance and REC-05 business-key resolution, and writes one `reconciliation_result` row per check and product group (DF-OPS-118 to DF-OPS-129).
- **The REC-05 orphan list.** Every business key on a Workbench row that resolves to no view row is listed with its table, its column and its key, for the data steward and, where the row is missing in ACE, for the ACE team. It never deletes or changes a Workbench record or an ACE row (BR-P1-011-3; FSD P1 v3 A2.11.3).
- **The reconciliation result read.** `GET /api/recovery/source-data/v1/admin/reconciliation/results` (API-P1-003, Platform administration R) replaces the withdrawn `/admin/data-quality/exceptions`. It serves the REC-01 and REC-02 results and the REC-05 orphans of a business date in one hop, and both the console slice RWB-P3-AD019-APP and the harness slice RWB-ITG-AD019-ITG read it.
- **The freshness answer consumed, not written.** The freshness of every data product (`data_product_load`, read from `v_ace_batch_status`) is RWB-P1-E1015-APP's. This story asks `FreshnessQuery` for the stamp of the products its run reads, in service and over no REST hop, and stamps nothing. The stale-product answer the console shows is E1015's; what this story proves is the STALE marking and its message on the run it starts (ASM-0715).

**No screen.** SCR-45 Data quality is the gateway-bff route over the three console reads of rwb-case (DP-19, H RWB-PLT-N001-CON; RWB-P3-AD019-APP). This story builds no route, no page and no report, and it adds no extract and no Power BI data set (DP-17). The read shape of the reconciliation operation and of the REC-05 break list is Not specified in the source documents (GAP-0519; ASM-0713), and so is DP-10's placement on this slice (GAP-0520; ASM-0714).

### 2. Business rationale

Under D-RCV-35 the Workbench loads no source data. ACE ingests the account, the arrears, the balances and the batch record, and rwb-source-data reads them through the 30 read-only `recovery.v_ace_*` views on its own login (DP-05; ADR-010; Arch v5 slide 41). That removed the load and left the data quality question where it always was: an account that reaches 90 days past due in ACE and has no case is recovery work nobody does, and a business key with no ACE row is a broken link that no foreign key will catch (FSD P1 v3 A2.11.1).

The legacy console saw the answer late. It read the reconciliation and data quality extract that the reconciliation step of JOB-04 writes, and the freshness stamp in `data_product_load`; it had no endpoint of its own, and the data quality exception endpoint was withdrawn with the exception table (legacy RWB-AD-019 "Endpoints"; TSD P1 v3 T-A.1 note on API-P1-003). The result of that arrangement was that the break, the orphan and the stale product were seen by the team that ran the job and by nobody else, and a product a day behind reached a route decision before anyone noticed (FSD P1 v3 A2.12.1).

This story keeps the half that is a data engine question and hands the half that is a case question to rwb-case:

| Legacy part | Where it lands | Why |
|---|---|---|
| The JOB-04 reconciliation run, REC-01 to REC-05, and `reconciliation_result` | Here | The run compares ACE rows to the case list rows, both read by the service that owns the views and the case list |
| The REC-05 orphan list and its read | Here | The orphan is a business key with no source row, so the service that reads the source answers it |
| The reconciliation result read (API-P1-003) | Here | The read is a resource of this service, one hop, Platform administration R |
| The freshness stamp and the stale flag | RWB-P1-E1015-APP, consumed here | Freshness comes from the ACE batch record and has one writer |
| SCR-45 and its three console reads | RWB-P3-AD019-APP | The screen annotates a break key with the case, the queue and the owner held in `rwb_case` |
| The cross-service proof | RWB-ITG-AD019-ITG | End-to-end evidence is a harness, not a service |

The control intent is unchanged: the case list reconciles to the ACE count of accounts at 90 or more days past due with no unexplained variance (REQ-RDF-007, NFR-018, DL25), every business key on a Workbench table resolves to an ACE row (REC-05), and every data product carries a freshness stamp from the ACE batch record (REQ-RDF-009). The legacy acceptance criteria AC1 and AC2 are the screen and the referential proof of that intent and stay with RWB-P3-AD019-APP and RWB-ITG-AD019-ITG; AC3 is the stale product, and this story owns it at the freshness answer and at the STALE marking the run relies on (ASM-0715).

Two things the legacy story never had to say are said here. **First**, the run is an event, not a job row: `AceDataReady` starts the workflow once per business date, the inbox dedupes on the event id, and there is no shared Quartz table and no scheduler console (DP-10; Arch v5 slide 44). **Second**, the run leaves no run table: its record is the Temporal visibility record of the workflow and its activities, read through the workflow kit (ASM-0723; GAP-0519).

### 3. Preconditions

- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, with the typed workflow and activity contract, the worker versioning rule and the visibility read of a run (DP-10).
- RWB-P1-E1011-CON is published: the reconciliation contract baseline on base `/api/recovery/source-data/v1`, with the OpenAPI document of the result reads, the AsyncAPI fragment of `rwb.source-data.AceDataReady.v1`, the typed `ReconciliationWorkflow` and `reconciliation` contract, the published `ReconciliationQuery` interface, the result and break-row schemas with their field IDs, the error envelope and the four contract fakes.
- RWB-P1-E1015-APP is done: `data_product_load` is written from `v_ace_batch_status`, `AceDataReady` (EV-26) and `AceDataLate` (EV-27) are published on `rwb.source-data.events.v1` through the outbox, and `FreshnessQuery` answers `stampFor`, `stampForRow` and `stampsFor` as a typed interface of this service.
- RWB-P1-E1069-APP and RWB-P1-E1069-DB are done: the 30 read-only `recovery.v_ace_*` views exist on the per-service Flyway sequence, the `rwb_source_data` login holds SELECT on them and nothing in `public`, and the conformance test is in the pipeline (DP-05, DP-15).
- RWB-P1-E1001-APP is done: `reconciliation_result`, `case_list_row`, `data_product_load`, `data_product`, `data_product_access` and the dictionary tables exist in schema `rwb_source_data`, and the outbox, inbox and idempotency objects of the event library are created there (DP-01, DP-09).
- RWB-P1-E1002-APP is done: the daily case list build writes `case_list_row` for the business date, with `publish_status` as its own column, so the reconciliation has a workbench count and a balance sum to compare.
- The accounts excluded at entry are read through the case-query element of the contract baseline (RWB-P1-E1011-CON section 12.2), one hop and 2 s: the table `case_entry_exclusion` belongs to rwb-case (P3) and is never read by table here (DP-01, DP-05).
- The tolerance `recon.tolerance.pct`, the entry threshold `case.entry.dpd`, and the lists `LOV-PRODUCT` and `LOV-REC-RESULT` arrive through the parameter and reference-data elements of the same baseline; no tolerance is written in code (BR-P1-011; DP-06, DP-07).
- The guard of the published operation answers on the rwb-access authorise contract: the read runs only on Platform administration R, with the scope applied, and a deny refuses the call before any view is read (DP-08).
- The rwb-source-data login is the `rwb_source_data` login of Architecture v5 slide 29; its name is fixed and its credential is a secret reference, never a value in a file.
- The shape of the reconciliation read and of the REC-05 break list is Not specified in the source documents (GAP-0519; ASM-0713). The read is built against the result and break-row schemas of RWB-P1-E1011-CON and the field IDs of `reconciliation_result`, and the shape is fixed there.
- No build dependency blocks the start beyond H: the five H rows are platform contract stories and same-service stories. The wave 4 tag is the W-MAP tag of EP08 and does not delay the build (Template and Rules section R5.7; GAP-0520; ASM-0714).

### 4. Flow

1. **Trigger.** rwb-source-data consumes `rwb.source-data.AceDataReady.v1` from `rwb.source-data.events.v1` through its inbox, dedupes on the event id, and takes `sourceSystem`, `businessDate`, `status` and `completedAt` from the CloudEvents payload (DP-09, DP-14). No field of the payload is personal data.
2. **Start.** `ReconciliationWorkflow` is started once per business date, workflow ID `recon-{businessDate}`, on task queue `rwb-source-data`, with the business date, the source system and the event id as its input. A second delivery of the same event starts nothing (BR4).
3. **Gate.** The workflow calls `DailyCompletenessGate.check` of RWB-P1-E1015-APP and reads `FreshnessQuery.stampForRow("DP01", businessDate)` in service. When the ALS batch of the business date is not COMPLETE, the run does not proceed for that date and the answer carries DP01 with its last complete business date, status STALE and MSG-P1-001 (BR7, AC3 pattern).
4. **Case list gate.** The workflow reads `case_list_row` for the business date. No row for the date means the case list build has not finished: the run waits for its own retry window and then fails with MSG-GEN-006 naming the case list step, and writes no result row (X2).
5. **`runRec01`.** Reads `v_ace_account` for the business date in `data_as_of` at `days_past_due` at or above the entry threshold, takes away the accounts excluded at entry read through the case-query element, counts the remainder per product group, and compares it with the `case_list_row` count of the same product group (REC-01).
6. **`runRec02`.** Sums `v_ace_account.total_balance` for the same rows per product group and compares it with the `case_list_row.total_balance` sum of the same product group (REC-02).
7. **`resolveRec05`.** Pages the distinct business keys held on a Workbench row and resolves each against its view: `account_key` in `v_ace_account`, `person_key` in `v_ace_customer`, `asset_key` in `v_ace_asset` and `payment_code` in `v_ace_payment`. A key with no view row is an orphan and is recorded with its table, its column and its key, and a count and an amount per product group (REC-05).
8. **`writeReconciliationResult`.** Writes one `reconciliation_result` row per check and product group for the business date: `rec_code`, `business_date`, `product_group`, `source_count`, `workbench_count`, `source_amount`, `workbench_amount`, `variance_count`, `variance_pct`, `tolerance_pct` and `result` (DF-OPS-118 to DF-OPS-129). The variance and the variance percent are computed once, here, from the tolerance in force, and are never recomputed by a reader.
9. **Publish state.** When every REC-01 and REC-02 result of the date is PASS the workflow leaves the case list RELEASED; when any is BREAK it sets `case_list_row.publish_status` to HELD for the date and raises MSG-P1-012 with the date, the product, the variance and the percent (FSD P1 v3 A2.13; BR6).
10. **Orphan notice.** A REC-05 orphan is never repaired by the run: it is listed for the data steward and, where the row is missing in ACE, for the ACE team, and the run changes no Workbench record and no ACE row (BR-P1-011-3, BR5).
11. **Run record.** The workflow writes no run table. Its record is the Temporal visibility record of the workflow and its activities, with the search attributes `BusinessDate` and `RecSource`, read through the workflow kit (ASM-0723).
12. **Read.** A caller asks `GET /api/recovery/source-data/v1/admin/reconciliation/results` with `recCode`, `product`, `result`, `from` and `to`. The guard checks Platform administration R and the scope, the query service reads `reconciliation_result` and the break rows of the date range, and the answer carries the results and the REC-05 orphans, each with its business date, in one hop (API-P1-003).
13. **Console.** rwb-case's console reads call this operation behind the gateway-bff route of SCR-45 (DP-19, RWB-P3-AD019-APP), and the harness of RWB-ITG-AD019-ITG calls it directly. Neither is built here and neither adds a field: the break rows arrive as this operation publishes them.
14. **No write from a reader.** No read of this story writes a row, stamps a product or acknowledges a break. The console records no acknowledgement and this service holds no acknowledgement column (BR9).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `v_ace_account` returns an error after the MORTGAGE count is read | No `reconciliation_result` row for the business date is written, the run ends FAILED and the visibility record names the activity and the view, and a rerun from the job monitor writes all six rows (FSD P1 v3 AC-EXC-P1-011-02) | MSG-GEN-006 for system "ACE database" | AC3 pattern; TC-AD-019-03 |
| X2 | No `case_list_row` exists for the business date | The run waits its retry window, then ends FAILED; no result row is written for the date and no break is shown as zero | MSG-GEN-006 naming the case list step | AC4; TC-AD-019-05 |
| X3 | `AceDataReady` arrives twice with the same event id | The inbox dedupes, the workflow starts once and no second result row is written | None | AC5; BR4; TC-AD-019-06 |
| X4 | The ALS batch of the business date is not COMPLETE at the gate | The run does not proceed for the date; the answer names DP01 with its last complete business date, status STALE and the warning, and no result row is written | MSG-P1-001 | AC3 |
| X5 | A business key on a Workbench row has no view row | The REC-05 result is BREAK for that product group and the orphan is listed with its table, its column and its key; the Workbench row and the ACE rows are unchanged | None | AC10; BR5; TC-AD-019-10 |
| X6 | A result is BREAK over the tolerance | The case list of the date is HELD and the warning names the date, the product, the variance and the percent; no case is changed | MSG-P1-012 | AC6; BR6; TC-AD-019-07 |
| X7 | The caller's Platform administration R is absent | The call is refused before any read; no row is returned and nothing is written | MSG-P4-002 | AC7; TC-AD-019-04 |
| X8 | The query carries a malformed `from` or `to` date | The call is refused before any read, naming the field | MSG-GEN-001 | AC8; TC-AD-019-08 |
| X9 | The freshness answer of E1015 names a product with no complete batch and no last complete date | The run is not started for that date, and the product is never reported as current | MSG-P1-001 | AC3 |
| X10 | The parameter read of the baseline does not answer | The run ends FAILED and no result is written with a default tolerance; no tolerance is assumed in code | MSG-GEN-006 | AC9; BR8; TC-AD-019-09 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds one workflow with four activities, one repository over `reconciliation_result`, one read operation and one consumed event; the freshness is read through E1015's typed interface and the cross-service reads are stubbed in the contract fakes |
| Negotiable | The element names of the read are fixed by RWB-P1-E1011-CON; the internal split of the run into four activities, the retry policy and the paging of the resolve step are design choices |
| Valuable | The break, the orphan and the stale product are computed once, by the owner of the ACE views, and reach the console with their business date |
| Estimable | One workflow, four activities, one repository, one controller, one read operation, one consumer and two test cases |
| Small | Fits one sprint with its tests, on top of the contract and freshness stories it depends on |
| Testable | Every owned criterion is one automated test on synthetic view fixtures with no ACE data; the transport is the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Data quality and reconciliation console

  Scenario: AC3 A stale data product (legacy RWB-AD-019 AC3)
    Given a data product past its expected business date
    Given the rwb-case contract mock returns the console read of a data product past its expected business date, with its last complete ACE business date
    When I open the console
    Then it shows as stale with its last complete ACE business date

  Scenario: AC4 A business date with no case list row (new, D-RCV-60)
    Given no case_list_row exists for the business date
    When the reconciliation run of that date waits its retry window
    Then the run ends FAILED, no reconciliation_result row is written for the date, no break is shown as zero, and MSG-GEN-006 names the case list step

  Scenario: AC5 A redelivered AceDataReady event (new, D-RCV-60)
    Given AceDataReady arrives twice with the same event id
    When the inbox dedupes the second delivery
    Then the workflow starts once and no second reconciliation_result row is written

  Scenario: AC6 A result over the tolerance holds the case list (new, D-RCV-60)
    Given a REC-01 or REC-02 result of the business date is BREAK over the tolerance
    When the run completes
    Then the case list of the date is HELD, MSG-P1-012 names the date, the product, the variance and the percent, and no case is changed

  Scenario: AC7 A caller without Platform administration R (new, D-RCV-60)
    Given the caller's Platform administration R is absent
    When the caller asks for GET /admin/reconciliation/results
    Then the call is refused before any read with MSG-P4-002, no row is returned and nothing is written

  Scenario: AC8 A malformed query date (new, D-RCV-60)
    Given the query carries a malformed from or to date
    When the caller asks for GET /admin/reconciliation/results
    Then the call is refused before any read and MSG-GEN-001 names the field

  Scenario: AC9 A parameter read that does not answer (new, D-RCV-60)
    Given the parameter read of the baseline does not answer
    When the reconciliation run starts
    Then the run ends FAILED, no reconciliation_result row is written with a default tolerance, and MSG-GEN-006 is shown

  Scenario: AC10 A REC-05 orphan (new, D-RCV-60)
    Given a business key on a Workbench row has no view row
    When REC-05 resolves the business keys
    Then the result for that product group is BREAK, the orphan is listed with its table, its column and its key, and the Workbench row and the ACE rows are unchanged

  Scenario: AC11 Reconciliation rules hold on every run (new, D-RCV-60)
    Given a reconciliation run for one business date
    When the run completes
    Then rules BR1, BR2, BR3, BR4, BR5, BR6, BR8, BR9, BR10 and BR14 of section 8 hold for that run

  Scenario: AC12 A provided operation answers 401, 403 or 404 (new, D-RCV-60)
    Given a caller of GET /api/recovery/source-data/v1/admin/reconciliation/results
    When the call carries no valid credential, the caller lacks Platform administration R, or the operation answers not found (the 404 condition is Not specified in the source documents (NEWAC-RWB-P1-AD019-APP-AC11))
    Then the answer is 401, 403 or 404 respectively, no row is returned and nothing is written

  Scenario: AC13 A consumed event delivered again after its run has completed (new, D-RCV-60)
    Given AceDataReady with an event id has been consumed and its run has completed
    When the same event is delivered again
    Then the inbox dedupes it, the workflow starts nothing and no second reconciliation_result row is written

  Scenario: AC14 A run activity is retried or times out (new, D-RCV-60)
    Given an activity of the reconciliation run fails or times out
    When the activity is retried within the retry window of the run
    Then a retry that completes lets the run continue, and an activity that does not complete ends the run FAILED with no reconciliation_result row written for the date

  Scenario: AC15 A consumed call fails or does not answer (new, D-RCV-60)
    Given a call the run consumes, an ACE view or the freshness interface, does not answer
    When the run reads it
    Then the run ends FAILED, no reconciliation_result row is written for the date and MSG-GEN-006 is shown

  Scenario: AC16 A status change the model does not allow is refused (new, D-RCV-60)
    Given the case list of a business date has a publish_status in case_list_row
    And the allowed changes of publish_status are Not specified in the source documents (NEWAC-RWB-P1-AD019-APP-AC15)
    When a status change that the publish status model does not allow is attempted
    Then the change is refused, case_list_row keeps its status and no case is changed
```

AC3 is copied character for character from legacy RWB-AD-019, and its `Scenario` line carries the legacy origin tag. The added Given is the rwb-case contract answer, because the console that renders the stale product is RWB-P3-AD019-APP's and this story builds no screen; it changes no legacy value and adds no number. AC1 and AC2 of the same legacy story stay with RWB-P3-AD019-APP and RWB-ITG-AD019-ITG and are not copied here. The freshness stamp and the stale flag are RWB-P1-E1015-APP's, so this story does not own them either: what it owns is the stale product proved at the freshness answer it consumes and on the JOB-04 result it writes, which is what AC3's Given and Then name (ASM-0715). The run, its gate and its STALE answer on a business date with no complete batch are specified in BR7 and in the flow, and are tested by TC-AD-019-03 at component level.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The reconciliation runs once per business date, started by `AceDataReady`, and never for a business date whose ALS batch is not COMPLETE | Arch v5 slide 44 (JOB-04); FSD P1 v3 BR-P1-014-4; DP-10 |
| BR2 | The run reads ACE for the business date of the ACE batch that started it and never a mix of two business dates | FSD P1 v3 BR-P1-011-2 |
| BR3 | A result row is written per check and product group, with the source count, the workbench count, the two amounts, the variance, the variance percent, the tolerance in force and the result | `reconciliation_result` DF-OPS-118 to DF-OPS-129; TSD P1 v3 T3.6 |
| BR4 | The consumed event is deduped on its id in the inbox, so a redelivery starts no second run and writes no second row | DP-09; TSD P1 v3 T5.3; RWB-P1-E1011-CON section 12.4 |
| BR5 | A REC-05 orphan never deletes or changes a Workbench record or an ACE row; it is listed with its table, its column and its key for the data steward and, where the row is missing in ACE, for the ACE team | FSD P1 v3 BR-P1-011-3; legacy RWB-AD-019 guardrails |
| BR6 | The case list of a date is HELD when any REC-01 or REC-02 result of that date is BREAK, and MSG-P1-012 names the date, the product, the variance and the percent; otherwise it stays RELEASED | FSD P1 v3 A2.13; VR-P1-013-1 |
| BR7 | A data product past its expected business date is not served as current: the run carries DP01's last complete business date, status STALE and MSG-P1-001, and starts no comparison for the incomplete date | VR-P1-014-1; FSD P1 v3 A2.14.3; TSD P1 v3 T3.7 |
| BR8 | No value a business person may change is written in code: the tolerance, the entry threshold and the product and result lists are read with their version, and a missing parameter fails the run rather than defaulting | BR-P1-011; DP-06, DP-07 |
| BR9 | A break, an orphan and a stale product change nothing on the record they describe, and no read of this story acknowledges a break | Legacy RWB-AD-019 "No endpoint in this story"; FSD P1 v3 BR-P1-011-3 |
| BR10 | The variance and the variance percent are computed once, by the run, and are served exactly as written; no reader recomputes them | Legacy AC1; `reconciliation_result` DF-OPS-126, DF-OPS-127 |
| BR11 | Freshness is read from `v_ace_batch_status` only, by RWB-P1-E1015-APP; this story asks the typed freshness interface and writes no stamp and no `data_product_load` row | FSD P1 v3 BR-P1-014-2; TSD P1 v3 T3.7 |
| BR12 | The run record is the Temporal visibility record of the workflow and its activities; no job-run table and no run table is created in `rwb_source_data` | Arch v5 slide 44; TSD P1 v3 T4; ASM-0723 |
| BR13 | ACE data is read only through `recovery.v_ace_*` on the service login, and `recovery_case`, `case_party` and `case_account` are never read by table: the excluded accounts arrive through the rwb-case element of the baseline | DP-01, DP-05; ownership map (P3 owns the three tables) |
| BR14 | The shape of the reconciliation read and of the REC-05 break list is Not specified in the source documents (GAP-0519; ASM-0713) and follows the result and break-row schemas of RWB-P1-E1011-CON | GAP-0519; ASM-0713 |

### 9. State transitions

None in the case model: this story changes no case status, no stage and no task, and it writes no case row. The moves it owns are the state of a run and the state of the case list of a business date.

| From | Event | Condition | To |
|---|---|---|---|
| No run for the business date | `AceDataReady` processed and deduped | The ALS batch of the date is COMPLETE and `case_list_row` exists | Running |
| Running | `runRec01`, `runRec02`, `resolveRec05` and `writeReconciliationResult` complete | The rows are written in one transaction | Complete, with the case list RELEASED or HELD |
| Running | A view, the case list or a parameter read fails | No row of the date is written | Failed, with MSG-GEN-006 and the visibility record naming the step |
| Failed | A rerun for the same business date | The failing read answers | Running |
| Case list RELEASED for the date | A REC-01 or a REC-02 result of the date is BREAK | The tolerance is exceeded for a product group | HELD, with MSG-P1-012 |
| Case list HELD for the date | A rerun after the break is cleared | Every REC-01 and REC-02 result of the date is PASS | RELEASED |
| A data product LOADED | The product cut-off passes with no complete batch | The ACE batch record answers | STALE, with `stale_flagged_at` and MSG-P1-001 (owned by RWB-P1-E1015-APP) |

The freshness row above is shown for completeness and is RWB-P1-E1015-APP's; this story reads it and writes nothing in `data_product_load`. The run publishes no Kafka event: `AceDataLate` is E1015's and the reconciliation raises no fact of its own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Reads the results and the orphans of a business date on Platform administration R, and takes an orphan to the ACE team |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Hold Platform administration R and read the results and the orphans, read only |
| Every other role | Has no Platform administration right; refused with MSG-P4-002 |
| The rwb-source-data service identity (`rwb_source_data` login) | Reads the `recovery.v_ace_*` views, writes `reconciliation_result`, sets `case_list_row.publish_status` for the date, and writes no ACE row |
| The reconciliation workflow | Runs unattended on task queue `rwb-source-data` under a service identity; takes no decision on a case and approves nothing |
| rwb-access | Owns the roles, the scope and the access log; answers the authorise check and records the read |
| The ACE team | Owns the ACE rows behind a break and an orphan and fixes them at source; the run changes nothing there |
| No delegation of authority level applies | The reconciliation is a data check and posts no treatment, no write-off and no payment |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | `id`, `rec_code`, `business_date`, `product_group`, `source_count`, `workbench_count`, `source_amount`, `workbench_amount`, `variance_count`, `variance_pct`, `tolerance_pct`, `result` | Write, one row per check and product group per business date |
| DF-RPT-001 to DF-RPT-019 | `case_list_row` | `business_date`, `case_id`, `case_no`, `account_key`, `product_group`, `total_balance`, `days_past_due`, `publish_status` | Read for the workbench count and the balance sum; `publish_status` written for the date only |
| DF-OPS-001 to DF-OPS-009 | `data_product_load` | `product_code`, `source_system`, `business_date`, `loaded_at`, `status`, `stale_flagged_at`, `duplicate_count` | Read through `FreshnessQuery` of RWB-P1-E1015-APP; never written here |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` | `account_key`, `days_past_due`, `total_balance`, `data_as_of` | Read, one SELECT per check, on the `rwb_source_data` login |
| DF-ACE-055 to DF-ACE-074 | `v_ace_customer` | `person_key` and the identity fields the resolution needs | Read for REC-05 only |
| DF-ACE-099 to DF-ACE-107 | `v_ace_asset` | `asset_key` | Read for REC-05 only |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` | `payment_code`, `account_key` | Read for REC-05 only |
| DF-ACE-178 to DF-ACE-186 | `v_ace_batch_status` | `source_system`, `business_date`, `is_complete`, `started_at`, `completed_at` | Read for the gate only; the stamp is E1015's |
| DF-CAS-024 to DF-CAS-029 | `case_account` | `account_key` | Never read by table: through the rwb-case element of the baseline (owner P3) |
| DF-CAS-030 to DF-CAS-035 | `case_party` | `person_key` | Never read by table: through the rwb-case element of the baseline (owner P3) |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | `case_no`, `primary_person_key` | Never read by table: through the rwb-case element of the baseline (owner P3) |

Field IDs are those of the Logical Data Model and Data Dictionary v9 and of TSD P1 v3 T3.6. `reconciliation_result`, `case_list_row`, `data_product_load` and the five `recovery.v_ace_*` views are the whole of this story's data; `recovery_case`, `case_party` and `case_account` belong to rwb-case (P3) and are reached only through its published element, never by table (DP-01, DP-05). No field of this story is personal: a break row carries a business key, a table, a column and a reason code, and never a name, an address or an identity number. The break rows of REC-01 and the orphan rows of REC-05 are served for the business date from the run record of the workflow (ASM-0723); where a per-key row is persisted is Not specified in the source documents (GAP-0519; ASM-0713).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/source-data/v1`; owner rwb-source-data (P1). The operation is read only and its shape is published by RWB-P1-E1011-CON.

| Method | Path | Operation | Purpose | Access |
|---|---|---|---|---|
| GET | `/admin/reconciliation/results` | API-P1-003 | The REC-01 and REC-02 results and the REC-05 orphans of a business date, filtered by `recCode`, `product`, `result`, `from` and `to`, each row carrying its business date | Platform administration R, scope applied |

The operation replaces the legacy `/admin/data-quality/exceptions` of version 2, which listed load-check exceptions and reconciliation breaks; the load checks left with the load, so only the reconciliation result and its breaks remain (TSD P1 v3 T-A.1 note). The response fields, the paging and the break-row shape are Not specified in the source documents (GAP-0519; ASM-0713) and are the result and break-row schemas of RWB-P1-E1011-CON. The freshness read `GET /data-products/freshness` (API-P1-009) is named here as published by RWB-P1-E1015-APP and is not claimed by this story.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Timeout |
|---|---|---|---|---|
| None on the wire | The typed freshness interface `FreshnessQuery` (`stampFor`, `stampForRow`, `stampsFor`) | RWB-P1-E1015-APP, same service | The stamp of the products the run reads, for its gate and its stale answer, called in service as a Java interface and not as a REST hop | In process; no hop |

No other service is called by the code of this story. The excluded accounts, the tolerance, the entry threshold and the two lists arrive through the consumed elements that RWB-P1-E1011-CON section 12.2 fixes for the reconciliation resource, one hop and 2 s each; this story adds none of them and restates no path.

#### 12.3 Events published

None. `rwb.source-data.events.v1` carries `AceDataReady` and `AceDataLate`, and both belong to RWB-P1-E1015-APP: the reconciliation publishes no fact of its own, writes no outbox row and adds no schema to the topic.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | RWB-P1-E1015-APP | Starts `ReconciliationWorkflow` for the business date of the completed ACE batch, once per event id, after the case list build |

The payload is `eventId`, `occurredAt`, `schemaVersion`, `sourceSystem`, `businessDate`, `status` and `completedAt` under a CloudEvents 1.0 envelope, with no personal data (TSD P1 v3 T5.3; RWB-P1-E1011-CON section 12.4). The inbox dedupes on the event id, and the run is idempotent for a business date.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| `ReconciliationWorkflow` | Workflow, one run per business date, workflow ID `recon-{businessDate}`, search attributes `BusinessDate` and `RecSource` | `rwb-source-data` | The JOB-04 reconciliation of the business date, started by `AceDataReady` |
| `runRec01` | Activity | `rwb-source-data` | The count comparison of REC-01 per product group, with the exclusions taken away |
| `runRec02` | Activity | `rwb-source-data` | The balance comparison of REC-02 per product group |
| `resolveRec05` | Activity | `rwb-source-data` | The business-key resolution of REC-05, paged, with every orphan recorded by table, column and key |
| `writeReconciliationResult` | Activity | `rwb-source-data` | The result rows of the date and the publish state of the case list, in one transaction |

`ReconciliationWorkflow` is the workflow the contract baseline publishes as `ReconciliationWorkflow`, and its typed activity contract names the activity `reconciliation` (RWB-P1-E1011-CON section 12.5); the four activities above are the internal steps of that contracted activity on the same task queue. The run also calls `DailyCompletenessGate.check` of RWB-P1-E1015-APP before its first step. No workflow of this story is started by a Schedule (GAP-0520; ASM-0714).

#### 12.6 Schedules

None. The run is event-started, not a Schedule: JOB-04 starts from `AceDataReady`, and JOB-05 Timer check is retired in favour of durable timers inside the workflow (Arch v5 slide 44). The only Schedule that touches this legacy key is the freshness refresh behind the console, and it runs in rwb-case (RWB-P3-AD019-APP section 12.6), not here.

#### 12.7 Tables owned

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `reconciliation_result` | `rwb_source_data` | P1 | Written: one row per check and product group per business date |
| `case_list_row` | `rwb_source_data` | P1 | Read for the workbench count and the balance sum; `publish_status` written for the date; built by RWB-P1-E1002-APP |
| `data_product_load` | `rwb_source_data` | P1 | Read through `FreshnessQuery` only; written by RWB-P1-E1015-APP |
| `processed_event` | `rwb_source_data` | PLT library, created in this schema | Written by the inbox for the consumed event |

The ACE views `v_ace_account`, `v_ace_customer`, `v_ace_asset`, `v_ace_payment` and `v_ace_batch_status` are read in schema `recovery` on the `rwb_source_data` login and are never written. `recovery_case`, `case_party` and `case_account` belong to rwb-case (P3) and are read only through its published element, never by table (DP-01, DP-05). No run table is created: the run record is the Temporal visibility record (ASM-0723).

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| View fixtures (`v_ace_account`, `v_ace_customer`, `v_ace_asset`, `v_ace_payment`, `v_ace_batch_status`) | Synthetic rows of the five views in a container | The three checks, the gate and the stale answer, with no ACE data |
| rwb-case contract mock | The console read of SCR-45: a data product past its expected business date with its last complete ACE business date, and the three console blocks of RWB-P3-AD019-APP | AC3, whose Given is that answer |
| rwb-access authorise fake | The Platform administration R answer, allow and deny | TC-AD-019-04 |
| P1 contract fake of the reconciliation read | `GET /admin/reconciliation/results` with the result rows and the REC-05 orphans of a business date | The read shape, the empty date and the refused read |

The four fakes answer the shapes of RWB-P1-E1011-CON and are replaced by the real operation when it lands; a drift between a fake and the published document fails the contract test.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 0 consumed on the wire | The reconciliation result read provided; the freshness is an in-service Java interface, and the three baseline elements are RWB-P1-E1011-CON's |
| Kafka | 1 consumed | `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1` |
| Temporal | 1 workflow, 4 activities | `ReconciliationWorkflow` with `runRec01`, `runRec02`, `resolveRec05` and `writeReconciliationResult` on `rwb-source-data` |
| File | None | No file is read or written; the legacy lake extract is removed (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.reconciliation`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data`, namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies in its own-service form: this is the service that owns the views, so the three checks are its own SQL on its own login and add no hop. DP-10 applies as an event-started workflow, not a Schedule, because Architecture v5 slide 44 records JOB-04 that way and the console's Schedule is rwb-case's (GAP-0520; ASM-0714). DP-19 applies as a route this story does not build: SCR-45 is composed over rwb-case's reads, and this story only answers the reconciliation read that the route reaches through rwb-case.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReconciliationController | Controller | `GET /admin/reconciliation/results` with the right check, the scope and the query parameters |
| ReconciliationResultQueryService | Service | Reads the result rows and the break rows of a date range and returns them with their business date; recomputes nothing |
| ReconciliationResultRepository | Repository | The only SQL of the read: `reconciliation_result` by date range and filter; no other schema |
| ReconciliationWorkflow | Workflow | The JOB-04 run for a business date through the workflow kit; no run table |
| runRec01, runRec02 | Activity | The count and the balance comparison per product group, with the exclusions taken away |
| resolveRec05 | Activity | The paged business-key resolution and the orphan list by table, column and key |
| writeReconciliationResult | Activity | The result rows and the publish state of the case list in one transaction |
| AceDataReadyListener | Consumer | The inbox consumer of the event and the single start of the workflow per event id |
| ReconciliationBatchGate | Service | `DailyCompletenessGate.check` and the freshness stamp of the products the run reads, through the typed interface of RWB-P1-E1015-APP |
| CaseListSourceClient | Client | The excluded accounts, the tolerance and the two lists through the baseline elements of RWB-P1-E1011-CON, one hop, 2 s, with a breaker |

**Database and migrations**

- Reads `v_ace_account`, `v_ace_customer`, `v_ace_asset`, `v_ace_payment` and `v_ace_batch_status` in schema `recovery` on the `rwb_source_data` login, SELECT only, with no statement naming a `public` table (BR13).
- Writes `reconciliation_result` and `case_list_row.publish_status`, and the inbox row of the consumed event; writes no run table and no break table (BR12; GAP-0519).
- The tables and their indexes are created by RWB-P1-E1001-APP on the per-service Flyway sequence; this story adds no version of its own beyond an index on `reconciliation_result (business_date, product_group)` if the read plan needs it, and a version is never edited in place (DP-15).
- No foreign key leaves `rwb_source_data`: a business key is a `varchar(255)` column and REC-05 is the check that replaces the constraint the boundary rule forbids (BR-P1-001-3; TSD P1 v3 T1.1).

**Configuration and reference data**

- The tolerance `recon.tolerance.pct`, the entry threshold `case.entry.dpd`, `LOV-PRODUCT` and `LOV-REC-RESULT` are read with their version through the baseline elements of RWB-P1-E1011-CON; no value is written in code and a missing value fails the run (BR8).
- The workflow timeouts, the retry policy and the page size of the resolution are configuration of the workflow kit and the client, read from the platform configuration of the service template.
- The feature switch is `rwb.source-data.reconciliation-run` from the platform flag library: off, no run starts from the event and the read serves the last completed business date (RWB-P1-AD019-OPS).

**Build steps**

1. AceDataReadyListener with the inbox dedupe and the single start per event id; tests the redelivery of X3.
2. ReconciliationBatchGate over `DailyCompletenessGate` and `FreshnessQuery`, with the COMPLETE, the late and the unknown cases; tests the gate and the X4 and X9 paths.
3. `runRec01` and `runRec02` over the view fixtures, with the exclusions taken away and the product groups of the reference list; tests the count, the balance and the BREAK case of X5 and X6.
4. `resolveRec05` with the paging and the four keys, returning every orphan with its table, column and key; tests the orphan list and the unchanged-row rule of BR5.
5. `writeReconciliationResult` with the result rows and the publish state in one transaction, and the MSG-P1-012 raise on a hold; tests BR3 and BR6.
6. ReconciliationController and ReconciliationResultQueryService on the P1 contract fake, with the refused read and the malformed range; tests TC-AD-019-04 and X8.
7. The AC3 proof: the console answer of the rwb-case contract mock, the freshness answer of E1015, and the STALE marking and message on a business date with no complete batch; tests TC-AD-019-03.
8. The contract-fake run of the whole path, so the story builds before E1015, E1011-CON and the database story land.

**Done when.** The tests of section 16 pass, the run writes one result row per check and product group for a business date with zero variance on the clean fixture and BREAK with variance 12 and 0.41 percent on the SSME fixture, every orphan is listed with its table, column and key, the stale answer names DP01 and MSG-P1-001, the refused read answers MSG-P4-002, and `rwb_source_data` holds no run table and no break table.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A product group does not reconcile for the business date | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | The ALS batch of the business date is not complete, or a product is past its expected business date | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A query parameter is missing or malformed | Enter {field}. |
| MSG-P4-002 | The caller has no Platform administration R | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A downstream is unavailable: an ACE view, the case list step or the parameter read | {system} is not available. Your request is queued and will be retried. |

The texts are copied unchanged from legacy RWB-AD-019 and from the platform catalogue; no new wording is introduced. For MSG-P1-012, {date} is the business date, {product} the product group, {variance} the variance and {pct} the variance percent as written by the run. For MSG-P1-001, {product} is the product code ("DP01") and {date} its last complete business date. For MSG-P4-002, {action} is "read the reconciliation results". An unknown product group or data product is not an error: the read returns the rows that exist and never shows a missing row as a zero difference.

### 15. Screens and states

No screen in this story. SCR-45 Data quality is the gateway-bff composite route over the three console reads of rwb-case (DP-19, H RWB-PLT-N001-CON), and the route specification is Not specified in the source documents (RWB-P3-AD019-APP section 15). This story exposes four states to whatever reads it, and renders none of them.

| State | What this service answers |
|---|---|
| Current | The result rows of a business date whose ACE batch completed, each with the workbench count, the source count, the variance and the result; the freshness of DP01 LOADED through `FreshnessQuery` |
| Stale | No comparison for the business date; DP01 with its last complete business date, status STALE and MSG-P1-001 |
| Break | A result row with `result` BREAK, its variance and its variance percent, the break keys with their days past due, and the case list of the date HELD, with MSG-P1-012 |
| Not run | No result row for the business date, with the reason the run did not start or the step that failed, read from the workflow visibility record |

The screen keeps the legacy states Loading, breaks, referential completeness and stale (legacy RWB-AD-019 "Screen and states"); the first and the fourth of the four above are what this story adds to that list, because a reader of the operation needs to tell "no break" from "not run".

The empty, error and no access states of SCR-45 are Not specified in the source documents (CG-ALL-1874), because Screen Specifications v1 does not give them; the loading state is the legacy Loading state named above.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-019-03 | AC3; BR7, BR11, BR12 | Component | A data product past its expected business date with its last complete ACE business date, reached twice: once through the freshness answer of E1015 and the STALE marking on the run, once through the rwb-case contract mock of the console read |
| TC-AD-019-04 | The access refusal; BR13; AC7 | Component | A caller without Platform administration R asking `GET /admin/reconciliation/results`, refused with MSG-P4-002 before any read, with a second call with the right present for the contrast |
| TC-AD-019-05 | AC4; X2 | Component | No case_list_row for the business date: the run waits its retry window, ends FAILED with MSG-GEN-006 naming the case list step, and writes no row |
| TC-AD-019-06 | AC5; X3; BR4 | Component | AceDataReady delivered twice with the same event id: one workflow start and one reconciliation_result row |
| TC-AD-019-07 | AC6; X6; BR6; BR9 | Component | A REC-01 or REC-02 BREAK over the tolerance: the case list is HELD, MSG-P1-012 names the date, product, variance and percent, and no case is changed |
| TC-AD-019-08 | AC8; X8 | Component | A malformed from or to date: refused before any read with MSG-GEN-001 naming the field |
| TC-AD-019-09 | AC9; X10; BR8 | Component | The parameter read does not answer: the run ends FAILED, no result is written and no default tolerance is assumed |
| TC-AD-019-10 | AC10; X5; BR5 | Component | A Workbench business key with no view row: REC-05 BREAK, orphan listed with table, column and key, no Workbench or ACE row changed |
| TC-AD-019-11 | BR1; BR2 | Component | The run starts once per business date from AceDataReady, never when the ALS batch is not COMPLETE, and reads one business date only |
| TC-AD-019-12 | BR3; BR10; BR14 | Component | One reconciliation_result row per check and product group with the DF-OPS-118 to DF-OPS-129 fields; the variance and percent are served as the run wrote them |
| TC-AD-019-13 | AC11; BR1, BR2, BR3, BR4, BR5, BR6, BR8, BR9, BR10, BR14 | Component | A reconciliation run for one business date, each rule of section 8 listed in the Covers column checked against the run |
| TC-AD-019-14 | AC12 | Component | A call with no valid credential, a call by a caller without Platform administration R and a call answered not found (404 condition Not specified in the source documents (NEWAC-RWB-P1-AD019-APP-AC11)): answers 401, 403 and 404, with no row returned |
| TC-AD-019-15 | AC13; BR4 | Component | AceDataReady delivered again after its run has completed: no workflow start and no second reconciliation_result row |
| TC-AD-019-16 | AC14 | Component | An activity that fails or times out and is retried: the retry runs within the retry window, and an activity that does not complete ends the run FAILED with no row written |
| TC-AD-019-17 | AC15 | Component | An ACE view or the freshness interface the run consumes does not answer: the run ends FAILED, no row is written and MSG-GEN-006 is shown |
| TC-AD-019-18 | AC16 | Component | A publish status change the model does not allow: the change is refused and case_list_row keeps its status |
| TC-AD-019-19 | Section 12 operations, events and activities (contract test) | Contract | The operations, events and activities of section 12 checked against the contract baseline of RWB-P1-E1011-CON |
| TC-AD-019-20 | Section 12.7 tables (ASM-3438; boundary test) | Component | Each table of section 12.7 read and written at its boundary values |

TC-AD-019-01 and TC-AD-019-02 belong to the screen slice of this legacy key and appear on RWB-P3-AD019-APP, with their `-ITG` copies on RWB-ITG-AD019-ITG; they are not repeated here. The legacy test text of TC-AD-019-03 and TC-AD-019-04 is kept, its legacy level System maps to Component, and the Covers column names the criteria this story owns. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the tolerance, the entry threshold, the product groups and the result list are data with a version; the variance and the variance percent are computed once by the run and never by a constant or a reader.
- No personal data in logs, workflow inputs, events or prompts: the event carries a source system, a date, a status and a time, a break row carries a table, a column and a business key, and the fixtures are synthetic.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: the five views are read on the `rwb_source_data` login, and no statement names a `public` table (DP-05, ADR-010).
- No read of another service's table: `recovery_case`, `case_party` and `case_account` are P3's and arrive through the rwb-case element of the baseline; `case_list_row`, `data_product_load` and `reconciliation_result` are this service's own (DP-01).
- One login per service: `rwb_source_data`, SELECT on the views, write on its own tables only, no privilege outside its schema (DP-02).
- One hop and a 2 s budget on every cross-service call, with a breaker; the freshness is an in-service interface and adds no hop (DP-11, ADR-020).
- A break never deletes or changes a Workbench record or an ACE row, and the read acknowledges nothing (BR5, BR9).
- No run table and no break table: the run record is the Temporal visibility record and the rows are the result's own (BR12; ASM-0723).
- One consumed event, deduped on its id; a redelivery starts no second run (BR4, DP-09).
- Every read that shows ACE data shows the business date and the status of its product (TSD P1 v3 T3.7 "Display").

### 18. Traceability

| Requirement ID | Feature | L3 process |
|---|---|---|
| REQ-RDF-007 | FEAT-RDF-03 | All recovery processes |
| REQ-RDF-008 | FEAT-RDF-16 | All recovery processes |
| REQ-RDF-009 | FEAT-RDF-14 | All recovery processes |

Features are those of the Requirements Traceability Matrix v7. The process is that of legacy story RWB-AD-019 (Administration Stories v3), which names no feature of its own.

| Legacy RWB-AD-019 row | Value (verbatim) | Where it lands |
|---|---|---|
| Module | P1 Recovery data engine | Service rwb-source-data, service epic RWB-SVC-P1 |
| Story | As a data steward, I want the reconciliation breaks of REC-01 to REC-05, the referential completeness of every business key and the stale data products on one screen, so that I fix data problems before they reach a decision. | Section 1 and section 2: the breaks, the orphans and the stale product are computed and answered here; the one screen is RWB-P3-AD019-APP's |
| Acceptance criteria owned | AC3 | Section 7, with its origin tag and the rwb-case mock Given |
| Acceptance criteria elsewhere | AC1, AC2 | RWB-P3-AD019-APP (screen) and RWB-ITG-AD019-ITG (cross-service proof), not copied here |
| Data | `reconciliation_result` DF-OPS-118 to DF-OPS-129; `case_list_row` DF-RPT-001 to DF-RPT-019; `data_product_load` DF-OPS-001 to DF-OPS-008; `v_ace_account` DF-ACE-001 to DF-ACE-042 | Section 11 |
| Endpoints | No endpoint in this story. The console reads the reconciliation and data quality extract that the reconciliation step of JOB-04 writes, and the freshness stamp in `data_product_load`. The data quality exception endpoint is withdrawn by D-RCV-35 and there is no exception table. | Section 12.1: the read is added as API-P1-003, the replacement of `/admin/data-quality/exceptions`; the freshness stamp is E1015's |
| Screen and states | SCR-45 Data quality: Loading; breaks; referential completeness; stale | Section 15: the four states this service exposes, and no screen |
| Permission checks | Platform administration, R: RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10 and section 12.1 |
| Validation and messages | MSG-P1-012, MSG-P1-001, MSG-GEN-001, MSG-P4-002 | Section 14, texts unchanged |
| Test cases | TC-AD-019-01 to TC-AD-019-04 | Section 16: TC-AD-019-03 and TC-AD-019-04 here, the first two on the screen slice |
| Guardrails | No business value in code; no personal data in logs, tests or prompts; ACE data only through `recovery.v_ace_*`; a break never deletes or changes a record | Section 17. Personal data is handled as Data Classification and Personal Data Inventory v5 states: `account_key` (Indirect identifier, Confidential) travels in events and workflow inputs as a reference only, the clear key is read by REST under the masking policy, and logs carry the id of the read only; `days_past_due`, `total_balance` and `data_as_of` of `v_ace_account` (Customer data, Confidential) travel as a business fact only, never beside a direct identifier, and logs carry a code or an id only, never the customer value |

| Trace | Reference |
|---|---|
| Legacy key | RWB-AD-019, disposition Split (rework), business epic EP08, wave 4, release 30 June 2027 (tentative) |
| Build dependencies | RWB-PLT-E1071-CON (workflow kit, DP-10), RWB-PLT-N001-CON (gateway-bff route, DP-19), RWB-P1-E1015-APP (freshness and the event), RWB-P1-E1069-APP (the views and the login), RWB-P1-E1011-CON (the reconciliation contract baseline) |
| Contract dependencies | None |
| Integration dependencies | None |
| Pattern rows | DP-05, DP-10, DP-19 |
| Parameters and reference data | Parameters `recon.tolerance.pct` and `case.entry.dpd`: parameters contract of rwb-case (DP-06; RWB-PLT-E1042-CON, RWB-P3-E1042-CON). Lists `LOV-PRODUCT` and `LOV-REC-RESULT`: reference-data contract of rwb-case (DP-07; RWB-PLT-E1043-CON, RWB-P3-E1043-CON). All are read through the elements of the RWB-P1-E1011-CON baseline |
| Requirement rows | REQ-RDF-007, REQ-RDF-008, REQ-RDF-009; NFR-018; DL25 |
| Related slices of this legacy key | RWB-P3-AD019-APP (the screen), RWB-ITG-AD019-ITG (the cross-service proof), RWB-P1-AD019-OPS (the deployment) |
| Gaps and assumptions | GAP-0519, GAP-0520; ASM-0713 to ASM-0723; DL25 assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602 |

### 19. Out of scope

- SCR-45 Data quality, its three console reads, its annotation from `rwb_case` and its freshness Schedule: RWB-P3-AD019-APP.
- The cross-service end-to-end harness, its run report and its `-ITG` test copies: RWB-ITG-AD019-ITG.
- The deployment of this service with the reconciliation read and the JOB-04 worker, the route registration, the feature flag, the alerts, the dashboards, the runbook and the rollback: RWB-P1-AD019-OPS.
- The freshness stamp, the STALE flag at the cut-off, `AceDataReady` and `AceDataLate`, and `data_product_load`: RWB-P1-E1015-APP. This story reads the stamp and writes none.
- The tables, their indexes and the baseline migration: RWB-P1-E1001-APP. The views, the login and the grant: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- The case list build and its `publish_status` column: RWB-P1-E1002-APP. This story sets the status of the date and builds no case list row.
- The reconciliation contract baseline, the OpenAPI and AsyncAPI documents, the typed workflow contract, the break-row schema and the fakes: RWB-P1-E1011-CON.
- The data quality exception endpoint and its table, withdrawn by D-RCV-35: there is no exception table in the target and none is read.
- The lake extract, the Power BI data set and any scheduled data quality report: removed or not part of this story (DP-17).
- The interface and job monitor (legacy RWB-AD-018) and the `GET /admin/jobs` operations it reads: their own stories.
- The repair of a break or an orphan at source: the ACE team's and the data steward's work, outside every service.
