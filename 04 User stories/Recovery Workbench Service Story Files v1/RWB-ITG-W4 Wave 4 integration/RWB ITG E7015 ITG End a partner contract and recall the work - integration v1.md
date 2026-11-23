# RWB-ITG-E7015-ITG End a partner contract and recall the work

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7015-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S9-E7015-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-015 as the wave 4 integration proof of the contract end and the recall of the work, driven through the S9 partner read, the instruction read and the result write, with the contract-end action sequenced through the S9 fixture hook, the decision record read back through rwb-decision and the recall read back through rwb-case; the build of the contract end, the recall, the re-selection and the instruction states is RWB-S9-E7015-APP and its CON story. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the contract of a partner to be closed and every open case pulled back for re-selection, proved end to end through the real partner, instruction, case and decision contracts**, so that **partners are placed, paid and measured by rule, and a contract end that cannot be recorded changes nothing**.

This story builds the wave 4 integration harness and its evidence, and nothing else. The contract end, the recall of the instruction, the re-selection of the next partner and the instruction states are built by S9 in RWB-S9-E7015-APP and its CON story. The harness sequences the contract-end action through S9's fixture hook, observes the events on the owners' topics, reads the partner, the instructions and the case before and after, reads the decision record back through rwb-decision, and writes a run report per partner. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A panel exit or a contract end is the one point where every open case a partner holds has to come back at once. The legacy story states it as a single action: close the contract and pull every open case back for re-selection. R-UNI-26 gives the rule and the clock — recall every open case held by that partner and re-select, to PARTNER_RECALLED, within 5 working days — and REQ-S9-006 gives the trigger set: a panel exit, a declared conflict of interest, insolvency or an upheld conduct breach. If the recall is only half done, a partner that has left still holds live instructions, work is not re-placed, and the case sits outside the clock the partner was managed on.

The recall is also where the rest of the partner rules land. A missed service level is chased once and then recalled (R-UNI-25); a declared conflict withdraws the instruction and re-selects the next partner (R-UNI-27); insolvency recalls the work and stops fee payments (R-UNI-28); an upheld conduct breach suspends allocation and recalls the affected cases (R-UNI-29); an open case keeps the rule version it was decided under when a new version takes effect (R-UNI-38); and no action proceeds unlogged, because a decision log entry that cannot be written blocks the action (R-UNI-39). FEAT-PRM-12 is the feature, and the contract end sits behind FEAT-PRM-11, the notice on a missed target, which is the step before the exit on the S9 journey. S9 turns the partner service levels into timers — recall 5 working days, re-select 2 working days — which is why this harness asserts the effect through the reads and not through a state it sets.

Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). The harness carries REQ-S9-001 and REQ-S9-006 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S9 rwb-partner (the partner read, the instruction read and the result write), P7 rwb-decision (the decision log), P3 rwb-case (the case) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The partner portal rights are in force for the run: Partner portal R to read the partner and the instructions, Partner portal U to record a result. The right lists in the legacy section name RW-NPAMGR, RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG and PT-AGENCY among the holders of U; the harness itself holds no business right.
- A synthetic partner on the panel with a passed contract end and panel status EXITED, two open instructions on one case, and one result already recorded, are held in the fixture as data, with the rule package version the fixture names rather than a version written in code.
- RWB-S9-E7015-APP owns the contract end, the recall, the re-selection and the instruction states; until it lands, the contract-end fixture hook and the stub set of §12.8 stand in for its effect and the story is reported as a stub pass.
- The recall of R-UNI-25 and R-UNI-27 to R-UNI-29 is context this run reads, not a state it makes; the panel reference data and the fee schedule (FEAT-PRM-02) are read as versioned reference data and are not built here.
- The harness environment and base hosts, the fixture layout, the synthetic partner, instruction and case keys, the stub answer shapes, the fixture hook that stands in for the unpublished contract-end action, the definition of "open case" the recall enumerates, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0479; ASM-0671).
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S9-E7015-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: partner `PTR-SYN-0015` with partner_code `PTR-SYN-0015`, partner_type AGENCY, panel_status EXITED and contract_end 2027-03-31, holding instructions `INS-SYN-001501` (status SENT, one result recorded) and `INS-SYN-001502` (status ACCEPTED) on case `RW-2027-001501`. On Day 1 the stub of §12.8 returns the same records.
2. Harness: reads the partner through `GET /api/recovery/partner/v1/partners` and asserts the partner_code, partner_type, panel_status and contract_end, and that the contract end has passed or the panel status is EXITED.
3. Harness: reads `GET /api/recovery/partner/v1/partner/instructions` and asserts the two open instructions with their case_id, instructed_at, due_at and status, and that both belong to the partner.
4. Harness: submits the result of `INS-SYN-001501` through `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results`, then submits the same result a second time, and asserts one result is left against the instruction.
5. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and records the case state before the recall, so nothing changes can be asserted later and not assumed.
6. Harness: sequences the contract-end action through the S9 fixture hook of §12.8, because the Ownership Map publishes no operation for it; the hop is marked stub until RWB-S9-E7015-APP lands and is reported as a stub pass.
7. Harness: reads the partner and the instructions again and asserts that every open instruction of the partner reads RECALLED with its case_id, instructed_at, due_at and status, and that the partner still reads with its panel_status and contract_end.
8. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` again and asserts the case reads the recall, with no state set by the harness at any point.
9. Harness: submits a result for the recalled instruction `INS-SYN-001502` after the recall and asserts the write is refused with 409 or 422, the exact code the published contract of S9 names, and that the recalled instruction does not move.
10. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry for the contract end with its decision_code, rule_id and rule_version, and that the entry records the rule version in force.
11. Harness: counts one `rwb.partner.PartnerResultSubmitted.v1` on `rwb.partner.events.v1`, asserts the consume in rwb-case through the case read and the consume in rwb-litigation and rwb-asset through the consumer evidence in the fixture, counts the `rwb.decision-record.DecisionRecorded.v1` and the `rwb.partner.InstructionIssued.v1`, then replays each event and asserts nothing changes.
12. Harness: forces the local decision-record library to fail for the contract-end action and asserts the action stops with MSG-P7-003, the partner, the instructions and the cases are unchanged when they are read again, and no decision entry exists.
13. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller holding Partner portal R and not U, then attempts the result write and asserts 403 with MSG-P4-002 and nothing changes.
14. Harness: writes one run report per partner, keyed by story and partner_code, naming the contract version of each hop, whether the hop was a stub or the owner, the recall set with its instruction and case keys, the decision record and its rule version, and the pass or fail gate.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no hop is marked as a real pass | None | TC-E7-015-01-ITG (ITG AC1) |
| X2 | The partner read shows a contract end in the future and a panel status other than EXITED | The run fails on AC2 and the report names the partner, the contract_end and the panel_status; a recall is never run on a partner that has not exited | None | TC-E7-015-01-ITG (ITG AC2) |
| X3 | An open instruction still reads SENT or ACCEPTED after the recall | The run fails on AC2 and the report names the instruction, its status and its case_id; the recall set is never reported as complete from a narrative | None | TC-E7-015-01-ITG (ITG AC2) |
| X4 | The case does not read the recall after the recall is sequenced | The run fails on AC2 and the report names the case, the state before and the state after | None | TC-E7-015-01-ITG (ITG AC2) |
| X5 | A result is accepted for an instruction that already reads RECALLED | The run fails on AC3 and the report names the instruction, the result and the answer; a recalled instruction that moves is a failure even when the write returned 200 | None | TC-E7-015-01-ITG (ITG AC3) |
| X6 | The same result submitted twice before the recall leaves two results | The run fails on AC3 and the report names the two submissions and the instruction; a repeated click is never a second result | None | TC-E7-015-01-ITG (ITG AC3) |
| X7 | The contract end completes and no decision entry carries the rule version | The run fails on AC3 and the report names the case, the entry and the missing rule version | None | TC-E7-015-01-ITG (ITG AC3) |
| X8 | The decision record fails and the partner, an instruction or a case still moves | The run fails on AC4 and the report names the value before and after; nothing changes is asserted, not assumed | MSG-P7-003 (expected) | TC-E7-015-02-ITG (ITG AC4) |
| X9 | A caller holding Partner portal R and not U is allowed to submit a result | The run fails on AC5 and the report names the caller's rights, the operation and the answer; a 200 is a failure even when no business data changed | MSG-P4-002 (expected, and missing) | TC-E7-015-03-ITG (ITG AC5) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts, the stubs and the S9 fixture hook from Day 1; the only wait is RWB-S9-E7015-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the fixture hook, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The recall is proved to reach every open instruction and the case through the owners' reads, the in-flight result write is proved to be refused, and a contract end that cannot be recorded is proved to change nothing |
| Estimable | One runner, one stub set, one fixture hook, one partner probe, one instruction probe, one case probe, one result write, one decision read-back, one event observer and one report |
| Small | Fits in one sprint with its five criteria and four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S9-E7015-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: End a partner contract and recall the work - wave 4 integration harness

  Background:
    Given the synthetic partner "PTR-SYN-0015" is on the panel with partner_type "AGENCY", panel_status "EXITED" and contract_end 2027-03-31
    Given the partner holds the open instructions "INS-SYN-001501" and "INS-SYN-001502" on case "RW-2027-001501"
    And the contract-end set for the partner is loaded as data and the fixture names the rule package version in force

  Scenario: AC1 End a partner contract and recall the work (legacy RWB-E7-015 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then closes the contract and pulls every open case back for re-selection
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The recall is proved through the owners' reads (new, D-RCV-60)
    Given the partner read returns "PTR-SYN-0015" with partner_code, partner_type, panel_status and contract_end
    And the contract end date of the partner has passed or the panel status is "EXITED"
    When the contract is ended and every open case of the partner is recalled
    Then every open instruction of the partner reads "RECALLED" with its case_id, instructed_at, due_at and status
    And every affected case reads the recall through GET /api/recovery/case/v1/cases/{caseId}
    And nothing in the partner, the instructions or the cases is set by the harness

  Scenario: AC3 The in-flight result write is refused after the recall (new, D-RCV-60)
    Given the result of "INS-SYN-001501" is submitted through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    And the same result is submitted a second time before the recall
    When the contract end is sequenced and a result is submitted for the recalled instruction "INS-SYN-001502"
    Then the second submission before the recall leaves one result against "INS-SYN-001501"
    And the submission after the recall is refused with 409 or 422, the exact code the published contract of S9 names
    And the recalled instruction "INS-SYN-001502" does not move
    And one decision record is written with decision_code, rule_id and rule_version
    And "rwb.partner.PartnerResultSubmitted.v1" is published once on "rwb.partner.events.v1" and consumed once by rwb-case, rwb-litigation and rwb-asset
    And a replay of the event changes nothing

  Scenario: AC4 A forced local decision-record failure stops the contract-end action (new, D-RCV-60)
    Given the local decision-record library is forced to fail for the contract-end action
    When the contract is ended and the work is recalled
    Then the action stops with "MSG-P7-003"
    And the partner, the instructions and the cases are unchanged when they are read again
    And no decision entry exists for the action

  Scenario: AC5 A caller holding Partner portal R and not U is refused on the result write (new, D-RCV-60)
    Given a synthetic caller whose right set holds Partner portal R and not Partner portal U
    When the caller submits a result through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    Then the answer is 403 with "MSG-P4-002"
    And nothing changes
```

Legacy AC2 (the decision log cannot be written) is built and tested in RWB-S9-E7015-APP, and this story asserts the same failure at the contract-end action through AC4.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A partner panel exit, a declared conflict of interest, insolvency or an upheld conduct breach recalls every open case held by that partner | REQ-S9-006 |
| BR2 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit | REQ-S9-001 |
| BR3 | When the partner misses the service level on the portal, the work is chased once and then recalled and re-selected on the scorecard, to PARTNER_RECALLED | R-UNI-25 |
| BR4 | When the partner leaves the panel or the contract ends, every open case held by that partner is recalled and re-selected, to PARTNER_RECALLED, within 5 working days | R-UNI-26 |
| BR5 | When the partner declares a conflict of interest, the instruction is withdrawn and the next partner on the scorecard is selected, to PARTNER_RECALLED | R-UNI-27 |
| BR6 | When the partner enters insolvency, the work is recalled, the documents and any cash held are secured and fee payments stop, to PARTNER_RECALLED | R-UNI-28 |
| BR7 | When a conduct or complaint breach is upheld, allocation is suspended, the affected cases are recalled and the breach is reported to the partner review, to PARTNER_RECALLED | R-UNI-29 |
| BR8 | When a new rule version reaches its effective date, it applies to decisions taken from that date, and open cases keep the version they were decided under | R-UNI-38 |
| BR9 | When the decision log entry cannot be written, the action is blocked and no action proceeds unlogged | R-UNI-39 |
| BR10 | Every call is one hop on the owner's base with a 2 s budget, and the decision record is written through the local decision-record library on the shared topic | DP-11, DP-13, DP-03; ADR-020, ADR-022 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E7015-APP, and BR3 and BR5 to BR7 are the recall context the exit sits in, not states the harness sets.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| SENT | `PartnerResultSubmitted` on `rwb.partner.events.v1` | the partner records the result on the portal | IN_PROGRESS |
| ACCEPTED | PARTNER_PANEL_EXIT | the partner leaves the panel or the contract ends (R-UNI-26) | RECALLED |
| SENT | PARTNER_PANEL_EXIT | the partner leaves the panel or the contract ends (R-UNI-26) | RECALLED |
| ANY_ACTIVE | PARTNER_NO_RESPONSE | the service level is missed and the chase has run once (R-UNI-25) | RECALLED |
| ANY_ACTIVE | PARTNER_CONFLICT_DECLARED | the partner declares a conflict (R-UNI-27) | RECALLED |
| ANY_ACTIVE | PARTNER_INSOLVENT | the partner enters insolvency (R-UNI-28) | RECALLED |
| ANY_ACTIVE | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld (R-UNI-29) | RECALLED |

SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED are the instruction status values of DF-PRT-014; PARTNER_NO_RESPONSE, PARTNER_PANEL_EXIT, PARTNER_CONFLICT_DECLARED, PARTNER_INSOLVENT and PARTNER_CONDUCT_BREACH are the event codes of R-UNI-25 to R-UNI-29, whose to_state is PARTNER_RECALLED, and `PartnerResultSubmitted` is the event of Arch v5 slide 43 row 21. The panel status of DF-PRT-005 (ACTIVE, ON_NOTICE, SUSPENDED, EXITED) is a classification the run reads, not a transition it makes. S9 rwb-partner owns every instruction status above and drives InstructionWorkflow; P3 rwb-case holds the case state the run reads. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-NPAMGR, partner and agency manager | Holds Partner portal U and R; is the role the contract end is written for, and the role that closes the contract |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY | Hold Partner portal U per the legacy section and record results on the instructions they hold |
| RW-CASEOWN, RW-TEAMMGR, RW-LEGAL | Read the partner and the instructions where their rights allow; the R list of the legacy section names them |
| QA lead | Owns the harness configuration, the fixtures, the fixture hook, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S9 runs InstructionWorkflow, answers the partner and instruction reads, records the result and writes the decision record; P7 holds the central ledger; P3 holds the case; P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the exit is the manager's, and authorisation is answered by rwb-access and the DoA table of P4 |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Read through the rwb-case contract |
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | Read through the rwb-partner contract |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read through the rwb-partner contract; the result write is S9's |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v8. The legacy section gives recovery_case DF-CAS-001 to DF-CAS-023, partner DF-PRT-001 to DF-PRT-007, decision_log_entry DF-DEC-001 to DF-DEC-018 and rule_row DF-REF-001 to DF-REF-015; partner_instruction is the FSD S9 field catalog and the dictionary gives it DF-PRT-008 to DF-PRT-016, so those rows are cited where the dictionary gives them and no field ID is invented. The partner and its instructions are S9's, the case is P3's and the decision log and the rule rows are P7's; the harness reads them only through those contracts and never from a schema. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The partner, its type, its panel status and its contract end, before and after the recall (AC1, AC2) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The open instructions of the partner, with their case, due time and status, before and after the recall (AC1, AC2, AC3) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/results` | S9 rwb-partner | The in-flight result write: one result before the recall, a repeated submission, and a submission refused after the recall (AC1, AC3, AC4, AC5) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of the contract end, with its decision code and rule version (AC1, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case before and after the recall, and the consumer effect of the partner event (AC2, AC3, AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a read or a write (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The contract-end and recall action itself has no published operation in the Ownership Map, so the harness sequences it through the S9 fixture hook of §12.8, reports that hop as a stub pass until RWB-S9-E7015-APP lands, and proves the effect through the reads — never by setting a state it then asserts. No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.partner.PartnerResultSubmitted.v1` | `rwb.partner.events.v1` | S9 rwb-partner | Counts one publication per recorded result, asserts the consume once in each of rwb-litigation, rwb-asset and rwb-case, and proves a replay changes nothing (AC3) |
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | S9 rwb-partner | Counts the publication of each instruction the run reads, so the instruction set under recall is evidenced from the owner (AC2); it is consumed by the partner portal, so it is counted only |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | S9 rwb-partner through the local decision-record library (DP-03) | Proves the decision record of the contract end was published with its rule version and that the case saw one record (AC3, AC4) |

The harness subscribes to both topics under one consumer group of its own, counts publications and replays each event once. The consumer effect it reads is the case through the rwb-case operation of §12.2; the consume in rwb-litigation and rwb-asset, the other consumers of `rwb.partner.PartnerResultSubmitted.v1`, comes from the consumer evidence in the run fixture, because neither consumer exposes an operation in this story.

#### 12.5 Workflows and activities

None added. The harness observes InstructionWorkflow, S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace: its SLA timer per partner type, which is what turns a missed service level into a chase and a recall, and the activities `issueInstruction` and `recordResult`. The recall is held by that workflow and its timer; the harness starts nothing and holds nothing. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. InstructionWorkflow is started by the instruction and held by its own SLA timer, so the harness starts nothing by cron and sets no overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); partner and partner_instruction are S9's, recovery_case is P3's, and decision_log_entry and rule_row are P7's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (partner read) | `GET /partners` | Partner `PTR-SYN-0015` with partner_code, partner_type AGENCY, panel_status EXITED and contract_end 2027-03-31, and the same partner with panel_status ACTIVE on the negative case of X2 |
| Stub for rwb-partner (instruction read) | `GET /partner/instructions` | Instructions `INS-SYN-001501` (SENT, one result) and `INS-SYN-001502` (ACCEPTED) on case `RW-2027-001501`, and both reading RECALLED after the recall is sequenced |
| Stub for rwb-partner (result write) | `POST /partner/instructions/{instructionId}/results` | Accepts the result once per instruction and returns it with its new status; refuses with the code the published contract names where the instruction reads RECALLED |
| S9 contract-end fixture hook | No published operation (the contract-end and recall action) | Sequences the contract end and the recall of every open instruction of `PTR-SYN-0015` at the point where RWB-S9-E7015-APP would answer: the partner keeps its partner_code, partner_type, panel_status and contract_end, the open instructions move to RECALLED, and the case reads the recall |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One entry for the contract end with its decision_code, rule_id and rule_version, and no entry where the action was blocked |
| Stub for rwb-case | `GET /cases/{caseId}` | Case `RW-2027-001501` reading the recall after the hook, and unchanged across the refused write and the forced failure |
| Stub for rwb-access | `GET /me/session` | Allows RW-NPAMGR with Partner portal U and R; refuses a caller holding R and not U with 403 and MSG-P4-002 |
| Contract-end fixture | The contract end and the recall set | The action set for `PTR-SYN-0015` as data: the contract end date, the panel status, the instruction keys under recall and the rule package version, at the point where S9's contract end would answer |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the stub answer shapes, the fixture hook and its answer, the definition of "open case" the recall enumerates, the fixture layout, the synthetic partner, instruction and case keys, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0479; ASM-0671).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 6 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; three consumed, `rwb.partner.PartnerResultSubmitted.v1`, `rwb.partner.InstructionIssued.v1` and `rwb.decision-record.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; InstructionWorkflow on `rwb-partner` observed, with its SLA timer and the `issueInstruction` and `recordResult` activities |
| File | None. The result write holds no file in this run, and the report is written to the wave record |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies the table adds, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None; DP-13 adds none. The only blocking dependency is the I story RWB-S9-E7015-APP, which replaces its stub and its fixture hook; until it is live the run uses the stub, and a stub pass is reported as a stub pass. The story is Day 1.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| ContractEndRunner | Job | Runs the five owned criteria in order for a partner and holds the run lock |
| PartnerProbe | Service | Reads the partner with its partner_code, partner_type, panel_status and contract_end, before and after the recall |
| InstructionProbe | Service | Reads the open instructions with their case_id, instructed_at, due_at and status, and reads them again after the recall |
| ResultDriver | Service | Submits one result, repeats the submission, and submits again after the recall to assert the refusal |
| ContractEndHook | Fake | Sequences the contract end and the recall at the point where RWB-S9-E7015-APP would answer, and never writes a row by hand |
| CaseProbe | Service | Reads the case before and after the recall, and after the forced failure |
| DecisionReadBack | Service | Reads the decision log and asserts one entry with its decision code and rule version |
| EventObserver | Service | Subscribes to `rwb.partner.events.v1` and `rwb.decision-record.v1`, counts publications and replays each event once |
| StubSet | Fake | The stub set and the two fixtures of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per partner keyed by story and partner_code, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs and the fixture hook from Day 1 and the real services as RWB-S9-E7015-APP lands, on the synthetic partner `PTR-SYN-0015`, instructions `INS-SYN-001501` and `INS-SYN-001502`, case `RW-2027-001501` and contract end 2027-03-31. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the stub answer shapes, the fixture hook's answer, the definition of "open case", the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0479; ASM-0671).

**Build steps**

1. Generate the stub set and the two fixtures of §12.8 from the published contracts, pin each contract version in the report, and fail the run on a mismatch (X1).
2. Build the PartnerProbe and the InstructionProbe and prove the two reads answer the partner and its open instructions with every field of AC2 (X2).
3. Build the ResultDriver for AC3: one result on `INS-SYN-001501`, a repeated submission that leaves one result, and the answer read against the contract's code (X6).
4. Build the ContractEndHook and sequence the contract end, then read the partner and the instructions again and prove every open instruction reads RECALLED (X3).
5. Add the CaseProbe and prove the case reads the recall through its owner, with no state set by the harness (X4).
6. Submit a result for the recalled instruction and prove the refusal and that the instruction does not move (X5).
7. Add the DecisionReadBack for AC1 and AC3: one decision record with its decision code and rule version (X7).
8. Add the EventObserver for AC3: one publication of the partner event, the consume once in each of rwb-case, rwb-litigation and rwb-asset, a replay that changes nothing, and the instruction and decision counts (AC3).
9. Add the forced decision-record failure for AC4 through the partner, instruction and case reads before and after, so nothing changes is asserted and not assumed (X8).
10. Add the session read and the refused result write for AC5, then the EvidenceReport and the gate, and swap a stub or the hook for the real owner as RWB-S9-E7015-APP lands (X9).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the stubs and the fixture hook and again against RWB-S9-E7015-APP when it lands, and the wave entry check holds a run report keyed by story and partner_code.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. The legacy section carries these three messages for the feature and no S9-specific message, so none is invented here: MSG-GEN-001 with the missing field when a read is made short of a required parameter, MSG-P4-002 with the refused action on the result write, and MSG-P7-003 when the decision record cannot be written and nothing changes.

### 15. Screens and states

The harness renders no screen: it observes the owners' operations and writes a report. The legacy section names SCR-34 Partner list and SCR-35 Placement and allocation, which belong to S9 and its CON story; the harness neither builds nor reads them, and it asserts their data through the partner read, the instruction read and the case read.

| State | Read through | What the run asserts |
|---|---|---|
| ACTIVE, ON_NOTICE, SUSPENDED, EXITED (panel status) | rwb-partner partner read | The panel classification of the partner at the contract end, and that an exit is what the recall is run on (DF-PRT-005) |
| SENT, ACCEPTED, IN_PROGRESS, DONE, DECLINED, RECALLED (instruction status) | rwb-partner instruction read | The status of each open instruction before and after the recall, and that a refused result write leaves a recalled instruction unchanged (DF-PRT-014) |
| The recall set of the partner | rwb-partner instruction read and rwb-case case read | Every open instruction reads RECALLED and every affected case reads the recall, or the run reports the instruction or the case as a gap in the evidence |
| The decision record of the contract end | rwb-decision decision log | One entry with its decision code, its rule version and its case, and no entry where the action was blocked |
| The case state | rwb-case case read | The case is unchanged by the refused result write and by the forced failure |
| PARTNER_RECALLED, ESCALATED | the rule rows and the instruction read | The recall and escalation context S9 records, never set by the harness |

The environment, layout and retention of the run report are Not specified in the source documents (GAP-0479; ASM-0671), and so is the definition of "open case" the recall enumerates; until both are agreed the report names the instruction keys it counted so the set can be checked by hand.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-015-01-ITG | AC1 (legacy); ITG AC1 | End to end | One partner with a passed contract end and two open instructions, the contract-end hook, the recall and the decision record live |
| TC-E7-015-02-ITG | Legacy AC2 not recorded stays with RWB-S9-E7015-APP; ITG AC4 | Integration | The decision-record library forced to fail on the contract-end action |
| TC-E7-015-03-ITG | Access; ITG AC5 | Component | A caller holding Partner portal R and not U |
| TC-E7-015-04-ITG | Principle 5; ITG AC4 | Integration | A forced decision-record failure with the partner, instruction and case reads before and after |

The Covers column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx under the same legacy test case ID. Legacy AC2, the forced decision-log failure, stays with RWB-S9-E7015-APP and is asserted here at the contract-end action through AC4.

### 17. Guardrails

- No business value in code: the partner, its type, its panel status, the contract end, the rule package version, the recall set and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- ACE data only through the owner's contract or `v_ace_*` views: this run reads no ACE data at all, and the partner, instruction, case and decision rows are read only through their owners' contracts (DP-01).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub, the fixture hook or the owner.
- The fixture hook sequences the contract end; it never writes a row, and the harness never asserts a state it set itself.
- The harness never runs against UAT or production.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-015 End a partner contract and recall the work | Recovery Workbench User Stories Epics 3 to 8 v3, lines 12718 to 12797 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 12737 to 12741 | Section 7, AC1, marked (legacy RWB-E7-015 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E7-015-02 | The same, lines 12743 to 12746 and 12792 | AC4 asserts the same failure here; the legacy AC stays with RWB-S9-E7015-APP (section 19) |
| Legacy test cases TC-E7-015-01 to TC-E7-015-04 | The same, lines 12791 to 12794 | Copied as -ITG in section 16 |
| FEAT-PRM-12 End a partner contract and recall the work | Epics 3 to 8 Specification v3, line 145 | Sections 1, 2 and 3 |
| FEAT-PRM-11 Issue a notice on a missed target | Epics 3 to 8 Specification v3, line 144 | Section 2: the notice is the step before the exit and is not asserted here |
| FEAT-PRM-02 Hold the partner panel and fee schedule as data | Epics 3 to 8 Specification v3, line 135 | Sections 3 and 19: the panel, fee schedule and service levels are read as reference data |
| The S9 partner, instruction and result operations | Epics 3 to 8 Specification v3, lines 217 to 219; API Specification v4 `/partners`, `/partner/instructions`, `/partner/instructions/{instructionId}/results` | Section 12.2 |
| REQ-S9-001 and REQ-S9-006 | Business Requirements Program v4, lines 430 and 435 | Section 8, BR2 and BR1; section 7, AC2 |
| R-UNI-25, R-UNI-26, R-UNI-27, R-UNI-28 and R-UNI-29 | Business Rules and Routing Logic v4, lines 429 to 433 | Sections 2, 8 and 9 |
| R-UNI-38 and R-UNI-39 | Business Rules and Routing Logic v4, lines 442 and 443 | Sections 2, 8 and 9: the rule version in force, and no action unlogged |
| S9 rwb-partner contract, InstructionWorkflow and the partner topic | Architecture v5 slides 17 and 41; slide 43 rows 20 and 21; slide 42 row 08 | Sections 2, 12.2, 12.4 and 12.5 |
| InstructionWorkflow SLA timers, recall 5 working days and re-select 2 working days | Temporal and Drools design slide 25 | Sections 2, 8, 9 and 12.5 |
| DF-CAS-001 to DF-CAS-023, DF-PRT-001 to DF-PRT-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v8 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v3 | Sections 8 and 12: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |

### 19. Out of scope

- RWB-S9-E7015-CON and RWB-S9-E7015-APP: the build of the contract end, the recall, the re-selection and the instruction states.
- The S9 build: the partner and instruction tables, the result write, InstructionWorkflow, the panel reference data and the partner portal rights.
- The published operation for the contract-end action: this story sequences it through the fixture hook and does not create an operation for it.
- The notice on a missed target (FEAT-PRM-11) and its cure period; the panel, fee schedule and service level reference data (FEAT-PRM-02).
- The partner gateway and FAPI 2.0: partner users reach the portal through the DMZ gateway, which is the edge stories' own scope.
- The recall and re-selection work of R-UNI-25 to R-UNI-29 as products: the harness asserts the effect, it does not build the recall.
- Platform deployment and configuration, and the platform H dependencies named in section 13.
- Any production change: the harness runs in the test environment only.
