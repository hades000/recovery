# RWB-P1-E1064-CON Data dictionary for the 14 data products

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-064 for rwb-source-data. The two published Java interfaces `DataDictionaryLoader` and `DataDictionaryQuery` become one REST read and one reference-table handler, so the interface of the dictionary is published before either is written: the five admin operations on base `/api/recovery/source-data/v1` (DP-13), their five schemas, the one error envelope, the reference-table handler contract for table code `sys_fields` (DP-11, DP-07), the versioning rule, the field-level source-system rule, the four fixture sets and the nine contract tables of section 12. The nine business rules and the eight legacy acceptance criteria stay with RWB-P1-E1064-APP and are carried here as regression evidence; this story owns the contract criteria only. It publishes documents, schemas and fakes and builds nothing: no table, no DDL, no migration and no deployment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P1-E1064-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-064 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-004, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-026, FR-P1-027, FR-P1-029) |
| Status | Draft (realignment v1) |

### 1. Story

As a **recovery developer and data steward**, I want **the five admin operations, their five schemas, one error envelope and the reference-table handler contract for table code `sys_fields` published with fakes**, so that **the dictionary slice builds against a fixed interface from Day 1 and a caller never imports a jar**.

This is the contract slice of legacy RWB-E1-064. It delivers:

- the OpenAPI 3.1 document of the five admin operations on base `/api/recovery/source-data/v1` (DP-13): `GET /admin/data-dictionary/fields`, `PATCH /admin/data-dictionary/fields/{fieldCode}`, `GET /admin/data-contracts`, `PATCH /admin/data-contracts/{contractId}` and `POST /admin/data-contracts/{contractId}/publish`, with the paths, the query parameters and the response field names of the API specification;
- the five schemas `DataDictionaryField`, `DataDictionaryFieldPage`, `DataDictionaryFieldChange`, `DataContract` and `DataContractConfirmation`, every property named character for character;
- the one error envelope of the service, the seven status codes the five operations answer and the message identifier each failure carries;
- the reference-table handler contract for table code `sys_fields`, which is what replaces the published `DataDictionaryLoader` interface: the shape of a load, the whole-load validation and the refusal in full (DP-11, DP-07);
- the versioning rule of a data contract and the field-level source-system rule, as rules the document states and the contract tests assert;
- the four fixture sets that stand in for the neighbouring stories, the drift rule that fails a build when a fixture leaves the document, and the nine contract tables of section 12 with their owners from the Ownership Map.

**It publishes documents, schemas and fakes only: no table, no DDL, no migration, no deployment.** The five tables `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` are created by the baseline of RWB-P1-E1001-APP in schema `rwb_source_data`; the 30 `recovery.v_ace_*` views are created by RWB-P1-E1069-APP in schema `recovery`. This story names both and creates neither. The implementation of the five operations and of the handler is RWB-P1-E1064-APP; the chart, the flag values, the migration step, the probes, the alerts and the runbook are RWB-P1-E1064-OPS.

### 2. Business rationale

Contract-first is the decoupling decision of the target (DP-11, ADR-020), and the dictionary is the worst place to skip it. In the monolith the definition of a field was reached in process through two Java interfaces, `DataDictionaryQuery` and `DataDictionaryLoader`, so every module compiled against the implementation and no caller could be tested until the implementation existed. In the target the dictionary is one service of 19 (Architecture v5 slide 41), three stories touch it, and the interface is the only thing that keeps them apart.

Fixing the interface first buys four things. The application story can build the two controllers and the two services against five schemas and a fake instead of against the seeded tables. The deployment story can wire alerts to message identifiers that already exist instead of inventing them at release time. The contract tests of this story fail on a drift between a document, a schema and a fixture before any of that code exists. And the one caller outside the service — the reference-data contract of rwb-case, which submits the governance load — gets a named handler for table code `sys_fields` instead of an imported jar (DP-07, DP-11).

**What D-RCV-60 changes.** The two legacy published interfaces become (i) a REST read on base `/api/recovery/source-data/v1` and (ii) the reference-table handler that the rwb-case reference-data contract calls (DP-11, DP-07; Architecture v5 slides 11 and 15). The dictionary itself stays P1's: it is the one place where a field, a number or a source column is resolved to a data product and an owner, and split across 19 schemas it would answer 19 ways (DP-01, DP-05; Architecture v5 slide 29). Parameters and reference data are P3's under the R-PREC default ruling (Template and Rules §R3), which is why the load is submitted through rwb-case's contract and lands in P1's tables.

Serves REQ-RDF-001 (14 data products, each with one system of record and one owner) and REQ-RDF-011 (catalog entry content). The measure of the contract is narrow and testable: every property of every operation is named in the document, every failure carries one of the agreed message identifiers, and a caller can answer all five operations and the handler from the fakes alone.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base path, the schema name, the topic name and the Java package follow the platform rule rather than a local choice.
- The per-service Flyway sequence rule is available (RWB-PLT-E1044-CON, DP-15), so the document names the sequence and its baseline instead of a monolith version.
- The reference-data contract of rwb-case is published (RWB-P3-E1043-CON, DP-07); where the source set of this run does not name its read path, the contract carries the placeholder and the reading of section 12.2.
- The API specification is the only source of the operation paths, the query parameters and the schema property names; no property is renamed to a local preference (API Specification v4, x-module P1).
- The Ownership Map is the only source for the owner of an object named in the contract; no object of another service is documented as this story's.
- The five tables and their 122 and 1,366 seed rows are the baseline of RWB-P1-E1001-APP, and the 30 `recovery.v_ace_*` views are RWB-P1-E1069-APP's; this contract describes both and creates neither (DP-01, DP-05, DP-15).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- The exact required flags and the lengths of the five schemas are not given by the API specification, which names the properties and their types only; they are Not specified in the source documents (GAP-0499; ASM-0691) and the contract fixes the names, the types and the format of each property.

### 4. Flow

1. Read the five operations from the API specification (API-P1-012 to API-P1-016) and fix the paths, the query parameters, the request bodies and the response bodies, character for character.
2. Write the OpenAPI 3.1 document on base `/api/recovery/source-data/v1`, with the five operations, their access rights (Reference data R for the two reads, Reference data U for the three writes) and their idempotency rule (`If-Match` on the two changes, `Idempotency-Key` on the publish).
3. Write the five schemas and the one error envelope, and map every failure to its message identifier (section 14).
4. Write the reference-table handler contract for table code `sys_fields`: the load it accepts, the whole-load validation of the six attributes, the source system and the view column, the refusal in full with the first failing check, and the apply in one transaction.
5. Write the versioning rule of a data contract and of a field definition: DRAFT, confirmed, PUBLISHED, and the new DRAFT version a change to a published contract opens.
6. Write the field-level source-system rule: a view field is ACE and names its column as `public.table.column`, or it is one of the 7 derived fields; every other field is Workbench.
7. Publish the four fixture sets and the drift rule that fails a build when a fixture answers a shape the document does not declare, or when the document declares a shape no fixture answers.
8. Write the nine contract tables of section 12, check every owner against the Ownership Map, tag the baseline and hand it to RWB-P1-E1064-APP, RWB-P1-E1064-OPS and the tests of this legacy key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document names a path, a query parameter or a property that the API specification does not | The contract test fails and names the property; the baseline is not tagged | None | AC1, AC2 |
| X2 | An operation is published without its request schema, its response schema or its access right | The contract test fails and names the operation | None | AC1, AC2 |
| X3 | The document carries a second error shape, or a failure without a message identifier | The contract test fails on the envelope | None | AC3 |
| X4 | The handler contract omits table code `sys_fields`, the whole-load refusal or the first failing check | The contract test fails and names the missing element | None | AC4 |
| X5 | A fixture answers a shape the document does not declare, or the document declares a shape no fixture answers | The contract test fails on the drift and the merge is blocked | None | AC5 |
| X6 | One of the nine contract tables is missing, or names an owner the Ownership Map does not give | The contract test fails and names the table | None | AC6 |
| X7 | A rule would let a published contract be edited in place, or let a version be overwritten | The contract test fails on the versioning rule | None | AC7 |
| X8 | The document lets a view field carry a source system other than ACE, or a table field carry ACE | The contract test fails on the source-system rule and names the field | None | AC8 |
| X9 | A field-level definition is missing from the source material | The property carries the placeholder, and one gap row and one assumption row are recorded for the whole story | None | AC2, AC4 |

X1 to X8 are the contract paths this story adds; X9 is the placeholder path of the run (Template and Rules §R9). This story has no run-time exception path of its own, because it has no run time: the failures the five operations answer are the envelope and the message mapping of AC3, and the failures the handler answers are the refusal contract of AC4.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the API specification, the platform libraries, the reference-data contract and the Ownership Map only |
| Negotiable | The required flags, the lengths and the format details are settled at the baseline review; the names, the paths, the schemas, the envelope and the handler shape are fixed by this story |
| Valuable | Unblocks the application, the deployment and the tests of this legacy key on Day 1, and gives the rwb-case reference-data contract a named handler |
| Estimable | One OpenAPI document, five schemas, one envelope, one handler contract, four fixture sets and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against an artefact: the document, a schema, a fixture, a table of section 12 — never against a built service |

### 7. Acceptance criteria

```gherkin
Feature: Data dictionary contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the base path of the service is /api/recovery/source-data/v1 and its schema is rwb_source_data

  Scenario: AC1 The document publishes the five admin operations on the service base (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the dictionary slice
    When it is reviewed against the API specification
    Then it publishes GET /admin/data-dictionary/fields with the query parameters product, entity, field, sourceSystem, page and size
    Then it publishes PATCH /admin/data-dictionary/fields/{fieldCode} with an If-Match header and a reason in the body
    Then it publishes GET /admin/data-contracts with the query parameters sourceSystem and status
    Then it publishes PATCH /admin/data-contracts/{contractId} with an If-Match header and the confirmation in the body
    Then it publishes POST /admin/data-contracts/{contractId}/publish with an Idempotency-Key header
    Then no operation sits outside the base /api/recovery/source-data/v1
    Then the two reads declare Reference data R and the three writes declare Reference data U

  Scenario: AC2 The five schemas carry every property of the API specification (new, D-RCV-60)
    Given the five schemas DataDictionaryField, DataDictionaryFieldPage, DataDictionaryFieldChange, DataContract and DataContractConfirmation
    When each schema is compared with the API specification
    Then DataDictionaryField carries fieldId, entity, fieldName, dataType, physicalType, mandatory, listCode, sourceSystem, sourceField, refreshCycle, ownerRole, lateBehavior, interfaceId, isPersonal, version and versionDate
    Then DataDictionaryFieldPage carries items of DataDictionaryField, page, size and total
    Then DataDictionaryFieldChange carries dataType, physicalType, mandatory, listCode, sourceSystem, sourceField, refreshCycle, ownerRole, lateBehavior, interfaceId, isPersonal and reason
    Then DataContract carries id, contractCode, sourceSystem, interfaceIds, contractVersion, status, fieldCount, confirmedByRole, confirmedOn, confirmationDocumentId, publishedAt and version
    Then DataContractConfirmation carries confirmedByRole, confirmedOn and confirmationDocumentId
    Then no property is renamed, added or dropped

  Scenario: AC3 One error envelope and one message identifier per failure (new, D-RCV-60)
    Given the error section of the document
    When each failure of the five operations is read
    Then every error response uses one envelope with the RFC 9457 problem members type, title, status, detail and instance
    Then the document declares 401, 403, 404, 409, 422, 428 and 503 and no other status
    Then a publish of a contract with no confirmation answers 409 with MSG-P1-021
    Then an empty reason or an empty confirmation field answers 422 with MSG-GEN-001
    Then a stale If-Match version answers 409 with MSG-GEN-004 and a missing If-Match answers 428 with MSG-GEN-004
    Then an unknown field or contract answers 404 with the text of MSG-P4-003
    Then an unavailable store answers 503 with MSG-GEN-006
    Then a refused load answers with MSG-P1-002 and names the first failing check

  Scenario: AC4 The reference-table handler contract for table code sys_fields (new, D-RCV-60)
    Given the reference-table handler contract of the document
    When it is reviewed against the legacy loader
    Then it names table code sys_fields and the caller as the reference-data contract of rwb-case
    Then it states the load it accepts: a load version, a valid-from date and the rows of the field
    Then it states the six attributes a row must carry and refuses the whole load when one is empty
    Then it refuses the whole load when a view field's source system is not ACE, when a table field's source system is not Workbench, or when a view field's source field is not a column of that view and is not one of the 7 derived fields
    Then it answers accepted or refused with the first failing check and no row written
    Then it applies an accepted load in one transaction, writes version 1 of each field and adds no endpoint to the service
    Then the service's own login is rwb_source_data and the credential a caller presents is Not specified in the source documents (GAP-0499; ASM-0691)

  Scenario: AC5 The four fixture sets answer every declared shape and drift fails the build (new, D-RCV-60)
    Given the dictionary fixture, the contract fixture, the reference-data fake and the delivered-baseline fixture
    When the contract tests compare each fixture with the document
    Then the dictionary fixture answers a page of fields with the 122 objects and the 1,366 fields, a single field, the 7 derived view fields, DF-ACE-018 and DF-ACE-204
    Then the contract fixture answers DC-ACE in DRAFT, DC-ACE confirmed on 2026-11-12 with DOC-SYN-0640, DC-ACE PUBLISHED at version 1, the DRAFT version 2 a change opens, and DC-ACE-2 with no confirmation
    Then the reference-data fake answers LOV-ROLE and the refresh-cycle list per table code, an empty list and a timeout
    Then the delivered-baseline fixture answers schema rwb_source_data with the five tables and schema recovery with the 30 views
    Then a fixture that answers a shape the document does not declare fails the build
    Then a shape the document declares with no fixture to answer it fails the build

  Scenario: AC6 The nine contract tables are complete and each names its owner (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed against the Ownership Map
    Then each of 12.1 to 12.9 is present
    Then every table named in 12.7 carries an owner from the Ownership Map and no other
    Then the 30 recovery.v_ace_* views are marked not created here
    Then the four fixture sets of 12.8 are the ones the contract tests use
    Then the summary of 12.9 agrees with 12.1 to 12.5

  Scenario: AC7 A published contract is never edited in place (new, D-RCV-60)
    Given contract DC-ACE is PUBLISHED at version 1
    When a field of DC-ACE changes and the document is read for the rule
    Then the rule opens DC-ACE version 2 as DRAFT
    Then version 1 stays PUBLISHED and in force until version 2 is confirmed and published
    Then the rule forbids a change to a published version in place
    Then the same rule keeps version 1 of a field readable when the field moves to version 2
    Then the publish of a version with no recorded confirmation is refused with 409 and MSG-P1-021

  Scenario: AC8 The field-level source-system rule holds for all 1,366 fields (new, D-RCV-60)
    Given the source-system rule of the document
    When it is applied to the 122 objects and the 1,366 fields
    Then 304 view fields carry source system ACE and 1,062 table fields carry source system Workbench
    Then 297 of the 304 view fields name an ACE column in the form public.table.column
    Then the 7 derived view fields v_ace_contact.contact_type, city, post_code and country and v_ace_plan.installments, recommended_installment and recommended_package carry source system ACE and no single ACE column
    Then 49 of the 1,062 table fields are the fields of the four extension tables party_ext, contact_point_ext, account_ext and valuation_ext
    Then a view field with a source system other than ACE is refused by the contract test
    Then a table field with source system ACE is refused by the contract test
```

The eight criteria are new and prove only the contract artefacts: the document, the five schemas, the envelope, the handler contract, the fixtures, the nine tables, the versioning rule and the source-system rule. No legacy criterion text is copied here; the eight criteria of RWB-E1-064 are owned by RWB-P1-E1064-APP and appear in this story only as regression test cases.

### 8. Business rules

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

**Where each rule is answered in the contract.** The nine rules are unchanged in text and in ID from RWB-E1-064. BR1 is answered by the `sourceSystem`, `sourceField`, `ownerRole`, `refreshCycle` and `lateBehavior` properties of `DataDictionaryField` and by the source-system rule of AC8. BR2 is answered by `DataDictionaryFieldPage` — `total` reports 1,366 fields over 122 objects, which is what the page of AC1 reads — and by the counts the dictionary fixture answers in AC5. BR3 is answered by the `sourceSystem` property and by the `data_product` row of 12.7, which holds one system of record and one owner role per product. BR4 is answered by the three confirmation properties of `DataContract` and `DataContractConfirmation` and by the 409 of MSG-P1-021 in AC3 and AC7. BR5 is answered by the `version` and `versionDate` properties and by the change reason `DataDictionaryFieldChange` requires. BR6 is answered by the handler contract of AC4, which carries the whole-load refusal of the legacy loader. BR7 is answered by the versioning rule of AC7. BR8 is answered by 12.7: the contract names the five tables, marks them created by the baseline and adds no DDL. BR9 is answered by the handler contract's rule that a load follows the view column and never edits an applied migration, and by the pair of the view migration on RWB-P1-E1069-APP's sequence and the row this contract describes.

### 9. State transitions

None of a case. The contract moves DRAFT → CONFIRMED → PUBLISHED, where CONFIRMED is the recorded confirmation of BR4 — the confirming role, the date and the stored document reference — and not a status value invented here: the legacy story names DRAFT and PUBLISHED, and the confirmed step is the condition the publish rule reads. Each field change adds a version; earlier versions stay readable.

| From | Event | Condition | To |
|---|---|---|---|
| Field version n | `PATCH /admin/data-dictionary/fields/{fieldCode}` | The `If-Match` version is current and a reason is given | Field version n+1; version n stays readable |
| Field version n | `PATCH /admin/data-dictionary/fields/{fieldCode}` | No `If-Match` version | Refused 428 with MSG-GEN-004; nothing is written |
| Contract DRAFT, no confirmation | `POST /admin/data-contracts/{contractId}/publish` | No confirmation is recorded | Refused 409 with MSG-P1-021; the contract stays DRAFT |
| Contract DRAFT | `PATCH /admin/data-contracts/{contractId}` | `confirmedByRole`, `confirmedOn` and `confirmationDocumentId` are recorded | DRAFT, confirmed — the publish is now allowed |
| Contract DRAFT, confirmed | `POST /admin/data-contracts/{contractId}/publish` | The confirmation is present | PUBLISHED at its version, in force |
| Contract PUBLISHED | A field of the contract changes | The change is accepted | The same contract opens version n+1 as DRAFT; the published version stays in force |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the document, the five schemas, the envelope and the four fixture sets; tags the baseline |
| Solution architect | Approves a change to the base path, a schema name or a new baseline |
| Data steward and data product owner (RW-DATASTEW) | Confirms that the five schemas carry every attribute the dictionary must publish (Reference data U) |
| Reference data administrator (RW-REFADM) | Confirms the load shape of the handler contract against the reference-data contract of rwb-case (Reference data C) |
| ACE team lead | Confirms the ACE read path the contract describes and the source column form `public.table.column` |
| rwb-case (P3) | Owns the reference-data contract that calls the handler for table code `sys_fields` and whose read path is the one consumed operation of 12.2 (DP-07) |
| rwb-access (P4) | Holds the roles and the rights as data and answers the authorise check behind the two access rights of 12.1 (DP-08, not in this story's pattern set) |
| No approval level from the delegation of authority applies | The story takes no business decision |

Every "who" in this table is a role code, never a person. The roles and their rights are held as data in rwb-access and reached through its authorise contract, not by a table read (DP-01).

### 11. Data

The contract declares shapes, names and rules, not business values. The five schemas are the ones of section 12.1 and their properties are these, character for character from the API specification.

**`DataDictionaryField`**

| Property | Type | Meaning and the value the legacy story gives |
|---|---|---|
| `fieldId` | string | The field ID, for example `DF-ACE-018` |
| `entity` | string | The object the field belongs to, for example `v_ace_account` |
| `fieldName` | string | The field name, for example `days_past_due` |
| `dataType` | string | The data type, for example `NUMBER` |
| `physicalType` | string | The physical type, for example `integer` |
| `mandatory` | boolean | Whether the field is required in its object |
| `listCode` | string | The list of values the field reads, for example `LOV-ROLE` for an owner role |
| `sourceSystem` | string | `ACE` or `Workbench` |
| `sourceField` | string | The ACE column of a view field, for example `public.account.delay_days`; empty for one of the 7 derived fields and for a Workbench field |
| `refreshCycle` | string | The refresh cycle, for example `DAILY` or `WEEKLY` |
| `ownerRole` | string | The owner role, for example `RW-DATASTEW` |
| `lateBehavior` | string | The behavior when the data is late, for example `Keep the previous value and mark DP01 stale` |
| `interfaceId` | string | The interface the field arrives on, where it has one |
| `isPersonal` | boolean | Whether the field is personal data |
| `version` | integer | The version of the definition, for example `1` or `2` |
| `versionDate` | date | The date of that version, for example `2026-11-18` |

**`DataDictionaryFieldPage`**

| Property | Type | Meaning |
|---|---|---|
| `items` | array of `DataDictionaryField` | The page of fields |
| `page` | integer | The page number requested, for example `1` |
| `size` | integer | The page size requested, for example `1` |
| `total` | integer | The total number of fields the filters match, `1,366` with no filter over `122` objects |

**`DataDictionaryFieldChange`**

| Property | Type | Meaning |
|---|---|---|
| `dataType` | string | The new data type |
| `physicalType` | string | The new physical type |
| `mandatory` | boolean | The new required flag |
| `listCode` | string | The new list of values |
| `sourceSystem` | string | The new source system |
| `sourceField` | string | The new ACE source column |
| `refreshCycle` | string | The new refresh cycle |
| `ownerRole` | string | The new owner role |
| `lateBehavior` | string | The new behavior when late, for example `Keep the previous value, mark DP01 stale and alert the data steward daily` |
| `interfaceId` | string | The new interface |
| `isPersonal` | boolean | The new personal-data flag |
| `reason` | string | The reason of the change, mandatory, for example `add the daily stale alert for DP01` |

**`DataContract`**

| Property | Type | Meaning and the value the legacy story gives |
|---|---|---|
| `id` | string | The identifier of the contract record |
| `contractCode` | string | The contract code, for example `DC-ACE` or `DC-ACE-2` |
| `sourceSystem` | string | The source system, for example `ACE` |
| `interfaceIds` | array of string | The read interfaces the contract lists, for example `V0002` and `V0003` |
| `contractVersion` | integer | The version, for example `1` or `2` |
| `status` | string | `DRAFT` or `PUBLISHED` |
| `fieldCount` | integer | The mapped fields, `304` for `DC-ACE` |
| `confirmedByRole` | string | The confirming role, for example `ACE team lead` |
| `confirmedOn` | date | The date of the confirmation, for example `2026-11-12` |
| `confirmationDocumentId` | string | The stored document reference, for example `DOC-SYN-0640` |
| `publishedAt` | date-time | When the version was published |
| `version` | integer | The optimistic-lock version the `If-Match` header carries |

**`DataContractConfirmation`**

| Property | Type | Meaning |
|---|---|---|
| `confirmedByRole` | string | The confirming role, mandatory |
| `confirmedOn` | date | The date of the confirmation, mandatory |
| `confirmationDocumentId` | string | The stored document reference, mandatory |

The five tables the schemas are stored in are `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` in schema `rwb_source_data`, created by the baseline of RWB-P1-E1001-APP (DP-01, DP-15); the contract names the five tables and their role in 12.7 and creates none of them. The required flags and the lengths of the five schemas are Not specified in the source documents (GAP-0499; ASM-0691); this story fixes the property names, the JSON types and the formats above and leaves the required flags and the lengths to the baseline review.

### 12. Contract

Base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-13, DP-14, DP-02, DP-15). This section is the contract this story publishes; it states what the service offers and what it consumes, and every artefact it names is a document, a schema or a fake, never a built object.

#### 12.1 REST operations provided

Five operations, all owned by P1 rwb-source-data (Ownership Map rows `GET /admin/data-dictionary/fields`, `PATCH /admin/data-dictionary/fields/{fieldCode}`, `GET /admin/data-contracts`, `PATCH /admin/data-contracts/{contractId}` and `POST /admin/data-contracts/{contractId}/publish`). Access is Reference data R for the two reads and Reference data U for the three writes.

| Method | Path | Purpose | Schemas | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/admin/data-dictionary/fields` | The paged field read with the filters `product`, `entity`, `field` and `sourceSystem`, returning `DataDictionaryFieldPage` (`items` of `DataDictionaryField`, `page`, `size`, `total`) | `DataDictionaryFieldPage`, `DataDictionaryField` | Reference data R | Idempotent by the query |
| PATCH | `/admin/data-dictionary/fields/{fieldCode}` | Changes a field definition with a reason and writes a new `sys_field_version` row | `DataDictionaryFieldChange` in, `DataDictionaryField` out | Reference data U | `If-Match` version; 428 without it, 409 on a stale version |
| GET | `/admin/data-contracts` | Lists the data contracts, filtered by `sourceSystem` and `status`, returning `DataContract[]` | `DataContract` | Reference data R | Idempotent by the query |
| PATCH | `/admin/data-contracts/{contractId}` | Records the confirming role, the date and the stored document reference of a contract | `DataContractConfirmation` in, `DataContract` out | Reference data U | `If-Match` version |
| POST | `/admin/data-contracts/{contractId}/publish` | Publishes a confirmed contract; a contract without a confirmation is refused | `DataContract` | Reference data U | `Idempotency-Key` header |

The document is `openapi/rwb-source-data-v1.yaml`, OpenAPI 3.1, with `/v1` in the path and one hop per call (DP-11, DP-13; Architecture v5 slide 11). Error responses are 401, 403, 404, 409, 422, 428 and 503 in the one error envelope of 12.3; a 404 on an unknown field or contract carries the text of MSG-P4-003.

#### 12.2 REST operations consumed

| Method | Path | Owner | Contracted use |
|---|---|---|---|
| GET | Not specified in the source documents (GAP-0499; ASM-0691); read as `/api/recovery/case/v1/reference-data/{tableCode}` | P3 rwb-case | The lists of values the field read and the governance load resolve, read as data per table code once and cached per call, never written as a constant; `ownerRole` is checked against LOV-ROLE and `refreshCycle` against its own list; one hop, 2 s timeout, no retry beyond the client default (DP-07, DP-11) |

The list read is the one consumed dependency of this contract. The load of 12.5 travels the other way round: rwb-case calls this service's reference-table handler for table code `sys_fields`, so the contract states a handler and not a path. The path of the list read is not in the source set, which is why it is the placeholder above and the assumption ASM-0691; the fake of 12.8 answers it with a list, an empty list and a timeout.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (Architecture v5 slide 15). A dictionary change, a confirmation and a publish are synchronous admin calls; this contract declares no outbox row, no event and no AsyncAPI document.

The error envelope of 12.1 is the one error shape the document declares: the RFC 9457 problem members `type`, `title`, `status`, `detail` and `instance`, with the message identifier of section 14 carried in the body. No operation answers a second shape.

#### 12.4 Events consumed

None. A dictionary change is a person's admin call and a load is a reference-load call; neither is started by an event, and Architecture v5 slide 15 gives the service no consumed event ("none: Airflow call; fallback polls ACE batch record"). The contract declares no consumer group.

#### 12.5 Workflows and activities

None. The five operations, the validation of a load and the version writes are synchronous steps. The activities `listEligibleAccounts` and `snapshot(page)` and the workflows `AceIngestCheck` and `reconciliation` on task queue `rwb-source-data` in namespace `rwb-recovery` belong to other P1 stories (Architecture v5 slide 15); this contract declares no workflow, no activity and no worker on that queue.

The **reference-table handler contract** is the one interface this story publishes outside REST: table code `sys_fields`, the caller the reference-data contract of rwb-case, an accepted load of a load version, a valid-from date and the rows of the field, the whole-load validation of the six attributes, the source system and the view column, the refusal in full with the first failing check and MSG-P1-002, and the apply in one transaction with version 1 of each field. It is a document the caller builds against and the service implements; it is not a path of this service and it is not a Temporal activity.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this contract: the dictionary is changed by a person and loaded by a governed reference load (DP-07; DP-10 is not in this story's pattern set).

#### 12.7 Tables owned

No table is created by this story. The objects the contract names, and their owners:

| Object | Schema | Owner (Ownership Map) | Contracted role |
|---|---|---|---|
| `sys_objects` | `rwb_source_data` | P1 | One row per object, 122 rows; read by the field read. Created by RWB-P1-E1001-APP, not here |
| `sys_fields` | `rwb_source_data` | P1 | One row per field, 1,366 rows; read and written through the handler of 12.5 and the field change of 12.1. Created by RWB-P1-E1001-APP, not here |
| `sys_field_version` | `rwb_source_data` | P1 | One row per accepted change, with its version and reason; written by the field change. Created by RWB-P1-E1001-APP, not here |
| `data_product` | `rwb_source_data` | P1 | The 14 products, their systems of record and their owner roles; read by the field read. Created by RWB-P1-E1001-APP, not here |
| `data_contract` | `rwb_source_data` | P1 | DC-ACE, its confirmation, its status and its versions; read and written by the three contract operations. Created by RWB-P1-E1001-APP, not here |
| `recovery.v_ace_*` (30 views) | `recovery` | View owner `ace_view_owner`; contract owner P1 rwb-source-data | **Not created here**: RWB-P1-E1069-APP creates the 30 views; this contract describes their 304 fields and the `public.table.column` form of their source field |

No DDL is added by this story, and no migration is published with it: the five tables and their read model `v_data_dictionary` are the baseline of RWB-P1-E1001-APP, the 30 views are RWB-P1-E1069-APP's, and this contract writes neither (DP-01, DP-05, DP-15). No table of another service is named as this story's and no foreign key crosses a schema.

#### 12.8 Contract fakes

| Fixture set | Serves | Shapes it answers |
|---|---|---|
| Dictionary fixture | The two dictionary operations of 12.1 | A page of fields with `page`, `size` and `total`, the 122 objects and the 1,366 fields, a single field, the 7 derived view fields, `DF-ACE-018` at version 1 and 2, `DF-ACE-204`, and the envelopes 404, 422 and 428 |
| Contract fixture | The three contract operations of 12.1 | `DC-ACE` in DRAFT with 304 fields and the interfaces V0002 and V0003, `DC-ACE` confirmed on 2026-11-12 with `DOC-SYN-0640`, `DC-ACE` PUBLISHED at version 1, the DRAFT version 2 a change opens, `DC-ACE-2` with no confirmation, and the envelopes 404, 409 and 422 |
| Reference-data fake | The consumed read of 12.2 and the handler of 12.5 | LOV-ROLE with and without the role a load names, the refresh-cycle list, an empty list and a timeout; a full load, a refused load and a repeated file for table code `sys_fields` |
| Delivered-baseline fixture | RWB-P1-E1001-APP and RWB-P1-E1069-APP | Schema `rwb_source_data` holding the five tables and the 1,366 seeded rows, and schema `recovery` holding the 30 views, so the counts of AC5 and AC8 are answered once and not against a copy |

A fixture that answers a shape the document does not declare fails the build, and a shape the document declares with no fixture to answer it fails the build. The fakes carry no production data and no personal value: the dictionary holds definitions, not values.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 5 operations on `/api/recovery/source-data/v1` | 1 operation, the rwb-case list read of 12.2 | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11, DP-13) |
| Kafka | None | None | The topic `rwb.source-data.events.v1` and its two events belong to RWB-P1-E1015-APP (DP-14) |
| Temporal | None | None | No workflow, activity or Schedule; queue `rwb-source-data` is not used by this contract |
| File | None | None | A load file arrives inside the reference-load request of the rwb-case contract and is never read from a store by this contract |
| Reference load | 1 reference-table handler (`sys_fields`) | 1 load submission through the rwb-case contract | The handler validates and applies in one transaction; the load is P3's operation and this service's rows (DP-07) |

### 13. Solution plan

**Deliverables**

| Artefact | Content |
|---|---|
| `openapi/rwb-source-data-v1.yaml` | The five operations of 12.1 on base `/api/recovery/source-data/v1`, their query parameters, their `If-Match` and `Idempotency-Key` rules and their access rights |
| The five schemas | `DataDictionaryField`, `DataDictionaryFieldPage`, `DataDictionaryFieldChange`, `DataContract` and `DataContractConfirmation`, with the properties of section 11 |
| The error envelope | The one RFC 9457 shape of 12.3, the seven status codes and the message identifier of each failure |
| `contract/reference-table-handler.md` | The handler contract of 12.5 for table code `sys_fields`: the load, the whole-load validation, the refusal in full and the one transaction |
| `contract/data-contract-versioning.md` | The versioning rule of AC7: DRAFT, confirmed, PUBLISHED, and the new DRAFT a change opens |
| `contract/field-source-rule.md` | The source-system rule of AC8: ACE with a `public.table.column` or one of the 7 derived fields, Workbench otherwise |
| Four fixture sets | `fixtures/dictionary/`, `fixtures/contracts/`, `fixtures/reference-data/` and `fixtures/baseline/`, with the shapes of 12.8 and the drift rule |
| The nine contract tables | Section 12, 12.1 to 12.9, each owner checked against the Ownership Map |
| The contract tests | The eight new cases of section 16, run in every build |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 and DP-07 are the subject of this contract: one published interface becomes one REST read, the other becomes one reference-table handler, and the load is submitted through rwb-case's contract. DP-01, DP-05, DP-13, DP-15 and DP-19 are named for completeness of the pattern set, because the application and the deployment implement them; this story fixes their names in the contract and builds none of them, and its metadata dependency list is empty by rule for a CON story.

**Build steps**

1. The five operations of 12.1, read from the API specification, with their paths, parameters, schemas, access rights and idempotency rule.
2. The five schemas of section 11, property by property, with no rename and no addition.
3. The error envelope of 12.3 and the message mapping of section 14.
4. The handler contract of 12.5 for table code `sys_fields`, with the whole-load refusal and the 7 derived-field exception.
5. The versioning rule of AC7 and the source-system rule of AC8, as documents the contract tests read.
6. The four fixture sets of 12.8 and the drift rule.
7. The eight contract tests of section 16; a drift between a fixture and the document fails the build.
8. The nine contract tables, each owner checked against the Ownership Map; then the baseline tag and the consumer note for RWB-P1-E1064-APP, RWB-P1-E1064-OPS and the tests of this legacy key.

**Done when.** The eight contract tests pass, the four fixture sets answer every shape the document declares, the nine tables are complete with their owners, and the application story, the deployment story and the tests of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-021 | Publish of a contract with no confirmation | The data contract for {system} cannot be published until its confirming role records the confirmation. |
| MSG-P1-022 | Never in this contract: the append failure of the interaction ledger, which RWB-P1-E1066-OPS alerts on; carried because the service publishes one message set and both contracts use the one envelope | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-P1-002 | A dictionary load is refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | A reason or a confirmation field is empty | Enter {field}. |
| MSG-GEN-004 | A change is sent from an old version, or with no `If-Match` version | Someone else changed this record. Reload it to see their change. |
| MSG-P4-003 | An unknown field or an unknown contract is called | This case is not in your scope. |
| MSG-GEN-006 | The store or a view is unavailable | {system} is not available. Your request is queued and will be retried. |

The six texts of the dictionary slice are the legacy texts of RWB-E1-064, copied unchanged, and the seventh, MSG-P1-022, is the ledger text of RWB-E1-066, unchanged. The contract fixes which status code carries which identifier: 409 for MSG-P1-021 and for a stale MSG-GEN-004, 422 for MSG-GEN-001, 428 for a missing MSG-GEN-004, 404 for MSG-P4-003, 503 for MSG-GEN-006, and the handler's refusal for MSG-P1-002. Thai text for each message follows decision DL10 and is not written in this document; the message identifiers are the contract, the wording belongs to the Error and Message Standard. MSG-P4-002, the refusal of a role without the right, is raised by the guard library of rwb-access before an operation is reached and is therefore not a row of this table; the access case of section 16 names it because the legacy case names it.

### 15. Screens and states

No screen in this contract. Two screens will read these operations and neither is built or asserted here: the dictionary screen and the contract screen of SCR-40 Reference data. Both reach the five operations through the gateway-bff composite route, one hop per call with a 2 s budget (DP-19; RWB-PLT-N001-CON), and neither reads a table. The route, the screen field list and the rendering of a version belong to the screen owners; the states they show are the DRAFT, confirmed and PUBLISHED of section 9 and the field versions of a definition, which are rwb-case's screen states and not this contract's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-064-01 | AC1, BR1, BR2 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Seeded 122 objects and 1,366 fields; count and completeness queries |
| TC-E1-064-02 | AC2, BR2 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | 30 views, 304 fields; one view column with no dictionary row |
| TC-E1-064-03 | AC3, BR1, BR3 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Account ACC0000017 with delay_days 95; dictionary query for DF-ACE-018 |
| TC-E1-064-04 | AC4, BR6, BR9 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Dictionary fixture without DF-ACE-204; load with the correct and the wrong ACE column |
| TC-E1-064-05 | AC5, BR5 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Change of DF-ACE-018 late behavior with a reason and with an empty reason |
| TC-E1-064-06 | AC6, BR4 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | DC-ACE with 304 fields; confirmation on 2026-11-12; a second contract with no confirmation |
| TC-E1-064-07 | AC7 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Two changes to DF-ACE-020 from version 1; one change with no If-Match |
| TC-E1-064-08 | AC8, BR7 — regression evidence: the criterion is owned by RWB-P1-E1064-APP | End to end | Published DC-ACE and a change to DF-ACE-018 |
| TC-E1-064-09 | Access — regression evidence: the access path belongs to RWB-P1-E1064-APP and rwb-access | Component | RW-TRIBE sends PATCH /admin/data-dictionary/fields/DF-ACE-018; refused with MSG-P4-002 |
| TC-E1-064-C01 | AC1 | Contract | The document rendered and compared with the five API specification rows; one path and one query parameter changed to a wrong value |
| TC-E1-064-C02 | AC2 | Contract | Each of the five schemas compared with the API specification, property by property; one property renamed and one dropped |
| TC-E1-064-C03 | AC3 | Contract | Every failure of the five operations mapped to its status and its message identifier; a second envelope and an unmapped failure |
| TC-E1-064-C04 | AC4 | Contract | The handler contract for table code sys_fields; a load with an empty attribute, a wrong source system and a source field that is not a column of the view |
| TC-E1-064-C05 | AC5 | Contract | The four fixture sets compared with the document, plus one added shape and one missing shape |
| TC-E1-064-C06 | AC6 | Component | The nine contract tables reviewed against the Ownership Map and against the summary of 12.9 |
| TC-E1-064-C07 | AC7 | Contract | DC-ACE at version 1 published; a field change; the rule read for the new DRAFT and for the publish refusal |
| TC-E1-064-C08 | AC8 | Contract | The source-system rule applied to the 304 view fields and the 1,062 table fields, the 7 derived fields and the 49 extension fields |

The eight new cases prove the contract artefacts of this story and run at Contract level; TC-E1-064-C06 reviews the tables of section 12 and runs at Component level. The nine legacy cases are carried as regression evidence: their IDs, Covers and Data are kept in legacy order and character for character, the legacy Covers text is qualified as regression evidence, the legacy level "System" maps to "End to end" and "Access" to "Component", and the criteria themselves are owned by RWB-P1-E1064-APP. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the document: owners, cycles, late behavior and contract content are data rows in `rwb_source_data`; the schemas carry their names and types and never a default value.
- No personal data in an example or a fixture: the dictionary holds definitions, not values; the confirmation names a role, never a person, and the four fixture sets are synthetic.
- No read of another service's tables: the contract names `rwb_source_data` and the `recovery.v_ace_*` views and nothing else, and the one consumed operation is a contract call (DP-01, DP-05).
- One hop and 2 s on the rwb-case list read; a slow answer is an error and never a cached constant (DP-11).
- A published contract is never edited in place; a change makes a new version, and an applied migration is never edited either (DP-15).
- No DDL, no migration and no deployment in this story: the tables are RWB-P1-E1001-APP's, the views are RWB-P1-E1069-APP's, and the chart is RWB-P1-E1064-OPS's.
- A fixture that leaves the contract fails the build; a shape with no fixture fails the build.
- The document publishes no event: the topic `rwb.source-data.events.v1` belongs to RWB-P1-E1015-APP and the contract declares no AsyncAPI document.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | Recovery data is organized in 14 data products, each with exactly one named system of record, one read path and one named owner. Source data is read from ACE through read-only views and is not copied | The `sourceSystem`, `sourceField` and `ownerRole` properties of `DataDictionaryField`, the source-system rule of AC8 and the five tables of 12.7 | TC-E1-064-C02, TC-E1-064-C04, TC-E1-064-C08 |
| REQ-RDF-011 | Every data product has a catalog entry stating its definition, owner, system of record, refresh cycle and retention | The `DataContract` and `DataContractConfirmation` schemas, the versioning rule of AC7 and the confirmation fields BR4 requires | TC-E1-064-C03, TC-E1-064-C05, TC-E1-064-C07 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1064-APP | App development | Implements the five operations and the reference-table handler this contract publishes; consumes the five schemas and the four fixture sets |
| RWB-P1-E1064-OPS | DevOps | Deploys the slice, wires the alerts to the message identifiers of section 14 and runs the smoke test against this contract |
| RWB-P1-E1001-APP | App development | Delivers the five tables, the 122 and 1,366 seed rows and `v_data_dictionary` that the delivered-baseline fixture stands in for |
| RWB-P1-E1069-APP | App development | Delivers the 30 `recovery.v_ace_*` views whose 304 fields this contract describes and never creates |
| RWB-P3-E1043-CON | Contract | C: the reference-data contract whose list read is 12.2 and which calls the handler of 12.5 for table code `sys_fields` |
| RWB-PLT-E1044-CON, RWB-PLT-E1047-CON | Contract | The per-service Flyway sequence and the naming library the contract follows, recorded as notes in section 3 |
| RWB-PLT-N001-CON | Contract | The gateway-bff composite route the two screens of section 15 will use (DP-19) |

### 19. Out of scope

- The two controllers, the two services, the handler implementation and the five tables' read and write code: RWB-P1-E1064-APP.
- The chart, the flag values, the migration step, the probes, the dashboards, the alerts, the runbook and the smoke run: RWB-P1-E1064-OPS.
- The five tables, their DDL, the 122 and 1,366 seed rows and the read model `v_data_dictionary`: RWB-P1-E1001-APP.
- The 30 `recovery.v_ace_*` views, the login, the grants, the view owner `ace_view_owner` and the four extension tables: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- The reference-data contract itself, its reference-load operation and its approval: rwb-case, RWB-P3-E1043-CON (DP-07). This contract names one handler for table code `sys_fields` and consumes one list read; it defines nothing of that contract.
- Access control per data product, PDPA masking and the catalog entry maintenance: RWB-P1-E1016-APP and rwb-access (DP-08).
- Freshness stamps per data product, retention per product and table, and the reconciliation report: RWB-P1-E1015-APP, RWB-P1-E1017-APP and RWB-P1-E1011-APP.
- The dictionary and contract screens of SCR-40 in their final form, and the gateway-bff composite route: the screen owners and RWB-PLT-N001-CON (DP-19).
- Contracts for stage 2 data products: RWB-P1-E2010-CON.
