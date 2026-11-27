# RWB-ITG-E7014-ITG Issue a notice on a missed target

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7014-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Set at refinement by the squad; not sized in this story |
| Depends on (build) | RWB-S9-E7014-APP (not done; the notice build) |
| Contract dependencies | RWB-S9-E7014-CON |
| Integration dependencies | RWB-S9-E7014-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-014 as the wave 4 integration proof of the notice on a missed target and the start of the cure period, driven through the S9 partner and instruction reads, the P6 notice write and read-back, the P6 notice events and the P7 decision record; the build of the notice itself is RWB-S9-E7014-APP and P6 rwb-comms in its own stories. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E7014-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 2 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the contractual notice to go out when a partner misses its target and the cure period to start, proved end to end through the real partner, notice and decision contracts**, so that **partners are placed, paid and measured by rule, and a notice that cannot be recorded changes nothing**.

This story builds the wave 4 integration harness and its evidence, and nothing else. The feature itself, the screen and the data are built by S9 in RWB-S9-E7014-APP, and the notice, its template and its dispatch are built by P6 rwb-comms in its own stories. The harness loads the fixture, compares the score with the contractual target of the rule version the fixture names, drives the notice write and the notice read-back through P6's published operations, observes the notice events on P6's topic and the decision record on the shared topic, reads the case and the session back through their owners, and writes one run report per case and partner. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A partner can be measured every month and still never be told, in writing, that it missed. That is the gap this story is written against. The notice on a missed target is the point of the six points every partner type is managed on at which measurement turns into a contractual consequence: the partner is served the notice its contract provides for, and the cure period it has to put the miss right starts to run (REQ-S9-001, FEAT-PRM-11). Without it, a miss is a number on a scorecard and nothing follows, the cure period has no start, and the same partner is allocated the same work next month.

The notice also sits inside the recall and conduct context. A partner that misses its service level on the portal is chased once and then has the work recalled (R-UNI-25, REQ-S9-005); an upheld conduct or complaint breach suspends allocation, recalls the affected cases and is reported to the partner review (R-UNI-29); a service level exceeded in the current state is raised to the named escalation point while the case does not move (R-UNI-30); and partner performance, conduct and complaint data are reported to the partner review forum (REQ-S9-007). A notice is the evidence those processes are run on, which is why this harness asserts the notice, its type, its sent date and the cure period start as named facts rather than as a narrative.

The score is the monthly scorecard (FEAT-PRM-08) and the legacy story depends on it; the harness reads the score through S9's partner read and leaves the scorecard's calculation out of scope. The contractual target and the length of the cure period are versioned reference data under FEAT-PRM-02, and a new rule version applies to decisions taken from its effective date while open cases keep the version they were decided under (R-UNI-38), which is why the fixture names the rule version and the harness never writes one in code. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The decision record is written by the owning service through the local decision-record library on `rwb.decision-record.v1` (DP-03) and confirmed by the central ledger in rwb-decision; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). The harness carries REQ-S9-001, REQ-S9-005 and REQ-S9-007 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S9 rwb-partner (the partner read and the instruction read), P6 rwb-comms (the notice write and the notice read), P7 rwb-decision (the decision log), P3 rwb-case (the case) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one. The run builds against contract version 5.0.0 (`info.version` in API Specification v5) of rwb-partner, rwb-comms, rwb-decision, rwb-case and rwb-access, on their `/v1` paths.
- The partner portal rights are in force for the run: Partner portal C to issue a notice and Partner portal R to read the partner and the instructions. The right lists in the legacy section name RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT and RW-AGENCYMG among the holders of C; the harness itself holds no business right.
- A synthetic partner on the panel with a score below the contractual target of the named rule version, one instruction on one case, and one approved notice template for the notice type are held in the fixture as data, and the fixture names the rule version, the target, the score, the notice type and the cure period length rather than a value written in code.
- The cure period length is read from versioned reference data under FEAT-PRM-02, dated and read back; the harness asserts the start it records against that length and never counts the period itself.
- RWB-S9-E7014-APP owns the notice action, its screen and its data; until it lands, the stub set of §12.8 stands in for its effect and the story is reported as a stub pass.
- The monthly scorecard (FEAT-PRM-08) is not asserted here: the partner read carries the score of DF-PRT-007 and its calculation is RWB-S9-E7014-*'s sibling scope.
- The harness environment and base hosts, the fixture layout, the synthetic partner, instruction, case and notice keys, the stub answer shapes, the conduct of the missed-target comparison against the named rule version, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0475; ASM-0667).
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S9-E7014-APP, which replaces its stub as it lands and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: the synthetic partner with partner_code, partner_type, panel_status, contract_end and score, one instruction on one case, the notice type, the approved template for it, the rule version, the contractual target of that version, the cure period length, and the case and partner keys. On Day 1 the stub set of §12.8 returns the same records (GAP-0475; ASM-0667).
2. Harness: reads the partner through `GET /api/recovery/partner/v1/partners` and asserts partner_code, partner_type, panel_status, contract_end and score (DF-PRT-001 to DF-PRT-007).
3. Harness: reads `GET /api/recovery/partner/v1/partner/instructions` and asserts the instruction on the case with its case_id, partner_id, instruction_type, instructed_at, due_at and status (DF-PRT-008 to DF-PRT-016).
4. Harness: compares the score with the contractual target of the rule version the fixture names and records the miss as a fact of the run, with the rule version beside it; the comparison never uses a target taken from the code (R-UNI-38).
5. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and holds the case state before the notice, so that "nothing changes" can be asserted later rather than assumed.
6. Harness: issues the notice through `POST /api/recovery/comms/v1/cases/{caseId}/notices` with the notice type and the template the fixture names, and asserts 201 with the notice carrying notice_type and sent_date (DF-LEG-015 to DF-LEG-023).
7. Harness: reads the notice back through `GET /api/recovery/comms/v1/notices/{noticeId}` and asserts the same notice, field for field, and asserts that the cure period start is recorded and read back with its length taken from the versioned reference data.
8. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one record for the notice with its decision_code, rule_id and rule_version, and that the rule version is the one the fixture named.
9. Harness: counts one `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` and asserts the central ledger in rwb-decision confirmed the record.
10. Harness: counts one `rwb.comms.NoticeGenerated.v1` and one `rwb.comms.NoticeDispatched.v1` on `rwb.comms.events.v1`, asserts each was consumed once by the consumer the event catalogue names, replays each event once, and asserts nothing changed.
11. Harness: forces the local decision-record library to fail for the notice and asserts the notice stops with MSG-P7-003, no notice and no decision entry are written, and the partner and the instruction are unchanged when they are read again.
12. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller holding Partner portal R and not C, then attempts the notice write and asserts 403 with MSG-P4-002 and no state change.
13. Harness: writes one run report per case and partner, keyed by story, caseId and partner_code, naming the contract version of each hop, whether the hop was a stub or the owner, the score and the target with the rule version, the notice with its type and sent date, the cure period start and its length and version, the decision record, the two notice events with their consumer effects, and the pass or fail gate.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no further step is marked evidenced | None | TC-E7-014-01-ITG (ITG AC2) | AC2 |
| X2 | The partner read returns a score and no target of the named rule version to compare it with | The run fails on AC2 and the report names the partner, the rule version and the missing target; a miss is never declared from a target held in the code | None | TC-E7-014-01-ITG (ITG AC2) | AC2 |
| X3 | The notice write answers 201 and the notice read-back returns a different notice | The run fails on AC2 and the report names the two answers field by field and the contract version of each hop | None | TC-E7-014-01-ITG (ITG AC2) | AC2 |
| X4 | The cure period start is recorded with a length that is not the versioned reference value | The run fails on AC2 and the report names the length recorded, the length in force and its version; the length is never a value in the harness | None | TC-E7-014-01-ITG (ITG AC2) | AC2 |
| X5 | A notice event is published twice, or consumed twice, or a replay changes state | The run fails on AC3 and the report names the event, the publication count and the consumer effect before and after the replay | None | TC-E7-014-01-ITG (ITG AC3) | AC3 |
| X6 | The decision record fails and the notice still goes out, or a decision entry is written without the ledger confirmation | The run fails on AC4 and the report names the notice state, the notice read-back and the decision log before and after; nothing changes is asserted, not assumed | MSG-P7-003 (expected) | TC-E7-014-02-ITG and TC-E7-014-04-ITG (ITG AC4) | AC4 |
| X7 | A caller holding Partner portal R and not C is allowed to issue a notice | The run fails on AC5 and the report names the caller's rights, the operation and the answer; a 201 is a failure even when no business data changed | MSG-P4-002 (expected, and missing) | TC-E7-014-03-ITG (ITG AC5) | AC5 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S9-E7014-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the stub answer shapes, the evidence shape, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The notice is proved to be issued on a miss with the rule version in the record, the cure period is proved to start from versioned reference data, and a notice that cannot be recorded is proved to change nothing |
| Estimable | One runner, one stub set, one partner probe, one target probe, one notice driver, one decision read-back, one event observer and one report |
| Small | Fits in one sprint with its five criteria and four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S9-E7014-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Issue a notice on a missed target - wave 4 integration harness

  Scenario: AC1 Issue a notice on a missed target (legacy RWB-E7-014 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then sends the contractual notice when a partner misses its targets, and starts the cure period
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The notice is issued on a missed target and the cure period starts (new, D-RCV-60)
    Given the partner read returns the partner with partner_code, partner_type, panel_status, contract_end and score
    And the score and the contractual target of the named rule version show the miss
    When the notice is issued through POST /api/recovery/comms/v1/cases/{caseId}/notices
    Then the answer is 201 and the notice carries notice_type and sent_date
    And GET /api/recovery/comms/v1/notices/{noticeId} returns the same notice
    And the cure period start is recorded and read back
    And the length of the cure period is taken from versioned reference data and never from code

  Scenario: AC3 One decision record and each event once (new, D-RCV-60)
    Given the notice has been issued for the case
    When the decision record and the events are read back
    Then one decision record carries decision_code, rule_id and rule_version
    And "rwb.decision.DecisionRecorded.v1" is published once and confirmed by the central ledger
    And "rwb.comms.NoticeGenerated.v1" is published once and consumed once
    And "rwb.comms.NoticeDispatched.v1" is published once and consumed once
    And a replay of each event changes nothing

  Scenario: AC4 A forced local decision-record failure stops the notice (new, D-RCV-60)
    Given the local decision-record library is forced to fail for the notice
    When the notice is issued through POST /api/recovery/comms/v1/cases/{caseId}/notices
    Then the notice write stops with "MSG-P7-003"
    And no notice and no decision entry are written
    And the partner and the instruction are unchanged when they are read again

  Scenario: AC5 A caller holding Partner portal R and not C is refused (new, D-RCV-60)
    Given a caller whose right set holds Partner portal R and not Partner portal C
    When the caller issues a notice through POST /api/recovery/comms/v1/cases/{caseId}/notices
    Then the answer is 403 with "MSG-P4-002"
    And nothing changes

  Scenario: AC6 Each business rule in section 8 is asserted or recorded as a guardrail (new, D-RCV-60)
    Given the business rules BR1 to BR9 are listed in section 8
    When the run reads the partner, the instruction, the notice and the decision record
    Then each rule is asserted against the data it governs, or is recorded as an architecture constraint in a guardrail or boundary test
    And the harness changes none of the rules

  Scenario: AC7 A consumed call that fails or does not answer stops the notice (new, D-RCV-60)
    Given the partner read or the notice write that this story consumes fails or does not answer
    When the notice is issued through POST /api/recovery/comms/v1/cases/{caseId}/notices
    Then the answer is not 201 and no notice and no decision entry are written
    And the cure period start is not recorded
    And the partner and the instruction are unchanged when they are read again
```

Legacy AC2 (the decision log cannot be written) is built and tested in RWB-S9-E7014-APP, and this story asserts the same failure at the notice write through AC4.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit; the notice on a missed target is the notice and exit point of that set | REQ-S9-001 |
| BR2 | A partner that misses its service level is chased once and then has the work recalled | REQ-S9-005 |
| BR3 | When the partner misses the service level on the portal, the work is chased once, then recalled and re-selected on the scorecard, to PARTNER_RECALLED | R-UNI-25 |
| BR4 | When a conduct or complaint breach is upheld, allocation is suspended, the affected cases are recalled and the breach is reported to the partner review, to PARTNER_RECALLED | R-UNI-29 |
| BR5 | When the time in the current state exceeds the service level, the breach is raised to the named escalation point and the case does not move, to ESCALATED | R-UNI-30 |
| BR6 | When a new rule version reaches its effective date, it applies to decisions taken from that date, and open cases keep the version they were decided under, so the notice carries the rule version in force on its sent date | R-UNI-38 |
| BR7 | When the decision log entry cannot be written, the action is blocked and no action proceeds unlogged, which is MSG-P7-003 on the notice write | R-UNI-39 |
| BR8 | Partner performance, conduct and complaint data are reported to the partner review forum, and the notice is one of the facts reported | REQ-S9-007 |
| BR9 | Every call is one hop on the owner's base with a 2 s budget, and the decision record is written through the local decision-record library on the shared topic and confirmed by the central ledger | DP-11, DP-13, DP-03; ADR-020, ADR-022 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E7014-APP and P6 rwb-comms, and the contractual target and the length of the cure period are the versioned reference data of FEAT-PRM-02 that the run reads and never writes. The reference data the run reads (the rule version, the contractual target and the cure period length) is read under the reference-data contract (DP-06, DP-07) and never written.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No notice | `NoticeGenerated` on `rwb.comms.events.v1` | the notice is issued on a missed target and the cure period starts | Notice record raised, cure period running |
| Notice raised | `NoticeDispatched` on `rwb.comms.events.v1` | the notice leaves by its channel | Notice dispatched |
| Notice dispatched | `NoticeDelivered` on `rwb.comms.events.v1` | the channel confirms delivery | Notice delivered |
| SENT | PARTNER_NO_RESPONSE | the service level is missed and the chase has run once (R-UNI-25) | RECALLED |
| ANY_ACTIVE | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld (R-UNI-29) | RECALLED |
| ANY_ACTIVE | SLA_BREACHED | time in the current state exceeds the service level (R-UNI-30) | ESCALATED |

`NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered` are the events of Arch v5 slide 42 rows 13 to 15; SENT and RECALLED are instruction status values of DF-PRT-014, and PARTNER_NO_RESPONSE, PARTNER_CONDUCT_BREACH and SLA_BREACHED are the event codes of R-UNI-25, R-UNI-29 and R-UNI-30, whose to_state is PARTNER_RECALLED and ESCALATED. No source names a notice status list for the record P6 holds, so the run asserts the notice through its facts — notice_type, sent_date, the template, the dispatch and the delivery events — and asserts no status value for it that the source does not name (GAP-0475; ASM-0667). The cure period is a date fact, not a state the harness sets: the start is recorded by the owning service and the end is counted from the versioned reference length. The harness changes no state at all: P6 rwb-comms owns the notice and NoticeDispatchWorkflow, S9 rwb-partner owns the instruction and the partner, and P3 rwb-case holds the case state the run reads. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-NPAMGR, partner and agency manager | Holds Partner portal C and R; is the role the notice is written for and the role that issues it |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG | Hold Partner portal C per the legacy section; issue the same notice where their scope allows |
| RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and the 21 further roles of the legacy R list | Read the partner and the instructions where their rights allow; the R list of the legacy section names them |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P6 issues the notice, answers the notice read, publishes NoticeGenerated and NoticeDispatched and runs NoticeDispatchWorkflow; S9 answers the partner and instruction reads and writes the decision record; P7 holds the central ledger; P3 holds the case; P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the notice is the manager's, and authorisation is answered by rwb-access and the DoA table of P4 |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 to DF-LEG-023 | notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | Read back through the rwb-comms contract; the write is P6's |
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end, score | Read through the rwb-partner contract |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status | Read through the rwb-partner contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | case_id, decision_code, rule_id, rule_version, model_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code | Read through the rwb-decision contract |

Field IDs are those the legacy section names and the Logical Data Model and Data Dictionary v9 holds. The notice is P6's, the partner and its instructions are S9's, the decision log and the rule rows are P7's, and the case behind the instruction is P3's; the harness reads them only through those contracts and never from a schema. The contractual target and the length of the cure period are the versioned reference data of FEAT-PRM-02, read as data and never written by the harness. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The partner, with partner_code, partner_type, panel_status, contract_end and score (AC1, AC2, AC4) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instructions on the case, with their case, type, due time and status (AC1, AC2, AC4) |
| POST | `/api/recovery/comms/v1/cases/{caseId}/notices` | P6 rwb-comms | Issues the notice from the approved template the fixture names (AC1, AC2, AC4, AC5) |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | Reads the notice back with its notice_type and sent_date (AC2, AC4) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of the notice, with its decision code and rule version (AC1, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case before and after the notice, and the consumer effect of the events (AC3, AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a read or a write (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19). The Ownership Map publishes no notice-on-a-missed-target operation and no cure-period read of its own, so the notice is not called through an operation of its own here: it is asserted through the P6 notice write and read-back, the partner and instruction reads, and the decision log, which is what the manager's screen would read after the action.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` | `rwb.comms.events.v1` | P6 rwb-comms | Counts one publication per notice and proves the notice is generated from the approved template before it is dispatched (AC2, AC3) |
| `rwb.comms.NoticeDispatched.v1` | `rwb.comms.events.v1` | P6 rwb-comms | Counts one publication per notice and asserts the consumer effect once, with the replay proving one processed row per consumer (AC3) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | The owning service through the local decision-record library (DP-03) | Proves the decision record of the notice was published with its rule version and confirmed by the central ledger, and stays one record after a replay (AC3, AC4) |

The harness subscribes to both topics under one consumer group of its own, counts publications and replays each event once. `rwb.comms.NoticeGenerated.v1` is consumed by rwb-decision and `rwb.comms.NoticeDispatched.v1` by rwb-reporting, per the event catalogue of Arch v5 slide 42 rows 13 and 14, so those are the consumer effects the run counts; `rwb.decision.DecisionRecorded.v1` is consumed by rwb-decision and rwb-reporting per slide 42 row 08. The consumer effect that has a published operation in this story is the case through the rwb-case read of §12.2; where a consumer exposes no operation here, its inbox row count comes from the consumer evidence in the run fixture. `rwb.comms.NoticeDelivered.v1` is out of the harness's scope: delivery happens after the notice leaves the service, and the harness asserts the notice to the dispatch and no further.

#### 12.5 Workflows and activities

None added. The harness observes two workflows and builds neither. NoticeDispatchWorkflow, P6's kit-template workflow on the task queue `rwb-comms` in the `rwb-recovery` namespace, takes the generated notice, generates the letter through rwb-document, takes the approval child on rwb-decision and hands the file to rwb-integration; the activities it observes are that document and integration hand-off as named on Arch v5 slide 17. InstructionWorkflow, S9's workflow on the task queue `rwb-partner`, holds the SLA timer per partner type that turns a missed service level into a chase and then a recall, with the activities `issueInstruction` and `recordResult`; the harness observes it because the notice is about a partner whose instruction is on that clock. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. NoticeDispatchWorkflow is started by the notice event and InstructionWorkflow is started by the instruction and held by its own SLA timer, so the harness starts nothing by cron and sets no overlap policy or catch-up window. JOB-10, the 16:00 WIN notices run owned by rwb-comms with rwb-integration, is the owner's schedule and not this story's.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); notice and template are P6's, partner and partner_instruction are S9's, decision_log_entry and rule_row are P7's, the reference data rows are P3's under the default ruling, and recovery_case is P3's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (partner read) | `GET /partners` | The synthetic partner with partner_code, partner_type, panel_status, contract_end and the score the fixture names (GAP-0475; ASM-0667) |
| Stub for rwb-partner (instruction read) | `GET /partner/instructions` | The one synthetic instruction on the case, with its case_id, partner_id, instruction_type, instructed_at, due_at and status; the keys are the fixture's (GAP-0475; ASM-0667) |
| Stub for rwb-comms (notice write) | `POST /cases/{caseId}/notices` | Accepts the notice for the notice type and template the fixture names, answers 201 with the notice carrying notice_type and sent_date, and answers 403 with MSG-P4-002 for a caller holding R and not C (GAP-0475; ASM-0667) |
| Stub for rwb-comms (notice read) | `GET /notices/{noticeId}` | Returns the same notice the write answered, field for field, including the cure period start (GAP-0475; ASM-0667) |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One record for the notice with its decision_code, rule_id, rule_version and the central ledger confirmation (GAP-0475; ASM-0667) |
| Stub for rwb-case | `GET /cases/{caseId}` | The case with its state unchanged across the notice and the forced failure (GAP-0475; ASM-0667) |
| Stub for rwb-access | `GET /me/session` | Allows RW-NPAMGR with Partner portal C and R; refuses a caller holding R and not C with 403 and MSG-P4-002 (GAP-0475; ASM-0667) |
| Fixture for the missed target and the cure period | The named rule version, its contractual target, the score and the versioned cure period length | The partner score, the contractual target of the named rule version, the notice type, the approved template and the cure period length with its version, held as fixture data (GAP-0475; ASM-0667) |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic partner, instruction, case and notice keys, the stub answer shapes, the conduct of the missed-target comparison against the named rule version, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0475; ASM-0667).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; three consumed, `rwb.comms.NoticeGenerated.v1`, `rwb.comms.NoticeDispatched.v1` and `rwb.decision.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; NoticeDispatchWorkflow on `rwb-comms` and InstructionWorkflow on `rwb-partner` observed, with their timers and activities |
| File | None. The notice letter is generated and delivered on P6's own contract and workflow, and the run holds no file of its own |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies the table adds, RWB-PLT-E1027-CON for DP-03 and RWB-PLT-N001-CON for DP-19, are platform contract stories delivered in the platform wave, are recorded here and are not repeated in the metadata H field of this story, which stays None; DP-13 adds none. The only blocking dependency is the I story RWB-S9-E7014-APP, which replaces its stub as it lands and never blocks the lane.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeRunner | Job | Runs the five owned criteria in order for a case and partner and holds the run lock |
| PartnerProbe | Service | Reads the partner with partner_code, partner_type, panel_status, contract_end and score from S9 |
| TargetProbe | Service | Compares the score with the contractual target of the rule version the fixture names and records the miss with the version beside it |
| NoticeDriver | Service | Issues the notice through P6 from the approved template, reads it back through P6, and reads the cure period start and its versioned length |
| DecisionReadBack | Service | Reads the decision log through P7 and asserts one record with its decision code, rule id and rule version, and the ledger confirmation |
| EventObserver | Service | Subscribes to `rwb.comms.events.v1` and `rwb.decision-record.v1`, counts publications and consumptions, and replays each event once |
| StubSet | Fake | The eight stubs and the fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per case and partner keyed by story, caseId and partner_code, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S9-E7014-APP lands, on the synthetic partner, instruction, case and notice keys held as fixture data, with the rule version, the contractual target, the score, the notice type and the cure period length named by the fixture and never by the code. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the stub answer shapes, the conduct of the missed-target comparison, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0475; ASM-0667).

**Build steps**

1. Generate the eight stubs and the missed-target fixture from the published contracts, pin each contract version in the run report, and fail the run on a mismatch (X1).
2. Build the PartnerProbe and prove the partner read answers partner_code, partner_type, panel_status, contract_end and score, and the instruction read answers the instruction on the case (AC2).
3. Build the TargetProbe: compare the score with the contractual target of the named rule version, record the miss with the version, and fail the run where the target is missing or taken from the code (AC2, X2).
4. Build the NoticeDriver for the write and the read-back, and prove 201 with notice_type and sent_date and the same notice returned, field for field (AC2, X3).
5. Prove the cure period start is recorded and read back with the length of the versioned reference data and its version, and fail the run where the length differs (AC2, X4).
6. Add the DecisionReadBack for AC1 and AC3: one record with decision_code, rule_id and rule_version, and the ledger confirmation before the notice is reported as recorded.
7. Add the EventObserver for AC3: one publication and one consumption of each notice event, one `DecisionRecorded` confirmed by the ledger, the case effect once, and a replay of each event that changes nothing (X5).
8. Add the forced decision-record failure for AC4 through the notice read-back, the decision log, the partner read and the instruction read before and after, so nothing changes is asserted and not assumed (X6).
9. Add the session read and the refused notice write for AC5, then the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S9-E7014-APP lands (X7).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S9-E7014-APP when it lands, and the wave entry check holds a run report keyed by story, caseId and partner_code, with the rule version, the target, the notice and the cure period cited from the fixture and the data.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. The legacy section carries these three messages for the feature and no P6-specific or S9-specific message, so none is invented here: MSG-GEN-001 with the missing field when the notice write is made short of a required value such as the notice type or the template, MSG-P4-002 with the refused action on the notice write, and MSG-P7-003 when the decision record cannot be written and the notice does not go out.

### 15. Screens and states

The harness renders no screen: it observes the owners' operations and writes a report. The legacy section names SCR-34 Partner list and SCR-35 Placement and allocation, which belong to S9 and its CON story; the harness neither builds nor reads them, and it asserts their data through the partner read, the instruction read and the notice read-back.

| State | Read through | What the run asserts |
|---|---|---|
| ACTIVE, ON_NOTICE, SUSPENDED, EXITED (panel status) | rwb-partner partner read | The panel classification of the partner at the time of the notice (DF-PRT-005) |
| SENT, ACCEPTED, IN_PROGRESS, DONE, DECLINED, RECALLED (instruction status) | rwb-partner instruction read | The status of the instruction before and after the notice, and that a refused or failed notice leaves it unchanged (DF-PRT-014) |
| The notice record | rwb-comms notice read | The same notice the write answered, with its notice_type, sent_date and barcode, and no status value the source does not name (DF-LEG-015 to DF-LEG-023) |
| The cure period | rwb-comms notice read and the versioned reference data | The start is recorded and read back, and its length is the versioned reference value with its version (FEAT-PRM-02) |
| The decision record of the notice | rwb-decision decision log | One record with its decision code, rule id and rule version, confirmed by the central ledger |
| The case state | rwb-case case read | The case is unchanged by the notice and by the forced failure |
| PARTNER_RECALLED, ESCALATED | the rule rows and the instruction read | The recall and conduct context the notice sits in, recorded by S9 and never set by the harness |
| SCR-34 empty, loading, error, no access | Not specified in the source documents (CG-ALL-1214) | Not specified in the source documents (CG-ALL-1214) |
| SCR-35 empty, loading, error, no access | Not specified in the source documents (CG-ALL-1215) | Not specified in the source documents (CG-ALL-1215) |

The environment, layout and retention of the run report are Not specified in the source documents (GAP-0475; ASM-0667). The SIT base hosts, fixture layout and keys, stub answer shapes, missed-target comparison, evidence format and retention, and pass or fail gate are agreed by the integration lead at the wave 4 entry check and recorded in the harness README; no business value is hard-coded.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-014-01-ITG | AC1 (legacy); ITG AC1 | End to end | One partner on the panel with a score below the target of the named rule version, one instruction on one case, the notice and the decision record live |
| TC-E7-014-02-ITG | Legacy AC2 not recorded stays with RWB-S9-E7014-APP; ITG AC4 | Integration | The decision-record library forced to fail on the notice write |
| TC-E7-014-03-ITG | Access; ITG AC5 | Component | A caller holding Partner portal R and not C |
| TC-E7-014-04-ITG | Principle 5; ITG AC4 | Integration | A forced decision-record failure with the notice, partner and instruction reads before and after |
| TC-E7-014-05-ITG | ITG AC3 | Integration | A notice issued for one case, read back with its decision record and its events |
| TC-E7-014-06-ITG | ITG AC6; section 8 BR1 to BR9 | Not specified in the source documents (NEWAC-RWB-ITG-E7014-ITG-AC6) | Not specified in the source documents (NEWAC-RWB-ITG-E7014-ITG-AC6) |
| TC-E7-014-07-ITG | ITG AC7 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E7014-ITG-AC7) |

The Covers column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. Legacy AC2, the forced decision-log failure, stays with RWB-S9-E7014-APP and is asserted here at the notice write through AC4.

### 17. Guardrails

- No business value in code: the rule version, the contractual target, the score, the notice type, the approved template, the cure period length and its version, the synthetic keys and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- ACE data only through the owner's contract or `v_ace_*` views: this run reads no ACE data at all, and the partner, instruction, notice, decision and case rows are read only through their owners' contracts (DP-01).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The notice is asserted from the owner's answer and never from a narrative, and no status value is asserted for it that no source names.
- The cure period length is read from versioned reference data and never counted in the harness, and a new rule version is never applied to a case decided under an earlier one (R-UNI-38).
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-014 Issue a notice on a missed target | Recovery Workbench User Stories Epics 3 to 8 v4, lines 12636 to 12714 | Sections 1, 3, 10, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 12655 to 12659 | Section 7, AC1, marked (legacy RWB-E7-014 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E7-014-02 | The same, lines 12661 to 12664 and 12710 | AC4 asserts the same failure here; the legacy AC stays with RWB-S9-E7014-APP (section 19) |
| Legacy test cases TC-E7-014-01 to TC-E7-014-04 | The same, lines 12709 to 12712 | Copied as -ITG in section 16 |
| Legacy endpoints and the Partner portal rights | The same, lines 12676 to 12695 | Sections 10 and 12.2: the legacy paths sit under `/api/recovery/v1` and the target paths under `/api/recovery/<short>/v1` (DP-13) |
| FEAT-PRM-11 Issue a notice on a missed target | Epics 3 to 8 Specification v3, line 144 | Sections 1, 2 and 3 |
| FEAT-PRM-08 Score partners monthly | Epics 3 to 8 Specification v3, line 141 | Sections 2, 3 and 19: the score is read, the scorecard is not built here |
| FEAT-PRM-02 Hold the partner panel and fee schedule as data | Epics 3 to 8 Specification v3, line 135 | Sections 2, 3 and 15: the target and the cure period length are versioned reference data |
| REQ-S9-001, REQ-S9-005 and REQ-S9-007 | Business Requirements Program v5, lines 430, 434 and 436 | Section 8, BR1, BR2 and BR8; section 7, AC2 |
| R-UNI-25, R-UNI-29, R-UNI-30, R-UNI-38 and R-UNI-39 | Business Rules and Routing Logic v4, lines 429, 433, 434, 442 and 443 | Sections 2, 8 and 9 |
| P6 rwb-comms contract, the notice operations and NoticeDispatchWorkflow | Architecture v5 slide 17; slide 41 | Sections 2, 12.2, 12.4 and 12.5 |
| NoticeGenerated, NoticeDispatched, NoticeDelivered and DecisionRecorded | Architecture v5 slide 42 rows 13, 14, 15 and 08 | Sections 12.4 and 9 |
| gateway-bff and the composite route of a screen | Architecture v5 slide 20 | Sections 2 and 13, DP-19 |
| CaseWorkflow with a child per stage and the four steps of every workflow | Architecture v5 slide 25; Temporal and Drools design slide 13 | Sections 9 and 12.5 |
| S9 partner journey and the partner SLA timers | Temporal and Drools design slide 25 | Sections 2 and 12.5 |
| The point of no return and the ledger confirmation in strict mode | Temporal and Drools design slide 26 | Sections 2 and 12.5 |
| The overnight chain and JOB-10 WIN notices | Architecture v5 slide 31; slide 44 | Section 12.6 |
| DF-LEG-015 to DF-LEG-023, DF-PRT-001 to DF-PRT-007, DF-PRT-008 to DF-PRT-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 8 and 12: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |

### 19. Out of scope

- RWB-S9-E7014-CON and RWB-S9-E7014-APP: the build of the notice on a missed target, its screen, its cure period action and its data in S9.
- The P6 rwb-comms build: the notice record, the templates and merge fields, the proof of delivery, NoticeDispatchWorkflow and the dispatch to rwb-integration, which are P6's own stories.
- Legacy AC2, the decision-log failure as a product behaviour of the feature, which is built and tested in RWB-S9-E7014-APP.
- The monthly scorecard (FEAT-PRM-08) and the calculation of the score; this story reads the score of DF-PRT-007 and nothing else.
- The partner panel, fee schedule and service level reference data (FEAT-PRM-02) and the contractual target and cure period values; this story reads them as versioned data.
- The recall and re-selection work of R-UNI-25, R-UNI-29 and R-UNI-30 as products: the harness asserts the context, it does not build the recall.
- The partner gateway and FAPI 2.0: partner users reach the portal through the DMZ gateway, which is the edge stories' own scope.
- NoticeDelivered, the delivery confirmation, and the WIN letters run JOB-10, which are P6's and the integration schedule's own scope.
- Platform deployment and configuration, and the platform H dependencies named in section 13.
- Any production change: the harness runs in the test environment only.
