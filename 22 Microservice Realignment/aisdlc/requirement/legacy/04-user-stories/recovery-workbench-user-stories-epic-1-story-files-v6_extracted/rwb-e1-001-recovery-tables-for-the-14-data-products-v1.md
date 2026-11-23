<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 001 Recovery tables for the 14 data products v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 001 Recovery tables for the 14 data products v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-001 Recovery tables for the 14 data products

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-001 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-01 Create the recovery tables and extension tables in the ACE database; FEAT-RDF-02 Define the 14 data products and their systems of record |
| Requirement IDs | REQ-RDF-001 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | All recovery processes |
| Decision | D-RCV-35 (U1 to U5); ADR-010; DL43 open |
| Priority | Must |
| Depends on | RWB-E1-044, RWB-E1-043 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the 92 recovery tables for the 14 data products created in the ACE database, with a data dictionary that covers those tables and the 30 read-only ACE views, and one system of record and one owner per data product**, so that **every Workbench record has one home and every data product has one accountable owner and one read path**.

## 2. Business rationale

The Workbench holds no copy of source data. ACE ingests ALS, SCBPDM, EFS, COLLINS, CCMS, SVAF, AMIS, RPS, LIT, WIN, GL, NLEADS, EasyApp and Entra ID, and the Workbench reads what it needs through the 30 `recovery.v_ace_*` views (D-RCV-35 U1 and U4, ADR-010). This story creates the 88 Workbench tables, the four extension tables that hold a Workbench decision about an ACE record, the metadata registry that holds the data dictionary as data, and the catalog of the 14 data products DP01 to DP14. Each data product then has exactly one system of record, written "ACE (ingested from X)" for source data, "Recovery Workbench" for Workbench records, or one sentence naming both where the product holds both, and one named owner, as REQ-RDF-001 requires. The measure it serves is "the ACE batch is complete when the Workbench reads it on 99 percent of days", because the dictionary and the catalog are what every later read and every freshness stamp are resolved against.

## 3. Preconditions

- RWB-E1-044 is done: Flyway runs in the ACE pipeline and takes the schema name from the parameter `recoverySchema`.
- RWB-E1-043 is done: the reference data service accepts a validated load for a table code and calls the handler that the owning module provides.
- The DEV and SIT databases of the ACE service exist and the pipeline service identity may run migrations in the recovery schema.
- The reference data administrator (RW-REFADM) holds Reference data C. The person who queries the dictionary view has read access to the recovery schema in DEV or SIT.
- The catalog load file for the 14 data products is prepared from the seed table in section 13, with an owner user ID for each product in that environment (synthetic test users in DEV and SIT).
- The Section A and Section B views are not created here. RWB-E1-069 ships the 16 Section A views as V0002 after V0001, and the 14 Section B views as V0003 once RWB-ACE-001 lands (DL43).

## 4. Flow

1. Pipeline: runs migration `V0001__rwb_e1_001_recovery_schema.sql` in DEV with `recoverySchema = recovery`.
2. Migration: creates the 92 tables (the 88 Workbench tables and the four extension tables), their indexes, the append-only triggers on `decision_log_entry` and `interaction`, and the catalog table `data_product`, in one transaction.
3. Migration: inserts the 14 `data_product` rows, then the 122 `sys_objects` rows and the 1,366 `sys_fields` rows (section 13), and creates the view `v_data_dictionary`.
4. Migration: adds `fk_sys_objects_data_product`; `sys_objects.data_product` is nullable, so the 24 operational objects of OPS, AGT and RPT carry no product.
5. Pipeline: runs the dictionary conformance test, which compares every column of the 92 tables in the recovery schema with `sys_fields` (1,062 fields).
6. Pipeline: repeats steps 1 to 5 in SIT.
7. Reference data administrator: loads the data product catalog file with table code `data_product` through `POST /admin/reference-loads`, naming the owner user ID of each product for the environment.
8. System: `DataProductCatalogHandler.validate` checks the file: 14 products DP01 to DP14, each with one system of record written "ACE (ingested from X)", "Recovery Workbench" or one sentence naming both, one owner role from LOV-ROLE, one owner user ID and one refresh cycle.
9. Data steward: confirms the load as owner of the catalog through the reference data change process (RWB-E1-043).
10. System: `DataProductCatalogHandler.apply` writes the 14 rows in one transaction with the valid from date.
11. Developer or data steward: queries `v_data_dictionary` for entity `v_ace_account` and field `days_past_due`.
12. System: returns field ID DF-ACE-018, data type NUMBER, physical type integer, source system ACE, source field `public.account.delay_days`, data product DP01, system of record "ACE (ingested from ALS)", refresh cycle DAILY and the owner of DP01.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A statement in the migration fails | The transaction rolls back; no table is left half created; the pipeline stage fails with the statement named | None (pipeline log) | AC4 |
| X2 | A table column exists with no sys_fields row, or a sys_fields row has no column or a different physical type | The conformance test fails and names the table, the column and the field ID | None (pipeline log) | AC5 |
| X3 | The migration runs again on a schema where it is already applied | Flyway skips it; no table or row changes | None | AC6 |
| X4 | A catalog row names no system of record, two systems of record, a bare source name such as "CCMS", or no owner user ID | The whole load is refused; no row is written | MSG-P1-003 | AC7, AC11 |
| X5 | The catalog file does not hold exactly the 14 products DP01 to DP14 | The whole load is refused | MSG-P1-004 | AC8 |
| X6 | A catalog row names an owner role or refresh cycle outside its list | The whole load is refused | MSG-P1-007 | AC9 |
| X7 | The same catalog file is loaded again | Nothing is written; the load is reported as already done | MSG-P1-011 | AC10 |
| X8 | A role without Reference data C loads the catalog | 403 Problem response; the refusal is in the access log | MSG-P4-002 | TC-E1-001-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the migration tooling (RWB-E1-044) and the reference load service (RWB-E1-043); every later read, the case list and the data dictionary story (RWB-E1-064) build on this one |
| Negotiable | The catalog values (names, definitions, owners, refresh cycles) are data in a load file; the story fixes the tables and the checks |
| Valuable | Gives every Workbench record one home, every data product one accountable owner and every source read one dictionary entry |
| Estimable | One migration, one view, one conformance test, one reference table handler |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: Recovery tables for the 14 data products

  Scenario: AC1 Schema deployed
    Given the migration V0001__rwb_e1_001_recovery_schema.sql and the parameter recoverySchema = "recovery"
    When the pipeline applies it in DEV and then in SIT
    Then the recovery schema in each environment holds 92 tables: the 88 Workbench tables and the four extension tables party_ext, contact_point_ext, account_ext and valuation_ext
    Then it holds none of the tables that left the schema: loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory and tracker_row
    Then no constraint in schema recovery references a table in schema public
    Then every link to an ACE record is a varchar(255) business key with no foreign key: account_key, person_key, asset_key, payment_code and contact_key
    Then the conformance test reports 1,062 of the 1,062 table fields matched by name and physical type
    Then the 30 recovery.v_ace_* views ship separately in RWB-E1-069 and add their 304 fields to the dictionary

  Scenario: AC2 Dictionary published
    Given the data dictionary and the data product seed loaded by the migration, and the catalog loaded for DP01
    When a developer queries v_data_dictionary for entity "v_ace_account" and field "days_past_due"
    Then the row holds field ID "DF-ACE-018", data type "NUMBER", physical type "integer"
    Then source system "ACE", source field "public.account.delay_days"
    Then data product "DP01", system of record "ACE (ingested from ALS)", refresh cycle "DAILY", owner role "RW-DATASTEW" and the owner user ID of DP01
    Then the row for entity "account_ext" and field "dispute_open" holds field ID "DF-EXT-028", data type "BOOLEAN", physical type "boolean", source system "Workbench" and data product "DP01"

  Scenario: AC3 One system of record
    Given a catalog load file with the 14 rows DP01 to DP14, each with one system of record and one owner user ID
    When the reference data administrator loads it with valid from 2026-11-30
    Then data_product holds 14 rows
    Then each row has a definition, exactly one system of record and one owner user ID
    Then DP01 names system of record "ACE (ingested from ALS)" and refresh cycle "DAILY"
    Then DP03 names system of record "Recovery Workbench" and refresh cycle "ON_CHANGE"
    Then DP06 names system of record "ACE (ingested from CCMS, SVAF, AMIS and RPS)", refresh cycle "WEEKLY" and expected by "MON 08:00"

  Scenario: AC4 Failed migration leaves no partial schema
    Given a copy of the migration in which the statement creating table valuation_ext fails
    When the pipeline applies it in DEV
    Then the pipeline stage fails and names the failing statement
    Then the recovery schema holds none of the tables of that migration
    Then the Flyway history has no successful row for version 1.001

  Scenario: AC5 Column without a dictionary entry fails the build
    Given a branch that adds the column account_ext.branch_code with no sys_fields row
    When the conformance test runs in the pipeline
    Then the test fails with "account_ext.branch_code has no data dictionary entry"
    Then a sys_fields row DF-EXT-028 whose column is changed to type text fails the test with "DF-EXT-028 physical type boolean expected, text found"

  Scenario: AC6 Repeated migration has no effect
    Given the migration version 1.001 already applied in SIT
    When the pipeline runs again in SIT
    Then Flyway reports version 1.001 as already applied
    Then the row counts of sys_objects (122) and sys_fields (1,366) are unchanged

  Scenario: AC7 Catalog row with two systems of record is refused
    Given a catalog load file in which DP06 names system of record "ACE (ingested from CCMS); SVAF"
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
    Given the catalog version loaded on 2026-11-30 is in force
    When the reference data administrator loads the same file again
    Then the system writes nothing
    Then the response carries MSG-P1-011 "The data product catalog load for 2026-11-30 is already complete or running. It was not run again."

  Scenario: AC11 Source named on its own is refused
    Given a catalog load file in which DP06 names system of record "CCMS"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-003 "DP06 must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner."
    Then no row is written and the version in force stays in use
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every table column and every view column in the recovery schema has exactly one row in the data dictionary, with its BR Field ID, types, source system and meaning | Logical Data Model and Data Dictionary; sys_fields |
| BR2 | Workbench data is held in the 14 data products DP01 to DP14 | REQ-RDF-001; sys_objects.data_product |
| BR3 | Each data product has exactly one system of record, written "ACE (ingested from X)" for source data, "Recovery Workbench" for Workbench records, or, where the product holds both, one sentence that names ACE with its sources and the Recovery Workbench; and one named owner | REQ-RDF-001; D-RCV-35 U1 |
| BR4 | The catalog values are a versioned data load, changed without a code release; a load with an exception is refused in full | Principle 1; DT02; CTL-08 |
| BR5 | Where a product is fed by several sources (DP06, DP07, DP13), its one system of record names ACE and every source it ingests; a bare source name is refused because no source reaches the Workbench except through ACE | D-RCV-35; ADR-010 |
| BR6 | Schema names come from parameters; one migration per story; forward only in PROD | RWB-E1-044 |
| BR7 | Personal fields carry is_personal = true in the dictionary so masking (RWB-E1-016) can read them | sys_fields.is_personal; CTL-11 |
| BR8 | The recovery schema holds no copy of source data. No constraint references a table in schema public, and a link to an ACE record is a varchar(255) business key with no foreign key | D-RCV-35 U4; ADR-010; Data Tier Map section 1 |
| BR9 | V0001 seeds the dictionary for the tables and the 30 views before the views exist; the view columns are matched from V0002 onward by the view conformance test of RWB-E1-069 | D-RCV-29 amended; RWB-E1-069 |

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
| DF-REF-070 to DF-REF-079 | data_product | all 10 fields | Create and write 14 rows; read |
| DF-REF-087 to DF-REF-093 | sys_objects | all 7 fields | Create and write 122 rows; read |
| DF-REF-094 to DF-REF-110 | sys_fields | all 17 fields | Create and write 1,366 rows; read |
| DF-EXT-001 to DF-EXT-049 | party_ext, contact_point_ext, account_ext, valuation_ext | all 49 fields | Create (four tables) |
| DF-CAS, DF-WRK, DF-TRT, DF-LEG, DF-PRT, DF-SAL, DF-INT, DF-DOC, DF-DEC, DF-FIN, DF-REF, DF-OPS, DF-RPT and DF-AGT prefixes | the 85 other Workbench tables | 979 fields | Create (tables only; no rows) |

Field IDs are those in the Logical Data Model and Data Dictionary and in Physical Schema v5. The 92 tables hold 1,062 fields: 1,013 on the 88 Workbench tables, including the 34 of data_product, sys_objects and sys_fields, and 49 on the four extension tables. The 30 views add 304 fields, so the dictionary holds 122 objects and 1,366 fields.

Ruled 2026-11-06 as D-RCV-29 and amended by D-RCV-35: the baseline migration seeds the full recovery dictionary, 122 `sys_objects` rows and 1,366 `sys_fields` rows, as held in Recovery Workbench Physical Schema v5.sql, so the dictionary is complete before the views exist and the conformance test can run. The 108 objects and 1,256 fields of the v4 copy schema are superseded. `delegation_limit` holds no baseline rows; its content is loaded as version DOA-2026.11 through RWB-E1-043 by RWB-E1-038 (D-RCV-34). Later dictionary changes are reference loads through RWB-E1-043 (D-RCV-28).

## 12. Contract

**Dictionary view** `v_data_dictionary` (read model created by the migration; RWB-E1-064 builds the dictionary endpoint on it)

| Column | From |
|---|---|
| entity, data_product, entity_system_of_record | sys_objects |
| field, field_id, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, late_behavior, interface_id, description | sys_fields |
| product_system_of_record, refresh_cycle, owner_role, owner_user_id | data_product |

The view joins sys_fields to sys_objects on object_name and left joins data_product on product_code where the product is active, and returns active rows only. It reads no ACE table.

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
| Name | `V0001__rwb_e1_001_recovery_schema.sql` with placeholder `${recoverySchema}` |
| Includes | The 92 tables, their indexes and triggers, data_product, the dictionary seed and v_data_dictionary. No `v_ace_*` view: those are V0002 and V0003 in RWB-E1-069 |
| Idempotency | The Flyway version 1.001; a changed checksum on an applied version fails the pipeline |
| Restart | A failed run rolls back; the next run applies the full version again |

## 13. Solution plan

**Package.** Folder `recovery/dataengine/catalog`, Java package `recovery.dataengine.catalog`; migration in `src/main/resources/db/migration/recovery`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| V0001__rwb_e1_001_recovery_schema.sql | Flyway migration | Creates the 92 tables of the physical schema, data_product, the references, indexes, triggers and v_data_dictionary; inserts sys_objects, sys_fields and the 14 data_product seed rows |
| DataDictionaryConformanceTest | Test (pipeline) | Compares information_schema.columns with sys_fields in both directions for the 92 tables, ignoring the 7 standard columns |
| DataProduct | Entity | Maps data_product |
| DataProductRepository | Repository | Reads and writes data_product |
| DataProductCatalogHandler | Published interface implementation | Implements ReferenceTableHandler for table code `data_product` |

**Database.** Creates the 92 tables of Physical Schema v5 and nothing else: no loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory or tracker_row. Creates data_product with product_code varchar(25) primary key, product_name varchar(80) not null, definition varchar(400) not null, system_of_record varchar(120) not null, owner_role varchar(20) not null, owner_user_id uuid, refresh_cycle varchar(10) not null with values DAILY, WEEKLY, MONTHLY and ON_CHANGE, expected_by varchar(20), valid_from date not null and the 7 standard columns. Creates v_data_dictionary. Adds fk_sys_objects_data_product; sys_objects.data_product is nullable, so the 98 product objects name DP01 to DP14 and the 24 operational objects of OPS (13), AGT (8) and RPT (3) leave it empty. The 24 placeholder rows of delegation_limit are not seeded. The migration inserts the data_product rows before the sys_objects rows.

**Configuration and reference data.** Parameter `recoverySchema` per environment (platform administrator). Seed values inserted by the migration and repeated in the first catalog load file, with the owner user IDs, prepared by the reference data administrator and confirmed by the data steward:

| Code | Name | Definition | System of record | Refresh cycle | Expected by | Valid from |
|---|---|---|---|---|---|---|
| DP01 | Account and arrears | Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments | ACE (ingested from ALS) | DAILY | 08:00 | 2026-11-30 |
| DP02 | Customer and party | Customers, guarantors, co-borrowers and heirs, identity masked to the last four, contact points, consent and flags for vulnerability, death and bankruptcy | ACE (ingested from SCBPDM and the core bank) | DAILY | 08:00 | 2026-11-30 |
| DP03 | Case and ownership | The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations | Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP04 | Treatment and offers | Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome | ACE (ingested from the core bank) for the plan, with the treatment held in the Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP05 | Contact and promises | Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS | ACE (ingested from EFS) | DAILY | 08:00 | 2026-11-30 |
| DP06 | Collateral and assets | Collateral, appraisals, assets held after repossession or transfer, listings and sale results | ACE (ingested from CCMS, SVAF, AMIS and RPS) | WEEKLY | MON 08:00 | 2026-11-30 |
| DP07 | Legal events and cases | Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement | ACE (ingested from LIT and WIN) for the court record and the proof of delivery, with notices and enforcement held in the Recovery Workbench | DAILY | 08:00 | 2026-11-30 |
| DP08 | Partner performance | Partners on the panel, work placed with each, results, fees and scorecards | Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP09 | Debt sale | Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs | Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP10 | Documents and extracted fields | Documents against the case, the fields read from them, retention class and custody of originals | Recovery Workbench document hub | ON_CHANGE | As it changes | 2026-11-30 |
| DP11 | Scores and route economics | Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions | ACE (ingested from COLLINS) | DAILY | 08:00 | 2026-11-30 |
| DP12 | Decision log | One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome | Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP13 | Money and closure | Payments and proceeds matched to the case, write-off postings and recovery after charge-off | ACE (ingested from ALS and GL) | DAILY | 08:00 | 2026-11-30 |
| DP14 | Reference data | Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned | Recovery Workbench, with the ACE lists read through the views | ON_CHANGE | As it changes | 2026-11-30 |

Owner role RW-DATASTEW for every product; owner user IDs per environment.

**Build steps**

Ruled 2026-11-05 as D-RCV-28: recovery Flyway files are named `V<seq>__<story>_<name>.sql` with a four-digit sequence taken in merge order; line 1 is `-- Story: <story key>`; the schema is referenced only as `${recoverySchema}` and is `recovery` in every environment. The RWB-E1-001 baseline is `V0001__rwb_e1_001_recovery_schema.sql`; RWB-E1-044 ships no production migration file.

1. Write `V0001__rwb_e1_001_recovery_schema.sql` from Physical Schema v5, with `${recoverySchema}` in place of the fixed schema name, plus data_product with its 14 seed rows and v_data_dictionary; run it on an empty PostgreSQL container.
2. Write DataDictionaryConformanceTest and add it to the pipeline after the migration stage; prove it fails on an extra column and on a changed type.
3. Write DataProduct, DataProductRepository and DataProductCatalogHandler with the checks for BR2, BR3 and the list values; unit test the checks for X4, X5 and X6, including a bare source name.
4. Connect the handler to the reference data service of RWB-E1-043 and test a full load, a refused load and a repeated file against a container database.
5. Write a test that reads v_data_dictionary for v_ace_account.days_past_due and account_ext.dispute_open after a catalog load.
6. Add messages MSG-P1-003, MSG-P1-004, MSG-P1-007 and MSG-P1-011 to the message table with English and Thai text.
7. Leave V0002 and V0003 to RWB-E1-069; confirm that V0001 creates no `v_ace_*` view.

**Feature flag.** `rwb.p1.data-catalog`. The flag covers the catalog handler; the migration is not behind a flag.

**Done when.** The tests in section 16 pass, the migration runs clean in DEV and SIT, and the catalog version for SIT holds 14 rows.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-003 | Catalog row with no system of record, more than one, a bare source name, or no owner | {product} must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner. |
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
| TC-E1-001-01 | AC1, BR1, BR6, BR8 | System | Empty DEV and SIT schemas; schema parameter "recovery"; a branch that adds a foreign key to public.account |
| TC-E1-001-02 | AC2, BR1 | System | Dictionary from the migration; catalog with a synthetic owner for DP01 |
| TC-E1-001-03 | AC3, BR2, BR3, BR5 | System | Catalog file of 14 rows from the seed table |
| TC-E1-001-04 | AC4 | System | Migration copy with a failing CREATE TABLE valuation_ext |
| TC-E1-001-05 | AC5, BR1 | System | Branch with account_ext.branch_code; changed type on DF-EXT-028 |
| TC-E1-001-06 | AC6 | System | SIT schema at version 1.001 |
| TC-E1-001-07 | AC7, BR3, BR4 | System | Catalog file with DP06 naming two systems and DP11 with no owner |
| TC-E1-001-08 | AC8, BR2, BR4 | System | Catalog file of 13 rows without DP09 |
| TC-E1-001-09 | AC9, BR4 | System | Catalog file with owner role DP_OWNER and refresh cycle HOURLY |
| TC-E1-001-10 | AC10, BR4 | System | Same catalog file loaded twice |
| TC-E1-001-11 | Access | Access | RW-DATASTEW calls POST /admin/reference-loads with table data_product; refused with MSG-P4-002 |
| TC-E1-001-12 | AC11, BR3, BR5 | System | Catalog file with DP06 naming "CCMS" |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: product names, definitions, systems of record, owners and refresh cycles come from the catalog load.
- No personal data in logs, tests or prompts. Owner user IDs in DEV and SIT are synthetic test users.
- ACE data only through `recovery.v_ace_*` views. This story creates no view over a public table and reads no public table.
- The migration changes no data outside the recovery schema, creates no constraint into schema public and never drops a table in PROD.
- The dictionary reads only sys_objects, sys_fields and data_product in the recovery schema.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record, one read path and one owner | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-01, FEAT-RDF-02 | All recovery processes | CTL-08; Principle 1; D-RCV-35 U1, U4 | TC-E1-001-01 to TC-E1-001-12 |

## 19. Out of scope

- The 30 read-only ACE views, their grants and the view conformance test (RWB-E1-069).
- Freshness stamp per data product from the ACE batch record (RWB-E1-015).
- Access control per data product, PDPA masking and the catalog entry screen (RWB-E1-016).
- Retention and archive rules (RWB-E1-017).
- Stage 2 data products for contracts, plans and treatments (REQ-RDF-014, Epic 2).
- The dictionary endpoint, field versions and data contracts with each system owner (RWB-E1-064).
