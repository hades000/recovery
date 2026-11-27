# RWB-P3-E2012-CON Manual transfer and reassignment screen with reason

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004.

| Item | Value |
|---|---|
| Story key | RWB-P3-E2012-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Contract version | v1 (REST /api/recovery/case/v1; event rwb.case.CaseTransferred.v1) |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Open decisions | DL23 (assumptions ASM-1232, ASM-1237, ASM-1259, ASM-1560) |
| Size | Not specified in the source documents (DOR-RWB-P3-E2012-CON-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON (tracked; platform contract stories gate the build at pickup) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-013, FR-P3-017, FR-P3-018, FR-P3-019, FR-P3-021, FR-P3-030, FR-P3-031) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-012 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 18 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **consumer of the case service (the gateway-bff composite route, the transfer screen and the test stories of this key)**, I want **one published, versioned contract for the manual transfer and reassignment of a case — single and in a selection — with its request and response shapes, its mandatory reason-code list, its idempotency rule, its rights, its refusals, its decision-record evidence, its event and its one-hop budget**, so that **the screen, the deployment and the tests build on Day 1 against one agreed, testable shape without waiting for the transfer capability of rwb-decision, rwb-access or rwb-deviation to run**.

This story is the contract baseline of the manual move of `rwb-case`:

- REST base `/api/recovery/case/v1`, OpenAPI 3.1, operation `POST /cases/{caseId}/transfer`.
- Topic `rwb.case.events.v1`, event `rwb.case.CaseTransferred.v1`, AsyncAPI 3.0, CloudEvents 1.0.
- Temporal task queue `rwb-case` in namespace `rwb-recovery`; Java package `th.co.scb.ace.workbench.recovery.case`.
- Schema `rwb_case`, owned by P3, under the per-service login of DP-02, referred to as "the rwb-case login (DP-02)" and never by a literal name.

It carries no business logic. It fixes the artefacts that RWB-P3-E2012-APP builds and RWB-P3-E2012-OPS deploys, and it publishes the fakes that both build against.

The contract does not invent the manual move. The operation, its request, its response, its errors and its authorisation are the ones recorded in RWB-P3-E1021-CON; this story fixes what that baseline left to the screen: the single-and-selection shape, the reason list as a run-time read, the idempotency storage rule, the two pre-check answers, the decision-record evidence a move must carry, and the error-code-to-status binding of the manual path.

### 2. Business rationale

Contract-first REST with one hop and a 2 s budget is the decoupling rule (DP-11, ADR-020). A manual move is the one write in the case service that a person triggers and then watches, so the seam is load-bearing twice: the screen needs an answer inside the user's wait, and the record of the move has to be provable afterwards. If the shape is agreed and faked on Day 1, three teams move at once — the app story builds the manual path and the bulk runner against the fakes, the deployment story wires readiness, metrics and alerts against the same elements, and the test stories of this key read one set of statuses and message IDs.

The contract also fixes the two things that changed under D-RCV-60 and that a consumer could otherwise guess: the reason list is read as reference data of `rwb-case` on every form load and never frozen into a client (DP-07), and the rule answer is the `RuleResult` of the embedded Drools kit behind the `EvaluateRules` activity, not a rule table read by the caller (DP-04). Both appear as named components, so a consumer can see where a value comes from without reading a table (DP-01).

The last thing it fixes is what the move proves. A manual transfer is a decision, and a decision is evidenced by a record that holds the case, the rule ID, the package version, the from and to queue and owner and the reason code, hash-chained to the previous record and published on `rwb.decision-record.v1` (DP-03, ADR-022). Without that element in the contract, a later screen or a later report would ask the case service to vouch for a move it cannot prove.

### 3. Preconditions

- The service facts of Template and Rules v1 are in force: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, queue `rwb-case`, package `th.co.scb.ace.workbench.recovery.case`, and the schema and login per service of DP-02 and DP-15.
- The Ownership Map confirms P3 owns `POST /cases/{caseId}/transfer`, `GET /cases/{caseId}`, `GET /queues`, `GET /queues/{queueId}/cases` and `POST /queues/{queueId}/placements`, and the tables `recovery_case`, `assignment`, `queue`, `queue_member` and `task`. This story declares no operation outside that list and no table outside that list.
- RWB-P3-E1021-CON version 1 is published: it fixes the transfer operation, `TransferRequest`, `Assignment`, `TransferReason`, `RuleResult`, `DecisionRecordRef`, the error envelope and `CaseTransferred`. This story narrows none of them and adds no field to the request or the response.
- The platform envelopes are in force: CloudEvents 1.0 for the event, RFC 9457 problem responses with `messageId`, `detail`, `instance` and `traceId` for the errors, and the naming library for the topic and the event name (DP-14).
- The embedded Drools kit contract of RWB-PLT-E1072-CON and the local decision-record library of RWB-PLT-E1027-CON are in force, so `RuleResult`, `NoPackageInForce` and the record reference are the platform elements and not local inventions (DP-03, DP-04).
- The transfer reason list is the reference data of `rwb-case`, read at run time with `GET /api/recovery/case/v1/admin/lists/{listCode}` from the reference-data contract of RWB-P3-E1043-CON (Ownership Map api row, ASM-0041); the values in force are the intended set R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue. Who may add or retire a code is Not specified in the source documents (GAP-0712; ASM-1259).
- No build dependency: this story is Day 1 and sits in contract group `CG-W2` (Template and Rules §R5.7).

### 4. Flow

1. Draft the manual section of the OpenAPI 3.1 document: `POST /cases/{caseId}/transfer` with `TransferRequest` in, `Assignment` out, the `Idempotency-Key` header required, and the seven error responses bound to their message IDs.
2. Fix the single-and-selection shape: one request per case and a set-level answer assembled by the caller, with the per-case result array, its order and its summary rule (GAP-0710; ASM-1257).
3. Fix the reason element: `transferReasonCode` is a reference to LOV-TRANSFER-REASON, read at run time with `GET /api/recovery/case/v1/admin/lists/{listCode}` from the reference-data contract, with the six codes of the intended set as examples only and never as a closed enum in a client.
4. Fix the two pre-check answers: what the operation returns for a target owner at the cap, for every owner of the target queue at the cap, and for a case under a legal hold before any write (GAP-0711; ASM-1258).
5. Fix the idempotency rule: the header is a uuid, kept 24 hours, a repeat returns the stored response and creates no second assignment, no second decision record and no second event.
6. Fix the rights and the refusal: Queue and allocation U, scope applied, 403 with MSG-P4-002 before the handler runs; no delegation of authority level applies to a transfer.
7. Fix the decision-record evidence: which elements of the record a move must carry, the hash link, the topic and the moment of the write in the transaction.
8. Write the AsyncAPI 3.0 document for `rwb.case.CaseTransferred.v1`: envelope, key, payload and the four fields of the Kafka Catalog v1 event.
9. Publish the one-hop budget of each consumed call and the activity contract of the manual path, with `NoPackageInForce` non-retryable (GAP-0713; ASM-1260).
10. Write the nine contract tables of section 12 and the five fakes.
11. Run the thirteen test cases of section 16 against the fakes and publish the document in the service contract catalogue.

### 5. Exception paths

| ID | Situation | What the contract does | Covered by |
|---|---|---|---|
| C1 | A caller sends a field the `TransferRequest` does not declare | The schema sets `additionalProperties: false` and the request is refused with the 422 example | AC2 |
| C2 | A caller omits `Idempotency-Key` | The header is declared required and the document names the refusal and its message ID | AC1 |
| C3 | A caller sends a reason code that is not in the list | The document states that the code is checked against the reference-data list at run time and that the refusal is MSG-P3-001; no code is enumerated in the schema | AC3 |
| C4 | A caller sends a selection of more than the agreed limit of 50 cases | The per-case operation declares nothing set-level; the limit is a property of the calling screen and of the composite route, and the document says so | AC1 |
| C5 | A case in a selection is refused | The document fixes the per-case result element that carries the message ID, so the caller can render one row per case and a summary | AC1 |
| C6 | A consumer reads the event without the CloudEvents envelope | The AsyncAPI document marks the envelope required and the schema refuses a bare payload | AC8 |
| C7 | A producer adds a field to the event | Allowed as an additive change inside `v1`; the consumer schema keeps `additionalProperties: true` and ignores an unknown field | AC8 |
| C8 | A breaking change is needed | A new path version is published; `v1` stays served until its announced retirement date | Not specified in the source documents (DOR-RWB-P3-E2012-CON-3) |
| C9 | A fake drifts from the document | The contract test fails the pipeline and the document is not published | AC12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1; no build dependency, no service code, no cluster |
| Negotiable | The field names follow the legacy request and response; the descriptions, the examples and the selection envelope are reviewable |
| Valuable | Unblocks the app and deployment stories of the key, the composite route and the tests, on one shape |
| Estimable | Two documents, nine tables, five fakes and twelve contract tests |
| Small | One sprint-week for one pair |
| Testable | Every criterion is tested against an artefact — the document, a schema, a table, a fake — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Manual transfer and reassignment contract baseline for rwb-case

  Background:
    Given the contract baseline of rwb-case version 1 is published
    Given the service facts: base /api/recovery/case/v1, topic rwb.case.events.v1, queue rwb-case, schema rwb_case
    Given the transfer operation and its request and response are those of RWB-P3-E1021-CON

  Scenario: AC1 The manual transfer operation is declared for one case and for a selection (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case version 1
    When the path /cases/{caseId}/transfer is read
    Then it declares POST with TransferRequest in and 200 Assignment out
    Then it declares the Idempotency-Key header as required and the Authorization bearer scheme
    Then it states that a selection of cases is sent as one request per case and never as one set-level request
    Then it declares the selection element TransferSelection with results[], each carrying caseId, the assignment or the messageId of its refusal, and the counts done and total
    Then it states that the selection limit of 50 is a property of the calling screen and not of the contract
    Then the selection element is an ordered array in the caller's order, every result carries caseId and either the assignment or the messageId, and the summary is derived from the array and never from a second call

  Scenario: AC2 TransferRequest and Assignment carry the legacy fields only (new, D-RCV-60)
    Given the components of the document
    When TransferRequest is read
    Then it carries toQueueId or toOwnerId, one of which is required, reasonCode as TRANSFER for a queue move or MANUAL for a reassignment, transferReasonCode as required, and note with a maximum of 500 characters
    Then it carries no other field and additionalProperties is false
    When Assignment is read
    Then it carries id, caseId, assigneeUserId, assignedAt, reason, ruleId, transferReasonCode and queueId
    Then the move that is refused carries no Assignment and its message ID only

  Scenario: AC3 The reason code is a run-time read of the reference data, not a frozen enum (new, D-RCV-60)
    Given the named schema TransferReason
    When a form load reads the list
    Then the list is read through the reference-list operation GET /api/recovery/case/v1/admin/lists/{listCode} of the reference-data contract of rwb-case with the version in force
    Then the six codes of the intended set are R01, R02, R03, R04, R05 and R06 and the document carries them as examples only
    Then a code that is not in the list in force is refused with 422 and MSG-P3-001 and nothing changes
    Then the document states that the party which adds or retires a code is Not specified in the source documents (GAP-0712; ASM-1259)

  Scenario: AC4 The Idempotency-Key rule and the stored response (new, D-RCV-60)
    Given a request with Idempotency-Key "5b0c7a1e-0000-4000-8000-000000000001"
    When the same request is sent again with the same key
    Then the first response is returned unchanged
    Then the store keeps the key, the endpoint, the request hash and the response for 24 hours
    Then there is one assignment, one decision record entry and one CaseTransferred event
    Then a key reused with a different request hash is refused with 409 and MSG-GEN-004

  Scenario: AC5 The rights and the 403 answer (new, D-RCV-60)
    Given the operation declares Queue and allocation U with the scope applied
    When a caller without that right calls it
    Then the rwb-access authorise answer is consulted before the handler runs and the answer is 403 with MSG-P4-002
    Then nothing changes and no decision record entry is written
    Then RW-TEAMMGR and RW-CAPACITY are named as the roles that hold Queue and allocation U
    Then the document states that no delegation of authority level applies to a transfer, because it moves work and not money

  Scenario: AC6 The at-cap and legal-hold refusals are declared (new, D-RCV-60)
    Given the error table of the operation
    When the refusals are read
    Then a target owner at the cap answers 422 with MSG-P3-002 naming the owner and changes nothing
    Then every owner of the target queue at the cap answers 422 with MSG-P3-002 naming every owner and changes nothing
    Then a case under a legal hold or closed answers 409 with MSG-P3-005 naming the target state and HELD_LEGAL and changes nothing
    Then the refusal element carries a reason code, the owner list with an open-case count and a cap for each owner, and the current and target state, and the cap and the hold are read inside the operation before the first write so a refusal never leaves a partial change

  Scenario: AC7 The decision-record evidence of a move is fixed (new, D-RCV-60)
    Given a successful move
    When its decision record entry is read
    Then it carries the case ID, the decision code read at run time from LOV-DECISION as reference data, the rule ID, the rule version "TRF-2026.12", the from and to queue and owner, the reason code, the actor, the decided time, the chain sequence and the hash link
    Then it is written in the same transaction as the assignment swap and the case update
    Then it is published as rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 and the central ledger in rwb-decision collects it
    Then the reference DecisionRecordRef carries the record ID and the hash link and never the inputs

  Scenario: AC8 CaseTransferred is one event with five payload fields (new, D-RCV-60)
    Given the AsyncAPI 3.0 document of rwb.case.events.v1
    When the message rwb.case.CaseTransferred.v1 is read
    Then the envelope is CloudEvents 1.0 with the key caseId, the source rwb-case and the type of the event name
    Then the payload carries caseId, fromOwner, toOwner, reasonCode and ruleId and nothing else
    Then no payload carries a party name, a national identifier, a contact detail or a note
    Then the event is written to the outbox in the transaction that changes the case

  Scenario: AC9 Every consumed call is one hop with a 2 s budget (new, D-RCV-60)
    Given the consumed contracts of section 12.2
    When each call is read
    Then the authorise check, the deviation read of GET /api/recovery/deviation/v1/cases/{caseId}/deviations and the rule-model fetch are each one hop with a 2 s client budget and a breaker
    Then rwb-case calls no service that calls another inside the move
    Then the reference-data read is the service's own contract and is not a hop
    Then the activity timeouts of the manual path are marked Not specified in the source documents (GAP-0713; ASM-1260) and are carried by the deployment story

  Scenario: AC10 Every refusal carries its message ID and its status (new, D-RCV-60)
    Given the error table of the operation
    When each refusal is read
    Then 401 carries MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003, 409 MSG-P3-005, MSG-P3-033 and MSG-GEN-004, 422 MSG-P3-001, MSG-P3-002 and MSG-P3-027, and 503 MSG-P7-003
    Then MSG-P3-033 carries the rule ID of RuleResult and MSG-P3-027 names the package code TRANSFER and the business date only
    Then MSG-P3-035 is the summary of a selection with refusals and carries the done and total counts
    Then every response is an RFC 9457 problem response with type, title, status, detail, instance, messageId and traceId

  Scenario: AC11 The nine contract tables are complete (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.6 states None with a sentence and 12.4 states None with a sentence
    Then 12.1 declares only operations the Ownership Map gives P3 and 12.2 declares only operations of another owner or of the service's own reference-data contract
    Then 12.7 names only rwb_case tables and the platform library objects

  Scenario: AC12 The five fakes answer every element and fail on drift (new, D-RCV-60)
    Given the published fakes
    When each consumed path and each evaluated rule is called
    Then rwb-access answers a granted right, a refusal and no delegation of authority level
    Then rwb-deviation answers an open deviation, an empty list and a delayed answer beyond 2 s
    Then rwb-decision answers the TRANSFER model with its checksum, a wrong checksum and a version that is not in force
    Then the Drools stub answers the refusing row "TRF-010", the allowing rule and NoPackageInForce
    Then the reference-data stub answers LOV-TRANSFER-REASON with R01 to R06 and its version in force
    Then a drift between any fake and this document fails the contract test

  Scenario: AC13 Every business rule of section 8 has a criterion or a guardrail test (new, D-RCV-60)
    Given the business rules table of section 8
    When BR1 to BR12 are read
    Then each of BR1 to BR12 is covered by at least one criterion of this section, or by the guardrail test named in section 16 when it is an architecture constraint
    Then the proposed test for each rule is Not specified in the source documents (NEWAC-RWB-P3-E2012-CON-AC13)
```

These twelve criteria are new for the contract artefact and test no business outcome: they test that the document, the schemas, the nine tables and the four fakes agree with each other and with RWB-P3-E1021-CON. Where a source fixes no value, the criterion names the placeholder and the assumption instead of choosing one silently.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The manual transfer keeps its endpoint, request, response, errors and authorisation; this contract copies them and adds no field to the request or the response | REQ-CWC-010; RWB-P3-E1021-CON BR1 | AC2 |
| BR2 | The reason code is a run-time read of LOV-TRANSFER-REASON with its version in force, and never a closed enum in a client | DP-07; REQ-WKM-003 | AC3 |
| BR3 | The selection is one request per case; the contract fixes the per-case result element and the summary rule, and never a set-level write | REQ-WKM-003; the legacy bulk runner | AC1 |
| BR4 | A repeat with the same Idempotency-Key returns the first response and creates no second assignment, record or event | R-UNI-40; Architecture v5 slide 11 | AC4 |
| BR5 | A caller without Queue and allocation U is refused with 403 and MSG-P4-002 before the handler runs | DP-08; the rwb-access contract | AC5 |
| BR6 | A move of a case under a legal hold or closed is refused, and a move to an owner at the cap is refused, each with its own message ID and status | R-UNI-20; DL23 | AC6 |
| BR7 | Every move writes one decision record entry with the rule ID, the package version, the from and to queue and owner and the reason code, in the same transaction as the change | R-UNI-39; DP-03; ADR-022 | AC7 |
| BR8 | CaseTransferred carries caseId, fromOwner, toOwner, reasonCode and ruleId and no personal data; the note of the request never reaches the event | EV-04; DP-09 | AC8 |
| BR9 | Each consumed call is one hop with a 2 s budget and a breaker; the reference-data read is the service's own contract | DP-11; ADR-020 | AC9 |
| BR10 | One REST base and one topic per service: this document declares `/api/recovery/case/v1` and `rwb.case.events.v1` and never another service's base as provided | DP-13; DP-14 | AC1 |
| BR11 | The document names no table of another service and no rule table; the rule answer is a `RuleResult` | DP-01; DP-04 | AC11 |
| BR12 | No business value is frozen in the document: the reason codes, the caps, the rule IDs and the package version are data of the reference tables and of the evaluated package | Template and Rules §R7.2 s17 | AC3 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the selection element, the reason reference, the two pre-check answers, the record evidence and the event are described | In review |
| In review | Consumer sign-off | The app, deployment and test stories of the key accept the document and the fakes | Baselined |
| Baselined | Additive change | A field, an example or a table row is added without removing one | Baselined |
| Baselined | Breaking change to the operation or the event | RWB-P3-E1021-CON removes, renames or retypes an element this document consumes | In review, with the owner of the baseline |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A new package version is in force | rwb-decision announces it and the rule version a record carries changes | Baselined (new version named in the examples) |

The document has no case state; the case states it describes are those of RWB-P3-E2012-APP section 9, and a manual move changes the queue, the owner and the team and never the status.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the document, the schemas, the nine tables and the fakes; tags the baseline |
| Solution architect | Approves the selection element, the pre-check answer shape and any change to the error binding |
| The owner of RWB-P3-E1021-CON | Signs off the elements taken from the transfer baseline |
| The owner of RWB-P4-E1037-CON | Signs off the authorise answer and the Queue and allocation U letter this document consumes |
| The owner of the S8 contract | Signs off the deviation read whose answer decides the refusal of a move |
| The rwb-case app, deployment and test stories | Review and accept the parts they consume |
| Data steward | Confirms that no personal data field is declared in the event, the request or the record reference |

The reference-list read is the reference-data contract of rwb-case, owned by P3 (Ownership Map api row, ASM-0041), and it is named in 12.2 as an own-contract read. The authority over the list rows is the centre of excellence's, and who may add or retire a code is Not specified in the source documents (GAP-0712; ASM-1259); this document therefore names the centre of excellence as the owner of the values and leaves the change rule to that question.

### 11. Data

The contract declares shapes, not business values.

| Schema or element | Fields | Owning table in rwb_case | BR Field ID |
|---|---|---|---|
| `TransferRequest` | toQueueId, toOwnerId, reasonCode, transferReasonCode, note | none; accepted as input | BR1 |
| `Assignment` | id, caseId, assigneeUserId, assignedAt, reason, ruleId, transferReasonCode, queueId | `assignment`; `queue` for the queue reference | BR1 |
| `TransferSelection` | results[], each with caseId, the assignment or the messageId, and the counts done and total | none; ordered array in the caller's order, the summary derived from it (GAP-0710) | BR3 |
| `TransferReason` | code, label, version in force | `reference_row`, `reference_version` through the reference-list operation of the reference-data contract | BR2 |
| `RuleResult` | packageCode, packageVersion, ruleId, outputs | none; the answer of the embedded Drools kit | BR11 |
| `DecisionRecordRef` | decisionRecordId, entryHash, chainSeq | the decision-record library table | BR7 |
| `CaseTransferred` payload | caseId, fromOwner, toOwner, reasonCode, ruleId | `recovery_case`, `assignment` | BR8 |
| Deviation answer (consumed) | deviationCode, raisedAt, handlerUserId, pausedState | none; owned by S8 | BR9 |
| Cap answer (consumed) | ownerUserId, openCases, capacityCap | `assignment`, `queue`, `queue_member` | BR6 |

The pre-check answer for the cap and the hold is the refusal element of the error table: a reason code, the owner list with an open-case count and a cap for each owner, and the current and target state; the cap and the hold are read inside the operation before the first write. The activity timeouts are Not specified in the source documents (GAP-0713; ASM-1260) and are fixed by RWB-P3-E2012-OPS. The `note` field is declared as an input that is stored nowhere in this contract and never reaches the event.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3). Only operations the Ownership Map gives P3 are declared, and this story fixes the manual element of the first one alone.

| Method | Path | Purpose | Fixed in this story | Access |
|---|---|---|---|---|
| POST | `/cases/{caseId}/transfer` | Transfer or reassign one case with a reason code; `Idempotency-Key` required | The manual path, the selection element, the reason reference, the two pre-check refusals, the record evidence, the event and the error binding | Queue and allocation U, scope applied |
| GET | `/cases/{caseId}` | Read the case after the move | Nothing; the operation is RWB-P3-E1023-CON's | Case record R, scope applied |
| GET | `/queues` | The target queue list of the form | Nothing; the operation is RWB-P3-E2011-CON's | Queue and allocation R, scope applied |
| GET | `/queues/{queueId}/cases` | The cases of a queue, the source of a selection | Nothing; the operation is RWB-P3-E2011-CON's | Queue and allocation R, scope applied |

`POST /queues/{queueId}/placements` is owned by P3 and is not part of this contract: it places a case on a queue from a model or an agent, and it belongs to RWB-P3-E2036-CON.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and Queue and allocation U check, cached per request; faked with a granted right, a refusal and the statement that no delegation of authority level applies |
| GET | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The open deviations that decide a refusal under R-DEV-02; faked with an open deviation, an empty answer and a delayed answer |
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{version}` | P7 rwb-decision | The TRANSFER model the embedded Drools kit fetches and verifies by checksum; faked with a correct checksum, a wrong one and a version that is not in force |
| GET | `/api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=` | P7 rwb-decision | The action text and the owner role of a rule ID the screen may show; faked for R-UNI-18 and for the refusing row |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, own contract (RWB-P3-E1043-CON, DP-07; Ownership Map api row, ASM-0041) | LOV-TRANSFER-REASON with its version in force, as the form and the refusal both read it |

Each consumed call of another owner is one hop with a 2 s client budget and a breaker (DP-11, ADR-020). The reference-data read is the service's own contract and is not a hop.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.case.CaseTransferred.v1` (EV-04) | `rwb.case.events.v1` | P3 | caseId | caseId, fromOwner, reasonCode, toOwner |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained decision record |

Both rows are written to the outbox in the transaction that changes the case; the relay publishes them. CloudEvents 1.0 envelope, `additionalProperties: true` on the consumer schema for an additive change inside `v1`, and no personal data in either payload.

#### 12.4 Events consumed

None. The manual path is started by the REST call and subscribes to nothing. The seven trigger events of the rule-driven transfer are the case router's and are declared in RWB-P3-E1021-CON; this contract declares no subscription and no consumer group.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `CaseWorkflow` | Workflow, one execution per manual request; the workflow ID carries the case ID and the idempotency key | `rwb-case` | Input: case ID, target queue or owner, reasonCode, transferReasonCode, note, caller, idempotency key, business date. Output: the `Assignment` view or the refusal element |
| `EvaluateRules` | Activity, from the workflow kit | `rwb-case` | Input: package code TRANSFER, the facts, the business date. Output: `RuleResult(packageCode, packageVersion, ruleId, outputs)`; raises `NoPackageInForce`, which is non-retryable |
| `RecordAndApply` | Activity, from the workflow kit | `rwb-case` | Input: the decision record, the state change and the outbox rows; one transaction, and no partial write |

The retry policy of the two activities is 1 s initial interval, back-off 2 and 10 attempts, with `NoPackageInForce` non-retryable, as the Temporal and Drools design fixes. Their start-to-close and schedule-to-close values are Not specified in the source documents (GAP-0713; ASM-1260) and are deployment values of RWB-P3-E2012-OPS.

#### 12.6 Schedules

None. A manual move is started by a person and not by a clock, and this contract registers no Schedule, no cron entry and no task queue of its own; the queue `rwb-case` and the 06:30 rebalancing Schedule belong to the case service and are not changed here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `recovery_case` | P3 (rwb_case) | Queue, team, owner, status, legal hold, deviation flag, rule version and the version column that is the optimistic lock |
| `assignment` | P3 (rwb_case) | The open row that ends and the new row with reason, reason code, queue and rule ID |
| `queue` | P3 (rwb_case) | The target queue, its team, its assignment method and its capacity cap |
| `queue_member` | P3 (rwb_case) | The member capacity used by the cap pre-check |
| decision-record library table, `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in rwb_case | The record reference, the outbox rows, the inbox and the stored response of the idempotency key |

`deviation` is owned by S8 and `decision_log_entry` by P7; neither is named as a source, and `rwb_case` holds no foreign key into another schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-access WireMock | Granted Queue and allocation U, a refusal with MSG-P4-002, a scope refusal over another team, and the no-delegation answer | App story, contract tests |
| rwb-deviation WireMock | One open deviation, an empty list and a delayed answer beyond 2 s | App story, contract tests |
| rwb-decision WireMock | The TRANSFER model "TRF-2026.12" with its checksum, one wrong checksum, a 404, and the catalog answer for R-UNI-18 | App story, contract tests |
| Drools stub | Package TRANSFER "TRF-2026.12" with the refusing row "TRF-010", the allowing rule and `NoPackageInForce` for 2026-12-20 | App story, contract tests |
| rwb-case reference-data stub | LOV-TRANSFER-REASON with R01 to R06 and its version in force | App story, contract tests |

A drift between any fake and this document fails the contract test, and the fakes are the same five artefacts the deployment story runs in SIT.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 4 consumed plus 1 own-contract read | The transfer and the three reads provided; authorise, deviations, the rule model and the catalog consumed at one hop and 2 s each; the reference-list read of the same service |
| Kafka | 2 published, none consumed | `rwb.case.CaseTransferred.v1` and the decision record on their topics, through the outbox |
| Temporal | 1 workflow, 2 activities | `ManualTransferWorkflow` with `EvaluateRules` and `RecordAndApply`; no Schedule |
| File | None | No file is read or written |

### 13. Solution plan

**Deliverables.** `contracts/rwb-case/openapi-manual-transfer-v1.yaml` (the operation, the selection element, the request and response, the reason reference and the error table), `contracts/rwb-case/asyncapi-case-transferred-v1.yaml` (the event), `contracts/rwb-case/manual-transfer-record.md` (the record evidence), five WireMock mapping sets and the contract test suite.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

As a contract story this one has no build dependency (§R5.7 rule 1). The pattern rows above are the patterns the capability applies; the dependencies they add are carried by RWB-P3-E2012-APP and by the platform contract stories themselves.

**Build steps**

1. Extract the manual element of the transfer operation from RWB-P3-E1021-CON and add the selection element, the per-case result and the summary rule; carry GAP-0710 in the description of the element.
2. Add the `TransferReason` reference and the run-time read statement of `GET /admin/lists/{listCode}` (RWB-P3-E1043-CON, ASM-0041), and carry GAP-0712 for the authority question that stays open.
3. Add the two pre-check refusals and their elements; carry GAP-0711.
4. Add the error table with the eight message IDs and their statuses, and the RFC 9457 problem schema with `traceId`.
5. Write the record evidence document: the elements a move must carry, the transaction rule and the topic.
6. Write the AsyncAPI document with the CloudEvents envelope, the key and the five payload fields.
7. Write the activity contract of `ManualTransferWorkflow`, `EvaluateRules` and `RecordAndApply`, with the retry policy and `NoPackageInForce` non-retryable; carry GAP-0713 for the timeouts.
8. Build the four fakes and their fixtures.
9. Add the twelve contract tests, including the drift test between each fake and the document.
10. Tag the baseline and collect the sign-off of the app, deployment and test stories.

**Done when.** Both documents validate, the nine sub-tables are complete, the five fakes answer every consumed path and evaluated rule, the twelve contract tests pass, and the app and deployment stories of the key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | No reason code, or a code not in the list in force | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner, or every owner of the target queue, at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Case closed or under a legal hold | This case cannot move to {state} from {current}. |
| MSG-P3-027 | No TRANSFER package version in force | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P3-033 | A TRANSFER rule refuses the move | Rule {rule} does not allow this transfer. |
| MSG-P3-035 | A selection with refusals | {done} of {total} cases were moved. The others show the reason on their row. |
| MSG-GEN-004 | Two moves of one case at once, or a reused key with another request hash | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-001 | No session, or no Recovery Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without Queue and allocation U | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is unknown or outside the caller's scope | This case is not in your scope. |

The texts are the agreed texts of the legacy story and of the platform catalogue; this contract adds no message and rewords none. The status binding is: MSG-P4-001 to 401, MSG-P4-002 to 403, MSG-P4-003 to 404, MSG-P3-005, MSG-P3-033 and MSG-GEN-004 to 409, MSG-P3-001, MSG-P3-002 and MSG-P3-027 to 422, and MSG-P7-003 to 503. MSG-P3-035 is the summary element of a selection and is not a status of its own.

Screen SCR-05 states: no access shows MSG-P4-002 (403) or MSG-P4-001 (401); an unknown or out-of-scope case shows MSG-P4-003 (404); a failed decision record shows MSG-P7-003 (503); a refused move shows the message of its refusal row. Empty and loading states: Not specified in the source documents (DOR-RWB-P3-E2012-CON-10).

### 15. Screens and states

No screen. The document is the input to the gateway-bff composite route (DP-19) that serves SCR-05, to the screen built in RWB-P3-E2012-APP and to the fakes the tests use. It states, for the screen's benefit, the four states its answers produce: the Form answer, the At cap refusal with its owner list, the Refused answer with its message ID and rule ID, and the Saved answer with its assignment, plus the per-case result and the summary of a selection. Screen states for SCR-05 (empty, loading, error and no access) are Not specified in the source documents (CG-ALL-4145).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2012-CON-01 | AC1 | Contract | OpenAPI 3.1 validation; the operation, the selection element and the header |
| TC-P3-E2012-CON-02 | AC2 | Contract | `TransferRequest` and `Assignment` field for field against the legacy request and response; an unknown field refused |
| TC-P3-E2012-CON-03 | AC3 | Contract | The reason reference, the six example codes and the run-time read statement; a code outside the list refused; owner of list changes and approval Not specified in the source documents (GAP-0712) |
| TC-P3-E2012-CON-04 | AC4 | Component | The same key twice returns the first answer; a reused key with another hash is refused; one record and one event |
| TC-P3-E2012-CON-05 | AC5 | Contract | The Queue and allocation U statement, the 403 example and the no-delegation statement |
| TC-P3-E2012-CON-06 | AC6 | Component | An owner at the cap, every owner at the cap and a case under a legal hold, each with its status and message ID |
| TC-P3-E2012-CON-07 | AC7 | Contract | The record evidence document against the decision-record elements; the hash link and the transaction rule |
| TC-P3-E2012-CON-08 | AC8 | Contract | AsyncAPI validation; the envelope, the key, the four payload fields and a payload scan for personal data |
| TC-P3-E2012-CON-09 | AC9 | NFR | Each consumed call declared one hop with a 2 s budget; no chain; the timeout placeholder carried; activity timeouts and alert thresholds Not specified in the source documents (GAP-0713) |
| TC-P3-E2012-CON-10 | AC10 | Contract | Every refusal example carries its message ID and its status; the problem schema on all of them |
| TC-P3-E2012-CON-11 | AC11 | Component | The nine sub-tables present, each owner matched against the Ownership Map; 12.4 and 12.6 None with a sentence |
| TC-P3-E2012-CON-12 | AC12 | Component | The four fakes answer every consumed path and evaluated rule; a drift fails the test |
| TC-P3-E2012-CON-13 | AC11 | Component | Boundary of the section 12.7 tables: each owner matched and no table or foreign key outside the owned set (ASM-3438) |

### 17. Guardrails

- No business value frozen in the document: the reason codes, the caps, the rule IDs and the package version are data of the reference tables and of the evaluated package.
- No personal data in any example, event payload or response: case IDs, staff user IDs, codes and dates only, and the note of the request never reaches the event or a fixture.
- The document names only rwb_case tables and only P3 operations as provided; every other operation is consumed and attributed to its owner (DP-01, DP-13).
- One REST base and one topic per service; a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1`, fails the review (DP-13, DP-14).
- The manual transfer keeps its request, response, errors and authorisation; this contract records them and never changes them.
- The document is versioned and never edited in place: a breaking change is a new path version.
- Every fake is generated from the document, so a drift between document and fake fails the pipeline.
- The envelopes, the naming rule, the Drools kit elements and the record library come from the platform; this story narrows them and never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-WKM-003 | A case is transferred or reassigned manually only with a reason code from the agreed list | The `TransferReason` reference, the run-time read statement and the MSG-P3-001 refusal | TC-P3-E2012-CON-02, TC-P3-E2012-CON-03 |
| REQ-WKM-007 | An absent or over-cap owner's cases reallocated inside the team, keeping the state and the clocks | The MSG-P3-002 refusal for one owner and for every owner, and the R-UNI-18 answer | TC-P3-E2012-CON-06 |
| REQ-WKM-008 | Queue and transfer history visible on the case | The `Assignment` element and the event payload that carry the from and to queue and owner | TC-P3-E2012-CON-02, TC-P3-E2012-CON-08 |
| REQ-CWC-010 | Manual request with a reason code, beside the rule-driven triggers | The operation, its request and its response, taken unchanged from the baseline | TC-P3-E2012-CON-01, TC-P3-E2012-CON-02 |
| REQ-CWC-016 | Every transfer logged with the rule ID and the rule version that caused it | The record evidence, the `RuleResult` element and the decision-record topic | TC-P3-E2012-CON-07 |
| ADR-017 | Embedded Drools per service; the registry in rwb-decision | The `RuleResult` element, the `EvaluateRules` contract and the model fake | TC-P3-E2012-CON-07, TC-P3-E2012-CON-12 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed table with its budgets and the one-hop statement | TC-P3-E2012-CON-09 |
| ADR-022 | Local decision record plus central ledger | The record evidence and the `rwb.decision-record.v1` publication | TC-P3-E2012-CON-07 |

### 19. Out of scope

- The manual path, the pre-checks, the cap check and the screen (RWB-P3-E2012-APP).
- The Helm values, the consumer groups, the activity timeouts, the dashboards, the alerts and the runbook (RWB-P3-E2012-OPS).
- The transfer baseline itself — the request, the response, the task operations, the legal-hold operation and the versioning rule (RWB-P3-E1021-CON).
- The queue view contract and the selection that opens SCR-05 (RWB-P3-E2011-CON).
- The queue history contract on the case (RWB-P3-E2016-CON).
- The rule package authoring, approval and promotion (RWB-P3-E1073-APP).
- The authorise contract and the permission matrix as data (RWB-P4-E1037-CON).
- The deviation read contract of S8 and its own error shape.
- The cross-service journey harness and its evidence (RWB-ITG-E2012-ITG).
- The field-level detail left open by the three gaps of this story (GAP-0710 to GAP-0713).
