# RWB-ITG-E6033-ITG Receive a partner result into the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E6033-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-033 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S9-E6033-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-033 as the wave 4 integration proof of a partner result reaching the case, driven through rwb-partner and observed across rwb-partner, rwb-source-data, rwb-case and rwb-decision; the intake of the result is RWB-S9-E6033-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the contact, promise and cash results a partner reports on the portal to land on the case once, on the same business day, with the decision record written and the refused and failed paths proved to change nothing**, so that **partners are placed, paid and measured by rule and no result is lost, doubled or booked against the wrong day**.

This story builds the wave 4 integration harness and its evidence, and nothing else. The partner result intake, the check that attaches it to the case and the decision record are built by S9 rwb-partner in RWB-S9-E6033-APP and its CON story; the interaction ledger the result lands in is P1's, the case is P3's, and the rule version and the central ledger are P7's. The harness submits one result through S9's partner-portal operation, reads the interaction through P1's contract, reads the case through P3, reads the decision log through P7, counts the events and writes a run report per instruction. It provides no endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A partner reports a contact, a promise or a cash result on the portal, and the case does not show it. That is the failure this story is written against. R-WO-33 puts the timing plainly: when the result is reported on the portal the contact, promise and cash are attached to the case **the same day**. A result that lands a day later breaks the promise date it carries, a result that lands twice double-counts a payment the bank has not received, and a result that lands against another business date makes the case's own history unreadable to the collector who calls the borrower next. REQ-S9-004 then makes the result the money side of the partner relationship: fees are calculated from the contracted schedule and paid against **recorded** results, so an unrecorded result is an unpaid partner and an over-recorded result is a fee paid twice. REQ-S9-008 fixes the channel: partners exchange data through the partner portal and the external gateway, not by email, so the portal submission is the only path this run exercises.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13); there is no in-process call and no second hop. The partner and the instruction are S9's, the interaction ledger is P1's under the default ruling (DP-18), the case is P3's, the decision log and the rule rows are P7's; DP-01 forbids reading another service's schema, and the ACE-side and boundary reads go through P1's published contract (DP-05). The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract. On the edge, DP-19 sends partners through the **partner gateway** (FAPI 2.0) that fronts rwb-partner, and reserves gateway-bff composite routes for staff screens; this run calls S9's own operation at the service boundary, which is the same operation the partner gateway fronts.

One limit is stated here because it shapes the run: the Ownership Map publishes the partner-portal result operation and the instruction read, but no result read. The harness therefore asserts the result twice over — through the instruction read, which carries the recorded result, and through P1's interaction ledger, which carries the ledger entry the result creates on the case. It never invents a result endpoint, and where a screen would compose the partner read, the case read and the ledger read, the path is the partner gateway for the partner and the gateway-bff composite route for staff (DP-19).

### 3. Preconditions

- The published contracts of S9 rwb-partner (the partner instruction read and the result submission), P1 rwb-source-data (the case interaction ledger and DP08 Partner performance), P3 rwb-case (the case), P7 rwb-decision (the decision log) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- S9 owns the panel, the partner users, the instructions, the results, the fees and the scorecards in `rwb_partner` (Arch v5 slide 41), so the instruction and the result this run drives have one named owner before a value is asserted.
- P1 owns the interaction ledger under the default ruling (Template and Rules v1 §R3, DP-18), and publishes DP08 Partner performance refreshed on change; the harness reads the ledger and the product through P1's contract and never from a schema.
- The instruction is placed before this story runs: the placement is R-WO-33's `PLACED_WITH_AGENCY`, driven by InstructionWorkflow on `rwb-partner` with its SLA timers and its `issueInstruction` and `recordResult` activities (Arch v5 slide 17), and the harness observes that workflow and builds none of it.
- RWB-S9-E6033-APP owns the result intake, the attachment to the case and the decision record; until it lands, the partner fixture of §12.8 stands in for its effect and the story is reported as a stub pass.
- FEAT-PRM-05 is the S9 feature and FEAT-PRM-03 its placement dependency: the fixture holds an instruction that is already placed, so this story never asserts the placement decision, the panel comparison or the scorecard order (R-WO-30, REQ-S9-003).
- The harness environment and base hosts, the fixture layout, the synthetic partner, instruction and case keys, the result reference and answer shape, the same-day cut-off, the evidence format and retention, and the pass or fail gate: Not specified in the source documents (GAP-0463; ASM-0655).
- The synthetic partner, its placement, the instruction, the result, the business date and the case are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S9-E6033-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: partner `PRT-SYN-0033` with its partner_code and panel status, case `RW-2027-000833`, instruction `INS-SYN-2027-0033` for that partner and case in `PLACED_WITH_AGENCY`, the partner result with its result reference `RES-SYN-0033` for contact, promise and cash, and business date `2027-04-30`. On Day 1 the stubs of §12.8 return the same records.
2. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and names the case, its status and its stage before the submission, so a change after the run has a baseline.
3. Harness: reads `GET /api/recovery/partner/v1/partner/instructions` and asserts one instruction for the partner and the case, its instruction_type, its instructed_at, its due_at and its status `PLACED_WITH_AGENCY`, and that no result is recorded on it yet (AC2).
4. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP08/records?caseId={caseId}` and names the partner and the instruction as the published product carries them, so the boundary view the rest of the bank sees is the same placement the owner holds (AC2).
5. Harness: submits the result through `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results` with one Idempotency-Key, and asserts the answer names the same instruction and the same result reference, and that it is an acceptance and not a duplicate (AC2).
6. Harness: re-reads `GET /api/recovery/partner/v1/partner/instructions` and asserts one accepted result on the instruction, with its result_code and its acceptance time inside the business date, and no second result (AC2).
7. Harness: reads `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` and asserts exactly one interaction for the case, against business date `2027-04-30`, on the portal channel, with the contact, promise or cash facts the result carried; a second row, a row on another date or a row for another case fails the run (AC2).
8. Harness: replays the same submission with the same Idempotency-Key, asserts the answer is the first answer unchanged, and re-reads the instruction and the ledger and asserts no second result and no second interaction (AC2).
9. Harness: counts one `rwb.partner.PartnerResultSubmitted.v1` on `rwb.partner.events.v1` after the acceptance, replays it once, and asserts no consumer row is added, because the inbox holds one processed row per consumer (AC3).
10. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` again and asserts the case is the same status and stage as the baseline, because R-WO-33 attaches the evidence to the case and does not move it (AC2, AC5).
11. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts exactly one entry for the acceptance, with its rule_id and rule_version, and no second entry after a re-read (AC4).
12. Harness: reads the decision record as published on `rwb.decision-record.v1` as `rwb.decision-record.DecisionRecorded.v1` and asserts it carries the acceptance and its rule version, and that the central ledger in rwb-decision has confirmed it once (AC4).
13. Harness: resets the fixture to the pre-submission snapshot, turns the fault switch on the decision-record hop on, submits the result under a new Idempotency-Key, and asserts the answer carries MSG-P7-003 with no interaction, no partner event and no state change; the switch is reset before the next run (AC5).
14. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller holding Partner portal R but not U, submits the same result, and asserts 403 with MSG-P4-002 and no recorded result and no interaction (AC6).
15. Harness: writes one run report per instruction, keyed by story and instruction id, naming the contract version of each hop, whether the hop was a stub or the owner, the result reference, the business date, the one interaction, the decision entry with its rule version, both event counts, the workflow run and the gate verdict.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E6-033-01-ITG (ITG AC1) |
| X2 | The result is accepted twice, or two interactions are read for the case | The run fails on AC2 and the report names both accepts, the Idempotency-Key each carried and both interaction rows | None | TC-E6-033-01-ITG (ITG AC2) |
| X3 | The interaction is written against another business date, or for another case | The run fails on AC2 and the report names the interaction, its occurred_at, the business date and the case id, because a result on the wrong day is the failure R-WO-33 is written against | None | TC-E6-033-01-ITG (ITG AC2) |
| X4 | A partner event is published more than once, or a replay adds a consumer row | The run fails on AC3 and the report names the topic, the event id, the consumer and the inbox row count | None | TC-E6-033-01-ITG (ITG AC3) |
| X5 | The decision record is written twice, written without its rule version, or the ledger has not confirmed it | The run fails on AC4 and the report names the entries, their rule versions and the missing confirmation | None | TC-E6-033-04-ITG (ITG AC4) |
| X6 | A forced decision-record failure leaves an interaction, an event or a state change, or answers without MSG-P7-003 | The run fails on AC5 and the report names the interaction count, the event count and the case read before and after | MSG-P7-003 (expected, and missing) | TC-E6-033-02-ITG (ITG AC5) |
| X7 | A caller without Partner portal U is allowed to submit a result, or a submission short of a required field is accepted | The run fails on AC6 and the report names the caller role, the right, the operation and the answer; a 200 is a failure even when no data changed | MSG-P4-002 (expected, and missing); MSG-GEN-001 (expected, and missing) | TC-E6-033-03-ITG (ITG AC6) |
| X8 | A stub pass is reported as a real pass while RWB-S9-E6033-APP is not live | The run fails on AC1 and the report names the hop that was a stub and the owner it waits for | None | TC-E6-033-01-ITG (ITG AC1) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S9-E6033-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the same-day cut-off, the fault switch, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The result is proved to land once, on the same business day, as one interaction on the case; the event, the decision record and the central ledger are proved single; and the refused and failed paths are proved to change nothing |
| Estimable | One runner, one stub set, one partner fixture, one instruction, one result submission, one ledger read, one decision probe, one event observer, one workflow observation and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S9-E6033-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Receive a partner result into the case - wave 4 integration harness

  Background:
    Given the synthetic partner "PRT-SYN-0033" is on the panel and holds instruction "INS-SYN-2027-0033" on case "RW-2027-000833"
    Given the instruction is in PLACED_WITH_AGENCY under R-WO-33 and carries no result yet
    Given the rule package in force holds R-WO-33, R-UNI-25 and R-UNI-27 and DP08 answers for the partner

  Scenario: AC1 Receive a partner result into the case (legacy RWB-E6-033 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then takes contact, promise and cash results from the portal onto the case the same day
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The result is recorded once and attached to the case the same day (new, D-RCV-60)
    Given the instruction "INS-SYN-2027-0033" with the partner result held in the fixture for business date "2027-04-30"
    When the result is submitted through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results with one Idempotency-Key
    Then GET /api/recovery/partner/v1/partner/instructions answers the instruction with one accepted result and the same result reference
    And GET /api/recovery/source-data/v1/cases/{caseId}/interactions answers exactly one interaction for the case
    And the interaction is against the same business date "2027-04-30"
    When the same submission is replayed with the same Idempotency-Key
    Then no second interaction is added and the instruction is unchanged

  Scenario: AC3 The result event is published once and reaches its three consumers (new, D-RCV-60)
    Given the result for the instruction is accepted
    When the acceptance commits
    Then "rwb.partner.PartnerResultSubmitted.v1" is published once on "rwb.partner.events.v1"
    And the event is consumed once by rwb-case, rwb-litigation and rwb-asset
    And a replay of the event adds no consumer row, because the inbox holds one processed row per consumer

  Scenario: AC4 The decision record is written once per acceptance and confirmed by the central ledger (new, D-RCV-60)
    Given the rule package in force holds R-WO-33 with its rule version
    When the result is accepted
    Then GET /api/recovery/decision/v1/decision-log?caseId={caseId} holds exactly one entry for the acceptance with its rule_id and rule_version
    And "rwb.decision-record.DecisionRecorded.v1" is published once on "rwb.decision-record.v1"
    And the central ledger in rwb-decision has confirmed the record
    And a re-read of the decision log holds no second entry

  Scenario: AC5 A forced decision-record failure stops the result with nothing attached (new, D-RCV-60)
    Given the decision record cannot be written for the acceptance
    When the result is submitted through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    Then the answer carries "MSG-P7-003"
    And no interaction is read for the case
    And no "rwb.partner.PartnerResultSubmitted.v1" is published
    And the instruction and the case are read unchanged

  Scenario: AC6 A caller without Partner portal U is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-CASEOWN" holding Partner portal R and not Partner portal U
    When the caller submits a result for the instruction
    Then the answer is 403 with "MSG-P4-002"
    And no result is recorded and no interaction is read for the case
```

Legacy AC1 is the only legacy criterion this story owns. Legacy AC2 (the decision log cannot be written and nothing changes) is not owned as a build criterion here: the intake that must fail is RWB-S9-E6033-APP's, and this story asserts the same failure across the service boundary in AC5, where the interaction, the event and the case state are read before and after the refused acceptance.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A result reported on the portal attaches contact, promise and cash to the case the same day | R-WO-33 |
| BR2 | Fees are calculated from the contracted schedule and paid against recorded results, so the recorded result is what the fee is paid on | REQ-S9-004 |
| BR3 | Partners exchange data through the partner portal and the external gateway, and not by email | REQ-S9-008 |
| BR4 | When the partner misses the service level on the portal, the work is chased once, then recalled and re-selected on the scorecard | R-UNI-25 |
| BR5 | When the partner declares a conflict of interest, the instruction is withdrawn and the next partner is selected, so a withdrawn instruction carries no accepted result from this run | R-UNI-27 |
| BR6 | Every hop in the run is one REST call on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout and no second hop | DP-11, DP-13 |
| BR7 | The interaction ledger is P1's under the default ruling, and ACE-side or boundary data is read only through P1's contract or the service's own ACE views, never from another service's schema | DP-01, DP-05, DP-18 |
| BR8 | The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1`, and the central ledger in rwb-decision confirms it; nothing is attached when the record cannot be written | DP-03; ADR-022; legacy Principle 5, TC-E6-033-04 |
| BR9 | The event is one CloudEvent per acceptance on the owner's topic, consumed once per consumer through the inbox | DP-09; ADR-015 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E6033-APP, the ledger is P1's, the case is P3's and the rule versions are P7's.

### 9. State transitions

| From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|
| PLACED_WITH_AGENCY | AGENCY_REPORTED_RESULT | the result is reported on the portal, and one acceptance is recorded | PLACED_WITH_AGENCY | S9 rwb-partner, InstructionWorkflow `recordResult`, R-WO-33; `rwb.partner.PartnerResultSubmitted.v1` |
| PLACED_WITH_AGENCY | none on the case | the result attaches contact, promise and cash to the case | PLACED_WITH_AGENCY, unchanged | P3 rwb-case holds the case and moves no state; the evidence is the P1 interaction ledger |
| PLACED_WITH_AGENCY | none | the acceptance is refused for want of Partner portal U, or stops on a decision-record failure | PLACED_WITH_AGENCY, unchanged | S9 rwb-partner refuses before any write; nothing is attached |

`PLACED_WITH_AGENCY` is the state R-WO-33 gives in its from-state and its to-state, and the rule table attaches the contact, promise and cash without moving the placement. The case status and stage are read through the P3 contract before and after every attempt, and the harness asserts they are the same value; it invents no case state beyond the ones the sources give, and it never sets a state it then asserts. The only state the run can see change is the instruction's own recorded result, which S9 holds, and the only artefact the result adds to the case is the ledger entry P1 holds. The interaction ledger is not a case state: it is the record that the same-day attachment happened, read through P1's published operation, and the run counts it rather than moving anything.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Case owner | Owns the case the result lands on; holds Partner portal R and not U, and is the role the journey is written for |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and the other holders of Partner portal U listed in the legacy permission table | Submit a result where their scope allows; the run records the right each operation answered with and asserts U on the result path |
| RW-CASEOWN and the other holders of Partner portal R | Read the partner and the instruction; RW-CASEOWN is the refused caller of AC6 because it does not hold U |
| Partner and agency manager | Owns the recall of BR4 and BR5 that stops a withdrawn instruction from carrying an accepted result |
| QA lead | Owns the harness configuration, the fixtures, the fault switch, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S9 holds the partner, the instruction and the result and runs InstructionWorkflow, P1 holds the interaction ledger and DP08, P3 holds the case, P7 holds the decision log and the central ledger, and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | partner_code, partner_name, partner_type, panel_status, contract_end | Read through the rwb-partner contract and through DP08 |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code, primary_person_key | Read through the rwb-case contract, before and after every attempt |
| DF-INT-001 to DF-INT-013 | interaction | id, case_id, occurred_at, channel, direction, contact_result, promise_amount, promise_date, summary, source_system | Read through the P1 interaction-ledger contract; the entry is written by S9's acceptance, not by the harness |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, model_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, event_code | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v8, and the legacy data table of RWB-E6-033 cites these five entities under these IDs. The partner and the instruction are S9's in `rwb_partner`; the legacy data table cites the partner as DF-PRT-001 to DF-PRT-007 and stops there, so the instruction record is carried by its instruction id through S9's contract and no field ID is asserted for it here. The interaction is P1's ledger under the default ruling and DP-18 (the table's own data product is DP05 Interaction, and the partner-facing product is DP08), and it is read only through P1's contract and never from a schema. The decision log entry and the rule rows are P7's, and the case is P3's. The harness owns no table and writes no row: the two changes it drives are S9's own published operations of §12.2, each with one Idempotency-Key, and everything else it reads is a contract read.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instruction, its placement status and the one accepted result and its reference (AC2, AC3, AC5) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/results` | S9 rwb-partner | Submits the result once with one Idempotency-Key, and is the refused and the failed operation of AC5 and AC6 (AC2, AC5, AC6) |
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The single interaction on the case, the business date it is against and the contact, promise or cash facts it carries (AC2, AC5, AC6) |
| GET | `/api/recovery/source-data/v1/data-products/DP08/records?caseId={caseId}` | P1 rwb-source-data | DP08 Partner performance, refreshed on change, as the boundary view of the partner and the instruction (AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case status and stage before and after the submission, the replay and the two refusals (AC1 to AC6) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | Exactly one entry per acceptance with its rule id and rule version, and no second entry after a re-read (AC1, AC4, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a submission (AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation in the Ownership Map. The map publishes no result read, so the result is asserted through the instruction read, which carries the recorded result and its reference, and through P1's ledger, which carries the attachment to the case; the harness never calls an endpoint the map does not publish. For a partner the edge path to the result operation is the partner gateway (FAPI 2.0) that fronts rwb-partner, and for a staff screen the same values would be composed by a gateway-bff composite route (DP-19); the run itself calls the service boundary the gateway fronts.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.partner.PartnerResultSubmitted.v1` | `rwb.partner.events.v1` | S9 rwb-partner | Counts one publication per acceptance and proves the three consumers hold one processed row each after a replay (AC3) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | S9 rwb-partner through the local decision-record library (DP-03) | Proves the acceptance and its rule version were published once and confirmed by the central ledger (AC4, AC5) |

The harness subscribes to both topics under one consumer group of its own, counts publications and replays the partner event once. The consumer effect it reads for rwb-case is the case through the rwb-case operation of §12.2; the inbox row counts of rwb-litigation and rwb-asset, which Arch v5 slide 43 row 21 gives as the consumers of `PartnerResultSubmitted`, come from the consumer evidence in the run fixture, because neither consumer exposes an operation for this result in this story.

#### 12.5 Workflows and activities

None added. The harness exercises InstructionWorkflow, S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace, through the result submission: its SLA timers and its `issueInstruction` and `recordResult` activities are the ones the run observes in the workflow history (Arch v5 slide 17). It observes CaseWorkflow on `rwb-case` as the parent that holds the case the interaction lands on, and observes it only: the result does not signal it and moves no case state. Neither workflow, activity nor Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added, and none needed. The result arrives as a partner submission on the portal and the acceptance is event-driven, so nothing in the journey is on a cron: the harness starts the run with its own submission and holds the business date in the fixture. JOB-05 Timer check is retired in favour of durable timers inside the workflows (Arch v5 slide 44), and the instruction's SLA is read as a workflow timer, not as a scheduled job.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): partner and partner_instruction are S9's in `rwb_partner`, the interaction ledger is P1's, recovery_case is P3's in `rwb_case`, decision_log_entry and rule_row are P7's in `rwb_decision`, and DP08 is P1's published product over the Workbench records.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (S9) | `GET /partner/instructions`, `POST /partner/instructions/{instructionId}/results` | Partner `PRT-SYN-0033` on the panel; instruction `INS-SYN-2027-0033` on case `RW-2027-000833` in `PLACED_WITH_AGENCY` with its due_at and no result; a result accepted once per Idempotency-Key with reference `RES-SYN-0033` and its result_code, and a repeat of the key returning the first answer unchanged; with the fault switch on, an answer carrying MSG-P7-003 and no acceptance |
| Stub for rwb-source-data (P1), the ledger | `GET /cases/{caseId}/interactions` | No interaction before the acceptance, exactly one interaction `INT-SYN-0033` after it, against business date `2027-04-30` on the portal channel; none at all after the forced failure or the refused caller |
| Stub for rwb-source-data (P1), DP08 | `GET /data-products/DP08/records?caseId={caseId}` | The partner and the instruction as the published product carries them, refreshed on change, with its business date |
| Stub for rwb-case (P3) | `GET /cases/{caseId}` | Case `RW-2027-000833` with the same status and stage before and after every attempt |
| Stub for rwb-decision (P7) | `GET /decision-log?caseId={caseId}` | No entry before the acceptance; exactly one entry with its rule_id and rule_version after it; the central ledger confirmation once; unchanged by the forced failure and the refusal |
| Stub for rwb-access (P4) | `GET /me/session` | Allows the case owner with Partner portal R and U where the run needs it; refuses RW-CASEOWN on the result path with 403 and MSG-P4-002; refuses a submission short of a required field with MSG-GEN-001 |
| Partner-portal fixture | The portal submission and its same-day window | The submitted result body, its reference and its business date, held as data, with the cut-off that decides whether the attachment is same-day |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic partner, instruction and case keys, the result reference and answer shape, the same-day cut-off, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0463; ASM-0655).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.partner.PartnerResultSubmitted.v1` and `rwb.decision-record.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; InstructionWorkflow on `rwb-partner` exercised through the submission, with CaseWorkflow on `rwb-case` observed as the parent that holds the case |
| File | None. The result is S9's own request body and the report is the harness's own output; no file or claim-check is transferred by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None. DP-13 adds nothing: the partner-portal and ledger paths are rewritten onto each owner's own base and there is no shared base left. DP-19 has two edges in this journey and the run names both: for the **partner** the route is the **partner gateway** in the DMZ under FAPI 2.0, which fronts rwb-partner and is the only path a partner has (Arch v5 slide 20, line 1458, and slide 35, line 2517), and **gateway-bff** composes the **staff** screens only, including the case view a case owner would see the attached result on. The one blocking dependency is the I story RWB-S9-E6033-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the six owned criteria in order for one instruction and holds the run lock and the fixture reset |
| ResultDriver | Service | Submits the result once per Idempotency-Key and reads the acceptance back through the instruction read |
| InstructionReadBack | Service | Reads the instruction, its placement status, its due_at and its one recorded result with its reference |
| LedgerReadBack | Service | Reads P1's interaction ledger for the case and asserts exactly one interaction against the same business date |
| ProductReadBack | Service | Reads DP08 and names the partner and the instruction as the boundary product carries them |
| DecisionProbe | Service | Reads the one decision entry and its rule version, reads the published decision record and holds the fault switch |
| EventObserver | Service | Subscribes to `rwb.partner.events.v1` and `rwb.decision-record.v1`, counts publications and replays the partner event once |
| WorkflowProbe | Service | Observes InstructionWorkflow in the `rwb-recovery` namespace, its SLA timer and its recordResult step, and observes CaseWorkflow only |
| StubSet | Fake | The six stubs and the portal fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per instruction, keyed by story and instruction id, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S9-E6033-APP lands, on the synthetic partner `PRT-SYN-0033`, the case `RW-2027-000833`, the instruction `INS-SYN-2027-0033`, the result reference `RES-SYN-0033` and business date `2027-04-30`. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the result reference and answer shape, the same-day cut-off, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0463; ASM-0655).

**Build steps**

1. Generate the six stubs and the portal fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the InstructionReadBack and the ProductReadBack, and prove the instruction is placed with no result yet and that DP08 carries the same partner and instruction (AC2).
3. Add the ResultDriver: one submission with one Idempotency-Key, the acceptance read back with its reference, and a replay that returns the first answer unchanged (AC2, X2).
4. Add the LedgerReadBack for AC2: exactly one interaction for the case, against the same business date, on the portal channel, and no second row after the replay (X3).
5. Add the case baseline: read the case before and after the run and assert the status and stage are unchanged, because R-WO-33 attaches the evidence and moves no state (AC2, AC5).
6. Add the EventObserver for AC3: one PartnerResultSubmitted publication, its three consumers with one processed row each, and a replay that adds none.
7. Add the DecisionProbe for AC1 and AC4: one entry per acceptance with its rule_id and rule_version, one published decision record, the central ledger confirmation, and no second entry after a re-read (X5).
8. Add the fault switch for AC5: force the decision-record failure before the acceptance, assert MSG-P7-003, and assert no interaction, no partner event and no state change; reset the fixture and the switch after the run (X6).
9. Add the access path for AC6 through the session read and the submission, assert 403 with MSG-P4-002 and no recorded result, then add the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S9-E6033-APP lands (X7, X8).

**Feature switch.** None. The harness has no production flag; the fault switch of step 8 exists in the test environment only and is reset by the runner before and after each run.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S9-E6033-APP when it lands, and the wave entry check holds a run report keyed by story and instruction id.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text and no S9 message of its own. MSG-GEN-001 is asserted with the missing field when a result submission is made short of a required parameter (X7), MSG-P4-002 with the refused action when the caller holds Partner portal R but not U (AC6), and MSG-P7-003 when the decision record cannot be written and nothing is attached (AC5).

### 15. Screens and states

The legacy story's screens are SCR-34 Partner list and SCR-35 Placement and allocation, and neither is built or rendered here: the harness calls the two partner-portal operations behind them and reads the states through the owners. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0463; ASM-0655).

| State | Read through | What the run asserts |
|---|---|---|
| PLACED_WITH_AGENCY | S9 instruction read, DP08 and the InstructionWorkflow history | The instruction is with the partner with its due_at, no result is recorded, and the SLA timer is running |
| One accepted result | S9 instruction read and the InstructionWorkflow history | The result is recorded once with its reference and result_code, inside the same business date |
| The attachment | P1 interaction ledger for the case | Exactly one interaction for the case, against the same business date, on the portal channel |
| The decision record | P7 decision log and the published decision record | Exactly one entry per acceptance with its rule version, and the central ledger confirmation |
| The case | P3 case read before and after every attempt | The same status and stage, because the result attaches evidence and moves no case state |
| A refused or failed submission | P4 session read, S9 answer, P1 ledger and the case read | 403 with MSG-P4-002 or MSG-P7-003, no recorded result, no interaction, no event and no state change |

SCR-34 Partner list and SCR-35 Placement and allocation belong to the S9 stories of the legacy key, and neither is built or read here. The partner reaches the result operation through the partner gateway and a staff member reaches a case view through a gateway-bff composite route (DP-19); this harness renders neither and asserts the operations behind them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-033-01-ITG | AC1 (legacy); ITG AC1, AC2 and AC3 | End to end | Partner `PRT-SYN-0033`, instruction `INS-SYN-2027-0033` in PLACED_WITH_AGENCY, one result submitted once and replayed, on business date `2027-04-30` |
| TC-E6-033-02-ITG | AC2 not recorded (legacy); ITG AC5 | Integration | A forced decision-record failure before the acceptance, with the ledger, the event and the case read before and after |
| TC-E6-033-03-ITG | Access; ITG AC6 | Component | A synthetic RW-CASEOWN caller holding Partner portal R and not U, and a submission short of a required field |
| TC-E6-033-04-ITG | Principle 5; ITG AC4 | Integration | One acceptance with its decision entry and its rule version, a re-read, and the central ledger confirmation |

The AC column names the legacy test the copy derives from and the ITG acceptance criteria it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx under the same legacy test case ID. Legacy AC2 stays with RWB-S9-E6033-APP, which owns the failure inside the intake; the -ITG copy here asserts the same failure across the service boundary. ITG AC2 and ITG AC3 are asserted inside the run of TC-E6-033-01-ITG, which is the end-to-end case that submits the result once, reads the one interaction and counts the one event; they add no test case ID because the legacy set has four.

### 17. Guardrails

- No business value in code: the synthetic partner, its placement, the instruction, the result reference, the business date, the same-day cut-off, the fault switch and the report layout are data.
- No personal data in logs, events, workflow inputs or reports: every key is synthetic, the interaction is read by ID and business date, and the events carry IDs and facts only.
- Service data only through the owner's contract: the partner and the instruction from S9, the ledger and DP08 from P1, the case from P3, the decision log and the rule rows from P7; never a direct schema read and never another service's table (DP-01, DP-05, DP-18).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented operation: only the one result submission and the six reads of §12.2, and the result is never asserted through a read the map does not publish.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The fault switch is reset by the runner before and after each run and is never left on, so a forced failure cannot be mistaken for a real one.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E6-033 Receive a partner result into the case | Recovery Workbench User Stories Epics 3 to 8 v3, lines 12148 to 12227 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 12167 to 12171 | Section 7, AC1, marked (legacy RWB-E6-033 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E6-033-02 | The same, lines 12173 to 12177 and 12223 | AC5 asserts the same failure here; the legacy criterion stays with RWB-S9-E6033-APP (section 19) |
| Legacy test cases TC-E6-033-01 to TC-E6-033-04 | The same, lines 12222 to 12225 | Copied as -ITG in section 16 |
| Legacy endpoints, permission checks, screens and messages | The same, lines 12193 to 12194, 12200 to 12201, 12207 to 12208 and 12214 to 12216 | Sections 12.2, 15, 10 and 14 |
| FEAT-PRM-05 Receive a partner result into the case, with FEAT-PRM-03 as its placement dependency | Epics 3 to 8 Specification v3, line 138 | Sections 1, 2 and 19 |
| REQ-S9-004 Fees paid against recorded results, and REQ-S9-008 partners exchange data through the portal | Business Requirements Program v4, lines 433 and 437 | Section 8, BR2 and BR3, and section 2 |
| R-WO-33 the result reported on the portal attaches contact, promise and cash to the case the same day | Business Rules and Routing Logic v4, line 364 | Sections 8 and 9, BR1 |
| R-UNI-25 the partner misses the service level and the work is chased then recalled, and R-UNI-27 a declared conflict withdraws the instruction | The same, lines 429 and 431 | Section 8, BR4 and BR5 |
| DF-PRT-001 to DF-PRT-007, DF-CAS-001 to DF-CAS-023, DF-INT-001 to DF-INT-013, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v8 | Section 11 |
| S9 contract: the partner-portal result operation, the instruction read, InstructionWorkflow, `rwb_partner` and `rwb.partner.events.v1` | Architecture v5 slide 17, lines 1243 to 1256 and 1270 to 1272 | Sections 2, 8, 12.2, 12.7 and 12.5 |
| rwb-partner ownership, schema, topic, task queue and wave | Architecture v5 slide 41, line 2891 | Sections 1, 12.7 and 13 |
| PartnerResultSubmitted, producer rwb-partner, consumers rwb-litigation, rwb-asset and rwb-case | Architecture v5 slide 43, row 21, line 2947 | Section 12.4, AC3 |
| The job map: no scheduled job for the result, and JOB-05 retired in favour of durable timers | Architecture v5 slide 44, lines 2974 to 2993 | Section 12.6 |
| The edge: partners only through the partner gateway (FAPI 2.0), gateway-bff for staff screens | Architecture v5 slide 20, line 1458, and slide 35, lines 2517 and 2560; DP-19 | Sections 2, 13 and 15 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| The interaction ledger owned by P1 under the default ruling | Template and Rules v1 §R3, DP-18 | Sections 11 and 12.2 |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v3 | Sections 12.4, 12.2 and 8: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| The six criteria of this harness and the gap and assumption behind its configuration | This file, sections 3, 7 and 12.8; GAP-0463 and ASM-0655 | Sections 3, 7, 12.8, 13 and 15 |

### 19. Out of scope

- RWB-S9-E6033-CON and RWB-S9-E6033-APP: the build of the partner result intake, the attachment to the case and the decision record, including legacy AC2 (the not-recorded path), which is its build criterion and which this story asserts only across the boundary in AC5.
- The S9 build itself: the panel, the partner users, the instructions, the results, the fees, the scorecards, InstructionWorkflow and its SLA timers, and every S9 CON, APP and DB story of the legacy key.
- The placement decision and the scorecard order (FEAT-PRM-03, R-WO-30, REQ-S9-003): the fixture holds an instruction that is already placed.
- The partner portal screens SCR-34 Partner list and SCR-35 Placement and allocation, and the partner gateway and the external partner sign-in, which are the partner portal's own product.
- The gateway-bff composite routes for the staff case view, which DP-19 names but this story neither builds nor calls.
- The platform H stories DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, which the platform wave delivers.
- The payments and proceeds posting of the cash result, the partner fee calculation (FEAT-PRM-07) and the partner scorecards (FEAT-PRM-08), which are their own features and are not called here.
- The recall paths of R-UNI-25 and R-UNI-27, which are asserted around the result and built by their own stories.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
