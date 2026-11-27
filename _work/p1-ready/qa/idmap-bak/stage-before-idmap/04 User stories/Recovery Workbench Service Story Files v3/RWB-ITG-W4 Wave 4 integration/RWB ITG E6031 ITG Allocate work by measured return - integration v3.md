# RWB-ITG-E6031-ITG Allocate work by measured return

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Freshness answer named by its published fields: `status` `LOADED` or `STALE`, `businessDate`, `loadedAt`.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E6031-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | RWB-S9-E6031-APP |
| Contract dependencies | RWB-ITG-E6031-CON |
| Contract version | v1 (the /v1 path of each consumed operation, section 12.2) |
| Integration dependencies | RWB-S9-E6031-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005, RD-P1-041 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-031 as the wave 4 integration proof that work is placed with the partner the scorecard picks on measured return, proved across rwb-partner, rwb-source-data and rwb-decision: the measured return read through DP08 and the score and route economics through DP11, the pick recorded with its scorecard version, the instruction issued once with its partner clock, and the freshness of the score read gating the placement; the allocation is RWB-S9-E6031-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E6031-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the placement of work by measured return proved end to end on the real services: the partner the scorecard picks read back on the instruction, the measured return behind the pick read through DP08 and the score through DP11 as of the business date, the pick recorded once with its scorecard version and rule version, two identical cases on the same business date going to the same partner rather than by rotation, and a stale score product stopping the placement**, so that **work goes where the measured return is best and no case is placed by rotation, habit or a product that has not been refreshed**.

This story builds the wave 4 integration harness and its evidence, and then stops. The scorecard evaluation, the pick of the partner and the instruction that carries it are built by S9 rwb-partner in RWB-S9-E6031-APP and its CON story. The measured return this run asserts is P1's DP08 Partner performance product over S9's own partner and instruction records, and the score the pick rests on is P1's DP11 Scores and route economics product over `v_ace_score`; the case, the assignment and the queue are P3's, the decision record and the rule rows are P7's, and the right on the placement is answered by P4. The harness reads those published values, drives the one placement operation, counts the events, observes the workflow and writes a run report per case. It provides no endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

Today partner work runs on email and spreadsheets and allocation is not based on performance (FSD S9 A1.3, line 80). The consequence is the failure this story is written against: a firm can keep receiving work after its measured return has fallen, and a firm that improves gets nothing, because nothing in the path compares one firm with another on what it actually recovered. REQ-S9-003 states the rule the story is written against — work is allocated to partners **by measured return against a scorecard, not by a fixed share** — and R-WO-30 gives the placement its concrete form: where `placement_type = soft_recovery` and an agency on the panel has capacity, the account is placed **with the agency chosen on measured return** and the instruction is sent **the same day on the portal**. R-WO-31 gives the other half: where no agency on the panel has capacity, the placement is **held** and escalated on the timer, and nothing is placed to keep a queue moving.

The second half of the story is the evidence, because a pick is only defensible if the number behind it can be read back as of the day it was used. That number is DP08 Partner performance — the Workbench product over partner and partner_instruction, refreshed on change — and DP11 Scores and route economics, the ACE product over `v_ace_score`, refreshed daily at 08:00 (FSD P1, lines 290 and 293). Both are read through rwb-source-data's published contract and never from a view or another service's schema. The decision entry the placement writes has to name the scorecard version it was taken under, because BR-S9-003 keeps the scorecard and the panel as versioned reference data and a pick whose version is unrecorded cannot be replayed. A stale score product is the quiet failure of this journey: the placement looks right, the instruction goes out, and it rests on a number from an earlier day, which is exactly what VR-S9-003-1 refuses with MSG-P1-001.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13); there is no in-process call and no second hop. ACE data reaches the run only through P1's published contract (DP-05), never by reading `v_ace_score` in a query of the harness's own, and DP-01 forbids reading another service's schema at all. The decision record is written by S9 through the local decision-record library on rwb.decision-record.v1 (DP-03) and confirmed by the central ledger in rwb-decision (ADR-022); the harness reads it back through P7's contract. On the edge, DP-19 sends partners through the **partner gateway** (FAPI 2.0) that fronts rwb-partner, and reserves gateway-bff composite routes for staff screens; the run calls S9's own operation at the service boundary, which is the operation the partner gateway fronts.

One limit is stated plainly because it shapes the whole run. The Ownership Map publishes one placement operation, `POST /cases/{caseId}/instructions`, described as "Issue an instruction to a partner by rule", and it publishes `GET /partner/instructions`. It publishes no scorecard read and no allocation read of its own. The harness therefore reads the pick from the instruction, the measured return from DP08 and the score from DP11, and it never invents an allocation endpoint to make an assertion look cleaner. The `InstructionRequest` body shape is not published either, so the body the run sends is held in the fixture from S9's CON story and is asserted only for the fields the published response returns.

### 3. Preconditions

- The published contracts of S9 rwb-partner (the placement and the instruction read), P1 rwb-source-data (DP08 and DP11 records and the freshness read), P3 rwb-case (the case), P7 rwb-decision (the decision log) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- S9 owns the panel, the partner users and the instructions in `rwb_partner` (Arch v5 slide 41, line 2891), so the instruction this run asserts and the pick it records have one named owner before any value is compared.
- The placement and the scorecard evaluation are RWB-S9-E6031-APP until it lands; until then the partner fixture of §12.8 stands in for its effect and the story is reported as a stub pass.
- FEAT-PRM-03 Allocate work by measured return is the S9 feature, with FEAT-PRM-02 Hold the partner panel and fee schedule as data as its prerequisite (Epics 3 to 8 Specification v3, lines 135 and 136).
- The scorecard and the panel are versioned data read from reference data **with their version**, so a pick is recorded against the version it was taken under and not against "current" (BR-S9-003, FSD S9 A2.3.3.1).
- The rules the placement answers to are R-WO-30 (place with the agency chosen on measured return, send the instruction the same day on the portal), R-WO-31 (no agency on the panel has capacity, hold and escalate on the timer), R-UNI-25, R-UNI-26, R-UNI-27, R-UNI-29 (a conduct breach suspends allocation) and R-UNI-45 (re-select and re-issue with the clock restarted).
- The right on the placement is **Partner portal C** as API-S9-002 declares it, and the instruction read is **Partner portal R** as API-S9-003 declares it (TSD S9 T-A.1 and T-A.2).
- The synthetic partners, the two cases, the instruction keys, the scorecard version, the business date and the next business date, the measured-return values, the capacity state, the freshness cut-off, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0461; ASM-0653).
- The synthetic partners, cases, instruction keys, scorecard version and measured-return values are held in the fixture as data, never written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S9-E6031-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: runs preflight. It reads the eight contracts, pins each version in the run report, resets the fixture and the freshness switch, and stops the run before any assertion if a contract is missing or a pinned version has moved. The environment, base hosts, fixture layout, scorecard version, freshness cut-off, evidence format and retention and the wave 4 entry gate are agreed at the wave 4 entry check, where a stub pass is never a real pass (GAP-0461).
2. Harness: loads the fixture: cases `RW-2027-000831` and `RW-2027-000832` both at `PLACEMENT_DECIDED` with instruction type `COLLECT`, partners `PRT-SYN-0031-A` and `PRT-SYN-0031-B` on the panel with capacity, partner `PRT-SYN-0031-C` on the panel with no capacity, and the measured return for business date `2027-04-30` held so that A ranks first.
3. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP11/records?caseId={caseId}` and asserts the score the pick will rest on, then reads `GET /api/recovery/source-data/v1/data-products/freshness?product=DP11` and asserts `status` `LOADED`, `businessDate` `2027-04-30` and `loadedAt`, the load time of the 08:00 daily refresh (AC2, AC4).
4. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP08/records?caseId={caseId}` for the three partners and asserts the measured return the pick rests on, as the published product carries it, refreshed on change (AC2).
5. Harness: places the work on the first case through `POST /api/recovery/partner/v1/cases/{caseId}/instructions` with one Idempotency-Key, as a caller holding Partner portal C, and asserts the answer names partner A (AC2).
6. Harness: reads `GET /api/recovery/partner/v1/partner/instructions` and asserts one instruction with its instruction type `COLLECT`, its partner A, its `instructed_at`, its `due_at` and its status `SENT` (AC2, AC5).
7. Harness: places the work on the second identical case and asserts the same partner A, which is the proof that the pick is not a rotation; it then reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry per placement, each naming the pick, the scorecard version and the rule id (AC2, AC3).
8. Harness: replays the first placement with the same Idempotency-Key, asserts the first answer is returned unchanged and one instruction remains, counts one `rwb.partner.InstructionIssued.v1` per placement on `rwb.partner.events.v1`, and observes `InstructionWorkflow` on `rwb-partner` with one partner SLA timer for the instruction type (AC3, AC5).
9. Harness: resets the fixture to its pre-placement snapshot and moves the measured return so that B ranks first for the next business date, then places the same case again and asserts the pick follows B; the next business date is held in the fixture and is Not specified in the source documents (GAP-0461; ASM-0653) (AC3).
10. Harness: runs the no-capacity variant with C only, and asserts the placement is held under R-WO-31 with the case read unchanged at `PLACEMENT_DECIDED` through `GET /api/recovery/case/v1/cases/{caseId}` and a decision entry naming the hold (AC2).
11. Harness: makes DP11 stale after a late or failed ACE batch for its source and places the work again; the answer must carry MSG-P1-001 with the product and the date substituted, no instruction may be read and no `InstructionIssued` may be published (AC4).
12. Harness: resets the product and turns the fault switch on the decision-record hop, places the work under a new Idempotency-Key, and asserts the answer carries MSG-P7-003 with no instruction, no event and the case unchanged; the switch is reset before the next run (AC6).
13. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic RW-CASEOWN caller holding Partner portal R and not C, places the work, and asserts 403 with MSG-P4-002 and no instruction; then it writes one run report per case, keyed by story and case id (AC7).

### 5. Exception paths

| ID | Covered by | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|---|
| X1 | AC2 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E6-031-01-ITG (ITG AC2) |
| X2 | AC2, AC3 | The pick is not the top-ranked partner on the measured return, or two identical cases are split across two partners | The run fails on AC2 and AC3 and the report names both picks, their DP08 measured return, their DP11 score and the two decisions | None | TC-E6-031-01-ITG (ITG AC3) |
| X3 | AC3 | The pick does not follow a change in the measured return, and the same partner is picked again | The run fails on AC3 and the report names the old pick, the new measured return, the partner the product ranks first and the partner the instruction names | None | TC-E6-031-01-ITG (ITG AC3) |
| X4 | AC5 | A second instruction is created for one placement, or a replay publishes a second event or starts a second clock | The run fails on AC5 and the report names both instruction ids, the Idempotency-Key each carried, both event ids and both workflow runs | None | TC-E6-031-01-ITG (ITG AC5) |
| X5 | AC2, AC5 | The decision record is written twice, written without its scorecard version, or the central ledger has not confirmed it | The run fails on AC2 and AC5 and the report names the entries, the scorecard version each carries and the missing confirmation | MSG-P7-003 (expected only where the record cannot be confirmed) | TC-E6-031-01-ITG (ITG AC2, AC5) |
| X6 | AC4 | A placement is made on a stale score product | The run fails on AC4 unless the answer carries MSG-P1-001 with the product and the date, and no instruction and no event exist | MSG-P1-001 (expected, and missing) | TC-E6-031-04-ITG (ITG AC4) |
| X7 | AC6 | A forced decision-record failure leaves an instruction, an event or a case change, or answers without MSG-P7-003 | The run fails on AC6 and the report names the instruction count, the event count and the case read before and after | MSG-P7-003 (expected, and missing) | TC-E6-031-02-ITG (ITG AC6) |
| X8 | AC7 | A caller without Partner portal C is allowed to place work | The run fails on AC7 and the report names the caller role, the right, the operation and the answer; a 200 is a failure even when nothing was written | MSG-P4-002 (expected, and missing) | TC-E6-031-03-ITG (ITG AC7) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S9-E6031-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic partners and keys, the measured-return values, the scorecard version, the freshness cut-off, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | Proves across services that work reached the partner the scorecard picks, that the pick tracked the measured return and not a rotation, and that a stale score product and a refused or failed placement changed nothing |
| Estimable | One runner, one stub set, one scorecard and capacity fixture, two placements, one capacity probe, one freshness probe, one decision probe, one event observer, one workflow observation, one access probe and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion is asserted on an observable: an instruction, its partner and status, a DP08 record, a DP11 record, a freshness stamp, a decision entry with its scorecard and rule version, an event count, a workflow timer and a response code |

### 7. Acceptance criteria

```gherkin
Feature: Allocate work by measured return - wave 4 integration harness

  Background:
    Given the synthetic partners "PRT-SYN-0031-A" and "PRT-SYN-0031-B" are on the panel with capacity and partner "PRT-SYN-0031-C" is on the panel with no capacity
    Given the cases "RW-2027-000831" and "RW-2027-000832" are in PLACEMENT_DECIDED with no instruction
    Given the measured return for business date "2027-04-30" is held in the fixture so that "PRT-SYN-0031-A" ranks first
    Given the rule package in force holds R-WO-30, R-WO-31 and R-UNI-29 with its rule version and the scorecard and the panel are versioned reference data

  Scenario: AC1 Allocate work by measured return (legacy RWB-E6-031 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then places work with the partner the scorecard rule picks, not by rotation or habit
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The instruction names the partner the scorecard picks (new, D-RCV-60)
    Given the fixture holds the measured return of the three partners for business date "2027-04-30" and the scorecard version in force
    When the work is placed on case "RW-2027-000831" through POST /api/recovery/partner/v1/cases/{caseId}/instructions with one Idempotency-Key
    Then the answer names partner "PRT-SYN-0031-A" and one instruction of type COLLECT with status SENT
    And GET /api/recovery/source-data/v1/data-products/DP08/records?caseId={caseId} carries the measured return of "PRT-SYN-0031-A"
    And GET /api/recovery/source-data/v1/data-products/DP11/records?caseId={caseId} carries the score the pick rests on
    And GET /api/recovery/source-data/v1/data-products/freshness?product=DP11 answers `status` "LOADED", `businessDate` "2027-04-30" and its `loadedAt`
    And GET /api/recovery/decision/v1/decision-log?caseId={caseId} holds one entry naming the pick, the scorecard version and the rule id
    When no agency on the panel has capacity and the work is placed with partner "PRT-SYN-0031-C" only
    Then the placement is held under R-WO-31 and no instruction is created
    And GET /api/recovery/case/v1/cases/{caseId} reads the case unchanged at PLACEMENT_DECIDED
    And the decision log holds one entry naming the hold

  Scenario: AC3 The pick follows the measured return and not a rotation (new, D-RCV-60)
    Given the measured return for business date "2027-04-30" is held so that "PRT-SYN-0031-A" ranks first
    When the identical work is placed on case "RW-2027-000832"
    Then the same partner "PRT-SYN-0031-A" is picked and not the next partner by rotation
    And the decision log holds one entry per placement, each naming the same scorecard version
    When the fixture is reset and the measured return is moved so that "PRT-SYN-0031-B" ranks first for the next business date
    Then the next placement picks "PRT-SYN-0031-B"
    And no placement in the run is made by rotation, habit or a fixed share

  Scenario: AC4 A stale score product stops the placement (new, D-RCV-60)
    Given the rwb-source-data (P1) freshness stub answers DP11 with `status` "STALE", naming the product and the date it is from
    When the work is placed through POST /api/recovery/partner/v1/cases/{caseId}/instructions
    Then the answer carries "MSG-P1-001" with the product and the date substituted
    And no instruction is read through GET /api/recovery/partner/v1/partner/instructions
    And no "rwb.partner.InstructionIssued.v1" is published
    And the case is read unchanged at PLACEMENT_DECIDED

  Scenario: AC5 One placement carries one instruction, one partner clock and one event (new, D-RCV-60)
    Given the placement of case "RW-2027-000831" is accepted and carried one Idempotency-Key
    When the same placement is replayed with the same Idempotency-Key
    Then GET /api/recovery/partner/v1/partner/instructions answers one instruction with its instructed_at, its due_at and status SENT
    And "rwb.partner.InstructionIssued.v1" is published once per placement on "rwb.partner.events.v1"
    And InstructionWorkflow on "rwb-partner" holds one partner SLA timer for the instruction type
    And the replay adds no instruction, no event and no second clock

  Scenario: AC6 A forced decision-record failure stops the placement with nothing issued (new, D-RCV-60)
    Given the decision record cannot be written for the placement
    When the work is placed through POST /api/recovery/partner/v1/cases/{caseId}/instructions
    Then the answer carries "MSG-P7-003"
    And no instruction is read through GET /api/recovery/partner/v1/partner/instructions
    And no "rwb.partner.InstructionIssued.v1" is published
    And the case is read unchanged at PLACEMENT_DECIDED

  Scenario: AC7 A caller without Partner portal C is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-CASEOWN" holding Partner portal R and not Partner portal C
    When the caller places the work through POST /api/recovery/partner/v1/cases/{caseId}/instructions
    Then the answer is 403 with "MSG-P4-002"
    And no instruction is created and no case state changes

  Scenario: AC8 The measured return and the score are read only through rwb-source-data, one REST call per hop (new, D-RCV-60)
    When the work is placed through POST /api/recovery/partner/v1/cases/{caseId}/instructions
    Then the measured return and the score are read only through DP08 and DP11 and never from "v_ace_score" or another service's schema
    And every hop is one REST call on the owner's base with a 2 s timeout and no second hop

  Scenario: AC9 A duplicate delivery of a consumed event starts no second clock (new, D-RCV-60)
    Given a consumed event on "rwb.partner.events.v1" is delivered twice
    Then the duplicate adds no instruction, no event and no second partner clock

  Scenario: AC10 A consumed call that fails or does not answer stops the placement with nothing issued (new, D-RCV-60)
    Given a consumed call to rwb-source-data or rwb-decision fails or does not answer within 2 s
    When the work is placed through POST /api/recovery/partner/v1/cases/{caseId}/instructions
    Then no instruction is read through GET /api/recovery/partner/v1/partner/instructions
    And no "rwb.partner.InstructionIssued.v1" is published
```

Legacy AC1 is the only legacy criterion this story owns, and it is the business outcome the S9 allocation has to reach: the work goes to the partner the scorecard picks and the decision log carries the rule version. Legacy AC2 (the decision log cannot be written, nothing changes) stays with RWB-S9-E6031-APP as its build criterion and is asserted here across the boundary in AC6, where the instruction, the event and the case state are read before and after the refused placement. The measured return and the score are read as data products through P1's contract — DP08 and DP11 — and never from `v_ace_score` or another service's schema.

### 8. Business rules

| ID | Covered by | Rule | Source |
|---|---|---|---|
| BR1 | AC2, AC3 | Work is allocated to partners by measured return against a scorecard, not by a fixed share | REQ-S9-003 |
| BR2 | AC2 | Where `placement_type = soft_recovery` and an agency on the panel has capacity, the account is placed with the agency chosen on measured return and the instruction is sent the same day on the portal | R-WO-30 |
| BR3 | AC2 | Where no agency on the panel has capacity, the placement is held and escalated on the timer, and no instruction is issued to keep a queue moving | R-WO-31 |
| BR4 | AC4 | A data product that is stale after a late or failed ACE batch for its source refuses the placement, and the answer names the product and the date it is from | VR-S9-003-1; MSG-P1-001 |
| BR5 | AC2, AC3 | No value a business person may change is written in code: the panel, the scorecard and the service levels are read from reference data with their version, and the decision entry names the scorecard version the pick was taken under | BR-S9-003 (FSD S9 A2.3.3.1) |
| BR6 | RWB-S9-E6031-APP (not asserted in this story) | A partner that misses its service level on the portal is chased once, then the work is recalled and re-selected on the scorecard | R-UNI-25 |
| BR7 | RWB-S9-E6031-APP (not asserted in this story) | A panel exit or the end of a contract recalls every open case held by that partner and re-selects, so a recalled case never stays with the exiting firm | R-UNI-26 |
| BR8 | RWB-S9-E6031-APP (not asserted in this story) | A declared conflict of interest withdraws the instruction and re-selects the next partner on the scorecard | R-UNI-27 |
| BR9 | RWB-S9-E6031-APP (not asserted in this story) | An upheld conduct or complaint breach suspends allocation and recalls the affected cases, and a re-selected partner gets the instruction re-issued with the partner clock restarted | R-UNI-29; R-UNI-45 |
| BR10 | AC2, AC4, AC8 | The measured return is read as DP08 Partner performance (refreshed on change) and the score as DP11 Scores and route economics (daily at 08:00), both through rwb-source-data's contract; the run never reads `v_ace_score` directly and no service reads another service's schema | DP-05; DP-01; FSD P1, lines 290 and 293 |
| BR11 | AC5, AC6, AC8 | The decision record is written by S9 through the local decision-record library on rwb.decision-record.v1 and confirmed by the central ledger, so nothing is placed when it cannot be recorded; every hop is one REST call on the owner's base with a 2 s timeout and no second hop | DP-03; ADR-022; DP-11; DP-13 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E6031-APP, the panel and the scorecard are versioned reference data in S9, the case is P3's, the decision log is P7's and the session is P4's. Reference data read: the panel, the scorecard version and the service levels, read through the reference-data contract (DP-06, DP-07).

### 9. State transitions

| From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|
| PLACEMENT_DECIDED | SOFT_RECOVERY_SELECTED | `placement_type = soft_recovery` and an agency on the panel has capacity | PLACED_WITH_AGENCY | S7 rwb-writeoff rules component moves the case stage under R-WO-30; S9 rwb-partner writes the instruction through InstructionWorkflow `issueInstruction` and publishes `rwb.partner.InstructionIssued.v1` |
| PLACEMENT_DECIDED | NO_AGENCY_CAPACITY | no agency on the panel has capacity | PLACEMENT_DECIDED, held | S7 rwb-writeoff rules component under R-WO-31; S9 writes no instruction and the hold is recorded in the decision log |
| PLACEMENT_DECIDED | none | the placement is refused for want of Partner portal C, MSG-P1-001 or MSG-P7-003 | PLACEMENT_DECIDED, unchanged | S9 rwb-partner refuses before any write; the rule engine is not reached |
| PARTNER_RECALLED | PARTNER_RESELECTED | the next partner is selected on the scorecard | ROUTE_D6_REOPEN, then PLACED_WITH_AGENCY on re-issue | Partner and agency manager under R-UNI-45; S9 re-issues the instruction and restarts the clock |
| PARTNER_RECALLED | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld against the partner | allocation suspended, cases recalled | Partner and agency manager under R-UNI-29 |
| Instruction `SENT` | partner acceptance on the portal | the partner accepts the instruction | `ACCEPTED` | S9 rwb-partner, InstructionWorkflow |
| Instruction `ACCEPTED` | result recorded or timer expiry | the result is recorded, or the partner misses the service level | `DONE` or `RECALLED` | S9 rwb-partner, InstructionWorkflow; R-UNI-25 |

The case stages are the rule table's own from-states and to-states, and the harness sets none of them: it reads the case through P3's contract before and after every attempt and asserts it is unchanged where the rule says the placement is held or refused. The instruction statuses are S9's own LOV values `SENT`, `ACCEPTED`, `DECLINED`, `IN_PROGRESS`, `DONE` and `RECALLED` (TSD S9 T3.2), and the run asserts only `SENT` on a fresh placement. The harness changes no state; every change in the table belongs to S9 or to the rule engine under the write-off legacy key.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG Partner and agency manager | Holds Partner portal CRUDA and is the primary role of the journey and of the placement it asserts |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT and PT-AGENCY | Hold Partner portal C (or RU on the portal for the partner user) per the TSD RBAC matrix, and are the other callers the placement accepts |
| RW-CASEOWN Case owner | Holds Partner portal R and not C, and is the refused caller of AC7 |
| RW-TEAMMGR, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL, RW-TRIBE, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC | Hold Partner portal R and read the partner and the instruction; the run records the right each operation answered with |
| QA lead | Owns the harness configuration, the fixture, the freshness switch, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S9 holds the panel, the partner users and the instructions and runs InstructionWorkflow, P1 holds DP08 and DP11 and the freshness stamp, P3 holds the case, P7 holds the decision log and the central ledger, P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's, so no delegation level is asserted here |

### 11. Data

| BR Field ID | Entity | Field | Owner | Read or write |
|---|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end, score | S9 rwb-partner | Read through the S9 contract and through DP08 |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | S9 rwb-partner | Written only by S9's placement; read through the instruction read and DP08 |
| DF-WRK-009 to DF-WRK-016 | assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at, reason, rule_id | P3 rwb-case | Read through the P3 contract; not written by the harness |
| DF-WRK-001 to DF-WRK-008 | queue | id, queue_code, queue_name, team_code, role_code, assignment_method, capacity_cap, overflow_queue_id | P3 rwb-case | Read through the P3 contract |
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, status, stage_code, primary_person_key and the case attributes | P3 rwb-case | Read through the P3 contract before and after every attempt |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version, entry_hash | P7 rwb-decision | Read through the P7 contract |
| DF-REF-001 to DF-REF-015 | rule_row | id, rule_id, rule_version, route_set, from_state, event_code, test_case_id | P7 rwb-decision | Read through the P7 contract |
| DF-ACE-270 to DF-ACE-279 | v_ace_score behind DP11 | score_key, account_key, model_code, model_version, score_value, estimate_value, route_code, scored_at, source_system, data_as_of | P1 rwb-source-data, over the ACE view | Read only through DP11; never read directly |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The partner and the instruction are S9's in `rwb_partner`; the case, the assignment and the queue are P3's in `rwb_case`; the decision entries and the rule rows are P7's in `rwb_decision`. The ACE score fields sit behind `v_ace_score` and reach the run only as DP11 Scores and route economics through P1's contract, which is the only way a caller outside P1 may see them (DP-05). The queue's own `assignment_method` carries `ROUND_ROBIN` as a staff-queue default, and the partner pick is not that mechanism: the run proves the partner is chosen on measured return while the queue's staff allocation stays what it is. The harness owns no table and writes no row; the only change it drives is S9's own placement operation of §12.2, and everything else it reads is a contract read. Personal data: `primary_person_key` in DF-CAS-001 to DF-CAS-023 is personal data; the run reads it through the P3 contract and writes none.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/partner/v1/cases/{caseId}/instructions` | S9 rwb-partner | Issues the instruction to the partner chosen by rule, with one Idempotency-Key; the accepted, the held, the stale, the failed and the refused operation of the run (AC2, AC3, AC4, AC5, AC6, AC7) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The one instruction, its instruction type, its partner, its instructed_at, its due_at and its status (AC2, AC4, AC5, AC6) |
| GET | `/api/recovery/source-data/v1/data-products/DP08/records?caseId={caseId}` | P1 rwb-source-data | DP08 Partner performance, refreshed on change, carrying the measured return the pick rests on (AC2, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/DP11/records?caseId={caseId}` | P1 rwb-source-data | DP11 Scores and route economics, daily at 08:00, carrying the score the pick rests on (AC2, AC4) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP11` | P1 rwb-source-data | The business date and the load time of the score product, and the stale state that stops the placement (AC2, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case status and stage at `PLACEMENT_DECIDED`, before and after the held, the stale, the failed and the refused attempts (AC2, AC4, AC6, AC7) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | One entry per placement, naming the pick, the scorecard version and the rule id, and one entry naming the hold (AC2, AC3, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a placement (AC7) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation in the Ownership Map. The map publishes no allocation read and no scorecard read, so the pick is asserted through the instruction S9 issues, the measured return through DP08 and the score through DP11, and the harness never calls an endpoint the map does not publish. The `InstructionRequest` body shape is not published either; the body the run sends is held in the fixture from S9's CON story, and only the fields the published `PartnerInstruction` response returns are asserted. For a partner the edge path to the portal operations is the partner gateway (FAPI 2.0) that fronts rwb-partner, and for a staff screen the same values would be composed by a gateway-bff composite route (DP-19); the run itself calls the service boundary the gateway fronts.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | S9 rwb-partner | Counts one publication per placement, proves a replay adds none, and carries the partner clock the partner portal consumes (AC5) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | S9 rwb-partner through the local decision-record library (DP-03) | Proves the placement decision and its scorecard and rule version were published once and confirmed by the central ledger, and that the forced failure publishes none (AC2, AC5, AC6) |

The harness subscribes to both topics under one consumer group of its own and replays the instruction event once. `InstructionIssued` is EV-20 in the event catalogue with the partner portal as its consumer (Arch v5 slide 43, row 20, line 2946); the run counts the publication and reads the portal effect through the instruction read of §12.2, because the partner portal exposes no operation of its own to this story.

#### 12.5 Workflows and activities

None added. The harness exercises `InstructionWorkflow`, S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace, through the placement: its `issueInstruction` activity issues the instruction and starts the partner SLA timer for the instruction type, and both are read in the workflow history (Arch v5 slide 17, line 1247; Temporal design slide 25, step 3 and the clocks at lines 1742 to 1745). It observes CaseWorkflow on `rwb-case` as the parent that holds the case the placement acts on, and observes it only: the placement does not signal it and moves no case state. Neither workflow, activity nor Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added, and none needed. The scorecard is refreshed by its own product — DP11 daily at 08:00 and DP08 on change — and the partner clock is a durable workflow timer, so nothing in the journey is on a cron: the harness starts each run itself and holds the business date in the fixture. JOB-05 Timer check is retired in favour of durable timers inside the workflows (Arch v5 slide 44), and the partner SLA is read as a timer on `InstructionWorkflow`, not as a scheduled job.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): partner, partner_user and partner_instruction are S9's in `rwb_partner`, assignment, recovery_case and queue are P3's in `rwb_case`, decision_log_entry and rule_row are P7's in `rwb_decision`, and DP08 and DP11 are P1's published products.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (S9) | `POST /cases/{caseId}/instructions`, `GET /partner/instructions` | Partners `PRT-SYN-0031-A` and `PRT-SYN-0031-B` with panel status `ACTIVE` and capacity; partner C with no capacity; a placement accepted once per Idempotency-Key with partner A, instruction type `COLLECT` and status `SENT`; the same instruction returned on a replay of the key; a held placement under R-WO-31 with no instruction; a stale answer carrying MSG-P1-001; with the fault switch on, an answer carrying MSG-P7-003 and no instruction |
| Stub for rwb-source-data (P1), DP08 | `GET /data-products/DP08/records?caseId={caseId}` | The three partners and their measured return for business date `2027-04-30` as the published product carries them, refreshed on change, with A ranked first and, on the next business date, B ranked first |
| Stub for rwb-source-data (P1), DP11 | `GET /data-products/DP11/records?caseId={caseId}` | The score, expected return and route code of each partner as the published product carries them, daily at 08:00, with its `data_as_of` |
| Stub for rwb-source-data (P1), freshness | `GET /data-products/freshness?product=DP11` | `status` `LOADED`, `businessDate` `2027-04-30` and `loadedAt` on a fresh run, and a `status` `STALE` answer naming the product and the date it is from on the stale run |
| Stub for rwb-case (P3) | `GET /cases/{caseId}` | Cases `RW-2027-000831` and `RW-2027-000832` at `PLACEMENT_DECIDED`, with the same status and stage before and after every attempt |
| Stub for rwb-decision (P7) | `GET /decision-log?caseId={caseId}` | Exactly one entry per placement, naming the pick, the scorecard version and the rule id; one entry naming the hold; nothing after the stale, the forced failure or the refusal; the central ledger confirmation once |
| Stub for rwb-access (P4) | `GET /me/session` | Allows RW-AGENCYMG with Partner portal CRUDA and the other holders of C where the run needs them; refuses RW-CASEOWN with 403 and MSG-P4-002 on the placement |
| Scorecard and capacity fixture | The panel, the scorecard version and the capacity state | The three partners, their panel status, their capacity, their measured return for the two business dates and the scorecard version in force, held as data with the `InstructionRequest` body from S9's CON |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic partners, cases and instruction keys, the scorecard version, the measured-return values, the capacity state, the business date and the next business date, the freshness cut-off, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0461; ASM-0653).

The fake library version the stub set is published from is Not specified in the source documents (DOR-RWB-ITG-E6031-ITG-22). Each stub carries that version in the run report beside the contract version it was generated from, so the published fake, the contract and the pin are recorded together for the wave entry check, and a fake regenerated from a moved contract shows up as a run failure rather than a silent pass.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.partner.InstructionIssued.v1` and `rwb.decision.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; InstructionWorkflow on `rwb-partner` exercised through the placement, with its partner SLA timer and its `issueInstruction` activity, and CaseWorkflow on `rwb-case` observed as the parent that holds the case |
| File | None. The placement body is S9's own request and the report is the harness's own output; no file or claim-check is transferred by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery-w4/partner-allocation`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None. DP-05 adds nothing: the legacy story's `v_ace_score` read becomes DP11 Scores and route economics through P1's contract, and nothing in the harness reads the view. DP-13 adds nothing: the partner paths are rewritten onto S9's own base and there is no shared base left. DP-19 has two edges in this journey and the run names both: for the **partner** the route is the **partner gateway** in the DMZ under FAPI 2.0, which fronts rwb-partner (Arch v5 slide 17, line 1251, and slide 20, line 1458), and **gateway-bff** composes the **staff** screens only, including SCR-35 Placement and allocation. The one blocking dependency is the I story RWB-S9-E6031-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the seven criteria in order for one case and holds the run lock, the fixture reset and the freshness switch |
| ScoreboardReadBack | Service | Reads DP08 and DP11, names the measured return and the score of each partner, and holds the ranking for the business date |
| FreshnessProbe | Service | Reads the DP11 freshness stamp, asserts the business date and the load time, and turns the product stale for AC4 |
| PlacementDriver | Service | Places the work once per Idempotency-Key through S9's operation and holds the accepted, the held, the stale, the failed and the refused attempt |
| InstructionReadBack | Service | Reads the instruction, its partner, its type, its `instructed_at`, its `due_at` and its status |
| RotationProbe | Service | Places the second identical case, compares the two picks, and moves the measured return for the next business date |
| CapacityProbe | Service | Runs the no-capacity variant with partner C and asserts the hold under R-WO-31 |
| DecisionProbe | Service | Reads the entries, the scorecard version and the rule id, reads the published decision record, and holds the fault switch |
| EventProbe | Service | Subscribes to `rwb.partner.events.v1` and `rwb.decision-record.v1`, counts publications and replays the instruction event once |
| WorkflowProbe | Service | Observes InstructionWorkflow in the `rwb-recovery` namespace, its partner SLA timer and its `issueInstruction` step, and observes CaseWorkflow only |
| AccessProbe | Service | Reads the session and drives the refused placement of AC7 |
| EvidenceReport | Service | Writes one report per case, keyed by story and case id, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stub set from Day 1 and the real services as RWB-S9-E6031-APP lands, on the synthetic partners `PRT-SYN-0031-A`, `PRT-SYN-0031-B` and `PRT-SYN-0031-C`, the cases `RW-2027-000831` and `RW-2027-000832`, instruction type `COLLECT`, business date `2027-04-30` and the next business date in the fixture. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the scorecard version, the measured-return values, the capacity state, the freshness cut-off, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0461; ASM-0653).

**Build steps**

1. Generate the stub set and the scorecard and capacity fixture from the published contracts, pin each contract version in the run report, and fail the run on a mismatch (X1).
2. Build the ScoreboardReadBack and the FreshnessProbe: DP08 carries the measured return, DP11 carries the score, and the freshness read answers the business date `2027-04-30` with its load time (AC2, AC4).
3. Add the PlacementDriver: one placement on the first case with one Idempotency-Key, and the answer naming partner A (AC2, X2).
4. Add the InstructionReadBack: one instruction of type `COLLECT`, partner A, its `instructed_at`, its `due_at` and status `SENT` (AC2, AC5).
5. Add the DecisionProbe: one entry per placement naming the pick, the scorecard version and the rule id, one published decision record and the central ledger confirmation, and no second entry after a re-read (AC2, AC5, X5).
6. Add the RotationProbe: the second identical case picks A, and after the fixture reset the next business date picks B (AC3, X2, X3).
7. Add the EventProbe and the WorkflowProbe: one `InstructionIssued` per placement, one partner SLA timer, and a replay that adds no instruction, no event and no second clock (AC5, X4).
8. Add the CapacityProbe for the hold: partner C only, the case read unchanged at `PLACEMENT_DECIDED`, and a decision entry naming the hold under R-WO-31 (AC2).
9. Add the three negative paths — the stale product with MSG-P1-001, the forced decision-record failure with MSG-P7-003, and the caller without Partner portal C with 403 and MSG-P4-002 — then add the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S9-E6031-APP lands (AC4, AC6, AC7, X6, X7, X8).

**Feature switch.** None. The harness has no production flag; the freshness switch and the fault switch of steps 8 and 9 exist in the test environment only and are reset by the runner before and after each run.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S9-E6031-APP when it lands, and the wave entry check holds a run report keyed by story and case id.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message text of MSG-P1-001 is copied word for word from Error and Message Standard v4 section 4; the FSD S9 row (FSD S9 A2.3.3.1, line 289) differs and is not used; MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are copied word for word from the legacy story's validation table (lines 12045 to 12051). The harness asserts the message ID and the substituted values it reads on the answer, and owns no message text: MSG-P1-001 with the product `DP11` and the date it is from when the score product is stale (AC4, X6), MSG-GEN-001 with the missing field when a placement is made short of a required parameter (X1), MSG-P4-002 with the refused action when the caller holds Partner portal R and not C (AC7, X8), and MSG-P7-003 when the decision record cannot be written and nothing is placed (AC6, X7).

### 15. Screens and states

The legacy story's screens are SCR-34 Partner list and SCR-35 Placement and allocation, and neither is built or rendered here: the harness calls the placement and the instruction read behind them and reads the states through the owners. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0461; ASM-0653).

| State | Read through | What the run asserts |
|---|---|---|
| PLACEMENT_DECIDED | P3 case read, DP08 and the instruction read | The case is at the stage the rule table gives, no instruction exists, and the measured return of the three partners is present |
| PLACED_WITH_AGENCY | S9 instruction read, the decision log and the InstructionWorkflow history | One instruction of type `COLLECT` with partner A, its `instructed_at`, its `due_at` and status `SENT`, one decision entry naming the pick and the scorecard version, and one SLA timer running |
| The held placement | P3 case read, the decision log and the instruction read | The case is unchanged at `PLACEMENT_DECIDED`, no instruction exists, and one decision entry names the hold under R-WO-31 |
| The stale product | P1 freshness read, the S9 answer and the instruction read | The freshness read names the product and the date it is from, the answer carries MSG-P1-001, and no instruction and no event exist |
| A refused or failed placement | P4 session read, S9 answer, P7 decision log, the event count and the case read | 403 with MSG-P4-002 or MSG-P7-003, no instruction, no event and no state change |

SCR-34 Partner list and SCR-35 Placement and allocation belong to the S9 stories of the legacy key, and neither is built or read here. The partner reaches the portal operations through the partner gateway and a staff member reaches the placement screen through a gateway-bff composite route (DP-19); this harness renders neither and asserts the operations behind them. The SCR-34 loading state is taken from Screen Specifications v1; its empty, error and no access states are Not specified in the source documents (CG-ALL-1129). The SCR-35 loading state is taken from Screen Specifications v1; its empty, error and no access states are Not specified in the source documents (CG-ALL-1130).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-031-01-ITG | AC1 (legacy); ITG AC2, AC3 and AC5 | End to end | Partners `PRT-SYN-0031-A` and `PRT-SYN-0031-B` with capacity and `PRT-SYN-0031-C` without, cases `RW-2027-000831` and `RW-2027-000832` at `PLACEMENT_DECIDED`, business date `2027-04-30`, one placement per case, one replay, the next business date after the fixture reset |
| TC-E6-031-02-ITG | The not-recorded path across the boundary (legacy AC2); ITG AC6 | Integration | A forced decision-record failure before the placement, with the instruction, the event and the case read before and after |
| TC-E6-031-03-ITG | Access; ITG AC7 | Component | A synthetic RW-CASEOWN caller holding Partner portal R and not C, and the placement operation of API-S9-002 |
| TC-E6-031-04-ITG | Principle 5 and the freshness gate; ITG AC4 | Integration | the rwb-source-data (P1) freshness stub answers DP11 stale, its freshness stamp, the placement answer and the absence of the instruction and the event |
| TC-E6-031-05-ITG | ITG AC8 (BR10, BR11) | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E6031-ITG-AC8) |
| TC-E6-031-06-ITG | ITG AC9 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E6031-ITG-AC9) |
| TC-E6-031-07-ITG | ITG AC10 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E6031-ITG-AC10) |

The AC column names the legacy test each copy derives from: TC-E6-031-01-ITG from TC-E6-031-01 (AC1 Allocate work by measured return), TC-E6-031-02-ITG from TC-E6-031-02 (AC2 Not recorded), TC-E6-031-03-ITG from TC-E6-031-03 (Access) and TC-E6-031-04-ITG from TC-E6-031-04 (Principle 5), and the full legacy tests, with their Given, When and Then, are in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. ITG AC2, AC3 and AC5 are asserted inside the run of TC-E6-031-01-ITG, which is the end-to-end case that places the work twice, reads the one instruction per case, counts the one event per placement and moves the measured return; they add no test case ID because the legacy set has four.

### 17. Guardrails

- No business value in code: the synthetic partners, the cases, the panel and capacity state, the measured-return values, the scorecard version, the business dates, the freshness cut-off, the switches and the report layout are data.
- No personal data in logs, events, workflow inputs or reports: every key is synthetic, the partner is read by code and the case by case number, and the events carry IDs and facts only.
- Service data only through the owner's contract: the partner and the instruction from S9, DP08, DP11 and the freshness stamp from P1, the case from P3, the decision log and the rule rows from P7, the session from P4; never a direct schema read and never another service's table (DP-01, DP-05).
- **DP-05 is explicit here:** the score is read through DP11 and never from `v_ace_score`, and no service reads another service's schema; the same rule covers DP08, the measured return.
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented operation: only the one placement and the seven reads of §12.2, and the pick is never asserted through an allocation or scorecard read the map does not publish.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The freshness switch and the fault switch are reset by the runner before and after each run and are never left on, so a forced failure cannot be mistaken for a real one; the harness never runs against UAT or production and never writes a row by hand or sets a state it then asserts.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E6-031 Allocate work by measured return | Recovery Workbench User Stories Epics 3 to 8 v4, lines 11983 to 12062 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 12002 to 12006 | Section 7, AC1, marked (legacy RWB-E6-031 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E6-031-02 | The same, lines 12008 to 12012 and 12058 | AC6 asserts the same failure here; the legacy criterion stays with RWB-S9-E6031-APP (section 19) |
| Legacy data table, including `v_ace_score` DF-ACE-270 to DF-ACE-279 | The same, lines 12014 to 12022 | Section 11 |
| Legacy endpoints | The same, lines 12024 to 12029 | Section 12.2, rewritten onto S9's base; the legacy table names Partner portal R and U only, while API-S9-002 declares C on the placement (GAP-0461) |
| Legacy screens SCR-34 and SCR-35 | The same, lines 12031 to 12036 | Section 15, named and not built |
| Legacy permission checks | The same, lines 12038 to 12043 | Section 10, against the TSD RBAC matrix |
| Legacy messages MSG-GEN-001, MSG-P4-002 and MSG-P7-003 | The same, lines 12045 to 12051 | Section 14, copied word for word |
| Legacy test cases TC-E6-031-01 to TC-E6-031-04 | The same, lines 12053 to 12060 | Copied as -ITG in section 16 |
| FEAT-PRM-03 Allocate work by measured return, with FEAT-PRM-02 as its prerequisite | Epics 3 to 8 Specification v3, lines 136 and 135 | Sections 1, 2 and 19 |
| REQ-S9-003 work is allocated by measured return against a scorecard, not by a fixed share | Business Requirements Program v5, line 432 | Section 8, BR1, and section 2 |
| R-WO-30 place the account with the agency chosen on measured return and send the instruction the same day on the portal | Business Rules and Routing Logic v4, line 361 | Sections 8 and 9, BR2 |
| R-WO-31 no agency on the panel has capacity, hold the placement and escalate on the timer | The same, line 362 | Sections 8 and 9, BR3 |
| R-UNI-29 a conduct breach suspends allocation, and R-UNI-45 re-select and re-issue with the clock restarted | The same, lines 433 and 449 | Section 8, BR9; section 9 |
| FSD S9 A2.3: the step table, VR-S9-003-1 with MSG-P1-001, BR-S9-003, the roles and the two exception criteria | Functional Specifications by Module v7, Recovery Workbench FSD S9 Partner management v3, lines 257 to 326 | Sections 2, 3, 8 and 14 |
| TSD S9 field definitions, LOVs and RBAC matrix | Technical Specifications by Module v6, Recovery Workbench TSD S9 Partner management v2, lines 63 to 106 and 130 to 165 | Sections 9, 10 and 11 |
| TSD S9 API-S9-002 and API-S9-003 with their rights, Idempotency-Key and error lists | The same, lines 197 to 244 | Section 12.2, AC2 and AC7 |
| S9 contract: the staff and portal paths, InstructionWorkflow, `rwb_partner` and `rwb.partner.events.v1` | Architecture v5 slides 17, lines 1245 to 1256 and 1270 to 1272 | Sections 2, 8, 12.2, 12.5 and 12.7 |
| rwb-partner ownership, schema, topic, task queue and wave | Architecture v5 slide 41, line 2891 | Sections 1, 12.7 and 13 |
| InstructionIssued, producer rwb-partner, consumer the partner portal (EV-20) | Architecture v5 slide 43, row 20, line 2946 | Section 12.4, AC5 |
| The edge: partners only through the partner gateway (FAPI 2.0), gateway-bff for staff screens | Architecture v5 slide 17, line 1251, and slide 20, line 1458; DP-19 | Sections 2, 13 and 15 |
| Scorecard picks partner, instruction sent with the partner clock, the SLA and recall clocks, the UNIVERSAL rule package | Temporal and Drools Design v1, slide 25, lines 1663 to 1755 | Sections 2, 9, 12.5 and 13 |
| DP08 Partner performance on change and DP11 Scores and route economics daily at 08:00 | FSD P1 Recovery data engine v3, lines 290 and 293 | Sections 2, 8, 12.2 and 12.8 |
| DP-03, DP-05, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 12.4, 12.2 and 8: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| The seven criteria of this harness and the gap and assumption behind its configuration | This file, sections 3, 7 and 12.8; GAP-0461 and ASM-0653 | Sections 3, 7, 12.8, 13 and 15 |

### 19. Out of scope

- RWB-S9-E6031-CON and RWB-S9-E6031-APP: the scorecard evaluation, the pick of the partner, the placement, the instruction and the decision record inside the service, including legacy AC2 (the not-recorded path), which is its build criterion and which this story asserts only across the boundary in AC6.
- The S9 build as a whole: the panel, the partner users, the instructions, the results, the fees, the scorecards, InstructionWorkflow and its SLA timers, and every S9 CON, APP and DB story of the legacy key.
- The panel and the fee schedule versions (RWB-S9-E6030), which are FEAT-PRM-02 and the prerequisite of this feature.
- The onboarding of a partner and its terms (RWB-S9-E6029).
- The override of an allocation with a reason (RWB-S9-E6032).
- The partner result intake (RWB-S9-E6033).
- The monthly scorecard build and the partner review (FEAT-PRM-08 and FEAT-PRM-10), which publish the scorecard this story reads as data.
- The recall and re-selection paths as products (R-UNI-25 to R-UNI-29, R-UNI-45): the run reads the states and asserts none of the recall steps.
- The DP08 and DP11 product builds in P1, and the ACE batch that feeds DP11.
- SCR-34 Partner list and SCR-35 Placement and allocation, and the partner gateway and the gateway-bff composite routes, which are the portal's and the edge's own product.
- The platform H stories DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, which the platform wave delivers.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
