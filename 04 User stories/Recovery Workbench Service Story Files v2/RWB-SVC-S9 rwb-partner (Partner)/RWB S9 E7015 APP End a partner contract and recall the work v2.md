# RWB-S9-E7015-APP End a partner contract and recall the work

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7015-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement; no size value in the source documents (DOR-RWB-S9-E7015-APP-16) |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S9-Q |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E7015-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | v1 (path `/api/recovery/partner/v1`); contract version number not specified in the source documents (DOR-RWB-S9-E7015-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract-end and recall slice of RWB-E7-015 is realigned onto rwb-partner (S9, service wave 4, business wave 4). The legacy criterion this story owns (AC2, not recorded) is kept word for word with its origin tag and nothing is added to it, because it carries no cross-service part; the main criterion of the legacy key (AC1) is owned by the wave 4 integration harness RWB-ITG-E7015-ITG. The slice is a branch of `InstructionWorkflow` on task queue `rwb-partner`: it sets `partner.panel_status` to EXITED with the contract end date, recalls every open `partner_instruction` of the partner to RECALLED, records one entry through the local decision-record library before any change (DP-03), asks rwb-case for the re-selection of each affected case on the case boundary, and sets one durable clock. It declares no REST operation, because the Ownership Map gives S9 six operations and none of them ends a contract; the effect is read through `GET /partners` and `GET /partner/instructions` on base `/api/recovery/partner/v1` (DP-13) behind the gateway-bff composite route (DP-19). The service owns EV-20 `InstructionIssued` and EV-21 `PartnerResultSubmitted` and both belong to the issue and the result of an instruction, so no event carries the contract end or the recall. No PRM rule set exists in the Business Rules and Routing Logic v4, the word "open" is not defined for an instruction, the case-side re-selection boundary is unpublished and the partner service level sits on no rule row (GAP-3129; ASM-5460 to ASM-5467). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E7015-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 16 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager (RW-AGENCYMG)** — and as the other roles the legacy permission table gives Partner portal U — I want **to close the contract of a partner and pull every open instruction of that partner back for re-selection**, so that **no case stays with a partner that has left the panel and the exit is on the decision record with the rule version it was judged under**.

This story owns:

- the one legacy criterion of RWB-E7-015 that the plan gives it (AC2, not recorded), copied verbatim with its origin tag;
- the `contractEnd` branch of `InstructionWorkflow` on task queue `rwb-partner` in namespace `rwb-recovery`, one execution per partner that holds its open instructions and their clocks;
- the close of the contract on the partner row: `panel_status` EXITED with the end date in `contract_end` (DF-PRT-005, DF-PRT-006);
- the recall of every open instruction of the partner to RECALLED (`partner_instruction.status`, DF-PRT-014, LOV-INSTR-STATUS);
- the decision record: one entry per contract end, written through the local decision-record library **before** anything else, carrying the partner, the instruction set, the case set, R-UNI-26 and the package version in force (DP-03; legacy AC2);
- the request to rwb-case to re-select each affected case on the rule of R-UNI-45, one Temporal command per case on the case boundary;
- one durable clock: the R-UNI-26 service level of 5 working days, whose expiry escalates under R-UNI-30;
- the reads behind SCR-34 Partner list and SCR-35 Placement and allocation through the gateway-bff composite route (DP-19), on the service base `/api/recovery/partner/v1` (DP-13).

It does not own: the published shapes, the recall command element, the rights, the error set and the fakes (RWB-S9-E7015-CON); the main criterion AC1 and its end-to-end proof (RWB-ITG-E7015-ITG); the issue of an instruction, its acceptance, its result and its invoice (the other stories of this service); the notice on a missed target and its cure period (FEAT-PRM-11); the allocation and the scorecard that pick the next partner (FEAT-PRM-03, FEAT-PRM-08); the job that scores partners monthly (FEAT-PRM-08); the case of record, its route state and its timers (rwb-case P3); the rule packages and the central ledger (rwb-decision P7); the roles and rights (rwb-access P4); and the schema, migration and deployment of this service (the DB, INF and OPS stories of this key).

### 2. Business rationale

The objective, the problem and the metric are the module's and do not move: partners are instructed and paid by email and spreadsheet and allocation is not based on performance, the metric is the placements made by scorecard against 100 percent, measured on the decision log and the Workbench records and reviewed monthly (FSD S9 A2.12.1). The requirements are REQ-S9-006, "A partner panel exit, a declared conflict of interest, insolvency or an upheld conduct breach recalls every open case held by that partner", and REQ-S9-001, the six points every partner type is managed on, the last of which is notice and exit (Program BRD v4; FSD S9 Requirements served).

A contract end is the one point where every case a partner holds has to come back at once. The legacy story states it as a single action on one screen; the rule that carries it is R-UNI-26 — the partner leaves the panel or the contract ends, every open case of that partner is recalled and re-selected, to PARTNER_RECALLED, within 5 working days — with R-UNI-45 for the re-selection, R-UNI-25 for the recall of a missed service level, R-UNI-27 to R-UNI-29 for the other recall triggers, R-UNI-38 for the rule version an open case keeps and R-UNI-39 for the record-first rule. What D-RCV-60 changes is who owns each fact of that exit:

- **The contract and the instruction are this service's.** `partner` holds `panel_status` and `contract_end` and `partner_instruction` holds the status of every placed instruction (TSD S9 T3.1, DF-PRT-005, DF-PRT-006, DF-PRT-014), so this service is the only one that can close the contract and say which work was still open.
- **The case is not.** The recall of the work is a change of the partner's instructions plus a request to rwb-case to re-select, because R-UNI-45's to_state is ROUTE_D6_REOPEN, a case route state, and `recovery_case` and its timers are P3's. This step therefore commands the case and never writes it (ASM-5462).
- **The exit is a decision, so it is recorded.** Legacy AC2 says that where the decision log cannot be written nothing changes and MSG-P7-003 is shown; R-UNI-39 says the same in the rules. The entry is written through the local library in one transaction, before the partner row, the instructions or the case request move (DP-03).
- **The instruction states are a closed list.** RECALLED is one of the six values of LOV-INSTR-STATUS (SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE, RECALLED) and EXITED is one of the four of LOV-PANEL; this story adds no state, no column and no table (ASM-5461).
- **The clock is a rule fact, not a constant.** R-UNI-26's timer column carries 5 working days and the partner type sets its own service level, so the length is read from the rule row or the reference data at its version and never written in code (ASM-5463).

### 3. Preconditions

- RWB-S9-E7015-CON is published and tagged: the two read elements, the unchanged partner and instruction shapes, the recall command element, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-34 and SCR-35 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `partner` and `partner_instruction` exist in `rwb_partner` from the DB story of this service, with the fields of DF-PRT-001 to DF-PRT-016 and the standard record columns of TSD S9 T3.0; at least one partner carries open instructions (DF-PRT-014).
- An `InstructionWorkflow` execution exists for the partner on `rwb-partner` and holds its open instructions with their clocks. The one workflow the Ownership Map gives S9 is this one (context pack ownership rows, Workflows: 1; ASM-5461).
- The UNIVERSAL package is in force at its version with R-UNI-25, R-UNI-26, R-UNI-30, R-UNI-38, R-UNI-39 and R-UNI-45; it is authored, tested and approved in rwb-decision (P7) and loaded here. No PRM package exists in the rule set (Business Rules and Routing Logic v4; ASM-5464).
- The case-side re-selection boundary is available for the fake: the case reference, its route state and the requested re-selection arrive as a Temporal command and the outcome is the child result. Its workflow or operation name is Not specified in the source documents (GAP-3129; ASM-5462).
- The lists of values this step reads — `LOV-PANEL` with ACTIVE, ON_NOTICE, SUSPENDED and EXITED and `LOV-INSTR-STATUS` with SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED — are reference data with their version, read on the owner's contract and never written in code (TSD S9 T3.2).
- The service runs as its own login on `rwb_partner` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E7015-CON when its tests pass.

### 4. Flow

1. The partner and agency manager ends the contract of a partner on SCR-34. The act has no published REST operation: it arrives as a Temporal command on the partner's `InstructionWorkflow` execution on queue `rwb-partner`, with the partner reference, the end date and the reason code (GAP-3129; ASM-5460).
2. The `contractEnd` branch starts and reads the open instructions of the partner from `rwb_partner`: every row whose `status` is SENT, ACCEPTED or IN_PROGRESS, with its case reference and its due time (ASM-5461).
3. `evaluateRecallRules` loads the UNIVERSAL package version in force and evaluates R-UNI-26 for the exit, R-UNI-38 for the version an open case keeps and R-UNI-39 for the record-first rule; no version in force stops the branch and changes nothing (ASM-5464).
4. `recordAndApplyExit` writes one entry through the local library **before any other effect**: the partner, the end date, the recalled instruction set with its case keys, the rule ID R-UNI-26 with its package version, the actor and the clock start. A failed write stops the step with nothing changed and MSG-P7-003 (DP-03; legacy AC2).
5. In the same transaction the partner row is closed: `panel_status` EXITED and `contract_end` set to the end date (DF-PRT-005, DF-PRT-006). No other column of `partner` moves.
6. Each open instruction is moved to RECALLED in the same transaction, so the set the entry names and the set that reads RECALLED are the same set (DF-PRT-014).
7. `requestCaseReselection` asks rwb-case, one command per affected case on the case boundary, to reopen the route and re-select the next partner under R-UNI-45. The request carries the partner, the recalled instructions and the reason code, and the case applies it; this service writes no case row (ASM-5462).
8. `recallClock` starts one durable timer for the R-UNI-26 service level of 5 working days and R-UNI-45's 2 working days for the re-selection; the expiry escalates under R-UNI-30 to the named escalation point and the case does not move (ASM-5463).
9. A repeated command for the same partner and end date is idempotent: one entry, one recall, one timer, and the repeat answers the entry it already wrote (ASM-5465).
10. The partner reads EXITED on `GET /partners` and its instructions read RECALLED on `GET /partner/instructions`, both through the composite route, read only (DP-13, DP-19).
11. The re-selection that follows is the partner manager's separate act under FEAT-PRM-03 and FEAT-PRM-04; this story requests it and builds none of it.
12. A result submitted for a recalled instruction is refused by the result operation of the service, because the instruction no longer reads a status that accepts a result (R-UNI-26; ASM-5466).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: the partner stays open, no instruction moves, no case is asked to re-select and no clock starts | MSG-P7-003 | AC2, TC-E7-015-02, TC-E7-015-04 |
| X2 | The role does not hold Partner portal U | 403 before the partner row is read and before the record is written | MSG-P4-002 | AC3, TC-E7-015-03 |
| X3 | A required value is absent or invalid: no partner reference, no end date or no reason code | The branch refuses the exit, writes nothing and names the field | MSG-GEN-001 (VR-S9-012-1) | AC4, TC-E7-015-07 |
| X4 | The case re-selection command does not answer inside 2 s, or its breaker is open | The instruction set stays recalled, the command is retried on the workflow's own schedule, the case is not marked re-selected, and the caller sees the platform 503 envelope | None (platform envelope) | AC5, TC-E7-015-08 |
| X5 | The partner already reads EXITED with the same end date | Idempotent: the entry already written is answered and nothing is written or escalated again | None | AC6, TC-E7-015-09 |
| X6 | The partner holds no open instruction | The contract is still closed and recorded, the recall set is empty and the answer says so; no case is asked to re-select | None | AC7, TC-E7-015-10 |
| X7 | An instruction moves out of an open status while the branch is running (DONE, DECLINED) | That instruction is left as it is and is not named in the recall set; the transaction re-checks the status before the update | None | AC8, TC-E7-015-11 |
| X8 | The UNIVERSAL package has no version in force for R-UNI-26 or R-UNI-45 | The branch waits, the contract is not closed and no clock is taken on an unversioned rule | None | AC9, TC-E7-015-12 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC10, TC-E7-015-13, Section 17, BR5, BR6 |

X1 and X2 are the legacy not-recorded and access paths of this key carried onto the slice; X3 to X8 are the paths the recall set, the case command and the clock add; X9 is the schema and ACE boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E7015-CON, the decision-record stub, the case re-selection fake, the package fake and the gateway-bff fake, on its own schema, and needs no live P3 or P7 |
| Negotiable | The activity names, the "open" status set, the command shape and the entry attributes are this story's choice; the rules, the messages, the screens, the clock source and the lists are fixed |
| Valuable | A partner that leaves the panel has every open instruction recalled and every case sent back for re-selection, and the exit is recorded once with its rule version |
| Estimable | One workflow branch, four activities, one record write, one partner update, one instruction update set, one child command per case and one durable timer |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on a synthetic partner through the contract fakes, plus the empty recall set, the repeat, the refused right and the forced record-write failure |

### 7. Acceptance criteria

```gherkin
Feature: End a partner contract and recall the work

  Background:
    Given the UNIVERSAL rule package is in force at its version and carries R-UNI-26, R-UNI-38, R-UNI-39 and R-UNI-45
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Not recorded (legacy RWB-E7-015 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Partner portal U not held (X2) (new, D-RCV-60)
    Given the caller holds Partner portal R and not U
    When the contract end is requested
    Then the request is refused with 403 and MSG-P4-002 before the partner row is read or the record is written

  Scenario: AC4 Required value absent or invalid (X3) (new, D-RCV-60)
    Given the contract end request has no partner reference, no end date or no reason code
    When the branch runs
    Then the exit is refused, nothing is written and the field is named with VR-S9-012-1 and MSG-GEN-001

  Scenario: AC5 Case re-selection does not answer (X4) (new, D-RCV-60)
    Given the case re-selection command does not answer within 2 s or its breaker is open
    When the branch requests the re-selection
    Then the instruction set stays RECALLED, the command is retried on the workflow schedule, the case is not marked re-selected and the caller sees the platform 503 envelope

  Scenario: AC6 Repeat of an exit with the same end date (X5) (new, D-RCV-60)
    Given the partner already reads EXITED with the same end date
    When the contract end is requested again
    Then the entry already written is answered and nothing is written or escalated again

  Scenario: AC7 Partner holds no open instruction (X6) (new, D-RCV-60)
    Given the partner holds no open instruction
    When the contract end is requested
    Then the contract is closed and recorded, the recall set is empty, the answer says so and no case is asked to re-select

  Scenario: AC8 Instruction leaves an open status during the branch (X7) (new, D-RCV-60)
    Given an instruction moves to DONE or DECLINED while the branch is running
    When the recall update runs
    Then that instruction is left as it is, is not named in the recall set and the transaction re-checks its status before the update

  Scenario: AC9 No version in force for R-UNI-26 or R-UNI-45 (X8) (new, D-RCV-60)
    Given the UNIVERSAL package has no version in force for R-UNI-26 or R-UNI-45
    When the contract end is requested
    Then the branch waits, the contract is not closed and no clock is taken

  Scenario: AC10 ACE view, case row or foreign schema reached (X9) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a rwb_case row or another service's schema
    When the grant or the boundary test runs
    Then the grant refuses the statement, the boundary test fails the build and nothing is released

  Scenario: AC11 Rules of section 8 hold (new, D-RCV-60)
    Given the contract end is requested on a partner with open instructions
    When the branch runs
    Then each rule BR1 to BR9 of section 8 holds as written there

  Scenario: AC12 Activity retried or timed out (new, D-RCV-60)
    Given the case re-selection activity is retried or times out
    When the branch waits for the re-selection answer
    Then the retry runs on the workflow schedule, the instruction set stays RECALLED and the case is not marked re-selected

  Scenario: AC13 Status change the model does not allow (new, D-RCV-60)
    Given an instruction is asked to move to a status the model does not allow from its current status
    When the status change is applied
    Then the change is refused and the instruction keeps its status
```

The criterion is the legacy criterion of RWB-E7-015 with its origin tag added and one word changed: `decision log` is now `decision record`, so the wording of `the decision record cannot be written`, `the action is taken` and `nothing changes and the user sees MSG-P7-003` all stand. It carries no cross-service part, so no `Given the <service> contract mock returns <x>` line is added to it. On this story "the action" is the contract end on a partner, and what the legacy line describes now happens in two places: rwb-partner closes the contract, recalls the instructions and writes the local record, and rwb-case is asked to re-select each case. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_partner`, with the `decision_log_entry` ledger of rwb-decision behind it. The main criterion of the key (AC1) stays with RWB-ITG-E7015-ITG, which owns it word for word; this story builds the path it proves.

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-UNI-25 | Universal rules | All | ANY_ACTIVE | PARTNER_NO_RESPONSE | the partner misses the service level on the portal | Chase once, then recall the work and re-select on the scorecard | PARTNER_RECALLED | Partner and agency manager | Partner Portal | per partner type |
| R-UNI-26 | Universal rules | All | ANY_ACTIVE | PARTNER_PANEL_EXIT | the partner leaves the panel or the contract ends | Recall every open case held by that partner and re-select | PARTNER_RECALLED | Partner and agency manager | Partner Portal | 5 working days |
| R-UNI-30 | Universal rules | All | ANY_ACTIVE | SLA_BREACHED | time in the current state exceeds the service level | Raise the breach to the named escalation point. The case does not move | ESCALATED | Team manager | Workbench | per state |
| R-UNI-38 | Universal rules | All | ANY_ACTIVE | RULE_VERSION_EFFECTIVE | a new rule version reaches its effective date | Apply it to decisions taken from that date. Open cases keep the version they were decided under | RESUME_STATE | Center of excellence | Workbench | on the effective date |
| R-UNI-39 | Universal rules | All | ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision log entry cannot be written | Block the action and raise an incident. No action proceeds unlogged | EXCEPTION_QUEUE | Platform team | Workbench | immediate |
| R-UNI-45 | Universal rules | All | PARTNER_RECALLED | PARTNER_RESELECTED | the next partner is selected on the scorecard | Re-issue the instruction and restart the partner clock | ROUTE_D6_REOPEN | Partner and agency manager | Partner Portal | 2 working days |

The six rows are the rows of the Business Rules and Routing Logic v4, copied character for character. This story evaluates R-UNI-26 for the exit, R-UNI-38 for the version an open case keeps and R-UNI-39 for the record-first rule; it names R-UNI-45 as the rule of the request it sends to rwb-case and R-UNI-30 as the rule its clock expires under, and it reads R-UNI-25 because a missed service level is the chase that ends in the same recall. R-UNI-27 to R-UNI-29 recall the work for a conflict, an insolvency and a conduct breach and run through the same branch; they are not fired here. Their owner column names a business role and a system, not a service: "Partner Portal" is this service and its partner-facing screens.

| ID | Rule | Source |
|---|---|---|
| BR1 | The exit is a decision first: one entry per contract end is written through the local library, with the partner, the end date, the recalled instruction set and case keys, R-UNI-26 and the package version; a failed write changes nothing and answers MSG-P7-003 | DP-03; TSD S9 T2; R-UNI-39; legacy AC2 |
| BR2 | The contract and the instruction are this service's: `partner.panel_status` and `partner.contract_end` close the contract and `partner_instruction.status` moves each open instruction to RECALLED, both inside the transaction of the entry | TSD S9 T3.1 (DF-PRT-005, DF-PRT-006, DF-PRT-014); TSD S9 T3.2 (LOV-PANEL, LOV-INSTR-STATUS) |
| BR3 | "Open" is the three statuses SENT, ACCEPTED and IN_PROGRESS; DONE, DECLINED and RECALLED are not recalled, and an instruction that leaves an open status during the branch is left as it is | TSD S9 T3.2; ASM-5461 |
| BR4 | The case is not written here: the re-selection is a Temporal command to rwb-case under R-UNI-45, whose to_state ROUTE_D6_REOPEN is a case route state, and its outcome is the child result | R-UNI-45; Architecture v5 slides 8 and 12; ASM-5462 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_partner`; `case_id` and the case reference are identifiers of another service's fact | DP-01; TSD S9 T3.3 |
| BR6 | ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and no customer value, number or address is read or written by this path | DP-05, DP-11; TSD S9 T5.2 |
| BR7 | Every value a business person may change is a rule row or reference data read with its version: the 5 working days of R-UNI-26, the 2 working days of R-UNI-45, the escalation point, the panel and instruction lists and the package versions | FSD S9 BR-S9-012; legacy Guardrails |
| BR8 | The exit is idempotent per partner and end date: one entry, one recall set and one clock, and a repeat answers the entry that exists | TSD S9 T-A.2; Architecture v5 slide 11 |
| BR9 | No person name, customer identity, account number or contact value enters `rwb_partner`, an entry, a log, a workflow input or an event; the partner code and the case and instruction references are not personal data | Template and Rules §R7.2 (s17); LDM v8 |
| BR10 | R-UNI-25: a missed service level on the portal is chased once, then the work is recalled and re-selected; read here as the chase that ends in the same recall | Business Rules and Routing Logic v4 (R-UNI-25) |
| BR11 | R-UNI-26: the partner leaves the panel or the contract ends; recall every open case held by that partner and re-select, 5 working days | Business Rules and Routing Logic v4 (R-UNI-26) |
| BR12 | R-UNI-30: time in the current state exceeds the service level; the breach is raised to the named escalation point and the case does not move; the recall clock expires under it | Business Rules and Routing Logic v4 (R-UNI-30) |
| BR13 | R-UNI-38: a new rule version reaches its effective date; open cases keep the version they were decided under | Business Rules and Routing Logic v4 (R-UNI-38) |
| BR14 | R-UNI-39: the decision record entry cannot be written; the action is blocked and an incident is raised, and no action proceeds unlogged | Business Rules and Routing Logic v4 (R-UNI-39) |
| BR15 | R-UNI-45: the next partner is selected on the scorecard; the instruction is re-issued and the partner clock restarts, 2 working days | Business Rules and Routing Logic v4 (R-UNI-45) |

### 9. State transitions

This story moves two states of its own tables and one of the rule set, and never a case state:

| From (`partner.panel_status`, DF-PRT-005) | Event | Condition | To | What this story writes |
|---|---|---|---|---|
| ACTIVE | PARTNER_PANEL_EXIT | the contract ends (R-UNI-26) | EXITED | `panel_status` and `contract_end`, in the transaction of the entry |
| ON_NOTICE | PARTNER_PANEL_EXIT | the contract ends after the notice and the cure period (FEAT-PRM-11) | EXITED | the same two columns |
| SUSPENDED | PARTNER_PANEL_EXIT | the contract ends while the partner is suspended | EXITED | the same two columns |
| EXITED | PARTNER_PANEL_EXIT | the same end date arrives again | EXITED | Nothing; the entry already written is answered |

| From (`partner_instruction.status`, DF-PRT-014) | Condition | To | Note |
|---|---|---|---|
| SENT | The instruction is open at the contract end | RECALLED | The case is asked to re-select |
| ACCEPTED | The instruction is open at the contract end | RECALLED | The case is asked to re-select |
| IN_PROGRESS | The instruction is open at the contract end | RECALLED | The case is asked to re-select |
| DONE, DECLINED, RECALLED | Not open | unchanged | Not named in the recall set |

| Branch step | Event | Condition | To |
|---|---|---|---|
| Waiting | A contract-end command arrives for the partner | The package version is read | Reading |
| Reading | The open instructions are read | At least one instruction is open | Evaluating |
| Reading | The recall set is empty | X6 | Recording, with an empty set |
| Evaluating | R-UNI-26 holds and a version is in force | The clock is taken from the rule row | Recording |
| Recording | The entry is written and the partner and instructions move | The transaction commits | Commanding |
| Recording | The entry write fails | X1 | Waiting, nothing changed, MSG-P7-003 |
| Commanding | A case answers the re-selection request | The child result is accepted | Clocked |
| Commanding | A case does not answer inside 2 s | X4 | Retried on the workflow's schedule |
| Clocked | The durable timer expires | The service level has run | Escalated under R-UNI-30 |

RECALLED and EXITED are values of the two published lists and this story adds none; PARTNER_RECALLED, PARTNER_PANEL_EXIT and PARTNER_RESELECTED are the event codes of R-UNI-26 and R-UNI-45, and ROUTE_D6_REOPEN is the case state rwb-case moves to, not this service (ASM-5462).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Partner and agency manager (RW-AGENCYMG) | The primary actor of FSD S9 A2.12.3.3 and the role the legacy screen is written for: holds Partner portal U and R (TSD S9 T6.1 CRUDA) and ends the contract |
| Head of Litigation (RW-HEADLIT), Head of Asset Liquidity (RW-HEADASL) | The "also uses" roles of FSD S9 A2.12.3.3, with Partner portal RA in the matrix; they end the contract of a partner in their type |
| Litigation officer (RW-LITOFF), enforcement owner (RW-ENFORCE), sale officer (RW-SALEOFF), NPA and asset manager (RW-NPAMGR), debt sale officer (RW-DEBTSALE), guarantee officer (RW-GUARANT) | Hold Partner portal U in the legacy permission table and take the act where the partner manager delegates it |
| Case owner (RW-CASEOWN), team manager (RW-TEAMMGR), legal counsel (RW-LEGAL) | Partner portal R: read the partner and its instructions, and never end a contract |
| Partner portal users (PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC) | Partner portal RU: read their own instructions and record results; they cannot end a contract or read another firm |
| Platform team (R-UNI-39, owner column) | Receives the incident when the record cannot be written; no business right is used for it |
| rwb-case (P3) | Owns the case, its route state and its timers, and applies the re-selection request this story sends |
| rwb-decision (P7) | Owns the UNIVERSAL package, its rule rows and the central ledger; this story evaluates them and records locally |
| rwb-access (P4) | Owns the roles, the capability rights and the lists of values this story reads through the guard |

No delegated authority limit is set here: the customer-level delegation table is rwb-access's (P4) and this act moves partner work, not a customer decision.

### 11. Data

| BR Field ID | Entity | Owner | Use in this story |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | `partner` | S9, `rwb_partner` | **Read** `id`, `partner_code`, `partner_name`, `partner_type`, `score`; **write** `panel_status` to EXITED (DF-PRT-005) and `contract_end` to the end date (DF-PRT-006) |
| DF-PRT-008 to DF-PRT-016 | `partner_instruction` | S9, `rwb_partner` | **Read** `id`, `case_id`, `partner_id`, `instruction_type`, `instructed_at`, `due_at`, `status`; **write** `status` to RECALLED (DF-PRT-014) for the open set only |
| None in the sources | `partner_user` | S9, `rwb_partner` | Not read and not written. The context pack gives S9 this table and TSD S9 T3.1 gives it no field list (ASM-5461) |
| None: library table | `decision_record` | Platform library in `rwb_partner` | **Write**: one hash-linked entry per contract end, before anything else (DP-03) |
| None: library table | `idempotency_key`, `outbox_event` | Platform library in `rwb_partner` | The partner-and-date key and the answer it holds; the outbox object exists as a library row and this step writes no event row to it (§12.3) |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | P3 rwb-case | Not read as a table and not written: the case reference arrives from `partner_instruction.case_id` and the re-selection is a command, not a row |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | Not written: the local entry is copied to the central ledger by its owner, and its identifier is not stored here |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | Not read as a table: the UNIVERSAL package arrives loaded at its version in force |
| `LOV-PANEL`, `LOV-INSTR-STATUS` | reference data and lists of values | P3 rwb-case (default ruling) | Read at their version; the panel list carries EXITED and the instruction list carries RECALLED (TSD S9 T3.2) |

No new table, no new column and no migration: the two tables arrive with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_partner` by the library's own migration (DP-03).

**No personal data.** The entry and the commands carry a partner reference, a partner code, case and instruction references, a status, a date and a rule version. No customer name, identity number, account number or contact value enters `rwb_partner`, an entry, a log or a workflow input (BR9).

### 12. Contract

#### 12.1 REST operations provided

None declared by this story. Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). The six operations the Ownership Map gives S9 are `GET /partners`, `GET /partner/instructions`, `POST /cases/{caseId}/instructions`, `POST /partner/instructions/{instructionId}/accept`, `POST /partner/instructions/{instructionId}/invoices` and `POST /partner/instructions/{instructionId}/results`; none of them ends a contract, and this story declares no seventh. The two reads of the service answer the effect of this story — `panel_status` and `contract_end` on the partner, `status` on the instruction — and both are declared by RWB-S9-E7015-CON. The act itself has no published entry point and carries the placeholder (GAP-3129; ASM-5460). A build that declares a contract-end operation here fails the absence test of RWB-S9-E7015-CON.

#### 12.2 REST operations consumed

None. The step consumes no REST operation: its own two tables are read on `rwb_partner`, the packages arrive loaded at their version, and the case is reached on the Temporal boundary (§12.5). The re-selection request is therefore a contract dependency of class C in fact and not in the plan, whose C row is empty, and the absence is recorded (GAP-3129; ASM-5462).

#### 12.3 Events published

None. The service publishes on `rwb.partner.events.v1` and its event set is `InstructionIssued` (`rwb.partner.InstructionIssued.v1`, EV-20) and `PartnerResultSubmitted` (`rwb.partner.PartnerResultSubmitted.v1`, EV-21); both describe the issue of an instruction and the result the partner records, and both belong to the instruction stories of this service (context pack ownership rows; Event and Messaging Design v5 EV-20 and EV-21; TSD S9 T5.3). A contract end issues no instruction and records no result, so this story declares no producer group, no envelope and no outbox row, and RWB-S9-E7015-CON fails a build that adds one (GAP-3129; ASM-5465).

#### 12.4 Events consumed

None. No source gives rwb-partner a consumed event for a contract end: the act arrives as a Temporal command from the partner-facing act, the panel and the scorecard are this service's own records, and EV-21 is the result the partner portal records and not an exit. This service therefore declares no consumer group, no subscription and no inbox of its own (ASM-5465).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per partner holding its open instructions and their clocks, continues-as-new | `rwb-partner` | Hosts the `contractEnd` branch; its input is the partner reference, the end date and the reason code, and its outcome is the recall answer |
| `contractEnd` | Branch of `InstructionWorkflow` (not a separate catalogued workflow) | `rwb-partner` | The path from the command to the entry, the partner close, the recall set, the case requests and the clock |
| `readOpenInstructions` | Activity | `rwb-partner` | The partner and its instructions in; the open set with its case keys and the partner classification out |
| `evaluateRecallRules` | Activity | `rwb-partner` | The package in force in; R-UNI-26, R-UNI-38 and R-UNI-39 with their versions and the recall decision out |
| `recordAndApplyExit` | Activity | `rwb-partner` | The entry, the partner close, the recall set and the clock start out, one transaction |
| `requestCaseReselection` | Activity | `rwb-partner` | One child command per case on the case boundary, under R-UNI-45; the case reference and the recall reason in |
| `recallClock` | Durable timer of the branch | `rwb-partner` | The 5 working days of R-UNI-26 and the 2 working days of R-UNI-45 with their versions; the expiry is the escalation |

The recall answer carries the partner, the entry reference, the recalled instruction set with its case keys, R-UNI-26 with its version, the number of cases asked to re-select and the clock start. The execution grain — one execution per partner holding that partner's open instructions rather than one per instruction, because a contract end spans a partner's instruction set and the sources give the workflow's name only — is a target design choice recorded in the registers. The branch and activity names are a target design choice fixed by no source document, and the case-side command has no published name (GAP-3129; ASM-5462). Workflow ID form: Not specified in the source documents (DOR-RWB-S9-E7015-APP-8). Start rule of InstructionWorkflow: Not specified in the source documents (DOR-RWB-S9-E7015-APP-8).

#### 12.6 Schedules

None. The Ownership Map gives S9 no job (context pack ownership rows, Jobs: 0) and FSD S9 A2.12.4.4 declares no background event for this feature. The recall clock is a durable Temporal timer inside the branch, not a Schedule, not a Quartz row and not a shared job table; DP-10 is not in this key's pattern set (ASM-5463).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `partner` | S9, `rwb_partner` | The partner, its type, its panel status, its contract end and its score; this story writes `panel_status` and `contract_end` only |
| `partner_instruction` | S9, `rwb_partner` | The work placed with a partner on a case; this story writes `status` for the open set only |
| `partner_user` | S9, `rwb_partner` | Owned per the context pack ownership rows; this story neither reads nor writes it (ASM-5461) |
| `decision_record` | Platform library in `rwb_partner` | The local hash-linked entry of the contract end (DP-03) |
| `idempotency_key` | Platform library in `rwb_partner` | The partner-and-date key of the repeated command |
| `outbox_event` | Platform library in `rwb_partner` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case`, `queue`, `assignment` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6) and every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC2, X1 |
| rwb-case re-selection fake | The case `RW-2027-001501` accepting the re-selection request with its route reopened, the same case refusing it, and no answer inside 2 s | X4, X5 |
| rwb-decision package fake | The UNIVERSAL package at its version in force with R-UNI-25, R-UNI-26, R-UNI-30, R-UNI-38, R-UNI-39 and R-UNI-45; a package with no version in force | X8 |
| rwb-access guard fake | RW-AGENCYMG with Partner portal U and R, and a role with R only | X2 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answers for the partner and its instructions | Section 15 |
| Partner fixture | Partner `PTR-2027-001501` of type AGENCY at ACTIVE with contract_end in the future, holding instructions `INS-2027-001501` (SENT) and `INS-2027-001502` (ACCEPTED) on case `RW-2027-001501`, and one instruction at DONE | X3, X6, X7 |

The fakes are test-only and are replaced by the real services in SIT. The case-side command name is a placeholder until its owner publishes it (GAP-3129; ASM-5462).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | The two reads of the service are declared by RWB-S9-E7015-CON; the act has no operation |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 belong to the instruction stories; the decision record rides the library's shared `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 4 activities, 1 durable timer and 1 child command per case | `InstructionWorkflow` and its `contractEnd` branch on `rwb-partner`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `exit`; front end `src/modules/recovery/partner/PartnerExit.tsx`, the SCR-34 and SCR-35 fragments this story answers.

**Pattern application** (§R5.5)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the entry commits before the partner row, the recall set and the case requests, and a failed write leaves nothing behind. DP-13 fixes the base of the service and gives the act no element of its own, because the six operations the Ownership Map gives S9 belong to the other stories of this service. DP-19 is how SCR-34 and SCR-35 reach this service, one hop through the gateway. Two dependencies the plan does not carry are recorded rather than added: the case re-selection boundary (ASM-5462) and the lists of values read at a version (ASM-5461).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `InstructionWorkflow` contract-end branch | Workflow | Receives the command, hosts the clock, applies the idempotency key and reports the answer |
| `readOpenInstructions` | Activity | Reads the partner and its open instructions on `rwb_partner` and builds the recall set |
| `evaluateRecallRules` | Activity | Evaluates R-UNI-26, R-UNI-38 and R-UNI-39 and returns the rule IDs with their package versions |
| `recordAndApplyExit` | Activity | Writes the entry, closes the partner and moves the recall set in one transaction |
| `ExitEntryWriter` | Library adapter | Writes the hash-linked entry before any other effect and refuses the step when the write fails |
| `CaseReselectionClient` | Client | The Temporal command to rwb-case per affected case, with the breaker and the retry of the workflow |
| `PartnerExitReader` | Repository | The partner and its instructions, read on this schema only |
| `RecallClock` | Durable timer | The 5 working days of R-UNI-26 and the 2 of R-UNI-45 with their versions |
| `PartnerExit` | React component | Shows the contract end, the recall set and the clock on SCR-34 and SCR-35 |

**Database and migrations.** No Flyway file. `partner` and `partner_instruction` arrive with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_partner` by the library's migration (DP-03). No column is added: the recall is carried by `partner_instruction.status` and the exit by `partner.panel_status` and `partner.contract_end` (ASM-5461).

**Configuration and reference data.**

- The 5 working days of R-UNI-26 and the 2 working days of R-UNI-45: rule rows read at their version (ASM-5463).
- The named escalation point of R-UNI-30 and the partner type service level: reference data with their versions.
- `LOV-PANEL` and `LOV-INSTR-STATUS`: read at their version through the reference-data contract of rwb-case (default ruling DP-07).
- The capability area "Partner portal" and its rights: access rows of rwb-access, read through the guard.

**Build steps**

1. The `contractEnd` branch and its input record on `rwb-partner`, registered as a branch of `InstructionWorkflow`, with the command, the idempotency key and the durable timer.
2. `PartnerExitReader` with the open set (SENT, ACCEPTED, IN_PROGRESS), the empty set and the instruction that leaves an open status mid-run (X3, X6, X7).
3. `evaluateRecallRules` over the package in force, with R-UNI-26, R-UNI-38 and R-UNI-39 and the unversioned-package path (X8).
4. `ExitEntryWriter` against the stub, with the failed-write path and MSG-P7-003 (AC2, X1).
5. `recordAndApplyExit` with the partner close, the recall set and the entry in one transaction, and the repeat path (X5).
6. `CaseReselectionClient` against its fake, one command per case, with the 2 s budget, the breaker and the unavailable path (X4).
7. The recall clock and the R-UNI-30 escalation, then the read-only SCR-34 and SCR-35 fragments through the composite route fake (DP-19).
8. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no row or write in another service's schema (X9, BR5, BR6).

**Screen states (SCR-34 and SCR-35).** Empty, error and no access states: Not specified in the source documents (CG-ALL-12083, CG-ALL-12084). The command outcomes behind them are in AC2 (decision record cannot be written: nothing changes and MSG-P7-003), AC3 (no access: 403 with MSG-P4-002 and no partner read) and AC7 (no open instruction: recall set empty). Empty-state display text and loading state: Not specified in the source documents (DOR-RWB-S9-E7015-APP-10).

**Feature flag.** `rwb.partner.contract-exit-v1`, a flag of the platform library; off means the command is refused, the partner stays open and the recall does not run.

**Done when.** The tests of section 16 pass, a contract end on a synthetic partner recalls every open instruction, a case is asked to re-select and reads the recall after the child result, the entry carries its rule version, the clock escalates at the service level, an empty recall set closes the contract and records an empty set, a repeated command writes once, a forced entry failure changes nothing, the refused right answers MSG-P4-002, and no row or write in another service's schema and no `v_ace_*` read exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the exit is absent or invalid, for example no partner reference, no end date or no reason code (X3, VR-S9-012-1) | Enter {field}. |
| MSG-P4-002 | A role without Partner portal U takes the act, or a partner portal user tries to read another firm's instructions (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The entry cannot be written before anything else (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are those of the legacy message set of this key; the text is the legacy and FSD S9 wording, copied unchanged, and no message is reworded and no new one is added. R-UNI-39's incident is raised by the platform on the same failure and is not a message of this service.

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-34 Partner list | Loading; list; contract ended; recall running; empty, error and no access: Not specified in the source documents (CG-ALL-12083) | The partner with its partner type, panel status EXITED and contract end, and the recall set with each instruction's status and case, read only through the composite route |
| SCR-35 Placement and allocation | Loading; list; recalled; re-selection requested; empty, error and no access: Not specified in the source documents (CG-ALL-12084) | The placement of the recalled instructions and the case each one was pulled back from, read only |

Both screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case and its route state; this story fixes only its own partner and instruction answer, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The recalled, refused, not-recorded and unavailable states read the messages of section 14 on the same route. The re-selection itself renders on FEAT-PRM-03's and FEAT-PRM-04's screens and is not built here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-015-01 | The recall path built here (AC1 run by RWB-ITG-E7015-ITG) | Component | Partner `PTR-2027-001501` at ACTIVE with instructions SENT and ACCEPTED on case `RW-2027-001501`; the entry, the partner close, the recall set, the case request and the clock asserted; the end-to-end proof of AC1 is RWB-ITG-E7015-ITG |
| TC-E7-015-02 | AC2 | Component | The decision-record stub stopped; no entry, no partner close, no recall, no case request and MSG-P7-003 |
| TC-E7-015-03 | AC3, Access | Component | A role with Partner portal R and not U; 403 with MSG-P4-002 and no partner read |
| TC-E7-015-04 | Principle 5; AC2, X1 | Component | A forced decision-record write failure stops the action with MSG-P7-003 and leaves the partner, the instructions, the cases and the timer unchanged |
| TC-E7-015-05 | Contract of §12: operations, events and activities | Contract | The recall answer and the case request as §12.5 defines them; EV-20 and EV-21 carry no contract end and no recall |
| TC-E7-015-06 | §12.7 table boundary (ASM-3438) | Component | Writes only `partner.panel_status`, `partner.contract_end` and `partner_instruction.status`; no read or write of `partner_user`, `recovery_case`, `queue`, `assignment` or `timer`; no `v_ace_*` read |
| TC-E7-015-07 | AC4 (X3) | Component | Requests missing the partner reference, the end date or the reason code, and one with an invalid value; each is refused with VR-S9-012-1 and MSG-GEN-001 and nothing is written |
| TC-E7-015-08 | AC5 (X4) | Component | The case re-selection stub does not answer within 2 s, then with an open breaker; the instruction set stays RECALLED, the case is not marked re-selected and the platform 503 envelope is returned |
| TC-E7-015-09 | AC6 (X5) | Component | A second contract end with the same partner and end date; the stored entry is answered and no second entry, recall or request is written |
| TC-E7-015-10 | AC7 (X6) | Component | A partner with no open instruction; the contract is closed and recorded, the recall set is empty and no case request is sent |
| TC-E7-015-11 | AC8 (X7) | Component | An instruction set to DONE during the branch; it keeps its status, is not in the recall set and the update re-checks the status |
| TC-E7-015-12 | AC9 (X8) | Component | The UNIVERSAL package with no version in force for R-UNI-26; the branch waits, the contract stays open and no clock starts |
| TC-E7-015-13 | AC10 (X9) | Component | A statement reading a v_ace_* view and a rwb_case row; the grant refuses it and the boundary test fails the build |
| TC-E7-015-14 | AC11 (BR1 to BR9) | Component | The rules of section 8 on the fakes: the record first, the open statuses, the case request, the rule version and the idempotent repeat, with no personal data in any entry, log, input or event |
| TC-E7-015-15 | AC12 | Component | The case re-selection stub times out and is retried; the retry runs on the workflow schedule, the instruction set stays RECALLED and the case is not marked re-selected |
| TC-E7-015-16 | AC13 | Component | An instruction status change the status model does not allow from its current status; the change is refused and the instruction keeps its status |

The four IDs are the legacy cases of RWB-E7-015 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The empty recall set, the instruction that leaves an open status, the repeat and the unversioned package are covered by TC-E7-015-09 to TC-E7-015-12 (AC7 to AC9) and by the new contract cases of RWB-S9-E7015-CON. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; the `-ITG` copies of the four belong to RWB-ITG-E7015-ITG, and no `-ITG` copy is written by this story. Rule coverage of section 8: BR1 by TC-E7-015-02 and TC-E7-015-04; BR2 by TC-E7-015-06; BR3 by TC-E7-015-11; BR4 by TC-E7-015-05; BR5 by TC-E7-015-06 and TC-E7-015-13; BR6 by TC-E7-015-13; BR7 by TC-E7-015-12; BR8 by TC-E7-015-09; BR9 by TC-E7-015-05; BR10, BR11, BR12 and BR15 by TC-E7-015-01; BR13 by TC-E7-015-12; BR14 by TC-E7-015-02 and TC-E7-015-04.

### 17. Guardrails

- No business value in code: the 5 working days, the 2 working days, the escalation point, the panel and instruction lists and the package versions stay rule rows or reference data read with their version.
- No personal data in `rwb_partner`, in an entry, a command, a log or a prompt: identifiers, a status, a date, a reason code and a rule version only.
- ACE data only through the owner's contract: no `v_ace_*` view, no ACE table and no other service's schema (BR5, BR6).
- The case, its route state and its timers stay with rwb-case: this story sends a command and writes no case row and no timer row (BR4).
- One base, one topic, one queue and one login per service; this story adds no second topic, no event and no Schedule (DP-13, DP-14).
- The record is written before the change and in its transaction; a failure leaves nothing behind (DP-03, R-UNI-39).
- The recall is never a hard delete: the instruction keeps its row and changes status, so the history of the placement survives the exit.
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no write to the retired log table and no data-lake path.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Story element | Test cases |
|---|---|---|---|---|---|
| REQ-S9-006 | A partner panel exit, a declared conflict of interest, insolvency or an upheld conduct breach recalls every open case held by that partner (Must, E7) | FEAT-PRM-12 | Not specified in the source documents (DOR-RWB-S9-E7015-APP-2) | The contract end, the recall set, the case re-selection request and the clock | TC-E7-015-01, TC-E7-015-02 |
| REQ-S9-001 | Every partner type is managed on the same six points, the last of which is notice and exit (Must, E6) | FEAT-PRM-12 | Not specified in the source documents (DOR-RWB-S9-E7015-APP-2) | The closed contract and the recorded exit with its rule version | TC-E7-015-01, TC-E7-015-04 |
| ADR-013 | 19 services inside ACE | FEAT-PRM-12 | Not specified in the source documents (DOR-RWB-S9-E7015-APP-2) | rwb-partner as the owner of the partner and the instruction | TC-E7-015-01 |
| ADR-014 | Schema and login per service | FEAT-PRM-12 | Not specified in the source documents (DOR-RWB-S9-E7015-APP-2) | `rwb_partner` and its own login | TC-E7-015-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | FEAT-PRM-12 | Not specified in the source documents (DOR-RWB-S9-E7015-APP-2) | The case re-selection command with its budget and breaker | TC-E7-015-01 |
| ADR-022 | Local decision record plus central ledger | FEAT-PRM-12 | Not specified in the source documents (DOR-RWB-S9-E7015-APP-2) | The exit entry written before anything else | TC-E7-015-02, TC-E7-015-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-015, disposition Split (rework); feature FEAT-PRM-12 |
| Legacy criteria | AC2, owned word for word by this story; AC1 owned by RWB-ITG-E7015-ITG |
| Source text | Legacy RWB-E7-015; FSD S9 Partner management v3 A2.12 and Requirements served; TSD S9 Partner management v2 T2, T3.0 to T3.3, T4, T5.2, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-UNI-25, R-UNI-26, R-UNI-30, R-UNI-38, R-UNI-39 and R-UNI-45; LDM and Data Dictionary v8 `partner`, `partner_instruction`, `LOV-PANEL` and `LOV-INSTR-STATUS`; Event and Messaging Design v5 EV-20 and EV-21; Program BRD v4 REQ-S9-001 and REQ-S9-006 |
| Test cases | TC-E7-015-01 to TC-E7-015-04 |
| Feature and screens | FEAT-PRM-12, SCR-34 Partner list and SCR-35 Placement and allocation |
| Rules | R-UNI-26, R-UNI-38 and R-UNI-39 evaluated; R-UNI-25, R-UNI-30 and R-UNI-45 read |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the recall command element, the rights, the error set and the fakes: RWB-S9-E7015-CON.
- The main criterion AC1 of this key and its end-to-end evidence through the real partner, case and decision contracts: RWB-ITG-E7015-ITG.
- The notice on a missed target and its cure period (FEAT-PRM-11), which is the step before the exit.
- The allocation and the re-selection that picks the next partner and restarts its clock (FEAT-PRM-03, FEAT-PRM-04, FEAT-PRM-08) and the monthly scorecard.
- The issue, acceptance, result and invoice of an instruction and the operations that carry them: the other stories of this service.
- The case of record, its route state, its re-selection and its timers: rwb-case (P3), which applies the request this story sends.
- The UNIVERSAL package, its rule rows and the central ledger, and the partner and instruction reference data as products: rwb-decision (P7) and rwb-access (P4).
- The partner gateway and FAPI 2.0: partner users reach the portal through the DMZ gateway, which is the edge stories' own scope.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
