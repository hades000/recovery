# Technical Specification — RWB-E1-002 Case list v1 with case ID, owner and queue

| Field | Value |
|---|---|
| Story | RWB-E1-002 — Case list v1 with case ID, owner and queue |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-047-epic-1-RWB-E1-002` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-001; REQ-RDF-007); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 002 Case list v1 with case ID owner and queue v1.md`; FSD P1 A2.18; TSD P1 T3.1 (`case_list_row`), T5.1 |
| Upstream IDs | BRD section: Business Requirements Epic 1, 3.1; Program 5.1; REQ-RDF-007; FEAT-RDF-18; US-RWB-E1-002; CTL-01; REC-01; R-UNI-34, R-UNI-40; DL16, DL17, DL25 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — the story builds no Workbench screen. The team manager reads the Power BI report "Case list v1", built by the reporting and BI analyst on the lake extract. |
| Logic In Scope | `YES` — case list build, account join, count check, allocation wait, replace-by-date, exception row and publish hand-off. |
| API In Scope | `NO` — no new or changed endpoint. The story uses existing `GET /api/recovery/v1/admin/jobs` (API-P1-001) and `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (API-P1-002). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `JOB-04 Daily reconciliation` (case list step); `case_list_row` (new); `load_run` (extended checks); `dq_exception` (CL-01); `loan_account` (read); outbound file adapter INT-19. |
| New Nodes Required | `YES` — `CaseListStepConfig`, `CaseListChainListener`, `CaseListRow`, `CaseListRowRepository`, `CaseListCountCheck`, `CaseListExtractWriter`, `CaseListLastContactEnricher` (owned by RWB-E1-004 but invoked here). |
| Inherited Existing Behavior | Case record and `CaseQueryApi` (RWB-E1-018); morning allocation JOB-03 (RWB-E1-020); INT-01 load and `LoadRunQuery` (RWB-E1-003); outbound file adapter INT-19 (RWB-E1-007); parameters (RWB-E1-042). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The case list holds one row per open case and linked account for the business date. | SPEC-RWB-E1-002-003, 004 | DIRECT | `uk_case_list_row (business_date, case_id, account_id)`. | COVERED |
| BR2 | The ALS count to match is accounts at or above the entry threshold, less accounts excluded at entry. | SPEC-RWB-E1-002-005 | DIRECT | `loan_account` count minus `CaseQueryApi.excludedAccountCount`. | COVERED |
| BR3 | The count check passes when the difference is within the tolerance. | SPEC-RWB-E1-002-006 | DIRECT | `recon.caselist.tolerance.pct`, 0.00 assumed (DL25). | COVERED |
| BR4 | The list is built only when the INT-01 load for the business date is COMPLETED. | SPEC-RWB-E1-002-002 | DIRECT | `LoadRunQuery.completedLoad("INT-01", businessDate)`. | COVERED |
| BR5 | Every row carries the business date and the refresh time. | SPEC-RWB-E1-002-012 | DIRECT | `business_date` and `refreshed_at` on each row. | COVERED |
| BR6 | A repeated step for the same business date replaces that date's rows. | SPEC-RWB-E1-002-008 | DIRECT | Delete and insert in one transaction. | COVERED |
| BR7 | A file that fails after the retry limit goes to the exception queue with a task for the owner. | SPEC-RWB-E1-002-010 | DIRECT | `PUBLISHED = NO`; exception-queue task for RW-PLATADM. | COVERED |
| BR8 | Case data is read only through the P3 published interface. | SPEC-RWB-E1-002-003 | DIRECT | `CaseQueryApi`; no P3 table read. | COVERED |
| AC1 | 28,156 rows; count check 28,119 vs 28,119 PASS; 37 rows below the threshold recorded. | SPEC-RWB-E1-002-003, 005, 006 | DIRECT | Build, count, check results. | COVERED |
| AC2 | The extract holds case, account, product, stage, status, owner, queue, route, balance and days past due in order, plus team, business date and refresh time. | SPEC-RWB-E1-002-004 | DIRECT | Fixed column order; Power BI filters on team, queue, product. | COVERED |
| AC3 | Every row carries the refresh time; the report shows the refresh line. | SPEC-RWB-E1-002-012, 013 | DIRECT | `refreshed_at` set at step completion. | COVERED |
| AC4 | Count outside tolerance: list built and published; COUNT FAIL with difference 25, 0.09 percent; alert. | SPEC-RWB-E1-002-005, 006, 010 | DIRECT | FAIL does not hold the list in this story; RWB-E1-011 adds the hold. | COVERED |
| AC5 | INT-01 not COMPLETED: step does not run; no rows; previous lake file stays; REFUSED with "INT-01 not complete"; MSG-P1-001. | SPEC-RWB-E1-002-002, 011 | DIRECT | Gate before the load_run opens. | COVERED |
| AC6 | JOB-03 not complete at 07:15: list built with current owner/queue; `ALLOCATION_COMPLETE = NO`; report warning. | SPEC-RWB-E1-002-007 | DIRECT | Wait until `caselist.allocation.wait.until`. | COVERED |
| AC7 | Rerun for the same date keeps 28,156 rows; no duplicate case account; refresh time is the rerun time. | SPEC-RWB-E1-002-008 | DIRECT | Replace by business date. | COVERED |
| AC8 | `CaseQueryApi` error: no rows for the date; FAILED; prior date unchanged. | SPEC-RWB-E1-002-009 | DIRECT | One transaction; rollback. | COVERED |
| AC9 | Adapter fails all retries: COMPLETED with `PUBLISHED = NO`; exception queue task. | SPEC-RWB-E1-002-010 | DIRECT | Publish is a separate check. | COVERED |
| AC10 | Case account with no `loan_account` row: empty balance and days past due; one `CL-01` exception. | SPEC-RWB-E1-002-011 | DIRECT | Left join; exception row. | COVERED |
| X1 | Count differs above tolerance. | SPEC-RWB-E1-002-005, 006 | DIRECT | FAIL; alert; list published. | COVERED |
| X2 | INT-01 not COMPLETED. | SPEC-RWB-E1-002-002 | DIRECT | Step does not run. | COVERED |
| X3 | JOB-03 not complete by 07:15. | SPEC-RWB-E1-002-007 | DIRECT | Build with current values; NO check. | COVERED |
| X4 | Step runs again for the same date. | SPEC-RWB-E1-002-008 | DIRECT | Replace. | COVERED |
| X5 | `CaseQueryApi` raises an error. | SPEC-RWB-E1-002-009 | DIRECT | Rollback; FAILED. | COVERED |
| X6 | Lake transfer fails after retries. | SPEC-RWB-E1-002-010 | DIRECT | COMPLETED with `PUBLISHED = NO`. | COVERED |
| X7 | Case account has no `loan_account` row. | SPEC-RWB-E1-002-011 | DIRECT | Empty values; `CL-01`. | COVERED |
| X8 | Role without Platform administration R lists the runs. | SPEC-RWB-E1-002-014 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **team manager (RW-TEAMMGR)**, I want **one case list with case number, account, product, stage, status, owner, queue, route, total balance and days past due for every account at 90 days past due or more, refreshed each working day and available in Power BI**, so that **every recovery team works from one list**.

The story is a batch and reporting story. It builds the daily `case_list_row` table and the lake extract;
Power BI presentation belongs to the BI analyst. It does not build the Workbench case list screen
SCR-02 (RWB-E1-031) and does not hold the publish (RWB-E1-011). The count check here is the first
control; RWB-E1-011 replaces it with the product-level reconciliation.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Quartz `JOB-04 Daily reconciliation`, case list step, chained after JOB-03 completes for the business date, or at 07:15 if JOB-03 has not completed. |
| Preconditions | RWB-E1-018 open cases and `CaseQueryApi`; RWB-E1-020 JOB-03; RWB-E1-003 INT-01 COMPLETED; RWB-E1-007 outbound adapter; parameters `case.entry.dpd` 90 (DL16), `recon.caselist.tolerance.pct` 0.00 (assumed, DL25), `caselist.allocation.wait.until` 07:15. |
| Input | `CaseQueryApi.openCaseAccounts(businessDate)`, `CaseQueryApi.excludedAccountCount(businessDate)`, `loan_account`, `LoadRunQuery` (INT-01). |
| Output | `case_list_row`; `load_run` checks `COUNT`, `BELOW_ENTRY`, `ALLOCATION_COMPLETE`, `PUBLISHED`; extract `case-list/<businessDate>.csv`; `dq_exception` `CL-01`. |
| Feature flag | `rwb.p1.case-list`. Off: JOB-04 skips the case list step. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `case_list_row` | `business_date` | Step business date | System writes | Part of the unique key |
| `case_list_row` | `case_id`, `case_no` | `CaseQueryApi` | System writes | Must be an open case |
| `case_list_row` | `account_id`, `account_no` | `CaseQueryApi` / `loan_account` | System writes | Unique per business date, case and account |
| `case_list_row` | `product_group`, `stage_code`, `status` | `CaseQueryApi` | System writes | Values from their lists |
| `case_list_row` | `owner_user_id`, `queue_code`, `team_code`, `route_code` | `CaseQueryApi` | System writes | May be empty when allocation has not run |
| `case_list_row` | `total_balance`, `days_past_due` | `loan_account` | System writes | Empty when no account row; `CL-01` exception |
| `case_list_row` | `refreshed_at` | Step completion time | System writes | Required; rerun time on repeat |
| `case_list_row` | `last_contact_at`, `last_action_code` | RWB-E1-004 enricher | System writes | Optional |
| `load_run` | `check_results` | Step | System writes | JSON with the four checks |
| `dq_exception` | `check_code`, `record_key` | Step | System writes | `CL-01` and the account key |

## Status-transition matrix

| Record | From | Event | To | Side effects |
|---|---|---|---|---|
| `load_run` (JOB-04 case list) | — | Step starts | `RUNNING` | Row opened with job code and product DP03 |
| `load_run` | `RUNNING` | Step completes | `COMPLETED` | Counts and checks written; extract handed off |
| `load_run` | `RUNNING` | INT-01 not COMPLETED | `REFUSED` | Failed check "INT-01 not complete"; no rows |
| `load_run` | `RUNNING` | `CaseQueryApi` error | `FAILED` | Rollback; prior date unchanged |
| `case_list_row` | Prior date rows | Step for date D | Rows for D | Delete and insert in one transaction |
| `case_list_row` | Rows for D | Rerun for D | Replaced rows | Refresh time updated; no duplicates |

No case status changes.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Count outside tolerance | List built and published; `COUNT = FAIL`; alert | MSG-P1-012 |
| X2 | INT-01 not COMPLETED | Step does not run; previous lake file stays; `REFUSED` | MSG-P1-001 |
| X3 | JOB-03 not complete by 07:15 | Build with current owner/queue; `ALLOCATION_COMPLETE = NO` | Report warning |
| X4 | Repeat run for the date | Rows replaced; no duplicates | None |
| X5 | `CaseQueryApi` error | Rollback; `FAILED`; prior date unchanged | Alert to platform administrator |
| X6 | Lake transfer fails after retries | `COMPLETED` with `PUBLISHED = NO`; exception queue task | None (R-UNI-34) |
| X7 | Case account without `loan_account` | Empty balance and days past due; `CL-01` exception | None |
| X8 | Role without Platform administration R | 403; nothing listed | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/jobs` with `type=JOB-04`; `POST /api/recovery/v1/admin/jobs/{jobId}/rerun`. |
| Contract delta | None. The Job response carries the checks in its existing `checks` field. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R for the listing; Platform administration U for rerun. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P1-011 while a run for the date is RUNNING; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No Workbench screen, component, route, state or label change; the Power BI report is built by RW-BIANAL. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-007; SPEC-RWB-E1-002-001..016 | New batch step, chain listener, entity, repository, count check and extract writer. | Positive, negative, boundary and error-path tests: 28,156 rows; count at/above/below tolerance; INT-01 gate; allocation wait; replace; interface error; adapter failure; `CL-01`; column order. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `CaseListStepConfig` | Spring Batch step in JOB-04 | Reads open case accounts, joins accounts, writes rows, runs the count check. |
| `CaseListChainListener` | Quartz job listener | Starts the step when JOB-03 completes, or at the wait time. |
| `CaseListRow` | Entity | Maps `case_list_row`. |
| `CaseListRowRepository` | Repository | Deletes and inserts the rows of one business date. |
| `CaseListCountCheck` | Service | Computes the ALS count to match and compares within the tolerance. |
| `CaseListExtractWriter` | Service | Writes the CSV in fixed column order and hands it to the adapter. |
| `LoadAlertNotifier` | Service (RWB-E1-003) | Sends MSG-P1-012 and MSG-P1-001. |
| `RecoveryDataEngineController` | Controller (RWB-E1-003) | Lists and reruns the step. |

Package `recovery.dataengine.caselist`. Case, case account and queue data come only through
`CaseQueryApi`; `loan_account` is P1-owned.

### Data and migration

Migration `V1_002__case_list_row.sql` creates `case_list_row` with `case_no` varchar(18),
`account_no` varchar(20), `product_group` varchar(15), `stage_code` varchar(20), `status` varchar(20),
`queue_code` varchar(30), `team_code` varchar(20), `route_code` varchar(4), `total_balance`
numeric(18,2), `days_past_due` integer, `refreshed_at` timestamptz, the standard columns, unique
`uk_case_list_row (business_date, case_id, account_id)` and index `(business_date, team_code,
queue_code)`. RWB-E1-004 adds `last_contact_at` and `last_action_code`.

### Build algorithm

1. Check `LoadRunQuery.completedLoad("INT-01", businessDate)`. If false, write `REFUSED` and stop.
2. Open `load_run` with job code `JOB-04`, product `DP03`, status `RUNNING`.
3. Stream `CaseQueryApi.openCaseAccounts(businessDate)`.
4. Left join `loan_account` by `account_id`; write empty balance and days past due when absent and one
   `CL-01` exception per account.
5. Delete the date's rows and insert the new rows in one transaction.
6. Count rows at or above `case.entry.dpd`; compare with `loan_account` count at or above the threshold
   minus `CaseQueryApi.excludedAccountCount(businessDate)`.
7. Write checks `COUNT`, `BELOW_ENTRY`, `ALLOCATION_COMPLETE`, `PUBLISHED`.
8. Write the extract in the fixed column order and hand it to the outbound adapter.
9. On adapter failure after retries, keep `COMPLETED` with `PUBLISHED = NO` and open an exception-queue
   task for RW-PLATADM.

**Transaction.** The delete and insert of one business date run in one transaction; a failure leaves the
prior date's rows unchanged. No event is published by this story.

### Column order

Case number, account number, product, stage, status, owner, queue, route, total balance, days past due,
then team, business date, refresh time. The order is part of the report contract; a change is a
report change owned by RW-BIANAL.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Runs the step; writes rows, load_run and exceptions | All |
| SY-CASEWF | Serves `CaseQueryApi` | All |
| RW-PLATADM | Platform administration R; rerun U | All |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Platform administration R | All |
| RW-BIANAL | Reporting CRUD for the data set | All |
| RW-TEAMMGR, RW-CASEOWN, RW-PHONECOL | Reporting R in Power BI | Team / own |

### Observability and operations

- Job record: status, counts, checks, start and end.
- Metrics: rows written, rows below threshold, count variance, duration, publish failures.
- Alerts: count FAIL; INT-01 missing; adapter failure; step late.
- Run book entry under RWB-E1-056.

### Performance

- One pass over open case accounts; set-based join to `loan_account`.
- Target: complete inside the JOB-04 window before the 07:30 Power BI refresh.
- Replace-by-date keeps the table at one copy per business date.

### Feature flag and rollback

`rwb.p1.case-list`. Off: JOB-04 skips the step; the prior lake file remains. Rollback: turn the flag
off; the new table remains and is harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-002-01 | AC1, BR1, BR2, BR3 | System | 28,140 accounts; 21 exclusions; 37 below threshold | 28,156 rows; 28,119 vs 28,119 PASS; BELOW_ENTRY 37 |
| TC-E1-002-02 | AC2, BR1 | System | Built list; case RW-2026-000123 | Ten columns in order plus team, date, refresh; Power BI filters |
| TC-E1-002-03 | AC3, BR5 | System | JOB-03 at 06:52; step at 07:12 | Refresh time 2026-12-01 07:12 on every row; report line |
| TC-E1-002-04 | AC4, BR3 | System | 28,094 vs 28,119 | COUNT FAIL, 25 accounts, 0.09 percent; MSG-P1-012 |
| TC-E1-002-05 | AC5, BR4 | System | INT-01 refused | No rows; REFUSED; previous file; MSG-P1-001 |
| TC-E1-002-06 | AC6 | System | JOB-03 not complete at 07:15 | List built; `ALLOCATION_COMPLETE = NO`; report warning |
| TC-E1-002-07 | AC7, BR6 | System | Rerun of a built date | 28,156 rows; no duplicate; new refresh time |
| TC-E1-002-08 | AC8 | System | Interface error after 12,000 accounts | No rows; FAILED; 2026-11-27 unchanged |
| TC-E1-002-09 | AC9, BR7 | System | Adapter forced to fail | COMPLETED; `PUBLISHED = NO`; exception-queue task |
| TC-E1-002-10 | AC10 | System | Account ACC0000456 with no account row | Empty balance and days past due; `CL-01` |
| TC-E1-002-11 | X8 | Security | RW-CASEOWN lists JOB-04 | 403 MSG-P4-002 |
| TC-E1-002-12 | BR3 | Unit | Variance at, below and above the tolerance | PASS/PASS/FAIL boundaries |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR3; SPEC-006 | What is the case list tolerance? | Determines PASS/FAIL. | `recon.caselist.tolerance.pct` 0.00, assumed under DL25; load as a parameter. | RESOLVED | SPEC-006 |
| CLAR-002 | AC4; SPEC-010 | Does a count FAIL hold the publish in this story? | Determines publish behaviour. | No; this story builds and publishes. RWB-E1-011 adds the product-level hold. | RESOLVED | SPEC-010 |
| CLAR-003 | BR1; SPEC-003 | Is the row per case or per case account? | Determines uniqueness. | One row per open case and linked account; unique (business_date, case_id, account_id). | RESOLVED | SPEC-003 |
| CLAR-004 | AC6; SPEC-007 | What happens when allocation is late? | Determines wait and check. | Build with current owner/queue at 07:15; `ALLOCATION_COMPLETE = NO`; report warning. | RESOLVED | SPEC-007 |
| CLAR-005 | UI; SPEC-013 | Is the Power BI data set built here? | Determines UI scope. | No; RW-BIANAL builds it. The story supplies the extract and column order. | RESOLVED | SPEC-013 |
| CLAR-006 | BR2; SPEC-005 | How are P3 exclusions applied? | Determines the count to match. | `CaseQueryApi.excludedAccountCount`; subtract from the ALS count. | RESOLVED | SPEC-005 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story, the FSD/TSD or DL25. No
item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend/reporting story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New daily case-list batch step and lake extract; no Workbench screen or API contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new batch table and extract using existing job endpoints]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 10 acceptance criteria, 8 exception paths and 6 record transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
