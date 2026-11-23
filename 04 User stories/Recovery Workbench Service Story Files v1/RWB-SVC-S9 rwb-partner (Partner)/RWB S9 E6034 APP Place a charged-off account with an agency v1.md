# RWB-S9-E6034-APP Place a charged-off account with an agency

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6034-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S9-K |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E6034-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the placement slice of RWB-E6-034 in rwb-partner. The two legacy criteria are kept word for word with their origin tag; the step issues the instruction that places a post charge-off account with the agency the measured-return allocation picks, writes the `partner_instruction` row at `SENT`, records the result through the local decision-record library with the rule version in force **before** the instruction is sent (DP-03), serves `POST /cases/{caseId}/instructions` (API-S9-002) on base `/api/recovery/partner/v1` (DP-13), publishes EV-20 `InstructionIssued` on `rwb.partner.events.v1`, and reaches SCR-35 and SCR-34 through the gateway-bff composite route (DP-19). The legacy story names two read endpoints and no write operation; `partner_instruction` carries no rule-version or decision column; S9 owns no route set, so the placement rule is only expressible as the D9 rows R-WO-29 to R-WO-32; the legacy permission table gives right R while the operation needs C; the plan's C row is empty while the case and the rule package are consumed; DP-04 and DP-09 are absent; and no requirement row traces to FEAT-PRM-06 (GAP-3117; ASM-5394, ASM-5395, ASM-5396, ASM-5397, ASM-5398, ASM-5399, ASM-5402). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **to place post charge-off accounts with an agency under the placement rule**, so that **partners are placed, paid and measured by rule**.

This is the placement slice of legacy RWB-E6-034. It owns:

- the two legacy criteria this story owns (AC1, AC2), copied verbatim with their origin tag, and the messages, the operation and the screens they depend on;
- one step of `InstructionWorkflow` on task queue `rwb-partner` in namespace `rwb-recovery`, executed by the `issueInstruction` activity the architecture names on this service (context pack, Temporal and Drools slides; Arch v5 slide 12 notes);
- the issue of the instruction that places the account: the case reference, the partner reference and the instruction type are taken on the request, the agency is the one the measured-return allocation of FEAT-PRM-03 picks under the placement rule, and the result is one `partner_instruction` row at status `SENT` (FSD S9 A2.6.2; TSD S9 T3.1, T3.2);
- the record of the placement through the local decision-record library, with the rule version in force, **before the instruction is sent**, because AC1 asks for the result in the decision log with the rule version (DP-03; ASM-5395, ASM-5396);
- EV-20 `InstructionIssued` on `rwb.partner.events.v1` with IDs only, because R-WO-30 sends the instruction and the service owns the instruction event set (ASM-5397);
- `POST /cases/{caseId}/instructions` (API-S9-002) on base `/api/recovery/partner/v1`, with the Partner portal right C, the scope filter, the `Idempotency-Key` header, the `InstructionRequest` body and the `PartnerInstruction` answer of TSD S9 T-A.2 (DP-13);
- SCR-35 Placement and allocation and SCR-34 Partner list in their list states behind the gateway-bff composite route, where the officer confirms the placement (DP-19).

It does not own: the published shapes of the three operations, the `Partner`, `PartnerInstruction` and `InstructionRequest` elements, the consumed rows, the error set and the fakes, which are RWB-S9-E6034-CON; the onboarding and the panel (RWB-S9-E6029-APP, RWB-S9-E6030-APP) and the allocation and its override (RWB-S9-E6031-APP, RWB-S9-E6032-APP); the intake of a partner result (RWB-S9-E6033-APP) and the fee (RWB-S9-E6035-APP), with the accept, results and invoices operations they serve; the two read operations of this key, first published in E2 and E4; the case of record and its route states, which are rwb-case (P3), and the D9 states, which are the write-off route set's (S7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: places post charge-off accounts with an agency under the placement rule, because partners are instructed and paid by email and spreadsheet and allocation is not based on performance (FSD S9 A1.3, A2.6.1). Placements by scorecard are measured at 100 percent on the decision log and the Workbench records, reviewed monthly (FSD S9 A2.6.1). What D-RCV-60 changes is who owns the case, the partner, the rule, the record, the event and the screens.

- **The instruction is this service's.** `partner` and `partner_instruction` are S9's tables in `rwb_partner` (context pack, ownership rows owned by S9; TSD S9 T3.1, T3.3), and the instruction status machine SENT to RECALLED is the module's own list (TSD S9 T3.2); the placement is written as one row of `partner_instruction` and nothing else.
- **The row has no rule column.** No field of DF-PRT-008 to DF-PRT-016 carries a rule version, a decision reference or a placement-rule code (TSD S9 T3.1), and the FSD field catalog of A2.6.3.2 lists the eight partner and instruction fields only. The rule version and the picked agency therefore live in the decision record, which is also what legacy AC1 asks for (GAP-3117; ASM-5395).
- **The placement rule has no set of its own.** The routing logic carries ten route sets and none of them is a partner set: the placement is expressible only as the D9 rows R-WO-29 to R-WO-32, where the agency is chosen on measured return, and the measured-return choice itself is the allocation of FEAT-PRM-03, which is this feature's declared prerequisite (Business Rules and Routing Logic v4, Route sets sheet; FSD S9 A1.1; ASM-5396).
- **The package is read, not embedded.** The placement rows are governed in rwb-decision by the default ruling, and DP-04 is not in this key's pattern set, so the version in force arrives on a package read and is recorded with the placement (ASM-5396).
- **The case stays where it is.** The D9 state `PLACEMENT_DECIDED` and the move to `PLACED_WITH_AGENCY` are states of the write-off route set of 27 states (Business Rules and Routing Logic v4, States sheet), held by rwb-case and the write-off stage; this story issues the instruction against a case reference and writes no `recovery_case` row and no stage column (ASM-5398).
- **The officer's right is short.** The FSD names the Partner and agency manager as primary and the Credit Administration officer as also-uses, while the legacy permission table gives the Partner portal right R and the issue needs C; the right is taken from the access matrix and the conflict is recorded (GAP-3117; ASM-5399).
- **The placement is announced.** R-WO-30 sends the instruction, and the service owns EV-20 `InstructionIssued` on its own topic, so the issue is a fact other services can hear with IDs only and no personal data (ASM-5397).

No business value moves: the instruction type, the panel statuses, the partner types, the instruction statuses, the right and the rule version are list values and rule rows, read with their version and never written in code.

### 3. Preconditions

- RWB-S9-E6034-CON is published: API-S9-002 with its `Idempotency-Key` header and its error set, the `Partner`, `PartnerInstruction` and `InstructionRequest` elements, the consumed rows, the right, the lists and the fakes are baselined and handed to this story.
- The rwb-case case read is published with its fake: the case and its post charge-off state. The operation name is Not specified in the source documents (GAP-3117; ASM-5398).
- The rwb-decision placement-rule read is published with its fake and answers the D9 rows R-WO-29 to R-WO-32 at their version in force (GAP-3117; ASM-5396).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-35 and SCR-34 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The allocation step is in place: the agency is the one the measured-return rule picks for the case, and a case with no agency on the panel is held and escalated under R-WO-31, which the allocation story owns (FSD S9 A2.6.2; Business Rules and Routing Logic v4).
- `partner` and `partner_instruction` exist in schema `rwb_partner` from the DB story of this service, with the columns of DF-PRT-001 to DF-PRT-016 and the standard record columns of TSD S9 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on schema `rwb_partner`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, `rwb_decision` or an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E6034-CON when its tests pass.

### 4. Flow

1. The post charge-off treatment is decided for the case under R-WO-29, and the placement type is `soft_recovery`, so an agency on the panel has to receive the account; this story reads that state only (Business Rules and Routing Logic v4).
2. The partner and agency manager opens SCR-35 Placement and allocation through the gateway-bff composite route, one hop, and reads the case, its placement decision and the panel with its scores (DP-19).
3. The officer confirms the placement. The screen sends the case reference, the partner reference the allocation picked and the instruction type; the operation declares the `Idempotency-Key` header (TSD S9 T-A.2).
4. `PartnerInstructionController` serves `POST /cases/{caseId}/instructions` (API-S9-002) on base `/api/recovery/partner/v1`, declares the Partner portal right C with the scope applied and validates the inputs (DP-13).
5. The service reads the case on the rwb-case contract: the case exists, it carries the case reference of the path and it is post charge-off. A case that is not is refused with 409 and nothing is written (ASM-5398).
6. The service reads the partner row in `rwb_partner`: its code, name, type, panel status, contract end and latest score. A partner that is not `ACTIVE` on the panel, or whose type is not the instruction's, is refused with 409 (FSD S9 A2.6.3.2; TSD S9 T3.2).
7. The service reads the placement rule in force on the rwb-decision contract and holds its version; the agency must be the one the measured-return allocation picked for that case (ASM-5396).
8. `PartnerInstructionService` prepares the instruction: the case reference, the partner reference, the instruction type of LOV-INSTRUCTION, the instructed-at time, the due-at time from the panel service level and the status `SENT`. No rule value is a branch of the code (FSD S9 BR-S9-006).
9. `PartnerDecisionRecordWriter` writes one decision record through the local decision-record library, **before the instruction is sent**: the case reference, the partner reference, the instruction type, the picked agency, the rule version in force and the decided-at time. A failed write stops the step with nothing changed (DP-03; AC1, AC2).
10. The instruction row is written and committed with the record in one transaction; the service publishes EV-20 `InstructionIssued` through the outbox with IDs only: the case, the partner and the instruction (ASM-5397).
11. The answer returns the `PartnerInstruction` element with its reference and status `SENT`, and the officer sees the placement on SCR-35, read back from this service (DP-19).
12. A repeat of the same request answers the instruction that exists and writes no second one, matched on the `Idempotency-Key` header; the due-at time and the service level are reference data, not a constant.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no instruction is issued and no row is written, and the case stays with its placement decision | MSG-P7-003 | AC2, TC-E6-034-02, TC-E6-034-04 |
| X2 | The role does not hold the Partner portal right C | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E6-034-03 |
| X3 | A required element is absent or invalid: the partner reference, the instruction type, or a body that fails validation | 422 with nothing written and no record | MSG-GEN-001 | AC1, X7 |
| X4 | The partner is not `ACTIVE` on the panel, its contract has ended, or its type is not the instruction's | 409 with nothing written; the placement is refused and the case keeps its decision | MSG-GEN-001 | AC1, X7 |
| X5 | The case is not on the case reference given, or it is not post charge-off | 404 or 409 with nothing written; no instruction is issued against another case | None | AC1, X7 |
| X6 | The rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written; the caller sees 503 with the platform error envelope | None | AC1, X2 |
| X7 | A repeated request with the same `Idempotency-Key` | One instruction and one record; the repeat answers the instruction that exists | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR6 |

X1 and X2 are the legacy exception paths of the key carried onto the slice (the legacy set also carries MSG-GEN-001, kept in section 14), X3 to X7 are the paths the target call types and the interactive trigger add, and X8 is the ACE and schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E6034-CON, the rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P3 or P7 |
| Negotiable | The activity name, the record's internal shape and the due-at rule are this story's and the baseline's choice; the operation, the right, the message set, the screens and the two criteria are fixed |
| Valuable | A charged-off account reaches the agency the measured-return rule picks, with the rule version on record, instead of by email and spreadsheet with no performance basis |
| Estimable | One workflow step, one activity, one record write, one operation, one event, two clients and two read-only screen states |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic post charge-off case through the contract fakes, plus the access, panel, case, repeat and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Place a charged-off account with an agency

  Background:
    Given case "RW-2026-000731" is post charge-off at state "PLACEMENT_DECIDED" with placement type "soft_recovery"
    Given the partner "AG-014" is on the panel with panel status "ACTIVE" and the instruction type "COLLECT"
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Place a charged-off account with an agency (legacy RWB-E6-034 AC1)
    Given the rwb-case contract mock returns the post charge-off case and its placement decision
    Given the rwb-decision contract mock returns the rule version in force
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then places post charge-off accounts with an agency under the placement rule
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E6-034 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E6-034 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `the user acts on the screen`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so AC1 carries two `Given the <service> contract mock returns <x>` lines, and those are the only additions. AC2 has no cross-service part and is copied with nothing added. The same outcome is the one FSD S9 AC-S9-006-01 records as written one epic ahead — "The data and rules it needs are in place / The user acts / The result is recorded with its rule version" — so the legacy line and the module line agree. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_partner`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

S9 owns no route set: the routing logic carries ten sets and the placement is expressible only through the D9 rows of the Write-off set (Business Rules and Routing Logic v4, Route sets sheet). The three rows below are the placement rows this step reads and does **not** own; they are copied character for character, and they are the rows that decide that an account goes to an agency and that the instruction is sent.

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-29 | Write-off | D9 | FINANCE_FEED_SENT | POST_CHARGEOFF_RULE_RUN | finance_feed_status = accepted | Decide the post charge-off treatment under D9.3 | PLACEMENT_DECIDED | Partner and agency manager | Rules component | 5 working days |
| R-WO-30 | Write-off | D9 | PLACEMENT_DECIDED | SOFT_RECOVERY_SELECTED | placement_type = soft_recovery and an agency on the panel has capacity | Place the account with the agency chosen on measured return and send the instruction | PLACED_WITH_AGENCY | Outsourced agency | Partner Portal, OA portal | same day on the portal |
| R-WO-31 | Write-off | D9 | PLACEMENT_DECIDED | NO_AGENCY_CAPACITY | no agency on the panel has capacity | Hold the placement and escalate on the timer | PLACEMENT_DECIDED | Partner and agency manager | Partner Portal | 5 working days |

Their owner and systems columns name a business role and systems, not services: "Partner Portal" is this service's base and the partner gateway in front of it, "Rules component" is rwb-decision's package, and "Outsourced agency" is the party the instruction is issued to. R-WO-30 is the placement rule the legacy story names without an ID; it says "send the instruction", which is the step this story builds, and the move to `PLACED_WITH_AGENCY` is the D9 stage's (GAP-3117; ASM-5396, ASM-5398).

| ID | Rule | Source |
|---|---|---|
| BR1 | The placement is one `partner_instruction` row at status `SENT` in `rwb_partner`, written by `InstructionWorkflow` on `rwb-partner`; no case row and no case state column is written | TSD S9 T3.1, T3.2; context pack ownership rows (tables, workflow); FSD S9 A2.6.2 |
| BR2 | The result is recorded before the instruction is sent, with the rule version in force, the picked agency and the instruction type; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S9 T2 ("writes the decision log entry before any change"); legacy AC1 and AC2 |
| BR3 | Only a case that is post charge-off at its placement decision, and only an `ACTIVE` partner on the panel of the instruction's type, is placed; any other case or partner is refused with nothing written | Business Rules and Routing Logic v4 rows R-WO-29, R-WO-30, R-WO-31; FSD S9 A2.6.3.1, A2.6.3.2; TSD S9 T3.2 |
| BR4 | The agency is the one the measured-return allocation of FEAT-PRM-03 picks under the rule version in force; the placement never chooses a partner by rotation, habit or a code branch | FSD S9 A1.2 (FEAT-PRM-03), A2.6.1; ASM-5396 |
| BR5 | The case and its placement decision are read on rwb-case's contract and never as a `recovery_case` row or a `v_ace_*` view; the case reference is an identifier of another service's fact | DP-05 as a prohibition; TSD S9 T5.2; ASM-5398 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_partner`; `case_id` and `partner_id` are identifiers, not foreign keys across schemas | DP-01; TSD S9 T3.3 |
| BR7 | The rule version in force is read from rwb-decision and recorded with the placement; no rule row of S9 is recorded, because the service owns none | ASM-5396; TSD S9 T4 |
| BR8 | The instruction declares the `Idempotency-Key` header and a repeat with the same key writes one row and one record | TSD S9 T-A.2; ASM-5394 |
| BR9 | Every value a business person may change is a list or a rule row read with its version: the instruction type, the instruction status, the panel status, the partner type, the service level and the rule version | FSD S9 BR-S9-006; legacy Guardrails |
| BR10 | EV-20 `InstructionIssued` carries IDs only: the case, the partner and the instruction; no name, amount, contact value or identity number enters the event, a workflow input or a log | Template and Rules §R7.2 (s17); TSD S9 T6.2; ASM-5397 |

### 9. State transitions

The case route state is not changed by this story: `PLACEMENT_DECIDED` is a decision point of the D9 write-off set, and the move to `PLACED_WITH_AGENCY` is recorded on that stage by its own story. What this story owns is the instruction and its row.

| From (D9 state, write-off route set) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `PLACEMENT_DECIDED` | `SOFT_RECOVERY_SELECTED` | placement_type = soft_recovery and an agency on the panel has capacity | `PLACED_WITH_AGENCY` | the D9 stage on R-WO-30; this story sends the instruction and publishes EV-20 (ASM-5398) |
| `PLACEMENT_DECIDED` | `NO_AGENCY_CAPACITY` | no agency on the panel has capacity | `PLACEMENT_DECIDED` | the D9 stage on R-WO-31; nothing is issued here |
| Any state but `PLACEMENT_DECIDED` | A placement request | The case is not post charge-off at its placement decision | Unchanged | none; 409 (X5) |
| `PLACEMENT_DECIDED` | A placement request | The partner is not `ACTIVE` on the panel or its type is not the instruction's | Unchanged | none; 409 (X4) |

| Instruction status (rwb-partner) | Event | Condition | To |
|---|---|---|---|
| none | A placement request | The record is written and the row commits | `SENT` |
| none | A placement request | The record write fails (X1) | none; nothing is written |
| `SENT` | `InstructionAcceptance` | The agency accepts or declines | `ACCEPTED` or `DECLINED`, by the accept story |
| `ACCEPTED` | A progress report | The agency reports it is working the case | `IN_PROGRESS`, by the result story |
| `IN_PROGRESS` | A result is recorded | The result is accepted on the portal | `DONE`, by the result story |
| Any active status | A recall | The placement is recalled under R-WO-34 or R-UNI-26 | `RECALLED`, by the recall story |

The six instruction statuses are those of LOV-INSTR-STATUS in TSD S9 T3.2 (`SENT`, `ACCEPTED`, `DECLINED`, `IN_PROGRESS`, `DONE`, `RECALLED`); this step writes `SENT` only, and the D9 states are those of the write-off route set of 27 states in the States sheet of the Business Rules and Routing Logic v4.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG, partner and agency manager | Partner portal CRUDA in TSD S9 T6.1: the primary role of FSD S9 A2.6.3.3, placing an account with the operation's right C |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT | Partner portal CRU: the six further roles that hold C, which is the legacy table's right R widened by the matrix (ASM-5399) |
| RW-HEADLIT, RW-HEADNPA, RW-HEADASL | Partner portal RA: approve and read; they hold no C and place nothing |
| PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC | Partner portal RU: the partner identities read and update their own instructions, scoped to their own firm, and place nothing |
| RW-CASEOWN, RW-TEAMMGR, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL, RW-TRIBE | Partner portal R: read only, in scope, and refused the placement |
| Credit Administration officer | The FSD's also-uses role of A2.6.3.3; TSD S9 T6.1 has no row for it, so it holds no Partner portal right until the access owner adds one (GAP-3117; ASM-5399) |
| rwb-partner service identity | Prepares the instruction, writes the record and the row, publishes EV-20 and serves the operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S9 T6.1 and nothing wider. The right this story needs is C: TSD S9 T-A.2 declares right C on API-S9-002, and seven identities hold it — RW-AGENCYMG and the six `CRU` roles. The legacy permission table gives the Partner portal right R to the eight roles it names "and 21 more", and those 21 resolve exactly to the fifteen further staff roles and the six `PT-*` partner identities of the matrix, which is 29 identities in all (GAP-3117; ASM-5399). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 | partner (S9, `rwb_partner`) | id | Read, the partner reference the request carries; recorded in the decision record |
| DF-PRT-002, DF-PRT-003 | partner (S9, `rwb_partner`) | partner_code, partner_name | Read, to name the partner on the answer and the screen; never copied into the event |
| DF-PRT-004 | partner (S9, `rwb_partner`) | partner_type | Read, the type the instruction must suit: LOV-PARTNER-TYPE |
| DF-PRT-005, DF-PRT-006 | partner (S9, `rwb_partner`) | panel_status, contract_end | Read, the panel test: `ACTIVE` and an unexpired contract (R-WO-30) |
| DF-PRT-007 | partner (S9, `rwb_partner`) | score | Read, the latest scorecard result the measured-return choice rests on; not written here |
| DF-PRT-008, DF-PRT-009, DF-PRT-010 | partner_instruction (S9, `rwb_partner`) | id, case_id, partner_id | Write, the instruction reference, the case of the placement and the agency |
| DF-PRT-011, DF-PRT-012, DF-PRT-013 | partner_instruction (S9, `rwb_partner`) | instruction_type, instructed_at, due_at | Write, the type of LOV-INSTRUCTION, the time of the issue and the due time from the panel service level |
| DF-PRT-014 | partner_instruction (S9, `rwb_partner`) | status | Write `SENT`; the later statuses are the accept, result and recall stories' |
| DF-PRT-015, DF-PRT-016 | partner_instruction (S9, `rwb_partner`) | result_code, fee_amount | Not written: the result story and the fee story own them (R-WO-33, R-WO-37) |
| No field ID | partner_user (S9, `rwb_partner`) | The panel user of the partner; TSD S9 T3.1 has no field catalog for it and the table exists only in the context pack's ownership rows (GAP-3117; ASM-5399) | Not read and not written: the partner sign-in is the portal's, and a placement creates no user |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_partner`) | rule id, rule version, decision code, inputs reference, reason, from and to state, decided at | Write through the local library, before the instruction is sent: the case, the partner, the instruction type, the picked agency and the rule version |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case arrives on the rwb-case read and as the path reference |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rule version arrives on the package read |

Field IDs are those of TSD S9 T3.1 and the Logical Data Model and Data Dictionary, and the case, ledger and rule rows are the rows the legacy Data table lists, with their owners changed to P3 and P7 by the target. **No new table, no new column and no migration**: the tables arrive with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_partner` by the libraries' own migrations (DP-03, DP-09). The placement's rule version and decision reference have no column in `partner_instruction` and live on the record only (GAP-3117; ASM-5395).

**No personal data.** The rows carry identifiers, codes, dates, list values, an amount of the fee story and a rule version. The partner is a firm and its users are portal identities; no name of a person, contact value or identity number enters `rwb_partner`, the record, the event, a log or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). This story supplies API-S9-002 and uses the two reads the same baseline declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/instructions` (API-S9-002) | `InstructionRequest` in, `PartnerInstruction` out at status `SENT` with its decision-record reference | Partner portal, right C, scope applied | `Idempotency-Key` header |
| GET | `/partners` (API-S9-001) | `Partner[]` out with the panel status and the score; first in E2, declared by the baseline and built by the panel stories, not here (ASM-5394) | Partner portal, right R, scope applied | Not applicable |
| GET | `/partner/instructions` (API-S9-003) | `InstructionPage` out for the caller's own firm; first in E4, declared by the baseline and built by the instruction stories, not here (ASM-5394) | Partner portal, right R, scope applied | Not applicable |

API-S9-002 answers 400, 401, 403 with MSG-P4-002, 404 for a case that is not on the reference, 409 for a case that is not at its placement decision or a partner that is not on the panel, 422 with MSG-GEN-001 and 503, each with the error envelope and one message of section 14. The paths, the operation ids, the element names, the rights and the error codes are published in TSD S9 T-A.1 and T-A.2; the property lists of `InstructionRequest` and `PartnerInstruction` carry the placeholder of section 11 of the baseline (GAP-3117; ASM-5394).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3117; ASM-5398)) | `/api/recovery/case/v1` | P3 rwb-case | The case and its post charge-off state; read only, faked |
| The placement-rule read in force (operation name Not specified in the source documents (GAP-3117; ASM-5396)) | `/api/recovery/decision/v1` | P7 rwb-decision | The D9 placement rows R-WO-29 to R-WO-32 at their version; read only, faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). Both rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3117; ASM-5396, ASM-5398).

#### 12.3 Events published

| Event | Name | Topic | Payload | Fan-out |
|---|---|---|---|---|
| EV-20 | `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` with its retry and `.dlt` topics | IDs only: the case reference, the partner reference and the instruction reference; no personal data | To the case that moves to `PLACED_WITH_AGENCY` and to the reporting read model; the consumer set is Not specified in the source documents (GAP-3117; ASM-5397) |

EV-20 is the service's own instruction event (context pack, ownership rows: EV-20 and EV-21; TSD S9 T5.3 lists `InstructionIssued` as published). One event per instruction and one producer group: this story publishes EV-20 for a post charge-off placement and RWB-S9-E6031-APP publishes the same event for a scorecard allocation, so no second event, no second topic and no second outbox is added. The relay is the outbox of the platform library, and DP-09 is not in this key's pattern set, so `RWB-PLT-TE006-CON` is recorded as an absent H row (ASM-5397). EV-21 `PartnerResultSubmitted` belongs to RWB-S9-E6033-APP and is not declared here.

#### 12.4 Events consumed

None. The trigger is the officer's confirmation on SCR-35 after the post charge-off treatment decision of R-WO-29, and the FSD declares no background event for the feature (FSD S9 A2.6.4.4). The service therefore holds no consumer group, no subscription and no inbox row for this step, and a build that adds one fails the absence test. The placement decision arrives through the placement-rule read of §12.2 and never as a command event, because events announce and Temporal commands.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction, continues-as-new across the instruction's life | `rwb-partner` in namespace `rwb-recovery` | Input: the case reference, the partner reference, the instruction type and the rule version in force; signals: the acceptance, the result and the recall; outcome: the instruction status |
| `issueInstruction` | Activity, the one placement step of the workflow; the architecture names it as the activity other routes call on rwb-partner | `rwb-partner` | The case reference, the partner reference, the instruction type and the rule version in; the instruction reference and its status out, with the record written before the instruction is sent |

`InstructionWorkflow` is the one workflow the context pack gives S9. The activity name `issueInstruction` comes from the Arch v5 slide 12 notes ("activity issueInstruction on rwb-partner"), so no name is invented. No child workflow exists in this service.

#### 12.6 Schedules

None. The placement is an officer-driven step and owns no Temporal Schedule, no Quartz row and no shared job table; the service's job list is empty in the context pack's ownership rows (Jobs: None). The placement timer of R-WO-31 and the recall timers of R-WO-34 are the write-off stage's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| partner | S9 (`rwb_partner`) | The outside firm on the panel; read here for the type, the panel status, the contract end and the score, and never written |
| partner_instruction | S9 (`rwb_partner`) | Work placed with a partner on a case; this story inserts one row at status `SENT` |
| partner_user | S9 (`rwb_partner`) | The panel user of the partner; not used by a placement |
| decision_record | PLT library, created in `rwb_partner` | The local hash-linked decision record of the placement (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of API-S9-002 and the answer it holds |
| outbox_event | PLT library, created in `rwb_partner` | The relay of EV-20 (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | The post charge-off case of `RW-2026-000731` at `PLACEMENT_DECIDED`, and a case that is not post charge-off | AC1, X5 |
| rwb-decision placement-rule fake | The D9 rows R-WO-29 to R-WO-32 at their version in force, and a package that cannot answer | AC1, X6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-35 answer for the case of `RW-2026-000731` and the panel of `AG-014`, before and after the placement | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the case read and the rule read carry the placeholder until their owners confirm them (GAP-3117; ASM-5396, ASM-5398).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 consumed | API-S9-002 on `/api/recovery/partner/v1/cases/{caseId}/instructions`, with the two reads of the same base declared and not built here; the case read and the rule read; one hop, 2 s |
| Kafka | 1 published, 0 consumed | EV-20 `InstructionIssued` on `rwb.partner.events.v1` with IDs only; no consumed event |
| Temporal | 1 workflow and 1 activity | `InstructionWorkflow` and `issueInstruction` on `rwb-partner`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `instruction`; front end `src/modules/recovery/partner/PlacementAllocation.tsx`, the fragment SCR-35 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the instruction commit together or not at all. DP-13 moves the base of the legacy paths and gives API-S9-002 its home. DP-19 is how SCR-35 and SCR-34 reach this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-09 (the outbox and inbox library) and DP-05 (the case read) are real dependencies of the step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3117; ASM-5396, ASM-5397, ASM-5398).

**Dependencies the tables add and the plan does not hold.** The two consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the package is read as data and the row in force is recorded, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed by EV-20. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `InstructionWorkflow` placement branch | Workflow | Runs the placement step on `rwb-partner`, reads the rule version and reports the instruction status |
| `issueInstruction` | Activity | Reads the case and the partner, evaluates the placement, writes the record and the row and answers |
| `PlacementService` | Service | Applies R-WO-30 over the rule version in force: the case test, the panel test, the type test and the measured-return choice |
| `PartnerDecisionRecordWriter` | Library adapter | Writes the record with the rule version before the instruction is sent, hash-linked; refuses the step when the write fails |
| `PartnerInstructionController` | Controller | API-S9-002 with the Partner portal right C, the scope, the `Idempotency-Key` and the problem mapping |
| `CaseClient` | Client | The case read of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `RulePackageClient` | Client | The placement-rule read of rwb-decision at its version in force |
| `InstructionOutbox` | Library adapter | Publishes EV-20 `InstructionIssued` with IDs only, in the row's transaction |
| `PlacementAllocation` | React component | Shows the case, the placement decision, the panel with its scores and the issued instruction on SCR-35, and the partner list on SCR-34 |

**Database and migrations.** No Flyway file. The `partner` and `partner_instruction` tables arrive with the DB story of this service, and the record, the key and the outbox are library objects created in `rwb_partner` by the libraries' migrations (DP-03, DP-09). No column is added for the rule version or the decision: neither has a source (ASM-5395).

**Configuration and reference data.**

- The placement rows R-WO-29 to R-WO-32, the rule version, the panel statuses, the partner types, the instruction types and the instruction statuses: rule rows and lists read with their version, never written in code (ASM-5396).
- The capability area "Partner portal" and its rights: access rows of rwb-access, read through the guard.
- The due-at time comes from the panel service level, which the panel story holds as reference data; the placement itself sets no timer.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. The placement branch of `InstructionWorkflow` and its input record, registered on `rwb-partner` with the officer's confirmation as its signal.
2. `CaseClient` against its fake, with the 2 s budget, the breaker and the not-post-charge-off path (AC1, X5, X6).
3. `RulePackageClient` against its fake, with the version in force recorded with the placement (AC1).
4. `PlacementService` over the rule version, with the case, panel, type and measured-return tests and the refusal path (AC1, X3, X4).
5. `PartnerDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC2, X1).
6. `PartnerInstructionController` with API-S9-002, right C, the scope, the `Idempotency-Key` and the problem mapping of the declared errors, and `PlacementAllocation` on SCR-35 and SCR-34 through the composite route fake (AC1, X2, X7).
7. `InstructionOutbox` with EV-20 and its IDs-only payload, with the outbox test (BR10).
8. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or any other schema, and no case state column (X8, BR5, BR6).

**Feature flag.** `rwb.partner.placement-v1`, a flag of the platform library; off means the operation answers 503 with no write and SCR-35 hides the placement action, and the allocation, result and fee stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic post charge-off case in SIT, the placement is recorded with the rule version in force, a case that is not post charge-off and a partner that is not on the panel are refused, a repeated request writes once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, EV-20 carries IDs only, and SCR-35 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element is absent or invalid: the partner reference, the instruction type, or a partner that is not on the panel (X3, X4) | Enter {field}. |
| MSG-P4-002 | A role without the Partner portal right C calls the placement (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the instruction is sent (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are those of the legacy message set of RWB-E6-034; the text is the legacy and FSD wording, copied unchanged, and no message is reworded and no new one is added. The legacy table carries no module message of its own, so none is declared.

### 15. Screens and states

SCR-35 Placement and allocation and SCR-34 Partner list are served through the gateway-bff composite route (DP-19). The route calls rwb-partner for the panel, the scores and the issued instruction, and rwb-case for the case and its placement decision; this story fixes the rwb-partner answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives SCR-35 "Loading; list" and SCR-34 "Loading; list". This story produces the placement from the list state of SCR-35: a placed account shows the agency, the instruction reference and its status `SENT`, and the state stays "list". Neither screen is described anywhere as a placement form, so the form in which the officer confirms the placement and its field list are Not specified in the source documents (GAP-3117; ASM-5400). The refusal, not-post-charge-off, not-on-panel, repeat and not-recorded states read the messages of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-034-01 | AC1 | Component | The post charge-off case of `RW-2026-000731` on the fakes; the partner of `AG-014`, the panel test, the rule version, the record, the `SENT` row and EV-20 asserted |
| TC-E6-034-02 | AC2 | Component | The decision-record stub stopped; nothing written, no row and MSG-P7-003 shown |
| TC-E6-034-03 | Access | Component | A role without the Partner portal right C; 403 with MSG-P4-002 and no read |
| TC-E6-034-04 | Principle 5 | Component | A forced decision log write failure inside the transaction; the case is unchanged and no instruction exists |

The four legacy cases are those of RWB-E6-034 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the placement rows, the panel statuses, the partner types, the instruction types and statuses, the service level, the right and the rule version stay rule rows and reference data, never a constant, a default or a branch.
- No personal data in `rwb_partner`, an event, a workflow input or a log: identifiers, codes, dates, list values and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table.
- The case stays with rwb-case: no `recovery_case` row, no case state column and no case write here (BR5, BR6).
- The partner row is read, not written: a placement sets the panel status of no partner and writes no column of `partner`.
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no data-lake extract and no `recovery_log` write.
- The record is written before the instruction is sent; a build that sends the instruction outside the record's transaction fails the review (DP-03).
- The instruction is issued to one partner for one case: a bulk placement across a population is not part of this step (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-PRM-06 | The requirement this feature serves is Not specified in the source documents (GAP-3117; ASM-5402): TSD S9 T8 maps every REQ-S9 row to FEAT-PRM-01 or FEAT-PRM-08 | The trace rests on the legacy key, the feature row and the module criterion | TC-E6-034-01 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the instruction and the partner panel | TC-E6-034-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-E6-034-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | EV-20 with IDs only on `rwb.partner.events.v1`, relayed by the outbox | TC-E6-034-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-E6-034-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the instruction is sent | TC-E6-034-02, TC-E6-034-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-034, disposition Split (rework); feature FEAT-PRM-06 |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Wave and release | Wave 4 and release 30 April 2027 (tentative), copied unchanged from the plan; EP06 is wave 4 and the service's Arch v5 wave is 4, so the W-MAP wave is not earlier and no conflict is raised (ASM-5401) |
| Source text | Legacy RWB-E6-034; FSD S9 Partner management v3 A1.2, A1.3, A2.6, A2.6.2, A2.6.3 and A2.6.4; TSD S9 Partner management v2 T2, T3.1, T3.2, T3.3, T4, T5.2, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-29, R-WO-30 and R-WO-31; Recovery Workbench Epics 3 to 8 Specification v3 row FEAT-PRM-06 |
| Test cases | TC-E6-034-01 to TC-E6-034-04 |
| Feature and screens | FEAT-PRM-06, SCR-35 Placement and allocation, SCR-34 Partner list |
| Rules | R-WO-29, R-WO-30 and R-WO-31 read as the D9 placement rows; S9 owns no route set (ASM-5396) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the three operations, the `Partner`, `PartnerInstruction` and `InstructionRequest` elements, the consumed rows, the error set and the fakes: RWB-S9-E6034-CON.
- The onboarding and the panel, and the measured-return allocation and its override: RWB-S9-E6029-APP, RWB-S9-E6030-APP, RWB-S9-E6031-APP and RWB-S9-E6032-APP.
- The intake of a partner result and the fee, with the accept, results and invoices operations: the E4 instruction stories, RWB-S9-E6033-APP, RWB-S9-E6035-APP and the Epic 6 invoice story.
- The two read operations of this key, API-S9-001 and API-S9-003, which are first published in E2 and E4 and declared in the baseline only (ASM-5394).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3). The D9 states `PLACEMENT_DECIDED`, `PLACED_WITH_AGENCY` and `PLACEMENT_RECALLED`: the write-off route set (S7) (ASM-5398).
- The authoring, testing, approval and versioning of the placement rows R-WO-29 to R-WO-32: rwb-decision (P7) (ASM-5396).
- The partner portal sign-in, its multi-factor rule and the partner gateway in front of this service: the edge stories and the ACE Common sign-in (FSD S9 NFR-049, NFR-050).
- The notification of the agency that an instruction exists: rwb-comms, on its own contract.
- The gateway-bff composite route and the field list of SCR-35 and SCR-34: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
