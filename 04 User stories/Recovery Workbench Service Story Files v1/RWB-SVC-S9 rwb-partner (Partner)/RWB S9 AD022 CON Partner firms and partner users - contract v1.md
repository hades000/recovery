# RWB-S9-AD022-CON Partner firms and partner users - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-AD022-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-AD-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the partner firm and instruction surface of rwb-partner, split from RWB-AD-022. It fixes the six partner operations on `/api/recovery/partner/v1` (DP-13) with the `Partner`, `PartnerInstruction`, `InstructionRequest`, `InstructionAcceptance` and `Invoice` elements, the sixteen fields of DF-PRT-001 to DF-PRT-016, the four lists of TSD S9 T3.2, the rights of T6.1, the error sets of T-A.2, the two events EV-20 and EV-21, the tables of `rwb_partner` and the fakes. No source publishes an element for `partner_user`, maps EV-20 and EV-21 to their names in the ownership rows, or gives the rights behind the partner portal a contract of their own (GAP-3104; ASM-5334, ASM-5337). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract of the partner firm and instruction surface of rwb-partner - the six operations, the elements, the lists, the rights, the error set, the events, the tables and the fakes**, so that **the app story, the instruction stories, SCR-34, PRT-01 to PRT-04 and the wave 4 harness build against one fixed, testable contract on Day 1, and a field, a list value or an answer shape can never drift between rwb-partner, rwb-access and the partner gateway without a failing build**.

This baseline declares shapes and moves nothing. It writes no code, no migration and no table, and changes no firm, no user and no instruction. What it publishes is one OpenAPI 3.1 document, nine contract tables, four fakes and the two event schemas of the topic.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story named two endpoints on the monolith base `/api/recovery/v1`, while TSD S9 T-A.1 publishes six operations for the module and the ownership rows confirm six provided and none consumed: the firm and its users are S9's, the rights belong to rwb-access, and the partner outside the bank arrives through the partner gateway of FAPI 2.0 (Arch v5 slide 8; INT-24). Three boundaries are therefore fixed before the app story starts.

- **The base moves and nothing else.** DP-13 moves `monolith-base/partners` and `monolith-base/partner/instructions` to `/api/recovery/partner/v1`; the paths, the query parameters and the answer elements are TSD S9 T-A.1 and T-A.2 unchanged.
- **The firm and its work are the element set.** `Partner` covers DF-PRT-001 to DF-PRT-007 and `PartnerInstruction` covers DF-PRT-008 to DF-PRT-016; no element of any source covers `partner_user`, whose fields are DF-REF-212 to DF-REF-217 of the Logical Data Model, so the account is fixed as a table and not as an answer (GAP-3104; ASM-5329, ASM-5337).
- **The rights are the matrix.** TSD S9 T6.1 gives 29 identities the partner-portal rights R, C, U and A, and the legacy table names eight of them and "21 more"; the baseline publishes the matrix and widens nothing.
- **The events are two and neither is a recall.** EV-20 `InstructionIssued` and EV-21 `PartnerResultSubmitted` are TSD S9 T5.3's published pair, and the baseline maps the IDs to the names in the ownership order and publishes no recall event (GAP-3104; ASM-5334).
- **The edge is one hop.** The gateway-bff composite route serves SCR-34 to staff and PRT-01 to PRT-04 to partners, and the partner gateway terminates the partner's token (DP-19).
- **No user accounts of rwb-access.** rwb-access holds identities and rights and no partner user; the firm of a partner user is S9's row (ASM-5337).

The naming the checks require is fixed here: schema and login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules §R4; context pack).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case` is P3's, `decision_log_entry` is P7's, every `v_ace_*` view is P1's, `document` is P5's and `payment` is P8's. No other service's table or operation is declared here.
- TSD S9 T-A.1 and T-A.2 publish the six operations, their requests, their answers, their rights and their error sets, and the API Specification publishes `Partner`, `PartnerInstruction` and `Invoice`; FSD S9 A2.12 and the legacy story give the business meaning of the firm, the user and the recall.
- rwb-access publishes the partner-portal rights, and the partner gateway publishes the FAPI 2.0 token profile; neither document is named, and the baseline records the placeholder (GAP-3104; ASM-5332).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).
- No approval is needed to tag a Draft baseline; the consumer sign-off is recorded in section 10.

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-partner: the six operations under the base `/api/recovery/partner/v1`, each with its request, its answer, its right and its errors.
2. Fix the `Partner` element over DF-PRT-001 to DF-PRT-007: `id`, `partnerCode`, `partnerName`, `partnerType`, `panelStatus`, `contractEnd` and `score`, with the lists of TSD S9 T3.2 published unchanged.
3. Fix the `PartnerInstruction` element over DF-PRT-008 to DF-PRT-016: `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt`, `dueAt`, `status`, `resultCode` and `feeAmount`.
4. Fix the request elements: `InstructionRequest`, `InstructionAcceptance`, the multipart result of API-S9-005 and `InvoiceRequest` of API-S9-006.
5. Record that `partner_user` is a table of S9 and is published by no element, and that the account's status is read by the service and not by the portal as an element (GAP-3104; ASM-5337).
6. Fix the rights of the six operations from TSD S9 T-A.1 and T6.1: R on the two reads, C on the issue and the invoice, U on the accept and the result.
7. Publish the two event schemas of `rwb.partner.events.v1`: EV-20 `InstructionIssued` and EV-21 `PartnerResultSubmitted`, with their envelope, their payload and the rule that a payload carries identifiers and no personal data.
8. Publish the fakes of 12.8, the error envelope of section 14 and the naming baseline of 12.9.
9. Add the contract tests: schema validation, the additive rule, the element shapes, the lists, the rights, the error envelope, the boundary, the drift of a fake and the absence of a consumed operation and a recall event.
10. Tag the baseline and hand it to RWB-S9-AD022-APP, to the instruction stories of the module, to SCR-34 and PRT-01 to PRT-04, and to the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or a response fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | An element is published for `partner_user`, or an account field appears in an answer | The review fails and the absence test fails the build | None | AC3 |
| X5 | A right differs from TSD S9 T6.1 or T-A.1 | The access test fails the build | MSG-P4-002 | AC4 |
| X6 | A consumed operation, a second topic or a recall event is declared | The absence test fails the build | None | AC5, AC7 |
| X7 | The document names another service's base, table or topic as its own | The boundary test fails the review | None | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, FSD S9 and TSD S9, and the ownership rows only |
| Negotiable | The example values and the internal record shape are settled in the baseline review; the base, the operations, the rights, the lists, the topic, the queue and the schema are fixed |
| Valuable | Unblocks RWB-S9-AD022-APP, the instruction stories, SCR-34, PRT-01 to PRT-04 and the wave 4 harness on Day 1 |
| Estimable | One OpenAPI document, two event schemas, nine contract tables, four fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the partner firm and instruction surface of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner, partner_user and partner_instruction is S9, of recovery_case is P3, of every v_ace_* view is P1, of decision_log_entry is P7 and of document is P5
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The six partner operations are declared on the partner base with their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /partners (API-S9-001) and GET /partner/instructions (API-S9-003) with the query parameters, the Partner[] and InstructionPage answers and the errors 401, 403 and 503
    Then it declares POST /cases/{caseId}/instructions (API-S9-002), POST /partner/instructions/{instructionId}/accept (API-S9-004), POST /partner/instructions/{instructionId}/results (API-S9-005) and POST /partner/instructions/{instructionId}/invoices (API-S9-006) with their requests, their answers, the Idempotency-Key header and the errors 401, 403, 404, 409, 415, 422 and 503
    Then every path sits under the base /api/recovery/partner/v1 and no operation is declared on /api/recovery/v1
    Then the two reads declare no Idempotency-Key and the four mutations declare it
    Then the operations are those six and no seventh is added

  Scenario: AC2 The firm and instruction elements, their required flags and their lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S9 T3.0, T3.1, T3.2 and T-A.2
    Then Partner declares the seven fields of DF-PRT-001 to DF-PRT-007: id, partnerCode, partnerName, partnerType, panelStatus, contractEnd and score
    Then PartnerInstruction declares the nine fields of DF-PRT-008 to DF-PRT-016: id, caseId, partnerId, instructionType, instructedAt, dueAt, status, resultCode and feeAmount
    Then the required flags are id, partnerCode, partnerName, partnerType and panelStatus on the firm, and id, caseId, partnerId, instructionType, instructedAt and status on the instruction, with id read-only on both
    Then the lists are LOV-PARTNER-TYPE, LOV-PANEL, LOV-INSTRUCTION and LOV-INSTR-STATUS, copied from TSD S9 T3.2 and published unchanged
    Then contractEnd is a date with no default, score is numeric(5,2), feeAmount is numeric(18,2) and dueAt is optional
    Then the request elements are InstructionRequest, InstructionAcceptance, the multipart result of API-S9-005 and InvoiceRequest, with no field that no source gives

  Scenario: AC3 The partner user is a table of S9 and no element is published for it (new, D-RCV-60)
    Given the data section of the baseline
    When it is compared with the ownership rows and the API appendix
    Then partner_user is declared as a table of S9 in rwb_partner with partner_instruction and partner, carrying the period fields DF-REF-212 to DF-REF-217 of the Logical Data Model
    Then the document declares no PartnerUser element, no user path, no account field in an answer and no account status list
    Then TSD S9 T3.1 catalogues the firm and the instruction and not the user, so the user's fields are cited from DF-REF-212 to DF-REF-217 and no element, path or account status list is published for it (GAP-3104; ASM-5329, ASM-5338)
    Then the document declares no personal name, e-mail, phone number, address or identity number in any element or example

  Scenario: AC4 The rights of TSD S9 T6.1 and T-A.1 are fixed for every operation (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T6.1 and T-A.1
    Then the two reads declare Partner portal right R, the issue and the invoice right C, and the accept and the result right U, each with the scope applied
    Then RW-AGENCYMG holds CRUDA and is the only identity that changes the firm
    Then the matrix publishes the 23 RW-* and 6 PT-* identities of T6.1, which are the eight roles and the 21 more of the legacy table
    Then a role without the right is described as refused with MSG-P4-002
    Then the partner user is scoped to its own firm on every read and no operation takes the firm as a parameter

  Scenario: AC5 The two events are declared with their names and the topic is the service's own (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with TSD S9 T5.3 and the context pack events
    Then EV-20 is declared as rwb.partner.InstructionIssued.v1 with caseId, partnerId, instructionType and dueAt
    Then EV-21 is declared as rwb.partner.PartnerResultSubmitted.v1 with caseId, instructionId, resultCode and resultedAt
    Then both carry the CloudEvents envelope, the producer group rwb-partner, the outbox and the inbox rules of the platform
    Then the topic is rwb.partner.events.v1 with its retry and .dlt topics and no second topic is declared
    Then no recall event, no consumer group and no Schedule is declared by this baseline

  Scenario: AC6 The four fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-access right and identity fake answers every right of AC4 and a live and a disabled account
    Then the gateway-bff and partner-gateway fake answers SCR-34 and PRT-01 to PRT-04 with the firm of the caller only
    Then the decision-record stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1 with its retry and .dlt topics, the queue is rwb-partner in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_user and partner_instruction, and recovery_case, every v_ace_* view, decision_log_entry, document and payment are named as other owners'
    Then the document declares no consumed operation, no v_ace_* read and no case, document or payment element of its own
    Then the absence test fails a build that adds a consumed operation, a second topic, a recall event, a Schedule or a v_ace_* path
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-AD022-APP, whose one legacy criterion stays with it word for word, and they copy no criterion of the legacy story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The firm, its users and its instructions are rwb-partner's, and the contract declares their fields, flags and lists on its own elements only | TSD S9 T3.1, T3.2; context pack ownership rows |
| BR2 | The base is one per service: every path sits under `/api/recovery/partner/v1` and no legacy `/api/recovery/v1` path is kept | DP-13; Template and Rules §R4 |
| BR3 | The event names are `rwb.<short>.<Event>.v1` on `rwb.partner.events.v1`, with the retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR4 | No value a business person may change is an enumeration member taken from no source: every list is the published list of TSD S9 T3.2, copied unchanged | BR-S9-012; FSD S9 A2.12.3.1 |
| BR5 | The rights are the matrix of TSD S9 T6.1 and T-A.1; the contract widens none and adds no capability area of its own | TSD S9 T6.1, T-A.1 |
| BR6 | `partner_user` is a table and not an element: no user path, no account field in an answer and no account status list is published; its period fields are DF-REF-212 to DF-REF-217 | GAP-3104; ASM-5329, ASM-5337 |
| BR7 | The two events carry identifiers and codes and no personal data; a payload never carries a name, an e-mail, a phone number, an address or an identity number | Template and Rules §R7.2 (s17); TSD S9 T6.2 |
| BR8 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR9 | The document lists only operations owned by rwb-partner; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11; context pack ownership rows (6 provided, 0 consumed) |
| BR10 | No read of ACE: no `v_ace_*` path, view or property is declared, and DP-05 is a prohibition for this service | DP-05; ASM-5332 |
| BR11 | The `Idempotency-Key` header is declared on the four mutations and on neither read, as T-A.2 gives it | TSD S9 T-A.2 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operations, the elements, the rights, the events and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the instruction stories, the screens and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list member changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3, AC5 and AC7 fail | In review |

The state machine the document serves is the firm's: the panel moves on `panel_status` from `ACTIVE`, `ON_NOTICE` and `SUSPENDED` to `EXITED`, and the instruction moves on `status` from `SENT`, `ACCEPTED` and `IN_PROGRESS` to `RECALLED`, `DECLINED` and `DONE` (TSD S9 T3.2). This baseline publishes the vocabulary and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document, the event schemas and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the correction of the plan rows the baseline consumes, and the reading of `partner_user` as a table |
| Business lead | Confirms the meaning of the panel and instruction states and the contract end |
| Consuming teams (the app story, the instruction stories, SCR-34, PRT-01 to PRT-04, the wave 4 harness and the owners of rwb-access and the partner gateway) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the outbox and inbox library and the decision-record library |
| Data steward | Confirms that no personal data field is declared in an element, an event or a fake |

The per-service login behind the security scheme is named "the rwb-partner login (DP-02)" and is not part of this baseline.

### 11. Data

The baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Firm element | DF-PRT-001 to DF-PRT-007: `id`, `partnerCode`, `partnerName`, `partnerType`, `panelStatus`, `contractEnd`, `score` |
| Instruction element | DF-PRT-008 to DF-PRT-016: `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt`, `dueAt`, `status`, `resultCode`, `feeAmount` |
| Requests | `InstructionRequest`, `InstructionAcceptance`, the multipart result of API-S9-005 and `InvoiceRequest` |
| Required flags | `id`, `partnerCode`, `partnerName`, `partnerType`, `panelStatus` on the firm and `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt`, `status` on the instruction; `id` read-only on both |
| Lists | LOV-PARTNER-TYPE, LOV-PANEL, LOV-INSTRUCTION and LOV-INSTR-STATUS, copied from TSD S9 T3.2 |
| Event data | EV-20 `caseId`, `partnerId`, `instructionType`, `dueAt`; EV-21 `caseId`, `instructionId`, `resultCode`, `resultedAt` |
| Provider data | `recovery_case` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `payment` (P8): named, never declared |
| Not published | `partner_user`: it is an S9 table with no element, no path and no account field; its period fields are DF-REF-212 to DF-REF-217 (GAP-3104; ASM-5329, ASM-5337) |

The field-level types, lengths and required flags are those of TSD S9 T3.1 and the API Specification; this story fixes the element names and the flags of AC2. **No new table, no new column and no migration** is declared.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/partners` (API-S9-001) | Query `type`, `status`; `Partner[]` out | Partner portal, right R, scope applied | Not applicable |
| GET | `/partner/instructions` (API-S9-003) | Query `status`, `page`, `size`; `InstructionPage` out for the caller's firm | Partner portal, right R, scope applied | Not applicable |
| POST | `/cases/{caseId}/instructions` (API-S9-002) | `InstructionRequest` in, `PartnerInstruction` out | Partner portal, right C, scope applied | `Idempotency-Key` |
| POST | `/partner/instructions/{instructionId}/accept` (API-S9-004) | `InstructionAcceptance` in, `PartnerInstruction` out | Partner portal, right U, scope applied | `Idempotency-Key` |
| POST | `/partner/instructions/{instructionId}/results` (API-S9-005) | Multipart `result` and `files` in, `PartnerInstruction` out | Partner portal, right U, scope applied | `Idempotency-Key` |
| POST | `/partner/instructions/{instructionId}/invoices` (API-S9-006) | `InvoiceRequest` in, `Invoice` out | Partner portal, right C, scope applied | `Idempotency-Key` |

API-S9-001 and API-S9-003 answer 401, 403 with MSG-P4-002 and 503. API-S9-002 answers 401, 403, 404 for a case that is not in scope, 409 for a duplicate key, 422 with MSG-GEN-001 and 503. API-S9-004 answers 401, 403, 404, 409 and 503. API-S9-005 answers 401, 403, 404, 409, 415 for a file type outside the allowed set, 422 and 503. API-S9-006 answers 401, 403, 404, 409, 422 and 503. Each carries the error envelope and one message ID of section 14. The paths, the operation IDs, the requests, the answers and the error sets are published in TSD S9 T-A.1 and T-A.2; what carries a placeholder is the account behind the caller, which no element publishes (GAP-3104; ASM-5337).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The partner-portal right and identity read (operation Not specified in the source documents (GAP-3104; ASM-5332)) | `/api/recovery/access/v1` | P4 rwb-access | The right per operation and the status of the partner's sign-in, declared as a consumed row and faked |

The row is one hop with a 2 s timeout and a breaker (ADR-020). The plan's C row of the app story carries RWB-P4-E1022-CON and this baseline's own row is None, because a CON story has no contract dependency; the operation name is a placeholder until its owner publishes it.

#### 12.3 Events published

| Event | Name | Payload | Consumed by |
|---|---|---|---|
| EV-20 `InstructionIssued` | `rwb.partner.InstructionIssued.v1` | `caseId`, `partnerId`, `instructionType`, `dueAt` | The case-owning service and rwb-reporting |
| EV-21 `PartnerResultSubmitted` | `rwb.partner.PartnerResultSubmitted.v1` | `caseId`, `instructionId`, `resultCode`, `resultedAt` | The case-owning service and rwb-reporting |

Both are published on `rwb.partner.events.v1` with its retry and `.dlt` topics, through the outbox and the CloudEvents envelope of DP-09; the producer group is `rwb-partner`. The two names come from TSD S9 T5.3, which publishes them without an ID, and the IDs EV-20 and EV-21 from the ownership rows, so the mapping is taken in the ownership order and recorded (GAP-3104; ASM-5334). No recall event is declared. The building of the two events belongs to the instruction stories; this baseline publishes their schemas only.

#### 12.4 Events consumed

None. The service places and receives work through REST on its own base and reads no other service's topic in the ownership rows. A consumer group, a subscription or an inbox row added here fails the absence test of AC5, and the module's two published events leave no third event to consume.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction | `rwb-partner` in namespace `rwb-recovery` | Input: the instruction reference, the case reference and the firm; signals: accept, result, recall, contract end; outcome: the instruction status |

`InstructionWorkflow` is the one workflow in the context pack's ownership rows; its activities are the instruction stories' and this baseline declares the workflow and its signal surface only, and registers no activity. The contract end has no published operation: it arrives as the `contractEnd` command on this workflow, and the branch that applies it belongs to RWB-S9-E7015-APP, with the dated trigger of RWB-S9-AD022-APP; the baseline declares the command surface and neither builds the branch (ASM-5331).

#### 12.6 Schedules

None. This baseline declares no Temporal Schedule, no Quartz row and no shared job table; the service's job list is empty in the ownership rows (Jobs: None). The daily contract-end pass of the app story is declared there and its name, time and catch-up rule carry a placeholder (GAP-3104; ASM-5330).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| partner | S9 (`rwb_partner`) | The firm, its panel status, its contract end and its score; the source of the firm element |
| partner_instruction | S9 (`rwb_partner`) | The work placed with a firm; the source of the instruction element |
| partner_user | S9 (`rwb_partner`) | The firm's users over DF-REF-212 to DF-REF-217; a table with no element and no path (AC3) |
| decision_record | PLT library, in `rwb_partner` | The local hash-linked record of a change (DP-03) |
| idempotency_key | PLT library, in `rwb_partner` | The key and the stored answer of the four mutations |
| outbox_event | PLT library, in `rwb_partner` | The relay row of EV-20 and EV-21 |

`recovery_case` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6) and `payment` (P8) are not owned: the document names them and declares none of their fields, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-access right and identity fake (`RWB-P4-E1022-CON`) | The partner-portal right R, C, U and A per operation, and a live and a disabled partner account | AC4, AC6 |
| gateway-bff and partner-gateway fake | SCR-34 and PRT-01 to PRT-04 with the firm of the caller only, before and after an exit | AC5, AC6 |
| Decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6 |
| Identity fake of a partner user | A caller mapped to a firm and to a status, with no personal field | AC3, AC4 |

The fakes are test-only and are replaced by the real services in SIT; the operation name of the rwb-access read carries the placeholder until its owner confirms it (GAP-3104; ASM-5332).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 6 provided, 1 consumed | API-S9-001 to API-S9-006 on `/api/recovery/partner/v1`; the rwb-access read; one hop, 2 s |
| Kafka | 2 published, 0 consumed | EV-20 and EV-21 on `rwb.partner.events.v1` with the retry and `.dlt` topics; no recall event |
| Temporal | 1 workflow declared, 0 registered | `InstructionWorkflow` on `rwb-partner`; no Schedule, no activity and no child of `CaseWorkflow` |
| File | None | No file is read, built or delivered; the multipart result of API-S9-005 is an upload to rwb-document through its owner |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: the document declares no `v_ace_*` path or property and the service holds no grant. DP-13 moves the two legacy paths and gives the six operations their home. DP-19 sits behind SCR-34 and PRT-01 to PRT-04, whose screen model is the edge contract's. DP-09, which the two events need, DP-14, which the topic name carries, and DP-08, which the rights carry, are not in the pattern set: the topic follows the naming library, the events are the instruction stories' build, and the rights are a contract row of rwb-access, so their absence is recorded (GAP-3104; ASM-5332, ASM-5334).

**Deliverables and build steps**

1. Write the six operations and validate the additive rule of AC1 in the pipeline.
2. Fix the `Partner` and `PartnerInstruction` elements with their sixteen fields, the ten required flags and the four lists (AC2).
3. Fix the four request elements and the two answers of the multipart and the invoice.
4. Record `partner_user` as a table and publish no element for it (AC3).
5. Publish the rights matrix and the scope rule (AC4), the two event schemas (AC5) and the four fakes with the drift test (AC6).
6. Record the naming baseline, the boundary and the nine tables, then tag the baseline and collect the consumer sign-off (AC7).

The deliverables are `openapi/rwb-partner-v1.yaml`, the two event schemas, the contract README rows for the consumed row and its placeholder, and the four fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the eight contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the instruction stories, the screens and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation (X1) | Enter {field}. |
| MSG-P4-002 | The role lacks the partner-portal right the operation declares, or the partner account is disabled (X5) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before a change is answered | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are the legacy and FSD set of RWB-AD-022 (MSG-GEN-001, MSG-P4-002) plus the exception flow AC-EXC-S9-012-02 of FSD S9 A2.12.4.3; the text is copied unchanged and no message is added.

### 15. Screens and states

The contract serves SCR-34 Partner list for staff and PRT-01 Partner home, PRT-02 Instruction, PRT-03 Upload result and PRT-04 Invoice for partners, all through the gateway-bff composite route and, outside the bank, the partner gateway of FAPI 2.0 (FSD S9 Screens; Arch v5 slide 8; INT-24). The legacy screen table gives SCR-34 and PRT-01 "Loading; list"; PRT-02 to PRT-04 are named by the FSD and carry no legacy state, and the composite route specification and the screen field lists belong to RWB-PLT-N001-CON.

No source publishes a screen for the firm's users or for the contract-end pass, so the place of the account list is Not specified in the source documents (GAP-3104; ASM-5337). The refusal, disabled-account, duplicate and invalid-answer states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-022-01 | AC1, AC4 | Contract | A partner user of one firm; the firm read and the instruction read answer with that firm's rows only and with right R |
| TC-AD-022-02 | AC1, AC2 | Contract | A firm with a contract end of today and a live instruction; the contract half asserts the two elements, the lists, the flags and the recall status in the vocabulary |
| TC-AD-022-03 | AC4 | Contract | A role without the partner-portal right; the 403 with MSG-P4-002 of the envelope |
| TC-S9-AD022-CON-01 | AC1 | Contract | The document validates; the six operations, the base, the rights, the `Idempotency-Key` rule and the error sets are present |
| TC-S9-AD022-CON-02 | AC2 | Contract | The two elements with their sixteen fields, the ten required flags, the four lists and the four request elements |
| TC-S9-AD022-CON-03 | AC3, AC7 | Contract | `partner_user` as a table with no element; the naming baseline, the tables owned and the `v_ace_*` prohibition |
| TC-S9-AD022-CON-04 | AC4, AC5 | Contract | The 29 identities, the rights per operation, the two event schemas, the topic and the retry and `.dlt` topics |
| TC-S9-AD022-CON-05 | AC6 | Contract | The four fakes match the document and a drifted fake fails the build |

The three legacy cases are those of RWB-AD-022 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, and the business outcome is proved by RWB-S9-AD022-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S9-AD022-CON-01` to `-05` are new. The full test is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the panel states, the instruction states, the types, the right and the contract end stay reference data and rule rows, never a schema default or an enumeration member taken from no source.
- No personal data in a schema, an event, an example or a fake: identifiers, codes, dates, list values and amounts only, and every example is synthetic.
- The firm, the user and the instruction stay with rwb-partner: the document declares no case, document, payment or ACE property (DP-01).
- ACE data only through the owner's contract: no `v_ace_*` path, view or property is declared (DP-05, BR10).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-partner; a consumed operation is described as consumed and faked, never as provided (DP-11).
- No retired element is reintroduced: no `v_ace_*` read, no data-lake export, no shared job table and no consumer group.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S9-008 | Partners exchange data through the portal and the external gateway, not by email | The six operations, the partner gateway and the composite route | TC-AD-022-01, TC-S9-AD022-CON-01 |
| REQ-S9-001 | Every partner type is managed on the same six points, notice and exit among them | The firm element, the panel list and the instruction element | TC-S9-AD022-CON-02 |
| REQ-S9-002 | Each partner type has one named owner | The firm element and its users as a table | TC-S9-AD022-CON-02 |
| REQ-S9-003 | Work is allocated to partners by measured return against a scorecard | The allocation read of the instruction element; the rule is FEAT-PRM-03's | TC-AD-022-02 |
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results | `feeAmount` and the invoice operation | TC-S9-AD022-CON-02 |
| REQ-S9-006 | A panel exit, a conflict of interest, insolvency or an upheld conduct breach recalls every open case held by that partner | `status` over LOV-INSTR-STATUS and the recall vocabulary | TC-AD-022-02 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the six operations | TC-S9-AD022-CON-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-AD022-CON-03 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The two event schemas and the outbox row | TC-S9-AD022-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed row and the six operations | TC-AD-022-01 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-AD-022, disposition Split (rework); legacy feature None, and the closest published features are FEAT-PRM-01, FEAT-PRM-02 and FEAT-PRM-12 (FSD S9 A2.1, A2.2, A2.12) |
| Legacy criteria | AC1 and AC2 belong to the read stories and to RWB-S9-AD022-APP; this baseline copies neither |
| Wave and release | Wave 4 and release 28 February 2027 (tentative), copied unchanged; EP08 is wave 4 and the service's Arch v5 wave is 4, so no W-MAP conflict is raised (ASM-5335) |
| Source text | Legacy RWB-AD-022; FSD S9 Partner management v3 A1.1, A1.2, A2.1, A2.2, A2.12 and Screens; TSD S9 Partner management v2 T0.2, T2, T3.0, T3.1, T3.2, T3.3, T5.1, T5.3, T6.1, T6.2, T8, T-A |
| Test cases | The three legacy cases as the contract half, and the five new contract cases TC-S9-AD022-CON-01 to -05 |
| Feature and screens | FEAT-PRM-01, FEAT-PRM-02 and FEAT-PRM-12; SCR-34 and PRT-01 to PRT-04 |
| Rules | BR-S9-012, VR-S9-012-1 and the four lists of TSD S9 T3.2 |
| Decoupling patterns | DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the operations, the dated pass and the account effect: RWB-S9-AD022-APP; the exit branch, the recall, its record, the case request and the clock: RWB-S9-E7015-APP.
- The building of the two events and of the accept, result and invoice steps: the instruction stories of the module.
- The case of record and its re-selection after a recall: rwb-case (P3); no case element is declared.
- The rights as code, the partner's sign-in and the FAPI 2.0 token: rwb-access (P4) and the partner gateway, declared as a consumed row and faked.
- The documents and the files of a result and an invoice: rwb-document (P5) and rwb-payment (P8) through their owners.
- The account element, its screen fields and its status list: Not specified in the source documents (GAP-3104; ASM-5337).
- The gateway-bff composite route and the screen field lists of SCR-34 and PRT-01 to PRT-04: RWB-PLT-N001-CON.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
