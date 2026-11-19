# Technical Specification — RWB-E1-013 Baseline measures

| Field | Value |
|---|---|
| Story | RWB-E1-013 — Baseline measures |
| Epic / module | E1 / P9 Reporting |
| RUN_ID | `INC-042-epic-1-RWB-E1-013` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-RDF-012); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 013 Baseline measures v1.md` |
| Upstream IDs | REQ-RDF-012; NFR-065; FEAT-RDF-19, FEAT-RPT-01; US-RWB-E1-013; CTL-02; DL10, DL11; INT-19 |
| Status | `SUCCESS` — CLAR-002 and CLAR-003 resolved (story AC7 corrected; measures approved as D-RCV-32) |
| Prepared | 2026-11-04 |
| Regated | 2026-11-06 — Technical Specifier re-run after the AC7 correction and the measure decision D-RCV-32 |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. JOB-15 runs are read through `GET /admin/jobs`; SCR-44 and SCR-37 are Epic 2 and the Power BI report is external. Story §15. |
| Logic In Scope | `YES` — definition load and validation, effective dating, six calculators, snapshot idempotency, baseline freeze, load-status gate, extract hold/resend. |
| API In Scope | `NO` — no new or changed contract. Reuses `POST /admin/reference-loads` (P4), `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` (P1). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | P4 reference-load service and handler registry; P1 job monitor and rerun; P3 `CaseReportingApi`; P1 `RecoveryDataApi`; INT-19 outbound adapter; `sys_fields`; RWB-E1-043 reference data; RWB-E1-056 run book. |
| New Nodes Required | `YES` — `ReportingExtractJob`, `MeasureDefinitionLoadHandler`, `MeasureCatalogService`, six calculators, two entities, two repositories, `DataLakeWriter`, `LoadStatusGuard`, `BaselineService`, `measure_definition`, `measure_snapshot`, `V1_013__measures.sql`. |
| Inherited Existing Behavior | Case record (RWB-E1-018); reference loads (RWB-E1-029); versioned reference data (RWB-E1-043); outbound adapter (RWB-E1-007); freshness stamp (RWB-E1-015); job monitor and run book (RWB-E1-056). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

Out of scope: steering dashboard, SCR-37 and `GET /reports/measures` (RWB-E2-009); queue and ageing measures (RWB-E1-030); benefit realisation (Epic 6); decision log copy (RWB-E1-014); Power BI layout (RW-BIANAL).

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A measure is published only under a definition in force that names its data product, formula, unit and approver. | SPEC-RWB-E1-013-003, -004, -018 | DIRECT | `MeasureCatalog.inForce(businessDate)`; the loader checks the fields; no formula is executed. | COVERED |
| BR2 | The baseline is the snapshot of the configured baseline business date and is frozen once written. | SPEC-RWB-E1-013-013, -014, -015, -020 | DIRECT | `rwb.reporting.baseline-date`; `is_baseline`/`frozen`; service skip and DB trigger. | COVERED |
| BR3 | Measures are computed from Workbench records read through the owning modules, never from a separate count. | SPEC-RWB-E1-013-005, -006 | DIRECT | P3 `caseFacts` and P1 `paymentsSinceEntry`; no table read. | COVERED |
| BR4 | A measure is computed only from loads that passed their checks; stale data is not published as the baseline. | SPEC-RWB-E1-013-002 | DIRECT | `loadStatus` per data product named by the definitions; no rows for a stale date. | COVERED |
| BR5 | The extract holds the publish and alerts on failure, and runs again in the next window. | SPEC-RWB-E1-013-016, -017 | DIRECT | Staging hold; MSG-GEN-006; next JOB-15 drains the hold. | COVERED |
| BR6 | Age bands are a reference list. | SPEC-RWB-E1-013-008 | DIRECT | Band edges loaded as reference data; no day numbers in code. | COVERED |
| BR7 | A definition load with any invalid row is refused in full. | SPEC-RWB-E1-013-003 | DIRECT | One transaction; any invalid row rolls back the file; no version in force. | COVERED |
| AC1 | Six definitions load with valid from 2026-11-21; MD-2026.11 is in force; `MeasureCatalog` returns data product and formula. | SPEC-RWB-E1-013-003, -004 | DIRECT | Load fixture; effective dating; catalog read. | COVERED |
| AC2 | Baseline rows for 2026-11-27 are baseline and frozen; CASES_BY_ROUTE totals 120 (60 Mortgage); REALIZED_RECOVERY is 4,350,000.00 THB. | SPEC-RWB-E1-013-007, -010, -013, -014 | DIRECT | 120-case synthetic set; known payment total; baseline date. | COVERED |
| AC3 | The 2026-12-01 extract has freshness stamp and trailer count; baseline rows unchanged; job record has count and times. | SPEC-RWB-E1-013-016, -019 | DIRECT | File plus trailer; baseline rows read from the frozen snapshot. | COVERED |
| AC4 | A TIME_IN_STAGE row with no formula refuses the whole load with MSG-GEN-001 naming "formula"; no version in force. | SPEC-RWB-E1-013-003 | DIRECT | First invalid field; 422; rollback. | COVERED |
| AC5 | A second publication of 2026-11-27 leaves frozen rows unchanged and records MSG-P9-001. | SPEC-RWB-E1-013-014, -015, -020 | DIRECT | Service skip; trigger; job check. | COVERED |
| AC6 | A refused 2026-11-27 COLLINS load writes no baseline rows; MSG-P1-001 names "DP03 Case" and 2026-11-26; the baseline publishes after the next good load. | SPEC-RWB-E1-013-002 | DIRECT | `loadStatus`; baseline catch-up; last good date. | COVERED |
| AC7 | A data lake outage writes the run's snapshot rows, holds the extract, alerts with MSG-GEN-006 naming "Data lake", and sends on the next run. The fixture runs JOB-15 at 01:30 on 2026-12-01 for business date 2026-11-30 (corrected story, 2026-11-06). | SPEC-RWB-E1-013-016, -017 | DIRECT | Snapshot commit before extract; hold and resend; the run processes the previous business date, skipping Saturday and Sunday. | COVERED |
| AC8 | A configured measure with no definition writes no value and records MSG-P9-003 naming the measure. | SPEC-RWB-E1-013-018 | DIRECT | `rwb.reporting.measures` checked against `MeasureCatalog`. | COVERED |
| X1 | A definition row has no formula or no data product. | SPEC-RWB-E1-013-003 | DIRECT | Load refused whole; MSG-GEN-001. | COVERED |
| X2 | The baseline is published a second time. | SPEC-RWB-E1-013-015, -020 | DIRECT | Frozen unchanged; MSG-P9-001. | COVERED |
| X3 | The loads of the baseline date failed. | SPEC-RWB-E1-013-002 | DIRECT | No baseline rows; MSG-P1-001; catch-up. | COVERED |
| X4 | The data lake is unavailable. | SPEC-RWB-E1-013-017 | DIRECT | Hold; alert; resend. | COVERED |
| X5 | A measure in the extract has no definition in force. | SPEC-RWB-E1-013-018 | DIRECT | No value; MSG-P9-003. | COVERED |
| AC-EXC-P9-001-05 | A role without the right is refused with MSG-P4-002 and nothing changes. | SPEC-RWB-E1-013-021 | DIRECT | Reference data C for the load; Platform administration U for the rerun; 403. | COVERED |

## User story intent interpretation

As the **Tribe lead (RW-TRIBE)**, I want **cases by route, age and queue, realized recovery, time in stage and turnaround per route published as the baseline, with definitions agreed by the Tribe**, so that **every later epic is measured against the same baseline**. This is a backend batch and reporting story. It adds no screen. The Tribe lead reads the baseline in the Power BI report built by the Reporting and BI analyst from the INT-19 extract; the platform administrator reads the JOB-15 run through the existing job endpoint. SCR-44 and SCR-37 are Epic 2. The definition file is the control: the Tribe lead approves each row, the reference data administrator loads it, and no formula is written in code.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Quartz `JOB-15 Reporting extract`, nightly 01:30 Asia/Bangkok (`0 30 1 * * ?`), for the previous business date. `@DisallowConcurrentExecution`. |
| Preconditions | RWB-E1-018, RWB-E1-029, RWB-E1-043, RWB-E1-007 and RWB-E1-056 done; MD-2026.11 in force; `rwb.reporting.baseline-date=2026-11-27`; data lake load area available; flag `rwb.reporting.baseline` on. |
| Input | Case facts through P3; payments since entry through P1; load status through P1; definitions in force; age-band reference list; baseline date. |
| Output | `measure_snapshot` rows; INT-19 extract with business date, freshness stamp and trailer; JOB-15 job record with row count, start and end; MSG-P1-001/MSG-P9-001/MSG-P9-003/MSG-GEN-006 where applicable. |
| Feature flag | `rwb.reporting.baseline`. Off: JOB-15 does not run; the definition load remains available for setup. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `measure_definition` | `measure_code`, `definition_version`, `name`, `formula`, `data_product`, `unit`, `approved_by`, `approved_at`, `valid_from` | Load file / request | System-written on load | Required; code+version unique; `data_product`/`unit` in their LOVs; approver UUID; in force when `valid_from <= businessDate`. |
| `measure_snapshot` | `measure_code`, `definition_version`, `business_date` | Definition in force; job | System-written | Required; the version and date measured; from `MeasureCatalog.inForce(businessDate)`. |
| `measure_snapshot` | `product_group`, `dimension_code`, `dimension_value` | Case facts; calculator | System-written | LOV-PRODUCT and LOV-MEASURE-DIM; value is the route, band, queue or stage code. |
| `measure_snapshot` | `value`, `case_count`, `is_baseline`, `frozen`, `published_at` | Calculator; baseline configuration; job | System-written | numeric(18,4)/integer; baseline/frozen true only for `rwb.reporting.baseline-date`; `published_at` set at insert. |
| `Job` | `type`, `businessDate`, `status`, `startedAt`, `endedAt`, `checks` | Job monitor | System-written | `JOB-15`; Running/Complete/Failed; checks carry row count, baseline count, version and extract status. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | JOB-15 trigger at 01:30 | Quartz fires | Running | Job record created; business date resolved; definitions read. |
| Running | Date computed | Loads current and adapter accepts, or loads stale | Complete | Current rows and extract when current; no rows for a stale date with MSG-P1-001; baseline catch-up checked. |
| Running | Data lake unavailable | Adapter fails | Complete | Snapshot rows committed; extract HELD; MSG-GEN-006; resend next run. |
| Complete | Rerun a date | Frozen rows exist or not | Complete | Frozen rows unchanged with MSG-P9-001, or non-frozen rows replaced; no duplicates. |
| Running | Unexpected error | Any unhandled failure | Failed | Job record FAILED; alert; snapshot transaction rolled back. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | A definition row lacks a formula or a data product | Load refused whole; no version in force | MSG-GEN-001 naming the field |
| X2 | The baseline is republished, or a frozen row is changed directly | Frozen rows unchanged; the service records MSG-P9-001; the trigger refuses a direct update/delete | MSG-P9-001 / database error |
| X3 | The baseline date loads failed | No baseline rows; the first good run after the load passes publishes them | MSG-P1-001 naming the product and last good date |
| X4 | The data lake is unavailable | Snapshot rows written; extract held; alert; next run sends | MSG-GEN-006 naming "Data lake" |
| X5 | A configured measure has no definition in force | No value written; run record lists the measure | MSG-P9-003 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /api/recovery/v1/admin/reference-loads` (P4) with table `measure_definition`; `GET /api/recovery/v1/admin/jobs` (P1) with type `JOB-15`; `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (P1). |
| Contract delta and authorization | None. `measure_definition` is a new table code on the existing generic reference-load endpoint; the job record uses the existing `Job` schema. Backward compatible; no version change. Reference data C to load; Platform administration R to list jobs and U to rerun; Reporting R/CRUD for the snapshot read in E2. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P2-006; 422 MSG-GEN-001; 503 MSG-GEN-006. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, label or state change. SCR-44/SCR-37 are Epic 2; the Power BI report is external. | Existing frontend tests remain green; no new frontend test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-012; NFR-065; SPEC-RWB-E1-013-001..022 | New job, load handler, catalog, six calculators, snapshot repository, data lake writer and migration. | Definition load valid/invalid; effective dating; case and payment facts; each calculator; baseline marking; frozen update fails; rerun; stale load; missing definition; lake hold; 403; no personal data. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ReportingExtractJob`, `LoadStatusGuard`, `BaselineService`, `DataLakeWriter` | Job and services | JOB-15; resolves the business date; checks loads; runs calculators; writes the snapshot and extract; marks/freezes the baseline and catches up after a failed load; holds and resends the extract. |
| `MeasureDefinitionLoadHandler`, `MeasureCatalogService` | P4 handler and published interface | Validates the `measure_definition` file in full; `inForce(LocalDate)` returns the definitions effective on the date, latest `valid_from` per measure. |
| `MeasureCalculators`, repositories | Services and repositories | Six calculators, one per measure code; read/write `measure_definition`; replace non-frozen rows and insert the snapshot. |

Package `recovery.reporting.baseline`. P9 owns both tables. Case facts come only through P3 `CaseReportingApi`; payments and load status only through P1 `RecoveryDataApi`; reference data only through P4. No module reads another module's tables. `MeasureCatalog` is a published Java interface for E2-009, not an HTTP contract here.

### Data and migration

- `measure_definition` (`id`, `measure_code`, `name`, `formula`, `data_product`, `unit`, `definition_version`, `approved_by`, `approved_at`, `valid_from`, standard columns; unique `(measure_code, definition_version)`) and `measure_snapshot` (`id`, `measure_code`, `definition_version`, `business_date`, `product_group`, `dimension_code`, `dimension_value`, `value`, `case_count`, `is_baseline`, `frozen`, `published_at`, standard columns).
- `V1_013__measures.sql` creates both tables, a unique index on `(measure_code, definition_version, business_date, COALESCE(product_group,''), COALESCE(dimension_code,''), COALESCE(dimension_value,''))`, `ix_measure_snapshot_date`, and a `BEFORE UPDATE OR DELETE` trigger that raises when `OLD.frozen = true`. The physical schema draft has the tables but not the unique index or trigger; this migration adds them. `measure_publish` in TSD T3 belongs to E2-009 and is not created here. No hard-coded business values: formulas, data products, units, band edges, baseline date and measure list are data or configuration.

### Definition load and catalog

P4 calls `MeasureDefinitionLoadHandler` for table code `measure_definition` with the parsed rows and `validFrom`. Every row must have a measure code, name, formula, data product, unit, definition version, approver UUID, approval date and valid from; `data_product` and `unit` must be in their LOVs. The first missing or invalid field refuses the whole file with 422 MSG-GEN-001 naming the field; no row is written and no version is in force. On success, all rows are written in one transaction with `is_active = true`; the version is in force from `valid_from`. The row-level approver is the approval record; the story does not specify a separate P4 approve action for this table. `MeasureCatalog.inForce(onDate)` returns, per measure code, the row with the greatest `valid_from <= onDate` where `is_active = true`; a later version (MD-2026.12 in E2-009) does not change the definition used for an earlier business date.

### Rules and calculations

| Measure | Dimension | Computation | Unit |
|---|---|---|---|
| `CASES_BY_ROUTE` | `ROUTE` | Count of open cases by route and product at the business date. | COUNT |
| `CASES_BY_AGE` | `AGE_BAND` | Count of open cases by age band (`business_date − entry_date`) and product; bands 0–90, 91–180, 181–365, 366–730, over 730. | COUNT |
| `CASES_BY_QUEUE` | `QUEUE` | Count of open cases by queue code and product. | COUNT |
| `REALIZED_RECOVERY` | none | Sum of payments since entry to the business date, by product. | THB |
| `TIME_IN_STAGE` | `STAGE` | Median days from `stage_clock_start` to the run date for cases open on the business date, by stage and product. Approved as D-RCV-32. | DAYS |
| `TAT_BY_ROUTE` | `ROUTE` | Median days from `entry_date` to `closed_date` for cases closed on the business date, by route and product. Approved as D-RCV-32. | DAYS |

Open means `closed_date` is null and status is not `CLOSED`. Band edges come from the reference list; the calculator holds no day numbers. A measure with no cases writes value 0 and case count 0 where the product/dimension combination exists in the facts. The `formula` is approved plain text and is not executed; no rules engine is added.

### Snapshot, baseline, transaction and events

One row per measure, definition version, business date, product group and dimension value. The job deletes the non-frozen rows for the business date and inserts the complete set in one transaction, so a rerun replaces rather than duplicates; frozen rows are skipped and never deleted. The `COALESCE` unique index makes the key effective when a dimension is null. `published_at` is set at insert; `created_by`/`updated_by` carry the `SY-DATALOAD` identity.

`rwb.reporting.baseline-date` is `2026-11-27`; when the business date matches, every row is written with `is_baseline = true` and `frozen = true`. The trigger refuses any update or delete where `frozen = true`; the service also skips frozen rows before a rerun. A rerun of the baseline records MSG-P9-001 naming the date and leaves the rows unchanged. If the baseline date's loads were stale, the job writes no baseline rows; on every later run it checks the baseline date after the current date, and the first run whose `loadStatus` is current computes and freezes the baseline. Non-baseline dates are not frozen; a rerun replaces their rows. The definition load is one transaction. The snapshot write is one transaction per business date; the extract is written after the commit. The baseline catch-up is a separate transaction. Events: none — story §12 and the event list publish no P9 event. The job record and the frozen snapshot are the audit record.

### INT-19 extract

One file per business date, `measures/<businessDate>.csv`, written through the RWB-E1-007 outbound adapter; the module never writes to the lake directly. Header columns: `measure_code`, `definition_version`, `business_date`, `product_group`, `dimension_code`, `dimension_value`, `value`, `case_count`, `is_baseline`, `frozen`, `published_at`. The file carries the union of the current date's rows and every frozen baseline row, deduplicated by the snapshot key, unchanged. The trailer holds `businessDate`, `freshnessDate` (= business date), `recordCount`, `baselineRecordCount` and `publishedAt`. On adapter failure the file stays in the outbound staging area; the job completes with `extractStatus = HELD`, sends MSG-GEN-006 naming "Data lake" to the operations channel, and the next JOB-15 run drains the staging area before writing the new day. A partial write is not marked complete; the next run rewrites the same file. The extract is checked against `sys_fields`; no field marked personal is written. It carries codes, counts, amounts and dates only.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| `SY-DATALOAD` | Reporting C on the P9 tables; Reporting R on the P3/P1 facts; INT-19 write | All |
| `RW-REFADM` | Reference data C to load the definition file | All |
| `RW-TRIBE`, `RW-BIANAL`, `RW-FINANCE` | Reporting R / CRUD; the Tribe lead approves the definitions; the analyst builds the Power BI data set | All |
| `RW-DATASTEW`, `RW-PLATADM` | Reporting CRU / Platform administration R/U; read the run and rerun JOB-15 | All |

Every endpoint uses Spring Security method security. A role without Reference data C is refused at the load with 403 MSG-P4-002; a role without Platform administration U is refused at the rerun with 403 MSG-P4-002. The `SY-DATALOAD` grant is confirmed under CLAR-006.

### Observability, performance and rollback

- Job record: type `JOB-15`, business date, status, start/end, checks `rowCount`, `baselineRowCount`, `measureCount`, `definitionVersion`, `extractStatus`, `freshnessDate`, `lakeFile`. The platform administrator reads it through `GET /admin/jobs?type=JOB-15`; SCR-44 in E2 shows the same record.
- Metrics: rows written, baseline rows, measures computed, duration, extract held, definitions missing, loads stale. Alerts: job failed or late, extract held, no definition in force; run book under RWB-E1-056 and the operations channel. JOB-15 starts at 01:30 and must finish before the 07:30 Power BI refresh; the snapshot write is one transaction per business date and the extract is streamed after commit. The functional fixture is the 120-case synthetic set; the SIT volume is the platform data set. The story sets no numeric duration target; NFR-011 and DL11 apply.
- `rwb.reporting.baseline`. Off: JOB-15 does not run; the definition load remains available for setup. Rollback: turn the flag off; redeploy the previous tag. The migration is forward-only; the two tables and trigger remain and are harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-013-01 | AC1, BR1 | System | Six-row definition file approved by the Tribe lead, valid from 2026-11-21 | MD-2026.11 in force with six measures; `MeasureCatalog` returns each data product and formula |
| TC-E1-013-02 | AC2, BR2, BR3 | System | 120 open cases on 2026-11-27: 60 Mortgage, 45 HP, 15 SSME; known payments | Baseline and frozen rows; CASES_BY_ROUTE 120/60 Mortgage; REALIZED_RECOVERY 4,350,000.00 THB |
| TC-E1-013-03 | AC3, BR5 | System | JOB-15 on 2026-12-02 for 2026-12-01 | Extract with freshness 2026-12-01 and trailer count; baseline rows of 2026-11-27 unchanged; job record has count and times |
| TC-E1-013-04 | AC4, BR7 | System | TIME_IN_STAGE row with no formula | 422 MSG-GEN-001 naming "formula"; no version in force |
| TC-E1-013-05 | AC5, BR2 | System | Rerun JOB-15 for 2026-11-27 | Frozen rows unchanged; run record shows MSG-P9-001 naming 2026-11-27 |
| TC-E1-013-06 | AC6, BR4 | System | COLLINS load for 2026-11-27 refused at control total | No baseline rows; MSG-P1-001 naming "DP03 Case" and 2026-11-26; baseline published by the first good run |
| TC-E1-013-07 | AC7, BR5 | System | Data lake unavailable; JOB-15 runs 2026-12-01 for business date 2026-11-30 | Snapshot rows written; extract HELD; MSG-GEN-006 naming "Data lake"; next run sends |
| TC-E1-013-08 | AC8, BR1 | System | `COST_PER_CASE` configured with no definition in force | No value; run record shows MSG-P9-003 naming `COST_PER_CASE` |
| TC-E1-013-09 | Access | Security | RW-BIANAL posts `measure_definition` to `/admin/reference-loads` | 403 MSG-P4-002; nothing loaded |
| TC-E1-013-10 | BR6, BR3, PDPA | System and unit | Age-band list changed; P3/P1 stubbed; valid-from boundary; known facts and even/odd medians; frozen update/delete; AC3 extract | Re-buckets without code change; no direct table read; `inForce` right at the boundary; counts, sum and medians match; trigger refuses frozen change; no personal field in `sys_fields` |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC5; SPEC-019..021 | AC5 reruns JOB-15 "from SCR-44", but SCR-44 is first in E2. How is the rerun triggered in E1? | The rerun surface and the access test. | In E1 the platform administrator uses `GET /admin/jobs?type=JOB-15` and `POST /admin/jobs/{jobId}/rerun`; the job record carries `businessDate=2026-11-27`. SCR-44 in E2 shows the same record and action. | RESOLVED | SPEC-019, SPEC-020, SPEC-021 |
| CLAR-002 | AC7; SPEC-001, -002, -016, -017 | AC7 had the 2026-11-30 01:30 run writing rows for 2026-11-28 (a Saturday), inconsistent with AC3's previous-business-date rule. | The business-date rule and the AC7 fixture. | **Resolved 2026-11-06:** the business analyst corrected the story AC7 to run JOB-15 at 01:30 on 2026-12-01 for business date 2026-11-30; the rule stands that a run processes the previous business date, skipping Saturday and Sunday (2026-12-01 is a Tuesday; its previous business date is 2026-11-30). AC3 (2026-12-02 → 2026-12-01) and AC2 (2026-11-28 → 2026-11-27) are unchanged. The corrected AC7 is reissued in the consolidated story and every per-story copy; TC-E1-013-07 was corrected with it. | `RESOLVED` | SPEC-001, SPEC-002, SPEC-016, SPEC-017 |
| CLAR-003 | AC1, AC2; SPEC-011, -012 | TIME_IN_STAGE and TAT_BY_ROUTE are named but no approved formula or population is given. Which cases and dates are in the median? | Two of the six published measures and their unit tests. | **Ruled 2026-11-06 as D-RCV-32:** the Tribe lead approves these definitions in the MD-2026.11 row set — TIME_IN_STAGE = median days from `stage_clock_start` to the run date for cases open on the business date, by stage and product; TAT_BY_ROUTE = median days from `entry_date` to `closed_date` for cases closed on the business date, by route and product; the population is the cases the run holds and the definition rows carry the formula text. The frozen snapshot keeps the approved version (MD-2026.11). | `RESOLVED` | SPEC-011, SPEC-012 |
| CLAR-004 | BR6; SPEC-008 | Where are the age-band edges held? | The calculator must read them as data. | The five bands and edges are the story Background values, owned by the Tribe lead, loaded as a P4 reference list and read through the reference data interface; the list code is registered at load time. | RESOLVED | SPEC-008 |
| CLAR-005 | FSD A2.1.2 step 3; SPEC-019, -022 | Does JOB-15 write a decision log entry? | Whether a decision log outage can fail the run. | No; a reporting publish is not a case decision. The P4 load record, the frozen snapshot and the job record are the audit trail. The FSD step is the generic P9 template; the specific story governs. MSG-P7-003 does not arise. | RESOLVED | SPEC-019, SPEC-022 |
| CLAR-006 | Authority; SPEC-021 | Which service identity runs JOB-15 and writes the extract? | The access grants for the P3/P1 reads and P9 writes. | `SY-DATALOAD`, the outbound-file identity from RWB-E1-007, runs JOB-15; it holds Reporting C on the P9 tables and Reporting R on the P3/P1 facts. Confirm the grant with the access owner before build. | RESOLVED | SPEC-021 |
| CLAR-007 | AC1; SPEC-003 | AC1 names the approver "TRB-0001", but `approved_by` is a UUID. What does the file carry? | The load validation and the AC1 fixture. | The file carries the approver's user UUID; "TRB-0001" is the synthetic user's reference and maps to a UUID in the synthetic user set. The loader validates a non-null UUID, not a display code. | RESOLVED | SPEC-003 |
| CLAR-008 | AC8; SPEC-018 | Where is the extract configuration that lists `COST_PER_CASE` held? | How the job knows which measure codes to publish. | The measure codes are configuration `rwb.reporting.measures`, initially the six MD-2026.11 codes. A configured code with no definition is skipped with MSG-P9-003; a definition with no calculator is a run error and is not published. | RESOLVED | SPEC-018 |

`CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]` — CLAR-002 is closed by the corrected story AC7
and CLAR-003 by the D-RCV-32 approval carried into the MD-2026.11 definition rows.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source; no UI change in this story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New nightly baseline measure job and definition load; no UI or API contract change; P4 reference-load and P1 job endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: nightly baseline measure job with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 8 acceptance criteria, 5 exception paths and the access path are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Start the Implementation Planner on this specification.
```
