# RWB-P1-E1015-CON Freshness stamp per data product

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1015-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (base path /api/recovery/source-data/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-014, FR-P1-015, FR-P1-016, FR-P1-017) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-015 for rwb-source-data. The freshness capability publishes a contract for the first time: three operations on `/api/recovery/source-data/v1`, the typed interfaces `FreshnessQuery` and `DailyCompletenessGate`, the two events `AceDataReady` and `AceDataLate` on `rwb.source-data.events.v1` under a CloudEvents 1.0 envelope, the `AceIngestCheckWorkflow` activity contract and the one cut-off Schedule per data product (DP-09, DP-10, DP-11, DP-14). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1015-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 22 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of rwb-source-data for freshness: an OpenAPI 3.1 document for `GET /data-products/freshness`, `GET /freshness` and `POST /business-days/{date}/ready`, the typed `FreshnessQuery` and `DailyCompletenessGate` interfaces in a contract jar, an AsyncAPI 3 document for `AceDataReady` and `AceDataLate` under a CloudEvents 1.0 envelope, the `AceIngestCheckWorkflow` activity contract, the declaration of one cut-off Schedule per data product, the nine contract tables of section 12 and the contract fakes for rwb-decision, rwb-case and the platform**, so that **rwb-case, rwb-payment, rwb-deviation, rwb-writeoff, rwb-decision, the alerts and the gateway-bff banner build against a fixed, testable contract on Day 1 without waiting for the freshness code to be written**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the freshness capability is the one read that four services and one screen depend on before anything else can run: rwb-case starts `DailyCaseRun` on `AceDataReady`, rwb-payment starts payment matching on the same event, rwb-deviation and rwb-writeoff follow it, rwb-decision writes the freshness of every input into its own snapshot, and the stale banner reaches gateway-bff on `AceDataLate` (Arch v5 slide 43, rows 26 and 27). If the shapes, the envelope and the activity contract are agreed once and faked, the app, operations and test stories of this legacy key, and the four consuming services, build in parallel; a change in any of them is caught in a contract test rather than in an integration window.

The baseline also fixes the naming the checks enforce: schema `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1`, event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-13, DP-14; Arch v5 slides 29, 41 and 43).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice.
- The outbox, inbox and idempotency library is available as a reference for the table names and the envelope (RWB-PLT-TE006-CON, DP-09).
- The workflow kit is available, with its Schedule registration and its typed activity contract convention (RWB-PLT-E1071-CON, DP-10).
- The platform RFC 9457 problem body and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners are taken from the Ownership Map only; rwb-source-data never documents an operation owned by another service.
- The event payload and the envelope attributes are fixed by GAP-0493 with ASM-0685; the Schedule names and per-product cut-offs by GAP-0494 with ASM-0686; the source/load time mapping by GAP-0492 with ASM-0684.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the three operations with the shared components, the security scheme and the error responses of every code.
2. Draft the typed interfaces `FreshnessQuery` and `DailyCompletenessGate` and the `FreshnessStamp` record in the contract jar, with their nullability and their timeout budget.
3. Draft the AsyncAPI 3 document for `rwb.source-data.events.v1`: the two event types, the CloudEvents 1.0 envelope and the seven payload fields.
4. Draft the `AceIngestCheckWorkflow` contract: the input schema, the mode, the workflow ID rule and the five activity inputs and outputs.
5. Declare the one cut-off Schedule per source-fed data product, with its cadence source, its overlap policy and its catch-up window.
6. State the versioning rule for the REST surface, the event schemas and the activity contract.
7. Publish the nine contract tables of section 12 and the six fakes.
8. Add the contract tests: schema validation, envelope validation, error mapping, idempotency replay on the Airflow signal and drift between a fake and the document.
9. Tag the baseline and hand it to RWB-P1-E1015-APP, RWB-P1-E1015-OPS and every consuming service.
10. Draft the scheduler interface with the ready and status operations and the poll of the ACE batch record as the fallback; confirm with the bank platform team which path is live at go-live before the integration test.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | 400 with the problem body and the failing pointer | MSG-GEN-001 | AC1 |
| X2 | A caller asks for a major version the service does not serve | 404 with the problem body and the served major versions | MSG-GEN-001 | AC1 |
| X3 | An interface signature changes without a new major version | The contract test fails and the merge is blocked | None (pipeline log) | AC2 |
| X4 | A consumer cannot deserialise an event | The registry validation fails the build; the event schema is not published | None (pipeline log) | AC3 |
| X5 | A declared Schedule has no data source for its cadence | The registration check fails the build, because a cadence in code would be a business value there | None (pipeline log) | AC4 |
| X6 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None (pipeline log) | AC5 |
| X7 | A field-level definition is missing from the source material | The field is marked with the placeholder and the row of section 12 carries it | None | AC6 |
| X8 | The Airflow signal is replayed with the same business date | The stored answer is returned; no second gate run and no second event | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the workflow kit and the Ownership Map only |
| Negotiable | Field-level detail of the payload and the response bodies is settled with the consumers; the named operations, events, interfaces and rules are fixed by the target architecture |
| Valuable | Unblocks the app, operations and test stories of this legacy key on Day 1, and the four consuming services and rwb-decision |
| Estimable | Two documents, one contract jar, one AsyncAPI file, one workflow contract, nine contract tables, six fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Freshness contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the freshness capability publishes on the topic rwb.source-data.events.v1 with the task queue rwb-source-data in namespace rwb-recovery

  Scenario: AC1 The three operations are published with their shapes (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-source-data is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/source-data/v1
    Then it declares GET /data-products/freshness with the query parameters product and asOf, GET /freshness with the query parameter businessDate, and POST /business-days/{date}/ready with an Idempotency-Key header
    Then every operation names its right, its 400, 401, 403 and 503 responses and the message ID of each
    Then a replay of the Airflow signal for one business date returns the stored answer and raises no second gate run

  Scenario: AC2 The two published interfaces are in the contract jar (new, D-RCV-60)
    Given the contract jar of rwb-source-data
    When it is published to the consumers
    Then it carries FreshnessQuery with stampFor, stampForRow and stampsFor
    Then it carries DailyCompletenessGate with check over a business date and a set of product codes, answering COMPLETE or HOLD with the product and the source
    Then FreshnessStamp carries productCode, businessDate, sourceExtractedAt, loadedAt, status and staleSince, with status one of LOADED and STALE
    Then a signature change without a new major version fails the contract test

  Scenario: AC3 The two events carry the envelope and the payload (new, D-RCV-60)
    Given the AsyncAPI 3 document of rwb-source-data is published
    When it is validated against the AsyncAPI 3 schema
    Then it declares the topic rwb.source-data.events.v1 with the retry topic and the .dlt topic
    Then it declares rwb.source-data.AceDataReady.v1 and rwb.source-data.AceDataLate.v1
    Then every message carries a CloudEvents 1.0 envelope with id, source, type, specversion, time, subject and datacontenttype
    Then every payload carries eventId, occurredAt, schemaVersion, sourceSystem, businessDate, status and completedAt, and no personal data field

  Scenario: AC4 The workflow and the cut-off Schedules are contracted (new, D-RCV-60)
    Given the workflow contract of rwb-source-data
    When the consumers review it
    Then it declares AceIngestCheckWorkflow on the task queue rwb-source-data with the input sourceSystem, businessDate, observedStatus and mode
    Then it declares the activities stampProducts, markStale, publishAceDataReady, publishAceDataLate and checkDailyCompleteness with their inputs and outputs
    Then it declares one cut-off Schedule per source-fed data product, named from the product code, at data_product.expected_by in Asia/Bangkok, with overlap policy SKIP and a catch-up window whose size is Not specified in the source documents (GAP-0494)
    Then no Schedule, cadence or cut-off time is written in code or in the contract as a literal

  Scenario: AC5 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then every consumed path and every published event has one fake that answers it
    Then a drift between a fake and the document fails the build

  Scenario: AC6 The naming, the versioning and the boundary are fixed (new, D-RCV-60)
    Given the baselined documents
    When the naming and version rules are checked
    Then the base is /api/recovery/source-data/v1, the topic is rwb.source-data.events.v1, the events are rwb.source-data.<Event>.v1, the queue is rwb-source-data and the package is th.co.scb.ace.workbench.recovery.sourcedata
    Then a breaking change needs a new major version and an additive change stays inside version 1
    Then the document names data_product_load and data_product as this service's own tables and decision_log_entry as P7's, reached only through FreshnessQuery

  Scenario: AC9 The business rules BR1 to BR8 of section 8 hold across the contract (new, D-RCV-60)
    Given the contract documents and the contract jar of rwb-source-data
    When each rule of section 8 is checked against them
    Then BR1 to BR8 each pass their check, and a failing rule fails the build

  Scenario: AC10 An unknown major version answers 404 with the problem body and the served major versions (new, D-RCV-60)
    Given the published operations of rwb-source-data
    When a caller asks for a major version the service does not serve
    Then it answers 404 with the problem body and the served major versions under MSG-GEN-001

  Scenario: AC11 A status other than LOADED or STALE is refused (new, D-RCV-60)
    Given a FreshnessStamp for one product and business date
    When a status other than LOADED or STALE is written to it
    Then the write is refused and the stored status is unchanged
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; a document never declares another service's path | DP-13; Arch v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by the source system and the business date, and carries no personal data | Arch v5 slides 42 and 43 notes; DP-09 |
| BR4 | Every POST declares the Idempotency-Key header and stores its response | Arch v5 slide 11; DP-09 |
| BR5 | Error responses use one envelope and one message ID per condition; business message texts are copied unchanged from the legacy story | Arch v5 platform baseline; Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version, for the REST surface, the events and the activity contract | Arch v5 slide 11 notes |
| BR7 | The document lists only operations owned by rwb-source-data; a consumed path is described as consumed, never as provided | Ownership Map v1 |
| BR8 | No business value is fixed in the contract: the expected-by times, the refresh cycles and the product-to-source map stay data rows, and a cadence is never a literal | Template and Rules §R7.2 s17; DP-10 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the two interfaces, the two events and the workflow are described | In review |
| In review | Consumer sign-off | The app, operations and test stories, rwb-case, rwb-payment, rwb-deviation, rwb-writeoff and rwb-decision accept the baseline and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field or an activity signature is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the documents, the contract jar and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Consuming teams (the app, operations and test stories, and the rwb-case, rwb-payment, rwb-deviation, rwb-writeoff and rwb-decision owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the problem body, the naming rule and the workflow kit this document reuses |
| Data steward | Confirms that no personal data field is declared in an event and that no business value is fixed in the contract |

The per-service login name behind the document's security scheme is Not specified in the source documents (GAP-0493; ASM-0685); the document names it "the rwb_source_data login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Freshness stamp resource | `productCode`, `productName`, `businessDate`, `sourceExtractedAt`, `loadedAt`, `status` (LOADED or STALE), `staleSince`, taken from `data_product_load` fields DF-OPS-001 to DF-OPS-009 and `data_product` fields DF-REF-071 to DF-REF-078 | DF-OPS-001 to DF-OPS-009 and DF-REF-071 to DF-REF-078 |
| ACE batch resource | `sourceSystem`, `businessDate`, `startedAt`, `completedAt`, `status`, `recordCount`, `feedVersion`, `isComplete`, `ageDays`, from `v_ace_batch_status` fields DF-ACE-178 to DF-ACE-186 | DF-ACE-178 to DF-ACE-186 |
| Gate result | `businessDate`, the result COMPLETE or HOLD, the product and source that hold it, and the time read | Not specified in the source documents (DOR-RWB-P1-E1015-CON-7) |
| Event payloads | `eventId`, `occurredAt`, `schemaVersion`, `sourceSystem`, `businessDate`, `status`, `completedAt`; no name, address, identity number or contact point | Not specified in the source documents (DOR-RWB-P1-E1015-CON-7) |
| Workflow inputs | `sourceSystem`, `businessDate`, `observedStatus`, `mode`; no personal data and no ACE fact beyond those four | Not specified in the source documents (DOR-RWB-P1-E1015-CON-7) |

The exact JSON field names of the two freshness responses and the detail texts of the problem body are fixed here and confirmed with the consumers; the source/load time mapping behind `sourceExtractedAt` and `loadedAt` is the one ruled in GAP-0492 with ASM-0684, and the envelope attributes by GAP-0493 with ASM-0685. The CloudEvents envelope carries the attributes id, source, type, specversion, time, subject and datacontenttype, with subject set to the source system; the two events are keyed by sourceSystem and businessDate, and their seven payload fields carry the types fixed in the AsyncAPI document. The registry subject is named by the platform event owner, and the login is referenced as DP-02 until it is allocated. Before the ACE additions land, system test reads freshness from the batch-status view populated with synthetic batch rows; where the view is absent the data product is shown as not stamped and no date is inferred from a row count, a file or a view's data date. The fallback freshness source is Not specified in the source documents (GAP-1507) and is named before the go-live decision. The field names that the rwb-source-data data-product contract returns for DP01 Account and arrears, DP07 Legal and the other products it reads are Not specified in the source documents (GAP-1080); the record and page shape of the answer follows when they are published.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/data-products/freshness` | `DataProductFreshness[]`; query product (DP01 to DP14, optional) and asOf (optional) | Case record R |
| GET | `/freshness` | The architecture alias: query businessDate; answers the ACE batch rows with `sourceSystem`, `businessDate`, `startedAt`, `completedAt`, `status`, `recordCount`, `feedVersion`, `isComplete` and `ageDays` | Case record R |
| POST | `/business-days/{date}/ready` | The Airflow signal of Arch v5 slide 15: no body, Idempotency-Key required, answers the gate result COMPLETE or HOLD with product and source | Server to server, workload identity |

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and right check before a stamp is returned, faked |

No other operation is consumed at run time: ACE is read through the views, not over REST (DP-05).

#### 12.3 Events published

| Event | Topic | Owner | Schema |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | P1 | eventId, occurredAt, schemaVersion, sourceSystem, businessDate, status, completedAt; CloudEvents 1.0 envelope |
| `rwb.source-data.AceDataLate.v1` (EV-27) | `rwb.source-data.events.v1` | P1 | The same seven fields, with the status of the latest batch row |

Consumers of AceDataReady are rwb-case, rwb-payment, rwb-deviation and rwb-writeoff; consumers of AceDataLate are the alerts and the gateway-bff banner (Arch v5 slide 43, rows 26 and 27). `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is the shared ledger event of the library and is not published by this capability (DP-03).

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| None | None | None | The capability polls `v_ace_batch_status`; the architecture's IN line states that Airflow calls the ready signal and that the fallback polls the ACE batch record (Arch v5 slide 15) |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AceIngestCheckWorkflow | Workflow, one run per source system and business date, workflow ID from both | `rwb-source-data` | Input schema sourceSystem, businessDate, observedStatus, mode; the signal and query surface |
| stampProducts, markStale | Activities | `rwb-source-data` | Product-to-source map and batch row in; stamps and one outbox row out |
| publishAceDataReady, publishAceDataLate | Activities (event library) | `rwb-source-data` | The envelope and the payload of 12.3 |
| checkDailyCompleteness | Activity | `rwb-source-data` | Business date and products in; COMPLETE, or HOLD with product and source out |

The two published interfaces travel with the workflow contract in the same jar: `FreshnessQuery` (`stampFor`, `stampForRow`, `stampsFor`) and `DailyCompletenessGate` (`check`).

#### 12.6 Schedules

| Schedule | Cadence | Documented fields | Legacy reference |
|---|---|---|---|
| One cut-off check per source-fed data product (DP01, DP02, DP05, DP06, DP07, DP11, DP13) | At `data_product.expected_by` in Asia/Bangkok: 08:00 daily, MON 08:00 weekly, as data rows | Schedule ID, the product code, the overlap policy SKIP, the catch-up window, the mode input | The legacy Quartz trigger per product |

The Schedule names and the per-product expected-by values beyond 08:00 and MON 08:00 are Not specified in the source documents (GAP-0494; ASM-0686); the contract fixes one Schedule per product and that the cadence is read from the data row.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| data_product_load | P1 (rwb_source_data) | The freshness stamp resource of 12.1 and of the two events |
| data_product | P1 (rwb_source_data) | The product name, refresh cycle and expected-by behind the stamp and the Schedules |
| outbox_event, processed_event | PLT library, created in rwb_source_data | The outbox of the two events and the inbox of the listener (DP-09) |
| decision_log_entry | P7 (rwb_decision) | **Named as P7's and never read**; the inputs snapshot reaches this capability only through `FreshnessQuery` (DP-01, DP-03) |

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision WireMock | The inputs snapshot fixture for case RW-2026-000101 with DP01 and DP06 | App story, contract tests |
| rwb-case reference-data WireMock | The product-to-source map and the two expected-by rows of DP01 and DP06 | App and operations stories |
| rwb-access WireMock | `POST /authorise` with a granted answer and a refused answer for a role without Case record R | App story, contract tests |
| Workflow kit fake | Schedule registration and activity retry with a test clock | App and operations stories |
| Event platform fake | The outbox, the inbox and the CloudEvents envelope | App story, contract tests |
| gateway-bff route fake | The composite route of the data panel | App story |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 1 consumed | Freshness reads and the Airflow signal; the authorise hop; one hop, 2 s timeout |
| Kafka | 2 published, 0 consumed | AceDataReady and AceDataLate on `rwb.source-data.events.v1` with retry and `.dlt` |
| Temporal | 1 workflow, 5 activities, 7 Schedules | AceIngestCheckWorkflow on `rwb-source-data`; one cut-off Schedule per source-fed product |
| File | None | No file in this contract; the batch status arrives as a view row |

### 13. Solution plan

**Deliverables.** `openapi/rwb-source-data-v1.yaml` (OpenAPI 3.1), `asyncapi/rwb-source-data-v1.yaml` (AsyncAPI 3), `contract/rwb-source-data-freshness-contract.jar` with the two interfaces, `FreshnessStamp` and the workflow and activity types, the versioning and idempotency rules in the contract README, and the six WireMock or fixture mappings.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the three operations and the error responses; schema lint in the pipeline.
2. The two response shapes and the gate result, with the field names of section 11.
3. The contract jar: `FreshnessQuery`, `DailyCompletenessGate`, `FreshnessStamp` and the workflow and activity types, with the timeout budget on the client side.
4. AsyncAPI 3 document with the topic, the two event types, the CloudEvents envelope and the registry versioning rule.
5. The idempotency rule on the Airflow signal and the stored answer, and the versioning rule for the three surfaces.
6. The six fakes and their fixtures, including the AC3 snapshot fixture.
7. Six contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note.

**Done when.** The OpenAPI and AsyncAPI documents validate in the pipeline, the contract jar resolves for the four consuming services and rwb-decision, the six contract tests pass, every fake answers its path and the app, operations and test stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A request body or query fails schema validation | Enter {field}. |
| MSG-P4-001 | No session on a read | Sign in to continue. |
| MSG-P4-002 | Role without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | The store or the view is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P1-001 | A product is stale, or the gate holds a business date | {product} is from {date}. Today's load has not arrived. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed, except MSG-P1-001, whose English text is that of Error and Message Standard v4, and Thai text follows DL10, which stays open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed under the programme directive.

### 15. Screens and states

The contract serves SCR-03 Case record, state Read only, whose data panel shows each product's business date and load time, and state Stale input, which shows MSG-P1-001 next to a stale product. The gateway-bff composite route (DP-19) calls the freshness read and the case read in parallel and merges the answers; the composite route specification and the panel field list are Not specified in the source documents (GAP-0494; ASM-0686), so this document fixes the service side of the merge only. The loading state of SCR-03 is the state Screen Specifications v1 section SCR-03 gives; the empty, error and no-access states of SCR-03 are Not specified in the source documents (CG-ALL-2132). For the freshness data this contract supplies to the panel, the error state follows the 503 answer with MSG-GEN-006 and the no-access state follows the 403 answer with MSG-P4-002; the empty state of that data is Not specified in the source documents (DOR-RWB-P1-E1015-CON-10).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-015-09 | AC1, AC6; regression evidence for legacy Access | Contract | RW-REFADM calls GET /data-products/freshness; refused with MSG-P4-002 |
| TC-E1-015-01 | AC1, AC3 | Contract | ALS batch row for 2026-11-30, started 23:30, completed 05:40; DP01 |
| TC-E1-015-02 | AC3, AC4 | Contract | No COMPLETED ALS row at 08:00; test clock on the cut-off Schedule |
| TC-E1-015-03 | AC2, AC5 | Contract | Decision for RW-2026-000101 reading DP01 and DP06; the snapshot fixture |
| TC-E1-015-04 | AC3 | Contract | ALS batch row FAILED at 05:20 |
| TC-E1-015-05 | AC3 | Contract | Same COMPLETED row delivered twice; one inbox row |
| TC-E1-015-06 | AC3, AC4 | Contract | Late ALS batch at 08:40 after the stale flag |
| TC-E1-015-07 | AC4 | Contract | ALS batch at 07:59; the cut-off Schedule at 08:00 |
| TC-E1-015-08 | AC4 | Contract | Weekly DP06 batch on Monday; the cut-off on Thursday |
| TC-E1-015-10 | AC2, AC4 | Contract | EFS batch FAILED at the 08:00 cut-off; the gate result HOLD with DP05 and EFS |
| TC-E1-015-11 | AC2 | Contract | Every source COMPLETED for 2026-11-30; the gate result COMPLETE |
| TC-E1-015-12 | AC3, AC4 | Contract | CCMS COMPLETED 2026-11-27; SVAF only to 2026-11-20 |
| TC-E1-015-13 | Table boundary of 12.7 (DOR-RWB-P1-E1015-CON-12) | Contract | Each table of 12.7 at its boundary; decision_log_entry is named and never read |
| TC-E1-015-14 | AC9 | Contract | Each rule BR1 to BR8 of section 8 checked against the contract |
| TC-E1-015-15 | AC10 | Contract | A caller asks for a major version the service does not serve; 404 with MSG-GEN-001 (X2 of section 5) |
| TC-E1-015-16 | AC11 | Contract | A status other than LOADED or STALE written to a FreshnessStamp |

This story owns no legacy acceptance criterion, so the rows TC-E1-015-01 to TC-E1-015-12 are the legacy test cases of RWB-E1-015 with their IDs kept in legacy order, and TC-E1-015-13 to TC-E1-015-16 are added under D-RCV-60, TC-E1-015-13 being the table boundary case; the Covers column names this story's own criteria, because the baseline is what each case now exercises: the document, the jar, the envelope, the Schedule declaration, the nine tables and the fakes. The legacy level "System" maps to "Contract" and "Access" to "Contract" as well, because no database is touched by a contract test. The criteria themselves are proven in RWB-P1-E1015-APP for AC3 and AC8 and with the other slices of RWB-E1-015. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; TC-E1-015-10 to TC-E1-015-16 have no row there yet. The criterion numbers Test Cases v8 gives for these cases are those of the legacy story RWB-E1-015, not of section 7: TC-E1-015-02 AC2, TC-E1-015-03 AC3, TC-E1-015-04 AC4, TC-E1-015-05 AC5, TC-E1-015-06 AC6, TC-E1-015-07 AC7 and TC-E1-015-08 AC8.

### 17. Guardrails

- No business value in the contract: the expected-by times, the refresh cycles, the product-to-source map and the alert channel stay data, and a cadence is never a literal (DP-07, DP-10).
- No personal data in an event schema, a workflow input, an example or a fake: identifiers, codes, dates and times only (DP-09).
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: the contract describes the views as read-only and writes nothing to ACE (DP-05).
- No cross-schema read and no cross-schema key: the document names `rwb_source_data` tables as this service's own and `decision_log_entry` as P7's, reached only through `FreshnessQuery` (DP-01, DP-11).
- One REST base, one topic and one queue per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The envelope, the problem body and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-009 | Every data product carries a freshness stamp from the ACE batch record; every decision records the freshness of the data it used | The freshness resource, the gate result, `FreshnessQuery`, AceDataReady and AceDataLate | TC-E1-015-01, TC-E1-015-03, TC-E1-015-10, TC-E1-015-11 |
| FEAT-RDF-14 | Stamp each data product with its freshness | The two events, the cut-off Schedule declaration | TC-E1-015-02, TC-E1-015-06, TC-E1-015-07, TC-E1-015-08 |
| FEAT-DRI-12 | Carry a freshness stamp on every decision input | `FreshnessQuery` and the `FreshnessStamp` record | TC-E1-015-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed authorise path and the client budget | TC-E1-015-09 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic, the envelope and the registry rule | TC-E1-015-01, TC-E1-015-04, TC-E1-015-05 |

### 19. Out of scope

- The implementation of the stamp, the stale flag, the gate, the listener and the panel (RWB-P1-E1015-APP).
- The deployment, the chart, the topic and queue provisioning, the Schedule registration, the dashboards, the alerts and the runbook (RWB-P1-E1015-OPS).
- The operations of other services: the rwb-access, rwb-case and rwb-decision contracts are consumed and faked, never defined here.
- The inputs snapshot and the decision log of rwb-decision (RWB-P7-E1027-CON and the P7 stories).
- The gateway-bff composite route specification and the panel field list (platform edge story and RWB-P1-E1015-APP).
- The view definitions and their grants (RWB-P1-E1069-APP, RWB-P1-E1069-DB) and the tables themselves (RWB-P1-E1001-APP).
- The field-level completeness of the two response bodies beyond the names of section 11 (GAP-0493).
