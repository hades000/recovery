# RWB-S9-E6032-APP Override an allocation with a reason

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6032-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S9-I |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E6032-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the override slice of RWB-E6-032 in rwb-partner. Legacy AC2 is kept word for word with its origin tag; the step lets the partner and agency manager place work with a partner other than the one the scorecard rule picked, writes the reason to the local decision record with the rule ID and the rule version in force **before any change** (DP-03), ends the previous `partner_instruction` at `RECALLED` and creates the replacement at `SENT` (DF-PRT-009, DF-PRT-010, DF-PRT-014), and serves the override branch of the published `POST /cases/{caseId}/instructions` (API-S9-002) under base `/api/recovery/partner/v1` (DP-13), reached from SCR-35 Placement and allocation through the gateway-bff composite route (DP-19). No source publishes an override operation, an override element or a reason property on the request; no rule row or decision code of the Business Rules and Routing Logic v4 names the placement override; the instruction status list has no published transition table; the legacy permission table gives right U while the operation declares right C; SCR-35 and SCR-34 carry "Loading; list" only and name no override action; and no requirement row traces to FEAT-PRM-04 (GAP-3112; ASM-5379, ASM-5380, ASM-5381, ASM-5382, ASM-5384, ASM-5385, ASM-5387). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E6032-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **to place work with a different partner from the one the scorecard rule picked, with the reason recorded**, so that **partners are placed, paid and measured by rule**.

This is the override slice of legacy RWB-E6-032 (FEAT-PRM-04). It owns:

- AC2, the one legacy criterion the plan gives this story, copied verbatim with its origin tag, and the messages and the failure path it depends on;
- the override step of `InstructionWorkflow` on task queue `rwb-partner` in namespace `rwb-recovery`, the step that re-places one instruction of a case;
- the re-placement record: the previous `partner_instruction` ends at `RECALLED` and the replacement is created at `SENT`, with `partner_id`, `instruction_type`, `instructed_at` and `due_at` (DF-PRT-009 to DF-PRT-014);
- the reason, written through RWB-PLT-E1027-CON to the local decision record with the case, the instruction, the partner replaced, the partner chosen, the rule ID and the rule version in force, **before the placement changes** (DP-03);
- the override branch of the published `POST /cases/{caseId}/instructions` (API-S9-002) on `/api/recovery/partner/v1`, partner-portal right C, scope applied (DP-13);
- the override action on SCR-35 Placement and allocation behind the gateway-bff composite route, with the partner choice read from SCR-34 Partner list (DP-19).

It does not own: the published shapes of the operation, of the `InstructionRequest` and `PartnerInstruction` elements and of the `overrideReason` property, the rights of the document and the fakes, which are RWB-S9-E6032-CON; the scorecard placement the override departs from (RWB-S9-E6031-APP); the partner panel, fee schedule and contract terms (RWB-S9-E6030-APP); the onboarding of a partner (RWB-S9-E6029-APP); the intake of a partner result (RWB-S9-E6033-APP); the case of record, its stage and its clock, which are rwb-case (P3); the officer assignment of the case, `assignment` DF-WRK-009 to DF-WRK-016, which is P3's and is not changed here; the `decision_log_entry` ledger and the rule rows, which are rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective and the problem are unchanged from the legacy story and the module FSD: the partner and agency manager may place work differently from the scorecard result, with the reason recorded, because partners are instructed and paid by email and spreadsheet and allocation is not based on performance (FSD S9 A1.3, A2.4.1). The metric is unchanged too — placements by scorecard, 100 percent, measured on the decision log and the Workbench records, reviewed monthly (FSD S9 A2.4.1). What D-RCV-60 changes is where the placement lives, where the reason lives, which operation serves the action and who owns the case.

- **The placement is this service's row.** `partner_instruction` is S9's (context pack ownership rows; TSD S9 T3.1, DF-PRT-008 to DF-PRT-016), and it carries the partner, the instruction type, the instructed and due dates and the status. The legacy data table also names `assignment`, which is P3's officer assignment; an override of the partner changes no officer, so that table is neither read nor written here.
- **The reason has a published home.** The API Specification v5 gives `DecisionLogEntry` an `overrideReason` of up to 1000 characters, "Reason when the person did not follow the recommendation". The override is exactly that case, so the reason is written to the decision record and to that element, and `partner_instruction` needs no reason column (ASM-5381).
- **The override has no operation of its own.** The six published operations of the service (context pack ownership rows; TSD S9 T-A.1) carry the issue of an instruction as API-S9-002 `POST /cases/{caseId}/instructions` with right C, and nothing for an override. The two endpoints the legacy story lists — a read of the caller's instructions and a result post — place no work at all. The override is therefore declared as a branch of API-S9-002 with one additive optional property, `overrideReason`, whose name and length are the published decision-log element's (GAP-3112; ASM-5380).
- **The rule version is reference data.** BR-S9-004 says no value a business person may change is written in code: it is read from reference data with its version. The rows of the Business Rules and Routing Logic v4 that re-select a partner are R-LIT-29, R-DIS-31, R-WO-35 and R-UNI-45, and none of them is an override with a reason or names the partner and agency manager's override; the rule ID, the rule set and the decision code therefore carry the placeholder and are recorded as read, never invented (GAP-3112; ASM-5382).
- **The right is C, and the legacy U is narrower.** TSD S9 T-A.1 declares right C on API-S9-002 and T6.1 gives RW-AGENCYMG CRUDA; the legacy permission table gives "Partner portal" R and U. The override creates a replacement instruction, so right C is taken over the operation matrix and the narrower legacy right is recorded as a conflict rather than widened (GAP-3112; ASM-5384).
- **The case stays with rwb-case.** `case_id` is an identifier of another service's fact; the stage, the route and the clock are not written here, and no REST call is made to rwb-case (DP-01, DP-11).
- **The screen is a composite.** SCR-35 Placement and allocation and SCR-34 Partner list are described only as "Loading; list" and no source says where the override action sits on them; the action is placed on SCR-35 in its list state and the partner choice is read from SCR-34 through the same composite route (GAP-3112; ASM-5385).
- **No requirement row names the feature.** TSD S9 T8 maps REQ-S9-001 to REQ-S9-004 and REQ-S9-008 to FEAT-PRM-01 and REQ-S9-005 to REQ-S9-007 and REQ-S9-009 to FEAT-PRM-08, and the legacy story carries no REQ id, so the story cites no requirement until the E6 BRD and the PRD publish one (GAP-3112; ASM-5387).

No business value moves: the partner types, panel states, instruction types, instruction statuses, the metric target, the rule version and the right stay reference data and rule rows, read with their version and never written in code.

### 3. Preconditions

- RWB-S9-E6032-CON is published: the override branch of API-S9-002, the additive `overrideReason` property, the elements, the rights, the error set, the consumed row and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-35 Placement and allocation reaches this service through the gateway-bff composite route, one hop, and no screen calls the service directly (DP-19).
- `partner_instruction` and `partner` exist in schema `rwb_partner` from the DB story of this service, with the columns and the lists of TSD S9 T3.0, T3.1 and T3.2; this story adds no table, no column and no migration, and writes `partner_id`, `instruction_type`, `instructed_at`, `due_at` and `status` only.
- A placement exists on the case: one `partner_instruction` in `SENT`, `ACCEPTED` or `IN_PROGRESS` (LOV-INSTR-STATUS), created by the allocation step (FEAT-PRM-03). An instruction already `DECLINED`, `DONE` or `RECALLED` is not overridden.
- The partner chosen is an existing row of `partner` with its `panel_status` of LOV-PANEL and its `score`; the partner panel is maintained by FEAT-PRM-02 and is read, not changed, here.
- The rule version in force is available from the rule-row read of rwb-decision; the operation name is Not specified in the source documents (GAP-3112; ASM-5382).
- The service runs as its own login on schema `rwb_partner`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E6032-CON when its tests pass.
- Wave 4 and release 30 April 2027 are the plan's and are copied unchanged, the release marked tentative; EP06 is wave 4 and the service's Arch v5 wave is 4, so no wave conflict is raised (ASM-5386).

### 4. Flow

1. The allocation step has placed one instruction of the case with a partner (FEAT-PRM-03), and the `partner_instruction` row is in `SENT`, `ACCEPTED` or `IN_PROGRESS`.
2. The partner and agency manager opens SCR-35 Placement and allocation through the gateway-bff composite route and reads the placements of the case with their partner, their instruction type, their due date and their status (DP-19).
3. The manager chooses to place the work differently, picks the partner from SCR-34 Partner list, and enters the reason; the screen sends the case, the instruction type, the chosen partner, the due date and the reason (FSD S9 A2.4.2).
4. `PartnerInstructionController` serves the override branch of `POST /cases/{caseId}/instructions` (API-S9-002) under base `/api/recovery/partner/v1`, declares partner-portal right C with the scope applied, honours the `Idempotency-Key` header and validates the request (DP-13).
5. The service reads the current `partner_instruction` of the case in `rwb_partner`: its reference, its case, its partner, its instruction type and its status. An instruction that is not open, or a partner that does not exist, is refused with 409 or 404 and nothing is written.
6. The service reads the chosen `partner` row: its code, its name, its type and its panel status. A partner that is not on the active panel is refused under the rule in force and no branch of the code decides it.
7. `PlacementRuleReader` reads the rule row in force on the rwb-decision contract and holds its rule ID and its version for the record; the read is one hop with a 2 s budget and a breaker (ASM-5382).
8. `PlacementDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case, the instruction being replaced, the partner replaced, the partner chosen, the instruction type, the rule ID, the rule version in force, the reason as `overrideReason`, the deciding identity and the decided-at time. A failed write stops the step with nothing changed (DP-03; AC2).
9. `RecordAndApply` writes in one transaction: `status` = `RECALLED` on the replaced row, and a new `partner_instruction` at `SENT` with `partner_id`, `instruction_type`, `instructed_at`, `due_at` and the standard columns. `result_code` and `fee_amount` of the recalled row are left as they are.
10. The answer returns the new `PartnerInstruction` element with its reference, its partner, its due date and its status; the manager sees the replacement on SCR-35, read back from this service (DP-19).
11. The step returns its outcome to the stage that hosts the placement; the case, its stage and its clock stay with `CaseWorkflow` on `rwb-case` and are not written here.
12. A repeat with the same `Idempotency-Key` answers the instruction that exists and writes no second one. No personal name, contact detail or identity number is copied into the record, the answer or a log.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision record cannot be written | Nothing changes: the placement stays as it was and no replacement row is created | MSG-P7-003 | AC2, TC-E6-032-02, TC-E6-032-04 |
| X2 | The role does not hold the partner-portal right C | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E6-032-03 |
| X3 | The instruction is not `SENT`, `ACCEPTED` or `IN_PROGRESS`, or it is not on that case | 409 or 404 with nothing written; a closed placement is never reopened by an override | MSG-GEN-001 | AC2, X1 |
| X4 | The chosen partner is absent, or its panel status is not the one the rule requires | 422 with nothing written; the panel value stays the list's and never the code's | MSG-GEN-001 | X1 |
| X5 | The rwb-decision rule-row read does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written; the caller sees 503 with the platform error envelope | None | X1 |
| X6 | The reason is absent or empty | 422 with nothing written: an override without a reason is not recorded | MSG-GEN-001 | X1 |
| X7 | A repeated request with the same `Idempotency-Key` | One replacement and one answer; the repeat answers the record that exists | None | X1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR8 |

X1 and X2 are the legacy exception paths carried onto the slice (the legacy set also carries MSG-GEN-001, kept in section 14); X3 to X7 are the paths the target call types and the interactive trigger add; X8 is the ACE and schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E6032-CON, the rwb-decision rule-row fake and the decision-record stub, on its own schema, and needs no live P3, P7 or P10 |
| Negotiable | The activity name, the record's internal shape and the front-end component are this story's and the baseline's choice; the operation, the right, the lists, the messages, the screen and the criterion are fixed |
| Valuable | Every departure from the scorecard result carries the reason, the rule ID and the rule version that were in force, instead of a placement known only to the manager |
| Estimable | One workflow step, one rule reader, one record write, one operation branch, one client and one screen state |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | The criterion runs on a synthetic placement through the contract fakes, plus the access, closed-placement, absent-reason and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Override an allocation with a reason

  Background:
    Given case "RW-2026-000512" has the partner instruction "PI-000241" placed with the agency "AG-014" at state "SENT"
    Given the partner "AG-021" is on the panel and holds the latest scorecard result
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Not recorded (legacy RWB-E6-032 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC2 is the legacy criterion of RWB-E6-032 word for word, with its origin tag added and nothing else changed: the wording of `the decision log cannot be written`, `the action is taken` and `MSG-P7-003` all stand. It has no cross-service part, so no `Given the <service> contract mock returns <x>` line is added. AC1 of the legacy story — "lets the partner manager place work differently, with the reason recorded", with the result written to the decision log with the rule version — is owned by RWB-ITG-E6032-ITG, the wave 4 harness, whose integration row lists this story; the behaviour it exercises at the end of the chain is the step this story builds in sections 4 and 8, and its rule-version part is the read of step 7. The module criterion AC-S9-004-01 agrees with AC1: "The data and rules it needs are in place / The user acts / The result is recorded with its rule version" (FSD S9 A2.4.4.1). The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_partner`, with the central `decision_log_entry` ledger of rwb-decision appended from `rwb.decision-record.v1` behind it.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The override is one step of the instruction: it runs in `InstructionWorkflow` on `rwb-partner`, ends the current `partner_instruction` at `RECALLED` and creates the replacement at `SENT`; it writes those two rows and nothing else | TSD S9 T3.1, T3.2; FSD S9 A2.4.2; context pack ownership rows (workflow `InstructionWorkflow`) |
| BR2 | The result is recorded before the change, with the rule ID, the rule version in force and the reason; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S9 T2 ("writes the decision log entry before any change"); legacy AC2 |
| BR3 | Only an instruction in `SENT`, `ACCEPTED` or `IN_PROGRESS` of that case is overridden, and only to a partner that exists; any other state, case or partner is refused | TSD S9 T3.1, T3.2; FSD S9 VR-S9-004-1; legacy exception paths |
| BR4 | The reason is required and is written as `overrideReason` to the decision record; `partner_instruction` has no reason column and none is added | API Specification v5 `DecisionLogEntry.overrideReason`; TSD S9 T3.1; ASM-5381 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_partner`; `case_id` is an identifier of another service's fact and the officer assignment of P3 is not read | DP-01; TSD S9 T3.3; legacy Data |
| BR6 | The rule ID, the rule set and the decision code are read with their version from the rule row in force and recorded as read; no rule row of the Routing Logic set names this override | FSD S9 BR-S9-004; ASM-5382 |
| BR7 | Every value a business person may change is a rule row or reference data read with its version: LOV-PARTNER-TYPE, LOV-PANEL, LOV-INSTRUCTION, LOV-INSTR-STATUS, the metric target and the right | FSD S9 BR-S9-004; legacy Guardrails |
| BR8 | No personal data in `rwb_partner`, the decision record, a log or a workflow input; the deciding identity is a user key and not a name | Template and Rules §R7.2 (s17); TSD S9 T6.2 |
| BR9 | The instruction is not recalled on the partner portal and no notice is sent by this step: the recall rules R-UNI-25 to R-UNI-29 belong to the partner-management stories and are not fired here | Business Rules and Routing Logic v4 rows R-UNI-25 to R-UNI-29; ASM-5383 |
| BR10 | The same request twice writes one replacement and sends one answer, matched on the `Idempotency-Key` the published operation declares | TSD S9 T-A.2 |

The rows that re-place work in the Business Rules and Routing Logic v4 are R-LIT-29 (the next firm on the scorecard), R-DIS-31 (the next vendor on the scorecard), R-WO-35 (the next agency on the scorecard) and R-UNI-45 (re-selection after a recall). Each of them fires on a partner step of its own route set, none is an override with a reason, and none names the partner and agency manager's decision, so this story fires no row of the set and records the version it read (GAP-3112; ASM-5382).

### 9. State transitions

| From (`partner_instruction.status`) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `SENT` | The override of the placement | A different partner is chosen and the reason is recorded | `RECALLED` | rwb-partner, this story |
| `ACCEPTED` | The override of the placement | A different partner is chosen and the reason is recorded | `RECALLED` | rwb-partner, this story |
| `IN_PROGRESS` | The override of the placement | A different partner is chosen and the reason is recorded | `RECALLED` | rwb-partner, this story |
| New row | The override commits | The record is written and the replaced row has ended | `SENT` | rwb-partner, this story |
| `DECLINED`, `DONE`, `RECALLED` | An override request | The placement is closed | Unchanged; 409 | none |
| `SENT` | `INSTRUCTION_ACCEPTED` | The partner accepts on the portal | `ACCEPTED` | the instruction-acceptance step (API-S9-004) |
| `ACCEPTED` | `PARTNER_RESULT_SUBMITTED` | A result arrives from the portal | `IN_PROGRESS` | the result step (FEAT-PRM-05, RWB-S9-E6033-APP) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | An override request for an open instruction | The placement and the partner are read | Evaluating |
| Evaluating | The rule row in force is read | The partner is on the active panel | Recording |
| Evaluating | The partner is refused by the rule | The panel status is not the one the rule requires | Waiting, 422 |
| Recording | The record and the two rows commit | The transaction commits | Waiting for the next request |
| Recording | Either write fails | X1 | Waiting, nothing changed |

`LOV-INSTR-STATUS` publishes the six values `SENT`, `ACCEPTED`, `DECLINED`, `IN_PROGRESS`, `DONE` and `RECALLED` (TSD S9 T3.2) and no source publishes the transition table of that list; only the two moves this step writes and the two moves of the acceptance and result steps are stated here, and the rest of the list's transitions carry the placeholder (GAP-3112; ASM-5379).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG, partner and agency manager | Partner portal CRUDA in TSD S9 T6.1: the primary role of FSD S9 A2.4.3.3, recording an override through the operation's right C |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC | Partner portal C or RU as T6.1 gives it: the eighth role and the five further holders the legacy permission table's "and 5 more" resolves to (ASM-5384) |
| RW-CASEOWN, RW-TEAMMGR, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL, RW-TRIBE | Partner portal R: read only, in scope, and refused the override with MSG-P4-002 |
| rwb-partner service identity | Reads the placement, the partner and the rule row, writes the record and the two rows and serves the operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S9 T6.1 and nothing wider. The operation needs right C: TSD S9 T-A.1 declares C on API-S9-002 and T6.1 gives RW-AGENCYMG CRUDA, while the legacy permission table names right U for the same area and lists "21 more" holders of R and "5 more" of U without naming them; the matrix is not widened and the difference is recorded (GAP-3112; ASM-5384). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated and not built.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-008 | partner_instruction (S9, `rwb_partner`) | id | Read and write, the reference of the replaced row and of the replacement the answer returns |
| DF-PRT-009 | partner_instruction (S9) | case_id | Read, the case of the placement; an identifier of P3's fact and not a foreign key |
| DF-PRT-010 | partner_instruction (S9) | partner_id | Read, the partner being replaced; written on the replacement with the partner chosen |
| DF-PRT-011 | partner_instruction (S9) | instruction_type | Read and write, over LOV-INSTRUCTION |
| DF-PRT-012 | partner_instruction (S9) | instructed_at | Write, the time of the replacement |
| DF-PRT-013 | partner_instruction (S9) | due_at | Read and write, the due date carried to the replacement |
| DF-PRT-014 | partner_instruction (S9) | status | Write, `RECALLED` on the replaced row and `SENT` on the replacement, over LOV-INSTR-STATUS |
| DF-PRT-015, DF-PRT-016 | partner_instruction (S9) | result_code, fee_amount | Not touched: the result and the fee belong to the result and fee steps |
| DF-PRT-001 to DF-PRT-007 | partner (S9) | partner_code, partner_name, partner_type, panel_status, contract_end, score | Read, the partner being replaced and the partner chosen, over LOV-PARTNER-TYPE and LOV-PANEL |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7) | decision_code, rule_id, rule_version, final_call, override_reason, approver_user_id, decided_at | Written as a decision record through the local library (DP-03); the ledger row is appended by rwb-decision from `rwb.decision-record.v1`, never by this service |
| DF-WRK-009 to DF-WRK-016 | assignment (P3) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | Not read and not written: the officer assignment is P3's and the override changes no officer |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Read through the rule-row contract at its version in force; never joined and never written |

The field-level types, lengths and lists are those of TSD S9 T3.0, T3.1 and T3.2; this story adds **no new table, no new column and no migration**, and the legacy `assignment` row is named only to say that it is not touched. The reason's column, list and value format are Not specified in the source documents (GAP-3112; ASM-5381).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). This story supplies the override branch of the instruction operation, whose shape RWB-S9-E6032-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/instructions` (API-S9-002) | `InstructionRequest` in with the instruction type, the partner and the due date plus the additive optional `overrideReason`, `PartnerInstruction` out with the new reference, the partner and the status | Partner portal, right C, scope applied | `Idempotency-Key` header |

The errors are 401, 403 with MSG-P4-002, 404 for a case or a partner that is not there, 409 for an instruction that is not open, 422 with MSG-GEN-001 for an absent partner, an absent reason or a value outside its list, and 503 when the library or the rule-row read does not answer. TSD S9 T-A.1 and T-A.2 publish the operation, its request, its answer, its access and the error set, and the API Specification v5 publishes `InstructionRequest`, `PartnerInstruction` and `DecisionLogEntry.overrideReason`; the override branch, the `overrideReason` property and the decision code carry the placeholder (GAP-3112; ASM-5380, ASM-5382). The acceptance, the result and the invoice operations of the same base belong to other stories of the module and none of them is built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The rule row in force (operation name Not specified in the source documents (GAP-3112; ASM-5382)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule ID and the rule version of the placement rule, read once per override; faked |

The row is one hop with a 2 s timeout and a breaker (ADR-020). It is a contract dependency of class C that the plan's C row does not carry, because the rule version the legacy criterion names has no other published source; DP-04 is not in this key's pattern set, so no Drools kit is embedded and the version is read as data (GAP-3112; ASM-5382).

#### 12.3 Events published

None. The service owns the topic `rwb.partner.events.v1` with its retry and `.dlt` topics (DP-14), and its event set carries EV-20 `InstructionIssued` (`instructionId`, `partnerId`, `type`, `dueOn`, consumed by the partner portal) and EV-21 `PartnerResultSubmitted` (`instructionId`, `result`, `documents`) (Event and Messaging Design v5; context pack events EV-20 and EV-21). EV-20 belongs to the step that first issues the instruction and EV-21 arrives from the portal, so an override that re-places an instruction announces nothing of its own here; the outbox and inbox library that would relay it is the DP-09 dependency this key's pattern set does not hold, and a build that publishes an event from this step fails the absence test (GAP-3112; ASM-5383).

#### 12.4 Events consumed

None. EV-21 `PartnerResultSubmitted` is the result step's trigger and EV-20 is published, not consumed; this step is triggered by the manager's confirmation on SCR-35, and the FSD declares no background event for the feature (FSD S9 A2.4.4.4). The story therefore holds no consumer group, no subscription of its own and no inbox row. TSD S9 T5.3 lists both events as Published while the Event and Messaging Design v5 gives EV-21 the direction Consumed; the conflict is recorded and no direction is declared here (GAP-3112; ASM-5383).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction, can start at any time on a case, continues-as-new with the case stage | `rwb-partner` in namespace `rwb-recovery` | Input: the case reference, the instruction reference and the rule version; signals: the override request, the acceptance and the result; outcome for the parent: the instruction status |
| `recordPlacementOverride` | Activity, the one override step of the instruction | `rwb-partner` | The case, the instruction, the chosen partner and the reason in; the new instruction reference, the status and the record reference out, with the record written before the rows |
| the stage outcome for the parent | Parent-child workflow edge to `CaseWorkflow` | `rwb-case` | The instruction status as the stage result; no REST row is declared for the case move |

The parent is `CaseWorkflow` on task queue `rwb-case`, which hosts the stage and owns the clock and the route; the stage outcome travels on the parent-child edge and never on a REST call (context pack ownership rows, workflow `InstructionWorkflow`). The activity name is a target design choice fixed by no source document, and no activity is registered by this story.

#### 12.6 Schedules

None. The override is a manager-driven step; this story declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The context pack's ownership rows give this service no job (Jobs: 0), and nothing of the panel review, the monthly scorecard or the recall timers is built or declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| partner_instruction | S9 (`rwb_partner`) | The placement of work with a partner on a case; this story writes `partner_id`, `instruction_type`, `instructed_at`, `due_at`, `status` and the audit columns on the replacement and `status` on the replaced row |
| partner | S9 (`rwb_partner`) | The outside firm; read for the panel status, the type and the score, never written here |
| decision_record | PLT library, created in `rwb_partner` | The local hash-linked decision record of the override (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of the published operation and the answer it holds |
| outbox_event | PLT library, created in `rwb_partner` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `assignment` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01). `partner_user` belongs to this service and to the portal sign-in story, not to this one.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision rule-row fake | The placement rule row at its version in force, with its rule ID and the panel condition | AC2, step 7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-35 answer for the placements of `RW-2026-000512` and the SCR-34 partner list, before and after the override | step 2, step 10 |

The fakes are test-only and are replaced by the real services in SIT. The operation name of the rule-row read carries the placeholder until its owner confirms it (GAP-3112; ASM-5382).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed | The override branch of `/api/recovery/partner/v1/cases/{caseId}/instructions`; the rule row of rwb-decision; one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 belong to the issue and result steps; the decision record travels on `rwb.decision-record.v1` as a library fact, not an event of this service (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `InstructionWorkflow` and `recordPlacementOverride` on `rwb-partner`; the stage outcome returns to `CaseWorkflow` on `rwb-case`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `placement`; front end `src/modules/recovery/partner/PlacementAllocation.tsx`, the fragment SCR-35 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the two rows commit together or not at all. DP-13 moves the base of the legacy `/api/recovery/v1` path and gives the instruction operation its home. DP-19 is how SCR-35 and SCR-34 reach this service, one hop through the gateway. These three are the whole pattern set of the key: DP-04 (the embedded Drools kit) is not taken because the rule version is read as data, DP-07 (the reference-data contract of rwb-case) is not taken because the lists are published values of TSD S9 T3.2 and the panel is this service's own row, DP-08 (the access guard) is a template capability, and DP-09 (the outbox library) is needed only by the step that publishes the event; each absence is recorded in the registers instead of the metadata table (GAP-3112; ASM-5382, ASM-5383).

**Dependencies the tables add and the plan does not hold.** The rule-row read is a class C dependency in fact and the plan's C row is None, so the story builds against its document and fake on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the version is read as data, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed only by the step that publishes. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `InstructionWorkflow` override branch | Workflow | Receives the override request as a signal, reads the rule row, reports the new instruction status to the parent |
| `recordPlacementOverride` | Activity | Reads the placement, the partner and the rule row, writes the record and the two rows and answers |
| `PlacementRuleReader` | Service | Reads the rule row in force over the rwb-decision contract and holds its rule ID and version; decides nothing |
| `PlacementDecisionRecordWriter` | Library adapter | Writes the record with the reason as `overrideReason` before anything else, hash-linked; refuses the step when the write fails |
| `PartnerInstructionController` | Controller | The override branch of the instruction operation, the capability area and right C, the scope, the `Idempotency-Key` and the problem mapping |

**Deliverables and build steps.** The override branch of the controller, the workflow step and its activity, the rule reader, the record writer, the two-row transaction, the SCR-35 action and the component, contract and access tests.

**Done when.** AC2 passes on the decision-record stub, the two rows commit or roll back together, the record carries the rule ID, the version and the reason, the panel refusal and the closed-placement refusal are proved, and the boundary test shows no `v_ace_*`, `recovery_case` or foreign-schema statement.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the request is absent or invalid: the partner, the instruction type, the due date or the reason | Enter {field}. |
| MSG-P4-002 | The role lacks the partner-portal right C the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the placement changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are those the legacy story and FSD S9 A2.4.3.1 give, copied unchanged; no message is reworded and no new one is added. The panel and closed-placement refusals reuse MSG-GEN-001 because no source gives the feature a message of its own (GAP-3112).

### 15. Screens and states

| Screen | States | Use here |
|---|---|---|
| SCR-35 Placement and allocation | Loading; list | The placements of the case with their partner, type, due date and status, and the override action on the selected placement |
| SCR-34 Partner list | Loading; list | The partner choice, with code, name, type, panel status and score, read through the same composite route |

Both screens reach this service through the gateway-bff composite route (DP-19); the route calls rwb-partner for the placements and the partners and rwb-case for the case header, and this story fixes the rwb-partner answers only. A source gives neither screen an override state: both are described as "Loading; list" and the legacy story names no form, so the action is placed on SCR-35 in its list state and the dialog's field list carries the placeholder (GAP-3112; ASM-5385). The refusal, closed-placement, panel, absent-reason and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-032-01 | AC1 of the legacy story, owned by RWB-ITG-E6032-ITG; the component half here | Component | The open placement `PI-000241` of `RW-2026-000512` and the panel partner `AG-021` on the fake; the replacement, the recall and the record with the rule version |
| TC-E6-032-02 | AC2 | Component | The decision-record stub stopped; the placement and the partner are unchanged and the caller sees MSG-P7-003 |
| TC-E6-032-03 | Access | Component | A role without partner-portal right C and a malformed request; the 403 with MSG-P4-002 and the 422 of the envelope |
| TC-E6-032-04 | Principle 5 | Component | A forced decision-record write failure; the action stops with MSG-P7-003 and no row changes |

The four legacy cases are those of RWB-E6-032 in their legacy order, kept by ID; their Data keeps the legacy intent on synthetic identifiers, and the business outcome of the first is proved end to end by RWB-ITG-E6032-ITG, which owns AC1. No `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: the partner types, panel states, instruction types, instruction statuses, the metric target, the rule ID and version and the right stay reference data and rule rows, read with their version, never a constant or a branch of the code.
- No personal data in a row, a record, a log or a workflow input: identifiers, codes, dates, a list value, a rule ID, a rule version and a reason text only, and every example is synthetic.
- The case stays with rwb-case: no `recovery_case` read or write, no case state, no route and no clock, and no REST call to rwb-case from this step.
- The officer assignment stays with rwb-case: `assignment` is neither read nor written, and an override of the partner changes no officer.
- The ledger stays with rwb-decision: this service writes its own decision record and never the `decision_log_entry` table or a rule row.
- One base, one topic, one queue, one schema and one login per service; a build that names another service's base, topic or schema as its own fails the review (DP-13, DP-14).
- ACE data only through the owner's contract or a `v_ace_*` view, and this service holds neither grant (DP-05 prohibition).
- No event of this step: a build that publishes EV-20 here, adds a producer group or writes an outbox row fails the absence test until the pattern set carries DP-09 (ASM-5383).

### 18. Traceability

| Requirement ID | Requirement (short) | Element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-PRM-04 | The requirement this feature serves is Not specified in the source documents (GAP-3112; ASM-5387): TSD S9 T8 maps REQ-S9-001 to REQ-S9-004 and REQ-S9-008 to FEAT-PRM-01 and REQ-S9-005 to REQ-S9-007 and REQ-S9-009 to FEAT-PRM-08 | The override branch of API-S9-002, the two instruction rows and the decision record | TC-E6-032-01, TC-E6-032-02 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-E6-032-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The rule-row read with its budget and breaker | TC-E6-032-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the change, with `overrideReason` | TC-E6-032-02, TC-E6-032-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-032, disposition Split (rework); feature FEAT-PRM-04; module S9 Partner management |
| Legacy criteria | AC2 of the legacy story, owned word for word by this story; AC1 is owned by RWB-ITG-E6032-ITG |
| Source text | Legacy RWB-E6-032; FSD S9 Partner management v3 A1.2, A1.3, A2.4, A2.4.2, A2.4.3.1 and A2.4.4; TSD S9 Partner management v2 T1, T2, T3.0 to T3.3, T5.2, T5.3, T6.1, T6.2, T8, T-A.1 and T-A.2; API Specification v5 elements `InstructionRequest`, `PartnerInstruction` and `DecisionLogEntry`; Business Rules and Routing Logic v4 rows R-LIT-29, R-DIS-31, R-WO-35 and R-UNI-45; Event and Messaging Design v5 EV-20 and EV-21; Epics 3 to 8 Specification v3 row FEAT-PRM-04 |
| Test cases | The four legacy cases TC-E6-032-01 to -04, kept by ID |
| Feature and screens | FEAT-PRM-04; SCR-35 Placement and allocation, SCR-34 Partner list |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the elements, the `overrideReason` property, the rights of the document and the fakes: RWB-S9-E6032-CON.
- The scorecard placement the override departs from, and its rule: FEAT-PRM-03 and RWB-S9-E6031-APP.
- The partner panel, the fee schedule and the contract terms: FEAT-PRM-02 and RWB-S9-E6030-APP. The onboarding of a partner: FEAT-PRM-01 and RWB-S9-E6029-APP.
- The result, the acceptance and the invoice of an instruction: FEAT-PRM-05, RWB-S9-E6033-APP and the fee stories of the module.
- The recall and re-selection rules R-UNI-25 to R-UNI-29, the notice on a missed target and the end of a contract: the partner-management stories of EP07.
- The case of record, its stage, its route, its clock and the officer assignment: rwb-case (P3).
- The rule row, the rule version and the ledger: rwb-decision (P7), whose row this story reads and never writes.
- The reason's field ID and value format, the decision code and the instruction status transitions: the business lead and the rule owner confirm them, and the placeholders stand until then (GAP-3112; ASM-5379, ASM-5381, ASM-5382).
- The gateway-bff composite route and the screen field lists of SCR-35 and SCR-34: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
