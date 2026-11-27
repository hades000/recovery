# RWB-P4-E8008-CON Move an approval limit

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8008-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement |
| Contract version | 1 (path `/api/recovery/access/v1`; major version 1 per section 12.1) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-008 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P4-E8008-CON-L206). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 9 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Tribe lead and squad members (RW-TRIBE)**, I want **the published contract baseline of the limit move of `rwb-access`: an OpenAPI 3.1 document for the two writes, the `DoaLimitMove` and `DoaLimit` schemas with the field names of the delegation table, the state set of a moved row, the `rwb.access.DoaLimitChanged.v1` declaration on `rwb.access.events.v1` in AsyncAPI, one RFC 9457 error envelope with its message IDs, the consumed authorise and parameters operations with their owners, one hop and the 2 s budget, the contract tables of section 12 and the contract fakes**, so that **the app story, the screen route and any consumer of a limit change can build against a fixed, testable contract on Day 1 without waiting for `rwb-access`, `rwb-case` or the DoA version load to be built**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-008 belong to RWB-P4-E8008-APP, and the six criteria of section 7 test the document, the schemas and the state set, the change event, the envelope, the consumed declarations and the fakes.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story changed a delegated limit through a screen of the monolith, where the shape of the change, the version that carried it and the record that evidenced it were whatever the screen happened to write. In the target the limit is a row of `rwb-access`'s own schema, the change is a new row version in a state set, and the change is announced on the service's own topic so that a permission or limit cache elsewhere can be refreshed without a rebuild.

The Temporal and Drools design states the discipline the contract has to express: delegation limits are held as versioned reference data and follow the same approve-and-date discipline as the Drools packages, and every answer of the delegation lookup shows which version made it. A contract that does not fix the states, the date fields, the event name and the payload leaves the app story, the consent of the Risk approver and any subscriber to guess; and a contract that leaks the holder and the substitute into the event publishes the person references of the delegation table to every subscriber that does not need them.

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with the parameters contract of `rwb-case`, the local decision-record library and the whole-version DoA load, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with the event name `rwb.access.DoaLimitChanged.v1`, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that calls the two writes behind SCR-41 Delegation of authority, and it is a consumer of this baseline.
- RWB-P4-E1038-APP is the owner of `delegation_limit`, of its migration and of the whole-version load; this document describes rows of that table as TSD P4 v3 T3.1 publishes them and adds no column.
- The platform error envelope, the CloudEvents 1.0 envelope and the AsyncAPI conventions are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners are taken from the ownership map only: the two writes are P4's, and the authorise and parameters operations this document consumes are P4's and P3's. No table of another service is named (DP-01).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the two writes with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the error responses and the two schemas.
2. Fix the `DoaLimitMove` request schema and the `DoaLimit` answer schema with the field names of TSD P4 v3 T3.1 (DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062) and the standard record columns of T3.0 where they are answerable.
3. Fix the state set of a moved row — `PENDING_APPROVAL`, `IN_FORCE`, `SUPERSEDED` — and the transition each operation may cause, so that no consumer can read two limits in force for one date.
4. Declare `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1` in AsyncAPI, with its payload and its key, and state in the same element that the payload carries no holder, no substitute, no name and no personal field.
5. Agree the error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, with the business texts taken from the legacy story where the message already existed and MSG-P7-002 carried as a message ID only.
6. Declare the consumed authorise and parameters operations as consumed, each with its owner, one hop and the 2 s client budget; declare the delegation lookup and the whole-version load as not provided here.
7. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes.
8. Add the contract tests: schema validation, the two schemas' field names, the state set and the event, the envelope and message IDs, the consumed declarations and drift detection between a fake and the document.
9. Tag the baseline and hand it to RWB-P4-E8008-APP, the Epic 8 screen work of RWB-PLT-N001-CON and the harness of the wave 4 access journey.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner, or declares the delegation lookup as provided here | The review refuses the document; the lookup stays RWB-P4-E2013-APP's | None | AC1, AC5 |
| X3 | A response of 401, 403, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A field of a schema is not one of the TSD field names, or a required field is optional | The contract test fails | None | AC2 |
| X5 | A state outside `PENDING_APPROVAL`, `IN_FORCE` and `SUPERSEDED` is declared for a moved row, or a transition that would leave two rows in force | The review refuses the document | None | AC3 |
| X6 | The event payload carries a holder reference, a substitute reference or a personal field, or the event name or topic deviates from the naming rule | The contract test fails and the review refuses the document | None | AC3, AC6 |
| X7 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X8 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X9 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the TSD field names, the DP-03 record schema and the P3 and P4 contracts only |
| Negotiable | The two paths and the field names are confirmed with Risk and the screen route; the base, the event name, the topic and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the SCR-41 route and the harness on Day 1, and keeps the holder references out of the event |
| Estimable | One OpenAPI document, one AsyncAPI element, one error envelope, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Move an approval limit contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the limit-move half of the legacy journey is one row versioned by a move and put in force by an approval

  Scenario: AC1 The OpenAPI 3.1 document describes the two writes (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the limit move is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares PATCH /doa-limits/{delegationLimitId} and POST /doa-limits/{delegationLimitId}/approve with the owner rwb-access
    Then the move names Rules and parameters U and the approval names Rules and parameters A
    Then both name their error responses 401, 403, 409, 422 and 503 and both require an Idempotency-Key
    Then GET /doa-limits is not declared as provided here and the whole-version load appears in no path

  Scenario: AC2 The move and limit schemas carry the delegation field names (new, D-RCV-60)
    Given the DoaLimitMove and DoaLimit schemas of the document
    When the schemas are compared with the TSD P4 v3 T3.1 field names and the DF-REF map
    Then DoaLimitMove carries principalLimit, lossPctLimit, minPricePctFmv, maxLossAmount, validFrom, reason and version
    Then DoaLimit carries delegationLimitId, moveId, limitVersion, state, decisionCode, approvalLevel, productGroup, regulationItem, principalLimit, lossPctLimit, minPricePctFmv, maxLossAmount, validFrom, validTo, holderReference, substituteReference, version, approverRole, approvedByRole and approvedAt
    Then every field maps to DF-REF-016 to DF-REF-026 or DF-REF-055 to DF-REF-062, or to a standard record column of TSD P4 v3 T3.0
    Then validFrom and reason are required on the move and no state or limit_version is accepted from the caller
    Then the move answers 200 with state "PENDING_APPROVAL" and approverRole "RW-RISK"

  Scenario: AC3 The state set and the change event are fixed (new, D-RCV-60)
    Given the state set of a moved row in the document
    When a move, an approval and a supersede write a row
    Then state is one of PENDING_APPROVAL, IN_FORCE and SUPERSEDED
    Then a move writes PENDING_APPROVAL and an approval writes IN_FORCE for the moved row and SUPERSEDED for the row it replaces
    Then the AsyncAPI document declares rwb.access.DoaLimitChanged.v1 on the topic rwb.access.events.v1 with the key delegationLimitId
    Then its payload is delegationLimitId, limitVersion, decisionCode, approvalLevel, productGroup, effectiveFrom and reason and nothing else
    Then the payload declares no holder reference, no substitute reference and no personal field
    Then no workflow and no Schedule is declared for the capability

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 409, 422 or 503 response is produced by either write
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002 on an absent right and MSG-P7-002 on an approval by the author
    Then 409 carries MSG-GEN-004, 422 carries MSG-GEN-001 and 503 carries MSG-P7-003
    Then no operation declares a second error shape

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation and the parameters read this service calls
    When the document declares its consumed and provided operations
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then GET /api/recovery/access/v1/doa-limits and the whole-version load of a DoA version are declared as neither provided nor consumed here
    Then no operation owned by rwb-decision or by rwb-case is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of the baseline
    When they are run against the document and against the AsyncAPI element
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then no schema, example, fake or event payload carries a name, an e-mail address or a personal field, and none carries a holder or substitute reference in the event

  Scenario: AC7 The contract names only the tables this service owns (new, D-RCV-60)
    Given the owned tables of section 12.7
    When the tables named in the contract are compared with the owner column
    Then every named table is owned by P4 rwb_access
    Then no table of another service is named in the contract

  Scenario: AC8 A replayed write answers the first answer and publishes no second event (new, D-RCV-60)
    Given a write of a limit move with an Idempotency-Key already answered
    When the same Idempotency-Key is sent again
    Then the first answer is returned unchanged
    Then no second DoaLimitChanged event is published and no second record entry is written

  Scenario: AC9 A schema change within version 1 is additive (new, D-RCV-60)
    Given the schemas of the document at major version 1
    When a schema of the document is changed
    Then an additive change stays in major version 1
    Then a removed, renamed or retyped field is declared as a new major version

  Scenario: AC10 A provided operation answers 404 with the problem envelope when the resource is not found (new, D-RCV-60)
    Given the provided operations of the document
    When a request names a delegation limit or a path the service does not hold
    Then the answer is 404 and the body is the one RFC 9457 problem response of AC4
    Then no provided operation answers 404 with a second error shape

  Scenario: AC11 A status change the state model does not allow is refused (new, D-RCV-60)
    Given a moved row in state SUPERSEDED
    When an approval is written for that row
    Then the write is refused with 409 and the problem response of AC4 carrying MSG-GEN-004
    Then no row changes state and no DoaLimitChanged event is published
```

These six criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-008 belong to RWB-P4-E8008-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1, AC5; TC-E8-008-CON-01, TC-E8-008-CON-05 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5; TC-E8-008-CON-05 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are taken from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC4; TC-E8-008-CON-04 |
| BR4 | The schemas carry the field names of TSD P4 v3 T3.1 and the standard record columns of T3.0, and add no field of another service | TSD P4 v3 T3.0, T3.1; DP-01 | AC2; TC-E8-008-CON-02 |
| BR5 | The state set of a moved row is `PENDING_APPROVAL`, `IN_FORCE` and `SUPERSEDED`, and no transition declared in the document leaves two rows in force for one date | FSD P4 v3 A2.6.4.2; ASM-1574, ASM-1575 | AC3; TC-E8-008-CON-03 |
| BR6 | The change event is `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1`, keyed by the limit, with the payload of section 12.3 | Architecture v5 slide 14 and slide 41; ASM-1576 | AC3; TC-E8-008-CON-03 |
| BR7 | The event and every example carry no holder reference, no substitute reference, no name and no personal field | NFR-040; ASM-1576 | AC3, AC6; TC-E8-008-CON-03, TC-E8-008-CON-06 |
| BR8 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC9; TC-E8-008-CON-09 |
| BR9 | A write requires an `Idempotency-Key`; a replay answers the first answer and publishes no second event | Architecture v5 slide 42; DP-09 | AC1, AC8; TC-E8-008-CON-01, TC-E8-008-CON-08 |
| BR10 | The contract declares no workflow, no activity and no Schedule for the capability | Architecture v5 slide 14; TSD P4 v3 T5.3 | AC3; TC-E8-008-CON-03 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two writes, the two schemas, the state set, the event and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the SCR-41 route and the harness accept the document, the event and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or the event payload changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A consumed operation changes | The parameters read or its version handling changes | Baselined, with the client budget and the stub restated |

The state set the document fixes for a moved row is `PENDING_APPROVAL`, `IN_FORCE` and `SUPERSEDED`, with the transition of BR5; the lifecycle of a whole DoA version (loaded, approved, in force, rolled back) is the contract of RWB-P4-E1038-APP and is not restated here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the two schemas, the state set, the event declaration and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Risk and model risk officer, as the approver of every move | Reviews the approval operation, the four-eyes message ID and the effective-date fields |
| Center of excellence analyst, as the author of every move | Reviews the move operation and the fields the screen sends |
| Tech lead of rwb-case (P3) | Reviews the parameters operation as rwb-access uses it; owns its definition |
| Tech lead of rwb-access with RWB-P4-E1038-APP and RWB-P4-E2013-APP | Confirms that the load of a version and the delegation lookup stay out of this document |
| Data steward | Confirms that no holder reference, substitute reference or personal field is declared in the event, the examples or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| `DoaLimitMove` | `principalLimit`, `lossPctLimit`, `minPricePctFmv`, `maxLossAmount`, `validFrom` (required), `reason` (required), `version` (the optimistic lock of the row read) | DF-REF-020, DF-REF-021, DF-REF-022, DF-REF-058, DF-REF-025 for the four amounts and `validFrom`; `reason`: Not specified in the source documents (DOR-RWB-P4-E8008-CON-7); `version`: TSD P4 v3 T3.0 |
| `DoaLimit` | `delegationLimitId` DF-REF-016, `moveId`, `limitVersion` DF-REF-055, `state` (T3.0), `decisionCode` DF-REF-017, `approvalLevel` DF-REF-018, `productGroup` DF-REF-019, `regulationItem` DF-REF-056, `principalLimit` DF-REF-020, `lossPctLimit` DF-REF-021, `minPricePctFmv` DF-REF-022, `maxLossAmount` DF-REF-058, `validFrom` DF-REF-025, `validTo` DF-REF-026, `holderReference` DF-REF-023, `substituteReference` DF-REF-024, `version` (T3.0), `approverRole`, `approvedByRole`, `approvedAt` | The DF-REF of each field named in the row (DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-058); `state`, `version`: TSD P4 v3 T3.0; `moveId`, `approverRole`, `approvedByRole`, `approvedAt`: Not specified in the source documents (DOR-RWB-P4-E8008-CON-7) |
| State set | `PENDING_APPROVAL`, `IN_FORCE`, `SUPERSEDED` in the `state` column of TSD P4 v3 T3.0 | None (no DF-REF); the `state` column of TSD P4 v3 T3.0 is the field |
| Change event | `rwb.access.DoaLimitChanged.v1` with `delegationLimitId`, `limitVersion`, `decisionCode`, `approvalLevel`, `productGroup`, `effectiveFrom`, `reason`; no holder, no substitute, no personal data | None (no DF-REF); field names fixed by section 12.3 |
| Record event | `rwb.decision.DecisionRecorded.v1` with the entry of a move and of an approval, from the DP-03 library | None (no DF-REF) |
| Refusal | `messageId` MSG-P4-001, MSG-P4-002, MSG-P7-002 on a 403, MSG-GEN-004 on a 409, MSG-GEN-001 on a 422 and MSG-P7-003 on a 503 | None (no DF-REF); message IDs from section 14 |

The exact request and answer field set of the two writes, the type and length of each field, the `limit_version` scheme and the record code of a move are Not specified in the source documents (GAP-0869; ASM-1574): TSD P4 v3 T3.1 fixes the columns of `delegation_limit` and API Specification v5 declares no write on the table. The state set is fixed by AC3 (GAP-0869; ASM-1574). The supersede date rule is Not specified in the source documents (GAP-0869; ASM-1575) and is fixed by the transition of BR5. The payload of the change event is Not specified in the source documents (GAP-0869; ASM-1576) and is fixed by AC3 and section 12.3. The decision code, approval level and product group of a moved row are taken from the row it moves; no reference list of this service checks them (GAP-0869). The text of MSG-P7-002 is left to the message catalogue (GAP-0869).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| PATCH | `/doa-limits/{delegationLimitId}` | `DoaLimitMove` in with an `Idempotency-Key` header, `DoaLimit` out in state `PENDING_APPROVAL` with `moveId`, `limitVersion`, `validFrom` and `approverRole` `RW-RISK` | Rules and parameters U, scope applied; `Idempotency-Key` required |
| POST | `/doa-limits/{delegationLimitId}/approve` | `limitVersion`, `version` and `decision` in with an `Idempotency-Key` header, `DoaLimit` out in state `IN_FORCE` with `validTo`, `approvedByRole` `RW-RISK` and `approvedAt`; the superseded row answers `SUPERSEDED` with its `valid_to` | Rules and parameters A, and the approver is not the author; `Idempotency-Key` required |

Errors for both: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002) and an approval by the author (MSG-P7-002), 409 a stale `version`, a row that is no longer in force or a version already pending (MSG-GEN-004), 422 a required field empty or an amount of the wrong shape (MSG-GEN-001), 503 the record or the outbox row cannot be written (MSG-P7-003). Both are writes, so every request carries an `Idempotency-Key` and a replay answers the first answer with no second row, entry or event (BR9). Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR8).

The two paths are Not specified in the source documents (GAP-0869; ASM-1574): Architecture v5 slide 14 names `GET /doa-limits` only, and the write paths are fixed here and confirmed by the contract review before they are frozen. The delegation lookup and the whole-version load are not declared in this document.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The U check behind the move and the A check behind the approval, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The move bounds and the six-monthly review flag, with the version in force (DP-06) |

Neither is declared as provided by rwb-access, and no operation of `rwb-decision`, `rwb-case` or the central ledger appears in the document as provided.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.access.DoaLimitChanged.v1` | `rwb.access.events.v1` | P4 rwb-access | AsyncAPI message keyed by `delegationLimitId`, payload `delegationLimitId`, `limitVersion`, `decisionCode`, `approvalLevel`, `productGroup`, `effectiveFrom`, `reason`; published from the outbox of the approving transaction |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of a move and of an approval with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

The payload of `DoaLimitChanged` declares no holder reference, no substitute reference, no name and no personal field, and no case id: a subscriber learns that a limit of a level and a product group changed from a date and asks the delegation lookup for the holder it needs (BR6, BR7). `rwb.access.AccessPolicyChanged.v1` is RWB-P4-E1037-APP's and is not declared here; the load of a whole DoA version publishes its change under the version rules of RWB-P4-E1038-APP.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14, and the two writes of this contract need no subscription. The document declares no inbox and no consumer group.

#### 12.5 Workflows and activities

None. No workflow, no activity and no signal is part of this contract: the approval is synchronous and the four-eyes rule is a right. The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only (BR10).

#### 12.6 Schedules

None. The two writes are request-driven, and the effective date of a move is data and not a Schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `delegation_limit` | P4 (rwb_access) | The row a move creates and the row an approval puts in force and supersedes; the columns are those of TSD P4 v3 T3.1 |
| `role` | P4 (rwb_access) | The role code and class behind the U and A letters |
| `permission` | P4 (rwb_access) | The U and A letters in Rules and parameters |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The entry the record event carries for a move and an approval |

No table of another service is named in the contract (DP-01): `decision_log_entry` and the rule registry are P7 rwb_decision's, `case`, `task` and `lov_value` are P3 rwb_case's, and `document` is rwb_document's. The holder and substitute references of a row are values of this service's own table and are never carried by the event (BR7).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| authorise fake | `POST /authorise` with a granted answer for RW-COE with U and for RW-RISK with A, and a refused answer with MSG-P4-002 for RW-PRODHEAD with R only | App story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with the move bounds and the six-monthly review flag at version PAR-2026.11 | App story, contract tests |
| decision-record fake | The append of a move and of an approval, the hash-link check, the replay of an `Idempotency-Key` and a forced failure | App story, contract tests |
| DoA fixture | DOA-2026.11 with the L6 row of item 2.1.1 MORTGAGE at principal 100,000,000.00 and loss 30.00 percent, and the same limit at principal 120,000,000.00 from 2027-01-01 as the moved version | App story, contract tests, harness |
| gateway-bff fake | The composite route of SCR-41 with the limits panel, the move form and the pending-approval state, calling both writes | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The move and the approval provided; the authorise and parameters reads consumed; one hop, 2 s timeout |
| Kafka | 2 event types published, 0 consumed | `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1` and `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | No file input and no file output; the DoA workbook is RWB-P4-E1038-APP's |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-doa-limit-v1.yaml` (OpenAPI 3.1) with the two writes and the shared components, `asyncapi/rwb-access-doa-limit-v1.yaml` with `rwb.access.DoaLimitChanged.v1`, `contract/error-envelope.yaml`, the `DoaLimitMove` and `DoaLimit` schemas with their examples, the state-set rule in the contract README, the versioning rules, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The two writes with the shapes of section 11: `DoaLimitMove` in, `DoaLimit` out, and the two rights.
3. The state set and the transition rule of BR5, stated in the document and in the contract README, with the two-rows-in-force case named as refused.
4. The AsyncAPI element of `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1`, with its key, its payload and the explicit absence of the holder and the substitute.
5. The consumed operations with their owners, the one-hop rule and the 2 s client budget.
6. The error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, with the texts of the legacy messages and MSG-P7-002 as an ID only.
7. The five fakes and the stub fixtures of section 12.8, including the two versions of the moved limit.
8. The six contract tests; a drift between a fake and the document fails the build.
9. Baseline tag and the consumer sign-off note from the app story, the screen route and the harness.

**Feature switch.** Both writes are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of this contract; the document declares no 404 branch of its own and adds no parameter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8008-APP | The two provided writes, the `DoaLimitMove` and `DoaLimit` schemas, the state set, the change event and the five fakes |
| RWB-PLT-N001-CON (gateway-bff and SCR-41) | The two writes as the limits panel, the move form and the pending-approval state call them |
| The harness of the wave 4 access journey | The state set, the effective dates and the change event, as the evidence it records |

The `limit_version` scheme the contract fixes is Not specified in the source documents (GAP-0869; ASM-1574): the document states that the move writes the next version of the limit and the DoA version load writes the version label of a whole version, and the two are agreed with RWB-P4-E1038-APP before the endpoints are frozen.

**Done when.** The document validates in the pipeline, the six contract tests pass, the AsyncAPI element matches the published topic, the five fakes answer every declared path, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without Rules and parameters U on a move, or without A on an approval | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty or an amount is not of its shape | Enter {field}. |
| MSG-GEN-004 | A stale `version`, a row no longer in force, or a version already pending | Someone else changed this record. Reload it to see their change. |
| MSG-P7-002 | The approver is the author of the move (four-eyes rule) | Not specified in the source documents (GAP-0869; ASM-1574) |
| MSG-P7-003 | The record or the outbox row cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. MSG-P7-002 carries a message ID and no text in this baseline, because TSD P4 v3 T6.3 states the four-eyes rule and not its wording; the message catalogue supplies the text before the endpoints are frozen.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-41 Delegation of authority | Limits, list | The rows of the version in force, read through the lookup of RWB-P4-E2013-APP, each naming its decision code, level, product group and limits |
| SCR-41 Delegation of authority | Move, form | `DoaLimitMove` with the four amounts, `validFrom`, `reason` and the `version` of the row read |
| SCR-41 Delegation of authority | Move, pending approval | `DoaLimit` in state `PENDING_APPROVAL` with its `limitVersion`, `validFrom` and `approverRole` `RW-RISK`, beside the row in force and unchanged |
| SCR-41 Delegation of authority | Move, approved | `DoaLimit` in state `IN_FORCE` and the superseded row in state `SUPERSEDED` with its `validTo` |
| SCR-41 Delegation of authority | Move, stale | The 409 of the envelope with MSG-GEN-004 and a reload action |
| SCR-41 Delegation of authority | Move, refused | The 403 of the envelope with MSG-P4-002 or MSG-P7-002 |
| SCR-41 Delegation of authority | Move, not recorded | The 503 of the envelope with MSG-P7-003 |
| SCR-41 Delegation of authority | Limits, empty | No row in the version in force; the state text is taken from Screen Specifications v1 SCR-41 |
| SCR-41 Delegation of authority | Loading | Not specified in the source documents (CG-ALL-5479) |
| SCR-41 Delegation of authority | Error | Not specified in the source documents (CG-ALL-5479) |
| SCR-41 Delegation of authority | No access | Not specified in the source documents (CG-ALL-5479) |

The screens are served by the gateway-bff composite route (DP-19), which reads the lookup of RWB-P4-E2013-APP and calls the two writes of this contract, one hop each. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work; the document fixes the limit-move side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-008-CON-01 | AC1 | Contract | The document validates; the base, the two writes, the rights U and A, the five error responses and the `Idempotency-Key` are present; the lookup and the version load are not provided |
| TC-E8-008-CON-02 | AC2 | Contract | The `DoaLimitMove` and `DoaLimit` fields map to DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 and the standard record columns; the required fields and the `PENDING_APPROVAL` answer |
| TC-E8-008-CON-03 | AC3 | Contract | The three states and the transition rule; the AsyncAPI element of `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1` with its seven fields and no holder or substitute |
| TC-E8-008-CON-04 | AC4 | Contract | A 401, 403, 409, 422 and 503 response carry one problem envelope with a valid message ID, and 403 carries MSG-P7-002 for an approval by the author |
| TC-E8-008-CON-05 | AC5 | Contract | Two consumed operations with their owners P4 and P3, one hop and the 2 s budget; the lookup and the version load declared as neither provided nor consumed |
| TC-E8-008-CON-06 | AC6 | Component | The five fakes match the document and the AsyncAPI element; a drifted fake fails the build; no name, e-mail address, personal field or holder reference in the event |
| TC-E8-008-CON-07 | AC7 | Contract | The tables named in the contract are the owned tables of section 12.7 with owner P4 rwb_access; no table of another service is named |
| TC-E8-008-CON-08 | AC8 | Contract | A replayed write with the same Idempotency-Key returns the first answer and publishes no second event or record entry |
| TC-E8-008-CON-09 | AC9 | Contract | A schema change within version 1 is additive; a removed, renamed or retyped field is declared as a new major version |
| TC-E8-008-CON-10 | AC10 | Contract | A request for a missing resource on a provided operation answers 404 with the one problem envelope of AC4 |
| TC-E8-008-CON-11 | AC11 | Contract | An approval of a row in state SUPERSEDED is refused with 409 and MSG-GEN-004; no state changes and no event is published |

### 17. Guardrails

- No business value in the contract: the amounts, the dates, the levels, the product groups and the decision codes stay rows and values behind the document, and the bounds stay parameter rows.
- No personal data in a schema, an example or a fake: references, codes, versions, amounts and times only, and the change event carries neither the holder nor the substitute (BR7).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the central ledger, the case, the task and the list values are absent or consumed, never named as this service's (DP-01).
- One REST base, one topic and one event-name pattern per service; a document that names another service's base or topic fails the review (DP-13).
- The delegation lookup and the whole-version DoA load stay out of this document: they are RWB-P4-E2013-APP's and RWB-P4-E1038-APP's, and a path of theirs declared here fails the review.
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- A write without its `Idempotency-Key` is refused by the contract, and a replay never produces a second event.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-004 | The delegation of authority table is held as reference data and sets every approval limit | The two writes, the `DoaLimit` schema with the delegation fields and the state set; the table itself is RWB-P4-E1038-APP's | TC-E8-008-CON-01, TC-E8-008-CON-02 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | The parameters read as consumed, the bounds behind the document, and the effective date as data | TC-E8-008-CON-02, TC-E8-008-CON-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The two writes as the SCR-41 route consumes them, with the four-eyes message ID and the refusal shapes | TC-E8-008-CON-04, TC-E8-008-CON-06 |

The requirement IDs are taken from the FSD feature table and the Program BRD under the fill order of Template and Rules §R7.3, which is the order the Work Package directs; the Work Package itself carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 move a delegated limit, with Risk approving and the change versioned | Sections 4, 7, 11, 12.1 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 7, 12.1, 14 |
| The permission check: Rules and parameters C for RW-COE and A for RW-RISK | Sections 7 (AC1, AC5), 10, 12.1, 14 |
| The delegation table fields of the legacy Data table | Section 11, section 12.7 |
| Legacy key RWB-E8-008, story RWB-P4-E8008-APP, contract RWB-P4-E8008-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the move and of the approval (RWB-P4-E8008-APP).
- The whole-version load of a DoA version, its approval and its rollback, and the columns and indexes of `delegation_limit` (RWB-P4-E1038-APP); this document consumes their shapes.
- The lookup `GET /api/recovery/access/v1/doa-limits` and the authority decision behind `POST /authorise` (RWB-P4-E2013-APP).
- The rule-change request and the rule-version paths of the same legacy key (`rwb-decision`, P7; RWB-E8-007).
- The approval record, the approval queue and the escalation (`rwb-decision`, P7).
- The screen SCR-41 Delegation of authority, its other panels and its composite route specification (RWB-PLT-N001-CON and the Epic 8 screen work).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The operations of other services: the authorise operation and the `rwb-case` parameters read are consumed and faked, never defined here.
- The cross-service journey harness and its evidence, and the `-ITG` copies of the test cases.
