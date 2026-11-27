# RWB-ITG-E6032-ITG Override an allocation with a reason

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E6032-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S9-E6032-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-032 as the wave 4 integration proof that the partner manager can place work with a partner other than the one the scorecard picks, with the reason recorded, and that the scorecard's own pick is preserved beside the override: the instruction read back with the override partner, the pick and the override held as two decision entries, an override without a reason refused, a partner outside the panel refused, and the forced decision-record failure leaving nothing behind; the override is RWB-S9-E6032-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E6032-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the override of an allocation proved end to end on the real services: work placed with a partner other than the one the scorecard picks, the reason recorded in the decision log beside the scorecard's own pick rather than in place of it, an override without a reason and an override to a partner outside the panel both refused with nothing created, and one decision record per action with its rule version**, so that **the manager can depart from the rule where the facts require it, and the departure is visible, attributable and never able to erase the rule's own answer**.

This story builds the wave 4 integration harness and its evidence, and nothing else. The override, the reason, the instruction and the decision record are built by S9 rwb-partner in RWB-S9-E6032-APP and its CON story; the scorecard pick the override departs from is RWB-S9-E6031-APP's and is read here, never recomputed. The case is P3's, the decision ledger is P7's and the right is P4's. The harness places the work once through S9's published operation, drives the override through the same operation with the pick departed from, reads the instruction, the case, the decision log and the session, counts the event, observes the workflow and writes one run report per action. It provides no endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

An allocation rule that cannot be departed from is not workable. A panel firm with a conflict, a capacity the scorecard has not yet seen, or a court that only one firm covers all force a manual placement, and the partner manager is the role that has to make it. An override that leaves no trace is worse than no override at all, because the next reviewer cannot tell a rule placement from a favour. The Temporal and Drools design states the control in six words on slide 25, "Partner manager: overrides need a reason" (line 1739), and REQ-S9-003 keeps the rule intact underneath: work is allocated by measured return against a scorecard, not by a fixed share. R-UNI-24 supplies the pattern the log has to follow — a booked decision is corrected by a correcting entry naming the original, never overwritten — so the override is recorded beside the pick, and the pick stays readable afterwards.

The refusals matter as much as the acceptance. An override with no reason, or an override to a firm that is suspended, exited or past its contract end, would put work where R-WO-30 does not allow it and with nothing to defend the placement. FEAT-PRM-04 is the S9 feature, FEAT-PRM-03 is its prerequisite, and the panel the override is checked against is FEAT-PRM-02's: the run asserts all three boundaries without building any of them.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13); there is no in-process call and no second hop. The partner and the instruction are S9's in `rwb_partner`, the case is P3's in `rwb_case`, the decision entry and the rule rows are P7's in `rwb_decision`, and DP-01 forbids reading another service's schema, so every value is read through its owner's contract; DP-05 keeps ACE-side data out of the run entirely, and where such data would arise it arrives through P1's published contract and never from a view of the harness's own. The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1` (DP-03, ADR-022) and read back through rwb-decision's contract at the service boundary. On the edge, DP-19 sends partners through the **partner gateway** in the DMZ under FAPI 2.0, which fronts rwb-partner, and reserves gateway-bff composite routes for staff screens; the run calls S9's own operation at the service boundary, which is the same operation the partner gateway fronts.

One limit is stated plainly because it shapes the whole run: the Ownership Map publishes no separate override operation. The published placement, `POST /cases/{caseId}/instructions` ("Issue an instruction to a partner by rule", right Partner portal C, one Idempotency-Key), carries the named partner and the reason, and the override is that operation with the scorecard's pick departed from. The `InstructionRequest` shape the operation takes is not published either, so it is held in the fixture generated from S9's CON story, and the harness invents no second endpoint and no second payload.

### 3. Preconditions

- The published contracts of S9 rwb-partner (the placement by rule and the instruction read), P3 rwb-case (the case), P7 rwb-decision (the decision log) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one and pinned in the report.
- S9 owns partner, partner_user and partner_instruction in `rwb_partner` (Arch v5 slide 41, line 2891), so the partner the override names and the instruction it writes have one named owner before a value is asserted.
- The override, the reason validation, the panel check and the decision record are RWB-S9-E6032-APP's; until it lands, the partner, override and reason fixture of §12.8 stands in for its effect and the run is reported as a stub pass.
- The scorecard pick the override departs from is RWB-S9-E6031-APP's, and this story reads it and never recomputes it: the fixture holds the pick, and the run asserts the pick's own decision entry is still there afterwards.
- FEAT-PRM-04 Override an allocation with a reason is the S9 feature, with FEAT-PRM-03 Allocate work by measured return as its prerequisite and FEAT-PRM-02 the panel it is checked against.
- The rules the run asserts are R-WO-30 (place the account with the agency chosen on measured return and send the instruction, PLACEMENT_DECIDED to PLACED_WITH_AGENCY), R-WO-31 (no capacity: hold the placement and escalate on the timer), R-UNI-24 (a booked decision is corrected by a correcting entry naming the original, never overwritten), R-UNI-25, R-UNI-26, R-UNI-27, R-UNI-29 and R-UNI-45.
- The right on the placement is Partner portal C per API-S9-002, and the right on the instruction read is Partner portal R per API-S9-003.
- The harness environment and base hosts, the fixture layout, the synthetic partners, case and instruction keys, the reason code, the business date, the evidence format and retention, and the pass or fail gate: Not specified in the source documents (GAP-0462; ASM-0654).
- The reason code, the reason text, the pick, the override partner, the suspended partner, the case and the business date are held in the fixture as data, never written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S9-E6032-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: preflights the stub set, pins the contract version of every hop in the report, and loads the fixture: case `RW-2027-000834` at `PLACEMENT_DECIDED` with instruction type COLLECT, partner `PRT-SYN-0034-A` as the scorecard pick, partner `PRT-SYN-0034-B` as the override, partner `PRT-SYN-0034-C` at `SUSPENDED` with an ended contract, the reason code and reason text held in the fixture, and business date `2027-04-30`. On Day 1 the stubs of §12.8 return the same records.
2. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and names the case status and stage, so a change after any step has a baseline; then reads `GET /api/recovery/access/v1/me/session` and asserts the caller holds Partner portal C and R before an action is taken (AC6).
3. Harness: places the work with the scorecard pick through `POST /api/recovery/partner/v1/cases/{caseId}/instructions` with one Idempotency-Key, reads it back through `GET /api/recovery/partner/v1/partner/instructions`, and asserts the instruction answers partner `PRT-SYN-0034-A`, instruction type COLLECT, business date `2027-04-30` and status `SENT` (AC1, AC2).
4. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts exactly one entry for the pick, with its rule_id, its rule_version and the scorecard version the pick was made under (AC1, AC2).
5. Harness: overrides the placement to partner `PRT-SYN-0034-B` with the reason held in the fixture and a second Idempotency-Key, through the same published placement operation, and reads the instruction back through `GET /api/recovery/partner/v1/partner/instructions` and asserts it answers `PRT-SYN-0034-B` (AC2).
6. Harness: reads the decision log again and asserts two entries: the pick entry unchanged with its own rule_id, rule_version and scorecard version, and the override entry naming the pick it departs from, with the reason, its rule_id and its rule_version; and asserts no entry was overwritten, removed or re-hashed (AC2).
7. Harness: overrides again with the reason field empty and a third Idempotency-Key, and asserts 422 with MSG-GEN-001 naming the reason field, no instruction created, the instruction read unchanged and no third decision entry (AC3).
8. Harness: overrides again to partner `PRT-SYN-0034-C`, which is `SUSPENDED` with an ended contract, with the reason held in the fixture and a fourth Idempotency-Key, and asserts 409 with no instruction created for that partner and the case read the same status and stage as the baseline (AC4).
9. Harness: replays the override of step 5 with the same Idempotency-Key, and asserts the answer is the first answer unchanged, that one instruction exists for the case, that it names `PRT-SYN-0034-B`, and that the decision log still holds two entries and not three (AC2).
10. Harness: counts exactly one `rwb.partner.InstructionIssued.v1` on `rwb.partner.events.v1` per accepted placement and no publication from the refused and failed attempts, and observes `InstructionWorkflow` on the `rwb-partner` queue in the `rwb-recovery` namespace with its `issueInstruction` activity and the partner SLA timer for the instruction type (AC1, AC2).
11. Harness: resets the fixture to the snapshot after the pick, turns the fault switch on the decision-record hop on, overrides to `PRT-SYN-0034-B` with the reason under a new Idempotency-Key, and asserts the answer carries MSG-P7-003 with no instruction created, no `InstructionIssued` publication and both entries read unchanged; the switch and the fixture are reset before the next run (AC5).
12. Harness: calls the placement as a synthetic caller holding Partner portal R and not C, asserts 403 with MSG-P4-002, no instruction and no third entry (AC6).
13. Harness: writes one run report per action, keyed by story, case and instruction id, naming the contract version of each hop, whether the hop was a stub or the owner, the pick, the override partner, the reason code, the business date, both decision entries with their rule versions, the event counts, the workflow run and the gate verdict.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E6-032-01-ITG (ITG AC2) |
| X2 | The override replaces the pick instead of standing beside it, or the pick entry disappears from the log | The run fails on AC2 and the report names both entries, the rule version of each, and the entry that is missing or overwritten | None | TC-E6-032-01-ITG (ITG AC2) |
| X3 | An override without a reason is accepted, or is refused without MSG-GEN-001 on the reason field | The run fails on AC3 and the report names the answer, the status code and the field the message named | MSG-GEN-001 (expected, and missing) | TC-E6-032-04-ITG (ITG AC3) |
| X4 | An override to a partner outside the panel is accepted, or is refused after an instruction was created | The run fails on AC4 and the report names the partner, its `panel_status`, its `contract_end`, the answer and the instruction count for that partner | None (409 is the published error; no message is published for it) | TC-E6-032-04-ITG (ITG AC4) |
| X5 | A replay yields a second instruction, or a third decision entry | The run fails on AC2 and the report names the Idempotency-Key each attempt carried, the instruction count and the entry count | None | TC-E6-032-01-ITG (ITG AC2) |
| X6 | The forced decision-record failure leaves an instruction, an event or a changed entry, or answers without MSG-P7-003 | The run fails on AC5 and the report names the instruction count, the event count and both entries read before and after | MSG-P7-003 (expected, and missing) | TC-E6-032-02-ITG (ITG AC5) |
| X7 | A caller without Partner portal C is allowed to place or override, and no 403 is answered | The run fails on AC6 and the report names the caller role, the right the session answered, the operation and the answer; a 200 is a failure even when no data changed | MSG-P4-002 (expected, and missing) | TC-E6-032-03-ITG (ITG AC6) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14, and each is asserted by ID and by its substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S9-E6032-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic partner keys, the reason code, the fault switch, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The override is proved to stand beside the scorecard's pick with the reason recorded, an override without a reason and an override outside the panel are proved to create nothing, and one decision record per action is proved with its rule version |
| Estimable | One runner, one stub set, three synthetic partners, one case, one reason fixture, two placement calls, one read back, one decision read, three refused attempts, one event observer, one workflow observation and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S9-E6032-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Override an allocation with a reason - wave 4 integration harness

  Background:
    Given the synthetic case "RW-2027-000834" is at PLACEMENT_DECIDED on business date "2027-04-30"
    Given the scorecard pick is partner "PRT-SYN-0034-A" and the override partner is "PRT-SYN-0034-B"
    Given the partner "PRT-SYN-0034-C" is SUSPENDED with an ended contract
    Given the reason code is held in the fixture and the rule package in force holds R-WO-30 and R-UNI-24

  Scenario: AC1 Override an allocation with a reason (legacy RWB-E6-032 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the partner manager place work differently, with the reason recorded
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The override stands beside the scorecard pick and the reason is recorded (new, D-RCV-60)
    Given the work is placed with the scorecard pick "PRT-SYN-0034-A" through POST /api/recovery/partner/v1/cases/{caseId}/instructions with one Idempotency-Key
    When the partner manager overrides the placement to "PRT-SYN-0034-B" with the reason held in the fixture and a second Idempotency-Key
    Then GET /api/recovery/partner/v1/partner/instructions answers the instruction with "PRT-SYN-0034-B"
    And GET /api/recovery/decision/v1/decision-log?caseId={caseId} holds two entries
    And the pick entry is unchanged and keeps its rule_id, its rule_version and its scorecard version
    And the override entry names the pick it departs from, the reason, its rule_id and its rule_version
    And no entry is overwritten, removed or re-hashed
    When the override is replayed with the same Idempotency-Key
    Then one instruction exists for the case and the decision log still holds two entries

  Scenario: AC3 An override without a reason is refused with nothing created (new, D-RCV-60)
    Given an override of the placement to "PRT-SYN-0034-B" with the reason field empty
    When the partner manager calls POST /api/recovery/partner/v1/cases/{caseId}/instructions with a new Idempotency-Key
    Then the answer is 422 with "MSG-GEN-001" naming the reason field
    And no instruction is created and the instruction read is unchanged
    And GET /api/recovery/decision/v1/decision-log?caseId={caseId} holds no third entry

  Scenario: AC4 An override to a partner outside the panel is refused (new, D-RCV-60)
    Given the partner "PRT-SYN-0034-C" is SUSPENDED and its contract has ended
    When the partner manager overrides the placement to "PRT-SYN-0034-C" with the reason held in the fixture
    Then the answer is 409
    And no instruction is created for "PRT-SYN-0034-C"
    And the instruction still answers "PRT-SYN-0034-B" and the decision log still holds two entries
    And GET /api/recovery/case/v1/cases/{caseId} answers the same status and stage as the baseline

  Scenario: AC5 A forced decision-record failure stops the override with nothing changed (new, D-RCV-60)
    Given the decision record cannot be written for a further override of the placement
    When the partner manager overrides the placement from "PRT-SYN-0034-B" back to "PRT-SYN-0034-A" with the reason held in the fixture
    Then the answer carries "MSG-P7-003"
    And no instruction is created and no "rwb.partner.InstructionIssued.v1" is published
    And both decision entries are read unchanged
    And the instruction still answers "PRT-SYN-0034-B"

  Scenario: AC6 A caller without Partner portal C is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-CASEOWN" holding Partner portal R and not Partner portal C
    When the caller calls POST /api/recovery/partner/v1/cases/{caseId}/instructions
    Then the answer is 403 with "MSG-P4-002"
    And no instruction is created and no third entry is written
```

Legacy AC1 is the only legacy criterion this story owns. Legacy AC2 (the decision log cannot be written and nothing changes) stays with RWB-S9-E6032-APP as that story's build criterion and is asserted here across the service boundary in AC5, where the instruction, the event and both decision entries are read before and after the refused override. The override is driven through the one published placement operation, `POST /cases/{caseId}/instructions`, because the map publishes no separate override endpoint; the run never invents one, and the `InstructionRequest` shape the operation takes is held in the fixture from S9's CON story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Work is allocated to partners by measured return against a scorecard, not by a fixed share; the override departs from that answer and never replaces it | REQ-S9-003 |
| BR2 | An account on the panel with capacity is placed with the agency chosen on measured return and the instruction is sent, PLACEMENT_DECIDED to PLACED_WITH_AGENCY | R-WO-30 |
| BR3 | Where no agency on the panel has capacity, the placement is held and escalated on the timer and no instruction is sent | R-WO-31 |
| BR4 | A booked decision is corrected by a correcting entry naming the original, never overwritten; the override is that correcting entry and names the pick it departs from | R-UNI-24 |
| BR5 | A partner panel exit, a declared conflict of interest or an upheld conduct breach recalls every open case held by that partner, and the next partner is selected on the scorecard before the instruction is re-issued | R-UNI-26, R-UNI-27, R-UNI-29, R-UNI-45 |
| BR6 | A partner that misses its service level is chased once, then the work is recalled and re-selected on the scorecard | R-UNI-25 |
| BR7 | No value a business person may change is written in code; the partner panel, the contract end and the service levels are read from reference data with its version | BR-S9-004, FSD S9 A2.4.3.1 |
| BR8 | A required field that is empty is refused with MSG-GEN-001 naming the field, and an override carries its reason | VR-S9-004-1, FSD S9 A2.4.3.1; Temporal design slide 25, line 1739, "Partner manager: overrides need a reason" |
| BR9 | The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1` and confirmed by the central ledger in rwb-decision; nothing is created when it cannot be written | DP-03; ADR-022; legacy Principle 5, TC-E6-032-04 |
| BR10 | Every hop is one REST call on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout and no second hop, and no service reads another service's schema | DP-11, DP-13, DP-01 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E6032-APP, the pick they depart from is RWB-S9-E6031-APP's, and the rule versions are P7's.

### 9. State transitions

| From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|
| PLACEMENT_DECIDED | SOFT_RECOVERY_SELECTED | the scorecard pick is placed and the instruction is sent | PLACED_WITH_AGENCY | S9 rwb-partner, InstructionWorkflow `issueInstruction`, R-WO-30 |
| PLACEMENT_DECIDED | SOFT_RECOVERY_SELECTED | the partner manager overrides to a partner on the panel with a reason | PLACED_WITH_AGENCY | S9 rwb-partner, InstructionWorkflow `issueInstruction`, R-WO-30 with R-UNI-24 for the correcting entry |
| PLACEMENT_DECIDED | NO_AGENCY_CAPACITY | no agency on the panel has capacity, so the placement is held | PLACEMENT_DECIDED, held | S9 rwb-partner, R-WO-31; the timer escalates |
| PLACED_WITH_AGENCY | PARTNER_PANEL_EXIT | the partner leaves the panel or its contract ends | PARTNER_RECALLED | S9 rwb-partner, R-UNI-26 |
| PLACED_WITH_AGENCY | PARTNER_CONFLICT_DECLARED | the partner declares a conflict of interest | PARTNER_RECALLED | S9 rwb-partner, R-UNI-27 |
| PLACED_WITH_AGENCY | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld | PARTNER_RECALLED | S9 rwb-partner, R-UNI-29 |
| PARTNER_RECALLED | PARTNER_RESELECTED | the next partner is selected on the scorecard | the instruction is re-issued and the partner clock restarts | S9 rwb-partner, R-UNI-45 |
| SENT | partner acceptance | the partner accepts the instruction on the portal | ACCEPTED | S9 rwb-partner, `status` on partner_instruction, LOV-INSTR-STATUS |
| ACCEPTED | the result is reported | the partner reports on the portal | DONE | S9 rwb-partner, R-WO-33, the result of RWB-S9-E6033-APP |
| SENT or ACCEPTED | the work is recalled | a recall of R-UNI-25 to R-UNI-29 or R-UNI-45 fires | RECALLED | S9 rwb-partner, `status` on partner_instruction |

`PLACEMENT_DECIDED` and `PLACED_WITH_AGENCY` are the from-state and the to-state R-WO-30 gives, and `PLACEMENT_DECIDED` held is the state R-WO-31 keeps while the timer runs. The instruction states are the LOV-INSTR-STATUS values SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED that TSD S9 T3.2 publishes. The harness changes no state: it drives the two placement operations and reads the result through S9, P3 and P7, and the override moves no case stage of its own — the case stays where R-WO-30 put it, and the only thing the override adds is a second decision entry. The harness invents no state beyond the ones the sources give, and it never sets a state it then asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG Partner and agency manager | Primary. Holds Partner portal CRUDA in the TSD S9 T6.1 matrix, and is the only role the legacy story gives the action to |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT | Hold Partner portal CRU and so hold the right C the placement declares; the run records the right each operation answered with and asserts C on the placement path |
| PT-AGENCY Collection agency user | The partner-side role that acts on the instruction at the partner end; the matrix gives it Partner portal RU and the legacy permission table lists it among the holders of Partner portal U, so the run asserts R on the instruction read for it and never asserts C on the partner side |
| RW-CASEOWN Case owner | Holds Partner portal R and not C, and is the refused caller of AC6 |
| QA lead | Owns the harness configuration, the fixtures, the reason code, the fault switch, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S9 holds the partner, the partner user and the instruction and runs InstructionWorkflow; P3 holds the case; P7 holds the decision log and the central ledger; P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write | Owner |
|---|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | partner_code, partner_name, partner_type, panel_status, contract_end, score | Read through the rwb-partner contract | S9 rwb-partner, `rwb_partner` |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read through the rwb-partner contract; written by S9 on the two placement calls, not by the harness | S9 rwb-partner, `rwb_partner` |
| DF-WRK-009 to DF-WRK-016 | assignment | case_id, task_id, assignee_user_id, assigned_at, ended_at, reason, rule_id | Read through the rwb-case contract | P3 rwb-case, `rwb_case` |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code | Read through the rwb-case contract, before and after every attempt | P3 rwb-case, `rwb_case` |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, model_version, inputs_ref, override_reason, final_call, decided_at | Read through the rwb-decision contract; the entries are written by S9's placement and override, not by the harness | P7 rwb-decision, `rwb_decision` |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code, condition_expr, action_text, to_state, owner_role | Read through the rwb-decision contract | P7 rwb-decision, `rwb_decision` |

Field IDs are those in the Logical Data Model and Data Dictionary v9, and they are the entities the legacy data table of RWB-E6-032 cites under the same ranges. The reason and the pick the override departs from are carried by the decision entry and by nothing else: DF-DEC-013 `override_reason` is "Reason when the person did not follow the recommendation", and the pick is the earlier entry the override names through its own rule_id, its rule_version and its inputs reference. The assignment row carries the allocation reason DF-WRK-015 with its LOV-ASSIGN-REASON values, which is how P3 records that an allocation was manual rather than by rule. The harness owns no table and writes no row: the only changes it drives are S9's two published placement calls of §12.2, each with one Idempotency-Key, and everything else it reads is a contract read.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | ACs |
|---|---|---|---|---|
| POST | `/api/recovery/partner/v1/cases/{caseId}/instructions` | S9 rwb-partner | Issues the instruction to a partner by rule, right Partner portal C, one Idempotency-Key per action; it carries the scorecard pick of step 3 and the override that departs from it in step 5, and it is the refused operation of AC3, AC4, AC5 and AC6 | AC1, AC2, AC3, AC4, AC5, AC6 |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instruction, the partner it names, its instruction type, its due_at and its status after each accepted, refused and failed attempt | AC1, AC2, AC3, AC4, AC5 |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case status and stage before and after every attempt, so a change has a baseline and a refusal is proved to change nothing | AC1 to AC6 |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The pick entry with its rule id, rule version and scorecard version, the override entry that names it with its reason and rule version, and the proof that no third entry and no overwrite occurs | AC1, AC2, AC3, AC5 |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before an attempt, and the right the placement answered with | AC6 |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation in the Ownership Map. The map publishes no separate override operation, so the override rides on `POST /cases/{caseId}/instructions` — "Issue an instruction to a partner by rule", right C, one Idempotency-Key, errors 401, 403, 404, 409, 422 and 503 per API-S9-002 — with the scorecard's pick departed from; the `InstructionRequest` request shape and the `PartnerInstruction` response shape are not published either, and both are held in the fixture generated from S9's CON story. For a partner the edge path to the same operation is the partner gateway (FAPI 2.0) that fronts rwb-partner, and for a staff screen the placement would be composed by a gateway-bff route (DP-19); the run itself calls the service boundary the gateway fronts.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | S9 rwb-partner, EV-20, consumer the partner portal | Counts one publication per accepted placement and no publication from the refused, the failed or the replayed attempt | 
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision, written by S9 through the local decision-record library (DP-03) | Proves one record per accepted action with its rule version, two records after the override, and none from the forced failure |

The harness subscribes to both topics under one consumer group of its own, counts publications and replays the placement once to prove the inbox holds one processed row per consumer. The consumer effect it reads for the partner portal is the instruction read of §12.2; the consumer evidence for the portal push comes from the run fixture, because the portal exposes no operation for this event in this story.

#### 12.5 Workflows and activities

None added. The harness exercises `InstructionWorkflow`, S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace, through the placement and the override: its `issueInstruction` activity and the partner SLA timer for the instruction type are the ones the run observes in the workflow history (Arch v5 slide 17, lines 1245 to 1247; Temporal design slide 25, step 3 "Instruction sent EV-20 · partner clock"). It observes `CaseWorkflow` on `rwb-case` as the parent that holds the case the instruction was placed on, and observes it only: the override does not signal it and moves no case stage. Neither workflow, activity nor Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added, and none needed. The override is a user act and the partner clock is a workflow timer, so nothing in the journey is on a cron: the harness starts the run with its own placement call and holds the business date in the fixture. JOB-05 Timer check is retired in favour of durable timers inside the workflows, and the instruction's due_at is read as a workflow timer, not as a scheduled job.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): partner and partner_instruction are S9's in `rwb_partner`, assignment and recovery_case are P3's in `rwb_case`, decision_log_entry and rule_row are P7's in `rwb_decision`, and the roles, rights and session are P4's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (S9) | `POST /cases/{caseId}/instructions`, `GET /partner/instructions` | Case `RW-2027-000834` at `PLACEMENT_DECIDED`; partner `PRT-SYN-0034-A` as the scorecard pick, `PRT-SYN-0034-B` as the override and `PRT-SYN-0034-C` at `SUSPENDED` with an ended contract; an instruction `INS-SYN-2027-0034` placed once per Idempotency-Key with instruction type COLLECT, due_at and status `SENT`, and a repeat of the key returning the first answer unchanged; 422 with MSG-GEN-001 on the reason field, 409 to the partner outside the panel, and MSG-P7-003 with the fault switch on |
| Stub for rwb-case (P3) | `GET /cases/{caseId}` | Case `RW-2027-000834` with the same status and stage before and after every attempt, and the assignment reason `manual` where the override placed it |
| Stub for rwb-decision (P7) | `GET /decision-log?caseId={caseId}` | One pick entry with its rule_id, rule_version and scorecard version; a second entry after the override naming the pick, with its reason and its rule_id and rule_version; unchanged by the replay, the two refusals and the forced failure; the central ledger confirmation once per accepted action |
| Stub for rwb-access (P4) | `GET /me/session` | Allows RW-AGENCYMG with Partner portal CRUDA; refuses RW-CASEOWN on the placement path with 403 and MSG-P4-002 |
| Pick, override and reason fixture | The placement request shape from S9's CON story, and the panel check | The pick `PRT-SYN-0034-A`, the override `PRT-SYN-0034-B`, the suspended partner `PRT-SYN-0034-C`, the reason code and reason text, the instruction type COLLECT, the business date `2027-04-30` and the idempotency keys, all held as data |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic partners, case and instruction keys, the reason code, the business date, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0462; ASM-0654).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 5 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.partner.InstructionIssued.v1` and `rwb.decision-record.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; InstructionWorkflow on `rwb-partner` exercised through the placement and the override, with CaseWorkflow on `rwb-case` observed only |
| File | None. The placement request is S9's own body and the report is the harness's own output; no file or claim-check is transferred by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery-w4/partner-override`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None. DP-13 adds nothing: the legacy `/partner/instructions` path is rewritten onto S9's own base and there is no shared base left. DP-19 has two edges in this journey and the run names both: for the **partner** the route is the **partner gateway** in the DMZ under FAPI 2.0, which fronts rwb-partner and is the only path a partner has, and **gateway-bff** composes the **staff** screens only, including SCR-35 Placement and allocation where the partner manager would take the action. The one blocking dependency is the I story RWB-S9-E6032-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the six owned criteria in order for one case and holds the run lock, the fixture reset and the fault-switch reset |
| PickProbe | Service | Places the work with the scorecard pick once and reads the instruction back with the pick and status SENT |
| OverrideDriver | Service | Overrides the placement to the named partner with the reason and one Idempotency-Key, and replays the same key unchanged |
| InstructionReadBack | Service | Reads the instruction, the partner it names, its instruction type, its due_at and its status after every attempt |
| DecisionSideBySide | Service | Reads the two entries, proves the pick is unchanged and that the override names it, and proves nothing is overwritten, removed or re-hashed |
| ReasonProbe | Service | Sends the override with the reason field empty and asserts 422 with MSG-GEN-001 on that field |
| PanelProbe | Service | Sends the override to the suspended partner and asserts 409 with nothing created |
| EventProbe | Service | Subscribes to `rwb.partner.events.v1` and `rwb.decision-record.v1`, counts publications and replays the accepted placement once |
| AccessProbe | Service | Reads the session, asserts Partner portal C on the placement path, and makes the refused call as RW-CASEOWN |
| EvidenceReport | Service | Writes one report per action, keyed by story, case and instruction id, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S9-E6032-APP lands, on the case `RW-2027-000834`, the partners `PRT-SYN-0034-A` (the scorecard pick), `PRT-SYN-0034-B` (the override) and `PRT-SYN-0034-C` (suspended, contract ended), the instruction `INS-SYN-2027-0034`, the reason code from the fixture and business date `2027-04-30`. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the reason code, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0462; ASM-0654).

**Build steps**

1. Generate the five stubs and the pick, override and reason fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the PickProbe and the InstructionReadBack, and prove the work is placed with the scorecard pick and reads back as SENT with its instruction type and due_at (AC1, AC2).
3. Add the DecisionSideBySide read for the pick: one entry with its rule_id, rule_version and scorecard version, readable before the override and after it (AC1, AC2).
4. Add the OverrideDriver: the override to `PRT-SYN-0034-B` with the reason and a second Idempotency-Key, the read back, then the same key replayed and one instruction and two entries proved (AC2, X2, X5).
5. Add the DecisionSideBySide proof for the override: two entries, the pick unchanged, the override naming it with its reason and its rule version, and no overwrite, removal or re-hash (AC2, X2).
6. Add the ReasonProbe for AC3 and the PanelProbe for AC4: reason empty yields 422 with MSG-GEN-001 on the field, and the suspended partner yields 409; in both, no instruction, no event and no third entry (X3, X4).
7. Add the fault switch and the EventProbe for AC5: force the decision-record failure, assert MSG-P7-003, no instruction, no `InstructionIssued` publication and both entries unchanged, then reset the switch and the fixture (X6).
8. Add the AccessProbe for AC6 and the case baseline, then the EvidenceReport and the gate; swap a stub for the real owner as RWB-S9-E6032-APP lands (X7).

**Feature switch.** None. The harness has no production flag; the fault switch of step 7 exists in the test environment only and is reset by the runner before and after each run.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S9-E6032-APP when it lands, and the wave entry check holds a run report keyed by story, case and instruction id, with the pick and the override side by side and the addressee of each refusal named.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text and no refusal message of its own. MSG-GEN-001 is asserted with the reason field when the override is sent with that field empty, which is VR-S9-004-1 in FSD S9 A2.4.3.1 (X3, AC3). MSG-P4-002 is asserted with the place action when the caller holds Partner portal R but not C (X7, AC6). MSG-P7-003 is asserted when the decision record cannot be written and nothing is created (X6, AC5). The refusal of an override to a partner outside the panel is asserted by its published status code alone, 409 in API-S9-002's error list, because no source publishes a message for it; the run invents none.

### 15. Screens and states

The legacy story's screens are SCR-35 Placement and allocation and SCR-34 Partner list, and neither is built or rendered here: the harness calls the placement and the instruction read behind them and reads the states through the owners. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0462; ASM-0654).

| State | Read through | What the run asserts |
|---|---|---|
| The scorecard pick | S9 instruction read and the decision log | The work is with `PRT-SYN-0034-A`, status SENT, with its instruction type and due_at, and the pick entry carries its rule id, rule version and scorecard version |
| The override | S9 instruction read and the decision log | The instruction answers `PRT-SYN-0034-B` with the reason recorded, and the override entry names the pick, with its rule id and rule version, beside the pick entry |
| The refused override without a reason | S9 answer and the decision log | 422 with MSG-GEN-001 on the reason field, no instruction, no event, no third entry |
| The refused override to a partner outside the panel | S9 answer, the instruction read and the case read | 409, no instruction for that partner, the instruction still on the override partner, the case the same status and stage |
| A failed action | S9 answer, the event count and the two entries | MSG-P7-003, no instruction, no `InstructionIssued` publication, both entries unchanged |

SCR-34 Partner list and SCR-35 Placement and allocation belong to the S9 stories of the legacy key, and neither is built or read here. The partner manager reaches the placement through the partner gateway and a staff member reaches the same operation through a gateway-bff composite route (DP-19); this harness renders neither and asserts the operations behind them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-032-01-ITG | AC1 (legacy) and ITG AC2 | End to end | Case `RW-2027-000834`, the pick `PRT-SYN-0034-A` placed once, the override `PRT-SYN-0034-B` with the reason, the read back, the two decision entries and the replay, on business date `2027-04-30` |
| TC-E6-032-02-ITG | The not-recorded path across the boundary, ITG AC5, derived from legacy AC2 | Integration | A forced decision-record failure before the override, with the instruction, the event and both entries read before and after |
| TC-E6-032-03-ITG | Access, ITG AC6 | Component | A synthetic RW-CASEOWN caller holding Partner portal R and not C, on the placement path |
| TC-E6-032-04-ITG | Principle 5 and the two refusals, ITG AC3 and AC4 | Integration | The override with the reason field empty and the override to `PRT-SYN-0034-C`, suspended with a contract end, each with no instruction and no third entry |

The AC column names the legacy test each copy derives from and the ITG acceptance criteria it asserts: TC-E6-032-01-ITG derives from TC-E6-032-01, TC-E6-032-02-ITG from TC-E6-032-02, TC-E6-032-03-ITG from TC-E6-032-03 and TC-E6-032-04-ITG from TC-E6-032-04, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. Legacy AC2 stays with RWB-S9-E6032-APP, which owns the failure inside the service; the -ITG copy here asserts the same failure across the service boundary in AC5.

### 17. Guardrails

- No business value in code: the reason code, the reason text, the partners, the case, the business date, the fault switch and the report layout are data.
- The reason code and the override are data, and the scorecard pick is never recomputed or overwritten by the harness: the pick is read from S9 and its decision entry, and it is proved to be there afterwards.
- No personal data in logs, events, workflow inputs or reports: every key is synthetic, the partners are firms and not people, and the events carry IDs and facts only.
- Service data only through the owner's contract: the partner and the instruction from S9, the case from P3, the decision log and the rule rows from P7, the rights from P4; never a direct schema read and never another service's table (DP-01), and ACE data only through P1's contract where it arises (DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented operation and no invented message: only the one placement and the four reads of §12.2, and the refusal outside the panel is asserted by its published 409 alone.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The fault switch is reset by the runner before and after each run and is never left on; the harness never runs against UAT or production, never writes a row by hand, and a failing criterion is fixed in the owning service or raised as a gap and never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E6-032 Override an allocation with a reason | Recovery Workbench User Stories Epics 3 to 8 v4, lines 12066 to 12144 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 12085 to 12089 | Section 7, AC1, marked (legacy RWB-E6-032 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E6-032-02 | The same, lines 12091 to 12095 and 12140 | AC5 asserts the same failure here; the legacy criterion stays with RWB-S9-E6032-APP (section 19) |
| Legacy data table: assignment, partner, decision_log_entry, rule_row | The same, lines 12097 to 12104 | Section 11 |
| Legacy endpoints and permission checks | The same, lines 12106 to 12111 and 12120 to 12125 | Sections 10 and 12.2 |
| Legacy screens SCR-35 Placement and allocation and SCR-34 Partner list | The same, lines 12113 to 12118 | Section 15 |
| Legacy messages MSG-GEN-001, MSG-P4-002 and MSG-P7-003 | The same, lines 12127 to 12133 | Section 14, copied word for word |
| Legacy test cases TC-E6-032-01 to TC-E6-032-04 | The same, lines 12135 to 12142 | Copied as -ITG in section 16 |
| FEAT-PRM-04 Override an allocation with a reason, with FEAT-PRM-03 as its prerequisite | Epics 3 to 8 Specification v3, line 137, and line 136 | Sections 1, 2, 3 and 19 |
| REQ-S9-003 work is allocated by measured return against a scorecard, not by a fixed share | Business Requirements Program v5, line 432 (REQ-S9-001 at line 430) | Section 8, BR1, and section 2 |
| R-WO-30 place with the agency chosen on measured return and send the instruction; R-WO-31 no capacity, hold and escalate | Business Rules and Routing Logic v4, lines 361 and 362 | Sections 8 and 9, BR2 and BR3 |
| R-UNI-24 a booked decision is corrected by a correcting entry naming the original, never overwritten | The same, line 428 | Sections 2, 8 and 9, BR4 |
| R-UNI-26 panel exit, R-UNI-27 declared conflict, R-UNI-29 conduct breach, R-UNI-45 re-issue after re-selection | The same, lines 430, 431, 433 and 449 | Sections 8 and 9, BR5 and BR6 |
| FSD S9 A2.4: the step table, VR-S9-004-1 with MSG-GEN-001, BR-S9-004, the field catalogue, the roles and the two exception criteria (MSG-P4-002, MSG-P7-003) | Recovery Workbench FSD S9 Partner management v3, lines 328 to 408 | Sections 3, 8, 10 and 14 |
| TSD S9: field definitions and LOV-INSTR-STATUS, LOV-INSTRUCTION, LOV-PANEL; the RBAC matrix; API-S9-002 and API-S9-003 with their errors and the Idempotency-Key | Recovery Workbench TSD S9 Partner management v2, lines 63 to 106, 91 to 99, 130 to 165 and 197 to 244 | Sections 3, 9, 10 and 12.2 |
| S9 contract: the placement and the instruction read, InstructionWorkflow, `rwb_partner` and `rwb.partner.events.v1` | Architecture v5, lines 1245 to 1256 and 1270 to 1272 | Sections 2, 12.2, 12.5 and 12.7 |
| rwb-partner ownership, schema, topic, task queue and wave 4 | Architecture v5 slide 41, line 2891 | Sections 1, 12.7 and 13 |
| InstructionIssued, producer rwb-partner, consumer the partner portal | Architecture v5 slide 43, row 20, line 2946 | Section 12.4, AC2 |
| The edge: partners only through the partner gateway under FAPI 2.0, gateway-bff for staff screens | Architecture v5, line 1458; DP-19 | Sections 2, 13 and 15 |
| Temporal design slide 25: step 2 "Scorecard picks partner", step 3 "Instruction sent EV-20 · partner clock", the UNIVERSAL package rules R-UNI-29 and R-UNI-28, and "Partner manager: overrides need a reason" | Temporal and Drools Design Text Extract v1, lines 1663 to 1755, line 1739 quoted | Sections 2, 8, 12.5 and 12.6 |
| DF-PRT-001 to DF-PRT-007, DF-PRT-008 to DF-PRT-016, DF-WRK-009 to DF-WRK-016, DF-CAS-001 to DF-CAS-023, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015 outbox and inbox on Kafka, ADR-020 contract-first REST with one hop and 2 s, ADR-022 local decision record plus central ledger | Architecture Decision Records v4 | Sections 12.4, 8 and 12.2 |
| The six criteria of this harness and the gap and assumption behind its configuration | This file, sections 3, 7 and 12.8; GAP-0462 and ASM-0654 | Sections 3, 7, 12.8, 13 and 15 |

### 19. Out of scope

- RWB-S9-E6032-CON and RWB-S9-E6032-APP: the build of the override, the reason, the instruction and the decision record inside the service, including legacy AC2 (the not-recorded path), which is its build criterion and which this story asserts only across the boundary in AC5.
- The scorecard pick and the placement rule themselves (RWB-S9-E6031-CON and RWB-S9-E6031-APP): the fixture holds the pick and the run reads it and never recomputes it.
- The panel and fee schedule versions (RWB-S9-E6030) and the partner onboarding (RWB-S9-E6029): the run reads the panel status and the contract end and builds neither.
- The result intake of RWB-S9-E6033 and the partner result of FEAT-PRM-05, beyond the instruction status the run reads back.
- The recall and re-selection paths as products (R-UNI-25, R-UNI-26, R-UNI-27, R-UNI-28, R-UNI-29 and R-UNI-45, and the universal rules slide 25 names), which are asserted around the override and built by their own stories.
- The partner review and the conduct check (FEAT-PRM-10 and FEAT-PRM-13), and the fee approval of FEAT-PRM-09.
- The partner portal screens SCR-34 Partner list and SCR-35 Placement and allocation, the partner gateway and the external partner sign-in, and the gateway-bff composite routes, which DP-19 names but this story neither builds nor calls.
- The platform H stories DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, which the platform wave delivers.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
