# RWB-ITG-E6030-ITG Hold the partner panel and fee schedule as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E6030-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP07, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E6030-ITG-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-S9-E6030-CON |
| Integration dependencies | RWB-S9-E6030-APP |
| External dependencies | None |
| Contract version | /v1 (path version of the consumed REST operations, section 12.9) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-030 as the wave 4 integration proof that the partner panel, the fee schedule and the service levels are read as versioned data through rwb-partner, that the list values behind them come from rwb-case's reference-data contract and not from a copy, that a new version leaves an instruction issued under the old version untouched, and that each version carries one decision record with its rule version; the panel and the versions are RWB-S9-E6030-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E6030-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 6 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **reference data administrator**, I want **the partner panel, the fee schedule and the service levels proved end to end on the real services as versioned data: read back through rwb-partner with the version in force for the business date, their list values read through rwb-case's reference-data contract, an instruction issued under one version left untouched when the next version comes into force, and one decision record per version with its rule version**, so that **a placement is priced and timed by the terms that were in force when it was made and no business value is ever written in code**.

This story builds the wave 4 integration harness and its evidence, and nothing else. The partner panel, the fee schedule, the service levels and the versions are built by S9 rwb-partner in RWB-S9-E6030-APP and its CON story; the list values behind them are P3's reference data under the default ruling; the decision record and the central ledger are P7's; the case the instruction sits on is P3's; and the right that answers the read is P4's. The harness loads the fixture, reads the panel and the terms through S9's published operations, resolves every list value through P3's reference-data contract, advances the fixture's business date across a version boundary, reads the decision log and the published decision record, and writes a run report per version. It provides no endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

Partners are instructed and paid by email and spreadsheet today, and the fee is worked out by hand. A fee schedule that lives in a spreadsheet cannot be defended a year later: nobody can say which rate applied on the day the work was placed, and the person who maintained the file has usually moved on. REQ-S9-001 puts contract and fees on the six points every partner type is managed on, and REQ-S9-004 makes the contracted schedule the basis of the fee actually paid — so a schedule that changes in place re-prices work already done and pays a partner a rate that was never agreed for that placement. BR-S9-002 (FSD S9 A2.2.3.1) is the rule this story is written against: no value a business person may change is written in code; it is read from reference data with its version. A panel, a fee schedule and a service level that live in a class constant break that rule silently, because the run still passes and only the money is wrong.

The second half of the rationale is the boundary. DP-07 makes the list values a contract of rwb-case, so a list copied into the partner service drifts the moment the list changes; the panel status the bank uses, the partner types it recognises and the instruction types and statuses it issues have to come from one source, or a status read in one service stops matching the status read in another. That is why this harness asserts the list values through P3's contract and not through a second copy, and why the version boundary is asserted on an instruction that was already issued: the version in force changes the next placement, not the one already made.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13); there is no in-process call and no second hop. The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and confirmed by the central ledger in rwb-decision (ADR-022). DP-01 forbids reading another service's schema, so the panel and the instructions are read through S9's contract, the lists through P3's, and the case through P3's; ACE-side data is read only through P1's published contract (DP-05). On the edge, DP-19 sends partners through the partner gateway in the DMZ and reserves gateway-bff composite routes for the staff screens; this run calls S9's own operations at the service boundary, which are the operations both edges front.

One limit is stated plainly because it shapes the run. The Ownership Map publishes `GET /partners` and the partner-instruction operations but no panel-version or fee-schedule load operation, and it publishes no parameter that carries a panel version or a fee-schedule version. The harness therefore reads the versions in force through the published reads and the reference-data contract, drives the load through S9's own path inside RWB-S9-E6030-APP, and asserts it through those reads and the decision log; it never invents a reference-load endpoint of its own.

### 3. Preconditions

- The published contracts of S9 rwb-partner (the partner list and the partner-instruction operations), P3 rwb-case (the reference-data contract `GET /admin/lists/{listCode}` and `GET /admin/parameters`, DP-07, and the case read), P7 rwb-decision (the decision log) and P4 rwb-access (the session) are in the contract registry, and a contract fake is generated from each one with its version pinned.
- S9 owns `partner` and `partner_instruction` in `rwb_partner` (Arch v5 slide 41, line 2891), so the panel row and the instruction this run reads have one named owner before a value is asserted.
- The panel and the versions are RWB-S9-E6030-APP until it lands; until then the fixture of §12.8 stands in for its effect and the story is reported as a stub pass.
- P3 owns `lov_value` and publishes the reference-data contract of DP-07, so the list values are read through that contract and never from a copy.
- FEAT-PRM-02 Hold the partner panel and fee schedule as data is the S9 feature, with FEAT-CWC-23 as its prerequisite (Epics 3 to 8 Specification v3, line 135); this story asserts the feature across the service boundary and builds neither.
- The lists are LOV-PANEL (ACTIVE, ON_NOTICE, SUSPENDED, EXITED), LOV-PARTNER-TYPE, LOV-INSTRUCTION and LOV-INSTR-STATUS, with the values the TSD S9 gives at lines 93 to 98.
- The rules in force are R-WO-30, R-WO-31, R-UNI-25, R-UNI-26 and R-UNI-45; the harness reads them with their version and evaluates none of them.
- The synthetic partner, panel version, fee schedule versions, service levels, business date, evidence format and gate are Not specified in the source documents (GAP-0460; ASM-0652), and are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the contract fakes in place from the first run; the one wait is RWB-S9-E6030-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: runs preflight. It reads the six contracts of §12.2, pins each version in the run report, loads the panel and fee-schedule fixture, and stops the run before any assertion if a contract is missing or a pinned version has moved (X1).
2. Harness: loads the fixture: partner `PRT-SYN-0030` with its partner_type, panel_status, contract_end and scope, panel version `PNLV-SYN-0030-v2`, fee schedule `FS-SYN-0030-v2` in force and `FS-SYN-0030-v3` effective from the next business date, the service levels held by partner type, business date `2027-04-30`, and case `RW-2027-000830`. On Day 1 the stubs of §12.8 return the same records.
3. Harness: reads `GET /api/recovery/partner/v1/partners` and asserts the panel row with its partner_code, partner_type, panel_status and contract_end, and the version of the fee schedule the row points at, which is `FS-SYN-0030-v2` (AC2).
4. Harness: reads `GET /api/recovery/case/v1/admin/lists/{listCode}` for LOV-PANEL, LOV-PARTNER-TYPE, LOV-INSTRUCTION and LOV-INSTR-STATUS and asserts that every code the partner read returns has its list row, its label_en and its valid_from through P3, that one source answers all four lists, and that no list value is read from a copy inside rwb-partner (AC3).
5. Harness: asserts the version in force and its valid-from are the ones the partner read applies, and that the decision entry of the load records the same two values. The map publishes no parameter that carries a panel or fee-schedule version, so the version is asserted where the partner read applies it and in the decision entry, and if a later contract publishes such a parameter the run reads `GET /api/recovery/case/v1/admin/parameters` and fails on a second copy (AC2, AC3).
6. Harness: places an instruction under `FS-SYN-0030-v2` through `POST /api/recovery/partner/v1/cases/{caseId}/instructions` with one Idempotency-Key, reads it back through `GET /api/recovery/partner/v1/partner/instructions`, and asserts instruction `INS-SYN-2027-0030` on case `RW-2027-000830`, its instruction_type from LOV-INSTRUCTION, its status `SENT` from LOV-INSTR-STATUS and its fee_amount (AC4).
7. Harness: counts one `rwb.partner.InstructionIssued.v1` per instruction on `rwb.partner.events.v1`, and asserts a replay of the same placement with the same Idempotency-Key adds no second instruction and no second event (AC4).
8. Harness: advances the fixture to the business date on which `FS-SYN-0030-v3` is in force, reads the partner and the instruction again, and asserts the partner now names v3 while the instruction still carries v2 and its fee_amount has not changed (AC4).
9. Harness: reads the four lists again on the later business date and asserts the same values as before, because a new fee schedule does not fork the list (AC3).
10. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry per version load with its rule_id, its rule_version and the valid-from date it applied, and reads `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` and asserts one publication per version, confirmed once by the central ledger, with no second entry after a re-read (AC1).
11. Harness: resets the fixture to the snapshot before the v3 load, turns the fault switch on the decision-record hop on, drives the v3 load again through S9's own path, and asserts the answer carries MSG-P7-003, that the partner read still names v2 in force, and that the decision log holds no entry for the refused load; the version in force keeps running and the switch is reset after the run (AC5).
12. Harness: calls `GET /api/recovery/partner/v1/partners` as a synthetic caller whose session carries no Partner portal R and asserts 403 with MSG-P4-002 with no panel row and no version returned (AC6).
13. Harness: writes one run report per version, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the panel row, the version in force, the list values and their source, the instruction and its fee, the decision entries with their rule versions, both event counts and the gate verdict.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow, or the load is driven short of a required field | The run fails at that hop and the report names the service, the operation, the contract version and the missing field; no criterion is marked passed | MSG-GEN-001 (expected, and missing) | TC-E6-030-01-ITG (ITG AC1) | AC1 |
| X2 | A code the partner read returns has no row in the list the reference-data contract answers, or the contract answers a different label or valid_from from a copy held elsewhere | The run fails on AC3 and the report names the code, the list, the contract answer and the copy, because a list with two sources is the drift DP-07 forbids | None | TC-E6-030-04-ITG (ITG AC3) | AC3 |
| X3 | A version change re-prices an instruction that was already issued, or moves it to the new version | The run fails on AC4 and the report names the instruction, its fee_amount before and after, and both versions | None | TC-E6-030-04-ITG (ITG AC4) | AC4 |
| X4 | Two versions are in force for one partner on one business date, or the partner read names a version whose valid-from is later than the business date | The run fails on AC2 and the report names both versions, their valid-from dates and the business date | None | TC-E6-030-01-ITG (ITG AC2) | AC2 |
| X5 | The decision record is written twice for one version load, written without its rule_version, or written without the valid-from date it applied | The run fails on AC1 and the report names the entries, their rule ids, their rule versions and the missing valid-from | None | TC-E6-030-01-ITG (ITG AC1) | AC1 |
| X6 | A forced decision-record failure leaves the new version in force, adds a decision entry, or answers without MSG-P7-003 | The run fails on AC5 and the report names the version read before and after, the entry count and the answer | MSG-P7-003 (expected, and missing) | TC-E6-030-02-ITG (ITG AC5) | AC5 |
| X7 | A caller without Partner portal R is allowed the partner read | The run fails on AC6 and the report names the caller role, the right, the operation and the answer; a 200 is a failure even when no data changed | MSG-P4-002 (expected, and missing) | TC-E6-030-03-ITG (ITG AC6) | AC6 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and their stubs from Day 1; the only wait is RWB-S9-E6030-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the two versions and their dates, the fault switch, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | Proves that the panel and the terms are read as data with a version, that their lists come from one source, that a new version does not re-price issued work, and that a version load without its decision record changes nothing |
| Estimable | One runner, one stub set, one panel and fee-schedule fixture, one partner, one instruction, two version loads, one list probe, one decision probe, one event observer and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S9-E6030-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Hold the partner panel and fee schedule as data - wave 4 integration harness

  Background:
    Given the synthetic partner "PRT-SYN-0030" is on the panel on panel version "PNLV-SYN-0030-v2"
    Given fee schedule "FS-SYN-0030-v2" is in force on business date "2027-04-30" and "FS-SYN-0030-v3" is effective from the next business date
    Given LOV-PANEL, LOV-PARTNER-TYPE, LOV-INSTRUCTION and LOV-INSTR-STATUS answer from the rwb-case reference-data contract

  Scenario: AC1 Hold the partner panel and fee schedule as data (legacy RWB-E6-030 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then keeps every panel, fee schedule and service level as versioned reference data
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The panel and its terms are read as the version in force (new, D-RCV-60)
    Given the partner "PRT-SYN-0030" is on the panel with its partner_type, panel_status and contract_end
    When GET /api/recovery/partner/v1/partners is called on business date "2027-04-30"
    Then the panel row names panel version "PNLV-SYN-0030-v2" and fee schedule "FS-SYN-0030-v2" in force
    And the row carries the service levels held for its partner type
    And the version and its valid-from date are the ones the decision entry of the load records

  Scenario: AC3 The list values come from rwb-case's reference-data contract and not from a copy (new, D-RCV-60)
    Given GET /api/recovery/partner/v1/partners returns panel, partner type, instruction type and instruction status codes
    When GET /api/recovery/case/v1/admin/lists/{listCode} is called for LOV-PANEL, LOV-PARTNER-TYPE, LOV-INSTRUCTION and LOV-INSTR-STATUS
    Then every code the partner read returns has its list row, its label_en and its valid_from through rwb-case
    And the same values answer for both fee schedule versions, so a new schedule does not fork the list
    And no list value is read from a copy inside rwb-partner

  Scenario: AC4 A new version leaves an instruction issued under the old version untouched (new, D-RCV-60)
    Given instruction "INS-SYN-2027-0030" is placed on case "RW-2027-000830" under "FS-SYN-0030-v2" with its fee_amount
    When the fixture advances to the business date on which "FS-SYN-0030-v3" is in force
    Then GET /api/recovery/partner/v1/partners names "FS-SYN-0030-v3"
    And GET /api/recovery/partner/v1/partner/instructions still returns the instruction under "FS-SYN-0030-v2"
    And the fee_amount of the instruction has not changed

  Scenario: AC5 A forced decision-record failure stops the version load with nothing changed (new, D-RCV-60)
    Given the decision record cannot be written for the load of "FS-SYN-0030-v3"
    When the load is driven through rwb-partner's own path in RWB-S9-E6030-APP
    Then the answer carries "MSG-P7-003"
    And GET /api/recovery/partner/v1/partners still names "FS-SYN-0030-v2" in force
    And the decision log holds no entry for the refused load
    And the version in force keeps running

  Scenario: AC6 A caller without Partner portal R is refused the partner read (new, D-RCV-60)
    Given a synthetic caller with role "RW-CASEOWN" whose session carries no Partner portal R
    When the caller calls GET /api/recovery/partner/v1/partners
    Then the answer is 403 with "MSG-P4-002"
    And no panel row and no version is returned

  Scenario: AC7 The business rules BR1 to BR10 are asserted against their owners and changed by none of the harness (new, D-RCV-60)
    Given the rules BR1 to BR10 of section 8 are the rules this story asserts
    When the harness reads each rule through its owner's published operation
    Then each rule BR1 to BR10 is asserted against its owner and the harness changes none of them

  Scenario: AC8 A redelivered consumed event leaves the panel and the decision log unchanged (new, D-RCV-60)
    Given one event the harness consumes is delivered to the harness twice
    When the harness processes the second delivery
    Then the publication is counted once
    And the panel and the version in force are unchanged by the second delivery
    And the decision log holds one entry for the load

  Scenario: AC9 A consumed call that fails or does not answer fails the run and leaves the panel and the version in force unchanged (new, D-RCV-60)
    Given one REST call the harness consumes fails or does not answer
    When the harness runs that hop
    Then the run fails at that hop and no criterion is marked passed
    And the panel and the version in force are unchanged
```

Legacy AC1 is the only legacy criterion this story owns. Legacy AC2 (the decision log cannot be written and nothing changes) stays with RWB-S9-E6030-APP as its build criterion and is asserted here across the service boundary in AC5, where the panel, the version in force and the decision log are read before and after the refused load. The versions are asserted through the published reads and the decision log because the Ownership Map publishes no reference-load operation for the partner panel; the harness never calls an operation the map does not publish. The valid-from rule for a partner-panel version is Not specified in the source documents (GAP-0460), so the valid-from is asserted only as the decision entry of the load records it.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit | REQ-S9-001 |
| BR2 | Fees are calculated from the contracted schedule and paid against recorded results, so the contracted schedule is the basis of the fee actually paid | REQ-S9-004 |
| BR3 | No value a business person may change is written in code; it is read from reference data with its version | BR-S9-002 (FSD S9 A2.2.3.1) |
| BR4 | The list values behind the panel, the partner types, the instruction types and the instruction statuses are the reference-data contract of rwb-case; a list has one source and is never copied into rwb-partner | DP-07 |
| BR5 | An agency on the panel with capacity takes the placement and the instruction is sent, so the panel a placement reads is the panel in force for the business date | R-WO-30 |
| BR6 | No agency on the panel has capacity: the placement is held and escalated on the timer | R-WO-31 |
| BR7 | When the partner leaves the panel or the contract ends, every open case held by that partner is recalled and re-selected | R-UNI-26 |
| BR8 | When the next partner is selected on the scorecard, the instruction is re-issued and the partner clock restarts | R-UNI-45 |
| BR9 | The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1`, and the central ledger in rwb-decision confirms it; nothing moves when the record cannot be written | DP-03; ADR-022 |
| BR10 | Every hop is one REST call on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout and no second hop; ACE data only through P1's contract; never another service's schema or table | DP-11; DP-13; DP-01; DP-05 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E6030-APP, the list values are P3's, the decision log and the rule rows are P7's, and the case is P3's. R-UNI-24 is read for one principle only — a recorded decision is corrected by a correcting entry naming the original and never overwritten — so a version and its decision entry are never rewritten in place; the run makes no correction and claims none.

### 9. State transitions

| From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|
| ACTIVE | none in the rule set read here | a partner is on the panel and the read carries its contract_end and score | ACTIVE, unchanged | S9 writes the panel value; the placement is RWB-S9-E6031's |
| ON_NOTICE | none in the rule set read here | the contract is running to its end and contract_end is the field the read carries | ON_NOTICE | S9 through the reference-data load of RWB-S9-E6030-APP |
| SUSPENDED | R-UNI-29 conduct breach suspends allocation | a conduct breach is recorded; the panel value is data and the rule's effect is on allocation | SUSPENDED | S9 for the panel value; the allocation effect is the rule's |
| EXITED | R-UNI-26 partner leaves the panel or the contract ends | the partner leaves the panel or the contract ends, and every open case is recalled and re-selected | EXITED, with PARTNER_RECALLED on the cases | S9 for the panel value; the recall is the partner and agency manager's |
| SENT | R-UNI-25 partner misses the service level | the work is chased once, then recalled and re-selected on the scorecard | RECALLED | S9 rwb-partner |
| SENT | R-UNI-26 partner exits the panel | the partner exits, so its open instructions are recalled | RECALLED | S9 rwb-partner |

The panel states are the four values LOV-PANEL holds — ACTIVE, ON_NOTICE, SUSPENDED and EXITED — and the instruction states run from SENT to RECALLED on the two rules above; S9 owns both changes and the harness observes them. The version states are two, and neither is a case state:

| Version state | What it means | Owner of the change | Read that shows it |
|---|---|---|---|
| In force | the version's valid-from is on or before the business date | S9 rwb-partner through the load of RWB-S9-E6030-APP | `GET /api/recovery/partner/v1/partners` names it, and the decision entry of the load records it |
| Effective from a future date | the version's valid-from is after the business date | S9 rwb-partner through the load of RWB-S9-E6030-APP | the same read still names the version in force, and the future version is not applied to any instruction |

The harness changes no state and writes no row: it reads the panel, the instruction and the versions, advances the fixture's business date instead of waiting for a schedule, and asserts the reads. The list values are read, never written; a list change is P3's reference-data change and is not part of this run.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG (Partner and agency manager) | Primary role of the S9 module, holding Partner portal CRUDA (TSD S9 T6.1, line 145); the run reads the panel and places the instruction under this role |
| The reference data administrator | The actor of the legacy story: keeps the panel, the fee schedule and the service levels as versioned data; the load itself is RWB-S9-E6030-APP's and this story only observes it |
| RW-CASEOWN and RW-TEAMMGR | Read the partner panel and the instructions at R (TSD S9 T6.1, lines 136 and 137), and are the reading callers of AC2, AC3 and AC4 |
| RW-RISK and RW-COE | Read the versions and the rule version at R (TSD S9 T6.1, lines 152 and 153) where the run records the rule version behind a load |
| The refused caller of AC6 | A synthetic caller whose session carries role RW-CASEOWN with no Partner portal R: every published Recovery role in the S9 matrix holds at least R, so the negative fixture is a session in which the grant is absent, and the run asserts the refusal only, never that the role lacks the right |
| QA lead | Owns the harness configuration, the fixture, the fault switch, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S9 holds the panel, the instruction and the version load, P3 holds the lists and the case, P7 holds the decision log and the central ledger, and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end, score | Read through the rwb-partner contract; S9 owns the table in `rwb_partner` |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read through the rwb-partner instruction read; S9 owns the table in `rwb_partner` |
| DF-REF-027 to DF-REF-033 | lov_value | id, lov_code, value_code, label_en, label_th, sort_order, valid_from | Read through P3's reference-data contract; P3 owns the table |
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, status, stage_code, route_state, rule_version | Read through the rwb-case case contract; the case the instruction sits on; P3 owns the table |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version, decided_at | Read through the rwb-decision contract; written by S9's load through the local decision-record library; P7 owns the table |
| DF-REF-001 to DF-REF-015 | rule_row | id, rule_id, rule_version, valid_from, valid_to, approved_by | Read through the rwb-decision contract; P7 owns the table |

Field IDs are those of the Logical Data Model and Data Dictionary v9, and the legacy data table of RWB-E6-030 cites the partner, the decision log entry, the rule row and `lov_value` under these ranges. The panel and the instruction are S9's in `rwb_partner`, and the fee_amount the version boundary is asserted on is DF-PRT-016; the list values are P3's and are read only through the reference-data contract the legacy table cites as `lov_value` DF-REF-027 to DF-REF-033; the decision entry and the rule rows are P7's; the case is P3's. No source publishes a table for the panel version or the fee schedule version, so the versions are held as data inside S9's own contract and no field ID is asserted for them here. The harness owns no table and writes no row: the two changes it drives are S9's own published operation of §12.2 and the load inside RWB-S9-E6030-APP, and everything else it reads is a contract read.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The panel row with its partner_type, panel_status and contract_end, and the fee schedule version in force (AC2, AC5, AC6) |
| POST | `/api/recovery/partner/v1/cases/{caseId}/instructions` | S9 rwb-partner | Places the instruction under the version in force, once per Idempotency-Key (AC4) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instruction, its type, its status and its fee_amount, read back before and after the version boundary (AC4) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The rows and labels of LOV-PANEL, LOV-PARTNER-TYPE, LOV-INSTRUCTION and LOV-INSTR-STATUS, the reference-data contract of DP-07 (AC3) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | One entry per version load with its rule_id, its rule_version and the valid-from it applied (AC1, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before the partner read (AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation in the Ownership Map. DP-07 makes the list read a C dependency — RWB-P3-E1043-CON — and that story is built against the published reference-data contract and its fake, so it never blocks this run. The map publishes no panel-version or fee-schedule load operation, and no parameter that carries either version; the version in force is therefore asserted where the partner read applies it and in the decision entry, and if a later contract publishes such a parameter the run reads it and fails on a second copy.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | S9 rwb-partner (EV-20) | Counts one publication per instruction and proves a replay of the same placement adds none (AC4) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | S9 rwb-partner through the local decision-record library (DP-03), confirmed by P7 rwb-decision | Proves one decision record per version load, with its rule version, published once and confirmed once by the central ledger (AC1, AC5) |

The harness subscribes to both topics under one consumer group of its own and counts publications; the effect it reads for rwb-decision is the decision log through the operation of §12.2, because the central ledger confirmation is read there and not from a schema.

#### 12.5 Workflows and activities

None added. The harness observes `InstructionWorkflow`, S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace, through the placement of §4 step 6: its `issueInstruction` step and its due_at timer are the ones the run sees in the workflow history (Arch v5 slide 17, line 1247). Neither the workflow, an activity nor a Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added, and none needed. A version takes effect by its valid-from date and not by a job, so nothing in the journey is on a cron: the harness advances the fixture's business date across the boundary instead of waiting for a schedule.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): `partner` and `partner_instruction` are S9's in `rwb_partner`, `lov_value` and `recovery_case` are P3's, and `decision_log_entry` and `rule_row` are P7's in `rwb_decision`.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (S9) | `GET /partners`, `POST /cases/{caseId}/instructions`, `GET /partner/instructions` | Partner `PRT-SYN-0030` on panel version `PNLV-SYN-0030-v2` with fee schedule `FS-SYN-0030-v2` in force and `FS-SYN-0030-v3` effective from the next business date; instruction `INS-SYN-2027-0030` on case `RW-2027-000830` in `SENT` under v2 with its fee_amount; on the later business date the panel names v3 and the instruction keeps v2; with the fault switch on, the load answers MSG-P7-003 and the panel stays on v2 |
| Stub for rwb-case (P3), reference data | `GET /admin/lists/{listCode}` | The rows, labels and valid_from of LOV-PANEL, LOV-PARTNER-TYPE, LOV-INSTRUCTION and LOV-INSTR-STATUS, unchanged across both business dates |
| Stub for rwb-decision (P7) | `GET /decision-log?caseId={caseId}` | No entry before a load; one entry per version load with its rule_id, rule_version and the valid-from it applied; the central ledger confirmation once; nothing added by the refused load |
| Stub for rwb-access (P4) | `GET /me/session` | Allows RW-AGENCYMG and the reading callers where the run needs them; for the refused caller of AC6 answers 403 with MSG-P4-002 |
| Panel and fee-schedule fixture | The version and the terms, held as data | Partner `PRT-SYN-0030` with its type, status, contract_end and scope; panel version `PNLV-SYN-0030-v2`; fee schedules `FS-SYN-0030-v2` and `FS-SYN-0030-v3`; the service levels by partner type; business date `2027-04-30` and the next effective date |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The five fakes are published by RWB-S9-E6030-CON; the published fake library version is Not specified in the source documents (DOR-RWB-ITG-E6030-ITG-22), and the run report pins it once that story publishes it. The harness environment, base hosts, fixture layout, synthetic partner and case keys, the panel version and the two fee schedule versions, the service levels, the business date and the next effective date, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0460; ASM-0652).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 6 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.partner.InstructionIssued.v1` and `rwb.decision.DecisionRecorded.v1`, counted once each |
| Temporal | None added; `InstructionWorkflow` on `rwb-partner` observed through the placement |
| File | None. The versions and the terms are S9's own request bodies and the report is the harness's own output; no file or claim-check is transferred by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery-w4/partner-panel-versions`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies these patterns add — RWB-PLT-E1027-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON — are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None. DP-13 adds nothing: the panel, the instruction, the list and the decision log are each called on the owner's own base and there is no shared base left. DP-07's C is RWB-P3-E1043-CON, and C never blocks: the run builds against the published reference-data contract and its fake from Day 1. DP-19 has two edges and the run names both: for a **partner** the route is the **partner gateway** in the DMZ under FAPI 2.0, and **gateway-bff** composes the **staff** screens only, including the panel list and the placement view; the harness renders neither and calls the operations behind them. The one blocking dependency is the I story RWB-S9-E6030-APP, which replaces its stub; until it is live a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the six owned criteria in order for one partner and one business date, holds the run lock and the fixture reset |
| PanelVersionReadBack | Service | Reads the panel row, its partner_type, panel_status and contract_end, and the fee schedule version in force on the business date |
| ListReadBack | Service | Resolves every code the partner read returns through the rwb-case reference-data contract for the four lists, and asserts one source |
| InstructionVersionProbe | Service | Places the instruction once under v2, advances the business date, and asserts the instruction still carries v2 and its fee_amount |
| DecisionProbe | Service | Reads one decision entry per version load with its rule_id, rule_version and valid-from, reads the published decision record, and holds the fault switch |
| EventProbe | Service | Subscribes to `rwb.partner.events.v1` and `rwb.decision-record.v1`, counts publications and asserts a replay adds none |
| AccessProbe | Service | Reads the session, calls the partner read as the refused caller, and asserts the 403 and the message |
| EvidenceReport | Service | Writes one report per version and business date, keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real service as RWB-S9-E6030-APP lands, on the synthetic partner `PRT-SYN-0030`, the case `RW-2027-000830`, the panel version `PNLV-SYN-0030-v2`, the fee schedules `FS-SYN-0030-v2` and `FS-SYN-0030-v3`, and business date `2027-04-30`. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the panel version and the two fee schedule versions, the service levels, the business date and the next effective date, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0460; ASM-0652).

**Build steps**

1. Generate the stub set and the panel and fee-schedule fixture from the published contracts, pin each contract version in the run report, and fail the run on a mismatch (X1).
2. Build the PanelVersionReadBack and the ListReadBack and prove the panel row, its terms, the version in force and every list code through P3, with one source and no copy (AC2, AC3, X2, X4).
3. Add the InstructionVersionProbe: one placement under v2 with one Idempotency-Key, the instruction read back with its type, status and fee_amount, and the EventProbe counting one InstructionIssued (AC4).
4. Advance the fixture business date and assert the boundary: the panel names v3, the instruction still carries v2 and its fee is unchanged, and the lists answer the same values (AC4, AC3, X3).
5. Add the DecisionProbe: one entry per version load with its rule_id, rule_version and valid-from, one published decision record, the central ledger confirmation, and no second entry after a re-read (AC1, X5).
6. Add the fault switch: force the decision-record failure on the v3 load, assert MSG-P7-003, the panel still on v2, no decision entry and the version in force still running; reset the fixture and the switch after the run (AC5, X6).
7. Add the AccessProbe: the refused caller at 403 with MSG-P4-002 and no panel row returned (AC6, X7).
8. Add the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S9-E6030-APP lands; a stub pass is never reported as a real pass.

**Feature switch.** None. The harness has no production flag; the fault switch of step 6 exists in the test environment only and is reset by the runner before and after each run.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S9-E6030-APP when it lands, and the wave entry check holds a run report keyed by story and business date.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text and no S9 message of its own. MSG-GEN-001 is asserted with the missing field when a version load is driven short of a required field, the validation rule VR-S9-002-1 of FSD S9 A2.2.3.1 (X1); MSG-P4-002 is asserted with the refused action when the caller carries no Partner portal R (AC6, X7); and MSG-P7-003 is asserted when the decision record cannot be written and nothing changes (AC5, X6).

### 15. Screens and states

The legacy story's screens are SCR-34 Partner list and SCR-35 Placement and allocation, and neither is built or rendered here: the harness calls the partner and instruction operations behind them and reads the states through the owners. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0460; ASM-0652).

SCR-34 Partner list states: empty, Not specified in the source documents (CG-ALL-1119); loading, as Screen Specifications v1 section SCR-34 gives it; error, Not specified in the source documents (CG-ALL-1119); no access, Not specified in the source documents (CG-ALL-1119).

SCR-35 Placement and allocation states: empty, Not specified in the source documents (CG-ALL-1120); loading, as Screen Specifications v1 section SCR-35 gives it; error, Not specified in the source documents (CG-ALL-1120); no access, Not specified in the source documents (CG-ALL-1120).

| State | Read through | What the run asserts |
|---|---|---|
| The version in force | `GET /api/recovery/partner/v1/partners` and the decision log | The panel names `FS-SYN-0030-v2` on business date `2027-04-30`, with its valid-from and one decision entry |
| The version effective from a future date | the same reads on the later business date | `FS-SYN-0030-v3` is named once the business date reaches its valid-from, and v2 is no longer named |
| The instruction issued under v2 | `GET /api/recovery/partner/v1/partner/instructions` | The instruction still carries v2 and its fee_amount has not changed after v3 is in force |
| The refused or failed load | the S9 answer, the partner read and the decision log | 403 with MSG-P4-002 or MSG-P7-003, the panel and the version unchanged, and no decision entry for the refused load |

SCR-34 Partner list and SCR-35 Placement and allocation belong to the S9 stories of the legacy key, and neither is built or read here. A partner would reach its own instruction view through the partner gateway and a staff member would reach the panel and the placement through a gateway-bff composite route (DP-19); this harness renders neither and asserts the operations behind them. The wave 4 entry check agrees the environment and base hosts, the fixture layout, the synthetic partner and case keys, the panel version and the two fee schedule versions, the service levels by partner type, the business date and the next effective date, the evidence format and its retention, and the pass or fail gate; a stub pass is never a real pass, and the integration lead owns that agreement. Until it is agreed, any of these values that this story does not state is Not specified in the source documents (GAP-0460).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-030-01-ITG | AC1 (legacy) and ITG AC2 | End to end | Partner `PRT-SYN-0030` on panel version `PNLV-SYN-0030-v2` with fee schedule `FS-SYN-0030-v2` in force on business date `2027-04-30`, one decision entry with its rule version |
| TC-E6-030-02-ITG | The not-recorded path across the boundary, ITG AC5, derived from legacy AC2 | Integration | A forced decision-record failure on the `FS-SYN-0030-v3` load, with the panel, the version in force and the decision log read before and after |
| TC-E6-030-03-ITG | Access, ITG AC6 | Component | A synthetic caller with role RW-CASEOWN whose session carries no Partner portal R, and the partner read |
| TC-E6-030-04-ITG | Principle 5 and the version boundary, ITG AC3 and AC4 | Integration | The four lists resolved through the rwb-case reference-data contract on both business dates, and one instruction placed under v2 and read after v3 is in force |
| TC-E6-030-05-ITG | ITG AC7, the business rules BR1 to BR10 | Not specified in the source documents (NEWAC-RWB-ITG-E6030-ITG-AC7) | Not specified in the source documents (NEWAC-RWB-ITG-E6030-ITG-AC7) |
| TC-E6-030-06-ITG | ITG AC8, a redelivered consumed event | Not specified in the source documents (NEWAC-RWB-ITG-E6030-ITG-AC8) | Not specified in the source documents (NEWAC-RWB-ITG-E6030-ITG-AC8) |
| TC-E6-030-07-ITG | ITG AC9, a consumed call that fails or does not answer | Not specified in the source documents (NEWAC-RWB-ITG-E6030-ITG-AC9) | Not specified in the source documents (NEWAC-RWB-ITG-E6030-ITG-AC9) |

The AC column names the legacy test each copy derives from and the ITG acceptance criteria it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID: TC-E6-030-01 to TC-E6-030-04. Legacy AC2 stays with RWB-S9-E6030-APP, which owns the failure inside the load; the -ITG copy here asserts the same failure across the service boundary. ITG AC2 and ITG AC3 are asserted inside the run of TC-E6-030-01-ITG, which is the end-to-end case that reads the panel and the versions; they add no test case ID because the legacy set has four.

### 17. Guardrails

- No business value in code, first and without exception: the panel, the fee schedule and the service levels are data rows with a version, read from reference data, and the synthetic partner, the versions, the service levels, the business date and the lists are fixture and reference data (BR-S9-002).
- No personal data in logs, events, workflow inputs or reports: every key is synthetic and the reads carry codes, dates and amounts only.
- Service data only through the owner's contract: the panel and the instruction from S9, the lists and the case from P3, the decision log and the rule rows from P7, the session from P4; never a direct schema read and never another service's table (DP-01, DP-07).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented operation: only the six operations of §12.2, and no reference-load endpoint, because the map publishes none for the partner panel.
- A list has one source: a value the partner read returns that the reference-data contract does not hold fails the run, and no copy is accepted as a pass (DP-07).
- A new version never re-prices issued work: an instruction read under a different version from the one it was issued under fails the run.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner, and the fault switch is reset before and after each run.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E6-030 Hold the partner panel and fee schedule as data | Recovery Workbench User Stories Epics 3 to 8 v4, lines 11901 to 11979 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 11920 to 11924 | Section 7, AC1, marked (legacy RWB-E6-030 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E6-030-02 | The same, lines 11926 to 11930 and 11970 to 11977 | AC5 asserts the same failure here; the legacy criterion stays with RWB-S9-E6030-APP (section 19) |
| Legacy data table: partner, decision_log_entry, rule_row and lov_value with their DF ranges | The same, lines 11932 to 11940 | Section 11 |
| Legacy endpoints, screens, permission checks and messages | The same, lines 11942 to 11947, 11949 to 11954, 11956 to 11960 and 11962 to 11968 | Sections 12.2, 15, 10 and 14 |
| Legacy test cases TC-E6-030-01 to TC-E6-030-04 | The same, lines 11970 to 11977 | Copied as -ITG in section 16 |
| FEAT-PRM-02 Hold the partner panel and fee schedule as data, with FEAT-CWC-23 as its prerequisite | Epics 3 to 8 Specification v3, line 135 | Sections 1, 3 and 19 |
| REQ-S9-001 the six points, and REQ-S9-004 the contracted schedule as the basis of the fee paid | Business Requirements Program v5, lines 430 and 433 | Section 8, BR1 and BR2, and section 2 |
| FSD S9 A2.2: the step table, VR-S9-002-1, BR-S9-002, the field catalogue and the two exception criteria | FSD S9 Partner management v3, lines 173 to 255 | Sections 2, 3, 8, 12.8 and 14 |
| TSD S9: the field definitions, the four LOV blocks and the API detail | TSD S9 Partner management v2, lines 63 to 106, 91 to 99 and 197 to 245 | Sections 3, 5, 9, 11 and 12.2 |
| S9 contract: the partner and instruction operations, InstructionWorkflow and `rwb.partner.events.v1` | Architecture v5, lines 1245 to 1256 and 1270 to 1272 | Sections 2, 8, 12.2, 12.4 and 12.5 |
| rwb-partner ownership, schema, topic and wave | Architecture v5 slide 41, line 2891 | Sections 1, 12.7 and 13 |
| S9 journey: onboard, scorecard, instruction, result, recall, fee, exit; partner SLA by type | Temporal and Drools design, slide 25, lines 1663 to 1755 | Sections 8 and 9 |
| Versioned rule and reference packages: valid-from, version on every answer, the version in force keeps running when a load fails | Temporal and Drools design, lines 790 to 798, 820 to 828 and 1901 to 1932 | Sections 8, 9 and 13 |
| R-WO-30, R-WO-31, R-UNI-24, R-UNI-25, R-UNI-26 and R-UNI-45 | Business Rules and Routing Logic v4, lines 361, 362, 428, 429, 430 and 449 | Section 8, BR5 to BR8, and section 9 |
| DF-PRT-001 to DF-PRT-016, DF-REF-027 to DF-REF-033, DF-CAS-001 to DF-CAS-023, DF-DEC-001 to DF-DEC-018 and DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-07, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 8, 12.4 and 12.2: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| The six criteria of this harness and the gap and assumption behind its configuration | This file, sections 3, 7 and 12.8; GAP-0460 and ASM-0652 | Sections 3, 7, 12.8, 13 and 15 |

### 19. Out of scope

- RWB-S9-E6030-CON and RWB-S9-E6030-APP: the panel, the fee schedule, the service levels, the versions and the decision record inside the service, including legacy AC2 (the not-recorded path), which is its build criterion and which this story asserts only across the boundary in AC5.
- The reference-data service build in P3, RWB-P3-E1043-CON and its APP, and the platform reference-data library RWB-PLT-E1043-CON.
- The onboarding itself (RWB-S9-E6029), allocation (RWB-S9-E6031) and the override (RWB-S9-E6032).
- The result intake (RWB-S9-E6033).
- The fee approval and the invoice path (FEAT-PRM-07 and FEAT-PRM-09).
- The partner portal screens SCR-34 Partner list and SCR-35 Placement and allocation.
- The partner gateway and the gateway-bff composite routes, which DP-19 names but this story neither builds nor calls.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
