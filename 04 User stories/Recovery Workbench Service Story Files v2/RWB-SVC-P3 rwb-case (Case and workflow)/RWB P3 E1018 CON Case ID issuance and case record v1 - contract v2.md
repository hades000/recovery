# RWB-P3-E1018-CON Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1018-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Contract version | v1 (REST path prefix /v1; event channel rwb.case.events.v1) |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-P3-E1018-CON-16) |
| Patterns applied | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-001, FR-P3-002, FR-P3-003, FR-P3-004, FR-P3-005, FR-P3-006, FR-P3-007, FR-P3-012, FR-P3-030, FR-P3-031, FR-P3-035) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-018 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 44 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of rwb-case for the case resource: an OpenAPI 3.1 document for the case operations, an AsyncAPI document with the six event schemas under a CloudEvents envelope, the error envelope, the Idempotency-Key rule on every POST, the versioning rule, the contract tables of section 12 and the contract fakes for rwb-source-data, rwb-access and rwb-decision**, so that **every consuming team and the app, operations and test stories of this legacy key can build against a fixed, testable contract on Day 1 without waiting for rwb-case to be built**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). rwb-case publishes sixteen REST operations and six event types; the case-creation capability of RWB-E1-018 needs four of those operations, two event types it publishes and two it consumes. If the field-level contract is agreed once and faked, the app story builds in parallel with rwb-source-data, rwb-access and rwb-decision, and a change in any of them is caught in a contract test rather than in an integration window. The baseline also fixes the naming that the checks require: schema rwb_case, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, event names `rwb.case.<Event>.v1`, task queue `rwb-case` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.case`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice.
- The outbox, inbox and idempotency library is available as a reference for the table names and columns (RWB-PLT-TE006-CON, DP-09).
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners are taken from the Ownership Map only; rwb-case never documents an operation owned by another service.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the four case operations the capability needs, with the shared components used across the sixteen rwb-case operations.
2. Draft the AsyncAPI document for `rwb.case.events.v1` with the six event types and the shared CloudEvents 1.0 envelope.
3. Agree the error envelope and map each HTTP status to its message ID.
4. State the Idempotency-Key rule for every POST and the stored-response behaviour.
5. State the versioning rule for the REST surface and for the event schemas.
6. Publish the contract tables of section 12 (nine sub-tables) and the three contract fakes.
7. Add the contract tests: schema validation, envelope validation, error mapping, idempotency replay and version negotiation.
8. Tag the baseline and hand it to RWB-P3-E1018-APP, RWB-P3-E1018-OPS and every consuming service.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request body fails schema validation | 400 with the error envelope and the failing pointer | MSG-P3-030 | AC3 |
| X2 | A required header is missing on a POST | 400 with the error envelope naming the header | MSG-P3-031 | AC4 |
| X3 | The same Idempotency-Key is replayed with a different body | 422 with the error envelope; the stored response is not overwritten | MSG-P3-032 | AC4 |
| X4 | A caller asks for a major version the service does not serve | 404 with the error envelope and the served major versions | MSG-P3-033 | AC5 |
| X5 | A consumer cannot deserialise an event | The schema registry validation fails the build; the event is not published | None | AC2 |
| X6 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X7 | A field-level definition is missing from the source material | The field is marked with the placeholder and one gap row is carried | None | AC1 |

Message IDs MSG-P3-030 to MSG-P3-033 are the contract-level codes of this baseline; the business messages MSG-P1-001, MSG-P3-025, MSG-P3-027, MSG-P4-002, MSG-P4-003 and MSG-P7-003 keep their text from the legacy story and are carried unchanged in the error envelope mapping.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and the Ownership Map only |
| Negotiable | Field-level detail is settled with the consumers; the named operations, events, envelope and rules are fixed by the target architecture |
| Valuable | Unblocks the app, operations and test stories of this legacy key on Day 1 and every consumer of the case resource |
| Estimable | Two documents, one error envelope, two rules, nine contract tables, three fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Case resource contract baseline for rwb-case

  Background:
    Given the service naming rule of the platform library is in force
    Given the six rwb-case event types are CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged and TimerBreached

  Scenario: AC1 The OpenAPI 3.1 document describes the case operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/case/v1
    Then it declares GET /cases, GET /cases/{caseId}, GET /cases/{caseId}/accounts and GET /cases/{caseId}/parties with the owner rwb-case
    Then every operation names its security right and its error responses 401, 403, 404 and 503

  Scenario: AC2 The AsyncAPI document carries the six event schemas (new, D-RCV-60)
    Given the AsyncAPI document of rwb-case is published
    When it is validated against the AsyncAPI 3 schema
    Then it declares the topic rwb.case.events.v1
    Then it declares the six event types rwb.case.CaseCreated.v1, rwb.case.CaseAllocated.v1, rwb.case.CaseAllocationFailed.v1, rwb.case.CaseTransferred.v1, rwb.case.CaseStateChanged.v1 and rwb.case.TimerBreached.v1
    Then every message uses the CloudEvents 1.0 envelope with the attributes id, source, type, specversion, time, subject and datacontenttype
    Then every message carries IDs and facts only and no personal data field

  Scenario: AC3 The error envelope is one shape for every failure (new, D-RCV-60)
    Given the error envelope component of the document
    When a 400, 401, 403, 404, 409, 422 or 503 response is produced
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then the messageId is one of the contract or business message IDs and the text is the agreed text
    Then the response carries the problem media type and the trace identifier

  Scenario: AC4 Every POST requires an Idempotency-Key (new, D-RCV-60)
    Given a POST operation in the document
    When the request omits the Idempotency-Key header
    Then the service answers 400 with the error envelope and MSG-P3-031
    When the same key is sent twice with the same body
    Then the second call returns the stored response and no second state change
    When the same key is sent with a different body
    Then the service answers 422 with the error envelope and MSG-P3-032

  Scenario: AC5 The versioning rule is stated and enforced (new, D-RCV-60)
    Given the document declares major version 1 in the path
    When a caller uses an unsupported major version
    Then the service answers 404 with the error envelope and the served major versions
    Then the event schemas are versioned in the registry with BACKWARD compatibility and the event name carries the schema version
    Then a breaking change to a published schema requires a new major version

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then the three contract fakes answer the paths and payloads of 12.2
    Then the contract tests compare the fakes with the document and fail on any drift

  Scenario: AC7 Every business rule of section 8 is covered by a criterion or test (new, D-RCV-60)
    Given the business rules BR1 to BR8 of section 8
    When the criteria and test cases of this story are reviewed
    Then each rule BR1 to BR8 is traced to a test case in section 16
    Then no rule of section 8 is left without a test

  Scenario: AC8 A failed event is retried and a timed-out activity is refused (new, D-RCV-60)
    Given an event publication fails
    When the publication is retried
    Then the event is routed to the .dlt topic once the retries are exhausted
    Then the retry count is Not specified in the source documents (NEWAC-RWB-P3-E1018-CON-AC8)
    Given a request exceeds its timeout
    Then the service answers with the error envelope and the timeout status Not specified in the source documents (NEWAC-RWB-P3-E1018-CON-AC8)

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case in a state from which the requested change is not allowed
    When the status change is requested
    Then the service answers 409 with the error envelope
    Then no CaseStateChanged event is emitted

  Scenario: AC10 The CaseCreated event and the decision record are asserted on the platform (new, D-RCV-60)
    Given the ALS batch is seeded through the W1J01 harness
    When DailyCaseRun creates a case
    Then rwb.case.CaseCreated.v1 is published on rwb.case.events.v1 with caseId, caseNo, productGroup, accounts and businessDate
    Then the decision is recorded through P7 as rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 under DP-03

  Scenario: AC11 A key and view with no row come back as a break row in the same answer (new, D-RCV-60)
    Given a key and a view of REC-05 with no matching row
    When the candidate read answers
    Then the same response carries one break row with keyType ACCOUNT or PERSON, businessKey, viewName and businessDate
    Then the break rows are counted in the run log of the call and listed for the data steward and the ACE team
    Then no dq_ table returns and no table is created for the break rows

  Scenario: AC12 P1 writes the extension flags through two PUT operations by business key (new, D-RCV-60)
    Given the exclusion screen records a decision on a case
    When the screen confirms with its right and its audit entry
    Then P1 writes party_ext and account_ext through two PUT operations by business key
    Then the body carries all four party flags, so party_ext.vulnerable is always written by the caller and never defaulted by P1
    Then a repeat of the same body leaves one row and a changed body replaces the flags on the same key with a version increment

  Scenario: AC13 product_group is returned as read, never mapped and never validated (new, D-RCV-60)
    Given v_ace_account.product_category holds a value
    When the candidate row is returned
    Then product_group is that value, unvalidated and unmapped
    Then a value outside LOV-PRODUCT is returned as read and is never coerced, dropped or defaulted
    Then any mapping, label or validation is the consumer's, through the rwb-case reference-data contract
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/case/v1`; a document never declares another service's path | DP-13; Arch v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by caseId and carries no personal data | Arch v5 slides 42 and 43 notes; DP-09 |
| BR4 | Every POST declares the Idempotency-Key header and stores its response | Arch v5 slide 11; DP-09 |
| BR5 | Error responses use one envelope and one message ID per condition; business message texts are copied unchanged from the legacy story | Arch v5 platform baseline; Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Arch v5 slide 42 notes (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-case; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR8 | No business value is fixed in the contract: the threshold, the exclusion reasons and the bands stay data | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The four case operations and the six events are described | In review |
| In review | Consumer sign-off | The app, operations and test stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the document, the AsyncAPI file and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Consuming teams (app, operations, test, and the rwb-source-data, rwb-access and rwb-decision owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an event |

The per-service login name behind the document's security scheme is Not specified in the source documents (GAP-0675; ASM-1222); the document names it "the rwb-case login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Case resource | `id`, `caseNo`, `productGroup`, `primaryPersonKey`, `status`, `stageCode` (DF-CAS-006), `routeCode` (DF-CAS-008), `entryDate`, `dpdAtEntry`, `exposureBand`, `totalOutstandingAtEntry`, `deviationOpen`, `legalHold`, taken from `recovery_case` fields DF-CAS-001 to DF-CAS-023 | Not specified in the source documents (DOR-RWB-P3-E1018-CON-7) |
| Case account resource | `id`, `caseId`, `accountKey`, `isPrimary`, `linkedFrom`, `linkedTo`, from `case_account` fields DF-CAS-024 to DF-CAS-029 | Not specified in the source documents (DOR-RWB-P3-E1018-CON-7) |
| Case party resource | `id`, `caseId`, `personKey`, `partyRole`, `roleFrom`, `roleTo`, from `case_party` fields DF-CAS-030 to DF-CAS-035 | Not specified in the source documents (DOR-RWB-P3-E1018-CON-7) |
| Exclusion resource | `accountKey`, `businessDate`, `reasonCode`, `ruleId`, `ruleVersion`, from `case_entry_exclusion` fields DF-CAS-056 to DF-CAS-061 | Not specified in the source documents (DOR-RWB-P3-E1018-CON-7) |
| Event payloads | IDs, codes, dates and amounts only; no name, address, identity number or contact point | Not specified in the source documents (DOR-RWB-P3-E1018-CON-7) |

The exact field-level schema of the new case resource (types, lengths, required flags per property and the page and sort parameters) is Not specified in the source documents (GAP-0676; ASM-1223); this story fixes the field names above and leaves the field-level detail to the baseline review.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-case (P3); base `/api/recovery/case/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/cases` | CasePage with the case-number search and the paging parameters (GAP-0676) | Case record R |
| GET | `/cases/{caseId}` | Case | Case record R |
| GET | `/cases/{caseId}/accounts` | CaseAccount[] | Case record R |
| GET | `/cases/{caseId}/parties` | CaseParty[] | Case record R |

The full rwb-case surface of sixteen operations is published in the service API file; this baseline documents the four operations the case-creation capability needs and keeps the shared components reusable for the rest. The task raise the capability needs (legacy `CaseWorkflowApi.raiseTask` with caseId, taskCode, ownerRole and reasonCode) is one of the remaining operations: its path is Not specified in the source documents (GAP-1085) and is published in the service API file and recorded in the Ownership Map before the app story is built against it.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/accounts/{id}` | P1 rwb-source-data | Account and arrears fields, faked |
| GET | `/api/recovery/source-data/v1/customers/{id}` | P1 rwb-source-data | Customer row and extension flags, faked |
| GET | `/api/recovery/source-data/v1/freshness` | P1 rwb-source-data | Batch completeness for the business date, faked |
| GET | `/api/recovery/decision/v1/rule-models/{n}/{v}` | P7 rwb-decision | Package model and checksum, faked |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and right check, faked |

#### 12.3 Events published

| Event | Topic | Owner | Schema |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 | caseId, caseNo, productGroup, accounts, businessDate |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 | caseId, caseNo, queueCode, ownerReference, allocationRuleId, packageVersion |
| `rwb.case.CaseAllocationFailed.v1` | `rwb.case.events.v1` | P3 | caseId, caseNo, queueCode, reasonCode, allocationRuleId, packageVersion |
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 | caseId, caseNo, transferReasonCode, fromReference, toReference |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 | caseId, caseNo, fromStatus, toStatus, ruleId, packageVersion, decidedAt |
| `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | P3 | caseId, caseNo, timerId, timerType, expiresAt |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 | decision record reference, ruleId, ruleVersion, finalCall, decidedAt |

The six `rwb.case.*` types are the rwb-case event contract; DecisionRecorded is the shared ledger event the local decision-record library publishes (DP-03).

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | Business date, source ALS, freshness summary; starts DailyCaseRun |
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 | Package code, version label, checksum, valid-from date; refreshes the KieBase cache |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case ID | `rwb-case` | Input and signal schemas, search attributes CaseId, Stage, ProductGroup, QueueCode |
| DailyCaseRun | Workflow, started by AceDataReady with a daily Schedule fallback; workflow ID: Not specified in the source documents (CG-ALL-3465); duplicate-start policy: Not specified in the source documents (CG-ALL-3465) | `rwb-case` | Input schema (business date, source), run record shape |
| allocate, transfer, rebalance | Activities | `rwb-case` | Input and output schemas |
| EvaluateRules, RecordAndApply | Activities (workflow kit) | `rwb-case` | Package code, facts and date in; rule ID, package version and outputs out; one transaction for the record and the state change |

#### 12.6 Schedules

| Schedule | Cadence | Documented fields | Legacy reference |
|---|---|---|---|
| DailyCaseRun | Daily with AceDataReady as the primary trigger | Schedule ID, overlap policy SKIP, catch-up window, business date input | JOB-02 Case creation |
| Allocation step | Daily by 07:00 inside DailyCaseRun | Step order and timeout | JOB-03 Morning allocation |

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| recovery_case | P3 (rwb_case) | Case resource |
| case_account | P3 (rwb_case) | Case account resource |
| case_party | P3 (rwb_case) | Case party resource |
| case_entry_exclusion | P3 (rwb_case) | Exclusion resource with rule ID and package version |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency envelope of the contract (DP-09) |

No other table is named in the contract, and no table of another service is read (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data WireMock | `GET /accounts/{id}`, `GET /customers/{id}`, `GET /freshness` and the `listEligibleAccounts` fixture | App story, contract tests |
| rwb-access WireMock | `POST /authorise` with a granted answer and a refused answer for a role without Case record R | App story, contract tests |
| rwb-decision WireMock | `GET /rule-models/{n}/{v}` for ENTRY "ENTRY-2026.11", EXCLUSION "EXCL-2026.11", rule IDs EXCL-004 and EXCL-006 | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 5 consumed | Case reads; source data, decision models and authorise; one hop, 2 s timeout |
| Kafka | 7 published, 2 consumed | Six rwb.case events and DecisionRecorded published; AceDataReady and RulePackageInForce consumed |
| Temporal | 2 workflows, 5 activities | CaseWorkflow, DailyCaseRun; allocate, transfer, rebalance, EvaluateRules, RecordAndApply |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-case-v1.yaml` (OpenAPI 3.1), `asyncapi/rwb-case-v1.yaml` (AsyncAPI 3) with the seven message schemas, `contract/error-envelope.yaml`, the idempotency and versioning rules in the contract README, and the three WireMock mappings.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The four case operations and their resources, with the field names of section 11; the field-level detail is agreed under GAP-0676.
3. AsyncAPI 3 document with `rwb.case.events.v1`, the six event types, the CloudEvents envelope and the registry versioning rule.
4. Error envelope and the message-ID mapping, business texts copied unchanged.
5. Idempotency-Key rule and the stored-response behaviour, and the versioning rule.
6. The three contract fakes and the stub fixtures.
7. The six contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note.

**Done when.** The OpenAPI and AsyncAPI documents validate in the pipeline, the six contract tests pass, the three fakes answer every consumed path and the app, operations and test stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-030 | A request body or query fails schema validation | The request could not be read: {detail}. |
| MSG-P3-031 | A required header is missing on a POST | The request is missing {header}. |
| MSG-P3-032 | An Idempotency-Key is replayed with a different body | This request was already sent with different content. |
| MSG-P3-033 | An unsupported major version is requested | This version of the service is not available. |
| MSG-P1-001 | DailyCaseRun waiting for a complete ALS batch | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-025 | Yearly case number range used up | Case numbers for {year} are used up. New cases are on hold until the range is extended. |
| MSG-P3-027 | No ENTRY or EXCLUSION version is in force on the business date | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P4-002 | Read without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed.

While v_ace_batch_status does not exist (until RWB-ACE-001 is deployed), the batch gate answers as for an incomplete batch: 409 with MSG-P1-001, no candidate and no break row, and DP01 is never stamped LOADED for the date, so no case is created for that date. The gate is read from the view only and is never inferred from data_as_of, a row count or a file. The refusal status 409 and the two filled fields of MSG-P1-001 are settled in ASM-B-P1-07-E1018-4.

### 15. Screens and states

The contract serves the two screens of the case-creation capability: SCR-02 Case list (Loading; empty; list; filtered; error: Not specified in the source documents (CG-ALL-3475); no access: Not specified in the source documents (CG-ALL-3475)) and SCR-03 Case record (Loading; read only; empty: Not specified in the source documents (CG-ALL-3476); error: Not specified in the source documents (CG-ALL-3476); no access: Not specified in the source documents (CG-ALL-3476)). The gateway-bff composite route (DP-19) calls the case operations and the rwb-source-data operations in parallel and merges the answers. The composite route specification, the screen field list and the masking of customer fields are Not specified in the source documents (GAP-0674; ASM-1221); the OpenAPI document fixes the case side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1018-CON-01 | AC1 | Contract | The OpenAPI 3.1 document validates; the four case operations and their error responses are present |
| TC-P3-E1018-CON-02 | AC2 | Contract | The AsyncAPI 3 document validates; six event types, CloudEvents envelope, no personal data field |
| TC-P3-E1018-CON-03 | AC3 | Contract | 400, 401, 403, 404, 409, 422 and 503 responses carry one envelope and a valid message ID |
| TC-P3-E1018-CON-04 | AC4 | Contract | A POST without the header is refused; a replay returns the stored response; a replay with a different body is refused |
| TC-P3-E1018-CON-05 | AC5 | Component | An unsupported major version is refused; the registry rejects a backward-incompatible schema |
| TC-P3-E1018-CON-06 | AC6 | Component | The nine contract tables are complete and each fake matches its consumed path |
| TC-P3-E1018-CON-07 | AC6 | Component | Boundary: a read or write of a table not named in §12.7 is refused; only the five tables of §12.7 are used |
| TC-P3-E1018-CON-08 | BR1 | Contract | The base is /api/recovery/case/v1; a document declaring another service's path is refused |
| TC-P3-E1018-CON-09 | BR2 | Contract | Event names are rwb.<short>.<Event>.v1 on rwb.<short>.events.v1, with retry and .dlt topics |
| TC-P3-E1018-CON-10 | BR3 | Contract | Every event carries the CloudEvents 1.0 envelope, is keyed by caseId and carries no personal data |
| TC-P3-E1018-CON-11 | BR4 | Contract | Every POST declares the Idempotency-Key header and stores its response |
| TC-P3-E1018-CON-12 | BR5 | Contract | Error responses use one envelope and one message ID per condition; message texts match the legacy story |
| TC-P3-E1018-CON-13 | BR6 | Component | A backward-compatible schema change is accepted within the major version; a breaking change requires a new major version |
| TC-P3-E1018-CON-14 | BR7 | Contract | The document lists only rwb-case operations; a consumed operation is described as consumed |
| TC-P3-E1018-CON-15 | BR8 | Contract | No threshold, exclusion reason or band value is fixed in the contract |
| TC-P3-E1018-CON-16 | AC7 | Contract | Each rule BR1 to BR8 of section 8 is traced to a test case; no rule is left without a test |
| TC-P3-E1018-CON-17 | AC8 | Component | A failed event is retried and then routed to the .dlt topic; a request past its timeout answers with the error envelope and a timeout status Not specified in the source documents (NEWAC-RWB-P3-E1018-CON-AC8) |
| TC-P3-E1018-CON-18 | AC9 | Component | A status change the model does not allow is refused with 409 and the error envelope; no CaseStateChanged event is emitted |
| TC-P3-E1018-CON-19 | AC10 | Component | The ALS batch is seeded through the W1J01 harness; rwb.case.CaseCreated.v1 is on rwb.case.events.v1 and the P7 DecisionRecorded entry is on rwb.decision-record.v1 |
| TC-P3-E1018-CON-20 | AC11 | Component | A key and view with no row yields one break row with keyType, businessKey, viewName and businessDate; the run log counts it and no table is created |
| TC-P3-E1018-CON-21 | AC12 | Component | P1 writes party_ext and account_ext through two PUT operations by business key; all four party flags are in the body; a repeat leaves one row and a changed body increments the version |
| TC-P3-E1018-CON-22 | AC13 | Contract | product_group is the product_category value as read; MORTGAGE and HIRE_PURCHASE come back unchanged and a value outside LOV-PRODUCT is neither coerced nor dropped |

### 17. Guardrails

- No business value in the contract: the threshold, the exclusion reasons, the exposure bands and the status list stay data in the parameters, the reference tables and the rule packages.
- No personal data in an event schema, an example or a fake: IDs, codes, dates and amounts only.
- The contract names only rwb-case tables and only operations owned by rwb-case; no other service's table is read or documented as provided (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due | Case resource, CaseCreated, DailyCaseRun input | TC-P3-E1018-CON-01, TC-P3-E1018-CON-02 |
| REQ-CWC-002 | Case ID RW-YYYY-NNNNNN, never reused | `caseNo` pattern in the Case resource and in every event | TC-P3-E1018-CON-01, TC-P3-E1018-CON-02 |
| REQ-CWC-003 | One case per customer and product | Case resource `primaryPersonKey`, `productGroup`; CaseCreated accounts | TC-P3-E1018-CON-01 |
| REQ-CWC-004 | Exclusion rules as data | rule ID and package version in the exclusion resource and CaseStateChanged | TC-P3-E1018-CON-01, TC-P3-E1018-CON-02 |
| REQ-CWC-005 | State model with one state at a time | `status` as a list reference; CaseStateChanged | TC-P3-E1018-CON-01, TC-P3-E1018-CON-02 |
| REQ-CWC-016 | Every workflow event logged with rule ID and version | DecisionRecorded schema and the evaluation activity contract | TC-P3-E1018-CON-02, TC-P3-E1018-CON-06 |
| REQ-CHO-004 | One agreed hand-over point in days past due for every rule and report | `dpdAtEntry`, `entryDate` in the Case resource | TC-P3-E1018-CON-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Consumed operations with the 2 s client budget | TC-P3-E1018-CON-06 |

### 19. Out of scope

- The implementation of the case creation, the grouping and the number issuer (RWB-P3-E1018-APP).
- The deployment, the Helm chart, the topic and queue provisioning and the dashboards (RWB-P3-E1018-OPS).
- The operations of other services: the rwb-source-data, rwb-access and rwb-decision contracts are consumed and faked, never defined here.
- The remaining twelve rwb-case operations beyond the four the case-creation capability needs; they are published in the same service API file by their own stories.
- The gateway-bff composite route and the screen field list (platform edge story and RWB-P3-E1023-APP).
- The field-level completeness of the case resource schema (GAP-0676).
