# RWB-E1-064 Data dictionary for the 14 data products

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-064 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Requirement IDs | REQ-RDF-001, REQ-RDF-011 |
| BRD section | Business Requirements Epic 1, section 3.1 (story), section 4 (REQ-RDF-001, REQ-RDF-011) and section 5 (data dictionary sources and owners) |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **every field in the 14 data products typed, sourced and owned, with a data contract per source system that its owner confirms**, so that **a data contract can be agreed with the system that owns it**.

## 2. Business rationale

The 1,256 fields of the recovery tables come from 13 source systems or from the Workbench itself, and 108 source mappings still read "To confirm with the system owner" (s2t.txt). Without a confirmed contract a source can change a field and the load breaks or loads the wrong value. This story holds the dictionary as versioned data with type, source, source field, refresh, owner and behavior when late, groups the mapped fields into one contract per source system, and lets a contract be published only after its system owner confirms it. Serves REQ-RDF-001 (one system of record and one owner per product) and REQ-RDF-011 (catalog entry content).

## 3. Preconditions

- RWB-E1-001 is done: sys_objects holds 108 entities and sys_fields holds 1,256 fields, seeded from the Logical Data Model.
- The reference data service (RWB-E1-043) accepts a load for table sys_fields and hands approved rows to P1.
- The data steward holds RW-DATASTEW (Reference data RU); the reference data administrator holds RW-REFADM (Reference data CRUD).
- The source mapping in s2t.txt lists 108 mapped fields across 13 source systems and interfaces INT-01 to INT-16.

## 4. Flow

1. Reference data administrator: loads the dictionary attributes (owner role, refresh cycle, behavior when late, interface) for all 1,256 fields through POST /admin/reference-loads with table sys_fields.
2. DataDictionaryLoader: refuses the whole load if any field lacks an attribute; otherwise writes the attributes and version 1 of each field to sys_field_version.
3. DataDictionaryLoader: creates or updates one data_contract per source system in status DRAFT, naming its interfaces, listing its mapped fields.
4. Developer or analyst: calls GET /admin/data-dictionary/fields and reads a field's type, source system, source field, refresh, owner and behavior when late.
5. Data steward: sends the contract to the system owner outside the Workbench and records the owner's confirmation with PATCH /admin/data-contracts/{contractId}: confirming role, date and the stored confirmation document.
6. Data steward: publishes the contract with POST /admin/data-contracts/{contractId}/publish; the service refuses a contract without a confirmation.
7. DataContractService: sets the contract PUBLISHED and the mapping status of its fields to Confirmed.
8. Data steward: changes a field definition with PATCH /admin/data-dictionary/fields/{fieldId} and a reason; the service writes a new version with its date and reason.
9. DataContractService: when a changed field belongs to a published contract, opens a new DRAFT contract version; the published version stays in force until the new one is confirmed and published.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Publish without the system owner's confirmation | 409; contract stays DRAFT | MSG-P1-021 | AC4 |
| X2 | A field change without a reason | 422; no version written | MSG-GEN-001 | AC5 |
| X3 | A dictionary load with a field missing an attribute | Load refused in full; previous dictionary stays in force | MSG-P1-002 | AC6 |
| X4 | Two stewards change the same field from the same version | Second change refused with 409 | MSG-GEN-004 | AC7 |
| X5 | A field of a published contract changes | New DRAFT contract version; published version stays in force | None | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the metadata tables seeded by RWB-E1-001 and the reference load path of RWB-E1-043 |
| Negotiable | Owners, refresh cycles and late behavior are data values; the story fixes the versioning and the confirm-before-publish rule |
| Valuable | Each source system agrees in writing what it sends, before loads depend on it |
| Estimable | Three tables, five endpoints, one loader |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion is one API test against the seeded metadata tables |

## 7. Acceptance criteria

```gherkin
Feature: Data dictionary for the 14 data products

  Background:
    Given the dictionary holds 1,256 fields in 108 entities
    Given data product "DP01" Account and arrears has owner role RW-DATASTEW and system of record "Core bank (ALS) via COLLINS"
    Given contract "DC-ALS" for source system "Core bank (ALS)" and interfaces "INT-01" and "INT-02" is "DRAFT" with 32 mapped fields

  Scenario: AC1 Every field is defined
    Given the 14 data products
    When a developer calls GET /admin/data-dictionary/fields?entity=loan_account&field=days_past_due
    Then the field "DF-ACC-014" shows type "NUMBER", physical type "integer", source system "Core bank (ALS) via COLLINS", source field "DELAY_DAYS", refresh "Daily, end of day", owner RW-DATASTEW and behavior when late "Keep the previous value and mark DP01 stale"
    Then a call for all 1,256 fields returns no field with an empty type, source system, source field, refresh, owner or behavior when late

  Scenario: AC2 The owning system has agreed it
    Given the data steward recorded the confirmation of "DC-ALS" by role "ALS system owner" on 2026-11-12 with document "DOC-SYN-0640"
    When the data steward publishes "DC-ALS"
    Then the contract status is "PUBLISHED" with version 1 and the confirmation on 2026-11-12
    Then the 32 mapped fields of Core bank (ALS) show mapping status "Confirmed"

  Scenario: AC3 A change is visible
    Given field "DF-ACC-014" is at version 1
    When the data steward changes its source field to "DPD_DAYS" with reason "ALS renamed the field in release 26.4" on 2026-11-18
    Then field "DF-ACC-014" is at version 2 dated 2026-11-18 with that reason
    Then version 1 stays readable with its own date

  Scenario: AC4 Publish without the owner's confirmation
    Given contract "DC-EFS" for EFS has no recorded confirmation
    When the data steward publishes "DC-EFS"
    Then the system refuses the call with status 409 and MSG-P1-021 for system "EFS"
    Then the contract stays "DRAFT"

  Scenario: AC5 A change without a reason
    When the data steward changes field "DF-ACC-015" with an empty reason
    Then the system refuses the call with status 422 and MSG-GEN-001 for field "reason"
    Then field "DF-ACC-015" stays at version 1

  Scenario: AC6 A dictionary load with a missing attribute
    Given a dictionary load in which field "DF-COL-005" collateral.plot_no has no refresh cycle
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and check "refresh_cycle missing for DF-COL-005"
    Then the dictionary in force is unchanged

  Scenario: AC7 Two changes to the same field at once
    Given two data stewards read field "DF-ACC-016" at version 1
    When both send a change with version 1
    Then the system saves the first change as version 2
    Then the system refuses the second with status 409 and MSG-GEN-004

  Scenario: AC8 A change to a field in a published contract
    Given contract "DC-ALS" is "PUBLISHED" at version 1
    When field "DF-ACC-014" changes to version 2
    Then the system creates contract "DC-ALS" version 2 as "DRAFT"
    Then version 1 stays "PUBLISHED" and in force
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every field carries type, source system, source field, refresh, owner and behavior when late | REQ-RDF-001; sys_fields |
| BR2 | Each data product has exactly one system of record and one owner role | REQ-RDF-001; data_product |
| BR3 | A data contract is published only after its system owner's confirmation is recorded | s2t.txt status "To confirm with the system owner"; DL12 |
| BR4 | A field change creates a new version with a date and a reason; earlier versions stay readable | Reference data change process; DT02; Principle 1 |
| BR5 | A dictionary load with an exception is refused in full | Reference data change process, step 3; CTL-08 |
| BR6 | A change to a published contract's field opens a new contract version; the published version stays in force until replaced | R-UNI-38 |

## 9. State transitions

None. This story does not change a case status. It changes the data contract status: DRAFT to PUBLISHED on publish after confirmation, and a new DRAFT version when a field of a published contract changes.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Changes field definitions, records confirmations, publishes contracts (Reference data U) |
| RW-REFADM, reference data administrator | Submits the dictionary load (Reference data C) |
| RW-COE, center of excellence analyst | Reads and changes field definitions (Reference data CRUD) |
| RW-TRIBE, RW-AUDIT and other roles with Reference data R | Read the dictionary and the contracts |
| SY-DATALOAD, data load | Applies an approved dictionary load |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-088 | sys_objects | object_name | Read |
| DF-REF-091 | sys_objects | data_product | Read |
| DF-REF-092 | sys_objects | system_of_record | Read |
| DF-REF-095 | sys_fields | field_id | Read |
| DF-REF-097 | sys_fields | field_name | Read |
| DF-REF-098 | sys_fields | data_type | Write |
| DF-REF-099 | sys_fields | physical_type | Write |
| DF-REF-103 | sys_fields | source_system | Write |
| DF-REF-104 | sys_fields | source_field | Write |
| DF-REF-105 | sys_fields | is_personal | Read |
| DF-REF-106 | sys_fields | description | Write |
| Standard column | sys_fields | version | Write |
| DF-REF-107 | sys_fields | owner_role | Write |
| DF-REF-108 | sys_fields | refresh_cycle | Write |
| DF-REF-109 | sys_fields | late_behavior | Write |
| DF-REF-110 | sys_fields | interface_id | Write |
| DF-REF-111 to DF-REF-115 | sys_field_version | all fields | Write |
| DF-OPS-010 to DF-OPS-020 | data_contract | all fields | Write |
| DF-REF-070 to DF-REF-079 | data_product | all fields | Write |

The sys_objects and sys_fields columns exist in Recovery Workbench Physical Schema v4.sql (metadata tables) and carry no BR Field ID in the Logical Data Model. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Endpoints (new, see additions)**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /admin/data-dictionary/fields | Query: product, entity, field, sourceSystem, page, size | DataDictionaryFieldPage: items of DataDictionaryField (fieldId, entity, fieldName, dataType, physicalType, mandatory, listCode, sourceSystem, sourceField, refreshCycle, ownerRole, lateBehavior, interfaceId, isPersonal, version, versionDate) | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 (MSG-GEN-006) | Reference data, R | Not applicable |
| PATCH /admin/data-dictionary/fields/{fieldCode} | Header If-Match: version; body DataDictionaryFieldChange (changed attributes, reason) | DataDictionaryField | 403; 404 unknown field (MSG-P4-003); 409 stale version (MSG-GEN-004); 422 reason empty (MSG-GEN-001) | Reference data, U | If-Match version |
| GET /admin/data-contracts | Query: sourceSystem, status | DataContract[] (id, sourceSystem, interfaceId, contractVersion, status, fieldCount, confirmedByRole, confirmedOn, confirmationDocumentId, publishedAt) | 401; 403; 503 | Reference data, R | Not applicable |
| PATCH /admin/data-contracts/{contractId} | Header If-Match; body DataContractConfirmation (confirmedByRole, confirmedOn, confirmationDocumentId) | DataContract | 403; 404; 409 (MSG-GEN-004); 422 field empty (MSG-GEN-001) | Reference data, U | If-Match version |
| POST /admin/data-contracts/{contractId}/publish | Header Idempotency-Key | DataContract | 403; 404; 409 no confirmation (MSG-P1-021) | Reference data, U | Idempotency-Key header |

The dictionary load uses POST /api/recovery/v1/admin/reference-loads with table `sys_fields` (Reference data, C), approved through POST /api/recovery/v1/admin/reference-loads/{loadId}/approve (Reference data, A).

**Published interface (P1, called by the reference data service and by RWB-E1-016)**

```java
package recovery.dataengine.dictionary.api;

public interface DataDictionaryLoader {
    LoadResult apply(String loadVersion, LocalDate validFrom, List<DictionaryFieldRow> rows);
}

public interface DataDictionaryQuery {
    Optional<DataDictionaryField> field(String fieldId);
    List<DataDictionaryField> fieldsOf(String productCode);
    DataProductDefinition product(String productCode);
}
```

## 13. Solution plan

- Package: folder `recovery/dataengine/dictionary`, Java package `recovery.dataengine.dictionary`.

| Component | Type | Responsibility |
|---|---|---|
| DataDictionaryController | Controller | The five endpoints in section 12 |
| DataDictionaryService | Service | Field reads, versioned changes with reason, optimistic lock |
| DataContractService | Service | Contract per source system; confirmation; publish rule; new version on change |
| DataDictionaryLoader | Published interface | Whole-load validation and apply |
| DataDictionaryQuery | Published interface | Field and product definitions for other packages and modules |
| SysFieldRepository, SysFieldVersionRepository, DataContractRepository, DataProductRepository | Repository | Read and write the four tables |
| SysField, SysFieldVersion, DataContract, DataProduct | Entity | One per table |

- Database: Flyway migration in this story adds columns owner_role varchar(20), refresh_cycle varchar(30), late_behavior varchar(200), interface_id varchar(10) to sys_fields; creates sys_field_version (id uuid, field_id varchar(16) references sys_fields, field_version integer, definition jsonb, change_reason varchar(400) not null, changed_at timestamptz, changed_by uuid; unique (field_id, field_version)); creates data_contract (id uuid, contract_code varchar(20), source_system varchar(80), interface_id varchar(40), contract_version integer, status varchar(10) check in DRAFT, PUBLISHED, SUPERSEDED, confirmed_by_role varchar(80), confirmed_on date, confirmation_document_id uuid, published_at timestamptz, published_by uuid, standard columns; unique (contract_code, contract_version)); creates data_product (product_code varchar(4) primary key, product_name varchar(80), definition varchar(400), owner_role varchar(20), system_of_record varchar(120), refresh_cycle varchar(10) check in DAILY, WEEKLY, MONTHLY, ON_CHANGE, expected_by varchar(20), standard columns) seeded with DP01 to DP14 from sys_objects.
- Configuration and reference data: the dictionary attribute load prepared by the data steward from s2t.txt and the LDM; data_product names and owners confirmed by each data product owner (BRD Epic 1 section 5); expected_by times assumed 08:00 for daily COLLINS products and Monday 08:00 for weekly file products (DL11).
- Build steps:
  1. Flyway migration for the sys_fields columns and the three new tables; seed data_product DP01 to DP14 and version 1 of each of the 1,256 fields.
  2. DataDictionaryLoader with whole-load validation of the six attributes; refusal with MSG-P1-002 and the first failing check.
  3. DataDictionaryService change with If-Match and a mandatory reason; new sys_field_version row per change.
  4. DataContractService: build contracts from sys_fields.interface_id; confirmation record; publish rule with MSG-P1-021.
  5. New DRAFT contract version when a field of a published contract changes.
  6. DataDictionaryController and the contract tests for the new endpoints (RWB-TE-003).
  7. Tests for AC1 to AC8 and the access test.
- Feature flag: `rwb.dataengine.data-dictionary`.
- Done when: the tests in section 16 pass and all 1,256 fields return the six attributes in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-021 | Publish of a contract with no confirmation (new, see additions) | The data contract for {system} cannot be published until its system owner confirms it. |
| MSG-GEN-001 | Reason or confirmation field empty | Enter {field}. |
| MSG-GEN-004 | Change from an old version | Someone else changed this record. Reload it to see their change. |
| MSG-P1-002 | Dictionary load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P4-002 | Role without Reference data U | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. Developers and analysts read the dictionary through GET /admin/data-dictionary/fields; SCR-40 Reference data shows versioned tables from Epic 8, and until then changes go by file load or the endpoints.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-064-01 | AC1, BR1, BR2 | System | Seeded 1,256 fields; field DF-ACC-014 |
| TC-E1-064-02 | AC2, BR3 | System | Contract DC-ALS with 32 fields; confirmation on 2026-11-12 |
| TC-E1-064-03 | AC3, BR4 | System | Change of DF-ACC-014 source field with reason |
| TC-E1-064-04 | AC4, BR3 | System | Contract DC-EFS with no confirmation |
| TC-E1-064-05 | AC5, BR4 | System | Change of DF-ACC-015 with empty reason |
| TC-E1-064-06 | AC6, BR5 | System | Load with no refresh cycle for DF-COL-005 |
| TC-E1-064-07 | AC7 | System | Two changes to DF-ACC-016 from version 1 |
| TC-E1-064-08 | AC8, BR6 | System | Published DC-ALS and a change to DF-ACC-014 |
| TC-E1-064-09 | Access | Access | RW-TRIBE sends PATCH /admin/data-dictionary/fields/DF-ACC-014; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: owners, cycles, late behavior and contract content are data rows.
- No personal data in logs, tests or prompts: the dictionary holds definitions, not values; the confirmation names a role, not a person.
- No read of another module's tables: other modules use DataDictionaryQuery.
- A published contract is never edited in place; a change makes a new version.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner | Business Requirements Epic 1, sections 3.1, 4 and 5 | None | All recovery processes | CTL-08; DL12 | TC-E1-064-01, TC-E1-064-02, TC-E1-064-04, TC-E1-064-06 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record and refresh | Business Requirements Epic 1, sections 3.1 and 4 | None | All recovery processes | R-UNI-38 | TC-E1-064-03, TC-E1-064-05, TC-E1-064-07, TC-E1-064-08 |

## 19. Out of scope

- The catalog endpoint, access by product and PDPA masking (RWB-E1-016).
- Freshness stamps per load (RWB-E1-015).
- Retention per product and table (RWB-E1-017).
- The reference data screen SCR-40 (Epic 8).
- Contracts for stage 2 data products (RWB-E2-010).

