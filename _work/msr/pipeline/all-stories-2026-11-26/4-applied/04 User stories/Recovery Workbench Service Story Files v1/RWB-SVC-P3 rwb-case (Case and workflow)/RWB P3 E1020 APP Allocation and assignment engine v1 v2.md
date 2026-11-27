# RWB-P3-E1020-APP Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1020-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1073-APP |
| Depends on (build) | RWB-P3-E1020-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1073-APP |
| Contract dependencies | RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | RWB-P3-E1020-OPS, RWB-PLT-E1056-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-009, FR-P3-010, FR-P3-011, FR-P3-012, FR-P3-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-020 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E1020-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **every new recovery case placed in a queue and given an owner by the ALLOCATION and ASSIGNMENT rule packages on the morning it arrives**, so that **each case at 90 days past due has one owner from its first day and nobody allocates cases by hand**.

This slice is the rwb-case build of that behaviour. The legacy engine worked inside the recovery-core monolith, called `RuleEvaluator` in process and left an assignment to the decision log writer of another module; the target keeps the same business behaviour and moves each mechanical part to its new owner:

- the trigger becomes **DailyCaseRun** on the rwb-case Temporal task queue (namespace `rwb-recovery`), started by the `AceDataReady` event and by a Temporal Schedule, replacing the Quartz job **JOB-03** (kept as the legacy job name in the run book, the metrics and the test cases; DP-10);
- the queue decision stays package **ALLOCATION** and the owner decision stays package **ASSIGNMENT**, both governed in rwb-decision and evaluated **locally** in rwb-case through the embedded Drools kit (DP-04), the model being fetched with `GET /rule-models/{n}/{v}` and verified by checksum;
- the decision record is written **locally in the same transaction** as the state change and the outbox row, then published on `rwb.decision-record.v1` for the central ledger in rwb-decision (DP-03, DP-09);
- the case, the queue, the team, the owner and the assignment stay in schema `rwb_case` (DP-01); the case record and the AssignmentEngine are read and written through the service's own tables only;
- the allocation summary to the team manager goes out through the ACE notification path, as today.

### 2. Business rationale

Cases are allocated today from team spreadsheets, and ownership is agreed by email, so a case can wait days with no owner. This story places every new case in a queue and gives it an owner by rule before 07:00 on the morning after case creation, with the rule ID and the package version on a decision record that is sealed in the central ledger. It meets REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 and REQ-CWC-016, and serves the business measure "cases inside the service level" (target set with DL22) and control CTL-03.

The legacy engine ran package ALLOCATION and package ASSIGNMENT through `RuleEvaluator` (RWB-E1-072) inside the monolith, with first-match semantics (T5) and the package version chosen at evaluation time (T7), and left a decision log entry through the writer of another module. In the target the governance and the registry stay with rwb-decision (P7) and the evaluation runs in the owning service: rwb-case fetches the model, keeps a local copy with its checksum, evaluates under 300 ms at the 95th percentile (NFR-011) and writes the decision record in its own schema before the case moves (R-UNI-39).

Nothing about the business answer changes. A MORTGAGE case in BKK still reaches the queue its row names, the officer with the fewest open cases still gets it, anyone at the cap is still skipped, and a case that matches no row still goes to the exception queue and raises a failure event.

### 3. Preconditions

- RWB-P3-E1018-APP is done: new cases exist in `rwb_case.recovery_case` with status NEW, product group, region and exposure band.
- RWB-P3-E1019-APP is done: queues, queue members and caseload caps are loaded; queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN.
- RWB-P3-E1073-APP is done: the service can fetch a rule model from rwb-decision and evaluate a package locally through the embedded Drools kit; a package with no version in force raises `NoPackageInForce` (MSG-P3-027).
- RWB-P3-E1020-CON is done: the OpenAPI 3.1 and AsyncAPI documents of this story are published and their fakes are available.
- Package ALLOCATION version "ALLOC-2026.11" is approved in rwb-decision by RW-RISK, who is not the author, and is in force from 2026-11-30; package ASSIGNMENT version "ASSIGN-2026.11" is approved and in force from the same date. Each package has at least 50 passing scenarios. The ALLOCATION default row is the last row and its check is at load in rwb-decision, not at run time.
- Every ALLOCATION row holds rule ID, product group, region, exposure band, target queue, valid from, valid to, approver and test case ID. Every ASSIGNMENT row holds queue code, method, cap, named owner and overflow queue.
- Parameters are loaded through the rwb-case parameter contract (DP-06, RWB-P3-E1042-CON): `allocation.exception.queue.code` = "RWB-EXC" and `allocation.deviation.queue.code` = "DEV-HANDLER" (assumed values; DL23).
- DailyCaseRun has received `AceDataReady` for today's business date, or the schedule for the business date has fired; JOB-02 case creation has completed for the same date.
- The worker runs as the rwb-case login (DP-02). The per-service login name is Not specified in the source documents (GAP-0684; ASM-1231).
- The caseload cap of 150 is held as data, not in code. Whether the cap is a parameter row (`parameter_value`) or reference data (`queue.capacity_cap`, `queue_member.capacity`) is Not specified in the source documents (GAP-0685; ASM-1232).

### 4. Flow

1. **Trigger.** rwb-source-data publishes `AceDataReady` (EV-26) for the business date 2026-12-01; rwb-case's case router consumes it and starts **DailyCaseRun** on task queue `rwb-case` (workflow ID `daily-case-run-2026-12-01`, so a duplicate delivery starts nothing new). The same workflow is started by the DailyCaseRun Temporal Schedule. Legacy reference: **JOB-03 Morning allocation**, previously a Quartz job started after JOB-02.
2. **Select.** The `allocate` activity selects every case in `rwb_case.recovery_case` with status NEW whose `last_allocation_date` is before the business date, in chunks, locking each row (`FOR UPDATE SKIP LOCKED`).
3. **Deviation branch.** The activity reads `deviation_open`; a case with an open deviation goes to the deviation handler queue named by `allocation.deviation.queue.code` (R-DEV-01) and gets no case owner.
4. **ALLOCATION.** The activity builds `AllocationFacts` and evaluates package ALLOCATION through the embedded Drools kit with the business date; the first matching row in row order decides (T5), and the answer returns the rule ID, the package version label and the outputs (target queue code, owner role).
5. **ASSIGNMENT.** The activity fills the target queue code and cap into the same facts object and evaluates package ASSIGNMENT for that queue; the row returns the method (`ROUND_ROBIN`, `LOWEST_LOAD`, `NAMED_OWNER` or `SKILL`), the cap and, for NAMED_OWNER, the named owner. `AssignmentEngine` counts the open cases of each queue member and picks the first owner below the cap by that method.
6. **One transaction.** In a single transaction in schema `rwb_case` the activity sets the queue, team, owner, status ASSIGNED, stage clock start, allocation rule ID and package version, writes the assignment row with reason ALLOCATION and the assignment rule ID and package version, sets `last_allocation_date`, writes the **decision record** (rule ID, rule version, inputs, answer, hash-linked to the previous record) and writes the outbox row for `CaseAllocated` and `CaseStateChanged`. If any part fails, nothing moves (R-UNI-39).
7. **Record and apply.** The outbox relay publishes `rwb.case.CaseAllocated.v1` and `rwb.case.CaseStateChanged.v1` on `rwb.case.events.v1` (CloudEvents 1.0, key caseId, IDs and facts only) and the same decision record on `rwb.decision-record.v1`, where rwb-decision collects it into the central ledger.
8. **Summary.** After the last case the workflow builds the allocation summary per team (MSG-P3-011, MSG-P3-012) and sends it to the team manager through the ACE notification path (ACE Common, outside the 19 services).
9. **Run record.** The workflow records the run result (cases read, assigned, overflow, exception, failed, skipped) as workflow search attributes and as a run summary row for the operations dashboard; the job monitor view of JOB-03 reads it from the workflow, because the legacy job table is no longer used.
10. **Rebalancing.** The same task queue serves the `rebalance` activity for JOB-06 at 06:30 Asia/Bangkok. The exact cadence of the rebalancing trigger is Not specified in the source documents (GAP-0686; ASM-1233); rebalancing behaviour itself belongs to the E1-030 story and is only registered here.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Every owner in the target queue is at or above the cap | Case goes to the overflow queue named by the ASSIGNMENT row; status stays NEW; counted in the summary | MSG-P3-011 | AC4 |
| X2 | No ALLOCATION rule matches the case | Case goes to the exception queue; status stays NEW; rule gap logged; `CaseAllocationFailed` (EV-03) published | MSG-P3-012 | AC5 |
| X3 | Decision record write fails | Allocation rolled back; case stays NEW with no queue change; retried in the next run | MSG-P3-013 | AC6 |
| X4 | Case has `deviation_open = true` | Case goes to the deviation handler queue; no case owner is chosen | None | AC7 |
| X5 | The run is repeated for the same business date | Cases already allocated for that date are skipped; no second assignment or decision record | None | AC8 |
| X6 | No case has status NEW | Run completes with zero counts; summary says 0 | MSG-P3-011, MSG-P3-012 with count 0 | AC9 |
| X7 | JOB-02 has not completed for the business date, so `AceDataReady` has not arrived | DailyCaseRun does not start; the run monitor shows it waiting; cases stay NEW | MSG-P1-001 | Legacy AC10, owned by RWB-P3-E1018-APP |
| X8 | A rerun starts while the first run still holds a case | The case row lock stops the second worker; each case is allocated once | None | AC11 |
| X9 | The ASSIGNMENT row names no overflow queue and every owner is at the cap | Case goes to the exception queue with the reason "NO_OVERFLOW_QUEUE" | MSG-P3-012 | AC13 |
| X10 | A user without the right starts DailyCaseRun from the run monitor | Refused with 403; nothing runs | MSG-P4-002 | Access test TC-E1-020-14 |
| X11 | No ALLOCATION or ASSIGNMENT version is in force, or the fetched model fails its checksum | The activity fails at once (non-retryable `NoPackageInForce`, or the last good model is kept); no case is touched; the stuck-workflow alert fires | MSG-P3-027 | AC6, guardrail G4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the case record (RWB-P3-E1018-APP), the roles, teams and queues table (RWB-P3-E1019-APP), the local rule evaluation (RWB-P3-E1073-APP), the decision-record library (RWB-PLT-E1027-CON), the workflow kit (RWB-PLT-E1071-CON), the parameters and reference-data contracts (RWB-P3-E1042-CON, RWB-P3-E1043-CON) and its own contract (RWB-P3-E1020-CON) |
| Negotiable | The allocation rows, the assignment method per queue, the cap and the queue codes are data values in rwb-decision and in the parameters. The story fixes the behaviour, not the values |
| Valuable | Ends allocation from spreadsheets for every new case, about 3,110 a month (DL15) |
| Estimable | Two rule packages consumed, one Temporal workflow with one activity, one transaction, no new screen |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Every criterion this slice owns has a test case in section 16; AC10 is tested by RWB-P3-E1018-APP |

### 7. Acceptance criteria

```gherkin
Feature: Allocate a new recovery case to a queue and an owner

  Background:
    Given package ALLOCATION version "ALLOC-2026.11" is in force from 2026-11-30
    Given package ASSIGNMENT version "ASSIGN-2026.11" is in force and gives queue "MTG-BKK-CO" the method "ROUND_ROBIN" with a caseload cap of 150
    Given the queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN
    Given the queue "MTG-BKK-CO" has the overflow queue "MTG-BKK-OVF"
    Given the business date is 2026-12-01

  Scenario: AC1 A new case is placed in the queue its rule names (legacy RWB-E1-020 AC1)
    Given a new case RW-2026-000201 with status "NEW", product group "MORTGAGE", region "BKK" and exposure band "B2"
    Given allocation rule "ALLOC-014" matches product group "MORTGAGE", region "BKK" and any exposure band, with target queue "MTG-BKK-CO"
    Given the rwb-decision contract mock returns package ALLOCATION version "ALLOC-2026.11" with rule "ALLOC-014" for product group "MORTGAGE", region "BKK" and any exposure band
    When the morning allocation run starts
    Then the system places the case in queue "MTG-BKK-CO"
    Then the case team is "MTG-BKK" and the region is "BKK"

  Scenario: AC2 The owner is chosen by the assignment rule (legacy RWB-E1-020 AC2)
    Given queue "MTG-BKK-CO" holds three case owners U-01, U-02 and U-03 with 120, 95 and 140 open cases
    Given the last owner given a case in the queue was U-02
    Given the rwb-decision contract mock returns package ASSIGNMENT version "ASSIGN-2026.11" with rule "ASSIGN-007", method "ROUND_ROBIN" and caseload cap 150 for queue "MTG-BKK-CO"
    When case RW-2026-000201 is placed in the queue
    Then the system gives the case to U-03
    Then the case status becomes "ASSIGNED"
    Then the system writes an assignment record with reason "ALLOCATION", allocation rule ID "ALLOC-014" and assignment rule ID "ASSIGN-007"

  Scenario: AC3 An owner at the caseload cap is skipped (legacy RWB-E1-020 AC3)
    Given the last owner given a case was U-02
    Given U-03, the next owner in turn, holds 150 open cases
    Given U-01 holds 120 open cases
    Given the rwb-decision contract mock returns package ASSIGNMENT version "ASSIGN-2026.11" with caseload cap 150 for queue "MTG-BKK-CO"
    When case RW-2026-000202 is placed in the queue
    Then the system gives the case to U-01, the following owner below the cap

  Scenario: AC4 Every owner is at the cap (legacy RWB-E1-020 AC4)
    Given U-01, U-02 and U-03 each hold 150 open cases
    Given the rwb-decision contract mock returns package ASSIGNMENT version "ASSIGN-2026.11" with caseload cap 150 and overflow queue "MTG-BKK-OVF" for queue "MTG-BKK-CO"
    When case RW-2026-000203 is placed in queue "MTG-BKK-CO"
    Then the system places the case in the overflow queue "MTG-BKK-OVF"
    Then the case status stays "NEW" and no owner is set
    Then the team manager of "MTG-BKK" receives the allocation summary with MSG-P3-011 and count 1

  Scenario: AC5 No allocation rule matches (legacy RWB-E1-020 AC5)
    Given a new case RW-2026-000204 with product group "SSME" and region "NE3" that matches no allocation rule
    Given the rwb-decision contract mock returns package ALLOCATION version "ALLOC-2026.11" with no matching row for product group "SSME" and region "NE3"
    When the morning allocation run starts
    Then the system places the case in the exception queue "RWB-EXC"
    Then the case status stays "NEW"
    Then the system writes a decision log entry with final call "RULE_GAP", product group "SSME" and region "NE3"
    Then the system publishes caseAllocationFailed with reason "NO_ROW_MATCHED"
    Then the allocation summary carries MSG-P3-012 with count 1

  Scenario: AC6 Every allocation is logged (legacy RWB-E1-020 AC6)
    Given case RW-2026-000205 matches rule "ALLOC-014" and owner U-02 is below the cap
    Given the rwb-decision contract mock returns package ALLOCATION version "ALLOC-2026.11" with rule "ALLOC-014" and package ASSIGNMENT version "ASSIGN-2026.11" with rule "ASSIGN-007"
    When the case is placed in the queue and given an owner
    Then the system writes one decision log entry with rule ID "ALLOC-014", package version "ALLOC-2026.11", queue "MTG-BKK-CO", owner U-02 and the inputs used
    Then the assignment row carries assignment rule ID "ASSIGN-007" and package version "ASSIGN-2026.11"
    Then if the decision log write fails, the allocation is not made, the case stays "NEW" with no queue and the job record carries MSG-P3-013 for the case

  Scenario: AC7 A case with an open deviation is not allocated to a case owner (legacy RWB-E1-020 AC7)
    Given a new case RW-2026-000206 with deviation_open = true
    Given the rwb-case reference-data contract mock returns queue "DEV-HANDLER" for parameter "allocation.deviation.queue.code"
    When the morning allocation run starts
    Then the system places the case in the deviation handler queue "DEV-HANDLER" named by rule R-DEV-01
    Then the system sets no case owner and the status stays "NEW"

  Scenario: AC8 A repeated run for the same date has no further effect (legacy RWB-E1-020 AC8)
    Given the morning allocation run for 2026-12-01 has assigned case RW-2026-000201 to U-03
    When the run for 2026-12-01 is started again from the job monitor
    Then case RW-2026-000201 keeps owner U-03 and its one assignment record
    Then the system writes no second decision log entry for the case
    Then the job record shows 1 case skipped as already allocated

  Scenario: AC9 A run with no new cases (legacy RWB-E1-020 AC9)
    Given no case has status "NEW" on 2026-12-01
    When the morning allocation run starts
    Then the run completes with 0 cases read
    Then the allocation summary for each team shows 0 in overflow and 0 in the exception queue

  Scenario: AC11 Two runs at the same time allocate each case once (legacy RWB-E1-020 AC11)
    Given a first run is allocating case RW-2026-000207
    When a rerun for 2026-12-01 reaches the same case at the same time
    Then the rerun skips the locked case
    Then the case has exactly one assignment record and one decision log entry for 2026-12-01

  Scenario: AC12 An owner one case below the cap gets the case (legacy RWB-E1-020 AC12)
    Given U-03 is next in turn and holds 149 open cases
    Given the rwb-decision contract mock returns package ASSIGNMENT version "ASSIGN-2026.11" with caseload cap 150 for queue "MTG-BKK-CO"
    When case RW-2026-000208 is placed in queue "MTG-BKK-CO"
    Then the system gives the case to U-03
    Then U-03 now holds 150 open cases

  Scenario: AC13 A queue with no overflow queue sends the case to the exception queue (legacy RWB-E1-020 AC13)
    Given the ASSIGNMENT row for queue "HP-CEN-CO" names no overflow queue
    Given every owner in queue "HP-CEN-CO" holds 150 open cases
    Given the rwb-decision contract mock returns package ASSIGNMENT version "ASSIGN-2026.11" with no overflow queue and caseload cap 150 for queue "HP-CEN-CO"
    When case RW-2026-000209 is placed in queue "HP-CEN-CO"
    Then the system places the case in the exception queue "RWB-EXC" with reason "NO_OVERFLOW_QUEUE"
    Then the case status stays "NEW"
```

AC10 of the legacy story ("The run waits for case creation") is owned by RWB-P3-E1018-APP and is not repeated here. The values in every scenario are copied unchanged from the legacy story: queue codes "MTG-BKK-CO", "HP-CEN-CO", "RWB-EXC", "DEV-HANDLER", the overflow queue "MTG-BKK-OVF", the rule IDs "ALLOC-014" and "ASSIGN-007", the package versions "ALLOC-2026.11" and "ASSIGN-2026.11", the cap 150 and the business date 2026-12-01.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case is allocated by the first row of package ALLOCATION, in row order, whose product group, region and exposure band match the case. First match follows the Drools design (first match wins, one row decides) and "any" in a column matches every value | Package ALLOCATION, governed in rwb-decision; REQ-CWC-008 |
| BR2 | The owner is chosen by the ASSIGNMENT row for the queue, whose outputs hold the method: ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER or SKILL, and the cap | Package ASSIGNMENT; LOV-ASSIGN |
| BR3 | An owner at or above the queue's caseload cap is skipped. Open cases are cases in the queue owned by the person with status other than CLOSED | Queue cap values, DL23; the storage of the cap is Not specified in the source documents (GAP-0685; ASM-1232) |
| BR4 | A case that cannot be given an owner goes to the overflow queue named in the ASSIGNMENT row | Overflow queue in the ASSIGNMENT row; `queue.overflow_queue_id` |
| BR5 | A case that matches no rule goes to the exception queue, and the gap is logged. R-UNI-41 handles the case once a person decides | R-UNI-41; FEAT-CWC-09 |
| BR6 | A case with an open deviation goes to the deviation handler queue | R-DEV-01 |
| BR7 | A decision that cannot be written to the decision record does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR8 | A case is allocated at most once per business date | R-UNI-40; idempotency key caseId and businessDate |
| BR9 | Each allocation records the ALLOCATION rule ID and package version on the decision record, and the ASSIGNMENT rule ID and package version on the assignment row | REQ-CWC-016; CTL-03 |
| BR10 | The ALLOCATION package always has a default row as its last row; the check is at load in rwb-decision and is not repeated at run time | REQ-CWC-008; DP-04 |
| BR11 | The rule answer is produced only inside an activity, never in workflow code, so a replay reuses the recorded answer | D-RCV-60; Drools design slide 14 |
| BR12 | The case, the assignment, the decision record and the outbox row are written in one transaction in schema `rwb_case`; a failure in any of them leaves the case unchanged | R-UNI-39 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| New | Allocation rule matched | ALLOCATION rule matched and the ASSIGNMENT rule gives an owner below the cap | Assigned |
| New | Allocation rule matched | ALLOCATION rule matched and every owner at the cap | New, in the overflow queue |
| New | Allocation rule matched | No ALLOCATION rule matched | New, in the exception queue |
| New | DEVIATION_FLAGGED (R-DEV-01) | `deviation_open = true` | New, in the deviation handler queue |

The transition to ASSIGNED publishes `rwb.case.CaseStateChanged.v1`; the case status column and the `CaseStateChanged` event are written in the same transaction as the assignment. A case placed in the overflow or exception queue does not change status and publishes no `CaseStateChanged`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-RULES, embedded rule evaluator | Fetches and evaluates packages ALLOCATION and ASSIGNMENT inside the `allocate` activity (Rules and parameters R) |
| SY-CASEWF, case workflow worker | Updates the case, writes the assignment and the decision record (Case record CRU; Queue and allocation CRU) |
| The decision-record library (DP-03) | Writes the local record in the same transaction and publishes it on `rwb.decision-record.v1` (Decision log C) |
| RW-TEAMMGR, team manager | Reads the queue and the allocation summary for their team (Queue and allocation R) |
| RW-CASEOWN, case owner | Reads the cases given to them (Case record R, scope Own) |
| RW-PLATADM, platform administrator | Starts or retries DailyCaseRun from the run monitor (Platform administration U) |
| RW-REFADM, reference data administrator | Prepares the package workbook; the load and the approval are in rwb-decision |
| Process owner for L1 18, Shared operations | Approves each package version through the rwb-decision rule change process. No delegation of authority level applies |

### 11. Data

| Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Write |
| DF-CAS-009 | recovery_case | owner_user_id | Write |
| DF-CAS-010 | recovery_case | queue_id | Write |
| DF-CAS-011 | recovery_case | team_code | Write |
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-CAS-015 | recovery_case | exposure_band | Read |
| DF-CAS-018 | recovery_case | stage_clock_start | Write |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-021 | recovery_case | rule_version (the ALLOCATION package version label) | Write |
| DF-CAS-054 | recovery_case | last_allocation_date | Write |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-005 | queue | role_code | Read |
| DF-WRK-006 | queue | assignment_method | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-008 | queue | overflow_queue_id | Read |
| DF-WRK-037 | queue | rr_cursor_user_id | Write |
| DF-WRK-047 | queue_member | user_id | Read |
| DF-WRK-048 | queue_member | capacity | Read |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Write |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | param_key, param_value, valid_from, status | Read |
| DF-REF-181 to DF-REF-184 | reference_row | row_key, row_data | Read |
| DF-REF-159 to DF-REF-180 | reference_version | version_label, status, valid_from | Read |
| The local decision record (DP-03 library) | decision record | rule ID, rule version, inputs, answer, prev_hash, entry_hash, decidedAt | Write |
| The outbox (DP-09 library) | outbox_event | event name, payload, key caseId | Write |

The rule rows themselves are no longer read here. Package ALLOCATION and package ASSIGNMENT, their row order, their conditions and their outputs arrive as a fetched model with a checksum, and the row catalog stays in rwb-decision (DP-01, DP-04). `queue.assignment_method` and `queue.capacity_cap` are facts for the ASSIGNMENT package: the row is the decision, and a change of method or cap is a new package version or a new parameter version. Whether the 150 cap arrives as a parameter value or as reference data is Not specified in the source documents (GAP-0685; ASM-1232). The rwb-case login name is Not specified in the source documents (GAP-0684; ASM-1231).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Purpose in this story |
|---|---|---|---|
| GET | /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Read the queue, team, owner, status and `ruleVersion` of a case after the run (the legacy result endpoint) |
| GET | /api/recovery/case/v1/queues/{queueId}/cases | P3 rwb-case | Read the cases placed in a queue, including the overflow and exception queues |

#### 12.2 REST operations consumed

| Operation | Path | Owner | Used for |
|---|---|---|---|
| GET | /api/recovery/decision/v1/rule-models/{n}/{v} | P7 rwb-decision | Fetch package ALLOCATION and package ASSIGNMENT at load and on `RulePackageInForce`; verify the checksum before the model is swapped in |

#### 12.3 Events published

| Event name | Topic | Key | Payload (no personal data) |
|---|---|---|---|
| rwb.case.CaseAllocated.v1 | rwb.case.events.v1 | caseId | caseId, queueId, ownerId, ruleId, ruleVersion (the ALLOCATION package version label) |
| rwb.case.CaseAllocationFailed.v1 | rwb.case.events.v1 | caseId | caseId, reason, ruleGap |
| rwb.case.CaseStateChanged.v1 | rwb.case.events.v1 | caseId | caseId, fromStatus, toStatus, ruleId, ruleVersion |
| rwb.case.DecisionRecorded (decision record) | rwb.decision-record.v1 | caseId | caseId, ruleId, ruleVersion, inputsRef, outcome, decidedAt, prev_hash, entry_hash |

#### 12.4 Events consumed

| Event name | Topic | Owner | Reaction |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 rwb-source-data | Starts DailyCaseRun for the business date (inbox dedupe; a duplicate starts nothing new) |
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | P7 rwb-decision | The service fetches the new model version, verifies the checksum and swaps it in; the last good model is kept on failure |

#### 12.5 Workflows and activities

| Item | Kind | Task queue | Owner | Note |
|---|---|---|---|---|
| CaseWorkflow | Parent workflow, one per case, workflow ID `case-{caseId}` | rwb-case | P3 | Starts DailyCaseRun work for the case and hosts the case state |
| DailyCaseRun | Workflow, started by `AceDataReady` and by its Schedule; workflow ID `daily-case-run-{businessDate}` | rwb-case | P3 | Replaces legacy **JOB-03 Morning allocation**; steps: select, allocate, summarise, record |
| allocate | Activity | rwb-case | P3 | Deviation branch, ALLOCATION evaluation, ASSIGNMENT evaluation, one transaction |
| transfer | Activity | rwb-case | P3 | Registered on the same queue; owned by RWB-P3-E1021-APP |
| rebalance | Activity | rwb-case | P3 | Registered on the same queue; owned by the E1-030 rebalancing story |

#### 12.6 Schedules

| Schedule | Cron (Asia/Bangkok) | Overlap policy | Owner | Note |
|---|---|---|---|---|
| DailyCaseRun | Fires after the ACE business date is ready; also event-started | SKIP | P3 rwb-case | JOB-03 runs inside it. The exact schedule expression for the date-based run is Not specified in the source documents (GAP-0686; ASM-1233) |
| JOB-06 rebalancing | 06:30 | SKIP | P3 rwb-case | Registered here, behaviour owned by the E1-030 story |

#### 12.7 Tables owned

| Table | Schema | Owner | Read or write |
|---|---|---|---|
| recovery_case | rwb_case | P3 rwb-case | Read, write |
| queue | rwb_case | P3 rwb-case | Read, write (`rr_cursor_user_id`) |
| queue_member | rwb_case | P3 rwb-case | Read |
| assignment | rwb_case | P3 rwb-case | Write |
| parameter_catalog | rwb_case | P3 rwb-case | Read |
| parameter_value | rwb_case | P3 rwb-case | Read |
| lov_value | rwb_case | P3 rwb-case | Read |
| reference_row | rwb_case | P3 rwb-case | Read |
| reference_version | rwb_case | P3 rwb-case | Read |
| outbox_event | rwb_case | PLT (library object created in the service schema) | Write |

No table outside schema `rwb_case` is read or written by this story. The decision ledger (`decision_log_entry`) is P7 rwb-decision and is reached only through `rwb.decision-record.v1`.

#### 12.8 Contract fakes

| Fake | Contract | Used for |
|---|---|---|
| rwb-decision rule-model fake | GET /api/recovery/decision/v1/rule-models/{n}/{v} | Returns package ALLOCATION "ALLOC-2026.11" and package ASSIGNMENT "ASSIGN-2026.11" with the rows the tests need, and the checksum |
| rwb-decision record fake | rwb.decision-record.v1 | Accepts the decision record and answers with a ledger reference; used to prove the outbox row is written in the same transaction |
| rwb-source-data event fake | rwb.source-data.events.v1 | Publishes `AceDataReady` for 2026-12-01, twice in the duplicate test |
| ACE notification path fake | ACE Common notification (INT-34) | Captures the allocation summary per team; ACE Common is outside the 19 services and has no ownership row |

The credentials of the fake and of the deployed sandbox use the rwb-case login (DP-02); its name is Not specified in the source documents (GAP-0684; ASM-1231).

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | Two read operations served; one fetch of a rule model from rwb-decision (one hop, 2 s timeout, circuit breaker per downstream) |
| Kafka | 4 published, 2 consumed | `CaseAllocated`, `CaseAllocationFailed`, `CaseStateChanged` on `rwb.case.events.v1`; the decision record on `rwb.decision-record.v1`; consumes `AceDataReady` and `RulePackageInForce` |
| Temporal | 2 workflows, 3 activities | CaseWorkflow (parent), DailyCaseRun; activities allocate, transfer, rebalance on task queue rwb-case in namespace rwb-recovery |
| File | None | No file is read or written by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case.allocation` (base package `th.co.scb.ace.workbench.recovery.case`).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AllocationWorkflow (DailyCaseRun) | Workflow | Select, allocate, summarise, record; deterministic workflow code only; no database, clock, random or rule call in workflow code |
| AllocationActivity | Activity | Deviation branch, the two rule evaluations, the owner choice, the single transaction, the outbox rows |
| AllocationFacts | Fact record | The fact object given to the rule evaluation: case number, product group, region, exposure band, days past due, deviation flag, queue code and cap |
| AssignmentEngine | Service | Applies the method and cap from the ASSIGNMENT outputs, counts open cases and picks the first owner below the cap |
| OwnerLoadRepository | Repository | Counts open cases per owner in a queue (`ix_case_owner_status`) |
| CaseAndWorkflowRepository | Repository | Reads and updates `recovery_case`, `queue`, `queue_member`, `assignment` in schema `rwb_case` |
| RuleModelClient | Client | Fetches the model with `GET /rule-models/{n}/{v}` from rwb-decision, verifies the checksum, keeps the last good model |
| LocalRuleEvaluator | Component | The embedded Drools kit call: package code, facts, business date in; rule ID, package version and outputs out |
| DecisionRecordWriter | Library client | Writes the local decision record in the caller's transaction and the outbox row (DP-03) |
| AllocationSummaryBuilder | Service | Counts overflow and exception cases per team; fills MSG-P3-011 and MSG-P3-012 |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Database**

- Reads: `recovery_case` (id, case_no, product_group, region_code, exposure_band, deviation_open, status, last_allocation_date), `queue` (id, queue_code, team_code, role_code, capacity_cap, overflow_queue_id), `queue_member` (user_id, capacity), `parameter_value`, `reference_row`, `reference_version`, `lov_value`.
- Writes: `recovery_case` (status, owner_user_id, queue_id, team_code, stage_clock_start, rule_version, last_allocation_date, version), `queue` (rr_cursor_user_id), `assignment` (all columns), the local decision record, `outbox_event`.
- Lock: `SELECT ... FROM recovery_case WHERE id = ? AND status = 'NEW' FOR UPDATE SKIP LOCKED`; optimistic version column on update.
- Migration in this story: `V020_1__allocation_columns.sql` in the rwb-case Flyway sequence (DP-15) adds `recovery_case.last_allocation_date` (date) and `queue.rr_cursor_user_id` (uuid). `queue_member` is created by RWB-P3-E1019-APP.

**Configuration and reference data**

- Package ALLOCATION version "ALLOC-2026.11" and package ASSIGNMENT version "ASSIGN-2026.11", authored by RW-REFADM, loaded and approved by RW-RISK in rwb-decision, in force from 2026-11-30.
- Queues, members and caps from RWB-P3-E1019-APP; caps DL23. Whether the cap is a parameter row or reference data is Not specified in the source documents (GAP-0685; ASM-1232).
- Parameters through the rwb-case parameter contract: `allocation.exception.queue.code`, `allocation.deviation.queue.code`.
- Lists LOV-ASSIGN, LOV-ASSIGN-REASON, LOV-CASE-STATUS from `lov_value` (DP-07).

**Build steps**

1. `AllocationFacts` and the ALLOCATION evaluation: given a case snapshot and a model version, return the first matching row, its rule ID and the package version, or none. Unit tests per BR1 with "any" values.
2. The ASSIGNMENT evaluation and `AssignmentEngine`: apply the row's method with cap skipping and the round-robin cursor. Unit tests for AC2, AC3, AC12 boundary.
3. `OwnerLoadRepository`: open case count per owner and queue; integration test on PostgreSQL with containerised database.
4. `AllocationActivity`: lock, deviation branch, two evaluations, overflow and exception branches, then the case update, the assignment, the decision record and the outbox row in one transaction.
5. Idempotency: skip when `last_allocation_date` equals the business date; return SKIPPED.
6. `DailyCaseRun` and the `AceDataReady` consumer with inbox dedupe; workflow ID by business date so a duplicate starts nothing.
7. `AllocationSummaryBuilder` and the call to the ACE notification path for each team manager.
8. End-to-end tests TC-E1-020-01 to TC-E1-020-15 on the synthetic case set. The default row check is not tested here; rwb-decision covers it.

**Feature flag.** `rwb.case.allocation` (the legacy name `rwb.p3.allocation` is retired by DP-14). Off: DailyCaseRun does not run and cases stay NEW.

**Done when.** The tests in section 16 pass; TC-E1-020-01 and TC-E1-020-08 are in the regression suite; every decision record names the ALLOCATION rule ID and package version; JOB-03 finishes 3,110 synthetic cases inside 15 minutes in SIT (assumed target; DL11); no query in the build reads a table outside schema `rwb_case`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-011 | Allocation summary, case in overflow | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-012 | Allocation summary, no rule matched | {count} new cases matched no allocation rule and are in the exception queue. |
| MSG-P3-013 | Decision record write failed for a case | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| MSG-P3-027 | No ALLOCATION or ASSIGNMENT version is in force at the run | The rule version was refused at the {check} check: {detail}. |
| MSG-P1-001 | DailyCaseRun waiting because the ACE batch has not completed | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the right starts DailyCaseRun | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10. For MSG-P3-027 the {check} value is "package in force" and the {detail} names the package code only. Error responses use the RFC 9457 problem-details envelope published in RWB-P3-E1020-CON.

### 15. Screens and states

No new screen. SCR-02 Case list (states Loading; list) shows the queue, the owner and the status of each case after the run. SCR-09 Exception queue (states Loading; list) shows cases placed in "RWB-EXC". The team manager receives the allocation summary after each run. Both screens are reached through the gateway-bff composite route (DP-19) from the rwb-case read operations of 12.1; queue screens come with the queue stories of Epic 2 (SCR-07).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-020-14 | Access | Component | RW-CASEOWN reruns JOB-03 and is refused with MSG-P4-002 |
| TC-E1-020-01 | AC1, BR1 | End to end | One case per product group and region in the synthetic set; package ALLOCATION "ALLOC-2026.11" |
| TC-E1-020-15 | Principle 5 | NFR | Decision log write forced to fail for every case in the run |
| TC-E1-020-08 | AC8, BR8 | End to end | The same run repeated for 2026-12-01 |
| TC-E1-020-02 | AC2, BR2 | End to end | Three owners with 120, 95 and 140 open cases, round robin |
| TC-E1-020-03 | AC3, BR3 | End to end | Next owner at 150 open cases |
| TC-E1-020-04 | AC4, BR4 | End to end | Every owner at 150 open cases |
| TC-E1-020-05 | AC5, BR5 | End to end | Product group SSME and region NE3 with no rule |
| TC-E1-020-06 | AC6, BR9 | End to end | Allocation run over the synthetic set; one log entry checked per case; log write forced to fail for one case |
| TC-E1-020-07 | AC7, BR6 | End to end | Case with deviation_open = true |
| TC-E1-020-09 | AC9 | End to end | No NEW cases |
| TC-E1-020-10 | AC10 | End to end | JOB-02 not complete for the business date |
| TC-E1-020-11 | AC11, BR8 | End to end | Two workers on the same case |
| TC-E1-020-12 | AC12, BR3 | End to end | Next owner at 149 open cases |
| TC-E1-020-13 | AC13, BR4 | End to end | Queue HP-CEN-CO with no overflow queue and every owner at 150 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Levels are mapped from the legacy values: System to End to end, Access to Component, Resilience to NFR. TC-E1-020-10 covers AC10, which is owned by RWB-P3-E1018-APP; the TC ID is kept here for the legacy trace and the test is executed with that story.

### 17. Guardrails

- **G1 No business value in code.** Product groups, regions, bands, queues, methods, caps and queue codes are data in the rule packages, the reference rows and the parameters.
- **G2 No personal data** in logs, tests, workflow history or prompts. Cases are named by case number only; search attributes are CaseId, Stage, ProductGroup and QueueCode.
- **G3 No other service's tables.** Every read and write is in schema `rwb_case` (DP-01); ACE data is not read here at all. Rule models arrive over the contract, not from rwb-decision's tables.
- **G4 One evaluator.** ALLOCATION and ASSIGNMENT are evaluated only through the embedded Drools kit with a fetched, checksum-verified model; no code compiles a workbook per call, and no code reads a rule table directly.
- **G5 Determinism.** No Drools call, database call, clock read, random or network call in workflow code; all of it is in activities, so a replay reuses the recorded answer.
- **G6 Decision before move.** The decision record, the case change and the outbox row are one transaction; a failed write leaves the case unchanged.
- **G7 The default row check is not repeated at run time**; it is at load in rwb-decision.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 18.3.2 | R-DEV-01 | TC-E1-020-01, TC-E1-020-02, TC-E1-020-09 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07, FEAT-CWC-09 | 18.3.2 | R-UNI-41 | TC-E1-020-01, TC-E1-020-05, TC-E1-020-07 |
| REQ-CWC-009 | Round robin, lowest load, named owner, cap and overflow | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-08 | 18.3.2 | R-UNI-19 | TC-E1-020-02, TC-E1-020-03, TC-E1-020-04, TC-E1-020-12, TC-E1-020-13 |
| REQ-CWC-016 | Every allocation logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 6.1 | R-UNI-39, R-UNI-40 | TC-E1-020-06, TC-E1-020-08, TC-E1-020-11, TC-E1-020-15 |

Legacy trace: story RWB-E1-020, module P3 Case and workflow, features FEAT-CWC-07, FEAT-CWC-08 and FEAT-CWC-09; the dropped criteria are AC10 (owned by RWB-P3-E1018-APP) and the manual transfer and rebalancing behaviour (RWB-P3-E1021-APP and the E1-030 rebalancing story).

### 19. Out of scope

- Manual transfer and reassignment screens and the `transfer` activity behaviour (RWB-P3-E1021-APP, RWB-E2-011, RWB-E2-012).
- Reallocation when an owner leaves or passes the cap, and daily rebalancing (R-UNI-18, R-UNI-19, Epic 2; JOB-06 in the E1-030 rebalancing story).
- The values of the caseload caps and the service levels (DL22, DL23).
- Loading, validating, approving and rolling back the ALLOCATION and ASSIGNMENT packages, and the default row check (rwb-decision, P7).
- The contract documents themselves (RWB-P3-E1020-CON) and the deployment of the worker, the schedule and the topics (RWB-P3-E1020-OPS).
- Placement on a queue by a model or an agent (RWB-E2-036).
