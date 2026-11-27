# RWB-ITG-E5009-ITG Instruct the firm through the portal

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E5009-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W3 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S4-E5009-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E5-009 for the wave 3 integration harness; the instruction is S9's, the case move is S4's, the pack is P5's and its serving fact P6's, and the partner clock is P3's. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E5009-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a member of the integration and QA team, I want **one repeatable cross-service harness that takes a seeded case whose pack is approved and whose firm is either selected by rule or nominated, drives the instruction through rwb-partner, and proves that the firm is served the instruction and the pack the case holds, that the case reaches FIRM_INSTRUCTED by its own owner, that the partner clock is running on the case with the dates the owner wrote, and that the decision record was written with the rule version before any of it was visible to the firm**, so that **every instruction to a law firm is shown to be one hop from a case that holds a complete pack, to exist once per case, to be on record before the portal serves it, and to be timed by the case and not by the caller, so no instruction reaches a firm without a record and no service level is measured on a clock somebody set by hand**.

### 2. Business rationale

A firm instructed without a pack is a firm that cannot file, and the delay is a legal delay. A firm instructed without a record cannot be shown to have been instructed at all when the instruction is later disputed, and the service level it is measured against cannot be defended. A partner clock started by the caller is worse than no clock: it reports an SLA on a start time nobody authorised. All three sit on one chain. The legal action and the case state are S4 rwb-litigation's, which owns legal actions, hearings, judgments, enforcement and the LED auction ladder in `rwb_litigation` and evaluates the panel rule that matches or nominates the firm (R-LIT-23; R-LIT-24; R-LIT-26). The pack and its checklist are P5 rwb-document's, which owns metadata, custody, OCR text and fields, signatures and retention in `rwb_document`, and the serving fact belongs to P6 rwb-comms, which owns notices, templates, merge fields and proof of delivery in `rwb_comms`. The instruction, its acceptance window and the result are S9 rwb-partner's, which owns the panel, partner users, instructions, results, fees and scorecards in `rwb_partner` (REQ-S4-004; REQ-S9-008). The case, its timer and its history are P3 rwb-case's, and the record that cites the rule and its version is written with the change and reaches the ledger through `rwb.decision-record.v1` (REQ-DRI-001; REQ-DRI-005).

This story owns the harness that proves that chain as the legacy key describes it, carrying AC1 of RWB-E5-009 into evidence. The legacy key ran the whole step inside the litigation module: one component issued the instruction, sent the pack, started the partner clock and wrote the record. In the target those are four owners, and the harness exists to prove they still act as one step. It serves REQ-S4-004 read with REQ-S4-002 on the pack and REQ-S9-008 on the portal, and it carries FEAT-LIT-09 into evidence, with REQ-DRI-001 and REQ-DRI-005 read on the record before the effect.

The harness is decoupled the same way the services are. It owns no schema and reads no other service's table (DP-01): `partner` and `partner_instruction` are S9's tables, so the harness reads them through rwb-partner's contract and never as tables; `legal_action` is S4's; `document` and `case_document_check` are P5's; `recovery_case` and `timer` are P3's; `decision_log_entry` and `rule_row` are P7's. It reads the record from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). Every call is one hop on the owner's base `/api/recovery/<short>/v1`, with a 2 s timeout and a circuit breaker per downstream, which is the base the target names and not the monolith base (DP-13). Where a screen would compose those calls, the harness calls the gateway-bff composite route, and where a partner would, it calls the partner gateway's surface on rwb-partner (DP-19).

### 3. Preconditions

- The published contracts of rwb-litigation, rwb-partner, rwb-document, rwb-comms, rwb-case, rwb-decision and rwb-access are in the contract registry, and a stub set is generated from each published OpenAPI or AsyncAPI document with its version pinned.
- A case sits at FIRM_SELECTION with an approved pack, and a second case sits at FIRM_ESCALATED with a firm nominated by the Head of Litigation. Both are seeded through the owning services' published operations only. The seeding set, the harness environment specification and the fixture contents are not specified in the source documents (GAP-0435; ASM-0613).
- The pack and its checklist are read from P5 rwb-document only, and the harness holds no copy of a document, a checklist row or a custody record.
- The instruction operation and its request and response fields are read from the published S9 contract. The field names of the instruction request, the field that carries the pack reference and the payload of the result path are not specified in the source documents (GAP-0435; ASM-0613).
- The panel firm read from rwb-partner carries the court region and case type it covers and the outcome of its conflict check, which R-LIT-24 conditions the instruction on. Where those two values live on `partner`, and whether the conflict check is a field or a result of its own, are not specified in the source documents (GAP-0435; ASM-0613).
- The rule package in force carries R-LIT-24, R-LIT-26, R-UNI-39, R-UNI-40 and R-UNI-45, and the version of each rule is readable on the decision record that cites it.
- The partner clock is the case timer that P3 rwb-case holds, and the harness reads it through the rwb-case contract. Which timer type the partner clock is, which date it expires from, and whether S9's own SLA timer or P3's case timer is the partner clock, are not specified in the source documents (GAP-0435; ASM-0614).
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for the roles that hold Litigation C and Litigation R, and for a caller whose role does not include the right.
- No build dependency and no contract dependency. Day 1, with the fakes of section 12.8 in place from the first run, and the rwb-litigation fake replaced by the real service when RWB-S4-E5009-APP lands.

### 4. Flow

1. Harness: seeds the case at FIRM_SELECTION with its approved pack, and the second case at FIRM_ESCALATED with its nominated firm, through the owning services' published operations only. The seeding set and its environment are not specified in the source documents (GAP-0435; ASM-0613).
2. Harness: reads the legal action through `GET /api/recovery/litigation/v1/legal-actions/{legalActionId}` and pins the action type, the law firm the action names and its state, so every assertion is made against the owner's data and not against a value in the script (REQ-S4-004).
3. Harness: reads the pack that belongs to the case through `GET /api/recovery/document/v1/cases/{caseId}/documents` and its completeness through `GET /api/recovery/document/v1/cases/{caseId}/document-checklist`, then reads the serving fact through `GET /api/recovery/comms/v1/notices/{noticeId}` where a notice or message serves it, and asserts the pack the run issues is the one the case holds (REQ-S4-002). The pack is P5's, its serving fact P6's, and the harness holds no copy of either.
4. Harness: reads the panel firm through `GET /api/recovery/partner/v1/partners` and asserts that it covers the court region and case type and carries no failed conflict check, which R-LIT-24 conditions the instruction on. The fields that carry both values are not specified in the source documents (GAP-0435; ASM-0613).
5. Harness: drives the instruction with `POST /api/recovery/partner/v1/cases/{caseId}/instructions`, one hop with a 2 s timeout, so the instruction is placed by the service that owns it and not by the harness. In production the same step is the `issueInstruction` activity on queue rwb-partner, inside InstructionWorkflow, which writes `rwb_partner` and its outbox in one transaction.
6. Harness: reads the instruction back through `GET /api/recovery/partner/v1/partner/instructions` as the firm's own surface, and asserts exactly one instruction for the case, that it names the partner the legal action names, and that the pack it carries is the pack read in step 3. `partner` and `partner_instruction` are S9's tables and are read here through S9's contract only.
7. Harness: exercises the result path once with `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results`, only so the run proves the instruction the portal serves is the case's own. The result itself is S9's work and is not asserted here.
8. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}` and asserts that it reached FIRM_INSTRUCTED by its owner, and reads `rwb.case.CaseStateChanged.v1` on `rwb.case.events.v1` to prove the move happened once and in that order.
9. Harness: reads the partner clock with `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts one running timer whose `started_at` is the moment the owner issued the instruction and whose `expires_at` is the date the owner recorded, per DF-WRK-027 to DF-WRK-036. The clock itself is the durable timer in CaseWorkflow on queue rwb-case; the harness sets no timer, no date and no state. The timer type of the partner clock is not specified in the source documents (GAP-0435; ASM-0614).
10. Harness: asserts the record came first: exactly one entry in `GET /api/recovery/decision/v1/decision-log` for the instruction, carrying R-LIT-24 (or R-LIT-26 on the escalated case) with its rule version, and asserts the entry's time is not later than the instruction's `instructed_at`.
11. Harness: repeats steps 2 to 10 for the case at FIRM_ESCALATED, on the R-LIT-26 path, where the Head of Litigation nominates a firm or widens the panel, and asserts the same instruction, the same case move and the same clock read.
12. Harness: re-drives the instruction with the same key and asserts that the second call is ignored: one instruction, one `InstructionIssued` fact, one timer and one record, with the idempotency hit recorded (R-UNI-40).
13. Harness: forces the decision record to fail and asserts that nothing moves: no instruction, no `InstructionIssued` fact, no case change and no partner clock, and the message the owner returns. This is the negative path of AC4, whose criterion belongs to RWB-S4-E5009-APP.
14. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a role that does not include Litigation C.
15. Harness: publishes one evidence report per story and business date, naming the criterion, the assertions, the contract versions and whether each hop was a stub or the owner. The evidence format and its retention are not specified in the source documents (GAP-0435; ASM-0617).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC1 |
| X2 | The pack read from rwb-document is incomplete against its checklist, or the checklist names a missing document type | The run fails on AC1 and the report names the checklist version and the missing types | MSG-S4-001 | AC1 |
| X3 | The panel firm read from rwb-partner covers no court region or case type for the case, or carries a failed conflict check | The run fails on AC1 and the report names the firm and the value it failed on | None | AC1 |
| X4 | The instruction is issued but no `InstructionIssued` fact arrives on `rwb.partner.events.v1` | The run fails on AC6 and the report names the instruction and the wait | None | TC-E5-009-01-ITG |
| X5 | The portal surface returns no instruction for the firm, or two instructions for one case | The run fails on AC2 and the report names the instructions it found | None | AC2 |
| X6 | The case does not reach FIRM_INSTRUCTED, or reaches it without the instruction | The run fails on AC1 and the report names the state, the event and the instruction | None | AC1 |
| X7 | No partner clock is running on the case, or its `started_at` and `expires_at` are not the owner's values, or the harness finds a clock it wrote itself | The run fails on AC3 and the report names the timers it found and their source | None | AC3 |
| X8 | More than one record exists for the instruction, its rule ID or rule version is missing, or it is later than `instructed_at` | The run fails on AC4 and the report names the records and their times | None | AC4 |
| X9 | The record does not reach `rwb.decision-record.v1` inside 5 minutes | The run fails on AC1 and the report names the record and its arrival time | None | AC1 |
| X10 | The decision record is forced to fail but an instruction, a case move or a partner clock still moves | The run fails on the negative path and the report names what moved | MSG-P7-003 | AC2 path, BR5 |
| X11 | A role that does not include Litigation C is authorised, or a caller outside the case scope passes | The run fails on the access check and the report names the operation | MSG-P4-002 | TC-E5-009-05-ITG |
| X12 | The re-driven instruction with the same key creates a second instruction, a second clock or a second record | The run fails on the idempotency assertion and the report names both calls | None | TC-E5-009-01-ITG, BR6 |
| X13 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC1 |

The report text is for the wave entry check and is not part of the message standard. R-LIT-24, R-LIT-26, R-UNI-39, R-UNI-40 and R-UNI-45 carry no message ID in the rule set, so the harness asserts the instruction, the case state, the clock and the decision record, and names a message ID only where an owning service returns one of those in section 14.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only wait is one I story, RWB-S4-E5009-APP |
| Negotiable | The seeding set, the pack fixture, the report shape and the composite route are configuration agreed at the wave entry check, not business values in code |
| Valuable | The instruction, its pack, its record and its clock are proven end to end before wave 3 opens |
| Estimable | One harness runner, one stub set, one event probe, one clock probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against its fakes and again against the real owner as RWB-S4-E5009-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Instruct the firm through the portal

  Background:
    Given the seeded case carries an approved pack and a firm selected by rule or nominated
    And the contract fakes of section 12.8 are published with their versions pinned

  Scenario: AC1 Instruct the firm through the portal (legacy RWB-E5-009 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the instruction and the pack to the firm and starts the partner clock
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 One hop and one instruction per case (new, D-RCV-60)
    Given the harness is pointed at the rwb-partner contract fake with its version pinned
    When it drives the instruction for the seeded case
    Then exactly one call is made to the owner's instruction operation with a 2 s timeout
    And exactly one instruction and one InstructionIssued fact exist for the case

  Scenario: AC3 The partner clock is read and not set (new, D-RCV-60)
    Given the case reached FIRM_INSTRUCTED by its owner
    When the harness reads the timers of the case
    Then it finds one running timer whose started_at and expires_at the owner wrote
    And the harness has set no timer, no date and no case state

  Scenario: AC4 The record before the effect (new, D-RCV-60)
    Given the decision record is forced to fail
    When the harness drives the instruction
    Then nothing moves: no instruction, no case move and no partner clock
    And the run reports the message the owner returned

  Scenario: AC5 The refusal is proven (new, D-RCV-60)
    Given a caller whose role does not include Litigation C
    When the harness drives the instruction through the owner's contract
    Then the owner refuses with MSG-P4-002
    And the run reports no instruction, no case move and no clock change

  Scenario: AC6 The evidence report (new, D-RCV-60)
    Given the run has finished
    When the evidence report is written
    Then it names the story, the business date, the criterion and each hop with its contract version
    And it states whether the hop was a stub or the owner, what the firm was served, how the case moved and which clock was read
    And it holds the pass or fail gate
```

AC2 and AC3 of the legacy key, the two rule paths R-LIT-24 and R-LIT-26, and AC4, "Not recorded", are owned by RWB-S4-E5009-APP and are not restated here; this story exercises the refusal in AC4's negative path in step 13 of section 4 and in TC-E5-009-04-ITG, and cites both rule paths as the evidence the harness reads.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The instruction with the pack is issued through the partner portal when the panel firm covers the court region and case type and passes the conflict check | R-LIT-24; REQ-S4-004 |
| BR2 | The same instruction is issued when the Head of Litigation nominates a firm or widens the panel on an escalated selection | R-LIT-26; REQ-S4-004 |
| BR3 | The pack is assembled and checked against the document checklist, and the pack the firm is served is the pack the case holds | REQ-S4-002; FEAT-LIT-09 |
| BR4 | Partners exchange data through the partner portal and the external gateway, not by email | REQ-S9-008 |
| BR5 | No instruction, no case move and no partner clock proceeds if the decision record cannot be written | REQ-DRI-005; R-UNI-39 |
| BR6 | A repeat of the same event with the same key is ignored and the idempotency hit is recorded | R-UNI-40 |
| BR7 | On a re-selection the instruction is re-issued and the partner clock restarted | R-UNI-45 |

The instruction and the pack travel together in the sources but are not stored together: the pack is P5's and the instruction S9's, and the field that links them is not named by any source read. The harness asserts the link through both owners' contracts and writes neither.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| FIRM_SELECTION | FIRM_MATCHED | the panel firm covers the court region and case type and passes the conflict check | FIRM_INSTRUCTED (R-LIT-24), with the instruction and the pack issued through the portal and the partner clock started |
| FIRM_ESCALATED | FIRM_NOMINATED | the Head of Litigation nominates a firm or widens the panel | FIRM_INSTRUCTED (R-LIT-26), with the same instruction and the same clock |

These are the owner's states and the owner's moves: rwb-litigation holds the legal action and the state, and rwb-case holds the case and the timer that times the instruction. The harness changes none of them. It seeds through the owning services' published operations, drives the instruction through the rwb-partner contract, and then asserts the state the owner reached and the clock the owner started, naming the owner and the operation behind each move in the report. A case state set, or a clock started, by the harness would prove nothing at all.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, RW-ENFORCE, and the roles that hold Litigation C | Drive the instruction for their case and read the pack, the legal action, the instruction and the record through the owning contracts |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and the further roles that hold Litigation R | Read the same run evidence, including the pack, the instruction, the partner clock and the decision record |
| Head of Litigation | Nominates a firm or widens the panel on the escalated path in production; the harness only reads the result of that nomination |
| QA lead | Owns the harness configuration, the seeding set, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-litigation, rwb-partner, rwb-document, rwb-comms, rwb-case, rwb-decision and rwb-access make every change the harness asserts |
| No approval level from the delegation of authority applies to the harness | The harness takes no business decision; the selection and the nomination belong to the litigation story and to the roles above |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code | Read, through the rwb-case contract, `GET /cases/{caseId}` (P3's `rwb_case`) |
| DF-WRK-027 to DF-WRK-036 | timer | id, case_id, task_id, timer_type, started_at, expires_at, status | Read, through the rwb-case contract, `GET /cases/{caseId}/timers`; the clock itself is the durable timer in CaseWorkflow (P3's `rwb_case`) |
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end | Read, through the rwb-partner contract, `GET /partners` (S9's `rwb_partner`) |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status | Read, through the rwb-partner contract, `POST /cases/{caseId}/instructions` and `GET /partner/instructions` (S9's `rwb_partner`) |
| DF-LEG-001 to DF-LEG-014 | legal_action | id, case_id, law_firm_id, action_type, lit_status, status | Read, through the rwb-litigation contract, `GET /legal-actions/{legalActionId}` (S4's `rwb_litigation`) |
| DF-DOC-001 to DF-DOC-011 | document | id, case_id, document_type, doc_version | Read, through the rwb-document contract, `GET /cases/{caseId}/documents` (P5's `rwb_document`) |
| DF-DOC-036 to DF-DOC-044 | case_document_check | case_id, checklist_version, required_count, present_count, missing_types, complete | Read, through the rwb-document contract, `GET /cases/{caseId}/document-checklist` (P5's `rwb_document`) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract (P7's `rwb_decision`) |
| DF-REF-001 to DF-REF-015 | rule_row | id, rule_id, rule_version, route_set, from_state, event_code | Read, through the rwb-decision contract (P7's `rwb_decision`) |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. `partner` and `partner_instruction` are S9's tables, so the harness reads them through rwb-partner's contract and never as tables (DP-01); `legal_action` is S4's, the two document tables are P5's, `recovery_case` and `timer` are P3's, and the record and the rule rows are P7's. Which field of `partner_instruction` carries the pack reference, which fields of `partner` carry the court region, the case type and the conflict-check outcome, and which `timer_type` the partner clock is, are not specified in the source documents (GAP-0435; ASM-0613; ASM-0614). The harness owns no table and writes no row directly: every read and every seed goes through the API of the owning service.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/partner/v1/cases/{caseId}/instructions` | S9 rwb-partner | Drive the instruction for the case, one hop (AC1) |
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The panel firm, its scope and its conflict-check outcome (AC1, BR1) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instruction as the firm's own surface serves it, read back for the case (AC2) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/results` | S9 rwb-partner | The result path, exercised once so the run proves the portal's instruction is the case's own (AC2) |
| GET | `/api/recovery/litigation/v1/legal-actions/{legalActionId}` | S4 rwb-litigation | The legal action with its pack, instruction, hearings and judgment (AC1) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The pack the case holds (AC1, BR3) |
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` | P5 rwb-document | The pack checklist and its completeness (AC1, BR3) |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | The serving fact, where the pack is served by a notice or message (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state, FIRM_SELECTION, FIRM_ESCALATED or FIRM_INSTRUCTED (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The partner clock, read and never set (AC3) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The record, with the rule ID and the rule version (AC4) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role and scope, including the refusal path (AC5) |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1`, with a 2 s timeout and a circuit breaker per downstream (DP-13). Where a screen would compose them, the harness calls the gateway-bff composite route, and where a partner would, the partner gateway's surface on rwb-partner (DP-19). The instruction operation is the path the Ownership Map and the Epics 3 to 8 Specification give to S9 as `POST /cases/{caseId}/instructions`; its request and response fields, the field that carries the pack reference and the payload of the result path are not named by any source read (GAP-0435; ASM-0613). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it drives the instruction through the rwb-partner contract and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.partner.InstructionIssued.v1` (EV-20) | `rwb.partner.events.v1` | S9 rwb-partner | The instruction exists once for the case, keyed by instructionId, partnerId, type and dueOn (AC2) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | The case reached FIRM_INSTRUCTED, once and after the instruction (AC1) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, through its own local decision-record library | The record written with the instruction reaches the ledger within 5 minutes (AC4, DP-03) |

All three carry IDs and business facts only, keyed by caseId and instructionId, and the harness asserts that no personal data is present. The three events that Architecture v5 slide 19 gives rwb-litigation on `rwb.litigation.events.v1` are LawsuitFiled, JudgmentRecorded and AuctionResult, so no `rwb.litigation.*` fact carries the instruction: the instruction fact is EV-20 on `rwb.partner.events.v1`, and the case move is P3's on `rwb.case.events.v1`. The harness reads the instruction fact from EV-20 on that basis (GAP-0435; ASM-0615).

#### 12.5 Workflows and activities

None added. The harness exercises only: the `issueInstruction` activity inside InstructionWorkflow on queue rwb-partner, which places the instruction and holds S9's own SLA timers; the durable timer in CaseWorkflow on queue rwb-case, which is the partner clock; and the LitigationWorkflow stage child on queue rwb-litigation, which continues as new and requests the instruction. It asserts their effects through the services' contracts and the owners' topics. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. The instruction is triggered by the selection or the nomination and not by a Schedule, and this story sets no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): the legal action is rwb-litigation's, `partner` and `partner_instruction` are rwb-partner's, the pack is rwb-document's, the notice is rwb-comms's, the case and the timer are rwb-case's, the record and the rule rows are rwb-decision's, and the role, scope and DoA data are rwb-access's.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| Stub for rwb-partner | `POST /cases/{caseId}/instructions`, `GET /partners`, `GET /partner/instructions`, `POST /partner/instructions/{instructionId}/results`, `rwb.partner.events.v1` | Day-1 run of AC1, AC2 and AC5 before RWB-S4-E5009-APP is live |
| Stub for rwb-litigation | `GET /legal-actions/{legalActionId}` | Day-1 assertion of the legal action, its firm and its state |
| Stub for rwb-document | `GET /cases/{caseId}/documents`, `GET /cases/{caseId}/document-checklist` | Day-1 assertion of the pack and its checklist |
| Stub for rwb-comms | `GET /notices/{noticeId}` | Day-1 assertion of the serving fact where a notice or message serves the pack |
| Stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | Day-1 assertion of the case state and the partner clock |
| Stub for rwb-decision | `GET /decision-log` | Day-1 assertion of one record for the instruction with its rule version |
| Stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |
| InstructionIssued event stub | `rwb.partner.InstructionIssued.v1` | The instruction fact, where the environment does not run the partner service |
| CaseStateChanged event stub | `rwb.case.CaseStateChanged.v1` | The case move, where the environment does not run the case workflow |

Each fake is generated from the published OpenAPI or AsyncAPI document of its service, and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The instruction's field names, the field that carries the pack reference, the conflict-check value, the timer type of the partner clock, the harness environment, the seeding set and the evidence format are not specified in the source documents (GAP-0435; ASM-0613).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 12 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s timeout and a circuit breaker per downstream, composed through gateway-bff where a screen would and through the partner gateway where a partner would (DP-13, DP-19) |
| Kafka | None published; `rwb.partner.InstructionIssued.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.decision-record.DecisionRecorded.v1` consumed (DP-03) |
| Temporal | Exercised only: `issueInstruction` in InstructionWorkflow on queue rwb-partner, the durable timer in CaseWorkflow on queue rwb-case and the LitigationWorkflow stage child on queue rwb-litigation; none added |
| File | None |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform wave and are not repeated in the metadata H row of this story, which stays None. The blocking dependency is the one I story, RWB-S4-E5009-APP: until it is live the run uses the rwb-litigation stub, and a stub pass is reported as a stub pass.

The decoupling is also the story's reading of the legacy behaviour, and it is the one thing this story adds to the legacy key. The legacy key ran the whole step inside the litigation module: one component sent the instruction and the pack and started the partner clock, then wrote the record. In the target the pack is P5 rwb-document's, with its serving fact P6 rwb-comms's where a notice or message serves it; the instruction, its acceptance window and the result are S9 rwb-partner's through the partner gateway in the DMZ; the panel rule, the legal action and the case move are S4 rwb-litigation's, evaluated in its own embedded rules; and the partner clock is P3 rwb-case's, as a durable timer in CaseWorkflow that survives restarts and upgrades. The harness therefore proves the chain and starts no clock itself: it drives one hop to S9, reads the case and the timer from P3, reads the pack from P5 and the serving fact from P6, and reads the record from P7. That split is recorded as a gap and as assumptions one, two and three, and the owners have not agreed a sequence or a compensation for a partial step (GAP-0435; ASM-0613; ASM-0614).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| InstructionRunner | Job | Runs the owned criterion, the second rule path and the negative path in order for a business date and holds the run lock |
| StubSet | Fake | The seven service stubs and the two event stubs of section 12.8, each generated from the published contract with the version pinned |
| PackProbe | Service | Reads the pack and its checklist from P5 and the serving fact from P6, and asserts that the pack the firm is served is the pack the case holds |
| PartnerProbe | Service | Drives the instruction and the result path through S9, and asserts one instruction per case, the firm it names and the pack it carries |
| ClockProbe | Service | Reads the case state, the case move and the partner clock from P3, and asserts the owner's dates without setting a timer |
| EventProbe | Service | Consumes `rwb.partner.events.v1`, `rwb.case.events.v1` and `rwb.decision-record.v1` and asserts the facts for the case |
| EvidenceReport | Service | Writes the report keyed by story and business date and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, with one case at FIRM_SELECTION carrying an approved pack and a panel firm, and one case at FIRM_ESCALATED carrying a nominated firm. The environment, the seeding set, the pack fixture and the evidence retention are not specified in the source documents (GAP-0435; ASM-0617). Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the seven service stubs and the two event stubs from the published contracts, pin each version in the report and fail the run on a version mismatch (X1, X13).
2. Build the PackProbe to read the pack and its checklist from rwb-document and the serving fact from rwb-comms, and to fail where the pack is incomplete for the business date (X2).
3. Build the PartnerProbe to read the panel firm and assert its court region, case type and conflict-check outcome before the instruction is driven (X3).
4. Build the InstructionRunner for AC1 and AC2: drive one hop to S9, read the instruction back as the firm sees it, and assert one instruction per case naming the partner the legal action names and carrying the pack the case holds (X5).
5. Add the EventProbe for `rwb.partner.InstructionIssued.v1` and `rwb.case.CaseStateChanged.v1`, and assert the instruction fact once and the case move once, in that order (X4, X6).
6. Build the ClockProbe: read the case and its timers from rwb-case and assert the partner clock's `started_at` and `expires_at` against the owner's instruction, with no write of any kind (X7).
7. Assert one record for the instruction through the rwb-decision contract, naming R-LIT-24 or R-LIT-26 and its version, and fail where it is absent, duplicated or later than `instructed_at` (X8).
8. Add the second rule path: rerun steps 3 to 7 for the case at FIRM_ESCALATED on R-LIT-26.
9. Add the idempotency assertion: re-drive the instruction with the same key and assert one instruction, one fact, one timer and one record (X12).
10. Add the negative path: force the decision record to fail, assert that nothing moves and record the message the owner returns (X10).
11. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a role that does not include Litigation C (X11), then add the EvidenceReport and the gate, and swap the rwb-litigation stub for the real service when RWB-S4-E5009-APP lands and rerun the criterion.

**Feature switch.** The legacy key names no feature switch for this behaviour. The harness runs behind the platform feature-flag library as the wave releases it; the flag key is not specified in the source documents (GAP-0435; ASM-0617).

**Done when.** The tests of section 16 pass; the criterion passes against the fakes on Day 1 and again against rwb-litigation when RWB-S4-E5009-APP lands; and the wave entry check holds a report keyed by story and business date with the contract, pack and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for the instruction cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-S4-001 | The pack is missing an item the checklist requires | The pack is missing {item}. Add it before filing. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

R-LIT-24, R-LIT-26, R-UNI-39, R-UNI-40 and R-UNI-45 carry no message ID in the rule set, so the harness asserts the instruction, the case state, the clock and the decision record, and names a message ID only where an owning service returns one of those above. The harness produces none of these messages itself, and MSG-S4-001 is the pack message the legacy key gives; where the owner raises it at the instruction rather than at filing is not stated by any source read (GAP-0435; ASM-0616).

### 15. Screens and states

SCR-19 Litigation workspace is the screen the legacy key names for this behaviour:

| State | What the user sees and does |
|---|---|
| Pack | The pack is assembled and checked against the checklist, and the firm is selected or nominated |
| instructed | The instruction and the pack have gone to the firm through the portal, the case reads FIRM_INSTRUCTED and the partner clock is running |
| filed | The firm has filed and the receipt and the court case number are on the case |
| hearing | Hearings and deadlines are tracked against the case |
| judgment | The judgment is recorded and the enforcement step opens |

The firm sees the same step on its own surface, as the instruction and the pack in the partner portal behind the partner gateway. The harness renders no screen: it reads these states through the rwb-litigation, rwb-partner, rwb-document, rwb-comms, rwb-case and rwb-decision contracts, and it reads the portal surface through rwb-partner, so a passed run means the screen and the portal have the right data behind them. What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0435; ASM-0617).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-009-01-ITG | AC1, AC2, AC3, AC6, BR1, BR3, BR4, BR6 | Integration | Seeded case at FIRM_SELECTION with an approved pack and a panel firm; a second case at FIRM_ESCALATED with a nominated firm |
| TC-E5-009-02-ITG | AC1, AC2, BR1; AC2 (owned by RWB-S4-E5009-APP) | Integration | Case in FIRM_SELECTION with the firm matched by R-LIT-24 |
| TC-E5-009-03-ITG | AC1, AC2, AC3, BR2; AC3 (owned by RWB-S4-E5009-APP) | Integration | Case in FIRM_ESCALATED with the firm nominated by the Head of Litigation, R-LIT-26 |
| TC-E5-009-04-ITG | AC4, BR5; AC4 (owned by RWB-S4-E5009-APP) | Integration | Decision log forced to fail; MSG-P7-003; nothing moves |
| TC-E5-009-05-ITG | AC5 | Component | A role without Litigation C; MSG-P4-002 |
| TC-E5-009-06-ITG | AC4, AC6, Principle 5 | NFR | Forced decision-log write failure; no instruction, no case move, no clock |

These are the ITG copies of TC-E5-009-01 to TC-E5-009-06 and carry the legacy data unchanged, with the component and NFR copies keeping the legacy levels. The full legacy tests, with their Given, When and Then, are in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases, under those IDs.

### 17. Guardrails

- No business value in code: the rule versions, the panel scope, the conflict-check outcome, the pack checklist, the partner clock's dates, the seeding set and the result mappings are data, and the harness holds no copy of any of them.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and business facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01). `partner` and `partner_instruction` are S9's and are read through rwb-partner's contract, never as tables.
- The Workbench holds no copy of the pack, the instruction or the clock: the pack is P5's, the instruction S9's and the timer P3's, and each is read back through its owner's contract.
- The harness never sets a case state, a timer, a date or a decision state by hand; it reads the state the owner reached and the clock the owner started.
- One hop and a 2 s timeout per call, with a circuit breaker per downstream, so the harness fails where a screen or the portal would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sends a document to a firm outside the SIT seed.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S4-004 | A law firm is selected from the panel by rule using panel performance, and instructed through the partner portal | Business Requirements Program v5, section 5.11 | FEAT-LIT-09 | D7 firm selection and instruction | R-LIT-24, R-LIT-26 | TC-E5-009-01-ITG, TC-E5-009-02-ITG, TC-E5-009-03-ITG |
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested | Business Requirements Program v5, section 5.11 | FEAT-LIT-09 | D7 pack assembly | R-LIT-24 | TC-E5-009-01-ITG |
| REQ-S9-008 | Partners exchange data through the partner portal and the external gateway, and not by email | Business Requirements Program v5, section 5.16 | FEAT-LIT-09 | D7 firm instruction | R-LIT-24, R-LIT-26 | TC-E5-009-01-ITG |
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome | Business Requirements Program v5, section 5.7 | FEAT-LIT-09 | D7 firm instruction | R-LIT-24, R-LIT-26 | TC-E5-009-01-ITG, TC-E5-009-02-ITG, TC-E5-009-06-ITG |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program v5, section 5.7 | FEAT-LIT-09 | D7 firm instruction | R-UNI-39 | TC-E5-009-04-ITG, TC-E5-009-06-ITG |

The case states read here, FIRM_SELECTION, FIRM_ESCALATED and FIRM_INSTRUCTED, and the events FIRM_MATCHED and FIRM_NOMINATED, are the ones Business Rules and Routing Logic gives under R-LIT-24 and R-LIT-26, and the panel rule that precedes them is R-LIT-23.

### 19. Out of scope

- AC2, AC3 and AC4 of the legacy key, the two rule paths and the refusal when the decision log cannot be written, which are owned by RWB-S4-E5009-APP; this story exercises them only as evidence reads and as the negative path.
- The legal action, the panel evaluation, the case move to FIRM_INSTRUCTED and the stage workflow inside rwb-litigation, which are RWB-S4-E5009-APP.
- The partner portal, the partner gateway in the DMZ, the partner users, the acceptance window and the result, which are rwb-partner's and belong to the S9 stories.
- The pack itself, its assembly, its checklist and its custody, which are rwb-document's and RWB-S4-E5009-APP's, and the notice, the template, the merge fields and the proof of delivery, which are rwb-comms's.
- The case, the case state and the timer table, which are rwb-case's; the harness reads the partner clock and never sets it.
- The contract baselines of rwb-litigation, rwb-partner, rwb-document, rwb-comms, rwb-case, rwb-decision and rwb-access, which are their CON stories and are consumed here through the published documents and their fakes.
- The platform configuration: the decision-record library, the gateway-bff composite route, the feature-flag library and the observability set.
- The head of litigation's nomination and the DoA table behind any approval, which belong to the litigation story, to rwb-access and to rwb-decision.
- Any production screen, event, workflow, Schedule or table: this story builds a test harness and its evidence only.
- The fixture contents, the harness environment, the evidence format and its retention, and the feature flag key: carried as a gap and assumptions, not decided here.
