# RWB-S9-E7012-CON Approve partner fees - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7012-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-012 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the fee-approval path of rwb-partner, split from RWB-E7-012. It fixes the `partner_instruction` element with its fee and result fields, the two consumed owner contracts of rwb-document and rwb-case, the fee-approval entry, the rights and the error set of the act, the fakes, and the four absences the path has — no operation of its own, no event, no fee status or approved column, and no Schedule — on the base `/api/recovery/partner/v1` (DP-13) behind the gateway-bff composite route (DP-19). The `partner_instruction` element and its nine fields are declared unchanged, because no field of TSD S9 T3.1 carries a fee approval, its approver or its approved instant, and the six operations of the service belong to the panel, instruction, result and invoice stories of Epics 2, 4 and 6. The approval operation is unpublished, the plan's C and X rows are empty although the path consumes rwb-document and the partner gateway, the fee schedule has no entity and no reference-table code, and no rule row of the Business Rules and Routing Logic v4 names a partner fee (GAP-3124; ASM-5432 to ASM-5437). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the fee-approval path of rwb-partner — the unchanged `partner_instruction` element with its fee and result fields, the two consumed owner contracts, the fee-approval entry, the rights and the error set of the act, the fakes and the four absences the path has**, so that **RWB-S9-E7012-APP and the wave 4 harness build against one fixed, testable contract on Day 1, and a fee field, a schedule version or a right can never drift between rwb-partner, rwb-case, rwb-document and rwb-decision without a failing build**.

The baseline is deliberately narrow: it declares one element of this service, two consumed rows and the absences the path has. It declares no operation, no event and no Schedule of its own.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy fee check of RWB-E7-012 ran inside one process and one schema: it read the partner, the instruction, the fee, the result, the schedule and the decision log without a boundary, and its two endpoints were partner-portal reads and writes of the same monolith. The target splits the facts: rwb-partner owns the panel, the instruction, its fee amount and its result code; rwb-case owns the case and, by the R3 default ruling, the reference data and lists of values (DP-07); rwb-document owns the upload link the claim's papers arrive through; rwb-decision owns the packages and the central ledger; and rwb-payment owns the money side of a fee (FEAT-PAY-05). Each boundary is a contract another team builds against, so the shapes have to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_partner`, login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules v1 §R4; context pack service row). It records that rwb-partner holds no grant on `rwb_case`, `rwb_document` or `rwb_decision`, so the case, the schedule, the upload link and the packages are consumed on their owners' contracts only.

Four points are carried as gaps and assumptions rather than decided quietly: no published operation serves the approval, because the Ownership Map gives S9 six operations and every one of them belongs to the panel, instruction, result or invoice story (GAP-3124; ASM-5432); no column and no list value of `partner_instruction` carries an approved fee, so the element is unchanged and the approval lives on its entry (ASM-5433); the fee schedule has no entity and no code in `LOV-REF-TABLE`, so its version and its read carry the placeholder (ASM-5434); and the plan's C and X rows are empty although TSD S9 T5.2.2 declares the rwb-document upload link as class C and the partner gateway as class X (ASM-5434).

The wave and the date are the plan's: this key is EP07, wave 4, release 31 May 2027, and rwb-partner is created in wave 4, so the business wave and the service wave are the same and no W-MAP conflict arises; the date is copied unchanged and marked tentative (ASM-5426).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case` and the reference data are P3's, `document` is P5's, `rule_row` and `decision_log_entry` are P7's and `proceeds` is P8's. This document never declares another service's table or operation as its own.
- The two consumed contracts of TSD S9 T5.2.2 — the rwb-document upload link (class C) and the partner gateway identity and MFA (class X) — are published with fakes; neither appears in the plan's C or X row, and both absences are recorded (GAP-3124; ASM-5434).
- The fee schedule is versioned reference data and is read on the rwb-case reference-data contract at a version; no entity for it exists in the logical data model and no code for it exists in `LOV-REF-TABLE`, so the version carries the placeholder (GAP-3124; ASM-5434).
- TSD S9 T6.1 is the only rights source for this service, and it has no row for the Finance and CFO delegate that FSD S9 A2.9.3.3 names as also using; the conflict is fixed here and not widened (GAP-3124; ASM-5436).
- The `partner`, `partner_instruction` and `partner_user` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The six operations of the service (API-S9-001 to API-S9-006) and the two events (EV-20 and EV-21) belong to the panel, instruction, result and invoice stories; this baseline names them and declares none of them.
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-partner for this step and record that it declares no operation for the fee approval, with the six operations of the service named and their first release.
2. Declare the `partner_instruction` element exactly as TSD S9 T3.1 gives it, and record that no property of it carries an approval, an approver or an approved instant.
3. Declare the two consumed rows with their class, their owner and their placeholders: the rwb-document upload link and the rwb-case reference-data read of the fee schedule.
4. Fix the fee-approval entry of DP-03 with its attributes, its write order and its failure behaviour.
5. Publish the rights of the claim, of the approval and of the read, and record the Finance and CFO delegate conflict between FSD S9 and TSD S9 T6.1.
6. Publish the error set, the status codes and the message IDs of the act and of the read.
7. Publish the fakes of 12.8 and the four absence tests: no operation, no event, no fee column and no Schedule.
8. Fix the naming baseline and the boundary, then tag the baseline and hand it to RWB-S9-E7012-APP and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation or an element carries a value outside a list of values | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC2, AC4, AC7 |
| X2 | A field is renamed or removed within major version 1, or a list value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3 |
| X5 | The document declares an approval operation, an event, a Schedule, a queue table, a foreign table property or a new column of `partner_instruction` | The absence and boundary tests fail the build | None | AC1, AC2, AC7 |
| X6 | The rights of the claim, of the approval and of the read are not the ones TSD S9 T6.1 declares, or a role the matrix does not carry is given a right | The access test fails the build | MSG-P4-002 | AC5 |
| X7 | The fee schedule, the fee amount or the approver is declared with a value no source gives, or as a schema default | The review fails the baseline; the element carries the placeholder | None | AC4, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-document and rwb-case only |
| Negotiable | The entry attribute names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S9-E7012-APP and the wave 4 harness on Day 1, and the rwb-document and rwb-case teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, five fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the fee-approval path of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner and partner_instruction is S9, of recovery_case and the reference data is P3, of document is P5, of rule_row and decision_log_entry is P7 and of proceeds is P8
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline provides no approval operation and records the six operations of the service with their first release (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares no operation whose behaviour is the approval of a partner fee
    Then it records GET /partners (API-S9-001, Partner portal R, E2), POST /cases/{caseId}/instructions (API-S9-002, C, E4), GET /partner/instructions (API-S9-003, R, E4), POST /partner/instructions/{instructionId}/accept (API-S9-004, U, E4), POST /partner/instructions/{instructionId}/results (API-S9-005, U, E4) and POST /partner/instructions/{instructionId}/invoices (API-S9-006, C, E6) as the panel, instruction, result and invoice stories', and the Ownership Map as giving S9 no seventh operation
    Then the act of approving a claim and the read of an approved claim carry the placeholder, with an error set of 400, 401, 403 with MSG-P4-002, 404, 409 and 503 and one message ID per condition (GAP-3124; ASM-5432)
    Then the absence test fails a build that declares an approval operation, a second base or a second topic

  Scenario: AC2 The partner_instruction element is declared unchanged and carries no fee status (new, D-RCV-60)
    Given the instruction section of the baseline
    When it is compared with TSD S9 T3.0, T3.1, T3.2 and T3.3 and with the API Specification's instruction element
    Then the partner_instruction element declares the nine properties of DF-PRT-008 to DF-PRT-016: id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code and fee_amount, with the types and lengths TSD S9 T3.1 gives them
    Then id, case_id, partner_id, instruction_type, instructed_at and status are required and due_at, result_code and fee_amount are optional, and state is declared as the standard record column of TSD S9 T3.0
    Then instruction_type is declared against LOV-INSTRUCTION, status against LOV-INSTR-STATUS with SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED, and none added, while fee_amount stays a decimal amount with no list
    Then the document records that no property of the element carries an approval, an approver, an approved instant or a fee status, that this step adds no column, no list value and no migration, and that the approval is carried on its entry (GAP-3124; ASM-5433)

  Scenario: AC3 The two consumed contracts and the fee-schedule read are declared with their class and their placeholders (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with TSD S9 T5.2.2 and with the R3 default ruling for reference data
    Then the partner upload link is declared as consumed from P5 rwb-document, class C, with a 2 s timeout, a breaker and a fake, and its operation name is Not specified in the source documents
    Then the fee schedule and the lists are declared as consumed from P3 rwb-case, class C, read at a version, and the entity, the version token and the operation name are Not specified in the source documents
    Then the partner identity and MFA of the partner gateway are recorded as class X, outside the Workbench and tracked only
    Then the document records that DP-07 and DP-11 are read and that DP-07 is not in this key's pattern set, and that the plan's C and X rows are empty although three rows are consumed (GAP-3124; ASM-5434)

  Scenario: AC4 The fee-approval entry is declared and written before anything else (new, D-RCV-60)
    Given the entry section of the baseline
    When it is compared with the local decision-record library and with the universal rows of the Business Rules and Routing Logic v4
    Then one approval entry is declared per instruction with the case reference, the instruction reference, the partner reference, the instruction type, the claimed fee amount, the amount the schedule allows, the schedule version, the result code, the rule ID with its package version, the approver and the decided-at instant
    Then the entry is written through the library on the shared rwb.decision-record.v1 before the approval is answered, and a failed write leaves everything unchanged with MSG-P7-003
    Then the approver is the Partner and agency manager, the record names R-UNI-28 where the partner is insolvent, and the rule ID of the fee check is Not specified in the source documents because no rule row names it (GAP-3124; ASM-5435)
    Then the document records that a fee amount, a schedule version or an approver is reference data or a rule row read with its version and never a schema default

  Scenario: AC5 The rights, the roles and the role conflict are fixed on the claim, the approval and the read (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T6.1 and with FSD S9 A2.9.3.3
    Then the invoice submission declares Partner portal right C and the result submission declares right U, both held by PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER and PT-RAMC RU, and the approval declares Partner portal right U held by RW-AGENCYMG CRUDA
    Then the read of the panel and of the instructions declares right R for the roles TSD S9 T6.1 gives it
    Then the document records that FSD S9 A2.9.3.3 names the Partner and agency manager primary and the Finance and CFO delegate as also using, that TSD S9 T6.1 carries no such role, and that the delegate therefore reads through a role holding R and no right is invented here (GAP-3124; ASM-5436)
    Then the access test fails a build that gives a role of the matrix a right the matrix does not give, or an unknown role a right

  Scenario: AC6 The entry element and the fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the instruction fake answers a DONE instruction of a synthetic case with a result_code and a fee amount equal to the amount the schedule allows, the same instruction with a smaller and a larger claim, and an instruction still IN_PROGRESS
    Then the reference-data fake answers the fee schedule at its version in force, a schedule with no version, and the four lists of TSD S9 T3.2
    Then the document fake answers a time-limited upload link and an expired one, the entry stub answers a healthy chain and a stopped chain, and the composite route fake answers the merged SCR-34 and SCR-35 read
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is published or scheduled (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1, the queue is rwb-partner and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_instruction and partner_user, and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, the reference data, document, rule_row, decision_log_entry, proceeds and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event, and names InstructionIssued (EV-20) and PartnerResultSubmitted (EV-21) as the instruction and result stories' (ASM-5432)
    Then the document declares no Schedule, no Quartz row and no shared job table, records that the Ownership Map gives S9 no job, and records that the InstructionWorkflow SLA timers are durable timers of the workflow and not Schedules
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-E7012-APP, whose single legacy criterion stays with the app story word for word, and they copy no criterion of the legacy story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The `partner_instruction` element is this service's and is declared exactly as TSD S9 T3.1 gives it, with no approval column, no approver column and no fee status | Context pack ownership row `partner_instruction`; TSD S9 T3.1, T3.2 and T3.3; DP-01 |
| BR2 | The approval is declared as an entry written before anything else, through the local library on the shared topic; a failed write changes nothing and answers MSG-P7-003 | DP-03; TSD S9 T2; legacy RWB-E7-012 AC1 and AC2 |
| BR3 | The fee schedule and the lists stay with rwb-case as reference data read at a version; the contract declares the read as consumed and declares no reference-data property | R3 default ruling; DP-07; TSD S9 T0.3; ASM-5434 |
| BR4 | The case stays with rwb-case: the contract declares no `recovery_case` property and no case write, and `case_id` is a cross-reference | Context pack ownership rows; TSD S9 T3.3; ASM-5434 |
| BR5 | The claim's papers stay with rwb-document: the contract declares the time-limited upload link as consumed and declares no `document` property | TSD S9 T5.2.2; DP-11 |
| BR6 | The packages and the central ledger stay with rwb-decision: the contract names no rule row and no ledger entry, and records that no rule row names a partner fee | Business Rules and Routing Logic v4; ASM-5435 |
| BR7 | No event belongs to this step: the contract declares no published and no consumed event, and names `InstructionIssued` (EV-20) and `PartnerResultSubmitted` (EV-21) as the instruction and result stories' | Event and Messaging Design v4; TSD S9 T5.3; ASM-5432 |
| BR8 | No Schedule belongs to this step: the instruction service levels are durable timers of `InstructionWorkflow` and the Ownership Map gives S9 no job | Context pack ownership rows (Jobs 0); TSD S9 T5.2.1; ASM-5432 |
| BR9 | The rights are TSD S9 T6.1's and nothing wider: C for the claim, U for the approval, R for the read, and the Finance and CFO delegate is recorded, not invented | TSD S9 T6.1; FSD S9 A2.9.3.3; ASM-5436 |
| BR10 | The state vocabulary is closed: the six INSTRUCTION states of TSD S9 T3.2 are declared and this step adds none | TSD S9 T3.2; ASM-5433 |
| BR11 | The amount is a decimal on the element and a value on the entry: no rate, no percentage and no fee amount is a schema default or a constant | FSD S9 BR-S9-009 |
| BR12 | No personal data in a schema, an example or a fake: identifiers, a code, an amount, an instant, a rule version and a state only, and the partner's name is a firm name and not a person | Template and Rules v1 §R7.2 (s17); LDM v8 |
| BR13 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules v1 §R4 |

### 9. State transitions

The lifecycle of this document, not of an instruction:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The unchanged element, the consumed rows, the entry and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the wave 4 harness, the rwb-document owner and the rwb-case owner accept the document and the fakes | Baselined |
| Baselined | Additive change | An attribute is added within major version 1 | Baselined |
| Baselined | Breaking change | An attribute is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | An approval operation, an event, a Schedule, a new column or a foreign table property | In review |

The INSTRUCTION machine of TSD S9 T3.2 is the app story's and this baseline declares it without moving any instruction: the six values are the vocabulary on which the `status` property is declared, and the approval adds no value to it (ASM-5433).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the publication of the approval operation and the reading of the delegate conflict |
| Consuming teams (the app story, the wave 4 harness, the rwb-document owner and the rwb-case owner) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an element or a fake, and that a firm name is not a person name |
| Finance and CFO delegate (named by FSD S9 A2.9.3.3, absent from TSD S9 T6.1) | Reads the claim and the approval through a role the matrix carries; the conflict is recorded, not resolved here (ASM-5436) |

The per-service login behind the security scheme of the document is named "the rwb-partner login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Instruction element | The nine columns of DF-PRT-008 to DF-PRT-016 as TSD S9 T3.1 gives them, unchanged: `id`, `case_id`, `partner_id`, `instruction_type`, `instructed_at`, `due_at`, `status`, `result_code`, `fee_amount` |
| Required flags | `id`, `case_id`, `partner_id`, `instruction_type`, `instructed_at` and `status` required; `due_at`, `result_code` and `fee_amount` optional |
| Lists of values | `LOV-INSTRUCTION` with COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST and SELL, `LOV-INSTR-STATUS` with SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED, `LOV-PARTNER-TYPE` and `LOV-PANEL`, all as TSD S9 T3.2 gives them |
| Partner element | The seven columns of DF-PRT-001 to DF-PRT-007 of the `partner` element, read only, with the firm's `partner_name` and never a person's name |
| Fee schedule | Read as reference data at its version; the entity, the version token and the operation name are Not specified in the source documents: no entity exists in the LDM v8 and no code exists in `LOV-REF-TABLE` (GAP-3124; ASM-5434) |
| Approval entry | The DP-03 attributes: case reference, instruction reference, partner reference, instruction type, the claimed amount, the amount the schedule allows, the schedule version, the result code, the rule ID with its package version, the approver and the decided-at instant; no column of `partner_instruction` carries any of them (ASM-5433) |
| Consumed document shape | The time-limited upload link of P5 rwb-document, with the document reference and the expiry; the operation name is Not specified in the source documents (GAP-3124; ASM-5434) |
| Not declared here | `recovery_case` and the reference data (P3), `document` (P5), `rule_row` and `decision_log_entry` (P7), `proceeds` (P8), every `v_ace_*` view (P1), and the six operations API-S9-001 to API-S9-006 as this step's own |

No new table, no new column and no migration is declared by this story. `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_partner` by the library's own migration (DP-03).

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). The Ownership Map gives this service exactly six operations, and every one of them belongs to another story of the service: `GET /partners` (API-S9-001, Partner portal R, first in E2) and `POST /cases/{caseId}/instructions` (API-S9-002, C, E4) to the panel and instruction stories, `GET /partner/instructions` (API-S9-003, R, E4) and `POST /partner/instructions/{instructionId}/accept` (API-S9-004, U, E4) to the instruction story, `POST /partner/instructions/{instructionId}/results` (API-S9-005, U, E4) to the result story and `POST /partner/instructions/{instructionId}/invoices` (API-S9-006, C, E6) to the invoice story. The approval act and the read of an approved claim have no published operation and carry the placeholder (GAP-3124; ASM-5432). A build that declares an approval operation here fails the absence test of AC1.

#### 12.2 REST operations consumed

| Method | Path | Owner | Class | Use in the baseline |
|---|---|---|---|---|
| The time-limited upload link of a claim's papers; operation name Not specified in the source documents (GAP-3124; ASM-5434) | `/api/recovery/document/v1` | P5 rwb-document | C | The document reference and the expiry the claim is checked and shown against; read only, faked |
| The fee schedule and the lists at their version; operation name Not specified in the source documents (GAP-3124; ASM-5434) | `/api/recovery/case/v1` | P3 rwb-case | C | The rate, the basis and the version the claimed amount is checked against, and `LOV-INSTRUCTION`, `LOV-INSTR-STATUS`, `LOV-PARTNER-TYPE` and `LOV-PANEL` |
| Partner identity and MFA of the partner gateway (FAPI 2.0) | The partner gateway in the DMZ | Partner gateway | X | Tracked only and outside the Workbench: the partner's identity is terminated at the DMZ and no partner identity is declared here |

Each REST row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020, DP-11). The two class C rows are contract dependencies that the plan's C row does not carry and the class X row is one its X row does not carry; the three absences are recorded (GAP-3124; ASM-5434). The case boundary behind the instruction is Temporal on the parent-and-child line, so it is declared in 12.5 and not as a REST row.

#### 12.3 Events published

None. The service publishes `InstructionIssued` (`rwb.partner.InstructionIssued.v1`, EV-20) and `PartnerResultSubmitted` (`rwb.partner.PartnerResultSubmitted.v1`, EV-21) on `rwb.partner.events.v1`, and both are the issue of an instruction and the submission of a result, published by the Epics 2, 4 and 6 stories of this service (Event and Messaging Design v4; TSD S9 T5.3). An approval issues no instruction and submits no result, so this baseline declares no producer, no envelope and no outbox row of its own, and the absence test of AC7 fails a build that adds one (ASM-5432).

#### 12.4 Events consumed

None. TSD S9 T5.2.2 records no event consumed by this service, and the two events of the service are published rather than consumed. TSD S9 T4 states that the module acts on events from P3, which contradicts the contract table; the baseline follows the contract table, declares no consumer group, no subscription and no inbox of its own, and records the disagreement as a gap (GAP-3124; ASM-5432).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction, started when an instruction is issued | `rwb-partner` in namespace `rwb-recovery` | The workflow of TSD S9 T5.2.1 that hosts the SLA timers and the fee-approval branch; its input, its signals and its outcome are declared, not built |
| The `feeApproval` branch of `InstructionWorkflow` | Workflow branch | `rwb-partner` | The path from the approval to the entry and the decision it returns |
| `readFeeClaim` | Activity | `rwb-partner` | The instruction, the fee schedule at its version and the result code in; the claim and the amount the schedule allows out |
| `evaluateFeeClaim` | Activity | `rwb-partner` | The claim in; the comparison, the rule ID with its version and the decision out |
| `recordFeeApproval` | Activity | `rwb-partner` | The entry and the decision out, one transaction |
| `issueInstruction`, `recordResult` | Activities, provided | `rwb-partner` | The two activities TSD S9 T5.2.1 publishes for S4 and S5; named here and declared unchanged |

The fee-approval branch, its three activities and their names are target design choices that no source document fixes; no activity is registered by this story. The SLA timers of `InstructionWorkflow` are durable timers and not Schedules.

#### 12.6 Schedules

None. The Ownership Map gives S9 no job and FSD S9 A2.9.4.4 declares no background event for the feature, so this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The instruction service levels are durable timers inside `InstructionWorkflow` (ASM-5432).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `partner` | S9 (`rwb_partner`) | The panel firm, its type, its panel status, its contract end and its score; read by the claim and the screen |
| `partner_instruction` | S9 (`rwb_partner`) | The instruction, its type, its due date, its status, its result code and its `fee_amount`; the element the baseline declares unchanged |
| `partner_user` | S9 (`rwb_partner`) | The partner user's binding to one firm and one partner role (LDM v8 DF-REF-212 to DF-REF-217); named as owned and given no element by this step |
| `decision_record` | PLT library, created in `rwb_partner` | The local hash-linked approval entry (DP-03) |
| `idempotency_key` | PLT library, created in `rwb_partner` | The key of the repeated approval and the decision it holds |
| `outbox_event` | PLT library, created in `rwb_partner` | Created in this schema by the library for the stories that publish; no row of it belongs to this step |

`recovery_case` and the reference data (P3), `document` (P5), `rule_row` and `decision_log_entry` (P7), `proceeds` (P8) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or records of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner instruction fake | The instruction `INS-2026-000712` of case `RW-2026-000712` at `DONE` with a `result_code` and a `fee_amount` equal to the amount the schedule allows; the same instruction with a smaller and a larger claim; an instruction at `IN_PROGRESS` with no result | AC2, AC6 |
| rwb-case reference-data fake | The fee schedule at its version in force, a schedule with no version in force, and `LOV-INSTRUCTION`, `LOV-INSTR-STATUS`, `LOV-PARTNER-TYPE` and `LOV-PANEL`; the entity, the version token and the operation name carry the placeholder (GAP-3124; ASM-5434) | AC3, AC6 |
| rwb-document upload-link fake | A time-limited upload link for a document reference and an expired link; the operation name carries the placeholder (GAP-3124; ASM-5434) | AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, AC6 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answer for the case, with the claim slice of this service read once | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. No package fake is declared, because no rule package carries a partner-fee row (GAP-3124; ASM-5435).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed, 1 tracked | The rwb-document upload link and the rwb-case fee schedule at its version; one hop, 2 s; the partner gateway is class X and tracked only |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 belong to the instruction and result stories; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 1 branch declared, 3 activities declared, 0 registered | `InstructionWorkflow` and its `feeApproval` branch on `rwb-partner`; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no instruction, no partner and no case. What it publishes is one OpenAPI 3.1 document, nine contract tables, the rights of the claim, the approval and the read, and five fakes.

**Deliverables.** The additive document `openapi/rwb-partner-v1.yaml` with the unchanged `partner_instruction` element and no approval operation, the contract README rows for the two consumed rows and their placeholders, the fee-approval schema of the library, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before anything else is answered. DP-13 moves the base of the service and adds no operation, because this step owns none. DP-19 is behind SCR-34 and SCR-35, whose screen model is the edge contract's. No other pattern is claimed: the reference data of rwb-case is a consumed contract (DP-07, recorded and not claimed) and the authorise contract of rwb-access (DP-08) is read for the rights the matrix gives, so neither appears in the metadata row and both are in the registers (GAP-3124; ASM-5434).

**Build steps**

1. Record the absence of an approval operation and the six operations as the panel, instruction, result and invoice stories', with the absent-operation test of AC1.
2. Publish the `partner_instruction` element unchanged with its nine properties, its six required flags and its lists, and record the no-fee-status rule of AC2.
3. Record the two consumed rows and the tracked external row of AC3 with their owner, their class, their budget and the placeholders.
4. Publish the approval-entry element of AC4, with the claim, the schedule version, the result code, the approver and the rule version, and validate it against the library schema.
5. Record the rights, the roles and the delegate conflict of AC5.
6. Publish the five fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every path and the drift test is green, and the app story and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of an element is absent or invalid, or a body fails schema validation, or a list value is outside its enumeration (VR-S9-009-1) | Enter {field}. |
| MSG-P4-002 | The role lacks the Partner portal right of the claim, of the approval or of the read, and an unknown role tries one of them | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The approval entry cannot be written before anything else | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three message IDs are those of the legacy message set of this key; the text is the legacy and FSD S9 wording, copied unchanged, and no message is reworded and no new one is added (ASM-5437). R-UNI-39's incident is raised by the platform on the same failure and is not a message of this service.

### 15. Screens and states

The contract serves the claim slice of SCR-34 Partner list and SCR-35 Placement and allocation through the gateway-bff composite route (DP-19). The route calls rwb-partner for the partner, the instruction and its fee, rwb-case for the case and the schedule, and rwb-document for the upload link; this baseline fixes the rwb-partner answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON (ASM-5432). The approval read behind the list is a placeholder, because no source publishes an operation for it. The partner's own claim screen, PRT-04 Invoice, submits the claim through API-S9-006 in the invoice story and is named here only as the source of the claim.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-012-01 | AC1, AC2 | Contract | The synthetic case `RW-2026-000712` and instruction `INS-2026-000712`; the contract half answers the unchanged element, the absent approval operation and the entry shape |
| TC-E7-012-02 | AC4 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the entry element |
| TC-E7-012-03 | AC5 | Contract | A role without the Partner portal right and an unknown role; the contract half answers the 403 with MSG-P4-002 and the rights of the claim, the approval and the read |
| TC-E7-012-04 | AC4, AC6 | Contract | A forced record failure and a drifted fake; the contract half answers the entry path and the drift test |
| TC-S9-E7012-CON-01 | AC1 | Contract | The document validates; no approval operation, no second base and no second topic, and the six operations are named with their first release |
| TC-S9-E7012-CON-02 | AC2 | Contract | The `partner_instruction` element validates with its nine properties, its six required flags and its lists; no approval column and no added state value |
| TC-S9-E7012-CON-03 | AC3 | Contract | The three consumed rows with their class and their placeholders; no document property and no reference-data property |
| TC-S9-E7012-CON-04 | AC4 | Contract | The entry element with the claim, the schedule version, the result code and the approver; the rule ID carries its placeholder |
| TC-S9-E7012-CON-05 | AC5 | Contract | Partner portal C for the claim and U for the approval; RW-AGENCYMG CRUDA; the delegate conflict recorded |
| TC-S9-E7012-CON-06 | AC6 | Contract | The five fakes match the document and a drifted fake fails the build |
| TC-S9-E7012-CON-07 | AC7 | Contract | The naming baseline; the absence test for an event, a second topic and a Schedule, and the boundary test for a foreign table property and a `v_ace_*` path |

The four legacy cases are the legacy cases of RWB-E7-012 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S9-E7012-APP and the wave 4 harness. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S9-E7012-CON-01` to `-07` are new. No `-ITG` copy is written here; the cross-service journey of the key belongs to RWB-ITG-E7012-ITG.

### 17. Guardrails

- No business value in the contract: the rate, the basis, the fee amount, the lists and the rule versions stay reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, a code, an amount, an instant, a rule version and a state only; a partner's registered name is a firm name and no person's name appears anywhere in the document.
- The case and the reference data stay with rwb-case, the documents with rwb-document and the packages and the ledger with rwb-decision: the document declares no `recovery_case`, no reference-data, no `document`, no `rule_row` and no ledger property (BR3, BR4, BR5, BR6).
- This step owns no operation and no event: the document declares none for it and records the six operations and the two events as other stories' (BR7, AC1, AC7).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- The `partner_instruction` element is declared unchanged: a build that adds an approval column, an approver or a fee status to it fails the absence test (BR1, ASM-5433).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row or a shared job table (BR8).
- The rights are TSD S9 T6.1's and are never widened in a contract; the delegate conflict is recorded, not resolved by invention (BR9, ASM-5436).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results (Must, E6) | The `fee_amount` and `result_code` the element declares, the schedule read at its version and the approval entry | TC-E7-012-01, TC-S9-E7012-CON-01, TC-S9-E7012-CON-03, TC-S9-E7012-CON-04 |
| REQ-S9-001 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit (Must, E6) | The unchanged `partner` and `partner_instruction` elements and the panel and instruction reads | TC-S9-E7012-CON-02, TC-S9-E7012-CON-05 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E7012-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-S9-E7012-CON-03 |
| ADR-022 | Local decision record plus central ledger | The approval entry and the central ledger of P7 | TC-S9-E7012-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-012, disposition Split (rework); feature FEAT-PRM-09 |
| Legacy criteria | AC2 of the legacy story, owned word for word by RWB-S9-E7012-APP; AC1 of the legacy story is owned by RWB-ITG-E7012-ITG; this baseline copies none of them |
| Test cases | The four legacy cases as the contract half, and the seven new contract cases TC-S9-E7012-CON-01 to -07 |
| Feature and screens | FEAT-PRM-09, SCR-34 Partner list, SCR-35 Placement and allocation and PRT-04 Invoice |
| Rules | R-UNI-28 read as the insolvency guard; no rule row names a partner fee, so the rule ID of the check carries the placeholder (ASM-5435) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the comparison, the entry and the refusal: RWB-S9-E7012-APP.
- The end-to-end approval journey across rwb-partner, rwb-case, rwb-document and rwb-decision: RWB-ITG-E7012-ITG.
- The panel, the instructions, their acceptance, the results and the invoices and their six operations: the Epics 2, 4 and 6 stories of this service.
- The fee schedule as versioned reference data and the lists of values: FEAT-PRM-02 and rwb-case (P3), whose entity and code this baseline does not publish (GAP-3124).
- The calculation of the fee due and the matching of a recovery: FEAT-PRM-07, built in Epic 6.
- The money side of a fee, the fee tables and the general ledger: FEAT-PAY-05 and rwb-payment (P8).
- The upload link, the documents and their retention: rwb-document (P5).
- The rule packages, their rows and the central ledger: rwb-decision (P7), which carries no partner-fee row today (ASM-5435).
- The gateway-bff composite route and the screen field list of SCR-34 and SCR-35: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
