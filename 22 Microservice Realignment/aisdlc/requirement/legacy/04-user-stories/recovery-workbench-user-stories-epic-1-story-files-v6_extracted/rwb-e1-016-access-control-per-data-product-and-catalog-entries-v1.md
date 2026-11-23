<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 016 Access control per data product and catalog entries v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 016 Access control per data product and catalog entries v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-016 Access control per data product and catalog entries

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-016 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-15 Set access control per data product for PDPA; FEAT-RDF-16 Maintain the data catalog entry per data product |
| Requirement IDs | REQ-RDF-010, REQ-RDF-011 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-010, REQ-RDF-011) |
| L3 process | All recovery processes |
| Decision | D-RCV-35 (U4); ADR-010 |
| Priority | Must |
| Depends on | RWB-E1-037, RWB-E1-001, RWB-E1-064, RWB-E1-069 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **read access to each data product granted by role, source data reached only through the ACE view grant, personal fields masked by role from `v_ace_customer` and `v_ace_contact`, every read logged, and a catalog entry per product that names its owner, system of record, freshness, views and tables and fields**, so that **personal data is read only by the roles that need it and every product is findable**.

## 2. Business rationale

Audit findings record staff sending debtor data outside the bank and users holding access they did not need (CTL-11, CTL-09). Under D-RCV-35 there is no load and no tokenization: source data is reached only through the `recovery.v_ace_*` views, so access to a data product is the role's access row plus the database grant on the view, and the identity number is masked inside `v_ace_customer` itself. Access rows held as data limit each role to the products its work needs; masking rules decide which role sees a personal field in clear; and every read of personal data goes to the PII access log. The catalog gives one entry per product so a developer, an analyst or an auditor finds the owner, the source, the freshness rule, the retention, the views behind it and the personal fields without asking. Serves REQ-RDF-010 and REQ-RDF-011.

## 3. Preconditions

- RWB-E1-001 is done: the 92 tables and the 122 sys_objects and 1,366 sys_fields rows exist, with the four extension tables.
- RWB-E1-069 is done: the 30 `recovery.v_ace_*` views exist and the grants are applied. `ace_view_owner` owns the views and holds SELECT on the ACE tables; recovery_svc holds SELECT on `recovery.v_ace_*` and no privilege on `public`.
- RWB-E1-037 is done: P4 holds the role to permission matrix and the masking rules, and publishes `FieldMasker` in section 12.
- RWB-E1-064 is done: data_product holds DP01 to DP14 with owner role, system of record and refresh cycle.
- data_product_access version "DPA-2026.11" is loaded and approved: for example RW-CASEOWN and RW-AUDIT read DP02; RW-PHONECOL reads DP01, DP02, DP03 and DP05 and not DP06.
- The masking rules from Compliance may be empty (DL26). Until they load, every personal field is masked for every role.
- The ACE common module PII access logging is available (INT-22).

## 4. Flow

1. User: opens a data product view, which calls GET /data-products/{productCode}/records?caseId=.
2. DataProductAccessService: checks the capability right Case record R through the ACE access check.
3. DataProductAccessService: checks data_product_access for a row in force for one of the user's roles and the product.
4. DataProductAccessService: calls the P3 case scope interface for the case's account keys and person keys in the user's scope.
5. DataProductRecordService: reads the product rows. A Workbench table is read in the recovery schema; a source product is read from its `recovery.v_ace_*` view by `account_key`, `person_key`, `asset_key`, `payment_code` or `contact_key`. The read runs as recovery_svc, which has SELECT on the view and nothing on `public`.
6. DataProductRecordService: for each field tagged is_personal in sys_fields, applies `FieldMasker` for the user's roles. The identity number is already masked in the view; the phone, email and address are full in the view because notices and calls need them.
7. DataProductAccessService: writes the read to the PII access log with user, product, case, field names and time; no value is logged.
8. Controller: returns the rows with the product's freshness stamp.
9. User with Platform administration R: calls GET /admin/data-products?product=DP01 and reads the catalog entry with owner, system of record, refresh cycle, retention, the views and tables behind it, the reconciliations and the fields with PDPA tags.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No data_product_access row for the user's roles and the product | 403; no row read; refusal written to the access log | MSG-P4-002 | AC3 |
| X2 | An access load names a role code not in the roles table, an unknown product, or two overlapping rows | Load refused in full; previous version stays in force | MSG-P1-002 | AC4 |
| X3 | The case is outside the user's scope | 404; no row read; refusal logged | MSG-P4-003 | AC5 |
| X4 | No masking rule is loaded for a personal field | The field is masked for every role | None | AC6 |
| X5 | The PII access log cannot be written | Read refused with 503; no personal data returned | MSG-GEN-006 | AC7 |
| X6 | An access row has a valid-from date after today | The row is not in force; the read is refused until that date | MSG-P4-002 | AC8 |
| X7 | A statement reads a `public.*` table as recovery_svc, or writes a view | The database refuses it; the grant test fails the pipeline if the privilege exists | None (pipeline log) | AC9 |
| X8 | A catalog load marks a `v_ace_*` view as system of record "Workbench" | The load is refused whole; the version in force stays | MSG-P1-003 | AC11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the tables and the metadata tables (RWB-E1-001), the views and grants (RWB-E1-069), the P4 masking (RWB-E1-037) and the data product table (RWB-E1-064) |
| Negotiable | Which role reads which product, and which field is masked for whom, are data rows; the story fixes the checks |
| Valuable | Personal data reaches only the roles that need it, source access is enforced by the grant, and every read is logged |
| Estimable | Two endpoints, one read service, one catalog service, calls to three published interfaces |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion is one API or database test with synthetic parties and roles |

## 7. Acceptance criteria

```gherkin
Feature: Access control per data product and catalog entries

  Background:
    Given data product access version "DPA-2026.11" is in force from 2026-11-20
    Given case "RW-2026-000102" has borrower person_key "P0000102" whose ACE customer has identity number "1234567890123" and mobile "0812345678"
    Given no masking rule from Compliance is loaded for the v_ace_customer or v_ace_contact fields

  Scenario: AC1 Role access
    Given user "u-audit-01" holds read-only role RW-AUDIT, which reads DP02
    When the user calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then the mobile number shows as "******5678" and the identity number as "*********0123"
    Then no response field holds the clear identity number
    Then the PII access log holds one entry with user "u-audit-01", product "DP02", case "RW-2026-000102" and the time of the read

  Scenario: AC2 Catalog entry
    Given the 14 data products DP01 to DP14
    When a data steward calls GET /admin/data-products?product=DP01
    Then the system returns the DP01 entry with owner role, system of record "ACE (ingested from ALS)", refresh cycle "DAILY", expected-by "08:00" and a retention class
    Then the entry lists the views v_ace_account, v_ace_payment, v_ace_aa_relation, v_ace_bucket_log, v_ace_product and v_ace_branch with system of record "ACE", and account_ext with system of record "Workbench"
    Then the field days_past_due shows field ID "DF-ACE-018", source system "ACE" and source field "public.account.delay_days"
    Then the entry lists REC-01 and REC-02 and the data_product_access rows for DP01
    Then the field list carries the PDPA tag for each field, taken from sys_fields.is_personal

  Scenario: AC3 Access denied
    Given user "u-phone-01" holds RW-PHONECOL, which has no access row for DP06
    When the user calls GET /data-products/DP06/records?caseId=RW-2026-000102
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system writes the refusal to the access log with user "u-phone-01" and product "DP06"

  Scenario: AC4 An access load with an unknown role is refused
    Given an access load version "DPA-2026.12" with a row for role "RW-UNKNOWN" and product "DP02"
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and check "unknown role RW-UNKNOWN"
    Then version "DPA-2026.11" stays in force

  Scenario: AC5 A case outside the user's scope
    Given user "u-owner-07" holds RW-CASEOWN with scope Own and does not own case "RW-2026-000102"
    When the user calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then the system refuses the call with status 404 and MSG-P4-003
    Then the system reads no row

  Scenario: AC6 No masking rule loaded keeps every personal field masked
    Given user "u-comply-01" holds RW-COMPLY, which reads DP02
    When the user calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then first_name, last_name, cif_no, date_of_birth and the contact value are returned masked

  Scenario: AC7 The PII access log is unavailable
    Given the PII access log rejects every write
    When user "u-audit-01" calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then the system refuses the call with status 503 and MSG-GEN-006 for system "PII access log"
    Then the system returns no personal field

  Scenario: AC8 An access row not yet in force
    Given access version "DPA-2026.12" gives RW-PHONECOL read on DP06 from 2026-12-15
    Given today is 2026-12-14
    When user "u-phone-01" calls GET /data-products/DP06/records?caseId=RW-2026-000102
    Then the system refuses the call with status 403 and MSG-P4-002

  Scenario: AC9 The view grant is the source data access
    Given the recovery service identity recovery_svc in SIT
    When the grant test runs
    Then SELECT on public.customer is refused with permission denied
    Then SELECT on recovery.v_ace_customer returns rows
    Then INSERT on recovery.v_ace_customer is refused with permission denied
    Then the test passes for every one of the 30 views

  Scenario: AC10 Thirty view rows in the catalog
    Given V0001, V0002 and V0003 are applied
    When a data steward calls GET /admin/data-products
    Then the system returns 14 entries
    Then every one of the 30 v_ace_* views has one catalog row under its data product with system of record "ACE"
    Then v_data_dictionary returns 1,366 fields over 122 objects, of which 304 are view fields with source system "ACE"
    Then no view row names system of record "Workbench"

  Scenario: AC11 A view marked as Workbench is refused
    Given a catalog load that sets system of record "Workbench" on v_ace_customer
    When the reference data administrator loads it
    Then the load is refused whole with MSG-P1-003 for v_ace_customer
    Then the version in force stays in use
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A role reads a data product only through a data_product_access row in force for that role and product | REQ-RDF-010; FEAT-RDF-15 |
| BR2 | A personal field is masked unless the masking rules let the role see it | CTL-11; masking_rule; DL26 |
| BR3 | With no masking rule loaded, every personal field stays masked | DL26 ("Masking rules load with no values") |
| BR4 | Every read of personal data is written to the PII access log; a read that cannot be logged is refused | REQ-ACA-006; CTL-11 |
| BR5 | A record outside the caller's scope is refused | CTL-09; permission matrix |
| BR6 | An access load with an exception is refused in full; the previous version stays in force | Reference data change process, step 3; CTL-08 |
| BR7 | Each data product has one catalog entry with owner, system of record, refresh cycle, retention, the views and tables behind it, the reconciliations and fields with PDPA tags | REQ-RDF-011; sys_fields.is_personal |
| BR8 | Source data access is the view grant: recovery_svc holds SELECT on `recovery.v_ace_*` and no privilege on `public`, and may not write any view. A direct public table read fails at the database, not in code review | D-RCV-35 U4; ADR-010; Data Tier Map section 1 |
| BR9 | There is no tokenization. `v_ace_customer` returns the identity number as id_no_masked and id_no_last4 only; `v_ace_contact` returns the full phone, email and address because notices and calls need them, and the API masks them by role | ADR-010; Data Tier Map section 7; DL26 |
| BR10 | Every one of the 30 `v_ace_*` views belongs to its data product with system of record "ACE"; a view marked "Workbench" is refused | BR-P1-002-2; FSD P1 A2.16 |

## 9. State transitions

None. This story does not change a case status. It changes the version in force of data_product_access when an approved load reaches its valid-from date.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Prepares the access rows for their products; reads the catalog (Platform administration R) |
| RW-REFADM, reference data administrator | Submits the access load through POST /admin/reference-loads (Reference data C) |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules (DL26); reads the catalog |
| RW-SECADM, security administrator | Owns the role to permission matrix; reads the access log |
| RW-COE, RW-AUDIT, RW-PLATADM | Read the catalog (Platform administration R) |
| Roles with Case record R and an access row, for example RW-CASEOWN, RW-AUDIT | Read a data product for a case in scope |
| recovery_svc, recovery service identity | Applies an approved access version to data_product_access; reads the views with SELECT only |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-055 | v_ace_customer | cif_no | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-057 | v_ace_customer | first_name | Read |
| DF-ACE-058 | v_ace_customer | last_name | Read |
| DF-ACE-059 | v_ace_customer | date_of_birth | Read |
| DF-ACE-061 | v_ace_customer | deceased_flag | Read |
| DF-ACE-073 | v_ace_customer | id_no_masked | Read |
| DF-ACE-074 | v_ace_customer | id_no_last4 | Read |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-076 | v_ace_contact | contact_key | Read |
| DF-ACE-077 | v_ace_contact | person_key | Read |
| DF-ACE-078 | v_ace_contact | contact_value | Read |
| DF-ACE-079 | v_ace_contact | contact_value_masked | Read |
| DF-ACE-080 | v_ace_contact | usage_code | Read |
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-EXT-001 | party_ext | person_key | Read |
| DF-EXT-002 | party_ext | vulnerable | Read |
| DF-EXT-003 | party_ext | deceased_override | Read |
| DF-EXT-004 | party_ext | bankruptcy | Read |
| DF-EXT-005 | party_ext | fraud_flag | Read |
| DF-EXT-013 | contact_point_ext | contact_key | Read |
| DF-EXT-014 | contact_point_ext | contact_type | Read |
| DF-EXT-015 | contact_point_ext | consent_given | Read |
| DF-EXT-018 | contact_point_ext | failed_count | Read |
| DF-EXT-027 | account_ext | account_key | Read |
| DF-EXT-028 | account_ext | dispute_open | Read |
| DF-EXT-036 | valuation_ext | valuation_key | Read |
| DF-EXT-037 | valuation_ext | accepted | Read |
| DF-EXT-041 | valuation_ext | stale_flag | Read |
| DF-REF-088 | sys_objects | object_name | Read |
| DF-REF-091 | sys_objects | data_product | Read |
| DF-REF-092 | sys_objects | system_of_record | Read |
| DF-REF-097 | sys_fields | field_name | Read |
| DF-REF-103 | sys_fields | source_system | Read |
| DF-REF-105 | sys_fields | is_personal | Read |
| DF-REF-071 | data_product | product_code | Read |
| DF-REF-074 | data_product | system_of_record | Read |
| DF-REF-075 | data_product | owner_role | Read |
| DF-REF-077 | data_product | refresh_cycle | Read |
| DF-REF-119 | retention_rule | record_class | Read |
| DF-REF-080 | data_product_access | id | Write |
| DF-REF-081 | data_product_access | product_code | Write |
| DF-REF-082 | data_product_access | role_code | Write |
| DF-REF-083 | data_product_access | can_read | Write |
| DF-REF-084 | data_product_access | access_version | Write |
| DF-REF-085 | data_product_access | valid_from | Write |
| DF-REF-086 | data_product_access | valid_to | Write |
| DF-REF-199 | masking_rule | role_code | Read |
| DF-REF-200 | masking_rule | field_id | Read |
| DF-REF-201 | masking_rule | unmasked | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. The personal tags on the view fields are read from sys_fields.is_personal.

## 12. Contract

**Endpoints**

| Item | GET /data-products/{productCode}/records | GET /admin/data-products |
|---|---|---|
| Request | Path: productCode (DP01 to DP14); query: caseId (required), page, size | Query: product (optional) |
| Response | DataProductRecordPage: items (record id, entity, fields map with masked values), freshness (FreshnessStamp from RWB-E1-015), page, size, total | DataProductCatalogEntry[]: productCode, productName, definition, ownerRole, systemOfRecord, refreshCycle, expectedBy, retentionClass, fields (entity, fieldName, fieldId, dataType, isPersonal), reconciliations (rec_code), access (roleCode, canRead, accessVersion, validFrom) |
| Errors | 400 missing caseId (MSG-GEN-001); 401 (MSG-P4-001); 403 no capability right or no access row (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 503 PII log or store down (MSG-GEN-006) | 401; 403; 503 |
| Authorization | Case record, R; plus a data_product_access row in force | Platform administration, R |
| Idempotency | Not applicable | Not applicable |

**Endpoint used for the access load**

POST /admin/reference-loads with table `data_product_access`, file and validFrom (Reference data, C); approval through POST /admin/reference-loads/{loadId}/approve (Reference data, A). Errors 409 version clash (MSG-GEN-004), 422 field invalid (MSG-GEN-001). The P4 reference data service hands approved rows to P1 through DataProductAccessLoader.

**Published interfaces**

```java
// P1, called by the reference data service after approval
package recovery.dataengine.access.api;
public interface DataProductAccessLoader {
    LoadResult apply(String accessVersion, LocalDate validFrom, List<DataProductAccessRow> rows);
}

// P3, called by P1 to resolve a case to its ACE keys within the caller's scope
package recovery.casewf.api;
public interface CaseScopeQuery {
    CaseLinks linksInScope(UUID caseId, UserContext user) throws CaseNotInScopeException;
}
public record CaseLinks(UUID caseId, List<String> accountKeys, List<String> personKeys) {}

// P4, from RWB-E1-037
package recovery.access.matrix;
public interface FieldMasker {
    <T> T mask(T dto, SessionContext session);       // masks every field annotated @PersonalData("DF-...")
    boolean isUnmasked(String fieldId, SessionContext session);
}
```

PII access logging goes through the ACE common module logging interface to PII Kafka with user, product, case, field names and time; no field value is logged. There is no token and no detokenization call anywhere in this path.

## 13. Solution plan

- Package: folder `recovery/dataengine/access`, Java package `recovery.dataengine.access`.

| Component | Type | Responsibility |
|---|---|---|
| DataProductController | Controller | GET /data-products/{productCode}/records and GET /admin/data-products |
| DataProductAccessService | Service | Capability check, access row check, scope call, PII log write |
| DataProductRecordService | Service | Reads rows of the product's entities or views and applies masking by sys_fields.is_personal |
| DataProductCatalogService | Service | Builds catalog entries from data_product, sys_objects, sys_fields, data_product_access and retention_rule |
| DataProductAccessRepository | Repository | Reads and writes data_product_access |
| DataProductAccess | Entity | One row per product, role and version |
| DataProductAccessLoader | Published interface | Applies an approved access version |
| Data product access rule table | Rule table | data_product_access rows by version and valid-from date |

- Database: data_product_access is created by V0001 (RWB-E1-001) with id uuid, product_code varchar(25), role_code varchar(20), can_read boolean, access_version varchar(20), valid_from date, valid_to date and the standard columns; unique (product_code, role_code, access_version). masking_rule is created by V0001 and its content is owned by RWB-E1-037 (DL26). This story creates no table. It reads sys_objects, sys_fields, data_product, data_product_access, retention_rule, the four extension tables and the `v_ace_*` views. No read of role or permission tables through SQL: the capability check uses the ACE access check, and role codes come from the session.
- Configuration and reference data: access version "DPA-2026.11" prepared by the data steward and loaded by the reference data administrator; masking rules loaded by Compliance under RWB-E1-037 (DL26).
- Build steps:
  1. Write DataProductAccessLoader with whole-load validation: known product code, known role code, no overlapping rows; refuse with MSG-P1-002.
  2. Write DataProductAccessService with the order: capability right, access row in force, scope through CaseScopeQuery.
  3. Write DataProductRecordService: a Workbench product reads its tables; a source product reads its views by business key; masking from sys_fields.is_personal through FieldMasker; mask every personal field when no rule exists.
  4. Write the PII access log before the response is returned; refuse with 503 when it fails.
  5. Write DataProductCatalogService and GET /admin/data-products, including the views behind each product and the access rows.
  6. Add the grant test: recovery_svc reads every view, cannot read `public.customer`, and cannot write any view.
  7. Contract tests for both new endpoints from the additions schema (RWB-TE-003).
  8. Tests for AC1 to AC10 and the access test.
- Feature flag: `rwb.dataengine.product-access`.
- Done when: the tests in section 16 pass and the catalog returns 14 complete entries in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | No capability right or no access row for the product | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P1-002 | Access load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-003 | A catalog load marks a view with a system of record other than ACE | {product} must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner. |
| MSG-GEN-001 | caseId missing | Enter {field}. |
| MSG-GEN-006 | PII access log unavailable | {system} is not available. Your request is queued and will be retried. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. In Epic 1 the case record view SCR-03 (Read only) shows the product data the role may read, with personal fields masked. Catalog entries are read through GET /admin/data-products; SCR-47 Personal data shows masking rules from Epic 8.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-016-01 | AC1, BR1, BR2, BR4, BR9 | System | RW-AUDIT; case RW-2026-000102; synthetic customer P0000102 with identity 1234567890123 and mobile 0812345678 |
| TC-E1-016-02 | AC2, BR7 | System | DP01 entry; six views and account_ext; DF-ACE-018; access rows |
| TC-E1-016-03 | AC3, BR1 | System | RW-PHONECOL; product DP06 |
| TC-E1-016-04 | AC4, BR6 | System | Access load with role RW-UNKNOWN |
| TC-E1-016-05 | AC5, BR5 | System | RW-CASEOWN, case not owned |
| TC-E1-016-06 | AC6, BR3 | System | RW-COMPLY; no masking rules loaded |
| TC-E1-016-07 | AC7, BR4 | System | PII access log stub rejecting writes |
| TC-E1-016-08 | AC8, BR1 | System | Access row valid from 2026-12-15; test clock 2026-12-14 |
| TC-E1-016-09 | Access | Access | RW-TRIBE calls GET /admin/data-products; refused with MSG-P4-002 |
| TC-E1-016-10 | AC9, BR8 | Database | recovery_svc; SELECT public.customer; SELECT and INSERT on v_ace_customer; all 30 views |
| TC-E1-016-11 | AC10, BR7, BR10 | System | 30 views; 122 objects and 1,366 fields |
| TC-E1-016-12 | AC11, BR10 | System | Catalog load setting v_ace_customer to Workbench |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: access by role and masking by role are data rows; the code holds no role or product list.
- No personal data in logs, tests or prompts: the PII access log carries field names, not values; test customers are synthetic.
- No read of another module's tables: case scope comes from CaseScopeQuery, masking from FieldMasker, roles from the session.
- ACE data only through `recovery.v_ace_*` views; a direct `public.*` read is a defect and fails at the database.
- A read that cannot be logged returns no personal data.
- No token, detokenization call or clear identity number exists in any response.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role through the views; personal data masked by role under PDPA | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | All recovery processes | CTL-09, CTL-11; DL26; BR-P1-001-4, BR-P1-001-6 | TC-E1-016-01, TC-E1-016-03 to TC-E1-016-10 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record, refresh and retention | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-16 | All recovery processes | CTL-08; BR-P1-002-2 | TC-E1-016-02, TC-E1-016-11, TC-E1-016-12 |

## 19. Out of scope

- The role to permission matrix and the masking rule mechanism (RWB-E1-037).
- The access log search and break-glass (RWB-E1-039).
- Masking rule values per role and field (DL26, Compliance).
- The personal data screen SCR-47 (Epic 8).
- Data product definitions and the field dictionary (RWB-E1-064).
- The view definitions, their ownership and the grants (RWB-E1-069).
