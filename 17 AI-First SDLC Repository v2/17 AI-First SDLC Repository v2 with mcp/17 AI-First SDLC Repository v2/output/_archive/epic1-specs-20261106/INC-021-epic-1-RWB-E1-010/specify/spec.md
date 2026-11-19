# Technical Specification — RWB-E1-010 Excel and SharePoint loads

| Field | Value |
|---|---|
| Story | RWB-E1-010 — Excel and SharePoint loads |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-021-epic-1-RWB-E1-010` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-RDF-006); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 010 Excel and SharePoint loads v1.md` |
| Upstream IDs | REQ-RDF-006; FEAT-RDF-08; US-RWB-E1-010; R-UNI-40; CTL-02; CTL-05; CTL-11; ADR-007 |
| Status | `SUCCESS` |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. Upload and sign-off are endpoints; story §15. |
| Logic In Scope | `YES` — file checks, row rejection, personal-field drop, replacement, counts, sign-off, separation of duty. |
| API In Scope | `YES` — new `POST /admin/trackers/{trackerId}/loads` (API-P1-005) and `POST /admin/trackers/{trackerId}/sign-off` (API-P1-006). |
| API Impact Type | `NEW_API_REQUIRED` — new endpoints; one response-code delta noted below. |
| Impacted Existing Nodes | `tracker_inventory` (RWB-E1-005); `load_run`, `dq_exception` (RWB-E1-003); `loan_account` (read); tracker file store. |
| New Nodes Required | `YES` — `TrackerLoadController`, `TrackerLoadService`, `TrackerFileReader`, `TrackerLoadJobConfig`, `TrackerRow`, `TrackerRowRepository`, `TrackerSignOffService`, `TrackerFileStore`. |
| Inherited Existing Behavior | Inventory and field list (RWB-E1-005); load_run/dq_exception and loan_account (RWB-E1-003); write-once storage pattern (ADR-007); notification path. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Only a tracker with decision LOAD is loaded, into the target product its inventory row names. | SPEC-RWB-E1-010-001, 007 | DIRECT | Pre-check decision and status; target from `tracker_inventory`. | COVERED |
| BR2 | A row is loaded only when its account number matches `loan_account`; other rows are rejected with a reason. | SPEC-RWB-E1-010-004 | DIRECT | TRK-01 empty account; TRK-02 unknown account; `dq_exception`. | COVERED |
| BR3 | Fields tagged personal in the field list are not stored. | SPEC-RWB-E1-010-005 | DIRECT | Drop before `tracker_row`; count `DROPPED_PERSONAL_FIELDS`. | COVERED |
| BR4 | File rows = loaded + rejected; the team manager confirms the file row count. | SPEC-RWB-E1-010-007, 011 | DIRECT | Counts on `tracker_inventory`; sign-off check. | COVERED |
| BR5 | The person who loaded the file cannot sign it off. | SPEC-RWB-E1-010-009 | DIRECT | Compare loader and signer; MSG-P7-002. | COVERED |
| BR6 | A file already loaded (same hash) is not loaded again. | SPEC-RWB-E1-010-012 | DIRECT | Unique `(tracker_id, source_file_hash)`; MSG-P1-011. | COVERED |
| BR7 | The stored file is write-once and kept as the read-only archive. | SPEC-RWB-E1-010-002 | DIRECT | Write-once container; never updated or deleted. | COVERED |
| BR8 | Tracker rows stay in `tracker_row` until the owning module maps them. | SPEC-RWB-E1-010-006 | DIRECT | No write to `legal_action` or other module tables. | COVERED |
| AC1 | A 1,240-row LIT-07 file returns 202 RUNNING and writes 1,240 rows; status LOADED. | SPEC-RWB-E1-010-001, 002, 006, 007 | DIRECT | Target DP07; source file name recorded. | COVERED |
| AC2 | The LIT team manager signs off 1,240 rows; status SIGNED_OFF. | SPEC-RWB-E1-010-008, 011 | DIRECT | Signer ID and time recorded. | COVERED |
| AC3 | 17 rows without an account number are rejected; 1,223 load; MSG-P1-008; exceptions visible. | SPEC-RWB-E1-010-004, 007 | DIRECT | TRK-01; record keys `LIT-07 row 14` etc. | COVERED |
| AC4 | No personal field value is stored; 16 other fields remain; 2 dropped. | SPEC-RWB-E1-010-005 | DIRECT | `field_values` holds 16 fields. | COVERED |
| AC5 | 5 rows with unknown accounts are rejected at TRK-02; 1,235 load. | SPEC-RWB-E1-010-004 | DIRECT | `dq_exception` rows. | COVERED |
| AC6 | A confirmed count of 1,251 against 1,240/1,223/17 is refused; status stays LOADED. | SPEC-RWB-E1-010-011 | DIRECT | MSG-P1-009. | COVERED |
| AC7 | The loader cannot sign off; MSG-P7-002. | SPEC-RWB-E1-010-009 | DIRECT | Separation of duty. | COVERED |
| AC8 | A team manager of another team gets 403. | SPEC-RWB-E1-010-010 | DIRECT | Team scope. | COVERED |
| AC9 | A KEEP tracker cannot be loaded; no file stored. | SPEC-RWB-E1-010-001 | DIRECT | MSG-P1-010. | COVERED |
| AC10 | The same file again returns 409 and changes nothing. | SPEC-RWB-E1-010-012 | DIRECT | MSG-P1-011. | COVERED |
| AC11 | A new file before sign-off replaces the rows and supersedes the earlier run. | SPEC-RWB-E1-010-006 | DIRECT | Earlier `load_run` SUPERSEDED. | COVERED |
| AC12 | A PDF returns 415. | SPEC-RWB-E1-010-013 | DIRECT | MSG-P1-018. | COVERED |
| AC13 | A missing header column refuses the load at structure; no row written. | SPEC-RWB-E1-010-003 | DIRECT | MSG-P1-002. | COVERED |
| X1 | Rows with no account number. | SPEC-RWB-E1-010-004 | DIRECT | TRK-01; rest load. | COVERED |
| X2 | Personal fields in the list. | SPEC-RWB-E1-010-005 | DIRECT | Not stored. | COVERED |
| X3 | Unknown account numbers. | SPEC-RWB-E1-010-004 | DIRECT | TRK-02. | COVERED |
| X4 | Confirmed count differs. | SPEC-RWB-E1-010-011 | DIRECT | MSG-P1-009. | COVERED |
| X5 | Signer loaded the file. | SPEC-RWB-E1-010-009 | DIRECT | MSG-P7-002. | COVERED |
| X6 | Signer from another team. | SPEC-RWB-E1-010-010 | DIRECT | 403 MSG-P4-002. | COVERED |
| X7 | Tracker not LOAD or already SIGNED_OFF/RETIRED. | SPEC-RWB-E1-010-001 | DIRECT | MSG-P1-010; no file stored. | COVERED |
| X8 | Same file again. | SPEC-RWB-E1-010-012 | DIRECT | 409 MSG-P1-011. | COVERED |
| X9 | New file before sign-off. | SPEC-RWB-E1-010-006 | DIRECT | Replace; SUPERSEDED. | COVERED |
| X10 | File not .xlsx/.csv. | SPEC-RWB-E1-010-013 | DIRECT | 415 MSG-P1-018. | COVERED |
| X11 | Header mismatch. | SPEC-RWB-E1-010-003 | DIRECT | Refuse at structure. | COVERED |
| X12 | Caller without Reference data U. | SPEC-RWB-E1-010-014 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **data steward and data product owner (RW-DATASTEW)**, I want **every inventoried tracker with a load decision loaded into its data product, with the row counts reconciled and the team manager's sign-off**, so that **the teams' own lists are held in the Workbench data store**.

The story loads the tracker content into `tracker_row`, not into the target product's business tables. It drops personal fields, rejects rows that cannot be matched to an account, and records the team manager's sign-off that the counts match. Retirement is RWB-E1-012.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | RW-DATASTEW uploads a file through `POST /admin/trackers/{trackerId}/loads`; RW-TEAMMGR signs off through `POST /admin/trackers/{trackerId}/sign-off`. |
| Preconditions | RWB-E1-005 done (inventory, field list, target product); RWB-E1-003 done (`load_run`, `dq_exception`, `loan_account`); tracker exported to .xlsx/.csv with matching headers; RW-DATASTEW Reference data U; RW-TEAMMGR Queue and allocation A, team scope; write-once container configured. |
| Input | Tracker file; confirmed file row count. |
| Output | `tracker_row`, `load_run`, `dq_exception`; tracker counts and status; MSG-P1-008. |
| Feature flag | `rwb.p1.tracker-load`. Off: upload and sign-off unavailable. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `tracker_inventory` | `decision`, `status`, `target_product` | RWB-E1-005 | Read | Decision must be LOAD; status LISTED or LOADED. |
| `tracker_inventory` | `field_list` | RWB-E1-005 | Read | Header must match; personal tags drive the drop. |
| `tracker_inventory` | `file_rows`, `loaded_rows`, `rejected_rows` | Load | System | file = loaded + rejected. |
| `tracker_inventory` | `status` | Load/sign-off | System | LISTED → LOADED → SIGNED_OFF; RETIRED is E1-012. |
| `tracker_inventory` | `signed_off_by`, `signed_off_at` | Sign-off | System | Team manager of the tracker's team; not the loader. |
| `tracker_row` | `tracker_id`, `load_run_id`, `row_no` | Load | System | One row per accepted file row. |
| `tracker_row` | `account_no`, `target_product`, `source_file_name`, `field_values`, `loaded_on` | Load | System | `field_values` excludes personal fields. |
| `load_run` | `tracker_id`, `source_file_hash`, `rows_rejected` | Load | System | Unique `(tracker_id, source_file_hash)`. |
| `load_run` | `status` | Load | System | RUNNING, COMPLETED, FAILED, SUPERSEDED. |
| `dq_exception` | `check_code`, `record_key`, `raised_on` | Rejected row | System | TRK-01 or TRK-02; record key is tracker code + row number. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| LISTED | File loaded | Decision LOAD; structure passes | LOADED | `tracker_row` written; counts; MSG-P1-008. |
| LOADED | New file loaded | Not signed off | LOADED | Earlier rows replaced; earlier run SUPERSEDED. |
| LOADED | Sign-off | Counts match; signer in team; not loader | SIGNED_OFF | Signer and time recorded. |
| LOADED | Sign-off refused | Counts differ, wrong team or loader | LOADED | MSG-P1-009/P4-002/P7-002. |
| KEEP/KEPT | Upload | Decision not LOAD | KEPT | MSG-P1-010; no file stored. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Rows without account numbers | Reject TRK-01; load the rest. | MSG-P1-008 |
| X2 | Personal fields in the list | Not stored; counted. | None |
| X3 | Unknown account numbers | Reject TRK-02. | MSG-P1-008 |
| X4 | Confirmed count differs | Refuse sign-off; stays LOADED. | MSG-P1-009 |
| X5 | Signer loaded the file | Refuse. | MSG-P7-002 |
| X6 | Signer from another team | Refuse. | MSG-P4-002 |
| X7 | Tracker not LOAD / already signed off or retired | Refuse; no file stored. | MSG-P1-010 |
| X8 | Same file again | 409; no change. | MSG-P1-011 |
| X9 | New file before sign-off | Replace rows; earlier run SUPERSEDED. | MSG-P1-008 |
| X10 | File not .xlsx/.csv | 415; nothing stored. | MSG-P1-018 |
| X11 | Header mismatch | Refuse at structure; no row. | MSG-P1-002 |
| X12 | Caller without Reference data U | 403. | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | `POST /admin/trackers/{trackerId}/loads` (API-P1-005); `POST /admin/trackers/{trackerId}/sign-off` (API-P1-006). |
| Contract delta | The story requires **202** on a successful upload; API Specification v2 lists **200**. Update the contract to 202. The request/response schemas otherwise match (`Job`, `TrackerSignOff`, `Tracker`). |
| Backward compatibility | New endpoints; no existing consumer. |
| Authorization | Reference data U for upload; Queue and allocation A, scope Team for sign-off. |
| Error behaviour | 400 MSG-GEN-001; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P1-010/011/009/P7-002/GEN-004; 413/415 MSG-P1-018; 503 MSG-GEN-006. |
| Versioning | Additive; update API Specification v2 before implementation (RWB-TE-003). |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | Story §15 states no screen; upload and sign-off are endpoints. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-006; SPEC-RWB-E1-010-001..016 | New controller, service, reader, batch job, row repository, sign-off service and file store. | Positive, negative, boundary and error-path tests: .xlsx/.csv; wrong type; header mismatch; TRK-01/02; personal drop; replace; counts; separation of duty; team scope; hash; 403. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `TrackerLoadController` | Controller | Upload and sign-off endpoints; capability checks; Problem mapping. |
| `TrackerLoadService` | Service | Pre-checks, file store, `load_run`, launch of `trackerLoadJob`. |
| `TrackerFileReader` | Service | Reads .xlsx (POI streaming) and .csv; checks the header against the field list. |
| `TrackerLoadJobConfig` | Spring Batch job | Row checks, personal drop, replace/write `tracker_row`, counts. |
| `TrackerRow` | Entity | Maps `tracker_row`. |
| `TrackerRowRepository` | Repository | Deletes the tracker's earlier rows and inserts the new ones in one transaction. |
| `TrackerSignOffService` | Service | Team scope, separation of duty, count check, status change with optimistic lock. |
| `TrackerFileStore` | Service | Writes the file to the write-once container; returns reference and SHA-256. |

### Data and migration

- Migration `V1_010__tracker_row.sql` creates `tracker_row` (`tracker_id`, `load_run_id`, `row_no`, `account_no`, `target_product`, `source_file_name`, `field_values` jsonb, `loaded_on`, standard columns; indexes on tracker and account).
- Adds `file_rows`, `loaded_rows`, `rejected_rows`, `last_load_run_id`, `signed_off_by`, `signed_off_at`, `source_file_ref` to `tracker_inventory`.
- Adds `tracker_id`, `rows_rejected`, `loaded_by`, `source_file_name`, `source_file_hash` to `load_run`; unique `(tracker_id, source_file_hash)`; adds SUPERSEDED to the status values.
- The write-once container is a property; `recovery-tracker-files` is the story's value (CLAR-001).

### Rules

1. Upload pre-checks: decision LOAD; status LISTED or LOADED; .xlsx or .csv; at most 20 MB; file hash not already loaded for the tracker.
2. Header columns must equal the field list names; a missing or extra column refuses the load at structure.
3. For each row: empty account number → TRK-01; account not in `loan_account` → TRK-02; both write `dq_exception`.
4. Personal fields are dropped before `tracker_row`; `field_values` holds only the non-personal fields.
5. Accepted rows replace the tracker's earlier rows in one transaction; the earlier `load_run` becomes SUPERSEDED.
6. `file_rows = loaded_rows + rejected_rows`; status LOADED; MSG-P1-008 to data steward and team manager.
7. Sign-off: status must be LOADED; signer holds Queue and allocation A with team scope; signer is not the loader; confirmed count equals `file_rows`.
8. A repeated sign-off by the same user returns the existing SIGNED_OFF tracker.

### Transaction and events

- `tracker_row` replacement and the tracker counts are one transaction.
- The file is written to the write-once store before the job starts; it is never changed or deleted.
- No event is published; the load result is the tracker status and `load_run`.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-DATASTEW | Reference data U — upload | All |
| RW-TEAMMGR | Queue and allocation A — sign off | Team |
| SY-DATALOAD | Run the load; write rows and counts | All |
| RW-COE, RW-DATASTEW, RW-PLATADM, RW-AUDIT | Platform administration R — list runs and rejected rows | All |
| Any other role | None | 403 MSG-P4-002 |

No personal data is stored in `tracker_row`; rejected rows are named by tracker code and row number only.

### Observability and operations

- `load_run`: tracker, file name, hash, rows read/loaded/rejected, status, check results.
- `tracker_inventory`: counts, status, signer and time.
- `GET /admin/data-quality/exceptions` shows the rejected rows.
- No scheduled job; `trackerLoadJob` is launched by the upload. A FAILED run is rerun by the platform administrator from the stored file.

### Performance

- The AC file is 1,240 rows; the reader streams .xlsx and .csv.
- The replacement is one delete/insert transaction per tracker; indexes on tracker and account.
- The 20 MB limit bounds memory; the file is stored once and read once.

### Feature flag and rollback

- `rwb.p1.tracker-load`. Off: upload and sign-off unavailable.
- Rollback: turn the flag off; the stored files and rows remain; a new file replaces the rows when the flag is on again.

### No UI change

No screen. SCR-44 shows the loads from Epic 2; the endpoints are used directly until then.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-010-01 | AC1, BR1, BR7 | System | LIT-07 file, 1,240 matched rows | 202 RUNNING; 1,240 rows for DP07; LOADED |
| TC-E1-010-02 | AC2, BR4 | System | 1,240/1,240/0; LIT manager | SIGNED_OFF with signer and time |
| TC-E1-010-03 | AC3, BR2 | System | 17 rows without account numbers | 1,223 rows; 17 TRK-01; MSG-P1-008; exceptions visible |
| TC-E1-010-04 | AC4, BR3 | System | Field list with two personal fields | No personal value; 16 fields; DROPPED_PERSONAL_FIELDS = 2 |
| TC-E1-010-05 | AC5, BR2 | System | 5 unknown accounts | 5 TRK-02; 1,235 rows |
| TC-E1-010-06 | AC6, BR4 | System | Confirmed 1,251 vs 1,240/1,223/17 | Refused; MSG-P1-009; stays LOADED |
| TC-E1-010-07 | AC7, BR5 | System | One user loads and signs | Refused; MSG-P7-002 |
| TC-E1-010-08 | AC8 | System | NPA manager signs LIT-07 | 403 MSG-P4-002 |
| TC-E1-010-09 | AC9, BR1 | System | TDR-03 KEEP | Refused; MSG-P1-010; no file |
| TC-E1-010-10 | AC10, BR6 | System | Same file hash twice | 409 MSG-P1-011; rows unchanged |
| TC-E1-010-11 | AC11 | System | Second file 1,262 rows before sign-off | 1,262 rows; earlier run SUPERSEDED |
| TC-E1-010-12 | AC12 | System | PDF | 415 MSG-P1-018 |
| TC-E1-010-13 | AC13 | System | No "Court name" column | Refused at structure; no row |
| TC-E1-010-14 | X12 | Security | RW-TEAMMGR uploads | 403 MSG-P4-002 |
| TC-E1-010-15 | BR4, BR5 | Unit | Count boundaries; loader = signer | Count check; separation of duty |

## Guardrails

- Field lists, target products and the size limit are data.
- No personal data in logs, tests or prompts; personal fields are dropped before storage; rejected rows are named by tracker code and row number.
- No read of another module's tables; tracker rows stay in `tracker_row`; no write to `legal_action` or other module tables.
- The stored tracker file is never changed or deleted by the Workbench.

## Out of scope

- Retiring the local copy and business sign-off (RWB-E1-012).
- Mapping tracker content into `legal_action`, asset or treatment records (Epic 5).
- A tracker load screen (SCR-44, Epic 2); KEEP trackers.

## Traceability

| Requirement ID | Requirement (short) | Feature | Rules | Test cases |
|---|---|---|---|---|
| REQ-RDF-006 | Each LOAD file loaded, counts reconciled, local copy retired with owner confirmation | FEAT-RDF-08 | R-UNI-40; CTL-02; CTL-05; CTL-11 | TC-E1-010-01..15 |

## Clarification Log

| CLAR_ID | Requirement/Spec Reference | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR7; SPEC-002 | §3 names the container `recovery-tracker-files`; §13 says the platform administrator sets the container name. | The storage target. | Make it a property; `recovery-tracker-files` is the DEV/SIT value. | `RESOLVED` | SPEC-002 |
| CLAR-002 | AC1; SPEC-001 | Story AC1 returns 202; API Specification v2 returns 200. | The upload response contract. | The story AC requires 202; update the API schema to 202. | `RESOLVED` | SPEC-001 |
| CLAR-003 | AC13; SPEC-003 | AC13 says "the previous load is still in use", but the tracker is LISTED and has no previous load. | Message wording only. | MSG-P1-002 is the standard refusal message; the tracker state is unchanged. No behaviour change. | `RESOLVED` | SPEC-003 |
| CLAR-004 | BR6; SPEC-012 | Is the hash unique per tracker or across all trackers? | Re-upload detection. | Per tracker: unique `(tracker_id, source_file_hash)`. | `RESOLVED` | SPEC-012 |
| CLAR-005 | BR4; SPEC-011 | What count does the team manager confirm? | Sign-off check. | The file row count; it must equal loaded + rejected. | `RESOLVED` | SPEC-011 |

`CLARIFICATION_STATUS: RESOLVED` — all 5 items are answered from the story or API contract. No open
item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New tracker upload and sign-off capability; two new endpoints; no UI.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new tracker load and sign-off endpoints with row checks]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 13 acceptance criteria and 12 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
