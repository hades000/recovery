# Technical Specification — RWB-E1-009 CCMS and SVAF loads

| Field | Value |
|---|---|
| Story | RWB-E1-009 — CCMS and SVAF loads |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-067-epic-1-RWB-E1-009` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-001; REQ-RDF-004); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 009 CCMS and SVAF loads v1.md`; FSD P1 A2.5, A2.6; TSD P1 T3.1 (`collateral`, `account_collateral`), T5.1 (INT-10, INT-11) |
| Upstream IDs | BRD section: Business Requirements Epic 1, 3.1; Program 5.1; REQ-RDF-004; FEAT-RDF-05, FEAT-RDF-06; US-RWB-E1-009; DQ-057..DQ-070; R-UNI-40; CTL-02, CTL-27; DL11, DL25 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The data steward reads runs through the job endpoint; collateral and valuations appear on the case record view through RWB-E1-023. |
| Logic In Scope | `YES` — CCMS and SVAF checks, collateral upsert, link replacement, appraisal age, valuation write, sample check, repeat-call guard and freshness stamp. |
| API In Scope | `NO` — no new or changed endpoint. The story uses existing `GET /api/recovery/v1/admin/jobs` (API-P1-001) and `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (API-P1-002). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `collateral`, `account_collateral` (write); `valuation` (through `ValuationRecordApi`); `load_run` (`interface_run_id`); `dq_exception`; `data_product_load` (DP06); JOB-09. |
| New Nodes Required | `YES` — `CcmsCollateralLoader`, `SvafAppraisalLoader`, `AppraisalAgeCalculator`, `CollateralRepository`, `AccountCollateralRepository`, `ValuationRecordApi`, `ValuationRecordWriter`. |
| Inherited Existing Behavior | File adapter and `RecordLoader` (RWB-E1-007); load framework and mapping (RWB-E1-003); freshness stamp (RWB-E1-015); reference data (RWB-E1-043). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Collateral and appraisals arrive by weekly file through the adapters; no call to CCMS or SVAF. | SPEC-RWB-E1-009-001 | DIRECT | `RecordLoader` called by JOB-09; no outbound call. | COVERED |
| BR2 | The adapter runs business date, structure, control total and key checks; the loader runs reference, list and movement checks. | SPEC-RWB-E1-009-002, 004 | DIRECT | DQ-057–DQ-070 split by owner. | COVERED |
| BR3 | Records with unknown references or codes are held; above 0.50 percent the file is refused. | SPEC-RWB-E1-009-002, 004, 009 | DIRECT | `load.hold.tolerance.pct`. | COVERED |
| BR4 | An appraisal older than `appraisal.max.age` days at the business date is stale. | SPEC-RWB-E1-009-005 | DIRECT | 365 days assumed (DL11); strict greater-than. | COVERED |
| BR5 | The data product is stale when the week's file has not loaded. | SPEC-RWB-E1-009-007 | DIRECT | Freshness check of RWB-E1-015. | COVERED |
| BR6 | Buddhist Era years become Gregorian; amounts are THB with two decimals. | SPEC-RWB-E1-009-011 | DIRECT | Mapping rule "Dates" and "Amounts". | COVERED |
| BR7 | A file already loaded is not loaded again. | SPEC-RWB-E1-009-010 | DIRECT | `interface_run_id`; return the prior outcome. | COVERED |
| BR8 | Valuations are written only through the S1 published interface. | SPEC-RWB-E1-009-006 | DIRECT | `ValuationRecordApi`; no direct table write. | COVERED |
| AC1 | 31,200 collateral rows; 33,050 links; 2,140 appraisals; BE date converted; both runs COMPLETED; DP06 2026-11-27. | SPEC-RWB-E1-009-001, 003, 006, 007, 011 | DIRECT | Loaders and stamp. | COVERED |
| AC2 | Sample of 50 cases matches; `SAMPLE = 50 of 50`. | SPEC-RWB-E1-009-008 | DIRECT | Sample check on INT-11. | COVERED |
| AC3 | Appraisal 366 days stale true; 365 days stale false. | SPEC-RWB-E1-009-005 | DIRECT | Boundary. | COVERED |
| AC4 | CCMS file refused by adapter: no CCMS change; SVAF still called; unknown collateral held DQ-068. | SPEC-RWB-E1-009-001, 004 | DIRECT | Loaders are independent. | COVERED |
| AC5 | 120 of 33,050 unknown links (0.36 percent): 32,930 links; 120 DQ-061. | SPEC-RWB-E1-009-002 | DIRECT | Hold within tolerance. | COVERED |
| AC6 | 4 appraisals for unknown collateral: held DQ-068; 2,136 written. | SPEC-RWB-E1-009-004 | DIRECT | Hold. | COVERED |
| AC7 | 2 records with type K7: held DQ-062; 31,198 collateral rows. | SPEC-RWB-E1-009-002 | DIRECT | Code map hold. | COVERED |
| AC8 | 180 of 33,050 unknown links (0.54 percent): refused DQ-061; no change; LoadRefused; MSG-P1-002. | SPEC-RWB-E1-009-002, 009 | DIRECT | Above tolerance. | COVERED |
| AC9 | No SVAF file by 2026-12-01 04:00: no INT-11 run; valuation keeps 2026-11-20; DP06 STALE; MSG-P1-001. | SPEC-RWB-E1-009-007 | DIRECT | Freshness check. | COVERED |
| AC10 | `ValuationRecordApi` fails after 1,000: no appraisal stored; INT-11 FAILED; rerun stores 2,140. | SPEC-RWB-E1-009-006, 009 | DIRECT | Transaction rollback. | COVERED |
| AC11 | Loader called twice for one completed file: no change; prior outcome returned. | SPEC-RWB-E1-009-010 | DIRECT | Idempotent call. | COVERED |
| X1 | Appraisal older than the age limit. | SPEC-RWB-E1-009-005 | DIRECT | Stale flag and age. | COVERED |
| X2 | Adapter refuses the CCMS file. | SPEC-RWB-E1-009-001 | DIRECT | CCMS not called; SVAF still runs. | COVERED |
| X3 | Unknown account links at or below 0.50 percent. | SPEC-RWB-E1-009-002 | DIRECT | Held. | COVERED |
| X4 | Appraisal names an unknown collateral. | SPEC-RWB-E1-009-004 | DIRECT | Held DQ-068. | COVERED |
| X5 | Collateral type missing from the code map. | SPEC-RWB-E1-009-002 | DIRECT | Held DQ-062. | COVERED |
| X6 | Unknown references above 0.50 percent. | SPEC-RWB-E1-009-009 | DIRECT | Refused; LoadRefused; alert. | COVERED |
| X7 | No SVAF file for the week. | SPEC-RWB-E1-009-007 | DIRECT | No run; DP06 stale. | COVERED |
| X8 | `ValuationRecordApi` fails during the write. | SPEC-RWB-E1-009-006 | DIRECT | Rollback; FAILED; rerun. | COVERED |
| X9 | Loader called again for a COMPLETED file. | SPEC-RWB-E1-009-010 | DIRECT | Prior outcome; no write. | COVERED |
| X10 | Role without Platform administration U asks for a rerun. | SPEC-RWB-E1-009-013 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **data steward and data product owner (RW-DATASTEW)**, I want **collateral records from CCMS and appraisals from SVAF loaded from their weekly files and linked to the loan accounts**, so that **the collateral and asset data product DP06 is current without anyone looking the values up in CCMS or SVAF**.

The story adds two record loaders on the RWB-E1-007 adapter and the RWB-E1-003 framework. It owns the
collateral and link tables, computes appraisal age and writes valuations through the S1 interface. It
does not receive or check the files (RWB-E1-007), order a new appraisal (Epic 4) or load AMIS/RPS
(Epic 3).

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | JOB-09 File loads, weekly Monday 04:00 or when a file arrives; the adapter calls INT-10 before INT-11. |
| Preconditions | RWB-E1-007 adapter and `RecordLoader`; RWB-E1-003 load framework and DP01; RWB-E1-015 freshness; mapping versions and code maps for INT-10/INT-11 approved; parameters `appraisal.max.age` 365, `load.hold.tolerance.pct` 0.50, `load.movement.tolerance.pct` 10.00 (assumed, DL11, DL25); S1 accepts `ValuationRecordApi`. |
| Input | Checked CCMS records (collateral and account links) and SVAF appraisals, with interface run ID and business date. |
| Output | `collateral`, `account_collateral`, `valuation` (through S1), `load_run`, `dq_exception`, DP06 stamp, `LoadOutcome`. |
| Feature flag | `rwb.p1.collateral-load`. Off: the loaders return `SKIPPED` and write nothing. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `collateral` | `collateral_no` | CCMS | Upsert by number | Unique |
| `collateral` | `collateral_type`, `title_doc_no`, `plot_no`, `area_text`, `province`, `district`, `subdistrict` | CCMS + code map | System writes | Code map for type and province |
| `collateral` | `insured_value`, `insurance_expiry` | CCMS | System writes | THB two decimals |
| `collateral` | `occupancy`, `encumbrance_status` | Workbench | Never overwritten by the load | Owned by S5 |
| `account_collateral` | `account_id`, `collateral_id`, `lien_rank` | CCMS | Replaced per loaded collateral | Unique (`account_id`, `collateral_id`) |
| `valuation` | `appraisal_no` | SVAF | Upsert by number | Unique |
| `valuation` | `appraisal_date` | SVAF | System writes | BE converted to Gregorian |
| `valuation` | `appraised_value`, `forced_sale_value` | SVAF | System writes | THB two decimals |
| `valuation` | `stale_flag`, `age_days` | Computed | System writes | Age above `appraisal.max.age` |
| `load_run` | `interface_run_id` | Adapter | System writes | Unique; repeat call returns prior outcome |
| `load_run` | `check_results` | Loader | System writes | `SAMPLE`, held counts |

## Status-transition matrix

| Record | From | Event | To | Side effects |
|---|---|---|---|---|
| `load_run` (INT-10/11) | — | Loader starts | `RUNNING` | Row opened with interface run ID |
| `load_run` | `RUNNING` | Checks pass and write commits | `COMPLETED` | Counts, checks, stamp, LoadCompleted |
| `load_run` | `RUNNING` | Reference/list check above tolerance | `REFUSED` | No change; LoadRefused; alert |
| `load_run` | `RUNNING` | Valuation write fails | `FAILED` | Rollback; rerun available |
| `load_run` | `COMPLETED` | Loader called again for the same interface run | `COMPLETED` | No write; prior outcome returned |
| DP06 freshness | `LOADED` | Week's file missing | `STALE` | Handled by RWB-E1-015 |

No case status changes.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Appraisal older than the age limit | Loaded with `stale_flag = true` and age | None (row flag) |
| X2 | Adapter refuses the CCMS file | CCMS loader not called; SVAF still loads | Adapter alert (RWB-E1-007) |
| X3 | Unknown account links at or below 0.50 percent | Links held; rest loaded | Count on the run |
| X4 | Appraisal names an unknown collateral | Held DQ-068 | Count on the run |
| X5 | Collateral type missing from the code map | Held DQ-062 | Count on the run |
| X6 | Unknown references above 0.50 percent | Refused in full; LoadRefused; alert | MSG-P1-002 |
| X7 | No SVAF file for the week | No INT-11 run; valuation unchanged; DP06 stale | MSG-P1-001 |
| X8 | `ValuationRecordApi` fails | Rollback; FAILED; rerun | Alert to platform administrator |
| X9 | Loader called again for a COMPLETED file | No write; prior outcome | None |
| X10 | Role without Platform administration U asks for a rerun | 403 | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/jobs` with `type=INT-10` or `INT-11`; `POST /api/recovery/v1/admin/jobs/{jobId}/rerun`. |
| Contract delta | None. `Job.type` already carries the interface; checks are in the existing `checks` field. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R for the listing; Platform administration U for rerun. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P1-011; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; collateral appears through RWB-E1-023. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-004; SPEC-RWB-E1-009-001..015 | Two loaders, age calculator, repositories and the S1 interface and writer. | Checks pass/fail; hold boundary 0.50; age 365/366 and leap year; BE date; link replacement; valuation rollback; repeat call; sample; security. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `CcmsCollateralLoader` | Service (`RecordLoader`) | DQ-061–DQ-063; maps and writes collateral and links. |
| `SvafAppraisalLoader` | Service (`RecordLoader`) | DQ-068–DQ-070; maps, computes age and stale flag, calls `ValuationRecordApi`; sample check. |
| `AppraisalAgeCalculator` | Service | Age in days from appraisal date to business date; stale above the parameter. |
| `CollateralRepository`, `AccountCollateralRepository` | Repository | Upsert by `collateral_no`; replace links per loaded collateral. |
| `ValuationRecordApi`, `ValuationRecordWriter` | Published interface (S1) | Upsert appraisals in the caller's transaction. |
| `LoadCheckRunner`, `SourceMappingService`, `LoadEventPublisher` | Service (RWB-E1-003) | Checks, approved mapping, events. |

Packages `recovery.dataengine.load.ccms`, `recovery.dataengine.load.svaf`; S1 interface in
`recovery.valuation.api`, writer in `recovery.valuation`.

### Data and migration

Migration `V1_009__valuation_age.sql` adds `stale_flag` boolean not null default false and `age_days`
integer to `valuation`; adds `uk_collateral_no UNIQUE (collateral_no)`,
`uk_account_collateral UNIQUE (account_id, collateral_id)`, `uk_valuation_appraisal_no UNIQUE
(appraisal_no)`; adds `interface_run_id` uuid to `load_run` with a unique index.

### Load algorithms

**CCMS (INT-10).** Open `load_run`; run DQ-061 references and DQ-062 lists of values; above 0.50 percent
refuse. Upsert collateral by `collateral_no`; replace the `account_collateral` links of each loaded
collateral in one transaction; never overwrite `occupancy` or `encumbrance_status`; run DQ-063 movement;
call `recordLoad("DP06", ...)`; set COMPLETED; publish LoadCompleted.

**SVAF (INT-11).** Open `load_run`; run DQ-068 references and DQ-069 lists; hold appraisals for unknown
collateral. Compute `age_days` at the file business date and `stale_flag = age_days > appraisal.max.age`.
Write through `ValuationRecordApi.upsertAppraisals` in the same transaction as the status; run DQ-070
movement and the 50-case sample; stamp DP06; publish LoadCompleted.

**Transaction.** Each loader writes its own interface run in one transaction; the CCMS and SVAF loads are
independent, so a CCMS refusal does not roll back SVAF. Publishes `LoadCompleted` (EV-26) per interface
and `LoadRefused` (EV-27) on refusal.

### Repeat-call guard

If `interface_run_id` already has a COMPLETED run, return the prior `LoadOutcome` and write nothing. The
adapter may call the loader again after a restart; the guard makes the call idempotent.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Runs the loaders; writes collateral, links, load_run and exceptions; calls S1 | All |
| RW-PLATADM | Platform administration R; rerun U | All |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Platform administration R | All |

### Observability and operations

- Job record: rows read, loaded, held; checks; interface run ID; duration.
- Metrics: rows loaded; held; stale appraisals; sample match; duration.
- Alerts: refusal; valuation write failure; DP06 stale.
- Run book entry under RWB-E1-056.

### Performance

- Set-based upsert per file; link replacement per loaded collateral.
- Weekly volume: 31,200 collateral, 33,050 links, 2,140 appraisals.
- The sample check reads 50 cases, not the full set.

### Feature flag and rollback

`rwb.p1.collateral-load`. Off: the loaders return `SKIPPED`. Rollback: turn the flag off; the added
columns and keys remain and are harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-009-01 | AC1, BR1, BR6 | System | 31,200 CCMS records; 33,050 links; 2,140 appraisals | Counts; BE date converted; COMPLETED; DP06 2026-11-27 |
| TC-E1-009-02 | AC2 | System | 50 random cases with collateral | `SAMPLE = 50 of 50` |
| TC-E1-009-03 | AC3, BR4 | System | Appraisals 2025-11-26 and 2025-11-27 | 366 stale true; 365 stale false |
| TC-E1-009-04 | AC4, BR2 | System | Adapter stub refusing CCMS | CCMS not called; SVAF still called; DQ-068 held |
| TC-E1-009-05 | AC5, BR3 | System | 120 of 33,050 unknown links (0.36 percent) | 32,930 links; 120 DQ-061 |
| TC-E1-009-06 | AC6, BR3 | System | 4 unknown collateral numbers | 4 DQ-068; 2,136 appraisals |
| TC-E1-009-07 | AC7, BR3 | System | 2 records with type K7 | 2 DQ-062; 31,198 collateral |
| TC-E1-009-08 | AC8, BR3 | System | 180 of 33,050 unknown links (0.54 percent) | Refused DQ-061; LoadRefused; MSG-P1-002 |
| TC-E1-009-09 | AC9, BR5 | System | No SVAF by 2026-12-01 04:00 | No INT-11 run; valuation 2026-11-20; DP06 STALE |
| TC-E1-009-10 | AC10, BR8 | System | Valuation API fails after 1,000 | No appraisal; FAILED; rerun stores 2,140 |
| TC-E1-009-11 | AC11, BR7 | System | Second call for IR-0000451 | No change; prior outcome |
| TC-E1-009-12 | X10 | Security | RW-DATASTEW reruns | 403 MSG-P4-002 |
| TC-E1-009-13 | BR3 | Unit | Hold ratio 0.49, 0.50, 0.51 percent | Hold, hold, refuse |
| TC-E1-009-14 | BR4 | Unit | Age 364, 365, 366 and leap year | Stale only above 365 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4; SPEC-005 | What is the appraisal age limit? | Determines the stale flag. | `appraisal.max.age` 365, assumed under DL11 and CTL-27; data, not code. | RESOLVED | SPEC-005 |
| CLAR-002 | BR3; SPEC-002, 004, 009 | What is the hold tolerance? | Determines hold vs refuse. | `load.hold.tolerance.pct` 0.50, assumed under DL25. | RESOLVED | SPEC-002, 004, 009 |
| CLAR-003 | BR4; SPEC-005 | Is the age boundary inclusive? | Determines AC3. | 365 days is not stale; 366 is stale (story AC3). | RESOLVED | SPEC-005 |
| CLAR-004 | BR1; SPEC-001 | Who calls the loaders? | Determines integration. | The P2 adapter calls INT-10 before INT-11 (story §4). | RESOLVED | SPEC-001 |
| CLAR-005 | BR7; SPEC-010 | What happens on a repeat call for one file? | Determines idempotency. | No write; return the prior outcome (story AC11). | RESOLVED | SPEC-010 |
| CLAR-006 | BR8; SPEC-006 | May P1 write `valuation` directly? | Determines the interface. | No; only through `ValuationRecordApi` (ADR-002, DT08). | RESOLVED | SPEC-006 |
| CLAR-007 | BR6; SPEC-011 | How are Thai dates and amounts handled? | Determines conversion. | Buddhist Era year to Gregorian; THB two decimals (mapping rules). | RESOLVED | SPEC-011 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the FSD/TSD or DL11/DL25. No
item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New CCMS and SVAF record loaders, appraisal age flag and DP06 stamp; existing job endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new file loaders with no contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 11 acceptance criteria, 10 exception paths, 5 run transitions and 1 freshness transition are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
