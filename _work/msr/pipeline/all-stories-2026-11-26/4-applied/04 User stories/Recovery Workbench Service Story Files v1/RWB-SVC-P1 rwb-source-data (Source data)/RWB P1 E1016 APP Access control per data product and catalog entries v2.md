# RWB-P1-E1016-APP Access control per data product and catalog entries

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP05, DP07, DP08, DP11, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1069-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1016-DB |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-004, FR-P1-006, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-026, FR-P1-027, FR-P1-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-016 for rwb-source-data. The access rows, the product records read and the catalog entry stay with the service that owns `data_product_access`, `sys_objects`, `sys_fields` and `data_product` in schema `rwb_source_data` (DP-01, DP-02; Architecture v5 slides 29 and 41); the role to permission matrix, the masking answer and the masking rows move to rwb-access and are consumed through its contracts (DP-08; Ownership Map v1, `masking_rule` to P4); the indexes, the catalog read model and the access seed move to the DB slice RWB-P1-E1016-DB. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-E1016-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **read access to each data product granted by role, source data reached only through the ACE view grant, personal fields masked by role from `v_ace_customer` and `v_ace_contact`, every read logged, and a catalog entry per product that names its owner, system of record, freshness, views and tables and fields**, so that **personal data is read only by the roles that need it and every product is findable**.

The legacy story built the behaviour inside one monolith process and one `recovery` schema. D-RCV-60 keeps the behaviour and moves the ownership:

- **Kept word for word:** the ten acceptance criteria this story owns (AC1, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11), their values, the messages MSG-P4-002, MSG-P4-003, MSG-P1-002, MSG-P1-003, MSG-GEN-001 and MSG-GEN-006, the two read operations and the ten business rules of section 8. No legacy line is dropped or reworded; a mock `Given` is added only where a cross-service part is stubbed.
- **The access rows are still P1's, the masking rows are not.** `data_product_access` is a table of this service in `rwb_source_data` (Ownership Map v1). `masking_rule` is a table of rwb-access (P4) and is read here only through the published `FieldMasker` interface of RWB-P4-E1037-CON, never by SQL: a second service's table may not be named in a query (DP-01, DP-08).
- **The authorise answer replaces the in-process guard.** The legacy `RecoveryAccessGuard` becomes one call to `POST /api/recovery/access/v1/authorise` owned by rwb-access (P4), one hop, 2 s timeout, and the answer carries the role, the right, the scope and a marker per field ID (DP-08, DP-11; Architecture v5 slides 11 and 14).
- **The case scope comes from P1's own rows plus the views, not from a case table.** P1 resolves a case's account keys from its own `case_list_row` and its person keys from the ACE views (`v_ace_account` to `v_ace_customer`); it reads no P3 case table and needs no P3 case contract. The authorise answer supplies the role, the right and the scope values, and P1 filters `case_list_row` by team and owner scope.
- **Bases and names:** REST base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-02, DP-13, DP-14; Architecture v5 slide 41).
- **What this story does not deliver:** the three indexes, the catalog read model `v_data_product_catalog`, the `data_product_access` seed and the schema checks are RWB-P1-E1016-DB (external dependency X). The tables themselves are already created by RWB-P1-E1001-APP, and the 30 `recovery.v_ace_*` views, their grants and boundary rule BND-6 by RWB-P1-E1069-APP and RWB-P1-E1069-DB (DP-05).

### 2. Business rationale

Audit findings record staff sending debtor data outside the bank and users holding access they did not need (CTL-11, CTL-09). Under D-RCV-35 there is no load and no tokenization: source data is reached only through the `recovery.v_ace_*` views, so access to a data product is the role's access row plus the database grant on the view, and the identity number is masked inside `v_ace_customer` itself. Access rows held as data limit each role to the products its work needs; the masking answer of rwb-access decides which role sees a personal field in clear; and every read of personal data goes to the PII access log through ACE Common. The catalog gives one entry per product so a developer, an analyst or an auditor finds the owner, the source, the freshness rule, the views behind it and the personal fields without asking. Serves REQ-RDF-010 (access per data product by role) and REQ-RDF-011 (one catalog entry per data product).

**What D-RCV-60 changes.** Not the rationale and not the controls: the controls are still the row, the grant, the masking answer and the log. What changes is that three of those four now live on the other side of a published contract. The role model, the permission matrix and the masking rows are rwb-access's data (Ownership Map v1: `role`, `permission`, `masking_rule` to P4), and P1 holds only the right to read a product for a role. That is the ownership rule of the target: one writer per table, every other reader through the owner's contract, one hop, 2 s timeout, breaker per downstream (DP-01, DP-11; Architecture v5 slides 11, 29 and 41). The second change is that P1 is now the one service that reads the views (DP-05, ADR-010), so the products this story serves are the same products the other 18 services reach through this service's read operations.

**Why the catalog stays here.** The catalog entry joins the dictionary (`sys_objects`, `sys_fields`) to `data_product` and `data_product_access`, and every one of those four tables is P1's. A second service building the entry would be a cross-schema read the boundary rule forbids, so the entry is served here and the retention class, which is P5's, arrives through P5's contract instead of a join (Ownership Map v1: `retention_rule` to P5).

**Measure.** 100 percent of personal field reads logged, measured monthly on the PII access log, and the dictionary conformance count of 122 objects and 1,366 fields matched to the schema each release (FSD P1 A2.15 and A2.16).

### 3. Preconditions

- RWB-P1-E1001-APP is done: `data_product` with the 14 rows DP01 to DP14, `data_product_access`, `sys_objects` with 122 rows, `sys_fields` with 1,366 rows, `sys_field_version` and `data_contract` exist in schema `rwb_source_data`, with the read model `v_data_dictionary` (DP-01, DP-15).
- RWB-P1-E1064-APP is done: the data product and dictionary administration operations of the service are in place, so this story adds the two reads of the legacy story and changes no path of theirs.
- RWB-P1-E1069-APP is done: the 30 `recovery.v_ace_*` views exist, `AceSourceReadRepository` reads them, and the login `rwb_source_data` holds SELECT on each of them and nothing in `public` (DP-02, DP-05; RWB-P1-E1069-DB issues the grants).
- RWB-P1-E1016-DB is delivered or faked: the indexes `ix_data_product_access_product_role`, `ix_sys_fields_object_field` and `ix_sys_objects_product`, the read model `v_data_product_catalog`, the seed of `data_product_access` version "DPA-2026.11" and the schema checks (external dependency X).
- RWB-P4-E1037-CON is published with its guard library and its fake: `POST /api/recovery/access/v1/authorise` answers with the role, the right, the scope values and a marker per field ID, and the `FieldMasker` interface is on the classpath (DP-08).
- RWB-P3-E1043-CON is published with its client library, so the access load arrives as reference data for table code `data_product_access` through the rwb-case reference-data contract with a handler this service implements (DP-07).
- The masking rules from Compliance may be empty (DL26). Until they load, every personal field is masked for every role, and that is the answer rwb-access gives.
- The ACE Common module PII access logging is available (INT-22), and the service identity of rwb-source-data may write to the PII access log.
- The full content of the `data_product_access` seed is not given by the sources: only the rows of section 11 are specified, the rest is Not specified in the source documents (GAP-0482; ASM-0674).

### 4. Flow

1. User: opens a data product panel, which the gateway-bff composite route serves by calling `GET /data-products/{productCode}/records?caseId=` on `/api/recovery/source-data/v1` (DP-19).
2. `DataProductAccessService`: calls `POST /api/recovery/access/v1/authorise` once with the caller identity from the session, the capability area `Case record`, the right `R`, the case reference and the field IDs about to be returned; the answer names the decision, the matrix version and the masking version with a marker per field ID (DP-08, DP-11).
3. `DataProductAccessService`: checks `data_product_access` in `rwb_source_data` for a row in force for one of the answered roles and the product, on the answered business date.
4. `DataProductAccessService`: resolves the case's account keys from its own `case_list_row` and filters them by the answered team and owner scope values; the person keys come from `v_ace_account` to `v_ace_customer` on those account keys. No P3 case table is read and no P3 case contract is called.
5. `DataProductRecordService`: reads the product rows. A Workbench product reads its own tables in `rwb_source_data`; a source product is read from its `recovery.v_ace_*` view by `account_key`, `person_key`, `asset_key`, `payment_code` or `contact_key`, through the view contract of RWB-P1-E1069-APP. The login holds SELECT on the view and nothing on `public`.
6. `DataProductRecordService`: applies the `FieldMasker` answer of rwb-access for every field tagged `is_personal` in `sys_fields`. The identity number is already masked in the view as `id_no_masked` and `id_no_last4`; the phone, email and address are full in `v_ace_contact` and the answer decides whether this role sees them clear.
7. `DataProductAccessService`: writes the read to the PII access log through ACE Common with the user, the product, the case, the field names and the time; no value is logged.
8. `SourceReadController`: returns the rows with the product's freshness stamp, which is RWB-P1-E1015-APP's read and is called inside this service, not over a contract.
9. User with the Platform administration right `R`: calls `GET /admin/data-products?product=DP01` and reads the catalog entry built from `v_data_product_catalog`: owner role, system of record, refresh cycle, retention class through P5's contract, the views and tables behind it, the reconciliations and the fields with their PDPA tags.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No `data_product_access` row for the answered roles and the product | 403; no row read; the refusal is written to the access log | MSG-P4-002 | AC3 |
| X2 | An access load names a role code not in the roles list of rwb-access, an unknown product, or two overlapping rows | Load refused in full; the previous version stays in force | MSG-P1-002 | AC4 |
| X3 | The case is outside the answered scope, so `case_list_row` holds no row for the case in that team or owner scope | 404; no row read; the refusal is logged | MSG-P4-003 | AC5 |
| X4 | No masking rule is in force for a personal field | The `FieldMasker` answer marks the field masked and the field is masked for every role | None | AC6 |
| X5 | The PII access log cannot be written | Read refused with 503; no personal data returned | MSG-GEN-006 | AC7 |
| X6 | An access row has a valid-from date after the business date | The row is not in force; the read is refused until that date | MSG-P4-002 | AC8 |
| X7 | A statement reads a `public.*` table as `rwb_source_data`, or writes a view | The database refuses it; the grant test of RWB-P1-E1069-DB and the view conformance test fail the pipeline if the privilege exists | None (pipeline log) | AC9 |
| X8 | A catalog load marks a `v_ace_*` view as system of record "Workbench" | The load is refused whole; the version in force stays | MSG-P1-003 | AC11 |
| X9 | The authorise call does not answer inside 2 s, or answers 5xx | The read is refused with 503 and no field is returned; no answer is taken from a stale cache | MSG-P4-002 from the guard library; no body from this service | Section 12.2 |
| X10 | The `FieldMasker` interface cannot be reached | Every personal field is returned masked and the read itself succeeds | None | Section 12.2 |

X1 to X8 are the exception paths of RWB-E1-016 carried onto the split, with the case-scope call of X3 replaced by the filter over `case_list_row`; X9 and X10 are the two paths the two consumed contracts of DP-08 add.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published authorise, `FieldMasker` and reference-data contracts and their fakes from Day 1; needs the P1 baseline, the dictionary operations story and the view contract; the DB slice X is tracked, not blocking |
| Negotiable | Which role reads which product, and which field is masked for whom, are data rows or another service's answer; the story fixes the checks and the two operations |
| Valuable | Personal data reaches only the roles that need it, source access is enforced by the grant, every read is logged and every product is findable in one catalog |
| Estimable | Two read operations, one access service, one record service, one catalog service and three consumed contracts |
| Small | Fits one sprint with its tests, once the one-hop contracts are published |
| Testable | Each criterion is one API or database test with synthetic parties and roles |

### 7. Acceptance criteria

```gherkin
Feature: Access control per data product and catalog entries

  Background:
    Given data product access version "DPA-2026.11" is in force from 2026-11-20
    Given case "RW-2026-000102" has borrower person_key "P0000102" whose ACE customer has identity number "1234567890123" and mobile "0812345678"
    Given no masking rule from Compliance is loaded for the v_ace_customer or v_ace_contact fields
    Given the rwb-access FieldMasker contract mock returns no rule in force for the v_ace_customer and v_ace_contact fields

  Scenario: AC1 Role access (legacy RWB-E1-016 AC1)
    Given the rwb-access authorise contract mock returns granted with role RW-AUDIT, the right Case record R and the scope values of that role
    Given user "u-audit-01" holds read-only role RW-AUDIT, which reads DP02
    When the user calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then the mobile number shows as "******5678" and the identity number as "*********0123"
    Then no response field holds the clear identity number
    Then the PII access log holds one entry with user "u-audit-01", product "DP02", case "RW-2026-000102" and the time of the read

  Scenario: AC3 Access denied (legacy RWB-E1-016 AC3)
    Given the rwb-access authorise contract mock returns refused with MSG-P4-002 for product DP06 and role RW-PHONECOL
    Given user "u-phone-01" holds RW-PHONECOL, which has no access row for DP06
    When the user calls GET /data-products/DP06/records?caseId=RW-2026-000102
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system writes the refusal to the access log with user "u-phone-01" and product "DP06"

  Scenario: AC4 An access load with an unknown role is refused (legacy RWB-E1-016 AC4)
    Given the rwb-case reference-data contract mock accepts a validated load for table code data_product_access and calls this service's handler
    Given an access load version "DPA-2026.12" with a row for role "RW-UNKNOWN" and product "DP02"
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and check "unknown role RW-UNKNOWN"
    Then version "DPA-2026.11" stays in force

  Scenario: AC5 A case outside the user's scope (legacy RWB-E1-016 AC5)
    Given the rwb-access authorise contract mock returns granted with role RW-CASEOWN, the right Case record R and the scope Own
    Given the rwb-case case scope is not called; P1 resolves the case links from case_list_row
    Given user "u-owner-07" holds RW-CASEOWN with scope Own and does not own case "RW-2026-000102"
    When the user calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then the system refuses the call with status 404 and MSG-P4-003
    Then the system reads no row

  Scenario: AC6 No masking rule loaded keeps every personal field masked (legacy RWB-E1-016 AC6)
    Given the rwb-access authorise contract mock returns granted with role RW-COMPLY and the right Case record R
    Given user "u-comply-01" holds RW-COMPLY, which reads DP02
    When the user calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then first_name, last_name, cif_no, date_of_birth and the contact value are returned masked

  Scenario: AC7 The PII access log is unavailable (legacy RWB-E1-016 AC7)
    Given the rwb-access authorise contract mock returns granted with role RW-AUDIT and the right Case record R
    Given the PII access log rejects every write
    When user "u-audit-01" calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then the system refuses the call with status 503 and MSG-GEN-006 for system "PII access log"
    Then the system returns no personal field

  Scenario: AC8 An access row not yet in force (legacy RWB-E1-016 AC8)
    Given the rwb-access authorise contract mock returns granted with role RW-PHONECOL and the right Case record R
    Given access version "DPA-2026.12" gives RW-PHONECOL read on DP06 from 2026-12-15
    Given today is 2026-12-14
    When user "u-phone-01" calls GET /data-products/DP06/records?caseId=RW-2026-000102
    Then the system refuses the call with status 403 and MSG-P4-002

  Scenario: AC9 The view grant is the source data access (legacy RWB-E1-016 AC9)
    Given the recovery service identity recovery_svc in SIT
    When the grant test runs
    Then SELECT on public.customer is refused with permission denied
    Then SELECT on recovery.v_ace_customer returns rows
    Then INSERT on recovery.v_ace_customer is refused with permission denied
    Then the test passes for every one of the 30 views

  Scenario: AC10 Thirty view rows in the catalog (legacy RWB-E1-016 AC10)
    Given V0001, V0002 and V0003 are applied
    Given the rwb-document retention contract mock returns the retention class of each of the 14 products
    When a data steward calls GET /admin/data-products
    Then the system returns 14 entries
    Then every one of the 30 v_ace_* views has one catalog row under its data product with system of record "ACE"
    Then v_data_dictionary returns 1,366 fields over 122 objects, of which 304 are view fields with source system "ACE"
    Then no view row names system of record "Workbench"

  Scenario: AC11 A view marked as Workbench is refused (legacy RWB-E1-016 AC11)
    Given the rwb-case reference-data contract mock accepts a validated load for table code sys_objects
    Given a catalog load that sets system of record "Workbench" on v_ace_customer
    When the reference data administrator loads it
    Then the load is refused whole with MSG-P1-003 for v_ace_customer
    Then the version in force stays in use
```

**Target reading.** Every assertion above keeps its legacy wording and its legacy value; what changes is where it runs and which service supplies the answer. The role to permission matrix, the masking answer and the masking rows are rwb-access's, reached once per read through `POST /api/recovery/access/v1/authorise` and the `FieldMasker` interface of RWB-P4-E1037-CON (DP-08), so AC1, AC3, AC6, AC7 and AC8 are executed against the published fake and never against a local copy of the matrix. The case scope of AC5 is no longer a call to rwb-case: P1 resolves the case's account keys from its own `case_list_row` and its person keys from `v_ace_account` to `v_ace_customer`, filters them by the team and owner scope values in the authorise answer, and returns 404 when no row survives, so the legacy `CaseScopeQuery` line becomes the "case scope is not called" Given and no P3 case contract is added. The role named `recovery_svc` in AC9 is the `rwb_source_data` login of the target (DP-02; Architecture v5 slides 11 and 29), and the grants, the three indexes, the catalog read model `v_data_product_catalog` and the `data_product_access` seed that AC9, AC10 and AC11 assert are delivered by RWB-P1-E1016-DB, so those criteria run against the objects that story ships and not against a second copy. The retention class that AC10's catalog entry carries is read through P5's retention contract, never by a join to `retention_rule` (Ownership Map v1), and the two operations are `/data-products/{productCode}/records` and `/admin/data-products` on the base `/api/recovery/source-data/v1` (DP-13). The legacy AC2 catalog-entry scenario is not owned by this story: its assertions are the read model and the seed of RWB-P1-E1016-DB and the catalog read-model tests of RWB-P1-E1064-APP. The seed rows that AC1 and AC3 depend on are only those of section 11: the rest of the `data_product_access` seed is Not specified in the source documents (GAP-0482; ASM-0674), and a missing masking value is Not specified in the source documents (GAP-0481; ASM-0673).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A role reads a data product only through a `data_product_access` row in force for that role and product | REQ-RDF-010; FEAT-RDF-15 |
| BR2 | A personal field is masked unless the masking answer of rwb-access lets the role see it | CTL-11; `masking_rule` owned by P4; DL26 |
| BR3 | With no masking rule in force, every personal field stays masked | DL26 ("Masking rules load with no values") |
| BR4 | Every read of personal data is written to the PII access log through ACE Common; a read that cannot be logged is refused | REQ-ACA-006; CTL-11; INT-22 |
| BR5 | A record outside the caller's scope is refused; the scope values come from the authorise answer and are applied to `case_list_row` | CTL-09; permission matrix |
| BR6 | An access load with an exception is refused in full; the previous version stays in force | Reference data change process, step 3; CTL-08 |
| BR7 | Each data product has one catalog entry with owner, system of record, refresh cycle, retention, the views and tables behind it, the reconciliations and fields with PDPA tags | REQ-RDF-011; `sys_fields.is_personal` |
| BR8 | Source data access is the view grant: the login holds SELECT on `recovery.v_ace_*` and no privilege on `public`, and may not write any view. A direct `public` table read fails at the database, not in code review | D-RCV-35 U4; ADR-010; Data Tier Map section 1 |
| BR9 | There is no tokenization. `v_ace_customer` returns the identity number as `id_no_masked` and `id_no_last4` only; `v_ace_contact` returns the full phone, email and address because notices and calls need them, and the API masks them by role | ADR-010; Data Tier Map section 7; DL26 |
| BR10 | Every one of the 30 `v_ace_*` views belongs to its data product with system of record "ACE"; a view marked "Workbench" is refused | BR-P1-002-2; FSD P1 A2.16 |

**Where each rule lives in the target.** BR1, BR6 and BR10 are this story's: the access rows, the load validation and the catalog guard are code and checks here, with the load arriving through the rwb-case reference-data contract (DP-07; GAP-0483; ASM-0675). BR2, BR3 and BR5 are rwb-access's decisions taken from its own rows; this story calls the answer once and applies it, and holds no masking row and no matrix row (GAP-0481; ASM-0673). BR4 is this story's call into ACE Common PII logging and its 503. BR7 is the catalog service here, with the retention class read through P5's contract. BR8 is enforced by the grants of RWB-P1-E1069-DB and asserted by AC9, and BR9 is the view SQL of RWB-P1-E1069-APP.

### 9. State transitions

None. This story does not change a case status. What moves is the version in force of `data_product_access` when an approved load reaches its valid-from date, and the states of a load.

| From | Event | Condition | To |
|---|---|---|---|
| no version in force | the seed of DPA-2026.11 | The migration of RWB-P1-E1016-DB runs | DPA-2026.11 in force from its valid-from date |
| DPA-2026.11 in force | an approved load DPA-2026.12 | Its valid-from date arrives and every check passes | DPA-2026.12 in force; DPA-2026.11 kept with its valid-to date |
| a load submitted | validation | A role, a product or an overlap check fails | Refused whole; the version in force is unchanged |
| a read | the authorise answer | The answer refuses, or the scope filter finds no row | 403 or 404; nothing read and the refusal logged |
| a personal field | the masking answer | No rule is in force for the role and the field | Masked, for every role |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Prepares the access rows for their products; reads the catalog with the Platform administration right R |
| RW-REFADM, reference data administrator | Submits the access load through the rwb-case reference-data contract with the Reference data right C |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules in rwb-access (DL26); reads the catalog |
| RW-SECADM, security administrator | Owns the role to permission matrix in rwb-access; reads the access log |
| RW-COE, RW-AUDIT, RW-PLATADM | Read the catalog with the Platform administration right R |
| Roles with the Case record right R and an access row, for example RW-CASEOWN, RW-AUDIT | Read a data product for a case in their scope |
| `rwb_source_data`, the service login | Applies an approved access version to `data_product_access` through the handler; reads the views with SELECT only |
| rwb-access (P4) | Owns the authorise answer, the masking answer and the masking rows (DP-08) |
| No approval level of the delegation of authority applies | The story takes no credit decision |

The login is `rwb_source_data` (Architecture v5 slides 11 and 29; DP-02). Its credential and rotation are held by the platform, and no credential appears in this story.

### 11. Data

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
| DF-ACE-078 | v_ace_contact | contact_value | Read; masked by role at the API |
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
| DF-REF-119 | retention_rule (P5) | record_class | Read through P5's retention contract only, never by SQL |
| DF-REF-080 | data_product_access | id | Write |
| DF-REF-081 | data_product_access | product_code | Write |
| DF-REF-082 | data_product_access | role_code | Write |
| DF-REF-083 | data_product_access | can_read | Write |
| DF-REF-084 | data_product_access | access_version | Write |
| DF-REF-085 | data_product_access | valid_from | Write |
| DF-REF-086 | data_product_access | valid_to | Write |
| DF-REF-199 | masking_rule (P4) | role_code | Read through the P4 `FieldMasker` interface only, never by SQL |
| DF-REF-200 | masking_rule (P4) | field_id | Read through the P4 `FieldMasker` interface only, never by SQL |
| DF-REF-201 | masking_rule (P4) | unmasked | Read through the P4 `FieldMasker` interface only, never by SQL |
| DF-RPT-003 | case_list_row | case_id | Read |
| DF-RPT-005 | case_list_row | account_key | Read |
| DF-RPT-010 | case_list_row | owner_user_id | Read |
| DF-RPT-012 | case_list_row | team_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. The personal tags on the view fields are read from `sys_fields.is_personal`. `data_product_access` is the only table this story writes; the four extension tables are created and written by other stories and are read only.

**Which side is this story's.** The 14 `DF-ACE-` rows are read here and defined by the view SQL of RWB-P1-E1069-APP; the 16 `DF-EXT-` rows belong to the extension tables of RWB-P1-E1069-DB; the `DF-REF-` rows on `data_product`, `sys_objects`, `sys_fields` and `data_product_access` are P1's own metadata and access rows, delivered with RWB-P1-E1001-APP and seeded by RWB-P1-E1016-DB; the `DF-RPT-` rows on `case_list_row` are P1's published projection and are how the case scope is resolved without a P3 table. The four `DF-REF-1xx` and `DF-REF-2xx` rows on `retention_rule` and `masking_rule` are named for traceability only: both tables belong to other services (P5 and P4) and are reached through their contracts.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/customers/{id}` | The customer behind `v_ace_customer`, with `id_no_masked` and `id_no_last4` only and never the clear identity number | Any authenticated caller with a Workbench role, the authorise answer and an access row for the customer's product | Idempotent by id and business date |
| GET | `/accounts/{id}` | The account behind `v_ace_account`, with its arrears, balance and classification fields | As above, for the account's product | Idempotent by id and business date |
| GET | `/collateral/{id}` | The collateral behind `v_ace_collateral`, with `v_ace_collateral_detail` once the Section B view is deployed | As above, for the collateral's product | Idempotent by id and business date |
| GET | `/payments?accountId=` | The payments behind `v_ace_payment` for one account key | As above, for the payment's product | Idempotent by accountId and business date |
| GET | `/data-products/{productCode}/records` | API-P1-010: the rows of one data product for a case, read through the views and the extension tables, masked by role, with the product's freshness stamp | Case record right R, plus a `data_product_access` row in force | Not applicable |
| GET | `/admin/data-products` | API-P1-011: the catalog entry or entries, with owner role, system of record, refresh cycle, retention class, the views and tables behind the product, the reconciliations and the fields with PDPA tags | Platform administration right R | Not applicable |

`/data-products/{productCode}/records` takes `caseId` (required), `page` and `size`; `/admin/data-products` takes `product` (optional). Errors: 400 missing `caseId` (MSG-GEN-001); 401 (MSG-P4-001); 403 no right or no access row (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 503 PII log, view or downstream contract down (MSG-GEN-006). The response types are `DataProductRecordPage` (items with record id, entity, a field map with masked values, the freshness stamp, page, size, total) and `DataProductCatalogEntry[]` (productCode, productName, definition, ownerRole, systemOfRecord, refreshCycle, expectedBy, retentionClass, fields, reconciliations, access). The three ACE read operations are the read path of section 12.2 of RWB-P1-E1069-APP served on the same base; the payments read and the freshness operations are served by RWB-P1-E1013-APP on the same base, and this story fixes only their access-control and masking semantics, which are this story's. The exact field-level schema of the two new responses is Not specified in the source documents (GAP-0481; ASM-0673).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Once per read: the caller identity, the capability area, the right, the case reference and the field IDs about to be returned; the answer names the decision, the matrix version, the masking version, the role, the scope values and a marker per field ID | DP-08, DP-11; one hop, 2 s timeout, breaker, no stale cache |
| (interface) | `FieldMasker` of RWB-P4-E1037-CON | P4 rwb-access | `mask(dto, session)` and `isUnmasked(fieldId, session)` applied to every field tagged `is_personal`; a field with no rule is masked | DP-08; library call, no hop, no SQL on `masking_rule` |
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | The approved load for table code `data_product_access`; P1 implements the reference-table handler and never exposes a load endpoint of its own | DP-07; P1 is the handler, not the caller |
| (interface) | P5 retention contract | P5 rwb-document | The retention class of a product for the catalog entry, one call per catalog read | DP-11; one hop, 2 s timeout |

A refusal is passed on with the rwb-access message; a call that does not answer inside 2 s refuses the read with 503 and returns no field (X9). No other service is called at run time: the service reads its own tables and its own views, and no case table of another service is read (DP-01, DP-05).

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP (Architecture v5 slides 15 and 43). This story writes no outbox row.

#### 12.4 Events consumed

None. An access load arrives as reference data through a contract, not as an event, and Architecture v5 slide 15 gives the service no consumed event ("none: Airflow call; fallback polls ACE batch record").

#### 12.5 Workflows and activities

None. Every step of section 4 is synchronous. The task queue `rwb-source-data` in namespace `rwb-recovery` is not used by this story, and the activities `listEligibleAccounts` and `snapshot(page)` and the workflows `AceIngestCheck` and `reconciliation` belong to other P1 stories.

#### 12.6 Schedules

None. No Temporal Schedule and no legacy Quartz job sits in this story; the freshness schedules of the service belong to RWB-P1-E1015-APP and the reconciliation job JOB-04 to RWB-P1-E1011-APP (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Schema | Owner (Ownership Map v1) | This story |
|---|---|---|---|
| `data_product_access` | `rwb_source_data` | P1 | Written: the approved load replaces the version in force; read by the access check |
| `data_product` | `rwb_source_data` | P1 | Read only: the 14 product rows are RWB-P1-E1001-APP's |
| `sys_objects` | `rwb_source_data` | P1 | Read only: the 122 object rows are RWB-P1-E1001-APP's |
| `sys_fields` | `rwb_source_data` | P1 | Read only: the 1,366 field rows are RWB-P1-E1001-APP's |
| `sys_field_version` | `rwb_source_data` | P1 | Read only: the field history is a later P1 story's |
| `data_contract` | `rwb_source_data` | P1 | Read only: the contract rows are RWB-P1-E1064-APP's |
| `case_list_row` | `rwb_source_data` | P1 | Read only: the case keys and the scope columns |
| `v_data_product_catalog` | `rwb_source_data` | P1 | **Not created here**: RWB-P1-E1016-DB creates the read model; this story reads it |
| `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | `rwb_source_data` | P1 | **Not created here**: RWB-P1-E1069-DB creates them; read only |
| `retention_rule` | `rwb_document` | P5 | Not read: the retention class comes through P5's contract |
| `masking_rule`, `role`, `permission` | `rwb_access` | P4 | Not read: reached through the authorise answer and the `FieldMasker` interface |

No table of another service is read and no foreign key crosses a schema (DP-01). The service table `data_product_access` is the only row this story writes.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P4-E1037-CON fake (with the RWB-PLT-E1037-CON guard library) | `POST /api/recovery/access/v1/authorise` | Granted with every field clear; granted with personal fields masked; refused with MSG-P4-002; refused for a case outside scope; a no-rule answer; a timeout |
| RWB-P4-E1037-CON `FieldMasker` fake | The masking interface | No rule in force for a field, one rule unmasking `contact_value` for RW-NOTICE, and an unavailable interface |
| RWB-P3-E1043-CON fake | The reference-data contract | An accepted load for table code `data_product_access` and one for `sys_objects`; a load naming an unknown role; a view marked "Workbench" |
| Delivered-DB fixture | RWB-P1-E1016-DB | A container with the three indexes, `v_data_product_catalog` and the DPA-2026.11 seed, so AC9, AC10 and AC11 run against the delivered objects |
| P5 retention fake | P5 rwb-document | The retention class of each of the 14 products |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 6 operations on `/api/recovery/source-data/v1` | 2 operations (`POST /api/recovery/access/v1/authorise`, the P5 retention read) and 1 handler (`.../case/v1/admin/reference-loads`) | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11) |
| Kafka | None | None | The topic `rwb.source-data.events.v1` belongs to RWB-P1-E1013-APP |
| Temporal | None | None | No workflow, activity or Schedule |
| File | None | None | No file interface in this story |
| SQL view | None created | The 30 `recovery.v_ace_*` views, through RWB-P1-E1069-APP's read path | SELECT only, 5 s statement timeout, one login `rwb_source_data` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, modules `access`, `catalog` and `read`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-08 is this story's own pattern and the largest change of the split: the guard becomes a call and the masking rows leave the service. DP-01, DP-02 and DP-05 are used, not delivered: the schema, the login and the views arrive with RWB-P1-E1001-APP, RWB-P1-E1069-APP and RWB-P1-E1069-DB. DP-07 is used for the access load path (GAP-0483; ASM-0675). DP-19 applies to the composite route that serves the product panels, which this story serves and does not build.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DataProductController` | Controller | `GET /data-products/{productCode}/records` and `GET /admin/data-products`; RFC 9457 problem details |
| `DataProductAccessService` | Service | Authorise hop, access-row check, scope filter over `case_list_row`, PII log write, 503 on a failed log |
| `DataProductRecordService` | Service | Reads the rows of the product's own tables or of its views, takes the masking answer per field and returns the row |
| `DataProductCatalogService` | Service | Builds the entries from `v_data_product_catalog` and the P5 retention answer |
| `DataProductAccessRepository` | Repository | Reads and writes `data_product_access`; no other schema is named |
| `DataProductAccessHandler` | Reference-table handler | Implements the rwb-case reference-data contract for table code `data_product_access`: known product, known role, no overlap, refuse whole |
| `AccessGuardClient` | Client | The authorise operation and the `FieldMasker` interface through the guard library; one hop, 2 s, breaker |
| `PiiAccessLogWriter` | Client | ACE Common PII logging: user, product, case, field names and time, never a value |
| `RetentionClient` | Client | P5's retention read for the catalog entry |
| `DataProductAccess` | Entity | One row per product, role and version |

**Database.** This story creates no table, no index and no view. It writes rows of `data_product_access` through the handler, and reads `data_product`, `sys_objects`, `sys_fields`, `sys_field_version`, `data_contract`, `case_list_row`, `v_data_product_catalog` and the four extension tables. The three indexes, the read model `v_data_product_catalog` and the DPA-2026.11 seed are RWB-P1-E1016-DB's, and that story creates no table RWB-P1-E1001-APP already creates (GAP-0484; ASM-0676).

**Configuration and reference data**

- Access version `DPA-2026.11` is prepared by the data steward and loaded by the reference data administrator through the rwb-case reference-data contract; the seed of the version is RWB-P1-E1016-DB's and covers only the rows of section 11 (GAP-0482; ASM-0674).
- Masking rules are loaded by Compliance into rwb-access under DL26 and are never copied here.
- The authorise contract, its 2 s budget and the masking answer are configuration of the guard library, not constants in this service (DP-08).
- The feature flag `rwb.source-data.product-access` gates the two operations until the seed and the read model are in place.

**Build steps**

1. `AccessGuardClient` and `PiiAccessLogWriter` against the published fakes, with the timeout and no-stale-cache rules (12.2, X9, X10).
2. `DataProductAccessService` with the order authorise, access row, scope filter (AC1, AC3, AC5, AC6, AC8).
3. `DataProductRecordService` reading own tables and views, applying the masking answer and masking every personal field when no rule exists (AC1, AC6).
4. `DataProductAccessHandler` with the whole-load validation: known product, known role, no overlap, refuse with MSG-P1-002 (AC4).
5. `DataProductCatalogService` and `GET /admin/data-products` over the delivered read model, with the P5 retention answer and the "Workbench" refusal (AC10, AC11).
6. The two operations on the contract, with the error envelope and the 403, 404 and 503 mappings (12.1).
7. Tests for AC1 and AC3 to AC11 against the delivered-DB fixture and the three fakes.

**Done when.** The tests in section 16 pass, the catalog returns 14 complete entries in SIT from `v_data_product_catalog`, every read of a personal field appears once in the PII access log, and no query in the service names `masking_rule`, `role`, `permission` or `retention_rule`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | No right, or no access row for the product | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P1-002 | Access load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-003 | A catalog load marks a view with a system of record other than ACE | {product} must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner. |
| MSG-GEN-001 | caseId missing | Enter {field}. |
| MSG-GEN-006 | PII access log unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-001 | No valid session | Your session has ended. Sign in again. |

Thai text for each message follows decision DL10. MSG-P4-001, MSG-P4-002, MSG-P4-003 and MSG-P7-003 are raised by the rwb-access guard library; this service passes them on unchanged and adds no message of its own.

### 15. Screens and states

No screen in this story. The case record view SCR-03 (Read only) shows the product data the role may read, with personal fields masked, and reaches this service through the gateway-bff composite route (DP-19). Catalog entries are read through `GET /admin/data-products` and rendered by the administration screen of RWB-P1-E1064-APP. SCR-47 Personal data shows masking rules from Epic 8 and reads them from rwb-access, not from this service. States on the screens: loading, empty (no access row, so the panel is not shown), refused (403 or 404 problem body) and ready.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-016-01 | AC1, BR1, BR2, BR4, BR9 | End to end | RW-AUDIT; case RW-2026-000102; synthetic customer P0000102 with identity 1234567890123 and mobile 0812345678 |
| TC-E1-016-02 | BR7; legacy AC2, whose proof sits with RWB-P1-E1016-DB's `v_data_product_catalog` and RWB-P1-E1064-APP | Component | DP01 entry; six views and account_ext; DF-ACE-018; access rows |
| TC-E1-016-03 | AC3, BR1 | End to end | RW-PHONECOL; product DP06 |
| TC-E1-016-04 | AC4, BR6 | Component | Access load with role RW-UNKNOWN |
| TC-E1-016-05 | AC5, BR5 | End to end | RW-CASEOWN, case not owned; `case_list_row` without a row in that scope |
| TC-E1-016-06 | AC6, BR3 | End to end | RW-COMPLY; no masking rule in force |
| TC-E1-016-07 | AC7, BR4 | End to end | PII access log stub rejecting writes |
| TC-E1-016-08 | AC8, BR1 | End to end | Access row valid from 2026-12-15; test clock 2026-12-14 |
| TC-E1-016-09 | Access; refusal of `GET /admin/data-products` for RW-TRIBE with MSG-P4-002 | Component | RW-TRIBE calls the catalog read; refused |
| TC-E1-016-10 | AC9, BR8 | Component | `rwb_source_data`; SELECT public.customer; SELECT and INSERT on v_ace_customer; all 30 views |
| TC-E1-016-11 | AC10, BR7, BR10 | End to end | 30 views; 122 objects and 1,366 fields |
| TC-E1-016-12 | AC11, BR10 | Component | Catalog load setting v_ace_customer to Workbench |

The legacy test case IDs, Covers and Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. TC-E1-016-02 proves the legacy catalog-entry scenario against the read model delivered by RWB-P1-E1016-DB, and TC-E1-016-09 names the same refusal as the legacy access row. TC-E1-016-10 runs against the grants of RWB-P1-E1069-DB. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: access by role and masking by role are data rows, in `data_product_access` here and in rwb-access's own tables there; the code holds no role, product or masking list.
- No personal data in logs, tests, events, workflow inputs or prompts: the PII access log carries field names, not values; test customers are synthetic; no event carries a personal field.
- No read of another module's tables: the case scope is `case_list_row` and the views, the masking answer is the P4 `FieldMasker` interface, the rights are the authorise answer; `masking_rule`, `role`, `permission` and `retention_rule` are never named in a query (DP-01).
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: this service reads its own views and publishes the read path; every other service calls this contract (DP-05, ADR-010).
- A read that cannot be logged returns no personal data.
- No token, detokenization call or clear identity number exists in any response.
- One hop and 2 s on every consumed contract; a slow answer refuses the read and returns no field (DP-11).
- The seed, the indexes and the read model are one story's delivery and one story's test: this story reads them and never re-creates them (GAP-0484; ASM-0676).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role through the views; personal data masked by role under PDPA | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | All recovery processes | CTL-09, CTL-11; DL26; BR-P1-001-4, BR-P1-001-6; BR-P1-015-2, BR-P1-015-3 | TC-E1-016-01, TC-E1-016-03 to TC-E1-016-10 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record, refresh and retention | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-16 | All recovery processes | CTL-08; BR-P1-002-2; BR-P1-016-2 | TC-E1-016-02, TC-E1-016-11, TC-E1-016-12 |
| REQ-ACA-006 | Every read of personal data is written to the PII access log, and a read that cannot be logged is refused | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | All recovery processes | CTL-11; BR-P1-015-4 | TC-E1-016-01, TC-E1-016-07 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1001-APP | App development | H build dependency: the `rwb_source_data` baseline, `data_product`, `sys_objects`, `sys_fields`, `data_product_access`, `data_contract` and `v_data_dictionary` |
| RWB-P1-E1064-APP | App development | H build dependency: the data product, dictionary and contract administration of the service, on the same base |
| RWB-P1-E1069-APP | App development | H build dependency: the 30 `recovery.v_ace_*` views and the read path this story's records come from |
| RWB-P1-E1016-DB | ACE DB | X external dependency: the three indexes, `v_data_product_catalog`, the DPA-2026.11 seed and the schema checks |
| RWB-P1-E1016-CON | Contract | Sibling of the same legacy key: the six read operations, the two interfaces, the error envelope and the read schemas |
| RWB-P4-E1037-CON | Contract | C: the authorise operation and the `FieldMasker` interface (DP-08) |
| RWB-P3-E1043-CON | Contract | C: the reference-data contract that carries the access load (DP-07) |
| RWB-P1-E1015-APP | App development | Sibling: the freshness stamp the record page carries |
| RWB-P1-E1069-DB | ACE DB | Delivers the grants and the four extension tables this story reads and AC9 asserts |

### 19. Out of scope

- The role to permission matrix, the masking rows and the masking answer: rwb-access (P4), RWB-P4-E1037-CON and its app story; this story calls the answer and holds no masking row (GAP-0481).
- The three indexes, the read model `v_data_product_catalog`, the `data_product_access` seed and the schema checks: RWB-P1-E1016-DB (GAP-0484).
- The tables themselves, the dictionary rows and the 14 product rows: RWB-P1-E1001-APP.
- The view SQL, the grants, the view owner and boundary rule BND-6: RWB-P1-E1069-APP and RWB-P1-E1069-DB; the grant matrix across the 19 logins is RWB-ITG-E1069-ITG.
- The dictionary search and the field-level administration: RWB-P1-E1064-APP.
- The freshness stamp and the business-day operations: RWB-P1-E1015-APP and RWB-P1-E1013-APP.
- The access log search and break-glass: the rwb-access story of the legacy key.
- The personal data screen SCR-47: Epic 8.
- The rest of the `data_product_access` seed, beyond the rows the sources give: a later approved load (GAP-0482; ASM-0674).
- The gateway-bff composite route and the rendering of a masked field: the platform edge story and the screen owners (DP-19).
