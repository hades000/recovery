# RWB-S9-E6035-APP Match a recovery and calculate the agency fee

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6035-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S9-L |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E6035-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the fee-calculation slice of RWB-E6-035 in rwb-partner. The two legacy criteria are kept word for word with their origin tag; the step matches the payment that arrives after charge-off to the case and the agency placement, works out the fee due from the contracted schedule in force, writes the result through the local decision-record library before any change (DP-03) and accrues it on `partner_instruction.fee_amount`, serves the fee-bearing read of `GET /partner/instructions` on base `/api/recovery/partner/v1` (DP-13) behind SCR-35 and SCR-34 through the gateway-bff composite route (DP-19), and moves no instruction status and no case state, because `PAYMENT_MATCHED` is the D9 state of rwb-writeoff. The contracted fee schedule has no table, no field, no rate and no basis in any source, the legacy data table carries no payment or recovery entity, the plan's C row is empty while four rows are consumed, DP-04, DP-06, DP-07, DP-10 and DP-16 are absent from the pattern set, TSD S8-style requirement tracing maps every REQ-S9 row to FEAT-PRM-01 or FEAT-PRM-08, and no event of the service carries the fee (GAP-3119; ASM-5404, ASM-5405, ASM-5406, ASM-5407, ASM-5409, ASM-5412). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the Workbench to match money recovered by an agency to the case and work out the fee due**, so that **partners are placed, paid and measured by rule**.

This is the fee-calculation slice of legacy RWB-E6-035. It owns:

- the two legacy criteria this story owns (AC1, AC2), copied verbatim with their origin tag, and the messages, the reads and the two screens they depend on;
- one step of `InstructionWorkflow` on task queue `rwb-partner` in namespace `rwb-recovery`: the step that runs when the payment of a case placed with an agency arrives (FSD S9 A2.7.2; Business Rules and Routing Logic v4 row R-WO-37; ASM-5403, ASM-5408);
- the match of that payment to the case and to the one open instruction of that case held by the agency, on `partner_instruction.case_id` and `partner_instruction.partner_id` (TSD S9 T3.1, T3.3);
- the fee due, worked out from the contracted fee schedule in force and the recorded result of the instruction, and written to `partner_instruction.fee_amount` (DF-PRT-016), the only fee field any source publishes (ASM-5405);
- the record of the match and the fee through the local decision-record library, with the package version in force, **before any change**, because AC1 asks for the result in the decision log with the rule version (DP-03; ASM-5406);
- the fee-bearing read of the published `GET /partner/instructions` (API-S9-003) on base `/api/recovery/partner/v1`, with the Partner portal right R and the scope applied (DP-13);
- SCR-35 Placement and allocation and SCR-34 Partner list in their list states behind the gateway-bff composite route, where the manager sees the matched recovery and the fee due (DP-19).

It does not own: the published shapes of the two reads, the `Partner`, `PartnerInstruction` and `InstructionPage` elements, the fee properties, the consumed rows, the rights, the error set and the fakes, which are RWB-S9-E6035-CON; the panel, the fee schedule and the service levels as reference data (FEAT-PRM-02, the reference-data story of the module); the allocation and the override (FEAT-PRM-03, FEAT-PRM-04); the result submission (FEAT-PRM-05) and the placement (FEAT-PRM-06); the fee claim and its approval, which is FEAT-PRM-09 on `POST /partner/instructions/{instructionId}/invoices` (ASM-5413); the post charge-off posting and the move to `PAYMENT_MATCHED`, which are rwb-writeoff's D9 route; the case of record, which is rwb-case (P3); the payment of record, which is rwb-payment (P8); the rule package, which is rwb-decision (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The objective, the problem and the metric are unchanged from the legacy story and the module FSD: partners are instructed and paid by email and spreadsheet and allocation is not based on performance, so the Workbench matches the money an agency recovers to the case and works out the fee due (FSD S9 A1.3, A2.7.1). Placements by scorecard are measured on the decision log and the Workbench records against a target of 100 percent, reviewed monthly (FSD S9 A2.7.1). What D-RCV-60 changes is who owns the case, the payment, the schedule, the package and the screens.

- **The instruction is this service's.** `partner` and `partner_instruction` are S9's in `rwb_partner` (context pack, ownership rows owned by S9; TSD S9 T3.1), and `fee_amount` (DF-PRT-016) is the fee the agency is due on that instruction, so the calculation lands on a column this service owns.
- **The money is not.** The legacy data table names `recovery_case`, `partner`, `decision_log_entry` and `rule_row` and no payment entity, and FSD S9 A2.7.2 names ALS and GL as the integration point with FEAT-PAY-01 as its prerequisite, so the matched money arrives from rwb-payment and is never a table of this service (GAP-3119; ASM-5404).
- **The schedule is not published.** FEAT-PRM-02 promises panel, fee schedule and service levels as versioned reference data, yet TSD S9 T3.1 lists no schedule table and no rate, tier or basis, and the FSD leaves A2.7.3.2 (the field catalog) out of the feature. The schedule therefore arrives as versioned reference data with a placeholder shape, and the fee is written only to `fee_amount` (GAP-3119; ASM-5405, ASM-5407).
- **The route state is not ours.** R-WO-37 moves the write-off route from `PLACED_WITH_AGENCY` to `PAYMENT_MATCHED`; that is rwb-writeoff's D9 machine and the Write-off module's row, and the S9 instruction status has no such member (LOV-INSTR-STATUS), so this step accrues a fee and moves nothing (ASM-5408).
- **The package is read, not embedded.** The rule package registry is rwb-decision's by the default ruling and DP-04 is not in this key's pattern set, so the version in force arrives on the package read and is recorded with the fee; no published rule row expresses the fee itself (ASM-5406).
- **Nobody acts.** FSD S9 A2.7.3.3 gives "None; runs unattended" as the primary role and the Partner and agency manager as the also-uses role, and the legacy permission table gives the Partner portal right R only, so the calculation has no user command and the manager reads the result (ASM-5410).
- **The measure has no event.** The service publishes EV-20 and EV-21, named InstructionIssued and PartnerResultSubmitted in TSD S9 T5.3, and neither carries a fee, so the fee rests on the instruction row and the decision-record ledger (GAP-3119; ASM-5409).

No business value moves: the instruction type, the panel and partner lists, the fee basis, the rounding and the package version are reference data and rule data, read with their version and never written in code (FSD S9 BR-S9-007).

### 3. Preconditions

- RWB-S9-E6035-CON is published: the `Partner`, `PartnerInstruction` and `InstructionPage` elements with their required flags and lists, the fee properties of the answer, the consumed rows, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-payment posted-payment read is published with its fake: the payment of the case after charge-off with its reference, its amount, its value date and its case reference. The operation name is Not specified in the source documents (GAP-3119; ASM-5404).
- The rwb-case case read is published with its fake and answers the case with its route state (ASM-5404).
- The rwb-case reference-data read is published with its fake and answers the contracted fee schedule of the partner type and instruction type at a date, with its version; the schedule's columns, tiers and rounding are Not specified in the source documents (GAP-3119; ASM-5405, ASM-5407).
- The rwb-decision package read is published with its fake and answers the partner package at its version in force (ASM-5406).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-35 and SCR-34 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `partner` and `partner_instruction` exist in schema `rwb_partner` from the DB story of this service, with the columns of DF-PRT-001 to DF-PRT-016 and the standard record columns of TSD S9 T3.0; this story adds no table, no column and no migration.
- The placement is in place: the case was placed with the agency under R-WO-30 and the agency accepts and reports on the portal under R-WO-30, R-WO-33 and API-S9-004, API-S9-005, which the E4 and E6 stories of the module own.
- The service runs as its own login on schema `rwb_partner`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, `rwb_payment`, `rwb_decision` or an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E6035-CON when its tests pass.

### 4. Flow

1. The payment of a case placed with an agency is posted after charge-off and reaches this service as the trigger, on the interface rwb-payment publishes, inside the next working day that R-WO-37 sets. Whether the trigger is an event or a scheduled read is Not specified in the source documents (FSD S9 A2.7.2; GAP-3119; ASM-5403, ASM-5404).
2. `InstructionWorkflow` starts the step `matchAgencyRecovery` on task queue `rwb-partner`, which is the service's one workflow in the context pack's ownership rows.
3. The service reads the payment on the rwb-payment contract: its reference, its amount, its value date and its case reference. One payment, one step.
4. The service reads the case on the rwb-case contract and checks that the payment belongs to a case in the write-off route held by an agency (ASM-5404).
5. The service reads `partner_instruction` in `rwb_partner` for that case and that agency: its reference, its type, its instructed and due dates, its status and its recorded result code. Exactly one open instruction of that case held by that agency is expected (DF-PRT-008 to DF-PRT-015); no open instruction, or more than one, is exception path X3.
6. The service reads `partner` in `rwb_partner` for the panel status and the contract end of the agency: a partner that is not on the panel, or whose contract has ended, is refused at X3 (DF-PRT-005, DF-PRT-006).
7. The service reads the contracted fee schedule as versioned reference data for the partner type, the instruction type and the payment date, and holds its version (FEAT-PRM-02; ASM-5405, ASM-5407).
8. The service reads the partner package version in force on the rwb-decision contract and holds it for the record; no rule row of the module expresses the fee (ASM-5406).
9. `AgencyFeeCalculator` works out the fee due from the schedule in force and the recovered amount matched to the case and the placement, and applies the rounding the schedule carries; the rate basis, the tiers and the rounding are Not specified in the source documents (GAP-3119; ASM-5405).
10. `PartnerDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the instruction reference, the partner reference, the payment reference, the recovered amount, the schedule version, the package version, the fee due and the calculated-at time. A failed write stops the step with nothing changed (DP-03; AC1, AC2).
11. `calculateAgencyFee` accrues the fee on `partner_instruction.fee_amount` (DF-PRT-016) in the same transaction as the record. No other column of the table is written: the status, the result code and the dates stand (ASM-5408).
12. No instruction status and no case state moves: `PAYMENT_MATCHED` is rwb-writeoff's D9 state, and the posting of the recovery as post charge-off income is the write-off and payment route's step, not this one.
13. The fee is answered on `GET /partner/instructions` (API-S9-003) with its decision-record reference, and the manager sees the matched recovery and the fee due on SCR-35 and SCR-34 through the composite route (DP-19).
14. A repeated trigger for the same payment answers the fee that exists and writes no second one, matched on the payment reference and the instruction reference. No account number, identity number or contact value is copied into the record, the answer or a log.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no fee is accrued and `fee_amount` keeps its value | MSG-P7-003 | AC2, TC-E6-035-02, TC-E6-035-04 |
| X2 | The role does not hold the Partner portal right R | 403 before any read; nothing changes and no fee is shown | MSG-P4-002 | TC-E6-035-03 |
| X3 | The payment does not match the case and the placement: no open instruction of that case held by that agency, more than one, or a partner off the panel or out of contract | Nothing is written and nothing is accrued; a task is raised for the partner and agency manager, because R-WO-37 makes the match its condition | Not specified in the source documents (GAP-3119; ASM-5404, ASM-5405) | AC1 |
| X4 | The contracted schedule in force carries no row for that partner type, instruction type and payment date | Nothing is written and nothing is accrued; a task is raised for the reference-data administrator | Not specified in the source documents (GAP-3119; ASM-5405) | AC1 |
| X5 | rwb-payment, rwb-case, rwb-decision or the reference data does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written; the caller sees 503 with the platform error envelope | None | AC1, X2 |
| X6 | The payment or the product it rests on is stale after a late or failed ACE batch | The step holds and nothing is accrued until the product carries today's business date | MSG-P1-001 | AC1 |
| X7 | A repeated trigger for the same payment | One fee, one record and one answer; the repeat answers what exists and is counted | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `payment` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR6 |

X1 and X2 are the legacy exception paths carried onto the slice (the legacy set also carries MSG-GEN-001, kept in section 14), X3 to X7 are the paths the target call types and the unattended trigger add, and X8 is the ACE and schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E6035-CON, the rwb-payment, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P7, P8 or P3 |
| Negotiable | The activity names, the record's internal shape and the fee-property names of the answer are this story's and the baseline's choice; the reads, the right, the message set, the three screens and the two criteria are fixed |
| Valuable | The money an agency recovers is matched to the case and the fee due is on the instruction with the schedule and package versions that were in force, instead of on a spreadsheet |
| Estimable | One workflow step, one calculator, one record write, one column write, one read branch, four clients and two list screens |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic placed case through the contract fakes, plus the no-instruction, no-schedule, stale-product and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Match a recovery and calculate the agency fee

  Background:
    Given case "RW-2026-000611" was placed with agency "AG-014" and carries one open instruction of type "COLLECT"
    Given the partner package is in force at its version and the contracted fee schedule is in force with its version
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Match a recovery and calculate the agency fee (legacy RWB-E6-035 AC1)
    Given the rwb-payment contract mock returns the payment after charge-off that matches the case and the placement
    Given the rwb-case contract mock returns the case and its reference-data read the contracted fee schedule in force
    Given the rwb-decision contract mock returns the rule version in force
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then matches money recovered by an agency to the case and works out the fee due
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E6-035 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E6-035 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `its trigger arrives` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 carries three `Given the <service> contract mock returns <x>` lines, and those are the only additions. AC2 has no cross-service part and is copied with nothing added. The same outcome is the one FSD S9 AC-S9-007-01 records as written one epic ahead — "The data and rules it needs are in place / The trigger arrives / The result is recorded with its rule version" — so the legacy line and the module line agree. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_partner`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

The two rows below are the published rows of the module for this feature, copied character for character; both are S9's own and this story implements the second.

| Rule ID | Rule | Message |
|---|---|---|
| VR-S9-007-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S9-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

The routing row below is the D9 row this step implements, copied character for character from the Write-off route set; it is rwb-writeoff's row and this step provides its fee half only.

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-37 | Write-off | D9 | PLACED_WITH_AGENCY | PAYMENT_RECEIVED_AFTER_CHARGEOFF | the payment matches the case and the placement | Post the recovery as post charge-off income and calculate the agency fee | PAYMENT_MATCHED | Workbench | ALS core and GL, Agent Runtime | next working day |
| R-WO-33 | Write-off | D9 | PLACED_WITH_AGENCY | AGENCY_REPORTED_RESULT | the result is reported on the portal | Attach contact, promise and cash to the case the same day | PLACED_WITH_AGENCY | Outsourced agency | OA portal, Partner Portal | same day |

Their owner and systems columns name a business role and systems, not services: "Workbench" is the case of rwb-case and this service's own instruction read through the composite route, "ALS core and GL" is the payment leg that lands in rwb-payment, and "Agent Runtime" is rwb-agent, which this step does not call.

| ID | Rule | Source |
|---|---|---|
| BR1 | The fee accrues on `partner_instruction.fee_amount` (DF-PRT-016) and no other column of the table is written: the status, the result code and the dates stand | TSD S9 T3.1; FSD S9 A2.7.2; ASM-5408 |
| BR2 | The result is recorded before anything else happens, with the schedule version and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S9 T2 ("writes the decision log entry before any change"); legacy AC1 and AC2 |
| BR3 | Only a payment that matches the case and the placement is matched: one open instruction of that case held by that agency, on the panel and in contract | Business Rules and Routing Logic v4 row R-WO-37; FSD S9 A2.7.2 |
| BR4 | The fee is worked out from the contracted schedule in force and the recorded result of the instruction, never from a constant, a percentage or a default in code | FSD S9 BR-S9-007; REQ-S9-004 text; ASM-5405 |
| BR5 | The payment and the case are read from rwb-payment and rwb-case and never from an ACE table or a `v_ace_*` view; the staleness signal arrives on the owner's read | DP-05 as a prohibition; BR-S9-007 stale rule; ASM-5404, ASM-5407 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_partner`; `case_id` and `partner_id` are identifiers of another service's fact | DP-01; TSD S9 T3.1, T3.3 |
| BR7 | The schedule version and the package version in force are recorded with the fee; no rule row of the module expresses the fee, so no rule ID is recorded as the fee's own | ASM-5406; Business Rules and Routing Logic v4 Rules sheet |
| BR8 | The step is unattended and has no command of its own: the manager reads the fee on the instruction read with the Partner portal right R | FSD S9 A2.7.3.3; legacy Permission checks; ASM-5403 |
| BR9 | The same payment twice accrues one fee and writes one record; the repeat is matched on the payment reference and the instruction reference | TSD S9 T-A.2 (no `Idempotency-Key` on the reads); ASM-5403 |
| BR10 | No account number, identity number, contact value or person name enters `rwb_partner`, the decision record, a log or a workflow input; the payment reference is a key | Template and Rules §R7.2 (s17); TSD S9 T6.2 |

### 9. State transitions

The instruction status and the case route state are not changed by this story. `PAYMENT_MATCHED` is a state of the D9 write-off route, not of the S9 instruction, and LOV-INSTR-STATUS carries no fee member.

| From (instruction status, rwb-partner) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `IN_PROGRESS` | A payment matched and a fee calculated | One open instruction of the case and the agency | `IN_PROGRESS`, unchanged; `fee_amount` accrues | this story (BR1) |
| `DONE` | A payment matched and a fee calculated | The instruction is closed and the fee still accrues on it | `DONE`, unchanged; `fee_amount` accrues | this story (BR1) |
| Any status | A payment that matches no open instruction of that case and agency | The match fails | Unchanged | none; X3 |
| `RECALLED` | A payment matched | The placement was recalled | Unchanged | none; X3 |
| `IN_PROGRESS` | `ACCEPTED` | The agency accepts under API-S9-004 | `ACCEPTED` | the E4 instruction stories |
| `IN_PROGRESS` | `DONE` | The result is reported and accepted under API-S9-005 | `DONE` | the result story (FEAT-PRM-05) |

| Write-off route (rwb-writeoff, D9) | Event | Condition | To |
|---|---|---|---|
| `PLACED_WITH_AGENCY` | `PAYMENT_RECEIVED_AFTER_CHARGEOFF` | the payment matches the case and the placement | `PAYMENT_MATCHED`, on rwb-writeoff's R-WO-37, not here |
| `PLACEMENT_DECIDED` | `SOFT_RECOVERY_SELECTED` | an agency on the panel has capacity | `PLACED_WITH_AGENCY`, before this step |

The D9 states are those of the Write-off route set of the Business Rules and Routing Logic v4 and the States sheet; the instruction states are LOV-INSTR-STATUS of TSD S9 T3.2. This step writes neither state machine.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG, partner and agency manager | Partner portal CRUDA in TSD S9 T6.1: the also-uses role of FSD S9 A2.7.3.3, reads the fee and the record on SCR-35 and SCR-34, and is the role a task is raised to when the match fails (X3) |
| RW-CASEOWN, RW-TEAMMGR, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL, RW-TRIBE | Partner portal R: read the instruction and its fee in scope |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT | Partner portal CRU in the matrix; the three rights beyond R belong to other stories of the module |
| RW-HEADLIT, RW-HEADNPA, RW-HEADASL | Partner portal RA: read and approve, no fee command |
| PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC | Partner portal RU: the partner sees the instruction and its own fee, and never acts on the calculation |
| rwb-partner service identity | Runs the match and the calculation and writes the record and `fee_amount`; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S9 T6.1 and nothing wider. The partner portal column gives R or better to all 29 identities of the matrix: the eight roles the legacy permission table names plus "and 21 more", which the matrix resolves to the remaining 21 (ASM-5410). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-008 | partner_instruction (S9, `rwb_partner`) | id | Read, the instruction reference recorded with the fee |
| DF-PRT-009 | partner_instruction (S9, `rwb_partner`) | case_id | Read, the match key of the payment |
| DF-PRT-010 | partner_instruction (S9, `rwb_partner`) | partner_id | Read, the match key of the agency |
| DF-PRT-011 | partner_instruction (S9, `rwb_partner`) | instruction_type | Read, the key of the schedule row in force |
| DF-PRT-012, DF-PRT-013 | partner_instruction (S9, `rwb_partner`) | instructed_at, due_at | Read, the dates the fee is measured from |
| DF-PRT-014 | partner_instruction (S9, `rwb_partner`) | status | Read, the open instruction the match requires (LOV-INSTR-STATUS) |
| DF-PRT-015 | partner_instruction (S9, `rwb_partner`) | result_code | Read, the recorded result the fee is paid against (REQ-S9-004) |
| DF-PRT-016 | partner_instruction (S9, `rwb_partner`) | fee_amount | **Write**, the fee due: numeric(18,2); the only fee the sources publish |
| DF-PRT-001 to DF-PRT-007 | partner (S9, `rwb_partner`) | id, partner_code, partner_name, partner_type, panel_status, contract_end, score | Read: the panel status and the contract end are the match's condition; the partner type is the schedule key; the name is read for the screen and not copied to a record |
| Standard columns | both tables (S9, `rwb_partner`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Written by the row's own transaction on `partner_instruction`, as TSD S9 T3.0 gives them |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_partner`) | rule id, rule version, decision code, inputs reference, reason, from and to state, decided at | Write through the local library, before anything else: the payment reference, the recovered amount, the schedule version, the package version, the fee due and the calculated-at time |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the package version arrives on the package read |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case reference arrives on the payment and the case itself on the case read |
| The payment | rwb-payment (P8) | reference, amount, value date, case reference | Read as request inputs of the step; no field ID, table or value format in any source: Not specified in the source documents (GAP-3119; ASM-5404) |
| The contracted fee schedule | reference data (rwb-case, P3, by the default ruling) | partner type, instruction type, effective dates, basis, tiers, rounding, version | Read with its version; no table, column, rate or basis in any source (GAP-3119; ASM-5405, ASM-5407) |

Field IDs are those of TSD S9 T3.1 and the Logical Data Model and Data Dictionary, and the case and rule rows are the rows the legacy Data table lists, with their owners changed to P3 and P7 by the target. **No new table, no new column and no migration**: the two tables arrive with the DB story of this service, the fee is accrued on DF-PRT-016, and `decision_record` and `idempotency_key` are library objects created in `rwb_partner` by the library's own migration (DP-03). `outbox_event` also sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3).

**No personal data.** The rows carry identifiers, codes, dates, amounts, list values, two versions and one reference. The payment reference is a key: no account number, card number, identity number, address or person name is read into the record, the answer, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). This story supplies the fee-bearing read of the instruction list and the partner list, whose shape RWB-S9-E6035-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/partner/instructions` (API-S9-003) | Query status, page, size in; `InstructionPage` out, each instruction with its matched recovery and its `feeAmount` and decision-record reference | Partner portal, right R, scope applied | Not applicable |
| GET | `/partners` (API-S9-001) | Query type, status in; `Partner[]` out with panel status and score | Partner portal, right R, scope applied | Not applicable |

The errors are 401, 403 with MSG-P4-002 and 503 when library or a consumed contract does not answer, which is the error set TSD S9 T-A.2 publishes for both operations; the reads themselves are published and need no placeholder. The fee properties of the answer and the payment-reference format are what the baseline fixes with a placeholder (§12.8; GAP-3119; ASM-5405). The invoice operation `POST /partner/instructions/{instructionId}/invoices` (API-S9-006) is the partner's fee claim and belongs to the fee-approval story of E7, not here (ASM-5413).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The posted-payment read (operation name Not specified in the source documents (GAP-3119; ASM-5404)) | `/api/recovery/payment/v1` | P8 rwb-payment | The payment of the case after charge-off with its reference, amount, value date and case reference; faked |
| The case read (operation name Not specified in the source documents (GAP-3119; ASM-5404)) | `/api/recovery/case/v1` | P3 rwb-case | The case of the payment and its write-off route state; faked |
| The reference-data read of the contracted fee schedule and the LOVs (operation name Not specified in the source documents (GAP-3119; ASM-5407)) | `/api/recovery/case/v1` | P3 rwb-case | The schedule in force with its version; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3119; ASM-5406)) | `/api/recovery/decision/v1` | P7 rwb-decision | The partner package at its version; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All four rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3119; ASM-5404, ASM-5406, ASM-5407).

#### 12.3 Events published

None. The service publishes on `rwb.partner.events.v1` and its event set carries EV-20 and EV-21, named InstructionIssued and PartnerResultSubmitted in TSD S9 T5.3; which ID carries which name is Not specified in the source documents (GAP-3119; ASM-5409). An instruction issued is the placement's fact and a result submitted is the result story's, and neither carries a fee, so this story declares no event, no producer group and no outbox row, and a build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry.

#### 12.4 Events consumed

None. TSD S9 T5.3 names the two published events and no consumed event, and the context pack's ownership rows give the service no consumer group; the payment fact therefore arrives on rwb-payment's contract read, and if the payment owner publishes an event the row of §12.2 moves here without a change of this story's behaviour (GAP-3119; ASM-5404). A build that adds a consumer group, a subscription or an inbox of its own fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction, continues-as-new with the case stage | `rwb-partner` in namespace `rwb-recovery` | Input: the case reference, the instruction reference and the trigger; outcome for the parent: the fee accrued or the task raised |
| `matchAgencyRecovery` | Activity, the match step | `rwb-partner` | The payment reference, the case reference and the agency in; the instruction reference and the matched amount out |
| `calculateAgencyFee` | Activity, the fee step | `rwb-partner` | The instruction reference, the schedule and package versions and the recovered amount in; the fee due, the record reference and the accrued column out |

The service owns one workflow and no job in the context pack's ownership rows (Workflows: 1, Jobs: 0). The two activity names are a target design choice fixed by no source document, and the trigger's delivery is recorded in §12.6 (ASM-5403).

#### 12.6 Schedules

None declared here. R-WO-37 measures the step at "next working day", and FSD S9 A2.7.2 gives the trigger as "a completed ACE batch, an event or a timer"; whether that is an event-started workflow or a Temporal Schedule in this service is Not specified in the source documents (GAP-3119; ASM-5403). The service owns no job, no Quartz row and no shared job table, and the daily scan of the write-off route is rwb-writeoff's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| partner | S9 (`rwb_partner`) | The outside firm, its type, panel status and contract end; read only here |
| partner_instruction | S9 (`rwb_partner`) | Work placed with a partner on a case; this story reads it and writes `fee_amount` |
| partner_user | S9 (`rwb_partner`) | The partner's own portal users; not read by this story |
| decision_record | PLT library, created in `rwb_partner` | The local hash-linked decision record of the match and the fee (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of the write operations of the module; the two reads declare none (§12.1) |
| outbox_event | PLT library, created in `rwb_partner` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` (P3), `payment` (P8), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6). No foreign key leaves the schema and `case_id` and `partner_id` are identifiers, not foreign keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment posted-payment fake | The payment after charge-off for `RW-2026-000611`, and a payment that matches no placement | AC1, X3 |
| rwb-case case fake | The case with its write-off route state and its party reference | AC1 |
| rwb-case reference-data fake | The contracted fee schedule in force at a date, by partner type and instruction type, with its version; and a date with no row | AC1, X4 |
| rwb-decision rule-package fake | The partner package at its version in force | AC1 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-35 and SCR-34 answers before and after the fee, for `RW-2026-000611` and `AG-014` | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the three consumed owners and the schedule's shape carry the placeholder until their owners confirm them (GAP-3119; ASM-5404, ASM-5405, ASM-5407).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | `/api/recovery/partner/v1/partner/instructions` and `/partners`; the payment read, the case read, the reference-data read and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 belong to the placement and the result; no event of this step (§12.3, §12.4) |
| Temporal | 1 workflow and 2 activities | `InstructionWorkflow`, `matchAgencyRecovery` and `calculateAgencyFee` on `rwb-partner`; no Schedule declared |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `fees`; front end `src/modules/recovery/partner/PlacementAllocation.tsx` and `PartnerList.tsx`, the fragments SCR-35 and SCR-34 embed.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the `fee_amount` update commit together or not at all. DP-13 moves the base of the legacy paths and gives the two reads their home. DP-19 is how SCR-35 and SCR-34 reach this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-06 and DP-07 (the parameters and reference-data contracts), DP-10 (the workflow kit) and DP-16 (the integration contract) are real dependencies of the step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3119; ASM-5404, ASM-5405, ASM-5406, ASM-5407).

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the package is read as data and applied by this service's own calculator, so no kit is declared. The reference-data contract of DP-07 would add `RWB-PLT-E1043-CON` and `RWB-P3-E1043-CON`, and the workflow kit of DP-10 `RWB-PLT-E1071-CON`; both are recorded as absent. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `InstructionWorkflow` fee branch | Workflow | Receives the payment trigger on the instruction stage, reads the versions in force and reports the outcome to the parent |
| `matchAgencyRecovery` | Activity | Reads the payment, the case, the instruction and the partner and binds them under R-WO-37's condition |
| `calculateAgencyFee` | Activity | Reads the schedule and the package, works out the fee and accrues it with the record in one transaction |
| `AgencyFeeCalculator` | Service | The fee over the schedule in force: the basis, the tiers and the rounding the schedule carries, never a constant |
| `PartnerDecisionRecordWriter` | Library adapter | Writes the record with both versions before anything else, hash-linked; refuses the step when the write fails |
| `InstructionController` | Controller | The two reads, the Partner portal right R, the scope and the problem mapping |
| `PaymentClient`, `CaseClient` | Clients | The payment read of rwb-payment and the case read of rwb-case, one hop, 2 s, breaker, no retry of their own |
| `ReferenceDataClient`, `RulePackageClient` | Clients | The schedule read with its version and the package read at its version |
| `PlacementAllocation`, `PartnerList` | React components | Show the matched recovery and the fee due on SCR-35 and SCR-34, read only |

**Database and migrations.** No Flyway file. The two tables arrive with the DB story of this service, and the record is a library object created in `rwb_partner` by the library's migration (DP-03). No column is added for the schedule, the rate or the recovered amount: none has a source, and the fee lands on DF-PRT-016 (ASM-5405).

**Configuration and reference data.**

- The schedule basis, the tiers, the rounding, the partner and instruction lists and the package version: reference data and rule data with their version, never written in code (ASM-5405, ASM-5406).
- The schedule's columns, the rate basis and the rounding: placeholders until the business lead confirms them (ASM-5405).
- The capability area "Partner portal" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the "next working day" of R-WO-37 is the measure of the step, not a timer this story owns.

**Build steps**

1. The fee branch of `InstructionWorkflow` and its input record, registered on `rwb-partner`, with the payment trigger as its start.
2. `PaymentClient` and `CaseClient` against their fakes, with the 2 s budget, the breaker and the payment-that-matches-nothing path (AC1, X3, X5).
3. `ReferenceDataClient` against its fake, with the schedule in force, its version and the no-row path (AC1, X4).
4. `RulePackageClient` against its fake, with the version in force recorded with the fee (AC1).
5. `AgencyFeeCalculator` over the schedule, with the basis, the tiers and the rounding driven by data and the no-schedule path (AC1).
6. `PartnerDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC2, X1).
7. `calculateAgencyFee` accruing `fee_amount` in the record's transaction, with the repeated-trigger path (AC1, X7).
8. `InstructionController` with the two reads, right R, the scope and the problem mapping, and the two screen fragments through the composite route fake (AC1, X2).
9. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no write to `rwb_case`, `rwb_payment` or any other schema, and no write to a column of `partner_instruction` other than `fee_amount` (X8, BR1, BR6).

**Feature flag.** `rwb.partner.agency-fee-v1`, a flag of the platform library; off means the step does not run and the instruction read answers with no `feeAmount`, and the placement, result and approval stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic placed case in SIT, the fee is accrued with the schedule and package versions in force, a payment that matches no placement and a date with no schedule row are refused, a repeated trigger accrues once, a forced record failure changes nothing, no `recovery_case`, `payment` or `v_ace_*` read and no column write other than `fee_amount` exists in the build, and SCR-35 and SCR-34 answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | Carried from the legacy message set of RWB-E6-035: a required element of the step or of a read is absent or invalid. No field of this step is mandatory in any source, so it is kept and not raised here | Enter {field}. |
| MSG-P1-001 | A data product or the payment is stale after a late or failed ACE batch for its source (VR-S9-007-1, X6) | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | A role without the Partner portal right R calls one of the two reads (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the fee is accrued (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set and of the module rule VR-S9-007-1; the text is the legacy and FSD wording, copied unchanged, and no message is reworded and no new one is added. The task raised at X3 and X4 carries no published message, so its text is the placeholder of §5.

### 15. Screens and states

SCR-35 Placement and allocation and SCR-34 Partner list are served through the gateway-bff composite route (DP-19). The route calls rwb-partner for the instruction, the partner and the fee, rwb-case for the case and its route state and rwb-payment for the payment; this story fixes the rwb-partner answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives SCR-35 "Loading; list" and SCR-34 "Loading; list", and the FSD gives SCR-35 as "Work placed with partners by rule, with recalls and re-selection" and SCR-34 as "Partners, contracts, panel status and scorecards" (FSD S9 Screens). This story produces the fee from the list state of both: a matched instruction shows its recovered amount, its fee due and its record reference, and no screen carries a fee command. Neither screen is described as a calculation screen, so the place of the fee on it is Not specified in the source documents (GAP-3119; ASM-5405). The refusal, stale-product and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-035-01 | AC1 | Component | The placed case `RW-2026-000611` with agency `AG-014` on the fakes; the payment, the case, the schedule, the package version, the record and `fee_amount` asserted |
| TC-E6-035-02 | AC2 | Component | The decision-record stub stopped; nothing accrued and MSG-P7-003 shown |
| TC-E6-035-03 | Access | Component | A role without the Partner portal right R; 403 with MSG-P4-002 and no read |
| TC-E6-035-04 | Principle 5 | Component | A forced decision log write failure inside the transaction; `fee_amount` keeps its value and no record exists |

The four legacy cases are those of RWB-E6-035 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the schedule basis, the tiers, the rounding, the partner and instruction lists, the states, the right and the package version stay reference data and rule data, never a constant, a default or a branch.
- No personal data in `rwb_partner`, in a workflow input or in a log: identifiers, codes, dates, amounts, two versions and one reference only, and every fixture is synthetic. The payment reference is a key and never an account or card number.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and the staleness signal arrives on the owner's read (BR5).
- The case stays with rwb-case and the payment with rwb-payment: no `recovery_case` row, no `payment` row and no state of either is written here.
- The instruction row is read, not rewritten: only `fee_amount` is set, and no status, result code or date moves (BR1).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no data-lake path.
- The record is written before the accrual; a build that accrues outside the record's transaction fails the review (DP-03).
- The invoice operation and the fee approval are not built here: a build that declares a write on `POST /partner/instructions/{instructionId}/invoices` fails the review (ASM-5413).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-PRM-07 | The requirement this feature serves is Not specified in the source documents (GAP-3119; ASM-5412): TSD S9 T8 maps every REQ-S9 row to FEAT-PRM-01, FEAT-PRM-08 or a placeholder, and maps REQ-S9-004 — whose text names the contracted fee schedule — to FEAT-PRM-01 | The trace rests on the legacy key, the feature row and AC1 | TC-E6-035-01 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the partner panel and its instructions | TC-E6-035-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-E6-035-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-E6-035-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the fee is accrued | TC-E6-035-02, TC-E6-035-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-035, disposition Split (rework); feature FEAT-PRM-07 |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Wave and release | Wave 4 and release 30 April 2027 (tentative), copied unchanged from the plan; EP06 is wave 4 and the service's Arch v5 wave is 4, so the W-MAP wave is not earlier and no conflict is raised (ASM-5411) |
| Source text | Legacy RWB-E6-035; FSD S9 Partner management v3 A1.1, A2.7, A2.7.2, A2.7.3.1, A2.7.3.3 and A2.7.4, Requirements served (REQ-S9-004) and Screens; TSD S9 Partner management v2 T2, T3.0, T3.1, T3.2, T3.3, T5.1, T5.2, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-33 and R-WO-37 |
| Test cases | TC-E6-035-01 to TC-E6-035-04 |
| Feature and screens | FEAT-PRM-07, SCR-35 Placement and allocation, SCR-34 Partner list |
| Rules | VR-S9-007-1, BR-S9-007 and R-WO-37 read as the rows of the feature; no row expresses the fee basis (ASM-5405, ASM-5406) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the two reads, the `Partner`, `PartnerInstruction` and `InstructionPage` elements, the fee properties, the consumed rows, the rights, the error set and the fakes: RWB-S9-E6035-CON.
- The panel, the fee schedule, the service levels and the LOVs as versioned reference data: the reference-data stories of the module (FEAT-PRM-02, E8 panel publication).
- The allocation by measured return, the override with a reason, the result submission and the placement: the other E6 stories of the module.
- The partner's fee claim and its approval, on `POST /partner/instructions/{instructionId}/invoices`: FEAT-PRM-09 in E7 (ASM-5413).
- The posting of the recovery as post charge-off income and the move to `PAYMENT_MATCHED`: rwb-writeoff's D9 route and rwb-payment.
- Every state of the instruction and of the write-off route: this step writes `fee_amount` and nothing else (§9).
- The payment of record and its ALS and GL leg: rwb-payment (P8). The case of record and its route states: rwb-case (P3). The package and its rule rows: rwb-decision (P7).
- The gateway-bff composite route and the screen field lists of SCR-35 and SCR-34: RWB-PLT-N001-CON and the edge stories.
- An event that carries the fee to another service: none is published and the fee rests on the instruction row and the ledger (ASM-5409).
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
