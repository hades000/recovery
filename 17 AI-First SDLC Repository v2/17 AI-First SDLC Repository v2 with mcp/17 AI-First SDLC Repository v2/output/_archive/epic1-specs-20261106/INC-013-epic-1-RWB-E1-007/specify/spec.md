# Technical Specification — RWB-E1-007 Integration adapters for file loads and outbound files

| Field | Value |
|---|---|
| Story | RWB-E1-007 — Integration adapters for file loads and outbound files |
| Epic / module | E1 / P2 Integration |
| RUN_ID | `INC-013-epic-1-RWB-E1-007` |
| Source requirement | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 007 Integration adapters for file loads and outbound files v1.md`; REQ-DRI-006, 007, 008; BRD Epic 1 §3.2; BRD Program §5.2 |
| Upstream IDs | REQ-DRI-006..008; FEAT-RDF-21, 23, 24; FEAT-DRI-09, 10, 11, 13; R-UNI-33..36, 40; ADR-005; DT12; INT-10, 11, 14, 15; DL11 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Platform administrator; see `compliance-validation.md` |
## Change Scope Declaration
| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — SCR-09 Exception queue gains the outbound item list (interface, attempt count, last error, case count) and the resend action; states Loading and list. |
| Logic In Scope | `YES` — inbound file checks, run status, duplicate and missing handling, outbound retry, exception move, case events, idempotency and resend. |
| API In Scope | `YES` — two new E1 endpoints: `GET /admin/outbound-items` and `POST /admin/outbound-items/{itemId}/resend`. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `interface_run` (new); `outbound_item` (new); `processed_event` (new); `interface_config` (new); SCR-09 Exception queue; `recovery_case.route_state` and `task` through P3; `DataProductStatus.markStale` through P1. |
| New Nodes Required | `YES` — `FileLoadAdapterImpl`; `FileCheckRunner`; `OutboundFilesImpl`; `OutboundSender`; `SftpTransport`; `IdempotencyGuardImpl`; four repositories and entities; `FileLoadJob`; `IntegrationController`; `AdapterBoundaryTest`. |
| Inherited Existing Behavior | Recovery schema (RWB-E1-001); P1 loaders and data-product status (RWB-E1-015/016); P3 case events and tasks; P6 notice approval; ACE audit log; key store (NFR-052); Quartz scheduler. |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage
| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | No component calls a system of record directly; files move only through the adapters. | SPEC-RWB-E1-007-001 | DIRECT | Only `SftpTransport` opens a session; `AdapterBoundaryTest` enforces it. | COVERED |
| BR2 | A file failing business date, structure, control total or key check is refused in full; the previous load stays in use. | SPEC-RWB-E1-007-004, SPEC-RWB-E1-007-005 | DIRECT | Checks run on header/trailer before any record is passed. | COVERED |
| BR3 | A data product is marked stale one business day after its file was due. | SPEC-RWB-E1-007-007 | DIRECT | Missing run; `DataProductStatus.markStale` through P1. | COVERED |
| BR4 | An outbound file is retried on the intervals in its configuration row; after the third failure a task goes to the owning team. | SPEC-RWB-E1-007-010, SPEC-RWB-E1-007-011, SPEC-RWB-E1-007-012 | DIRECT | `max_attempts`, `retry_intervals_min`, `owner_role` are data. | COVERED |
| BR5 | A system that is unavailable queues the action and retries. | SPEC-RWB-E1-007-011, SPEC-RWB-E1-007-014 | DIRECT | `SYSTEM_UNAVAILABLE` for each case; item RETRY. | COVERED |
| BR6 | An item that fails after the retry limit moves to the exception queue with a task for the owner. | SPEC-RWB-E1-007-012 | DIRECT | Item EXCEPTION; task `RESOLVE_OUTBOUND_ITEM`; cases `EXCEPTION_QUEUE`. | COVERED |
| BR7 | An event with a key already processed is ignored and the hit is counted. | SPEC-RWB-E1-007-013 | DIRECT | `processed_event` primary key `(consumer, idempotency_key)`; `hit_count`. | COVERED |
| BR8 | Retry counts, intervals, folders, patterns and owners are data rows, never code. | SPEC-RWB-E1-007-002 | DIRECT | `interface_config` version in force; no literal in the adapter. | COVERED |
| AC2 | A CCMS file with trailer total 4,201 against 4,200 records is refused whole; no record passes; previous load stays; stale; data steward alerted. | SPEC-RWB-E1-007-004, SPEC-RWB-E1-007-005 | DIRECT | Failed check `DQ-059 Control total`; MSG-P1-002. | COVERED |
| AC3 | A WIN outbound file for 85 notices fails three times; retries at +5 and +15; cases RETRY_QUEUE after attempt 1; item EXCEPTION after attempt 3; cases EXCEPTION_QUEUE with task; MSG-P2-001. | SPEC-RWB-E1-007-010..012, SPEC-RWB-E1-007-014 | DIRECT | Intervals from the row; one task per case? One task per case group; see CLAR-001. | COVERED |
| AC4 | A CCMS file with header business date 2026-11-02 when 2026-11-09 is expected is refused with DQ-057; run REFUSED, count 0. | SPEC-RWB-E1-007-004, SPEC-RWB-E1-007-005 | DIRECT | First check fails; no record used. | COVERED |
| AC5 | No SVAF file by Monday 04:00: run MISSING; SVAF stale on 2026-11-10 with MSG-P1-001. | SPEC-RWB-E1-007-007 | DIRECT | JOB-09 writes MISSING; stale next business day. | COVERED |
| AC6 | The same CCMS file arrives again: run DUPLICATE; no record passed. | SPEC-RWB-E1-007-006 | DIRECT | Unique `(interface_id, business_date, file_hash)`. | COVERED |
| AC7 | The same event key arrives twice: consumer does not act; hit count 2. | SPEC-RWB-E1-007-013 | DIRECT | `IdempotencyGuard.firstTime` returns false; increments. | COVERED |
| AC8 | Two senders pick the same item: sent once; attempt count 1. | SPEC-RWB-E1-007-010 | DIRECT | `FOR UPDATE SKIP LOCKED`; row lock. | COVERED |
| AC9 | A platform administrator resends an EXCEPTION item: PENDING, attempt count 0; audit with user and time; MSG-GEN-005. | SPEC-RWB-E1-007-015, SPEC-RWB-E1-007-019 | DIRECT | 200; version check; audit write. | COVERED |
| X1–X3 | A file check fails; the outbound transfer fails; the retry limit is reached. | SPEC-RWB-E1-007-005, 011, 012 | DIRECT | REFUSED with stale; RETRY with RETRY_QUEUE; EXCEPTION with task and EXCEPTION_QUEUE. | COVERED |
| X4–X6 | No file by cut-off; the same file again; the same event key again. | SPEC-RWB-E1-007-006, 007, 013 | DIRECT | MISSING; DUPLICATE; event ignored with hit count. | COVERED |
| X7–X9 | Two senders on one item; resend an EXCEPTION item; a role without the right. | SPEC-RWB-E1-007-010, 015, 018 | DIRECT | One send; PENDING with attempt 0 and audit; 403. | COVERED |
> **AC cleanup (4 November 2026):** the development-process criteria removed from story §7 are not mapped here. The remaining acceptance criteria are those in the current story.

## User story intent interpretation
As a **platform administrator (RW-PLATADM)**, I want **one adapter pattern for every file load and outbound file, with file checks, a run log, retry and an exception queue**, so that **every later interface follows one pattern and a failed file is found on the day it fails**.

The story builds the single path every file takes in and out: the inbound adapter writes a run row, runs the data-held checks on the header and trailer, and hands records to the owning module's loader only when every check passes. The outbound side writes one item in the caller's transaction, sends it on a schedule held as data, and moves it to the exception queue with a task after the last attempt. The platform administrator sees failed items on SCR-09 and resends one. No case status changes; P3 moves the route state when the adapter raises an event.
## Entry trigger and preconditions
| Item | Value |
|---|---|
| Trigger | JOB-09 file loads (weekly Monday 04:00; monthly on the 2nd working day); JOB-10 WIN outbound notices daily 16:00; JOB-11 outbox sender every minute. |
| Preconditions | RWB-E1-001 schema; `interface_config` version `IF-2026.11` for INT-10, INT-11, INT-14, INT-15; load check rows DQ-057..DQ-063 and DQ-085..DQ-091 in force; SFTP folders in DEV/SIT; credentials in the key store; `SY-DATALOAD` managed identity; Quartz runs JOB-09/10/11. |
| Input | Inbound file matching `file_pattern`; approved notices from P6; outbound items due; interface configuration rows. |
| Output | `interface_run` row; `outbound_item` row; `processed_event` row; records to the owning loader; case events and tasks through P3; SCR-09 list; audit on resend. |
| Feature flag | `rwb.integration.file-adapters`. Off: JOB-09/10/11 do not run; no item is sent; existing data stays in use. |
## Field-level behaviour matrix
| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `interface_config` | `interface_id`, `direction`, `transport`, `inbound_path`, `file_pattern`, `data_product`, `max_attempts`, `retry_intervals_min`, `owner_role`, `alert_role`, `valid_from`, `valid_to` | Reference data (RW-REFADM) | Read-only to the adapter | Version in force for the business date |
| `interface_run` | `file_name`, `file_hash`, `business_date`, `record_count`, `control_total`, `status`, `failed_check`, `checks`, `started_at`, `ended_at` | Adapter | System writes | Unique `(interface_id, business_date, file_hash)`; status in LOV-INTERFACE-RUN |
| `outbound_item` | `idempotency_key`, `payload_ref`, `case_ids`, `attempt_count`, `next_attempt_at`, `status`, `last_error`, `owner_role` | Caller + sender | System writes; resend resets status/attempt | Unique `idempotency_key`; status in LOV-OUTBOUND-STATUS |
| `processed_event` | `consumer`, `idempotency_key`, `event_id`, `hit_count`, `last_seen_at` | Consumer | System writes | Primary key `(consumer, idempotency_key)` |
| `recovery_case` | `route_state` | Current state | P3 writes on the adapter event | RETRY_QUEUE, RESUME_STATE, EXCEPTION_QUEUE |
## Status-transition matrix
| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| — | File found | — | `RECEIVED` | Run row with name, hash, business date |
| `RECEIVED` | Every check passes | Loader accepts | `LOADED` | Record count; records to the loader |
| `RECEIVED` | A check fails | Any DQ check | `REFUSED` | Count 0; previous load stays; stale; MSG-P1-002 |
| — | No file by cut-off | — | `MISSING` | Stale next business day; MSG-P1-001 |
| — | Same interface, date and hash | Already loaded | `DUPLICATE` | No record passed |
| `PENDING` | Sender succeeds | — | `SENT` | Attempt count +1 |
| `PENDING`/`RETRY` | Transfer fails | Attempts left | `RETRY` | Next attempt from the row; cases RETRY_QUEUE on first failure |
| `RETRY` | Transfer fails | No attempts left | `EXCEPTION` | Task; cases EXCEPTION_QUEUE; MSG-P2-001 |
| `EXCEPTION` | Platform administrator resends | Version matches | `PENDING` | Attempt count 0; audit entry |
## Exceptional-case behaviour
| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | File check fails | Refused whole; no record; previous load stays; stale; data steward alert | MSG-P1-002 |
| X2 | Outbound transfer fails | Item RETRY; cases RETRY_QUEUE; next attempt from the row | MSG-GEN-006; `SYSTEM_UNAVAILABLE` |
| X3 | Retry limit reached | Item EXCEPTION; task for `owner_role`; cases EXCEPTION_QUEUE | MSG-P2-001; `OUTBOUND_FAILED` |
| X4 | No file by cut-off | Run MISSING; stale next business day | MSG-P1-001 |
| X5 | Same file again | Run DUPLICATE; nothing loaded | None |
| X6 | Same event key again | Consumer does not act; hit count +1 | None |
| X7 | Two senders on one item | One sends; the other skips | None |
| X8 | Resend an EXCEPTION item | PENDING, attempt 0; audit with user and time | MSG-GEN-005 |
| X9 | Role without Platform administration R/U | 403; nothing changes | MSG-P4-002 |
## API change assessment
| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | `GET /api/recovery/v1/admin/outbound-items` (Platform administration R); `POST /api/recovery/v1/admin/outbound-items/{itemId}/resend` (Platform administration U). |
| Contract delta | Query `status`, `interfaceId`, `from`, `to`; `OutboundItem` response with `id`, `interfaceId`, `status`, `attemptCount`, `lastError`, `caseCount`, `ownerRole`, `updatedAt`, `version`; resend returns the item. The resend requires an `If-Match` header with the item version — the OpenAPI file must declare it. |
| Backward compatibility | New endpoints; no existing operation changes. |
| Authorization | Platform administration R for the list, U for the resend; scope applied; 403 MSG-P4-002. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-GEN-004 (not EXCEPTION or version changed); 503 MSG-GEN-006. |
| Versioning | No version change; both operations are first in E1. |
## Unit Test Applicability
| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | AC2, AC3, AC9; SPEC-RWB-E1-007-016, SPEC-RWB-E1-007-017 | SCR-09 gains the outbound item list and the resend action. | Component tests cover loading, empty, list, error, 403, 404, 409, successful resend and refresh; keyboard and label checks. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR8; SPEC-RWB-E1-007-001..025 | New adapter, checks, sender, idempotency, repositories and endpoints. | Positive, negative, boundary and error-path tests: each check, refusal, duplicate, missing, retry boundary 2/3, exception, lock, idempotency, resend, access. |
## Detailed design
### Components
| Component | Type | Responsibility |
|---|---|---|
| `IntegrationController` | Controller | Two exception-queue endpoints; maps errors to Problem responses. |
| `FileLoadAdapterImpl` | Service | Lists the inbound folder, writes the run row, runs checks, passes records to `RecordLoader`. |
| `FileCheckRunner` | Service | Runs business date, structure, control total and key checks from the DQ rows. |
| `OutboundFilesImpl` | Service | Writes `outbound_item` in the caller's transaction; `enqueue` published interface. |
| `OutboundSender` | Job | JOB-11; sends due items, applies retry intervals, moves to EXCEPTION, raises case events. |
| `SftpTransport` | Service | The only class that opens SFTP; credentials from the key store. |
| `IdempotencyGuardImpl` | Service | Inserts `processed_event`; on conflict increments `hit_count` and returns false. |
| Repositories/entities | Repository/Entity | `interface_config`, `interface_run`, `outbound_item`, `processed_event` only. |

### Data and migration
Flyway `V2026_11_07__p2_adapter_tables.sql` creates the four tables in schema `recovery` with the standard columns. Constraints: unique `(interface_id, business_date, file_hash)` on `interface_run`; unique `idempotency_key` on `outbound_item`; primary key `(consumer, idempotency_key)` on `processed_event`; index `(status, next_attempt_at)` on `outbound_item`. `caseCount` is the size of `case_ids`; no name, address or identifier is stored in the item.

### Inbound flow
1. JOB-09 reads the configuration row in force and lists the inbound folder for `file_pattern` and business date.
2. Write `RECEIVED` with file name, SHA-256 hash (64 hex characters) and business date.
3. Run every check on the header and trailer before any record is passed: business date, structure, control total, keys.
4. On failure, write `REFUSED`, count 0, mark the product stale, alert the data steward, and pass no record.
5. On success, call `RecordLoader.load` through the owning module's published interface and write `LOADED` with the record count.
6. A second file with the same interface, business date and hash writes `DUPLICATE` and loads nothing.
7. No file by the cut-off writes `MISSING`; the product is marked stale on the next business day.

### Outbound flow and retry
1. The owning module calls `OutboundFiles.enqueue` in its transaction; one `outbound_item` is written with an idempotency key.
2. JOB-11 selects `PENDING`/`RETRY` items with `next_attempt_at <= now` using `FOR UPDATE SKIP LOCKED`.
3. On success, mark `SENT`, increment the attempt count; `ACKNOWLEDGED` when the acknowledgment for the interface and business date is matched (RWB-E1-055 owns the WIN acknowledgment content).
4. On failure, increment the attempt count, set `next_attempt_at` from `retry_intervals_min`, set `RETRY`, and raise `SYSTEM_UNAVAILABLE` for each case on the first failure.
5. When the attempt count reaches `max_attempts`, set `EXCEPTION`, raise `OUTBOUND_FAILED` for each case and one task for `owner_role`, and log MSG-P2-001.
6. A `SENT` item without acknowledgment after 30 minutes (DL11) is sent again.

### Idempotency and events
`IdempotencyGuard.firstTime(consumer, key)` inserts `processed_event`; on conflict it increments `hit_count` and returns false. Every consumer of an application event calls it before acting. Events raised through P3: `SYSTEM_UNAVAILABLE`, `RETRY_SUCCEEDED`, `RETRY_LIMIT_REACHED`, `OUTBOUND_FAILED`. No event is published by P2 itself for a file load; P1 publishes `LoadCompleted` or `LoadRefused`.

### Security and authority
| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Read files, write runs/items, send files | All |
| SY-CASEWF | Move route state; raise task | All |
| RW-PLATADM | Platform administration R/U | All |
| RW-DATASTEW, RW-REFADM, RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Platform administration R; load interface configuration | All |

Every endpoint has a Spring Security method check. The resend writes the ACE audit log with the user and the time. File contents are never logged; only names, counts, hashes and check results.

### Observability and operations
- Metrics and alerts: files received/loaded/refused/missing/duplicate; items sent/retried/exception; refused load, missing file, item in EXCEPTION, sender late.
- Run book and job monitor: RWB-E1-056; SCR-09 shows exception items; log events `rwb.integration.load.refused` and `rwb.integration.job.failed`.

### Performance
- JOB-11 every minute; batch size is data; `SKIP LOCKED` keeps two instances apart.
- Inbound checks run on the header/trailer before the record stream; a large file is streamed to the loader.
- No numeric throughput target is stated; record SIT duration (DL11).

### Feature flag and rollback
`rwb.integration.file-adapters`. Off: JOB-09/10/11 do not run and no item is sent; the tables and endpoints remain. Rollback: turn the flag off, redeploy the previous tag; the migration is forward-only and additive.

### UI behaviour (SCR-09)
The platform administrator sees failed outbound items with interface, attempt count, last error and case count; the list has Loading and list states; resend asks for confirmation, is disabled without Platform administration U, shows MSG-GEN-004 on a version conflict and MSG-GEN-005 on success, and refreshes the row. The screen specification SCR-09 currently lists case fields only; the outbound item fields are added by this story (see CLAR-003). Design evidence is the local screen specification and prototype, not Figma.
## Test scenarios
| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-007-01 | BR1, BR8 | System | Synthetic INT-15 sample, 120 records | Contract test passes; no client outside the adapter |
| TC-E1-007-02 | AC2, BR2 | System | CCMS file, 4,200 records, trailer 4,201 | REFUSED; DQ-059; no record; stale; MSG-P1-002 |
| TC-E1-007-03 | AC3, BR4–BR6 | System | WIN file, 85 cases; SFTP stub fails 3 times | +5/+15; RETRY_QUEUE; EXCEPTION; task; MSG-P2-001 |
| TC-E1-007-05 | AC5, BR3 | System | Empty SVAF folder | MISSING; stale on 2026-11-10; MSG-P1-001 |
| TC-E1-007-07 | AC7, BR7 | System | Event key sent twice | No action; hit count 2 |
| TC-E1-007-08 | AC8 | System | One due item, two senders | Sent once; attempt count 1 |
| TC-E1-007-09 | AC9 | System | Item EXCEPTION after 3 attempts | PENDING, attempt 0; audit; MSG-GEN-005 |
| TC-E1-007-10 | X9 | Security | RW-CASEOWN calls resend | 403; MSG-P4-002 |
| TC-E1-007-11 | BR2–BR7 | Unit | Each check; retry boundary 2/3; lock; duplicate key | Pass/fail as specified; no off-by-one |
| TC-E1-007-12 | SCR-09 | Unit | Loading, empty, list, 409, success | States render; resend refreshes; no PII |
## Guardrails
- No business value in code: retry counts, intervals, folders, patterns, owners and tolerances are table rows.
- No personal data in logs, tests or prompts; file contents are never logged, only names, counts, hashes and check results.
- Only `SftpTransport` opens a connection; the boundary test fails the build on any other call, and outbound items carry case IDs only.
## Out of scope
- Record-level checks and the stale marker: P1 loaders, RWB-E1-015 and RWB-E1-016.
- Run books and job monitoring: RWB-E1-056.
- Control-M/ADF schedules, SCR-44 and WIN notice content: RWB-E1-051, Epic 2/8 and RWB-E2-021.
## Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No direct call to a system of record | Epic 1 §3.2; Program §5.2 | FEAT-DRI-09, 10, 11 | All recovery processes | None | TC-E1-007-01, 02 |
| REQ-DRI-007 | Log every file, retry, exception queue with an owner task | Epic 1 §3.2; Program §5.2 | FEAT-RDF-21, 23, 24; FEAT-DRI-13 | All recovery processes | R-UNI-33..36, 40 | TC-E1-007-03, 07..09, 11 |
| REQ-DRI-008 | Data moves by COLLINS or a file load | Epic 1 §3.2; Program §5.2 | FEAT-RDF-24; FEAT-DRI-10 | All recovery processes | None | TC-E1-007-05, 11 |
## Clarification Log
| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4, AC3; SPEC-011 | INT-14 has `max_attempts` 3 and intervals 5, 15 and 45; which gaps apply? | Determines attempt times and when EXCEPTION is reached. | Intervals are gaps after a failed attempt: attempt 2 at +5, attempt 3 at +15; the 45 is spare data with max 3. AC3 confirms +5 and +15. | RESOLVED | SPEC-011 |
| CLAR-002 | LOV-INTERFACE-RUN; SPEC-003 | When is run status `FAILED` used, since the ACs only cover RECEIVED/LOADED/REFUSED/MISSING/DUPLICATE? | A status in the list must have a meaning. | `FAILED` is an adapter or loader error after the checks pass; record-level rejection belongs to P1. The previous load stays in use and the data steward is alerted. | RESOLVED | SPEC-003 |
| CLAR-003 | §15; SPEC-017 | SCR-09's specification lists case fields, not outbound item fields. | The UI delta must be defined. | The story adds interface, attempt count, last error, case count and resend to SCR-09; the screen specification is updated by this story. | RESOLVED | SPEC-017 |
| CLAR-004 | §15; SPEC-017 | The frontend context says SCR-09 is first in E2; the screen inventory and the story say E1. | Determines whether the UI is in this release. | The screen inventory and the story are authoritative: SCR-09 is E1 for this list and action; the wider queue screens remain E2. | RESOLVED | SPEC-017 |
| CLAR-005 | §12; SPEC-015 | `If-Match` is required by the story but not declared in the OpenAPI file. | A contract delta is needed. | Add the required `If-Match` header to the resend operation in `api/recovery-api.yaml`; a missing or stale value returns 409 MSG-GEN-004. | RESOLVED | SPEC-015 |
| CLAR-006 | ACK; SPEC-010 | How is `ACKNOWLEDGED` set? | The status is in the LOV but no AC exercises it. | RWB-E1-055 owns the WIN acknowledgment content; the item is matched by interface and business date (its idempotency key) and moves SENT → ACKNOWLEDGED. A SENT item without acknowledgment after 30 minutes is resent. | RESOLVED | SPEC-010 |
| CLAR-007 | §12; SPEC-016 | `caseCount` is not a column in `outbound_item`. | The API field needs a source. | It is the size of `case_ids`; no new column. | RESOLVED | SPEC-016 |
| CLAR-008 | §12; SPEC-003 | The file hash algorithm is not named. | The column is `char(64)`. | SHA-256, hex-encoded, 64 characters; recorded on the run row. | RESOLVED | SPEC-003 |

`CLARIFICATION_STATUS: RESOLVED` — all eight items are answered from the story, the API specification, the screen inventory or RWB-E1-055. No item changes the business outcome.
## Status reporting
```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP source; design evidence is the local screen specification and prototype.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New inbound and outbound file adapters, retry and exception queue, two E1 admin endpoints and the SCR-09 outbound list.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new adapter capability, two new endpoints and a screen delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 8 acceptance criteria, 9 exception paths and 10 state transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
