# RWB-S7-E6014-APP Apply the tax criteria

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6014-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-B |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S7-E6014-APP-16); the squad sizes the story at refinement |
| Depends on (build) | RWB-S7-E6014-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | v1 (the /v1 path of each consumed API in section 12.2) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the tax-criteria slice of RWB-E6-014 in rwb-writeoff (FEAT-WOF-02). The four legacy criteria are kept word for word with their origin tag; the step evaluates the WO route set (R-WO-01 with R-WO-03 on the hold path and R-WO-51 on the post charge-off remittance path), writes `write_off.tax_criteria_met` and `write_off.recovered_after` in `rwb_writeoff`, records the decision through the local decision-record library before any row changes (DP-03), answers rwb-case for the case moves `POPULATION_PROPOSED` and `CASE_CLOSED` and serves API-S7-001 on base `/api/recovery/writeoff/v1` (DP-13), reached from SCR-27 through the gateway-bff composite route (DP-19). The eligibility half of R-WO-01 belongs to the scan story of RWB-E6-013; `tax_criteria_version` has no owner, no table and no parameter key in any source; the R-WO-51 trigger has no channel in the target; DP-04, DP-09 and DP-10 are absent although this step evaluates 51 rules, the service owns topic EV-24 and the scan is job JOB-16. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (29 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off team member**, I want **the Workbench to test each proposed account against the tax criteria and record the result**, so that **write-offs follow the criteria and the committee's decision**.

This is the tax-criteria slice of legacy RWB-E6-014. It owns:

- the four legacy criteria of the key (AC1 to AC4), copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- one step of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow`, on the monthly scan trigger and on the case signal the parent forwards (Temporal and Drools Design slides 5 and 13; context pack workflow row);
- the evaluation of R-WO-01 for the tax criteria, of R-WO-03 on the hold path and of R-WO-51 on the post charge-off remittance path, against the WO package version in force (FSD S7 A2.2; TSD S7 T4);
- the write of the proposed population row of each account in `write_off` in `rwb_writeoff` — `tax_criteria_met` (DF-FIN-014) for the tax test and `recovered_after` (DF-FIN-020) for the post charge-off remittance — within the columns of DF-FIN-010 to DF-FIN-020 that this step fills;
- the local decision record of each outcome, written through RWB-PLT-E1027-CON before the rows change (DP-03), with the rule ID, the package version and the case move;
- the answer to rwb-case for `POPULATION_PROPOSED` and for `CASE_CLOSED`, and for `SCAN_HELD` on the tax-criteria hold path, with the rule and its version;
- the tax-criteria half of API-S7-001 `POST /write-off-scans` on base `/api/recovery/writeoff/v1`, and the scan state of SCR-27 Write-off proposal behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the scan operation, the `ScanRequest` and `WriteOffScan` elements, the fields DF-FIN-010 to DF-FIN-020, the consumed rows, the error set and the fakes, which are RWB-S7-E6014-CON; the eligibility test of R-WO-01 on both tracks and the population proposal of FEAT-WOF-01, which are the scan story of RWB-E6-013; the pack (FEAT-WOF-03), committee routing, approve, reject and defer (FEAT-WOF-05 to 08, API-S7-002), posting (FEAT-WOF-09) and closure by retention (FEAT-WOF-13); the case of record and its route states, which are rwb-case (P3); the WO package and `tax_criteria_version`, which are rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The objective, the problem and the metric are unchanged from the legacy story and the module FSD: the Workbench tests each proposed account against the tax criteria and records the result (FSD S7 A2.2.1), because write-off populations are assembled by hand each month (FSD S7 A1.3), and the result is measured on the decision log and the Workbench records against a target of "write-off packs accepted first time, rising each month", reviewed monthly (FSD S7 A2.2.1). The requirement is REQ-S7-001, "Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks" (FSD S7 Requirements served). What D-RCV-60 changes is who owns the population, the case, the version and the package.

- **The population is this service's.** `write_off` is S7's only table in `rwb_writeoff` (context pack ownership rows; TSD S7 T3.1), so the tested result and the post charge-off remittance are recorded here and nowhere else (ASM-5013).
- **The case stays with rwb-case.** `recovery_case`, its route states and the parent `CaseWorkflow` are P3's; this step reads the population, applies the rule, writes its row, records the decision and **answers** the case move (ASM-5012).
- **The version is a fact in force, not a constant.** VR-S7-002-1 and R-WO-03 hold the scan when `tax_criteria_version` is absent, and FEAT-WOF-14 lets the centre of excellence publish the criteria as a versioned rule load; no source gives the version a table, an owner or a parameter key, so it is read from the package in force and recorded with the outcome (ASM-5011, ASM-5016). The scan reports the version of the rule package it applied. The track names and the criteria are Not specified in the source documents (GAP-1469).
- **The package is read, not embedded.** The WO route set is 51 rules over 27 states (TSD S7 T4), governed in rwb-decision; DP-04 is not in this key's pattern set, so the package arrives on its read with the version in force (ASM-5016).
- **The decision is recorded first**, in the same transaction as the `write_off` row, which is what legacy AC1 asked for and legacy AC4 tested.
- **The remittance trigger has no owner.** R-WO-51 fires on "the buyer confirms receipt", the buyer is met on an S6 or S9 path and the connection matrix shows no event line into S7 from either, so the confirmation reaches this step as a signal the parent forwards and the amount is recorded on `recovered_after` (ASM-5014).

No business value moves: the tax criteria, the eligibility condition, the hold condition, the remittance condition and the states are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S7-E6014-CON is published: the scan operation, the `ScanRequest` and `WriteOffScan` elements, the fields DF-FIN-010 to DF-FIN-020, the consumed rows, the case-move answer, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-case population read is published with its fake, so the proposed accounts can be read on Day 1: the case reference, the case number, the product group, the balance, the account link and the state. The operation name is Not specified in the source documents (GAP-3018; ASM-5012), and the row is not in this story's contract-dependency list, which is None.
- The rwb-decision package read is published with its fake and answers the WO package at its version in force, with R-WO-01, R-WO-03 and R-WO-51 among its 51 rules over 27 states and the `tax_criteria_version` the FSD names; its operation name and the owner of `tax_criteria_version` are Not specified in the source documents (GAP-3018; ASM-5011, ASM-5016).
- The case-move answer of rwb-case is available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-3018; ASM-5012).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so the `write_off` row and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The WO package and `tax_criteria_version` are in force at their version and are read on the package read; the rule rows and the reference data they use are governed in rwb-decision and are not a build item of this story.
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-02).
- No approval is needed to build against a Draft contract baseline; this story stays at Draft (realignment v1) until the wave 4 contract freeze (ASM-5017).

### 4. Flow

1. The monthly write-off scan opens for a cut-off date, or the parent `CaseWorkflow` forwards a case signal. This step reads no ACE view and runs no inbound load (FSD S7 A1.4; FSD S7 A2.2.2 step 1).
2. The tax-criteria step of `WriteOffWorkflow` on queue `rwb-writeoff` receives the trigger: the monthly scan started for the cut-off date, or the forwarded case signal on the remittance path (FSD S7 A2.2.4.4; ASM-5015).
3. The step reads the WO package in force from rwb-decision, with its rule rows, the `tax_criteria_version` and the reference data the rules need, one hop with a 2 s budget and a breaker (ASM-5011, ASM-5016).
4. Where `tax_criteria_version` is absent, R-WO-03 holds the scan with VR-S7-002-1 and MSG-S7-001; nothing is written and no move is answered (FSD S7 A2.2.3.1).
5. The step reads the proposed population on the rwb-case contract: the cases in `SCAN_DUE` for the cut-off date, with their case reference, product group, balance, account link and state, read only; it never reads `recovery_case` (ASM-5012).
6. `TaxCriteriaEvaluator` evaluates R-WO-01 on each proposed account: the eligibility test is the scan story's, and this step runs the tax-criteria test of the rule and records its outcome (legacy AC2; FSD S7 A2.2.3.1).
7. The evaluation answers the rule ID, the package version with `tax_criteria_version`, the action of the rule and the case move the rule names — `POPULATION_PROPOSED` for R-WO-01, `SCAN_HELD` for R-WO-03 and `CASE_CLOSED` for R-WO-51.
8. `WriteOffDecisionRecordWriter` writes one decision record per outcome through the local decision-record library, **before any change**: the case reference, the rule ID with its package version, the inputs reference, the tax-criteria outcome, the amount and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
9. `WriteOffTaxCriteriaWriter` inserts the `write_off` row of a proposed account in one `rwb_writeoff` transaction with the decision record and the idempotency row, filling the columns of §11 and setting `tax_criteria_met` from the rule outcome; `amount` comes from the account balance the population read carries.
10. On the post charge off path, `WriteOffRemittanceWriter` updates the `write_off` row of the sold account with `recovered_after` and records the remittance, in one transaction with its decision record; the row is not created a second time.
11. `CaseMoveAnswer` answers rwb-case for each case with the move the rule names, with the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row; this service writes neither the row nor the state (ASM-5012).
12. A repeated trigger with the same cut-off date and population version writes no second row, no second record and no second answer, and counts the repeat; the `Idempotency-Key` of a repeated POST answers the scan it ran.
13. SCR-27 Write-off proposal shows the proposed population in its scan state — the tested accounts with their tax-criteria result, the held ones with their reason and the cut-off date — from this service through the gateway-bff composite route, read only, next to the case state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no `write_off` row, no remittance update and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E6-014-04, TC-E6-014-06 |
| X2 | The role does not hold the Write-off and posting right of the operation | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC5, TC-E6-014-05, TC-E6-014-09 |
| X3 | The case is not in `SCAN_DUE` or `REMITTED_TO_BUYER`, or has left the population since it was read | 409 and nothing is written for that case; a case that has already moved is not re-tested | None | AC2, AC3 |
| X4 | `tax_criteria_version` is absent from the package in force | R-WO-03 holds the scan at `SCAN_HELD`, writes nothing and shows the hold; the scan resumes when the version is published | MSG-S7-001 | AC2, X6 |
| X5 | The rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | None | AC1, AC2 |
| X6 | The case satisfies no rule of the package, or the remittance matches no sold account | No rule fires and the case keeps its state, or the remittance is not recorded and the item stays open; the population is written without it | MSG-GEN-001 | AC1, AC3 |
| X7 | A repeated trigger for the same cut-off date and population version, or the same `Idempotency-Key` twice | One row, one record and one answer per case; the repeat is counted and the key answers the scan that exists | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC6, TC-E6-014-10, Section 17, BR4, BR5 |

X1 and X4 are the legacy exception paths carried onto the slice, X2 and X3 are the access and precondition paths of the same feature, and X5 to X8 are the paths the target call types and the once-per-cut-off trigger add. The deviation codes X1 to X7 of R-WO-06 are codes of the rule package and are not the path identifiers of this table.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6014-CON, the rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P3 or P7 |
| Negotiable | The activity name, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screen, the operation and the table columns are fixed |
| Valuable | Every proposed account is tested against the tax criteria by rule with its version recorded, so the population that reaches the committee is provable |
| Estimable | One workflow step, one evaluator, one record write, two row writers, one case-move answer, two clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic population and a synthetic package through the contract fakes, plus the access, hold and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Apply the tax criteria

  Background:
    Given case "RC-2026-000914" is one of 120 cases in state "SCAN_DUE" on the population of the monthly write-off scan
    Given the WO rule package is in force at its version and carries R-WO-01, R-WO-03 and R-WO-51
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Apply the tax criteria (legacy RWB-E6-014 AC1)
    Given the rwb-case contract mock returns the population of the cut-off date with 120 cases in state "SCAN_DUE"
    Given the rwb-decision contract mock returns the WO package at its version with tax_criteria_version "2026-11"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tests each proposed account against the tax criteria and records the result
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-WO-01 (legacy RWB-E6-014 AC2)
    Given the rwb-case contract mock returns the case state "SCAN_DUE" for "RC-2026-000914" and accepts the move "POPULATION_PROPOSED"
    Given a case in state SCAN_DUE
    When monthly scan started
    Then test every open case against the eligibility rule on both tracks and the tax criteria
    Then the case moves to POPULATION_PROPOSED

  Scenario: AC3 Rule R-WO-51 (legacy RWB-E6-014 AC3)
    Given the rwb-case contract mock returns the case state "REMITTED_TO_BUYER" for "RC-2026-000914" and accepts the move "CASE_CLOSED"
    Given a case in state REMITTED_TO_BUYER
    When remittance confirmed
    Then record the remittance against the sold account and close the item
    Then the case moves to CASE_CLOSED

  Scenario: AC4 Not recorded (legacy RWB-E6-014 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Access (X2) (new, D-RCV-60)
    Given the role does not hold the Write-off and posting right of the scan operation
    When the scan operation is called
    Then the system answers 403 with MSG-P4-002 before any read or write
    Then nothing changes and no decision record is written

  Scenario: AC6 Boundary (X8) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a recovery_case row or another service's schema
    When the boundary test runs
    Then the grant refuses the statement and the build fails
    Then nothing is released

  Scenario: AC7 Activity retry and timeout (X5) (new, D-RCV-60)
    Given the rwb-case contract does not answer inside 2 s
    When the tax-criteria step runs
    Then the step retries on the workflow's own schedule
    Then nothing is written and no move is answered
    Then the caller sees 503 with the platform error envelope

  Scenario: AC8 Consumed call fails or does not answer (X5) (new, D-RCV-60)
    Given the rwb-decision contract call fails or does not answer
    When the tax-criteria step runs
    Then nothing is written and no move is answered
    Then the caller sees 503 with the platform error envelope

  Scenario: AC9 Disallowed transition (X3) (new, D-RCV-60)
    Given the case is not in SCAN_DUE or REMITTED_TO_BUYER
    When a status move is requested for the case
    Then the move is refused with 409
    Then nothing is written for that case

  Scenario: AC10 Business rules (BR1 to BR10) (new, D-RCV-60)
    Given the rule rows of section 8 and the fixtures of TC-E6-014-01 to TC-E6-014-10 are in place
    When each rule row of section 8 is evaluated
    Then each rule BR1 to BR10 holds and is tested by its BR ID
    Then a rule without a criterion or a test fails the build

  Scenario: AC11 Error answers of the provided operations (401, 403, 404) (new, D-RCV-60)
    Given the call to the scan operation carries no valid credential
    When the scan operation is called
    Then the system answers 401 before any read or write
    Then nothing changes and no decision record is written
    Then a call naming a case identifier that is not found answers 404 and nothing is written
    Then a call by a role without the right answers 403 as AC5 states

  Scenario: AC12 Replay of a write with the same idempotency key (BR8) (new, D-RCV-60)
    Given the scan write was answered once with an Idempotency-Key
    When the same write is replayed with the same Idempotency-Key
    Then nothing new is written and the same answer is returned
    Then one write-off row, one decision record and one answer exist per case
```

The four criteria are the legacy criteria of RWB-E6-014 word for word, with their origin tag added and nothing else changed except `decision log` read as `decision record`: the repeated `Then`, the wording of `its trigger arrives`, `monthly scan started`, `remittance confirmed` and `the action is taken` stands. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry one or two `Given the <service> contract mock returns <x>` lines, and those are the only additions. AC2 names the whole R-WO-01 action, whose eligibility half on both tracks is the scan story's: this story runs and records the tax-criteria half of the same rule, so one step produces the outcome and neither duplicates the other (ASM-5012). The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-01 (BR11) | Write-off | D9 | SCAN_DUE | MONTHLY_SCAN_STARTED | cut_off_date reached and the ALS load is complete | Test every open case against the eligibility rule on both tracks and the tax criteria | POPULATION_PROPOSED | Write-off team | Rules component, COLLINS, ALS core and GL | monthly cut-off |
| R-WO-03 (BR12) | Write-off | D9 | SCAN_DUE | TAX_CRITERIA_UNPUBLISHED | tax_criteria_version absent | Hold the scan until Finance publishes the version | SCAN_HELD | Write-off team | Reference data, Finance provision feed | None |
| R-WO-51 (BR13) | Write-off | D9 | REMITTED_TO_BUYER | REMITTANCE_CONFIRMED | the buyer confirms receipt | Record the remittance against the sold account and close the item | CASE_CLOSED | Credit Administration | ALS and GL, Workbench | 5 working days |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: in the target the "Rules component" is the WO package read from rwb-decision (P7) and evaluated here, "Reference data" and the "Finance provision feed" are the versioned rows that carry `tax_criteria_version`, "Workbench" is SCR-27 and "ALS core and GL" is reached by rwb-payment (P8) on the posting and remittance paths, not by this step. The case moves are written by rwb-case on this story's answer, and the `write_off` rows are written here. R-WO-02, the hold for an absent ALS extract, reaches the same `SCAN_HELD` state from the scan feed; no criterion of this key names it and its message is the data-staleness message of that feed, so this story tables the state with the restart of R-WO-04 and not the ALS-load condition.

| ID | Rule | Source |
|---|---|---|
| BR1 | The population is this service's: `write_off` is the row of `rwb_writeoff`, and no other service writes it | Context pack ownership rows (table `write_off`); TSD S7 T3.1; FSD S7 A2.2.2 |
| BR2 | The decision is recorded before the row changes, with the rule ID, the package version and the tax criteria version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy AC1 and AC4 |
| BR3 | The test is by rule: the tax criteria, the eligibility condition, the hold condition and the states are rule rows and reference data read with their version, never a constant or a branch | FSD S7 BR-S7-002; Business Rules and Routing Logic v4; legacy Guardrails |
| BR4 | The case move is answered and not written: `recovery_case` and the states `SCAN_DUE`, `SCAN_HELD`, `POPULATION_PROPOSED`, `REMITTED_TO_BUYER` and `CASE_CLOSED` are rwb-case's | ASM-5012; TSD S7 T4 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_writeoff`; `case_id` is an identifier of another service's fact | DP-01; TSD S7 T3.3 |
| BR6 | `tax_criteria_version` is read from the package in force and recorded with the outcome; an absent version holds the scan and is never defaulted | FSD S7 VR-S7-002-1 and A2.2.3.1; R-WO-03; ASM-5011 |
| BR7 | The post charge off remittance is recorded against the sold account in `recovered_after`; no new table and no new column is added for it | TSD S7 T3.1 (DF-FIN-020); ASM-5013 |
| BR8 | The same trigger twice, or the same `Idempotency-Key` twice, writes one row, one record and one answer per case | TSD S7 T-A.2 |
| BR9 | No person name, address, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input; the population carries identifiers, amounts, dates and a rule version only | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR10 | The rights are the rows of TSD S7 T6.1 on the capability area "Write-off and posting": right C to create the scan, right A to decide, right R to read | TSD S7 T6.1, T-A.1 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the `write_off` row and the state of the step.

| From (case route state) | Event | Condition | To |
|---|---|---|---|
| SCAN_DUE | A tax-criteria test under R-WO-01 | cut_off_date reached and the ALS load is complete | POPULATION_PROPOSED, answered per case with the tax-criteria result recorded |
| SCAN_DUE | The hold of R-WO-03 | tax_criteria_version absent | SCAN_HELD, answered with MSG-S7-001 and nothing written |
| SCAN_HELD | The restart of R-WO-04 | the ALS extract is complete and the tax criteria published | SCAN_DUE, answered for the next run |
| REMITTED_TO_BUYER | A remittance under R-WO-51 | the buyer confirms receipt | CASE_CLOSED, with `recovered_after` written on the sold account's row |
| Any other state | A trigger for a case outside the population | X3 | Unchanged: 409 and nothing written |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The scan opens, or the parent forwards a case signal | The package in force is read | Evaluating |
| Evaluating | R-WO-01 or R-WO-51 fires on the case | The decision record is written | Applying |
| Applying | The `write_off` row is written and the answers sent | The transaction commits | Waiting for the next cut-off |
| Evaluating | `tax_criteria_version` is absent | X4 | Held, until the version is published |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |

The route states are those of the WRITEOFF machine of TSD S7 T4 and live on the case of record. This step writes `tax_criteria_met` and `recovered_after` only; `posted_date`, `committee_date`, `responsibility_center`, `cost_center` and `gl_product` are the later stories' columns.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WRITEOFF, write-off team member | Write-off and posting CRU in TSD S7 T6.1: the primary role of the feature, reading the population and re-running the scan |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: the role the remittance path names as owner, reading and acting on the item |
| RW-PRODHEAD, RW-WOCOMM, RW-FINANCE | Write-off and posting RA: read the tested population and decide through the committee stories, not here |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT | Write-off and posting R as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Runs the step, reads the population and the package, writes the record and the row and answers the moves; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S7 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the write-off team member as also-user (FSD S7 A2.2.3.3), and both statements hold: the step runs under the service identity with no officer task on the happy path, and the officer is the primary role when a person acts, on SCR-27 and on a re-run of the scan. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated here and not built here: the scan operation is authorised through the rwb-access authorise check for the capability area `Write-off and posting` and the right of the operation (TSD S7 T6.1); the check's operation path is Not specified in the source documents (DOR-RWB-S7-E6014-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Write, the write-off reference of the row and the answer |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Write, from the population read of the cut-off date |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Write, the decision record of the outcome |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Write, from the balance the population read carries |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Write, the result of the tax-criteria test |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Not written here: the committee stories |
| DF-FIN-016 | write_off (S7, `rwb_writeoff`) | posted_date | Not written here: the posting story (GL is the source) |
| DF-FIN-017 | write_off (S7, `rwb_writeoff`) | responsibility_center | Not written here: the posting story (GL is the source) |
| DF-FIN-018 | write_off (S7, `rwb_writeoff`) | cost_center | Not written here: the posting story (GL is the source) |
| DF-FIN-019 | write_off (S7, `rwb_writeoff`) | gl_product | Not written here: the posting story (GL is the source) |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Write, the post charge off remittance of R-WO-51 |
| Standard columns | write_off (S7, `rwb_writeoff`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the row changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the population and the state arrive on the rwb-case contract |
| `tax_criteria_version` | the version of the tax criteria in force | Read from the package; its table, its owner and its key are Not specified in the source documents (GAP-3018; ASM-5011) |
| rule_row, decision_log_entry (P7) | the rule rows and the central ledger | Not written and not read here: the local record is this service's and the rule rows arrive on the package read |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary, and the ACE and ledger rows are the rows the legacy Data table lists, with their owners changed to P1, P3 and P7 by the target. **No new table, no new column and no migration**: `write_off` arrives with the DB story of this service, this story writes seven of its columns, and `decision_record` and `idempotency_key` are library objects created in `rwb_writeoff` by the library's own migration (DP-03). `outbox_event` also sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3). Every ACE field is read through the rwb-source-data contract, under the FSD field names that contract returns; no ACE view or ACE table is read by this service (GAP-1792). The personal-data class of each field carried here is the class Data Classification v5 gives it; the fields classed as personal data are Not specified in the source documents (DOR-RWB-S7-E6014-APP-11).

**No personal data.** The rows carry identifiers, amounts, dates, a boolean, list values and a rule version. No name, address, contact value or identity number enters `rwb_writeoff`, the record, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This story supplies the behaviour behind the tax-criteria half of the scan, whose shape RWB-S7-E6014-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-off-scans` | ScanRequest in, WriteOffScan out, the scan run for a cut-off date with the tested population and its tax-criteria results (API-S7-001) | Write-off and posting, right C, scope applied | `Idempotency-Key` header |

The errors are 401, 403 with MSG-P4-002, 409 for a repeated or conflicting cut-off date, 422 with MSG-GEN-001 and MSG-S7-001 for an absent `tax_criteria_version`, and 503 when the library or a consumed contract does not answer, as TSD S7 T-A.2 gives them. `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) records the committee decision and belongs to the approve, reject and defer stories of this key; it is not built or declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The population read (operation name Not specified in the source documents (GAP-3018; ASM-5012)) | `/api/recovery/case/v1` | P3 rwb-case | The cases in `SCAN_DUE` for the cut-off date and the sold account of the remittance path, with the case reference, product group, balance, account link and state; read only, faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3018; ASM-5011)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-01, R-WO-03 and R-WO-51 among its 51 rules over 27 states and `tax_criteria_version`; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3018; ASM-5012)) | rwb-case (P3) | P3 rwb-case | The move `POPULATION_PROPOSED`, `SCAN_HELD` or `CASE_CLOSED` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3018; ASM-5012).

#### 12.3 Events published

None. The service publishes on `rwb.writeoff.events.v1`, whose event set carries `WriteOffApproved` (event `EV-24`) with the retry and `.dlt` topics of the platform (TSD S7 T5.3; DP-14), and it does not belong to this step: the tax-criteria test approves nothing. `WriteOffApproved` is the committee approval story's, so this story declares no event, no producer group and no outbox row of its own, and a build that publishes one fails the absence test. The outbox and inbox library that relays it is the DP-09 dependency the plan does not carry for this key (ASM-5016).

#### 12.4 Events consumed

None. The step is started by the monthly scan or by the case signal the parent `CaseWorkflow` forwards, and it holds no consumer group, no subscription and no inbox row (ASM-5014). The remittance confirmation of R-WO-51 has no event path into this service in the connection matrix, so it reaches the step as a forwarded signal and not as a Kafka subscription; a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` | Input: the case, the cut-off date, the population reference and the package in force; signals: the population answered by rwb-case, the package in force and the remittance signal. It hosts the tax-criteria step and needs no compensation |
| `evaluateTaxCriteria` | Activity, the one tax-criteria step | `rwb-writeoff` | The population, the package and the cut-off date in; the rule ID with its package version, the tax-criteria result, the remittance amount, the write-off reference and the case moves out, with the record and the row written in one transaction |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice fixed by no source document. The step waits on the monthly scan and on the forwarded signal, because R-WO-03 and R-WO-51 carry no clock of their own beyond the 5 working days of the remittance timer.

Workflow ID form: Not specified in the source documents (CG-ALL-10862). Start rule: JOB-16 on the third working day after AceDataReady (R-WO-01); the start or signalWithStart choice and the duplicate-start policy are Not specified in the source documents (CG-ALL-10862).

Trigger (GAP-1801): the scan runs as a Temporal Schedule in rwb-writeoff on the third working day and also tests the ALS batch, so both the date and the data condition are met; no Quartz table, connection or job is used, and the ruling of ASM-A6-flows-12 stands.

Rule package (GAP-1802): the criteria and rules are read from a governed package through the rwb-decision contract, and the package and rule version are recorded on every scan and decision. The package code and its promotion date are Not specified in the source documents (GAP-1802).

#### 12.6 Schedules

None. The monthly write-off scan is job `JOB-16` in the legacy and becomes a Temporal Schedule of the scan story (`RWB-S7-E6013-APP`), which starts this step; this story declares no Schedule and no Quartz row (ASM-5015). The pattern set of this key does not carry DP-10 and its `RWB-PLT-E1071-CON` row, and that absence is recorded rather than added (GAP-3018).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of a balance on a case and the proposed population; this story writes the columns of §11 |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), every `v_ace_*` view (P1), `proceeds` (P8), and the later stories' tables of this service. No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case population fake | The population of the cut-off date with 120 cases in `SCAN_DUE`, `RC-2026-000914` among them, with the product group, the balance, the account link and the state; a case that has left the population | AC1, AC2, X3 |
| rwb-decision package fake | The WO package at its version in force with R-WO-01, R-WO-03 and R-WO-51, `tax_criteria_version "2026-11"`, and an absent version | AC1, AC2, X4 |
| rwb-case case-move fake | The moves `POPULATION_PROPOSED`, `SCAN_HELD` and `CASE_CLOSED` accepted for `RC-2026-000914`; a move refused because the case is not in the expected state | AC2, AC3, X3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000914`, in its scan state | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the population read, the package read and the case-move answer carry the placeholder until their owners confirm them (GAP-3018; ASM-5012).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | `POST /write-off-scans` on `/api/recovery/writeoff/v1`; the population read, the package read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (EV-24) is the committee story's and no event is consumed here (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `WriteOffWorkflow` and its tax-criteria step on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `taxcriteria`; front end `src/modules/recovery/writeoff/WriteOffProposal.tsx`, the fragment SCR-27 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the `write_off` row commit together or not at all. DP-13 moves the base of the scan operation and nothing else. DP-19 is how SCR-27 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-09 (the outbox and inbox library) and DP-10 (the Temporal Schedule or the event-started workflow) are real dependencies of this step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3018; ASM-5015, ASM-5016).

**Dependencies the tables add and the plan does not hold.** The three consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON`; the schedule row of DP-10 would add `RWB-PLT-E1071-CON` for `JOB-16`; the outbox library of DP-09 would add `RWB-PLT-TE006-CON`. None of the three is declared, because the step reads the package as data, starts on the scan that its sibling owns and publishes nothing. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` tax-criteria branch | Workflow | Waits for the scan or the forwarded signal, reads the package in force and reports the outcome to the parent |
| `evaluateTaxCriteria` | Activity | Reads the population and the package, evaluates R-WO-01, R-WO-03 and R-WO-51, writes the record and the row, answers the moves |
| `TaxCriteriaEvaluator` | Service | The rule evaluation over the package in force, with `tax_criteria_version`, the hold path, the remittance path and the no-fire path |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked; refuses the step when the write fails |
| `WriteOffTaxCriteriaWriter` | Repository | Inserts the `write_off` row in one `rwb_writeoff` transaction with the idempotency row and the optimistic lock |
| `WriteOffRemittanceWriter` | Repository | Updates `recovered_after` on the sold account's row for R-WO-51, in one transaction with its record |
| `CasePopulationClient` | Client | The population read of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `RulePackageClient` | Client | The package read of rwb-decision at its version in force, with `tax_criteria_version` |
| `CaseMoveAnswer` | Client | The case-move answer to rwb-case, one answer per case of the population |
| `WriteOffScanController` | Controller | The scan operation, the capability area and right, the `Idempotency-Key` and the problem mapping |
| `WriteOffProposal` | React component | Shows the tested population on SCR-27, read only, with the held, refused and stale states |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the record and idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the tax criteria version, the remittance reference or the case: the version is a package fact and the case is P3's fact, referenced and not copied.

**Configuration and reference data.**

- `tax_criteria_version` and the WO rule rows: package facts read with their version, never a constant, a default or a branch (ASM-5011).
- Parameters and reference-data contract: the parameter keys of the WO rule rows and of `tax_criteria_version` are Not specified in the source documents (DOR-RWB-S7-E6014-APP-20); the reference data is read on the rule-package read of rwb-decision (`RulePackageClient`, DP-06, DP-07), not from a parameter of this service.
- The capability area "Write-off and posting" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the monthly cut-off is the rule's timer and not a parameter of this build.

**Build steps**

1. The tax-criteria branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the scan and the forwarded signal as its triggers.
2. `CasePopulationClient` and `RulePackageClient` against their fakes, with the 2 s budget, the breaker, the out-of-population path and the no-answer path (AC1, AC2, X3, X5).
3. `TaxCriteriaEvaluator` over the package, with R-WO-01, R-WO-03, R-WO-51, `tax_criteria_version`, the hold path and the no-fire path (AC1, AC2, AC3, X4, X6).
4. `WriteOffDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC4, X1).
5. `WriteOffTaxCriteriaWriter` with the one transaction, the row, the idempotency row and the optimistic lock (AC1, AC2, X7).
6. `WriteOffRemittanceWriter` with the `recovered_after` update of the sold account (AC3).
7. `CaseMoveAnswer` with the three moves, one per case of the population (AC2, AC3, X3).
8. `WriteOffScanController` with the right, the `Idempotency-Key` and the problem mapping of the declared errors, and `WriteOffProposal` on SCR-27 through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to another service's schema (X8, BR4, BR5).

**Feature flag.** `rwb.writeoff.taxcriteria-v1`, a flag of the platform library; off means the step holds the scan, writes nothing and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic population in SIT, R-WO-01 records the tax-criteria result, R-WO-03 holds an absent version, R-WO-51 records a remittance and answers `CASE_CLOSED`, a repeated trigger writes once, a forced record failure changes nothing, no row of another service's table and no `v_ace_*` read exists in the build, and SCR-27 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | `tax_criteria_version` is absent from the package in force, so R-WO-03 holds the scan (X4) | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of the request, of the population or of the package is absent or invalid (X6) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right calls the scan (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set and of FSD S7 A2.2.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S7-001 is the VR-S7-002-1 hold of R-WO-03 and is shown on SCR-27 in its held state.

### 15. Screens and states

SCR-27 Write-off proposal, in its loading and scan states, is served through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the tested population, its tax-criteria result and the remittance record, and rwb-case for the case and its route state; this story fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The state this story produces is the scan state of SCR-27: the proposed accounts of the cut-off date with their tax-criteria result, the held accounts with MSG-S7-001, and the sold account whose remittance was recorded. The legacy screen table gives the states "Scan; proposed; in committee; approved"; the proposed state is this story's reading of "Scan" once the row exists, and the in-committee and approved states belong to the committee stories. The refusal, not-recorded and hold states read the messages of section 14.

The empty, loading, error and no access states of SCR-27 are not in Screen Specifications v1 and are Not specified in the source documents (CG-ALL-10867).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-014-01 | AC1 | Component | The 120-case population and the package at `2026-11` on the fakes; the `write_off` row, the record and the answer asserted |
| TC-E6-014-02 | AC2 | Component | Case `RC-2026-000914` at `SCAN_DUE`; the tax-criteria result written and the `POPULATION_PROPOSED` move asserted on the fake |
| TC-E6-014-03 | AC3 | Component | Case `RC-2026-000914` at `REMITTED_TO_BUYER`; `recovered_after` written and the `CASE_CLOSED` move asserted on the fake |
| TC-E6-014-04 | AC4 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E6-014-05 | Access | Component | A role without the Write-off and posting right; 403 with MSG-P4-002 and no read |
| TC-E6-014-06 | Principle 5 | Component | A forced decision record write failure inside the transaction; no row, no remittance update and no answer |
| TC-E6-014-07 | Contract of the operations, events and activities of section 12 | Contract | The published contracts of the scan operation and of the consumed rows of section 12.2 on the fakes; each operation and activity checked against its contract |
| TC-E6-014-08 | Boundary of the section 12.7 tables (ASM-3438) | Component | The tables of section 12.7 and their owners; no statement outside `rwb_writeoff` and no table of another owner read or written |
| TC-E6-014-09 | AC5 | Component | A role without the Write-off and posting right on the scan operation; 403 with MSG-P4-002, nothing read or written |
| TC-E6-014-10 | AC6 | Component | A statement, a component or a test reaching a `v_ace_*` view or another service's schema; the boundary test fails the build |
| TC-E6-014-11 | BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 | Component | The fixtures of TC-E6-014-01 to TC-E6-014-10; each rule row tested by its BR ID |
| TC-E6-014-12 | AC7 | Component | The rwb-case contract stub not answering inside 2 s; the retry, no write, no move and the 503 asserted |
| TC-E6-014-13 | AC8 | Component | The rwb-decision contract stub failing or not answering; no write, no move and the 503 asserted |
| TC-E6-014-14 | AC9 | Component | A case at a state outside SCAN_DUE and REMITTED_TO_BUYER; the 409 asserted and nothing written |
| TC-E6-014-15 | AC10 | Component | The fixtures of TC-E6-014-01 to TC-E6-014-10; each rule row of section 8 asserted by its BR ID |
| TC-E6-014-16 | AC11 | Component | A call without a valid credential, a call naming an unknown case identifier and a call by a role without the right; 401, 404 and 403 asserted and nothing written |
| TC-E6-014-17 | AC12 | Component | The scan write sent twice with the same Idempotency-Key; one row, one decision record and one answer asserted |

The six legacy cases are those of RWB-E6-014 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the tax criteria, `tax_criteria_version`, the eligibility and hold conditions, the remittance condition, the states and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, amounts, dates, a boolean and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test.
- The case stays with rwb-case: no `recovery_case` row, no case route-state column and no case write here (BR4).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no `v_ace_write_off` read.
- The decision is recorded before the change; a build that writes the row outside the record's transaction fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Story element | Test cases |
|---|---|---|---|---|---|
| REQ-S7-001 | Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks (FSD S7 Requirements served); the split plan carries no requirement id for this slice (GAP-3018) | FEAT-WOF-02 | Not specified in the source documents (DOR-RWB-S7-E6014-APP-2) | The tax-criteria step, the `write_off` row and the case moves | TC-E6-014-01, TC-E6-014-02, TC-E6-014-06 |
| REQ-S7-007 | Recoveries after charge-off are matched to the account, with income and agency fees recorded (FSD S7 Requirements served) | FEAT-WOF-02 | Not specified in the source documents (DOR-RWB-S7-E6014-APP-2) | The `recovered_after` write and the `CASE_CLOSED` answer of R-WO-51 | TC-E6-014-03 |
| ADR-013 | 19 services inside ACE | FEAT-WOF-02 | Not specified in the source documents (DOR-RWB-S7-E6014-APP-2) | rwb-writeoff as the owner of the population | TC-E6-014-01 |
| ADR-014 | Schema and login per service | FEAT-WOF-02 | Not specified in the source documents (DOR-RWB-S7-E6014-APP-2) | `rwb_writeoff` and its own login | TC-E6-014-01 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | FEAT-WOF-02 | Not specified in the source documents (DOR-RWB-S7-E6014-APP-2) | The WO package read at its version and evaluated here | TC-E6-014-01, TC-E6-014-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | FEAT-WOF-02 | Not specified in the source documents (DOR-RWB-S7-E6014-APP-2) | The three consumed rows with their budget and breaker | TC-E6-014-01, TC-E6-014-02 |
| ADR-022 | Local decision record plus central ledger | FEAT-WOF-02 | Not specified in the source documents (DOR-RWB-S7-E6014-APP-2) | The record written before the change | TC-E6-014-04, TC-E6-014-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-014, disposition Split (rework); feature FEAT-WOF-02 |
| Legacy criteria | AC1, AC2, AC3 and AC4, owned word for word by this story; the eligibility half of AC2's rule is the scan story's |
| Source text | Legacy RWB-E6-014; FSD S7 Write-off and recovery v3 A2.2 and Requirements served; TSD S7 Write-off and recovery v2 T2, T3.1, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-01, R-WO-03 and R-WO-51 |
| Test cases | TC-E6-014-01 to TC-E6-014-06 |
| Feature and screens | FEAT-WOF-02, SCR-27 Write-off proposal |
| Rules | R-WO-01, R-WO-03 and R-WO-51, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-017, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the scan operation, the `ScanRequest` and `WriteOffScan` elements, the fields DF-FIN-010 to DF-FIN-020, the consumed rows, the error set and the fakes: RWB-S7-E6014-CON.
- The eligibility test of R-WO-01 on both tracks, the population proposal of FEAT-WOF-01 and the monthly scan Schedule from `JOB-16`: the scan story of RWB-E6-013 (ASM-5015).
- The committee decision of API-S7-002, the pack, the routing, the approve, the reject and the defer: FEAT-WOF-03 and FEAT-WOF-05 to 08.
- The posting to ALS and the general ledger, the provision release, the Finance feed and the reconciliation of the approved and posted populations: FEAT-WOF-09 to 11.
- The exception loop, the retention closure, the change of the criteria as a versioned rule load and the post charge off sale: FEAT-WOF-12 to 14 and FEAT-WOF-16.
- The owner, the table and the parameter key of `tax_criteria_version`: no source names them (GAP-3018; ASM-5011).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3); the WO package and its rule rows: rwb-decision (P7); the money and the posting reference: rwb-payment (P8).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
