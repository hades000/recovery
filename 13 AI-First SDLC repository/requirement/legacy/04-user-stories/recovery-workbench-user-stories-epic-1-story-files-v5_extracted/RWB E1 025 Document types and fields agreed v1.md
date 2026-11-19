<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 025 Document types and fields agreed v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 025 Document types and fields agreed v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-025 Document types and fields agreed

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-025 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-03 Agree the six document types and their fields |
| Requirement IDs | REQ-DCM-004 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | D7.2 |
| Priority | Must |
| Depends on | RWB-E1-012 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the first six document types (demand letter, court notice, appraisal report, title deed, settlement agreement, guarantor notice) with their key fields agreed with Legal and NPA and held as versioned reference data**, so that **the OCR pipeline, classification and extraction have one signed target list**.

## 2. Business rationale

Classification and extraction cannot be built or measured until the bank fixes which types are read and which fields come out of each (REQ-DCM-004, DL19). Today no signed list exists, so the model would train on a list that may change. This story turns the agreed list into a versioned table that the store (RWB-E1-024), classification (RWB-E1-050) and extraction (RWB-E1-053) read, and that changes by a data load without a code release (DT02). The measure it serves is fields extracted without review (FSD P5 A2.3.1).

## 3. Preconditions

- RWB-E1-012 is done: the local trackers are listed with their owners, so the types in the current trackers are known.
- The load file "DOCTYPE-2026.11" is prepared by the reference data administrator with the six types, 26 fields and the sign-offs of a legal counsel user and a Head of NPA user.
- LOV-RETENTION holds the codes LEGAL10Y and GENERAL05Y, assumed until the bank retention schedule arrives (DL26), loaded by the data steward.
- The loader holds RW-REFADM (Reference data C). The approver holds Reference data A (see section 10).
- The P4 endpoint POST /admin/reference-loads exists and calls the P5 ReferenceTableLoader for table code DOCUMENT_TYPE.
- Feature flag rwb.dochub.doctypes is on.

## 4. Flow

1. Center of excellence analyst: prepares the list of six types and 26 fields; legal counsel and the Head of NPA review it and sign with a date.
2. Reference data administrator: uploads the file with POST /admin/reference-loads, table DOCUMENT_TYPE, validFrom 2026-11-30.
3. P4 reference load service: passes the rows to DocumentTypeLoader through the ReferenceTableLoader interface.
4. DocumentTypeLoader: validates every row: type code unique, label present, write-once flag present, retention class in LOV-RETENTION, at least one field, both sign-offs with a user ID and a date.
5. DocumentTypeLoader: on any failure refuses the load whole and returns the row errors; the version in force is unchanged.
6. DocumentTypeLoader: on success writes the rows as table version DOCTYPE-2026.11 with status LOADED, not yet in force.
7. Approver: approves with POST /api/recovery/v1/admin/reference-loads/{loadId}/approve; a different person from the loader.
8. DocumentTypeLoader: sets the version APPROVED; from validFrom the readers return it as the version in force; the previous version gets valid_to of the day before.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A row has no Legal or no NPA sign-off, or a sign-off without a date | Load refused in full; version in force unchanged | MSG-P3-027 | AC3 |
| X2 | A row has a retention class not in LOV-RETENTION, or repeats a type code | Load refused in full | MSG-P3-027 | AC4 |
| X3 | The same table version is loaded a second time | Refused with 409; the first load is kept | MSG-P3-027 | AC5 |
| X4 | A new version with a future valid from date | The current version stays in force until that date; open work keeps the version it used | None | AC6 |
| X5 | The loader tries to approve their own load | Refused with 409 | MSG-P7-002 | AC7 |
| X6 | A role without Reference data C uploads the file | Refused with 403 | MSG-P4-002 | TC-E1-025-08 (Access) |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the tracker list (RWB-E1-012) and the P4 reference load endpoint |
| Negotiable | The type list and fields are data; the bank list replaces the six proposed types under DL19 |
| Valuable | Gives the OCR, classification and extraction stories one signed target |
| Estimable | One table, one loader, one validation set |
| Small | Under one week with its tests |
| Testable | Each criterion below is one test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Document types and fields agreed

  Background:
    Given LOV-RETENTION holds "LEGAL10Y" and "GENERAL05Y"
    Given user "TEST-REFADM-01" holds RW-REFADM
    Given user "TEST-APPROVER-01" holds Reference data A

  Scenario: AC1 Field list signed
    Given the six types and their 26 fields in load file "DOCTYPE-2026.11"
    Given each row carries the legal counsel sign-off of user "TEST-LEGAL-01" dated 6 November 2026
    Given each row carries the NPA sign-off of user "TEST-HEADNPA-01" dated 6 November 2026
    When "TEST-REFADM-01" loads the file for table "DOCUMENT_TYPE" with valid from 30 November 2026
    Then the load has status "LOADED" with 6 rows
    Then every row holds both sign-off user IDs and both dates

  Scenario: AC2 Reference data
    Given the load from AC1
    When "TEST-APPROVER-01" approves it
    Then the document type table version "DOCTYPE-2026.11" is in force from 30 November 2026
    Then it holds DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE
    Then COURT_NOTICE holds the fields court_name, black_case_no, notice_date and hearing_date with retention class "LEGAL10Y" and write_once true
    Then APPRAISAL_REPORT has retention class "GENERAL05Y", write_once false and 4 fields

  Scenario: AC3 Load without both sign-offs is refused
    Given a load file where the GUARANTOR_NOTICE row has no NPA sign-off
    When "TEST-REFADM-01" loads it
    Then the system refuses the load in full with MSG-P3-027 naming row 6 and "NPA sign-off missing"
    Then no row of that file is written and the version in force is unchanged

  Scenario: AC4 Invalid values are refused in full
    Given a load file where the TITLE_DEED row has retention class "KEEP99" and a seventh row repeats the type code "COURT_NOTICE"
    When "TEST-REFADM-01" loads it
    Then the system refuses the load in full with MSG-P3-027 listing both rows
    Then the version in force is unchanged

  Scenario: AC5 The same version loaded twice
    Given version "DOCTYPE-2026.11" is loaded
    When "TEST-REFADM-01" loads a file with version "DOCTYPE-2026.11" again
    Then the system refuses the request with 409 and MSG-P3-027 naming "version already loaded"
    Then the first load is unchanged

  Scenario: AC6 A future version takes effect on its date
    Given version "DOCTYPE-2026.11" is in force
    Given version "DOCTYPE-2027.01" adds field "court_region" to COURT_NOTICE and is approved with valid from 1 January 2027
    When the type table is read on 31 December 2026 and on 1 January 2027
    Then the read on 31 December 2026 returns "DOCTYPE-2026.11"
    Then the read on 1 January 2027 returns "DOCTYPE-2027.01" with field "court_region"

  Scenario: AC7 The loader cannot approve their own load
    Given "TEST-REFADM-01" loaded version "DOCTYPE-2027.01" and also holds Reference data A in the test set
    When "TEST-REFADM-01" approves it
    Then the system refuses the request with 409 and MSG-P7-002
    Then the load stays "LOADED"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The document types and their fields are signed by Legal and NPA before extraction is built | REQ-DCM-004; DL19 |
| BR2 | Each type row carries the write-once flag, the retention class and the field list | Document type table (New); DT02 |
| BR3 | A load with any invalid row is refused in full | refdata.txt change process, step 3; CTL-08 |
| BR4 | A version takes effect on its valid from date; work already done keeps the version it used | refdata.txt change process, step 6; R-UNI-38 |
| BR5 | The person who loads a version does not approve it | roles.txt separation of duty; CTL-08 |
| BR6 | Retention class codes come from LOV-RETENTION | LOV-RETENTION; DL26 |
| BR7 | The six proposed types apply until the bank provides its own list | DL19 |

The initial field lists are assumed until the sign-off (DL19): DEMAND_LETTER case_no, account_no, letter_date, amount_demanded, pay_by_date; COURT_NOTICE court_name, black_case_no, notice_date, hearing_date; APPRAISAL_REPORT appraisal_no, appraisal_date, appraised_value, title_doc_no; TITLE_DEED title_doc_no, land_office, owner_name, area_sq_wa; SETTLEMENT_AGREEMENT case_no, agreement_date, settlement_amount, installment_count, borrower_name; GUARANTOR_NOTICE case_no, guarantor_name, notice_date, amount_claimed. Fields account_no, owner_name, borrower_name and guarantor_name are marked personal. Write-once true for every type except APPRAISAL_REPORT; retention LEGAL10Y for the write-once types and GENERAL05Y for APPRAISAL_REPORT (assumed; DL26, DL27).

## 9. State transitions

None. This story does not change a case status. It changes the reference load status: LOADED on a valid load; REFUSED on a failed check; APPROVED on approval, in force from valid from.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Prepares the list and reads the table |
| RW-LEGAL, legal counsel | Signs the list for Legal |
| RW-HEADNPA, Head of NPA | Signs the list for NPA |
| RW-REFADM, reference data administrator | Loads the file (Reference data C) |
| Approver with Reference data A | Approves the load. The permission matrix gives Reference data A to no role today; assumed granted to the legal counsel who owns the table (DL01) |
| SY-OCR, SY-RULES | Read the version in force |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
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

LOV-RETENTION is read through the P4 list service (lov_value rows, no BR Field ID). Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /admin/reference-loads** (P4 endpoint; this story adds the table code DOCUMENT_TYPE)

| Item | Value |
|---|---|
| Request | multipart/form-data: file (binary, the load file in the Excel template), table = "DOCUMENT_TYPE", validFrom (date) |
| Response | 201 ReferenceLoad: id, table, validFrom, status (LOADED or REFUSED), rows |
| Errors | 401; 403 no Reference data C (MSG-P4-002); 409 version already loaded (MSG-P3-027); 422 a row fails validation (MSG-P3-027 with row and error); 503 store unavailable (MSG-GEN-006) |
| Authorization | Reference data, right C |
| Idempotency | The table code and the table version; a second load of the same version is refused with 409 |

**POST /api/recovery/v1/admin/reference-loads/{loadId}/approve**

| Item | Value |
|---|---|
| Request | Path loadId (uuid) |
| Response | 200 ReferenceLoad with status APPROVED |
| Errors | 401; 403 no Reference data A (MSG-P4-002); 404; 409 approver is the loader (MSG-P7-002) or status is not LOADED; 503 |
| Authorization | Reference data, right A |
| Idempotency | Approving an APPROVED load returns it unchanged |

**Published interfaces**

```java
// P5 implements the P4 loader contract for its own tables
public interface ReferenceTableLoader {
    String tableCode();                                           // "DOCUMENT_TYPE"
    LoadResult validateAndStage(UUID loadId, String tableVersion, LocalDate validFrom, List<Map<String, String>> rows);
    void approve(UUID loadId, UUID approverId);
}

// P5 reader used by RWB-E1-024, RWB-E1-050 and RWB-E1-053
public interface DocumentTypeCatalog {
    DocumentTypeVersion inForce(LocalDate businessDate);         // version, types, fields
    Optional<DocumentTypeDef> type(String docTypeCode, LocalDate businessDate);
}
```

## 13. Solution plan

**Package.** Folder `recovery/dochub/types`, Java package `recovery.dochub.types`.

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| DocumentTypeLoader | Service | Implements ReferenceTableLoader for DOCUMENT_TYPE: parse, validate, stage, approve |
| DocumentTypeCatalog | Published interface | Returns the version in force and a type by code for a business date |
| DocumentTypeCatalogService | Service | Implements DocumentTypeCatalog with a 5-minute cache, cleared on approval |
| DocumentTypeRepository | Repository | Reads and writes document_type only |
| DocumentTypeEntity | Entity | Maps document_type |
| document_type rows | Rule table | The six types as data |

**Database.**
- Flyway migration `V1_5_025__document_type.sql` creates document_type: id uuid, doc_type_code varchar(30), label_en varchar(120), label_th varchar(120), write_once boolean, retention_class varchar(10), field_definitions jsonb, legal_signoff_by uuid, legal_signoff_date date, npa_signoff_by uuid, npa_signoff_date date, table_version varchar(20), valid_from date, valid_to date, load_id uuid, plus the standard columns.
- Constraints: unique (doc_type_code, table_version); not null on both sign-off columns.
- Index ix_document_type_valid on (valid_from, valid_to).

**Configuration and reference data.**
- The load file DOCTYPE-2026.11, prepared by the reference data administrator, signed by legal counsel and the Head of NPA.
- LOV-RETENTION values, loaded by the data steward (DL26).

**Build steps.**
1. Write the migration and the entity; test the constraints.
2. Build the row parser for the Excel template columns; unit test a valid file of 6 rows.
3. Build the validation rules and the refuse-whole behavior; unit test AC3 and AC4.
4. Build staging, the version check and approval with the separation of duty check; test AC1, AC2, AC5 and AC7.
5. Build DocumentTypeCatalogService with the valid from rule; test AC6 on the boundary dates.
6. Add the loader to the table codes of the P4 reference load service; API test through POST /admin/reference-loads and the access test.

**Feature flag.** `rwb.dochub.doctypes`. Off: the table code DOCUMENT_TYPE is refused by the reference load endpoint.

**Done when.** The tests in section 16 pass and version DOCTYPE-2026.11 is approved in SIT with both sign-offs.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A document hub reference load fails a check | The {table} load was refused: {error} at row {row}. The version in force is unchanged. |
| MSG-P7-002 | Loader approves their own load | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. SCR-40 Reference data comes in Epic 8; until then the table is loaded by file through the reference load endpoint. The reference data administrator sees the load status and the row errors in the endpoint response; the center of excellence analyst reads the version in force through GET /api/recovery/v1/admin/lists/{listCode} with listCode LOV-DOC-TYPE.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-025-01 | AC1, BR1 | System | Load file DOCTYPE-2026.11 with six types, 26 fields and both sign-offs |
| TC-E1-025-02 | AC2, BR2, BR6 | System | Approved load; read of COURT_NOTICE and APPRAISAL_REPORT |
| TC-E1-025-03 | AC3, BR1, BR3 | System | GUARANTOR_NOTICE row without the NPA sign-off |
| TC-E1-025-04 | AC4, BR3 | System | Retention class KEEP99 and a repeated type code |
| TC-E1-025-05 | AC5 | System | Same version loaded twice |
| TC-E1-025-06 | AC6, BR4 | System | Version DOCTYPE-2027.01 valid from 1 January 2027 |
| TC-E1-025-07 | AC7, BR5 | System | Loader approves own load |
| TC-E1-025-08 | Access | Access | Case owner (RW-CASEOWN, Reference data R only) uploads the file; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: type codes, fields, write-once flags and retention classes are rows in document_type.
- No personal data in logs, tests or prompts. Sign-off users in tests are synthetic IDs.
- No read of another module's tables: LOV-RETENTION is read through the P4 list service.
- A refused load writes no row.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-004 | Document types and key fields agreed and signed before extraction is built | Business Requirements Epic 1, section 3.5 | FEAT-DCM-03 | 13 Manage documents and correspondence | R-UNI-38 | TC-E1-025-01 to TC-E1-025-08 |

## 19. Out of scope

- The retention periods behind each class (RWB-E1-041; DL26).
- The checklist of required types per case type (RWB-E1-040).
- Stage 2 and 3 document types (RWB-E2-025).
- The reference data screen SCR-40 (Epic 8).
