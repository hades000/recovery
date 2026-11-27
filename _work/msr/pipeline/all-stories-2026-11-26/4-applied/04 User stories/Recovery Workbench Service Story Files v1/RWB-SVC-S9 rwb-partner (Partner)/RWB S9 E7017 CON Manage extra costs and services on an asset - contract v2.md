# RWB-S9-E7017-CON Manage extra costs and services on an asset - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7017-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the additional-cost claim on a held asset, split from RWB-E7-017. It fixes the three partner operations the claim is made and read by on `/api/recovery/partner/v1` (DP-13), the claim and invoice elements over DF-PRT-008 to DF-PRT-016, the rights of TSD S9 T6.1, the error sets of T-A.2, the one event of the pair that announces a claim, the tables of `rwb_partner` and the fakes. No source publishes the fields of `InvoiceRequest` or `Invoice`, a cost line of its own, the value set of `result_code`, an operation that approves a claim, or an event that announces an invoice or an approval (GAP-3134; ASM-5483, ASM-5484, ASM-5488). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E7017-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract of the additional-cost claim of rwb-partner - the three operations, the claim and invoice elements, the rights, the error set, the event, the tables and the fakes**, so that **the app story, SCR-35, the partner gateway and the wave 4 harness build against one fixed, testable contract on Day 1, and a field, a right or an answer shape of a cost claim can never drift between rwb-partner, rwb-access and rwb-asset without a failing build**.

This baseline declares shapes and moves nothing. It writes no code, no migration and no table, and changes no instruction, no firm and no claim. What it publishes is one OpenAPI 3.1 fragment for three operations, nine contract tables, four fakes and the one event schema the claim is announced by.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story named two endpoints on the monolith base; TSD S9 T-A.1 publishes six operations for the module and the ownership rows confirm six provided and none consumed. The extra cost of a held asset is a partner result and a fee invoice, so two mutations and one read of those six are this key's surface.

- **The base moves and nothing else.** DP-13 moves the result and instruction paths to `/api/recovery/partner/v1`; the paths, the requests, the answers and the error sets are TSD S9 T-A.1 and T-A.2 unchanged.
- **The claim is a result, and the money is an invoice.** `PartnerInstruction` covers DF-PRT-008 to DF-PRT-016 and API-S9-005 records the claim with its files; API-S9-006 takes `InvoiceRequest` and answers `Invoice`. No source publishes a cost line of its own, so the baseline fixes the element names, the flags and the absence, and nothing more (GAP-3134; ASM-5483).
- **The rights are the matrix.** TSD S9 T6.1 gives 29 identities the partner-portal rights R, C, U and A; the claim is U on the result write, C on the invoice write and R on the instruction read, and the baseline widens nothing.
- **One event and no approval announcement.** EV-21 `PartnerResultSubmitted` is TSD S9 T5.3's published fact and a claim is a result, so its schema is published and no invoice or approval event exists to publish (GAP-3134; ASM-5488).
- **The edge is one hop and the asset is not declared.** The composite route serves SCR-35 and PRT-02 to PRT-04 and the partner gateway terminates the partner's token (DP-19; INT-24); the asset record and `v_ace_npa_asset` are rwb-asset's and P1's, and no property of them is declared (DP-05; ASM-5486).

The naming is fixed here: schema and login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules §R4; context pack).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event name follow the platform rule.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership comes from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case` is P3's, `decision_log_entry` and `rule_row` are P7's, `document` is P5's, `payment` is P8's, and the asset record with `v_ace_npa_asset` is S5's and P1's. No other service's table or operation is declared here.
- TSD S9 T-A.1 and T-A.2 publish the six operations with their requests, answers, rights and error sets, and the API Specification publishes `PartnerInstruction` and `Invoice`; FSD S9 A2.14 and the legacy story give the business meaning of the extra cost.
- RWB-S9-AD022-CON publishes the firm element, the partner read, the issue and the accept operations and shares this service's schema and topic; this baseline re-publishes none of them and names the boundary in 12.1.
- The partner gateway's FAPI 2.0 token profile and the partner-portal rights of rwb-access are named but not yet published for this key, and the placeholder is recorded (GAP-3134; ASM-5487).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7), and no approval is needed to tag a Draft baseline.

### 4. Flow

1. Draft the OpenAPI 3.1 fragment: `POST /partner/instructions/{instructionId}/results` (API-S9-005), `POST /partner/instructions/{instructionId}/invoices` (API-S9-006) and `GET /partner/instructions` (API-S9-003), each with its request, its answer, its right and its errors.
2. Fix the claim on the `PartnerInstruction` element over DF-PRT-008 to DF-PRT-016 and mark the three fields it writes: `resultCode`, `feeAmount` and `status`.
3. Fix `InvoiceRequest` and `Invoice` with the fields the API Specification gives them and record that no source publishes the rest (GAP-3134; ASM-5483).
4. Record that the additional cost has no table and no element of its own in S9: it rides on `partner_instruction` and on the result file of rwb-document (AC3).
5. Fix the rights from TSD S9 T-A.1 and T6.1: U on the result write, C on the invoice write, R on the read, each with the scope applied (AC4).
6. Publish one event schema: EV-21 `PartnerResultSubmitted`, with its envelope, its payload and the rule that a payload carries identifiers and no personal data (AC5).
7. Publish the fakes of 12.8, the error envelope of section 14 and the naming baseline of 12.9 (AC6).
8. Record the boundary: no consumed operation, no `v_ace_*` read, no asset element, no approval route and no second topic (AC7).
9. Add the contract tests and tag the baseline, then hand it to RWB-S9-E7017-APP, SCR-35, PRT-02 to PRT-04, RWB-PLT-N001-CON and RWB-ITG-E7017-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or a response fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A field of the invoice element carries a value no source gives | The review fails and the element test fails the build | None | AC2, AC3 |
| X5 | A right differs from TSD S9 T6.1 or T-A.1 | The access test fails the build | MSG-P4-002 | AC4 |
| X6 | A consumed operation, a second topic, an approval route or an asset element is declared | The absence test fails the build | None | AC5, AC7 |
| X7 | The document names another service's base, table or topic as its own | The boundary test fails the review | None | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, FSD S9, TSD S9 and the ownership rows only |
| Negotiable | The example values and the internal record shape are settled in the baseline review; the base, the operations, the rights, the element names, the topic, the queue and the schema are fixed |
| Valuable | Unblocks RWB-S9-E7017-APP, SCR-35, PRT-02 to PRT-04 and RWB-ITG-E7017-ITG on Day 1 |
| Estimable | One OpenAPI fragment, one event schema, nine contract tables, four fakes and seven contract tests |
| Small | One sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the additional-cost claim of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner, partner_user and partner_instruction is S9, of recovery_case is P3, of every v_ace_* view is P1, of the asset record is S5, of decision_log_entry is P7 and of document is P5
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The three claim operations are declared on the partner base with their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then POST /partner/instructions/{instructionId}/results (API-S9-005) declares the multipart result, its files, the PartnerInstruction answer, the Idempotency-Key header and the errors 401, 403, 404, 409, 415, 422 and 503
    Then POST /partner/instructions/{instructionId}/invoices (API-S9-006) declares InvoiceRequest in, Invoice out, the Idempotency-Key header and the errors 401, 403, 404, 409, 422 and 503
    Then GET /partner/instructions (API-S9-003) declares the query status, page and size, the InstructionPage answer for the caller's firm, no Idempotency-Key and the errors 401, 403 and 503
    Then every path sits under the base /api/recovery/partner/v1 and none on the monolith base
    Then the partner read, the issue and the accept operations are named as RWB-S9-AD022-CON's and are not re-published, and the operations are those three and no fourth

  Scenario: AC2 The claim element, the invoice elements and their flags are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S9 T3.1, T3.2 and T-A.2 and with the API Specification
    Then PartnerInstruction declares the nine fields of DF-PRT-008 to DF-PRT-016, and the claim writes resultCode, feeAmount and status and reads the other six
    Then InvoiceRequest and Invoice declare only the fields the API Specification publishes, and the cost line of a claim is Not specified in the source documents (GAP-3134; ASM-5483)
    Then feeAmount is numeric(18,2), status is required over LOV-INSTR-STATUS, resultCode is varchar(40) and optional, and the lists are LOV-INSTRUCTION, LOV-INSTR-STATUS, LOV-PANEL and LOV-PARTNER-TYPE copied from TSD S9 T3.2
    Then the value set of resultCode is reference data and no member is invented

  Scenario: AC3 The additional cost has no table and no element of its own in S9 (new, D-RCV-60)
    Given the data section of the baseline
    When it is compared with the ownership rows and TSD S9 T3.1
    Then partner, partner_user and partner_instruction are declared as the three tables of S9 and the claim is carried on partner_instruction
    Then the document declares no cost table, no cost column, no cost path and no cost element beyond the invoice pair of AC2
    Then the evidence file of a claim is named as rwb-document's and no document field is declared
    Then the asset record and v_ace_npa_asset are named as S5's and P1's and no asset property appears in any element

  Scenario: AC4 The rights of TSD S9 T6.1 are fixed for every operation (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T6.1 and T-A.1
    Then the result write declares Partner portal right U, the invoice write right C and the instruction read right R, each with the scope applied
    Then the matrix publishes the 23 RW-* and 6 PT-* identities of T6.1, which are the eight roles and the 21 more of the legacy table
    Then a role without the right is described as refused with MSG-P4-002
    Then a partner is scoped to its own firm on every operation and no operation takes the firm as a parameter
    Then no approval right is declared, because no operation of the module approves a claim

  Scenario: AC5 One event is declared and the topic is the service's own (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with TSD S9 T5.3 and the context pack events
    Then EV-21 is declared as rwb.partner.PartnerResultSubmitted.v1 with caseId, instructionId, resultCode and resultedAt
    Then it is declared as the announcement of a recorded claim, once per claim, with the outbox and inbox rules and the CloudEvents envelope
    Then the topic is rwb.partner.events.v1 with its retry and .dlt topics and no second topic is declared
    Then no invoice event, no approval event, no consumer group and no Schedule is declared, and EV-20 InstructionIssued is named and not declared

  Scenario: AC6 The four fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the partner-portal right and identity fake answers every right of AC4 and a caller of one firm
    Then the gateway-bff and partner-gateway fake answers SCR-35 and PRT-02 to PRT-04 with the firm of the caller only
    Then the decision-record stub answers a healthy chain and a stopped chain
    Then the document upload fake answers a stored reference and a 415 for a disallowed type, and the claim fixture answers one instruction with its amount and evidence
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1 with its retry and .dlt topics, the queue is rwb-partner in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_user and partner_instruction, and the asset record, every v_ace_* view, recovery_case, decision_log_entry, document and payment are named as other owners'
    Then the document declares no consumed operation, no v_ace_* read and no asset, case, document or payment element of its own
    Then the absence test fails a build that adds a consumed operation, a second topic, an approval route, a cost table, a Schedule or a v_ace_* path
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-E7017-APP, whose one legacy criterion stays with it word for word, and they copy no criterion of the legacy story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The claim and its invoice are rwb-partner's, and the contract declares the claim on the instruction element and the money on the invoice pair only | TSD S9 T3.1, T-A.2; ownership rows |
| BR2 | Every path sits under `/api/recovery/partner/v1` and no monolith path is kept | DP-13; Template and Rules §R4 |
| BR3 | The event name is `rwb.<short>.<Event>.v1` on `rwb.partner.events.v1`, with the retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR4 | No value a business person may change is an enumeration member taken from no source: the lists are TSD S9 T3.2's and the codes of `resultCode` are reference data | BR-S9-014; FSD S9 A2.14.3.1 |
| BR5 | The rights are the matrix of TSD S9 T6.1 and T-A.1; the contract widens none and declares no approval right | TSD S9 T6.1, T-A.1 |
| BR6 | The additional cost has no table of its own: the claim rides on `partner_instruction` and the evidence on rwb-document | GAP-3134; ASM-5483 |
| BR7 | The payload of EV-21 carries identifiers, a code and a date and no personal data | Template and Rules §R7.2 (s17); TSD S9 T6.2 |
| BR8 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR9 | The document lists only operations owned by rwb-partner and re-publishes no other baseline's operations | DP-01, DP-11; ownership rows (6 provided, 0 consumed) |
| BR10 | No read of ACE and no read of the asset: no `v_ace_*` path, view or property and no asset element is declared | DP-05; ASM-5486 |
| BR11 | The `Idempotency-Key` header is declared on the two mutations and on neither read | TSD S9 T-A.2 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operations, the elements, the rights, the event and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the screens, the edge contract and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list member changes | New major version drafted |
| Baselined | Drift in a fake, or a forbidden element | A contract test or an absence test fails | In review |

The state machine the document serves is the claim's: the instruction moves on `status` from `SENT` and `ACCEPTED` to `IN_PROGRESS`, then to `DONE` on approval, and a recall moves it to `RECALLED` (TSD S9 T3.2). This baseline publishes the vocabulary and moves nothing, and it declares no approval status because the list has none (ASM-5485).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI fragment, the event schema and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the reading of the claim as a row of `partner_instruction` with no cost table |
| Business lead | Confirms the meaning of the instruction states and the invoice |
| Consuming teams (the app story, SCR-35, PRT-02 to PRT-04, RWB-PLT-N001-CON, RWB-ITG-E7017-ITG and the owners of rwb-access, rwb-document, rwb-asset and the partner gateway) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the outbox and inbox library and the decision-record library |
| Data steward | Confirms that no personal data field is declared in an element, an event or a fake |

The per-service login behind the security scheme is named "the rwb-partner login (DP-02)" and is not part of this baseline.

### 11. Data

| Item | Content |
|---|---|
| Claim element | DF-PRT-008 to DF-PRT-016: `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt`, `dueAt`, `status`, `resultCode`, `feeAmount` |
| Claim fields written | `resultCode`, `feeAmount` and `status`; the other six are read |
| Requests and answers | `InvoiceRequest` in and `Invoice` out on API-S9-006; the multipart result and its files in and `PartnerInstruction` out on API-S9-005 |
| Required flags | `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt` and `status` on the instruction, with `id` read-only |
| Lists | LOV-INSTRUCTION, LOV-INSTR-STATUS, LOV-PANEL and LOV-PARTNER-TYPE, copied from TSD S9 T3.2 |
| Event data | EV-21 `caseId`, `instructionId`, `resultCode`, `resultedAt` |
| Provider data | The asset record and `v_ace_npa_asset` (S5, P1), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), `payment` (P8): named, never declared |
| Not published | A cost table, a cost line element and a value set for `resultCode` (GAP-3134; ASM-5483) |

The field-level types, lengths and required flags are those of TSD S9 T3.1 and the API Specification; this story fixes the element names, the flags of AC2 and the absence of AC3. **No new table, no new column and no migration** is declared.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/partner/instructions/{instructionId}/results` (API-S9-005) | Multipart `result` and `files` in, `PartnerInstruction` out | Partner portal, right U, scope applied | `Idempotency-Key` |
| POST | `/partner/instructions/{instructionId}/invoices` (API-S9-006) | `InvoiceRequest` in, `Invoice` out | Partner portal, right C, scope applied | `Idempotency-Key` |
| GET | `/partner/instructions` (API-S9-003) | Query `status`, `page`, `size`; `InstructionPage` out for the caller's firm | Partner portal, right R, scope applied | Not applicable |

API-S9-003 answers 401, 403 with MSG-P4-002 and 503. API-S9-005 answers 401, 403, 404, 409, 415, 422 with MSG-GEN-001 and 503. API-S9-006 answers 401, 403, 404, 409, 422 and 503. Each carries the error envelope and one message ID of section 14. The paths, requests, answers and error sets are TSD S9 T-A.1 and T-A.2's; the fields of the two invoice elements are not published there and that absence is recorded (GAP-3134; ASM-5483). The other three operations of the module — API-S9-001, API-S9-002 and API-S9-004 — are RWB-S9-AD022-CON's and are not restated here.

#### 12.2 REST operations consumed

None. The right is enforced by the platform guard and the assets the claim refers to arrive as identifiers, so no consumed operation and no read of another service is declared. The plan's contract-dependency row is empty and DP-08 is not in its pattern set, so the guard is not a contract row of this key (ASM-5487).

#### 12.3 Events published

| Event | Name | Payload | Consumed by |
|---|---|---|---|
| EV-21 `PartnerResultSubmitted` | `rwb.partner.PartnerResultSubmitted.v1` | `caseId`, `instructionId`, `resultCode`, `resultedAt` | The case-owning service, rwb-litigation, rwb-asset and rwb-reporting |
| `DecisionRecorded` (library, DP-03) | `rwb.decision-record.v1` | The record reference, the decision code, the rule id and its version | rwb-decision, which seals it in the central ledger |

Both go through the outbox, the CloudEvents envelope and the retry and `.dlt` topics (DP-09). The pair of the service is EV-20 `InstructionIssued` and EV-21, and only EV-21 is the claim's; EV-20 is named and not declared. No invoice and no approval event exists in the pair, so none is declared (GAP-3134; ASM-5488). The app story builds the events; this baseline publishes the schema.

#### 12.4 Events consumed

None. The service places and receives work through REST on its own base and reads no other service's topic in the ownership rows. A consumer group, a subscription or an inbox row added here fails the absence test of AC5.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction | `rwb-partner` in namespace `rwb-recovery` | Input: the instruction, the case reference and the firm; signals: accept, result, costApproval, recall, contract end; outcome: the instruction status |

`InstructionWorkflow` is the one workflow in the ownership rows; this baseline declares the workflow and its signal surface only and registers no activity and no Schedule. The `costApproval` signal is the claim's approval step and has no REST operation behind it (GAP-3134; ASM-5484).

#### 12.6 Schedules

None. This baseline declares no Temporal Schedule, no Quartz row and no shared job table; the service's job list is empty in the ownership rows (Jobs: None).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| partner_instruction | S9 (`rwb_partner`) | The claim and its approval; the source of the claim element |
| partner | S9 (`rwb_partner`) | The firm that claims the cost; read only through this baseline |
| partner_user | S9 (`rwb_partner`) | The caller's account and its firm; published by no element here |
| decision_record | PLT library, in `rwb_partner` | The local hash-linked record of a claim and an approval (DP-03) |
| idempotency_key | PLT library, in `rwb_partner` | The key and the stored answer of the two mutations |
| outbox_event | PLT library, in `rwb_partner` | The relay row of EV-21 |

The asset record and `v_ace_npa_asset` (S5, P1), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6) and `payment` (P8) are not owned: the document names them and declares none of their fields, and no foreign key leaves the schema (DP-01). No cost table exists and none is declared (BR6).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Partner-portal right and identity fake | Right R, C and U per operation, a caller of one firm, and a caller with no right | AC4, AC6 |
| gateway-bff and partner-gateway fake | SCR-35 and PRT-02 to PRT-04 with the firm of the caller only, before and after an approval | AC6 |
| Decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6 |
| rwb-document upload fake (P5) | A stored document reference and a 415 for a disallowed type | AC6 |

The fakes are test-only and are replaced by the real services in SIT; RWB-ITG-E7017-ITG swaps them for the owners and pins the contract version of each hop.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 0 consumed | API-S9-003, API-S9-005 and API-S9-006 on `/api/recovery/partner/v1`; one hop, 2 s |
| Kafka | 1 published + the library's record event, 0 consumed | EV-21 on `rwb.partner.events.v1` with the retry and `.dlt` topics; `rwb.decision-record.v1` from the library |
| Temporal | 1 workflow declared, 0 registered | `InstructionWorkflow` on `rwb-partner` with the `costApproval` signal; no Schedule and no activity |
| File | The result file and the invoice attachment of a claim | Uploaded to rwb-document through its owner; the service keeps the reference |

### 13. Solution plan

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is a prohibition: the document declares no `v_ace_*` path or property and the service holds no grant, so the asset of a claim is an identifier and the asset record is S5's (ASM-5486). DP-13 moves the two legacy paths and gives the three operations their home, and DP-19 sits behind SCR-35 and PRT-02 to PRT-04. DP-09, which the outbox carries, DP-14, which the topic name carries, and DP-08, which the rights carry, are not in the pattern set, so their absence is recorded (GAP-3134; ASM-5487, ASM-5488).

1. Write the three operations and the additive rule of AC1 into the pipeline.
2. Fix the claim element with its nine fields and the flags of AC2, and the two invoice elements with the fields their owner publishes.
3. Record the absence of a cost table and a cost line, and name the evidence file of rwb-document (AC3).
4. Publish the rights (AC4), the one event schema (AC5), the four fakes with the drift test (AC6) and the naming baseline, the tables and the boundary (AC7).
5. Tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-partner-cost-v1.yaml`, the EV-21 schema, the contract README row of the absence, and the four fakes of 12.8. **Done when** the fragment validates in the pipeline, the seven contract tests pass, the fakes answer every path and the drift test is green, and the app story, the screens, the edge contract and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation (X1) | Enter {field}. |
| MSG-P4-002 | The role lacks the partner-portal right the operation declares (X5) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before a claim or an approval is answered | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are the legacy and FSD set of RWB-E7-017 (MSG-GEN-001, MSG-P4-002) plus the exception flow AC-EXC-S9-014-02 of FSD S9 A2.14.4.3; the text is copied unchanged and no message is added.

### 15. Screens and states

The contract serves SCR-35 Placement and allocation for the claim and the approval, SCR-34 Partner list for the firm, PRT-02 Instruction and PRT-03 Upload result for the partner, and PRT-04 Invoice for the fee; all arrive through the gateway-bff composite route and, outside the bank, the partner gateway of FAPI 2.0 (FSD S9 Screens; Arch v5 slide 8; INT-24). The legacy screen table gives SCR-34 and SCR-35 "Loading; list"; PRT-02 to PRT-04 are named by the FSD and carry no legacy state, and the composite route specification and the screen field lists belong to RWB-PLT-N001-CON.

No source publishes a screen for the approval or the refusal, so the place and the wording of the approval state are Not specified in the source documents (GAP-3134; ASM-5485). The refusal, duplicate, invalid-answer and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-017-01 | AC1, AC2 | Contract | An instruction with a cost claim; the two mutations and the read answer with the instruction's own fields and right |
| TC-E7-017-02 | AC5, AC2 | Contract | A recorded claim; one EV-21 schema with its four payload fields and the envelope, and the stop at the record |
| TC-E7-017-03 | AC4 | Contract | A role without the partner-portal right; the 403 with MSG-P4-002 of the envelope |
| TC-E7-017-04 | AC3, AC7 | Contract | No cost table, no cost line element, no asset element, no consumed operation and no second topic |
| TC-S9-E7017-CON-01 | AC1 | Contract | The document validates; the three operations, the base, the rights, the `Idempotency-Key` rule and the error sets |
| TC-S9-E7017-CON-02 | AC2 | Contract | The nine instruction fields, the six required flags, the four lists and the two invoice elements |
| TC-S9-E7017-CON-03 | AC4, AC5 | Contract | The 29 identities, the three rights, the EV-21 schema, the topic with its retry and `.dlt` topics |
| TC-S9-E7017-CON-04 | AC6, AC7 | Contract | The four fakes match the document, a drifted fake fails the build, and the naming baseline and the boundary hold |

The four legacy cases are those of RWB-E7-017 in their legacy order, carried as the contract half: their Covers column names the criterion that fixes the surface each one exercises, and the business outcome is proved by RWB-S9-E7017-APP and end to end by RWB-ITG-E7017-ITG. The legacy level maps to `Contract` here because the artefact under test is the contract. The four cases `TC-S9-E7017-CON-01` to `-04` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story.

### 17. Guardrails

- No business value in the contract: the states, the types, the rights, the cost codes and the amount stay reference data and rule rows, never a schema default.
- No personal data in a schema, an event, an example or a fake: identifiers, codes, dates, amounts and list values only, and every example is synthetic.
- The claim, the invoice and the firm stay with rwb-partner: the document declares no case, asset, document, payment or ACE property (DP-01).
- ACE data and the asset only through their owners: no `v_ace_*` path, no view property and no asset element is declared (DP-05, BR10).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-partner and re-publishes no other baseline's operations (BR9).
- No approval route is invented: where no operation exists, the contract says so and the signal is declared in 12.5.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results | `feeAmount`, the invoice pair and the claim element | TC-E7-017-01, TC-S9-E7017-CON-02 |
| REQ-S9-001 | Every partner type is managed on the same six points, contract and fees among them | The claim element and the panel list | TC-E7-017-01 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the three operations | TC-S9-E7017-CON-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E7017-CON-04 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The EV-21 schema and the outbox row | TC-S9-E7017-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three operations and their error sets | TC-E7-017-03 |
| ADR-022 | Local decision record plus central ledger | The record row and the library's event | TC-E7-017-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-017, disposition Split (rework); legacy feature FEAT-PRM-14 (FSD S9 A2.14) |
| Legacy criteria | AC2 belongs to RWB-S9-E7017-APP and AC1 to RWB-ITG-E7017-ITG; this baseline copies neither |
| Wave and release | Wave 4 and release 31 May 2027 (tentative), copied unchanged; EP07 is wave 4 and the service's Arch v5 wave is 4, so no W-MAP conflict is raised (ASM-5490) |
| Legacy endpoints | The legacy result and instruction paths move to `/api/recovery/partner/v1` under DP-13; the invoice write is added from TSD S9 T-A.1 |
| Source text | Legacy RWB-E7-017; FSD S9 Partner management v3 A1.1, A1.2, A2.14 and Screens; TSD S9 Partner management v2 T0.2, T2, T3.0, T3.1, T3.2, T3.3, T5.1, T5.3, T6.1, T6.2, T8, T-A |
| Test cases | The four legacy cases as the contract half, and the four new cases TC-S9-E7017-CON-01 to -04 |
| Feature and screens | FEAT-PRM-14 and FEAT-AST-07; SCR-35, SCR-34 and PRT-02 to PRT-04 |
| Rules | BR-S9-014, VR-S9-014-1 and the four lists of TSD S9 T3.2 |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the operations, the fee check and the approval: RWB-S9-E7017-APP.
- The end-to-end proof of the claim through the real contracts: RWB-ITG-E7017-ITG.
- The firm element, the partner read, the issue and the accept operations: RWB-S9-AD022-CON.
- The held asset, its holding cost, the work order and the provision step: rwb-asset (S5) and FEAT-AST-07.
- The fields of `InvoiceRequest` and `Invoice` beyond the API Specification's, the cost line, and the value set of `resultCode`: Not specified in the source documents (GAP-3134; ASM-5483).
- The fee schedule, the panel and the service levels as reference data: FEAT-PRM-02 and the panel change FEAT-ADM-07.
- The payment of a released invoice and its posting: rwb-payment (P8).
- The rights as code, the partner's sign-in and the FAPI 2.0 token: rwb-access (P4) and the partner gateway.
- The gateway-bff composite route and the screen field lists of SCR-35, SCR-34 and PRT-02 to PRT-04: RWB-PLT-N001-CON.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
