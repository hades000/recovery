# RWB-P5-E1016-APP Access control per data product and catalog entries

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP05, DP07, DP08, DP11, DP19 |
| Parallel lane | L-P5-C |
| Ready to start | Day 1 against the two fakes of RWB-P3-E1018-CON and RWB-P4-E1037-CON |
| Depends on (build) | None |
| Contract dependencies | RWB-P4-E1037-CON; RWB-P1-E1064-CON; RWB-P3-E1018-CON |
| Integration dependencies | None |
| External dependencies | None |
| Size | Not specified in the source documents (DOR-RWB-P5-E1016-APP-16); the squad sizes this story at refinement |
| Contract version | /v1 on base /api/recovery/document/v1; no numbered contract version in the source documents (DOR-RWB-P5-E1016-APP-23) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-009, FR-P5-010) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-021, RD-P1-004, RD-P1-025 |

**Version 3 changes.**

- The dictionary field read is cited to RWB-P1-E1064-CON with its published parameters and property names (RD-P1-021; findings 1 and 2).
- Any dictionary answer other than 200 refuses the read; AC10 added; the right of the rwb-document identity on that operation is Pending under NEW-GAP-F17-3 (finding 3).
- Error answers use the shared Problem body with `messageCode` and `traceId` (RD-P1-004; finding 4).
- Dictionary counts restated as the RD-P1-025 baseline (finding 5).
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).
- MSG-GEN-006 carries the English text of Error and Message Standard v6 (RD-P1-004).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: the secondary P5 slice of RWB-E1-016. It brings the document data product DP10's retention-class contribution and the access, masking and PII-log rules of the two document reads into `rwb-document`, with schema `rwb_document`, REST base `/api/recovery/document/v1` and the ownership rulings of Architecture v5. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1016-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 15 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the document data product to be one findable catalog contribution whose retention class is served by `rwb-document`, and every document read of the service to be authorised per role and data product, scope-checked, masked by role and written to the PII access log**, so that **personal data in documents is read only by the roles that need it, every read is evidenced, and the product's retention is stated once, by the service that owns the rule**.

Inside `rwb-document` this is the access and catalog contribution of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- **This is the secondary P5 slice of RWB-E1-016 and it owns no legacy acceptance criterion.** The legacy AC1 to AC11 stay where the split puts them: RWB-P1-E1016-APP carries the data products, the access rows, the records read, the masking of a record, the PII log, the view grants and the catalog content, RWB-P4-E1016-APP carries the roles, the permissions, the masking policy and the data-product half of the authorise answer, and RWB-ITG-E1016-ITG carries the composed entry. The six criteria of section 7 are new under D-RCV-60 and test only the P5 contribution. No legacy criterion text is copied into this file (GAP-1028; ASM-1960).
- The **document data product is DP10**: `document`, `document_field`, `document_custody`, `document_type`, `document_checklist_item`, `case_document_check`, `document_hub_parameter`, `document_intake`, `document_text`, `retention_action` and `retention_rule`, all in `rwb_document` and all P5's under the Ownership Map. The composed catalog entry is served by P1's catalog and P4's role and masking contracts; this service contributes **the retention class of the DP10 entry and the P5 object and field list behind the product**, and nothing else of the entry (GAP-1028; ASM-1961).
- The two document reads of the service are `GET /api/recovery/document/v1/documents/{documentId}` and `GET /api/recovery/document/v1/cases/{caseId}/documents`. Both are authorised through the `rwb-access` `authorise` contract for the Documents right and the DP10 access row, scope-checked through the P3 case contract, masked by role through the P4 masking answer, and every read of personal data is written to the PII access log by the ACE common module. **This package never writes the log** and never holds a role, a permission, an access row or a masking row.
- The retention class is served by the shared shape that RWB-P5-AD021-CON defines and that RWB-P5-E1017-APP also reuses: `RetentionClass` with `classCode`, `labelEn`, `labelTh`, `productCode`, `docTypeCode`, `retentionMonths`, `ageBasisField`, `endAction`, `ruleVersion`, `validFrom` and `validTo`, read through `GET /api/recovery/document/v1/retention-classes` and `GET /api/recovery/document/v1/retention-classes/{classCode}` (12.1). The field-level names of that answer are Not specified in the source documents (GAP-1028; ASM-1965).
- The only ACE facts this service sees arrive through the P1 source-data contract: the `isPersonal` tag of a field and the field metadata (`sys_fields.is_personal` behind it). P5 reads no `recovery.v_ace_*` view, holds no grant on the recovery schema and keeps no copy of a `sys_fields` row (DP-05, DP-01).
- No event is published and none is consumed. Architecture v5 gives this service exactly two events, `DocumentStored` and `DocumentFieldsExtracted` (slides 16, 41 and 43); neither belongs to this slice, and DP-09 is not a pattern of this story.
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-1028; ASM-1966); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.

### 2. Business rationale

Audit findings record staff sending debtor data outside the bank and users holding access they did not need (CTL-11, CTL-09). Legacy RWB-E1-016 answers both inside one data engine: a role reads a data product only through an access row, personal fields are masked by role under PDPA, every read of personal data goes to the PII access log, and one catalog entry per product names its owner, its system of record, its freshness and its retention. The Workbench also holds the recovery document estate, so the document data product is one of the products that answer has to cover, and its retention class - the class of every document type and the rule behind the monthly retention run - is the part of the entry only the document service can state (REQ-RDF-011).

In the target the answer is assembled from its owners, not read from one schema. Architecture v5 slide 41 gives P4 `rwb-access` the Recovery roles as data, the scope, the masking policy and the access log, slide 41 gives P1 `rwb-source-data` the ACE view contract, the data products, the dictionary and the freshness, and slides 16, 41 and 44 give P5 `rwb-document` the document metadata, the custody, the OCR text and fields, the signatures **and the retention**. So the catalog entry a data steward reads is composed of a P1 catalog part, a P4 role and masking part and a P5 retention part, and no service copies another's row. This story builds the P5 part and the rules that make a document read safe: authorised for the Documents right, gated by a DP10 access row, confined to the caller's scope, masked by role, and logged before the answer leaves the service.

The realignment changes the mechanics, not the business rule:

1. **One schema and one base.** `rwb_document` replaces the recovery schema and `/api/recovery/document/v1` replaces the monolith base (DP-01). No table of another service is read and no monolith table name survives in this story.
2. **DP10 ownership.** The eleven document and retention tables are P5's under the Ownership Map, so the document product's object and field list is written by this service and by none other. `data_product`, `data_product_access`, `sys_objects` and `sys_fields` are P1's and are never read here.
3. **The retention-class contribution.** `retention_rule` is P5's (ownership ruling ASM-0076; P1 drops its copy) and `document_type.retention_class` is P5's. The class of the DP10 entry carries the rule version in force, for example `RET-2026.11`, and the class per document type, for example `LEGAL10Y` and `GENERAL05Y`. That is the contribution the ITG suite joins to the P1 entry by product code.
4. **The authorise contract and the guard.** The in-process ACE access check becomes the `POST /api/recovery/access/v1/authorise` contract of `rwb-access` behind the guard library (DP-08, DP-11), one hop with a 2 s timeout and a breaker per downstream. This story writes no guard of its own; it inherits the service template's.
5. **Masking by role from one place.** `FieldMasker` in the same JVM becomes the P4 masking answer: the marker per field ID at the masking version in force, applied to the fields of a document read. A missing row means masked, and with no rule loaded every personal field is masked (DL26).
6. **The PII log path.** The read is logged by the ACE common module (INT-22), as in the legacy story, and a read that cannot be logged returns no personal data: the service answers 503 with MSG-GEN-006 rather than a value. The entry carries the user, the product, the case and the field names, never a value.
7. **The dictionary read instead of the dictionary tables.** The personal tag of a field comes through the P1 source-data contract (DP-05, DP-11) and never from `sys_fields` inside this service or from a `recovery.v_ace_*` view. The boundary statement of BR9 and AC6 keeps that true at the database and in the build.

The story meets REQ-RDF-010 by making the personal fields of a document read maskable by role from one place and refusing a read without the right or the access row, REQ-RDF-011 by serving the retention class that the DP10 entry names, and REQ-ACA-006 by making every read of personal data a logged read with no value in the log.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| rwb-access `POST /api/recovery/access/v1/authorise` (RWB-P4-E1037-CON) | The allowed or refused answer for the Documents right, the product code `DP10`, the case reference and the field list, with the matrix version, the masking version and a marker per field ID (DP-08) |
| rwb-access `GET /api/recovery/access/v1/me/permissions` (RWB-P4-E1037-CON) | The caller's role codes and letters, cached by the guard library |
| rwb-case `GET /api/recovery/case/v1/cases/{caseId}` (RWB-P3-E1018-CON) | The case exists and its owner, team and scope attributes, so the read is confined to the caller's scope; one hop, 2 s timeout (DP-11) |
| rwb-source-data `GET /api/recovery/source-data/v1/admin/data-dictionary/fields` (RWB-P1-E1064-CON) | The `isPersonal` tag and the field metadata (`fieldId`, `entity`, `fieldName`, `sourceSystem`, `sourceField`) of the fields of the document read, so the masking decision is P1's data and not a code list (DP-05). The rwb-document service identity needs the right the operation requires, Reference data R: Pending, owner security architect, tracked as NEW-GAP-F17-3 |
| rwb-case reference-data contract (RWB-P3-E1043-CON, through the RWB-PLT-E1043-CON client library) | `LOV-RETENTION`, `LOV-RETENTION-ACTION` and `LOV-RETENTION-END` with the version in force; no class code and no action code is typed in code (DP-07) |
| Guard library of DP-08 (RWB-PLT-E1037-CON) | The authorisation filter the service template already carries; this story configures it for the two document reads and builds no guard |
| gateway-bff composite route (RWB-PLT-N001-CON) | The route behind SCR-03, which reads this service; the route is not built here (DP-19) |

The story's contract dependency list is None, and none of the four consumed operations above is in it. Each is therefore consumed as a published contract against its fake, and the missing C entries are recorded as a gap and an assumption (GAP-1028; ASM-1963). The same holds for the platform contract stories in column 1: they are build dependencies of the service template and of the P4 service's own stories, not of this slice (GAP-1028; ASM-1964).

Business preconditions carried from RWB-E1-016:

- `data_product_access` version `DPA-2026.11` is in force from 2026-11-20 and holds a read row for role `RW-AUDIT` on product `DP10`. The version in force is P4's answer and P1's table; this service reads neither (ASM-1963).
- Case `RW-2026-000102` exists with borrower person_key `P0000102`, whose ACE customer has identity number `1234567890123` and mobile `0812345678`. The case arrives through the P3 contract; the customer values are synthetic test data and never reach this service in clear.
- No masking rule from Compliance is loaded (DL26). Until the rules load, every personal field is masked for every role.
- The ACE common module PII access logging is available (INT-22), and its failure is a refusal, not a silent read (BR5).
- Data product `DP10` is the document data product of this service. The code is the one the run fixes for the P5 slice and no source names the mapping (GAP-1028; ASM-1967).
- Document type table version `DOCTYPE-2026.11` is in force, with type `DEMAND_LETTER` class `LEGAL10Y` and type `APPRAISAL_REPORT` class `GENERAL05Y` (RWB-P5-E1025-APP owns the load).
- Retention rule version `RET-2026.11` is in force in `retention_rule` with a row for class `LEGAL10Y` and a row for class `GENERAL05Y` (RWB-P5-AD021-APP owns the load; the shape is RWB-P5-AD021-CON's).
- The reference lists arrive through the reference-data contract of `rwb-case` with the version in force; no list value is a Java constant.
- The feature flag of this slice is `rwb.document.access`. Off: the two retention-class reads answer 404 and the two document reads return the feature-off error of the service template, with no partial access, masking or logging path (GAP-1028; ASM-1968).
- The release date 30 November 2026 is tentative and is copied unchanged.

The database login name is Not specified in the source documents (GAP-1028; ASM-1966).

### 4. Flow

1. Caller: opens a document or the case document list, through SCR-03's document panel (the route is RWB-PLT-N001-CON's and the panel is RWB-P5-E1024-APP's), and so reaches `GET /api/recovery/document/v1/documents/{documentId}` or `GET /api/recovery/document/v1/cases/{caseId}/documents`.
2. `DocumentAccessService`: asks the guard library (DP-08) for the `rwb-access` `authorise` answer with the Documents right `R`, the product code `DP10`, the case reference and the field IDs of the requested read. No Documents letter, or no access row in force for one of the caller's roles and `DP10`, is refused before any row is read: 403 with MSG-P4-002 (DP-08, DP-11, one hop, 2 s timeout, breaker per downstream).
3. `DocumentAccessService`: asks the P3 case contract `GET /api/recovery/case/v1/cases/{caseId}` for the case and its scope attributes. A case that does not exist, or that is outside the caller's scope, is answered 404 with MSG-P4-003 and no row is read (DP-11).
4. `DocumentAccessRepository`: reads the `document` rows of the case, or the one `document` row with its `document_field` rows and version list, inside `rwb_document` and by the `rwb-document` login only (DP-01).
5. `DocumentMaskingService`: takes the field IDs of the answer and asks the P4 masking answer for the marker of each, at the masking version in force. A field marked `clear` is returned as stored; a field marked `masked`, or with no row at all, is returned masked (DP-08; BR3, BR4).
6. `DataDictionaryClient`: resolves which of those fields are personal through `GET /api/recovery/source-data/v1/admin/data-dictionary/fields`, queried by `entity` (and `field` where one field is asked) with `page` and `size`; the operation has no field-ID filter, so the client matches `fieldId` in the returned page items and reads `isPersonal` (RWB-P1-E1064-CON; DP-05). The field set sent for masking is the dictionary's and not a list in the code. A field with no dictionary row is treated as personal.
7. `PiiLogClient`: calls the ACE common module to write the read with the user, the product `DP10`, the case and the field names. The write happens before the answer leaves the service; a failure refuses the answer with 503 and MSG-GEN-006 and returns no personal field (BR5).
8. `DocumentAccessController`: returns the masked answer with the document metadata, the extracted fields and the version list, or the `DocumentPage`. No value of a personal field appears in the answer, in the log or in an event payload.
9. Data steward: reads the DP10 retention class with `GET /api/recovery/document/v1/retention-classes?productCode=DP10`, and one class with `GET /api/recovery/document/v1/retention-classes/{classCode}`. The class carries the rule version in force, the class per document type and the owner `P5`. That answer is the P5 contribution to the composed catalog entry: the P1 catalog names the product and its objects and fields, P4 resolves the owner role and the masking, and P5 states the retention. The ITG suite reads the composed entry from the P1 catalog API, resolves roles and masking through P4 and the retention class through P5 (GAP-0341); no service copies another service's table.
10. Nothing is published and nothing is consumed: no outbox row is written, no topic is touched and no workflow is started by this slice.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No `data_product_access` row in force for the caller's roles and product `DP10` | 403; no document row is read; the refusal is written to the access log by the ACE common module | MSG-P4-002 | AC3 |
| X2 | The caller's roles hold no Documents `R` letter | 403 before any document row is read | MSG-P4-002 | AC3, TC-E1-016-09 |
| X3 | The case is outside the caller's scope | 404; no row is read; the refusal is logged | MSG-P4-003 | AC5 |
| X4 | No masking rule is loaded for a personal field | The field is masked for every role | None | AC4 |
| X5 | The PII access log cannot be written | The read is refused with 503; no personal data is returned | MSG-GEN-006 | AC6 |
| X6 | An access row has a valid-from date after today | The row is not in force; the read is refused until that date | MSG-P4-002 | AC7, TC-P5-E1016-APP-09 |
| X7 | A class of the module names a `recovery.v_ace_*` view or a `public.*` table, or the migration holds a foreign key into another schema | The build fails and names the class or the constraint, and a statement that names the object fails at the database with SQLSTATE 42501 | None (build log) | AC6 |
| X8 | The retention class of a document type is not in the rule version in force | The document is listed as exception `RETENTION_CLASS_MISSING` in the review list and no class value is returned for it; the document itself is unchanged | None (review list) | AC1 |
| X9 | The P1 data-dictionary read answers 400, 401, 403 or 503, does not answer within 2 s, or its breaker is open | The read is refused with 503 and no personal field is returned, because the masking decision cannot be made | MSG-GEN-006 | AC4, AC10 |

Two target-service notes:

- MSG-P1-002 and MSG-P1-003 of the legacy story are the reference-load path's messages. The access version and the catalog part are loaded there, which is RWB-P1-E1016-APP's and the P3 reference-loads surface's, so this story names them in section 14 and produces neither.
- A refused read is not retried by the caller: the guard answer and the scope answer are cached per request, and a repeat after the access version changes is answered from the version then in force.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the service template's guard, the four consumed contracts and their fakes, and the class tables it already owns; it creates no table and needs no other story's build |
| Negotiable | The product code, the class codes, the rule version, the field IDs, the masking rows, the access rows and the roles are data rows; the story fixes only the checks and the answer shape |
| Valuable | The DP10 catalog entry gets its retention class from the service that owns the rule, and a document read is authorised, scope-checked, masked and logged on every path |
| Estimable | Two retention-class reads, two document reads behind one access service, one masking resolver, one dictionary client, one log client |
| Small | Fits one sprint as a secondary slice of the legacy key, with no schema change and no event |
| Testable | Each criterion in section 7 is one component or end-to-end test with synthetic fixtures; every failure path of section 5 has one |

### 7. Acceptance criteria

```gherkin
Feature: Access control per data product and catalog entries - the rwb-document contribution

  Background:
    Given data product access version "DPA-2026.11" is in force from 2026-11-20
    Given case "RW-2026-000102" has borrower person_key "P0000102" whose ACE customer has identity number "1234567890123" and mobile "0812345678"
    Given no masking rule from Compliance is loaded for the personal fields of a document read
    Given data product "DP10" is the document data product and its tables are document, document_field, document_custody, document_type, document_checklist_item, case_document_check, document_hub_parameter, document_intake, document_text, retention_action and retention_rule
    Given document type table version "DOCTYPE-2026.11" is in force, type "DEMAND_LETTER" carries retention class "LEGAL10Y" and type "APPRAISAL_REPORT" carries retention class "GENERAL05Y"
    Given retention rule version "RET-2026.11" is in force with a row for class "LEGAL10Y" and a row for class "GENERAL05Y"
    Given the rwb-access contract mock answers the Documents right and the DP10 access rows of the roles named below
    Given the rwb-case contract mock returns case "RW-2026-000102" in the caller's scope unless the scenario says otherwise
    Given the rwb-source-data data-dictionary contract mock tags first_name, last_name, cif_no, date_of_birth and the contact value as personal

  Scenario: AC1 The DP10 retention class is served by rwb-document (new, D-RCV-60)
    Given a data steward holds RW-DATASTEW with read on product "DP10"
    When the data steward calls GET /api/recovery/document/v1/retention-classes?productCode=DP10
    Then the answer is 200 with a RetentionClassPage of the classes of product "DP10" at rule version "RET-2026.11"
    And each class carries classCode, labelEn, labelTh, productCode, docTypeCode, retentionMonths, ageBasisField, endAction, ruleVersion, validFrom and validTo
    And class "LEGAL10Y" names document type "DEMAND_LETTER" and class "GENERAL05Y" names document type "APPRAISAL_REPORT"
    And every class names owner "P5" and the answer holds no copy of a data_product, data_product_access or sys_fields row
    When the data steward calls GET /api/recovery/document/v1/retention-classes/LEGAL10Y
    Then the answer is the same class "LEGAL10Y" with ruleVersion "RET-2026.11"
    When the data steward calls the same read with a class code that is not in the rule version in force
    Then the call is refused with status 404 and no class is returned
    And the ITG suite joins the answer to the P1 DP10 entry by productCode "DP10" and finds the same classCode

  Scenario: AC2 A document read is authorised, masked and logged (new, D-RCV-60)
    Given user "u-audit-01" holds read-only role RW-AUDIT, whose Documents letters are "R", with an access row in force for product "DP10"
    Given the demand letter of type "DEMAND_LETTER" is stored on case "RW-2026-000102" with document ID "DOC-0102-01"
    When the user calls GET /api/recovery/document/v1/documents/DOC-0102-01
    Then the answer is 200 with the document metadata, the extracted fields and the version list
    And "rwb-access" was asked once for the Documents right "R", productCode "DP10" and caseId "RW-2026-000102"
    And the PII access log holds one entry with user "u-audit-01", product "DP10", case "RW-2026-000102" and the field names of the read
    And no log entry, no response field and no event payload holds a field value
    And no table of "rwb-access", "rwb-case" or "rwb-source-data" is read by the rwb-document login

  Scenario: AC3 A role without a DP10 access row is refused (new, D-RCV-60)
    Given user "u-phone-01" holds RW-PHONECOL, which has an access row for no product "DP10"
    When the user calls GET /api/recovery/document/v1/cases/RW-2026-000102/documents
    Then the system refuses the call with status 403 and MSG-P4-002
    And no document row, no extracted field and no retention class is read
    And the ACE common module writes the refusal to the access log with user "u-phone-01" and product "DP10"
    And the refusal carries no case fact and no field value

  Scenario: AC4 With no masking rule loaded every personal field is masked (new, D-RCV-60)
    Given user "u-comply-01" holds RW-COMPLY, whose Documents letters are "R", with an access row in force for product "DP10"
    Given the demand letter holds the extracted fields first_name, last_name, cif_no, date_of_birth, the contact value, id_no_masked and id_no_last4
    When the user calls GET /api/recovery/document/v1/documents/DOC-0102-01
    Then first_name, last_name, cif_no, date_of_birth and the contact value are returned masked
    And the identity number is returned only as id_no_masked and id_no_last4
    And each masked field is masked because the "rwb-access" answer carries the marker "masked" or no row for it at the masking version in force
    And no response field holds "1234567890123" and no response field holds "0812345678"

  Scenario: AC5 A case outside the caller's scope answers 404 (new, D-RCV-60)
    Given user "u-owner-07" holds RW-CASEOWN with scope Own and an access row in force for product "DP10", and does not own case "RW-2026-000102"
    When the user calls GET /api/recovery/document/v1/documents/DOC-0102-01
    Then the system refuses the call with status 404 and MSG-P4-003
    And the service reads no document row, no document_field row and no retention_rule row
    And no metadata, no field and no class is returned
    When the same user calls GET /api/recovery/document/v1/cases/RW-2026-000102/documents
    Then that call is also refused with status 404 and MSG-P4-003

  Scenario: AC6 The boundary holds and a read that cannot be logged returns no personal data (new, D-RCV-60)
    Given the rwb-document login and the rwb-source-data data-dictionary contract fake, which lists the 30 views of schema "recovery" as P1 objects
    When the boundary test of the module runs
    Then no class of `th.co.scb.ace.workbench.recovery.document.access` names "recovery.v_ace_customer" or any other "recovery.v_ace_*" view
    And no class of the module names a "public" table, and the migration of "rwb_document" holds no foreign key into another service's schema
    And a session as the rwb-document login that selects from "recovery.v_ace_customer" fails with SQLSTATE 42501
    And the test passes for every class of the module and for every one of the 30 views
    Given the PII access log rejects every write
    When user "u-audit-01" calls GET /api/recovery/document/v1/documents/DOC-0102-01
    Then the system refuses the call with status 503 and MSG-GEN-006 for system "PII access log"
    And the system returns no personal field

  Scenario: AC7 An access row valid from a later date is refused until that date (new, D-RCV-60)
    Given the access row of product "DP10" for role RW-AUDIT has a valid-from date of 2026-12-15
    Given the test clock is 2026-12-14
    When user "u-audit-01" calls GET /api/recovery/document/v1/documents/DOC-0102-01
    Then the system refuses the call with status 403 and MSG-P4-002
    And no document row and no field value is returned
    When the test clock is 2026-12-15 and user "u-audit-01" calls the same read
    Then the answer is 200 with the document metadata

  Scenario: AC8 The identity number is never tokenized and each field comes from the contract (new, D-RCV-60)
    Given user "u-comply-01" holds RW-COMPLY, whose Documents letters are "R", with an access row in force for product "DP10"
    When the user calls GET /api/recovery/document/v1/documents/DOC-0102-01
    Then no token and no detokenization call is made on the read path
    And the value and the personal tag of each field come from the rwb-source-data contract fake
    And no "recovery.v_ace_*" view is read by the rwb-document login

  Scenario: AC9 A call without a valid login is refused with 401 (new, D-RCV-60)
    Given no valid login is presented with the call
    When the caller calls GET /api/recovery/document/v1/documents/DOC-0102-01
    Then the system refuses the call with status 401
    And no document row, no field value and no retention class is returned
    When the caller calls GET /api/recovery/document/v1/retention-classes?productCode=DP10
    Then the system refuses the call with status 401
    And the same 401 is returned by GET /api/recovery/document/v1/cases/RW-2026-000102/documents

  Scenario: AC10 A dictionary read that is refused or fails refuses the document read (new, RD-P1-021)
    Given the RWB-P1-E1064-CON fake answers GET /api/recovery/source-data/v1/admin/data-dictionary/fields with 403 MSG-P4-002
    When user "u-audit-01" reads a document of case "RW-2026-000102"
    Then the answer is 503 with messageCode "MSG-GEN-006" and a traceId, and no personal field is returned
    And the same holds for a 503 answer and for no answer within 2 s
```

The criteria AC1 to AC10 are new and test only the P5 delivery: the DP10 retention-class contribution, the authorised, scope-checked read, the access-row refusal, the masking rule, the scope refusal, the boundary and log path, the source-access and no-tokenization rules and the login refusal. The legacy criteria of RWB-E1-016 are owned by RWB-P1-E1016-APP, RWB-P4-E1016-APP and RWB-ITG-E1016-ITG and are not restated here (GAP-1028; ASM-1960).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A role reads a document only through a `data_product_access` row in force for that role and product `DP10`; the row is P1's table and arrives in the P4 answer, and an absent or not-yet-in-force row is a refusal | REQ-RDF-010; legacy BR1; FEAT-RDF-15 |
| BR2 | A document read needs the Documents `R` right in the caller's roles, checked before any row is read | REQ-RDF-010; TSD P5 T6.1; legacy section 4 step 2 |
| BR3 | A personal field is masked unless the masking rule lets the role see it; the decision is the P4 marker at the masking version in force and this service applies it and never decides it | CTL-11; `masking_rule`; NFR-039; DL26 |
| BR4 | With no masking rule loaded, every personal field stays masked | DL26 ("Masking rules load with no values") |
| BR5 | Every read of personal data is written to the PII access log with the user, the product, the case and the field names; a read that cannot be logged is refused and returns no personal field | REQ-ACA-006; CTL-11; legacy BR4 |
| BR6 | A document of a case outside the caller's scope is refused with 404 and no row is read | CTL-09; legacy BR5 |
| BR7 | The retention class of the DP10 entry is P5's: `retention_rule` and `document_type.retention_class` live in `rwb_document` and are served by the retention-class reads; no service keeps a second copy of the class | REQ-RDF-011; Ownership Map (P5 `retention_rule`); legacy BR7; ASM-0076 |
| BR8 | Source access is the owner's contract: the value and the personal tag of a field come from the P1 source-data contract and from the case contract, and this service reads no ACE view and no other service's table | D-RCV-35 U4; ADR-010; legacy BR8; DP-05; DP-01 |
| BR9 | `rwb_document` holds no grant on the `recovery` schema and no foreign key into another schema, and no class of the module names a `recovery.v_ace_*` view or a `public` table; the build and the database both refuse one | D-RCV-35 U4; ADR-010; DP-01; legacy BR8 |
| BR10 | There is no tokenization in this path: the identity number exists only as `id_no_masked` and `id_no_last4`, no response field carries the clear value, and no token or detokenization call exists | ADR-010; Data Tier Map section 7; DL26; legacy BR9 |
| BR11 | Each data product has one catalog entry; this service contributes exactly its retention class and the P5 object and field list behind product `DP10`, and no other part of the entry | REQ-RDF-011; legacy BR7 and BR10; ASM-0076 |
| BR12 | No cross-schema read and no cross-schema write: every statement of the module names `rwb_document` only, and the role, access, dictionary and case data of other services arrive through their contracts | DP-01; DP-11; legacy BR8 |

DL26 is open. Its assumptions ASM-0247, ASM-0264, ASM-0275 and ASM-0355 are confirmed by the directive of 26 November 2026, and BR3 and BR4 build on them as stated.

Target-service statements that make the rules hold in `rwb-document`:

- BR1 and BR2 are executed by the guard library of DP-08 before the controller body: the authorise answer is requested with the Documents right, `DP10` and the case reference, and a refused answer becomes 403 with MSG-P4-002. The service reads no `data_product_access`, `permission`, `role` or `masking_rule` row.
- BR3, BR4 and BR10 are executed by `DocumentMaskingService`: the marker of each field ID is taken from the P4 answer, a missing row is `masked`, and the identity number only ever exists as the two masked dictionary fields. No rendering and no last four digits are computed here.
- BR5 is executed by `PiiLogClient` calling the ACE common module before the answer is written; the client carries field names, the user, the product and the case, and the failure path is the 503 of AC6.
- BR6 is executed by the case contract read and the scope test that the guard passes to it; the service holds no case row and no scope table.
- BR7 is executed in `rwb_document`: the class rows of `retention_rule` in the rule version in force plus the class of each `document_type`, joined by `product_code` and `doc_type_code`, with no P1 copy.
- BR8, BR9 and BR12 are executed by the boundary rule and by the login: the module names no `recovery` object, the migration holds no foreign key across a schema, and a statement that names one fails with SQLSTATE 42501.
- BR11 is executed by serving only the class reads from this service; the catalog entry, the owner role, the access rows and the PDPA tags are read from P1 and P4 by the caller, never assembled or copied here.

### 9. State transitions

None. This story does not change a case status and does not change the document record state: a read of a document, a class or a case list writes no `document` row and no `document.state` value.

Two statements stand in place of a state table:

- The version in force of `data_product_access`, of the matrix, of the masking policy and of `retention_rule` moves only when an approved load reaches its valid-from date. The load is the reference-load path's and RWB-P5-AD021-APP's; this story reads the version in force and writes none of it. The approved load arrives as reference data for table code data_product_access through the rwb-case reference-data contract; this service exposes no load endpoint of its own (GAP-0483).
- A read leaves the access log with one entry and the document tables unchanged. The only state this story observes is the outcome of the permission test, the access-row test, the scope test and the masking test, which is an answer, not a transition.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Reads the DP10 retention class through `GET /retention-classes` and the case's documents through the two document reads; owns the class rows through the type table and the rule load, not here |
| RW-REFADM, reference data administrator | Submits a retention-rule or access version through the reference-loads surface of P3 (Reference data C); that surface is not built here |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules (DL26); reads the class and the masked document |
| RW-SECADM, security administrator | Owns the role to permission matrix; reads the access log |
| RW-COE, RW-AUDIT, RW-PLATADM | Read the class through the retention-class reads |
| Roles with Documents `R` and a DP10 access row, for example RW-CASEOWN, RW-AUDIT, RW-COMPLY | Read a document, its fields and the case document list, for a case in scope |
| The rwb-document service identity | Reads and writes its own tables only, and calls the authorise, case, dictionary and PII-log interfaces as itself |
| Nobody | Writes a PII log entry, a role row, a permission row, an access row or a masking row through this service |

The refusal shape is the shared Problem body (RFC 9457; RD-P1-004) with `messageCode` set to MSG-P4-002 or MSG-P4-003, a `traceId` and the detail naming the action and never a case fact or a field value. The database login is the per-service login of DP-02, named here as "the rwb-document login (DP-02)" and Not specified in the source documents (GAP-1028; ASM-1966).

### 11. Data

| BR Field ID | Table or contract | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 to DF-DOC-011 | `document` in `rwb_document` | id, case_id, party_id, document_type, source, storage_ref, classification_confidence, review_status, retention_class, write_once, doc_version | Read |
| DF-DOC-025 | `document` in `rwb_document` | previous_version_id | Read |
| DF-DOC-026 | `document` in `rwb_document` | content_sha256 | Read |
| DF-DOC-012 to DF-DOC-017 | `document_field` in `rwb_document` | id, document_id, field_name, field_value, confidence, confirmed_by | Read |
| Standard columns | `document`, `document_field` | state, is_active, version, created_at, created_by, updated_at, updated_by | Read |
| DF-REF-219 | `document_type` in `rwb_document` | doc_type_code | Read |
| DF-REF-223 | `document_type` in `rwb_document` | retention_class | Read |
| DF-REF-229 | `document_type` in `rwb_document` | table_version | Read |
| DF-REF-116 to DF-REF-126 | `retention_rule` in `rwb_document` | id, product_code, table_name, record_class, retention_months, age_basis_field, end_action, rule_version, valid_from, valid_to, approved_by | Read |
| DF-REF-097 | P1 `sys_fields`, through `GET /api/recovery/source-data/v1/admin/data-dictionary/fields` | field_name | Read through the contract; no row is copied |
| DF-REF-103 | P1 `sys_fields`, through the same contract | source_system | Read through the contract; no row is copied |
| DF-REF-105 | P1 `sys_fields`, through the same contract | is_personal (`isPersonal` on the wire) | Read through the contract; no row is copied |
| DF-REF-199 | P4 `masking_rule`, through `POST /api/recovery/access/v1/authorise` | role_code | Read through the contract; no row is copied |
| DF-REF-200 | P4 `masking_rule`, through the same contract | field_id | Read through the contract; no row is copied |
| DF-REF-201 | P4 `masking_rule`, through the same contract | unmasked | Read through the contract; the marker is the answer |
| DF-CAS-001 | P3 case, through `GET /api/recovery/case/v1/cases/{caseId}` | id | Read through the contract |
| DF-CAS-002 | P3 case, through the same contract | case_no | Read through the contract |
| DF-CAS-020 | P3 case, through the same contract | legal_hold | Read through the contract for the retention answer; this story asserts no hold |
| DF-REF-080 to DF-REF-086 | P1 `data_product_access` | the access row of the read | Not read and not written: it arrives in the P4 answer (BR1) |

Field IDs are those in the Logical Data Model and Data Dictionary v9 and the TSD P5 T3.1 tables. No `rwb_access`, `rwb_case`, `rwb_source_data` or `recovery` row is read by this service, and no `recovery.v_ace_*` view is named by any class. The personal values of a document read are field values that never enter a log, an event, a workflow input or a test prompt; the fixtures of sections 7 and 16 are synthetic.

The fields tagged personal are those P1 returns with `isPersonal` true at read time: first_name, last_name, cif_no, date_of_birth, the contact value and the identity number, which is read only as id_no_masked and id_no_last4. This service declares no field of its own tables as personal; the tag is the contract's answer at read time, not a copy.

### 12. Contract

#### 12.1 REST operations provided

All on base `/api/recovery/document/v1`.

| Method | Path | Owner | Notes |
|---|---|---|---|
| GET | `/retention-classes` | P5 | The classes of a product at the rule version in force; query `productCode`, `docTypeCode`, `page`, `size`; answer `RetentionClassPage`. Access: any authenticated caller with a Workbench role and read on `DP10` (DP-08) |
| GET | `/retention-classes/{classCode}` | P5 | One class by code with the rule version in force; answer `RetentionClass`; 404 when the code is not in the version in force |
| GET | `/documents/{documentId}` | P5 | The document metadata, the extracted fields and the version list; Documents `R`, a DP10 access row and the case in scope; masked by role; each read logged (AC2, AC4) |
| GET | `/cases/{caseId}/documents` | P5 | The document list of a case; documents `R`, a DP10 access row and the case in scope; masked by field; each read logged (AC3, AC5) |

The `RetentionClass` and `RetentionClassPage` shapes are the shared shape of RWB-P5-AD021-CON: `classCode`, `labelEn`, `labelTh`, `productCode`, `docTypeCode`, `retentionMonths`, `ageBasisField`, `endAction`, `ruleVersion`, `validFrom` and `validTo`. The same shape file names `GET /documents/{documentId}/retention` and its `DocumentRetention` answer (`documentId`, `retentionClass`, `expiryDate`, `state`, `legalHold`, `legalHoldRef`, `lastAction`); this story reuses the shape and leaves that read to RWB-P5-AD021-APP, so the shape exists once and the two stories do not define it twice. The field-level names of the two class operations are Not specified in the source documents (GAP-1028; ASM-1965), and the operation path itself is not named in the sources either (GAP-1028; ASM-1962).

The `Document` answer is the Document shape of TSD P5 T-A.2 (id, caseId, partyId, documentType, source, storageRef, classificationConfidence, reviewStatus, retentionClass, writeOnce, docVersion), extended with the stored date, the previous version, the version list and the extracted fields. Errors use the shared Problem body (RFC 9457 with `messageCode` and `traceId`; RD-P1-004).

#### 12.2 REST operations consumed

| Operation | Owner | Story | Note |
|---|---|---|---|
| POST `/api/recovery/access/v1/authorise` | P4 rwb-access | RWB-P4-E1037-CON | The Documents right, the product code `DP10`, the case reference and the field IDs; the answer carries allowed or refused, the matrix version, the masking version and a marker per field ID. One hop, 2 s timeout, breaker (DP-08, DP-11) |
| GET `/api/recovery/access/v1/me/permissions` | P4 rwb-access | RWB-P4-E1037-CON | The caller's role codes and letters, cached by the guard library |
| GET `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | RWB-P3-E1018-CON | The case and its scope attributes; 404 when the case is absent or out of scope (DP-11) |
| GET `/api/recovery/source-data/v1/admin/data-dictionary/fields` | P1 rwb-source-data | RWB-P1-E1064-CON | Query `product`, `entity`, `field`, `sourceSystem`, `page`, `size`; answers `DataDictionaryFieldPage`; the `isPersonal` tag and the field metadata that decide which fields are sent for masking (DP-05). 200, 400, 401, 403, 503 |

All four are consumed as published contracts with their fakes, because this slice's contract dependency list is None (GAP-1028; ASM-1963). The reference lists `LOV-RETENTION`, `LOV-RETENTION-ACTION` and `LOV-RETENTION-END` are not REST operations of this story: they arrive through the `rwb-case` reference-data client library (DP-07, RWB-P3-E1043-CON under RWB-PLT-E1043-CON).

#### 12.3 Events published

None. DP-09 is not a pattern of this story, so this slice writes no outbox row and adds no topic. The service's two events are `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` (Arch v5 slides 16, 41 and 43); neither belongs to a read of a document or of a class.

#### 12.4 Events consumed

None. The class is read from `retention_rule` and `document_type` on each call, and the access, scope and masking answers are synchronous. No topic is consumed by this slice.

#### 12.5 Workflows and activities

None. All four operations are synchronous REST answers in the caller's thread. The retention Schedule (legacy JOB-17) and `DocumentIntakeWorkflow` belong to RWB-P5-E1017-APP and RWB-P5-E1024-APP; this story registers no activity on the `rwb-document` queue.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story; the monthly retention run is JOB-17 and is RWB-P5-E1017-APP's.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 (`rwb_document`) | Read only: the metadata, the version rows and the retention class of a document |
| `document_field` | P5 (`rwb_document`) | Read only: the extracted fields that carry the personal field IDs |
| `document_type` | P5 (`rwb_document`) | Read only: the class and the version of each document type (RWB-P5-E1025-APP owns the load) |
| `retention_rule` | P5 (`rwb_document`) | Read only: the rule rows of the version in force, the class codes and the period |

No table of another schema is read (DP-01): `role`, `permission`, `masking_rule` and `delegation_limit` are P4's, `data_product`, `data_product_access`, `sys_objects` and `sys_fields` are P1's, `recovery_case` and `case_party` are P3's, `decision_log_entry` is P7's. The other seven tables of product DP10 (`document_custody`, `document_checklist_item`, `case_document_check`, `document_hub_parameter`, `document_intake`, `document_text`, `retention_action`) are P5's and behind the product, but this story reads none of them.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-access authorise fake | RWB-P4-E1037-CON | An allowed Documents `R` with a DP10 row, a refused right, a refused access row, a row not yet in force, and a marker per field ID |
| rwb-access permissions fake | RWB-P4-E1037-CON | The caller's role codes and letters for the guard |
| rwb-case case fake | RWB-P3-E1018-CON | Case `RW-2026-000102` in scope, another owner's case out of scope, a case that does not exist, and the 2 s timeout |
| rwb-source-data data-dictionary fake | RWB-P1-E1064-CON | `isPersonal` true for first_name, last_name, cif_no, date_of_birth and the contact value; the identity number as `id_no_masked` and `id_no_last4` only; 403, 503 and a timeout for X9 |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | `LOV-RETENTION`, `LOV-RETENTION-ACTION` and `LOV-RETENTION-END` with the version in force (DP-07) |
| PII log stub | ACE common module (INT-22) | The write of a read, and the stub that rejects every write for AC6 |

The request and answer field names of the four consumed contracts are taken as published by their owners and are not restated here; the field-level names of the two class operations are the ones section 12.1 fixes (GAP-1028; ASM-1965).

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 4, consumed 4 | The two class reads and the two document reads; the authorise and permissions reads of P4, the case read of P3 and the dictionary read of P1 |
| Kafka | Published 0, consumed 0 | DP-09 is not applied; the two service events belong to other stories |
| Temporal | 0 workflows, 0 activities | JOB-17 and `DocumentIntakeWorkflow` are other stories' |
| File | None | A document read returns metadata and fields, not content; the content read is RWB-P5-E1024-APP's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/access`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DocumentAccessController` (or the existing document controller with the guard) | Controller | The two document reads with the access check, the scope check and the error mapping to the shared Problem body with `messageCode` |
| `RetentionClassController` | Controller | `GET /retention-classes` and `GET /retention-classes/{classCode}`: validation of `productCode`, `docTypeCode`, `page` and `size`, and the 404 of a code outside the version in force |
| `RetentionClassReader` | Repository and service | Reads `retention_rule` and `document_type` in the version in force and composes `RetentionClass` and `RetentionClassPage`; read-only |
| `DocumentAccessService` | Service | The order of the checks: authorise answer, scope answer, then the row read; the refusal shapes of MSG-P4-002 and MSG-P4-003 |
| `DocumentMaskingService` | Service | Applies the marker per field ID from the P4 answer; no row means masked; never computes a rendering |
| `DataDictionaryClient` | Client | Calls `GET /admin/data-dictionary/fields` of P1 (RWB-P1-E1064-CON) for the `isPersonal` tag and the metadata of the fields of the answer, by `entity` with paging; cached, one hop, 2 s timeout |
| `PiiLogClient` | Client | Calls the ACE common module to write the read with user, product, case and field names; called, never reimplemented; a failure is the 503 of X5 |
| `AccessLogRefusal` | Service | Hands the refusal of a read to the ACE common module so the refusal is logged with no case fact and no value |

**Database.**

- This story creates no table and owns no Flyway version of its own. `document`, `document_field`, `document_type` and `retention_rule` are created by the document baseline (RWB-P5-E1024-APP and RWB-P5-E1025-APP) and the retention load (RWB-P5-AD021-APP) in the per-service sequence of DP-15, and this story reads them through its repository.
- No write statement exists in `RetentionClassReader` or in the document read path: the reader exposes no save, update or delete, so a class read and a document read can never change a row.
- If SIT needs an index that the creating story does not hold, it is added to that story's migration, not to a new one here. The read predicates are `product_code`, `doc_type_code`, `rule_version`, `valid_from` and `valid_to` for the class, and the document ID or the case ID for the read.

**Configuration and reference data.**

- The rule version in force is read from `valid_from` and `valid_to`; the SIT version is `RET-2026.11`, the label the sources carry. No production label is fixed by this story.
- The class codes `LEGAL10Y` and `GENERAL05Y` are data rows of `retention_rule` and `document_type`; no class code, action code, product code or field ID is a constant in Java.
- `LOV-RETENTION`, `LOV-RETENTION-ACTION` (`ARCHIVED`, `LISTED`, `HELD`, `EXCEPTION`, TSD P5 T3.2) and `LOV-RETENTION-END` are read through the `rwb-case` reference-data contract with the version in force (DP-07).
- Feature flag `rwb.document.access`, assumed (GAP-1028; ASM-1968). Off: the two class reads answer 404 and the two document reads return the feature-off error of the template, with no partial access, masking or logging path.

**Build steps**

1. `RetentionClassReader` and the two class operations over `retention_rule` and `document_type` in the rule version in force, with a test on a boundary date between two rule versions and the 404 of AC1.
2. `DocumentAccessService` with the order of the checks and the two refusal shapes; tests for AC3, AC5 and X6 against the P4 and P3 fakes.
3. `DocumentMaskingService` and `DataDictionaryClient`, with the marker per field ID, the no-row default and the refusal and timeout paths of X9; tests for AC4 and AC10.
4. `PiiLogClient` and the refusal of a read that cannot be logged, with the field-names-only assertion; tests for AC2 and AC6.
5. The boundary test of AC6: no class names a `recovery.v_ace_*` view or a `public` table, no foreign key crosses a schema, and the login fails on `recovery.v_ace_customer` with SQLSTATE 42501.
6. The guard wiring for the two document reads on the service template's filter (DP-08), with the cached permissions read; no guard code is written by this story (GAP-1028; ASM-1964).
7. A contract-fake run of all four operations, so the slice builds on Day 1 before the P1, P3 and P4 stories are live, and a check that the fragment and the story name the same four operations.

**Pattern application**

| DP | Legacy marker in RWB-E1-016 | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` and the recovery schema read in the flow | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-05 | AceSourceQuery, `v_ace_*`, `sys_fields` and `sys_objects` read for the personal tag | Read through rwb-source-data's contract or the service's own ACE views; this service reads no view and uses the contract | none |
| DP-07 | Reference data and LOV behind the class | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard and the capability check | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call and the published interfaces `CaseScopeQuery`, `FieldMasker`, `DataProductAccessLoader` | REST contract with mock; one hop; 2 s timeout | C RWB-P3-E1018-CON; C RWB-P4-E1037-CON |
| DP-19 | Screen and the case record view behind the entry | gateway-bff composite route | H RWB-PLT-N001-CON |

The right-hand column is the dependency row of §R5.5 and it names the platform contract stories that the libraries and the guard carry in wave 0. **This slice adds none of them**: its dependency rows are None, the guard and the libraries are already build dependencies of the service template and of the P4 service's own stories, and the gateway route is behind SCR-03, which this story does not build (GAP-1028; ASM-1964).

DP-01 moves the eleven document and retention tables into `rwb_document` and removes every cross-module read. DP-05 turns the direct `sys_fields` and `v_ace_*` read into the P1 contract, which is also why this service holds no grant on the `recovery` schema. DP-08 replaces the in-process `RecoveryAccessGuard` with one authorise contract and the template's filter. DP-11 replaces the three in-process interfaces of the legacy flow with three REST contracts and their fakes. DP-07 keeps the class and action lists in reference data, and DP-19 is the route the screen uses to reach the document panel.

**Done when.** The tests in section 16 pass; `GET /retention-classes?productCode=DP10` returns the classes of `RET-2026.11` with the owner `P5`; the two document reads are refused with MSG-P4-002 without a DP10 row and with MSG-P4-003 out of scope, masked for every personal field with no rule loaded, and logged by the ACE common module on every read; the boundary test passes for the module and for the login; and the build is green against the four contract fakes with no table of another service named.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-002 | No Documents right, or no DP10 access row in force, or a row whose valid-from date is after today | You cannot {action} here. Your role does not include it. | This story, on the two document reads |
| MSG-P4-003 | The case is absent or outside the caller's scope | This case is not in your scope. | This story, on the two document reads |
| MSG-GEN-001 | A required query field is empty, or `productCode` is not one of DP01 to DP14, or `size` is above the page limit | Enter {field}. | This story, on the two class reads |
| MSG-GEN-006 | The PII access log, the data-dictionary contract or the case contract does not answer | {system} is not available. Try again in a few minutes. | This story, on the two document reads |
| MSG-P1-002 | An access or class load is refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. | The P1 reference-load path (RWB-P1-E1016-APP) and the P3 reference-loads surface; named here, not produced here |
| MSG-P1-003 | A catalog load marks a view with a system of record other than ACE | {product} must have exactly one system of record and one named owner. | P1's catalog load (RWB-P1-E1016-APP); named here, not produced here |

No new message ID is created by this story, and every wording above is the legacy wording unchanged except MSG-P1-003, whose text is copied from the Error and Message Standard v4 (CG-ALL-5755). The HTTP mapping follows the legacy contract: 403 for MSG-P4-002, 404 for MSG-P4-003, 422 for MSG-GEN-001 on a malformed or unknown query value, and 503 for MSG-GEN-006. Thai text for each message follows decision DL10. DL10 is open. Its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the directive of 26 November 2026, and the Thai text follows them as stated.

Delivery shape: every error is an RFC 9457 problem response in the shared Problem body (RD-P1-004) with `messageCode` set to the ID above, a `traceId`, `title` naming the class of failure, `detail` carrying the text with its placeholders filled, and `instance` naming the request (Arch v5 slide 11). For MSG-GEN-006 the `{system}` value is "PII access log", "Source data service" or "Case service"; for MSG-P4-002 the `{action}` value is "read this document" or "read the documents of this case" and never a case fact or a field value. The masking marker and the class answer are answer values, not messages.

This story draws no screen. The empty, loading, error and no-access states of SCR-03 and SCR-47 are rendered by the screens they belong to and are not produced here; this story supplies the refusals of sections 5 and 14 (403 MSG-P4-002, 404 MSG-P4-003, 503 MSG-GEN-006) that those states depend on.

### 15. Screens and states

No screen is built by this story. States of SCR-03: loading, as Screen Specifications v1 gives it; empty, error and no access, Not specified in the source documents (CG-ALL-5761).

| Screen | Mode | Where it is |
|---|---|---|
| SCR-03 Case record | Read only | Shows the product data the role may read, with the personal fields masked, which is the rule AC4 applies; the document detail panel opened from it is RWB-P5-E1024-APP's, and the case record itself is RWB-P3-E1018-APP's |
| SCR-47 Personal data | Epic 8 | The masking rules and versions, and the personal field register; out of scope for this story. States: loading, as Screen Specifications v1 gives it; empty, error and no access, Not specified in the source documents (CG-ALL-5762) |

The class answer is an API read for the data steward, the auditors and the ITG suite; no screen of this story shows it. The route behind SCR-03 is the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), which calls this service once and never chains a call. The field-level rendering of a masked field belongs to the screen owner: this story returns a masked value and a marker and never a rendering rule.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1016-APP-02 | AC2, AC4, BR1, BR2, BR3, BR4, BR5 (legacy AC1) | End to end | RW-AUDIT; case RW-2026-000102; synthetic customer P0000102 with identity 1234567890123 and mobile 0812345678; no masking rule loaded |
| TC-P5-E1016-APP-03 | AC1, BR7, BR11 (legacy AC2) | End to end | The DP10 class contribution; the DP01 entry, its six views and `account_ext` and DF-ACE-018 are P1's; access rows are P4's |
| TC-P5-E1016-APP-04 | AC3, BR1 (legacy AC3) | End to end | RW-PHONECOL; product DP10 with no access row |
| TC-P5-E1016-APP-05 | BR1, BR7 (legacy AC4) | End to end | The refused access load is P1's reference-load path; here `DPA-2026.11` stays the version in force and the class version is unchanged |
| TC-P5-E1016-APP-06 | AC5, BR6 (legacy AC5) | End to end | RW-CASEOWN with scope Own; case RW-2026-000102 owned by another user |
| TC-P5-E1016-APP-07 | AC4, BR4 (legacy AC6) | End to end | RW-COMPLY; no masking rules loaded |
| TC-P5-E1016-APP-08 | AC6, BR5 (legacy AC7) | End to end | PII access log stub rejecting every write |
| TC-P5-E1016-APP-09 | AC3, AC7, BR1 (legacy AC8) | End to end | Access row valid from 2026-12-15; test clock 2026-12-14 |
| TC-E1-016-09 | AC3, BR2 (legacy Access) | Component | RW-TRIBE calls the two document reads; refused with MSG-P4-002; the catalog call of the legacy case is P1's |
| TC-E1-016-10 | AC6, BR9, BR12 (legacy AC9) | Component | The rwb-document login; SELECT on `recovery.v_ace_customer` and on `public.customer` refused with SQLSTATE 42501; the 30 views and their grants are P1's |
| TC-P5-E1016-APP-01 | AC1, BR7, BR11 (legacy AC10) | End to end | The DP10 classes joined to the P1 DP10 entry by product code; the 30 view rows and the dictionary baseline of at least 123 objects and 1,379 fields are P1's |
| TC-E1-016-12 | BR11 (legacy AC11); run by RWB-P1-E1016-APP | End to end | The catalog load that sets `v_ace_customer` to Workbench is refused by P1; here the DP10 class the load does not touch is unchanged |
| TC-E1-016-13 | AC1, AC2, AC3, BR1, BR2 (contract test of section 12 operations, events and activities) | Contract | The section 12.8 contract fakes; the operations, events and activities of section 12 |
| TC-E1-016-14 | BR9, BR12 (boundary test of the section 12.7 tables) | Component | The four tables of section 12.7 in `rwb_document`; a read or write against a table of another schema is refused |
| TC-E1-016-15 | AC4, AC8, BR10 (no tokenization) | End to end | RW-COMPLY; identity 1234567890123; no token or detokenization call in the path |
| TC-E1-016-16 | AC6, AC8, BR8 (source access through the contract) | Component | The rwb-source-data data-dictionary contract fake; the value and the personal tag come from the contract and no ACE view is read |
| TC-E1-016-17 | AC9 (401 without a valid login) | Component | The three reads of documents, classes and case documents called with no valid login |

AC10: TC: TC-P5-E1016-APP-01 (Test Cases v9). The data of TC-P5-E1016-APP-01 changes to the RD-P1-025 counts: TC: to be updated in Test Cases v9 (W2-tests).

The twelve test cases are the legacy test cases of RWB-E1-016 in the legacy order, with the slice of behaviour this story answers named in the Covers column. TC-E1-016-13 to TC-E1-016-17 are added by this story under D-RCV-60 and are not legacy cases: TC-E1-016-13 is the contract test of section 12, TC-E1-016-14 the boundary test of the section 12.7 tables, TC-E1-016-15 the no-tokenization rule of BR10, TC-E1-016-16 the source access rule of BR8 and TC-E1-016-17 the login refusal of AC9. Every case is a test of this service's contribution only: TC-P5-E1016-APP-02 runs the authorised read and the logging rule end to end on the composed path, TC-P5-E1016-APP-03 and TC-P5-E1016-APP-01 assert the class contribution and name the P1 values as P1's, TC-P5-E1016-APP-04, -05, -06, -08 and -09 assert the authorise, scope and masking rules of the reads, TC-P5-E1016-APP-08 asserts the refusal of a read that cannot be logged, and TC-E1-016-10 asserts the two facts about this service's own login while the view grants stay with P1. The `-ITG` copies of these cases belong to RWB-ITG-E1016-ITG and are not listed here. The full test, with its Given, When and Then, is in the Recovery Workbench Test Cases workbook, tab Story test cases, under the same test case ID.

Version 3: rows that cite `TC-P5-E1016-APP-` identifiers are this story's rows of Recovery Workbench Test Cases v9. Where a shared legacy identifier now names another story's case there, this story's identifier replaces it, and cases run by one identifier are joined in one row.

### 17. Guardrails

- **No business value in code.** The product code, the class codes, the rule version, the retention months, the age basis, the action codes, the field IDs, the masking rows and the access rows are data rows read with the version in force. No role code, product code, class code or field-ID list appears in Java.
- **No personal data in logs, events, workflow inputs, tests or prompts.** The PII access log carries the user, the product, the case and the field names, never a value; the fixtures of sections 7 and 16 are synthetic; a field value in a trace is replaced by the field name.
- **No cross-schema read and no cross-schema key** (DP-01): every statement of the module names `rwb_document` only, and `rwb_document` holds no foreign key into another schema. The case, the roles, the access rows and the dictionary arrive through their owners' contracts.
- **No ACE view read by P5** (DP-05): the service holds no grant on the `recovery` schema and no class names a `recovery.v_ace_*` view or a `public` table; the build and the database both refuse one.
- **A read that cannot be logged returns no personal data**: the log write precedes the answer, and its failure is a 503 with no field.
- **No token and no detokenization.** The identity number exists only as `id_no_masked` and `id_no_last4`; no response field carries the clear value, and no masking rendering is computed here.
- **Default deny twice over.** A missing Documents right, a missing or not-yet-in-force access row, a case out of scope, a missing masking row and a missing dictionary answer all resolve to refused, masked or 503, never to allowed and never to clear.
- **One catalog contribution per product.** This service serves its class and its object list and assembles no part of the catalog entry that another service owns.
- **No event and no guard is built here.** The service's two events belong to other stories, and the guard is the service template's.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role through the views; personal data masked by role under PDPA | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | All recovery processes | CTL-09, CTL-11; DL26; BR-P1-001-4, BR-P1-001-6 | TC-P5-E1016-APP-02, TC-E1-016-03 to TC-E1-016-10 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record, refresh and retention | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-16 | All recovery processes | CTL-08; BR-P1-002-2 | TC-P5-E1016-APP-03, TC-P5-E1016-APP-01, TC-E1-016-12 |
| REQ-ACA-006 | Every read of the case store and the document store is written to the access log; here, every read of a document is logged by the ACE common module and a read that cannot be logged is refused | Business Requirements Epic 1, section 4 (named in the legacy metadata and BR4; the legacy section 18 table carries no row for it) | FEAT-RDF-15 | All recovery processes | CTL-09, CTL-11; BR5 | TC-P5-E1016-APP-02, TC-P5-E1016-APP-08 |

The two legacy rows are copied unchanged and the third row is added for the requirement the legacy metadata names and the legacy traceability table omits; no requirement value is changed.

| Legacy reference | Where it is kept |
|---|---|
| Access version `DPA-2026.11` in force from 2026-11-20, and the row in force test | Background, sections 3, 5 X1 and X6, 7 AC3, 8 BR1, 16 |
| Data product `DP10` and the eleven P5 tables behind it | Sections 1, 2, 7, 11, 12.7, 19 |
| The DP01 catalog entry of legacy AC2: owner role, system of record "ACE (ingested from ALS)", refresh cycle "DAILY", expected-by "08:00", the six views, `account_ext`, DF-ACE-018, REC-01 and REC-02 and the access rows | Named as P1's and P4's in sections 2, 7, 11, 16 and 19; not built or restated here |
| The 30 `recovery.v_ace_*` views and the dictionary baseline of at least 123 sys_objects and 1,379 sys_fields rows (RD-P1-025) | Sections 5 X7, 7 AC6, 8 BR8 and BR9, 16; the content and the grants are RWB-P1-E1016-APP's and RWB-P1-E1016-DB's |
| The masking rules and the no-rule default (DL26) | Background, sections 3, 5 X4, 7 AC4, 8 BR3 and BR4, 11 |
| The PII access log, its field-names-only content and its refusal rule (INT-22) | Sections 1, 4 step 7, 5 X5, 7 AC2 and AC6, 8 BR5, 12.8, 16 |
| Retention class values `LEGAL10Y` and `GENERAL05Y`, rule version `RET-2026.11` and the exception `RETENTION_CLASS_MISSING` | Background, sections 2, 5 X8, 7 AC1, 11, 13 |
| Legacy key RWB-E1-016, story RWB-P5-E1016-APP, self-tests TC-E1-016-01 to TC-E1-016-12 | Metadata, sections 3, 12, 16 |

### 19. Out of scope

- The data products and the catalog (RWB-P1-E1016-APP and RWB-P1-E1016-CON), the data dictionary and the PDPA tags (RWB-P1-E1064-CON and its app story), `data_product_access`, `sys_objects` and `sys_fields`: they are neither read as tables nor defined here.
- The roles, the permission matrix, the masking policy and the authorise and permissions operations: RWB-P4-E1016-APP; the role to permission matrix and the masking rule mechanism: RWB-P4-E1037-APP.
- The composed catalog entry a data steward reads and the end-to-end proof across the owners: RWB-ITG-E1016-ITG.
- The access-log search and break-glass: RWB-P4-E1039-APP.
- The personal data screen SCR-47: Epic 8.
- The view definitions, their ownership and the grants on the `recovery` schema: RWB-P1-E1069-APP and RWB-P1-E1016-DB.

### 20. Remaining delivery steps

- Size the story at refinement (squad).
- RWB-P1-E1064-CON, RWB-P4-E1037-CON and RWB-P3-E1018-CON Done with their fakes published at a pinned version (contract owners).
- Grant the rwb-document service identity the dictionary read, NEW-GAP-F17-3 (security architect).
- Add the AC10 test case row and update TC-P5-E1016-APP-01 in Test Cases v9 and the RTM (test lead).
- Load the synthetic test data in DEV (platform administrator).
- The gateway-bff composite route and the screen that calls it: RWB-PLT-N001-CON and the P3, P5 screen stories.
- The document detail panel and the case document list screen: RWB-P5-E1024-APP and RWB-P5-E1026-APP.
- The retention load, the retention Schedule (JOB-17) and the retention answer of one document (`GET /documents/{documentId}/retention`): RWB-P5-AD021-APP, with the shape of RWB-P5-AD021-CON, which this story reuses and does not redefine.
- The document type table and its load: RWB-P5-E1025-APP.
- The service template, the guard library, the per-service Flyway baseline, the topic and queue provisioning, the dashboards and the runbook.
