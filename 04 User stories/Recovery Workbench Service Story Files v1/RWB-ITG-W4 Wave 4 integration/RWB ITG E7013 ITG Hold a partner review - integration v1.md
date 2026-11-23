# RWB-ITG-E7013-ITG Hold a partner review

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7013-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S9-E7013-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-013 as the wave 4 integration proof of the partner review, driven through the S9 partner read, the instruction read and the result write, with the decision record read back through rwb-decision; the build of the review itself is RWB-S9-E7013-APP and its CON story. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the review of a partner to be held against the six points every partner type is managed on, with the actions recorded once and the decision record carrying the rule version, proved end to end through the real partner and decision contracts**, so that **partners are placed, paid and measured by rule, and a review that cannot be recorded changes nothing**.

This story builds the wave 4 integration harness and the evidence, and nothing else. The review, the six-point screen and the recording of the actions are built by S9 in RWB-S9-E7013-APP and its CON story. The harness drives the review action through S9's published operations, observes the events on the owners' topics, reads the decision record back through rwb-decision, and writes a run report per partner. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A partner can hold work, submit results and be paid, and still never be reviewed. That is the gap this story is written against. Every partner type — agency, law firm, valuer, auction vendor, broker, debt buyer, AMC and RAMC — is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit (REQ-S9-001). If no review is held, a partner whose conduct breached is still allocated work, a partner whose contract has ended still holds open cases, and the panel decision is taken on a score nobody has looked at beside the contract.

The review is also where the recall and escalation context lands. A partner that misses its service level on the portal is chased once and then recalled (R-UNI-25); a partner that leaves the panel or whose contract ends has every open case recalled and re-selected (R-UNI-26); a declared conflict withdraws the instruction and re-selects the next partner (R-UNI-27); an upheld conduct or complaint breach suspends allocation, recalls the affected cases and is reported to the partner review (R-UNI-29); and a service level exceeded in the current state is escalated to the named escalation point while the case does not move (R-UNI-30). Partner performance, conduct and complaint data are reported to the partner review forum (REQ-S9-007), which is why this harness asserts the six points as named evidence rather than as a narrative.

The monthly scorecard is FEAT-PRM-08 and the legacy story depends on it; the review reads the score through S9's partner read and leaves the scorecard itself out of scope. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). The harness carries REQ-S9-001 and REQ-S9-007 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S9 rwb-partner (the partner read, the instruction read and the result write), P7 rwb-decision (the decision log), P3 rwb-case (the case) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The partner portal rights are in force for the run: Partner portal R to read the partner and the instructions, Partner portal U to record a result. The right lists in the legacy section name RW-NPAMGR and PT-AGENCY among the holders of U; the harness itself holds no business right.
- A synthetic partner on the panel and two instructions on one case are held in the fixture as data, with the rule package version the fixture names rather than a version written in code.
- RWB-S9-E7013-APP owns the review, the six points and the recording of the actions; until it lands, the stub set of §12.8 stands in for its effect and the story is reported as a stub pass.
- The monthly scorecard (FEAT-PRM-08) is not asserted here: the partner read carries the score of DF-PRT-007 and its calculation is RWB-S9-E7013-*'s sibling scope.
- The harness environment and base hosts, the fixture layout, the synthetic partner and instruction keys, the review evidence shape, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0474; ASM-0666).
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S9-E7013-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: partner `PTR-SYN-0007` with partner_code `PTR-SYN-0007`, partner_type AGENCY, panel_status ACTIVE and contract_end 2027-12-31, holding instructions `INS-SYN-000701` and `INS-SYN-000702` on case `RW-2027-000701`. On Day 1 the stub of §12.8 returns the same records.
2. Harness: reads the partner through `GET /api/recovery/partner/v1/partners` with the `type` and `status` filters, and asserts the partner_code, partner_type, panel_status and contract_end, and that the score row is present (DF-PRT-001 to DF-PRT-007).
3. Harness: reads `GET /api/recovery/partner/v1/partner/instructions` and asserts the two instruction rows with their case_id, partner_id, instruction_type, instructed_at, due_at and status (DF-PRT-008 to DF-PRT-016).
4. Harness: runs the review of the six points of REQ-S9-001 for the partner, and names each point in the evidence with its evidence source: selection and contract and fees and notice and exit from the partner read, targets and incentives and data exchange from the instruction read, performance reviews from the score on the partner read.
5. Harness: records the action decided for each instruction through `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results`, once per instruction, and asserts the answer carries the instruction with its status and result.
6. Harness: submits the same result a second time and asserts the answer is 409 and one result remains, so a repeated click is never a second action.
7. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry for the review with its decision_code, rule_id and rule_version, and that the entry records the rule version in force.
8. Harness: counts one `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` and asserts the central ledger in rwb-decision confirmed the record, then replays the event and asserts the decision log still holds one entry for the review.
9. Harness: counts the `rwb.partner.InstructionIssued.v1` and `rwb.partner.PartnerResultSubmitted.v1` publications on `rwb.partner.events.v1` and asserts the consumer effect through `GET /api/recovery/case/v1/cases/{caseId}`, then replays each event and asserts the case and the instruction are unchanged, because the inbox holds one processed row per consumer.
10. Harness: forces the local decision-record library to fail for the review action and asserts the action stops with MSG-P7-003, no result is recorded against the instruction and the decision log holds no entry for the review.
11. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller holding Partner portal R and not U, then attempts the result write and asserts 403 with MSG-P4-002 and no state change.
12. Harness: writes one run report per partner, keyed by story and partner_code, naming the contract version of each hop, whether the hop was a stub or the owner, the six points with their evidence source, the decision record and its rule version, and the pass or fail gate.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no point is marked evidenced | None | TC-E7-013-01-ITG (ITG AC1) |
| X2 | A point of the six has no evidence behind it in either read | The run fails on AC2 and the report names the point, the read and the missing field; a point is never reported as passed from a narrative | None | TC-E7-013-01-ITG (ITG AC2) |
| X3 | The review action completes and no decision entry carries the rule version | The run fails on AC3 and the report names the case, the entry and the missing rule version | None | TC-E7-013-01-ITG (ITG AC3) |
| X4 | The central ledger has not confirmed the decision record and the action completes anyway | The run fails on AC3 and the report names the case, the entry and the missing confirmation; confirmation is never assumed | MSG-P7-003 | TC-E7-013-04-ITG (ITG AC3) |
| X5 | The same result is submitted twice and a second action is recorded | The run fails on AC3 and the report names the two submissions and the instruction; a repeated click is never a second action | None | TC-E7-013-01-ITG (ITG AC3) |
| X6 | The decision record fails and the instruction still moves | The run fails on AC4 and the report names the instruction status before and after; nothing changes is asserted, not assumed | MSG-P7-003 (expected) | TC-E7-013-02-ITG (ITG AC4) |
| X7 | A caller without Partner portal U is allowed to record a result | The run fails on AC5 and the report names the caller's rights, the operation and the answer; a 200 is a failure even when no business data changed | MSG-P4-002 (expected, and missing) | TC-E7-013-03-ITG (ITG AC5) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S9-E7013-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the review evidence shape, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The six points are proved to be evidenced from named reads, the actions are proved to be recorded once, and a review that cannot be recorded is proved to change nothing |
| Estimable | One runner, one stub set, one partner probe, one instruction probe, one result write, one decision read-back, one event observer and one report |
| Small | Fits in one sprint with its five criteria and four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S9-E7013-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Hold a partner review - wave 4 integration harness

  Background:
    Given the synthetic partner "PTR-SYN-0007" is on the panel with partner_type "AGENCY", panel_status "ACTIVE" and contract_end 2027-12-31
    Given the partner holds instructions "INS-SYN-000701" and "INS-SYN-000702" on case "RW-2027-000701"
    Given the review set for the partner is loaded as data and the fixture names the rule package version in force

  Scenario: AC1 Hold a partner review (legacy RWB-E7-013 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then runs the review against the six points every partner type is managed on, and records the actions
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The six points are evidenced through the owners' reads (new, D-RCV-60)
    Given the partner read returns "PTR-SYN-0007" with partner_code, partner_type, panel_status, contract_end and score
    And the instruction read returns "INS-SYN-000701" and "INS-SYN-000702" with case_id, partner_id, instruction_type, instructed_at, due_at and status
    When the review is run for the partner
    Then each of the six points of REQ-S9-001 is named in the evidence with its evidence source
    And selection is evidenced from the partner read: partner_type and panel_status
    And contract and fees is evidenced from the partner read: contract_end, with the fee schedule as versioned reference data
    And targets and incentives is evidenced from the instruction read: instructed_at, due_at and status
    And data exchange is evidenced from the instruction read: the result reported against each instruction
    And performance reviews is evidenced from the partner read: score, whose calculation is the monthly scorecard
    And notice and exit is evidenced from the partner read: contract_end and panel_status
    And a point with no evidence behind it is reported as a gap in the evidence, never as a pass

  Scenario: AC3 The actions are recorded once and the decision record carries the rule version (new, D-RCV-60)
    Given the review has decided the action for "PTR-SYN-000701" and for "PTR-SYN-000702"
    When each action is recorded through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    Then each instruction carries its result once and its status moves through S9's own states
    And the same result submitted again is refused with 409 and one result remains
    And the review writes one decision record with its decision_code, rule_id and rule_version
    And "rwb.decision-record.DecisionRecorded.v1" is published once on "rwb.decision-record.v1" and confirmed by the central ledger in rwb-decision
    And a replay of the event leaves the decision log with one entry for the review
    And "rwb.partner.PartnerResultSubmitted.v1" is published once on "rwb.partner.events.v1" and consumed once by rwb-case, rwb-litigation and rwb-asset

  Scenario: AC4 A forced decision-record failure stops the review action (new, D-RCV-60)
    Given the local decision-record library is forced to fail for the review action
    When the review action is recorded through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    Then the action stops with "MSG-P7-003"
    And no result is recorded against the instruction
    And the decision log holds no entry for the review
    And the partner, the instruction and the case are unchanged when they are read again

  Scenario: AC5 A caller without the Partner portal U right is refused (new, D-RCV-60)
    Given a synthetic caller whose right set holds Partner portal R and not Partner portal U
    When the caller records a result through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    Then the answer is 403 with "MSG-P4-002"
    And no result and no decision record are written
```

Legacy AC2 (the decision log cannot be written) is built and tested in RWB-S9-E7013-APP, and this story asserts the same failure at the review action through AC4.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit | REQ-S9-001 |
| BR2 | Partner performance, conduct and complaint data are reported to the partner review forum | REQ-S9-007 |
| BR3 | When the partner misses the service level on the portal, the work is chased once and then recalled and re-selected on the scorecard, to PARTNER_RECALLED | R-UNI-25 |
| BR4 | When the partner leaves the panel or the contract ends, every open case held by that partner is recalled and re-selected, to PARTNER_RECALLED | R-UNI-26 |
| BR5 | When the partner declares a conflict of interest, the instruction is withdrawn and the next partner on the scorecard is selected, to PARTNER_RECALLED | R-UNI-27 |
| BR6 | When a conduct or complaint breach is upheld, allocation is suspended, the affected cases are recalled and the breach is reported to the partner review, to PARTNER_RECALLED | R-UNI-29 |
| BR7 | When the time in the current state exceeds the service level, the breach is raised to the named escalation point and the case does not move, to ESCALATED | R-UNI-30 |
| BR8 | Every call is one hop on the owner's base with a 2 s budget, and the decision record is written through the local decision-record library on the shared topic and confirmed by the central ledger | DP-11, DP-13, DP-03; ADR-020, ADR-022 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E7013-APP, and BR3 to BR7 are the recall and escalation context the review forum sees, not states the harness sets.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| SENT | `PartnerResultSubmitted` on `rwb.partner.events.v1` | the partner records the result on the portal | IN_PROGRESS |
| IN_PROGRESS | `PartnerResultSubmitted` on `rwb.partner.events.v1` | the result is the final one for the instruction | DONE |
| SENT | PARTNER_NO_RESPONSE | the service level is missed and the chase has run once (R-UNI-25) | RECALLED |
| SENT | PARTNER_CONFLICT_DECLARED | the partner declares a conflict (R-UNI-27) | RECALLED |
| ANY_ACTIVE | PARTNER_PANEL_EXIT | the partner leaves the panel or the contract ends (R-UNI-26) | RECALLED |
| ANY_ACTIVE | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld (R-UNI-29) | RECALLED |

SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED are the instruction status values of DF-PRT-014; PARTNER_NO_RESPONSE, PARTNER_PANEL_EXIT, PARTNER_CONFLICT_DECLARED and PARTNER_CONDUCT_BREACH are the event codes of R-UNI-25, R-UNI-26, R-UNI-27 and R-UNI-29, whose to_state is PARTNER_RECALLED, and `PartnerResultSubmitted` is the event of Arch v5 slide 43 row 21. R-UNI-30 leaves the case in place and records ESCALATED. The harness changes no state: S9 rwb-partner owns every instruction status above and drives InstructionWorkflow, and P3 rwb-case holds the case state the run reads. The panel status of DF-PRT-005 (ACTIVE, ON_NOTICE, SUSPENDED, EXITED) is a classification the run reads, not a transition it makes. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-NPAMGR, partner and agency manager | Holds Partner portal U and R; is the role the review is written for and the role that records the actions |
| RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-DEBTSALE | Read the partner and the instructions where their rights allow; the R list of the legacy section names them |
| PT-AGENCY, partner user | Records the result of its own instruction on the portal; holds Partner portal U per the legacy section |
| RW-AGENCYMG, RW-GUARANT, RW-DEBTSALE | Hold U per the legacy section; read the same review evidence |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S9 runs InstructionWorkflow, answers the partner and instruction reads, records the result and writes the decision record; P7 holds the central ledger; P3 holds the case; P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the review is the manager's, and authorisation is answered by rwb-access and the DoA table of P4 |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end, score | Read through the rwb-partner contract |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read through the rwb-partner contract; the result write is S9's |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, inputs_ref | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, event_code | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v8. The legacy section names partner with DF-PRT-001 to DF-PRT-007; partner_instruction is the FSD S9 field catalog and the dictionary gives it DF-PRT-008 to DF-PRT-016, so those rows are cited where the dictionary gives them and no field ID is invented. The partner and its instructions are S9's, the decision log and the rule rows are P7's, and the case behind the instruction is P3's; the harness reads them only through those contracts and never from a schema. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The partner, its type, panel status, contract end and score, with the optional `type` and `status` filters (AC1, AC2, AC5) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instructions placed with the partner, with their case, type, due time and status (AC1, AC2, AC3) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/results` | S9 rwb-partner | Records the action decided in the review against its instruction, once (AC1, AC3, AC4, AC5) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of the review, with its decision code and rule version (AC1, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state before and after the action, and the consumer effect of the partner events (AC3, AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a read or a write (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19). The Ownership Map publishes no partner-review operation and no scorecard read for this feature, so the review is not called through an operation of its own here: it is asserted through the partner read, the instruction read and the decision log, which is what the manager's screen would read after the action.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | S9 rwb-partner | Counts the publication of the instruction the review reads, and proves the instruction is off the partner clock once it is issued (AC3) |
| `rwb.partner.PartnerResultSubmitted.v1` | `rwb.partner.events.v1` | S9 rwb-partner | Counts one publication per recorded action and asserts the case effect once, with the replay proving one processed row per consumer (AC3) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | S9 rwb-partner through the local decision-record library (DP-03) | Proves the decision record of the review was published with its rule version and confirmed by the central ledger, and stays one entry after a replay (AC3, AC4) |

The harness subscribes to both topics under one consumer group of its own, counts publications and replays each event once. The consumer effect it reads is the case through the rwb-case operation of §12.2; the inbox row counts of rwb-litigation and rwb-asset, the other consumers of `rwb.partner.PartnerResultSubmitted.v1`, come from the consumer evidence in the run fixture, because neither consumer exposes an operation in this story. `rwb.partner.InstructionIssued.v1` is consumed by the partner portal, so it is observed by count only.

#### 12.5 Workflows and activities

None added. The harness exercises InstructionWorkflow, S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace, and observes what it does: the SLA timer per partner type that turns a missed service level into a chase and then a recall, and the activities `issueInstruction` and `recordResult`. They are stated here as observed and not built here; no workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. InstructionWorkflow is started by the instruction and held by its own SLA timer, so the harness starts nothing by cron and sets no overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); partner and partner_instruction are S9's, decision_log_entry and rule_row are P7's, and recovery_case is P3's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (partner read) | `GET /partners` | Partner `PTR-SYN-0007` with partner_code, partner_type AGENCY, panel_status ACTIVE, contract_end 2027-12-31 and a score, filtered by the `type` and `status` parameters it is given |
| Stub for rwb-partner (instruction read) | `GET /partner/instructions` | Instructions `INS-SYN-000701` and `INS-SYN-000702` on case `RW-2027-000701`, each with its instruction_type, instructed_at, due_at, status and result |
| Stub for rwb-partner (result write) | `POST /partner/instructions/{instructionId}/results` | Accepts the result once per instruction, returns the instruction with its new status, and returns 409 on a second submission of the same result |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One entry for the review with its decision_code, rule_id, rule_version and inputs_ref, and the central ledger confirmation |
| Stub for rwb-case | `GET /cases/{caseId}` | Case `RW-2027-000701` with its state unchanged across the review action and the forced failure |
| Stub for rwb-access | `GET /me/session` | Allows RW-NPAMGR with Partner portal U and R; refuses a caller holding R and not U with 403 and MSG-P4-002 |
| Partner-review fixture | The six points and the actions decided | The review set for `PTR-SYN-0007` as data: the point names, the action decided for each of the two instructions and the rule package version, at the point where S9's review would answer |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the stub answer for the review and its evidence shape, the fixture layout, the synthetic partner and instruction keys, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0474; ASM-0666).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 6 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; three consumed, `rwb.partner.InstructionIssued.v1`, `rwb.partner.PartnerResultSubmitted.v1` and `rwb.decision-record.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; InstructionWorkflow on `rwb-partner` observed, with its SLA timer and the `issueInstruction` and `recordResult` activities |
| File | None. The result write accepts documents on the S9 contract, and the run holds no file of its own |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies the table adds, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None; DP-13 adds none. The only blocking dependency is the I story RWB-S9-E7013-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| ReviewRunner | Job | Runs the five owned criteria in order for a partner and holds the run lock |
| PartnerProbe | Service | Reads the partner with its type, panel status, contract end and score, and names the point each value evidences |
| InstructionProbe | Service | Reads the instructions with their case, type, due time and status, and reads them again after each action |
| ActionDriver | Service | Records the decided action once per instruction, retries a repeated submission and asserts the 409 |
| DecisionReadBack | Service | Reads the decision log and asserts one entry with its rule version and the ledger confirmation |
| EventObserver | Service | Subscribes to `rwb.partner.events.v1` and `rwb.decision-record.v1`, counts publications and replays each event once |
| StubSet | Fake | The six stubs and the partner-review fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per partner keyed by story and partner_code, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S9-E7013-APP lands, on the synthetic partner `PTR-SYN-0007`, instructions `INS-SYN-000701` and `INS-SYN-000702`, case `RW-2027-000701` and contract end 2027-12-31. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the review evidence shape, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0474; ASM-0666).

**Build steps**

1. Generate the six stubs and the partner-review fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the PartnerProbe and the InstructionProbe and prove the two reads answer the partner and its instructions with every field of AC2 (X2).
3. Name the six points of REQ-S9-001 in the evidence with their evidence source, and fail the run where a point has no evidence behind it (AC2).
4. Build the ActionDriver for AC3 against both instructions, and prove one action per instruction, a 409 on a repeated submission and one result left behind (X5).
5. Add the DecisionReadBack for AC1 and AC3: one decision record with its decision code and rule version, and the ledger confirmation before the action is reported as recorded (X3, X4).
6. Add the EventObserver for AC3: one publication of each partner event, the case effect once, a replay that changes nothing, and one decision entry after the replay.
7. Add the forced decision-record failure for AC4 through the instruction read before and after, so nothing changes is asserted and not assumed (X6).
8. Add the session read and the refused result write for AC5, then the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S9-E7013-APP lands (X7).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S9-E7013-APP when it lands, and the wave entry check holds a run report keyed by story and partner_code.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. The legacy section carries these three messages for the feature and no S9-specific message, so none is invented here: MSG-GEN-001 with the missing field when a read is made short of a required parameter, MSG-P4-002 with the refused action on the result write, and MSG-P7-003 when the decision record cannot be written and nothing changes.

### 15. Screens and states

The harness renders no screen: it observes the owners' operations and writes a report. The legacy section names SCR-34 Partner list and SCR-35 Placement and allocation, which belong to S9 and its CON story; the harness neither builds nor reads them, and it asserts their data through the partner read and the instruction read.

| State | Read through | What the run asserts |
|---|---|---|
| ACTIVE, ON_NOTICE, SUSPENDED, EXITED (panel status) | rwb-partner partner read | The panel classification of the partner at the time of the review (DF-PRT-005) |
| SENT, ACCEPTED, IN_PROGRESS, DONE, DECLINED, RECALLED (instruction status) | rwb-partner instruction read | The status of each instruction before and after the action, and that a refused or failed action leaves it unchanged (DF-PRT-014) |
| The six points of the review | rwb-partner partner and instruction reads | Each point is named with its evidence source, or reported as a gap in the evidence |
| The decision record of the review | rwb-decision decision log | One entry with its decision code, rule version and inputs reference, confirmed by the central ledger |
| The case state | rwb-case case read | The case is unchanged by the review action and by the forced failure |
| PARTNER_RECALLED, ESCALATED | the rule rows and the instruction read | The recall and escalation context the review forum sees, recorded by S9 and never set by the harness |

The environment, layout and retention of the run report are Not specified in the source documents (GAP-0474; ASM-0666).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-013-01-ITG | AC1 (legacy); ITG AC1 | End to end | One partner on the panel with two instructions, the review and the decision record live |
| TC-E7-013-02-ITG | Legacy AC2 not recorded stays with RWB-S9-E7013-APP; ITG AC4 | Integration | The decision-record library forced to fail on the review action |
| TC-E7-013-03-ITG | Access; ITG AC5 | Component | A caller holding Partner portal R and not U |
| TC-E7-013-04-ITG | Principle 5; ITG AC4 | Integration | A forced decision-record failure with the partner and instruction reads before and after |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx under the same legacy test case ID. Legacy AC2, the forced decision-log failure, stays with RWB-S9-E7013-APP and is asserted here at the review action through AC4.

### 17. Guardrails

- No business value in code: the partner, its type, its panel status, the contract end, the rule package version, the six point names, the actions and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- ACE data only through the owner's contract or `v_ace_*` views: this run reads no ACE data at all, and the partner, instruction, decision and case rows are read only through their owners' contracts (DP-01).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- A point of the six is evidenced or reported as a gap; it is never written up from a narrative.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-013 Hold a partner review | Recovery Workbench User Stories Epics 3 to 8 v3, lines 12555 to 12633 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 12574 to 12578 | Section 7, AC1, marked (legacy RWB-E7-013 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E7-013-02 | The same, lines 12580 to 12583 and 12628 | AC4 asserts the same failure here; the legacy AC stays with RWB-S9-E7013-APP (section 19) |
| Legacy test cases TC-E7-013-01 to TC-E7-013-04 | The same, lines 12627 to 12630 | Copied as -ITG in section 16 |
| FEAT-PRM-10 Hold a partner review | Epics 3 to 8 Specification v3, line 143 | Sections 1, 2 and 3 |
| FEAT-PRM-08 Score partners monthly | Epics 3 to 8 Specification v3, line 141 | Sections 2, 3 and 19: the score is read, the scorecard is not built here |
| The S9 partner, instruction and result operations | Epics 3 to 8 Specification v3, lines 217 to 219; API Specification v4 `/partners`, `/partner/instructions`, `/partner/instructions/{instructionId}/results` | Section 12.2 |
| REQ-S9-001 and REQ-S9-007 | Business Requirements Program v4, lines 430 and 436 | Section 8, BR1 and BR2; section 7, AC2 |
| R-UNI-25, R-UNI-26, R-UNI-27, R-UNI-29 and R-UNI-30 | Business Rules and Routing Logic v4, lines 429 to 434 | Sections 2, 8 and 9 |
| S9 rwb-partner contract, InstructionWorkflow and the partner topic | Architecture v5 slides 17 and 41; slide 43 rows 20 and 21 | Sections 2, 12.2, 12.4 and 12.5 |
| InstructionWorkflow SLA timers, chase then recall | Temporal and Drools design slide 25 | Sections 2, 8 and 12.5 |
| DF-PRT-001 to DF-PRT-007, DF-PRT-008 to DF-PRT-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v8 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v3 | Sections 8 and 12: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |

### 19. Out of scope

- RWB-S9-E7013-CON and RWB-S9-E7013-APP: the build of the review, the six-point screen and the recording of the actions.
- The S9 build: the partner and instruction tables, the result write, InstructionWorkflow, the panel reference data and the partner portal rights.
- The monthly scorecard (FEAT-PRM-08) and the calculation of the score; this story reads the score of DF-PRT-007 and nothing else.
- The partner gateway and FAPI 2.0: partner users reach the portal through the DMZ gateway, which is the edge stories' own scope.
- The partner panel, fee schedule and service level reference data (FEAT-PRM-02) and the panel change (FEAT-ADM-07).
- The recall and re-selection work of R-UNI-25 to R-UNI-30 as products: the harness asserts the context, it does not build the recall.
- Platform deployment and configuration, and the platform H dependencies named in section 13.
- Any production change: the harness runs in the test environment only.
