# Technical Specification — RWB-E1-003 ALS daily extract load

| Field | Value |
|---|---|
| Story | RWB-E1-003 — ALS daily extract load |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-011-epic-1-RWB-E1-003` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-RDF-002); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 003 ALS daily extract load v1.md` |
| Upstream IDs | REQ-RDF-002; FEAT-RDF-03; US-RWB-E1-003; DQ-001..DQ-014; R-UNI-40; CTL-02; NFR-013; DL25 |
| Status | `SUCCESS` |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. Alerts and `GET /admin/jobs` are the surfaces; SCR-44 is Epic 2. |
| Logic In Scope | `YES` — seven load checks, tolerance handling, mapping, transaction, movement and sample checks, events. |
| API In Scope | `NO` — no new or changed contract. Reuses `GET /api/recovery/v1/admin/jobs` (API-P1-001) and `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (API-P1-002). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `JOB-01` (new); `loan_account`, `account_payment`, `load_run`, `dq_exception`, `source_field_map`, `source_code_map` (new or extended); outbox. |
| New Nodes Required | `YES` — `CollinsLoadJob`, `AlsLoadJobConfig`, `LoadCheckRunner`, `SourceMappingService`, `LoanAccountWriter`, `AccountPaymentWriter`, `LoadRunQueryService`, `LoadEventPublisher`, `LoadAlertNotifier`. |
| Inherited Existing Behavior | Recovery tables (RWB-E1-001); reference data and working-day calendar (RWB-E1-043); parameter catalogue (RWB-E1-042); job monitor and rerun (RWB-E1-056). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A load is refused in full if business date, structure, control totals or keys fail; previous load stays in use; `LoadRefused` is published. | SPEC-RWB-E1-003-003, 009, 012 | DIRECT | Blocking checks DQ-001..004 and DQ-008..011 run before the write; one transaction per interface. | COVERED |
| BR2 | A record with an unmatched reference or code is held; above 0.50% the load is refused. | SPEC-RWB-E1-003-004, 006 | DIRECT | DQ-005/006 for INT-01; DQ-012/013 for INT-02; boundary is strictly greater than 0.50%. | COVERED |
| BR3 | A count or balance change above 10% is loaded and alerted. | SPEC-RWB-E1-003-007 | DIRECT | DQ-007/014; boundary is strictly greater than 10.00%. | COVERED |
| BR4 | JOB-01 starts at 05:00 and retries hourly until 09:00. | SPEC-RWB-E1-003-001, 011 | DIRECT | Quartz cron plus retry to `load.window.end`; `@DisallowConcurrentExecution`. | COVERED |
| BR5 | Every loaded row carries the business date in `data_as_of`. | SPEC-RWB-E1-003-005, 018 | DIRECT | Set from the load, not from the source field. | COVERED |
| BR6 | Buddhist Era years become Gregorian; amounts are THB numeric(18,2); codes map through the versioned code map. | SPEC-RWB-E1-003-005 | DIRECT | Transformations `TO_DATE_BE`, `TO_NUMERIC_2`, `CODE_MAP`. | COVERED |
| BR7 | Source fields map through the approved mapping version; an unapproved mapping refuses the load. | SPEC-RWB-E1-003-005 | DIRECT | `source_field_map.approved_on` and `valid_from` checked before the write. | COVERED |
| BR8 | A repeated run for a completed business date changes nothing. | SPEC-RWB-E1-003-002, 010 | DIRECT | Unique active run key; rerun returns 409 MSG-P1-011. | COVERED |
| BR9 | Load results are recorded on `load_run`, not the decision log. | SPEC-RWB-E1-003-002, 009 | DIRECT | No case exists; no decision log entry. | COVERED |
| AC1 | 184,500 accounts and 2,310 payments load by 07:00 with 0 held and one `LoadCompleted` per interface. | SPEC-RWB-E1-003-001, 002, 005, 009 | DIRECT | Two Spring Batch steps; INT-02 after INT-01. | COVERED |
| AC2 | A trailer count mismatch refuses INT-01 at DQ-003; previous data stays; alert and `LoadRefused`. | SPEC-RWB-E1-003-003, 009, 017 | DIRECT | No row changes; `failedCheck = DQ-003`. | COVERED |
| AC3 | The 50-account sample matches the staging values and records "50 of 50". | SPEC-RWB-E1-003-008 | DIRECT | Random sample after the write, read back from `loan_account`. | COVERED |
| AC4 | A wrong business date refuses at DQ-001. | SPEC-RWB-E1-003-003 | DIRECT | Compare staging and trailer date with the expected date. | COVERED |
| AC5 | A duplicate account key refuses at DQ-004. | SPEC-RWB-E1-003-003 | DIRECT | Count distinct keys against row count. | COVERED |
| AC6 | 11 unmatched payments (0.48%) are held and 2,299 are written. | SPEC-RWB-E1-003-004, 006 | DIRECT | DQ-012; 11 `dq_exception` rows; status COMPLETED. | COVERED |
| AC7 | 13 unmatched payments (0.56%) refuse INT-02 at DQ-012. | SPEC-RWB-E1-003-004, 012 | DIRECT | No `account_payment` row for the date. | COVERED |
| AC8 | 3 records with bucket Z9 are held at DQ-006 and 184,497 load. | SPEC-RWB-E1-003-004, 006 | DIRECT | Code map miss; record held, not refused. | COVERED |
| AC9 | An 11.82% movement loads and alerts; exactly 10.00% sends no alert. | SPEC-RWB-E1-003-007, 017 | DIRECT | DQ-007; strict `>` comparison. | COVERED |
| AC10 | No delivery by 09:00 leaves status LATE, previous data and a `LoadRefused` with `LATE`. | SPEC-RWB-E1-003-001, 011 | DIRECT | Last attempt at the window end. | COVERED |
| AC11 | A rerun of a COMPLETED load returns 409 and changes nothing. | SPEC-RWB-E1-003-010 | DIRECT | MSG-P1-011. | COVERED |
| AC12 | Two nodes at 05:00 produce one run row and no duplicate accounts. | SPEC-RWB-E1-003-002, 013 | DIRECT | Unique active run key; upsert by `account_no`. | COVERED |
| AC13 | A database failure after 90,000 rows leaves no 2026-11-30 row; status FAILED; 06:00 attempt completes. | SPEC-RWB-E1-003-012, 001 | DIRECT | One transaction per interface; retry at the next hourly trigger. | COVERED |
| AC14 | A rerun after a refused load returns 200 RUNNING and completes with 184,500 accounts. | SPEC-RWB-E1-003-010, 009 | DIRECT | New attempt; `LoadCompleted` once. | COVERED |
| X1 | A blocking check fails. | SPEC-RWB-E1-003-003 | DIRECT | Refuse whole; MSG-P1-002. | COVERED |
| X2 | Wrong business date. | SPEC-RWB-E1-003-003 | DIRECT | DQ-001. | COVERED |
| X3 | Duplicate account key. | SPEC-RWB-E1-003-003 | DIRECT | DQ-004. | COVERED |
| X4 | Unmatched references at or below 0.50%. | SPEC-RWB-E1-003-004 | DIRECT | Held; count on `load_run`. | COVERED |
| X5 | Unmatched references above 0.50%. | SPEC-RWB-E1-003-004 | DIRECT | Refuse. | COVERED |
| X6 | Source code missing from the code map. | SPEC-RWB-E1-003-004 | DIRECT | DQ-006; held. | COVERED |
| X7 | Movement above 10%. | SPEC-RWB-E1-003-007 | DIRECT | Loaded; MSG-P1-006. | COVERED |
| X8 | No delivery by 09:00. | SPEC-RWB-E1-003-011 | DIRECT | LATE. | COVERED |
| X9 | Rerun of a completed date. | SPEC-RWB-E1-003-010 | DIRECT | 409 MSG-P1-011. | COVERED |
| X10 | Two nodes start together. | SPEC-RWB-E1-003-013 | DIRECT | One run; unique key. | COVERED |
| X11 | Database failure during the write. | SPEC-RWB-E1-003-012 | DIRECT | Rollback; FAILED; next attempt. | COVERED |
| X12 | Caller without Platform administration U. | SPEC-RWB-E1-003-014 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **data steward and data product owner (RW-DATASTEW)**, I want **ALS balances, arrears, payments and classification loaded every working day from the COLLINS daily batch for accounts at 90 days past due or more**, so that **account and arrears data is current to the previous working day**.

The job reads COLLINS staging, not ALS. It writes DP01 and publishes the load result; it does not create cases or make decisions. The data steward and platform administrator read `GET /admin/jobs` and receive alerts.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Quartz `JOB-01 COLLINS load check and intake` at 05:00 Asia/Bangkok on working days; retry every 60 minutes to 09:00. |
| Preconditions | RWB-E1-001 done; COLLINS INT-01/INT-02 staging and trailer present; mapping and code map approved; working-day calendar loaded; parameters `load.window.end`, `load.retry.interval`, `load.hold.tolerance.pct`, `load.movement.tolerance.pct`, `load.sample.size`; service identity SY-DATALOAD. |
| Input | INT-01 account records, INT-02 payment records, trailer (count, balance total, business date), staging table names from configuration. |
| Output | `loan_account`, `account_payment`, `load_run`, `dq_exception`; `LoadCompleted`/`LoadRefused`; alerts. |
| Feature flag | `rwb.p1.als-load`. Off: JOB-01 skips INT-01/INT-02 and records nothing. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `loan_account` | `account_no` | INT-01 account key | System | Unique; upsert key. |
| `loan_account` | `total_balance`, `days_past_due`, `classification` | INT-01 after mapping | System | Sample check compares to staging. |
| `loan_account` | `data_as_of` | Load business date | System | Required; previous date kept on refusal. |
| `loan_account` | DF-ACC-001..021 | INT-01 mapped fields | System | All columns written; see TSD T3.1. |
| `account_payment` | `account_id`, `payment_code` | INT-02 after account lookup | System | Unique pair; `ON CONFLICT DO NOTHING`. |
| `account_payment` | `data_as_of` | Load business date | System | Required. |
| `load_run` | `interface_id`, `business_date` | Job | System | Unique while RUNNING or COMPLETED. |
| `load_run` | `status` | Job | System | RUNNING, COMPLETED, REFUSED, LATE, FAILED. |
| `load_run` | `rows_read`, `rows_loaded`, `rows_held`, `failed_check` | Checks | System | Counts per attempt. |
| `dq_exception` | `check_code`, `record_key`, `raised_on` | Held row | System | No personal value; account key only. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | JOB-01 trigger | No active run for interface/date | RUNNING | New `load_run`. |
| RUNNING | Checks and write complete | All blocking checks pass | COMPLETED | Rows written; `LoadCompleted`. |
| RUNNING | Blocking check fails, or held > 0.50% | Any refusal condition | REFUSED | No row change; `LoadRefused`. |
| RUNNING | Window end reached | No complete delivery | LATE | No row change; `LoadRefused` with LATE. |
| RUNNING | Write error | Database or step error | FAILED | Rollback; next attempt. |
| REFUSED/LATE/FAILED | Next attempt or rerun | Delivery present | RUNNING | New attempt row. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Blocking check fails | Refuse whole; nothing written. | MSG-P1-002; `LoadRefused` |
| X2 | Wrong business date | Refuse at DQ-001. | MSG-P1-002 |
| X3 | Duplicate account key | Refuse at DQ-004. | MSG-P1-002 |
| X4 | Unmatched references ≤ 0.50% | Hold the records; load the rest. | Count on `load_run` |
| X5 | Unmatched references > 0.50% | Refuse whole. | MSG-P1-002 |
| X6 | Code missing from the map | Hold the record at DQ-006. | Count on `load_run` |
| X7 | Movement > 10% | Load and alert. | MSG-P1-006 |
| X8 | No delivery by 09:00 | LATE; previous data stays. | MSG-P1-002; `LoadRefused` LATE |
| X9 | Rerun of a completed date | 409; nothing changes. | MSG-P1-011 |
| X10 | Two nodes start together | One run proceeds; the other stops at the unique key. | None |
| X11 | Database failure during the write | Rollback; FAILED; next hourly attempt. | Alert |
| X12 | Caller without Platform administration U | 403. | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/jobs` (API-P1-001); `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (API-P1-002). |
| Contract delta | None. `Job` already carries id, type, businessDate, status, startedAt, endedAt and checks. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R for the list; Platform administration U for rerun. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P1-011; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | Story §15 states no screen; alerts and `GET /admin/jobs` only. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-002; SPEC-RWB-E1-003-001..018 | New job, batch steps, check runner, mapper, writers, event publisher and notifier. | Positive, negative, boundary and error-path tests: each check pass/fail; 0.50% and 10.00% boundaries; wrong date; duplicate key; code miss; sample; movement; late; rerun; concurrency; rollback; 403. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `CollinsLoadJob` | Quartz job | JOB-01 trigger; expected business date from the calendar; launches INT-01 then INT-02; `@DisallowConcurrentExecution`. |
| `AlsLoadJobConfig` | Spring Batch job | Open run, blocking checks, tolerance checks, map/write, movement, sample, close. |
| `LoadCheckRunner` | Service | Runs DQ checks by SQL over staging; returns a `CheckResult` per code. |
| `SourceMappingService` | Service | Reads approved mapping and code map; applies COPY_TRIM, SUM, TO_DATE_BE, TO_NUMERIC_2, BOOLEAN_YN, CODE_MAP, BUSINESS_DATE. |
| `LoanAccountWriter`, `AccountPaymentWriter` | Repository | Upsert `loan_account` by `account_no`; insert `account_payment` by `(account_id, payment_code)`. |
| `LoadRunRepository`, `DqExceptionRepository` | Repository | Read and write the load tables. |
| `LoadRunQueryService` | Service / published interface | Implements `LoadRunQuery.completedLoad(interfaceId, businessDate)`. |
| `LoadEventPublisher` | Service | Writes `LoadCompleted` and `LoadRefused` to the outbox. |
| `LoadAlertNotifier` | Service | Sends MSG-P1-002 and MSG-P1-006 to the recipient groups. |
| `RecoveryDataEngineController` | Controller | `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun`. |

### Data and migration

- Writes `loan_account` (all columns) and `account_payment` (all columns).
- Migration `V1_003__load_run.sql` creates `load_run`, `dq_exception`, `source_field_map`, `source_code_map`, `uk_load_run_active UNIQUE (interface_id, business_date) WHERE status IN ('RUNNING','COMPLETED')`, `uk_loan_account_no`, `uk_account_payment`, and an index on `dq_exception (product_code, raised_on)`.
- Staging table names are configuration, not schema objects owned by P1.
- Each attempt opens a new `load_run` row; the previous attempt keeps its terminal status. The active-row unique index prevents two live attempts.

### Rules

1. Expected business date = previous working day from the reference-data calendar.
2. DQ-001 business date, DQ-002 structure, DQ-003 control total and DQ-004 keys are blocking.
3. DQ-008..DQ-011 are blocking checks from the check catalogue; the story names the codes but not their SQL. No SQL is invented here.
4. DQ-005/DQ-006 apply to INT-01 references and codes; DQ-012/DQ-013 apply to INT-02 unmatched account keys. DQ-012 is the code on held payments (AC6/AC7).
5. Held ratio = held / read. Refuse when ratio > `load.hold.tolerance.pct`; at exactly 0.50% hold and continue.
6. Movement = absolute change against the previous completed load. Alert when > `load.movement.tolerance.pct`; at exactly 10.00% no alert.
7. Mapping version must have `approved_on` and be in force; otherwise refuse.
8. `data_as_of` is the load business date on every row.

### Transaction and events

- One transaction per interface for the write. A failure rolls back every row of that interface; the other interface is independent.
- `LoadCompleted` (EV-26) and `LoadRefused` (EV-27) are written to the outbox in the same transaction as the `load_run` status.
- No decision log entry: a load has no case. `load_run` is the record.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Run JOB-01; write load tables | All |
| RW-PLATADM | Platform administration R/U | All |
| RW-SECADM | Platform administration CRUDA (break-glass) | All |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY | Platform administration R | All |
| Any other role | None | 403 MSG-P4-002 |

No personal data in logs or `dq_exception`; `record_key` is the account key only.

### Observability and operations

- `load_run`: interface, business date, status, counts, failed check, mapping version, check results.
- Alerts: refusal, late delivery, movement; recipient groups from reference data.
- Metrics: rows read/loaded/held, duration, refusal count, late count.
- Run book and job monitor from RWB-E1-056; SCR-44 in Epic 2.

### Performance

- 184,500 accounts and 2,310 payments complete before 07:00; the story's SIT target is under 30 minutes.
- Set-based mapping and batch insert; one transaction per interface; no per-row commit.
- The sample check reads 50 rows after the write; it does not scan the full table.

### Feature flag and rollback

- `rwb.p1.als-load`. Off: JOB-01 skips both steps and records nothing.
- Rollback: turn the flag off; redeploy the previous tag. The migration is forward-only; new tables remain harmless.

### No UI change

No screen. The data steward and platform administrator use `GET /admin/jobs` and alerts. SCR-44 arrives in Epic 2.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-003-01 | AC1, BR4, BR5 | System | 184,500 accounts; 2,310 payments; 2026-11-30 | 184,500 rows by 07:00; counts 184,500/0 and 2,310/0; one `LoadCompleted` per interface |
| TC-E1-003-02 | AC2, BR1 | System | Trailer 184,500 vs 184,498 | Refused at DQ-003; no row change; MSG-P1-002; `LoadRefused` |
| TC-E1-003-03 | AC3, BR6, BR7 | System | Completed load; 50 random accounts | All 50 match; "SAMPLE" = "50 of 50" |
| TC-E1-003-04 | AC4, BR1 | System | Staging dated 2026-11-27 | Refused at DQ-001 |
| TC-E1-003-05 | AC5, BR1 | System | ACC0000017 twice | Refused at DQ-004 |
| TC-E1-003-06 | AC6, BR2 | System | 11/2,310 unknown payment accounts (0.48%) | 2,299 written; 11 held at DQ-012; COMPLETED |
| TC-E1-003-07 | AC7, BR2 | System | 13/2,310 unknown (0.56%) | Refused at DQ-012; no payment row |
| TC-E1-003-08 | AC8, BR2, BR6 | System | 3 records with bucket Z9 | 3 held at DQ-006; 184,497 loaded |
| TC-E1-003-09 | AC9, BR3 | System | 165,000 → 184,500 (11.82%); exactly 10.00% | Alert at 11.82%; no alert at 10.00% |
| TC-E1-003-10 | AC10, BR4 | System | Empty staging until 09:00 | LATE; previous data; MSG-P1-002; `LoadRefused` LATE |
| TC-E1-003-11 | AC11, BR8 | System | Completed load; rerun | 409 MSG-P1-011; no change |
| TC-E1-003-12 | AC12, BR8 | System | Two scheduler nodes | One `load_run`; 184,500 unique accounts |
| TC-E1-003-13 | AC13, BR1 | System | Connection cut after 90,000 rows | No 2026-11-30 row; FAILED; 06:00 attempt COMPLETED |
| TC-E1-003-14 | AC14 | System | Refused load; corrected staging | 200 RUNNING; 184,500; one `LoadCompleted` |
| TC-E1-003-15 | X12 | Security | RW-DATASTEW rerun | 403 MSG-P4-002 |
| TC-E1-003-16 | BR2, BR3 | Unit | 0.50% and 10.00% boundaries; each check | Hold at boundary; alert only above |

## Guardrails

- Tolerances, window, sample size, mappings and code maps are data.
- No personal data in logs, tests or prompts; `dq_exception.record_key` holds the account key only.
- No read of another module's tables; reference values come through P4.
- No call to ALS or another system of record; input is COLLINS staging only (ADR-005).
- No partial load is visible: one transaction per interface.

## Out of scope

- Case creation (JOB-02, RWB-E1-018), payment matching (JOB-07), DQ rules (RWB-E1-006), reconciliation (RWB-E1-011).
- Freshness and stale flag (RWB-E1-015), SCBPDM/UDP and EFS loads, SCR-44 (Epic 2).

## Traceability

| Requirement ID | Requirement (short) | Feature | Rules | Test cases |
|---|---|---|---|---|
| REQ-RDF-002 | Balances, arrears, payments and classification current to the previous working day | FEAT-RDF-03 | DQ-001..014; R-UNI-40; CTL-02; NFR-013; DL25 | TC-E1-003-01..16 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR2, AC6, AC7; SPEC-004, 006 | Flow step 4 names DQ-005 for unmatched references; X4/X5 and AC6/AC7 name DQ-012 for unmatched payments. | The check code written on held payments. | FSD AC-EXC-P1-003-03 and the story ACs use DQ-012 for INT-02 payments; DQ-005 remains the INT-01 reference check. | `RESOLVED` | SPEC-004, 006 |
| CLAR-002 | BR8, AC13; SPEC-002 | Does a retry reuse the failed `load_run` row or open a new one? | Job counts and the unique-key behaviour. | The story's unique active key and AC11/AC14 imply one active row per attempt; each attempt opens a new row and the previous keeps its terminal status. Implementation decision, no business change. | `RESOLVED` | SPEC-002 |
| CLAR-003 | BR3, AC9; SPEC-007 | Is exactly 10.00% a breach? | Whether an alert is sent at the boundary. | AC9: "a change of exactly 10.00 percent sends no alert"; alert only above. | `RESOLVED` | SPEC-007 |
| CLAR-004 | BR2, AC6; SPEC-004 | Is exactly 0.50% held or refused? | Whether the load continues at the boundary. | BR2: above 0.50% refuses; at or below holds. | `RESOLVED` | SPEC-004 |
| CLAR-005 | BR1; SPEC-003 | DQ-008..DQ-011 are named as blocking but their SQL is not in the story. | The check implementation. | The codes are fixed; the definitions come from the DQ check catalogue. The spec does not invent SQL. | `RESOLVED` | SPEC-003 |
| CLAR-006 | BR9; SPEC-009 | Is a decision log entry required for a load? | Audit path. | BR9: no; a load has no case and `load_run` is the record. | `RESOLVED` | SPEC-009 |
| CLAR-007 | BR4; SPEC-001 | Is the expected business date the previous working day? | The trigger date and DQ-001. | Story §4.1 and the working-day calendar. | `RESOLVED` | SPEC-001 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, FSD or TSD. No open item
changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New daily ALS load job; no UI or API contract change; existing job list and rerun endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new load job and checks with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 9 business rules, 14 acceptance criteria and 12 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
