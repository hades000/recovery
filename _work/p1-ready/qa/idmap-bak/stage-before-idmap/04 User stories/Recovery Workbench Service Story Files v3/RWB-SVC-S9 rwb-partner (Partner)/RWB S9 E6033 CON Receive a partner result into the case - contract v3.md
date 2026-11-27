# RWB-S9-E6033-CON Receive a partner result into the case - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the contract slice of legacy RWB-E6-033 for the partner service is split out. It freezes the two operations the legacy story lists, the multipart result shape, the instruction and result vocabularies, the `PartnerResultSubmitted` envelope, the access rule, the idempotency rule and the fakes, so that the rwb-partner build (RWB-S9-E6033-APP), the partner gateway and the rwb-case consumer can all start on Day 1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E6033-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S9-E6033-CON |
| Readiness decisions | RD-P1-007, RD-P1-064 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-033 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S9-E6033-CON-16) |
| Contract version | v1 (base path /api/recovery/partner/v1) |
| Early contract publication | InstructionWorkflow, EV-20 and EV-21 published as a contract ahead of wave 4 for dependent builds against the fake (GAP-1845) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Added the partner-owned REST ledger append, its key and the matching EV-21 header. RD-P1-064.


### 1. Story

As a **contract owner of the partner service**, I want **the published contract of the partner result intake — the two operations and their shapes, the instruction and result vocabularies, the `PartnerResultSubmitted` envelope on the service topic, the access and idempotency rules and the fakes — instead of the monolith's in-process partner interface and its portal-consumed event**, so that **rwb-partner, the partner gateway and the rwb-case consumer build from Day 1 against one frozen contract**.

This is the contract slice of legacy RWB-E6-033 (FEAT-PRM-05). The two operations are published here once as the E4 partner instruction contract; the allocation and result features FEAT-PRM-03 and FEAT-PRM-05 consume them, and the allocation rules arrive in E6. It owns **no legacy acceptance criterion**: AC1 and TC-E6-033-01 are the journey owned by `RWB-ITG-E6033-ITG`, AC2 and TC-E6-033-02/04 belong to `RWB-S9-E6033-APP`, and the access case **TC-E6-033-03** is executed against the rule this contract declares. Every criterion in section 7 is new under D-RCV-60 and tests only the deliverable in the title.

### 2. Business rationale

The monolith had three things this contract replaces. The endpoints were on the monolith's one base with the partner portal as a calling tenant (legacy section 7); the result came back into the module as an event the module consumed from the portal (EV-21); and the shape of the submission lived in code, not in a document. Architecture v5 changes the edge and the transport: partners reach the partner gateway, FAPI 2.0, which fronts S9 (slide 8), and every service answers on its own base `/api/recovery/partner/v1` with its own topic `rwb.partner.events.v1` (§R4, DP-13). The fact then travels to rwb-case as a published event, not as a consumed portal event, because the case is another service's row.

The contract has to exist before either side is written. The portal team needs the multipart shape and the error set to build the submission screen; rwb-case needs the envelope, the key and the payload to build its consumer; and the app slice needs one place where "a result is the result code plus its documents, keyed on the case" is written down. The access rule is part of the contract because a partner user must never read another firm's instruction: right U on the intake and right R on the list, with the scope filter applied by the caller (NFR-050; TSD S9 T6.1). The idempotency rule is part of it because the legacy portal retried: one `Idempotency-Key` is one result, one record and one event (R-UNI-40).

The fake is the Day-1 unblocker: the app slice and the rwb-case consumer both build and test against it before the other side exists (Template and Rules §R5.4 class C). No business value is invented: the states, the instruction types, the panel states, the error statuses and the messages are TSD S9 T3.2 and T-A.2, FSD S9 A2.5 and the legacy story, character for character.

### 3. Preconditions

- The partner gateway (FAPI 2.0) fronts rwb-partner and no other path reaches the service from outside the bank (Architecture v5 slide 8).
- The base is `/api/recovery/partner/v1` and the topic is `rwb.partner.events.v1`, per the naming rule of §R4; the service short name is `partner`, so the event name is `rwb.partner.PartnerResultSubmitted.v1`.
- The operations and their errors are those of TSD S9 T-A.1 and T-A.2 (API-S9-003 and API-S9-005); the legacy partner resources `/partner/instructions` and its `/results` child move to the new base unchanged in name (DP-13).
- The vocabularies are those of TSD S9 T3.2: LOV-INSTR-STATUS (`SENT`, `ACCEPTED`, `DECLINED`, `IN_PROGRESS`, `DONE`, `RECALLED`), LOV-INSTRUCTION (`COLLECT`, `FILE_SUIT`, `ENFORCE`, `APPRAISE`, `REPOSSESS`, `LIST`, `SELL`), LOV-PANEL (`ACTIVE`, `ON_NOTICE`, `SUSPENDED`, `EXITED`).
- The resource fields are those of TSD S9 T3.1 (DF-PRT-008 to DF-PRT-016), and the firm and user bindings are DF-PRT-001 to DF-PRT-007 and DF-REF-212 to DF-REF-217.
- The messages MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are unchanged from FSD S9 and the legacy story; the 409, 415 and 422 bodies carry no message ID in any source, so that element is Not specified in the source documents (GAP-3115; ASM-5388).
- EV-21 is a consumed portal event in the monolith; the target publishes it from this service, with the case ID as key and subject (ASM-5389).
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7) and is published at Draft (realignment v1). FSD S9 is "In review" (ASM-5389).

### 4. Flow

1. The contract author fixes the two operations on the base: the multipart result intake and the instruction list, with their query, body, response and error sets from TSD S9 T-A.2.
2. The author fixes the resource shape of `PartnerInstruction` and `InstructionPage` from the fields of TSD S9 T3.1, and the three vocabularies from T3.2, with the rule that the members are read at their version and never written in code.
3. The author fixes the `PartnerResultSubmitted` envelope: CloudEvents 1.0 binary, `ce_type`, the key and subject rule, the payload fields and the rule that the payload carries identifiers and references only.
4. The author fixes the access rule and the scope: right U on the intake, right R on the list, the firm scope applied by the caller, and the refusal with MSG-P4-002.
5. The author fixes the idempotency rule: an `Idempotency-Key` header on the intake, one result per key, the repeat answered with the first result and counted.
6. The author fixes the error set and the RFC 9457 problem body, with the status mapping of section 14.
7. The lint and schema steps run: the OpenAPI validated, the examples scanned for personal data, the envelope validated against one accepted and one refused body, and the vocabulary compared with TSD S9 T3.2.
8. The fakes are generated from the document: the intake fake, the list fake, the event fixture and the writer fake, all answering from the same example set.
9. The drift test runs on every change; the document is published at v1 and the app slice and the consumer pin it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published path is not on the service base, or a resource name drifts from the TSD | The lint fails the build; the path and the resource are fixed | None | AC1 |
| X2 | A vocabulary member is published that TSD S9 T3.2 does not carry, or a list is frozen in the document as code values | The vocabulary test fails the build; the members are read at their version | None | AC2 |
| X3 | The envelope is published with another type, no key, or a personal field in the payload | The envelope validation fails the build; the type, the key and the payload rule are fixed | None | AC3 |
| X4 | An operation publishes no access rule, or a scope-free read | The lint fails the build; the rights and the scope are declared | None | AC4 |
| X5 | A fake answers something the document does not say, or a consumer ships without the drift test | The drift test fails the build | None | AC5 |
| X6 | A value the consumers need is named by no source — the multipart bound, the error bodies or the payload beyond three fields | The value is published as the working read and the gap stays open | Not specified in the source documents (GAP-3115; ASM-5388) | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document, a schema pair and fakes; builds against nothing, reads no business data, starts on Day 1 |
| Negotiable | The multipart bound, the example set and the fake names are open until v1 is frozen; the paths, the vocabularies, the envelope and the rules are fixed |
| Valuable | Unblocks the app slice, the partner gateway and the rwb-case consumer on Day 1 with one frozen contract |
| Estimable | One OpenAPI document, one AsyncAPI section, three vocabularies, one access rule, one idempotency rule and four fakes |
| Small | One sprint for the document, the schemas, the fakes and the lint rules |
| Testable | Each criterion below is one lint, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the partner result intake contract of rwb-partner

  Background:
    Given the contract document is published with major version 1
    Given the service base is /api/recovery/partner/v1 and the topic is rwb.partner.events.v1
    Given the contract declares no other path and no topic of its own

  Scenario: AC1 The two operations and their shapes are published (new, D-RCV-60)
    Given the operations section of the document
    When it is validated and linted
    Then it publishes POST /partner/instructions/{instructionId}/results with a multipart body of the result and its files, answering PartnerInstruction, with errors 401, 403, 404, 409, 415, 422 and 503
    Then it publishes GET /partner/instructions with the query status, page and size, answering InstructionPage, with errors 401, 403 and 503
    Then both paths sit under the base and both carry the Idempotency-Key rule on the intake only
    Then PartnerInstruction carries the fields of TSD S9 T3.1, DF-PRT-008 to DF-PRT-016, with their types and lists
    Then the problem body of every error is RFC 9457 with a status, a messageId where a source names one, and an instance

  Scenario: AC2 The three vocabularies are the TSD lists read at their version (new, D-RCV-60)
    Given the vocabulary section of the document
    When it is compared with TSD S9 T3.2
    Then LOV-INSTR-STATUS carries SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED
    Then LOV-INSTRUCTION carries COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST and SELL
    Then LOV-PANEL carries ACTIVE, ON_NOTICE, SUSPENDED and EXITED
    Then no operation accepts a value outside its list and no member is declared as a constant of the build

  Scenario: AC3 The PartnerResultSubmitted envelope is fixed (new, D-RCV-60)
    Given the envelope section of the document
    When one result is validated against it
    Then the event is rwb.partner.PartnerResultSubmitted.v1 on rwb.partner.events.v1 in CloudEvents 1.0 binary mode with ce_specversion, ce_id, ce_type, ce_source, ce_subject, ce_time and the trace header
    Then rwb-partner (S9) publishes the event and holds the result as its own row; the dated DP06 to DP08 copies are read-only data products of P1 built from its events
    Then the record key and ce_subject are the case ID of the instruction
    Then the payload carries the instruction ID, the result and the document references
    Then the payload carries no personal data, no free text and no document content
    Then the registry holds one accepted schema version and refuses a body that does not match it

  Scenario: AC4 The access rule and the firm scope are declared (new, D-RCV-60)
    Given the access section of the document
    When a caller is checked against it
    Then the intake requires Partner portal U and the list requires Partner portal R, both with the scope applied by the caller
    Then a role without the right is refused with MSG-P4-002 and nothing is read
    Then a caller of another firm receives 404 on the intake and reads no instruction of that firm
    Then the partner gateway is the only outside route and the bank staff route is the composite route

  Scenario: AC5 The fakes answer the document and the drift test binds both sides (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the intake fake, the list fake, the event fixture and the writer fake
    Then the intake fake accepts a valid submission, answers 409 for a closed instruction, 404 for a foreign firm, 415 for a wrong body and 422 for a refused element
    Then the intake fake answers a repeated Idempotency-Key with the first result and marks the repeat
    Then the event fixture holds one event per result keyed on the case ID and refuses a payload with a personal field
    Then the drift test of the app slice and of the consumer fails on any difference from section 12

  Scenario: AC6 The tables named by the contract sit in rwb_partner only (new, D-RCV-60)
    Given the tables owned section of the document
    When its tables are checked against DP-01 and the schema boundary
    Then every table of section 12.7 sits in rwb_partner and is owned by S9
    Then no schema, login, table of another service or foreign key across a service boundary is declared

  Scenario: AC7 A value named by no source is published as the working read and the gap stays open (new, D-RCV-60)
    Given a value the consumers need that no source names
    When the document publishes it
    Then it is published as the working read with GAP-3115 and ASM-5388 kept open
    Then the value is not presented as a fixed contract value

  Scenario: AC8 An activity retry and a timeout are declared as the contract allows (new, D-RCV-60)
    Given an activity of the rwb-partner result intake that is retried or times out
    When the document is checked for its retry and timeout rule
    Then the retry rule and the timeout are Not specified in the source documents (GAP-3114)
    Then no retry count or timeout value is presented as a fixed contract value
```

Every criterion is new and tests only the contract deliverable: no legacy criterion is repeated here. AC2 and TC-E6-033-02/04 stay with `RWB-S9-E6033-APP`, AC1 and TC-E6-033-01 with `RWB-ITG-E6033-ITG`, and every identifier comes from the legacy story, TSD S9 or Architecture v5, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The service publishes two operations on `/api/recovery/partner/v1` and nothing else for this feature; the legacy base is not kept | DP-13; TSD S9 T-A.1; Architecture v5 slide 8 |
| BR2 | The intake body is multipart — the result and its files — and answers the instruction resource; the list answers a page | TSD S9 T-A.2, API-S9-005 and API-S9-003 |
| BR3 | The three vocabularies are read at their version; a member outside its list is refused, and no member is a constant of a build | TSD S9 T3.2; FSD S9 BR-S9-005 |
| BR4 | `PartnerResultSubmitted` is published on `rwb.partner.events.v1` in CloudEvents 1.0 binary mode, keyed and subject on the case ID, from the outbox in the caller's transaction | DP-03, DP-13; Architecture v5 slides 12 and 42 |
| BR5 | The intake requires Partner portal U and the list Partner portal R, with the firm scope applied; a foreign firm sees 404 and a role without the right MSG-P4-002 | NFR-050; TSD S9 T6.1 |
| BR6 | One `Idempotency-Key` is one result, one record and one event; the repeat returns the first answer and is counted | TSD S9 T-A.2; R-UNI-40 |
| BR7 | A result carries identifiers, a result code and document references only; the payload holds no personal data and no document content | legacy guardrail; Architecture v5 slide 22 |
| BR8 | A published version is never edited: a backward-compatible change stays in major version 1, a breaking change raises version 2 | Template and Rules §R7.2; §R5.4 class C |

### 9. State transitions

The contract fixes the instruction vocabulary and the transitions the intake may take; the implementation behind them is `RWB-S9-E6033-APP` section 9.

| From | Event | Condition | To |
|---|---|---|---|
| `SENT` | Accept | The partner accepts on the accept operation | `ACCEPTED` |
| `SENT`, `ACCEPTED`, `IN_PROGRESS` | Result submitted | A valid submission and a written record | `DONE`, `result_code` set |
| `DONE`, `DECLINED`, `RECALLED` | Result submitted | The instruction is closed | No change; 409 |
| Any open state | Result submitted, record fails | The record cannot be written | No change; MSG-P7-003 |
| Any open state | Decline | The partner declines on the accept operation | `DECLINED` |
| Any open state | Recall | The recall rule of the panel story | `RECALLED` |

`DONE` and `result_code` are set in one statement, so the vocabulary holds no state in which an instruction is done without a result. The accept, decline and recall operations are declared by the panel and allocation contracts, not by this one.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the schemas, the rules and the fakes |
| The partner service owner (S9) | Approves a breaking change, freezes a version and confirms the two operations |
| The case service owner (P3) | Confirms the consumer side: the envelope, the key and the payload it applies to the case |
| The access owner (P4) | Confirms the two rights, the scope and the MSG-P4-002 refusal |
| The platform edge owner | Confirms the partner gateway route and the composite route the staff screens use |
| RW-AUDIT, RW-COE | Read the published contract and the versions pinned by each service |
| No delegation of authority level applies | A service contract is a technical artefact, not a credit decision |

No personal name, email address or credential appears in the document, an example or a fake; where a caller must be named, the example uses a role code or a user identifier only.

The rwb-access authorise check that the two operations apply is Not specified in the source documents (DP-08; DOR-RWB-S9-E6033-CON-6).

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The document publishes paths, element names, codes, status values, error statuses and message identifiers; no customer, account or case value appears | Not specified in the source documents (DOR-RWB-S9-E6033-CON-7) |
| Resource shape published | `PartnerInstruction` over DF-PRT-008 to DF-PRT-016, `InstructionPage` over the same fields, and the multipart submission of the result and its files | Not specified in the source documents (DOR-RWB-S9-E6033-CON-7) |
| Vocabularies published | LOV-INSTR-STATUS, LOV-INSTRUCTION and LOV-PANEL of TSD S9 T3.2, referenced as values read at their version; the reference data is read under DP-06 and DP-07, and the parameters it reads are Not specified in the source documents (DOR-RWB-S9-E6033-CON-20) | Not specified in the source documents (DOR-RWB-S9-E6033-CON-7) |
| Personal data | None. A caller is a role code or a user identifier; no partner user identity, name, account number or document content appears | Not specified in the source documents (DOR-RWB-S9-E6033-CON-7) |
| Tables named | `partner_instruction`, `partner` and `partner_user` as the shapes the resources map to; all three are S9's in `rwb_partner` | Not specified in the source documents (DOR-RWB-S9-E6033-CON-7) |
| Retention | Not published here: the instruction and its result follow the retention of the partner records, which is Not specified in the source documents (GAP-3115; ASM-5388) | Not specified in the source documents (DOR-RWB-S9-E6033-CON-7) |

The document fixes that a result is a code and a set of document references, never a document body and never a customer field; the storage of the files is rwb-document's and is out of scope.

The `ce_` names are CloudEvents 1.0 attributes of the envelope, not LDM v9 fields, and `decision_record` is the local decision-record library named in API Specification v6, not an LDM v9 or Data Classification v5 entity (DOR-RWB-S9-E6033-CON-7).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). Every error is an RFC 9457 problem body.

| Method | Path | Request | Response | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/partner/instructions/{instructionId}/results` (API-S9-005) | Multipart: result, files | `PartnerInstruction`; errors 401, 403, 404, 409, 415, 422, 503 | Partner portal U, scope applied | `Idempotency-Key` header |
| GET | `/partner/instructions` (API-S9-003) | Query: status, page, size | `InstructionPage`; errors 401, 403, 503 | Partner portal R, scope applied | Not applicable |

| Element | Published rule |
|---|---|
| `PartnerInstruction` | The fields of DF-PRT-008 to DF-PRT-016 with their types and lists, the result code and the status |
| `InstructionPage` | The instruction rows of the caller's firm with their status and due date, paged |
| Multipart bound | Not specified in the source documents (GAP-3115; ASM-5388); the document publishes the working read and the app slice enforces it |
| Problem body | `status`, `messageId` where a source names one, `detail`, `instance`; the 409, 415 and 422 carry no message ID (GAP-3115; ASM-5388) |

#### 12.2 REST operations consumed

After the local result commits, rwb-partner appends the result through POST /api/recovery/source-data/v1/cases/{caseId}/interactions under its workload identity with eventCode PARTNER_RESULT, actorType PARTNER, actorRef the partner code, channel PORTAL and business key EV-21-<caseNo>-<yyyyMMdd>-<actionId>. Send a UUID Idempotency-Key and reuse it on an identical retry. The same business key is carried in ce_idempotencykey of PartnerResultSubmitted. The event serves its existing consumers. P1’s Kafka intake does not append this event (RD-P1-064 rule 9; ASM-5391). The lists and version in force still come from the template client library.

#### 12.3 Events published

PartnerResultSubmitted carries ce_idempotencykey equal to the REST append business key. The contract fake covers the PARTNER_RESULT append and replay.

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| `rwb.partner.PartnerResultSubmitted.v1` (EV-21) | `rwb.partner.events.v1` | `caseId` | instruction ID, the result (result code), the document references | Announces the result to rwb-case, which applies it to the case, and to rwb-reporting |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary |
| ce_specversion | 1.0 |
| ce_type | `rwb.partner.PartnerResultSubmitted.v1` |
| ce_source | rwb-partner |
| ce_subject and key | The case ID of the instruction |
| ce_id and traceparent | The event identifier and the W3C trace context of the call |
| Payload | The three documented elements only; identifiers and a code, no personal data and no document content |

EV-21 is documented as a consumed portal event (Event and Messaging Design v4); the target publishes it from this service once the portal ingress is the REST operation, and the case ID is added as key and subject so the consumer needs no second call (ASM-5389). The payload beyond the three documented elements is Not specified in the source documents (GAP-3115; ASM-5389).

#### 12.4 Events consumed

None. Nothing on a topic starts this feature.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction; the one workflow the S9 ownership row carries | `rwb-partner`, namespace Not specified in the source documents (CG-ALL-11876) | Signal `resultSubmitted` with the instruction ID and the result reference; the stage ends and the outcome is reported to the parent `CaseWorkflow` of rwb-case |

The contract fixes the signal name and its two elements because a workflow signal is an interface between the app slice and the case stage; the activity names behind it are the app slice's choice and are not declared here (GAP-3115; ASM-5388).

Workflow ID form and start rule: Not specified in the source documents (CG-ALL-11877; DOR-RWB-S9-E6033-CON-8).

#### 12.6 Schedules

None. The intake is started by a person's submission; the instruction clock is a durable timer inside `InstructionWorkflow` and no Schedule is declared by this contract.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `partner_instruction` | `rwb_partner` | S9 | The resource the two operations read and the intake closes: DF-PRT-008 to DF-PRT-016 |
| `partner` | `rwb_partner` | S9 | The firm named on the instruction and its panel status, DF-PRT-001 to DF-PRT-007 |
| `partner_user` | `rwb_partner` | S9 | The firm and role binding of a partner user, DF-REF-212 to DF-REF-217; the scope the access rule applies |

The contract creates no schema, no login and no table in another service's schema and declares no foreign key across a service boundary (DP-01). The local `decision_record` and the outbox tables the intake writes are the platform library's in the same schema and are named in the app slice.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Intake fake | `POST /partner/instructions/{instructionId}/results` | A valid submission answering the instruction in `DONE`; a 409 for a closed instruction, a 404 for a foreign firm, a 415 for a wrong body, a 422 for a refused element; a repeated key answering the first result |
| List fake | `GET /partner/instructions` | One page of the firm's instructions with status, due date and result; an empty page; a 403 refusal |
| Event fixture | The `PartnerResultSubmitted` envelope | One event per result keyed on the case ID; a refused body with a personal field; a repeat under one key |
| Writer fake | The local decision-record library (RWB-PLT-E1027-CON) | An accepted record and a refusal with MSG-P7-003, so the refusal path is testable from Day 1 |

The fakes answer from the same example set as the document, so a change shows up as a contract-test failure in a consumer rather than as a surprise at run time.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations fixed by the contract | 0 | The intake and the list on the service base; the partner gateway outside, the composite route for staff |
| Kafka | 1 event type fixed by the contract, published by the app slice through its outbox | 0 | AsyncAPI 3.0, CloudEvents 1.0 binary, key the case ID, on `rwb.partner.events.v1` |
| Temporal | 1 workflow signal fixed by the contract | 0 | `InstructionWorkflow` on `rwb-partner`; no Schedule |
| File | 1 multipart element | 0 | The result and its files in the submission; no file is stored by this contract |

### 13. Solution plan

**Package.** Contract artefact of the partner service: an OpenAPI 3.1 document for the two operations, an AsyncAPI 3.0 section for the event, the three vocabularies as referenced value sets, and the fake set. The implementation is RWB-S9-E6033-APP; the publication channel and the artefact coordinates are Not specified in the source documents (GAP-3115; ASM-5388).

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the contract fixes the refusal the caller must honour | referred to; the app slice carries the H row |
| DP-13 | `/api/recovery/v1` | `/api/recovery/partner/v1`; the two legacy paths move to the new base unchanged in their resource names | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the contract declares no screen route, the staff route is named only | referred to; the app slice carries the H row |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `partner-result-api.yaml` | OpenAPI 3.1 document | The two operations, their bodies, responses, errors, access and idempotency (AC1, AC2, AC4) |
| `partner-events.yaml` | AsyncAPI 3.0 section | The `PartnerResultSubmitted` channel, envelope, key and payload (AC3) |
| Vocabulary set | Resource | LOV-INSTR-STATUS, LOV-INSTRUCTION and LOV-PANEL as referenced value sets read at their version (AC2) |
| Fake set | Test asset | The intake fake, the list fake, the event fixture and the writer fake (AC5) |
| Drift test | Test | Compares the app slice and the consumer with section 12 on every build (AC5) |

**Build steps.** (1) Write the two operations with their bodies, responses and errors from TSD S9 T-A.2; lint the base and the resource names (AC1). (2) Write the resource shape from TSD S9 T3.1 and the three vocabularies from T3.2; compare them line by line (AC2). (3) Write the event section and validate one accepted and one refused body (AC3). (4) Write the access rule, the scope and the refusal (AC4). (5) Generate the fakes and the drift test, and wire the test into both builds (AC5). (6) Publish v1 and record the pinned version of the app slice and of the rwb-case consumer. **Done when** the document validates, the two vocabularies match TSD S9 T3.2, the fakes answer every criterion including the refusal and the repeat, the drift test is green on both builds, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required element of the submission is empty | Enter {field}. | 422 problem body with `messageId` |
| MSG-P4-002 | The caller has no right on the operation | You cannot {action} here. Your role does not include it. | 403 problem body with `messageId` |
| MSG-P7-003 | The caller's record cannot be written and the result is not recorded | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503 problem body with `messageId`, raised by the app slice |
| Not specified in the source documents (GAP-3115; ASM-5388) | A closed instruction, a foreign firm, a wrong body type or a refused element | The 409, 404, 415 and 422 bodies carry a status, a detail and an instance but no message ID in any source | 409, 404, 415, 422 problem bodies |

The three texts are copied unchanged from RWB-E6-033, FSD S9 A2.5 and the platform error standard; this contract adds no message ID. Thai text follows DL10.

### 15. Screens and states

No screen in this story. The contract declares the two operations the portal screens call and the composite route the staff screens use, but no route, field list or layout: SCR-34 Partner list and SCR-35 Placement and allocation are read through the gateway-bff composite route (DP-19) and belong to `RWB-S9-E6033-APP` and the platform edge story.

States of SCR-34 Partner list: loading as Screen Specifications v1 section SCR-34 defines it; empty, error and no access: Not specified in the source documents (CG-ALL-11879).

States of SCR-35 Placement and allocation: loading as Screen Specifications v1 section SCR-35 defines it; empty, error and no access: Not specified in the source documents (CG-ALL-11880).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-033-03 | AC4, BR5 | Contract | A partner user of another firm on the intake, a role without Partner portal R on the list; the 404 and MSG-P4-002 answers |
| TC-S9-E6033-CON-01 | AC1, BR1, BR2 | Contract | The two operations linted against TSD S9 T-A.2; the base, the resource names, the multipart body, the paging and the error set |
| TC-S9-E6033-CON-02 | AC2, BR3 | Contract | The three vocabularies compared with TSD S9 T3.2; a member outside its list refused |
| TC-S9-E6033-CON-03 | AC3, BR4, BR7 | Contract | One accepted and one refused envelope; the key and subject; a payload with a personal field refused |
| TC-S9-E6033-CON-04 | AC5, BR6, BR8 | Component | The four fakes answering every case including the repeat and the refusal; the drift test on both builds; a breaking change raising version 2 |
| TC-S9-E6033-CON-05 | AC6 | Contract | The tables of section 12.7 checked for the schema boundary, with the boundary cases of DP-01 |
| TC-S9-E6033-CON-06 | AC7 | Contract | A value named by no source published as the working read; the gap GAP-3115 kept open |
| TC-S9-E6033-CON-07 | AC8 | Contract | An activity retried and one timed out; the retry rule and the timeout Not specified in the source documents (GAP-3114) |

The legacy identifier TC-E6-033-03 is kept because its scenario is the access rule this contract declares. TC-E6-033-01 is executed by `RWB-ITG-E6033-ITG` and TC-E6-033-02/04 by `RWB-S9-E6033-APP`; they are not copied here and no legacy id is renumbered.

### 17. Guardrails

- No business value in the contract: the vocabularies are referenced value sets read at their version, and the only literals are the legacy paths, the field identifiers and the message identifiers.
- No personal data in a schema, an example or a fake: the caller is a role code or a user identifier, and the payload scan fails the build otherwise.
- No cross-schema reference and no foreign key across services in the resource shapes; the boundary test fails the build.
- The envelope is the only event channel and the intake is the only write; the contract declares no second topic and no second path.
- No screen route, no layout and no field list is published here; the composite route is named only.
- A published version is never edited in place: a breaking change raises major version 2 with a migration note and both sides pin the version.
- The contract names no service's table as a read path: the case, the ledger and the documents are reached by their owners' contracts only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S9-008 | Partners exchange data through the portal and the external gateway, not by email — this contract fixes the portal operation behind the partner gateway | Program, 5.16 | FEAT-PRM-05 | 12 Manage partners | BR1, BR5 | TC-E6-033-03, TC-S9-E6033-CON-01 |
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results — this contract fixes the result a fee is checked against | Program, 5.16 | FEAT-PRM-05 | 12 Manage partners | BR2, BR6, BR7 | TC-S9-E6033-CON-01, TC-S9-E6033-CON-03, TC-S9-E6033-CON-04 |
| NFR-050 | Partner accounts authenticate with multi-factor and are scoped to their own cases | NF specification, NFR-050 | FEAT-PRM-05 | 12 Manage partners | BR5 | TC-E6-033-03 |

The rows are the S9 rows of the Program section 5.16 and the S9 non-functional row; FEAT-PRM-05 is the legacy feature. The legacy story carries no requirement identifiers, so none is invented.

Open decision DL10 applies to this story and is still open. Each open decision has an assumption: DL10 is carried by ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

| Story or item | Relation to this story |
|---|---|
| RWB-S9-E6033-APP | H consumer: implements both operations, the transaction, the record and the event against this contract and its fakes; owns AC2 and TC-E6-033-02/04 |
| RWB-ITG-E6033-ITG | The end-to-end proof of AC1 and TC-E6-033-01 across rwb-partner, rwb-case and the ledger |
| rwb-case (P3) | Consumer of `PartnerResultSubmitted`; confirms the envelope, the key and the payload |
| rwb-access (P4) | Confirms the two rights, the scope and the MSG-P4-002 refusal the access rule names |
| RWB-PLT-E1027-CON | The local decision-record library whose refusal the contract requires the caller to honour |
| RWB-PLT-N001-CON | The composite route the staff screens use; named only, no path declared here |
| Partner gateway (FAPI 2.0) | The only outside route to the service; its profile belongs to the edge story |

### 19. Out of scope

- The implementation — the transaction, the record, the outbox, the workflow branch and the screen fragment: `RWB-S9-E6033-APP`.
- The end-to-end proof of the arrival on the case and the ledger entry: `RWB-ITG-E6033-ITG`.
- The application of the result to the case, the case status and the task: rwb-case (P3).
- The ledger entry and the chain check: rwb-decision (P7).
- The interaction ledger row of a contact result: rwb-source-data (P1).
- The storage, OCR and retention of the result documents: rwb-document (P5).
- The accept, decline, issue and invoice operations (API-S9-002, API-S9-004, API-S9-006): the panel and allocation contracts.
- The partner gateway profile, the composite route specification and the SCR-34/SCR-35 field list and layout: the platform edge story.
- The panel, fee schedule, allocation, override, fee match and scorecard: the other S9 stories of FEAT-PRM-01 to FEAT-PRM-15.
- The physical schema files, the grants and the deployment of either build.
