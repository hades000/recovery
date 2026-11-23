<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 001 Recovery tables for the 14 data products v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 001 Recovery tables for the 14 data products v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-001 Recovery tables for the 14 data products

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-001 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-01 Create the recovery tables in the ACE database; FEAT-RDF-02 Define the 14 data products and their systems of record |
| Requirement IDs | REQ-RDF-001 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-044, RWB-E1-043 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the recovery tables for the 14 data products created in the ACE database, with a data dictionary and one system of record and one owner per data product**, so that **every later load has one target table and one accountable owner**.

## 2. Business rationale

Recovery data is held today in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy. This story creates the 43 recovery tables from the physical schema, the metadata registry that holds the data dictionary as data, and the catalog of the 14 data products DP01 to DP14. Each data product then has exactly one system of record and one named owner, as REQ-RDF-001 requires. The measure it serves is "loads on time and complete on 99 percent of days" (FSD P1 A2.1), because no load can start until its target table and owner exist.

## 3. Preconditions

- RWB-E1-044 is done: Flyway runs in the ACE pipeline and takes the schema name from the parameter `recoverySchema`.
- RWB-E1-043 is done: the reference data service accepts a validated load for a table code and calls the handler that the owning module provides.
- The DEV and SIT databases of the ACE service exist and the pipeline service identity may run migrations in the recovery schema.
- The reference data administrator (RW-REFADM) holds Reference data C. The person who queries the dictionary view has read access to the recovery schema in DEV or SIT.
- The catalog load file for the 14 data products is prepared from the seed values in section 13, with an owner user ID for each product in that environment (synthetic test users in DEV and SIT).

## 4. Flow

1. Pipeline: runs migration `V1_001__recovery_schema.sql` in DEV with `recoverySchema = recovery`.
2. Migration: creates the 43 tables, the 68 foreign keys, the 76 indexes and the append-only triggers on decision_log_entry and interaction, and the new table data_product, in one transaction.
3. Migration: inserts the 41 sys_objects rows, the 413 sys_fields rows and the 14 data_product seed rows (section 13), and creates the view `v_data_dictionary`.
4. Pipeline: runs the dictionary conformance test, which compares every column in the recovery schema with sys_fields.
5. Pipeline: repeats steps 1 to 4 in SIT.
6. Reference data administrator: loads the data product catalog file with table code `data_product` through `POST /admin/reference-loads`, naming the owner user ID of each product for the environment.
7. System: `DataProductCatalogHandler.validate` checks the file: 14 products DP01 to DP14, each with one system of record, one owner role from LOV-ROLE, one owner user ID and one refresh cycle.
8. Data steward: confirms the load as owner of the catalog through the reference data change process (RWB-E1-043).
9. System: `DataProductCatalogHandler.apply` writes the 14 rows in one transaction with the valid from date.
10. Developer or data steward: queries `v_data_dictionary` for entity loan_account and field days_past_due.
11. System: returns field ID DF-ACC-014, the types, the source system and source field, the data product, its refresh cycle and its owner.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A statement in the migration fails | The transaction rolls back; no table is left half created; the pipeline stage fails with the statement named | None (pipeline log) | AC4 |
| X2 | A column exists with no sys_fields row, or a sys_fields row has no column or a different physical type | The conformance test fails and names the table, the column and the field ID | None (pipeline log) | AC5 |
| X3 | The migration runs again on a schema where it is already applied | Flyway skips it; no table or row changes | None | AC6 |
| X4 | A catalog row names no system of record, two systems of record, or no owner user ID | The whole load is refused; no row is written | MSG-P1-003 | AC7 |
| X5 | The catalog file does not hold exactly the 14 products DP01 to DP14 | The whole load is refused | MSG-P1-004 | AC8 |
| X6 | A catalog row names an owner role or refresh cycle outside its list | The whole load is refused | MSG-P1-007 | AC9 |
| X7 | The same catalog file is loaded again | Nothing is written; the load is reported as already done | MSG-P1-011 | AC10 |
| X8 | A role without Reference data C loads the catalog | 403 Problem response; the refusal is in the access log | MSG-P4-002 | TC-E1-001-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the migration tooling (RWB-E1-044) and the reference load service (RWB-E1-043); every load story and the data dictionary story (RWB-E1-064) build on this one |
| Negotiable | The catalog values (names, owners, refresh cycles) are data in a load file; the story fixes the tables and the checks |
| Valuable | Gives every later load one target and every data product one accountable owner |
| Estimable | One migration, one view, one conformance test, one reference table handler |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: Recovery tables for the 14 data products

  Scenario: AC1 Schema deployed
    Given the migration V1_001__recovery_schema.sql and the parameter recoverySchema = "recovery"
    When the pipeline applies it in DEV and then in SIT
    Then the recovery schema in each environment holds 44 tables: the 41 tables of the data products, sys_objects and sys_fields which hold the data dictionary, and data_product which is the catalog
    Then the table loan_account has the 24 columns DF-ACC-001 to DF-ACC-021 and DF-ACC-029 to DF-ACC-031, plus the 7 standard columns
    Then the conformance test reports 413 of the 413 fields of these tables matched by name and physical type

  Scenario: AC2 Dictionary published
    Given the data dictionary and the data product seed loaded by the migration, and the catalog loaded for DP01
    When a developer queries v_data_dictionary for entity "loan_account" and field "days_past_due"
    Then the row holds field ID "DF-ACC-014", data type "NUMBER", physical type "integer"
    Then source system "Core bank (ALS) via COLLINS", source field "DELAY_DAYS"
    Then data product "DP01", refresh cycle "DAILY", owner role "RW-DATASTEW" and the owner user ID of DP01

  Scenario: AC3 One system of record
    Given a catalog load file with the 14 rows DP01 to DP14, each with one system of record and one owner user ID
    When the reference data administrator loads it with valid from 2026-11-20
    Then data_product holds 14 rows
    Then each row has exactly one system of record and one owner user ID
    Then the catalog for DP06 names system of record "CCMS" and refresh cycle "WEEKLY"

  Scenario: AC4 Failed migration leaves no partial schema
    Given a copy of the migration in which the statement creating table valuation fails
    When the pipeline applies it in DEV
    Then the pipeline stage fails and names the failing statement
    Then the recovery schema holds none of the tables of that migration
    Then the Flyway history has no successful row for version 1.001

  Scenario: AC5 Column without a dictionary entry fails the build
    Given a branch that adds the column loan_account.branch_code with no sys_fields row
    When the conformance test runs in the pipeline
    Then the test fails with "loan_account.branch_code has no data dictionary entry"
    Then a sys_fields row DF-ACC-021 whose column is changed to type text fails the test with "DF-ACC-021 physical type date expected, text found"

  Scenario: AC6 Repeated migration has no effect
    Given the migration version 1.001 already applied in SIT
    When the pipeline runs again in SIT
    Then Flyway reports version 1.001 as already applied
    Then the row counts of sys_objects (41) and sys_fields (413) are unchanged

  Scenario: AC7 Catalog row with two systems of record is refused
    Given a catalog load file in which DP06 names system of record "CCMS; SVAF"
    Given DP11 has no owner user ID
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-003 for DP06 and for DP11
    Then data_product keeps the rows of the version in force

  Scenario: AC8 Catalog with a missing product is refused
    Given a catalog load file with 13 rows and no row for DP09
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-004 naming "DP09"
    Then the system writes no row

  Scenario: AC9 Value outside its list
    Given a catalog load file in which row 4 (DP04) names owner role "DP_OWNER" and row 5 (DP05) names refresh cycle "HOURLY"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-007 "Row 4: owner_role must be one of the role codes in LOV-ROLE." and "Row 5: refresh_cycle must be one of DAILY, WEEKLY, MONTHLY, ON_CHANGE."

  Scenario: AC10 Same catalog file loaded again
    Given the catalog version loaded on 2026-11-20 is in force
    When the reference data administrator loads the same file again
    Then the system writes nothing
    Then the response carries MSG-P1-011 "The data product catalog load for 2026-11-20 is already complete or running. It was not run again."
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every table and column in the recovery schema has exactly one row in the data dictionary, with its BR Field ID, types, source system and meaning | Logical Data Model and Data Dictionary; sys_fields |
| BR2 | Recovery data is held in the 14 data products DP01 to DP14 | REQ-RDF-001; sys_objects.data_product |
| BR3 | Each data product has exactly one system of record and one named owner | REQ-RDF-001 |
| BR4 | The catalog values are a versioned data load, changed without a code release; a load with an exception is refused in full | Principle 1; DT02; CTL-08 |
| BR5 | Where the entities of one product name more than one source (DP06, DP07, DP13), the catalog names one accountable system of record; the seed values in section 13 are assumed until the data steward confirms them | DL12 |
| BR6 | Schema names come from parameters; one migration per story; forward only in PROD | RWB-E1-044 |
| BR7 | Personal fields carry is_personal = true in the dictionary so masking (RWB-E1-016) can read them | sys_fields.is_personal; CTL-11 |

## 9. State transitions

None. This story does not change a case status. It changes the Flyway version of the recovery schema (none to 1.001) and the version of the data product catalog (none to the first loaded version).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| Pipeline service identity (ACE pipeline) | Runs the migration and the conformance test in DEV and SIT |
| RW-REFADM, reference data administrator | Loads the catalog file (Reference data C) |
| RW-DATASTEW, data steward and data product owner | Confirms the catalog version as its owner (Reference data U); cannot load it (no Reference data C) |
| Developers and the data steward in DEV and SIT | Query v_data_dictionary with read access to the recovery schema |
| Any role without Reference data C | Refused with MSG-P4-002 on the catalog load |

No approval level from the delegation of authority applies.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Create (table) |
| DF-CAS-024 to DF-CAS-029 | case_account | all fields | Create (table) |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Create (table) |
| DF-CAS-036 to DF-CAS-045 | deviation | all fields | Create (table) |
| DF-WRK-001 to DF-WRK-008 | queue | all fields | Create (table) |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Create (table) |
| DF-WRK-017 to DF-WRK-026 | task | all fields | Create (table) |
| DF-WRK-027 to DF-WRK-036 | timer | all fields | Create (table) |
| DF-PTY-001 to DF-PTY-012 | party | all fields | Create (table) |
| DF-PTY-013 to DF-PTY-020 | contact_point | all fields | Create (table) |
| DF-ACC-001 to DF-ACC-021 | loan_account | all fields | Create (table) |
| DF-ACC-022 to DF-ACC-028 | account_payment | all fields | Create (table) |
| DF-COL-001 to DF-COL-013 | collateral | all fields | Create (table) |
| DF-COL-014 to DF-COL-017 | account_collateral | all fields | Create (table) |
| DF-COL-018 to DF-COL-027 | valuation | all fields | Create (table) |
| DF-COL-028 to DF-COL-042 | asset | all fields | Create (table) |
| DF-TRT-001 to DF-TRT-014 | treatment | all fields | Create (table) |
| DF-TRT-015 to DF-TRT-022 | guarantee_claim | all fields | Create (table) |
| DF-LEG-001 to DF-LEG-014 | legal_action | all fields | Create (table) |
| DF-LEG-015 to DF-LEG-023 | notice | all fields | Create (table) |
| DF-LEG-024 to DF-LEG-029 | hearing | all fields | Create (table) |
| DF-PRT-001 to DF-PRT-007 | partner | all fields | Create (table) |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | all fields | Create (table) |
| DF-SAL-001 to DF-SAL-008 | listing | all fields | Create (table) |
| DF-SAL-009 to DF-SAL-019 | asset_sale | all fields | Create (table) |
| DF-SAL-020 to DF-SAL-030 | debt_sale_lot | all fields | Create (table) |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account | all fields | Create (table) |
| DF-INT-001 to DF-INT-013 | interaction | all fields | Create (table) |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Create (table) |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Create (table) |
| DF-DOC-018 to DF-DOC-024 | document_custody | all fields | Create (table) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Create (table only; no entry is written) |
| DF-DEC-019 to DF-DEC-027 | score | all fields | Create (table) |
| DF-FIN-001 to DF-FIN-009 | proceeds | all fields | Create (table) |
| DF-FIN-010 to DF-FIN-020 | write_off | all fields | Create (table) |
| DF-REF-001 to DF-REF-015 | rule_row | all fields | Create (table) |
| DF-REF-016 to DF-REF-026 | delegation_limit | all fields | Create (table) |
| DF-REF-027 to DF-REF-033 | lov_value | all fields | Create (table) |
| DF-REF-034 to DF-REF-039 | role | all fields | Create (table) |
| DF-REF-040 to DF-REF-044 | permission | all fields | Create (table) |
| DF-REF-045 to DF-REF-051 | template | all fields | Create (table) |
| DF-REF-088 | sys_objects | object_name | Create and write 108 rows; read |
| DF-REF-089 | sys_objects | business_name | Create and write 108 rows; read |
| DF-REF-090 | sys_objects | subject_area | Create and write 108 rows; read |
| DF-REF-091 | sys_objects | data_product | Create and write 108 rows; read |
| DF-REF-092 | sys_objects | system_of_record | Create and write 108 rows; read |
| DF-REF-093 | sys_objects | description | Create and write 108 rows; read |
| DF-REF-095 | sys_fields | field_id | Create and write 1,256 rows; read |
| DF-REF-096 | sys_fields | object_name | Create and write 1,256 rows; read |
| DF-REF-097 | sys_fields | field_name | Create and write 1,256 rows; read |
| DF-REF-098 | sys_fields | data_type | Create and write 1,256 rows; read |
| DF-REF-099 | sys_fields | physical_type | Create and write 1,256 rows; read |
| DF-REF-100 | sys_fields | is_mandatory | Create and write 1,256 rows; read |
| DF-REF-101 | sys_fields | lov_code | Create and write 1,256 rows; read |
| DF-REF-103 | sys_fields | source_system | Create and write 1,256 rows; read |
| DF-REF-104 | sys_fields | source_field | Create and write 1,256 rows; read |
| DF-REF-105 | sys_fields | is_personal | Create and write 1,256 rows; read |
| DF-REF-106 | sys_fields | description | Create and write 1,256 rows; read |
| DF-REF-071 | data_product | product_code | Create and write |
| DF-REF-072 | data_product | product_name | Create and write |
| DF-REF-073 | data_product | definition | Create and write |
| DF-REF-074 | data_product | system_of_record | Create and write |
| DF-REF-075 | data_product | owner_role | Create and write |
| DF-REF-076 | data_product | owner_user_id | Create and write |
| DF-REF-077 | data_product | refresh_cycle | Create and write |
| DF-REF-078 | data_product | expected_by | Create and write |
| DF-REF-079 | data_product | valid_from | Create and write |

Field IDs are those in the Logical Data Model and Data Dictionary.

Open point, logged as DL41 for the data architect. Step 3 and AC6 seed 41 `sys_objects` rows and 413 `sys_fields` rows, the entities and fields of this migration. The table above, RWB-E1-016 and RWB-E1-064 assume the dictionary already holds all 108 entities and 1,256 fields of the recovery module. Build to 41 and 413 only once the ruling is recorded in Recovery Workbench Decision Log v8.xlsx.

## 12. Contract

**Dictionary view** `v_data_dictionary` (read model created by the migration; RWB-E1-064 builds the dictionary endpoint on it)

| Column | From |
|---|---|
| field_id, entity, field, data_type, physical_type, mandatory, lov_code, source_system, source_field, personal | sys_fields |
| data_product, entity_system_of_record | sys_objects |
| product_system_of_record, refresh_cycle, owner_role, owner_user_id | data_product |

**Reference load handler** (published interface of P4 that P1 implements, from RWB-E1-043)

```java
public interface ReferenceTableHandler {
    String tableCode();                                              // returns "data_product"
    ValidationReport validate(ReferenceLoadFile file);               // checks every row, writes nothing
    int apply(UUID loadId, ReferenceLoadFile file, LocalDate validFrom); // writes all rows in one transaction, returns the row count
}
```

The load itself is `POST /admin/reference-loads` (P4, Reference data C) with `table = data_product`, and its response is `ReferenceLoad`. A refused load returns 422 with MSG-P1-003, MSG-P1-004 or MSG-P1-007 in the Problem response; a caller without Reference data C gets 403 with MSG-P4-002. Idempotency: a file whose content hash matches the version in force is reported with MSG-P1-011 and writes nothing.

**Migration**

| Item | Value |
|---|---|
| Trigger | The ACE pipeline, on each deployment to DEV and SIT |
| Name | `V1_001__recovery_schema.sql` with placeholder `${recoverySchema}` |
| Idempotency | The Flyway version 1.001; a changed checksum on an applied version fails the pipeline |
| Restart | A failed run rolls back; the next run applies the full version again |

## 13. Solution plan

**Package.** Folder `recovery/dataengine/catalog`, Java package `recovery.dataengine.catalog`; migration in `src/main/resources/db/migration/recovery`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| V1_001__recovery_schema.sql | Flyway migration | Creates the 43 tables of the physical schema, data_product, the references, indexes, triggers and v_data_dictionary; inserts sys_objects, sys_fields and the 14 data_product seed rows |
| DataDictionaryConformanceTest | Test (pipeline) | Compares information_schema.columns with sys_fields in both directions, ignoring the 7 standard columns |
| DataProduct | Entity | Maps data_product |
| DataProductRepository | Repository | Reads and writes data_product |
| DataProductCatalogHandler | Published interface implementation | Implements ReferenceTableHandler for table code `data_product` |

**Database.** Creates every table in the physical schema. Creates data_product with the columns RWB-E1-064 also uses: product_code varchar(4) primary key, product_name varchar(80) not null, definition varchar(400), owner_role varchar(20) not null, system_of_record varchar(120) not null, refresh_cycle varchar(10) not null check in ('DAILY','WEEKLY','MONTHLY','ON_CHANGE'), expected_by varchar(20), plus owner_user_id uuid (null in the seed, required by the catalog load) and valid_from date, and the 7 standard columns. Creates v_data_dictionary. Adds a foreign key from sys_objects.data_product to data_product.product_code; the migration inserts the data_product seed rows before the sys_objects rows.

**Configuration and reference data.** Parameter `recoverySchema` per environment (platform administrator). Seed values inserted by the migration and repeated in the first catalog load file, with the owner user IDs, prepared by the reference data administrator and confirmed by the data steward:

| Product | Name | System of record | Refresh cycle |
|---|---|---|---|
| DP01 | Account and arrears | Core bank (ALS) via COLLINS | DAILY |
| DP02 | Customer and party | SCBPDM via COLLINS | DAILY |
| DP03 | Case and work management | Workbench | DAILY |
| DP04 | Treatment | Workbench | DAILY |
| DP05 | Interaction | Workbench | DAILY |
| DP06 | Collateral and asset | CCMS (assumed, DL12) | WEEKLY |
| DP07 | Legal | LIT via COLLINS (assumed, DL12) | DAILY |
| DP08 | Partner | Workbench | DAILY |
| DP09 | Debt sale | Workbench | DAILY |
| DP10 | Document | Workbench document hub | DAILY |
| DP11 | Score | COLLINS | DAILY |
| DP12 | Decision log | Workbench | DAILY |
| DP13 | Money and closure | Workbench (assumed, DL12) | DAILY |
| DP14 | Reference and access | Workbench | DAILY |

Owner role RW-DATASTEW for every product; owner user IDs per environment.

**Build steps**

Open point, logged as DL42 for the ACE tech lead, needed by 2 November. This story names the migration file V1_001__recovery_schema.sql with the placeholder ${recoverySchema}. RWB-E1-044, which sets the migration rule for the module, names the baseline V1__rwb_e1_001_baseline.sql with the placeholder ${schema} fed by the environment value RWB_SCHEMA. Write the file to the names above and change them once the ruling is recorded in Recovery Workbench Decision Log v8.xlsx.

1. Write `V1_001__recovery_schema.sql` from the physical schema, with `${recoverySchema}` in place of the fixed schema name, plus data_product with its 14 seed rows and v_data_dictionary; run it on an empty PostgreSQL container.
2. Write DataDictionaryConformanceTest and add it to the pipeline after the migration stage; prove it fails on an extra column and on a changed type.
3. Write DataProduct, DataProductRepository and DataProductCatalogHandler with the checks for BR2, BR3 and the list values; unit test the checks for X4, X5 and X6.
4. Connect the handler to the reference data service of RWB-E1-043 and test a full load, a refused load and a repeated file against a container database.
5. Write a test that reads v_data_dictionary for loan_account.days_past_due after a catalog load.
6. Add messages MSG-P1-003, MSG-P1-004, MSG-P1-007 and MSG-P1-011 to the message table with English and Thai text.

**Feature flag.** `rwb.p1.data-catalog`. The flag covers the catalog handler; the migration is not behind a flag.

**Done when.** The tests in section 16 pass, the migration runs clean in DEV and SIT, and the catalog version for SIT holds 14 rows.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-003 | Catalog row with no system of record, more than one, or no owner | {product} must have exactly one system of record and one named owner. |
| MSG-P1-004 | Catalog file without exactly DP01 to DP14 | The catalog must hold the 14 data products DP01 to DP14. Missing: {products}. |
| MSG-P1-007 | Catalog value outside its list | Row {row}: {field} must be one of {values}. |
| MSG-P1-011 | Same catalog file loaded again | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Role without Reference data C | You cannot {action} here. Your role does not include it. |

Thai text for each new message follows DL10 and is in the additions file.

## 15. Screens and states

No screen in this story. The pipeline log shows the migration and conformance results. Developers read the dictionary through v_data_dictionary; the dictionary endpoint comes with RWB-E1-064, the catalog entries with RWB-E1-016, and SCR-40 Reference data in E8.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-001-01 | AC1, BR1, BR6 | System | Empty DEV and SIT schemas; schema parameter "recovery" |
| TC-E1-001-02 | AC2, BR1 | System | Dictionary from the migration; catalog with a synthetic owner for DP01 |
| TC-E1-001-03 | AC3, BR2, BR3, BR5 | System | Catalog file of 14 rows from the seed table |
| TC-E1-001-04 | AC4 | System | Migration copy with a failing CREATE TABLE valuation |
| TC-E1-001-05 | AC5, BR1 | System | Branch with loan_account.branch_code; changed type on DF-ACC-021 |
| TC-E1-001-06 | AC6 | System | SIT schema at version 1.001 |
| TC-E1-001-07 | AC7, BR3, BR4 | System | Catalog file with DP06 naming two systems and DP11 with no owner |
| TC-E1-001-08 | AC8, BR2, BR4 | System | Catalog file of 13 rows without DP09 |
| TC-E1-001-09 | AC9, BR4 | System | Catalog file with owner role DP_OWNER and refresh cycle HOURLY |
| TC-E1-001-10 | AC10, BR4 | System | Same catalog file loaded twice |
| TC-E1-001-11 | Access | Access | RW-DATASTEW calls POST /admin/reference-loads with table data_product; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: product names, systems of record, owners and refresh cycles come from the catalog load.
- No personal data in logs, tests or prompts. Owner user IDs in DEV and SIT are synthetic test users.
- No read of another module's tables. The dictionary reads only sys_objects, sys_fields and data_product.
- The migration changes no data outside the recovery schema and never drops a table in PROD.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, one system of record and one owner each | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-01, FEAT-RDF-02 | All recovery processes | CTL-08; Principle 1 | TC-E1-001-01 to TC-E1-001-11 |

## 19. Out of scope

- Freshness stamp per data product (RWB-E1-015).
- Access control per data product, PDPA masking and the catalog entry screen (RWB-E1-016).
- Retention and archive rules (RWB-E1-017).
- Stage 2 data products for contracts, plans and treatments (REQ-RDF-014, Epic 2).
- The dictionary endpoint, field versions and data contracts with each system owner (RWB-E1-064).
