# Technical Specification — RWB-E1-025 Document types and fields agreed

| Field | Value |
|---|---|
| Story | RWB-E1-025 — Document types and fields agreed |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-036-epic-1-RWB-E1-025` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-015); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 025 Document types and fields agreed v1.md`; FSD P5 A2.3; TSD P5 T3.1 |
| Upstream IDs | BRD-RWB-005; FR-RWB-015; REQ-DCM-004; US-RWB-E1-025; CTX-FEATURE-005; DL01, DL19, DL26; R-UNI-38; CTL-08 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Center of excellence analyst and legal counsel (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. SCR-40 Reference data is Epic 8; until then the table is loaded by file and read through the endpoint response. |
| Logic In Scope | `YES` — row validation, refuse-whole load, version staging, separation-of-duty approval and version-in-force resolution. |
| API In Scope | `NO` — no new or changed endpoint. The story adds the table code `DOCUMENT_TYPE` to the existing P4 `POST /admin/reference-loads` and uses `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | P4 reference-load service and `ReferenceTableLoader` contract; `reference_version` and `reference_row`; `document` store (RWB-E1-024), classification (RWB-E1-050) and extraction (RWB-E1-053) readers. |
| New Nodes Required | `YES` — `DocumentTypeLoader`, `DocumentTypeCatalog`, `DocumentTypeCatalogService`, `DocumentTypeRepository`, `DocumentTypeEntity`, `document_type` table. |
| Inherited Existing Behavior | Reference data load and approval (P4); reference version registry (RWB-E1-043); LOV service for `LOV-RETENTION`; local tracker list (RWB-E1-012). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The document types and their fields are signed by Legal and NPA before extraction is built. | SPEC-RWB-E1-025-002, SPEC-RWB-E1-025-003 | DIRECT | Every row carries `legal_signoff_by/date` and `npa_signoff_by/date`. | COVERED |
| BR2 | Each type row carries the write-once flag, the retention class and the field list. | SPEC-RWB-E1-025-001, SPEC-RWB-E1-025-002 | DIRECT | Columns from TSD T3.1; `field_definitions` is jsonb. | COVERED |
| BR3 | A load with any invalid row is refused in full. | SPEC-RWB-E1-025-004 | DIRECT | Validate all rows before writing; no partial load. | COVERED |
| BR4 | A version takes effect on its valid from date; work already done keeps the version it used. | SPEC-RWB-E1-025-007, SPEC-RWB-E1-025-015 | DIRECT | `valid_from`/`valid_to`; the document row records the type table version used. | COVERED |
| BR5 | The person who loads a version does not approve it. | SPEC-RWB-E1-025-006 | DIRECT | Compare loader and approver user IDs; 409 MSG-P7-002. | COVERED |
| BR6 | Retention class codes come from `LOV-RETENTION`. | SPEC-RWB-E1-025-004 | DIRECT | Read through the P4 list service; `KEEP99` is refused. | COVERED |
| BR7 | The six proposed types apply until the bank provides its own list. | SPEC-RWB-E1-025-002 | DIRECT | Six types and 26 fields as data (assumed; DL19). | COVERED |
| AC1 | A valid file loads as `LOADED` with 6 rows, each holding both sign-off user IDs and both dates. | SPEC-RWB-E1-025-003, SPEC-RWB-E1-025-009 | DIRECT | No row in force until approval. | COVERED |
| AC2 | Approval puts `DOCTYPE-2026.11` in force from 30 November 2026 with the six codes; `COURT_NOTICE` has 4 fields, `LEGAL10Y`, write-once true; `APPRAISAL_REPORT` has `GENERAL05Y`, write-once false, 4 fields. | SPEC-RWB-E1-025-002, SPEC-RWB-E1-025-007 | DIRECT | Read through `DocumentTypeCatalog`. | COVERED |
| AC3 | A load with a missing NPA sign-off is refused whole, naming row 6 and the error; no row is written; the version in force is unchanged. | SPEC-RWB-E1-025-003, SPEC-RWB-E1-025-004 | DIRECT | MSG-P3-027 names the row and the error. | COVERED |
| AC4 | A load with `KEEP99` and a repeated `COURT_NOTICE` row is refused whole, listing both rows. | SPEC-RWB-E1-025-004 | DIRECT | All row errors are returned, not only the first. | COVERED |
| AC5 | Loading `DOCTYPE-2026.11` twice is refused with 409 naming "version already loaded"; the first load is unchanged. | SPEC-RWB-E1-025-005 | DIRECT | Unique (table code, table version) at the load service. | COVERED |
| AC6 | A version approved with valid from 1 January 2027 is read on 1 January 2027; the 31 December 2026 read returns the previous version. | SPEC-RWB-E1-025-007, SPEC-RWB-E1-025-015 | DIRECT | Boundary date test; open work keeps the version it used. | COVERED |
| AC7 | The loader who holds Reference data A cannot approve their own load; 409; the load stays `LOADED`. | SPEC-RWB-E1-025-006 | DIRECT | Separation of duty check before status change. | COVERED |
| X1 | A row has no Legal or NPA sign-off, or a sign-off without a date. | SPEC-RWB-E1-025-003, SPEC-RWB-E1-025-004 | DIRECT | Refused whole; MSG-P3-027. | COVERED |
| X2 | A retention class outside `LOV-RETENTION`, or a repeated type code. | SPEC-RWB-E1-025-004 | DIRECT | Refused whole; both rows listed. | COVERED |
| X3 | The same table version is loaded twice. | SPEC-RWB-E1-025-005 | DIRECT | 409; first load kept. | COVERED |
| X4 | A new version has a future valid from date. | SPEC-RWB-E1-025-007, SPEC-RWB-E1-025-015 | DIRECT | Current version stays in force until that date. | COVERED |
| X5 | The loader tries to approve their own load. | SPEC-RWB-E1-025-006 | DIRECT | 409 MSG-P7-002; status stays `LOADED`. | COVERED |
| X6 | A role without Reference data C uploads the file. | SPEC-RWB-E1-025-011 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **the first six document types (demand letter, court notice, appraisal report, title deed, settlement agreement, guarantor notice) with their key fields agreed with Legal and NPA and held as versioned reference data**, so that **the OCR pipeline, classification and extraction have one signed target list**.

The story turns the agreed list into a versioned table. It adds the loader that validates a whole file, the approval step that puts a version in force, and the read interface that the store, classification and extraction use. It adds no screen: the reference data administrator loads by file through the P4 endpoint, and the center of excellence analyst reads the version in force. The six types and 26 fields are the proposed list under DL19 until the bank signs its own.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Reference data administrator uploads a load file for table `DOCUMENT_TYPE`; an approver approves the staged load. |
| Preconditions | RWB-E1-012 done; `LOV-RETENTION` holds `LEGAL10Y` and `GENERAL05Y` (assumed; DL26); the loader holds RW-REFADM (Reference data C); the approver holds Reference data A; P4 `POST /admin/reference-loads` calls the P5 loader; `rwb.dochub.doctypes` flag on. |
| Input | Excel load file `DOCTYPE-2026.11` with six type rows and 26 field definitions; `validFrom` 2026-11-30; both sign-offs per row. |
| Output | `document_type` rows staged as `LOADED`; approved version in force from `valid_from`; `DocumentTypeCatalog` result. |
| Feature flag | `rwb.dochub.doctypes`. Off: the table code `DOCUMENT_TYPE` is refused by the reference-load endpoint. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document_type` | `doc_type_code` | Load file | New version only | Unique within the version; one of the six codes until DL19 changes |
| `document_type` | `label_en`, `label_th` | Load file | New version only | `label_en` required; `label_th` optional |
| `document_type` | `write_once` | Load file | New version only | Required; true for every type except `APPRAISAL_REPORT` in the proposed list |
| `document_type` | `retention_class` | Load file | New version only | Must exist in `LOV-RETENTION` |
| `document_type` | `field_definitions` | Load file | New version only | At least one field; jsonb array with name, label, type and personal flag |
| `document_type` | `legal_signoff_by`, `legal_signoff_date` | Load file | New version only | Both required on every row |
| `document_type` | `npa_signoff_by`, `npa_signoff_date` | Load file | New version only | Both required on every row |
| `document_type` | `table_version` | Load file | New version only | `DOCTYPE-YYYY.NN`; unique across loads |
| `document_type` | `valid_from`, `valid_to` | Load file / approval | System writes `valid_to` on supersession | `valid_to` is the day before the next version's `valid_from` |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Load file received | Every row passes validation | `LOADED` | Six rows written; not in force |
| None | Load file received | Any row fails validation | `REFUSED` | No row written; all row errors returned; version in force unchanged |
| `LOADED` | Approve | Approver is not the loader | `APPROVED` | In force from `valid_from`; previous version gets `valid_to` |
| `LOADED` | Approve | Approver is the loader | `LOADED` | 409 MSG-P7-002; no change |
| `APPROVED` | Next version takes effect | Its `valid_from` date is reached | Superseded | `valid_to` set to the day before; readers return the new version from its date |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Missing Legal or NPA sign-off, or a sign-off date absent | Load refused whole; row and error named | MSG-P3-027 |
| X2 | Retention class not in `LOV-RETENTION`, or duplicate type code | Load refused whole; every bad row listed | MSG-P3-027 |
| X3 | Same table version loaded twice | 409; first load kept | MSG-P3-027 |
| X4 | Future `valid_from` | Current version stays in force until that date; open work keeps the version it used | None |
| X5 | Loader approves their own load | 409; load stays `LOADED` | MSG-P7-002 |
| X6 | Role without Reference data C | 403; nothing written | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /admin/reference-loads` (P4; table `DOCUMENT_TYPE`); `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve`; `GET /api/recovery/v1/admin/lists/{listCode}` for `LOV-DOC-TYPE`. |
| Contract delta | None. The table code is a request value; the load and approval responses already carry status, table, version, rows and row errors. |
| Backward compatibility | Unchanged. |
| Authorization | Reference data C to load; Reference data A to approve; 401, 403 MSG-P4-002, 409 MSG-P3-027/MSG-P7-002, 422 MSG-P3-027, 503 MSG-GEN-006. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label changes; SCR-40 is Epic 8. | Existing frontend tests remain green; no new frontend test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-004; SPEC-RWB-E1-025-001..015 | New table, loader, catalog service and repository. | Valid six-row load; missing sign-off; invalid retention class; duplicate code; duplicate version; self-approval; boundary date 31 Dec / 1 Jan; access refusal. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `DocumentTypeLoader` | Service | Implements `ReferenceTableLoader` for `DOCUMENT_TYPE`: parse, validate, stage and approve. |
| `DocumentTypeCatalog` | Published interface | `inForce(businessDate)` and `type(docTypeCode, businessDate)`; used by RWB-E1-024, RWB-E1-050 and RWB-E1-053. |
| `DocumentTypeCatalogService` | Service | Implements the catalog with a 5-minute cache cleared on approval. |
| `DocumentTypeRepository` | Repository | Reads and writes `document_type` only. |
| `DocumentTypeEntity` | Entity | Maps `document_type`, including `field_definitions` jsonb. |
| `document_type` rows | Rule table | Six types and 26 field definitions as data. |

### Package and boundaries

Folder `recovery/dochub/types`, Java package `recovery.dochub.types`. The loader implements the P4
`ReferenceTableLoader` contract; the catalog is the only read path for other P5 packages. `LOV-RETENTION`
is read through the P4 list service, never from a P5 table.

### Data and migration

Flyway `V1_5_025__document_type.sql` creates `document_type`: `id`, `doc_type_code varchar(30)`,
`label_en varchar(120)`, `label_th varchar(120)`, `write_once boolean`, `retention_class varchar(10)`,
`field_definitions jsonb`, `legal_signoff_by uuid`, `legal_signoff_date date`, `npa_signoff_by uuid`,
`npa_signoff_date date`, `table_version varchar(20)`, `valid_from date`, `valid_to date`, `load_id uuid`
and the standard columns. Constraints: unique (`doc_type_code`, `table_version`); not null on both
sign-off user and date pairs. Index `ix_document_type_valid` on (`valid_from`, `valid_to`).

### Validation

1. Type code unique within the file and not repeated.
2. `label_en` present; `write_once` present.
3. `retention_class` exists in `LOV-RETENTION` in force.
4. At least one field definition; each field has a name, a label and a type.
5. Both sign-offs present: user ID and date for Legal and for NPA.
6. Any failure refuses the load whole; all row errors are returned, not only the first.

### Version in force

`inForce(businessDate)` returns the approved version whose `valid_from <= businessDate` and whose
`valid_to` is null or later than `businessDate`. Approval sets the previous version's `valid_to` to the
day before the new `valid_from`. A future version is not returned before its date. A document keeps the
type table version it used when it was stored; later versions do not rewrite it.

### Approval and separation of duty

The approver must hold Reference data A and must not be the loader (`load_id` creator). The check runs
before the status change. A self-approval returns 409 MSG-P7-002 and leaves the load `LOADED`. Approval
clears the catalog cache.

### Transaction and events

The load writes the `reference_version` and all six rows in one transaction; a validation failure writes
no row. Approval updates the version status and the previous version's `valid_to` in one transaction. No
domain event is published; the load and approval are recorded in the reference data audit.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-COE Center of excellence analyst | Reference data R; prepares and reads the list | All |
| RW-LEGAL Legal counsel | Signs for Legal | All |
| RW-HEADNPA Head of NPA | Signs for NPA | All |
| RW-REFADM Reference data administrator | Reference data C; loads the file | All |
| Approver with Reference data A | Approves; assumed granted to the legal counsel table owner (DL01) | All |
| SY-OCR, SY-RULES | Read the version in force | All |

### Observability and operations

- Load response: status, table version, row count and every row error with its row number.
- Audit: loader, approver, table version, valid from and row count.
- Metrics: loads, refusals by check, approval latency, cache hit rate.
- Alert: a load refused in SIT or PROD; a version approved with no sign-off (should be impossible).

### Performance

- Six rows per version; validation is in memory before the write.
- The catalog is cached for 5 minutes and cleared on approval; a read is one indexed query on a cache
  miss.
- No effect on document write latency.

### Feature flag and rollback

- `rwb.dochub.doctypes`. Off: the table code `DOCUMENT_TYPE` is refused by the reference-load endpoint.
- Rollback: turn the flag off; the version in force stays readable. A data rollback is a new approved
  version, never an edit of a loaded version.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-025-01 | AC1, BR1 | System | `DOCTYPE-2026.11`, six types, 26 fields, both sign-offs | `LOADED` with 6 rows; sign-offs present |
| TC-E1-025-02 | AC2, BR2, BR6 | System | Approved load; read `COURT_NOTICE` and `APPRAISAL_REPORT` | Six codes; `COURT_NOTICE` 4 fields, `LEGAL10Y`, write-once; `APPRAISAL_REPORT` `GENERAL05Y`, not write-once |
| TC-E1-025-03 | AC3, BR1, BR3 | System | `GUARANTOR_NOTICE` row without NPA sign-off | Refused whole; row 6 and "NPA sign-off missing"; version unchanged |
| TC-E1-025-04 | AC4, BR3 | System | `KEEP99` and repeated `COURT_NOTICE` | Refused whole; both rows listed |
| TC-E1-025-05 | AC5 | System | Same version loaded twice | 409 "version already loaded"; first load unchanged |
| TC-E1-025-06 | AC6, BR4 | System | `DOCTYPE-2027.01` valid from 1 January 2027 | 31 Dec read returns 2026.11; 1 Jan returns 2027.01 with `court_region` |
| TC-E1-025-07 | AC7, BR5 | System | Loader approves own load | 409 MSG-P7-002; load stays `LOADED` |
| TC-E1-025-08 | X6 | Security | RW-CASEOWN uploads the file | 403 MSG-P4-002 |
| TC-E1-025-U1 | BR3, BR4, AC3, AC6 | Unit | Rows with missing sign-off, `KEEP99`, duplicate code, and a version on the boundary date | Refuse-whole with every row error; boundary read returns the correct version |

## Guardrails

- No business value in code: type codes, fields, write-once flags and retention classes are rows in
  `document_type`.
- No personal data in logs, tests or prompts. Sign-off users in tests are synthetic IDs.
- No read of another module's tables: `LOV-RETENTION` is read through the P4 list service.
- A refused load writes no row and leaves the version in force unchanged.

## Out of scope

- The retention periods behind each class (RWB-E1-041; DL26).
- The checklist of required types per case type (RWB-E1-040).
- Stage 2 and 3 document types (RWB-E2-025).
- The reference data screen SCR-40 (Epic 8).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-004 | Document types and key fields agreed and signed before extraction is built | Business Requirements Epic 1, section 3.5 | FEAT-DCM-03 | 13 Manage documents and correspondence | R-UNI-38 | TC-E1-025-01..08 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR7; SPEC-002 | Are the six types and 26 fields the final bank list? | Determines the seed data. | The six types and 26 fields are the proposed list under DL19 until the bank provides its own; they are data, not code. | RESOLVED | SPEC-002 |
| CLAR-002 | BR6; SPEC-004 | Are `LEGAL10Y` and `GENERAL05Y` the approved retention classes? | Validation of the load. | Assumed until the bank retention schedule arrives (DL26); loaded in `LOV-RETENTION` by the data steward. | RESOLVED | SPEC-004 |
| CLAR-003 | BR5; SPEC-006 | Who holds Reference data A? | Determines who can approve. | No role holds it in the permission matrix today; assumed granted to the legal counsel who owns the table (DL01). | RESOLVED | SPEC-006 |
| CLAR-004 | AC1; SPEC-003 | Are the sign-off dates per row or one date for the file? | Validation shape. | Per row: the table carries a user and a date for each sign-off, and the AC shows 6 November 2026 on each row. | RESOLVED | SPEC-003 |
| CLAR-005 | BR4; SPEC-015 | Does a new version change a document already stored? | Would rewrite history. | No. Work already done keeps the version it used; only new reads use the new version from its date (story BR4, AC6). | RESOLVED | SPEC-015 |
| CLAR-006 | Contract; SPEC-010 | Is a new endpoint needed for the load? | Would add a contract. | No. P4 `POST /admin/reference-loads` already accepts a table code; the story adds `DOCUMENT_TYPE` as a value. | RESOLVED | SPEC-010 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story, the P4 contract or the
named decision log entries. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this reference-data story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New versioned document type table and loader; no screen and no contract change; the P4 reference-load and approval endpoints are reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: reference data table and loader with no endpoint delta]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 7 acceptance criteria, 6 exception paths and 5 load states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
