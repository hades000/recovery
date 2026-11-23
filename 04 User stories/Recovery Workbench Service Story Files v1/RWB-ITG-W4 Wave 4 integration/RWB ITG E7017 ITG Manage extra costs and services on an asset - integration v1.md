# RWB-ITG-E7017-ITG Manage extra costs and services on an asset

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7017-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S9-E7017-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-017 as the wave 4 integration proof of the extra costs and services of a held asset, driven through the S5 asset read, the S9 partner read, the S9 instruction read, the S9 result write and the decision record read back through rwb-decision; the recording and the approval of the additional partner cost are built by S9 in RWB-S9-E7017-APP and the asset holding record and its instruction cost line are S5 rwb-asset's own stories. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the additional partner costs on a held asset to be recorded and approved against the asset and the partner, once, with the decision record carrying the rule version, proved end to end through the real asset, partner and decision contracts**, so that **partners are placed, paid and measured by rule, and a cost that cannot be recorded changes nothing**.

This story builds the wave 4 integration harness and its evidence, and nothing else. The recording and the approval of the additional partner cost, the asset holding record and the instruction cost line are built by S9 in RWB-S9-E7017-APP and by S5 rwb-asset in its own stories. The harness drives the cost claim through S9's published result write, reads the held asset through S5's published asset read, observes the events on the owners' topics, reads the decision record back through rwb-decision, and writes a run report per asset. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A held asset costs money while it is held, and the legacy key is the one place where that cost meets the partner who is paid for it. FEAT-PRM-14 records and approves additional partner costs on a held asset; FEAT-AST-07 is the sibling it depends on, and records maintenance, insurance and custody costs against the asset in AMIS. Both land on the same record, which is why the legacy story is written against the asset and not against the case: REQ-S5-001 says every repossessed or surrendered asset is recorded with its source, date taken in, holding cost and provision step, and REQ-S5-003 says holding age drives re-appraisal and the provision step by rule. A cost recorded on an asset the holding record does not carry is a cost nobody can reconcile, and a cost approved without a decision record is a cost nobody can defend.

The approval itself is a decision taken under a rule version. Fees are calculated from the contracted schedule and paid against recorded results (REQ-S9-004), and the contract and fees point of the six every partner type is managed on (REQ-S9-001) is the point this key exercises. R-UNI-38 fixes the version: a new rule version applies to decisions taken from its effective date, and open cases keep the version they were decided under. R-UNI-39 fixes the failure: where the decision log entry cannot be written, the action is blocked, an incident is raised, and no action proceeds unlogged. The recall and escalation context of R-UNI-25 to R-UNI-30 sits behind the same partner — a partner that misses its service level, leaves the panel, declares a conflict, becomes insolvent, breaches conduct or overruns its service level is recalled or escalated — and the harness reads that context, it never sets it.

Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). The legacy data section reaches the asset through `v_ace_npa_asset`, and the split keeps it that way: the harness reads no ACE view and no schema (DP-05). The DF-ACE-208 to DF-ACE-219 fields reach it through S5's asset contract, which owns the asset record and reads the view under its own login; `valuation_ext` stays with P1 and is not read here at all. The harness carries REQ-S5-001, REQ-S5-003 and REQ-S9-004 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S5 rwb-asset (the asset read), S9 rwb-partner (the partner read, the instruction read and the result write), P7 rwb-decision (the decision log), P3 rwb-case (the case) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The partner portal rights are in force for the run: Partner portal R to read the partner and the instructions, Partner portal U to record the cost claim. The right lists in the legacy section name RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG and PT-AGENCY among the holders of U, and RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR and RW-DEBTSALE among the holders of R; the harness itself holds no business right.
- A synthetic held asset, the partner that holds the work and one instruction against the asset are held in the fixture as data, with the rule package version the fixture names rather than a version written in code.
- RWB-S9-E7017-APP owns the recording and the approval of the additional partner cost, and S5 rwb-asset owns the asset holding record and the instruction cost line; until they land, the stub set of §12.8 stands in for their effect and the story is reported as a stub pass.
- The holding cost and the provision step of the asset are read through S5's asset contract, and `valuation_ext` is P1's and is not read in this run (DP-05); no ACE view and no schema is opened by the harness.
- The partner panel, fee schedule and service level reference data (FEAT-PRM-02) are versioned reference data and are not asserted here: the approval reads the schedule through its owner and the schedule's own holdings are RWB-S9-E7017-APP's sibling scope.
- The harness environment and base hosts, the fixture layout, the synthetic asset, partner, instruction and case keys, the stub answer shapes, the shape of the additional-cost claim, where the cost approval is recorded in S9 and in S5, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0477; ASM-0669).
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S9-E7017-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: held asset `AST-SYN-0017` with asset_key `AST-SYN-0017`, asset_code `NPA-SYN-0017`, transfer_in_type REPOSSESSION, from_segment NPA, book_value held as data, transfer_in_date and stock_date held as data; partner `PTR-SYN-0017` with partner_code `PTR-SYN-0017`, partner_type AGENCY, panel_status ACTIVE and contract_end 2027-12-31; instruction `INS-SYN-001701` on case `RW-2027-001701`. On Day 1 the stub of §12.8 returns the same records.
2. Harness: reads the asset through `GET /api/recovery/asset/v1/assets/{assetKey}` and asserts the asset_key, asset_code, transfer_in_type, from_segment, book_value, transfer_in_date and stock_date of the held asset (DF-ACE-208 to DF-ACE-219), and that it is held.
3. Harness: reads `GET /api/recovery/partner/v1/partners` with the `type` and `status` filters, and asserts the partner_code, partner_type, panel_status and contract_end (DF-PRT-001 to DF-PRT-007).
4. Harness: reads `GET /api/recovery/partner/v1/partner/instructions` and asserts the instruction with its case_id, partner_id, instruction_type, instructed_at, due_at and status (DF-PRT-008 to DF-PRT-016).
5. Harness: records the additional-cost claim against the asset once through `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results`, and asserts the answer carries the instruction with its status and result.
6. Harness: submits the same claim a second time and asserts the answer is 409 and one claim remains, so a repeated submission is never a second cost.
7. Harness: takes the cost approval on the same instruction and asserts the status moves through S9's own states; the statement of where the approval is recorded in S9 and in S5 is Not specified in the source documents (GAP-0477; ASM-0669).
8. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry for the cost approval with its decision_code, rule_id and rule_version, and that the entry records the rule version in force (R-UNI-38).
9. Harness: counts one `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` and asserts the central ledger in rwb-decision confirmed the record, then replays the event and asserts the decision log still holds one entry for the approval.
10. Harness: counts the `rwb.partner.PartnerResultSubmitted.v1` publications on `rwb.partner.events.v1` and asserts the consumer effect through `GET /api/recovery/case/v1/cases/{caseId}`, then replays the event and asserts the case and the instruction are unchanged, because the inbox holds one processed row per consumer.
11. Harness: forces the local decision-record library to fail for the cost approval and asserts the approval stops with MSG-P7-003, no claim is recorded against the instruction, the decision log holds no entry, and the asset, the partner and the instruction are unchanged when they are read again (R-UNI-39).
12. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller holding Partner portal R and not U, then attempts the claim write and asserts 403 with MSG-P4-002 and no state change.
13. Harness: writes one run report per asset, keyed by story and asset_key, naming the contract version of each hop, whether the hop was a stub or the owner, the asset and partner fields with their source, the claim and the decision record with its rule version, and the pass or fail gate.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no field is marked evidenced | None | TC-E7-017-01-ITG (ITG AC1) |
| X2 | The asset read is short of a field the legacy data section names | The run fails on AC2 and the report names the asset, the operation and the missing field; a field is never reported as passed from a narrative | None | TC-E7-017-01-ITG (ITG AC2) |
| X3 | The cost approval completes and no decision entry carries the rule version | The run fails on AC3 and the report names the case, the entry and the missing rule version | None | TC-E7-017-01-ITG (ITG AC3) |
| X4 | The central ledger has not confirmed the decision record and the approval completes anyway | The run fails on AC3 and the report names the case, the entry and the missing confirmation; confirmation is never assumed | MSG-P7-003 | TC-E7-017-04-ITG (ITG AC3) |
| X5 | The same claim is submitted twice and a second claim is recorded | The run fails on AC3 and the report names the two submissions and the instruction; a repeated submission is never a second cost | None | TC-E7-017-01-ITG (ITG AC3) |
| X6 | The decision record fails and the instruction or the asset still moves | The run fails on AC4 and the report names the instruction status and the asset fields before and after; nothing changes is asserted, not assumed | MSG-P7-003 (expected) | TC-E7-017-02-ITG (ITG AC4) |
| X7 | A caller without Partner portal U is allowed to record a claim | The run fails on AC5 and the report names the caller's rights, the operation and the answer; a 200 is a failure even when no business data changed | MSG-P4-002 (expected, and missing) | TC-E7-017-03-ITG (ITG AC5) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S9-E7017-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the claim shape, the evidence shape, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The asset and the partner are proved to be evidenced from named reads, the claim and its approval are proved to be recorded once, and an approval that cannot be recorded is proved to change nothing |
| Estimable | One runner, one stub set, one asset probe, one partner probe, one instruction probe, one claim write, one decision read-back, one event observer and one report |
| Small | Fits in one sprint with its five criteria and four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S9-E7017-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Manage extra costs and services on an asset - wave 4 integration harness

  Background:
    Given the synthetic held asset "AST-SYN-0017" is held with asset_code "NPA-SYN-0017", transfer_in_type "REPOSSESSION" and from_segment "NPA"
    Given the synthetic partner "PTR-SYN-0017" is on the panel with partner_type "AGENCY", panel_status "ACTIVE" and contract_end 2027-12-31
    Given the partner holds instruction "INS-SYN-001701" on case "RW-2027-001701" against the asset
    Given the rule package version in force is named by the fixture as data

  Scenario: AC1 Manage extra costs and services on an asset (legacy RWB-E7-017 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then records and approves additional partner costs on a held asset
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The asset, the partner and the cost claim are evidenced through their owners (new, D-RCV-60)
    Given the asset read returns the held asset "AST-SYN-0017" with asset_key, asset_code, transfer_in_type, from_segment, book_value, transfer_in_date and stock_date
    And the partner read returns "PTR-SYN-0017" with partner_code, partner_type, panel_status and contract_end
    And the instruction read returns "INS-SYN-001701" with its case_id, partner_id, instruction_type, instructed_at, due_at and status
    When the additional-cost claim is recorded against the instruction through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    Then the asset read answers every field the legacy data section names, DF-ACE-208 to DF-ACE-219, through S5's contract and never from an ACE view
    And the partner read answers the four fields of DF-PRT-001 to DF-PRT-007 the claim is made against
    And the claim is recorded once against its instruction through the published result write
    And a field with no value in either read is reported as a gap in the evidence, never as a pass

  Scenario: AC3 The cost approval is recorded once and the decision record carries the rule version (new, D-RCV-60)
    Given the additional-cost claim for "INS-SYN-001701" has been recorded
    When the cost approval is taken through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    Then one decision record is written with its decision_code, rule_id and rule_version
    And "rwb.decision-record.DecisionRecorded.v1" is published once on "rwb.decision-record.v1" and confirmed by the central ledger in rwb-decision
    And "rwb.partner.PartnerResultSubmitted.v1" is published once on "rwb.partner.events.v1" and consumed once by rwb-case, rwb-litigation and rwb-asset
    And one publication is made per claim, and a repeated submission of the same claim is refused and leaves one
    And a replay of each event changes nothing

  Scenario: AC4 A forced decision-record failure stops the cost approval (new, D-RCV-60)
    Given the local decision-record library is forced to fail for the cost approval
    When the cost approval is taken through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    Then the cost approval stops with "MSG-P7-003"
    And no claim is recorded against the instruction and no decision entry is written
    And the asset, the partner and the instruction are unchanged when they are read again

  Scenario: AC5 A caller without the Partner portal U right is refused (new, D-RCV-60)
    Given a synthetic caller whose right set holds Partner portal R and not Partner portal U
    When the caller records a cost claim through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    Then the answer is 403 with "MSG-P4-002"
    And no claim and no decision entry are written, and the asset, the partner and the instruction are unchanged
```

Legacy AC2 (the decision log cannot be written) stays with RWB-S9-E7017-APP, and this story asserts the same failure at the cost approval through AC4.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The additional partner costs on a held asset are recorded and approved against the asset, and the approval is what lets the cost be paid | FEAT-PRM-14 |
| BR2 | Maintenance, insurance and custody costs are recorded against the asset, and holding age drives re-appraisal and the provision step by rule | FEAT-AST-07; REQ-S5-003 |
| BR3 | Every repossessed or surrendered asset is recorded with its source, date taken in, holding cost and provision step | REQ-S5-001 |
| BR4 | Fees are calculated from the contracted schedule and paid against recorded results | REQ-S9-004 |
| BR5 | Every partner type is managed on the same six points, and contract and fees is the point this key exercises | REQ-S9-001 |
| BR6 | A new rule version applies to decisions taken from its effective date, and a decision keeps the version it was taken under | R-UNI-38 |
| BR7 | Where the decision log entry cannot be written, the action is blocked and no action proceeds unlogged | R-UNI-39 |
| BR8 | Every call is one hop on the owner's base with a 2 s budget, and the decision record is written through the local decision-record library on the shared topic and confirmed by the central ledger | DP-11, DP-13, DP-03; ADR-020, ADR-022 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E7017-APP, the asset holding record and its provision step are S5 rwb-asset's, and the recall and escalation context of R-UNI-25 to R-UNI-30 is what the run reads around the partner, never a state the harness sets.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| SENT | `PartnerResultSubmitted` on `rwb.partner.events.v1` | the partner records the cost claim against the instruction | IN_PROGRESS |
| IN_PROGRESS | `PartnerResultSubmitted` on `rwb.partner.events.v1` | the claim is the final one for the instruction | DONE |
| ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision record of the cost approval cannot be written (R-UNI-39) | EXCEPTION_QUEUE, with the instruction and the asset unchanged |
| ANY_ACTIVE | RULE_VERSION_EFFECTIVE | a new rule version reaches its effective date (R-UNI-38) | RESUME_STATE; the approval keeps the version it was decided under |

SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED are the instruction status values of DF-PRT-014, and DECISION_LOG_WRITE_FAILED and RULE_VERSION_EFFECTIVE are the events of R-UNI-39 and R-UNI-38, whose to_state is EXCEPTION_QUEUE and RESUME_STATE. The harness changes no state: S9 rwb-partner owns every instruction status above and drives InstructionWorkflow, S5 rwb-asset owns the asset holding record and the holding states it carries, and P3 rwb-case holds the case state the run reads. The panel status of DF-PRT-005 (ACTIVE, ON_NOTICE, SUSPENDED, EXITED) is a classification the run reads, not a transition it makes. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts; the holding states of the asset are read from S5's contract and the statement of which they are is Not specified in the source documents (GAP-0477; ASM-0669).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-NPAMGR, partner and agency manager | Holds Partner portal U and R; is the role the cost approval is written for and the role that records and approves the cost |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG | Hold U per the legacy section; record and approve the cost where their rights allow |
| RW-CASEOWN, RW-TEAMMGR, RW-LEGAL | Read the partner and the instructions where their rights allow; the R list of the legacy section names them |
| PT-AGENCY, partner user | Records the result of its own instruction on the portal, which is the claim the approval reads; holds Partner portal U per the legacy section |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S5 answers the asset and its holding fields; S9 runs InstructionWorkflow, answers the partner and instruction reads, records the claim and the approval and writes the decision record; P7 holds the central ledger; P3 holds the case; P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the approval is the manager's, and authorisation is answered by rwb-access and the DoA table of P4 |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset, held by S5 rwb-asset | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and 6 more, including transfer_in_date and stock_date | Read through the rwb-asset contract; the harness opens no view (DP-05) |
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and score | Read through the rwb-partner contract |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read through the rwb-partner contract; the claim and the approval write is S9's |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, inputs_ref | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, event_code | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. The legacy data section names v_ace_npa_asset with DF-ACE-208 to DF-ACE-219, and the split keeps the view with its owner: the asset and its holding fields are read through S5's contract, never from the view and never from a schema. `valuation_ext` is one of P1's four extension tables and is not read in this run. The asset is S5's, the partner and its instructions are S9's, the decision log and the rule rows are P7's, and the case behind the instruction is P3's. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/asset/v1/assets/{assetKey}` | S5 rwb-asset | The held asset and its holding fields: asset_key, asset_code, transfer_in_type, from_segment, book_value, transfer_in_date and stock_date (AC1, AC2, AC4) |
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The partner that holds the work, with partner_code, partner_type, panel_status and contract_end, filtered by the `type` and `status` parameters (AC1, AC2, AC5) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instruction the claim is made against, with its case, type, due time and status (AC1, AC2, AC3) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/results` | S9 rwb-partner | Records the additional-cost claim once against its instruction, and carries the approval (AC1, AC2, AC3, AC4, AC5) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of the cost approval, with its decision code and rule version (AC1, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state before and after the approval, and the consumer effect of the partner event (AC3, AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a read or a write (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13), and no operation is invented in this story: each path is the owner's published operation in the Ownership Map. Where a screen would compose them the path is the gateway-bff composite route (DP-19).

The legacy data section reaches the asset through `v_ace_npa_asset`, and DP-05 settles how that is read after the split: the harness reads no ACE view and no schema. The DF-ACE-208 to DF-ACE-219 fields reach it through S5's asset contract, because S5 rwb-asset owns the asset record and reads the view under its own login; `valuation_ext` is P1's and is not read here at all. The two legacy partner paths, `POST partner/instructions/{instructionId}/results` and `GET partner/instructions`, sit under the old monolith base `/api/recovery/v1`; in the target they are the S9 result write and the S9 instruction read on `/api/recovery/partner/v1`, both under DP-13.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.partner.PartnerResultSubmitted.v1` | `rwb.partner.events.v1` | S9 rwb-partner | Counts one publication per recorded claim and asserts the case effect once, with the replay proving one processed row per consumer, against the three consumers rwb-litigation, rwb-asset and rwb-case (AC3) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | S9 rwb-partner through the local decision-record library (DP-03) | Proves the decision record of the cost approval was published with its rule version and confirmed by the central ledger, and stays one entry after a replay (AC3, AC4) |

The harness subscribes to the two topics under one consumer group of its own, counts publications and replays each event once. The consumer effect it reads is the case through the rwb-case operation of §12.2; the inbox row counts of rwb-litigation and rwb-asset, the other consumers of `rwb.partner.PartnerResultSubmitted.v1` (Architecture v5 slide 43 row 21), come from the consumer evidence in the run fixture, because neither consumer exposes an operation in this story. `rwb.asset.AssetTakenOn.v1` on `rwb.asset.events.v1` (Architecture v5 slide 43 row 22) is the asset's own event and is published when an asset is taken on, and this run starts with the asset already held, so it is not on the run path and is not consumed here.

#### 12.5 Workflows and activities

None added. The harness observes two workflows and builds neither. InstructionWorkflow is S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace (Architecture v5 slide 17; Temporal design slide 25), and the run observes the `issueInstruction` and `recordResult` activities and the SLA timer that turns a missed service level into a chase and then a recall. AssetDisposalWorkflow is S5's child workflow of the case on the task queue `rwb-asset` (Architecture v5 slide 19; Temporal design slides 13 and 26), and the run observes that the asset it reads is the asset that workflow holds, without starting or signalling it. No workflow, activity, worker or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. JOB-19 re-appraisal is a Schedule of rwb-asset (Architecture v5 slide 44) and is observed only: the harness neither starts it, stops it, times it nor asserts its cron, overlap policy or catch-up window. Nothing in this run is started by clock.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); partner and partner_instruction are S9's, the asset and its holding record are S5's, decision_log_entry and rule_row are P7's, and recovery_case is P3's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-asset (asset read) | `GET /assets/{assetKey}` | Asset `AST-SYN-0017` with asset_code `NPA-SYN-0017`, transfer_in_type REPOSSESSION, from_segment NPA, book_value, transfer_in_date and stock_date, and the status HELD |
| Stub for rwb-partner (partner read) | `GET /partners` | Partner `PTR-SYN-0017` with partner_code, partner_type AGENCY, panel_status ACTIVE and contract_end 2027-12-31, filtered by the `type` and `status` parameters it is given |
| Stub for rwb-partner (instruction read) | `GET /partner/instructions` | Instruction `INS-SYN-001701` on case `RW-2027-001701` against asset `AST-SYN-0017`, with its instruction_type, instructed_at, due_at, status and result |
| Stub for rwb-partner (result write) | `POST /partner/instructions/{instructionId}/results` | Accepts the claim once per instruction, carries the approval, returns the instruction with its new status, and returns 409 on a second submission of the same claim |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One entry for the cost approval with its decision_code, rule_id, rule_version and inputs_ref, and the central ledger confirmation |
| Stub for rwb-case | `GET /cases/{caseId}` | Case `RW-2027-001701` with its state unchanged across the approval and the forced failure |
| Stub for rwb-access | `GET /me/session` | Allows RW-NPAMGR with Partner portal U and R; refuses a caller holding R and not U with 403 and MSG-P4-002 |
| Additional-cost fixture | The asset, the partner and the instruction, and the claim and the approval decided | The held asset, the panel partner and the instruction as data, the additional-cost claim with the fields the fixture names and the rule package version, at the point where S9's approval would answer |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic asset, partner, instruction and case keys, the stub answer shapes, the shape of the additional-cost claim, where the cost approval is recorded in S9 and in S5 (the Ownership Map publishes no cost-approval operation and no owned cost table), the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0477; ASM-0669).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.partner.PartnerResultSubmitted.v1` and `rwb.decision-record.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; InstructionWorkflow on `rwb-partner` and AssetDisposalWorkflow on `rwb-asset` observed, with the `issueInstruction` and `recordResult` activities and the SLA timer of the first |
| File | None. The run transfers no file and holds no document of its own |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 adds no dependency: the asset's ACE fields are read through the service that owns them, which is S5 rwb-asset, and the harness opens no view and calls no source-data operation. The H dependencies the table adds, RWB-PLT-E1027-CON for DP-03 and RWB-PLT-N001-CON for DP-19, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None; DP-05 and DP-13 add none. The only blocking dependency is the I story RWB-S9-E7017-APP, which replaces its stub, so the story is Day 1; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| CostRunner | Job | Runs the five owned criteria in order for one asset and holds the run lock |
| AssetProbe | Service | Reads the held asset and asserts asset_key, asset_code, transfer_in_type, from_segment, book_value, transfer_in_date and stock_date, naming the legacy field the value evidences |
| PartnerProbe | Service | Reads the partner with partner_code, partner_type, panel_status and contract_end |
| InstructionProbe | Service | Reads the instruction with its case, type, due time and status, and reads it again after the claim and after the forced failure |
| ClaimDriver | Service | Records the additional-cost claim once per instruction, carries the approval, retries a repeated submission and asserts the 409 |
| DecisionReadBack | Service | Reads the decision log and asserts one entry with its decision code and rule version, and the ledger confirmation |
| EventObserver | Service | Subscribes to `rwb.partner.events.v1` and `rwb.decision-record.v1`, counts publications and replays each event once |
| StubSet | Fake | The seven stubs and the additional-cost fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per asset keyed by story and asset_key, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S9-E7017-APP lands, on the synthetic held asset `AST-SYN-0017`, partner `PTR-SYN-0017`, instruction `INS-SYN-001701` and case `RW-2027-001701`, with the contract end and the rule package version held as fixture data. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the stub answer shapes, the shape of the additional-cost claim, where the cost approval is recorded in S9 and in S5, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0477; ASM-0669).

**Build steps**

1. Generate the seven stubs and the additional-cost fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the AssetProbe and prove the asset read answers the held asset with every field of AC2, including the DF-ACE-208 to DF-ACE-219 fields, through S5's contract and not from a view (DP-05).
3. Build the PartnerProbe and the InstructionProbe and prove the two S9 reads answer the partner and its instruction with every field of AC2 (X2).
4. Build the ClaimDriver for AC2 and AC3 against the instruction, and prove one claim per instruction, a 409 on a repeated submission and one claim left behind (X5).
5. Add the DecisionReadBack for AC1 and AC3: one decision record with its decision code and rule version, and the ledger confirmation before the approval is reported as recorded (X3, X4).
6. Add the EventObserver for AC3: one publication of each event, the case effect once, a replay that changes nothing, and one decision entry after the replay.
7. Add the forced decision-record failure for AC4 through the asset, partner and instruction reads before and after, so nothing changes is asserted and not assumed (X6).
8. Add the session read and the refused claim write for AC5, then the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S9-E7017-APP lands (X7).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S9-E7017-APP when it lands, and the wave entry check holds a run report keyed by story and asset_key.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. The legacy section carries these three messages for the feature and no asset-specific message, so none is invented here: MSG-GEN-001 with the missing field when a read is made short of a required parameter, MSG-P4-002 with the refused action on the claim write, and MSG-P7-003 when the decision record cannot be written and nothing changes.

### 15. Screens and states

The harness renders no screen: it observes the owners' operations and writes a report. The legacy section names SCR-34 Partner list and SCR-35 Placement and allocation, which belong to S9 and its CON story; the harness neither builds nor reads them, and it asserts their data through the partner read, the instruction read and the asset read.

| State | Read through | What the run asserts |
|---|---|---|
| ACTIVE, ON_NOTICE, SUSPENDED, EXITED (panel status) | rwb-partner partner read | The panel classification of the partner at the time of the cost approval (DF-PRT-005) |
| SENT, ACCEPTED, IN_PROGRESS, DONE, DECLINED, RECALLED (instruction status) | rwb-partner instruction read | The status of the instruction before and after the claim and the approval, and that a refused, failed or refused-right write leaves it unchanged (DF-PRT-014) |
| The held asset and its holding fields | rwb-asset asset read | The asset_key, asset_code, transfer_in_type, from_segment, book_value, transfer_in_date and stock_date are the same before and after every step, including the forced failure |
| The decision record of the cost approval | rwb-decision decision log | One entry with its decision code, rule version and inputs reference, confirmed by the central ledger |
| The case state | rwb-case case read | The case is unchanged by the approval and by the forced failure |
| EXCEPTION_QUEUE, RESUME_STATE | the rule rows and the instruction read | The blocked-action and rule-version context of R-UNI-39 and R-UNI-38, recorded by S9 and never set by the harness |

The environment, layout and retention of the run report are Not specified in the source documents (GAP-0477; ASM-0669).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-017-01-ITG | AC1 (legacy); ITG AC1 | End to end | One held asset, one partner on the panel and one instruction against the asset, with the cost claim and the decision record live |
| TC-E7-017-02-ITG | Legacy AC2 not recorded stays with RWB-S9-E7017-APP; ITG AC4 | Integration | The decision-record library forced to fail on the cost approval |
| TC-E7-017-03-ITG | Access; ITG AC5 | Component | A caller holding Partner portal R and not U |
| TC-E7-017-04-ITG | Principle 5; ITG AC4 | Integration | A forced decision-record failure with the asset, partner and instruction reads before and after |

The Covers column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx under the same legacy test case ID. Legacy AC2, the forced decision-log failure, stays with RWB-S9-E7017-APP and is asserted here at the cost approval through AC4.

### 17. Guardrails

- No business value in code: the asset, its holding fields, the partner, its type and panel status, the contract end, the instruction, the rule package version, the claim fields and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- ACE data only through the owner's contract or `v_ace_*` views: this run reads no ACE view at all, and the asset, partner, instruction, decision and case rows are read only through their owners' contracts (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- A field of the asset or the partner is evidenced or reported as a gap; it is never written up from a narrative.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-017 Manage extra costs and services on an asset | Recovery Workbench User Stories Epics 3 to 8 v3, lines 12881 to 12960 | Sections 1, 3, 10, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 12900 to 12904 | Section 7, AC1, marked (legacy RWB-E7-017 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E7-017-02 | The same, lines 12906 to 12910 and 12955 | AC4 asserts the same failure here; the legacy AC stays with RWB-S9-E7017-APP (section 19) |
| Legacy test cases TC-E7-017-01 to TC-E7-017-04 | The same, lines 12954 to 12957 | Copied as -ITG in section 16 |
| Legacy endpoints and permission checks | The same, lines 12923 to 12940 | Sections 12.2, 10 and 7 |
| FEAT-PRM-14 Manage extra costs and services on an asset | Epics 3 to 8 Specification v3, line 147 | Sections 1, 2 and 8 |
| FEAT-AST-07 Maintain a held property | Epics 3 to 8 Specification v3, line 73 | Sections 2 and 8 |
| FEAT-PRM-02 Hold the partner panel and fee schedule as data | Epics 3 to 8 Specification v3, line 135 | Sections 3 and 19 |
| REQ-S9-001 and REQ-S9-004 | Business Requirements Program v4, lines 430 and 433 | Section 8, BR4 and BR5 |
| REQ-S5-001 and REQ-S5-003 | Business Requirements Program v4, lines 361 and 363 | Section 8, BR2 and BR3; section 2 |
| R-UNI-25 to R-UNI-30 | Business Rules and Routing Logic v4, lines 429 to 434 | Sections 2 and 8 |
| R-UNI-38 and R-UNI-39 | Business Rules and Routing Logic v4, lines 442 and 443 | Sections 2, 7, 8 and 9 |
| The S5 asset contract, the S9 partner contract and the partner topic | Architecture v5 slides 17, 19 and 41; slide 43 rows 21 and 22 | Sections 2, 12.2 and 12.4 |
| AssetDisposalWorkflow and JOB-19 re-appraisal | Architecture v5 slides 19 and 44; Temporal design slides 13 and 26 | Sections 12.5 and 12.6 |
| InstructionWorkflow and the partner SLA timer | Architecture v5 slide 17; Temporal design slide 25 | Sections 12.5 and 9 |
| DF-ACE-208 to DF-ACE-219, DF-PRT-001 to DF-PRT-007, DF-PRT-008 to DF-PRT-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary | Section 11 |
| DP-03, DP-05, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application, and the metadata Patterns applied row |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v3 | Sections 8 and 12: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |

### 19. Out of scope

- RWB-S9-E7017-CON and RWB-S9-E7017-APP: the build of the recording and the approval of the additional partner cost, and the screen behind it.
- The S5 build: rwb-asset, the asset holding record, the holding states, the instruction cost line, AssetDisposalWorkflow and the JOB-19 re-appraisal Schedule.
- The S9 build: the panel and partner data, the instruction and result tables, InstructionWorkflow, the fee schedule reference data and the partner portal rights.
- The partner panel, fee schedule and service level reference data (FEAT-PRM-02) and the panel change (FEAT-ADM-07).
- The holding age, the re-appraisal order and the provision step as products: the harness reads the holding fields, it does not compute them.
- The recall and re-selection work of R-UNI-25 to R-UNI-30 as products: the harness asserts the context, it does not build the recall.
- Platform deployment and configuration, and the platform H dependencies named in section 13.
- Any production change: the harness runs in the test environment only.
