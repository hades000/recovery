# RWB-S2-E3014-APP Unlock the asset as a non performing asset by rule

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-014 for rwb-treatment (S2). The auto-unlock leaves the monolith's S2 service in the one `recovery` schema and becomes the unlock step of the deed-in-lieu stage of `TreatmentWorkflow` on this service's own task queue, evaluating R-DIL-22 and R-DIL-23 with the DEEDINLIEU package in force and reporting the target state to the parent `CaseWorkflow`; the unlock facts are written on the treatment row in the same `rwb_treatment` transaction as the local decision record through the RWB-PLT-E1027-CON library (DP-03); the ACE NPA-asset facts arrive as facts and no `v_ace_*` view is read (DP-05); the base is `/api/recovery/treatment/v1` (DP-13) and SCR-14 and SCR-16 are reached through the gateway-bff composite route (DP-19). The four legacy acceptance criteria are copied verbatim with one contract mock line added to AC1, AC2 and AC3. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3014-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-Y |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3014-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the unlock step of the deed-in-lieu stage of `TreatmentWorkflow` on task queue `rwb-treatment` — the inspection-completed trigger evaluated against R-DIL-22, the auto-unlock answer derived by R-DIL-23 with the rule ID and the package version in force, the answer and the NPA asset reference written on the treatment row of `rwb_treatment`, the local decision record written in the same transaction, and the target state reported to the parent `CaseWorkflow` that owns and moves the case status**, so that **about 95% of qualified cases release the asset for transfer with no person in the path, the asset reaches the asset list of rwb-asset through FEAT-AST-02, and every release is provable with the rule and the version that made it**.

This is the application slice of legacy RWB-E3-014. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and R-DIL-22 and R-DIL-23, the messages, the screens and the data rows they depend on;
- `runAssetUnlockRule`, the unlock step of the deed-in-lieu stage of `TreatmentWorkflow` (DP-12), on this service's own queue `rwb-treatment` in namespace `rwb-recovery`, with the `recordAndApply` activity beside it;
- the treatment columns that hold the unlock facts — `inspectionOutcome`, `unlockDecision`, `unlockDecidedAt` and `assetRef` — in schema `rwb_treatment` (GAP-2676; ASM-4399);
- the local decision record of the unlock, written through RWB-PLT-E1027-CON inside the caller's transaction, with the rule ID, the package version and decision code D6.4 (DP-03);
- the outcome report of the unlock to the parent `CaseWorkflow`: the case status the rule implies — ASSET_UNLOCK_DECISION, or AWAITING_TRANSFER on the pass — handed to the parent, which moves it; this service writes no case table (DP-01);
- the asset-unlock element as the service side of SCR-16 and SCR-14, composed by the gateway-bff composite route (DP-19).

It does not own: the published element set of the unlock, the value rules, the no-new-table rule, the decision-record group, the compatibility rule and the fakes, which are RWB-S2-E3014-CON; the treatment record and its creation, which are RWB-S2-E3001-APP; the deed-in-lieu stage chain — the offer, the inspection capture, the transfer, the approver summary of R-DIL-24 to R-DIL-26 and the AMIS, ALS and registration requests — which are RWB-S2-E3012-APP; the asset record and the asset list, which are rwb-asset (S5) and FEAT-AST-02; the case status, the case task and the case signal, which are rwb-case's (P3); the DEEDINLIEU package and the central ledger, which are rwb-decision's (P7); the roles, rights and scope data, which are rwb-access's (P4); the composite route, the screen field list and the layout, which are the platform edge story's and the screen owners'.

### 2. Business rationale

A deed in lieu only pays off if the asset stops being security and becomes stock the bank can sell. Today the step between the completed inspection and the transfer is a person: an officer reads the checklist, the photographs and the bills, judges whether the asset may be released, and writes the case forward by hand (FSD S2 A2.14.1; Business Rules and Routing Logic v4 R-DIL-22 and R-DIL-23). FEAT-TRT-14 asks for that judgement to be a rule, with the cases that qualify released with no person in the path and the rest left to the approver; the restructure-and-deed-in-lieu turnaround target of 5 days is measured from the decision log and the Workbench records, and the unlock is the step that keeps it in days.

The monolith answered it inside one process: the S2 service moved `recovery_case.status` itself, read `v_ace_npa_asset` from the `recovery` schema, wrote `decision_log_entry` in the same schema and set the treatment row in the same transaction. In the 19-service target each of those facts has a different owner. The case status is rwb-case's and reaches the step on the case signal the parent forwards (ASM-4401). The decision record is the platform library's, written locally in this service's schema (DP-03). The NPA-asset facts are rwb-source-data's, and the connection matrix gives rwb-treatment no link to rwb-source-data, so they arrive as facts on the case signal and no `v_ace_*` view is read here (DP-05; ASM-4402). The asset list itself is rwb-asset's: FEAT-AST-02 links the case to the property in `v_ace_npa_asset` by `asset_key` when the deed-in-lieu transfer completes, and it depends on this feature (ASM-4401).

What the business keeps is the rule, not the code. R-DIL-22 runs the unlock rule when the checklist, the photographs and the bills are captured and the case is in WITH_FIELD_INSPECTION; R-DIL-23 releases the asset for transfer when the unlock rule passes, which it does in about 95% of cases, and the case is in ASSET_UNLOCK_DECISION. The state names, the trigger event names, the decision code D6.4 and the thresholds are values in force of their owners, never constants (BR-S2-014).

The legacy key divides and the division is fixed. This story owns the unlock rule and its record; the stage that carries the offer, the inspection capture and the transfer is RWB-S2-E3012-APP, and the two build independently against RWB-S2-E3014-CON and RWB-S2-E3012-CON with no build dependency between them. The cross-service proof is the wave 2 harness. Serves REQ-S2-007, and no business value moves into code.

### 3. Preconditions

- RWB-S2-E3014-CON is published: the `AssetUnlock` element (`inspectionOutcome`, `unlockDecision`, `unlockDecidedAt`, `assetRef`), its value rules with the event codes of R-DIL-22 and R-DIL-23, the decision-record group, the no-new-table rule, the compatibility rule and the fakes (H).
- RWB-PLT-E1027-CON is published (DP-03): `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003, and the `decision_record` DDL template applied in this service's own schema.
- RWB-PLT-N001-CON is published (DP-19): the gateway-bff composite route that carries SCR-14 and SCR-16, one hop each, read only.
- RWB-S2-E3001-APP is done: `treatment` exists in schema `rwb_treatment` with DF-TRT-001 to DF-TRT-033, and the service's own Flyway sequence is the only place a column is added (DP-15).
- The case is a deed-in-lieu case that has passed the field inspection: the parent `CaseWorkflow` of rwb-case forwards the case signal to the running treatment stage, and the inspection capture is carried as a fact of that signal (ASM-4401).
- Package DEEDINLIEU is in force for the business date with rows R-DIL-22 and R-DIL-23, each carrying its from-state, its event code, its condition, its action text and its timer spec; the package and its version arrive from rwb-decision on `rwb.decision.RulePackageInForce.v1` and are evaluated by the embedded Drools runtime of the service template (ASM-4403).
- The workflow kit, the outbox and inbox library and the guard library are service-template capabilities, so the stage, the activities, the timers and the outbox add no build dependency of their own (ASM-4403).
- The NPA-asset facts of the case — `asset_ref`, `asset_key`, `asset_code`, `transfer_in_type`, `from_segment` and `book_value` of DF-ACE-208 to DF-ACE-219 — are on the case signal; this service reads no ACE view and holds no copy (DP-05; ASM-4402).
- The lists LOV-TREATMENT, LOV-TRT-OUTCOME and the event codes of the DEEDINLIEU set are values in force read with their version; no member of any list and no threshold is written in code (BR-S2-014).
- The case status of a case is readable only as the case signal the parent forwards; this service reads no case row and holds no case table (DP-01; ASM-4401).
- No approval is needed to build against a Draft contract baseline, and every build dependency is a CON story: this story starts on Day 1 (§R5.7).

### 4. Flow

1. The parent `CaseWorkflow` on rwb-case forwards the case signal to the running `TreatmentWorkflow` child on `rwb-treatment`; the signal carries the case status, the product, the treatment ID, the inspection capture and the NPA-asset facts, and the status stays rwb-case's (ASM-4401).
2. The stage holds a treatment of type DEED_IN_LIEU in WITH_FIELD_INSPECTION with the checklist, the photographs and the bills captured (FSD S2 A2.14.3.1 R-DIL-22).
3. The stage asks the embedded Drools runtime for the DEEDINLIEU package version in force and evaluates R-DIL-22 against the case facts: the from-state, the event INSPECTION_COMPLETED and the condition that the checklist, the photographs and the bills are captured.
4. R-DIL-22 fires: `runAssetUnlockRule` takes the inspection facts and calls the unlock rule, and the treatment takes `inspectionOutcome`; the rule reports the target state ASSET_UNLOCK_DECISION to the parent, which moves the case status.
5. R-DIL-23 is evaluated on the same facts: the unlock condition of the package is tested against the NPA-asset facts of the signal, and the answer is AUTO_UNLOCK_PASSED for the cases that qualify, about 95% of them (FSD S2 A2.14.3.1; Business Rules and Routing Logic v4 R-DIL-23).
6. `recordAndApply`, one `rwb_treatment` transaction: the treatment row takes `inspectionOutcome`, `unlockDecision` (the answer as the event code the package returned), `unlockDecidedAt` and `assetRef` (the NPA asset reference the release names), and the `decision_record` row is written through `DecisionRecordWriter.record` with decision code D6.4, the rule ID and the package version (DP-03).
7. The step reports the outcome to the parent `CaseWorkflow`: on a pass, the target state AWAITING_TRANSFER; this service writes nothing to a case table, and the parent moves the status.
8. On the pass the asset is released for transfer: rwb-asset links the case to the property by `asset_key` under FEAT-AST-02 when the deed-in-lieu transfer completes, and the property moves to the asset list; this service publishes no event for the release (ASM-4401).
9. On a fail the case is left to the approver path of RWB-S2-E3012-APP (R-DIL-24 to R-DIL-26); this story records the answer and reports it, and writes no approver task.
10. A redelivered case signal answers the open step and starts no second evaluation: the workflow ID and the idempotency of the record carry the dedupe, and a replayed workflow reuses the recorded signal.
11. SCR-16 reads the unlock answer, the inspection outcome and the asset reference through the gateway-bff composite route, which composes the case read of rwb-case and this service's treatment read in one hop each (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without Treatment and offer R reads the unlock answer | 403 from the guard library; the refusal is logged with the role and the operation, never a personal field | MSG-P4-002 | AC1, TC-E3-014-05 |
| X2 | The local decision record cannot be written | The transaction rolls back: no treatment column, no outbox row, no outcome report to the parent; the user sees MSG-P7-003 and the call is retried | MSG-P7-003 | AC4, TC-E3-014-06 |
| X3 | The record is refused for a missing or invalid field | The transaction rolls back and the field is named in the service log and the incident | MSG-P7-009 | AC4 |
| X4 | The inspection capture is incomplete — a checklist line, a photograph or a bill is missing | No rule fires; the stage holds the case at WITH_FIELD_INSPECTION and names the missing item | MSG-GEN-001 | AC2 |
| X5 | No DEEDINLIEU version is in force for the business date | The step ends with the package refusal it received, reports no target state and writes nothing; the case keeps its status | MSG-P7-003 | AC2, AC3 |
| X6 | The case signal names a state or an event no row of the package expects | No rule fires, nothing is written and the stage waits on the next signal | None | AC2, AC3 |
| X7 | The NPA-asset facts are absent from the signal, or two assets answer the same case | The unlock is not evaluated, the missing fact is named to the parent, and no asset is released on a partial answer | None | AC1, AC2 |
| X8 | The record is written and the outcome report to the parent fails | The step retries on the kit's policy; the treatment and the record are already committed, so the retry reports the same answer and writes no second record | None | AC1, AC3 |

X1 to X4 are the paths of the legacy story carried onto the split; X5 to X8 are the refusal, unmatched-signal, missing-fact and report-retry paths the workflow model adds. A refusal under X1 writes nothing at all, because the guard runs before the transaction opens, and the "nothing changes" of AC4 is the rollback of one transaction that also holds the treatment columns and the outbox row (DP-03).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-S2-E3014-CON fake, the decision-record fake and the composite-route fake; needs no live rwb-case, rwb-decision, rwb-asset or ACE view |
| Negotiable | The activity names, the column names, the workflow ID derivation and the flag name are this story's choice; the rules, the states, the event codes, the lists and the messages are fixed |
| Valuable | About 95% of qualified cases release the asset for transfer with no person, in days, with the rule and the version recorded |
| Estimable | One unlock step, two activities, four treatment columns, one library adapter and one migration |
| Small | Fits two weeks with its tests |
| Testable | Each criterion of section 7 is one automated test; the parent, the package, the guard and the asset owner are stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Unlock the asset as a non performing asset by rule

  Scenario: AC1 Unlock the asset as a non performing asset by rule (legacy RWB-E3-014 AC1)
    Given the rwb-case contract mock returns the completed inspection and the NPA asset facts of the case
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then applies the auto-unlock rule so the asset moves to the asset list without a person for the cases that qualify
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIL-22 (legacy RWB-E3-014 AC2)
    Given the rwb-case contract mock returns case status WITH_FIELD_INSPECTION
    Given a case in state WITH_FIELD_INSPECTION
    When inspection completed
    Then run the asset unlock rule
    Then the case moves to ASSET_UNLOCK_DECISION

  Scenario: AC3 Rule R-DIL-23 (legacy RWB-E3-014 AC3)
    Given the rwb-case contract mock returns case status ASSET_UNLOCK_DECISION
    Given a case in state ASSET_UNLOCK_DECISION
    When auto unlock passed
    Then release the asset for transfer
    Then the case moves to AWAITING_TRANSFER

  Scenario: AC4 Not recorded (legacy RWB-E3-014 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line is kept character for character, including the legacy repetition of `Then`; what changes is who produces each fact and where it is asserted. The trigger of AC1 is no longer a monolith request but the start of the unlock step inside `TreatmentWorkflow` on task queue `rwb-treatment`, the child of `CaseWorkflow` (DP-12), and "the data and the rule version this feature needs are in place" is the DEEDINLIEU package version announced on `rwb.decision.RulePackageInForce.v1` together with the list and threshold values in force (ASM-4403). "The system writes the result to the decision log with the rule version" is the local `decision_record` row written in the same `rwb_treatment` transaction through the RWB-PLT-E1027-CON library, with decision code D6.4, and published to the central ledger of P7 (DP-03; ASM-4399). In AC2 and AC3 the state is the case's, so each line that names a case state is asserted against the parent `CaseWorkflow` of rwb-case, which the added `Given the rwb-case contract mock returns case status ...` line stands in for; this service holds no case table and no status column (DP-01; ASM-4401). "So the asset moves to the asset list" of AC1 is rwb-asset's FEAT-AST-02, which links the case to the property in `v_ace_npa_asset` by `asset_key` when the deed-in-lieu transfer completes; the NPA-asset facts the rule tests arrive from the same signal, and no `v_ace_*` view is read here (DP-05; ASM-4401; ASM-4402). "Release the asset for transfer" of AC3 is the AUTO_UNLOCK_PASSED answer recorded on the treatment, and the transfer itself is RWB-S2-E3012-APP's. The decision-log failure of AC4 is the library's MSG-P7-003, and the "nothing changes" is the rollback of one transaction that also holds the treatment columns and the outbox row (DP-03). SCR-16 and SCR-14 reach the answer on base `/api/recovery/treatment/v1` through the gateway-bff composite route (DP-13; DP-19).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The unlock rule runs when the checklist, the photographs and the bills are captured on a case in WITH_FIELD_INSPECTION; its target state is ASSET_UNLOCK_DECISION | R-DIL-22; FSD S2 A2.14.3.1 |
| BR2 | The asset is released for transfer when the unlock rule passes, which it does in about 95% of cases, and the target state is AWAITING_TRANSFER | R-DIL-23; FSD S2 A2.14.3.1 |
| BR3 | A failed unlock is not part of this story: it goes to the approver summary of the deed-in-lieu stage with a three-working-day clock | R-DIL-24; FSD S2 A2.14.3.1; ASM-4404 |
| BR4 | The result is written to the decision record with decision code D6.4, the rule ID and the rule version the evaluated package returned | legacy RWB-E3-014 AC1; DP-03; TSD S2 T4 |
| BR5 | A decision that cannot be recorded does not proceed: the treatment columns, the record and the outbox row are one transaction, and the user sees MSG-P7-003 | Principle 5; legacy RWB-E3-014 AC4 |
| BR6 | The case status stays rwb-case's: the step reports its outcome to the parent `CaseWorkflow`, which moves the status, and this service writes no case table | DP-01; ASM-4401 |
| BR7 | The asset list, the AMIS record and the transfer stay rwb-asset's and rwb-integration's: this story releases the asset for transfer and links nothing | FSD S2 A2.14.1; FEAT-AST-02; ASM-4401 |
| BR8 | No ACE view is read and no asset fact is copied: the NPA-asset facts arrive on the case signal, and `rwb_treatment` holds only the reference the release names | DP-05; ASM-4402 |
| BR9 | No value a business person may change is written in code: the states, the event codes, the decision code, the lists and the thresholds are values in force read with their version | BR-S2-014; FSD S2 A2.14.3.1 |
| BR10 | The right is declared and not re-implemented: the answer is read on Treatment and offer R, and the guard library answers | TSD S2 T6.1; DP-08 |

**Where each rule lives in the target.** BR1 and BR2 are `runAssetUnlockRule` and the R-DIL-22 and R-DIL-23 rows of the evaluated package. BR3 is the sibling stage's approver path, named here only to fix the boundary. BR4 and BR5 are `recordAndApply` and the library. BR6 is the child-workflow return and the parent. BR7 and BR8 are the signal contract and the absence of any ACE statement in this service. BR9 is the reference-data reads and the Drools runtime. BR10 is the contract's declared right and the guard, and no check is written in this service.

### 9. State transitions

None of the transitions below is a case status owned here: each row is the outcome this step reports, and the status itself is moved by the parent `CaseWorkflow` on rwb-case (ASM-4401; DP-01).

| From (case status on the signal) | Event | Condition | Reported target state |
|---|---|---|---|
| WITH_FIELD_INSPECTION | INSPECTION_COMPLETED | R-DIL-22: checklist, photographs and bills captured | ASSET_UNLOCK_DECISION |
| ASSET_UNLOCK_DECISION | AUTO_UNLOCK_PASSED | R-DIL-23: the unlock rule passes, about 95% of cases | AWAITING_TRANSFER |
| ASSET_UNLOCK_DECISION | AUTO_UNLOCK_FAILED | R-DIL-24: the unlock rule fails | AWAITING_APPROVER_SUMMARY, by RWB-S2-E3012-APP's approver path |
| AWAITING_APPROVER_SUMMARY | APPROVER_RELEASED, APPROVER_REFUSED | R-DIL-25, R-DIL-26 | AWAITING_TRANSFER or RETURNED_TO_ROUTE_DIL, by the sibling |
| WITH_FIELD_INSPECTION | no rule fired | A capture item is missing | None reported; the case stays and the missing item is named |
| any of the above | no rule fired | The signal names a state or an event no row expects | None reported; the stage waits |

The treatment row has its own lifecycle in the `state` column — Draft, submitted, approved, booked and broken are the names SCR-14 shows — and this story writes no state of its own beyond the unlock columns. The step execution itself is RUNNING, COMPLETED or FAILED in the workflow history, and a failed execution is retried on the platform policy, 1 s initial interval with back-off 2 and 10 attempts, with the package refusal non-retryable.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE), service identity of `rwb_treatment` | Runs the unlock step, writes the treatment columns, the decision record and the outbox row |
| Sale officer | The primary role of FEAT-TRT-14: reads the unlock answer, the inspection outcome and the asset reference on SCR-16; the rule itself runs unattended |
| RW-RESTRUCT, restructuring officer (FCR) | Also uses the feature per FSD S2 A2.14.3.3; holds CRUA in "Treatment and offer" |
| RW-CASEOWN, RW-TEAMMGR, RW-SPECIAL, RW-GUARANT, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and the other reading roles of TSD S2 T6.1 | Read the treatment and its unlock answer under right R, scope applied |
| RW-PRODHEAD, RW-CREDCOMM | Hold RA and answer the below-floor and unlock approvals that the sibling stage routes; this story routes nothing to them |
| rwb-case (P3) | Owns `CaseWorkflow`, the case status, the case task and the case signal; moves the status this step reports |
| rwb-decision (P7) | Owns the DEEDINLIEU package, its rows, its version and the central ledger |
| rwb-asset (S5), rwb-integration (P2) | Own the asset record, the asset list, FEAT-AST-02, AMIS and the transfer |
| rwb-source-data (P1) | Owns the ACE NPA-asset read that reaches this step as facts |
| No delegation of authority level applies | The story evaluates a rule and records it; it approves nothing |

No credential and no personal name appears in the request, the row, the workflow input, the record or the logs. Where a person must be named the row carries the user identifier, never a name, and the masking of the personal fields of the case is the platform edge's.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read: DEED_IN_LIEU on this path |
| DF-TRT-005 | treatment | proposed_by | Read |
| DF-TRT-006 | treatment | proposed_at | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-014 | treatment | outcome_at | Read |
| (no field ID) | treatment | `inspectionOutcome`, `unlockDecision`, `unlockDecidedAt`, `assetRef` | Write: the unlock facts, the name of no TSD field (GAP-2676; ASM-4399) |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, in `rwb_treatment`) | all fields through `DecisionRecordWriter.record` | Write, in the same transaction (DP-03) |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset (`rwb_source_data`'s read) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and the rest | Read as facts on the case signal, never from the view (DP-05) |
| DF-CAS-001 to DF-CAS-023; DF-WRK-009 to DF-WRK-016 | recovery_case, assignment (`rwb_case`, owner P3) | the case and its status, the assignment | Not read and not written: the status and the facts arrive on the case signal (ASM-4401) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (`rwb_decision`, owner P7) | the central ledger entry | Not written and not read here: P7 seals it from the shared topic (DP-03) |
| DF-REF-001 to DF-REF-015 | rule_row (`rwb_decision`, owner P7) | the rows of R-DIL-22 and R-DIL-23 | Not read directly: the evaluated package returns the row outputs |

`treatment` is this service's table and the only one this story writes, together with the library's `decision_record` and the outbox in the same schema (DP-01; DP-03). The four unlock columns carry no field ID and no TSD definition, because TSD S2 T3.1 stops at DF-TRT-033 and has no inspection, unlock or asset reference: their names and types are the working read of ASM-4399, shared with the sibling deed-in-lieu element set. `assignment`, `recovery_case`, `decision_log_entry`, `rule_row` and `v_ace_npa_asset` belong to rwb-case, rwb-decision and rwb-source-data; the case and asset facts arrive on the signal, and no ACE view is named in a statement of this service (DP-05). Field IDs are those of the Logical Data Model and Data Dictionary; the element names and the holding of them are Not specified in the source documents (GAP-2676; ASM-4399).

### 12. Contract

#### 12.1 REST operations provided

None of its own. Owner rwb-treatment (S2), base `/api/recovery/treatment/v1` (DP-13): the unlock element is a component of the treatment representation that RWB-S2-E3001-CON publishes on `GET /treatments/{treatmentId}` (API-S2-002 of TSD S2 T-A.1), and this story fixes the service side of the answer, not a path. The officer's screen actions on the same treatment are the sibling contracts' (the draft-terms change, the offer and the submit of RWB-S2-E3002-CON, RWB-S2-E3003-CON and RWB-S2-E3004-CON).

| Element this story reads or writes on the treatment | Source | Use |
|---|---|---|
| `inspectionOutcome` | RWB-S2-E3014-CON | The capture fact the R-DIL-22 trigger is proved by; written here |
| `unlockDecision`, `unlockDecidedAt` | RWB-S2-E3014-CON | The rule's answer and its instant; written here |
| `assetRef` | RWB-S2-E3014-CON | The NPA asset reference the release names; written here |
| The treatment reference, the type and the outcome | RWB-S2-E3001-CON | The stage entry and the record of the treatment |

#### 12.2 REST operations consumed

None. The case status, the inspection capture and the NPA-asset facts arrive on the case signal the parent `CaseWorkflow` forwards, which is the only way a case fact reaches this service (ASM-4401; ASM-4402). The asset list, the AMIS record and the transfer are reached through the case signal and their owners' own flows, because route services reach shared capabilities through Temporal and never REST (ASM-4401). The Work Package lists no contract dependency for this story, and none is added.

#### 12.3 Events published

None. The topic of the service is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its one catalogue event, EV-10 `TreatmentApproved`, belongs to the offer release stories of this service (TSD S2 T5.3; context pack S2, Events row). The unlock publishes no event of its own: the release is reported to the parent and rwb-asset links the asset under FEAT-AST-02, and no source names an unlock or release event (GAP-2676; ASM-4401). The `DecisionRecorded` row the library writes inside the transaction is not a type of this story (DP-03).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | Announces the DEEDINLIEU package version in force; the step swaps it in and stamps it on the decision record |
| CaseEvent (EV-29), the case signal | no topic: the case router and the parent `CaseWorkflow` of rwb-case | P3 rwb-case | Carries the case status, the product, the inspection capture and the NPA-asset facts the step evaluates; forwarded to this child by the parent |

The package event is consumed through the inbox of the outbox library, so a redelivery starts no second swap. The case signal is a Temporal signal forwarded by the parent and is not a Kafka subscription of this service; a replayed workflow reuses the recorded signal (ASM-4403).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, stage, case status, treatment ID, inspection capture and NPA-asset facts; output: the unlock outcome of section 9 |
| `runAssetUnlockRule` | Activity | `rwb-treatment` | The inspection facts and the package version in; the R-DIL-22 and R-DIL-23 answers, the rule ID and the decision code D6.4 out |
| `recordAndApply` | Activity | `rwb-treatment` | The treatment columns, the decision record through RWB-PLT-E1027-CON and the outbox row in one transaction |

The package evaluation itself is the embedded Drools runtime's, asked by the activity inside its own step (ASM-4403). The workflow and activity names outside the design's `TreatmentWorkflow` and `RecordAndApply` are a target design choice fixed by no source document (GAP-2676; ASM-4399).

#### 12.6 Schedules

None. The step is signal-started inside `TreatmentWorkflow` and owns no Temporal Schedule and no legacy Quartz job; the deed-in-lieu offer validity, the inspection clock and the three-working-day approver clock of R-DIL-24 are workflow timers of the sibling stage (DP-10).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Updated by `recordAndApply`: `inspectionOutcome`, `unlockDecision`, `unlockDecidedAt` and `assetRef`; no row is inserted here |
| `decision_record` | `rwb_treatment` | PLT (library object, written through RWB-PLT-E1027-CON) | Written in the same transaction as the treatment update (DP-03) |
| `outbox` | `rwb_treatment` | S2, from the service template | Written in the same transaction for the record event of the library |
| `asset` | `rwb_asset` | S5 | Not written and not read: the asset record and the asset list are FEAT-AST-02's |
| `recovery_case`, `assignment` | `rwb_case` | P3 | Not written and not read: the status, the task and the facts arrive on the case signal |
| `v_ace_npa_asset` | ACE view, `rwb_source_data`'s read | P1 | Never named in a statement of this service (DP-05) |

No new table is created for the inspection, the unlock or the release, and no foreign key crosses a schema (DP-01; GAP-2676; ASM-4399). `decision_log_entry` is P7's ledger and is named here only.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3014-CON unlock fake | The four treatment elements and their value rules | A treatment in WITH_FIELD_INSPECTION with a complete capture, one with a missing item, one in ASSET_UNLOCK_DECISION with a pass and one with a fail |
| RWB-PLT-E1027-CON decision-record fake | The record write | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable writer with MSG-P7-003 |
| RWB-PLT-N001-CON gateway route fake | The composite route of SCR-14 and SCR-16 | A granted right R; a refused answer; a scope miss |
| rwb-case case-signal mock | The three added Given lines and the facts of the step | Case status WITH_FIELD_INSPECTION and ASSET_UNLOCK_DECISION on the signal, the inspection capture, the NPA-asset facts and the status the parent reports back |
| DEEDINLIEU package fixture | The evaluated package | Version "DIL-2026.11" with rows R-DIL-22 and R-DIL-23, their conditions and event codes; a version with no row for the state |

The unlock fake is the published contract of RWB-S2-E3014-CON, and the case-signal fixture is test-only: it stands where the parent `CaseWorkflow` and the case of rwb-case would be, and it is recorded with ASM-4401 and ASM-4402.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the element rides the treatment read of a sibling contract | 0 | OpenAPI 3.1; the browser reaches the read through gateway-bff (DP-19) |
| Kafka | 0 | 1 event (`rwb.decision.RulePackageInForce.v1`) | Inbox dedupe by cloud event id; the service's own topic is the sibling stories' |
| Temporal | 1 stage and 2 activities | 0 child workflows | Namespace `rwb-recovery`; one child per case; no Schedule |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `deed-in-lieu` and `treatment`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the unlock answer is a local row written in the caller's transaction | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data read through rwb-source-data's contract or the service's own ACE views; here the NPA-asset facts arrive on the case signal and no view is named | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record of the unlock inside the same transaction; DP-05 is the NPA-asset read that comes to this step as facts, because the connection matrix gives rwb-treatment no call to rwb-source-data and the views are granted to rwb-source-data alone (ASM-4402); DP-13 fixes the base on which the sibling operations answer; DP-19 is the route by which SCR-14 and SCR-16 reach this service. The embedded Drools runtime and the DEEDINLIEU package, the access guard, the outbox and inbox library and the workflow kit are the service template's wave-0 capabilities (ASM-4403).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `runAssetUnlockRule` | Activity | The R-DIL-22 trigger, the R-DIL-23 answer and the rule ID and version out |
| `recordAndApply` | Activity | The four treatment columns, the decision record and the outbox row in one transaction |
| `UnlockHandler` | Handler | The stage entry from the case signal: the inspection capture and the NPA-asset facts mapped onto the step input |
| `UnlockOutcomeReporter` | Service | Builds the outcome of section 9 and returns it to the parent workflow |
| `DecisionRecordAdapter` | Library adapter | Calls `DecisionRecordWriter.record` with decision code D6.4, the rule ID and the package version (DP-03) |
| `TreatmentRepository` | Repository | The update of `treatment` by ID, with the optimistic-lock version of the row |
| `Migrations` | Migration | The four unlock columns on the per-service Flyway sequence, without a cross-schema key |

**Database.** `treatment` already holds DF-TRT-001 to DF-TRT-033. This story adds `inspectionOutcome`, `unlockDecision`, `unlockDecidedAt` and `assetRef` on the service's own migration sequence and creates no table: the inspection and the unlock have none of their own (DP-15; GAP-2676; ASM-4399). The types follow the shape of the values: `inspectionOutcome` jsonb or varchar as the capture returns it, `unlockDecision` varchar(30) carrying the event code the package returned, `unlockDecidedAt` timestamptz and `assetRef` varchar(60); `decision_record` is the library object of RWB-PLT-E1027-CON in the same schema.

**Configuration and reference data.** The from-states, the event codes INSPECTION_COMPLETED, AUTO_UNLOCK_PASSED and AUTO_UNLOCK_FAILED, the decision code D6.4, the 95% expectation and the three-working-day approver clock are values in force of their owners and are read, never set here (BR9). The package version arrives through `rwb.decision.RulePackageInForce.v1`. The capability area and the rights are the guard library's data.

**Build steps**

1. The migration that adds the four unlock columns to `treatment` on the service sequence, with no new table (DP-15).
2. `UnlockHandler` and the step input, with the case signal, the inspection capture and the NPA-asset facts (AC1).
3. `runAssetUnlockRule` against the package fixture, R-DIL-22 and R-DIL-23, with the complete and the incomplete capture and the pass and the fail (AC2, AC3).
4. `recordAndApply` with the four columns, the decision record through the fake and the outbox row, and the rollback on MSG-P7-003 and MSG-P7-009 (AC4).
5. `UnlockOutcomeReporter` and the outcome returned to the parent, with the two mocked case statuses (AC2, AC3).
6. The guard on the treatment read and the rollback test of TC-E3-014-06 (AC1, AC4).
7. Tests for AC1 to AC4 against the fakes and the fixtures.

**Feature flag.** `rwb.treatment.asset-unlock`.

**Done when.** The tests in section 16 pass, a synthetic deed-in-lieu case walks from WITH_FIELD_INSPECTION through ASSET_UNLOCK_DECISION to AWAITING_TRANSFER in SIT with the four columns and one decision record written in one transaction, a failed record leaves the treatment unchanged with MSG-P7-003, an incomplete capture holds the case and names the missing item, and SCR-16 shows the unlock answer, the inspection outcome and the asset reference through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-001 | An offer below the floor is submitted on the deed-in-lieu path | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | The payoff or the figure behind the treatment is older than the freshness limit | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | The offer to the customer carries its end date | The offer to the customer ends on {date}. |
| MSG-GEN-001 | A required field of the inspection capture is missing | Enter {field}. |
| MSG-P4-002 | The role does not hold the right the action needs in "Treatment and offer" | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |

MSG-S2-001, MSG-S2-002, MSG-S2-003, MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are the six legacy texts carried unchanged; MSG-P7-009 comes with the decision-record contract of RWB-PLT-E1027-CON. MSG-S2-001 to MSG-S2-003 are raised by the offer and settlement branches of the sibling stories and are listed because the legacy story carries them. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | States | What this story puts on it |
|---|---|---|
| SCR-16 Deed in lieu | Checks; appraisal; approved; transferred | The inspection outcome, the unlock answer with its instant and the NPA asset reference the release names |
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken | The treatment the unlock was decided on, read only from this story |

Both screens are served by the gateway-bff composite route, which composes the case read of rwb-case with the treatment read of this service, one hop each, read only (DP-19); the browser calls no owner service directly. The screen field list, the composite route specification and the layout belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-014-01 | AC1 | End to end | Unlock the asset as a non performing asset by rule |
| TC-E3-014-02 | AC2 | End to end | Rule R-DIL-22 |
| TC-E3-014-03 | AC3 | End to end | Rule R-DIL-23 |
| TC-E3-014-04 | AC4 | End to end | Not recorded |
| TC-E3-014-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-014-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and the "Access" and "Principle 5" cases to "Component", as in the other stories of this run. Where Covers names `Access`, the criterion is the guard's published answer on the treatment read, and where it names `Principle 5` the criterion is the rollback of the one transaction. The fakes of section 12.8 stand behind every case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these six cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the from-states, the event codes, the decision code, the lists and the 95% expectation are values in force read with their version (BR-S2-014).
- No personal data in logs, tests, workflow inputs or prompts: the step carries case and treatment identifiers, codes, amounts, versions and timestamps only, and the profile codec is on every payload.
- No read of another module's tables and no read of an ACE view: the case and NPA-asset facts arrive on the case signal, and `rwb_treatment` holds no foreign key into another schema (DP-01; DP-05; ASM-4402).
- No write outside the transaction that records the change: the treatment columns, the decision record and the outbox row commit together or not at all (DP-03; BR5).
- The decision is written before the change takes effect, and a refused or unavailable record leaves the case exactly as it was (BR5).
- The rule version and the decision code are written with every answer, so an auditor can see why an asset was released or held.
- No case status, no case task and no asset row is written: the parent moves the status and rwb-asset links the property under FEAT-AST-02 (ASM-4401).
- An applied migration is never edited: a correction to the unlock columns is a new version on the service sequence (DP-15).
- No credential, no secret and no document content appears in code, configuration, a prompt or an event payload.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-007 | An asset accepted under a deed in lieu is unlocked as a non performing asset by rule, with exceptions summarized for the approver | Business Requirements Program, section 5.9 | FEAT-TRT-14 | 07 Route, settle and claim | R-DIL-22; R-DIL-23 | TC-E3-014-01 to TC-E3-014-06 |

REQ-S2-007 is the requirement the sibling deed-in-lieu story traces for R-DIL-22 and R-DIL-23; FEAT-TRT-14 is the feature of this story (FSD S2 A2.14), and TSD S2 T8 maps its ten requirement IDs to FEAT-TRT-01 generically, so the trace runs on the feature code until the C1 PRD allocates the requirement of the unlock (GAP-2676; ASM-4400).

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3014-CON | Contract | H: declares the `AssetUnlock` element, its value rules, the decision-record group, the no-new-table rule and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library, its `MANDATORY` rule and its two exceptions (DP-03) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route of SCR-14 and SCR-16 (DP-19) |
| RWB-S2-E3001-APP | App development | Sibling: the treatment record the unlock is written on |
| RWB-S2-E3012-APP | App development | Sibling: the deed-in-lieu stage chain, the inspection capture, the transfer and the approver path of R-DIL-24 to R-DIL-26; the two build independently against their own contracts |
| The FEAT-AST-02 story of rwb-asset (S5) | App development | The asset list: FEAT-AST-02 links the case to the property by `asset_key` when the transfer completes, and it depends on FEAT-TRT-14 |
| P3 rwb-case | App development | The parent `CaseWorkflow`, the case status, the case task and the case signal the AC mock stands for |
| P7 rwb-decision | App development | The DEEDINLIEU package, its rows and its version, announced on `RulePackageInForce` |
| P1 rwb-source-data | App development | The ACE NPA-asset read that reaches this step as facts |
| RWB-ITG-W2 | Integration | The cross-service proof of the unlock against the live parent, the live package and rwb-asset, held by the wave 2 harness |

### 19. Out of scope

- The published element set, the value rules, the decision-record group, the compatibility rule and the fakes: RWB-S2-E3014-CON.
- The treatment record, its creation, its fields DF-TRT-001 to DF-TRT-033 and its own migration: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The deed-in-lieu stage chain — the offer and its documents, the inspection capture, the transfer, the AMIS record, the ALS settlement and the registration release: RWB-S2-E3012-APP and RWB-S2-E3012-CON.
- The failed unlock and its approver path, R-DIL-24 to R-DIL-26, with the three-working-day clock and the agent summary: the sibling stage and rwb-decision's `ApprovalWorkflow`.
- The asset record, the asset list, FEAT-AST-02, the AMIS interface and the auction that follows: rwb-asset (S5) and rwb-integration (P2).
- The case status, the case table, the case task and the case signal: rwb-case (P3).
- The DEEDINLIEU package, its rows, its version and the central ledger: rwb-decision (P7).
- The rights, the roles and the scope data, and the guard library that answers them: rwb-access (P4) and the platform library stories.
- The gateway-bff composite route, the screen field list and the layout: the platform edge story and the screen owners (DP-19).
- The inspection and unlock columns beyond the four this story writes, and any table for the inspection, the unlock or the release (GAP-2676; ASM-4399).
- The announcement of the release on Kafka: no source names an event, and the release travels to the parent and to rwb-asset as the case signal (GAP-2676; ASM-4401).
- The deployment of this build: chart values, the queue and topic provisioning, the flag, dashboards and the runbook.
