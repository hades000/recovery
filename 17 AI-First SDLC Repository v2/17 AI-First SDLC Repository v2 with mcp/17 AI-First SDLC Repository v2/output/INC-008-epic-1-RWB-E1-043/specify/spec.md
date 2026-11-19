> **HISTORICAL — do not build from this file.** This run was written on 10 November 2026 under
> D-RCV-47 (schema `ace`, `rwb_` prefix). Document set v14 (16 November 2026) reinstates schema
> `recovery` and `${recoverySchema}` through D-RCV-35 and ADR-010. Re-run the spec and plan before
> build (`OPEN-036`). The implementation evidence for the two current stories is in
> `output/INC-003-...` and `output/INC-002-...`.

# Technical Specification — RWB-E1-043 Reference data service with versioned tables

| Field | Value |
|---|---|
| Story | RWB-E1-043 — Reference data service with versioned tables |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-009-epic-1-RWB-E1-043` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-012, FR-RWB-020); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 043 Reference data service with versioned tables v1.md` |
| Upstream IDs | BRD-RWB-004, BRD-RWB-020; FR-RWB-012, FR-RWB-020; REQ-DRI-011, REQ-CWC-006; US-RWB-E1-043; CTX-FEATURE-003; CTL-08; R-UNI-38; DF-REF-159..184 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. SCR-40 is Epic 8; the administrator loads by file and reads the response. |
| Logic In Scope | `YES` — versioning, load checks, approval, effective dating, cache, read logging and no-version handling. |
| API In Scope | `YES` — this story first delivers `POST /admin/reference-loads`, `POST /admin/reference-loads/{loadId}/approve` and `GET /admin/lists/{listCode}` (P4). The contract is already in API Specification v2; no OpenAPI delta. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | P4 load and approval handler; case service, allocation engine and timer engine start-up hooks; `lov_value` read interface. |
| New Nodes Required | `YES` — `ReferenceVersionRegistryImpl`, `ReferenceDataServiceImpl`, `ReferenceRowCache`, `ReferenceTableSchemas`, `ReferenceVersionRepository`, `ReferenceRowRepository`, `ReferenceVersionLogger`, `reference_version`, `reference_row`. |
| Inherited Existing Behavior | RWB-E1-044 migrations; RWB-E1-042 configuration service and `refdata.cache.ttl-seconds`; P4 access check; ACE business date from JOB-01. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The served tables are PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD, HOLIDAY and PRODUCT_PARAMETER; the list is data. | SPEC-RWB-E1-043-002 | DIRECT | Table codes read from LOV-REF-TABLE; no table name in code. | COVERED |
| BR2 | Each load creates one version, numbered one above the highest for the table; a version is never changed after it is written. | SPEC-RWB-E1-043-001, SPEC-RWB-E1-043-004 | DIRECT | `UNIQUE (table_code, version_no)`; append-only trigger. | COVERED |
| BR3 | The version in force on a business date is the approved version with the latest valid from on or before that date. | SPEC-RWB-E1-043-006 | DIRECT | Date resolution; no clock read inside the service. | COVERED |
| BR4 | A version takes effect only after an approver who is not the author approves it. | SPEC-RWB-E1-043-005 | DIRECT | Approver present, different, holds Reference data A. | COVERED |
| BR5 | A load with any failed check is refused in full. | SPEC-RWB-E1-043-003 | DIRECT | One transaction; no version and no rows on failure. | COVERED |
| BR6 | A valid from before the current business date is refused; open cases keep the version they were decided under. | SPEC-RWB-E1-043-003, SPEC-RWB-E1-043-006 | DIRECT | Equal to the business date is allowed; earlier is refused. | COVERED |
| BR7 | Every engine logs the table code and version of every table it reads. | SPEC-RWB-E1-043-008 | DIRECT | `ReferenceVersionLogger`, one line per table; no row content. | COVERED |
| BR8 | Approving a new version sets the valid to of the version it replaces to the day before the new valid from. | SPEC-RWB-E1-043-007 | DIRECT | Same transaction as approval. | COVERED |
| BR9 | An engine that finds no version in force does not run on stale or missing values. | SPEC-RWB-E1-043-009 | DIRECT | `NoVersionInForceException`; alert; no run. | COVERED |
| AC1 | Version 4 with 5 rows is approved; version 3 stays readable with 4 rows and valid to 2026-11-30; version 3 served for 30 Nov, version 4 for 1 Dec. | SPEC-RWB-E1-043-004, SPEC-RWB-E1-043-006, SPEC-RWB-E1-043-007 | DIRECT | EXPOSURE_BAND fixture. | COVERED |
| AC2 | The author cannot approve; version stays VALIDATED; the previous version is still served. | SPEC-RWB-E1-043-005 | DIRECT | MSG-P7-002. | COVERED |
| AC3 | Each engine reads every table through the service and logs table code, version and business date; no party identifier. | SPEC-RWB-E1-043-008 | DIRECT | QUEUE v7, SERVICE_LEVEL v2, HOLIDAY v1. | COVERED |
| AC4 | A row with text in `limit_days` is refused naming row 12 and column; no version is written. | SPEC-RWB-E1-043-003 | DIRECT | MSG-P3-027. | COVERED |
| AC5 | An unapproved version is never served; the previous version remains in force. | SPEC-RWB-E1-043-005, SPEC-RWB-E1-043-006 | DIRECT | HOLIDAY v2 stays VALIDATED. | COVERED |
| AC6 | A valid from before the business date is refused and no version is written. | SPEC-RWB-E1-043-003 | DIRECT | LEGAL_PERIOD 2026-11-24 against business date 2026-11-25. | COVERED |
| AC7 | The same file with the same valid from returns version 5 and creates no version 6. | SPEC-RWB-E1-043-004 | DIRECT | Idempotency on table, valid from and content hash. | COVERED |
| AC8 | Two simultaneous approvals record one approval and refuse the other. | SPEC-RWB-E1-043-010 | DIRECT | Optimistic lock; MSG-GEN-004. | COVERED |
| AC9 | With no approved TEAM version, the allocation engine does not start and an alert names TEAM and the date. | SPEC-RWB-E1-043-009 | DIRECT | MSG-P3-027. | COVERED |
| AC10 | A header-only DOCUMENT_TYPE file is refused and no version is written. | SPEC-RWB-E1-043-003 | DIRECT | MSG-GEN-001 names `rows`. | COVERED |
| X1..X7 | Exceptional paths in the table below map to SPEC-003..010. | SPEC-RWB-E1-043-003..010 | DIRECT | Author approval, schema/key, past valid from, duplicate load, concurrent approval, no version, empty file. | COVERED |

## User story intent interpretation

As a **reference data administrator (RW-REFADM)**, I want **products, regions, exposure bands, roles, teams, queues, service levels, document types, templates, delegation of authority, legal periods and holidays held as versioned reference data with valid from, valid to, author and approver**, so that **business values change by a data release and not by code, and every engine can say which version it used**.

The story is the reference-data backbone for the module. It does not change a case status; it makes every value an engine reads dated, approved and attributable, and gives each read a table code and version in the log so a decision can be reproduced.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `POST /admin/reference-loads` for a table code and valid from; `POST /admin/reference-loads/{loadId}/approve`; engine start or cache expiry for a read. |
| Preconditions | RWB-E1-044 done; RWB-E1-042 serves `refdata.cache.ttl-seconds` (300 assumed; DL11) and the table-code list; LOV-REF-TABLE holds the 13 codes; the P4 load endpoint calls the published interface; loader holds RW-REFADM; approver holds the approve right; the ACE business date is set from JOB-01. |
| Input | CSV or XLSX with one sheet, table code, valid from, caller identity, business date. |
| Output | `reference_version` and `reference_row` rows; approved versions; `VersionedRows`; one log line per table read; load response. |
| Feature flag | `rwb.p3.refdata-versions`. Off: engines read the values loaded before this story. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `reference_version` | `table_code` | Load request | New row only | Must be in LOV-REF-TABLE. |
| `reference_version` | `version_no` | Service | System-managed | One above the highest for the table; unique (table_code, version_no). |
| `reference_version` | `valid_from`, `valid_to` | Load request / approval | New row; `valid_to` set on approval | Valid from not before the business date; valid to is the day before the next valid from. |
| `reference_version` | `status` | Service | VALIDATED → APPROVED → ROLLED_BACK | Never edited to any other value. |
| `reference_version` | `author_user_id`, `approver_user_id`, `approved_at` | Session / approval | System-managed | Approver must differ from author. |
| `reference_version` | `row_count`, `content_hash`, `load_id` | Service | System-managed | Hash is SHA-256 over rows sorted by key; unique (table_code, valid_from, content_hash). |
| `reference_row` | `row_key`, `row_data` | Load file | New row only | Unique (version_id, row_key); append-only. |
| `reference_row` | all fields | — | Never updated | Update trigger refuses changes; a correction is a new version. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Load | Every check passes | VALIDATED | Version and rows written; not served. |
| None | Load | Any check fails | Not written | Load refused in full; previous version stays. |
| VALIDATED | Approve | Approver present, not author, holds the right | APPROVED | Approver and time recorded; replaced version's `valid_to` set. |
| APPROVED | Valid from reached | Date reached | In force (derived) | Reads for that date return this version. |
| APPROVED | Rollback | A later version is rolled back | ROLLED_BACK | Previous version in force again. |

This story changes no case status. "In force" is derived from status and date, not a stored status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Approval with no approver or by the author | Version stays VALIDATED; never served | MSG-P7-002 |
| X2 | Row fails the schema or key check | Load refused in full; no version or rows | MSG-P3-027 |
| X3 | Valid from before the business date | Load refused in full | MSG-P3-027 |
| X4 | Same file loaded twice for the same table and valid from | First load returned; no second version | None |
| X5 | Two approvals of the same load at once | One succeeds; the other refused | MSG-GEN-004 |
| X6 | No approved version in force for a table | Engine does not start; alert names table and date | MSG-P3-027 |
| X7 | Empty load file | Load refused in full | MSG-GEN-001 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| Endpoints delivered | `POST /api/recovery/v1/admin/reference-loads`; `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve`; `GET /api/recovery/v1/admin/lists/{listCode}`. |
| Contract delta | None against API Specification v2. `ReferenceLoad` already carries id, table, validFrom, status and rows; approval returns the same shape; the list endpoint returns `ListOfValues` with versions. |
| Backward compatibility | Additive; no existing endpoint changes. |
| Authorization | Reference data C to load; A to approve; R to read lists. 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P3-027/MSG-P7-002/MSG-GEN-004; 422 MSG-P3-027/MSG-GEN-001; 503. |
| Versioning | No API version change; the OpenAPI file is unchanged. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; SCR-40 is Epic 8. | Existing frontend tests remain green. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-012, FR-RWB-020; SPEC-RWB-E1-043-001..014 | New registry, read service, cache, schema checks, repositories and logger. | Positive, negative, boundary and error-path tests: load, approve, author refusal, past date, empty file, schema error, duplicate, concurrent approval, version resolution, no version, rollback. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ReferenceVersionRegistryImpl` | Service | Runs load checks, numbers the version, writes version and rows, approves. |
| `ReferenceDataServiceImpl` | Service | Resolves the version in force for a date and serves rows from the cache. |
| `ReferenceRowCache` | Service | In-memory cache keyed by table code and business date; TTL from `refdata.cache.ttl-seconds`. |
| `ReferenceTableSchemas` | Rule table | Column names, types and key columns per table code, held as catalog entries (RWB-E1-042). |
| `ReferenceVersionRepository` / `ReferenceRowRepository` | Repository | Read and write `reference_version` and `reference_row`. |
| `ReferenceVersionLogger` | Service | One log line per table read: table code, version, business date. |
| `ReferenceVersionRegistry` / `ReferenceDataService` | Published interface | The interfaces in the story contract. |

### Package and boundaries

`recovery.casewf.refdata` holds the implementation; published types in `recovery.casewf.refdata.api`.
P4 reaches the registry only through `ReferenceVersionRegistry`; other modules read only through
`ReferenceDataService`. No module reads `reference_version` or `reference_row` directly. `lov_value`
is read through the P4 interface.

### Data and migration

`V<next>__rwb_e1_043_reference_versions.sql` creates:

- `reference_version`: id uuid PK, table_code varchar(30), version_no integer, valid_from date,
  valid_to date, status varchar(15), author_user_id uuid, approver_user_id uuid, approved_at
  timestamptz, row_count integer, content_hash char(64), load_id uuid, standard columns;
  `UNIQUE (table_code, version_no)`, `UNIQUE (table_code, valid_from, content_hash)`,
  `CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id)`, partial unique index on
  `(table_code, valid_from) WHERE status = 'APPROVED'`.
- `reference_row`: id uuid PK, version_id uuid FK, row_key varchar(200), row_data jsonb, standard
  columns; `UNIQUE (version_id, row_key)`; index on version_id.
- Append-only triggers refuse changes to `reference_row`, and to `reference_version` except status,
  approver, approved_at, valid_to and the standard columns.

### Load checks

1. Table code in LOV-REF-TABLE.
2. File has at least one data row.
3. Every row matches the column schema for the table code: name, type, required, list.
4. Row keys are present and unique within the file.
5. Valid from is not before the business date.
6. Author is present.
7. Content hash (SHA-256 over rows sorted by key) and next version number.

Any failure refuses the load whole. A repeat with the same table, valid from and hash returns the
existing load.

### Approval and version resolution

- Approval requires an approver, different from the author, holding Reference data A.
- The optimistic `version` column prevents two approvers from both succeeding; the second receives
  MSG-GEN-004.
- Approval sets the replaced version's `valid_to` to the day before the new `valid_from`.
- `rows(tableCode, businessDate)` returns the approved version with the latest `valid_from` on or
  before the business date. If none exists it throws `NoVersionInForceException`.

### Cache and logging

- Cache key is table code plus business date; TTL from `refdata.cache.ttl-seconds`.
- The cache never serves a version that is not APPROVED.
- Each engine calls `ReferenceVersionLogger` once per table read; the line carries table code, version
  and business date only. No party identifier, row content or personal data.

### Transaction and events

The load writes the version and all rows in one transaction. Approval writes status, approver and the
replaced version's `valid_to` in one transaction. No event is published; engines refresh on start and
on cache expiry.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-REFADM | Reference data CRUD | All |
| RW-COE | Reference data C for tables it owns | All |
| RW-RISK | Reference data A (assumed; DL01) | All |
| SY-CASEWF | Reference data R | All |
| SY-RULES | Reference data R | All |
| RW-AUDIT | Reference data R | All |

The same person may not hold RW-REFADM and RW-RISK. Approval of DELEGATION_LIMIT follows `doa.txt`
rule 11: a data load approved by Risk.

### Observability and operations

- Load response: status, row count, each failed row and column.
- Daily data quality report lists load results (RWB-E1-011).
- Metrics: loads, refusals by check, approvals, rollbacks, cache hit rate, no-version alerts.
- Alert: no version in force names table and business date; the engine does not run.

### Performance

- Reads are cached; a miss is one indexed query plus row fetch.
- The 13 tables are small; the cache holds one version per table and date.
- Approval is a single row update with an optimistic lock.

### Feature flag and rollback

- `rwb.p3.refdata-versions`: off means engines read the values loaded before this story.
- Rollback: turn the flag off; redeploy the previous tag. A version rollback is a data action through
  the rollback endpoint, not a deployment.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-043-01 | AC1, BR2, BR3, BR8 | System | EXPOSURE_BAND v3/v4; 30 Nov and 1 Dec | v3 served on 30 Nov; v4 on 1 Dec; v3 valid to 30 Nov |
| TC-E1-043-02 | AC2, BR4 | System | DELEGATION_LIMIT 24 rows; author approves | Refused; v stays VALIDATED; previous served |
| TC-E1-043-03 | AC3, BR7 | System | QUEUE v7, SERVICE_LEVEL v2, HOLIDAY v1 | One log line per table; no party ID |
| TC-E1-043-04 | AC4, BR5 | System | SERVICE_LEVEL row 12 text in `limit_days` | Refused; row 12 and column named |
| TC-E1-043-05 | AC5, BR3, BR4 | System | HOLIDAY v2 unapproved | v1 served; v2 VALIDATED |
| TC-E1-043-06 | AC6, BR6 | System | LEGAL_PERIOD valid from 2026-11-24 | Refused; no version |
| TC-E1-043-07 | AC7, BR2 | System | REGION file twice, same hash | v5 returned; no v6 |
| TC-E1-043-08 | AC8 | System | Two parallel approvals of QUEUE v8 | One approval; other MSG-GEN-004 |
| TC-E1-043-09 | AC9, BR9 | System | TEAM with no approved version | Engine does not start; alert names TEAM |
| TC-E1-043-10 | AC10, BR5 | System | DOCUMENT_TYPE header only | Refused; MSG-GEN-001 |
| TC-E1-043-11 | Authority | Security | RW-CASEOWN calls the load endpoint | 403; MSG-P4-002 |
| TC-E1-043-12 | BR1 | Unit | Unknown table code | Refused; no version |

## Guardrails and out of scope

- No business value in code. Table codes, columns, bands, periods and limits are rows; the code holds
  only the versioning behaviour.
- No personal data in logs, tests or prompts. Log lines carry table codes and version numbers only.
- `lov_value` is read through the P4 interface; P4 reaches the registry only through
  `ReferenceVersionRegistry`.
- Out of scope: rule-table load, validation and rollback (RWB-E1-029); permission and masking tables
  (RWB-E1-037); delegation content (RWB-E1-038); checklist fields and audit report (RWB-E1-048);
  product completeness checks (RWB-E1-045); screens SCR-39/40/42 (Epic 8).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4; SPEC-005 | No role holds Reference data A in the permission matrix. Who approves? | Approval cannot be implemented without an approver role. | Assume RW-RISK holds it (DL01); the permission matrix change is loaded through RWB-E1-037, holders by DL18. | RESOLVED | SPEC-005 |
| CLAR-002 | BR1; SPEC-002 | Are 13 table codes final when RWB-E1-019 adds QUEUE_MEMBER? | The list must accept a new code without code change. | Yes: 13 for this story; E1-019 adds QUEUE_MEMBER to LOV-REF-TABLE by a list load. | RESOLVED | SPEC-002 |
| CLAR-003 | §13; SPEC-003 | Where do table column definitions live? | The row check needs a schema per table. | As catalog entries under RWB-E1-042, owned by RW-REFADM; the exact `kind` value is an implementation choice. | RESOLVED | SPEC-003 |
| CLAR-004 | BR6, AC6; SPEC-003 | Is a valid from equal to the business date allowed? | Boundary behaviour. | Yes; only a date before the business date is refused. | RESOLVED | SPEC-003 |
| CLAR-005 | AC7; SPEC-004 | What if the same valid from carries different content? | Idempotency vs conflict. | Same hash returns the existing load; different content at an already-approved valid from is refused with 409 MSG-P3-027. | RESOLVED | SPEC-004 |
| CLAR-006 | §9; SPEC-006 | Is IN_FORCE a stored status? | The status list includes it. | No; status stays APPROVED and "in force" is derived from the date. | RESOLVED | SPEC-006 |
| CLAR-007 | BR7; SPEC-008 | Is a log line written per read or per table per start? | Log volume. | One line per table per engine start or cache refresh, not per row. | RESOLVED | SPEC-008 |
| CLAR-008 | §9; SPEC-014 | Is reference rollback the same call as rule rollback? | Endpoint reuse. | Yes; `POST /admin/reference-loads/{loadId}/rollback` with a reason, as recorded with RWB-E1-019. | RESOLVED | SPEC-014 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the permission matrix or
the API specification. The approver grant is an accepted assumption with an owner, not open behaviour.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend reference-data story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New versioned reference-data service; three P4 endpoints delivered from the existing v2 contract; no screen.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: first delivery of the reference-load, approve and list endpoints with no OpenAPI delta]
REQUIREMENT_COVERAGE_SUMMARY: All 9 business rules, 10 acceptance criteria, 7 exception paths and 4 version states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
