# Technical Specification — RWB-E1-011 Reconciliation and data quality report

| Field | Value |
|---|---|
| Story | RWB-E1-011 — Reconciliation and data quality report |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-059-epic-1-RWB-E1-011` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-001; REQ-RDF-007, REQ-RDF-008); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 011 Reconciliation and data quality report v1.md`; FSD P1 A2.11, A2.12, A2.13; TSD P1 T3.1 (`reconciliation_result`) |
| Upstream IDs | BRD section: Business Requirements Epic 1, 3.1 and 3.8; Program 5.1; REQ-RDF-007, REQ-RDF-008; FEAT-RDF-11, FEAT-RDF-12, FEAT-RDF-13, FEAT-RPT-05, FEAT-RPT-09; US-RWB-E1-011; REC-01, REC-02; CTL-01; R-UNI-40; DL16, DL25 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no Workbench screen. The team manager reads the Power BI report "Reconciliation and data quality"; SCR-45 is Epic 2. |
| Logic In Scope | `YES` — REC-01 and REC-02 by product, variance and tolerance, break rows, publish hold and release, rerun replacement. |
| API In Scope | `NO` — no new or changed endpoint. The story uses existing `GET /api/recovery/v1/admin/data-quality/exceptions` (API-P1-003) and `GET /api/recovery/v1/admin/jobs` (API-P1-001). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `reconciliation_result` (new); `case_list_row.publish_status` (new); `dq_exception` (REC-01/REC-02); `loan_account` (read); JOB-04 reconciliation and publish steps. |
| New Nodes Required | `YES` — `ReconciliationStepConfig`, `ReconciliationService`, `ReconciliationResult`, `ReconciliationResultRepository`, `CaseListPublishGate`, `ReconciliationExtractWriter`. |
| Inherited Existing Behavior | Case list and `case_list_row` (RWB-E1-002); data quality rules and `dq_exception` (RWB-E1-006); INT-01 `LoadRunQuery` (RWB-E1-003); outbound adapter (RWB-E1-007); parameters (RWB-E1-042). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Accounts at 90 days past due in the ALS load are compared with open recovery cases, by count per product, every day. | SPEC-RWB-E1-011-003 | DIRECT | REC-01; `loan_account` count minus exclusions. | COVERED |
| BR2 | Balances in the ALS load are compared with balances on the case accounts, by sum per product. | SPEC-RWB-E1-011-004 | DIRECT | REC-02; `total_balance` on both sides. | COVERED |
| BR3 | A result is a break when the variance percent is above the tolerance. | SPEC-RWB-E1-011-005 | DIRECT | `recon.tolerance.pct`, 0.00 assumed (DL25). | COVERED |
| BR4 | A break holds the publish of the case list for the business date and lists the break rows. | SPEC-RWB-E1-011-006, 007 | DIRECT | `publish_status = HELD`; `dq_exception` rows. | COVERED |
| BR5 | Accounts excluded at entry are explained and do not count as breaks. | SPEC-RWB-E1-011-003 | DIRECT | `CaseQueryApi.excludedAccountsByProduct`. | COVERED |
| BR6 | No reconciliation runs until the INT-01 load is COMPLETED. | SPEC-RWB-E1-011-002 | DIRECT | `LoadRunQuery` gate. | COVERED |
| BR7 | Report grades: green, red, not run with reason. | SPEC-RWB-E1-011-010 | DIRECT | Extracts carry the result and reason. | COVERED |
| BR8 | A repeated run for the same date replaces that date's results. | SPEC-RWB-E1-011-008 | DIRECT | Replace by (`rec_code`, `business_date`, `product_group`). | COVERED |
| AC1 | Six PASS rows, variance 0; case list released; all three products green. | SPEC-RWB-E1-011-003, 004, 005, 007 | DIRECT | Two reconciliations per product. | COVERED |
| AC2 | SSME BREAK variance 12, 0.41 percent; 12 REC-01 exceptions; publish held; lake keeps 2026-11-27; MSG-P1-012; report red. | SPEC-RWB-E1-011-005, 006, 007, 010 | DIRECT | Break rows both directions. | COVERED |
| AC3 | Tolerance 0.10: MORTGAGE 0.10 PASS, SSME 0.11 BREAK. | SPEC-RWB-E1-011-005 | DIRECT | Boundary is inclusive PASS. | COVERED |
| AC4 | INT-01 LATE: no results; publish held; report "not run" with reason. | SPEC-RWB-E1-011-002, 007, 010 | DIRECT | Gate before results. | COVERED |
| AC5 | Rerun after a fix replaces six results, all PASS; 12 exceptions CLEARED; publish released. | SPEC-RWB-E1-011-006, 007, 008 | DIRECT | Replace and clear. | COVERED |
| AC6 | Two runs for the same date: one row per reconciliation, product and date. | SPEC-RWB-E1-011-009 | DIRECT | Unique key and idempotent replace. | COVERED |
| X1 | A product's variance is above tolerance. | SPEC-RWB-E1-011-005, 006, 007 | DIRECT | BREAK; hold; alert. | COVERED |
| X2 | Variance equals tolerance. | SPEC-RWB-E1-011-005 | DIRECT | PASS. | COVERED |
| X3 | INT-01 not COMPLETED. | SPEC-RWB-E1-011-002 | DIRECT | Not run; hold. | COVERED |
| X4 | Rerun after a fix. | SPEC-RWB-E1-011-008 | DIRECT | Replace; release if all PASS. | COVERED |
| X5 | Two runs for the same date. | SPEC-RWB-E1-011-009 | DIRECT | One row per key. | COVERED |
| X6 | A role without Platform administration R lists breaks. | SPEC-RWB-E1-011-012 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **team manager (RW-TEAMMGR)**, I want **a daily reconciliation of the case list to ALS, with the variance by product and the data quality results in one Power BI report**, so that **everyone sees whether today's case list can be trusted**.

The story completes the daily control that RWB-E1-002 starts. It compares the case list to ALS by count
and balance for each product, writes a result per reconciliation and product, lists every breaking
account, and holds the case-list publish when any product is outside tolerance. The report is Power BI;
the Workbench data quality screen is Epic 2.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | JOB-04 Daily reconciliation, reconciliation step after the case list step and before the publish step. |
| Preconditions | RWB-E1-002 case list built; RWB-E1-006 rule results written; INT-01 COMPLETED per `LoadRunQuery`; parameters `recon.tolerance.pct` 0.00 (assumed, DL25) and `case.entry.dpd` 90 (DL16); Power BI report built by RW-BIANAL. |
| Input | `loan_account`; `case_list_row`; `LoadRunQuery`; `CaseQueryApi.excludedAccountsByProduct(businessDate)`; parameters. |
| Output | `reconciliation_result`; `dq_exception` REC-01/REC-02; `case_list_row.publish_status`; extracts `reconciliation/<date>.csv` and `data-quality/<date>.csv`. |
| Feature flag | `rwb.p1.reconciliation`. Off: the case list publishes as in RWB-E1-002 with its count check. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `reconciliation_result` | `rec_code` | Step | System writes | `REC-01` or `REC-02` |
| `reconciliation_result` | `business_date` | Step | System writes | Part of the unique key |
| `reconciliation_result` | `product_group` | Step | System writes | MORTGAGE, HIRE_PURCHASE, SSME |
| `reconciliation_result` | `source_count`, `workbench_count` | ALS and case list | System writes | Counts at or above the threshold |
| `reconciliation_result` | `source_amount`, `workbench_amount` | ALS and case list | System writes | Balance sums |
| `reconciliation_result` | `variance_count`, `variance_pct` | Computed | System writes | Variance and percentage |
| `reconciliation_result` | `tolerance_pct` | Parameter | System writes | Snapshot of the value used |
| `reconciliation_result` | `result` | Computed | System writes | `PASS` or `BREAK` |
| `case_list_row` | `publish_status` | Gate | System writes | `PENDING`, `HELD`, `RELEASED` |
| `dq_exception` | `check_code`, `record_key` | Break list | System writes | `REC-01`/`REC-02` and the account number |

## Status-transition matrix

| Record | From | Event | To | Side effects |
|---|---|---|---|---|
| `reconciliation_result` | Does not exist | Step runs | PASS or BREAK | One row per reconciliation, product and date |
| `reconciliation_result` | Prior run for the date | Rerun | Replaced | Six rows replaced; exceptions cleared or refreshed |
| `case_list_row.publish_status` | `PENDING` | All results PASS | `RELEASED` | Publish step writes the case list extract |
| `case_list_row.publish_status` | `PENDING` | Any result BREAK | `HELD` | Publish step does not write; lake keeps the prior file |
| `case_list_row.publish_status` | `HELD` | Rerun all PASS | `RELEASED` | Publish released |
| `dq_exception` | `OPEN` | Rerun passes | `CLEARED` | `cleared_on` set |

No case status changes.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Variance above tolerance | BREAK; publish held; break rows listed; alert | MSG-P1-012 |
| X2 | Variance equals tolerance | PASS | None |
| X3 | INT-01 not COMPLETED | Not run; report shows not run; publish held | MSG-P1-001 |
| X4 | Rerun after a fix | Results replaced; release if all PASS | None |
| X5 | Two runs for the same date | One row per reconciliation, product and date | None |
| X6 | Role without Platform administration R | 403 | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/data-quality/exceptions` (API-P1-003); `GET /api/recovery/v1/admin/jobs` (API-P1-001); `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (API-P1-002). |
| Contract delta | None. The JOB-04 checks appear in the existing `checks` field; break rows appear as data quality exceptions. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R for reads; Platform administration U for rerun. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P1-011; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No Workbench screen, component, route, state or label change; the Power BI report is built by RW-BIANAL. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-007, REQ-RDF-008; SPEC-RWB-E1-011-001..014 | New batch step, service, entity, repository, publish gate and extract writer. | Variance 0, at tolerance, above tolerance; exclusions; break rows both directions; hold/release; rerun replace; concurrency; INT-01 gate; security. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ReconciliationStepConfig` | Spring Batch step in JOB-04 | Runs REC-01 and REC-02 per product, writes results and breaks, sets publish status. |
| `ReconciliationService` | Service | Computes counts, sums, variances and results against the tolerance. |
| `ReconciliationResult` | Entity | Maps `reconciliation_result`. |
| `ReconciliationResultRepository` | Repository | Replaces the results of one business date. |
| `CaseListPublishGate` | Service | Sets `HELD` or `RELEASED`; the publish step writes only when RELEASED. |
| `ReconciliationExtractWriter` | Service | Writes the reconciliation and data quality extracts. |
| `LoadAlertNotifier` | Service (RWB-E1-003) | Sends MSG-P1-012 and MSG-P1-001. |

Package `recovery.dataengine.recon`.

### Data and migration

Migration `V1_011__reconciliation_result.sql` creates `reconciliation_result` (`rec_code` varchar(6),
`business_date` date, `product_group` varchar(15), `source_count` integer, `workbench_count` integer,
`source_amount` numeric(18,2), `workbench_amount` numeric(18,2), `variance_count` integer,
`variance_pct` numeric(9,4), `tolerance_pct` numeric(9,4), `result` varchar(8) check in
('PASS','BREAK'), standard columns, unique (`rec_code`, `business_date`, `product_group`)); adds
`publish_status` varchar(10) default 'PENDING' check in ('PENDING','HELD','RELEASED') to
`case_list_row`.

### Reconciliation algorithm

1. Check INT-01 COMPLETED; if not, write NOT_RUN checks and hold the publish.
2. For each product group: count ALS accounts at or above `case.entry.dpd` less the P3 exclusions
   (REC-01); sum `total_balance` on both sides (REC-02).
3. Compute variance and variance percent; compare with `recon.tolerance.pct` per reconciliation.
4. Write one `reconciliation_result` per reconciliation and product.
5. List each breaking account in `dq_exception` with `REC-01` and the account number, in both
   directions: in ALS and not on the case list, or on the case list and not in ALS.
6. If every result is PASS, set the date's publish status to `RELEASED`; if any is BREAK, `HELD`.
7. Write the reconciliation and data quality extracts.

**Transaction.** The six results and the publish status of one business date are replaced in one
transaction; a failure leaves the prior results and status unchanged. No event is published by this
story.

### Tolerance boundary

A result is PASS when `variance_pct <= tolerance_pct`; BREAK when strictly greater. The tolerance is
snapshotted on the result row so a later parameter change does not rewrite history.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Runs the step; writes results, exceptions and publish status | All |
| RW-DATASTEW | Platform administration R; signs the daily reconciliation | All |
| RW-PLATADM | Platform administration R; rerun U | All |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Platform administration R | All |
| RW-TEAMMGR, RW-BIANAL | Reporting R; BI analyst Reporting CRUD | All |

### Observability and operations

- Job record: REC-01 and REC-02 per product (PASS, BREAK, NOT_RUN) and PUBLISH (RELEASED, HELD).
- Metrics: variance per product; break count; hold count; duration.
- Alerts: break above tolerance; INT-01 missing; publish held.
- Run book entry under RWB-E1-056.

### Performance

- Two aggregate queries per product group; set-based.
- Complete inside the JOB-04 window before the 07:30 Power BI refresh.
- The unique key makes a rerun idempotent.

### Feature flag and rollback

`rwb.p1.reconciliation`. Off: the case list publishes as in RWB-E1-002 with its count check. Rollback:
turn the flag off; the new table and column remain and are harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-011-01 | AC1, BR1, BR2, BR5, BR7 | System | MORTGAGE 12,256; HIRE_PURCHASE 12,960; SSME 2,903 with exclusions | Six PASS rows; release; all green |
| TC-E1-011-02 | AC2, BR3, BR4 | System | 12 SSME accounts missing | BREAK 12, 0.41 percent; 12 exceptions; held; MSG-P1-012 |
| TC-E1-011-03 | AC3, BR3 | System | Tolerance 0.10; variances 0.10 and 0.11 | PASS and BREAK |
| TC-E1-011-04 | AC4, BR6, BR7 | System | INT-01 LATE | No results; held; not run with reason |
| TC-E1-011-05 | AC5, BR8 | System | Break; missing cases created; rerun | Six PASS; 12 CLEARED; released |
| TC-E1-011-06 | AC6, BR8 | System | Two JOB-04 runs on two nodes | Six rows only |
| TC-E1-011-07 | X6 | Security | RW-CASEOWN lists exceptions | 403 MSG-P4-002 |
| TC-E1-011-08 | BR5 | Unit | Exclusions 0, 21, all accounts | Count to match adjusts; excluded not a break |
| TC-E1-011-09 | BR3 | Unit | Variance below, at and above tolerance | PASS, PASS, BREAK |
| TC-E1-011-10 | BR4 | Unit | One BREAK among six results | Publish HELD; prior lake file retained |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR3; SPEC-005 | What is the reconciliation tolerance? | Determines PASS/BREAK. | `recon.tolerance.pct` 0.00, assumed under DL25; loaded per reconciliation. | RESOLVED | SPEC-005 |
| CLAR-002 | BR3; SPEC-005 | Is the tolerance boundary inclusive? | Determines AC3. | Variance equal to tolerance is PASS; above is BREAK (story AC3). | RESOLVED | SPEC-005 |
| CLAR-003 | BR4; SPEC-007 | Does one break hold the whole case list? | Determines publish scope. | Yes; the publish for the business date is held (story BR4, AC2). | RESOLVED | SPEC-007 |
| CLAR-004 | BR5; SPEC-003 | How are exclusions applied? | Determines the count to match. | `CaseQueryApi.excludedAccountsByProduct`; excluded accounts are not breaks. | RESOLVED | SPEC-003 |
| CLAR-005 | BR8; SPEC-008 | Does a rerun clear prior break rows? | Determines exception state. | Yes; REC-01 exceptions that pass are CLEARED with the date (AC5). | RESOLVED | SPEC-008 |
| CLAR-006 | UI; SPEC-010 | Is the Power BI report built here? | Determines UI scope. | No; RW-BIANAL builds it. The story supplies both extracts and the grades. | RESOLVED | SPEC-010 |
| CLAR-007 | API; SPEC-011 | Are new endpoints needed? | Determines API impact. | No; existing job and exception endpoints are reused. | RESOLVED | SPEC-011 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the FSD/TSD or DL25. No
item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend/reporting story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New daily reconciliation, break list and publish gate; existing job and exception endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new batch reconciliation and publish gate with no contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 6 acceptance criteria, 6 exception paths and 6 record transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
