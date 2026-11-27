# RWB-P1-E1016-APP Access control per data product and catalog entries

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- RD-P1-021 narrows the products served; RD-P1-024 removes P1 case-list storage and keeps case scope behind the rwb-case contract (review #5).
- RD-P1-026 adds RW-COMPLY/DP02 to the access seed used by AC6 (review #1).
- RD-P1-023 fixes `caseId` to UUID and RD-P1-025 fixes dictionary counts; pending sources are tracked below (review #11, #15).
- The authorise call now sends what RWB-P4-E1016-APP v3 needs (access resolution, case attributes, `Idempotency-Key`) and reads only `allowed`, the two version labels and the markers; the case facts come from three published rwb-case reads (review #2, #9, #13, #18; GAP-3322).
- DP02 contact rows carry no contact value, address or name (rwb-source-data.yaml 5.1.0); the legacy mobile-number assertions are Pending under GAP-3347 (review #4, #14).
- RD-P1-004, RD-P1-020 and RD-P1-045: failure bodies, access-version load rules, paging, flag-off and new criteria AC26 to AC34 (review #6, #7, #16, #17, #22, #23, #25).
- Finishing pass (RD-P1-060, RD-P1-063, RD-P1-072; requests F09-affected-0164, S7-stories-0358, W3-messages-0040; test case backfill): the contact value, name and address read is `GET /customers/{personKey}`, the interim authorise rules and the no-decision-record rule for reads are stated, MSG-GEN-006 and MSG-P4-001 follow Error and Message Standard v6, and Test Cases v9 IDs are cited.



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
| Size | Not specified in the source documents (DOR-RWB-P1-E1016-APP-16) |
| Patterns applied | DP01, DP02, DP05, DP07, DP08, DP11, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1069-APP |
| Contract dependencies | RWB-P3-E1043-CON; RWB-P4-E1037-CON; RWB-P5-AD021-CON; rwb-case.yaml 5.1.0 reads `GET /cases/{caseId}`, `/cases/{caseId}/accounts`, `/cases/{caseId}/parties`; rwb-access.yaml 5.1.0 `GET /admin/roles`; `POST /authorise` as RWB-P4-E1016-APP v3 states it (not yet in rwb-access.yaml, GAP-0983) |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1016-DB |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-004, FR-P1-006, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-026, FR-P1-027, FR-P1-030; NFR-P1-001) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-020, RD-P1-021, RD-P1-023, RD-P1-024, RD-P1-025, RD-P1-026, RD-P1-041, RD-P1-043, RD-P1-045, RD-P1-060, RD-P1-063, RD-P1-072 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-016 for rwb-source-data. The access rows, the product records read and the catalog entry stay with the service that owns `data_product_access`, `sys_objects`, `sys_fields` and `data_product` in schema `rwb_source_data` (DP-01, DP-02; Architecture v5 slides 29 and 41); the role to permission matrix, the masking answer and the masking rows move to rwb-access and are consumed through its contracts (DP-08; Ownership Map v1, `masking_rule` to P4); the indexes, the catalog read model and the access seed move to the DB slice RWB-P1-E1016-DB. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1016-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: operations, access controls and data scope aligned to final rulings. Tool: T3 Code.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **read access to each data product granted by role, source data reached only through the ACE view grant, personal fields masked by role from `v_ace_customer` and `v_ace_contact`, every read logged, and a catalog entry per product that names its owner, system of record, freshness, views and tables and fields**, so that **personal data is read only by the roles that need it and every product is findable**.

The legacy story built the behaviour inside one monolith process and one `recovery` schema. This slice keeps the control intent while applying the final P1 decisions:

- `data_product_access` remains P1 data. P1 receives approved reference versions through the P3 reference-data pipeline and applies each version atomically and idempotently; it has no load-state table (RD-P1-020).
- P1 reads records only for DP01, DP02, DP04, DP05, DP06, DP07, DP11 and DP13, from ACE views and P1-owned tables. Other product codes return 400 E400 naming the owning service; the pending message and DP14 status are listed in section 20 (RD-P1-021).
- `caseId` is the UUID `rwb_case.recovery_case.id`. The display case number is not a lookup key. P1 reads the case's attributes, account keys and person keys from three published rwb-case operations and reads no P3 table (RD-P1-023, RD-P1-024).
- The authorise answer replaces the in-process guard. P1 calls `POST /api/recovery/access/v1/authorise` of rwb-access (P4) once per records read, with a new `Idempotency-Key`, one hop, 2 s timeout, no automatic retry and no stale cached answer (DP-08, DP-11; RD-P1-001). The request carries the access resolution P1 resolved from its own rows and the case attributes; rwb-access applies the right, the scope, the data-product condition and the masking policy.
- Bases and names: REST base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-02, DP-13, DP-14; Architecture v5 slide 41).
- The indexes, `v_data_product_catalog`, seven-row access seed and schema checks are delivered by RWB-P1-E1016-DB. The 30 `recovery.v_ace_*` views and grants are delivered by RWB-P1-E1069-APP and RWB-P1-E1069-DB (DP-05).

### 2. Business rationale

Audit findings record staff sending debtor data outside the bank and users holding access they did not need (CTL-11, CTL-09). Under D-RCV-35 there is no load and no tokenization: source data is reached only through the `recovery.v_ace_*` views, so access to a data product is the role's access row plus the database grant on the view, and the identity number is masked inside `v_ace_customer` itself. Access rows held as data limit each role to the products its work needs; the masking answer of rwb-access decides which role sees a personal field in clear; and every read of personal data goes to the PII access log through ACE Common. The catalog gives one entry per product so a developer, an analyst or an auditor finds the owner, the source, the freshness rule, the views behind it and the personal fields without asking. Serves REQ-RDF-010 (access per data product by role) and REQ-RDF-011 (one catalog entry per data product).

**What D-RCV-60 changes.** Not the rationale and not the controls: the controls are still the row, the grant, the masking answer and the log. What changes is that three of those four now live on the other side of a published contract. The role model, the permission matrix and the masking rows are rwb-access's data (Ownership Map v1: `role`, `permission`, `masking_rule` to P4), and P1 holds only the right to read a product for a role. That is the ownership rule of the target: one writer per table, every other reader through the owner's contract, one hop, 2 s timeout, breaker per downstream (DP-01, DP-11; Architecture v5 slides 11, 29 and 41). The second change is that P1 is now the one service that reads the views (DP-05, ADR-010), so the products this story serves are the same products the other 18 services reach through this service's read operations.

**Why the catalog stays here.** The catalog entry joins the dictionary (`sys_objects`, `sys_fields`) to `data_product` and `data_product_access`, and every one of those four tables is P1's. A second service building the entry would be a cross-schema read the boundary rule forbids, so the entry is served here and the retention class, which is P5's, arrives through P5's contract instead of a join (Ownership Map v1: `retention_rule` to P5).

**Measure.** 100 percent of personal field reads are logged, measured monthly on the PII access log. Each release includes every E1001 baseline object and field ID and at least 123 objects and 1,379 fields, including the 304 ACE view fields (FSD P1 A2.15 and A2.16; RD-P1-025).

### 3. Preconditions

- RWB-P1-E1001-APP is applied: the 14 `data_product` rows, 123 baseline `sys_objects` rows, 1,379 baseline `sys_fields` rows, `data_product_access`, `sys_field_version` and `data_contract` exist in `rwb_source_data`.
- RWB-P1-E1064-APP provides the data-product and dictionary administration operations on the service base.
- RWB-P1-E1069-APP and RWB-P1-E1069-DB provide the `recovery.v_ace_*` views and grants used by P1. Only this service reads those views; all other services use this service contract (RD-P1-021).
- RWB-P1-E1016-DB provides `v_data_product_catalog`, the three indexes and the seven DPA-2026.11 access rows, including RW-COMPLY on DP02 (RD-P1-026).
- RWB-P4-E1037-CON provides the guard library, `AccessGuard` and `FieldMasker`; RWB-P4-E1016-APP answers the data-product half of `POST /authorise`. Pending: the property names of the authorise request (including the case attributes and the access resolution) and of the answer, the marker vocabulary and the publication of the path in rwb-access.yaml, owner rwb-access solution architect, GAP-0983. Interim build (RD-P1-063): each call carries a uuid `Idempotency-Key`, tests run against the P4 fake and assert allow or deny and the Problem `messageCode` (401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003), never a role or scope value the provider has not published.
- RWB-P3-E1043-CON carries approved reference loads for `data_product_access`; this service implements its whole-version apply handler.
- rwb-case.yaml 5.1.0 publishes `GET /cases/{caseId}` (`ownerUserId`, `teamCode`, `regionCode`), `GET /cases/{caseId}/accounts` (`accountKey`) and `GET /cases/{caseId}/parties` (`personKey`), each with Case record R. P1 forwards the user JWT with its workload identity (Architecture v5 slide 11).
- A missing masking rule keeps `is_personal=true` fields masked. `cif_no` is tagged `is_personal=false`; Pending: whether that field is masked by another rule, owner Compliance, tracked as GAP-3439.
- ACE Common PII access logging is available; the log stores user, product, case UUID, field names and time, never a value.
- P1 serves records only for DP01, DP02, DP04, DP05, DP06, DP07, DP11 and DP13. It returns 400 E400 for DP03, DP08, DP09, DP10, DP12 and DP14 with the owning service in problem detail. Pending: unsupported-product message ID, owner product owner and Error Standard owner, tracked as GAP-3272 (RD-P1-021). Pending: DP14 records availability, owner rwb-ace-data service owner, tracked as GAP-3281 (RD-P1-021 / RD-P1-041).
- The records path reads only these objects, per product, filtered by the case's `account_key` and `person_key` values (RD-P1-021; rwb-source-data.yaml 5.1.0):

| Product | Objects P1 reads |
|---|---|
| DP01 | `v_ace_account`, `v_ace_payment`, `v_ace_bucket_log`, `account_ext` |
| DP02 | `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation`, `v_ace_aa_relation`, `v_ace_party_product`, `party_ext`, `contact_point_ext` |
| DP04 | `v_ace_plan`, `v_ace_credit_decision`, `dp_treatment`, `dp_guarantee_claim` |
| DP05 | `v_ace_efs_action`, `v_ace_efs_action_code`, `v_ace_efs_assignment`, `interaction` |
| DP06 | `v_ace_collateral`, `v_ace_asset`, `v_ace_valuation`, `v_ace_collateral_detail`, `v_ace_npa_asset`, `v_ace_npa_sale`, `valuation_ext` |
| DP07 | `v_ace_lawsuit`, `v_ace_hearing`, `v_ace_pod` |
| DP11 | `v_ace_score` |
| DP13 | `v_ace_write_off` |

- Objects the dictionary lists under these products but another service owns (for example `treatment`, `listing`, `legal_action`, `proceeds`) are never read. Pending: the field list of each product, and how an object with neither an `account_key` nor a `person_key` column is restricted to the case, owner data architect, GAP-3445.
- Not served, with the owner named in the problem `detail`: DP03 rwb-case, DP08 rwb-partner, DP09 rwb-debtsale, DP10 rwb-document, DP12 rwb-decision, DP14 the DP14 owners.
- DP02 contact rows have the fields `contactKey`, `contactType`, `consentStatus` and `verifiedAt` only: no contact value, address, name or identity number (rwb-source-data.yaml 5.1.0). RWB-P1-E2021-APP builds those rows; this story never selects `contact_value`. The clear name, postal address and contact value are read only through `GET /customers/{personKey}` (`getCustomer`, published in rwb-source-data.yaml 5.1.0 and built by RWB-P1-E1069-APP), which answers `contactValue` clear only when `FieldMasker` says the session may see it (RD-P1-060). Pending: the masking rule rows for the rwb-comms notice and rwb-integration outbound-file identities, owner data protection officer with the rwb-access owner, GAP-3283.
- Section B views are built and tested in DEV and the pipeline on the synthetic fixture; in SIT and later the flag stays off until RWB-ACE-001 lands (DL43, working answer A; RD-P1-043).

### 4. Flow

1. The gateway-bff calls `GET /data-products/{productCode}/records` with a case UUID, `page` and `size`. The service validates the request (X11, X12, X14) before any downstream call.
2. `DataProductAccessService` takes the caller's role codes from the session and reads the `data_product_access` rows in force for those roles and the product on the business date in Asia/Bangkok. A row is in force when `valid_from <= business_date` and (`valid_to` is null or `business_date <= valid_to`). The result, with or without a row, is the access resolution: access version, product code, role codes and valid-from date. Pending: which business date applies (RWB-P4-E1016-APP uses the case's business date), owner solution architect, GAP-3443.
3. The service reads the case once from each published rwb-case operation: `GET /cases/{caseId}` for the case attributes of the scope test, `/accounts` for the account keys and `/parties` for the person keys.
4. The service calls `POST /api/recovery/access/v1/authorise` once, with a new uuid `Idempotency-Key`, capability area `CASE_RECORD`, right `R`, `productCode`, `caseId`, the field IDs about to be returned, the case attributes and the access resolution. The answer holds `allowed`, `matrixVersion`, `maskingVersion` and one marker (`masked` or `clear`) per field ID. It holds no role, scope or business date, and P1 expects none.
5. 403 MSG-P4-002 and 404 MSG-P4-003 from rwb-access are passed on; `allowed` false is answered 403 MSG-P4-002. P1 reads no source row unless `allowed` is true and the resolution holds a row in force.
6. `DataProductRecordService` reads the objects of the product (section 3), filtered by the case's account and person keys.
7. `DataProductRecordService` applies the markers through `FieldMasker`: a field tagged `is_personal=true` is clear only where its marker is `clear`; a missing marker, no masking rule or a `FieldMasker` error leaves it masked. The marker is the only masking source. `cif_no` masking remains Pending under GAP-3439.
8. For every read that returns a field tagged `is_personal`, masked or clear, the service writes one PII access log entry with the user, product, case UUID, field names and time. A failed write returns 503 MSG-GEN-006 with no data.
9. `SourceReadController` returns `DataProductRecordPage`: `items` (each `recordId`, `entity`, `fields` as `FieldValue[]`), `freshness`, `page`, `size` and `total`. A case with no row of the product answers 200 with empty `items` and `total` 0. Pending: sort order and the unit counted by `total` across several objects, owner API specification owner, GAP-3444.
10. `GET /admin/data-products`: the guard library of RWB-PLT-E1037-CON checks Platform administration R (there is no case, so no data-product authorise request is made); the catalog is built from P1 metadata and adds the P5 retention class through the P5 contract.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | rwb-access answers `allowed` false (no access row in force for the caller's roles and the product), or refuses the right with 403 | 403; no source row read; one refusal log entry | MSG-P4-002 | AC3, AC8, AC27 |
| X2 | A reference load contains an unknown role, product or overlapping access rows | Whole load is refused; prior version remains in force | MSG-P1-002 | AC4, AC18 |
| X3 | rwb-access answers 404 for a case outside scope, or rwb-case answers 404 | 404; no source row read; one refusal log entry | MSG-P4-003 | AC5, AC28 |
| X4 | No masking rule is in force for an `is_personal=true` field | The authorise marker is `masked` and the field stays masked | None | AC6 |
| X5 | PII access log cannot be written | 503; no personal data is returned | MSG-GEN-006 | AC7 |
| X6 | An access row starts after the business date | Row is not in force; read is refused | MSG-P4-002 | AC8 |
| X7 | The service login requests a table in `public` or writes an ACE view | Database privilege check refuses it; deployment test fails if the privilege exists | Pipeline finding; no message ID | AC9 |
| X8 | A catalog load sets an ACE view's system of record to Workbench | Whole load is refused; current version remains in force | MSG-P1-003 | AC11 |
| X9 | Authorise does not answer within 2 s, answers 5xx or answers a malformed body | 503; no data returned; no retry and no stale answer | MSG-GEN-006 | AC12 |
| X10 | `FieldMasker` throws its unavailable error | Every field tagged `is_personal` stays masked, whatever the marker; the read succeeds and is logged | None | AC13 |
| X11 | A product code is not served by P1 | 400 E400 with the owning service in detail; no source row is read | Message ID Pending, GAP-3272 | AC22 |
| X12 | `caseId` is missing or is not a UUID | 400 before any downstream call or row query | MSG-GEN-001 | AC17 |
| X13 | An rwb-case read does not answer within 2 s or answers 5xx | 503; no authorise call and no source row read | MSG-GEN-006 | AC29 |
| X14 | `productCode` or `?product=` is not in LOV-DATA-PRODUCT; `page` below 0 or `size` outside 1 to 200 | 400 for the unknown code; 422 for the range; nothing read | MSG-GEN-007; MSG-GEN-002 | AC30 |
| X15 | The retention read or an ACE view query fails or times out | 503; no partial page or catalog | MSG-GEN-006 | AC21 |
| X16 | A load is back-dated, or the role list cannot be read during its check | Nothing is written; the version in force stays | MSG-P1-002 for the back-dated version; MSG-GEN-006 where the role list is down | AC31, AC32 |
| X17 | Feature flag `rwb.source-data.product-access` is off | The two operations answer 404 | Pending: message ID of the flag-off 404, GAP-3506 | AC33 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published authorise, `FieldMasker` and reference-data contracts and their fakes from Day 1; needs the P1 baseline, the dictionary operations story and the view contract; the DB slice X is tracked, not blocking |
| Negotiable | Which role reads which product, and which field is masked for whom, are data rows or another service's answer; the story fixes the checks and the two operations |
| Valuable | Personal data reaches only the roles that need it, source access is enforced by the grant, every read is logged and every product is findable in one catalog |
| Estimable | Two read operations, one access service, one record service, one catalog service, one apply handler and the consumed contracts of section 12.2 |
| Small | Fits one sprint with its tests, once the one-hop contracts are published |
| Testable | Each criterion is one API or database test with synthetic parties and roles |

### 7. Acceptance criteria

```gherkin
Feature: Access control per data product and catalog entries

  Background:
    Given access version DPA-2026.11 is in force from 2026-11-20 and contains seven sourced rows
    Given the customer fixture uses identity number 1234567890123 and mobile 0812345678
    Given no masking rule from Compliance is loaded for the v_ace_customer or v_ace_contact fields
    Given the authorise fake answers every marker masked unless a scenario says otherwise
    Given the synthetic case UUID is 00000000-0000-4000-8000-000000000102
    Given the rwb-case fake answers that case with its owner, team, region, account keys and the borrower person key P0000102

  Scenario: AC1 A role with an access row reads DP02 with personal values masked
    Given RW-AUDIT has an active DPA-2026.11 access row for DP02
    Given the authorise fake answers allowed true with every marker masked
    When u-audit-01 calls GET /data-products/DP02/records with the case UUID
    Then the answer is 200 and the identity value is *********0123 from id_no_masked with masked true
    Then no field holds 1234567890123 or 0812345678, and a DP02 contact row holds only contactKey, contactType, consentStatus and verifiedAt
    Then one PII log entry holds user u-audit-01, product DP02, the case UUID, the field names and the time, and no value
    Then the legacy mobile-number assertion is not part of this read: it belongs to `GET /customers/{personKey}`, built by RWB-P1-E1069-APP (RD-P1-060)

  Scenario: AC3 A role without a product access row is refused
    Given RW-PHONECOL has no DPA-2026.11 access row for DP06
    Given the authorise fake answers allowed false to a resolution with no row
    When u-phone-01 calls GET /data-products/DP06/records with the case UUID
    Then the response is 403 MSG-P4-002 and no view or table of DP06 is queried
    Then one refusal log entry holds the user, product DP06, the case UUID and the time

  Scenario: AC4 A reference load with an unknown role is refused in full
    Given the role-list contract returns no RW-UNKNOWN role
    Given DPA-2026.12 contains a DP02 row for RW-UNKNOWN
    When the P1 reference-data handler validates DPA-2026.12
    Then the whole load is refused with MSG-P1-002 and check text naming RW-UNKNOWN
    Then DPA-2026.11 remains in force and no DPA-2026.12 row is applied

  Scenario: AC5 A case outside the caller scope is refused
    Given u-owner-07 holds RW-CASEOWN and case 00000000-0000-4000-8000-000000000456 has another owner
    Given the authorise fake answers 404 MSG-P4-003 for those case attributes
    When u-owner-07 calls GET /data-products/DP02/records with that case UUID
    Then the response is 404 MSG-P4-003 and no view or table of DP02 is queried
    Then one refusal log entry holds the user, product DP02, the case UUID and the time

  Scenario: AC6 No masking rule keeps tagged personal fields masked for RW-COMPLY
    Given user u-comply-01 holds RW-COMPLY, which has an active DPA-2026.11 access row for DP02
    Given the authorise fake answers allowed true with every marker masked
    When the user calls GET /data-products/DP02/records with the case UUID
    Then first_name, last_name and date_of_birth are returned masked
    Then every other returned field tagged is_personal, including id_no_masked and id_no_last4, has masked true
    Then no contact value is returned; contact values are read only through `GET /customers/{personKey}` (RD-P1-060)
    Then no masking rule is read from a P4 table
    Then whether cif_no is masked remains Pending, owner Compliance, GAP-3439

  Scenario: AC7 A PII access-log failure returns no personal data
    Given the authorise fake answers allowed true for RW-AUDIT on DP02
    Given the ACE Common PII log rejects a write
    When the user calls GET /data-products/DP02/records with the case UUID
    Then the response is 503 MSG-GEN-006
    Then no personal field is returned

  Scenario: AC8 An access row starting on a later date is not in force
    Given DPA-2026.12 grants RW-PHONECOL DP06 from 2026-12-15
    Given the business date in Asia/Bangkok is 2026-12-14
    When u-phone-01 calls GET /data-products/DP06/records with the case UUID
    Then the access resolution sent to authorise holds no DP06 row in force
    Then the response is 403 MSG-P4-002 and no DP06 object is queried
    When the business date is 2026-12-15 and the same call is made
    Then the resolution holds DPA-2026.12, DP06, RW-PHONECOL and valid_from 2026-12-15, and the response is 200

  Scenario: AC9 The service login reads ACE data only through the granted views
    Given the database login rwb_source_data in SIT
    When the database privilege check runs
    Then SELECT on public.customer is refused
    Then SELECT is allowed on each of the 30 recovery.v_ace_* views
    Then INSERT, UPDATE and DELETE are refused on every recovery.v_ace_* view

  Scenario: AC10 The catalog exposes the P1 dictionary baseline and view rows
    Given the E1001 baseline and E1016-DB read model are applied
    When a data steward calls GET /admin/data-products
    Then the response contains the 14 active data products
    Then the dictionary contains every E1001 baseline object and field ID, at least 123 objects and 1,379 fields, including 304 ACE view fields
    Then each of the 30 ACE views is listed under its mapped product with system of record ACE
    Then no view is listed with system of record Workbench

  Scenario: AC11 A catalog load cannot mark an ACE view as Workbench
    Given the P1 reference-data handler receives a sys_objects load setting v_ace_customer to Workbench
    When the handler validates the load
    Then the whole load is refused with MSG-P1-003 and text DP02 must have exactly one system of record and one named owner.
    Then the prior version remains in force and no sys_objects row changes

  Scenario: AC12 An authorise failure returns no data
    Given authorise does not answer within 2 seconds
    When a user calls GET /data-products/DP02/records with the case UUID
    Then the response is 503 application/problem+json with messageCode MSG-GEN-006 naming rwb-access in detail
    Then no source row is read, no field is returned and the call is not retried
    When authorise answers 503
    Then the response is the same

  Scenario: AC13 FieldMasker unavailable keeps personal fields masked
    Given the authorise fake answers allowed true with date_of_birth marked clear
    Given FieldMasker throws its documented unavailable error
    When the user calls GET /data-products/DP02/records with the case UUID
    Then the response is 200 and every field tagged is_personal, date_of_birth included, has masked true
    Then one PII log entry is written

  Scenario: AC14 A request without a Workbench role receives the session error
    Given the caller has no valid Workbench role
    When the caller requests GET /data-products/DP02/records or GET /admin/data-products
    Then the response is 401 MSG-P4-001 "Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one."
    Then the Problem response contains no personal data or catalog items

  Scenario: AC15 The DP01 catalog entry uses the published catalog shape
    Given the E1001 seed and the P5 retention fake
    When a data steward calls GET /admin/data-products?product=DP01
    Then one entry holds productName "Account and arrears", ownerRole RW-DATASTEW, systemOfRecord "ACE (ingested from ALS)", refreshCycle DAILY and expectedBy 08:00
    Then sourceViews holds v_ace_account, v_ace_payment, v_ace_bucket_log and v_ace_batch_status
    Then definition and retentionClass are returned, and each field entry holds entity, fieldName, fieldId, dataType and isPersonal
    Then reconciliations holds REC-01 and REC-02 (the stored source of this list is Pending, GAP-3446)
    Then access is capabilityArea "Case record" and right "R"
    Then no roleCode, canRead or accessVersion is returned

  Scenario: AC16 A caller without Platform administration R cannot read the catalog
    Given RW-TRIBE has no Platform administration R
    When the user calls GET /admin/data-products
    Then the response is 403 MSG-P4-002 and no entry is returned

  Scenario: AC17 Missing or non-UUID caseId is refused before a read
    Given an authorised user calls GET /data-products/DP02/records without caseId
    When the request is validated
    Then the response is 400 MSG-GEN-001 and no authorise call or row query occurs
    Given a caller supplies the display case number RW-2026-000102 as caseId
    When the request is validated
    Then the response is 400 MSG-GEN-001 before any read

  Scenario: AC18 Invalid or overlapping access loads are refused without changing the current version
    Given a DPA-2026.12 load with an unknown product, and separately a load with overlapping rows
    When the P1 handler validates each load
    Then each whole load is refused with MSG-P1-002 naming the failed check
    Then DPA-2026.11 remains unchanged and no row of DPA-2026.12 exists

  Scenario: AC19 A new access version starts on its valid-from date
    Given DPA-2026.12 is approved with valid_from 2026-12-15
    When the business date reaches 2026-12-15 in Asia/Bangkok
    Then DPA-2026.12 rows decide access
    Then superseded DPA-2026.11 rows have valid_to 2026-12-14 inclusive
    Then at most one row is in force per product and role on any date

  Scenario: AC20 Re-delivery of an applied version is a no-op
    Given DPA-2026.12 has already been applied for data_product_access
    When the P3 reference-data contract delivers the same table code and version again
    Then no access row is added or changed

  Scenario: AC21 A view or retention dependency failure returns no partial data
    Given an ACE view query exceeds 5 seconds
    When GET /data-products/DP02/records is called
    Then the response is 503 MSG-GEN-006 and no field is returned
    Given the P5 retention read exceeds 2 seconds or answers 5xx
    When GET /admin/data-products is called
    Then the response is 503 MSG-GEN-006 and no catalog entry is returned

  Scenario: AC22 A product P1 does not serve is refused
    Given a caller requests DP03, DP08, DP09, DP10, DP12 or DP14
    When GET /data-products/{productCode}/records is called
    Then the response is 400 E400 with problem detail naming the owning service
    Then no product row is read and the message ID is Pending under GAP-3272

  Scenario: AC24 A product owned by another service is never read through a foreign schema
    Given a user holding an access row requests GET /data-products/DP10/records with the case UUID
    When the product code is validated
    Then the response is 400 and detail names rwb-document
    Then no rwb-case read, no authorise call and no query on any schema is made

  Scenario: AC25 A clear marker unmasks only the marked field
    Given RW-AUDIT has an active access row for DP02
    Given the authorise fake marks date_of_birth clear and every other personal field masked
    When u-audit-01 calls GET /data-products/DP02/records with the case UUID
    Then date_of_birth is returned with masked false
    Then every other field tagged is_personal has masked true, and one PII log entry is written
    Then no contact value is returned, whatever the markers

  Scenario: AC26 The authorise request carries what rwb-access evaluates
    Given RW-AUDIT has an active DPA-2026.11 access row for DP02
    When u-audit-01 calls GET /data-products/DP02/records with the case UUID twice
    Then each authorise request holds area CASE_RECORD, right R, productCode DP02, the caseId, the field IDs, the case owner, team and region, and the resolution DPA-2026.11, DP02, RW-AUDIT, 2026-11-20
    Then each request has a uuid Idempotency-Key and the two keys differ
    Then P1 reads only allowed, matrixVersion, maskingVersion and the markers from the answer

  Scenario: AC27 A missing capability letter is refused
    Given the authorise fake answers 403 MSG-P4-002 for u-sec-01
    When u-sec-01 calls GET /data-products/DP02/records with the case UUID
    Then the response is 403 MSG-P4-002, no source row is read and one refusal log entry is written

  Scenario: AC28 An unknown case is not found
    Given the rwb-case fake answers 404 for case 00000000-0000-4000-8000-000000000999
    When u-audit-01 calls GET /data-products/DP02/records with that case UUID
    Then the response is 404 MSG-P4-003 and no authorise call or source query is made

  Scenario: AC29 An rwb-case failure returns no data
    Given GET /cases/{caseId}/accounts does not answer within 2 seconds
    When u-audit-01 calls GET /data-products/DP02/records with the case UUID
    Then the response is 503 MSG-GEN-006 and no authorise call or source query is made

  Scenario: AC30 Unknown product code and paging limits
    When GET /data-products/DP99/records is called with the case UUID
    Then the response is 400 MSG-GEN-007 and nothing is read
    When GET /data-products/DP02/records is called with size 201, or with page -1
    Then the response is 422 MSG-GEN-002 and nothing is read
    When a granted case has no DP11 row and GET /data-products/DP11/records is called
    Then the response is 200 with empty items, page 0, size 50 and total 0

  Scenario: AC31 A back-dated access version is refused
    Given DPA-2026.12 valid from 2026-12-15 has been applied
    When the handler receives a version valid from 2026-12-01
    Then it is refused whole with MSG-P1-002 and no row changes

  Scenario: AC32 An access load cannot be checked without the role list
    Given GET /api/recovery/access/v1/admin/roles does not answer within 2 seconds
    When the handler validates DPA-2026.12
    Then the apply fails with MSG-GEN-006, no row of DPA-2026.12 exists and DPA-2026.11 rows are unchanged

  Scenario: AC33 With the flag off the operations are not served
    Given the flag rwb.source-data.product-access is off
    When either operation is called
    Then the response is 404 and nothing is read or logged as a personal read

  Scenario: AC34 Reads write no event and meet the read target
    Given the busiest-hour test load in SIT
    When GET /data-products/DP02/records is called under that load
    Then 95 percent of calls answer in under 2 seconds (NFR-P1-001)
    Then no outbox row is written and no event is published
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A role reads a data product only through a `data_product_access` row in force for that role and product | REQ-RDF-010; FEAT-RDF-15 |
| BR2 | A personal field is masked unless the authorise answer of rwb-access marks it `clear` for this read | CTL-11; `masking_rule` owned by P4; DL26 |
| BR3 | With no masking rule in force, every personal field stays masked | DL26 ("Masking rules load with no values") |
| BR4 | Every read of personal data is written to the PII access log through ACE Common; a read that cannot be logged is refused | REQ-ACA-006; CTL-11; INT-22 |
| BR5 | A record outside the caller's scope is refused; rwb-access tests the scope on the case attributes P1 sends and P1 applies no scope filter of its own | CTL-09; permission matrix; RWB-P4-E1016-APP |
| BR6 | An access load with an exception is refused in full; the previous version stays in force | Reference data change process, step 3; CTL-08 |
| BR7 | Each data product has one catalog entry with owner, system of record, refresh cycle, retention, the views and tables behind it, the reconciliations and fields with PDPA tags | REQ-RDF-011; `sys_fields.is_personal` |
| BR8 | Source data access is the view grant: the login holds SELECT on `recovery.v_ace_*` and no privilege on `public`, and may not write any view. A direct `public` table read fails at the database, not in code review | D-RCV-35 U4; ADR-010; Data Tier Map section 1 |
| BR9 | There is no tokenization. `v_ace_customer` returns the identity number as `id_no_masked` and `id_no_last4` only. `v_ace_contact` holds full phone, email and address, and the records operation returns none of them (RD-P1-060) | ADR-010; Data Tier Map section 7; DL26; rwb-source-data.yaml 5.1.0 |
| BR10 | Every one of the 30 `v_ace_*` views belongs to its data product with system of record "ACE"; a view marked "Workbench" is refused | BR-P1-002-2; FSD P1 A2.16 |
| BR11 | At most one access row is in force per product and role on any date; applying a version valid from D closes the replaced rows at D − 1; the same table code and version is applied once; a back-dated version is refused. Load states, approver and rollback are rwb-case's (`reference_version`); P1 has no load-state table | RD-P1-020 |

**Where each rule lives in the target.** BR1, BR6 and BR10 are this story's: the access rows, the load validation and the catalog guard are code and checks here, with the load arriving through the rwb-case reference-data contract (DP-07; GAP-0483; ASM-0675). BR2, BR3 and BR5 are rwb-access's decisions taken from its own rows; this story calls the answer once and applies it, and holds no masking row and no matrix row (GAP-0481; ASM-0673). BR11 is this story's apply handler. BR4 is this story's call into ACE Common PII logging and its 503. BR7 is the catalog service here, with the retention class read through P5's contract. BR8 is enforced by the grants of RWB-P1-E1069-DB and asserted by AC9, and BR9 is the view SQL of RWB-P1-E1069-APP.

### 9. State transitions

None. This story does not change a case status. What moves is the version in force of `data_product_access` when an approved load reaches its valid-from date, and the states of a load.

| From | Event | Condition | To |
|---|---|---|---|
| no version in force | the seed of DPA-2026.11 | The migration of RWB-P1-E1016-DB runs | DPA-2026.11 in force from its valid-from date |
| DPA-2026.11 in force | an approved load DPA-2026.12 | Its valid-from date arrives and every check passes | DPA-2026.12 in force; DPA-2026.11 kept with its valid-to date |
| a load delivered to the handler | validation | A role, product, overlap or back-date check fails | Refused whole; the version in force is unchanged. The load states themselves are in rwb-case (RD-P1-020) |
| a read | the authorise answer | The answer is `allowed` false, 403 or 404 | 403 or 404; nothing read and the refusal logged |
| a personal field | the marker | The marker is missing or `masked`, or `FieldMasker` fails | Masked |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Prepares the access rows for their products; reads the catalog with the Platform administration right R |
| RW-REFADM, reference data administrator | Submits the access load through the rwb-case reference-data contract with the Reference data right C |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules in rwb-access (DL26); reads the catalog |
| RW-SECADM, security administrator | Owns the role to permission matrix in rwb-access; reads the access log |
| RW-COE, RW-AUDIT, RW-PLATADM, RW-SECADM | Read the catalog with the Platform administration right R (RW-SECADM holds CRUDA). Any other role the matrix gives that right reads it too; the matrix is rwb-access data |
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
| DF-ACE-078 | v_ace_contact | contact_value | Not selected by the records operation (RD-P1-060) |
| DF-ACE-079 | v_ace_contact | contact_value_masked | Not selected by the records operation (RD-P1-060) |
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
Field IDs are those in the Logical Data Model and Data Dictionary. The personal tags on the view fields are read from `sys_fields.is_personal`. `data_product_access` is the only table this story writes; the four extension tables are created and written by other stories and are read only.

**Which side is this story's.** The `DF-ACE-` rows are read through the ACE views, and the `DF-EXT-` rows belong to P1 extension tables; the `DF-REF-` rows on `data_product`, `sys_objects`, `sys_fields` and `data_product_access` are P1 metadata and access rows. P1 does not read `case_list_row` or any P3 table. It reads the case attributes, account keys and person keys through the three published rwb-case operations of section 12.2. Retention and masking remain other services' data and are reached through their contracts.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13).

Contract versions built against: `rwb-source-data.yaml` 5.1.0 (API Specification v7); `rwb-case.yaml` 5.1.0; `rwb-access.yaml` 5.1.0 for `GET /admin/roles`; RWB-P4-E1037-CON; RWB-P3-E1043-CON; and RWB-P5-AD021-CON. `POST /authorise` is not in rwb-access.yaml: its request and answer follow RWB-P4-E1016-APP v3 and their property names are Pending under GAP-0983.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/data-products/{productCode}/records` | `DataProductRecordPage`; `caseId` is a required UUID; `page` defaults to 0; `size` defaults to 50 and has maximum 200; `fields` is `FieldValue[]` with `fieldName`, `value` and `masked` | Case record right R plus an active access row; P1 serves DP01, DP02, DP04, DP05, DP06, DP07, DP11 and DP13 only | Read only |
| GET | `/admin/data-products` | `DataProductCatalogEntry[]`; P1 metadata plus P5 retention; includes published `sourceViews`, `reconciliations: string[]` and `access: {capabilityArea, right}` where asserted by the criteria | Platform administration right R | Read only |

Errors are Problem bodies (RD-P1-004): 400 MSG-GEN-001 or MSG-GEN-007, 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003, 422 MSG-GEN-002, 503 MSG-GEN-006. `productCode` matches `^DP(0[1-9]|1[0-4])$`. `caseId` is the UUID `rwb_case.recovery_case.id`; the display number `RW-YYYY-NNNNNN` is not a lookup key. Requests for DP03, DP08, DP09, DP10, DP12 or DP14 return 400 E400 with the owning service in `detail`; the message ID is Pending under GAP-3272, and DP14 remains pending GAP-3281. The records response contains `items`, `freshness`, `page`, `size` and `total`; each field is a `FieldValue` with `fieldName`, `value` and `masked`. `/admin/data-products` takes optional `product`. This story adds none of the four ACE-specific reads. `GET /payments` is built by RWB-P1-E1013-APP and published through RWB-P1-E1015-CON. `GET /customers/{personKey}`, `GET /accounts/{accountKey}` and `GET /collateral/{assetKey}` are operations of rwb-source-data.yaml 5.1.0 built by RWB-P1-E1069-APP (RD-P1-060).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Once per records read. Header `Idempotency-Key` (new uuid). Request: area `CASE_RECORD`, right `R`, `productCode`, `caseId`, field IDs, case attributes, access resolution (access version, role codes, valid-from). Answer: `allowed`, `matrixVersion`, `maskingVersion`, one marker per field ID. Property names Pending, GAP-0983 | DP-08, DP-11; one hop, 2 s, breaker, no retry, no stale cache |
| GET | `/api/recovery/access/v1/admin/roles` | P4 rwb-access | `Role.roleCode` values, to validate an access version. Pending: identity and permission of the handler's call, GAP-3447 | Load validation only; 2 s |
| (interface) | `AccessGuard` and `FieldMasker` of RWB-P4-E1037-CON | P4 rwb-access | Catalog right check; rendering of the masked value from the authorise markers | DP-08; library, no SQL on `masking_rule` |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | `ownerUserId`, `teamCode`, `regionCode` for the scope test | Case record R; one hop, 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}/accounts` | P3 rwb-case | `accountKey` filter | Case record R; one hop, 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}/parties` | P3 rwb-case | `personKey` filter | Case record R; one hop, 2 s |
| reference-data apply handler | table code `data_product_access` | P1 handler invoked by the P3 reference-data pipeline | Applies the approved whole version atomically and idempotently on (table code, version); no load-state table. Transport Pending, GAP-3338 | RD-P1-020 |
| GET | `/api/recovery/document/v1/retention-classes` | P5 rwb-document | Query `productCode`; `RetentionClassPage` of `RetentionClass` (RWB-P5-AD021-CON). Not yet in rwb-document.yaml. Pending: product-code mapping, calls per catalog read, and the value when a product has no class or several, GAP-1028 | `Documents R`; one hop, 2 s |

A 403 or 404 from rwb-access or a 404 from rwb-case is passed on with its message; a timeout, 5xx or malformed answer of any runtime call is 503 MSG-GEN-006 and returns no data. Each call is one hop; no case table of another service is read (DP-01, DP-05, DP-11).

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
| `sys_objects` | `rwb_source_data` | P1 | Read only: the E1001 baseline and active object mappings |
| `sys_fields` | `rwb_source_data` | P1 | Read only: the E1001 baseline and active field metadata |
| `sys_field_version` | `rwb_source_data` | P1 | Read only: the field history is a later P1 story's |
| `data_contract` | `rwb_source_data` | P1 | Read only: the contract rows are RWB-P1-E1064-APP's |
| ACE views | `recovery` | P1 read path | Read only where mapped to one of the eight products P1 serves; no other service reads these views directly |
| `v_data_product_catalog` | `rwb_source_data` | P1 | **Not created here**: RWB-P1-E1016-DB creates the read model; this story reads it |
| `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | `rwb_source_data` | P1 | **Not created here**: RWB-P1-E1069-DB creates them; read only |
| `retention_rule` | `rwb_document` | P5 | Not read: the retention class comes through P5's contract |
| `masking_rule`, `role`, `permission` | `rwb_access` | P4 | Not read: reached through the authorise answer and the `FieldMasker` interface |

No table of another service is read and no foreign key crosses a schema (DP-01). The service table `data_product_access` is the only row this story writes.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access: RWB-P4-E1037-CON fake (with the RWB-PLT-E1037-CON guard library) | `POST /api/recovery/access/v1/authorise` | allowed true with all markers masked; one marker clear; allowed false; 403 MSG-P4-002; 404 MSG-P4-003; 503; timeout |
| rwb-access role-list fake | `GET /api/recovery/access/v1/admin/roles` | `Role` array with `roleCode`, per rwb-access.yaml 5.1.0; a timeout |
| rwb-case fake | The three case reads | A case in scope, a case of another owner, a 404 and a timeout, per rwb-case.yaml 5.1.0 |
| rwb-access: RWB-P4-E1037-CON `FieldMasker` fake | The masking interface | Applies the markers; the unavailable error |
| rwb-case: RWB-P3-E1043-CON reference-data fake | The reference-data contract | An accepted load for table code `data_product_access` and one for `sys_objects`; a load naming an unknown role; a view marked "Workbench" |
| Delivered-DB fixture | RWB-P1-E1016-DB | A container with the three indexes, `v_data_product_catalog` and the DPA-2026.11 seed, so AC9, AC10 and AC11 run against the delivered objects |
| P5 retention fake | P5 rwb-document | The retention class of each of the 14 products |

Published version of the contract fake library for rwb-access and rwb-case: Not specified in the source documents (DOR-RWB-P1-E1016-APP-22).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/source-data/v1` | P4 authorise and role list, three rwb-case reads, P5 retention read; the P3 reference pipeline invokes the P1 apply handler | OpenAPI 3.1; one hop and 2 s for each runtime call (DP-11) |
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
| `DataProductController` | Controller | `GET /data-products/{productCode}/records` and `GET /admin/data-products`; request validation; RFC 9457 problem details |
| `DataProductAccessService` | Service | Access resolution, authorise call, refusal log, PII log write, 503 on a failed log |
| `CaseReadClient` | Client | The three rwb-case reads; one hop, 2 s, breaker |
| `DataProductRecordService` | Service | Reads the objects of the product listed in section 3, applies the authorise markers and returns the page |
| `DataProductCatalogService` | Service | Builds the entries from `v_data_product_catalog` and the P5 retention answer |
| `DataProductAccessRepository` | Repository | Reads and writes `data_product_access`; no other schema is named |
| `DataProductAccessHandler` | Reference-table handler | Apply handler for table code `data_product_access`: known product, known role, no overlap, not back-dated, refuse whole, idempotent on (table code, version) |
| `AccessGuardClient` | Client | The authorise operation with `Idempotency-Key`, the guard and `FieldMasker`; one hop, 2 s, breaker |
| `PiiAccessLogWriter` | Client | ACE Common PII logging: user, product, case, field names and time, never a value |
| `RetentionClient` | Client | P5's retention read for the catalog entry |
| `DataProductAccess` | Entity | One row per product, role and version |

**Database.** This story creates no table, no index and no view. It writes rows of `data_product_access` through the handler and reads P1 metadata, `v_data_product_catalog` and P1 extension tables. Case facts come from the rwb-case contract, not a P1 or P3 table. The indexes, read model and DPA-2026.11 seed are RWB-P1-E1016-DB's (GAP-0484; ASM-0676).

**Configuration and reference data**

- Access version `DPA-2026.11` is prepared by the data steward and loaded by the reference data administrator through the rwb-case reference-data contract; the seed of the version is RWB-P1-E1016-DB's and covers only the rows of section 11 (GAP-0482; ASM-0674).
- Masking rules are loaded by Compliance into rwb-access under DL26 and are never copied here.
- The authorise contract, its 2 s budget and the masking answer are configuration of the guard library, not constants in this service (DP-08).
- The feature flag `rwb.source-data.product-access` gates the two operations until the seed and read model are in place. Section B view tests run in DEV and the pipeline; the related read feature remains off until RWB-ACE-001 (RD-P1-043).

**Build steps**

1. `AccessGuardClient` and `PiiAccessLogWriter` against the published fakes, with the timeout and no-stale-cache rules (12.2, X9, X10).
2. `CaseReadClient`, then `DataProductAccessService` in the order of section 4 steps 2 to 5 (AC1, AC3, AC5, AC8, AC26 to AC29).
3. `DataProductRecordService` reading the objects of section 3, applying the markers and paging (AC1, AC6, AC13, AC22, AC24, AC25, AC30).
4. `DataProductAccessHandler` with the whole-load validation: known product, known role, no overlap, not back-dated (AC4, AC18 to AC20, AC31, AC32).
5. `DataProductCatalogService` and `GET /admin/data-products` over the delivered read model, with the P5 retention answer and the "Workbench" refusal (AC10, AC11).
6. The two operations on the contract, with the error envelope and the 403, 404 and 503 mappings (12.1).
7. Tests for every criterion of section 7 against the delivered-DB fixture and the fakes of section 12.8, behind the flag (AC33, AC34).

**Done when.** The tests listed in section 16 pass, the catalog returns active entries from `v_data_product_catalog`, every read of a personal field appears once in the PII access log, records are served only for the eight listed products, and no query names `masking_rule`, `role`, `permission` or `retention_rule`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | No right, or no access row for the product | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P1-002 | Access load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-003 | A catalog load does not name exactly one system of record and one owner | {product} must have exactly one system of record and one named owner. |
| MSG-GEN-001 | caseId missing or not a UUID | Enter {field}. |
| MSG-GEN-002 | `page` or `size` out of range | Text of Error and Message Standard v6 |
| MSG-GEN-007 | Unknown product code | Text of Error and Message Standard v6 |
| MSG-GEN-006 | PII access log, authorise, rwb-case, role list, ACE view or retention read unavailable | {system} is not available. Try again in a few minutes. |
| MSG-P4-001 | Caller has no Recovery Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |

The Problem response follows RD-P1-004: `type`, `title`, `status`, `detail`, `messageCode`, `messageTh`, `field` and `traceId`. MSG-P4-001, MSG-P4-002 and MSG-P4-003 are passed through unchanged from the P4 guard. Pending: the values of {action} and {system} for these two operations, owner product owner with the Error and Message Standard owner, GAP-3449. The refusal log: Pending which log holds a refusal, its fields, what happens when that write fails and the time limit of the ACE Common log call, owner Compliance with the rwb-access owner, GAP-3442. The rendering of a masked name, date of birth, email, address, null or short value is Pending, owner Compliance with the data architect, GAP-3441. Thai translations follow Error and Message Standard v6.

### 15. Screens and states

No screen in this story. The case record view SCR-03 (Read only) shows the product data the role may read, with personal fields masked, and reaches this service through the gateway-bff composite route (DP-19). Catalog entries are read through `GET /admin/data-products` and rendered by the administration screen of RWB-P1-E1064-APP. SCR-47 Personal data shows masking rules from Epic 8 and reads them from rwb-access, not from this service. States on the screens: loading, empty (no access row, so the panel is not shown), refused (403 or 404 problem body) and ready. SCR-03 states: loading; read only; on hold banner; empty section (MSG-P3-024); error in the section that failed (MSG-P3-023); stale input (MSG-P1-001); no access when the case is out of scope (MSG-P4-003); access record cannot be written (MSG-P7-003). SCR-47 states: loading; list; empty (for the data subject request register, total 0 and no error); error when a request is not recorded (503 MSG-P7-003); no access (403 MSG-P4-002).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1016-APP-27 | Legacy regression: read regression | End to end | Role access (legacy RWB-E1-016 AC1) |
| TC-P1-E1016-APP-28 | Legacy regression: access-row refusal regression | End to end | Access denied (legacy RWB-E1-016 AC3) |
| TC-P1-E1016-APP-29 | Legacy regression: reference-load refusal regression | Component | An access load with an unknown role is refused (legacy RWB-E1-016 AC4) |
| TC-P1-E1016-APP-31 | Legacy regression: no-mask-rule regression | End to end | No masking rule loaded keeps every personal field masked (legacy RWB-E1-016 AC6) |
| TC-P1-E1016-APP-32 | Legacy regression: PII-log refusal regression | End to end | The PII access log is unavailable (legacy RWB-E1-016 AC7) |
| TC-P1-E1016-APP-33 | Legacy regression: future-access-row regression | End to end | An access row not yet in force (legacy RWB-E1-016 AC8) |
| TC-P1-E1016-APP-34 | Access; refusal of `GET /admin/data-products` for RW-TRIBE with MSG-P4-002 | Component | Access; refusal of `GET /admin/data-products` for RW-TRIBE with MSG-P4-002 |
| TC-P1-E1016-APP-35 | AC9 | Component | The service login reads ACE data only through the granted views |
| TC-P1-E1016-APP-36 | AC10 | End to end | The catalog exposes the P1 dictionary baseline and view rows |
| TC-P1-E1016-APP-37 | AC11 | Component | A catalog load cannot mark an ACE view as Workbench |
| TC-P1-E1016-APP-38 | §12 operations, events and activities | Component | §12 operations, events and activities |
| TC-P1-E1016-APP-39 | §12.7 tables (ASM-3438) | Component | §12.7 tables (ASM-3438) |
| TC-P1-E1016-APP-40 | AC12 | End to end | An authorise failure returns no data |
| TC-P1-E1016-APP-41 | AC13 | End to end | FieldMasker unavailable keeps personal fields masked |
| TC-P1-E1016-APP-42 | AC14 | End to end | A request without a Workbench role receives the session error |
| TC-P1-E1016-APP-01 | AC1 | Contract | A role with an access row reads DP02 with personal values masked |
| TC-P1-E1016-APP-02 | AC3 | Contract | A role without a product access row is refused |
| TC-P1-E1016-APP-03 | AC4 | Contract | A reference load with an unknown role is refused in full |
| TC-P1-E1016-APP-04 | AC5 | Contract | A case outside the caller scope is refused |
| TC-P1-E1016-APP-05 | AC6 | Contract | No masking rule keeps tagged personal fields masked for RW-COMPLY |
| TC-P1-E1016-APP-06 | AC7 | Contract | A PII access-log failure returns no personal data |
| TC-P1-E1016-APP-07 | AC8 | Contract | An access row starting on a later date is not in force |
| TC-P1-E1016-APP-08 | AC15 | Contract | The DP01 catalog entry uses the published catalog shape |
| TC-P1-E1016-APP-09 | AC16 | Contract | A caller without Platform administration R cannot read the catalog |
| TC-P1-E1016-APP-10 | AC17 | Contract | Missing or non-UUID caseId is refused before a read |
| TC-P1-E1016-APP-11 | AC18 | Contract | Invalid or overlapping access loads are refused without changing the current version |
| TC-P1-E1016-APP-12 | AC19 | Contract | A new access version starts on its valid-from date |
| TC-P1-E1016-APP-13 | AC20 | Contract | Re-delivery of an applied version is a no-op |
| TC-P1-E1016-APP-14 | AC21 | Contract | A view or retention dependency failure returns no partial data |
| TC-P1-E1016-APP-15 | AC22 | Contract | A product P1 does not serve is refused |
| TC-P1-E1016-APP-16 | AC24 | Contract | A product owned by another service is never read through a foreign schema |
| TC-P1-E1016-APP-17 | AC25 | Contract | A clear marker unmasks only the marked field |
| TC-P1-E1016-APP-18 | AC26 | Component | The authorise request carries what rwb-access evaluates |
| TC-P1-E1016-APP-19 | AC27 | Component | A missing capability letter is refused |
| TC-P1-E1016-APP-20 | AC28 | Component | An unknown case is not found |
| TC-P1-E1016-APP-21 | AC29 | Component | An rwb-case failure returns no data |
| TC-P1-E1016-APP-22 | AC30 | Component | Unknown product code and paging limits |
| TC-P1-E1016-APP-23 | AC31 | Component | A back-dated access version is refused |
| TC-P1-E1016-APP-24 | AC32 | Component | An access load cannot be checked without the role list |
| TC-P1-E1016-APP-25 | AC33 | Component | With the flag off the operations are not served |
| TC-P1-E1016-APP-26 | AC34 | Component | Reads write no event and meet the read target |

TC-P1-E1016-APP-27 to TC-P1-E1016-APP-29, TC-P1-E1016-APP-31 to TC-P1-E1016-APP-33 are legacy regression cases only and TC-P1-E1016-APP-30 is retired. The criteria are covered by the other rows above, on the fixtures below.

| Fixture | Value |
|---|---|
| Case in scope | `00000000-0000-4000-8000-000000000102` (display number RW-2026-000102), borrower `P0000102` |
| Case of another owner | `00000000-0000-4000-8000-000000000456` (display number RW-2026-000456) |
| Unknown case | `00000000-0000-4000-8000-000000000999` |
| Synthetic values | identity `1234567890123`, mobile `0812345678`; identity masked by the view with `*` |
| Access version | DPA-2026.11, seven rows, in force from 2026-11-20 |

### 17. Guardrails

- No business value in code: access by role and masking by role are data rows, in `data_product_access` here and in rwb-access's own tables there; the code holds no role, product or masking list.
- No personal data in logs, tests, events, workflow inputs or prompts: the PII access log carries field names, not values; test customers are synthetic; no event carries a personal field.
- Data Classification v5 classes these fields as personal data: `account_key`, `person_key`, `asset_key` and `contact_key` (Confidential, Indirect identifier) and `payment_code` (Confidential; Indirect identifier in proceeds, Customer data in `v_ace_payment`). Their values are never written to logs, events, workflow inputs or prompts, and tests use synthetic values only. A field tagged `is_personal` in `sys_fields` follows the `FieldMasker` answer. Payload codec rule for these fields: Not specified in the source documents (DOR-RWB-P1-E1016-APP-11).
- A records or catalog read is not a decision: it is written to the access log only and publishes no `DecisionRecorded` (RD-P1-072).
- No read of another module's tables: the case facts come from rwb-case, the rights, scope and masking markers from the authorise answer; `masking_rule`, `role`, `permission` and `retention_rule` are never named in a query (DP-01).
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: this service reads its own views and publishes the read path; every other service calls this contract (DP-05, ADR-010).
- A read that cannot be logged returns no personal data.
- No token, detokenization call or clear identity number exists in any response.
- One hop and 2 s on every consumed contract; a slow answer refuses the read and returns no field (DP-11).
- Records reads answer in under 2 seconds at the 95th percentile (NFR-P1-001); the flag `rwb.source-data.product-access` off answers 404.
- The seed, the indexes and the read model are one story's delivery and one story's test: this story reads them and never re-creates them (GAP-0484; ASM-0676).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role through the views; personal data masked by role under PDPA | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | All recovery processes | CTL-09, CTL-11; DL26; BR-P1-015-2, BR-P1-015-3 | TC-P1-E1016-APP-35 to TC-P1-E1016-APP-37, TC-P1-E1016-APP-40 to TC-P1-E1016-APP-42, TC-P1-E1016-APP-01 to TC-P1-E1016-APP-26; legacy regression TC-P1-E1016-APP-27 to TC-P1-E1016-APP-29, TC-P1-E1016-APP-31 to TC-P1-E1016-APP-33 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record, refresh and retention | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-16 | All recovery processes | CTL-08; BR-P1-002-2; BR-P1-016-2 | TC-P1-E1016-APP-35 to TC-P1-E1016-APP-37, TC-P1-E1016-APP-40 to TC-P1-E1016-APP-42, TC-P1-E1016-APP-01 to TC-P1-E1016-APP-26 |
| REQ-ACA-006 | Every read of personal data is written to the PII access log, and a read that cannot be logged is refused | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | All recovery processes | CTL-11; BR-P1-015-4 | TC-P1-E1016-APP-35 to TC-P1-E1016-APP-37, TC-P1-E1016-APP-40 to TC-P1-E1016-APP-42, TC-P1-E1016-APP-01 to TC-P1-E1016-APP-26; legacy regression TC-P1-E1016-APP-27, TC-P1-E1016-APP-32 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1001-APP | App development | H build dependency: the `rwb_source_data` baseline, `data_product`, `sys_objects`, `sys_fields`, `data_product_access`, `data_contract` and `v_data_dictionary` |
| RWB-P1-E1064-APP | App development | H build dependency: the data product, dictionary and contract administration of the service, on the same base |
| RWB-P1-E1069-APP | App development | H build dependency: the 30 `recovery.v_ace_*` views and the read path this story's records come from |
| RWB-P1-E1016-DB | ACE DB | X external dependency: the three indexes, `v_data_product_catalog`, the DPA-2026.11 seed and the schema checks |
| RWB-P1-E1016-CON | Contract | Sibling of the same legacy key: two E1016 operations, shared schemas and the Problem envelope |
| RWB-P4-E1037-CON | Contract | C: the guard library and the `FieldMasker` interface (DP-08) |
| RWB-P4-E1016-APP | App development | C: the data-product half of `POST /authorise` this story calls |
| RWB-P3-E1043-CON | Contract | C: the reference-data contract that carries the access load (DP-07) |
| RWB-P1-E1015-APP | App development | Sibling: the freshness stamp the record page carries |
| RWB-P1-E1069-DB | ACE DB | Delivers the grants and the four extension tables this story reads and AC9 asserts |

### 19. Out of scope

- The role to permission matrix, masking rows and masking answer: rwb-access (P4); this story calls its published contracts and holds no P4 table.
- The three indexes, the read model, seven-row access seed and schema checks: RWB-P1-E1016-DB.
- The P1 baseline tables, dictionary rows and 14 product rows: RWB-P1-E1001-APP.
- ACE view SQL and grants: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- `GET /payments`: RWB-P1-E1013-APP; this story exposes the product-record and catalog operations only.
- Case-list storage and direct P3 table reads: removed by RD-P1-024.
- `GET /customers/{personKey}`, `GET /accounts/{accountKey}` and `GET /collateral/{assetKey}` (RD-P1-060; built by RWB-P1-E1069-APP) and the DP02 contact rows (RWB-P1-E2021-APP).
- Message ID for unsupported-product E400: Pending under GAP-3272. DP14 records remain unavailable pending GAP-3281.
- The gateway-bff composite route and screen rendering: platform edge and screen owners (DP-19).

### 20. Remaining delivery steps

- Size: Not specified; owner P1 delivery lead.
- EP01 design sign-off: Pending; owner product owner.
- RWB-P1-E1016-CON Done: Pending; owner contract owner.
- Authorise path in rwb-access.yaml and its property names: Pending; owner rwb-access service owner, GAP-0983.
- Authorise caller alignment recorded in RWB-P4-E1016-APP (its Pending note on this story): owner rwb-access story editor.
- Masked rendering (GAP-3441), refusal log (GAP-3442), business date (GAP-3443), sort order and total (GAP-3444), field lists and case filter (GAP-3445), reconciliation list source (GAP-3446), role-call identity (GAP-3447), message placeholders (GAP-3449): Pending; owners as stated where each is named.
- `cif_no` masking: Pending; owner Compliance, GAP-3439.
- Reference-load handler transport: Pending; owner solution architect with the rwb-case owner, GAP-3338.
- Whether the catalog filters by `data_product.valid_from`: Pending; owner data architect, GAP-3440.
- Message ID for unsupported-product E400: Pending; owner product owner and Error and Message Standard owner, GAP-3272.
- DP14 records access: Pending; owner rwb-ace-data service owner, GAP-3281.
- Test data in DEV: Pending; owner QA lead.
- Section B view tests in DEV and pipeline; the related read feature stays off until RWB-ACE-001, owner ACE team (RD-P1-043).
