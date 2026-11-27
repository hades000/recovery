# RWB-ITG-E6029-ITG Onboard a partner and set terms

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E6029-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-029 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E6029-APP |
| Contract dependencies | RWB-S9-E6029-CON, major version 1; published file `rwb-partner.yaml` of API Specification v5, version 5.0.0 |
| Integration dependencies | RWB-S9-E6029-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-029 as the wave 4 integration proof that a partner is on the panel with its contract, fee schedule, service levels and scope read back as data through rwb-partner, that the same panel and terms reach the boundary product DP08, that a partner outside the panel cannot be instructed, and that the onboarding carries one decision record with its rule version; the onboarding and the terms are RWB-S9-E6029-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E6029-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 5 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the onboarding of a partner proved end to end on the real services: the partner and its contract end, fee schedule, service levels and scope read back through rwb-partner as versioned data, the same panel and terms read through DP08 Partner performance, a partner outside the panel refused for a new instruction, and one decision record with the rule version**, so that **no partner is instructed before its terms are in force and no panel the rest of the bank sees differs from the panel the bank holds**.

This story builds the wave 4 integration harness and its evidence, and nothing else. The onboarding, the panel and the terms are built by S9 rwb-partner in RWB-S9-E6029-APP and its CON story; the case is P3's, the decision record and the central ledger are P7's, DP08 Partner performance is P1's product over S9's records, and the right that answers the read is P4's. The harness drives the onboarding through S9's own path, reads the partner and its terms through S9's published read, reads the same panel through DP08, reads the decision log through P7, counts the events and writes a run report per run. It provides no endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

Partners are instructed and paid by email and spreadsheet today, and allocation is not based on performance (FSD S9 A1.3). The failure this story is written against is a firm instructed before it is on the panel, or after its contract has ended: the bank places work with an agency it has not contracted, or keeps placing work with one whose terms have lapsed, and neither the fee nor the service level nor the scope the case was placed under can be said afterwards. REQ-S9-001 puts every partner type on the same six points — selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit — and REQ-S9-002 gives each partner type one named owner, so the onboarding is the point where those six are fixed for a firm. R-UNI-26 then makes the exit real: a panel exit or a contract end recalls every open case held by that partner and forces a re-selection, and R-WO-30 places work only with an agency that is on the panel. Read together, the two rules mean the panel status and the contract end are not paperwork: they decide whether an instruction may be issued at all.

The second half of the rationale is the boundary. DP08 Partner performance is a Workbench product over `partner` and `partner_instruction`, refreshed on change, so a panel the bank holds but the product does not carry is a panel nobody else can see — not the review forum, not the reporting that runs off the products, not the screen a head of the partner type opens. A partner onboarded in one place and read differently in another is the same class of failure as a partner instructed off the panel.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13); there is no in-process call and no second hop. The partner and the instruction are S9's; the case is P3's; the decision log, the rule rows and the central ledger are P7's; DP08 is P1's product over S9's records. DP-01 forbids reading another service's schema, and ACE-side or boundary data is read only through P1's contract (DP-05). The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract. On the edge, DP-19 sends partners through the **partner gateway** (FAPI 2.0) that fronts rwb-partner and reserves gateway-bff composite routes for staff screens; this run calls S9's own operation at the service boundary, which is the same operation the partner gateway fronts.

One limit is stated plainly because it shapes the run. The Ownership Map publishes `GET /partners` and `GET /partner/instructions` but no partner create and no panel-change operation, so the harness reads the onboarded partner and its terms through the published read, drives the write through S9's own path inside RWB-S9-E6029-APP, and asserts the step through that read, through DP08 and through the decision log. It never invents a partner endpoint, and where a screen would compose the panel read with the case view, the path is the partner gateway for the partner and the gateway-bff composite route for staff (DP-19).

### 3. Preconditions

- The published contracts of S9 rwb-partner (the partner read, the instruction placement and the partner instruction read), P1 rwb-source-data (DP08 Partner performance and its freshness), P3 rwb-case (the case), P7 rwb-decision (the decision log) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- S9 owns the panel, the partner users, the instructions, the results, the fees and the scorecards in `rwb_partner` (Arch v5 slide 41, line 2891), so the partner, its terms and its instructions have one named owner before a value is asserted.
- The onboarding and the terms are RWB-S9-E6029-APP and its CON story; until they land, the S9 stub of §12.8 stands in for their effect and the story is reported as a stub pass.
- FEAT-PRM-01 is the S9 feature and FEAT-OCC-13 is its prerequisite (Epics 3 to 8 Specification v3, line 134); the fixture presupposes the block and contact work FEAT-OCC-13 delivers, so this story never asserts it.
- The lists of values are LOV-PARTNER-TYPE, LOV-PANEL, LOV-INSTRUCTION and LOV-INSTR-STATUS, with the values in TSD S9 lines 93 to 98.
- The rules in force for this journey are R-WO-30, R-WO-31, R-UNI-25, R-UNI-26, R-UNI-27, R-UNI-29 and R-UNI-45.
- The synthetic partner, its contract, the fee schedule version, the service levels, the scope, the business date and the gate: Not specified in the source documents (GAP-0459; ASM-0651).
- The synthetic partner, its terms, the second partner and the business date are held in the fixture as data, never written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S9-E6029-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Preflight: the harness pins the contract version of each of the seven operations of §12.2 and the version of the terms fixture, and fails the run where a version is missing (X1).
2. Harness: loads the fixture — partner `PRT-SYN-0029` with its partner_code, partner_type `AGENCY`, panel_status `ACTIVE`, its contract_end, the fee schedule version `FS-SYN-0029-v2`, the service levels by partner type, the scope and business date `2027-04-30`, plus a second partner `PRT-SYN-0029-X` at `SUSPENDED` with an ended contract. On Day 1 the stubs of §12.8 return the same records.
3. Harness: reads `GET /api/recovery/partner/v1/partners` and asserts the partner with its partner_code, partner_type, panel_status `ACTIVE`, contract_end and latest score, and that no second row is returned for the same partner code (AC2).
4. Harness: asserts the fee schedule version, the service levels and the scope are the versions in force for business date `2027-04-30` and are the values held in the fixture, never constants in the harness, and that the decision record names the same version of the terms (AC2).
5. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP08/records?partnerId={partnerId}` and asserts the same partner_code, the same panel_status and the same contract_end as the owner holds, with its business date, so the boundary view the rest of the bank sees is the panel the bank holds (AC3).
6. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts exactly one entry for the onboarding, with its rule_id and its rule_version, and no second entry after a re-read (AC2).
7. Harness: places a work item with the partner through `POST /api/recovery/partner/v1/cases/{caseId}/instructions` with one Idempotency-Key, and asserts the answer names the partner and the case (AC4).
8. Harness: reads `GET /api/recovery/partner/v1/partner/instructions` and asserts one instruction for the partner and the case, with its instruction_type, instructed_at, due_at and status `SENT` (AC4).
9. Harness: replays the same placement with the same Idempotency-Key, asserts the answer is the first answer unchanged, and re-reads the instruction and asserts one instruction and no second `rwb.partner.InstructionIssued.v1` (AC4).
10. Harness: attempts a placement naming the suspended partner `PRT-SYN-0029-X`, and asserts 409 with no instruction created and no `rwb.partner.InstructionIssued.v1` published; it then reads `GET /api/recovery/case/v1/cases/{caseId}` before and after and asserts the case did not move (AC4).
11. Harness: resets the fixture to the pre-onboarding snapshot, turns the fault switch on the decision-record hop on, runs the onboarding step through S9's own path, and asserts the answer carries MSG-P7-003 with no partner change and no instruction; the switch is reset before the next run (AC5).
12. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller without Partner portal R, then `GET /api/recovery/partner/v1/partners`, and asserts 403 with MSG-P4-002 and no partner row returned (AC6).
13. Harness: writes one run report per run, keyed by story and partner code, naming the contract version of each hop, whether the hop was a stub or the owner, the partner and its terms version, the business date, the DP08 read, the one decision entry with its rule version, the instruction and both event counts, the workflow run and the gate verdict.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow, or the placement body omits a required field | The run fails at that hop and the report names the service, the operation, the contract version and the missing field; no criterion is marked passed | MSG-GEN-001 (expected where a required field is omitted, and missing) | TC-E6-029-01-ITG (ITG AC2) | AC2 |
| X2 | The panel the owner holds differs from DP08, or a second row is returned for the same partner code | The run fails on AC3 and the report names the partner code, the owner's panel_status and contract_end, the product's values and both business dates | None | TC-E6-029-04-ITG (ITG AC3) | AC3 |
| X3 | A placement naming the suspended partner `PRT-SYN-0029-X` is accepted, or leaves an instruction or an event behind | The run fails on AC4 and the report names the partner, the answer code, the instruction count and the event count, because a partner off the panel is the failure R-WO-30 is written against | None | TC-E6-029-01-ITG (ITG AC4) | AC4 |
| X4 | A second instruction is created for the same work item | The run fails on AC4 and the report names both instructions, the Idempotency-Key each carried and the instructed_at of each | None | TC-E6-029-01-ITG (ITG AC4) | AC4 |
| X5 | The onboarding decision record is written twice, written without its rule version, or names a different version of the terms than the fixture pins | The run fails on AC2 and the report names the entries, their rule versions, the version of the terms each names and the missing confirmation | None | TC-E6-029-04-ITG (ITG AC2) | AC2 |
| X6 | A forced decision-record failure leaves a partner change or an instruction, or answers without MSG-P7-003 | The run fails on AC5 and the report names the partner read before and after, the instruction count and the event count | MSG-P7-003 (expected, and missing) | TC-E6-029-02-ITG (ITG AC5) | AC5 |
| X7 | A caller without Partner portal R is allowed the partner read, or the read answers a body instead of 403 | The run fails on AC6 and the report names the caller role, the right the session answered, the operation and the answer; a 200 is a failure even when the body is empty | MSG-P4-002 (expected, and missing) | TC-E6-029-03-ITG (ITG AC6) | AC6 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S9-E6029-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the terms fixture, the fault switch, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The partner and its terms are proved to be on the panel and in force as data, the same panel is proved to reach DP08, a firm off the panel is proved to be refused, and the refused and failed paths are proved to change nothing |
| Estimable | One runner, one stub set, one partner fixture with its terms, one second partner off the panel, one placement, two reads of the panel, one probe of the product, one decision probe, one event observer and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S9-E6029-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Onboard a partner and set terms - wave 4 integration harness

  Background:
    Given the synthetic partner "PRT-SYN-0029" is on the panel with fee schedule "FS-SYN-0029-v2", its service levels and its scope, and partner "PRT-SYN-0029-X" is at SUSPENDED with an ended contract
    Given the rule package in force holds R-WO-30, R-UNI-26 and R-UNI-27 and DP08 answers for the partner
    Given the business date is "2027-04-30"

  Scenario: AC1 Onboard a partner and set terms (legacy RWB-E6-029 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes a partner onto the panel with its contract, fee schedule, service levels and scope
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The partner and its terms are read back as versioned data (new, D-RCV-60)
    Given the partner "PRT-SYN-0029" is onboarded with its contract end, fee schedule "FS-SYN-0029-v2", its service levels and its scope
    When GET /api/recovery/partner/v1/partners is read for the partner code
    Then the answer carries the partner_code, partner_type "AGENCY", panel_status "ACTIVE", contract_end and the latest score
    And no second row is returned for the same partner code
    And the fee schedule version, the service levels and the scope are the versions in force for business date "2027-04-30"
    And GET /api/recovery/decision/v1/decision-log?caseId={caseId} holds exactly one onboarding entry with its rule_id and rule_version

  Scenario: AC3 The same panel and terms reach the boundary product (new, D-RCV-60)
    Given the partner is onboarded and DP08 Partner performance is refreshed on change
    When GET /api/recovery/source-data/v1/data-products/DP08/records?partnerId={partnerId} is read
    Then the product carries the same partner_code, panel_status and contract_end that the owner holds
    And the product carries its business date

  Scenario: AC4 A partner outside the panel cannot be instructed (new, D-RCV-60)
    Given partner "PRT-SYN-0029-X" is at SUSPENDED and its contract has ended
    When a placement is attempted through POST /api/recovery/partner/v1/cases/{caseId}/instructions naming "PRT-SYN-0029-X"
    Then the answer is 409
    And no instruction is read through GET /api/recovery/partner/v1/partner/instructions for that partner
    And no "rwb.partner.InstructionIssued.v1" is published
    And GET /api/recovery/case/v1/cases/{caseId} answers the same status and stage as before

  Scenario: AC5 A forced decision-record failure stops the onboarding with nothing changed (new, D-RCV-60)
    Given the decision record cannot be written for the onboarding
    When the onboarding step is run through S9's own path with the fault switch on
    Then the answer carries "MSG-P7-003"
    And the partner is read unchanged through GET /api/recovery/partner/v1/partners
    And no instruction is created and no "rwb.partner.InstructionIssued.v1" is published

  Scenario: AC6 A caller without Partner portal R is refused the partner read (new, D-RCV-60)
    Given a synthetic caller with role "RW-CASEOWN" whose session answers without the Partner portal right R
    When the caller reads GET /api/recovery/partner/v1/partners
    Then the answer is 403 with "MSG-P4-002"
    And no partner row is returned

  Scenario: AC7 Each business rule BR1 to BR10 names the criterion or the owner story that asserts it (new, D-RCV-60)
    Given the business rules table in section 8 is the current version
    When the Covered by entry of each rule is read
    Then every rule BR1 to BR10 names a criterion of this story or the owner story that evaluates it
    And no rule has an empty Covered by entry

  Scenario: AC8 A redelivered consumed event adds no second instruction or partner event (new, D-RCV-60)
    Given "rwb.partner.InstructionIssued.v1" has been delivered once for partner "PRT-SYN-0029" and its instruction is at SENT
    When the same event is delivered again
    Then no second instruction is created for the partner and the case
    And no second "rwb.partner.InstructionIssued.v1" is published

  Scenario: AC9 A consumed call that fails or does not answer changes nothing (new, D-RCV-60)
    Given the partner read or the instruction call the harness consumes fails or does not answer within the 2 s budget
    When the onboarding or placement step is run against it
    Then the answer is a failure and no instruction is created
    And no "rwb.partner.InstructionIssued.v1" is published
    And once the call answers again the partner is read unchanged through GET /api/recovery/partner/v1/partners
```

Legacy AC1 is the only legacy criterion this story owns, and it is the business outcome the S9 onboarding has to reach: a partner on the panel with its contract, fee schedule, service levels and scope, and the result written to the decision log with the rule version. Legacy AC2 (the decision log cannot be written, so nothing changes and the user sees MSG-P7-003) stays with RWB-S9-E6029-APP as its build criterion, and this story asserts the same failure across the service boundary in AC5, where the partner read, the instruction count and the event count are taken before and after the refused onboarding. The read of the onboarded partner in AC2 is the published path and not a create operation, because the Ownership Map publishes no partner create and no panel change; the write itself is S9's own path, asserted through the read, DP08 and the decision log.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit | REQ-S9-001 | None in this harness; evaluated in RWB-S9-E6029-APP |
| BR2 | Each partner type has one named owner | REQ-S9-002 | None in this harness; evaluated in RWB-S9-E6029-APP |
| BR3 | Work is placed only with an agency that is on the panel, chosen on measured return, and the instruction is sent the same day on the portal | R-WO-30 | AC4; TC-E6-029-05-ITG |
| BR4 | When no agency on the panel has capacity the placement is held and escalated on the timer, so nothing is placed with a firm off the panel | R-WO-31 | None in this harness; evaluated in RWB-S9-E6029-APP |
| BR5 | A partner panel exit or a contract end recalls every open case held by that partner and forces a re-selection, inside 5 working days | R-UNI-26 | None in this harness; evaluated in RWB-S9-E6029-APP |
| BR6 | When the partner misses the service level on the portal the work is chased once, then recalled and re-selected on the scorecard | R-UNI-25 | None in this harness; evaluated in RWB-S9-E6029-APP |
| BR7 | A declared conflict withdraws the instruction and re-selects the next partner; an upheld conduct breach suspends allocation and recalls the affected cases; the re-selection re-issues the instruction and restarts the partner clock | R-UNI-27, R-UNI-29, R-UNI-45 | None in this harness; evaluated in RWB-S9-E6029-APP |
| BR8 | No value a business person may change is written in code; it is read from reference data with its version | BR-S9-001, FSD S9 A2.1.3.1 | AC2; TC-E6-029-01-ITG |
| BR9 | The onboarding writes one decision record through the local decision-record library on `rwb.decision-record.v1`, and the central ledger in rwb-decision confirms it; nothing changes when it cannot be written | DP-03; ADR-022 | AC1, AC2, AC5; TC-E6-029-01-ITG, TC-E6-029-02-ITG, TC-E6-029-04-ITG |
| BR10 | Every hop is one REST call on the owner's base `/api/recovery/<short>/v1` with a 2 s budget, and no service reads another service's schema or reaches ACE data except through P1's contract | DP-11, DP-13, DP-01, DP-05 | AC2, AC3, AC9; TC-E6-029-01-ITG, TC-E6-029-04-ITG, TC-E6-029-08-ITG |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E6029-APP, the panel and the terms are S9's, the case is P3's, and the rule versions and the central ledger are P7's. The reference data is read under DP-06 and DP-07: the fee schedule `FS-SYN-0029-v2`, the service levels and the scope are read as data with their version through the panel read; the parameter names are Not specified in the source documents (DOR-RWB-ITG-E6029-ITG-20).

### 9. State transitions

| From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|
| ACTIVE | none | the partner is onboarded with its contract, fee schedule, service levels and scope, and the terms are in force on the business date | ACTIVE, in force | S9 rwb-partner, RWB-S9-E6029-APP |
| ACTIVE | PARTNER_PANEL_EXIT | the partner leaves the panel or the contract ends | EXITED, and every open case held by the partner recalled and re-selected | S9 rwb-partner under R-UNI-26, 5 working days; outside the run |
| SUSPENDED | none | a placement naming the suspended partner is attempted | SUSPENDED, unchanged | S9 rwb-partner refuses before any write, under R-WO-30 |
| no instruction | instruction issued on the case | the partner is on the panel and the placement is accepted | SENT | S9 rwb-partner, InstructionWorkflow `issueInstruction`, R-WO-30; `rwb.partner.InstructionIssued.v1` |
| SENT | PARTNER_NO_RESPONSE | the partner misses the service level on the portal | RECALLED, then re-selected | S9 rwb-partner under R-UNI-25 and R-UNI-45; outside the run |
| any | none | the onboarding is refused for want of Partner portal R, or stops on a decision-record failure | unchanged | S9 rwb-partner refuses before any write; nothing changes |

`LOV-PANEL` gives the partner the four states ACTIVE, ON_NOTICE, SUSPENDED and EXITED, and `LOV-INSTR-STATUS` gives the instruction SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED (TSD S9 lines 95 and 97); S9 owns both. The harness changes no state: it drives the onboarding and the placement through S9's published operations and reads every state back, and it never sets a state it then asserts. The case is read through P3 before and after each attempt and is asserted unchanged, because an onboarding and a placement are partner decisions, not case transitions; the case status and stage are whatever P3 already held. A partner the bank suspends or whose contract ends is recalled under R-UNI-26, and that recall is asserted as a rule this run respects, not as a state it moves.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG Partner and agency manager | Primary role of the journey: holds Partner portal CRUDA in the TSD RBAC matrix, owns the panel, the terms and the placement, and is the role the six points of REQ-S9-001 belong to |
| RW-HEADLIT Head of Litigation, RW-HEADNPA Head of NPA, RW-HEADASL Head of Asset Liquidity | Also use the panel, with RA in the matrix; the run records that the read and the onboarding right answer for them where their scope allows |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT | Hold Partner portal CRU and place work with a partner where their scope allows; the run asserts C on the placement path |
| RW-CASEOWN | Holds Partner portal R in the matrix (TSD S9 line 136) and holds no onboarding right; because the map publishes no onboarding operation to refuse, the refusal this run proves is the read right R, and the AC6 fixture answers the RW-CASEOWN session without that right so the 403 is real |
| RW-TRIBE, RW-PLATADM, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD | Hold Partner portal R and read the panel; they place nothing and onboard nothing |
| PT-AGENCY and the other partner-side roles | Read and update their own instructions through the partner portal; the run neither drives nor asserts them |
| QA lead | Owns the harness configuration, the fixtures, the terms fixture, the fault switch, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S9 holds the partner, the terms and the instruction and runs InstructionWorkflow, P1 holds DP08, P3 holds the case, P7 holds the decision log and the central ledger, and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end, score | Read through the rwb-partner contract and through DP08; written by S9's onboarding, not by the harness |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read through the rwb-partner contract; the row is written by S9's placement, not by the harness |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code, route_state, primary_person_key | Read through the rwb-case contract, before and after every attempt |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, inputs_ref, model_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9, and the legacy data table of RWB-E6-029 cites the partner, the decision log entry and the rule rows under these IDs. The partner and the instruction are S9's in `rwb_partner`; `partner` carries seven fields and `partner_instruction` nine (LDM lines 20 and 21, TSD S9 lines 63 to 89). The case is P3's in `rwb_case`. The decision log entry and the rule rows are P7's in `rwb_decision`, and the entry's `inputs_ref` is the field the run reads when it asserts that the decision names the version of the terms in force. The legacy data table also cites the timer under DF-WRK-027 to DF-WRK-036; the harness reads no timer, because the partner clock is a workflow timer inside InstructionWorkflow and not a scheduled job (Temporal design slide 25). The harness owns no table and writes no row: the two changes it drives are S9's own published operations of §12.2, each with one Idempotency-Key, and everything else it reads is a contract read.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The onboarded partner with its partner_code, partner_type, panel_status, contract_end and latest score, and no second row for the same code (AC2, AC5, AC6) |
| POST | `/api/recovery/partner/v1/cases/{caseId}/instructions` | S9 rwb-partner | Places one instruction with one Idempotency-Key, and is the refused operation of AC4 (AC1, AC4) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The one instruction with its instruction_type, instructed_at, due_at and status `SENT`, and the absence of one after the refusal (AC4) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | DP08 Partner performance with productCode DP08, refreshed on change, as the boundary view of the same panel and terms (AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case status and stage before and after the placement and the refused placement (AC4) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | Exactly one onboarding entry with its rule_id and rule_version, and no second entry after a re-read (AC1, AC2, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before the partner read (AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation in the Ownership Map, which lists `GET /partners`, `POST /cases/{caseId}/instructions`, `GET /partner/instructions`, `GET /data-products/{productCode}/records`, `GET /cases/{caseId}`, `GET /decision-log` and `GET /me/session` under those owners. Two things the map does not publish shape the run. First, there is no partner create and no panel-change operation, so the onboarding write is RWB-S9-E6029-APP's, reached through S9's own path, and the step is asserted through the published read, DP08 and the decision log; the harness never calls an endpoint the map does not carry. Second, the `InstructionRequest` body of the placement is S9's contract shape from RWB-S9-E6029-CON, so the harness pins that version and reads the body from the fixture rather than composing it. For a partner the edge path to the instruction operations is the partner gateway (FAPI 2.0) that fronts rwb-partner, and for a staff screen the same values would be composed by a gateway-bff composite route (DP-19); the run itself calls the service boundary the gateway fronts.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | S9 rwb-partner (EV-20) | Counts one publication per accepted placement and proves that a replay and the refused placement add none; the consumer Arch v5 gives it is the partner portal (AC4) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | S9 rwb-partner through the local decision-record library (DP-03) | Proves the onboarding and its rule version were published once and confirmed by the central ledger, and that the forced failure published none (AC2, AC5) |

The harness subscribes to both topics under one consumer group of its own and counts publications; it replays the placement once and asserts the event count is unchanged. The partner portal, which Arch v5 slide 43 row 20 gives as the consumer of `InstructionIssued`, exposes no operation for this story, so its consumer effect is read from the consumer evidence in the run fixture; this story reads no portal state of its own.

#### 12.5 Workflows and activities

None added. The harness exercises InstructionWorkflow, S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace, through the placement: its SLA timer for the partner type and its `issueInstruction` activity are the ones the run observes in the workflow history (Arch v5 slide 17, line 1247; Temporal design slide 25). It observes CaseWorkflow on `rwb-case` as the parent that holds the case the instruction is placed against, and observes it only: the placement does not signal it and moves no case state. Neither workflow, activity nor Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added, and none needed. The onboarding is a user act and the partner clock is a workflow timer, not a job: the recall at 5 working days and the re-selection at 2 working days are timers inside the workflow (Temporal design slide 25, lines 1744 to 1745), and the partner SLA by type is a timer per partner type. JOB-05 Timer check is retired in favour of durable timers inside the workflows (Arch v5 slide 44, line 2981), so the run has nothing to schedule and starts from its own fixture and business date.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): `partner`, `partner_user` and `partner_instruction` are S9's in `rwb_partner`, `recovery_case` is P3's in `rwb_case`, `decision_log_entry` and `rule_row` are P7's in `rwb_decision`, and DP08 is P1's published product over S9's records.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (S9), the panel | `GET /partners` | Partner `PRT-SYN-0029` with its partner_code, partner_type `AGENCY`, panel_status `ACTIVE`, contract_end and latest score, one row per code; partner `PRT-SYN-0029-X` at `SUSPENDED` with an ended contract when asked; 403 with MSG-P4-002 for a caller without Partner portal R |
| Stub for rwb-partner (S9), the placement | `POST /cases/{caseId}/instructions` | One instruction accepted per Idempotency-Key with its instruction_type, instructed_at and due_at, and a repeat of the key returning the first answer unchanged; 409 for `PRT-SYN-0029-X` with no instruction created |
| Stub for rwb-partner (S9), the instruction read | `GET /partner/instructions` | The one instruction in `SENT`, and no instruction for the refused partner |
| Stub for rwb-source-data (P1), DP08 | `GET /data-products/DP08/records?partnerId={partnerId}` | The partner and its terms as the published product carries them, refreshed on change, with its business date |
| Stub for rwb-case (P3) | `GET /cases/{caseId}` | The case with the same status and stage before and after every attempt |
| Stub for rwb-decision (P7) | `GET /decision-log?caseId={caseId}` | No entry before the onboarding; exactly one entry with its rule_id, its rule_version and the version of the terms in `inputs_ref` after it, and the central ledger confirmation once; unchanged by the forced failure |
| Stub for rwb-access (P4) | `GET /me/session` | Allows RW-AGENCYMG on the panel and the placement; answers the RW-CASEOWN session without Partner portal R for AC6 |
| Partner and terms fixture | The partner, the contract, the terms and the second partner | Partner `PRT-SYN-0029`, its contract_end, fee schedule `FS-SYN-0029-v2`, the service levels by partner type, the scope, business date `2027-04-30`, and `PRT-SYN-0029-X` at `SUSPENDED` with an ended contract, all held as data with the fixture version pinned |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic partner and contract keys, the terms fixture, the business date, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0459; ASM-0651).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.partner.InstructionIssued.v1` and `rwb.decision.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; InstructionWorkflow on `rwb-partner` exercised through the placement, with its SLA timer and its `issueInstruction` activity, and CaseWorkflow on `rwb-case` observed only |
| File | None. The placement body is S9's own request shape and the report is the harness's own output; no file or claim-check is transferred by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery-w4/partner-onboarding`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None. DP-13 adds nothing: the panel and instruction paths are rewritten onto each owner's own base and there is no shared base left. DP-19 has two edges in this journey and the run names both: for the **partner** the route is the **partner gateway** in the DMZ under FAPI 2.0, which fronts rwb-partner and is the only path a partner has (Arch v5 slide 20, line 1458, and slide 35, line 2517), and **gateway-bff** composes the **staff** screens only, including the panel a partner and agency manager opens. The one blocking dependency is the I story RWB-S9-E6029-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the six owned criteria in order for one partner and holds the run lock and the fixture reset |
| PanelReadBack | Service | Reads the partner through `GET /partners` and asserts its code, type, panel status, contract end, latest score and single row |
| TermProbe | Service | Asserts the fee schedule version, the service levels and the scope against the pinned terms fixture, the business date and the version the decision record names |
| ProductReadBack | Service | Reads DP08 and asserts the same partner_code, panel_status and contract_end as the owner holds, with its business date |
| InstructionDriver | Service | Places one instruction per Idempotency-Key, reads it back, replays the key, and attempts the refused placement naming the suspended partner |
| DecisionProbe | Service | Reads the one onboarding entry and its rule version, reads the published decision record, and holds the fault switch |
| EventProbe | Service | Subscribes to `rwb.partner.events.v1` and `rwb.decision-record.v1`, counts publications and replays the placement once |
| AccessProbe | Service | Answers the session for the allowed caller and for the caller without Partner portal R |
| EvidenceReport | Service | Writes one report per run, keyed by story and partner code, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S9-E6029-APP lands, on the synthetic partner `PRT-SYN-0029` with fee schedule `FS-SYN-0029-v2`, the second partner `PRT-SYN-0029-X` at `SUSPENDED` with an ended contract, and business date `2027-04-30`. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic partner and contract keys, the terms fixture, the business date, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0459; ASM-0651).

**Build steps**

1. Generate the stubs and the partner and terms fixture from the published contracts, pin each contract version and the fixture version in the run report, and fail the run on a mismatch (X1).
2. Build the PanelReadBack for AC2: the partner with its code, type, panel status, contract end and latest score, and no second row for the same code.
3. Add the TermProbe for AC2: the fee schedule version, the service levels and the scope are the versions in force on `2027-04-30` and the values in the pinned fixture, and the decision record names the same version (X5).
4. Add the ProductReadBack for AC3: DP08 carries the same partner_code, panel_status and contract_end as the owner, with its business date (X2).
5. Add the DecisionProbe for AC1 and AC2: one onboarding entry with its rule_id and rule_version, one published decision record, the central ledger confirmation, and no second entry after a re-read.
6. Add the InstructionDriver for AC4: one placement with one Idempotency-Key, the read back in `SENT`, a replay that returns the first answer unchanged, 409 for the suspended partner with no instruction and no partner event, and the case read before and after (X3, X4).
7. Add the EventProbe: one `InstructionIssued` per accepted placement, none for the replay and none for the refusal, and the confirmation the decision record carries.
8. Add the fault switch for AC5 and the AccessProbe for AC6, then the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S9-E6029-APP lands (X6, X7).

**Feature switch.** None. The harness has no production flag; the fault switch of step 8 exists in the test environment only and is reset by the runner before and after each run.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S9-E6029-APP when it lands, and the wave entry check holds a run report keyed by story and partner code.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text and no S9 message of its own. MSG-GEN-001 is the S9 validation message of VR-S9-001-1: it is asserted where the placement body leaves a required field out and S9 answers 422 with the field named, which is the same omission the X1 shape check runs against the stub (FSD S9 A2.1.3.1, line 121). MSG-P4-002 is asserted with the refused action when the caller answers without Partner portal R (AC6, AC-EXC-S9-001-01, FSD S9 A2.1.4.3 line 162). MSG-P7-003 is asserted when the decision record cannot be written and nothing changes (AC5, AC-EXC-S9-001-02, FSD S9 A2.1.4.3 line 163).

### 15. Screens and states

The legacy story's screens are SCR-34 Partner list and SCR-35 Placement and allocation, and neither is built or rendered here: the harness calls the operations behind them and reads the states through the owners. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0459; ASM-0651).

| State | Read through | What the run asserts |
|---|---|---|
| ACTIVE, in force | S9 partner read, the terms fixture and the decision record | The partner is on the panel with its contract end, fee schedule version, service levels and scope, and the version of the terms is the one in force on the business date |
| The boundary view | DP08 through P1 | The same partner_code, panel_status and contract_end as the owner holds, with its business date |
| One instruction at SENT | S9 instruction read and the InstructionWorkflow history | One instruction for the partner and the case with its due_at, and one partner event; a replay adds none |
| A refused action | P4 session read, S9 answer, the instruction read and the case read | 409 for the suspended partner or 403 with MSG-P4-002 for the caller without R, no instruction, no partner event and no case change |
| A failed action | The decision log, the partner read and the instruction read | MSG-P7-003, the partner read unchanged and no instruction |
| SCR-34 Partner list, empty | Screen Specifications v1 SCR-34, not built or rendered here | Not specified in the source documents (CG-ALL-1114) |
| SCR-34 Partner list, loading | Screen Specifications v1 SCR-34, not built or rendered here | The screen's Loading state; nothing is asserted on it in this run |
| SCR-34 Partner list, error | Screen Specifications v1 SCR-34, not built or rendered here | Not specified in the source documents (CG-ALL-1114) |
| SCR-34 Partner list, no access | Screen Specifications v1 SCR-34, not built or rendered here | Access is Partner portal, checked on every request; an action outside the role's permission shows MSG-P4-002 |
| SCR-35 Placement and allocation, empty | Screen Specifications v1 SCR-35, not built or rendered here | Not specified in the source documents (CG-ALL-1115) |
| SCR-35 Placement and allocation, loading | Screen Specifications v1 SCR-35, not built or rendered here | The screen's Loading state; nothing is asserted on it in this run |
| SCR-35 Placement and allocation, error | Screen Specifications v1 SCR-35, not built or rendered here | Not specified in the source documents (CG-ALL-1115) |
| SCR-35 Placement and allocation, no access | Screen Specifications v1 SCR-35, not built or rendered here | Access is Partner portal, checked on every request; an action outside the role's permission shows MSG-P4-002 |

SCR-34 Partner list and SCR-35 Placement and allocation belong to the S9 stories of the legacy key, and neither is built or read here. The partner reaches the portal through the partner gateway (FAPI 2.0) and staff reach a screen through the gateway-bff composite route (DP-19); this harness renders neither and asserts the operations behind them. The run report replaces the screen for the wave entry check, and its environment, layout and retention are Not specified in the source documents (GAP-0459; ASM-0651).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-029-01-ITG | AC1 (legacy), ITG AC2 and ITG AC4 | End to end | Partner `PRT-SYN-0029` with fee schedule `FS-SYN-0029-v2`, its service levels and its scope on business date `2027-04-30`, read back through the panel read, the terms fixture and the decision record |
| TC-E6-029-02-ITG | The not-recorded path across the boundary; ITG AC5, derived from legacy AC2 | Integration | A forced decision-record failure before the onboarding, with the partner read and the instruction count taken before and after |
| TC-E6-029-03-ITG | Access; ITG AC6 | Component | A synthetic RW-CASEOWN session answering without Partner portal R, and the partner read it attempts |
| TC-E6-029-04-ITG | Principle 5; ITG AC3 and the decision record of AC2 | Integration | The DP08 read beside the owner's partner read on the same business date, one onboarding decision entry with its rule version, a re-read, and the central ledger confirmation |
| TC-E6-029-05-ITG | ITG AC4, the refusal of a partner off the panel; no legacy copy | Integration | A partner off the panel, with the case, the instruction count and the partner read taken before and after one placement and one refused placement |
| TC-E6-029-06-ITG | ITG AC7, the coverage of each business rule BR1 to BR10 | Component | Not specified in the source documents (NEWAC-RWB-ITG-E6029-ITG-AC7) |
| TC-E6-029-07-ITG | ITG AC8, a redelivered consumed event | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E6029-ITG-AC8) |
| TC-E6-029-08-ITG | ITG AC9, a consumed call that fails or does not answer | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E6029-ITG-AC9) |

The AC column names the legacy test each copy derives from and the ITG acceptance criteria it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID: TC-E6-029-01 Onboard a partner and set terms, TC-E6-029-02 Not recorded, TC-E6-029-03 the access refusal, and TC-E6-029-04 the forced decision log failure. Legacy AC2 stays with RWB-S9-E6029-APP, which owns the failure inside the service; the -ITG copy here asserts the same failure across the service boundary. ITG AC4, the refusal of a partner off the panel, is asserted inside the run of TC-E6-029-01-ITG, which places the instruction and attempts the refused one, and by TC-E6-029-05-ITG, which has no legacy copy. TC-E6-029-06-ITG, TC-E6-029-07-ITG and TC-E6-029-08-ITG assert ITG AC7, AC8 and AC9 in turn and have no legacy copy either.

### 17. Guardrails

- No business value in code: the synthetic partner, its contract, the fee schedule version, the service levels, the scope, the second partner, the business date, the fault switch and the report layout are data.
- No customer value in logs, events, workflow inputs or reports: every key is synthetic, the partner is read by code and the case by id, and the events carry IDs and facts only. `decision_log_entry.inputs_ref` (DF-DEC-008) is personal data, category Customer data, classed Confidential (Data Classification and Personal Data Inventory v5): it is shown only within the role's scope; in events and workflow inputs it carries a business fact only (a code, an amount or a date), never beside a direct identifier; in logs, and so in the run report, only a code or an id appears, never the customer value.
- Service data only through the owner's contract: the partner and the instruction from S9, DP08 from P1, the case from P3, the decision log and the rule rows from P7, the session from P4; never a direct schema read and never another service's table (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented operation: only the three S9 operations and the four reads of §12.2, and no partner create or panel change is composed, because the map publishes neither.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The fault switch is reset by the runner before and after each run and is never left on, so a forced failure cannot be mistaken for a real one.
- The harness never runs against UAT or production, never writes a row by hand, and never sets a state it then asserts; a failing criterion is fixed in the owning service or raised as a gap, and never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E6-029 Onboard a partner and set terms | Recovery Workbench User Stories Epics 3 to 8 v3, lines 11820 to 11899 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 11839 to 11843 | Section 7, AC1, marked (legacy RWB-E6-029 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E6-029-02 | The same, lines 11845 to 11849 and 11893 | AC5 asserts the same failure here; the legacy criterion stays with RWB-S9-E6029-APP (section 19) |
| Legacy test cases TC-E6-029-01 to TC-E6-029-04 | The same, lines 11888 to 11895 | Copied as -ITG in section 16 |
| Legacy endpoints, screens, permission checks and messages | The same, lines 11860 to 11865, 11867 to 11872, 11874 to 11878 and 11880 to 11886 | Sections 12.2, 15, 10 and 14 |
| FEAT-PRM-01 Onboard a partner and set terms, with FEAT-OCC-13 as its prerequisite | Epics 3 to 8 Specification v3, line 134 | Sections 1, 2 and 3 |
| REQ-S9-001 the six points, REQ-S9-002 one named owner, and REQ-S9-008 partners exchange data through the portal | Business Requirements Program v4, lines 430, 431 and 437 | Section 8, BR1 to BR3, and section 2 |
| R-WO-30 work placed only with an agency on the panel, and R-WO-31 the held placement | Business Rules and Routing Logic v4, lines 361 and 362 | Section 8, BR3 and BR4, and section 9 |
| R-UNI-26 a panel exit or a contract end recalls every open case, R-UNI-27 a declared conflict withdraws the instruction, and R-UNI-45 the re-selection re-issues and restarts the clock | The same, lines 430, 431 and 449 | Section 8, BR5 and BR7, and section 9 |
| R-UNI-25 the missed service level and R-UNI-29 the conduct breach | The same, lines 429 and 433 | Section 8, BR6 and BR7 |
| FSD S9 A2.1: the step table, VR-S9-001-1, BR-S9-001, the field catalogue, the roles and AC-EXC-S9-001-01 and AC-EXC-S9-001-02 | Recovery Workbench FSD S9 Partner management v3, lines 89 to 170 | Sections 3, 8, 10 and 14 |
| TSD S9 object and field definitions, the four lists of values, the RBAC matrix and the endpoint inventory and detail | Recovery Workbench TSD S9 Partner management v2, lines 63 to 106, 91 to 99, 130 to 165 and 197 to 277 | Sections 3, 8, 9, 10, 11 and 12.2 |
| S9 contract: the partner and instruction operations, InstructionWorkflow, `rwb_partner` and `rwb.partner.events.v1` | Architecture v5 slide 17, lines 1245 to 1256 and 1270 to 1272 | Sections 2, 9, 12.2, 12.5 and 12.7 |
| rwb-partner ownership, schema, topic, task queue and wave | Architecture v5 slide 41, line 2891 | Sections 1, 12.5 and 12.7 |
| InstructionIssued, producer rwb-partner, consumer partner portal | Architecture v5 slide 43, row 20, line 2946 | Section 12.4, AC4 |
| PartnerResultSubmitted, producer rwb-partner, consumers rwb-litigation, rwb-asset and rwb-case | Architecture v5 slide 43, row 21, line 2947 | Section 12.4, as the event this run does not use and does not count |
| The partner journey: onboard partner and terms as step 1, the partner clock, kit Partner instruction, the recall at 5 working days and the re-selection at 2 working days, and the exit recalling every open case | Temporal and Drools Design v1, slide 25, lines 1663 to 1755 | Sections 2, 9 and 12.6 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015 outbox and inbox on Kafka, ADR-020 contract-first REST with one hop and 2 s, ADR-022 local decision record plus central ledger | Architecture Decision Records v4 | Sections 12.4, 12.2 and 8 |
| The partner panel and terms: DF-PRT-001 to DF-PRT-016, DF-CAS-001 to DF-CAS-023, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v8, lines 20, 21, 137 to 159, 299 to 314, 416 to 433 and 480 to 494 | Section 11 |
| The six criteria of this harness and the gap and assumption behind its configuration | This file, sections 3, 7 and 12.8; GAP-0459 and ASM-0651 | Sections 3, 7, 12.8, 13 and 15 |

### 19. Out of scope

- RWB-S9-E6029-CON and RWB-S9-E6029-APP: the onboarding, the panel, the terms, the decision record inside the service and legacy AC2, which are its build criterion and which this story asserts only across the boundary in AC5.
- The S9 build as a whole: the panel, the partner users, the instructions, the results, the fees, the scorecards and InstructionWorkflow with its SLA timers, and every S9 CON, APP and DB story of the legacy key.
- The reference-data versions themselves, which RWB-S9-E6030 holds as versioned data: the harness pins them and changes none.
- Allocation by measured return (RWB-S9-E6031) and the override with a reason (RWB-S9-E6032): the fixture places one instruction and never asserts the scorecard order.
- The result intake and the attachment of a result to the case (RWB-S9-E6033), which is its own journey.
- The recall paths of R-UNI-26, R-UNI-27, R-UNI-29 and R-UNI-45 as products: they are asserted here as rules the run respects, and built by their own stories.
- The partner screens SCR-34 Partner list and SCR-35 Placement and allocation, and the partner gateway and the external partner sign-in, which are the partner portal's own product.
- The gateway-bff composite routes for the staff panel view, which DP-19 names but this story neither builds nor calls.
- The platform H stories DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, which the platform wave delivers.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
