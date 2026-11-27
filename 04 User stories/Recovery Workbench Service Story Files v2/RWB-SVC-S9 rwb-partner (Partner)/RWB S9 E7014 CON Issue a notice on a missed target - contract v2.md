# RWB-S9-E7014-CON Issue a notice on a missed target - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7014-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-S9-E7014-CON-16) |
| Contract version | API Specification v5 rwb-partner.yaml, path version /v1 (DOR-RWB-S9-E7014-CON-23) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the partner notice of rwb-partner, split from RWB-E7-014. It fixes the instruction operations on `/api/recovery/partner/v1` (DP-13) — `POST /cases/{caseId}/instructions` (API-S9-002) as the surface the notice is submitted on, with the `Idempotency-Key` header, API-S9-003 and API-S9-001 as the reads — the `Partner`, `PartnerInstruction`, `InstructionRequest`, `InstructionAcceptance` and `InstructionPage` elements over DF-PRT-001 to DF-PRT-016, the four lists of TSD S9 T3.2, the rights of TSD S9 T6.1, the error envelope, the consumed rows of rwb-comms and rwb-case, the events EV-20 and EV-21, the decision-record element of DP-03, the fakes and the absence tests. No source owns the notice in S9, publishes a notice or target property, gives the cure period a length or the target a threshold, and EV-21 is published in TSD S9 T5.3 while the event catalogue reads it as consumed; the `partner_user` table has no field list and no partner route set exists (GAP-3128; ASM-5450, ASM-5451, ASM-5452, ASM-5453, ASM-5454, ASM-5459). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E7014-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (10 resolved, 12 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the partner notice of rwb-partner — the instruction operations on `/api/recovery/partner/v1`, the partner and instruction elements with their required flags and lists, the notice and the reference data as consumed rows, the decision-record element with the rule ID and the version, the events, the rights and the fakes**, so that **the app story, SCR-34 and SCR-35 and the wave 4 harness build against one fixed, testable contract on Day 1, and a panel status, a list value, a consumed row or an answer shape can never drift between rwb-partner, rwb-comms, rwb-case and rwb-decision without a failing build**.

This baseline declares shapes and moves nothing. It owns:

- one OpenAPI 3.1 document for `/api/recovery/partner/v1` with API-S9-001, API-S9-002 and API-S9-003;
- the elements of the panel and of the instruction, the required flags and the four lists of TSD S9 T3.2;
- the two consumed rows: the notice of rwb-comms and the reference data of rwb-case, each with a fake and a placeholder where the sources are silent;
- the events of the service: EV-20 published and EV-21 consumed, with the direction conflict recorded;
- the decision-record element of DP-03 and the naming baseline of the service;
- the error envelope, the rights and the absence tests.

It does not own: the behaviour of the notice (RWB-S9-E7014-APP), the cross-service journey of AC1 (RWB-ITG-E7014-ITG), the notice document and its dispatch (rwb-comms), the case and its clock (rwb-case), the rule rows (rwb-decision), the accept, results and invoice operations (RWB-S9-E6033, RWB-S9-E6035) and the deployment of the service (the operations story of this legacy key).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy feature crossed four boundaries at once — the partner panel of the service, the target and the cure period held as reference data, the notice, which the module FSD gives to P6, and a screen — and the legacy endpoint table named the instruction operations rather than any notice operation. The target splits them: rwb-partner owns the panel and the instruction, rwb-comms owns the notice, rwb-case owns the case, its clock and the parameters, and rwb-decision owns the rule row. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_comms`, `rwb_case` or `rwb_decision`, so DP-05 is declared as a prohibition and DP-01 as the schema rule.

Five points are carried as gaps and assumptions rather than decided quietly: the notice is a rwb-comms row and the notice and target properties have no source, so they carry the placeholder (ASM-5450, ASM-5453); no partner route set exists, so the rule ID and the version the record carries have no row (ASM-5451); the target and the cure period are reference data of rwb-case with no parameter name and no value, and DP-07 is absent from the pattern set (ASM-5452, ASM-5459); EV-21 is published in TSD S9 T5.3 and consumed in the event catalogue (ASM-5454); and the `partner_user` table the ownership rows give the service has no field list in TSD S9 T3.1.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's, `notice` is P6's, `document` is P5's, `payment` is P8's and every `v_ace_*` view is P1's. This document never declares another service's table or operation as its own.
- The operations are published: TSD S9 T-A.1 gives API-S9-001 `GET /partners`, API-S9-002 `POST /cases/{caseId}/instructions`, API-S9-003 `GET /partner/instructions`, API-S9-004 accept, API-S9-005 results and API-S9-006 invoices with their access and idempotency rules, and T-A.2 gives the request and answer elements, the purpose, the errors and the `Idempotency-Key` header.
- The rwb-comms notice contract and the rwb-case reference-data read are published with their fakes. Their operation names and the notice's property for a partner are Not specified in the source documents (GAP-3128; ASM-5450, ASM-5459).
- The `partner` and `partner_instruction` tables arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration. `partner_user` is listed as owned and has no field list (ASM-5453).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-partner for the three operations: API-S9-001, API-S9-002 and API-S9-003, with their requests, answers, rights, idempotency and errors.
2. Fix the `Partner` element over DF-PRT-001 to DF-PRT-007 and the `PartnerInstruction` element over DF-PRT-008 to DF-PRT-016, with the required flags of T3.1 and the lists of T3.2 published unchanged.
3. Fix `InstructionRequest`, `InstructionAcceptance` and `InstructionPage`, and record that no property of any of them carries a notice, a target or a cure period.
4. Record the notice row as consumed from rwb-comms with its placeholder, and the target and the cure period as consumed from the reference data of rwb-case with their placeholder.
5. Record the decision-record element of DP-03, written before the answer, with the rule ID and the version in force, and record that no partner route set exists.
6. Record the events: EV-20 published as `rwb.partner.InstructionIssued.v1` on `rwb.partner.events.v1`, EV-21 consumed, and the direction conflict of EV-21.
7. Record the rights of the three operations from TSD S9 T6.1 and T-A.1, the naming baseline, the boundary and the rule that no value is a constant of the code.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the shapes, the lists, the scope, the error envelope, the absence of a `v_ace_*` read and of a `notice`, `recovery_case` or `timer` write, the drift between a fake and the document, and the absence of a notice operation.
10. Tag the baseline and hand it to RWB-S9-E7014-APP, to the other partner stories that share the three operations, to SCR-34 and SCR-35 and to the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row or a property has no name, list or value in the sources | The row or the property carries the placeholder and the fake is derived from the published document | None | AC3, AC6 |
| X5 | A value of a list is declared as a code enumeration taken from no source | The vocabulary test fails the build: the list is the published LOV and nothing else | None | AC2 |
| X6 | The document declares another service's operation or table as provided, a `v_ace_*` view, a `notice`, `recovery_case` or `timer` row, or a rule row | The review fails the baseline and the boundary test fails the build | None | AC3, AC7 |
| X7 | The document declares a second topic, a notice path, a Schedule, a Quartz row or a job | The absence test fails the build | None | AC4, AC7 |
| X8 | The rights of an operation are not the ones TSD S9 T6.1 and T-A.1 give it | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S9 appendices, the event catalogue and the published owner contracts of rwb-comms and rwb-case only |
| Negotiable | The example values and the internal record shape are settled in the baseline review; the base, the operations, the rights, the lists, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S9-E7014-APP, the partner stories that share the three operations, SCR-34 and SCR-35 and the wave 4 harness on Day 1, and the rwb-comms and rwb-case teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, four fakes and ten contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the partner notice of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner, partner_instruction and partner_user is S9, of recovery_case and timer is P3, of notice is P6, of decision_log_entry and rule_row is P7 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The three instruction operations are declared with their rights and errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/instructions as API-S9-002 with an InstructionRequest body in and a PartnerInstruction answer, the Idempotency-Key header, the errors 401, 403, 404, 409, 422 and 503, and the base /api/recovery/partner/v1 owned by rwb-partner
    Then it declares GET /partners as API-S9-001 with a Partner array answer and the errors 401, 403 and 503, and GET /partner/instructions as API-S9-003 with an InstructionPage answer and the same errors
    Then API-S9-003 declares no Idempotency-Key and a page and size query, and API-S9-001 declares the type and status query
    Then the answers 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then it declares no notice path, no target path and no cure-period path, and no operation of the accept, results or invoice branch is built by this baseline

  Scenario: AC2 The partner and instruction elements, their required flags and their lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S9 T3.0, T3.1, T3.2 and T-A.2
    Then the Partner element declares the seven columns of DF-PRT-001 to DF-PRT-007: id, partnerCode, partnerName, partnerType, panelStatus, contractEnd and score
    Then the PartnerInstruction element declares the nine columns of DF-PRT-008 to DF-PRT-016: id, caseId, partnerId, instructionType, instructedAt, dueAt, status, resultCode and feeAmount
    Then the required flags are id, partnerCode, partnerName, partnerType and panelStatus on the partner, and id, caseId, partnerId, instructionType, instructedAt and status on the instruction, with id read-only and the other properties optional
    Then the lists are LOV-PARTNER-TYPE AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC, LOV-PANEL ACTIVE, ON_NOTICE, SUSPENDED and EXITED, LOV-INSTR-STATUS SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED, and LOV-INSTRUCTION COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST and SELL, copied from TSD S9 T3.2 and published unchanged
    Then the InstructionRequest, InstructionAcceptance and InstructionPage elements declare no notice property, no target property and no cure-period property, and their notice-carrying property is Not specified in the source documents (GAP-3128; ASM-5453)
    Then the document declares no property for a notice, a document, a target, a threshold, a cure period, a rule row, an ACE extract or a case state

  Scenario: AC3 The notice and the reference data are declared as consumed and the boundary is fixed (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack and with FSD S9 T5.2
    Then the notice is declared as consumed from P6 rwb-comms, carrying the fields DF-LEG-015 to DF-LEG-023 of the legacy notice row, and its operation name is Not specified in the source documents (GAP-3128; ASM-5450)
    Then the target and the cure period are declared as consumed from the reference data of P3 rwb-case at their version in force, per the R3 default ruling, and their parameter names and values are Not specified in the source documents (GAP-3128; ASM-5452, ASM-5459)
    Then the document declares no v_ace_* path or property, no notice property, no recovery_case property, no timer property, no rule_row property and no grant on any rwb_* schema of another owner
    Then each consumed row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)
    Then the panel status is declared as a property of the answer with LOV-PANEL as its only vocabulary, and the rule ID and the version of the decision-record element are Not specified in the source documents because no partner route set exists (GAP-3128; ASM-5451)

  Scenario: AC4 The events are declared with their direction and the conflict is recorded (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with Event and Messaging Design v5 and with TSD S9 T5.3
    Then the topic is rwb.partner.events.v1 with its retry and .dlt topics, and the published event is rwb.partner.InstructionIssued.v1 with the payload instructionId, partnerId, type and dueOn
    Then the consumed event is rwb.partner.PartnerResultSubmitted.v1 with the payload instructionId, result and documents, declared consumed from the partner portal as Event and Messaging Design v4 gives it
    Then the conflict between the catalogue, which reads EV-21 as consumed, and TSD S9 T5.3, which lists it as published, is recorded and the baseline declares one direction only (GAP-3128; ASM-5454)
    Then the document declares no event of the notice and no second topic, and no producer group or consumer group of a step other than the instruction and result steps

  Scenario: AC5 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T-A.1, T-A.2 and T6.1
    Then API-S9-002 declares Partner portal right C with the scope applied, and API-S9-001 and API-S9-003 declare Partner portal right R with the scope applied
    Then the seven identities that hold right C are RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT and RW-AGENCYMG, and they are the seven the legacy permission table names
    Then the 29 identities of the Partner portal column hold right R, and they are the legacy table's eight roles and its "and 21 more" (ASM-5456)
    Then the PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER and PT-RAMC identities hold RU and are refused right C, so a partner never issues an instruction or a notice
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC6 The decision-record element and the four fakes answer the document (new, D-RCV-60)
    Given the record and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per notice with the partner reference, the case reference, the rule ID and the version in force, the score, the target, the notice reference, the from and the to panel status
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the answer leaves the service, and the MSG-P7-003 path is declared
    Then the rwb-comms notice fake answers a notice reference, the rwb-case reference-data fake answers the target, the cure period and the panel list, the decision-record stub answers a healthy and a stopped chain, and the gateway-bff fake answers the merged SCR-34 answer before and after the notice
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline, the tables and the boundary are fixed and no Schedule is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1 with its retry and .dlt topics, the queue is rwb-partner in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_instruction and partner_user, and the library objects decision_record, idempotency_key and outbox_event, and notice, recovery_case, timer, decision_log_entry, rule_row, document and payment are named as other owners' and consumed only through their contracts
    Then the field list of partner_user is declared as Not specified in the source documents (GAP-3128; ASM-5453) and no property of it is invented
    Then the document declares no Schedule, no Quartz row and no job, because the ownership rows give the service none and the cure expiry is P3's timer
    Then the absence test fails a build that adds a notice path, a second topic, a Schedule, a job, a v_ace_* read or a notice, case or timer write (ASM-5450, ASM-5452)

  Scenario: AC8 Each business rule BR1 to BR13 of section 8 is tested by a contract test (new, D-RCV-60)
    Given the business rules BR1 to BR13 of section 8 with their sources
    When each rule is compared with the criteria AC1 to AC7 and with the test cases of section 16
    Then each rule BR1 to BR13 is held by at least one criterion and at least one test case, and the coverage line of section 8 lists TC-S9-E7014-CON-08 against each
    Then TC-S9-E7014-CON-08 checks BR1, BR2, BR3, BR4, BR5, BR6 and BR7 against the elements, the consumed rows, the decision-record element, the LOV-PANEL vocabulary and the events of AC2 to AC4
    Then TC-S9-E7014-CON-08 checks BR8, BR9, BR10 and BR11 against the Idempotency-Key header, the personal-data scan of every schema, example and fake, the base and topic names and the additive-change rule
    Then TC-S9-E7014-CON-08 checks BR12 and BR13 against the operation list and the rights of AC5
    Then the architecture constraints BR8 to BR12 are also held by the boundary test of AC3 and AC7, so a build that breaks one of them fails
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-E7014-APP and copy no criterion of the legacy story, whose AC2 stays with the app story word for word and whose AC1 belongs to RWB-ITG-E7014-ITG. The baseline fixes a surface; it issues no notice, requests no notice and moves no panel status (ASM-5450, ASM-5455).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The panel and the instruction are rwb-partner's, and the contract declares the fields, the required flags and the lists on the `Partner`, `PartnerInstruction`, `InstructionRequest`, `InstructionAcceptance` and `InstructionPage` elements only | TSD S9 T3.1, T3.2, T-A.2; context pack ownership rows (tables `partner`, `partner_instruction`, `partner_user`) |
| BR2 | The notice is rwb-comms' and the contract declares it as a consumed row with a fake; it declares no notice property, no notice path and no notice value | FSD S9 T5.2; Event and Messaging Design v5 events EV-13 and EV-14; ASM-5450 |
| BR3 | The target and the cure period are reference data of the owner the R3 default ruling names (rwb-case), declared as one consumed row with a fake and a placeholder | Template and Rules §R3 default rulings; ASM-5452, ASM-5459 |
| BR4 | No partner route set exists: the contract declares no rule row, no rule package and no rule ID set, and the rule ID and the version of the decision-record element carry the placeholder | Business Rules and Routing Logic v4 (no R-PRM rows; R-UNI-25 to R-UNI-29 are the nearest); ASM-5451 |
| BR5 | The panel status of the answer is over LOV-PANEL and nothing else, and the contract declares no other vocabulary for it | TSD S9 T3.2; ASM-5455 |
| BR6 | EV-20 is published as `rwb.partner.InstructionIssued.v1` and EV-21 is consumed as `rwb.partner.PartnerResultSubmitted.v1`; the direction conflict is recorded and no second topic is declared | Event and Messaging Design v5; TSD S9 T5.3; ASM-5454 |
| BR7 | No event of the notice is declared: the notice's facts are rwb-comms' | Event and Messaging Design v5 events EV-13 and EV-14; ASM-5454 |
| BR8 | API-S9-002 declares the `Idempotency-Key` header and stores its answer; API-S9-001 and API-S9-003 declare no key and are safe to repeat | TSD S9 T-A.2 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, dates, list values, an amount, a rule ID and a version only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S9 T6.2 |
| BR10 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR12 | The document lists only operations owned by rwb-partner; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11; context pack ownership rows (6 REST operations) |
| BR13 | The rights are the Partner portal rights of TSD S9 T6.1 and T-A.1: C on API-S9-002, R on API-S9-001 and API-S9-003, and no partner-side identity holds C | TSD S9 T6.1, T-A.1; legacy permission table of RWB-E7-014; ASM-5456 |

Coverage by test case (DOR-RWB-S9-E7014-CON-4): BR1 TC-E7-014-01, TC-S9-E7014-CON-02, TC-S9-E7014-CON-08; BR2 TC-E7-014-02, TC-S9-E7014-CON-03, TC-S9-E7014-CON-08; BR3 TC-S9-E7014-CON-03, TC-S9-E7014-CON-08; BR4 TC-S9-E7014-CON-03, TC-S9-E7014-CON-08; BR5 TC-S9-E7014-CON-02, TC-S9-E7014-CON-08; BR6 TC-S9-E7014-CON-04, TC-S9-E7014-CON-08; BR7 TC-S9-E7014-CON-03, TC-S9-E7014-CON-08; BR8 TC-S9-E7014-CON-01, TC-S9-E7014-CON-08; BR9 TC-S9-E7014-CON-05, TC-S9-E7014-CON-08; BR10 TC-S9-E7014-CON-01, TC-S9-E7014-CON-08; BR11 TC-S9-E7014-CON-01, TC-S9-E7014-CON-08; BR12 TC-S9-E7014-CON-01, TC-E7-014-04, TC-S9-E7014-CON-08; BR13 TC-E7-014-03, TC-S9-E7014-CON-05, TC-S9-E7014-CON-08.

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operations, the elements, the lists, the consumed rows, the events, the record element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the partner stories that share the three operations, SCR-34, SCR-35, the wave 4 harness and the owners of rwb-comms, rwb-case and rwb-decision accept the document and the fakes | Baselined |
| Baselined | The notice property is confirmed | The business lead and rwb-comms name the property, the notice type and the operation inside major version 1 | Baselined |
| Baselined | The target and the cure period are confirmed | The reference-data owner names the parameters and publishes the values inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional notice reference on the instruction answer | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a panel status becomes a set the list does not hold | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC1, AC3, AC4 and AC7 fail: a notice path, a second topic, a Schedule, a job, a `v_ace_*` read, a notice write or a rule row | In review |

The state machine the document describes is the app story's: LOV-PANEL is `ACTIVE`, `ON_NOTICE`, `SUSPENDED` and `EXITED`, and the notice step writes `ON_NOTICE` only. This baseline fixes the vocabulary and the answer shape and moves no partner.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the confirmed notice property, the confirmed reference-data parameters and the correction of the plan's C row |
| Business lead | Confirms the notice property that replaces the placeholder, the notice type of a partner notice, the target, the cure period and the reading of `partner_user` |
| Consuming teams (the app story, the partner stories that share the three operations, SCR-34, SCR-35, the wave 4 harness and the owners of rwb-comms, rwb-case and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-partner login (DP-02)" and is not part of this baseline. The partner gateway of the DMZ (FAPI 2.0) fronts this service for the partner's own users and is the edge's, not this baseline's. The authorise check of rwb-access (DP-08) governs the three operations of API-S9-001 to API-S9-003; its name is Not specified in the source documents (DOR-RWB-S9-E7014-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Partner element | The seven columns of DF-PRT-001 to DF-PRT-007: `id`, `partnerCode`, `partnerName`, `partnerType`, `panelStatus`, `contractEnd` and `score` | DF-PRT-001 to DF-PRT-007 |
| Instruction element | `PartnerInstruction`: the nine columns of DF-PRT-008 to DF-PRT-016: `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt`, `dueAt`, `status`, `resultCode` and `feeAmount` | DF-PRT-008 to DF-PRT-016 |
| Request elements | `InstructionRequest` for API-S9-002, `InstructionAcceptance` for API-S9-004 and `InstructionPage` for API-S9-003, with the paging of the platform | Not specified in the source documents (DOR-RWB-S9-E7014-CON-7) |
| Required flags | `id`, `partnerCode`, `partnerName`, `partnerType` and `panelStatus` on the partner, and `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt` and `status` on the instruction, with `id` read-only; the other properties optional | DF-PRT-001 to DF-PRT-016 |
| Lists | LOV-PARTNER-TYPE, LOV-PANEL, LOV-INSTR-STATUS and LOV-INSTRUCTION, copied from TSD S9 T3.2 and published unchanged | Not specified in the source documents (DOR-RWB-S9-E7014-CON-7) |
| Event data | EV-20 `InstructionIssued` published and EV-21 `PartnerResultSubmitted` consumed, with the payloads of 12.3 and 12.4 (§12.3, §12.4) | Not specified in the source documents (DOR-RWB-S9-E7014-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the answer, with the rule ID and the version in force (DP-03) | DF-DEC-001 to DF-DEC-018 |
| Case, timer and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` and DF-WRK-027 to DF-WRK-036 of `timer` in P3, and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here | DF-CAS-001 to DF-CAS-023, DF-WRK-027 to DF-WRK-036, DF-REF-001 to DF-REF-015 |
| Notice | DF-LEG-015 to DF-LEG-023 of `notice` in P6: `id`, `case_id`, `document_id`, `notice_type`, `sent_date`, `barcode` and three further fields the legacy table does not name | DF-LEG-015 to DF-LEG-023 |
| Table with no field list | `partner_user` is S9's and TSD S9 T3.1 gives it no column: its field list is Not specified in the source documents (GAP-3128; ASM-5453) | Not specified in the source documents (DOR-RWB-S9-E7014-CON-7) |
| Consumed fields with no source | The notice operation name and the partner-notice property, the reference-data parameters and values, and the rule ID and version of the record: Not specified in the source documents (GAP-3128; ASM-5450, ASM-5452, ASM-5459) | Not specified in the source documents (DOR-RWB-S9-E7014-CON-7) |
| Not declared here | `notice` (P6), `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `payment` (P8) | Not specified in the source documents (DOR-RWB-S9-E7014-CON-7) |

The field-level types, lengths and required flags of the declared elements are those of TSD S9 T3.1; this story fixes the element names, the required flags of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/instructions` (API-S9-002) | `InstructionRequest` in, `PartnerInstruction` of status 201 out, carrying the instruction, the due date and the status; the operation the notice of FEAT-PRM-11 is submitted on | Partner portal, right C, scope applied | `Idempotency-Key` header |
| GET | `/partner/instructions` (API-S9-003) | `InstructionPage` out over the query status, page and size, holding the instructions placed with the caller's firm | Partner portal, right R, scope applied | Not applicable |
| GET | `/partners` (API-S9-001) | `Partner[]` out over the query type and status, holding the panel with its panel status and score | Partner portal, right R, scope applied | Not applicable |

API-S9-002 answers 400, 401, 403 with MSG-P4-002, 404 for a case outside the scope, 409 for a partner off the panel or already on notice, 422 with MSG-GEN-001 for a missing or unlisted value, and 503, each with the error envelope and one message ID of section 14. API-S9-001 and API-S9-003 answer 401, 403 and 503. The paths, the operation IDs, the request and answer element names, the rights and the error codes are published in TSD S9 T-A.1 and T-A.2; the notice, the target and the cure period have no operation, no path and no property in any source, so they carry the placeholder (GAP-3128; ASM-5450, ASM-5453). API-S9-004 accept, API-S9-005 results and API-S9-006 invoices share the base and belong to the result and invoice stories; none of them is built or narrowed here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The notice request (operation name Not specified in the source documents (GAP-3128; ASM-5450)) | `/api/recovery/comms/v1` | P6 rwb-comms | The contractual notice of a partner with its type, its template, its document and its dispatch; answers the notice reference; faked |
| The reference-data read at its version (operation name Not specified in the source documents (GAP-3128; ASM-5459)) | `/api/recovery/case/v1` | P3 rwb-case | The target, the cure period and the panel list at their version in force, per the R3 default ruling that gives parameters and reference data to rwb-case; faked |

Both rows are one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). They are contract dependencies of class C that the plan's C row does not carry, and DP-07, the reference-data pattern, is not in the pattern set of the key; the absence is recorded (GAP-3128; ASM-5450, ASM-5459). No rule-package row is declared: no partner route set exists in the Business Rules and Routing Logic v4, so the rule ID and the version the record carries have no row to read (GAP-3128; ASM-5451).

#### 12.3 Events published

One event is declared, and it belongs to the instruction step rather than to the notice.

| Event | Topic and name | Payload | Consumers | Declared for |
|---|---|---|---|---|
| EV-20 `InstructionIssued` | `rwb.partner.events.v1`; `rwb.partner.InstructionIssued.v1`, CloudEvents envelope, schema `rwb_partner_instruction_issued` | `instructionId`, `partnerId`, `type`, `dueOn` | The partner portal | API-S9-002, whose behaviour is RWB-S9-E6031-APP and RWB-S9-E6034-APP; this baseline fixes the shape and the producer group |

The notice step publishes nothing: the notice's facts are rwb-comms' (`NoticeGenerated` EV-13, `NoticeDispatched` EV-14), the partner panel change is this service's own row, and the baseline declares no event of the notice, no outbox row of the step and no second topic. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays the event is the DP-09 dependency the plan does not carry (GAP-3128; ASM-5454).

#### 12.4 Events consumed

| Event | Topic and name | Producer | Payload | Declared for |
|---|---|---|---|---|
| EV-21 `PartnerResultSubmitted` | `rwb.partner.events.v1`; `rwb.partner.PartnerResultSubmitted.v1` | The partner portal, through the external gateway (INT-24) | `instructionId`, `result`, `documents` | API-S9-005 and its result step, which is RWB-S9-E6033-APP; not the notice step |

Event and Messaging Design v4 lists EV-21 as consumed from the partner portal, TSD S9 T5.3 lists `PartnerResultSubmitted` as published, and the context pack's ownership rows give the service both EV-20 and EV-21; the baseline declares one direction, records the conflict and does not build a producer for it (GAP-3128; ASM-5454). The notice step consumes no event: its trigger is the manager's confirmation and the FSD declares no background event for the feature (FSD S9 A2.11.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per partner instruction; the notice step rides it | `rwb-partner` | The case reference, the partner reference and the instruction in; the panel status and the notice reference out |
| `issuePartnerNotice` | Activity, the one notice step | `rwb-partner` | The partner reference, the case reference, the score, the target, the cure period and the notice type in; the notice reference, the panel status and the record reference out |
| the stage outcome for the parent | Parent-child workflow edge to `CaseWorkflow` | `rwb-case` | The panel status and the notice reference as the stage result; no REST row is declared for the case move |

The service owns one workflow and no job in the context pack's ownership rows, and TSD S9 T4 gives it no case state machine of its own, so the case stage, its clock and the cure-period timer stay with rwb-case. The activity name is a target design choice fixed by no source document, and nothing of it is registered by this story. The workflow ID form of `InstructionWorkflow` and its start rule (start or signalWithStart, duplicate-start policy) are Not specified in the source documents (CG-ALL-12065).

#### 12.6 Schedules

None. The service owns no job in the context pack's ownership rows (Jobs: None), the notice is an officer-driven step, and the cure expiry of the app story's BR9 is the case stage's timer in P3. This baseline therefore declares no Temporal Schedule, no Quartz row, no shared job table and no batch table.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| partner | S9 (`rwb_partner`) | The panel firm, its code, its name, its type, its panel status, its contract end and its latest score; the table the partner element is drawn from |
| partner_instruction | S9 (`rwb_partner`) | The work placed with a partner on a case with its type, its due date, its status, its result and its fee; the table the instruction element is drawn from |
| partner_user | S9 (`rwb_partner`) | The partner's own users; the table is owned and has no field list in TSD S9 T3.1, so no property is declared (GAP-3128; ASM-5453) |
| decision_record | PLT library, created in `rwb_partner` | The local hash-linked decision record of the notice (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of API-S9-002 and the answer it holds |
| outbox_event | PLT library, created in `rwb_partner` | The library object that relays EV-20; the notice step declares no row in it (§12.3) |

`notice` (P6), `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5) and `payment` (P8) are not owned by this baseline; it names them only as consumed answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-comms notice fake | A notice reference for a partner notice of the type requested, with its template and its sent date | AC3, AC6 |
| rwb-case reference-data fake | The target, the cure period and the panel list at their version in force | AC2, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answer for the panel of a manager, before and after the notice | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The notice operation, the partner-notice property and the reference-data parameters carry the placeholder until their owners confirm them (GAP-3128; ASM-5450, ASM-5453, ASM-5459).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | API-S9-001, API-S9-002 and API-S9-003 on `/api/recovery/partner/v1`; the notice request of rwb-comms and the reference-data read of rwb-case; one hop, 2 s |
| Kafka | 1 published, 1 consumed | `rwb.partner.InstructionIssued.v1` on `rwb.partner.events.v1` and `rwb.partner.PartnerResultSubmitted.v1` consumed; no event of the notice, and the decision record rides the library's topic `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `InstructionWorkflow` and `issuePartnerNotice` on `rwb-partner`; the stage outcome to `CaseWorkflow` on `rwb-case`; no Schedule and no job |
| File | None | No file is read, built or delivered here; the notice document and its dispatch are rwb-comms' |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no partner, no instruction, no notice and no rule row. What it publishes is one OpenAPI 3.1 document, nine contract tables and four fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the answer. DP-13 moves the base of the legacy `/api/recovery/v1` paths and gives the three operations their home. DP-19 sits behind SCR-34 and SCR-35, whose screen model is the edge contract's. DP-07 and DP-06 are not in the pattern set: the target and the cure period are declared as a consumed reference-data row with a fake rather than through the published rwb-case contracts of FEAT-PRM-02, and the lists are published as values of TSD S9 T3.2 (GAP-3128; ASM-5452, ASM-5459). DP-05 is declared as a prohibition: this service holds no `v_ace_*` grant. DP-09 is absent because the notice step publishes no event, and the outbox that relays EV-20 is the instruction stories' dependency.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries. The two consumed rows of §12.2 are class C dependencies in fact and the plan's C row is empty, so they are built against their documents and fakes on Day 1 with the placeholder; DP-07 would add `RWB-PLT-E1043-CON` and `RWB-P3-E1043-CON` and DP-06 would add `RWB-PLT-E1042-CON` and `RWB-P3-E1042-CON`, and neither is added.

**Deliverables and build steps**

1. Write the three operations of `/api/recovery/partner/v1` and validate the additive rule of AC1 in the pipeline.
2. Write the `Partner` and `PartnerInstruction` elements with their required flags and the four lists of AC2.
3. Write `InstructionRequest`, `InstructionAcceptance` and `InstructionPage`, with the notice, target and cure-period properties left to the placeholder.
4. Record the two consumed rows of AC3 with their owners, their budgets and their placeholders, and the prohibition on `v_ace_*` and on the other services' tables.
5. Record the events of AC4, the direction of EV-21 and the conflict.
6. Record the rights and the error envelope of AC5.
7. Record the decision-record element of AC6 and validate it against the library schema.
8. Publish the four fakes of AC6 and the drift test.
9. Record the naming baseline, the tables owned and the absence tests of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-partner-v1.yaml`, the five elements, the contract README rows for the two consumed rows and their placeholders, and the four fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the ten contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the partner stories, SCR-34, SCR-35 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request is absent or invalid, or a value is outside its list, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Partner portal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the answer leaves the service | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| the refusal of a partner off the panel | The partner is at `SUSPENDED` or `EXITED`, its contract has ended, or it is already at `ON_NOTICE` | Not specified in the source documents (GAP-3128; ASM-5455) |

The three IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The fourth row is the refusal of the app story's X3 and has no message in any source, so it carries the placeholder.

### 15. Screens and states

The contract serves SCR-34 Partner list and SCR-35 Placement and allocation in their list state, before and after the notice, through the gateway-bff composite route (DP-19). The route calls rwb-partner for the partner, its panel status, its contract end and its score, and rwb-case for the case and its stage; this baseline fixes the rwb-partner answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The partner's own screens PRT-01 to PRT-04 are served by the partner gateway of the DMZ and read API-S9-003 on the partner's scope.

The legacy screen table gives SCR-34 and SCR-35 "Loading; list", so both are list screens and neither is a notice form: no source describes a notice form or a cure-period panel, so the place of the notice action and the return of the panel status after the cure period are Not specified in the source documents (GAP-3128; ASM-5455). The refusal, the not-in-force, the bad-value and the not-recorded states read the messages of section 14 on the same route.

SCR-34 Partner list states: loading (legacy screen table: Loading; list); empty, error and no access: Not specified in the source documents (CG-ALL-12068).

SCR-35 Placement and allocation states: loading (legacy screen table: Loading; list); empty, error and no access: Not specified in the source documents (CG-ALL-12069).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-014-01 | AC1, AC2 | Contract | The `Partner` and `PartnerInstruction` elements of `PRT-0007`; the contract half answers the three operations, the required flags and the four lists |
| TC-E7-014-02 | AC3, AC6 | Contract | The consumed notice and reference-data rows with their placeholders and fakes; the contract half answers the decision-record element and the MSG-P7-003 path |
| TC-E7-014-03 | AC5 | Contract | A role without right C and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E7-014-04 | AC3, AC7 | Contract | The two absent operations; the contract half answers the absence of a notice path, of a `v_ace_*` read, of a notice, case or timer write, of a Schedule and of a job |
| TC-S9-E7014-CON-01 | AC1 | Contract | The document validates; the three operations, the base, the `Idempotency-Key` rule and the eight error answers are present |
| TC-S9-E7014-CON-02 | AC2 | Contract | The two elements validate with seven and nine properties, the eleven required flags, the four lists and the absent notice, target and cure-period properties |
| TC-S9-E7014-CON-03 | AC3 | Contract | The two consumed rows and their placeholders; the no-`v_ace_*`, no-notice, no-case, no-timer and no-rule-row boundary |
| TC-S9-E7014-CON-04 | AC4 | Contract | EV-20 and EV-21 with their payloads on `rwb.partner.events.v1`; the one direction of EV-21 and the recorded conflict; no second topic |
| TC-S9-E7014-CON-05 | AC5, AC6 | Contract | The rights, the seven holders of C, the 29 holders of R, the error envelope, the decision-record element and the four fakes against the library schema |
| TC-S9-E7014-CON-06 | AC6, AC7 | Contract | The drift test fails on a drifted fake; the naming baseline, the tables owned, the `partner_user` placeholder and the absence of a Schedule and a job |
| TC-S9-E7014-CON-07 | AC3, AC6 | Contract | The six tables of §12.7 with their owners and the not-owned list; the contract half proves each table name and owner and that no foreign key leaves the schema (DP-01) |
| TC-S9-E7014-CON-08 | AC8 | Contract | The business rules BR1 to BR13 of section 8 against the document, the schemas, the examples and the fakes; the contract half answers each rule with a pass or a fail |

The four legacy cases are those of RWB-E7-014 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S9-E7014-APP and by RWB-ITG-E7014-ITG for AC1. The legacy level maps to `Contract` here because the artefact under test is the contract. The eight cases `TC-S9-E7014-CON-01` to `-08` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the panel list, the partner type list, the target, the cure period, the rule ID and the version stay reference data and rule values, never a schema default, an enumeration member taken from no source or a constant of the code.
- No personal data in a schema, an example or a fake: partner identifiers, codes, list values, dates, an amount, a rule ID and a version only, and every example is synthetic.
- ACE data only through the owner's contract: the document declares no `v_ace_*` path, no `v_ace_*` property and no ACE table, and this service holds no `v_ace_*` grant.
- The notice stays with rwb-comms: the document declares no notice property, no notice path and no notice value (BR2).
- The case and the clock stay with rwb-case: the document declares no `recovery_case` property, no `timer` property, no case write and no Schedule (BR3).
- The rule rows stay with rwb-decision: the document declares no rule row, no package and no rule ID set (BR4).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-partner; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that adds a notice path, a second topic, a Schedule, a Quartz row or a job.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-PRM-11 | The requirement this feature serves is Not specified in the source documents (GAP-3128; ASM-5458): TSD S9 T8 maps REQ-S9-001 to REQ-S9-009 to FEAT-PRM-01 and FEAT-PRM-08 | The three operations, the two elements, the consumed rows and the events | TC-E7-014-01, TC-S9-E7014-CON-01, TC-S9-E7014-CON-02 |
| REQ-S9-001 (nearest) | Every partner type is managed on the same six points, notice and exit among them | The instruction surface and the panel status of the partner element | TC-E7-014-01 |
| REQ-S9-008 | Partners exchange data through the partner portal and the external gateway, and not by email | The partner portal access of the three operations and the partner gateway | TC-S9-E7014-CON-05 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E7014-CON-06 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the CloudEvents envelope of EV-20 and EV-21 | TC-S9-E7014-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-S9-E7014-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S9-E7014-CON-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-014, disposition Split (rework); feature FEAT-PRM-11 |
| Legacy criteria | AC2 is owned word for word by RWB-S9-E7014-APP and AC1 by RWB-ITG-E7014-ITG; this baseline copies none of them |
| Source text | Legacy RWB-E7-014; FSD S9 Partner management v3 A1.2, A1.4, A2.11, A2.11.2, A2.11.3.1 to A2.11.3.3 and the Screens table; TSD S9 Partner management v2 T1, T2, T3.0, T3.1, T3.2, T3.3, T4, T5.2, T5.3, T6.1, T6.2, T8 and T-A; Business Rules and Routing Logic v4 (no R-PRM rows; R-RES-27 and R-UNI-25 to R-UNI-29 nearest); Event and Messaging Design v5 events EV-13, EV-14, EV-20 and EV-21; Epics 3 to 8 Specification v3 row FEAT-PRM-11 and its endpoint table |
| Test cases | The four legacy cases as the contract half, and the six new contract cases TC-S9-E7014-CON-01 to -06 |
| Feature and screens | FEAT-PRM-11, SCR-34 Partner list and SCR-35 Placement and allocation; the partner's own screens PRT-01 to PRT-04 through the partner gateway |
| Rules | No partner route set exists, so no rule ID is declared and the value carries the placeholder (ASM-5451) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the notice branch, the target comparison, the decision record and the answer: RWB-S9-E7014-APP.
- The cross-service journey of AC1 across the panel, the notice and the case: RWB-ITG-E7014-ITG.
- The notice document, its template, its dispatch and its delivery proof: rwb-comms (P6), whose row this baseline declares as consumed and faked.
- The case of record, its stage, its clock and the cure-period timer: rwb-case (P3). The `decision_log_entry` ledger and the rule rows: rwb-decision (P7).
- The operation names, properties and values of the target, the cure period and the notice: their owners confirm them at the baseline review and the placeholder stands until then (GAP-3128; ASM-5450, ASM-5452, ASM-5453, ASM-5459).
- The field list of `partner_user`: no source gives one, and the placeholder stands (GAP-3128; ASM-5453).
- The direction of EV-21 beyond the one the baseline declares: the event catalogue and TSD S9 T5.3 disagree and the conflict is recorded (GAP-3128; ASM-5454).
- The accept, results and invoice operations of the same base: RWB-S9-E6033-APP and RWB-S9-E6035-APP.
- The scorecard that publishes the score: FEAT-PRM-08 (RWB-S9-E7011-APP). The panel, the fee schedule and the service levels as reference data: FEAT-PRM-02 (RWB-S9-E6030).
- The gateway-bff composite route and the screen field list of SCR-34 and SCR-35: RWB-PLT-N001-CON and the edge stories. The partner gateway of the DMZ: the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
