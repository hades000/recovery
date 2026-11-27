# RWB-P5-E1025-APP Document types and fields agreed

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1025-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-025 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-011) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: moved RWB-E1-025 into rwb-document as the versioned `document_type` table served by its owner. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E1025-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the first six document types (demand letter, court notice, appraisal report, title deed, settlement agreement, guarantor notice) with their key fields agreed with Legal and NPA and held as versioned reference data**, so that **the OCR pipeline, classification and extraction have one signed target list**.

Inside `rwb-document` this is the document-type catalog. The legacy story put the types, the fields and the sign-offs in the monolith reference data; D-RCV-60 keeps the behaviour and moves the rows to their owner:

- **Stays in rwb-document (P5), schema `rwb_document`:** the table `document_type` — the six types, the 26 fields, the write-once flag, the retention class and the Legal and NPA sign-offs, by table version (ownership map: `document_type` is P5's; DP-01).
- **Read locally:** `DocumentTypeCatalog` answers "the version in force on this business date" and "this type on this business date" from `rwb_document` alone, with no cross-service hop for the consumers inside this service (DP-01).
- **Moves to rwb-case (P3):** the reference version registry, the reference rows and the lists of values — `reference_version`, `reference_row` and `lov_value` are P3 tables (ownership map; DP-07). This story reads LOV-RETENTION and the version registry entry for table DOCUMENT_TYPE through the rwb-case reference-data contract (H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON) and never reads `rwb_case` tables.
- **Served by the owner:** the load, the approve and the read of the version in force are P5 operations under `/api/recovery/document/v1` (DP-13), the pattern RWB-P3-E1019-APP applies to its own reference tables. The legacy `POST /admin/reference-loads` and its approve path were a P4 surface; in the target the table owner serves them for its own table (section 12.1).
- **Database access:** through the rwb-document login (DP-02). The login name is Not specified in the source documents (GAP-1041; ASM-1989).
- **Events:** none in this story. The pattern set carries no event pattern (no DP-09), so a load is a synchronous reference operation and no `rwb.document.<Event>.v1` message announces it (section 12.3).
- **Screens:** through the gateway-bff composite route (DP-19); this story adds no screen, and SCR-40 Reference data arrives in Epic 8.

### 2. Business rationale

Classification and extraction cannot be built or measured until the bank fixes which types are read and which fields come out of each (REQ-DCM-004, DL19). Today no signed list exists, so the model would train on a list that may change. This story turns the agreed list into a versioned table that the store (RWB-E1-024), classification (RWB-E1-050) and extraction (RWB-E1-053) read, and that changes by a data load without a code release (DT02). The measure it serves is fields extracted without review (FSD P5 A2.3.1).

The realignment does not change that rationale; it changes where the rows live and who serves them. The signed list is document-hub data, so it becomes `document_type` in `rwb_document`, a versioned table in the service's own schema, served by its owner at the rwb-document base. The one value the table does not own is the retention code list: LOV-RETENTION is reference data and stays with rwb-case (P3), so the loader checks a row's retention class against the list the contract returns, and a list that cannot be read refuses the load whole. What the consumers get is the same signed target list, read in one local call: RWB-P5-E1024-APP (the store) copies the write-once flag and the retention class onto each document, RWB-P5-E1050-APP (classification) reads the types, RWB-P5-E1053-APP (extraction) reads the field list per type, and RWB-P5-E1040-APP (the checklist) points at the type codes. They are consumers of this catalog, not dependencies of this story.

### 3. Preconditions

- RWB-PLT-E1043-CON is published: the reference-data client library, with the list read, the version registry read and its contract fake, so the build runs against the fake from Day 1 (H; DP-07, DP-11).
- RWB-PLT-E1044-CON is in place: the per-service Flyway sequence, so `V1025_1__document_type.sql` runs after the V0001 baseline in `rwb_document` (H; DP-15).
- RWB-PLT-N001-CON is in place: the gateway-bff composite route that carries SCR-40 when the screen arrives in Epic 8 (H; DP-19).
- RWB-P3-E1043-CON is published (C): the reference-data contract of rwb-case returns LOV-RETENTION and the registry entry for table DOCUMENT_TYPE, one hop, 2 s timeout. A C dependency never blocks the build: the story builds against the published contract and the fake.
- RWB-E1-069 is done: the 30 ACE views are in place, so the source fields that each document type can carry are known (legacy precondition, kept).
- The load file "DOCTYPE-2026.11" is prepared by the reference data administrator with the six types, 26 fields and the sign-offs of a legal counsel user and a Head of NPA user (legacy precondition, kept).
- LOV-RETENTION holds the codes LEGAL10Y and GENERAL05Y, assumed until the bank retention schedule arrives (DL26), loaded by the data steward; in the target the list is read through the rwb-case reference-data contract (DP-07). The retention periods behind the classes are not set (DL26) and are out of scope here.
- The loader holds RW-REFADM (Reference data C). The approver holds Reference data A (see section 10); the permission matrix gives Reference data A to no role today and the grant is assumed (legacy DL01; GAP-1040; ASM-1988).
- The legacy precondition that "the P4 endpoint POST /admin/reference-loads exists and calls the P5 ReferenceTableLoader for table code DOCUMENT_TYPE" is replaced: in the target the table owner serves the load and the approve itself under `/api/recovery/document/v1` (section 12.1; DP-13), so no separate P4 surface is needed. The legacy row is kept here for traceability.
- Feature flag `rwb.document.doctypes` is on (the legacy flag `rwb.dochub.doctypes`, renamed to the service naming).
- The rwb-document login exists in the ACE database (DP-02). Its name is Not specified in the source documents (GAP-1041; ASM-1989).
- DL19, DL26 and DL27 stay open: the six proposed types apply until the bank provides its own list (DL19); the retention periods (DL26) and the storage, backup, legal hold and e-discovery arrangements (DL27) are not set, and this story carries only the retention class codes.

### 4. Flow

1. Center of excellence analyst: prepares the list of six types and 26 fields; legal counsel and the Head of NPA review it and sign it with a date (legacy step 1, unchanged).
2. Reference data administrator: prepares the file DOCTYPE-2026.11 in the load template and calls `POST /api/recovery/document/v1/admin/document-types/loads` with the file and validFrom 2026-11-30, carrying an `Idempotency-Key`. The template column layout is Not specified in the source documents (GAP-1039; ASM-1987).
3. DocumentTypeLoader: reads LOV-RETENTION through the rwb-case reference-data contract once per load and validates every row: type code unique in the file and against the stored versions, label present, write-once flag present, retention class in LOV-RETENTION, at least one field, both sign-offs with a user ID and a date.
4. DocumentTypeLoader: on any failure refuses the load whole, writes no row and returns the row errors; the version in force is unchanged.
5. DocumentTypeLoader: on success writes the rows as table version DOCTYPE-2026.11 with `state` LOADED (the standard record column of TSD P5 v2 T3.0), registers the version through the reference-data contract and links it in `reference_version_id`; the version is not yet in force.
6. Approver: approves with `POST /api/recovery/document/v1/admin/document-types/loads/{loadId}/approve`; the approver must be a different person from the loader (MSG-P7-002 otherwise).
7. DocumentTypeLoader: sets the version APPROVED. From validFrom the readers return it as the version in force; the previous version gets `valid_to` of the day before, so exactly one version is in force on any business date.
8. DocumentTypeCatalogService: answers the consumers from `rwb_document` with a five-minute cache cleared on approval; the knowledge of which version was used by work already done stays with the record that used it (R-UNI-38).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A row has no Legal or no NPA sign-off, or a sign-off without a date | Load refused in full; version in force unchanged; no row written | MSG-P3-027 | AC3 |
| X2 | A row has a retention class not in LOV-RETENTION, or repeats a type code | Load refused in full; no row written | MSG-P3-027 | AC4 |
| X3 | The same table version is loaded a second time | Refused with 409; the first load is kept | MSG-P3-027 | AC5 |
| X4 | A new version with a future valid from date | The current version stays in force until that date; open work keeps the version it used | None | AC6 |
| X5 | The loader tries to approve their own load | Refused with 409; the version stays LOADED | MSG-P7-002 | AC7 |
| X6 | A role without Reference data C uploads the file | Refused with 403 | MSG-P4-002 | TC-E1-025-08 (Access) |
| X7 | The rwb-case reference-data contract does not answer inside 2 s, or LOV-RETENTION comes back empty | The load is refused whole and writes no row; no retention class is guessed and no cached list past its time-to-live is used | None from this service; 503 with an RFC 9457 problem detail | Not a legacy AC; the contract test of RWB-P3-E1043-CON covers the 503 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the rwb-case reference-data contract and its fake, the Flyway sequence and the gateway route; it adds the table, the loader, the checks and two read operations, and no other story |
| Negotiable | The type list, the fields, the write-once flags and the retention classes are data; the bank list replaces the six proposed types under DL19 |
| Valuable | Gives the store, classification, extraction and the checklist one signed target list, read locally and changed by a load |
| Estimable | One table, one loader, one validation set, two read operations |
| Small | Under one week with its tests and its contract fake |
| Testable | Each criterion below is one test case in section 16, on the boundary dates where a version changes |

### 7. Acceptance criteria

```gherkin
Feature: Document types and fields agreed

  Background:
    Given LOV-RETENTION holds "LEGAL10Y" and "GENERAL05Y"
    Given user "TEST-REFADM-01" holds RW-REFADM
    Given user "TEST-APPROVER-01" holds Reference data A
    Given the rwb-case reference-data contract mock returns LOV-RETENTION with "LEGAL10Y" and "GENERAL05Y"

  Scenario: AC1 Field list signed (legacy RWB-E1-025 AC1)
    Given the six types and their 26 fields in load file "DOCTYPE-2026.11"
    Given each row carries the legal counsel sign-off of user "TEST-LEGAL-01" dated 6 November 2026
    Given each row carries the NPA sign-off of user "TEST-HEADNPA-01" dated 6 November 2026
    When "TEST-REFADM-01" loads the file for table "DOCUMENT_TYPE" with valid from 30 November 2026
    Then the load has status "LOADED" with 6 rows
    Then every row holds both sign-off user IDs and both dates

  Scenario: AC2 Reference data (legacy RWB-E1-025 AC2)
    Given the rwb-case reference-data contract mock registers reference version "DOCTYPE-2026.11" for table "DOCUMENT_TYPE"
    Given the load from AC1
    When "TEST-APPROVER-01" approves it
    Then the document type table version "DOCTYPE-2026.11" is in force from 30 November 2026
    Then it holds DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE
    Then COURT_NOTICE holds the fields court_name, black_case_no, notice_date and hearing_date with retention class "LEGAL10Y" and write_once true
    Then APPRAISAL_REPORT has retention class "GENERAL05Y", write_once false and 4 fields

  Scenario: AC3 Load without both sign-offs is refused (legacy RWB-E1-025 AC3)
    Given a load file where the GUARANTOR_NOTICE row has no NPA sign-off
    When "TEST-REFADM-01" loads it
    Then the system refuses the load in full with MSG-P3-027 naming row 6 and "NPA sign-off missing"
    Then no row of that file is written and the version in force is unchanged

  Scenario: AC4 Invalid values are refused in full (legacy RWB-E1-025 AC4)
    Given a load file where the TITLE_DEED row has retention class "KEEP99" and a seventh row repeats the type code "COURT_NOTICE"
    When "TEST-REFADM-01" loads it
    Then the system refuses the load in full with MSG-P3-027 listing both rows
    Then the version in force is unchanged

  Scenario: AC5 The same version loaded twice (legacy RWB-E1-025 AC5)
    Given version "DOCTYPE-2026.11" is loaded
    When "TEST-REFADM-01" loads a file with version "DOCTYPE-2026.11" again
    Then the system refuses the request with 409 and MSG-P3-027 naming "version already loaded"
    Then the first load is unchanged

  Scenario: AC6 A future version takes effect on its date (legacy RWB-E1-025 AC6)
    Given the rwb-case reference-data contract mock registers reference version "DOCTYPE-2026.11" and version "DOCTYPE-2027.01" for table "DOCUMENT_TYPE"
    Given version "DOCTYPE-2026.11" is in force
    Given version "DOCTYPE-2027.01" adds field "court_region" to COURT_NOTICE and is approved with valid from 1 January 2027
    When the type table is read on 31 December 2026 and on 1 January 2027
    Then the read on 31 December 2026 returns "DOCTYPE-2026.11"
    Then the read on 1 January 2027 returns "DOCTYPE-2027.01" with field "court_region"

  Scenario: AC7 The loader cannot approve their own load (legacy RWB-E1-025 AC7)
    Given "TEST-REFADM-01" loaded version "DOCTYPE-2027.01" and also holds Reference data A in the test set
    When "TEST-REFADM-01" approves it
    Then the system refuses the request with 409 and MSG-P7-002
    Then the load stays "LOADED"
```

Every AC above is the legacy AC, value for value. The only additions are the origin tag on each Scenario line, one Background line for the rwb-case reference-data contract fake, and the version-registry line in AC2 and AC6; no legacy line was changed or dropped.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The document types and their fields are signed by Legal and NPA before extraction is built | REQ-DCM-004; DL19 |
| BR2 | Each type row carries the write-once flag, the retention class and the field list | Document type table (New); DT02 |
| BR3 | A load with any invalid row is refused in full | refdata change process, step 3; CTL-08 |
| BR4 | A version takes effect on its valid from date; work already done keeps the version it used | refdata change process, step 6; R-UNI-38 |
| BR5 | The person who loads a version does not approve it | roles separation of duty; CTL-08 |
| BR6 | Retention class codes come from LOV-RETENTION | LOV-RETENTION; DL26 |
| BR7 | The six proposed types apply until the bank provides its own list | DL19 |

The initial field lists are assumed until the sign-off (DL19): DEMAND_LETTER case_no, account_no, letter_date, amount_demanded, pay_by_date; COURT_NOTICE court_name, black_case_no, notice_date, hearing_date; APPRAISAL_REPORT appraisal_no, appraisal_date, appraised_value, title_doc_no; TITLE_DEED title_doc_no, land_office, owner_name, area_sq_wa; SETTLEMENT_AGREEMENT case_no, agreement_date, settlement_amount, installment_count, borrower_name; GUARANTOR_NOTICE case_no, guarantor_name, notice_date, amount_claimed. Fields account_no, owner_name, borrower_name and guarantor_name are marked personal. Write-once true for every type except APPRAISAL_REPORT; retention LEGAL10Y for the write-once types and GENERAL05Y for APPRAISAL_REPORT (assumed; DL26, DL27).

Where each rule lives in the target: no rule changes, and four of them change their mechanism. BR1, BR2 and BR7 are rows in `document_type` in `rwb_document`, written by the owner (DP-01, DP-15), so a type list change is a data load and not a release. BR3 and BR5 are enforced in this service on its own rows: the validation runs on the whole file before a single row is written, and the approve compares the approver with the loader of that load. BR4 is answered from `valid_from` and `valid_to` in `rwb_document`; a future-dated approved version is written and not returned until its date, and the version a piece of work used stays on the record that used it. BR6 is answered by the rwb-case reference-data contract (DP-07, DP-11): the list is read once per load over one hop with a 2 s timeout, and a list that cannot be read refuses the load whole (X7). No rule is written in code as a value: the six codes, the 26 fields, the write-once flags and the retention codes are rows or list values.

### 9. State transitions

None for the case. This story does not change a case status; it changes the state of a table version, held on the `document_type` rows in the standard record column `state` (TSD P5 v2 T3.0).

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every row passes every check and LOV-RETENTION is answered over the contract | LOADED; no row in force yet |
| None | Load | Any row fails a check, or the contract does not answer | REFUSED; no row is written and the version in force is unchanged |
| LOADED | Approve | The approver is not the loader | APPROVED; in force from `valid_from` |
| APPROVED | A later version approved with a later `valid_from` | The later date arrives | The earlier version is SUPERSEDED and gets `valid_to` of the day before |

ROLLED_BACK is the fifth state named in the reference-data vocabulary and is reached only through the reference version registry of rwb-case (RWB-P3-E1043-CON): this story writes LOADED, APPROVED and SUPERSEDED, and REFUSED writes no row at all. A version with a future `valid_from` shows APPROVED and changes nothing it does not cover until its date (AC6).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Prepares the list and reads the table |
| RW-LEGAL, legal counsel | Signs the list for Legal |
| RW-HEADNPA, Head of NPA | Signs the list for NPA |
| RW-REFADM, reference data administrator | Loads the file (Reference data C) |
| Approver with Reference data A | Approves the load. The permission matrix gives Reference data A to no role today; assumed granted to the legal counsel who owns the table (DL01; GAP-1040; ASM-1988) |
| SY-OCR, SY-RULES | Read the version in force through the document-type read (section 12.1) |
| The rwb-document service identity | Serves the load, the approve and the read of the version in force; reads LOV-RETENTION through the rwb-case reference-data contract; writes `document_type` only |

Every "who" is a role code, and the rights are the legacy ones: Reference data C to load, Reference data A to approve, Reference data R to read. The rights are enforced by the platform guard library that every service from the template carries; this story's pattern set does not include the access pattern, so it adds no dependency for the guard and no role table of its own. The role codes, their rights and their separation-of-duty conflicts stay with rwb-access (P4) and are not read here.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-218 | document_type | id | Write |
| DF-REF-219 | document_type | doc_type_code | Write |
| DF-REF-220 | document_type | label_en | Write |
| DF-REF-221 | document_type | label_th | Write |
| DF-REF-222 | document_type | write_once | Write |
| DF-REF-223 | document_type | retention_class | Write |
| DF-REF-224 | document_type | field_definitions | Write |
| DF-REF-225 | document_type | legal_signoff_by | Write |
| DF-REF-226 | document_type | legal_signoff_date | Write |
| DF-REF-227 | document_type | npa_signoff_by | Write |
| DF-REF-228 | document_type | npa_signoff_date | Write |
| DF-REF-229 | document_type | table_version | Write |
| DF-REF-230 | document_type | valid_from | Write |
| DF-REF-231 | document_type | valid_to | Write |
| DF-REF-232 | document_type | reference_version_id | Write |
| DF-REF-233 | document_type | classify_threshold | Write |

LOV-RETENTION is read through the rwb-case reference-data contract (`lov_value` rows, no BR Field ID of this story). Field IDs are those in the Logical Data Model and Data Dictionary and in TSD P5 v2 T3.1.

`document_type` is in schema `rwb_document` and is P5's (ownership map). `reference_version`, `reference_row` and `lov_value` are P3 tables in `rwb_case`: they are never read directly by SQL from this service, only through the reference-data contract (DP-01, DP-07) — the version the loader registers comes back as the id written to `reference_version_id`. The standard record columns of TSD P5 v2 T3.0 (`state`, `is_active`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`) are written by the platform persistence layer and carry the load state. `document_hub_parameter` is a P5 table too but is not read or written by this story.

### 12. Contract

#### 12.1 REST operations provided
| Operation | Purpose | Owner (ownership map) | Idempotency |
|---|---|---|---|
| POST /api/recovery/document/v1/admin/document-types/loads | Loads the DOCUMENT_TYPE file as one table version: every row is checked, a failed row refuses the whole file, and a clean file is staged with state LOADED and is not in force | P5 | `Idempotency-Key` header; a second load of the same table version is refused with 409 |
| POST /api/recovery/document/v1/admin/document-types/loads/{loadId}/approve | Approves a LOADED version; refused when the approver is the loader; from `valid_from` the version is in force and the previous version gets `valid_to` | P5 | Approving an APPROVED load returns it unchanged |
| GET /api/recovery/document/v1/document-types | The version in force on a business date: the table version and every type with its fields, write-once flag and retention class; the read RWB-P5-E1024-APP, RWB-P5-E1050-APP, RWB-P5-E1053-APP and RWB-P5-E1040-APP consume | P5 | Not applicable |
| GET /api/recovery/document/v1/document-types/{docTypeCode} | One type in the version in force on a business date | P5 | Not applicable |

The exact path segments, the request and response field names, the row-error shape of a refused load and the shape of the reference-version registration call are Not specified in the source documents (GAP-1039; ASM-1987). What this story fixes is the behaviour: 401; 403 without Reference data C (MSG-P4-002); 409 for a version already loaded (MSG-P3-027) or for the loader approving their own load (MSG-P7-002); 422 for a failed row (MSG-P3-027 with row and error); 503 when the reference contract or the store does not answer. Every response is an OpenAPI 3.1 contract published before code, with `Idempotency-Key` on the two POSTs.

These operations are the pattern RWB-P3-E1019-APP applies to its own reference tables: the table owner serves its own load and approve, so no other service writes `document_type` and no other service needs a P4 surface to load it.

#### 12.2 REST operations consumed
| Operation | Provider | Why | Pattern |
|---|---|---|---|
| GET /api/recovery/case/v1/admin/lists/{listCode} | rwb-case (P3), reference-data contract | LOV-RETENTION in force (LEGAL10Y, GENERAL05Y; DL26) for the row check and for the type read; one hop, 2 s timeout, cached for the life of the load | DP-07, DP-11 |

The reference version registry is reached through the same contract: `document_type.reference_version_id` (DF-REF-232) takes the registry's id for table DOCUMENT_TYPE, and the call that registers a version is part of the load surface in 12.1 (GAP-1039; ASM-1987). No parameter is read: the load file version and the retention codes are reference data, and the feature flag is a platform flag, so there is no parameters row in this story.

#### 12.3 Events published
None. This story publishes no event, and the pattern set carries no event pattern (no DP-09, no outbox in this story): a load and an approval are synchronous operations whose result is returned to the caller.

#### 12.4 Events consumed
None. No event starts a load or a read; a version takes effect on its `valid_from` date when the catalog is read, not on a message.

#### 12.5 Workflows and activities
None. The load, the approve, the version-boundary read and the cache clear are service steps in one transaction each; there is no Temporal workflow or activity in this story, and none is needed (DP-10 is not in its pattern set).

#### 12.6 Schedules
None. Nothing runs on a clock: a future version takes effect because the read compares the business date with `valid_from` and `valid_to`, not because a job moves it (DP-10 is not in this story's pattern set).

#### 12.7 Tables owned
| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| document_type | rwb_document | P5 | Writes every field, DF-REF-218 to DF-REF-233, plus the standard record columns |
| document_hub_parameter | rwb_document | P5 | Not read and not written here |
| lov_value, reference_row, reference_version | rwb_case | P3 | **Never read.** Reached over the rwb-case reference-data contract only (DP-01, DP-07) |

Database access uses the rwb-document login (DP-02); its name is Not specified in the source documents (GAP-1041; ASM-1989). No statement in this story names a table in another schema: the retention list, the version registry entry and every list value arrive over the contract, and no other schema is read.

#### 12.8 Contract fakes
| Fake | Serves | Used for |
|---|---|---|
| rwb-case reference-data contract fake (RWB-PLT-E1043-CON, RWB-P3-E1043-CON) | GET /admin/lists/{listCode} with LOV-RETENTION returning "LEGAL10Y" and "GENERAL05Y", and the version registry answers for table DOCUMENT_TYPE | Every row check and every read in the tests, including AC2 and AC6, from Day 1 (DP-07, DP-11) |
| document-type admin fake (this story's own OpenAPI document) | The two load and approve operations and the two reads of 12.1 | RWB-P5-E1024-APP, RWB-P5-E1050-APP, RWB-P5-E1053-APP and RWB-P5-E1040-APP build against the catalog before the table is in force; the harness of RWB-ITG-E1025-ITG uses it for the end-to-end copy |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)
| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 operations under `/api/recovery/document/v1` | 1 operation (the rwb-case reference-data list read) | OpenAPI 3.1, one hop, 2 s timeout, `Idempotency-Key` on the two POSTs |
| Kafka | None | None | No `rwb.document.events.v1` message in this story; the pattern set carries no event pattern |
| Temporal | None | None | No workflow, activity or schedule |
| File | 1 (the load file as `multipart/form-data` on the load operation) | 0 | The file is read in the request; no claim-check store |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `types`. Service base `/api/recovery/document/v1`, schema `rwb_document`, topic `rwb.document.events.v1`, task queue `rwb-document` (not used by this story).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentTypeLoader | Service | Parses the load file, reads LOV-RETENTION over the contract, validates every row, refuses the whole file on any failure, stages a version as LOADED and approves it with the separation-of-duty check |
| DocumentTypeCatalog | Published interface | The version in force on a business date and one type by code on that date, for the consumers inside this service |
| DocumentTypeCatalogService | Service | Implements DocumentTypeCatalog from `rwb_document` with a five-minute cache cleared on approval; applies the `valid_from`/`valid_to` rule |
| DocumentTypeRepository | Repository | Reads and writes `document_type` only; no cross-schema SQL |
| DocumentTypeEntity | Entity | Maps `document_type`, including the standard record columns |

**Database**

- `document_type` in `rwb_document`, columns from TSD P5 v2 T3.1: `id` uuid, `doc_type_code` varchar(30), `label_en` varchar(120), `label_th` varchar(120), `write_once` boolean, `retention_class` varchar(10), `field_definitions` jsonb, `legal_signoff_by` uuid, `legal_signoff_date` date, `npa_signoff_by` uuid, `npa_signoff_date` date, `table_version` varchar(20), `valid_from` date, `valid_to` date, `reference_version_id` uuid, `classify_threshold` numeric(4,3), `load_id` uuid, plus the standard record columns of T3.0.
- Constraints: unique (`doc_type_code`, `table_version`); not null on the sign-off columns, `table_version`, `valid_from`, `doc_type_code`, `write_once`, `retention_class` and `field_definitions`, per the Required column of TSD P5 v2 T3.1.
- Index `ix_document_type_valid` on (`valid_from`, `valid_to`), so the in-force read on a business date is one index range.
- Flyway step `V1025_1__document_type.sql` in the per-service sequence, after the V0001 baseline (DP-15, H RWB-PLT-E1044-CON). The legacy migration name `V1_5_025__document_type.sql` maps into that sequence; no monolith migration name is reused.

**Configuration and reference data**

- The load file DOCTYPE-2026.11, prepared by the reference data administrator and signed by legal counsel and the Head of NPA (legacy); its template layout is Not specified in the source documents (GAP-1039; ASM-1987).
- LOV-RETENTION (LEGAL10Y, GENERAL05Y; DL26) through the rwb-case reference-data contract (DP-07), never a constant in code.
- Feature flag `rwb.document.doctypes`, from the platform flag library (the legacy flag `rwb.dochub.doctypes`). Off: the load operation refuses table DOCUMENT_TYPE and the catalog returns the version already in `rwb_document`.
- The rwb-document login (DP-02), name Not specified in the source documents (GAP-1041; ASM-1989).

**Build steps**

1. Write the migration and the entity; test the constraints, the unique key on (`doc_type_code`, `table_version`) and the index.
2. Build the row parser for the load template columns; unit test a valid file of 6 rows and 26 fields.
3. Build the validation rules and the refuse-whole behaviour, with LOV-RETENTION from the contract fake; unit test AC3 and AC4 and the empty-list path (X7).
4. Build staging, the version check and approval with the separation-of-duty check; test AC1, AC2, AC5 and AC7.
5. Build DocumentTypeCatalogService with the `valid_from` rule and the cache clear on approval; test AC6 on the boundary dates.
6. Publish the four operations and the fake, and add the access test on the load operation; run the catalogue against the fake from RWB-P5-E1024-APP.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Each row in place. DP-01 puts `document_type` in `rwb_document` and is why no statement here names `rwb_case`; the table is read locally by DocumentTypeCatalog, so the four consumers pay no cross-service hop. DP-07 supplies LOV-RETENTION, and the registry entry for table DOCUMENT_TYPE, through the rwb-case reference-data contract — the one value this story does not own is answered there, and a refused or empty answer refuses the load whole instead of falling back to a constant. DP-11 makes that read a one-hop REST call with a mock, one hop and a 2 s timeout, so the build starts on the fake before P3 publishes. DP-15 is the per-service Flyway step `V1025_1__document_type.sql` that creates `document_type` in the sequence after the V0001 baseline. DP-13 moves the base from the monolith path to `/api/recovery/document/v1`, so the load, the approve and the two reads sit under the owner's base. DP-19 is the gateway-bff composite route to SCR-40 Reference data when the screen arrives in Epic 8: this story carries the route dependency and adds no screen.

**Done when.** The tests in section 16 pass, version DOCTYPE-2026.11 is approved in SIT with both sign-offs, the four consumers read the version in force from `rwb_document`, and no statement in the service names a table outside `rwb_document`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A document hub reference load fails a check | The {table} load was refused: {error} at row {row}. The version in force is unchanged. |
| MSG-P7-002 | Loader approves their own load | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The message IDs and texts are the legacy ones, unchanged; Thai text for each message follows decision DL10. For MSG-P3-027 the {table} value is DOCUMENT_TYPE, {error} names the failed check (for example "NPA sign-off missing" or "version already loaded") and {row} is the file row number.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The load answers 401, 403, 409, 422 and 503; the approve answers 401, 403, 404, 409 and 503. When the rwb-case reference-data contract does not answer inside 2 s the service returns 503 with no message of its own and writes nothing (X7), so no retention class is ever guessed.

### 15. Screens and states

No screen in this story. SCR-40 Reference data comes in Epic 8 and reaches rwb-document through the gateway-bff composite route (DP-19). The reference data administrator sees the load status and the row errors in the response of the load and approve operations; the center of excellence analyst reads the version in force through the document-type read in section 12.1. The only state a version has is the one in section 9: LOADED, APPROVED (and in force from its date), SUPERSEDED, REFUSED.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-025-08 | Access | Component | Case owner (RW-CASEOWN, Reference data R only) uploads the file; refused with MSG-P4-002 |
| TC-E1-025-01 | AC1, BR1 | End to end | Load file DOCTYPE-2026.11 with six types, 26 fields and both sign-offs |
| TC-E1-025-02 | AC2, BR2, BR6 | End to end | Approved load; read of COURT_NOTICE and APPRAISAL_REPORT |
| TC-E1-025-03 | AC3, BR1, BR3 | End to end | GUARANTOR_NOTICE row without the NPA sign-off |
| TC-E1-025-04 | AC4, BR3 | End to end | Retention class KEEP99 and a repeated type code |
| TC-E1-025-05 | AC5 | End to end | Same version loaded twice |
| TC-E1-025-06 | AC6, BR4 | End to end | Version DOCTYPE-2027.01 valid from 1 January 2027 |
| TC-E1-025-07 | AC7, BR5 | End to end | Loader approves own load |

The legacy TC IDs, Covers and Data are kept character for character. The legacy Level "System" maps to "End to end" and "Access" maps to "Component", because the access test now exercises the guard library and the reference-data fake in one component. The end-to-end copies of these test cases in the wave-1 harness are RWB-ITG-E1025-ITG, where each carries the `-ITG` suffix (TC-E1-025-01-ITG to TC-E1-025-08-ITG) and runs the load, the approve and the future-dated read through the gateway against the real rwb-case contract. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: type codes, fields, write-once flags and retention classes are rows in `document_type`, and the retention codes are list values read over the contract (DP-07).
- No personal data in logs, tests or prompts. Sign-off users in tests are synthetic IDs; no name, address or customer identifier is written to a log, and the personal fields of a type are marked in `field_definitions` and never logged.
- No cross-schema read (DP-01): LOV-RETENTION and the version registry arrive over the rwb-case reference-data contract, and no statement in the service names `rwb_case` or any other schema.
- A refused load writes no row: the validation runs on the whole file before the first insert, and a contract that does not answer refuses the load (X7).
- The separation of duty is enforced on this service's own rows: the approve compares the approver with the loader of that load (MSG-P7-002).
- One version in force per business date, from `valid_from` and `valid_to` only; a future-dated approval changes nothing until its date, and work already done keeps the version it used (R-UNI-38).
- The table is in `rwb_document` only; the rwb-document login is the only grantee, and its name is Not specified in the source documents (GAP-1041; ASM-1989).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-004 | Document types and key fields agreed and signed before extraction is built | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-03 | 13 Manage documents and correspondence | R-UNI-38 | TC-E1-025-01 to TC-E1-025-08 |

| Legacy reference | Where it is kept |
|---|---|
| Load file DOCTYPE-2026.11 with six types and 26 fields, signed by Legal and NPA | Sections 3, 4, 7, 8, 13, 16 |
| Type codes DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT, GUARANTOR_NOTICE | Sections 7, 8, 16 |
| Retention classes LEGAL10Y and GENERAL05Y (LOV-RETENTION; DL26) | Background, AC2, sections 8, 12.2, 13 |
| MSG-P3-027, MSG-P7-002, MSG-P4-002 | Section 14, exception paths |
| Write-once flag and the assumed field lists (DL19, DL27) | Sections 8, 11, 13 |
| Table document_type and DF-REF-218 to DF-REF-233 | Sections 11, 13 |
| Legacy key RWB-E1-025, story RWB-P5-E1025-APP, its contract and fake | Metadata, sections 3, 12 |
| DL19, DL26, DL27 | Sections 3, 8, 13, 18 |

### 19. Out of scope

- The retention periods behind each class and the retention job (RWB-P5-E1041-APP; DL26).
- The checklist of required types per case stage and route (RWB-P5-E1040-APP).
- Stage 2 and 3 document types (RWB-P5-E2025-APP; FSD P5 A2.22).
- The SCR-40 Reference data screen (Epic 8); this story carries only its gateway-bff route dependency (DP-19).
- The reference version registry, the reference rows and the list values themselves: rwb-case (P3) owns them and serves them over its reference-data contract (RWB-P3-E1043-CON).
- The consumers themselves: the store (RWB-P5-E1024-APP), classification (RWB-P5-E1050-APP), extraction (RWB-P5-E1053-APP) and the checklist (RWB-P5-E1040-APP) read the catalog here but are built by their own stories.
- The end-to-end proof of the load, the approve and the future-dated version across the gateway: RWB-ITG-E1025-ITG.
- The decision-record entry for a load: this story's pattern set carries no decision-log pattern (no DP-03).
