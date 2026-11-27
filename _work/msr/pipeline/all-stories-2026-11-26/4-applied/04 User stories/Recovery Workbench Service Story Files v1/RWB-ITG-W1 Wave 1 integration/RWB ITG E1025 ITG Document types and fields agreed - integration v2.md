# RWB-ITG-E1025-ITG Document types and fields agreed

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-025 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E1025-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1025-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-025 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1069-APP, RWB-P5-E1025-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-004) |
| Status | Draft (realignment v1) |

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-025 document-type reference data across rwb-document (P5, the owner of `rwb_document.document_type` and of the version in force) and rwb-source-data (P1, the owner of the ACE field dictionary)**, so that **the store, the type reader and every field definition are proved to agree on one signed version before wave 1 exits**.

### 2. Business rationale

The legacy story turns the signed list of six document types and their key fields into versioned reference data so that classification and extraction have one target: the type table carries the write-once flag, the retention class and the field list per row, the P4 reference-load endpoint carries the file, the P4 list service serves LOV-RETENTION, and a version in force is selected by its valid-from date. The document store (RWB-E1-024), classification (RWB-E1-050) and extraction (RWB-E1-053) all read the same table, which is what makes the list one signed target rather than three opinions. The measure it serves is fields extracted without review (FSD P5 A2.3.1) under REQ-DCM-004.

In the target the table stays where the rows belong. `document_type` is a P5 rwb-document table and its version in force is P5's own fact (DP-01; Architecture v5 slide 16 and slide 41 put metadata, custody, OCR text and fields, signatures and retention in `rwb_document`). Reference data and LOV are owned by P3 rwb-case under the default ruling and DP-07 (Ownership Map rows `reference_row`, `reference_version` and `lov_value`), so the legacy P4 `POST /admin/reference-loads` path and the P4 list service are replaced by that owner's path, while P5 still implements the loader and the approval for its own table and publishes them as the DOCUMENT_TYPE load path of RWB-P5-E1025-APP. Three facts follow, and none of them can be proved inside one service: the store and the type reader must use the same version in force for the same business date; every field definition in force must resolve to a field of the P1 ACE field dictionary published by rwb-source-data; and the load, the sign-offs and the retention classes must be refused in full without moving the version in force. Every call in the run is one hop with a 2 s budget (ADR-020, DP-11), and SCR-40 Reference data is an Epic 8 screen that will reach the same data through gateway-bff (DP-19), so the suite asserts the screen facts through the contracts instead.

The legacy criteria are not re-implemented here. The legacy AC1 to AC7 stay with RWB-P5-E1025-APP, which proves the loader, the row validation, the separation of duty and the version-in-force rule inside rwb-document against its published contract. This story owns no legacy criterion (`acs` is empty in the work package) and writes nine new criteria that only a run across the two owners can prove: the store and the reader agreeing on one version, the field definitions resolving to P1, the store refusing a type not in force, the load refusing a field with no source field, the sign-off and value refusals at the owner's path, the repeated version, the future-version boundary and the permission refusal.

No service contract is faked: the two integration dependencies are the real services on their published wave 1 contracts, and a fake would defeat the purpose of the run. Where the sources do not name the DOCUMENT_TYPE load path after the reference-data ruling, the suite asserts through the P5 owner's published path as it is delivered by RWB-P5-E1025-APP and records the open point as `Not specified in the source documents (GAP-0350; ASM-0444)`. The only stubs are the external ones named in section 12.8.

### 3. Preconditions

- RWB-P5-E1025-APP is done: the `document_type` table, the DOCUMENT_TYPE loader, the sign-off columns, the version-in-force rule and the type reader are in SIT, and the DOCUMENT_TYPE load and approval path of the owner is published.
- RWB-P1-E1069-APP is done: the data dictionary contract of rwb-source-data answers `GET /api/recovery/source-data/v1/admin/data-dictionary/fields` for the entity and field registry of the 30 ACE views.
- The published contracts of P5 rwb-document, P1 rwb-source-data and P3 rwb-case are deployed in SIT under their own per-service bases behind gateway-bff.
- Version "DOCTYPE-2026.11" is in force from 30 November 2026 with the six types DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE, their 26 fields and both sign-offs.
- LOV-RETENTION holds the codes "LEGAL10Y" and "GENERAL05Y" and is read through the P3 reference-data contract under DP-07.
- The load file fixture "DOCTYPE-2026.11" and the negative variants of section 7 are prepared with synthetic sign-off identities, each sign-off carrying a user ID and a date.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic case and its business-date clock control.
- The environment is SIT with the topics of the wave 1 services, their retry and `.dlt` topics and the schema registry.
- No production data is read, copied or connected to; every case, type file, sign-off identity and field row in the run is synthetic.
- The release date 30 November 2026 is tentative and is copied unchanged; there is no build dependency, so the story is ready on Day 1.

### 4. Flow

1. QA integration engineer: seeds the synthetic case, the load-file fixtures and the dictionary expectations of the harness RWB-ITG-W1J01-ITG; no service schema is opened and no production row is used.
2. Harness: reads the version in force for 30 November 2026 through the P5 document contract and records table version "DOCTYPE-2026.11" with its six types and 26 field definitions.
3. Harness: reads `GET /api/recovery/source-data/v1/admin/data-dictionary/fields` and resolves the four field definitions in force for COURT_NOTICE, namely court_name, black_case_no, notice_date and hearing_date.
4. Harness: stores one synthetic court notice through `POST /api/recovery/document/v1/documents` with type COURT_NOTICE and reads it back through `GET /api/recovery/document/v1/documents/{documentId}`; it asserts the type, retention class "LEGAL10Y", write_once true and the same table version the type reader returns.
5. Harness: repeats the store and read for APPRAISAL_REPORT and asserts retention class "GENERAL05Y", write_once false and four fields.
6. Harness: posts a store with a type that is not in force and records the 422 and MSG-P5-006; it then reads the documents of the case and asserts that nothing was added.
7. Harness: posts a load through the DOCUMENT_TYPE load path published by RWB-P5-E1025-APP whose row 4 field `guarantor_email` has no source field in the P1 data dictionary, and asserts refusal in full with MSG-P3-027 naming the row and the field and the version in force unchanged; the load path is not named in the source documents (GAP-0350).
8. Harness: posts the sign-off variant whose row 6 has no NPA sign-off, then the value variant with retention class "KEEP99" and a repeated type code, then a second load of the same version, and records every status and message.
9. Harness: loads "DOCTYPE-2027.01", which adds field court_region to COURT_NOTICE, with valid from 1 January 2027; it moves the business date with the clock control and asserts the reads of the type table and of the store's reader on 31 December 2026 and on 1 January 2027.
10. Harness: posts a load as a caller without the Reference data C right, records the 403 and MSG-P4-002, writes the evidence report and removes the synthetic fixtures and the extra version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A row has no Legal or no NPA sign-off, or a sign-off without a date | The load is refused in full; no row of the file is written; the version in force is unchanged | MSG-P3-027 | AC5 |
| X2 | A row has a retention class that is not in LOV-RETENTION, or repeats a type code | The load is refused in full; the version in force is unchanged | MSG-P3-027 | AC6 |
| X3 | The same table version is loaded a second time | Refused with 409; the first load is kept unchanged | MSG-P3-027 | AC7 |
| X4 | A new version carries a valid-from date in the future | The current version stays in force until that date and the store keeps storing under it; the boundary is asserted on both dates | None | AC8 |
| X5 | The person who loaded a version tries to approve it | Refused with 409; the load stays LOADED. The separation of duty is proved by the owner story, not re-implemented here | MSG-P7-002 | Regression of RWB-P5-E1025-APP AC7 |
| X6 | A caller without the Reference data C right posts a load | Refused with 403; nothing is loaded and the version in force is unchanged | MSG-P4-002 | AC9 |
| X7 | A consumed contract drifts from the published one (path, field, status or payload) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC1, AC2 |
| X8 | A consumed call exceeds the 2 s budget or returns a server error | The step is retried under the run policy; the evidence report records the call and the response; no store, type or load fact is asserted on unverified data | None | AC1, AC2 |
| X9 | The P1 field dictionary is unavailable or answers no field for a definition in force | The load check cannot complete and the load is not asserted as accepted; the suite fails the scenario and names the field and the row | MSG-GEN-006 | AC2, AC4 |
| X10 | The W1J01 fixture set, a load file or its sign-off identities do not match the run | The suite fails as a fixture fault and names the mismatched element; no production value is substituted | None | AC1, AC8 |
| X11 | A suite step tries to read a service schema directly | The step does not exist: the suite is built with no client for `rwb_document`, `rwb_source_data` or `rwb_case`, and the pipeline scan fails any change that adds one | None | Section 17 |

X1 to X4 and X6 are the legacy exception paths carried onto the real services, X5 is the legacy separation of duty asserted through the owner story, and X7 to X11 are the cross-service failures that only appear when the run leaves one service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the two APP stories and the published contracts of P5, P1 and P3, not their source code, and it owns no schema and no table |
| Negotiable | The fixture composition, the poll interval and the report layout are configuration; the six type codes, the 26 fields, the retention classes, the table versions and the dates are copied from the legacy story |
| Valuable | Proves across services what no single service can prove: the store and the type reader agree on one version, every field definition resolves to the P1 dictionary, and a refusal never moves the version in force |
| Estimable | One suite module, one load-file fixture pack with its negative variants, one clock control for the version boundary, three contract probes and one evidence report |
| Small | Fits one sprint with the report; no service code and no schema change |
| Testable | Every criterion is asserted on an observable: a document response, a type-table read, a dictionary entry, a refusal status or a message |

### 7. Acceptance criteria

```gherkin
Feature: Document types and fields agreed, end-to-end across rwb-document and rwb-source-data

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force from 30 November 2026
    Given it holds DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE with their 26 fields
    Given LOV-RETENTION holds "LEGAL10Y" and "GENERAL05Y" in the P3 reference data in force
    Given the wave 1 services rwb-document, rwb-source-data and rwb-case are deployed in SIT with their published contracts
    Given the RWB-ITG-W1J01-ITG synthetic data set is loaded and no production data is used

  Scenario: AC1 The store and the type reader use the same version in force (new, D-RCV-60)
    Given the version in force for 30 November 2026 is "DOCTYPE-2026.11"
    When a synthetic document is stored through POST /api/recovery/document/v1/documents with type "COURT_NOTICE"
    Then the stored document carries type "COURT_NOTICE", retention class "LEGAL10Y" and write_once true
    Then GET /api/recovery/document/v1/documents/{documentId} returns the same table version that the type reader returns for the business date
    Then no service reads another service's schema to obtain the type

  Scenario: AC2 Every field definition in force resolves to a P1 field (new, D-RCV-60)
    Given the field definitions in force for "COURT_NOTICE" are court_name, black_case_no, notice_date and hearing_date
    When GET /api/recovery/source-data/v1/admin/data-dictionary/fields is read
    Then each of the four field definitions resolves to a field of the P1 data-dictionary contract
    Then a field definition that resolves to no P1 field refuses the load of AC4

  Scenario: AC3 A type not in force is refused by the store (new, D-RCV-60)
    Given "BANK_STATEMENT" is not a type of version "DOCTYPE-2026.11"
    When a document is stored for the synthetic case with type "BANK_STATEMENT"
    Then the store refuses the call with 422 and MSG-P5-006 naming "BANK_STATEMENT"
    Then no document row, no extracted field and no rwb.document.DocumentStored.v1 exist for that call

  Scenario: AC4 A load whose field has no P1 source field is refused in full (new, D-RCV-60)
    Given a load file for "DOCTYPE-2026.11" whose row 4 field "guarantor_email" has no source field in the P1 data dictionary
    When the file is loaded through the DOCUMENT_TYPE load path published by RWB-P5-E1025-APP
    Then the load is refused in full with MSG-P3-027 naming row 4 and "guarantor_email"
    Then no row of the file is written and the version in force stays "DOCTYPE-2026.11"

  Scenario: AC5 A row without both sign-offs is refused in full (new, D-RCV-60)
    Given a load file whose GUARANTOR_NOTICE row 6 has no NPA sign-off
    When the file is loaded through the DOCUMENT_TYPE load path
    Then the load is refused in full with MSG-P3-027 naming row 6 and "NPA sign-off missing"
    Then no row of the file is written and the version in force is unchanged

  Scenario: AC6 Invalid values are refused in full (new, D-RCV-60)
    Given a load file whose TITLE_DEED row has retention class "KEEP99" and whose seventh row repeats the type code "COURT_NOTICE"
    When the file is loaded through the DOCUMENT_TYPE load path
    Then the load is refused in full with MSG-P3-027 listing both rows
    Then no row of the file is written and the version in force is unchanged

  Scenario: AC7 The same version loaded twice is refused (new, D-RCV-60)
    Given version "DOCTYPE-2026.11" is loaded
    When a file with version "DOCTYPE-2026.11" is loaded again
    Then the request is refused with 409 and MSG-P3-027 naming "version already loaded"
    Then the first load is unchanged

  Scenario: AC8 A future version takes effect on its date and both readers follow it (new, D-RCV-60)
    Given version "DOCTYPE-2026.11" is in force
    Given version "DOCTYPE-2027.01" adds field "court_region" to COURT_NOTICE and is approved with valid from 1 January 2027
    When the type table and the store's reader are read on 31 December 2026 and on 1 January 2027
    Then the reads on 31 December 2026 return "DOCTYPE-2026.11" without "court_region"
    Then the reads on 1 January 2027 return "DOCTYPE-2027.01" with field "court_region"
    Then the store and the type reader return the same version on both dates

  Scenario: AC9 A caller without the Reference data C right is refused at the load path (new, D-RCV-60)
    Given a caller holds a role without the Reference data C right
    When the caller posts a load through the DOCUMENT_TYPE load path
    Then the service refuses the call with 403 and MSG-P4-002
    Then nothing is loaded and the version in force is unchanged
```

**Target reading.** The version in force, the type rows and the store are asserted only through the P5 document contract on `rwb_document`; the field names are resolved only through the P1 data-dictionary contract; LOV-RETENTION is read through the P3 reference-data contract under DP-07; and the load and approval are exercised through the DOCUMENT_TYPE load path of the P5 owner as delivered by RWB-P5-E1025-APP. The suite opens no schema, writes no row and copies no business value: every type code, field name, retention class and table version in section 7 is copied from RWB-E1-025.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The document types and their fields are signed by Legal and NPA before extraction is built | RWB-E1-025 BR1; REQ-DCM-004; DL19 |
| BR2 | Each type row carries the write-once flag, the retention class and the field list | RWB-E1-025 BR2; DT02 |
| BR3 | A load with any invalid row is refused in full | RWB-E1-025 BR3; refdata change process, step 3; CTL-08 |
| BR4 | A version takes effect on its valid from date; work already done keeps the version it used | RWB-E1-025 BR4; refdata change process, step 6; R-UNI-38 |
| BR5 | The person who loads a version does not approve it | RWB-E1-025 BR5; roles separation of duty; CTL-08 |
| BR6 | Retention class codes come from LOV-RETENTION | RWB-E1-025 BR6; LOV-RETENTION; DL26 |
| BR7 | The six proposed types apply until the bank provides its own list | RWB-E1-025 BR7; DL19 |
| BR8 | P5 rwb-document owns the `document_type` rows and the version in force in `rwb_document`; no other service holds a copy of the type rows | DP-01; Ownership Map P5 `document_type`; Architecture v5 slide 41 |
| BR9 | Reference data and LOV are owned by P3 rwb-case under the default ruling, so LOV-RETENTION is read through the P3 reference-data contract and the legacy P4 reference-load path is replaced by that owner's path | DP-07; R-PREC default ruling; Ownership Map P3 `reference_row`, `reference_version`, `lov_value` |
| BR10 | The store and the type reader read one version in force for the same business date, and a document stored on that date carries the retention class and write-once flag of that version | RWB-E1-025 BR4; DP-01 |
| BR11 | Every field definition in force resolves to a field of the P1 ACE field dictionary, and a type whose field has no source field is not loaded | REQ-DCM-004; DP-05; Ownership Map P1 `sys_fields`, `sys_field_version` |
| BR12 | No cross-schema read: the suite asserts through the owners' contracts and never opens `rwb_document`, `rwb_source_data` or `rwb_case` | DP-01; ADR-021 |
| BR13 | One hop and two seconds: every cross-service call goes to the owning service under its own base with the 2 s client budget, and no service is called through another service | ADR-020; DP-11; DP-13 |

The initial field lists are assumed until the sign-off (DL19) and are copied unchanged from RWB-E1-025: DEMAND_LETTER case_no, account_no, letter_date, amount_demanded, pay_by_date; COURT_NOTICE court_name, black_case_no, notice_date, hearing_date; APPRAISAL_REPORT appraisal_no, appraisal_date, appraised_value, title_doc_no; TITLE_DEED title_doc_no, land_office, owner_name, area_sq_wa; SETTLEMENT_AGREEMENT case_no, agreement_date, settlement_amount, installment_count, borrower_name; GUARANTOR_NOTICE case_no, guarantor_name, notice_date, amount_claimed. Write-once is true for every type except APPRAISAL_REPORT; retention is LEGAL10Y for the write-once types and GENERAL05Y for APPRAISAL_REPORT (assumed; DL26, DL27).

### 9. State transitions

None for the case status. This story does not change a case status and writes no document state. It reads and asserts the reference-load state, the type version in force and the state a stored document inherits.

| Object | State | Meaning |
|---|---|---|
| Reference load | LOADED | Every row passed its checks, the rows are stored and the version is not yet in force |
| Reference load | REFUSED | At least one row failed a check; no row of the file is written and the version in force stays in force |
| Reference load | APPROVED | Approved by a different person from the loader; the version enters force from its valid-from date |
| Document type version | Future | Approved with a valid-from date after the business date; the earlier version stays in force |
| Document type version | In force | The approved version whose valid-from and valid-to cover the business date |
| Document type version | Superseded | Replaced by a later approved version; documents already stored keep the version they used |
| Document | Stored | Stored with the type, retention class and write-once flag of the version in force on its stored date |

The suite moves a load to REFUSED only through the owner's load path, and it never writes a state directly.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, moves the business date, reads the evidence report |
| RW-COE, center of excellence analyst | Prepares the type list and reads the version in force through the P5 contract |
| RW-LEGAL, legal counsel | Signs the list for Legal; the sign-off identity on the load file is synthetic in the run |
| RW-HEADNPA, Head of NPA | Signs the list for NPA; the sign-off identity on the load file is synthetic in the run |
| RW-REFADM, reference data administrator | Loads a version with the Reference data C right |
| Approver with Reference data A | Approves a load and is a different identity from the loader |
| SY-OCR, SY-RULES | Read the version in force; not exercised by this story |
| Service owner of rwb-document | Owns the type rows, the loader, the approval, the version in force and the store |
| Service owner of rwb-source-data | Owns the ACE field dictionary and its contract |
| Service owner of rwb-case | Owns the reference data and the lists under DP-07 |
| No role | Reads a service schema directly, or takes production data into the run |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-219 | document_type (P5 rwb-document) | doc_type_code | Write (P5 rwb-document) |
| DF-REF-220 | document_type (P5 rwb-document) | label_en | Write (P5 rwb-document) |
| DF-REF-221 | document_type (P5 rwb-document) | label_th | Write (P5 rwb-document) |
| DF-REF-222 | document_type (P5 rwb-document) | write_once | Write (P5 rwb-document) |
| DF-REF-223 | document_type (P5 rwb-document) | retention_class | Write (P5 rwb-document) |
| DF-REF-224 | document_type (P5 rwb-document) | field_definitions | Write (P5 rwb-document) |
| DF-REF-225 | document_type (P5 rwb-document) | legal_signoff_by | Write (P5 rwb-document) |
| DF-REF-226 | document_type (P5 rwb-document) | legal_signoff_date | Write (P5 rwb-document) |
| DF-REF-227 | document_type (P5 rwb-document) | npa_signoff_by | Write (P5 rwb-document) |
| DF-REF-228 | document_type (P5 rwb-document) | npa_signoff_date | Write (P5 rwb-document) |
| DF-REF-229 | document_type (P5 rwb-document) | table_version | Write (P5 rwb-document) |
| DF-REF-230 | document_type (P5 rwb-document) | valid_from | Write (P5 rwb-document) |
| DF-REF-231 | document_type (P5 rwb-document) | valid_to | Write (P5 rwb-document) |
| Cross-service load path | document_type, the ACE field dictionary and the P3 reference data | The DOCUMENT_TYPE load path after the P3 reference-data ruling | Not specified in the source documents (GAP-0350; ASM-0444) |

The read-or-write column keeps the legacy marking and names the owner that writes each row: `document_type` is written by P5 rwb-document, and this suite only reads it through the P5 document contract. LOV-RETENTION carries no BR Field ID in the legacy story and is read through the P3 reference-data contract under DP-07. Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-E1-025 unchanged. Every row in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — /api/recovery/integration/v1, rwb.integration.events.v1, rwb-integration and rwb_integration — are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/document/v1/documents | P5 rwb-document | Store a document under the type in force |
| GET /api/recovery/document/v1/documents/{documentId} | P5 rwb-document | Read the retention class and the write-once flag carried from the type version in force |
| GET /api/recovery/source-data/v1/admin/data-dictionary/fields | P1 rwb-source-data | The ACE field dictionary that every field definition in force must resolve to |
| DOCUMENT_TYPE load and approval path of the P5 owner as published by RWB-P5-E1025-APP | P5 rwb-document | Load a version, read the refused rows and approve it as a different identity. The path is Not specified in the source documents (GAP-0350; ASM-0444) |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the suite calls no service through another service.

#### 12.3 Events published

None. The suite publishes no event; it observes the event of the owning service listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.document.DocumentStored.v1 | rwb.document.events.v1 | P5 rwb-document | Exactly one event per stored document, carrying the document ID, the case, the type and the table version it was stored under; the negative store of AC3 publishes none |

No event is produced by the suite. The envelope is CloudEvents 1.0 and a consumer dedupes on the event ID through its inbox (ADR-015).

#### 12.5 Workflows and activities

None of its own. The document intake behind `POST /api/recovery/document/v1/documents` is the P5 owner's workflow on queue `rwb-document`, observed through the event of 12.4; the suite starts no workflow and reads no workflow history.

#### 12.6 Schedules

None. The DOCUMENT_TYPE load is a request to the owner's load path, not a Schedule, and the version in force is read on demand (GAP-0350). The suite fires no Schedule and reads no Schedule state.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). Every fact it asserts is read through a contract of 12.2 or an event of 12.4.

#### 12.8 Contract fakes

External stubs only:

| Stub | Use |
|---|---|
| Synthetic fixture set (harness RWB-ITG-W1J01-ITG) | Supplies the synthetic case, the load files, their sign-off identities and the field rows of the run |
| Mock Entra sign-in | Gives the run its synthetic test identities, as the platform demo sign-in does |

No published service contract is faked: every call in section 12.2 goes to the real SIT service under its published wave 1 contract.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 4 |
| Kafka | 0 | 1 event type |
| Temporal | 0 | 0 |
| File | 0 | 0 |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the nine scenarios against SIT and holds no service code |
| Load-file fixture pack | Test data | The signed file "DOCTYPE-2026.11" with six types and 26 fields, the file with no NPA sign-off on row 6, the file with "KEEP99" and a repeated type code, the file with `guarantor_email`, and the file "DOCTYPE-2027.01" with court_region |
| Version-in-force clock control | Harness control | Moves the business date to 31 December 2026 and to 1 January 2027 and restores it after each assertion |
| Type probe | Assertion | Reads the version in force and the field definitions of a type through the P5 document contract |
| Dictionary probe | Assertion | Resolves every field definition in force against the P1 data-dictionary contract |
| Store probe | Assertion | Stores and reads a document, and compares its table version, retention class and write-once flag with the type probe's answer |
| Evidence report | Report | Records per scenario the table version, the type, the field list, the load results, the messages and the counts |

**Configuration and reference data**

- The SIT endpoints of P5 rwb-document, P1 rwb-source-data and P3 rwb-case, the topics, the queue name and the schema-registry address, all as configuration.
- The table versions "DOCTYPE-2026.11" and "DOCTYPE-2027.01", the six type codes, the 26 field definitions and the retention codes "LEGAL10Y" and "GENERAL05Y", read through the owners' contracts and never written in the suite code.
- The business dates 30 November 2026, 31 December 2026 and 1 January 2027.
- The 2 s client budget, the poll interval and the retention of the evidence report.

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | `document_type` sits in `rwb_document`; the field registry in `rwb_source_data`; the suite asserts through contracts only |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | LOV-RETENTION is read through the P3 contract; the load path replaces the legacy P4 endpoint; on the APP stories, not a build dependency of this suite |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The four consumed REST operations of section 12.2 |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every consumed path in section 12.2 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The history of `document_type` in `rwb_document`; on the APP story, the suite changes no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | SCR-40 Reference data (Epic 8) reaches the same rows through gateway-bff; this suite builds no screen |

An ITG story carries no H, C or X dependency: the dependency-added column records the build dependency of the owning story, and here it sits on RWB-P5-E1025-APP and on the platform contract stories. The two I dependencies are the APP stories RWB-P1-E1069-APP and RWB-P5-E1025-APP, which are the real services the run exercises.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Signed type file | "DOCTYPE-2026.11" with the six type codes, the 26 fields and both sign-offs with a user ID and a date | AC1, AC2, AC7 |
| Field dictionary rows | The P1 dictionary entries that resolve court_name, black_case_no, notice_date and hearing_date, and the absence of a source field for `guarantor_email` | AC2, AC4 |
| Sign-off variant | The GUARANTOR_NOTICE row 6 without the NPA sign-off | AC5 |
| Value variant | The TITLE_DEED row with retention class "KEEP99" and a seventh row that repeats "COURT_NOTICE" | AC6 |
| Future version | "DOCTYPE-2027.01" with field court_region on COURT_NOTICE and valid from 1 January 2027 | AC8 |
| Store fixture | One synthetic case and one court notice of 1.2 MB for the store and the negative type | AC1, AC3 |
| Identity set | The loader, the approver and the caller without the Reference data C right, as synthetic test identities | AC7, AC9 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P5, P1 and P3, with the contract preflight that fails on any drift.
2. Build the load-file fixture pack and the identity set, and record the table versions and the field lists as data rows.
3. Build the type probe and the dictionary probe; assert AC2 on the four COURT_NOTICE field definitions and on the absence of a source field for `guarantor_email`.
4. Build the store probe and assert AC1 and AC3: the stored document carries the type, the retention class and the write-once flag of the version in force, and a type not in force is refused with 422 and MSG-P5-006.
5. Implement the load-path scenarios AC4 to AC7 through the DOCUMENT_TYPE load path published by RWB-P5-E1025-APP, and assert the exact message, row and field of each refusal and the unchanged version in force.
6. Add the version-in-force clock control and assert AC8 on 31 December 2026 and on 1 January 2027, including that the store's reader returns the same version as the type table.
7. Add the negative identity of AC9 and assert 403 with MSG-P4-002 at the load path.
8. Write the evidence report, remove the extra version and the synthetic fixtures, and run the suite twice to prove that a repeated run adds no row and no event.

**Done when.** The nine criteria of section 7 and the eight copies of section 16 pass in SIT against the published wave 1 contracts, the store and the type reader return the same version on every asserted date, the evidence report names every criterion with its observable, the synthetic set and the extra version are removed, and no service code or schema was changed by this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A document hub reference load fails a check | The {table} load was refused: {error} at row {row}. The version in force is unchanged. |
| MSG-P7-002 | Loader approves their own load | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The three messages are copied unchanged from RWB-E1-025 and this story adds no message ID. MSG-P5-006, used by AC3, is the message of the P5 document store asserted as regression of RWB-P5-E1024-APP and is owned there. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. SCR-40 Reference data is an Epic 8 screen and reaches the type table and the lists through gateway-bff (DP-19), so the suite asserts the same facts that the screen will show — the version in force, the six types, their field lists, the retention class and the write-once flag, and the refused rows of a load — through the contracts of section 12.2. The reference data administrator reads the load status and the row errors on the load response, as the owner story describes.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-025-08-ITG | AC9 | Integration | A case owner with Reference data R only posts a load; refused with 403 and MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-025-01-ITG | Regression of RWB-P5-E1025-APP AC1 | Integration | Load file "DOCTYPE-2026.11" with six types, 26 fields and both sign-offs; end-to-end: real services on the wave 1 contracts |
| TC-E1-025-02-ITG | AC1, AC2 | Integration | Approved version in force; read of COURT_NOTICE and APPRAISAL_REPORT, then one stored court notice read back; end-to-end: real services on the wave 1 contracts |
| TC-E1-025-03-ITG | AC5 | Integration | GUARANTOR_NOTICE row 6 without the NPA sign-off; end-to-end: real services on the wave 1 contracts |
| TC-E1-025-04-ITG | AC6 | Integration | Retention class "KEEP99" and a repeated type code "COURT_NOTICE"; end-to-end: real services on the wave 1 contracts |
| TC-E1-025-05-ITG | AC7 | Integration | Version "DOCTYPE-2026.11" loaded twice; end-to-end: real services on the wave 1 contracts |
| TC-E1-025-06-ITG | AC8 | Integration | Version "DOCTYPE-2027.01" with court_region valid from 1 January 2027; reads on 31 December 2026 and on 1 January 2027; end-to-end: real services on the wave 1 contracts |
| TC-E1-025-07-ITG | Regression of RWB-P5-E1025-APP AC7 | Integration | Loader approves own load; refused with 409 and MSG-P7-002; end-to-end: real services on the wave 1 contracts |

The eight rows are the legacy test cases of RWB-E1-025 with their legacy IDs, each suffixed `-ITG` and listed in the order the work package fixes, which puts the access case first; the legacy System level becomes Integration and the legacy Access level becomes Integration (Template and Rules §R7.2). The new cross-service criteria AC3 and AC4 have no legacy test case id of their own: the suite proves them in the same fixture pass that backs TC-E1-025-02-ITG and TC-E1-025-03-ITG, and the evidence report gives each its own verdict. The legacy full test text, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case id.

### 17. Guardrails

- Synthetic data only: the harness RWB-ITG-W1J01-ITG loads every case, load file, sign-off identity and field row, and no production data is read, copied or connected to.
- No personal data in events, logs, evidence or fixtures: the load files carry synthetic sign-off identities and the store carries identifiers and counts only.
- No cross-service table read: every assertion goes through the owner's contract, and the suite ships with no client for `rwb_document`, `rwb_source_data` or `rwb_case` (DP-01).
- No business value in code: the type codes, the field names, the retention classes, the versions and the dates are data rows or properties, read through the owners' contracts.
- A refused load writes no row and never moves the version in force.
- No version is edited or deleted: the extra version of AC8 is removed only as fixture clean-up, and a document already stored keeps the version it used.
- One hop and a 2 s budget on every call (ADR-020).
- No production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-004 | Document types and key fields agreed and signed before extraction is built | The P5 document contract, the DOCUMENT_TYPE load path, the P1 data-dictionary contract, MSG-P3-027 | TC-E1-025-01-ITG, TC-E1-025-02-ITG, TC-E1-025-03-ITG, TC-E1-025-06-ITG |
| DP-01 | Owner's schema, never another service's tables | `document_type` in `rwb_document`; the type reader of P5 | TC-E1-025-02-ITG, TC-E1-025-06-ITG |
| DP-07 | Reference data and LOV owned by rwb-case | LOV-RETENTION through the P3 reference-data contract; the legacy P4 path replaced | TC-E1-025-04-ITG, TC-E1-025-08-ITG |
| DP-11 | One hop, 2 s timeout | The four consumed REST operations of section 12.2 | TC-E1-025-02-ITG, TC-E1-025-05-ITG |
| DP-13 | `/api/recovery/<short>/v1` | Every consumed path in section 12.2 | All |
| DP-15 | Per-service Flyway in the service's own schema | The history of `document_type` in `rwb_document`; the suite changes no schema | TC-E1-025-01-ITG |
| DP-19 | Screen through gateway-bff | SCR-40 Reference data (Epic 8) reaches the same rows through gateway-bff; no screen built here | TC-E1-025-02-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The contract preflight and the four consumed operations | TC-E1-025-02-ITG, TC-E1-025-05-ITG, TC-E1-025-08-ITG |
| ADR-021 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; it asserts through contracts only | Every test case, at the preflight |
| RWB-E1-025 (legacy story) | Document types and fields agreed: AC1 to AC7 | The type table, the loader, the approval and the six types of section 7 | TC-E1-025-01-ITG to TC-E1-025-07-ITG |
| RWB-P5-E1025-APP (component copy) | The loader, the row validation, the separation of duty and the version-in-force rule inside rwb-document | The DOCUMENT_TYPE load path and the P5 document contract | TC-E1-025-01-ITG, TC-E1-025-07-ITG |
| GAP-0350; ASM-0444 | The load path after the P3 reference-data ruling is the P5 owner's published path | The fourth row of section 12.2 | TC-E1-025-03-ITG, TC-E1-025-04-ITG, TC-E1-025-05-ITG, TC-E1-025-08-ITG |

The legacy acceptance criteria AC1 to AC7 stay with RWB-P5-E1025-APP and are not re-owned here; the nine criteria of section 7 are new under D-RCV-60 and test only the cross-service deliverable. The integration dependencies are RWB-P1-E1069-APP and RWB-P5-E1025-APP.

### 19. Out of scope

- The P1 and P5 APP builds and their unit and component tests.
- The contract, database, operations and infrastructure stories of the legacy key.
- The legacy AC1 to AC7 at component level, which RWB-P5-E1025-APP owns, including the four-eyes approval path.
- The P3 reference-data implementation and the LOV administration that replace the legacy P4 endpoint.
- SCR-40 Reference data, which is an Epic 8 screen reached through gateway-bff.
- The retention periods behind each class (RWB-E1-041) and the checklist of required types per case type (RWB-E1-040).
- Stage 2 and 3 document types (RWB-E2-025) and the extraction and classification builds that read the table in force.
- The build of the harness RWB-ITG-W1J01-ITG and the NFR epic RWB-ITG-NFR.
