# RWB-S9-E7013-CON Hold a partner review - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7013-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S9-E7013-CON-14) |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S9-E7013-CON-16); the squad sizes it at refinement |
| Contract version | v1 (base `/api/recovery/partner/v1`) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the partner review of rwb-partner, split from RWB-E7-013. It fixes the review-entry element, the unchanged `partner` and `partner_instruction` elements, the consumed rule-row and reference-data rows, the rights and the error set of the act, the fakes, and the three absences the act has — no operation, no event and no column of its own — on the base `/api/recovery/partner/v1` (DP-13) behind the gateway-bff composite route (DP-19). The six operations of the service are declared as the earlier stories' and the review act is not given a seventh. Two consumed operation names, the review read and the action list are unpublished, and the plan's C row is empty although the act consumes rwb-decision and rwb-case (GAP-3126; ASM-5446 to ASM-5449). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E7013-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 11 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-partner**, I want **the published contract baseline of the partner review — the review-entry element, the unchanged `partner` and `partner_instruction` elements, the consumed rule-row and reference-data rows, the rights and the error set of the act, the fakes and the three absences**, so that **the app story, the SCR-34 and SCR-35 review slice and the wave 4 harness build against one fixed, testable contract on Day 1, and a point, a list or a right can never drift between rwb-partner, rwb-decision and rwb-case without a failing build**.

The baseline is deliberately narrow: it declares one element of this service, two unchanged elements, two consumed rows and the absences the act has. It declares no operation, no event and no Schedule of its own.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy review of RWB-E7-013 ran inside one process and one schema: it read the partner, the instructions, the rule row and the decision log without a boundary. The target splits them: rwb-partner owns the partner and its instructions, rwb-decision owns the package, the rule rows and the central ledger, rwb-case owns the parameters and the reference data by the R3 default ruling, and rwb-access owns the rights and the lists of values. Each boundary is a contract another team builds against, so the shapes have to be fixed before the app story starts: the partner element it reads, the six points and the actions it records, the entry it writes and the rights of the act.

The baseline also fixes the naming the checks require: schema `rwb_partner`, login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules v1 §R4; context pack service row). It records that rwb-partner holds no grant on `rwb_case`, `rwb_decision` or `rwb_access`, so the reference data, the rule rows and the rights are consumed on their owners' contracts only.

Four points are carried as gaps and assumptions rather than decided quietly: the baseline declares no operation for the review, because the six the Ownership Map gives S9 all belong to earlier stories of the service and the review read is unpublished (GAP-3126; ASM-5446); no column of `partner` or `partner_instruction` carries the review, so both elements are unchanged and the review lives on its entry (ASM-5447); the rule-row read and the reference-data read carry placeholders because no source publishes their operation names and DP-04, DP-06 and DP-07 are not in the pattern set (ASM-5448); and the six points and the action list are declared as reference data with no published action list (GAP-3126; ASM-5449).

The wave and the date are the plan's: this key is EP07, wave 4, release 31 May 2027, and rwb-partner is itself wave 4, so the business wave and the service wave agree and no W-MAP conflict is raised; the date is copied unchanged and marked tentative (ASM-5449).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case`, `queue`, `assignment` and `timer` are P3's, `rule_row` and `decision_log_entry` are P7's, `document` is P5's, `notice` is P6's and `interaction` is P1's. This document never declares another service's table or operation as its own.
- The rule-package read and the reference-data read are published with fakes so the consumed rows name a real owner document; neither is a row of this story's dependency list, which is None, and the absence is recorded (GAP-3126; ASM-5448).
- TSD S9 T6.1 is the only rights source for this service, and the legacy permission table of the key gives the same intent for the act (right U) and for the read (right R); no right is widened here (ASM-5449).
- The three tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The six operations of this legacy key's service, API-S9-001 to API-S9-006, are outside this baseline and belong to the earlier stories of the service.
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-partner for this step and record that it declares no operation for the review, with the six operations of the service named as the earlier stories' and their rights restated.
2. Declare the `partner` and `partner_instruction` elements exactly as TSD S9 T3.1 gives them, and record that no field of either carries the review, a point or an action.
3. Declare the consumed rule-row read of rwb-decision and the reference-data read of rwb-case, with the fields the review needs, and record that their operation names are unpublished.
4. Fix the review-entry element of DP-03 with its attributes, its write order and its failure behaviour.
5. Publish the rights of the act and of the read from TSD S9 T6.1, and record the two heads of function as readers and approvers rather than writers.
6. Publish the error set, the status codes and the message IDs of the act and of the read.
7. Publish the fakes of 12.8 and the three absence tests: no operation, no event and no column.
8. Fix the naming baseline and the boundary, then tag the baseline and hand it to RWB-S9-E7013-APP, the SCR-34 and SCR-35 review slice and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation or an element carries a value outside a list of values | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC2, AC4, AC7 |
| X2 | A field is renamed or removed within major version 1, or a list value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3 |
| X5 | The document declares a review operation, an event, a Schedule, a queue table, a foreign table property or a new column of `partner` | The absence and boundary tests fail the build | None | AC1, AC2, AC7 |
| X6 | The rights of the act and of the read are not the ones TSD S9 T6.1 declares, or the unattended identity is given a user right | The access test fails the build | MSG-P4-002 | AC5 |
| X7 | A point, a status, an action or a rule version is declared with a value no source gives, or as a schema default | The review fails the baseline; the element carries the placeholder | None | AC4, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-decision and rwb-case only |
| Negotiable | The element attribute names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S9-E7013-APP, the SCR-34 and SCR-35 review slice and the wave 4 harness on Day 1 |
| Estimable | One OpenAPI document, nine contract tables, five fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the partner review of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner and partner_instruction is S9, of recovery_case is P3, of rule_row and decision_log_entry is P7 and of the rights is P4
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline provides no operation for the review and records the six operations of the service as earlier stories' (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares no operation whose behaviour is the review of a partner against the six points
    Then it records GET /partners (API-S9-001), POST /cases/{caseId}/instructions (API-S9-002), GET /partner/instructions (API-S9-003), POST /partner/instructions/{instructionId}/accept (API-S9-004), POST /partner/instructions/{instructionId}/results (API-S9-005) and POST /partner/instructions/{instructionId}/invoices (API-S9-006) as the earlier stories' of the service, each with its documented right
    Then the review read behind SCR-34 and SCR-35 carries the placeholder, with an error set of 400, 401, 403 with MSG-P4-002, 404 and 503 and one message ID per condition (GAP-3126; ASM-5446)
    Then the absence test fails a build that declares a review operation, a second base or a second topic

  Scenario: AC2 The partner and partner_instruction elements are unchanged and carry no review field (new, D-RCV-60)
    Given the partner and instruction sections of the baseline
    When they are compared with TSD S9 T3.0, T3.1 and T3.2 and with the API Specification's Partner and PartnerInstruction elements
    Then the partner element declares the seven properties of DF-PRT-001 to DF-PRT-007: id, partner_code, partner_name, partner_type, panel_status, contract_end and score, with the types and lengths TSD S9 T3.1 gives them
    Then the partner_instruction element declares the nine properties of DF-PRT-008 to DF-PRT-016: id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code and fee_amount, with the types TSD S9 T3.1 gives them
    Then partner_type is declared against LOV-PARTNER-TYPE, panel_status against LOV-PANEL, instruction_type against LOV-INSTRUCTION and status against LOV-INSTR-STATUS, with the values TSD S9 T3.2 gives and none added
    Then the document records that no property of either element carries a review, a point or an action, that this step adds no column and no migration, and that the review is carried on its entry (GAP-3126; ASM-5447)

  Scenario: AC3 The consumed rule-row and reference-data rows are declared with their placeholders (new, D-RCV-60)
    Given the consumed rows and the boundary of the baseline
    When they are compared with rwb-decision as the owner of the rule package and rwb-case as the owner of reference data under the R3 default ruling
    Then the rule-row read is declared as consumed from P7 rwb-decision, with the rule ID, the package, the version and the route set, and no rule row is declared as a property of this service
    Then the reference-data read is declared as consumed from P3 rwb-case, with the six points of REQ-S9-001, the status list, the action list and the four lists of TSD S9 T3.2, each with its version
    Then the action list is Not specified in the source documents, both operation names are Not specified in the source documents, each read is one hop with a 2 s budget and a breaker, and the document records that DP-04, DP-06 and DP-07 are not in this key's pattern set although the package and the reference data are consumed (GAP-3126; ASM-5448)
    Then the document declares no rule_row, no recovery_case, no queue, no timer and no v_ace_* property, and no personal-data field

  Scenario: AC4 The review-entry element is declared and written before anything else (new, D-RCV-60)
    Given the entry section of the baseline
    When it is compared with the local decision-record library and with R-UNI-39
    Then one review entry is declared per partner and review date, with the partner reference, the six point values and their actions, the rule ID and package version, the reviewer and the instant
    Then the entry is written through the library on the shared rwb.decision-record.v1 before the review is answered, and a failed write leaves everything unchanged with MSG-P7-003
    Then the six points are declared in REQ-S9-001's order and the status and action values are declared as reference data read at a version and never a default
    Then the document records that the action list is unpublished and carries the placeholder (GAP-3126; ASM-5449)

  Scenario: AC5 The rights, the roles and the unattended identity are fixed on the act and on the read (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T6.1 and with FSD S9 A2.10.3.3
    Then the act declares Partner portal right U, held by RW-AGENCYMG CRUDA and by RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and RW-GUARANT CRU plus the partner portal users RU, and the read declares Partner portal right R
    Then the document records that RW-HEADLIT and RW-HEADASL are the "also uses" roles of FSD S9 A2.10.3.3 and hold RA in TSD S9 T6.1, so they read and approve and take no U act
    Then the document records that the act runs under the rwb-partner user identity of the caller and that any unattended run holds no user right of its own
    Then the access test fails a build that gives a role a right the matrix does not give or widens the read to a partner portal user outside its own firm

  Scenario: AC6 The elements and the fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the rule-version fake answers the package at its version in force with no row naming a review, and a package with no version in force
    Then the reference-data fake answers the six points in order with their version, the four lists of TSD S9 T3.2, an unpublished action list and no answer inside 2 s
    Then the decision-record stub answers a healthy chain and a stopped chain, the composite-route fake answers the merged SCR-34 and SCR-35 slice, and the authorise stub answers right U held and a caller without it
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is published or scheduled (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1, the queue is rwb-partner and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_instruction, partner_user and the library objects decision_record and idempotency_key, and recovery_case, queue, assignment, timer, rule_row, decision_log_entry, document, notice, interaction and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event, and names InstructionIssued (EV-20) and PartnerResultSubmitted (EV-21) as the instruction stories' (ASM-5446)
    Then the document declares no Schedule, no Quartz row and no shared job table, and records that the Ownership Map gives S9 no job
    Then the document records that the plan's C row is empty although the act consumes rwb-decision and rwb-case (GAP-3126; ASM-5446)

  Scenario: AC8 Every business rule of section 8 names its criterion and its test case (new, D-RCV-60)
    Given the business rules table of section 8
    When each row is compared with section 7 and section 16
    Then every rule BR1 to BR13 names at least one criterion of section 7 in its Covered by cell
    Then every criterion and test case named in a Covered by cell is present in section 7 or as a row of section 16 with the same ID

  Scenario: AC9 A retried or timed-out activity writes no second review entry (new, D-RCV-60)
    Given a review whose rule-package or reference-data read is retried or exceeds its 2 s budget as AC3 fixes it
    When the review is answered again under the same idempotency key
    Then the review entry is written at most once and the timed-out read answers with the 503 of AC1

  Scenario: AC10 A status value the model does not allow is refused (new, D-RCV-60)
    Given a status change that the transition model does not allow (Not specified in the source documents (NEWAC-RWB-S9-E7013-CON-AC10)), or a partner_instruction status or a panel_status outside the lists of TSD S9 T3.2 as AC2 declares them
    When a write carries that value
    Then the write is refused with an answer Not specified in the source documents (NEWAC-RWB-S9-E7013-CON-AC10) and no value is stored
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-E7013-APP and they copy no criterion of the legacy story, whose AC2 stays with the app story word for word and whose AC1 belongs to RWB-ITG-E7013-ITG.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The `partner` and `partner_instruction` elements are this service's and are declared exactly as TSD S9 T3.1 gives them, with no review field and no added list value | Context pack ownership rows; TSD S9 T3.1 and T3.2; DP-01 | AC2; TC-E7-013-01, TC-S9-E7013-CON-02 |
| BR2 | The review is declared as an entry written before anything else, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S9 T2; R-UNI-39; legacy RWB-E7-013 AC2 | AC4; TC-E7-013-02, TC-E7-013-04, TC-S9-E7013-CON-04 |
| BR3 | The rule rows stay with rwb-decision: the contract declares the read as consumed and declares no `rule_row` property and no rule ID of its own | TSD S9 T2, T5.2; ASM-5448 | AC3; TC-S9-E7013-CON-03 |
| BR4 | The reference data stays with rwb-case under the R3 default ruling: the contract declares the read as consumed and declares no reference-data property | R3 default rulings; DP-06, DP-07; ASM-5448 | AC3; TC-S9-E7013-CON-03 |
| BR5 | The six points are REQ-S9-001's and are declared in its order; a status or an action with no published list carries the placeholder | REQ-S9-001; FSD S9 BR-S9-010; GAP-3126 | AC4; TC-S9-E7013-CON-04 |
| BR6 | No event belongs to this act: the contract declares no published event and no consumed event, and names `InstructionIssued` (EV-20) and `PartnerResultSubmitted` (EV-21) as the instruction stories' | Context pack ownership rows; TSD S9 T5.3; ASM-5446 | AC7; TC-S9-E7013-CON-07 |
| BR7 | No Schedule belongs to this act: the Ownership Map gives S9 no job and FSD S9 A2.10.4.4 declares no background event | Context pack ownership rows (Jobs 0); FSD S9 A2.10.4.4; ASM-5449 | AC7; TC-S9-E7013-CON-07 |
| BR8 | The rights are TSD S9 T6.1's and nothing wider: Partner portal U for the act, R for the read, and the two heads of function keep RA | TSD S9 T6.1; FSD S9 A2.10.3.3; ASM-5449 | AC5; TC-E7-013-03, TC-S9-E7013-CON-05 |
| BR9 | The partner and instruction vocabularies are closed: the values of TSD S9 T3.2 are declared and this step adds none | TSD S9 T3.2; ASM-5447 | AC2; TC-S9-E7013-CON-02 |
| BR10 | No personal data in a schema, an example or a fake: identifiers, list values, a rule version and an instant only, and the registered name of the firm is not personal data | Template and Rules v1 §R7.2 (s17); FSD S9 A2.10.3.2 | AC6; TC-E7-013-04, TC-S9-E7013-CON-06 |
| BR11 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules v1 §R4 | AC1; TC-E7-013-01, TC-S9-E7013-CON-01 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 notes | AC7; TC-S9-E7013-CON-07 |
| BR13 | No point, no status, no action and no rule version is a schema default or a constant | FSD S9 BR-S9-010; ASM-5449 | AC4; TC-S9-E7013-CON-04 |

### 9. State transitions

The lifecycle of this document, not of a partner:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The entry, the unchanged elements, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the SCR-34 and SCR-35 review slice, the wave 4 harness, the rwb-decision owner and the rwb-case owner accept the document and the fakes | Baselined |
| Baselined | Additive change | An attribute is added within major version 1 | Baselined |
| Baselined | Breaking change | An attribute is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | An operation, an event, a Schedule, a new column or a foreign table property | In review |

The panel status of a partner is a value of `LOV-PANEL` and moves on the notice and the contract end, not here: this baseline declares the vocabulary on which `panel_status` is declared and adds no value to it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the correction of a consumed row and the reading of the rights |
| Consuming teams (the app story, the SCR-34 and SCR-35 review slice, the wave 4 harness, the rwb-decision owner and the rwb-case owner) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal-data field and no contact value is declared in an entry or a fake |
| Compliance and PDPA officer | Confirms that the six points and the actions are reference data and that the registered name of the firm is not personal data |

The per-service login behind the security scheme of the document is named "the rwb-partner login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | Business rule |
|---|---|---|
| Partner element | The seven columns of DF-PRT-001 to DF-PRT-007 as TSD S9 T3.1 gives them, unchanged: `id`, `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end`, `score` | BR1 |
| Instruction element | The nine columns of DF-PRT-008 to DF-PRT-016 as TSD S9 T3.1 gives them, unchanged: `id`, `case_id`, `partner_id`, `instruction_type`, `instructed_at`, `due_at`, `status`, `result_code`, `fee_amount` | BR1 |
| Required flags | `partner_code`, `partner_name`, `partner_type` and `panel_status` required and `contract_end` and `score` optional; `case_id`, `partner_id`, `instruction_type`, `instructed_at` and `status` required and `due_at`, `result_code` and `fee_amount` optional, as TSD S9 T3.1 gives them | BR1 |
| Lists of values | `LOV-PARTNER-TYPE` with AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC; `LOV-PANEL` with ACTIVE, ON_NOTICE, SUSPENDED and EXITED; `LOV-INSTRUCTION` with COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST and SELL; `LOV-INSTR-STATUS` with SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED, all as TSD S9 T3.2 gives them | BR9 |
| Review entry | The DP-03 entry attributes: partner reference, the six point values, their actions, the rule ID and package version, the reviewer and the instant; no column of `partner` or `partner_instruction` carries any of them (ASM-5447) | BR2 |
| Consumed rule-row shape | The rule ID, the package, the version and the route set of the row read from rwb-decision, declared as consumed and faked (ASM-5448) | BR3 |
| Consumed reference shape | The six points of REQ-S9-001, the status list, the action list and the four lists of TSD S9 T3.2, each with its version, declared as consumed and faked; the action list is Not specified in the source documents (GAP-3126; ASM-5449); the reference-data contract is DP-06 and DP-07 and its parameters are Not specified in the source documents (DOR-RWB-S9-E7013-CON-20) | BR4 |
| Not declared here | `recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6), `interaction` (P1), every `v_ace_*` view (P1), and the six operations API-S9-001 to API-S9-006 (the earlier stories of the service) | BR11 |

The field-level formats of the entry are settled in the baseline review; this story fixes the element names, the two unchanged elements, the consumed fields and the additive rule of BR12. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). The Ownership Map gives this service exactly six operations — `GET /partners` (API-S9-001), `POST /cases/{caseId}/instructions` (API-S9-002), `GET /partner/instructions` (API-S9-003), `POST /partner/instructions/{instructionId}/accept` (API-S9-004), `POST /partner/instructions/{instructionId}/results` (API-S9-005) and `POST /partner/instructions/{instructionId}/invoices` (API-S9-006) — and all six are the frozen baseline of RWB-S9-AD022-CON, with a first-in epic of Epic 2 to Epic 6 (TSD S9 T-A.1). None of them records a review, so the act has no published entry point and the review read behind SCR-34 and SCR-35 is Not specified in the source documents (GAP-3126; ASM-5446). A build that declares a seventh operation here fails the absence test of AC1.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The rule-package and rule-row read (operation name Not specified in the source documents (GAP-3126; ASM-5448)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package, the rule ID and the version in force at the review instant, and any row that names a partner review; read only, faked |
| The reference-data read (operation name Not specified in the source documents (GAP-3126; ASM-5448)) | `/api/recovery/case/v1` | P3 rwb-case, as the owner of parameters and reference data (R3 default ruling) | The six points of REQ-S9-001, the status list, the action list and the four lists of TSD S9 T3.2, each with its version; read only, faked |

Each row is one hop with a 2 s timeout, one retry with jitter on a GET and a breaker per downstream (ADR-020, DP-11). Both are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3126 with ASM-5448.

#### 12.3 Events published

None. The service owns `InstructionIssued` (EV-20) and `PartnerResultSubmitted` (EV-21) on `rwb.partner.events.v1` — an instruction reference with its case, partner, type and due date for the first, and an instruction reference with its result code and fee for the second — and both report an instruction or a result: their schemas are declared in the service baseline RWB-S9-AD022-CON and their behaviour belongs to the instruction stories of this service (context pack ownership rows; TSD S9 T5.3). A review issues no instruction and submits no result, so this baseline declares no producer, no envelope and no outbox row of its own, and the absence test of AC7 fails a build that adds one (ASM-5446).

#### 12.4 Events consumed

None. No source gives rwb-partner a consumed event for this act: the service acts on the events of rwb-case for its instruction stories, and the review is started by a person on a screen. This baseline declares no consumer group, no subscription and no inbox of its own (ASM-5446).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, the service's only one | `rwb-partner` in namespace `rwb-recovery` | The workflow of the instruction stories; this baseline names it and declares no branch of it; workflow ID form Not specified in the source documents (CG-ALL-12036); start rule Not specified in the source documents (CG-ALL-12036) |
| The review act | Synchronous service act, no workflow | `rwb-partner` | The read, the reference load, the rule version and the entry, in one request |
| `recordReview` | Synchronous step of the act, one transaction | `rwb-partner` | The entry, the reviewer and the answer out |

The service has no case state machine of its own and no job (TSD S9 T4; context pack Jobs 0), so the review is a synchronous act whose only durable artefact is the decision record. No source puts the review inside `InstructionWorkflow`, and this baseline declares no child workflow, no activity registration and no durable timer (ASM-5449).

#### 12.6 Schedules

None. The Ownership Map gives S9 no job and FSD S9 A2.10.4.4 declares no background event for the feature, so this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table (ASM-5449).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `partner` | S9 (`rwb_partner`) | The partner, its type, its panel status, its contract end and its score; the element the baseline declares unchanged and the app story reads |
| `partner_instruction` | S9 (`rwb_partner`) | The work placed with the partner; the element the baseline declares unchanged and the app story reads |
| `partner_user` | S9 (`rwb_partner`) | The partner portal identities of the firm; declared as owned and not read by the review |
| `decision_record` | PLT library, created in `rwb_partner` | The local hash-linked review entry (DP-03) |
| `idempotency_key` | PLT library, created in `rwb_partner` | The key of the repeat and the answer it holds (R-UNI-40) |

`recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6), `interaction` (P1) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or records of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain, a stopped chain and a hash break | AC4, AC6 |
| rwb-decision rule-version fake | The package at its version in force with no row naming a partner review, and a package with no version in force; the operation name carries the placeholder (GAP-3126; ASM-5448) | AC3, AC6 |
| rwb-case reference-data fake | The six points in REQ-S9-001's order with their version, the four lists of TSD S9 T3.2, an unpublished action list and no answer inside 2 s; the operation name carries the placeholder (GAP-3126; ASM-5448) | AC3, AC6 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answer for a synthetic partner, with the review slice of this service read once | AC1, AC6 |
| Authorise stub of the service template | Partner portal right U held, a caller without it, and a partner portal user scoped to another firm | AC5, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The two operation names are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3126; ASM-5448).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | The rwb-decision rule-package read and the rwb-case reference-data read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 are the instruction stories'; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 0 branches, 0 activities and 0 timers declared | `InstructionWorkflow` is the service's and belongs to the instruction stories; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no partner, no instruction, no rule package and no case. What it publishes is one OpenAPI 3.1 document, nine contract tables, the rights of the act and the read, and five fakes.

**Deliverables.** The additive document `openapi/rwb-partner-v1.yaml` with the two unchanged elements and no review operation, the contract README rows for the two consumed rows and their placeholders, the review-entry schema of the library, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before anything else is answered. DP-13 moves the base of the service and adds no operation, because this step owns none. DP-19 is behind SCR-34 and SCR-35, whose screen model is the edge contract's. No other pattern is claimed: the rule package is a consumed contract (DP-04, recorded and not claimed), the reference data is consumed at a version (DP-06 and DP-07, recorded and not claimed), so none of the three appears in the metadata row and all three are in the registers (GAP-3126; ASM-5448).

**Build steps**

1. Record the absence of a review operation and the six operations as the earlier stories', with the absent-operation test of AC1.
2. Publish the `partner` and `partner_instruction` elements unchanged with their sixteen properties, their required flags and their four lists, and record the no-review-column rule of AC2.
3. Record the two consumed rows of AC3 with their owners, their fields, their lists, their budget and the placeholders.
4. Publish the review-entry element of AC4, with the six points, the actions, the rule ID and version, the reviewer and the instant, and validate it against the library schema.
5. Record the rights, the roles and the identity of AC5.
6. Publish the five fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every path and the drift test is green, and the app story, the SCR-34 and SCR-35 review slice and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | Type | Message | When |
|---|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. | A required field of an element is absent or invalid, or a body fails schema validation, or a list value is outside its enumeration |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | The role lacks the Partner portal right of the act or of the read, and a scope outside the caller's firm is refused the same way |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The review entry cannot be written before anything else |

The three message IDs are those of the legacy message set of this key; the text is the legacy and FSD S9 wording, copied unchanged, and no message is reworded or added. R-UNI-39's incident is raised by the platform on the same failure and is not a message of this service.

### 15. Screens and states

The contract serves the review slice of SCR-34 Partner list and SCR-35 Placement and allocation through the gateway-bff composite route (DP-19). The route calls rwb-partner for the partner, its instructions and the review entry, rwb-case for the case label and rwb-decision for the rule version; this baseline fixes the rwb-partner answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON (ASM-5446). The review read behind the list is a placeholder, because no source publishes it. The legacy screen table's two screens are accounted for, and SCR-36 Partner scorecard is FEAT-PRM-08's screen and is not answered here. The loading, list, review-open, recorded, refused, not-recorded, empty-score and unavailable states read the messages of section 14 on the same route. For SCR-34 and SCR-35, the empty, error and no access states are Not specified in the source documents (CG-ALL-12038, CG-ALL-12039), because Screen Specifications v1 lacks them. SCR-36 is not answered here, and its empty, error and no access states are Not specified in the source documents (CG-ALL-12040).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-013-01 | AC1, AC2 | Contract | The synthetic partner `P-2026-000713` of type AGENCY and an instruction in status DONE; the contract half answers the two unchanged elements, the absent review operation and the review entry shape |
| TC-E7-013-02 | AC4 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the entry element |
| TC-E7-013-03 | AC5 | Contract | A role without Partner portal U and a partner portal user scoped to another firm; the contract half answers the 403 with MSG-P4-002 and the rights of the act and the read |
| TC-E7-013-04 | AC4, AC6 | Contract | A forced record failure and a drifted fake; the contract half answers the entry path and the drift test |
| TC-S9-E7013-CON-01 | AC1 | Contract | The document validates; no review operation, no second base and no second topic are declared, and the six operations are named as the earlier stories' |
| TC-S9-E7013-CON-02 | AC2 | Contract | The `partner` element with its seven properties and the `partner_instruction` element with its nine, their required flags and their four lists; no review column and no added list value |
| TC-S9-E7013-CON-03 | AC3 | Contract | The rule-row row and the reference-data row with their fields, their lists and their placeholders; no `rule_row`, `recovery_case` or `v_ace_*` property |
| TC-S9-E7013-CON-04 | AC4 | Contract | The entry with the six points, their actions, the rule ID and version, the reviewer and the instant; the action list carries its placeholder |
| TC-S9-E7013-CON-05 | AC5 | Contract | Partner portal U for the act and R for the read; RW-AGENCYMG CRUDA, the U holders, the two RA heads and a partner portal user scoped to another firm |
| TC-S9-E7013-CON-06 | AC6 | Contract | The five fakes match the document and a drifted fake fails the build |
| TC-S9-E7013-CON-07 | AC7 | Contract | The naming baseline; the absence test for an event, a second topic, a Schedule and a Quartz row, and the boundary test for a `v_ace_*` path and a foreign table property |
| TC-S9-E7013-CON-08 | AC7 | Contract | The boundary test for the five tables of §12.7 (ASM-3438): the three owned tables and the two library objects, with no table outside the schema and no foreign key |
| TC-S9-E7013-CON-09 | AC8 | Contract | Every section 8 row with its Covered by cell and the section 7 and section 16 rows it names |
| TC-S9-E7013-CON-10 | AC9 | Contract | A review whose read is retried or passes 2 s, repeated under the same idempotency key; one review entry and the 503 answer |
| TC-S9-E7013-CON-11 | AC10 | Contract | A disallowed status change, and a partner_instruction status or panel_status outside the TSD S9 T3.2 lists; the refusal and no stored value |

The four legacy cases are the legacy cases of RWB-E7-013 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S9-E7013-APP or, for TC-E7-013-01, by RWB-ITG-E7013-ITG. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The eleven cases `TC-S9-E7013-CON-01` to `-11` are new. The full test, with its Given, When and Then, is missing from Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID (CG-ALL-12037); no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness. The harness environment and base hosts, fixture layout, synthetic partner and instruction keys, review evidence shape and retention, and pass or fail gate are Not specified in the source documents (GAP-0474).

### 17. Guardrails

- No business value in the contract: the six points, the statuses, the actions, the partner types, the panel states, the instruction lists and the rule versions stay reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, list values, a rule version and an instant only; no contact value, number or address appears anywhere in the document.
- The rule rows and the central ledger stay with rwb-decision, the reference data and the case with rwb-case and the rights with rwb-access: the document declares no `rule_row`, `recovery_case`, `queue`, `timer` or `v_ace_*` property (BR3, BR4).
- This step owns no operation and no event: the document declares none for it and records the six operations of the service as the earlier stories' (BR6, AC1).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- The `partner` and `partner_instruction` elements are declared unchanged: a build that adds a review column, a point or an action list to them fails the absence test (BR1, ASM-5447).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row or a shared job table (BR7).
- The rights are TSD S9 T6.1's and are never widened in a contract; a partner portal user sees its own firm only, and that scope is tested (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S9-001 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit (Must, E6) | The six-point list of the reference-data row and the entry | TC-S9-E7013-CON-03, TC-S9-E7013-CON-04 |
| REQ-S9-007 | Partner performance, conduct and complaint data are reported to the partner review forum (Must, E7) | The review-entry element and the evidence it leaves | TC-S9-E7013-CON-04 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E7013-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-S9-E7013-CON-03 |
| ADR-022 | Local decision record plus central ledger | The review-entry element and the central ledger of P7 | TC-S9-E7013-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-013, disposition Split (rework); feature FEAT-PRM-10 |
| Legacy criteria | AC2 owned word for word by RWB-S9-E7013-APP; AC1 owned by RWB-ITG-E7013-ITG; this baseline copies neither |
| Test cases | The four legacy cases as the contract half, and the seven new contract cases TC-S9-E7013-CON-01 to -07 |
| Feature and screens | FEAT-PRM-10, SCR-34 Partner list and SCR-35 Placement and allocation |
| Rules | R-UNI-39 named from the Business Rules and Routing Logic v4 and governed in rwb-decision, with R-UNI-25 to R-UNI-29, R-UNI-40 and R-UNI-45 read |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the six points, the actions, the entry and the screen slice: RWB-S9-E7013-APP.
- AC1 of the legacy key and the cross-service journey that evidences it: RWB-ITG-E7013-ITG.
- The six operations of the service and the instruction flow behind them: the instruction stories of this service (API-S9-001 to API-S9-006, Epic 2 to Epic 6).
- The monthly scorecard that fills `partner.score`: FEAT-PRM-08, RWB-S9-E7011-APP; the approval of partner fees: FEAT-PRM-09, RWB-S9-E7012-APP; the notice: FEAT-PRM-11, RWB-S9-E7014-APP; the contract end and recall: FEAT-PRM-12, RWB-S9-E7015-APP; the conduct check: FEAT-PRM-13, RWB-S9-E7016-APP.
- The partner panel and the fee schedule as data: FEAT-PRM-02, RWB-S9-E6030-APP; the partner identities through the external gateway: RWB-S9-E2019-APP.
- The case of record, its stage and its timers: rwb-case (P3); the rule rows, the package and the central ledger: rwb-decision (P7); the roles, the rights and the lists of values: rwb-access (P4); the documents and the notices: rwb-document (P5) and rwb-comms (P6).
- The gateway-bff composite route and the screen field list of SCR-34 and SCR-35: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
