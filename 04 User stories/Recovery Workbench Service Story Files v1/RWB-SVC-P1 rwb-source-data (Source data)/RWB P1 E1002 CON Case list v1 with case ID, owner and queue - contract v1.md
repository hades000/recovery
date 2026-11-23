# RWB-P1-E1002-CON Case list v1 with case ID, owner and queue - contract v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1002-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-014, FR-P1-015, FR-P1-016, FR-P1-017, FR-P1-018, FR-P1-019, FR-P1-020, FR-P1-021, FR-P1-022) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-002 for rwb-source-data. This story publishes the contract baseline of the case list: the four REST operations and their answer shapes, the consumed event, the workflow, activity and Schedule contracts, the nine contract tables and the four rwb-case fakes. The case-list operations and their answer shapes, the workflow and schedule names and the 07:15 fallback are fixed here under GAP-0486, GAP-0487 and ASM-0678, ASM-0679, and the removal of the lake, the extract file and the Power BI data set is recorded under GAP-0485 and ASM-0677. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of rwb-source-data for the case list: an OpenAPI 3.1 document for `GET /admin/jobs`, `POST /admin/jobs/{jobId}/rerun`, `GET /case-list/dates/{businessDate}` and `GET /case-list/rows`, an AsyncAPI document for the consumed `rwb.source-data.AceDataReady.v1`, the typed workflow and activity interfaces of `CaseListBuildWorkflow`, `listEligibleAccounts` and `snapshot(page)`, the `DailyCaseList` Schedule declaration, the error envelope, the Idempotency-Key rule, the versioning rule, the nine contract tables of section 12 and the four rwb-case fakes**, so that **the app, operations and test stories of this legacy key build against a fixed, testable contract on Day 1 without waiting for rwb-source-data, rwb-case, rwb-integration or the reporting team to be built**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the Temporal contract jar is the same rule for workflow steps (Arch v5 slide 11). This legacy key spans four stories in three disciplines: the build, this contract, the deployment and the end-to-end integration. They can only run in parallel if the answer shapes are fixed once. Two of the shapes are fixed nowhere in the source material — the case-list date and rows operations do not appear in Arch v5 or in TSD P1, and neither do the workflow and Schedule names — so read as written the build story would invent them privately and every reader would invent a different answer. This story writes them down, fakes the four rwb-case contracts the build reads, and states the DP-17 removal in the contract itself so that no consuming team plans a lake file that will never exist (GAP-0485, GAP-0486, GAP-0487).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the idempotency library are the platform baseline; this document narrows them but never redefines them (DP-09, DP-11).
- The workflow kit and the namespace `rwb-recovery` are available for the typed activity and Schedule declarations (RWB-PLT-E1071-CON).
- The operations and the tables are taken from the Ownership Map only: `case_list_row` is P1's, the case list API and screen are P3's, and a document never declares another service's path.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the four operations, with the shared components used across the rwb-source-data surface.
2. Agree and write the answer shapes of `/case-list/dates/{businessDate}` and `/case-list/rows`, including the column order, the filters and the HELD behaviour.
3. Draft the AsyncAPI document for the consumed `rwb.source-data.AceDataReady.v1` with the CloudEvents 1.0 envelope and the payload fields.
4. Write the typed workflow and activity interfaces and the `DailyCaseList` Schedule declaration into the contract jar.
5. Agree the error envelope and map each condition to MSG-P1-001, MSG-P1-011 or MSG-P4-002.
6. State the Idempotency-Key rule for the rerun POST and the versioning rule for REST and for the activity jar.
7. Publish the nine contract tables and the four rwb-case fakes.
8. Add the contract tests and tag the baseline for RWB-P1-E1002-APP, RWB-P1-E1002-OPS and RWB-ITG-E1002-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request body or query fails schema validation | 400 with the error envelope and the failing pointer | None (contract code) | AC3 |
| X2 | The rerun POST omits the Idempotency-Key header | 400 with the error envelope naming the header | None (contract code) | AC4 |
| X3 | The same Idempotency-Key is replayed with a different body | 422 with the error envelope; the stored response is not overwritten | None (contract code) | AC4 |
| X4 | A reader asks a date that is PENDING or HELD | 200 with the status and no rows | None | AC1 |
| X5 | A fake drifts from the document | The contract test fails and the merge is blocked | None | AC7 |
| X6 | A field-level definition is missing from the source material | The field is marked with the placeholder and the gap is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the workflow kit and the Ownership Map only |
| Negotiable | Field-level detail of the row answer is settled with rwb-case and rwb-reporting; the named operations, the shapes and the rules are fixed here |
| Valuable | Unblocks the build, operations and integration stories of this legacy key on Day 1 |
| Estimable | Two documents, one contract jar, two rules, nine contract tables, four fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion tests an artefact, never a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Case-list contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-source-data is /api/recovery/source-data/v1

  Scenario: AC1 The OpenAPI 3.1 document describes the four case-list operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-source-data is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /admin/jobs with the filters jobCode, status, from and to and the checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE and PUBLISHED on every Job
    Then it declares POST /admin/jobs/{jobId}/rerun with the Idempotency-Key header and the 409 condition for a date that is not complete or a run that is open
    Then it declares GET /case-list/dates/{businessDate} answering the business date, the publish_status, the row count and refreshed_at
    Then it declares GET /case-list/rows with the filters businessDate, team, queue, product and page, and the row in the 19-column order DF-RPT-001 to DF-RPT-019
    Then a date whose publish_status is PENDING or HELD answers its status and no rows

  Scenario: AC2 The event contract names one consumed event and none published (new, D-RCV-60)
    Given the AsyncAPI document of rwb-source-data is published
    When it is validated against the AsyncAPI 3 schema
    Then it declares the topic rwb.source-data.events.v1 and the consumed rwb.source-data.AceDataReady.v1
    Then the payload carries eventId, occurredAt, schemaVersion, sourceSystem, businessDate, status and completedAt and no personal data field
    Then every message uses the CloudEvents 1.0 envelope with the attributes id, source, type, specversion, time, subject and datacontenttype
    Then the document declares no published rwb-source-data event for this capability

  Scenario: AC3 The error envelope is one shape and the message IDs are fixed (new, D-RCV-60)
    Given the error envelope component of the document
    When a 400, 401, 403, 404, 409, 422 or 503 response is produced
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then the messageId is MSG-P1-001, MSG-P1-011, MSG-P4-002 or a contract code, with the legacy text where the message already existed
    Then the response carries the problem media type and the trace identifier

  Scenario: AC4 The rerun POST requires an Idempotency-Key (new, D-RCV-60)
    Given the rerun operation of the document
    When the request omits the Idempotency-Key header
    Then the service answers 400 with the error envelope
    When the same key is sent twice for the same business date
    Then the second call returns the stored response and starts no second run
    When the same key is sent with a different body
    Then the service answers 422 with the error envelope

  Scenario: AC5 The versioning rule covers REST and the activity jar (new, D-RCV-60)
    Given the document declares major version 1 in the path
    When a caller uses an unsupported major version
    Then the service answers 404 with the error envelope and the served major versions
    Then the activity and workflow interfaces are versioned in the contract jar with a compatible change rule, and an incompatible change needs a new interface package
    Then the consumed event schema is versioned in the registry with BACKWARD compatibility

  Scenario: AC6 The workflow, activity and Schedule contracts are declared (new, D-RCV-60)
    Given the contract jar and the Schedule declaration
    When they are reviewed against Arch v5 slides 12, 15 and 44
    Then CaseListBuildWorkflow is declared with workflow ID = business date, the run record shape and the search attributes BusinessDate and PublishStatus
    Then listEligibleAccounts is declared with the business date in and the case-account rows out, and snapshot(page) with the business date and page in and the released rows out
    Then DailyCaseList is declared at 07:15 Asia/Bangkok with overlap policy SKIP, the catch-up window and AceDataReady as the primary trigger
    Then no activity payload carries a case payload or a personal data field

  Scenario: AC7 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then the four rwb-case fakes answer the paths and payloads of 12.2
    Then the contract tests compare the fakes with the document and fail on any drift
    Then the document states that no file, no lake path and no data set is part of the contract
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; a document never declares another service's path | DP-13; Arch v5 slide 41 |
| BR2 | The service topic is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | Every consumed event carries the CloudEvents 1.0 envelope, is keyed by caseId where a case exists and carries no personal data | Arch v5 slides 42 and 43; DP-09 |
| BR4 | Every POST declares the Idempotency-Key header and stores its response | Arch v5 slide 11; DP-09 |
| BR5 | Error responses use one envelope and one message ID per condition; business message texts are copied unchanged from the legacy story | Arch v5 platform baseline; Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version or a new interface package | Arch v5 slide 42; DP-11 |
| BR7 | The document lists only operations and tables owned by rwb-source-data; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR8 | The contract carries no file, lake or data-set artefact: the publish path is removed by DP-17 | DP-17; GAP-0485 |
| BR9 | No business value is fixed in the contract: the threshold, the tolerance and the wait time stay parameters read by contract | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The four operations, the consumed event and the three Temporal contracts are described | In review |
| In review | Consumer sign-off | The build, operations and integration stories accept the document, the jar and the fakes | Baselined |
| Baselined | Additive change | A field or an optional filter is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the documents, the contract jar and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Consuming teams (the build, operations and integration stories, and the rwb-case and reporting owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the idempotency library and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in a payload |

No approval level from the delegation of authority applies. Every "who" is a role.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Case list date | `businessDate`, `publishStatus` (PENDING, HELD, RELEASED), `rowCount`, `refreshedAt` |
| Case list row | The 19 fields DF-RPT-001 to DF-RPT-019 in order: `id`, `businessDate`, `caseId`, `caseNo`, `accountKey`, `accountNo`, `productGroup`, `stageCode`, `status`, `ownerReference`, `queueCode`, `teamCode`, `routeCode`, `totalBalance`, `daysPastDue`, `refreshedAt`, `lastContactAt`, `lastActionCode`, `publishStatus` |
| Job | `jobId`, `jobCode` (JOB-04), `businessDate`, `status`, `startedAt`, `finishedAt` and the checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE, PUBLISHED |
| Consumed event | `eventId`, `occurredAt`, `schemaVersion`, `sourceSystem`, `businessDate`, `status`, `completedAt` |
| Activity payloads | Business date, page number and page size only; no case payload in workflow code or payloads |

The maximum page size, the sort key and the exact JSON types of the row answer are Not specified in the source documents (GAP-0486; ASM-0678); this story fixes the field names and the column order and leaves the field-level detail to the baseline review.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`.

| ID | Method | Path | Documented shape | Access |
|---|---|---|---|---|
| API-P1-001 | GET | `/admin/jobs` | `Job[]` filtered by `jobCode`, `status`, `from`, `to` | Platform administration R |
| API-P1-002 | POST | `/admin/jobs/{jobId}/rerun` | `Job`; Idempotency-Key required; 409 for a date not complete or a run open | Platform administration U |
| — | GET | `/case-list/dates/{businessDate}` | CaseListDate; 404 for a date with no run | Reporting R |
| — | GET | `/case-list/rows` | CaseListRowPage in the 19-column order, filtered by `businessDate`, `team`, `queue`, `product`, `page` | Reporting R |

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | Open case accounts for the business date; faked |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | Allocation state, owner and queue; faked |
| GET | `/api/recovery/case/v1/parameters/{key}` | P3 rwb-case | `case.entry.dpd`, `recon.caselist.tolerance.pct`, `caselist.allocation.wait.until`; faked |
| GET | `/api/recovery/case/v1/reference-data/{lovCode}` | P3 rwb-case | LOV-PUBLISH-STATUS, LOV-PRODUCT, LOV-CASE-STATUS; faked |

No operation of rwb-integration is consumed. RWB-P2-E1007-CON is named in this baseline only because the legacy publish step used its outbound file adapter and that step is removed (DP-17, GAP-0485): the adapter is documented as removed, never as consumed.

#### 12.3 Events published

None. This capability publishes no event. `AceDataReady` and `AceDataLate` on `rwb.source-data.events.v1` are produced by RWB-P1-E1015-APP; the release of a case-list date is a state of the row, read through the date operation.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 (RWB-P1-E1015-APP) | Business date, source ALS, freshness summary; starts `CaseListBuildWorkflow`; deduped through `processed_event` |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseListBuildWorkflow | Workflow, one per business date, workflow ID = business date | `rwb-source-data` | Input schema, run record shape, search attributes BusinessDate and PublishStatus |
| listEligibleAccounts | Activity | `rwb-source-data` | Business date in; case-account rows out; read only |
| snapshot(page) | Activity | `rwb-source-data` | Business date and page in; released rows out in the 19-column order; read only, idempotent |

#### 12.6 Schedules

| Schedule | Cadence | Documented fields | Legacy reference |
|---|---|---|---|
| DailyCaseList | Daily at 07:15 Asia/Bangkok, with AceDataReady as the primary trigger | Schedule ID, cadence, overlap policy SKIP, catch-up window one business date, business date input | JOB-04 case list step; the 07:15 wait |

The name and time are fixed here because no source gives them (GAP-0487; ASM-0679).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| case_list_row | P1 (rwb_source_data) | Case list date and case list row resources |
| data_product_load | P1 (rwb_source_data) | Freshness status read by the date operation |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_source_data | Inbox dedupe and the stored rerun response |

No other table is named in the contract and no table of another service is read (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case query fake (RWB-P3-E1018-CON) | `GET /cases` with the fixture case "RW-2026-000123" and account "ACC0000123", plus an error after 12,000 accounts | Build story, contract tests, integration harness |
| rwb-case allocation fake (RWB-P3-E1020-CON) | `GET /queues/{queueId}/cases` answering allocation complete YES and NO for 2026-11-30 | Build story, contract tests |
| rwb-case parameters fake (RWB-P3-E1042-CON) | `GET /parameters/{key}` for the three keys with a version label | Build story, contract tests |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | `GET /reference-data/{lovCode}` for LOV-PUBLISH-STATUS, LOV-PRODUCT and LOV-CASE-STATUS | Build story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 4 consumed | Case-list reads and the admin jobs; case query, allocation, parameters and reference data; one hop, 2 s |
| Kafka | 0 published, 1 consumed | AceDataReady on `rwb.source-data.events.v1` |
| Temporal | 1 workflow, 2 activities, 1 Schedule | CaseListBuildWorkflow, listEligibleAccounts, snapshot(page), DailyCaseList |
| File | None | No file in this contract: the extract file, the outbound adapter and the data set are removed (DP-17) |

### 13. Solution plan

**Deliverables.** `openapi/rwb-source-data-v1.yaml` (OpenAPI 3.1), `asyncapi/rwb-source-data-v1.yaml` (AsyncAPI 3), `contract/rwb-source-data-activities.jar` (typed workflow and activity interfaces plus the Schedule declaration), `contract/error-envelope.yaml`, the idempotency and versioning rules in the contract README, and the four WireMock mappings.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The four operations with the shapes of section 11 and the 19-column order; the date operation and the HELD behaviour (GAP-0486).
3. AsyncAPI 3 document with the consumed event, the CloudEvents envelope and the registry versioning rule.
4. Contract jar: the workflow and activity interfaces and the Schedule declaration at 07:15 Asia/Bangkok (GAP-0487).
5. Error envelope and the message-ID mapping, business texts copied unchanged.
6. Idempotency-Key rule and the versioning rule for REST and for the jar.
7. The four fakes and their fixtures; the drift test.
8. Baseline tag and the consumer sign-off note.

**Done when.** The OpenAPI, AsyncAPI and jar validate in the pipeline, the seven contract tests pass, the four fakes answer every consumed path, the document states the DP-17 removal, and the build, operations and integration stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ACE batch for the business date is not complete, list not built | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P1-011 | A second start while a run for the date is running or complete | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The IDs and the texts are the legacy ones, character for character; the baseline adds the routing into the error envelope, never a new wording.

### 15. Screens and states

The contract serves the SCR-02 Case list of rwb-case (Loading; empty; list; filtered), reached through the gateway-bff composite route (DP-19), and the reporting screens of rwb-reporting. This baseline fixes the source-data side of the merge only: the date operation, the paged rows and the `snapshot(page)` activity. The composite route specification and the screen field list belong to the edge and rwb-case stories; the fact that a HELD date shows its status and no rows is part of this contract.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-002-01 | AC1, AC7 | Contract | OpenAPI document validates; the four operations, the 19-column order and the HELD behaviour are present |
| TC-E1-002-02 | AC1, AC6 | Contract | Date and rows answers match the fixtures; the workflow and activity declarations match the jar |
| TC-E1-002-03 | AC2 | Contract | AsyncAPI document validates; one consumed event, CloudEvents envelope, no personal data field |
| TC-E1-002-04 | AC3 | Contract | 400, 401, 403, 404, 409, 422 and 503 carry one envelope and a valid message ID |
| TC-E1-002-05 | AC4 | Contract | Rerun POST without the header is refused; a replay returns the stored response; a replay with a different body is refused |
| TC-E1-002-06 | AC5 | Component | An unsupported major version is refused; an incompatible jar change needs a new interface package |
| TC-E1-002-07 | AC1, AC6 | Contract | DailyCaseList declares 07:15 Asia/Bangkok, overlap policy SKIP and the catch-up window |
| TC-E1-002-08 | AC7 | Contract | The four fakes answer their consumed paths; a deliberate drift fails the build |
| TC-E1-002-09 | AC7, BR8 | Component | No file, lake path, adapter or data set appears in any document of the baseline |
| TC-E1-002-10 | AC6, BR3 | Contract | No activity or workflow payload carries a case payload or a personal data field |
| TC-E1-002-11 | Access | Component | A role without Platform administration R is refused with MSG-P4-002 at the document's security scheme |

The 11 legacy TC IDs are kept in legacy order and character for character, with new Covers, because the contract baseline proves the same conditions as artefacts rather than as business outcomes: a row still named AC2 or AC6 of the legacy story where the legacy named it. The legacy Level "System" maps to "Contract" or "Component" for the same reason.

### 17. Guardrails

- No business value in the contract: the threshold, the tolerance and the wait time stay parameters read by contract, never constants (DP-06).
- No personal data in an event schema, an example, a workflow payload or a fake: IDs, codes, dates, counts and amounts only.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: the baseline names no ACE object and no `public` table, and the views are read by the `rwb_source_data` login alone (DP-05).
- No cross-schema read and no cross-schema key: the contract names `case_list_row` in `rwb_source_data` only, and `caseId` and `accountKey` are identifiers without a foreign key (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- Every example in the document and every fixture is synthetic; no production payload is copied into a schema or a fake.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the count of accounts at 90 days past due or more, and every business key resolves to an ACE row | CaseListDate, CaseListRow, `snapshot(page)`, DailyCaseList | TC-E1-002-01, TC-E1-002-02, TC-E1-002-07 |
| REQ-RDF-009 | Every screen and API that shows source data shows its business date and freshness status | `refreshedAt` and `businessDate` in the date and row answers | TC-E1-002-02 |
| REQ-DRI-007 | A delivery that fails after its retry limit is parked with a task for its owner | The error envelope and the removed file path stated in the baseline | TC-E1-002-04, TC-E1-002-09 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Consumed operations with the 2 s client budget | TC-E1-002-08 |

### 19. Out of scope

- The implementation of the build, the activities and the contract controller (RWB-P1-E1002-APP).
- The deployment, the Helm chart, the worker scaling, the Schedule registration and the dashboards (RWB-P1-E1002-OPS).
- The end-to-end run of the legacy criteria AC1, AC3, AC4, AC5 and AC10 (RWB-ITG-E1002-ITG).
- The operations of other services: the rwb-case contracts are consumed and faked, never defined here.
- The case list API and screen of rwb-case and the reporting screens of rwb-reporting.
- The gateway-bff composite route and the screen field list (platform edge story and RWB-P3-E1002-APP).
- Any file, lake or data-set artefact, which DP-17 removes (GAP-0485).
