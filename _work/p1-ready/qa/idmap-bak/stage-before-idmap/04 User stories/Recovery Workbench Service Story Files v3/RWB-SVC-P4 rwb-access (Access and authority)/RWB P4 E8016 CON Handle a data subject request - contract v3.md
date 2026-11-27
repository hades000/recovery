# RWB-P4-E8016-CON Handle a data subject request

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8016-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P4-E8016-CON-14) |
| Size | Sized by the squad at refinement (DOR-RWB-P4-E8016-CON-16) |
| Contract version | 1 (major version in path /api/recovery/access/v1) |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-016 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 10 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the data subject request register of `rwb-access`: an OpenAPI 3.1 document for the open, the decision, the read and the list, the `DataSubjectRequest`, `DataSubjectRequestDecision` and `DataSubjectRequestList` schemas with the state set and the evidence block and no person, one RFC 9457 error envelope with its message IDs, the consumed authorise, access-log and parameters operations with their owners and the 2 s budget, the contract tables of section 12 and the five contract fakes**, so that **the app story, the SCR-47 route, the access-log owner, the parameters owner and the integration harness can build against a fixed, testable contract on Day 1 without waiting for `rwb-access`, `rwb-case` or the access-log capability to be built**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-016 belong to RWB-P4-E8016-APP, and the eight criteria of section 7 test the document, the schemas and the state set, the envelope, the consumed declarations, the fakes, the additive change and the rule coverage.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story worked a data subject request inside a screen of the monolith, where the request, the masking rows and the decision log were rows of one schema and no other service had to agree on what "answered inside the statutory period" meant. In the target the period is a parameter of `rwb-case`, the case and its hold are `rwb-case`'s and `rwb-deviation`'s, the masking policy and the access entries are `rwb-access`'s, and the record of who decided what is the decision record (ADR-022).

Three things must therefore be fixed once. The first is the boundary: which service owns the register (this one), which owns the period (P3 through DP-06) and which owns the access evidence (the access-log capability of this service). The second is the state set: a request moves from open to in progress to answered or refused, and no consumer should have to infer that from dates. The third is what the register says: a person reference, case ids, field ids, a decision code, a role code and times, and never a personal value, because the answer of a request is read by audit and copied into a topic that every consumer of the decision record reads.

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with the parameters contract of `rwb-case`, the local decision-record library and the access-log read, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

The baseline also states the one thing it is not: it defines no retention class, no masking policy, no access entry and no case state, and it names no table of `rwb-case`, `rwb-decision` or `rwb-source-data` as this service's. The consumed operations appear in the document as consumed, which is what makes the split real.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that calls the four operations behind SCR-47 Personal data, and it is a consumer of this baseline.
- The access-log read is described by TSD P4 v3 appendix T-A as API-P4-008 `GET /admin/access-log` with the query `user`, `from`, `to`, `event`, `page` and `size` and the response `AccessLogPage`; the case-id filter this story needs is not in that list, so the filter is fixed here and raised with the access-log owner (GAP-0877; ASM-1592).
- The parameters read is DP-06 and the `rwb-case` parameters contract (RWB-P3-E1042-CON): the statutory period, the person-reference shape and the page bounds are rows and not fields of this document's code.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The register is a set of entries of the DP-03 library (RWB-PLT-E1027-CON); this document describes the fields a step records and no field of another service.
- The operations and their owners are taken from the ownership map only: the four operations of this document are P4's, the authorise operation and the access-log read are P4's, and the parameters read is P3's. No table of another service is named as this service's (DP-01).
- No build dependency: this story is Day 1 by rule (Template and Rules R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the four operations with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the paging parameters and the three schemas.
2. Fix the `DataSubjectRequest` request and answer schemas with the fields of section 11: `dataSubjectRef`, `requestType`, `caseIds`, `fieldIds`, `receivedAt` and `reason` in, and `requestId`, `requestType`, `state`, `openedAt`, `dueDate`, `version`, `steps` and `evidence` out, with no person field of any kind.
3. Fix the `DataSubjectRequestDecision` schema behind the `PATCH`, with `decision`, `fieldIds`, `effectiveFrom`, `refusalReason`, `answerSummary` and `reason` in, `requestId`, `state`, `decision`, `version`, `updatedAt`, `maskingVersion` and `maskingRowCount` out, and the `If-Match` header declared as required.
4. Fix the state set: `OPEN`, `IN_PROGRESS`, `ANSWERED` and `REFUSED`, with the transition each operation may cause, the terminal pair and the overdue flag as a computed answer field and not a state.
5. Fix the evidence block of a read: one item per access entry with its case id, decision code, decided time, field ids and mask flag, and the statement that no actor name and no personal value is part of it.
6. Agree the error envelope and the message-ID mapping for 401, 403, 404, 409, 422 and 503, with the business texts taken from the legacy story where the message already existed and MSG-GEN-004 used for the stale version and the terminal state.
7. Declare the consumed own authorise operation, the own access-log read and the `rwb-case` parameters read as consumed, each with its owner, one hop and the 2 s client budget; declare the case, task, retention, masking-policy and ledger operations as neither provided nor consumed here.
8. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes.
9. Add the contract tests: schema validation, the three schemas and their required fields, the state set, the envelope and message IDs, the consumed declarations and drift detection between a fake and the document.
10. Tag the baseline and hand it to RWB-P4-E8016-APP, the SCR-47 route of RWB-PLT-N001-CON, the access-log owner, the `rwb-case` parameters owner and the harness of the wave 4 access journey.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner, or declares a case, retention, masking-policy or ledger operation as provided here | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC5 |
| X3 | A response of 401, 403, 404, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A schema carries a name, an e-mail address, a national identity number, a phone number, an address, a date of birth or a user reference of the person or of the officer | The contract test fails; the review refuses the document | None | AC2, AC6 |
| X5 | A state outside `OPEN`, `IN_PROGRESS`, `ANSWERED` and `REFUSED` is declared, or an operation is declared to move a state it may not move | The review refuses the document | None | AC3 |
| X6 | The document declares a `case`, `task`, `decision_log_entry`, retention or masking-policy table as this service's, or declares a case state as written here | The review refuses the document | None | AC3, AC5 |
| X7 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X8 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X9 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |
| X10 | The `If-Match` header is declared optional, or the evidence block is declared to carry an actor name | The review refuses the document | None | AC2, AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the DP-03 entry schema, the P4 appendix T-A and the P3 and P4 contracts only |
| Negotiable | The statutory period, the reference shape and the page bounds are parameter rows behind the document; the base, the paths, the state set and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the SCR-47 route, the access-log owner and the harness on Day 1, and keeps the person out of the register and out of the evidence |
| Estimable | One OpenAPI document, one error envelope, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Handle a data subject request contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the data subject request register is held by rwb-access and the case, its hold and the statutory period are held by rwb-case

  Scenario: AC1 The OpenAPI 3.1 document describes the four operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the data subject request register is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/data-subject-requests, PATCH /admin/data-subject-requests/{requestId}, GET /admin/data-subject-requests/{requestId} and GET /admin/data-subject-requests with the owner rwb-access
    Then the open, the decision and the answer name Platform administration U, the two reads name Platform administration R, and every operation names its error responses 401, 403, 404, 409, 422 and 503
    Then the open requires an Idempotency-Key and the decision requires an If-Match
    Then no operation of rwb-case, rwb-decision or the access log is declared as provided by rwb-access

  Scenario: AC2 The schemas are fixed and carry no person (new, D-RCV-60)
    Given the DataSubjectRequest, DataSubjectRequestDecision and DataSubjectRequestList schemas of the document
    When the schemas of the published document are reviewed against the fields of this register
    Then the open request carries dataSubjectRef, requestType, caseIds, fieldIds, receivedAt and reason, with dataSubjectRef, requestType, caseIds and receivedAt required
    Then the answer carries requestId, requestType, state, openedAt, dueDate, version, steps and evidence
    Then the decision carries decision, fieldIds, effectiveFrom, refusalReason, answerSummary and reason, with decision and reason required
    Then the list carries items of requestId, requestType, state, openedAt, dueDate, overdue, page, size and total
    Then dataSubjectRef is a reference and no schema declares a name, an e-mail address, a national identity number, a phone number, an address, a date of birth or a user reference
    Then the evidence item carries the case id, the decision code, the decided time, the field ids and the mask flag, and no actor name
    Then the statutory period, the reference shape and the page bounds are read from the parameters contract and never from code

  Scenario: AC3 The state set is fixed and one operation moves each state (new, D-RCV-60)
    Given the state set of a data subject request in the document
    When the state set of the published document and the operations that move it are reviewed
    Then state is one of OPEN, IN_PROGRESS, ANSWERED and REFUSED
    Then the open moves a request to OPEN, the first correction or erasure decision moves it to IN_PROGRESS, and the answer or the refusal moves it to ANSWERED or REFUSED
    Then ANSWERED and REFUSED are terminal and any further decision is a 409
    Then the overdue flag is a computed answer field and not a state, and no workflow and no Schedule escalates it
    Then the document states that no case state, no hold and no task is written by this service

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by any operation
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002, 409 carries MSG-GEN-004 and 422 carries MSG-GEN-001
    Then 503 carries MSG-P7-003 and 404 carries MSG-GEN-004 with no personal value in the detail
    Then no operation declares a second error shape, and a break-glass grant adds a warning block carrying MSG-P4-004 with its end time to the answer and not a new error

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation, the access-log read and the parameters read this service calls
    When the declared operations of the published document are reviewed against their owners
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/access/v1/admin/access-log is declared as consumed with the owner P4 rwb-access and the case-id filter this document fixes
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then the case, task, retention, masking-policy and decision-ledger operations appear as neither provided nor consumed here
    Then the case hold and the document erasure appear as neither provided nor consumed here
    Then no operation owned by rwb-case, rwb-decision or rwb-source-data is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the access-log fake answers an entry with its case id, decision code, time, field ids and mask flag only, and no actor name
    Then no schema, example or fake carries a name, an e-mail address or a personal value, and no answer of this service carries a user reference

  Scenario: AC7 A schema change stays additive and a replay answers the first answer (new, D-RCV-60)
    Given the schemas and the write operations of version 1
    When a schema change or a replayed write is reviewed
    Then a removed, renamed or retyped field is refused as a new major version, and only additive change is allowed within version 1
    Then a write replayed with the same Idempotency-Key answers the first answer

  Scenario: AC8 Every business rule of section 8 is covered by a criterion and a test case (new, D-RCV-60)
    Given the business rules BR1 to BR12 of section 8
    When the covered-by column of the rules is reviewed
    Then every rule names at least one criterion of section 7 and at least one test case of section 16
    Then a rule without a criterion or without a test case fails the review
```

These eight criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-016 belong to RWB-P4-E8016-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1; TC-E8-016-CON-01 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5; TC-E8-016-CON-05 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are taken from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules R7.2 s14 | AC4; TC-E8-016-CON-04 |
| BR4 | The schemas carry the fields of this register and no field of another service: no case state, no retention class, no access entry and no ledger row | DP-01; Ownership Map v1 (`case` = P3, `decision_log_entry` = P7) | AC2; TC-E8-016-CON-02 |
| BR5 | The person is a reference: no schema, example, fake or entry of this contract carries a name, an e-mail address, a national identity number, a phone number, an address, a date of birth or a user reference | NFR-040; ASM-1589 | AC2, AC6; TC-E8-016-CON-02, TC-E8-016-CON-06 |
| BR6 | The state set is `OPEN`, `IN_PROGRESS`, `ANSWERED` and `REFUSED`, one operation moves each state, and the last two are terminal | FSD P4 v3 A2.27.4.1; ASM-1589 | AC3; TC-E8-016-CON-03 |
| BR7 | The statutory period, the person-reference shape and the page bounds are parameter rows behind the document and never fields of the code | DP-06; NFR-043; ASM-1590 | AC2; TC-E8-016-CON-02 |
| BR8 | The access-log read is consumed with its case-id filter, its owner, one hop and the 2 s budget, and the missing filter in TSD P4 v3 appendix T-A is carried in the gap and not added to the metadata; this service answers an access request from its own access entries only, and the workbench-wide answer is the P7 ledger query, joined by case id, with no personal value copied | GAP-0877; ASM-1592 | AC5; TC-E8-016-CON-05 |
| BR9 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC7; TC-E8-016-CON-08 |
| BR10 | A write requires an `Idempotency-Key` or an `If-Match`, and a replay answers the first answer | Architecture v5 slide 42; DP-09 | AC1, AC7; TC-E8-016-CON-01, TC-E8-016-CON-08 |
| BR11 | The contract declares no workflow, no activity and no Schedule for the capability, and no timer for the due date | Architecture v5 slide 14; TSD P4 v3 T5.3 | AC3; TC-E8-016-CON-03 |
| BR12 | The contract names no retention class, no masking policy row and no case hold: those are P5's, RWB-P4-E1037-APP's and `rwb-case`'s | Ownership Map v1; FSD P4 v3 screen list | AC5; TC-E8-016-CON-05 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The four operations, the three schemas, the state set and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the SCR-47 route, the access-log owner, the parameters owner and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a state is removed | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A consumed operation changes | The access-log read or the parameters read changes | Baselined, with the client budget and the stub restated |

The state set the document fixes for a data subject request is `OPEN`, `IN_PROGRESS`, `ANSWERED` and `REFUSED`, with the register of this service as its only writer and no case state among them. A case state such as the `HELD_LEGAL` of R-UNI-11 is `rwb-case`'s and `rwb-deviation`'s and is not declared here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the three schemas, the state set and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Compliance and PDPA officer, as the primary user of the feature | Reviews the open, the decision, the state set, the due date and the evidence block |
| Tech lead of the access-log capability (P4) | Reviews the read as `rwb-access` consumes it, owns its definition and the case-id filter |
| Tech lead of rwb-case (P3) | Reviews the parameters read as `rwb-access` uses it; owns its definition and the statutory-period row |
| Internal audit | Reviews the evidence fields, the absence of an actor name and the stable order of the list |
| Data steward | Confirms that no name, e-mail address, personal value or user reference is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

The empty, loading, error and no access states of SCR-47 are Not specified in the source documents (DOR-RWB-P4-E8016-CON-10); this contract declares no screen.

| Item | Content | BR Field ID |
|---|---|---|
| `DataSubjectRequest` open request | `dataSubjectRef` (a reference, validated against a parameter row), `requestType` (`ACCESS`, `CORRECTION`, `ERASURE`), `caseIds`, `fieldIds`, `receivedAt` (a date), `reason`; `dataSubjectRef`, `requestType`, `caseIds` and `receivedAt` required, `fieldIds` required for a correction and for an erasure | Not specified in the source documents (DOR-RWB-P4-E8016-CON-7) |
| `DataSubjectRequest` answer | `requestId`, `requestType`, `state`, `openedAt`, `dueDate`, `version`, `steps[]` in entry order, `evidence[]` for an access request | Not specified in the source documents (DOR-RWB-P4-E8016-CON-7) |
| `DataSubjectRequestDecision` request | `decision` (`CORRECTION`, `ERASURE`, `ANSWER`, `REFUSAL`), `fieldIds`, `effectiveFrom`, `refusalReason`, `answerSummary`, `reason`, under an `If-Match`; `decision` and `reason` required, `fieldIds` required for a correction and for an erasure, `effectiveFrom` required for an erasure, `refusalReason` required for a refusal | Not specified in the source documents (DOR-RWB-P4-E8016-CON-7) |
| `DataSubjectRequestDecision` answer | `requestId`, `state`, `decision`, `version`, `updatedAt`, and for an erasure `maskingVersion` and `maskingRowCount` | Not specified in the source documents (DOR-RWB-P4-E8016-CON-7) |
| `DataSubjectRequestList` | `items[]` of `requestId`, `requestType`, `state`, `openedAt`, `dueDate`, `overdue`, `page`, `size`, `total` | Not specified in the source documents (DOR-RWB-P4-E8016-CON-7) |
| Evidence item | `caseId`, `decisionCode`, `decidedAt`, `fieldIds[]`, `masked`; no actor, no name, no value | Not specified in the source documents (DOR-RWB-P4-E8016-CON-7) |
| Roles and letters | The role code of the caller and of the erasure, and the capability areas of `role` DF-REF-034 to DF-REF-039 and `permission` DF-REF-040 to DF-REF-044, read behind the authorise answer; a request reads the capability area Platform administration, the write the U letter and the reads the R letter | DF-REF-034 to DF-REF-044 |
| Masking rows, as consumed by the story | `masking_rule` DF-REF-198 to DF-REF-204: `role_code`, `field_id`, `unmasked`, `masking_version`, `valid_from`, `valid_to` | DF-REF-198 to DF-REF-204 |
| Record event | `rwb.decision.DecisionRecorded.v1` with the entry of a step, from the DP-03 library | Not specified in the source documents (DOR-RWB-P4-E8016-CON-7) |
| Refusal | `messageId` MSG-P4-001 on a 401, MSG-P4-002 on a 403, MSG-GEN-004 on a 404 and a 409, MSG-GEN-001 on a 422 and MSG-P7-003 on a 503 | Not specified in the source documents (DOR-RWB-P4-E8016-CON-7) |

The exact field set of the three schemas, the type and length of each field, the shape of `dataSubjectRef`, the record code of a data subject request and the case-id filter of the access-log read are Not specified in the source documents (GAP-0874; ASM-1589) and (GAP-0877; ASM-1592): FSD P4 v3 A2.27 names the journey, two validation rules and BR-P4-027 and no operation and no field, and the P4 appendix T-A declares neither a data subject request operation nor a case filter on the access log. The statutory period is Not specified either: NFR-043 states the target as "Statutory period, Not set as a working service level" and marks it "Open, DL26" (GAP-0875; ASM-1590). Where a corrected value is applied and where an erased field is removed are recorded here (GAP-0876; ASM-1591): rwb-source-data and rwb-case, which hold the personal field, apply a corrected value and remove or blank an erased field; an erasure covers the fieldIds of its request and no other field; a case hold of R-UNI-11 takes precedence over a retention class, and a retention class over a masking row written by RWB-P4-E1037-APP. This document declares no value field. Open decision DL26 applies and is still open; its assumptions are ASM-0247, ASM-0264, ASM-0275 and ASM-0355.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/data-subject-requests` | `DataSubjectRequest` in; `DataSubjectRequest` out in state `OPEN` with `requestId`, `openedAt`, `dueDate`, `version` and the `Location` of the read by id | Platform administration U; `Idempotency-Key` required |
| PATCH | `/admin/data-subject-requests/{requestId}` | `DataSubjectRequestDecision` in; the decision out with `state`, `version`, `updatedAt` and, for an erasure, `maskingVersion` and `maskingRowCount` | Platform administration U; `If-Match` required; Idempotency-Key: Not specified in the source documents (DOR-RWB-P4-E8016-CON-8) |
| GET | `/admin/data-subject-requests/{requestId}` | `DataSubjectRequest` out with its `steps` and its `evidence` block | Platform administration R, scope applied |
| GET | `/admin/data-subject-requests` | `DataSubjectRequestList` out, paged, ordered by `openedAt` then request id | Platform administration R, scope applied |

Errors for all four: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 404 no request with that id (MSG-GEN-004), 409 a stale `If-Match` or a state that does not accept the decision (MSG-GEN-004), 422 a required field empty or a value of the wrong shape (MSG-GEN-001), 503 a read or a record that cannot be completed (MSG-P7-003). The open is a write and carries an `Idempotency-Key`; the decision is a write and carries an `If-Match`; both reads carry neither and are a read only. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR9).

The four paths are fixed here (GAP-0874; ASM-1589). No case, retention, masking-policy or ledger operation is declared as provided in this document.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The C check behind the open, the A check behind the decision and the R check behind the reads, cached for the session |
| GET | `/api/recovery/access/v1/admin/access-log` | P4 rwb-access | The access entries of the case ids of a request, with the case-id filter this document fixes, for the evidence block (API-P4-008; BR8) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The statutory period, the person-reference shape and the page bounds, with the version in force (DP-06) |

None of the three is declared as provided by rwb-access in this document, although two are owned by this service: the authorise operation is RWB-P4-E1037-CON's and the access-log read is RWB-P4-E1039-CON's, so both appear here as consumed and are stubbed by their fakes. The case-id filter is not in the T-A list of API-P4-008, which declares `user`, `from`, `to`, `event`, `page` and `size`; it is fixed here and raised with the access-log owner (GAP-0877; ASM-1592), and the gap is not added to this story's metadata. The case read, the task operations, the retention operations, the masking-policy operations and `GET /decision-log` appear nowhere in this document as provided or consumed.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of a step with its request id, type, person reference, case ids, field ids, decision code, role code, received date, due date and time, with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

This document declares the record message only. `rwb.access.AccessPolicyChanged.v1` is RWB-P4-E1037-APP's and `rwb.access.DoaLimitChanged.v1` is RWB-P4-E8008-APP's, and a data subject request publishes neither (Architecture v5 slide 14); a request announces no change on `rwb.access.events.v1`, because the caching consumers of that topic have nothing to refresh for a register.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14, and the four operations of this contract need no subscription. The document declares no inbox and no consumer group, and no case, retention or ledger event is consumed.

#### 12.5 Workflows and activities

None. No workflow, no activity and no signal is part of this contract: the open, the decision and the answer are synchronous, and the statutory due date is data and not a timer (BR11). The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only.

#### 12.6 Schedules

None. All four operations are request-driven, and the due date of a request is computed from its received date and the parameter row in force; no Schedule reminds, escalates or closes a request in this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role code of the caller and the role codes an erasure covers |
| `permission` | P4 (rwb_access) | The U and R letters of Platform administration and the role they are held through |
| `masking_rule` | P4 (rwb_access), created by RWB-P4-E1037-APP | The rows an erasure writes: `role_code`, `field_id`, `unmasked`, `masking_version`, `valid_from` |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The step entries the register is built from and the record event carries |
| `idempotency_key` | PLT library, created in rwb_access | The stored request and answer of an open, so one key answers one request (DP-09; ASM-0074) |
| `case`, `task`, `parameter_catalog`, `lov_value` | P3 (rwb_case) | Not named as this service's: the period arrives in the consumed answer and no case row is read (DP-01, DP-06, DP-07) |
| `decision_log_entry` | P7 (rwb_decision) | Not named as this service's: the ledger consumes the topic and answers its own query |
| retention, consent and the case hold | P5 and the P3 and S8 work | Declared nowhere in this document (BR12) |

No table of another service is named in the contract (DP-01): `template`, `notice` and `merge_field` are not part of this capability, `decision_log_entry` and the rule registry are P7 rwb_decision's, and `case`, `task`, `parameter_catalog` and `lov_value` are P3 rwb_case's. The register is a chain of entries and not a table, so the document names no request table and no column of one (BR1 of the app story).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| parameters fake | `GET /admin/parameters` with the statutory-period row at "2027.1" (45 days) and at "2027.2" (60 days), the person-reference shape, the page bounds, a version not in force and a 503 | App story, contract tests, harness |
| authorise fake | `POST /authorise` with a granted answer for RW-COE with C, RW-RISK with A and RW-AUDIT with R in Rules and parameters, and a refused answer with MSG-P4-002 for RW-CASEOWN with R only and for a C holder without A | App story, contract tests, harness |
| access-log fake | `GET /admin/access-log?caseId=...` answering two `AC-READ` entries and one `AC-EXPT` entry for "RW-2026-000123", each with its field ids and mask flag, an empty page for a case with no entry and a 503 | App story, contract tests, harness |
| decision-record fake | The append of a step, the hash-link check, a seeded register of "DSR-2027-000118" with its opening, its erasure decision and its answer, and a forced failure | App story, contract tests |
| gateway-bff fake | The composite route of SCR-47 with the register list, the request form, the decision form and the evidence panel | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 3 consumed | The open, the decision, the read and the list provided; the authorise, the access-log read and the parameters read consumed; one hop, 2 s timeout |
| Kafka | 1 event type published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | No file input and no file output; the evidence is an answer block and not a document |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-data-subject-request-v1.yaml` (OpenAPI 3.1) with the four operations and the shared components, `contract/error-envelope.yaml`, the `DataSubjectRequest`, `DataSubjectRequestDecision` and `DataSubjectRequestList` schemas with their examples, the state-set rule and the versioning rules in the contract README, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own. The access-log read is consumed and faked, and its missing case-id filter is carried in the gap row of the key and not added to this story's metadata (GAP-0877; ASM-1592).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The four operations with the shapes of section 11: the open, the decision with its `If-Match`, the read with its steps and its evidence, and the list with its paging.
3. The state set of BR6, stated in the document and in the contract README, with the operation that may move each state and the terminal pair named.
4. The evidence block of a read, with the five fields of an item and the explicit statement that no actor name and no personal value is part of it.
5. The consumed operations with their owners, the one-hop rule and the 2 s client budget, the case-id filter of the access-log read, and the explicit statement that no case, retention, masking-policy or ledger operation is provided here.
6. The error envelope and the message-ID mapping for 401, 403, 404, 409, 422 and 503, with the texts of the legacy messages and MSG-GEN-004 for the conflict and the absent request.
7. The five fakes and the stub fixtures of section 12.8, including the two versions of the statutory-period row and the seeded register of "DSR-2027-000118".
8. The six contract tests; a drift between a fake and the document fails the build.
9. Baseline tag and the consumer sign-off note from the app story, the SCR-47 route, the access-log owner, the parameters owner and the harness.

**Feature switch.** The four operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of this contract; the document declares no 404 branch of its own beyond the absent request and adds no parameter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8016-APP | The four provided operations, the three schemas, the state set, the evidence block and the five fakes |
| RWB-PLT-N001-CON (gateway-bff and SCR-47) | The register list, the request form, the decision form with its `If-Match` and the evidence panel |
| The access-log owner (RWB-P4-E1039-CON) | The read as consumed, with the case-id filter this document fixes |
| The `rwb-case` parameters owner (RWB-P3-E1042-CON) | The statutory-period row, the reference shape and the page bounds as consumed |
| The harness of the wave 4 access journey | The due date, the state path and the evidence as the facts it records |

The shape of `dataSubjectRef`, the record code of a data subject request and the case-id filter of the access-log read are Not specified in the source documents (GAP-0874; ASM-1589) and (GAP-0877; ASM-1592); the reference is validated against a parameter row, the record code is the library's data subject request code, and both are confirmed with Compliance and with the decision-record library owner before the operations are frozen.

**Done when.** The document validates in the pipeline, the six contract tests pass, the five fakes answer every declared path, the access-log owner has accepted the case-id filter, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without Rules and parameters C opens, without A decides, or without R reads | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty, `requestType` is not one of the three, `caseIds` is empty, `fieldIds` is missing for a correction or an erasure, `receivedAt` is not a date, or `dataSubjectRef` is not of the shape in force | Enter {field}. |
| MSG-GEN-004 | The `If-Match` is stale, the state does not accept the decision, or no request has that id | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The parameters read or the access-log read cannot be completed, or a step cannot be recorded | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001 and MSG-P7-003 are the five texts of RWB-E8-016, copied unchanged; MSG-GEN-004 is the platform conflict text, declared here for the stale version, the terminal state and the absent request. MSG-P4-003, the legacy scope message of another key, is declared on no response of this document, because a request is scoped by role and by the person reference and not by a case in the caller's scope.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-47 Personal data | Loading, list | `DataSubjectRequestList` with the type, state, received date, due date and overdue flag of each request |
| SCR-47 Personal data | Register, empty | An empty `items` with total 0 and no error |
| SCR-47 Personal data | Request, form | `DataSubjectRequest` request with `dataSubjectRef`, `requestType`, `caseIds`, `fieldIds`, `receivedAt` and `reason` |
| SCR-47 Personal data | Request, opened | `DataSubjectRequest` answer in state `OPEN` with `openedAt`, `dueDate` and the `Location` |
| SCR-47 Personal data | Decision, form | `DataSubjectRequestDecision` request with its `decision`, its field ids, its effective date and its reason, and the `If-Match` the screen holds |
| SCR-47 Personal data | Decision, recorded | The decision answer with the new state and version, and for an erasure `maskingVersion` and `maskingRowCount` |
| SCR-47 Personal data | Decision, stale | The 409 of the envelope with MSG-GEN-004 and a reload action |
| SCR-47 Personal data | Request, answered | The `steps` of the request in order, the answer and whether the due date was met |
| SCR-47 Personal data | Evidence | The `evidence` block: one item per access entry with its case id, decision code, time, field ids and mask flag |
| SCR-47 Personal data | Evidence, empty | An empty `evidence` block and no error |
| SCR-47 Personal data | Refused | The 403 of the envelope with MSG-P4-002 |
| SCR-47 Personal data | Error | Not specified in the source documents (CG-ALL-5636) |
| SCR-47 Personal data | No access | Not specified in the source documents (CG-ALL-5636) |
| SCR-47 Personal data | Not recorded | The 503 of the envelope with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |

The screens are served by the gateway-bff composite route (DP-19), which shows the register from this service and calls the four operations of this contract, one hop each. The composite route specification, the retention panel, the masking-policy panel and the consent log belong to RWB-PLT-N001-CON, to RWB-P4-E1037-APP and to the retention work of P5; the document fixes the request register and its evidence only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-016-CON-01 | AC1 | Contract | The document validates; the base, the four operations, the letters U and R in Platform administration, the six error responses, the `Idempotency-Key` on the open and the `If-Match` on the decision are present; no case, retention, masking-policy or ledger operation is provided |
| TC-E8-016-CON-02 | AC2 | Contract | The fields and required fields of `DataSubjectRequest`, `DataSubjectRequestDecision` and `DataSubjectRequestList`, the five fields of an evidence item, `dataSubjectRef` as a reference, and no name, e-mail address, personal value or user reference in any schema |
| TC-E8-016-CON-03 | AC3 | Contract | The four states, the operation that moves each, the terminal pair, the overdue flag as a computed field, and no case state, hold or task written by this service |
| TC-E8-016-CON-04 | AC4 | Contract | A 401, 403, 404, 409, 422 and 503 response carry one problem envelope with a valid message ID, 409 and 404 carry MSG-GEN-004, and no second error shape is declared |
| TC-E8-016-CON-05 | AC5 | Contract | Three consumed operations with their owners P4 and P3, the case-id filter of the access-log read, one hop and the 2 s budget; the case, task, retention, masking-policy and ledger operations, and the case hold and document erasure, declared as neither provided nor consumed |
| TC-E8-016-CON-06 | AC6 | Component | The five fakes match the document; a drifted fake fails the build; the access-log fake carries no actor name and the evidence item no value |
| TC-E8-016-CON-07 | AC5 | Contract | Each table of section 12.7 is read at its boundary: the rows it names as owned are accepted, and a table or row of another service fails the contract test |
| TC-E8-016-CON-08 | AC7 | Contract | A schema change that removes, renames or retypes a field is refused within major version 1, and a replayed write with the same `Idempotency-Key` answers the first answer |
| TC-E8-016-CON-09 | AC8 | Contract | Each rule BR1 to BR12 of section 8 names at least one criterion of section 7 and at least one test case row of section 16; a rule without either fails the review |

### 17. Guardrails

- No business value in the contract: the statutory period, the reference shape and the page bounds stay parameter rows behind the document, and the role codes stay rows of `role` and `permission`.
- No personal data in a schema, an example or a fake: person references, case ids, field ids, decision codes, role codes and times only, and no user reference of the officer or of the person (BR5).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access` and by its parameters owner; `case`, `task`, `decision_log_entry`, the retention classes and the masking policy are not named as fields of this register (BR4, BR12).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- One writer of a request state: the document states that the register of this service moves `OPEN`, `IN_PROGRESS`, `ANSWERED` and `REFUSED`, and that no case state is written here (BR6).
- The access-log read is consumed and faked, and its missing case-id filter is carried in the gap rather than added to the metadata (BR8).
- Every example in the document is synthetic; no production personal value is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- A write without its `Idempotency-Key` or its `If-Match` is refused by the contract, and a replay never makes a second step (BR10).
- The due date is declared as an answer field computed from the parameter row, never as a constant and never as a timer (BR7, BR11).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S8-007 | A data subject request holds automated processing on the case and routes to Compliance inside the statutory period | The four operations as the register of the request, the state set with the terminal answer, and the statement that the hold and the routing stay with `rwb-case` and `rwb-deviation` | TC-E8-016-CON-01, TC-E8-016-CON-03 |
| NFR-043 | A data subject access, correction or erasure request is answered inside the statutory period | `dueDate` and `overdue` as answer fields computed from the parameters contract, and the evidence block of an access request | TC-E8-016-CON-02, TC-E8-016-CON-05 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules R7.3; NFR-043 carries the status "Open, DL26" in TSD P4 v3 T7, which is why the period is a parameter row and its value is a gap. The Work Package carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 handle a data subject request inside the statutory period, with the result written to the decision log | Sections 4, 7 (AC1, AC2), 11, 12.1, 12.3 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 7, 12.1, 14 |
| The permission check: Rules and parameters C for RW-COE and A for RW-RISK | Sections 7 (AC1, AC5), 10, 12.1, 14 |
| The legacy data rows `decision_log_entry` DF-DEC-001 to DF-DEC-018 and `role` DF-REF-034 to DF-REF-038 | Section 11, section 12.7 |
| The legacy endpoints `/admin/rule-versions` and `/admin/rule-versions/{versionId}/approve` on the monolith base | Section 19 and GAP-0878; ASM-1593: a rule-version load and approval are RWB-P4-E8007-APP's and RWB-P4-AD011-APP's and are declared nowhere in this document |
| The legacy screens SCR-47 Personal data and SCR-39 Rules and parameters as the story named them | Section 15, carried to SCR-47 Personal data |
| Legacy key RWB-E8-016, story RWB-P4-E8016-APP, contract RWB-P4-E8016-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the four operations, the state path, the erasure writer and the evidence reader (RWB-P4-E8016-APP).
- The masking policy and its panel: the field list, the versions and the rows a role may see (RWB-P4-E1037-APP and RWB-P4-AD004-APP). This document declares the rows an erasure writes and no policy value.
- The access log and its owner: the writer, the break-glass grant, the search and the export (RWB-P4-E1039-APP, RWB-P4-AD007-APP and the DB and OPS stories of that key). This document consumes the read.
- The case, its state and its hold, and the routing of a request to Compliance (R-UNI-11, REQ-S8-007): `rwb-case` and `rwb-deviation`.
- The retention classes, the retention of a request and of an access entry, and the consent log (the `rwb-document` retention work, RWB-P4-E1037-APP and the P3 and S8 reference work).
- The generation and dispatch of the answer letter to a data subject (FEAT-OCC-01 and the P6 stories).
- The central decision ledger, the workbench-wide access query and the chain verification (P7 `rwb-decision`).
- The screen SCR-47 Personal data, its other panels and its composite route specification (RWB-PLT-N001-CON and RWB-P4-E1037-APP).
- The correction and the erasure in the owning services (GAP-0876; ASM-1591).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The operations of other services: the authorise operation, the access-log read and the parameters read are consumed and faked, never defined here.
- The cross-service journey harness and its evidence, and the `-ITG` copies of the test cases.
