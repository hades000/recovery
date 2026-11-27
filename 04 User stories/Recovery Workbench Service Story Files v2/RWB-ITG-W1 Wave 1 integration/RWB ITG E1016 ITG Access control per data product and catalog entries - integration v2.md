# RWB-ITG-E1016-ITG Access control per data product and catalog entries

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1016-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP05, DP07, DP08, DP11, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | RWB-P1-E1016-APP, RWB-P4-E1016-APP, RWB-P5-E1016-APP |
| Contract dependencies | Wave 1 /v1 contracts of rwb-source-data, rwb-access, rwb-document and rwb-case (see 12.2); contract version: Not specified in the source documents (DOR-RWB-ITG-E1016-ITG-23) |
| Integration dependencies | RWB-P1-E1016-APP, RWB-P4-E1016-APP, RWB-P5-E1016-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019, FR-PLT-026, FR-PLT-033) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-016 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 7 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-016 data-product catalog entry across rwb-source-data (P1), rwb-access (P4), rwb-document (P5) and rwb-case (P3)**, so that **the catalog a data steward reads is the composed, cross-service truth and not a local copy**.

### 2. Business rationale

Audit findings record staff sending debtor data outside the bank and users holding access they did not need (CTL-11, CTL-09). The legacy story builds the access rows, the masking and one catalog entry per data product inside one engine. This story owns exactly one legacy acceptance criterion, **AC2 (Catalog entry)**, and proves it end to end on the target services: the DP01 entry a data steward reads must carry the owner role, the system of record "ACE (ingested from ALS)", the refresh cycle "DAILY", the expected-by time "08:00" and a retention class; the entry must list the six views **v_ace_account, v_ace_payment, v_ace_aa_relation, v_ace_bucket_log, v_ace_product and v_ace_branch** with system of record "ACE", and **account_ext** with system of record "Workbench"; the field **days_past_due** must show field ID **DF-ACE-018**, source system "ACE" and source field **public.account.delay_days**; the entry must list **REC-01 and REC-02** and the **data_product_access** rows for DP01; and the field list must carry the **PDPA tag** of each field, taken from **sys_fields.is_personal**.

The target split decides which service answers which part of that one entry. rwb-source-data (P1) owns data_product, data_product_access, sys_fields and sys_objects and serves the catalog through its own API; rwb-access (P4) owns the Recovery roles as data, the scope and the masking policy, and resolves the owner role and the caller's rights; rwb-document (P5) owns retention_rule and therefore the retention class; rwb-case (P3) keeps the case, its parties and the non-DoA reference data. No service copies another service's table, so the single legacy query becomes one composed read over three owner contracts, and the catalog a data steward sees is the composed truth rather than a local copy. The entry-candidate read is GET /api/recovery/source-data/v1/entry-candidates, with businessDate and threshold as required query parameters and page and size optional; it answers EntryCandidatePage with businessDate, threshold, asOf, page, size, total, candidates[] and breaks[], uses the status set 400, 401, 403, 409, 422 and 503, and is called by the service identity of rwb-case. This story publishes the OpenAPI 3.1 fragment of these operations with the service API document, because no contract story of this key exists.

The composition of the catalog across P1, P4 and P5 and the exposure path of the P5 retention class are not specified as one contract in the Ownership Map (GAP-0341; ASM-0435). No service contract is faked: every service in the path is the real service on its published wave 1 contract, and only the outside systems stand in as stubs.

### 3. Preconditions

- RWB-P1-E1016-APP is done: the data products, the 30 read-only ACE views, data_product_access, sys_fields and sys_objects are served by rwb-source-data's catalog API, and the published P1 contract is in the registry.
- RWB-P4-E1016-APP is done: the roles, the scope, the masking policy and the authorise operation are served by rwb-access, and the published P4 contract is in the registry.
- RWB-P5-E1016-APP is done: retention_rule and the retention class are served by rwb-document, and the published P5 contract is in the registry.
- The published P3 contract is in the registry: the case and its parties are read from rwb-case for the scope check.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic set: customer P0000102 and case RW-2026-000102, with access version "DPA-2026.11".
- SIT is provisioned with the rwb-recovery Temporal namespace, the wave 1 Kafka topics and the stub endpoints for ACE customer fixture, mock sign-in and PII log.
- No production data is used anywhere in this story; every value is synthetic.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. Seed the synthetic case RW-2026-000102, its borrower person_key P0000102 and the access version "DPA-2026.11" through the RWB-ITG-W1J01-ITG harness.
2. Apply the access version through the P4 contract so the version in force is the one the suite asserts.
3. Read the DP01 entry from rwb-source-data's catalog operation GET /api/recovery/source-data/v1/admin/data-products. (P1)
4. Resolve the owner role named in that entry and the caller's rights through rwb-access: POST /api/recovery/access/v1/authorise and GET /api/recovery/access/v1/me/permissions. (P4)
5. Read the retention class of the DP01 entry owned by rwb-document through the P5 contract, never from a P1 copy. (P5)
6. Read the field metadata and the PDPA tags of the DP01 entry through GET /api/recovery/source-data/v1/admin/data-dictionary/fields, and the masked record path through GET /api/recovery/data-products/{productCode}/records. (P1)
7. Confirm the case scope through rwb-case GET /api/recovery/case/v1/cases/{caseId} and GET /api/recovery/case/v1/cases/{caseId}/parties. (P3)
8. Assert every AC2 value: owner role, system of record, refresh cycle, expected-by, retention class, the six views and account_ext, DF-ACE-018 with its source field, REC-01 and REC-02, the access rows for DP01 and the PDPA tag of every field.
9. Assert that no response and no log line holds the clear identity number 1234567890123; the PII log carries field names only.
10. Write the catalog assertion report with one row per AC2 value and clean up the synthetic fixture rows of the run.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The P1 catalog entry for DP01 is missing one of the six v_ace_* views or account_ext | The assertion fails on the missing view and names the product and the view; the suite never fills the gap from a table read | MSG-P1-003 | AC2; BR7, BR10 |
| X2 | rwb-access does not resolve the owner role of the DP01 entry, or returns no rights for the caller | The composed entry stays incomplete; the report names the unresolved owner role from the P4 contract and the run fails | MSG-P4-002 | AC2; BR1, BR11 |
| X3 | rwb-document returns no retention class for DP01 | The retention class cell is empty and the assertion fails with the product code and the missing class | None | AC2; BR13 |
| X4 | A field of the DP01 list carries no PDPA tag in the P1 data dictionary | The assertion fails and names the field ID; the suite assumes no default tag | None | AC2; BR7, BR11 |
| X5 | A field tagged is_personal is returned in clear by the P1 records read | The run fails with the field name only, never the value; the check is repeated over the whole field list | None | AC2; BR4, BR15 |
| X6 | The PII log cannot be read back or is unavailable during the run | The read is refused with 503 and the suite records no personal field | MSG-GEN-006 | AC2; BR4 |
| X7 | A published contract on P1, P3, P4 or P5 drifts from the wave 1 version the suite pins | The contract check fails before the assertion; the run stops and names the operation and the schema version | None (pipeline log) | AC2; BR11, BR14 |
| X8 | The synthetic fixture is missing: no customer P0000102 or no case RW-2026-000102 | The harness reports the missing fixture and the run stops; no data is created outside the fixture | None (harness log) | AC2; BR14, BR15 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on three finished APP stories and their published contracts; the harness is already in place, so the suite waits for no other work |
| Negotiable | Product codes, role codes, field IDs and access rows are data; the story fixes only the assertions of AC2 |
| Valuable | A data steward sees the composed catalog truth of three owning services, and no service keeps a copy of another service's table |
| Estimable | One suite module, three synthetic fixtures and seven contract reads |
| Small | One suite module, finished inside two weeks with its assertions |
| Testable | Every Then is one assertion on a published contract response, with synthetic values only |

### 7. Acceptance criteria

```gherkin
Feature: Access control per data product and catalog entries

  Background:
    Given data product access version "DPA-2026.11" is in force from 2026-11-20
    Given case "RW-2026-000102" has borrower person_key "P0000102" whose ACE customer has identity number "1234567890123" and mobile "0812345678"
    Given no masking rule from Compliance is loaded for the v_ace_customer or v_ace_contact fields
    Given all involved services are deployed in SIT with their published contracts
    Given the RWB-ITG-W1J01-ITG synthetic set is loaded

  Scenario: AC2 Catalog entry (legacy RWB-E1-016 AC2)
    Given the 14 data products DP01 to DP14
    When a data steward calls GET /admin/data-products?product=DP01
    Then the system returns the DP01 entry with owner role, system of record "ACE (ingested from ALS)", refresh cycle "DAILY", expected-by "08:00" and a retention class
    Then the entry lists the views v_ace_account, v_ace_payment, v_ace_aa_relation, v_ace_bucket_log, v_ace_product and v_ace_branch with system of record "ACE", and account_ext with system of record "Workbench"
    Then the field days_past_due shows field ID "DF-ACE-018", source system "ACE" and source field "public.account.delay_days"
    Then the entry lists REC-01 and REC-02 and the data_product_access rows for DP01
    Then the field list carries the PDPA tag for each field, taken from sys_fields.is_personal

  Scenario: AC12 The suite reads each owner's published contract and copies no row (BR11 to BR15) (new, D-RCV-60)
    Given the rwb-source-data, rwb-access and rwb-document contracts are published
    When the suite asserts the AC2 catalog entry
    Then every value is read through a published contract, no response or log holds the clear identity number, and the PII log carries field names only

  Scenario: AC13 A consumed call that fails or does not answer is refused (new, D-RCV-60)
    Given the rwb-access contract does not answer
    When a data steward calls GET /admin/data-products?product=DP01
    Then the system refuses the read and returns no partial DP01 entry

  Scenario: AC14 A status change the model does not allow is refused (new, D-RCV-60)
    Given the data product DP01 has a status that the model does not allow to change
    When a data steward requests that change
    Then the change is refused and the entry stays as it was
```

**Target reading.** The catalog is served by rwb-source-data's GET /admin/data-products. The owner role and the access rows are resolved through rwb-access. The retention class is owned by rwb-document. The retention class cell of the entry is therefore read from the P5 contract and joined to the P1 entry by product code inside the suite; the suite reads each owner's contract and never joins tables. The views named in AC2 are read only by rwb-source-data, and no other service holds a grant on them (GAP-0341; ASM-0435).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A role reads a data product only through a data_product_access row in force for that role and product | RWB-E1-016 BR1 |
| BR2 | A personal field is masked unless the masking rules let the role see it | RWB-E1-016 BR2 |
| BR3 | With no masking rule loaded, every personal field stays masked | RWB-E1-016 BR3 |
| BR4 | Every read of personal data is written to the PII access log; a read that cannot be logged is refused | RWB-E1-016 BR4 |
| BR5 | A record outside the caller's scope is refused | RWB-E1-016 BR5 |
| BR6 | An access load with an exception is refused in full; the previous version stays in force | RWB-E1-016 BR6 |
| BR7 | Each data product has one catalog entry with owner, system of record, refresh cycle, retention, the views and tables behind it, the reconciliations and fields with PDPA tags | RWB-E1-016 BR7 |
| BR8 | Source data access is the view grant: the source service holds SELECT on the ACE views and no privilege on `public`, and may not write any view. A direct public table read fails at the database, not in code review | RWB-E1-016 BR8 |
| BR9 | There is no tokenization. The customer view returns the identity number as id_no_masked and id_no_last4 only; the contact view returns the full phone, email and address because notices and calls need them, and the API masks them by role | RWB-E1-016 BR9 |
| BR10 | Every one of the 30 ACE views belongs to its data product with system of record "ACE"; a view marked "Workbench" is refused | RWB-E1-016 BR10 |
| BR11 | rwb-source-data's catalog contract is authoritative for the data products, the views behind them, the field dictionary and the PDPA tags; the suite reads them through GET /admin/data-products and GET /admin/data-dictionary/fields and copies no row | new, integration (P1 catalog ownership, Ownership Map) |
| BR12 | rwb-access is authoritative for role codes, scope and masking; the suite resolves the owner role and the caller's rights through POST /authorise and GET /me/permissions | new, integration (P4 ownership, Ownership Map) |
| BR13 | rwb-document is authoritative for the retention class; the suite reads it through the P5 contract and never from a P1 copy | new, integration (P5 ownership of retention_rule) |
| BR14 | No cross-service table read: the suite holds no schema, joins no tables and asserts only through published contracts | new, integration (DP-01, DP-11) |
| BR15 | No clear personal data in any response, log or fixture: the suite asserts masked values, and the PII log carries field names, not values | new, integration (BR4, BR9) |

### 9. State transitions

None. This story does not change a case status. It observes the access version in force and the catalog version.

| Observed state | Meaning for the suite | Source of truth |
|---|---|---|
| Access version valid | The data_product_access rows of "DPA-2026.11" are in force and the DP01 rows are readable | P4 rwb-access over P1 data_product_access |
| Access version not yet in force | The rows with a valid-from date after the run date are not returned; the assertion is skipped for that version and recorded | P4 rwb-access |
| Access version expired | The rows of the previous version are not returned; the entry still lists the version in force | P4 rwb-access |
| Catalog entry complete | Every AC2 value is present: owner role, system of record, refresh cycle, expected-by, retention class, six views and account_ext, DF-ACE-018, REC-01 and REC-02, the access rows and the PDPA tags | P1 rwb-source-data, P5 rwb-document |
| Catalog entry with a missing field | The entry is returned without that value; the assertion fails and the report names the value, never a substituted default | P1 rwb-source-data |

### 10. Authority

| Role | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, reads the assertion report and records failures against the story |
| Data steward | Reads the DP01 catalog entry and confirms that the composed entry is the one their work reads |
| Compliance and PDPA officer | Owns the masking rules and the PDPA tag source; confirms that no personal field is returned in clear |
| Security administrator | Owns the role to permission matrix and the scope; reads the access log |
| Service owner of rwb-source-data | Publishes and versions the catalog and dictionary contracts |
| Service owner of rwb-access | Publishes and versions the authorise and permissions contracts |
| Service owner of rwb-document | Publishes and versions the retention contract |
| Platform administrator | Owns the SIT namespace, the topics and the stub endpoints for the outside systems |

### 11. Data

All values in this story are synthetic; the run holds no production data. Field IDs are those of the Logical Data Model and the Data Dictionary and are copied unchanged.

| BR Field ID | Entity | Field | Source | Read or write |
|---|---|---|---|---|
| DF-ACE-055 | v_ace_customer | cif_no | P1 rwb-source-data, ACE view | Read |
| DF-ACE-056 | v_ace_customer | person_key | P1 rwb-source-data, ACE view | Read |
| DF-ACE-057 | v_ace_customer | first_name | P1 rwb-source-data, ACE view | Read |
| DF-ACE-058 | v_ace_customer | last_name | P1 rwb-source-data, ACE view | Read |
| DF-ACE-059 | v_ace_customer | date_of_birth | P1 rwb-source-data, ACE view | Read |
| DF-ACE-061 | v_ace_customer | deceased_flag | P1 rwb-source-data, ACE view | Read |
| DF-ACE-073 | v_ace_customer | id_no_masked | P1 rwb-source-data, ACE view | Read |
| DF-ACE-074 | v_ace_customer | id_no_last4 | P1 rwb-source-data, ACE view | Read |
| DF-ACE-075 | v_ace_contact | contact_type | P1 rwb-source-data, ACE view | Read |
| DF-ACE-076 | v_ace_contact | contact_key | P1 rwb-source-data, ACE view | Read |
| DF-ACE-077 | v_ace_contact | person_key | P1 rwb-source-data, ACE view | Read |
| DF-ACE-078 | v_ace_contact | contact_value | P1 rwb-source-data, ACE view | Read |
| DF-ACE-079 | v_ace_contact | contact_value_masked | P1 rwb-source-data, ACE view | Read |
| DF-ACE-080 | v_ace_contact | usage_code | P1 rwb-source-data, ACE view | Read |
| DF-EXT-001 | party_ext | person_key | P1 rwb-source-data | Read |
| DF-EXT-002 | party_ext | vulnerable | P1 rwb-source-data | Read |
| DF-EXT-003 | party_ext | deceased_override | P1 rwb-source-data | Read |
| DF-EXT-004 | party_ext | bankruptcy | P1 rwb-source-data | Read |
| DF-EXT-005 | party_ext | fraud_flag | P1 rwb-source-data | Read |
| DF-EXT-013 | contact_point_ext | contact_key | P1 rwb-source-data | Read |
| DF-EXT-014 | contact_point_ext | contact_type | P1 rwb-source-data | Read |
| DF-EXT-015 | contact_point_ext | consent_given | P1 rwb-source-data | Read |
| DF-EXT-018 | contact_point_ext | failed_count | P1 rwb-source-data | Read |
| DF-EXT-027 | account_ext | account_key | P1 rwb-source-data | Read |
| DF-REF-071 | data_product | product_code | P1 rwb-source-data, catalog | Read |
| DF-REF-074 | data_product | system_of_record | P1 rwb-source-data, catalog | Read |
| DF-REF-075 | data_product | owner_role | P1 rwb-source-data, resolved through P4 | Read |
| DF-REF-077 | data_product | refresh_cycle | P1 rwb-source-data, catalog | Read |
| DF-REF-080 | data_product_access | id | P1 rwb-source-data, read as an access row | Read |
| DF-REF-081 | data_product_access | product_code | P1 rwb-source-data, read as an access row | Read |
| DF-REF-082 | data_product_access | role_code | P1 rwb-source-data, resolved through P4 | Read |
| DF-REF-083 | data_product_access | can_read | P1 rwb-source-data, read as an access row | Read |
| DF-REF-084 | data_product_access | access_version | P1 rwb-source-data, read as an access row | Read |
| DF-REF-085 | data_product_access | valid_from | P1 rwb-source-data, read as an access row | Read |
| DF-REF-086 | data_product_access | valid_to | P1 rwb-source-data, read as an access row | Read |
| DF-REF-088 | sys_objects | object_name | P1 rwb-source-data | Read |
| DF-REF-091 | sys_objects | data_product | P1 rwb-source-data | Read |
| DF-REF-092 | sys_objects | system_of_record | P1 rwb-source-data | Read |
| DF-REF-097 | sys_fields | field_name | P1 rwb-source-data | Read |
| DF-REF-103 | sys_fields | source_system | P1 rwb-source-data | Read |
| DF-REF-105 | sys_fields | is_personal | P1 rwb-source-data | Read |
| DF-REF-119 | retention_rule | record_class | P5 rwb-document | Read |
| DF-REF-199 | masking_rule | role_code | P4 rwb-access, through POST /api/recovery/access/v1/authorise | Read |
| DF-REF-200 | masking_rule | field_id | P4 rwb-access, through POST /api/recovery/access/v1/authorise | Read |
| DF-REF-201 | masking_rule | unmasked | P4 rwb-access, through POST /api/recovery/access/v1/authorise | Read |

The DP01 entry, the six views with account_ext, the access rows for DP01 and the retention class come from the RWB-ITG-W1J01-ITG synthetic set. The DP01 entry is composed by reading the P1 catalog API, resolving roles and masking through P4 and reading the retention class from P5; no service copies another service's table. The data_product_access seed holds only the six rows the sources give under version DPA-2026.11 (RW-CASEOWN and RW-AUDIT read DP02; RW-PHONECOL reads DP01, DP02, DP03 and DP05); every other role and product is left to a later approved load through the rwb-case reference-data contract, and no role is granted a product by default. The approved access load arrives as reference data for table code data_product_access through the rwb-case reference-data contract, handled by a handler in rwb-source-data; the service exposes no load endpoint of its own. Criteria and test data read the P1 catalog and access contracts, not the ACE views directly (BR14). The masking rows are not read by table: P1 takes the masking answer from POST /api/recovery/access/v1/authorise and the FieldMasker interface of RWB-P4-E1037-CON, one hop with a 2 s timeout. The fixture rows are Not specified in the source documents (ASM-0435).

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The reserved names of P2 rwb-integration — /api/recovery/integration/v1, rwb.integration.events.v1, rwb-integration and rwb_integration — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Operation | Owner | What the suite reads | Call type |
|---|---|---|---|
| GET /api/recovery/source-data/v1/admin/data-products | P1 rwb-source-data | The DP01 catalog entry: owner role, system of record, refresh cycle, expected-by, the views behind it, the fields and their IDs, the reconciliations and the access rows | REST |
| GET /api/recovery/source-data/v1/admin/data-dictionary/fields | P1 rwb-source-data | The field IDs, the field names, the source system and is_personal, which is the PDPA tag of each field | REST |
| GET /api/recovery/source-data/v1/data-products/{productCode}/records | P1 rwb-source-data | The masked record values and the PII log path for the read | REST |
| GET /api/recovery/access/v1/me/permissions | P4 rwb-access | The caller's role and rights, which decide whether the catalog entry is readable | REST |
| POST /api/recovery/access/v1/authorise | P4 rwb-access | The role, scope and DoA answer that resolves the owner role of the entry | REST |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | The case of RW-2026-000102 that the scope check uses | REST |
| GET /api/recovery/case/v1/cases/{caseId}/parties | P3 rwb-case | The party links of the case for the scope check | REST |

All seven calls are one hop from the suite with a 2 s timeout and a circuit breaker per downstream (ADR-020). No call is retried more than once, and no call is chained into another service.

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

None. The catalog read is synchronous, so the suite consumes no event. The services' own AccessPolicyChanged and DoaLimitChanged events are outside this AC.

#### 12.5 Workflows and activities

None. The suite starts no workflow; the read path is synchronous REST.

#### 12.6 Schedules

| Schedule | Job | Owner | Run by this story |
|---|---|---|---|
| Access review list, six-monthly | JOB-18 | P4 rwb-access | No. Named only as the owner of the access review |

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The data behind the composed entry is reached only through the contracts of its owners.

| Data | Owner | Reached through |
|---|---|---|
| data_product, data_product_access, sys_fields, sys_objects | P1 rwb-source-data | P1 catalog and dictionary contracts |
| Role, scope and masking policy, masking_rule | P4 rwb-access | P4 authorise and permissions contracts |
| retention_rule | P5 rwb-document | P5 retention contract |
| Case, case parties, reference data | P3 rwb-case | P3 case and reference contracts |

#### 12.8 Contract fakes

| Stand-in | Owner | Used for |
|---|---|---|
| ACE customer fixture, RWB-ITG-W1J01-ITG | QA harness | The synthetic customer P0000102 and the ACE data behind the views |
| Mock Entra sign-in | Platform | The session of the synthetic users |
| PII log stub | Platform | The read-back of the PII log entries |
| rwb-source-data contract fake | P1 rwb-source-data | Test data of the DP01 entry, its views and account_ext; library version: Not specified in the source documents (DOR-RWB-ITG-E1016-ITG-22) |
| rwb-access contract fake | P4 rwb-access | Role, scope and masking data behind authorise and permissions; library version: Not specified in the source documents (DOR-RWB-ITG-E1016-ITG-22) |
| rwb-case contract fake | P3 rwb-case | Case and party data behind the case scope; library version: Not specified in the source documents (DOR-RWB-ITG-E1016-ITG-22) |

The stand-ins above cover outside systems, except the rwb-source-data, rwb-access and rwb-case contract fakes, which stand in for those service contracts; every other operation in 12.2 is the real service on its published wave 1 contract.

#### 12.9 Call-type summary

| Call type | Provided | Consumed |
|---|---|---|
| REST | 0 | 7 |
| Kafka | 0 | 0 |
| Temporal | 0 | 0 (JOB-18 named only) |
| File | None | None |

### 13. Solution plan

| Deliverable | Type | Responsibility |
|---|---|---|
| ITG suite module for the E1016 catalog entry | Suite module | Reuses the RWB-ITG-W1J01-ITG harness; seeds the fixture, reads the owner contracts and asserts every AC2 value |
| Synthetic fixtures for customer P0000102, case RW-2026-000102, access version "DPA-2026.11" and the DP01 entry | Data | Data rows only; no business value in the code |
| Catalog assertion report | Report | One row per AC2 value with pass or fail, field names only, no values |

No service code and no schema change is part of this story.

| DP | Legacy marker in RWB-E1-016 | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` and the recovery schema read in the flow | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data and LOV behind the entry | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard and the capability check | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call and the published interfaces DataProductAccessLoader, CaseScopeQuery, FieldMasker | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-19 | Screen and the case record view behind the entry | gateway-bff composite route | H RWB-PLT-N001-CON |

The rows above are the pattern rows of §R5.5 and they name the platform contract stories that the libraries and the guard carry in wave 0. This story adds no build dependency of its own: it has no H dependency, and it has no build dependency on an ITG story. The dependency it does have is the real cross-service behaviour of the three APP stories it names, which is why they sit in Integration dependencies.

Build steps:

1. Extend the RWB-ITG-W1J01-ITG harness with a suite module for the E1016 catalog entry, so the fixture and the synthetic users are shared.
2. Load the fixture: case RW-2026-000102, borrower person_key P0000102, access version "DPA-2026.11" and the DP01 entry with the six views, account_ext, REC-01, REC-02 and the access rows.
3. Read the DP01 entry from the P1 catalog contract and record every value it returns.
4. Resolve the owner role and the caller's rights through the P4 authorise and permissions contracts.
5. Read the retention class through the P5 contract and match it to the DP01 entry by product code.
6. Read the field metadata and the PDPA tags through the P1 dictionary contract, and the masked record path through the P1 records contract.
7. Assert every AC2 value and assert that no response and no log line holds the clear identity number.
8. Publish the catalog assertion report, reset the fixture rows of the run and leave the SIT data as found.

Done when every AC2 assertion passes in SIT against the real wave 1 contracts, the catalog assertion report is attached to the story, the test cases of section 16 are recorded, and no service table was read outside its owner's contract.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | No capability right or no access row for the product | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P1-002 | Access load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-003 | A catalog load marks a view with a system of record other than ACE | {product} must have exactly one system of record and one named owner. |
| MSG-GEN-001 | caseId missing | Enter {field}. |
| MSG-GEN-006 | PII access log unavailable | {system} is not available. Your request is queued and will be retried. |

No new message ID is created by this story. Thai text for each message follows decision DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 apply).

### 15. Screens and states

| Screen | Mode | What it shows |
|---|---|---|
| SCR-03 Case record | Read only | The product data the role may read, with the personal fields masked. States: loading as in Screen Specifications v1 SCR-03; empty, error and no access: Not specified in the source documents (CG-ALL-216) |
| SCR-47 Personal data | Epic 8 | Out of scope for this story. States: loading as in Screen Specifications v1 SCR-47; empty, error and no access: Not specified in the source documents (CG-ALL-217) |

The catalog itself is an API read through GET /admin/data-products and has no screen in this story. The suite reads that operation, not a screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-016-01-ITG | AC1, BR1, BR2, BR4, BR9 (run by owner story) | Integration | RW-AUDIT; case RW-2026-000102; synthetic customer P0000102 with identity 1234567890123 and mobile 0812345678; end-to-end: real services on the wave 1 contracts |
| TC-E1-016-02-ITG | AC2, BR7 | Integration | DP01 entry and its six views and account_ext from the rwb-source-data contract fake; DF-ACE-018; access rows; other services real on the wave 1 contracts |
| TC-E1-016-03-ITG | AC3, BR1 (run by owner story) | Integration | RW-PHONECOL; product DP06; end-to-end: real services on the wave 1 contracts |
| TC-E1-016-04-ITG | AC4, BR6 (run by owner story) | Integration | Access load with role RW-UNKNOWN; end-to-end: real services on the wave 1 contracts |
| TC-E1-016-05-ITG | AC5, BR5 (run by owner story) | Integration | RW-CASEOWN, case not owned; end-to-end: real services on the wave 1 contracts |
| TC-E1-016-06-ITG | AC6, BR3 (run by owner story) | Integration | RW-COMPLY; no masking rules loaded; end-to-end: real services on the wave 1 contracts |
| TC-E1-016-07-ITG | AC7, BR4 (run by owner story) | Integration | PII access log stub rejecting writes; end-to-end: real services on the wave 1 contracts |
| TC-E1-016-08-ITG | AC8, BR1 (run by owner story) | Integration | Access row valid from 2026-12-15; test clock 2026-12-14; end-to-end: real services on the wave 1 contracts |
| TC-E1-016-09-ITG | Access | Integration | RW-TRIBE calls GET /admin/data-products; refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-016-10-ITG | AC9, BR8 (run by owner story) | Integration | recovery_svc; SELECT public.customer; SELECT and INSERT on v_ace_customer; all 30 views from the rwb-source-data contract fake; other services real on the wave 1 contracts |
| TC-E1-016-11-ITG | AC10, BR7, BR10 (run by owner story) | Integration | 30 views from the rwb-source-data contract fake; 122 objects and 1,366 fields; other services real on the wave 1 contracts |
| TC-E1-016-12-ITG | AC11, BR10 (run by owner story) | Integration | Catalog load via the rwb-source-data contract fake setting v_ace_customer to Workbench; other services real on the wave 1 contracts |
| TC-E1-016-13-ITG | ASM-3438 | Integration | Boundary values for the tables of 12.7; data: Not specified in the source documents (DOR-RWB-ITG-E1016-ITG-12); end-to-end: real services on the wave 1 contracts |
| TC-E1-016-14-ITG | AC12, BR11, BR12, BR13, BR14, BR15 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1016-ITG-AC12); end-to-end: real services on the wave 1 contracts |
| TC-E1-016-15-ITG | AC13 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1016-ITG-AC13); end-to-end: real services on the wave 1 contracts |
| TC-E1-016-16-ITG | AC14 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1016-ITG-AC14); end-to-end: real services on the wave 1 contracts |

TC-E1-016-02-ITG is the copy this story signs off: it is the end-to-end run of AC2 on the composed catalog entry. The other eleven are regression evidence for the sibling stories RWB-P1-E1016-APP, RWB-P4-E1016-APP and RWB-P5-E1016-APP, and this story runs them to show that the composed entry does not move when the owners change. The full test, with its Given, When and Then, is in the Recovery Workbench Test Cases workbook, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- Synthetic data only: customer P0000102, case RW-2026-000102 and the access rows are fixtures of the harness; no production data is read, copied or logged.
- No clear personal data in any response, log, report or fixture: the suite asserts masked values and the PII log carries field names, not values.
- No cross-service table read: the suite holds no schema, joins no table and asserts only through the contracts of the owners.
- No business value in test code: role codes, product codes and access rows are data rows of the fixture.
- One hop and 2 s per call, with a circuit breaker per downstream; no call is chained into another service.
- The PII log check reads field names and the time of the read only.
- No production access of any kind from the suite, and no write path into a service schema.

### 18. Traceability

| Requirement | ADR and DP | Contract element | Test cases | Stories |
|---|---|---|---|---|
| REQ-RDF-010 | ADR-020; DP-01, DP-08, DP-11 | P4 POST /authorise and GET /me/permissions; P1 GET /admin/data-products and GET /data-products/{productCode}/records | TC-E1-016-01-ITG, TC-E1-016-03-ITG, TC-E1-016-05-ITG, TC-E1-016-06-ITG, TC-E1-016-09-ITG | RWB-E1-016; RWB-P1-E1016-APP, RWB-P4-E1016-APP, RWB-P5-E1016-APP |
| REQ-RDF-011 | ADR-020; DP-01, DP-07, DP-11 | P1 GET /admin/data-products and GET /admin/data-dictionary/fields; P5 retention contract | TC-E1-016-02-ITG, TC-E1-016-11-ITG, TC-E1-016-12-ITG | RWB-E1-016; RWB-P1-E1016-APP, RWB-P4-E1016-APP, RWB-P5-E1016-APP |
| REQ-ACA-006 | ADR-020; DP-08, DP-11 | P1 GET /data-products/{productCode}/records and the PII log path; P4 POST /authorise | TC-E1-016-02-ITG, TC-E1-016-07-ITG, TC-E1-016-10-ITG | RWB-E1-016; RWB-P1-E1016-APP, RWB-P4-E1016-APP, RWB-P5-E1016-APP |

The legacy story is RWB-E1-016, disposition Split (rework). The three APP stories named above are its build owners in the target services; this ITG story is the proof over them and holds no other acceptance criterion.

### 19. Out of scope

- The P1, P4 and P5 APP builds themselves: RWB-P1-E1016-APP, RWB-P4-E1016-APP and RWB-P5-E1016-APP.
- The P1 contract, database and operations stories of the same legacy key.
- The non-owned acceptance criteria of RWB-E1-016: AC1, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10 and AC11.
- The personal data screen SCR-47, which is Epic 8.
- The harness build RWB-ITG-W1J01-ITG; this story reuses it.
- The non-functional epic RWB-ITG-NFR: throughput, latency targets beyond the 2 s call timeout and resilience testing.
- Any change to the ACE views, to the grants or to the role to permission matrix.
