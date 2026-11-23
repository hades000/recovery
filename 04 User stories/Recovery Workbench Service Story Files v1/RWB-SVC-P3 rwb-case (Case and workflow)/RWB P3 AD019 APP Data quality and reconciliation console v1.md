# RWB-P3-AD019-APP Data quality and reconciliation console

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-AD019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP10, DP19 |
| Parallel lane | L-P3-A |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1071-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-019 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW)**, I want **the reconciliation breaks of REC-01 to REC-05, the referential completeness of every business key held on a case table and the stale data products on one read-only screen, each break and each key named with its product, its table, its column and its business date**, so that **I fix data problems before they reach a decision**.

The screen is SCR-45 Data quality, delivered as a gateway-bff composite route (DP-19, H RWB-PLT-N001-CON). gateway-bff calls three read operations of rwb-case, one hop each: `GET /data-quality/reconciliation-breaks`, `GET /data-quality/referential-completeness` and `GET /data-quality/stale-products`. rwb-case serves the break list annotated with the case number, the queue and the owner that hold each account key in its own schema `rwb_case`; it computes the orphan list from the business keys its own tables hold (`case_party.person_key`, `case_account.account_key`, `recovery_case.primary_person_key`) against the key-resolution read of the rwb-source-data contract; and it serves the stale list from the freshness of the data products read through that same contract. The reconciliation run itself (legacy JOB-04, now owned by rwb-source-data) and the freshness stamps stay with rwb-source-data; rwb-case owns no reconciliation table and reads no ACE view (DP-05). The stale list is refreshed by a Temporal Schedule in rwb-case through the workflow kit (DP-10, H RWB-PLT-E1071-CON), so no reader touches a Quartz job or batch table.

### 2. Business rationale

Under D-RCV-35 the Workbench loads no source data, so the data quality question changed shape: the reconciliation of the case list to ACE is the JOB-04 step of rwb-source-data, which compares the accounts at 90 days past due or more less the exclusions to the workbench count per product group, writes `reconciliation_result` and carries the freshness stamp in `data_product_load`, while REC-05 lists every business key with no source row. Today those results are seen only by the team that runs the job, and a stale product reaches a route decision before anyone notices it. This story gives the data steward one screen that names the break, the orphan and the stale product, with the business date behind each, and links each finding to the case it touches.

The legacy story sat in the P1 Recovery data engine module. Under D-RCV-60 the screen is delivered where the business keys it checks live, rwb-case, and the reconciliation run and the freshness it reads stay with rwb-source-data; the P1 slice of this legacy key (RWB-P1-AD019-APP) builds the run and the extract, and the ITG slice (RWB-ITG-AD019-ITG) proves the cross-service behaviour end to end. The placement, the login, the edge route and the read shape are recorded as GAP-0728 with assumptions ASM-1276 to ASM-1280.

The story meets the legacy control intent of REC-01 (accounts at 90 days past due against open cases, zero unexplained), REC-05 (every business key on a case table resolves to its source row) and the staleness control of every data product, as the screen a person uses; the computation itself is proved by the P1 slice.

### 3. Preconditions

- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-45 (DP-19). The exact route specification (path, merge rules, per-call timeout ownership) is Not specified in the source documents (GAP-0728; ASM-1277).
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, with the Schedule template (overlap policy SKIP, catch-up window) and the typed activity contract (DP-10).
- The rwb-case service contract, already published by the rwb-case contract stories, fixes the OpenAPI 3.1 base `/api/recovery/case/v1`, the problem response and the Idempotency-Key rule; this story publishes its three read operations under that base. The plan carries no separate contract story for RWB-AD-019, so the operations are added to the service contract (GAP-0728; ASM-1279).
- The rwb-source-data contract is published with its fake: `GET /api/recovery/source-data/v1/freshness` for the business date (Arch v5 slide 15), plus the reconciliation read behind REC-01 to REC-05 and the business-key resolution read used by REC-05. The path, the paging and the field shape of the reconciliation and key-resolution reads are Not specified in the source documents (GAP-0728; ASM-1278).
- RWB-P3-E1018-APP is done: cases exist in schema `rwb_case` with `case_party.person_key`, `case_account.account_key` and `recovery_case.primary_person_key` links by business key, with no foreign key across services.
- The JOB-04 reconciliation of rwb-source-data runs for the ACE business date and writes `reconciliation_result` (owner P1); this story reads its result and never runs it.
- The caller holds Platform administration R in rwb-access, with scope All, and the read is written to the access log by the rwb-access contract already carried by the service.
- The stale set is refreshed only when the rwb-source-data freshness operation answers; a product whose freshness is unknown is never shown as fresh.
- The login is the rwb-case login: Not specified in the source documents (GAP-0728; ASM-1276).

### 4. Flow

1. Data steward: opens SCR-45 Data quality from the administration menu; the gateway-bff composite route shows the Loading state.
2. gateway-bff: checks the session in Redis, takes the short-lived JWT through ACE Common sign-in and checks the coarse Platform administration permission.
3. gateway-bff: calls the three rwb-case read operations in parallel, one hop each, 2 s budget per call, no chained call.
4. rwb-case DataQualityController: checks Platform administration R and the scope through the cached authorise answer of rwb-access, and rejects a request whose business date parameter is missing or malformed.
5. rwb-case ReconciliationBreakQueryService: asks the rwb-source-data reconciliation read for the business date and receives the REC-01 to REC-05 rows with product group, source count, workbench count, variance, variance percent and the account keys on the break.
6. rwb-case ReconciliationBreakQueryService: for each account key and case number in the answer, looks up the case, the queue and the owner in schema `rwb_case` by `account_key` and adds them to the row; a key that no case holds is returned with the key alone.
7. rwb-case ReconciliationBreakQueryService: returns variance and variance percent exactly as the reconciliation read returns them; nothing is recomputed at the screen, because the run is JOB-04 in rwb-source-data.
8. rwb-case ReferentialCompletenessService: pages the distinct business keys held on its own tables (`case_party.person_key`, `case_account.account_key`, `recovery_case.primary_person_key`) and asks the rwb-source-data key-resolution read whether each resolves to a source row.
9. rwb-case ReferentialCompletenessService: returns every unresolved key with its table, its column and its key, and changes nothing: the case and its `case_party` row stay exactly as they are.
10. rwb-case StaleProductQueryService: returns the data products past their expected business date from the stale set, each with its last complete ACE business date, its status and MSG-P1-001.
11. rwb-case DataQualityFreshnessCheck (Temporal Schedule on queue `rwb-case`): every 15 minutes reads `GET /freshness` through the rwb-source-data contract once per data product and replaces the stale set in the api and worker pods; the run writes no table, holds no business record and is not a reconciliation run.
12. gateway-bff: merges the three answers into the screen model.
13. DataQualityPage: renders Break list, Referential completeness and Stale products, each row carrying its business date, and links a finding to the case record (SCR-03) where a case holds the key.
14. Data steward: takes a break to the ACE team and a stale product to rwb-source-data; the console records no acknowledgement and writes nothing.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The reconciliation read of the rwb-source-data contract does not answer inside the 2 s budget | Break list shows its error state from the problem response; the referential and stale blocks show | None | AC1 pattern |
| X2 | No reconciliation result exists for the requested business date | Break list shows its empty sentence and the last business date that has a result; no break is shown as zero | None | AC1 pattern |
| X3 | A business key on a case table has no source row | The orphan shows with its table, its column and its key; the case and its row are unchanged | None | AC2 |
| X4 | A data product is past its expected business date | The stale row shows with its last complete ACE business date | MSG-P1-001 | AC3 |
| X5 | The case list count does not reconcile to ACE for a product group | The REC-01 row shows as a break with its variance and variance percent | MSG-P1-012 | AC1 |
| X6 | A role without Platform administration R opens SCR-45 | The call is refused with 403; nothing shows | MSG-P4-002 | Access test TC-AD-019-04 |
| X7 | A break names an account key that no case holds | The row shows the key with empty case, queue and owner | None | AC1 |
| X8 | The freshness Schedule has not run since a restart | The stale block shows the business date of its last refresh and marks nothing as fresh | None | AC3 pattern |
| X9 | The business date parameter is missing or malformed | The call is refused before any read | MSG-GEN-001 | Validation |
| X10 | The business-key resolution read of rwb-source-data does not answer | Referential completeness shows its error state; a key is never reported as resolved without an answer | None | AC2 pattern |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads results other stories write; the reconciliation run, the freshness stamps and the source rows belong to rwb-source-data, and every cross-service answer is stubbed in that contract's fake |
| Negotiable | The column order of the three blocks, the refresh cadence and the link to the case record are design choices; the story fixes the behaviour and the legacy values |
| Valuable | One screen names every break, orphan and stale product with its business date, so a bad row is fixed before a route decision uses it |
| Estimable | Three read operations, three query services, one contract client, one Schedule and one activity, one page with three blocks |
| Small | Fits two weeks with its tests |
| Testable | Every owned criterion has a test case in section 16; every cross-service answer is stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Data quality and reconciliation console

  Scenario: AC1 A reconciliation break (legacy RWB-AD-019 AC1)
    Given v_ace_account holds 2,903 SSME accounts at 90 days past due or more less the exclusions and the case list holds 2,891
    Given the rwb-source-data contract mock returns the REC-01 result for SSME with source count 2,903, case list count 2,891, variance 12 and variance percent 0.41 for the business date
    When the reconciliation step of JOB-04 runs
    Then the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41
    And the 12 account keys are on the break list with their days past due from v_ace_account

  Scenario: AC2 Referential completeness (legacy RWB-AD-019 AC2)
    Given case_party on case "RW-2026-000140" carries person_key "P0099881" with no row in v_ace_customer
    Given the rwb-source-data contract mock returns no customer row for person_key "P0099881"
    When the REC-05 step runs
    Then the orphan shows with its table, its column and its key
    And the case and its case_party row are unchanged

  Scenario: AC3 A stale data product (legacy RWB-AD-019 AC3)
    Given a data product past its expected business date
    Given the rwb-source-data contract mock returns that data product with its last complete ACE business date and no complete batch for the business date
    When I open the console
    Then it shows as stale with its last complete ACE business date
```

The `Feature` line and every Given, When and Then of AC1, AC2 and AC3 are copied unchanged from legacy RWB-AD-019, and each `Scenario` line carries the legacy origin tag. In the target the ACE rows and the business date behind each finding arrive through the rwb-source-data contract, so `v_ace_account` and `v_ace_customer` are named as the system of record behind that contract and rwb-case reads neither directly (DP-05); the added Given is the contract answer the story is built against and changes no legacy value. The reconciliation run REC-01 to REC-05 and the freshness stamps are built by the P1 slice of this legacy key (RWB-P1-AD019-APP) and the cross-service proof is carried by the ITG slice (RWB-ITG-AD019-ITG); this story owns the three criteria as screen behaviour and as the referential check over the business keys of `rwb_case`.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A break, an orphan or a stale product never deletes or changes a Workbench record or an ACE row; the console is read only | Legacy RWB-AD-019 guardrails; AC2 |
| BR2 | The REC-01 to REC-05 rows are read as produced by the JOB-04 reconciliation of rwb-source-data; the variance and the variance percent are never recomputed at the screen | Arch v5 slide 44 (JOB-04 owner rwb-source-data); MSG-P1-012 |
| BR3 | A break row carries the product group, the business date, the source count, the workbench count, the variance and the variance percent, and the account keys on the break | `reconciliation_result` (DF-OPS-118 to DF-OPS-129) |
| BR4 | A business key held on a case table with no row in the source contract is listed with its table, its column and its key; the case and its row are unchanged | REC-05; FSD P3 v4 "Referential integrity is checked by the read model and by REC-05"; AC2 |
| BR5 | The referential check covers the keys rwb-case itself holds: `case_party.person_key`, `case_account.account_key` and `recovery_case.primary_person_key`; it reads no other service's table | DP-05; FSD P3 v4 (business keys with no foreign key) |
| BR6 | A data product is stale when the ACE batch for its expected business date is not complete; the console shows it with its last complete ACE business date and MSG-P1-001 | AC3; FSD P3 v4 VR-P3-001-1; MSG-P1-001 |
| BR7 | Freshness is read through the rwb-source-data freshness operation; rwb-case never reads `recovery.v_ace_batch_status` and never reads `data_product_load` by table | DP-05; ADR-010; Arch v5 slide 41 (P1 owns freshness) |
| BR8 | Only Platform administration R opens SCR-45; a role without the right is refused with MSG-P4-002 | Legacy RWB-AD-019 permission table |
| BR9 | The console has no write operation, no acknowledgement and no export in this story | Legacy RWB-AD-019 "No endpoint in this story"; D-RCV-60 read shape |
| BR10 | A break row shows the case number, the queue and the owner of a key from schema `rwb_case` only, and shows the key alone when no case holds it; the case list row itself belongs to rwb-source-data | DP-05; AC1; ownership ruling on `case_list_row` |
| BR11 | The stale set is refreshed by a Temporal Schedule in rwb-case through the workflow kit; no Quartz job table and no shared job table is read, because JOB-05 is retired and the Schedules belong to each service | Arch v5 slide 44 (JOB-05 retired); DP-10 |
| BR12 | A product whose freshness is unknown is never shown as fresh; an unrefreshed stale set shows the business date of its last refresh | BR6; AC3 pattern |
| BR13 | The read shape of the reconciliation and key-resolution operations is Not specified in the source documents (GAP-0728; ASM-1278) | D-RCV-60; DP-05 |

### 9. State transitions

None. This story changes no case status, no break status and no data product status. It reads the REC-01 to REC-05 results of the JOB-04 reconciliation, the business keys of the case tables and the freshness of the data products, and shows them. The reconciliation run and the freshness stamps are owned by rwb-source-data; the console publishes no event and consumes none.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW | Opens SCR-45 (Platform administration R, scope All) and reads the breaks, the orphans and the stale products |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Open SCR-45 with Platform administration R, read only |
| Every other role | Has no Platform administration right; refused with MSG-P4-002 |
| The rwb-case login | Reads schema `rwb_case` only, and calls the rwb-source-data contract for reconciliation, key resolution and freshness. The login name is Not specified in the source documents (GAP-0728; ASM-1276) |
| rwb-source-data | Owns the JOB-04 reconciliation, `reconciliation_result`, `data_product_load`, the ACE views and the freshness; answers every reconciliation, key-resolution and freshness read |
| rwb-access | Owns the roles, the scope and the access log; answers the authorise check and records the read |
| ACE team | Owns the ACE rows behind the breaks and the orphans, and fixes them at source; the console changes nothing |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | rec_code, business_date, product_group, source_count, workbench_count and the variance fields | Read through the rwb-source-data reconciliation read (owner P1) |
| DF-OPS-001 to DF-OPS-008 | data_product_load | product_code, source_system, business_date, loaded_at, status, stale_flagged_at | Read through the rwb-source-data freshness read (owner P1) |
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code | Read |
| DF-CAS-024 to DF-CAS-029 | case_account | account_key, is_primary, linked_from, linked_to | Read |
| DF-CAS-030 to DF-CAS-035 | case_party | person_key and party role | Read |
| DF-CAS-002 | recovery_case | case_no on a break row | Read |
| DF-WRK-002, DF-WRK-003 | queue | queue_code, queue_name on a break row | Read |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_key, days_past_due, data_as_of behind the break | Read through the rwb-source-data contract only |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer | person_key and the masked identity behind an orphan | Read through the rwb-source-data key-resolution read only |

Field IDs are those in the Logical Data Model and Data Dictionary v8. `reconciliation_result` and `data_product_load` belong to rwb-source-data (P1) and are read through its contract, never by table read (DP-05). This story writes no field and inserts no row; the only record written is the access record of rwb-access, on its own contract.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3). The three operations are read only and are published under the rwb-case service contract.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/data-quality/reconciliation-breaks` | The REC-01 to REC-05 rows of the business date, each with the account keys on the break and, for each key, the case number, queue and owner held in `rwb_case` | Platform administration R, scope All | Not applicable |
| GET | `/data-quality/referential-completeness` | The business keys held on `case_party`, `case_account` and `recovery_case` that the rwb-source-data key-resolution read does not resolve, with table, column and key | Platform administration R, scope All | Not applicable |
| GET | `/data-quality/stale-products` | The data products past their expected business date, each with its last complete ACE business date and status | Platform administration R, scope All | Not applicable |

Query parameter `businessDate` is an ISO business date and defaults to the date of the last reconciliation result. Errors: 401 no session, 403 no Platform administration R (MSG-P4-002), 400 missing or malformed parameter (MSG-GEN-001), 503 rwb-source-data down. The response schema, the error envelope and the status codes are fixed by the rwb-case service contract (GAP-0728; ASM-1279).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/freshness` | rwb-source-data (P1) | The business date and the batch state behind the stale block and behind the business date of each break row | One hop, 2 s timeout |
| GET | The reconciliation read of the rwb-source-data contract | rwb-source-data (P1) | The REC-01 to REC-05 rows of the business date. Path, paging and field shape: Not specified in the source documents (GAP-0728; ASM-1278) | One hop, 2 s timeout |
| GET | The business-key resolution read of the rwb-source-data contract | rwb-source-data (P1) | Whether a `person_key` or an `account_key` held on a case table resolves to a source row (REC-05). Path and batch shape: Not specified in the source documents (GAP-0728; ASM-1278) | One hop, 2 s timeout |

The right check and the access-record write go through the rwb-access authorise and access-log contract already carried by the rwb-case service (the shared guard library, declared by RWB-P3-E1018-APP); this story adds no contract dependency of its own (Contract dependencies: None).

#### 12.3 Events published

None. The console is a read and publishes no case event; the service topic `rwb.case.events.v1` is not used by this story.

#### 12.4 Events consumed

None. The stale set is refreshed by a Schedule, not by an event, and no inbox consumer is added.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| DataQualityFreshnessCheck | Workflow started by a Schedule | `rwb-case` | Reads the freshness of every data product through the rwb-source-data contract and replaces the stale set the console shows |
| refreshStaleSet | Activity | `rwb-case` | One read of the freshness operation per data product, with the 2 s budget and one GET retry; returns the stale rows; writes no table |

#### 12.6 Schedules

| Schedule | Cadence | Trigger | Legacy reference |
|---|---|---|---|
| DataQualityFreshnessCheck | Every 15 minutes during the business window | Temporal Schedule, overlap policy SKIP, catch-up window, workflow ID `data-quality-freshness-<env>` | The freshness read behind legacy JOB-04; the reconciliation run itself stays with rwb-source-data |

The default of 15 minutes is a design value and is Not specified in the source documents (GAP-0728; ASM-1280).

#### 12.7 Tables owned

None. This story writes no table and adds no migration. It reads `recovery_case`, `case_account`, `case_party` and `queue` in schema `rwb_case` with the rwb-case login; `reconciliation_result`, `data_product_load` and `case_list_row` belong to rwb-source-data (P1) and arrive only through its contract. Outbox, inbox and idempotency objects are untouched because no event is written.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The P1 contract | `GET /freshness` for the business date; the REC-01 result for SSME with the legacy counts; a `person_key` with no customer row; a data product past its expected business date |
| gateway-bff composite route stub | The SCR-45 route (RWB-PLT-N001-CON) | The parallel three-call merge and the per-block error state |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The three console reads provided; freshness, the reconciliation read and the key-resolution read consumed; one hop, 2 s timeout |
| Kafka | None | A read publishes and consumes nothing |
| Temporal | 1 workflow, 1 activity, 1 Schedule | DataQualityFreshnessCheck, refreshStaleSet, the 15-minute Schedule |
| File | None | No file is read or written; the console has no export in this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `dataquality`, Java package `th.co.scb.ace.workbench.recovery.case.dataquality`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DataQualityController | Controller | The three read operations with the right check, the scope and the business date parameter |
| ReconciliationBreakQueryService | Service | Reads the REC-01 to REC-05 rows through the contract, annotates each key with the case, queue and owner from `rwb_case`, and recomputes nothing |
| ReferentialCompletenessService | Service | Pages the distinct business keys of `case_party`, `case_account` and `recovery_case`, resolves them through the contract and returns the unresolved ones with table, column and key |
| StaleProductQueryService | Service | Serves the stale set with the last complete ACE business date and the message code |
| SourceDataClient | Client | The rwb-source-data freshness, reconciliation and key-resolution reads; 2 s timeout, one GET retry with jitter |
| DataQualityFreshnessCheck | Workflow | The Schedule-started refresh of the stale set through the workflow kit |
| refreshStaleSet | Activity | The contract reads of the refresh; no write, no event |
| DataQualityPage | Screen component | SCR-45 with the Loading, breaks, referential completeness and stale states |
| BreakListPanel, OrphanPanel, StaleProductPanel | Screen component | One block each, with the business date on every row and the link to SCR-03 |
| SectionMessage | Screen component | The empty and error state of one block, so one failing read never blanks the console |

**Database and migrations**

- No migration. No table is created, altered or written: the break rows, the freshness and the source rows are read through the rwb-source-data contract, and the annotation is a single indexed read on `case_account.account_key` and `recovery_case.case_no` in schema `rwb_case`.
- The existing index on `case_account (account_key)` from RWB-P3-E1018-CON serves the annotation; no new index is added for another schema.
- The stale set lives in the memory of the api and worker pods only: no Redis key, no business data outside `rwb_case` and no cache of a personal value.

**Configuration and reference data**

- The permission, the roles and the scope come from rwb-access; the reference-data and parameter contracts are not read by this story, so the console adds no parameter and no LOV.
- The refresh cadence and the per-call timeout (2 s) are configuration of the Schedule and the client, read from the platform configuration of the service template.

**Build steps**

1. DataQualityController with the three operations, the right check, the scope and the business date parameter; tests the refusal path and the validation.
2. SourceDataClient over the rwb-source-data fake for freshness, reconciliation and key resolution, with the 2 s budget and the retry; tests the contract answers.
3. ReconciliationBreakQueryService: the break row, the annotation by `account_key` and the key with no case; tests AC1 and the X7 path.
4. ReferentialCompletenessService: the paging, the resolution read and the orphan row with table, column and key; tests AC2 and the X3 and X10 paths.
5. StaleProductQueryService with the last complete ACE business date and MSG-P1-001; tests AC3 and the X4 and X8 paths.
6. DataQualityFreshnessCheck and refreshStaleSet against the workflow-kit test harness; tests the Schedule, the overlap policy and the restart behaviour.
7. DataQualityPage and the three panels over the gateway-bff route stub, with the per-block empty and error states; tests the X1 and X2 paths.
8. Access test through the rwb-access contract; test TC-AD-019-04.

**Feature switch.** The console sits behind the platform feature flag `rwb.p3.dataqualityconsole` served by the platform flag library (default ruling: feature flags belong to the platform library). Off: the route answers 404 and the menu entry is hidden, and the Schedule is paused.

**Done when.** The tests in section 16 pass, the three blocks show the legacy values of AC1 to AC3 on the SIT data set, the console writes no row, and the contract fakes of the rwb-source-data reads are green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A product group does not reconcile for the business date | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | A data product is past its expected business date | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | The business date parameter is missing or malformed | Enter {field}. |
| MSG-P4-002 | A role without Platform administration R opens the console | You cannot {action} here. Your role does not include it. |

Every error is returned as the service's problem response (TSD P3 v3 T2.1) carrying the MSG code and the trace ID; the response schema and the status codes 401, 400, 403 and 503 are fixed by the rwb-case service contract. An unknown product group or an unknown data product code is not an error: the console returns the rows that exist and never shows a missing row as a zero difference.

### 15. Screens and states

SCR-45 Data quality, served as the gateway-bff composite route of RWB-PLT-N001-CON (DP-19); the exact route specification is Not specified in the source documents (GAP-0728; ASM-1277). The legacy screen is kept: states Loading, breaks, referential completeness and stale, in one read-only page with three blocks.

- Break list: product group, business date, source count, workbench count, variance, variance percent, the account keys on the break with their days past due, and the case number, queue and owner where a case holds the key. Empty state when no result exists for the date.
- Referential completeness: table, column and key for every unresolved business key, with the link to the case that holds it.
- Stale products: product code, product name, last complete ACE business date, status and MSG-P1-001.

Each row shows its business date and links to SCR-03 Case record where a case holds the key. The console has no edit control, no acknowledgement and no export. One failing block shows its own message and the other two blocks show.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-019-01 | AC1, BR2, BR3 | End to end | `v_ace_account` with 2,903 SSME accounts at 90 days past due or more less the exclusions, the case list at 2,891, REC-01 variance 12 and 0.41 percent |
| TC-AD-019-02 | AC2, BR4, BR5 | End to end | `case_party` on case RW-2026-000140 with person_key P0099881 and no `v_ace_customer` row |
| TC-AD-019-03 | AC3, BR6, BR7 | End to end | A data product past its expected business date with its last complete ACE business date |
| TC-AD-019-04 | Access, BR8 | Component | A role without Platform administration R calls the console operations and is refused with MSG-P4-002 |

The legacy TC IDs, the legacy Covers and the legacy Test wording are kept unchanged. The legacy level System maps to End to end and Access maps to Component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the refresh cadence and the timeouts are configuration; the variance, the variance percent, the product groups and the expected business dates come from the reconciliation and freshness reads, never from a constant in the code.
- No personal data in logs, tests, workflow inputs or prompts. The console shows `person_key` and `account_key` and never a name, an address or an identity number; test data uses synthetic keys only.
- ACE data only through the owner's contract: account, customer and batch facts arrive through the rwb-source-data contract, and rwb-case reads no `recovery.v_ace_*` view and holds no foreign key into another schema (DP-05).
- No read of another service's tables: `reconciliation_result`, `data_product_load`, `case_list_row` and the ACE views belong to rwb-source-data (DP-05).
- A break never deletes or changes a Workbench record or an ACE row, and the console has no write operation.
- One hop, no call chain: gateway-bff asks rwb-case, and rwb-case asks rwb-source-data; each call has a 2 s budget and a breaker.
- The stale set holds no business record and no personal value; a product with unknown freshness is never shown as fresh.
- Every outbound read of personal data is recorded through the rwb-access access-log contract.

### 18. Traceability

| Source | Reference |
|---|---|
| Legacy story | RWB-AD-019 Data quality and reconciliation console, `04 User stories/Recovery Workbench Administration Stories v3.md` |
| Legacy acceptance criteria owned | AC1, AC2, AC3 |
| Legacy test cases | TC-AD-019-01 to TC-AD-019-04 |
| Reconciliation rules | REC-01 to REC-05 (JOB-04 reconciliation, `reconciliation_result`) |
| Freshness | `data_product_load` and `v_ace_batch_status`, read through rwb-source-data |
| Screen | SCR-45 Data quality (legacy states Loading, breaks, referential completeness, stale) |
| Related slices of this legacy key | RWB-P1-AD019-APP (the run and the extract), RWB-ITG-AD019-ITG (cross-service proof), RWB-P1-AD019-OPS (deployment) |

| Trace | Reference |
|---|---|
| Legacy key | RWB-AD-019, disposition Split (rework), business epic EP08, wave 4, release 30 June 2027 (tentative) |
| Build dependencies | RWB-PLT-E1071-CON (workflow kit, DP-10), RWB-PLT-N001-CON (gateway-bff composite route, DP-19) |
| Contract dependencies | None |
| Pattern rows | DP-05, DP-10, DP-19 |
| Test cases | TC-AD-019-01 (AC1), TC-AD-019-02 (AC2), TC-AD-019-03 (AC3), TC-AD-019-04 (Access) |
| Gaps and assumptions | GAP-0728; ASM-1276 to ASM-1280 |

### 19. Out of scope

- The JOB-04 reconciliation run, `reconciliation_result` and the reconciliation rules REC-01 to REC-05 (RWB-P1-AD019-APP).
- The data product loads, the freshness stamp in `data_product_load` and the ACE batch record (rwb-source-data).
- The data quality exception endpoint and its table, which D-RCV-35 withdrew; there is no exception table in the target.
- The interface and job monitor (legacy RWB-AD-018, its own realignment).
- The case list screen SCR-02 and the queue views (their own rwb-case stories).
- The cross-service end-to-end harness and its evidence (RWB-ITG-AD019-ITG).
- The deployment of the console: route provisioning, dashboards and the runbook (RWB-P1-AD019-OPS).
- The break-list export and the scheduled data quality report to management, whose format and recipients are not part of this story.
