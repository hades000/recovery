# RWB-S9-E7015-CON End a partner contract and recall the work - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7015-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the contract-end and recall path of rwb-partner, split from RWB-E7-015. It fixes the two reads of this path, the unchanged `partner` and `partner_instruction` elements, the recall command element with its placeholders, the exit entry of the local decision record, the rights and the error set of the act, the fakes, and the three absences the path has — no operation for the contract end, no event for the recall and no Schedule — on the base `/api/recovery/partner/v1` (DP-13) behind the gateway-bff composite route (DP-19). The two table elements are declared unchanged, because no field of TSD S9 T3.1 carries a recall, and the recall is carried by `partner_instruction.status` with RECALLED and the exit by `partner.panel_status` with EXITED. The contract-end act has no published operation, the word "open" has no definition, the case-side re-selection command has no name, the refusal code for a result on a recalled instruction is unpublished and the partner service level sits on no PRM rule row (GAP-3130; ASM-5468 to ASM-5472). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the contract-end and recall path of rwb-partner — the two reads it answers, the unchanged `partner` and `partner_instruction` elements, the recall command, the exit entry, the rights and the error set, the fakes and the three absences**, so that **RWB-S9-E7015-APP, the wave 4 harness and the screens build against one fixed, testable contract on Day 1, and a field, a status value, a right or a case command can never drift between rwb-partner, rwb-case and rwb-decision without a failing build**.

The baseline is deliberately narrow: it declares two of the service's six operations, two unchanged elements, one command and one record. It declares no operation for the contract end, no event and no Schedule.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy contract end of RWB-E7-015 ran inside one process and one schema: it read the partner, the instruction and the decision log without a boundary. The target splits them: rwb-partner owns the partner and the instruction, rwb-case owns the case, its route state and its timers, rwb-decision owns the UNIVERSAL package and the central ledger, and rwb-access owns the roles, the rights and the lists of values. Each boundary is a contract another team builds against, so the shapes have to be fixed before the app story starts: the partner and its panel status, the instruction and its status set, the recall command, the exit entry and the rights of the act.

The baseline also fixes the naming the checks require: schema `rwb_partner`, login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules v1 §R4; context pack service row). It records that rwb-partner holds no grant on `rwb_case` or `rwb_decision`, so the case is commanded on the Temporal boundary and the package is loaded at its version.

Five points are carried as gaps and assumptions rather than decided quietly: no operation ends a contract, so the act has no published entry point (GAP-3130; ASM-5468); no column carries a recall, so the two elements stay as published and the recall is a status (ASM-5469); the word "open" has no definition (ASM-5470); the case-side re-selection command has no name (GAP-3130; ASM-5471); and no PRM rule row carries the partner service level, so the clock is the UNIVERSAL row R-UNI-26 with its 5 working days (ASM-5472).

The wave and the date are the plan's: this key is EP07, wave 4, release 31 May 2027, and rwb-partner is created in wave 4, so the two waves agree and the date is copied unchanged and marked tentative (U7, R7; ASM-5472).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case`, `queue`, `assignment` and `timer` are P3's, `rule_row` and `decision_log_entry` are P7's, `document` is P5's and `notice` is P6's. This document never declares another service's table or operation as its own.
- The case-side re-selection boundary is published with a fake so the command names a real owner; it is not a row of this story's dependency list, which is None, and the absence is recorded (GAP-3130; ASM-5471).
- The UNIVERSAL package and the rows R-UNI-26, R-UNI-30, R-UNI-38, R-UNI-39 and R-UNI-45 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- TSD S9 T6.1 is the only rights source for this service; FSD S9 A2.12.3.3 names the Partner and agency manager primary and the Head of Litigation and the Head of Asset Liquidity as also using, and the baseline declares exactly that and widens nothing.
- The `partner` and `partner_instruction` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The six operations of the service are the Ownership Map's and the other five belong to the instruction stories of this key; only the two reads are declared here.
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-partner for this step and declare the two reads of the path, recording that no operation ends a contract.
2. Declare the `partner` element exactly as TSD S9 T3.1 gives it, and record that no field of it carries a recall or a re-selection.
3. Declare the `partner_instruction` element exactly as TSD S9 T3.1 gives it, with LOV-INSTR-STATUS including RECALLED, and record that the recall is the status.
4. Fix the recall command element with its attributes, its write order, its idempotency rule and its failure behaviour, and record that the case re-selection is a Temporal command of rwb-case.
5. Publish the rights of the reads and of the act, and record that the partner portal users see their own firm only.
6. Publish the error set, the status codes and the message IDs of the act and of the reads, including the refusal of a result on a recalled instruction.
7. Publish the fakes of 12.8 and the three absence tests: no contract-end operation, no event and no Schedule.
8. Fix the naming baseline and the boundary, then tag the baseline and hand it to RWB-S9-E7015-APP, the SCR-34 and SCR-35 slices and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation or an element carries a value outside a list of values | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC2, AC4, AC7 |
| X2 | A field is renamed or removed within major version 1, or a list value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed or commanded element has a field list or a name the sources do not give | The element carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC7 |
| X5 | The document declares a contract-end operation, an event, a Schedule, a queue table, a foreign table property or a new column of `partner` or `partner_instruction` | The absence and boundary tests fail the build | None | AC1, AC2, AC7 |
| X6 | The rights of the reads and of the act are not the ones TSD S9 T6.1 declares, or a partner portal user is given sight of another firm | The access test fails the build | MSG-P4-002 | AC5 |
| X7 | The service level, an escalation point or a status value is declared with a value no source gives, or as a schema default | The review fails the baseline; the element carries the placeholder | None | AC4, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-case and rwb-decision only |
| Negotiable | The command attribute names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S9-E7015-APP, the SCR-34 and SCR-35 slices and the wave 4 harness on Day 1, and the rwb-case team on the same day |
| Estimable | One OpenAPI document, nine contract tables, six fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the contract-end and recall path of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner and partner_instruction is S9, of recovery_case and timer is P3 and of rule_row and decision_log_entry is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline declares the two reads of the path and records that no operation ends a contract (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /partners with the partner_code, partner_type, panel_status and contract_end of the partner and GET /partner/instructions with the case_id, instructed_at, due_at and status of each instruction
    Then it records POST /cases/{caseId}/instructions, POST /partner/instructions/{instructionId}/accept, POST /partner/instructions/{instructionId}/invoices and POST /partner/instructions/{instructionId}/results as the other four operations of the service, owned by the instruction stories of this key
    Then it declares no operation whose behaviour is the end of a partner contract, and the act carries the placeholder with an error set of 400, 401, 403 with MSG-P4-002, 404, 409 and 503 and one message ID per condition (GAP-3130; ASM-5468)
    Then the absence test fails a build that declares a contract-end operation, a second base or a second topic

  Scenario: AC2 The partner and partner_instruction elements are declared unchanged and carry no recall column (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S9 T3.0, T3.1 and T3.2 and with the API Specification's partner and instruction elements
    Then the partner element declares the seven properties of DF-PRT-001 to DF-PRT-007: id, partner_code, partner_name, partner_type, panel_status, contract_end and score, with the types and lengths TSD S9 T3.1 gives them
    Then the partner_instruction element declares the nine properties of DF-PRT-008 to DF-PRT-016: id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code and fee_amount
    Then partner_type is declared against LOV-PARTNER-TYPE, panel_status against LOV-PANEL with ACTIVE, ON_NOTICE, SUSPENDED and EXITED, instruction_type against LOV-INSTRUCTION and status against LOV-INSTR-STATUS with SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED, with the values TSD S9 T3.2 gives and none added
    Then the document records that the recall is carried by status RECALLED and the exit by panel_status EXITED and contract_end, that this step adds no column and no migration, and that no property carries a recall flag or a re-selection reference (ASM-5469)

  Scenario: AC3 The recall command element and the definition of "open" carry their placeholders (new, D-RCV-60)
    Given the command section of the baseline
    When it is compared with R-UNI-26, R-UNI-45 and TSD S9 T3.2
    Then one recall command is declared per partner and end date, carrying the partner reference, the end date, the reason code, the recalled instruction set with its case keys, R-UNI-26 with its package version, the clock start and the escalation point
    Then the command is declared as a Temporal command on task queue rwb-partner that writes the entry, closes the partner and moves the recall set in one transaction, and asks rwb-case to re-select each affected case under R-UNI-45
    Then the definition of an open instruction is Not specified in the source documents and is carried as the three statuses SENT, ACCEPTED and IN_PROGRESS with the gap and the assumption (GAP-3130; ASM-5470)
    Then the name of the case-side re-selection command is Not specified in the source documents, and the document records that the case is commanded and never written (GAP-3130; ASM-5471)

  Scenario: AC4 The exit entry is declared and written before anything else (new, D-RCV-60)
    Given the entry section of the baseline
    When it is compared with the local decision-record library and with R-UNI-39
    Then one entry is declared per contract end with the partner reference, the end date, the reason code, the recalled instruction set with its case keys, the rule ID R-UNI-26 with its package version, the actor and the clock start
    Then the entry is written through the library on the shared rwb.decision-record.v1 before the partner row, the recall set and the case requests, and a failed write leaves everything unchanged with MSG-P7-003
    Then the clock length is declared as the 5 working days of R-UNI-26's timer column read with its version and never a default, and the escalation point is the one the rule row names
    Then the document records that no PRM rule set exists in the Business Rules and Routing Logic v4, that the exit is recorded against the UNIVERSAL row R-UNI-26, and that R-UNI-38 keeps the version an open case was decided under (ASM-5472)

  Scenario: AC5 The rights, the roles and the scope of the partner portal user are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T6.1 and with FSD S9 A2.12.3.3
    Then the reads declare Partner portal right R and the act declares Partner portal right U, held by RW-AGENCYMG CRUDA, by RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and RW-GUARANT CRU and by the partner portal roles RU
    Then the document records that RW-CASEOWN, RW-TEAMMGR and RW-LEGAL hold R only, that RW-HEADLIT and RW-HEADASL hold RA, and that the act is refused to a role without U with MSG-P4-002
    Then the document records that a partner portal user reads the instructions of its own firm only, that the scope filter is applied to every query, and that the unattended branch runs under the rwb-partner service identity with same checks
    Then the access test fails a build that gives a partner portal user sight of another firm or a role a right the matrix does not give

  Scenario: AC6 The elements and the fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the partner fake answers a partner of type AGENCY at ACTIVE with a contract end in the future, and the same partner at EXITED with the contract end passed
    Then the instruction fake answers instructions at SENT and ACCEPTED on one case, the same instructions at RECALLED after the recall, and one at DONE outside the recall set
    Then the package fake answers the UNIVERSAL package at its version with R-UNI-26, R-UNI-30, R-UNI-38, R-UNI-39 and R-UNI-45 and a package with no version in force, the entry stub answers a healthy chain and a stopped chain, the case fake answers an accepted and a refused re-selection, and the access fake answers a role with U and R and a role with R only
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is published or scheduled (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1, the queue is rwb-partner and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_instruction and partner_user, and recovery_case, queue, assignment, timer, rule_row, decision_log_entry, document, notice and every v_ace_* view are named as other owners' and are reached only through their contracts or the workflow boundary
    Then the document declares no published event and no consumed event for this path, names InstructionIssued (EV-20) and PartnerResultSubmitted (EV-21) as the instruction stories', and records that no event carries the recall (ASM-5471)
    Then the document declares no Schedule, no Quartz row and no shared job table, records that the recall clock is a durable timer of InstructionWorkflow, and records that the Ownership Map gives S9 no job
    Then the document records that the plan's C row is empty although the path commands rwb-case (GAP-3130; ASM-5471)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-E7015-APP and they copy no criterion of the legacy story, whose AC2 stays with the app story word for word and whose AC1 stays with RWB-ITG-E7015-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The `partner` and `partner_instruction` elements are this service's and are declared exactly as TSD S9 T3.1 gives them, with no recall column and no re-selection reference | Context pack ownership rows; TSD S9 T3.1 and T3.2; DP-01 |
| BR2 | The exit is declared as an entry written before anything else, through the local library on the shared topic; a failed write changes nothing and answers MSG-P7-003 | DP-03; TSD S9 T2; R-UNI-39; legacy RWB-E7-015 AC2 |
| BR3 | The case and its route state stay with rwb-case: the contract declares the re-selection as a Temporal command of R-UNI-45 and declares no `recovery_case` and no `timer` property and no case write | Context pack ownership rows; R-UNI-45; ASM-5471 |
| BR4 | The UNIVERSAL package and the central ledger stay with rwb-decision: the contract names R-UNI-26, R-UNI-30, R-UNI-38, R-UNI-39 and R-UNI-45 and declares no rule row and no ledger entry | Business Rules and Routing Logic v4; ASM-5472 |
| BR5 | No event belongs to this path: the contract declares no published event and no consumed event, and names `InstructionIssued` (EV-20) and `PartnerResultSubmitted` (EV-21) as the instruction stories' | Event and Messaging Design v4 EV-20 and EV-21; TSD S9 T5.3; ASM-5471 |
| BR6 | No Schedule belongs to this path: the recall clock is a durable timer of the workflow and the Ownership Map gives S9 no job | Context pack ownership rows (Jobs 0); FSD S9 A2.12.4.4; ASM-5472 |
| BR7 | The rights are TSD S9 T6.1's and nothing wider: Partner portal R for the reads, U for the act, and a partner portal user sees its own firm only | TSD S9 T6.1; FSD S9 A2.12.3.3; ASM-5469 |
| BR8 | The status vocabulary is closed: EXITED is declared against LOV-PANEL and RECALLED against LOV-INSTR-STATUS, and this step adds no value to either | TSD S9 T3.2; ASM-5469 |
| BR9 | A result submitted for an instruction that reads RECALLED is refused; the condition is declared here and the code carries its placeholder | R-UNI-26; ASM-5470 |
| BR10 | No personal data in a schema, an example or a fake: a partner code, a partner type, case and instruction references, a status, a date and a rule version only | Template and Rules v1 §R7.2 (s17); LDM v8 |
| BR11 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules v1 §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 notes |
| BR13 | No service level, no escalation point and no status value is a schema default or a constant | FSD S9 BR-S9-012; ASM-5472 |

### 9. State transitions

The lifecycle of this document, not of a contract:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the unchanged elements, the command, the entry and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the SCR-34 and SCR-35 slices, the wave 4 harness and the rwb-case owner accept the document and the fakes | Baselined |
| Baselined | Additive change | An attribute is added within major version 1 | Baselined |
| Baselined | Breaking change | An attribute is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | A contract-end operation, an event, a Schedule, a new column or a foreign table property | In review |

The `partner` and `partner_instruction` state machines are the app story's and this baseline declares their vocabularies without moving any row: EXITED and RECALLED are the two values the path uses, and no value is added.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the correction of the commanded element and the reading of the case command |
| Consuming teams (the app story, the SCR-34 and SCR-35 slices, the wave 4 harness and the rwb-case owner) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field enters an element or a fake and that no column is added |
| Compliance and the center of excellence | Confirm the service level the clock names and the rule version an open case keeps |

The per-service login behind the security scheme of the document is named "the rwb-partner login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Partner element | The seven columns of DF-PRT-001 to DF-PRT-007 as TSD S9 T3.1 gives them, unchanged: `id`, `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end`, `score` |
| Instruction element | The nine columns of DF-PRT-008 to DF-PRT-016, unchanged: `id`, `case_id`, `partner_id`, `instruction_type`, `instructed_at`, `due_at`, `status`, `result_code`, `fee_amount` |
| Lists of values | `LOV-PANEL` with ACTIVE, ON_NOTICE, SUSPENDED and EXITED; `LOV-INSTR-STATUS` with SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED; `LOV-PARTNER-TYPE` with AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC; `LOV-INSTRUCTION` with COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST and SELL, all as TSD S9 T3.2 gives them |
| Recall command | The command attributes: partner reference, end date, reason code, recalled instruction set with its case keys, R-UNI-26 with its package version, the clock start and the escalation point; no column of either table carries them (ASM-5469) |
| Exit entry | The DP-03 entry attributes of AC4, declared as a library object and not as a table of this service |
| Open instruction | The three statuses SENT, ACCEPTED and IN_PROGRESS: Not specified in the source documents (GAP-3130; ASM-5470) |
| Case command | The re-selection request of R-UNI-45, consumed from rwb-case on the Temporal boundary; its command name is Not specified in the source documents (GAP-3130; ASM-5471) |
| Clock and escalation | The 5 working days of R-UNI-26's timer column and the named escalation point of R-UNI-30, read from the package at its version; no PRM row carries the partner service level (ASM-5472) |
| Not declared here | `recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6), `partner_user` and every `v_ace_*` view (P1), and the other four operations of the service |

The field-level formats of the command and the entry are settled in the baseline review; this story fixes the element names, the unchanged table elements, the lists and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Use | Owner |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | The partner with its `partner_code`, `partner_type`, `panel_status` and `contract_end`, before and after the exit | S9 rwb-partner |
| GET | `/api/recovery/partner/v1/partner/instructions` | The instructions of the caller's firm with their `case_id`, `instructed_at`, `due_at` and `status`, before and after the recall | S9 rwb-partner |

None for the contract end. The Ownership Map gives S9 exactly six operations and the other four — `POST /cases/{caseId}/instructions`, `POST /partner/instructions/{instructionId}/accept`, `POST /partner/instructions/{instructionId}/invoices` and `POST /partner/instructions/{instructionId}/results` — belong to the instruction stories of this key. No operation ends a contract, so the act has no published entry point and carries the placeholder; a build that declares one here fails the absence test of AC1 (GAP-3130; ASM-5468). `POST /partner/instructions/{instructionId}/results` is the service's and this baseline fixes one condition of it only: where the instruction reads RECALLED the write is refused, and the exact code is Not specified in the source documents and is declared non-committally as 409 or 422 (GAP-3130; ASM-5470).

#### 12.2 REST operations consumed

None. The step reads its own two tables, the package arrives loaded at its version and the case is reached on the Temporal boundary, so no REST row is consumed. The case command is a contract dependency of class C in fact and not in this baseline's dependency list, which is None, and the absence is recorded (GAP-3130; ASM-5471).

#### 12.3 Events published

None. The service owns `InstructionIssued` (EV-20) on `rwb.partner.events.v1` — `instructionId`, `partnerId`, `type` and `dueOn` — and `PartnerResultSubmitted` (EV-21) — `instructionId`, `result` and `documents` — and both describe the issue of an instruction and the result the partner records, published by the instruction stories (Event and Messaging Design v4 EV-20 and EV-21; TSD S9 T5.3). A contract end issues no instruction and records no result, so this baseline declares no producer, no envelope and no outbox row of its own, and the absence test of AC7 fails a build that adds one (ASM-5471).

#### 12.4 Events consumed

None. No source gives rwb-partner a consumed event for this path: the act arrives as a Temporal command, the panel and the scorecard are this service's own records, and EV-21 is the result the partner portal records and not an exit. This baseline declares no consumer group, no subscription and no inbox of its own (ASM-5471).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per partner holding its open instructions, continues-as-new | `rwb-partner` in namespace `rwb-recovery` | The host of the `contractEnd` branch; its input, its signals and its outcome are declared, not built |
| The `contractEnd` branch of `InstructionWorkflow` | Workflow branch | `rwb-partner` | The path from the command to the entry, the partner close, the recall set, the case requests and the clock |
| `readOpenInstructions` | Activity | `rwb-partner` | The partner and its instructions in; the open set out |
| `evaluateRecallRules` | Activity | `rwb-partner` | The package in force in; R-UNI-26, R-UNI-38 and R-UNI-39 with their versions out |
| `recordAndApplyExit` | Activity | `rwb-partner` | The entry, the partner close, the recall set and the clock start out, one transaction |
| `requestCaseReselection` | Activity | `rwb-partner` | One child command per case on the case boundary under R-UNI-45; the request in and the child result out |
| `recallClock` | Durable timer | `rwb-partner` | The 5 working days of R-UNI-26 and the 2 of R-UNI-45 with their versions; the expiry is the escalation |

No child workflow of this service exists in this path and no timer table is declared here: the `timer` rows are P3's. The execution grain — one execution per partner holding that partner's open instructions rather than one per instruction — is the target reading of the workflow the sources name, and the branch and activity names are target design choices no source document fixes; no activity is registered by this story.

#### 12.6 Schedules

None. The Ownership Map gives S9 no job and FSD S9 A2.12.4.4 declares no background event for the feature, so this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The recall clock is a durable timer inside the branch (ASM-5472).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `partner` | S9 (`rwb_partner`) | The partner, its type, its panel status, its contract end and its score; the element the baseline declares unchanged and the app story writes two columns of |
| `partner_instruction` | S9 (`rwb_partner`) | The work placed with the partner and its status; the element the baseline declares unchanged and the app story writes `status` of |
| `partner_user` | S9 (`rwb_partner`) | Owned per the Ownership Map; this path neither reads nor writes it, and TSD S9 T3.1 gives it no field list |
| `decision_record` | PLT library, created in `rwb_partner` | The local hash-linked exit entry (DP-03) |
| `idempotency_key` | PLT library, created in `rwb_partner` | The partner-and-date key of the repeated command |
| `outbox_event` | PLT library, created in `rwb_partner` | Created in this schema by the library for the stories that publish; no row of it belongs to this path |

`recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or facts of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Partner fake | Partner `PTR-2027-001501` of type AGENCY at ACTIVE with a contract end in the future, and the same partner at EXITED with the contract end passed | AC2, AC6 |
| Instruction fake | Instructions `INS-2027-001501` (SENT) and `INS-2027-001502` (ACCEPTED) on case `RW-2027-001501`, the same at RECALLED, and one at DONE outside the recall set | AC2, AC6 |
| rwb-decision package fake | The UNIVERSAL package at its version in force with R-UNI-26, R-UNI-30, R-UNI-38, R-UNI-39 and R-UNI-45; a package with no version in force | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, AC6 |
| rwb-case re-selection fake | The case accepting the request with its route reopened, the same case refusing it, and no answer inside 2 s; the command name carries the placeholder (GAP-3130; ASM-5471) | AC3, AC6 |
| rwb-access guard fake | RW-AGENCYMG with Partner portal U and R, a role with R only, and a partner portal user of another firm | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answers for the partner and its instructions | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The case command name is derived from the published documents and carries the placeholder until its owner confirms it (GAP-3130; ASM-5471).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 0 consumed | `GET /partners` and `GET /partner/instructions`; the act has no operation |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 are the instruction stories'; the exit entry is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 4 activities, 1 durable timer and 1 child command per case declared, 0 registered | `InstructionWorkflow` and its `contractEnd` branch on `rwb-partner`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no partner, no instruction, no case and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables, the rights of the reads and of the act, and seven fakes.

**Deliverables.** The additive document `openapi/rwb-partner-v1.yaml` with the two unchanged elements and no contract-end operation, the contract README rows for the commanded case element and its placeholder, the exit-entry schema of the library, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before anything else is answered. DP-13 moves the base of the service and leaves the four other operations to the instruction stories. DP-19 is behind SCR-34 and SCR-35, whose screen model is the edge contract's. No other pattern is claimed: the case command is a Temporal boundary recorded and not claimed (ASM-5471) and the lists of values are read at a version (DP-07, recorded and not claimed), so neither appears in the metadata row and both are in the registers.

**Build steps**

1. Record the absence of a contract-end operation and the two reads of AC1, with the absent-operation test.
2. Publish the `partner` and `partner_instruction` elements unchanged with their properties, their required flags and their four lists, and record the no-recall-column rule of AC2.
3. Publish the recall command of AC3 with the open-status placeholder, the case command and the transaction order.
4. Publish the exit entry of AC4, with the rule ID, the clock, the escalation and the version an open case keeps, and validate it against the library schema.
5. Record the rights, the roles and the partner-portal scope of AC5.
6. Publish the seven fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every path and the drift test is green, and the app story, the SCR-34 and SCR-35 slices and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of an element is absent or invalid, or a body fails schema validation, or a list value is outside its enumeration | Enter {field}. |
| MSG-P4-002 | The role lacks Partner portal U for the act or R for the read, or a partner portal user asks for another firm | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The exit entry cannot be written before anything else | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three message IDs are those of the legacy message set of this key; the text is the legacy and FSD S9 wording, copied unchanged, and no message is reworded or added.

### 15. Screens and states

The contract serves SCR-34 Partner list and SCR-35 Placement and allocation through the gateway-bff composite route (DP-19). The route calls rwb-partner for the partner and its instructions, rwb-case for the case and its route state and rwb-decision for the decision records; this baseline fixes the rwb-partner answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The contract end itself has no button of its own in the published operations, so the screen's act carries the placeholder of AC1. The legacy screen table's two screens are accounted for: SCR-34 and SCR-35 belong to this service, and this story answers their contract-ended, recalled, re-selection-requested, refused, not-recorded and unavailable states with the messages of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-015-01 | AC1, AC2 | Contract | Partner `PTR-2027-001501` with instructions SENT and ACCEPTED on case `RW-2027-001501`; the contract half answers the two reads, the two unchanged elements and the absent contract-end operation |
| TC-E7-015-02 | AC4 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the entry element |
| TC-E7-015-03 | AC5 | Contract | A role with Partner portal R and not U, and a partner portal user of another firm; the contract half answers the 403 with MSG-P4-002 and the scope rule |
| TC-E7-015-04 | AC4, AC6 | Contract | A forced record failure and a drifted fake; the contract half answers the entry path and the drift test |
| TC-S9-E7015-CON-01 | AC1 | Contract | The document validates; no contract-end operation, no second base and no second topic, and the four other operations named as the instruction stories' |
| TC-S9-E7015-CON-02 | AC2 | Contract | The two elements validate with seven and nine properties and their four lists; no recall column and no added state value |
| TC-S9-E7015-CON-03 | AC3 | Contract | The command with its eight attributes, the open-status placeholder and the case command placeholder |
| TC-S9-E7015-CON-04 | AC4 | Contract | The entry with R-UNI-26 and R-UNI-38, the clock, the escalation and the version an open case keeps |
| TC-S9-E7015-CON-05 | AC5 | Contract | Partner portal R for the reads and U for the act; the partner portal user sees its own firm only |
| TC-S9-E7015-CON-06 | AC6 | Contract | The seven fakes match the document and a drifted fake fails the build |
| TC-S9-E7015-CON-07 | AC7 | Contract | The naming baseline; the absence test for an event, a second topic, a Schedule and a Quartz row, and the boundary test for a `v_ace_*` path and a foreign table property |

The four legacy cases are the legacy cases of RWB-E7-015 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S9-E7015-APP and by RWB-ITG-E7015-ITG. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S9-E7015-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here.

### 17. Guardrails

- No business value in the contract: the service level, the escalation point, the status values, the lists and the rule rows stay reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: a partner code, a partner type, case and instruction references, a status, a date and a rule version only.
- The case and its timers stay with rwb-case and the package and the ledger with rwb-decision: the document declares no `recovery_case`, `timer`, `rule_row` or ledger property (BR3, BR4).
- This path owns no contract-end operation and no event: the document declares none for it and names the six operations and the two events as the service's and the instruction stories' (BR5, AC1).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- The two table elements are declared unchanged: a build that adds a recall flag, a re-selection reference or a status value fails the absence test (BR1, BR8, ASM-5469).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row or a shared job table (BR6).
- The rights are TSD S9 T6.1's and are never widened in a contract; the partner portal scope is declared and tested, not assumed (BR7, ASM-5469).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S9-006 | A partner panel exit, a declared conflict of interest, insolvency or an upheld conduct breach recalls every open case held by that partner (Must, E7) | The recall command, the exit entry, the recalled status and the case command | TC-E7-015-01, TC-S9-E7015-CON-01, TC-S9-E7015-CON-03, TC-S9-E7015-CON-04 |
| REQ-S9-001 | Every partner type is managed on the same six points, the last of which is notice and exit (Must, E6) | The two unchanged elements, the panel status EXITED and the contract end | TC-S9-E7015-CON-02, TC-S9-E7015-CON-06 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E7015-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two reads and the case command with its budget and breaker | TC-S9-E7015-CON-01 |
| ADR-022 | Local decision record plus central ledger | The exit entry and the central ledger of P7 | TC-S9-E7015-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-015, disposition Split (rework); feature FEAT-PRM-12 |
| Legacy criteria | AC2 of the legacy story, owned word for word by RWB-S9-E7015-APP; AC1 by RWB-ITG-E7015-ITG; this baseline copies none of them |
| Test cases | The four legacy cases as the contract half, and the seven new contract cases TC-S9-E7015-CON-01 to -07 |
| Feature and screens | FEAT-PRM-12, SCR-34 Partner list and SCR-35 Placement and allocation |
| Rules | R-UNI-26, R-UNI-30, R-UNI-38, R-UNI-39 and R-UNI-45 named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the reads, the recall, the entry, the partner close and the case request: RWB-S9-E7015-APP.
- The end-to-end proof of the legacy key through the real contracts: RWB-ITG-E7015-ITG.
- The issue, acceptance, result and invoice of an instruction and the four operations that carry them: the instruction stories of this service.
- The notice on a missed target and its cure period (FEAT-PRM-11) and the allocation and scorecard that pick the next partner (FEAT-PRM-03, FEAT-PRM-04, FEAT-PRM-08).
- The case of record, its route state and its timers, and the re-selection itself: rwb-case (P3), which applies the command this baseline declares.
- The UNIVERSAL package, its rule rows and the central ledger: rwb-decision (P7).
- The roles, the rights and the lists of values: rwb-access (P4).
- The partner gateway and FAPI 2.0: the edge stories' own scope.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
