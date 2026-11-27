# RWB-P1-E1011-CON Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1011-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-008, FR-P1-010, FR-P1-018, FR-P1-019, FR-P1-020, FR-P1-021, FR-P1-022, FR-P1-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-011 for rwb-source-data. The reconciliation is published as one resource on `/api/recovery/source-data/v1`, with a typed workflow and activity contract on task queue `rwb-source-data` in namespace `rwb-recovery` and one consumed event, `rwb.source-data.AceDataReady.v1` (DP-10, DP-11, DP-14). The two lake extracts and the Power BI data set are removed, and rwb-reporting reads the results through this contract (DP-17; GAP-0495; ASM-0687). The path, the result element names and the workflow name are fixed here (GAP-0497; ASM-0689). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-E1011-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of rwb-source-data for the reconciliation resource: an OpenAPI 3.1 document for the two result reads, an AsyncAPI fragment for the consumed `rwb.source-data.AceDataReady.v1`, the typed workflow and activity interfaces of `ReconciliationWorkflow` and `reconciliation`, the published interface `ReconciliationQuery`, the result and break-row schemas with their field IDs, the error envelope, the Idempotency-Key rule of the rerun, the nine contract tables of section 12 and the four contract fakes**, so that **the app, operations and test stories of this legacy key, and rwb-reporting, build against a fixed, testable contract on Day 1 without waiting for the reconciliation to be built**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and an event-started workflow is the replacement for the shared Quartz job (DP-10, ADR-016). The legacy story had no interface at all: the report read two CSV files in the lake and the job record in the shared job table, so every reader was coupled to a file layout and to a scheduler console. In the target the same figures are a resource with a version, a filter and an error body, and the run is a workflow with an input and an output schema.

The baseline matters on Day 1 because three parties move at once: the app story builds the activity against the same result shape, the operations story binds the rerun and the alerts to the same operation names, and rwb-reporting builds its dashboard against the two reads instead of the lake (DP-17). A change to an element name is then a contract change caught by a contract test, not a report that silently returns nothing.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base path, the topic and the event names follow the platform rule (DP-13, DP-14).
- The workflow kit and the `rwb-recovery` namespace exist (RWB-PLT-WF, RWB-PLT-E1071-CON), so the workflow and activity contract is declared against the kit's version and build ID.
- The outbox, inbox and idempotency library is the reference for the table names and columns of the inbox and the stored rerun response (RWB-PLT-TE006-CON, DP-09).
- The platform error envelope, the CloudEvents 1.0 envelope and the message catalogue are the baseline; where this document narrows them it says so.
- The operations and their owners are read from the Ownership Map only: API-P1-003 belongs to this story, and API-P1-001 and API-P1-002 belong to the jobs and case-list contract (RWB-P1-E1002-CON).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document on base `/api/recovery/source-data/v1` for the two result reads, with the shared components of the service.
2. Draft the AsyncAPI fragment for the consumed `rwb.source-data.AceDataReady.v1`, with the CloudEvents 1.0 envelope and the fields the run needs.
3. Declare the `ReconciliationQuery` interface and the workflow and activity contract of `ReconciliationWorkflow` and `reconciliation` on task queue `rwb-source-data`, with the input, the output and the retry policy.
4. Fix the result and break-row schemas against the field IDs of `reconciliation_result` and the break list, with no personal data field.
5. Agree the error envelope, the message mapping and the Idempotency-Key rule of the rerun that starts this workflow.
6. Publish the nine contract tables of section 12 and the four fakes.
7. Add the contract tests: schema validation, envelope validation, error mapping, workflow input validation, idempotent replay and version negotiation.
8. Tag the baseline and hand it to RWB-P1-E1011-APP, RWB-P1-E1011-OPS, RWB-P1-E1002-CON and rwb-reporting.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A query or path element fails schema validation on the read | 400 with the error envelope and the failing element | MSG-GEN-001 | AC1 |
| X2 | The caller reads without Platform administration R | 403 with the error envelope; nothing is returned | MSG-P4-002 | AC1 |
| X3 | A result id does not exist for the date range | 404 with the error envelope; no empty row is invented | None (the envelope carries the code and no message ID is fixed) | AC1 |
| X4 | The rerun POST arrives twice with the same key and body | The stored response is returned and the workflow is started once | None | AC6 |
| X5 | The rerun POST names a date the batch record does not show complete | 409 with the error envelope and the date | MSG-P1-001 | AC6 |
| X6 | A workflow input omits the business date | The workflow is not started; the caller sees the contract error | None | AC3 |
| X7 | A fake drifts from the document | The contract test fails and the merge is blocked | None | AC7 |
| X8 | A value is missing from the source material | The element is marked with the placeholder and one gap row is carried | None | AC2 |

X1 to X3 are the read paths of API-P1-003; X4 to X6 are the run paths of the rerun and the workflow; X7 keeps the fakes honest. No message identifier is invented here: MSG-GEN-001, MSG-P1-001, MSG-P4-002 and MSG-GEN-006 come from the platform catalogue and the legacy story, and the 404 read carries the error envelope with no message ID of its own.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the workflow kit only |
| Negotiable | Element names inside the result are settled with rwb-reporting; the path, the operations, the event, the workflow name and the rules are fixed |
| Valuable | Unblocks the app, operations and test stories of this key and the rwb-reporting dashboard on Day 1 |
| Estimable | Two documents, one interface, one workflow contract, two schemas, nine contract tables and four fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against an artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Reconciliation contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the reconciliation resource is owned by rwb-source-data (P1) and its results are read by rwb-reporting

  Scenario: AC1 The two result reads are described and validate (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-source-data is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/source-data/v1
    Then it declares GET /admin/reconciliation/results with the filters recCode, product, result, from and to, and GET /admin/reconciliation/results/{resultId}, both owned by rwb-source-data
    Then every operation names Platform administration R and its error responses 401, 403, 404 and 503

  Scenario: AC2 The result and break-row schemas carry the field IDs and no personal data (new, D-RCV-60)
    Given the result schema of the document
    When it is compared with reconciliation_result
    Then every property maps to a field ID of DF-OPS-118 to DF-OPS-129
    Then the break-row schema carries the table, the column and the business key, and the account key with its days past due, and no name, address, identity number or contact point
    Then a result row carries recCode, businessDate, productGroup, sourceCount, workbenchCount, sourceAmount, workbenchAmount, varianceCount, variancePct, tolerancePct and result

  Scenario: AC3 ReconciliationWorkflow and reconciliation are published as a typed contract (new, D-RCV-60)
    Given the workflow contract of the document
    When it is reviewed against the workflow kit
    Then it declares ReconciliationWorkflow on task queue rwb-source-data in namespace rwb-recovery with workflow ID recon-{businessDate}
    Then it declares the activity reconciliation with the business date and the source system as input and the run summary as output
    Then the run summary carries the six result rows of the date, the orphan count and the publish state
    Then a missing business date fails validation and starts no workflow

  Scenario: AC4 The AceDataReady intake is fixed with its envelope, key and dedupe (new, D-RCV-60)
    Given the AsyncAPI fragment of the document
    When a consumed message is validated
    Then it is rwb.source-data.AceDataReady.v1 on topic rwb.source-data.events.v1
    Then it uses the CloudEvents 1.0 envelope with id, source, type, specversion, time, subject and datacontenttype
    Then it carries sourceSystem, businessDate, status and completedAt and no personal data
    Then the inbox dedupes on the event id and the workflow starts once per business date and event

  Scenario: AC5 The consumed rwb-case elements are fixed and faked (new, D-RCV-60)
    Given the three consumed elements of the document
    When each is read against its owner's published contract
    Then the case query operation returns the excluded accounts for a business date with product group, account key and reason code
    Then the parameter read returns recon.tolerance.pct and case.entry.dpd for the business date
    Then the reference-data read returns LOV-PRODUCT and LOV-REC-RESULT with their versions
    Then no ACE view and no rwb_case table is named in the document

  Scenario: AC6 The error envelope, the message mapping and the rerun rule are fixed (new, D-RCV-60)
    Given the error components of the document
    When a 400, 401, 403, 404, 409 or 503 response is produced
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then MSG-P1-012, MSG-P1-001, MSG-GEN-006 and MSG-P4-002 keep their legacy text
    Then the rerun of POST /admin/jobs/{jobId}/rerun requires the Idempotency-Key header and starts ReconciliationWorkflow for the business date
    Then a replay with the same key returns the stored response and a date that is not complete is refused with 409

  Scenario: AC7 The nine contract tables are complete, the fakes match them and no lake element exists (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then the four fakes answer the paths and payloads of 12.2 and 12.4
    Then the contract tests compare each fake with the document and fail on any drift
    Then no extract, no lake target and no Power BI data set appears in any schema, path or fake
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; the document declares no other service's path | DP-13; Arch v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`; this resource consumes one event and publishes none | DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope and no personal data | Arch v5 slide 42 notes; DP-09 |
| BR4 | Every POST declares the Idempotency-Key header and stores its response; the rerun is the only POST this resource relies on | DP-09; TSD P1 v3 T-A.2 |
| BR5 | Error responses use one envelope and one message ID per condition; the legacy texts are copied unchanged | Arch v5 platform baseline; Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within major version 1; a breaking change is a new major version | Arch v5 slide 42 notes |
| BR7 | The document lists only operations owned by rwb-source-data; the case query, the parameters and the reference data are described as consumed | Ownership Map v1 |
| BR8 | No business value is fixed in the contract: the tolerance, the entry threshold and the waiting periods stay parameters | Template and Rules §R7.2 s17; DP-06 |
| BR9 | No lake element exists in the contract: the result is read, never extracted (DP-17) | Arch v5 slides 2 and 37; DP-17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the workflow contract and the event are described | In review |
| In review | Consumer sign-off | The app, operations and test stories and rwb-reporting accept the document and the fakes | Baselined |
| Baselined | Additive change | An element is added within major version 1 | Baselined |
| Baselined | Breaking change | An element is removed, renamed or retyped, or the workflow name changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the document, the AsyncAPI fragment, the workflow contract and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| rwb-reporting owner and the app, operations and test teams | Review and sign off the parts they consume |
| Platform workflow owner | Owns the workflow kit, the namespace and the worker versioning rule the contract reuses |
| Data steward | Confirms that no personal data field is declared in the event or in a break row |

The per-service login named in the security scheme is `rwb_source_data` (DP-02; Architecture v5 slide 29); the document names it as a security scheme and carries no credential.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Result resource | `resultId`, `recCode`, `businessDate`, `productGroup`, `sourceCount`, `workbenchCount`, `sourceAmount`, `workbenchAmount`, `varianceCount`, `variancePct`, `tolerancePct`, `result`, from `reconciliation_result` fields DF-OPS-118 to DF-OPS-129 |
| Break row resource | `recCode`, `businessDate`, `productGroup`, `objectName`, `fieldName`, `businessKey`, `daysPastDue` where the key is an account, and `reasonCode`; no personal field |
| Workflow input | `businessDate`, `sourceSystem`, `eventId` |
| Run summary | The rows of the date, the orphan count and the publish state RELEASED or HELD |
| Event payload | `sourceSystem`, `businessDate`, `status`, `completedAt`; no personal data |

The names `resultId`, `recCode`, `productGroup` and the element list above are fixed by this story because no source gives a path, a result shape or a workflow name (GAP-0497; ASM-0689); the field IDs are the fixed part and an element may be renamed only through the versioning rule.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`; access Platform administration R with scope applied.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/admin/reconciliation/results` | Result page filtered by `recCode`, `product`, `result`, `from` and `to` | Platform administration R |
| GET | `/admin/reconciliation/results/{resultId}` | One result row with its break rows | Platform administration R |

API-P1-003 is the identifier of the first operation (TSD P1 v3 T-A.1); the second is the single-row read the contract needs and its identifier is not fixed by any source (GAP-0497). `GET /admin/jobs` (API-P1-001) and `POST /admin/jobs/{jobId}/rerun` (API-P1-002) belong to RWB-P1-E1002-CON; this document references them as consumed and documents no shape of theirs beyond the Idempotency-Key rule.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| POST | the case query operation of the rwb-case contract | P3 rwb-case | Excluded accounts for a business date, faked |
| GET | the parameter read of the rwb-case contract | P3 rwb-case | `recon.tolerance.pct`, `case.entry.dpd`, faked |
| GET | the reference-data read of the rwb-case contract | P3 rwb-case | `LOV-PRODUCT` and `LOV-REC-RESULT`, faked |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1, RWB-P1-E1002-CON | The run trigger this resource is bound to, documented by its own story |

The three rwb-case elements are one hop each with a 2 s timeout and a breaker (DP-11). The document names no path of the case query beyond the contract's own operation id, because the rwb-case baseline owns the path and this story must not restate it (DP-11; BR7).

#### 12.3 Events published

None. `rwb.source-data.events.v1` carries `AceDataReady` and `AceDataLate`, and both belong to RWB-P1-E1013-APP; the reconciliation publishes no fact of its own and writes no outbox row.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | `sourceSystem`, `businessDate`, `status`, `completedAt`; starts `ReconciliationWorkflow` after the case list step; inbox dedupe on the event id |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `ReconciliationWorkflow` | Workflow, one run per business date, workflow ID `recon-{businessDate}` | `rwb-source-data` | Input and output schemas; retry policy; search attributes `BusinessDate`, `RecSource` |
| `reconciliation` | Activity | `rwb-source-data` | Business date and source system in; run summary out; one transaction for the rows and the publish state |
| `ReconciliationQuery` | Published interface | — | The typed read the reporting projection and the admin surface call: results by date range and filter, and one result by id; one implementation behind 12.1 |

The interface name is fixed here and no source gives one (GAP-0497; ASM-0689). It is a Java type inside the service and not a shared library across services: the cross-service path is REST (DP-11).

#### 12.6 Schedules

None. The workflow is event-started; the only daily start of the service is the `DailyCaseList` Schedule of RWB-P1-E1002-CON, which this resource does not register or own (DP-10; Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `reconciliation_result` | P1 (`rwb_source_data`) | The result resource, unique on `(rec_code, business_date, product_group)` |
| `case_list_row` | P1 (`rwb_source_data`) | Read for the two count checks; `publish_status` written for the date |
| `data_product_load` | P1 (`rwb_source_data`) | Read for the completeness gate of the date |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_source_data` | Inbox dedupe of the consumed event and the stored rerun response |

No other table is named in the contract, no `rwb_case`, `rwb_treatment` or `rwb_payment` table is read, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| RWB-P1-E1002-CON fake | A `case_list_row` set for a business date, an `AceDataReady` event and the rerun answer | App story, contract tests |
| RWB-P3-E1042-CON fake | `recon.tolerance.pct` 0.00 and 0.10, `case.entry.dpd` 90, `recon.treatment.days` 2, `recon.payment.days` 1 | App story, contract tests |
| RWB-P3-E1043-CON fake | `LOV-PRODUCT` and `LOV-REC-RESULT` with versions | App story, contract tests |
| View fixture | The eight views of RWB-P1-E1069-APP with a batch row and a failing `v_ace_account` stub | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed plus the rerun binding | Result reads; case query, parameters and reference data; one hop, 2 s |
| Kafka | None published, 1 consumed | `rwb.source-data.AceDataReady.v1` |
| Temporal | 1 workflow, 1 activity | `ReconciliationWorkflow`, `reconciliation` |
| File | None | No extract, no lake target, no Power BI data set (DP-17) |

### 13. Solution plan

**Deliverables.** `openapi/rwb-source-data-reconciliation-v1.yaml` (OpenAPI 3.1), `asyncapi/rwb-source-data-acedataready-v1.yaml` (AsyncAPI 3 fragment), `contract/reconciliation-workflow.yaml` with the workflow, the activity and the `ReconciliationQuery` interface, `contract/error-envelope.yaml`, the idempotency and versioning rules in the contract README, and the four WireMock mappings.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 is the pattern this baseline delivers: the published interface of the legacy story is replaced by an OpenAPI document, a workflow contract and one typed query interface behind them. DP-17 is used as a removal, and the contract test of AC7 enforces it. DP-03 and DP-19 are named in the contract only where a run record and the admin surface consume it; the baseline builds neither.

**Build steps**

1. OpenAPI skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The two result reads and their schemas, with the field IDs and the break rows.
3. AsyncAPI fragment for the consumed event, with the CloudEvents envelope and the dedupe rule.
4. The workflow contract: `ReconciliationWorkflow`, `reconciliation`, the run summary and the retry policy.
5. The `ReconciliationQuery` interface and its documented answer shapes.
6. Error envelope and message mapping, with the legacy texts copied unchanged.
7. The Idempotency-Key rule of the rerun and the versioning rule.
8. The four fakes and the stub fixtures.
9. The contract tests; a drift between a fake and the document fails the build.
10. Baseline tag and the consumer sign-off note.

**Done when.** The OpenAPI and AsyncAPI artefacts validate in the pipeline, the workflow contract is accepted by the workflow kit owner, the contract tests pass, the four fakes answer every consumed element and the app, operations and test stories and rwb-reporting have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A product breaks the tolerance | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | The batch for the date is not complete | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | A read without Platform administration R | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required query or path element is missing | Enter {field}. |
| MSG-GEN-006 | A downstream is unavailable | {system} is not available. Your request is queued and will be retried. |

The message IDs are contract elements and the texts are the agreed texts, copied unchanged from the legacy story and the platform catalogue; no new wording is introduced. A 404 read carries the error envelope and no message ID of its own.

### 15. Screens and states

The contract serves the admin result list rendered through the gateway-bff composite route (DP-19) and the rwb-reporting dashboard that reads the same operations. The screen field list and the composite route specification belong to the platform edge story and to rwb-reporting; this story fixes only the case of the merge, which is the result row and its break rows. No Power BI report is in scope.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-011-07 | AC1, AC6; the 403 path of the reads and the rerun | Contract | A read and a rerun as RW-CASEOWN, refused with MSG-P4-002; a read and a rerun as RW-PLATADM, accepted |
| TC-E1-011-01 | AC2, AC7 | Contract | The result schema against DF-OPS-118 to DF-OPS-129; a clean date with three product groups |
| TC-E1-011-02 | AC2, AC3 | Contract | A break row for 12 SSME accounts; the run summary of the date |
| TC-E1-011-03 | AC2, AC8 | Contract | The tolerance element on two rows, 0.10 and 0.11 percent; a placeholder element |
| TC-E1-011-04 | AC6, AC8 | Contract | A rerun on a date the batch record does not show complete; 409 with MSG-P1-001 |
| TC-E1-011-05 | AC3, AC6 | Contract | A rerun with a key; the same key replayed; the stored response returned |
| TC-E1-011-06 | AC3, AC4 | Contract | Two runs for one business date on two workers; the inbox dedupe on one event id |
| TC-E1-011-08 | AC2, AC7 | Contract | A break row for `party_ext` person_key P0099881 with no personal field |
| TC-E1-011-09 | AC3, AC5 | Contract | An unavailable view in the fake; a case query fake with the 12 missing cases |

This story owns no legacy acceptance criterion, so the nine rows are the legacy test cases of RWB-E1-011 listed against the new criteria they exercise: their IDs, their order and their data are kept, and the Covers column names this story's own criteria only where the legacy case tests the contract's artefact. The legacy criteria themselves are owned by RWB-P1-E1011-APP and the sibling slices and proven end to end in RWB-ITG-E1011-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code or in the contract: the tolerance, the entry threshold and the waiting periods stay parameters, and the product groups and the result list stay reference data.
- No personal data in events, workflow inputs or logs and none in an event schema, an example or a fake: the event carries a source system, a date, a status and a time, and a break row carries business keys and account keys only.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: the document names no ACE table and no `rwb_*` schema other than `rwb_source_data`.
- No cross-schema read and no cross-schema key: the contract names only P1's tables, and no element of it is a foreign key into another schema (DP-01).
- One REST base, one topic, one task queue per service; a document that names another service's base, topic or queue fails the review (DP-13, DP-14).
- No lake element: an extract, a lake target or a Power BI data set in the document fails AC7 (DP-17).
- Every example is synthetic; no production payload is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the count in `v_ace_account`, and every business key resolves to an ACE row | Result resource, `ReconciliationWorkflow`, `reconciliation`, `AceDataReady` | TC-E1-011-01, TC-E1-011-02, TC-E1-011-07 |
| REQ-RDF-008 | Reconciliation breaks and referential completeness are reported to the data product owner | Break-row schema, the single-row read, the run summary | TC-E1-011-02, TC-E1-011-08 |
| REQ-CWC-004 | Exclusion rules are data | The consumed case query element and the exclusion reason code | TC-E1-011-09 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed elements and their client budget | TC-E1-011-09 |

### 19. Out of scope

- The implementation of the checks, the workflow and the read operations (RWB-P1-E1011-APP).
- The deployment, the chart, the worker, the KEDA scaling, the alerts and the rerun binding (RWB-P1-E1011-OPS).
- The jobs and case-list operations `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun`: RWB-P1-E1002-CON, referenced here and not restated.
- The rwb-case case query, parameter and reference-data contracts: consumed and faked, never defined here.
- The REC-03, REC-04 and cross-service REC-05 elements: the local contracts of RWB-P3-E1011-APP, RWB-S5-E1011-APP and RWB-P6-E1011-APP.
- The rwb-reporting dashboard and its own document.
- Any lake extract or Power BI data set, which the target removes (DP-17; GAP-0495).
