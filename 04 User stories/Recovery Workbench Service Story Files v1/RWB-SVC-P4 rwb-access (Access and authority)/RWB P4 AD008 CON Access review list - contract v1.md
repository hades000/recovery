# RWB-P4-AD008-CON Access review list

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD008-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-008 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the access recertification: an OpenAPI 3.1 document for the review read and the decision write, the `AccessReview`, `AccessReviewHolder` and `AccessReviewDecision` schemas with the holder page and the idempotent decision, the role-owner scoping rule, one RFC 9457 error envelope with its message IDs, the consumed authorise operation and the ACE Common removal path with their owner and one-hop budget, the contract tables of section 12 and the contract fakes**, so that **the app story, the operations story and the integration harness can build against a fixed, testable contract on Day 1 without waiting for `rwb-access` or the bank IAM to be built**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story produced a holder list with a Quartz job and read it on a screen of the monolith, and the removal of an unconfirmed holder was an e-mail to the bank IAM team. In the target `rwb-access` opens the cycle as a Temporal Schedule, answers the list from the Entra group mapping and posts the removal through the ACE Common path, so the screen, the harness and the operations story need a document that says exactly what the list is, what a decision is, who may see which role and what one removal request looks like.

If that field-level contract is agreed once and faked for the two operations, the authorise call and the removal path, the app story builds in parallel with the bank IAM work and a change in either side is caught in a contract test rather than in an integration window. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the document, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that serves SCR-43 and merges the review read with the access-log read of RWB-P4-AD007-APP.
- RWB-PLT-E1027-CON is published: the decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), whose entry is the access log of this capability.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners are taken from the ownership map only. `GET /admin/roles` and `GET /admin/access-log` are P4's and stay with their own stories; the two review operations have no row in that map, so their path, right and response are carried as this document's own decision and as an assumption (GAP-0806; ASM-1507).
- The workflow kit RWB-PLT-E1071-CON carries the Schedule and the two activities this document contracts (JOB-18); the kit is not in the app story's metadata build list and the absence is carried (GAP-0807; ASM-1508).
- The removal request goes through the ACE Common group membership path (INT-21) and its request and answer shapes are Not specified in the source documents (GAP-0808; ASM-1509).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the two review operations under the base `/api/recovery/access/v1`, with the shared components the sixteen `rwb-access` operations use.
2. Draft the schemas `AccessReview`, `AccessReviewHolder`, `AccessReviewDecision` and the holder page, with the decision states of an item and no property that could carry a person's name.
3. State the role-owner scoping rule in the document: the owner of a role is the holder of the A letter in Platform administration for that role, and the answer returns only the roles the caller owns.
4. Agree the error envelope and the message mapping for 401, 403, 404, 409, 422 and 503, with the business texts copied unchanged from the legacy story.
5. State the idempotency rule of the decision write: the same `Idempotency-Key` returns the first answer and writes no second entry; a different key on a decided item is 409.
6. State the consumed authorise operation and the ACE Common removal path with their owner and the 2 s one-hop budget.
7. State the Schedule `access-review`, the workflow `AccessReviewWorkflow` and the two activities as contract elements on queue `rwb-access`.
8. Publish the contract tables of section 12 (nine sub-tables) and the contract fakes.
9. Add the contract tests: schema validation, the paging rule, the idempotency rule, the envelope, the owner declarations and the drift between a fake and the document.
10. Tag the baseline and hand it to RWB-P4-AD008-APP, the operations story of this legacy key and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A response schema declares a holder name, an e-mail address or an identity number | The review fails and the property is removed; the rule is a lint item of the document | None | AC3 |
| X3 | A field of the review entry has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |
| X4 | An error response carries no `messageId`, or a `messageId` not in the agreed set | The contract test fails and the merge is blocked | None | AC4 |
| X5 | The document declares an operation of another service as provided | The review fails; the operation is documented as consumed | None | AC5 |
| X6 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X7 | A consumed operation does not answer inside the 2 s budget | The call answers 503 for that operation and the document declares the 503 | MSG-P7-003 | AC5 |
| X8 | The ACE Common path answers no request reference | The document declares the failure, and the app story keeps the item open with its task and its incident | MSG-GEN-004 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; it reads the ownership map, the platform envelopes, the authorise contract of RWB-P4-E1037-CON and the ACE path only |
| Negotiable | The field-level detail of the review, the holder page and the decision is settled with the security administrator and the harness; the operations, the base, the topics, the schedule and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the operations story and the wave 4 harness on Day 1, and keeps the case tables and the central ledger out of the contract |
| Estimable | One document, four schemas, one error envelope with five message IDs, nine contract tables, three fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Access review contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the recertification half of legacy RWB-AD-008 is the review read and the decision write

  Scenario: AC1 The OpenAPI 3.1 document describes the two review operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares GET /admin/access-reviews/{reviewId} and POST /admin/access-reviews/{reviewId}/decisions with the owner rwb-access
    Then both operations declare Platform administration with the right R, and the decision write declares the A letter in Platform administration for the role
    Then every operation names its error responses 401, 403, 404, 409, 422 and 503

  Scenario: AC2 The review, the holder page and the decision are schemas of the document (new, D-RCV-60)
    Given the schemas AccessReview, AccessReviewHolder and AccessReviewDecision of the document
    Then AccessReview carries reviewId, cycleCode, openedOn, closesOn, state and the roles with their holder page
    Then AccessReviewHolder carries holderUserReference, decisionState, decidedAt, reasonCode and removalRequestRef
    Then AccessReviewDecision carries roleCode, holderUserReference, decision, reasonCode, reason and the Idempotency-Key header
    Then the holder page carries items, page, size and total with a default of 50 and a maximum of 200
    Then the decision write declares the same key returning the stored answer and a different key on a decided item answering 409

  Scenario: AC3 The role-owner scoping rule is declared and no holder name is a property (new, D-RCV-60)
    Given the description of the review read and of the decision write
    Then the document states that a role owner sees only the roles in which the caller holds the A letter in Platform administration, and RW-COE for the reference-data roles
    Then the document states that a caller who owns no role in the review is refused with 403
    Then no schema, no parameter and no example declares a holder name, an e-mail address or an identity number
    Then the entry property of a holder is the staff user reference and the decision state only

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by either operation
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002, 422 carries MSG-GEN-001 and 409 carries MSG-GEN-004
    Then 503 carries MSG-P7-003 and names the record that could not be written
    Then the response carries the problem media type and the trace identifier

  Scenario: AC5 The consumed authorise operation and the ACE removal path are declared as consumed (new, D-RCV-60)
    Given the authorise operation of rwb-access and the ACE Common group membership path
    Then POST /api/recovery/access/v1/authorise is declared in the consumed section with the owner rwb-access and the right Platform administration R
    Then the removal request is declared with the owner ACE Common and the INT-21 reference
    Then both are declared one hop, with the 2 s client budget and the 503 when the call does not answer in time
    Then no operation owned by another service is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the three contract fakes of section 12.8
    When a fake is compared with the document
    Then the review fake answers the paths and payloads of 12.1 with review "AR-2027-H1" opened on 4 January 2027 with 12 role owners and their holders
    Then the removal fake answers request "IAM-REM-0007" accepted for holder "U-4105" and one refused request
    Then a contract test fails on any drift between a fake and the document
    Then no schema, example or fake carries a name or an e-mail address
```

These six criteria test the artefact only. No criterion restates a legacy acceptance criterion; the two legacy criteria and the three new behaviour criteria of RWB-AD-008 belong to RWB-P4-AD008-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's path | DP-13; Architecture v5 slides 14 and 41 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 |
| BR3 | Events are named `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, and the shared record type stays on `rwb.decision-record.v1`, with the CloudEvents 1.0 envelope | DP-03; Template and Rules §R4 |
| BR4 | The contract declares no table of another service: `assignment` is P3's and `decision_log_entry` is P7's, and neither is contracted here | DP-01 |
| BR5 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR6 | The holder entry is a staff user reference and a decision state; no property of the document may carry a name, an e-mail address or an identity number | REQ-ACA-005; Guardrails |
| BR7 | The decision write is idempotent by `Idempotency-Key`; a different key on a decided item is 409 and never overwrites the first decision | R-UNI-40; Architecture v5 slide 11 |
| BR8 | The document states the role-owner rule, so no consumer builds its own scoping: the A letter in Platform administration for the role, and RW-COE for the reference-data roles | GAP-0809; ASM-1510; TSD P4 v3 T6.1 |
| BR9 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the four schemas, the envelope and the consumed path are described | In review |
| In review | Consumer sign-off | The app story, the operations story and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-access` | Owns the document, the four schemas, the activity contract and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Security administrator and the audit representative | Review and sign off the holder entry, the scoping rule and the decision states |
| Tech lead of the ACE Common integration | Reviews the removal path, its request and answer shape and the INT-21 reference |
| Data steward | Confirms that no personal data property is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Review resource | `reviewId`, `cycleCode`, `openedOn`, `closesOn`, `state` (OPEN, CLOSED), `roles[]`; from `access_review`, whose field IDs are Not specified in the source documents (GAP-0806; ASM-1507) |
| Review role | `roleCode`, `roleName`, the holder page and the role's conflict list; from `role` DF-REF-034 to DF-REF-039 and `role_conflict` DF-REF-205 to DF-REF-211 |
| Holder page | `items[]` of `holderUserReference`, `decisionState` (PENDING, CONFIRMED, REMOVED, REMOVAL_REQUESTED), `decidedAt`, `reasonCode`, `removalRequestRef`; `page`, `size`, `total`; from `access_review_item`, whose field IDs are Not specified in the source documents (GAP-0806; ASM-1507) |
| Decision request | `roleCode`, `holderUserReference`, `decision` (CONFIRM, REMOVE), `reasonCode`, `reason`, and the `Idempotency-Key` header |
| Decision answer | `reviewId`, `roleCode`, `holderUserReference`, `decision`, `decidedAt`, `decisionRecordEntryRef`, `removalRequestRef` |
| Removal request | The holder reference, the role code and the group of the role, sent to the ACE Common path; the request and answer shapes are Not specified in the source documents (GAP-0808; ASM-1509) |
| Event payloads | IDs, role codes, counts and times only; no name, no e-mail address, no identity number and no staff user reference |

The exact field-level schema of the review, of the holder page and of the decision — types, lengths, required flags and the sort parameters — is this baseline's decision and is fixed by the document; the sources define no field list for the two operations (GAP-0806; ASM-1507).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/admin/access-reviews/{reviewId}` | `AccessReview`: path `reviewId`; query `roleCode`, `state`, `page`, `size` (default 50, max 200); roles with their holder page | Platform administration R, then the A letter in Platform administration for each role returned |
| POST | `/admin/access-reviews/{reviewId}/decisions` | `AccessReviewDecision` in, with the `Idempotency-Key` header; the decision record out | Platform administration R, and the A letter in Platform administration for that role |

Errors for both: 401 no session (MSG-P4-001), 403 no right, no ownership, or the holder's own confirmation (MSG-P4-002), 404 unknown review, role or holder (envelope), 409 item decided or review closed (MSG-GEN-004), 422 missing or invalid field (MSG-GEN-001), 503 record not written (MSG-P7-003). The GET is a read, so the `Idempotency-Key` rule does not apply to it and the baseline states it so that no consumer sends the header. Major version 1 sits in the path (BR9).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access`, published by RWB-P4-E1037-CON | Platform administration R and the caller's A letter per role, behind both operations |
| POST | ACE Common group membership removal (INT-21) | ACE Common, the bank IAM entry point on the sign-in and group-to-role path | One removal request per unconfirmed holder at the close; the answer says whether the request was accepted and carries the request reference |

Neither is declared as provided by `rwb-access`, and the ACE path is an external system interface rather than a service operation. The `rwb-case` parameters and reference-data contracts are not declared: this capability has no parameter row and no list of values.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | Review id, role codes, the counts of confirmed and removed holders and the change kind; no holder reference |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library; consumed by P7 | Entry id, decision code, the review and the decision, the reason code and the time; the access log of the capability |

Both messages use the CloudEvents 1.0 envelope with the attributes id, source, type, specversion, time, subject and datacontenttype. No message carries a name, an e-mail address, an identity number or a staff user reference. `rwb.access.DoaLimitChanged.v1` is not declared for this capability.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this capability adds no subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AccessReviewWorkflow` | Workflow, workflow ID = review id | `rwb-access` | Input business date and cycle; the open, the build and the close; search attributes ReviewId and CycleCode |
| `BuildReviewList` | Activity (workflow kit) | `rwb-access` | The roles, the group read through `v_ace_iam_group` and the one item per holder per role; the count of an unread group |
| `RequestRemoval` | Activity (workflow kit) | `rwb-access` | One removal request per unconfirmed holder and one entry per request; the declared failure leaves the item open with its task |

#### 12.6 Schedules

| Schedule | Cron | Overlap policy | Contract element |
|---|---|---|---|
| `access-review` | Six-monthly, Asia/Bangkok (DL38 placeholder value until SCB IT security supplies the bank IAM standard value) | SKIP, with the kit's catch-up window | Schedule ID `access-review`, workflow `AccessReviewWorkflow`, queue `rwb-access` in namespace `rwb-recovery`, the business date as input, and the pause, resume and backfill operations of the kit. Legacy JOB-18 |

The exact month, day and hour of the cron are the deployment's configuration and are Not specified in the source documents (GAP-0807; ASM-1508). This is the only Schedule of the service (Architecture v5 slide 14), and it runs on RWB-PLT-E1071-CON.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (`rwb_access`) | The role code, the role name and the `entra_group` behind the holder list |
| `permission` | P4 (`rwb_access`) | The A letter in Platform administration that makes a caller a role owner |
| `role_conflict` | P4 (`rwb_access`) | The pair of roles one person may not hold together, listed to the role owner |
| `access_review` | P4 (`rwb_access`) | The review resource; new, created by RWB-P4-AD008-APP (GAP-0806; ASM-1507) |
| `access_review_item` | P4 (`rwb_access`) | The holder page and the decision; new, created by RWB-P4-AD008-APP (GAP-0806; ASM-1507) |

`assignment` of P3, `decision_log_entry` of P7 and `partner_user` of S9 appear nowhere in the contract (DP-01). `v_ace_iam_group` is the service's own granted read-only view and supplies the membership behind the list; it is not another service's table.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `rwb-access` access-review WireMock | Both paths of 12.1: review "AR-2027-H1" opened on 4 January 2027 with 12 role owners and their holders; review "AR-2027-H2" for the Schedule run of 7 July 2027; a holder page of role "RW-CASEOWN" with page, size and total; the stored answer for a repeated `Idempotency-Key`; 409 for a decided item with a new key; 403 with MSG-P4-002 for a role the caller does not own and for a self-confirmation; 422 with MSG-GEN-001 for a missing reason | App story, contract tests, wave 4 harness |
| Removal fake for the ACE Common path | Removal request "IAM-REM-0007" accepted for holder "U-4105" with its request reference, and one request refused with the failure the contract declares | App story, contract tests, wave 4 harness |
| Decision-record fake | The entry append, the hash-chain check and the 503 with MSG-P7-003 when the entry cannot be written | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The review read and the decision write provided; the authorise operation and the ACE Common removal path consumed; one hop, 2 s timeout |
| Kafka | 2 published, 0 consumed | `rwb.access.AccessPolicyChanged.v1` and `rwb.decision-record.DecisionRecorded.v1` |
| Temporal | 1 workflow, 2 activities, 1 Schedule | `AccessReviewWorkflow`, `BuildReviewList`, `RequestRemoval`, the `access-review` Schedule |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-access-review-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, the four schemas, the `contract/error-envelope.yaml` with the agreed message IDs, the activity contract for `AccessReviewWorkflow`, `BuildReviewList` and `RequestRemoval`, the removal path stub with its INT-21 reference, and the three WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is contracted as the entry the document declares on `rwb.decision-record.v1`; DP-05 as the statement that the membership is read through the service's own `v_ace_iam_group` and never through a table of ACE; DP-13 as the base of the document; DP-19 as the composite route that serves SCR-43. DP-10 (Quartz, JOB-nn → a Temporal Schedule through the workflow kit) is carried by the legacy key and is not in this story's pattern row: the Schedule is contracted here and it needs RWB-PLT-E1071-CON, which the app story's metadata build list does not carry (GAP-0807; ASM-1508).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The two operations and the four schemas of section 11, with the decision states and the holder page.
3. The role-owner scoping rule in the description of both operations and the 403 it produces.
4. The error envelope and the message-ID mapping, with the business texts copied unchanged from the legacy story.
5. The consumed authorise operation and the ACE removal path with their owners, the one-hop rule and the 2 s budget.
6. The activity contract and the `access-review` Schedule element with its cadence, overlap policy and catch-up window.
7. The three fakes and the stub fixtures of section 12.8.
8. The six contract tests; a drift between a fake and the document fails the build.
9. Baseline tag and the consumer sign-off note from the app story, the operations story and the wave 4 harness.

**Feature switch.** The contract carries no switch. The review read and the decision write are operations of the service; the operational control is the pause and resume of the `access-review` Schedule, which the contract declares as a kit operation and which never closes an open review.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD008-APP | The two provided operations, the four schemas, the scoping rule and the three fakes |
| The operations story of this legacy key | The `access-review` Schedule element, its cadence and the two activities |
| The wave 4 harness | The fakes of 12.8 and the removal path stub |

The deprecation window of a published field and the retention of the contract fakes are Not specified in the source documents (GAP-0806; ASM-1507).

**Done when.** The OpenAPI document validates in the pipeline, the six contract tests pass, the three fakes answer every consumed path and every provided path, and the app story, the operations story and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session, or a caller with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without Platform administration R, a review the caller does not own, or the holder's own confirmation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is empty or malformed | Enter {field}. |
| MSG-GEN-004 | The item is already decided under another key, or the review is closed | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The decision-record entry could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. MSG-GEN-004 and MSG-P7-003 are answered by `rwb-access` under this contract and are declared here as mapped responses.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-43 Roles and access | Open review | The review resource with its dates and the roles the caller owns, each with its holder page |
| SCR-43 Roles and access | Decided | The decision answer and the holder page, with the decision state, the reason code and the request reference |
| SCR-43 Roles and access | Closed | The review with state CLOSED, and the 409 of a further decision |
| SCR-43 Roles and access | Access log | The entry of the decision record, read through the access-log operation of RWB-P4-AD007-APP on the same composite route |
| SCR-43 Roles and access | Refused | The 403 with MSG-P4-002 and no role and no holder |
| SCR-43 Roles and access | Not available | The 503 with MSG-P7-003 |

The screens are served by the gateway-bff composite route (DP-19), which calls the review read and the access-log read in parallel, one hop each, and merges the answers. The composite route specification, the screen field list and the column order are Not specified in the source documents (GAP-0806; ASM-1507); the document fixes the review side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-008-CON-01 | AC1 | Contract | The OpenAPI 3.1 document validates; the base, the two operations, the rights and the six error responses are present |
| TC-AD-008-CON-02 | AC2 | Contract | The four schemas, the decision states, the holder page with default 50 and maximum 200, and the idempotency rule of the decision |
| TC-AD-008-CON-03 | AC3 | Contract | The scoping rule is declared and no schema, parameter or example holds a name, an e-mail address or an identity number |
| TC-AD-008-CON-04 | AC4 | Contract | 401, 403, 404, 409, 422 and 503 carry one envelope and a valid message ID |
| TC-AD-008-CON-05 | AC5 | Contract | The authorise operation and the ACE removal path with their owner, one hop, the 2 s budget and the 503; no foreign operation is declared as provided |
| TC-AD-008-CON-06 | AC6 | Component | The three fakes match the document, a drifted fake fails the build, and no fake carries a name or an e-mail address |

### 17. Guardrails

- No business value in the contract: the interval is the Schedule's configuration under DL38, the reason codes are enumerated values, and the role owners are rows of `permission`; none of them is fixed by the document.
- No personal data in a schema, an example or a fake: the holder entry is a staff user reference and a decision state, and a name or an e-mail address in the document fails the review (BR6).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the authorise operation and the ACE path are documented as consumed (DP-01, BR2).
- One REST base and one topic per service, and the shared record type on `rwb.decision-record.v1`; a document that names another service's base or topic fails the review (DP-13, BR3).
- Every example is synthetic; no production payload is copied into a schema or a fake.
- A decision is idempotent and never overwrites: the document declares the replay and the 409, so no consumer treats a second click as a new decision (BR7).
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-002 | Roles are held as data and a role change takes effect without a code release | The review resource and its role list read from `role` and `permission`; the holder list read from the group mapping through the service's own view | TC-AD-008-CON-01, TC-AD-008-CON-02 |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench | The holder entry as a staff user reference and a decision state; the removal request on the ACE Common path at the close | TC-AD-008-CON-05, TC-AD-008-CON-06 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation | The two operations and the SCR-43 states they feed through the composite route | TC-AD-008-CON-03, TC-AD-008-CON-04 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy AC1 "List produced" and AC2 "Not confirmed" | The behaviour of RWB-P4-AD008-APP; this contract carries the elements they are tested against |
| The permission check Platform administration R | Section 12.1, section 8 |
| MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-GEN-004, MSG-P7-003 | Section 14, exception paths |
| Screens SCR-43 and SCR-41 | Section 15 |
| JOB-18 six-monthly and DL38 | Section 12.6 |
| Field IDs DF-REF-034 to DF-REF-039, DF-REF-040 to DF-REF-044, DF-REF-205 to DF-REF-211, DF-ACE-301 to DF-ACE-304 | Section 11 |

### 19. Out of scope

- The implementation of the review read, the decision write, the Schedule, the list build and the removal request (RWB-P4-AD008-APP).
- The roles read and the access-log read of this service (the role administration of legacy RWB-AD-001 and RWB-P4-AD007-APP); the composite route serves them but this contract does not define them.
- The break-glass grant and its activation (legacy RWB-AD-006); the contract carries MSG-P4-004 only as the warning of an answer.
- The case task, the case state and the central decision ledger: `assignment` is P3's and `decision_log_entry` is P7's, and they appear nowhere in the contract.
- The deployment of the capability: the Helm values, the Schedule creation, the topics, the dashboards and the runbook.
- The operations of the ACE Common path beyond the removal request this capability posts; the bank IAM owns its own contract.
- The integration harness and its evidence.
- The field-level completeness of the review resource and of the holder page beyond what section 11 fixes (GAP-0806; ASM-1507).
