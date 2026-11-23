# RWB-S9-E7012-APP Approve partner fees

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S9-N |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E7012-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the fee-approval slice of RWB-E7-012 is realigned onto rwb-partner (S9, service wave 4, business wave 4). The one legacy criterion this story owns is kept word for word with its origin tag; the legacy main-flow criterion belongs to RWB-ITG-E7012-ITG, and the component-level criteria added here are tagged new. The step is the `feeApproval` branch of `InstructionWorkflow` on task queue `rwb-partner`: it reads the instruction and its `fee_amount`, `result_code` and `status` from this service's own schema, reads the fee schedule at its version from the reference data of rwb-case (DP-07, class C, placeholder) and the claim's papers from rwb-document (class C, placeholder), decides against the schedule and the result, and records one approval entry through the local decision-record library before anything else (DP-03). It declares no operation of its own, because the six operations of the service are the panel, instruction, result and invoice stories'; the act and the read reach the screen through the gateway-bff composite route (DP-19) on base `/api/recovery/partner/v1` (DP-13). No column or list value of `partner_instruction` carries an approved fee, no rule row of the Business Rules and Routing Logic v4 names a partner fee, the fee schedule has no entity and no reference-table code, and the Finance and CFO delegate of FSD S9 A2.9.3.3 is absent from TSD S9 T6.1 (GAP-3123; ASM-5427 to ASM-5426). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager (RW-AGENCYMG)** — and as the finance delegate that reads the same claim where the matrix gives it a read — I want **the Workbench to check a partner's fee claim against the contracted schedule and the recorded result and to approve it**, so that **a fee is paid only where the schedule and the result both support it, and the approval is on the decision record with the schedule version and the rule version it was judged under**.

This story owns:

- the one legacy criterion of RWB-E7-012 that this slice owns (AC2), copied verbatim with its origin tag, and the refusal it describes;
- the `feeApproval` branch of `InstructionWorkflow` on task queue `rwb-partner` in namespace `rwb-recovery`, as the step that holds the approval of a completed instruction (context pack ownership row `InstructionWorkflow`);
- the read of the instruction and its `fee_amount`, `result_code` and `status` on this service's own schema, and the read of the fee schedule at its version on the reference-data contract of rwb-case (ASM-5429);
- the comparison of the claim with the amount the schedule allows and with the result the partner reported, and the refusal where the two disagree;
- the approval entry: one record per instruction, written through the local decision-record library **before** anything else, carrying the claim, the amount the schedule allows, the schedule version, the result code, the rule ID with its version and the approver (DP-03);
- the idempotency of the act: one entry per instruction, and a repeat answers the entry that exists;
- the read-only claim slice of SCR-34 and SCR-35 behind the gateway-bff composite route (DP-19), on the service base `/api/recovery/partner/v1` (DP-13).

It does not own: the published shapes, the entry element, the consumed rows, the rights, the error set and the fakes (RWB-S9-E7012-CON); the end-to-end journey across the four services (RWB-ITG-E7012-ITG); the panel, the instructions, their acceptance, the results and the invoices and their six operations (the Epics 2, 4 and 6 stories of this service); the fee schedule as versioned reference data (FEAT-PRM-02); the calculation of the fee due (FEAT-PRM-07); the money side and the fee tables (FEAT-PAY-05, rwb-payment P8); the documents (rwb-document P5); the rules and the central ledger (rwb-decision P7); the rights and the lists of values (rwb-access P4); and the schema, migration and deployment of this service (the DB, INF and OPS stories of this key).

### 2. Business rationale

The objective, the problem and the metric are the module's and do not move: partners are instructed and paid by email and spreadsheet, allocation is not based on performance, and the metric is the share of placements made by scorecard, targeted at 100 percent, measured on the decision log and the Workbench records and reviewed monthly (FSD S9 A2.9.1). The requirement is REQ-S9-004, "Fees are calculated from the contracted schedule and paid against recorded results", with REQ-S9-001 for the contract and fee point of the six every partner type is managed on (Program BRD v4; FSD S9 Requirements served). FEAT-PRM-09 is the approval of a claim, one epic after FEAT-PRM-07 calculated the fee due.

A schedule is only worth having as data if the payment that follows is checked against it. What D-RCV-60 changes is who owns each fact of that check:

- **The instruction, its fee and its result are this service's own.** `partner_instruction` carries `fee_amount` (DF-PRT-016, "Fee payable, baht"), `result_code` (DF-PRT-015) and `status` (DF-PRT-014) in `rwb_partner` (TSD S9 T3.1), so this service is the only one that can compare a claim with what it instructed and what the partner reported.
- **The schedule is reference data of another owner.** FEAT-PRM-02 keeps the panel, the fee schedule and the service levels as versioned reference data, and the R3 default ruling gives reference data to rwb-case (DP-07); no fee-schedule entity exists in the LDM and no code for it exists in `LOV-REF-TABLE`, so the read and its version carry a placeholder (ASM-5429).
- **The approval is a decision, so it is recorded.** Legacy AC1 asks for the result in the decision log with the rule version and legacy AC2, which this story owns, stops the action when the log cannot be written; R-UNI-39 says the same ("Block the action and raise an incident. No action proceeds unlogged"). The entry is written through the local library in one transaction, before anything else (DP-03).
- **No column carries the approval.** TSD S9 T3.1 gives `partner_instruction` nine fields and `LOV-INSTR-STATUS` six values, none of which is an approval, an approver or an approved instant; the approval therefore lives on its entry and the element stays as published (ASM-5427).
- **The amount is never a constant.** The rate, the basis and the version come from the schedule at its version; FSD S9 BR-S9-009 forbids any value a business person may change from being written in code (ASM-5430).

No business value moves: the instruction types, the status values, the schedule rate and basis and the fee amount stay reference data or rule rows read with their version.

The wave and the date are the plan's: this key is EP07, wave 4, release 31 May 2027, and rwb-partner is created in wave 4, so the business wave and the service wave are the same and no W-MAP conflict arises; the date is copied unchanged and marked tentative (ASM-5426).

### 3. Preconditions

- RWB-S9-E7012-CON is published and tagged: the `partner_instruction` element, the two consumed rows, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-34 and SCR-35 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `partner` and `partner_instruction` exist in `rwb_partner` from the DB story of this service with the columns of DF-PRT-001 to DF-PRT-016 and the standard record columns of TSD S9 T3.0; at least one instruction of the case is at `DONE` with a `result_code` and a `fee_amount` (TSD S9 T3.1).
- The fee schedule is published with its version and a fake: the rate and the basis the claim is judged on. Its entity, its version token and its operation name are Not specified in the source documents (GAP-3123; ASM-5429).
- The time-limited upload link of rwb-document is published with its fake, class C, one hop and 2 s (TSD S9 T5.2.2; ASM-5429).
- The lists this step reads — `LOV-INSTRUCTION`, `LOV-INSTR-STATUS`, `LOV-PARTNER-TYPE` and `LOV-PANEL` — are reference data with their version, read on the owner's contract and never written in code (TSD S9 T3.2; ASM-5430).
- The service runs as its own login on `rwb_partner` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, on `rwb_document` or on a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-05).
- No rule package carries a partner-fee row: the step therefore evaluates the comparison the schedule defines and records the rule ID as a placeholder, and invents no rule ID (ASM-5428).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E7012-CON when its tests pass.

### 4. Flow

1. A partner submits a fee claim against a completed instruction through PRT-04 Invoice and API-S9-006, which the invoice story of Epic 6 owns; the claim names the instruction and its papers (FSD S9 Screens; TSD S9 T-A.2).
2. The partner and agency manager opens the claim on SCR-35 through the gateway-bff composite route, which merges the partner, the instruction, its `fee_amount`, its `result_code`, the schedule and the upload link (DP-19; ASM-5431).
3. The manager starts the approval; the request names the instruction and carries the `Idempotency-Key`. No screen calls this service directly (DP-19).
4. The `feeApproval` branch starts: `readFeeClaim` reads the instruction and its `fee_amount`, `result_code` and `status` from `rwb_partner`, the fee schedule at its version from rwb-case, and the upload link from rwb-document (ASM-5429).
5. The branch refuses the claim where the instruction is not at `DONE`, carries no `result_code`, or carries no `fee_amount`: there is nothing to approve (ASM-5427).
6. `evaluateFeeClaim` compares the claimed amount with the amount the schedule allows for that instruction type and with the result the partner reported. Where the two agree the decision is approve; where they disagree the decision is refuse and the difference is named. No rule row of the Business Rules and Routing Logic v4 names the condition, so the record carries the rule ID as a placeholder and the schedule version it used (ASM-5428).
7. The step reads the insolvency guard: where the partner has entered insolvency, R-UNI-28 stops fee payments and the claim is refused with that reason, not approved (ASM-5428).
8. `recordFeeApproval` writes one approval entry through the local library **before any other effect**: the case, the instruction, the partner, the instruction type, the claimed amount, the amount the schedule allows, the schedule version, the result code, the rule ID with its version and the approver. A failed write stops the step with nothing changed and MSG-P7-003 (DP-03; legacy AC2).
9. The instruction row is not touched: no column of `partner_instruction` carries the approval and `status` stays at `DONE`, because `LOV-INSTR-STATUS` has no approval value and adding one is a DB story (ASM-5427).
10. The branch answers the request with the decision, the amount and the schedule version; the screen shows the decision, the amount, the schedule version and the entry reference, read only.
11. A repeated request for the same instruction with the same key answers the entry it already wrote, and writes and decides nothing again.
12. The finance delegate reads the same claim and the same decision on SCR-35 through a role the matrix gives R, and the conflict between FSD S9 A2.9.3.3 and TSD S9 T6.1 is recorded rather than resolved here (ASM-5431).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no approval, no decision, no entry, and the instruction row is untouched | MSG-P7-003 | AC2, TC-E7-012-02, TC-E7-012-04 |
| X2 | The role does not hold the Partner portal right of the approval | 403 before any read of the schedule and before any record; the branch runs under the service identity with the same check | MSG-P4-002 | AC4, TC-E7-012-03 |
| X3 | A required value is absent or invalid: no instruction reference, no schedule version, no result code or no amount | The branch refuses the claim, writes nothing and names the field | MSG-GEN-001 (VR-S9-009-1) | AC1, AC5 |
| X4 | The schedule or the upload link does not answer inside 2 s, or its breaker is open | No approval and no refusal is written, the branch retries on the workflow's own schedule and the caller sees the platform 503 envelope | None (platform envelope) | AC1 |
| X5 | The claimed amount and the amount the schedule allows disagree, or the result does not support the claim | The claim is refused, the difference is named and nothing is approved | None | AC1 |
| X6 | The instruction is not at `DONE`, or carries no `result_code`, or carries no `fee_amount` | No claim to approve: the branch ends and records the reason | None | AC1 |
| X7 | The partner has entered insolvency | R-UNI-28 stops fee payments, the claim is refused with that reason and nothing is approved | None | AC1 |
| X8 | The schedule has no version in force | The branch waits, no decision is taken and the claim stays open; no amount is judged against an unversioned schedule | None | AC5 |
| X9 | The same instruction is approved twice, or the request is repeated with the same key | One entry per instruction; the repeat answers the entry that exists and counts the repeat | None | AC3 |
| X10 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row, a `rwb_document` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR6 |

X1 and X2 are the legacy not-recorded and access paths of this key carried onto the slice; X3 to X9 are the paths the schedule read, the claim, the guard and the target call types add; X10 is the schema and ACE boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E7012-CON, the decision-record stub, the reference-data fake, the upload-link fake and the gateway-bff fake, on its own schema, and needs no live P1, P3, P5 or P7 |
| Negotiable | The branch and activity names, the reason codes of a refusal and the shape of the entry are this story's choice; the element, the lists, the messages, the screens and the right are fixed |
| Valuable | A fee claim is checked against the contracted schedule and the recorded result, decided once, and recorded with the schedule version it was judged under |
| Estimable | One workflow branch, three activities, two clients, one record write, one idempotency row and one read-only screen slice |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on a synthetic case through the contract fakes, plus the mismatch, the not-done, the insolvent, the refused-right, the repeat and the forced record-write failure |

### 7. Acceptance criteria

```gherkin
Feature: Approve partner fees

  Background:
    Given the partner_instruction element and the consumed rows are the published baseline of RWB-S9-E7012-CON at its version
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The claim is checked against the schedule and the result before it is approved (new, D-RCV-60)
    Given the rwb-partner contract mock returns instruction "INS-2026-000712" on case "RW-2026-000712" at status "DONE" with a result_code and a fee_amount equal to the amount the schedule allows
    Given the rwb-case contract mock returns the fee schedule at its version in force with the rate and the basis the instruction is judged on
    When the partner and agency manager approves the claim
    Then the claim is compared with the amount the schedule allows for that instruction type and with the result_code recorded on the instruction
    Then the approval is refused where the two disagree, and the difference is named
    Then the approval carries the schedule version and the result it was judged against

  Scenario: AC2 Not recorded (legacy RWB-E7-012 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 One approval per instruction and the instruction row is unchanged (new, D-RCV-60)
    Given the instruction "INS-2026-000712" was approved and its entry exists
    When the same instruction is approved again, or the request is repeated with the same Idempotency-Key
    Then one approval entry exists for the instruction
    Then the repeat answers the entry it already wrote and writes nothing again
    Then no property of partner_instruction is written by the approval: fee_amount, result_code and status stay as the flow left them

  Scenario: AC4 A role without the Partner portal right of the approval is refused (new, D-RCV-60)
    Given a user whose role does not hold Partner portal right U
    When that user approves the claim
    Then the act is refused with MSG-P4-002 before any schedule read and before any record
    Then the entry is not written and the claim is unchanged

  Scenario: AC5 The rate, the basis, the lists and the rule version are read data (new, D-RCV-60)
    Given the fee schedule and the lists are read at their version
    When the claim is decided
    Then the rate and the basis come from the schedule version in force and never from a constant
    Then the rule ID the entry carries is a versioned row, and a schedule with no version in force leaves the claim open with no decision
    Then no fee amount, no rate and no status value is a schema default or a constant of the code
```

The one legacy criterion, AC2, is the legacy criterion of RWB-E7-012 word for word, with its origin tag added and nothing else changed: the wording of `the decision log cannot be written`, `the action is taken` and `the user sees MSG-P7-003` all stand, and AC2 has no cross-service part, so no `Given the <service> contract mock returns <x>` line is added to it. AC1 of the legacy story is owned word for word by RWB-ITG-E7012-ITG and is not copied here. AC1 and AC3 to AC5 are new component-level criteria for this story's own deliverable, tagged `(new, D-RCV-60)`, and restate no business outcome the integration story owns. On this story "the action" is the approval of a fee claim, and "the screen" is the claim slice of SCR-35 behind the composite route. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_partner`, with the `decision_log_entry` ledger of rwb-decision behind it. The instruction number and the case number in the mock lines are synthetic test data and no source value (section 16).

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-UNI-28 | Universal rules | All | ANY_ACTIVE | PARTNER_INSOLVENT | the partner enters insolvency | Recall the work, secure the documents and any cash held, stop fee payments | PARTNER_RECALLED | Head of the partner type | Partner Portal, Workbench | same day |
| R-UNI-39 | Universal rules | All | ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision log entry cannot be written | Block the action and raise an incident. No action proceeds unlogged | EXCEPTION_QUEUE | Platform team | Workbench | immediate |
| R-WO-37 | Write-off | D9 | PLACED_WITH_AGENCY | PAYMENT_RECEIVED_AFTER_CHARGEOFF | the payment matches the case and the placement | Post the recovery as post charge-off income and calculate the agency fee | PAYMENT_MATCHED | Workbench | ALS core and GL, Agent Runtime | next working day |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. This story reads R-UNI-28 as the guard that stops fee payments when a partner is insolvent, evaluates R-UNI-39 as the record-first rule, and reads R-WO-37 as the rule of the post charge-off recovery whose fee the claim is against. Their owner column names a business role and a system, not a service: "Workbench" is this service and its stage, and "ALS core and GL" is outside Recovery. No row of the table names the fee-approval condition itself, which is the gap of ASM-5428.

| ID | Rule | Source |
|---|---|---|
| BR1 | The approval is a decision first: one entry per instruction is written through the local library, with the claim, the amount the schedule allows, the schedule version, the result code, the rule ID and the version, and a failed write changes nothing and answers MSG-P7-003 | DP-03; TSD S9 T2; R-UNI-39; legacy AC2 |
| BR2 | The instruction, its fee and its result are this service's: `fee_amount` (DF-PRT-016), `result_code` (DF-PRT-015) and `status` (DF-PRT-014) of `partner_instruction` decide the claim, and nothing else is read for it | Context pack ownership row `partner_instruction`; TSD S9 T3.1; DP-01 |
| BR3 | The schedule and the lists are not this service's: they arrive on the reference-data contract of rwb-case at a version, and no property of them is declared here | R3 default ruling; DP-07; TSD S9 T0.3; ASM-5429 |
| BR4 | A claim is approved only where the claimed amount equals the amount the schedule allows and the recorded result supports it; otherwise it is refused and the difference is named | FSD S9 A2.9.2 and A2.9.3.1; REQ-S9-004; ASM-5428 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_partner`; `case_id` and `partner_id` are identifiers of other services' facts and the document reference is an identifier of rwb-document's | DP-01; TSD S9 T3.3 |
| BR6 | ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and no customer datum reaches it | DP-05, DP-11; TSD S9 T0.4 |
| BR7 | Every value a business person may change is reference data or a rule row read with its version: the rate, the basis, the lists and the rule version | FSD S9 BR-S9-009; TSD S9 T3.2; legacy Guardrails |
| BR8 | The approval is idempotent per instruction and per key: one entry, one decision, and a repeat answers the entry that exists | TSD S9 T-A.2 (`Idempotency-Key`); DP-03 |
| BR9 | The approval writes no column of `partner_instruction`: `status`, `result_code` and `fee_amount` stay as the instruction flow left them, because no property and no list value carries an approval | TSD S9 T3.1, T3.2; ASM-5427 |
| BR10 | A partner in insolvency is not paid: R-UNI-28 stops fee payments and the claim is refused with that reason | R-UNI-28; ASM-5428 |
| BR11 | No person name, personal contact value or identity number enters `rwb_partner`, the entry, a log, a workflow input or an event; a partner's registered name is a firm name | Template and Rules §R7.2 (s17); LDM v8 (masking) |

### 9. State transitions

The instruction's own machine and the case route state are not moved by this story: the claim is decided on an instruction that its own flow has already completed, and the approval is carried on its entry (BR9, ASM-5427). What this story owns is the approval step and its record.

| From (`partner_instruction.status`, read) | The approval act | Condition | What this story writes |
|---|---|---|---|
| `DONE` | A claim is submitted and approved | The claim equals the amount the schedule allows and the result supports it | One approval entry, its schedule version and its rule ID; the instruction row is unchanged |
| `DONE` | A claim is submitted and refused | The claim and the schedule disagree, or the partner is insolvent | One refusal entry with its reason; the instruction row is unchanged |
| `IN_PROGRESS` or `ACCEPTED` | A claim is submitted | The result is not final | Nothing; the branch ends and records that there is nothing to approve |
| `RECALLED` or `DECLINED` | A claim is submitted | The instruction is no longer with the partner | Nothing; the branch ends |
| Any | The same instruction is approved twice | The entry exists | Nothing written; the existing entry is answered |

| Approval step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A claim is started for an instruction | The instruction reference and the key are read | Reading |
| Reading | The instruction, the schedule and the upload link are read | The instruction is at `DONE` with a result and an amount | Evaluating |
| Reading | The instruction is not done, or has no result or amount | X6 | Closed, nothing written |
| Evaluating | The claim matches the schedule and the result | The partner is not insolvent | Recording |
| Evaluating | The claim differs, or the partner is insolvent | X5, X7 | Recording a refusal |
| Recording | The entry is written | The transaction commits | Decided |
| Recording | The entry write fails | X1 | Waiting, nothing changed, MSG-P7-003 |
| Decided | The same instruction or key arrives again | X9 | The existing entry is answered |

The approval states are the entry's own and no value of `LOV-INSTR-STATUS` or of the case is added by this story (ASM-5427).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Partner and agency manager (RW-AGENCYMG) | The primary actor of FSD S9 A2.9.3.3: holds the claim and the approval. TSD S9 T6.1 gives this role CRUDA on Partner portal, so it holds the U the act needs |
| Finance and CFO delegate (named by FSD S9 A2.9.3.3, absent from TSD S9 T6.1) | The "also uses" role of the feature: reads the claim and the decision through a role that holds R; the conflict is recorded and no right is invented (GAP-3123; ASM-5431) |
| Head of the partner type (R-UNI-28, owner column) | Receives the recall when a partner is insolvent; no case right is used for it |
| Litigation officer, enforcement owner, sale officer, NPA and asset manager, debt sale officer, guarantee officer (RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT) | Partner portal CRU: hold the instructions whose fee a claim is against |
| Partner and agency user roles (PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC) | Partner portal RU: submit the claim on PRT-04 Invoice and read their own instructions; they never approve |
| Platform team (R-UNI-39, owner column) | Receives the incident when the record cannot be written; no case right is used for it |
| rwb-case (P3) | Owns the case and the reference data, the fee schedule and the lists, at their versions |
| rwb-document (P5) | Owns the claim's papers and the time-limited upload link |
| rwb-decision (P7) | Owns the rule packages and the central ledger; this story records locally and evaluates the rows it reads |
| rwb-payment (P8) | Owns the fee tables and the money side of an approved fee (FEAT-PAY-05) |

No delegated authority limit applies to this step: it approves a fee against a schedule and a result and takes no credit decision, and the instruction's own delegation, if any, was applied where the instruction was issued.

### 11. Data

| BR Field ID | Entity | Owner | Use in this story |
|---|---|---|---|
| DF-PRT-008 to DF-PRT-016 | `partner_instruction` | S9, `rwb_partner` | **Read** only: `id`, `case_id`, `partner_id`, `instruction_type`, `instructed_at`, `due_at`, `status`, `result_code`, `fee_amount`. No column of it carries the approval, so this story writes none of them (ASM-5427) |
| DF-PRT-001 to DF-PRT-007 | `partner` | S9, `rwb_partner` | **Read** only: the firm, its code, its name, its type, its panel status, its contract end and its score |
| None: library table | `decision_record` | Platform library in `rwb_partner` | **Write**: one hash-linked approval entry per instruction, before anything else (DP-03) |
| None: library table | `idempotency_key`, `outbox_event` | Platform library in `rwb_partner` | The instruction key and the decision it holds; the outbox object exists as a library row and this step writes no event row to it (§12.3) |
| Not specified in the source documents | the fee schedule | P3 rwb-case, reference data | Read at its version: the rate and the basis the claim is checked against; the entity, the version token and the operation name carry the placeholder (GAP-3123; ASM-5429) |
| DF-DOC-001 and the upload link | `document` | P5 rwb-document | Not read as a table: the document reference and the expiry arrive on the owner's contract (ASM-5429) |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | P3 rwb-case | Not read and not written: the case reference is a cross-reference and the case is untouched (BR5) |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | Not written: the local entry is copied to the central ledger by its owner, and its identifier is not stored here |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | Not read as a table: the rule version arrives from the package in force, and no row names a partner-fee condition (ASM-5428) |
| `LOV-INSTRUCTION`, `LOV-INSTR-STATUS`, `LOV-PARTNER-TYPE`, `LOV-PANEL` | reference data and lists of values | P3 rwb-case (default ruling) | Read at their version; `LOV-INSTR-STATUS` carries the six values of TSD S9 T3.2 and no approval value exists (ASM-5430) |

No new table, no new column and no migration: the tables arrive with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_partner` by the library's own migration (DP-03).

**No personal data.** The entry carries identifiers, a code, an amount, an instant, a rule version and a state. No person name, contact value or identity number enters `rwb_partner`, the entry, a log or a workflow input; a partner's registered name is a firm name and only the firm identifier reaches the entry (BR11).

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). The six operations of the service belong to other stories of the same service: `GET /partners` (API-S9-001) and `POST /cases/{caseId}/instructions` (API-S9-002) to the panel and instruction stories, `GET /partner/instructions` (API-S9-003) and `POST /partner/instructions/{instructionId}/accept` (API-S9-004) to the instruction story, `POST /partner/instructions/{instructionId}/results` (API-S9-005) to the result story and `POST /partner/instructions/{instructionId}/invoices` (API-S9-006) to the invoice story. The approval act has no published operation, so this story builds the handler behind the placeholder that RWB-S9-E7012-CON declares, and the read of a decided claim behind the composite route is a placeholder too (GAP-3123; ASM-5431). A build that declares an approval operation here fails the absence test of RWB-S9-E7012-CON.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The fee schedule and the lists at their version; operation name Not specified in the source documents (GAP-3123; ASM-5429) | `/api/recovery/case/v1` | P3 rwb-case | The rate, the basis and the version the claimed amount is checked against, and the four lists of TSD S9 T3.2; read only, faked |
| The time-limited upload link of the claim's papers; operation name Not specified in the source documents (GAP-3123; ASM-5429) | `/api/recovery/document/v1` | P5 rwb-document | The document reference and the expiry the claim is shown against; read only, faked |

Each row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020, DP-11). Both are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3123; ASM-5429).

#### 12.3 Events published

None. The service publishes on `rwb.partner.events.v1` and its event set is `InstructionIssued` (`rwb.partner.InstructionIssued.v1`, EV-20) and `PartnerResultSubmitted` (`rwb.partner.PartnerResultSubmitted.v1`, EV-21), both of which belong to the issue of an instruction and the submission of a result and therefore to the Epics 2, 4 and 6 stories (Event and Messaging Design v4; TSD S9 T5.3). An approval issues nothing and submits nothing, so this story declares no producer group, no envelope and no outbox row, and RWB-S9-E7012-CON fails a build that adds one (ASM-5431).

#### 12.4 Events consumed

None. TSD S9 T5.2.2 records no event consumed by this service; the claim arrives as a request on the approval act and the instruction is read on this schema. TSD S9 T4 states that the module acts on events from P3, which contradicts the contract table, so the disagreement is recorded as a gap and this story declares no consumer group, no subscription and no inbox of its own (GAP-3123; ASM-5431).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction, started when an instruction is issued, parent close policy ABANDON, continues-as-new | `rwb-partner` in namespace `rwb-recovery` | Hosts the `feeApproval` branch and the SLA timers; its input is the instruction reference, and its outcome is the decision |
| `feeApproval` | Workflow branch | `rwb-partner` | The path from the claim to the entry and the decision |
| `readFeeClaim` | Activity | `rwb-partner` | The instruction, the schedule at its version and the upload link in; the claim and the amount the schedule allows out |
| `evaluateFeeClaim` | Activity | `rwb-partner` | The comparison, the insolvency guard, the rule ID with its version and the decision out |
| `recordFeeApproval` | Activity | `rwb-partner` | The entry and the decision out, one transaction, with the idempotency key |
| `issueInstruction`, `recordResult` | Activities, provided to S4 and S5 | `rwb-partner` | The two activities of TSD S9 T5.2.1; named here and unchanged by this story |

The decision carries the instruction reference, the amount, the schedule version, the rule ID with its version and the approver. The branch and activity names are a target design choice fixed by no source document, and this story creates no child workflow.

#### 12.6 Schedules

None. The Ownership Map gives S9 no job (context pack ownership rows, Jobs: 0) and FSD S9 A2.9.4.4 declares no background event for the feature. The instruction service levels are durable timers inside `InstructionWorkflow`, not a Schedule, not a Quartz row and not a shared job table; DP-10 is not in this key's pattern set (ASM-5431).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `partner_instruction` | S9, `rwb_partner` | The instruction, its type, its due date, its status, its result code and its `fee_amount`; this story reads it and writes no column of it |
| `partner` | S9, `rwb_partner` | The firm, its panel status and its contract end; read only, and the insolvency guard reads the partner's status |
| `decision_record` | Platform library in `rwb_partner` | The local hash-linked approval entry (DP-03) |
| `idempotency_key` | Platform library in `rwb_partner` | The key of the repeated approval and the decision it holds |
| `outbox_event` | Platform library in `rwb_partner` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and the reference data (P3), `document` (P5), `rule_row` and `decision_log_entry` (P7), `proceeds` (P8), `partner_user`'s bindings as another story's and every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner instruction fake | The instruction `INS-2026-000712` of case `RW-2026-000712` at `DONE` with a `result_code` and a `fee_amount` equal to the amount the schedule allows; the same instruction with a smaller and a larger claim; an instruction at `IN_PROGRESS`; an instruction at `RECALLED`; an insolvent partner | AC1, AC3, X5, X6, X7 |
| rwb-case reference-data fake | The fee schedule at its version in force, a schedule with no version in force, and `LOV-INSTRUCTION`, `LOV-INSTR-STATUS`, `LOV-PARTNER-TYPE` and `LOV-PANEL`; the entity, the version token and the operation name carry the placeholder (GAP-3123; ASM-5429) | AC1, AC5, X8 |
| rwb-document upload-link fake | A time-limited upload link for a document reference, an expired link and no answer inside 2 s; the operation name carries the placeholder (GAP-3123; ASM-5429) | AC1, X4 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answer for the case, with the claim slice of this service read once | AC1, AC4 |

The fakes are test-only and are replaced by the real services in SIT. No package fake is declared, because no rule package carries a partner-fee row (GAP-3123; ASM-5428).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | The fee schedule of rwb-case and the upload link of rwb-document; one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 belong to the instruction and result stories; the decision record rides the library's shared `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch and 3 activities | `InstructionWorkflow` and its `feeApproval` branch on `rwb-partner`, with `readFeeClaim`, `evaluateFeeClaim` and `recordFeeApproval`; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here; the claim's papers are a document reference, not a file |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `fee`; front end `src/modules/recovery/partner/PartnerFeeClaim.tsx`, the SCR-35 claim fragment this story answers, read only.

**Pattern application** (§R5.5)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the entry commits before the decision is returned, and a failed write leaves nothing behind. DP-13 fixes the base of the service and gives the approval no element of its own, because its six operations belong to other stories. DP-19 is how the claim slice of SCR-35 reaches this service, one hop through the gateway. Two patterns the plan does not carry are real dependencies here and are recorded rather than added: DP-07, the reference data of rwb-case read at a version (ASM-5429), and DP-08, the authorise contract of rwb-access behind the guard (ASM-5431). DP-09 is absent and rightly so, because this step publishes nothing (ASM-5431).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `InstructionWorkflow` fee branch | Workflow | Receives the claim, hosts the step, applies the idempotency key and returns the decision |
| `readFeeClaim` | Activity | Reads the instruction, the schedule at its version and the upload link, and refuses a claim with nothing to approve |
| `evaluateFeeClaim` | Activity | Compares the claim with the schedule and the result, applies the insolvency guard and returns the rule version and the decision |
| `recordFeeApproval` | Activity | Writes the entry and its idempotency row in one transaction and returns the decision |
| `ApprovalEntryWriter` | Library adapter | Writes the hash-linked entry before any other effect and refuses the step when the write fails |
| `ReferenceDataClient` | Client | The fee schedule and the lists of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `DocumentLinkClient` | Client | The time-limited upload link of rwb-document, one hop, 2 s, breaker |
| `InstructionReader` | Repository | The instruction, its fee, its result and its status, read on this schema |
| `PartnerFeeClaim` | React component | Shows the claim, the amount the schedule allows, the result, the decision and the schedule version on SCR-35, read only |

**Database and migrations.** No Flyway file. `partner` and `partner_instruction` arrive with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_partner` by the library's migration (DP-03). No column is added for the approval, its approver or its instant, because no column of `partner_instruction` carries them and the schedule stays with its owner (ASM-5427).

**Configuration and reference data.**

- The rate, the basis and the version of the fee schedule: reference data of rwb-case, read on its contract at its version (ASM-5429).
- `LOV-INSTRUCTION`, `LOV-INSTR-STATUS`, `LOV-PARTNER-TYPE` and `LOV-PANEL`: reference data with their version, never a constant (ASM-5430).
- The capability area "Partner portal" and its rights: access rows of rwb-access, read through the guard (ASM-5431).
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. The `feeApproval` branch and its input record on `rwb-partner`, with the claim reference, the idempotency key and the decision.
2. `InstructionReader` and the nothing-to-approve paths of AC1, with the not-done, no-result and no-amount cases (X6).
3. `ReferenceDataClient` against its fake, with the 2 s budget, the breaker and the unversioned-schedule path (AC5, X4, X8).
4. `DocumentLinkClient` against its fake, with the expired-link path (AC1, X4).
5. `evaluateFeeClaim` with the comparison of AC1, the difference it names and the insolvency guard of R-UNI-28 (X5, X7).
6. `ApprovalEntryWriter` and `recordFeeApproval` against the stub, with the failed-write path and MSG-P7-003 (AC2, X1).
7. The repeat and the same-instruction paths, one entry per instruction (AC3, X9).
8. The read-only claim slice of `PartnerFeeClaim` on SCR-35 through the composite route fake (AC1, AC4).
9. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no `rwb_case` read and no `rwb_document` read (X10, BR5, BR6).

**Feature flag.** `rwb.partner.fee-approval-v1`, a flag of the platform library; off means the claim is read and shown but cannot be decided, and the instruction, result and invoice flows are unaffected.

**Done when.** The tests of section 16 pass, the branch decides a synthetic claim in SIT, the entry carries its schedule version and its rule version, a mismatched claim and an insolvent partner are refused, a claim with nothing to approve ends with no entry, a repeated request writes once, a forced entry failure changes nothing, no `rwb_case`, `rwb_document` or `v_ace_*` read exists in the build, and SCR-35 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the claim is absent or invalid, for example no instruction reference, no schedule version, no result code or no amount (X3, VR-S9-009-1) | Enter {field}. |
| MSG-P4-002 | A role without the Partner portal right of the approval takes the act (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The approval entry cannot be written before the decision (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are those of the legacy message set of this key; the text is the legacy and FSD S9 wording, copied unchanged, and no message is reworded and no new one is added. R-UNI-39's incident is raised by the platform on the same failure and is not a message of this service.

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-35 Placement and allocation | Loading; list; claim open; approved; refused; not recorded; unavailable | The claim slice: the partner, the instruction, its type, the claimed amount, the amount the schedule allows, the result, the decision, the schedule version and the entry reference, read only |
| SCR-34 Partner list | Loading; list | The panel row of the firm the claim belongs to, read only through the same route |
| PRT-04 Invoice | Form; submitted | No part: the partner's claim is submitted by the invoice story of Epic 6 through API-S9-006, and this story reads the claim it produces |

Both staff screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case and the schedule and rwb-document for the upload link; this story fixes only its own claim answer, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON (ASM-5431). The decided-claim read itself is a placeholder, because no source publishes an operation for it (GAP-3123). The approved, refused, not-recorded and unavailable states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-012-01 | AC1 | Component | The synthetic case `RW-2026-000712` and instruction `INS-2026-000712` at `DONE` with a result and a fee equal to the amount the schedule allows; the match is approved, and a smaller and a larger claim are refused with the difference named |
| TC-E7-012-02 | AC2 | Component | The decision-record stub stopped; no entry, no decision and MSG-P7-003 |
| TC-E7-012-03 | AC4 | Component | A role without Partner portal U; 403 with MSG-P4-002, no schedule read and no entry |
| TC-E7-012-04 | AC2, X1 | Component | A forced decision-record write failure stops the approval with MSG-P7-003 and leaves the instruction and the schedule untouched |
| TC-S9-E7012-APP-01 | AC1 | Component | The instruction at `IN_PROGRESS`, at `RECALLED`, with no result and with no amount; nothing is approved and the reason is recorded |
| TC-S9-E7012-APP-02 | AC3 | Component | The same instruction approved twice and the same key repeated; one entry, one decision and the repeat answered |
| TC-S9-E7012-APP-03 | AC5 | Component | The schedule at its version and a schedule with no version in force; the rate and the basis are read, and an unversioned schedule leaves the claim open |
| TC-S9-E7012-APP-04 | AC1, X7 | Component | A partner in insolvency; R-UNI-28 stops the payment, the claim is refused and nothing is approved |

The four `TC-E7-012-xx` ids are the legacy cases of RWB-E7-012 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`, and the legacy level `System` maps to `Component` because the artefact under test is the branch against its contract fakes. Their business outcome is proved end to end by RWB-ITG-E7012-ITG, which copies the legacy main-flow case with the `-ITG` suffix. The four `TC-S9-E7012-APP-xx` cases are new and cover the component criteria this story adds. No `-ITG` copy is written here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same id.

### 17. Guardrails

- No business value in code: the rate, the basis, the lists and the rule version stay reference data or rule rows read with their version.
- No personal data in `rwb_partner`, in an entry, a workflow input, a log or a prompt: identifiers, a code, an amount, an instant, a rule version and a state only, and a partner's registered name is a firm name.
- ACE data and the schedule only through the owner's contract: no `v_ace_*` view, no ACE table, no `rwb_case` row and no other service's schema (BR5, BR6).
- The case, its route state and its timers stay with rwb-case: this story writes no case row and no case state.
- The instruction row is read only: a build that writes `fee_amount`, `result_code` or `status` from the approval fails the review (BR9).
- One base, one topic, one queue and one login per service; this story adds no second topic, no event and no Schedule (DP-13, DP-14).
- The record is written before the decision and in its transaction; a failure leaves nothing behind (DP-03, R-UNI-39).
- A partner in insolvency is never paid here: R-UNI-28 is read before the decision, and a build that approves past it fails the review (BR10).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no `recovery_log` write and no data-lake path.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results (Must, E6) | The claim check against the schedule at its version and the recorded result, and the approval entry | TC-E7-012-01, TC-S9-E7012-APP-01 |
| REQ-S9-001 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit (Must, E6) | The fee-approval step of the panel and its record | TC-E7-012-01, TC-S9-E7012-APP-03 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the instruction and its fee | TC-E7-012-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-E7-012-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-S9-E7012-APP-03 |
| ADR-022 | Local decision record plus central ledger | The approval entry written before the decision | TC-E7-012-02, TC-E7-012-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-012, disposition Split (rework); feature FEAT-PRM-09 |
| Legacy criteria | AC2, owned word for word by this story; AC1 is owned by RWB-ITG-E7012-ITG and is not copied here |
| Source text | Legacy RWB-E7-012; FSD S9 Partner management v4 A2.9 and Requirements served; TSD S9 Partner management v3 T0 to T6.1 and T-A; Business Rules and Routing Logic v4 rows R-UNI-28, R-UNI-39 and R-WO-37; LDM and Data Dictionary v8 `partner`, `partner_instruction` and `LOV-INSTR-STATUS`; Event and Messaging Design v4 EV-20 and EV-21; Program BRD v4 REQ-S9-001 and REQ-S9-004 |
| Test cases | TC-E7-012-01 to TC-E7-012-04 and TC-S9-E7012-APP-01 to -04 |
| Feature and screens | FEAT-PRM-09, SCR-34 Partner list, SCR-35 Placement and allocation and PRT-04 Invoice |
| Rules | R-UNI-39 and R-UNI-28 evaluated; R-WO-37 read; no rule row names the fee-approval condition (ASM-5428) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the entry element, the consumed rows, the rights, the error set and the fakes: RWB-S9-E7012-CON.
- The end-to-end approval journey across rwb-partner, rwb-case, rwb-document and rwb-decision: RWB-ITG-E7012-ITG, which owns AC1 of the legacy story.
- The panel, the instructions, their acceptance, the results and the invoices and their six operations: the Epics 2, 4 and 6 stories of this service.
- The fee schedule and the panel as versioned reference data: FEAT-PRM-02 and rwb-case (P3).
- The calculation of the fee due and the matching of a recovery: FEAT-PRM-07, built in Epic 6.
- The fee tables, the payment of an approved fee and the general ledger: FEAT-PAY-05 and rwb-payment (P8).
- The claim's documents, their intake and their retention: rwb-document (P5).
- The rule packages, their rows and the central ledger: rwb-decision (P7), which carries no partner-fee row today (ASM-5428).
- The gateway-bff composite route and the screen field list of SCR-34 and SCR-35: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
