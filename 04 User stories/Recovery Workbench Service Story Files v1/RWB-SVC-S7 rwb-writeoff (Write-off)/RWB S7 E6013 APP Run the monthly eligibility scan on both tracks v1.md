# RWB-S7-E6013-APP Run the monthly eligibility scan on both tracks

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-A |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S7-E6013-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the scan slice of RWB-E6-013 in rwb-writeoff. The three legacy criteria are kept word for word with their origin tag; the monthly step evaluates the WO package (R-WO-01 to R-WO-04), writes one `write_off` row per proposed case in `rwb_writeoff`, records the decision through the local decision-record library before any row changes (DP-03), answers rwb-case for the case move `POPULATION_PROPOSED` or `SCAN_HELD` and serves API-S7-001 on base `/api/recovery/writeoff/v1` (DP-13), reached from SCR-27 through the gateway-bff composite route (DP-19). The scan is JOB-16 and runs from a Temporal Schedule; DP-10 is absent from the pattern set of this key, as are DP-04, DP-05 and DP-09, and all four are recorded rather than added to the metadata row. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off team member (RW-WRITEOFF)**, I want **the Workbench to scan the portfolio each month against the eligibility rules and propose the write-off population**, so that **write-offs follow the criteria and the committee's decision**.

This is the scan slice of legacy RWB-E6-013. It owns:

- the three legacy criteria (AC1, AC2, AC3), copied verbatim with their origin tag, and the rules, messages and screen state they depend on;
- the monthly step of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`, the stage child of `CaseWorkflow`, and the JOB-16 scan behind a Temporal Schedule (context pack ownership rows; Temporal and Drools Design slides 5, 12 and 13);
- the read of the open cases of the write-off stage for a cut-off date and the evaluation of R-WO-01, R-WO-02, R-WO-03 and R-WO-04 against the WO package version in force (FSD S7 A2.1; TSD S7 T4);
- one `write_off` row per proposed case in `rwb_writeoff`, within the columns of DF-FIN-010 to DF-FIN-020 that this step fills (§11);
- the local decision record of each outcome, written before the rows change (DP-03), with the rule ID, the package version and the case move;
- the answer to rwb-case for `POPULATION_PROPOSED`, or for `SCAN_HELD` on the two hold paths, with the rule and its version;
- API-S7-001 `POST /write-off-scans` on base `/api/recovery/writeoff/v1` and the scan state of SCR-27 Write-off proposal behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the operation, the `ScanRequest` and `WriteOffScan` elements, the `WriteOff` element, the field IDs, the consumed rows, the rights, the error set and the fakes, which are RWB-S7-E6013-CON; the per-account tax record of FEAT-WOF-02 (RWB-S7-E6014-APP); the pack (RWB-S7-E6015-APP); the removal from the population and R-WO-07 (RWB-S7-E6016-APP); the committee routing (RWB-S7-E6017-APP); the approval, rejection and deferral with API-S7-002 (RWB-S7-E6018-APP); the posting, `WriteOffApproved` (EV-24) and the money (RWB-S7-E6021-APP and rwb-payment, P8); the case of record and its route states, which are rwb-case (P3); the ACE batch status and the balance products, which are rwb-source-data's (P1); the WO package, which is rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: the Workbench scans the portfolio each month against the eligibility rules and proposes the write-off population (FSD S7 A2.1.1), because write-off populations are assembled by hand each month (FSD S7 A1.3), and the measure is "Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly" (FSD S7 A2.1.1). The requirement is REQ-S7-001, "Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks." (FSD S7 Requirements served). What D-RCV-60 changes is who owns the population, the case, the batch status and the package.

- **The population is this service's.** `write_off` is S7's one table in `rwb_writeoff` (context pack ownership rows; TSD S7 T3.1), so the proposed population is recorded here and nowhere else.
- **The case stays with rwb-case.** `recovery_case` and the route states `SCAN_DUE`, `POPULATION_PROPOSED` and `SCAN_HELD` are P3's; this step reads the list of the stage, evaluates the rule, writes its rows and **answers** the move to rwb-case (ASM-4888).
- **The ACE batch status stays with rwb-source-data.** R-WO-01 tests the ALS load as `COMPLETED` in `v_ace_batch_status`, and in the target only rwb-source-data holds the `v_ace_*` views, so the status arrives on the owner's contract with its business date and no view is granted here (ASM-5004).
- **The package is read, not embedded.** The WO route set is 51 rules over 27 states (TSD S7 T4), authored, tested and approved in rwb-decision; DP-04 is not in this key's pattern set, so the package arrives on its read with the version in force and the version is recorded with the outcome (ASM-5005).
- **The decision is recorded first**, in the same transaction as the rows, which is what legacy AC1 asked for and legacy AC3 tested.
- **The clock is JOB-16.** The legacy job runs "Monthly, 3rd working day, on the ACE batch-complete record for ALS" (Batch and Scheduling Design v4, JOB-16) and its failure action is "Hold until the ACE batch or the version arrives (R-WO-02, R-WO-03)"; in the target the clock is a Temporal Schedule and the two holds are the step's own. DP-10 is absent from the pattern set, so the Schedule is built and the kit row is recorded (ASM-5008).
- **Both tracks are one population.** The route set's end states name them: "Posted, placed, recovered and closed after the retention period; Rejected by the committee and returned to the pursue track; Sold to a buyer as a charged-off population" (Business Rules and Routing Logic v4, sheet Route sets, row Write-off), and R-WO-29 and R-WO-32 are what choose between them after posting. The criterion that separates the tracks is named by no source, so the scan applies the one eligibility rule and the tax criteria to every open case and does not invent a per-track test (ASM-5007).
- **The scan has no table of its own.** The operation answers `id`, `cutOffDate`, `eligible`, `heldOut` and `status` (API Specification v4, `WriteOffScan`), while `write_off` carries no cut-off date and no scan reference and the ownership rows give S7 one table only, so the answer is assembled from the run and its rows and the missing table is recorded (ASM-5009).

No business value moves: the eligibility condition, the tax criteria, the cut-off date, the third working day and the two tracks are rule rows and reference data read with their version, never constants of the code.

### 3. Preconditions

- RWB-S7-E6013-CON is published: the operation, the `ScanRequest` and `WriteOffScan` elements, the `WriteOff` element, the field IDs, the consumed rows, the rights, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-case case-list read is published with its fake, so the open cases of the stage can be read on Day 1: the case reference, the case number, the product group, the account link, the state and the balance key. Its operation name is Not specified in the source documents (GAP-3016; ASM-5004).
- The rwb-source-data contracts are published with their fakes: the read that carries the ACE batch status of source ALS with its business date, and the read that carries the balance of the account. Their operation names are Not specified in the source documents (GAP-3016; ASM-5004).
- The rwb-decision rule-package read is published with its fake and answers the WO package at its version in force, with R-WO-01 to R-WO-04 among its 51 rules over 27 states and the tax criteria among its rows; its operation name is Not specified in the source documents (GAP-3016; ASM-5005).
- The case-move answer is available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-3016; ASM-4888).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so the rows and their record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The WO package is in force at its version and the tax criteria version is published; where the tax criteria version is absent the scan holds with MSG-S7-001 and R-WO-03, which is the state the story must be able to reach.
- The Temporal Schedule for JOB-16 exists in namespace `rwb-recovery`; its schedule ID, its hour and the definition of the third working day are Not specified in the source documents (GAP-3016; ASM-5008).
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_batch_status` or `rwb_case` is refused by the database and fails the boundary test (ASM-5004).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6013-CON when its tests pass.

### 4. Flow

1. The Temporal Schedule of JOB-16 fires on the third working day of the month for the cut-off date; rwb-source-data publishes the ACE data-ready fact for source ALS with its business date, and this service reads no ACE view (FSD S7 A2.1.2 step 1; Batch and Scheduling Design v4, JOB-16; ASM-5004).
2. The scan step of `WriteOffWorkflow` on queue `rwb-writeoff` reads the version of the WO package in force from rwb-decision, one hop with a 2 s budget and a breaker (ASM-5005).
3. The step reads the ACE batch status of source ALS for the cut-off date on the rwb-source-data contract, with its business date. An absent or incomplete load holds the scan under R-WO-02 with no row and an incident raised. An absent `tax_criteria_version` holds it under R-WO-03 with MSG-S7-001. A restored load and a published version return it to `SCAN_DUE` under R-WO-04 (FSD S7 A2.1.3.1, VR-S7-001-1; TSD S7 T4).
4. The step reads the open cases of the write-off stage for the cut-off date on the rwb-case contract: the case reference, the case number, the product group, the account link, the state and the balance key, read only; it never reads `recovery_case` (ASM-5004, ASM-4888).
5. The step reads the balance of each case's account on the rwb-source-data product, with the as-of date of the product, which is the amount the row carries (DF-FIN-013 Source GL).
6. `EligibilityEvaluator` evaluates R-WO-01 on each case: the eligibility rule on both tracks and the tax criteria, with the package version in force. Where the rule passes, the case is proposed and `POPULATION_PROPOSED` is the move. Where the rule does not fire, the case keeps its state and the reason is reported to the parent.
7. The evaluation answers the rule ID, the package version, the action of the rule and the case move; the two tracks of the rule are carried as the rule's own facts and are not re-tested here.
8. `WriteOffDecisionRecordWriter` writes one decision record per outcome through the local decision-record library, **before any change**: the case reference, the write-off reference, the rule ID with its package version, the inputs reference with the business date of the batch and the as-of date of the balance, the cut-off date, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
9. `WriteOffRowWriter` inserts one `write_off` row per proposed case in one `rwb_writeoff` transaction with the decision record and the idempotency row, filling the columns of §11 and carrying `POPULATION_PROPOSED` as the row state; the ids of DF-FIN-015 to DF-FIN-019 stay empty for the later stories.
10. `CaseMoveAnswer` answers rwb-case for each case of the list with the move the rule names — `POPULATION_PROPOSED` for a proposed case and `SCAN_HELD` for a held one — with the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row; this service writes neither the row nor the state (ASM-4888).
11. The step counts the proposed and the held-out cases of the run and answers `WriteOffScan` with `id`, `cutOffDate`, `eligible`, `heldOut` and `status`; the persisted form of that answer has no table and is recorded as a gap (ASM-5009).
12. A repeated trigger with the same cut-off date and the same batch business date writes no second row, no second record and no second answer, and counts the repeat; the same `Idempotency-Key` answers the run it created.
13. SCR-27 Write-off proposal shows the population in its scan state — the proposed cases, the held-out cases with their reason and the cut-off date — from this service through the gateway-bff composite route, read only, next to the case state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no `write_off` row and no case-move answer leaves the service | MSG-P7-003 | AC3, TC-E6-013-03, TC-E6-013-05 |
| X2 | The role does not hold the Write-off and posting right C of the operation | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E6-013-04 |
| X3 | The ACE batch status for source ALS is absent or not complete for the cut-off date | R-WO-02 holds the scan at `SCAN_HELD`, writes nothing and raises an incident; no message ID is named for the incident (GAP-3016) | None named | AC2, X6 |
| X4 | The tax criteria version is absent | R-WO-03 holds the scan at `SCAN_HELD`, writes nothing, and the scan resumes when the version is published | MSG-S7-001 | AC1, X6 |
| X5 | The rwb-case, rwb-source-data or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | None | AC1, X6 |
| X6 | The load is restored and the version published after a hold | R-WO-04 returns the scan to `SCAN_DUE` for the same cut-off date and the run proceeds once | None | AC2 |
| X7 | A repeated trigger for the same cut-off date and batch business date, or the same `Idempotency-Key` twice | One row set, one record and one answer per case; the repeat is counted and the key answers the run it created | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR4 |

X1 and X2 are the legacy exception paths carried onto the slice, X3 to X6 are the two holds and their recovery that JOB-16 names, and X7 to X8 are the once-per-cut-off trigger and the ACE and schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6013-CON, the rwb-case, rwb-source-data and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity name, the decision code per rule and the shape of the stage outcome are this story's choice; the rule, the messages, the screen state, the operation and the table columns are fixed |
| Valuable | The population of a month is proposed by rule with its decision recorded and the case moves in the service that owns it, so a pack reaches the committee without manual assembly |
| Estimable | One workflow step, one evaluator, one record write, one row writer, one case-move answer, four clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic case list, a synthetic batch status and synthetic balances through the contract fakes, plus the access, the two holds and the failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Run the monthly eligibility scan on both tracks

  Background:
    Given case "RC-2026-000701" is one of 210 open cases in state "SCAN_DUE" on the case list of the write-off stage
    Given the WO rule package is in force at its version and carries R-WO-01, R-WO-02, R-WO-03 and R-WO-04
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Run the monthly eligibility scan on both tracks (legacy RWB-E6-013 AC1)
    Given the rwb-source-data contract mock returns the ACE batch status of source ALS as "COMPLETED" with its business date and the balance of the 210 cases
    Given the rwb-case contract mock returns the case list of the write-off stage with 210 cases in state "SCAN_DUE"
    Given the rwb-decision contract mock returns the WO package at its version in force with the tax criteria version published
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then scans the portfolio each month against the eligibility rules and proposes the write-off population
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-01 (legacy RWB-E6-013 AC2)
    Given the rwb-case contract mock returns the case state "SCAN_DUE" for "RC-2026-000701" and accepts the move "POPULATION_PROPOSED"
    Given the rwb-source-data contract mock returns the ACE batch status of source ALS as "COMPLETED" for the cut-off date
    Given a case in state SCAN_DUE
    When monthly scan started
    Then test every open case against the eligibility rule on both tracks and the tax criteria
    Then the case moves to POPULATION_PROPOSED

  Scenario: AC3 Not recorded (legacy RWB-E6-013 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E6-013 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `its trigger arrives`, `monthly scan started` and `the action is taken`, and the two legacy Givens of AC2 all stand. The cross-service parts are mocked, so AC1 carries three `Given the <service> contract mock returns <x>` lines and AC2 one, and those are the only additions. What the legacy lines describe now happens in four places: rwb-case answers the case list and writes the move; rwb-source-data answers the ACE batch status that R-WO-01 tests and the balances; rwb-decision holds the package at its version with the tax criteria; and this story evaluates the rule, writes the record and the rows and answers the move. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it. Two points are recorded rather than smoothed over: MSG-S7-001 is the message of the R-WO-03 hold, which AC1 does not reach but which the story must build (ASM-5008); and `test ... on both tracks` is the rule's own sentence, whose two tracks are named by the route set's end states and by no other source (ASM-5007).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-01 | Write-off | D9 | SCAN_DUE | MONTHLY_SCAN_STARTED | cut_off_date reached and the ALS load is complete | Test every open case against the eligibility rule on both tracks and the tax criteria | POPULATION_PROPOSED | Write-off team | Rules component, COLLINS, ALS core and GL | monthly cut-off |
| R-WO-02 | Write-off | D9 | SCAN_DUE | ALS_LOAD_FAILED | the ALS extract is absent for the cut-off date | Hold the scan and raise an incident | SCAN_HELD | Write-off team | ALS core and GL | 1 working day |
| R-WO-03 | Write-off | D9 | SCAN_DUE | TAX_CRITERIA_UNPUBLISHED | tax_criteria_version absent | Hold the scan until Finance publishes the version | SCAN_HELD | Write-off team | Reference data, Finance provision feed | None |
| R-WO-04 | Write-off | D9 | SCAN_HELD | LOAD_RESTORED | the ALS extract is complete and the tax criteria published | Restart the scan for the cut-off date | SCAN_DUE | Workbench | Reference data | None |

The four rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: in the target the "Rules component" is the WO package read from rwb-decision (P7) and evaluated here, "COLLINS", "ALS core and GL" and the "Finance provision feed" are facts of the rwb-source-data products, "Reference data" is rwb-case's by default ruling, "Workbench" is SCR-27, and the case moves are written by rwb-case on this story's answer while the rows are written here.

| ID | Rule | Source |
|---|---|---|
| BR1 | The population is this service's: `write_off` is the one table of `rwb_writeoff`, and no other service writes it | Context pack ownership rows (table `write_off`); TSD S7 T3.1; FSD S7 A2.1.2 |
| BR2 | The decision is recorded before the rows change, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy AC1 and AC3 |
| BR3 | The ACE batch status and the balances stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes both on the owner's contract with their dates | DP-05 as a prohibition; FSD S7 A2.1.3.1; ASM-5004 |
| BR4 | The case move is answered and not written: `recovery_case` and the states `SCAN_DUE`, `POPULATION_PROPOSED` and `SCAN_HELD` are rwb-case's | ASM-4888; TSD S7 T4 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_writeoff`; `case_id` and `decision_log_id` are identifiers of other services' facts | DP-01; TSD S7 T3.3 |
| BR6 | Every value a business person may change is reference data or a rule row read with its version: the eligibility condition, the tax criteria, the cut-off date, the third working day of the month and the two tracks | FSD S7 A2.1.3.1, BR-S7-001; legacy Guardrails; TSD S7 T3.2 |
| BR7 | The two holds are states and not exceptions: R-WO-02 and R-WO-03 write nothing, and R-WO-04 restarts the same cut-off date once | TSD S7 T4; Batch and Scheduling Design v4, JOB-16 |
| BR8 | The same trigger twice, or the same `Idempotency-Key` twice, writes one row set, one record and one answer per case | TSD S7 T-A.2 |
| BR9 | No person name, address, contact value or identity number enters `rwb_writeoff`, the record, a log or a workflow input | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR10 | The write-off row carries the route state the rule names, `POPULATION_PROPOSED`, because no list of values for a write-off state exists | TSD S7 T3.2 (empty); ASM-5009 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the state of the step and the row it writes.

| From (step) | Event | Condition | To |
|---|---|---|---|
| Waiting | The Schedule fires for a cut-off date | The package in force is read | Reading the load |
| Reading the load | The ACE batch status is complete and the tax criteria version is published | R-WO-01 applies | Evaluating |
| Reading the load | The ALS extract is absent for the cut-off date | R-WO-02 | Held, `SCAN_HELD` answered, incident raised |
| Reading the load | `tax_criteria_version` is absent | R-WO-03 | Held, `SCAN_HELD` answered, MSG-S7-001 |
| Held | The load is restored and the version published | R-WO-04 | Reading the load, same cut-off date |
| Evaluating | R-WO-01 fires on the case | The decision record is written | Applying |
| Applying | The rows are written and the answers sent | The transaction commits | Waiting for the next cut-off date |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |

| From (`write_off.state`) | Event | Condition | To |
|---|---|---|---|
| None, no row | A proposal under R-WO-01 | The eligibility rule and the tax criteria pass | One row per case, state `POPULATION_PROPOSED` |
| None, no row | A hold under R-WO-02 or R-WO-03 | The load is incomplete or the version is absent | No row, no record and the answer `SCAN_HELD` |
| `POPULATION_PROPOSED` | The tax record of FEAT-WOF-02 | RWB-S7-E6014-APP | Unchanged: `tax_criteria_met` written there |
| `POPULATION_PROPOSED` | The pack step | RWB-S7-E6015-APP | `PACK_PREPARED`, written there |
| `POPULATION_PROPOSED` | A removal by the team | R-WO-07, RWB-S7-E6016-APP | `CASE_REMOVED_BY_TEAM`, written there |

The route states are those of the WRITEOFF machine of TSD S7 T4 and live on the case of record. `POPULATION_PROPOSED` is the only state this step writes, because no list of values publishes a write-off row state (BR10).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WRITEOFF, write-off team member | Write-off and posting CRU in TSD S7 T6.1 and right C of API-S7-001 in the legacy permission table: the primary role, running a scan and reading its population |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA and right C: runs a scan and re-runs a cut-off date |
| RW-PRODHEAD, RW-WOCOMM, RW-FINANCE | Write-off and posting RA: read the population; right A belongs to the committee stories, not to this one |
| RW-RISK, RW-COE, RW-CONDUCT, RW-AUDIT, RW-BIANAL, RW-TRIBE, RW-FRAUD, RW-DEBTSALE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Write-off and posting R as the matrix gives them: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Runs the Schedule and the step, reads the case list, the batch status, the balances and the package, writes the record and the rows and answers the moves; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S7 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the write-off team member as also-user (FSD S7 A2.1.3.3), and both statements hold: the step runs under the service identity with no officer task on the happy path, and the officer is the primary role when a person acts, on SCR-27 and on a re-run of a cut-off date. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Write, the write-off reference of the row and the case-move answer |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Write, from the case list of the cut-off date |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Write, the identifier the local decision record returns |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Write, from the balance on the rwb-source-data product with its as-of date (Source GL) |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Not written here: RWB-S7-E6014-APP; the required flag against a later write is a gap (ASM-5009) |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Not written here: RWB-S7-E6018-APP |
| DF-FIN-016 | write_off (S7, `rwb_writeoff`) | posted_date | Not written here: RWB-S7-E6021-APP |
| DF-FIN-017 | write_off (S7, `rwb_writeoff`) | responsibility_center | Not written here: RWB-S7-E6021-APP (Source GL) |
| DF-FIN-018 | write_off (S7, `rwb_writeoff`) | cost_center | Not written here: RWB-S7-E6021-APP (Source GL) |
| DF-FIN-019 | write_off (S7, `rwb_writeoff`) | gl_product | Not written here: RWB-S7-E6021-APP (Source GL) |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Write 0 at insert: nothing is recovered after charge-off before the charge-off exists; the value moves on RWB-S7-E6027-APP |
| Standard columns | write_off (S7, `rwb_writeoff`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, `state` = `POPULATION_PROPOSED`, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the rows change |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case list and the state arrive on the rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rule rows arrive on the package read |
| `v_ace_batch_status` (P1) | the ACE batch status and its business date | Not read: no `v_ace_*` grant. The field IDs are Not specified in the source documents (GAP-3016; ASM-5004) |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary, and the ACE and ledger rows are the rows the legacy Data table lists, with their owners changed to P1 and P7 by the target. **No new table, no new column and no migration**: `write_off` arrives with the DB story of this service, this story writes eight of its existing columns, and `decision_record` and `idempotency_key` are library objects created in `rwb_writeoff` by the library's own migration (DP-03).

**No personal data.** The rows carry identifiers, amounts, dates, a state and a rule version. No name, address, contact value or identity number enters `rwb_writeoff`, the record, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This story supplies the behaviour behind the run, whose shape RWB-S7-E6013-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-off-scans` | ScanRequest in, WriteOffScan of status 201 out, the run of the cut-off date with its eligible and held-out counts (API-S7-001) | Write-off and posting, right C, scope applied | `Idempotency-Key` header |

The errors are 401, 403 with MSG-P4-002, 409 for a repeated or conflicting run, 422 with MSG-GEN-001 for an invalid request and 503 when the library or a consumed contract does not answer, as TSD S7 T-A.2 gives them. `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) is RWB-S7-E6018-APP's and is neither built nor declared here.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use |
|---|---|---|---|
| The case-list read of the write-off stage (operation name Not specified in the source documents (GAP-3016; ASM-5004)) | `/api/recovery/case/v1` | P3 rwb-case | The open cases of the stage for a cut-off date: case reference, case number, product group, account link, state and balance key; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3016; ASM-4888)) | rwb-case (P3) | P3 rwb-case | The move `POPULATION_PROPOSED` or `SCAN_HELD` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The ACE batch status of source ALS, and the balance of the account (operation names Not specified in the source documents (GAP-3016; ASM-5004)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The status of the ALS load for the cut-off date with its business date, and the balance with the as-of date of the product; faked |
| The WO rule-package read in force (operation name Not specified in the source documents (GAP-3016; ASM-5005)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-01 to R-WO-04 among its 51 rules over 27 states and the tax criteria; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3016; ASM-5004).

#### 12.3 Events published

None. The service publishes on `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (event `EV-24`), which the approval story RWB-S7-E6018-APP publishes when the committee approves and rwb-payment consumes. The scan approves nothing, so this story declares no event, no producer group and no outbox row of its own, and a build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry for this key (ASM-5006).

#### 12.4 Events consumed

One subscription, and nothing else. The step listens for the ACE data-ready event of rwb-source-data for source ALS — the target form of `EV-26 AceDataReady`, whose consumer list in the monolith catalogue names "write-off scan (JOB-16)" — and uses it with the Schedule of §12.6 to decide whether the load is complete for the cut-off date. The event name follows the naming rule of §R4 and is published in no source document (GAP-3016; ASM-5006). The `ProceedsMatched` subscription of rwb-payment that the connection matrix gives row S7 belongs to the post-charge-off recovery story RWB-S7-E6027-APP and is not consumed here. Where the event does not arrive, the batch status is read on the contract of §12.2 and the scan holds under R-WO-02; the inbox library of DP-09 is the recorded missing H row.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case in the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` in namespace `rwb-recovery` | Input: the case, the route state and the package in force; signals: the monthly scan for a cut-off date, the AC batch answer and the later approval and deviation answers. This step sits at the head of the stage and needs no compensation |
| `runMonthlyScan` | Activity, the one scan step | `rwb-writeoff` | The cut-off date, the case list and the batch status in; the rule ID with its package version, the proposed and held-out cases, the row set and the case moves out, with the record and the rows written in one transaction |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice fixed by no source document.

#### 12.6 Schedules

One Temporal Schedule, per service and environment, replaces the legacy Quartz job JOB-16: it fires monthly on the third working day for the cut-off date and starts the scan activity on queue `rwb-writeoff` in namespace `rwb-recovery` (Batch and Scheduling Design v4, JOB-16; context pack ownership rows, jobs). The Schedule is DP-10 in fact; DP-10 is absent from this key's pattern set, so the kit row RWB-PLT-E1071-CON is recorded and not added to the metadata (ASM-5008). Its schedule ID, its hour and the definition of the third working day are Not specified in the source documents (GAP-3016; ASM-5008). The scan holds inside the run rather than skipping it, so a late batch or a late tax criteria version still produces the month's population.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of a case; this story inserts one row per proposed case and writes the columns of §11 |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `proceeds` (P8), and the later stories' data. **No table holds the scan itself**: the operation answers `id`, `cutOffDate`, `eligible`, `heldOut` and `status`, and the ownership rows give S7 one table, so the run is answered from the workflow run and its row set and the missing table or columns are a gap (GAP-3016; ASM-5009). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-list fake | The case list of the stage with 210 cases in `SCAN_DUE`, `RC-2026-000701` among them, with the balance key; a case that has left the list | AC1, AC2, X7 |
| rwb-source-data batch-status fake | The status of the ALS load as `COMPLETED` with its business date; an absent load; a load for another source | AC1, AC2, X3, X6 |
| rwb-source-data balance fake | The balance of the 210 cases with as-of date `2026-11-30`; a stale product with its date; no answer beyond 2 s | AC1, X5 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-01 to R-WO-04, the tax criteria version and the two tracks | AC1, AC2, X4 |
| rwb-case case-move fake | The moves `POPULATION_PROPOSED` and `SCAN_HELD` accepted for `RC-2026-000701`; a move refused because the case is not in the expected state | AC2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000701`, in its scan state | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows carry the placeholder until their owners confirm them (GAP-3016; ASM-5004, ASM-5005, ASM-4888).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `POST /write-off-scans` on `/api/recovery/writeoff/v1`; the case-list read, the case-move answer, the batch status and balance reads and the package read; one hop, 2 s |
| Kafka | 0 published, 1 consumed | No event of this step; the ACE data-ready event of rwb-source-data for source ALS (§12.4); `WriteOffApproved` is the approval story's |
| Temporal | 1 workflow and 1 activity, 1 Schedule | `WriteOffWorkflow`, `runMonthlyScan` and the JOB-16 Schedule on `rwb-writeoff` |
| File | None | No file is read, built or delivered here; JOB-16 produces no file |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `scan`; front end `src/modules/recovery/writeoff/WriteOffProposal.tsx`, the fragment SCR-27 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the `write_off` rows commit together or not at all. DP-13 moves the base of the one operation and nothing else. DP-19 is how SCR-27 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-05 (the ACE read), DP-09 (the outbox and inbox library) and DP-10 (the Schedule that replaces JOB-16) are real dependencies of this step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3016; ASM-5004, ASM-5005, ASM-5006, ASM-5008).

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The outbox and inbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed for the consumed ACE data-ready event. The Temporal schedule kit of DP-10 would add `RWB-PLT-E1071-CON`. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` scan head | Workflow | Waits for the Schedule and the batch answer, reads the package in force and reports the outcome to the parent |
| `runMonthlyScan` | Activity | Reads the batch status, the case list and the balances, evaluates R-WO-01 to R-WO-04, writes the record and the rows, answers the moves |
| `EligibilityEvaluator` | Service | The rule evaluation over the package in force, with the tax criteria, the two tracks and the no-fire path |
| `ScanHoldGuard` | Service | The two holds of R-WO-02 and R-WO-03 and the restart of R-WO-04 for the same cut-off date |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked; refuses the step when the write fails |
| `WriteOffRowWriter` | Repository | Inserts the rows in one `rwb_writeoff` transaction with the idempotency row and the optimistic lock |
| `CaseListClient` | Client | The case-list read of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `SourceDataClient` | Client | The ACE batch status and the balance of rwb-source-data with their dates and the stale path |
| `RulePackageClient` | Client | The package read of rwb-decision at its version in force |
| `CaseMoveAnswer` | Client | The case-move answer to rwb-case, one answer per case of the list |
| `WriteOffScanController` | Controller | The operation, the capability area and right, the `Idempotency-Key` and the problem mapping |
| `WriteOffProposal` | React component | Shows the population and the scan state on SCR-27, read only, with the hold and refusal states |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the record and idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the batch status, the case, the balance or the rule row: those are facts and rows of their owners and are referenced, not copied. The absent scan table of §12.7 is the recorded gap and is not created here.

**Configuration and reference data.**

- The eligibility condition, the tax criteria, the cut-off date, the third working day and the two tracks: rule rows of the package with their version, never written in code (ASM-5007, ASM-5008).
- The capability area "Write-off and posting" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the cut-off date of a run is a parameter of the operation and not a constant.

**Build steps**

1. The scan head of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the Schedule of §12.6 as its trigger.
2. `SourceDataClient` and `CaseListClient` against their fakes, with the 2 s budget, the breaker, the business date, the as-of date and the no-answer path (AC1, AC2, X3, X5).
3. `RulePackageClient` against its fake, with the version in force recorded with the outcome (AC1).
4. `ScanHoldGuard` and `EligibilityEvaluator` over the package, with R-WO-01 to R-WO-04, the tax criteria, the two tracks and the no-fire path (AC1, AC2, X3, X4, X6).
5. `WriteOffDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC3, X1).
6. `WriteOffRowWriter` with the one transaction, the row set, the idempotency row and the optimistic lock (AC1, X7).
7. `CaseMoveAnswer` with the two moves, one per case of the list (AC2).
8. `WriteOffScanController` with the rights, the `Idempotency-Key` and the problem mapping of the declared errors, and `WriteOffProposal` on SCR-27 through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_source_data` (X8, BR3, BR5).

**Feature flag.** `rwb.writeoff.scan-v1`, a flag of the platform library; off means the Schedule holds the run, writes nothing and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic batch status and case list in SIT, R-WO-01 proposes the population, R-WO-02 and R-WO-03 hold it with their messages and R-WO-04 restarts it, a repeated trigger writes once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-27 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The scan is held because `tax_criteria_version` is absent and Finance has not published the criteria version (X4, VR-S7-001-1) | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of the request or of the case list is absent or invalid (X5, X7) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right calls the operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the rows change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set and of FSD S7 A2.1.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The incident that R-WO-02 raises on the absent ALS load has no message ID in any source and is recorded as such (GAP-3016).

### 15. Screens and states

SCR-27 Write-off proposal, in its scan state, is served through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the population, its counts and its state, rwb-case for the case and its route state and rwb-source-data for the batch status and its business date; this story fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Scan; proposed; in committee; approved". The scan state is this story's: the proposed cases of the cut-off date, the held-out cases with their reason and the cut-off date itself. The proposed state belongs to RWB-S7-E6015-APP, the in-committee state to RWB-S7-E6017-APP and the approved state to RWB-S7-E6018-APP. The refusal, not-recorded and held states read the messages of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-013-01 | AC1 | Component | The 210-case list, the `COMPLETED` ALS load and the published tax criteria on the fakes; the row set, the record and the answers asserted with the package version |
| TC-E6-013-02 | AC2 | Component | Case `RC-2026-000701` at `SCAN_DUE`; the rule applied on both tracks and the `POPULATION_PROPOSED` move asserted on the fake |
| TC-E6-013-03 | AC3 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E6-013-04 | Access | Component | A role without the Write-off and posting right C; 403 with MSG-P4-002 and no read |
| TC-E6-013-05 | Principle 5 | Component | A forced decision log write failure inside the transaction; no `write_off` row and no case-move answer |

The five legacy cases are those of RWB-E6-013 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the eligibility condition, the tax criteria, the cut-off date, the third working day, the two tracks, the states and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, amounts, dates, a state and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR3).
- The case stays with rwb-case: no `recovery_case` row, no case route-state column and no case write here (BR4).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no Quartz job row, no shared job table, no monolith base, no data-lake extract and no event published by this step.
- The decision is recorded before the change; a build that writes a row outside the record's transaction fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S7-001 | Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks (FSD S7 Requirements served); the split plan carries no requirement id for this slice (GAP-3016) | The scan step, the `write_off` rows and the case move | TC-E6-013-01, TC-E6-013-02, TC-E6-013-05 |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the population | TC-E6-013-01 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-013-01 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The JOB-16 Schedule and the stage child workflow | TC-E6-013-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-E6-013-01, TC-E6-013-02 |
| ADR-022 | Local decision record plus central ledger | The record written before the change | TC-E6-013-03, TC-E6-013-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-013, disposition Split (rework); feature FEAT-WOF-01 |
| Legacy criteria | AC1, AC2 and AC3, owned word for word by this story |
| Source text | Legacy RWB-E6-013; FSD S7 Write-off and recovery v3 A2.1 and Requirements served; TSD S7 Write-off and recovery v2 T3, T4, T6 and T-A; Business Rules and Routing Logic v4 rows R-WO-01 to R-WO-04; Batch and Scheduling Design v4, JOB-16 |
| Test cases | TC-E6-013-01 to TC-E6-013-05 |
| Feature and screens | FEAT-WOF-01, SCR-27 Write-off proposal |
| Rules | R-WO-01, R-WO-02, R-WO-03 and R-WO-04, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the operation, the elements, the field IDs, the consumed rows, the error set and the fakes: RWB-S7-E6013-CON.
- The per-account tax criteria record of FEAT-WOF-02 and `tax_criteria_met`: RWB-S7-E6014-APP.
- The pack of FEAT-WOF-03: RWB-S7-E6015-APP. The removal of a case and R-WO-07: RWB-S7-E6016-APP.
- The committee routing and scheduling of FEAT-WOF-05: RWB-S7-E6017-APP. The approval, rejection and deferral, API-S7-002 and `WriteOffApproved` (EV-24): RWB-S7-E6018-APP.
- The posting, the provision release, the Finance feed, the reconciliation, the exception loop and the retention close: RWB-S7-E6021-APP to RWB-S7-E6025-APP, with the money in rwb-payment (P8).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3); the ACE batch status and the balance products: rwb-source-data (P1); the WO package and its rule rows: rwb-decision (P7).
- The scan table the operation implies: no source publishes one (ASM-5009).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
