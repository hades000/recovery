# RWB-P4-E1039-CON Access log into the decision log and break-glass admin

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes.**

- Corrected the decision-record event type name to `rwb.decision.DecisionRecorded.v1` (2 places); the topic `rwb.decision-record.v1` is unchanged.
- Readiness decisions: RD-P1-008.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: contract slice of legacy RWB-E1-039 for rwb-access — the access-log read and the break-glass grant, end and read operations with their record shape, two-person rule, time box, refusal vocabulary and fail-closed rule. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 16 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E1039-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Contract version | 1 (major version 1 in the path `/api/recovery/access/v1`; an additive field within version 1 is compatible, BR10) |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-039 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E1039-CON-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-023, FR-P4-024, FR-P4-025, FR-P4-026, FR-P4-027, FR-P4-028, FR-P4-029, FR-P4-030, FR-P4-031) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-008 |

### 1. Story

As a **tech lead**, I want **the published contract baseline of the access log and the break-glass grant of `rwb-access`: an OpenAPI 3.1 document for the access-log read and the grant, end and read operations, the fixed record shape of one access-log entry, the two-person rule of break-glass with its time box, one refusal vocabulary with one error envelope, the fail-closed rule, the consumed session, parameters and reference-data operations with their owners, and the contract fakes**, so that **the app story, the gateway-bff route, the security administrator's review and the integration harness can build against a fixed, testable contract on Day 1 without waiting for `rwb-access`, the schema or the central ledger to be built**.

This is the contract slice of legacy key RWB-E1-039 under epic RWB-SVC-P4. It carries no legacy acceptance criterion: **AC1 to AC10 of RWB-E1-039 belong to RWB-P4-E1039-APP**, and the seven criteria of section 7 are new and test the document, the two shapes, the vocabulary, the fail-closed rule, the consumed declarations and the fakes.

**The division of this legacy key is fixed and is the same in all four stories.** **RWB-P4-E1039-APP** owns the ten legacy criteria and implements the writer, the grant and the read. **This story** owns the published contract of the four operations, the record shape of one entry, the two-person rule, the time box, the refusal vocabulary and the fail-closed rule. **RWB-P4-E1039-DB** owns the ACE DB slice in `rwb_access`: the Flyway sequence, the four tables of the key, the grants, the retention and the partitioning. **RWB-P4-E1039-OPS** owns the DevOps slice: the Helm values, the Kafka ACLs, the secrets, the alerting and the run book. **The end-to-end proof is RWB-ITG-E1039-ITG**, and the two neighbours of the same legacy key are **RWB-P5-E1039-APP** on the document side and **RWB-P7-E1039-APP** on the ledger side.

The contract declares no event of its own and consumes none: the entry it describes is published by the DP-03 library as `rwb.decision.DecisionRecorded.v1` and is named in section 12.3 only, and `rwb-access` is the reference-data owner of Architecture v5 slide 14, whose contract line records no consumed event.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story answered the access log and the break-glass grant out of one package inside one process, with a publisher called in-process and one `decision_log_entry` table, so the shape of an entry, the time box and the refusal vocabulary were decided by whichever module asked. In the target, the entry is a decision record of the serving service's own chain (DP-03), the central ledger collects it from `rwb.decision-record.v1` and answers the workbench-wide query (Architecture v5 slides 28 and 42; ADR-022), and the grant is an operation of the access owner. Three consumers need those answers to mean the same thing — the app story that implements the operations, the gateway-bff route that renders the banner and the access-log panel, and the harness that proves the journey across the wave 1 services — or each of them will invent its own.

**The division is fixed and is the same in all four stories.** The permission matrix, the masking policy and the scope rule stay with RWB-P4-E1037-APP; the writer, the grant and the read are **RWB-P4-E1039-APP**'s; the schema, the grants and the retention are **RWB-P4-E1039-DB**'s; the deployment and the alerts are **RWB-P4-E1039-OPS**'s; **RWB-P4-E1039-CON** fixes only what they must all agree on, and **RWB-ITG-E1039-ITG** proves it end to end. **RWB-P5-E1039-APP** writes the entry of a document content read where the document is served, and **RWB-P7-E1039-APP** owns the central ledger and the `GET /decision-log` query; both build to the shapes of this document, and neither defines them.

Fixing the shape once, with faked consumers, lets the app story build in parallel with the DP-03 library, the two rwb-case contracts and the ledger work of P7, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

Two things the document fixes are the point of the legacy story rather than its plumbing. **The two-person rule**: the person who asks for break-glass in the bank IAM, the person who approves it there and the person who reviews the use are never the same person, and the grant operation verifies the approval rather than granting it. **The time box**: a grant ends at the earlier of the parameter window and the IAM group end, with no action by anyone, and the check runs on every request rather than in a job — so a forgotten grant cannot outlive its window. The values of the criteria are the legacy values unchanged: incident INC0004521, IAM request IAM-778812, group RWB-SIT-BREAKGLASS, case RW-2026-000123, the 10:30 to 14:31 window of the test clock, the 12-character reason with its 20 and 1000 bounds, Idempotency-Key k-001 and k-002, and the messages MSG-P4-002, MSG-P4-004, MSG-P4-007, MSG-GEN-001 to MSG-GEN-004 and MSG-P7-003.

It supports REQ-ACA-006 and REQ-ACA-008. Where no source names the end and read paths of a grant, gives the business message id of an expired session, or fixes the grant answer beyond the legacy request and response fields, the document builds to the assumption in force and records the open point as Not specified in the source documents (GAP-0781; ASM-1425) and (GAP-0781; ASM-1426).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the operation names follow the platform rule rather than a local choice.
- RWB-PLT-E1027-CON is published: the DP-03 library and the `rwb.decision-record.v1` message, whose entry shape this document describes and never extends.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that consumes the access-log read and the session read, and one of the two sign-off parties of this baseline.
- The platform error envelope, the CloudEvents 1.0 envelope and the `Idempotency-Key` rule of every POST are the platform baseline; where this document narrows them it says so explicitly.
- The operations and their owners come from the Ownership Map only: `GET /admin/access-log`, `POST /admin/break-glass-grants`, `GET /me/session` and `GET /admin/roles` are P4's, and the parameters and reference-data operations this document consumes are P3's. No table of another service is named (DP-01).
- The parameters and the reference lists are those of the legacy story: `rwb.access.breakglass.window-hours=4`, `rwb.access.breakglass.incident-pattern=^INC[0-9]{7}$`, `rwb.access.breakglass.reason-min=20`, `rwb.access.breakglass.review-days=1` (assumed values; DL38), and LOV-DECISION with the access event codes AC-SIGN, AC-DENY, AC-READ, AC-EXPT, AC-BGON and AC-VERS.
- No approval is required to publish a Draft baseline; the document is tagged for consumers when the contract tests of section 16 pass.
- No build dependency: this story has only CON dependencies by rule, so it is ready on Day 1 and sits in contract group CG-W1 (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the paging parameters, the idempotency header and the two schemas.
2. Fix the record shape of one access-log entry in `AccessLogEntry`: the decision code from its list, the actor reference, the case id where there is one, the document id, the capability area, the right, the result, the list of field ids with their mask flag, the filter and the row count for a list or an export, the grant id, the incident reference, `decidedAt`, `matrixVersion` and `maskingVersion`.
3. Fix the `AccessLogPage` answer: the items, the page and the size, the total, and the two version fields the entries were read under.
4. Fix the four operations: the access-log read, the grant activation, the grant end and the grant read, each with its security right, its idempotency rule, its success status and its error set.
5. Fix the two-person rule, the time box and the end rule of a grant in the document, with `endsAt` stated as the earlier of the parameter window and the IAM group end, and the end enforced on every request.
6. Agree the refusal vocabulary and the envelope: MSG-P4-002, MSG-P4-004, MSG-P4-007, MSG-GEN-001 to MSG-GEN-004 and MSG-P7-003, with the business texts copied unchanged from the legacy story.
7. Fix the fail-closed rule: an access-log read or a grant call whose entry cannot be written answers 503 with MSG-P7-003, no business payload and no partial answer.
8. Declare the consumed session, parameters and reference-data operations as consumed, each with its owner, one hop and the 2 s client budget.
9. Publish the nine contract tables of section 12 and the seven fakes, then run the contract tests and tag the baseline for the app story, the gateway-bff route and the harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC6 |
| X3 | An entry field carries a personal value, or the mask flag is stated as anything but `clear` or `masked` | The review and the contract test refuse the document | None | AC2, AC7 |
| X4 | A grant answer is declared without the two-person rule, without `endsAt`, or with an end that is not the earlier of the window and the group end | The contract test fails | None | AC3 |
| X5 | A response of 401, 403, 409, 422 or 503 is declared without the envelope or without its message id | The contract test fails | None | AC4 |
| X6 | A fail-closed branch is declared with a business payload or with a status other than 503 | The contract test fails; an unaudited read must never look like a success | MSG-P7-003 | AC5 |
| X7 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC6 |
| X8 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC7 |
| X9 | The window, the incident pattern or the reason bounds change | The parameter row changes and the document's bounds are restated; no schema change and no new major version | None | AC3 |
| X10 | A field of the answer has no source definition | The field carries the placeholder and the gap is carried; no field is invented | None | AC2, AC3 |

Alert, routing and deployment values (GAP-0783). The routes of a failed or refused access-log write and of break-glass use, and their thresholds, are deployment values with a parameter row behind them; the routes in force and the thresholds are Not specified in the source documents (GAP-0783). The Kafka ACL set of rwb.decision-record.v1 follows the producer rule of the platform and the platform retry topics, and its retry cadence is Not specified in the source documents (GAP-0783). The secret names, their key references and the deployment topology values are Not specified in the source documents (GAP-0783).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the Ownership Map, the platform envelopes, the DP-03 message and the two rwb-case contracts only |
| Negotiable | The end and read paths and the grant answer detail are open until the contract freeze; the base, the four operations, the entry shape and the vocabulary are fixed by the target architecture |
| Valuable | Unblocks the app story, the screen route and the harness on Day 1, and keeps the central ledger out of the `rwb-access` contract |
| Estimable | One OpenAPI document, two schemas, one envelope, nine contract tables, seven fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Access log and break-glass contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the access-log half of the legacy journey is the grant, the entry and the read over the local decision-record chain

  Scenario: AC1 The document describes the four operations and validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the access log and the grant is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares GET /admin/access-log, POST /admin/break-glass-grants, POST /admin/break-glass-grants/{grantId}/end and GET /admin/break-glass-grants/{grantId} with the owner rwb-access
    Then every operation names its security right, Platform administration R for the two reads and C for the two writes, and its error responses
    Then no operation of another service is declared as provided by rwb-access

  Scenario: AC2 The record shape of one access-log entry is fixed (new, D-RCV-60)
    Given the AccessLogEntry and AccessLogPage schemas of the document
    When a reader is given one access-log entry and its page to check against the record shape of the contract
    Then the entry carries decisionCode as one of AC-SIGN, AC-DENY, AC-READ, AC-EXPT, AC-BGON and AC-VERS, actorReference, capabilityArea, right, result, decidedAt, matrixVersion and maskingVersion
    Then the entry carries caseReference and documentReference as optional values, and filter and rowCount for a list or an export
    Then the entry carries grantId and incidentReference as optional values, present only while a grant is active
    Then field ids are declared as a list of fieldId with a mask flag of clear or masked and never a value
    Then the page carries items, page, size, total, matrixVersion and maskingVersion
    Then no schema, example or fake carries a personal value

  Scenario: AC3 The grant fixes the two-person rule and the time box (new, D-RCV-60)
    Given the BreakGlassActivation and BreakGlassGrant schemas of the document
    When an activation request and its grant are checked against the two-person rule and the time box
    Then the activation carries incidentReference, iamRequestId, capabilityArea, right, scope and reason with a minimum of 20 and a maximum of 1000 characters
    Then the grant carries grantId, incidentReference, capabilityArea, right, scope, startsAt and endsAt
    Then the document states that the requester, the IAM approver and the reviewer are never the same person, and that the operation verifies the approval and never grants it
    Then the document states that endsAt is the earlier of the parameter window and the IAM group end, and that the end is enforced on every request
    Then the end and the read operations carry the grant id in the path and refuse an ended grant for every right beyond the role's own letters
    Then the window, the incident pattern and the reason bounds are read from the parameters contract and are never constants in the document

  Scenario: AC4 Every refusal is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 409, 422 or 503 response is produced by any of the four operations
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 403 carries MSG-P4-002 for a missing right and MSG-P4-007 for a missing or unverified IAM approval
    Then 409 carries MSG-GEN-004 and 422 carries MSG-GEN-001, MSG-GEN-002 or MSG-GEN-003
    Then 503 carries MSG-P7-003 and the active grant banner carries MSG-P4-004 with its end time
    Then no operation declares a second error shape

  Scenario: AC5 The fail-closed rule is fixed in the document (new, D-RCV-60)
    Given the access-log read and the grant operations
    When the access-log read or a grant operation is called and its entry cannot be written
    Then each declares that an entry which cannot be written answers 503 with MSG-P7-003 and no business payload
    Then the access-log read declares no partial page and no empty page in that case
    Then the grant activation declares no grant and no AC-BGON entry in that case
    Then the document states that an unaudited read is refused rather than served

  Scenario: AC6 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the session read, the parameters read and the reference-data read this service calls
    When each consumed operation is checked against the owner and hop rules of the document
    Then GET /api/recovery/access/v1/me/session is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters and GET /api/recovery/case/v1/admin/lists/{listCode} are declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then no operation owned by rwb-case, rwb-decision or rwb-document is declared as provided by rwb-access

  Scenario: AC7 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the seven contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the grant fake answers an ACTIVE and an ENDED grant for incident INC0004521 and IAM request IAM-778812
    Then no schema, example or fake carries a name, an e-mail address or a personal field

  Scenario: AC8 Every business rule is covered by a criterion and a test (new, D-RCV-60)
    Given the business rules BR1 to BR11 of section 8
    When the coverage of the rules by the criteria and the test cases is checked
    Then each rule names at least one criterion of section 7 in its Covered by column
    Then each criterion of section 7 is covered by at least one test case of section 16
    Then a rule without a criterion or without a test fails the review of the story

  Scenario: AC9 A request the document does not provide answers 404 (new, D-RCV-60)
    Given the four provided operations of the document
    When a request names a path of the base that the document does not declare, or a grant id that is not found
    Then the answer is 404 and the body is the one RFC 9457 problem response of AC4
    Then the message id is Not specified in the source documents (NEWAC-RWB-P4-E1039-CON-AC12)
    Then no operation of another service answers in its place

  Scenario: AC10 A replay of a write with the same idempotency key creates nothing twice (new, D-RCV-60)
    Given the two write operations that create a grant and end a grant
    When a write is replayed with the same idempotency key
    Then the replay creates no second grant and no second end
    Then the answer to the replay is Not specified in the source documents (NEWAC-RWB-P4-E1039-CON-AC13)
```

These criteria test the artefact only. No criterion restates a legacy acceptance criterion: AC1 to AC10 of RWB-E1-039 belong to RWB-P4-E1039-APP, and their end-to-end form belongs to RWB-ITG-E1039-ITG.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the Ownership Map | DP-11; Ownership Map v1 | AC6 |
| BR3 | Error responses use one envelope and one message id per condition, and the business texts are copied unchanged from the legacy story | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC4 |
| BR4 | The entry the document describes is the decision record of DP-03, written locally by each service and relayed on rwb.decision-record.v1: the contract describes it, adds no field and this service writes no decision record of another service | DP-03; RWB-PLT-E1027-CON; GAP-1250 | AC2 |
| BR5 | The contract declares no table of another service and no central ledger; `decision_log_entry` is P7's and the grant table is this key's | DP-01; Ownership Map v1 | AC1 |
| BR6 | Break-glass needs an approval in the bank IAM against an open incident, and the requester, the approver and the reviewer are never the same person | Admin and access model, section 5.3 and 6.2; REQ-ACA-008 | AC3 |
| BR7 | A grant ends at the earlier of the parameter window (4 hours) and the IAM group end, and the end is enforced on every request rather than by a job | rwb.access.breakglass.window-hours; DL38 (open; assumptions ASM-0245, ASM-1413, ASM-1424, ASM-1508) | AC3 |
| BR8 | An access entry states the matrix version and the masking version it was written under, and carries no personal value | NFR-040; RWB-E1-039 BR3 | AC2 |
| BR9 | An access read that cannot be recorded is refused, never served, and the refusal is one 503 with MSG-P7-003 and no business payload | RWB-E1-039 BR2; Principle 5; R-UNI-39 | AC4, AC5 |
| BR10 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC1 |
| BR11 | The window, the incident pattern, the reason bounds and the review window are parameter rows behind the contract, never constants in it | DP-06; BR-P4-007 | AC3 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The four operations, the two schemas, the vocabulary and the fail-closed rule are described | In review |
| In review | Consumer sign-off | The app story, the gateway-bff route and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A parameter row changes | The window, the incident pattern or the reason bounds change | Baselined, with the bounds restated in the document |

The grant itself has the states ACTIVE and ENDED, and the entry the document describes is append only; both belong to the app story and are stated here only so that the answers carry them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the two schemas, the envelope and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Security administrator and the owner of the bank IAM integration | Review the two-person rule, the time box, the group check and the refusal vocabulary |
| Audit representative and the security architecture reviewer | Review the entry shape, the two version fields, the mask flag and the fail-closed rule |
| Tech lead of rwb-case (P3) | Reviews the parameters and reference-data operations as rwb-access uses them; owns their definitions |
| Data steward | Confirms that no personal data field is declared in an entry, an example or a fake |
| The ledger owner of rwb-decision (P7) | Confirms that the document names the DP-03 message and never the ledger's tables or its query |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Access entry | `decisionCode` from AC-SIGN, AC-DENY, AC-READ, AC-EXPT, AC-BGON and AC-VERS, `actorReference`, `caseReference` (optional), `documentReference` (optional), `capabilityArea`, `right`, `result`, `fields[]` of `fieldId` and `maskFlag` (`clear` or `masked`), `filter`, `rowCount`, `grantId` (optional), `incidentReference` (optional), `decidedAt`, `matrixVersion`, `maskingVersion` | Not specified in the source documents (DOR-RWB-P4-E1039-CON-7) |
| Access page | `items[]` of the entry, `page`, `size`, `total`, `matrixVersion`, `maskingVersion` | Not specified in the source documents (DOR-RWB-P4-E1039-CON-7) |
| Grant request | `incidentReference`, `iamRequestId`, `capabilityArea`, `right` (one of C, R, U), `scope`, `reason` (20 to 1000 characters) | Not specified in the source documents (DOR-RWB-P4-E1039-CON-7) |
| Grant answer | `grantId`, `incidentReference`, `capabilityArea`, `right`, `scope`, `startsAt`, `endsAt`, and the state ACTIVE or ENDED | Not specified in the source documents (DOR-RWB-P4-E1039-CON-7) |
| Query | `user`, `from`, `to`, `event`, `capabilityArea`, `page` (default 50), `size` (maximum 200) | Not specified in the source documents (DOR-RWB-P4-E1039-CON-7) |
| Refusal | `messageId` of the vocabulary of section 14, with the field list for a 422 and the trace id for every response | Not specified in the source documents (DOR-RWB-P4-E1039-CON-7) |

The entry carries the legacy field ids of the decision record — DF-DEC-002 for the case id, DF-DEC-003 for the decision code, DF-DEC-014 for the actions, DF-DEC-016 for the decided at and DF-DEC-030 for the actor — and it holds no field value, only the case id, the document id, the field id and the flag (NFR-040). The exact JSON names of the array elements, the sort order of a page and the full grant answer beyond the seven legacy fields are Not specified in the source documents (GAP-0781; ASM-1426). The end and read paths of a grant follow the base rule of DP-13 because no source names them, and the business message id of a 401 is not in the source (GAP-0781; ASM-1425).

The minimum content of the actions element is the legacy list: area, right, field IDs with the masking position, filter, row count, document ID, grant ID, incident reference and reason code. The three read elements of the decision-log read, grantId, incidentReference and reviewDueAt, are working names until the contract baseline of the service publishes them. AC-VERS is accepted as an access code and is mapped like the other five, with its subject not fixed. The legacy message identifiers are kept; their catalogue entry format is Not specified in the source documents (GAP-2452) and comes from the message catalogue owner. The parameter path is taken from the parameters contract of rwb-case.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/admin/access-log` | AccessLogPage: query `user`, `from` (required), `to` (required), `event`, `capabilityArea`, `page` (default 50), `size` (maximum 200); items of the entry of section 11 with `matrixVersion` and `maskingVersion` | Platform administration R, scope applied |
| POST | `/admin/break-glass-grants` | BreakGlassActivation in, BreakGlassGrant out with 201; `Idempotency-Key` required | Platform administration C, plus a verified IAM approval and group membership |
| POST | `/admin/break-glass-grants/{grantId}/end` | BreakGlassGrant out with its state ENDED and its end time; `Idempotency-Key` required | Platform administration C, or the requester of that grant |
| GET | `/admin/break-glass-grants/{grantId}` | BreakGlassGrant with its state ACTIVE or ENDED, `startsAt`, `endsAt` and the IAM request id | Platform administration R, scope applied |

Errors for the four: 401 the gateway-bff session envelope; 403 no right (MSG-P4-002) and no verified IAM approval or group membership on the grant operation (MSG-P4-007); 409 a grant is already active (MSG-GEN-004); 422 a required field empty (MSG-GEN-001), a bound violated (MSG-GEN-002) or a period that ends before it starts (MSG-GEN-003); 503 the entry cannot be written (MSG-P7-003). The two reads carry no idempotency rule and the document says so, so that no consumer sends the header. Major version 1 sits in the path; an additive field within version 1 is a compatible change (BR10). The end and read paths follow the base rule of DP-13 and the assumption in force (GAP-0781; ASM-1425).

The end and read operations are POST /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end and GET /api/recovery/access/v1/admin/break-glass-grants/{grantId}. The grant answer beyond grantId, incidentReference, capabilityArea, right, scope, startsAt and endsAt, and the name of its state field, are Not specified in the source documents (GAP-0781) and are to be confirmed with the security administrator. The legacy criteria call POST /admin/break-glass; that spelling is an alias of the published operation POST /admin/break-glass-grants and is not a second operation. The table name of the local decision record is Not specified in the source documents (GAP-0780). The keys of the actions element of an entry for a refusal and for an export, with their order, are Not specified in the source documents (GAP-0780) and are fixed in the contract before the endpoint is frozen. The fault point of a grant is the write of its local decision record (503, MSG-P7-003); the evidence location for the SIT run is Not specified in the source documents (GAP-0359) and is named at the integration pack review. The masking policy is keyed by view field ID: each field of an entry carries fieldId and maskFlag, and the request and response shape of the masking contract, including the names of the masked and clear source columns, is Not specified in the source documents (GAP-0694).

Access-log values (GAP-2332; GAP-2316). The access-event codes of a dashboard read and of a refusal, and the object-type code of the agent monitor with the list it belongs to, are Not specified in the source documents (GAP-2332; GAP-2316). The record code of an access event is taken from the DP-03 library code set at build time. The field list of an entry beyond the screen and the page bounds of the log read are Not specified in the source documents (GAP-2332; GAP-2316). The name of the read index on the record table is Not specified in the source documents (GAP-2332; GAP-2316) and is set in the physical schema of rwb_access. The Flyway step of this service is registered in its own sequence, and its parameter codes in its own parameter set; the accept date and the version number of that step are Not specified in the source documents (GAP-2332; GAP-2316).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles, the matrix and masking versions of the answer, and the break-glass state with the end time the document declares for the banner |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The window of 4 hours, the incident pattern, the reason minimum of 20 and the review window, with the version in force (DP-06); the window of 4 hours and the reason bounds of 20 to 1000 characters are placeholder values held as versioned parameters until the DL38 answer (GAP-1571) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION, LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE with the version in force (DP-07) |

None of the three is declared as provided by rwb-access, and no operation of `rwb-decision` — the `GET /decision-log` query above all — appears in the document as provided. The ledger is referenced by the entry it consumes and is never called by this service.

The grant ID and the incident reference of an active grant reach a consuming service on a document content read as a signed, short-lived claim in the session envelope that gateway-bff forwards; a missing or expired claim is no grant. The lifetime and the reuse bound of the claim are Not specified in the source documents (GAP-2339).

#### 12.3 Events published

None. This document declares no event: the entry of an access event is published by the DP-03 library as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, and the two policy events of the service, `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1`, belong to RWB-P4-E1037-APP and the delegation story. The message is named so that consumers recognise it, and its schema stays with RWB-PLT-E1027-CON.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and neither the access read nor the grant needs a subscription: the break-glass state comes from the session, and the policy comes from the authorise and permission operations.

#### 12.5 Workflows and activities

None. No workflow and no activity is part of this contract, and the `rwb-access` task queue carries the access review Schedule of RWB-P4-AD008-APP only.

#### 12.6 Schedules

None. All four operations are request-driven, and the review window of one working day is a parameter, not a Schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role code a grant extends and an entry states |
| `permission` | P4 (rwb_access) | The Platform administration letters and the matrix version |
| `masking_rule` | P4 (rwb_access) | The masking version an entry states |
| the local decision-record table of the DP-03 library (name Not specified in the source documents (GAP-0782)) | P4, in `rwb_access` | The entry the document describes; written by the app story through the library |
| `break_glass_grant` | P4, in `rwb_access` | The grant the document describes; created by RWB-P4-E1039-DB under the assumption in force (GAP-0781; ASM-1425); the two-person constraint is Not specified in the source documents (GAP-0782) |

No table of another service is named as this service's (DP-01): `decision_log_entry` and `approval` are P7 rwb_decision's, `lov_value` and the reference tables are P3's, and `document` is P5's. The case, document, image and incident references in an entry and in a grant are values, not foreign keys. The retention period and the partition granularity of the access log are parameter rows, not constants: the retention period is Not specified in the source documents (GAP-0782), and the expiry of a partition is a partition drop. The grantee login name is Not specified in the source documents (GAP-0782).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| authorise fake | Grant and refuse answers for RW-PLATADM, RW-SECADM, RW-AUDIT, RW-COE and RW-PHONECOL, with MSG-P4-002 on the refusal | App story, contract tests, harness |
| decision-record fake | A seeded chain with AC-READ, AC-DENY, AC-EXPT and AC-BGON entries, one grant entry with incident INC0004521, the append, the hash-link check and a forced failure | App story, contract tests |
| grant fake | An ACTIVE grant for incident INC0004521 and IAM request IAM-778812 ending at 14:30, an ENDED grant, a grant refused with MSG-P4-007, a second activation with MSG-GEN-004 and the end and read answers | App story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with window-hours 4, incident-pattern `^INC[0-9]{7}$`, reason-min 20 and review-days 1 | App story, contract tests |
| reference-data fake | `GET /admin/lists/{listCode}` for LOV-DECISION, LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE at version REF-2026.11 | App story, contract tests, harness |
| session fake | `GET /me/session` with the roles, the two versions and the break-glass state with its end time | Screen route, harness |
| gateway-bff fake | The composite route with the access-log panel, the grant panel and the MSG-P4-004 banner | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 | 3 | The access-log read, the grant activation, the grant end and the grant read provided; the session, parameters and reference-data reads consumed; one hop, 2 s timeout |
| Kafka | 0 | 0 | No event of this document; the DP-03 message is named, not declared |
| Temporal | 0 | 0 | No workflow, activity or Schedule |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-accesslog-v1.yaml` (OpenAPI 3.1) with the four operations and the shared components, `contract/error-envelope.yaml`, the `AccessLogEntry`, `AccessLogPage`, `BreakGlassActivation` and `BreakGlassGrant` schemas with their examples, the refused-event and grant vocabulary in the contract README, the paging and versioning rules, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The document names only `rwb_access` objects and the DP-03 entry | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. The document describes the entry and declares no event of its own | referred to; the consuming story carries the dependency H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. The window, the incident pattern and the reason bounds are parameter rows behind the document | referred to; the consuming story carries the dependency H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The event codes, the areas, the scopes and the roles arrive with their version | referred to; the consuming story carries the dependency H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The document is the mock's source and every consumed call is declared with its budget | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1`; the four operations sit under the service base and no other base appears | none |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. The document declares no lake read and no lake copy of the log | none; no lake data is needed |
| DP-19 | Screen, ace-web | gateway-bff composite route. The route consumes the access-log read and the session read, and the document fixes the access-log side of the merge | referred to; the consuming story carries the dependency H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses, the idempotency header and the shared components; schema lint in the pipeline.
2. The two schemas of the access log with the entry shape of section 11, the field list and the mask flag, and the page with the two version fields (AC2).
3. The two grant schemas and the four operations, with the two-person rule, `endsAt` as the earlier of the window and the group end, and the end enforced on every request (AC1, AC3).
4. The error envelope and the message-id mapping, with the business texts copied unchanged from the legacy story and the 401 left to the gateway-bff session envelope (AC4).
5. The fail-closed branch of each operation, with 503, MSG-P7-003 and no business payload (AC5).
6. The consumed session, parameters and reference-data operations with their owners, the one-hop rule and the 2 s client budget (AC6).
7. The seven fakes and their stub fixtures (AC7).
8. The seven contract tests, with a drift between a fake and the document failing the build, then the baseline tag and the consumer sign-off.

**Feature switch.** None of its own: the operations are switched by the service baseline of RWB-P4-E1037-CON and by the `rwb.access.access-log` parameter, and this document declares no 404 branch.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E1039-APP | The four provided operations, the two schemas, the vocabulary, the fail-closed rule and the seven fakes |
| RWB-PLT-N001-CON (gateway-bff, the SCR-43 panel and the banner) | The access-log read, the session read and the MSG-P4-004 banner state |
| RWB-ITG-E1039-ITG | The entry shape, the grant shape, the vocabulary and the fakes as the evidence it records |
| RWB-P7-E1039-APP | The decision-code list and the grant fields an entry carries, so that the ledger and the access log agree on what an access entry states |

**Done when.** The document validates in the pipeline, the seven contract tests pass, the seven fakes answer every declared path, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-004 | A break-glass grant is active for the caller; the banner shows the end time | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-007 | The grant operation is called with no approved IAM request or no verified group membership | Emergency access needs an approved break-glass request in the bank IAM with an open incident. |
| MSG-P4-002 | A read or a write without Platform administration in its right, or an action after the grant has ended | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is empty, or a code is not in its list | Enter {field}. |
| MSG-GEN-002 | The reason is shorter than 20 or longer than 1000 characters, or the page size is outside 1 to 500 | {field} must be between {min} and {max}. |
| MSG-GEN-003 | The period ends before it starts | {field} cannot be before {other}. |
| MSG-GEN-004 | A second activation while a grant is active | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The entry of a read or a grant cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message ids are contract elements and the text is the legacy text, copied unchanged. The refusal vocabulary is closed: an operation declares no message outside this table, and the business message id of an expired session is Not specified in the source documents (GAP-0781; ASM-1426), so a 401 carries the gateway-bff session envelope and no business id.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| The ACE front-end shell | Break-glass active | The session answer with the break-glass state and the end time, rendered as the MSG-P4-004 banner |
| SCR-43 Roles and access | Access log, list and filtered | The page with the entries, `matrixVersion` and `maskingVersion`, paged at 50 and at most 200, filtered by `user`, `from`, `to`, `event` and `capabilityArea` |
| SCR-43 Roles and access | Access log, empty | An empty `items` with total 0 and no error |
| SCR-43 Roles and access | Refused, no access | The 403 of the envelope with MSG-P4-002 and no list |
| SCR-43 Roles and access | Grant panel | The grant read with its state, `startsAt`, `endsAt` and the IAM request id, and the end operation |
| SCR-43 Roles and access | Grant refused | The 403 with MSG-P4-007, or the 422 with the field named, and no grant |
| SCR-43 Roles and access | Loading | Not specified in the source documents (CG-ALL-5040) |
| SCR-43 Roles and access | Error | Not specified in the source documents (CG-ALL-5040) |

The screens are served by the gateway-bff composite route (DP-19), which calls the access-log read, the grant read and the session read in parallel, one hop each, and merges the answers. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work; this document fixes the access-log and grant side of the merge only. The `matrixVersion` and `maskingVersion` of an access entry record the version the owning service applied at the time of the event; the registry in rwb-decision stays the source of each version and its effective date.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-039-CON-01 | AC1 | Contract | The document validates; the base, the four operations, the two rights and the error responses are present; no foreign operation is provided |
| TC-E1-039-CON-02 | AC2 | Contract | The entry and page schemas, the six decision codes, the field list with the mask flag, the optional case, document, grant and incident values, and no personal value in an example |
| TC-E1-039-CON-03 | AC3 | Contract | Incident INC0004521, IAM request IAM-778812, the reason bounds of 20 and 1000, `endsAt` at the earlier of 4 hours and the group end, the two-person rule, the end and read paths |
| TC-E1-039-CON-04 | AC4 | Contract | A 401, 403, 409, 422 and 503 response carry one envelope with a valid message id from the closed vocabulary |
| TC-E1-039-CON-05 | AC5 | Contract | The fail-closed branch of each operation: 503, MSG-P7-003, no page, no grant, no AC-BGON entry |
| TC-E1-039-CON-06 | AC6 | Contract | Three consumed operations with their owners P4 and P3, one hop and the 2 s budget; none declared as provided |
| TC-E1-039-CON-07 | AC7 | Component | The seven fakes match the document; a drifted fake fails the build; no name, e-mail address or personal field |
| TC-E1-039-CON-08 | §12.7 tables | Contract | The five tables of section 12.7 with their owners; the boundary of each contracted use; no table of another service named |
| TC-E1-039-CON-09 | AC8 | Contract | Each of BR1 to BR11 names a criterion of section 7 and each criterion names a test case of section 16; a rule without either fails the coverage check |
| TC-E1-039-CON-10 | AC9 | Contract | A request to an undeclared path and to an unknown grant id answers 404 in the one RFC 9457 envelope; the message id is Not specified in the source documents (NEWAC-RWB-P4-E1039-CON-AC12) |
| TC-E1-039-CON-11 | AC10 | Contract | A replayed grant and a replayed end with the same idempotency key create one grant or one end; the replay answer is Not specified in the source documents (NEWAC-RWB-P4-E1039-CON-AC13) |

No test in this story is an integration copy: the baseline is exercised against the fakes of section 12.8, never against a live service, and no `-ITG` variant belongs to it.

### 17. Guardrails

- No business value in the contract: the window, the incident pattern, the reason bounds, the review window, the event codes, the areas and the scopes stay parameter rows and reference data behind the document.
- No personal data in a schema, an example or a fake: references, codes, versions, field ids and flags only (BR8).
- The contract names only `rwb-access` objects and only operations owned by `rwb-access`; the ledger, the case, the document and the reference tables are consumed or absent, never named as this service's (DP-01, BR5).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- The two-person rule is verified and never granted by this service: the approval lives in the bank IAM and the contract states the check.
- A read that cannot be recorded is refused, and the refusal is the same 503 in the document, the fake and the implementation (BR9).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-006 | Every read is written to the access log, and the log is readable | The access-log read, the entry schema with the mask flag and the two version fields, and the fail-closed branch; the writer itself is RWB-P4-E1039-APP's | TC-E1-039-CON-01, TC-E1-039-CON-02, TC-E1-039-CON-05 |
| REQ-ACA-008 | Break-glass needs its own approval and writes to the access log | The grant, end and read operations, the two-person rule, the time box and the MSG-P4-007 refusal; the grant's implementation is RWB-P4-E1039-APP's | TC-E1-039-CON-03, TC-E1-039-CON-04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1039-APP | App development | The consumer and implementer of this baseline; owns the ten legacy criteria |
| RWB-P4-E1039-DB | ACE DB | X dependency tracked: the grant table and the chain this document describes, and the access-log table in rwb_access (append-only, read through GET /admin/access-log, which this document publishes) |
| RWB-P4-E1039-OPS | DevOps | X dependency tracked: the deployment of the operations and the alert routes of the vocabulary |
| RWB-P5-E1039-APP | App development | Neighbour of the same legacy key on the document side; writes the entry of a content read to this shape. A content read uses capability area DOCUMENTS, the legacy success result and lists no field ID until the reference data fixes the codes. |
| RWB-P7-E1039-APP | App development | Neighbour of the same legacy key on the ledger side; owns the central ledger and the query this document does not declare |
| RWB-ITG-E1039-ITG | Integration | The end-to-end proof that consumes this baseline |

The legacy test cases of this key — TC-E1-039-01, TC-E1-039-02, TC-E1-039-03, TC-E1-039-04, TC-E1-039-05, TC-E1-039-06, TC-E1-039-07, TC-E1-039-08, TC-E1-039-09, TC-E1-039-10, TC-E1-039-11 and TC-E1-039-12 — are executed by RWB-P4-E1039-APP and, as the cross-service copy, by RWB-ITG-E1039-ITG. No legacy test case is executed against this document, because the document is an artefact and not a behaviour.

### 19. Out of scope

- The implementation of the four operations, the writer, the grant and the read (RWB-P4-E1039-APP).
- The schema, the four tables, the grants and the retention of the log (RWB-P4-E1039-DB).
- The deployment, the topic ACLs, the secrets, the alerts and the run book (RWB-P4-E1039-OPS).
- The permission matrix and the masking policy (RWB-P4-E1037-APP); this document consumes their versions.
- The central ledger, the `GET /decision-log` query and the chain verification (P7 rwb-decision; RWB-P7-E1039-APP).
- The document content read and the entry it writes (P5 rwb-document; RWB-P5-E1039-APP).
- The screen SCR-43 Roles and access, its other panels and the composite route specification (RWB-PLT-N001-CON and the Epic 8 screen work).
- The access review list and its Schedule (RWB-P4-AD008-APP).
- The bank IAM integration that approves a break-glass request; this service verifies the approval and never issues it.
- The cross-service journey harness and its evidence (RWB-ITG-E1039-ITG).
