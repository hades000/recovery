# RWB-P1-E1016-CON Access control per data product and catalog entries

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register): AC2 compares the field metadata directly against the Physical Schema v9 seed.

- RD-P1-005 aligns the contract to `rwb-source-data.yaml` 5.1.0 (API Specification v7) and the `FieldValue[]` records shape (review #3, #4).
- RD-P1-021 and RD-P1-024 correct supported products and remove P1 case-list storage; RD-P1-026 adds RW-COMPLY/DP02 (review #18).
- RD-P1-004 aligns problem responses and current error texts (review #3, #16, #17, #21).
- The published rwb-access operation requires `Idempotency-Key`. P1 uses the RD-P1-063 fake until request and answer property names are published (GAP-3322).
- DP02 contact rows are those of rwb-source-data.yaml 5.1.0; the provider fake, apply handler, role list, PII log and retention rows are stated and criteria AC10 to AC16 added (review #2, #7, #9, #10, #11, #13, #14, #15, #24).
- The build dependency on the app and DB stories is removed (this story is Day 1), and the ACE field types are copied again from Physical Schema v9.
- Finishing pass (RD-P1-060, RD-P1-063; requests W2-tests-1063, W3-messages-0041, F09-affected-0164; test case backfill): the three entity reads are RWB-P1-E1069-APP's, the interim authorise assertions are stated, message texts follow Error and Message Standard v6 and Test Cases v9 IDs are cited.



| Item | Value |
|---|---|
| Story key | RWB-P1-E1016-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E1016-CON-16); squad sizes at refinement |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7); base `/api/recovery/source-data/v1` |
| Depends on (build) | None |
| Contract dependencies | rwb-source-data.yaml 5.1.0; RWB-P4-E1037-CON; RWB-P3-E1043-CON; RWB-P5-AD021-CON; rwb-case.yaml 5.1.0 (three case reads); rwb-access.yaml 5.1.0 (`GET /admin/roles`, `POST /authorise`); authorise builder RWB-P4-E1016-APP (GAP-3322) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-004, FR-P1-006, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-026, FR-P1-027, FR-P1-030) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-020, RD-P1-021, RD-P1-023, RD-P1-024, RD-P1-025, RD-P1-026, RD-P1-041, RD-P1-060, RD-P1-063 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-016 for rwb-source-data. This story publishes the E1016 records and catalog operations, shared schemas and error envelope; the four ACE-specific reads are owned by the corresponding P1 service slices. Authorise, role-list, case-scope and retention answers are consumed, never redefined (DP-08, DP-11; Architecture v5 slides 11, 15 and 41). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1016-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: contract baseline aligned to the readiness rulings. Tool: T3 Code.

### 1. Story

As a **tech lead**, I want **the published contract baseline for the two E1016 operations: records for the products P1 serves and the product catalog, including schemas, access behavior, owner contracts, errors and compatibility rules**, so that **the app and DB stories and consumers can build against one reviewed contract**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). rwb-source-data is the only service that reads the 30 `recovery.v_ace_*` views, so its read operations are the read path of the other 18 services and of the agents (DP-05; Architecture v5 slides 11, 15 and 41). Access control and the catalog are the two things every consumer must be able to reproduce before the service exists: which product a role may read, and how a masked field is shaped in a response. If those are agreed once and faked, the app story builds in parallel with rwb-access, rwb-case and rwb-document, and a change in any of them is caught in a contract test rather than in an integration window.

The baseline also fixes the naming the checks require: schema and login `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-02, DP-13, DP-14; Architecture v5 slides 29 and 41). This capability publishes no event and starts no workflow, so the contract says so explicitly and no consumer waits for one.

**What D-RCV-60 changes.** The legacy story had no published contract: the guard, the masking rules, the case scope and the catalog were in-process calls. Now three of them are other services' published contracts (rwb-access's authorise and `FieldMasker`, rwb-case's reference data, rwb-document's retention read) and one is P1's own read model. The contract is what keeps that change from becoming five local agreements.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice (DP-14).
- The platform error envelope is the baseline; where this document narrows it, it does so explicitly and names the message ID per condition.
- The operations and their owners are taken from the Ownership Map v1 only; rwb-source-data never documents an operation owned by another service, and `POST /api/recovery/access/v1/authorise` is documented as consumed (DP-08).
- `masking_rule`, `role` and `permission` are rwb-access's tables and `retention_rule` is rwb-document's (Ownership Map v1), so no field of those tables appears in a request or response schema of this document.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- No human approval is needed to publish a Draft baseline; the baseline is tagged and handed to the consumers when the contract tests pass.

### 4. Flow

1. Check the E1016 records and catalog operations of `rwb-source-data.yaml` 5.1.0 against RD-P1-004, RD-P1-005, RD-P1-021, RD-P1-023 and RD-P1-024, and request what is missing from the API specification owner.
2. Define records as `DataProductRecordPage` with `FieldValue[]`, and define the catalog with only its published properties.
3. Document the P4 authorise, role list and guard, the three rwb-case reads, the P5 retention read, the PII access log and the reference-load handler with owners and budgets; carry unresolved shapes as Pending with owners.
4. Map statuses and messages to the Problem schema and Error and Message Standard v6.
5. Publish the provider fake and the consumed fakes, record compatibility and consumer requests.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required value is missing or `caseId` is not a UUID | 400 Problem with the failing field | MSG-GEN-001 | AC3 |
| X2 | A caller without the right, or `allowed` false from authorise | 403 Problem | MSG-P4-002 | AC3, AC11 |
| X3 | A case outside the caller's scope | 404 with the error envelope and MSG-P4-003 | MSG-P4-003 | AC3 |
| X4 | A required field of a response schema is missing from the source material | The field carries the placeholder and one gap row is carried | None | AC2 |
| X5 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X6 | A schema declares a masking or role field owned by another service | The contract test fails on the ownership check | None | AC5 |
| X7 | A caller asks for a major version the service does not serve | 404 Problem, `type` ending `/unknown-version`, the version named as the value | MSG-GEN-007 | AC7 |
| X8 | A productCode is valid but its records are not served by P1 | 400 E400; detail names the owning service; no row is read | Message ID Pending, GAP-3272 | AC1 |
| X9 | Authorise, rwb-case, role list, PII log, ACE view or retention read fails or times out | 503 Problem; no data | MSG-GEN-006 | AC15 |
| X10 | Unknown product code, or `page` or `size` out of range | 400 for the code; 422 for the range | MSG-GEN-007; MSG-GEN-002 | AC16 |

Business message text follows Error and Message Standard v6 and the final RD-P1 register. The unsupported-product E400 message ID remains Pending under GAP-3272.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map v1 and the target architecture only |
| Negotiable | Field-level detail is settled with the consumers; the operations, the interfaces, the envelope and the naming are fixed by the target architecture |
| Valuable | Unblocks the app and DB stories of this legacy key and every consumer of the service's read path on Day 1 |
| Estimable | One API publication artifact, two operations, shared response schemas, consumed contract references, fakes and contract checks |
| Small | Fits one sprint with the contract tests |
| Testable | Each criterion is checked against the API artifact and its contract fakes; its cases are in Test Cases v9 |

### 7. Acceptance criteria

```gherkin
Feature: E1016 product-record and catalog contract

  Background:
    Given rwb-source-data.yaml version 5.1.0 (API Specification v7) is the publication artifact
    Given P1 owns data_product, data_product_access, sys_objects and sys_fields

  Scenario: AC1 The records operation enforces the final product and query contract
    Given GET /data-products/{productCode}/records is documented
    When a request is validated
    Then productCode matches ^DP(0[1-9]|1[0-4])$
    Then caseId is required and is a UUID for rwb_case.recovery_case.id
    Then page has minimum 0 and default 0
    Then size has minimum 1, default 50 and maximum 200
    Then records are served only for DP01, DP02, DP04, DP05, DP06, DP07, DP11 and DP13
    Then DP03, DP08, DP09, DP10, DP12 and DP14 return 400 E400 with owning service in detail and no source row is read

  Scenario: AC2 Records and catalog schemas match their published shapes
    Given the shared response schemas are reviewed against RD-P1-005
    When DataProductRecordPage and DataProductCatalogEntry are validated
    Then DataProductRecord.fields is FieldValue[] with fieldName, value and masked
    Then DataProductCatalogEntry retains sourceViews and adds reconciliations as string[] and access as {capabilityArea, right}
    Then no story-only catalog property or roleCode, canRead or accessVersion appears
    Then an automated comparison checks every served ACE field against the section 11 sys_fields seed, matching field ID, view, field name, logical type, physical type and is_personal
    Then FieldValue.value encoding for non-TEXT source types remains Pending under DOR-RWB-P1-E1016-CON-7

  Scenario: AC3 Errors use one Problem shape and Error and Message Standard v6 text
    Given a request or consumed dependency fails
    When a Problem response is returned
    Then type, title, status, messageCode and traceId are required; detail and messageTh are optional; the owning service stamps instance with the request path and trace ID. Include field only for an input failure and errors only on 400 or 422 when multiple inputs fail.
    Then the content type is application/problem+json
    Then MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P1-003 and MSG-GEN-006 match section 14 exactly

  Scenario: AC4 Consumed contracts name their owner, payload status and budget
    Given section 12.2 lists consumed contracts
    When each row is reviewed
    Then authorise, GET roles, the guard library, the three rwb-case reads, P5 retention and the PII access log are shown as consumed from their owners
    Then runtime REST calls are one hop with a 2 s budget
    Then unresolved payloads have a Pending statement, owner and gap reference
    Then P3 reference loads invoke P1's atomic, idempotent handler and no P1 load-state table is defined

  Scenario: AC5 No foreign service table is part of a P1 schema
    Given every property and query in the contract is reviewed
    When ownership is checked
    Then no rwb-access role, permission or masking table and no rwb-document retention table appears
    Then case attributes and keys are obtained through the rwb-case contract and not a P3 table

  Scenario: AC6 Contract fakes match the interfaces they represent
    Given the fakes in section 12.8
    When contract comparisons run
    Then each fake matches its current published interface
    Then missing versions or response schemas remain explicit Pending items, not invented properties

  Scenario: AC7 Major version changes follow the compatibility rule
    Given the REST base ends in /v1
    When an additive change is made
    Then it remains within major version 1
    When a breaking change is proposed
    Then a new major version and base path are required
    Then the pipeline compatibility check refuses a /v1 document that removes, renames or retypes a property
    When GET /api/recovery/source-data/v2/data-products/DP02/records is called
    Then the answer is 404 with messageCode MSG-GEN-007 naming v2

  Scenario: AC10 The provider fake serves both operations
    Given the fake at fakes/rwb-source-data/5.1.0/ generated from rwb-source-data.yaml 5.1.0
    When a consumer calls getDataProductsProductcodeRecords and getAdminDataProducts
    Then there is one mapping for each status each operation declares, with Problem bodies for the 4xx and 5xx
    Then the provider build verifies every fixture against the implementation

  Scenario: AC11 The consumed authorise contract matches the provider story
    Given the authorise fake of section 12.8
    When P1 sends area CASE_RECORD, right R, productCode DP02, the caseId, field IDs, case attributes, the access resolution and a uuid Idempotency-Key
    Then the contract test asserts the allow or deny outcome. Masking markers and version fixtures used by local P1 tests are local test data pending the published answer shape (GAP-3322).
    When the Idempotency-Key is missing
    Then the fake answers 400 MSG-PLT-N009-03

  Scenario: AC12 Each operation refuses a call without a session
    Given no session
    When either of the two operations is called
    Then the answer is 401 MSG-P4-001 and no data

  Scenario: AC13 The DP02 contact row carries no contact value
    Given the records fixture for DP02
    When a contact row is validated
    Then its fields are contactKey, contactType, consentStatus (GIVEN, WITHDRAWN or UNKNOWN) and verifiedAt
    Then no contact value, address, name or identity number is present

  Scenario: AC14 The access-load handler contract refuses and replays as stated
    Given the version in force is DPA-2026.11
    When the handler fixture delivers DPA-2026.12 with role RW-UNKNOWN twice
    Then both deliveries are refused whole with MSG-P1-002 naming the check and no row changes
    When an accepted version is delivered twice
    Then the second delivery changes no row

  Scenario: AC15 Each dependency failure has one answer
    Given the authorise, rwb-case, role list, PII log, ACE view or retention fake times out
    When the dependent operation runs
    Then the answer is 503 MSG-GEN-006 and no record, field or catalog entry is returned

  Scenario: AC16 Unknown product code and paging limits are stated
    When productCode DP99 is sent
    Then the answer is 400 MSG-GEN-007
    When size 201 or page -1 is sent
    Then the answer is 422 MSG-GEN-002
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 |
| BR2 | Event names would be `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`; this capability publishes none | DP-14; Template and Rules §R4 |
| BR3 | Every personal field is masked unless the authorise answer marks it `clear`; the contract carries the marker, never a rule value | DP-08; CTL-11 |
| BR4 | Error responses use one envelope and one message ID per condition; business message texts are those of Error and Message Standard v6 | RD-P1-004 |
| BR5 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 11 |
| BR6 | The document lists only operations owned by rwb-source-data; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR7 | No business value is fixed in the contract: the roles, the products, the access rows and the masking rules stay data | Template and Rules §R7.2 s17 |
| BR8 | The contract names no table of another service: the role, permission, masking and retention tables are reached through their owners' contracts | DP-01; Ownership Map v1 |
| BR9 | RWB-P1-E1016-DB creates no table that RWB-P1-E1001-APP or RWB-P1-E1069-DB already creates; a repeated run changes nothing | RWB-P1-E1001-APP; RWB-P1-E1069-DB |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two E1016 operations, shared schemas and Problem envelope are described | In review |
| In review | Consumer sign-off | The app and DB stories and the consuming teams accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake or an ownership breach | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the document, the interfaces and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Consuming teams (app, DB, and the rwb-access, rwb-case and rwb-document owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope and the naming rule this document reuses |
| Data steward | Confirms that the catalog entry publishes no personal value and that the field list carries only the PDPA tag |

The identity scheme behind the document's security definition is the platform one: a user JWT from gateway-bff plus workload identity (Architecture v5 slide 11). No credential and no personal name appears in the document or a fake.

### 11. Data

The contract schema is the published product page and catalog. The ACE property types below are copied from the E1001 sys_fields baseline in Physical Schema v9; they describe source metadata, not separate record endpoints.

| Schema item | Property | Type / rule | Source |
|---|---|---|---|
| Record query | productCode | string matching ^DP(0[1-9]\|1[0-4])$ | RD-P1-005 |
| Record query | caseId | required UUID for rwb_case.recovery_case.id | RD-P1-023 |
| Record query | page | integer; min 0; default 0 | RD-P1-005 |
| Record query | size | integer; min 1; default 50; max 200 | RD-P1-005 |
| DataProductRecordPage | items, freshness, page, size, total | items is DataProductRecord[]; page, size and total are integers; freshness uses published DataProductFreshness | API Specification v7 |
| DataProductRecord | recordId, entity, fields | recordId and entity are strings; fields is FieldValue[] | API Specification v7 |
| FieldValue | fieldName, value, masked | fieldName string; value is string in current v7; masked boolean. Encoding non-TEXT source types is Pending, owner API specification owner, tracked as DOR-RWB-P1-E1016-CON-7 | API Specification v7; RD-P1-005 |
| DataProductCatalogEntry | productCode, productName, definition, ownerRole, systemOfRecord, sourceViews, reconciliations, access, refreshCycle, expectedBy, retentionClass, fields | Strings except arrays; access is {capabilityArea: string, right: string}; no roleCode, canRead or accessVersion | RD-P1-005 |
| DataProductField | entity, fieldName, fieldId, dataType, isPersonal | Strings except isPersonal boolean | API Specification v7 |

A DP02 contact row is a `DataProductRecord` with the fields `contactKey`, `contactType`, `consentStatus` (GIVEN, WITHDRAWN or UNKNOWN) and `verifiedAt`, and no contact value, address, name or identity number (rwb-source-data.yaml 5.1.0; built by RWB-P1-E2021-APP). This contract publishes no `ContactRecord` and no entry-candidate operation. A contact value, name or address is read only through `GET /customers/{personKey}` (RD-P1-060), built by RWB-P1-E1069-APP and masked by `FieldMasker`.

| Consumed or handled item | Members | Source |
|---|---|---|
| Authorise request | header `Idempotency-Key` (uuid); capability area, right, `productCode`, `caseId` (uuid), `fieldIds`, case attributes (owner, team, region), access resolution (access version, role codes, valid-from date). Provider property names pending (GAP-3322). These inputs describe the local fake semantics | rwb-access.yaml 5.1.0; RD-P1-063 |
| Authorise answer | Assert allow or deny and the Problem `messageCode` in the provider contract tests. P1 masking fixtures may carry local marker and version values pending the provider properties (GAP-3322) | rwb-access.yaml 5.1.0; RD-P1-063 |
| Access-load row | `product_code`, `role_code`, `can_read`, `access_version`, `valid_from`, `valid_to` | Physical Schema v9; RD-P1-020 |

Use the E1001 baseline in Physical Schema v9, file `rwb_source_data.sql`, as the field contract. Select the `sys_fields` seed rows for the `v_ace_*` views behind the served products; the data-product mapping identifies those views. For each field use `field_id`, `object_name`, `field_name`, `data_type`, `physical_type` and `is_personal` from the same seed row. These rows are the source for the field metadata used by AC2.

Pending: whether the catalog read model filters data products by data_product.valid_from, owner data architect, tracked as GAP-3440. The catalog contains only the published properties above and does not expose story-only properties.
### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base /api/recovery/source-data/v1. This E1016 contract slice specifies two operations.

| Method | Path | Request | Response | Access |
|---|---|---|---|---|
| GET | /data-products/{productCode}/records | productCode pattern ^DP(0[1-9]\|1[0-4])$; required caseId UUID; page min 0 default 0; size min 1 default 50 max 200 | DataProductRecordPage with FieldValue[] (fieldName, value, masked) | Case record R and an active data_product_access row |
| GET | /admin/data-products | optional product query | DataProductCatalogEntry[] with sourceViews, reconciliations string[], access {capabilityArea,right}, and P5 retention class | Platform administration R |

P1 serves records only for DP01, DP02, DP04, DP05, DP06, DP07, DP11 and DP13 (RD-P1-021). Requests for DP03, DP08, DP09, DP10, DP12 or DP14 return 400 E400 with the owning service in detail. Pending: unsupported-product message ID, owner product owner and Error Standard owner, tracked as GAP-3272. Pending: DP14 records availability, owner rwb-ace-data service owner, tracked as GAP-3281. caseId is the UUID rwb_case.recovery_case.id; RW-YYYY-NNNNNN is display-only (RD-P1-023). Responses use the Problem schema in RD-P1-004. `rwb-source-data.yaml` 5.1.0 (API Specification v7) is the one publication artifact and already carries the required `caseId`, the paging bounds, `FieldValue[]` and the catalog properties; the 422 of the records operation is requested from its owner. Statuses: records 200, 400, 401, 403, 404, 422, 503; catalog 200, 400, 401, 403, 503. The catalog `access` block is the capability of the records operation (`Case record`, `R`). Pending: the stored source of `reconciliations`, owner data steward, GAP-3446; sort order and the unit of `total`, owner API specification owner, GAP-3444.

The four ACE-specific reads are not part of this story's contract content. `GET /payments` is built by RWB-P1-E1013-APP and published through RWB-P1-E1015-CON (RD-P1-061). `GET /customers/{personKey}`, `GET /accounts/{accountKey}` and `GET /collateral/{assetKey}` are operations of rwb-source-data.yaml 5.1.0 built by RWB-P1-E1069-APP, with right Case record R and masking by policy (RD-P1-060).

#### 12.2 REST operations and interfaces consumed

| Method / interface | Path / contract | Owner | Use and budget |
|---|---|---|---|
| POST | /api/recovery/access/v1/authorise | rwb-access (P4) | Once per records read with a new `Idempotency-Key`; members in section 11. Published in rwb-access.yaml 5.1.0; provider property names pending (GAP-3322). One hop, 2 s, no retry, no stale cache. 403 and 404 passed on; anything else unsuccessful is 503 Interim (RD-P1-063): consumers test against the P4 fake and assert allow or deny and the Problem `messageCode` only, never a role or scope value the provider has not published. |
| GET | /api/recovery/access/v1/admin/roles | rwb-access (P4) | `Role.roleCode`, to validate an access load; rwb-access.yaml 5.1.0. Pending: the handler's identity and permission, GAP-3447. 2 s; failure fails the apply |
| Library | `AccessGuard`, `FieldMasker` | rwb-access (P4), RWB-P4-E1037-CON | Catalog right check; rendering of the markers |
| GET | /api/recovery/case/v1/cases/{caseId}, /accounts, /parties | rwb-case (P3) | Case attributes (`ownerUserId`, `teamCode`, `regionCode`), `accountKey`, `personKey`; Case record R; rwb-case.yaml 5.1.0; 2 s each; 404 passed on |
| GET | /api/recovery/document/v1/retention-classes?productCode= | rwb-document (P5) | `RetentionClassPage` (RWB-P5-AD021-CON); Documents R; 2 s; failure is 503. Pending: product-code mapping and the value with no class or several, GAP-1028; not in rwb-document.yaml 5.1.0 |
| Library | PII access log of ACE Common (INT-22) | ACE Common | One entry per personal read: user, product, case UUID, field names, time; failure is 503. Pending: the call's time limit and the refusal log, GAP-3442 |

**Reference-load handler (RD-P1-020).** rwb-case's reference-load pipeline delivers an approved version of table code `data_product_access` to the P1 handler. The handler checks known product, known role, one row in force per product and role on any date and no back-dating; it applies the whole version in one transaction, sets `valid_to` of replaced rows to the day before the new `valid_from`, and is idempotent on (table code, version). A refusal carries MSG-P1-002 with the failed check and changes nothing. Load states and approver are rwb-case's; P1 has no load-state table. Pending: the transport and message shape of the handler, GAP-3338.

#### 12.3 Events published

None by this capability.

#### 12.4 Events consumed

None. Approved reference loads reach the P1 handler through the reference-data pipeline.

#### 12.5 Workflows and activities

None.

#### 12.6 Schedules

None.

#### 12.7 Tables owned

| Table / view | Owner | Contract use |
|---|---|---|
| data_product, data_product_access, sys_objects, sys_fields | P1, rwb_source_data | Catalog and product access metadata |
| v_data_product_catalog | P1, rwb_source_data | Read model built by RWB-P1-E1016-DB |
| party_ext, contact_point_ext, account_ext, valuation_ext | P1, rwb_source_data | Record sources only for products mapped to these tables |
| recovery.v_ace_* views | P1 read path | ACE source fields only for products in RD-P1-021 |

No P3, P4 or P5 table appears in a schema or query. Case facts, roles, masking and retention use owner contracts.

#### 12.8 Contract fakes

**Provider fakes (RD-P1-011).**

| Fake | Operations | Version and fixtures |
|---|---|---|
| `fakes/rwb-source-data/5.1.0/` | `getDataProductsProductcodeRecords`, `getAdminDataProducts` | Equal to rwb-source-data.yaml 5.1.0; one WireMock mapping per declared status; a DP02 page with a customer row and a contact row; the DP01 catalog entry |

**Consumed fakes.**

| Fake | Required behavior |
|---|---|
| P4 authorise fake | allowed true for RW-AUDIT and RW-COMPLY on DP02 (all masked; one clear), allowed false, 400 without `Idempotency-Key`, 403, 404, 503, timeout |
| P4 role-list fake | `Role` array with `roleCode` (rwb-access.yaml 5.1.0); timeout |
| Guard and `FieldMasker` fake | Catalog right allowed and refused; unavailable error |
| rwb-case fake | The three reads: in scope, another owner, 404, timeout |
| P5 retention fake | One class per product; timeout |
| ACE Common PII log fake | Accepts; rejects every write |
| Reference-load handler fixture | Accepted, refused (unknown role, overlap, back-dated) and re-delivered versions |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided; consumed: authorise, role list, three rwb-case reads, retention (6) | One hop and 2 s for runtime calls; the P3 reference pipeline invokes the P1 handler |
| Library | Guard and `FieldMasker`; PII access log (2 consumed) | In process |
| Kafka | None | None in this capability |
| Temporal | None | None |
| File | None | None |

### 13. Solution plan

**Deliverable.** Update the API Specification v7 publication artifact rwb-source-data.yaml for the two E1016 operations and shared schemas. Do not publish a competing OpenAPI file. Contract fakes mirror the published contracts. The artefact form is OpenAPI only; no Java read interface of this service is distributed, and consumers use REST (the P1 internal view reader stays inside P1). A REQUEST to the API specification owner asks for the 422 on the records operation and for `FieldValue.value` typing.

**Compatibility rule.** Major version 1 is additive. A breaking change requires a new major version and base path; this story defines no status-transition API.

**Build steps**

1. Check GET /data-products/{productCode}/records against RD-P1-005 and RD-P1-021, including UUID, productCode pattern, paging, FieldValue[] and unsupported-product handling.
2. Check GET /admin/data-products against the published catalog shape: sourceViews, reconciliations string[], access {capabilityArea,right}, and retention via P5.
3. Map errors to the Problem schema of RD-P1-004 and Error and Message Standard v6.
4. Document the consumed contracts and the handler of section 12.2 with owners, budgets and pending gaps.
5. Publish the provider fake and the consumed fakes of section 12.8; record consumer sign-off.
6. Run the Test Cases v9 rows of section 16; legacy rows remain regression evidence only.

### 14. Validation and messages

| ID | HTTP / condition | Text |
|---|---|---|
| MSG-GEN-001 | 400 required value missing or `caseId` not a UUID | Enter {field}. |
| MSG-GEN-002 | 422 `page` or `size` out of range | Text of Error and Message Standard v6 |
| MSG-GEN-007 | 400 unknown product code; 404 unserved major version | Text of Error and Message Standard v6 |
| MSG-P4-001 | 401 caller has no Recovery Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | 403 missing right or active access row | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | 404 case outside caller scope | This case is not in your scope. |
| MSG-P1-002 | Reference version rejected | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-003 | Catalog row has invalid system-of-record / owner cardinality | {product} must have exactly one system of record and one named owner. |
| MSG-GEN-006 | 503 authorise, rwb-case, role list, PII log, ACE view or retention unavailable; `detail` names which | {system} is not available. Try again in a few minutes. |
| E400 | 400 product not served by P1 | Problem detail names the owning service; message ID Pending under GAP-3272. |

The published Problem schema requires type, title, status, messageCode and traceId (RD-P1-004). The owning service stamps instance with the request path and trace ID. detail and messageTh are optional. Include field only for an input failure and errors only on 400 or 422 when multiple inputs fail. Pending: the values of {action} and {system} per operation, owner product owner with the Error and Message Standard owner, GAP-3449.
### 15. Screens and states

The contract serves two screens and one administration view. SCR-03 Case record (Read only; loading, refused, ready; empty, error and no access: Not specified in the source documents (CG-ALL-2171)) shows the product data the role may read, with personal fields masked, through the gateway-bff composite route (DP-19). The catalog entry is read by the administration screen of RWB-P1-E1064-APP through `GET /admin/data-products` (loading, empty, list, refused). SCR-47 Personal data reads masking rules from rwb-access in Epic 8 and is not served here. Its states empty, loading, error and no access are Not specified in the source documents (CG-ALL-2172). The composite route specification and the screen field list are the platform edge story's; this document fixes the service side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1016-CON-27 | Legacy regression: catalog regression only | Contract | The two interfaces and the read schemas are published (new, D-RCV-60) |
| TC-P1-E1016-CON-01 | AC1, AC2, AC4 | Contract | The records operation enforces the final product and query contract |
| TC-P1-E1016-CON-02 | AC3 | Contract | Errors use the published Problem shape and Error and Message Standard v6 text |
| TC-P1-E1016-CON-04 | Legacy regression: out-of-scope regression only | Contract | No masking or role field of another service appears in a schema (new, D-RCV-60) |
| TC-P1-E1016-CON-05 | AC6 | Contract | Contract fakes match the interfaces they represent |
| TC-P1-E1016-CON-06 | AC7 | Contract | Major version changes follow the compatibility rule |
| TC-P1-E1016-CON-10 | AC2, AC7 | Contract | Records and catalog schemas match their published shapes |
| TC-P1-E1016-CON-13 | BR1 to BR5, BR7; the REST base, the event rule, the error envelope, the schema change rule and the no-business-value rule, checked on the document | Contract | BR1 to BR5, BR7; the REST base, the event rule, the error envelope, the schema change rule and the no-business-value rul |
| TC-P1-E1016-CON-16 | AC4 | Contract | Consumed contracts name their owner, payload status and budget |
| TC-P1-E1016-CON-17 | AC5 | Contract | No foreign service table is part of a P1 schema |
| TC-P1-E1016-CON-20 | AC10 | Contract | The provider fake serves both operations |
| TC-P1-E1016-CON-21 | AC11 | Contract | The consumed authorise contract matches the provider story |
| TC-P1-E1016-CON-22 | AC12 | Contract | Each operation refuses a call without a session |
| TC-P1-E1016-CON-23 | AC13 | Contract | The DP02 contact row carries no contact value |
| TC-P1-E1016-CON-24 | AC14 | Contract | The access-load handler contract refuses and replays as stated |
| TC-P1-E1016-CON-25 | AC15 | Contract | Each dependency failure has one answer |
| TC-P1-E1016-CON-26 | AC16 | Contract | Unknown product code and paging limits are stated |

TC-P1-E1016-CON-27 and TC-P1-E1016-CON-04 are legacy regression evidence only. The criteria are covered by the other rows above, on synthetic UUID 00000000-0000-4000-8000-000000000102, DP02 and DPA-2026.11.

Review checklist (not test cases): (1) trace every section 8 rule to an AC or guardrail; (2) check all nine section 12 subsections and ownership; (3) compare API Specification v7 and the story for drift; (4) verify each request row has a consumer owner and pending payload gap where needed.
### 17. Guardrails

- No business value in the contract: the roles, the products, the access rows and the masking rules stay data; the document carries codes and enums only.
- No personal data in an example, a fake or an event schema: records carry `id_no_masked` and `id_no_last4`, never a clear identity number; a DP02 contact row carries no contact value; every example is synthetic.
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: the document declares the views as this service's read path and no other service's table anywhere (DP-05, DP-01).
- No cross-schema read and no cross-schema key: no property of the document is sourced from `masking_rule`, `role`, `permission` or `retention_rule`, and none carries a foreign key to another schema.
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- The error envelope and the naming rule come from the platform library; this story narrows them but never redefines them.
- A fake that drifts from the document fails the build, and a property added from another service's table fails the ownership check.

### 18. Traceability

| Requirement ID | Requirement | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-010 | Access per data product by role; personal fields masked | Records operation, authorise and the markers | TC-P1-E1016-CON-01, TC-P1-E1016-CON-02, TC-P1-E1016-CON-05, TC-P1-E1016-CON-06, TC-P1-E1016-CON-10, TC-P1-E1016-CON-16, TC-P1-E1016-CON-17, TC-P1-E1016-CON-20 to TC-P1-E1016-CON-26 |
| REQ-RDF-011 | Catalog entry with definition, owner, system of record, refresh and retention | Catalog schema and GET /admin/data-products | TC-P1-E1016-CON-01, TC-P1-E1016-CON-02, TC-P1-E1016-CON-05, TC-P1-E1016-CON-06, TC-P1-E1016-CON-10, TC-P1-E1016-CON-16, TC-P1-E1016-CON-17, TC-P1-E1016-CON-20 to TC-P1-E1016-CON-26; legacy regression TC-P1-E1016-CON-27 |
| REQ-ACA-006 | Personal reads logged and refused when logging fails | PII logging behavior and Problem mapping | TC-P1-E1016-CON-01, TC-P1-E1016-CON-02, TC-P1-E1016-CON-05, TC-P1-E1016-CON-06, TC-P1-E1016-CON-10, TC-P1-E1016-CON-16, TC-P1-E1016-CON-17, TC-P1-E1016-CON-20 to TC-P1-E1016-CON-26 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Consumed contracts in 12.2 | Review checklist; TC-P1-E1016-CON-21, TC-P1-E1016-CON-22 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1016-APP | App development | Implements this contract against its fakes |
| RWB-P1-E1016-DB | ACE DB | Provides the indexes, read model and seven-row seed |
| RWB-P1-E1069-APP | App development | The views the records operation reads |
| RWB-P1-E1013-APP | App development | Builds `GET /payments`, published through RWB-P1-E1015-CON; outside this contract |
| RWB-P1-E2021-APP | App development | Builds the DP02 contact-and-consent rows of the records operation |
| RWB-P4-E1016-APP | App development | Answers the data-product half of `POST /authorise` |
| RWB-P4-E1037-CON | Contract | Guard library and `FieldMasker` dependencies |
| RWB-P3-E1043-CON | Contract | Reference-data pipeline invoking the P1 apply handler |
| RWB-P5-AD021-CON | Contract | Retention-class dependency |
### 19. Out of scope

- Implementation of the product access check, record reads and catalog service: RWB-P1-E1016-APP.
- Indexes, read model, seven seed rows and schema checks: RWB-P1-E1016-DB.
- Four ACE-specific read operations: `GET /payments` is RWB-P1-E1013-APP's with RWB-P1-E1015-CON; the other three are RWB-P1-E1069-APP's (RD-P1-060).
- Authorise, role list, masking rules and FieldMasker behavior: rwb-access (P4).
- Reference-load approval and transport: rwb-case (P3); this contract defines only P1's apply handler behavior.
- The case reads themselves: rwb-case (P3).
- Retention rule and records: rwb-document (P5).
- Message ID for unsupported-product E400: Pending under GAP-3272; DP14 availability Pending under GAP-3281.

### 20. Remaining delivery steps

- Size: Not specified; owner P1 delivery lead.
- EP01 design sign-off: Pending; owner product owner.
- 422 on the records operation and the retention path in `rwb-document.yaml`: Pending; owners API specification owner and rwb-document service owner (REQUEST).
- Publish the authorise request and answer property names and confirm the fake version, owner rwb-access service owner, GAP-3322.
- sort order and total (GAP-3444), reconciliation list source (GAP-3446), role-call identity (GAP-3447), refusal log (GAP-3442), message placeholders (GAP-3449), handler transport (GAP-3338): Pending; owners as stated where each is named.
- Retention class mapping: Pending; owner rwb-document service owner, GAP-1028.
- FieldValue.value encoding for non-TEXT source types: Pending; owner API specification owner, DOR-RWB-P1-E1016-CON-7.
- Unsupported-product E400 message ID: Pending; owner product owner and Error Standard owner, GAP-3272.
- Test data in DEV: Pending; owner QA lead.
- RWB-P1-E1016-CON Done and consumer sign-off: Pending; owner contract owner.
