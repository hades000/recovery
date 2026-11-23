# RWB-P1-E2010-CON Stage 2 data products: contracts, plans and treatments

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2010-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-006, FR-P1-024, FR-P1-025, FR-P1-030, FR-P1-031) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-010 for rwb-source-data. The stage 2 capability had no published contract in the monolith: the DP04 rows, the join to the ACE views and the access check were in-process calls of one deployable. This baseline publishes the DP04 branch of the record read on `/api/recovery/source-data/v1` with its record shapes, its error envelope, its status and freshness rules and its fakes, so the app story and the Epic 3 consumers build in parallel from Day 1 (DP-11, DP-13; Architecture v5 slides 15 and 41). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the DP04 record of rwb-source-data: an OpenAPI 3.1 document for the DP04 branch of the record read, the `DataProductRecordPage`, `DataProductRecord` and `FieldValue` shapes with the system of record of every part, the error envelope and the message mapping, the status and freshness rules as data, the versioning rule, the nine contract tables and the fakes of the four dependencies it consumes**, so that **the app, operations and test stories of this legacy key and the Epic 3 consumers build against a fixed, testable shape from Day 1 without waiting for the service or for rwb-guarantee to be built**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). DP04 is read by the case record and by the settlement, restructure and deed-in-lieu screens of Epic 3, and its two content types come from different systems of record: the dated Workbench snapshot in this service's schema and the live ACE facts in the views (BR1-BR2 of the legacy story). If the shape of that mix is not agreed once and faked, every consumer invents its own way of joining a snapshot row to a contract number and distinguishing a Workbench fact from an ACE fact, and the guarantee claim, whose owner is only built in wave 3, blocks the whole read.

The baseline also fixes the naming the checks require: schema and login `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-02, DP-13, DP-14; Architecture v5 slides 29 and 41). The capability adds no event of its own, so the document says so explicitly and no consumer waits for one.

**What D-RCV-60 changes.** The legacy story had nothing published: the snapshot, the view join and the access check were in one process over the one `recovery` schema. Now the snapshot tables are this service's, the ACE facts are this service's views, the treatment entity is rwb-case's contract and the guarantee claim is rwb-guarantee's, and the access and freshness answers belong to two other P1 stories. The contract is what keeps that change from becoming five local agreements.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice (DP-14).
- The platform error envelope is the baseline; where this document narrows it, it does so explicitly and names the message ID per condition.
- The operations and their owners are taken from the Ownership Map v1 only; rwb-source-data never documents an operation owned by another service, and the treatment and guarantee reads are documented as consumed (DP-11).
- The record shapes reuse the components already published by RWB-P1-E1016-CON: `DataProductRecordPage`, `DataProductRecord`, `FieldValue`, `DataProductFreshness` and the error envelope; this baseline narrows the DP04 branch and adds no component owned by another service.
- `dp_treatment`, `dp_guarantee_claim`, `data_product`, `data_product_access`, `sys_objects` and `sys_fields` are P1's (Ownership Map v1), so the entity names of the record are this service's own.
- The guarantee claim contract of rwb-guarantee is a C dependency the Work Package does not list, and the field-level DP04 record schema is fixed by no source document (GAP-0512; ASM-0704).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the DP04 branch of `GET /data-products/{productCode}/records` in the OpenAPI 3.1 document, with the path parameter, the three query parameters, the owner, the 200 shape and the five error responses.
2. Fix the `DataProductRecordPage`, `DataProductRecord` and `FieldValue` shapes for DP04, with the entity of each row naming its system of record and every field carrying its field ID.
3. Agree the error envelope and map each HTTP status and refusal to its message ID, with the legacy texts copied unchanged.
4. State the status and freshness rules: LOADED and STALE from LOV-FRESHNESS, the expected-by time, and the hold on a count difference, each as a data row rather than a constant.
5. State the versioning rule: additive within major version 1, a change to the record shape is a new major version, and no event is added.
6. Publish the contract tables of section 12 and the four fakes.
7. Add the contract tests: schema validation, the shape of the record, the envelope mapping, the freshness rule, the versioning rule and the fake-to-document comparison.
8. Tag the baseline and hand it to RWB-P1-E2010-APP, RWB-P1-E2010-OPS and the Epic 3 consumers.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `caseId`, `page` or `size` fails schema validation | 400 with the error envelope and the failing pointer | MSG-GEN-001 | AC1, AC3 |
| X2 | No valid session, or a session without the Case record right | 401 or 403 with the error envelope | MSG-P4-001, MSG-P4-002 | AC1, AC3 |
| X3 | A DP04 access row is absent or not in force | 403 with MSG-P4-002; no row is returned and no field is leaked | MSG-P4-002 | AC3 |
| X4 | The case is outside the caller's scope | 404 with MSG-P4-003 | MSG-P4-003 | AC3 |
| X5 | A required property of the record has no definition in the source material | The property carries the placeholder and the gap row is carried | None | AC2 |
| X6 | A fake drifts from the document, or a property of another service's table appears in a schema | The contract test fails and the merge is blocked | None | AC2, AC6 |
| X7 | A caller asks for a major version the service does not serve | 404 with the error envelope and the served major versions | None described in the sources | AC5 |

MSG-P4-002, MSG-P4-003, MSG-P1-001, MSG-P1-002 and MSG-GEN-006 keep their text from the legacy story and are carried unchanged in the envelope mapping; MSG-GEN-001 and MSG-P4-001 are the shared envelope messages declared by RWB-P1-E1016-CON.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelope, the ownership map, the API Specification v4 and the record components of RWB-P1-E1016-CON |
| Negotiable | Field-level detail is settled with the consumers; the path, the query parameters, the record shapes and the rules are fixed |
| Valuable | Unblocks the app and operations stories of this legacy key and the Epic 3 consumers of DP04 on Day 1 |
| Estimable | One document branch, three record shapes, one envelope, two rules, nine contract tables, four fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: DP04 record contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the Ownership Map v1 names P1 as the owner of dp_treatment, dp_guarantee_claim, data_product and data_product_access

  Scenario: AC1 The OpenAPI 3.1 document declares the DP04 branch of the record read (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-source-data is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/source-data/v1
    Then it declares GET /data-products/{productCode}/records with the owner rwb-source-data and productCode as a required path parameter
    Then the DP04 branch of that operation names caseId, page and size as query parameters
    Then the operation answers 400, 401, 403, 404 and 503
    Then the 200 answer is DataProductRecordPage, its items are DataProductRecord, its fields are FieldValue and its freshness is DataProductFreshness
    Then no other service's path and no other base path is declared

  Scenario: AC2 The record shape names every fact with its system of record (new, D-RCV-60)
    Given the DataProductRecord, FieldValue, DataProductRecordPage and DataProductFreshness schemas of the document
    When the DP04 properties are reviewed
    Then the treatment fields DF-TRT-001 to DF-TRT-014 appear with entity "dp_treatment"
    Then the guarantee claim fields DF-TRT-015 to DF-TRT-022 appear with entity "dp_guarantee_claim"
    Then the contract number and contract date of the primary account appear with entity "v_ace_account"
    Then the plan terms appear with entity "v_ace_plan"
    Then each row names its entity, so that dp_treatment and dp_guarantee_claim read as the Workbench snapshot and v_ace_account and v_ace_plan read as the ACE facts
    Then the record carries the business date of the snapshot and the freshness of the product
    Then no Workbench table of the document holds a property that copies an ACE column

  Scenario: AC3 One envelope and one message mapping cover every refusal (new, D-RCV-60)
    Given the error envelope component of the document
    When a 400, 401, 403, 404 or 503 response is produced
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then a missing caseId answers 400 with MSG-GEN-001
    Then a caller without the Case record right or without a DP04 access row answers 403 with MSG-P4-002
    Then a case outside the caller's scope answers 404 with MSG-P4-003
    Then a failed freshness or record read answers 503 with MSG-GEN-006
    Then MSG-P4-002, MSG-P4-003, MSG-P1-001, MSG-P1-002 and MSG-GEN-006 carry the legacy text unchanged

  Scenario: AC4 The status and freshness rules are data, not constants (new, D-RCV-60)
    Given the status and freshness section of the document
    When the DP04 rules are reviewed
    Then the freshness status is LOADED or STALE from the list LOV-FRESHNESS and the record never invents a third value
    Then the expected-by time of the product is read from data_product and is not a value of the document or the code
    Then a difference between the active treatment count written and the count answered by the treatment contract holds the stamp, so the record answers the previous business date with status STALE
    Then the rollup of a product fed by several sources takes the oldest business date, as the freshness contract of RWB-P1-E1015-CON states it
    Then no threshold, tolerance or business date is fixed in the contract

  Scenario: AC5 The versioning rule is stated and no event is added (new, D-RCV-60)
    Given the document declares major version 1 in the path of /api/recovery/source-data/v1
    When a property of the DP04 record is added within the same major version
    Then the addition is accepted and a consumer that ignores it still reads the record
    When a property is removed, renamed or retyped
    Then the change requires a new major version and a caller of version 1 is answered 404 with the served major versions
    Then the document declares no event, no workflow and no Schedule for this capability, and the topic rwb.source-data.events.v1 carries only the events of RWB-P1-E1015-APP

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map v1
    Then the three fakes answer the treatment read, the guarantee claim read and the ACE account and plan fixture, and the case-existence stub answers the link check
    Then the access fake answers a granted and a refused DP04 answer
    Then the contract tests compare each fake with the document and fail on any drift
    Then 12.3, 12.4, 12.5 and 12.6 state None for the events, the workflows and the Schedules this baseline adds
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 |
| BR2 | Event names would be `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`; this capability publishes none and adds none | DP-14; Template and Rules §R4 |
| BR3 | DP04 holds treatments and guarantee claims from the Workbench and contract and plan facts read from the ACE views, with one system of record for each part, and no Workbench table copies a contract, a plan or an account | REQ-RDF-014; BR1 and BR2 of the legacy story |
| BR4 | The record answers LOADED or STALE from LOV-FRESHNESS; the product is stamped only when the active count matches, with zero tolerance | DL25; TSD P1 freshness rules |
| BR5 | A role reads DP04 only through an access row in force, answered by the access contract of this service | data_product_access; REQ-RDF-010 |
| BR6 | The contract names no table of another service and no property of another service's table; the treatment and guarantee facts are consumed as contracts | DP-01; Ownership Map v1 |
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

The DP04 freshness states LOADED and STALE belong to the product and not to this baseline, which only carries their names.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the document, the record shapes and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Consuming teams (app, operations, and the rwb-case, rwb-guarantee and Epic 3 owners) | Review and sign off the parts they consume |
| Data steward | Confirms the system of record of each part of DP04 and that the record publishes no personal value |
| Platform library owner | Owns the error envelope and the naming rule this document reuses |

The identity scheme behind the document's security definition is the platform one: a user JWT from gateway-bff plus workload identity (Architecture v5 slide 11). No credential and no personal name appears in the document or in a fake.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Record page | `items` of `DataProductRecord`, `freshness` of `DataProductFreshness`, `page`, `size`, `total` |
| Snapshot row | `recordId` (the treatment or claim record ID), `entity` `dp_treatment` or `dp_guarantee_claim`, `fields` of `FieldValue` with `fieldName`, `value` and `masked` |
| ACE fact row | `recordId` (the `account_key` or the `plan_ref`), `entity` `v_ace_account` or `v_ace_plan`, `fields` of `FieldValue` |
| Field list | DF-TRT-001 to DF-TRT-022 for the snapshot rows, DF-TRT-034 to DF-TRT-061 for the two snapshot tables, DF-ACE-001, DF-ACE-006, DF-ACE-007, DF-ACE-160, DF-ACE-168, DF-ACE-174 and DF-ACE-175 for the ACE facts |
| Freshness | `productCode`, `productName`, `sourceSystem`, `businessDate`, `sourceExtractedAt`, `loadedAt`, `status` (LOADED or STALE), `staleSince` |
| Catalog entry of DP04 | The entry of RWB-P1-E1016-CON with `systemOfRecord` naming the Workbench for the snapshot and ACE for the plan, and the two views in `sourceViews` |

The exact field-level schema of the DP04 record — the required flags, lengths and formats per property of the snapshot and ACE rows — and the shape of the guarantee claim read of rwb-guarantee are Not specified in the source documents (GAP-0512; ASM-0704); this baseline fixes the property names above from the legacy data rows and the API Specification v4 and leaves the field-level detail to the baseline review.

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
| GET | `/api/recovery/case/v1/cases/{caseId}/treatments` and the changed-window and active-count reads of that contract | P3 rwb-case (`RWB-P3-E2004-CON`) | The treatment facts of a case; operation names are fixed by that contract; faked |
| GET | the guarantee claim read of the rwb-guarantee contract | S3 rwb-guarantee | The TCG claims of a case; faked, and not in the Work Package's C list (GAP-0512; ASM-0704) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case-existence answer of the link check; faked and test-only |
| (interface) | `AceSourceReadRepository` over `recovery.v_ace_account` and `recovery.v_ace_plan` | P1 rwb-source-data | The contract and plan facts, read at request time through this service's own ACE read contract |

No other service is called: the status list arrives as reference data through the keeper library of rwb-case (DP-07), and the ACE facts are read in this service's own views (DP-01, DP-05).

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP. This baseline declares no event and adds none.

#### 12.4 Events consumed

None in this baseline. The stage 2 build is started by this service's own `rwb.source-data.AceDataReady.v1`, consumed by RWB-P1-E2010-APP; the contract adds no consumed event and no consumer group.

#### 12.5 Workflows and activities

None in this baseline. `Stage2ProductWorkflow` and its activities `snapshot(page)`, `writeDp04Page`, `checkActiveCount` and `stampDp04` run on task queue `rwb-source-data` in namespace `rwb-recovery` and are the application story's; those names are a target design choice fixed by no source document, recorded in the application slice (GAP-0510; ASM-0702). The contract fixes no workflow shape and this baseline declares none.

#### 12.6 Schedules

None. The capability owns no Temporal Schedule and no legacy Quartz job; the freshness cut-off Schedules belong to RWB-P1-E1015-CON and RWB-P1-E1015-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `dp_treatment`, `dp_guarantee_claim` | P1 (`rwb_source_data`) | The snapshot rows of the record, keyed by record ID and business date; no `contract_no` and no `contract_date` column |
| `data_product` | P1 (`rwb_source_data`) | The product code, owner role, refresh cycle and expected-by time behind the record and the freshness |
| `data_product_access` | P1 (`rwb_source_data`) | The DP04 access row the read is answered with |
| `sys_objects`, `sys_fields` | P1 (`rwb_source_data`) | The field IDs, entity names and data types of the record properties |
| `data_product_load` | P1 (`rwb_source_data`) | The freshness of DP04 carried by the record; written by RWB-P1-E1015-APP |

No other table is named in the contract, and no table of another service is read (DP-01, BR6).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| RWB-P3-E2004-CON treatment fake | 40 active treatments and 12 plans for the fixture case; a treatment changed at the end of the business date; a contract error | App story, contract tests |
| rwb-guarantee guarantee claim fake | 5 TCG claims for existing cases, one claim for an unknown case ID, an empty list, a contract error | App story, contract tests |
| ACE account and plan fixture | Rows of `v_ace_account` and `v_ace_plan` with `contract_no`, `contract_date`, `plan_ref`, `installments`, `recommended_installment` and `booked_at`; an account with no plan | App story, contract tests |
| RWB-P1-E1016-CON access fake | A granted DP04 answer for RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD, RW-COE and RW-AUDIT; a refused answer for RW-PHONECOL; a row not yet in force | App story, contract tests |

The case-existence answer used by the link check is the test-only stub of rwb-case's case contract and is listed with the four fakes above in the contract tests; it is recorded with GAP-0512 and ASM-0704.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed (2 contracts and 1 case read) | The DP04 record read; the treatment and guarantee reads and the case-existence read; one hop, 2 s timeout |
| Kafka | None | No event published or consumed by this baseline |
| Temporal | None | No workflow, activity or Schedule in the contract |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-source-data-v1.yaml` with the DP04 branch and the shared components, `contract/dp04-record.yaml` for the record shapes, `contract/error-envelope.yaml`, the status, freshness and versioning rules in the contract README, and the four fake mappings of 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
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
6. The four fakes and their fixtures.
7. The six contract tests; a drift between a fake and the document, or a property from another service's table, fails the build.
8. Baseline tag and the consumer sign-off note.

**Done when.** The document validates in the pipeline, the six contract tests pass, the four fakes answer every consumed path, and the app and operations stories of this legacy key and the Epic 3 consumers have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | caseId or another required query field is missing | Enter {field}. |
| MSG-P4-001 | No valid session | Your session has ended. Sign in again. |
| MSG-P4-002 | No Case record right, or no DP04 access row | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P1-001 | DP04 is stale at its expected-by time | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | The count check held the publish of the business date | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | The freshness, the record read or a consumed contract is unavailable | {system} is not available. Your request is queued and will be retried. |

The message IDs are contract elements; the five business texts are the legacy texts carried unchanged, and MSG-GEN-001 and MSG-P4-001 are the shared envelope messages of RWB-P1-E1016-CON. Thai text for each message follows decision DL10.

### 15. Screens and states

The baseline serves SCR-03 Case record (Read only; loading, refused, ready), which shows the DP04 data the role may read with the personal fields masked, through the gateway-bff composite route (DP-19), and SCR-45 Data quality (Loading; breaks empty; breaks list), which shows the count break and the References break the app story writes. The settlement, restructure and deed-in-lieu screens of Epic 3 read the same record and are declared by their own stories. The composite route specification and the screen field list are the platform edge story's and the screen owners'; this document fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E2010-CON-01 | AC1 | Contract | The OpenAPI 3.1 document validates; the DP04 branch, its three query parameters and the five error responses are present; no other base path |
| TC-P1-E2010-CON-02 | AC2 | Contract | The DP04 properties of the record with their entities and field IDs; no copied ACE column |
| TC-P1-E2010-CON-03 | AC3 | Contract | 400, 401, 403, 404 and 503 responses carry one envelope, one valid message ID and the legacy text |
| TC-P1-E2010-CON-04 | AC4 | Contract | LOADED and STALE from LOV-FRESHNESS; the expected-by time from data_product; a count difference holding the stamp |
| TC-P1-E2010-CON-05 | AC5 | Contract | An additive property accepted; a removed property refused with the served major versions; no event declared |
| TC-P1-E2010-CON-06 | AC6 | Component | The nine sub-tables complete; the four fakes and the case-existence stub match the document |
| TC-E2-010-01 | Legacy AC1, BR1, BR2, BR6, BR7; regression evidence for the record of the snapshot and the ACE facts | End to end | 40 synthetic treatments, 12 plans, 9 approvals |
| TC-E2-010-02 | Legacy AC2, BR1; regression evidence for the guarantee part of the record | End to end | 5 TCG claims for existing cases |
| TC-E2-010-03 | Legacy AC3, BR5; regression evidence for the 403 mapping of the record read | End to end | RW-PHONECOL reads DP04 |
| TC-E2-010-04 | Legacy AC4, BR3; regression evidence for the unknown case of the guarantee part | End to end | TCG claim for an unknown case ID |
| TC-E2-010-05 | Legacy AC5; regression evidence for the 503 mapping of the treatment contract | End to end | The treatment contract fake returning errors |
| TC-E2-010-06 | Legacy AC6; regression evidence for the page and repeat behaviour of the record | End to end | Step run twice for 2026-12-14 |
| TC-E2-010-07 | Legacy AC7, BR4; regression evidence for the freshness vocabulary of AC4 | End to end | The active count 41 against 40 rows |
| TC-E2-010-08 | Legacy AC8; regression evidence for the snapshot window of the record | End to end | Changes at 23:59:59 and 00:00:00 |
| TC-E2-010-09 | Legacy Access, BR5; regression evidence for the refused DP04 answer | Component | RW-TRIBE calls the DP04 read with no DP04 access row; refused with MSG-P4-002 |

The six new test cases own this story's six criteria; the nine legacy test case IDs, their Covers and their Data are carried onto the split as regression evidence, the legacy level "System" maps to "End to end" and "Access" to "Component". This story owns no legacy acceptance criterion, so the business behaviour behind the legacy rows is proven by RWB-P1-E2010-APP against these fakes; the baseline is tested here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the product code, the owner role, the expected-by time, the status list and the access rows stay data; the document carries codes, field IDs and enums only.
- No personal data in an example or a fake: the record carries case IDs, record IDs, field IDs, codes, dates and amounts only, and every example is synthetic.
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: the document names `v_ace_account` and `v_ace_plan` as the ACE facts and no other service's table anywhere (DP-05, DP-01).
- No property of another service's table: the treatment and guarantee facts are consumed as contracts, and a property that copies an ACE column into a Workbench table fails the contract test.
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- No event, workflow or Schedule is added by the baseline: the capability is synchronous and the build is event-started by the app story (BR2).
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
| RWB-P3-E2004-CON | Contract | Consumed: the treatment facts, faked (DP-11) |
| S3 rwb-guarantee claim contract | Contract | Consumed but outside the Work Package's C list: the guarantee claim read, faked (GAP-0512; ASM-0704) |

### 19. Out of scope

- The workflow, the four activities, the two snapshot tables and the DP04 branch implementation: RWB-P1-E2010-APP.
- The chart, the worker registration, the trigger proof, the flag, the dashboards, the alerts and the runbook: RWB-P1-E2010-OPS.
- The treatment entity and its plan timers: rwb-case, RWB-P3-E2004-APP and its contract.
- The guarantee claim record, its filing and its deadline timers: rwb-guarantee (S3, wave 3); only the consumed shape is faked here, and the filing flow is not documented by this baseline.
- The settlement, restructure and deed-in-lieu screens of Epic 3 and their composite routes: the Epic 3 screen stories and the platform edge story.
- The freshness stamp, the stale flag, the expected-by time and the `data_product_load` writer: RWB-P1-E1015-CON and RWB-P1-E1015-APP.
- The access rows, the catalog entry and the access answer: RWB-P1-E1016-CON and RWB-P1-E1016-APP.
- The ACE view SQL and the read path: RWB-P1-E1069-APP.
- The field-level completeness of the DP04 record and the shape of the guarantee claim read (GAP-0512; ASM-0704).
