# RWB-P1-E1015-CON Freshness stamp per data product

Version 3. 27 November 2026.
SCB Collections and Recovery. Henka Group.
(C) Siam Commercial Bank and Henka Pte Ltd

### Version 3 changes

- Applied RD-P1-003, RD-P1-005, RD-P1-022, RD-P1-040 and RD-P1-041 to the freshness, event, workflow and readiness contract; fixed findings #1-#6, #11, #13, #14, #20 and #22.
- Applied RD-P1-001 and RD-P1-004 (idempotency answers, status and message codes, security rights per operation); fixed findings #16, #17 and #25.
- Applied RD-P1-011 (provider fake 5.1.0, contract jar rwb-source-data-contract 1.x); fixed findings #9, #21, #23 and #26 in the story text. Publishing the fake and the test case rows (finding #24) are delivery steps.
- Applied X-27: this contract is the home of the account-page read used by rwb-case, with the values rwb-case reads; path and page limit stay pending under NEW-GAP-B3.
- Findings #7, #8, #10, #12, #15, #18 and #19 are fixed as far as the rulings go; the open points are listed as pending, with a temporary gap ID each, in section 20.
- Business rule IDs BR1 to BR8 and exception ID X8 keep their version 2 meaning; AC7 and AC8 are not used.
- Finishing pass (RD-P1-061, -062, -063, -065, -066; requests S1-stories-0133, W2-tests-1061, W2-tests-3485, W3-messages-0039, W5-runtime-0063, F11-affected-0041; test case backfill): `getPayments` is published here, rwb-integration joins the AceDataReady consumers, the freshness fixtures and account-page errors are stated, and Test Cases v9 IDs are cited.

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
| Size | Not specified; set by the squad at refinement |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-PLT-N009-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON |
| Contract version | rwb-source-data.yaml and asyncapi/rwb-source-data.asyncapi.yaml 5.1.0 (API Specification v7); contract jar rwb-source-data-contract 1.x |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-014, FR-P1-015, FR-P1-016, FR-P1-017) |
| Readiness decisions | RD-P1-001, RD-P1-002, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-020, RD-P1-021, RD-P1-022, RD-P1-024, RD-P1-040, RD-P1-041, RD-P1-043, RD-P1-061, RD-P1-062, RD-P1-063, RD-P1-065, RD-P1-066 |
| CON Done | Pending |
| Fake published | Pending |
| DEV test data | Pending |
| Status | Draft (RD-P1 decisions applied; delivery pending) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-015 for rwb-source-data. The freshness capability publishes a contract for the first time: three operations on `/api/recovery/source-data/v1`, the typed interfaces `FreshnessQuery` and `DailyCompletenessGate`, the two events `AceDataReady` and `AceDataLate` on `rwb.source-data.events.v1` under a CloudEvents 1.0 envelope, the `AceIngestCheckWorkflow` activity contract and the one cut-off Schedule per data product (DP-09, DP-10, DP-11, DP-14). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1015-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 22 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied the binding readiness decisions and story review fixes. Agent: S3-stories.

### 1. Story

As the tech lead of rwb-source-data, I want the published version 5.1.0 baseline to define freshness, the readiness pair, the account-page read used by rwb-case, the two source-data events, AceIngestCheck and DailyCompletenessGate, so that every consumer and implementation team builds against one service contract.

RWB-P1-E1015-CON publishes the freshness resource (built by RWB-P1-E1015-APP) and the readiness pair (built by RWB-P1-E1013-APP). Under X-27 it also publishes the account-page read used by rwb-case, built by RWB-P1-E1002-APP; RWB-P1-E1002-CON publishes nothing and is retired with a pointer to this story.

### 2. Business rationale

A single service contract gives consumers one source for freshness and readiness shapes, event keys and payloads, workflow identity and error handling (DP-11). RWB-P1-E1015-APP implements freshness, the two events and the completeness gate; RWB-P1-E1013-APP implements the readiness handler and record (RD-P1-022).

The baseline fixes the names the checks enforce: schema `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1`, event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.sourcedata`.

### 3. Preconditions

- Platform naming, the Problem schema, the CloudEvents envelope, the outbox library and the workflow kit are available (RWB-PLT-N009-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON).
- RWB-P1-E1015-APP, RWB-P1-E1013-APP and RWB-P1-E1002-APP use this contract as their target; the contract may be built first.
- The operations and their owners are those of the Ownership Map; this service never documents another service's operation as provided.
- The account-page read's path and maximum keys per call are pending under NEW-GAP-B3 and remain a delivery dependency of the rwb-case consumer.

### 4. Flow

1. Publish the service-owned REST and event contracts in the API Specification v7 files; use version 5.1.0.
2. Define the freshness schema, nullable never-stamped business date, readiness request and response shapes, Problem errors, access rules and idempotency.
3. Define the four-field AceDataReady and AceDataLate payloads and CloudEvents envelope.
4. Define the AceIngestCheck type, business-date workflow ID, starts, four activities and DailyCompletenessGate interface.
5. Declare the 05:30 Schedule and expected-by durable timers; do not declare per-product cut-off Schedules.
6. Add the account-page read to the service contract when the path and maximum keys per call are resolved under NEW-GAP-B3.
7. Publish version-matched provider and dependency fakes in the platform fake library.
8. Run schema, compatibility, fixture and consumer contract checks; release the contract and fake together.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request value fails validation | 400 Problem with messageCode and field: unknown list value, or malformed value | MSG-GEN-007; MSG-GEN-001 | AC1, AC16 |
| X2 | Caller requests an unsupported major API version | 404 Problem with type ending /unknown-version, naming the version | MSG-GEN-007 | AC10 |
| X3 | A signature changes without a new major version | The compatibility check fails the build | None | AC2 |
| X4 | An event sample fails its published schema | The registry compatibility check blocks publication | None | AC3, AC13 |
| X5 | An expected_by value is absent | The contract holds no literal cadence; the missing data row is a configuration error of the app | None | AC4 |
| X6 | The provider fake differs from the 5.1.0 documents | Provider and consumer builds fail | None | AC5 |
| X7 | A field or route is not defined by a ruling or source | It is marked pending with its owner and gap; nothing is invented | None | AC20 |
| X8 | The readiness POST is replayed with the same key for the same date | The stored 202 is replayed; no second run and no second event | None | AC14 |
| X9 | The same key is used for another date (another resolved path) | 409 | MSG-PLT-N009-05 | AC14 |
| X10 | The POST has no valid Idempotency-Key | 400; nothing written | MSG-PLT-N009-03 | AC14 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; uses the platform Problem and CloudEvents envelopes, the workflow kit and the Ownership Map |
| Negotiable | Names the rulings leave open are settled with the consumers; the named operations, events, interfaces and rules are fixed |
| Valuable | Gives app, operations and consumer stories one versioned freshness, readiness and event contract to build against |
| Estimable | One REST fragment, one AsyncAPI fragment, two typed interfaces, one workflow contract and one provider fake |
| Small | Fits one contract increment; the account read is added when its path is fixed |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Freshness and readiness contract for rwb-source-data

  Background:
    Given API Specification v7 declares rwb-source-data version 5.1.0

  Scenario: AC1 Operations have complete shapes, rights and errors
    Given the rwb-source-data OpenAPI file
    When it is validated and compared with section 12.1
    Then GET /data-products/freshness declares 200, 400, 401, 403 and 503 and right Case record R
    And POST /business-days/{date}/ready declares 202, 400, 401, 403, 409, 422 and 503, a required uuid Idempotency-Key and right Platform administration U
    And GET /business-days/{date}/status declares 200, 400, 401, 403, 404 and 503 and right Platform administration R
    And GET /payments declares exactly one of the queries businessDate and accountKey and the statuses 200, 400, 401, 403, 409 and 503
    And every error body is the shared Problem schema under security scheme entraId

  Scenario: AC2 The two interfaces are in the contract jar
    Given the contract jar rwb-source-data-contract 1.x
    When the signature test runs
    Then FreshnessQuery exposes stampFor, stampForRow and stampsFor
    And DailyCompletenessGate exposes check(businessDate, productCodes) answering COMPLETE, or HOLD with the blocking product and source
    And FreshnessStamp carries productCode, businessDate, sourceExtractedAt, loadedAt, status and staleSince
    And removing or retyping a member without a new major version fails the build

  Scenario: AC3 Events use the ruled envelope, key and payload
    Given the AsyncAPI file declares rwb.source-data.AceDataReady.v1 and rwb.source-data.AceDataLate.v1 on rwb.source-data.events.v1
    When samples of both are validated
    Then each carries the CloudEvents attributes id, source, type, specversion, time, subject and datacontenttype
    And data holds sourceSystem (string, at most 10), businessDate (date), status (string) and completedAt (date-time or null)
    And the record key is {sourceSystem}:{businessDate} and ce_subject is sourceSystem

  Scenario: AC4 Workflow contract matches its owner
    Given the AceIngestCheck contract
    When its declaration is inspected
    Then one run per business date has ID ace-ingest-check-{businessDate} and input {businessDate, startedBy: AIRFLOW, SCHEDULE, POLL or ADMIN} on task queue rwb-source-data
    And readBatchStatus, stampProducts, markStale and checkDailyCompleteness are declared with 1 s initial interval, back-off 2 and 10 attempts
    And the Schedule rwb-source-data-ace-late-check is 05:30 Asia/Bangkok, overlap SKIP, catch-up window 1 h
    And expected_by checks are durable timers that read data_product.expected_by, with no per-product Schedule and no publish activity

  Scenario: AC5 Provider fake matches the published contract
    Given the provider fake folder fakes/rwb-source-data/5.1.0/
    When provider verification runs every fixture
    Then it holds one mapping per documented status of the four operations, one sample record per event and a fake of the activity interface
    And the freshness fixtures cover LOADED, STALE and never stamped, and the status fixtures RUNNING, DONE and LATE
    And a drift between a fixture and a document fails the provider and the consumer build

  Scenario: AC6 Names and version rule are fixed
    Given the API and AsyncAPI files
    When the naming and version checks run
    Then the base is /api/recovery/source-data/v1, the topic rwb.source-data.events.v1 and the queue rwb-source-data
    And an additive change stays inside /v1, takes a new minor version and publishes a new fake folder, and a breaking change needs a new major version

  Scenario: AC9 Each business rule has a named check
    Given the version 5.1.0 documents and jar
    When the pipeline runs one named assertion for each rule BR1 to BR12 of section 8
    Then the path prefix, event name, envelope, Idempotency-Key, Problem, schema diff, owned path, literal cadence, freshness, readiness, workflow and pending-account-read assertions pass
    And a failed assertion fails the build

  Scenario: AC10 Unsupported major version is refused
    Given a client calls /api/recovery/source-data/v2/data-products/freshness
    When the request is routed
    Then it answers 404 with a Problem whose type ends /unknown-version and whose messageCode is MSG-GEN-007

  Scenario: AC11 Other freshness statuses are rejected
    Given the schema of the DataProductFreshness status property
    When a sample with status CURRENT is validated
    Then validation fails because only LOADED and STALE are allowed

  Scenario: AC12 Consumer compatibility is checked
    Given the consumers and fields of section 12.10
    When their contracts are verified against version 5.1.0
    Then every property they read exists with the same wire name and type

  Scenario: AC13 Schema evolution is backward compatible
    Given a registered event schema
    When a property is removed or retyped inside the same major version
    Then the BACKWARD compatibility check fails the build

  Scenario: AC14 Idempotency of the readiness signal
    Given the readiness fake accepted POST /business-days/2026-11-30/ready with key K
    When the call is repeated with K, sent without a key, or K is used for 2026-12-01
    Then the answers are the stored 202, 400 MSG-PLT-N009-03 and 409 MSG-PLT-N009-05
    And an unavailable idempotency store is declared as 503 MSG-PLT-N009-06

  Scenario: AC15 Refusals per operation
    Given no session, a caller without the operation's right, and an unavailable store
    When each of the four operations is called on the fake
    Then the answers are 401 MSG-P4-001, 403 MSG-P4-002 and 503 MSG-GEN-006 as Problem bodies

  Scenario: AC16 Query and readiness boundaries
    Given product=DP99, a business date with no readiness row and a never-stamped DP05
    When the freshness and status reads are called on the fake
    Then DP99 answers 400 MSG-GEN-007 and the unknown date answers 404 MSG-P4-003
    And DP05 answers 200 with businessDate null and status STALE

  Scenario: AC17 Late event with no completed batch
    Given the AceDataLate sample for a source with no completed batch
    When it is validated
    Then completedAt is null and the other three fields are present and typed

  Scenario: AC18 Multi-source product fixtures
    Given DP06 maps to CCMS, SVAF, AMIS and RPS
    When the fixtures for all sources complete and for SVAF behind are read
    Then the complete case returns one stamp whose sourceSystem completed the set, sourceExtractedAt is the latest completed_at and loadedAt is the write instant
    And the behind case returns the last business date with a complete set, with status STALE

  Scenario: AC19 Readiness pair returns asynchronous state
    Given the readiness fake for 2026-11-30
    When POST ready and then GET status are called
    Then POST answers 202 BusinessDayStatus and GET answers 200 with businessDate, status RUNNING, DONE or LATE and changedAt

  Scenario: AC20 Account-page read is held for rwb-case
    Given X-27 places the account-page read used by rwb-case in this contract
    When section 12.1 and the OpenAPI file are checked
    Then section 12.11 lists the request content and the seven values rwb-case reads, with path, page limit and wire names marked pending
    And no path, limit or property name for it is in the OpenAPI file until NEW-GAP-B3 and NEW-GAP-S3-14 are closed
```

AC7 and AC8 are not used. For every criterion above, the Test Cases v9 row is listed in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base, /api/recovery/source-data/v1; the document never declares another service's path | RD-P1-005 |
| BR2 | Event names are rwb.source-data.<Event>.v1 on rwb.source-data.events.v1, with the catalog retry topics and .dlt | RD-P1-003; Kafka catalog v3 |
| BR3 | Events use CloudEvents 1.0, key {sourceSystem}:{businessDate}, ce_subject sourceSystem, camelCase fields and no personal data | RD-P1-003 |
| BR4 | Every POST declares a uuid Idempotency-Key and replays the stored answer for an identical request | RD-P1-001 |
| BR5 | One Problem schema and one message ID per condition; message texts are copied unchanged from the Error and Message Standard | RD-P1-004 |
| BR6 | An additive change stays inside /v1 with a new minor version; a breaking change is a new major version | RD-P1-005, RD-P1-011 |
| BR7 | The document lists only operations owned by rwb-source-data; a consumed path is labelled consumed | Ownership Map |
| BR8 | expected_by times, refresh cycles and the product-to-source map are data, never contract literals | RD-P1-021, RD-P1-040 |
| BR9 | DataProductFreshness requires productCode and status; businessDate is nullable; sourceExtractedAt is ACE completed_at; loadedAt is the write instant; status LOADED or STALE | RD-P1-005, RD-P1-041 |
| BR10 | Readiness is POST 202 and GET 200 of BusinessDayStatus; an unknown date on GET is 404 MSG-P4-003 | RD-P1-005, RD-P1-020 |
| BR11 | AceIngestCheck is one run per business date; event rows are transactional outbox rows, not activities | RD-P1-003, RD-P1-022, RD-P1-040 |
| BR12 | The account-page read used by rwb-case is published here once its path and page limit are ruled | X-27; NEW-GAP-B3 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | API, event and activity fragments are reviewed | In review |
| In review | Consumer acceptance | Version 5.1.0 shapes are accepted | Baselined |
| Baselined | Additive change | New compatible field is added | New minor version |
| Baselined | Breaking change | A field or signature is removed or retyped | New major version |
| Baselined | Fake drift | Provider or consumer fixture fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data tech lead | Own the API Specification and AsyncAPI fragments, contract jar and provider fake |
| Solution architect | Approve breaking changes; settle NEW-GAP-B3 and the other open wire details |
| Consumer service owners | Verify the fields and operations their services use |
| Platform contract owner | Own the shared Problem, CloudEvents, naming and workflow conventions |

The security scheme of every operation is entraId (OpenID Connect). Rights: freshness read, Case record R; readiness POST, Platform administration U; status read, Platform administration R. The database login rwb_source_data is not an API credential. Service callers (the Airflow signal and consuming services) use workload identities; their identifiers and grants are pending with the solution architect (NEW-GAP-S3-6).

### 11. Data

**DataProductFreshness** (rwb-source-data.yaml; fields DF-OPS-001 to DF-OPS-009, DF-REF-071, DF-REF-072)

| Property | Type | Required | Nullable | Meaning |
|---|---|---|---|---|
| productCode | string | Yes | No | DP01 to DP14 |
| productName | string | No | No | data_product.product_name |
| sourceSystem | string | No | No | Source whose completion completed the set |
| businessDate | date | No | Yes | ACE business date of the stamp in use; null only for a never-stamped product or while the Section B flag is off |
| sourceExtractedAt | date-time | No | No | Latest ace_batch_run.completed_at among the product's sources; not returned when never stamped |
| loadedAt | date-time | No | No | Instant the Workbench wrote the stamp; not returned when never stamped |
| status | LOADED or STALE | Yes | No | LOV-FRESHNESS |
| staleSince | date | No | Yes | First business date with no completed ACE batch; null when LOADED |

Query parameters: product (optional, one product code) and asOf (optional). Without asOf the stamp in use of each product is returned. Pending: asOf meaning and format, ordering, and whether products with no source (DP03, DP08, DP09, DP10, DP12, DP14) appear (NEW-GAP-S3-5).

**BusinessDayStatus**

| Property | Type | Required | Meaning |
|---|---|---|---|
| businessDate | date | Yes | The {date} of the call |
| status | RUNNING, DONE or LATE | Yes | RUNNING while the run is open and ALS is not stamped; DONE once ALS is stamped; LATE once AceDataLate is out with ALS not COMPLETED, and while the Section B flag is off |
| changedAt | date-time | Yes | Time of the last state change |

**AceDataReady and AceDataLate data**

| Field | Type | Required | Nullable |
|---|---|---|---|
| sourceSystem | string, at most 10 | Yes | No |
| businessDate | date | Yes | No |
| status | string, copied from v_ace_batch_status | Yes | No |
| completedAt | date-time | Yes | Yes, when no batch completed |

**Envelope:** id, source, type, specversion, time, subject (= sourceSystem), datacontenttype. eventId, occurredAt and schemaVersion are not data fields.

**DailyCompletenessGate:** input businessDate and productCodes; answer COMPLETE, or HOLD with the blocking product and source. The freshness answer carries the gate value (RD-P1-005); the published array has no member for it, so its name and wrapper are pending (NEW-GAP-S3-7).

Pending: the event status value when no batch row exists (NEW-GAP-S3-2); the event allows 10 characters for sourceSystem while data_product_source allows 20 (NEW-GAP-S3-11). No personal data is present in freshness or event payloads.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base /api/recovery/source-data/v1; contract version 5.1.0 in Recovery Workbench API Specification v7.

| Method | Path | Shape and status | Access | Built by |
|---|---|---|---|---|
| GET | /data-products/freshness | Queries product and asOf; 200 DataProductFreshness[]; 400 MSG-GEN-007; 401; 403; 503 | Case record R | RWB-P1-E1015-APP |
| POST | /business-days/{date}/ready | No body; uuid Idempotency-Key; 202 BusinessDayStatus; a repeat for the date replays 202 with the stored state and starts nothing once it is DONE or LATE; 400, 401, 403, 409, 422, 503 | Platform administration U | RWB-P1-E1013-APP |
| GET | /business-days/{date}/status | 200 BusinessDayStatus; 404 MSG-P4-003 for a date with no readiness row; 400, 401, 403, 503 | Platform administration R | RWB-P1-E1013-APP |
| GET | /payments | `getPayments`: exactly one of `businessDate` (date) or `accountKey` (string, at most 255); both or neither 400 MSG-GEN-001 with `field`; 200 PaymentsAnswer; 401; 403; 409 MSG-P1-001; 503. `businessDate` form: one row per paymentCode, ordered by paymentCode, rules in RWB-P1-E2008-APP. `accountKey` form: rows ordered by paymentDate then paymentCode, businessDate = the DP01 stamp in use. Unpaged (GAP-0601, NEW-GAP-S10-04) | rwb-payment runs (date form); Case record R for E1013 baseline measures and gateway-bff (account form) | RWB-P1-E1013-APP |
| Pending (NEW-GAP-B3) | Account-page read used by rwb-case | Section 12.11 | Pending (NEW-GAP-S3-14) | RWB-P1-E1002-APP |

Errors are the shared Problem schema (application/problem+json; RD-P1-004). The ready POST does not return the gate result. The version 2 alias GET /freshness is not in rwb-source-data.yaml 5.1.0; consumers use GET /data-products/freshness.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | /api/recovery/access/v1/authorise | P4 rwb-access | Authorise a read; one hop and 2 s budget. Not yet published in rwb-access.yaml (NEW-GAP-S3-15) |

Changes to P1 reference rows arrive as reference loads through the apply handler of RWB-P3-E1043-CON, not as a run-time call. ACE data is consumed only through the recovery.v_ace_* views.

#### 12.3 Events published

| Event | Topic | Key | Published | Consumers |
|---|---|---|---|---|
| rwb.source-data.AceDataReady.v1 (EV-26) | rwb.source-data.events.v1 | {sourceSystem}:{businessDate} | Once per source system and business date, when its batch is COMPLETED and stamped | rwb-case, rwb-payment, rwb-integration (JOB-08), rwb-deviation, rwb-writeoff |
| rwb.source-data.AceDataLate.v1 (EV-27) | rwb.source-data.events.v1 | {sourceSystem}:{businessDate} | Once per source system and business date: 05:30 Asia/Bangkok, or at once on FAILED | alerts, gateway-bff |

Payloads and envelope are in section 11. Both events are outbox rows written in the stamp transaction; there are no publish activities. A consumer that starts a daily job starts only on AceDataReady with sourceSystem ALS and status COMPLETED, and deduplicates by its workflow ID (RD-P1-040).

#### 12.4 Events consumed

None from rwb.source-data.events.v1: the service does not consume its own topic. Ledger-intake consumption is declared by RWB-P1-E1066-OPS (RD-P1-003, RD-P1-009).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract |
|---|---|---|---|
| AceIngestCheck | Workflow, one run per businessDate; ID ace-ingest-check-{businessDate} | rwb-source-data | Input {businessDate, startedBy}; starters: readiness handler, 05:30 Schedule, flagged fallback poll, admin rerun of a FAILED run; USE_EXISTING + ALLOW_DUPLICATE for system starts; closes when every due source is stamped or after 24 h (NEW-ASM-C2) |
| readBatchStatus(businessDate) | Activity | rwb-source-data | Reads v_ace_batch_status for every mapped source |
| stampProducts | Activity | rwb-source-data | Writes a row only when every mapped source is COMPLETED; commits the event outbox row with it |
| markStale | Activity | rwb-source-data | Marks the stamp STALE at expected_by or on FAILED |
| checkDailyCompleteness | Activity | rwb-source-data | Checks productCodes against mapped sources; COMPLETE or HOLD |

Activity retry: 1 s initial interval, back-off 2, 10 attempts; start-to-close timeout and heartbeat pending (GAP-0143). In the workflow task that commits the ALS stamp the run starts ReconciliationWorkflow and Stage2ProductWorkflow as children (ABANDON). The contract jar provides FreshnessQuery (stampFor, stampForRow, stampsFor) and DailyCompletenessGate (check); a caller in another service reaches freshness over the REST read (one hop, 2 s). Pending: the other activity inputs and outputs, the parameters and results of the FreshnessQuery methods, the REST mapping of stampForRow, signal and query names and non-retryable errors (NEW-GAP-S3-12).

#### 12.6 Schedules and timers

| Item | Cadence | Contract |
|---|---|---|
| rwb-source-data-ace-late-check | 05:30 Asia/Bangkok | The one P1 freshness Schedule; overlap SKIP; catch-up window 1 h; registered by RWB-P1-E1015-OPS |
| Product expected_by checks | data_product.expected_by | Durable timers inside AceIngestCheck; no per-product Schedules |
| Control-M fallback poll | Start time pending (NEW-GAP-C1) | Flag rwb.source-data.ingest-poll-fallback; off whenever Airflow is live; until NEW-GAP-C1 closes it is built and tested in DEV only and stays off in SIT, UAT and PROD |

#### 12.7 Tables and views

| Item | Owner | Contract use |
|---|---|---|
| data_product_load | P1 rwb_source_data | Freshness stamp; written only by RWB-P1-E1015-APP |
| data_product and data_product_source | P1 rwb_source_data | Product metadata, expected_by and source map |
| outbox_event | Platform library in rwb_source_data | Transactional delivery of EV-26 and EV-27 |
| decision_log_entry | P7 rwb_decision | Never read or written by P1; P7 calls FreshnessQuery and writes its own snapshot |
| v_ace_batch_status and v_ace_holiday | ACE | Read only |

#### 12.8 Contract fakes

**Provider fakes** (RD-P1-011): fakes/rwb-source-data/5.1.0/ (working value, NEW-ASM-A1); publication pending. REST mappings for each documented status of the four operations; fixtures LOADED, STALE, never stamped, RUNNING, DONE, LATE and a replayed 202; one AceDataReady and one AceDataLate record; a fake activity implementation in the jar's testFixtures. The freshness fixtures use the expected business date D of RD-P1-041 (the latest bank business day before the test day): LOADED for D; STALE with businessDate the business day before D and staleSince D; never stamped with businessDate null (RD-P1-062). Account-page fixtures (200, 400, 401, 403, 503) are added once its path is fixed. A HOLD fixture waits for NEW-GAP-S3-7. A consumer states the contract and fake version it builds against.

**Consumed fakes:** rwb-access authorise (granted and refused), reference-load apply (RWB-P3-E1043-CON), workflow kit, event platform.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Detail |
|---|---|---|---|
| REST | Freshness, readiness pair and payments; account-page read when NEW-GAP-B3 closes | rwb-access authorise | One hop, 2 s |
| Kafka | AceDataReady and AceDataLate | No own-topic consumption | Transactional outbox |
| Temporal | One workflow, four activities, one 05:30 Schedule and durable timers | None | rwb-source-data queue |
| File | None | None | ACE is read through its views |

#### 12.10 Consumers and what they read

| Consumer | Reads |
|---|---|
| rwb-case daily case run | AceDataReady with sourceSystem ALS and status COMPLETED |
| rwb-case case list | DP01 freshness: businessDate, status, staleSince, sourceExtractedAt, loadedAt; account-page read (12.11) |
| rwb-payment, rwb-integration, rwb-deviation, rwb-writeoff | AceDataReady: sourceSystem, businessDate, status, completedAt |
| rwb-decision | Freshness stamps for its own inputs snapshot |
| alerts and gateway-bff | AceDataLate; gateway-bff also the freshness read for the data panel |

A consumer story that expects a property not in section 11 (for example is_complete, feed version, an ACE batch list or a gate value on the readiness POST) changes to this shape; no property is added without a ruling.

#### 12.11 Account-page read used by rwb-case

| Item | Content |
|---|---|
| Request | The account keys of one list page and one business date |
| Response per account | Account number, product, total balance, days past due, last contact time, last action code and dataAsOf (as read by RWB-P3-E1002-APP) |
| Account with no data | No entry for the key |
| Caller and limits | rwb-case; one hop, 2 s, one retry with jitter by the caller |
| Errors | Problem schema: 200; 400 MSG-GEN-001; 401 MSG-P4-001; 403 MSG-P4-002 for any caller other than the rwb-case workload identity; 503 MSG-GEN-006; a key with no data returns no entry. Fixtures 200, 400, 401, 403, 503 |
| Pending | Path and maximum keys per call (NEW-GAP-B3); method, wire names, types and access right (NEW-GAP-S3-14) |

### 13. Solution plan

**Published artifacts.** The rwb-source-data REST fragment in API Specification v7, version 5.1.0; the event schemas in the matching AsyncAPI file; the contract jar rwb-source-data-contract 1.x; the version-matched provider fake in the platform fake library. No story-local contract file.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*` | The service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-load apply handler of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. Freshness and readiness schemas with the rights, status codes and Problem mapping of sections 11 and 12.
2. AsyncAPI messages with typed data, key and envelope.
3. Contract jar: FreshnessQuery, DailyCompletenessGate, FreshnessStamp, workflow and activity types.
4. Schedule and timer declaration; provider fake and fixtures.
5. Contract tests of section 16; compatibility checks.
6. Add the account-page read after NEW-GAP-B3 and NEW-GAP-S3-14 close. Add no invented path, page size or member.

**Done when.** The OpenAPI and AsyncAPI files validate in the pipeline, the contract jar resolves for the consuming services, every fixture passes provider verification and the consumers have accepted the baseline.

### 14. Validation and messages

| ID | Condition | Contract message |
|---|---|---|
| MSG-GEN-001 | Malformed date or required value missing | Enter {field}. |
| MSG-GEN-007 | product value outside its list; unsupported major version | {value} is not a valid value for {field}. Choose a value from the list. |
| MSG-P4-001 | No valid session, or no Recovery Workbench role (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | Caller lacks the operation's right (403) | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Business date with no readiness row (404) | This case is not in your scope. |
| MSG-GEN-006 | Store or ACE view unavailable (503) | {system} is not available. Try again in a few minutes. |
| MSG-PLT-N009-03 | POST without a valid Idempotency-Key | The Idempotency-Key header is required and must be valid for {operation}. |
| MSG-PLT-N009-05 | Key reused with another request, or still in flight | The Idempotency-Key conflicts with another request to {operation}. |
| MSG-PLT-N009-06 | Idempotency store unavailable | The idempotency store for {operation} is unavailable. No changes were saved. Try again in a few minutes. |
| MSG-P1-001 | A product is stale, or the gate holds | {product} is from {date}. Today's load has not arrived. |

Texts are those of Error and Message Standard v6; Thai text follows DL10. The status and message mapping is the table of RD-P1-004; this story does not redefine the Problem schema.

### 15. Screens and states

The freshness resource supplies productName, businessDate, loadedAt and status to SCR-03 Case record. State Stale input shows MSG-P1-001 next to a stale product. The panel error state follows the 503 answer with MSG-GEN-006 and the no-access state follows the 403 answer with MSG-P4-002. A never-stamped product has businessDate null and status STALE; its panel text is pending (NEW-GAP-S3-10). The empty state is not specified (CG-ALL-2132). The composite route and the panel field list beyond these fields remain with the platform edge story.

### 16. Test cases

| TC ID | Covers | Level | Fixture |
|---|---|---|---|
| TC-E1-015-01 | AC1, AC3 | Contract | Operations have complete shapes, rights and errors |
| TC-E1-015-02 | AC3, AC4 | Contract | Events use the ruled envelope, key and payload |
| TC-E1-015-07 | AC4 | Contract | Workflow contract matches its owner |
| TC-P1-E1015-CON-01 | AC2, AC5 | Contract | The two interfaces are in the contract jar |
| TC-E1-015-10 | AC2, AC4 | Contract | As the covered item |
| TC-E1-015-12 | AC3, AC4 | Contract | As the covered item |
| TC-P1-E1015-CON-03 | Table boundary of 12.7 (DOR-RWB-P1-E1015-CON-12) | Contract | Table boundary of 12.7 (DOR-RWB-P1-E1015-CON-12) |
| TC-P1-E1015-CON-04 | AC9 | Contract | Each business rule has a named check |
| TC-P1-E1015-CON-05 | AC10 | Contract | Unsupported major version is refused |
| TC-P1-E1015-CON-06 | AC11 | Contract | Other freshness statuses are rejected |
| TC-E1-015-30 | AC6 | Component | Names and version rule are fixed |
| TC-P1-E1015-CON-07 | AC5 | Contract | Provider fake matches the published contract |
| TC-P1-E1015-CON-08 | AC12 | Contract | Consumer compatibility is checked |
| TC-P1-E1015-CON-09 | AC13 | Contract | Schema evolution is backward compatible |
| TC-P1-E1015-CON-10 | AC14 | Contract | Idempotency of the readiness signal |
| TC-P1-E1015-CON-11 | AC15 | Contract | Refusals per operation |
| TC-P1-E1015-CON-12 | AC16 | Contract | Query and readiness boundaries |
| TC-P1-E1015-CON-13 | AC17 | Contract | Late event with no completed batch |
| TC-P1-E1015-CON-14 | AC18 | Contract | Multi-source product fixtures |
| TC-P1-E1015-CON-15 | AC19 | Contract | Readiness pair returns asynchronous state |
| TC-P1-E1015-CON-16 | AC20 | Contract | Account-page read is held for rwb-case |

Contract tests to build, one per element:

| Element | Fixture | Criteria |
|---|---|---|
| GET /data-products/freshness | LOADED, STALE, never stamped, DP99, 401, 403, 503 | AC1, AC15, AC16, AC18 |
| POST /business-days/{date}/ready | 202, replay, missing key, key reused, 503 | AC14, AC19 |
| GET /business-days/{date}/status | RUNNING, DONE, LATE, 404 | AC16, AC19 |
| AceDataReady, AceDataLate | One sample each and one with completedAt null | AC3, AC13, AC17 |
| AceIngestCheck, activities, Schedule | Workflow kit fake | AC4 |
| FreshnessQuery, DailyCompletenessGate | Contract jar | AC2 |
| Versioning, names, provider fake, account read | Documents | AC5, AC6, AC9 to AC12, AC20 |

The criteria of the table above map to the Test Cases v9 rows listed first in this section.

### 17. Guardrails

- API Specification v7 is the only REST contract file for rwb-source-data; this story adds a fragment and does not create a story-local API file.
- Use only rwb-source-data-owned paths as provided; consumed paths are labeled consumed.
- Event payloads use sourceSystem, businessDate, status and completedAt; envelope attributes remain CloudEvents fields.
- Use the shared Problem schema and platform message identifiers.
- Do not publish a case-list contract or P1 case-list table.
- Keep the account-page read Pending until NEW-GAP-B3 resolves; do not infer a path or maximum page size.

### 18. Traceability

| Requirement | Contract element | Test case |
|---|---|---|
| REQ-RDF-009, FEAT-RDF-14 | DataProductFreshness, FreshnessQuery, AceDataReady and AceDataLate | TC-E1-015-01, TC-E1-015-02, TC-E1-015-07, TC-E1-015-10, TC-E1-015-12, TC-E1-015-30, TC-P1-E1015-CON-01, TC-P1-E1015-CON-03 to TC-P1-E1015-CON-16 |
| FEAT-DRI-12 | FreshnessQuery and FreshnessStamp for decision inputs | TC-P1-E1015-CON-01 |
| FR-P1-017 | Readiness POST and status GET | TC-P1-E1015-CON-10, TC-P1-E1015-CON-15 |
| ADR-020 | Contract-first REST, one hop, 2 s | TC-E1-015-01, TC-P1-E1015-CON-11 |
| ADR-015 | CloudEvents and transactional outbox | TC-E1-015-02, TC-P1-E1015-CON-09, TC-P1-E1015-CON-13 |
| X-27 (RD-P1-024) | Account-page read used by rwb-case | Pending NEW-GAP-B3 |

### 19. Out of scope

- Implementation of the stamps, events, gate and freshness read (RWB-P1-E1015-APP), the readiness handler (RWB-P1-E1013-APP) and the account read (RWB-P1-E1002-APP).
- Deployment chart, topic verification, Schedule registration, alert routing and runbook (RWB-P1-E1015-OPS).
- Operations of other services: consumed and faked, never defined here.
- View definitions, grants and tables (RWB-P1-E1069-APP, RWB-P1-E1001-APP).
- Case list and case-list table ownership (rwb-case; RD-P1-024).
- Consumer-specific composite routes and decision snapshots owned by their services.

### 20. Remaining delivery steps

- Set story size at refinement; owner: squad.
- Record epic design sign-off; owner: solution architect.
- Publish and baseline API Specification v7 and AsyncAPI version 5.1.0; owner: rwb-source-data tech lead.
- Publish the provider fake folder fakes/rwb-source-data/5.1.0/; owner: contract owner.
- Create synthetic Section B DEV fixtures; owner: data engineering and QA.
- Add the Test Cases v9 contract rows of section 16; owner: QA lead.
- Account-page read path and maximum keys per call (NEW-GAP-B3), and its method, wire names, types and right (NEW-GAP-S3-14); owner: solution architect with the rwb-case service owner.
- AceDataLate status when no batch row exists (NEW-GAP-S3-2); owner: solution architect.
- asOf meaning, ordering and listing of products with no source (NEW-GAP-S3-5); owner: solution architect.
- Workload identity IDs and grants (NEW-GAP-S3-6); owner: solution architect with the security owner.
- Gate result member of the freshness answer (NEW-GAP-S3-7); owner: solution architect.
- Panel text for a never-stamped product (NEW-GAP-S3-10); owner: screen owner.
- Length of sourceSystem (NEW-GAP-S3-11); owner: data architect.
- Typed signatures of activities and FreshnessQuery methods (NEW-GAP-S3-12); owner: rwb-source-data tech lead.
- Publication of the authorise path in rwb-access.yaml (NEW-GAP-S3-15); owner: rwb-access service owner.
- Control-M fallback poll start time (NEW-GAP-C1); owner: bank platform team with solution architect.

