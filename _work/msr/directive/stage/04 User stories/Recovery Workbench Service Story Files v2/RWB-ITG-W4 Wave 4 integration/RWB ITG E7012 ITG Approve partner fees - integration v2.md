# RWB-ITG-E7012-ITG Approve partner fees

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7012-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E7012-ITG-16); the squad sizes it at refinement |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-ITG-E7012-ITG-14); confirm with the epic design record |
| Depends on (build) | RWB-S9-E7012-APP (not built yet) |
| Contract dependencies | RWB-S9-E7012-CON |
| Contract version | v1, as the /v1 path of each API read in section 7 gives |
| Contract fake library version | Not specified in the source documents (DOR-RWB-ITG-E7012-ITG-22) |
| Integration dependencies | RWB-S9-E7012-APP |
| Reference data and parameters | Parameters: Not specified in the source documents (DOR-RWB-ITG-E7012-ITG-20); reference-data contract DP-06 and DP-07 |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-012 as the wave 4 integration proof of the partner fee approval, driven from the instruction and the result through rwb-partner and observed across rwb-partner, rwb-payment, rwb-decision and rwb-case; the build of the approval itself is RWB-S9-E7012-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E7012-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 6 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the fee claim to be checked against the contracted schedule and the recorded result and then approved, with the approval recorded once and the rule version it used, proved end to end against the real services from the instruction onwards**, so that **partners are placed, paid and measured by rule**.

This story builds the wave 4 integration harness and the evidence only. The fee approval, the check against the schedule and the decision record are built by S9 rwb-partner in RWB-S9-E7012-APP and its CON story; the schedule the claim is checked against is the partner's contracted fees held by S9, and the money the result is matched against is P8's proceeds record, which is P8's own product. The harness reads the instruction, submits one result and one invoice through the owner's partner-portal operations, reads the approval back through the decision log, and writes a run report per instruction. It writes no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A partner can do the work, the result can be recorded, and the fee can still be paid twice, paid against a schedule that was never contracted, or never recorded at all. That is the failure this story is written against. The instruction places the work with the partner (Temporal and Drools design slide 25, step 3, EV-20); the result comes back through the partner portal (step 4, EV-21); the fee is checked against the contracted schedule and the result and then approved (step 6, FEAT-PRM-09, REQ-S9-004). If the check is not against the contracted schedule, an agency is paid on a rate nobody agreed; if it is not against the recorded result, it is paid on work the bank cannot show was done; if the approval is not recorded with its rule version, the payment cannot be defended to an auditor or replayed after the rules change.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13); there is no in-process call and no second hop. The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). The proceeds read is P8's own contract and the schedule and the result are S9's, so the harness never reads another service's tables (DP-01). The partner portal is the external channel in front of rwb-partner (Arch v5 slide 17), and the run proves the approval through the decision log and the invoice submission outcome, because the Ownership Map publishes no fee-approval operation and no invoice read for this step. The universal rules R-UNI-25, R-UNI-26, R-UNI-28 and R-UNI-29 decide what happens to the work around the fee, and the harness proves a fee is never approved for work that was recalled or stopped.

This story builds the wave 4 integration harness and the evidence only. The approval, the check against the schedule and the result, and the decision record are RWB-S9-E7012-APP's, and the run proves them without owning them.

### 3. Preconditions

- The published contracts of S9 rwb-partner (partners, instructions, results, invoices), P8 rwb-payment (proceeds), P7 rwb-decision (the decision log), P3 rwb-case (the case) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- S9 owns the partner, the partner instruction, the result, the invoice, the fees and the scorecards in `rwb_partner` (Arch v5 slide 41, slide 17), so the schedule and the result the claim is checked against have one named owner.
- The instruction is placed and its result is recorded before this story runs: the instruction lifecycle is InstructionWorkflow on `rwb-partner` with its SLA timers and its `issueInstruction` and `recordResult` steps (Arch v5 slide 17), and the harness observes that workflow and builds none of it.
- RWB-S9-E7012-APP owns the approval, the check against the schedule and the decision record; until it lands, the partner fixture of §12.8 stands in for its effect and the story is reported as a stub pass.
- The fee calculation that produces the claim is FEAT-PRM-07 (E6, S9) and is out of scope here; the fixture holds a claim that is already calculated, so this story never asserts a rate, an amount or a formula.
- The instruction, result and invoice are S9's; the proceeds record is P8's; the decision log entry and the rule rows are P7's; the case is P3's. The harness reads them only through those contracts and never from a schema.
- The harness environment and base hosts, the fixture layout, the synthetic keys, the fee claim and schedule answer shape, the evidence format and retention, and the pass or fail gate: Not specified in the source documents (GAP-0473; ASM-0665).
- The synthetic partner, its contract, the instruction, the recorded result, the invoice and the case are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S9-E7012-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: partner `PRT-SYN-0007` with its partner_code and contract as data, case `RW-2027-000901`, instruction `INS-SYN-2027-0007` for that partner and case with its instruction_type, instructed_at and due_at, the recorded result of the work, and the invoice the partner has submitted against the instruction. On Day 1 the stub of §12.8 returns the same records.
2. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and names the case, its stage and its state before the approval, so a change after the run has a baseline.
3. Harness: reads `GET /api/recovery/partner/v1/partners` and asserts one partner, its partner_code, partner_type, panel_status and contract, and names the contracted schedule the claim is checked against (AC2).
4. Harness: reads `GET /api/recovery/partner/v1/partner/instructions` and asserts one instruction for the partner, its instruction_type, its due_at, its status and the recorded result_code, and names that result as the one the claim is checked against (AC2).
5. Harness: submits the result through `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results` with one Idempotency-Key, and asserts the answer carries the same instruction and result and that a repeat of the same key changes nothing (AC3).
6. Harness: submits the invoice through `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/invoices` with one Idempotency-Key, and asserts the answer, one invoice and its submission outcome; the map publishes no invoice read, so the submission answer is the outcome the run records (AC2, AC3).
7. Harness: reads `GET /api/recovery/payment/v1/proceeds` and names the proceeds record the result is matched against, so the claim is checked against money the bank can show was recovered (AC2).
8. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts exactly one entry for the approval, with its rule_id and rule_version, and no second entry after a re-read (AC1, AC3).
9. Harness: counts one `rwb.partner.InstructionIssued.v1` and one `rwb.partner.PartnerResultSubmitted.v1` on `rwb.partner.events.v1`, asserts the consumer effect through `GET /api/recovery/case/v1/cases/{caseId}`, then replays both events and asserts the case and the instruction are unchanged, because the inbox holds one processed row per consumer (AC3).
10. Harness: reads the decision record as published on `rwb.decision-record.v1` as `rwb.decision.DecisionRecorded.v1` and asserts it carries the approval and its rule version, and that rwb-decision accepted it once (AC1, AC3).
11. Harness: observes InstructionWorkflow for the instruction in the `rwb-recovery` namespace: its SLA timer, and its `issueInstruction` and `recordResult` steps, which are S9's and are not built here. The observation is read from the workflow's history, not from an operation the map publishes.
12. Harness: forces a decision-record failure at the record hop through the run environment's fault switch, attempts the approval, and asserts it stops with MSG-P7-003 and that the instruction, the invoice, the case and the decision log are unchanged (AC4).
13. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller holding Partner portal R but not U, then submits the same result and the same invoice and asserts 403 with MSG-P4-002 and no change to the instruction, the invoice or the decision log (AC5).
14. Harness: writes one run report per instruction and invoice, keyed by story and instruction id, naming the contract version of each hop, whether the hop was a stub or the owner, the schedule named, the result named, the proceeds named, the decision entry with its rule version, both event counts, the workflow run, and the gate verdict.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E7-012-01-ITG (ITG AC1) | AC1 |
| X2 | The approval is written without the schedule or the result it was checked against being named | The run fails on AC2 and the report names the partner read, the instruction read and the proceeds read behind the check | None | TC-E7-012-01-ITG (ITG AC2) | AC2 |
| X3 | The same invoice is approved twice, or a second decision entry appears | The run fails on AC3 and the report names both entries and the invoice id, with the Idempotency-Key each submission carried | None | TC-E7-012-01-ITG (ITG AC3) | AC3 |
| X4 | The result is submitted and InstructionWorkflow does not record it, or the instruction stays at its issued state | The run fails on AC3 and the report names the instruction, its status, the workflow run and the activity that did not step | None | TC-E7-012-01-ITG (ITG AC3) | AC3 |
| X5 | A partner event is published more than once, or a replay changes the case | The run fails on AC3 and the report names the topic, the event id and the consumer | None | TC-E7-012-01-ITG (ITG AC3) | AC3 |
| X6 | The decision record cannot be written and the approval completes anyway | The run fails on AC4 and the report names the instruction, the invoice, the state and the missing record; a partial approval is never reported as a pass | MSG-P7-003 | TC-E7-012-02-ITG (ITG AC4) | AC4 |
| X7 | A caller without Partner portal U is allowed to submit the result or the invoice, or a submission short of a required field is accepted | The run fails on AC5 and the report names the caller role, the right, the operation and the answer; a 200 is a failure even when no data changed | MSG-P4-002 (expected, and missing); MSG-GEN-001 (expected, and missing) | TC-E7-012-03-ITG (ITG AC5) | AC5 |
| X8 | A stub pass is reported as a real pass while RWB-S9-E7012-APP is not live | The run fails on AC1 and the report names the hop that was a stub and the owner it waits for | None | TC-E7-012-04-ITG (ITG AC4) | AC1 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S9-E7012-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the fault switch, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The claim is proved to be checked against a named schedule and a named result, the approval is proved to be recorded once with its rule version, and the refused and failed paths are proved to change nothing |
| Estimable | One runner, one stub set, one partner fixture, one instruction and invoice, one proceeds read, one event observer, one workflow observation and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S9-E7012-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Approve partner fees - wave 4 integration harness

  Background:
    Given the synthetic partner "PRT-SYN-0007" holds a contract and is on the panel
    Given the instruction "INS-SYN-2027-0007" is placed with that partner on case "RW-2027-000901" and its result is recorded
    Given the invoice against that instruction is held in the fixture as data

  Scenario: AC1 Approve partner fees (legacy RWB-E7-012 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then checks the fee claim against the schedule and the result, and approves it
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The claim is checked against a named schedule and a named result (new, D-RCV-60)
    Given the instruction "INS-SYN-2027-0007" with its recorded result and the invoice against it
    When the fee claim is checked against the contracted schedule and the recorded result
    Then the schedule is read through GET /api/recovery/partner/v1/partners and the result through GET /api/recovery/partner/v1/partner/instructions
    And the money the result is matched against is read through GET /api/recovery/payment/v1/proceeds
    And the schedule, the result and the proceeds record are each named in the run evidence
    And the harness asserts the comparison and the naming, and never a rate or an amount of its own

  Scenario: AC3 The approval is recorded once with its rule version (new, D-RCV-60)
    Given the instruction and its invoice are submitted for approval
    When the approval is taken
    Then one entry for the approval is written to the decision log with its rule_id and rule_version
    And a re-read of GET /api/recovery/decision/v1/decision-log?caseId={caseId} returns no second entry
    And "rwb.decision.DecisionRecorded.v1" is published once on "rwb.decision-record.v1"
    And "rwb.partner.InstructionIssued.v1" is published once on "rwb.partner.events.v1"
    And "rwb.partner.PartnerResultSubmitted.v1" is published once on the same topic
    And a replay of either partner event leaves the case and the instruction unchanged

  Scenario: AC4 A forced decision-record failure stops the approval with nothing changed (new, D-RCV-60)
    Given the decision record cannot be written for the approval
    When the approval is taken
    Then the approval stops with "MSG-P7-003"
    And the instruction, the invoice, the case and the decision log are unchanged
    And no partner event is published for the stopped attempt

  Scenario: AC5 A caller without Partner portal U is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-CASEOWN" holding Partner portal R and not Partner portal U
    When the caller submits the result or the invoice
    Then the answer is 403 with "MSG-P4-002"
    And the instruction, the invoice and the decision log are unchanged

  Scenario: AC6 Each business rule in section 8 is asserted here or named as evaluated in RWB-S9-E7012-APP, and none is changed (new, D-RCV-60)
    Given the business rules in section 8 with their Covered by entries
    When the harness run is checked against them
    Then BR1, BR7 and BR8 are each asserted by the criterion their Covered by entry names
    And BR2 to BR6 are each named as evaluated in RWB-S9-E7012-APP and are asserted by no step of this harness
    And the harness writes no rule, fee or threshold of its own

  Scenario: AC7 A consumed call that fails or does not answer within 2 s stops the fee check with nothing changed (new, D-RCV-60)
    Given one consumed read of the schedule, the result or the proceeds fails or does not answer within 2 s
    When the fee claim is checked
    Then the check stops and no approval is written
    And the instruction, the invoice, the case and the decision log are unchanged
    And no second hop is made to the same path
    And the run evidence names the call that failed
```

Legacy AC2 (the decision log cannot be written) is owned by RWB-S9-E7012-APP, and this story asserts the same failure where the approval would otherwise complete, through AC4.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Fees are calculated from the contracted schedule and paid against recorded results | REQ-S9-004 | AC2, AC6 |
| BR2 | Every partner type is managed on the same six points, of which the contract and fees and the performance review are the two this run touches | REQ-S9-001 | AC6 (named only; evaluated in RWB-S9-E7012-APP) |
| BR3 | When the partner misses the service level on the portal, the work is chased once, then recalled and re-selected on the scorecard, and no fee is approved for work that was recalled | R-UNI-25 | AC6 (named only; evaluated in RWB-S9-E7012-APP) |
| BR4 | When the partner leaves the panel or the contract ends, every open case held by that partner is recalled and re-selected inside five working days, and no fee is approved after the recall | R-UNI-26 | AC6 (named only; evaluated in RWB-S9-E7012-APP) |
| BR5 | When the partner enters insolvency, the work is recalled, the documents and any cash held are secured, and fee payments stop the same day | R-UNI-28 | AC6 (named only; evaluated in RWB-S9-E7012-APP) |
| BR6 | When a conduct or complaint breach is upheld, allocation is suspended, the affected cases are recalled and the matter is reported to the partner review the same day | R-UNI-29 | AC6 (named only; evaluated in RWB-S9-E7012-APP) |
| BR7 | Every call the harness makes is one hop on `/api/recovery/<short>/v1` with a 2 s budget and no second hop | DP-11, DP-13 | AC2, AC6 |
| BR8 | The approval is recorded through the local decision-record library on `rwb.decision-record.v1`, and nothing changes when the record cannot be written | DP-03; legacy Principle 5, TC-E7-012-04 | AC3, AC4, AC6 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E7012-APP, and the fee calculation is FEAT-PRM-07.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| SENT | `PartnerResultSubmitted` on `rwb.partner.events.v1` | the partner records the result on the portal, on the same day | DONE |
| DONE | `DecisionRecorded` on `rwb.decision-record.v1` | the fee claim matches the contracted schedule and the recorded result, and the decision record is written | DONE, with the approval held in the decision log |

SENT and DONE are LOV-INSTR-STATUS values of DF-PRT-014, and S9 rwb-partner is their owner. They follow the two steps of the S9 journey in Temporal and Drools design slide 25 (step 3, instruction sent, EV-20; step 4, result via portal, EV-21) and the fee approval at step 6 (FEAT-PRM-09); the event names in the table are the published events of Arch v5 slides 17 and 42, not codes this story makes up. The fee approval has no separate instruction status: it is the decision record written for the instruction, read through the decision log, and the harness invents no state code beyond the LOV values and the events the sources give. The harness changes no state: every change in the table is made by S9 through InstructionWorkflow and the partner-portal operations, and a state the harness had set by hand would prove nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Partner and agency manager | Owns the fee approval; holds Partner portal R and U; is the role the journey is written for |
| RW-NPAMGR, RW-AGENCYMG, RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE, RW-GUARANT and PT-AGENCY | Hold Partner portal U and may approve or submit where their scope allows, per the legacy permission table |
| RW-CASEOWN and the other holders of Partner portal R | Read the partner and the instruction; RW-CASEOWN is the refused caller of AC5 because it does not hold U |
| Head of the partner type | Owns the insolvency stop of R-UNI-28, which stops fee payments |
| QA lead | Owns the harness configuration, the fixtures, the fault switch, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S9 holds the partner, the instruction, the result, the invoice and the fees and runs InstructionWorkflow, P8 holds the proceeds, P7 holds the decision log, P3 holds the case and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | partner_code, partner_name, partner_type, panel_status, contract_end | Read through the rwb-partner contract |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read through the rwb-partner contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, event_code | Read through the rwb-decision contract |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code | Read through the rwb-case contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The partner and the instruction are S9's, the case is P3's, and the decision log entry and the rule rows are P7's; the proceeds record the result is matched against is P8's and is read through `GET /api/recovery/payment/v1/proceeds`, whose rows are not named here because this story cites only the field IDs the dictionary gives for the four entities above. The harness owns no table and writes no row. The fee amount of DF-PRT-016 is read as the claim carries it; the harness asserts the comparison and the naming, never a rate, an amount or a business value of its own.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The partner, its panel status and its contract, and the schedule the claim is checked against (AC2) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instruction, its status and the recorded result the claim is checked against (AC2, AC3) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/results` | S9 rwb-partner | Submits the result once, and is the refused and failed operation of AC4 and AC5 (AC3, AC4, AC5) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/invoices` | S9 rwb-partner | Submits the invoice once; its answer is the invoice submission outcome, because the map publishes no invoice read (AC2, AC3) |
| GET | `/api/recovery/payment/v1/proceeds` | P8 rwb-payment | The proceeds record the result is matched against (AC2) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | Exactly one approval entry with its rule version, and no second entry after a re-read (AC1, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state before and after the submission and the replay (AC3, AC4, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a submission (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19). The Ownership Map publishes no fee-approval operation and no invoice read for this step, so the approval is asserted through the decision log and through the invoice submission outcome, and never through an endpoint that does not exist. The legacy permission table of RWB-E7-012 carries Partner portal R and U, the S9 TSD publishes the invoice operation with Partner portal C (API-S9-006), and the run records the right each operation answered with and asserts U on the result path, which is the right AC5 names. The fee calculation itself is FEAT-PRM-07 and is not called here.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | S9 rwb-partner | Counts one publication when the instruction is issued, and proves a replay changes nothing (AC3) |
| `rwb.partner.PartnerResultSubmitted.v1` | `rwb.partner.events.v1` | S9 rwb-partner | Counts one publication when the result is recorded, and proves a replay changes nothing (AC3) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | S9 rwb-partner through the local decision-record library (DP-03) | Proves the approval and its rule version were published once and accepted by rwb-decision (AC1, AC3, AC4) |

The harness subscribes to both topics under one consumer group of its own, counts publications and replays each partner event once. The consumer effect it reads is the case through the rwb-case operation of §12.2 and the instruction through the S9 instruction read; the inbox row counts of rwb-litigation, rwb-asset and rwb-case, which Arch v5 slide 43 gives as the consumers of `PartnerResultSubmitted`, come from the consumer evidence in the run fixture, because neither rwb-litigation nor rwb-asset exposes an operation in this story.

#### 12.5 Workflows and activities

None added. The harness exercises InstructionWorkflow, S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace, and observes its SLA timers and its `issueInstruction` and `recordResult` activities (Arch v5 slide 17). They are stated here as observed and not built here; no workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. InstructionWorkflow is started by the instruction and runs on its SLA timers, so the harness starts the journey with the result and invoice submissions and sets no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); partner and partner_instruction are S9's in `rwb_partner`, decision_log_entry and rule_row are P7's in `rwb_decision`, recovery_case is P3's in `rwb_case`, and the proceeds records are P8's in `rwb_payment`.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (S9) | `GET /partners`, `GET /partner/instructions`, `POST /partner/instructions/{instructionId}/results`, `POST /partner/instructions/{instructionId}/invoices` | Partner `PRT-SYN-0007` with its panel status and contract; instruction `INS-SYN-2027-0007` on case `RW-2027-000901` with its status and result_code; a result accepted once per Idempotency-Key; an invoice accepted once per Idempotency-Key with its submission outcome; a repeat of either key returns the first answer unchanged. No invoice read is offered, because the map publishes none |
| Stub for rwb-payment (P8) | `GET /proceeds` | The proceeds record the result is matched against, with the case it belongs to, so the check has a money side and no amount is invented by the harness |
| Stub for rwb-decision (P7) | `GET /decision-log?caseId={caseId}` | One approval entry with its rule_id and rule_version once the approval is taken, and none before; a second read returns the same single entry |
| Stub for rwb-case (P3) | `GET /cases/{caseId}` | Case `RW-2027-000901` with its state before the submission and after it |
| Stub for rwb-access (P4) | `GET /me/session` | Allows the partner and agency manager with Partner portal R and U; refuses RW-CASEOWN with 403 and MSG-P4-002, and a submission short of a required field with MSG-GEN-001 |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic keys, the fee claim and schedule answer shape, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0473; ASM-0665).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; three consumed, `rwb.partner.InstructionIssued.v1`, `rwb.partner.PartnerResultSubmitted.v1` and `rwb.decision.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; InstructionWorkflow on `rwb-partner` observed from its history, with its SLA timers and its issueInstruction and recordResult activities |
| File | None owned. The result upload is the multipart body of S9's results operation and the invoice is S9's own request body; both are exercised through the owner's contract and neither is staged here |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-13 adds nothing: the partner-portal and proceeds paths are rewritten onto each owner's own base and there is no shared base left. The H dependency DP-03 adds, RWB-PLT-E1027-CON, is a platform story delivered by the platform wave and is not repeated in the metadata H field of this story, which stays None; the same holds for RWB-PLT-N001-CON, which DP-19 adds for the composite route behind the partner portal and the screens. The one blocking dependency is the I story RWB-S9-E7012-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the five owned criteria in order for one instruction and its invoice, and holds the run lock |
| PartnerDriver | Service | Reads the partner and its contract, and names the schedule the claim is checked against |
| InstructionDriver | Service | Reads the instruction and its recorded result, submits one result and one invoice with one Idempotency-Key each, and reads the answer back |
| ProceedsReadBack | Service | Reads the P8 proceeds record the result is matched against and names it in the report |
| DecisionProbe | Service | Reads the approval entry and its rule version, and holds the fault switch that forces the decision-record failure |
| EventObserver | Service | Subscribes to `rwb.partner.events.v1` and `rwb.decision-record.v1`, counts publications and replays each partner event once |
| WorkflowProbe | Service | Observes InstructionWorkflow in the `rwb-recovery` namespace: its SLA timer, its issueInstruction and recordResult steps and the run it belongs to |
| StubSet | Fake | The five stubs of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per instruction and invoice, keyed by story and instruction id, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S9-E7012-APP lands, on the synthetic partner `PRT-SYN-0007`, the case `RW-2027-000901`, the instruction `INS-SYN-2027-0007`, the invoice against it and the recorded result, with the fixture's business date. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the fee claim and schedule answer shape, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0473; ASM-0665).

**Build steps**

1. Generate the five stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the PartnerDriver and prove the partner read returns the partner, its panel status and its contract, and that the schedule is named from it (AC2).
3. Add the InstructionDriver: one instruction read, one result submission and one invoice submission, each with one Idempotency-Key, and a repeat that changes nothing (AC3, X3).
4. Add the ProceedsReadBack for AC2: the proceeds record the result is matched against, named in the report beside the schedule and the result, so a claim checked against neither fails the run (X2).
5. Add the DecisionProbe for AC1 and AC3: exactly one approval entry with its rule_id and rule_version, and no second entry after a re-read (X3).
6. Add the EventObserver for AC3: one InstructionIssued and one PartnerResultSubmitted publication, one DecisionRecorded publication, the consumer effect once, and a replay that changes nothing because the inbox holds one row per consumer (X5).
7. Add the WorkflowProbe for AC3: the InstructionWorkflow run for the instruction, its SLA timer, and the issueInstruction and recordResult steps, so a result that is submitted but never recorded fails the run (X4).
8. Add the fault switch for AC4: force the decision-record failure, assert MSG-P7-003 and assert the instruction, the invoice, the case and the decision log are unchanged (X6).
9. Add the access path for AC5 through the session read and the two submissions, then the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S9-E7012-APP lands (X7, X8).

**Feature switch.** None. The harness has no production flag; the fault switch of step 8 exists in the test environment only and is reset by the runner before each run.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S9-E7012-APP when it lands, and the wave entry check holds a run report keyed by story and instruction id.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text and no S9 message of its own. MSG-GEN-001 is asserted with the missing field when a result or an invoice submission is made short of a required parameter, MSG-P4-002 with the refused action when the caller holds Partner portal R but not U, and MSG-P7-003 when the decision record cannot be written and nothing changes.

### 15. Screens and states

The legacy story names SCR-34 Partner list and SCR-35 Placement and allocation, and this harness renders neither: it observes the owners' operations and writes a report. The states are read through those operations, not rendered.

| State | Read through | What the run asserts |
|---|---|---|
| SENT | S9 partner instruction read, and InstructionWorkflow | The instruction is with the partner with its due_at, and its SLA timer is running |
| DONE | S9 partner instruction read, and InstructionWorkflow | The result is recorded with its result_code, and the recordResult step has run once |
| The approval | P7 decision log, S9 invoice submission answer and the P7 decision record event | Exactly one approval entry with its rule version, and no second entry after a re-read |
| SCR-34 empty, loading, error and no access | Not rendered; the harness reads the owners' operations only | Not specified in the source documents (CG-ALL-1196; GAP-0473) |
| SCR-35 empty, loading, error and no access | Not rendered; the harness reads the owners' operations only | Not specified in the source documents (CG-ALL-1197; GAP-0473) |

The harness renders no screen. SCR-34 Partner list and SCR-35 Placement and allocation belong to the S9 stories of the legacy key and of the features around it, and neither is built or read here. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0473; ASM-0665).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-012-01-ITG | AC1 (legacy); ITG AC1 | End to end | Partner `PRT-SYN-0007` with its contract, instruction `INS-SYN-2027-0007` with its recorded result, the invoice, and the approval taken once |
| TC-E7-012-02-ITG | AC2 not recorded (legacy); ITG AC4 | Integration | A forced decision-record failure at the approval, after the result and the invoice are submitted |
| TC-E7-012-03-ITG | Access; ITG AC5 | Component | A synthetic RW-CASEOWN caller holding Partner portal R and not U |
| TC-E7-012-04-ITG | Principle 5; ITG AC4 | Integration | A forced decision-record failure with the instruction, the invoice, the case and the decision log read before and after |
| TC-E7-012-05-ITG | ITG AC3 | Integration | The instruction and its invoice submitted for approval, with the decision log and the partner events counted before the approval and after it, and each partner event replayed |
| TC-E7-012-06-ITG | ITG AC6 (BR1 to BR8 in section 8) | Component | The section 8 Covered by entries, checked against the criteria in section 7 and the test case rows in section 16 |
| TC-E7-012-07-ITG | ITG AC7 | Integration | One consumed read (schedule, result or proceeds) stubbed to fail or not answer within 2 s, with the instruction, the invoice, the case and the decision log read before and after |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. Legacy AC2 stays with RWB-S9-E7012-APP, which owns the failure inside the approval. ITG AC2 is asserted inside the run of TC-E7-012-01-ITG, which is the end-to-end case that names the schedule, the result and the proceeds and counts the single approval and its events; ITG AC3 has its own case, TC-E7-012-05-ITG, because the legacy set of four has no test for it.

### 17. Guardrails

- No business value in code: the synthetic partner, its contract, the instruction, the result, the invoice, the business date, the fault switch, the retry settings and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- Service data only through the owner's contract: the partner and the instruction from S9, the proceeds from P8, the decision log and the rule rows from P7, the case from P3; never a direct schema read and never another service's table (DP-01).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- The fault switch is reset by the runner before each run and is never left on, so a forced failure cannot be mistaken for a real one.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-012 Approve partner fees | Recovery Workbench User Stories Epics 3 to 8 v4, lines 12474 to 12552 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 12493 to 12497 | Section 7, AC1, marked (legacy RWB-E7-012 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E7-012-02 | The same, lines 12499 to 12503 and 12547 | AC4 asserts the same failure here; the legacy AC stays with RWB-S9-E7012-APP (section 19) |
| Legacy test cases TC-E7-012-01 to TC-E7-012-04 | The same, lines 12546 to 12549 | Copied as -ITG in section 16 |
| Legacy permission table, Partner portal R and U | The same, lines 12529 to 12532 | Sections 10 and 12.2, and AC5 |
| Legacy screens SCR-34 and SCR-35 | The same, lines 12522 to 12525 | Section 15 |
| FEAT-PRM-09 Approve partner fees | Epics 3 to 8 Specification v3, line 142 | Sections 1 and 2 |
| FEAT-PRM-07 Match a recovery and calculate the agency fee | Epics 3 to 8 Specification v3, line 140 | Sections 2, 8 and 19 (the calculation is out of scope) |
| The S9 partner-portal operations | Epics 3 to 8 Specification v3, lines 217 to 220 | Section 12.2 |
| REQ-S9-001 and REQ-S9-004 | Business Requirements Program v5, lines 430 and 433 | Section 8, BR1 and BR2 |
| R-UNI-25, R-UNI-26, R-UNI-28 and R-UNI-29 | Business Rules and Routing Logic v4, lines 429, 430, 432 and 433 | Section 8, BR3 to BR6 |
| DF-PRT-001 to DF-PRT-007, DF-PRT-008 to DF-PRT-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-CAS-001 to DF-CAS-023 | Logical Data Model and Data Dictionary v9 | Section 11 |
| S9 contract: partners, partner portal, InstructionWorkflow, rwb_partner, rwb.partner.events.v1 | Architecture v5 slides 17 and 41 | Sections 2, 9, 12.2, 12.4 and 12.5 |
| InstructionIssued and PartnerResultSubmitted | Architecture v5 slides 17 and 43, rows 20 and 21 | Section 12.4 |
| DecisionRecorded and the job map | Architecture v5 slides 42 and 44 | Sections 12.4 and 12.6 |
| The S9 journey, steps 3, 4 and 6, and one child per stage | Temporal and Drools design slides 25 and 13 | Sections 2, 9, 12.5 and 13 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 12.4, 12.2 and 8: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |

### 19. Out of scope

- RWB-S9-E7012-CON and RWB-S9-E7012-APP: the build of the approval, the check against the schedule and the result, and the decision record.
- The S9 build itself: the partner, the instruction, the result, the invoice, the fee and the scorecard records, InstructionWorkflow and its SLA timers, and every S9 CON, APP, DB and director story.
- The fee calculation, FEAT-PRM-07 Match a recovery and calculate the agency fee, and the payment that follows an approval.
- The partner gateway in the DMZ and the external partner sign-in, which are the partner portal's own product.
- SCR-34 Partner list and SCR-35 Placement and allocation, and every screen of the legacy key.
- The recall and the re-selection of R-UNI-25, R-UNI-26, R-UNI-28 and R-UNI-29, which are asserted around the fee and built by their own stories.
- Platform deployment and configuration, and the platform H dependencies named in section 13.
- Any production change: the harness writes no code in any service and no row in any schema.
