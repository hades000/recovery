# RWB-P2-E2036-CON Queue write interface for models and agents

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- The decision event type reads `rwb.decision.DecisionRecorded.v1`; the topic `rwb.decision-record.v1` is unchanged (RD-P1-008).

| Item | Value |
|---|---|
| Story key | RWB-P2-E2036-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-036 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020, REQ-ACA-010) |
| Readiness decisions | RD-P1-008 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-036 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 18 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **tech lead**, I want **the published contract of the rwb-integration queue-write adapter: the placement operation on the integration base with its request and response shape, its error mapping and its idempotent replay, the three contracts it consumes and never restates, the admission decision record of the local decision-record library, the two library tables it owns and the contract fakes for rwb-case and rwb-access**, so that **the app, operations and integration-harness stories of this legacy key build on Day 1 against one agreed, testable shape, without waiting for rwb-case or rwb-access to be built and without a second owner for the placement operation**.

### 2. Business rationale

Contract-first REST, one hop and a 2 s timeout is the decoupling rule (DP-11, ADR-020), and one REST base and one topic per service is the naming rule (DP-13, DP-14; Arch v5 slide 41). A non-engine caller that reaches into the case service directly would break both: it would need the case base, the case schema's semantics and the case team's release cycle, and the case team would inherit a caller it never agreed to serve. The adapter is the seam that keeps the caller on a base of its own while the case owner keeps the business rules.

The seam is load-bearing in three places and this document fixes all three. First, the **operation identity**: the Ownership Map keeps `POST /queues/{queueId}/placements` with P3 rwb-case, and the realignment also gives this legacy key a P2 story, so the contract must say which path is whose. The answer is that the case base keeps the placement and owns its behaviour, and the integration base serves a distinct admission and forwarding operation at the same suffix; the conflict and its reconciliation are recorded as GAP-0671. Second, the **admission rules** the adapter applies before it forwards anything: the feature flag, the Queue and allocation C right, the four field checks and the approved callers list, each with the message the legacy story already fixes. Third, the **replay**: an `Idempotency-Key` on every POST is the platform rule (Arch v5 slide 11), and an adapter that forwards a placement must be able to answer a retry without producing a second placement, a second admission record or a second decision entry.

If the shape is agreed and faked on Day 1, three teams move at once. The app story builds the admission, the record and the forward against the rwb-case and rwb-access fakes; the operations story wires the flag, the alerts and the runbook against the same contract; the wave 2 integration harness drives the journey through the owning services with the fake pack from the same documents. Without it, every caller invents its own body, the placement is owned twice, and the replay window and the admission record become a local choice per environment.

The contract also states what rwb-integration does not own: the queue, the allocation method, the cap, the overflow queue, the assignment, the placement decision entry and the CaseAllocated and CaseTransferred events are rwb-case's (Arch v5 slide 41; ownership map), and the role, scope and right answer is rwb-access's (Arch v5 slide 14). This story therefore defines the provided operation and the consumed side, and never restates another service's operation as its own (DP-01, DP-13).

### 3. Preconditions

- The service naming rule and the platform envelopes are in force: schema `rwb_integration`, REST base `/api/recovery/integration/v1`, topic `rwb.integration.events.v1`, task queue `rwb-integration` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.integration`, OpenAPI 3.1, RFC 9457 problem details and the CloudEvents 1.0 envelope (DP-13, DP-14; RWB-PLT-E1047-CON).
- The local decision-record library and the shared topic `rwb.decision-record.v1` are published, so the contract can state who publishes DecisionRecorded (DP-03; RWB-PLT-E1027-CON).
- The idempotency, outbox and inbox library is published, with the stored-response table, its 24-hour retention and the `Idempotency-Key` convention (DP-09; RWB-PLT-TE006-CON).
- The reference-data client library (DP-07; RWB-PLT-E1043-CON) and the rwb-access guard library (DP-08; RWB-PLT-E1037-CON) are published; the contract narrows their use and redefines neither.
- The rwb-case placement contract and the rwb-case reference-data and parameter contract are published by their stories (RWB-P3-E1019-CON, RWB-P3-E1020-CON, RWB-P3-E1043-CON), and the rwb-access authorise contract by RWB-P4-E1037-CON. This document consumes them, fakes them and defines none of them.
- The legacy values the contract reuses are the legacy values: the path suffix `queues/{queueId}/placements`, the four request fields `caseId`, `reason`, `modelOrAgent` and `version`, the configuration key `rwb.casewf.placement.approved-callers`, the caller types MODEL and AGENT and the messages MSG-GEN-001, MSG-GEN-002, MSG-P2-020, MSG-P2-021, MSG-P2-024, MSG-P2-025, MSG-P3-005, MSG-GEN-004, MSG-P4-001, MSG-P4-002, MSG-P4-003 and MSG-P7-003.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7 rule 1), and it sits in contract group CG-W2.

### 4. Flow

1. Draft the provided operation `POST /api/recovery/integration/v1/queues/{queueId}/placements` with the path parameter, the required `Idempotency-Key`, the request body and the access expectation; it forwards to `POST /api/recovery/case/v1/queues/{queueId}/placements`, the case-base operation that the Ownership Map keeps with P3, and returns that operation's status and body unchanged.
2. Fix the request and response shape, with the placement result returned exactly as rwb-case returns it, and mark every element that neither the legacy story nor a technical specification names with the placeholder.
3. Fix the error mapping: which status and which message comes from the adapter's own checks and which is returned unchanged from rwb-case or rwb-access.
4. Fix the idempotent replay: the key, the endpoint, the request hash, the stored status and body, the 24-hour window, the replay answer and the expiry behaviour.
5. Fix the approved callers source: the rwb-case parameter and reference-data row under the legacy key, the row fields, the caller types, the empty list at go-live and the rule that rwb-integration holds no copy.
6. State the admission decision record: the decision code D6, the caller identity and type, the version, the reason, the target queue and the answer, written before the forward and completed with it.
7. Publish the three consumed contracts as consumed, with their owners and the 2 s client budget, and state that none is restated as provided.
8. Publish the nine contract tables of section 12, the two library tables and the P3 and P4 fakes.
9. Add the contract tests: the completeness of 12.1 to 12.9, the request and response shape, the error mapping, the replay, the approved callers source and a drift test between each fake and this document.
10. Tag the baseline and hand it to the app story, the operations story and the wave 2 integration harness of this legacy key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A sub-table of section 12 is missing or names an owner that is not in the Ownership Map | The contract review fails and the baseline is not tagged | None | AC1 |
| X2 | The operation is declared on the case base, or the case placement is declared as provided here | The review fails: the case placement is P3's and is consumed by this service | None | AC1, AC2 |
| X3 | The request or response shape carries an element no source names, and the placeholder is missing | The contract test fails and the merge is blocked | None | AC2 |
| X4 | A status or a message in the error mapping differs from the legacy story or from the owning service's text | The contract test fails on the drift | None | AC3 |
| X5 | A repeat with the same `Idempotency-Key` inside 24 hours produces a second forward or a second admission record | The contract test fails and the merge is blocked | None | AC4 |
| X6 | The approved callers list is copied into `rwb_integration`, or read from anywhere but the rwb-case contract | The review fails; the list has one source and one owner | None | AC5 |
| X7 | A fake drifts from this document, or answers a path this document does not declare | The contract test fails and the merge is blocked | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and the four platform and service contracts as published, and fakes the two consuming ones |
| Negotiable | Field-level detail of the consumed contracts is settled with their owners; the provided operation, the replay and the admission record are fixed by this realignment |
| Valuable | Unblocks the app, operations and integration-harness stories of this legacy key on Day 1 and keeps one owner for the placement |
| Estimable | One provided operation, three consumed contracts, two library tables, nine contract tables and four fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the document, the OpenAPI file, the fake — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Queue write adapter contract baseline for rwb-integration

  Background:
    Given the service naming rule of the platform library is in force
    Given the REST base of rwb-integration is /api/recovery/integration/v1
    Given the local decision-record library publishes on rwb.decision-record.v1

  Scenario: AC1 The nine contract tables are complete and each names its owner (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.1 declares one provided operation on the integration base and no other
    Then 12.2 declares the rwb-case placement contract, the rwb-case reference-data and parameter contract and the rwb-access authorise contract as consumed, each attributed to P3 or P4
    Then 12.3 declares the decision record of the library and no business event of rwb.integration.events.v1
    Then 12.4, 12.5 and 12.6 are None
    Then 12.7 names the idempotency_key and decision_record library tables in rwb_integration and no business table
    Then the Ownership Map keeps POST /queues/{queueId}/placements with P3 rwb-case and this document declares the placement on the case base as consumed

  Scenario: AC2 The placement operation shape is fixed on the integration base (new, D-RCV-60)
    Given the provided operation of 12.1
    When its request and response are read
    Then the method is POST and the path is /queues/{queueId}/placements on /api/recovery/integration/v1
    Then the path carries queueId as a uuid and the body carries caseId, reason, modelOrAgent and version, each required
    Then the request carries an Idempotency-Key, which is required
    Then a 201 returns the placement result exactly as the rwb-case contract returns it, with the owner and the queue or the overflow queue with no owner
    Then every element that no source names carries the placeholder of this document and no invented type or length
    Then the access expectation is Queue and allocation right C, scope All for service identities, answered by the rwb-access contract

  Scenario: AC3 The error mapping is fixed and forwarded refusals are unchanged (new, D-RCV-60)
    Given the error table of 12.1
    When each status is read
    Then 404 with MSG-P2-025 is returned by the flag check before any read or write
    Then 403 with MSG-P4-002 is returned when the identity lacks Queue and allocation C
    Then 422 with MSG-GEN-001 or MSG-GEN-002 is returned for an empty field or a length out of range, and 422 with MSG-P2-020 for a caller that is not approved
    Then 409 with MSG-P2-024, MSG-P3-005, MSG-P2-021 or MSG-GEN-004, 404 with MSG-P4-003, 401 with MSG-P4-001 and 503 with MSG-GEN-006 are returned unchanged from rwb-case or rwb-access
    Then 503 with MSG-P7-003 is returned when the admission record cannot be written, and nothing is forwarded
    Then the adapter adds no message of its own to a forwarded refusal

  Scenario: AC4 The idempotent replay is fixed (new, D-RCV-60)
    Given the replay rule of 12.1 and 12.7
    When a request is admitted and its answer stored
    Then one row exists in idempotency_key for the endpoint and the Idempotency-Key, with the request hash, the stored status and the stored body
    Then a repeat with the same key and the same request hash inside 24 hours returns the stored status and body, with no second admission record and no second forward
    Then a repeat after 24 hours is treated as a new request and rwb-case's own one-open-assignment rule decides the answer
    Then a key reused with a different request hash is refused with 409 and nothing changes
    Then a refusal produced by the adapter's own checks is stored as well, so its retry replays the refusal

  Scenario: AC5 The approved callers list has one source (new, D-RCV-60)
    Given the approved callers rule of this document
    When the source of the list is read
    Then the list is the rwb-case reference-data and parameter row under the key rwb.casewf.placement.approved-callers, read through the rwb-case contract with the version in force
    Then the row carries the caller code, the caller type MODEL or AGENT, the service identity and the approval state
    Then the row field names carry the placeholder of this document and no invented name
    Then rwb-integration holds no copy of the list and no table for it
    Then the list is empty at go-live and an entry is requested by RW-COE and approved by RW-RISK before it is loaded

  Scenario: AC6 The P3 and P4 fakes match this document (new, D-RCV-60)
    Given the fakes of 12.8
    When each fake is compared with the tables of section 12
    Then the rwb-case placement fake answers the 201 with an owner, the 201 with the overflow queue, the four 409s, the 404 and the 503 of this document
    Then the rwb-case reference-data fake answers the approved callers list and the empty list
    Then the rwb-access fake answers the granted and the refused Queue and allocation C
    Then the decision-record stub answers one successful write and one forced failure
    Then a drift between a fake and this document fails the contract test and blocks the merge

  Scenario: AC7 The business rules of section 8 hold in the contract (new, D-RCV-60)
    Given the business rules BR1 to BR10
    When the contract and the adapter behaviour it fixes are checked against them
    Then only the integration base is declared as provided, the case placement stays with P3 rwb-case, and no case, queue or assignment row is written and no CaseAllocated or CaseTransferred is published
    Then every POST carries an Idempotency-Key and the stored answer is replayed for 24 hours against the same endpoint and request hash
    Then the adapter's own checks run in the order flag, right, fields, approved callers list, and a failure writes nothing except the stored refusal
    Then the admission decision record with decision code D6 is written before the forward, and a failure to write it blocks the forward
    Then the rwb-case answer is returned unchanged, with no added message, field or effect
    Then the approved callers list is read only from its rwb-case row, and a model, an agent and a person pass the same Queue and allocation C check
    Then the contract holds no business value as a literal of its own
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: this contract declares `/api/recovery/integration/v1` for the provided operation and consumes the rwb-case and rwb-access bases; it never declares another service's path as provided | DP-13; Arch v5 slide 41 |
| BR2 | The placement on the case base belongs to rwb-case; the Ownership Map keeps `POST /queues/{queueId}/placements` with P3, and the integration operation is a distinct admission and forwarding operation on the integration base | Ownership map (`POST /queues/{queueId}/placements` is P3); GAP-0671 |
| BR3 | Every POST carries an `Idempotency-Key`, and the stored answer is replayed for 24 hours against the same endpoint and request hash | Arch v5 slide 11 (Idempotency-Key on every POST, stored response); DP-09; TSD P2 v3 T3.1 |
| BR4 | The adapter's own checks run in one order: the flag, the right, the fields, the approved callers list; a failure at any step writes nothing except the stored refusal | Legacy RWB-E2-036 flow steps 2 to 4 and DS exception paths X1 to X3 |
| BR5 | The approved callers list has one source and one owner: the rwb-case reference-data and parameter row under the legacy key, read with the version in force; no copy exists in `rwb_integration` | Legacy BR1 and precondition; DP-07; R-PREC default ruling |
| BR6 | The access check is the same for a model, an agent and a person: Queue and allocation right C from the rwb-access authorise contract, with no bypass for a non-engine caller | REQ-ACA-010; CTL-09; NFR-051; DP-08 |
| BR7 | The admission decision record is written through the local decision-record library before the forward, with decision code D6, the caller identity and type, the version, the reason, the target queue and the answer; a failure blocks the forward | Legacy AC3 and BR5; DP-03; R-UNI-39 |
| BR8 | The adapter returns the rwb-case answer unchanged and adds no message, no field and no second effect of its own | Legacy AC1 and section 12; DP-11 |
| BR9 | The adapter writes no case, queue or assignment row and publishes no CaseAllocated or CaseTransferred; the case events belong to rwb-case | Arch v5 slide 41; DP-01 |
| BR10 | No business value in the contract: caller codes, caller types, caps, methods, overflow queues and the decision code are data of their owners, not literals of this document | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The provided operation, the three consumed contracts, the replay and the admission record are described | In review |
| In review | Consumer sign-off | The app, operations and integration-harness stories accept the document and the fakes | Baselined |
| Baselined | Additive change | An optional field, a status or a message is added without removing or retyping one | Baselined |
| Baselined | Breaking change | The path, a required field, the replay window or a consumed contract changes shape | New contract version drafted, with the owner of the affected contract |
| Baselined | Drift in a fake, or a status that differs from the owning service | A contract test fails | In review |
| Baselined | The Ownership Map changes the owner of the placement | The review reopens; this document restates which path is whose | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-integration | Owns the provided operation, the replay rule, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and any change to the operation identity between the two bases |
| The rwb-case owner | Owns the placement, the reference-data and parameter contract and signs off the shapes taken from its documents |
| The rwb-access owner | Owns the authorise contract and signs off the right and scope wording |
| Platform library owner | Owns the OpenAPI conventions, the problem detail envelope, the idempotency library and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in the request, the response, the record or the replay row |
| RW-RISK, risk and model risk officer | Approves a caller entry before it is loaded, and confirms the caller types of the list |

The deployment identity that calls rwb-case and rwb-access is the rwb-integration service identity (DP-02). Its login name is Not specified in the source documents (GAP-0671; ASM-1198).

### 11. Data

The contract declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Placement request | `caseId` (uuid), `reason` (text, 1 to 1,000 characters), `modelOrAgent` (a caller code in the approved list), `version` (1 to 40 characters); `Idempotency-Key` in the header | Not specified in the source documents (DOR-RWB-P2-E2036-CON-7) |
| Placement response, 201 | The placement result as rwb-case returns it: the case, the queue, the owner and the assignment when an owner was chosen, or the overflow queue with no owner; the decision entry reference and the status after the placement | Not specified in the source documents (DOR-RWB-P2-E2036-CON-7) |
| Problem response | RFC 9457 problem details with the status, the message identifier and the field or the caller it names; no personal value | Not specified in the source documents (DOR-RWB-P2-E2036-CON-7) |
| Admission record | Decision code D6, the caller identity and type, the caller code, the model or agent version, the reason, the target queue, the answer and the freshness of the list version used | Not specified in the source documents (DOR-RWB-P2-E2036-CON-7) |
| Replay row | The endpoint, the `Idempotency-Key`, the request hash, the stored status and body, the created time and the expiry at 24 hours | Not specified in the source documents (DOR-RWB-P2-E2036-CON-7) |
| Approved callers row | The caller code, the caller type MODEL or AGENT, the service identity and the approval state, read through the rwb-case contract with the version in force | Not specified in the source documents (DOR-RWB-P2-E2036-CON-7) |

The exact JSON field names of the placement request, the placement response and the three consumed contracts are Not specified in the source documents (GAP-0671; ASM-1199); the row fields of the approved callers list are Not specified in the source documents (GAP-0671; ASM-1200); the column names of the `decision_record` library table beyond the standard columns are Not specified in the source documents (GAP-0671; ASM-1201). This document fixes the element names above and leaves the property types and lengths to the review with the owners of those contracts. The `idempotency_key` column set is the one of TSD P2 v3 T3.1. The 201 overflow answer carries the overflow queue with no assignment; the caller mapping (caller code, caller type and service identity) is held in this contract; the approved callers list is a parameter read from rwb-case; the database login name is held in the rwb-integration DB story, and the legacy acceptance criteria in RWB-ITG-E2036-ITG.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2); OpenAPI 3.1, `placements.yaml`. Contract version: v1 (path version); the operation is not yet in API Specification v5 (CG-ALL-3313).

| Method | Path | Request | Responses | Owner |
|---|---|---|---|---|
| POST | `/queues/{queueId}/placements` | Path `queueId` (uuid); body `caseId` (uuid, required), `reason` (text, required, 1 to 1,000 characters), `modelOrAgent` (required, a caller code in the approved list), `version` (required, 1 to 40 characters); `Idempotency-Key` required | 201 Placement; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P2-025 or MSG-P4-003; 409 MSG-P2-024, MSG-P3-005, MSG-P2-021 or MSG-GEN-004; 422 MSG-GEN-001, MSG-GEN-002 or MSG-P2-020; 503 MSG-P7-003 or MSG-GEN-006 | P2 rwb-integration |

The check order is the contract: the feature flag, the replay lookup, the Queue and allocation C right, the field validation and the approved callers check, then the admission record and the forward. The operation requires the `Idempotency-Key` header on every call, and the replay lookup keys on it. A refusal produced by the adapter is stored against the `Idempotency-Key`, so a retry replays it. The ownership note is part of this table: the same path suffix appears on the case base as `POST /api/recovery/case/v1/queues/{queueId}/placements`, which the Ownership Map keeps with P3 and which this service consumes (12.2); the two are different operations and neither is a wrapper of the other's contract (GAP-0671; ASM-1197). The exact JSON element names of the request and of the returned result are Not specified in the source documents (GAP-0671; ASM-1199).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| POST | `/api/recovery/case/v1/queues/{queueId}/placements` | P3 rwb-case | The placement: the queue, the allocation method, the cap, the overflow queue, the access rule, the assignment, the placement decision entry and the CaseAllocated and CaseTransferred events. Faked with 201 and an owner, 201 with the overflow queue, four 409s, 404 and 503 |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The approved callers list under the key `rwb.casewf.placement.approved-callers`, with the version in force. Faked with the list and with the empty list |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Queue and allocation right C for the caller's service identity, with the matrix version that answered. Faked with a grant and a refusal |

Every operation is one hop with a 2 s client budget and a breaker per downstream (DP-11, ADR-020). None is declared as provided by this service. The rwb-case reference-data and parameter contract that answers the second row is RWB-P3-E1043-CON; the exact JSON field names of the three rows are Not specified in the source documents (GAP-0671; ASM-1199).

#### 12.3 Events published

None of its own. The local decision-record library publishes `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` when the admission record is written, with decision code D6, the caller identity and type, the caller code, the version, the reason, the target queue and the answer; its schema is unchanged by this story and is the one declared in RWB-PLT-E1027-CON (DP-03).

`rwb.integration.events.v1` carries FileDelivered and FileFailed for the outbound files (Arch v5 slides 16 and 43); this slice publishes neither, because a placement is not a file. CaseAllocated and CaseTransferred are rwb-case's on `rwb.case.events.v1` and are never declared here (DP-01, DP-14).

#### 12.4 Events consumed

None. The adapter is called synchronously and subscribes to no topic; it consumes no case event and therefore needs no inbox row for this slice.

#### 12.5 Workflows and activities

None. The adapter is a synchronous admission and forward of one REST request; it declares no workflow, no activity and no signal, and the placement starts no Temporal execution of its own. The `rwb-integration` task queue in namespace `rwb-recovery` belongs to the file and integration work of the other P2 stories.

#### 12.6 Schedules

None. The adapter is caller-driven; no Temporal Schedule, no cron expression and no timer is declared by this contract.

#### 12.7 Tables owned

| Table | Schema | Owner | Contracted use |
|---|---|---|---|
| idempotency_key | rwb_integration | PLT library, created in rwb_integration by the rwb-integration DB story | One stored answer per endpoint and `Idempotency-Key`, with the request hash, the status, the body, the created time and the 24-hour expiry (DP-09) |
| decision_record | rwb_integration | PLT library, created in rwb_integration by the rwb-integration DB story | The admission record of decision code D6, written before the forward and completed with the answer (DP-03) |

`processed_event` is declared in the baseline of every service schema, but this slice does not use it: the adapter consumes no event, so the contract names it only to say that no inbox row is written here. No business table is named: `recovery_case`, `queue` and `assignment` are P3's and are never read directly (DP-01). The column set of `idempotency_key` is the one of TSD P2 v3 T3.1 (id, idempotency_key, endpoint, request_hash, response, with the standard record columns); the further column names of `decision_record` are Not specified in the source documents (GAP-0671; ASM-1201). The 24-hour replay window is the platform rule (DP-09), and the database login name is left to the rwb-integration DB story.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case placement WireMock | 201 with owner "U-5002" in queue "MTG-BKK-PRI"; 201 with queue "MTG-BKK-OVF" and no owner; 409 with MSG-P2-024, MSG-P3-005, MSG-P2-021 and MSG-GEN-004; 404 with MSG-P4-003; 503 with MSG-P7-003 | App story, contract tests, integration harness |
| rwb-case reference-data WireMock | The approved callers list holding MDL-SYN-PRIORITY of type MODEL for SY-AGENT, the list without MDL-SYN-UNLISTED, the empty list at go-live and a stale version answer | App story, contract tests |
| rwb-access WireMock | `POST /authorise` granting Queue and allocation C for SY-AGENT under matrix PM-SIT-02 and refusing it under the production matrix | App story, contract tests |
| Decision-record library stub | One successful admission write and one forced failure that rolls the transaction back | App story, contract test TC-P2-E2036-CON-03, and the resilience case of the APP story (TC-E2-036-14) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | The placement on the integration base provided; the rwb-case placement, the rwb-case reference-data and parameter contract and the rwb-access authorise consumed; one hop, 2 s timeout, breaker per downstream |
| Kafka | None published by this service, 1 published by the decision-record library | `rwb.decision-record.v1` carries DecisionRecorded on the service's behalf (DP-03); `rwb.integration.events.v1` and `rwb.case.events.v1` are not used |
| Temporal | None | No workflow, no activity and no Schedule |
| File | None | The contract declares no file and no claim-check manifest |

### 13. Solution plan

**Deliverables.** `contract/placements.yaml` (the OpenAPI 3.1 document of the provided operation, with the request, the response, the error table and the `Idempotency-Key` header), `contract/placement-consumed.yaml` (the three consumed operations with their owners and the 2 s budget), `contract/placement-idempotency.md` (the key, the request hash, the stored answer and the 24-hour window), `contract/placement-approved-callers.md` (the one source and the row fields of the list), and the four WireMock mappings with their fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The contract story is Day 1 with no build dependency, so these platform contracts are listed as the patterns that shape it, not as build prerequisites (Template and Rules §R5.7 rule 1).

**Build steps**

1. Write `placements.yaml`: the path, the path parameter, the four body fields with their lengths, the required `Idempotency-Key`, the 201 shape and the problem responses.
2. Write the error mapping table and check every status and message against the legacy story and against the owning services' texts.
3. Write the replay contract: the key and endpoint pair, the request hash, the stored status and body, the 24-hour window, the replay answer, the expiry and the key-reuse refusal.
4. Write the approved callers contract: the key, the row fields, the two types, the empty list at go-live and the single-source rule.
5. Write the admission record contract against the decision-record library: decision code D6, the carried fields and the transaction boundary.
6. Write `placement-consumed.yaml` from the rwb-case and rwb-access documents, with the owners and the 2 s budget.
7. Build the four WireMock mappings and their fixtures from the shapes of this document.
8. Add the six contract tests, including the drift test between each fake and this document.
9. Tag the baseline and collect the sign-off of the app, operations and integration-harness stories.

**Done when.** The four contract files and the OpenAPI document validate in the pipeline, the six contract tests pass, the four fakes answer every declared path and status, and the app, operations and integration-harness stories of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-025 | The feature flag is off | Queue placement by models and agents is switched off. |
| MSG-P4-002 | Identity lacks Queue and allocation C | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is empty | Enter {field}. |
| MSG-GEN-002 | reason or version outside its length | {field} must be between {min} and {max}. |
| MSG-P2-020 | The caller is not in the approved callers list | {caller} is not approved to place cases on queues. |
| MSG-P4-001 | No valid session or workload token | Not specified in the source documents (GAP-0671; ASM-1198). |
| MSG-P2-024 | The case is already in the target queue | This case is already in {queue}. |
| MSG-P3-005 | The case is closed | This case cannot move to {state} from {current}. |
| MSG-P2-021 | The case has an open deviation | This case has an open deviation and stays with the deviation handler. |
| MSG-GEN-004 | The case changed during the placement | Someone else changed this record. Reload it to see their change. |
| MSG-P4-003 | Queue or case not found | This case is not in your scope. |
| MSG-P7-003 | Admission record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | A consumed service does not answer inside the 2 s budget | Platform catalogue text, not restated here (DOR-RWB-P2-E2036-CON-9) |

MSG-GEN-006 is the platform message for a consumed service that does not answer inside the 2 s budget; its text is the platform catalogue text and is not restated here. The texts above are the legacy texts of RWB-E2-036, unchanged; this contract adds no message. A status that this service returns unchanged from rwb-case or rwb-access carries that service's text, and the contract test compares it, so the two never drift. The admission refusals map by reason code: RIGHT_NOT_HELD, CALLER_KIND and SCOPE_NOT_ALL answer 403 with MSG-P4-002; the other two reason codes are Not specified in the source documents (GAP-0958), and the adapter maps the code and restates no text.

### 15. Screens and states

None in this story. The caller is a job or an agent, not a person; the placed case appears in its queue on the screens of the case service (SCR-07 Team queues and SCR-02 Case list), and the admission record is read by the platform team on the operation log, not on a business screen. The replay state is a row and a metric of the adapter, with no screen state. SCR-02 Case list states: Not specified in the source documents (CG-ALL-3318). SCR-07 Team queues states: Not specified in the source documents (CG-ALL-3319).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2036-CON-01 | AC1 | Contract | The nine sub-tables complete; 12.4, 12.5 and 12.6 None; 12.7 names only the two library tables; the placement is consumed and not provided |
| TC-P2-E2036-CON-02 | AC2 | Contract | The operation validated against the document: path, path parameter, the four body fields with their lengths, the required Idempotency-Key and the 201 shape |
| TC-P2-E2036-CON-03 | AC3 | Contract | Each status forced once: the flag, the right, the empty field, the length, the unlisted caller, the four case refusals, the unknown queue, the record failure and the downstream timeout |
| TC-P2-E2036-CON-04 | AC4 | Component | One admitted request, its replay inside 24 hours, its expiry, a key reused with a different hash, and a stored refusal replayed |
| TC-P2-E2036-CON-05 | AC5 | Contract | The list read through the rwb-case contract, the empty list, the stale version, and the absence of any list table in rwb_integration |
| TC-P2-E2036-CON-06 | AC6 | Component | The four fakes compared with the document, and one deliberate drift that fails the contract test |
| TC-P2-E2036-CON-07 | AC1 | Contract | Boundary of the section 12.7 tables: only the idempotency_key and decision_record library tables are used; processed_event receives no row; no business table of recovery_case, queue or assignment is read |
| TC-P2-E2036-CON-08 | AC7, BR1, BR2, BR9 | Contract | One REST base per service; the case placement is not provided here; the adapter writes no case, queue or assignment row and publishes no case event |
| TC-P2-E2036-CON-09 | AC7, BR3, BR4, BR7, BR8 | Component | Every POST carries the key; the checks run in order and a failure writes only the stored refusal; the admission record is written before the forward; the rwb-case answer returns unchanged |
| TC-P2-E2036-CON-10 | AC7, BR5, BR6, BR10 | Contract | The approved callers list read from the rwb-case row with no copy in rwb_integration; the access check applies to every caller type; no business value literal in the contract |

### 17. Guardrails

- No business value in the contract: caller codes, caller types, caps, methods, overflow queues and the decision code stay data of their owners.
- No personal data in the request, the response, the admission record, the replay row or a fake: identifiers, a caller code and a reason phrase only.
- The contract names only the integration base as provided and only the rwb-case and rwb-access bases as consumed; a document that names another service's path as provided fails the review (DP-13).
- The placement on the case base stays P3's; this document consumes it and never declares it, and the review fails a contract that inverts the two (BR2).
- No business table is named and no cross-schema reference is declared; the case, queue and assignment facts are read only through their owner's contract (DP-01).
- The envelope, the problem detail format, the naming rule, the idempotency library and the decision-record library come from the platform; this story narrows them but never redefines them.
- Every example and fixture is synthetic; no production caller, case number or payload is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-017 | A queue accepts a write from a model or an agent with the case and the reason | The provided operation and its four required fields; the consumed placement contract | TC-P2-E2036-CON-01, TC-P2-E2036-CON-02 |
| REQ-CWC-018 | A model or agent passes the same permission checks and its write is logged with its version | The authorise row of 12.2; the admission record of 12.3 and 12.7 | TC-P2-E2036-CON-03, TC-P2-E2036-CON-04 |
| REQ-CWC-019 | The interface ships behind a feature flag | The 404 with MSG-P2-025 as the first check of the provided operation | TC-P2-E2036-CON-03 |
| REQ-CWC-020 | Model and rule work in the same queue, in one priority order | The one placement path and the single queue contract it consumes; no second queue order in this service | TC-P2-E2036-CON-02 |
| REQ-ACA-010 | A model or agent identity passes the same role and scope checks as a person | The Queue and allocation C right of 12.1, answered by the rwb-access contract | TC-P2-E2036-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed operations with their owners and the 2 s client budget | TC-P2-E2036-CON-02, TC-P2-E2036-CON-03 |

### 19. Out of scope

- The implementation of the controller, the admission service, the clients, the replay store and the record writer (RWB-P2-E2036-APP).
- The placement itself and the queue, allocation, assignment, decision entry and event behaviour (RWB-P3-E2036-APP), and the queue and allocation engine it reuses (RWB-P3-E1019-APP, RWB-P3-E1020-APP).
- The role, scope and right answer and the matrix versions (RWB-P4-E1037-CON and the rwb-access stories).
- The central decision ledger and the decision log query (RWB-P7-E2036-APP).
- The open deviation that refuses a placement (RWB-S8-E2036-APP).
- The deployment, the flag change, the alerts and the runbook of the adapter (the operations story of this epic).
- The real cross-service proof of the journey through gateway-bff (RWB-ITG-E2036-ITG).
- The field-level completeness of the three consumed contracts (GAP-0671) and of the `decision_record` columns (ASM-1201).
