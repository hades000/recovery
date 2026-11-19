# RWB-E1-064 Data dictionary for the 14 data products

SCB Collections and Recovery. Henka Group, 15 November 2026.

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
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 |
| Priority | Must |
| Depends on | RWB-E1-001, RWB-E1-043, RWB-E1-069 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **all 122 objects and 1,366 fields of the 14 data products typed, sourced and owned, including the 30 ACE views and the four extension tables, with a data contract for the ACE read path that the ACE team confirms**, so that **every read has one published definition and a change to an ACE column reaches the dictionary through one governed load**.

## 2. Business rationale

The dictionary is the only place that says what a field is, where it comes from and who owns it. It now covers 122 objects and 1,366 fields: the 92 Workbench tables hold 1,062 fields, 49 of them on the four extension tables, and the 30 `recovery.v_ace_*` views hold 304 fields, 177 in Section A and 127 in Section B. The Workbench loads no source data (D-RCV-35 U1), so every source is either ACE, whose columns are recorded as `public.table.column` on the view fields where the view reads one column, or the Workbench itself.

V0001 creates `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` and seeds the 122 objects and 1,366 fields. This story does not create a table or a column. It publishes the governance attributes on every field, records the change history, and takes the ACE team's confirmation of the read contract before it is published. A new ACE column is added to the dictionary by a reference load through RWB-E1-043, never by editing an applied migration; the view conformance test of RWB-E1-069 blocks the merge until the row exists. Serves REQ-RDF-001 (one system of record and one owner per product) and REQ-RDF-011 (catalog entry content). The measure is that 100 percent of the 1,366 fields return a source, an owner, a refresh cycle and a late behavior.

## 3. Preconditions

- RWB-E1-001 is done: V0001 created the 92 tables, the 30 view objects in the dictionary, the 122 `sys_objects` rows, the 1,366 `sys_fields` rows, `sys_field_version`, `data_product` and `data_contract`.
- RWB-E1-069 is done: the 30 `recovery.v_ace_*` views exist and the view conformance test CHK-01 compares every view column with `sys_fields`.
- The reference data service (RWB-E1-043) accepts a load for table code `sys_fields` and hands approved rows to P1.
- The data steward holds RW-DATASTEW (Reference data U); the reference data administrator holds RW-REFADM (Reference data C).
- The ACE team lead is named as the confirming role for the ACE read contract; the confirmation is stored outside the Workbench as a document reference.
- `v_data_dictionary` returns the 122 objects and 1,366 fields of V0001.

## 4. Flow

1. Data steward: prepares the governance load for all 1,366 fields with owner role, refresh cycle, late behavior and interface, and checks the source system and source field of each view field against the view definition.
2. Reference data administrator: loads the file through POST /admin/reference-loads with table `sys_fields` and valid from 2026-11-30.
3. DataDictionaryLoader: refuses the whole load if any field is unknown, if a view field's source system is not "ACE", if a Workbench field's source system is not "Workbench", if a view field's source field is not a column of that view and is not one of the 7 derived fields, or if any of the required attributes is empty; otherwise writes the attributes and version 1 of each field to `sys_field_version`.
4. Data steward: records the ACE team lead's confirmation of contract DC-ACE, which lists the 304 ACE fields and the read interfaces V0002 and V0003, with the confirming role, the date and the stored document reference.
5. Data steward: publishes DC-ACE with POST /admin/data-contracts/{contractId}/publish; the service refuses a contract without a confirmation.
6. DataContractService: sets the contract PUBLISHED. The published version stays in force until a later version is confirmed and published.
7. Developer or analyst: calls GET /admin/data-dictionary/fields and reads a field's type, source system, source field, refresh, owner and behavior when late.
8. Data steward: changes a field definition with PATCH /admin/data-dictionary/fields/{fieldId}, a reason and an If-Match version; the service writes a new `sys_field_version` row with its date and reason.
9. DataContractService: when a changed field belongs to the published DC-ACE, opens a new DRAFT contract version; the published version stays in force.
10. ACE team and recovery developer: a new ACE column is added to a view by a Flyway migration and to the dictionary by a load through RWB-E1-043; no applied migration is edited, and CHK-01 passes only when both exist.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Publish of a contract without the ACE team's confirmation | 409; contract stays DRAFT | MSG-P1-021 | AC6 |
| X2 | A field change without a reason | 422; no version written | MSG-GEN-001 | AC5 |
| X3 | A dictionary load with an unknown field, a missing attribute, a source system outside ACE and Workbench, or an ACE source field that is not a column of the view and not one of the 7 derived fields | Load refused in full; the dictionary in force stays | MSG-P1-002 | AC4 |
| X4 | Two stewards change the same field from the same version | The second change is refused with 409 | MSG-GEN-004 | AC7 |
| X5 | A field of a published contract changes | A new DRAFT contract version; the published version stays in force | None | AC8 |
| X6 | A view column exists with no `sys_fields` row | CHK-01 fails and the merge is blocked | v_ace_account.legacy_bucket has no data dictionary entry | AC4 |
| X7 | A field definition is changed with no If-Match version | 428; no version written | MSG-GEN-004 | AC7 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the tables and seed of RWB-E1-001, the reference load of RWB-E1-043 and the views and conformance test of RWB-E1-069; it publishes the definition every later read uses |
| Negotiable | Owners, refresh cycles, late behavior and contract content are data values; the story fixes the completeness, source and version rules |
| Valuable | Every read has one published definition, and a source change is governed in one place |
| Estimable | No DDL, five endpoints, two services, one loader |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion is one API test against the seeded metadata tables |

## 7. Acceptance criteria

```gherkin
Feature: Data dictionary for the 14 data products

  Background:
    Given the dictionary holds 122 objects and 1,366 fields from V0001
    Given the governance load of owner role, refresh cycle and late behavior was published on 2026-11-30
    Given data product "DP01" Account and arrears has owner role RW-DATASTEW and system of record "ACE (ingested from ALS)"
    Given contract "DC-ACE" for source system "ACE" and read interfaces "V0002" and "V0003" is "DRAFT" with 304 mapped fields

  Scenario: AC1 Every field is defined
    Given the 14 data products
    When a developer calls GET /admin/data-dictionary/fields?page=1&size=1
    Then the response reports 122 objects and 1,366 fields
    Then the 92 Workbench tables hold 1,062 fields, of which 49 are on the four extension tables
    Then the 30 v_ace_* views hold 304 fields, 177 from Section A and 127 from Section B
    Then every field has a data type, a physical type, a description, a source system, an owner role, a refresh cycle and a behavior when late
    Then 297 of the 304 view fields name an ACE column in the form public.table.column
    Then the 7 derived view fields v_ace_contact.contact_type, city, post_code and country, and v_ace_plan.installments, recommended_installment and recommended_package carry source system ACE and no single ACE column

  Scenario: AC2 Every ACE view has dictionary rows
    Given V0001, V0002 and V0003 are applied in SIT
    When a developer counts v_data_dictionary by source system
    Then 30 objects named v_ace_* are returned with 304 fields
    Then each v_ace_* view has one sys_objects row and one sys_fields row per column
    Then no v_ace_* view has a column without a row and no row without a column
    Then the four extension tables party_ext, contact_point_ext, account_ext and valuation_ext hold 49 fields, DF-EXT-001 to DF-EXT-049

  Scenario: AC3 The arrears field comes from the ACE delay days
    Given V0001 and V0002 are applied in SIT
    Given one ACE account "ACC0000017" has delay_days 95
    When a developer queries v_data_dictionary for entity "v_ace_account" and field "days_past_due"
    Then the row holds field ID "DF-ACE-018", data type "NUMBER" and physical type "integer"
    Then the row holds source system "ACE" and source field "public.account.delay_days"
    Then the row holds data product "DP01", refresh cycle "DAILY", owner role "RW-DATASTEW" and late behavior "Keep the previous value and mark DP01 stale"
    Then select days_past_due from recovery.v_ace_account for "ACC0000017" returns 95

  Scenario: AC4 A new ACE column is a dictionary change through RWB-E1-043
    Given a dictionary fixture in which v_ace_collateral_detail holds 11 fields and no row for "insurance_expiry"
    Given RWB-ACE-001 adds public.collateral_detail.insurance_expiry and V0003 exposes it as v_ace_collateral_detail.insurance_expiry
    When the reference data administrator loads field "DF-ACE-204" with source system "ACE", source field "public.collateral_detail.insurance_expiry", owner RW-DATASTEW, refresh "WEEKLY" and late behavior "Keep the previous value and mark DP06 stale" through POST /admin/reference-loads with table sys_fields
    Then the load is validated and the field row and version 1 of DF-ACE-204 are written
    Then GET /admin/data-dictionary/fields?entity=v_ace_collateral_detail&field=insurance_expiry returns the row
    Then CHK-01 passes on the next pipeline run and no Flyway migration file was edited
    When the same load names source field "public.collateral_detail.insurance_date"
    Then the load is refused in full with MSG-P1-002 and no row is written

  Scenario: AC5 A change keeps its history
    Given field "DF-ACE-018" is at version 1 with late behavior "Keep the previous value and mark DP01 stale"
    When the data steward changes its late behavior to "Keep the previous value, mark DP01 stale and alert the data steward daily" with reason "add the daily stale alert for DP01" on 2026-11-18
    Then field "DF-ACE-018" is at version 2 dated 2026-11-18 with that reason
    Then version 1 stays readable with its own date and late behavior
    When the data steward sends a further change with an empty reason
    Then the system refuses the call with status 422 and MSG-GEN-001 for field "reason"
    Then field "DF-ACE-018" stays at version 2

  Scenario: AC6 The ACE read path is agreed before it is published
    Given the data steward recorded the confirmation of "DC-ACE" by role "ACE team lead" on 2026-11-12 with document reference "DOC-SYN-0640"
    When the data steward publishes "DC-ACE"
    Then the contract status is "PUBLISHED" with version 1 and the confirmation on 2026-11-12
    Then the contract lists 304 fields and the read interfaces "V0002" and "V0003"
    When a contract "DC-ACE-2" has no recorded confirmation and the data steward publishes it
    Then the system refuses the call with status 409 and MSG-P1-021 for system "ACE"

  Scenario: AC7 Two changes to the same field at once
    Given two data stewards read field "DF-ACE-020" at version 1
    When both send a change with version 1
    Then the system saves the first change as version 2
    Then the system refuses the second with status 409 and MSG-GEN-004
    When a third steward sends a change with no If-Match version
    Then the system refuses it with status 428 and MSG-GEN-004

  Scenario: AC8 A change to a field in a published contract
    Given contract "DC-ACE" is "PUBLISHED" at version 1
    When field "DF-ACE-018" changes to version 2
    Then the system creates contract "DC-ACE" version 2 as "DRAFT"
    Then version 1 stays "PUBLISHED" and in force
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every field carries its data type, physical type, source system, owner role, refresh cycle and behavior when late, and every view field names its ACE column as `public.table.column`, or, for the 7 derived view fields, states that the view derives it | REQ-RDF-001; sys_fields |
| BR2 | The dictionary holds 122 objects and 1,366 fields: 92 tables with 1,062 fields, 49 of them on the four extension tables, and 30 views with 304 fields, 177 in Section A and 127 in Section B | D-RCV-35; Data Tier Map v1 section 8 |
| BR3 | Each data product has exactly one system of record and one owner role; a source is either an ACE column recorded on a view field or the Workbench itself | REQ-RDF-001; data_product; D-RCV-35 U1 |
| BR4 | A data contract is published only after its confirming role is recorded with a date and a stored document reference | DL12; data_contract |
| BR5 | A field change creates a new `sys_field_version` row with a date and a reason; earlier versions stay readable | Reference data change process; DT02; Principle 1 |
| BR6 | A dictionary load with an exception is refused in full; an ACE source field that is not a column of the view is an exception unless the view derives it | Reference data change process, step 3; CTL-08 |
| BR7 | A change to a field of a published contract opens a new contract version; the published version stays in force until the new one is confirmed and published | R-UNI-38 |
| BR8 | V0001 owns `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract`; this story adds no table, column, index or constraint and publishes rows only through RWB-E1-043 and the endpoints | RWB-E1-001; D-RCV-28 |
| BR9 | A new ACE column reaches the dictionary as a reference load after its view column exists; an applied migration is never edited, and CHK-01 blocks the merge until the row exists | RWB-E1-069; BR-P1-001 |

## 9. State transitions

None. This story does not change a case status. It changes the data contract status: DRAFT to PUBLISHED after the confirming role is recorded, and a new DRAFT version when a field of a published contract changes. Each field change adds a version; earlier versions stay readable.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Changes field definitions, records the confirmation, publishes the contract (Reference data U) |
| RW-REFADM, reference data administrator | Submits the dictionary load (Reference data C) |
| RW-COE, center of excellence analyst | Reads and changes field definitions (Reference data CRUD) |
| ACE team lead | Confirms the ACE read contract; owns the ACE columns it names (RWB-ACE-001) |
| RW-TRIBE, RW-AUDIT and other roles with Reference data R | Read the dictionary and the contracts |
| SY-DATALOAD, data load | Applies an approved dictionary load |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-088 | sys_objects | object_name | Read |
| DF-REF-091 | sys_objects | data_product | Read |
| DF-REF-092 | sys_objects | system_of_record | Read |
| DF-REF-095 | sys_fields | field_id | Read |
| DF-REF-096 | sys_fields | object_name | Read |
| DF-REF-097 | sys_fields | field_name | Read |
| DF-REF-098 | sys_fields | data_type | Write |
| DF-REF-099 | sys_fields | physical_type | Write |
| DF-REF-103 | sys_fields | source_system | Write |
| DF-REF-104 | sys_fields | source_field | Write |
| DF-REF-105 | sys_fields | is_personal | Read |
| DF-REF-106 | sys_fields | description | Write |
| DF-REF-107 | sys_fields | owner_role | Write |
| DF-REF-108 | sys_fields | refresh_cycle | Write |
| DF-REF-109 | sys_fields | late_behavior | Write |
| DF-REF-110 | sys_fields | interface_id | Write |
| DF-REF-111 to DF-REF-115 | sys_field_version | all fields | Write |
| DF-OPS-010 to DF-OPS-020 | data_contract | all fields | Write |
| DF-REF-070 to DF-REF-079 | data_product | all fields | Read |

`sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` exist in Recovery Workbench Physical Schema v5.sql and are created by V0001. This story writes rows, not DDL. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Endpoints**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /admin/data-dictionary/fields | Query: product, entity, field, sourceSystem, page, size | DataDictionaryFieldPage: items of DataDictionaryField (fieldId, entity, fieldName, dataType, physicalType, mandatory, listCode, sourceSystem, sourceField, refreshCycle, ownerRole, lateBehavior, interfaceId, isPersonal, version, versionDate) and the object and field counts | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 (MSG-GEN-006) | Reference data, R | Not applicable |
| PATCH /admin/data-dictionary/fields/{fieldCode} | Header If-Match: version; body DataDictionaryFieldChange (changed attributes, reason) | DataDictionaryField | 403; 404 unknown field (MSG-P4-003); 409 stale version (MSG-GEN-004); 422 reason empty (MSG-GEN-001); 428 no If-Match (MSG-GEN-004) | Reference data, U | If-Match version |
| GET /admin/data-contracts | Query: sourceSystem, status | DataContract[] (id, contractCode, sourceSystem, interfaceId, contractVersion, status, fieldCount, confirmedByRole, confirmedOn, confirmationDocumentRef, publishedAt) | 401; 403; 503 | Reference data, R | Not applicable |
| PATCH /admin/data-contracts/{contractId} | Header If-Match; body DataContractConfirmation (confirmedByRole, confirmedOn, confirmationDocumentRef) | DataContract | 403; 404; 409 (MSG-GEN-004); 422 field empty (MSG-GEN-001) | Reference data, U | If-Match version |
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
    List<DataDictionaryField> fieldsOf(String objectName);
    DataProductDefinition product(String productCode);
    DictionaryCounts counts(); // 122 objects, 1,366 fields, 304 view fields, 49 extension fields
}
```

## 13. Solution plan

- Package: folder `recovery/dataengine/dictionary`, Java package `recovery.dataengine.dictionary`.

| Component | Type | Responsibility |
|---|---|---|
| DataDictionaryController | Controller | The five endpoints in section 12 |
| DataDictionaryService | Service | Field reads, versioned changes with reason, optimistic lock, object and field counts |
| DataContractService | Service | The ACE read contract; confirmation; publish rule; new version on change |
| DataDictionaryLoader | Published interface | Whole-load validation and apply; source and view column checks |
| DataDictionaryQuery | Published interface | Field and product definitions for other packages and modules |
| SysFieldRepository, SysFieldVersionRepository, DataContractRepository, DataProductRepository | Repository | Read and write the five tables |
| SysField, SysFieldVersion, DataContract, DataProduct | Entity | One per table |

- Database: no DDL. V0001 created `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` with the 122 and 1,366 seed rows. This story writes only rows, through the reference load and the endpoints.
- Configuration and reference data: the governance load prepared by the data steward from `v_data_dictionary` and the 30 view definitions; data_product owners confirmed by each product owner (BRD Epic 1 section 5); expected_by times assumed 08:00 for daily ACE products and Monday 08:00 for weekly ACE products (DL11).
- Build steps:
  1. Read the 122 objects and 1,366 fields from `v_data_dictionary`; confirm the counts and the 30 view rows. No migration.
  2. DataDictionaryLoader with whole-load validation of the six attributes, the source system and the view column; refusal with MSG-P1-002 and the first failing check.
  3. DataDictionaryService change with If-Match and a mandatory reason; one `sys_field_version` row per change.
  4. DataContractService: DC-ACE from the 304 ACE fields; confirmation record; publish rule with MSG-P1-021; new DRAFT on a field change.
  5. DataDictionaryController and the contract tests for the endpoints (RWB-TE-003).
  6. Prepare and load the governance file through RWB-E1-043; confirm the ACE team's confirmation and publish DC-ACE.
  7. Tests for AC1 to AC8 and the access test.
- Feature flag: `rwb.dataengine.data-dictionary`.
- Done when: the tests in section 16 pass, all 30 views have dictionary rows in SIT, and DC-ACE is PUBLISHED.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-021 | Publish of a contract with no confirmation | The data contract for {system} cannot be published until its confirming role records the confirmation. |
| MSG-GEN-001 | Reason or confirmation field empty | Enter {field}. |
| MSG-GEN-004 | Change from an old version, or no If-Match version | Someone else changed this record. Reload it to see their change. |
| MSG-P1-002 | Dictionary load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | The store or a view is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without Reference data U | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. Developers and analysts read the dictionary through GET /admin/data-dictionary/fields; SCR-40 Reference data shows versioned tables from Epic 8, and until then changes go by file load or the endpoints.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-064-01 | AC1, BR1, BR2 | System | Seeded 122 objects and 1,366 fields; count and completeness queries |
| TC-E1-064-02 | AC2, BR2 | System | 30 views, 304 fields; one view column with no dictionary row |
| TC-E1-064-03 | AC3, BR1, BR3 | System | Account ACC0000017 with delay_days 95; dictionary query for DF-ACE-018 |
| TC-E1-064-04 | AC4, BR6, BR9 | System | Dictionary fixture without DF-ACE-204; load with the correct and the wrong ACE column |
| TC-E1-064-05 | AC5, BR5 | System | Change of DF-ACE-018 late behavior with a reason and with an empty reason |
| TC-E1-064-06 | AC6, BR4 | System | DC-ACE with 304 fields; confirmation on 2026-11-12; a second contract with no confirmation |
| TC-E1-064-07 | AC7 | System | Two changes to DF-ACE-020 from version 1; one change with no If-Match |
| TC-E1-064-08 | AC8, BR7 | System | Published DC-ACE and a change to DF-ACE-018 |
| TC-E1-064-09 | Access | Access | RW-TRIBE sends PATCH /admin/data-dictionary/fields/DF-ACE-018; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: owners, cycles, late behavior and contract content are data rows.
- No personal data in logs, tests or prompts: the dictionary holds definitions, not values; the confirmation names a role, not a person.
- No read of another module's tables: other modules use DataDictionaryQuery. The only public schema names in the story are the ACE column names recorded in the dictionary, which no recovery class reads directly.
- A published contract is never edited in place; a change makes a new version.
- No DDL: V0001 owns the five tables; this story never adds or alters a column.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner | Business Requirements Epic 1, sections 3.1, 4 and 5 | None | All recovery processes | CTL-08; DL12; D-RCV-35 U1 | TC-E1-064-01, TC-E1-064-02, TC-E1-064-03, TC-E1-064-06, TC-E1-064-09 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record and refresh | Business Requirements Epic 1, sections 3.1 and 4 | None | All recovery processes | R-UNI-38 | TC-E1-064-04, TC-E1-064-05, TC-E1-064-07, TC-E1-064-08 |

## 19. Out of scope

- The tables, the seed and the dictionary view: RWB-E1-001.
- The 30 ACE views, their grants and the view conformance test: RWB-E1-069.
- The catalog endpoint, access by product and PDPA masking: RWB-E1-016.
- Freshness stamps per data product: RWB-E1-015.
- Retention per product and table: RWB-E1-017.
- The reference data screen SCR-40: Epic 8.
- Contracts for stage 2 data products: RWB-E2-010.
