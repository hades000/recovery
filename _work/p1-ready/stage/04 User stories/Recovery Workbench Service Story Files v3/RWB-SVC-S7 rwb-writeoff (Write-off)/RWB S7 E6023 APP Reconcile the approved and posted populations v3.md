# RWB-S7-E6023-APP Reconcile the approved and posted populations

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 P1 developer readiness (RD-P1 register). Set the GL/COMPLETED monthly trigger and cut-off gate. The posting-row read stays pending under GAP-3037. RD-P1-066.
- Start rule of `WriteOffWorkflow` / JOB-16: only the `AceDataReady` event with `sourceSystem` ALS and `status` COMPLETED counts; the event is published once per source system and business date (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-S7-E6023-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-023 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-K |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S7-E6023-APP-16) |
| Depends on (build) | RWB-S7-E6023-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | rwb-source-data posting product and its event (Not specified in the source documents (GAP-3037)), rwb-case and rwb-decision (class C; matching cross-reference Not specified in the source documents (GAP-3037)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-066 |

**Change log.** D-RCV-60, 22 November 2026: the reconciliation slice of legacy RWB-E6-023 written for rwb-writeoff, split from the contract baseline of the same key. The four legacy acceptance criteria are kept word for word with their origin tag. The comparison of the approved population with what the general ledger posted is now the reconciliation branch of `WriteOffWorkflow` on task queue `rwb-writeoff`: it evaluates R-WO-42 and R-WO-43 of the WO package, reads the monthly GL write-off postings on the rwb-source-data contract (INT-16, `v_ace_write_off`), records the result through the local decision-record library before `write_off` changes (DP-03), writes the WRITEOFF state `RETENTION_RUNNING` or `WRITEOFF_EXCEPTION` on the `write_off` row on the base `/api/recovery/writeoff/v1` (DP-13) behind the gateway-bff composite route (DP-19). The two operations of this key belong to RWB-S7-E6013-APP and to RWB-S7-E6018-APP to -E6020-APP, so this step provides none; the consumed contracts, the monthly trigger and the completeness publication are recorded as GAP-3037 with ASM-5083 to -9. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6023-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Credit Administration officer**, I want **the Workbench to compare what the committee approved to what was posted, and raise every difference**, so that **write-offs follow the criteria and the committee's decision**.

This is the reconciliation slice of legacy RWB-E6-023. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- the reconciliation branch of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case (context pack workflow row `WriteOffWorkflow`; Temporal and Drools Design slide 13, "Write-off · rwb-writeoff · WO 51");
- the evaluation of R-WO-42 (the populations agree) and R-WO-43 (they differ) on the posted population, with the WO package version in force, and the read of the approved-side facts the committee recorded under R-WO-13 and R-WO-15;
- the comparison of the approved population — `write_off` rows in `APPROVED` and `POSTED` in schema `rwb_writeoff` — with the posted population read from the monthly GL write-off postings through the rwb-source-data contract (INT-16, `v_ace_write_off`, DF-ACE-261 to DF-ACE-269), by count and amount, with the difference enumerated case by case;
- the local decision record of the period and of each difference, written through RWB-PLT-E1027-CON before the rows change (DP-03), which is what legacy AC1 and AC4 require;
- the WRITEOFF transition of `write_off.state` from `POSTED` to `RETENTION_RUNNING` (R-WO-42) or `WRITEOFF_EXCEPTION` (R-WO-43), with `write_off.decision_log_id` and the retention entry signalled to rwb-case, the timer from this entry being RWB-S7-E6025-APP's;
- the answer to rwb-case for the case move and the retention timer, and the exception hand-off to RWB-S7-E6024-APP.

It does not own: the published shapes of the `write_off` element, the state vocabulary, the consumed rows, the rights, the error set and the fakes, which are RWB-S7-E6023-CON; the scan, the tax criteria and JOB-16, which are RWB-S7-E6013-APP and RWB-S7-E6014-APP; the pack, which is RWB-S7-E6015-APP; the committee act that produced `APPROVED`, which is RWB-S7-E6018-APP to RWB-S7-E6020-APP; the posting to ALS and the ledger that produced `POSTED`, which is RWB-S7-E6021-APP; the provision feed, which is RWB-S7-E6022-APP; the exception loop, which is RWB-S7-E6024-APP; the retention expiry and the case closure, which are RWB-S7-E6025-APP; the case of record and its route states, which are rwb-case's (P3); the GL postings and their ACE views, which are ACE's and rwb-source-data's (P1); the rule package and the ledger, which are rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E6-023 gave the Workbench one step that compared what the committee approved to what was posted and raised every difference, so that write-offs follow the criteria and the committee's decision. The FSD keeps the objective unchanged — "Compares what the committee approved to the GL postings read through v_ace_write_off, and raises every difference" (FSD S7 A2.11.2; Epics 3 to 8 Specification v3, FEAT-WOF-11) — against the module metric "write-off packs accepted first time, rising each month", measured on the decision log and the Workbench records and reviewed monthly. The problem is unchanged: write-off populations are assembled by hand each month. The rule that makes the step measurable is REC-06 of the data quality set: write-offs approved in the Workbench against the postings in `recovery.v_ace_write_off`, by count and amount, tolerance zero, monthly, owned by Credit Administration.

What D-RCV-60 changes is where each population and the decision live:

- **the approved population is this service's.** `write_off` is S7's only table, in `rwb_writeoff` (context pack ownership row; TSD S7 T3.1, DF-FIN-010 to DF-FIN-020), so the approved amount, the committee date, the posting date and the record reference are read here and the state is written here.
- **the posted population is not this service's.** The GL write-off postings are ACE data landed by INT-16 into `gl_write_off` and read through `v_ace_write_off` (DF-ACE-261 to DF-ACE-269; LDM v8). In the target only rwb-source-data reads the `v_ace_*` views (Architecture v5 slide 8), so this story reads the monthly product on the rwb-source-data contract and holds no view grant. DP-05 would normally carry that read and is not in this story's pattern set, so the dependency is recorded rather than claimed (GAP-3037; ASM-5084).
- **the case, its route state and the retention timer are not this service's.** `recovery_case`, `route state` and `timer` are rwb-case's (P3); the legacy Data table names `recovery_case` and this story reads the state on the contract and answers the move and the retention start.
- **the rule package and the ledger are not this service's.** The 51 rules over 27 states are governed in rwb-decision (P7) and read here at their version; the ledger entry is P7's, and this service keeps the local decision record of DP-03 (ASM-5086).
- **the step provides no operation of its own.** The two operations the legacy story lists are the scan (API-S7-001) and the committee decision (API-S7-002), which the split gives to RWB-S7-E6013-APP and to RWB-S7-E6018-APP to -E6020-APP. Reconciliation is a workflow step on the monthly posting product, so DP-13 moves the base of the key's operations and adds none here, and DP-19 has no provided read of its own for SCR-27 (GAP-3037; ASM-5089).
- **the step publishes no event.** The service's event EV-24 `WriteOffApproved` is the committee's approval, and no source catalogues a completeness event; the completeness result is available to rwb-reporting, whose read model is built from events (DP-17, ADR-018) (ASM-5088).

The binding values are unchanged and are not written in code: the count-and-amount tolerance, the audit period, the retention class and the state list are rows of the package, of reference data and of parameters, read with their version.

The delivery is the plan's: this key is EP06 and therefore wave 4, and rwb-writeoff is created in wave 4 (Architecture v5), so the two agree and the release 30 April 2027 is copied unchanged and marked tentative (ASM-5090).

### 3. Preconditions

- RWB-S7-E6023-CON is published: the `write_off` element, the WRITEOFF state vocabulary, the rejected-posting state, the consumed rows, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-source-data contract is available for the fake: the monthly GL write-off posting product (INT-16) with `write_off_key`, `account_key`, `amount`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product`, `source_system` and `data_as_of` (DF-ACE-261 to DF-ACE-269). Pending: the monthly GL posting-row read, owner P1 contract owner with the rwb-writeoff owner, tracked as GAP-3037. Build against the posting-row fake.
- The cross-reference that matches a `write_off` row to a GL posting is available from rwb-source-data or from a column of this service; no source publishes it, and it is Not specified in the source documents (GAP-3037; ASM-5085).
- The rwb-case read of the case state and the case-move answer are available for the fake, with the moves `RETENTION_RUNNING` and `WRITEOFF_EXCEPTION` and the retention start; the operation name is Not specified in the source documents (GAP-3037; ASM-5087).
- The rwb-decision WO package read is available for the fake: R-WO-13, R-WO-15, R-WO-42 and R-WO-43 at their version; the operation name is Not specified in the source documents (GAP-3037; ASM-5086).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 Write-off proposal reaches this service and rwb-case through the gateway-bff composite route, one hop each (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case.recovery_case`, `rwb_decision.rule_row` or `recovery.v_ace_write_off` is refused by the database and fails the boundary test (DP-01, DP-02).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6023-CON when its tests pass.

### 4. Flow

1. The rwb-writeoff consumer uses one group on rwb.source-data.events.v1. Only rwb.source-data.AceDataReady.v1 (EV-26) with sourceSystem GL, status COMPLETED and businessDate on or after the audit period’s cut-off date starts the monthly branch. Its data members are sourceSystem, businessDate, status and completedAt; its record key is {sourceSystem}:{businessDate}. The monthly GL postings land through INT-16. The branch runs on task queue rwb-writeoff and takes the audit period and cut-off from the audit-period context.
2. The branch loads the `write_off` rows of the period in `rwb_writeoff` in state `APPROVED` or `POSTED`, with `amount`, `committee_date`, `posted_date`, the three GL columns and `decision_log_id`; these rows are the approved population.
3. It reads the WO package version in force from rwb-decision with R-WO-13, R-WO-15, R-WO-42 and R-WO-43 and the count-and-amount tolerance.
4. It reads the posted population on the rwb-source-data contract, one hop with a 2 s budget and a breaker: the GL postings of the period with their `data_as_of`, which must be the current business date (VR-S7-011-1).
5. `WriteOffReconciliationEvaluator` builds both sides — the approved count and amount from the final calls recorded under R-WO-13 and R-WO-15 with the approver and the limit applied, and the posted count and amount from the GL postings — and matches them on the write-off reference and the account key. The approved amount is `write_off.amount`; the posting date is `write_off.posted_date` against the `posted_date` of the GL postings read in step 4.
6. It compares count and amount inside the tolerance in force. Equality fires R-WO-42; a difference fires R-WO-43, and the difference is enumerated case by case with the write-off reference, the approved amount, the posted amount and the gap.
7. `WriteOffDecisionRecordWriter` writes one decision record for the period and one for each difference through the local decision-record library, **before any change**, with the two counts, the two amounts, the rule ID and its version, the package version, the inputs reference and the outcome. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. `WriteOffReconciliationWriter` updates each `write_off` row of the period in one `rwb_writeoff` transaction with the record, the idempotency row and the optimistic lock of `version`: `state` becomes `RETENTION_RUNNING` under R-WO-42 or `WRITEOFF_EXCEPTION` under R-WO-43, and `decision_log_id` (DF-FIN-012) holds the identifier the library returns. `committee_date`, `posted_date` and the three GL columns are not written here.
9. `CaseMoveAnswer` answers rwb-case with the move `RETENTION_RUNNING` or `WRITEOFF_EXCEPTION`, the rule ID, the version, the decided-at time and the retention class; rwb-case writes the case of record, and the retention timer from this entry is started by RWB-S7-E6025-APP under R-WO-47.
10. On R-WO-43 the exception list is handed to RWB-S7-E6024-APP with the reason `POPULATION_NOT_RECONCILED`; this step raises the exception and does not work it.
11. A repeated product for the same period and the same tolerance writes nothing, sends no second move and no second exception, and counts the repeat.
An ALS event, an AceDataLate event or a GL event before the audit cut-off does not start the monthly branch (RD-P1-066).
The replay check uses the existing period-and-tolerance result, so a repeat produces no second record, case move or exception.
12. The completeness result of the period is published from rwb-reporting (section 12.3), fed by the decision record and the WriteOffApproved event, with no extract to a data lake and no Power BI copy (ADR-018), and is available to SCR-27 in its approved and reconciled states through the gateway-bff composite route (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing is written: no state, no record reference, no case move and no exception | MSG-P7-003 | AC4, TC-E6-023-04, TC-E6-023-06 |
| X2 | The role does not hold the Write-off and posting right of the read | 403 before any read, and the screen refuses the action | MSG-P4-002 | AC5, TC-E6-023-05 |
| X3 | A write-off of the period is not in `POSTED`, or the period has no approved row | The row is skipped and counted; nothing is written for it and no difference is raised | None | AC1, AC9 |
| X4 | The posting product is stale after a late or failed ACE batch (VR-S7-011-1) | The branch holds the period: no comparison, no state change and no exception | MSG-P1-001 | AC1, TC-E6-023-01 |
| X5 | The posting product carries a write-off reference that matches no `write_off` row, or a `write_off` row has no posting | The posting is counted as a difference under R-WO-43 with the unmatched key, and the record names it; nothing is posted and nothing is deleted | None | AC1, AC2 |
| X6 | The amount of a posting equals the approved amount but the count differs, or the reverse | R-WO-43 fires: the comparison is count and amount together, and the record names which side differs | None | AC1, AC3 |
| X7 | The rwb-source-data, rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The branch waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 | None | AC1, AC2, AC3 |
| X8 | The same product arrives twice for the same period and tolerance | One record set, one update and one move; the repeat is counted | None | AC1, AC11 |
| X9 | A component, a statement or a test reaches another service's schema or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC6, TC-E6-023-07 |

X1 to X3 are the exception paths of RWB-E6-023 carried onto the split, X4 to X8 are the paths the posting read, the tolerance and the call types add, and X9 is the DP-01, DP-02 boundary. The tolerance of X6, the audit period and the retention class are values in force in the package and in reference data, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6023-CON, the rwb-source-data, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity name, the decision code and the shape of the reconciliation result are this story's choice; the rules, the messages, the screen, the state values and the `write_off` columns are fixed |
| Valuable | Every period ends with a reconciled population or a named difference list, recorded once, and the retention clock starts only on a population that agrees |
| Estimable | One workflow branch, one comparator, three clients, one record write, one row update, one case-move answer and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic postings and write-offs through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Reconcile the approved and posted populations

  Background:
    Given the audit period "2027-04" is closed and its GL write-off postings have landed in ACE
    Given write-off "WO-2027-000318" of case "RC-2027-000712" is in state POSTED with its approval recorded
    Given the WO rule package is in force at its version and carries R-WO-13, R-WO-15, R-WO-42 and R-WO-43
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Reconcile the approved and posted populations (legacy RWB-E6-023 AC1)
    Given the rwb-source-data contract mock returns the GL write-off postings of "2027-04" with data_as_of at today's business date
    Given the rwb-decision contract mock returns the WO package in force with R-WO-42 and R-WO-43 and the count-and-amount tolerance
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then compares what the committee approved to what was posted, and raises every difference
    Then the system writes the result to the local decision record with the rule version

  Scenario: AC2 Rule R-WO-13 (legacy RWB-E6-023 AC2)
    Given the rwb-case contract mock returns the case state "ESCALATED_TO_CREDIT_COMMITTEE" for "RC-2027-000712"
    Given the rwb-case contract mock accepts the move "APPROVED" for the credit committee approval
    Given the rwb-decision contract mock returns R-WO-13 with the delegation limit of the credit committee with Risk
    Given a case in state ESCALATED_TO_CREDIT_COMMITTEE
    When credit committee approved
    Then record the final call and release the case to posting
    Then the case moves to APPROVED

  Scenario: AC3 Rule R-WO-15 (legacy RWB-E6-023 AC3)
    Given the rwb-case contract mock returns the case state "WITH_COMMITTEE" for "RC-2027-000712"
    Given the rwb-case contract mock accepts the move "APPROVED" for the committee approval
    Given the rwb-decision contract mock returns R-WO-15 with the write-off committee limit applied
    Given a case in state WITH_COMMITTEE
    When committee approved
    Then record the final call, the approver and the limit applied, and release to posting
    Then the case moves to APPROVED

  Scenario: AC4 Not recorded (legacy RWB-E6-023 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Access to the reconciliation result (X2) (new, D-RCV-60)
    Given the role of the reader does not hold the Write-off and posting right of the read
    When the reconciliation result is requested
    Then the request is refused with 403 before any read and the screen refuses the action
    Then the user sees MSG-P4-002

  Scenario: AC6 Boundary of the service schema (X9) (new, D-RCV-60)
    Given the build is tested for statements and reads outside rwb_writeoff
    When the boundary test runs
    Then the build fails on any statement outside rwb_writeoff or any v_ace_* read and nothing is released

  Scenario: AC7 No personal data (BR11) (new, D-RCV-60)
    Given the decision record, a log and a workflow input of the step are written for a period
    When the step writes them
    Then no person name, contact value or identity number is in any of them

  Scenario: AC8 A consumed call fails or does not answer (X7) (new, D-RCV-60)
    Given the rwb-source-data contract mock does not answer inside 2 s
    When the reconciliation step reads the posted population
    Then the branch waits and retries on the workflow's own schedule
    Then nothing is written and the caller receives the failure outcome Not specified in the source documents (NEWAC-RWB-S7-E6023-APP-AC10)

  Scenario: AC9 A write-off not in POSTED is skipped (X3) (new, D-RCV-60)
    Given a write-off of the period is in state RETENTION_RUNNING
    When the reconciliation step reaches the write-off
    Then the row is skipped and counted; nothing is written for it and no difference is raised

  Scenario: AC10 Business rules BR1 to BR11 hold (new, D-RCV-60)
    Given the reconciliation step runs for one audit period
    When the step reads, compares, records and writes
    Then the approved population is read from rwb_writeoff, the posted population only through the rwb-source-data contract, and no other service schema or v_ace_* view is read
    Then the tolerance, the audit period and the state list are read as reference data with their version, and no person name, contact value or identity number is written

  Scenario: AC11 Duplicate delivery of a consumed event (X8, BR10) (new, D-RCV-60)
    Given the same posting product for one period and the same tolerance has been consumed once
    When the same product is delivered again
    Then nothing is written, no second case move and no second exception are sent, and the repeat is counted

  Scenario: AC12 Activity retry and timeout (NEWAC-RWB-S7-E6023-APP-AC9) (new, D-RCV-60)
    Given the rwb-source-data contract mock answers a retried call only after the first attempt has timed out
    When the reconciliation activity is retried by the workflow
    Then the activity is retried on the workflow's own schedule and the retry writes nothing twice
    Then a final timeout ends in the failure outcome of AC8 and nothing is written
```

The four criteria are the legacy criteria of RWB-E6-023 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `its trigger arrives`, `credit committee approved`, `committee approved` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 carries two `Given the <service> contract mock returns <x>` lines and AC2 and AC3 carry three each; those added lines are the only additions. What the legacy lines describe now happens in three places: rwb-source-data owns the GL postings and the product that carries them, rwb-case owns the case state and the move, and rwb-decision owns the WO package and the limits it carries, while this story compares the two populations, records the result and writes `state` and `decision_log_id` on the `write_off` row. Legacy AC2 and AC3 are the approval transitions R-WO-13 and R-WO-15, which are the act of RWB-S7-E6018-APP; they are owned here word for word because the legacy feature block carries them, and this step reads the `APPROVED` state, the final call, the approver and the limit applied that they produce as the approved side of the comparison (ASM-5083). Legacy AC1's "decision log" is read as the local decision record of DP-03 written before the rows change, plus the ledger entry P7 writes (ASM-5086).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-13 (BR12) | Write-off | D9 | ESCALATED_TO_CREDIT_COMMITTEE | CREDIT_COMMITTEE_APPROVED | approved inside the delegation with Risk | Record the final call and release the case to posting | APPROVED | Credit Administration | Committee View, Decision Log | None |
| R-WO-15 (BR13) | Write-off | D9 | WITH_COMMITTEE | COMMITTEE_APPROVED | approved inside the delegation | Record the final call, the approver and the limit applied, and release to posting | APPROVED | Credit Administration | Committee View, Decision Log | None |
| R-WO-42 (BR14) | Write-off | D9 | POSTED | POPULATION_RECONCILED | approved count and amount equal posted count and amount | Publish completeness and start the retention timer | RETENTION_RUNNING | Workbench | Rules component, Power BI, Workbench scheduler | monthly |
| R-WO-43 (BR15) | Write-off | D9 | POSTED | POPULATION_NOT_RECONCILED | approved and posted populations differ | Fire the exception and report completeness short | WRITEOFF_EXCEPTION | Owner to confirm with C&R | Rules component, Power BI | to confirm with Credit Administration |

The four rows are the rows of the Business Rules and Routing Logic v4, copied character for character with the BR ID added in the Rule cell, and they are the rows of the WRITEOFF machine of TSD S7 T4. R-WO-13 and R-WO-15 are read here as the approved side of the comparison and are taken by RWB-S7-E6018-APP; R-WO-42 and R-WO-43 are this story's. The owner column is a role of the business and not a service: this step runs under the service identity on behalf of Credit Administration (REC-06), answers the case move to rwb-case, and the "Power BI" of the two rows is read under DP-17 as the reporting read model of rwb-reporting, with no data lake (ADR-018). R-WO-42's "start the retention timer" is read as the retention entry this step signals, whose timer RWB-S7-E6025-APP starts from both entries (ASM-5087).

| ID | Rule | Source |
|---|---|---|
| BR1 | The approved population is this service's: `write_off` rows in `APPROVED` and `POSTED` in `rwb_writeoff`, with the approved amount, the committee date and the record reference, and no other service writes them | Context pack ownership row `write_off`; TSD S7 T3.1; DP-01 |
| BR2 | The posted population is ACE data: the GL postings of INT-16 are read through `v_ace_write_off` on the rwb-source-data contract, and this service holds no `v_ace_*` grant | Architecture v5 slide 8; LDM v8 DF-ACE-261 to DF-ACE-269; DP-01, DP-05 (recorded); ASM-5084 |
| BR3 | The comparison is count and amount for the period, inside the tolerance in force; no count, amount or tolerance is a constant of the build | REC-06 of the Data Quality and Reconciliation Rules v4; R-WO-42 and R-WO-43 |
| BR4 | The decision is recorded before any `write_off` row changes, with the rule ID and the package version; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy AC1 and AC4 |
| BR5 | Only the two reconciliation outcomes are written here: `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product` and `recovered_after` keep their values until their own stories write them | TSD S7 T3.1; ASM-5087 |
| BR6 | The case, its route state and the retention `timer` row stay with rwb-case: this service reads the state, answers the move and asks for the retention start, and writes no `recovery_case` row and no timer row | Context pack ownership rows; legacy Data table; ASM-5087 |
| BR7 | The rule package, its version and the ledger stay with rwb-decision: this service reads the package in force and writes its local decision record, and no rule row and no ledger entry of its own | DP-03; ASM-5086 |
| BR8 | No cross-schema join and no foreign key leaves `rwb_writeoff`; the case reference and the posting key are identifiers of other services' facts | DP-01, DP-02; TSD S7 T3.3 |
| BR9 | Every value a business person may change is reference data, a parameter or a rule row read with its version: the tolerance, the audit period, the retention class and the state list | FSD S7 A2.11.3.1 BR-S7-011; Template and Rules v1 §R3 default rulings |
| BR10 | The same product twice, or the same `Idempotency-Key` twice, writes once and answers the case move once | TSD S7 T-A.2; Architecture v5 slide 11 |
| BR11 | No person name, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input; the populations are handled by reference and amount | Template and Rules v1 §R7.2 (s17); context pack naming rule on PII |
| BR12 | R-WO-13 of the rule table: the approved case moves to APPROVED on the delegation with Risk, read here as the approved side (ASM-5083) | Business Rules and Routing Logic v4; R-WO-13 |
| BR13 | R-WO-15 of the rule table: the committee approval moves to APPROVED with the approver and the limit applied, read here as the approved side (ASM-5083) | Business Rules and Routing Logic v4; R-WO-15 |
| BR14 | R-WO-42 of the rule table: approved and posted populations equal in count and amount, completeness is published and the retention entry is signalled | Business Rules and Routing Logic v4; R-WO-42 |
| BR15 | R-WO-43 of the rule table: the populations differ, the exception fires and completeness is reported short | Business Rules and Routing Logic v4; R-WO-43 |

Coverage: AC1 and TC-E6-023-01 cover BR1, BR2, BR3, BR9, BR10, BR14 and BR15; AC1, AC4, TC-E6-023-04 and TC-E6-023-06 cover BR4 and BR7; AC2, AC3, TC-E6-023-02 and TC-E6-023-03 cover BR5, BR6, BR12 and BR13; AC6 and TC-E6-023-07 cover BR2 and BR8; AC7 and TC-E6-023-08 cover BR11; AC10 and TC-E6-023-11 cover BR1 to BR11.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR6). What this story writes is the WRITEOFF state of the `write_off` row.

| From (WRITEOFF, `write_off.state`) | Event | Condition | To |
|---|---|---|---|
| `POSTED` | `POPULATION_RECONCILED` under R-WO-42 | approved count and amount equal posted count and amount | `RETENTION_RUNNING`, with the record written, the retention entry signalled and the completeness recorded |
| `POSTED` | `POPULATION_NOT_RECONCILED` under R-WO-43 | approved and posted populations differ inside the enumerated difference list | `WRITEOFF_EXCEPTION`, with the record written and the exception handed to RWB-S7-E6024-APP |
| `APPROVED` or `POSTED` | The monthly product | The posting product is stale, or no posting matches the row | Unchanged; the row is counted in the difference list, not moved |
| Any other state | The monthly product | X3 | Unchanged, the skip is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The posting product of the period arrives | The package in force is loaded | Comparing |
| Comparing | R-WO-42 or R-WO-43 is decided on the two populations | The outcome is `RETENTION_RUNNING`, or `WRITEOFF_EXCEPTION` with the difference list | Applying |
| Applying | The records, the `write_off` rows and the case move are written | The transaction commits | Waiting for the next period |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |

`APPROVED` and `POSTED` are produced before this step by R-WO-13 and R-WO-15 (RWB-S7-E6018-APP) and by R-WO-20 to R-WO-22 (RWB-S7-E6021-APP); this story reads both and moves neither backwards. The 27 states of the WRITEOFF machine are those of TSD S7 T4; no published list of case route states exists for the write-off route, so the case-side values are read from rwb-case on its contract and the two story-side values are the WRITEOFF states (ASM-5087).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| None; runs unattended | Primary user of the step (FSD S7 A2.11.3.3): the monthly comparison runs under the service identity |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA in TSD S7 T6.1, and the owner role of REC-06: reads the reconciliation result and the difference list |
| RW-PRODHEAD, product head | Write-off and posting RA: reads the reconciliation result |
| RW-WOCOMM, write-off committee member | Write-off and posting RA: reads the reconciliation result of the population it approved |
| RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: reads the reconciliation result and the completeness of the period |
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: reads the difference list; its C right is exercised on the scan story |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Write-off and posting R or U: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Runs the branch, compares, writes the records and the `write_off` rows, answers the case move and raises the exception; no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S7 T6.1 and the two rows of the legacy Permission checks table, and nothing wider. The legacy table gives the A right to RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and the C right to RW-WRITEOFF and RW-CREDITAD; no role of this story exercises the A right, because the step is unattended and takes no committee act. FSD S7 A2.11.3.3 names "None; runs unattended" as the primary user and "Credit Administration officer" as the other user, which is the reading used here. DP-08 is not in this story's pattern set: the capability area and the right are declared per read and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference the comparison and the record carry |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, the case reference the move carries |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Write, the identifier the local decision-record library returns (ASM-5086) |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the approved amount of the comparison |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, the tax criteria result of RWB-S7-E6014-APP |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Read, the approval date of the approved side; written by RWB-S7-E6018-APP |
| DF-FIN-016 | write_off (S7, `rwb_writeoff`) | posted_date | Read, matched against the posting date of the GL row; written by RWB-S7-E6021-APP |
| DF-FIN-017, DF-FIN-018, DF-FIN-019 | write_off (S7, `rwb_writeoff`) | responsibility_center, cost_center, gl_product | Read, the three GL keys matched against the posting |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Read, the recovery to date of the posted write-off |
| Standard columns | write_off (S7, `rwb_writeoff`) | `state`, `version`, `updated_at`, `updated_by` | Write `state`, the record reference, `updated_at`, `updated_by` and the optimistic lock on the update |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the `write_off` rows change |
| DF-ACE-261 to DF-ACE-269 | v_ace_write_off (ACE, read by P1) | write_off_key, account_key, amount, posted_date, responsibility_center, cost_center, gl_product, source_system, data_as_of | Not read as a view: the posted population arrives on the rwb-source-data contract (GAP-3037; ASM-5084) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the rest | Not read as a table: the case state arrives on the rwb-case read and the move is answered (GAP-3037) |
| DF-WRK-027 to DF-WRK-036 | timer (P3) | id, case_id, timer_type, started_at, expires_at and the rest | Not written here: the retention start is answered to rwb-case, which owns the timer row (ASM-5087) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7) | id, case_id, decision_code, rule_id, rule_version and the rest | Not written here: P7 writes the ledger entry; this service keeps the local record |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, from_state, event_code and the rest | Not read as a table: the rule rows are governed in rwb-decision and loaded here as the package in force |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `write_off` arrives with the DB story of this service, this story writes two of its existing columns, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_writeoff` by the library's own migration (DP-03).

**Personal data.** The rows this story writes carry identifiers, amounts, a code and a rule version: the identifiers are classed Not personal, and the amounts, dates and GL keys are classed Customer data (Data Classification and Personal Data Inventory v5, DF-FIN-010 to DF-FIN-020; section 17). No name, address, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

Contract version: the `/v1` base path of each contract in this section; no further contract version is specified in the source documents (DOR-RWB-S7-E6023-APP-23).

#### 12.1 REST operations provided

None. Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). The two operations of this legacy key are declared by other stories of the same service: `POST /write-off-scans` (API-S7-001, Write-off and posting right C) is RWB-S7-E6013-APP's, and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A) is RWB-S7-E6018-APP's with the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP. Reconciliation is a workflow step on the monthly posting product, so this story provides no operation; a build that declares one here fails the absence test of the contract (GAP-3037; ASM-5089). The reconciliation report read behind SCR-27 is Not specified in the source documents (GAP-3037; ASM-5089).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The monthly GL write-off posting product read (operation name Not specified in the source documents (GAP-3037; ASM-5084)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The GL postings of INT-16 for the period: write-off key, account key, amount, posted date, the three GL keys, source system and data as of (DF-ACE-261 to DF-ACE-269); faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the stage the write-off belongs to; read only, faked |
| The case-move answer with the retention start (operation name Not specified in the source documents (GAP-3037; ASM-5087)) | rwb-case (P3) | P3 rwb-case | The move `RETENTION_RUNNING` or `WRITEOFF_EXCEPTION` with the rule ID, its version and the retention start; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The read of the WO rule package version in force (operation name Not specified in the source documents (GAP-3037; ASM-5086)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows R-WO-13, R-WO-15, R-WO-42 and R-WO-43 with the tolerance; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter, a breaker per downstream and no retry of its own (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3037 with ASM-5084, ASM-5086 and ASM-5087.

#### 12.3 Events published

None. The service owns event EV-24 `WriteOffApproved` on topic `rwb.writeoff.events.v1`, and it is the committee's approval, which RWB-S7-E6018-APP publishes. No source catalogues a completeness event, so "publish completeness" (R-WO-42) is delivered as the reconciliation result recorded in the decision record and available to rwb-reporting, and the event or read that would carry it to P9 is Not specified in the source documents (GAP-3037; ASM-5088). This step writes no outbox row and fails the absence test if it adds an event.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 (EV-26) | rwb.source-data.events.v1 | P1 rwb-source-data | The rwb-writeoff consumer uses one group on rwb.source-data.events.v1. Only rwb.source-data.AceDataReady.v1 (EV-26) with sourceSystem GL, status COMPLETED and businessDate on or after the audit period’s cut-off date starts the monthly branch. Its data members are sourceSystem, businessDate, status and completedAt; its record key is {sourceSystem}:{businessDate}. |

One consumer group on `rwb-writeoff`, CloudEvents envelope, inbox row in `rwb_writeoff` and the retry and `.dlt` topics of the service (DP-09 recorded, not claimed). No second event is consumed: the case and the package arrive on their owners' contracts.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case per stage, the stage child of `CaseWorkflow` | `rwb-writeoff` (namespace Not specified in the source documents (CG-ALL-11109)) | Input: the case, the write-off, the audit period and the package in force; signals: the posting product, the case state and the package answer |
| `WriteOffWorkflow` | Workflow branch (reconciliation step of the same workflow), the step from the posted population to `RETENTION_RUNNING` or `WRITEOFF_EXCEPTION` | `rwb-writeoff` | Applies R-WO-42, or R-WO-43 with the difference list, writes the records and the rows, answers the case move and reports the stage outcome to the parent |
| `reconcilePopulations` | Activity, the one step of this story | `rwb-writeoff` | The two populations and the package answer in; the counts, the amounts, the difference list, the state, the record references and the case move out, in one transaction |

No child workflow of this service exists in this step: the retention timer that R-WO-42 signals is RWB-S7-E6025-APP's, started from this entry under R-WO-47, and its expiry is that story's. The activity name is a target design choice of this story and is fixed by no source document; the trigger is read as the arrival of the monthly posting product for the open period.

Workflow ID form and start rule: Not specified in the source documents (CG-ALL-11110). Temporal Catalog v1 gives the trigger of `WriteOffWorkflow` as 'JOB-16 on the third working day after AceDataReady (R-WO-01)' (counted only for the event with `sourceSystem` = `ALS` and `status` = `COMPLETED`, RD-P1-040) and no ID form, start mode or duplicate-start policy.

#### 12.6 Schedules

None. The rwb-writeoff consumer uses one group on rwb.source-data.events.v1. Only rwb.source-data.AceDataReady.v1 (EV-26) with sourceSystem GL, status COMPLETED and businessDate on or after the audit period’s cut-off date starts the monthly branch. Its data members are sourceSystem, businessDate, status and completedAt; its record key is {sourceSystem}:{businessDate}. JOB-16 is the separate monthly scan of RWB-S7-E6013-APP.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; this story reads it as the approved population and updates `state` and `decision_log_id` |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the period and of each difference (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated product and the outcome it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Created in this schema by the library and used by the stories that publish; this step writes no row of it (12.3) |

Not owned and never read as a table: `recovery_case`, `timer` and `queue` (P3), `rule_row` and `decision_log_entry` (P7), `proceeds` (P8), `document` (P5) and every `v_ace_*` view including `v_ace_write_off` (P1). No foreign key leaves the schema and `write_off.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data postings fake | The GL postings of `2027-04` with `data_as_of` at today's business date, the same product dated stale, a product with an unmatched write-off key, and no answer beyond 2 s | AC1, X4, X5, X7 |
| rwb-case state fake | The states `APPROVED`, `POSTED`, `POSTING_REJECTED` and `RETENTION_RUNNING` of case `RC-2027-000712`; a case in a state the rule does not name | AC2, AC3, X3 |
| rwb-case case-move fake | The moves `APPROVED`, `RETENTION_RUNNING` and `WRITEOFF_EXCEPTION` accepted with the retention start, and a move refused because the case is not in the state the rule expects | AC2, AC3, X3 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-13, R-WO-15, R-WO-42 and R-WO-43, the delegation limits and the tolerance above and below the difference | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for write-off `WO-2027-000318`, with the write-off facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished names of the posting product, the case move and the package read are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3037).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The rwb-source-data posting product, the rwb-case state read and move answer, and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 1 consumed | The GL/COMPLETED AceDataReady event on `rwb.source-data.events.v1`; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 1 activity | `WriteOffWorkflow` and its reconciliation branch on `rwb-writeoff`, with its `reconcilePopulations` activity; no Schedule and no child workflow |
| File | None | The monthly GL file of INT-16 is received by ACE ingestion and lands in ACE; this service reads no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.writeoff`, module `reconciliation`, Java package `th.co.scb.ace.workbench.recovery.writeoff.reconciliation`; front end `src/modules/recovery/writeoff/WriteOffReconciliation.tsx`, the fragment SCR-27 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the records and the `write_off` updates commit together or not at all, and the failed write is MSG-P7-003. DP-13 moves the base of the key's two operations, neither of which this story provides, so it adds no element here. DP-19 is how SCR-27 reaches this service and rwb-case, one hop through the gateway, and this story fixes the screen fragment only. DP-05 is not in this story's pattern set although the step compares ACE's GL postings; the `v_ace_write_off` read is therefore consumed from rwb-source-data and no view grant is claimed (GAP-3037; ASM-5084). DP-09 and DP-10 stay off this table although the step consumes one event and signals the retention entry (ASM-5088).

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the plan already carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`. The four consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded (GAP-3037). No provided operation and no Schedule are recorded for this step. The matching cross-reference remains pending (GAP-3037); the step traces to REQ-S7-005 with that placeholder until the E6 BRD and the PRDs are written.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` reconciliation branch | Workflow | Waits for the posting product, loads the package, compares the two populations, applies R-WO-42 or R-WO-43 and reports the outcome to the parent |
| `reconcilePopulations` | Activity | The one step: read the approved rows and the postings, compare, write the records and the rows, answer the case move and hand the exception on |
| `WriteOffReconciliationEvaluator` | Service | The count-and-amount comparison against the tolerance in force, with the difference list, the matching keys and no business value in code |
| `PostingPopulationClient` | Client | The monthly GL write-off posting product of rwb-source-data, its `data_as_of` and its staleness; one hop, 2 s, breaker |
| `CaseClient` | Client | The case state read and the case-move answer with the retention start of rwb-case; one hop, 2 s, breaker |
| `RulePackageClient` | Client | The WO package version in force of rwb-decision; one hop, 2 s, breaker |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the period record and the difference records before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `WriteOffReconciliationWriter` | Repository | Updates `state` and `decision_log_id` on the rows of the period in one `rwb_writeoff` transaction, with the idempotency row and the optimistic lock |
| `WriteOffReconciliationController` | Controller | The read behind the SCR-27 fragment, the capability area and right, the scope and the problem mapping of 400, 401, 403, 404 and 503 |
| `WriteOffReconciliation` | React component | Shows the period, the two counts and amounts, the difference list, the failure states and the waiting state on SCR-27, read only |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the decision record, the idempotency key and the outbox are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the reconciliation: `state` and `decision_log_id` are existing columns.

**Configuration and reference data.**

- The count-and-amount tolerance and the audit period, read as package values and reference data at their version, never as constants (REC-06).
- The parameters read are the tolerance and the audit period, from the rwb-decision package in force, and the retention class and the state list, from rwb-case reference data; the reference-data contracts are the rwb-decision package read and the rwb-case read (client names Not specified in the source documents (DOR-RWB-S7-E6023-APP-20)), and DP-06 and DP-07 are not in this story's pattern set (DOR-RWB-S7-E6023-APP-20).
- The retention class and the state list of the WRITEOFF machine, read as reference data of rwb-case and of the package.
- The monthly posting calendar of the GL feed, read from the product's `data_as_of`; this service records no Schedule and no provided operation (GAP-3037; ASM-5084).
- The capability area "Write-off and posting" and its rights are access rows of rwb-access, read through the guard; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The reconciliation branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the posting product as its trigger.
2. The consumer of the rwb-source-data product event, with its inbox row, its consumer group and the `.dlt` path (AC1, X7).
3. `PostingPopulationClient` against its fake, with the product read, `data_as_of`, the staleness path and the unmatched key (AC1, X4, X5).
4. `RulePackageClient` and `WriteOffReconciliationEvaluator`, with the count-and-amount comparison, the tolerance and the difference list (AC1, X6).
5. `CaseClient` against its fake, with the state read, the two moves, the retention start and the no-answer path (AC2, AC3, X7).
6. `WriteOffDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
7. `WriteOffReconciliationWriter` with the one transaction, the two columns, the idempotency row and the optimistic lock (AC1, X8).
8. `CaseMoveAnswer` and the parent signal, with the two moves, and the exception hand-off to RWB-S7-E6024-APP (AC2, AC3).
9. The read behind the SCR-27 fragment and the screen fragment through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to another service's schema (X9, BR2, BR8).

**Feature flag.** `rwb.writeoff.reconciliation-v1`, read as a flag of the platform library; off means the branch holds the period, writes nothing, moves nothing and raises no exception, and the other stories of the service are unaffected.

**Done when.** The tests of section 16 pass, the branch runs from a synthetic posting product in SIT, R-WO-42 and R-WO-43 each produce their records, their state and their answer, a repeated product writes once, a forced record failure changes nothing, no `recovery_case`, `timer`, `rule_row` or `v_ace_write_off` read exists in the build, and SCR-27 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of this key. It names the tax criteria version, which is the scan's gate (R-WO-03) and RWB-S7-E6013-APP's path, so no path of this story raises it | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of the period, the product or a consumed request is absent or invalid | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right reads the reconciliation result (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the `write_off` rows change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The posting product is stale after a late or failed ACE batch (VR-S7-011-1), and it arrives with the product (X4) | {product} is from {date}. Today's load has not arrived. |

The first four message IDs are those of the legacy message set of this key, and MSG-P1-001 is the message of VR-S7-011-1 in FSD S7 A2.11.3.1; the text is the legacy and FSD wording, copied unchanged, and no message is reworded or added. MSG-S7-001 is carried because it is in the message set of the feature, and no path of this story raises it.

### 15. Screens and states

SCR-27 Write-off proposal — "the monthly population, the pack per case and removals with reasons", first in E6 (FSD S7 Screens) — is the screen of this step, in its scan, proposed, in-committee and approved states on the legacy screen table. It is served through the gateway-bff composite route (DP-19): the route calls this service for the write-off and its reconciliation state, rwb-case for the case and its route state, and rwb-reporting for the completeness of the period. This story fixes the write-off answer and the screen fragment; the composite route specification and the screen field list belong to RWB-PLT-N001-CON, and the reconciliation read behind the list is a placeholder (ASM-5089).

The states this story produces are the reconciliation state of the write-off on SCR-27 — reconciled with its period, or in the exception with its difference — and the states it shows: refused with MSG-P4-002, not recorded with MSG-P7-003, held as stale with MSG-P1-001 and waiting for the product. The approved state of SCR-27 belongs to the committee decision stories of this service, and the completeness report of the period is rwb-reporting's read model, not a screen of this service. The empty, loading, error and no access states of SCR-27 are Not specified in the source documents (CG-ALL-11118).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-023-01 | AC1 | Component | The closing period `2027-04` with its GL postings; the two counts, the two amounts, the records, the state and the case move asserted on the fakes |
| TC-E6-023-02 | AC2 | Integration | R-WO-13 with the credit committee approval; the `APPROVED` state, the final call and the limit applied read across the rwb-case and rwb-decision fakes |
| TC-E6-023-03 | AC3 | Integration | R-WO-15 with the committee approval; the approver and the limit applied read across the rwb-case and rwb-decision fakes |
| TC-E6-023-04 | AC4 | Component | The decision-record stub stopped; nothing written, no move answered, no exception raised and MSG-P7-003 shown |
| TC-E6-023-05 | AC5 (Access) | Component | A role without the Write-off and posting right; 403 with MSG-P4-002 and no read |
| TC-E6-023-07 | AC6 (Boundary) | Build | The boundary test fails the build on any statement outside `rwb_writeoff` or any `v_ace_*` read (X9, BR8) |
| TC-E6-023-08 | AC7 (Data) | Component | Synthetic fixtures only; no person name, contact value or identity number in the record, a log or a workflow input (BR11) |
| TC-E6-023-06 | Principle 5 | Component | A forced decision record write failure at the moment of the row update; no column changed and no move answered |
| TC-E6-023-14 | Contract (section 12) | Integration | Every operation, event and activity of section 12 checked against the contract it names; the fakes of 12.8 for the calls made |
| TC-E6-023-15 | Boundary (12.7, ASM-3438) | Component | The tables of 12.7 read and written only in `rwb_writeoff`; no foreign key, and no read of a `v_ace_*` view or of a table not owned here |
| TC-E6-023-09 | AC8 | Not specified in the source documents (NEWAC-RWB-S7-E6023-APP-AC10) | The rwb-source-data fake does not answer; nothing written and the AC8 failure outcome (AC8 Given) |
| TC-E6-023-10 | AC9 | Not specified in the source documents (NEWAC-RWB-S7-E6023-APP-AC11) | The write-off in RETENTION_RUNNING, not POSTED (AC9 Given) |
| TC-E6-023-11 | AC10 | Not specified in the source documents (NEWAC-RWB-S7-E6023-APP-AC7) | Synthetic period and fixtures as the AC10 Given lines |
| TC-E6-023-12 | AC11 | Not specified in the source documents (NEWAC-RWB-S7-E6023-APP-AC8) | The same product delivered twice for one period and tolerance (AC11 Given) |
| TC-E6-023-13 | AC12 | Not specified in the source documents (NEWAC-RWB-S7-E6023-APP-AC9) | The rwb-source-data fake answers a retry only after the first attempt times out; nothing written twice and the AC8 failure outcome on final timeout (AC12 Given) |

The six legacy cases are the legacy cases of RWB-E6-023 in their legacy order, with the Level column added: TC-E6-023-01, -04, -05 and -06 map to `Component` because the step is tested on its fakes, and -02 and -03 map to `Integration` because they cross the rwb-case and rwb-decision boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the tolerance, the audit period, the retention class, the state list and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, amounts, a code and a rule version only, and every fixture is synthetic. The comparison is by reference and never by party.
- The ACE data only through an owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, so `v_ace_write_off` reaches it only as the rwb-source-data product (DP-01, DP-02; ASM-5084).
- The case, its route state and the retention timer stay with rwb-case, and the package and the ledger with rwb-decision: no `recovery_case` row, no timer row, no rule row and no ledger entry is written here (BR6, BR7).
- The scan, the pack, the committee act, the posting, the provision feed, the exception loop and the closure stay with their own stories of this service: this step declares no operation, no event and no rule of theirs (ASM-5088, ASM-5089).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13).
- No retired element is reintroduced: no data-lake extract (DP-17), no shared job table, no Quartz row, no monolith base and no second event on the topic.
- The decision is recorded before the change and the records and the updates commit together; a build that writes the rows first fails the review (DP-03).
- Personal-data classes of the write-off fields (Data Classification and Personal Data Inventory v5): `id`, `case_id` and `decision_log_id` (DF-FIN-010 to DF-FIN-012) are Not personal; `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product` and `recovered_after` (DF-FIN-013 to DF-FIN-020) are classed Customer data and are held as a code, an amount or a date only, never beside a direct identifier.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published (Must, E6; FSD S7 Requirements served); this story owns the completeness half, and the plan's reqs row for the slice is empty (GAP-3037; ASM-5091) | The comparison, the completeness result and the exception list | TC-E6-023-01, TC-E6-023-04 | FEAT-WOF-11 | Not specified in the source documents (DOR-RWB-S7-E6023-APP-2) |
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account (Must, E6); this story reads the recorded final call, the approver and the limit applied as the approved side (ASM-5083) | The approved population and the record reference | TC-E6-023-02, TC-E6-023-03 | FEAT-WOF-11 | Not specified in the source documents (DOR-RWB-S7-E6023-APP-2) |
| REC-06 | Write-offs approved in the Workbench against the postings in `recovery.v_ace_write_off`, by count and amount, tolerance zero, monthly, owner Credit Administration | The two populations, the tolerance and the period | TC-E6-023-01 | FEAT-WOF-11 | Not specified in the source documents (DOR-RWB-S7-E6023-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the write-off row and its reconciliation state | TC-E6-023-01 | FEAT-WOF-11 | Not specified in the source documents (DOR-RWB-S7-E6023-APP-2) |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-023-06 | FEAT-WOF-11 | Not specified in the source documents (DOR-RWB-S7-E6023-APP-2) |
| ADR-018 | No data lake; rwb-reporting read model from events | The completeness result and its publication path | TC-E6-023-01 | FEAT-WOF-11 | Not specified in the source documents (DOR-RWB-S7-E6023-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget | TC-E6-023-02, TC-E6-023-03 | FEAT-WOF-11 | Not specified in the source documents (DOR-RWB-S7-E6023-APP-2) |
| ADR-022 | Local decision record plus central ledger | The decision record written before the change, with the ledger entry in P7 | TC-E6-023-04, TC-E6-023-06 | FEAT-WOF-11 | Not specified in the source documents (DOR-RWB-S7-E6023-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-023, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E6-023-01 to TC-E6-023-06 |
| Feature and screens | FEAT-WOF-11, SCR-27 Write-off proposal |
| Rules | R-WO-13, R-WO-15, R-WO-42 and R-WO-43, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-018, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the `write_off` element, the state vocabulary, the consumed rows, the rights, the error set and the fakes: RWB-S7-E6023-CON.
- The monthly eligibility scan, the tax criteria and JOB-16, and API-S7-001: RWB-S7-E6013-APP and RWB-S7-E6014-APP.
- The pack, its documents and its check: RWB-S7-E6015-APP; the removal by the team: RWB-S7-E6016-APP; the committee routing: RWB-S7-E6017-APP.
- The committee act that produced `APPROVED`, API-S7-002 and R-WO-13, R-WO-15, R-WO-14, R-WO-16 and R-WO-17: RWB-S7-E6018-APP, RWB-S7-E6019-APP and RWB-S7-E6020-APP.
- The posting to ALS and the general ledger that produced `POSTED`, R-WO-20 to R-WO-23: RWB-S7-E6021-APP; the provision feed, R-WO-25 to R-WO-28: RWB-S7-E6022-APP.
- The write-off exception loop, R-WO-24 and R-WO-44 to R-WO-46: RWB-S7-E6024-APP; the retention expiry and the case closure, R-WO-47 and R-WO-48: RWB-S7-E6025-APP.
- The case of record, its route states, the `timer` row and the move: rwb-case (P3), whose answers this story consumes and fakes (GAP-3037).
- The GL write-off postings, `gl_write_off` and `v_ace_write_off` (DF-ACE-261 to DF-ACE-269) and the INT-16 ingestion: ACE and rwb-source-data (P1) (GAP-3037; ASM-5084).
- The WO rule package, its version, the delegation limits and the ledger: rwb-decision (P7) (ASM-5086).
- The completeness read model and its report: rwb-reporting (P9) (ASM-5088); the gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
