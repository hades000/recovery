<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 010 Excel and SharePoint loads v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 010 Excel and SharePoint loads v1.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-010 Excel and SharePoint loads

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-010 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-08 Load the tracker data into the data store |
| Requirement IDs | REQ-RDF-006 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-005, RWB-E1-003 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **every inventoried tracker with a load decision loaded into its data product, with the row counts reconciled and the team manager's sign-off**, so that **the teams' own lists are held in the Workbench data store**.

## 2. Business rationale

The recovery teams hold case facts in trackers that only they can see, so the facts are lost when the tracker is retired unless they are loaded first. This story loads each tracker file with a LOAD decision into the tracker content of its target data product, rejects rows that cannot be matched to an account, drops fields tagged as personal data, and records the team manager's sign-off that the counts match the file. It meets the load and reconcile part of REQ-RDF-006; the retirement is RWB-E1-012.

## 3. Preconditions

- RWB-E1-005 is done: the tracker inventory is loaded and each LOAD tracker names its target data product and its field list with personal data tags.
- RWB-E1-003 is done: load_run, dq_exception and loan_account exist and loan_account is loaded.
- The team has exported the tracker to an .xlsx or .csv file with a header row whose column names match the field list in the inventory.
- The data steward holds Reference data U. The team manager of the tracker's team holds Queue and allocation A.
- The tracker file store (ACE storage pattern, write-once container `recovery-tracker-files`) is configured.

## 4. Flow

1. Data steward: calls `POST /admin/trackers/{trackerId}/loads` with the tracker file.
2. System: checks the tracker has decision LOAD and status LISTED or LOADED, the file type, and that the file hash has not been loaded before.
3. System: stores the file in the write-once tracker file store, opens a load_run for the tracker and returns 202 with the Job.
4. System: checks that the header columns match the field list; a mismatch refuses the file.
5. System: for each row, rejects it if the account number is empty (TRK-01) or not in loan_account (TRK-02), and writes the rejection to dq_exception with the row number.
6. System: drops every field tagged as personal data and writes the other fields of each accepted row to tracker_row with the target data product, the file name and the row number, in one transaction; rows of an earlier load of the same tracker are replaced.
7. System: sets the file rows, loaded rows and rejected rows on the tracker, sets status LOADED and sends MSG-P1-008 to the data steward and the team manager.
8. Team manager: calls `POST /admin/trackers/{trackerId}/sign-off` with the row count of the file the team knows.
9. System: checks the signer is not the person who loaded the file, belongs to the tracker's team, and that the confirmed count equals the file rows, which equal loaded plus rejected rows.
10. System: sets status SIGNED_OFF with the signer and the time.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Rows with no account number | Rows rejected with TRK-01; the rest loaded; counts reported | MSG-P1-008 | AC3 |
| X2 | Fields tagged personal in the field list | Not stored; counted on the load_run | None | AC4 |
| X3 | Rows whose account number is not in loan_account | Rows rejected with TRK-02 | MSG-P1-008 | AC5 |
| X4 | The confirmed count at sign-off differs from the file rows | Sign-off refused; status stays LOADED | MSG-P1-009 | AC6 |
| X5 | The signer loaded the file | Sign-off refused | MSG-P7-002 | AC7 |
| X6 | The signer is a team manager of another team | Sign-off refused | MSG-P4-002 | AC8 |
| X7 | The tracker's decision is not LOAD, or it is already SIGNED_OFF or RETIRED | Load refused; no file stored | MSG-P1-010 | AC9 |
| X8 | The same file is uploaded again | 409; nothing changes | MSG-P1-011 | AC10 |
| X9 | A new file for a tracker already LOADED and not signed off | The earlier rows are replaced; the earlier load_run is SUPERSEDED | MSG-P1-008 | AC11 |
| X10 | The file is not .xlsx or .csv | 415; nothing stored | MSG-P1-018 | AC12 |
| X11 | The header does not match the field list | Load refused at structure; no row written | MSG-P1-002 | AC13 |
| X12 | A role without Reference data U uploads a file | 403 | MSG-P4-002 | TC-E1-010-14 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the inventory of RWB-E1-005 and the account data of RWB-E1-003; the retirement story builds on it |
| Negotiable | The field list and the target product are data in the inventory; the story fixes the checks and the sign-off |
| Valuable | The teams' case facts are kept in the Workbench before any tracker is retired |
| Estimable | One upload endpoint, one sign-off endpoint, one batch step, one table |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Each criterion below is one automated test on synthetic tracker files |

## 7. Acceptance criteria

```gherkin
Feature: Excel and SharePoint loads

  Background:
    Given tracker "LIT-07 Litigation case tracker" of team LIT has decision LOAD, target data product DP07 and status LISTED
    Given its field list holds 18 fields, of which "Customer name" and "Mobile" are tagged personal

  Scenario: AC1 File loaded
    Given the file "LIT-07 Litigation tracker 2026-11-20.xlsx" with 1,240 rows, each with an account number found in loan_account
    When the data steward calls POST /admin/trackers/{trackerId}/loads with the file
    Then the response is 202 with a Job of type "TRACKER" and status RUNNING
    Then tracker_row holds 1,240 rows for LIT-07 with target data product DP07 and source file name "LIT-07 Litigation tracker 2026-11-20.xlsx"
    Then the tracker shows 1,240 file rows, 1,240 loaded, 0 rejected and status LOADED

  Scenario: AC2 Reconciled
    Given the LIT-07 load shows 1,240 file rows, 1,240 loaded and 0 rejected
    When the team manager of team LIT calls POST /admin/trackers/{trackerId}/sign-off with confirmed row count 1,240
    Then the tracker status is SIGNED_OFF with the team manager's user ID and the sign-off time

  Scenario: AC3 Rejected rows
    Given the LIT-07 file has 1,240 rows, of which 17 have no account number
    When the load runs
    Then the system writes 1,223 rows to tracker_row
    Then the system writes 17 dq_exception rows with check code "TRK-01" and record keys "LIT-07 row 14" to "LIT-07 row 1,205"
    Then the data steward and the LIT team manager receive MSG-P1-008 "1,223 rows loaded from LIT-07 Litigation tracker 2026-11-20.xlsx. 17 rows rejected; the reject list is on the load."
    Then GET /admin/data-quality/exceptions with product "DP07" returns the 17 rejected rows

  Scenario: AC4 Personal fields are dropped
    Given the LIT-07 file of 1,240 rows
    When the load runs
    Then no tracker_row holds a value for "Customer name" or "Mobile"
    Then each tracker_row holds the 16 other fields
    Then the load_run check results show "DROPPED_PERSONAL_FIELDS" = 2

  Scenario: AC5 Account number not found
    Given 5 rows of the LIT-07 file carry account numbers not in loan_account
    When the load runs
    Then the system rejects the 5 rows with check code "TRK-02"
    Then the system writes 1,235 rows

  Scenario: AC6 Counts do not match at sign-off
    Given the LIT-07 load shows 1,240 file rows, 1,223 loaded and 17 rejected
    When the team manager of team LIT signs off with confirmed row count 1,251
    Then the system refuses the sign-off with MSG-P1-009 "The counts do not match: 1,251 rows confirmed, 1,240 rows in the file, 1,223 loaded, 17 rejected. Sign-off is not allowed."
    Then the tracker status stays LOADED

  Scenario: AC7 The person who loaded cannot sign off
    Given a user who holds RW-DATASTEW and RW-TEAMMGR for team LIT loaded the LIT-07 file
    When the same user signs off
    Then the system refuses the sign-off with MSG-P7-002 "You prepared this decision, so you cannot approve it."

  Scenario: AC8 Team manager of another team
    Given the LIT-07 load is LOADED
    When the team manager of team NPA signs off LIT-07
    Then the system refuses the sign-off with 403 and MSG-P4-002

  Scenario: AC9 Tracker without a load decision
    Given tracker "TDR-03 Restructure follow-up list" has decision KEEP and status KEPT
    When the data steward uploads a file for TDR-03
    Then the system refuses the upload with MSG-P1-010 "TDR-03 cannot be loaded: its decision is KEEP and its status is KEPT."
    Then the system stores no file

  Scenario: AC10 Same file uploaded again
    Given "LIT-07 Litigation tracker 2026-11-20.xlsx" was loaded on 2026-11-20
    When the data steward uploads the same file again
    Then the response is 409 with MSG-P1-011
    Then tracker_row is unchanged

  Scenario: AC11 New file before sign-off
    Given the LIT-07 load of 2026-11-20 is LOADED with 1,223 rows and not signed off
    When the data steward uploads "LIT-07 Litigation tracker 2026-11-23.xlsx" with 1,262 rows, all matched
    Then tracker_row holds 1,262 rows for LIT-07, all from the 2026-11-23 file
    Then the load_run of 2026-11-20 has status SUPERSEDED

  Scenario: AC12 File type not allowed
    Given a file "LIT-07 tracker.pdf"
    When the data steward uploads it for LIT-07
    Then the response is 415 with MSG-P1-018 "Use an .xlsx or .csv file of at most 20 MB for a tracker load."

  Scenario: AC13 Header does not match the field list
    Given the LIT-07 file has no column "Court name", which is in the field list
    When the load runs
    Then the system refuses the load at structure with MSG-P1-002 "The LIT-07 load for 2026-11-20 was refused: structure. The previous load is still in use."
    Then no tracker_row for that file is written
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a tracker with decision LOAD is loaded, into the target data product its inventory row names | REQ-RDF-006; RWB-E1-005 BR2 |
| BR2 | A row is loaded only when its account number matches loan_account; other rows are rejected with a reason | References load check (INT load checks); CTL-02 |
| BR3 | Fields tagged personal in the field list are not stored | CTL-11; PDPA minimization (FEAT-RDF-15) |
| BR4 | The file rows equal the loaded rows plus the rejected rows, and the team manager confirms the file row count | REQ-RDF-006 |
| BR5 | The person who loaded the file cannot sign it off | Separation of duty, "a person may not approve a decision they prepared"; CTL-05 |
| BR6 | A file already loaded (same hash) is not loaded again | R-UNI-40 |
| BR7 | The stored file is write-once and kept as the read-only archive copy | ADR-007 storage pattern; REQ-RDF-006 |
| BR8 | Tracker rows are held as tracker content until the owning module maps them into its own tables | Case file item "Tracker content"; ADR-002 |

## 9. State transitions

None. This story does not change a case status. It changes the tracker status and the load_run status.

| From | Event | Condition | To |
|---|---|---|---|
| LISTED | Tracker file loaded | Decision LOAD; structure check passed | LOADED |
| LOADED | New tracker file loaded | Not signed off | LOADED (earlier load_run SUPERSEDED) |
| LOADED | Sign-off | Counts match; signer is in the team and did not load the file | SIGNED_OFF |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Uploads a tracker file (Reference data U) |
| RW-TEAMMGR, team manager of the tracker's team | Signs off the counts (Queue and allocation A, scope Team) |
| SY-DATALOAD, data load from COLLINS | Runs the load; writes tracker_row, load_run, dq_exception and the tracker counts |
| RW-COE, RW-DATASTEW, RW-PLATADM, RW-AUDIT | List the runs (Platform administration R) and the rejected rows |

The sign-off is not an approval within the delegation of authority; no approval level applies.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-002 | loan_account | account_no | Read (row match) |
| DF-OPS-094 | tracker_inventory | decision | Read and write |
| DF-OPS-096 | tracker_inventory | status | Read and write |
| DF-OPS-093 | tracker_inventory | target_product | Read and write |
| DF-OPS-091 | tracker_inventory | field_list | Read and write |
| DF-OPS-086 | tracker_inventory | team_code | Read and write |
| DF-OPS-098 | tracker_inventory | file_rows | Read and write |
| DF-OPS-099 | tracker_inventory | loaded_rows | Read and write |
| DF-OPS-100 | tracker_inventory | rejected_rows | Read and write |
| DF-OPS-101 | tracker_inventory | last_load_run_id | Read and write |
| DF-OPS-102 | tracker_inventory | signed_off_by | Read and write |
| DF-OPS-103 | tracker_inventory | signed_off_at | Read and write |
| DF-OPS-109 | tracker_row | id | Write |
| DF-OPS-110 | tracker_row | tracker_id | Write |
| DF-OPS-111 | tracker_row | load_run_id | Write |
| DF-OPS-112 | tracker_row | row_no | Write |
| DF-OPS-113 | tracker_row | account_no | Write |
| DF-OPS-114 | tracker_row | target_product | Write |
| DF-OPS-115 | tracker_row | source_file_name | Write |
| DF-OPS-116 | tracker_row | field_values | Write |
| DF-OPS-117 | tracker_row | loaded_on | Write |
| DF-OPS-021 | load_run | id | Write |
| DF-OPS-022 | load_run | interface_id | Write |
| DF-OPS-023 | load_run | job_code | Write |
| DF-OPS-024 | load_run | product_code | Write |
| DF-OPS-026 | load_run | status | Write |
| DF-OPS-029 | load_run | rows_read | Write |
| DF-OPS-030 | load_run | rows_loaded | Write |
| DF-OPS-032 | load_run | rows_rejected | Write |
| DF-OPS-034 | load_run | check_results | Write |
| DF-OPS-039 | load_run | source_file_name | Write |
| DF-OPS-040 | load_run | source_file_hash | Write |
| DF-OPS-037 | load_run | tracker_id | Write |
| DF-OPS-038 | load_run | loaded_by | Write |
| DF-OPS-044 | dq_exception | check_code | Write |
| DF-OPS-045 | dq_exception | record_key | Write |
| DF-OPS-046 | dq_exception | reason_code | Write |
| DF-OPS-048 | dq_exception | raised_on | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /admin/trackers/{trackerId}/loads** (new endpoint, recorded in the additions file)

| Item | Value |
|---|---|
| Request | multipart/form-data: `file` (binary, .xlsx or .csv, at most 20 MB); header `Idempotency-Key` |
| Response 202 | `Job`: id, type "TRACKER", businessDate (upload date), status RUNNING, startedAt |
| 403 | Role lacks Reference data U (MSG-P4-002) |
| 404 | No tracker with that id (MSG-P4-003) |
| 409 | Decision not LOAD or status not LISTED or LOADED (MSG-P1-010); same file hash already loaded (MSG-P1-011) |
| 413 | File above 20 MB (MSG-P1-018) |
| 415 | File type not allowed (MSG-P1-018) |
| 401, 503 | MSG-P4-001; storage or database unavailable |
| Authorization | Reference data U |
| Idempotency | Idempotency-Key header; the file SHA-256 hash per tracker |

**POST /admin/trackers/{trackerId}/sign-off** (new endpoint, recorded in the additions file)

| Item | Value |
|---|---|
| Request | `TrackerSignOff`: confirmedFileRows (integer, required), comment (string, up to 400 characters) |
| Response 200 | `Tracker` with status SIGNED_OFF, signedOffBy, signedOffAt |
| 400 | confirmedFileRows missing (MSG-GEN-001) |
| 403 | Role lacks Queue and allocation A, or the signer is not in the tracker's team (MSG-P4-002) |
| 409 | Status not LOADED (MSG-P1-010); counts do not match (MSG-P1-009); signer loaded the file (MSG-P7-002); record changed by someone else (MSG-GEN-004) |
| Authorization | Queue and allocation A, scope Team |
| Idempotency | A second sign-off of a SIGNED_OFF tracker by the same user returns 200 with the same Tracker |

**Job.** The load runs as Spring Batch job `trackerLoadJob`, launched by the upload; it is not a scheduled job and has no entry in the daily timeline. Restart: a FAILED run is rerun by POST /admin/jobs/{jobId}/rerun (Platform administration U) from the stored file.

## 13. Solution plan

**Package.** Folder `recovery/dataengine/tracker`, Java package `recovery.dataengine.tracker`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TrackerLoadController | Controller | The upload and sign-off endpoints; capability checks; Problem mapping |
| TrackerLoadService | Service | Pre-checks, file store, load_run, launch of trackerLoadJob |
| TrackerFileReader | Service | Reads .xlsx (Apache POI streaming) and .csv; checks the header against the field list |
| TrackerLoadJobConfig | Job (Spring Batch) | Row checks, personal field drop, replace and write of tracker_row, counts |
| TrackerRow | Entity | Maps tracker_row |
| TrackerRowRepository | Repository | Deletes the tracker's earlier rows and inserts the new ones in one transaction |
| TrackerSignOffService | Service | Team scope, separation of duty, count check, status change with optimistic lock |
| TrackerFileStore | Service | Writes the file to the write-once container and returns its reference and hash |

**Database.** Migration `V1_010__tracker_row.sql` creates tracker_row (tracker_id uuid references tracker_inventory, load_run_id uuid references load_run, row_no integer, account_no varchar(20), target_product varchar(4), source_file_name varchar(200), field_values jsonb, loaded_on date, standard columns; index on tracker_id and on account_no); adds file_rows, loaded_rows, rejected_rows integer, last_load_run_id uuid, signed_off_by uuid, signed_off_at timestamptz and source_file_ref varchar(400) to tracker_inventory; adds tracker_id uuid, rows_rejected integer, loaded_by uuid, source_file_name varchar(200) and source_file_hash char(64) to load_run, with a unique index on (tracker_id, source_file_hash), and SUPERSEDED to the load_run status values.

**Configuration and reference data.** The field list and target product per tracker come from the inventory (RWB-E1-005). File size limit `tracker.file.max.mb` 20 (assumed, DL11) from the parameter catalog. Container name set by the platform administrator.

**Build steps**

1. Write migration V1_010, TrackerRow and its repository.
2. Write TrackerFileStore and TrackerFileReader; test .xlsx, .csv, a wrong type and a header mismatch.
3. Write TrackerLoadService pre-checks (decision, status, hash) and the 202 response.
4. Write TrackerLoadJobConfig with TRK-01 and TRK-02 rejections, the personal field drop and the replace of earlier rows.
5. Write the counts, the LOADED status, the SUPERSEDED earlier run and MSG-P1-008 through the ACE notification path.
6. Write TrackerSignOffService with the team scope, the separation of duty check and the count check.
7. Write TrackerLoadController with both endpoints and their capability checks.

**Feature flag.** `rwb.p1.tracker-load`.

**Done when.** The tests in section 16 pass, and the 14 LOAD trackers of the SIT inventory load from synthetic files.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-008 | Load complete | {loaded} rows loaded from {file}. {rejected} rows rejected; the reject list is on the load. |
| MSG-P1-009 | Counts do not match at sign-off | The counts do not match: {confirmed} rows confirmed, {fileRows} rows in the file, {loaded} loaded, {rejected} rejected. Sign-off is not allowed. |
| MSG-P1-010 | Tracker not loadable | {tracker} cannot be loaded: its decision is {decision} and its status is {status}. |
| MSG-P1-011 | Same file again | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P1-018 | File type or size not allowed | Use an .xlsx or .csv file of at most {size} MB for a tracker load. |
| MSG-P1-002 | Header does not match | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P7-002 | Signer loaded the file | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | Confirmed count missing | Enter {field}. |
| MSG-GEN-004 | Tracker changed by someone else | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role or team without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. The data steward uploads the file through the endpoint and the team manager signs off through the endpoint, in the same way as reference data loads before SCR-40 arrives in E8. The loads show on SCR-44 from E2.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-010-01 | AC1, BR1, BR7 | System | Synthetic LIT-07 file of 1,240 matched rows |
| TC-E1-010-02 | AC2, BR4 | System | LIT-07 loaded with 1,240 rows; LIT team manager |
| TC-E1-010-03 | AC3, BR2 | System | LIT-07 file with 17 rows without account numbers |
| TC-E1-010-04 | AC4, BR3 | System | Field list with two personal fields |
| TC-E1-010-05 | AC5, BR2 | System | 5 rows with unknown account numbers |
| TC-E1-010-06 | AC6, BR4 | System | Confirmed count 1,251 against 1,240 |
| TC-E1-010-07 | AC7, BR5 | System | One user with RW-DATASTEW and RW-TEAMMGR |
| TC-E1-010-08 | AC8 | System | NPA team manager signs LIT-07 |
| TC-E1-010-09 | AC9, BR1 | System | Tracker TDR-03 with decision KEEP |
| TC-E1-010-10 | AC10, BR6 | System | Same file hash twice |
| TC-E1-010-11 | AC11 | System | Second file of 1,262 rows before sign-off |
| TC-E1-010-12 | AC12 | System | PDF file |
| TC-E1-010-13 | AC13 | System | File without the column Court name |
| TC-E1-010-14 | Access | Access | RW-TEAMMGR uploads a file; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: field lists, target products and the size limit are data.
- No personal data in logs, tests or prompts. Personal fields are dropped before storage; rejected rows are named by tracker code and row number only; test files are synthetic.
- No read of another module's tables. Tracker rows stay in tracker_row; no write to legal_action or any other module's table.
- The stored tracker file is never changed or deleted by the Workbench.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-006 | Each LOAD file loaded, counts reconciled, local copy retired with owner confirmation | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-08 | All recovery processes | R-UNI-40; CTL-02; CTL-05; CTL-11 | TC-E1-010-01 to TC-E1-010-14 |

## 19. Out of scope

- Retiring the local copy and the business sign-off (RWB-E1-012).
- Mapping tracker content into legal_action, asset or treatment records (S4, S5 and S2 in their epics).
- A screen for tracker loads (SCR-44 Interface and job monitor, Epic 2).
- Trackers with a KEEP decision.
