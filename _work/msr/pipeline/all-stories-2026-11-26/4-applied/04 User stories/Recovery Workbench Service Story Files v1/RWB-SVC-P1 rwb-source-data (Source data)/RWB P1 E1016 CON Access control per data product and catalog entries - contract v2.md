# RWB-P1-E1016-CON Access control per data product and catalog entries

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

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
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-004, FR-P1-006, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-026, FR-P1-027, FR-P1-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-016 for rwb-source-data. The contract of the access-control and catalog capability is published on Day 1 so the app story and every consumer of the service's read surface build against a fixed shape: six GET operations on `/api/recovery/source-data/v1`, the `AceSourceRead` and `DataProductCatalog` interfaces, the error envelope and the read schemas; the authorise and masking answers are consumed, never redefined (DP-08, DP-11; Architecture v5 slides 11, 15 and 41). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-E1016-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of rwb-source-data for the access-control and catalog capability: an OpenAPI 3.1 document for the six read operations, the `AceSourceRead` and `DataProductCatalog` interfaces with their read schemas, the error envelope, the versioning rule, the contract tables of section 12 and the fakes of the three contracts this capability consumes**, so that **the app and DB stories of this legacy key and the consuming teams build in parallel from Day 1 without waiting for the service to be built**.

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

1. Draft the OpenAPI 3.1 document for the six read operations, with the shared components used across the service's other operations.
2. Draft the `AceSourceRead` interface and its read records: the customer, account, collateral and payment reads over the views.
3. Draft the `DataProductCatalog` interface and its records: the product record page and the catalog entry, including the field list with PDPA tags and the access block.
4. Agree the error envelope and map each HTTP status and refusal to its message ID.
5. State the versioning rule for the REST surface; state that the capability publishes no event and starts no workflow or schedule.
6. Publish the contract tables of section 12 (nine sub-tables) and the three fakes.
7. Add the contract tests: schema validation, error mapping, the fake-to-document comparison and the masking shape.
8. Tag the baseline and hand it to RWB-P1-E1016-APP, RWB-P1-E1016-DB and every consuming team.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request body or query fails schema validation | 400 with the error envelope and the failing pointer | MSG-GEN-001 | AC3 |
| X2 | A caller without the Case record right, or without an access row | 403 with the error envelope and MSG-P4-002 | MSG-P4-002 | AC3 |
| X3 | A case outside the caller's scope | 404 with the error envelope and MSG-P4-003 | MSG-P4-003 | AC3 |
| X4 | A required field of a response schema is missing from the source material | The field carries the placeholder and one gap row is carried | None | AC2 |
| X5 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X6 | A schema declares a masking or role field owned by another service | The contract test fails on the ownership check | None | AC5 |
| X7 | A caller asks for a major version the service does not serve | 404 with the error envelope and the served major versions | None described in the sources | AC7 |

The business messages MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P1-002, MSG-P1-003 and MSG-GEN-006 keep their text from the legacy story and are carried unchanged in the envelope mapping; MSG-GEN-001 is the missing-field message of the legacy catalog read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map v1 and the target architecture only |
| Negotiable | Field-level detail is settled with the consumers; the operations, the interfaces, the envelope and the naming are fixed by the target architecture |
| Valuable | Unblocks the app and DB stories of this legacy key and every consumer of the service's read path on Day 1 |
| Estimable | One OpenAPI document, two interfaces, one error envelope, two rules, nine contract tables, three fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Access control and catalog contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the Ownership Map v1 names P1 as the owner of data_product, data_product_access, sys_objects, sys_fields, sys_field_version and data_contract

  Scenario: AC1 The OpenAPI 3.1 document describes the six read operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-source-data is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/source-data/v1
    Then it declares GET /customers/{id}, GET /accounts/{id}, GET /collateral/{id}, GET /payments?accountId=, GET /data-products/{productCode}/records and GET /admin/data-products with the owner rwb-source-data
    Then every operation names its security right and its error responses 400, 401, 403, 404 and 503
    Then the two administration-free reads are the only operations of the capability and no other service's path is declared

  Scenario: AC2 The two interfaces and the read schemas are published (new, D-RCV-60)
    Given the published Java contract of rwb-source-data
    When the AceSourceRead and DataProductCatalog interfaces are reviewed
    Then AceSourceRead declares the customer, account, collateral and payment reads over recovery.v_ace_* and returns typed records
    Then DataProductCatalog declares the product record page and the catalog entry and returns typed records
    Then the customer record carries id_no_masked and id_no_last4 and no clear identity number field
    Then the contact record carries contact_value and contact_value_masked and no unmasked flag owned by another service
    Then the catalog entry carries productCode, ownerRole, systemOfRecord, refreshCycle, expectedBy, retentionClass, fields with their PDPA tags, the reconciliations and the access block
    Then a field the sources do not define carries the placeholder and one gap row

  Scenario: AC3 The error envelope is one shape for every failure (new, D-RCV-60)
    Given the error envelope component of the document
    When a 400, 401, 403, 404 or 503 response is produced
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then a missing caseId answers 400 with MSG-GEN-001
    Then a caller without the right or without an access row answers 403 with MSG-P4-002
    Then a case outside the caller's scope answers 404 with MSG-P4-003
    Then a failed PII access log answers 503 with MSG-GEN-006

  Scenario: AC4 The consumed contracts are documented with their budgets (new, D-RCV-60)
    Given the consumed table of the document
    When the authorise operation, the FieldMasker interface and the reference-data operation are reviewed
    Then POST /api/recovery/access/v1/authorise is documented as owned by rwb-access with one hop, a 2 s timeout and no stale cache
    Then the FieldMasker interface is documented as a library call of rwb-access with mask and isUnmasked
    Then the reference-data operation is documented as owned by rwb-case, with rwb-source-data as the handler for table code data_product_access
    Then the P5 retention read of the catalog entry is documented with its one hop and 2 s budget

  Scenario: AC5 No masking or role field of another service appears in a schema (new, D-RCV-60)
    Given the schemas of the document
    When the ownership check runs over every property name
    Then no schema declares masking_rule, role_code of masking_rule, permission or role of rwb-access
    Then no schema declares a retention_rule property
    Then the masking of a personal field is described by the answer marker of the authorise operation, never by a rule value
    Then a property added from another service's table fails the check and the merge is blocked

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map v1
    Then the three fakes answer every path and payload of 12.2 and 12.8
    Then the contract tests compare each fake with the document and fail on any drift
    Then 12.3, 12.4, 12.5 and 12.6 state None and the document declares no event, workflow or Schedule

  Scenario: AC7 The naming and the versioning rule are stated and enforced (new, D-RCV-60)
    Given the document declares major version 1 in the path of /api/recovery/source-data/v1
    When a caller uses an unsupported major version
    Then the service answers 404 with the error envelope and the served major versions
    Then the document names schema and login rwb_source_data, topic rwb.source-data.events.v1, task queue rwb-source-data in namespace rwb-recovery and the Java package of the service
    Then a schema change is additive within major version 1 and a breaking change is a new major version
    Then no operation of the document carries a monolith base path
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 |
| BR2 | Event names would be `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`; this capability publishes none | DP-14; Template and Rules §R4 |
| BR3 | Every read of a personal field is answered from the authorise and masking answer of rwb-access; the contract carries a marker, never a rule value | DP-08; CTL-11 |
| BR4 | Error responses use one envelope and one message ID per condition; business message texts are copied unchanged from the legacy story | Template and Rules §R7.2 s14 |
| BR5 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 11 |
| BR6 | The document lists only operations owned by rwb-source-data; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR7 | No business value is fixed in the contract: the roles, the products, the access rows and the masking rules stay data | Template and Rules §R7.2 s17 |
| BR8 | The contract names no table of another service: the role, permission, masking and retention tables are reached through their owners' contracts | DP-01; Ownership Map v1 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The six operations, the two interfaces and the error envelope are described | In review |
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

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Customer read | `personKey`, `cifNo`, `firstName`, `lastName`, `dateOfBirth`, `deceasedFlag`, `idNoMasked`, `idNoLast4`, from `v_ace_customer` fields DF-ACE-055 to DF-ACE-074 |
| Contact read | `contactKey`, `personKey`, `contactType`, `contactValue`, `contactValueMasked`, `usageCode`, from `v_ace_contact` fields DF-ACE-075 to DF-ACE-083 |
| Account read | `accountKey`, balance, arrears and classification fields, from `v_ace_account` fields DF-ACE-001 to DF-ACE-042 |
| Collateral read | The collateral and asset fields of `v_ace_collateral` and `v_ace_asset`, fields DF-ACE-091 to DF-ACE-107 |
| Payment read | The payment fields of `v_ace_payment`, fields DF-ACE-043 to DF-ACE-054 |
| Product record page | `items` (record id, entity, field map with masked values), `freshness`, `page`, `size`, `total` |
| Catalog entry | `productCode`, `productName`, `definition`, `ownerRole`, `systemOfRecord`, `refreshCycle`, `expectedBy`, `retentionClass`, `fields` (entity, fieldName, fieldId, dataType, isPersonal), `reconciliations` (recCode), `access` (roleCode, canRead, accessVersion, validFrom) |

The exact field-level schema of the product record page and the catalog entry (types, lengths, required flags per property and the page and sort parameters) is Not specified in the source documents (GAP-0481; ASM-0673); this story fixes the field names above and leaves the field-level detail to the baseline review. The catalog entry carries no retention value of its own: the class is read through P5's contract and copied into the entry as a code.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13).

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/customers/{id}` | CustomerRecord, with `idNoMasked` and `idNoLast4` only | Authorise answer plus an access row for the product |
| GET | `/accounts/{id}` | AccountRecord with arrears, balance and classification | As above |
| GET | `/collateral/{id}` | CollateralRecord with its asset fields | As above |
| GET | `/payments?accountId=` | PaymentRecord[] for one account key | As above |
| GET | `/data-products/{productCode}/records` | API-P1-010: DataProductRecordPage, `caseId` required, `page` and `size` | Case record R plus an access row in force |
| GET | `/admin/data-products` | API-P1-011: DataProductCatalogEntry[], `product` optional | Platform administration R |

The full surface of the service is published in the service API file; this baseline documents the six operations of this capability and keeps the shared components reusable for the rest.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, right, scope, decision, matrix version, masking version and a marker per field ID; faked |
| (interface) | `FieldMasker` | P4 rwb-access | `mask(dto, session)` and `isUnmasked(fieldId, session)`; faked as a library |
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | The approved load for table code `data_product_access`; P1 provides the handler; faked |
| (interface) | P5 retention contract | P5 rwb-document | The retention class of a product for the catalog entry; faked |

#### 12.3 Events published

None. The topic `rwb.source-data.events.v1` and its two events belong to RWB-P1-E1013-APP; this capability publishes nothing on it.

#### 12.4 Events consumed

None. An access load arrives as reference data through a contract, and Architecture v5 slide 15 gives the service no consumed event.

#### 12.5 Workflows and activities

None. Every operation of this capability is synchronous; the task queue `rwb-source-data` is not used here.

#### 12.6 Schedules

None. No Temporal Schedule and no legacy Quartz job in this capability; JOB-04 reconciliation is RWB-P1-E1011-APP's (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| data_product | P1 (`rwb_source_data`) | Catalog entry: product code, name, definition, system of record, owner role, refresh cycle, expected-by |
| data_product_access | P1 (`rwb_source_data`) | Catalog access block and the access check |
| sys_objects, sys_fields | P1 (`rwb_source_data`) | Catalog field list, source system, source field and PDPA tag |
| sys_field_version, data_contract | P1 (`rwb_source_data`) | Named for the record shapes of the capability; no property is contracted from them beyond their IDs |
| v_data_product_catalog | P1 (`rwb_source_data`) | The read model the catalog operation reads; created by RWB-P1-E1016-DB |

No other table is named in the contract, and no table of another service is read (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-access WireMock | `POST /authorise` with a granted answer for RW-AUDIT, a granted answer for RW-COMPLY, a refused answer for DP06 and an out-of-scope answer | App story, contract tests |
| rwb-access `FieldMasker` stub | No rule in force for a field, one rule unmasking `contact_value` for RW-NOTICE, and an unavailable interface | App story, contract tests |
| rwb-case reference-data WireMock | An accepted load for table code `data_product_access`, one for `sys_objects`, a refused load naming an unknown role and a refused load marking a view "Workbench" | App story, contract tests |
| P5 retention stub | The retention class of each of the 14 products | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 6 provided, 3 consumed (1 operation, 2 interfaces) | The six reads; authorise, `FieldMasker` and the P5 retention read; the reference-data operation is consumed as a handler |
| Kafka | None | No event published or consumed by this capability |
| Temporal | None | No workflow, activity or Schedule |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-source-data-v1.yaml` (OpenAPI 3.1) with the six operations and the shared components, `contract/ace-source-read.yaml` and `contract/data-product-catalog.yaml` for the two interface schemas, `contract/error-envelope.yaml`, the versioning rule in the contract README, and the four fake mappings of 12.8.

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

DP-08 and DP-05 are the two patterns the contract exists for: the guard becomes an operation and the views become this service's read contract. DP-11 fixes the one hop and the 2 s budget on every consumed element; DP-07 and DP-19 are consumed by the app story, not here.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security definition, the error responses and the shared components; schema lint in the pipeline.
2. The six operations and their resources, with the field names of section 11; the field-level detail is agreed under the recorded gap.
3. `AceSourceRead` and `DataProductCatalog` interface schemas, with the read records and no property owned by another service.
4. Error envelope and the message-ID mapping, business texts copied unchanged.
5. The versioning rule and the statement that no event, workflow or schedule belongs to the capability.
6. The four fakes and their fixtures.
7. The seven contract tests; a drift between a fake and the document, or a property from another service's table, fails the build.
8. Baseline tag and the consumer sign-off note.

**Done when.** The document and the two interface schemas validate in the pipeline, the seven contract tests pass, the fakes answer every consumed path, and the app and DB stories of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | caseId or another required field is missing | Enter {field}. |
| MSG-P4-001 | No valid session | Your session has ended. Sign in again. |
| MSG-P4-002 | No right, or no access row for the product | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P1-002 | Access load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-003 | A catalog load marks a view with a system of record other than ACE | {product} must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner. |
| MSG-GEN-006 | PII access log, view or downstream contract unavailable | {system} is not available. Your request is queued and will be retried. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. Thai text for each message follows decision DL10.

### 15. Screens and states

The contract serves two screens and one administration view. SCR-03 Case record (Read only; loading, refused, ready) shows the product data the role may read, with personal fields masked, through the gateway-bff composite route (DP-19). The catalog entry is read by the administration screen of RWB-P1-E1064-APP through `GET /admin/data-products` (loading, empty, list, refused). SCR-47 Personal data reads masking rules from rwb-access in Epic 8 and is not served here. The composite route specification and the screen field list are the platform edge story's; this document fixes the service side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-016-01 | AC1, AC2, AC4; the granted read and the masked shape of AC1 of the app story | Contract | RW-AUDIT; case RW-2026-000102; the customer record with idNoMasked and idNoLast4 |
| TC-E1-016-02 | AC2; the catalog entry schema and the bag of fields that the read model of RWB-P1-E1016-DB fills | Contract | DP01 entry; six views and account_ext; DF-ACE-018; access block |
| TC-E1-016-03 | AC3; the 403 mapping of a role without an access row | Contract | RW-PHONECOL; product DP06 |
| TC-E1-016-04 | AC3, AC4, AC6; the refused load through the reference-data fake | Contract | Access load with role RW-UNKNOWN |
| TC-E1-016-05 | AC3; the 404 mapping of a case outside scope | Contract | RW-CASEOWN, case not owned; scope values Own |
| TC-E1-016-06 | AC3, AC5; the no-rule shape of a personal field | Contract | RW-COMPLY; no masking rule in force |
| TC-E1-016-07 | AC3; the 503 mapping when the PII access log fails | Contract | A fake that rejects every write |
| TC-E1-016-08 | AC3; the refusal of an access row not yet in force | Contract | Access row valid from 2026-12-15; business date 2026-12-14 |
| TC-E1-016-09 | AC1, AC3; the 403 of the catalog read for a role without Platform administration | Contract | RW-TRIBE calls GET /admin/data-products |
| TC-E1-016-10 | AC1, AC7; the statement that the service login reads the views and nothing in public, expressed as the contract's SQL view note | Contract | The 30 views; the login rwb_source_data |
| TC-E1-016-11 | AC2, AC7; 14 entries and the dictionary counts the entry restates | Contract | 30 views; 122 objects and 1,366 fields |
| TC-E1-016-12 | AC3, AC6; the refused catalog load that marks a view Workbench | Contract | A load setting v_ace_customer to Workbench |

The twelve legacy test case IDs of RWB-E1-016 are kept in order and character for character. This story owns no legacy acceptance criterion, so the Covers column names this story's new criteria only where the legacy case exercises the artefact in this story's title: the document, the interfaces, the envelope or a fake. The business behaviour of the legacy cases is proven by RWB-P1-E1016-APP against these fakes, and the schema facts by RWB-P1-E1016-DB. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the roles, the products, the access rows and the masking rules stay data; the document carries codes and enums only.
- No personal data in an example, a fake or an event schema: the customer record carries `idNoMasked` and `idNoLast4` and never a clear identity number; every example is synthetic.
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: the document declares the views as this service's read path and no other service's table anywhere (DP-05, DP-01).
- No cross-schema read and no cross-schema key: no property of the document is sourced from `masking_rule`, `role`, `permission` or `retention_rule`, and none carries a foreign key to another schema.
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- The error envelope and the naming rule come from the platform library; this story narrows them but never redefines them.
- A fake that drifts from the document fails the build, and a property added from another service's table fails the ownership check.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-010 | Access per data product by role through the views; personal data masked by role under PDPA | The product record read, the authorise operation, the `FieldMasker` interface and the access block of the catalog entry | TC-E1-016-01, TC-E1-016-03, TC-E1-016-05, TC-E1-016-06, TC-E1-016-08, TC-E1-016-09 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record, refresh and retention | The `DataProductCatalog` interface, the catalog entry schema and `GET /admin/data-products` | TC-E1-016-02, TC-E1-016-11, TC-E1-016-12 |
| REQ-ACA-006 | Every read of personal data is logged, and a read that cannot be logged is refused | The 503 mapping and the field-name-only audit note | TC-E1-016-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Every consumed element of 12.2 with its budget | TC-E1-016-04, TC-E1-016-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1016-APP | App development | The build that implements this baseline against its fakes |
| RWB-P1-E1016-DB | ACE DB | Sibling: the indexes, the read model and the access seed the catalog operation reads |
| RWB-P4-E1037-CON | Contract | Consumed: the authorise operation and the `FieldMasker` interface (DP-08) |
| RWB-P3-E1043-CON | Contract | Consumed: the reference-data contract that carries the access load (DP-07) |
| RWB-P1-E1001-APP | App development | Owns the tables behind the record shapes of this contract |

### 19. Out of scope

- The implementation of the access check, the record reads and the catalog entry (RWB-P1-E1016-APP).
- The indexes, the read model `v_data_product_catalog`, the access seed and the schema checks (RWB-P1-E1016-DB).
- The authorise answer, the masking answer and the masking rows: rwb-access (P4); they are consumed and faked here, never defined.
- The role to permission matrix and the role list: rwb-access (P4).
- The retention values and their rules: rwb-document (P5); only the class code crosses the contract.
- The operations of other services, including the freshness and business-day operations of the same base: their own stories.
- The gateway-bff composite route and the screen field list: the platform edge story and the screen owners (DP-19).
- The field-level completeness of the two new responses (GAP-0481; ASM-0673).
