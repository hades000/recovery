<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 016 Access control per data product and catalog entries v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 016 Access control per data product and catalog entries v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-016 Access control per data product and catalog entries

SCB Collections and Recovery. Henka Group, 28 October 2026.

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
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-037, RWB-E1-001, RWB-E1-064 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **read access to each data product granted by role, PDPA fields tagged, every read logged, and a catalog entry per product with owner, system of record, freshness and fields**, so that **personal data is read only by the roles that need it and every product is findable**.

## 2. Business rationale

Audit findings record staff sending debtor data outside the bank and users holding access they did not need (CTL-11, CTL-09). Access per data product, held as data rows, limits each role to the products its work needs; PDPA tags on each field drive masking; and every read goes to the PII access log. The catalog gives one entry per product so a developer, an analyst or an auditor finds the owner, the source, the freshness rule, the retention and the personal fields without asking. Serves REQ-RDF-010 and REQ-RDF-011.

## 3. Preconditions

- RWB-E1-001 is done: the 14 data products have tables, and sys_objects and sys_fields hold the 108 entities and 1,256 fields with is_personal set.
- RWB-E1-037 is done: P4 holds the role to permission matrix and the masking rules, and publishes the masking interface in section 12.
- RWB-E1-064 is done: data_product holds DP01 to DP14 with owner role, system of record and refresh cycle.
- data_product_access version "DPA-2026.11" is loaded and approved: for example RW-CASEOWN and RW-AUDIT read DP02; RW-PHONECOL reads DP01, DP02, DP03 and DP05 and not DP06.
- The masking rules from Compliance may be empty (DL26). Until they load, every personal field is masked for every role.
- The ACE common module PII access logging is available.

## 4. Flow

1. User: opens a data product view, which calls GET /data-products/{productCode}/records?caseId=.
2. DataProductAccessService: checks the capability right Case record R through the ACE access check.
3. DataProductAccessService: checks data_product_access for a row in force for one of the user's roles and the product.
4. DataProductAccessService: calls the P3 case scope interface for the case's accounts and parties in the user's scope.
5. DataProductRecordService: reads the product rows for those accounts or parties from P1 tables.
6. DataProductRecordService: for each field tagged is_personal in sys_fields, applies the P4 masking interface for the user's roles.
7. DataProductAccessService: writes the read to the PII access log with user, product, case, field list and time.
8. Controller: returns the rows with the product's freshness stamp.
9. User with Platform administration R: calls GET /admin/data-products and reads the 14 catalog entries with owner, system of record, refresh cycle, retention and fields with PDPA tags.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No data_product_access row for the user's roles and the product | 403; no row read; refusal written to the access log | MSG-P4-002 | AC3 |
| X2 | An access load names a role code not in the roles table | Load refused in full; previous version stays in force | MSG-P1-002 | AC4 |
| X3 | The case is outside the user's scope | 404; no row read; refusal logged | MSG-P4-003 | AC5 |
| X4 | No masking rule is loaded for a personal field | The field is masked for every role | None | AC6 |
| X5 | The PII access log cannot be written | Read refused with 503; no personal data returned | MSG-GEN-006 | AC7 |
| X6 | An access row has a valid-from date after today | The row is not in force; the read is refused until that date | MSG-P4-002 | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the tables and the metadata tables (RWB-E1-001), the P4 masking (RWB-E1-037) and the data product table (RWB-E1-064) |
| Negotiable | Which role reads which product, and which field is masked for whom, are data rows; the story fixes the checks |
| Valuable | Personal data reaches only the roles that need it, and every read is logged |
| Estimable | One access table, two endpoints, one read service, calls to three published interfaces |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion is one API test with synthetic parties and roles |

## 7. Acceptance criteria

```gherkin
Feature: Access control per data product and catalog entries

  Background:
    Given data product access version "DPA-2026.11" is in force from 2026-11-20
    Given case "RW-2026-000102" has borrower party "PTY-SYN-0102" with mobile contact point value "0812345678" stored as token
    Given no masking rule from Compliance is loaded for party or contact_point fields

  Scenario: AC1 Role access
    Given user "u-audit-01" holds read-only role RW-AUDIT, which reads DP02
    When the user calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then the mobile number shows as "******5678" and the national ID token is returned as "MASKED"
    Then the PII access log holds one entry with user "u-audit-01", product "DP02", case "RW-2026-000102" and the time of the read

  Scenario: AC2 Catalog entry
    Given the 14 data products DP01 to DP14
    When a data steward calls GET /admin/data-products
    Then the system returns 14 entries
    Then each has an owner role, a system of record, a refresh cycle, an expected-by time, a retention class and the field list with PDPA tags
    Then the DP02 entry lists 20 fields of which 9 are tagged personal

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
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A role reads a data product only through a data_product_access row in force for that role and product | REQ-RDF-010; FEAT-RDF-15 |
| BR2 | A personal field is masked unless the masking rules let the role see it | CTL-11; masking rules reference table; DL26 |
| BR3 | With no masking rule loaded, every personal field stays masked | DL26 ("Masking rules load with no values") |
| BR4 | Every read of personal data is written to the PII access log; a read that cannot be logged is refused | REQ-ACA-006; CTL-11 |
| BR5 | A record outside the caller's scope is refused | CTL-09; permission matrix |
| BR6 | An access load with an exception is refused in full; the previous version stays in force | Reference data change process, step 3; CTL-08 |
| BR7 | Each data product has one catalog entry with owner, system of record, refresh cycle, retention and fields with PDPA tags | REQ-RDF-011; sys_fields.is_personal |

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
| SY-DATALOAD, data load | Applies an approved access version to data_product_access |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PTY-002 | party | cif_no | Read |
| DF-PTY-004 | party | first_name | Read |
| DF-PTY-005 | party | last_name | Read |
| DF-PTY-007 | party | id_no_token | Read |
| DF-PTY-008 | party | date_of_birth | Read |
| DF-PTY-015 | contact_point | channel | Read |
| DF-PTY-016 | contact_point | value_token | Read |
| DF-PTY-018 | contact_point | consent_status | Read |
| DF-REF-035 | role | role_code | Read |
| DF-REF-042 | permission | capability_area | Read |
| DF-REF-043 | permission | letters | Read |
| DF-REF-097 | sys_fields | field_name | Read |
| DF-REF-105 | sys_fields | is_personal | Read |
| DF-REF-075 | data_product | owner_role | Read |
| DF-REF-074 | data_product | system_of_record | Read |
| DF-REF-077 | data_product | refresh_cycle | Read |
| DF-REF-080 | data_product_access | id | Write |
| DF-REF-081 | data_product_access | product_code | Write |
| DF-REF-082 | data_product_access | role_code | Write |
| DF-REF-083 | data_product_access | can_read | Write |
| DF-REF-084 | data_product_access | access_version | Write |
| DF-REF-085 | data_product_access | valid_from | Write |
| DF-REF-086 | data_product_access | valid_to | Write |
| DF-REF-119 | retention_rule | record_class | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Endpoints (new, see additions)**

| Item | GET /data-products/{productCode}/records | GET /admin/data-products |
|---|---|---|
| Request | Path: productCode (DP01 to DP14); query: caseId (required), page, size | Query: product (optional) |
| Response | DataProductRecordPage: items (record id, entity, fields map with masked values), freshness (FreshnessStamp from RWB-E1-015), page, size, total | DataProductCatalogEntry[]: productCode, productName, definition, ownerRole, systemOfRecord, refreshCycle, expectedBy, retentionClass, fields (entity, fieldName, fieldId, dataType, isPersonal) |
| Errors | 400 missing caseId (MSG-GEN-001); 401 (MSG-P4-001); 403 no capability right or no access row (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 503 PII log or store down (MSG-GEN-006) | 401; 403; 503 |
| Authorization | Case record, R; plus a data_product_access row in force | Platform administration, R |
| Idempotency | Not applicable | Not applicable |

**Endpoint used for the access load**

POST /api/recovery/v1/admin/reference-loads with table `data_product_access`, file and validFrom (Reference data, C); approval through POST /api/recovery/v1/admin/reference-loads/{loadId}/approve (Reference data, A). Errors 409 version clash (MSG-GEN-004), 422 field invalid (MSG-GEN-001). The P4 reference data service hands approved rows to P1 through DataProductAccessLoader.

**Published interfaces**

```java
// P1, called by the reference data service after approval
package recovery.dataengine.access.api;
public interface DataProductAccessLoader {
    LoadResult apply(String accessVersion, LocalDate validFrom, List<DataProductAccessRow> rows);
}

// P3, called by P1 to resolve a case to its accounts and parties within the caller's scope
package recovery.casewf.api;
public interface CaseScopeQuery {
    CaseLinks linksInScope(UUID caseId, UserContext user) throws CaseNotInScopeException;
}
public record CaseLinks(UUID caseId, List<UUID> accountIds, List<UUID> partyIds) {}

// P4, from RWB-E1-037
package recovery.access.api;
public interface MaskingPolicy {
    String apply(String objectName, String fieldName, String value, Set<String> roleCodes);
}
```

PII access logging goes through the ACE common module logging interface to PII Kafka with user, product, case, field names and time; no field value is logged.

## 13. Solution plan

- Package: folder `recovery/dataengine/access`, Java package `recovery.dataengine.access`.

| Component | Type | Responsibility |
|---|---|---|
| DataProductController | Controller | GET /data-products/{productCode}/records and GET /admin/data-products |
| DataProductAccessService | Service | Capability check, access row check, scope call, PII log write |
| DataProductRecordService | Service | Reads rows of the product's entities and applies masking by sys_fields.is_personal |
| DataProductCatalogService | Service | Builds catalog entries from data_product, sys_objects, sys_fields and retention_rule |
| DataProductAccessRepository | Repository | Reads and writes data_product_access |
| DataProductAccess | Entity | One row per product, role and version |
| DataProductAccessLoader | Published interface | Applies an approved access version |
| Data product access rule table | Rule table | data_product_access rows by version and valid-from date |

- Database: table data_product_access (new, Flyway migration in this story) with id uuid, product_code varchar(4), role_code varchar(20), can_read boolean, access_version varchar(20), valid_from date, valid_to date, standard columns; unique (product_code, role_code, access_version); index (role_code, product_code, valid_from). Reads sys_objects, sys_fields, data_product, retention_rule, party, contact_point, loan_account, collateral and the other P1 product tables. No read of role or permission tables: the capability check uses the ACE access check, and role codes come from the session.
- Configuration and reference data: access version "DPA-2026.11" prepared by the data steward and loaded by the reference data administrator; masking rules loaded by Compliance under RWB-E1-037 (DL26).
- Build steps:
  1. Flyway migration for data_product_access.
  2. DataProductAccessLoader with whole-load validation: known product code, known role code, no overlapping rows; refuse with MSG-P1-002.
  3. DataProductAccessService with the order: capability right, access row in force, scope through CaseScopeQuery.
  4. DataProductRecordService with masking from sys_fields.is_personal through MaskingPolicy; mask every personal field when no rule exists.
  5. PII access log write before the response is returned; refuse with 503 when it fails.
  6. DataProductCatalogService and GET /admin/data-products.
  7. Contract tests for both new endpoints from the additions schema (RWB-TE-003).
  8. Tests for AC1 to AC8 and the access test.
- Feature flag: `rwb.dataengine.product-access`.
- Done when: the tests in section 16 pass and the catalog returns 14 complete entries in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | No capability right or no access row for the product | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P1-002 | Access load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | caseId missing | Enter {field}. |
| MSG-GEN-006 | PII access log unavailable | {system} is not available. Your request is queued and will be retried. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. In Epic 1 the case record view SCR-03 (Read only) shows the product data the role may read, with personal fields masked. Catalog entries are read through GET /admin/data-products; SCR-47 Personal data shows masking rules from Epic 8.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-016-01 | AC1, BR1, BR2, BR4 | System | RW-AUDIT; case RW-2026-000102; synthetic party PTY-SYN-0102 |
| TC-E1-016-02 | AC2, BR7 | System | 14 data products; DP02 with 20 fields, 9 personal |
| TC-E1-016-03 | AC3, BR1 | System | RW-PHONECOL; product DP06 |
| TC-E1-016-04 | AC4, BR6 | System | Access load with role RW-UNKNOWN |
| TC-E1-016-05 | AC5, BR5 | System | RW-CASEOWN, case not owned |
| TC-E1-016-06 | AC6, BR3 | System | RW-COMPLY; no masking rules loaded |
| TC-E1-016-07 | AC7, BR4 | System | PII access log stub rejecting writes |
| TC-E1-016-08 | AC8, BR1 | System | Access row valid from 2026-12-15; test clock 2026-12-14 |
| TC-E1-016-09 | Access | Access | RW-TRIBE calls GET /admin/data-products; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: access by role and masking by role are data rows; the code holds no role or product list.
- No personal data in logs, tests or prompts: the PII access log carries field names, not values; test parties are synthetic.
- No read of another module's tables: case scope comes from CaseScopeQuery, masking from MaskingPolicy, roles from the session.
- A read that cannot be logged returns no personal data.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role; personal data masked by role under PDPA | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | All recovery processes | CTL-09, CTL-11; DL26 | TC-E1-016-01, TC-E1-016-03 to TC-E1-016-08 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record, refresh and retention | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-16 | All recovery processes | CTL-08 | TC-E1-016-02 |

## 19. Out of scope

- The role to permission matrix and the masking rule mechanism (RWB-E1-037).
- The access log search and break-glass (RWB-E1-039).
- Masking rule values per role and field (DL26, Compliance).
- The personal data screen SCR-47 (Epic 8).
- Data product definitions and the field dictionary (RWB-E1-064).
