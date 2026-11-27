# RWB-S9-E7017-APP Manage extra costs and services on an asset

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S9-S |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E7017-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the extra-cost slice of RWB-E7-017 in rwb-partner. AC2 is kept word for word with its origin tag added. The additional partner cost on a held asset is recorded as the partner's result on `partner_instruction` (`result_code`, `fee_amount`) through API-S9-005 and its fee invoice through API-S9-006, checked against the fee schedule version and the recorded result, then approved or refused on `InstructionWorkflow` with the decision record written first. The held asset and its holding cost stay with rwb-asset (S5, FEAT-AST-07). No source gives the claim a field catalogue, a cost type list, an approval limit or a table of its own, names an operation that approves it, or gives the event pair an invoice event (GAP-3133; ASM-5483, ASM-5484, ASM-5488). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E7017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the extra costs and services a partner claims on a held asset to be recorded against its instruction and approved or refused with the decision record written first**, so that **partners are placed, paid and measured by rule, and a cost that cannot be recorded changes nothing**.

This story owns: the one legacy criterion the plan gives it, AC2; the recording of the claim and its evidence on `partner_instruction` through API-S9-005 and the fee invoice through API-S9-006; the check against the fee schedule version and the recorded result; the approval or refusal with the decision record written first (DP-03) and one EV-21 publication per recorded claim; and SCR-35 with the SCR-34 read, through the gateway-bff composite route (DP-19) on base `/api/recovery/partner/v1` (DP-13).

It does not own: the published shapes, rights, error set and fakes, which are RWB-S9-E7017-CON; AC1, the end-to-end proof, which is RWB-ITG-E7017-ITG's; the held asset, its holding cost, the work order and the provision step, which are rwb-asset's (S5, FEAT-AST-07); the panel and the fee schedule as reference data (FEAT-PRM-02); issuing, accepting and closing an instruction; the recall and notice rules R-UNI-25 to R-UNI-30; the case, which is rwb-case; the rights as code, which is rwb-access; and the deployment, which is the operations story of this key.

### 2. Business rationale

The objective, the problem and the metric are unchanged from the legacy story and the module FSD: partners were instructed and paid by email and spreadsheet, and the cost of holding an asset is one of the six points every partner type is managed on (FSD S9 A1.3, A2.14.1; REQ-S9-001, REQ-S9-004). The target records the claim on the instruction, approves it against the contracted schedule and the recorded result, and writes one decision record, measured on the decision log at the monthly target of A2.14.1. What D-RCV-60 changes is who owns the claim, the approval, the record and the asset facts.

- **The claim is a result on the instruction, not a new object.** The ownership rows give S9 three tables and `partner_instruction` carries `result_code`, `fee_amount` and `status` (DF-PRT-014 to DF-PRT-016); the evidence lands in rwb-document, so no cost table and no migration is added (GAP-3133; ASM-5483).
- **The fee is checked, not computed here.** REQ-S9-004 pays fees from the contracted schedule against a recorded result; the schedule is a versioned reference-data row of the panel and the result is the instruction's own row (ASM-5489).
- **The extra cost is a work order on a held asset.** Storage, property tax, insurance, security and eviction are raised as work to a vendor; its invoice is released when the work is accepted and blocked when it is refused (R-DIS-10, R-DIS-11, R-DIS-12). The stage that raises the work order is rwb-asset's and this story owns the partner side of it.
- **The record is a condition of the act.** R-UNI-39 blocks an action whose log entry cannot be written; AC2 is that rule at this claim.
- **The asset keeps its owner.** The legacy data section reads `v_ace_npa_asset` (DF-ACE-208 to DF-ACE-219); after the split the asset record and that view are rwb-asset's and rwb-source-data's, and this service holds no `v_ace_*` grant (DP-05; ASM-5486).
- **Two facts have no source.** No published operation approves a claim, and the event pair has no invoice or approval event (GAP-3133; ASM-5484, ASM-5488).

No business value moves: the cost type, the fee schedule, the approval limit, the instruction states and the right are reference data and rule values, read with their version and never written in code.

### 3. Preconditions

- RWB-S9-E7017-CON is published: the results and invoice writes on `/api/recovery/partner/v1`, the claim and invoice elements, the rights, the error set and the fakes.
- `partner_instruction` exists in `rwb_partner` from the DB story of this service with DF-PRT-008 to DF-PRT-016 and the standard columns of TSD S9 T3.0; `partner` carries DF-PRT-001 to DF-PRT-007.
- RWB-PLT-E1027-CON is published: the decision-record library creates `decision_record` and `outbox_event` in `rwb_partner` and publishes on `rwb.decision-record.v1` (DP-03).
- RWB-PLT-N001-CON is published: SCR-34 and SCR-35 reach this service through the composite route (DP-19), and a partner outside the bank arrives on the partner gateway of FAPI 2.0 (INT-24).
- A partner holds a live instruction of a type from LOV-INSTRUCTION against a held asset, and the asset reference on it is an identifier of rwb-asset's record.
- The fee schedule version in force is a reference-data row of the panel (ASM-5489).
- The service runs as its own login on `rwb_partner`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant.
- No approval is needed to build against a Draft contract baseline.

### 4. Flow

1. The partner reads its own firm's work through `GET /partner/instructions` and picks the instruction the extra cost belongs to (DF-PRT-011 to DF-PRT-014).
2. It records the cost claim with its evidence through `POST /partner/instructions/{instructionId}/results` (API-S9-005, right U, `Idempotency-Key`): result code, the service performed, the amount claimed and the files.
3. The service validates the claim and answers 422 with MSG-GEN-001 on a missing field, 415 on a disallowed file type, 409 on a repeat (X3, X5, X6).
4. `CostDecisionRecordWriter` writes one local record before any row moves: the instruction, the firm, the case reference, the amount, the schedule version, the rule version in force and the trigger (DP-03; R-UNI-39). A failed write leaves the row as it was and answers MSG-P7-003 (AC2, X1).
5. `recordCostClaim` writes in one transaction: `result_code`, `fee_amount`, and `status` from `SENT` or `ACCEPTED` to `IN_PROGRESS`; no other column moves and no row is deleted.
6. The outbox publishes EV-21 `PartnerResultSubmitted` with `caseId`, `instructionId`, `resultCode` and `resultedAt`, once per recorded claim (DP-09).
7. The partner submits the fee invoice through `POST /partner/instructions/{instructionId}/invoices` (API-S9-006, right C): `InvoiceRequest` in, `Invoice` out, the same record-first rule.
8. The manager opens SCR-35, sees the claim against the instruction with its amount, its evidence and the schedule version in force, and checks it against the schedule and the recorded result (REQ-S9-004).
9. On approval the `costApproval` signal reaches `InstructionWorkflow`: the approval is recorded, `approveCostInvoice` releases the invoice for payment against `fee_amount`, and `status` moves to `DONE`. On refusal the claim is recorded as refused, the invoice stays blocked and the status stays `IN_PROGRESS`, with the coded reason from reference data (R-DIS-11, R-DIS-12; §9).
10. The asset, its holding cost and the work order are shown on SCR-35 through rwb-asset's own fragment; this service writes no asset row and announces nothing about the asset (ASM-5486).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision record cannot be written before the claim or the approval | Nothing changes: no column, no release, no outbox row | MSG-P7-003 | AC2, TC-E7-017-02 |
| X2 | The caller lacks the partner-portal right of the operation | 403 before any read or write | MSG-P4-002 | TC-E7-017-03 |
| X3 | The same claim is submitted twice, or the instruction already carries it | 409; one claim and one EV-21 remain | None | TC-S9-E7017-APP-02 |
| X4 | The instruction belongs to a partner of another firm | 404; the scope comes from the caller's firm, never from a parameter | None | BR8 |
| X5 | A result file is outside the allowed set | 415; nothing is recorded | None | TC-S9-E7017-APP-02 |
| X6 | The claim reaches an instruction already `DONE` or `RECALLED` | 409; the status is not moved backwards | None | §9, BR5 |
| X7 | The claim is refused | The refusal is recorded, the invoice stays blocked, the status stays `IN_PROGRESS` | None | TC-S9-E7017-APP-01 |
| X8 | An approval arrives for an instruction with no recorded claim | 422; no record is written | MSG-GEN-001 | TC-S9-E7017-APP-01 |
| X9 | A statement reaches a `v_ace_*` view, an `rwb_asset` row or another schema | The grant refuses it and the boundary test fails the build | None (pipeline log) | TC-S9-E7017-APP-03, BR6 |

X1 and X2 are the legacy exception flows of FSD S9 A2.14.4.3; X3 to X9 are the paths the portal writes, the workflow approval and the schema boundary add.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against RWB-S9-E7017-CON, the record library and the composite-route fake, on its own schema, with no live S5 or P4 |
| Negotiable | The activity names, the claim's internal shape and the screen fragment are this story's design; the criterion, the base, the rights, the element flags and the screens are fixed |
| Valuable | An extra cost on a held asset is recorded once and approved or refused with a record that can be defended |
| Estimable | Two writes, one transaction, one check, one approval step, one event and two screen fragments |
| Small | Two weeks with its tests on the fakes |
| Testable | Each path runs on a synthetic instruction, with the record library forced to fail and to pass |

### 7. Acceptance criteria

```gherkin
Feature: Manage extra costs and services on an asset

  Scenario: AC2 Not recorded (legacy RWB-E7-017 AC2)
    Given the rwb-decision contract mock returns a stopped decision record
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC2 is the legacy criterion word for word, with its origin tag added and nothing else changed: "the decision log cannot be written", "the action is taken", "nothing changes" and MSG-P7-003 all stand. Its cross-service part is the decision record, so AC2 carries the one `Given the rwb-decision contract mock returns a stopped decision record` line and that is the only addition. AC1, the recording and approval of the additional cost, is owned by RWB-ITG-E7017-ITG; the component behaviour behind it is proved by TC-E7-017-01, so no criterion is restated.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The claim is a result on `partner_instruction`: `result_code` and `fee_amount` hold it, the evidence goes to rwb-document, and no cost table and no column is added | DF-PRT-015, DF-PRT-016; GAP-3133; ASM-5483 |
| BR2 | The decision record is written before any row moves; a failed write leaves claim, status and invoice as they were and answers MSG-P7-003 | DP-03; R-UNI-39; AC2 |
| BR3 | A claim is recorded once per instruction: the `Idempotency-Key` rule, the 409 on a repeat and one EV-21 publication per claim | TSD S9 T-A.2; X3, X6 |
| BR4 | The fee is checked against the fee schedule version in force and the recorded result; both are read with their version and neither is computed here | REQ-S9-004; BR-S9-014; ASM-5489 |
| BR5 | The approval and the refusal move only `status` within LOV-INSTR-STATUS: `DONE` on approval, `IN_PROGRESS` on refusal; no new state and no new list value | TSD S9 T3.2; ASM-5485 |
| BR6 | The asset, its holding cost and the work order stay with rwb-asset; no `v_ace_*` view, no `rwb_asset` row and no foreign key leaves `rwb_partner` | DP-01, DP-05; ASM-5486 |
| BR7 | No value a business person may change is written in code: the cost type, the schedule, the approval limit and the coded refusal reason are reference data or rule rows read with their version | BR-S9-014; FSD S9 A2.14.3.1 |
| BR8 | The scope of every read and write is the firm of the caller's `partner_user` row; a parameter never widens it | TSD S9 T6.2; X4 |
| BR9 | No personal data in a row, a file, a log or a workflow input: an instruction, a case reference, a code, an amount and a date | Template and Rules §R7.2 (s17); TSD S9 T6.2 |
| BR10 | One base, one topic, one queue, one schema and one login per service, and the claim announces on the service's own pair only | DP-13, DP-14; Template and Rules §R4; ASM-5488 |

Lists this story reads, copied from TSD S9 T3.2 and published unchanged:

| List | Values | Use here |
|---|---|---|
| LOV-INSTR-STATUS | `SENT`, `ACCEPTED`, `DECLINED`, `IN_PROGRESS`, `DONE`, `RECALLED` | The status a claim and an approval move, and the one it refuses (X6) |
| LOV-INSTRUCTION | `COLLECT`, `FILE_SUIT`, `ENFORCE`, `APPRAISE`, `REPOSSESS`, `LIST`, `SELL` | The type of the instruction the cost is claimed against |
| LOV-PANEL | `ACTIVE`, `ON_NOTICE`, `SUSPENDED`, `EXITED` | Read to refuse a claim from a firm that has left the panel |
| LOV-PARTNER-TYPE | `AGENCY`, `LAW_FIRM`, `VALUER`, `AUCTION_VENDOR`, `BROKER`, `DEBT_BUYER`, `AMC`, `RAMC` | Read only, to show the firm that claims the cost |

### 9. State transitions

| From (`status`) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `SENT`, `ACCEPTED` | A cost claim recorded | The claim and its evidence are valid and the record is written | `IN_PROGRESS` | rwb-partner, this story |
| `IN_PROGRESS` | The approval | The claim is inside the fee schedule version and the result is recorded | `DONE`, invoice released | rwb-partner, this story |
| `IN_PROGRESS` | The refusal | The claim is outside the schedule or the result is missing | `IN_PROGRESS`, invoice blocked | rwb-partner, this story |
| `DONE`, `RECALLED` | A further claim | Any | Unchanged; 409 | none (X6) |
| `SENT`, `ACCEPTED`, `IN_PROGRESS` | A recall of the partner | R-UNI-25 to R-UNI-30 | `RECALLED` | the recall stories of the module |

| Invoice | Event | Condition | To |
|---|---|---|---|
| Submitted | The approval of its claim | The claim is approved | Released for payment against `fee_amount` |
| Submitted | The refusal of its claim | The claim is refused | Blocked; the refusal stands on the record |
| Submitted | A forced record failure | The record cannot be written | Submitted, unchanged (X1) |

The states are the lists of TSD S9 T3.2 and this story adds none; a claim whose status no source names sits at `IN_PROGRESS`, which is the only value the list offers (ASM-5485).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG, partner and agency manager | CRUDA: the primary role of FSD S9 A2.14.3.3, approving and refusing a claim |
| RW-NPAMGR, NPA and asset manager | CRU: the also-uses role of FSD S9 A2.14.3.3, reading the claim against the asset |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE, RW-GUARANT | CRU: record and approve where their rights allow; they are among the holders of U in the legacy table |
| RW-HEADLIT, RW-HEADNPA, RW-HEADASL | RA: read the claim and the record |
| RW-CASEOWN, RW-TEAMMGR, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL, RW-TRIBE | R: read only, refused the approval |
| PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC | RU: partner users, scoped to their firm, recording the claim and refused the approval |
| rwb-partner service identity | Writes the claim row, the record and the outbox row, serves the operations and sends the approval signal; no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S9 T6.1 and nothing wider: the legacy table names eight roles and "21 more", and T6.1 resolves them to the 23 `RW-*` and 6 `PT-*` identities above, which are 29 and agree with the legacy count. DP-08 is not in the pattern set: the right is enforced by the platform guard (ASM-5487).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-008, DF-PRT-009, DF-PRT-010 | partner_instruction (S9, `rwb_partner`) | id, case_id, partner_id | Read; `case_id` is a reference carried into EV-21, never a foreign key across schemas |
| DF-PRT-011 to DF-PRT-013 | partner_instruction (S9, `rwb_partner`) | instruction_type, instructed_at, due_at | Read only, shown on SCR-35 |
| DF-PRT-014 | partner_instruction (S9, `rwb_partner`) | status | Write, `IN_PROGRESS` and `DONE` over LOV-INSTR-STATUS |
| DF-PRT-015 | partner_instruction (S9, `rwb_partner`) | result_code | Write, the code of the claim or of the refusal |
| DF-PRT-016 | partner_instruction (S9, `rwb_partner`) | fee_amount | Write, the amount claimed and released |
| DF-PRT-001 to DF-PRT-007 | partner (S9, `rwb_partner`) | id, partner_code, partner_name, partner_type, panel_status, contract_end, score | Read only, to scope the claim and refuse a firm at `EXITED` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, in `rwb_partner`) | decision code, rule id, rule version, inputs, from and to state, decided at | Write through the library, before the row moves |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset (P1; asset record S5) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and 6 more | Not read: the asset reference is an identifier and the asset is read through rwb-asset (ASM-5486) |

**No new table, no new column and no migration** is declared: the claim rides on `partner_instruction`, the record, the key and the outbox are library objects created in `rwb_partner` by the library's migration (DP-03), and the evidence file is rwb-document's.

**No personal data.** The claim carries an instruction, a case reference, a code, an amount, a date and a file reference. No customer name, contact value or identity number is read into a row, an answer, a log or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). This story supplies the two writes the claim is made and paid by.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/partner/instructions/{instructionId}/results` (API-S9-005) | Multipart `result` and `files` in, `PartnerInstruction` out with `resultCode`, `feeAmount`, `status` | Partner portal, right U, scope applied | `Idempotency-Key` |
| POST | `/partner/instructions/{instructionId}/invoices` (API-S9-006) | `InvoiceRequest` in, `Invoice` out | Partner portal, right C, scope applied | `Idempotency-Key` |

API-S9-005 answers 401, 403 with MSG-P4-002, 404, 409, 415, 422 with MSG-GEN-001 and 503; API-S9-006 answers 401, 403, 404, 409, 422 and 503. Both sets are TSD S9 T-A.2's and neither is widened. No operation approves or refuses a claim: the service has six and none does, so the approval is a signal on `InstructionWorkflow` (§12.5) and not a route (GAP-3133; ASM-5484).

#### 12.2 REST operations consumed

None. The right is enforced by the platform guard and the asset reaches SCR-35 through rwb-asset's own fragment, so no consumed operation, no read of `rwb-asset` and no read of `rwb-source-data` is declared; the plan's contract-dependency row is empty (ASM-5486, ASM-5487).

#### 12.3 Events published

| Event | Name | Payload | Consumed by |
|---|---|---|---|
| EV-21 `PartnerResultSubmitted` | `rwb.partner.PartnerResultSubmitted.v1` | `caseId`, `instructionId`, `resultCode`, `resultedAt` | The case-owning service, rwb-litigation, rwb-asset and rwb-reporting |
| `DecisionRecorded` (library) | `rwb.decision-record.v1` | The record reference, the decision code, the rule id and its version | rwb-decision, which seals it in the central ledger |

Both go through the outbox, the CloudEvents envelope and the retry and `.dlt` topics (DP-09). EV-21 is published once per recorded claim; the decision record is the library's publication (DP-03). EV-20 `InstructionIssued` is not on this path, and nothing announces an approval, a refusal or an invoice (GAP-3133; ASM-5488).

#### 12.4 Events consumed

None. The claim is made by a person or a partner on the portal and the approval is a signal on this service's own workflow, so the story holds no consumer group, no subscription and no inbox row. FSD S9 A2.14.4.4 declares no background event for the feature.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction | `rwb-partner` in namespace `rwb-recovery` | Signal `costApproval` (approve or refuse, the claim reference, the reason) |
| `recordCostClaim` | Activity | `rwb-partner` | The claim in; the instruction with `resultCode`, `feeAmount` and `status` out, record first |
| `writeCostDecisionRecord` | Activity | `rwb-partner` | The claim and the rule version in; the record reference out |
| `approveCostInvoice` | Activity | `rwb-partner` | The instruction and the approval in; the invoice released or blocked, and the status out |

`InstructionWorkflow` is the one workflow in the ownership rows; this story adds the `costApproval` signal and its activities and creates no second workflow, no Schedule and no child of `CaseWorkflow`, which stays with rwb-case (ASM-5484).

#### 12.6 Schedules

None. The service's job list is empty in the ownership rows (Jobs: None) and the claim is event-driven on the workflow, so no Temporal Schedule, no Quartz row and no shared job table is declared (ADR-016).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| partner_instruction | S9 (`rwb_partner`) | The claim and its approval; this story writes `result_code`, `fee_amount` and `status` |
| partner | S9 (`rwb_partner`) | The firm and its panel status; read only here |
| partner_user | S9 (`rwb_partner`) | The caller's firm and period; read only here, to scope the claim |
| decision_record | PLT library, in `rwb_partner` | The local hash-linked record of the claim and the approval (DP-03) |
| idempotency_key | PLT library, in `rwb_partner` | The key and the stored answer of the two writes |
| outbox_event | PLT library, in `rwb_partner` | The relay row of EV-21, one per recorded claim |

Not owned and never read as a table: the asset record and `v_ace_npa_asset` (S5, P1), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8). No foreign key leaves the schema (DP-01), and the claim has no table of its own (GAP-3133; ASM-5483).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| Partner-portal right and identity fake | Right R, C and U per operation, and a caller of one firm | X2, X4 |
| gateway-bff composite route fake (SCR-35, SCR-34) | The claim, the instruction and the asset fragment of the caller's firm, before and after an approval | §15, TC-S9-E7017-APP-01 |
| Instruction and cost fixture | One instruction of a type from LOV-INSTRUCTION with a claim, its amount and its evidence | TC-E7-017-01 |
| rwb-document upload stub (P5) | A stored document reference, and a 415 for a type outside the allowed set | X5 |

The fakes are test-only and are replaced by the real services in SIT; RWB-ITG-E7017-ITG swaps them for the owners and asserts the same paths end to end.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 0 consumed | API-S9-005 and API-S9-006 on `/api/recovery/partner/v1`; the guard and the asset fragment are not contract rows of this key |
| Kafka | 1 published + the library's record event, 0 consumed | `rwb.partner.events.v1` with its retry and `.dlt` topics, and `rwb.decision-record.v1` from the library |
| Temporal | 1 workflow signal, 3 activities, 0 Schedules | `InstructionWorkflow` with `costApproval`, `recordCostClaim`, `writeCostDecisionRecord`, `approveCostInvoice` |
| File | The result file and the invoice attachment | Uploaded to rwb-document through its owner; the service keeps the reference, never the bytes |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `cost`; front end `src/modules/recovery/partner/PlacementAllocation.tsx`.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is applied as a prohibition: the legacy data section reads `v_ace_npa_asset`, and after the split that view and the asset record are rwb-asset's, so this service holds no `AceSourceQuery` and no grant and the asset reference arrives as an identifier (ASM-5486). DP-13 gives the two writes their base and DP-19 is how SCR-35 and SCR-34 reach this service. DP-09, which the outbox carries, DP-04, which a fee rule would need, and DP-08, which the rights carry, are not in the pattern set: the outbox follows the platform library, the fee is a reference-data comparison and not a Drools decision, and the right is enforced by the guard (GAP-3133; ASM-5487, ASM-5489).

| Component | Type | Responsibility |
|---|---|---|
| `CostClaimController` | Controller | Serves API-S9-005 and API-S9-006, maps the error envelope, enforces the `Idempotency-Key` |
| `CostClaimService` | Service | Validates the claim, checks it against the schedule version and the result, decides the approval path |
| `CostDecisionRecordWriter` | Service | Writes the record before a row moves, through the library (DP-03) |
| `CostClaimRepository` | Repository | The two transactions on `partner_instruction` and the read of the caller's firm |
| `CostApprovalSignal` | Workflow client | Sends `costApproval` to `InstructionWorkflow` and reports the outcome |
| `PlacementAllocation` | React component | SCR-35 with the claim, its evidence, the schedule version and the asset fragment |

**Database and migrations.** No Flyway file: the columns are those of `partner_instruction` and `partner`, and the record, the key and the outbox are library objects created in `rwb_partner` (DP-03).

**Configuration.** The cost type, the fee schedule, the approval limit and the coded refusal reason are reference data with their version (BR7); the capability area "Partner portal" and its rights are access rows; the retry and timeout of the two writes are platform configuration.

**Build steps**

1. `CostClaimController` and the two writes against the fakes, record first, with the error envelope (AC2, X1).
2. `recordCostClaim` as one transaction over `result_code`, `fee_amount` and `status`, with the repeat refused at 409 (X3, X6).
3. The fee check against the schedule version and the recorded result, and the approval and refusal paths (TC-S9-E7017-APP-01, X7, X8).
4. The `costApproval` signal with its idempotent repeat, and `approveCostInvoice` releasing or blocking the invoice.
5. The outbox publication of EV-21 once per claim, with its envelope and its `.dlt` path (BR3).
6. `PlacementAllocation` through the composite route fake, with the asset fragment and the states of §15.
7. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no asset row, no case write, no approval route (X9, BR6).

**Feature flag.** `rwb.partner.cost-claim-v1`; off means the two writes answer 503, the approvals wait and no row moves.

**Done when.** The tests of section 16 pass, a claim is recorded once with one EV-21, an approved claim releases its invoice at `DONE` and a refused one keeps it blocked, a forced record failure leaves the row unchanged with MSG-P7-003, a caller of another firm sees 404, no `v_ace_*` read and no asset write exists, and SCR-35 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the claim is absent or invalid, or an approval arrives with no claim (VR-S9-014-1; X8) | Enter {field}. |
| MSG-P4-002 | The role lacks the partner-portal right of the operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the claim or the approval moves a row (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are those of the legacy and FSD sets; the text is copied unchanged, no message is reworded and no new one is added. MSG-GEN-001 is VR-S9-014-1, MSG-P4-002 is the legacy refusal, and MSG-P7-003 is AC-EXC-S9-014-02 of FSD S9 A2.14.4.3 and the text of AC2.

### 15. Screens and states

SCR-35 Placement and allocation is where the cost is recorded and approved and SCR-34 Partner list is where the firm and its panel status are read (FSD S9 Screens; legacy table: both "Loading; list"). Both arrive through the gateway-bff composite route (DP-19), and a partner outside the bank arrives on the partner gateway of FAPI 2.0 (Arch v5 slide 8; INT-24).

| State on SCR-35 | What it shows | Act available |
|---|---|---|
| Loading | The instruction, its claim and the asset fragment being composed | None |
| Claim recorded | The amount, the evidence, the schedule version and an `IN_PROGRESS` instruction | Approve, refuse |
| Approved | The instruction at `DONE` and the invoice released | Read the record |
| Refused | The instruction at `IN_PROGRESS`, the invoice blocked, the coded reason | Re-claim once the cause is fixed |
| Not recorded | The claim unchanged, MSG-P7-003 shown (AC2) | Retry |

The screen field lists and the asset fragment belong to RWB-PLT-N001-CON and to rwb-asset's screens; the legacy table gives both screens "Loading; list" and no further state, so the refusal reason is Not specified in the source documents (GAP-3133; ASM-5485).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-017-01 | The claim is recorded and approved (legacy AC1, end to end in RWB-ITG-E7017-ITG) | Component | One instruction against a held asset, one claim with its amount and evidence; the row recorded, the status moved, EV-21 published once |
| TC-E7-017-02 | AC2 | Component | The record stub stopped; the claim unchanged, no outbox row, MSG-P7-003 |
| TC-E7-017-03 | Access | Component | A role without the partner-portal right; 403 with MSG-P4-002 and no read or write |
| TC-E7-017-04 | Principle 5 | Component | A forced record failure at the approval; status and invoice unchanged |
| TC-S9-E7017-APP-01 | Approval, refusal, X7, X8 | Component | A claim inside the schedule version and one outside it, and an approval with no claim; `DONE` with the invoice released, `IN_PROGRESS` with it blocked, 422 on the last |
| TC-S9-E7017-APP-02 | X3, X5 | Component | The same claim twice and a disallowed file type; 409 with one claim and one EV-21, 415 with nothing written |
| TC-S9-E7017-APP-03 | X9, BR6 | Component | A statement on a `v_ace_*` view, an `rwb_asset` row and a second schema; every one refused and the boundary test red |

The four legacy cases are those of RWB-E7-017 in their legacy order, with the Level column added: every case runs on the fakes and against this service's own rows, so every case is `Component`. TC-E7-017-01 exercises AC1, which RWB-ITG-E7017-ITG owns and proves end to end; its `-ITG` copy stays with that story and is not repeated here. The three cases `TC-S9-E7017-APP-01` to `-03` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: the cost type, the fee schedule, the approval limit, the refusal reason, the states and the right stay reference data and rule rows.
- No personal data in a row, a file, a workflow input or a log: an instruction, a case reference, a code, an amount and a date only.
- ACE data only through the owner's contract or `v_ace_*` views, and this service holds no `v_ace_*` grant at all (DP-05).
- The asset stays with rwb-asset and the case with rwb-case: no asset row and no case row is written here (BR6).
- The record is written before the rows and before the release; a build that answers outside its transaction fails the review (BR2).
- One base, one topic, one queue, one schema and one login per service (DP-13, DP-14).
- A claim is a fact announced once; a second publication or a new approval event fails the absence test (BR3, BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results | The fee check, the approval and `fee_amount` | TC-E7-017-01, TC-S9-E7017-APP-01 |
| REQ-S9-009 | Field work and its evidence reach the case through the field application | The claim and its evidence file on the instruction | TC-E7-017-01, TC-S9-E7017-APP-02 |
| REQ-S9-001 | Every partner type is managed on the same six points, contract and fees among them | The claim of the partner against its instruction | TC-E7-017-01 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the claim | TC-E7-017-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E7017-APP-03 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | EV-21 through the outbox, with its retry and `.dlt` topics | TC-S9-E7017-APP-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two writes on the partner base | TC-E7-017-02 |
| ADR-022 | Local decision record plus central ledger | The record written before the claim and the approval | TC-E7-017-02, TC-E7-017-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-017, disposition Split (rework); legacy feature FEAT-PRM-14 (FSD S9 A2.14) |
| Legacy criteria | AC2, owned word for word by this story; AC1 is RWB-ITG-E7017-ITG's |
| Wave and release | Wave 4 and release 31 May 2027 (tentative), copied unchanged; EP07 is wave 4 and the service's Arch v5 wave is 4, so no W-MAP conflict is raised (ASM-5490) |
| Legacy dependency | "Depends on FEAT-AST-07" is a monolith feature predecessor, not a build row; the asset side is rwb-asset's (ASM-5486) |
| Legacy endpoints | API-S9-005 and API-S9-003 on `/api/recovery/partner/v1`; the first is built here, the second is the read story's |
| Source text | Legacy RWB-E7-017; FSD S9 Partner management v3 A1.1, A1.3, A2.14, A2.14.1 to A2.14.4; TSD S9 Partner management v2 T2, T3.0, T3.1, T3.2, T5.3, T6.1, T6.2, T-A |
| Test cases | The four legacy cases as the component half, and the three new cases TC-S9-E7017-APP-01 to -03 |
| Feature and screens | FEAT-PRM-14 and its prerequisite FEAT-AST-07; SCR-35 Placement and allocation and SCR-34 Partner list |
| Rules | BR-S9-014, VR-S9-014-1, R-UNI-39, and R-DIS-10 to R-DIS-12 at the work order |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the element flags, the rights, the error set and the fakes: RWB-S9-E7017-CON.
- The end-to-end proof of AC1 and the harness that swaps the fakes for the owners: RWB-ITG-E7017-ITG.
- The held asset, its holding cost, the work order, the provision step and the holding states: rwb-asset (S5) and FEAT-AST-07.
- The fee schedule, the panel and the service levels as reference data: FEAT-PRM-02, and the panel change FEAT-ADM-07.
- The cost type, the approval limit and the refusal reason as values: Not specified in the source documents (GAP-3133; ASM-5485, ASM-5489).
- The partner read, the issue, the accept and the decline of an instruction and its close: the instruction stories and API-S9-001 to API-S9-004.
- The recall, the re-selection and the notice on a missed target: R-UNI-25 to R-UNI-30 and their stories.
- The payment of a released invoice and its posting: rwb-payment (P8).
- The roles and rights as code, the partner's sign-in and the FAPI 2.0 token: rwb-access (P4) and the partner gateway.
- The deployment, the flag, the dashboards, the alerts and the runbook: the operations story of this legacy key.
