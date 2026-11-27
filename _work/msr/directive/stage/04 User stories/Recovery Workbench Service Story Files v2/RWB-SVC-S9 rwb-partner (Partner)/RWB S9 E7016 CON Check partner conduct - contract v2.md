# RWB-S9-E7016-CON Check partner conduct - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7016-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Contract version | API Specification v5, rwb-partner.yaml; base /api/recovery/partner/v1 (DP-13) |
| Size | Not specified in the source documents (DOR-RWB-S9-E7016-CON-16); the squad sizes it at refinement |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-016 |
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
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the conduct-check path of rwb-partner, split from RWB-E7-016. It fixes the two reads that answer the effect of the check, the unchanged `partner` and `partner_instruction` elements, the sample element and the breach record element with their placeholders, the right of the unattended branch, the error set, the fakes, and the three absences the path has — no operation starts the check, no event carries a finding and no Schedule starts it — on the base `/api/recovery/partner/v1` (DP-13) behind the gateway-bff composite route (DP-19). The two table elements are declared unchanged, because no field of TSD S9 T3.1 carries a finding or a breach, and the effect is carried by `partner.panel_status` with SUSPENDED and `partner_instruction.status` with RECALLED. The sample of contacts and complaints has no entity, no field list and no named owner in any source, the sample size and period are unpublished, the word "upheld" has no definition and the request and answer shape of the re-selection command is unpublished (GAP-3132; ASM-5473, ASM-5475, ASM-5476 and ASM-5478). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E7016-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 16 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the conduct-check path of rwb-partner — the sample element, the breach record element, the unchanged `partner` and `partner_instruction` elements, the right of the unattended branch, the error set, the fakes and the three absences**, so that **RWB-S9-E7016-APP, the wave 4 harness and SCR-34 and SCR-35 build against one fixed, testable contract on Day 1, and a field, a status value, a right or a case command can never drift between rwb-partner, rwb-case and rwb-decision without a failing build**.

The baseline is deliberately narrow: it declares two of the service's six operations, two unchanged elements, one sample element with its placeholders, one record element and no command of its own. It declares no operation that starts the check, no event and no Schedule.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy conduct clause of RWB-E7-016 ran inside one process and one schema: it read the partner, the decision log and the rule rows without a boundary. The target splits them: rwb-partner owns the partner and the instruction, rwb-decision owns the UNIVERSAL package and the central ledger, rwb-access owns the roles, the rights and the lists of values, and the contacts, the notices and the complaints belong to other modules' reads. Each boundary is a contract another team builds against, so the shapes have to be fixed before the app story starts: the panel status and the instruction status a breach moves, the sample element, the breach record element and the right of an unattended branch.

The baseline also fixes the naming the checks require: schema `rwb_partner`, login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules v1 §R4; context pack service row). It records that rwb-partner holds no grant on `rwb_case`, `rwb_comms` or `rwb_decision`, so the case is commanded on the Temporal boundary, the sample arrives as another owner's answer and the package is loaded at its version.

Four points are carried as gaps and assumptions rather than decided quietly: the sample has no entity and no owner (GAP-3132; ASM-5473); the sample size and period are unpublished (ASM-5478); the word "upheld" has no definition (ASM-5476); and the case-side re-selection command has no published name or answer shape (ASM-5475).

The wave and the date are the plan's: this key is EP07, wave 4, release 31 May 2027, and rwb-partner is created in wave 4, so the two waves agree and the date is copied unchanged and marked tentative (U7, R7; ASM-5467).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case`, `queue`, `assignment` and `timer` are P3's, `rule_row` and `decision_log_entry` are P7's, `document` is P5's and `notice` is P6's. This document never declares another service's table or operation as its own.
- The sample boundary is declared with a fake so the element names no invented owner; it is not a row of this story's dependency list, which is None, and the absence is recorded (GAP-3132; ASM-5473).
- The UNIVERSAL package and the rows R-UNI-29, R-LIT-22, R-UNI-38, R-UNI-39 and R-UNI-45 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- TSD S9 T6.1 is the only rights source for this service; FSD S9 A2.13.3.3 names "None; runs unattended" as the primary actor and the Conduct and QA officer as also using, and the baseline declares exactly that and widens nothing.
- The `partner` and `partner_instruction` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The six operations of the service are the Ownership Map's and all six belong to the partner and instruction stories of this service; none is re-declared here as a conduct-check operation.
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-partner for this step and declare the two reads of the path, recording that no operation starts the check.
2. Declare the `partner` and `partner_instruction` elements exactly as TSD S9 T3.1 gives them, and record that no field of either carries a finding or a breach.
3. Declare the sample element with its reference, its period and its scope, and record that no source gives it a field list, an owner or a size.
4. Fix the breach record element with its attributes, its write order, its idempotency rule and its failure behaviour.
5. Publish the right of the reads and record that the check itself runs under the service identity and starts from no operation.
6. Publish the error set, the status codes and the message IDs of the reads and of the record, including the stale-batch message.
7. Publish the fakes of 12.8 and the three absence tests: no check operation, no event and no Schedule.
8. Fix the naming baseline and the boundary, then tag the baseline and hand it to RWB-S9-E7016-APP, the SCR-34 and SCR-35 slices and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation or an element carries a value outside a list of values | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC2, AC3, AC7 |
| X2 | A field is renamed or removed within major version 1, or a list value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed or commanded element has a field list, an owner or a name the sources do not give | The element carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC3, AC7 |
| X5 | The document declares an operation that starts the check, an event, a Schedule, a queue table, a foreign table property or a new column of `partner` or `partner_instruction` | The absence and boundary tests fail the build | None | AC1, AC2, AC5, AC7 |
| X6 | The rights of the reads are not the ones TSD S9 T6.1 declares, or the unattended branch is given a right a person holds | The access test fails the build | MSG-P4-002 | AC4 |
| X7 | The sample size, the sample period, a service level or a status value is declared with a value no source gives, or as a schema default | The review fails the baseline; the element carries the placeholder | None | AC2, AC3, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-case, rwb-comms and rwb-decision only |
| Negotiable | The sample element's attribute names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S9-E7016-APP, the SCR-34 and SCR-35 slices and the wave 4 harness on Day 1 |
| Estimable | One OpenAPI document, nine contract tables, six fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the conduct-check path of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner and partner_instruction is S9, of recovery_case and timer is P3 and of rule_row and decision_log_entry is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline declares the check as unattended and names the two reads that answer its effect (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /partners with the partner_code, partner_type, panel_status and contract_end of the partner and GET /partner/instructions with the case_id, instructed_at, due_at and status of each instruction
    Then it records POST /cases/{caseId}/instructions, POST /partner/instructions/{instructionId}/accept, POST /partner/instructions/{instructionId}/invoices and POST /partner/instructions/{instructionId}/results as the other four operations of the service, owned by the instruction stories of this key
    Then it declares no operation whose behaviour is the start of a conduct check or the raise of a breach, and records that the check runs unattended under the service identity with the trigger Not specified in the source documents (GAP-3132; ASM-5473)
    Then the absence test fails a build that declares a conduct-check operation, a second base or a second topic

  Scenario: AC2 The sample element carries its placeholders and owns nothing (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with FSD S9 A2.13, TSD S9 T3.1 and the Logical Data Model v8
    Then the sample element declares exactly four attributes, the partner reference, the sample period, the sample scope and the sample set with its case keys, and no value that the business owns is declared as a constant or a schema default
    Then the document records that the source gives the sample no entity, no field list and no owner, that rwb-partner reads the contacts and the complaints through their owners' reads, and that the sample size, the sample stratum and the sample period each carry Not specified in the source documents (GAP-3132; ASM-5473; ASM-5478)
    Then it declares no contact, notice or complaint property as this service's and no foreign table property
    Then the drift test fails a build that declares a contact, notice or complaint table or field as this service's own

  Scenario: AC3 The breach record element is declared and written before anything else (new, D-RCV-60)
    Given the record section of the baseline
    When it is compared with the local decision-record library and with R-UNI-29 and R-UNI-39
    Then one record is declared per check result with the partner reference, the check date, the sample set with its case keys, the findings, the rule ID R-UNI-29 with its package version, the actor and the upheld or cleared outcome
    Then the record is written through the library on the shared rwb.decision-record.v1 before the partner row, the recall set and the case requests, and a failed write leaves everything unchanged with MSG-P7-003
    Then the document records that the effect is carried by partner.panel_status with SUSPENDED and partner_instruction.status with RECALLED, that no column is added to either table, and that the word "upheld" has no definition in the sources and is declared as the person's outcome (ASM-5476)
    Then the service level is declared as R-UNI-29's same-day timer with its version and never a default
    Then a repeat of the same partner and check date answers the record already written and writes, suspends and escalates nothing (ASM-5479)

  Scenario: AC4 The right of the reads and of the unattended branch is fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T6.1 and with FSD S9 A2.13.3.3
    Then the two reads declare Partner portal right R, held by RW-AGENCYMG CRUDA, by the six officer roles at CRU, by RW-CASEOWN, RW-TEAMMGR, RW-LEGAL, RW-CONDUCT and the other R-only roles, and by the partner portal roles RU
    Then the document records that the check itself holds no right of a person, runs under the rwb-partner service identity with the same checks as NFR-051 requires, and is refused to no role because no role starts it
    Then the document records that RW-CONDUCT holds R only and that the Conduct and QA officer upholds or clears a finding on the task, not through an operation of this service
    Then the access test fails a build that gives a role a right the matrix does not give or gives the branch a right a person holds (ASM-5481)

  Scenario: AC5 Nothing is published and nothing is scheduled on this path (new, D-RCV-60)
    Given the event and schedule sections of the baseline
    When they are compared with the context pack ownership rows and with TSD S9 T5.3
    Then the document declares no published event and no consumed event for this path, names InstructionIssued (EV-20) and PartnerResultSubmitted (EV-21) as the instruction stories', and records that no event carries a finding or a breach (ASM-5480)
    Then the document declares no Schedule, no Quartz row and no shared job table, and records that the service level is a durable timer of InstructionWorkflow and that the Ownership Map gives S9 no job (ASM-5473)
    Then the absence test fails a build that declares an event, a second topic, a Schedule, a Quartz row or a shared job table

  Scenario: AC6 The elements and the fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the sample fake answers a sample with one contact finding and one complaint finding on case RW-2027-001601, and a clean sample
    Then the partner fake answers a partner of type AGENCY at ACTIVE, the same partner at SUSPENDED after an upheld breach, and one at EXITED with an empty recall set
    Then the instruction fake answers instructions at ACCEPTED and IN_PROGRESS on the case, the same at RECALLED after the breach, and one at DONE outside the recall set
    Then the package fake answers the UNIVERSAL package at its version with R-UNI-29, R-LIT-22, R-UNI-38, R-UNI-39 and R-UNI-45 and a package with no version in force, the entry stub answers a healthy chain and a stopped chain, the batch-status fake answers today's batch and a stale batch, the case fake answers an accepted and a refused re-selection, and the access fake answers RW-CONDUCT with R and a role with no right
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1, the queue is rwb-partner and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_instruction and partner_user, and recovery_case, queue, assignment and timer, rule_row and decision_log_entry, document, notice, the contacts, the complaints and every v_ace_* view are named as other owners' and are reached only through their contracts or the workflow boundary
    Then the document records that the plan's C row is empty although the path reads the sample through its owners' reads, the batch status through rwb-source-data and commands rwb-case (GAP-3132; ASM-5473; ASM-5475; ASM-5477)
    Then it records that the two unchanged elements and the two new elements are the whole surface of this path, and that no check operation, event or Schedule is declared (ASM-5482)

  Scenario: AC8 Each business rule of section 8 is traced to a criterion and a test (new, D-RCV-60)
    Given the business rules of section 8 with the rule IDs BR1 to BR14
    When each rule is compared with the criteria of section 7 and the test case rows of section 16
    Then each rule BR1 to BR14 names at least one criterion of this story and one test case row
    Then a rule that states an architecture constraint is proved by the boundary test or the guardrail test named in its row (TC-S9-E7016-CON-08)
    Then a rule with no criterion or no test case row fails the build

  Scenario: AC9 The error answers 401, 403 and 404 of the provided operations are declared (new, D-RCV-60)
    Given the provided operations of the baseline and the error set of the service
    When each provided operation is compared with the error answers of the baseline
    Then each provided operation declares a 401 answer for a request with no valid identity, a 403 answer carrying MSG-P4-002 for a request with no right, and a 404 answer for a reference that names no partner or instruction
    Then the 401 and 404 messages carry Not specified in the source documents (NEWAC-RWB-S9-E7016-CON-AC9)
    Then the error test fails a build where a provided operation lacks one of these status codes

  Scenario: AC10 A retried or timed-out activity is declared and repeats no write (new, D-RCV-60)
    Given the activities of the instruction workflow that the path consumes through its durable timer
    When a retried or timed-out activity is compared with the record and partner write order of AC3
    Then the retry and timeout values carry Not specified in the source documents (NEWAC-RWB-S9-E7016-CON-AC10)
    Then a retried activity repeats no write, by the same check as AC3 for a repeat of the same partner and check date
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-E7016-APP and they copy no criterion of the legacy story, whose AC2 stays with the app story word for word and whose AC1 stays with RWB-ITG-E7016-ITG.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The `partner` and `partner_instruction` elements are this service's and are declared exactly as TSD S9 T3.1 gives them, with no finding column and no breach column | Context pack ownership rows; TSD S9 T3.1 and T3.2; DP-01 | AC1, AC2; TC-E7-016-01 |
| BR2 | The effect is declared as a panel status and an instruction status: SUSPENDED against LOV-PANEL and RECALLED against LOV-INSTR-STATUS, and this step adds no value to either | TSD S9 T3.2; R-UNI-29; ASM-5476 | AC3; TC-S9-E7016-CON-03 |
| BR3 | The check result is declared as a record written before anything else, through the local library on the shared topic; a failed write changes nothing and answers MSG-P7-003 | DP-03; TSD S9 T2; R-UNI-39; legacy RWB-E7-016 AC2 | AC3; TC-E7-016-02, TC-S9-E7016-CON-03 |
| BR4 | The sample is a consumed element and not a table of this service: the contract fixes its reference, its period and its scope and carries the placeholder for its fields, its size and its owner | FSD S9 A2.13; TSD S9 T3.1; ASM-5473; ASM-5478 | AC2; TC-S9-E7016-CON-02 |
| BR5 | The case and its route state stay with rwb-case: the contract declares the re-selection as a Temporal command of R-UNI-45 and declares no `recovery_case` and no `timer` property and no case write | Context pack ownership rows; R-UNI-45; ASM-5475 | AC7; TC-S9-E7016-CON-07 |
| BR6 | The UNIVERSAL package and the central ledger stay with rwb-decision: the contract names R-UNI-29, R-LIT-22, R-UNI-38, R-UNI-39 and R-UNI-45 and declares no rule row and no ledger entry | Business Rules and Routing Logic v4; ASM-5474 | AC7; TC-S9-E7016-CON-07 |
| BR7 | No event belongs to this path: the contract declares no published event and no consumed event, and names `InstructionIssued` (EV-20) and `PartnerResultSubmitted` (EV-21) as the instruction stories' | Event and Messaging Design v5 EV-20 and EV-21; TSD S9 T5.3; ASM-5480 | AC5; TC-S9-E7016-CON-05 |
| BR8 | No Schedule belongs to this path: the service level is a durable timer of the workflow and the Ownership Map gives S9 no job | Context pack ownership rows (Jobs 0); FSD S9 A2.13.4.4; ASM-5473 | AC5; TC-S9-E7016-CON-05 |
| BR9 | The rights are TSD S9 T6.1's and nothing wider: Partner portal R for the reads, and the branch holds no right of a person and runs under the service identity | TSD S9 T6.1; FSD S9 A2.13.3.3; NFR-051 | AC4; TC-E7-016-03, TC-S9-E7016-CON-04 |
| BR10 | The stale batch is a declared condition of the path: where the data product is not today's the check records nothing and answers MSG-P1-001, and the batch status is consumed from rwb-source-data | VR-S9-013-1; DP-05; ASM-5477 | AC3; TC-S9-E7016-CON-09 |
| BR11 | No personal data in a schema, an example or a fake: a partner code, a partner type, case and instruction references, a status, a date and a rule version only | Template and Rules v1 §R7.2 (s17); LDM v8 | AC2; TC-S9-E7016-CON-02 |
| BR12 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules v1 §R4 | AC1; TC-S9-E7016-CON-01 |
| BR13 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 notes | AC7; TC-S9-E7016-CON-10 |
| BR14 | No sample size, sample period, service level or status value is a schema default or a constant | FSD S9 BR-S9-013; ASM-5478; DP-06; DP-07 | AC2; TC-S9-E7016-CON-11 |

### 9. State transitions

The lifecycle of this document, not of a contract:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the sample and record elements, the rights and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the SCR-34 and SCR-35 slices, the wave 4 harness and the rwb-case owner accept the document and the fakes | Baselined |
| Baselined | Additive change | An attribute is added within major version 1 | Baselined |
| Baselined | Breaking change | An attribute is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | A check operation, an event, a Schedule, a new column or a foreign table property | In review |

The `partner` and `partner_instruction` state machines are the app story's and this baseline declares their vocabularies without moving any row: SUSPENDED and RECALLED are the two values the path uses, and no value is added.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the correction of the sample element and the reading of the case command |
| Consuming teams (the app story, the SCR-34 and SCR-35 slices, the wave 4 harness and the rwb-case owner) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field enters an element or a fake and that no column is added |
| Compliance, the conduct and QA officer and the center of excellence | Confirm the conduct rule set the check evaluates and the outcome the word "upheld" carries |

The per-service login behind the security scheme of the document is named "the rwb-partner login (DP-02)" and is not part of this baseline.

Access to each operation of this baseline is checked by the rwb-access authorise check (DP-08); the baseline names that check and declares no check of its own.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Partner element | The seven columns of DF-PRT-001 to DF-PRT-007 as TSD S9 T3.1 gives them, unchanged: `id`, `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end`, `score` |
| Instruction element | The nine columns of DF-PRT-008 to DF-PRT-016, unchanged: `id`, `case_id`, `partner_id`, `instruction_type`, `instructed_at`, `due_at`, `status`, `result_code`, `fee_amount` |
| Lists of values | `LOV-PANEL` with ACTIVE, ON_NOTICE, SUSPENDED and EXITED; `LOV-INSTR-STATUS` with SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED; `LOV-PARTNER-TYPE` with AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC; `LOV-INSTRUCTION` with COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST and SELL, all as TSD S9 T3.2 gives them |
| Sample element | The partner reference, the sample period, the sample scope and the sample set with its case keys; the size, the stratum and the field list are Not specified in the source documents (GAP-3132; ASM-5473; ASM-5478) |
| Breach record | The record attributes of AC3, declared as a library object and not as a table of this service |
| Outcome | The upheld or cleared outcome of the person's task: the word has no definition in the sources and is declared as the person's outcome (ASM-5476) |
| Case command | The re-selection request of R-UNI-45, consumed from rwb-case on the Temporal boundary; its command name is Not specified in the source documents (GAP-3132; ASM-5475) |
| Not declared here | `recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice`, the contacts and the complaints (P6 and their owner), `partner_user` (no field list) and every `v_ace_*` view (P1) |

The field-level formats of the sample and of the record are settled in the baseline review; this story fixes the element names, the unchanged table elements, the lists and the optionality rule of BR13. **No new table, no new column and no migration** is declared by this story.

BR Field ID: each of the eight rows above has no BR Field ID in the source documents and carries Not specified in the source documents (DOR-RWB-S9-E7016-CON-7).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Use | Owner |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | The partner with its `partner_code`, `partner_type`, `panel_status` and `contract_end`, before and after a suspension | S9 rwb-partner |
| GET | `/api/recovery/partner/v1/partner/instructions` | The instructions of the caller's firm with their `case_id`, `instructed_at`, `due_at` and `status`, before and after a recall | S9 rwb-partner |

None for the check. The Ownership Map gives S9 exactly six operations and the other four — `POST /cases/{caseId}/instructions`, `POST /partner/instructions/{instructionId}/accept`, `POST /partner/instructions/{instructionId}/invoices` and `POST /partner/instructions/{instructionId}/results` — belong to the instruction stories of this key. No operation starts a conduct check, so the trigger carries the placeholder; a build that declares one here fails the absence test of AC1 (GAP-3132; ASM-5473).

#### 12.2 REST operations consumed

None. The step reads its own two tables, the package arrives loaded at its version and the case is reached on the Temporal boundary, so no REST row is consumed. The sample of contacts and complaints, the batch status and the case re-selection are consumed in fact — through their owners' reads, rwb-source-data and the Temporal boundary — and none is in this baseline's dependency list, which is None, and the absence is recorded (GAP-3132; ASM-5473; ASM-5475; ASM-5477).

#### 12.3 Events published

None. The service owns `InstructionIssued` (EV-20) on `rwb.partner.events.v1` — `instructionId`, `partnerId`, `type` and `dueOn` — and `PartnerResultSubmitted` (EV-21) — `instructionId`, `result` and `documents` — and both describe the issue of an instruction and the result the partner records, published by the instruction stories (Event and Messaging Design v5 EV-20 and EV-21; TSD S9 T5.3). A conduct finding is neither, so this baseline declares no producer, no envelope and no outbox row of its own, and the absence test of AC5 fails a build that adds one (ASM-5480).

#### 12.4 Events consumed

None. No source gives rwb-partner a consumed event for a conduct check: the sample arrives as another owner's answer, the package arrives loaded, and EV-21 is the result the partner portal records and not a finding. This baseline declares no consumer group, no subscription and no inbox of its own (ASM-5473; ASM-5480).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per partner holding its open instructions, continues-as-new | `rwb-partner` | The host of the `conductCheck` branch; its input, its signals and its outcome are declared, not built |
| The `conductCheck` branch of `InstructionWorkflow` | Branch of `InstructionWorkflow`; not a catalogued workflow | `rwb-partner` | The path from the trigger to the record, the finding, the person's outcome, the panel and instruction update, the case requests and the clock |
| `readConductSample` | Activity | `rwb-partner` | The partner in; the sample of contacts and complaints out |
| `evaluateConductRules` | Activity | `rwb-partner` | The package in force in; R-UNI-29, R-LIT-22 and R-UNI-38 with their versions out |
| `recordAndApplyBreach` | Activity | `rwb-partner` | The record, the partner status, the recall set and the clock start out, one transaction |
| `requestCaseReselection` | Activity | `rwb-partner` | One child command per affected case on the case boundary under R-UNI-45; the request in and the child result out |
| `breachClock` | Durable timer | `rwb-partner` | R-UNI-29's same-day service level and the 2 working days of R-UNI-45 with their versions; the expiry is the escalation |

No child workflow of this service exists in this path and no timer table is declared here: the `timer` rows are P3's. The branch and activity names are target design choices and no source document fixes them; no activity is registered by this story.

Workflow ID form: Not specified in the source documents (CG-ALL-12120). Start rule (start or signalWithStart, duplicate-start policy): Not specified in the source documents (CG-ALL-12120).

#### 12.6 Schedules

None. The Ownership Map gives S9 no job and FSD S9 A2.13.4.4 declares no background event for the feature, so this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The trigger is the branch start and the service level is a durable timer inside the branch (ASM-5473).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `partner` | S9 (`rwb_partner`) | The partner, its type, its panel status, its contract end and its score; the element the baseline declares unchanged and the app story writes `panel_status` of |
| `partner_instruction` | S9 (`rwb_partner`) | The work placed with the partner and its status; the element the baseline declares unchanged and the app story writes `status` of |
| `partner_user` | S9 (`rwb_partner`) | Owned per the Ownership Map; this path neither reads nor writes it, and TSD S9 T3.1 gives it no field list |
| `decision_record` | PLT library table, created in `rwb_partner`; not an LDM v9 or Data Classification v5 field | The local hash-linked entry of the check result (DP-03) |
| `idempotency_key` | PLT library, created in `rwb_partner` | The partner-and-check-date key of the repeated run |
| `outbox_event` | PLT library, created in `rwb_partner` | Created in this schema by the library for the stories that publish; no row of it belongs to this path |

`recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice`, the contacts and the complaints (P6 and their owner) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or facts of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Sample fake | A sample with one contact finding and one complaint finding on case `RW-2027-001601`, and a clean sample | AC2, AC6 |
| Partner fake | Partner `PTR-2027-001601` of type AGENCY at ACTIVE, the same partner at SUSPENDED after an upheld breach, and one at EXITED with an empty recall set | AC3, AC6 |
| Instruction fake | Instructions `INS-2027-001601` (ACCEPTED) and `INS-2027-001602` (IN_PROGRESS) on case `RW-2027-001601`, the same at RECALLED, and one at DONE outside the recall set | AC3, AC6 |
| rwb-decision package fake | The UNIVERSAL package at its version in force with R-UNI-29, R-LIT-22, R-UNI-38, R-UNI-39 and R-UNI-45; a package with no version in force | AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC3, AC6 |
| rwb-source-data batch-status fake | Today's batch, and a stale batch with its date and MSG-P1-001 | AC6 |
| rwb-case re-selection fake | The case accepting the request with its route reopened, the same case refusing it, and no answer inside 2 s; the command name carries the placeholder (GAP-3132; ASM-5475) | AC6, AC7 |
| rwb-access guard fake | RW-CONDUCT with Partner portal R, and a role with no right | AC4, AC6 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answers for the partner, its panel status and its instructions | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The sample element and the case command carry their placeholders until their owners publish them (GAP-3132; ASM-5473; ASM-5475).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 0 consumed | `GET /partners` and `GET /partner/instructions`; the check has no operation |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 are the instruction stories'; the check record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 4 activities, 1 durable timer and 1 child command per case declared, 0 registered | `InstructionWorkflow` and its `conductCheck` branch on `rwb-partner`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no partner, no instruction, no case and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables, the right of the reads, and nine fakes.

**Deliverables.** The additive document `openapi/rwb-partner-v1.yaml` with the two unchanged elements, the sample and record elements and no check operation; the contract README rows for the consumed sample element and its placeholders; the record schema of the library; and the nine WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before anything else is answered. DP-13 moves the base of the service and leaves the six operations to the partner and instruction stories. DP-19 is behind SCR-34 and SCR-35, whose screen model is the edge contract's. No other pattern is claimed: the case command is a Temporal boundary recorded and not claimed (ASM-5475), the sample is a consumed contract recorded and not claimed (ASM-5473), the rule package is loaded but adds no dependency row (DP-04 recorded and not claimed), and the lists of values are read at a version (DP-07 recorded and not claimed), so none of them appears in the metadata row.

**Build steps**

1. Record the absence of a check operation and the two reads of AC1, with the absent-operation test.
2. Publish the `partner` and `partner_instruction` elements unchanged with their properties, their required flags and their four lists, and record the no-finding-column rule of AC2.
3. Publish the sample element of AC2 with the owner, size and period placeholders and the consumed-contract row.
4. Publish the breach record of AC3, with the rule ID, the service level, the outcome and the transaction order, and validate it against the library schema.
5. Record the right of the reads and of the unattended branch of AC4.
6. Publish the nine fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every path and the drift test is green, and the app story, the SCR-34 and SCR-35 slices and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of an element is absent or invalid, or a body fails schema validation, or a list value is outside its enumeration | Enter {field}. |
| MSG-P4-002 | The caller lacks Partner portal R for the read of the partner, its panel status or its instructions | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The check record cannot be written before anything else | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product the sample or the batch status depends on is stale after a late or failed ACE batch (VR-S9-013-1) | {product} is from {date}. Today's load has not arrived. |

The first three IDs are those of the legacy message set of this key and the fourth is VR-S9-013-1's; the first three texts are copied unchanged, the fourth is copied from Error and Message Standard v4, and no message is reworded or added.

### 15. Screens and states

The contract serves SCR-34 Partner list and SCR-35 Placement and allocation through the gateway-bff composite route (DP-19). The route calls rwb-partner for the partner and its instructions, rwb-case for the case and its route state and rwb-decision for the decision records; this baseline fixes the rwb-partner answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The check itself has no screen, so the screen's act carries the placeholder of AC1 and the finding is read on the same two screens. The legacy screen table's two screens are accounted for: SCR-34 and SCR-35 belong to this service, and this story answers their finding-raised, suspended, recalled, re-selection-requested, refused, not-recorded, stale and unavailable states with the messages of section 14. SCR-34 and SCR-35 each carry the loading state of Screen Specifications v1; their empty, error and no access states are Not specified in the source documents (CG-ALL-12128; CG-ALL-12129).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-016-01 | AC1, AC2 | Contract | Partner `PTR-2027-001601` with instructions ACCEPTED and IN_PROGRESS on case `RW-2027-001601`; the contract half answers the two reads, the two unchanged elements and the absent check operation |
| TC-E7-016-02 | AC3 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the record element |
| TC-E7-016-03 | AC4 | Contract | RW-CONDUCT with Partner portal R and a role with no right; the contract half answers the 403 with MSG-P4-002 and the service-identity rule |
| TC-E7-016-04 | AC3, AC6 | Contract | A forced record failure and a drifted fake; the contract half answers the record path and the drift test |
| TC-S9-E7016-CON-01 | AC1 | Contract | The document validates; no check operation, no second base and no second topic, and the four other operations named as the instruction stories' |
| TC-S9-E7016-CON-02 | AC2 | Contract | The sample element with its four attributes and the owner, size and period placeholders; no contact, notice or complaint property |
| TC-S9-E7016-CON-03 | AC3 | Contract | The record with R-UNI-29 and its version, the service level, the outcome and the transaction order |
| TC-S9-E7016-CON-04 | AC4 | Contract | Partner portal R for the reads; the branch holds no right of a person; RW-CONDUCT holds R only |
| TC-S9-E7016-CON-05 | AC5 | Contract | No event, no consumed event, no Schedule and no Quartz row; the two events named as the instruction stories' |
| TC-S9-E7016-CON-06 | AC6 | Contract | The nine fakes match the document and a drifted fake fails the build |
| TC-S9-E7016-CON-07 | AC7 | Contract | The naming baseline; the absence test for an event, a second topic, a Schedule and a Quartz row, and the boundary test for a `v_ace_*` path and a foreign table property |
| TC-S9-E7016-CON-08 | AC7 | Contract | The boundary test for the tables of §12.7: each table with its owner; a table or a column outside the declared list fails the build |
| TC-S9-E7016-CON-09 | AC3 | Contract | A data product that is not today's: nothing is recorded, MSG-P1-001 is answered and the batch status is read from rwb-source-data |
| TC-S9-E7016-CON-10 | AC7 | Contract | A schema change that is not additive within major version 1 fails the build; a breaking change is a new major version |
| TC-S9-E7016-CON-11 | AC2 | Contract | No sample size, sample period, service level or status value appears as a schema default or a constant |
| TC-S9-E7016-CON-12 | AC8 | Contract | Each rule BR1 to BR14 traced to a criterion and a test case row; the boundary test for the architecture rules |
| TC-S9-E7016-CON-13 | AC9 | Contract | The provided operations answer 401, 403 with MSG-P4-002 and 404; the 401 and 404 messages carry the placeholder |
| TC-S9-E7016-CON-14 | AC10 | Contract | A retried activity and a timed-out activity: a repeat of the same partner and check date writes nothing; retry and timeout values carry the placeholder |

The four legacy cases are the legacy cases of RWB-E7-016 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S9-E7016-APP and by RWB-ITG-E7016-ITG. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The fourteen cases `TC-S9-E7016-CON-01` to `-14` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here.

### 17. Guardrails

- No business value in the contract: the sample size, the sample period, the service level, the status values, the lists and the rule rows stay reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: a partner code, a partner type, case and instruction references, a status, a date and a rule version only.
- The case and its timers stay with rwb-case and the package and the ledger with rwb-decision: the document declares no `recovery_case`, `timer`, `rule_row` or ledger property (BR5, BR6).
- The sample is a consumed element: the document declares no contact, notice or complaint property of this service and names their owners (BR4).
- This path owns no check operation and no event: the document declares none for it and names the six operations and the two events as the service's and the instruction stories' (BR7, AC1).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- The two table elements are declared unchanged: a build that adds a finding column, a breach reference or a status value fails the absence test (BR1, BR2).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row or a shared job table (BR8).
- The rights are TSD S9 T6.1's and are never widened in a contract; the unattended branch holds no right of a person and is tested as such (BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S9-007 | Partner performance, conduct and complaint data are reported to the partner review forum (Must, E7) | The record, the finding and the panel status the review reads | TC-E7-016-01, TC-S9-E7016-CON-03 |
| REQ-S9-006 | A partner panel exit, a declared conflict of interest, insolvency or an upheld conduct breach recalls every open case held by that partner (Must, E7) | The SUSPENDED panel status, the RECALLED instruction status and the case command | TC-S9-E7016-CON-02, TC-S9-E7016-CON-03 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E7016-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two reads and the consumed sample with its budget and breaker | TC-S9-E7016-CON-01, TC-S9-E7016-CON-02 |
| ADR-022 | Local decision record plus central ledger | The check record and the central ledger of P7 | TC-S9-E7016-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-016, disposition Split (rework); feature FEAT-PRM-13 |
| Legacy criteria | AC2 of the legacy story, owned word for word by RWB-S9-E7016-APP; AC1 by RWB-ITG-E7016-ITG; this baseline copies none of them |
| Test cases | The four legacy cases as the contract half, and the seven new contract cases TC-S9-E7016-CON-01 to -07 |
| Feature and screens | FEAT-PRM-13, SCR-34 Partner list and SCR-35 Placement and allocation |
| Rules | R-UNI-29, R-LIT-22, R-UNI-38, R-UNI-39 and R-UNI-45 named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the sample, the rules, the record and the breach: RWB-S9-E7016-APP.
- The end-to-end proof of the legacy key through the real contracts: RWB-ITG-E7016-ITG.
- The contacts, the notices and the complaints themselves and their repositories: rwb-comms (P6) and the complaint owner.
- The monthly scorecard and the partner review (FEAT-PRM-08, FEAT-PRM-10), the notice on a missed target (FEAT-PRM-11) and the contract end (FEAT-PRM-12).
- The receipt of a partner result onto the case and the issue of an instruction: the instruction stories of this service.
- The case of record, its route state and its timers, and the re-selection itself: rwb-case (P3), which applies the command this baseline declares.
- The UNIVERSAL package, its rule rows and the central ledger: rwb-decision (P7). The roles, the rights and the lists of values: rwb-access (P4).
- The partner gateway and FAPI 2.0: the edge stories' own scope.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
