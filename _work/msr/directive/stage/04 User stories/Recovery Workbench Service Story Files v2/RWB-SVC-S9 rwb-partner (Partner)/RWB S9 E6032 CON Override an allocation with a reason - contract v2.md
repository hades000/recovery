# RWB-S9-E6032-CON Override an allocation with a reason - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6032-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S9-E6032-CON-16) |
| Contract version | API Specification v5 (rwb-partner.yaml), base `/api/recovery/partner/v1` |
| Depends on (build) | None |
| Contract dependencies | Rule row of P7 rwb-decision, base `/api/recovery/decision/v1`, class C (GAP-3113; ASM-5382) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the placement override of rwb-partner, split from RWB-E6-032. It fixes the override branch of the published `POST /cases/{caseId}/instructions` (API-S9-002) on `/api/recovery/partner/v1` (DP-13) with the `InstructionRequest` of the API Specification v5 and the `PartnerInstruction` answer, the nine properties and six required flags of the instruction element over DF-PRT-008 to DF-PRT-016, the four lists of TSD S9 T3.2, one additive optional `overrideReason` property whose name and 1000-character length are the published decision-log element's, the rule row read as a consumed row, the decision-record element of DP-03 with the rule ID and the version in force, the rights of TSD S9 T6.1 and T-A.1, the fakes and the absence tests. No source publishes an override operation, an override element or a reason property on the request; no rule row or decision code names the placement override; TSD S9 T5.3 and the Event and Messaging Design v5 disagree on the direction of EV-21 and the pattern set carries no DP-09; the legacy permission table gives right U while the operation declares C; and no requirement row traces to FEAT-PRM-04 (GAP-3113; ASM-5379, ASM-5380, ASM-5381, ASM-5382, ASM-5383, ASM-5384, ASM-5387). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S9-E6032-CON-L29, X20 RWB-S9-E6032-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 8 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the placement override of rwb-partner — the override branch of the instruction operation on `/api/recovery/partner/v1`, the instruction and partner-instruction elements with their required flags and lists, the additive `overrideReason` property, the rule row as a consumed row, the decision-record element with the rule ID and the version in force, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-35 and the wave 4 harness build against one fixed, testable contract on Day 1, and a partner, a status value, a consumed row or an answer shape can never drift between rwb-partner, rwb-decision and rwb-case without a failing build**.

This is the contract slice of legacy RWB-E6-032 (FEAT-PRM-04). It owns:

- the override branch of `POST /cases/{caseId}/instructions` (API-S9-002), its request and answer elements, its right, its idempotency rule and its error set;
- the `PartnerInstruction` element over the nine columns of DF-PRT-008 to DF-PRT-016, its six required flags and the four lists of TSD S9 T3.2;
- one additive optional property on `InstructionRequest`, `overrideReason`, carrying the reason the legacy story asks for;
- the rule row of rwb-decision declared as a consumed row with a fake;
- the decision-record element of DP-03, written before the placement changes, with the rule ID and the version in force;
- the rights of the operation, the naming baseline and the fakes of section 12.8.

It does not own: the behaviour behind the branch, the two instruction rows and the screen action, which are RWB-S9-E6032-APP; the scorecard placement (RWB-S9-E6031-APP); the partner panel and fee schedule (RWB-S9-E6030-APP); the result, acceptance and invoice operations of the same base; the case of record (P3); the rule package and the ledger (P7); the deployment of the service; and the screen states of SCR-34 and SCR-35 (empty, loading, error and no access), which this contract does not declare (DOR-RWB-S9-E6032-CON-10).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy override of RWB-E6-032 crossed four boundaries at once: the placement of the case, the partner chosen, the rule version in force and a screen, and it named two endpoints that place no work at all — a read of the caller's instructions and a result post. The target splits them: rwb-case owns the case, its stage and the clock, rwb-decision owns the rule rows and the ledger, and rwb-partner owns the instruction, its partner and its status. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules §R4; context pack). It records that the service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition.

Six points are carried as gaps and assumptions rather than decided quietly: the override has no operation, element or reason property of its own and is declared as a branch of API-S9-002 with one additive property named after the published `DecisionLogEntry.overrideReason` (ASM-5380); the rule ID, the rule set and the decision code have no row in the Routing Logic set and carry the placeholder (ASM-5382); the instruction status list has no published transition table (ASM-5379); the pattern set carries no DP-09 although the service owns a topic, and the two documents disagree on the direction of EV-21 (ASM-5383); the legacy permission table gives right U while TSD S9 T-A.1 declares C, and the "21 more" and "5 more" holders are not enumerated (ASM-5384); and no requirement row traces to FEAT-PRM-04 (ASM-5387).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case` and `assignment` are P3's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's and `payment` is P8's. This document never declares another service's table or operation as its own.
- The operation is published: TSD S9 T-A.1 gives API-S9-002 `POST /cases/{caseId}/instructions` with right C and first in E4, T-A.2 gives its request, its answer, its `Idempotency-Key` and the error set 401, 403, 404, 409, 422 and 503, and the API Specification v5 publishes `InstructionRequest`, `PartnerInstruction` and `DecisionLogEntry`.
- The rwb-decision rule row is published with its fake, so the consumed row names a real owner document; it is not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3113; ASM-5382).
- The rule rows of the placement rule are governed in rwb-decision (P7); this baseline names the read and declares no rule row of its own.
- `partner_instruction` arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).
- Wave 4 and release 30 April 2027 are the plan's and are copied unchanged, the release marked tentative; EP06 is wave 4 and the service's Arch v5 wave is 4, so no wave conflict is raised (ASM-5386).

### 4. Flow

1. Draft the override branch of the OpenAPI 3.1 document of rwb-partner for API-S9-002: the operation with its request and answer elements, the override property, the right, the `Idempotency-Key` and the error responses.
2. Fix the `PartnerInstruction` element over DF-PRT-008 to DF-PRT-016, with its six required flags, the read-only `id` and the lists of TSD S9 T3.2 published unchanged.
3. Fix the `InstructionRequest` element: `instructionType`, `partnerId` and `dueOn` as published, plus one additive optional `overrideReason` whose name and length are the published decision-log element's.
4. Record that the override has no path, element or flag of its own and that the branch is declared inside API-S9-002.
5. Record the consumed row: the rule row in force of rwb-decision, with its placeholder operation name and its fake.
6. Record the decision-record element of DP-03, written before the placement changes, with the rule ID, the version in force and the reason.
7. Record the rights of the operation, the naming baseline, the boundary and the rule that no value is a constant of the code.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the shapes, the lists, the scope, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the drift between a fake and the document, and the absence of a published and of a consumed event.
10. Tag the baseline and hand it to RWB-S9-E6032-APP, to the other partner stories that share the instruction base, to SCR-35 and SCR-34, and to the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 422 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or an operation name the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC6 |
| X5 | A list value or a status is declared as a code enumeration taken from no source | The vocabulary test fails the build: the four lists are TSD S9 T3.2 and nothing else | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event published by this step, a consumed event, a second topic, a Schedule or a second reason property | The absence test fails the build | None | AC7 |
| X8 | The rights of the operation are not the ones TSD S9 T6.1 and T-A.1 give the instruction operation | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S9 appendices, the API Specification and the published owner contract of rwb-decision only |
| Negotiable | The example values and the internal record shape are settled in the baseline review; the base, the operation, the right, the lists, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S9-E6032-APP, the other partner stories of the instruction base, SCR-35, SCR-34 and the wave 4 harness on Day 1, and the rwb-decision team on the same day |
| Estimable | One OpenAPI document, nine contract tables, three fakes and five contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the placement override of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner and partner_instruction is S9, of recovery_case and assignment is P3, and of every v_ace_* view, decision_log_entry and rule_row is P1 or P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The instruction operation is declared with its override branch and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/instructions as API-S9-002 with an InstructionRequest body in and a PartnerInstruction answer of status 201, under the base /api/recovery/partner/v1 and owned by rwb-partner
    Then the override branch is declared inside API-S9-002 as the action the request carries, with no second path, no override path and no override flag of its own
    Then API-S9-002 declares the Idempotency-Key header and requires it, and a repeat is matched on that key
    Then the answers 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then no operation of the acceptance, the result, the invoice or a placement-list read is declared by this document

  Scenario: AC2 The instruction elements, the override property and the lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S9 T3.0, T3.1, T3.2 and T-A.2, and with the API Specification v5
    Then the PartnerInstruction element declares the nine columns of DF-PRT-008 to DF-PRT-016: id, caseId, partnerId, instructionType, instructedAt, dueAt, status, resultCode and feeAmount
    Then the required flags are id, caseId, partnerId, instructionType, instructedAt and status, id is read-only, and dueAt, resultCode and feeAmount are optional
    Then the lists are LOV-INSTRUCTION COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST and SELL, LOV-INSTR-STATUS SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED, LOV-PANEL ACTIVE, ON_NOTICE, SUSPENDED and EXITED, and LOV-PARTNER-TYPE AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC, copied from TSD S9 T3.2 and published unchanged
    Then the InstructionRequest element declares instructionType over LOV-INSTRUCTION, partnerId as a uuid and dueOn as a date, with the names the API Specification gives, and adds one optional overrideReason of up to 1000 characters taken from DecisionLogEntry.overrideReason
    Then the required flags of the InstructionRequest are Not specified in the source documents (GAP-3113; ASM-5380) and the override branch declares partnerId, instructionType and overrideReason as the fields it needs
    Then the document declares no reason property other than overrideReason, no override element, no override flag and no second status set
    Then the document declares no property for an officer assignment, a rule row, an ACE extract or a case state

  Scenario: AC3 The rule row is declared as consumed and the facts stay with their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the rule row is declared as consumed from P7 rwb-decision at its version in force, with its rule ID and the panel condition it carries
    Then the operation name of the row is Not specified in the source documents (GAP-3113; ASM-5382) and the row carries the placeholder and a fake
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no assignment property, no rule_row property and no grant on any rwb_* schema of another owner
    Then the row is one hop with a 2 s budget and a breaker (DP-11, ADR-020)
    Then the case move is declared on the parent-child workflow edge and not as a REST row

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T-A.1, T-A.2 and T6.1
    Then API-S9-002 declares Partner portal right C with the scope applied
    Then the seven identities of T6.1 that hold C on that area are RW-AGENCYMG (CRUDA), RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and RW-GUARANT (CRU)
    Then RW-CASEOWN, RW-TEAMMGR, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL and RW-TRIBE hold R and are refused the override, and the six PT-* portal identities hold RU and are refused it too
    Then the legacy permission table's right U, its "21 more" holders of R and its "5 more" holders of U are recorded as the narrower legacy reading and are not enumerated as new rights
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and written before the placement changes (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S9 T2
    Then one decision record is declared per override with the case reference, the instruction replaced and the instruction created, the partner replaced and the partner chosen, the rule ID that fired, the version in force, the reason as overrideReason, the deciding identity, and the from and to status
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the answer leaves the service, and a failed write leaves everything unchanged with MSG-P7-003
    Then the central decision_log_entry row is declared as appended by rwb-decision from that topic, so this document declares no write to the ledger and no rule row
    Then the record carries no personal name, no contact value and no identity number

  Scenario: AC6 The three fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-decision rule-row fake answers the placement rule at its version with its rule ID and the panel condition
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-35 placement answer and the SCR-34 partner list, before and after the override
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1 with its retry and .dlt topics, the queue is rwb-partner in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner_instruction and partner plus the library objects decision_record, idempotency_key and outbox_event, and recovery_case, assignment, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step, no consumed event, no second topic and no Schedule
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule, a v_ace_* read or a case write (ASM-5383)

  Scenario: AC8 Each business rule BR1 to BR13 is answered by a criterion or by a guardrail test (new, D-RCV-60)
    Given the business rules of section 8
    When each rule is compared with the criteria above, the rule coverage line and the guardrails of section 17
    Then every rule BR1 to BR13 is answered by the document, by a criterion above or by a guardrail test of section 17
    Then a rule that is an architecture constraint is held by the boundary and absence tests of AC6 and AC7, and a build that breaks it fails
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-E6032-APP and copy no criterion of the legacy story, whose AC2 stays with the app story word for word and whose AC1 belongs to RWB-ITG-E6032-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The instruction row is rwb-partner's, and the contract declares the fields, the required flags and the lists on the `PartnerInstruction` and `InstructionRequest` elements only | TSD S9 T3.1, T3.2, T-A.2; context pack ownership rows (tables `partner`, `partner_instruction`, `partner_user`) |
| BR2 | The override record is declared as an element written before the answer, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S9 T2; legacy AC2 |
| BR3 | The reason is declared as one additive optional `overrideReason` property of the request, with the name and the 1000-character length of the published `DecisionLogEntry.overrideReason`; no other reason property and no reason column is declared | API Specification v5; ASM-5380, ASM-5381 |
| BR4 | The rule row and the ledger are rwb-decision's: the document declares the read as consumed and declares no rule row, no threshold, no rule ID set and no ledger write | ASM-5382; TSD S9 T5.2 |
| BR5 | The override has no path of its own: it is a branch of API-S9-002 and no second operation, element or flag is declared | ASM-5380; TSD S9 T-A.1 |
| BR6 | No event of this step is declared: EV-20 `InstructionIssued` belongs to the step that first issues the instruction and EV-21 arrives from the portal, and the outbox library of DP-09 is recorded as an absent row | ASM-5383; Event and Messaging Design v5; TSD S9 T5.3 |
| BR7 | The status values are the six of LOV-INSTR-STATUS and the document declares no transition table for them: the two moves of the override are stated and the rest carries the placeholder | ASM-5379; TSD S9 T3.2 |
| BR8 | API-S9-002 declares the `Idempotency-Key` header, so a repeat answers the instruction that exists; the headers of the other operations of the base are theirs | TSD S9 T-A.2 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, dates, a list value, a rule ID, a version and a reason text only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S9 T6.2 |
| BR10 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR12 | The document lists only operations owned by rwb-partner; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11; context pack ownership rows (6 REST operations) |
| BR13 | The rights of the operation are the partner-portal right C that T-A.1 declares and T6.1 gives seven identities; the legacy U, its "21 more" and its "5 more" are recorded and the matrix is not widened | TSD S9 T6.1, T-A.1; legacy permission table of RWB-E6-032; ASM-5384 |

Rule coverage (DOR-RWB-S9-E6032-CON-4): BR1, BR3 and BR7 by TC-S9-E6032-CON-02; BR2 by TC-E6-032-04 and TC-S9-E6032-CON-04; BR4 and BR12 by TC-S9-E6032-CON-03; BR5 and BR8 by TC-S9-E6032-CON-01; BR6 by TC-S9-E6032-CON-05; BR9 and BR10 by TC-S9-E6032-CON-05; BR11 by TC-S9-E6032-CON-02; BR13 by TC-S9-E6032-CON-04. Every rule BR1 to BR13 is also covered by TC-S9-E6032-CON-07 (AC8).

### 9. State transitions

The lifecycle of this document, not of a placement:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the elements, the override property, the consumed row, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the other partner stories of the instruction base, SCR-35, SCR-34, the wave 4 harness and the owners of rwb-decision, rwb-case and rwb-access accept the document and the fakes | Baselined |
| Baselined | A business rule row is confirmed | The rule owner names the placement rule and its decision code inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional reason code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a status becomes a set the list does not hold | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC1, AC3 and AC7 fail: a second path, a `v_ace_*` view, a `recovery_case` property, a `rule_row` property, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's: `partner_instruction.status` moves from `SENT`, `ACCEPTED` or `IN_PROGRESS` to `RECALLED` and the replacement row starts at `SENT`. This baseline fixes the vocabulary and the answer shape and moves no instruction.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the additive `overrideReason` property and the correction of the plan rows the baseline consumes, including the consumed row and the absent DP-04, DP-07, DP-08 and DP-09 rows |
| Business lead | Confirms the placement rule, its decision code and the reading of the reason as free text of up to 1000 characters |
| Consuming teams (the app story, the other partner stories of the instruction base, SCR-35, SCR-34, the wave 4 harness and the owners of rwb-decision, rwb-case and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-partner login (DP-02)" and is not part of this baseline. The rwb-access authorise check that the operation calls (DP-08) is Not specified in the source documents (DOR-RWB-S9-E6032-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Instruction element | The nine columns of DF-PRT-008 to DF-PRT-016: `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt`, `dueAt`, `status`, `resultCode` and `feeAmount` | Not specified in the source documents (DOR-RWB-S9-E6032-CON-7) |
| Request element | `InstructionRequest`: `instructionType` over LOV-INSTRUCTION, `partnerId` as a uuid and `dueOn` as a date, plus the additive optional `overrideReason` | Not specified in the source documents (DOR-RWB-S9-E6032-CON-7) |
| Required flags | `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt` and `status` on the instruction element, with `id` read-only; `dueAt`, `resultCode` and `feeAmount` optional; the request's own list carries the placeholder | Not specified in the source documents (DOR-RWB-S9-E6032-CON-7) |
| Lists | LOV-INSTRUCTION (7), LOV-INSTR-STATUS (6), LOV-PANEL (4) and LOV-PARTNER-TYPE (8), copied from TSD S9 T3.2 and published unchanged | Not specified in the source documents (DOR-RWB-S9-E6032-CON-7) |
| Partner element | `partner`: `partnerCode`, `partnerName`, `partnerType`, `panelStatus`, `contractEnd` and `score` over DF-PRT-001 to DF-PRT-007, read for the panel test and never written here | Not specified in the source documents (DOR-RWB-S9-E6032-CON-7) |
| Event data | None of this step: no event is declared (§12.3) | Not specified in the source documents (DOR-RWB-S9-E6032-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the answer, with the rule ID, the version in force and the reason (DP-03) | Not specified in the source documents (DOR-RWB-S9-E6032-CON-7) |
| Case and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` and DF-WRK-009 to DF-WRK-016 of `assignment` in P3, and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here | Not specified in the source documents (DOR-RWB-S9-E6032-CON-7) |
| Not declared here | `recovery_case` and `assignment` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8) | Not specified in the source documents (DOR-RWB-S9-E6032-CON-7) |
| Consumed field with no source | The operation name of the rule-row read, the required flags of the request and the rule ID and decision code of the placement: Not specified in the source documents (GAP-3113; ASM-5380, ASM-5382); the outside-panel refusal message is Not specified in the source documents (GAP-0462) | Not specified in the source documents (DOR-RWB-S9-E6032-CON-7) |

The field-level types, lengths and required flags of the declared elements are those of the API Specification v5 and TSD S9 T3.1; this story fixes the element names, the required flags of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/instructions` (API-S9-002) | `InstructionRequest` in, `PartnerInstruction` of status 201 out, carrying the new reference, the partner, the type, the due date and the status; the override branch is the request that carries `overrideReason` | Partner portal, right C, scope applied | `Idempotency-Key` header, required |

API-S9-002 answers 401, 403 with MSG-P4-002, 404 for a case or a partner that is not there, 409 for an instruction that is not open, 422 with MSG-GEN-001 for a missing or unlisted value, and 503, each with the error envelope and one message ID of section 14. The path, the operation ID, the element names, the right, the header and the error codes are published in TSD S9 T-A.1 and T-A.2; the API Specification v5 rwb-partner.yaml does not declare this path yet, and where it is published is Not specified in the source documents (CG-ALL-11851); the override branch, the `overrideReason` property and the decision code carry the placeholder (GAP-3113; ASM-5380, ASM-5382). The acceptance (API-S9-004), the result (API-S9-005), the invoice (API-S9-006), the partner read (API-S9-001) and the instruction read (API-S9-003) of the same base belong to other stories of the module and none of them is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The rule row of the placement rule in force (operation name Not specified in the source documents (GAP-3113; ASM-5382)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule ID and the version in force, with the panel condition the override tests; read once per override; faked |

The row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). It is a contract dependency of class C that the plan's C row does not carry, and the R3 default ruling gives the rule package registry to rwb-decision; the absence is recorded (GAP-3113; ASM-5382).

#### 12.3 Events published

None. The service owns the topic `rwb.partner.events.v1` with its retry and `.dlt` topics (DP-14), and its event set carries EV-20 `InstructionIssued` (`instructionId`, `partnerId`, `type`, `dueOn`, consumed by the partner portal) and EV-21 `PartnerResultSubmitted` (`instructionId`, `result`, `documents`) (Event and Messaging Design v5; context pack events EV-20 and EV-21). EV-20 belongs to the step that first issues an instruction, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that would relay it is the platform library object of DP-09, which the pattern set for this key does not carry (GAP-3113; ASM-5383).

#### 12.4 Events consumed

None. EV-21 `PartnerResultSubmitted` is the result step's trigger and EV-20 is published by the issue step; neither belongs to the override, whose trigger is the manager's confirmation on SCR-35, and the FSD declares no background event for the feature (FSD S9 A2.4.4.4). TSD S9 T5.3 lists both events as Published while the Event and Messaging Design v5 gives EV-21 the direction Consumed; the conflict is recorded and this baseline declares no direction, no consumer group and no inbox (GAP-3113; ASM-5383).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction, can start at any time on a case, continues-as-new with the case stage | `rwb-partner` | The stage that hosts the override step; its signal and its outcome for the parent are declared, not built; workflow ID form Not specified in the source documents (DOR-RWB-S9-E6032-CON-8; CG-ALL-11855); start rule and duplicate-start policy Not specified in the source documents (CG-ALL-11855) |
| `recordPlacementOverride` | Activity, the one override step of the instruction | `rwb-partner` | The case, the instruction, the partner replaced and the partner chosen, the reason, the rule ID and the version in; the new reference, the status and the record reference out |
| the stage outcome for the parent | Parent-child workflow edge to `CaseWorkflow` | `rwb-case` | The instruction status as the stage result; no REST row is declared for the case move |

No child workflow for the case and none for the money exists in this service, and the service owns one workflow and no job in the context pack's ownership rows. The activity name is a target design choice, and the step runs from the manager's confirmation. No activity is registered by this story.

#### 12.6 Schedules

None. The override is a manager-driven step; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The service's job list is empty in the context pack's ownership rows, and the monthly scorecard and the partner review timers are other stories'.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| partner_instruction | S9 (`rwb_partner`) | The placement of work with a partner on a case, its type, its dates, its status, its result and its fee; the table the answer element is drawn from |
| partner | S9 (`rwb_partner`) | The outside firm, its code, its name, its type, its panel status, its contract end and its score; read for the panel test |
| decision_record | PLT library, created in `rwb_partner` | The local hash-linked decision record of the override (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of the operation and the answer it holds |
| outbox_event | PLT library, created in `rwb_partner` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `assignment` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6) and `payment` (P8) are not owned by this baseline; it names them only as answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01). `partner_user` belongs to this service and to the portal sign-in story.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision rule-row fake | The placement rule at its version in force with its rule ID and the panel condition | AC2, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-35 answer for the placements of `RW-2026-000512` and the SCR-34 partner list, before and after the override | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation name of the rule-row read carries the placeholder until its owner confirms it (GAP-3113; ASM-5382).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed | API-S9-002 on `/api/recovery/partner/v1`; the rule row of rwb-decision; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; EV-20 and EV-21 belong to the issue and result steps, and the decision record is the library's on `rwb.decision-record.v1` and not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `InstructionWorkflow` and `recordPlacementOverride` on `rwb-partner`; the stage outcome to `CaseWorkflow` on `rwb-case`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no placement, no partner and no rule row. What it publishes is one OpenAPI 3.1 document, nine contract tables and three fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the placement is answered. DP-13 moves the base of the legacy paths and gives the instruction operation its home. DP-19 sits behind SCR-35 and SCR-34, whose screen models are the edge contract's. DP-04, DP-05, DP-07, DP-08 and DP-09 are not in the pattern set: the rule row is declared as a consumed row rather than an embedded kit, ACE data is declared as a prohibition, the lists are published as values of TSD S9 T3.2 and not as a reference-data contract, the access guard is a template capability, and the outbox is an absent library row rather than an event of this step (GAP-3113; ASM-5382, ASM-5383).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, and the Drools kit row `RWB-PLT-E1072-CON` that a rule evaluation would add. The rule-row read is a C dependency in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the override branch of API-S9-002 and validate the additive rule of AC1 in the pipeline.
2. Write the `PartnerInstruction` element with its nine properties and six required flags, the `InstructionRequest` element and the four lists of AC2.
3. Record the additive `overrideReason` property and the statement that no other reason property and no reason column exists.
4. Record the consumed row of AC3 with its owner, its budget and its placeholder, and the parent-child edge of the case move.
5. Record the rights and the error envelope of AC4, with the legacy U and its unnamed holders as a recorded difference.
6. Record the decision-record element of AC5 and validate it against the library schema.
7. Publish the three fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-partner-v1.yaml`, the two elements, the contract README rows for the consumed row and its placeholder, and the three fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the five contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the other partner stories, SCR-35, SCR-34 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the request is absent or invalid, the partner among them, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the partner-portal right C the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the placement is answered | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-35 Placement and allocation and SCR-34 Partner list in their list state, before and after the override, through the gateway-bff composite route (DP-19). The route calls rwb-partner for the placements and the partners and rwb-case for the case header; this baseline fixes the rwb-partner answers only, and the composite route specification and the screen field lists belong to RWB-PLT-N001-CON. The legacy screen table gives both screens "Loading; list" and names no form and no dialog: the place of the override action and its field list are Not specified in the source documents (GAP-3113; ASM-5385). The empty, error and no access states of SCR-34 and SCR-35 are Not specified in the source documents (CG-ALL-11858; CG-ALL-11859), as Screen Specifications v1 also lacks them. The refusal, closed-placement, panel, absent-reason and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-032-01 | AC1, AC2 | Contract | The open placement `PI-000241` of `RW-2026-000512` on the fake; the contract half answers the operation, the elements, the override property and the lists |
| TC-E6-032-02 | AC2, AC5 | Contract | The instruction element and the override request; the contract half answers the nine properties, the lists, the decision element and the MSG-P7-003 path |
| TC-E6-032-03 | AC4 | Contract | A role without right C and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 422 of the envelope |
| TC-E6-032-04 | AC5, AC7 | Contract | The decision-record stub stopped; the contract half answers the failed-write path and the absence tests |
| TC-S9-E6032-CON-01 | AC1 | Contract | The document validates; the operation, the base, the override branch, the `Idempotency-Key` rule and the six error answers are present |
| TC-S9-E6032-CON-02 | AC2 | Contract | The two elements validate with their nine and four properties, the six required flags, the four lists, the `overrideReason` property and its placeholder |
| TC-S9-E6032-CON-03 | AC3 | Contract | The consumed rule row and its placeholder; the no-`v_ace_*`, no-`recovery_case`, no-`assignment`, no-rule-row boundary; the case move on the workflow edge |
| TC-S9-E6032-CON-04 | AC4, AC5 | Contract | The rights, the seven holders of C, the recorded legacy U, the error envelope and the decision-record element against the library schema |
| TC-S9-E6032-CON-05 | AC6, AC7 | Contract | The three fakes match the document and a drifted fake fails the build; the naming baseline, the tables owned and the absence of an event, a second topic and a Schedule |
| TC-S9-E6032-CON-06 | AC7 | Contract | The five tables of §12.7 at their boundary: the owned tables, the outside reads and the no-foreign-key boundary; a table or key outside §12.7 is refused |
| TC-S9-E6032-CON-07 | AC8 | Contract | Each rule BR1 to BR13 of section 8 against the criteria above, the rule coverage line and the guardrail tests of section 17; a rule with no criterion or guardrail is refused |

The four legacy cases are those of RWB-E6-032 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of the first is proved end to end by RWB-ITG-E6032-ITG while AC2's outcome is proved by RWB-S9-E6032-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S9-E6032-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the instruction types, statuses, panel states, partner types, the rule ID, the version and the right stay rule rows and reference data, never a schema default, an enumeration member taken from no source or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, dates, a list value, a rule ID, a version and a reason text only, and every example is synthetic.
- The case stays with rwb-case: the document declares no `recovery_case` property, no case row write and no case state write.
- The officer assignment stays with rwb-case: `assignment` is declared as another owner's and is neither read nor written.
- The rule rows and the ledger stay with rwb-decision: the document declares the read as consumed and declares no rule row, no threshold, no rule ID set and no ledger write.
- The reason is one additive optional property named after the published decision-log element; a second reason property, a reason column or an override element fails the review (BR3, BR5).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule or a Quartz row.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-PRM-04 | The requirement this feature serves is Not specified in the source documents (GAP-3113; ASM-5387): TSD S9 T8 maps REQ-S9-001 to REQ-S9-004 and REQ-S9-008 to FEAT-PRM-01 and REQ-S9-005 to REQ-S9-007 and REQ-S9-009 to FEAT-PRM-08 | The override branch of API-S9-002, the two elements and the rule row | TC-E6-032-01, TC-S9-E6032-CON-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E6032-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as a later story's | TC-S9-E6032-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The rule-row read with its budget and breaker | TC-S9-E6032-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S9-E6032-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-032, disposition Split (rework); feature FEAT-PRM-04 |
| Legacy criteria | AC2 of the legacy story, owned word for word by RWB-S9-E6032-APP; AC1 is owned by RWB-ITG-E6032-ITG; this baseline copies none of them |
| Source text | Legacy RWB-E6-032; FSD S9 Partner management v3 A1.2, A1.3, A2.4, A2.4.2, A2.4.3 and A2.4.4; TSD S9 Partner management v2 T1, T2, T3.0 to T3.3, T5.2, T5.3, T6.1, T6.2, T8 and T-A; API Specification v5 elements `InstructionRequest`, `PartnerInstruction`, `Partner` and `DecisionLogEntry`; Business Rules and Routing Logic v4 rows R-LIT-29, R-DIS-31, R-WO-35 and R-UNI-45; Event and Messaging Design v5 EV-20 and EV-21 |
| Test cases | The four legacy cases as the contract half, and the five new contract cases TC-S9-E6032-CON-01 to -05 |
| Feature and screens | FEAT-PRM-04, SCR-35 Placement and allocation, SCR-34 Partner list |
| Rules | The placement rule row is governed in rwb-decision and declares its ID and version; no row of the Routing Logic set names the override |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the branch, the two instruction rows and the screen action: RWB-S9-E6032-APP.
- The scorecard placement the override departs from: FEAT-PRM-03 and RWB-S9-E6031-APP. The panel, the fee schedule and the contract terms: FEAT-PRM-02 and RWB-S9-E6030-APP.
- The case of record, its stage, the parent `CaseWorkflow`, the route and the clock: rwb-case (P3).
- The authoring, testing, approval and versioning of the placement rule and of the rule rows, and the ledger row: rwb-decision (P7), whose row this baseline declares as consumed and faked (ASM-5382).
- The name and the decision code of the placement rule, and the transition table of the instruction status: the rule owner and the business lead confirm them, and the placeholders stand until then (GAP-3113; ASM-5379, ASM-5382).
- The acceptance, the result, the invoice, the partner read and the instruction read operations of the same base: the other stories of the module.
- The recall and re-selection rules R-UNI-25 to R-UNI-29, the notice on a missed target and the end of a contract: the partner-management stories of EP07.
- The gateway-bff composite route and the screen field lists of SCR-35 and SCR-34: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
