# RWB-P1-E2010-CON Stage 2 data products: contracts, plans and treatments

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2010-CON |
| Work type | CON (Contract) |
| Document version | v3 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), path major version /v1 |
| Contract fake publication | Pending: fakes at `fakes/rwb-source-data/5.1.0/` (working path, NEW-ASM-A1), owner platform library owner |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Stage 2 workflow | Stage2ProductWorkflow on queue rwb-source-data in namespace rwb-recovery, with activities readDp04SourcePage(businessDate, page), writeDp04Page, checkActiveCount and stampDp04; child of AceIngestCheck after the ALS stamp, ID stage2-dp04-{businessDate} (RD-P1-002, RD-P1-040) |
| Deployment values | Carried as a named chart value set per environment; replica count, resource size, thresholds and timings Not specified in the source documents (GAP-0513); test-data fixture owner Not specified in the source documents (GAP-0513), named at the wave 2 entry check |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E2010-CON-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | rwb-treatment (S2; ASM-4458, CDC-03559), rwb-guarantee changed-window claim read (GAP-2738), rwb-case case-existence and reference-data reads (DP-07), rwb-access authorise through RWB-P1-E1016-CON, and RWB-P1-E1015-CON (freshness) |
| Integration dependencies | rwb-guarantee claim read (wave 3): the DP04 guarantee part stays empty in wave 2 until it lands, recorded in the DP04 release note (GAP-2739) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-006, FR-P1-024, FR-P1-025, FR-P1-030, FR-P1-031) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-002, RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-021, RD-P1-023, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-043 |

**Version 3 changes.**

- Records read, Problem body, status and message mapping, freshness and versioning rules follow the register (RWB-P1-E2010-CON#5, #6, #7, #9, #10, #11 and #22; RD-P1-004, RD-P1-005, RD-P1-041).
- Treatment reads belong to rwb-treatment; consumed request and page shapes, the field table, the fakes and the call counts are stated (RWB-P1-E2010-CON#1, #2, #3, #4, #15, #17 and #18).
- Test case table cites Test Cases v9; DL25 and DL11 sources separated (RWB-P1-E2010-CON#19, #20 and #21).
- Pending: record ordering and total (NEW-GAP-S11-7), masking map and access-log failure (NEW-GAP-S11-8), event-built copies in the PRD (NEW-GAP-S11-9), ACE plan field types (NEW-GAP-W4-4) (RWB-P1-E2010-CON#8, #12, #13 and #14).
- Readiness decisions: as in the header.
- Test case references follow Test Cases v9: the legacy rows for AC1 to AC5 are TC-P1-E2010-CON-01 to -05 and the retired TC-P1-E2010-CON-07 is no longer cited.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-010 for rwb-source-data. The stage 2 capability had no published contract in the monolith: the DP04 rows, the join to the ACE views and the access check were in-process calls of one deployable. This baseline publishes the DP04 branch of the record read on `/api/recovery/source-data/v1` with its record shapes, its error envelope, its status and freshness rules and its fakes, so the app story and the Epic 3 consumers build in parallel from Day 1 (DP-11, DP-13; Architecture v5 slides 15 and 41). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: version 3 applies the listed RD-P1 rulings and review corrections.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E2010-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **the published contract baseline of the DP04 record of rwb-source-data: an OpenAPI 3.1 document for the DP04 branch of the record read, the `DataProductRecordPage`, `DataProductRecord` and `FieldValue` shapes with the system of record of every part, the error envelope and the message mapping, the status and freshness rules as data, the versioning rule, the nine contract tables and the fakes of the four dependencies it consumes**, so that **the app, operations and test stories of this legacy key and the Epic 3 consumers build against a fixed, testable shape from Day 1 without waiting for the service or for rwb-guarantee to be built**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). DP04 is read by the case record and by the settlement, restructure and deed-in-lieu screens of Epic 3, and its two content types come from different systems of record: the dated Workbench snapshot in this service's schema and the live ACE facts in the views (BR1-BR2 of the legacy story). If the shape of that mix is not agreed once and faked, every consumer invents its own way of joining a snapshot row to a contract number and distinguishing a Workbench fact from an ACE fact, and the guarantee claim, whose owner is only built in wave 3, blocks the whole read.

The baseline also fixes the naming the checks require: schema and login `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-02, DP-13, DP-14; Architecture v5 slides 29 and 41). The capability adds no event of its own, so the document says so explicitly and no consumer waits for one.

**What D-RCV-60 changes.** The legacy story had nothing published: the snapshot, the view join and the access check were in one process over the one `recovery` schema. Now the snapshot tables are this service's, the ACE facts are this service's views, the treatment entity belongs to rwb-treatment and the guarantee claim is rwb-guarantee's, and the access and freshness answers belong to two other P1 stories. The contract is what keeps that change from becoming five local agreements.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice (DP-14).
- The platform error envelope is the baseline; where this document narrows it, it does so explicitly and names the message ID per condition.
- The operations and their owners are taken from the Ownership Map v1 only; rwb-source-data never documents an operation owned by another service, and the treatment and guarantee reads are documented as consumed (DP-11).
- The record shapes reuse the components already published by RWB-P1-E1016-CON: `DataProductRecordPage`, `DataProductRecord`, `FieldValue`, `DataProductFreshness` and the error envelope; this baseline narrows the DP04 branch of rwb-source-data.yaml 5.1.0 and adds no component owned by another service (RD-P1-005).
- `dp_treatment`, `dp_guarantee_claim`, `data_product`, `data_product_access`, `sys_objects` and `sys_fields` are P1's (Ownership Map v1), so the entity names of the record are this service's own.
- The guarantee claim contract of rwb-guarantee is a C dependency the Work Package does not list, and the field-level DP04 record schema is fixed by no source document (GAP-0512; ASM-0704).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the DP04 branch of `GET /data-products/{productCode}/records` in the OpenAPI 3.1 document, with the path parameter, the three query parameters, the owner, the 200 shape and the five error responses.
2. Fix the `DataProductRecordPage`, `DataProductRecord` and `FieldValue` shapes for DP04, with the entity of each row naming its system of record and every field carrying its field ID.
3. Agree the error envelope and map each HTTP status and refusal to its message ID, with the legacy texts copied unchanged.
4. State the status and freshness rules: LOADED and STALE from LOV-FRESHNESS, the expected-by time, and the hold on a count difference, each as a data row rather than a constant.
5. State the versioning rule: additive within major version 1, a change to the record shape is a new major version, and no event is added.
6. Publish the contract tables of section 12 and the six fakes and fixtures of section 12.8.
7. Add the contract tests: schema validation, the shape of the record, the envelope mapping, the freshness rule, the versioning rule and the fake-to-document comparison.
8. Tag the baseline and hand it to RWB-P1-E2010-APP, RWB-P1-E2010-OPS and the Epic 3 consumers.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `caseId` is missing or not a UUID; `page` or `size` is out of range; `productCode` is outside its pattern | 400 for a missing or malformed `caseId` and for `productCode`; 422 for a value out of range; Problem body | MSG-GEN-001, MSG-GEN-002, MSG-GEN-007 | AC1, AC3, AC10 |
| X2 | No valid session or no Workbench role; or a session without the Case record right | 401; or 403; Problem body | MSG-P4-001; MSG-P4-002 | AC1, AC3 |
| X3 | A DP04 access row is absent or not in force | 403 with MSG-P4-002; no row is returned and no field is leaked | MSG-P4-002 | AC3 |
| X4 | The case is outside the caller's scope | 404 with MSG-P4-003 | MSG-P4-003 | AC3 |
| X5 | A required property of the record has no definition in the source material | The property carries the placeholder and the gap row is carried | None | AC2 |
| X6 | A fake drifts from the document, or a property of another service's table appears in a schema | The contract test fails and the merge is blocked | None | AC2, AC6 |
| X7 | A caller asks for a major version the service does not serve | 404 with a Problem body whose `type` ends `/unknown-version` and names the version | MSG-GEN-007 | AC5 |

Message texts are those of Error and Message Standard v6. MSG-P1-001 and MSG-P1-002 are operational messages of the stale product and the refused load; they are not REST answers of this read, and a stale product still answers 200 (RD-P1-041).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelope, the ownership map, the API Specification v5 and the record components of RWB-P1-E1016-CON |
| Negotiable | Field-level detail is settled with the consumers; the path, the query parameters, the record shapes and the rules are fixed |
| Valuable | Unblocks the app and operations stories of this legacy key and the Epic 3 consumers of DP04 on Day 1 |
| Estimable | One document branch, three record shapes, one envelope, two rules, nine contract tables, six fakes and fixtures and the tests of section 16 |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: DP04 record contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the Ownership Map v1 names P1 as the owner of dp_treatment, dp_guarantee_claim, data_product and data_product_access

  Scenario: AC1 The OpenAPI 3.1 document declares the DP04 branch of the record read (new, D-RCV-60; TC-P1-E2010-CON-01, TC-P1-E2010-CON-09)
    Given the OpenAPI 3.1 document of rwb-source-data is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/source-data/v1
    Then it declares GET /data-products/{productCode}/records with the owner rwb-source-data and productCode as a required path parameter
    Then the DP04 branch requires `caseId` (UUID); `page` is integer, minimum 0, default 0; `size` is integer, minimum 1, default 50, maximum 200 (RD-P1-005)
    Then `productCode` matches `^DP(0[1-9]|1[0-4])$`; the operation answers 400, 401, 403, 404 and 503 using the published response schemas
    Then the 200 answer is DataProductRecordPage, its items are DataProductRecord, its fields are FieldValue and its freshness is DataProductFreshness
    Then no other service's path and no other base path is declared

  Scenario: AC2 The record shape names every fact with its system of record (new, D-RCV-60; TC-P1-E2010-CON-02, TC-P1-E2010-CON-10)
    Given the DataProductRecord, FieldValue, DataProductRecordPage and DataProductFreshness schemas of the document
    When the DP04 properties are reviewed
    Then the properties of entity "dp_treatment" are those of the field table of section 11 (DF-TRT-034 to DF-TRT-049)
    Then the properties of entity "dp_guarantee_claim" are those of the same table (DF-TRT-052 to DF-TRT-061)
    Then no row of entity "dp_treatment" carries contract_no (DF-TRT-050) or contract_date (DF-TRT-051)
    Then the contract number and contract date of the primary account appear with entity "v_ace_account"
    Then the plan terms appear with entity "v_ace_plan"
    Then each row names its entity, so that dp_treatment and dp_guarantee_claim read as the Workbench snapshot and v_ace_account and v_ace_plan read as the ACE facts
    Then each `FieldValue` carries only `fieldName`, `value` and `masked`; dictionary field IDs identify properties outside the wire object. The record carries the snapshot date and freshness
    Then no Workbench table of the document holds a property that copies an ACE column

  Scenario: AC3 One envelope and one message mapping cover every refusal (new, D-RCV-60; TC-P1-E2010-CON-03, TC-P1-E2010-CON-11)
    Given the error envelope component of the document
    When a 400, 401, 403, 404 or 503 response is produced
    Then the body is `application/problem+json` and uses Problem properties `type`, `title`, `status`, `detail`, `instance`, `messageCode`, `messageTh`, `field`, `errors` and `traceId` as defined by RD-P1-004; every service-written problem has `messageCode`
    Then a missing or non-UUID `caseId` answers 400 with MSG-GEN-001
    Then a `page` or `size` out of range answers 422 with MSG-GEN-002
    Then a `productCode` outside its pattern answers 400 with MSG-GEN-007
    Then no session or no Workbench role answers 401 with MSG-P4-001; a caller without the Case record right or without a DP04 access row answers 403 with MSG-P4-002
    Then a case outside the caller's scope answers 404 with MSG-P4-003
    Then a failed freshness or record read answers 503 with MSG-GEN-006
    Then each listed message keeps the published text and is mapped to its declared status; MSG-P1-001 and MSG-P1-002 are operational messages, not extra properties on the 200 record response

  Scenario: AC4 The status and freshness rules are data, not constants (new, D-RCV-60; TC-P1-E2010-CON-04, TC-P1-E2010-CON-12)
    Given the status and freshness section of the document
    When the DP04 rules are reviewed
    Then the status is LOADED or STALE from LOV-FRESHNESS; `businessDate` is nullable and is null when never stamped or while the Section B flag is off (RD-P1-041, RD-P1-043)
    Then the expected-by time is read from `data_product.expected_by`; the DP04 working value is 08:00 under DL11 / ASM-0703 until the data steward records it (RD-P1-041)
    Then `staleSince` is the first business date with no completed ACE batch and is null when the status is LOADED (RD-P1-005)
    Then a difference between the two active treatment counts writes no stamp for the date, so the record answers the previous stamped business date, with status STALE from the expected-by time
    Then a DP04 stamp row exists for a business date only when every source mapped to DP04 in data_product_source is COMPLETED for it (RD-P1-041)
    Then no threshold, tolerance or business date is fixed in the contract

  Scenario: AC5 The versioning rule is stated and no event is added (new, D-RCV-60; TC-P1-E2010-CON-05, TC-P1-E2010-CON-13)
    Given the document declares major version 1 in the path of /api/recovery/source-data/v1
    When a property of the DP04 record is added within the same major version
    Then the addition is accepted and a consumer that ignores it still reads the record
    When a property is removed, renamed or retyped
    Then the change requires a new major version; v1 remains served while v2 is introduced, and only an unserved major version answers 404 with MSG-GEN-007 (RD-P1-004, RD-P1-005)
    Then the document declares no event, no workflow and no Schedule for this capability, and the topic rwb.source-data.events.v1 carries only the events of RWB-P1-E1015-APP

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60; TC-P1-E2010-CON-06)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map v1
    Then six fakes/fixtures cover the two treatment reads, guarantee claim read, ACE account/plan, access, case-existence and reference-data reads; the guarantee max-size value and error mapping remain Pending under GAP-2738
    Then the access fake answers a granted and a refused DP04 answer
    Then the contract tests compare each fake with the document and fail on any drift
    Then 12.3, 12.4, 12.5 and 12.6 state None for the events, the workflows and the Schedules this baseline adds

  Scenario: AC7 Error responses and schema changes keep the contract rules BR8 and BR9 (new, D-RCV-60; TC-P1-E2010-CON-08)
    Given the published document of major version 1 and its message mapping
    When the error responses and a proposed schema change are checked
    Then each error response uses the shared Problem schema and the status-to-message mapping in RD-P1-004, including 401 MSG-P4-001
    Then the business message texts are the texts of the legacy story, unchanged
    Then an additive schema change is accepted within major version 1
    Then a change to the record shape is accepted only as a new major version

  Scenario: AC8 Treatment read compatibility (TC-P1-E2010-CON-14)
    Given the published rwb-treatment fake on /api/recovery/treatment/v1
    When the rwb-source-data client test and the rwb-treatment provider test call GET /treatments?changedFrom=2026-12-14T00:00:00+07:00&changedTo=2026-12-15T00:00:00+07:00&page=0&size=1000
    Then both pass against the same request schema and a page of items, window, page, size and total
    Then GET /treatments/active-count passes the same provider and client schema
    Then an empty window answers 400
    # Pending: publication of both reads in rwb-treatment.yaml, owner rwb-treatment service owner, CDC-03559

  Scenario: AC9 Guarantee claim read and wave 2 fixture (TC-P1-E2010-CON-15)
    Given the guarantee claim fake
    When the claim page of a window with no claim is read
    Then it answers 200 with empty items and total 0, and the DP04 guarantee part stays empty rather than stale (GAP-2739)
    When changedFrom is not before changedTo
    Then it answers 400
    When the fake is set to unavailable
    Then it answers 503

  Scenario: AC10 Records request boundaries (TC-P1-E2010-CON-16)
    Given the records operation of rwb-source-data.yaml 5.1.0
    When size is 200 and page is 0
    Then it answers 200
    When size is 201, size is 0 or page is -1
    Then it answers 422 with MSG-GEN-002 and no row
    When caseId is absent or is "RW-2026-000512"
    Then it answers 400 with MSG-GEN-001 and no read of any row is made

  Scenario: AC11 Personal data masking and access logging (TC-P1-E2010-CON-17)
    Given the access fake grants DP04 to the caller without the unmasked right
    When the DP04 record is read
    Then every property that the access answer marks masked has masked true and no clear value
    Then the read is written to the access log
    # Pending: the DP04 properties to mask per role and the answer when the access log cannot be written, owner data owner with the compliance owner, NEW-GAP-S11-8

  Scenario: AC12 Empty DP04 result (TC-P1-E2010-CON-18)
    Given a case in scope with no treatment, claim or plan row
    When the DP04 records operation is called
    Then it answers 200 with an empty items list, total 0 and the freshness of DP04
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 |
| BR2 | Event names would be `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`; this capability publishes none and adds none | DP-14; Template and Rules §R4 |
| BR3 | DP04 holds treatments and guarantee claims from the Workbench and contract and plan facts read from the ACE views, with one system of record for each part, and no Workbench table copies a contract, a plan or an account | REQ-RDF-014; BR1 and BR2 of the legacy story |
| BR4 | The record answers LOADED or STALE from LOV-FRESHNESS; the product is stamped only when the active-count check matches with zero tolerance (RD-P1-042); DP04 expected-by is 08:00 under DL11 / ASM-0703 until recorded in `data_product.expected_by` | DL11; RD-P1-041; RD-P1-042 |
| BR5 | A role reads DP04 only through an access row in force, answered by the access contract of this service | data_product_access; REQ-RDF-010 |
| BR6 | The contract names no table of another service and no property of another service's table; the treatment and guarantee facts are consumed as contracts; the live treatment row is written and read only in schema `rwb_treatment` by rwb-treatment, and the P1 copy `dp_treatment` is read for reporting only and is never the source of a treatment | DP-01; Ownership Map v1 |
| BR7 | No business value is fixed in the contract: the product code, the owner role, the expected-by time, the status list and the access rows stay data | Template and Rules §R7.2 s17 |
| BR8 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Template and Rules §R7.2 s14 |
| BR9 | A schema change is additive within major version 1; a change to the record shape is a new major version | Architecture v5 slide 11 |

**Where each rule lives in the target.** BR1, BR2 and BR9 are the shape of the document itself. BR3 is the rule the record shape carries: `dp_treatment` and `dp_guarantee_claim` name the Workbench facts and `v_ace_account` and `v_ace_plan` name the ACE facts, and no snapshot property repeats an ACE column. BR4 is stated against the freshness contract of RWB-P1-E1015-CON and the hold of the app story, and this baseline only fixes the vocabulary and the data source. BR5 is answered by RWB-P1-E1016-CON and consumed here. BR6 is the ownership check of the contract tests. BR7 is why the document contains codes and field IDs only. BR8 is section 14.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The DP04 branch, the three record shapes and the envelope are described | In review |
| In review | Consumer sign-off | The app and operations stories and the Epic 3 consumers accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property of the record is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake or an ownership breach | A contract test fails | In review |

The DP04 freshness states LOADED and STALE belong to the product. `businessDate` is nullable and null for a never-stamped product or while its Section B flag is off; status is STALE in both cases (RD-P1-041, RD-P1-043).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the document, the record shapes and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Consuming teams (app, operations, and the rwb-case, rwb-guarantee and Epic 3 owners) | Review and sign off the parts they consume |
| Data steward | Confirms the system of record of each part of DP04 and the data-product expected-by value; confirms which DP04 properties are personal data and how each is masked (NEW-GAP-S11-8) |
| Platform library owner | Owns the error envelope and the naming rule this document reuses |

The identity scheme behind the document's security definition is the platform one: a user JWT from gateway-bff plus workload identity (Architecture v5 slide 11). No credential and no personal name appears in the document or in a fake. Each DP04 read is authorised by the rwb-access authorise check (DP-08), consumed under the access contract of RWB-P1-E1016-CON; this document names no operation path for it.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Record page | `items` of `DataProductRecord`, `freshness` of `DataProductFreshness`, `page`, `size`, `total` | Not specified in the source documents (DOR-RWB-P1-E2010-CON-7) |
| Snapshot row | `recordId` (the treatment or claim record ID), `entity` `dp_treatment` or `dp_guarantee_claim`, `fields` of `FieldValue` with `fieldName`, `value` and `masked` | DF-TRT-034 to DF-TRT-049, DF-TRT-052 to DF-TRT-061 |
| ACE fact row | `recordId` (the `account_key` or the `plan_ref`), `entity` `v_ace_account` or `v_ace_plan`, `fields` of `FieldValue` | DF-ACE-001, DF-ACE-006, DF-ACE-007, DF-ACE-160, DF-ACE-168, DF-ACE-174, DF-ACE-175 |
| Field list | The field table below; DF-TRT-001 to DF-TRT-022 are the source rows of the owners and are not entities of the record; DF-TRT-050 and DF-TRT-051 are not answered (Data Dictionary v11 note) | DF-TRT-034 to DF-TRT-049, DF-TRT-052 to DF-TRT-061, DF-ACE-001, DF-ACE-006, DF-ACE-007, DF-ACE-160, DF-ACE-168, DF-ACE-174, DF-ACE-175 |
| Freshness | `productCode`, `productName`, `sourceSystem`, `businessDate`, `sourceExtractedAt`, `loadedAt`, `status` (LOADED or STALE), `staleSince` | Not specified in the source documents (DOR-RWB-P1-E2010-CON-7) |
| Catalog entry of DP04 | The entry of RWB-P1-E1016-CON with `systemOfRecord` naming the Workbench for the snapshot and ACE for the plan, and the two views in `sourceViews` | Not specified in the source documents (DOR-RWB-P1-E2010-CON-7) |

**DP04 properties** (names and types from Data Dictionary v11; `FieldValue.value` is a string; the dictionary field ID is the column below and is not a wire member).

| Entity | fieldName | Field ID | Dictionary type | Mandatory |
|---|---|---|---|---|
| dp_treatment | id | DF-TRT-034 | uuid | Yes |
| dp_treatment | treatment_id | DF-TRT-035 | uuid | Yes |
| dp_treatment | case_id | DF-TRT-036 | uuid | Yes |
| dp_treatment | decision_log_id | DF-TRT-037 | uuid | No |
| dp_treatment | treatment_type | DF-TRT-038 | varchar(20), LOV-TREATMENT | Yes |
| dp_treatment | proposed_by | DF-TRT-039 | varchar(10), LOV-PROPOSER | Yes |
| dp_treatment | proposed_at | DF-TRT-040 | timestamptz | Yes |
| dp_treatment | offer_amount | DF-TRT-041 | numeric(18,2) | No |
| dp_treatment | haircut_amount | DF-TRT-042 | numeric(18,2) | No |
| dp_treatment | installments | DF-TRT-043 | integer | No |
| dp_treatment | valid_until | DF-TRT-044 | date | No |
| dp_treatment | approval_level | DF-TRT-045 | varchar(4), LOV-APPROVAL-LEVEL | No |
| dp_treatment | booked_at | DF-TRT-046 | timestamptz | No |
| dp_treatment | outcome | DF-TRT-047 | varchar(12), LOV-TRT-OUTCOME | No |
| dp_treatment | outcome_at | DF-TRT-048 | timestamptz | No |
| dp_treatment | business_date | DF-TRT-049 | date | Yes |
| dp_guarantee_claim | id | DF-TRT-052 | uuid | Yes |
| dp_guarantee_claim | guarantee_claim_id | DF-TRT-053 | uuid | Yes |
| dp_guarantee_claim | case_id | DF-TRT-054 | uuid | Yes |
| dp_guarantee_claim | claim_type | DF-TRT-055 | varchar(25), LOV-CLAIM-TYPE | Yes |
| dp_guarantee_claim | claim_deadline | DF-TRT-056 | date | Yes |
| dp_guarantee_claim | claimed_amount | DF-TRT-057 | numeric(18,2) | Yes |
| dp_guarantee_claim | filed_at | DF-TRT-058 | date | No |
| dp_guarantee_claim | paid_amount | DF-TRT-059 | numeric(18,2) | No |
| dp_guarantee_claim | status | DF-TRT-060 | varchar(12), LOV-CLAIM-STATUS | Yes |
| dp_guarantee_claim | business_date | DF-TRT-061 | date | Yes |
| v_ace_account | account_key | DF-ACE-001 | varchar(255) | No |
| v_ace_account | contract_no | DF-ACE-006 | varchar(255) | No |
| v_ace_account | contract_date | DF-ACE-007 | date | No |
| v_ace_plan | plan_ref | DF-ACE-160 | varchar(255) | No |
| v_ace_plan | booked_at | DF-ACE-168 | integer (see NEW-GAP-W4-4) | No |
| v_ace_plan | installments | DF-ACE-174 | integer (see NEW-GAP-W4-4) | No |
| v_ace_plan | recommended_installment | DF-ACE-175 | integer (see NEW-GAP-W4-4) | No |

Pending: the string format of date, date-time and decimal values and the length rules on the wire (GAP-0512, owner tech lead with the data owner); the physical types of the ACE plan fields that the view does not cast, where `booked_at` is sourced from a timestamp column (NEW-GAP-W4-4, owner data owner); the properties to mask (NEW-GAP-S11-8). Row order across the snapshot and ACE rows and the meaning of `total` are Pending, owner tech lead of rwb-source-data (NEW-GAP-S11-7). `page` starts at 0, `size` defaults to 50 and is at most 200; a case with no row answers 200 with empty `items` and total 0; a product that rwb-source-data does not serve answers 400 with its message Pending under GAP-3272 (RD-P1-005, RD-P1-021). The guarantee claim maximum page size and error-to-message mapping remain Pending under GAP-2738.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13).

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/data-products/{productCode}/records` (the DP04 branch) | API-P1-010: `DataProductRecordPage`; `productCode` DP04 required in the path; `caseId`, `page` and `size` in the query; 200 with the snapshot rows and the ACE fact rows of the case; 400, 401, 403, 404 and 503 | Case record R plus a DP04 access row in force, through the access contract of RWB-P1-E1016-CON |

The document declares the branch this legacy key supplies; the branches of the other 13 products stay with their own stories in the same service API file, and this baseline changes no path of theirs.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/treatments?changedFrom=&changedTo=&page=&size=` on `/api/recovery/treatment/v1` | S2 rwb-treatment (`rwb-treatment.yaml`; ASM-4458, CDC-03559) | Half-open window [D 00:00:00, D+1 00:00:00) +07:00; page of `items`, `window`, `page`, `size`, `total`; maximum size 1000; 400 on an empty window; ordering and other errors Pending under GAP-2696; faked |
| GET | `/treatments/active-count` on the same base | S2 rwb-treatment | The number of active treatments; the active states are a parameter row and the answer shape is Pending under GAP-2696; faked |
| GET | `/api/recovery/guarantee/v1/guarantee-claims?changedFrom=&changedTo=&page=&size=` | S3 rwb-guarantee | Same half-open window; page of `items`, `window`, `page`, `size` and scope-filtered `total`, ordered by `updated_at` then `id`; 400 on an empty or inverted window; maximum size value and error mapping Pending under GAP-2738; each claim answered with its `case_id`, with no case check by the provider; the wave 2 fake answers an empty list and an error (CDC-03545, CDC-03580) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case-existence answer of the link check; faked and test-only |
| GET | `/api/recovery/case/v1/reference-data/{tableCode}` with its version | P3 rwb-case | Reads the three required reference-data lists (DP-07) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4), through RWB-P1-E1016-CON | The access answer and the masking marks of each DP04 read; request and response property names Pending under GAP-0983; one hop, 2 s; faked |
| (interface) | `AceSourceReadRepository` over `recovery.v_ace_account` and `recovery.v_ace_plan` | P1 rwb-source-data | The contract and plan facts, read at request time through this service's own ACE read contract |

The guarantee operation follows the accepted target path; its maximum-size value and error mapping remain Pending under GAP-2738. The wave 2 fake returns an empty list, so the guarantee portion stays empty rather than stale (GAP-2739; R-22449). The case-existence and reference-data operations are consumed through rwb-case; ACE facts are read in this service's own views (DP-01, DP-05).

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP. This baseline declares no event and adds none.

#### 12.4 Events consumed

None. `Stage2ProductWorkflow` is a child of `AceIngestCheck` after the ALS stamp; no story of this legacy key consumes a topic or declares a consumer group (RD-P1-040, RD-P1-044).

#### 12.5 Workflows and activities

None in this baseline. `Stage2ProductWorkflow` and its activities `readDp04SourcePage(businessDate, page)`, `writeDp04Page`, `checkActiveCount` and `stampDp04` run on task queue `rwb-source-data` in namespace `rwb-recovery` and are the application story's; their names and the workflow ID `stage2-dp04-{businessDate}` are those of RD-P1-002 and the Temporal Workflow and Activity Catalog v3. The contract fixes no workflow shape and this baseline declares none.

#### 12.6 Schedules

None. The capability owns no Temporal Schedule and no legacy Quartz job; the 05:30 Schedule and the freshness timers belong to RWB-P1-E1015-CON and RWB-P1-E1015-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `dp_treatment`, `dp_guarantee_claim` | P1 (`rwb_source_data`) | The snapshot rows of the record, keyed by record ID and business date; `contract_no` and `contract_date` of Physical Schema v9 are neither written nor answered (NEW-GAP-S11-6) |
| `data_product` | P1 (`rwb_source_data`) | The product code, owner role, refresh cycle and expected-by time behind the record and the freshness |
| `data_product_access` | P1 (`rwb_source_data`) | The DP04 access row the read is answered with |
| `sys_objects`, `sys_fields` | P1 (`rwb_source_data`) | The field IDs, entity names and data types of the record properties |
| `data_product_load` | P1 (`rwb_source_data`) | The freshness of DP04 carried by the record; written by RWB-P1-E1015-APP |

No other table is named in the contract, and no table of another service is read (DP-01, BR6).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-treatment contract fake | 40 active treatments and 12 restructure plans with 9 approvals for the fixture; an active count of 41 against 40 rows; treatments changed at 2026-12-14T23:59:59+07:00 and 2026-12-15T00:00:00+07:00; 400 for an empty window; a contract error | App story, contract tests |
| rwb-guarantee guarantee claim fake | 5 TCG claims for existing cases, one claim for an unknown case ID, an empty list, a contract error | App story, contract tests |
| ACE account and plan fixture | Rows of `v_ace_account` and `v_ace_plan` with `contract_no`, `contract_date`, `plan_ref`, `installments`, `recommended_installment` and `booked_at`; an account with no plan | App story, contract tests |
| rwb-case case-existence fake | The known cases of the fixture; no case for "00000000-0000-0000-0000-000000000997" | App story, contract tests |
| rwb-case reference-data fake | The three lists with their version | App story, contract tests |
| RWB-P1-E1016-CON access fake | A granted DP04 answer for RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD, RW-COE and RW-AUDIT; a refused answer for RW-PHONECOL; a row not yet in force | App story, contract tests |

The records read of the DP04 fake also answers 400, 401, 403, 404 and 503 with the Problem body of section 7. The six fakes and fixtures above are published at the version of the header.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed | The DP04 record read; the treatment window and active-count reads, the guarantee claim read, the case-existence read, the reference-data read and the access check; one hop, 2 s timeout |
| Kafka | None | No event published or consumed by this baseline |
| Temporal | None | No workflow, activity or Schedule in the contract |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** The DP04 fragment of the one service file `rwb-source-data.yaml` (API Specification v7) with the shared components, the status, freshness and versioning rules in the contract README, and the six fakes and fixtures of 12.8 (RD-P1-005).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule, event-started or child workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 and DP-13 are the two patterns the baseline exists for: the in-process join becomes an operation and the monolith base becomes the service base. DP-01 and DP-05 decide what the record may name, DP-07 supplies the status list, DP-10 and DP-15 are named because the app story that consumes the baseline uses them, and DP-19 is the screen path the record is read through.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security definition, the error responses and the shared components; schema lint in the pipeline.
2. The DP04 branch and its three query parameters, with the field names and field IDs of section 11; the field-level detail is agreed under the recorded gap.
3. `DataProductRecordPage`, `DataProductRecord`, `FieldValue` and `DataProductFreshness` narrowed for DP04, with no property owned by another service.
4. Error envelope and the message-ID mapping, business texts copied unchanged.
5. The status, freshness and versioning rules, and the statement that no event, workflow or Schedule belongs to the baseline.
6. The six fakes and fixtures.
7. The contract tests of section 16; a drift between a fake and the document, or a property from another service's table, fails the build.
8. Baseline tag and the consumer sign-off note.

**Done when.** The document validates in the pipeline, the contract tests of section 16 pass, the fakes answer every consumed path, and the app and operations stories of this legacy key and the Epic 3 consumers have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | `caseId` missing or not a UUID (400) | Enter {field}. |
| MSG-GEN-002 | `page` or `size` out of range (422) | {field} must be between {min} and {max}. |
| MSG-GEN-007 | `productCode` outside its pattern (400) or unserved major version (404) | {value} is not a valid value for {field}. Choose a value from the list. |
| MSG-P4-001 | No valid session or no Workbench role (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | No Case record right, or no DP04 access row | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P1-001 | DP04 is stale at its expected-by time | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | The count check held the publish of the business date | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | A record, freshness or downstream read cannot complete (503) | {system} is not available. Try again in a few minutes. |

The message IDs are contract elements and the texts are those of Error and Message Standard v6. MSG-P1-001 and MSG-P1-002 are not REST answers of this read. Thai text for each message follows decision DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863).

### 15. Screens and states

The baseline serves SCR-03 Case record (Read only; loading, refused, ready; empty, error and no access Not specified in the source documents (CG-ALL-2418)), which shows the DP04 data the role may read with the personal fields masked, through the gateway-bff composite route (DP-19), and SCR-45 Data quality (Loading; breaks empty; breaks list; error and no access Not specified in the source documents (CG-ALL-2419)), which shows the count break and the References break the app story writes. The settlement, restructure and deed-in-lieu screens of Epic 3 read the same record and are declared by their own stories. The composite route specification and the screen field list are the platform edge story's and the screen owners'; this document fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E2010-CON-01 | Legacy AC1, BR1, BR2, BR6, BR7; regression evidence for the record of the snapshot and the ACE facts | End to end | 40 synthetic treatments, 12 plans, 9 approvals |
| TC-P1-E2010-CON-02 | Legacy AC2, BR1; regression evidence for the guarantee part of the record | End to end | 5 TCG claims for existing cases |
| TC-P1-E2010-CON-03 | Legacy AC3, BR5; regression evidence for the 403 mapping of the record read | End to end | RW-PHONECOL reads DP04 |
| TC-P1-E2010-CON-04 | Legacy AC4, BR3; regression evidence for the unknown case of the guarantee part | End to end | TCG claim for an unknown case ID |
| TC-P1-E2010-CON-05 | Legacy AC5; regression evidence for the 503 mapping of the treatment contract | End to end | The treatment contract fake returning errors |
| TC-E2-010-06 | Legacy AC6; regression evidence for the page and repeat behaviour of the record | End to end | Step run twice for 2026-12-14 |
| TC-E2-010-07 | Legacy AC7, BR4; regression evidence for the freshness vocabulary of AC4 | End to end | The active count 41 against 40 rows |
| TC-E2-010-08 | Legacy AC8; regression evidence for the snapshot window of the record; run by RWB-P1-E2010-APP | End to end | Changes at 23:59:59 and 00:00:00 |
| TC-E2-010-09 | Legacy Access, BR5; regression evidence for the refused DP04 answer | Component | RW-TRIBE calls the DP04 read with no DP04 access row; refused with MSG-P4-002 |

| TC ID | Covers | Level |
|---|---|---|
| TC-P1-E2010-CON-01, TC-P1-E2010-CON-09 | AC1 | Contract |
| TC-P1-E2010-CON-02, TC-P1-E2010-CON-10 | AC2 | Contract |
| TC-P1-E2010-CON-03, TC-P1-E2010-CON-11 | AC3 | Contract |
| TC-P1-E2010-CON-04, TC-P1-E2010-CON-12 | AC4 | Contract |
| TC-P1-E2010-CON-05, TC-P1-E2010-CON-13 | AC5 | Contract |
| TC-P1-E2010-CON-06 | AC6 | Component |
| TC-P1-E2010-CON-08 | AC7 | Contract |
| TC-P1-E2010-CON-14 | AC8 | Contract |
| TC-P1-E2010-CON-15 | AC9 | Contract |
| TC-P1-E2010-CON-16 | AC10 | Contract |
| TC-P1-E2010-CON-17 | AC11 | Contract |
| TC-P1-E2010-CON-18 | AC12 | Contract |

The TC-P1-E2010-CON rows are in Test Cases v9; TC-P1-E2010-CON-01 to -05 also carry the legacy AC1 to AC5 regression evidence, and TC-P1-E2010-CON-07 is retired there. TC-E2-010-06 to TC-E2-010-09 remain regression evidence of the legacy criteria, run by RWB-P1-E2010-APP against these fakes.

### 17. Guardrails

- No business value in the contract: the product code, the owner role, the expected-by time, the status list and the access rows stay data; the document carries codes, field IDs and enums only.
- No personal data in an example or a fake: the record carries case IDs, record IDs, field IDs, codes, dates and amounts only, and every example is synthetic.
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: the document names `v_ace_account` and `v_ace_plan` as the ACE facts and no other service's table anywhere (DP-05, DP-01).
- No property of another service's table: the treatment and guarantee facts are consumed as contracts, and a property that copies an ACE column into a Workbench table fails the contract test.
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- No event, workflow or Schedule is added by the baseline: the capability is synchronous and the build is a child workflow of the app story (BR2).
- A fake that drifts from the document fails the build, and the error envelope and the naming rule come from the platform library, narrowed but never redefined.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | The DP04 record branch, the record shapes and the freshness of the product | TC-P1-E2010-CON-01, TC-P1-E2010-CON-02, TC-P1-E2010-CON-04 |
| REQ-RDF-010 | Access per data product by role; personal data masked by role under PDPA | The access row of the DP04 read, the 403 mapping and the masked field value | TC-P1-E2010-CON-03, TC-P1-E2010-CON-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Every consumed element of 12.2 with its budget | TC-P1-E2010-CON-03, TC-P1-E2010-CON-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E2010-APP | App development | The build that implements this baseline against its fakes and the ACE views |
| RWB-P1-E2010-OPS | DevOps | Deploys the build, the trigger, the flag, the dashboards and the alerts that carry this baseline |
| RWB-P1-E1016-CON | Contract | Reused: the record components, the error envelope and the access answer |
| RWB-P1-E1015-CON | Contract | Reused: the freshness vocabulary LOADED and STALE and the expected-by time |
| RWB-S2-E2010-APP | App development | Consumer: builds against the treatment read request and page shape of section 12.2 and AC8 |
| RWB-S3-E2010-APP | App development | Consumer and provider: the claim read request and page shape of section 12.2 and AC9 |
| rwb-treatment.yaml | Contract | Consumed: GET `/api/recovery/treatment/v1/treatments` and GET `/api/recovery/treatment/v1/treatments/active-count`; operations and fake per ASM-4458 / CDC-03577 |
| S3 rwb-guarantee claim contract | Contract | Consumed but outside the Work Package's C list: GET /api/recovery/guarantee/v1/guarantee-claims?changedFrom=&changedTo=&page=&size=, ordered by `updated_at` then `id`, maximum page size and error mapping Pending (GAP-2738), answering each claim with its case_id with no case-existence check here; the claim read is faked with an empty list and an error (GAP-0512; ASM-0704) |
| rwb-case reference-data read | Contract | Consumed: the three lists through GET /api/recovery/case/v1/reference-data/{tableCode} with its version (GAP-2696) |

### 19. Out of scope

- The workflow, the four activities, the two snapshot tables and the DP04 branch implementation: RWB-P1-E2010-APP.
- The chart, the worker registration, the trigger proof, the flag, the dashboards, the alerts and the runbook: RWB-P1-E2010-OPS.
- The treatment entity and its plan timers: rwb-treatment. The case-existence check remains rwb-case.
- The guarantee claim record, its filing and its deadline timers: rwb-guarantee (S3, wave 3); only the consumed shape is faked here, and the filing flow is not documented by this baseline.
- The settlement, restructure and deed-in-lieu screens of Epic 3 and their composite routes: the Epic 3 screen stories and the platform edge story.
- The freshness stamp, the stale flag, the expected-by time and the `data_product_load` writer: RWB-P1-E1015-CON and RWB-P1-E1015-APP.
- The access rows, the catalog entry and the access answer: RWB-P1-E1016-CON and RWB-P1-E1016-APP.
- The ACE view SQL and the read path: RWB-P1-E1069-APP.
- The string formats and length rules of the DP04 values (GAP-0512; ASM-0704).
- The design of FR-P1-031 that builds the dated copies from events: this baseline builds them from REST changed-window reads; the PRD alignment is Pending, owner product owner with the solution architect (NEW-GAP-S11-9).

### 20. Remaining delivery steps

- Size: Not specified; owner recovery squad.
- Epic design sign-off: Pending; owner product owner.
- Contract Done and fake publication at the header version: Pending; owner rwb-source-data contract owner.
- Publication of the two treatment reads and the claim read in the owners' API files, and of both in Service Contract Catalog: Pending; owner rwb-treatment and rwb-guarantee service owners (CDC-03559, GAP-2738).
- Synthetic test data in DEV: Pending; owner QA lead.
- DL10, DL25: Pending; owners as in Decision Log.
